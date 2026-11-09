---
experiment_id: A15_06_E06_2b_10b_router_expert_specialization_audit
result_status: complete
eligibility: eligible_single_seed_frozen_audit
typed_verdict: mixed_not_supportive
updated: 2026-08-10
---

# Detailed: A15_06_E06 Router--Expert Specialization And Utilization Audit

Primary Anchor: [A15_06_02](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_06_online_spectral_routing_and_relay/subanchors/15_06_02_router_expert_specialization_anchor.md)  
Frozen Protocol and revision: [A15_06_E06-v1 plus AM01/AM02](protocol.md)  
Summary: [summary.md](summary.md) / [summary_cn.md](summary_cn.md)  
Result eligibility: **ELIGIBLE for a single-seed frozen functional audit.**

## 0. Quick Recap

- **Purpose:** determine whether covariance-ranked Local-HMT or Relay-HMT
  creates and exploits stronger expert specialization than a
  dimension-matched random-subspace Router.
- **Hypothesis:** HMT should lower counterfactual expert-choice regret and
  improve Router-score--expert-utility ordering at 10B.
- **Experiment logic:** first establish that experts differ in parameter
  geometry, same-input functions, and next-token consequences; then require an
  HMT-versus-random functional advantage before attributing any effect to
  covariance identity.
- **Direct result:** both registered HMT paths failed the joint functional
  certificate. Experts nevertheless showed strong token-conditional functional
  differences, and all Routers exploited a modest fraction of them.
- **Eligibility:** 15/15 checkpoint tasks completed under the amended Protocol;
  exact no-op, Router replay, state immutability, data, checkpoint, and
  same-input guards passed.
- **Verdict:** `mixed_not_supportive`.
- **Claim boundary:** no covariance-specific functional support at seed 17 and
  10B; no claim about training causality, cross-seed replication, gradients,
  load, or PCGrad.

## 1. Terminology And Definitions

| Term | Plain meaning | Concrete computation | Unit / range | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| expert-choice regret | extra immediate loss paid by the native expert choice | \(L_{selected}-\min_eL_e\) over eight one-token, one-layer forced experts | nat/token, lower better | direct top-1 Router quality | long-run training benefit |
| score--utility alignment | whether Router scores order experts by immediate usefulness | tokenwise Spearman between eight Router logits and \(-L_e\) | \([-1,1]\), higher better | tests more than winner identity | causal training mechanism |
| best-match rate | fraction of targets on which Router chooses the forced-loss oracle | \(\Pr[s=\arg\min_e L_e]\) | fraction; chance \(1/8\) | intuitive utilization level | calibration of all experts |
| same-input linear CKA | similarity of expert output sample geometry under identical inputs | centered \(\|X^TY\|_F^2/(\|X^TX\|_F\|Y^TY\|_F)\) | \([0,1]\) | detects functional representation differences up to orthogonal basis / scale | utility or semantic profession |
| parameter-subspace overlap | shared dominant expert weight directions | mean squared canonical correlation of equal-rank orthonormal bases | \([0,1]\) | separates common parameter backbone from random orientation | same-input function |
| forced-expert NLL spread | sensitivity of the next-token prediction to expert identity | standard deviation of eight candidate NLLs per target | nat/token | detects non-interchangeability | correct Router choice |
| oracle entropy | diversity of the best expert across tokens | entropy of oracle expert shares divided by \(\log 8\) | \([0,1]\) | excludes one global winner | semantic specialization |
| margin--regret correlation | whether confident routing is more correct | Pearson correlation of top1--top2 logit margin and regret | \([-1,1]\); negative desired | confidence calibration | causal error source |
| PCGrad | training-time projection of conflicting task gradients | remove the component of one task gradient opposing another | not run | possible LM/LB conflict intervention | checkpoint specialization |

## 2. Anchor Link And Decision Point

The parent A15_06 line had already shown that covariance identity did not have a
stable endpoint-quality advantage over matched random controls. E06 asked the
remaining mechanism question: could HMT nevertheless create more specialized
experts or a better Router--expert functional binding that aggregate NLL did not
expose? A Pass required both lower regret and higher score--utility alignment.
Descriptive parameter or CKA differences could not rescue a failed functional
comparison.

## 3. Protocol Freeze, Conformance, And Deviations

| Registered item | Expected | Actual | Status | Evidence | Eligibility impact |
| --- | --- | --- | --- | --- | --- |
| approval | implementation, smoke, full audit authorized | user approved on 2026-08-10 | PASS | Protocol §0/§17 | eligible |
| arms | Vanilla, Local-HMT/Random, Relay-HMT/Random | all five | PASS | [task completeness](tables/task_completeness.csv) | none |
| seed/checkpoints | seed17; 2B/5B/10B | 15/15 complete | PASS | task table / raw task receipts | none |
| held-out data | frozen DCLM tensor and hash | SHA `5c8cca...a52e4` | PASS | each task receipt | none |
| 10B confirmation | 128 documents × 8 positions | exact | PASS | raw arrays / document table | none |
| CKA inputs | identical 8,192 inputs per expert/layer | exact | PASS | task schema and evaluator | none |
| primary inference | document pairing, 20k bootstrap/sign flips, Holm | exact | PASS | frozen aggregator | none |
| no-op | forced native expert must be exact | 0 for all 15 tasks | PASS | task completeness | none |
| Router replay | replayed logits reproduce deployed winner | minimum 1.0 | PASS | task completeness | none |
| state mutation | frozen model unchanged | all before/after hashes equal | PASS | task completeness | none |
| full/prefix diagnostic | recorded, not a primary estimator | mismatch 0--0.293%, mean 0.125% | BOUNDED | task completeness | no impact: all candidates and controls use the same prefix execution |
| AM01 | remove sequence/batch-shape native-reference noise | target-output delta intervention | PASS | Protocol AM01 | repaired before eligible full |
| AM02 | isolate BF16 grouped-GEMM replica contamination | ninth in-forward native control | PASS | Protocol AM02 / smoke | repaired before eligible full |
| first full attempt | expected eligible full | eight tasks failed no-op before science | INELIGIBLE | archived `om-h9f7rog8` | excluded completely |
| PCGrad | explicitly outside execution | NOT RUN | NOT_RUN | Protocol §11/§16 | no PCGrad claim |

The eligible source manifest is SHA-256
`ce553db0da3c5b0a52f5933ba404bdee9c6e945293845c9c0eb52dbb94922a81`.
No result-derived metric, arm, document, or checkpoint was added after the full
run began.

## 4. Actual Setup

- **Models:** five four-block, hidden-768, top-1 MoE models with eight sparse
  experts and one shared expert; all use the repaired differentiable Switch
  load-balancing objective during training.
- **Arms:** `vanilla_full`, `local_hmt`, `local_random_matched`, `relay_hmt`,
  `relay_random`.
- **Training state:** frozen seed-17 checkpoints at steps 2544, 6358, and 12716,
  corresponding to approximately 2B, 5B, and 10B tokens.
- **Trajectory targets:** 64 held-out documents × positions
  128/310/492/674 at every checkpoint.
- **10B confirmation targets:** 128 documents × positions
  128/219/310/401/492/583/674/765.
- **CKA targets:** 64 documents × 128 positions = 8,192 same expert inputs per
  layer.
- **Counterfactual:** for each target and layer, eight candidate replicas plus
  one native control share one prefix forward environment. The sparse output
  delta is \(w(e_{candidate}(h)-e_{selected}(h))\); shared expert output and all
  non-target tokens remain native. Unit-amplitude sensitivity is also stored.
- **Parameter geometry:** expert input basis comes from the dominant
  eigenspace of \(W_{gate}^TW_{gate}+W_{up}^TW_{up}\); output basis comes from
  \(W_{down}W_{down}^T\). Rank 8 is primary, with rank 16/32 sensitivity and a
  Haar orientation null.
- **Independence unit:** held-out document. Tokens, target positions, layers,
  expert pairs, and checkpoints are repeated measurements, not seeds.
- **Worker:** `/data/250010109/MoE_Router/experiments/20260810_router_expert_specialization_e06_frozen_v1`.
- **Eligible raw root:** `/data/250010109/MoE_Router/outputs/online_spectral_router_training_lb_fixed/e06_router_expert_specialization/`.

## 5. Metrics And Registered Decision Rules

For each matched path, HMT minus Random is computed on document means at 10B.
The path passes only if:

1. regret 95% CI is entirely below zero;
2. score--utility 95% CI is entirely above zero;
3. both corresponding Holm-adjusted paired sign-flip \(p<0.05\).

The two metrics are separate families, each containing Local and Relay. A
single favorable point estimate, CKA, parameter overlap, or route stability
cannot pass the path.

## 6. Evidence Lineage

| Claim or decision | Protocol criterion | Raw artifact | Computation | Aggregation / uncertainty | Observed value | Eligibility | Verdict | Limitation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Local covariance identity | regret lower and score alignment higher than Local-Random | 10B Local task arrays | HMT minus Random document means | 20k paired bootstrap/sign flip + Holm | regret \(-0.01042\) CI \([-0.02878,0.00753]\); score \(-0.00022\) CI \([-0.01313,0.01278]\) | ELIGIBLE | not supported | seed17 only |
| Relay covariance identity | same versus Relay-Random | 10B Relay task arrays | same | same | regret \(+0.01352\) CI \([-0.00361,0.03052]\); score \(-0.01121\) CI \([-0.02745,0.00481]\) | ELIGIBLE | not supported | seed17 only |
| expert outputs differ | low same-input CKA | 10B same-input expert outputs | 28 expert-pair CKAs/layer | descriptive pair and layer means | arm means \(0.326\)--\(0.335\); layer means about \(0.24\)--\(0.42\) | ELIGIBLE | supported descriptively | no causal quality claim |
| differences affect prediction | forced candidates have NLL spread | 10B counterfactual arrays | per-target candidate std | document/layer summaries | \(0.467\)--\(0.505\) nat/token | ELIGIBLE | supported | local intervention |
| utility is token conditional | oracle not globally concentrated | oracle index per target | normalized entropy/share | all 10B targets | entropy \(0.996\)--\(0.997\); max share \(0.145\)--\(0.155\) | ELIGIBLE | supported | no semantic labels |
| Router partly exploits utility | above-chance best match and positive ranking | selected, logits, candidate NLL | oracle match and Spearman | all documents/positions/layers | best match \(0.337\)--\(0.344\); Spearman \(0.130\)--\(0.162\) | ELIGIBLE | supported descriptively | no matched HMT advantage |
| parameters share a backbone | overlap exceeds Haar null | checkpoint weights | rank-8 canonical overlap | expert-pair/layer mean | \(0.142\)--\(0.234\) versus Haar q95 \(0.01355\) | ELIGIBLE | supported descriptively | overlap is not function |
| PCGrad useful here | measured gradient conflict plus intervention | none | none | none | NOT RUN | NOT_RUN | unknown | separate raw-gradient Protocol required |

## 7. Main Results

### 7.1 Eligible decision evidence

The registered [primary comparison table](tables/primary_comparisons.csv) gives
`mixed_not_supportive`. Local-HMT has a favorable regret point estimate but no
interval or score-order certificate. Relay-HMT has unfavorable point estimates
on both registered metrics. Unit routing amplitude increases absolute regret
for every arm but preserves the same qualitative matched ordering: it does not
reveal a hidden HMT identity advantage.

### 7.2 Expert-specialization ladder

At 10B, expert input/output parameter subspaces are much more aligned than
random orientations, yet same-input output CKA is far below one. This means the
experts retain a common dominant parameter backbone while implementing
different sample geometries. The forced-expert NLL spread and high oracle
entropy show that these differences matter conditionally for prediction rather
than only reflecting parameter re-expression.

The Router captures part of this structure: a roughly 34% oracle match rate is
well above 12.5% chance, and score--utility correlation is positive. However,
the unrestricted Vanilla Router has the highest mean score--utility correlation
(\(0.1625\)), while Relay-HMT has the lowest (\(0.1299\)). This is descriptive, not
a registered Vanilla superiority test, but it is inconsistent with the idea
that HMT identity uniquely exposes expert function.

### 7.3 Maturation and calibration

Across arms, 10B regret is lower than the corresponding 5B value, and most
score--utility correlations rise by 10B. Deep-layer route identity is highly
stable between checkpoints, especially for Relay arms (often 0.95--0.996).
Yet stability is not correctness: Relay-Random is at least as stable as
Relay-HMT, and HMT does not gain a functional certificate.

Margin--regret correlations are mostly positive (\(0.03\)--\(0.18\) by plotted
layer/arm, with one near-zero negative point). A well-calibrated confidence
signal would produce a negative relation. Thus top1--top2 margin should not be
used as a proxy for expert-choice correctness in these checkpoints.

### 7.4 Bounded and ineligible evidence

- Full-versus-prefix routing differs for at most 0.293% of registered targets
  because BF16 kernels change with execution shape. The scientific estimator
  uses prefix-local logits, candidates, and native control within the same
  execution; the diagnostic therefore bounds but does not contaminate the
  matched comparison.
- `om-h9f7rog8` is wholly ineligible. Its only contribution is the AM02
  engineering diagnosis; no metric or result from it enters a table or figure.
- PCGrad and raw LM/LB gradients were not measured.

## 8. Visualization Results

### Figure 1 — Router functional-quality trajectory

![Router functional-quality trajectory](figures/figure1_router_function_trajectory.png)

- **Source:** [document_metrics.csv](tables/document_metrics.csv).
- **How to read:** upper y-axis is regret in nat/token (lower better); lower is
  Router-score--utility Spearman (higher better); bands are document bootstrap
  95% intervals.
- **Observed:** all arms have substantial regret; score alignment generally
  improves toward 10B, but HMT does not separate consistently from Random.
- **Cannot prove:** trajectory causality or terminal NLL mediation.

### Figure 2 — 10B specialization ladder

![10B specialization ladder](figures/figure2_specialization_ladder.png)

- **Source:** [specialization_ladder.csv](tables/specialization_ladder.csv).
- **How to read:** lower parameter overlap and CKA mean more difference; higher
  forced-NLL spread means less interchangeability; higher score--utility
  Spearman means better Router utilization.
- **Observed:** function and utility differences are real, but the utilization
  panel does not favor HMT over Random.
- **Cannot prove:** semantic profession or causal performance gain.

### Figure 3 — Decisive matched comparisons

![Decisive matched comparisons](figures/figure3_primary_matched_comparisons.png)

- **Source:** [primary_comparisons.csv](tables/primary_comparisons.csv).
- **How to read:** regret must be entirely left of zero and score alignment
  entirely right of zero for the same path.
- **Observed:** every interval crosses zero; Relay point estimates favor
  Random.
- **Anchor implication:** no covariance-specific functional certificate.

### Figure 4 — Confidence and oracle guards

![Confidence and oracle guards](figures/figure4_confidence_oracle_guards.png)

- **Source:** [specialization_ladder.csv](tables/specialization_ladder.csv).
- **Observed:** oracle identity is diverse, but Router margin is not usefully
  calibrated to regret.
- **Cannot prove:** a particular semantic expert decomposition.

All four rendered PNGs were opened and visually audited on 2026-08-10. Labels,
axes, sign conventions, legends, layer order, and zero/uniform reference lines
match [figure_contracts.md](figure_contracts.md).

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | State | What it rules out | What remains live |
| --- | --- | --- | --- | --- |
| S0 provenance | 15 checkpoint/data/schema checks | PASS | missing or mismatched model state | one-seed limitation |
| S1 math | 33/33 tests | PASS | CKA/rank/bootstrap identity errors | real-data interpretation |
| S2 smoke | `pt-00k83wyi`, exact no-op/replay/state | PASS | target-control implementation failure | full-scale numerical diagnostic |
| S3 full | `om-v6p5s9ri`, 15/15, zero retries | PASS | missing trajectory/confirmation condition | scientific hypothesis may fail |
| S4 inference | frozen paired aggregator | PASS | unpaired token/layer pseudo-replication | cross-seed uncertainty |
| S5 figures | four images opened | PASS | plot-contract mismatch | visualizations remain descriptive |

- **Falsified operational hypothesis:** covariance H/M/T identity is not a
  stronger frozen Router--expert functional coordinate than its matched random
  bottleneck at the registered scale.
- **Not falsified:** experts specialize; a function-aligned coordinate may
  exist; conditional-fine directions may pass a later semantic and functional
  gate; LM/LB gradient conflict may exist.
- **Remaining rival:** bottleneck dimension/stability, rather than covariance
  ordering, accounts for any architecture-level effect.

## 10. Full Experiment Record

1. Protocol and subanchor were approved and frozen.
2. Mathematical implementation and real-checkpoint smoke initially identified
   execution-shape BF16 differences (AM01).
3. First full `om-h9f7rog8` exposed cross-replica grouped-GEMM contamination of
   the external no-op reference; the job was stopped and archived without
   scientific eligibility (AM02).
4. A ninth native-control replica was added; 33/33 tests passed.
5. Remote smoke `pt-00k83wyi` succeeded with no-op 0, replay 1.0, zero routing
   mismatch in smoke, and unchanged model-state hash.
6. Eligible full `om-v6p5s9ri` ran on one 8×5090 node from
   13:33:13Z to 13:38:01.888235Z, completed all 15 tasks, and had zero retries.
7. Frozen aggregation produced 20,000-draw paired intervals/sign-flip tests,
   four figures, and `mixed_not_supportive`.

## 11. Interpretation

The evidence separates three questions that are often conflated:

1. **Are expert parameters different?** Yes, but they also retain dominant
   common subspaces far above random overlap.
2. **Do experts implement different functions on the same inputs?** Yes; low
   CKA, large candidate NLL spread, and diverse oracle identities agree.
3. **Does the Router select those functions well, and does covariance identity
   help?** The Router is better than chance but incomplete; HMT is not better
   than dimension-matched Random under the registered certificate.

This supports a function-first pivot. Variance rank can shape learnability and
optimization without being the coordinate that predicts expert utility. CKA is
valuable for detecting same-input differentiation but must be paired with
functional swap cost. PCGrad is orthogonal: it can only address conflicting
training objectives after raw LM/LB gradients are measured, and it cannot be
inferred from CKA or regret.

## 12. Claim Boundary

**Can claim:** at seed17 and 2B--10B, the five differentiable-LB models contain
functionally non-interchangeable, token-conditionally useful experts; their
Routers exploit this structure partially; neither Local nor Relay covariance
identity beats its matched random control on the frozen functional certificate.

**Cannot claim:** semantic expert labels, specialization causally improves
NLL, random is universally superior, H/M/T can never help, cross-seed/scale
replication, load behavior, gradient conflict, or PCGrad efficacy.

## 13. Next Decision

- **Decision:** whether the active A15_07 conditional-fine direction can pass
  its cross-expression semantic certificate and then independently predict
  counterfactual expert utility beyond Router scores and matched random
  directions.
- **Completion criterion:** a held-out semantic certificate followed by a
  registered functional-admission result; no Router training is opened by
  readability alone.
- **Resume action:** review the six `AI_PROPOSAL` choices in the A15_07 Anchor.

## 14. Artifact Manifest

| Artifact | Purpose | Identity / hash | Complete | Claim-eligible | Notes |
| --- | --- | --- | --- | --- | --- |
| [protocol.md](protocol.md) | frozen contract | A15_06_E06-v1 + AM01/AM02 | yes | yes | append-only amendments |
| [source manifest](artifacts/source_manifest.sha256) | worker provenance | aggregate SHA `ce553d...22a81` | yes | yes | 163 source files |
| [execution receipt](artifacts/execution_receipt.json) | job status/history | full `om-v6p5s9ri` | yes | yes | ineligible attempt separated |
| [smoke verdict](artifacts/smoke_verdict.json) | target-control guards | `pt-00k83wyi` | yes | yes | no-op 0 |
| [document metrics](tables/document_metrics.csv) | paired independent-unit table | SHA `917e7a...12f78` | yes | yes | 2B/5B/10B |
| [primary comparisons](tables/primary_comparisons.csv) | decision table | SHA `e8c53c...a2a3` | yes | yes | 20k inference |
| [specialization ladder](tables/specialization_ladder.csv) | mechanism table | SHA `fc7d69...ef77` | yes | yes | descriptive |
| [typed verdict](tables/typed_verdict.json) | registered classification | SHA `2d9ad6...7896` | yes | yes | mixed_not_supportive |
| [Figure 2](figures/figure2_specialization_ladder.png) | specialization ladder | SHA `2fdb71...2536` | yes | descriptive | visually audited |
| [Figure 3](figures/figure3_primary_matched_comparisons.png) | decisive comparison | SHA `3e2540...ec6f` | yes | yes | visually audited |

Raw checkpoint arrays, logs, and failed-attempt artifacts remain on the worker
surface and are intentionally not copied into Research_System.

## 15. Links

- Anchor: [A15_06_02](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_06_online_spectral_routing_and_relay/subanchors/15_06_02_router_expert_specialization_anchor.md)
- Protocol: [protocol.md](protocol.md)
- Summary: [summary.md](summary.md)
- Code workspace: `/data/250010109/MoE_Router/experiments/20260810_router_expert_specialization_e06_frozen_v1`
- Eligible raw result: `/data/250010109/MoE_Router/outputs/online_spectral_router_training_lb_fixed/e06_router_expert_specialization/`
- Ineligible attempt: `/data/250010109/MoE_Router/outputs/online_spectral_router_training_lb_fixed/e06_router_expert_specialization_attempts/om-h9f7rog8`
- Eligible jobs: smoke `pt-00k83wyi`; full `om-v6p5s9ri`

