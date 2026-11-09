from common import *
import numpy as np,torch,torch.nn.functional as F,sys,importlib.util,time,os
import transformers.utils as hfu,transformers.utils.import_utils as hfi
for m in [hfu,hfi]:
 for n in ['is_flash_attn_2_available','is_flash_attn_3_available','is_torchvision_available','is_librosa_available']:setattr(m,n,lambda:False)
from transformers import AutoModelForCausalLM
plan=json.load(open(R/'frozen_plan.json'));pp=rows(R/'data/panel.jsonl');assert not (R/'cache/activations.npz').exists()
for p,h in json.load(open(R/'evidence/protocol_freeze.json'))['hashes'].items():assert sha(p)==h
torch.set_num_threads(2);torch.set_num_interop_threads(1);torch.manual_seed(plan['seed']);start=time.time()
model=AutoModelForCausalLM.from_pretrained(plan['model'],torch_dtype=torch.float32,local_files_only=True,attn_implementation='sdpa').cpu().eval().requires_grad_(False);model.config.use_cache=False;saes={};out={s:{k:[] for k in ['indices','values','active_count','z_L2','h_L2','relative_reconstruction_error']} for s in SITES};decoder_norm={};checks=[]
for s,ss in plan['sites'].items():
 spec=importlib.util.spec_from_file_location('s08_'+s,ss['loader']);mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod);sae=mod.TopKSAE.from_pretrained(ss['path'],map_location='cpu').eval().requires_grad_(False);assert (sae.d_model,sae.n_latents,sae.k)==(1024,30000,32);saes[s]=sae;decoder_norm[s]=sae.decoder.weight.detach().norm(dim=0).numpy()
dump(R/'evidence/started.json',dict(UTC=now(),pid=os.getpid(),device='CPU',threads=2,shape=[8,128],documents=len(pp),sampled_positions_per_document=8,auxiliary_positions=[31,15],amendment_sha256=sha(R/'amendment_fixed16.json'),code_sha256=sha(__file__)))
@torch.inference_mode()
def capture(batch,hooks_on=True,truncated32=False):
 xx=torch.zeros(8,128,dtype=torch.long);mask=torch.zeros_like(xx);pos=[];caps={};hooks=[]
 for j in range(8):
  p=batch[min(j,len(batch)-1)];ids=p['input_ids'][:32] if truncated32 else p['input_ids'];xx[j,:len(ids)]=torch.tensor(ids);mask[j,:len(ids)]=1;pos.append(p['positions']+[31 if p['fixed32_position'] is not None else 0,15])
 pos=torch.tensor(pos);ii=torch.arange(8)[:,None]
 def grab(s,y):caps[s]=y[ii,pos].detach().clone()
 if hooks_on:hooks=[model.model.layers[27].self_attn.o_proj.register_forward_hook(lambda m,a,y:grab('ATTN_SAE',y)),model.model.layers[27].mlp.register_forward_pre_hook(lambda m,a:grab('MLPIN_SAE',a[0]))]
 try:y=model.model(input_ids=xx,attention_mask=mask,use_cache=False,return_dict=True).last_hidden_state
 finally:
  for h in hooks:h.remove()
 return caps,y
for lo in range(0,len(pp),8):
 batch=pp[lo:lo+8];caps,y=capture(batch)
 if lo==0:
  _,plain=capture(batch,False);no=float((plain-y).abs().max());assert no==0;cc,_=capture(batch,truncated32=True);prefix={s:float((caps[s][:,8]-cc[s][:,8]).abs().max()) for s in SITES};assert max(prefix.values())<1e-4;checks.append(dict(noop_max=no,fixed32_prefix_equivalence=prefix))
 for s,sae in saes.items():
  h=caps[s][:len(batch)].reshape(-1,1024)
  with torch.inference_mode():
   values,ids,z,pre=sae.encode_topk(h);assert torch.isfinite(values).all();active=z>0
   if lo==0:
    vv,jj=pre.relu().topk(32,sorted=False);ref=torch.zeros_like(pre).scatter(-1,jj,vv);assert torch.equal(z,ref)
   # Decoder is linear on sparse coordinates; this avoids multiplying a mostly-zero30000-vector.
   rec=(sae.decoder.weight.T[ids]*values[:,:,None]).sum(1)+sae.decoder.bias;err=(h-rec).norm(dim=1)/h.norm(dim=1)
   dd=dict(indices=ids.numpy().astype(np.int32),values=values.numpy(),active_count=active.sum(1).numpy().astype(np.int16),z_L2=z.norm(dim=1).numpy(),h_L2=h.norm(dim=1).numpy(),relative_reconstruction_error=err.numpy())
   for k,v in dd.items():out[s][k].append(v.reshape(len(batch),10,*v.shape[1:]))
 if lo%64==0:print('CAPTURE',lo+len(batch),'/',len(pp),'seconds',round(time.time()-start,2),flush=True)
payload=dict(ids=np.array([p['id'] for p in pp]),fixed32_valid=np.array([p['fixed32_position'] is not None for p in pp]))
for s,dd in out.items():
 for k,v in dd.items():payload[s+'__'+k]=np.concatenate(v)
 payload[s+'__decoder_norm']=decoder_norm[s]
np.savez_compressed(R/'cache/activations.npz',**payload)
dump(R/'evidence/extraction_complete.json',dict(UTC=now(),status='COMPLETED',documents=len(pp),main_positions=len(pp)*8,auxiliary_fixed32_valid=sum(p['fixed32_position'] is not None for p in pp),seconds=time.time()-start,CPU_threads=2,GPU=0,model_trainable=0,SAE_trainable=0,hook_checks=checks,code_sha256=sha(__file__),cache_sha256=sha(R/'cache/activations.npz'),data_sha256=sha(R/'data/panel.jsonl')))
print('EXTRACTION_COMPLETE',time.time()-start,flush=True)
