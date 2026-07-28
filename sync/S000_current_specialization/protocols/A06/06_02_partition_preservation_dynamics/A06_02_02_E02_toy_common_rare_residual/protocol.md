# Protocol: A06_02_02_E02_toy_common_rare_residual

## 0. Approval Snapshot

Approval status: user requested protocol writing and execution in the current turn.

Purpose: Run a synthetic mechanism audit for A06_02_02_E02.a--A06_02_02_E02.g before any real
DCLM or router-method claim.

Primary anchor:
`Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/subanchors/06_02_02_common_background_preservation_controls_anchor.md`

Anchor decision question: Does common-removed differential expert proxy improve
rare-margin initialization and preservation more than raw principal proxy,
hidden-centering, or load-only controls on synthetic data?

Experiment role: root-cause audit plus method-readiness gate.

Primary metrics from anchor:

- A06_02_02_E02.a--A06_02_02_E02.d: rare margin at step 0.
- A06_02_02_E02.e--A06_02_02_E02.g: rare margin at step 10 and sign-flip rate.

Minimal setup: synthetic hidden states with one common direction, four
orthogonal rare directions, four experts, and expert gain matrices whose raw
principal direction is intentionally common-dominated.

Conditions to run:

- A06_02_02_E02.a: vanilla random, row-normalized random, hidden-centered input, raw
  principal proxy, residual principal proxy, differential residual proxy.
- A06_02_02_E02.b: oracle common, mean common, top-PC common, perturbed common.
- A06_02_02_E02.c: raw principal overlap and induced margin audit.
- A06_02_02_E02.d: raw versus residual versus differential proxy initialization.
- A06_02_02_E02.e: early common recapture with ordinary input, residual input, residual
  row projection, and symmetric residual routing.
- A06_02_02_E02.f: synthetic route-function binding.
- A06_02_02_E02.g: ordinary update, smaller common-step update, smaller common-step plus
  larger rare-step update, zero-common-step variants, residual-input variants,
  row-projected variants, and rare-large without common control.

Pass: differential residual proxy improves rare margin beyond raw and
hidden-centering controls; residual input or row projection reduces sign flips;
common-small / rare-large update improves rare margin without synthetic loss
regression.

Fail: all gains reduce to load balance, projector choice flips the result, rare
margin does not improve, or synthetic loss worsens materially.

Insufficient: random controls match the proposed proxy, or common projector
estimation fails to recover the synthetic common direction.

Cannot claim: real DCLM transfer, semantic feature identity, deployed router
quality, or full expert utility.

Approval decision: execute synthetic run only.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Common direction | Shared strong direction | Synthetic vector $c$ | Unit vector | Tests common dominance | Real common semantics |
| Rare direction | Group-specific direction | Synthetic vectors $r_g$ | Unit vectors | Defines target route | Natural-language rare feature |
| Rare margin | Target expert score minus competitor | $z_{i,y_i}-\max_{e\ne y_i}z_{i,e}$ | Logit difference | Primary routing safety metric | Expert utility |
| Sign flip | Margin crosses boundary | Positive step-0 margin becomes non-positive | Fraction | Preservation metric | Cause of failure alone |
| Synthetic loss | Cross-entropy on synthetic expert labels | CE(logits, labels) | Nats | Loss guard | LM loss |

## 2. Data / Model / Algorithm / Objective

Data construction: Sample hidden states $h_i=\alpha c+\beta r_{y_i}+\epsilon_i$
with $E=4$ experts, $G=4$ rare groups, and balanced synthetic labels.

Expert gain matrix:

$$
M_e=g_c cc^\top + g_r r_er_e^\top + \xi_e.
$$

Raw principal proxy:

$$
u_e^{raw}=\mathrm{TopEig}(M_e).
$$

Residual principal proxy:

$$
u_e^{res}=\mathrm{TopEig}(P_RM_eP_R).
$$

Differential residual proxy:

$$
u_e^{diff}=\mathrm{TopEig}^+(P_R(M_e-\bar M)P_R).
$$

The objective is not to train a full model. The run audits routing geometry,
synthetic preservation under controlled common recapture, and differential
step-size feasibility.

## 3. Conditions, Seeds, And Checkpoints

Seeds: 0--7.

Synthetic checkpoints: step 0, step 5, step 10.

| Item | Anchor clause tested | Rival explanation | Why needed | Primary evidence | Pass | Fail | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A06_02_02_E02.a | load vs specialization | load-only gain | Separates balance from rare margin | rare margin step 0 | diff proxy wins | load-only wins | `a06_26a_variant_metrics.csv` |
| A06_02_02_E02.b | projector robustness | projector artifact | Tests common estimator sensitivity | rare margin by projector | conclusion stable | conclusion flips | `a06_26b_projector_metrics.csv` |
| A06_02_02_E02.c | raw common dominance | raw proxy already functional | Audits MPI-style proxy | common overlap | raw high common overlap | raw low overlap and high margin | `a06_26c_raw_proxy_metrics.csv` |
| A06_02_02_E02.d | better initialization | hidden-centering enough | Tests proxy target | rare margin step 0 | diff beats controls | controls match | `a06_26d_init_metrics.csv` |
| A06_02_02_E02.e | early preservation | initialization enough | Tests common recapture | sign flip and margin step 10 | residual routing preserves | ordinary matches | `a06_26e_preservation_metrics.csv` |
| A06_02_02_E02.f | functional value | pure route purity | Tests utility binding | selected utility | preserved routes bind | no utility gain | `a06_26f_functional_metrics.csv` |
| A06_02_02_E02.g | differential step size | rare larger LR unstable | Tests two user-proposed schemes | margin, sign flip, loss | common-small rare-large passes | loss/sign flips worsen | `a06_26g_lr_metrics.csv` |

## 4. Primary Metric

Rare margin decides A06_02_02_E02.a--A06_02_02_E02.d because it directly measures whether the
target rare group is inside the intended expert basin. Step-10 rare margin and
sign-flip rate decide A06_02_02_E02.e--A06_02_02_E02.g because the mainline bottleneck is
preservation, not step-0 route purity alone.

## 5. Secondary Metrics

Proxy-route NMI, selected-route accuracy, max load, effective experts, empty
expert count, common bias spread, common overlap, synthetic loss, and selected
expert utility.

## 6. Known Good / Known Bad / Known Confusing Cases

Known good: oracle rare proxy rows should recover high rare margin and high NMI.

Known bad: raw principal proxy should be common-dominated when $g_c>g_r$.

Known confusing: hidden-centering may improve max load without improving rare
margin.

## 7. Algorithm Specification

input: synthetic dimensions, seeds, common strength, rare strength, common gain,
rare gain, common recapture strength, and differential step-size coefficients.

parameters: $d=64$, experts $E=4$, samples per group $2048$, seeds 0--7,
checkpoints 0/5/10.

steps:

1. Build orthonormal common and rare directions.
2. Sample hidden states and labels.
3. Build expert gain matrices.
4. Estimate common projectors.
5. Build routing variants.
6. Compute step-0 metrics.
7. Simulate early common recapture.
8. Compute preservation metrics.
9. Simulate differential step-size variants.
10. Write tables and figures.

outputs: CSV tables, PNG figures, `summary.json`, and log metadata.

## 8. Success / Failure / Insufficient Evidence

Success: A06_02_02_E02.a--A06_02_02_E02.g pass their primary metrics and guards.

Failure: rare margin does not improve or preservation fails under residual
controls.

Insufficient: projector robustness fails or random controls match the proposed
proxy.

## 9. What This Cannot Claim

This synthetic run cannot claim real DCLM transfer, language-model loss
quality, semantic experts, or that a deployable router has been validated.

## 10. Artifact Map

code workspace:
`Projects/from-attention-to-search/main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_02_E02_toy_common_rare_residual`

runner:
`scripts/run_synthetic_common_removed_differential_proxy.py`

tables:
`tables/`

figures:
`figures/`

logs:
`logs/`
