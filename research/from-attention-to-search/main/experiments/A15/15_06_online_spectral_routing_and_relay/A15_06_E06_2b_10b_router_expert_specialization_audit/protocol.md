---
experiment_id: A15_06_E06_2b_10b_router_expert_specialization_audit
anchor_id: 15_06_02_router_expert_specialization
status: approved_for_implementation_smoke_and_full_evaluation
approved_by: user
approval_date: 2026-08-10
design_revision: A15_06_E06-v1
design_frozen_at: 2026-08-10T13:00:00Z
resource_profile: 5090-8-spot
primary_metric: paired_document_difference_in_10b_counterfactual_expert_choice_regret
---

# Protocol: A15_06_E06 Router--Expert Specialization And Utilization Audit

## 0. Approval Snapshot

**Document status:** `APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL_EVALUATION`  
**Approval status:** the researcher approved the five-arm, one-seed,
2B/5B/10B scale and direct execution on 2026-08-10.  
**Block audit status:** A--G `CONFIRMED`.  
**Cross-block consistency:** `PASS`.  
**Execution scope approved:** implementation, unit tests, smoke, one full
single-node 8x5090 frozen-checkpoint evaluation, aggregation, figures, result
records, and owning-anchor evidence update.  Publication, Git commit/push,
root sync, and graph changes are not approved.  
**Purpose:** determine whether covariance-ranked H/M/T routing creates and
uses token-conditional expert specialization beyond a dimension-matched random
routing bottleneck.  
**Primary Anchor:** A15_06_02 Router--Expert Specialization And Utilization.  
**Experiment role:** frozen root-cause and metric audit; no model training and
no method intervention.  
**Minimal setup:** five seed-17 differentiable-LB arms at 2B, 5B, and 10B;
fixed held-out documents; eight sparse-expert counterfactuals at one target
token and one target layer at a time.  
**Treatment and controls:** Local-HMT versus Local-Random-Matched and Relay-HMT
versus Relay-Random are the covariance-identity tests; Vanilla-Full is the
unrestricted reference.  
**Changed variable:** Router input geometry learned during the already
completed training prefix.  
**Held fixed:** architecture, seed, data order, tokenizer, checkpoint token
budget, differentiable microbatch Switch LB objective, evaluation documents,
target positions, intervention amplitude, expert count, and statistics.  
**Primary metric:** Router expert-choice regret in nat/token; lower is better.  
**Pass:** an HMT arm has lower 10B regret and higher Router-score--expert-utility
rank correlation than its matched random control, with document-paired 95%
intervals and Holm-adjusted sign-flip tests supporting both directions.  
**Fail:** all validity guards pass but neither HMT arm obtains that two-metric
functional certificate.  
**Insufficient:** any required checkpoint, paired token identity, no-op replay,
same-input CKA, model-state immutability, or primary artifact fails.  
**Cannot claim:** specialization caused terminal NLL, PCGrad helps this model,
H/M/T have universal semantics, or the result generalizes beyond one seed and
this four-layer model.

## 1. Terminology / Definitions

- **Sparse experts:** the eight routed MLPs in each Transformer block.  The
  shared expert always runs, is never selected by the Router, and is not pooled
  with sparse-expert metrics.
- **Counterfactual expert utility:** the next-token NLL obtained by forcing one
  sparse expert only for one target token at one layer, while every other
  token and layer follows native routing.
- **Expert-choice regret:** selected-expert NLL minus the minimum NLL among all
  eight forced experts, in nat/token.  Zero means the native Router picked an
  immediate counterfactual best expert; it does not measure long-horizon
  training value.
- **Linear CKA:** centered kernel alignment on two experts' outputs for the
  same input tokens.  It measures whether their sample-similarity geometry is
  the same up to orthogonal rotations and isotropic scaling.  It is not
  invariant to arbitrary invertible transforms and cannot by itself identify
  useful specialization.
- **Dominant parameter subspace:** the top right-singular input directions of
  the concatenated `gate_proj` and `up_proj`, or the top left-singular output
  directions of `down_proj`.
- **Oracle-best expert:** the expert with minimum forced next-token NLL for a
  target.  Its identity must vary across tokens for swap cost to support
  conditional specialization rather than one globally dominant expert.
- **PCGrad:** a training-time multi-objective gradient projection algorithm.
  It is explained in the result report but is not executable on frozen
  checkpoints and is outside this no-backward audit.

## 2. Anchor Alignment

The parent A15_06 result did not reproducibly establish covariance-identity
value over matched random routing and could not identify expert specialization
as the mechanism behind NLL differences.  This experiment tests that one
remaining mechanism clause without changing the parent endpoint-NLL question.
The main falsifier is: experts may become geometrically different while the
Router does not select experts according to token-specific utility.

## 3. Tested Hypothesis

At 10B, covariance-ranked Local-HMT or Relay-HMT should beat its matched random
control in both immediate expert-choice regret and within-token agreement
between Router scores and forced-expert utility.  A supporting specialization
ladder should progress from parameter-space differences, to different outputs
on identical inputs, to nonzero expert swap cost with token-varying oracle
identity.  The trajectory from 2B to 5B to 10B determines whether this relation
emerges with training rather than appearing only as an endpoint snapshot.

## 4. Rival Explanations

1. **Arbitrary stable bottleneck:** random matched routing creates the same
   differentiation and choice quality as H/M/T.
2. **Parameter-only difference:** expert weights occupy different subspaces,
   but functions remain redundant on the same inputs.
3. **Different but unused experts:** same-input outputs and swap costs differ,
   but Router scores do not rank utility and regret remains high.
4. **Globally dominant expert:** one expert is best for nearly every token;
   swap cost is then not conditional specialization.
5. **Routing-amplitude artifact:** forced alternatives inherit the native top-1
   probability.  Unit-amplitude sensitivity checks that conclusions do not
   depend on this scalar.

## 5. Data Construction And Provenance

The frozen evaluation source is
`/data/250010109/MoE_Router/experiments/20260802_a15_01_04_progressive_band_source_2b_5090/artifacts/eval_tokens.pt`.
Its file SHA-256 is
`5c8cca2b0821f25b8e7abc50d7653dfba8d71e9ccf167fee61b82624116a52e4`.
The `dclm` tensor has shape `[1024,1024]`; the training runs' frozen manifest
records its validation-token SHA as
`91acad820e5521832a4e54033fd062d4d275819856725d9803981c0c972a289c`.
No document or target is selected using model results.

Two nested sets are frozen:

1. **Trajectory set:** documents 0--63 and absolute token positions
   `[128,310,492,674]`, giving 256 targets at 2B, 5B, and 10B.
2. **10B confirmation set:** documents 0--127 and positions
   `[128,219,310,401,492,583,674,765]`, giving 1,024 targets.  The trajectory
   targets are a declared subset and are not treated as independent from it.

The same-input expert-output set is documents 0--63 at 128 positions
`64+7j`, \(j=0,\ldots,127\), for 8,192 expert inputs per layer.  The statistical
unit for uncertainty is the document; positions, layers, experts, and expert
pairs are repeated measurements, not independent samples.

## 6. Learning Task And Permitted Supervision

There is no fitting or training.  For each target token, layer, and candidate
expert, the evaluator predicts the native next token and records NLL.  Router
logits, native expert identity, forced-expert losses, expert inputs, unweighted
sparse-expert outputs, and expert parameters are permitted.  Test labels may
only be used to compute next-token NLL; they may not select documents,
positions, subspace rank, or checkpoints.

## 7. Model / Architecture And Frozen Variants

Every checkpoint is the verified E05 four-block H768 MoE with eight top-1
sparse experts, one shared expert, sparse-expert width 1536, BF16 inference,
and differentiable microbatch Switch LB used during training.  The five arms
are:

| Arm | Router view | Evidence role |
| --- | --- | --- |
| Vanilla-Full | uncentered complete local representation | unrestricted reference |
| Local-HMT | dynamic local covariance H/M/T in blocks 2--4 | local covariance treatment |
| Local-Random-Matched | dynamic local matched random nested subspaces | local identity control |
| Relay-HMT | block-1 covariance H/M/T relayed to blocks 2--4 | relay covariance treatment |
| Relay-Random | matched random block-1 relay | relay identity control |

The shared expert, attention, residual stream, LM head, and all parameters are
frozen.  Direct dot products between Router weights and expert weights are
forbidden because Router input and expert input are not the same object,
especially in Relay arms.

## 8. Training Objective And Optimization

No optimization occurs.  PCGrad is not run: it would require decomposed LM and
LB gradients and would change the training update.  The evaluator uses
`torch.inference_mode()` and verifies that parameter and persistent-buffer
hashes are unchanged before and after every checkpoint task.

## 9. Conditions, Seeds, And Checkpoints

Seed is fixed to 17.  All five arms are evaluated at:

| Label | Optimizer step | Actual cumulative tokens |
| --- | ---: | ---: |
| 2B | 2,544 | 2,000,683,008 |
| 5B | 6,358 | 5,000,134,656 |
| 10B | 12,716 | 10,000,269,312 |

The 15 checkpoint paths must exist under
`/data/250010109/MoE_Router/outputs/online_spectral_router_training_lb_fixed/`
and must match their recorded step, model schema, and frozen source manifest.
No 20B/25B/30B state is used in E06.

## 10. Primary Metric And Frozen Analysis Plan

For document \(d\), target \(p\), layer \(\ell\), selected expert \(s\), and forced
candidate \(e\), let \(L_{d,p,\ell,e}\) be next-token NLL.  Define

\[
r_{d,p,\ell}=L_{d,p,\ell,s}-\min_e L_{d,p,\ell,e}.
\]

At 10B, average positions within document, then equally average four layers.
For each matched pair, compute HMT minus random; negative means HMT chooses
better experts.  The second decision quantity is the analogous document-level
difference in mean Spearman correlation between the eight Router logits and
\(-L_e\); positive means better score--utility alignment.

- **Unit of observation:** target token and layer.
- **Unit of independence:** held-out document.
- **Confirmation sample:** 128 documents and eight targets per document at
  10B; the 64-document trajectory set is descriptive.
- **Uncertainty:** 20,000 paired document bootstrap draws with fixed RNG seed
  `20260810`, percentile 95% intervals.
- **Tests:** 20,000 paired document sign-flip draws per metric and comparison;
  two matched comparisons are Holm-adjusted within each primary metric family.
- **Checkpoint selection:** fixed 10B; no best-checkpoint selection.
- **Missing/outliers:** no outcome-based removal or winsorization.  A failed
  document is retained as a failure record and makes the comparison
  Insufficient unless reconstructed from the same frozen task.
- **Unsealing:** primary rules freeze before the first full scientific result.

Typed outcomes are `support_local`, `support_relay`, `support_both`,
`mixed_not_supportive`, `no_covariance_specific_support`, and `insufficient`.
Support for a path requires regret CI below zero and score--utility correlation
CI above zero, with Holm-adjusted \(p<0.05\) for both.  Secondary metrics cannot
rescue a non-supportive primary result.

## 11. Secondary Metrics And Guards

1. **Margin--regret calibration:** Router top1--top2 logit margin versus regret;
   a useful confidence score should associate larger margins with lower
   regret.  It cannot establish specialization.
2. **Route maturation:** fraction of the same targets retaining expert identity
   from 2B to 5B and 5B to 10B, per layer.  It describes stability, not quality.
3. **Parameter subspaces:** for `gate_proj+up_proj` input geometry and
   `down_proj` output geometry, compute pairwise mean squared canonical
   correlation at \(k=\max(1,\lceil0.01\min(d_{in},d_{out})\rceil)\) (primary,
   approximately 8), with \(k=16,32\) sensitivity and dimension-matched Haar
   q95.  Lower overlap means different dominant parameter geometry, not useful
   function.
4. **Same-input linear CKA:** use all experts on the identical 8,192 expert
   inputs, before routing amplitude and before the shared-expert addition.
   Lower CKA means different relational output geometry, not necessarily
   better experts.
5. **Swap cost and oracle diversity:** candidate-loss spread, native-to-
   alternative loss increase, per-expert oracle share, and oracle entropy.
6. **Router--expert empirical coupling:** correlate centered Router logit
   \(z_e-\bar z\) with \(\|B_{e,k}^{\top}h\|^2/k\) on the same tokens, where
   \(h\) is actual expert input and \(B_{e,k}\) is that expert's dominant input
   parameter basis.  This avoids invalid cross-space weight dot products.
7. **Amplitude sensitivity:** rerun 10B counterfactuals with target routing
   amplitude fixed to one.  Directional reversal of a primary comparison is a
   named confusing outcome and limits interpretation to the native-amplitude
   intervention.

No gradient conflict, PCGrad intervention, system throughput, capacity-drop,
or load-balance analysis is part of E06.

## 12. Known Good / Known Bad / Known Confusing Cases

- **Known good:** identical matrices/subspaces give overlap and CKA one;
  orthogonally changed feature bases preserve CKA; perfectly ordered Router
  scores and utilities give Spearman one; forcing the native assignment is a
  no-op.
- **Known bad:** independently permuting sample rows breaks same-input CKA;
  orthogonal subspaces have near-zero overlap; reversed score order gives
  Spearman minus one; missing target isolation invalidates forced utility.
- **Known confusing:** low parameter overlap with CKA near one is redundant
  parameterization; low CKA with zero swap cost is output difference without
  decision relevance; high swap cost with one oracle expert is global
  dominance; better regret without higher score correlation can arise from
  winner-only calibration rather than full ranking.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal | Input and assumptions | How | Expected output | Gate / named failure | Artifact |
| --- | --- | --- | --- | --- | --- | --- |
| S0 | freeze provenance | 15 checkpoints and held-out tensor | hash schema, step, source, model state, target manifest | immutable manifest | any mismatch: Insufficient | `raw/provenance.json` |
| S1 | validate math | synthetic known-good/bad arrays | unit tests for CKA, ranks, subspaces, bootstrap | test report | any failed identity blocks smoke | `tests/` report |
| S2 | real no-op smoke | Vanilla 2B, 2 docs, 2 positions, 64 CKA inputs | load, native replay, one intervention, state hash | smoke verdict | NLL error >2e-5 or mutation blocks full | `smoke_verdict.json` |
| S3 | full frozen audit | all 15 tasks | distribute checkpoint tasks over 8 GPUs; one target intervention per replicated sequence | raw arrays and summaries | missing task: affected comparison Insufficient | worker `raw/` |
| S4 | paired inference | complete raw arrays | frozen aggregation, bootstrap, sign-flip, matched contrasts | typed verdict tables | schema or pairing failure: Insufficient | project `tables/` |
| S5 | visual/evidence audit | eligible tables | render registered figures and open each image | audited figures | plot-contract mismatch blocks result finalization | project `figures/` |

Scale-up occurs only after S0--S2 pass.  NaN/Inf, OOM, corrupted checkpoint,
distributed task loss, no-op failure, or persistent model-state mutation stops
the affected task.  A scientifically poor result never triggers early stop.

## 14. Algorithm, Output, And Provenance Contract

For each target intervention the evaluator creates a separate causal sequence
replica, changes exactly one target-layer sparse expert, preserves all other
routing, and reads the logits predicting the next token.  The main analysis
retains the native top-1 probability as the common amplitude across all eight
candidate experts.  A target-only override sets that amplitude to one for the
sensitivity analysis.  The override never changes non-target tokens.

Code is frozen in a dedicated worker snapshot under
`/data/250010109/MoE_Router/experiments/20260810_router_expert_specialization_e06_frozen_v1`.
Raw outputs go to
`/data/250010109/MoE_Router/outputs/online_spectral_router_training_lb_fixed/e06_router_expert_specialization/`.
Research_System receives only Protocols, run receipts, compact tables, figures,
`summary.md`, and `detailed.md`; checkpoints and raw arrays remain in worker
storage.  The code manifest, environment, ACP job ID, commands, and every raw-
to-table transformation are recorded in `detailed.md`.

## 15. Success / Failure / Insufficient Evidence

- **Pass_Local / Pass_Relay / Pass_Both:** the corresponding matched path
  passes both registered primary quantities at 10B; the specialization ladder
  determines whether the result is Router exploitation of non-interchangeable
  experts or only a functional choice signal.
- **Fail:** validity guards pass, but neither matched HMT path passes both
  primary quantities.  This rejects a covariance-specific frozen functional
  certificate at the registered scale; it does not prove experts are identical.
- **Mixed:** one metric or one unadjusted comparison favors HMT but the full
  registered certificate does not pass.  Mixed is reported as not supportive.
- **Insufficient:** provenance, no-op, target isolation, state immutability,
  same-input condition, checkpoint completeness, or primary aggregation fails.

## 16. What This Cannot Claim

Even a Pass cannot show that expert specialization caused terminal held-out
NLL, that covariance bands have universal semantics, that Relay works at other
depths or scales, that two seeds would agree, or that PCGrad should be applied.
CKA and parameter overlap are descriptive representation metrics; regret is a
one-token frozen intervention, not a joint-training counterfactual.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | State | Grounding |
| --- | --- | --- |
| A Question and boundary | CONFIRMED | researcher approved Router function plus expert specialization scope |
| B Data and provenance | CONFIRMED | researcher approved scale; existing held-out artifact verified |
| C Task and supervision | CONFIRMED | frozen next-token counterfactual utility |
| D Architecture | CONFIRMED | five valid-LB E05 arms, seed 17, shared expert separate |
| E Objective/optimization | CONFIRMED | no training/backward; PCGrad excluded from execution |
| F Comparison/evidence | CONFIRMED | regret, score--utility alignment, CKA and specialization ladder |
| G Execution | CONFIRMED | implementation, smoke, 8x5090 full, records authorized |

Cross-block consistency passed before implementation.  The scientific body is
frozen as `A15_06_E06-v1` at the timestamp in the front matter.  After the
first execution starts, only status receipts, result links, or append-only
amendments with eligibility impact may be added; observed results never rewrite
the registered body.

### E06-AM01 — numerically exact target-local counterfactual realization

- **Amendment time:** 2026-08-10T13:45:00Z.
- **Before:** the first smoke changed the target expert through the model's
  batchwise forced-assignment hook and compared it with a native forward having
  a different prefix/batch shape.
- **Observed before amendment:** no scientific arm comparison was visible. The
  smoke-only native-expert replay differed by up to 0.0533 nat/token. A focused
  diagnostic showed that identical routing within the same execution shape had
  exactly zero logit error; the difference came from BF16 kernels changing with
  sequence and expert-group batch shape.
- **After:** all eight candidates, Router logits, and the no-op reference use
  the same prefix and replica shape. At the target MLP output, the evaluator
  applies \(w(e_{candidate}(h)-e_{selected}(h))\) for native-amplitude
  comparisons, or \(e_{candidate}(h)-w e_{selected}(h)\) for unit-amplitude
  sensitivity. Every non-target token and the native shared-expert output
  remain bitwise native.
- **Reason:** remove execution-shape numerical noise while preserving the
  registered intervention: one target token, one target layer, one candidate
  sparse expert, all other computation native.
- **Affected blocks:** scientific procedure and implementation identity only;
  question, data, checkpoints, metrics, aggregation, verdict, and claim
  boundary are unchanged.
- **Approval basis:** this implementation repair is inside the user-approved
  scope and does not change the scientific question or five-arm contract.
- **Eligibility:** the failed pre-amendment smoke is ineligible. The repeated
  smoke is eligible: native-expert no-op error 0, full-versus-prefix expert
  identity mismatch 0, Router replay 1.0, and unchanged state hash.

### E06-AM02 — in-forward native control for replica isolation

- **Amendment time:** 2026-08-10T13:27:00Z.
- **Trigger:** the first full attempt (`om-h9f7rog8`) failed all eight initial
  tasks before any scientific output. Although the selected-candidate delta was
  algebraically zero, its NLL differed from a native forward by
  0.0176--0.0931 nat/token.
- **Root cause:** the eight candidate replicas shared one forward. The seven
  non-native candidates changed downstream MoE expert-group sizes, so BF16
  grouped-GEMM kernel selection numerically perturbed the otherwise native
  replica. The intervention itself remained target-local; the no-op reference
  did not share the same downstream batch environment.
- **Repair:** every document now has nine replicas in one forward: eight expert
  candidates plus a ninth explicit native control. The selected-expert
  candidate and native control both receive an exact zero delta and share all
  downstream grouping effects. Candidate NLLs are evaluated relative to that
  within-forward control; all eight scientific candidates are unchanged.
- **Affected blocks:** numerical control realization and worker source identity
  only. Question, checkpoints, targets, sample size, metrics, inference,
  verdict, and claim boundary are unchanged.
- **Eligibility:** `om-h9f7rog8` is an ineligible engineering attempt. A new
  full run requires unit tests and a real-checkpoint no-op smoke to pass again.
