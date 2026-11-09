# 完整记录：domain_update_geometry

[摘要](summary_cn.md) · [Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_12_domain_update_geometry/17_12_domain_update_geometry_anchor_cn.md) · [冻结Protocol](protocol_cn.md) · [English](detailed.md)

**终版文本 R2；完成 reasoning auditor 审计，不代表科学问题关闭。** 结果资格：测量 COMPLETE；面板描述 BOUNDED；总体方向推断因 percentile 区间未校准而不足；原始程序 NON_SUPPORT 保持；人类科学判断 Unknown。以下 R 指[不可变运行结果](/data/250010109/MoE_Router/experiments/20260930_domain_update_geometry/runs/20260929T193805Z/result)，A 指 R/analysis，V 指[首次事后审计](/data/250010109/MoE_Router/experiments/20260930_domain_update_geometry/reviews/20260929_result_audit)，V2 指[本次终版审计](/data/250010109/MoE_Router/experiments/20260930_domain_update_geometry/reviews/20260929_reasoning_audit_final)。

## 0. Quick Recap

目的：直接研究真实文本更新需求与领域、表征和已有SAE的关系。主假设检验当前经验领域均值描述器是否优于整体均值，而非所有领域结构是否存在。实际last Q=−0.005715；程序输出NON_SUPPORT，但总体方向推断不足。领域平均激活频率模式跨split复现，样本估计的梯度方向留出覆盖有限；fit选出的共同body集合在rank64、pooled readout、单目标能量比较中高于三个随机空间，富集集合在此比较中低于随机。未据此否定所属领域选择性作用、证明干扰机制或支持专家隔离。

## 1. Terminology / Definitions

| 对象 | 具体含义及计算 | 为什么分析；不证明什么 |
| --- | --- | --- |
| c / a | W的2048维输入 / 1024维原生输出，a=Wc | 区分SAE实际编码对象；SAE不是c的同义词 |
| e | 当前真实目标的纯全词表CE对a的导数 | 描述输出需要如何改变；带目标信息 |
| G / K | 单位置G=ecᵀ；K为所选W参数块的梯度Gram | 一阶共享更新联系；不是原生表征或全模型所有参数的梯度 |
| mean16 | 16个固定目标外积的平均 | 观察尺度；不是平均c与平均e的外积 |
| μ / δ_s | fit整体均值 / 领域均值减整体均值 | 分开共同方向与领域差异；四领域偏离秩≤3是构造事实 |
| Q_D | 1−领域原型MSE/整体原型MSE | 评估这个描述器的留出改善；不检验所有领域信息 |
| z / atom / P | SAE正系数 / 归一化decoder列 / 所选列张成空间的正交投影 | 静态激活、方向覆盖分开；不同P不可加和 |

仅更新W、保持上游输入与其他参数固定，并采用共同标量SGD时，ΔW_A=−ηG_A和Δa_B=−ηe_A(c_Aᵀc_B)是精确关系；在当前状态的一阶展开才有ΔL_B=−ηK_AB+O(η²)。本轮只测G/K，不实施有限步；不推断其他优化器或长期训练后果。选取末块是因为其输出之后没有跨位置注意力混合，单目标只对应一处W使用；这个条件不能直接推广至中间层。

纯CE误差信号还满足 \(e_i=J_i^\top(p_i-\mathbf 1_{y_i})\)，其中 \(J_i\) 是当前记录的logits对a的Jacobian，p为预测概率，y为真实目标。不同记录的J、p、y同时变化，所以e不是独立于表征的外来随机量；它的几何与K相近也不是隔离了目标词或下游机制的因果证明。

SAE输出方向投影对应PG，投影与补空间的K贡献精确相加。能量覆盖是 \(\sum_{i\in R}\|PG_i\|_F^2/\sum_{i\in R}\|G_i\|_F^2\)，只测K的对角总量；有符号相容性来自非对角 \(K_{ij}\)，不能由该比例直接代替。

## 2. Anchor Link And Decision Point

用户明确认可领域优先方向，授权SVD、已有atoms及完整激活分析，并授权必要四卡H100 Reserved；文档先于提交。具体数字在委托内操作化。一个核心观测实验的主结果不控制后续诊断是否执行。下一决定仍是选择未来语言关系/观察尺度；旧问题、旧裁决没有修改。

## 3. Protocol Freeze, Conformance, And Deviations

首次Smoke前冻结：英文Protocol SHA256 `b8b08172ebc4c044fe7206c8008d4667b6077363c4e53ea124e1ef5c4ccc54e4`；中文 `f56042c6225696e1bdc65dd7093d741049534ba12d3b19b25805d4baf66c4966`。完整源码/设计/面板哈希见R/registration.json及R/source快照。

| 合同项 | 实际 | 资格/证据 |
| --- | --- | --- |
| 状态、矩阵、纯NTP、冻结 | 精确33B，末块attn.o，0次LM/SAE更新 | PASS；Smoke及checkpoint前后hash |
| 四领域、每子领域每split64 | 1024不同record IDs，无遗漏/重复 | PASS；data_manifest、collection_receipt；不同ID不证明统计独立，论文依赖Unknown |
| 16目标、255位置 | 16384目标、261120激活位置 | PASS；verification.json |
| 2000重采样、999置换 | 按注册seed/分层/重估原型执行 | 实现相符；区间覆盖有下述统计限制 |
| fit选atom/轴、readout测量 | 选择及轴先保存，全部必做分支完成 | PASS；fit_registration、atom_selection_frozen、spectral目录 |
| 同秩SAE/PCA/3随机对照 | 实际rank8/32/64，9类空间，共54结果行 | PASS；projection_receipt及表 |
| 数值与资源 | H100实际设备、230.05秒runner、约18.63GB产物 | PASS；4卡Reserved；未接近6小时/50GiB预算 |
| 图形 | 9张图，主Q图原误差条未正确显示点估计外区间 | 原件保留；V新图只修绘图，未改指标/阈值 |

没有采集重试、样本剔除、提前停止或科研阈值修订。首次事后工作含bootstrap代数审计、已有全atom表的描述性相关/集合交集汇总、阅读表和绘图修正。本次R2根据用户要求修订结果解释，额外从已存Gram核对§5的精确风险恒等式，保留修订前文件于V2/before；未重新采集、运行统计检验、拟合模型或修改注册结果。

**统计限制。** 对已注册分层有放回重采样，类别c的经验协方差迹记v_c，类别样本数n_c=64。原型重估带来的预期平方误差增加为Σ_c n_c v_c/N²。整体N=512；四领域各N=128后等权平均，额外误差更大。实算整体增加0.213213，领域增加0.852853，差0.639640。以两项期望MSE之比解释中心移动，得到Q≈−0.011650，接近实际bootstrap均值−0.011636，而原点估计−0.005715；**期望的比不等于比的期望，这只是中心偏移的核对，不是修正后的估计或区间。** 区间不含点估计本身不是普遍错误判据，但这里有明确二次估计量偏差来源，名义95%覆盖未验证。有限面板误差保留，总体方向证据不足；不把原NON_SUPPORT当作已校准的否定。[首次审计](evidence/review.json)

**R2推理审计修订表。** 对应[12项可追溯发现](evidence/reasoning_audit_final.json)：

| 推断缺口 | 终版修正 |
| --- | --- |
| 领域结构存在性与原型效果混用 | 只判断当前经验均值描述器；保留真实效应弱与高维估计方差两个竞争解释 |
| 注册程序字段与统计资格混用 | NON_SUPPORT原值保留；总体方向推断不足另列，不重写阈值 |
| SVD维数、输出投影秩及能量分母混用 | 区分完整W梯度方向、a方向和PG投影，见§7 |
| SAE能量与相容性混用 | 区分K对角trace与非对角有符号关系；限定pooled readout比较 |
| 领域平均模式与单记录能力混用 | cosine只指领域均值；完整注册统计不等于高阶/因果穷尽 |
| e构造关联当作独立机制 | 明示K由c/e构造及CE链式导数，保留共同变化解释 |
| 控制目标被预设为去混杂 | 总关联与条件关联并列，目标属于任务，见§13三分支 |
| 文档终版与科研结题混用 | 终版仅指结果文本；人类判断和新设计仍未确认 |

## 4. Actual Setup

模型是fresh S7、8层dense主干281431040参数，附61471024参数SAE；λ_rec=0.1是训练历史，本轮只取NTP。checkpoint为`20260920_s7_lambda0p1_from_scratch_4h100/runs/S7_lambda0p1_from_scratch_4h100/milestones/token_033000000000`，optimizer_step125894，state SHA `c30b78e5bcba8f0a09c5e215389be86778874e87fcbb9fe5211175d370bb0803`。

W=`model.blocks[7].attn.o.weight`，1024×2048、无bias。SAE位于W之后、残差之前，width30000、TopK32；重构不插入LM。FP32 eval、无TF32/autocast，tail全词表CE使用FP64，保留各位置自己的残差。Qwen3-0.6B目录仅提供原tokenizer，不是测量模型。

输入为历史`20260925_sae_domain_activation/selected.jsonl`的256个token；输入0..254，输出位置14,30,…,254预测15,31,…,255。computer_science(cs.CL/cs.CV)、mathematics(math.AG/math.NT)、physics(physics.flu-dyn/physics.optics)、biology(q-bio.GN/q-bio.NC)，每类别fit/test各64。原面板SHA `7e8858adfbf1ead8330937dc147eee3eb815be9025e620e53c0af0fc86d155d9`。

这是历史曝光面板的描述性复现，不是新封存确认。record ID及输入hash唯一；跨split精确重复和5-token Jaccard≥0.80近重复均0，但没有论文ID。原文窗口可含跨领域/格式内容，源类别不等于纯语义。

无训练数据更新、无优化器步骤；fit只用于分析原型、轴及集合，readout是记录级留出。bootstrap seed20261001，置换20261002，随机组20261003，随机QR31/43/59；四worker按记录index mod4分工。旧21B激活、旧MLP矩阵数组及旧二元tail均不复用。

## 5. Metrics And Registered Decision Rules

主Q无量纲，原始梯度MSE单位为W坐标中的平方梯度单位；注册支持须区间下界>0且p≤.05；不支持须上界≤0，否则不足。低方差/测量失败另有资格要求。程序机械触发NON_SUPPORT；审计不能用未校准区间完成总体方向判定，故该推断不足。单位梯度、mean16、谱、atoms、尺度是描述性次级证据，不能替代有效主推断。

**为什么负Q不等于没有领域结构。** 令 \(\widehat\mu_s^F,\widehat\mu_s^R\) 为fit/readout领域均值，\(\widehat\mu^F,\widehat\mu^R\) 为整体均值，\(\widehat\delta_s^F=\widehat\mu_s^F-\widehat\mu^F\)，R同理。此平衡四领域面板上定义

\[
B_F=\frac14\sum_s\|\widehat\delta_s^F\|^2,\qquad
H_{FR}=\frac14\sum_s\langle\widehat\delta_s^F,\widehat\delta_s^R\rangle.
\]

利用各split领域偏离之和为零，直接展开平方误差可得精确关系

\[
\operatorname{MSE}_{D}-\operatorname{MSE}_{0}
=B_F-2H_{FR},\qquad
Q_D=\frac{2H_{FR}-B_F}{\operatorname{MSE}_{0}}.
\]

last的B_F=0.643336、H_FR=0.014834，因此MSE差=0.613669；mean16分别为0.043553、0.005514，差=0.032525。已从完整冻结Gram直接核对，误差<1e−14。[算术审计](evidence/reasoning_audit_final.json) 这说明两个split的经验领域偏离可以略同向，但采用整个fit偏离仍不足以带来收益；它没有把H_FR变成显著总体效应，也没有验证收缩或其他估计器。这是既有测量的恒等式核查，不是新实验发现。

## 6. Evidence Lineage

| 结果 | 原始/中间证据与计算 | 观察及资格 |
| --- | --- | --- |
| 领域原型 | collection→A/gram_matrices→冻结stats.py→primary | Q−.005715；描述合格、区间未校准 |
| 共同/领域/内部 | 同Gram→common_decomposition | .19%/.58%/99.23%；closure1.3e−16；fit描述 |
| SVD迁移 | 同Gram与测量c/a/e→spectral fit轴→跨split坐标 | top64梯度3.18% vs a53.18%；条件于当前fit方向 |
| 激活复现 | 全位置indices/values→activation_stats/patterns→fit集合→readout | 99共同中65同规则复现；源类别关联 |
| decoder覆盖 | 同激活集合+原decoder→正交P→PG | common rank64 8.96%；直接代数投影，不是因果使用 |
| 目标/误差关系 | measured_events及K→nuisance/kernel_alignment | 同目标cos .193；e alignment .903；描述性、含目标 |
| 尺度 | 原K→100固定随机抽样与跨子领域原型 | mean16/m64对齐.104 vs .074；无总体CI |
| 推断/图审计 | 已有Gram、bootstrap数组、primary→V/review.py | 未重测；偏差说明和端点绘图修正，原件保持 |

各表的具体哈希与读取副本变换由[evidence/origins.json](evidence/origins.json)、[图来源](../../../../../../../daily_research_reports/backup/2026/09/0930/figures/domain_update_geometry/origins.json)、R/registration和V/review共同追溯。独立性单位最多是记录，不将配对、tokens、atoms或随机基当独立实验。

## 7. Main Results

主MSE：整体107.370350，领域107.984019。last-unit Q−.005533；mean16 Q−.005060；mean16-unit Q−.005182，均没有有限面板改善。双向跨子领域last Q−.011600/−.012194，mean16−.011665/−.010279。p=.022只表明原统计量高于多数已生成的随机标签结果；其总体检验解释需要标签可交换性及记录依赖假设，且不意味着优于整体原型。[主结果](evidence/primary.json)、[尺度](evidence/scale.json)

SVD：centered last参与比238.72、90%fit能量需251方向；mean16参与比399.80、需409方向。rank64 readout覆盖c34.50%、a53.18%、e18.15%、SAE频率56.62%、SAE幅度70.80%，梯度last3.18%、mean16 4.83%。当前可见谱不支持用一张二维图概括全部更新需求。[谱表](evidence/spectral_reading_rows.csv)

这些百分比使用各自以fit均值中心化后的readout能量作分母；c、a、e、梯度并非相同维度或几何。W梯度展开为2097152维，但fit只有512记录，centered样本秩至多511；因此不能从样本谱直接推断总体内在维度。已测的是pooled谱及均值/领域/内部能量分解，未单独识别每个领域的可迁移特有谱轴。

**两个rank64不能互换。** 梯度SVD选64个完整W梯度方向；SAE的rank64是1024维输出空间中的P。采用列优先向量化时，\(\mathrm{vec}(PG)=(I_{2048}\otimes P)\mathrm{vec}(G)\)，参数空间投影算子秩为131072。后者的8.96%与前者的3.18%不是同预算比较。原生a的PCA在表征谱中覆盖a能量，在投影表中覆盖梯度能量，53.18%与6.74%也不是同一分母。

| body集合 | fit合格数 | readout同规则 | readout富集差保持正 |
| --- | ---: | ---: | ---: |
| 共同 | 99 | 65 | 不适用 |
| 计算机 | 211 | 144 | 206 |
| 数学 | 221 | 175 | 217 |
| 物理 | 182 | 143 | 176 |
| 生物 | 124 | 78 | 112 |

last对应共同6/14；计算机22/31、数学45/67、物理34/53、生物12/27满足readout同规则。阈值附近会丢失资格，不能把阈值失败全称作反向。body计算机/生物富集集合有11个交集、物理/生物6个，富集非独占。全维频率cosine比较的是每领域记录/位置平均后的profile，不是单条记录分类；共同/富集规则也不是逐atom显著性检验。[审计](evidence/review.json)，原A/atom_replication.csv。

| readout领域 | 本面板观察到atoms | 每记录不同atoms均值 | 相邻support Jaccard | 重构相对平方误差 |
| --- | ---: | ---: | ---: | ---: |
| 计算机 | 10267 | 1080.66 | .305 | .0616 |
| 数学 | 8380 | 923.21 | .325 | .0696 |
| 物理 | 8924 | 1016.38 | .317 | .0601 |
| 生物 | 10158 | 1105.68 | .299 | .0588 |

readout pooled共观察14120个atoms，其余仅称本面板未观察；每位置32个正激活。atom24605在四领域所有位置都激活，但没有自动命名为共享语义。幅度模式同领域cos≥.9994、跨领域≥.9794，频率模式区分更明显，提示相似度受共同大幅度成分影响。位置、持续长度1..255、正值分位数和全部稀疏共激活均已存；图中示例只取fit集合，未凭readout筛选。[全量统计](/data/250010109/MoE_Router/experiments/20260930_domain_update_geometry/runs/20260929T193805Z/result/analysis/activation_stats.csv)

已有持续长度表的描述性汇总显示：约68.9–71.4%的连续发放段仅长1个位置，但长度≥16的段承载10.7–14.4%的正激活次数，数学最高；既有短促变化也有长持续背景。每领域fit按次数选的100条共激活边在readout全部出现，次数排序Spearman为计算机.878、数学.865、物理.838、生物.671。它受频率选边影响，不证明所有共激活关系泛化或具有语义功能；原始全部边仍可查。[汇总及边界](evidence/review.json)

在fit选出的body集合、rank64、pooled readout、last单目标这一比较中，共同集合覆盖8.96%平方梯度能量，四领域富集覆盖5.12–5.41%，三个随机空间6.21–6.31%，原生a PCA6.74%。随机种子只有三个；同秩并未匹配所有decoder各向异性或激活幅度，不能解释为SAE整体胜出或共同性本身的因果作用。该表是跨领域汇总trace，没有回答各富集集合是否特别适合自己的领域。

共同空间非对角K重建相对平方误差仍.803，故高于随机的能量覆盖并不充分解释有符号相容性；全部投影Q仍负。注册的有符号块关系另存projection_domain_relations，不能用trace比例替代。全atom方向能量与last频率的事后Spearman为.005–.023，仅last发放atoms为.080–.165；相关含大量零频率、重叠decoder方向，不能当独立atom显著性或功能归因。[投影](evidence/projection_results.csv)、[审计](evidence/review.json)

e与last K的alignment=.903，c=.00513、a=.00315、SAE频率=.00557；K本来就由c/e构造，所以这不是独立证据证明“只有e决定更新”，低几何alignment也不等于没有非线性预测信息。中心化在删除对角前进行，仍依赖样本对角范数。相同目标1944个有向记录对的平均K=5.797、cos=.193；不同目标259688对平均K=−.0384、cos=.000458，分组同时改变上下文/预测/导数，未隔离目标因果作用。配对数不等于独立样本数。四领域块alignment还受原型自身能量与秩≤3构造影响，**不作为独立复现证据**。

## 8. Visualization Results

以下9图全部检查过可读性；坐标/单位以原表为准，表中的观察不是新统计检验。所有图固定33B状态、相同面板；原始表路径可由[origins](../../../../../../../daily_research_reports/backup/2026/09/0930/figures/domain_update_geometry/origins.json)追溯。

| 图与目的 | 原表/聚合、读法、直接观察及边界 |
| --- | --- |
| [领域K矩阵](../../../../../../../daily_research_reports/backup/2026/09/0930/figures/domain_update_geometry/domain_compatibility.png) | domain_relations；readout有向对均值、去自身。last原始均值有正负，单位梯度块均值微正；mean16块均值全正。不等于每对相容 |
| [更新谱迁移](../../../../../../../daily_research_reports/backup/2026/09/0930/figures/domain_update_geometry/update_spectra_transfer.png) | spectra；相对奇异值和fit累计rank留出能量。top64低覆盖；样本秩不等于总体秩 |
| [三类能量](../../../../../../../daily_research_reports/backup/2026/09/0930/figures/domain_update_geometry/common_domain_within.png) | energy_decomposition；fit平方梯度占比，内部>99%。小领域均值不等于标签无信息 |
| [主比较审计图](../../../../../../../daily_research_reports/backup/2026/09/0930/figures/domain_update_geometry/domain_generalization_audited.png) | primary原数值；点和bootstrap端点独立画出。区间偏移可见，不能当已校准区间 |
| [固定fit二维坐标](../../../../../../../daily_research_reports/backup/2026/09/0930/figures/domain_update_geometry/common_fit_coordinates.png) | spectral数组；各空间各自轴、512readout记录。激活域结构可见；梯度二维只覆盖约.1% |
| [全atom及示例](../../../../../../../daily_research_reports/backup/2026/09/0930/figures/domain_update_geometry/sae_activation_patterns.png) | patterns+atom_sets；全部30000频率排序和fit选ID留出热图。零值及共同/富集均保留；无语义命名 |
| [位置/持续/共激活](../../../../../../../daily_research_reports/backup/2026/09/0930/figures/domain_update_geometry/sae_position_persistence_coactivation.png) | position_profiles/records/coactivation_display；fit选例8位置箱、记录Jaccard、fit选边readout次数。有领域差异；示例不代表全部atoms |
| [SAE更新覆盖](../../../../../../../daily_research_reports/backup/2026/09/0930/figures/domain_update_geometry/sae_update_span_capture.png) | projection_results；实际输出秩、trace比例、fit领域间覆盖。共同高于随机；fit覆盖不是留出领域效应 |
| [聚合尺度](../../../../../../../daily_research_reports/backup/2026/09/0930/figures/domain_update_geometry/aggregation_scale.png) | scale；100固定抽样平均cos，非CI。mean16/m64真实.104、混合.074；平均操作与领域效应分开 |

## 9. Stage Evidence And Failure Decomposition

S0数据/来源合格但历史曝光与论文依赖未解决；S1数值Smoke PASS；S2四shard全量完成；S3 fit选择冻结；S4全部分析完成；S5图与记录完成，增加区间/绘图审计。Smoke last及mean16外积相对误差0，非目标导数比例0，Wc误差0；16 OPS的CE最大9.30e−6，全量tail最大1.63e−5，低于2e−5合同门槛。投影闭合误差约1.4e−14。

没有否定数学梯度恒等式，也没有证实“领域没有机制”。当前面板未显示无收缩领域均值描述器的收益，也未显示所选富集集合在pooled rank64能量比较中的优势。最强竞争解释是可重复关联弱，与高维均值估计误差掩盖关联，两者未被区分；总体方向还受到bootstrap校准和记录依赖限制。目标组成、下游敏感性、来源与尺度均可共同作用，不能把其中一项当已确定原因。

## 10. Full Experiment Record

唯一轮次，文档归档0930，UTC实际执行2026-09-29。问题/假设见§2；固定33B模型和控制见§4；无训练，fit512用于分析，readout512用于复现；全量结果见§7。运行`pt-t33awf9u`于19:38:37提交、19:41:21平台启动，runner耗时230.05秒，所有必需产物齐备，0次重试。见[执行证书](execution_record_cn.md)。洞见是激活的领域性与更新的领域性必须分别测量；下一科研选择未自动批准。

## 11. Interpretation

**AI解释，待研究者判断：**同一个模型状态可以同时呈现领域平均激活的复现、当前均值描述器的负Q，以及某些共同decoder方向更高的梯度能量覆盖，三者不矛盾。共享激活不是共同更新方向；平均梯度很小也不代表缺乏共享可复用子空间。主结果首先约束当前估计器，不能越过估计方差否定所有领域结构。e几何和目标分层只给出候选解释，尚未区分目标组成、上下文与Jacobian变化。共同集合的有界覆盖优势保留，不延伸至干扰因果或Router收益。

## 12. Claim Boundary

能说：本面板有限记录上的原型误差、各自空间的谱迁移、领域平均及逐atom的注册激活统计、指定pooled跨度的能量覆盖。所有注册统计完成不等于所有高阶激活组合或因果功能已识别。不能说：普适语义因果、条件信息上限、总体领域效应被排除、SAE功能使用、所属领域选择性收益、一步实际损失或长期收益、较大模型结论、专家隔离。本轮没有重测仅凭完整表征预测K；低alignment不能替代该检验。纯标签关联也不能充当无标签事前路由成功。

## 13. Next Decision

**AI建议的唯一下一问题：领域相关K结构，有多少与目标组成、聚合尺度一起变化，又有多少在可比较目标条件下仍保留？** 目标属于自然学习需求：\(P(y\mid s)\) 的领域差异本身就可能是总领域关联的一部分。固定目标条件后的比较改变了研究对象，不能把被去掉的部分自动称作伪相关。

最小区分逻辑是在同一未来预定分组/尺度上，并列报告总体关联与目标共同支持范围内的条件关联；fit选择、估计器校准和独立记录资格先于readout。若条件增量稳定，支持在指定目标条件外还存在关联；若校准充分且精度足够却达不到预定效应，削弱该条件联系，但不否定总体关联；若重合目标稀疏、估计不稳或区间未校准，则不足。目标词身份条件也不隔离语义，不能据此宣称因果。

尚需研究者选择是否采用此问题；具体目标关系、效应阈值和未来协议仍未批准。本轮不启动新实验、不补造修正区间。终版完成的是测量与事实解释文本，人类科学判断仍Unknown。

## 14. Artifact Manifest

| 产物 | 完成与用途 | 权威位置/身份 |
| --- | --- | --- |
| 冻结设计与代码 | COMPLETE；研究合同/实现 | R/registration、R/source；上述Protocol hash |
| 提交/设备/Smoke/冻结 | COMPLETE；工程资格 | run提交json、R/smoke_receipt、R/verification |
| 记录/梯度/全SAE数组 | COMPLETE；原始测量 | R/collection/shard_0..3，A/measured_events、mean16_gradients |
| K与原型/谱 | COMPLETE；主与次级 | A/gram_matrices、fit_prototypes、spectra、spectral |
| 全激活与模式 | COMPLETE；300000统计行 | A/activation_stats、patterns、position_profiles、runs、coactivation |
| 集合/复现/上下文 | COMPLETE；fit-only来源可追溯 | A/atom_selection_frozen、atom_sets、atom_replication、atom_contexts |
| 全atom梯度/投影 | COMPLETE；240000方向能量行、54投影行 | A/atom_gradient_energy、projection_results、projection_domain_relations |
| 尺度/混杂 | COMPLETE；描述证据 | A/scale、nuisance、event_norms、kernel_alignment |
| 结果审计 | COMPLETE；有界资格/修图 | V/review.py、review.json；读取副本evidence/origins |
| R2终版推理审计 | COMPLETE；12项推断修正及既有Gram算术核对 | V2/audit.json、before快照；evidence/reasoning_audit_final.json |
| 图片 | COMPLETE；9张PNG/PDF阅读副本 | 本日期figures/domain_update_geometry及origins |

## 15. Links

[Summary](summary_cn.md) · [Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_12_domain_update_geometry/17_12_domain_update_geometry_anchor_cn.md) · [Protocol](protocol_cn.md) · [Focus](../../../../focus/focus_domain_update_geometry_cn.md) · [执行记录](execution_record_cn.md) · [执行代码](/data/250010109/MoE_Router/experiments/20260930_domain_update_geometry/scripts) · [数据manifest](/data/250010109/MoE_Router/experiments/20260930_domain_update_geometry/data/data_manifest.json) · [运行结果](/data/250010109/MoE_Router/experiments/20260930_domain_update_geometry/runs/20260929T193805Z/result) · [审计代码](/data/250010109/MoE_Router/experiments/20260930_domain_update_geometry/reviews/20260929_result_audit/review.py)。复现入口为runtime.sh后调用scripts/run.py --out全新非空禁止的输出目录；复现命令不是再次运行授权。当前任务ID为pt-t33awf9u。
