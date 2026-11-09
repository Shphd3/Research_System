"""Reader-facing explanation from unchanged frozen tables; no new selection or analysis."""
from common import *
def mdtab(h,rr):return '\n'.join(['| '+' | '.join(h)+' |','| '+' | '.join(['---']*len(h))+' |']+['| '+' | '.join(str(v) for v in row)+' |' for row in rr])+'\n'
coverage=list(csv.DictReader(open(R/'results/pattern_coverage.csv')))
def n3(site,g):return sum(r['site']==site and r['group']==g and r['split']=='heldout_check' and r['matches']=='3' for r in coverage)
overview='''\n本轮最直接的认识更新是：粗细文本的关系在这里表现为**部分成员保留、另一些成员换入换出，同时固定共同列表内比例也发生变化**。不是细类简单包含P的全部活跃成员。每条均为Top32，因此新增数与消失数相同；这个等式来自固定稀疏预算，本身不是概念规律。\n\n'''+mdtab(['接口','共同候选在3个检查家族均满足','猫新增候选均满足','狗新增候选均满足','H2方向在3对均同向'],[[s]+[f'{n3(s,g)}/6个候选' for g in ['H1_common','H1_added_cat','H1_added_dog','H2']] for s in SITES])+'''
“均满足”只是便于阅读的3/3计数，不是新增筛选门槛；所有6个候选的0/3、1/3和2/3结果都在后文，未保留漂亮结果来替换失败者。H2两个接口各有3/6候选方向在三个检查家族均保持，也各有反向。固定列表支持相同均6/6对，全字典支持相同均0/6对。原H1/H2额外信息仍未验证。
'''
path=C/'summary_cn.md';txt=path.read_text();marker='本次事实按三条路径阅读：';txt=txt.replace(marker,overview+'\n'+marker,1)
focus='\n### 用F01把实际数值连起来\n\n四条完整前文如下。它们与后文数字一一对应；猫狗两条沿用S02原件。\n\n'+ '\n\n'.join('```text\n'+p['prefix']+'\n```' for p in rows(R/'data/panel.jsonl')[:4])+'\n\n'
examples={'ATTN_SAE':[('H1_common',9495),('H1_added_cat',22344),('H2',23899)],'MLPIN_SAE':[('H1_common',25899),('H1_added_cat',22958),('H2',2682)]}
for site in SITES:
 rr=list(csv.DictReader(open(R/f'results/{site}/candidate_values.csv')));focus+=f'\n**{site}：**\n\n'
 for group,i in examples[site]:
  xx=[r for r in rr if r['group']==group and r['atom']==str(i) and r['family']=='F01']
  focus+=f'#{i}，固定列表{group}：\n\n'+mdtab(['条件','z','decoder范数','u','该列表q_weighted','preactivation'],[[r['condition']]+[f'{float(r[k]):.6f}' if r[k] else '未定义该量' for k in ['z','decoder_norm','u','q_weighted','preactivation']] for r in xx])+'\n'
 if site=='ATTN_SAE':
  focus+='共同候选#9495在P／猫／狗为正而N为0；但N的preactivation=0.679426仍为正，最终未进入Top32。新增候选#22344在P的preactivation=2.313256也为正而最终z=0，猫为11.523227，狗也为4.663494；它是原SAE规则下的支持新增，不是从编码器完全无响应变为有响应，也不是猫独占。H2的#23899在猫的原始z=34.930103低于狗35.805733，而固定6成员内q=0.713141高于狗0.711806，说明“原始更大”与“列表内占比更大”是不同事实。\n\n'
 else:
  focus+='共同候选#25899在前三条件均正、N为0；新增候选#22958在F01只有猫进入Top32，狗preactivation=1.518781仍未入选，不能只凭这个例子赋予唯一猫语义。H2的#2682猫／狗原始z=20.324385/22.410387，相对q=0.267951/0.288898，探索冻结方向为dog较强；该方向在3个检查家族均相同。正文仍明确出现cat/dog，复制解释未排除。\n\n'
 failures=[r for r in csv.DictReader(open(R/f'results/{site}/H2_directions.csv')) if r['split']=='heldout_check' and r['direction_matches']=='False']
 focus+='该接口H2在保留家族的**全部**反向或零向例：\n\n'+mdtab(['家族','ID','冻结方向','cat z','dog z','cat q','dog q'],[[r['family'],r['atom'],r['discovery_direction']]+[f'{float(r[k]):.6f}' for k in ['cat_z','dog_z','cat_q_weighted','dog_q_weighted']] for r in failures])+'\n'
focus+='H1反例见各接口casebook的末节，例如ATTN共同候选#13973在F04–F06的P都为0，而猫狗均正，故探索3/3、检查0/3。它不能继续称作跨这6种句式稳定的父类共同成员。全部H1失败保留在失败表。\n\n'
txt=txt.replace('## 5. 结论与认识更新',focus+'\n## 5. 结论与认识更新',1);path.write_text(txt)
p=C/'summary.md';t=p.read_text();overview_en='\nSelected candidates satisfying all three check families (descriptive counts, no new selection):\n\n'+mdtab(['site','H1 common','H1 cat added','H1 dog added','H2 direction'],[[s]+[f'{n3(s,g)}/6' for g in ['H1_common','H1_added_cat','H1_added_dog','H2']] for s in SITES])+'''
The observed organization is partial retention plus recruitment/loss, alongside redistribution within a fixed shared list. Each row has32active coordinates, so additions equal losses by design; the fine response is not a strict support superset of P. Every failed candidate remains reported. The same selected-list support holds in6/6pairs at both sites, while full-support equality holds in0/6. Original incremental-information claims remain untested.

Concrete F01: ATTN #9495 raw P/cat/dog/N=30.342440/30.277794/28.684868/0; #22344=0/11.523227/4.663494/0, but P preactivation=2.313256>0, excluded by Top32. ATTN H2 #23899 raw cat/dog=34.930103/35.805733, q=0.713141/0.711806: normalized direction can differ from raw direction. MLPIN #25899 raw=20.408159/18.879515/19.352499/0; #22958=0/6.376107/0/0. MLPIN H2 #2682 raw cat/dog=20.324385/22.410387, q=0.267951/0.288898, with dog-stronger direction repeating in all3check families. Full inputs and all opposite examples are in the casebooks.
''';t=t.replace('## Bounded interpretation and stop',overview_en+'\n## Bounded interpretation and stop');p.write_text(t)
dump(R/'evidence/reader_explanation.json',dict(UTC=now(),source='unchanged fixed tables',added='F01 complete inputs, raw/weighted/relative examples, all H2 check reversals, full-check integer overview',selection_unchanged=sha(R/'results/selection.json')))
