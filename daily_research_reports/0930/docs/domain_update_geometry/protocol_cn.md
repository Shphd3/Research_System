# Protocol：domain_update_geometry v1

## 0. Approval Snapshot

**APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL_WITHIN_SCOPE；NOT RUN。**[Anchor](anchor_cn.md) · [Focus](../../focus_domain_update_geometry_cn.md) · [English](protocol.md)。实验角色：共同/领域更新结构的原因与操作化审计。

2026-09-29 研究者明确认可领域优先分析，要求完成共同点/领域特殊性、SVD、已训 SAE atoms 和完整激活模式分析，先写 Anchor/Protocol，必要时提交四卡 H100 Reserved，期间不再批准。本指令直接授权范围内实现、工程资格和完整分析，免除重复逐块审批；下列数值由 AI 在委托范围内明确，并非声称研究者逐项指定。未来科学解释 Unknown。无 LM/SAE 训练、Router、参数干预、旧裁决改写、commit 或 push。

一个实验包含三个必做部分：同记录采集与领域原型比较；谱/共同/特有/尺度分析；全 atom 激活和 decoder 子空间对应。主结果不支持也不跳过后两部分。完成所有事实记录，保留失败和空集合，不另选有利子群。

## 1. Terminology / Definitions

N8 记录为带原始类别的 256 词元自然学术片段。fit 为历史 512 条，定义均值、坐标和 atom 集合；readout 为另 512 条。二者有历史曝光，不称全新 CONFIRM。

输入原 token 索引0..254；观察位置 t=14,30,…,254，预测 token t+1。最后事件是255词元前缀→第256词元，与旧DCLM256→257不同。全部255输入位置用于描述性SAE激活，16目标用于聚合损失；每个预测位置看不到自己的未来目标。

c为2048维，a和逐记录残差r为1024维，W为1024×2048。e_it是单目标全词表NTP导数，尚未除16；G_i^last=e_i,254 c_i,254^T，G_i^16=(1/16)Σ_t e_it c_it^T。各自Gram为K^last/K^16；梯度余弦kappa在零范数时未定义。共同均值、领域均值偏离、共同激活和decoder覆盖是不同对象。

## 2. Anchor Alignment

主H1检验fit领域原型是否比整体原型降低readout梯度误差。SVD描述更新变化所在方向；SAE描述原生活动及独立选出的decoder方向是否覆盖这些变化。同秩随机方向、同规模随机分组及幅度对照限制竞争解释。只有一个核心实验；找到负K不是完成标准。旧受控Focus仅是历史背景，不持有新问题。

## 3. Tested Hypothesis

H1：独立记录上Q_D^last>0。H2：共同/领域/内部更新变化有可复现谱结构，超出大均值或范数解释。H3：fit定义的共同/领域富集激活复现，decoder子空间比同秩随机方向更多覆盖相关更新。H4：固定记录内平均对领域关系的影响超过相同规模任意分组。H2—H4为预设描述性诊断，不能救回主结果，失败也不抹掉H1。

## 4. Rival Explanations

| 竞争解释 | 区分比较 | 边界 |
| --- | --- | --- |
| 整体均值已足够，领域偏离是抽样波动 | 领域/整体原型；双侧记录重采样；fit标签置换 | 记录独立性，不是论文/来源总体 |
| 大梯度造成领域差异 | 原始/单位梯度Q及谱；范数分布 | 单位梯度不再是原始SGD作用 |
| 共同均值被误当低维变化 | raw/fit-centered谱；共同/领域/内部能量 | 有限样本秩不是总体维数 |
| 目标词、难度、子领域解释领域 | 目标重合、loss/norm分层及双向子领域迁移 | 不识别语义因果 |
| 平均操作本身使任何组稳定 | 16目标与last；1/4/16/64条同规模随机分组 | 非整篇文档梯度，位置/目标数量也变化 |
| 同atom但幅度不同仍称共同 | 频率/正幅度双重规则与留出复现 | 激活相近不保证梯度相近 |
| decoder集合太大或冗余 | rank资格、最多64atom、同秩随机和native-a PCA | 不把全字典张成输出空间当成功 |

## 5. Data Construction And Provenance

原样复用 `/data/250010109/MoE_Router/experiments/20260925_sae_domain_activation/selected.jsonl`，SHA256=`7e8858adfbf1ead8330937dc147eee3eb815be9025e620e53c0af0fc86d155d9`。共1024条，fit/readout各512，每category/split64。类别映射：cs.CL/cs.CV→computer_science；math.AG/math.NT→mathematics；physics.flu-dyn/physics.optics→physics；q-bio.GN/q-bio.NC→biology。领域及子领域顺序按此固定。不按结果重新抽样。

N8 revision=`6ae613ba744ee56f645aee9c577d04f7e3d48b30`；原fit/test哈希分别为`647ce2662da53b31520c11203657338f237fd4be02a299c05203f17d4b1fedd1`、`440531b2c6670eec8c853a0dbc0b7e0b10e3eede5943f36ec0f1f8d6fda1148d`。`source_group_scope=record_only_paper_id_unavailable`：无法保证不同记录来自不同论文。来源曾用于审计，不称全新确认或未见预训练文本。

预检源哈希、256长度、词表范围、每类数量、ID和完整input哈希唯一及跨split无精确重复。检查跨split连续5-token shingle Jaccard≥0.80，不读取梯度；若发现近重复，保留原面板但标记相关记录推断INELIGIBLE_DEPENDENCE，不能悄悄删样本。保留原text/ID/token哈希；不向输入添加领域名，不生成新的语义标签。

OPS为fit每子领域按SHA256(`domain-geometry-20260930|sample_id`)排序前2，共16条，属于fit工程子集，不增加独立证据。full解释readout前固定索引及atom选择代码。历史激活结果已知，不声称研究项目设计盲于历史结果。

## 6. Learning Task And Permitted Supervision

不训练预测器、LM或SAE。原型、SVD轴、atom集合和描述性分层由fit确定。领域标签可构造领域均值；真实目标和梯度可用于解释K，因此不是事前仅表征预测。

atom选择只允许fit激活与领域标签，不使用任何e/K/loss/目标身份/更新覆盖效果。fit均值、轴和ID先保存，再生成readout总结。冻结后目标/loss/norm诊断属于描述性分析。高富集分数不自动给atom赋“数学/生物语义”。

## 7. Model / Architecture And Frozen Variants

固定 `/data/250010109/MoE_Router/experiments/20260920_s7_lambda0p1_from_scratch_4h100/runs/S7_lambda0p1_from_scratch_4h100/milestones/token_033000000000`。state SHA256=`c30b78e5bcba8f0a09c5e215389be86778874e87fcbb9fe5211175d370bb0803`；tokens_seen=33000000000，optimizer_step=125894。8层dense S7，主干281431040参数。W=`model.blocks[7].attn.o.weight`，无bias、1024×2048。SAE61471024参数、width30000、TopK32、hook7，在注意力输出投影后、残差相加前；历史重构系数0.1，sidecar不替换前向。

FP32 eval，关闭TF32/autocast；末端全词表logits/logsumexp CE转FP64。冻结参数和活动buffer，不加载optimizer。各记录/位置保留自己的残差。归一化、去均值、聚合、投影是各自命名的分析变体。decoder取模型实际归一化列，不能猜测方向。

`/data/share/Qwen3-0.6B-Base`仅取tokenizer展示词元上下文，不加载其权重；实际输入为原面板预分词ID。

## 8. Training Objective And Optimization

**NOT_APPLICABLE：没有优化。**每记录测16个CE，各分母1有效目标；聚合为算术均值。重构/AuxK不进入e/G/K；LM与SAE更新数均0，重复分析不计训练词元。

遵循[可观测合同](../../../../docs/training_observability_contract.md)：训练/optimizer tags记NOT_APPLICABLE；记录measurement/ntp_loss（nat/目标）、measurement/valid_targets_seen、records_seen、activation_positions_seen、阶段时间、峰值GPU allocated/reserved和finite/freeze资格。计数对应记录×16目标、记录×255激活位置。恢复只可新attempt或验证哈希的已完成不可变shard，不重复行/计数。

## 9. Conditions, Seeds, And Checkpoints

一个检查点。主last原始梯度；必做last-unit、16目标raw/unit、c_last/a_last/e_last/c_body_mean/a_body_mean、SAE last/body-frequency/body-amplitude，不选赢家。顺序seed20260930；bootstrap20261001、2000次；标签置换20261002、999次；随机分组20261003、100次；Gaussian-QR seeds31/43/59。谱迁移ranks1/2/4/8/16/32/64/128/256，受数值秩限制。SAE/native-a投影ranks8/32/64，缺秩按实际报告，随机对照匹配实际秩。

## 10. Primary Metric And Frozen Analysis Plan

F/R为fit/readout；g为last梯度展平，μ为fit整体均值，μ_s为fit领域均值。平衡面板下记录等权也使领域/子领域等权。

\[
Q_D=1-\frac{\sum_{j\in R}\|g_j-\mu_{s_j}\|^2}{\sum_{j\in R}\|g_j-\mu\|^2}.
\]

通过Gram元素及均值权重用FP64计算。配对描述去除自身配对，但原型误差必须保留每事件平方范数。无截尾、符号平衡或异常值删除。报告分子/分母、单位、Q及范数。若分母≤测得梯度平方数值误差的100倍或≤1e−12，主结果INSUFFICIENT_LOW_VARIATION。

2000次bootstrap分别在F和R的8个子领域内各有放回抽64条，每次重算原型，linear quantile给双侧95%区间。该区间条件于记录，不覆盖未知论文聚类、来源和检查点变化。999次置换在fit全体记录间随机置换领域标签并保持原数量，readout标签固定，重新计算Q；p=(1+#Q_perm≥Q_observed)/1000。它是可交换性假设下的标签关联诊断，不是随机化因果实验。

支持：资格通过、区间下界>0且p≤0.05；不支持：资格通过、上界≤0；其他为主方向判断不足。零门槛检验关联，不规定Router实用收益。只有一个主检验，其余区间/rank/atoms均描述性，不作未校正逐特征发现。历史曝光随所有结论保留。

## 11. Secondary Metrics And Guards

### A. 领域关系、共同性与尺度

last/16各给fit/readout原始K与kappa的4×4均值、SD、中位数、正负比例、计数和范数分布；同领域去自身配对。pair数不是独立样本数，不确定性以记录为单位。另给fit→readout领域平均梯度内积、整体μ、领域δ_s和内部残差能量。fit总二阶能量=均值能量+领域间能量+领域内部能量，relative closure≤1e−6；领域间rank≤3是构造约束。

单位梯度Q及16目标Q使用同一bootstrap，不选最好条件。子领域迁移：每领域只用第一个category的fit均值预测第二个category的readout，再反向；两项是次级稳健性，不是新确认。

m=1/4/16/64记录，100次固定抽样：各split/domain重新打乱取前m条构成4个真实领域均值；全局重新打乱取4m条分成4个不重叠混合组，各m条。除原面板平衡外，不声称抽出的单组子领域平衡。报告同标签fit/readout组均值对齐及真实领域减随机对齐；m=1定义保持一致。随机平均只控制平均操作，不能消除所有来源结构。

混杂表含目标ID重合、仅fit16目标估计的目标频率、CE、c/e/梯度范数和pair乘积。fit损失及log梯度范数四分位边界原样用于readout；每个相关cell≥20对才给分层领域对比，明确稀疏cell和覆盖率，不能从主分析删记录。相同/不同目标单独描述。该分析不能隔离语义因果或宣称排除一切词汇因素。

### B. SVD及原生表征联系

last/16梯度、c_last/a_last/e_last/body means、SAE last/body-frequency/body-amplitude全部保存fit样本可见谱。分别分析raw二阶矩、fit去均值变化、行单位归一化几何。Gram负特征值小于−1e−7×最大特征值则失败；容差内负数记录后裁0。数值rank为λ>1e−10×最大λ。报告participation ratio、谱熵有效秩、50/90/95%能量所需方向数及分母。

只用pooled fit轴，不按领域单独转轴。去均值梯度用中心化跨split Gram计算readout在fit右奇异方向上的坐标，逐rank报告留出能量覆盖；其他向量同理。仅fit谱不能证明总体结构稳定。二维图用前两个fit轴，注明readout覆盖比例。表征/SAE与梯度的中心化Gram alignment使用全部非对角元素，另给标签块偏离版本，仅描述性。几何相似不等于预测或因果使用。

### C. 已训SAE的完整激活模式

采全部255输入位置、1024记录、30000atoms的TopK索引和正值。value>0才算发放；所有表保留零/未观测atoms，不能称全局dead。

每split×domain×atom及pooled split保存：正token频率、记录出现率、无条件幅度均值/SD、正激活条件均值/SD和10/50/90%分位数、最大值及原记录/位置、条件decoder贡献范数、last对应量。以记录为不确定性单位时先记录内汇总。每记录保留30000维frequency/amplitude、活动atom数、正TopK数量、激活熵/有效数、a范数、重构相对平方误差/cosine，以及目标位置e·(a−重构)（敏感性，不是实际损失变化）。

位置分箱0..31、32..63、…、224..254，保留每箱长度及所有atom的counts/sums。相邻位置持续性：support Jaccard、逐atom连续激活次数/机会、run-length1..255直方图；记录边界必须截断。共激活统计每token所有正atom无序对k<l，保存每split/domain全部出现过的稀疏pair counts及边缘counts；lift=count×tokens/(count_k count_l)，罕见高lift不当显著性。图只用fit count≥20、按count降序/atom ID排序前100边/领域，再看同边readout；完整稀疏表仍保存。

共同选择分别对body/last执行：所有领域频率≥0.01(body)或≥0.05(last)，最大/最小频率≤2，正条件幅度最大/最小≤2。领域富集：p_s达到相同门槛，(p_s+1e−4)/(其他领域平均p+1e−4)≥2，并排除共同集合。一个atom可富集多个领域，报告交集；这不是语义相同或独占的证明。保存所有合格ID，空集合不放宽。

共同展示/投影取min-domain频率最高前64，tie按ID；领域富集按enrichment、p_s降序、ID升序取前64。body集合是主decoder集合，last选择单独作稳健性；先冻结再readout。全部atom都有留出效应；共同规则/富集符号和比例是否复现仅描述，不作多重逐特征显著性。示例来自fit最大激活原词元窗口，不造语义名。完整模式距离用全部30000维cosine、归一化profile TV和support overlap，比较同领域跨split与不同领域。

### D. SAE与更新结构连接

取fit body共同及4个富集集合的归一化decoder列，经SVD生成rank8/32/64或可用秩的正交基；重复/共线列不重复计秩。同秩native-a fit PCA与3个Gaussian-QR随机空间必做。SAE编码a，因此对应full-a，不暗换成c。

last/16均算PG、K_P及K−K_P，报告trace能量覆盖、fit共同均值/领域偏离覆盖、readout投影4×4带符号均值、投影Q_D、readout非对角K重建误差。显式小梯度检查投影+补空间relative≤1e−5。不同集合P可重叠，覆盖比例不能相加。空/低秩明确报告，rank0覆盖0不等于SAE无信息。

全部30000个单位decoder方向d_k另存各domain/split的单目标方向梯度能量E[(d_k^T e)^2||c||²]，并关联发放频率。这区分激活与输出方向敏感性；atoms非正交，其能量不可加成总能量。全部仅描述，不能事后按高梯度选择进入注册投影对照。

### E. 数值与冻结资格

last完整前向W autograd对ec^T，以及16目标均值对16个外积平均，relative Frobenius≤1e−5；非目标位置导数范数≤目标导数1e−7。Wc与a relative≤1e−5；捕获a等于native SAE input。tail与full CE绝对≤2e−5；精确重复编码/CE检查；buffer及内存state digest不变，checkpoint前后SHA一致。所有梯度有限；零范数保留、normalized标undefined，超过1%则归一化推断不足，raw资格单独处理。SAE维度、索引、非负、decoder单位范数、TopK≤32及重复编码通过。

## 12. Known Good / Known Bad / Known Confusing Cases

全量前验证：合成稳定领域原型产生正Q；随机标签不自动通过；相同领域/整体原型Q0；错误记录顺序拒绝；last/16外积与显式梯度一致；均值分解闭合；负非对角与PSD共存；P+补空间闭合；重复atoms降秩；频率相同但幅度差异过大不算共同；TopK零值不计；run-length跨记录重置；split重复拒绝；故意NaN失败。均为工程检查，不作自然语言发现。

## 13. Scientific Procedure And Stage Contracts

| 阶段 | 目的、输入→操作→输出 | 通过/失败/交接 |
| --- | --- | --- |
| S0 | 已授权文档+面板→schema/hash/曝光/重复→manifest | 来源缺失或身份错误即停；依赖异常标记，不悄悄删样本 |
| S1 | OPS16+检查点→native/gradient/SAE/freeze及资源→smoke receipt | 数学/数值护栏全通过；不据readout选参数 |
| S2 | 面板+PASS→4个独立GPU采集shard→c/a/e、16梯度、全位置SAE/损失 | 逐记录/目标核数；必要记录异常即停而非剔除 |
| S3 | 仅fit→原型/谱轴/atom集合→fit registration | ID、规则、轴和hash先冻结 |
| S4 | 冻结fit+readout→主Q/区间、谱、尺度、激活、投影 | 主负结果也完成全部诊断；失败定位到阶段 |
| S5 | 收据+结果→核验、图、双语Summary/Detailed | 分开工程完成、注册比较和Unknown人类判断 |

Smoke可独立allocation，也可在同一个已授权分阶段allocation开头执行S1；后者job命名`*-analysis`，代码必须在S1失败或1.5倍余时估计超预算时阻止S2，并非免Smoke。提交前本地已知案例测试；不能预先把Smoke写PASS。

执行面acp，profile=`h100-4-reserved`，image=`shphd-lite-0911`，单节点4个独立worker，无跨worker梯度平均。物理参数由[执行envelope](../../../../docs/execution_envelope.md)解析。总≤24GPU小时、单allocation≤6小时、产物≤50GiB；本地准备/有界只读分析≤60分钟。不自动换资源或新增全量sweep。工程失败修复保留原证据，新attempt记录代码变更；首测后科学内容冻结。无更长监控指令时启动观察≤5分钟，排队则交付已有job而非重提。

## 14. Algorithm, Output, And Provenance Contract

执行根 `/data/250010109/MoE_Router/experiments/20260930_domain_update_geometry/`，attempt为`runs/<UTC>/`。研究文本在本仓库，代码/原始数组/日志在执行根。模块`prepare.py`、`collect.py`、`analyze.py`、`run.py`、`test_contract.py`、`plot.py`；提交前记录实际hash。复用已读0930 `core.py` loader/capture，适配向量CE和位置；读取底层model/SAE源码。runtime复用已有offline依赖，不复用旧二元任务/21B数组。

| 产物 | 必须内容 |
| --- | --- |
| data_manifest.json/selected.jsonl | 原hash、ID顺序、类别/split、位置、曝光/重复审计 |
| registration.json | Anchor/Protocol/config/code/source哈希、授权、种子、阶段、检查点 |
| smoke_receipt.json | 各护栏误差、设备/内存/时间和full估计；执行后才PASS |
| collection/shard_*及收据 | 16位置c/a/r/e、loss/targets；last/body；16均值梯度；全位置SAE；精确计数 |
| fit_registration.json/fit数组 | 均值、轴/谱、atom集合/排序、随机基/seed；readout解释前冻结 |
| primary.json/domain_relations.csv | Q、MSE、CI/置换、资格、4×4raw/normalized及counts |
| spectra.csv/谱数组 | 全样本可见奇异/特征值、rank、fit/readout能量、共同/领域/内部 |
| activation_stats.csv/activation_patterns.npz | 含零的30000atoms、各split/domain、频率/幅度/分位数/上下文，body/last/位置/run统计 |
| coactivation/*.npz及模式表 | 全部观测稀疏pair与边缘；fit显示边；全atom距离 |
| atom_sets.json/atom_replication.csv | 共同/富集ID和规则、交集、留出复现/空集合 |
| atom_gradient_energy.csv/projection_results.csv | 全atom方向敏感性；SAE/PCA/random子空间、秩、覆盖、带符号K、重建/Q |
| scale.json/nuisance.csv | 尺度/随机组、子领域迁移、混杂分层/覆盖 |
| verification.json及必要failure.json | 必需文件/计数/hash、checkpoint冻结、阶段资格/失败、人类判断Unknown |
| figures及来源清单 | K/kappa矩阵；raw/centered谱与迁移；共同/领域/内部；全atom分布与fit选热图；位置/持续/共激活；SAE/random覆盖；尺度 |

四worker按记录index mod4分工，不重复记录。稀疏SAE数组为事实来源，每项统计可追到字段/公式。聚合梯度可memmap，last K可因子乘积计算。pair不确定性处理共享端点；不能把旧1024个离散对填0伪装完整K。

runner保存追加阶段日志、不可变源码快照、设备/image tuple、持久pod log和失败。输出根非空则拒绝。checkpoint、面板、源码、科学合同SHA可追溯。Smoke工程修复记录，结果驱动变更需附资格影响的修订。

## 15. Success / Failure / Insufficient Evidence

工程COMPLETE要求所有必需阶段/产物，或明确局部失败/空结果。主分支仅按§10。H2报告可重复能量和均值/范数解释，不临时造低秩门槛；H3分开激活复现和梯度覆盖，同秩随机限定含义；H4与任意分组比较，不能救回H1。缺来源、代数失败、freeze失败或主数据无效使相关证据ineligible，不能改称语义发现。

## 16. What This Cannot Claim

不是新封存确认、论文独立总体推断、语义因果、所有语言分组、atom语义纯度/因果使用、不可消除条件方差、实际有限步伤害、事前c-only预测、训练收益或expert隔离。所有结论条件于状态/矩阵/来源/尺度。四均值低维和样本rank上限是数学约束。旧NON_SUPPORT、MODULATION_WITHOUT_NET_HARM及未运行分支均保持。

## 17. Block Confirmation, Freeze, And Amendment Ledger

| 块 | 来源及状态 |
| --- | --- |
| A 问题/边界 | 用户认可领域共同/特殊分析，HUMAN_CONFIRMED_DIRECTION |
| B 数据 | 已核历史面板，AI_SPECIFIED_UNDER_EXPLICIT_DELEGATION，明确曝光 |
| C 任务/监督 | 标签/梯度解释，不冒称仅表征预测；在认可范围内 |
| D 模型 | 已核S7/SAE，同状态映射；AI操作化 |
| E 目标 | 冻结纯NTP测量、无训练；AI操作化 |
| F 比较 | 原型主比较及必做SVD/激活/投影/尺度；AI操作化 |
| G 执行 | 用户明确4H100 Reserved；本合同给有界预算/阶段 |

本次不再审批的明确委托授权上述范围内选择；不伪造逐项确认，也不重复询问。注册前核固定目标、因果位置、SAE site、投影维度、fit/readout、不确定性单位、完整激活覆盖和预算；审计结果与hash一起记录，不预设PASS。

首次S1测量前冻结科学正文。执行/结果状态写独立追加记录，保留本NOT RUN历史快照。实质偏差追加日期、原因和资格影响，不能暗改原合同。人类结果解释及后续优先级在确认前保持Unknown。
