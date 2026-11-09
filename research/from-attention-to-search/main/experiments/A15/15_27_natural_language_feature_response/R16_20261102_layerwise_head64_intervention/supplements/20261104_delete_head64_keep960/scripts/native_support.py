"""Frozen Qwen single-layer PCA interventions; no training, native suffix continuation."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
import json,time,hashlib,traceback,argparse
import numpy as np
import torch
import transformers.utils as hu
import transformers.utils.import_utils as hi
for m in [hu,hi]:
 m.is_flash_attn_2_available=lambda:False;m.is_flash_attn_3_available=lambda:False;m.is_torchvision_available=lambda:False;m.is_librosa_available=lambda:False
from transformers import AutoModelForCausalLM
from tokenizers import Tokenizer
E=Path(__file__).resolve().parents[1];cfg=json.loads((E/'manifest.json').read_text());O=Path(cfg['parent_round']);M=Path(cfg['model_dir'])
def dump(p,x):
 p=Path(p);p.parent.mkdir(exist_ok=True,parents=True);t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(x,ensure_ascii=False,allow_nan=False)+'\n');t.replace(p)
def rows(p):return [json.loads(l) for l in Path(p).read_text().splitlines()]
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for x in iter(lambda:f.read(8<<20),b''):h.update(x)
 return h.hexdigest()
def init(rank):
 torch.set_num_threads(2);torch.cuda.set_device(rank);torch.backends.cuda.matmul.allow_tf32=False;torch.manual_seed(20261105)
 assert os.environ.get('RESOURCE_PROFILE')=='5090-2-spot'
 assert '5090' in torch.cuda.get_device_name(rank)
 for p,h in json.loads((E/'freeze.json').read_text())['sha256'].items():assert sha(p)==h,('source freeze',p)
 for p,h in cfg['input_sha256'].items():assert sha(p)==h,('input changed',p)
 model=AutoModelForCausalLM.from_pretrained(str(M),local_files_only=True,trust_remote_code=False,torch_dtype=torch.bfloat16,attn_implementation='sdpa').to(f'cuda:{rank}').eval()
 for p in model.parameters():p.requires_grad_(False)
 assert model.config.num_hidden_layers==28 and model.config.hidden_size==1024
 return model
class Native:
 def __init__(self,m,rank):self.m=m;self.dev=f'cuda:{rank}';self.layers=m.model.layers;self.tok=Tokenizer.from_file(str(M/'tokenizer.json'))
 def inputs(self,doc,batch=1):
  x=torch.zeros((batch,256),dtype=torch.long,device=self.dev);x[:,:192]=torch.tensor(doc['token_ids'],device=self.dev);mask=torch.zeros_like(x);mask[:,:192]=1
  return x,mask
 def body(self,x,mask,start=0,emb=None):
  self.m.model.layers=torch.nn.ModuleList(list(self.layers)[start:])
  try:return self.m.model(input_ids=x if emb is None else None,inputs_embeds=emb,attention_mask=mask,position_ids=torch.arange(256,device=self.dev)[None].expand(mask.shape[0],-1),use_cache=False,return_dict=True).last_hidden_state
  finally:self.m.model.layers=self.layers
 def decode(self,y):
  # Fixed16-row GEMM matches R13 decoder shape; accepts arbitrary number of targets.
  result=[]
  for lo in range(0,len(y),16):
   a=y[lo:lo+16];z=torch.zeros((16,1024),device=self.dev,dtype=torch.bfloat16);z[:len(a)]=a;result.append(self.m.lm_head(z)[:len(a)].float())
  return torch.cat(result)
 def capture(self,doc):
  cap={};handles=[]
  for l in range(28):
   def hk(mod,a,y,l=l):cap[l]=(y[0] if isinstance(y,tuple) else y).detach().clone()
   handles.append(self.layers[l].register_forward_hook(hk))
  x,mask=self.inputs(doc)
  try:out=self.body(x,mask)
  finally:
   for h in handles:h.remove()
  return out,cap
 def metrics(self,logits,full,targets,indices):
  lp=logits.log_softmax(-1);flp=full.log_softmax(-1);p=lp.exp();fp=flp.exp();v,ids=p.topk(10,-1);fi=full.argmax(-1);ii=torch.arange(len(targets),device=self.dev);yy=torch.tensor(targets,device=self.dev);out=[]
  for j,ind in enumerate(indices):
   threshold=logits[j].topk(10).values[-1];above=torch.where(logits[j]>threshold)[0];equal=torch.where(logits[j]==threshold)[0];chosen=torch.cat([above,equal[:10-len(above)]]);items=[{'id':int(k),'fragment':self.tok.decode([int(k)],skip_special_tokens=False),'probability':float(p[j,k])} for k in chosen];items.sort(key=lambda x:(-x['probability'],x['id']))
   out.append({'index':ind,'top1_id':int(logits[j].argmax()),'full_top1_id':int(fi[j]),'top1_agreement':bool(logits[j].argmax()==fi[j]),'full_top1_probability':float(p[j,fi[j]]),'full_top1_rank':int((logits[j]>logits[j,fi[j]]).sum()+1),'target_probability':float(p[j,yy[j]]),'target_rank':int((logits[j]>logits[j,yy[j]]).sum()+1),'NLL':float(-lp[j,yy[j]]),'KL_full':float((fp[j]*(flp[j]-lp[j])).sum()),'entropy':float(-(p[j]*lp[j]).sum()),'top10':items,'max_probability_tie_count':int((logits[j]==logits[j].max()).sum())})
  return out
 def project(self,h,mu,q):
  a=h.float()-mu;z=mu+(a@q)@q.T if q.shape[1] else mu.expand_as(a);return z.to(h.dtype)
def basis(l,dev):
 b=np.load(E/'data/bases'/f'layer{l+1:02d}.npz');return b,torch.tensor(b['mean'],device=dev,dtype=torch.float32),torch.tensor(b['V'][:,:64],device=dev,dtype=torch.float32)

def norms(h,z,mu,positions):
 a=h.float()-mu;b=z.float()-mu;per=(b.square().sum(-1)/a.square().sum(-1).clamp_min(1e-20));pert=(z.float()-h.float()).square().sum(-1).sqrt();rel=pert/h.float().square().sum(-1).sqrt().clamp_min(1e-20);out=[]
 for t in positions:out.append({'target_retained_energy':float(per[0,t]),'prefix_retained_energy':float(per[0,:t+1].mean()),'target_intervention_norm':float(pert[0,t]),'prefix_intervention_norm':float(pert[0,:t+1].mean()),'target_relative_intervention':float(rel[0,t]),'prefix_relative_intervention':float(rel[0,:t+1].mean())})
 return out
