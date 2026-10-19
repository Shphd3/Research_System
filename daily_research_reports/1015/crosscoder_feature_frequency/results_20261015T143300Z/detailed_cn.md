# Detailed：缓存内特征关系分组与频率

[English](detailed.md) · [结果摘要](summary_cn.md) · [五图](figures_cn.md)

## 0. 结果及资格先读

实验ID：CC_FEATURE_FREQUENCY_20261015T143300Z。研究对象是最终14层/F16384字典在固定DCLM窗口的特征事件，不是模型训练或专家学习。

执行与描述性交付完成，完整H1的证据资格为 **BOUNDED / INSUFFICIENT**。H1a已有单bin分组复核读数；H1b全体均值匹配统计不可估计；随机化资格失败，B99正式校准NOT RUN。H2 NOT RUN。科学判断及是否关闭问题均为研究者所有，当前Unknown。

主发现：候选池15,666个；D/V非单成员组186/185；平均一对一成员Jaccard0.5483796213。q20产生65/61组及0.5424153390。输入未命中/唯一/多组为34.6626%/39.5150%/25.8223%。其意义、对照缺口和边界见Summary，不能将组数或平均重合解释为机制或学习收益。

## 1. 对象、公式与统计单位

feature是固定潜坐标，事件a_i(x)=1[z_i(x)>0]，z是缓存中已通过固定TRAIN范数加权阈值的非负激活。N为某侧有效位置数，n_i为命中数，n_ij为同一位置共同命中数；p_i=n_i/N。原始训练BatchTopK的256是batch平均预算，不是每个位置固定256。

二元相关phi是共同命中超出边际独立背景的标准化读数：

\[
\phi_{ij}=\frac{Nn_{ij}-n_in_j}{\sqrt{n_i(N-n_i)n_j(N-n_j)}}.
\]

分母为0则不可估计。组内离散度是在V对固定D组成员的log10频率求总体标准差（ddof=0），单位dex；越低越同频。p=0或1的成员按既定规则不可估计，不删除或加epsilon。

观测单位是位置；独立原始文档身份Unknown。频率和输入比例区间按旧连续块重采样1000次，明确条件于块独立假设。随机组分布范围不是数据采样置信区间；固定组重采样不是重新发现稳定性。

## 2. 设计、授权和实际符合性

原Anchor和旧Protocol正文均保留。[R0/R0.1执行登记](../execution_amendment_cn.md)记录本轮显式运行授权与读新端点前的参数/采样修正。registered_config.json当前SHA256为569b8ee9595a4455fd98f8a6912665b282f02925018186a180071bacafa7e7d9。

| 项目 | 实际状态 | 对证据的影响 |
|---|---|---|
| 字典/数据/cache | final14/F16384；旧完整VAL及D/V；严格访问通过 | 输入绑定符合，不等于文档独立或科学批准 |
| 科学范围 | 缓存关系/频率/输入映射；0训练、0新编码 | 不测H2 |
| 主关系/分组 | phi；mutual top10，gamma1，NetworkX2.6.3贪心模块度 | 无频率距离目标，但phi的内生偏好仍需null |
| 候选支持 | D命中≥100、≥10个旧D块、共同命中≥10 | 工程可靠性操作点，非文档支持或误差保证 |
| V候选 | 固定D池；保持不可估计成员身份 | 不据V回调 |
| 采样修正attempt0 | 早期仅边际bootstrap/候选准备即停止；无图/端点产出，记录保留 | 旧accepted-step控制代码不用于结果；正式使用R0.1固定proposal版本 |
| 配对随机组 | 同池同size，200次；均值匹配D-only成员交换±0.1dex | 保留全部组及资格不足；相关MCMC不当精确独立样本 |
| 控制预算失败 | 44/186组未合格，不改预算重抽 | 全体T_b为NA，不以142子集救回 |
| null | 每侧128context×32位置；两链1/2/4/8 accepted/M诊断，4个完整资格端点 | 行列守恒检查通过；T_b不可估，资格失败；B99未运行 |
| 多重比较 | 未产生合格主p值，不计算Holm | 不声称显著或FWER保证 |
| 图3展示 | 固定300ID，组大小排序+组内hash轮询 | 每组仅1或2个点，不能展示完整组内纹理；自相关对角mask与颜色饱和属排版修订 |
| 图4展示 | 主图D最大20组；全186组分页PDF和完整表 | 不隐藏NA或只报可估组 |
| 输入样本 | 随机hit context→其中hash位置；高score按成员数→位置ID | 非均匀token样本；不是按z幅度排序，右文仅阅读辅助 |
| 原文档确认 | 未执行、映射缺失，两侧已有暴露 | 完整H1独立文本部分不足 |

当前没有确认Focus/problem_key；本次用户明确要求的有界分析照常完成，不替研究者创建科学状态。旧草稿中“先不执行”已被本次指令覆盖，独立性和可估计条件没有被覆盖或放宽。

## 3. 准确输入和代码

执行根E=/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder；旧分析R=E/analysis/feature_relation_phase1/20261013T173130Z；本次输出W=E/analysis/feature_frequency/20261015T143300Z。这些缩写仅用于下面追溯；可读完整路径见[资产核对](../assets_checked_cn.md)。

- Base/tokenizer revision da87bfb608c14b7cf20ba1ce41287e8de496c0cd，冻结Qwen3-0.6B Base。
- CrossCoder E/runs/formal_14layer_batchtopk_a22/checkpoint_000999997440.pt，checkpoint SHA09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628，观察one-based2,4,…,28；本轮未加载权重。
- Cache注册ID representation_crosscoder_qwen3_final14_f16384_val10485760_phase1_20261013t173130z；固定TRAIN EMA cutoff0.051281172782182693及中心化vector-RMS；16contexts/Base、1024eligible/coder、SDPA、BF16/FP32历史推理定义不变。
- 全量N10,485,760，D5,238,097，V5,247,663；2,669,034,642非零，640CSR chunk；旧D/V total0/1.npy全F×F int64直接复用。
- 完整当前输入访问记录W/asset_access_preflight.json；代码冻结W/code_snapshot，实际命令及stage log位于W。core源码SHAae3567e7e24052e54e09c70cc7ccea34ce9c509fbe166cbb121e84509c904dc3，启动/当前/快照一致。

具体算法与阈值见R0/R0.1，不再重复所有注册表。复用CSR、位置key和旧共同计数；适配关系/组/control/文本映射；不复用旧方向DAG层级作为本次规律定义。未改模型、旧结果、训练配置或历史记忆。

## 4. 主要证据账本

| 问题/读数 | 原始来源→计算 | 实测值 | 资格与解释 |
|---|---|---:|---|
| 频率排序是否一致 | R/feature_frequency.npz→W/frequency.csv→descriptive_digest | Spearman0.9979156 | 单bin描述；相关高不证明独立文本或语义 |
| 零命中 | 保存边际→逐feature侧标记 | D353，V393，整窗290 | 窗口未见，非永久dead |
| 正频率范围 | V有效边际/NV | 中位0.37956%，最大99.26360% | 仅V正命中成员，中位分母不含393零项 |
| 主图/组 | 全pair counts→positivephi/mutualq10→一算法 | D34,757边/186非单成员组；V34,743/185 | 15,666候选，13,807D组成员，其余1,859singleton |
| 成员复现 | 固定D/V组→Hungarian最大Jaccard匹配 | T_a0.5483796213 | 有向D复核读数，无正式nullp |
| q敏感性 | 仅q10→20 | 65/61组；T_a0.5424153390 | 组尺度不唯一，不能事后挑q赢家 |
| 同size随机对照 | 全组V logSD对随机分箱 | 0.35331 vs0.67565dex，差−0.32234 | 描述性，未排除均值/phi偏好 |
| 主均值匹配T_b | 全186组对D均值匹配组V评价 | NA；142组可估/成员48.37% | 44组缺控制资格，不删除；可估子集均差−0.21516仅选择后描述 |
| sample观察 | 固定hash每侧4096位置，重跑全部步骤 | P6750；T_a0.1953114；T_bNA | 样本范围，不能对旧fullgraph给p |
| swap资格 | 两链全F二元2×2，包含拒绝自环 | 行列守恒全通过；资格NOT_QUALIFIED | 失败在未定义T_b；非边际破坏的证据；99formaldraws=0 |
| 组到输入 | 冻结D门槛→全V事件扫描 | none1,818,978；unique2,073,616；multiple1,355,069 | 分母5,247,663；三项合计完全一致，不强制top1 |
| 案例 | 原位置key+CSR事件+冻结tokenizer ByteLevel解码 | 176组×10=1,760 | 10组无法命中规则；随机context不是uniformtoken |

固定组SD的条件性块bootstrap结果另存W/main/dispersion_uncertainty.json。主均值匹配效应区间不可估；不把随机组95%范围称为主效应95%CI。

## 5. 失败分解与解释

均值匹配缺口不是V真实组频率缺失：全量186组的真实V离散度都能估计。15组因10,000提案上限无法留足20份对照，29组在固定10×组大小burn-in中接受交换不足组大小；两类本次不重合。这是设计预算/资格限制，不能用“数据没有同频”解释。所有组/失败原样保留，不放宽预算、改容差、挑seed或丢困难组。

尤其10,000与大组留样规则未做完整预检查：当size>333，30×size>10,000，所需burn-in+20draws必然超过预算。下一轮应在未见新结果前修复这项联动，预先验证控制能覆盖预定组规模。不得把本轮子集优势补写成全体H1b通过。

两链的4次完整资格T_a约0.03494–0.04080，观察sample为0.19531；这只是资格诊断，四次不是99次正式随机分布，accepted-count时刻也不是正式fixed-proposal留样。因此不能计算p或宣称已剔除稀疏约束的结构规律。后续formal拒绝自环处理已修，但本轮未运行。

H1a的成员可复核与q敏感性共同说明有对象可看，不能说明组数天然；H1b只有同size描述优势，无法裁定算法偏好；输入多组命中表明top1映射限制。三者不建立语义组合、因果关系、common功能或学习好处。AI建议一个下一决策见Summary，研究者尚未确认。

## 6. 计算与独立核验

主图+q20约186.03秒；null资格约279.66秒，记录峰值RSS2.964GiB；输入两遍CSR与文本约542.66秒。各阶段重叠，不能简单相加当墙钟账单。使用本机CPU，GPU未使用，0新模型前向、0训练。cpu-only-local计算在60分钟范围内；主进程地址空间32GiB硬限、4CPU affinity、BLAS1。全任务聚合峰值RSS没有完整连续测量，不能把null峰值当整项任务峰值。

core合成资格9项通过，null有手算共同计数/行列守恒/枚举提案转移对称测试。独立检查完整两侧矩阵对角与全部69,500条主图边的count/phi；44个固定端点邻居独立排序，完整P分区与186组Jaccard重算均通过。core与配置前后SHA相同。文本解码和位置/完整可见前缀与旧118条记录逐一一致；生产input额外10例一致。详见W/independent_core_checks.json和各stage selftest。

这些是工程/来源核验，不是独立科学复制。最终五图逐张打开检查中文、裁切、图例、NA及源表；其实际检查记录见图源provenance/交付检查。没有把文件存在冒充图像检查。

## 7. 产物与重现

W保留frequency全表、完整phi_D/V、q10/q20边与组、匹配矩阵、全部组control及诊断、sample CSR事件、两链资格、输入门槛/覆盖/1,760案例、五图PDF/SVG/PNG、图4全组分页PDF、源表、脚本快照/命令、配置和失败收据。大载荷留execution；本目录是自含中文/英文事实记录和图表说明。

[交付清单](artifact_manifest.json)绑定原路径/hash、输入/代码/figure源和状态；实际产物注册ID及当前访问快照见该清单。未执行H2、文档确认、B99正式校准或模型训练，没有这些产物或收益结论。旧Anchor、Focus与科学状态保持原样。


聚合口径也会改变外观：每组等权的真实平均离散度为0.35331dex，按组成员数加权后为0.66846dex（同size对照为0.85257dex）。小组不能在解释时代表大量feature；本轮主口径仍为每组等权，二者分开报告。
