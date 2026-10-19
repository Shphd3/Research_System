import json,csv,os
from pathlib import Path
P=json.load(open(Path(__file__).resolve().parents[1]/'config/frozen.json'))['paths'];R=Path(P['run']);E=Path(P['experiment']);read=lambda x:list(csv.DictReader(open(x)))
def table(h,rr):return '\n'.join(['|'+'|'.join(h)+'|','|'+'|'.join('---' for _ in h)+'|']+['|'+'|'.join(map(str,r))+'|' for r in rr])
# Add the decisive conditional-amplitude observation without creating a new hypothesis.
cn='''\n激活画像还显示：EVAL正激活事件池中，低/高频组的z中位数为0.02606/0.01792，路由幅度a为0.14808/0.11566，而第28层c为0.01938/0.02290。它们分别基于131652/8997930个正事件，不能当成各feature等权分布。低频并非在这三种量上都更弱，不能用z大小直接解释未接收，也不能用末层c冒充路由a。[图2](figures/figure2_conditional_amplitudes.png)、[完整分位/支持](tables/conditional_amplitudes.csv)。\n'''
f=E/'detailed_cn.md';s=f.read_text().replace('第28层重建EVAL raw相对平方误差',cn+'\n第28层重建EVAL raw相对平方误差');s=s.replace('实际26个唯一条件对×seed记录','实际26个唯一（条件对，seed）记录');f.write_text(s)
f=E/'detailed.md';s=f.read_text().replace('## 5. Independent target scene','EVAL positive-event pooled low/high medians are z=.02606/.01792, routing a=.14808/.11566, layer28 c=.01938/.02290, with131652/8997930events. These are event-pooled rather than equal-feature distributions: low frequency is not uniformly smaller amplitude and the three quantities cannot substitute for one another.\n\n## 5. Independent target scene');f.write_text(s)
windows=json.load(open(E/'evidence/fixed_windows.json'));scores=read(R/'tables/fixed_text_score_contributors.csv');ranks=read(R/'tables/low_window_rankings.csv');docs=['# 固定文本、评分主要项与低频贡献片段','','选择发生在学习前：按源顺序取首个完整64token且至少2个L原子命中的窗口；不根据路由胜负或loss挑选。h与z只依赖当前token及模型可见前文。右侧文字只是事后阅读辅助。源bin没有可验证原文档边界，不拼接不同窗口。训练前后的原z/c已逐项核对不变。','']
for w in windows:
 split=w['split'];docs += [f'## {split.upper()}：上下文{w["context"]}，文件偏移{w["start"]}起','','源文件：`'+w['source']+'`。','显示feature ID：'+', '.join(map(str,w['feature_ids']))+'。','', '64token原文：','','`````text',w['text'],'`````','','完整可见前文、原token ID与raw token片段保存在[固定窗口JSON](evidence/fixed_windows.json)。','']
 # First token, all groups and scores; full64-token table remains CSV.
 position=w['start'];token=w['raw_tokens'][0];docs += [f'### 同一首token（偏移{position}，raw片段{json.dumps(token,ensure_ascii=False)}）的八组竞争','','每格为“分数；主要feature ID前三项；最终去向”。a是原14层范数和加权激活，不是第28层c。S1/S2/S3各自有不同定义，数值不跨评分直接比单位。','']
 for g in ['T','R11']:
  rr=[]
  for e in range(8):
   cells=[]
   for sc in range(4):
    x=next(q for q in scores if q['split']==split and int(q['position'])==position and q['grouping']==g and q['score']==f'S{sc}' and int(q['expert'])==e);cells.append(f'{float(x["group_score"]):.5g}；ID '+','.join(x['top_feature_ids'].split(';')[:3])+'；→'+x['selected'])
   rr.append([e]+cells)
  docs+=['#### '+g,'',table(['名单组','S0','S1主方案','S2','S3'],rr),'']
 docs += ['### 所选低频feature的前5个贡献位置','','各feature按该固定窗口全部64位置的c从大到小排列；0贡献位置仍可出现在不足5个正命中时，不补造正例。前后2token只限同一缓存上下文。','']
 rr=[]
 for x in ranks:
  if x['split']==split and int(x['rank'])<=5:
   esc=lambda q:json.dumps(q,ensure_ascii=False).replace('|','\\|')
   rr.append([x['feature_id'],x['rank'],x['position'],f'{float(x["train_p"]):.5g}',f'{float(x["z"]):.5g}',f'{float(x["c28"]):.5g}',esc(x['previous2'])+' / '+esc(x['current'])+' / '+esc(x['following2'])])
 docs+=[table(['feature','排名','源位置','TRAIN p','z','第28层c','前2 / 当前 / 后2（后文只供阅读）'],rr),'']
docs+=['完整64位置×所有命中feature：[feature_text_profiles.csv](tables/feature_text_profiles.csv)；完整八组/四评分各主要项：[fixed_text_score_contributors.csv](tables/fixed_text_score_contributors.csv)。这些例子用于读懂竞争，不授予单义语义标签。']
(E/'text_profiles_cn.md').write_text('\n'.join(docs)+'\n')
explanations={
'figure1_fixed_activation_profiles':('频率、共享激活和末层贡献是否是同一件事？','左侧TRAIN频率p用正数对数轴；中是log1p(z)，右是log1p(c28)，行同一feature，列同一token，两个split按同一量共享色阶。','低频项能有突出激活；z图与末层幅度图并不相同。','展示feature按窗口最大c选择，不能估计全体语义或因果作用。'),
'figure2_conditional_amplitudes':('低频feature激活时是否普遍更弱？','全TRAIN/EVAL正激活事件池的中位数和四分位范围；三个面板分别z、c28、a，纵轴对数。','EVAL低频z/a中位数反而较高，c28稍低。','按正事件汇总，不是各feature等权；不同量不能互代，支持数在源表。'),
'figure3_train_low_position_ranks':('TRAIN所选低频项由哪些位置贡献？','每小图一个feature，横轴64位置的贡献排名，纵轴c；前5橙点对应文本表。','很多所选项在单个或少数位置突出。','窗口内描述，0值保留，不由尖峰推出语义。'),
'figure3_eval_low_position_ranks':('EVAL所选低频项由哪些位置贡献？','同TRAIN图，但使用独立固定EVAL窗。','出现稀疏局部峰，全部64排名仍保存。','不把所选强激活文本当总体典型。'),
'figure4_train_same_text_scores':('相同TRAIN文本换评分，去向如何变化？','上T下R11，每列S0/S1/S2/S3；色为log1p评分，白点是最终专家。','T的S0/S2集中，S1/S3明显分散。','不同评分单位与色阶不同，只同一规则内读；不是模型层或解码热图。'),
'figure4_eval_same_text_scores':('相同EVAL文本换评分，去向如何变化？','同TRAIN图，固定EVAL窗；八组主要feature见文本附录与CSV。','T的组校准能改变选择，R11原本就更分散。','不凭这64位置评价整批分发或学习。'),
'figure5_dispatch_outcomes':('负载、目标接收与零接收是否一起改变？','左负载分母全部65402位置，中每个低feature接收率再宏平均，右固定964零接收数。','S1接收33.4%/零5，S2为0%/零964，S3为41.7%/零0。','接收不等于同频，不等于学习收益。'),
'figure6_actual_frequency_profiles':('实际专家中还含哪些高频信息？','横轴9615项按TRAIN频率降序，包括Top10；纵轴专家，色为实际q∈[0,1]，空专家NA。','高频信息仍随完整输入进入，主体低q在统一线性色阶下较暗。','黑色低q应与图14和完整数值表合读，不能当成没有该信息。'),
'figure7_primary_learning_curves':('S1接收改善是否带来主比较学习收益？','A/B/C，两个panel整体和M_L，横轴累计有效预测位置；实/虚线seed11/22。','各曲线上升，B比A更差、比C稍好。','固定epoch3终点；低频宏指标不是低频知识掌握。'),
'figure7_learned_references_learning_curves':('本设置λ=.01均衡项是否改善学习？','仅D/E两参考；门乘数为选中softmax概率。','E终点比D更差，两者都差于原基座。','只裁定该结构/强度，不推广所有均衡损失。'),
'figure7_expanded_fixed_learning_curves':('四种评分和两名单的所有结果是什么？','全部8个固定条件×2seed；颜色条件，实/虚线seed。','T的S0/S2较少恶化，R11多种评分彼此接近；仍全差于基座。','不是从扩展中选最好再宣称独立主方案。'),
'figure8_primary_paired_differences':('预登记主门槛是否满足？','点为B−A或B−C；线段1000次配对EVAL块95%区间；负差更好。','B−A为正，B−C为负；联合要求失败。','区间不是文档独立总体显著性；两seed范围有限。'),
'figure9_same_input_expert_probes':('同一输入换expert会改变预测吗？','左强制门1的绝对NLL，右替换expert但保留自然门后的差值。','输出/损失有差异，撤回旁支通常更接近原基座。','expert ID跨策略不代表功能对应，不能由差异贴语义标签。'),
'figure10_target_assignment':('暂未用于背景更新的目标交给谁更安全？','左目标收益before−after对旧损害；右各expert绝对目标NLL随0/8/32步。','所有终点收益为负且旧损害>.01，安全候选为空。','该条件留出不是真正新知识；expert6原始最好但不安全，不能称归属成功。'),
'figure11_parameter_spectra':('参数几何变化是否与初始化区分开？','三行初始/终点/ΔW，三列gate/up/down，前16奇异值按8expert取中位数；全谱/范数另存。','S0很多expert未更新，分布中位数可能接近初始化或0。','奇异值不是方向，ΔW包含衰减，谱平不是容量高。'),
'figure12_response_spectra':('响应幅度与形状是否应分开？','同探针输出按位置中心化协方差；左绝对eigenvalue，中除完整trace，右所有expert的trace。','不同条件的响应能量和形状各异，零响应项在归一化中NA。','同输入几何描述，不构成功能或学习成功条件。'),
'figure13_group_to_actual_expert':('名单分组是否转化为实际分发？','行是原feature名单组，列实际expert；每格占该组全部feature命中事件的百分比。','S1/S3改变实际去向，但有组外共入。','一个token可贡献多个feature事件，行不是互斥token群。'),
'figure14_expert_frequency_distributions':('每个专家内真实频率分布是什么？','正q对数横轴；纵轴所有9615项中q≤横轴值的比例，q=0纳入起始比例；空专家单列NA。','列表分组未让完整输入自动同频；各expert零暴露与正频率形状差异可见。','不是只看正命中的条件分布，不由曲线断容量。')}
figs=['# 图外读图说明与术语','','所有图均有PNG、可放大的SVG和PDF；数字源表在tables，来源/文件SHA在curated_evidence_manifest.json。图中expert ID只在本模型内标识参数块，不能自动跨策略当成语义对应。','','## 先分清对象','','- feature ID：冻结CrossCoder字典原子的稳定编号，不是词、主题或模型层。','- TRAIN/EVAL：训练统计/监督侧与留出评价侧。它们来自不同bin，文档独立性未知，EVAL此前已查看。','- token位置：用当前token及其可见前文形成h，预测下一token；next/following片段只供事后读文本。','- z：14层联合编码得到的共享门控激活，不是每层独立激活。','- p_i：TRAIN命中频率，正激活位置数/有效位置数。此处p不是以前跨层解码占比图中的p分布。','- c28：z乘第28层decoder向量L2范数，单位为原CrossCoder的TRAIN中心化vector-RMS坐标幅度；不是有利任务的证据。','- a_i(t)：z乘原14层decoder范数和的路由幅度。表字段assigned_reception_a是旧字段名，指接收率，和这个a不是同一量。','- m_i：TRAIN中该feature激活时a_i的均值；μ_e：TRAIN组评分S0均值；均冻结。','- S0/S1/S2/S3：原评分/组级校准/条件幅度校准/频率与条件幅度校准，不叠加。S1是事前主方案。','- T/R11：固定频率组织名单/固定随机组织名单，候选与人数相同。R11的11是名单种子，不等于两模型种子构成两个随机名单。','- 接收率：feature命中时，被送入其名单指定expert的比例；宏平均是先算每feature再等权平均。','- q_i,e：实际送入expert e的位置中feature i命中的比例。与p的分母不同；无输入expert为NA。','- NLL：正确下一token负对数似然，单位nat/token，越低越好；M_L是964低频feature各自命中NLL的等权平均。','- Δ：后者按图注指定的差值；学习比较负更好；目标收益用before−after，所以正更好。','- W/ΔW：专家原矩阵/相对配对初始化变化。singular value是奇异值大小，不能说明方向相似；eigenvalue是响应协方差特征值。','- NA：按定义不可估；0是真实零。不能相互替换。','','## 每张图的问题、读法、观察与边界','']
for name,(q,how,obs,bound) in explanations.items():
 figs += ['### '+name,'',q,'','![图](figures/'+name+'.png)','',f'读法：{how}',f'观察：{obs}',f'边界：{bound}','',f'[SVG](figures/{name}.svg) · [PDF](figures/{name}.pdf)','']
(E/'figures_cn.md').write_text('\n'.join(figs)+'\n')
# Public audit, distinct from private reasoning and human scientific approval.
f=E/'reasoning_audit_cn.md';s=f.read_text();s+='''\n## 完成后审计\n\n|主张|证据|竞争解释|边界与决定|\n|---|---|---|---|\n|S1确实修复部分选择尺度|低频接收0.0023%→33.4033%，零960→5；地板触发0|单个强响应、共现与组尺度仍共同决定去向|支持具体分发变化，不认定已同频|\n|S1改善学习|B−A低频+0.1807/+0.1853，B−C−0.0326/−0.0256|更多参与expert造成更强TRAIN拟合，更新幅度/分布差异|联合H2不支持；相对随机较好不等于超越基座|\n|专家功能有差异|同一探针强制专家输出/NLL/替换代价不同|随机初始化、曝光与幅度都可能造成差异|只说本模型响应差异，不授语义功能或容量|\n|新目标应送频率所属专家|8份适配均目标恶化，旧损害均>.01|当前适配本身不安全，未能只隔离归属选择|无安全候选，不能把原始最低expert6当成功|\n\n工程与计量：所有20条件完整、初始等价与梯度/恢复通过、数据顺序/位置/TB核对、原z/c复读不变。独立文档泛化、训练总体稳定性和频率中介仍未建立。公开解释是AI_PROPOSAL；研究者科学批准Unknown。下一步只提出一次共享小更新强度的A/B/C复核建议，未执行。\n''';f.write_text(s)
print('text, terminology, figures and final reasoning audit complete')
