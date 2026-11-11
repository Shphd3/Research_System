from common import *
import torch,pandas as pd
from routing import score,group_scores,random_scores,set_scores
PAIRS=[(a,b) for a in range(8) for b in range(a+1,8)]
PAIRMAP=np.zeros((8,8),np.uint8)
for k,(a,b) in enumerate(PAIRS):PAIRMAP[a,b]=PAIRMAP[b,a]=k

def make_scores():
 frozen=torch.load(R4/'data/frozen.pt',map_location='cpu',weights_only=False);g=torch.load(R4/'data/atom_groups.pt',map_location='cpu',weights_only=False);group=g['group'].cuda();w=g['w'].cuda()
 for split in ['DEV','EVAL']:
  if (R/f'data/{split}_labels_fixed.npy').exists():continue
  d=torch.load(R4/f'data/{split}_codes.pt',map_location='cpu',weights_only=False)
  scores={a:np.lib.format.open_memmap(R/f'data/{split}_scores_{a}.npy',mode='w+',dtype=np.float32,shape=(N,8)) for a in ['A5','A1','A2']}
  labs=np.empty((N,3),np.uint8)
  for k in range(1024):
   sl=slice(k*2048,(k+1)*2048);i=d['indices'][sl].long().cuda();v=d['values'][sl].float().cuda()
   ss=[group_scores(i,v,group,w),score(i,v,frozen)[0],random_scores((1,2048,8),-1,k%4,k//4,'cuda').reshape(-1,8)]
   for j,a in enumerate(['A5','A1','A2']):
    scores[a][sl]=ss[j].cpu().numpy();sel=ss[j].topk(2).indices.cpu().numpy();labs[sl,j]=PAIRMAP[sel[:,0],sel[:,1]]
  for x in scores.values():x.flush()
  np.save(R/f'data/{split}_labels_fixed.npy',labs)
  print('SCORES',split,flush=True)

def extract(arm,step,splits,layers):
 m,cfg=load_model(arm,step);outweight=R/f'data/output_{arm}_{step}.pt'
 if not outweight.exists():torch.save(dict(output_weight=m.output_weight.detach().to('cpu',dtype=torch.bfloat16),norm_weight=m.norm.weight.detach().cpu(),eps=m.norm.eps),outweight)
 for split in splits:
  done=R/f'evidence/cache_{arm}_{step}_{split}.json'
  if done.exists():continue
  t=tokens(split);s1=np.load(R/f'data/{split}_scores_A1.npy',mmap_mode='r') if arm=='A1' else None
  hpath=R/f'data/h_{arm}_{step}_{split}.npy';h=np.lib.format.open_memmap(hpath,mode='w+',dtype=np.float16,shape=(N,1024));hs={l:np.lib.format.open_memmap(R/f'data/ffn_{arm}_{step}_L{l}_{split}.npy',mode='w+',dtype=np.float16,shape=(N,1024)) for l in layers};sel=np.lib.format.open_memmap(R/f'data/sel_{arm}_{step}_{split}.npy',mode='w+',dtype=np.uint8,shape=(8,N,2));diags=np.lib.format.open_memmap(R/f'data/route_{arm}_{step}_{split}.npy',mode='w+',dtype=np.float16,shape=(8,N,4));cap={};handles=[]
  for l in layers:handles.append(m.blocks[l].norm2.register_forward_hook(lambda mod,args,y,l=l:cap.__setitem__(l,y)))
  raw={}
  if arm in ['A0','A6']:
   for l,b in enumerate(m.blocks):handles.append(b.moe.router.register_forward_hook(lambda mod,args,y,l=l:raw.__setitem__(l,y)))
  tic=time.monotonic()
  with torch.inference_mode():
   for k in range(0,1024,2):
    sl=slice(k*2048,(k+2)*2048);x=torch.from_numpy(np.array(t[sl])).reshape(2,2048).long().cuda()
    set_scores(m,torch.from_numpy(np.array(s1[sl])).cuda() if s1 is not None else None)
    with torch.autocast('cuda',dtype=torch.bfloat16):pre,_=m.forward_features(x)
    h[sl]=pre.reshape(-1,1024).float().cpu().numpy()
    for l in layers:hs[l][sl]=cap[l].reshape(-1,1024).float().cpu().numpy()
    for l,b in enumerate(m.blocks):
     ids=b.moe.last_selected;sel[l,sl]=ids.cpu().numpy()
     if l in raw:
      p=raw[l].float().softmax(-1).reshape(-1,8);mass=p.gather(1,ids).sum(1);gates=p.gather(1,ids)/mass[:,None].clamp_min(torch.finfo(torch.float32).tiny);b0=p.topk(2).indices;flip=(b0.sort(1).values!=ids.sort(1).values).any(1)
      top3=p.topk(3).values;gap=top3[:,1]-top3[:,2]
      diags[l,sl]=torch.stack([gates.max(1).values,mass,flip.float(),gap],1).cpu().numpy()
     else:diags[l,sl]=0
    if k%128==0:print('FORWARD',arm,step,split,k,'sec',round(time.monotonic()-tic,1),flush=True)
  for hook in handles:hook.remove()
  for q in [h,sel,diags]+list(hs.values()):q.flush()
  paths=[hpath,outweight,R/f'data/sel_{arm}_{step}_{split}.npy',R/f'data/route_{arm}_{step}_{split}.npy']+[R/f'data/ffn_{arm}_{step}_L{l}_{split}.npy' for l in layers]
  register(f'representation_a5checks_{arm}_{step}_{split.lower()}_20261110',f'A5检查冻结{arm}{step} {split}表征',paths,dict(parent=str(model_path(arm,step)),split=split,position_count=N,hook='pre-final norm residual and norm2 FFN inputs',main_weights_updated=False),category='representation')
  dump(done,dict(arm=arm,step=step,split=split,gpu_seconds=time.monotonic()-tic,paths=list(map(str,paths))));print('CACHED',arm,step,split,flush=True)
 del m;torch.cuda.empty_cache()

if __name__=='__main__':
 import argparse
 a=argparse.ArgumentParser();a.add_argument('--stage',default='hosts');args=a.parse_args();torch.set_num_threads(4);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
 tic=time.monotonic()
 if args.stage=='hosts':
  make_scores();extract('A0',2000,['DEV','EVAL'],[0,2,4,7]);extract('A1',2000,['DEV','EVAL'],[])
  event('1前向','固定分发标签、A0/A1宿主pre-final-norm隐藏态缓存完成；主模型全部冻结。',time.monotonic()-tic)
 elif args.stage=='a6':extract('A6',2000,['EVAL'],[])
 elif args.stage=='early':
  deadline=time.monotonic()+600
  while not (R/'evidence/A0_500_restore.json').exists():
   assert time.monotonic()<deadline,'A0_500_ARCHIVE_RESTORE_NOT_READY'
   print('WAIT verified A0_500 archive copy',flush=True);time.sleep(5)
  for s in [500,1000]:extract('A0',s,['DEV','EVAL'],[0,2,4,7])
