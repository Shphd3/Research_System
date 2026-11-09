# Summary: A11_05 Semantic Efficiency Bridge

Primary anchor: `problem_anchors/11_informative_future_branch_mechanism/11_05_semantic_efficiency_bridge_anchor.md`
Protocol: `protocol.md`

## Result Snapshot

Verdict: **qualified support for the direct-supervision mechanism.** In the clean $\tau=3$ all-position setting, adding the decision-prefix horizon-3 loss to K=2 makes recovery perfect in the clean identical-branch setting, and masking the same direct term from K=3 weakens recovery. This supports the claim that direct decision-prefix supervision explains a measurable part of K=3 semantic efficiency. It does **not** show that direct supervision is the only path, because all-position indirect transfer remains strong.

What we established: direct $h_T\to S_Z$ supervision is sufficient to turn K=2 into a K=3-like condition on guarded semantic recovery, without hurting active local $Y_1/Y_2$ learning.

What the experiment shows: under identical-branch initialization, K2 plus decision-L3 reaches $Q\ge0.9$ in 5/5 seeds with early AUC 0.969, while K2 reaches 3/5 seeds with early AUC 0.771. Full K3 reaches 5/5 seeds with early AUC 0.965, while K3 with decision-L3 masked reaches 3/5 seeds with early AUC 0.817 and final $Q=0.70$.

What we do next: treat direct supervision as a supported mechanism component, but do not claim an unconditional all-position efficiency theorem. The next decision should either tighten the optimization bridge or move to a harder setup where random initialization and indirect transfer do not saturate $Q$ at step 0.

## Purpose

This run tested whether K=3's clean $\tau=3$ advantage comes from direct horizon-3 supervision on the current decision-prefix hidden state $h_T$, rather than from all-position indirect transfer, generic auxiliary loss, or a local next-token tradeoff.

## Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| clean $\tau=3$ | the first future token that needs $Z$ is three steps ahead | $Y_1=A$, $Y_2=C$, $Y_3=S_Z$ | token offset | isolates first informative horizon | natural-language horizon structure |
| direct decision-prefix supervision | the current state is directly trained to predict the informative future token | $\lambda_3\operatorname{CE}(q_3(\cdot\mid h_T),S_Z)$ | cross entropy | proposed efficiency mechanism | all MTP usefulness |
| indirect transfer | $h_T$ becomes branch-readable through other all-position losses | shared-parameter updates excluding decision-prefix $L_3$ | training effect | rival explanation | direct causality |
| $A(t)$ | informative-suffix decoder accuracy | linear decoder from frozen $h_T$ to branch label $Z$ | accuracy | checks whether $h_T$ contains the variable needed by $S_Z$ | native model prediction |
| $P(t)$ | independent probe accuracy | separate linear probe from frozen $h_T$ to $Z$ | accuracy | protects against one decoder artifact | causal mechanism |
| $S(t)$ | branch-swap consistency | swap the branch token, recompute $h_T$, decode swapped branch | accuracy | checks whether recovery follows branch identity | natural semantics |
| $Q(t)$ | guarded semantic recovery | minimum of three recovery checks | $Q(t)=\min\{A(t),P(t),S(t)\}$ | primary semantic-recovery metric | exact training path |
| $T_{0.9}$ | reliable time-to-threshold | first step where $Q(t)\ge0.9$ for 3 consecutive evals | steps | primary learning-efficiency metric | final capability alone |
| early AUC | early learning area | normalized area under $Q(t)$ over steps 0-3000 | score area | speed and stability before convergence | gradient cause |
| full AUC | whole-run recovery area | normalized area under $Q(t)$ over steps 0-15000 | score area | overall stability | direct causality |
| local guard | local next-token learning check | $Y_1/Y_2$ accuracy and CE at $h_T$ | accuracy / CE | rules out a local-learning tradeoff | full LM quality |
| native horizon-3 accuracy | direct head prediction of $S_Z$ | $\Pr[\arg\max q_3(\cdot\mid h_T)=S_Z]$ | accuracy | distinguishes direct prediction from probe-readable recovery | whether $h_T$ is causally useful elsewhere |
| gradient diagnostics | whether horizon-3 gradients align with later recovery | cosine, norm ratio, future $\Delta Q$ correlations | diagnostic scores | optional optimization audit | standalone causal proof |

## Exact Setup

Research question: in clean $\tau=3$ all-position training, does direct decision-prefix horizon-3 supervision improve semantic recovery beyond indirect all-position transfer?

Data / model / objective: one-layer Transformer, all-position LM-style next-K loss, 4 branches, 5 seeds `971-975`, 15000 steps, eval every 250 steps.

Conditions:

| Condition | Plain meaning | Loss structure |
| --- | --- | --- |
| K1 | next-token baseline | all-position $Y_1$ |
| K2 | non-covering MTP baseline | all-position $Y_1,Y_2$ |
| K3 full | direct plus indirect K=3 | all-position $Y_1,Y_2,Y_3$ |
| K3 no decision L3 | indirect-only K=3 control | all-position K=3 but mask $\operatorname{CE}(q_3(\cdot\mid h_T),S_Z)$ |
| K2 plus decision L3 | isolated direct-supervision control | all-position K=2 plus only $\operatorname{CE}(q_3(\cdot\mid h_T),S_Z)$ |

Known limitation: random initialization has $Q=1.0$ at step 0 for all conditions, so it cannot decide speed. It is treated as an initialization-leakage boundary. The primary speed judgment uses identical-branch initialization, where all conditions start at $Q=0.25$.

Paths:

- Raw result: `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a11_05_semantic_efficiency_bridge/a11_05_semantic_efficiency_bridge_4gpu_20260708_100650`
- Curated tables: `tables/`
- Curated figures: `figures/`
- ACP job: `pt-u0od5jmz`

## Primary Metric

The primary metric is $T_{0.9}$:

$$
T_{0.9}=\min\{t_i:Q(t_i)\ge0.9,\ Q(t_{i+1})\ge0.9,\ Q(t_{i+2})\ge0.9\}.
$$

It decides whether a condition learns the long-horizon variable earlier and reliably, not merely whether it eventually reaches a high final score. Because random initialization is saturated at step 0, $T_{0.9}$ is meaningful mainly under identical-branch initialization.

## Result

### Identical-Branch Initialization

This is the clean learning-efficiency comparison because all conditions start from chance-level $Q=0.25$.

| Condition | Reach rate | Mean $T_{0.9}$ reached-only | Early AUC | Full AUC | Final $Q$ | Native H3 acc | Final $Y_1/Y_2$ acc |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| K1 | 0.60 | 250 | 0.838 | 0.834 | 0.85 | NA | 1.00 / 0.00 |
| K2 | 0.60 | 333 | 0.771 | 0.731 | 0.85 | NA | 1.00 / 1.00 |
| K3 full | 1.00 | 300 | 0.965 | 0.993 | 1.00 | 1.00 | 1.00 / 1.00 |
| K3 no decision L3 | 0.60 | 833 | 0.817 | 0.750 | 0.70 | 0.00 | 1.00 / 1.00 |
| K2 plus decision L3 | 1.00 | 250 | 0.969 | 0.994 | 1.00 | 1.00 | 1.00 / 1.00 |

Interpretation:

- Adding direct decision-prefix L3 to K2 improves reach rate from 0.60 to 1.00, early AUC from 0.771 to 0.969, full AUC from 0.731 to 0.994, and final $Q$ from 0.85 to 1.00.
- Masking decision-prefix L3 from K3 weakens K3: reach rate drops from 1.00 to 0.60, mean threshold time worsens from 300 to 833, full AUC drops from 0.993 to 0.750, and final $Q$ drops from 1.00 to 0.70.
- Local $Y_1/Y_2$ learning is preserved in all active local-target conditions, so the direct-supervision gain is not explained by sacrificing local next-token learning.

### Random Initialization Boundary

Random initialization is not a clean speed test because $Q=1.0$ at step 0 for every condition. It still shows a useful boundary: K3 no decision L3 can have high final $Q=0.95$ while native horizon-3 accuracy remains 0.00. Thus all-position training can make $h_T$ probe-readable without directly training the horizon-3 head at $h_T$.

## Key Figures

### Figure: Identical-Branch Q Curves

![Identical-branch Q curves](figures/q_curves_identical.png)

What this tests: whether direct decision-prefix L3 changes the learning trajectory when all conditions start at chance.

Metric shown: $Q(t)=\min\{A(t),P(t),S(t)\}$.

Data source: `tables/curve_metrics.csv`, averaged over 5 seeds under identical-branch initialization.

How to read: higher curves mean more reliable branch-variable recovery from $h_T$; the dashed line is $Q=0.9$.

Observed result: K3 full and K2 plus decision L3 rapidly rise to 1.0 and stay there. K1, K2, and K3 no decision L3 recover intermittently and remain less stable.

Allowed claim: direct decision-prefix L3 explains a measurable part of the efficiency advantage.

What this does not prove: natural-language benefit, universal K=3 superiority, or a general gradient theorem.

### Figure: Guarded Recovery Versus Native Horizon-3 Prediction

![Final Q versus native horizon-3 accuracy](figures/final_q_vs_native_h3.png)

What this tests: whether probe-readable $Z$ recovery is the same as directly predicting $S_Z$ from $h_T$.

Observed result: K3 full and K2 plus decision L3 have both final $Q=1.0$ and native horizon-3 accuracy 1.0. K3 no decision L3 can retain nontrivial or high $Q$ but native horizon-3 accuracy stays 0.0.

Allowed claim: direct supervision is what makes the decision-prefix horizon-3 head predict $S_Z$; indirect transfer can still make $h_T$ branch-readable.

### Figure: Local Guard

![Local guard final loss](figures/local_guard_final_loss.png)

What this tests: whether the direct-supervision gain is a local next-token tradeoff.

Observed result: K2, K3 full, K3 no decision L3, and K2 plus decision L3 all keep active $Y_1/Y_2$ final accuracy at 1.0 with near-zero CE. K1 does not train $Y_2$, so its high $Y_2$ loss is expected and not a failure of the local guard.

Allowed claim: the observed direct-supervision gain does not come from sacrificing active local targets in this controlled setup.

## Gradient Diagnostics

The run logs horizon-gradient diagnostics, but they remain secondary. In identical-branch initialization, K2 plus decision L3 has supportive horizon-3 gradient-usefulness flags across shared groups, and K3 full has some supportive signals. However random initialization is saturated at step 0, and diagnostic correlations cannot establish causality. Therefore the optimization-level claim remains: **suggestive but not proved**.

## Claim Boundary

Can claim:

- In clean $\tau=3$ all-position training, direct decision-prefix horizon-3 supervision is a supported mechanism component for faster and more stable $Z$ recovery.
- K2 plus decision L3 essentially matches full K3 on guarded recovery in the clean identical-branch setup.
- Removing decision-prefix L3 weakens full K3 under identical-branch initialization.
- Active local $Y_1/Y_2$ learning is not sacrificed.

Cannot claim:

- all-position K1/K2 cannot learn $Z$;
- direct supervision is the only recovery path;
- random-init speed results are meaningful, because $Q$ starts saturated;
- gradient diagnostics prove an unconditional optimization mechanism;
- MTP is generally better in natural language or MoE routing.

## Next Decision

Do not broaden to K>3 yet. The next decision should be whether to tighten the optimization-efficiency bridge under a setup with no step-0 random-init leakage, or to move to a harder all-position construction where indirect transfer is present but not already near-saturating.
