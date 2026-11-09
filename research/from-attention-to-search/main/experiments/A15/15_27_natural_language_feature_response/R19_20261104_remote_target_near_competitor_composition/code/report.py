from common import *
import pandas as pd,numpy as np,shutil
primary=json.load(open(R/'results/primary_hypotheses.json'));joint=json.load(open(R/'results/joint_hypotheses.json'));geo=pd.read_csv(R/'tables/family_geometry.csv');mem=pd.read_csv(R/'tables/membership_summary.csv');freq=pd.read_csv(R/'tables/frequency_coverage.csv');sens=pd.read_csv(R/'tables/declared_sensitivities.csv');spec=json.load(open(R/'data/candidates.json'))['sites'];panel={x['id']:x for x in rows(R/'data/panel_portable.jsonl')};behavior={x['id']:x for split in ['smoke','discovery','heldout'] for x in rows(R/f'results/behavior_{split}.jsonl')};bsummary=pd.read_csv(R/'tables/behavior_summary.csv');cases=json.load(open(R/'results/case_selection.json'))
def num(x):return 'NA' if x is None or (isinstance(x,float) and not np.isfinite(x)) else f'{x:.4f}' if isinstance(x,(float,np.floating)) else str(x)
def md(headers,rows):return '| '+' | '.join(headers)+' |\n|'+'|'.join(['---']*len(headers))+'|\n'+''.join('| '+' | '.join(num(v).replace('|','/') for v in rr)+' |\n' for rr in rows)+'\n'
vcn={'SUPPORT_IN_THIS_PANEL':'支持（本面板）','LOCAL_SUPPORT_ONLY':'局部支持；完整关联未通过','NOT_SUPPORTED':'未支持','INSUFFICIENT':'证据不足'}
ph=md(['SAE','假设','合格家族/12','均值或ρ','95%家族区间','Holm p','判定'],[[x['site'],x['hypothesis'],x['N'],x['mean'],f"[{num(x['lo'])}, {num(x['hi'])}]",x['holm_p'],vcn[x['verdict']]] for x in primary])
jh=md(['SAE','联合层','固定对数','家族数','留出投影','95%家族区间','Holm p','判定'],[[x['site'],x['kind'],x['selected_pairs'],x['families'],x['score'],f"[{num(x['lo'])}, {num(x['hi'])}]",x['holm_p'],vcn[x['verdict']]] for x in joint])
bh=md(['条件','留出成对正确/12','留出正确前缀/24','留出平均正确分差nat','全部24家族成对正确'],[[co,int(bsummary[(bsummary.split=='heldout')&(bsummary.condition==co)].iloc[0].paired),int(bsummary[(bsummary.split=='heldout')&(bsummary.condition==co)].iloc[0].correct_prompts),bsummary[(bsummary.split=='heldout')&(bsummary.condition==co)].iloc[0].mean_margin,int(bsummary[bsummary.condition==co].paired.sum())] for co in ['main16','main64','main128','matched_neutral','matched_congruent','matched_opposite']])
mh=md(['SAE','比较','家族数','平均共同成员','平均换入=换出','平均Jaccard','95%家族区间'],[[site,role,12,r.mean_shared,r.mean_entered,r.mean_Jaccard,f'[{num(r.lo)}, {num(r.hi)}]'] for site in SITES for kind,role in [('content','main128'),('distance','16_to_128'),('competition','neutral_to_opposite')] for _,r in mem[(mem.site==site)&(mem.split=='heldout')&(mem.kind==kind)&(mem.role==role)].iterrows()])
fh=md(['SAE','参考组','本次成员数/参考成员数','阳性位置/144','家族/12','阳性成员-位置次数'],[[r.site,r.group,f'{r.observed_members}/{r.reference_members}',r.positions,r.families,r.active_instances] for _,r in freq[freq.split=='heldout'].iterrows()])
details=[]
for site in SITES:
 h=next(x for x in primary if x['site']==site and x['hypothesis']=='H3');s=h['secondary'];g=geo[(geo.site==site)&(geo.split=='heldout')]
 details.append(f"{site}: C={spec[site]['C']}；R={spec[site]['responsive']}。严格远矩阵支持 {int(g.H1_eligible.sum())}/12；近远支持 {int(g.H2_eligible.sum())}/12。H3平均模式损失={num(s['pattern_loss_mean'])}，CI={s['pattern_loss_CI']}；平均正确分差损失={num(s['behavior_loss_mean'])} nat，CI={s['behavior_loss_CI']}。单物品词评分的关联ρ={num(s['item_association']['rho'])}；模板内交换p={num(s['association']['template_p'])}。严格不合格家族：{', '.join(g[~g.H1_eligible].family) or '无'}。")
casefamilies=['F23']+sorted({'F27','F28','F11'}|{x['counter'] for x in cases if x['counter'] and x['counter']!='F23'});a=np.load(R/'cache/heldout.npz');by={str(pid):i for i,pid in enumerate(a['ids'])};casebook=['# 完整原文、真实 feature 与候选评分\n\nF23在留出读取前固定，取自旧R18首次留出失败；反例按协议规则确定，不更换主要六成员。所有数字来自真实前向。ID只在本字典有意义；本表不是语义命名或因果贡献。灰/零值代表实际未激活，不补选成员。\n\n']
for fam in casefamilies:
 casebook.append(f'## {fam}\n\n')
 rr=[f'{fam}_{co}_{gold}' for co in CONDS for gold in 'AB'] if fam=='F23' else [f'{fam}_{co}_{gold}' for co in ['nearN','nearA','nearB'] for gold in 'AB']
 for site in SITES:
  ids=spec[site]['C'];casebook.append(f'### {site}：同一固定六成员\n\n')
  table_rows=[]
  for pid in rr:
   k=by[pid];v=dict(zip(a[site+'__indices'][k],a[site+'__values'][k]));b=behavior[pid];table_rows.append([pid]+[float(v.get(f,0)) for f in ids]+[b['candidates'][0]['total_logprob'],b['candidates'][1]['total_logprob'],b['choice'],b['correct_margin']])
  casebook.append(md(['文本ID']+['#'+str(f) for f in ids]+['候选A总分','候选B总分','选择','正确分差'],table_rows))
  gg=geo[(geo.site==site)&(geo.family==fam)].iloc[0];casebook.append(f"同一族的相对强弱分解：T投影={num(gg.relative_target_projection)}，近词N投影={num(gg.relative_near_projection)}，相反条件保留={num(gg.relative_opposite_projection)}；模式损失={num(gg.relative_pattern_loss)}，行为分差损失={num(gg.behavior_loss)} nat；严格支持={gg.H3_eligible}。T−N为恒等式，不是额外发现。\n\n")
 for pid in rr:
  p=panel[pid];b=behavior[pid];casebook.append(f"### {pid}：完整前缀\n\n远目标={p['evidence_item']}；近处={p['near_item']}；e={p['evidence_last_position']}，目标物品token={p['evidence_token_ids']}；p={p['target_position']}，token={p['target_token_id']}；d={p['actual_distance']}。近处token位置={p['near_token_positions']}，IDs={p['near_token_ids']}。\n\n```text\n{p['text']}\n```\n\n")
  casebook.append(md(['候选完整串','token IDs','逐token条件log p','完整总分','物品部分','句号部分'],[[repr(c['text']),str(c['token_ids']),str(c['token_logprobs']),c['total_logprob'],c['item_logprob'],c['period_logprob']] for c in b['candidates']]))
(C/'casebook_cn.md').write_text(''.join(casebook));(C/'casebook.md').write_text('# Literal cases and scores\n\n[Full literal English prefixes, actual feature IDs/values and unrounded token scores](casebook_cn.md) are stored once. The explanatory text is Chinese; the examples themselves retain the original English. F23 was fixed before heldout extraction; the counterexamples follow the registered deterministic rule. No candidate list was changed. [Summary](summary.md) provides the English scientific interpretation.\n')
# Single, shared numeric annex avoids rounding or translation divergence.
annex='# Numeric evidence / 数值证据\n\n## Behavioral reference / 行为参照\n\n'+bh+'## Membership / 成员\n\n'+mh+'## Primary hypotheses / 主要假设\n\n'+ph+'## Joint tests / 联合检验\n\n'+jh+'## Reference groups / 频率支持\n\n'+fh+'## Heldout family geometry / 留出逐家族\n\n'
annex+=md(['SAE','家族','远矩阵严格','近远严格','H1cos','H2cos','T投影','N投影','相反投影','模式损失','分差损失nat','相反成对正确'],[[r.site,r.family,r.H1_eligible,r.H2_eligible,r.relative_target_alignment,r.relative_near_far_cosine,r.relative_target_projection,r.relative_near_projection,r.relative_opposite_projection,r.relative_pattern_loss,r.behavior_loss,r.opposite_paired] for _,r in geo[geo.split=='heldout'].iterrows()])
annex+='## Predeclared sensitivity / 预定敏感性\n\nFirst3and fixed-list-with-zeros never replace the primary support denominator. / 三成员与含零分析不替代主要分母。\n\n'+md(['SAE','C大小','表示','远矩阵严格/12','平均H1cos（全部有定义）','平均H2cos（全部有定义）'],[[site,n,form,int(q.all6far_positive.sum()),q.target_alignment.mean(),q.near_far_cosine.mean()] for site in SITES for n in [3,6] for form in ['raw','relative'] for q in [sens[(sens.site==site)&(sens.split=='heldout')&(sens['size']==n)&(sens.form==form)]]])
(C/'numeric_evidence.md').write_text(annex)
# These result files are used by the subsequent interpretive writer and curator.
dump(R/'results/report_numbers.json',dict(primary=primary,joint=joint,site_notes=details,case_families=casefamilies))
print('CASEBOOK_AND_NUMERIC_RECORDS',casefamilies)
