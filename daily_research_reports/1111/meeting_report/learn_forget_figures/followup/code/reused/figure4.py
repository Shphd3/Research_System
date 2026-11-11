from lf_common import *
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
def main():
 arms=['A0','A1','A2','A4','A1-deep','A5','A6','A8','A9','A9d'];rows=[];fit=[]
 for a in arms:
  d=artifact(a,2000);m=d['concentration'].numpy().mean(0);fb=d['feature_bin'].numpy();e=evals(a)[2000]
  for b in [-1,0,9]:
   v=float(np.nanmedian(m if b<0 else m[fb==b]));rows.append(dict(arm=a,band='overall' if b<0 else f'bin{b}',NLL=e['lm_loss'] if b<0 else e['bins'][b]['nll'],M=v,logM=np.log(v)))
 d=pd.DataFrame(rows);fig,axs=plt.subplots(1,3,figsize=(16,4.5))
 for ax,band in zip(axs,['overall','bin0','bin9']):
  z=d[d.band==band];q=z[z.arm.isin(['A2','A1','A5'])];slope,intercept=np.polyfit(q.logM,q.NLL,1);line=slope*z.logM+intercept;d.loc[z.index,'fitted_NLL']=line;d.loc[z.index,'vertical_residual_nat']=z.NLL-line;fit.append(dict(band=band,slope=slope,intercept=intercept,fit_arms='A2,A1,A5',observations=3))
  xx=np.linspace(z.logM.min()-.05,z.logM.max()+.05,100);ax.plot(xx,slope*xx+intercept,'--',c='grey')
  for p in z.itertuples():ax.scatter(p.logM,p.NLL);ax.annotate(p.arm,(p.logM,p.NLL),xytext=(3,3),textcoords='offset points',fontsize=8)
  ax.set(title=band,xlabel='ln hard concentration M (DEV denominator)',ylabel='EVAL NLL (nat)');ax.grid(alpha=.2)
 table(d,'fig4_fixed_fit_residuals','Only3fixed-routing arms enterOLS; residual is vertical NLL distance, not an independent mechanism test.');table(pd.DataFrame(fit),'fig4_OLS');savefig(fig,'图4a_NLL与集中度','三点拟合只描述固定分发臂，其他点的偏离不能单独归因于集中度。bin0/9为原子频段，位置支持重叠。')
 rows=[]
 for a in ['A9','A9d']:
  for s,e in evals(a).items():
   ref=evals('A0')[s]
   for b in range(-1,10):rows.append(dict(arm=a,step=s,band='overall' if b<0 else f'bin{b}',difference=(e['lm_loss']-ref['lm_loss']) if b<0 else e['bins'][b]['nll']-ref['bins'][b]['nll'],snapshot='zero_update_switch' if s==1000 else 'trained',reference='A0matchedstep'))
 dd=pd.DataFrame(rows);table(dd,'fig4_switch_recovery','Aggregate actual EVAL differences;1250/1750 oldA0 position arrays absent, no invented intervals.')
 fig,axs=plt.subplots(1,2,figsize=(13,4.5))
 for a in ['A9','A9d']:
  z=dd[(dd.arm==a)&(dd.band=='overall')];axs[0].plot(z.step,z.difference,'o-',label=a)
  z=dd[(dd.arm==a)&(dd.step==1000)&(dd.band!='overall')];axs[1].plot(range(10),z.difference,'o-',label=a)
 for ax in axs:ax.grid(alpha=.2);ax.legend()
 axs[0].set(xlabel='optimizer step',ylabel='NLL minus matched A0 (nat)',title='Zero-update switch and recovery');axs[1].set(xlabel='frequency bin (0=rarest)',ylabel='instant switch NLL increase',title='Fixed weights; routing/gates/bias change jointly');savefig(fig,'图4b_切换与恢复','1000点零更新，后续每250步为实际聚合NLL；主要旧基线来自H100，5090只读敏感性见R05。')
 old=pd.read_csv(R4/'analysis/out/C8_learn_forget_ledger.csv');print('LEDGER_COLUMNS',old.columns.tolist(),flush=True)
 if 'band' not in old:old['band']='overall'
 if 'to_step' not in old:
  old['from_step']=old.interval.str.split('-').str[0].astype(int);old['to_step']=old.interval.str.split('-').str[1].astype(int)
 old=old.rename(columns={'forget':'forgotten','n_forget':'forgotten'})
 if 'adjacent' in old:old=old[old.adjacent]
 new=pd.read_csv(R5/'analysis/out/C_ledger_by_bin.csv');cols=['arm','from_step','to_step','band','forgotten'];ledger=pd.concat([old[cols],new[cols]],ignore_index=True);table(ledger,'fig4_forgetting_all','Real intervals retained; A0has500-step andA4/A1deep1000-step intervals, never interpolated as250-step counts.')
 fig,ax=plt.subplots(figsize=(11,5))
 for a in arms:
  z=ledger[(ledger.arm==a)&(ledger.band=='overall')].sort_values('to_step');ax.plot(z.to_step,z.forgotten,'o-',label=a+' ('+str(int((z.to_step-z.from_step).iloc[0]))+' step intervals)')
 ax.set(xlabel='interval ending update',ylabel='significantly forgotten atoms',title='R04/R05 original ledgers; interval lengths differ');ax.grid(alpha=.2);ax.legend(fontsize=7,ncol=2);savefig(fig,'图4c_十臂遗忘','计数沿用R04阈值和真实区间；不同跨度不能作相同250步计数的排名。')
 event('图4','十臂固定分发拟合残差、切换恢复与真实间隔遗忘图已完成',gpu_seconds=0)
if __name__=='__main__':main()
