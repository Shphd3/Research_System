# Detailed：自然语言统计与局部更新结构

[Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_13_ntp_statistics_local_compatibility/17_13_ntp_statistics_local_compatibility_anchor_cn.md)；[Protocol](protocol_cn.md)；[Summary](summary_cn.md)；[执行记录 / execution record](execution_record_cn.md)。

## 0. Quick Recap

目的：测固定状态的局部更新领域结构，并用SAE分开观察出现与敏感性。假设、最强竞争解释与主规则见[Summary](summary_cn.md)。直接结果T=0.006637，95%区间[−0.003738,0.017012]；裁决INSUFFICIENT。采集及登记分析全部完成，科学判断Unknown；语料历史曝光／文档近似独立使证据BOUNDED。长期共享与有限W更新均未运行。

## 1. Terminology / Definitions

领域标签为CS、数学、物理、生物，各含两个学科子类别；不等于语义因果因素。F为工具拟合／第一池，R为来源test／第二池，本轮没有模型训练。真实目标相同指token ID一致，不要求模型预测相同。c是共享矩阵输入2048维，a是该矩阵原生输出1024维，e是损失对a的梯度。G=e c转置；K为两个G的Frobenius内积，一阶普通SGD候选相容性。T是目标固定的领域均值差跨池内积／历史梯度平方尺度。SAE的alpha是实际稀疏激活，decoder d是输出方向；I=d转置F_a d是模型预测对方向的敏感性。后者非负，不是有符号跨数据作用。Monte Carlo SE仅描述固定上下文上的计算探针误差，不是语料总体区间。

## 2. Anchor Link And Decision Point

当前对象仍为局部更新候选；不将功能profile作为主均值量的替代结论。[Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_13_ntp_statistics_local_compatibility/17_13_ntp_statistics_local_compatibility_anchor_cn.md)保留登记科学正文；[Summary](summary_cn.md)给出新事实。研究者科学判断／激活或关闭问题均Unknown。

## 3. Protocol Freeze, Conformance, And Deviations

冻结版本见Full/source/protocol.md及registration.json中的SHA，当前Protocol末尾追加修订，不覆盖登记科学正文。

| 登记项 | 实际 | 状态／证据影响 |
| --- | --- | --- |
| 固定33B状态与共享块 | 原检查点／SAE，0优化步，原状态逐位不变 | PASS；完成及分片回执 |
| 2048记录、16位置、192四元组 | 全部达到；768端点记录互不复用 | PASS；数据／端点清单 |
| F工具冻结后读取R | fit_freeze.json在R采集前生成；源码／配置与参考冻结 | PASS；日志及registration |
| 原精度门槛 | 前两次失败；诊断轮不合格；FP64反传求和修复后严格Smoke通过 | 工程修订，不改前向值／科学量／门槛 |
| 1%门槛与单一主区间 | 28类×5000校准通过；主区间跨门槛 | INSUFFICIENT，不是工程失败 |
| 目标功能单元≥8不同文档 | F数学period6；R物理comma/of7 | 对应单元INSUFFICIENT_COVERAGE；未回填 |
| 对角次级汇总 | 编号／名称映射导致原16值NaN；保留原件，按原1/3规则修复 | 输出修复；primary SHA不变 |
| 不超过2h／8GPUh | 正式Smoke34.9s；Full223.0s，重试合并远小于预算 | PASS；使用默认4H100 Reserved |
| 历史曝光与独立性 | 旧33B1024panel排除；N8有历史21B曝光，缺论文独立证书 | BOUNDED；不能称未见语料确认 |

没有改目标、剔除极端梯度、选择有利R方向、扩样或追加探针。运行后补导出既有领域差异的MC SE与编号标签，是登记量的读表，不是新增统计检验。

## 4. Actual Setup

固定S7 sidecar33B状态（累计历史33,000,000,000训练token，历史optimizer_step125894）；本轮0训练更新。模型8层；第8层W_O为1024×2048，SAE观察native a、残差加和之前，TopK32、30000单位decoder列。原完整检查点SHA c30b78e5bcba8f0a09c5e215389be86778874e87fcbb9fe5211175d370bb0803。

数据来自N8_v1 fit/test学术片段，每子类／池128条，8子类×2池=2048。输入每条前255token，预测位置14,30,…,254，对应真实目标15,31,…,255；每条16个有效测量目标。本轮先排除旧33B panel，再筛查精确文本／token及5-gram Jaccard≥0.8近重复，结果0；以登记SHA规则选择，未凭梯度选择。

主目标ID11、279、315、13对应逗号、space+the、space+of、句号；元数据选择每条至多一个主事件并分配不共享端点，24层×8四元组=192。每领域两子类均衡，四目标和六领域对等权。自然分析保留全部32768位置；其子总体与主选择总体不同。

功能面板每子类／池16条，共256条、4096上下文、每上下文8Rademacher词表探针（32768 VJP）。SAE激活仍收集全部32768测量位置；F激活选每集合最多64个，common和四领域富集共320不同展示atom。PCA在F全部测量a中心化；decoder span做SVD正交化；三随机QR种子31/43/59。秩8/32/64，按实际秩封顶并配同秩控制。c/e/G谱使用每领域／池固定64条的4096事件。模拟2026093001、校准2026093002、报告2026093003、探针哈希2026093004；其他选择哈希见Protocol与manifest。

当前NTP与SAE均冻结；没有辅助目标、优化器、重新拟合SAE、router或参数更新。FP32原生前向、FP64完整词表概率，词表投影反传用FP64累加；分项在原生中间值上独立复核。原生／回放损失和梯度、SAE编码重构、重复性、状态、KL敏感性资格由严格Smoke验证；所有采集分片有限值／目标ID检查通过。

## 5. Metrics And Registered Decision Rules

v0=100.77199611476297，原历史参考未重算。每四元组Z=A+B−C_FR−C_RF，T为24层均值／v0。层内8个独立记录四元组给出层方差，合成为分层近似Welch区间；下界>0.01支持、上界<0.01不支持、重叠不足。本轮SE0.005170，df51.9037，区间[−0.003738,0.017012]。

有符号均值矩阵比较F/R和各池的预设文档半区，分natural/common_support/uniform_target；只报告点估计。经验e二阶矩与真实目标均值／协方差独立于模型Fisher。Fisher使用完整模型p的无偏词表探针，不采样真实续写或伪造自然标签；I对8个平方投影平均，MC SE由探针样本方差／8和上下文平方权重合成。低于2MCSE只标计算分辨率不足，不做30000重未校正显著检验。未假设p=q。

## 6. Evidence Lineage

| 量／问题 | 原数据→计算→汇总 | 值或状态 | 资格与界限 |
| --- | --- | --- | --- |
| 主均值差复现 | features.npz的e/c→4个FP64Gram项→24×8Z→登记Welch区间→primary.json | T0.006637，CI跨0.01 | 数值合格、推断按文档近似独立有界；INSUFFICIENT |
| 有符号跨作用 | quartet.csv或全部位置G均值→同池半区／跨池内积→兼容性表 | 自然跨池10点4.291e−5至3.570e−4，均正 | 探索，不能认定总体符号 |
| 领域敏感性profile | fisher.npz中u→decoder投影平方→加权I及MCSE→F/R领域关系 | 同领域原始cos均值0.9973；去共同均值后0.5012 | 自然上下文描述；目标控制覆盖不足 |
| SAE实际出现 | 同位置encode indices/values→positive计数／条件幅值→activation表 | 全240000个池／领域／atom行；320方向展示 | 激活不等于因果使用 |
| 同秩输出方向控制 | 同批u→F冻结正交Q→投影trace／总trace | rank32 common4.472%、PCA3.672%、随机3.092–3.154% | 描述，不是容量分割或优越性测试 |
| 更新二阶方向迁移 | 4096事件／池→c/e/G Gram→F eigenspace→R覆盖／K误差 | rawG中心化rank64 R覆盖7.698%，K误差0.3633 | 协方差几何，不救回H1 |
| 参数冻结／完整性 | 前后state digest、state文件SHA、分片目标数→完成＋postrun审计 | 2048记录／32768目标／0更新；PASS | 运行事实，不等于科学支持 |

## 7. Main Results

合格而有界主值见[primary.json](evidence/primary.json)。主T的95%区间跨0和1%门槛，无法排除无复现或超过候选尺度；缺失的是精度，不能用功能结果补上。

SAE功能结果见[领域关系](evidence/functional_domain_relations.csv)、[选定方向表](evidence/sae_selected_functional_profiles.csv)。全局positive profile高度共通；去共同均值后，CS/math/physics/biology同领域cosine为0.7206/0.4705/0.6794/0.1341，整体中心化profile对齐0.5752。多数同领域单项差异仍在2MCSE以内（约69.8%–86.7%），这是计算差异分辨率，不能转写为总体无差异。目标组成控制不完整，覆盖不足不回填。

[对照表](evidence/functional_span_controls.csv)说明common SAE方向与富集SAE方向的敏感性不同；不要求SAE优越。[混合表](evidence/compatibility_mixture.csv)显示限制支持／改变目标权重显著改变点估计尺度，但不能解释为“多少百分比由词频导致”。[均值协方差](evidence/mean_covariance_decomposition.csv)、[方向结构](evidence/anisotropy.csv)保持独立结论。

失败Smoke、临时移除断言的诊断轮均不能进入主值或放行资格；正式Smoke与Full完整分片才有资格。

## 8. Visualization Results

[图像来源账本](figures/origins.json)记录原始路径、source tables、SHA、caption；图在此日期目录中的reading copy与原件相同。

- 主图primary_contrast：T／历史梯度能量，点及Welch区间，红线0.01。支持应在红线右侧、不支持在左侧，本轮跨线；不能宣布结构不存在。
- sae_activation_and_sensitivity：F选定的前4个／集合示例，R领域×atom；左为出现频率，右为Fisher I。不同色标代表不同物理量，不能相加或直接比较颜色强度；不赋语义名字。
- functional_recurrence：原始cosine与等领域中心化cosine，矩阵行F列R；用于区分共同pattern与领域偏离；不确立来源独立／语义因果。
- functional_span_controls：R、自然上下文、rank32、各领域trace fraction；同上下文同探针控制，不是参数容量份额。
- signed_mixtures：三种目标上下文加权的10个群体点估计对称矩阵；不画未校准误差条，也不能宣布显著帮助。

全部五幅实际图已检查；移开遮住数据的图例、去掉重复挤压行标签，仅调整布局，原图保留于Full/repair/figures_original，数值不变。Anchor科学判断未因此提升。

## 9. Stage Evidence And Failure Decomposition

来源资格PASS、28类校准PASS、CPU机制与原生前向精度检查PASS。Smoke1分项误差超门槛；Smoke2原生词表反传累加误差仍超门槛；Smoke3仅诊断、不能资格认证。Smoke4通过原门槛，最大分项重组相对误差3.3502e−7，48方向的三个尺度局部KL核对通过。

原失败定位实现数值累加，未证伪物理先验或数学恒等式。主区间不足也未证伪一阶候选，仅未达到裁决精度。次级整数ID映射修复经过审计，无主结果改动。剩余竞争解释包括共同预测敏感模式、目标组成、来源差别、采样误差；敏感性并不识别p−q系统误差或容量竞争。

## 10. Full Experiment Record

2026-09-30这一轮问题为固定NTP状态的局部均值相容性与功能敏感性。设置、数据与分裂见第4节；F工具先冻结、R后采集，无训练或确认语料独立证书。四次Smoke资格／诊断尝试均保留；Full pt-z162gb1w于05:32:22UTC开始、05:36:14UTC成功终止，程序223.0s。全部2048记录／32768位置与4096功能上下文达到，主判不足，功能独立描述与不足单元交付。研究者认识更新和下一决定Unknown；本轮不进入长期训练结论。

## 11. Interpretation

直接观察与派生量如上；AI解释候选是“均值判据当前精度不足，但SAE可同时呈现出现和方向敏感性，共同profile与领域偏离应分开看”。该解释为AI_PROPOSAL，尚待研究者确认，不改变Focus或问题状态。

## 12. Claim Boundary

可陈述本轮测量完整、主判INSUFFICIENT、有功能描述量及不足单元。不可声称自然语言统计必然导致冲突、模型真实校准偏差、SAE因果使用／容量竞争、router预测成功、实际有限W更新收益或长期共享／分开收益。

## 13. Next Decision

研究者决定Unknown；唯一AI建议是先决定是否提高主检验采样精度，再登记一次微调。完成条件：研究者选择待消除的不确定性，确认新的样本／预算契约。续接从本Summary和已完成Full开始；不重复提交此run，不用功能图救主判，不自动扩样。

## 14. Artifact Manifest

[研究阅读副本账本](evidence/artifact_manifest.json)记录每个curated文件的origin/SHA及冻结代码／Protocol身份；[图来源](figures/origins.json)补全图像producer/source/caption。小型主值、兼容性、功能关系／MC、控制、几何表保存在evidence；原始数组及全30000atom表只在执行侧。全模型检查点不复制到Research_System。

执行侧features/fisher分片包含e/c/a/r、目标、loss/p_y、ep/et、SAE编码、重构误差／残差敏感性；decoder.npy保存实际字典。功能raw I／MC variance／observed-label moments及1024²模型Fisher、选定D转置F D保留，不构造30000²矩阵。completion/analysis/functional/postrun回执各自证明运行、分析、功能条件与修复范围，不替代研究者判断。

## 15. Links

- [code](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/scripts)
- [runner](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/scripts/stage.py)
- [data/endpoint/functional manifests](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/data)
- [Full registration](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/full_initial/registration.json)
- [frozen Protocol](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/full_initial/source/protocol.md)
- [immutable sources](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/full_initial/source)
- [collection arrays and receipts](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/full_initial)
- [analysis outputs](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/full_initial/analysis)
- [post-run audit](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/full_initial/analysis/postrun_audit.json)
- [original failed diagonal rendering](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/full_initial/repair/conditional_diagonals.original.csv)
- [qualified Smoke](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/smoke_qualified)
- [failed/debug Smoke ledger](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs)
- [ACP receipts](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/acp_receipts)
- [durable pod logs](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/acp_receipts/pod)
- [checkpoint](/data/250010109/MoE_Router/experiments/20260920_s7_lambda0p1_from_scratch_4h100/runs/S7_lambda0p1_from_scratch_4h100/milestones/token_033000000000)

Job IDs: pt-wd184bbc / pt-gqxil5g2 / pt-xm7fqnf3 / pt-k68kogs3 / pt-z162gb1w. Monitor owner: this Codex chat. Default tuple and exact template gates: [execution record](execution_record.md).

Historical command (not automatically rerun; a new attempt requires fresh immutable roots):

```bash
source runtime.sh
python scripts/stage.py --mode full --out runs/full_initial --smoke-root runs/smoke_qualified
```


## Supplement: lexical_readout_01 — 已有原子的词面关联初筛

**执行完成，证据为运行后探索。**本节解释已有SAE的领域／出现差异，不改原主T结论。[登记与来源](evidence/lexical_readout_manifest.json)；[完整执行回执](evidence/lexical_readout_receipt.json)。

**目的：**检查原F已选择的320个共同／领域富集原子，是否可能与特定词面关联；区分当前输入身份、前文词面与预测下一词需求。

**假设与竞争解释：**原子可能具有集中且跨池保留的词面关联；也可能只是频繁词面、领域组成或语法／格式模式与原子共同出现。单个词面相关不能识别原子的唯一语义或因果功能。

**方法：**固定旧模型与缓存，CPU读取32768测量位置的正激活；按当前token、前一token、前16token存在性、该窗口完整英文词、真实下一词身份五个独立模式计算。F按最多共现且≥8不同共现文档选一个词面，冻结后再读R；R同时报告P(词面|激活)、P(激活|词面)、词面基础频率、lift、条件系数与领域内部关系。英文完整词用可见前缀字符边界、区分大小写，无词干化；不完整字节解码仅从词模式分母排除（F183／R182事件），其他四模式仍使用全部位置。词面命中率是激活时对应词面出现的比例，覆盖率是词面出现时原子激活的比例；lift为命中率除以该词面的基础出现率，常开原子lift=1。

**直接结果：**五个模式F有足够覆盖的映射数分别188／163／320／320／176；R≥8共现文档的数分别154／131／318／318／152。预先写入的描述性“命中率≥80%且lift≥2且R共现文档≥8”标签在此子集五种模式中均为0；这一AI初筛阈值不是显著性测试或不存在词特征的证据。

| 原子／F选定集合 | F选择的词面关系 | R命中率 | R覆盖率 | R lift | R共现文档 |
| --- | --- | --- | --- | --- | --- |
|28737/common | 当前token` (`，ID320 |66.23% |82.59% |43.93 |180 |
|21638/physics | 当前token` the`，ID279 |36.00% |3.66% |7.99 |27 |
|21737/common | 实际下一词` to`，ID311 |31.32% |53.69% |25.28 |105 |

示例选择仅为运行后解释，不是另一个确认性检验；[全部320×5候选与覆盖](evidence/lexical_readout_candidates.csv)保留未映射与不足，原完整表还保留F/R域内值。28737与` (`的关联在四个R领域中都有≥8共现文档，域内lift约38.69–56.89；其无该token激活的最高例当前为` ((`，可提出“括号模式”候选，但没有测完整符号家族或语义唯一性。21638对` the`只有physics内部满足8文档覆盖，其他领域仍不足；领域富集不能直接解释为领域词身份。21737活跃时下一词` to`比例较基础1.239%增高，关联在四领域均有足够覆盖；下一词并非前向输入，不能把它称为原子读取到的当前词。

[实际前缀与两类反例](evidence/lexical_readout_examples.json)同时保存“激活但无词面”及“有词面但不激活”；由此不能把词相关直接升级为一词一原子。多数前文词映射被高频`the`选中，最高前文完整词命中率约79.41%但lift仅1.55，说明必须扣除基础词频。当前选择规则偏向高共现词，对稀有但专属词／低频原子检测有限。

**资格与冻结：**CPU已知例通过，包括词选择原子、常开／高频词、领域混杂、R反转、重复事件但文档不足、完整词边界、CSC身份。执行18.8秒，模型加载0、模型更新0、GPU使用false；F映射哈希保持一致，原Full主JSON和完成回执哈希未变。依赖复用既有tokenizer（JSON SHA c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539）与原indices/values/targets；未复用或修改训练代码。原Full和两池领域／Fisher结果早已曝光；当前映射只用F，但不能宣称未见语料确认。模式／阈值见Protocol的LEXICAL_READOUT_01追加记录。

**边界与下一决定：**可陈述这320个预选原子中存在词面／符号／下一词关联，并有保留反例；不能推到全部30000原子、所有词、任意句子位置或唯一语义。窗口之外、多词语法、词形／大小写合并、同一词跨上下文的不变性、换词干预、因果必要／充分性均未测。AI解释为“词面关联可以解释一部分现象，但一词一原子尚未成立”，研究者判断Unknown。AI建议下一步在选定候选上决定是否做同词不同上下文／保持结构换词的干预；该运行未执行这一步，也不自动扩展原主检验。

完整来源：[新源码](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/scripts/lexical_readout.py)、[F冻结映射](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/lexical_readout_01/fit_maps.json)、[全词面结果](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/lexical_readout_01/atom_lexical_associations.csv)、[域内结果](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/lexical_readout_01/within_domain_associations.csv)、[词面组成描述读出](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/lexical_readout_01/domain_frequency_readout.csv)。
