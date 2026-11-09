# A15_08_07_E04 详细记录

Primary Anchor：[A15_08](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/15_08_target_conditioned_layer_innovation_anchor_cn.md) 旁路有界几何扩展  
Frozen Protocol：[protocol.md](protocol.md)，revision `E04-zru-geometry-v1`  
Summary：[summary.md](summary.md)  
Result eligibility：`ELIGIBLE`

## 0. Quick Recap

目的：判断完整表征的宽谱是否与多个粗类内部、可复现且彼此不同的细分类子空间共同存在，并在合并粗类时表现为方向并集增秩。  
假设：H1 同粗类更窄；H2 同粗类方向跨 split 可复现且不同粗类方向不同；H3 合并不同粗类后的并集有效秩超过重复同一粗类的 null。  
实验思路：固定 8 类×10 条、文本、模型、token、层和代码，只改变 8 类来自同一粗类还是八个粗类；\(Z_l\) 为主对象，\(R_U\) 仅补充。  
直接结果：B24/B28 的 H1、H2、H3 六项全部 `SUPPORTED`。  
资格：正式 ACP 作业成功，身份、split、重建、有限值、秩和产物守卫通过，未打开测试集。  
Verdict：`SUPPORTED`。  
边界：支持“多个局部判别子空间对宽谱有贡献”，不支持“主要/唯一原因”或 Router 功能结论。

## 1. 术语

| 术语 | 白话 | 计算 | 不能证明 |
| --- | --- | --- | --- |
| \(Z_l\) | 本层 attention 写入后、真正进入 MLP/候选 Router 的状态 | \(Z_l=X_l+U_l\) | 不是新增知识 |
| parent-centered | 每条样本减去所属粗类的 TRAIN 均值 | DEV 也只用 TRAIN 均值 | 不删除粗类内共享因素 |
| 谱宽 | 方差需要多少方向才能覆盖 | \(r_{90}\) / 79 | 不等于分类功能秩 |
| 局部判别子空间 | 一个粗类内部区分 8 个细类的方向 | diagonal reduced-rank LDA，rank 7 | 不等于完整表征秩 |
| overlap | 两个子空间只按方向比较 | \(\|P^TQ\|_F^2/7\) | 不衡量方差或功能增益 |
| 并集有效秩 | 多个 rank-7 基合并后的方向多样性 | 拼接基 Gram 谱的熵有效秩 | 不等于模型内禀秩 |

## 2. 实际数据与设置

- 数据：8 个粗类（数学、物理、化学、生物、计算机、经济、医学、语言学），每个粗类 8 个细类；TRAIN/DEVELOPMENT 各 640 条，每个粗类—细类单元各 10 条。
- 主比较：同一粗类的 8 个细类 vs 8 个粗类各取一个细类；每个任务都是 80 条。
- 模型：冻结 Qwen3-8B；决策 token 与 E03 相同。
- 十层谱：2、6、10、14、18、22、24、28、32、36；正式主层：24、28。
- split：TRAIN 学均值、residualizer 和方向；DEVELOPMENT 只做复现；CONFIRMATION-v3/TEST 打开行数为 0。
- \(Z_l\) 不做逐特征标准化；任务内协方差按总能量归一化。\(R_U\) 按 E03 residualizer 重新拟合后用原生坐标并做同样 parent-centering。

## 3. Protocol conformance

| 注册项 | 实际 | 状态 | 资格影响 |
| --- | --- | --- | --- |
| 数据与 split | metadata SHA256 `bf7c...a3dd`；TRAIN/DEV 各 640；TEST 0 | PASS | eligible |
| 跨粗类集合 | SHA256 `496d...f079`；8 batch×8 set | PASS | eligible |
| 激活身份 | 十层均复用冻结 fitting snapshot；逐层 SHA256 记录在 raw JSON | PASS | eligible |
| \(Z=X+U\) | B24 smoke 最大误差 0；正式逐层均通过 \(10^{-5}\) gate | PASS | eligible |
| 主对象与中心化 | parent-centered native \(Z_l\)；DEV 只用 TRAIN 均值 | PASS | eligible |
| 主层与主规则 | B24/B28；H1/H2/H3 三项合取 | PASS | eligible |
| null/uncertainty | row bootstrap 200；aggregate 2,000；overlap null 256；union null 1,000 | PASS | eligible |
| 资源 | ACP `pt-1qp1h2z0`，单节点 8×5090 SPOT | PASS | eligible |
| 未授权动作 | 未改 Anchor、未 commit/push/sync | PASS | none |

偏差：无科学偏差。正式结果可见后只调整了图 1 的版式，把 \(R_U\) 移到补充图；未改变数据、指标、数值或 verdict。

## 4. 主判定证据链

| 判定 | 注册规则 | 原始工件 | 观测 | Verdict | 限制 |
| --- | --- | --- | --- | --- | --- |
| B24 H1 | 跨减同 \(r_{90}\) 的 95% LCB > 0 | `layer_24.json` | 20−16=4 方向；归一化差 0.0506，LCB 0.0190 | SUPPORTED | bootstrap 区间基于分层重采样分布 |
| B28 H1 | 同上 | `layer_28.json` | 20−15=5；差 0.0633，LCB 0.0380 | SUPPORTED | 同上 |
| B24 H2 | overlap gap LCB > 0 且超过置乱/Haar | `layer_24.json` | gap 0.3474，LCB 0.3092，置乱 q95 0.1040 | SUPPORTED | 判别方向依赖注册线性方法 |
| B28 H2 | 同上 | `layer_28.json` | gap 0.5803，LCB 0.5547，置乱 q95 0.2181 | SUPPORTED | 同上 |
| B24 H3 | TRAIN/DEV k=8 actual > same-parent null q95 | `layer_24.json` | 41.29>15.62；40.71>16.23 | SUPPORTED | 有效秩不是完整表征秩 |
| B28 H3 | 同上 | `layer_28.json` | 48.27>11.75；47.22>11.82 | SUPPORTED | 同上 |

六项均支持，按冻结合取规则，总 verdict 为 `SUPPORTED`。

## 5. 图 1：粒度改变时谱怎样变化

![完整表征的粗细粒度能量谱](figures/figure_1_z_spectrum_granularity_depth.png)

目的：在样本量和类别数相同的情况下，直接看跨粗类是否比同粗类更宽。  
横轴：PCA 方向编号 1–79。纵轴：该方向占总方差比例，对数坐标。颜色：block 深度，B24/B28 加粗。  
观察：右侧跨粗类谱普遍更平；十个固定层的 H1 均为正，其中主层 B24/B28 分别从 16→20、15→20。  
允许结论：混合粗类会让完整表征的能量摊到更多方向。  
不能证明：这些新增方向分别属于哪个粗类，也不能单独证明局部子空间解释。

## 6. 图 2：多个局部方向合起来是否真的变大

![局部子空间并集维数增长](figures/figure_2_z_union_dimension_growth.png)

目的：排除“看似不同只是同一粗类小样本重复估计噪声”。  
横轴：加入粗类数 1–8。纵轴：rank-7 基并集的熵有效秩。实线：不同粗类；点线/带：同一粗类 bootstrap null。  
观察：不同粗类几乎持续线性增长到 41–48，而 null 很快饱和在 12–16 附近；TRAIN 与 DEV 复现。  
允许结论：不同粗类持续贡献新的局部判别方向。  
不能证明：增长方向占完整 \(Z_l\) 总方差的比例，也不能证明因果生成机制。

## 7. 图 3：这些方向稳定吗、不同吗

![局部子空间重合热力图](figures/figure_3_z_local_subspace_overlap.png)

目的：同时检验同粗类跨 split 复现和跨粗类分离。  
行/列：TRAIN/DEVELOPMENT 粗类。颜色：rank-7 overlap。  
观察：两层都形成亮对角线；B28 对角中位 0.6185、非对角 0.0382，比 B24 的 0.4315/0.0841 更清晰。  
允许结论：局部方向不是任意旋转或仅由同一批文本产生；不同粗类方向确实不同。  
不能证明：方向是模型原生读出的固定“语义轴”。

## 8. 补充：为什么 \(R_U\) 与新主结论不同

\(R_U\) 的 H2/H3 在两层都支持，但 H1 为 `INSUFFICIENT`：B24 的同/跨 \(r_{90}\) 为 53/54，LCB -0.0127；B28 为 45.5/49，LCB 0。这复现并解释了旧 E03 的边界。完整 \(Z_l\) 与候选新增更新回答不同问题：前者是当前实际表征几何，后者是线性注册旧状态后剩下的层更新。\(Z_l\) 的支持不能替 \(R_U\) 补票。

补充图：[Z/R_U overlap 对比](figures/figure_s1_z_ru_overlap_comparison.png)、[\(R_U\) 十层谱](figures/figure_s2_ru_spectrum_granularity_depth.png)。

## 9. Claim boundary 与唯一下一决策

Can claim：多个粗类内部的细分类方向在 B24/B28 的完整表征中可复现、彼此不同，并且其并集增长与跨粗类谱宽化同时成立；这支持它们对宽谱有贡献。

Cannot claim：主要或全部高秩由此造成；自然语言普适内禀秩；非线性新增信息；模型原生使用；Router/expert utility/遗忘收益。

Next decision：只有当研究问题转向“这些局部方向能否预测 expert 相对效用”时，才另行注册功能实验；本几何结果不自动启动该实验。

## 10. 运行与工件

- job：`pt-1qp1h2z0`，`SUCCEEDED`，2026-08-19 07:17:39Z–07:20:32Z。
- source snapshot：`/data/250010109/MoE_Router/experiments/20260819_a15_08_06_e04_z_ru_hierarchical_geometry/source-snapshots/formal-20260819T_e04_zru_geometry_r1`。
- raw result：`/data/250010109/MoE_Router/experiments/20260819_a15_08_06_e04_z_ru_hierarchical_geometry/runs/formal-20260819T_e04_zru_geometry_r1`。
- analysis manifest：`analysis/z_ru_geometry_manifest.json`，SHA256 `95e3d5ae3972fbcaa1c56cc0660ed18fc4f8a3caa4abdb305f4214a1bf9d2af3`。
- code hash：formal `z_ru_geometry_8gpu.py` SHA256 `cab1c04ab4c67afbd0784c9851868256e62fd6eb9d3f24a0031dcbf4d4739f71`。
- curated tables：[experiment_one_verdict_basis.csv](tables/experiment_one_verdict_basis.csv)、[spectrum_depth_summary.csv](tables/spectrum_depth_summary.csv)、[experiment_one_manifest.json](tables/experiment_one_manifest.json)。
- pre-submit full tests：90/90 passed；container-specific new tests：5/5 passed。
