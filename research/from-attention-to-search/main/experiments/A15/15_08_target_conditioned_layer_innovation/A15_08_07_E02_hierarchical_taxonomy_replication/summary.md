# Summary: A15_08_07_E02_hierarchical_taxonomy_replication

Primary Anchor: `15_08_07_semantic_conditioned_functional_subspace`  
Frozen Protocol: [protocol_cn.md](protocol_cn.md) (`a15_08_06_e02-r1`, SHA256 `3ba0788c...19269`)  
Detailed record: [detailed.md](detailed.md)  
Result status / eligibility: `ELIGIBLE`; typed result is `INSUFFICIENT` on both registered hypotheses. Knowledge wording is `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`.

## Result Snapshot

**Verdict:** block 24/28 的局部子空间并集假设均为 `GEOMETRY_INSUFFICIENT`；完整 \(R_U\) 的功能准入均未通过，因此正式 80%/90% 功能保留维数均为 `NA`，实验二为 `INSUFFICIENT_NO_FULL_GAIN`。

**What we established:** 八个粗类的局部判别子空间合并后确实明显增秩，但“同粗类谱显著更窄”和“同粗类方向稳定性差达到注册幅度”没有同时通过。完整 \(R_U\) 相对只用 \(X\) 有正增益，但相对 duplicate-\(X\)/错配-\(R_U\) 的优势区间跨 0，尚不能把增益归因于正确样本配对的 \(R_U\)。

**What the experiment shows:** 宽谱不能被本轮证据简化为“许多窄而稳定的局部子空间叠加”；PCA 高方差方向也没有被确认成低维功能方向。监督降秩岭在描述性曲线上 8 维达到 80%/90%，但完整 \(R_U\) 未准入且 8-way 输出秩天然不超过 7，所以这不是表征低秩结论。

**What we do next:** 只推进一个决策：在真实用户请求数据上先单独确认“正确配对的 full-\(R_U\) 是否稳定超过 duplicate/mismatch null”；通过后才读取功能维数并进入 Router 相对效用实验。

## Decision-Bearing Setup

**Question:** 已知粗类时，宽 \(R_U\) 是否来自多个局部低秩细分类子空间的并集；以及 full-\(R_U\) 的未见数据增益能否由低维输入投影保留？  
**Treatment and control:** 同粗类/跨粗类匹配几何；full-\(R_U\) 对 duplicate-\(X\) 与 64 个粗类内错配-\(R_U\)；PCA 头/尾、64 条 Haar 随机子空间、监督降秩岭。  
**Changed variable:** 类别是否来自同一粗类，以及 \(R_U\) 投影方法和维数。  
**Held fixed:** Qwen3-8B、block 24/28、prompt、decision token、每任务 8 类×每类 10 行、读出器族、正则网格与 base logits。  
**Primary metric and unit:** 几何为归一化 \(r_{90}^{var}\)、projector overlap 与 union effective rank；功能为粗类等权交叉熵增益，单位 nats/样本。  
**Known limitation:** 合成学科描述不等同于真实用户请求；跨粗类功能任务仅作兼容性分析；本实验不测 expert utility 或真实 Router。

## Verdict Basis

| Registered rule | Observed value | Guard / eligibility | Verdict | Evidence source |
| --- | --- | --- | --- | --- |
| H-GEO：集中、方向、并集三项合取 | B24：\(\Delta_{rank}=0.0127\), LCB \(-0.0253\)；\(\Delta_{orient}=0.0639\), LCB \(0.0346\)；union \(48.84>22.36\) q95 | float32 trace 守卫偏差经同数组 float64 复算通过；不改科学指标 | `GEOMETRY_INSUFFICIENT` | [geometry table](tables/geometry_task_summary.csv), [numerical audit](evidence/numerical_trace_audit.json) |
| H-GEO：集中、方向、并集三项合取 | B28：\(\Delta_{rank}=0.0443\), LCB \(-0.0063\)；\(\Delta_{orient}=0.0933\), LCB \(0.0480\)；union \(48.68>25.01\) q95 | 同上 | `GEOMETRY_INSUFFICIENT` | [geometry table](tables/geometry_task_summary.csv) |
| H-ADMIT：full-\(R_U\) 超过 matched null | B24：full \(0.1541\)，null \(0.1191\)，差 \(0.0350\)，同时 LCB \(-0.0108\) | 新确认集 640 行、冻结后一次打开；身份与完整性守卫通过 | `INSUFFICIENT_NO_FULL_GAIN` | [typed decisions](tables/typed_decisions.csv), [functional curves](tables/functional_curves.csv) |
| H-ADMIT：full-\(R_U\) 超过 matched null | B28：full \(0.0682\)，null \(0.0554\)，差 \(0.0128\)，同时 LCB \(-0.0196\) | 同上 | `INSUFFICIENT_NO_FULL_GAIN` | [typed decisions](tables/typed_decisions.csv) |
| H-FUNC：80%/90% 首次确认交点 | 两层 full gate 均关闭 | Protocol 规定 gate 关闭后所有正式交点为 `NA` | `NA` | [typed verdict matrix](figures/figure_3_typed_verdict_matrix.png) |

## Key Evidence

- [实验一几何图](figures/figure_1_geometry.png)：三个必要条件中只有并集增长通过。
- [实验二维数曲线](figures/figure_2_functional_rank_curves.png)：显示完整、0.8/0.9 阈值、PCA 头/尾、监督降秩岭与 64 条随机子空间；因 full gate 关闭，曲线只作描述。
- [数据构造图](figures/figure_0_dataset_construction.png)：8 粗类×8 细类×每 split 每类 10 行，共 1,920 行。

## Claim Boundary

**Can claim:** 在本平衡合成数据、Qwen3-8B block 24/28 和冻结线性分析族内，局部子空间并集增长存在，但完整的“局部窄谱并集”解释未获支持；未获得可报告的正式功能保留维数。  
**Cannot claim:** 语义本质高秩或低秩；\(R_U\) 是新知识；PCA/RRR 是 Router 应使用的方向；监督降秩岭的 8 维是表征秩；expert utility、持续学习或不遗忘得到改善。

## Next Decision

**Decision:** 是否在真实用户请求数据的新确认集上，先把 full-\(R_U\) 的样本配对功能准入单独做实。  
**Completion criterion:** 至少一个预注册 block 的 full-minus-matched-null 同时 95% LCB \(>0\)；否则停止读取功能维数，也不进入 Router 设计。  
**Resume action:** 审核 `A15_08_07_E01_clinc150_semantic_conditioned_functional_subspace` 的新确认数据来源与冻结边界，只批准 H-ADMIT 前置阶段。
