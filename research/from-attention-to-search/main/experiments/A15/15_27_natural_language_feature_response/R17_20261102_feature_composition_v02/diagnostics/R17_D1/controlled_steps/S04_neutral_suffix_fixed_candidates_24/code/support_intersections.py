"""Full-support intersections only; no candidate selection."""
from common import *
import numpy as np
rr=[]
for site in SITES:
 for ctx in ['old','new']:
  z=np.load(R/'cache/new.npz')[site+'__z'] if ctx=='new' else np.concatenate([np.load(OLD/f'cache/{sp}.npz')[site+'__z'] for sp in ['exploration','heldout_check']])
  for fi in range(6):
   ss=[set(np.flatnonzero(z[fi*4+j]>0)) for j in range(4)];triple=set.intersection(*ss[:3]);four=set.intersection(*ss);un=set.union(*ss[:3])
   rr.append(dict(site=site,context=ctx,family=f'F{fi+1:02d}',split='exploration' if fi<3 else 'heldout_check',P_count=len(ss[0]),cat_count=len(ss[1]),dog_count=len(ss[2]),N_count=len(ss[3]),PCD_intersection=len(triple),PCD_union=len(un),PCDN_intersection=len(four),PCD_over_P=f'{len(triple)}/{len(ss[0])}',PCD_over_union=f'{len(triple)}/{len(un)}',PCD_intersection_IDs=' '.join(map(str,sorted(triple))),PCDN_intersection_IDs=' '.join(map(str,sorted(four)))))
table(R/'results/actual_intersections.csv',rr)
for site in SITES:
 p=C/site/'H1_comparison_cn.md'
 with p.open('a') as f:
  f.write('\n## 全字典实际共同支持（独立于冻结候选）\n\n这些是所有30000坐标的支持交集，不是新增筛选出的候选；没有给它们赋语义。\n\n| 家族 | 旧PCD交集/P | 新PCD交集/P | 旧/新PCDN交集 |\n|---|---|---|---|\n')
  for fi in range(6):
   ff=f'F{fi+1:02d}';o=next(x for x in rr if x['site']==site and x['context']=='old' and x['family']==ff);n=next(x for x in rr if x['site']==site and x['context']=='new' and x['family']==ff);f.write(f'| {ff} | {o["PCD_over_P"]} | {n["PCD_over_P"]} | {o["PCDN_intersection"]}/{n["PCDN_intersection"]} |\n')
  f.write('\n交集完整ID、并集与分母见[实际交集表](../results/actual_intersections.csv)。\n')
print('FULL_SUPPORT_INTERSECTIONS_RECORDED')
