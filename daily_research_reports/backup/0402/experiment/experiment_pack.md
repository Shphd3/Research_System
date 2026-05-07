# Experiment Pack v2

## 1. Task Restatement

本轮实验不再围绕“对角线方差形式是否成立”展开。

当前主线已经更新为：

- 关注哪些二阶 / 低秩子空间结构与 MoE 专家分发真正相关；
- 以及训练得到的 router 是否已经学会利用这些结构。

因此，本轮实验必须拆成两个独立 round，顺序执行，但目录和结果保持分离：

### Round A: Clustering / Separation Audit

只回答一个问题：

`二阶 / 低秩子空间表示是否比一阶表示更能揭示 domain / semantic structure？`

### Round B: Interference / Geometry Audit

只回答一个问题：

`当前训练得到的 quadratic_low_rank 系列模型，是否已经形成更清晰的 expert geometry、更低的跨域 overlap，以及更合理的 routing structure？`

本轮不做：

- 新 router 设计
- 更大 benchmark 扩展
- forgetting / two-task 结论
- 对旧 diagonal variance routing 叙事的重复验证

---

## 2. Updated Model Priority

### Core Models

1. `quadratic_low_rank` (off)
   - 原因：Round3 `SI` 最低，是当前最值得看的结构模型

2. `quadratic_low_rank_acp_lite`
   - 原因：Round2 高噪声 `CR` 最强，Round0 任务表现也强，是当前最平衡的候选

3. `quadratic_low_rank_linear`
   - 原因：作为 low-rank 路线的辅助对照，帮助区分 ACP-lite 通道的作用

### Auxiliary Controls

4. `linear_running_center`
   - 原因：严格 baseline

5. `acp_lite`
   - 原因：当前最强公平 first-order comparator

### De-prioritized Models

6. `quadratic_nosvd`
7. `quadratic_nosvd_debias`
8. `quadratic_nosvd_debias2`

这些模型现在只保留为辅助参考，不再是本轮主线。

---

## 3. Protocol Lock

### Data

- 数据集：WoS（domain-labeled）
- 数据路径：
  `/data/share/109_cache_dir/hf_data/datasets/river-martin___web-of-science-with-label-texts`

### Base Model for Round A

- Base model：
  `/data/share/Qwen3-4B`
- 用途：只做 frozen feature extraction，不训练

### Checkpoints for Round B

优先使用 step `50000`。如果不存在，则回退到 step `40000`，但必须在结果中明确记录。

### Project Root

- 新项目目录：
  `/data/250010109/spectral_router/exp_quadratic_semantics`

### Script Layout

- `scripts/roundA/run_roundA_clustering.py`
- `scripts/roundB/run_roundB_interference.py`

### Output Layout

- `output/roundA/`
- `output/roundB/`

### Fixed Boundary

1. Round A 和 Round B 必须作为两个独立实验 round 执行。
2. 不允许把两个 round 混成一个大实验。
3. 不允许改理论目标。
4. 不允许擅自增加新模型。
5. 不允许只给日志，必须输出结构化结果。

---

## 4. Round A Redefinition

### Goal

验证二阶 / 低秩子空间表示是否比一阶表示更能揭示 domain / semantic grouping。

### Representation Comparison

至少比较以下表示：

1. First-order:
   - `z^(1) = x_c`

2. Second-order diagonal:
   - `z^(2) = x_c ⊙ x_c`

3. Debiased second-order:
   - `z^(2)_deb = x_c ⊙ x_c - λ_t`

4. 如实现方便，可加入一个低秩 / PCA-projected second-order representation
   - 但必须在结果中说明它与前两者的关系

### Minimal Procedure

1. 加载 Qwen3-4B 和 WoS 数据集。
2. 抽取 token-level hidden features。
3. 构造一阶与二阶表示。
4. 必要时统一降维到相同维数。
5. 做 clustering / grouping / separation analysis。
6. 生成一阶 vs 二阶表示的直接比较结果。

### Metrics

主指标：

- clustering quality
- separation quality

辅助指标：

- silhouette score
- purity
- 如果标签适合，可报告 NMI/AMI，但不是本轮唯一核心
- visualization（PCA / t-SNE / UMAP 任一即可）

### Decision Rule

- 如果二阶表示稳定地比一阶表示更能揭示 domain / semantic structure，则支持“二阶结构中包含与 routing 相关的信息”。
- 如果没有明显优于一阶表示，则当前 variance-aware 叙述需要降级。
- 如果不同表示结果接近，则结论记为 `unclear`。

### Output

- `output/roundA/clustering_comparison.json`
- `output/roundA/visualizations/...`
- `output/roundA/roundA_summary.json`

---

## 5. Round B Redefinition

### Goal

检查当前训练得到的 quadratic_low_rank 系列模型，是否已经表现出更清晰的 expert geometry、更低 overlap 和更合理的分发结构。

### Compared Models

Core:

- `quadratic_low_rank` (off)
- `quadratic_low_rank_acp_lite`
- `quadratic_low_rank_linear`

Controls:

- `linear_running_center`
- `acp_lite`

### Minimal Procedure

1. 对每个目标 checkpoint 运行 forward pass。
2. 提取 routed activations 与 expert assignments。
3. 按 domain 划分 routed activations。
4. 计算 per-expert covariance。
5. 计算 cross-domain overlap / interference / occupancy 指标。
6. 汇总 expert usage 与 token-level evidence。

### Metrics

主指标：

- `SI_e`
- `r_0.9`
- covariance overlap

辅助指标：

- per-domain expert usage
- token-level expert assignment pattern
- load balance

### Decision Rule

- 如果 quadratic_low_rank 系列在 `SI_e`、occupancy 和 expert usage structure 上都更清晰，且没有明显 collapse，则支持“模型正在学会利用相关结构信息”。
- 如果几何指标没有改善，或者 collapse 明显，则削弱该主张。
- 如果部分指标改善、部分不改善，则记为 `partial / unclear`。

### Output

- `output/roundB/{model_tag}/interference_metrics.json`
- `output/roundB/{model_tag}/domain_expert_usage.json`
- `output/roundB/cross_model_comparison.json`
- `output/roundB/roundB_summary.json`

---

## 6. Implementation Plan

### Directory Structure

```text
exp_quadratic_semantics/
├── docs/
│   ├── roundA/
│   └── roundB/
├── scripts/
│   ├── roundA/
│   │   └── run_roundA_clustering.py
│   └── roundB/
│       └── run_roundB_interference.py
└── output/
    ├── roundA/
    └── roundB/
```

### Round A Script Responsibilities

- 加载 WoS 和 Qwen3-4B
- 抽取 hidden features
- 构造多种表示
- 运行 clustering / separation analysis
- 生成比较结果与 summary

### Round B Script Responsibilities

- 加载目标 MoE checkpoints
- 抽取 routed activations 和 expert assignments
- 计算 `SI_e`、`r_0.9`、overlap
- 汇总 domain-level / token-level expert statistics
- 生成跨模型比较结果与 summary

---

## 7. Output Contract

| Round | File | Content |
| --- | --- | --- |
| A | `clustering_comparison.json` | 一阶 vs 二阶 / 低秩表示的指标比较 |
| A | `visualizations/*` | 可视化输出 |
| A | `roundA_summary.json` | Round A 的结论与置信度 |
| B | `{model_tag}/interference_metrics.json` | `SI_e`、`r_0.9`、overlap |
| B | `{model_tag}/domain_expert_usage.json` | 按 domain 的 expert usage |
| B | `cross_model_comparison.json` | 跨模型对比 |
| B | `roundB_summary.json` | Round B 的结论与置信度 |

实验完成后，必须额外输出：

- `Result Pack`
- `Experiment -> Theory Card`

---

## 8. Risk Check

| Risk | Mitigation |
| --- | --- |
| step50000 不存在 | 回退到 step40000，并在 summary 里写清 |
| Round A 结果受降维方法影响 | 固定 1-2 种方法，保持比较公平 |
| Round B 指标受 collapse 干扰 | 必须同时报告 load balance 和 usage pattern |
| quadratic_low_rank 系列存在配置差异 | 在 cross-model comparison 中显式记录配置 |
| 结果解释偏离当前主线 | 所有 summary 必须围绕 H1/H2/H3/H4-B，不得扩题 |

---

## 9. Execution Checklist

- [ ] 创建项目目录与 roundA / roundB 脚本目录
- [ ] 确认 WoS 数据路径和 Qwen3-4B 路径可用
- [ ] 确认目标 checkpoints 的 step50000 / step40000 可用性
- [ ] 实现 `run_roundA_clustering.py`
- [ ] 跑 Round A，并产出 summary
- [ ] 实现 `run_roundB_interference.py`
- [ ] 跑 Round B，并产出 summary
- [ ] 统一整理为 `Result Pack`
- [ ] 输出 `Experiment -> Theory Card`

---

## 10. Start Execution

现在不要再停留在旧认知里。

请直接按本 `Experiment Pack v2` 开始执行，顺序如下：

1. 先检查路径与 checkpoint 是否存在。
2. 创建项目目录结构。
3. 先实现并执行 Round A。
4. Round A 完成后，再实现并执行 Round B。
5. 最后统一输出 `Result Pack` 和 `Experiment -> Theory Card`。

如果遇到阻塞：
- 只允许提出最小必要问题；
- 不允许整体改题；
- 不允许把两个 round 混成一个大实验。

**Protocol locked, ready for execution.**
