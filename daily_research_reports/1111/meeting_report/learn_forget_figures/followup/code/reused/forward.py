from checkpoints import *
from torch.nn import functional as F
import gc
torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
def run(row):
 key=f"{row['model']}_{row['tokens']:012d}";out=R/f'positions/{key}.npz';rec=R/f'evidence/forward_{key}.json'
 if out.exists() and rec.exists():return
 tic=time.monotonic();m,info=load(row);versions=[p._version for p in m.parameters()];biases=[b.moe.load_bias.clone() for b in m.blocks] if row['model']=='MoE' else [];cap={};hooks=[]
 if row['model']=='MoE':
  for l,b in enumerate(m.blocks):hooks.append(b.moe.router.register_forward_hook(lambda mod,args,y,l=l,b=b:cap.__setitem__(l,(y.float().softmax(-1)+b.moe.load_bias).topk(2).indices)))
 toks=np.load(R4/'data/EVAL_tokens.npy',mmap_mode='r');loss=np.empty(N,np.float16);sel=np.empty((8,N,2),np.uint8) if biases else None;total=0.
 with torch.inference_mode():
  for k in range(0,1024,2):
   sl=slice(k*2048,(k+2)*2048);x=torch.from_numpy(np.array(toks[sl])).reshape(2,2048).long().cuda();y=torch.from_numpy(np.array(toks[k*2048+1:(k+2)*2048+1])).reshape(-1).long().cuda()
   with torch.autocast('cuda',dtype=torch.bfloat16):
    _,h=m.forward_features(x);ce=torch.cat([F.cross_entropy(F.linear(v,m.output_weight).float(),t,reduction='none') for v,t in zip(h.reshape(-1,1024).split(128),y.split(128))])
   loss[sl]=ce.cpu().numpy();total+=float(ce.double().sum())
   if sel is not None:
    for l in range(8):sel[l,sl]=cap[l].reshape(-1,2).cpu().numpy()
   if k%128==0:print('FORWARD',key,k,'seconds',round(time.monotonic()-tic,1),flush=True)
 assert versions==[p._version for p in m.parameters()]
 assert all(torch.equal(b,bk.moe.load_bias) for b,bk in zip(biases,m.blocks))
 for h in hooks:h.remove()
 tmp=out.with_suffix('.partial.npz');np.savez(tmp,loss=loss,**({'sel':sel} if sel is not None else {}));tmp.replace(out)
 info.update(row=row,NLL=total/N,positions=N,bias_unchanged=True,model_unchanged=True,training_updates=0,GPU_seconds=time.monotonic()-tic,torch=torch.__version__,device=str(torch.cuda.get_device_properties(0)),position_sha256=sha(out));dump(rec,info);event('前向',key+'完成',NLL=info['NLL'],GPU_seconds=info['GPU_seconds']);del m;gc.collect();torch.cuda.empty_cache()
def main():
 rows=json.load(open(R/'evidence/checkpoint_inventory.json'))
 for row in sorted(rows,key=lambda z:(z['tokens'],z['model'])):
  if row['exists']:run(row)
 dump(R/'evidence/forward_complete.json',dict(time_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),checkpoints=len(rows),training_updates=0))
if __name__=='__main__':main()
