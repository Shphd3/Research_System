# S18 详细记录：嵌套度与参考频率

[Summary](summary_cn.md)

执行根目录：`/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S18_nesting_reuse_1108/`。授权来自研究者 2026-11-08 上传的 MIG SNR prompt 任务 C（只用 CPU，复用 S13/S11 缓存，不重选成员）；该 prompt 原字节存于 `20261108_snr_mig_pilot/evidence/authorizing_prompt_20261108.md`。

## 1. 输入（只读，SHA256 前 12 位）

| 输入 | 作用 | 哈希 |
|---|---|---|
| S13 `data/controlled_panel.jsonl` | CONF 行与家族、标签、措辞的对应 | c01851a20497 |
| S13 `data/{ATTN,MLPIN}_SAE_confirmation_z_csr.npz` | CONF Top32 编码 | bc71ab41b4a6 / 57c876b7ebec |
| S13 更替审核 `results/stable_candidate_checks.csv` | DEV 冻结判别成员（`dataset=S13, relation=siblings, dev_stable_candidate`）与 Q/G 计数 | 17b39fd4c148 |
| S13 `results/core_member_records.csv` | 共享成员事件（`relation=siblings, role=retained`） | 64b3b7aed5df |

## 2. 计算

1. 对每个 SAE、措辞，构造 24 标签 × 48 家族 × 30000 的激活指示；出现率 = 家族平均。与 S13 `category_coverage.csv.gz` 对照，最大绝对误差 6.9×10⁻¹⁷（四个组合）。
2. 嵌套度 nest(f,P) = Σ_{l∈{P,子1,子2}} 出现率 / Σ_{全部 24 标签} 出现率；分母为 0 记 NA（本轮 0 个）。
3. 判别成员按 (兄弟对, feature) 计单位、权重 1；共享成员按 (兄弟对, feature) 汇总事件数作权重。
4. 对比：阈值 τ∈{0.5, 1/3, 2/3}，复用型（nest<τ）减嵌套型（nest≥τ）的 Q、G 均值差；Spearman ρ(nest, 频率)。
5. 不确定性：(a) 家族 bootstrap 2000 次（重抽 48 个 CONF 家族，重算出现率、嵌套度和分类；成员与频率固定）；(b) 场景簇 bootstrap 500 次；(c) 事后补充：成员重抽样 4000 次（分类固定，重抽成员）。

代码：`code/analyze_nesting.py`（7a9cfe54…）、`code/supplement_members.py`（41e575b1…，看过主表后补充）。

## 3. 全部结果

- 主表：`results/nesting_contrasts.csv`（f617ac51…）——两 SAE × 两措辞 × 三阈值 × Q/G，含家族与簇区间，及 Spearman 行。
- 单位表：`results/member_nesting_units.csv`（b39ead0c…）——每个判别/共享单位的嵌套度、Q、G、权重。
- 成员重抽样：`results/member_bootstrap_supplement.csv`（7ac33b69…）。
- 分兄弟对计数：`results/per_pair_counts.csv`；命名例子：`results/named_cases.csv`。

### 3.1 显式措辞、τ=0.5 摘要

| SAE | 种类 | 嵌套 / 复用（单位或事件权重） | Q 均值 嵌套 → 复用 | 复用−嵌套 [家族区间] [成员区间] |
|---|---|---|---|---|
| Attention | 判别 | 22 / 44 | 0.82% → 8.98% | 8.17pp [7.24, 8.57] [4.54, 12.67] |
| Attention | 共享 | 487 / 8035 事件 | 1.30% → 14.57% | 13.27pp — [10.09, 16.62] |
| MLP | 判别 | 20 / 21 | 0.48% → 45.32% | 44.84pp [42.79, 44.84] [30.16, 58.85] |
| MLP | 共享 | 493 / 9479 事件 | 1.15% → 41.77% | 40.62pp — [36.01, 45.10] |

家族区间的点估计贴近上界，是因为重抽家族时边界成员会换类、把差拉小；分布偏斜，不是计算错误。

### 3.2 敏感性

τ=1/3：Attention 29/37，差 8.66pp；MLP 21/20，差 46.44pp。τ=2/3：Attention 18/48，差 7.69pp；MLP 19/22，差 42.76pp。保留名称改写：Attention 24/42，差 8.53pp；MLP 与显式相同（20/21）。区间均不含 0。

## 4. 未运行与偏差

- S11 四域数据只用作成员定义来源的一致性背景，没有单独计算嵌套度（4 个父类太少），NOT RUN。
- “没学好”解释的检验（更大模型或更晚 checkpoint）NOT RUN。
- 无新前向、无训练、无干预。
