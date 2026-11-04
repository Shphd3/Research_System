"""Method-level presentation: equal-weight continuation-order means only."""
from pathlib import Path
import csv,json,math,hashlib,shutil,zipfile
F=Path(__file__).resolve().parent;E=F.parents[1];S=Path('/data/250010109/Research_System');M=S/'daily_research_reports/1023/meeting_report';D=M/'A17_R05_retention_figures'
def rows(p):return list(csv.DictReader(open(p)))
def csvout(p,x):
 with p.open('w') as f:w=csv.DictWriter(f,fieldnames=list(x[0]));w.writeheader();w.writerows(x)
def ev(p):return {'path':str(p.resolve()),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def table(h,body):return '| '+' | '.join(h)+' |\n| '+' | '.join(['---']*len(h))+' |\n'+''.join('| '+' | '.join(map(str,r))+' |\n' for r in body)
old_manifest=json.load(open(D/'manifest.json'));oldfiles={x['path']:x for x in old_manifest['files']}
for n in ['table1_main_experiment_21.csv','table2_residual_interventions_9.csv']:
 p=D/'tables'/n;assert ev(p)==oldfiles[str(p)],n
r=rows(D/'tables/table1_main_experiment_21.csv');z=rows(D/'tables/table2_residual_interventions_9.csv')
names={'U':'统一更新','UL':'整体固定减速','US':'整体调度减速','TC':'前16方向固定衰减','TS':'前16方向调度衰减','RS':'随机方向调度衰减','LS':'小奇异方向调度衰减'}
judgments={'U':'新任务学会，旧能力几乎丢失','UL':'保旧收益接近零，新学习达标不足3/3','US':'旧表现略高，但新表现降低且达标不足3/3','TC':'没有改善旧能力保持','TS':'没有改善旧能力保持','RS':'没有形成有效、稳定的保持收益','LS':'平均旧表现略高，但仍接近零'}
a=[]
for method in names:
 own=[x for x in r if x['method']==method];assert len(own)==3
 avg=lambda key:math.fsum(float(x[key]) for x in own)/3
 a.append({'method':method,'method_name_cn':names[method],'old_accuracy_mean_pct':avg('old_accuracy_pct'),'new_accuracy_mean_pct':avg('new_accuracy_pct'),'new_learning_qualified_orders':sum(x['new_learning_qualified']=='True' for x in own),'n_orders':3,'old_minus_U_mean_pp':avg('old_minus_U_pp'),'bounded_judgment_cn':judgments[method]})
b=[]
for kind in ['endpoint','target','random']:
 own=[x for x in z if x['condition']==kind];assert len(own)==3
 avg=lambda key:math.fsum(float(x[key]) for x in own)/3
 b.append({'condition':kind,'old_accuracy_mean_pct':avg('old_accuracy_mean_pct'),'new_accuracy_mean_pct':avg('new_accuracy_mean_pct'),'old_change_mean_pp':avg('old_change_mean_pp'),'new_change_mean_pp':avg('new_change_mean_pp'),'n_orders':3,'draws_per_order':5 if kind=='random' else 1})
csvout(D/'tables/table1_method_overview_7.csv',a);csvout(D/'tables/table2_residual_overview_3.csv',b)
# Independent total-count check of the arithmetic means, reusing validated source counts.
for x in a:
 own=[q for q in r if q['method']==x['method']]
 for mode in ['old','new']:
  total=sum(round(float(q[f'{mode}_accuracy_pct'])*8) for q in own)
  assert abs(total/2400*100-x[f'{mode}_accuracy_mean_pct'])<1e-10
u=next(x for x in a if x['method']=='U')
assert all(abs(x['old_accuracy_mean_pct']-u['old_accuracy_mean_pct']-x['old_minus_U_mean_pp'])<1e-10 for x in a)
t1=table(['方法','平均旧准确率（%）','平均新准确率（%）','新学习达标','结论'],[[names[x['method']]+'（'+x['method']+'）',f"{x['old_accuracy_mean_pct']:.3f}",f"{x['new_accuracy_mean_pct']:.3f}",f"{x['new_learning_qualified_orders']}/3",x['bounded_judgment_cn']] for x in a])
labels={'endpoint':'原终点','target':'靶向削弱残差主分量','random':'匹配随机干预'}
t2=table(['冻结干预','平均旧准确率（%）','平均新准确率（%）','旧表现变化（百分点）','新表现变化（百分点）'],[[labels[x['condition']],f"{x['old_accuracy_mean_pct']:.3f}",f"{x['new_accuracy_mean_pct']:.3f}",f"{x['old_change_mean_pp']:+.3f}",f"{x['new_change_mean_pp']:+.3f}"] for x in b])
body='''# 方法结果总览：参数保护与旧能力保持

## 结论1：减缓初始大奇异方向的更新，没有实现旧能力保持

'''+t1+'''

**汇报判断：** 前16方向保护的固定与调度两种方式，都没有优于普通更新的旧能力保持。整体减速只能换回少量旧表现，同时降低新表现或新学习达标次数；随机及小奇异方向限制也没有得到有效的保持收益。本轮“按初始大奇异方向选择保护对象”的具体配置不获支持。

表中为三个后续训练顺序的等权平均，不再逐顺序展开结论。三种顺序共用一个已学旧任务的模型；平均值不是跨模型估计。每个顺序旧、新评价各800题。新学习达标要求四个新任务评价格各自≥95%，达标次数不能替换为平均准确率判断。

## 结论2：残差特定分量同时影响新旧表现

'''+t2+'''

**汇报判断：** 靶向削弱使平均旧准确率从0.167%升到35.375%，但新准确率从99.500%降到67.625%；等量随机干预几乎没有改变结果。说明残差更新含有影响旧任务输出的特定结构，但削弱这些更新仍然是在新旧能力之间取舍，尚未实现两者兼顾。

本表聚焦保护组TS。先在每个训练顺序内汇总五个随机方向，再对三个顺序等权平均；不把15次干预当作15个独立模型。干预对象是新增ΔR，实际构造秩32，并逐矩阵匹配实际参数改动长度。五次随机范围保留在[备查表2](A17_R05_retention_figures/tables/table2_residual_interventions_cn.md)。

## 支持图与完整证据（按需打开）

- [图1：C净位移与终点行为](A17_R05_retention_figures/figures/figure1_protection_and_retention.png)。C净位移约减少一个数量级，旧表现没有改善。图中仍保留原始顺序点供核对；正文按方法给结论。
- [图2：靶向与随机残差干预](A17_R05_retention_figures/figures/figure2_residual_tradeoff.png)。旧表现恢复伴随新表现损失。
- [备用谱图](A17_R05_retention_figures/figures/figure3_backup_spectral_timing.png)。只在讨论时间关系时使用。
- [七方法原始21行备查](A17_R05_retention_figures/tables/table1_main_experiment_cn.md)。
- [表1汇总CSV](A17_R05_retention_figures/tables/table1_method_overview_7.csv) · [表2汇总CSV](A17_R05_retention_figures/tables/table2_residual_overview_3.csv) · [来源与核验](A17_R05_retention_figures/manifest.json)。

这次只调整汇报汇总方式，保留1200步主终点与原始结果。衰减的是优化器提出的参数更新；候选C的跨输入复用价值仍未确认。
'''
for suffix in ['_cn','']:
 p=M/f'meeting_brief_A17_R05_retention{suffix}.md';backup=F/'superseded_draft'/f'meeting_brief_before_method_overview{suffix}.md'
 if not backup.exists():shutil.copy2(p,backup)
 if suffix:p.write_text(body)
 else:p.write_text('''# Method-level overview: parameter protection and retention

The [Chinese speaking brief](meeting_brief_A17_R05_retention_cn.md) now leads with method-level means rather than per-order conclusions. Across three continuation orders, ordinary U reaches mean old/new accuracy0.292%/99.542%;top-direction TS reaches0.167%/99.500%. Both qualify on new learning in3/3orders. Fixed top protection also fails to retain old behavior. Uniform slowing gives little old retention while reducing new performance or qualification;random andtail-direction constraints do not provide useful retention.

For TS residual interventions,the original mean old/new endpoint is0.167%/99.500%;targeted weakening gives35.375%/67.625%;matched random controls give0.200%/99.533%. Targeted recovery is accompanied by new-learning loss.

[Method means CSV](A17_R05_retention_figures/tables/table1_method_overview_7.csv) · [Residual means CSV](A17_R05_retention_figures/tables/table2_residual_overview_3.csv). All means weight the three continuation orders equally. Random controls are first averaged within order. The three orders share one acquired-old model;they are not independent parent-model replicates. New qualification remains the four-cell95%gate,reported as a count out of three. Existing plots andper-order tables remain supporting evidence. Original1200endpoints andall scientific results are unchanged.
''')
(D/'method_overview_cn.md').write_text(body.replace('A17_R05_retention_figures/',''))
(D/'README_cn.md').write_text('''# A阶段方法结果总览

[唯一汇报入口](../meeting_brief_A17_R05_retention_cn.md)。正文按方法给结论，三个训练顺序只用于等权汇总。

- [方法总览与结论](method_overview_cn.md)。
- [七方法汇总CSV](tables/table1_method_overview_7.csv)。
- [残差干预汇总CSV](tables/table2_residual_overview_3.csv)。
- [原始21行主实验表](tables/table1_main_experiment_cn.md)与[逐顺序干预表](tables/table2_residual_interventions_cn.md)仅供备查。
- 两张主图与一张备用图仍在figures/，均有SVG、PDF和PNG。

[来源与核验](manifest.json)。未新增训练、干预或前向。
''')
(D/'README.md').write_text('''# A-stage method-level overview

[Single speaking entry](../meeting_brief_A17_R05_retention.md). The main reading now uses seven method means andthree intervention means. Per-order tables andplots remain supporting evidence. CSVs are in tables/table1_method_overview_7.csv andtable2_residual_overview_3.csv. No new training,intervention,or forward evaluation. [Manifest](manifest.json).
''')
shutil.copy2(Path(__file__),D/'reproduce/aggregate_methods.py')
check={'status':'PASS','aggregation':'equal-weight mean of three continuation orders; random mean within order before across-order mean','original_source_hashes_preserved':True,'accuracy_means_independently_checked_against_integer_correct_totals':True,'all7old_gain_means_checked':True,'new_qualification_counts_retained':True,'n_parent_models':1,'n_continuation_orders':3,'new_forward_or_training':False}
(D/'method_overview_verification.json').write_text(json.dumps(check,indent=2)+'\n')
manifest=old_manifest;manifest['scope']='method-level overview: seven training methods andthree residual interventions; raw-order tables andfigures supporting only';manifest['speaking_entries']=[ev(M/f'meeting_brief_A17_R05_retention{s}.md') for s in ['_cn','']];manifest['method_aggregation_verification']=ev(D/'method_overview_verification.json');manifest['files']=[ev(p) for p in sorted(D.rglob('*')) if p.is_file() and p.name not in ['manifest.json','delivery_check.json']]
(D/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
archive=E/'exports/A17_R05_conclusion_figures_20261023.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
 for p in [M/'meeting_brief_A17_R05_retention_cn.md',M/'meeting_brief_A17_R05_retention.md']+sorted(p for p in D.rglob('*') if p.is_file()):z.write(p,p.relative_to(M))
print(json.dumps({'status':'PASS','method_means':a,'residual_means':b,'brief':str(M/'meeting_brief_A17_R05_retention_cn.md'),'archive':ev(archive)},ensure_ascii=False))
