# Protocol Draft CN: A11_08 General-K Readout-Margin Dynamics

审批状态：等待用户审核。  
主 anchor：`daily_research_reports/0709/mtp_generalized_efficiency_story/anchors/11_08_general_k_readout_margin_dynamics_anchor.md`。  
实验角色：理论量验证 / metric audit，不是 MoE bridge，不是自然语言实验。

## 0. 审批快照

**Purpose:** 验证 next-K 的一阶效率机制：MTP 的优势是否由 K 覆盖到的“有信息未来位置”的中心化输出方向向量和决定。

**Anchor decision question:** 一般 K 下，读出有效语义边距的一阶速度是否等于被 K 覆盖的有信息 horizon 的向量和预测。

**Anchor physical prior tested:** 只有包含早期变量 $Z$ 的未来位置产生分支相关的一阶更新；多个有信息位置只有方向对齐时才稳定增强。

**Anchor core model term tested:**  

$$
v_z^{(K)}=\sum_{j\in\mathcal I_K}\lambda_j(u_{j,z}-\bar u_j)
$$

以及：

$$
G_K=\frac1{m^2}\sum_z\|v_z^{(K)}\|^2
$$

**Anchor falsifier:** 最小 falsifier 是“方向对齐失效”：在同样 `K=4`、同样两个 informative horizons、同样 active loss 数量下，如果 output-row geometry 预测 aligned condition 应显著大于 low/conflict condition，但 observed hidden-gradient velocity 不分开，则一般 K 向量和机制被削弱。

**Primary metric from anchor:** 观察到的一阶读出有效语义边距速度。操作化主指标采用 hidden-gradient velocity：

$$
G_K^{hidden}=\frac1m\sum_z v_z^{(K)\top}(-\nabla_{h_z}L_K)
$$

原因：A11_06 已显示 parameter finite-difference `Delta M / eta` 数值较小且不稳定；finite difference 本次保留为辅助 self-check。

**Minimal setup:** clean synthetic decision-prefix training only. 不做 all-position，不做 MoE routing。

**Basic configuration:** 4 branches, fixed max-K heads, primary `Kmax=4`, branch-collapsed initialization, seeds `971-975`, one-step diagnostics first，短曲线只作为 secondary check。

**Minimal conditions to run:** `single-informative` positive control, `aligned-two-informative`, `low/conflict-two-informative`, `shared-only` zero guard。`noisy / independent guard` 只作为可选 guard，不参与最小 falsifier。

**Pass:** output geometry audit 显示 $G^{pred}_{aligned}>G^{pred}_{low/conflict}$，且 observed $G^{hidden}_{aligned}>G^{hidden}_{low/conflict}$；`single-informative` 为正；`shared-only` 近零；local shared targets 不恶化。

**Fail:** 在 output geometry 和 leakage audit 都通过后，$G^{pred}_{aligned}$ 明显大于 $G^{pred}_{low/conflict}$，但 observed $G^{hidden}_{aligned}\le G^{hidden}_{low/conflict}$，或 observed gap 只有 predicted gap 的很小一部分；这直接削弱“next-K 效率由 informative horizons 的方向和决定”的机制。若 `shared-only` 也稳定产生正 margin，则削弱“无信息 horizon 只给公共更新”的先验。

**Insufficient:** step-0 泄漏；low/conflict target rows 没有实际形成低对齐或冲突；predicted gap 太小；finite-difference 与 hidden-gradient 分歧且无法定位；输出 head 几何过弱导致所有 predicted $G_K$ 近零。

**Cannot claim:** K 越大越好；自然语言 MTP 更好；all-position 间接迁移机制；MoE routing preservation 或 expert utility。

**Approval decision needed:** 用户确认本 protocol 的主指标、条件集合、Kmax、seeds、pass/fail 阈值后，才能开始实现和实验。

## 1. 术语解释

| 术语 | 中文含义 | 具体对象 / 计算 | 单位或公式 | 为什么重要 | 不能证明什么 |
| --- | --- | --- | --- | --- | --- |
| 早期变量 $Z$ | 前缀早期出现、未来才需要的信息 | synthetic branch id | 离散变量 | 要被写入 $h_T$ 的语义代理 | 自然语言全部语义 |
| 当前状态 $h_T$ | 决策前缀后的隐藏状态 | $h_z=h_T(Z=z)$ | 向量 | A11 检查语义写入的位置 | 所有位置状态 |
| 有信息 horizon | 某个未来位置新增 $Z$ 信息 | $Y_j=S_{j,Z}$ 且 $Z\mapsto S_{j,Z}$ 一一对应 | 未来偏移 | 决定该 horizon 是否应贡献语义更新 | 真实语料固定 horizon |
| $\mathcal I_K$ | K 覆盖到的有信息 horizon 集合 | $\{j\le K:I(Z;Y_j\mid Y_{<j})>0\}$ | 集合 | 一般 K 理论的核心对象 | 优化速度本身 |
| 中心化输出方向 | 正确 token 输出行去均值 | $u_{j,z}-\bar u_j$ | 向量 | 判断该 horizon 推 $h_T$ 的方向 | downstream utility |
| 聚合语义方向 | K 内所有有信息方向加权和 | $v_z^{(K)}=\sum_{j\in\mathcal I_K}\lambda_j(u_{j,z}-\bar u_j)$ | 向量 | 决定 predicted margin velocity | 多步收敛 |
| 读出有效语义边距 | $h_T$ 是否朝正确未来 token 输出方向移动 | $M_K(h)=m^{-1}\sum_z v_z^{(K)\top}h_z$ | scalar | 一阶效率主量 | 自然语言收益 |
| hidden-gradient velocity | loss 对 $h_T$ 的瞬时语义推动 | $G_K^{hidden}=m^{-1}\sum_z v_z^{(K)\top}(-\nabla_{h_z}L_K)$ | scalar | 本 protocol 主指标 | 参数空间样本效率 |
| finite-difference velocity | 一步更新后的边距变化 | $\Delta M_K/\eta$ | scalar / step size | 检查实际小步更新 | 若数值不稳，不能单独判定 |
| local guard | 共享近端目标是否被破坏 | shared target CE / accuracy | CE / accuracy | 排除牺牲局部学习换语义 margin | 全局 LM 质量 |

## 2. Anchor 对齐

**Decision question:** 一般 next-K 的一阶语义效率是否由 active informative horizons 的读出方向向量和决定。

**Physical prior:** 无信息 horizon 只给公共更新；有信息 horizon 给 branch-specific 更新；多个有信息 horizon 的效果由方向对齐关系决定。

**Core model term:** $v_z^{(K)}$ 和 $G_K$。

**Falsifier:** predicted $G_K$ 无法预测 observed $G_K^{hidden}$，或无信息 horizon 产生稳定 branch-specific margin。

**Claim boundary:** 本实验只验证 decision-prefix 的一阶理论量，不解释 all-position indirect transfer。

## 3. Tested Hypothesis

### 3.0 最小可证伪点

**最小研究判断：**  
不是“K 越大是否更好”，而是：

```text
在同样 K=4、同样有两个 informative horizons 的条件下，
第二个 informative horizon 的输出方向是否决定一阶语义速度。
```

因此最小对照只需要两组 K4：

```text
aligned-two-informative:
  Y3 = S_z, Y4 = T_z
  两个 horizon 的 branch code ordering 对齐

low/conflict-two-informative:
  Y3 = S_z, Y4 = T_pi(z)
  pi 被选择成让 Y4 的中心化输出方向与 Y3 低对齐或冲突
```

这两个条件的 active loss 数量相同，head 数量相同，K 相同。唯一要改变的是第二个 informative horizon 相对第一个 informative horizon 的方向关系。

**最小 falsifiable prediction：**

先计算 output-row geometry：

$$
G^{pred}_{aligned}
=\frac1{m^2}\sum_z\|a_{3,z}+a_{4,z}^{aligned}\|^2
$$

$$
G^{pred}_{low/conflict}
=\frac1{m^2}\sum_z\|a_{3,z}+a_{4,z}^{low/conflict}\|^2
$$

若：

$$
G^{pred}_{aligned}-G^{pred}_{low/conflict}
$$

足够大，则 observed hidden-gradient velocity 也必须满足：

$$
G^{hidden}_{aligned}>G^{hidden}_{low/conflict}.
$$

**可以 falsify 的结果：**

在以下前提都通过后：

1. step-0 leakage guard 通过；
2. `single-informative` 有正 hidden velocity；
3. `shared-only` 近零；
4. output geometry 确认 aligned 与 low/conflict 有明显 predicted gap；
5. local shared target guard 通过；

如果观察到：

```text
mean(G_hidden_aligned) <= mean(G_hidden_low/conflict)
```

或者：

```text
G_hidden_aligned - G_hidden_low/conflict
```

在大多数 seeds 中不为正，则判定最小机制被 falsified / strongly weakened。

**建议的“明显 predicted gap”门槛，供用户审核：**

```text
G_pred_aligned - G_pred_low/conflict >= 0.5 * G_pred_single_informative
```

若达不到这个门槛，不叫 fail，叫 insufficient：说明 target-code construction 没有制造出足够清楚的方向差异。

**H1: informative-horizon contribution.**  
若 $\mathcal I_K=\varnothing$，则 $G_K^{hidden}$ 应接近 0。

**H2: aligned addition.**  
新增有信息 horizon 的中心化输出方向若与已有 $v_z^{(K)}$ 对齐，则 $G_K^{hidden}$ 应增加，并接近 predicted $G_K$。

**H3: non-monotonic K.**  
新增 horizon 若无信息、弱对齐或冲突，则 K 增大不应被解释成无条件效率提升；observed velocity 应按方向和公式变化。

**H4: local guard.**  
语义 margin 增强不能以破坏 shared local targets 为代价。

## 4. Rival Explanations

| Rival explanation | 为什么合理 | 本 protocol 如何区分 |
| --- | --- | --- |
| loss scale 变大导致看似更快 | K 越大 active CE 项越多 | 固定 $\lambda_j$，报告 gradient norm，并以 predicted direction-specific $G_K$ 判定 |
| head 数量更多导致优势 | K1 可能没有高阶 head | 使用 fixed max-K heads，K 只改变 active losses |
| probe 假阳性 | probe-readable 不等于 readout-effective | 主指标是 output-row-facing margin，不以 probe 为主 |
| step-0 branch leakage | 初始化已含 $Z$ 会污染速度判断 | 要求 $Q(0)$ 近 chance，$M_K(0)$ 近 0，$E_Z(0)$ 近 0 |
| target code 未实际冲突 | permutation 不一定在输出几何上负对齐 | 先计算 centered cosine / predicted increment；若未形成冲突，标为 insufficient 而非 fail |

## 5. Data / Model / Objective

**Data shape:** decision-prefix synthetic branch sequence：

```text
BR_z F00 ... F{L-1} U00 U01 U02 U03 Y1 Y2 Y3 Y4 STOP
```

**Primary Kmax:** `4`。理由：K=4 已足够测试“新增第二个有信息 horizon”是否同向增强、弱对齐或冲突；暂不做更大 K sweep。

**Model:** 继承 A11_06 的 clean decision-prefix Transformer setup，固定 max-K prediction heads。

**Objective:**

$$
L_K(h_T)=\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_T),Y_j)
$$

**Scope:** decision-only。只在 $h_T$ 上计算 loss，排除 all-position indirect transfer。

## 6. Conditions, Seeds, And Checkpoints

初始建议：5 seeds `971-975`，与 A11_06 / A11_07 对齐。  
One-step eta: primary `3e-4`，辅助检查 `1e-4` 和 `1e-3`。  
短曲线：仅在 one-step 主结果可解释后跑 `0-2000` steps，eval interval `100`。

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| shared-only | 无信息 horizon 近零 | $\mathcal I_K=\varnothing$ | zero guard，不是主 falsifier | required guard | $G_K^{hidden}$ 近零 | 稳定正 margin | 泄漏或实现异常 | zero_guard.csv |
| single-informative | 恢复 K=2/K=3 定理 | one informative $a_{j,z}$ | positive control | required guard | positive and interpretable | 不为正 | predicted signal 过小 | single_info.csv |
| aligned-two-informative | 同向相加增强 | $a_{3,z}+a_{4,z}$ | 最小机制正例 | primary | observed high as predicted | 不高于 low/conflict | code alignment 未实现 | aligned.csv |
| low/conflict-two-informative | 方向依赖 / 非单调 K | small or negative increment | 最小机制反例 | primary | observed lower than aligned | matches or exceeds aligned despite predicted gap | 未形成低对齐 / 冲突 | low_conflict.csv |
| noisy / independent guard | 无用辅助目标 | target independent of $Z$ | 排除 generic auxiliary loss | optional secondary | no stable semantic margin | stable positive margin | finite noise too high | noisy_guard.csv |
| local guard | 不能破坏局部目标 | shared CE / accuracy | 排除 tradeoff | secondary | CE no material increase | local CE degrades | target too easy to see | local_guard.csv |

## 7. Primary Metric

主指标是 observed hidden-gradient velocity 与 predicted $G_K$ 的一致性。

**Predicted quantity:**

$$
G_K^{pred}=\frac1{m^2}\sum_z\left\|\sum_{j\in\mathcal I_K}\lambda_j(u_{j,z}-\bar u_j)\right\|^2
$$

**Observed quantity:**

$$
G_K^{hidden}=\frac1m\sum_z v_z^{(K)\top}(-\nabla_{h_z}L_K)
$$

**最小 falsification threshold for review:**

1. geometry precondition: $G^{pred}_{aligned}-G^{pred}_{low/conflict}\ge0.5G^{pred}_{single}$；
2. falsifier: under that precondition, if $\operatorname{mean}(G^{hidden}_{aligned})\le\operatorname{mean}(G^{hidden}_{low/conflict})$，则最小机制 fail；
3. strong weakening: if observed aligned-minus-low/conflict gap is positive in fewer than 4/5 seeds，或 observed gap is less than `25%` of predicted gap，标记为 strongly weakened even if mean is weakly positive；
4. zero guard: shared-only observed velocity should be no more than `10%` of single-informative positive-control scale；
5. full correlation across all cells is optional audit, not the minimal falsifier。

这些阈值需要用户审核。若你认为太严格，可以改成 order-only pass。

## 8. Secondary Metrics

| Metric | Meaning | Why secondary |
| --- | --- | --- |
| $\Delta M_K/\eta$ | 小步更新后的 margin 变化 | A11_06 显示 parameter finite-difference 可能不稳定 |
| $\Delta E_Z/\eta^2$ | branch hidden separation 二阶增长 | 可说明 probe / route 可分性，但不是 output-facing 主量 |
| native informative-horizon accuracy | 模型自身是否预测含 $Z$ token | 多步后解释辅助，不是一阶主量 |
| $Q(t)$ | guarded recovery | 短曲线辅助，不作为 direct 一阶证据 |
| local CE / accuracy | shared targets 是否被破坏 | 防止 tradeoff |
| gradient norm | loss scale 守卫 | 排除 K 大只是 norm 大 |

## 9. Known Good / Known Bad / Known Confusing Cases

**Known good:** single-informative K3 应复现 A11_06：K3 positive，K1/K2 near zero。

**Known bad:** shared-only 或 K 不覆盖任何 informative horizon，应 near zero。

**Known confusing 1:** conflicting construction 可能在实际初始化输出行上并不冲突。处理：先报告 centered cosine 和 predicted increment；若没有负对齐，不解释为 theory fail。

**Known confusing 2:** finite-difference $\Delta M_K/\eta$ 可能与 hidden-gradient velocity 不一致。处理：以 hidden-gradient velocity 为主，finite-difference 进入 detailed failure analysis。

**Known confusing 3:** noisy target 有 finite-sample 噪声。处理：它只作为 guard，不作为核心 theorem cell。

## 10. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| data audit | horizon 是否真的 informative / uninformative | generated manifest | target-Z relation matches regime | data_examples.json | detailed |
| output geometry audit | aligned / conflicting 是否真实成立 | output rows | predicted increment has intended sign/order | output_geometry.csv | summary table |
| leakage audit | step 0 是否已含 Z | $Q(0),M(0),E(0),native$ | near chance / near zero | leakage_audit.csv | summary |
| one-step gradient | theory 主测试 | gradients at $h_T$ | observed follows predicted | one_step_metrics.csv | summary |
| finite-diff check | 小步实现是否一致 | cloned step | no gross contradiction | finite_diff.csv | detailed |
| short curve | 一阶机制是否进入早期曲线 | 0-2000 step runs | only after one-step interpretable | q_margin_curves.png | summary if useful |
| local guard | shared targets 是否被牺牲 | CE / accuracy | no material regression | local_guard.csv | summary |

## 11. Algorithm Specification

**input:** regime config, branch count, max K, seed list, fixed architecture, target-code mapping.

**parameters:** `num_branches=4`, `Kmax=4`, seeds `971-975`, primary eta `3e-4`, auxiliary eta `1e-4/1e-3`, short-curve steps `2000` only if approved by one-step result.

**intermediate variables:** $u_{j,z}$, $\bar u_j$, $a_{j,z}$, $v_z^{(K)}$, $G_K^{pred}$, $G_K^{hidden}$, $\Delta M_K/\eta$, $\Delta E_Z/\eta^2$。

**steps:**

1. build data regimes and target-code mapping;
2. initialize fixed max-K-head model with branch-collapsed initialization;
3. run leakage audit at step 0;
4. compute output-row geometry and predicted $G_K$;
5. compute hidden gradients and observed $G_K^{hidden}$;
6. clone model and run one small update for finite-difference check;
7. only if stages 1-6 are interpretable, run short decision-only curves;
8. write `summary.md` and `detailed.md` with source tables and figures.

**outputs:** tables, figures, run config, summary, detailed.

**debug artifacts:** data examples, output geometry table, per-seed gradient tables, finite-difference stability table.

**pass conditions:** see section 12.

**failure reasons:** theory wrong; target-code construction failed; output geometry did not realize intended alignment; implementation gradient mismatch; leakage; loss-scale confound.

## 12. Success / Failure / Insufficient Evidence

**Success:**  
最小成功是 aligned-two-informative 与 low/conflict-two-informative 按 predicted direction gap 分开：aligned observed velocity 高于 low/conflict；single-informative 为正；shared-only 近零；local guard 和 leakage guard 通过。

**Failure:**  
最小 failure 是：在 leakage、geometry、single-positive、shared-zero 和 local guard 都通过后，predicted 显示 aligned 应显著高于 low/conflict，但 observed hidden-gradient velocity 没有分开：

```text
mean(G_hidden_aligned) <= mean(G_hidden_low/conflict)
```

或大多数 seeds 不支持 aligned > low/conflict。  
这会 falsify / strongly weaken “一般 K 效率由 informative horizons 的方向和决定”这个最小机制。

另一类 failure 是 shared-only 稳定产生正 readout-effective margin；这会 falsify / strongly weaken “无信息 horizon 只产生公共更新”的先验。

**Insufficient evidence:**  
alignment construction does not produce a large enough predicted gap; all predicted signals are too small; finite-difference and hidden-gradient disagree without localization; local guard fails; step-0 leakage invalidates speed metric.

## 13. What This Cannot Claim

This experiment cannot claim:

```text
K larger is always better.
MTP is better than NTP in natural language.
all-position indirect transfer is explained.
MoE routing preservation or expert utility follows.
Q alone proves direct supervision.
```

Allowed claim if supported:

```text
In controlled decision-prefix next-K training, first-order MTP semantic efficiency is governed by the vector sum of readout-effective directions from informative future horizons. Larger K helps only when added informative horizons contribute aligned branch-relevant directions.
```

## 14. Review Notes And Protocol Changes

需要用户审核的点：

1. 是否接受 hidden-gradient velocity 作为主指标，finite-difference 作为辅助指标。
2. 是否接受 `Kmax=4` 作为第一轮 general-K，而不是直接扫更大 K。
3. 是否接受 5 seeds `971-975` 和 eta `3e-4` primary。
4. 是否接受最小 falsifier：在 geometry predicted gap 足够大时，aligned observed velocity 必须高于 low/conflict。
5. 是否接受 geometry precondition：$G^{pred}_{aligned}-G^{pred}_{low/conflict}\ge0.5G^{pred}_{single}$。
6. 是否接受 strong weakening rule：若 aligned > low/conflict 少于 4/5 seeds，或 observed gap 小于 predicted gap 的 `25%`，则不算支持。
7. 是否保留 `noisy / independent guard`，还是先只做 shared-only、single、aligned-two-informative、low/conflict-two-informative。
8. 是否同意短曲线只在 one-step 诊断可解释后再跑。

审批意见填写：

```text
Approved / Revise before run:
Required edits:
Optional edits:
Can start implementation after English canonical protocol is written: yes / no
```
