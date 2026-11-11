"""Fixed DEV-fitted A; marginal-load-only EVAL bias calibration (transductive)."""
from offline import balance,quantities
from lf_common import *
from threadpoolctl import threadpool_limits
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
def main():
 F,_=features('EVAL');ct=np.asarray(F.sum(0)).ravel();fb=artifact('A0',2000)['feature_bin'].numpy();rows=[];per=[]
 for label in ['lambda0','lambda025','lambda05','lambda075','lambda1','equal']:
  p=np.load(R/f'offline/{label}.npz');scores=F@p['A'];ids,b,ok,it=balance(scores,p['bias']);M,q,u=quantities(F,ct,ids);rows.append(dict(label=label,feasible=ok,low_M_median=float(np.median(M[fb<=2])),high_M_median=float(np.median(M[fb>=7])),overall_M_median=float(np.median(M)),EVAL_max_load=float(u.max()*8),bias_iterations=it,A_refitted=False,EVAL_load_only_bias_calibration=True));per.append(pd.DataFrame(dict(label=label,atom=np.arange(30000),bin=fb,M=M)));np.save(R/f'offline/{label}_EVAL_load_calibrated_bias.npy',b)
 table(pd.DataFrame(rows),'fig3_EVAL_load_calibration','Exploratorytransductivemarginal-loadcalibration;A remains DEV-fitted andunchanged. Does notreplacefrozenDEVbiasgeneralizationtest. No modelbias is touched.')
 table(pd.concat(per),'per_atom_fig3_load_calibrated_M')
 d=pd.DataFrame(rows);old=pd.read_csv(R/'results/fig3_frontier.csv');old=old[old.kind=='optimized_binary_support'];fig,ax=plt.subplots(figsize=(8,6));z=d[(d.label!='equal')&d.feasible];ax.plot(z.high_M_median,z.low_M_median,'o-',label='fixed DEV A; EVAL load-calibrated bias');z=old[(old.label!='equal')&(old.DEV_feasible==True)];ax.plot(z.high_M_median,z.low_M_median,'o--',alpha=.5,label='frozen DEV bias; EVAL load cap violated')
 for row in d.itertuples():ax.scatter(row.high_M_median,row.low_M_median,marker='o' if row.feasible else 'x');ax.annotate(row.label+(' infeasible' if not row.feasible else ''),(row.high_M_median,row.low_M_median),xytext=(3,4),textcoords='offset points',fontsize=8)
 ax.scatter([4],[4],marker='*',s=70,label='uniform-load reference4');ax.set(xlabel='high-frequency M median',ylabel='low-frequency M median',title='Same DEV-fitted tables; load-calibration sensitivity');ax.grid(alpha=.2);ax.legend(fontsize=7);savefig(fig,'图3_负载校准敏感性','实线只展示固定A、EVAL边缘负载校准后可行的解；虚线原DEV偏置在EVAL上不满足1.2；两者不混作同一泛化结论。lambda1更新后仍不可行。')
 dump(R/'evidence/fig3_EVAL_load_calibration.json',dict(rows=rows,transductive=True,A_refitted=False,model_or_router_bias_updates=0))
if __name__=='__main__':
 with threadpool_limits(limits=4):main()
