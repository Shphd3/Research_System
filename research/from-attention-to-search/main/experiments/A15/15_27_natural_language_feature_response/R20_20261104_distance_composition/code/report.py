from load_data import *
from stats import *
import pandas as pd,math,re
pair=pd.read_csv(R/'tables/baseline_pair_metrics.csv');fact=pd.read_csv(R/'tables/baseline_fact_contrasts.csv');fm=pd.read_csv(R/'tables/baseline_fact_metrics.csv');summ=pd.read_csv(R/'tables/baseline_summaries.csv');frequency=pd.read_csv(R/'tables/baseline_frequency_pairs.csv');fsumm=pd.read_csv(R/'tables/baseline_frequency_summaries.csv');coverage=pd.read_csv(R/'tables/baseline_frequency_coverage.csv');threshold=pd.read_csv(R/'tables/threshold_summaries.csv');ctrl=pd.read_csv(R/'tables/controls_summaries.csv');primary=json.load(open(R/'results/primary_hypotheses.json'));selection=json.load(open(R/'results/case_selection.json'));b=behavior(True);families={p['family']:p for p in json.load(open(R/'data/families.json'))}
def n(x,digits=4):
 if x is None:return 'NA'
 if isinstance(x,(float,np.floating)):return 'NA' if not np.isfinite(x) else f'{x:.{digits}f}'
 return str(x)
def md(headers,body):return '| '+' | '.join(headers)+' |\n|'+'|'.join(['---']*len(headers))+'|\n'+''.join('| '+' | '.join(n(x).replace('|','/') for x in rr)+' |\n' for rr in body)+'\n'
def get(site,metric,lo=16,hi=128):return summ[(summ.site==site)&(summ.split=='heldout')&(summ.metric==metric)&(summ.distance_left==lo)&(summ.distance_right==hi)].iloc[0]
verdict={'SUPPORTED':'支持','NOT_SUPPORTED':'未支持','INSUFFICIENT':'证据不足'}
ph=md(['字典','操作假设','家族N','估计','95%家族区间','Holm p','判定'],[[h['site'],h['hypothesis'],h['N'],h['value'],f"[{n(h['lo'])}, {n(h['hi'])}]",h['holm_p'],verdict[h['verdict']]] for h in primary])
main_table=md(['字典','16→128共同/32','平均换入=换出','原始事实差异范数比','整体码尺度比','相对事实差异比','完整事实差方向cos'],[[site,get(site,'shared').value,32-get(site,'shared').value,get(site,'native_log_raw_ratio').value,get(site,'native_log_total_scale_ratio').value,next(h['value'] for h in primary if h['site']==site and h['hypothesis']=='H2'),get(site,'native_raw_contrast_cosine').value] for site in SITES])
ct=md(['字典','条件','N','相对事实差异128/16','95%家族区间'],[[site,frame,int(q.families),q.value,f'[{n(q.lo)}, {n(q.hi)}]'] for site in SITES for frame in ['reverse','content','fixed_e'] for _,q in ctrl[(ctrl.site==site)&(ctrl.frame==frame)&(ctrl.split=='heldout')&(ctrl.distance_left==16)&(ctrl.distance_right==128)&(ctrl.metric=='native_log_relative_ratio')].iterrows()])
bp=pd.concat([pd.read_csv(R/'tables/baseline_behavior_pairs.csv'),pd.read_csv(R/'tables/controls_behavior_pairs.csv')]);beh=[]
for (frame,d),q in bp[bp.split=='heldout'].groupby(['frame','distance']):
 lo,hi=interval(q.mean_margin);beh.append([frame,int(d),len(q),int(q.paired.sum()),q.mean_margin.mean(),f'[{n(lo)}, {n(hi)}]',int(q.item_paired.sum())])
bh=md(['条件','实际d','家族N','完整候选成对正确','平均正确分差nat','95%家族区间','仅物品词成对正确'],beh)
freqt=md(['字典','参考组','字典基数','本任务出现成员','位置/72','家族/12'],[[r.site,r.group,r.dictionary_members,r.observed_members,r.positions,r.families] for _,r in coverage[coverage.split=='heldout'].iterrows()])
fn=md(['字典','参考组','共同成员','换入','换出','参考期待换入','任务期待换入','绝对改变占比'],[[site,group,q.shared.mean(),q.entered.mean(),q.exited.mean(),q.reference_expected_entries.mean(),q.task_expected_entries.mean(),q.absolute_change_share.mean()] for site in SITES for group in GROUPS for q in [frequency[(frequency.site==site)&(frequency.split=='heldout')&(frequency.distance_left==16)&(frequency.distance_right==128)&(frequency.group==group)]]])
cases_dir=C/'cases';cases_dir.mkdir(exist_ok=True);data={site:load_site(site,True)[0] for site in SITES};case_overview=[]
case_explain={
 'F11':'这是两套字典平均成员保留最多的一族，但保留较多成员也没有保证事实差异幅度精确不变：两处的相对事实差异都略小于近距。三个距离仍成对答对，它是总体均值不减弱之下保留的局部反例。',
 'F15':'这是平均成员更替最多的一族，事实差异幅度却没有随之缩小。成员名单变化与A/B差异保留可以同时出现，不能把每次换入换出都叫作遗忘。',
 'F27':'两字典的相对事实差异变化很小且方向不同，完整事实差的方向也没有像预选六成员那样接近完全一致。这里的幅度、方向与答题成功是三件事，不能互相替代。',
 'F19':'同一文本族在Attention与MLP输入呈相反变化：前者的相对差异约降到0.79，后者约升到1.89，回答却始终正确。这个反例说明，一个字典中的距离比值不能直接作为模型总体事实信息量；本轮也未检验两个接口的机制差异。'}
for case in selection['families']:
 fam=case['family'];meta=families[fam];mainrows=[];full=[f'# Literal distance case {fam}: {meta["A"]} / {meta["B"]}\n\n',f'Rule: {case["reason"]}. Entire family is old representation-heldout; no case is used as a new confirmation sample. [Chinese reading]({fam}_cn.md).\n\n']
 full.append('## Complete prefixes and candidate scores\n\n')
 for d in DISTS:
  for g in 'AB':
   pid=cid('baseline',fam,d,g);p=META[pid];bb=b[pid];full.append(f'### {pid}\n\nGap={d}, e={p["evidence_last_position"]}, p={p["target_position"]}, item token IDs={p["evidence_token_ids"]}, target tokenID={p["target_token_id"]}.\n\n```text\n{p["text"]}\n```\n\n');full.append(md(['Candidate','token IDs','token log probabilities','complete total','item total','period'],[[repr(c['text']),str(c['token_ids']),str(c['token_logprobs']),c['total_logprob'],c['item_logprob'],c['period_logprob']] for c in bb['candidates']]))
 for site in SITES:
  full.append(f'## {site}: complete native members and strengths\n\n');ref=pd.read_csv(R/f'data/{site}_reference_frequency.csv').set_index('atom')
  for g in 'AB':
   vals={d:data[site][cid('baseline',fam,d,g)]['z'] for d in DISTS};ids=sorted(set().union(*[set(np.flatnonzero(v)) for v in vals.values()]));full.append(f'### Target {g}: union across all three distances\n\n');full.append(md(['ID','fixed reference group','z16','z64','z128'],[[int(atom),ref.loc[atom,'group']]+[float(vals[d][atom]) for d in DISTS] for atom in ids]))
   for lo,hi in PAIRS:
    left=set(np.flatnonzero(vals[lo]));right=set(np.flatnonzero(vals[hi]));full.append(f'{lo}→{hi}: common{sorted(map(int,left&right))}; entered{sorted(map(int,right-left))}; exited{sorted(map(int,left-right))}. Entry=exit count follows Top32.\n\n')
  q=fm[(fm.site==site)&(fm.family==fam)&fm.view.isin(['native','six'])];full.append(md(['distance','view','raw A-B norm','relative separation','all six active','fact-difference reconstruction error'],[[r.distance,r.view,r.raw_delta_norm,r.relative_separation,r.all_six_positive,r.fact_reconstruction_relative_error] for _,r in q.iterrows()]))
  q=fact[(fact.site==site)&(fact.family==fam)&(fact.view=='native')&(fact.distance_left==16)&(fact.distance_right==128)].iloc[0];pr=pair[(pair.site==site)&(pair.family==fam)&(pair.distance_left==16)&(pair.distance_right==128)];mainrows.append([site,pr.shared.mean(),32-pr.shared.mean(),np.exp(q.log_raw_ratio),np.exp(q.log_relative_ratio),q.raw_contrast_cosine]);case_overview.append(dict(family=fam,role=case['role'],site=site,shared=float(pr.shared.mean()),relative_ratio=float(np.exp(q.log_relative_ratio)),direction=float(q.raw_contrast_cosine)))
 (cases_dir/f'{fam}.md').write_text(''.join(full));text=case_explain.get(fam,'按预定规则选择，完整数值保留；该例不代替总体比较。');(cases_dir/f'{fam}_cn.md').write_text(f'# {fam}：{meta["A"]}/{meta["B"]}\n\n选择角色：{case["role"]}。{text}\n\n'+md(['字典','共同/32','换入/换出','原始差异比','相对差异比','差方向cos'],mainrows)+f'原始完整候选在三个距离均成对正确。全部原文、token位置、逐候选分数、成员并集、逐成员频率与三档强度保存在[完整原始案例]({fam}.md)。\n\n![真实六成员与行为](../figures/case_{fam}.png)\n')
overview='# 四个预定规则选出的案例\n\n规则在新分析前写入协议：按稳定、较大更替、剩余中差异比最小、反向/字典分歧依次选不同家族。F11已是整体均值的反向例；没有剩余的跨两字典平均反向族，因此第四例按预定备用规则取字典分歧最大的F19。所有12族均参与总体统计，没有用案例筛选检验。\n\n'
for case in selection['families']:
 fam=case['family'];overview+=f'## {fam}：{families[fam]["A"]}/{families[fam]["B"]}\n\n'+case_explain[fam]+f'\n\n[中文读法](cases/{fam}_cn.md) · [完整原文、所有成员和原始评分](cases/{fam}.md)。\n\n'
newfails=[x for x in b.values() if x['id'] in META and META[x['id']]['provenance']=='NEW_FORWARD' and not x['correct']];faildoc=['# All supplemental behavioral failures\n\nNo failed condition was deleted or replaced.\n\n']
for bb in newfails:
 p=META[bb['id']];faildoc.append(f'## {bb["id"]}\n\nCondition={p["condition"]},gap={p["actual_distance"]},e={p["evidence_last_position"]},p={p["target_position"]}; correct margin={bb["correct_margin"]}.\n\n```text\n{p["text"]}\n```\n\n'+md(['candidate','token IDs','per-token logp','full score'],[[repr(c['text']),str(c['token_ids']),str(c['token_logprobs']),c['total_logprob']] for c in bb['candidates']]))
(C/'supplement_failures.md').write_text(''.join(faildoc));overview+='## 补充对照中的全部失败\n\n填充反转的近距F28/stamp一条答错，完整分差−0.084757nat；其远距仍成对答对。[完整原文与原始分数](supplement_failures.md)。这说明即使距离固定很近，填充顺序也会影响偏好，不能只按距离解释成功或失败。\n';(C/'casebook_cn.md').write_text(overview);(C/'casebook.md').write_text('# Rule-selected cases\n\nThe fixed rule selects F11,F15,F27,F19. F11 is both relatively stable in membership and contrary to the average amplitude trend; the fourth uses the predeclared cross-site-disagreement fallback. All original prefixes, every member in the three-distance union, fixed frequency groups and literal candidate-token scores are stored once in the English raw cases: '+', '.join(f'[{x["family"]}](cases/{x["family"]}.md)' for x in selection['families'])+'. Chinese interpretation: [casebook](casebook_cn.md). [All supplemental failures](supplement_failures.md) remain. No illustrative selection changes the complete-family analysis.\n')
table(R/'tables/case_overview.csv',case_overview)
annex='# Numeric evidence / 数值证据\n\n## Main comparison / 主比较\n\n'+main_table+'## Operational hypotheses / 操作假设\n\n'+ph+'## Full behavior / 完整行为\n\n'+bh+'## New controls / 新对照\n\n'+ct+'## Frequency coverage / 频率覆盖\n\n'+freqt+'## Frequency changes16→128 / 频率变化\n\n'+fn+'## Every old-heldout family / 原留出逐家族\n\n'
q=fact[(fact.split=='heldout')&(fact.view=='native')&(fact.distance_left==16)&(fact.distance_right==128)];annex+=md(['字典','家族','原始差异比','整体尺度比','相对差异比','差异方向cos','沿近距方向投影增益'],[[r.site,r.family,np.exp(r.log_raw_ratio),np.exp(r.log_total_scale_ratio),np.exp(r.log_relative_ratio),r.raw_contrast_cosine,r.projection_gain] for _,r in q.iterrows()]);annex+='\nAll three pairs, confidence intervals, raw strengths, zeros, group opportunities and every feature ID are retained in the execution tables and result packet. Primary intervals use the registered site-specific seed; descriptive tables use the common recorded seed, so MonteCarlo bootstrap endpoints may differ slightly.\n';(C/'numeric_evidence.md').write_text(annex)
print('RAW_CASES_AND_ANNEX',list(x['family'] for x in selection['families']),len(newfails))
