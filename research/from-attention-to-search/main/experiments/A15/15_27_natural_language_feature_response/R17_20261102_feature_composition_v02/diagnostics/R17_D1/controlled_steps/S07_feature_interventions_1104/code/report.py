from common import *
import numpy as np,itertools,shutil
def tab(h,rr):return '\n'.join(['| '+' | '.join(h)+' |','| '+' | '.join(['---']*len(h))+' |']+['| '+' | '.join(str(v) for v in r)+' |' for r in rr])+'\n'
def f(v,n=5):return 'NA' if v is None or v=='' else f'{float(v):.{n}f}'
def rd(n):return list(csv.DictReader(open(R/f'results/{n}.csv')))
rr=rows(R/'results/conditions.jsonl');primary=json.load(open(R/'results/primary.json'));off=rd('offdomain_effects');quality=rd('control_quality');case=rows(R/'data/panel.jsonl');idx={p['id']:p for p in case};sel=json.load(open(R/'data/selection.json'));verify=json.load(open(R/'evidence/verification.json'));top={r['condition_id']:r['top'] for r in rows(R/'results/top20.jsonl')}
def get(p,s,d,arm,a=None,dest=None):return next(r for r in rr if r['text_id']==p['id'] and r['site']==s and r['intervention_domain']==d and r['arm']==arm and (arm=='identity' or r['group']=='common') and r['alpha']==a and r['destination']==dest)
pt=tab(['SAE','大类','干预','原始边际损失','相对对照差[95%区间]','合格家族/8','Holm p','裁决'],[[r['site'],r['domain'],r['kind'],f(r['raw_margin_loss_mean']),f"{f(r['specificity_mean'])} [{f(r['specificity_ci_low'])}, {f(r['specificity_ci_high'])}]",r['eligible_families'],f(r['p_holm']),r['specificity_status']] for r in primary])
qt=tab(['SAE','大类','对照','条件数','发现频率/强度合格','同成员支持保持','实际范数比合格'],[[r['site'],r['domain'],r['arm'],r['conditions'],r['discovery_qualified'],r['pure_support'],r['norm_ratio_matched']] for r in quality])
ot=tab(['SAE','干预组','操作','文本组','条件数','四候选平均绝对分数变化','全词表KL'],[[r['site'],r['domain'],r['kind'],r['cohort'],r['N'],f(r['mean_abs_score_change']),f(r['mean_KL'])] for r in off])
casebook=['# 干预逐例：文本、成员、完整候选分数和排名\n','F09事先固定展示；其余反例按既定规则first_nonpositive选取。所有未展示条件仍有逐条原始记录。概率p4以4个完整序列为分母；全词表排名及p_vocab只指答案首词，词表151936项。没有把受限二选一正确当作自由生成能力。\n']
case_table=[]
for s,d in itertools.product(SITES,DOMAINS):
 ls=DOMAINS[d];p=next(p for p in case if p['family']=='F09' and p['wording']=='explicit' and p['label']==ls[1]);dest=ls[2];a=get(p,s,d,'identity',0);b=get(p,s,d,'delete');c=get(p,s,d,'strength',.5,dest);sh=get(p,s,d,'strength_shuffle',.5,dest)
 casebook += [f'## {s} / {d}\n','```text\n'+p['prefix']+'\n```\n',f"目标token是答案前最后冒号ID25；0起位置{p['target_index_zero_based']}。原始token：`{p['token_ids']}`。\n",f"共同组 `{b['feature_ids']}`；原z `{b['old_z']}`；删除后 `{b['new_z']}`；alpha.5朝{dest}后 `{c['new_z']}`；等范数打乱模式后 `{sh['new_z']}`。\n",f"原/反侧组L2：{c['old_group_L2']:.6f}/{c['new_group_L2']:.6f}；实际构造的表征扰动L2：删除{b['delta_hidden_L2']:.6f}，反侧{c['delta_hidden_L2']:.6f}，打乱{sh['delta_hidden_L2']:.6f}。同成员支持保持：反侧{c['support_preserved']}、打乱{sh['support_preserved']}；反侧超出发现两类逐坐标范围{c['outside_discovery_coordinates']}个。实际注入FP32范数在actual_injection_norms.csv。\n"]
 cols=[]
 for j,label in enumerate(a['candidate_order']):
  cols.append([label]+[f(r['scores'][j],6) for r in [a,b,c,sh]]+[a['candidate_vocab_ranks'][j],c['candidate_vocab_ranks'][j],f(a['candidate_sequence_prob4'][j]),f(c['candidate_sequence_prob4'][j]),f(a['candidate_vocab_prob'][j],9),f(c['candidate_vocab_prob'][j],9)])
 casebook.append(tab(['完整候选','无操作重放S','删除S','反侧.5 S','打乱S','原首词rank','反侧rank','原p4','反侧p4','原p_vocab','反侧p_vocab'],cols))
 for label,r in [('original_noop',a),('delete',b),('opposite_strength',c),('same_member_shuffle',sh)]:
  casebook.append('### '+label+'：全词表top10\n'+tab(['rank','token ID','解码字符串','p_vocab'],[[v['rank'],v['token_id'],'`'+repr(v['decoded']).replace('|','\\|')+'`',f(v['p_vocab'],9)] for v in top[r['condition_id']][:10]])+f"top20质量{r['top20_mass']:.8f}，其余质量{r['tail_mass']:.8f}；全词表熵{r['entropy_nats']:.6f}，KL(new||original)={r['KL_new_vs_baseline']:.8f}。\n")
 case_table.append(dict(site=s,domain=d,text_id=p['id'],feature_ids=b['feature_ids'],old_z=b['old_z'],opposite_z=c['new_z'],baseline_scores=a['scores'],opposite_scores=c['scores'],deleted_scores=b['scores'],baseline_vocab_ranks=a['candidate_vocab_ranks'],opposite_vocab_ranks=c['candidate_vocab_ranks'],baseline_p4=a['candidate_sequence_prob4'],opposite_p4=c['candidate_sequence_prob4']))
casebook.append('## 固定规则反例\n')
for x in json.load(open(R/'results/counterexamples.json')):
 r=next(r for r in rr if r['condition_id']==x['condition_id']);p=idx[r['text_id']];casebook += [f"### {x['site']} / {x['domain']} / {x['kind']}\n",'```text\n'+p['prefix']+'\n```\n',f"规则：{x['reason']}；正确候选边际损失{x['margin_loss']:.6f}nats，负号表示正确差反而增大。原S={r['baseline_scores']}，干预S={r['scores']}，实际组ID={r['feature_ids']}，原z={r['old_z']}，新z={r['new_z']}，注入范数={r['delta_hidden_L2']:.6f}。\n"]
(R/'casebook_cn.md').write_text('\n'.join(casebook));dump(R/'results/fixed_case_values.json',case_table)
intro='''本补充研究的是前向临时干预后的输出作用。主S06已先完成并保存；本次不覆盖主实验候选、数据、结果和3.96MB原包。行为与控制、表征改变量、输出功能与数值质量三条路径分开；以下结论是AI有边界的认识更新，科学接受和机制判断仍由研究者保留Unknown。
'''
summary=['# SAE组合干预：有局部分数作用，尚未得到普遍语义转换\n',intro,
         '## 最重要的认识更新\n',
         '**可复现的组合关联，不能直接解释为维持正确分类所必需。** 删除共同大组通常让正确候选对兄弟的边际增大，同时改变其他类别分布。MLP输入动物／交通工具的平均边际增大约0.849／1.493 nats。共同组的完整频率／强度匹配失败，且扰动很大；因此不能把该变化归给类别专属成员，更不能把“删除后更好”命名为已识别的语义机制。\n',
         '**共同成员的强弱方向可以对候选分数有小的局部作用。** Attention动物组在alpha=.5反侧移动下，8/8家族的正确边际下降，平均0.01236 nats；同成员、等表征范数打乱对照平均下降0.00613，差0.00623，95%家族区间[0.00135,0.01340]，Holm p=.03125。该条件16/16文本仍选正确。它支持当前方向对受限候选分数的局部敏感性，没有实现猫狗判断转换。\n',
         '**作用依赖字典、类别和控制。** Attention交通工具反侧移动在8/8家族反而增强正确边际，未支持预期的反侧偏移；MLP动物相对打乱对照未支持，MLP交通工具只有5/8合格家族，证据不足。动物Attention强弱编辑也影响无关交通候选，不能称为纯语义定向。\n',pt,
         '“边际损失”=原正确候选对兄弟分数差减去干预后的差，正号才是削弱原答案；“相对对照差”=候选损失−对照损失。主判断按8个家族(每家族两子类)而非按feature／token计独立样本。删除0/8表示缺合格匹配，不表示没执行；全部删除和其他参照仍实际运行。\n',
         '## 真实文本、feature和解码分布\n']
for v in case_table:
 if (v['site'],v['domain']) not in [('ATTN_SAE','animal'),('MLPIN_SAE','vehicle')]:continue
 p=idx[v['text_id']];summary += ['```text\n'+p['prefix']+'\n```\n',f"{v['site']}，共同ID `{v['feature_ids']}`；z原 `{[round(a,4) for a in v['old_z']]}`，反侧alpha.5后 `{[round(a,4) for a in v['opposite_z']]}`。完整候选顺序cat/dog/car/bicycle，原S `{[round(a,5) for a in v['baseline_scores']]}`，反侧S `{[round(a,5) for a in v['opposite_scores']]}`。原首词全词表rank `{v['baseline_vocab_ranks']}`，反侧rank `{v['opposite_vocab_ranks']}`。\n"]
summary += ['F09猫的Attention例子尤其直观：cat首词rank174→167，dog2364→2234，但四候选归一化cat概率0.94743→0.94577。两词都上升时，猫仍可相对狗变弱。排名、全词表概率和候选间偏好必须分开解释。全词表首选通常不是这些强制候选，完整top20与其余质量在逐例记录中。\n',
            '![逐例干预](figures/case_animal_ATTN_SAE.png)\n热图给原始／删除／反侧／打乱后的同一组真实z，右侧是完整两token候选的log概率；下方并列范数和全词表排名，不把两种概率分母混合。\n',
            '![留出家族剂量与对照](figures/strength_family_dose_controls.png)\n散点是8个家族两子类平均边际损失，线是均值；每个alpha及反例都保留。主要条件没有改变16/16的二选一正确数，分数作用强度须如实看待。\n',
            '## 操作、检查与边界\n',
            '两套原生SAE在各自hook临时注入h新=h原+Wdecoder(z新−z原)，decoder偏置在差里抵消，原重构残差保留。没有把h替换成SAE重构，也没有训练或永久写权重。共同模式来自8个显式发现家族；96条原始输入=64显式留出(含父类／负类／跨域)+32属性细类。全部14976条件保留实际活跃成员数、旧新z、实际扰动范数和超范围标记。\n',
            '完整前向校准最大分数误差6.44e-6 nats，无操作重放最大9.54e-6；96条原模型重测与主实验分数和z完全一致。该最后一层单位置干预不改变后续候选token的句号项；批量计算重新经过全部剩余非线性MLP／RMSNorm／输出头，不是一阶近似。\n',
            '严格共同组删除匹配不足；等范数随机组合是其他活跃成员的正向添加，另标操作，不能冒充相同删除。强弱主对照在相同成员上打乱发现典型模式并按实际decoder扰动范数匹配。属性猫原行为3/8，仍仅作探索；不可用它把主结论升级为抽象语义因果机制。重编码诊断表明，编辑后的目标坐标与再编码结果也未必完全一致，结论因此限定为这些decoder方向的作用。\n',
            '本轮同时保留未支持、反向和匹配不足。没有证据表明这些方向是自然计算的唯一机制、真实概念替换或MoE router的专家分工。AI建议的下一项判断是：能否在词面受控且扰动局部、匹配足够的条件下保留这个很小的方向差；本轮不自动启动下一轮。\n',
            '[详细报告](detailed_cn.md) · [完整文本／排名／分布及反例](casebook_cn.md) · [协议](protocol_cn.md) · [复算和数据](reproduce.md)\n']
(R/'summary_cn.md').write_text('\n'.join(summary))
detail=['# Detailed：残差保留的SAE成员组合干预\n',intro,
        '## 研究问题、假设与竞争解释\n',
        '问题：改变发现组合后，原模型对同样候选的解码偏好是否出现跨留出家族复现、超出匹配参照的变化？预期分开为共同组删除和反侧强弱重组；删除不预设所有共同成员都是必需，强弱反侧预期削弱原正确候选。竞争解释是任意扰动范数、活跃删除数不匹配、泛化输出分布变化、超出发现范围、未保持共同支持和显式词复述。主S06的观察结果已知，故这是“观察已见、干预未见”的预登记补充，不称完全未见语义确认。\n',
        '## 来源、候选和实际输入\n',
        '在主实验完整结果、609项核验及3.96MB包保存后才固定S07。所有候选只来自原64条显式发现响应：共同组=原H2列表；非空换入／换出列表=原排名前3个。没有按主留出成功重选。共16个非空组，其中11个有发现频率／正幅值合格的逐坐标匹配名单，5个缺匹配；所有共同组在这5个中。每域／每字典各自IDs，不求一致。无非空候选的组不生造。\n',
        '沿用64条显式留出和32条属性细类原文，未调整提示结构。每模板8类别或属性4细类；父类／负类仅偏好无正确答案。每份文本仍以Description:冒号ID25结束。主解释以显式16细类/域为主；跨域和父／负类检验一般扰动，属性是探索。每个SAE是同一个冻结1024宽、30000/ReLU-Top32模型资产，实际hook及参数哈希见frozen_plan。\n',
        '## 干预计算与原始残差\n',
        'decoder(hat)=b+Wz。定义原残差e=h−b−Wz。编辑得到z新后，注入h新=h+W(z新−z)=b+Wz新+e。W列不重新归一化，偏置不重复加；从原hidden出发，保留原残差。Attention输出在block27.self_attn.o_proj残差相加前；MLP输入在block27.mlp的实际输入、残差和post_attention_layernorm之后。后者不得再归一化才进MLP。权重全部冻结。原始h、重构误差、decoder列范数、实际注入向量及旧新坐标均保留。\n',
        '删除将组内z设0，其余不变。强弱操作先求原组r=L2(v)，w=(1−alpha)v/r+alpha t目标，再v新=r*w/L2(w)。t是8发现文本逐条归一化向量平均后再单位化。alpha固定0/.25/.5/1。原r=0时不救样本；若原某坐标为零而目标为正，编辑会招入成员，单列身份改变。没有重新执行TopK来把改变量截掉；这里控制的是目标潜在坐标，不预设再编码器输出完全等于它。\n',
        '## 对照质量：同数量不等于同扰动\n',qt,
        '固定其他成员按发现频率计数±2/64、正激活均值比[.5,2]逐坐标匹配。找不到合格成员就记录最近但不合格，而不是放宽定义。实际删除活跃数和候选不同时也不能通过主比较。随机范数参照使用相同数量的其他活跃成员、正组合系数，缩放使表征扰动范数相同；这是正向添加，不把它称作同方向删除。两种参照分别报告。\n',
        '强弱主对照在相同组中循环打乱发现典型分量；同侧典型及其他匹配成员是额外参照。按65点beta网格、20次二分匹配decoder空间范数，只看表征不看输出。每条控制范数比和是否在.9–1.1都保存；匹配失败不丢弃数据，但失去特异主判断资格。单个成员定位也已运行，只改发现典型差最大的那个成员；联合比单个强不等于已证明非线性交互。\n',
        '## 完整输出计分、词语排名和精确末层计算\n',
        '四候选cat./dog./car./bicycle.均2token，词和句号完整条件log概率求和，FP32 logsoftmax后FP64相加，无长度／先验校正。全词表rank=1+首词logit严格更高的词数；p_vocab以输出151936词为分母。p4以4完整序列分数softmax为分母。top20未列质量另存，不谎称只显示top20就是完整全词表分布。完整四候选分布、熵/KL、逐候选排名及top20对所有条件均保留。\n',
        '实际源代码中，最后block27的Attention输出之后只剩逐位置MLP、RMSNorm、head。对冒号的修改不能再流到下一个candidate位置的注意力K/V；K/V已由未改的block输入形成，之后没有另一层注意力。因此句号项保持不变。Attention干预重算残差加法→RMSNorm→MLP→残差；MLP输入干预直接改该归一化输入→MLP→原残差；随后统一final norm/head。预选F09猫／汽车、两接口、identity/delete/alpha.5的12次完整hook前向校验先于批量效应，最大完整分数差6.44e-6。每条原生基线也与主实验完全相等。\n',
        '## 主要判断和全部分支\n',pt,
        '主8项做Holm；家族均值由两子类组成，至少6个合格家族，4096bootstrap百分位区间和精确家族符号置换。不将14976条件或多个token当作独立N。删除同频强度匹配不足，所以主特异判定都是不足；这不抹去实际输出变化。所有替换组、单成员、剂量、属性和跨域是次分析，不救回主判断。\n',
        '## 不同类别的结果与剩余解释\n',
        'Attention动物alpha.5有小的同成员方向差，8家族一致，支持受限候选分数对当前方向的局部作用；其余同成员参照和跨域仍约束语义定向。Attention交通工具的反侧平均变化与预期相反；MLP动物未超过打乱，MLP交通工具有效样本不足。不同结果可能来自类别、字典／重构、典型模式代表性及样本能力，尚未以功效匹配唯一归因为不同概念组织。\n',ot,
        '无关域效应没有按范数独立匹配，所以此表只显示广泛敏感性，不能单凭大小比较得出类别专属性。动物Attention强弱目标文本四候选平均绝对变化约.01353，其他域约.04468；因此局部相对对照差不等于只动动物语义。MLP共同删除目标及无关文本的KL均约.63–.68，原大共同组存在广泛输出作用。主要候选仍16/16正确，不能说分类能力被破坏或概念被转换。\n',
        '## 具体例子、失败和图\n','[完整F09猫／汽车、两SAE、原新z与全部候选分数、top词、反例](casebook_cn.md)给出每个值与原文的对应。F09猫cat首词rank变好但相对dog略弱，说明排名和判别边际不是同一量。\n']
for p in sorted((R/'figures').glob('*.png')):detail.append(f'![{p.stem}](figures/{p.name})\n')
detail += ['每个家族散点保留两子类平均效应；正值才表示正确边际损失，反向点不删除。删除图中的最近其他名单明确为不合格；等范数正添加也明确命名。图面已检查，来源表在figure_provenance.json。\n',
           '## 数值、保真与追加诊断\n',
           f"14976条件的实际注入向量与decoder线性差映射最大坐标舍入{verify['max_decoder_delta_rounding']:.3g}；原残差代数闭合最大误差{verify['max_residual_preservation_error']:.3g}。离线完整候选概率复算误差6.15e-8，固定组范数误差2.85e-14。原始FP32总概率质量有舍入，KL最小约−1.66e-6，保留原值不剪零；它远小于主分数差。复算曾因用float64读取FP32 norm／剩余质量而失败，已改为重放原精度运算，未放宽1e-10/1e-12阈值、未改任何原响应或分析标准。amendments保留该工程记录。\n",
           '事后测量诊断重新编码固定F09 edited hidden：删除目标在一些例中确实为0，而重组目标与再编码数值并不完全一致。例如Attention猫反侧目标[28.9664,4.0809,3.1192]，再编码约[28.9919,3.7747,3.0773]。这限制“精确控制了自然feature状态”的说法，但不改变原已验证的decoder方向注入。该表未用于筛选、原阈值或主裁决。\n',
           '## 边界、认识更新与下一判断\n',
           '观察到的功能作用是这些SAE decoder方向在给定模型、最后层、冒号位置和强度下改变候选解码分数。稳定响应、必要性、特异作用和真实概念转换是不同层次。本轮支持一个很小的Attention动物方向差；不支持把所有观察组合当作语义单元或真实router分工。大共同组删除的普遍提升与无关词变化，使“共同响应越稳定就越必要”的直觉不再可直接沿用。科学接受、机制判断、关闭和下一研究者决策Unknown。\n',
           'AI建议：下一项决策应聚焦该小方向差能否在词面和位置受控、局部幅度和充分匹配下复现。这里不自动启动后续。\n',
           '[复算／索引](reproduce.md) · [冻结协议](protocol.md) · [数值检查](evidence/verification.json)\n']
(R/'detailed_cn.md').write_text('\n'.join(detail))
en='''# S07: combination interventions and native decoding

S06 was completed, independently audited and packaged before this supplement. All original inputs/caches/candidates/results remain unchanged. This intervention-unseen supplement uses original observationally exposed heldout families; no hidden semantic confirmation claim. Parameters stay frozen.

There is a small local effect of the Attention animal relative-pattern direction: opposite-patternalpha.5reduces correct-sibling margin by.01236nats averaged over8families; same-member norm-matched shuffled patterns reduce it by.00613. Difference.00623,95%family interval[.00135,.01340],Holm p=.03125. All16texts remain correct. Other-domain scores also move, so this is not a pure semantic conversion. Attention vehicle shifts oppose the predicted margin loss; MLP animal fails the comparator test and MLP vehicle has only5/8eligiblefamilies.

Deleting large common groups usually increases correct margins (.849/1.493nats for MLP animal/vehicle, respectively) and changes broad vocabulary distributions. Every common-group strict frequency/intensity deletion comparator fails matching, so deletion specificity remains insufficient. Equal-norm random additions are separately named, not misrepresented as matched deletions. Stable observational coactivation is therefore not equivalent to necessity for candidate discrimination.

Injection is h'=h+Wdecoder(z'-z), bias cancelled and original reconstruction residual retained. Common patterns and recruit/loss groups are selected only from the original64explicit discovery rows.96unchangedheldoutprefixes cover64explicit(alllabels) and32propertyfineconditions.14976actualconditions include deletion/count/norm controls, strengthalpha0/.25/.5/1, same-member shuffled/own-side/other-member controls and single-member localization. Report full2token candidate scores, correct margin, full-vocabulary first-word ranks/probabilities,top20+remaining mass,entropy/KL and normalized4-sequence probabilities.

The final-block tail is exact for these post-attention single-prefix-position edits, verified against12fullhookforwards (max6.44e-6nats). Period terms are invariant under this architecture-specific intervention. Every96nativebaseline matches S06exactly. Offline checks preserve original FP32 arithmetic, no tolerance relaxation. Edited latent targets need not equal re-encoded features; the claim concerns actual decoder-direction sensitivity, not unique natural mechanisms or MoE expert dispatch. Researcher acceptance and closure Unknown.

'''
(R/'summary.md').write_text(en+pt+'\n[完整中文解释](summary_cn.md) · [Detailed](detailed.md) · [Literal cases/ranks](casebook_cn.md) · [Reproduction](reproduce.md)\n')
(R/'detailed.md').write_text('# Detailed: S07\n\n'+en+pt+'\n'+qt+'\nThe complete owned execution ledger, figure explanations, all competing controls, raw cases, counterexamples and posthoc reencoding diagnostic are in [Detailed Chinese companion](detailed_cn.md). Exact frozen definitions are in [Protocol](protocol.md); all raw14976rows and full candidate rank/probability tables are portable. No new primary selection followed effects. [Reproduction and exclusions](reproduce.md).\n')
repro=f'''# S07 数据、运行和离线复算

- data/panel.jsonl：96条原始主留出文本／token，不另造更容易的prompt。
- data/selection.json：发现固定ID、典型强弱、计数／幅度范围及匹配细节。完整发现逐值仍在主包main/data的全稀疏z。
- results/conditions.jsonl：14976条件全部旧新坐标、实际有效数、构造范数、4完整候选分数、4全词表rank／概率、p4、熵/KL／top20质量。
- results/top20.jsonl：每条件实际top20词语字符串、ID、排名和概率；完整4候选分布都在conditions。没有保存／冒称包含完整151936项概率向量。
- results/actual_injection_norms.csv：实际FP32注入范数与构造范数舍入核对。
- data/key_injected_deltas.npz：固定F09部分实际1024维注入向量；所有条件向量较大，留在执行侧cache/all_injected_deltas.npz，路径及大小见large_files_index.json。
- cache/baseline_tail.npz：96条原末层input／attention／MLPinput／finalhidden／period项，体量小，可用于完整可信资产下重算末层。无模型／SAE权重。

离线小包复算：

```bash
python code/reproduce_portable.py .
```

合并包则在interventions目录运行，或传入该目录。主包仍可单独复算，原包hash保持。要重新执行全部推理需要冻结模型和两字典，其路径/sha/native loaders与依赖目录见frozen_plan.json；run.py拒绝覆盖已完成记录。CPU2threads；没有训练／GPU／云job。原始源脚本、协议freeze、校准、候选、数据和所有汇总均包含。S06文件和输入权重逐项hash通过，无永久写checkpoint。

完整执行目录：{R}。主执行目录：{MAIN}。所有大文件精确bytes/SHA在large_files_index.json；未包含文件绝不称已进包。研究者科学接受/关闭Unknown；无commit/push/外部发布。
'''
(R/'reproduce.md').write_text(repro)
for n in ['summary.md','summary_cn.md','detailed.md','detailed_cn.md','casebook_cn.md','reproduce.md','amendments.md','frozen_plan.json']:shutil.copy2(R/n,C/n)
for folder in ['figures','code','data','evidence']:
 (C/folder).mkdir(exist_ok=True)
 for p in (R/folder).glob('*'):
  if p.is_file() and (folder!='evidence' or p.suffix in ['.json','.md','.csv']):shutil.copy2(p,C/folder/p.name)
(C/'results').mkdir(exist_ok=True)
for n in ['primary.csv','family_primary.csv','control_quality.csv','offdomain_effects.csv','fixed_case_values.json','key_reencoding_diagnostic.csv']:shutil.copy2(R/'results'/n,C/'results'/n)
dump(C/'payload_manifest.json',dict(UTC=now(),execution_root=str(R),purpose='Selected curated text/candidate/actual edit/figure evidence; full conditions and large cache remain indexed execution-side',files=[dict(path=str(p.relative_to(C)),bytes=p.stat().st_size,sha256=sha(p)) for folder in ['data','results','figures'] for p in (C/folder).glob('*') if p.is_file()]))
daily=SYS/'daily_research_reports/1104/meeting_report/sae_feature_hierarchy_with_interventions_cn.md'
daily.write_text('''# 1104组会：先观察组合，再检验输出作用

主实验先完成384条、每域16家族、固定8/8和双SAE留出／措辞对照，之后执行14976个临时干预条件。原模型／SAE权重、文本、候选和主缓存均保留。

**认识更新一：组合不是“父类成员全部保留后再加成员”。** 同32预算内只有部分保留并更替，候选也有8/8和0/8。显式类内重叠高于跨类，但共同强弱的复现范围更窄；动物属性猫3/8限制语义判断，交通工具MLP固定列表只有5/8合格。

**认识更新二：稳定响应并不等于分类时必需。** 删除大共同组经常增强正确候选边际，MLP动物／交通约增加.849／1.493nats，也同步改变无关类别分布。共同组找不到完整同频同幅匹配，不能判定类别专属作用。

**认识更新三：Attention动物有小的局部强弱方向作用。** alpha.5朝反侧模式移动，8家族平均正确边际损失.01236nats；等范数同成员打乱.00613，差.00623[.00135,.01340]，Holm p=.03125。各主要条件仍16/16正确，支持分数敏感性，没有翻转概念。

**原始例子紧接结论。** F09原文“Asked what the survey was about, the researcher replied that it concerned a cat. The interview then ended. / Description:”。Attention共同#23899/#18691/#9522：原[29.234,1.816,2.736]，反侧.5后[28.966,4.081,3.119]；cat/dog完整S从−11.20893/−14.14577变为−11.17121/−14.07189。cat全词表rank174→167、dog2364→2234，但cat在四候选中的概率.94743→.94577，两词都增强时相对偏好仍可变弱。

机制直觉（AI）：同一共同组可能同时承载背景尺度与细微判别偏向，删大组和重新分配强弱会经过不同的非线性后续计算。当前数据没有把这个直觉升级为自然机制；方向注入只能识别本模型、hook、位置和强度下的输出作用。

实验分析：h新=h原+Wdecoder(z新−z原)，偏置抵消、原残差保留；发现集冻结组合/典型模式，留出执行删除、计数/范数对照、alpha剂量、同成员打乱和其他组对照。完整前向与末层重算最大分数差6.44e−6；完整两token计分、全词表排名/概率和top20都记录。原始匹配不足、反向、身份改变和超范围保留。

边界：词面复述、属性词线索、小样本和广泛输出变化仍在；没有真实概念转换或MoE/router分工证据。H1局部组合关联、H2条件组合关联和干预的局部作用分开报告。科研接受和下一决策Unknown。

'''+f'[主实验]({C.parent/MAIN.name}/summary_cn.md) · [干预Summary]({C}/summary_cn.md) · [完整反例／排名／分布]({C}/casebook_cn.md)\n')
print('S07_REPORTS',C,flush=True)
