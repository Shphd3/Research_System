"""Posthoc measurement/identification audit; no new interventions or refitting."""
from common import *
import numpy as np,shutil
rr=rows(R/'results/conditions.jsonl');a=np.load(R/'cache/all_injected_deltas.npz');delta=a['delta_hidden'];index={s:i for i,s in enumerate(a['condition_ids'])};lk={(x['text_id'],x['site'],x['intervention_domain'],x['arm'],x['group'],x['alpha'],x['destination']):x for x in rr};out=[];summary=[]
for s in SITES:
 for d,ls in DOMAINS.items():
  vals=[]
  for r in rr:
   if not(r['site']==s and r['intervention_domain']==d and r['wording']=='explicit' and r['label'] in ls[1:] and r['arm']=='strength' and r['alpha']==.5 and r['destination']!=r['label']):continue
   c=lk[(r['text_id'],s,d,'strength_shuffle','common',.5,r['destination'])];u=delta[index[r['condition_id']]].astype(float);v=delta[index[c['condition_id']]].astype(float);co=float(u@v/np.linalg.norm(u)/np.linalg.norm(v));vals.append(co)
   out.append(dict(site=s,domain=d,text_id=r['text_id'],family=r['family'],label=r['label'],members=len(r['feature_ids']),candidate_id=r['condition_id'],shuffle_id=c['condition_id'],actual_delta_cosine=co,candidate_norm=float(np.linalg.norm(u)),shuffle_norm=float(np.linalg.norm(v)),role='posthoc diagnostic, not additional confirmation test'))
  summary.append(dict(site=s,domain=d,N=16,min_cos=min(vals),median_cos=float(np.median(vals)),max_cos=max(vals),near_same_gt_0p99=sum(v>.99 for v in vals),near_opposite_lt_minus0p99=sum(v<-.99 for v in vals)))
table(R/'results/control_delta_geometry.csv',out);table(R/'results/control_delta_geometry_summary.csv',summary)
audit='''# Reasoning audit: control geometry and category comparison

After the registered14976conditions and their statistics were complete, inspection of actual injected-vector alignment showed that the same-member shuffled control is not uniformly an independent new direction. In a positive two-member list at fixed L2norm, only one angular degree of freedom remains. A norm-matched movement can nearly coincide with the target or reverse it. This is an algebraic constraint on the control, not a newly discovered semantic rule. The measured per-text cosines are preserved, not filtered.

The registered statistics remain unchanged: they identify only the actual chosen perturbation contrast. Do not upgrade that contrast to a claim about arbitrary shuffles or many independent compositional directions. Differences between animal and vehicle can reflect list dimensionality/control sensitivity as well as category content. Existing own-side, other-member and norm controls remain available; no new direction/threshold is selected or used to rescue a prediction. A new experiment is unnecessary to explain this current design limitation. This audit refines the interpretation within the user's reasoning-audit request, not the frozen intervention protocol.
'''
(R/'evidence/control_geometry_reasoning_audit.md').write_text(audit)
cn='''\n## 追加控制几何审核（事后测量诊断）

交通工具Attention固定共同组只有2个正成员，固定L2范数后只有1个角度自由度。实际alpha.5目标／打乱注入向量的余弦既有接近+1也有接近−1；F09汽车中两改动几乎相同。因此原检验只识别这些实际选择的有限方向对比，不证明对任意打乱都特异。动物Attention的16个逐文本余弦中位数约.8164，部分也近乎同向。两大类的不同结果还可能来自列表维数／控制能力，不应唯一归因类别组织。完整逐文本数据与范围见results/control_delta_geometry*.csv。本诊断未新增干预、筛选或改变主判定，也不救回未支持结果。
'''
for name in ['summary_cn.md','detailed_cn.md']:
 p=R/name;t=p.read_text();assert '追加控制几何审核' not in t;p.write_text(t+cn);shutil.copy2(p,C/name)
for name in ['summary.md','detailed.md']:
 p=R/name;t=p.read_text();p.write_text(t+'\nPosthoc control-geometry audit: the two-member Attention-vehicle list has only one angular degree of freedom at fixed norm. Some matched shuffles coincide with or reverse actual target perturbations. The contrast concerns these chosen directions, not arbitrary independent compositional changes. Category differences can therefore reflect list dimension/control sensitivity. No original statistic or selection changed; per-text delta cosines are retained.\n');shutil.copy2(p,C/name)
for name in ['control_delta_geometry.csv','control_delta_geometry_summary.csv']:shutil.copy2(R/'results'/name,C/'results'/name)
shutil.copy2(R/'evidence/control_geometry_reasoning_audit.md',C/'evidence/control_geometry_reasoning_audit.md')
print(summary,flush=True)
