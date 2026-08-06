# exp\_synthetic\_data 实验执行计划（Protocol v1）

## 1) Summary

本计划用于在 `/data/250010109/spectral_router/exp_synthetic_data` 内落地 v6.5 文档第 7 节的 synthetic benchmark 主线，按“先数据生成与几何验证，再冒烟训练，再全量 4-router 对比，再结构化报告与状态文档回填”的顺序执行。\
本轮采用 **DeepSpeed ZeRO-0 主线**（可在 2 卡本地与 8 卡集群复用），并以 **冻结 backbone 的严格对比** 为主，随后补充“同初始化联合训练”作为扩展对照。

## 2) Current State Analysis

* 已确认 `exp_synthetic_data` 当前仅有文档：

  * `/data/250010109/spectral_router/exp_synthetic_data/docs/MoE - 迭代状态存档 v6.5.md`

* 已有可复用训练入口：

  * `/data/250010109/spectral_router/train_qwen3_moe.py`（支持 `router_type={linear,quadratic,low_rank,quadratic_low_rank}`，支持 `--zero_stage`）

  * `/data/250010109/spectral_router/scripts/run_moe.sh`（当前为预训练场景，需新增 synthetic 专用启动脚本）

* 已有 router 实现位于：

  * `/data/250010109/spectral_router/src/model/qwen3_moe/myqwen.py`

* 已有可复用聚类指标实现参考：

  * `/data/250010109/spectral_router/exp_quadratic_semantics/scripts/roundA/run_roundA_clustering.py`（含 NMI/ARI）

* 现缺口：synthetic 数据生成、2 层最小模型训练入口、Type1/2/3 分类型评估、PCA/t-SNE sanity、统一报告产物。

## 3) Proposed Changes (files + what/why/how)

### A. 数据生成与可视化验证

1. 新增 `/data/250010109/spectral_router/exp_synthetic_data/data/generate_continuous_hmm.py`

   * What: 生成 Continuous HMM 序列数据，产出 train/val/test 及 token latent label `z_token`。

   * Why: 修复“token 继承句子标签”漏洞，提供可控 token-level ground truth。

   * How:

     * 统一公式：`x_i = mu_global + mu_local(z_i) + Sigma(z_i)^(1/2) * eps_i`

     * Type1(mean-separable)：主要由 `mu_local` 分离，`Sigma` 近各向同性

     * Type2(covariance-separable)：保留小幅 `mu_local` 偏移，但主分离来自类别专属低秩正交方差拉伸

     * Type3(hybrid-separable)：序列级混合 Type1/Type2 token 段

     * 输出 `.npz`（features, z\_token, split, type\_id, metadata）与可选 `.jsonl` 索引

2. 新增 `/data/250010109/spectral_router/exp_synthetic_data/scripts/sanity_check_geometry.py`

   * What: PCA/t-SNE 与统计检验（均值差/协方差谱差）

   * Why: 在训练前数学确认 Type1/Type2 结构满足设计

   * How:

     * Type1 验证：类间均值距离显著高于类内均值差

     * Type2 验证：类间主轴子空间夹角/谱差显著，均值差仅次级

     * 输出图与数值到 `exp_synthetic_data/output/<run>/sanity/`

### B. 训练主线（2 层最小模型 + 4 router 对比）

1. 新增 `/data/250010109/spectral_router/exp_synthetic_data/train/train_synth_moe.py`

   * What: 2 层最小 Transformer 训练脚本（Layer1 Dense FFN，Layer2 Top-1 MoE）

   * Why: 满足第 7 节最小实验设计，减少与大模型预训练脚本耦合

   * How:

     * router 对比：`linear_running_center`、`acp_lite`、`old_diagonal_quadratic`、`hybrid_route(quadratic_low_rank + acp)`

     * 参数量匹配：对每个 router 输出参数统计并校验 `O(Kd)` 同量级

     * 训练阶段：

       1. 冒烟：单 router 小步数，验证收敛与日志完整
       2. 全量：4 router × 3 dataset type（可串行或并行）

     * Backbone 策略：

       * 主实验：冻结 backbone，仅训练 router/专家

       * 扩展实验：同初始化联合训练（保持相同 seed）

2. 新增 `/data/250010109/spectral_router/exp_synthetic_data/scripts/run_synth_moe.sh`

   * What: 统一启动脚本（本地 2 卡 + 集群 8 卡参数模板）

   * Why: 可直接执行，替代当前面向预训练的 `run_moe.sh`

   * How:

     * 默认 `zero_stage=0`（ZeRO-0）

     * 提供 smoke/full 两档配置

     * 提供 router\_type、dataset\_type、seed、冻结策略等显式开关

### C. 评估与结果汇总

1. 新增 `/data/250010109/spectral_router/exp_synthetic_data/eval/evaluate_routing_alignment.py`

   * What: 计算主指标并按 Type1/2/3 独立输出

   * Why: 对齐 handoff block 的核心结论标准

   * How:

     * Task Loss (MSE)

     * Routing Alignment: `NMI(E, z_token)`、`ARI(E, z_token)`

     * Load balance: `CV_load`

     * Eigenvalue Spectrum: 每 expert 的特征值谱与低秩性指标

2. 新增 `/data/250010109/spectral_router/exp_synthetic_data/scripts/summarize_results.py`

   * What: 汇总各 run 指标，生成 markdown 表格与综合排名

   * Why: 支撑最终报告与状态文档回填

   * How:

     * 产出总体表、分 Type 明细表、相对 baseline 增量表（Δ）

### D. 文档与回填

1. 新增 `/data/250010109/spectral_router/exp_synthetic_data/README.md`

   * What: 大实验索引（round 状态、运行命令、产物路径、关键结论）

   * Why: 保持实验可追溯与后续轮次对接

2. 新增 `/data/250010109/spectral_router/exp_synthetic_data/docs/round_v6_5_synth_execution.md`

   * What: 本轮详细执行文档（目标、方法、指标、结果解释、假设更新）

   * Why: 满足实验记录规范

3. 更新 `/data/250010109/spectral_router/exp_synthetic_data/docs/MoE - 迭代状态存档 v6.5.md` 的 `## 8. Experiment Return`

   * What: 回填 5 项交付（objective/steps/results/analysis/hypothesis update）

   * Why: 与迭代主文档保持一致

## 4) Assumptions & Decisions (locked)

* 决策 1：训练框架采用 **DeepSpeed ZeRO-0** 主线，不先重写纯 DDP。

* 决策 2：先执行 **冻结 backbone** 的严格对比；再补充“同初始化联合训练”扩展。

* 决策 3：执行顺序固定为：

  1. 数据生成
  2. PCA/t-SNE + 数学 sanity
  3. 单 router 冒烟
  4. 全量 4-router 开训与评估
  5. 报告与状态文档回填

* 决策 4：输出目录统一：`/data/250010109/spectral_router/exp_synthetic_data/output/<experiment_name>/...`

* 决策 5：最终报告必须突出 `NMI(E,z_token)`，并提供分 Type 结果与综合排名。

## 5) Verification Steps

### 阶段 1：数据正确性

* 运行数据生成脚本并检查：

  * 三类数据均成功落盘

  * `z_token` 覆盖所有类别且分布合理

  * metadata 含均值/协方差配置快照

### 阶段 2：几何 sanity

* 运行 PCA/t-SNE 与统计检验：

  * Type1：均值分离显著

  * Type2：协方差/子空间分离显著，均值仅次级

  * Type3：混合结构可观测

### 阶段 3：训练与评估冒烟

* 在 2 卡上完成最小步数训练 + 评估：

  * 训练无 shape/NaN/挂起

  * 可输出 NMI/ARI/CV\_load/TaskLoss

  * 记录每 expert 谱统计文件

### 阶段 4：全量实验

* 跑完 4 router × 3 types（至少固定 seed=1 全覆盖）

* 汇总脚本生成对比表，检查字段齐全

### 阶段 5：交付完整性

* 交付 5 项内容：

  1. 实验目标与数据可视化验证
  2. 实验步骤
  3. 核心指标表（Task Loss, NMI, CV\_load）
  4. 结果分析
  5. 假设更新

* 回填 `v6.5` 文档 `Experiment Return` 区块。

## 6) 风险和阻塞点（提前规避）

* 风险 1：Type2 被均值泄漏主导，导致“伪协方差分离”

  * 规避：生成后做均值差阈值与协方差主轴检验，不达标则重采样

* 风险 2：4 router 参数量不等导致比较失真

  * 规避：训练前打印并落盘 router 参数统计，超阈值则调整 rank/branch

* 风险 3：2 卡显存/吞吐不足

  * 规避：先 smoke 缩短 seq\_len、batch、steps；再逐步放大

* 风险 4：仅冻结策略结论可能偏保守

  * 规避：增加同初始化联合训练作为 secondary evidence

* 风险 5：日志字段缺失影响最终报告

  * 规避：在冒烟阶段先检查所有指标文件 schema，再启动全量

## 7) 结果格式（最终回传模板）

* `report.md`：

  * 实验目标

  * 实验具体步骤

  * 指标总表（含 Δbaseline）

  * 分 Type 明细表

  * 结果分析与结论

  * 假设更新

* `metrics_summary.csv/json`：

  * 字段至少包括：`router`, `dataset_type`, `seed`, `task_loss`, `nmi`, `ari`, `cv_load`, `rank_score`

* `sanity/`：

  * `pca_type1.png`, `pca_type2.png`, `tsne_type1.png`, `tsne_type2.png`, `sanity_stats.json`

***

**Protocol locked, ready for execution**（进入执行后将先完成 Step 1 数据生成与数学结构确认，再推进训练）。
