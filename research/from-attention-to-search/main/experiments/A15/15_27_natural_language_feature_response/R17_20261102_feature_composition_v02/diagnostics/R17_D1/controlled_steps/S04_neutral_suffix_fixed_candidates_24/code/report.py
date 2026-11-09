from common import *
import numpy as np
def readcsv(p):return list(csv.DictReader(open(p)))
def mdtab(h,rr):return '\n'.join(['| '+' | '.join(h)+' |','| '+' | '.join(['---']*len(h))+' |']+['| '+' | '.join(str(v) for v in row)+' |' for row in rr])+'\n'
def f(x,n=6):return '不可定义' if x in [None,''] else f'{float(x):.{n}f}'
def yes(x):return '是' if x in [True,'True'] else '否'
def arrow(x):return '不可定义' if x in [None,''] else '+' if int(x)>0 else '−' if int(x)<0 else '0'
def counts(c):return '/'.join(c[k] for k in ['same','opposite','member_inactive','zero_norm','zero_difference','no_reference'])
panel=rows(R/'data/panel.jsonl');behavior=rows(R/'results/behavior_raw.jsonl');summary=json.load(open(R/'results/summary.json'));ver=json.load(open(R/'evidence/verification.json'));plan=json.load(open(R/'frozen_plan.json'));selection=json.load(open(R/'data/S03_frozen_selection.json'))['sites'];run=json.load(open(R/'evidence/run_complete.json'));ct=readcsv(R/'results/H2_direction_counts.csv');pc=readcsv(R/'results/H1_pattern_coverage.csv')
C.mkdir(exist_ok=True);bb={b['id']:b for b in behavior}
data=['# S04：24条完整前文、token与原模型分数\n','所有正文沿用S03，唯一后缀精确为换行+`Description:`。两完整候选` cat.`→[8251,13]、` dog.`→[5562,13]，均2个token，含前导空格与句号。总分含全部token，不校正先验或长度。P/N无正确答案；不能把偏好当作正确分类。\n']
for p in panel:
 b=bb[p['id']];data += [f"## {p['id']} · {p['split']} · {p['labels']}\n",'```text\n'+p['prefix']+'\n```\n',f"完整token IDs：`{p['token_ids']}`；token pieces：`{p['token_pieces']}`。目标`:`，ID25，0起位置{p['target_index_zero_based']}／1起{p['target_index_one_based']}。旧目标` a`，ID264，0起位置{p['old_target_index_zero_based']}。\n",mdtab(['精确候选（JSON保留空格）','token IDs','长度','逐token logP','总logP'],[[json.dumps(c['text']),c['candidate_token_ids'],c['token_count'],c['token_logprobs'],f(c['total_logprob'],9)] for c in b['candidates']]),f"差S_cat−S_dog={b['delta_cat_minus_dog']:.9f}；首选{b['choice']}；正确标签={b['gold'] or '不定义'}；正确性={b['correct'] if b['gold'] else '不评分'}。P的cat/dog标签为未知，非否定。\n"]
(C/'data_casebook_cn.md').write_text('\n'.join(data))

active=rows(R/'results/all_active_members.jsonl')
for site in SITES:
 dst=C/site;dst.mkdir(exist_ok=True);vals=readcsv(R/f'results/{site}/candidate_values.csv');h=readcsv(R/f'results/{site}/H2_old_new_pairs.csv');trans=readcsv(R/f'results/{site}/support_transitions.csv')
 case=[f'# {site}：全部固定候选原始值与相对值\n','列表和顺序均沿用S03。旧、新分别表示S03原前缀末尾space-a与S04中性Description:末尾冒号，正文不变。z为Top32后的激活，u=z×该字典decoder列L2范数；每个命名列表独立L2归一化，不用所有候选并集作分母。灰色/不可定义指整个列表零范数。某原子z=0但列表非零时，其q=0可定义。\n','[全部24条完整前文、token和行为分数](../data_casebook_cn.md)。下面保留每条的全部四个固定列表；完整精度、preactivation、是否进入Top32及两类范数见[逐候选CSV](../results/'+site+'/candidate_values.csv)。\n']
 for p in panel:
  case.append(f"## {p['id']} · {p['condition']} · {p['split']}\n\n```text\n{p['prefix']}\n```\n")
  for group in ['H1_common','H1_added_cat','H1_added_dog','H2']:
   rr=[v for v in vals if v['id']==p['id'] and v['group']==group];oo={v['atom']:v for v in rr if v['context']=='old'};nn=[v for v in rr if v['context']=='new'];case.append(f'### {group}\n')
   case.append(mdtab(['ID','decoder范数','旧/新z','旧/新u','旧/新q_raw','旧/新q_weighted','新Top32/正激活'],[[v['atom'],f(v['decoder_norm'],9),f(oo[v['atom']]['z'])+' / '+f(v['z']),f(oo[v['atom']]['u'])+' / '+f(v['u']),f(oo[v['atom']]['q_raw'])+' / '+f(v['q_raw']),f(oo[v['atom']]['q_weighted'])+' / '+f(v['q_weighted']),yes(v['Top32'])+' / '+yes(v['active'])] for v in nn]))
   if nn:case.append(f"旧/新列表原始L2={f(oo[nn[0]['atom']]['list_raw_L2'])}/{f(nn[0]['list_raw_L2'])}；加权L2={f(oo[nn[0]['atom']]['list_weighted_L2'])}/{f(nn[0]['list_weighted_L2'])}。\n")
 (dst/'candidate_casebook_cn.md').write_text('\n'.join(case))
 h2=[f'# {site}：每个固定H2候选的旧新配对与方向\n','正差表示猫大于狗，负差表示狗大于猫。方向零阈值绝对值≤1e-8。先按每对原始/归一化值阅读，再看状态；成员未双侧激活仍有数值，但不算固定成员方向保持。原子未激活与列表零范数分开。\n','计数串顺序固定为**同向/反向/成员未双侧激活/零范数/零差/无参照方向**；每串总和3。相对旧配对的参照是该家族旧差；相对冻结探索的参照是S03探索平均方向，两者可能相反。按预定优先顺序先列零范数，再列未激活，再判断方向。\n']
 for atom in selection[site]['H2']:
  rr=[v for v in h if v['atom']==str(atom)];h2 += [f'## #{atom}\n',mdtab(['家族','旧/新原始差Δz','旧/新原始方向','旧/新归一化差Δq','旧/新归一化方向','新猫/狗激活','新-旧配对状态','新-冻结探索状态'],[[v['family'],f(v['old_raw_delta'])+' / '+f(v['new_raw_delta']),arrow(v['old_raw_direction'])+' / '+arrow(v['new_raw_direction']),f(v['old_q_delta'])+' / '+f(v['new_q_delta']),arrow(v['old_q_direction'])+' / '+arrow(v['new_q_direction']),yes(v['new_cat_active'])+' / '+yes(v['new_dog_active']),v['q_weighted_old_pair_status'],v['q_weighted_S03_discovery_status']] for v in rr]),mdtab(['量','参照','探索3家族','保留3家族'],[[metric,ref]+[counts(next(c for c in ct if c['site']==site and c['atom']==str(atom) and c['metric']==metric and c['reference']==ref and c['split']==sp)) for sp in ['exploration','heldout_check']] for metric in ['raw','q_weighted'] for ref in ['old_pair','S03_discovery']])]
 h2.append(f'\n![旧新原始及归一化差](../figures/{site}_H2_old_new_differences.png)\n\n左旧右新，上为原始z差、下为同一固定6成员列表的加权归一化差，旧新同量共用颜色范围；红猫更大、蓝狗更大；星号表示该候选未双侧正激活，此数值不可算固定成员方向复现。黑线区分探索/检查。完整精度和两套原始范数见[72条配对总表](../results/all_H2_old_new_pairs.csv)。\n')
 (dst/'H2_comparison_cn.md').write_text('\n'.join(h2))
 h1=[f'# {site}：H1四条件与旧新支持变化\n','共同模式仍指P/猫/狗均正且min(u_P,u_cat,u_dog)>u_N；新增模式仍指P为0、相应细类为正。全部沿用S03固定候选，未从新结果补选。\n','P与N的新后缀完全相同，正文仍是animal与chair、an/An与a/A；两者以object指代。猫狗正文以animal指代并明确出现cat/dog。新面板只消除了原本条件依赖的后缀差异，不消除正文词面或复述解释。\n']
 for group in ['H1_common','H1_added_cat','H1_added_dog']:
  ids=selection[site]['H1_common'] if group=='H1_common' else selection[site]['H1_added']['cat' if group.endswith('cat') else 'dog'];h1.append('## '+group+'\n')
  h1.append(mdtab(['ID','旧探索/3','旧检查/3','新探索/3','新检查/3'],[[i]+[next(v['matches'] for v in pc if v['site']==site and v['group']==group and v['atom']==str(i) and v['context']==ctx and v['split']==sp) for ctx,sp in [('old','exploration'),('old','heldout_check'),('new','exploration'),('new','heldout_check')]] for i in ids]))
 h1.append('## 每个家族四条件的全部实际支持\n')
 for fi in range(6):
  ff=f'F{fi+1:02d}';h1.append('### '+ff+'\n')
  for cond in CONDS:
   oo=next(v for v in active if v['site']==site and v['context']=='old' and v['family']==ff and v['condition']==cond);nn=next(v for v in active if v['site']==site and v['context']=='new' and v['family']==ff and v['condition']==cond)
   h1 += [f"{cond}正文：{oo['text']}\n",f"旧活跃{len(oo['active_members'])}：`{oo['active_members']}`\n\n新活跃{len(nn['active_members'])}：`{nn['active_members']}`\n"]
  h1.append(mdtab(['上下文','转换','源/目标数','保留/源','新增/目标','消失/源','保留增强/减弱'],[[v['kind'],v['source']+'→'+v['destination'],v['source_count']+'/'+v['destination_count'],v['retained_fraction'],v['new_fraction'],v['lost_fraction'],v['retained_stronger']+'/'+v['retained_weaker']] for v in trans if v['family']==ff]))
 h1.append('全部原子的实际z/u与preactivation见[全活跃成员原始记录](../results/all_active_members.jsonl)；所有候选四条件的旧新数值见[逐候选表](candidate_casebook_cn.md)。每条仍为Top32，换入换出数相同由预算决定，不是“独立新语义”的证据。\n')
 (dst/'H1_comparison_cn.md').write_text('\n'.join(h1))

# Explicitly named atoms: report every family and both old/new texts, no favorable-case filtering.
focus=['# Attention字典 #14602 与 #3516：全部六组旧新文本和数值\n','这两个ID仅指ATTN_SAE，不能对应MLPIN同号原子。两者都在S03冻结H2列表。每对的归一化分母始终是原固定6成员列表，不是单原子或按激活重选。\n']
vv=readcsv(R/'results/ATTN_SAE/candidate_values.csv');hh=readcsv(R/'results/ATTN_SAE/H2_old_new_pairs.csv')
for atom in [14602,3516]:
 focus.append(f'## #{atom}\n')
 for fi in range(6):
  ff=f'F{fi+1:02d}';focus.append(f'### {ff} · '+('探索' if fi<3 else '保留检查')+'\n')
  for cond in ['cat','dog']:
   p=next(p for p in panel if p['family']==ff and p['condition']==cond);focus += [f'**{cond}旧前文：**\n\n```text\n'+p['old_prefix']+'\n```\n',f'**{cond}新前文：**\n\n```text\n'+p['prefix']+'\n```\n',f"旧位置{p['old_target_index_zero_based']}，token ` a` ID264；新位置{p['target_index_zero_based']}，token `:` ID25。\n"]
  rr=[v for v in vv if v['group']=='H2' and v['atom']==str(atom) and v['family']==ff and v['condition'] in ['cat','dog']];focus.append(mdtab(['上下文','条件','Top32/正激活','z','decoder范数','u','q_raw','q_weighted','列表加权L2','preactivation'],[[v['context'],v['condition'],yes(v['Top32'])+'/'+yes(v['active'])]+[f(v[k],9) for k in ['z','decoder_norm','u','q_raw','q_weighted','list_weighted_L2','preactivation']] for v in rr]))
  h=next(v for v in hh if v['atom']==str(atom) and v['family']==ff);focus.append(f"原始猫减狗旧/新={f(h['old_raw_delta'],9)}/{f(h['new_raw_delta'],9)}；归一化猫减狗旧/新={f(h['old_q_delta'],9)}/{f(h['new_q_delta'],9)}。相对本家族旧方向：{h['q_weighted_old_pair_status']}；相对S03冻结探索方向：{h['q_weighted_S03_discovery_status']}。\n")
focus.append('## 必须区分的事实\n\n#14602的新猫狗两侧全部为0，属于成员未激活；原H2列表仍有其他正成员，列表范数不为0，所以该原子的q=0是可定义的0，并非零范数。#3516仅F03/F05双侧激活，新归一化差均负、旧配对差均正，因此相对旧配对反向；旧探索平均方向为负，故相对冻结平均方向同向。F01/F04仅狗侧激活，F02/F06两侧均不激活，均不能当作固定共同成员的方向复现。\n')
(C/'focused_14602_3516_cn.md').write_text('\n'.join(focus))

bs=summary['behavior'];pair=readcsv(R/'results/behavior_pairs.csv')
overview=[]
for site in SITES:
 for sp in ['exploration','heldout_check']:
  rr=[v for v in ct if v['site']==site and v['split']==sp and v['metric']=='q_weighted' and v['reference']=='old_pair'];overview.append([site,'探索' if sp=='exploration' else '保留',*[sum(int(x[k]) for x in rr) for k in ['same','opposite','member_inactive','zero_norm','zero_difference']]])
cn=f'''# S04：统一中性后缀后的行为与固定候选检查

**原模型猫6/6、狗6/6，6/6组随类别切换。原S03固定候选的响应对完整后缀语境敏感，多个成员不再进入Top32。** Attention #14602在12条猫狗前文均未激活；#3516只在F03/F05双侧激活，这两组相对各自旧归一化方向均反向。旧结果和候选原件保留，不重筛、不改H1/H2。

本次按三条路径阅读：①原生行为仍能区分明确猫狗；②两套SAE坐标中，旧成员及相对比例的保持范围明显收窄；③本轮没有干预或功能检验，编码、token、旧值重放与计数核验通过。科学接受和下一步决定等待共同审阅。

## 1. 目的

统一四条件的后缀，检查原S03响应模式在另一固定续写语境下是否保持，并确认原模型行为是否仍随明确类别变化。H1的额外成员信息、H2的身份/总幅值控制后额外信息仍是原命题，本步只检查固定候选的语境稳定性。

## 2. 假设与竞争解释

若原候选响应与这批正文的细类关联能跨后缀保持，应在新后缀的对应位置仍能观察到其激活和比例方向。反例包括成员消失、方向反转或零差。这是较弱检查，不等于证实或推翻原H1/H2功能命题。

原模型、两套SAE、24条正文、标签、6家族与候选顺序都不变。旧后缀“The animal is a”或“The object is a”变为统一的`Description:`，同时改变了完整任务框架、取样token和绝对位置。因而不能把旧新差异单独归因于animal、冒号或某一个词，也不能把SAE变化当作干预后模型仍正确的因果结果。

## 3. 实验

新后缀精确为换行+`Description:`，末尾无空格。24条均取最后的`:`，ID25；旧为` a`，ID264；同家族四条件新位置一致。正文全部是完整描述句，此标签式后缀可自然接在P、猫、狗和椅子后。ATTN为block27 o_proj输出、残差相加前，MLPIN为实际MLP输入、残差相加与post_attention_layernorm后；各用原ReLU-Top32规则，不额外归一化输入或减decoder偏置，不是MLP输入输出的因果对照。

每个原命名列表保持原坐标和长度：原始z，自己的decoder列范数d，加权u=z×d，以及z、u分别按列表L2归一化。零范数不可定义；不随成员消失重选列表。逐值见[全部候选旧新表](results/ATTN_SAE/candidate_values.csv)和[MLPIN表](results/MLPIN_SAE/candidate_values.csv)。

原生评分使用同一新前缀与完整候选` cat.`（[8251,13]）、` dog.`（[5562,13]），均2 token。总分含词与句号的条件自然对数概率，不校正先验/长度，不搜prompt。P只知animal，猫狗未知；N是chair，猫狗均不适用，二者只报偏好。

## 4. 分析

### 原模型：明确猫狗仍全部正确

'''+mdtab(['家族','猫前文 S_cat / S_dog','猫前文差/首选','狗前文 S_cat / S_dog','狗前文差/首选'],[[p['family'],f(bb[f'S04_{p["family"]}_cat']['candidates'][0]['total_logprob'])+' / '+f(bb[f'S04_{p["family"]}_cat']['candidates'][1]['total_logprob']),f(p['new_cat_input_delta'])+' / '+p['new_cat_choice'],f(bb[f'S04_{p["family"]}_dog']['candidates'][0]['total_logprob'])+' / '+f(bb[f'S04_{p["family"]}_dog']['candidates'][1]['total_logprob']),f(p['new_dog_input_delta'])+' / '+p['new_dog_choice']] for p in pair])+f'''
猫{bs['cat_correct']}/6、狗{bs['dog_correct']}/6，配对均切换且两条都对{bs['both_correct_pairs']}/6。明确猫狗没有错误例，不构造不存在的错误。P偏好猫{bs['P_preferences']['cat']}、狗{bs['P_preferences']['dog']}；N偏好猫{bs['N_preferences']['cat']}、狗{bs['N_preferences']['dog']}，它们不计入正确数。特别是椅子也被迫从猫狗选一个，说明本测试是二候选相对偏好，不是完整对象识别。

S02也是12/12，但使用另一前缀；这里只并列保留为不同语境历史参照，不把两次同样正确解释成某一个词无作用。完整24条前文、token、全部分数及P/N偏好见[数据与行为逐条记录](data_casebook_cn.md)。

### H2：方向、未激活与零范数分开

下面是**相对同家族旧归一化方向**的计数，每行18个“候选×家族”观察（6候选×3家族），不是18个独立样本。先排零范数与成员未双侧激活，再分同向、反向、零差。

'''+mdtab(['接口','分组','同向','反向','成员未双侧激活','零范数','零差'],overview)+'''
本轮两套H2列表均无零范数；但大量旧候选未双侧激活。新H2列表支持相同均4/6对，列表全部6成员均双侧激活均0/6对；全字典支持完全相同仍均0/6对。两侧支持相同也可能是同时失去某些成员，不能等同于原列表全员保持。

每个候选相对**旧配对**与相对**S03冻结探索方向**的探索/保留计数，以及原始差、归一化差和方向，分别见[Attention完整对照](ATTN_SAE/H2_comparison_cn.md)／[MLPIN完整对照](MLPIN_SAE/H2_comparison_cn.md)，原始计数见[固定口径CSV](results/H2_direction_counts.csv)。两种参照不混用。

'''
for site in SITES:
 cn+=f'#### {site}：相对S03冻结探索方向\n\n'+mdtab(['ID','探索：同/反/未激活/零范数/零差/无参照','保留：同/反/未激活/零范数/零差/无参照'],[[i]+[counts(next(v for v in ct if v['site']==site and v['atom']==str(i) and v['split']==sp and v['metric']=='q_weighted' and v['reference']=='S03_discovery')) for sp in ['exploration','heldout_check']] for i in selection[site]['H2']])+f'\n![{site}旧新方向](figures/{site}_H2_old_new_differences.png)\n\n旧新同一量使用同一颜色范围，红猫较强、蓝狗较强；星号是未双侧激活，不算固定成员方向复现；黑线区分探索与检查。所有反向、消失及零差都保留。\n\n'
cn+='''### 指定案例：#14602、#3516

这两个编号仅属于Attention字典。[指定案例全文与全部数值](focused_14602_3516_cn.md)保留6组完整旧新猫狗前文、z/u/q、Top32、preactivation和范数。

- **#14602：**旧猫减狗归一化差在六组均负；新猫狗的z/u/q全为0，未进入Top32，因列表其他成员仍正，q=0可定义。这是候选未激活，不是列表零范数，也不能叫“方向继续偏狗”。
- **#3516：**F03旧Δq=+0.002868399，新Δq=−0.041341155；F05旧Δq=+0.013762367，新Δq=−0.078677683。两组均双侧激活，故相对旧配对反向；S03冻结探索均值方向原本为负，故又与该平均方向同向。F01/F04仅狗侧激活，F02/F06两侧均不激活。未将这些失败排除后再宣称6/6稳定。
- **归一化退化的例子：**Attention #23899在F02新猫z=29.157364、狗z=29.162550，仍有原始差；但固定6成员只剩它在两侧激活，因此两边归一化均为1，差为0。列表归一化会丢掉这个幅值差，不等于模型失去类别区分。

### H1：共同模式与支持换入换出

旧共同候选在新保留家族的完整模式覆盖：

'''
for site in SITES:
 cn+=f'**{site}**\n\n'+mdtab(['ID','旧检查/3','新检查/3'],[[i]+[next(v['matches'] for v in pc if v['site']==site and v['group']=='H1_common' and v['atom']==str(i) and v['split']=='heldout_check' and v['context']==ctx) for ctx in ['old','new']] for i in selection[site]['H1_common']])+f'\n![{site}新前缀固定候选](figures/{site}_fixed_candidates.png)\n\n左为新原始z，右为该命名列表加权L2归一化值；上H1共同、下H2。红线分开探索/检查，灰为不可定义。加权原始u、decoder范数、其余H1新增列表与零范数均在逐候选表中，没有从图上删去失败后补选成员。\n\n[该接口全部P/猫/狗/N支持、旧新变化与候选覆盖]({site}/H1_comparison_cn.md) · [所有候选逐样本原始/相对数值]({site}/candidate_casebook_cn.md)。\n\n'
cn+='''P与N现在后缀完全相同，正文仍有animal/chair与冠词an/a差异。两个正文都用object指代，猫狗正文仍用animal并明确写cat/dog；词面与复述解释未排除。每条仍Top32，旧→新和P→细类的换入/换出只能说明原字典支持变化，不对应独立新语义。共同模式有消失也有保持，例如MLPIN #17366新检查3/3；本轮未据此改候选。

## 5. 结论与认识更新

**统一后缀后知道了什么：**明确猫狗的二候选偏好仍随正文改变，而S03挑出的许多末尾成员与比例模式不跨这次完整后缀变更保持。因此，原行为区分与某份固定SAE候选列表的语境稳定性要分开检验。现在多确定了这些候选可观察的适用语境边界，不能把旧列表直接当作普遍的粗细概念组成。

**H1：**观察到具体共同/新增模式随后缀保持或消失，只涉及当前字典支持；新增提供额外细类信息仍未验证。后缀统一消除了新P/N之间的尾部类别词差异，正文、目标token和语境仍限制解释。

**H2：**仍有保持及反向，但多数“未复现”首先卡在固定候选成员未激活，并非本轮H2列表零范数或原模型行为失败。Attention #14602全消失、#3516仅2/6配对可作双侧比例方向检查；两套列表全员双侧激活均0/6，故不能用本轮描述完成原H2的身份/总幅值控制及额外信息命题。部分H1新增列表确有零范数，表中如实记为不可定义。

六个已使用的短英文家族、明确的cat/dog词、单一chair非动物对照和强制二候选仍限制结论。词面复制、句式/任务框架、目标token差异及Top32竞争均未排除；没有做因果干预，不能推断这些原子是否被模型使用或可被删除。训练、probe、SVD、新类别、提示搜索及后续实验均未运行。原假设不改，下一步等待共同审阅。

[完整24条](data_casebook_cn.md) · [指定两原子全文](focused_14602_3516_cn.md) · [中文Detailed与质量检查](detailed_cn.md) · [冻结协议](protocol_cn.md) · [全部原始行为分数](results/behavior_raw.jsonl) · [原始表征数组](cache/new.npz)
'''
(C/'summary_cn.md').write_text(cn)
en=f'''# S04: neutral suffix and fixed S03 candidates

Native behavior remains12/12correct (cat6/6,dog6/6), with6/6correct paired switches. Many original S03 SAE candidates cease to enter Top32 under the new suffix. These are different observations: behavioral discrimination of explicit words persists, while this fixed coordinate panel is context dependent. Scientific acceptance and next decision await joint review.

Purpose/hypotheses: check suffix robustness of existing H1/H2 response patterns, not incremental predictive information or causal model use. Preserve original hypotheses and exact candidates. Same frozen official Qwen3-0.6BBase/tokenizer and native attention-output/MLP-input SAEs. No training,classifier,screening,SVD,intervention or prompt search.

All24S03body strings and labels are unchanged. Replace only the entire suffix with exact newline+'Description:'; observe final colon,token25,without any answer tokens. Old target was space-a,token264. Same family positions match across four conditions, but the entire framing,target token and absolute index change relative to S03. It is not a single-word causal test. P/N bodies still differ in animal/chair and article; explicit cat/dog copying remains a competitor.

Score complete ' cat.' [8251,13] and ' dog.' [5562,13],2tokens each, conditional natural-log sequence sum including period. P preferences cat/dog={bs['P_preferences']['cat']}/{bs['P_preferences']['dog']}; N preferences={bs['N_preferences']['cat']}/{bs['N_preferences']['dog']},without correctness labels. No cat/dog errors exist. S02 is historical different-prefix context, not a word-isolation comparison.

Raw z, own decoder norm d,weighted u=z*d,original Top32 selection/positive support,and q_raw/q_weighted normalized within each exact named S03 list are retained side by side. Zero norm is undefined, not filled with zero. Dictionary IDs are separate. ATTN hook: block27o_proj before residual add; MLPIN hook: actual block27mlp input after residual add and post_attention_layernorm. These are not an MLP input/output causal pair.

Weighted-relative directions compared with the same-family old direction, counts per18atom-family observations (6candidates x3families, not18independent replicates):

'''+mdtab(['site','split','same','opposite','inactive','zero_norm','zero_difference'],overview)+'''
Exact per-atom old/new raw and normalized differences, all failures, and comparison against original frozen S03 discovery directions are in the bilingual numeric tables and Chinese casebooks. The two references are not interchangeable. At both sites, new fixed-list support equality is4/6pairs, all six members bilateral positive0/6, full-dictionary support equality0/6. Neither H2 list has a zero-norm row; membership loss is the primary observed coverage failure.

ATTN #14602 is inactive for both cat/dog in all6pairs, although other H2 members keep list norm positive: its defined q=0is not a zero-norm observation. #3516 remains bilateral positive only inF03/F05: old->new weighted q differences +.002868399->-.041341155 and +.013762367->-.078677683. These reverse each old pair, yet match the original negative discovery-average direction. Other pairs are unilateral or inactive, not fixed-member replication. All six old/new full text pairs and exact values are retained in focused_14602_3516_cn.md.

H1 common patterns partly vanish and partly remain. For example, ATTΝ #9495 old check3/3,new0/3; MLPIN #17366 old2/3,new3/3. No candidate was reselected. All four conditions' full supports and transitions, including P/N and old/new, are reported. Top32 turnover is not independent new semantics. Some fixed H1-added lists have zero norms and are explicitly undefined.

Recognition update: native explicit-word discrimination and robustness of a particular SAE coordinate list must be assessed separately. S03's list cannot be treated as a universal coarse/fine concept decomposition across this full framing change. Original H1/H2 extra-information and functional claims remain untested. Six reused short English families, explicit words, one chair control,forced choice and dictionary/Top32 effects limit scope. STOP_WAIT_FOR_JOINT_REVIEW; no automatic next experiment.

[24full prefixes and behavior](data_casebook_cn.md) · [ATTN H2](ATTN_SAE/H2_comparison_cn.md) · [MLPIN H2](MLPIN_SAE/H2_comparison_cn.md) · [Detailed](detailed.md) · [verification](evidence/verification.json)
'''
(C/'summary.md').write_text(en.replace('ATTΝ','ATTN'))
detail=f'''# S04 执行与证据口径

本轮24条捕获、24条双候选评分完成，模型与SAE全冻结，无训练/筛选/干预。运行耗时{run['elapsed_seconds']:.2f}秒，CPU2线程，FP32；离线统计和序列求和FP64。新旧结果独立目录，原S02/S03共{ver['old_files_unchanged']}个文件哈希不变。[Summary](summary_cn.md)保留目的、假设、分析和有界结论；[协议](protocol_cn.md)及[frozen_plan](frozen_plan.json)在新响应前固定。

## 取样和原生编码

正文/标签/家族完全沿用S03；新后缀一致，末尾冒号ID25，同家族绝对位置一致；旧末尾space-a ID264，不能当同一token下的单词消融。捕获仅包括24条完整可见前缀，没有任何候选答案；随后移除全部hook，才做原生评分。ATTN和MLPIN分别使用原loader，编码与线性+bias→ReLU→Top32实现完全一致；保留preactivation和32/33门限，激活为最终z>0，Top32选入索引另存。原生无hook对照最大差0；候选重复lane最大差{run['max_duplicate_lane_difference']}。这些是实现检查，不是科学确认。

## 量与分母

z为最终稀疏激活，d为同字典decoder列L2范数，u=z*d。q_raw/q_weighted各在原命名列表内归一化。固定位置保留为0，不按新激活重选；整个列表范数0才不可定义。H1-added旧归一化是本轮从原数组新算的派生值，不冒充S03已报告量。所有列表范数、preactivation、Top32/正值和完整精度见candidate_values。方向零阈值1e-8与旧口径一致。

H2两种参照分别报告：同家族旧差；S03原探索方向。归一化方向直接沿用原selection，原始差探索参照在新响应前仅用旧探索均值固定。计数每候选每split分母3，优先zero_norm→member_inactive→no_reference→same/opposite/zero_difference。原子未激活的q数值仍保存但不算共同成员比例保持。每串和为3；新未双侧激活与零范数的非互斥原始标记也保留。数据独立单位是家族，无显著性或总体结论。

## 原始行为

精确候选和拼接完整ID在data/panel.jsonl，token级logP在results/behavior_raw.jsonl。分数为含句号的完整序列自然对数概率，最大和首选，无长度/先验校正。每候选2token，等长排除本轮长度数量差，但不排除词/标点先验。cat/dog各6条准确率，P/N只偏好，P并非猫狗负例。旧S02使用另一前缀，仅作历史并列。

## 核验与范围

{ver['candidate_token_sums']}项候选求和、{ver['candidate_value_replays']}个候选值、{ver['H2_pair_replays']}条H2旧新差、{ver['direction_count_rows']}条方向计数、{ver['support_transition_replays']}条支持转换独立复核；旧H2的q与S03原CSV精确重放。所有正文0改动、原候选0重筛、212旧文件保持；最终以verification中实际计数为准。

'''
for site in SITES:
 err=np.array(summary['sites'][site]['new_reconstruction_relative_L2']);zv=ver['sites'][site];detail+=f'### {site}\n\n新hook重建相对L2误差||h-reconstruction||/||h||的最小/中位/最大={err.min():.6f}/{np.median(err):.6f}/{err.max():.6f}；不作跨接口排名。第32与33正值最小差{zv["min_Top32_margin"]:.9f}，精确边界并列{zv["exact_Top32_boundary_ties"]}。\n\n新24条各固定列表零范数数：`{zv["zero_norm_by_list"]}`。这些列表的不可定义情况都保留在表中，尤其H1新增列表，不能用H2无零范数替代全列表报告。\n\n'
detail+='''## 文件与覆盖

- data：24条旧新前缀/原始标签/所有token与候选、S03原面板/selection、S02原行为分数；全部byte lineage保留。
- cache/new.npz：样本ID，各site__h/z/pre/topk_indices/decoder_norm/cutoff32/33/reconstruction_relative_L2；不含答案位置。
- results：24原生分数及48候选序列、逐家族行为；两SAE全部旧新候选值、72H2配对、96计数、H1四条件模式与192支持转换；全活跃成员原始值。
- 4幅图：每字典一幅固定列表原始/相对热图、一幅旧新H2差值图，来源均是冻结列表及cache，不展示新筛选结果。
- code/evidence：实际脚本、冻结、捕获、核验和输入/输出资产记录；模型/SAE checkpoint不复制。

| 需求 | 状态 | 边界 |
|---|---|---|
| 24正文保持、中性后缀与token | DONE_VALID | 全部完整记录 |
| 两冻结SAE、原候选及全部量 | DONE_VALID | 不跨字典对齐 |
| 原生猫狗评分和P/N偏好 | DONE_EXPLORATORY | 强制二候选 |
| H2旧新方向、指定两原子与失败 | DONE_EXPLORATORY | 成员未激活单列 |
| H1支持变化与正文竞争解释 | DONE_EXPLORATORY | 未测额外信息 |
| 训练/重筛/SVD/干预/新类别 | NOT_RUN_BY_SCOPE | 用户要求止步 |
| 科学接受/下一步 | Unknown | 等待共同审阅 |

无研究假设或Anchor科学状态修改，无commit/push。原协议科学规则未改。小样本、明确词面、整体任务框架与取样token变化、Top32竞争和重建近似仍限制解释。
'''
(C/'detailed_cn.md').write_text(detail)
(C/'detailed.md').write_text(f'''# S04 execution record

Completed24prefix captures and24complete-candidate comparisons in{run['elapsed_seconds']:.2f}seconds on CPU,FP32,two threads,physical4x192. All model/SAE parameters frozen. Native encoding equivalence and hook no-op pass; no answer tokens captured and no hooks during native scoring. No training,selection,SVD or intervention.

All24bodies/labels unchanged; original S02/S03{ver['old_files_unchanged']}files hash-unchanged.48token sums,2304candidate values,72H2pairs,96count partitions,192support transitions independently replay. Old H2 normalized differences match original S03 tables. Undefined norms and inactivated coordinates are distinguished. Exact provenance,norm-zero counts,per-site reconstruction error,data schema and task coverage are in[the full execution ledger](detailed_cn.md),[run receipt](evidence/run_complete.json),[verification](evidence/verification.json),[frozen plan](frozen_plan.json),and[protocol](protocol.md).

Only context robustness and native forced-choice behavior are observed; original incremental-information and causal claims remain untested. STOP_WAIT_FOR_JOINT_REVIEW.
''')
(C/'README.md').write_text('''# S04 · Neutral suffix / native behavior / fixed S03 candidates

[中文小结](summary_cn.md) · [English Summary](summary.md) · [24条全文与完整分数](data_casebook_cn.md) · [#14602/#3516全部文本与数值](focused_14602_3516_cn.md) · [执行与口径](detailed_cn.md) · [冻结协议](protocol_cn.md)

- Attention：[H2旧新方向与计数](ATTN_SAE/H2_comparison_cn.md) · [H1四条件支持变化](ATTN_SAE/H1_comparison_cn.md) · [全部固定候选](ATTN_SAE/candidate_casebook_cn.md)
- MLP输入：[H2旧新方向与计数](MLPIN_SAE/H2_comparison_cn.md) · [H1四条件支持变化](MLPIN_SAE/H1_comparison_cn.md) · [全部固定候选](MLPIN_SAE/candidate_casebook_cn.md)

Only the requested neutral-suffix24-row step is complete. Exact S03 candidates reused; no feature selection,training,classifier,SVD,intervention or follow-up. Original S02/S03 files unchanged. Generated data/code/array/table/figure copies keep execution ownership; payload_manifest records source hashes. Scientific acceptance and next decision remain pending joint review.
''')
print('S04_REPORTS_WRITTEN',flush=True)
