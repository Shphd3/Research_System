from fu import *
from threadpoolctl import threadpool_limits
def concentration(Fx,ct,t):
 p=F/f'data/M_{t}.npy'
 if p.exists():return np.load(p)
 sel=np.load(ROOT/f'positions/MoE_{t:012d}.npz')['sel'];out=[]
 for l in range(8):
  Y=np.zeros((N,8),np.float32);Y[np.arange(N)[:,None],sel[l]]=1;u=Y.mean(0)/2;q=np.asarray(Fx.T@Y)/np.maximum(2*ct[:,None],1);out.append(2*(q**3/np.maximum(u[None,:],1e-30)).sum(1))
 out=np.stack(out);np.save(p,out);return out
def decile_sets(ok,M,fb):
 out=[]
 for name,z in [('overall',ok),('low',ok&(fb<=2)),('high',ok&(fb>=7))]:
  ids=np.flatnonzero(z);ids=ids[np.lexsort((ids,M[ids]))]
  for q,group in enumerate(np.array_split(ids,10)):out.append((name,q+1,group))
 # Common boundaries provide an explicit sensitivity to within-band deciles.
 ids=np.flatnonzero(ok);ids=ids[np.lexsort((ids,M[ids]))]
 for q,group in enumerate(np.array_split(ids,10)):
  for name,z in [('common_low',fb<=2),('common_high',fb>=7)]:out.append((name,q+1,group[z[group]]))
 return out
def monotonic(d):
 if len(d)!=10:return False,0,np.nan
 v=d.sort_values('decile').G_mean.to_numpy();n=int((np.diff(v)>=0).sum());r=float(spearmanr(np.arange(10),v).statistic);return n>=7 and r>=.8,n,r
def main():
 start=time.monotonic();Fx,_=features('EVAL');ct=np.asarray(Fx.sum(0)).ravel();fb,p,ag=metadata();lp=np.log(np.maximum(p,1e-30));dd=docs();D=int(dd.max())+1;rng=np.random.default_rng(20261111);W=rng.multinomial(D,np.full(D,1/D),size=2000).astype(np.float32);S={a:states(a) for a in ['Dense','MoE']};ms={t:concentration(Fx,ct,t) for t in [500000000,1000000000,10000000000]};correlations=[];deciles=[];rules=[];allraw={}
 for t,m in ms.items():table(pd.DataFrame(dict(atom=np.arange(30000),bin=fb,count_EVAL=ct,**{f'M_layer{l}':m[l] for l in range(8)},M_mean=m.mean(0))),f'raw/M_layers_{t}','EVALfrequencydenominator;actualbaselineTop2;allEVALpositions.')
 for ref in REFS:
  learn=refmask(ref);C=doc_features(Fx,learn,dd);np.save(F/f'data/learnable_{ref}.npy',learn);counts=np.asarray(C.sum(1)).ravel();ok=counts>=50;Diffs={};details={};sets={};boot={};missing={}
  for t in ms:
   ti=TIMES.index(t);cd=np.asarray(Fx.T@(learn&S['Dense'][ti]).astype(np.float32)).ravel();cm=np.asarray(Fx.T@(learn&S['MoE'][ti]).astype(np.float32)).ravel();kd=cd/np.maximum(counts,1);km=cm/np.maximum(counts,1);g=km-kd;M=ms[t].mean(0);x=np.log(np.maximum(M,1e-30));details[t]=(g,kd,km,M,cd,cm);sets[t]=decile_sets(ok,M,fb);boot[t]=np.empty((len(sets[t]),2000),np.float64);missing[t]=np.zeros(len(sets[t]));diff=(S['MoE'][ti].astype(np.int8)-S['Dense'][ti].astype(np.int8)).astype(np.float32);Diffs[t]=doc_features(Fx,learn&(diff!=0),dd,diff)
   for l in [-1]+list(range(8)):
    xx=x if l<0 else np.log(np.maximum(ms[t][l],1e-30))
    for b in range(-1,10):
     z=ok&((fb==b) if b>=0 else True);correlations.append(dict(reference=ref,tokens=t,layer='mean8' if l<0 else str(l),band='overall' if b<0 else f'bin{b}',atoms=int(z.sum()),rho_G_logM=float(spearmanr(g[z],xx[z]).statistic),partial_Spearman=partial_rho(g[z],xx[z],lp[z],kd[z])))
   raw=pd.DataFrame(dict(atom=np.arange(30000),bin=fb,A5_group=ag,p_DEV=p,learnable_count=counts,eligible=ok,Dense_known_count=cd,MoE_known_count=cm,K_Dense=kd,K_MoE=km,G=g,M=M));table(raw,f'raw/A_{ref}_{t}');allraw[ref,t]=raw
  for k in range(0,2000,50):
   denom=np.asarray(C@W[k:k+50].T,dtype=np.float64)
   for t in ms:
    numerator=np.asarray(Diffs[t]@W[k:k+50].T,dtype=np.float64);r=np.divide(numerator,denom,out=np.full_like(numerator,np.nan),where=denom>0)
    for j,(_,_,ix) in enumerate(sets[t]):
     if len(ix):boot[t][j,k:k+50]=np.nanmean(r[ix],axis=0);missing[t][j]+=np.isnan(r[ix]).sum()
     else:boot[t][j,k:k+50]=np.nan
   if k%500==0:print('A_BOOT',ref,k,'seconds',round(time.monotonic()-start),flush=True)
  for t in ms:
   g,kd,km,M,cd,cm=details[t]
   for j,(cohort,q,ix) in enumerate(sets[t]):
    vals=boot[t][j];ci=np.nanquantile(vals,[.025,.975]) if np.isfinite(vals).any() else [np.nan,np.nan];deciles.append(dict(reference=ref,tokens=t,cohort=cohort,decile=q,atoms=len(ix),M_median=float(np.median(M[ix])) if len(ix) else np.nan,G_mean=float(g[ix].mean()) if len(ix) else np.nan,ci95_low=ci[0],ci95_high=ci[1],bootstrap_missing_feature_fraction=float(missing[t][j]/max(len(ix)*2000,1))))
   rr=pd.DataFrame(correlations);vv=rr[(rr.reference==ref)&(rr.tokens==t)&(rr.layer=='mean8')&(rr.band!='overall')].rho_G_logM;med=float(np.nanmedian(vv));d=pd.DataFrame(deciles);checks={c:monotonic(d[(d.reference==ref)&(d.tokens==t)&(d.cohort==c)]) for c in ['overall','low','high']};verdict='MoE多学会的内容偏向router集中的feature' if med>=.15 and checks['low'][0] and checks['high'][0] else '与集中度无关，优势是普遍的（按预写阈值）' if abs(med)<.05 else '介于阈值之间或单调条件未满足，如实报告';rules.append(dict(reference=ref,tokens=t,median_within_bin_rho=med,low_monotonic=checks['low'][0],high_monotonic=checks['high'][0],low_non_decreasing=checks['low'][1],high_non_decreasing=checks['high'][1],low_decile_rank_rho=checks['low'][2],high_decile_rank_rho=checks['high'][2],overall_monotonic=checks['overall'][0],result=verdict))
 table(pd.DataFrame(correlations),'A_correlations','PartialrankcorrelationcontrolslogDEVfrequencyandDenseownmastery;overlappingsupportsdescriptive,notcausality.');table(pd.DataFrame(deciles),'A_deciles','Exactdocumentresamplingratios,feature-equalmeans;fixeddeciles,zero-supportfeaturesexcludedwithmissingfractionreported.');table(pd.DataFrame(rules),'A_rules')
 ctx=[];extreme=[];summary=[];recognition=np.load(ROOT/'data/strata.npz')['bigram_recognition']
 for ref in REFS:
  raw=allraw[ref,10000000000];z=raw[raw.eligible].sort_values(['G','atom']);learn=np.load(F/f'data/learnable_{ref}.npy');nr=np.asarray(Fx.T@(learn&recognition).astype(np.float32)).ravel();rec=nr/np.maximum(raw.learnable_count.to_numpy(),1)
  for label,sel in [('MoE_more',z.tail(20).sort_values('G',ascending=False)),('Dense_more',z.head(20))]:
   ix=sel.atom.to_numpy();selected=sel.copy();selected['reference']=ref;selected['selection']=label;selected['recognition_position_fraction']=rec[ix];selected['majority_content']=np.where(rec[ix]>=.5,'认token','靠上下文');extreme.append(selected)
   prefer=(S['MoE'][-1]&~S['Dense'][-1]) if label=='MoE_more' else (S['Dense'][-1]&~S['MoE'][-1]);cc=decode_contexts(Fx,ix,prefer,ref+'_'+label,dict(Dense_known=S['Dense'][-1],MoE_known=S['MoE'][-1]),allowed=learn);cc['reference']=ref;ctx.append(cc)
   for key,values in [('A5_group',ag),('bin',fb),('majority_content',np.where(rec>=.5,'认token','靠上下文'))]:
    val,cnt=np.unique(values[ix],return_counts=True)
    for v,n in zip(val,cnt):summary.append(dict(reference=ref,selection=label,by=key,value=str(v),features=int(n)))
 table(pd.concat(extreme),'A_extreme_features','Each20primaryextremefeatureanditsactualstates;contextsareselecteddescriptively,notindependentconfirmation.');table(pd.concat(ctx),'A_extreme_contexts');table(pd.DataFrame(summary),'A_extreme_summary')
 plt=plotting();d=pd.DataFrame(deciles)
 for ref in REFS:
  fig,axs=plt.subplots(1,3,figsize=(15,4.5))
  for ax,t in zip(axs,ms):
   for c,name in [('low','低频 bin0–2'),('high','高频 bin7–9')]:
    z=d[(d.reference==ref)&(d.tokens==t)&(d.cohort==c)];ax.errorbar(z.M_median,z.G_mean,yerr=[np.maximum(z.G_mean-z.ci95_low,0),np.maximum(z.ci95_high-z.G_mean,0)],fmt='o-',label=name,color=COLORS[c],capsize=2)
   ax.axhline(0,c='grey',ls='--');ax.set(title=f'{t/1e9:g}B',xlabel='原生router集中度M（EVAL分母）',ylabel='掌握率差：MoE−Dense');ax.grid(alpha=.2);ax.legend(fontsize=8)
  savefig(fig,'A_十等份_'+ref,'低/高频分别按集中度分十等份，feature等权均值，区间按文档重抽样2000次；横坐标为组内M中位数。只代表相关，不代表集中导致学会。')
 dump(F/'evidence/A_complete.json',dict(seconds=time.monotonic()-start,ref_count=2,bootstrap=2000,tokens=list(ms),training_updates=0));event('A','逐feature掌握率差、分层相关、文档十分位与解码内容全部完成',seconds=time.monotonic()-start)
if __name__=='__main__':
 with threadpool_limits(limits=4):main()
