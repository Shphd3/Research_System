# 最新执行与推理审计：双臂训练完整结束（2026-10-07 09:33:37北京时间）

[Summary](summary_cn.md)是当前结论入口。本节覆盖此前A仍运行的状态；下面原有日期记录作为历史完整保留，[改写前副本](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261007T013337Z/canonical_before)。

## 完成性与合同符合性

| 条件 | job | 平台 / 监督 | 结束时间（北京时间） | 进度 / 终点 |
| --- | --- | --- | --- | --- |
| A coupled / 4H100 Reserved | pt-txeitsor | SUCCEEDED / COMPLETED，child exit0 | 10月7日05:47:33 | 7629/1999896576，100%，完整milestone/weights7629 |
| B router_input_detached / 8RTX5090 Spot | pt-3u6bcqbq | SUCCEEDED / COMPLETED，child exit0 | 10月6日21:10:33 | 7629/1999896576，100%，完整milestone/weights7629 |

[ A平台 ](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261007T013337Z/A_platform.json)、[ B平台 ](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261007T013337Z/B_platform.json)、两臂completion/supervision、[ A pod完成 ](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261007T013337Z/A/pod_completion_evidence.json)、[ B pod完成 ](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261007T013337Z/B/pod_completion_evidence.json)和终止片段相互一致。终点manifest均complete，state及4/8rank RNG文件存在且尺寸一致；大型payload未重新hash，声明的checksum原样保留。共同weights为0/64/1024/3814/7629；恢复完整state不是只模型权重。

[源码锁核验](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261007T013337Z/source_lock_verification.json)：68文件PASS，SHA7faa926ec24d2664a3cc0f2ad66978382c363ac42cafc974a84ac1fd458821aa。代码/config/Protocol/数据身份未改变；本次适配旧分析入口为inspect_completed_pair.py，只改完成资格检查与图说明，旧图和源码留存。两臂metrics均连续1–7629、每步262144有效目标、LM/aux/total有限，weighted=.01×raw误差<1e-7、total加和误差<1e-5；resolved规范JSON hash匹配声明。没有跳步、缺行、NUL、忽略末行。实际batch归约保持一致，数据曝光严格匹配，但硬件/卡数对手未消除。

## 当前对照与结果链

本节问“切断一条反向边后，完整训练轨迹有什么变化”。两臂在同一参数状态的数值前向相同，所以不是用不同输入值解释初始预测差；但训练途中参数和路由分配会分化，专家暴露及硬件仍是竞争解释。路由器是从r算专家权重的可训练矩阵，专家是读取h的可训练网络；共享专家始终参与计算。它们均与旧固定候选更新不同。

返回激活r的梯度不是直接更新r；它通过上游导数改变参数梯度，AdamW修改参数后，同一输入下一次计算出的r才可能变化。训练CE能说明拟合，封存文档CE和保持负载的路由置换分别回答泛化与当前分配的功能价值；后两项还没有结果。

A保留LM门控返回r的反向边；B仅切断该边。r是残差相加前的注意力输出，h是残差相加后再归一化得到的完整专家输入；专家和shared expert在两臂均读live h，W及主干其他路径均训练。辅助项两臂共同以W stop_gradient(r)计算；均衡目标及定义与A3相同。同state/input前向公式相同，不意味着学成后的模型相同。当前不是冻结路由/表示/专家，也不是有/无均衡比较。

| 指标：最后64步均值 | A：保留LM路由反馈 | B：切断LM路由输入反馈 | B−A |
| --- | --- | --- | --- |
| LM交叉熵，nat/有效目标 | 4.109270 | 4.123641 | +0.014371 |
| 加权负载均衡项 | 0.013589 | 0.012073 | −0.001516 |
| 总训练目标 | 4.122859 | 4.135714 | +0.012855 |

末步本身LM CE A4.091892/B4.106052，差+.014160；末64均值如表。末32/128/256差+.014477/+.014643/+.014735，重叠窗口不能视独立证据。[里程碑训练描述](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261007T013337Z/milestone_training_description.json)按预留时间点作后向64步描述：268435456目标处差+.007740，999817216处+.011823，1999896576处+.014371。它们不是独立评测checkpoint CE，而是到该步最近训练batch CE。

每层有效专家熵计数末64均值A7.034546/B7.523360；它是负载分布的等效计数，不是语义专家数。两臂全部记录health/guard_failed为false，终点逐层load streak max0，12层各自零分配专家均0。旧零均衡失败不能与新目标混合推出“均衡造成改善”的因果；当前只证明新条件完成了训练。

## 对比图与来源

![完整训练比较](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261007T013337Z/loss_comparison.png)

横轴累计有效预测目标（十亿），两臂均到约2B；左上纯LM CE、右上同一步B−A、左下加权aux、右下总目标。浅线保留原始逐步值，深线为相同后向64步均值（16777216targets）；早期虚线为warmup结束。B−A正值表示A训练CE低。完整PNG已实际查看，轴/图例/正文均可读、无裁切，PDF也保存。纯训练图不显示TEST或表征功能证据。

| 可核验事实 / 派生判断 | 原始链路 | 资格边界 |
| --- | --- | --- |
| 双臂工程完成 | platform+supervision+completion+pod+完整manifest/weights | 已核验工程结果；不等于问题关闭 |
| A尾部训练CE低.014371 | 两份原始metrics快照 → 逐步/schema/targets检查 → aligned_updates →7566–7629平均 | BOUNDED；单对轨迹、事后窗口、硬件混杂 |
| B负载均衡项更低 | 同步router_aux_weighted → 同窗口平均 | 均衡指标，不是实用分工或机制 |
| 图/统计 | inspect_completed_pair.py → comparison/CSV/PNG/PDF | source/producer/output hash、metric/axis/聚合在figure契约与provenance |
| 主终点/功能/几何 | 未执行 | NOT_RUN，不由曲线补齐 |

[comparison](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261007T013337Z/comparison.json)、[aligned table](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261007T013337Z/aligned_updates.csv)、[figure contract](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261007T013337Z/figure_contract.json)、[figure provenance](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261007T013337Z/figure_provenance.json)。原始快照、标量CSV、实际config、完成/manifest/pod证据均在A/B子目录；脚本hash记录于provenance。将训练batch CE记在已完成更新的目标坐标，损失取自该batch更新前计算，并非终点模型在独立数据上的CE。

## 用白话组织推理（AI分析，研究者判断Unknown）

观察：两臂成功走完同一数据预算；A训练预测更准一点，B分配更均匀。我们实际比较的是允许不允许“路由选择的预测误差”反过来调整上游表征。

候选解释：A让表征为路由选择和预测一起适应，因此拟合较好。数学/局部资格证实切边改变对应梯度，**“改变梯度→形成更有用表征→改善独立预测”仍含未测试的经验桥梁**；当前曲线只测训练拟合，不完成这条机制链。

竞争解释：两臂专家接触数据的分布不同，梯度规模/Adam预条件不同；A/B还与H100/RTX5090完全绑定。这些可能在没有更好语义分工时产生较低训练损失。较低训练损失也可能不延伸到新文档。均衡更好而CE略高的B说明两目标不能互相替代，并不证明“集中造成收益”。

当前可说：在本次共同均衡、固定预算的单对训练轨迹中，A的预测拟合略好，B的负载更均匀。不能说：A普遍更好、直接反馈因果改善表征、专家学出有用语义分工、采用/关闭问题已确认。训练末64差>.01不适用原TEST区间/功能判据。

AI建议的最小下一检验：按既定合同比较两个终点的同一独立文档面板。优势保留→有界泛化差得到支持；消失/反向→训练优势不构成泛化收益；区间宽→INSUFFICIENT。若要机制主张，还需保持负载的因果route-bundle干预，并排除硬件对手；这些未执行，不以故事替代证据。

## 当前轮完整记录

1. 问题：有限匹配预算下LM反馈的净预测/功能作用，方向开放。
2. Setup/controls：共同均衡A3、同保存初态和Adam，只改LM gate→r；硬件对手保留。
3. 数据：同DCLM冻结view/order、262144目标/update，7629updates。
4. 确认：原1024文档FIT/DEV/DIAG/TEST封存方案不变，本轮未访问后测面板。
5. 结果：双工程完成，7629条匹配训练比较；主TEST/功能等NOT_RUN。
6. 理解/边界/下一行动：拟合与均衡不能互换，机制/采用Unknown；AI建议终点独立面板评估，本次未启动后测或新GPU任务。双监督正常结束，无自动重提。

下面旧记录完整保留为日期历史；不得将此前进度或失败条件当本次终点。

# 当前进度与损失比较：B完成、A继续（北京时间2026-10-06 21:31:44）

[当前Summary](summary_cn.md)拥有结论入口。本节是新条件`rrc_1006_balanced_r3`的最新事实；以下既有记录保留为有日期的历史，不再作为当前进度。原Summary与Detailed更新前副本在[本次证据目录](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261006T133144Z/canonical_before)。

## 对象、问题与当前对照

原科学问题与Anchor不变：有限匹配预算下LM门控反馈的净预测/功能作用。r为残差相加前Attention输出；h为残差相加后归一化专家输入。A门控W r、B门控W stop_gradient(r)；两臂专家都获得完整live h。B只切LM门控返回r的反向边，不冻结路由权重、主干或专家。同一state/input下数值前向相同；训练后参数可不同。

当前A3共同目标LM CE+0.01×router_aux。每序列T=1024，f_i为top2槽位计数/(2T)，pbar_i为平均softmax概率，单层aux=8Σ_i f_i pbar_i，先12层平均，再256序列全局平均；均匀基准1。两臂辅助softmax均以W stop_gradient(r)计算，保留W梯度、排除aux返回r的反馈，因此干预仍是LM反馈。沿用共同初态/data/顺序/Adam和262144有效目标/update；A实际4H100、B实际8RTX5090。

## 合同符合性与证据资格

| 登记对象 | 本次观察 / 证据 | 资格边界 |
| --- | --- | --- |
| Protocol A3 / 源身份 | [源码锁核验](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261006T133144Z/source_lock_verification.json)，68文件PASS；resolved config规范JSON hash与训练声明一致 | 没有改训练代码或配置 |
| 数据 / 初态 / 目标 | 两resolved config的pair rrc_1006_balanced_r3、data/initial_state身份保持；全部日志每步262144目标，连续1..4173/7629 | 相同batch/order，单seed |
| 目标 / 差异 | 两臂aux系数0.01，LM/aux/total均有限；weighted=0.01×raw误差<1e-7，total加和误差<1e-5 | 双臂辅助r路径共同detach由既有梯度资格证实 |
| 资源 | A H4 RUNNING；B RTX8 SUCCEEDED | 算法与硬件/卡数完全混杂 |
| 停止 / 完成 | A未完成；B completion7629/1999896576、pod training_complete、监督child exit0、完整终点manifest | B工程完成不等于科学比较完成 |
| 恢复留存 | A快照latest full manifest step4151；B完整终点state/RNG8ranks；文件存在与大小匹配 | 未重新hash大型checkpoint payload |
| 后测 / 阈值 | 封存TEST、bootstrap、功能干预均NOT_RUN；复杂入口仍有PREPARED_NOT_IMPLEMENTED | 登记主终点不能判定；不套用TEST阈值到训练曲线 |
| 本次新增分析 | 32/64/128/256事后窗口与原始匹配差 | BOUNDED训练描述；不视step/窗口为独立样本，无CI或显著性判断 |

## 完成性与派生比较

平台[ A ](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261006T133144Z/A_platform.json) / [ B ](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261006T133144Z/B_platform.json)为本次只读快照。A已4173步/1093926912targets=54.699%；B已7629步/1999896576targets=100%。B完成平台时间13:10:33UTC（北京时间21:10:33），[pod完成证据](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261006T133144Z/B/pod_completion_evidence.json)、[终止片段](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261006T133144Z/B/pod_terminal_excerpt.txt)、[completion](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261006T133144Z/B/completion.json)和[终点manifest](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261006T133144Z/B/latest_checkpoint_manifest.json)相互一致。A监督时间13:31:44UTC，近步长外推剩余26808.69秒=7.45小时，仅是估计。

| 共同行程末尾：steps4110–4173，16777216有效目标 | A | B | B−A |
| --- | --- | --- | --- |
| LM CE（nat/valid target） | 4.243208 | 4.256216 | +0.013008 |
| 加权aux | 0.013676 | 0.012065 | −0.001611 |
| 总目标 | 4.256884 | 4.268281 | +0.011397 |
| 每层有效路由专家均值（描述性熵指标） | 6.971997 | 7.419154 | +0.447158 |

瞬时匹配step4173的CE A4.244847/B4.258299。末32/128/256窗口的B−A CE差分别+.013271/+.012634/+.012051，方向一致；这些窗口互相重叠，不能当独立复现实验。B最后64步CE均值4.123641属于更后进度，不与A当前CE比较。两臂全部已记录health/guard_failed为false；最新逐层load streak max0、每层零负载专家0。有效专家计数与均衡项描述负载，不证明语义分工或因果收益。

## 图与可复核来源

![共同均衡双臂损失](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261006T133144Z/loss_comparison.png)

横轴为累计有效预测目标（十亿），不用墙钟时间。左上纯LM CE、右上同一步B−A、左下加权均衡项、右下总目标。浅线为原始逐步值，深线为后向64步滑动均值，窗口16777216targets；虚竖线标warmup结束33554432targets，点竖线标共同终点1093926912targets。右侧阴影/B虚线是只有B走过的数据，不进入配对差。右上正数表示A训练CE低，负数表示B低。已查看完整PNG，所有轴/图例/说明可读，无裁切；PDF同时保存。

| 事实 / 派生结论 | 原始来源 → 计算 | 资格 / 可说范围 |
| --- | --- | --- |
| B完成，A仍运行 | 平台+supervision+completion+pod+checkpoint manifests → comparison.json | 工程事实，不是科学胜负 |
| 匹配末64步A训练CE低0.013008 | 两份metrics_snapshot → 连续/schema/目标与分量检查 → aligned_updates.csv → 同步平均 | BOUNDED；训练、单seed、硬件混杂 |
| B均衡项低0.001611 | 同原始metrics的router_aux_weighted → 同一64步平均 | 负载项本身，不能代替CE/功能 |
| 图 | snapshot/scalar CSV → inspect_balanced_pair.py → PNG/PDF | 数据、尺度、聚合、边界在figure_contract.json；producer与图hash在provenance |

[comparison](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261006T133144Z/comparison.json)保存来源hash、身份、逐步资格与窗口；[aligned table](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261006T133144Z/aligned_updates.csv)共4173配对行；两臂原始metrics快照与标量CSV在该目录A/B；[figure contract](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261006T133144Z/figure_contract.json)与[provenance](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261006T133144Z/figure_provenance.json)记录图链路。源码锁SHA仍7faa926ec24d2664a3cc0f2ad66978382c363ac42cafc974a84ac1fd458821aa。本次producer初版将规范JSON hash误当原文件hash而停止，修正解析后重跑；未改任何训练文件，旧分析未完成目录标INCOMPLETE_ANALYSIS_ATTEMPT_NOT_A_RESULT。

## 当前轮记录与边界

1. 问题/假设：共同均衡下直接LM反馈有限轨迹的净作用；帮助/损害两个方向开放。
2. Setup/controls：Protocol A3精确冻结，当前差别为LM gate→r反向；硬件对手无法排除。
3. 数据：同冻结DCLM view/顺序，同262144targets/update。
4. 确认：原独立封存面板不变，未访问主TEST或执行功能后测。
5. 结果：B工程完成，A未完成；匹配训练CE和aux方向不同，统计如上；主终点NOT_RUN。
6. 有限理解/下一行动：当前曲线说明训练预测与均衡指标不能互换，不建立机制或采用结论。A既有任务内监督继续，B正常结束；研究者机制/采用/关闭Unknown。本次无新增训练、重提、恢复、GPU后测、commit/push。

下面为先前有日期记录，包含新双臂启动、原无均衡失败及1005提交历史；不与本次快照混合。

## 新共同均衡正式双臂：已核验实际启动与首步

核验时间2026-10-06T03:30:26.518923+00:00。A `pt-txeitsor`实际world4，已记录73updates/19136512有效目标；B `pt-3u6bcqbq`实际world8，已记录19updates/4980736有效目标。两者平台RUNNING，启动、有限组件tags与目标计数均PASS，两个任务内监督器活跃。新正式create每臂一次，平台max_retries=0。新H4/G2 Smoke `pt-96b4ccz1`/`pt-xdfrqwsi`均验收PASS且平台SUCCEEDED，cross-hardware PASS。五项本地资格PASS，源码锁SHA为7faa926ec24d2664a3cc0f2ad66978382c363ac42cafc974a84ac1fd458821aa。

[当前Summary](summary_cn.md)；[分析思路](analysis_notes_20261006_cn.md)；[实际启动快照](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/receipts/startup_pair_20261006.json)；[新条件冻结](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/receipts/formal_pair_freeze.json)；[原执行源码保留核验](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/receipts/old_execution_preservation.json)。raw/checkpoint/metrics/pod日志均在新root，supervision.json由各ACP监督器刷新。没有读取主TEST效用、执行功能或其他后测；高级入口仍明确待实现。未commit/push、修改其他项目或1002对话记录。

以下分阶段记录为历史，本段实际启动观察覆盖其待提交/未观察状态。训练尚未完成，主终点不可判断。整个pod强制撤销时任务内监督也会终止；监督器没有桌面主动推送或自动重提能力。原零均衡失败条件和完整证据继续单独保留。

## 当前A3共同均衡重训

新条件已登记；本地梯度/辅助路径、checkpoint/外进程恢复、保护终步保存、监督器终态分类均PASS。新4H100 Smoke为pt-96b4ccz1；2RTX Smoke直接回执在以下新root。须新双硬件资格均PASS后才提交新正式；原零均衡失败历史保留且分开。此次监督已获明确请求。

Execution root: `/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced`. [Protocol A3](protocol_cn.md); [analysis notes](analysis_notes_20261006_cn.md).

# Detailed：路由—表征梯度反馈对照执行

## 当前核验：2026-10-06正式训练提前退出

来源快照时间：2026-10-06T02:29:47.761936+00:00；用户请求“检查是否训练完成，然后给出训练比较”。以下是当前事实；后面的1005提交记录保留为历史，不再代表当前正式状态。

### 完成性、失败与原始证据

| 条件 | job | 平台终态/结束（北京时间） | 最后持久化进度 | 完整最新恢复manifest |
| --- | --- | --- | --- | --- |
| A coupled | pt-9egkfirg | FAILED，10月5日19:08:06 | 274steps/71827456targets | step265/69468160targets |
| B router_input_detached | pt-86fsmog5 | FAILED，10月5日20:12:55 | 274steps/71827456targets | step157/41156608targets |

平台快照在[status receipts](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/receipts/status_20261006)；durable pod日志：[A pod](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/acp_receipts/pod/rrc-1005-full-coupled-v1-20261005T103331Z.log)、[B pod](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/acp_receipts/pod/rrc-1005-full-router-input-detached-v1-20261005T115134Z.log)。两者均明确RuntimeError LOAD_COLLAPSE；没有completion.json，未生成终点milestone。保留恢复manifest标complete，但本次只读核验未重算数GBcheckpoint payload校验和。

正式world4/8运行已发生，8卡资格不再是“完全未观察”；对应resolved_config记录实际硬件/运行层。训练前的2卡Smoke边界仍是历史资格边界，不改写旧回执。

### 训练比较与证据链

[comparison.json](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/analysis/20261006_training_comparison/comparison.json)保存源SHA256、算法、窗口及条件；[aligned updates](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/analysis/20261006_training_comparison/aligned_updates.csv)保存274条逐步对齐结果。两臂每步tokens完全一致，训练view/随机state/超参数由冻结Protocol及resolved_config追溯；比较单位为相同全局预测batch，不是独立重复。

| 训练CE（nat/valid target） | A | B | B−A |
| --- | --- | --- | --- |
| step64 | 10.357514 | 10.361484 | +0.003970 |
| step128 | 7.823689 | 7.828560 | +0.004870 |
| step274 | 6.321735 | 6.322187 | +0.000452 |
| last32，steps243–274事后描述 | 6.484663 | 6.483023 | −0.001640 |
| last64，steps211–274事后描述 | 6.576622 | 6.576355 | −0.000267 |

没有把滑窗、step当独立样本构造CI，也没有把训练差套用TEST的.01nat建议门槛。两臂loss均有限且下降；274条health/guard_failed均false。负载归约先累积每microbatch的load fraction，再跨rank平均，最后由全局向量计算零负载专家和entropy effective count；因此末尾闲置专家数是真正全局batch零分配，不是microbatch均值。

step274 A有效专家均值2.0166、每层平均零load4.8333，layers3–10共8层6/8路由专家零load；B分别2.1191/3.0833，layers7–10共4层6/8零load。编号仅用于各模型内部定位，不当语义对齐。shared expert仍参与前向，两个专家指routed专家。

### 保护计数和恢复边界

源码[guard source](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/src/coupling/train.py:1486)先optimizer.step、增计数，再评估load guard，最后写metrics/checkpoint。现存日志完整连续1–274；两臂148–274的ANY-layer streak为1–127，RuntimeError意味着下一次达到128。由代码推断275更新已执行，但275loss/权重未落盘，不能把274日志或旧恢复checkpoint写成最新275状态。

实现使用一个ANY-layer计数器，越界层可变化；已记录127步没有固定层全程越界。这与“某一固定层持续128步”的读法有差距，属于计数口径审计，不修订冻结Protocol或代码，不据此否认观测到的严重路由集中。保护异常未走终止checkpoint/completion发布，恢复只能使用A265/B157；共同分析weights仅0/64（16777216targets），不能拿不同步恢复state做matched-token终点比较。

### 图、资源与资格

![训练比较](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/analysis/20261006_training_comparison/training_comparison.png)

横轴共同valid targets（百万）；上方CE几乎重合，中间B−A小幅变号，下方6/8路由专家闲置的层数末尾A8/B4。虚线为warmup结束128步，浅红为148–274连续ANY-layer越界窗口。producer inspect_training_20261006.py；原始表[aligned updates](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/analysis/20261006_training_comparison/aligned_updates.csv)，图来源[figure provenance](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/analysis/20261006_training_comparison/figure_provenance.json)，渲染已查看无裁切。图只支持早期训练/负载描述，不能证明heldout或机制。

包含checkpoint停顿的训练循环平均速度A37029/B67932 valid targets/s；末64步吞吐中位A44222/B108974；峰值reserved A10.047/B10.031GiB/卡。B使用8RTX5090而A4H100，速度差含硬件/卡数/路由稀疏性，不作算法效率因果结论。

观测/派生：双FAILED、早期CE接近、负载集中与保护触发。工程停止条件按实际实现触发。登记主要终点缺失，科学comparisonINSUFFICIENT；效用、机制和采用判断Unknown。没有执行TEST/功能后测，没有重提、改参数、放宽guard或恢复训练。唯一下一研究者决定是如何取得有效比较，尚未确认。前次delivery_artifact_manifest是1005历史身份快照；本次身份/来源由comparison.json和dated状态回执持有。

## 1005提交与资格记录（历史正文原样保留）

更新时间：2026-10-05T10:40:26.520517+00:00。[Summary](summary_cn.md)；[唯一Anchor](../../problem_anchors/router_representation_gradient_feedback/anchor_cn.md)；[训练Protocol：R1 + A1/A2](protocol_cn.md)；[后测Protocol](analysis_protocol_cn.md)。

## 0. 快速结论与证据资格

问题是有限轨迹下直接路由反馈的净作用，收益/损害两个方向仍开放。直接事实：双硬件Smoke与交叉检查PASS；两项正式create各返回一个ID。证据仅对实现、生产形状和短窗恢复合格。终点分析NOT_RUN；按用户要求，正式运行NOT_OBSERVED。研究者机制/采用判断Unknown；问题未关闭。

## 1. 对象与计算

| 对象 | 实际含义 | 边界 |
| --- | --- | --- |
| reference r | 残差相加前Attention输出 | 不等于专家输入 |
| 专家输入h | Attention残差相加后归一化hidden | 两臂均保持live |
| A coupled | router读取live r | LM门控反馈可返回r |
| B router_input_detached | router读取r.detach() | 仅切这一反向边；router、专家、gate权重和残差仍可训练 |
| valid targets | 非忽略的下一个token预测标签 | 成功优化更新后才推进全局累计数 |
| 硬件比较 | 每种硬件内从共同初态运行A/B | 正式算法与硬件完全混杂 |

## 2. Anchor与决定

唯一Anchor持有科学设计，Focus持有研究者的保留/移除/继续验证决定。执行批准来自[研究者请求](../../../handoff/researcher_request_cn.md)，已规范化到Protocol；批准与工程PASS不证明收益、机制或采用价值。

## 3. 冻结、一致性与修订

| 登记项 | 实际情况/证据 | 资格边界 |
| --- | --- | --- |
| 干预仅切12层router-input，aux=0 | 局部梯度与两硬件完整模型诊断PASS | 实现正确性 |
| 共同模型/数据/初态/全局batch | 源码锁、Smoke resolved contracts及启动自检PASS | 同初态与样本分片 |
| 262144targets/update，H4/G2短窗 | 每臂两步，update1外进程恢复PASS | 无长期稳定性证据 |
| 正式A H4reserved / B G8spot | 展开资源tuple与直接返回一致 | 正式运行未观察 |
| schedule | Smoke明确warmup1,total2；正式warmup128,total7629 | 工程schedule不作正式轨迹证据 |
| A1 | 真FP64参考与隔离ABI/运行层修复；保留原失败 | 未放宽生产容差 |
| A2 | 首轮均在训练前FAIL；诊断整数索引修复；第二轮SUCCEEDED | 首轮仅失败账本 |
| TEST终点/不确定性 | 面板曝光前锁定；后测尚未运行 | 主结果缺失 |
| 停止边界 | 正式直接返回后未读运行状态，无监控/重提 | 按用户要求 |

R2源码锁SHA256：`9e5d2d288c7c9a12dc23f9dba6d60631ec19ceaafa7ebb5a0c602f11d398bf9e`，56文件；[正式共同冻结回执](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/receipts/formal_pair_freeze.json)。没有事后科学分析或按结果选择终点。

## 4. 实际Smoke与登记正式配置

模型342097408参数、12层、hidden512、4Attention/2KV heads、head_dim128、RoPE theta1000000、vocab151936、tied embedding、8路由专家/top2/宽1536、每层1shared expert、dropout0。温度1，top2 softmax gate权重不再次归一化。全部参数可训练；关闭EMA/de-common/SAE/谱项，raw辅助均衡只作遥测，weighted目标0。

共同新随机CPU seed1005初态；文件SHA256 `a232a4fc0a7afad23cf1f410089239ef125edcefc9760942a5365c5825d3abcd`；tensorSHA256 `d835c0afd8ca57302506c5f23009268c2e4173b75b79361a32a9a39029c72e2c`。未使用预训练或旧实验权重。

训练view `/data/250010109/training_data_views/dclm_pair_v1/train`，manifestSHA256 `8a91bdbb0eb537bd80612015b99f178ca1cbb54a2fa7cf8442ab1eae7f0a2f2d`。核验路径/大小及抽样token边界，不声称完整1.2TB内容hash。每update连续256序列，按rank划分；不重排、不跨epoch。tokenizer身份见inputs/analysis_manifest.json。独立heldout原始shard02 SHA256 `4c5ce60258943051758148653c448bb57724af7592cc9d3e9c053cc6f9e10323`；1024去重文档，FIT128/DEV128/DIAG128/TEST640；panelSHA256 `350d883e439ac62e6303e6d00b86a7e882ce7b0454fe3402a405d89ae51bb05a`。选样未曝光loss；全语料语义去重未验证。

任务为next-token LM CE，全局有效标签加权均值，CE分块256。AdamW1e-4，betas(.9,.95)，eps1e-8，WD.01，clip1，fused=false。BF16 autocast、FP32参数/Adam，SDPA、TF32关闭，无activation checkpoint。两硬件实际均torch2.8.0+cu128/CUDA12.8/HF4.53.3/cuDNN91002/NCCL2.27.3，使用隔离挂载层，不改base。

序列1024、microbatch1；H4 acc64、G2 acc128、正式G8 acc32，均262144valid targets/update。每种硬件每臂实际两步/524288targets，update1外进程恢复；登记的Smoke warmup1使只有step2采用非零LR。正式目标7629updates/1999896576targets，warmup128=33554432targets，cosine到终点。正式是否启动/完成或产出checkpoint均未检查。

登记weights steps0/64/1024/3814/7629，对应tokens0/16777216/268435456/999817216/1999896576。完整optimizer/RNG rolling checkpoint每10min或累计>=0.2B（先到者），latest2；终点完整状态。每run100GiB上限。Smoke留存后实测10.197GiB/run；正式weights+resume粗估18–25GiB/臂，不含未来activation缓存，上限不是精确预测。独立代码的[复用账本](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/docs/reuse_sources.json)与[实际读源审计](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/docs/source_read_audit.json)区分复用data/DDP/checkpoint/runtime、适配detach/sampler/遥测/guard及拒绝旧权重/正则。

## 5. 指标与预登记判据

工程门槛包括同硬件同state完整前向/routes/gates、末层router/专家梯度及reference切边、B router更新；tiny真FP64全网络telescoping；DDP/累计、外进程恢复、有限TensorBoard tags、两步计数；reserved<78GiB H/<30GiB G。交叉初态logits相对RMS<=.02、CE差<=.02nat。梯度/routes/短窗差异完整报告，不冒称精确硬件梯度相同。

科学主要量为终点TEST负logprob总和/valid targets，B减A，nat/token。整文档配对5000-bootstrap、seed1005、percentile95% CI；AI建议实用差异.01nat，不是人工采用阈值。[后测Protocol](analysis_protocol_cn.md)持有六类测试及支持/反对/INSUFFICIENT分支。主分析尚未执行，单seed和硬件混杂仍在。

## 6. 完整证据链

| 有界事实 | 原始来源/计算者 | 值或检查 | 资格与限制 |
| --- | --- | --- | --- |
| 切边正确 | [局部梯度](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/receipts/local_gradient_contract.json)；gradient_contract.py | 真FP64残差7.446e-17/4.054e-17；错误expert-detach负对照可识别 | tiny恒等式，不是轨迹收益 |
| CPU恢复/DDP | [外进程恢复](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/receipts/local_external_resume.json)；external_resume.py | 同拓扑model/Adam/schedule精确恢复；1vs2rank累计等价；64tokens/2steps | CPU tiny |
| GPU同state路径 | [H诊断](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/receipts/diagnostics_h100.json)；[G诊断](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/receipts/diagnostics_5090.json) | 完整logits/routes/gates相同，末层路径/B更新PASS | 其他层参数差需完整网络拆分 |
| 正式batch/恢复/遥测 | [H100 acceptance](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/receipts/smoke_h100_acceptance.json)；[RTX5090 acceptance](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/receipts/smoke_5090_acceptance.json)；verify_smoke.py | 每硬件每臂2steps/524288targets、1resume segment | 两步、单seed，无长期稳定性证据 |
| 交叉初态 | [cross-hardware acceptance](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/receipts/cross_hardware_acceptance.json)；diagnostics_*.pt -> compare_hardware.py | RMS.008265；CEabs.0002336502nat；topk slot mismatch.003051758；梯度sample相对L2 A.02864/B.02868 | 登记初态门槛PASS；不证明硬件效应零 |
| 固定训练样本短窗 | [cross-hardware acceptance](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/receipts/cross_hardware_acceptance.json)；short_window_*.pt | H B−A=−.0001573563nat；G B−A=.0003747940nat；跨硬件G−H A=−.0003385544/B=.0001935959 | 单训练样本，方向不同，非TEST科学结果 |
| 正式创建调用 | [A direct return](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/receipts/submissions/full_coupled/direct_return.json)；[B direct return](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/receipts/submissions/full_router_input_detached/direct_return.json)；submit.py | rc0，各1ID：pt-9egkfirg/pt-86fsmog5 | 仅提交直接结果，运行未观察 |
| 后测准备 | [入口清单](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/docs/analysis_entrypoints.json)；[合成统计资格](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/receipts/analysis_stats_qualification.json) | CE/统计可运行；gradient/capture/functional/finite-update明确待实现 | 没有训练模型后测结果 |

## 7. 实测Smoke显存与吞吐

| 硬件/条件 | ranks | updates/valid targets | peak allocated/reserved GiB每卡 | valid targets/s | 资格 |
| --- | --- | --- | --- | --- | --- |
| h100 / coupled | 4 | 2 / 524,288 | 9.211 / 9.686 | 15996.3 | PASS |
| h100 / router_input_detached | 4 | 2 / 524,288 | 9.211 / 9.686 | 16140.2 | PASS |
| 5090 / coupled | 2 | 2 / 524,288 | 9.165 / 9.670 | 19578.1 | PASS |
| 5090 / router_input_detached | 2 | 2 / 524,288 | 9.165 / 9.670 | 19968.8 | PASS |

数值为短窗实测峰值与恢复后训练循环速度，不是长期平均。仅训练计算外推：A约34.73小时；B按2到8卡理想缩放约6.95小时。不含排队、checkpoint开销、spot中断；8卡实际速度/拓扑未验证，不承诺完成日期。

## 9. 失败分解

首轮H=pt-0bhf38z4/G=pt-oz88x40i均在训练前FAILED：诊断FP32 linspace把embedding末索引77791231舍入为77791232。整数计算修复，边界检查PASS；A2保留旧锁/日志，容差不变。局部ABI、cuDNN优先级及原mixed-FP64严格检查失败均保留，不重标PASS。这些工程失败没有推翻科学假设。

## 10. 追加式执行历史

以下原记录按当时观测保留，不作为当前正式运行状态。

Registered R1; result_state=NOT_RUN. Execution records and amendments follow below. Authority: handoff/researcher_request_cn.md; code/raw root /data/250010109/MoE_Router/experiments/20261005_router_representation_coupling.


## Execution checkpoint — 2026-10-05, Smoke create calls returned

- Purpose: qualify only the router-reference backward edge before the two finite trajectories.
- Hypothesis: benefit/harm both open; scientific result NOT RUN.
- Setup: one342,097,408-parameter12-layer8E/top2/shared-expert model, seed1005 common saved random state; reference is pre-residual Attention output, expert input is separate normalized post-residual hidden state. All-layer detach in B only. Final target1,999,896,576targets/7629updates,global262144batch.
- Data: training path/size frozen-view inventory verified; no full1.2TB content hash. Separate raw-shard02 source hash checked,1024unique documents frozen128FIT/128DEV/128DIAG/640TEST. No model losses exposed during panel selection.
- Confirmation: one main TEST endpoint. Early checkpoints descriptive; bootstrap whole docs does not estimate seed uncertainty.
- Engineering results: local isolated gradients and true-FP64 full-network edge telescoping PASS; external-process checkpoint/model+optimizer+scheduler exact restoration PASS;1-vs2rank accumulation/model tolerance PASS. Source logs under execution receipts. Preserve initial FlashAttention ABI, torchvision ABI, cuDNN precedence, test indexing/deepcopy and mixed-precision1e-10 residual failures; repaired locally, no old source/base environment edits. Original native mixed-FP64 failure is not relabelledPASS.
- Submitted Smoke: H=pt-0bhf38z4 (4H100 reserved), G=pt-oz88x40i (2RTX5090 spot), each direct create returned an ID. Both observedSTARTING at09:56UTC; actual GPU/qualification not yet verified. Formal jobs NOT_SUBMITTED. Owner currentthread only.
- Post-test readiness: document CE and bootstrap/geometry-statistic scripts runnable. Gradient/capture/functional/finite-update entries PREPARED_NOT_IMPLEMENTED with exact input/output and preregistered procedures; this turn does not perform or submit later expensive analysis.
- Insight/boundary/next action: path checks certify intervention wiring only. Observe these existing Smokes; both auditedPASS plus cross-hardware check required before full creates. Formal submit once each, save direct returns, immediately stop polling. No mechanism/adoption decision inferred.

Evidence root: /data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/receipts/; source lock docs/source_lock.sha256; submission direct_return.json perstage.


## 执行检查点：2026-10-05，Smoke 创建已返回

- 问题/假设：检验 router reference 的直接 LM 反向反馈；帮助与损害均开放，科学结果 NOT RUN。
- 设置：342,097,408 参数，12层8E/top2、共享专家、seed1005共同保存随机初态。r是残差前Attention输出，h是残差后归一化专家输入；B只在全部层router输入detach。正式终点1,999,896,576targets/7629updates，每更新262144真实目标。
- 数据：训练路径/大小/链接清单核验，不是1.2TB全内容hash。独立raw global-shard02源hash已核验；1024去重文档冻结为128FIT/128DEV/128DIAG/640TEST，选择时无模型loss曝光。
- 确认边界：唯一TEST主终点；早期只描述，整文档bootstrap不估计seed不确定性。
- 已得工程证据：隔离梯度与独立真FP64全网逐边VJP分解PASS；外进程checkpoint恢复model/optimizer/scheduler精确一致；1/2rank累计模型结果在预定容差内一致。保留FlashAttention/torchvision ABI、cuDNN优先级、测试索引/deepcopy及混合FP64原1e-10等式失败日志；修复限项目进程/副本，无旧源/base环境修改。混合精度失败不改写PASS。
- Smoke任务：H=pt-0bhf38z4，4H100 reserved；G=pt-oz88x40i，2RTX5090 spot。创建直接返回ID。09:56UTC均STARTING，09:59worker Pending但已有宿主分配。实际GPU资格未确认。正式双臂 NOT_SUBMITTED。
- 后测准备：CE读取及bootstrap/几何统计入口可运行；梯度捕获、保持负载的功能置换和有限更新入口明确 PREPARED_NOT_IMPLEMENTED，并持有冻结输入/操作/输出要求。本轮不运行或提交昂贵后测。
- 边界/下一动作：路径检查只证明实现。继续观察这两个既有Smoke；双PASS及跨硬件数值检查PASS后各一次full create，保存直接返回立即停止正式轮询。不从Smoke推断科学机制/采用。

证据root：/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/receipts/；docs/source_lock.sha256持有源身份；每stage的submissions/direct_return.json持有创建事实。


## Smoke 修订 A2 — 2026-10-05T10:10:50.492643+00:00

首轮两项均在进入训练前失败：H100 pt-0bhf38z4 于10:01:39UTC结束；5090 pt-oz88x40i于10:03:56UTC结束。梯度指纹 FP32 末索引越界，整数边界检查已PASS。修订仅改诊断索引和显式Smoke重试记录，算法和容差不变；保留旧源码锁及日志。第二轮创建直接返回：4H100 pt-eemr6vdt，2RTX5090 pt-z63ayg30。正式尚未提交，科学结果尚无。执行证据位于新执行目录receipts与docs/freeze_r2.json。


## 11. 解释与可主张边界

观测：资格通过、create返回ID。派生统计：短窗计算ETA与跨硬件差值。科学机制/采用判断Unknown。可主张干预接线、4H100/2RTX5090生产batch及短窗恢复合格；不可主张收益、语义分工、长期因果机制、正式训练完成、硬件效应零或8卡实际资格。

## 13. 研究者下一决定与执行停止

唯一下一科学决定是依据有界终点证据，保留、移除或继续验证直接反馈；研究者判断Unknown。本轮完成标准是双资格+双提交+后测准备。已停止正式轮询，无后台监控、额外seed/臂或自动重提。未来明确请求状态时只查现有ID/回执，不重提。后测依据冻结Protocol和保存checkpoint进行，本轮不运行。

## 14. 产物manifest

[机器可读manifest](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/docs/delivery_artifact_manifest.json)保存小文件来源/回执hash及输入身份；checkpoint留执行目录，由各manifest/checksum持有完整性。正式条目仅覆盖create直接回执，不指称未见运行产物。

## 15. 入口

代码/config/raw根：`/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling`。Smoke/正式launcher：scripts/run_smoke.sh与launch_train.sh；正式configs/formal_coupled.json和formal_router_input_detached.json。提交/失败回执在receipts/submissions；durable Smoke pod logs在acp_receipts/pod/rrc-1005-smoke-*-v[12]-*.log。后测清单为inputs/analysis_manifest.json、docs/analysis_entrypoints.json，未来输出analysis/。本次非可视工程检查不需要图。
