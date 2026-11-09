# Summary: A06_03_01_E01 Trainable Expert Utility Binding

Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_03_utility_binding_and_sparse_discovery/06_03_utility_binding_and_sparse_discovery_anchor.md`

Protocol: `protocol.md`

## Result Snapshot

**Verdict:** Correct route-conditioned exposure creates held-out task-specific expert utility on the controlled context-defined LM task. This effect does not require representation drift and survives joint representation training. However, a larger counterfactual utility gap does not create a larger weighted-top-1 router gradient; the preregistered utility-to-pressure hypothesis is rejected.

**What we established:** With frozen representation and identical expert initialization, correct exposure produces positive held-out utility gap in 128/128 task-seed cells. The paired correct-minus-balanced-shuffle median is 8.892 nats per task token, with seed-clustered 95% CI \([8.694,9.142]\).

**What the experiment shows:** Route identity can create expert function when it induces stable task-conditional update distributions. Route purity alone cannot show this: native route NMI remains 1.0 in both correct and shuffled conditions, while the shuffled experts remain functionally interchangeable. The learned utility gap also does not monotonically calibrate raw weighted-top-1 margin pressure.

**What we do next:** A06_03_01_E02 should release the router after specialist or generalist exposure and test task-preserving route/utility co-stability. It must track utility, route identity, and task loss jointly rather than using raw pressure magnitude as a utility proxy.

## Purpose

A06_02_04_E04 used fixed function-matched experts and therefore assumed expert utility. A06_03_01_E01 removes that assumption and asks whether a supplied route partition can make trainable experts acquire different functions on a sequence-level instruction-conditioned next-token task.

## Terminology / Definitions

| Term | Plain meaning | Computation | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- |
| Context-defined task | The sequence-start instruction specifies a modular token transformation used at later positions | task \(f\in\{0,1,2,3\}\) | operational long-range conditional variable | natural-language semantics |
| Correct exposure | Task \(f\) always updates expert \(f\) | fixed oracle assignment during exposure | creates stable conditional updates | label-free routing |
| Balanced shuffle | Every expert receives equal updates from every task | cyclic task-expert permutations | deletes stable identity while matching load | every real-data confound |
| Counterfactual utility gap | Assigned-expert loss advantage over the best competitor on held-out task positions | \(G_f^{cf}=\min_{b\ne f}(L_{f,b}^{cf}-L_{f,f}^{cf})\) | primary functional-binding metric | long-run routing stability |
| Native route | Router-selected expert without forced counterfactual replacement | weighted top-1 forward path | checks deployable-path behavior in the bridge | real-LLM transfer |
| Router pressure | One-step margin movement predicted by the task-loss router gradient | \(-\langle g_f-g_b,\mu_f\rangle\) | tests utility-to-gate transmission | long-run convergence |

## Exact Setup

- Four equally frequent instructions. Instruction \(f\) maps content \(c\) to output \((c+f)\bmod4\).
- Each sequence has one instruction token and sixteen content/output pairs: 33 tokens and 32 supervised next-token positions.
- Per seed: 32 train and 32 held-out sequences with disjoint content orders.
- One causal attention layer, residual plus LayerNorm, no learned positional embedding, four identically initialized trainable MLP experts, fixed readout, and weighted top-1 routing.
- A fixed instruction-state broadcast is the known-good context-visibility control. It is not a proposed gate.
- Exposure uses full-sequence LM loss for 200 steps and 32 seeds.
- Primary comparison: correct versus balanced-shuffled exposure with representation frozen and only experts trainable.
- Transfer comparison: the same two exposures with experts and representation co-trained.
- Formal run: `a06_38_full_4gpu_20260710_02`, ACP job `pt-oivsn732`, four H100 GPUs, succeeded.

## Primary Evidence

| Quantity | Correct expert-only | Balanced shuffle | Decision |
| --- | ---: | ---: | --- |
| Positive held-out gap cells | 128/128 = 100% | 34/128 = 26.56% | correct exposure passes |
| Median held-out \(G_f^{cf}\) | 8.895 | -0.004 | functional separation |
| Paired correct-minus-shuffle median | 8.892 | -- | 95% CI \([8.694,9.142]\) |
| Forced assigned-expert task loss | 0.0023 | 0.0844 | correct specialist solves its task |
| Native task loss | 0.842 | 1.808 | specialist routing has lower native loss |
| Native route NMI | 1.000 | 1.000 | route purity alone is non-decisive |
| Persistent paired binding time | step 10 | -- | controlled update-efficiency result |

Correct joint exposure also transfers: its final median utility gap is 9.530, versus -0.034 for shuffled joint exposure. Native route NMI stays 1.0 in both, while mean p05 margin remains positive at 0.309 and 0.235 respectively.

## Central Figures

### Held-Out Utility-Gap Trajectory

![Held-out utility-gap trajectory](figures/utility_gap_trajectory.png)

- **Question:** Does stable task-expert identity create held-out expert function, and when?
- **How to read:** The y-axis is assigned-expert loss advantage over the best competitor. Positive is required; correct exposure must also exceed shuffle.
- **Observed:** Correct expert-only and correct joint conditions become persistently separated from controls by step 10 and reach gaps of 8.895 and 9.530. Shuffled conditions end near zero.
- **Take-home:** Conditional exposure, not update count alone, creates expert function.
- **Does not prove:** Learned routing can discover or preserve the identity without oracle exposure.

### Final Counterfactual Loss Matrices

![Counterfactual expert loss matrices](figures/counterfactual_loss_matrices.png)

- **Question:** Are correct experts task-specific or merely equally good generalists?
- **How to read:** Rows are tasks and columns are forced experts. A low diagonal with high off-diagonal values means specialist binding.
- **Observed:** Correct exposure produces approximately 0.002 diagonal loss and 9.4--9.8 off-diagonal loss. Balanced shuffle produces nearly flat 0.082--0.087 losses.
- **Take-home:** Correct exposure creates specialists; shuffle creates nearly interchangeable generalists.
- **Does not prove:** Specialists are preferable on natural text or under a compute budget.

### Utility And Router Pressure

![Utility and router pressure](figures/utility_router_pressure.png)

- **Question:** Does a larger counterfactual utility gap imply stronger task-aligned weighted-top-1 pressure?
- **How to read:** X is held-out utility gap; Y is one-step assigned-boundary pressure. Both conditions have positive pressure, but larger Y means stronger raw reinforcement.
- **Observed:** Correct specialists have median pressure 121.94; shuffled generalists have 146.99. The paired difference is -23.44 with 95% CI \([-26.82,-20.98]\); correct exceeds shuffle in only 1/128 cells.
- **Take-home:** Utility formation and raw router-gradient magnitude are different objects. H3 is rejected.
- **Does not prove:** Correct specialists will be unstable after router unfreezing; both conditions have positive absolute pressure.

## Mechanism Update

Counterfactual utility compares expert functions:

\[
G_f^{cf}
=
\min_{b\ne f}
\left[L_{f,b}^{cf}-L_{f,f}^{cf}\right].
\]

The tested weighted-top-1 update instead uses the selected expert benefit:

\[
\Delta w_j
=
\frac{\eta}{\tau}
p_r(\mathbf 1[j=r]-p_j)B_rh,
\qquad
B_r=-\langle\nabla_{\hat y}\ell,E_r(h)\rangle.
\]

\(B_r\) does not compare the selected expert against each competitor's function. Therefore a large \(G_f^{cf}\) need not produce a larger raw margin update. The larger pressure in the shuffled condition is consistent with its larger remaining native task loss, but this experiment does not isolate the complete mediation through \(B_r\).

## Hypothesis Adjudication

| Hypothesis | Verdict | Evidence |
| --- | --- | --- |
| H1 correct exposure creates held-out functional binding | supported | 128/128 positive; paired median 8.892; CI lower 8.694 |
| H2 representation drift is necessary | rejected | expert-only non-expert state change is exactly 0 and H1 still passes |
| H3 larger utility gap creates stronger router pressure | rejected | correct > shuffle in 1/128; paired median pressure difference -23.44 |
| H4 route purity alone is insufficient | supported | both conditions route NMI 1.0, but only correct exposure has strong positive utility gap |

## Validity And Invalid Run

Run 02 passes all preregistered guards: 32 seeds; zero train/test overlap; zero initial expert difference; minimum initial route NMI numerically 1; zero non-expert change in expert-only conditions; zero per-expert count spread; zero shuffled task-expert pair-count spread; and 99.97% forced assigned-task loss reduction.

Run 01 (`a06_38_full_4gpu_20260710_01`, job `pt-hcom4dn8`) is not evidence. It failed only the supplied-partition guard because minimum initial native route NMI was 0.9198. The instruction-state visibility control was added before run 02; no primary metric, threshold, condition, optimizer, or seed count changed.

## Claim Boundary

**Supported:** Correct route-conditioned exposure can create held-out task-specific trainable expert function on this controlled context-defined LM task; the effect does not require representation drift and survives joint representation training; route purity and utility are distinct; counterfactual utility gap does not monotonically calibrate raw weighted-top-1 pressure.

**Not supported:** Natural-language semantic experts, label-free task discovery, long-context scaling, real downstream benefit, sparse-compute efficiency, or a deployable gate.

## Next Decision

Use a two-stage A06_03_01_E02 handoff on the same task: initialize from specialist or generalist expert checkpoints with the same correct router, release router updates, and test whether route identity, counterfactual utility, and native task loss remain jointly stable. Do not use raw pressure magnitude as the primary utility proxy.
