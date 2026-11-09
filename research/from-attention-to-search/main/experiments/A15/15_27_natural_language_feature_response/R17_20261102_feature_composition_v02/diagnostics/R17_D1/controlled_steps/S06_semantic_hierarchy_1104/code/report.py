from common import *
import numpy as np,itertools,shutil
from scipy import sparse
def rd(n):return list(csv.DictReader(open(R/f'results/{n}.csv')))
def fmt(x,k=4):return 'NA' if x is None or x=='' else f'{float(x):.{k}f}'
def tab(headers,rr):return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(str(x) for x in row)+' |' for row in rr])+'\n'
pp=rows(R/'data/panel.jsonl');ix={p['id']:i for i,p in enumerate(pp)};sel=json.load(open(R/'results/selection.json'))['sites'];primary=json.load(open(R/'results/primary.json'));ver=json.load(open(R/'results/verdict.json'));beh=rd('behavior_summary');stats=rd('hypothesis_statistics');ov=rd('overlaps');joint=rd('joint_patterns');cov=rd('candidate_coverage');parts=rd('difference_decomposition');met=rd('row_metrics');values=rd('candidate_values');matched=rd('matched_candidate_baselines');geom=rd('shared_parent_geometry');wc=rd('wording_controls');events=rd('preactivation_events');cases=json.load(open(R/'results/case_selection.json'))
z={s:sparse.load_npz(R/f'data/{s}_all_z_csr.npz').toarray() for s in SITES}
def getstat(s,d,h,w='explicit'):return next(r for r in stats if r['site']==s and r['domain']==d and r['hypothesis']==h and r['wording']==w and r['split']=='heldout')
def primarytab():return tab(['SAE','大类','预测','估计','95%家族区间','可用/8','Holm p'],[[r['site'],r['domain'],r['hypothesis'],fmt(r['estimate']),f"[{fmt(r['ci_low'])}, {fmt(r['ci_high'])}]",r['eligible'],fmt(r['p_holm'])] for r in sorted(primary,key=lambda r:(r['site'],r['domain'],r['hypothesis']))])
bt=tab(['措辞','类别','同父二选一/8','四选一/8'],[[r['wording'],r['label'],r['sibling_correct'],r['four_correct']] for r in beh if r['split']=='heldout' and r['sibling_correct']!=''])
vt=tab(['SAE','大类','H','显式条件','跨措辞'],[[r['site'],r['domain'],r['hypothesis'],r['explicit_status'],r['cross_wording_status']] for r in ver])
rec=[]
for s,d in itertools.product(SITES,DOMAINS):
 rr=[r for r in cov if r['site']==s and r['domain']==d and r['split']=='heldout' and r['wording']=='explicit'];lns=sorted(set(r['list'] for r in rr))
 for ln in lns:
  rs=[r for r in rr if r['list']==ln];ids=sorted(set(r['feature_id'] for r in rs),key=int);counts={a:sum(r['event']=='True' for r in rs if r['feature_id']==a) for a in ids};random=next(r for r in matched if r['site']==s and r['domain']==d and r['list']==ln and r['split']=='heldout' and r['wording']=='explicit')
  rec.append(dict(site=s,domain=d,list=ln,member_count=len(ids),coverage_by_id='; '.join('#'+a+':'+str(counts[a])+'/8' for a in ids),members_all8=sum(n==8 for n in counts.values()),mean_event_coverage=float(np.mean(list(counts.values())))/8 if ids else None,matched_random_mean=random['random_mean'],valid_random_lists=random['valid_matches']))
table(R/'results/coverage_summary.csv',rec)
ct=tab(['SAE/大类','列表','留出各ID事件数/8','平均覆盖','匹配随机均值/有效组'],[[r['site']+'/'+r['domain'],r['list'],r['coverage_by_id'],fmt(r['mean_event_coverage']),fmt(r['matched_random_mean'])+'/'+r['valid_random_lists']] for r in rec])
pooled=[]
for s,d,w in itertools.product(SITES,DOMAINS,['explicit','synonym','property']):
 tt=[r for r in parts if r['site']==s and r['domain']==d and r['wording']==w and r['split']=='heldout' and r['pair'].startswith(d+'->')];den=sum(float(r['total_squared_norm']) for r in tt)/3
 if den:
  pooled.append(dict(site=s,domain=d,wording=w,paired_differences=16,retained_share=sum(float(r['squared_norm']) for r in tt if r['part']=='retained_amplitude')/den,recruited_share=sum(float(r['squared_norm']) for r in tt if r['part']=='recruited')/den,lost_share=sum(float(r['squared_norm']) for r in tt if r['part']=='lost')/den,total_squared_norm=den))
table(R/'results/pooled_energy_shares.csv',pooled)
pt=tab(['SAE','大类','共同强弱%','换入%','换出%','配对数'],[[r['site'],r['domain'],fmt(100*r['retained_share'],2),fmt(100*r['recruited_share'],2),fmt(100*r['lost_share'],2),r['paired_differences']] for r in pooled if r['wording']=='explicit'])
controlled=tab(['SAE','大类','措辞','H1关系重叠差[区间]','H2联合强弱投影[区间]','H2可用/8'],[[s,d,w,f"{fmt(getstat(s,d,'H1',w)['estimate'])} [{fmt(getstat(s,d,'H1',w)['ci_low'])}, {fmt(getstat(s,d,'H1',w)['ci_high'])}]",f"{fmt(getstat(s,d,'H2',w)['estimate'])} [{fmt(getstat(s,d,'H2',w)['ci_low'])}, {fmt(getstat(s,d,'H2',w)['ci_high'])}]",getstat(s,d,'H2',w)['eligible']] for s,d,w in itertools.product(SITES,DOMAINS,['explicit','synonym','property'])])

casebook=['# 逐例证据：完整F09、固定规则反例与行为失败\n','F09在模型响应前固定展示；反例按先非正、否则最弱正对齐选取。所有其他样本仍在data/panel.jsonl和完整CSV，不把展示选择当作检验。\n']
for s,d in itertools.product(SITES,DOMAINS):
 labels=DOMAINS[d];choice=next(r for r in cases if r['site']==s and r['domain']==d)
 casebook.append(f'## {s} / {d}\n\n发现集固定H2列表：`{sel[s][d]["H2"]}`。反例规则结果：{choice}。\n')
 for fam in dict.fromkeys(['F09',choice['counter_family']]):
  casebook.append('### '+fam+'\n')
  for w in ['explicit','synonym','property']:
   casebook.append('#### '+w+'\n')
   ps=[next(p for p in pp if p['family']==fam and p['wording']==w and p['label']==c) for c in labels]
   for p in ps:casebook += ['```text\n'+p['prefix']+'\n```\n',f"标签{p['label']}；显式标签词{p['explicit_label_word']}；目标位置0起{p['target_index_zero_based']}，末尾ID25；全部token `{p['token_ids']}`。\n"]
   ids=sel[s][d]['H2'];rr=[]
   for a in ids:
    vs=[next(r for r in values if r['site']==s and r['list']=='H2' and r['id']==p['id'] and int(r['feature_id'])==a) for p in ps]
    rr.append([a]+[fmt(r['z'],6) for r in vs]+[fmt(r['q'],6) for r in vs])
   casebook.append(tab(['ID']+[c+' z' for c in labels]+[c+' q' for c in labels],rr))
   for k in [1,2]:
    a=z[s][ix[ps[0]['id']]];b=z[s][ix[ps[k]['id']]];common=np.flatnonzero((a>0)&(b>0));new=np.flatnonzero((a==0)&(b>0));lost=np.flatnonzero((a>0)&(b==0))
    casebook.append(f"{labels[0]}→{labels[k]}：保留{len(common)}/32，换入{len(new)}，换出{len(lost)}；共同IDs `{common.tolist()}`；换入 `{new.tolist()}`；换出 `{lost.tolist()}`。\n")
behavior=rows(R/'data/behavior_all.jsonl');errors=[r for r in behavior if r['gold'] is not None and not r['sibling_correct']]
casebook.append(f'## 全部行为错误\n\n{len(errors)}条同父二选一错误；不删除、不重新选prompt。完整每候选token分数在data/behavior_all.jsonl。\n')
for r in errors:
 p=pp[ix[r['id']]];casebook.append('```text\n'+p['prefix']+'\n```\n'+f"{r['id']}，gold={r['gold']}，首选={r['sibling_choice']}，正确边际={r['sibling_margin']:.6f} nats；候选："+', '.join(c['label']+'='+fmt(c['total_logprob'],6) for c in r['candidates'])+'。\n')
(R/'casebook_cn.md').write_text('\n'.join(casebook))

intro='''本轮按三条路径阅读：①原模型行为与措辞／家族控制；②SAE成员组合及联合强弱；③功能与质量。本轮未做功能干预；数值和来源检查检验测量可信性。按用户本次要求，以下同时给出原始观察和有边界的AI认识更新，科学接受／机制判断／关闭仍Unknown。
'''
summary=['# SAE组合与语义层级：本轮认识更新\n',intro,'目的：用具体自然文本观察动物→猫／狗与交通工具→汽车／自行车的组合变化。H1看共同使用和成员更替；H2看同一共同列表的相对强弱。上下位关系只是本轮选定语言现象。\n',
         '## 1. 哪些认识得到更新\n',
         '当前最稳妥的更新是：组合的适用范围必须同时带上“类别、措辞、取样位置和字典”。发现集候选可以在新家族保持，也可以在同义词／属性改写中改变、消失或失去固定成员资格。两大类无需服从同一种组织规律。下面按事先固定的分支报告，不把可读性升级为因果或router分发。\n',vt,
         '这些状态分别判断显式条件下的局部预测和跨措辞预测。H1主统计只裁决“类内组合比跨类更接近”子预测；固定共同／换入／换出列表的实际复现见Detailed，不能由这个统计代替。H2主统计控制固定列表内成员身份；未满足资格的点仍画出，但只作描述。\n',
         '## 2. 决定性数据紧接结论\n',primarytab(),
         'H1的数值是每家族同域P–子1、P–子2、子1–子2三对平均Jaccard，减去同模板跨大类九对平均Jaccard。Jaccard=交集成员数/并集成员数。H2是兄弟类的固定列表L2归一化向量差，沿发现集平均差单位方向的投影；数值为正表示沿候选联合方向变化。8个留出模板簇构成区间；8项显式主检验作Holm校正。跨措辞均为冻结候选检查，不另选成员。\n',
         '![家族间差异和参照](figures/relations_and_joint_patterns.png)\n每点是一个留出家族。左图同时给Top32均匀／频率加权随机支持参照；右图展示联合强弱投影和反例，叉号保留不适用点。\n',
         '## 3. 从原文到真实成员\n']
for d,ls in DOMAINS.items():
 p=next(p for p in pp if p['family']=='F09' and p['wording']=='explicit' and p['label']==ls[1]);summary.append('```text\n'+p['prefix']+'\n```\n')
 for s in SITES:
  ids=sel[s][d]['H2'];ps=[next(p for p in pp if p['family']=='F09' and p['wording']=='explicit' and p['label']==c) for c in ls];xx=z[s][[ix[p['id']] for p in ps]][:,ids];qq=xx/np.linalg.norm(xx,axis=1,keepdims=True)
  summary.append(f"**{s} / {d}，F09**：固定成员`{ids}`；{ls[0]}／{ls[1]}／{ls[2]}原始激活分别为`{np.round(xx,4).tolist()}`；同一列表L2归一化后为`{np.round(qq,4).tolist()}`。它展示多个成员一起换强弱，不给单个ID命名为概念。完整三条原文和换入／换出ID见[逐例记录](casebook_cn.md)。\n")
summary += ['## 4. 竞争解释与语义资格\n',bt,
            '父类和负类只有偏好，没有编造猫狗／车骑行正确标签。所有384条均保留；错误文本及完整分数在casebook和原始数据。显式词复制、同义词线索和属性词自身差异仍在；属性描述并不等于只改变抽象类别。固定后缀统一了功能取样位置，绝对位置和长度仍记录，不据此声称位置已独立操控。\n',
            '![固定方向的措辞检查](figures/wording_control_joint.png)\n三个横坐标分别为显式词、同义词、属性描述；方向始终来自显式发现集，叉号表示固定成员条件不成立。图中同时给行为正确数和可用家族数，区分模式改变与检验资格不足。\n',
            '## 5. 解释与边界\n',
            '机制直觉假设（AI）：固定稀疏预算允许编码器的相对排序把一些成员挤出，同时保留成员可以重新分配强弱。这给“语境条件下的组合”提供一个可检验解释；它尚未被因果干预验证。全32支持不相同不妨碍固定小列表相同，但不能从小列表外推全字典身份受控。\n',pt,
            '上表分母是16条留出父子差的平方范数之和，只说明激活坐标中的变化来自哪里，不是语义或模型输出贡献。每条32活跃时换入数等于换出数来自Top-K结构。共同成员的变化、支持更替与字典重构残差分别保留。\n',
            'AI建议：下一项判断应是哪些类别／措辞条件允许稳定共同列表，及其变化能否由词面和位置解释；是否开展该后续由研究者决定。本轮停止，不启动H3/H4或router训练。\n',
            '[Detailed：全部做法、对照、失败与复现](detailed_cn.md) · [Protocol](protocol_cn.md) · [S02–S05定义核验](prior_audit.md) · [数据与复算](reproduce.md)\n']
(R/'summary_cn.md').write_text('\n'.join(summary))
detail=['# Detailed：H1/H2完整实验与竞争解释\n',intro,
        '## 目的、模型与实际步骤\n',
        '沿用同一official Qwen3-0.6B Base和原生Attention输出／MLP输入SAE。前者hook为block27.self_attn.o_proj残差相加前；后者是block27.mlp实际输入，经过残差相加和post_attention_layernorm。两字典各30000维、ReLU后Top32，不额外归一化。它们不是MLP前后因果对照，ID不对应。参数全部冻结；模型、SAE、router、分类读出和SVD均未训练或拟合。只拟合发现集联合差均值，冻结后投影留出。\n',
        '固定16个独立撰写的上下文模板，每个大类16家族，两个域共享模板所以独立单位是16个模板簇。F01–08发现、F09–16留出。每模板8类别×显式／同义／属性3措辞=24条，合384条。先冻结文本／协议／哈希，再算显式发现64条并冻结候选；之后才推理其余320条。类别短语跨模板重复，不能声称全句级内容完全独立或模型训练未见。没有按结果删样本。\n',
        '在统一Description:冒号取样。完整候选cat/dog/car/bicycle分别为[8251,13]、[5562,13]、[1803,13]、[34986,13]，均2token。对整串的条件对数概率求和，FP32 logsoftmax、FP64加总，无长度／先验校正。以每个细类每措辞8条为分母，父类／椅子／石头没有二选一正确标签。前向四个candidate lane都只取答案前冒号；前缀独立前向、候选lane和hook无改动检验证明没有读取未来答案。\n',
        '代码复用：原生SAE loader和S04取样／完整候选评分适配到384条与四候选，新写组合分析。训练复用索引已读，训练设施不使用。CPU2线程、4×128、GPU0、云job无。实际耗时、PyTorch版本和首尾哈希在evidence/*_complete.json。\n',
        '## 协议一致性和修订\n',
        '科学分析体与数据在第一次响应前落盘，原始freeze保留。selection最终控制台打印曾因numpy整数序列化失败；此时selection和gate已完整保存，修复仅影响日志，未重筛。amendments.md保留前后代码和曝光状态。若另有计算／排版修复，其记录同处；不改变阈值、候选或数据。旧S02–S05哈希逐项复核。\n',
        '## 行为和语义判断资格\n',bt,
        '每个“8”是留出家族数。每子类至少6/8才达到本轮语义资格；失败组仍描述表征。父类一般信息不足以指定子类。四选一提供跨域偏好补充，未作为主统计替代。具体错误和每token分数全部可审计。\n',
        '## H1：共同成员与更替\n',
        '逐对共同成员就是两个支持集合交集；三方共同是P、子1、子2三支持交集。发现固定列表是跨发现家族筛出的另一对象。主统计比较同域3对与跨域9对Jaccard，家族内六标签打乱保留每个真实稀疏向量、模板与总规模。均匀／频率加权随机支持只标出固定稀疏度和高频坐标带来的背景，不被当作独立语义标签参照。\n',primarytab(),
        '共同候选要求发现三方>=6/8，换入／换出候选>=4/8，按频率、幅度固定排序。下表完整列每个新候选在留出显式文本的事件数，包括0/8，不重新筛选；完整措辞细分见candidate_coverage.csv。频率分母为64条显式发现位置，是本面板使用频率，不是训练语料频率。\n',ct,
        '随机候选逐feature匹配发现活跃计数±2，256组，排除当前名单。若有效匹配0，比较不存在，不能把没有随机数据称为赢过随机。其余观察均值和随机区间在matched_candidate_baselines.csv；只作辅助，不能救回主检验。\n',
        '## H2：同一成员的联合强弱\n',
        'H2列表只选8发现家族P／两子类始终共同激活的成员，按平均z最多8个，不按兄弟差异挑成员。每文本q是该固定列表除其L2范数，原始z和整体L1／L2并列。兄弟差的发现均值单位向量固定后，留出差沿它投影；仅列表支持相同且至少2成员为正的配对进入主统计，至少6/8组才足够。其他完整列表差和动态配对共同成员差照样保存，但无固定成员语义资格。固定列表支持不等于全30000支持相同。\n',controlled,
        '多个成员的联合差向量、共同支持组合和发现选定4组成员间强弱顺序保存在joint_patterns.csv和rank_pairs.csv。强弱顺序比较的量为“子2内feature_b−feature_a”减“子1内同一差”，不把某个单独原子当成组合。随机H2列表也只用显式发现拟合方向，在相同留出条件上算投影，并报告每组可用样本数，见matched_joint_baselines.csv。\n',
        '## 类别相同、措辞变化与家族配对\n',
        'synonym替换为feline/canine/automobile/pedal cycle等；property改为meows/retractile claws、barks/wags tail、four wheels/engine/cabin、two wheels/pedals等，不出现六个目标类别词。它降低字面复制，仍包含语义强线索。父类nonhuman creature、conveyance和宽泛功能描述只是近似对照，不能单凭其成败归因抽象层级。不同家族共享类别短语，模板切换尚不是开放自然语料泛化。\n',
        '同类别显式→改写支持Jaccard逐家族在wording_controls.csv；同模板内的语义换类、跨域和两负类对照在overlaps.csv。家族错配固定为后一家族循环配对，不重新拟合方向，见family_pairing_controls.csv。原始固定功能末尾token相同，但改写长度及绝对位置变化仍是竞争解释，不声称已单独排除。\n',
        '## Top32、幅度和重构限制\n',pt,
        'native preactivation是encoder线性输出，ReLU后只保留32个。零值可能是原始响应非正，也可能正但排名不够。preactivation_events.csv逐换入／换出列出两侧pre和32名门槛；row_metrics.csv给每文本被截断正响应数。decoder不是正交基，z坐标能量份额不是输出能量、语义份额或因果贡献。decoder范数接近1使尺度补充接近；scale_sensitivity.json报告最大差而不只选好看的尺度。重构相对L2误差为||h−decode(z)||/||h||，完整逐样本保存；差异可能包含字典捕获能力。\n',
        '## 共享父类配对差的几何参照\n',
        '直接计算30000维子1−P与子2−P余弦；保留共享父结构，枚举每个三文本家族6个角色重排。若真实余弦同样可由共享父及三点几何产生，就不能命名共同语义方向。shared_parent_geometry.csv报告实际值及该结构参照的范围和均值。SVD本轮不运行：无需用总体方差轴代替真正配对差。S05的分母核验见prior_audit.md和独立复算表。\n',
        '## 反例、旧候选与图\n',
        '[完整F09及每接口／大类固定规则反例](casebook_cn.md)保留原文、全部token、具体成员z/q、换入／换出ID和行为失败。旧S03候选另在old_S03_candidates.csv全量报告，新名单不冒充旧名单。按预选F09展示不意味F09最好；同向时也显示最弱例并明确没有负例满足规则。\n']
for image in sorted((R/'figures').glob('*.png')):detail.append(f'![{image.stem}](figures/{image.name})\n')
detail += ['所有图均使用本轮冻结数据。家族散点保留个体差异，置信区间是8个模板簇的4096次bootstrap百分位，不是所有语言总体置信。图中分母32／固定列表L2／8家族分别标出，实际图面已检查并保存figure_review。\n',
           '## 裁决、竞争解释及仍不能说明的事\n',vt,
           '以上是AI按预登记操作标准的有限裁决。H1的局部关系重叠和具体成员事件分别理解；H2身份合格时才能讨论同成员强弱的候选复现。未复现不自动等于因果反证，资格或检验能力不足保留INSUFFICIENT。两大类差异首先是该模型／字典／措辞条件下的事实；目前没有功效匹配足以唯一归因“类别规律不同”。\n',
           '词面复制／属性提示、模板残余、改写位置、固定Top32排序、全局规模和重构限制尚未完全排除；发现选择与留出哈希门排除了本轮直接按留出重筛，但小样本选择不确定仍在。H1/H2都不说明feature唯一语义、真实专家路由、功能必要性、训练收益或广泛自然语义层级。H3、H4、真实router训练NOT_RUN_BY_PROTOCOL，仍在parking lot。\n',
           'AI机制直觉：相同字典中可能同时发生强度再分配和排序竞争。当前观察不足以判定模型内部实际采用哪种语义计算机制。科学接受、问题关闭和下一研究者决策Unknown。本轮任务完成后停止。\n',
           '## 覆盖与可复现入口\n',
           '资产核验、旧定义核验、384文本／token、行为、H1全支持、H2固定／动态组合、留出／改写、随机／打乱、重构／pre、反例、图、独立复算与小包均由evidence/coverage_ledger.csv登记最终状态。完整原始激活用稀疏CSR包含所有384×30000坐标零值信息；大缓存外留不等于丢样本。实际文件、大小和hash见output_manifest.json；包内容见PACKAGE_MANIFEST.json。\n',
           '[复算说明](reproduce.md) · [冻结协议](protocol.md) · [原始输入](data/panel.jsonl)\n']
(R/'detailed_cn.md').write_text('\n'.join(detail))
# English canonical records preserve the same numeric tables and boundaries.
en=['# SAE combinations and semantic hierarchy: S06\n',
    'Behavior/factor controls, representation combinations, then function/quality are kept separate. This round observes frozen dictionary coordinates; no causal intervention or router training occurs. These are AI operational verdicts under the registered rules; researcher acceptance and closure remain Unknown.\n',
    'Purpose: inspect member recruitment/loss/shared use (round H1) and joint relative strength (round H2) for animal→cat/dog and vehicle→car/bicycle. Sixteen authored frames/domain, shared across domains, form16 correlated frame clusters;8 discovery/8 heldout. Explicit/synonym/property variants plus chair/stone yield384 prefixes, all retained. Both native30000/ReLU-Top32 dictionaries use the same official Qwen3-0.6B Base but different final-block tensors and unrelated feature IDs.\n',
    'The bounded update is category/wording/dictionary-conditional organization. A successful explicit condition remains local unless frozen patterns and behavioral eligibility persist under lexical controls. The H1 primary contrast evaluates within-versus-cross-domain overlap, not the entire hierarchy hypothesis. H2 requires identical support on the fixed small list and>=2 active members; whole-dictionary support remains distinct.\n',primarytab(),vt,
    'H1 estimate is the mean3 within-domain Jaccards minus mean9 cross-domain Jaccards within a frame. H2 estimate is the sibling q difference projected along its frozen discovery mean direction; q uses exact fixed-list L2. Intervals resample8 family clusters4096times. Eight explicit primary tests use Holm.\n',bt,
    'Behavior is sibling constrained continuation and four-candidate scoring, not free generation. Parents/negatives have preferences, not fabricated fine gold labels. All candidates have2tokens including period; per-token log probabilities sum in nats with no correction. Synonym/property descriptions retain lexical cues, and absolute positions can vary.\n',
    'Common features and replacement patterns are reported separately from relative-strength changes. Equal recruitment/loss counts follow fixed32-positive supports. Coordinate squared differences and decoder-norm weighted activations are not semantic or output contributions. Matched random candidate failures remain explicit; shared-parent cosines have a role-reassignment structural reference. No classifier/SVD/model training. H3/H4 and real router work remain parked.\n',
    'AI mechanistic intuition: relative amplitude redistribution and encoder-rank competition can coexist. The current measurements do not establish native functional use. Lexical cues, remaining template/position effects, dictionary reconstruction and finite stimulus selection remain alternatives. One next researcher decision is whether any conditional fixed-list pattern merits an independently controlled lexical/position study; no such follow-up is started.\n',
    '[Complete procedure and audit](detailed.md) · [中文完整说明](detailed_cn.md) · [Literal cases and failures](casebook_cn.md) · [Protocol](protocol.md) · [Reproduction](reproduce.md)\n']
(R/'summary.md').write_text('\n'.join(en))
(R/'detailed.md').write_text('''# Detailed execution and lineage: S06

The complete numerical ledger, all conditions and literal cases are retained in the Chinese Detailed companion and raw CSV/JSON/CSR files. This canonical English entry supplies the exact computational definitions and links; it does not strengthen the bounded verdict.

Input identities: frozen_plan.json carries exact model/tokenizer/SAE/native-loader SHA values inherited from verified S04. Two separate final block27 hooks: Attention o_proj output before residual addition; actual MLP input after residual/RMSNorm. No encoder input normalization or decoder-bias subtraction. CPU2threads, FP32,4x128; gradients disabled.16frames x8labels x3wordings=384prefixes. F01–08 discovery, F09–16 heldout; a whole template and all related conditions stay together.

Order: protocol/panel/Anchor scope frozen first;64explicit discovery prefixes; candidate and direction hash gate; remaining320prefixes; all controls/heldout analysis; numerical replay; figures/reports/package. Native behavior scores four complete2token sequences with summed conditional natural log probabilities, parent/negative gold undefined. Capture at prefix colonID25 excludes candidate tokens; prefix-only/lane/noop checks verify causal independence. All384 rows retained, including behavioral errors.

For each support pair, I=intersection count, U=union count, J=I/U. Primary H1 averages3within-domain pairs minus9cross-domain pairs in the same frame. Six semantic labels are permuted within each heldout frame4095times, plus-one p. H1 common candidates have triple-active discovery count>=6/8; recruited/lost events>=4/8, fixed ranks and max8/6. Uniform and discovery-frequency weighted32-of30000 supports use512draws. Candidate random lists match discovery counts within±2,256requests, unmatched draws remain missing.

H2 features are triple-active in all8explicit discovery families, ranked mean raw z, max8. Fixed-list q=z/L2(z), zero norm undefined; raw/full/list scales are retained. Sibling q differences are projected onto the unit mean explicit-discovery difference. Same-list support and>=2positive features are required;>=6heldout eligible pairs permits the registered primary test. Exact family sign swaps form its null. Parent-child differences, pair-dynamic intersections, member strength orders and joint support are explanatory, not single-input router predictions. Matched random lists fit their direction only on discovery.

Eight explicit primaries use Holm .05.4096family-bootstrap percentile95% intervals describe only eight constructed heldout frame clusters. Cross-wording support needs positive lower intervals, behavioral>=.75per child and H2eligibility; contrary valid results limit support, missing behavior/support/power is insufficient. No result-driven reselection or threshold revision. Amended console-only serialization is documented; old source bytes and gate hashes are unchanged.

Full-coordinate paired differences split into disjoint retained-amplitude/recruit/loss supports; squared norms divided by full paired squared norm sum1. Pooled denominator=sum full paired squared norms. Mean component energies do not add across families. Shared-parent difference cosines are compared with6within-family role permutations. Reconstruction residual and all preactivations are retained execution-side; complete sparse activations, selected preactivations and full indexed summaries are portable.

Scientific/data/implementation audits and coverage status are in evidence/. All source paths/hashes/sizes are indexed by output_manifest.json. The accompanying Detailed contains all candidate counts, wording replications, failed cases, figure explanations and live rivals. No causal, functional, router, training-benefit or general semantic-hierarchy conclusion is authorized by the present associations. Researcher scientific acceptance and closure: Unknown.

[Complete Detailed](detailed_cn.md) · [Exact protocol](protocol.md) · [Summary](summary.md) · [Cases](casebook_cn.md) · [Reproduction](reproduce.md)
''')
repro=f'''# 数据与复算 / Reproduction

全部384条文本、标签、家族、模板、划分、token及位置：data/panel.jsonl。全部四候选逐token分数：data/behavior_all.jsonl。两套SAE所有384×30000激活坐标（零值隐式完整保存）：data/*_all_z_csr.npz。非零逐值表active_values.csv；全部支持交并／事件overlaps.csv；冻结候选selection.json；每候选z/pre/u/q/cutoff在candidate_values.csv。两域选中成员对所有384样本的完整预激活在data/*_selected_pre.npz。未选中feature的完整预激活和h留在下列大缓存，不谎称包内含全部pre。

主统计的离线复算只需Python/numpy/scipy：

```bash
python code/reproduce_portable.py .
```

原生重新推理需要外部冻结模型和SAE，路径/sha/native loader见frozen_plan.json，依赖目录/data/250010109/dependency_packages/hf_transformers_qwen3。原脚本为prepare.py、run.py discovery、select.py、run.py remaining、analyze.py、figures.py、report.py、verify.py；脚本拒绝覆盖既有结果。要完全重跑，复制源码到新执行目录，并先保留原协议及显式改动记录，不在原完成目录重跑。

实际大缓存：{R}/cache/discovery.npz 和 remaining.npz。每个包含行IDs、h、完整30000维z/pre、Top32索引/门槛、重构相对误差及decoder范数；确切大小和SHA由large_files_index.json登记。完整模型／字典权重不在包内。脚本和配置版本、哈希、软件／时间／CPU记录在evidence/*_complete.json及output_manifest.json。

当前报告是本轮观察和AI有限判定，科学接受Unknown；本地阅读副本不代表GitHub发布。没有commit/push/外部发送。
'''
(R/'reproduce.md').write_text(repro)
daily=['# 1104组会：SAE特征组合与语义层级\n',
       '目的：看成员如何换入换出，以及共同成员怎样搭配强弱，把几何坐标带回具体文本。预期H1为可复现成员关系，H2为可复现共同强弱；实际按类别／字典／措辞分别判定。\n',vt,
       '## 认识更新与紧接的原始数据\n',
       '组合模式需要给出适用语境。换一句表达后，原方向可以保留、改变，或因成员不再共同激活而无法检验；这三者对应不同认识。两个大类和两套SAE分开看，不拼成统一层级规律。\n',controlled,
       '## 从完整文本看组合\n']
for d,ls in DOMAINS.items():
 for c in ls:
  p=next(p for p in pp if p['family']=='F09' and p['wording']=='explicit' and p['label']==c);daily.append('```text\n'+p['prefix']+'\n```\n')
 for s in SITES:
  ids=sel[s][d]['H2'];xx=z[s][[ix[next(p['id'] for p in pp if p['family']=='F09' and p['wording']=='explicit' and p['label']==c)] for c in ls]][:,ids]
  daily.append(s+'，固定ID `'+str(ids)+'`，依次父／子1／子2原始z `'+str(np.round(xx,4).tolist())+'`。\n')
daily += ['## 实验分析与机制直觉\n',
          '每大类16家族、8发现／8留出；统一Description:冒号取样。显式词、同义词、属性描述和两负类都保留。H1算逐对支持交并、三方共同、换入／换出和同模板跨大类；H2用发现固定共同列表L2归一化，联合方向只在发现拟合，留出不重选。原模型先检查完整二选一／四选一，不删错误。随机支持／频率匹配、家族内标签打乱、同义／属性和共享父结构参照分别检查竞争解释。\n',
          'AI机制直觉：固定Top32会使排序竞争与强弱再分配同时出现。它是下一步可检验的解释，不是本轮确认的语义计算机制。\n',
          '边界：显式词复述、属性词线索、改写长度／位置、重构限制和小样本仍在。组合可区分不等于router已学会分发。H3/H4和router本轮未运行。科研接受和下一决策由研究者保留。\n',
          f'[完整中文Summary]({C}/summary_cn.md) · [详细报告]({C}/detailed_cn.md) · [具体反例]({C}/casebook_cn.md) · [图]({C}/figures)\n']
day=SYS/'daily_research_reports/1104';(day/'meeting_report').mkdir(parents=True,exist_ok=True)
(day/'meeting_report/sae_feature_hierarchy_cn.md').write_text('\n'.join(daily))
index=day/'README_cn.md';entry='\n- [SAE组合与语义层级：问题、模型、结果、边界、决策及原始证据](meeting_report/sae_feature_hierarchy_cn.md)；结果包：`20261104_SAE_hierarchy_analysis.zip`。\n'
if not index.exists():index.write_text('# 1104研究阅读\n')
if 'sae_feature_hierarchy_cn' not in index.read_text():
 with index.open('a') as f:f.write(entry)
for n in ['summary.md','summary_cn.md','detailed.md','detailed_cn.md','casebook_cn.md','prior_audit.md','reproduce.md','amendments.md','frozen_plan.json']:shutil.copy2(R/n,C/n)
for folder in ['figures','code']:
 (C/folder).mkdir(exist_ok=True)
 for p in (R/folder).glob('*'):
  if p.is_file():shutil.copy2(p,C/folder/p.name)
# Selected evidence exception, with an explicit manifest; full raw CSV/CSR stays execution-side and in portable package.
(C/'results').mkdir(exist_ok=True);selected=['hypothesis_statistics.csv','behavior_summary.csv','verdict.csv','coverage_summary.csv','pooled_energy_shares.csv','family_effects.csv','scale_sensitivity.json']
for n in selected:shutil.copy2(R/'results'/n,C/'results'/n)
dump(C/'payload_manifest.json',dict(UTC=now(),purpose='Selected small tables and figures for this bounded result, source owner remains execution',execution_root=str(R),files=[dict(path=str(p.relative_to(C)),bytes=p.stat().st_size,sha256=sha(p)) for folder in ['results','figures'] for p in (C/folder).glob('*') if p.is_file()]))
print('REPORTS_WRITTEN',C,flush=True)
