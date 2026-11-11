"""Local first-order readout only. No optimizer or model/bias updates."""
import os
os.environ.setdefault('PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION','python')
from checkpoints import *
from torch.nn import functional as F
import gc,math
from threadpoolctl import threadpool_limits
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=2147483647;DIM=2**20
SOURCE_R=R
BATCH_SEQUENCES=int(os.environ.get('LF_BATCH_SEQUENCES','1'))
suffix=os.environ.get('LF_RUN_SUFFIX','')
if suffix:
 R=SOURCE_R/suffix
 for directory in ['evidence','gradient','logs']:(R/directory).mkdir(parents=True,exist_ok=True)
 (R/'evidence/checkpoint_inventory.json').write_text((SOURCE_R/'evidence/checkpoint_inventory.json').read_text())
 _table=table;_savefig=savefig
 def table(d,name,note=''):return _table(d,suffix+'/'+name,note)
 def savefig(fig,name,note):return _savefig(fig,suffix+'/'+name,note)
def make_batch(tokens,W,seqs,group):
 if isinstance(seqs,int):seqs=[seqs]
 x=torch.stack([torch.from_numpy(np.array(tokens[s*2048:(s+1)*2048])) for s in seqs]).long().cuda()
 y=torch.cat([torch.from_numpy(np.array(tokens[s*2048+1:(s+1)*2048+1])) for s in seqs]).long().cuda()
 w=torch.cat([torch.from_numpy(W[s*2048:(s+1)*2048,group]) for s in seqs]).cuda()
 return x,y,w
torch.backends.cuda.matmul.allow_tf32=False
torch.backends.cudnn.allow_tf32=False
def parameter_blocks(m,kind):
 out={'attention':[],'expert' if kind=='MoE' else 'FFN':[]}
 for n,p in m.named_parameters():
  if '.attn.' in n:out['attention'].append((n,p))
  elif ('.moe.experts.' in n if kind=='MoE' else any('.'+x+'.' in n for x in ['gate','up','down'])):out['expert' if kind=='MoE' else 'FFN'].append((n,p))
 for arr in out.values():
  for _,p in arr:p.requires_grad_(True)
 return out
def maps(blocks):
 rng=np.random.default_rng(20261111);out={}
 for block,arr in blocks.items():
  aa,bb,cc,dd=map(int,rng.integers(1,P,size=4));offset=0
  for n,p in arr:
   k=torch.arange(offset,offset+p.numel(),device='cuda',dtype=torch.int64);ix=(((k*aa+bb)%P)%DIM).to(torch.int32);sign=((((k*cc+dd)%P)%2)*2-1).to(torch.int8);out[n]=(ix,sign);offset+=p.numel()
 return out
def gradient(m,blocks,mapping,x,y,w):
 m.zero_grad(set_to_none=True)
 with torch.autocast('cuda',dtype=torch.bfloat16):
  _,h=m.forward_features(x);hs=h.reshape(-1,1024);total=hs.sum()*0
  # Recompute small head chunks duringbackward instead of retaining all logits.
  from torch.utils.checkpoint import checkpoint
  for i in range(0,len(y),128):
   def ce(a,weight,t,v):return (F.cross_entropy(F.linear(a,weight).float(),t,reduction='none')*v).sum()
   total+=checkpoint(ce,hs[i:i+128],m.output_weight,y[i:i+128],w[i:i+128],use_reentrant=False)
  total=total/w.sum()
 total.backward();out={};norms={}
 for block,arr in blocks.items():
  v=torch.zeros(DIM,device='cuda');norm=torch.zeros((),device='cuda',dtype=torch.float64)
  for n,p in arr:
   if p.grad is None:continue
   g=p.grad.detach().reshape(-1);norm+=(g.double()*g.double()).sum();ix,sign=mapping[n]
   v.index_add_(0,ix.long(),g*sign)
  out[block]=v.cpu().numpy();norms[block]=float(norm)
 return out,norms,float(total)
def raw_T(gram,weights=None):
 K=gram.shape[0];weights=np.ones(4) if weights is None else np.asarray(weights);w=weights[:,None]*weights[None,:];np.fill_diagonal(w,0);den=w.sum()
 if den==0:return np.full((K,K),np.nan),np.full(K,np.nan)
 cross=np.einsum('arbs,rs->ab',gram,w)/den;sig=np.diag(cross);valid=sig>0;T=np.full((K,K),np.nan);good=valid[:,None]&valid[None,:];T[good]=cross[good]/np.sqrt((sig[:,None]*sig[None,:])[good]);return T,sig
def summarize(G,groups,cooc,model,tokens,block):
 K=len(groups);flat=G.reshape(K*4,DIM).astype(np.float64);gram=(flat@flat.T).reshape(K,4,K,4);T,sig=raw_T(gram);pairs=[]
 for i in range(K):
  for j in range(K):pairs.append(dict(model=model,tokens=tokens,block=block,group_a=groups[i],group_b=groups[j],T=T[i,j],signal_a=sig[i],signal_b=sig[j],signal_sufficient=bool(sig[i]>0 and sig[j]>0),cooccurrence_lift=cooc[groups[i],groups[j]]))
 valid=[(i,j) for i in range(K) for j in range(i+1,K) if np.isfinite(T[i,j])];negative=np.mean([T[i,j]<0 for i,j in valid]) if valid else np.nan;rho=float(spearmanr([T[i,j] for i,j in valid],[cooc[groups[i],groups[j]] for i,j in valid]).statistic) if len(valid)>2 else np.nan
 def borrowing(T):
  v=[]
  for i,g in enumerate(groups):
   if g%2:continue
   same=groups.index(g+1);others=[j for j,h in enumerate(groups) if h%2 and h!=g+1 and np.isfinite(T[i,j])]
   if np.isfinite(T[i,same]) and others:v.append(T[i,same]-np.mean(T[i,others]))
  return np.mean(v) if v else np.nan
 point=borrowing(T);rng=np.random.default_rng(20261111);boot=[]
 for _ in range(2000):
  weights=rng.multinomial(4,np.full(4,.25));v,_=raw_T(gram,weights);boot.append(borrowing(v))
 boot=np.array(boot);good=np.isfinite(boot);ci=np.quantile(boot[good],[.025,.975]) if good.any() else [np.nan,np.nan]
 summary=dict(model=model,tokens=tokens,block=block,groups=K,valid_undirected_pairs=len(valid),negative_pair_fraction=negative,conflict_rule='几乎不存在需要隔离的冲突' if np.isfinite(negative) and negative<.05 else '负组对不少于5%' if np.isfinite(negative) else '信号不足',borrowing_difference=point,borrowing_ci_low=ci[0],borrowing_ci_high=ci[1],borrowing_rule='低频从共现高频借力' if ci[0]>0 else '分不出',valid_bootstrap_fraction=float(good.mean()),cooccurrence_spearman=rho,proxy_rule='共现可作互助代理（按规则）' if rho>=.3 else '未达到共现代理阈值',insufficient_groups=int((sig<=0).sum()))
 return pairs,summary,T
def main():
 start=time.monotonic();limit_seconds=3480 if suffix else 5280;deadline=start+limit_seconds;dev=codes('DEV');groups=torch.load(R4/'data/atom_groups.pt',map_location='cpu',weights_only=False);gi=groups['group'].numpy();fb=artifact('A0',2000)['feature_bin'].numpy();ii=dev['indices'].numpy();v=dev['values'].numpy();positive=v>0;labels=gi[ii]*2+(fb[ii]>=7);allowed=((fb[ii]<=2)|(fb[ii]>=7))&positive;W=np.stack([((labels==g)&allowed).sum(1)/32 for g in range(16)],1).astype(np.float32);mass=np.bincount(gi[ii].ravel(),weights=(v*groups['w'].numpy()[ii]).ravel(),minlength=8);largest=np.argsort(mass)[-2:];small=sorted(int(g*2+s) for g in largest for s in range(2));seqweight=W.reshape(1024,2048,16).sum(1);rng=np.random.default_rng(20261111);used=set();selection={}
 for g in range(16):
  candidates=np.array([x for x in range(1024) if x not in used]);prob=seqweight[candidates,g];prob=prob/prob.sum();chosen=rng.choice(candidates,4*BATCH_SEQUENCES,replace=False,p=prob);selection[g]=chosen.reshape(4,BATCH_SEQUENCES).tolist();used.update(chosen.tolist())
 dump(R/'evidence/gradient_batches.json',dict(sequence_ids=selection,largest_A5_groups=largest.tolist(),fallback_four_groups=small,group_name='A5group*2+0low/1high',global_sequence_disjoint=True,per_batch_sequences=BATCH_SEQUENCES,R=4,seed=20261111))
 active=W>0;co=(active.astype(np.float64).T@active)/N;prob=active.mean(0);co=co/np.maximum(prob[:,None]*prob[None,:],1e-30);table(pd.DataFrame(co,index=range(16),columns=range(16)).reset_index(),'fig2_cooccurrence_lift');del dev,ii,v,active
 inv=json.load(open(R/'evidence/checkpoint_inventory.json'));common=sorted(set(r['tokens'] for r in inv if r['model']=='Dense')&set(r['tokens'] for r in inv if r['model']=='MoE'));times=[min(common,key=lambda t:abs(t-1e9)),max(t for t in common if t<=1e10)];allpairs=[];summaries=[];matrices=[];group_scope=list(range(16));projected=None;toks=np.load(R4/'data/DEV_tokens.npy',mmap_mode='r')
 for t in times:
  for kind in ['MoE','Dense']:
   if time.monotonic()>=deadline:raise TimeoutError('90minute gradient budget before nextmodel')
   row=next(z for z in inv if z['model']==kind and z['tokens']==t);m,_=load(row,False);versions=[p._version for p in m.parameters()];bias=[b.moe.load_bias.clone() for b in m.blocks] if kind=='MoE' else [];blocks=parameter_blocks(m,kind);mapping=maps(blocks);Gs={b:[] for b in blocks};seen=[];normrows=[]
   # Benchmark before deciding the frozenfallback. The measuredfirst sample is
   # retained if its group is in the resulting scope.
   first=group_scope[0];seq=selection[first][0];x,y,ww=make_batch(toks,W,seq,first);tic=time.monotonic();sample,norms,ll=gradient(m,blocks,mapping,x,y,ww);elapsed=time.monotonic()-tic
   if projected is None:
    projected=elapsed*256+(time.monotonic()-start)*4;group_scope=small if projected>limit_seconds else list(range(16));dump(R/'evidence/gradient_timing.json',dict(first_gradient_seconds=elapsed,projected_all16_seconds=projected,selected_groups=group_scope,budget_seconds=limit_seconds))
   for g in group_scope:
    batches={b:[] for b in blocks}
    for rr,seq in enumerate(selection[g]):
     if time.monotonic()>=deadline:raise TimeoutError('90minute gradient budget reached')
     if g==first and rr==0:out=sample;nn=norms;loss=ll
     else:
      x,y,ww=make_batch(toks,W,seq,g);out,nn,loss=gradient(m,blocks,mapping,x,y,ww)
     for block in blocks:batches[block].append(out[block]);normrows.append(dict(model=kind,tokens=t,group=g,replicate=rr,block=block,exact_gradient_norm_squared=nn[block],projected_norm_squared=float(np.sum(out[block].astype(np.float64)**2)),loss=loss))
    for block in blocks:Gs[block].append(np.stack(batches[block]))
    seen.append(g);print('GRADIENT',kind,t,'group',g,'done','seconds',round(time.monotonic()-start),flush=True)
   assert [p._version for p in m.parameters()]==versions
   assert all(torch.equal(b,bk.moe.load_bias) for b,bk in zip(bias,m.blocks))
   table(pd.DataFrame(normrows),f'fig2_norm_audit_{kind}_{t}')
   for block,arr in Gs.items():
    G=np.stack(arr);np.save(R/f'gradient/{kind}_{t}_{block}_sketch.npy',G);pairs,summary,T=summarize(G,seen,co,kind,t,block);allpairs+=pairs;summaries.append(summary);matrices.append((kind,t,block,T,seen));table(pd.DataFrame(allpairs),'fig2_transfer_coefficients');table(pd.DataFrame(summaries),'fig2_rules')
   m.zero_grad(set_to_none=True);del m,mapping,Gs;gc.collect();torch.cuda.empty_cache()
 fig,axs=plt.subplots(4,2,figsize=(14,23));scat,saxs=plt.subplots(4,2,figsize=(13,17))
 for ax,sax,(kind,t,block,T,gs) in zip(axs.flat,saxs.flat,matrices):
  finite=np.abs(T[np.isfinite(T)]);limit=max(1,float(np.quantile(finite,.95))) if len(finite) else 1;im=ax.imshow(T,vmin=-limit,vmax=limit,cmap='coolwarm');lab=[f'{g//2}'+('H' if g%2 else 'L') for g in gs];ax.set_xticks(range(len(gs)),lab,rotation=90,fontsize=7);ax.set_yticks(range(len(gs)),lab,fontsize=7);ax.set_title(f'{kind} {t/1e9:g}B {block}; clipped {int((finite>limit).sum())} cells');fig.colorbar(im,ax=ax,fraction=.045)
  pp=[z for z in allpairs if z['model']==kind and z['tokens']==t and z['block']==block and z['group_a']<z['group_b']];sax.scatter([z['cooccurrence_lift'] for z in pp],[z['T'] for z in pp],alpha=.6);sax.axhline(0,c='grey',ls='--');sax.set(title=f'{kind} {t/1e9:g}B {block}',xlabel='DEV cooccurrence /independent expectation',ylabel='cross-replicate T');sax.grid(alpha=.2)
 savefig(fig,'图2_局部帮助与冲突','每格是不同DEV份之间投影梯度的归一化内积；分母信号非正为缺失。色标按95%绝对值界显示并明确标记裁剪，原始T表保留全部值；不等于实际训练效果。');savefig(scat,'图2_共现与帮助','各点是无向组对；与共现lift的相关为局部读数，不证明长期共同训练收益。')
 dump(R/'evidence/fig2_complete.json',dict(seconds=time.monotonic()-start,groups=group_scope,nodes=times,models=['MoE','Dense'],R=4,gradient_projection='fixedCountSketch2^20',training_updates=0,model_and_bias_unchanged=True));event('图2','局部只读梯度与共现散点完成',GPU_process_wall_seconds=time.monotonic()-start,groups=len(group_scope))
if __name__=='__main__':
 with threadpool_limits(limits=4):main()
