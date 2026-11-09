---
experiment_id: A14_02_E01_shared_rule_vs_lookup_root_rank
status: completed_insufficient
run_authorized: true
run_id: a14_02_e01_shared_rule_vs_lookup_root_rank_4gpu_20260723_1427
job_id: pt-q6hu0fq5
result_summary: summary.md
primary_anchor: ../../../../problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/14_02_relation_reuse_root_effective_rank_anchor.md
companion_cn: protocol_cn.md
---

# Protocol: A14_02_E01 Shared Rules Versus Lookup Root-State Rank

## 0. Approval Snapshot

**Approval status:** Approved with frozen amendments after user review on
2026-07-23. The user authorized the frozen full four-GPU execution on
2026-07-23.

**Purpose:** Determine whether shared compositional structure reduces the
task-functional dimension of a final root state after exact-relation
frequency, rule-instance count, context pool, answer distribution, training
contract, and full-state utility are matched.

**Primary anchor:** [A14_02 shared compositional rules and task-functional
root-state rank](../../../../problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/14_02_relation_reuse_root_effective_rank_anchor.md)

**Decision question:** At matched rule-instance count \(K\), training exposure
\(F\), context diversity \(D\), output entropy, model, and full-state held-out
utility, does the shared family require fewer post-final-normalization `ROOT`
directions than independent lookup tables?

**Physical prior tested:** Reusing one compositional mechanism across rule
instances can permit a reusable task-state formation mechanism.

**Core model term:** Task-functional root rank
\(k_{\mathrm{func}}(\epsilon_L,\epsilon_A)\).

**Main falsifier:** The shared-versus-lookup difference vanishes after
matching, or is fully explained by lookup cardinality, answer bottlenecks,
capability mismatch, or the final-normalization interface.

**Experiment role:** Root-cause and operationalization audit; not a Router
method experiment.

**Primary metric:** Normalized shared-structure functional-rank advantage,
\(\Delta k_{\mathrm{structure}}\).

**Claim boundary:** Controlled synthetic NTP representation mechanism only.

**Minimal setup:** A two-step synthetic NTP task; matched shared and lookup
generators; a final post-normalization `ROOT` primary state; a
pre-normalization localization state; five paired seeds.

**Basic configuration:** Two-layer, one-head decoder-only Transformer with
\(d_{\mathrm{model}}=64\); full-position NTP CE; identical training and
measurement contracts across paired conditions.

**Conditions:** Stage A shared-versus-lookup by low/high exposure; Stage B
lookup-\(K\) rival calibration; Stage C diverse-context versus exact-duplicate
guard.

**Pass:** Both primary conditions pass matched utility and replay gates; the
post-normalization functional-rank advantage is at least \(4/64\), has a paired
95% interval above zero, and has the expected sign in at least four of five
seeds; the learned subspace beats equal-rank random subspaces; lookup
cardinality and answer bottlenecks do not explain the result.

**Fail:** Matched shared and lookup conditions require the same functional
rank, or the full difference is explained by a registered rival.

**Insufficient:** Capability or matching fails; a generator, split, replay,
leakage, or sample-size guard fails; or the result is unstable.

**Cannot claim:** Natural language is low-rank; language is an explicit tree;
QK is low-rank; state and parameter rank are equal; or a Router is useful.

**Approval decision:** Approved with amendments; full execution authorized.

## 1. Terminology And Definitions

| Term | Plain meaning | Concrete object / computation | Unit | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Exact relation | One input--rule-instance--answer mapping entry | Shared: \((a,\alpha,\beta,y)\); lookup: \((a,k,y)\) | tuple | Defines \(F\) | Semantic rule identity |
| Rule-instance count \(K\) | Number of distinguishable rule IDs in the input | 16 parameter pairs or 16 random tables | count | Matches rule-ID cardinality | Equal algorithmic independence |
| Training exposure \(F\) | Number of training occurrences of one exact relation | Samples per mapping entry | count | Separates low/high frequency | Shared structure |
| Context diversity \(D\) | Balanced nuisance templates available in a generator or split | Context-pool coverage | count | Separates context variation from duplication | Per-relation diversity when \(F=1\) |
| Shared family | Rule instances reuse one two-step function form | \(u=\phi_\alpha(a)\), \(y=\psi_\beta(u)\) | generator | Treatment | Natural-language semantics |
| Lookup family | Each rule instance is an independent random permutation | \(y=\pi_k(a)\) | generator | Memorization rival | That the trained model only memorizes |
| Post-norm root | Final `ROOT` state after LayerNorm/RMSNorm and before the LM head | Primary intervention state | directions | Registered answer interface | All intermediate computation |
| Pre-norm root | Same `ROOT` residual state before final normalization | Secondary intervention followed by real final norm and LM head | directions | Localizes normalization effects | Algebraic equivalence to post-norm rank |
| Task-functional root rank | Minimum retained directions preserving held-out answer behavior | Calibration-fit subspace, test replay | directions | Primary causal metric | Strict rank or nonlinear intrinsic dimension |
| Effective rank | Equivalent number of spectral-energy directions | Entropy effective rank | directions | Secondary geometry | Task sufficiency |

## 2. Anchor Alignment

The experiment tests whether shared composition contributes task-state
compression beyond frequency and lookup cardinality. It does not test a
parameter-rank requirement or Router utility.

The A14_01/E08 reconstruction mixed reuse, per-rule frequency, and independent
rule count. A14_02 orthogonalizes these variables and moves the primary object
from an attention update to a final task root.

## 3. Tested Hypothesis

For the low-exposure matched comparison,

\[
\Delta k_{\mathrm{structure}}
=
\frac{
k_{\mathrm{func}}^{lookup}
-k_{\mathrm{func}}^{shared}
}{64}
\ge \frac{4}{64}.
\]

The paired 95% bootstrap interval must have a lower bound above zero, and at
least four of five seed differences must be positive.

Frozen replay tolerances are

\[
\epsilon_L=0.02\ \text{nat},
\qquad
\epsilon_A=0.01.
\]

## 4. Rival Explanations

1. Fewer lookup tables reduce rank.
2. Higher exact-relation exposure reduces rank.
3. Exact surface duplication, rather than cross-context structure, creates
   concentration.
4. A finite answer vocabulary creates a final-state bottleneck.
5. One condition did not learn the task or has different confidence.
6. Test-answer identity leaked into the fitted intervention.
7. Finite sample count artificially limits rank.
8. Any equal-rank projection works because the model is generally tolerant.
9. Checkpoints were selected after observing test rank.
10. Lookup was unfairly asked to predict unseen random mapping entries.
11. Later attention reread deleted information from other positions.
12. Final normalization alone created or removed the observed contrast.

## 5. Data, Model, Algorithm, And Objective

### 5.1 Shared generator

Use a finite, exactly computable, bijective two-step family:

\[
u=\phi_\alpha(a),
\qquad
y=\psi_\beta(u).
\]

There are 16 registered parameter-pair rule instances. All instances share the
same function family. The concrete finite-group or bitwise operation must be
frozen before implementation and cannot be changed after rank inspection.

### 5.2 Lookup generator

Use 16 independent random permutations,

\[
y=\pi_k(a),
\]

with the same entity set, rule-token surface, answer set, sequence length, and
answer marginal as the shared generator.

### 5.3 Variables held exactly fixed

Paired conditions use identical:

1. entity cardinality;
2. rule-instance count \(K=16\);
3. per-entry training exposure \(F\);
4. nuisance context pool and split allocation;
5. train, calibration, and test sample counts;
6. vocabulary, token positions, sequence length, and NTP supervision;
7. answer vocabulary, per-rule answer marginals, and output entropy;
8. total training tokens and filler count;
9. model architecture, parameter count, paired initialization seed, optimizer,
   learning rate, batch size, training budget, and evaluation interval;
10. `ROOT` position, state sample count, subspace budget, \(k\) grid, random-space
    count, and bootstrap contract.

The same latent-index, context, and split manifest is reused. Only the mapping
column changes from shared composition to independent lookup. Both generators
use bijections so that answers are exactly balanced.

### 5.4 Split contract

**Primary functional-rank test:** New nuisance contexts for mapping entries
seen during training. Both shared and lookup conditions can solve this test.

**Composition-generalization diagnostic:** Unseen input--rule combinations.
This verifies that the shared generator was learned compositionally. It does
not enter the shared-versus-lookup primary rank contrast, and lookup is not
required to infer unseen random table entries.

### 5.5 Sequence and model

```text
[rule-part-1] [entity] [nuisance-context] [rule-part-2] [ROOT] [ANSWER]
```

Use a two-layer, one-head, \(d_{\mathrm{model}}=64\) causal Transformer trained
with full-position NTP CE.

The primary intervention is the `ROOT` state after final LayerNorm/RMSNorm and
before the LM head. Replay only the frozen LM head. The secondary intervention
uses the pre-final-normalization `ROOT` residual state, then replays the real
final normalization and frozen LM head. The post-norm result alone decides the
verdict.

## 6. Conditions, Seeds, And Checkpoints

### Stage A: decisive \(2\times2\)

| Condition | Structure | Exposure | Context allocation | Role |
| --- | --- | --- | --- | --- |
| S-U | Shared | \(F=1\) | Family-level diverse pool | Decisive rare shared case |
| L-U | Lookup | \(F=1\) | Same manifest | Matched memorization rival |
| S-R | Shared | \(F=F_H\) | Diverse repetitions | Frequency guard |
| L-R | Lookup | \(F=F_H\) | Same manifest | Frequency guard |

### Stage B: lookup cardinality

Use lookup-only repeat-diverse conditions with \(K\in\{1,4,16\}\). Interpret the
curve causally only if per-rule exposure, total token budget, output marginal,
and filler are exactly matched.

### Stage C: frequency versus diversity

Compare shared repeat-diverse and shared repeat-duplicate conditions at the
same exact-relation count.

### Seeds and checkpoint gate

Use five paired seeds. On calibration data, select the first checkpoint with:

- answer accuracy at least 0.95;
- answer CE at most 0.10 nat;
- three consecutive passing evaluations;
- no missing answer class.

After selection, the paired conditions must also satisfy, on full-state
held-out evaluation:

- absolute accuracy difference at most 0.01;
- absolute CE difference at most 0.02 nat.

Test does not select checkpoints. Failed matching produces an insufficient
verdict, with no test-guided reselection or condition-specific retuning.

### Condition and guard registry

| Item | Clause / rival tested | Evidence role | Pass | Fail / insufficient | Artifact |
| --- | --- | --- | --- | --- | --- |
| S-U vs L-U | Shared structure beyond \(K,F,D\) | Primary | Frozen effect and inference rules pass | No contrast or failed gates | Primary rank table |
| S-R vs L-R | Exposure interaction | Secondary guard | Direction interpretable | Descriptive only | Exposure table |
| Lookup-\(K\) | Lookup cardinality rival | Rival calibration | Cannot explain full primary gap | Explains gap | Lookup-\(K\) table |
| Diverse vs duplicate | Context variation rival | Rival calibration | Separates context effect | No separation | Diversity table |
| Full-rank replay | Hook validity | Hard gate | Numerical restoration | Insufficient | Replay table |
| Shuffle | State use | Hard guard | Task degrades | Insufficient | Replay table |
| Random subspaces | Arbitrary tolerance | Hard guard | Learned basis wins | Fail / insufficient | Random-control table |
| Pre/post norm | Normalization artifact | Localization | Boundary is clear | Contrast exists only at interface | Norm table |

## 7. Primary Metric

Fit a task-aware orthogonal subspace on calibration data only. The model is
frozen. For each registered \(k\), project a test post-norm root state as

\[
\widetilde h_i^{(k)}
=
\mu^{cal}
+U_kU_k^\top(h_i-\mu^{cal}),
\]

then replay the frozen LM head. The calibration mean is global and does not
depend on test-answer identity.

Define \(k_{\mathrm{func}}\) as the smallest registered \(k\) for which loss
increases by at most 0.02 nat and accuracy decreases by at most 0.01, with all
higher registered dimensions also passing. The primary comparison is S-U
versus L-U at the post-norm root.

The task-aware optimizer, steps, initialization set, and calibration selection
rule must be frozen before execution. Calibration PCA replay is an auditable
upper-bound diagnostic, not the primary metric.

## 8. Ordered Secondary Analysis

Results must be read in this order:

1. generator, capability, matched-utility, and full-rank replay gates;
2. post-norm \(\Delta k_{\mathrm{structure}}\);
3. loss/accuracy, random-subspace, shuffle, and equal-sample guards;
4. pre-norm functional rank and the pre/post contrast;
5. PCA replay, full-root effective rank, answer-residual effective rank,
   within-answer energy, and \(r_{95}\);
6. semantic consistency and unseen-combination accuracy;
7. lookup-\(K\) and diverse-versus-duplicate rivals;
8. gradient alignment and Q/K/\(B_{QK}\) bridges as exploratory diagnostics only;
9. earlier-layer localization only with a registered no-reread or bypass audit.

No secondary result can reverse a failed primary verdict.

## 9. Known Cases

**Known good:** The shared oracle generator is exact on all registered splits.

**Known bad:** Shuffled rule parameters or answers reduce unseen-combination
accuracy toward chance.

**Known confusing:** Low rank with failed utility; lookup \(K=1\) with low rank
but no composition; a final answer bottleneck; a post-norm-only contrast; PCA
rank above task-aware rank; or an intermediate-state replay that succeeds only
because later attention rereads the input.

## 10. Stage-Level Profiling

| Stage | Question | Hard rule | Output |
| --- | --- | --- | --- |
| Generator audit | Are marginals and manifests matched? | Exact checks | Generator table |
| Capability | Did all primary conditions learn? | Frozen gate | Curves by seed |
| Root extraction | Are pre/post states correct? | Position and shape checks | State manifest |
| Replay audit | Is the intervention valid? | Full rank, zero rank, shuffle | Replay table |
| Functional rank | Does shared win? | Frozen primary rule | Rank curves |
| Final-norm audit | Is the contrast interface-specific? | Secondary localization | Norm table |
| Rival audit | Do \(K\) or duplication explain it? | Registered controls | Rival tables |

## 11. Algorithm Specification

1. Load paired calibration and test manifests and selected checkpoints.
2. Cache pre-final-normalization and post-final-normalization `ROOT` states.
3. Fit each registered task-aware subspace on calibration data only.
4. Replay projected post-norm states through the frozen LM head.
5. Replay projected pre-norm states through the real final norm and LM head.
6. Run full-rank, zero-rank, shuffle, and random-subspace controls.
7. Compute persistent-threshold functional ranks.
8. Compute paired seed differences and paired bootstrap intervals.
9. Report gates, primary result, guards, norm localization, geometry,
   generalization, and rivals in the frozen order.

Required result tables include capability gates, generator matching, primary
functional ranks, pre/post norm ranks, projection curves, random controls,
lookup-\(K\), and diversity guards.

## 12. Success, Failure, And Insufficient Evidence

**Success:** All gates pass; S-U and L-U have matched full-state utility;
\(\Delta k_{\mathrm{structure}}\ge4/64\); paired 95% lower bound is above zero;
at least four of five seeds are positive; learned subspaces beat random spaces;
and registered rivals do not explain the full difference. Shared
unseen-combination accuracy at least 0.80 and semantic consistency at least
0.95 confirm that the shared generator was learned compositionally, but lookup
is not required to predict unseen random entries.

**Failure:** Matching succeeds but there is no shared functional-rank
advantage, or a registered rival fully explains it.

**Insufficient:** Any primary condition misses capability or utility matching;
generator, sample, replay, leakage, or stability guards fail; or post-hoc
retuning would be required.

## 13. What This Cannot Claim

The experiment cannot establish that natural language is tree structured or
low-rank, that all low-frequency relations are high-rank, that NTP generally
produces low-rank states, that state rank equals parameter rank, or that a
particular MoE Router has utility.

## 14. Review Notes And Changes

- 2026-07-23: Chinese draft created; no run authorization.
- 2026-07-23: Primary object changed from residual spectral rank to held-out
  task-functional root rank; leakage, replay, random-subspace, answer-bottleneck,
  and suffix-bypass guards added.
- 2026-07-23: User approved with amendments. Frozen additions: exact matching
  ledger; primary versus composition-generalization split separation;
  post-final-normalization primary state; pre-normalization localization;
  ordered analysis; matched capability gate; \(\epsilon_L=0.02\) nat,
  \(\epsilon_A=0.01\), \(\delta_k=4/64\); five seeds and paired inference. Execution
  was initially unauthorized.
- 2026-07-23: User authorized implementation, smoke validation, and the frozen
  four-GPU full run. No hypothesis, metric, threshold, condition, or seed was
  changed after authorization.
- 2026-07-23: Four-GPU run `pt-q6hu0fq5` completed 35/35 jobs. The formal
  verdict is `insufficient`: both low-exposure primary conditions failed
  held-out capability, so their emitted rank contrast is not interpretable.
  See [summary.md](summary.md) and [detailed.md](detailed.md).
