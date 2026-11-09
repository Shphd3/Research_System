# Detailed: A15_17_E02 Gradient, Parameter, And Local-Utility Follow-Up

Primary Anchor: [A15_17](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/15_17_three_model_sae_representation_trajectory_anchor.md)  
Frozen Protocol and registered revision: [protocol.md](protocol.md), including R001--R003  
Summary: [summary.md](summary.md); Chinese companion: [summary_cn.md](summary_cn.md)  
Result eligibility: `ELIGIBLE`; verdict `AI_DRAFT_NOT_SUPPORTED_AWAITING_HUMAN_CONFIRMATION`.

## 0. Quick Recap

- Purpose: test whether an actual reconstruction-to-backbone gradient improves one-step held-out representation readability, and fill the registered L1--L4/15B gaps.
- Hypothesis: U1 should yield positive P-report \(\mathrm{CE}(U0)-\mathrm{CE}(U1)\) with an interval above zero; the rival is a real but locally unhelpful gradient path.
- Direct result: 10B `−0.000622 [−0.001691, 0.000400]`; 15B `−0.000571 [−0.001664, 0.000564]` nats. Both fail the registered support rule.
- Eligibility: Smoke, fresh full v2, 16 isolated updates, all guards, and CPU synthesis passed. Failed roots are excluded.
- Claim boundary: one-step local direction, descriptive historical displacement, and development-panel NLL only; no long-run causal formation or general-capability claim.

The researcher has not supplied the closed-book final judgment. The measurements and eligibility audit are complete; the scientific wording remains an AI draft.

## 1. Terminology And Definitions

| Term | Plain meaning | Concrete object / computation | Unit | Why it matters | Cannot prove |
|---|---|---|---|---|---|
| U0 | matched LM-only backbone update | one restored AdamW step; SAE frozen | one update | control direction | long-run LM-only behavior |
| U1 | LM plus reconstruction backbone update | same state/batch plus \(\lambda=1\) reconstruction | one update | treatment direction | from-zero formation |
| local utility | post-update held-out readout change | P-report \(\mathrm{CE}(U0)-\mathrm{CE}(U1)\) | nats/example, class balanced | closest registered one-step benefit test | downstream task utility |
| B | between-class energy | mean squared distance of class means from their balanced center | representation squared norm | class-center separation | causal use |
| W | within-class energy | mean within-class squared deviation | representation squared norm | class compactness/scale | semantic quality |
| F | Fisher ratio | \(F=B/W\); parent-wise ratios averaged for fine labels | dimensionless | relative geometry | whether B or W caused change |
| h gradient | gradient at final-block pre-MLP SAE input | LM and reconstruction gradients separately | L2 norm/cosine | verifies local path | historical accumulation |
| same-ID angle | signed angle between one decoder column at 0B and later | all 30,000 columns, no absolute cosine | degrees | numeric direction change | semantic identity |
| N-report NLL | teacher-forced next-token loss on fixed academic rows | total loss sum / total valid targets | nats/valid token | local frozen prediction cost | general capability |

## 2. Anchor Link And Decision Point

The Anchor asks whether SAE-mediated training changes residual domain-readable organization and whether a live reconstruction gradient explains a useful formation mechanism. E01 established bounded representation differences but not causal use. E02 asks the smallest causal-direction question available without retraining: after an actual, optimizer-correct, isolated update, does adding reconstruction improve frozen held-out readability over LM alone?

The only next decision is whether the remaining from-zero mechanism question merits a separately matched C/T training design. E02 does not authorize it.

## 3. Protocol Freeze, Conformance, And Deviations

| Registered item | Expected | Actual | Status | Evidence | Eligibility impact |
|---|---|---|---|---|---|
| checkpoints | M0/M1/M2 0B, 10B, 15B as applicable | all manifests complete; 15B tokens `15,000,000,000`, optimizer step `57,224` | `PASS` | local parameter receipt | eligible |
| primary checkpoint | M2 10B | complete 4×U0/U1 | `PASS` | G0/G1 JSON | eligible |
| sensitivity | full M2 15B, reported separately | complete; not pooled with 10B | `PASS` | primary table | eligible |
| G1 reset | same model, optimizer, scheduler, RNG before each arm | eight trials/checkpoint, no chaining | `PASS` | runner and trial records | eligible |
| SAE freeze | all `sae.*` parameters and activity buffers unchanged | digest identical in 16/16 trials | `PASS` | trial records | eligible |
| objective | U0 LM; U1 LM + \(\lambda=1\) reconstruction; AuxK disabled | exact | `PASS` | runner | eligible |
| effective update batch | 8 rows × 256 valid targets = 2,048 | exact four fixed batches | `PASS` | registered sample IDs | eligible |
| uncertainty | 5,000 stratified paired draws | exact | `PASS` | analysis source and table | eligible |
| NLL normalization | total loss sum / valid-token sum | 400 rows, 102,400 targets per model/checkpoint | `PASS` | NLL source table | eligible |
| resource | amendment R001: one 4×H100 Reserved node | four H100s allocated and visible; frozen runner used `cuda:0` | `CONFORMING_WITH_EFFICIENCY_NOTE` | execution receipt | no scientific impact |
| Smoke | must pass before full | `pt-eweyxti7` passed | `PASS` | Smoke receipt/log | permits full |
| full | complete supervision to terminal state | `pt-d6swd6xd` `SUCCEEDED` | `PASS` | execution receipt | eligible |
| failed roots | no reuse | Spot unallocated; Smoke v1 and full v1 excluded; fresh v2 root | `PASS` | amendments and logs | eligible |
| result authority | AI must not invent human judgment | all verdicts marked awaiting confirmation | `PASS` | Summary/Detailed | no Anchor promotion |

Frozen Protocol revision: the scientific body plus append-only R001--R003 in [protocol.md](protocol.md).  
Execution scope approved: researcher explicitly authorized 4×H100 Reserved, completion of Smoke, and supervision of the full run to terminal state.  
Amendments: R001 replaced the never-started Spot profile; R002 supplied the source-required checkpoint dead-feature mask to G0; R003 made the frozen NLL calculation remain inside inference mode. R002/R003 were numerically/scientifically invariant engineering repairs.  
Retries and exclusions: `pt-vyrf07oi`, `pt-mwjknz0d`, and `pt-tthi96r1` are `INELIGIBLE`; no partial scientific artifact was reused.  
Missing required conditions: none.  
Post-hoc analysis: the reader summary and focused 10B B/W intervals materialize registered L1 quantities; they do not select a new endpoint or decision rule.

## 4. Actual Setup

- Data: P has 360 constructed sentences split by family into 120 fit, 60 tune, and 180 confirmation rows. N has 1,200 academic M2D2 rows split 600 fit, 200 tune, and 400 report rows. N is a development replication.
- Models: M0 Dense; M1 SAE-mediated with reconstruction input detached from the backbone; M2 SAE-mediated with live reconstruction gradient plus historical SAE-only AuxK. M1/M2 use an eight-layer, hidden-1024 backbone and a width-30,000 Top32 SAE before the final MLP.
- G0/G1 checkpoints: M2 at 10B and 15B.
- Readouts: fitted only on untouched-checkpoint fit rows, selected on tune rows, then frozen. P actual input is primary; P h and N h/actual are secondary.
- G0: four fixed N-fit batches; separate LM and reconstruction gradients at h and mutually exclusive backbone groups. Target and energy denominator remain detached.
- G1: one true AdamW step per isolated arm, restored checkpoint moments/scheduler/LR/weight decay/clipping; four batch pairs at each checkpoint. SAE-only AuxK is zeroed because the SAE is frozen.
- Frozen NLL: M0/M1/M2 at 10B and 15B on identical N-report input/target arrays.
- Read-only supplements: E01 caches for 0--10B, new 15B caches, physical checkpoint tensors, and all 30,000 decoder columns.
- Primary independence unit: P family within the frozen strata. Checkpoints and batch directions are not independent training replicates.
- Code: `/data/250010109/MoE_Router/experiments/20260916_sae_gradient_parameter_followup/scripts/`.
- Eligible result root: `/data/250010109/MoE_Router/experiments/20260916_sae_gradient_parameter_followup/runs/full_h100_4reserved_v2/`.

### Gradient ownership

| Objective | Backbone path | SAE parameters | Final-block MLP/output | Target/denominator | E02 handling |
|---|---|---|---|---|---|
| LM | through mediated main forward | historically trainable; frozen in G1 | yes | token targets fixed | U0 and U1 |
| reconstruction | M2 only, through h and earlier backbone | historically trainable; frozen in G1 | no direct path through the downstream final MLP; tied embedding receives input-side gradient | detached | U1 only |
| AuxK | no backbone path in the registered topology | SAE only | no | checkpoint dead mask | disabled in both frozen-SAE arms |

FVU becoming smaller cannot establish better semantics because reconstruction accuracy does not say whether class-relevant information became more accessible or functionally used. A current gradient is an instantaneous derivative at one checkpoint; it is not the optimizer-integrated historical parameter trajectory.

## 5. Metrics And Registered Decision Rules

Primary metric:

\[
\Delta_{\mathrm{local}} = \operatorname{CE}_{P,\mathrm{report}}(U0)-\operatorname{CE}_{P,\mathrm{report}}(U1).
\]

The per-example CE is averaged across the four batch directions and then class balanced. A 5,000-draw family/class-stratified paired percentile interval entirely above zero supports U1. An interval crossing zero is `NOT_SUPPORTED`; without a registered equivalence margin it is not equivalence. The 15B checkpoint is a separate sensitivity and cannot alter the 10B primary verdict.

Secondary metrics are P/N balanced accuracy, h/actual B/W/F, post-update N NLL, parameter-group update norms, G0 gradient norms/cosines/support, historical parameter displacement, same-ID decoder angles, and frozen N-report NLL. None can rescue a failed primary rule.

## 6. Evidence Lineage

| Claim or decision | Protocol criterion | Raw artifact | Computation | Aggregation / uncertainty | Observed value | Eligibility | Verdict | Limitation |
|---|---|---|---|---|---|---|---|---|
| 10B local utility | primary interval above 0 | `gradient_and_local_utility.json` | frozen readout CE U0−U1 | four directions; 5,000 paired draws | `−0.000622 [−0.001691, 0.000400]` | `ELIGIBLE` | `NOT_SUPPORTED` | one step, one checkpoint trajectory |
| 15B sensitivity | separate interval above 0 | same | same | separate 5,000 draws | `−0.000571 [−0.001664, 0.000564]` | `ELIGIBLE` | `NOT_SUPPORTED` | cannot rescue 10B |
| path support | finite, selected positions only | eight G0 records | LM/reconstruction autograd | four batches/checkpoint | outside-position max `0.0` in 8/8 | `ELIGIBLE` | `PASS` | local derivative only |
| update integrity | 16 isolated updates, unchanged SAE | 16 trial records | state digests and before/after deltas | exact count | 16/16 complete and unchanged | `ELIGIBLE` | `PASS` | no multi-step trajectory |
| Fisher decomposition | report B/W/F and paired key differences | 21 caches | class-balanced B/W; parent-wise F | focused 10B and full 15B paired draws | M1−M0 B and W both positive at 10B/15B | `ELIGIBLE` | descriptive mechanism boundary | scale-sensitive energies |
| historical displacement | physical tensors; common-init normalization | parameter CSVs | deduplicated norms | all registered groups | M2−M1 `1.4503` at 10B, `1.6332` at 15B | `ELIGIBLE` | descriptive | not single-loss attribution |
| dictionary rotation | all 30,000 signed same-ID columns | decoder CSV | signed cosine/angle quantiles | complete columns | median `84.73°--86.53°` | `ELIGIBLE` | descriptive | no semantic identity |
| frozen local performance | token-weighted NLL differences | NLL rows | loss sums / valid counts | row/category paired bootstrap | 15B M2−M1 `+0.00625 [0.000079, 0.01384]` | `ELIGIBLE_BOUNDED` | local cost on N | development panel only |

## 7. Main Results

### Eligible decision evidence

The primary table is [primary_local_utility.csv](tables/primary_local_utility.csv). At 10B, two batch directions favor each arm; at 15B, one favors U1 and three favor U0. Both paired intervals cross zero. This meets the registered `NOT_SUPPORTED` branch, not a harm or equivalence branch.

The G0 h-gradient ratio is `0.0827--0.1006` at 10B and `0.0345--0.0557` at 15B. Its cosine with the LM gradient stays close to zero on these batches. Parameter-group reconstruction gradients are nonzero upstream of h; the final block MLP and final norm have zero direct reconstruction gradient, as expected from the injection point. U1−U0 actual increment differences are nonzero in upstream groups, verifying that AdamW transforms the added signal into a distinct update.

### Bounded representation decomposition

At 10B P actual/raw, M1−M0 B, W, and F are all positive with paired intervals above zero. At 15B the pattern remains. The B3 transform gives the same qualitative result. Therefore the E01 Fisher-ratio increase is not caused by tighter within-class clusters; both between- and within-class energies increase, with B increasing sufficiently relative to W.

For M2−M1 at 10B and 15B, B, W, and F are all lower on P actual/raw and B3. This does not supply the missing M2 local-utility evidence and cannot be interpreted as better compression or worse semantics by itself.

### Parameter and dictionary supplements

| Object | 10B relative displacement | 15B relative displacement |
|---|---:|---:|
| M0 backbone / init | 1.8104 | 1.7302 |
| M1 backbone / init | 1.6773 | 1.6893 |
| M1 SAE / init | 2.2343 | 2.6106 |
| M2 backbone / init | 1.7814 | 1.7445 |
| M2 SAE / init | 2.2627 | 2.6531 |
| M2−M1 shared backbone / common 0B norm | 1.4503 | 1.6332 |

All values are physical tensor norms with the tied embedding/output counted once and SAE separated. A large value measures numeric displacement, not semantic or functional benefit.

The same-ID decoder-column median angles from 0B are M1 `84.73°` and M2 `85.37°` at 10B, increasing to `86.13°` and `86.53°` at 15B. No column is zero at either endpoint. These observations show substantial numeric rotation and make stable-ID semantic reading less, not more, justified.

### Performance supplement

The existing 15B training plot is provenance-qualified: 25M-token interpolation, a 200-update trailing arithmetic mean, and millinats/token deltas. At 15B it reports M1/Dense `−8.252` and M2/Dense `−9.286` millinats on training logs. It is descriptive and not held-out evaluation.

On the fixed frozen N-report panel, M2−M1 is `−0.00263 [−0.00920, 0.00536]` at 10B and `+0.00625 [0.000079, 0.01384]` at 15B nats/valid token. The 15B positive value means M2 is worse than M1 on this panel under the registered sign convention. N is a development replication, the lower bound is close to zero, and no general-capability conclusion follows.

### Evidence matrix

The compact requested matrix is [evidence_matrix.csv](tables/evidence_matrix.csv). Unmeasured and out-of-scope items remain: unlabeled clustering, feature semantic naming, cross-model ID mapping, general benchmarks, new DCLM held-out evaluation, multiple training seeds, functional ablation, and matched-from-zero C/T training.

### Ineligible and debug evidence

- The never-started Spot job has no scientific evidence.
- Reserved Smoke v1 and full v1 logs establish two implementation failures only.
- Smoke v2 is runtime/guard evidence, not a scientific effect estimate.
- Local regression outputs certify numerical/call-contract repairs only.

## 8. Visualization Result

### One-step local utility at 10B and 15B

![One-step local utility](figures/primary_local_utility.png)

Purpose: show the only decision-bearing contrast and its uncertainty.  
Metric: class-balanced P-report CE(U0)−CE(U1), nats; positive favors U1.  
Source: [primary_local_utility.csv](tables/primary_local_utility.csv), lineage rows 1--2.  
Aggregation: four fixed update directions and 5,000 family/class-stratified paired bootstrap draws.  
Observed result: both point estimates are negative and both intervals cross zero.  
Take-home: neither 10B nor 15B supports one-step U1 benefit.  
Cannot prove: equivalence, harm, long-run training behavior, or downstream functional effect.

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | Status | Failure reason | What this rules out | What remains live |
|---|---|---|---|---|---|
| S0 | manifests and hashes | `PASS` | none | checkpoint identity mismatch | historical confounding |
| S1 | local L2/L3, syntax and call regressions | `PASS` | two excluded pre-full bugs repaired | missing physical tensors | semantic meaning of displacement |
| S2 | fresh Reserved Smoke v2 | `PASS` | Smoke v1 omitted required mask | runtime/freeze/support failure | full-matrix outcome |
| S3 | caches and NLL rows | `PASS` | full v1 inference-context bug excluded | missing 15B/NLL evidence | panel generality |
| S4 | 8 G0 batches | `PASS` | none | absent backbone path; off-support gradient | usefulness of path |
| S5 | 16 isolated G1 updates | `PASS` | none | missing arms or SAE drift | multi-step/from-zero effect |
| S6 | synthesis and reader artifacts | `PASS` | none | missing registered summaries | human scientific judgment |

Falsified implementation rivals: absent reconstruction-to-backbone gradient, off-support reconstruction gradient, changed SAE state, missing optimizer restoration, and incomplete pair matrix.  
Not falsified: the reconstruction direction may require long-horizon accumulation, other batches, matched from-zero training, or a different functional outcome. These possibilities cannot rescue the present one-step primary result.

## 10. Full Experiment Record

1. Question: does adding the registered reconstruction gradient to one optimizer-correct M2 update improve held-out P readability relative to LM-only, and do 15B/read-only supplements change the evidence boundary?
2. Setup: M2 10B primary plus 15B sensitivity; U0/U1 matched except the reconstruction term; frozen SAE; four restored batch pairs; M0/M1/M2 frozen NLL; read-only checkpoint audits.
3. Training data: four fixed N-fit batches, 8 rows × 256 valid targets per update. This is a local intervention, not a new training run.
4. Testing data: P confirmation is primary; N report is a development replication. Frozen readouts use fit/tune only.
5. Result: eligible full matrix; primary and sensitivity both `NOT_SUPPORTED`; all supplements complete. Sources are the tables linked above and the execution workspace manifest.
6. Insight and boundary: local gradient existence is separated from local utility. Historical geometry, parameter displacement, and dictionary rotation remain descriptive. The remaining causal formation question needs matched from-zero evidence.

## 11. Interpretation

The strongest result is negative in the precise registered sense: the added reconstruction direction is physically present and produces a measurably different AdamW update, but it does not yield a detectable improvement in the frozen P readout after one step. That removes a simple version of the mechanism—“the current reconstruction gradient is immediately better for readable domain structure”—without establishing that long-run reconstruction training is useless.

The L1 decomposition also changes the interpretation of E01. M1's higher Fisher ratio is not a compression-only story: absolute within-class scatter rises substantially while between-class energy rises more. The representation scale and organization both change. L2/L3 show large historical numeric movement, but the original histories differ in more than the live/detached switch, so those measurements cannot identify a cause.

## 12. Claim Boundary

Can claim:

- the reconstruction gradient reaches the M2 backbone with correct position support at 10B and 15B;
- it creates a distinct one-step backbone update under restored AdamW state;
- the registered one-step P-report benefit is not supported at either checkpoint;
- B/W/F, physical displacement, same-ID decoder rotation, and frozen N-report NLL through 15B are complete and eligible within their stated panels.

Cannot claim:

- U1 is harmful or equivalent to U0;
- the gradient is ineffective over many updates or from initialization;
- historical M2−M1 differences were caused by reconstruction-to-backbone flow alone;
- SAE feature IDs preserve semantics over time or across models;
- any model has generally better language ability or downstream utility;
- the original “easier formation from scratch” mechanism has been established.

## 13. Next Decision

Decision: researcher confirms or corrects the `NOT_SUPPORTED` local verdict and decides whether the remaining from-zero question justifies a separately frozen matched C/T training design.  
Completion criterion: a proposed design fixes token budget, data order, effective global batch, optimizer/schedule, SAE capacity, multiple seeds, held-out functional primary metric, and stopping rule before submission.  
Stop/redirect: if those matching conditions or the budget cannot be guaranteed, stop using current local/history evidence to pursue the causal formation claim.  
Resume action: begin from this Detailed record and the Anchor; do not reuse a failed job root or expand E02 post hoc.

## 14. Artifact Manifest

| Artifact | Purpose | Producer | Source inputs | Identity | Complete | Claim-eligible | Notes |
|---|---|---|---|---|---|---|---|
| [protocol.md](protocol.md) | frozen contract | experiment-card workflow | prompt and approved amendments | R001--R003 | yes | yes | execution owner |
| [execution_receipt.md](execution_receipt.md) | resource/run history | monitored ACP workflow | job states, logs, receipts | `pt-d6swd6xd` | yes | yes | failed roots separated |
| `gradient_and_local_utility.json` | raw G0/G1 evidence | GPU runner | M2 10B/15B | SHA-256 `752ba5...9ad` | yes | yes | 8 G0, 16 G1 |
| `n_report_nll_rows.csv` | per-row frozen loss sums/counts | GPU runner | M0/M1/M2 10B/15B | eligible v2 root | yes | yes | 2,400 model/checkpoint rows |
| synthesis outputs | Fisher/NLL intervals | registered CPU analyzer | 21 caches and NLL rows | receipt `PASS` | yes | yes | 5,000 draws |
| local L2/L3 CSVs | parameter/dictionary audit | local parameter analyzer | nine checkpoint states | receipt `PASS`, 720.90 s | yes | yes | buffers excluded |
| [reader_artifact_manifest.json](reader_artifact_manifest.json) | curated table/figure hashes | materializer | eligible raw outputs | status `PASS` | yes | yes | 9 tables, 1 figure |
| 15B training context JSON | training-loss provenance | prior approved reader artifact | three metrics streams | target 15B | yes | bounded | descriptive training logs only |

## 15. Links

- Anchor: [A15_17](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/15_17_three_model_sae_representation_trajectory_anchor.md)
- Protocol: [protocol.md](protocol.md)
- Summary: [summary.md](summary.md), [summary_cn.md](summary_cn.md)
- Execution root: `/data/250010109/MoE_Router/experiments/20260916_sae_gradient_parameter_followup/`
- Runner: `/data/250010109/MoE_Router/experiments/20260916_sae_gradient_parameter_followup/scripts/run_gpu_followup.py`
- Local analyzer: `/data/250010109/MoE_Router/experiments/20260916_sae_gradient_parameter_followup/scripts/audit_parameters.py`
- Synthesis: `/data/250010109/MoE_Router/experiments/20260916_sae_gradient_parameter_followup/scripts/analyze_supplements.py`
- Eligible result directory: `/data/250010109/MoE_Router/experiments/20260916_sae_gradient_parameter_followup/runs/full_h100_4reserved_v2/`
- Persistent full log: `/data/250010109/MoE_Router/experiments/20260916_sae_gradient_parameter_followup/acp_receipts/pod/sae-grad-followup-0916-h1004-full-v2-20260916T072803Z.log`
- Job IDs: Smoke `pt-eweyxti7`; full `pt-d6swd6xd`; excluded full v1 `pt-tthi96r1`.
