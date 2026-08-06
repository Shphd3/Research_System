# Qwen3-8B 实验 Agent 执行计划

## 0. 文档定位

本文档是面向实验 agent 的**执行手册**，不是高层 brainstorming 文档。  
它的任务是把当前研究主线拆成可执行阶段、硬性门槛、固定输入、固定输出和失败分支，保证实验过程可复现、可审计、可中途止损。

上游理论与背景来源于两份已有文档：
- `01_toy_report.md`：已经在 toy model 中验证“统一 WD + 全局 LR decay 会导致 tail 死亡；WD/LR 同时解耦可以救回 tail”。
- `02_real_representation_model_plan.md`：已经给出从 toy 走向真实模型的高层路线 A -> B -> C。

本文档的用途是：  
**让实验 agent 先完成真实模型阶段的第一轮严密执行，并在每个阶段结束时交付可判断的中间结论。**

---

## 1. 背景解析

### 1.1 已完成的理论闭环

当前主线已经完成 toy 级别的命题 C 验证：

1. Flat / coupled 结构的失败，不是表达能力不够，而是统一优化条件导致 tail 特征同时遭受：
   - Weight Decay 压低稳态上限；
   - 全局 LR decay 过早关闭有效学习时间窗。
2. 只放松 WD 或只延长 tail 的 LR，都只能部分救援。
3. 只有把 Common / Tail 物理拆开，并给 Tail 独立、宽松的 WD / LR，tail 才能显著恢复。

这意味着：  
**当前最关键的不确定性已经不在优化理论本身，而在于这些结论能否迁移到真实 LLM 的表征与训练动力学中。**

### 1.2 为什么下一步不能直接上完整 MoE

如果现在直接做完整 Hierarchical MoE，会同时引入三类新变量：
- projector 是否正确；
- common / tail 分支是否必要；
- router / experts 是否真的带来 specialization。

这样一旦结果不好，就无法定位问题到底出在：
- 真实 hidden state 根本没有明显的 shared head；
- shared head 存在，但选错了层或 $k$；
- projector 对了，但 Tail 的优化条件仍不够；
- 结构和优化都对，但 routing 才是新瓶颈。

因此，下一轮科研迭代必须坚持单变量推进：

1. 先验证**真实表征解耦**是否成立；
2. 再验证**无路由条件下的分支解耦 + 优化解耦**是否成立；
3. 最后验证**Hierarchical MoE specialization** 是否成立。

### 1.3 当前迭代的核心研究问题

本轮实验 agent 需要回答三个递进问题：

1. Qwen3-8B 的真实 hidden state 中，是否存在可被 top principal directions 表征的 shared head？
2. 切除 shared head 后的 residual tail 空间，是否更利于 WoS 领域语义的线性区分与路由？
3. 若答案是肯定的，那么在固定 projector 的前提下，仅靠 split-FFN + decoupled optimization，是否已能改善 rare / domain-specific 指标？

---

## 2. 总体执行原则

### 2.1 阶段门槛

实验 agent 必须按以下顺序执行：

1. `Phase 0`：环境与数据检查
2. `Phase A`：冻结表征诊断
3. `Phase B`：单层 split-FFN / no-routing 验证
4. `Phase C`：最小版 Hierarchical MoE

其中：
- `Phase A` 是**必须立即执行**的当前主任务。
- `Phase B` 只有在 `Phase A` 达到通过门槛后才允许执行。
- `Phase C` 只有在 `Phase B` 达到通过门槛后才允许执行。

### 2.2 不允许的做法

实验 agent 不得：
- 同时改动 projector、分支结构、router 和 optimizer 再一起汇报；
- 在未记录原因的情况下私自修改数据规模、层位、$k$、WD、LR、路由方式；
- 只汇报最好结果，不汇报扫描范围与失败配置；
- 用单次随机种子结果代替稳定结论；
- 在 `Phase A` 尚未确认 shared head 存在前，就宣称需要完整 MoE 改造。

### 2.3 输出优先级

实验 agent 的输出优先级如下：

1. 先给结构化表格与数值结论；
2. 再给图；
3. 最后才给文字解释。

若数值和图冲突，以数值表和原始日志为准。

---

## 3. 固定输入与默认设置

### 3.1 模型

- Backbone：本地 `Qwen3-8B`
- 本轮默认：冻结 backbone
- Hidden state 抽取位置：`post-attention / pre-FFN`

### 3.2 数据

- Common 数据：Wiki 通用文本
- Tail 数据：WoS 四领域文档
- WoS 首轮固定四类：
  - `Medical`
  - `Psychology`
  - `CS`
  - `Biochemistry`

### 3.3 默认规模

- Wiki：2,000 篇文档
- WoS：每类 1,000 篇文档
- 统一 `max_length = 512`
- 协方差估计时的 token 池采样比例：`Wiki:WoS = 4:1`
- WoS 文档级 train / val / test 划分：`70 / 15 / 15`
- 重复种子数：5

### 3.4 层位与 $k$ 扫描

- 若总层数记为 $L$，首轮扫描层位：
  - $\lfloor 0.15L \rfloor$
  - $\lfloor 0.40L \rfloor$
  - $\lfloor 0.65L \rfloor$
  - $\lfloor 0.90L \rfloor$
- 首轮扫描 $k$：
  - $\{4, 8, 16, 32, 64\}$
- 若前述 $k$ 的 explained variance 明显不足，再补：
  - $\{96, 128\}$

### 3.5 数值精度

- 模型前向：可用 `bfloat16`
- 均值、协方差、SVD、probe 训练与统计：统一转 `float32`

---

## 4. 目录与产物约定

实验 agent 必须把所有产物集中写到以下目录：

`daily_research_reports/0417/exp/agent_runs/qwen3_8b_cycle1/`

建议目录结构：

```text
agent_runs/qwen3_8b_cycle1/
  phase0_env_check/
    manifest.md
    env_info.json
    data_inventory.csv
  phaseA_probe/
    config.json
    hidden_manifest.csv
    eigenspectrum/
    probes/
    metrics/
    figures/
    summary.md
  phaseB_split_ffn/
    config.json
    logs/
    checkpoints/
    metrics/
    figures/
    summary.md
  phaseC_hier_moe/
    config.json
    logs/
    checkpoints/
    metrics/
    figures/
    summary.md
  final_decision.md
```

命名规则：
- 每次实验都必须保存 `config.json`
- 每个 summary 都必须写明：
  - 输入数据
  - 层位
  - $k$
  - 随机种子
  - 关键指标均值与标准差
  - 是否通过阶段门槛

---

## 5. Phase 0：环境与数据检查

### 5.1 目标

在开始任何模型前向与训练前，确认：
- `Qwen3-8B` 可正常加载；
- Wiki 与 WoS 数据可访问；
- WoS 标签映射无歧义；
- 实验目录、日志目录、缓存目录可写。

### 5.2 必做事项

1. 记录模型标识、精度模式、设备信息、可用显存。
2. 统计 Wiki / WoS 实际可用样本数。
3. 记录 WoS 四类标签名与每类样本量。
4. 记录 tokenizer 的 `max_length`、截断策略、padding 策略。
5. 输出一份 `manifest.md`，明确说明：
   - 哪些输入已就绪；
   - 哪些输入缺失；
   - 是否能继续进入 `Phase A`。

### 5.3 通过门槛

满足以下条件才允许进入 `Phase A`：
- 模型前向正常；
- 四类 WoS 数据齐全；
- 至少满足默认数据规模的 80%；
- 目录与日志写入正常。

若不满足，实验 agent 必须停止，并在 `final_decision.md` 中写明阻塞项。

---

## 6. Phase A：冻结表征诊断

### 6.1 目标

验证真实表征解耦假设是否成立：

> 在 Qwen3-8B 的某些层，shared head 主导 top principal directions；切除这些方向后的 residual tail 空间，比 raw 或 simple centering 更利于 WoS 领域语义的区分。

### 6.2 待验证假设

- `H_A1`：hidden state 协方差谱明显 head-heavy。
- `H_A2`：`centered` 相比 `raw` 只有有限提升。
- `H_A3`：`tail residual` 相比 `centered` 有稳定的 probe / purity / NMI 提升。
- `H_A4`：删除过多 top-$k$ 后性能会回落，说明不是“删得越多越好”。

### 6.3 实验输入

- 冻结的 `Qwen3-8B`
- Wiki 文档 2,000 篇
- WoS 四类文档，每类 1,000 篇
- 扫描层位：4 个
- 扫描 $k$：5 到 7 个取值

### 6.4 执行步骤

1. 预处理数据：
   - 清洗空文档与过短文档；
   - 统一分词与截断；
   - 保存文档 id、类别标签、长度统计。
2. 前向提取 hidden states：
   - 在四个目标层提取 `post-attention / pre-FFN` hidden state；
   - 分别保存 token 级与文档级索引映射。
3. 估计几何统计量：
   - 用 `Wiki:WoS = 4:1` 的混合 token 池估计每层 $\mu$ 与 $\Sigma$；
   - 计算 eigenspectrum；
   - 对每个 $k$ 构造 $V_k$。
4. 构造三类表示：
   - `raw`
   - `centered`
   - `tail = (I - V_kV_k^\top)(h-\mu)`
5. 文档级评估：
   - 对 WoS 文档做 mean pooling；
   - 在三类表示上训练同构的 4-way 线性 probe；
   - 计算 accuracy、macro-F1、confusion matrix。
6. 路由代理评估：
   - 用同构线性 router 预测 WoS 类别；
   - 计算 purity / NMI。
7. 几何评估：
   - 计算 $\mathrm{Sep}_F$
   - 计算 explained variance 与谱陡峭度
8. 结果聚合：
   - 按层、按 $k$ 汇总均值和标准差；
   - 选出最优层和最优 $k$。

### 6.5 关键指标

主指标：
- WoS domain linear probe accuracy
- router purity
- NMI
- $\mathrm{Sep}_F$

辅助指标：
- macro-F1
- confusion matrix
- explained variance curve
- eigenspectrum slope

### 6.6 通过门槛

`Phase A` 判为通过，必须同时满足：

1. 至少一个层位和一个 $k$ 上，`tail` 相比 `centered` 在主指标中至少两项稳定提升；
2. 该提升在 5 个随机种子下方向一致；
3. `centered` 相比 `raw` 的增益明显小于 `tail` 相比 `centered` 的增益；
4. 当 $k$ 继续增大时，主指标出现平台或下降，说明确实存在合理的最佳 $k$。

### 6.7 失败分支

如果 `Phase A` 不通过，按以下顺序排查：

1. 是否层位选错：
   - 增补 2 个邻近层再测；
2. 是否 $k$ 扫描过粗：
   - 在最佳区间补更密的 $k$；
3. 是否文档级 pooling 抹掉了 token 局部信号：
   - 补做 token-level 稀有 token bucket 分析；
4. 是否 WoS 主 proxy 过粗：
   - 补做局部语义簇 proxy。

若补充排查后仍不通过，本轮实验终止，不进入 `Phase B`。

### 6.8 必交付产物

- `metrics/layer_k_summary.csv`
- `metrics/probe_results.csv`
- `metrics/router_results.csv`
- `figures/eigenspectrum_layer_*.png`
- `figures/probe_accuracy_vs_k.png`
- `figures/purity_nmi_vs_k.png`
- `summary.md`

`summary.md` 必须回答：
- shared head 是否存在；
- 最优层位是哪个；
- 最优 $k$ 是多少；
- `tail residual` 是否优于 `centered`；
- 是否允许进入 `Phase B`。

---

## 7. Phase B：单层 Split-FFN / No-Routing 验证

### 7.1 进入条件

只有当 `Phase A` 明确给出：
- 一个最佳层位；
- 一个最佳 $k$；
- 并且 `tail residual` 相比 `centered` 有稳定提升；

才允许进入 `Phase B`。

### 7.2 目标

验证在真实模型中，即便先不做 MoE，只做：
- `common branch + tail branch`
- tail 独立 WD / LR

是否已能改善 rare / domain-specific 指标。

### 7.3 待验证假设

- `H_B1`：只做 split-FFN，但仍使用统一 WD / LR，收益有限。
- `H_B2`：split-FFN + decoupled optimization 会显著改善 rare / domain-specific 指标。
- `H_B3`：这些改善不会显著伤害 common / frequent 指标。

### 7.4 固定实现

- 只改造 `Phase A` 选出的 1 个最佳层位
- backbone 冻结
- projector 固定，不在线更新
- 使用：
  \[
  h_{\text{out}} = h + F_c(h) + F_t(h_{\text{tail}})
  \]

### 7.5 对比配置

1. `Baseline FFN`
2. `Split-FFN / coupled-optim`
3. `Split-FFN / decoupled-optim`

默认超参：
- `lr_common = 1e-4`
- `wd_common = 1e-2`
- `lr_tail = 3e-4`
- `wd_tail = 1e-4`
- `hold_ratio = 0.8`

### 7.6 关键指标

主指标：
- overall validation perplexity
- rare-token perplexity
- domain-specific perplexity

辅助指标：
- frequent-token perplexity
- rare-token top-1 / top-k accuracy
- tail branch activation norm
- tail branch parameter norm
- tail branch gradient/update count

### 7.7 通过门槛

`Phase B` 判为通过，必须同时满足：

1. `Split-FFN / decoupled-optim` 的 rare/domain 主指标优于另外两组；
2. `Split-FFN / coupled-optim` 与 baseline 差距有限，支持“关键是优化解耦而非仅仅分支化”；
3. frequent-token 指标不出现明显恶化；
4. tail branch 的参数范数与有效更新数显著高于 coupled 版本。

### 7.8 必交付产物

- `metrics/ppl_summary.csv`
- `metrics/rare_token_metrics.csv`
- `metrics/tail_branch_dynamics.csv`
- `figures/rare_vs_frequent_ppl.png`
- `figures/tail_norm_update_curve.png`
- `summary.md`

`summary.md` 必须回答：
- 分支化本身是否足够；
- 优化解耦是否必要；
- 是否允许进入 `Phase C`。

---

## 8. Phase C：最小版 Hierarchical MoE

### 8.1 进入条件

只有当 `Phase B` 明确支持“优化解耦在真实模型中有效”时，才允许进入 `Phase C`。

### 8.2 目标

验证完整命题：

> router 应在 `h_{tail}` 上工作，而非 raw hidden state；同时 tail experts 需要独立 WD / LR。

### 8.3 固定实现

- 仅在 `Phase A / B` 选出的 1 至 2 个关键层引入 tail-MoE
- backbone 冻结
- common path 保持 dense
- tail path 使用 `E = 4` 个 experts
- routing 默认 `top-1`

块结构：
\[
h_{\text{out}} = h + F_c(h) + \sum_{e=1}^{E} g_e(h_{\text{tail}}) E_e(h_{\text{tail}})
\]

### 8.4 对比配置

1. `Flat MoE / raw router / uniform WD+LR`
2. `Tail-router only / raw common path`
3. `Tail-router + decoupled WD`
4. `Tail-router + decoupled WD + decoupled LR`

### 8.5 关键指标

主指标：
- rare / domain token perplexity
- router purity
- NMI
- rare expert survival ratio

辅助指标：
- expert occupancy
- per-expert effective update count
- per-expert parameter norm
- per-expert gradient norm

### 8.6 通过门槛

`Phase C` 判为通过，必须同时满足：

1. Hierarchical 版本的 purity / NMI 高于 flat MoE；
2. rare / domain token 的 ppl 更低；
3. rare experts 的 update count 与 survival ratio 更健康；
4. common 侧性能无明显退化。

### 8.7 必交付产物

- `metrics/router_summary.csv`
- `metrics/expert_dynamics.csv`
- `metrics/ppl_summary.csv`
- `figures/router_purity_nmi.png`
- `figures/expert_survival.png`
- `summary.md`

`summary.md` 必须回答：
- router 是否应工作在 `h_tail` 上；
- tail experts 是否确实需要独立 WD / LR；
- 是否形成完整 specialization 闭环。

---

## 9. 实验记录规范

实验 agent 每跑完一个阶段，必须同步更新：

1. `config.json`
2. `summary.md`
3. `final_decision.md`

其中 `final_decision.md` 必须使用固定格式：

```text
Phase:
Question:
Answer:
Passed:
Best layer:
Best k:
Key metrics:
Primary evidence files:
Next action:
Risks:
```

任何超参或采样策略的变更，都必须追加到该阶段的 `summary.md`，并写明：
- 变更前设置
- 变更后设置
- 变更原因
- 对结论的影响

---

## 10. 本轮推荐执行顺序

实验 agent 本轮只应保证完成以下闭环：

1. `Phase 0`
2. `Phase A`
3. 若 `Phase A` 通过，则进入 `Phase B` 的最小实现

本轮不要求必须完成 `Phase C`。  
更合理的策略是：
- 本轮把 `Phase A` 跑扎实；
- 若 `Phase A` 很强，再推进 `Phase B`；
- `Phase C` 作为下一轮增量任务。

原因很简单：  
当前最大的不确定性不是 MoE 结构，而是**真实 LLM 表征中 shared head 的存在性、层位与 $k$ 的选择**。  
这一点若不钉死，后续所有结构改造都缺乏稳定基座。

---

## 11. 最终预期结论格式

实验 agent 完成本轮后，应最终给出以下三类结论之一：

### 类型 A：强支持

- Qwen3-8B 中存在明确 shared head
- `tail residual` 明显优于 `centered`
- split-FFN + decoupled optimization 进一步改善 rare/domain 指标

这意味着下一轮应直接进入最小版 Hierarchical MoE。

### 类型 B：部分支持

- shared head 存在，但层位或 $k$ 敏感
- `tail residual` 仅在部分 proxy 上有效
- split-FFN 收益有限

这意味着下一轮应优先打磨 projector 选择、proxy 设计与 pooling 方式，而不是急着上 MoE。

### 类型 C：当前不支持

- 未观察到稳定 shared head -> tail residual 优势
- 或观察到几何差异，但功能指标不配合

这意味着当前主线需要回到表征定义本身，重新检查：
- hidden state 位置是否选错；
- proxy 是否过粗；
- `raw / centered / tail` 的统计口径是否不合适。

---

## 12. 一句话执行指令

**先把 Qwen3-8B 上的 frozen representation probe 做扎实，找到最优层和最优 $k$；只有当 `tail residual` 的优势在 WoS domain 任务上被稳定验证后，才进入 split-FFN 与后续 Hierarchical MoE。**
