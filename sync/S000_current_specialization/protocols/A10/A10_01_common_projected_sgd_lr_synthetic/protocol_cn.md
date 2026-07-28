# Protocol CN: A10_01_common_projected_sgd_lr_synthetic

## 0. Approval Snapshot

**Approval status:** Draft for user review. Do not run yet.

**Purpose:** 测试公共梯度投影是否能在合成 output-head 任务中提高 SGD-style update 的临界学习率。

**Primary anchor:** `Projects/from-attention-to-search/main/problem_anchors/10_optimizer_learning_rate_mechanism/10_01_common_projected_sgd_lr_anchor.md`

**Anchor decision question:** 去掉 batch 公共梯度是否能显著提高 SGD 的临界学习率，并且不恶化 rare-token learning？

**Anchor physical prior tested:** 大学习率 SGD 的第一个失败点可能是公共/高频 loud direction。

**Anchor core model term tested:** $G_c=uu^\top G$ 与 $G_r=(I-uu^\top)G$。

**Anchor falsifier:** 公共投影 SGD 不能超过 norm-matched control，或 rare-token loss 明显恶化。

**Experiment role:** root-cause audit / operationalization test，不是 optimizer 方法构造。

**Primary metric from anchor:** $\eta_{\mathrm{crit}}(\mathrm{common\text{-}projected\ SGD}) / \eta_{\mathrm{crit}}(\mathrm{vanilla\ SGD})$。

**Claim boundary from anchor:** 只裁定合成 output-head 中的 common-gradient LR bottleneck；不证明 Adam、Nesterov、真实 LM 或 MoE routing。

**Minimal setup:** 固定 hidden states，只训练一个 softmax output head。

**Basic configuration:** $d=64$，$V=64$；frequent tokens 8 个，rare tokens 56 个；frequent:rare per-class count ratio 初始设为 16:1；每 seed 训练 200 个 full-batch steps。

**Conditions to run:** vanilla SGD；common-projected SGD；norm-matched SGD；random-projected SGD。

**Pass:** projected/vanilla 的 $\eta_{\mathrm{crit}}$ ratio $\ge 3$；projected/norm-matched ratio $\ge 2$；random-projected 不匹配 projected；rare eval loss 不比 vanilla 差超过 5%。

**Fail:** projected/vanilla ratio $\le 1.5$，或 norm-matched / random-projected 给出同等提升。

**Insufficient:** 所有条件都不稳定；synthetic common energy 太低；projected 稳定但 rare loss collapse。

**Cannot claim:** 不能 claim common projection 是最终 optimizer；不能 claim Adam/Nesterov 机制；不能 claim真实 MoE preservation。

**Approval decision:** 等用户确认数据构造、LR grid、pass/fail 阈值后再写英文 canonical `protocol.md` 并执行。

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| 公共方向 (common direction) | batch 中共享的 hidden 方向 | $u=\mathrm{mean}(h_i)/\|\mathrm{mean}(h_i)\|$ | unit vector | 定义要投掉的方向 | 不证明真实 LLM common |
| 公共投影 SGD (common-projected SGD) | 更新前去掉公共方向梯度 | $G_r=(I-uu^\top)G$ | gradient matrix | 主干预 | 不等于最终 optimizer |
| 范数匹配 SGD (norm-matched SGD) | 把 vanilla 梯度缩放到与 $G_r$ 同范数 | $G\cdot\|G_r\|_F/\|G\|_F$ | gradient matrix | 排除“只是梯度变小” | 不测试方向机制 |
| 随机投影 SGD (random-projected SGD) | 投掉随机方向 | $(I-vv^\top)G$ | gradient matrix | 排除“随便投掉一维都有效” | 不定义 common |
| 临界学习率 (critical LR) | 固定窗口内稳定下降的最大 LR | $\eta_{\mathrm{crit}}$ | scalar | 主指标 | 不证明泛化 |
| rare-token loss | rare token 子集交叉熵 | eval CE on rare classes | loss | 检查 rare 学习是否受损 | 不证明语义 rare |

## 2. Anchor Alignment

**Decision question:** 公共梯度是否限制 SGD 临界学习率？

**Physical prior tested:** loud common direction 会压低全局 SGD 学习率。

**Core model term tested:** $G_c=uu^\top G$。

**Falsifier:** norm-matched 或 random-projected control 解释全部提升，或 rare loss 恶化。

**Claim boundary:** 只测试合成 output-head；不进入真实 LM 或 Nesterov 结论。

## 3. Tested Hypothesis

**H1:** common-projected SGD 的 $\eta_{\mathrm{crit}}$ 至少是 vanilla SGD 的 3 倍。

**H2:** 这个提升不是由梯度范数缩小或随机投影解释。

**H3:** common projection 不明显伤害 rare-token learning。

## 4. Rival Explanations

1. **范数缩小解释：** 投掉公共方向只是减小了更新范数，所以更稳定。
2. **随机投影解释：** 任意投掉一维都能提高稳定性，与 common 无关。
3. **token reweighting 解释：** rare 改善来自频率权重变化，而不是公共方向机制。
4. **必要公共信号解释：** 公共方向对 rare token 也必要，投掉后 rare loss 变差。

## 5. Data / Model / Algorithm / Objective

**Data generation:**

- hidden dimension: $d=64$。
- vocabulary size: $V=64$。
- frequent token classes: 8。
- rare token classes: 56。
- per-class count ratio: frequent:rare = 16:1。
- train/eval split: 每个 seed 重新生成 train 与 eval；eval 使用同分布但独立噪声。

**Hidden construction:**

$$
h_i=\alpha_c c+\alpha_y z_{y_i}+\sigma\epsilon_i
$$

- $c$ 是全局公共单位向量。
- $z_y$ 是 token-specific 单位向量，尽量与 $c$ 正交。
- 初始建议：$\alpha_c=2.0$，$\alpha_y=0.5$，$\sigma=0.05$。

**Model:**

- 固定 hidden states。
- 只训练 softmax output head $W$。
- Objective: cross-entropy over target token $y$。

**Update convention:**

- 梯度矩阵使用 $G\in\mathbb{R}^{d\times V}$。
- vanilla update uses $G$。
- projected update uses $G_r=(I-uu^\top)G$。

## 6. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| vanilla SGD | baseline $\eta_{\mathrm{crit}}$ | no projection | 参照基线 | primary | stable LR boundary exists | no stable LR | all LRs unstable | LR stability curve |
| common-projected SGD | H1 | $G_r=(I-uu^\top)G$ | 主干预 | primary | ratio $\ge 3$ vs vanilla | ratio $\le 1.5$ | rare loss collapse | LR table / rare loss |
| norm-matched SGD | Rival 1 | norm shrinkage | 排除范数解释 | guard | projected still $\ge 2$ vs norm-matched | norm-matched matches projected | unstable grid | control table |
| random-projected SGD | Rival 2 | random direction | 排除随机投影解释 | guard | random does not match projected | random matches projected | high seed variance | control table |

**Seeds:** 5 seeds: `0, 1, 2, 3, 4`。

**Steps:** 200 full-batch update steps。

**Checkpoints:** step `0, 1, 5, 10, 25, 50, 100, 200`。

**Learning-rate grid:** initial grid $\eta\in\{0.003,0.01,0.03,0.1,0.3,1,3,10,30\}$。若全部稳定或全部发散，向外扩一档。

## 7. Primary Metric

**Definition:**

$$
R_{\eta}=
\frac{\eta_{\mathrm{crit}}(\mathrm{common\text{-}projected\ SGD})}
{\eta_{\mathrm{crit}}(\mathrm{vanilla\ SGD})}
$$

**Critical LR rule:** 在至少 4/5 seeds 中满足稳定条件的最大 LR。

**Stable condition:** 训练过程中无 NaN/Inf；final train loss < initial train loss；final eval loss 不高于 initial eval loss；任一 checkpoint loss 不超过 initial loss 的 3 倍。

**Why it decides:** 当前问题是公共投影是否提高 SGD 可用学习率；$\eta_{\mathrm{crit}}$ 直接测这个上界。

**False positive cost:** 如果 norm shrinkage 解释了提升，会误把 scaling 当成 mechanism。

**False negative cost:** 若 synthetic common 太弱，可能错过真实机制；因此记录 common energy ratio。

## 8. Secondary Metrics

- rare eval loss at each method's $\eta_{\mathrm{crit}}$。
- frequent eval loss。
- rare-token update share。
- per-token column update norm distribution。
- common gradient energy ratio $\|G_c\|_F/\|G\|_F$。
- top singular energy of $G$ and $G_r$。
- divergence step for unstable LRs。

## 9. Known Good / Known Bad / Known Confusing Cases

**Known good:** $\alpha_c=2.0$ and skewed frequency should produce visible common energy.

**Known bad:** $\alpha_c=0$ should remove the common mechanism; projected SGD should not strongly outperform vanilla.

**Known confusing:** projected SGD may increase stability but slow total loss because common signal was useful. This is insufficient, not pass.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| Data audit | common direction exists? | generated $h_i$ | $\|\mathrm{mean}(h)\|$ and common energy visible | hidden PCA table | detailed |
| Gradient audit | common gradient is loud? | step-0 $G$ | $\|G_c\|_F/\|G\|_F$ nontrivial | gradient spectrum | detailed |
| LR sweep | projected raises LR? | loss curves by LR | stable-window rule | LR stability figure | summary |
| Control audit | effect is not norm/random? | control LR table | projected beats controls | control table | summary |
| Rare guard | rare learning preserved? | rare eval loss | no >5% worsening | rare loss curve | summary |

## 11. Algorithm Specification

**Input:** seed, $d$, $V$, frequent/rare split, frequency ratio, $\alpha_c$, $\alpha_y$, $\sigma$, LR grid, steps.

**Parameters:** default $d=64$，$V=64$，frequent classes 8，rare classes 56，ratio 16:1，$\alpha_c=2.0$，$\alpha_y=0.5$，$\sigma=0.05$，steps 200，seeds 5。

**Intermediate variables:** $h_i$，$c$，$z_y$，$G$，$u$，$G_c$，$G_r$，condition-specific update matrix。

**Steps:**

1. Generate train/eval synthetic hidden-token pairs.
2. Initialize output head identically per seed and condition.
3. For each LR and condition, run 200 full-batch updates.
4. Record loss trajectory, gradient projections, update norms, and divergence.
5. Compute $\eta_{\mathrm{crit}}$ per condition.
6. Aggregate over seeds and apply pass/fail rules.

**Outputs:** LR table, loss curves, rare/frequent loss table, common-energy table, summary decision.

**Debug artifacts:** generated-data audit, gradient spectrum, per-token update norm histogram.

**Pass conditions:** projected beats vanilla and controls under the primary metric while rare loss is preserved.

**Fail conditions:** projected does not beat vanilla, or controls explain the effect.

**Failure reasons:** weak synthetic common; wrong common estimator; instability not caused by common direction; projection removes useful signal.

## 12. Success / Failure / Insufficient Evidence

**Success:** $R_{\eta}\ge3$，projected/norm-matched $\ge2$，random-projected not matching，rare eval loss no worse than vanilla by more than 5%。

**Failure:** $R_{\eta}\le1.5$，or norm/random control matches projected。

**Insufficient:** projected stable but rare loss collapses；common energy absent；LR grid cannot locate boundary；seed variance too high。

## 13. What This Cannot Claim

- 不能说明 Adam 的全部优势来自 common removal。
- 不能说明 Nesterov 的 solution-space 路径机制。
- 不能说明真实 LM 中 SGD 可用。
- 不能说明 MoE routing preservation 被解释。
- 不能说明 common direction 应该在最终 optimizer 中硬投掉。

## 14. Review Notes And Protocol Changes

待确认：

1. 默认 frequency ratio 是否用 16:1，还是需要更强的 32:1？
2. full-batch 是否作为第一轮唯一主设置，mini-batch noise 是否推迟到 follow-up？
3. stable condition 中 “checkpoint loss 不超过 initial loss 3 倍” 是否太宽或太严？
4. Nesterov 是否只放 follow-up，不进入第一轮 protocol？
