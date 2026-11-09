from pathlib import Path
import os,sys,time,json,hashlib,gc,types
import numpy as np
import torch
from tokenizers import Tokenizer
E=Path(__file__).resolve().parents[1];CC=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder');M=Path('/data/250010109/model_cache/Qwen3-0.6B-Base-official')
# CPU read-only exact inference adaptation inherited from R14; do not touch local H100.
os.environ['CUDA_VISIBLE_DEVICES']='';torch.cuda.is_available=lambda:False
import transformers.utils as hfu,transformers.utils.import_utils as hfi
for mod in [hfu,hfi]:
 mod.is_flash_attn_2_available=lambda:False
 mod.is_flash_attn_3_available=lambda:False
 mod.is_torchvision_available=lambda:False
 mod.is_librosa_available=lambda:False
from transformers import AutoModelForCausalLM
sys.path.insert(0,str(CC));from crosscoder.model import CrossCoderConfig
from crosscoder.fast_batchtopk_a21 import FastBatchTopKCrossCoder
from crosscoder.batchtopk_a18 import CenteredRMSStats
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(8<<20),b''):h.update(b)
 return h.hexdigest()
def dump(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def save(p,**x):
 p=Path(p);tmp=p.with_suffix('.tmp')
 with tmp.open('wb') as f:np.savez_compressed(f,**x)
 tmp.replace(p)
@torch.inference_mode()
def main():
 t0=time.time();torch.set_num_threads(2);torch.manual_seed(110203)
 fr=json.load(open(E/'freeze.json'))
 for p,s in fr['sha256'].items():assert sha(p)==s,('freeze',p)
 cfg=json.load(open(E/'config.json'));assert sha(M/'model.safetensors')==fr['model_sha256_expected'];assert sha(cfg['crosscoder_checkpoint'])==fr['CC_sha256_expected'];docs=[json.loads(l) for l in (E/'data/documents.jsonl').read_text().splitlines()]
 model=AutoModelForCausalLM.from_pretrained(str(M),torch_dtype=torch.bfloat16,attn_implementation='sdpa',local_files_only=True).cpu().eval().requires_grad_(False);model.config.use_cache=False
 cp=torch.load(cfg['crosscoder_checkpoint'],map_location='cpu',weights_only=False,mmap=True)
 cc=FastBatchTopKCrossCoder(CrossCoderConfig(n_layers=14,hidden_size=1024,dict_size=16384,init_encoder_norm=1/np.sqrt(14)),device='meta',compute_dtype='bfloat16');cc.load_state_dict(cp['crosscoder'],assign=True,strict=True);cc=cc.cpu().eval().requires_grad_(False);cc._gemm_context=types.MethodType(lambda self,x:torch.autocast(device_type='cpu',dtype=torch.bfloat16),cc)
 stats=CenteredRMSStats.from_state_dict(cp['normalization']);del cp;gc.collect();nw=cc.decoder_norm_weights().detach();threshold=float(cc.threshold);assert abs(threshold-.051281172782182693)<1e-12
 D=cc.decoder[-1].float()*float(stats.rms[-1]);bias=cc.decoder_bias[-1].float()*float(stats.rms[-1])+stats.train_mean[-1].float();np.savez(E/'data/decoder_last_scale.npz',D=D.numpy(),bias=bias.numpy(),cc_rms=stats.rms.numpy(),cc_mean=stats.train_mean[-1].numpy())
 selected=np.array(cfg['candidate_features']);np.save(E/'data/selected_decoder.npy',D[selected].numpy())
 meta={'model_class':model.__class__.__name__,'layers':len(model.model.layers),'hidden':model.config.hidden_size,'vocab':model.config.vocab_size,'lm_head_shape':list(model.lm_head.weight.shape),'embedding_tied':model.lm_head.weight.data_ptr()==model.model.embed_tokens.weight.data_ptr(),'bias':None if model.lm_head.bias is None else model.lm_head.bias.detach().tolist(),'final_norm_eps':model.model.norm.variance_epsilon,'A22_layers':cfg['layers'],'threshold':threshold,'normalization':'frozen TRAIN centered vector RMS','actual_device':'CPU2threads;BF16model/encoder;FP32raw decoder;FP64geometry','local_H100_used':False};dump(E/'audit/model_interface.json',meta)
 def forward(doc,cut=None,native=False):
  ids=doc['token_ids'];x=torch.zeros((1,512),dtype=torch.long);x[0,:len(ids)]=torch.tensor(ids);mask=torch.zeros_like(x);mask[:,:len(ids)]=1
  if cut is not None:x[:,cut+1:]=0;mask[:,cut+1:]=0
  caps={};hh=[]
  for j,layer in enumerate(cfg['layers']):
   def hook(m,a,y,k=j):caps[k]=(y[0] if isinstance(y,tuple) else y)[0].detach()
   hh.append(model.model.layers[layer].register_forward_hook(hook))
  try:
   out=model(input_ids=x,attention_mask=mask,use_cache=False,return_dict=True) if native else model.model(input_ids=x,attention_mask=mask,use_cache=False,return_dict=True)
   if native:return torch.stack([caps[k] for k in range(14)],1).float(),out.logits[0].float(),None
   return torch.stack([caps[k] for k in range(14)],1).float(),None,out.last_hidden_state[0].float()
  finally:
   for h in hh:h.remove()
 def encode(h):
  x=torch.zeros((1024,14,1024),dtype=torch.float32);x[:len(h)]=stats.normalize(h);u=cc._post_relu(x);return (u*(u.float()*nw>cc.threshold))[:len(h)].float()
 # New shape/text check only; no historical sweep repeated.
 if not (E/'audit/smoke.json').exists():
  checks=[]
  for doc in [x for x in docs if x['split']=='discovery'][:3]:
   h,logits,_=forward(doc,native=True);h2,_,y=forward(doc);p=doc['positions'][len(doc['positions'])//2];hc,_,yc=forward(doc,cut=p);z=encode(h[doc['positions']]);z2=encode(h2[doc['positions']]);recon=z@D+bias;res=h[doc['positions'],-1]-recon
   fullhead=model.lm_head(model.model.norm(h[:,-1].to(torch.bfloat16))).float();native_y=model.model.norm(h[:,-1].to(torch.bfloat16)).float();sparse=z.numpy();rr,ii=np.nonzero(sparse);recovered=np.zeros_like(sparse);recovered[rr,ii]=sparse[rr,ii]
   target=torch.tensor(doc['token_ids'][1:]);a=torch.log_softmax(logits[:-1],1);b=torch.log_softmax(fullhead[:-1],1);n=len(target)
   e={'doc_id':doc['doc_id'],'native_logit_max':float((fullhead-logits).abs().max()),'native_target_logp_max':float((a[:n][torch.arange(n),target]-b[:n][torch.arange(n),target]).abs().max()),'norm_after_y_max':float((native_y-y).abs().max()),'causal_h_max':float((h[p]-hc[p]).abs().max()),'causal_y_max':float((y[p]-yc[p]).abs().max()),'cache_h_replay_max':float((h-h2).abs().max()),'encoder_replay_max':float((z-z2).abs().max()),'sparse_roundtrip_max':float(np.max(abs(sparse-recovered))),'ledger_max':float((recon+res-h[doc['positions'],-1]).abs().max())};e['pass']=e['native_logit_max']<=.5 and e['native_target_logp_max']<=.05 and all(e[k]==0 for k in ['norm_after_y_max','causal_h_max','causal_y_max','cache_h_replay_max','encoder_replay_max','sparse_roundtrip_max']) and e['ledger_max']<=1e-4;checks.append(e)
  dump(E/'audit/smoke.json',{'pass':all(x['pass'] for x in checks),'checks':checks,'time_seconds':time.time()-t0,'forwards':9,'gate':'before any formal cache'});print('SMOKE',json.dumps(checks),flush=True)
 assert json.load(open(E/'audit/smoke.json'))['pass'],'failed new-text smoke'
 # Head parameter geometry independent of validation positions and labels.
 if not (E/'analysis/head_geometry.npz').exists():
  t=time.time();W=model.lm_head.weight;V,H=W.shape;G=np.zeros((H,H),np.float64);s=np.zeros(H,np.float64)
  for lo in range(0,V,2048):w=W[lo:lo+2048].double().numpy();G+=w.T@w;s+=w.sum(0)
  mean=s/V;Gc=G-V*np.outer(mean,mean);eval_raw,Uraw=np.linalg.eigh(G);ev,U=np.linalg.eigh(Gc);ix=np.argsort(ev)[::-1];ixr=np.argsort(eval_raw)[::-1];ev=ev[ix];U=U[:,ix];eval_raw=eval_raw[ixr];Uraw=Uraw[:,ixr]
  gram_res=np.linalg.norm(Gc@U-U*ev)/np.linalg.norm(Gc);rng=np.random.default_rng(110205);ds=rng.normal(size=(4,H));direct=[]
  for d in ds:
   acc=0.
   for lo in range(0,V,4096):v=(W[lo:lo+4096].double().numpy()-mean)@d;acc+=float(v@v)
   direct.append(abs(acc-d@Gc@d)/max(acc,1e-12))
  save(E/'analysis/head_geometry.npz',G=G,Gc=Gc,vocab_mean=mean,eigenvalues=ev,U=U,raw_eigenvalues=eval_raw,raw_U=Uraw,final_norm_weight=model.model.norm.weight.float().numpy(),norm_eps=np.array(model.model.norm.variance_epsilon))
  dump(E/'audit/head_geometry.json',{'shape':list(W.shape),'raw_rank':int((eval_raw>eval_raw[0]*1e-10).sum()),'centered_rank':int((ev>ev[0]*1e-10).sum()),'eigen_residual':float(gram_res),'direct_Gram_relative_errors':direct,'word_mean_subtraction_changes_probabilities':'only uniform logit shift removed','elapsed':time.time()-t});print('HEAD_GEOMETRY',time.time()-t,flush=True)
 for i,doc in enumerate(docs):
  dest=E/'cache'/(doc['doc_id']+'.npz')
  if dest.exists():
   a=np.load(dest);assert str(a['freeze_hash'])==sha(E/'freeze.json');continue
  t=time.time();h,_,y=forward(doc);pp=doc['positions'];hs=h[pp];z=encode(hs);rec=z@D+bias;rr,ii=np.nonzero(z.numpy());vals=z.numpy()[rr,ii];rowptr=np.r_[0,np.cumsum(np.bincount(rr,minlength=len(pp)))].astype(np.int32)
  save(dest,h=hs[:,-1].numpy(),y=y[pp].numpy(),z_selected=z[:,selected].numpy(),z_indices=ii.astype(np.uint16),z_values=vals,z_indptr=rowptr,positions=np.array(pp),input_ids=np.array(doc['token_ids']),reconstruction=rec.numpy(),freeze_hash=np.array(sha(E/'freeze.json')))
  if i%10==0:print(json.dumps({'completed':i+1,'documents':len(docs),'last_doc_seconds':time.time()-t,'elapsed':time.time()-t0}),flush=True)
 # Numerical extraction completed; no validation response analysis performed here.
 dump(E/'terminal_extraction.json',{'status':'COMPLETED','documents':len(docs),'positions':sum(len(x['positions']) for x in docs),'seconds':time.time()-t0,'CPU_threads':2,'GPU_used':0,'training_updates':0,'validation_response_statistics_opened':False});print('EXTRACTION_COMPLETE',time.time()-t0,flush=True)
if __name__=='__main__':main()
