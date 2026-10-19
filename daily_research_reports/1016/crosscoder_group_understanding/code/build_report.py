"""Derived group reading report from frozen tables; no training or graph construction."""
from pathlib import Path
import json,csv,shutil,hashlib
from datetime import datetime,timezone
E=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder')
R=E/'analysis/group_understanding'
T=R/'20261016_tables'; C=R/'20261016_cases'; F=R/'20261016_figures'
D=Path('/data/250010109/Research_System/daily_research_reports/1016/crosscoder_group_understanding')
OLD=E/'analysis/feature_frequency/20261015T143300Z'
def rows(p):
 with p.open() as f:return list(csv.DictReader(f))
def table(headers,records):
 return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+''.join('| '+' | '.join(str(x).replace('|','\\|').replace('\n',' ') for x in r)+' |\n' for r in records)
def number(x):return f'{int(x):,}'
def pct(x):return f'{100*float(x):.6g}%'
def yes(x):return '是' if x in [True,'True'] else '否'
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
def main():
 D.mkdir(parents=True,exist_ok=True)
 shutil.copytree(T,D/'tables',dirs_exist_ok=True)
 shutil.copytree(C,D/'text_evidence',dirs_exist_ok=True)
 shutil.copytree(F,D/'figures',dirs_exist_ok=True)
 (D/'code').mkdir(exist_ok=True)
 for p in (E/'analysis_tools/group_understanding').glob('*.py'):shutil.copy2(p,D/'code'/p.name)
 (D/'provenance').mkdir(exist_ok=True)
 shutil.copy2(R/'20261016_input_access.json',D/'provenance/input_access.json')
 source_dir=D/'source_tables';source_dir.mkdir(exist_ok=True)
 for name in ['frequency.csv','main/groups_D.json','main/groups_V.json','main/matches.csv','main/edges_D.csv','main/edges_V.csv','registered_config.json']:
  shutil.copy2(OLD/name,source_dir/Path(name).name)
 idx=rows(T/'all_groups_index.csv'); by={int(r['group_id']):r for r in idx}
 examples=json.loads((C/'selected_cases.json').read_text())['cases']
 for e in examples:
  # Original execution-side identity is retained separately; reading-copy paths are relative.
  e['original_model_visible_prefix_file']=e['model_visible_prefix_file']
  e['model_visible_prefix_file']='prefixes/'+Path(e['model_visible_prefix_file']).name
 write(D/'text_evidence/selected_cases.json',json.dumps({'cases':examples,'source':str(C/'selected_cases.json'),'operation':'only prefix reading paths rebased; original path retained'},indent=2,ensure_ascii=False)+'\n')
 choices={87:'小组定义为2–5成员。为了完整展示缺边，先要求有现成3随机/3高分案例且不是完全图，再取成员数最接近4者；同分取最小原group ID。最终为G87。这是教学案例，不是随机抽到的代表组。',74:'中等组定义为6–19成员。以该层原始成员数中位数14为目标，要求现成随机/高分各至少3条；按离中位数最近、原group ID最小选到G74。没有按语义或稳定性挑选。',34:'大组定义为20成员及以上。以该层原始成员数中位数149为目标，要求现成随机/高分各至少3条；按离中位数最近、原group ID最小选到G34。没有按语义或稳定性挑选。'}
 narratives={
 87:('四个成员，三角形加一条桥','G87的四个成员并非两两有边。800、14514、15978构成三角形，1572只通过15978接入；1572–15978是唯一桥，移除15978会把1572与另两个成员分开。六对phi虽都为正，但大小从约0.046到0.220，关系强弱并不一致。','D频率相差5.67倍，V相差5.27倍，所以“同组”没有要求相同频率。V的匹配组G92恰为同四人，四条D边也全部保留；现有q20分组仍是同四人。这只能说这两种现有复核下成员和边较稳定，不能给出以后数据上的稳定概率。','六例跨评论、赛事、论文条目、医疗及学术讨论，尚看不出统一话题。随机三例当前token是the/for/the，高分三例却是逗号、cp、J，连单一当前token也不能概括这个组；高分仅表示更多成员同时激活。'),
 74:('多数原成员仍相聚，组的外边界却扩张','14个成员之间只有33/91对是边，含5条桥和4个割点；全对phi中位数约0.0468，且存在非正关系。它包含较紧的局部连接，也有靠桥接入的成员，不能把14人整体当作相互都很相似。','D命中次数102–8621次，相差84.52倍；V相差125.56倍。匹配V组G43含98人，保留原组12/14，却额外加入86人，因此Jaccard仅0.12；这主要体现外边界扩张，不能误说成86%的原成员消失。原成员12922、15635没有留在这个匹配V组，具体去向见成员表。','三条高分都位于Message-ID字符段，当前token为CC/BD/BA，提示局部字符/标识符形态可能有关。但随机例分别出现博客ID的ef、用户名的JC和DOI中的5，直接限制了“邮件专属主题”的解释。只将这个共同点保留为这六例上的描述，不命名主题。'),
 34:('局部边大多保留，149人的整体边界仍改变','149个成员有11026种配对，现成D图只保留310条边（2.81%）；互选前10名规则本来就限制大组密度，不能只靠密度判弱。进一步看未筛选全对，phi中位数约0.00125，约42.1%的对非正。组内有38条桥和35个割点，说明局部连接与桥接部分并存，不能说149个成员彼此都很近。','D命中次数165–99814次，相差604.93倍；V相差561.49倍。292/310条D内部边在V仍是边，但原149人只有86人进入匹配V组G42（该组100人，另有14名新成员）；63名原成员分流，完整去向有表。局部连接重复性高于整个社区边界的重复性。','六例当前token都为of，三条高分前面均为quarter(s)，随机例却分别为pool of、subject of、rebirth of，横跨生态、语法和乐评。这里首先看见局部词法/句法片段相似，尚没有统一话题证据；每例仅15–35/149人激活，也不是所有成员一起响应。')}
 for gid in [87,74,34]:
  r=by[gid]; mem=rows(T/f'groups/group_{gid:03d}_members.csv');title,top,frq,txt=narratives[gid]
  out=f'# 案例卡：G{gid} · {title}\n\n[回到一页导读](../README_cn.md) · [186组索引](../group_index_cn.md)\n\n'
  out+=f'原group ID为{gid}，保留原始0起始编号；有{r["size"]}个成员。本卡来自已冻结的q=10分组，没有重建图或重新训练。\n\n**选择规则。** {choices[gid]}\n\n'
  out+='这里的feature是冻结CrossCoder的潜变量坐标；门控z>0表示在一个文本位置命中。D是发现部分，V是同一来源bin内另一复核部分，不是已确认独立的原始文档。\n\n'
  out+='## 组内究竟有哪些关系\n\n'+top+'\n\n'
  out+=f'![G{gid}关系图](../figures/group_{gid:03d}_relations.png)\n\n'
  if gid==87:
   out+='图中四个圆点是全部成员，线是现成D图的四条边；看三角形及1572接入的位置。实际看到三角形加一条桥，另外两对没有连边；图上的同组和路径都不能证明语义组合或学习相容。\n\n'
  elif gid==74:
   out+='图中展示全部14名成员和33条D边，颜色区分是否留在匹配V组，线型区分该D边在V是否仍保留。图内存在桥和外围成员；几何距离只由绘图布局产生，不能当作额外相似度。\n\n'
  else:
   out+='这张图只展示按固定规则选出的30/149名成员，明确不是整组；完整149名成员在下方表中。它显示所选局部的现成连接（最大组内度起点、按原phi降序广度优先选点，ID破同分，再画诱导边）；这30人恰好全留在匹配V组，但整组只有86/149人保留，不能外推。遗漏节点和连边不能理解为不存在，局部密度也不代表整组。\n\n'
  out+=f'**频率与现有复核。** {frq}\n\n'
  if gid==74:
   out+='33条D内部边中25条在V仍保留（75.76%）。已有q20分组中，原14人有11人进入同一个284人大组，说明扩大邻居数后边界更大；这次只是读取原q20文件，没有改参数重跑。\n\n'
  if gid==34:
   out+='已有q20分组中，原149人有112人进入同一个321人大组，其余分散在其他组；原组内配对中57.52%在q20仍同组。这里的“未留在匹配组”不是feature不再激活或被删除。\n\n'
  out+=f'![G{gid}成员频率](../figures/group_{gid:03d}_frequencies.png)\n\n'
  out+='横轴按D频率从高到低排列成员，纵轴是D/V有效位置中的激活频率；D分母为5,238,097，V为5,247,663。实际频率范围见上文，读图应比较比例而非直接比较不同分母的次数；这些频率不测量知识稀有性或任务难度。\n\n'
  if gid==34:
   out+='本图使用对数刻度，全部149人的ID对应[频率顺序表](../figures/group_034_members_frequency_order.csv)。\n\n'
  if gid==87:
   pairs=rows(T/'cases/group_087_all_pairs.csv');rank={(800,1572):(49,500),(800,14514):(2,1),(800,15978):(1,1),(1572,14514):(596,45),(1572,15978):(6,4),(14514,15978):(2,2)}
   out+='## 从次数到phi，再到连边与分组\n\n一个位置中保存的门控激活值z>0，就记为该feature命中。D是发现部分，V是同一来源bin内另一部分；它们不是已确认独立的原始文档。feature ID只是固定CrossCoder潜变量坐标，尚没有可靠语义标签。\n\n'
   out+='两feature的phi比较“实际共同激活”与“仅按各自频率独立出现”的差异。令N为位置数，n_i、n_j为各自命中次数，n_ij为共同命中次数，则：\n\n\\[\n\\phi_{ij}=\\frac{N n_{ij}-n_i n_j}{\\sqrt{n_i(N-n_i)n_j(N-n_j)}}.\n\\]\n\n'
   out+='例如800与14514在D分别命中243,591和84,036次，共同命中24,825次；独立频率背景期望约3,908次，得到phi约0.150935。phi为正表示超过该独立背景，不表示因果或语义联系。\n\n'
   out+=table(['feature对','D共同次数','D phi','V共同次数','V phi','D互选名次 i→j / j→i','D连边'],[(f'{p["u"]}–{p["v"]}',number(p['joint_D']),f'{float(p["phi_D"]):.6f}',number(p['joint_V']),f'{float(p["phi_V"]):.6f}',f'{rank[int(p["u"]),int(p["v"])][0]} / {rank[int(p["u"]),int(p["v"])][1]}',yes(p['edge_D'])) for p in pairs])
   out+='\n各成员先通过原D候选门槛（至少100次命中且覆盖10个D块）。候选对共同命中至少10次且phi为正后，每个成员按phi降序选择最多10个邻居，同分按feature ID；只有相互选中才连边。800–1572虽共同出现28,105次、phi也为正，却分别只排49和500，因此不连边。\n\n'
   out+='原算法从单节点出发，反复合并能提高模块度的社区；模块度比较组内连边权重与保持节点加权度的背景预期。这就是现成的greedy modularity方法，resolution=1，再按成员数及ID确定组编号。此例四人恰好构成没有对外边的连通分量，现有分组把四人放在一起；它没有要求组内全连接。原逐步合并日志未保存，不能声称知道实际每一步的合并先后。\n\n'
  out+='## 全部成员及其次数\n\n'
  out+=table(['feature ID','D次数','D频率','V次数','V频率','实际V组','留在匹配V组'],[(m['feature_id'],number(m['n_D']),pct(m['p_D']),number(m['n_V']),pct(m['p_V']),m['actual_V_group_id'],yes(m['retained_in_matched_V_group'])) for m in mem])
  out+=f'\n此表完整列出{len(mem)}名成员，没有用画出的节点代替全部名单。[成员原始CSV](../tables/groups/group_{gid:03d}_members.csv)含组内邻居、桥关联、V去向和q20去向；[全部D内部边](../tables/groups/group_{gid:03d}_edges.csv)和[全部成员对共同次数/phi](../tables/cases/group_{gid:03d}_all_pairs.csv)供核对。\n\n'
  out+='## 三条随机命中、三条高得分命中\n\n随机例沿用原seed=20261015的命中context哈希抽样，再从已保存5例中取context哈希最小3例；不是对命中token均匀抽样。高分从已保存5例按“激活成员数/组大小”降序取3例，同分取较早位置，所以存在同分早位置偏向；高分不代表激活幅度更大或语义更纯。\n\n'
  out+='【】标出当前已看见的token t，前缀止于t；当前激活用于预测t+1。下列“下一token”是真实语料标签，模型尚不可见，且不是模型生成结果；已有缓存未保存这些位置的模型argmax预测，记为未提供。\n\n'
  es=[x for x in examples if x['group_id']==gid]
  appendix=f'# G{gid}完整文本前缀与激活值\n\n[返回案例卡](group_{gid:03d}_cn.md)\n\n每条前缀完整保留，含原始特殊token及可能的拼接文本边界；原文档ID未知。激活取当前位置t，真实下一token仅作标签，不混入前缀。\n\n'
  for e in es:
   lab='随机' if e['sample_type']=='random' else '高分'; cid=e['case_id']; prefixfile=Path(e['model_visible_prefix_file']).name
   vals='；'.join(f'{x["feature_id"]}={x["z"]:.8g}' for x in e['active_members_complete'])
   next_repr=json.dumps(e['next_target_token_label_only'],ensure_ascii=False)
   out+=f'### {lab}{e["selection_rank"]} · {cid}\n\ncontext={e["context_index"]}，当前位置t={e["current_context_offset_zero_based"]}，预测位置t+1={e["prediction_position_context_offset_zero_based"]}（均为context内0起始token编号）；前缀共{e["visible_prefix_token_count"]}tokens。当前token={json.dumps(e["current_token"],ensure_ascii=False)}；真实下一token={next_repr}。分数{e["active_member_count"]}/{e["group_size"]}={e["group_score"]:.4f}。\n\n'
   out+='```text\n'+e['display_suffix_current_marked']+'\n```\n\n'
   out+='以上只展示前缀末45个token及当前token；[完整模型可见前缀](../text_evidence/prefixes/'+prefixfile+')已保存，未把预测位置或右文放进来。\n\n'
   out+='**当时全部非零组内激活（z）：** '+vals+'。其余组内成员的门控z=0，完整含零表见[原始CSV](../text_evidence/selected_case_all_member_z.csv)。\n\n'
   appendix+=f'## {cid}\n\ncontext={e["context_index"]}；当前t={e["current_context_offset_zero_based"]}；预测t+1={e["prediction_position_context_offset_zero_based"]}；真实下一token={next_repr}（标签，不可见）。\n\n'
   appendix+='```text\n'+e['model_visible_prefix']+'\n```\n\n全部非零组内激活：'+vals+'。\n\n'
  out+='**只依据六例的解释与反例。** '+txt+'\n\n'
  out+=f'[六条完整前缀汇总](group_{gid:03d}_texts_cn.md) · [文本及全部激活JSON](../text_evidence/selected_cases.json) · [定位表](../text_evidence/selected_cases_index.csv)\n\n'
  out+='## 可以保留的判断\n\n同组不意味着两两连接，不意味着每一对都有高phi，也不要求频率完全接近。这些图表只描述固定编码器、固定数据和现成分组下的共同激活；六条文本不能证明语义组合，现成D/V和q20复核也不能证明学习相容或共同更新有益。\n\n数值来源：[原始频率表](../source_tables/frequency.csv)、[D分组](../source_tables/groups_D.json)、[D边](../source_tables/edges_D.csv)、[V边](../source_tables/edges_V.csv)、[D/V匹配](../source_tables/matches.csv)。计数矩阵、来源哈希和逐字段映射见[表来源清单](../tables/source_manifest.json)；文本来自原examples.json并逐条与CSR及token位置核对，见[提取回执](../text_evidence/extraction_receipt.json)。\n'
  write(D/f'cases/group_{gid:03d}_cn.md',out)
  write(D/f'cases/group_{gid:03d}_texts_cn.md',appendix)
 index='# 全部186个非单例组索引\n\n[一页导读](README_cn.md) · [全组索引CSV](tables/all_groups_index.csv) · [全部13807名成员CSV](tables/all_group_members.csv)\n\n保留原group ID（0起始），仅列原D的186个非单例组；1859个单例不在本表。频率是门控激活命中位置比例，D/V分母分别为5,238,097/5,247,663；下列频率范围为百分比。\n\n匹配J是原全局一对一社区匹配的交集/并集；保留人数以原D组为分母，两者不可混用。CSV另列每组不受全局一对一约束的最佳V匹配，以免把被其他组占用的匹配误认作不存在；V分组变化不是feature消失。复核限现有D/V和现有q20结果，没有长期稳定性或独立文档保证。\n\n'
 index+=table(['原group ID','人数','D频率范围','V频率范围','D边数/可能对','匹配V组：人数','D→V保留','匹配J','成员表 / 边表'],[(r['group_id'],r['size'],f'{pct(r["p_D_min"])}–{pct(r["p_D_max"])}',f'{pct(r["p_V_min"])}–{pct(r["p_V_max"])}',f'{r["internal_edges_D"]}/{r["possible_pairs"]}',f'{r["matched_V_group_id"]}：{r["matched_V_group_size"]}',f'{r["matched_V_intersection"]}/{r["size"]}',f'{float(r["matched_V_jaccard"]):.3f}',f'[成员](tables/{r["members_csv"]}) / [边](tables/{r["edges_csv"]})') for r in idx])
 index+='\n所有成员的ID、D/V次数及频率、实际V去向、是否留在匹配组、q20去向均已导出，未留白伪作零。未知字段明确标为NOT_MEASURED/NOT_ASSIGNED/NOT_ESTABLISHED；字段与原始数值的对应见[数据字典](data_dictionary_cn.md)和[来源清单](tables/source_manifest.json)。\n'
 write(D/'group_index_cn.md',index)
 readme='''# 逐组理解报告：先看一个真实小组\n\n**先读[四成员G87完整案例](cases/group_087_cn.md)。** 它把成员次数、六对共同次数/phi、四条实际边、分组依据和六条文本连在一起：三角形加一条桥，并不是四人两两都连边。\n\n本次只整理现有缓存、分组、频率和文本，未训练、未编码新位置，也未改变或重跑建图/分组参数。所有解释是AI依据现有证据的有界阅读，不改变科学批准。\n\n## 三张卡要回答什么\n\n- [G87：4成员](cases/group_087_cn.md)。三角形加桥，D/V及已有q20都保留同四人，但D频率仍相差5.67倍。六例语境分散，不能强命名主题。\n- [G74：14成员](cases/group_074_cn.md)。原14人中12人仍在同一V组，却被并入98人的大组，导致Jaccard只有0.12；这是边界扩张，不能误读为多数成员丢失。高分字符片段的共同点被随机博客ID、用户名和DOI案例限制。\n- [G34：149成员](cases/group_034_cn.md)。局部边292/310保留，但完整成员只有86/149进入匹配V组；D频率相差约605倍。关系图明确只画30人，频率图和成员表覆盖全部149人。六例都在当前token ` of`，仍不能推出统一话题或全部成员一起激活。\n\n## 全部组与原始表\n\n[186组可读索引](group_index_cn.md) · [186行索引CSV](tables/all_groups_index.csv) · [13807行完整成员CSV](tables/all_group_members.csv) · [每组完整成员/边表](tables/groups/)\n\n[原始频率表](source_tables/frequency.csv)、[原始D分组](source_tables/groups_D.json)、[原始D边表](source_tables/edges_D.csv)、[原始V分组](source_tables/groups_V.json)、[原始V边表](source_tables/edges_V.csv)、[原始匹配表](source_tables/matches.csv)均为来源文件的字节副本。[数据字典](data_dictionary_cn.md)说明分母、来源和未知项。\n\n每卡有3随机/3高分既有案例，逐条标注当前已见token、下一预测位置、完整前缀链接和全部非零组内z；[完整文本与激活](text_evidence/selected_cases.json)另含所有成员的零值。旧文件名target_token实际指当前已见token，本次已区分；真实下一token只是标签，不能写成模型实际预测。\n\n**本次应保留的理解：** 同一个组里可以同时有较密局部、桥接成员、很宽的频率范围和不一致的文本触发。现有稳定性告诉我们哪部分在这次复核中重复，并不把这些统计组升级为语义组合，更不说明适合共同学习。此前“比匹配随机对照更同频”是群体相对比较，不保证每组频率范围都窄；本报告的宽范围并不与那个平均结果矛盾。\n\n[审计与完整性核对](reasoning_audit_cn.md) · [全部产物来源/哈希](artifact_manifest.json)\n'''
 write(D/'README_cn.md',readme)
 write(D/'README.md','# Group-by-group reading report\n\nThe researcher requested Chinese explanations. Start with [the Chinese one-page guide](README_cn.md), then the complete four-member [G87 case](cases/group_087_cn.md). The original graph parameters, groups and research states are unchanged.\n')
 dictionary='''# 数据字典与来源边界\n\n- feature：冻结14源层、16384维CrossCoder中的原始latent坐标。激活事件是现成CSR中该坐标的门控z>0，不是已确认知识或语义标签。\n- D/V：原缓存按既有块规则分成的发现/复核部分，N_D=5238097、N_V=5247663；文档独立性和近重复独立性未知。n是命中次数，p=n/N，是位置比例，不是文本篇数。\n- group_id：沿用q10 D分组原始0起始ID。186非单例组共13807成员，各成员只归一个D组；不包括1859个单例。\n- phi：二值命中事件的相关系数，计算包含未共同激活位置；不能只用共同次数排名代替。索引CSV的全对分布字段复用原phi float32；案例成对CSV精确表从原int64共同计数重新代入同一公式（数值精度差别不改变原边）。\n- 连边：原候选集内，joint≥10、phi>0且互为前10邻居；门槛及排序不变。本报告只审计已有边，未重建图。\n- group：原加权greedy modularity分区，resolution=1。同组不要求全连接、全对高phi、频率相等或每次全员激活。原合并过程日志没有保存。互选前10名还强制度≤10，大组密度因此有10/(人数−1)的上界，不能仅凭低密度判定关系弱；同时参考未筛选全对phi与桥结构。\n- bridge/桥：在原组诱导子图里删除后增加连通分量数的边；articulation/割点同理但删除节点。这是现成图的描述，不是删feature的模型干预。\n- matched_V_jaccard：原全局一对一匹配的交集/并集；matched_V_member_retention是交集/原D人数。actual_V_group_id逐成员给出实际去向，没进匹配V组不表示feature不再激活。\n- unconstrained_best_V：只读比较现有V组（包括V单例）、取消全局一对一占位限制得到的最佳J，不是替换原注册匹配。q20_*读取已存在敏感性分组，不是新增q20运行。\n- 稳定性：现有一次D/V和一次q20复核，不是时间序列、多个新split或独立文档复现。未测的长期稳定性为NOT_MEASURED；语义主题为NOT_ASSIGNED；学习相容为NOT_ESTABLISHED。\n- 原随机案例：每组命中context按固定哈希抽样，再在选中context的命中位置哈希抽样；不是位置均匀、不是独立文档抽样。只复用已保存5+5中的3+3，未补采或补造。\n- 高分：活跃组员数/组大小；不是z幅度和，不是统计置信度。同分按较早位置取，可能偏向早位置。\n- 预测位置：当前t的feature来自模型可见token0…t；预测目标位于t+1。next_target_token_label_only来自真实语料，不是模型argmax；这些位置的实际模型预测未保存。\n- 完整前缀和z：18条逐一复核原CSR，完整前缀独立复核token解码；卡片只显示末45token及当前token，前缀原文另附TXT和完整汇总。激活列表无top-k截断，未列成员z=0，完整含零CSV另存。\n\n表内source_id对应[tables/source_manifest.json](tables/source_manifest.json)，包含绝对源地址、大小、SHA256及推导说明；frequency_source_row_1based_including_header可逐行定位原频率表。原始文本可能跨拼接片段，original_document_id仍UNKNOWN，不把context当独立原文档。\n'''
 write(D/'data_dictionary_cn.md',dictionary)
 print(str(D))
if __name__=='__main__':main()
