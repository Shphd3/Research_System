"""Read-only paired Dense activation collector; atomic content-addressed resume."""
from pathlib import Path
import json,hashlib,os,gc,time,argparse,datetime,sys
import numpy as np
import torch
from torch.nn.attention import sdpa_kernel,SDPBackend
ROOT=Path(__file__).resolve().parents[1]
MAN=json.load(open(ROOT/'manifest.json'));CFG=json.load(open(ROOT/'config.json'))
sys.path.insert(0,MAN['source_code_root'])
from dense_sae.model import Qwen3SAEConfig,Qwen3SAEForCausalLM

def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(16*1024*1024),b''):h.update(b)
 return h.hexdigest()
def js(p,d):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);q=p.with_suffix(p.suffix+'.partial');q.write_text(json.dumps(d,indent=2)+'\n');os.replace(q,p)
def save_array(p,a):
 q=p.with_suffix('.partial')
 with open(q,'wb') as f:np.save(f,a);f.flush();os.fsync(f.fileno())
 os.replace(q,p)
def native_load(row,device):
 t=time.time();digest=sha(row['state_path']);assert digest==row['state_sha256'],('PAYLOAD_HASH_MISMATCH',row['tokens'])
 p=torch.load(row['state_path'],weights_only=False,map_location='cpu',mmap=True)
 assert int(p['tokens_seen'])==row['tokens'] and int(p['optimizer_step'])==row['step'],('COUNTER_MISMATCH',row['tokens'])
 c=p['extra_training_state']['model_config'];assert c==row['architecture'],('ARCHITECTURE_MISMATCH',row['tokens'])
 with torch.device('meta'):m=Qwen3SAEForCausalLM(Qwen3SAEConfig.from_dict(c))
 m.load_state_dict(p['model'],strict=True,assign=True)
 m=m.to(device=device,dtype=torch.float32).eval();m.requires_grad_(False)
 del p;gc.collect();assert sum(x.numel() for x in m.parameters())==281431040
 return m,dict(state_sha256_verified=digest,tokens_seen=row['tokens'],optimizer_step=row['step'],strict_load='PASS',parameters=281431040,seconds=time.time()-t)

@torch.inference_mode()
def measure(model,panel,layers,geometry,smoke=False,batch=8):
 ids=panel['input_ids'];mask=panel['attention_mask']
 if smoke:
  if geometry:
   rows=np.r_[np.flatnonzero(panel['split']=='fit')[:4],np.flatnonzero(panel['split']=='test')[:4]]
  else:rows=np.arange(8)
 else:rows=np.arange(len(ids))
 out={f'layer{l}':[] for l in layers};checks=[];current={};hooks=[]
 def record(l):
  def hook(_m,_i,o):current[l]=o
  return hook
 for l in layers:
  if l!=7:hooks.append(model.blocks[l].register_forward_hook(record(l)))
 def pre_norm(_m,args):current['norm_input']=args[0]
 hooks.append(model.norm.register_forward_pre_hook(pre_norm))
 try:
  for start in range(0,len(rows),batch):
   ix=rows[start:start+batch];x=torch.tensor(ids[ix],dtype=torch.long,device='cuda');am=torch.tensor(mask[ix],device='cuda')
   with sdpa_kernel(SDPBackend.MATH):f=model.forward_intermediates(x,am)
   current[7]=f['final_raw_h'];checks.append(torch.equal(f['final_raw_h'],current['norm_input']))
   for l in layers:
    if geometry:a=current[l][:,panel['positions'],:]
    else:a=current[l][torch.arange(len(ix),device='cuda'),torch.tensor(panel['positions'][ix],device='cuda')]
    assert torch.isfinite(a).all(),('NONFINITE',start,l)
    out[f'layer{l}'].append(a.float().cpu().numpy())
   del f,x,am;current.clear()
  assert all(checks),'HOOK_MISMATCH'
 finally:
  for h in hooks:h.remove()
 return {k:np.concatenate(v) for k,v in out.items()},dict(records=len(rows),observations=len(rows)*(32 if geometry else 1),main_equals_final_norm_input=all(checks),layer_module_names={str(l):('model.norm input / final_raw_h' if l==7 else f'blocks.{l} output') for l in layers},forwards_batches=len(checks))

def cache_spec(row,smoke):
 layers=[0,3,7] if row['tokens'] in CFG['semantic_tokens'] else [7]
 spec=dict(checkpoint_payload=row['state_sha256'],checkpoint_manifest=row['manifest_sha256'],geometry_sha256=sha(ROOT/'data/geometry.npz'),bridge_sha256=sha(ROOT/'data/bridge.npz') if len(layers)>1 else None,layers=layers,smoke=smoke,preprocessing='own reference mean applied later;raw FP32 collection',precision=CFG['precision'],collector_sha256=sha(__file__))
 key=hashlib.sha256(json.dumps(spec,sort_keys=True).encode()).hexdigest();return layers,spec,key

def run(smoke=False):
 assert torch.cuda.is_available();name=torch.cuda.get_device_name(0);assert '5090' in name,('WRONG_GPU',name)
 assert torch.cuda.device_count()<=2,('RESOURCE_CEILING',torch.cuda.device_count())
 torch.set_num_threads(4);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
 torch.manual_seed(CFG['seed']);np.random.seed(CFG['seed'])
 geom=dict(np.load(ROOT/'data/geometry.npz',allow_pickle=False));bridge=dict(np.load(ROOT/'data/bridge.npz',allow_pickle=False))
 rows=MAN['checkpoints'];selected=[r for r in rows if r['tokens'] in CFG['semantic_tokens']] if smoke else rows
 index=[];began=time.time()
 for row in selected:
  assert time.time()-began<CFG['wall_hours']*3600,'WALL_CEILING'
  layers,spec,key=cache_spec(row,smoke);out=ROOT/('smoke_cache' if smoke else 'cache')/f"token_{row['tokens']:012d}_{key[:12]}";meta=out/'complete.json'
  if meta.exists():
   saved=json.load(open(meta));assert saved['cache_key']==key
   for f,dig in saved['files'].items():assert sha(out/f)==dig,('CACHE_CORRUPT',f)
   index.append(saved);print('REUSED',row['tokens'],flush=True);continue
  out.mkdir(parents=True,exist_ok=True);print('LOAD',row['tokens'],flush=True);m,load=native_load(row,'cuda')
  versions={n:p._version for n,p in m.named_parameters()};res,gchecks=measure(m,geom,layers,True,smoke)
  for k,v in res.items():save_array(out/f'geometry_{k}.npy',v)
  del res;gc.collect()
  bchecks=None
  if len(layers)>1:
   res,bchecks=measure(m,bridge,[7],False,smoke)
   for k,v in res.items():save_array(out/f'bridge_{k}.npy',v)
   del res
  assert all(p._version==versions[n] and p.grad is None and not p.requires_grad for n,p in m.named_parameters()),'WEIGHT_MUTATION'
  peak=int(torch.cuda.max_memory_allocated());del m;gc.collect();torch.cuda.empty_cache();torch.cuda.reset_peak_memory_stats()
  saved=dict(cache_key=key,cache_spec=spec,path=str(out),checkpoint=row['checkpoint'],tokens=row['tokens'],step=row['step'],load=load,geometry_checks=gchecks,bridge_checks=bchecks,gpu=name,torch=torch.__version__,cuda=torch.version.cuda,peak_cuda_allocated_bytes=peak,model_released=True,files={p.name:sha(p) for p in out.glob('*.npy')},completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
  js(meta,saved);index.append(saved);js(ROOT/('smoke_cache_index.json' if smoke else 'cache_index.json'),index)
  print('DONE',row['tokens'],'elapsed',round(time.time()-began,2),'released',flush=True)
 js(ROOT/('smoke_cache_index.json' if smoke else 'cache_index.json'),index)
 return index

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--smoke',action='store_true');args=p.parse_args()
 try:run(args.smoke)
 except BaseException as e:
  js(ROOT/'audit'/('smoke_failure.json' if args.smoke else 'formal_failure.json'),dict(error=repr(e),time=datetime.datetime.now(datetime.timezone.utc).isoformat()));raise
