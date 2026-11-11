"""DEV-only heuristic optimization of a binary-support dispatch table."""
from lf_common import *
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from threadpoolctl import threadpool_limits

def select(scores,bias):return np.argpartition(scores+bias,-2,axis=1)[:,-2:]
def balance(scores,bias=None):
 b=np.zeros(8,np.float32) if bias is None else bias.copy();scale=max(float(scores.std()),1e-8);history=[]
 identical=float((np.ptp(scores,axis=1)==0).mean())
 if 4*identical>1.2:return select(scores,b),b,False,0
 # Bias acts only on this offline table; calibrate on all DEV positions.
 for k in range(120):
  ids=select(scores,b);u=np.bincount(ids.ravel(),minlength=8)/(2*len(ids));ratio=u.max()*8;history.append(float(ratio))
  if ratio<=1.2:return ids,b,True,k+1
  step=scale*.5/(1+k/15)**.5;b-=step*(u*8-1);b-=b.mean()
 return ids,b,False,120
def quantities(F,ct,ids):
 Y=np.zeros((len(ids),8),np.float32);Y[np.arange(len(ids))[:,None],ids]=1
 joint=np.asarray(F.T@Y);u=Y.mean(0)/2;q=joint/np.maximum(2*ct[:,None],1);M=2*(q**3/np.maximum(u[None,:],1e-30)).sum(1)
 return M,q,u
def objective(M,omega):return float(np.sum(omega*np.log(np.maximum(M,1e-8))))
def main():
 start=time.monotonic();F,dc=features('DEV');counts=np.asarray(F.sum(0)).ravel();groups=torch.load(R4/'data/atom_groups.pt',map_location='cpu',weights_only=False);g=groups['group'].numpy();w=groups['w'].numpy();fb=artifact('A0',2000)['feature_bin'].numpy();low=fb<=2;high=fb>=7;history=[];solutions=[]
 for label,lam in [('lambda0',0),('lambda025',.25),('lambda05',.5),('lambda075',.75),('lambda1',1),('equal',None)]:
  omega=np.full(30000,1/30000,dtype=np.float32) if lam is None else (low*lam/max(low.sum(),1)+high*(1-lam)/max(high.sum(),1)).astype(np.float32);best=None;unconstrained=None
  for seed in range(4):
   if seed==0:A=np.zeros((30000,8),np.float32);A[np.arange(30000),g]=w
   else:A=np.random.default_rng(20261110+seed).normal(0,1,(30000,8)).astype(np.float32)
   ids,b,_,_=balance(F@A);M,q,u=quantities(F,counts,ids)
   for it in range(30):
    A=omega[:,None]*np.log(np.maximum(q,1e-8)/np.maximum(u[None,:],1e-8))
    scores=F@A;ids,b,feasible,iterations=balance(scores);M,q,u=quantities(F,counts,ids);J=objective(M,omega)
    row=dict(objective=label,lambda_value=lam,start=seed,round=it+1,DEV_J=J,DEV_load_max_over_mean=float(u.max()*8),feasible=feasible,bias_iterations=iterations,seconds=time.monotonic()-start);history.append(row)
    if unconstrained is None or J>unconstrained['J']:unconstrained=dict(A=A.copy(),bias=b.copy(),J=J,start=seed,round=it+1,DEV_M=M.copy(),DEV_load=u.copy())
    if feasible and (best is None or J>best['J']):best=dict(A=A.copy(),bias=b.copy(),J=J,start=seed,round=it+1,DEV_M=M.copy(),DEV_load=u.copy())
    if (it+1)%10==0:print('OFFLINE',label,seed,it+1,'J',J,'load',u.max()*8,'sec',round(time.monotonic()-start),flush=True)
   # Save each completed start so restarts do not erase work.
   dump(R/f'offline/{label}_start{seed}.json',dict(last=row,best_J=None if best is None else best['J']))
  valid=best is not None
  if best is None:best=unconstrained
  np.savez(R/f'offline/{label}.npz',A=best['A'],bias=best['bias'],DEV_M=best['DEV_M'],omega=omega)
  solutions.append(dict(label=label,lambda_value=lam,DEV_J=best['J'],selected_start=best['start'],selected_round=best['round'],DEV_max_load=float(best['DEV_load'].max()*8),DEV_feasible=valid))
  table(pd.DataFrame(history),'fig3_optimization_history','All starts and30rounds, including infeasible rounds. Selection uses DEV objective only.')
 del F,dc
 F,ec=features('EVAL');counts=np.asarray(F.sum(0)).ravel();rows=[];per=[]
 for sol in solutions:
  pack=np.load(R/f"offline/{sol['label']}.npz");ids=select(F@pack['A'],pack['bias']);M,q,u=quantities(F,counts,ids);row=dict(**sol,EVAL_J=objective(M,pack['omega']),low_M_median=float(np.median(M[low])),high_M_median=float(np.median(M[high])),overall_M_median=float(np.median(M)),EVAL_max_load=float(u.max()*8),kind='optimized_binary_support');rows.append(row);per.append(pd.DataFrame(dict(solution=sol['label'],atom=np.arange(30000),bin=fb,count=counts,M=M)));np.save(R/f'offline/{sol["label"]}_EVAL_top2.npy',ids.astype(np.uint8))
 # Baselines use exactly the EVAL-frequency form of M, not the old DEV form.
 for a in ['A2','A0','A5','A8','A9d']:
  d=artifact(a,2000);ct=d['feature_count'].numpy();joint=d['joint_count'].numpy();u=d['expert_count'].numpy();u=u/u.sum(-1,keepdims=True);q=joint/np.maximum(2*ct[None,:,None],1);M=(2*(q**3/np.maximum(u[:,None,:],1e-30)).sum(-1)).mean(0);rows.append(dict(label=a,low_M_median=float(np.median(M[low])),high_M_median=float(np.median(M[high])),overall_M_median=float(np.median(M)),kind='actual_trained_route'))
 table(pd.concat(per),'per_atom_fig3_M','EVAL-coordinate M peratom; optimizer is DEV-only; no model was updated.');d=pd.DataFrame(rows);table(d,'fig3_frontier','Heuristic feasible objective values give lower bounds on best attainable DEV objectives; EVAL generalization may violate the DEVload cap. 4 is an upper bound only under uniform global expert load.')
 ii=ec['indices'].numpy();vv=ec['values'].numpy();gg=g[ii];valid=vv>0;mass=np.zeros((N,8),np.float32);countmass=np.zeros_like(mass)
 for e in range(8):countmass[:,e]=((gg==e)&valid).sum(1);mass[:,e]=(vv*w[ii]*(gg==e)).sum(1)
 coverage=(countmass>0).sum(1);top2=np.partition(mass,-2,axis=1)[:,-2:].sum(1)/np.maximum(mass.sum(1),1e-30);countshare=np.partition(countmass,-2,axis=1)[:,-2:].sum(1)/np.maximum(countmass.sum(1),1)
 table(pd.DataFrame([dict(metric=k,mean=float(v.mean()),p10=float(np.quantile(v,.1)),median=float(np.median(v)),p90=float(np.quantile(v,.9))) for k,v in [('A5groups_covered',coverage),('top2_weighted_activation_mass',top2),('top2_binary_feature_count_share',countshare)]]),'fig3_overlap_summary','Quality mass explicitly means sum z_j*w_j; binary count share also reported.')
 table(pd.DataFrame(dict(groups_covered=np.arange(9),positions=np.bincount(coverage,minlength=9))),'fig3_groups_covered_histogram')
 fig,axs=plt.subplots(1,2,figsize=(13,5));z=d[d.kind=='optimized_binary_support'];zz=z[(z.label!='equal')&(z.DEV_feasible==True)];axs[0].plot(zz.high_M_median,zz.low_M_median,'o-',label='DEV feasible optimized binary routing')
 for r in d.itertuples():axs[0].scatter(r.high_M_median,r.low_M_median,marker='x' if r.kind=='optimized_binary_support' and not r.DEV_feasible else 'o');axs[0].annotate(r.label+(' infeasible' if r.kind=='optimized_binary_support' and not r.DEV_feasible else ''),(r.high_M_median,r.low_M_median),xytext=(3,3),textcoords='offset points',fontsize=8)
 axs[0].scatter([4],[4],marker='*',s=90,label='uniform-load bound4');axs[0].set(xlabel='high-frequency M median (bins7-9)',ylabel='low-frequency M median (bins0-2)',title='Held-out concentration; teacher coordinates');axs[0].legend(fontsize=7);axs[0].grid(alpha=.2)
 axs[1].hist(top2,bins=40,alpha=.7,label='weighted activation mass');axs[1].hist(countshare,bins=40,alpha=.5,label='binary feature share');axs[1].set(xlabel='fraction in top2 A5groups',ylabel='positions',title='Overlap constraint at each position');axs[1].legend(fontsize=7);savefig(fig,'图3_集中度可达曲线','解在DEV选择、EVAL报告。此曲线为启发式已找到的解，不是已证明最优的Pareto边界；4仅为完全均匀负载参照。')
 a=d[d.label=='lambda0'].iloc[0];b=d[d.label=='lambda1'].iloc[0];drop=1-b.high_M_median/a.high_M_median;equal=d[d.label=='equal'].iloc[0];rule=('无法套用：lambda1无满足负载约束的可行解' if not b.DEV_feasible else '低频和高频存在明显取舍' if drop>.2 else '可以同时集中（按预写规则）');dump(R/'evidence/fig3_complete.json',dict(seconds=time.monotonic()-start,high_frequency_drop_lambda1_vs0=float(drop),rule_result=rule,equal_EVAL_M=float(equal.overall_M_median),uniform_load_bound_only=True,training_updates=0,iterations=30,starts=4,objectives=6));event('图3',f'等权EVAL中位M={equal.overall_M_median:.6f}；{rule}',CPU_seconds=time.monotonic()-start)
if __name__=='__main__':
 with threadpool_limits(limits=4):main()
