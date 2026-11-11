from fu import *
import argparse
def first():
 plt=plotting();n=pd.read_csv(ROOT/'results/baseline_NLL_document_CI.csv');k=pd.read_csv(ROOT/'results/fig1_mastery_transitions.csv');k=k[(k.reference=='MoE33B')&(k.stratum=='overall')];fig,axs=plt.subplots(2,2,figsize=(12,8))
 axs[0,0].errorbar(n.tokens/1e9,n.paired_fp16_difference,yerr=[n.paired_fp16_difference-n.ci95_low,n.ci95_high-n.paired_fp16_difference],fmt='o-',color=COLORS['MoE'],capsize=3);axs[0,0].axhline(0,c='grey',ls='--');axs[0,0].set(title='NLL差：Dense−MoE',xlabel='累计训练token（B）',ylabel='NLL差（nat，正值偏向MoE）')
 for m in ['Dense','MoE']:
  z=k[k.model==m];axs[0,1].plot(z.tokens/1e9,z.K,'o-',color=COLORS[m],label=m);axs[0,1].fill_between(z.tokens.to_numpy()/1e9,z.K_ci95_low.to_numpy(),z.K_ci95_high.to_numpy(),color=COLORS[m],alpha=.15);z=z[~z.initial_point];xx=np.arange(len(z));off=-.19 if m=='Dense' else .19
  for ax,key in zip(axs[1],['new_learned_contribution','forgotten_contribution']):ax.bar(xx+off,z[key],.36,color=COLORS[m],label=m);ax.set_xticks(xx,[f'{v/1e9:g}' for v in z.tokens]);ax.set_xlabel('区间终点token（B）')
 axs[0,1].set(title='可学位置的掌握率',xlabel='累计训练token（B）',ylabel='掌握率K');axs[1,0].set(title='各区间新学会贡献',ylabel='占可学位置的比例');axs[1,1].set(title='各区间忘掉贡献',ylabel='占可学位置的比例')
 for ax in axs.flat:ax.grid(alpha=.2)
 for ax in [axs[0,1],*axs[1]]:ax.legend(fontsize=9)
 savefig(fig,'M1_学得快还是忘得少','仅总体；主参照MoE33B。上排文档bootstrap区间，下排各真实区间贡献，不把差距归于因果路由效应。')
 mm=pd.read_csv(ROOT/'results/baseline_concentration.csv');fig,ax=plt.subplots(figsize=(9,5));ax.plot(mm.tokens/1e9,mm.M_DEV_median,'o-',color=COLORS['MoE'],label='原生MoE router（DEV分母）')
 for value,text,color in [(1,'Dense参考1（示意）',COLORS['Dense']),(1.34,'A5原报告1.34',COLORS['A5']),(1.78,'离线原报告1.78','#666666')]:ax.axhline(value,ls='--',color=color,label=text)
 ax.set(xlabel='累计训练token（B）',ylabel='硬路由集中度中位数',title='原生router的集中度缓慢变化');ax.grid(alpha=.2);ax.legend(fontsize=9);savefig(fig,'M2_router集中度','曲线和A5原报告沿DEV分母；Dense1是示意而非Dense router测量；离线1.78为EVAL分母且原负载超1.2，仅保留指定参照，严格比较见随表EVAL口径和校准1.762。');table(mm,'M2_source','Bothfrequencydenominatorsretained;Dense1notphysicalroutermeasurement.')
 step=1908;w=(np.log(step)-np.log(1750))/(np.log(2000)-np.log(1750));rows=[]
 for a in ['A2','A1','A0','A5']:
  e=evals(a);y=(1-w)*e[1750]['lm_loss']+w*e[2000]['lm_loss'];M=[]
  for s in [1750,2000]:M.append(float(np.nanmedian(artifact(a,s)['concentration'].numpy().mean(0))))
  x=(1-w)*np.log(M[0])+w*np.log(M[1]);rows.append(dict(arm=a,step=step,NLL=y,M=float(np.exp(x)),logM=x,source='1750/2000的ln步数插值',interpolation_weight=w))
 rows.append(dict(arm='Dense',step=step,NLL=float(n[n.tokens==500000000].Dense_NLL.iloc[0]),M=1.,logM=0.,source='0.5B实测NLL；M=1示意',interpolation_weight=np.nan));d=pd.DataFrame(rows);q=d[d.arm.isin(['A2','A1','A5'])];slope,intercept=np.polyfit(q.logM,q.NLL,1);d['fitted_NLL']=slope*d.logM+intercept;d['vertical_residual']=d.NLL-d.fitted_NLL;table(d,'M3_source','NLLandlnMinterpolatedonlnupdate;Densepointnotroutermeasurementandnotinfit.');fig,ax=plt.subplots(figsize=(8,5));xx=np.linspace(d.logM.min()-.05,d.logM.max()+.05,100);ax.plot(xx,slope*xx+intercept,'--',c='grey',label='固定分发A2/A1/A5三点拟合')
 for z in d.itertuples():ax.scatter(z.logM,z.NLL,c=COLORS[z.arm],s=50,marker='s' if z.arm=='Dense' else 'o');ax.annotate(z.arm,(z.logM,z.NLL),xytext=(5,5),textcoords='offset points')
 ax.set(title='0.5B附近：固定分发关系与原生路由',xlabel='ln集中度M（DEV分母）',ylabel='EVAL NLL（nat）');ax.text(.02,.02,'A臂为1750–2000步间按ln步数插值到1908；Dense为0.5B实测',transform=ax.transAxes,fontsize=8);ax.grid(alpha=.2);ax.legend(fontsize=8);savefig(fig,'M3_NLL与集中度','三点拟合为描述关系，A0不参与拟合；DenseM=1示意，不据此断言Dense与MoE集中度等价。所有插值点均明确标注。')
 shock=pd.read_csv(R5/'analysis/out/D_switch_bootstrap.csv');shock=shock[(shock.band=='overall')&shock.pair.isin(['A9-A0','A9d-A0'])];diff=pd.read_csv(ROOT/'results/fig4_switch_recovery.csv');fig,axs=plt.subplots(1,2,figsize=(11,4.5))
 for i,a in enumerate(['A9','A9d']):
  z=shock[shock.pair==a+'-A0'].iloc[0];axs[0].bar(i,z.difference,color=COLORS[a],label=a);axs[0].errorbar(i,z.difference,yerr=[[z.difference-z.ci95_low],[z.ci95_high-z.difference]],fmt='none',c='black',capsize=4);q=diff[(diff.arm==a)&(diff.band=='overall')&(diff.step>=1250)];axs[1].plot(q.step,q.difference,'o-',color=COLORS[a],label=a)
 axs[0].set(xticks=[0,1],xticklabels=['A9全8层','A9d后4层'],ylabel='切换瞬间NLL增加（nat）',title='1000步同权重，零参数更新');axs[1].set(xlabel='优化更新步数',ylabel='NLL−同点A0（nat）',title='切换后250步起的恢复');axs[1].axhline(0,c='grey',ls='--')
 for ax in axs:ax.grid(alpha=.2);ax.legend()
 savefig(fig,'M4_切换冲击与恢复','左图是换分发/gate/bias的联合即时冲击，右图只从1250步起放大恢复；并非独立分组机制效应。')
 tt=pd.read_csv(ROOT/'results/precision8/fig2_transfer_coefficients.csv');fig,axs=plt.subplots(1,2,figsize=(14,6));labels=[f'{g//2}'+('高' if g%2 else '低') for g in range(16)]
 for ax,t in zip(axs,[1000000000,10000000000]):
  z=tt[(tt.model=='MoE')&(tt.block=='expert')&(tt.tokens==t)];T=z.pivot(index='group_a',columns='group_b',values='T').reindex(index=range(16),columns=range(16)).to_numpy();im=ax.imshow(T,cmap='coolwarm',vmin=-1,vmax=1);ax.set_xticks(range(16),labels,rotation=90,fontsize=8);ax.set_yticks(range(16),labels,fontsize=8);ax.set_title(f'{t/1e9:g}B：MoE expert块，每份8序列');fig.colorbar(im,ax=ax,fraction=.045)
 savefig(fig,'M5_不同内容的局部帮助','组号为A5分组；低=bin0–2，高=bin7–9。白色为跨份信号不足，正值为局部原始梯度方向帮助；色阶截到±1，10B有2格超界，原始T不截断；不是实际训练干预。')
 dump(F/'evidence/D_first_complete.json',dict(figures=['M1','M2','M3','M4','M5']));event('D1','M1–M5中文组会图完成')
def last():
 plt=plotting();d=pd.read_csv(F/'results/A_deciles.csv');z=d[(d.reference=='MoE33B')&(d.tokens==10000000000)];fig,ax=plt.subplots(figsize=(9,5))
 for c,name in [('low','低频bin0–2'),('high','高频bin7–9')]:
  q=z[z.cohort==c];ax.errorbar(q.M_median,q.G_mean,yerr=[np.maximum(q.G_mean-q.ci95_low,0),np.maximum(q.ci95_high-q.G_mean,0)],fmt='o-',capsize=3,label=name,color=COLORS[c])
 ax.axhline(0,c='grey',ls='--');ax.set(xlabel='原生router集中度M（EVAL分母）',ylabel='feature掌握率差：MoE−Dense',title='10B：多学会的内容是否更集中');ax.grid(alpha=.2);ax.legend();savefig(fig,'M6_掌握率差与router集中度','低频/高频内分别按M分十等份，固定feature组的等权G均值，误差线按文档2000次bootstrap；不是因果曲线。')
 fig,axs=plt.subplots(1,2,figsize=(12,4.8));src=[]
 for a in ['A0','A5','A9d']:
  ev=evals(a);ss=sorted(s for s in ev if s<=2000)
  for s in ss:src.append(dict(arm=a,step=s,NLL=ev[s]['lm_loss'],source='actualaggregateeval'))
  for ax,lo in zip(axs,[0,1000]):
   s=[t for t in ss if t>=lo];ax.plot(s,[ev[t]['lm_loss'] for t in s],'o-',color=COLORS[a],label=a,ms=4)
 dense=pd.read_csv(ROOT/'results/baseline_NLL_document_CI.csv');inventory=pd.read_csv(ROOT/'results/checkpoint_inventory_final.csv');matched=[]
 for e in dense.itertuples():
  z=inventory[(inventory.model=='Dense')&(inventory.tokens==e.tokens)]
  if len(z) and int(z.step.iloc[0])<=2000:matched.append((int(z.step.iloc[0]),e.Dense_NLL));src.append(dict(arm='Dense',step=int(z.step.iloc[0]),NLL=e.Dense_NLL,source='actualDensecheckpoint'))
 for ax,lo in zip(axs,[0,1000]):
  m=[v for v in matched if v[0]>=lo]
  if m:ax.scatter([x[0] for x in m],[x[1] for x in m],marker='s',s=60,c=COLORS['Dense'],label='Dense实测点',zorder=5)
  ax.set(xlabel='优化更新步数',ylabel='EVAL NLL（nat）',title='0–2000步' if lo==0 else '1000–2000步放大');ax.grid(alpha=.2);ax.legend(fontsize=9)
 savefig(fig,'M7_训练曲线精简版','只用实际EVAL点；Dense仅0与1908步两点，不连线填造早期曲线。A9d从1000步切换快照起。A0缺少0/250附近逐位置数据不妨碍既有聚合NLL点。');table(pd.DataFrame(src),'M7_source')
 dump(F/'evidence/D_last_complete.json',dict(figures=['M6','M7']));event('D2','M6/M7中文组会图完成')
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('stage',choices=['first','last']);args=a.parse_args();first() if args.stage=='first' else last()
