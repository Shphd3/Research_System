from common import *
import numpy as np,itertools
def readcsv(p):return list(csv.DictReader(open(p)))
def tab(h,rr):return '\n'.join(['| '+' | '.join(h)+' |','| '+' | '.join(['---']*len(h))+' |']+['| '+' | '.join(str(v) for v in row)+' |' for row in rr])+'\n'
def f(v,n=6):return '不可定义' if v is None or v=='' else f'{float(v):.{n}f}'
panel=rows(R/'data/panel.jsonl');D=np.load(R/'data/S04_frozen_activations.npz');mat=rows(R/'results/matrix_manifest.jsonl');geom=rows(R/'results/geometry_comparisons.jsonl');top=readcsv(R/'results/top_loading_members.csv');spectrum=readcsv(R/'results/spectrum_and_gaps.csv');pair=readcsv(R/'results/paired_differences_summary.csv');parts=readcsv(R/'results/difference_decomposition.csv');means=readcsv(R/'results/mean_difference_summary.csv');boot=readcsv(R/'results/bootstrap_summary.csv');variance=readcsv(R/'results/SVD_between_within_family.csv');counters=rows(R/'results/counterexamples.jsonl');member=readcsv(R/'results/selected_member_all24_values.csv');verification=json.load(open(R/'evidence/verification.json'));H2=json.load(open(R/'data/S03_frozen_selection.json'))['sites'];C.mkdir(exist_ok=True)
aggregates=[];sensitivity=[];means_sparse=[]
for site,scale,sp in itertools.product(SITES,SCALES,['exploration','heldout_check']):
 rr=[r for r in parts if r['site']==site and r['scale']==scale and r['split']==sp];total=sum(float(x['component_squared_norm']) for x in rr)
 for part in PARTS:aggregates.append(dict(site=site,scale=scale,split=sp,part=part,pooled_squared_norm_share=sum(float(x['component_squared_norm']) for x in rr if x['part']==part)/total,pairs=6,definition='sum component energies over 3families x cat/dog divided by sum full delta energies;descriptive,not causal importance'))
for site in SITES:
 a=next(v for v in geom if v['site']==site and v['scale']=='raw_z');b=next(v for v in geom if v['site']==site and v['scale']=='decoder_weighted')
 for metric in ['PC1_absolute_cosine','top2_normalized_overlap','exploration_mean_delta_cosine','exploration_mean_delta_cat_L2','exploration_mean_delta_dog_L2']:sensitivity.append(dict(site=site,metric=metric,raw=a[metric],weighted=b[metric],weighted_minus_raw=b[metric]-a[metric]))
for m in mat:
 a=np.load(R/m['cache'])
 for i in np.flatnonzero(a['mean']):means_sparse.append(dict(site=m['site'],scale=m['scale'],group=m['group'],atom=int(i),column_mean=float(a['mean'][i])))
table(R/'results/pooled_component_energy_shares.csv',aggregates);table(R/'results/scale_sensitivity.csv',sensitivity);table(R/'results/exploration_means_nonzero_columns.csv',means_sparse)

data=['# S05 输入：24条真实前文、取样位置与Top32\n','本轮只读取已完成S04缓存。每条后缀相同、目标为冒号ID25；未重新前向，也未使用S03旧后缀。完整30000维预激活和原始稀疏值见[data/S04_frozen_activations.npz](data/S04_frozen_activations.npz)。下面列出每条所有实际活跃ID及其z/pre；未入选但pre为正的情况在成员表和完整预激活中保留。\n']
for fi in range(6):
 data.append(f'## F{fi+1:02d} · '+('exploration' if fi<3 else 'heldout_check')+'\n')
 for p in panel[fi*4:fi*4+4]:
  j=panel.index(p);data += [f"### {p['condition']} · {p['labels']}\n",'```text\n'+p['prefix']+'\n```\n',f"完整token IDs：`{p['token_ids']}`；目标`:` ID25，0起位置{p['target_index_zero_based']}。\n"]
  for site in SITES:
   ids=D[site+'__topk_indices'][j];ids=sorted(int(i) for i in ids);data.append(f"**{site}** Top32：`{ids}`。\n\n实际值（ID:z/pre）："+', '.join(f"#{i}:{D[site+'__z'][j,i]:.6f}/{D[site+'__pre'][j,i]:.6f}" for i in ids)+'。\n')
(C/'data_casebook_cn.md').write_text('\n'.join(data))

for site in SITES:
 out=C/site;out.mkdir(exist_ok=True);z=D[site+'__z'].astype(float);pre=D[site+'__pre'].astype(float);dn=D[site+'__decoder_norm'].astype(float)
 # Every selected direction is explained through the same full four-condition text families.
 doc=[f'# {site}：SVD主要成员、符号与完整文本\n','每方向前5个成员只按探索绝对系数选择。最大绝对系数设正，整组方向/投影同步翻转；不同方向间的单个正负号不能直接解释为语义相反。系数大不等于因果重要。所有ID仅属于本字典。每行原始z、实际Top32支持、预激活与decoder范数均可核对；weighted尺度的矩阵输入是z×d，以下仍同时展示原始z。\n']
 for scale,g,k in itertools.product(SCALES,['AC','AD'],[1,2]):
  rr=[r for r in top if r['site']==site and r['scale']==scale and r['group']==g and int(r['direction'])==k];ids=[int(r['atom']) for r in rr];doc.append(f'## {scale} · {g} · PC{k}\n');doc.append(tab(['探索系数排名','ID','有符号系数','decoder范数'],[[r['loading_rank'],r['atom'],f(r['coefficient'],9),f(dn[int(r['atom'])],9)] for r in rr]))
  for fi in range(6):
   doc.append(f'### F{fi+1:02d} · '+('探索' if fi<3 else '保留检查')+'\n')
   for p in panel[fi*4:fi*4+4]:doc.append(f"{p['condition']}：\n\n```text\n{p['prefix']}\n```\n")
   doc.append(tab(['ID','P z/u；T；pre','cat z/u；T；pre','dog z/u；T；pre','N z/u；T；pre'],[[i]+[f'{z[fi*4+j,i]:.6f}/{z[fi*4+j,i]*dn[i]:.6f}; {"T" if z[fi*4+j,i]>0 else "F"}; {pre[fi*4+j,i]:.6f}' for j in range(4)] for i in ids]))
 (out/'directions_and_members_cn.md').write_text('\n'.join(doc))
 fixed=[f'# {site}：原S03 H2成员额外记录\n','本列表不按本轮结果筛选，不预设SVD排名。正激活/Top32和预激活分开；所有实际文本见[完整输入](../data_casebook_cn.md)。\n']
 for i in H2[site]['H2']:
  fixed.append(f'## #{i}\n');fixed.append(tab(['尺度','AC PC1系数','AC PC2系数','AD PC1系数','AD PC2系数'],[[scale]+[f(np.load(R/f'cache/{site}/{scale}/{g}.npz')['components'][k,i],9) for g in ['AC','AD'] for k in [0,1]] for scale in SCALES]))
  fixed.append(tab(['家族','条件','z','decoder范数','u','Top32/正激活','预激活'],[[p['family'],p['condition'],f(z[j,i],9),f(dn[i],9),f(z[j,i]*dn[i],9),'是' if z[j,i]>0 else '否',f(pre[j,i],9)] for j,p in enumerate(panel)]))
 if site=='ATTN_SAE':fixed.append('#14602在这24条最终z均为0，仍如实保留其预激活；对应非零SVD方向的该坐标系数为0，不能据此推断模型没有猫狗信息。#3516进入原始AC第二方向前5，但其系数和AD第二方向的符号取决于整组轴的定向与旋转，不证明猫狗语义相反。\n')
 (out/'fixed_H2_cn.md').write_text('\n'.join(fixed))

detail=['# S05 详细记录：总体轴、配对差与真实成员\n','[中文小结](summary_cn.md)先读。[冻结协议](protocol_cn.md)与[frozen_plan](frozen_plan.json)拥有执行规则；科学接受和下一步等待共同审阅。全部输入来自已完成S04的Description:冒号位置，没有模型前向或旧后缀替换。\n','## 样本矩阵、均值与谱\n','每个家族行相邻，P和对应细类一一配对。AC与AD的P逐行完全相同。原始X/中心X均6×30000，均值30000维、奇异值6个、右方向6×30000均在对应NPZ保存；最后数值零方向不解释。列均值非零项另有CSV以供人工核对，未列项为0。\n']
detail.append(tab(['接口','尺度','组','行ID（顺序）','维度','数值秩','均值/矩阵文件'],[[m['site'],m['scale'],m['group'],'; '.join(m['row_ids']),'6×30000',m['rank'],f"[NPZ]({m['cache']})"] for m in mat]))
detail.append('中心化分别减AC/AD自己的探索均值，持出投影仍用对应均值；不能把不同组坐标的原点或轴直接当作同一坐标。差向量投影不用再减均值，等于子类坐标减P坐标。\n')
detail.append(tab(['接口','尺度','组','序号','奇异值','方差比例','到下一值间隔','相对间隔','小间隔提醒','非零秩内'],[[r[k] if k not in ['singular_value','variance_fraction','gap_to_next','relative_gap_to_next'] else f(r[k],9) for k in ['site','scale','group','direction','singular_value','variance_fraction','gap_to_next','relative_gap_to_next','small_gap_warning','numerically_nonzero']] for r in spectrum]))
detail += ['## 固定轴上的每条坐标、类内和家族内变化\n','[所有24条在AC/AD前二维的坐标](results/projections_all24.csv)，包含非拟合条件及椅子；[类内中心与离散](results/class_spread_frozen_coordinates.csv)是在冻结轴中的描述统计，不是重拟合或分类。家族内变化在[配对投影](results/paired_projections_both_bases.csv)，同时投到两组轴；完整30000维差及分项保存在每site/scale的paired_differences.npz。\n']
detail.append(tab(['接口','尺度','家族','猫差长度','狗差长度','猫差/狗差有向余弦','猫差/探索均值余弦','狗差/探索均值余弦'],[[v['site'],v['scale'],v['family']]+[f(v[k]) for k in ['cat_delta_L2','dog_delta_L2','cat_dog_delta_signed_cosine','cat_to_exploration_mean_cosine','dog_to_exploration_mean_cosine']] for v in pair]))
detail += ['## 共同强弱与Top32更替分开\n','逐家族共同正成员、换入、换出在坐标上互斥，差向量平方范数=三部分平方范数之和。份额是激活空间的几何量，不是因果重要性。逐原子原始P/细类值、pre及事件见[difference_member_events](results/difference_member_events.csv)。\n']
detail.append(tab(['接口','尺度','家族','细类','部分','成员数','分项L2','总差L2','平方范数份额','零端仍有正pre数'],[[v['site'],v['scale'],v['family'],v['fine'],v['part'],v['members'],f(v['component_L2']),f(v['total_difference_L2']),f(v['squared_norm_share']),v['zero_parent_pre_positive']+'/'+v['zero_fine_pre_positive']] for v in parts]))
detail.append('跨家族求均值后，同一原子可在不同家族属于不同部分，均值分项会重叠；不能把均值分项平方范数继续当互斥能量相加。下面9项把均值差点积按猫/狗三类分开，除以两条完整均值差范数积后，九项相加才等于整体有向余弦。\n')
cross=readcsv(R/'results/mean_difference_cross_parts.csv');detail.append(tab(['接口','尺度','猫分项','狗分项','点积','对整体均值差余弦的代数分项'],[[v['site'],v['scale'],v['cat_part'],v['dog_part'],f(v['dot_product']),f(v['contribution_to_total_mean_cosine'])] for v in cross]))
detail += ['## 稳定性与方向不唯一\n','27个有序bootstrap样本只来自3个探索家族，实际10个无序多重集；其中3个只含单一家族，秩1，二维子空间不可定义；18个含2家族，6个含3家族。27不是独立样本数，下面分位值不是置信区间。数值上余弦/重叠最大值可能因舍入高于1约1e−15，图文按1显示，原始值保留。\n']
detail.append(tab(['接口','尺度','量','有效/27','不可定义','最小','5%','中位','95%','最大'],[[v['site'],v['scale'],v['metric'],v['valid'],v['undefined']]+[f(v[k]) for k in ['min','q05','median','q95','max']] for v in boot]))
detail += ['## 预定反例：不满足同一PC1父子方向\n','反例来自运行前固定规则，只挑展示家族，不用检查结果选原子或重拟合。两套原始尺度都选到F05；其完整均值差方向仍有正夹角关联，但沿自身AC第一轴的分量与探索平均父子分量反号。一个投影分量反号不等于完整向量相反。\n']
for site in SITES:
 rec=next(c for c in counters if c['site']==site and c['scale']=='raw_z');detail.append(f"### {site} · {rec['family']}\n\n规则：{rec['rule']}；探索参考投影={f(rec.get('reference'))}，检查投影={f(rec['value'])}。\n")
 fi=int(rec['family'][1:])-1
 for p in panel[fi*4:fi*4+4]:detail.append(f"{p['condition']}：\n\n```text\n{p['prefix']}\n```\n")
 ids=[int(v['atom']) for v in top if v['site']==site and v['scale']=='raw_z' and v['group']=='AC' and v['direction']=='1'];zz=D[site+'__z'];pr=D[site+'__pre'];detail.append(tab(['AC PC1固定前5 ID','P z','cat z','dog z','N z','cat−P','P/cat预激活'],[[i]+[f(zz[fi*4+j,i]) for j in range(4)]+[f(zz[fi*4+1,i]-zz[fi*4,i]),f(pr[fi*4,i])+'/'+f(pr[fi*4+1,i])] for i in ids]))
detail += ['## 原始/加权尺度及数值质量\n',tab(['接口','量','原始','加权','加权−原始'],[[v['site'],v['metric'],f(v['raw'],9),f(v['weighted'],9),f(v['weighted_minus_raw'],12)] for v in sensitivity]),f"8个基础SVD与216个bootstrap SVD；{verification['projection_replays']}条投影、{verification['paired_difference_replays']}条完整差向量、{verification['member_value_replays']}个成员值核对。中心化/正交/重建/Gram谱及分解闭合误差见[verification](evidence/verification.json)：`{verification['max_errors']}`。S03/S04原件{verification['old_files_unchanged']}个哈希保持。没有新LM/SAE前向、学习参数、optimizer、probe、干预、decoder空间比较或后续实验。\n",'## 证据链与覆盖\n','| 项目 | 原始记录→计算→观察 | 状态/边界 |\n|---|---|---|\n| AC/AD总体方向 | matrix_manifest及各NPZ→探索SVD→绝对余弦/主角/重叠 | DONE_EXPLORATORY；总体变化 |\n| 父类到细类 | S04 z→逐家族fine−P/均值→有向余弦/长度/双轴投影 | DONE_EXPLORATORY；不等同总体轴 |\n| 强弱/支持更替 | 原始z/pre/Top32→三分项→逐对能量/均值交叉点积 | DONE_EXPLORATORY；无语义因果 |\n| 稳定性 | 3探索家族→27成组重采样→有效数/范围 | DONE_EXPLORATORY；不是置信区间 |\n| 成员与真实文本 | 只按探索系数选前5+原H2→全部24值/完整前文 | DONE_VALID；未按检查补选 |\n| 数据/均值/脚本/图/数值核验 | 来源哈希/冻结/闭合 | DONE_VALID |\n| 模型作用/一般概念规律 | 没有功能对照或独立大样本 | NOT_RUN/Unknown |\n\n科学接受和下一步决定等待共同审阅。\n']
(C/'detailed_cn.md').write_text('\n'.join(detail))

cn='''# S05：动物→猫与动物→狗的激活变化几何

**两组总体轴与父类到细类的配对差都呈正向关联，但它们是不同对象。第一轴主要反映家族中点间差异；保留家族只部分沿用探索方向，并存在分量反号。** 下面数值仅描述6个短文本家族，不构成一般语义规律。

先分三条路径阅读：①行为与条件：本轮沿用已完成S04的统一Description:缓存，原生猫狗12/12是前轮结果，没有新行为实验；②表征：分别比较两套SAE的总体SVD及配对差；③功能与质量：没有干预/训练，行对应、谱、分解与投影闭合核验通过，功能判断等待共同审阅。

## 1. 目的与假设

要区分“P/猫与P/狗的总体变化轴接近”和“猫−P与狗−P沿相近有方向变化”。前者是每组中心化样本的总体方差轴，正负任意；后者有父类到细类的明确方向，用有符号余弦。两者相近都只说明本面板和字典坐标里的几何关系，不能认定语义相同或feature因果重要。原H1/H2额外信息命题未改、未在此验证。

## 2. 实验

同一冻结Qwen3-0.6B Base与两套原生SAE产生的S04缓存：24条正文、统一Description:、末尾冒号ID25。Attention读取block27 o_proj残差相加前输出；MLP输入读取block27实际MLP输入，残差及post_attention_layernorm后。两字典各30000坐标，不对齐同号原子。只做缓存分析，没有新模型前向。

F01–03探索，F04–06检查。每个AC矩阵按P01/猫01/P02/猫02/P03/猫03排6行；AD换成对应狗，三个P完全相同。各组分别减自己的探索列均值，拟合前1/前2方向；检查均值/方向不重拟合。6×30000中心化矩阵数值秩均5，不能从它推断30000维概念总体结构。原始z为主，z×decoder列范数为尺度补充，两套完整报告。输入完整前文、Top32及预激活见[24条真实输入](data_casebook_cn.md)，行ID/完整均值/奇异值见[Detailed](detailed_cn.md)。

## 3. 总体变化轴是否相近

'''+tab(['接口','原始PC1绝对余弦','前二维投影重叠（0–1）','两主角（度）','猫−P/狗−P探索均值差有向余弦'],[[v['site'],f(v['PC1_absolute_cosine']),f(v['top2_normalized_overlap']),', '.join(f(a,3) for a in v['principal_angles_degrees']),f(v['exploration_mean_delta_cosine'])] for v in geom if v['scale']=='raw_z'])+'''
绝对余弦只比较无定向第一轴；前二维重叠是两投影算子重叠除以2，1才是同一二维子空间。它们不是语义相似度。AC/AD有一半相同P行，共享句式/词面也会带来总体轴接近，未由本对照排除。

把探索每轴的投影平方和分成“家族中点间”与“家族内父子差”后，第一轴如下：

'''+tab(['接口','矩阵','第一轴：家族中点间份额','家族内父子份额'],[[v['site'],v['group'],f(float(v['between_fraction'])*100,2)+'%',f(float(v['within_fraction'])*100,2)+'%'] for v in variance if v['scale']=='raw_z' and v['direction']=='1'])+'''
这里的分解是同一投影平方和的恒等式，不能将中点变化进一步直接认定为句式语义。它说明“总体第一轴”主要不是家族内P→细类差；不能仅凭轴相近回答父子变化问题。

## 4. 配对差、支持变化与复现

逐家族直接计算完整30000维猫−P与狗−P，长度与有向余弦不依赖SVD中心化。

'''+tab(['家族','Attention：猫/狗差余弦','MLP输入：猫/狗差余弦'],[[f'F{i+1:02d} '+('探索' if i<3 else '检查')]+[f(next(v['cat_dog_delta_signed_cosine'] for v in pair if v['site']==site and v['scale']=='raw_z' and v['family']==f'F{i+1:02d}')) for site in SITES] for i in range(6)])+'''
六家族均为正，但没有都趋近同一探索均值方向。探索/检查的**均值差**（先平均向量再算余弦，不是平均逐对余弦）如下：

'''+tab(['接口','探索猫/狗均值差L2','检查猫/狗均值差L2','探索两均值差余弦','检查两均值差余弦','检查均值相对探索：猫/狗余弦'],[[v['site'],f(v['exploration_cat_L2'])+'/'+f(v['exploration_dog_L2']),f(v['check_cat_L2'])+'/'+f(v['check_dog_L2']),f(v['exploration_cat_dog_signed_cosine']),f(v['check_cat_dog_signed_cosine']),f(v['cat_check_mean_to_exploration_mean'])+'/'+f(v['dog_check_mean_to_exploration_mean'])] for v in means if v['scale']=='raw_z'])+'''
因此“每组猫/狗变化彼此有共同方向分量”可作为候选现象；“跨句式沿一条固定父子轴”仍受限制。每条完整坐标、长度和两组投影均保留，不能只看二维图是否分开。

### 来自共同强弱还是Top32更替

每条差分成共同正成员的幅度变化、P零而细类正的换入、P正而细类零的换出。下面按3家族×猫狗6条差的平方范数汇总，分母是这些完整差的平方范数之和，属于几何份额，不是语义/功能份额。

'''+tab(['接口','分组','共同成员强弱','换入','换出'],[[site,'探索' if sp=='exploration' else '检查']+[f(next(v['pooled_squared_norm_share'] for v in aggregates if v['site']==site and v['scale']=='raw_z' and v['split']==sp and v['part']==part)*100,2)+'%' for part in PARTS] for site,sp in itertools.product(SITES,['exploration','heldout_check'])])+'''
两种变化都存在；本度量下成员换入/换出合计更大。Top32零值仍可能有正预激活，不能称作“独立新语义出现”。逐家族三部分互斥；跨家族平均后可能重叠，不能把均值分项能量直接相加。均值差比较的3×3交叉点积分项与具体成员事件在[Detailed](detailed_cn.md)及[原始事件表](results/difference_member_events.csv)中分别给出。

### 反例与稳定性

按预定规则，两接口都选到F05猫−P的AC第一轴投影反号：Attention探索均值 **+1.191980**，F05 **−1.002533**；MLP输入探索均值 **−3.266106**，F05 **+3.332532**。完整F05文本、固定主要成员数值见[反例段](detailed_cn.md)。完整向量余弦仍为正，一个分量反号不能说整条变化相反。

只用探索家族的27种成组bootstrap中，前二维有24/27可定义，其余3个只剩单一家族、秩1。第一轴相对原全探索轴的对齐范围很宽；这部分也受重采样删去句式家族所影响，不能给方向作可靠总体置信判断。

'''+tab(['接口','AC/AD第一轴绝对余弦重采样范围','前二维重叠范围（24有效）','AC第一轴对原拟合轴范围','AD第一轴对原拟合轴范围'],[[site]+[f(next(v['min'] for v in boot if v['site']==site and v['scale']=='raw_z' and v['metric']==metric))+'–'+f(next(v['max'] for v in boot if v['site']==site and v['scale']=='raw_z' and v['metric']==metric)) for metric in ['PC1_absolute_cosine','top2_overlap','AC_PC1_vs_full','AD_PC1_vs_full']] for site in SITES])+'''
这些是27个有序重采样（10个无序多重集）的经验范围，不是置信区间。Attention AD第二/三奇异值相对间隔约0.075，MLP AC第一/二约0.095，需警惕相近根下的轴旋转；完整谱与间隔均报告，二维子空间比较不能替代小样本稳定性判断。

## 5. 回到成员、尺度与认识更新

'''
for site in SITES:
 cn+=f'### {site}\n\n'+tab(['探索方向','前5个有符号系数（本字典ID）'],[[f'{g} PC{k}',', '.join('#'+r['atom']+':'+f(r['coefficient'],4) for r in top if r['site']==site and r['scale']=='raw_z' and r['group']==g and int(r['direction'])==k)] for g,k in itertools.product(['AC','AD'],[1,2])])+f'\n[每个方向的全部主要成员、P/猫/狗/椅子原始激活/预激活与完整前文]({site}/directions_and_members_cn.md) · [原S03 H2成员额外记录]({site}/fixed_H2_cn.md)。\n\n![冻结投影](figures/{site}_raw_z_projections.png)\n\n上下是探索与检查，左右是两组各自均值/方向的坐标，不能把左右轴当成同一坐标。箭头为每家族实际P→猫/狗；椅子仅投影，不参与SVD。\n\n![配对变化与分解](figures/{site}_raw_paired_decomposition.png)\n\n上：逐家族两差的有向余弦，虚线是探索均值差余弦；中：原始完整差长度；下：共同强弱/换入/换出的互斥平方范数份额。分组线分开探索/检查。\n\n'
maxsens=max(abs(float(v['weighted_minus_raw'])) for v in sensitivity if v['metric'] in ['PC1_absolute_cosine','top2_normalized_overlap','exploration_mean_delta_cosine'])
cn+=f'''特别记录：Attention #14602在本面板最终激活全为0，非零SVD方向对应系数也为0；#3516是AC第二方向的第一大绝对系数（+0.349），也是AD第二方向前5成员（约−0.243）。后者的正负受整组轴定向/旋转影响，不能解释成猫狗语义相反。它们都按原H2名单保留，未强行排在前面。

原始/decoder范数加权两尺度的三个主要相似度最大差为 **{maxsens:.3e}**；各原子decoder范数接近1，所以本轮尺度补充几乎相同，而不是事后选较好的一套。完整补充见[尺度表](results/scale_sensitivity.csv)、[Attention加权投影](figures/ATTN_SAE_decoder_weighted_projections.png)和[MLP输入加权投影](figures/MLPIN_SAE_decoder_weighted_projections.png)。加权坐标仍非decoder线性映射后的1024维几何；未执行该可选比较。

**认识更新：**当前面板中，猫−P与狗−P共享正向变化分量，而总体第一轴的接近大部分对应家族中点间变化；它们不能合成同一个“父子概念方向”结论。细类变化同时包含共同成员强弱和支持更替，后者在本平方范数度量中占较大部分；跨家族固定方向只部分保持，F05分量反号需保留。

共享P本身、相同/相近句式、P中的object与细类中的animal指代、明确的cat/dog词、冠词变化、Top32竞争、非唯一SAE坐标和只有3个探索家族仍是竞争解释。图分开或方向相近都不确定语义、功能或因果作用。原H1/H2假设不修订，下一步等待共同审阅；没有继续扩数据、训练、probe、干预或后续实验。

[Detailed与所有谱/差分/反例](detailed_cn.md) · [24条完整输入](data_casebook_cn.md) · [核验](evidence/verification.json)
'''
(C/'summary_cn.md').write_text(cn)
en='''# S05: overall AC/AD variation versus paired parent-to-fine changes

Exploratory geometry is complete on the verified S04 neutral-suffix cache. Positive alignment is observed for both overall axes and signed paired mean changes, but these are different objects. PC1 predominantly reflects between-family midpoint variation; check families only partly follow discovery directions, with an explicit F05 projection reversal. No semantic, functional or causal confirmation is inferred.

Purpose: compare animal-to-cat and animal-to-dog organization in each independent frozen SAE coordinate system. Use the same24 S04 bodies and final colon after Description:, without new model forwards. AC/AD each have6x30000 discovery rows from F01-03, identical P rows and separate column means; F04-06 only projected. Primary raw z, supplemental z times own decoder norm, both retained. Each centered matrix has numerical rank5. Original H1/H2 additional-information hypotheses remain unchanged and untested functionally.

'''+tab(['site','raw PC1 abs cosine','raw top2 normalized overlap','principal angles degrees','signed discovery mean-delta cosine'],[[v['site'],f(v['PC1_absolute_cosine']),f(v['top2_normalized_overlap']),str(v['principal_angles_degrees']),f(v['exploration_mean_delta_cosine'])] for v in geom if v['scale']=='raw_z'])+'''
SVD axes are unoriented; paired cat-P/dog-P vectors have meaningful signs. Separate own centering describes total within-group variation, not parent-child change. PC1 between-family midpoint fractions are ATTΝ AC.977/AD.888 and MLPIN AC.970/AD.941. Shared P rows, wording and explicit class tokens remain competitors for axis alignment.

Signed cat-P/dog-P cosine is positive in all6families at both sites. Check mean versus discovery mean alignment is only .480/.598(cat/dog) at Attention and .601/.543 at MLPIN. Check paired-mean cat/dog cosine is.768/.709 respectively. F05 cat-P projection on its frozen own AC PC1 reverses the discovery mean: Attention +1.191980 to -1.002533; MLPIN -3.266106 to +3.332532. A component reversal is not a whole-vector reversal. Full texts and fixed member values are retained.

Per-pair support-disjoint squared-difference energy separates retained amplitude/new support/lost support. Raw discovery shares are Attention.131/.543/.326 and MLPIN.327/.386/.286; check shares.140/.552/.309 and.369/.338/.293. These are geometric shares, not functional contributions or independent semantics. Means of parts can overlap across families; a separate3x3cross-dot table sums to the total mean-vector cosine and prevents treating mean energies as disjoint.

All27 ordered paired-family bootstrap samples use discovery only, representing10unordered multisets, not27independent observations. Top2 comparisons are valid24/27; the3single-family rank1 samples are undefined. Wide reference-axis alignment ranges and small spectral gaps limit fixed-axis interpretation. Quantiles are empirical resampling descriptions, not confidence intervals or reliable significance.

Top5absolute coefficients per direction were frozen before check projections, signs oriented as a group; original S03 H2 atoms are reported separately. ATTN14602 is inactive throughout this panel;3516 ranks first on AC PC2 but its AD sign need not match because axes can flip/rotate. Coefficient magnitude is not causal importance. Every selected atom has all24P/cat/dog/chair values,Top32 status,preactivation and full text. No dictionary-ID alignment or30000-to1024 comparison occurs. Decoder-norm weighting barely changes the main similarities (maximum<1e-6); both scales and their full spectra/projections are saved.

Recognition update: the current panel supports a candidate shared component in paired fine-minus-parent changes, while overall-axis similarity is largely about family midpoint variation. Support turnover and retained strength both contribute and fixed directions do not fully transfer. Six reused short explicit-word families, shared parents,referent/article changes,Top32 effects and dictionary dependence prevent general semantic claims. Stop for joint review; no training,probe,intervention,new data or follow-up.

[Chinese full result](summary_cn.md) · [Detailed](detailed_cn.md) · [24inputs](data_casebook_cn.md) · [verification](evidence/verification.json)
'''
(C/'summary.md').write_text(en.replace('ATTΝ','ATTN'))
(C/'detailed.md').write_text('''# S05 execution and evidence

Cache-only float64 analysis of completed S04, with8full exploration SVD fits and216paired-bootstrap fits; no model/SAE forward or training. Exact matrices,own means,directions,spectra,gaps,row IDs,all24projections,full30000-dimensional paired differences and their disjoint parts are saved. Top5direction members were frozen before check access; check rows never refit or select atoms. Original S03/S04 files remain hash-unchanged.

[The complete evidence ledger](detailed_cn.md) contains singular spectra,all per-family lengths/cosines,energy decomposition,mean cross-dot accounting,bootstrap validity/quantiles,full F05 counterexamples with text/values,scale sensitivity and numerical verification. [Protocol](protocol.md) retains the frozen rules. Scientific acceptance and next decision await joint review. No functional or semantic proof is claimed.
''')
(C/'README.md').write_text('''# S05 · AC/AD SVD and paired parent-to-fine geometry

[中文小结](summary_cn.md) · [English Summary](summary.md) · [完整谱、差分与反例](detailed_cn.md) · [24条真实输入与支持](data_casebook_cn.md) · [冻结协议](protocol_cn.md)

- Attention：[方向前5成员与完整文本](ATTN_SAE/directions_and_members_cn.md) · [原H2成员额外记录](ATTN_SAE/fixed_H2_cn.md)
- MLP输入：[方向前5成员与完整文本](MLPIN_SAE/directions_and_members_cn.md) · [原H2成员额外记录](MLPIN_SAE/fixed_H2_cn.md)

Only S04 neutral-suffix cached activations are used. Overall centered axes and signed paired changes are separate. All source matrices,means,differences,bootstrap rows,scripts and figures are included as requested; generated reading copies retain execution ownership in payload_manifest. Original S03/S04 records are immutable. STOP_WAIT_FOR_JOINT_REVIEW; no model forward,training,probe,intervention or automatic next experiment.
''')
print('S05_REPORTS_WRITTEN',flush=True)
