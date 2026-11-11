from common import *
import torch,pandas as pd
from torch import nn
from torch.nn import functional as F
from scipy.optimize import linear_sum_assignment
from check45 import feature_matrix,mcalc,hardweights,pair_selection
from cache_forward import PAIRS
from torch.utils.tensorboard import SummaryWriter

class Dictionary(nn.Module):
 def __init__(self):
  super().__init__();self.encoder=nn.Linear(1024,8192);self.decoder=nn.Linear(8192,1024,bias=False)
  nn.init.normal_(self.decoder.weight,std=1/(1024**.5));self.decoder.weight.data/=self.decoder.weight.data.norm(dim=0,keepdim=True);self.encoder.weight.data.copy_(self.decoder.weight.data.T);nn.init.zeros_(self.encoder.bias)
 def codes(self,x):return F.relu(self.encoder(x)).topk(32,dim=-1,sorted=False)
 def forward(self,x):
  v,i=self.codes(x);z=torch.zeros(len(x),8192,device=x.device,dtype=v.dtype).scatter(1,i,v);return self.decoder(z),v,i

def kmeans(x,k,seed,iters=300):
 g=torch.Generator(device=x.device).manual_seed(seed);n=len(x);c=[x[int(torch.randint(n,(1,),generator=g,device=x.device))]]
 for _ in range(k-1):
  d=torch.cdist(x,torch.stack(c)).min(-1).values.square();c.append(x[int(torch.multinomial(d,1,generator=g))])
 c=torch.stack(c)
 for _ in range(iters):
  lab=torch.cdist(x,c).argmin(-1);new=torch.stack([x[lab==e].mean(0) if (lab==e).any() else c[e] for e in range(k)])
  if torch.allclose(new,c):break
  c=new
 return lab

def groups_from_codes(ii,vv):
 n=torch.bincount(ii[vv>0],minlength=8192).float();C=torch.zeros(8192*8192,device='cuda');
 for b in range(0,len(ii),16384):
  ids=ii[b:b+16384];good=vv[b:b+16384]>0;ids=torch.where(good,ids,-1);a=ids[:,:,None].expand(-1,32,32);c=ids[:,None,:].expand(-1,32,32);mask=(a>=0)&(c>=0)&(a!=c);keys=a[mask]*8192+c[mask];C.index_add_(0,keys,torch.ones(len(keys),device='cuda'))
 W=C.view(8192,8192)/(n[:,None]*n[None,:]).sqrt().clamp_min(1e-30);del C
 core=(n>=20).nonzero().flatten();Wc=W[core][:,core];deg=Wc.sum(1);keep=deg>0;core=core[keep];Wc=Wc[keep][:,keep];deg=deg[keep];S=Wc/deg.sqrt()[:,None]/deg.sqrt()[None,:];g=torch.Generator(device='cuda').manual_seed(2026110902);X=torch.randn(len(S),8,device='cuda',generator=g);evals,U=torch.lobpcg(S,k=8,X=X,largest=True,niter=2000,tol=1e-7);eigen_residual=((S@U-U*evals).norm(dim=0)/U.norm(dim=0).clamp_min(1e-30)).tolist();U=U/U.norm(dim=1,keepdim=True).clamp_min(1e-30);lab=kmeans(U,8,2026110902);del S,Wc,U
 group=torch.full((8192,),-1,device='cuda',dtype=torch.long);group[core]=lab;rest=(group<0).nonzero().flatten()
 if len(rest):
  best=W[rest][:,core].max(1);group[rest]=torch.where(best.values>0,lab[best.indices],torch.full_like(best.indices,-1))
 mass=torch.zeros(8192,device='cuda').index_add_(0,ii[vv>0],vv[vv>0]);p=n/len(ii);lp=(1/p.double().clamp_min(1e-300)).log();med=lp[p>0].median();weights=(lp/med).clamp(max=3).float();weights[p==0]=3
 def masses():return torch.stack([mass[group==e].sum() for e in range(8)])
 for j in (group<0).nonzero().flatten().tolist():group[j]=int(masses().argmin())
 before=masses().tolist();A=torch.stack([W[:,group==e].sum(1) for e in range(8)],1);moves=0
 for it in range(200000):
  m=masses();mean=m.mean()
  if float(((m-mean).abs()/mean).max())<=.2:break
  h=int(m.argmax());cand=(group==h).nonzero().flatten();own=A[cand,h];other=A[cand].clone();other[:,h]=-1;other[:,m>=mean]=-1;best=other.max(1);ratio=best.values/own.clamp_min(1e-30);target=best.indices;ok=best.values>=0
  if not ok.any():target=torch.full_like(target,int(m.argmin()));ratio=torch.zeros_like(ratio);ok[:]=True
  k=int(torch.where(ok,ratio,torch.full_like(ratio,-1)).argmax());j=int(cand[k]);t=int(target[k]);group[j]=t;A[:,h]-=W[:,j];A[:,t]+=W[:,j];moves+=1
 return group,weights,dict(dev_counts=n.cpu(),p=p.cpu(),laplacian_eigenvalues=(1-evals).tolist(),core_atoms=len(core),moves=moves,mass_before=before,mass_after=masses().tolist(),eigen_residual=eigen_residual,balance_stop='same original abs deviation<=20%; not hard 1.05 upper bound')

def get_codes(net,mm,mean,scale):
 ii=torch.empty((N,32),device='cuda',dtype=torch.long);vv=torch.empty((N,32),device='cuda',dtype=torch.float32);mse=den=0.
 with torch.inference_mode():
  for b in range(0,N,8192):
   x=torch.from_numpy(np.array(mm[b:b+8192])).float().cuda();x=(x-mean)/scale
   with torch.autocast('cuda',dtype=torch.bfloat16):re,v,i=net(x)
   ii[b:b+len(x)]=i;vv[b:b+len(x)]=v.float();mse+=float((re.float()-x).square().sum());den+=float(x.square().sum())
 return ii,vv,mse/den

def main():
 torch.set_num_threads(4);torch.backends.cuda.matmul.allow_tf32=False;start=time.monotonic();records=[];Fm=feature_matrix();ft=torch.load(erows('A0')[2000]['feature_artifact'],weights_only=False);p=ft['p_dev'].numpy();bins=ft['feature_bin'].numpy();a5labels=np.load(R/'data/EVAL_labels_fixed.npy')[:,0];a5pairs=np.array(PAIRS)[a5labels];target=np.array(tokens('EVAL')[1:N+1],np.int64);devy=np.array(tokens('DEV')[1:N+1],np.int64);base=np.load(R/'data/unigram_eval_loss.npy');grid=[.0001,.001,.01,.1,1,10]
 for step in [500,1000,2000]:
  for layer in [4,7]:
   name=f'A0_{step}_L{layer}';done=R/f'evidence/dictionary_{name}.json'
   if done.exists():records.append(json.load(open(done)));continue
   dev=np.load(R/f'data/ffn_A0_{step}_L{layer}_DEV.npy',mmap_mode='r');test=np.load(R/f'data/ffn_A0_{step}_L{layer}_EVAL.npy',mmap_mode='r');mean=np.zeros(1024,np.float64);sumsq=0.
   for b in range(0,N,8192):
    xx=np.asarray(dev[b:b+8192],np.float64);mean+=xx.sum(0);sumsq+=float((xx*xx).sum())
   mean/=N;scale=float(np.sqrt(sumsq/N/1024-(mean*mean).mean()));mu=torch.tensor(mean,device='cuda').float();torch.manual_seed(SEED);net=Dictionary().cuda();opt=torch.optim.Adam(net.parameters(),lr=.0003,betas=(.9,.999));writer=SummaryWriter(str(R/f'dictionaries/tb/{name}'));rng=np.random.default_rng(SEED);hist=[];tic=time.monotonic();order=None
   for s in range(10000):
    b=(s%(N//4096))*4096
    if b==0:order=rng.permutation(N)
    ids=order[b:b+4096];x=torch.from_numpy(np.array(dev[ids])).float().cuda();x=(x-mu)/scale;opt.zero_grad(set_to_none=True)
    with torch.autocast('cuda',dtype=torch.bfloat16):re,v,i=net(x);loss=(re.float()-x).square().mean()
    loss.backward();opt.step()
    with torch.no_grad():net.decoder.weight.div_(net.decoder.weight.norm(dim=0,keepdim=True).clamp_min(1e-12))
    if (s+1)%200==0:
     val=float(loss);active=int(i[v>0].unique().numel());hist.append(dict(step=s+1,reconstruction_mse=val,batch_active_atoms=active,seconds=time.monotonic()-tic));writer.add_scalar('train/reconstruction_mse',val,s+1);writer.add_scalar('train/batch_active_atoms',active,s+1);print('DICTIONARY',name,s+1,val,round(time.monotonic()-tic,1),flush=True)
    if time.monotonic()-tic>=1800:break
   trainsecs=time.monotonic()-tic;net.eval();ii,vv,devnmse=get_codes(net,dev,mu,scale);group,w,extra=groups_from_codes(ii,vv);devscores=torch.zeros(N,8,device='cuda').scatter_add_(1,group[ii],w[ii]*vv);devsel=devscores.topk(2).indices.cpu().numpy();del ii,vv,devscores
   ii,vv,nmse=get_codes(net,test,mu,scale);dead=float((torch.bincount(ii[vv>0],minlength=8192)==0).float().mean());scores=torch.zeros(N,8,device='cuda').scatter_add_(1,group[ii],w[ii]*vv);sel=scores.topk(2).indices.cpu().numpy();del ii,vv,scores
   overlap=np.zeros((8,8),np.int64)
   for x in range(2):
    for y in range(2):overlap+=np.bincount(sel[:,x]*8+a5pairs[:,y],minlength=64).reshape(8,8)
   row,col=linear_sum_assignment(-overlap);mapping=np.empty(8,int);mapping[row]=col;aligned=mapping[sel];over=(aligned[:,:,None]==a5pairs[:,None,:]).any(2).sum(1);M=mcalc(Fm,hardweights(sel),p);ds=np.sort(devsel,1);es=np.sort(sel,1);pm=np.zeros((8,8),np.uint8)
   for k,(a,b) in enumerate(PAIRS):pm[a,b]=pm[b,a]=k
   dl=pm[ds[:,0],ds[:,1]];el=pm[es[:,0],es[:,1]];doc=docs('DEV');uids=np.unique(doc);rs=np.random.default_rng(SEED);rs.shuffle(uids);hold=np.isin(doc,uids[:len(uids)//5]);ct=np.bincount(dl[~hold].astype(np.int64)*VOCAB+devy[~hold],minlength=28*VOCAB).reshape(28,VOCAB);valid=[float(-np.log((ct[dl[hold],devy[hold]]+a)/(ct.sum(1)[dl[hold]]+a*VOCAB)).mean()) for a in grid];alpha=grid[int(np.argmin(valid))];ct=np.bincount(dl.astype(np.int64)*VOCAB+devy,minlength=28*VOCAB).reshape(28,VOCAB);cl=-np.log((ct[el,target]+alpha)/(ct.sum(1)[el]+alpha*VOCAB));I=float((base-cl).mean())
   rec=dict(step=step,layer=layer,updates=s+1,training_seconds=trainsecs,total_gpu_seconds=time.monotonic()-tic,Mbar_median=float(np.nanmedian(M)),M_over_A5=float(np.nanmedian(M)/1.3449677106947389),top2_exact_after_hungarian=float((np.sort(aligned,1)==np.sort(a5pairs,1)).all(1).mean()),top2_overlap_fraction=float(over.mean()/2),at_least_one=float((over>0).mean()),I_X=I,unigram_alpha=alpha,eigen_residual_max=max(extra['eigen_residual']),balance_mass_min_rel=min(extra['mass_after'])/(sum(extra['mass_after'])/8),balance_mass_max_rel=max(extra['mass_after'])/(sum(extra['mass_after'])/8),balance_moves=extra['moves'],normalized_reconstruction_error=nmse,dev_normalized_error=devnmse,dead_atom_fraction=dead,**{f'bin{k}_M_median':float(np.nanmedian(M[bins==k])) for k in range(10)},rule='自举值得做' if np.nanmedian(M)>=1.08 else 'student早期表征不足' if np.nanmedian(M)<1.01 else '两阈值之间，无法区分')
   torch.save(dict(model=net.state_dict(),optimizer=opt.state_dict(),input_mean=mean,input_scale=scale,group=group.cpu(),w=w.cpu(),metadata=extra,updates=s+1,seed=SEED),R/f'dictionaries/{name}.pt');np.save(R/f'data/dictionary_{name}_selection.npy',sel);pd.DataFrame(hist).to_csv(R/f'dictionaries/{name}_metrics.csv',index=False);dump(done,rec);records.append(rec);table(pd.DataFrame(records),'check6b_bootstrap_atoms','字典只在DEV训练；student字典独立于teacher。teacher坐标M、匈牙利对齐及信息量只做EVAL诊断，不更新主模型。');writer.close();print('DICTIONARY_DONE',rec,flush=True);del net,opt,group,w;torch.cuda.empty_cache()
 dump(R/'evidence/check6b_complete.json',dict(rows=len(records),gpu_seconds=time.monotonic()-start));dump(R/'evidence/check6_complete.json',dict(conclusion='student可读性24探针与6个8192原子字典完成；逐配置判读见原表',rule='按10pp/60%与1.08/1.01逐项套用；不等同NLL收益',gpu_seconds=time.monotonic()-start));event('6b','6个student自举字典完成，按预登记M阈值逐项判断，未改任何主模型。',time.monotonic()-start)
if __name__=='__main__':main()
