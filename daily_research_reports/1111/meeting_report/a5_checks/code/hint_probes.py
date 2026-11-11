from common import *
import torch
from torch import nn
from torch.nn import functional as F
import pandas as pd
from torch.utils.tensorboard import SummaryWriter
from cache_forward import PAIRMAP

class Hint(nn.Module):
 def __init__(self):
  super().__init__();self.a=nn.Linear(1052,1024);self.b=nn.Linear(1024,1024);nn.init.zeros_(self.b.weight);nn.init.zeros_(self.b.bias)
 def forward(self,h,s):return h+self.b(F.gelu(self.a(torch.cat([h.float(),F.one_hot(s,28).float()],1))))

def label_matrix(split):
 z=np.load(R/f'data/{split}_labels_fixed.npy');a=np.load(R/f'data/sel_A0_2000_{split}.npy',mmap_mode='r')[7];return np.column_stack([z,PAIRMAP[a[:,0],a[:,1]]])
def final_norm(h,weight,eps):
 v=h.float();return (v*torch.rsqrt(v.square().mean(-1,keepdim=True)+eps)).to(h.dtype)*weight.to(h.dtype)
def prepare1a():
 from scipy.special import logsumexp
 labels={s:label_matrix(s) for s in ['DEV','EVAL']};y={s:np.array(tokens(s)[1:N+1],dtype=np.int64) for s in ['DEV','EVAL']};dd=docs('DEV');ids=np.unique(dd);rng=np.random.default_rng(SEED);rng.shuffle(ids);hold=np.isin(dd,ids[:len(ids)//5]);grid=[.0001,.001,.01,.1,1,10];rows=[]
 def counts(ss,yy):return np.bincount(ss.astype(np.int64)*VOCAB+yy,minlength=28*VOCAB).reshape(28,VOCAB)
 base_train=np.bincount(y['DEV'][~hold],minlength=VOCAB);base_all=np.bincount(y['DEV'],minlength=VOCAB)
 bv=[float(-np.log((base_train[y['DEV'][hold]]+a)/(base_train.sum()+a*VOCAB)).mean()) for a in grid];ab=grid[int(np.argmin(bv))];base=-np.log((base_all[y['EVAL']]+ab)/(N+ab*VOCAB));np.save(R/'data/unigram_eval_loss.npy',base)
 for j,a in enumerate(['A5','A1','A2','A0-L7']):
  c=counts(labels['DEV'][~hold,j],y['DEV'][~hold]);den=c.sum(1);s=labels['DEV'][hold,j];yy=y['DEV'][hold];val=[float(-np.log((c[s,yy]+alpha)/(den[s]+alpha*VOCAB)).mean()) for alpha in grid];alpha=grid[int(np.argmin(val))]
  c=counts(labels['DEV'][:,j],y['DEV']);s=labels['EVAL'][:,j];cond=-np.log((c[s,y['EVAL']]+alpha)/(c.sum(1)[s]+alpha*VOCAB));np.save(R/f'data/conditional_unigram_{a}.npy',cond)
  weights=np.load(R/'data/EVAL_bin_weights.npy',mmap_mode='r')
  for k in range(-1,10):
   w=np.ones(N) if k==-1 else weights[:,k];rows.append(dict(distribution=a,band='overall' if k==-1 else f'bin{k}',I_X=float(np.dot(base-cond,w)/w.sum()),unigram_nll=float(np.dot(base,w)/w.sum()),conditional_nll=float(np.dot(cond,w)/w.sum()),alpha=alpha,base_alpha=ab,internal_holdout_positions=int(hold.sum())))
  dump(R/f'evidence/unigram_alpha_{a}.json',dict(grid=grid,heldout_nll=val,selected=alpha,base_selected=ab,selection_split='DEV document20%; final refit full DEV'))
 table(pd.DataFrame(rows),'check1a_route_information','DEV内文档留出选加性平滑，全DEV重估，EVAL验证。A0-L7使用实际bias硬Top2；其余b0。I_X是条件unigram改善，不是对宿主独立的信息上界。')
 return labels

def run():
 torch.set_num_threads(4);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
 start=time.monotonic();labels=prepare1a();train_ids=np.random.default_rng(SEED).choice(N,524288,replace=False);perm={s:np.random.default_rng(SEED+(0 if s=='DEV' else 1)).permutation(N) for s in ['DEV','EVAL']};np.save(R/'data/hint_train_position_ids.npy',train_ids)
 rows=[];weights=np.load(R/'data/EVAL_bin_weights.npy',mmap_mode='r');target={s:np.array(tokens(s)[1:N+1],dtype=np.int64) for s in ['DEV','EVAL']}
 for host in ['A0','A1']:
  output=torch.load(R/f'data/output_{host}_2000.pt',map_location='cuda',weights_only=False);W=output['output_weight'].detach();normw=output['norm_weight'].detach();eps=output['eps'];hdev=np.load(R/f'data/h_{host}_2000_DEV.npy',mmap_mode='r');heval=np.load(R/f'data/h_{host}_2000_EVAL.npy',mmap_mode='r');htrain=torch.from_numpy(np.array(hdev[train_ids])).pin_memory()
  for j,a in enumerate(['A5','A1','A2','A0-L7']):
   losses={}
   for shuffled in [False,True]:
    name=f'{host}_{a}_'+('shuffled' if shuffled else 'real');done=R/f'evidence/probe_{name}.json'
    if done.exists():
     z=json.load(open(done));losses[shuffled]=z['means'];continue
    torch.manual_seed(SEED);torch.cuda.manual_seed_all(SEED);net=Hint().cuda();opt=torch.optim.AdamW(net.parameters(),lr=.001,betas=(.9,.999),eps=1e-8,weight_decay=.01);writer=SummaryWriter(str(R/f'probes/tb/{name}'));hist=[];tic=time.monotonic()
    train_s=labels['DEV'][perm['DEV'] if shuffled else np.arange(N),j][train_ids];train_y=target['DEV'][train_ids]
    net.train()
    for b in range(0,len(train_ids),1024):
     hh=htrain[b:b+1024].cuda(non_blocking=True);ss=torch.tensor(train_s[b:b+1024],device='cuda').long();yy=torch.tensor(train_y[b:b+1024],device='cuda');opt.zero_grad(set_to_none=True)
     with torch.autocast('cuda',dtype=torch.bfloat16):
      hp=net(hh,ss);hn=final_norm(hp,normw,eps);loss=F.cross_entropy(F.linear(hn,W).float(),yy)
     loss.backward();gn=torch.nn.utils.clip_grad_norm_(net.parameters(),1);opt.step();step=b//1024+1;val=float(loss);writer.add_scalar('train/lm_ce',val,step);writer.add_scalar('train/gradient_norm',float(gn),step);hist.append(dict(step=step,loss=val,gradient_norm=float(gn)))
     if step%64==0:print('PROBE_TRAIN',name,step,round(val,6),'sec',round(time.monotonic()-tic,1),flush=True)
    net.eval();sumv=np.zeros(11);denv=np.zeros(11);predloss=np.lib.format.open_memmap(R/f'data/probe_loss_{name}.npy',mode='w+',dtype=np.float32,shape=(N,));eval_s=labels['EVAL'][perm['EVAL'] if shuffled else np.arange(N),j]
    with torch.inference_mode():
     for b in range(0,N,1024):
      hh=torch.from_numpy(np.array(heval[b:b+1024])).cuda();ss=torch.tensor(eval_s[b:b+1024],device='cuda').long();yy=torch.tensor(target['EVAL'][b:b+1024],device='cuda')
      with torch.autocast('cuda',dtype=torch.bfloat16):hn=final_norm(net(hh,ss),normw,eps);ce=F.cross_entropy(F.linear(hn,W).float(),yy,reduction='none')
      v=ce.double().cpu().numpy();predloss[b:b+len(v)]=v;ww=np.column_stack([np.ones(len(v)),weights[b:b+len(v)]]);sumv+=v@ww;denv+=ww.sum(0)
    predloss.flush();means=(sumv/denv).tolist();losses[shuffled]=means;secs=time.monotonic()-tic
    torch.save(dict(probe=net.state_dict(),optimizer=opt.state_dict(),host=host,distribution=a,shuffled=shuffled,train_position_ids=str(R/'data/hint_train_position_ids.npy'),seed=SEED,updates=512,main_weights_updated=False),R/f'probes/{name}.pt');pd.DataFrame(hist).to_csv(R/f'probes/{name}_metrics.csv',index=False);writer.close();dump(done,dict(host=host,distribution=a,shuffled=shuffled,means=means,gpu_seconds=secs,train_positions=524288,test_positions=N,updates=512))
    print('PROBE_DONE',name,means[0],round(secs,2),flush=True);del net,opt;torch.cuda.empty_cache()
   I=pd.read_csv(R/'results/check1a_route_information.csv');I=I[I.distribution==a].set_index('band')
   for k,band in enumerate(['overall']+[f'bin{k}' for k in range(10)]):rows.append(dict(host=host,distribution=a,band=band,I_X=float(I.loc[band,'I_X']),real_probe_nll=losses[False][k],shuffled_probe_nll=losses[True][k],delta_hint=losses[True][k]-losses[False][k],train_positions=524288,test_positions=N,probe='residual MLP1024 onehot28; full-vocab frozen head'))
   table(pd.DataFrame(rows),'check1_hint_probes','宿主全部冻结；real/shuffled为同初始化、同训练位置和超参数的独立小探针；不是测试时仅打乱。A1宿主先前已用过A1分发，因此该格不满足“未用过该分发”的理想条件，按用户明确宿主矩阵保留。')
  del htrain,W,normw,output;torch.cuda.empty_cache()
 df=pd.DataFrame(rows);v=df[(df.host=='A0')&(df.band=='overall')].set_index('distribution').delta_hint;d=float(v['A5']);rule='泄露足以解释A5对A0全部优势，A5不能作为分工更好证据' if d>=.044 else '泄露不是主要解释' if d<=.010 else '无法区分'
 dump(R/'evidence/check1_complete.json',dict(delta_A5=d,rule=rule,extra_A5_minus_A1=float(v['A5']-v['A1']),ratio_to_01185=float((v['A5']-v['A1'])/.1185),gpu_seconds=time.monotonic()-start,judgment='Unknown'))
 event('1',f'A0宿主Δhint_A5={d:.6f} nat；规则套用：{rule}。',time.monotonic()-start)
if __name__=='__main__':run()
