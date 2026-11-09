# Protocol：定位被总体帮助抵消的任务相关不利作用

## 0. Approval Snapshot

- 文档状态：**AUTHORIZED_LOCAL_POSTHOC / POST_HOC_EXPLORATORY**。2026-09-28，研究者明确要求接续交接入口并完成此方案中的进一步结果分析；授权范围是第5—14节的现有数组本地CPU分析、0928结果记录与日期图，不含新训练、GPU任务、前瞻预测、参数隔离、Git发布或科学结论批准。下列机制分支仍为AI建议，研究者判断待定。
- 类型：已有数据上的机制定位与测量工具审计（root-cause audit / proxy test），不是训练方法开发。
- 目的：定位任务信号相关的增损作用，解释它为何被较大的减损作用抵消；SAE、PCA/SVD和probe均为工具，不要求其中任何一个成功。
- 关联：[原Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_10_shared_update_conditional_interference/17_10_shared_update_conditional_interference_anchor.md)第4—5节的“原生表征位移→有符号作用”与共同子空间诊断；[Focus](../../../../focus/focus_shared_update_conditional_interference.md)。这是现有局部作用问题的追加分析，不能回写为原注册的主检验。
- 原正式结果：[Summary](../20260927_controlled/summary_cn.md)、[Detailed](../20260927_controlled/detailed.md)。原Anchor中NOT RUN为历史设计快照，运行状态以完成记录为准；不修改冻结来源。
- 本轮直接要减少的不确定性：共同激活／主要变化空间，是否承载了已经观察到的任务相关不利分量，还是主要反映背景与其他变化？原Focus的前瞻预测决策尚未被研究者更新；本方案为该决定补机制证据，不自动启动预测或隔离实验。
- 改变的对象：分析坐标、投影空间与观测量；固定模型、数据、源更新、损失与全部条件。所有12方向族已被查看，本轮始终是事后探索，不能重新命名为未见确认集。
- 主要读数：原生任务信号分量在保持／翻转规则下的带符号作用，以及这部分规则差异如何随输入重合改变；再用每种预列工具定位它与抵消项。SAE无需胜出，任一工具的结果都不挽救原“产生净伤害”的强预测。
- 执行载体候选：本地CPU，最多8线程、32 GiB常驻内存、2小时墙钟、2 GiB新产物；此为AI工程预算，不是实测ETA。逐文件流式读取，不加载模型权重，不新增GPU任务。
- 完成：复现→交叉分解→工具对照→区间与失败记录→四段式结果和唯一下一判断；研究者最终科学结论仍待确认。

## 1. Terminology / Definitions

- 原生输出表征 \(a\)：固定S7末层注意力输出矩阵 \(W\) 的1024维输出；输入 \(c\) 为2048维。不是把输入和输出接在一起。
- 参数变化与表征变化：\(\Delta a=\Delta W_Ac\)。本轮分析已经保存的实际位移，不生成新的参数更新。
- 逻辑样本：同一个无关变量 \(\xi_i\) 配上 \(t=-1,+1\) 的两条记录。不能拆开重抽样。
- SAE common：保留原定义，同原子、激活频率和正强度分布相近；冻结32原子的完整解码空间记为 \(S\)，正交基为 \(Q_S\)。几何主成分不继承“相同原子”的含义。
- 联合主成分：A、B原生表征按**样本行**堆叠，在同一1024维坐标中做分解；只能叫候选共同变化空间，必须另报双方对它的占用。
- 未中心化SVD观察原始能量；中心化PCA观察去除总体均值后的变化。两者不混用。PCA不是监督式probing。
- 线性probe：用已知信号标签 \(t\) 拟合线性读出，只检验信号是否可读；不预测更新后果，不证明模型使用了该读出方向。

## 2. Anchor Alignment

原Anchor第4节给出 \(\Delta a=\Delta W_Ac\) 与一阶损失作用，第5节要求分析共同空间及其正交剩余。本轮进一步把位移按已知信号正负配对拆开，避免总体帮助遮住不利分量。原主量 \(M\)、原净伤害裁决及原SAE资格结论均保持不动。

本轮的机制问题、替代解释、数值选择及分支都是**AI建议的追加分析设计**，不是已获确认的新Anchor判断。当前用户选择了分析方向和工具对照，未确认工具必然有效或共同原子致因。只读复现和资产核验可独立进行；新方案成为正式执行合同须由接手时的明确执行指令覆盖，不能从memory推导权限。

## 3. Tested Hypothesis

候选解释：A更新中与任务信号有关的不利作用，优先落在双方共同使用的表征方向；较大的其他减损作用使总后果仍为帮助。

需要分别检验两条：一是确实存在带符号的任务信号作用；二是它是否集中于共同结构。第一条的事后初步读数不能自动证明第二条。即使几何定位得到支持，仍只是基于真实位移和目标导数的局部归因，未检验因果必要性。

## 4. Rival Explanations

1. **背景解释：**共同激活／首个大主成分主要描述固定背景，任务相关增损发生在其余方向。用信号×空间交叉分解区分。
2. **单组或方差解释：**合并数据的主成分被一组主导，或只因高方差而显得重要。分别报告A/B占用，并比较未中心化SVD、中心化PCA和同秩随机空间。
3. **可读性与作用分离：**probe容易读出 \(t\)，但实际位移及损失作用不经过其读出空间。同时报告解码、位移捕获和有符号贡献，不能以高准确率代替机制。

## 5. Data Construction And Provenance

唯一原执行根（下称R）：

`/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/runs/full_h100_20260928T010310Z`

- 模型：精确33,000,000,000训练词元S7；非330亿参数。原state SHA256为c30b78e5bcba8f0a09c5e215389be86778874e87fcbb9fe5211175d370bb0803。
- 原注册SHA256：ab201f81cdcfa9ff9b5be7e745d7125ffe4f7908df3d8727f1b479c8c397616c；measurement_complete.json SHA256：e3ee791665dd7e3e80bdaae50891fb51fe2f7a68720a20650a4d1497bd102f26。
- 分析所有f21001—f21012、rho=0.1/0.8、repeat=0—3、step=1e-4/5e-5、B same/flip；192次虚拟更新、384个B条件格，不挑受害样本或方向族。
- 拟合结构空间：R/confirm/f*/structure_{rho}_{A|B}.npz中的a、a_hat、t、xi、indices、values；每格256行（128对），a形状256×1024。四格平衡堆叠，共1024行；每个方向族独立拟合一套空间，跨rho共用，不使用读出损失。
- 动态评价：R/confirm/f*/rho{rho}_rep{repeat}/step_{step}.npz中的source/same/flip_a0、da、e、I、I1、R及logits0/1；每格512行（256对）。source是独立A读出，不是产生更新的A训练批次。
- 配对与标签核验：同族source_readout_rho*.npz和target_rho*.npz中的pair_id、t、y_same、y_flip。保持／翻转a0和da必须逐元素相同。
- SAE基：R/confirm/f*/common_span.npz中的Q（1024×32）和selected_atom_ids；不重选原子、不修改原0.5任务信号门槛。
- 不重新取自然文本，不构造新方向，不加载检查点。独立结构／读出样本只保证本轮拟合与评价分离，不使已查看方向族成为前瞻测试。

## 6. Learning Task And Permitted Supervision

PCA/SVD只用结构集a。probe额外可用结构集信号t；不得用目标损失、e、da、I挑坐标、调秩、选正则或选原子。B翻转标签不另拟合一套probe：预测t与预测−t只是符号翻转，不是两个独立发现。

probe按每个rho分别拟合A、B各一条读出（每族四条），在独立A、B读出a0上同时报告同组解码和跨组解码。主要输出是t的平衡准确率和均方误差；阈值为预测值0，零预测记为0.5的平衡猜测，不按测试集调截距或阈值。

这些标签读出仅用于“信号可读性”控制。所有有符号作用可在事后使用原B导数，须明确这是带目标信息的解释，不得称作无标签或独立事前预测。

## 7. Model / Architecture And Frozen Variants

无需运行S7。所有分析保持原生输出坐标、原始量纲，不逐维标准化后再将坐标误当原生几何。下列空间是AI_PROPOSAL，必须在产生新作用图之前记录配置哈希：

| 空间 | 固定构造 | 回答什么 |
| --- | --- | --- |
| SAE-full | 原Q_S，完整秩32 | 原共同原子空间承载何种作用；保留旧定义的定位对照 |
| raw-SVD-k | 四格a按行平衡堆叠X，取右奇异向量前k列 | 主要原始能量是否主要是背景 |
| centered-PCA-k | X减同一个 pooled mean 后取右奇异向量 | 主要样本变化是否对应功能作用 |
| SAE-restricted-PCA-k | 对(X−pooled mean)Q_S做SVD，取右方向V_k，再令Q=Q_S V_k | 在原common空间内做同秩比较；不等于选了k个原子 |
| probe-span | 四条非零probe权重归一化后合并，SVD正交化，保留有效秩 | 可读任务方向是否承载实际作用；不命名为common |
| random-k | 原生1024维随机正交空间，同秩 | 排除单纯维数／任意投影解释 |

固定秩曲线k={1,2,4,8,16}，主要几何对照为k=8；原SAE-full另配random-32。probe使用自身有效秩，并给PCA/SVD/SAE-restricted及random同秩读数；不得把32维SAE与一维probe直接按捕获比例排优劣。

有效秩定义为s_j/s_1>1e-5，并报告1e-4的纯敏感性诊断；若s_1=0则秩为0。超过有效秩的k记NOT_IDENTIFIABLE，禁止用零奇异值／浮点噪声方向填满。任一族主要k=8不可识别时，该方法总体主要比较记INSUFFICIENT，不删族或临时换k。若边界奇异值差不清晰，报告(s_k−s_{k+1})/s_1；小于1e-5标记子空间边界不稳定，不作方向身份结论。

构造本身在中心化前后最多提供约17／16个精确信号维度；规划时首族检查支持此数值秩，但不是全族结论。原分析的PCA-32实现没有有效秩截断，本轮补审这一限制，不覆盖或改写其原读数。

## 8. Training Objective And Optimization

没有基座训练、SAE重训或优化器更新。probe使用解析岭回归：

\[
\min_w\ n^{-1}\|X_cw-t\|_2^2+\lambda\|w\|_2^2,
\quad\lambda=10^{-3}\operatorname{tr}(X_c^\top X_c/n)/1024.
\]

每个拟合格用自己的结构均值中心化，截距为 \(\bar t-\bar a^\top w\)。用FP64求解，可用256×256对偶形式；不扫lambda，不用测试准确率挑模型。零方差／非有限值记PROBE_UNIDENTIFIABLE。输出权重、均值、lambda、条件数和拟合集身份。

每条probe另用种子17/29/43生成配对随机符号标签，保持对内平衡。种子固定为SeedSequence([seed,family,rho_index,group_index])，rho_index=0/1对应低/高、group_index=0/1对应A/B；128对中恰好64个整对翻转、64个整对保持后随机排列，以免随机的微小标签相关被无噪声线性任务放大为分类准确率。仅在拟合集打乱，评价仍用真实t，不根据结果增添种子。

比较准确率时同时报告预测值RMS和MSE：幅度接近0却因符号达到较高准确率，不单独判作泄漏或有效读出。若打乱标签表现异常，应检查泄漏或原生几何捷径，不能据此将真实probe读数升级为机制。原生结构信号按构造近似低秩且线性可读，probe高分本来就可能很容易，因此它只提供定位参照。

## 9. Conditions, Seeds, And Checkpoints

沿用原全部条件与固定检查点身份，不增加模型／步长。random基在每族用SeedSequence([seed,family])、seed∈{17,29,43}生成1024×32高斯矩阵后QR；前k列形成嵌套同秩对照。该新低秩规则预先固定，不假称与旧脚本逐k独立QR完全相同；原32维对照须先复现。三组随机实现不是完整随机空间分布。

所有方法空间在结构集上一次拟合，两个步长、两种B规则、四源批次和高低rho共用。不能对翻转组另找更有害的空间。生成配置与脚本后先记录其哈希，再开始新投影读数；已看过数据的事实保持POST_HOC_EXPLORATORY。

## 10. Primary Metric And Frozen Analysis Plan

先复现[已有配对补查](/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/checks/pairwise_direction_audit_y4hq_pjj/result.json)。对一对更新位移定义：

\[
b_i=(\Delta a_{i,+}+\Delta a_{i,-})/2,\quad
s_i=(\Delta a_{i,+}-\Delta a_{i,-})/2,\quad
\Delta a_{i,t}=b_i+t s_i.
\]

b包含共同背景和无关变化，不能重命名为SAE common；t s是按已知任务信号配对得到的位移，不是参数梯度夹角。对任一正交投影P=QQᵀ：

\[
C_{P,sig}=\mathbb E_{i,t}[e_{i,t}^\top P(t s_i)],\quad
C_{P,even}=\mathbb E_{i,t}[e_{i,t}^\top P b_i].
\]

同样计算(I−P)下两项，并核对：

\[
I=C_{P,sig}+C_{P,even}+C_{\perp,sig}+C_{\perp,even}+R.
\]

**先在原生表征中读作用，不以工具表现作主结果。**取P=I得到原生信号项C_sig与信号不变项C_even，并对两个步长分别计算

\[
M_{sig}=[C_{sig,H,flip}-C_{sig,H,same}]-[C_{sig,L,flip}-C_{sig,L,same}].
\]

同算M_even和M_R，核对原注册M=M_sig+M_even+M_R。主要机制读数为M_sig，同时保留高重合A、B保持和B翻转各自C_sig的符号，以及C_even+R为何使实际I仍为负。没有一种工具成功也可以完成这一分析。

**再逐空间读定位。**高rho、翻转B、两个步长分别计算每个预列投影的C_P,sig、C_P,even及正交补；同秩超额贡献定义为\(\delta_P=C_{P,sig}-\mathrm{mean}_{3\ seeds}C_{random-k,sig}\)。另报D_P=C_P,sig−C_perp,sig，审计“主要落在该空间”的更强说法。全部单位为nat／目标。工具对照均为事后、描述性的条件区间；不以所有方法中最显著者宣布新机制。

- 聚合：先对±t配对，再在256逻辑对、4源重复、12方向族上等权平均。方法差在同一原始条目相减后聚合。
- 区间：复用R/analysis/bootstrap_indices.npz的family、source_repeat、target_pair、source_pair，共2000次；原seed=20260928。同一次抽样保留规则、rho、步长、方法配对。禁止把384条件格当独立重复。
- 空间与probe在bootstrap中固定，因此区间条件于拟合出的空间，没有覆盖重新拟合的不确定性，也不代表新模型／新方向族的确认性证据。
- 报告双侧95%区间。主分支要求两个步长同时满足判据，不从中挑一个。几何工具／秩曲线与probe为描述性对照，不按多个方法中最显著者宣布发现；若要正式多方法优劣检验，另设计未查看数据和多重性规则。
- 比值可附录报告，但分母接近0、正负抵消时标UNSTABLE；不得裁剪到[0,1]或将它叫因果解释率。
- 无样本、族或异常值排除；缺少一个必需格就记录INCOMPLETE，已有可核验结果可保留，但不出全量分支判断。

## 11. Secondary Metrics And Guards

每种空间同时报告三类量，避免高能量或高准确率冒充作用定位：

1. **静态结构占用**：分别在独立A/B读出上报告均值投影能量比例\(\|P\mu_D\|^2/\|\mu_D\|^2\)、去各自样本均值后的方差捕获率\(\sum\|P(a-\mu_D)\|^2/\sum\|a-\mu_D\|^2\)；报告A/B两值与min/max比及逐主方向分布。联合PCA若只被一组占用，写成单组主方向。均值分量与变化分量分开，不能只给pooled解释方差；零分母标UNDEFINED，不置0或加大epsilon掩盖。
2. **实际位移捕获**：\(\sum\|P(ts)\|^2/\sum\|ts\|^2\)，并对b另算。只用于几何，不决定帮助／伤害。不得为了做PCA而中心化da或e，删掉真正的背景作用。
3. **带符号损失作用**：四项分解、正负比例和绝对原单位值；帮助和伤害都保留。对原生任务差a(+)-a(-)也报告投影保留，但不叫SAE编码重构。

SAE原任务信号重构误差由a_hat差与a差比较，重现原失败，不修改门槛；子空间投影保留率与完整编码／解码误差是不同指标。高probe准确率不补救SAE失败，也不证明probe空间承载更新。

必须通过：全数据顺序／shape／hash核验；同一B规则对的a0/da相同；QᵀQ误差<1e-8；逐条一阶与四项闭合误差≤max(1e-7,1e-4×|I1|)；原C_S复现到同样容差。全程FP64分析，容差为工程保护，不是科学显著性阈值。

SVD/PCA基向量正负号任意，不用两个独立拟合轴的符号判定“任务方向相反”。主要几何读数均基于投影而不受换号影响；如需显示带符号坐标，固定该方向绝对值最大的载荷为正，保存换号规则。

## 12. Known Good / Known Bad / Known Confusing Cases

仅做保护符号和信息边界的小型数值检查，不新增模型训练：

- P=0／P=I：投影项为0／全部一阶项；互补项相反。
- 对内交换正负并同步交换t，配对重建和均值保持；只换标签时da不能变化，e和损失允许变化。
- rank=0／rank超出有效秩：明确返回空空间或NOT_IDENTIFIABLE，不补随机方向冒充PC。
- 大均值＋小可分类信号：raw-SVD首轴可以很大但无分类能力；中心化／probe与有符号作用应分别读取。
- probe高准确率但C_P,sig小：合法结果，不是实现失败；共同激活很多而C_S,sig≤0也合法。

## 13. Scientific Procedure And Stage Contracts

| 阶段 | 输入与操作 | 为什么做／输出 | 通过或停下 |
| --- | --- | --- | --- |
| 0 复现 | 核验R、完整性、配对顺序；复现原I/I1/C_S与已有配对补查 | 排除读取与符号错误；preflight.json、baseline_reproduction.csv | 原数值不闭合则停止依赖投影，记录FAIL_READOUT；仍可做资产清单 |
| 1 拟合坐标 | 只从结构a拟合SAE基、SVD/PCA、probe及随机空间 | 分离均值、主要变化和可读信号；bases/、rank_audit.csv、probe_fit.json | 不看e/da/I挑参数；秩不足只停对应比较，保留原生分解 |
| 2 交叉定位 | 同一e和da计算信号／非信号×空间／互补四项 | 找不利作用及抵消项；per_pair_terms.npz、signed_terms.csv | 每方法逐项闭合；不丢失条件 |
| 3 不确定性与对照 | 同一配对bootstrap；同秩比较；原子／PCA占用和probe独立样本评价 | 区分定位、方差和可读性；intervals.json、occupancy.csv、probe_eval.csv | 工具失败不停止其他独立工具；数据身份失败则停止相关结果解释 |
| 4 交付 | 写四段Summary及Detailed；三张必要图；科学解释待研究者确认 | 得到可以决定是否需新干预的证据 | 全部必需项有结果或具名失败；不按期望改条件 |

顺序不可反过来：不要先画漂亮common画像，再寻找能解释它的损失故事。

## 14. Algorithm, Output, And Provenance Contract

执行代码与数值产物写入新的执行目录：

`/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/posthoc/signal_localization_<UTC>/`

由接手Agent新建，禁止复用覆盖旧目录。建议入口analyze_signal_localization.py和plot_signal_localization.py；配置先从本协议明确写出，不允许运行中根据新后果改rank、正则或条件。

复用并先检查：

- checks/pairwise_direction_audit_y4hq_pjj/reproduce.py：配对分解与顺序核验。
- 原scripts/analyze_full.py：原bootstrap索引语义、聚合和signed projection；**不直接照搬PCA-32而忽略有效秩**。
- Research_System中原包scripts/mechanism_core.py：正交投影与损失闭合含义；本轮无需其Torch模型运行路径。

上面两条相对执行工程根`/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled`。复用数学和已存资产，新增CPU分析适配，不复用旧脚本的输出目录或覆盖入口。

产物至少包含registration.json（当前计划／代码／配置及输入身份哈希、已查看数据声明）、preflight.json、rank_audit.csv、basis_manifest.json、probe_fit.json、probe_eval.csv、signed_terms.csv、intervals.json、failures.json、manifest.json。signed_terms保留family/rho/repeat/step/rule/method/k/effective_rank及四项、R、I；逐逻辑样本数组供重抽样，不能只存总体均值。

研究阅读面放本目录summary.md、summary_cn.md、detailed.md；执行前可写NOT RUN骨架，不能预填支持性结论。图仅保留三类：①信号/非信号四项及净后果；②同秩位移捕获和带符号贡献；③原始能量/中心化方差与probe读出对照。生成文件留执行目录，日期阅读副本在daily_research_reports/0928/figures/，SOURCES.md记原路径和哈希。日期图链接从本目录为../../figures/。

失败记录必须写发生阶段、条件、错误、受影响推断、还能完成什么；缺工具不能伪造空结果为0。旧Protocol、Summary/Detailed、Anchor、Focus、模型、原始数组和原冻结分析保持只读；不commit/push，不提交新GPU任务。

## 15. Success / Failure / Insufficient Evidence

工程完成与科学分支分别报告。以下为本追加分析的AI建议，绝不覆盖原MODULATION_WITHOUT_NET_HARM：

- **原生作用分解支持当前解释：**资格通过，两个步长的M_sig与高重合翻转C_sig区间下界>0，高重合A及保持B的C_sig区间上界<0，并且C_even+R的减损足以使实际I仍为负。最多说明已查看数据中的任务信号分量带来相反损失作用，并被其他作用抵消，不说明SAE common是原因。
- **不支持或不足：**合格情况下上述符号可靠地相反，削弱对应解释；符号／区间混合、闭合失败、缺条件则保持不足。不能用某个工具较高准确率或捕获率挽救未成立的原生分量解释。
- **空间定位的独立读法：**对每个预列空间分别给C_P,sig、delta_P和D_P。C_P,sig与delta_P的两步区间下界均>0，才描述为相对这三组同秩随机对照有额外增损定位信息；再有D_P下界>0才能说净有符号作用主要位于该空间。某项上界≤0削弱对应定位解释，跨零或秩不足则未分辨。不同空间可同时承载重叠信息，不能将它们的贡献相加，也不按显著性挑冠军；这些条件区间不构成新确认性检验。
- **工具失败仍是完整结果：**SAE不承载主要不利作用、PCA只描述背景、或probe易读却无明显功能贡献，都能更新对工具及机制的认识。无需修好SAE；若所有候选空间均未定位，保留原生分解并说明位置尚未解释。

无论哪一支，都要回答：不利分量在哪里、较大的帮助在哪里、哪种工具看到了什么、哪种工具遗漏了什么。候选的唯一后续决定是**这些定位证据是否足以提出一个新的、针对性的表征干预来检验因果作用**；该建议须交研究者裁决，不改原Focus状态，也不自动进入事前预测或参数隔离。

## 16. What This Cannot Claim

没有新的净伤害证据；没有自然领域、长期训练或隔离收益结论；没有未见方向族确认；没有单原子因果干预。不能把b叫SAE common，不能把pooling后的最大PC叫“已证明的共同机制”，不能把probe预测t叫预测干扰。SAE任务信号重构失败保留；投影分析作为几何诊断仍可报告，但不得升级为合格编码代理。

## 17. Block Confirmation, Freeze, And Amendment Ledger

| 块 | 状态 | 来源与待确认范围 |
| --- | --- | --- |
| A 问题／边界 | AUTHORIZED_LOCAL_ANALYSIS | 承接现有作用定位；不要求SAE有效；具体分支仍为AI建议 |
| B 数据 | AUTHORIZED_LOCAL_ANALYSIS | 原数组和切分已核验；本轮全部12族事后分析 |
| C 标签权限 | AUTHORIZED_LOCAL_ANALYSIS | 结构标签只拟合t；目标导数只用于事后作用归因 |
| D 工具／空间 | AUTHORIZED_LOCAL_ANALYSIS | 固定SAE＋raw-SVD/PCA＋probe＋同秩随机；有效秩保护 |
| E 拟合 | AUTHORIZED_LOCAL_ANALYSIS | 无模型训练；解析probe固定正则，无调参 |
| F 指标／判据 | AUTHORIZED_LOCAL_ANALYSIS | 先原生信号及抵消项，再各工具同秩定位；科学支持判据仍是AI建议 |
| G 执行 | AUTHORIZED_LOCAL_ANALYSIS | 本地CPU分析与新目录产物；无GPU重跑、Git发布 |

AI一致性检查：问题与旧结论边界一致；数据与接口足够；任务标签不进入无监督空间；投影和probe角色分离；秩比较及配对统计明确；旧结果不覆盖。A—G的本地执行已由本轮用户指令覆盖；不把执行授权解释为科学结论批准。

接手Agent接到用户明确“按此方案执行本地追加分析”的指令时，可一次登记其覆盖的块和本地范围，核验一致性后再冻结新的配置与代码；无需为每个阶段反复请求同范围批准。若用户纠正科学对象或判据，先改这份唯一方案并保留修改记录。新读数产生后，不静默修改条件、指标或排除规则；变化须追加说明并保持事后证据身份。

执行勘误（2026-09-28，首次新投影运行在 `signal_localization_20260928T025000Z` 的首族护栏失败后）：原执行仅为 B 的 same/flip 保存有效 `C_S`；`source_C_S` 是占位零值。原生 A 的 SAE 投影仍可由保存的 `source_e`、`source_da` 和冻结 `Q_S` 直接计算，但不能用占位值作复现断言。仅将 `C_S` 原值核验限于 B 两规则；配对、秩、样本、指标、区间与判据均未改变。失败运行原样保留，修正代码在新执行目录重新冻结后运行。

执行实现修订（2026-09-28，第二目录全12族投影与核验通过后）：逐项 Python 抽样循环速度低于预算，在新区间产生前中断；已冻结的逐对项与原 bootstrap 索引保留。另写并登记 `bootstrap_signal_localization.py`，以配对样本的抽样频数一次聚合全部方法，计算与原索引循环完全相同的统计量。只改计算顺序，不改索引、样本、指标、区间或选择规则；中断与两阶段哈希在执行目录记录。
