from fu import *
from gradients import raw_T
from threadpoolctl import threadpool_limits
import itertools
MAIN_TIMES=[500000000,1000000000,3000000000,5000000000,10000000000]

def expected_jaccard(n,a,b):
 if a+b==0:return np.nan
 k=np.arange(max(0,a+b-n),min(a,b)+1);return float(np.sum(hypergeom.pmf(k,n,a,b)*k/(a+b-k)))
def fixed_statistics(T,scope):
 vals=[];same=[];other=[]
 for low,hi,others in scope:
  z=np.array([T[low,hi]]+[T[low,j] for j in others])
  if not np.isfinite(z).all():return [np.nan]*3
  same.append(z[0]);other.append(z[1:].mean());vals.append(z[0]-z[1:].mean())
 return [float(np.mean(x)) if len(x) else np.nan for x in [vals,same,other]]
def condition(mode,model,t,block,cooc):
 isold=mode=='8_original' and t in [1000000000,10000000000]
 path=(ROOT/f'precision8/gradient/{model}_{t}_{block}_sketch.npy') if isold else (F/f'data/E/sketches/{mode}_{model}_{t}_{block}.npy')
 cache=F/f'data/E/gram_{mode}_{model}_{t}_{block}.npy'
 if cache.exists():gram=np.load(cache)
 else:
  g=np.load(path,mmap_mode='r');flat=np.asarray(g).reshape(64,-1).astype(np.float64);gram=(flat@flat.T).reshape(16,4,16,4);np.save(cache,gram);del g,flat
 T,sig=raw_T(gram);valid=np.isfinite(T);upper=np.triu(valid,1);total=int(upper.sum());negative=int(((T<0)&upper).sum());rho=float(spearmanr(T[upper],cooc[upper]).statistic) if total>2 else np.nan
 scope=[]
 for a in range(0,16,2):
  others=[j for j in range(1,16,2) if j!=a+1 and valid[a,j]]
  if valid[a,a+1] and others:scope.append((a,a+1,others))
 stat=fixed_statistics(T,scope);rng=np.random.default_rng(20261111);boot=[]
 for _ in range(2000):
  z,_=raw_T(gram,rng.multinomial(4,np.full(4,.25)));boot.append(fixed_statistics(z,scope))
 boot=np.asarray(boot);good=np.isfinite(boot[:,0]);cis=np.quantile(boot[good],[.025,.975],axis=0) if good.any() else np.full((2,3),np.nan)
 if isold:
  nn=pd.read_csv(ROOT/f'results/precision8/fig2_norm_audit_{model}_{t}.csv');nn=nn[nn.block==block];norms=nn.groupby('group').exact_gradient_norm_squared.mean().reindex(range(16)).to_numpy()
 else:
  nn=pd.read_csv(F/f'results/E_norm_{mode}_{model}_{t}.csv');nn=nn[nn.block==block];norms=nn.groupby('group').exact_gradient_norm2.mean().reindex(range(16)).to_numpy()
 ratio=sig/norms;normtable=pd.DataFrame(dict(mode=mode,model=model,tokens=t,block=block,group=np.arange(16),cross_replicate_signal=sig,mean_exact_norm2=norms,signal_to_total_norm_ratio=ratio))
 # The difference follows the original matched low/high comparison; additionally report all cross-group pairs explicitly.
 allcross=np.array([T[i,j] for i in range(16) for j in range(i+1,16) if i//2!=j//2 and valid[i,j]])
 summary=dict(mode=mode,model=model,tokens=t,block=block,sequences=32 if mode=='32_extended' else 8,valid_pairs=total,negative_pairs=negative,negative_pair_fraction=negative/total if total else np.nan,insufficient_groups=int((sig<=0).sum()),same_low_high_mean=stat[1],cross_low_high_mean=stat[2],all_cross_group_mean=float(allcross.mean()) if len(allcross) else np.nan,borrowing_difference=stat[0],borrowing_ci_low=cis[0,0],borrowing_ci_high=cis[1,0],same_ci_low=cis[0,1],same_ci_high=cis[1,1],cross_ci_low=cis[0,2],cross_ci_high=cis[1,2],fixed_scope_low_groups=len(scope),valid_bootstrap_fraction=float(good.mean()),cooccurrence_spearman=rho,signal_to_total_norm_ratio_median=float(np.median(ratio)),signal_to_total_norm_ratio_sum=float(sig.sum()/norms.sum()))
 pairs=[]
 for a in range(16):
  for b in range(a+1,16):pairs.append(dict(mode=mode,model=model,tokens=t,block=block,group_a=a,group_b=b,T=float(T[a,b]),sign='信号不足' if not valid[a,b] else '负' if T[a,b]<0 else '正' if T[a,b]>0 else '零',signal_a=float(sig[a]),signal_b=float(sig[b]),cooccurrence_lift=float(cooc[a,b])))
 return summary,pairs,normtable

def content_label(g,reps,ctx):
 ss=reps[reps.group==g].sort_values('rank');examples=[]
 for z in ss.itertuples():
  rr=ctx[(ctx.group==g)&(ctx.atom==z.atom)].sort_values('example').iloc[0];examples.append(f'原子{z.atom}：{str(rr.current_token)}→{str(rr.next_token)}')
 return f'A5组{g//2}'+('高频' if g%2 else '低频')+'；'+'；'.join(examples)

def main():
 tic=time.monotonic();assert (F/'evidence/E_gradients_complete.json').exists();old=pd.read_csv(ROOT/'results/precision8/fig2_transfer_coefficients.csv');cooc=np.empty((16,16))
 for r in old.drop_duplicates(['group_a','group_b']).itertuples():cooc[r.group_a,r.group_b]=r.cooccurrence_lift
 summaries=[];pairs=[];normrows=[]
 for mode,times in [('8_original',MAIN_TIMES),('32_extended',[10000000000]),('8_extended_control',[10000000000])]:
  for t in times:
   for model in ['MoE','Dense']:
    for block in ['expert' if model=='MoE' else 'FFN','attention']:
     s,p,n=condition(mode,model,t,block,cooc);summaries.append(s);pairs+=p;normrows.append(n);print('E_ANALYSED',mode,model,t,block,flush=True)
 S=pd.DataFrame(summaries);P=pd.DataFrame(pairs);table(S,'E_statistics','同组低高与跨组低高均值按有效低频组等权；另给所有跨A5分组对的均值。CI固定原点有效组对集合，bootstrap出现无定义分母的整份读数标缺失，不动态换组。');table(P,'E_pair_signs_and_values','120组对×全部时点/精度/参数块；信号不足保留缺失，不填零。');table(pd.concat(normrows),'E_signal_norm_audit','完整累积梯度范数；每组信号/总范数比包含非正信号，非仅保留有效组。')
 main=S[((S.model=='MoE')&(S.block=='expert'))|((S.model=='Dense')&(S.block=='FFN'))];table(main,'E_main_statistics');table(main[main.tokens==10000000000],'E_10B_precision_comparison')
 pp=P[((P.model=='MoE')&(P.block=='expert'))|((P.model=='Dense')&(P.block=='FFN'))];overlaps=[]
 for mode in ['8_original','8_extended_control','32_extended']:
  for t in (MAIN_TIMES if mode=='8_original' else [10000000000]):
   z=pp[(pp['mode']==mode)&(pp.tokens==t)];a=z[z.model=='MoE'].set_index(['group_a','group_b']).T if False else z[z.model=='MoE'].set_index(['group_a','group_b'])['T'];b=z[z.model=='Dense'].set_index(['group_a','group_b'])['T'];valid=np.isfinite(a)&np.isfinite(b);x=a[valid]<0;y=b[valid]<0;n=int(valid.sum());na=int(x.sum());nb=int(y.sum());both=int((x&y).sum());union=int((x|y).sum());jac=both/union if union else np.nan;ej=expected_jaccard(n,na,nb);fold=jac/ej if ej>0 else np.nan;overlaps.append(dict(mode=mode,tokens=t,common_valid_pair_universe=n,negative_MoE=na,negative_Dense=nb,negative_both=both,negative_union=union,Jaccard=jac,random_expected_Jaccard=ej,fold_random=fold))
 O=pd.DataFrame(overlaps);table(O,'E_negative_set_overlap')
 z=main[(main['mode']=='32_extended')];rr=O[(O['mode']=='32_extended')].iloc[0];neg=z.negative_pair_fraction.to_numpy();verdict='后期读到的干扰主要是估计噪声（按预写规则）' if np.all(neg<.05) else '后期确实出现稳定的干扰组合（按预写规则）' if np.all(neg>=.10) and rr.fold_random>=3 else '未达到任一联合判据，如实报告';table(pd.DataFrame([dict(MoE_negative_fraction=float(z[z.model=='MoE'].negative_pair_fraction.iloc[0]),Dense_negative_fraction=float(z[z.model=='Dense'].negative_pair_fraction.iloc[0]),negative_overlap_fold=float(rr.fold_random),result=verdict)]),'E_precision_rule')
 reps=pd.read_csv(F/'results/E_group_representative_features.csv');ctx=pd.read_csv(F/'results/E_group_representative_contexts.csv',keep_default_na=False);lookup={(r['mode'],r['model'],int(r['tokens']),int(r['group_a']),int(r['group_b'])):float(r['T']) for r in pp.to_dict('records')};candidate=[];helps=[]
 for a,b in itertools.combinations(range(16),2):
  row=dict(group_a=a,group_b=b,content_a=content_label(a,reps,ctx),content_b=content_label(b,reps,ctx),cooccurrence_lift=float(cooc[a,b]));joint=0;per={m:0 for m in ['MoE','Dense']};ten=[]
  for t in MAIN_TIMES:
   vals=[]
   for model in ['MoE','Dense']:
    v=lookup['8_original',model,t,a,b];row[f'{model}_{t//1000000}M']=v;vals.append(v);ten.append(v)
    if t in [3000000000,5000000000,10000000000] and v<0:per[model]+=1
   if t in [3000000000,5000000000,10000000000] and all(np.isfinite(v) and v<0 for v in vals):joint+=1
  v32=[]
  for model in ['MoE','Dense']:
   v=lookup['32_extended',model,10000000000,a,b];row[f'{model}_10B_32']=v;row[f'{model}_10B_8extended']=lookup['8_extended_control',model,10000000000,a,b];v32.append(v)
  row.update(joint_negative_late_nodes=joint,MoE_negative_late_nodes=per['MoE'],Dense_negative_late_nodes=per['Dense'],both_negative_32=all(np.isfinite(v) and v<0 for v in v32),both_positive_32=all(np.isfinite(v) and v>0 for v in v32),joint_rule_candidate=joint>=2,broader_rule_candidate=all(per[m]>=2 for m in per))
  if row['broader_rule_candidate'] or joint>=2:candidate.append(row.copy())
  if all(np.isfinite(v) and v>0 for v in ten):row['minimum_T_across_10']=float(min(ten));helps.append(row.copy())
 columns=['group_a','group_b','content_a','content_b','cooccurrence_lift']
 C=pd.DataFrame(candidate) if candidate else pd.DataFrame(columns=columns+['joint_rule_candidate','broader_rule_candidate','both_negative_32']);table(C,'E_interference_candidates','主候选要求3/5/10B至少两个相同节点两模型都负；另列两模型各自至少两次负的较宽敏感性。32确认单列。');table(C[C.joint_rule_candidate==True] if len(C) else C,'E_stable_interference_pairs','这是原8版的跨时点候选；必须结合32确认，不自动称为精度稳定。')
 H=pd.DataFrame(helps).sort_values('minimum_T_across_10',ascending=False).head(10) if helps else pd.DataFrame(columns=columns+['minimum_T_across_10']);table(H,'E_strongest_stable_help_pairs','五时点×两模型的10个T全部有效为正；按最小T降序；不足10对给实际数量。32确认另列。')
 plt=plotting();fig,axs=plt.subplots(1,3,figsize=(16,4.7));curves=main[main['mode']=='8_original']
 for model,label in [('MoE','MoE expert'),('Dense','Dense FFN')]:
  z=curves[curves.model==model].sort_values('tokens');x=z.tokens/1e9;color=COLORS[model];axs[0].plot(x,100*z.negative_pair_fraction,'o-',color=color,label=label);axs[1].errorbar(x,z.borrowing_difference,yerr=[np.maximum(z.borrowing_difference-z.borrowing_ci_low,0),np.maximum(z.borrowing_ci_high-z.borrowing_difference,0)],fmt='o-',color=color,label=label,capsize=3);axs[2].plot(x,z.cooccurrence_spearman,'o-',color=color,label=label)
 axs[0].set(title='负的组对比例（有效组对为分母）',ylabel='比例（%）');axs[0].axhline(5,color='gray',ls='--',lw=1);axs[0].axhline(10,color='gray',ls=':',lw=1);axs[1].set(title='同组低高帮助 − 跨组低高帮助',ylabel='局部帮助系数差');axs[1].axhline(0,color='gray',ls='--');axs[2].set(title='帮助系数与共现的相关',ylabel='Spearman相关')
 for ax in axs:ax.set_xlabel('累计训练 token（B）');ax.grid(alpha=.2);ax.legend(fontsize=8)
 savefig(fig,'E_帮助与干扰随训练变化','全部时点严格复用原8序列批次；中图为同组低高T减跨组低高T及固定组对的R4自助区间。无定义信号不填零；局部量不是实际训练干预。10B扩展32精度结果另表，不能混入同样本曲线。')
 fig,axs=plt.subplots(1,2,figsize=(11,4.5));modes=['8_original','8_extended_control','32_extended'];labels=['原DEV 8序列','扩展DEV 8序列','扩展DEV 32序列']
 for k,model in enumerate(['MoE','Dense']):
  z=main[(main.model==model)&(main.tokens==10000000000)].set_index('mode').reindex(modes);xx=np.arange(3)+(k-.5)*.32;axs[0].bar(xx,100*z.negative_pair_fraction,.3,label=model,color=COLORS[model]);axs[1].bar(xx,z.signal_to_total_norm_ratio_median,.3,label=model,color=COLORS[model])
 axs[0].set(ylabel='负的有效组对（%）',title='10B：精度与样本组成');axs[1].set(ylabel='跨份信号 / 完整梯度总范数²',title='16组比值的中位数（含非正组）')
 for ax in axs:ax.set_xticks(range(3),labels,fontsize=8);ax.legend();ax.grid(axis='y',alpha=.2)
 savefig(fig,'E_10B精度检查','32版每组每份32条，全局2048条不复用；原DEV不足，已获准扩展独立DEV。扩展8与32属于同扩展集合但每份样本数量不同；样本组成仍是敏感性来源。')
 fig,axs=plt.subplots(1,2,figsize=(11,4.5))
 for ax,model in zip(axs,['MoE','Dense']):
  z=curves[curves.model==model].sort_values('tokens');x=z.tokens/1e9
  for name,lab,col in [('same','同组低频−高频',COLORS[model]),('cross','跨组低频−高频','#777777')]:
   y=z.same_low_high_mean if name=='same' else z.cross_low_high_mean;ax.errorbar(x,y,yerr=[np.maximum(y-z[name+'_ci_low'],0),np.maximum(z[name+'_ci_high']-y,0)],fmt='o-',label=lab,color=col,capsize=2)
  ax.set(title=model+(' expert' if model=='MoE' else ' FFN'),xlabel='累计训练 token（B）',ylabel='局部帮助系数 T');ax.legend(fontsize=8);ax.grid(alpha=.2)
 savefig(fig,'E_同组与跨组帮助均值','同组低高与对应低频组的其他高频组分别等权平均；固定原点有效组对的R4 bootstrap区间；差值与其区间详E_main_statistics。')
 dump(F/'evidence/E_complete.json',dict(seconds=time.monotonic()-tic,main_rule=verdict,strict_interference_candidates=int(C.joint_rule_candidate.sum()) if len(C) else 0,precision_confirmed_candidates=int((C.joint_rule_candidate&C.both_negative_32).sum()) if len(C) else 0,stable_help_pairs=len(H),training_updates=0));event('E完成',verdict,seconds=time.monotonic()-tic,GPU_seconds=0)
if __name__=='__main__':
 with threadpool_limits(limits=4):main()
