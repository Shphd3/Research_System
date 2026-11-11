from fu import *
from threadpoolctl import threadpool_limits
def test_delta(Fx,ct,dx):
 mu=np.asarray(Fx.T@dx).ravel()/np.maximum(ct,1);second=np.asarray(Fx.T@(dx*dx)).ravel()/np.maximum(ct,1);se=np.sqrt(np.maximum(second-mu*mu,0)/np.maximum(ct-1,1));ok=ct>=50;p=np.ones(30000);p[ok]=2*norm.sf(abs(mu[ok])/np.maximum(se[ok],1e-12));q=np.ones(30000);q[ok]=bh(p[ok]);return mu,se,q,ok&(q<.05)&(mu>=.01),ok&(q<.05)&(mu<=-.01)
def main():
 tic=time.monotonic();Fx,_=features('EVAL');ct=np.asarray(Fx.sum(0)).ravel();fb,p,ag=metadata();ok=ct>=50;S={m:states(m) for m in ['Dense','MoE']};learn={r:refmask(r) for r in REFS};counts={r:np.asarray(Fx.T@v.astype(np.float32)).ravel() for r,v in learn.items()};LL={m:{t:loss(m,t) for t in [1000000000,3000000000,5000000000,10000000000]} for m in S};intervals=[(1000000000,3000000000),(3000000000,5000000000),(5000000000,10000000000)];summary=[];stats={};state_rows=[]
 for a,b in intervals:
  for m in S:
   mu,se,q,forgot,got=test_delta(Fx,ct,LL[m][b]-LL[m][a]);stats[m,a,b]=(mu,se,q,forgot,got);raw=pd.DataFrame(dict(atom=np.arange(30000),bin=fb,A5_group=ag,count=ct,delta=mu,SE=se,q=q,forgotten=forgot,learned=got));table(raw,f'raw/B_{m}_{a}_{b}')
   for r in REFS:
    start=S[m][TIMES.index(a)];end=S[m][TIMES.index(b)];known=np.asarray(Fx.T@(learn[r]&start).astype(np.float32)).ravel();nf=np.asarray(Fx.T@(learn[r]&start&~end).astype(np.float32)).ravel();state_rows.append(pd.DataFrame(dict(reference=r,model=m,from_tokens=a,to_tokens=b,atom=np.arange(30000),learnable_count=counts[r],known_at_start=known,forgotten_positions=nf,conditional_f=np.divide(nf,known,out=np.full(30000,np.nan),where=known>0),forgotten_fraction_of_learnable=nf/np.maximum(counts[r],1))))
  x=stats['Dense',a,b][3];y=stats['MoE',a,b][3];n=int(ok.sum());na=int(x.sum());nb=int(y.sum());overlap=int((x&y).sum());union=int((x|y).sum());jac=overlap/union if union else np.nan
  if na and nb:
   xx=np.arange(max(0,na+nb-n),min(na,nb)+1);prob=hypergeom.pmf(xx,n,na,nb);ej=float(np.sum(prob*xx/(na+nb-xx)));ratio=jac/ej if ej>0 else np.nan
  else:ej=0.;ratio=np.nan
  dm=stats['Dense',a,b][0];mm=stats['MoE',a,b][0];rho=float(spearmanr(dm[ok]-dm[ok].mean(),mm[ok]-mm[ok].mean()).statistic);summary.append(dict(from_tokens=a,to_tokens=b,eligible_features=n,Dense_forgotten=na,MoE_forgotten=nb,both_forgotten=overlap,union=union,Jaccard=jac,random_expected_Jaccard=ej,random_expected_intersection=na*nb/n,jaccard_fold_random=ratio,rho_centered_deltas=rho,rho_raw_deltas=float(spearmanr(dm[ok],mm[ok]).statistic),result='这次遗忘由两个架构共同的因素决定（按预写规则）' if ratio>=10 and rho>=.5 else '未同时达到10倍重合和0.5相关阈值'))
 table(pd.DataFrame(summary),'B_overlap_and_correlations','RandomJaccard expectation integrates exacthypergeometric intersection distribution atfixedeligibleNandsetsizes. Centering cannot changeSpearman ranks.');table(pd.concat(state_rows),'raw/B_state_forgetting','Stateforgetrateconditionalonknownstart;zeroknownisNaN. Bothlearnabilityreferencesretained.')
 a,b=3000000000,5000000000;dm=stats['Dense',a,b][0];mm=stats['MoE',a,b][0];shared=stats['Dense',a,b][3]&stats['MoE',a,b][3];recognition=np.load(ROOT/'data/strata.npz')['bigram_recognition'];nrec=np.asarray(Fx.T@(learn['MoE33B']&recognition).astype(np.float32)).ravel();frac=nrec/np.maximum(counts['MoE33B'],1);selected=np.flatnonzero(shared);groups=[]
 for by,v in [('bin',fb),('A5_group',ag),('majority_content',np.where(frac>=.5,'认token','靠上下文'))]:
  vv,nn=np.unique(v[selected],return_counts=True)
  for value,num in zip(vv,nn):groups.append(dict(by=by,value=str(value),features=int(num),fraction=float(num/max(len(selected),1))))
 table(pd.DataFrame(groups),'B_shared_content_summary')
 top=selected[np.lexsort((selected,-(dm[selected]+mm[selected])/2))[:20]];features_table=pd.DataFrame(dict(atom=selected,bin=fb[selected],A5_group=ag[selected],p_DEV=p[selected],Dense_delta3to5=dm[selected],MoE_delta3to5=mm[selected],recognition_position_fraction=frac[selected]));recovery=[]
 for m in S:
  l3=np.asarray(Fx.T@LL[m][3000000000]).ravel()/np.maximum(ct,1);l10=np.asarray(Fx.T@LL[m][10000000000]).ravel()/np.maximum(ct,1);back=l10<=l3;significant=stats[m,5000000000,10000000000][4];features_table[m+'_NLL_recovered10B']=back[selected];features_table[m+'_significant_recovery5to10']=significant[selected]
  for ref in REFS:
   p3=S[m][TIMES.index(3000000000)];p5=S[m][TIMES.index(5000000000)];p10=S[m][-1];nf=np.asarray(Fx.T@(learn[ref]&p3&~p5).astype(np.float32)).ravel();nr=np.asarray(Fx.T@(learn[ref]&p3&~p5&p10).astype(np.float32)).ravel();features_table[m+'_'+ref+'_state_recovered_fraction']=np.divide(nr[selected],nf[selected],out=np.full(len(selected),np.nan),where=nf[selected]>0);recovery.append(dict(model=m,reference=ref,shared_features=len(selected),loss_recovered_features=int((back&shared).sum()),loss_recovered_fraction=float(np.mean(back[selected])) if len(selected) else np.nan,significant_5to10_improvement_features=int((significant&shared).sum()),state_forgotten_positions_feature_occurrences=float(nf[selected].sum()),state_recovered_occurrences=float(nr[selected].sum()),state_recovered_fraction=float(nr[selected].sum()/max(nf[selected].sum(),1))))
 table(features_table,'raw/B_shared_features');table(features_table[features_table.atom.isin(top)].assign(mean_delta=lambda d:(d.Dense_delta3to5+d.MoE_delta3to5)/2).sort_values('mean_delta',ascending=False),'B_top20_shared_forgetting');table(pd.DataFrame(recovery),'B_recovery')
 prefer=(LL['Dense'][5000000000]>LL['Dense'][3000000000])&(LL['MoE'][5000000000]>LL['MoE'][3000000000]);ctx=decode_contexts(Fx,top,prefer,'shared3to5',dict(Dense_loss_delta=LL['Dense'][5000000000]-LL['Dense'][3000000000],MoE_loss_delta=LL['MoE'][5000000000]-LL['MoE'][3000000000]));table(ctx,'B_shared_contexts')
 dump(F/'evidence/B_complete.json',dict(seconds=time.monotonic()-tic,intervals=3,models=2,references=2,shared3to5_features=len(selected),training_updates=0));event('B','三段逐feature损失/状态账本、交集随机期望、内容和恢复完成',seconds=time.monotonic()-tic)
if __name__=='__main__':
 with threadpool_limits(limits=4):main()
