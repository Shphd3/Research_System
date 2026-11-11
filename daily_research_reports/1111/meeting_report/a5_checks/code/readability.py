from common import *
import torch,pandas as pd
from torch import nn
from torch.nn import functional as F
from check45 import feature_matrix,mcalc,hardweights
from cache_forward import PAIRS
from torch.utils.tensorboard import SummaryWriter

class Probe(nn.Module):
 def __init__(self,kind):
  super().__init__();self.kind=kind;self.a=nn.Linear(1024,28 if kind=='linear' else 1024);self.b=nn.Linear(1024,28) if kind!='linear' else None
 def forward(self,h):
  a=self.a(h)
  if self.b is None:return a
  a=F.relu(a);v,i=a.topk(64,dim=-1);a=torch.zeros_like(a).scatter(1,i,v);return self.b(a)

def main():
 torch.set_num_threads(4);torch.backends.cuda.matmul.allow_tf32=False;start=time.monotonic();target=np.load(R/'data/DEV_labels_fixed.npy')[:,0];testtarget=np.load(R/'data/EVAL_labels_fixed.npy')[:,0];pairs=np.array(PAIRS);truepairs=pairs[testtarget];trainids=np.random.default_rng(SEED).choice(N,262144,replace=False);Fmat=feature_matrix();fa=torch.load(erows('A0')[2000]['feature_artifact'],weights_only=False);p=fa['p_dev'].numpy();results=[]
 for step in [500,1000,2000]:
  for layer in [0,2,4,7]:
   dev=np.load(R/f'data/ffn_A0_{step}_L{layer}_DEV.npy',mmap_mode='r');test=np.load(R/f'data/ffn_A0_{step}_L{layer}_EVAL.npy',mmap_mode='r');hh=torch.from_numpy(np.array(dev[trainids])).pin_memory()
   for kind in ['linear','mlp_topk64']:
    name=f'A0_{step}_L{layer}_{kind}';done=R/f'evidence/readability_{name}.json'
    if done.exists():results.append(json.load(open(done)));continue
    torch.manual_seed(SEED);net=Probe(kind).cuda();opt=torch.optim.AdamW(net.parameters(),lr=.001,betas=(.9,.999),eps=1e-8,weight_decay=.01);writer=SummaryWriter(str(R/f'probes/tb_readability/{name}'));tic=time.monotonic();hist=[]
    for epoch in range(3):
     order=np.random.default_rng(SEED+epoch).permutation(len(trainids))
     for b in range(0,len(order),1024):
      q=order[b:b+1024];x=hh[q].cuda();y=torch.tensor(target[trainids[q]],device='cuda').long();opt.zero_grad(set_to_none=True)
      with torch.autocast('cuda',dtype=torch.bfloat16):loss=F.cross_entropy(net(x).float(),y)
      loss.backward();gn=torch.nn.utils.clip_grad_norm_(net.parameters(),1);opt.step();s=epoch*256+b//1024+1;writer.add_scalar('train/classification_ce',float(loss),s);writer.add_scalar('train/gradient_norm',float(gn),s);hist.append(dict(step=s,loss=float(loss),gradient_norm=float(gn)))
    pred=np.empty(N,np.uint8);net.eval()
    with torch.inference_mode():
     for b in range(0,N,8192):
      x=torch.from_numpy(np.array(test[b:b+8192])).cuda()
      with torch.autocast('cuda',dtype=torch.bfloat16):v=net(x)
      pred[b:b+len(x)]=v.argmax(1).cpu().numpy()
    pp=pairs[pred];overlap=(pp[:,:,None]==truepairs[:,None,:]).any((1,2));M=mcalc(Fmat,hardweights(pp),p);row=dict(step=step,layer=layer,probe=kind,exact_set_accuracy=float((pred==testtarget).mean()),at_least_one_expert=float(overlap.mean()),mean_overlap_fraction=float((pp[:,:,None]==truepairs[:,None,:]).any(2).sum(1).mean()/2),Mbar_median=float(np.nanmedian(M)),gpu_seconds=time.monotonic()-tic,train_positions=len(trainids),test_positions=N)
    dump(done,row);results.append(row);np.save(R/f'data/readability_{name}_labels.npy',pred);torch.save(dict(model=net.state_dict(),kind=kind,step=step,layer=layer,seed=SEED,train_ids=trainids),R/f'probes/{name}.pt');pd.DataFrame(hist).to_csv(R/f'probes/{name}_metrics.csv',index=False);writer.close();print('READABILITY',row,flush=True);table(pd.DataFrame(results),'check6a_readability');del net,opt;torch.cuda.empty_cache()
   del hh
 df=pd.DataFrame(results);rules=[]
 for (s,l),z in df.groupby(['step','layer']):
  z=z.set_index('probe');dif=z.loc['mlp_topk64','exact_set_accuracy']-z.loc['linear','exact_set_accuracy'];rules.append(dict(step=s,layer=l,mlp_minus_linear=dif,above_10pp=bool(dif>.1),L7_above60=bool(l==7 and z.loc['mlp_topk64','exact_set_accuracy']>.6)))
 table(pd.DataFrame(rules),'check6a_rules','逐字规则作操作性判读；有限探针优势不证明所有线性router不可能；一致率不是NLL收益。')
 extraction_seconds=sum(json.load(open(q))['gpu_seconds'] for q in (R/'evidence').glob('cache_A0_*_*.json') if '2000' not in q.name);dump(R/'evidence/check6a_complete.json',dict(rows=len(results),gpu_seconds=time.monotonic()-start+extraction_seconds));event('6a','24个固定超参数student可读性探针完成；按10个百分点及L7>60%逐项判读，不把分类准确率等同训练收益。',time.monotonic()-start+extraction_seconds)
if __name__=='__main__':main()
