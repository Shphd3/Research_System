派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_24_frequency_composition_common_path/common_optimizer_coupling_20261022/detailed.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_24_frequency_composition_common_path/common_optimizer_coupling_20261022/detailed.md)；研究修改仍回到原件。

---

# Detailed: common-gradient coupling through global clipping

[中文](detailed_cn.md) · [Summary](summary.md) · [Protocol](protocol.md) · [Artifact manifest](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_24_frequency_composition_common_path/common_optimizer_coupling_20261022/artifact_manifest.json)

Primary owner: [A15_24_01](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_24_frequency_composition_common_path/subanchors/15_24_01_common_optimizer_coupling_anchor.md). Four of four planned models completed, with 168 updates and 85,548 valid targets each. Qualification and independent result audits passed. Evidence is eligible for the registered **exploratory** policy comparison. Low-feature macro changes are -0.000332028 and +0.000529222: the two-seed improvement rule is not met. Researcher mechanism judgment and scientific closure remain Unknown.

## 1. Question, objects and actual comparison

The parent experiment added an always-on common expert while retaining both frequency-routed experts. It increased global clipping frequency without stable low-feature improvement. This round investigates the optimizer coupling caused by the clipping denominator. It complements the separate feature-relation/frozen-representation investigation: no input, feature group, route or architecture changes here.

A valid training position is a cached answer-prediction hidden vector and its original next-token target. The frozen Qwen3-0.6B block-28 hidden state is 1,024-dimensional BF16. Eight bias-free width-1,024 SwiGLU experts use the saved T_F top-2 route, weights 0.5/0.5. The ninth common expert is always active with coefficient one. Each reads the same full hidden state divided by the original TRAIN RMS scale. Their scaled residual output is added back before the frozen final norm/head. Only these nine modules train; T_F has no trainable router.

The control clips all raw gradients by one global factor. The treatment calculates the routed factor using only routed gradients while retaining the original global factor for common. This holds architecture and capacity constant. Later common learning may differ because the full trajectories separate; only the same-state shadow comparison holds common's update exactly fixed.

The hypothesized outcome was lower final low-feature macro NLL in both seeds. Its strongest rival is that AdamW absorbs gradient scaling or that the resulting trajectory change does not improve prediction. The experiment estimates the total effect of the specified policy, not complete mediation of the original baseline/common contrast.

## 2. How clipping enters AdamW

After accumulating one complete effective batch, let \(g_R\) denote the concatenated routed parameter gradients and \(g_C\) common gradients. Both are raw, before clipping. With threshold one,

\[
q=\min\{1,1/(\sqrt{\lVert g_R\rVert^2+\lVert g_C\rVert^2}+10^{-6})\},\qquad
r=\min\{1,1/(\lVert g_R\rVert+10^{-6})\}.
\]

Control sends \((qg_R,qg_C)\) into AdamW; treatment sends \((rg_R,qg_C)\). Norms are calculated before either gradient is modified. The stabilizer 1e-6 belongs to clipping. AdamW epsilon is separately 1e-8.

For one parameter coordinate with raw gradient \(g_t\), clipping factor \(c_t\), learning rate \(\eta_t\), first/second moment states \(m_t,v_t\), and weight decay \(\lambda\), the update is

\[
m_t=0.9m_{t-1}+0.1c_tg_t,\quad
v_t=0.95v_{t-1}+0.05c_t^2g_t^2,\quad
\Delta\theta_t=-\eta_t\frac{\widehat m_t}{\sqrt{\widehat v_t}+10^{-8}}-\eta_t\lambda\theta_{t-1}.
\]

Hats denote the usual bias corrections. A common positive scalar preserves a current raw gradient's direction. It need not preserve the direction after moment accumulation and coordinatewise normalization. At the first zero-moment step, the adaptive term reduces to \(-\eta_1c_1g_1/(|c_1g_1|+10^{-8})\), giving near scale cancellation away from near-zero coordinates. Actual measured parameter movement also includes weight decay and rounding.

At pre-update steps 1/42/84/126/168, the implementation clones parameters, Adam state and raw accumulated gradients. It computes both policies without an extra backward pass and retains the chosen policy for the real update. The records contain each update norm, their difference norm divided by the global update norm, cosine and common-update equality. No additional targets enter the progress counter.

**Measured example, seed 11 global trajectory, step 42:** the original factor is 0.774878294; the routed-only factor is 1. Global and isolated routed update norms are 0.354099235 and 0.364755159, a 3.0093% norm increase. Their difference vector has norm 0.035335699, or 9.9790% of the global update; cosine is 0.995605965, angle 5.3731 degrees. Common's update is exactly equal. These percentages describe distinct quantities and should not be interchanged. [Raw step record](../../../../../../../../UNAVAILABLE.md)

## 3. Registered setup and qualification

| Item | Actual setting and evidence |
|---|---|
| Freeze | 2026-10-22 23:35:06 Asia/Shanghai (15:35:06 UTC); [freeze hashes](../../../../../../../../UNAVAILABLE.md) |
| Scope | User-authorized autonomous distinct mechanism analysis; four local T_F plus-common models; no remote submission |
| Data | Tulu revision 6248b175d2ccb5ec7c4aeb22e6d8ee3b21b2c752; TRAIN 1,024 dialogues/85,548 targets, EVAL 256/22,446, DEV 128/10,340 |
| Labels | Answer-only next-token targets including EOS; zero prompt/padding targets; normalized prompt overlap zero; near-duplicate/Base-pretraining independence Unknown |
| Features | Same 14-layer, 16,384-feature CrossCoder; threshold 0.051281172782182693; original frozen bands/routes |
| Model | Nine width-1,024 SwiGLUs, 28,311,552 trainable parameters; frozen Base/dictionary/head; no router, auxiliary loss or dropping |
| Objective | Valid-target cross entropy, sum over microbatches divided by actual effective-batch targets |
| Optimization | AdamW 3e-4, betas .9/.95, eps 1e-8, weight decay .01; inherited nine-step warmup and cosine final ratio .1 |
| Exposure | Microbatch 128, effective batch 512, final batch 44; 168 updates and 85,548 targets per model |
| Conditions | global and route_isolated, each seeds 11 and 22; original shared initialization and order |
| Checkpoints | Initial complete state, complete states at 1/42/84/126/168; final_resumable.pt hard-links step168; no best-checkpoint selection |
| Evaluation | TRAIN/EVAL at 0/42/84/126/168; DEV only after all four endpoints; fixed final168 |
| Device | Existing local NVIDIA H100 80GB HBM3 MIG 3g.40gb; torch 2.3.0a0+6ddf5cf85e.nv24.04; two CPU threads |
| Resources | Summed process active time 307.246 seconds against 1,200-second ceiling; no failed invocation; each train procedure approximately 65.6–66.3 seconds |

[Dataset guide](dataset_guide.md) binds each split JSON, target construction, label supports and source identity. Required input IDs are recorded in [config](../../../../../../../../UNAVAILABLE.md); [current access](../../../../../../../../UNAVAILABLE.md) precedes loading. Source, config and Protocol hashes are fixed. The old frozen-cache model, evaluator and schedule were reused; clipping, complete milestone saves and shadow measurements were adapted.

[Qualification](../../../../../../../../UNAVAILABLE.md) passed source-equivalent global updates, no-common policy equality, exact common shadow updates, label checks, both-policy next-update model/optimizer/metric resume equality, finite required TensorBoard tags and token counts 512/1024. Shadow observations do not replace the endpoint test.

## 4. Conformance, deviations and evidence eligibility

| Registered item | Actual check | Status and impact |
|---|---|---|
| Four same-environment runs | All four completed with fixed config and source hashes | PASS; within-round contrast eligible |
| Same budget and routes | Every arm has 168 updates/85,548 targets; per-step routed exposure equal between policies | PASS; no exposure confound |
| Valid labels and frozen components | Source/label/freeze checks passed | PASS |
| Twenty fixed-state comparisons | Four runs × five registered steps; common updates exactly equal; zero extra backward calls | PASS; immediate optimizer contrasts eligible |
| Endpoint aggregation | Independent audit recomputed from DEV NLL arrays and original feature CSR without importing the trainer; paired CSV error zero | PASS |
| Historical replay | Initial TRAIN/EVAL arrays equal; trained old/new global arrays differ | BOUNDED historical comparison; no old/new pooling |
| Save contract | Complete rather than weights-only intermediate states, plus step1 | Declared pre-start; strengthens recoverability without changing learning |
| Draft language in registered body | Final appended freeze receipt supersedes earlier pending wording; separate qualification receipt records later PASS | Administrative chronology preserved; no post-result rewrite |
| Failures, retries, exclusions | Six completed invocations: qualification, four workers, final evaluation; no omitted seed or outcome-driven checkpoint | None in this execution |

DEV remains exposed, two seeds are exploratory, and no low feature has at least 20 DEV hits. These sampling limits apply even though the numerical comparison is qualified. No independent confirmation set was used. The independent audit, not a job-status label, supports completeness and metric eligibility. [Audit](../../../../../../../../UNAVAILABLE.md)

## 5. Metrics, endpoints and trajectories

Low-feature macro NLL averages each supported feature's active-position losses, then averages equally across 838 supported B1 features. The original pool has 1,694, with 856 unsupported. Overall NLL averages all 10,340 DEV positions; low-union averages 1,701 unique positions. Feature events overlap; two seeds are the training repeats. There is no significance claim or feature-as-independent-sample inference.

The primary sign rule was fixed before final DEV: both isolated-minus-global differences negative supports the policy exploratorily; mixed directions are inconsistent with stable improvement; both nonnegative do not support; invalid/missing pairs are insufficient. The actual outcome is **mixed**, not an execution failure.

| Policy | Seed | DEV overall | DEV low macro | DEV low union | DEV high macro |
|---|---:|---:|---:|---:|---:|
| Global | 11 | 1.226603156 | 1.056352688 | 1.063884757 | 1.192203082 |
| Isolated | 11 | 1.226504336 | 1.056020660 | 1.064022403 | 1.192145080 |
| Global | 22 | 1.227334069 | 1.057152509 | 1.063403929 | 1.192921787 |
| Isolated | 22 | 1.227341095 | 1.057681732 | 1.063815882 | 1.192944507 |

| Seed | Delta overall | Delta low macro | Delta low union |
|---|---:|---:|---:|
| 11 | -0.000098819364 | -0.000332028097 | +0.000137646481 |
| 22 | +0.000007025948 | +0.000529222412 | +0.000411952484 |
| Mean | -0.000045896708 | +0.000098597157 | +0.000274799482 |

[Condition results](../../../../../../../../UNAVAILABLE.md) and [paired comparisons](../../../../../../../../UNAVAILABLE.md) are the decisive tables. There were 5,027/4,934/379 improved/worse/equal DEV positions for seed 11 and 4,830/5,109/401 for seed 22. These counts describe heterogeneity; they are not independent trials or new success criteria.

| Policy | Seed | Final TRAIN overall | Final EVAL overall | Routed clipped steps | Routed cumulative path |
|---|---:|---:|---:|---:|---:|
| Global | 11 | 0.897871470 | 1.221650079 | 161 | 37.528428 |
| Isolated | 11 | 0.900642155 | 1.221437095 | 21 | 36.521194 |
| Global | 22 | 0.900176130 | 1.220305537 | 160 | 37.460139 |
| Isolated | 22 | 0.902447295 | 1.220278808 | 18 | 36.499159 |

The complete trajectories are retained at five milestones under each condition's `metrics_step*.json`, `train_step*.npz` and `eval_step*.npz`. The cumulative routed path sums the joint eight-expert parameter-update norm over steps. It excludes common and any router, and is not net displacement. It decreased 2.6839%/2.5653% in the treatment despite less clipping. Immediate shadow effects and complete-trajectory effects condition on different histories, so this is not a contradiction.

## 6. Fixed-state update results and historical evidence

The table reports shadow isolated/global norm ratio, relative vector difference and angle on each actual trajectory. A ratio near one does not imply equal vectors. Common updates were exactly equal in every row.

| Actual policy | Seed | Step | Update norm ratio | Relative vector difference | Angle, degrees |
|---|---:|---:|---:|---:|---:|
| Global | 11 | 1 | 1.000362 | 0.002778 | 0.158 |
| Global | 11 | 42 | 1.030093 | 0.099790 | 5.373 |
| Global | 11 | 84 | 1.013573 | 0.042859 | 2.314 |
| Global | 11 | 126 | 1.000000 | 0.000000 | 0.000 |
| Global | 11 | 168 | 1.045434 | 0.156135 | 8.378 |
| Global | 22 | 1 | 1.000320 | 0.002466 | 0.140 |
| Global | 22 | 42 | 1.028893 | 0.097240 | 5.246 |
| Global | 22 | 84 | 1.012151 | 0.037086 | 1.996 |
| Global | 22 | 126 | 1.010867 | 0.030312 | 1.613 |
| Global | 22 | 168 | 1.051217 | 0.157107 | 8.307 |
| Isolated | 11 | 1 | 1.000362 | 0.002778 | 0.158 |
| Isolated | 11 | 42 | 1.022951 | 0.087289 | 4.772 |
| Isolated | 11 | 84 | 1.011998 | 0.040574 | 2.208 |
| Isolated | 11 | 126 | 1.000000 | 0.000000 | 0.000 |
| Isolated | 11 | 168 | 1.042663 | 0.151151 | 8.143 |
| Isolated | 22 | 1 | 1.000320 | 0.002466 | 0.140 |
| Isolated | 22 | 42 | 1.022927 | 0.086841 | 4.746 |
| Isolated | 22 | 84 | 1.011336 | 0.035623 | 1.924 |
| Isolated | 22 | 126 | 1.010515 | 0.030095 | 1.607 |
| Isolated | 22 | 168 | 1.047938 | 0.152017 | 8.081 |

Step168 uses the registered final batch of 44 rather than 512 targets; its larger contrast is not a clean temporal increase. These five batches are fixed diagnostic points, not an estimated distribution of all update effects. The independent audit retains exact values and source hashes.

Historical observations were known before intervention registration. Across old MoE/T_F and seeds 11/22, adding common increased routed path length by 1.9560%, 1.9162%, 2.3090%, 2.1547%, respectively. First-step clip ratios were 0.576727/0.602401/0.562662/0.598823; actual update norm ratios were 0.999579/0.999589/0.999639/0.999680. Only raw-gradient norms, not gradient vectors, were logged. This contradicts a simple decrease in overall movement, not all possible optimization mechanisms. [Historical source audit](../../../../../../../../UNAVAILABLE.md)

New-minus-old global DEV low-feature macro differences are approximately -0.0005581/-0.0006180, comparable to the intervention effects. The historical controls therefore cannot be substituted for this round's locally rerun controls. The experiment does not identify the exact cause of cross-environment numerical divergence.

## 7. Three compact audits and evidence lineage

**Research identification audit — PASS within the bounded claim.** Architecture, capacity, frequency groups, sample order and exposure are held fixed. The immediate shadow comparison changes only the routed coefficient and preserves common's update. Full retraining then measures feedback through changed future states. The policy effect is identified within this setting; complete mediation, feature semantics and Rank-one claims are outside the comparison.

**Data/statistics audit — PASS for exploratory metrics.** Original split/labels and target counts are verified. Independent recomputation from raw NLL plus original feature CSR matches the published differences exactly. Unsupported features remain unsupported; repeated feature events are not independent. DEV exposure, sparse supports and two seeds limit generalization. No outcome-selected exclusions, bins or checkpoints occurred.

**Implementation/numerics audit — PASS.** Unchanged global updates and no-common equality were checked; both-policy resume model/optimizer/metric equality, frozen head, counters, finite TensorBoard tags and all twenty common shadow equalities passed. All four complete records bind the frozen worker/config. Old/new post-training equality failed as anticipated as a possible cross-environment limit; it is preserved and does not invalidate same-environment policy pairs. [Independent audit](../../../../../../../../UNAVAILABLE.md)

| Claim | Raw evidence and computation | Observation | Eligibility / boundary |
|---|---|---|---|
| Stable low-feature gain | Four DEV `.npz` files + original CSR; worker metric_bundle and independent bincount audit | -0.000332028 / +0.000529222 | ELIGIBLE exploratory; mixed criterion |
| Denominator changes Adam | Same-state shadows in 4 × steps.jsonl | Step42 seed11 relative vector difference 9.979%; common identical | ELIGIBLE immediate optimizer effect |
| Less clipping need not mean longer movement | Sum logged route_update_norm over 168 steps | Paths decrease 2.6839%/2.5653% | ELIGIBLE descriptive trajectory; movement is not utility |
| Old simple shrinking account | Original eight complete logs, independently aggregated | All four old common paths longer | BOUNDED observational evidence; trajectories differ |
| Completion/engineering | Qualification, four complete.json, final receipt, independent audit | All planned conditions and counters present | Engineering PASS, not scientific closure |

Actual outputs are registered in seven assets: two qualification states, four complete checkpoint families and one analysis asset. All seven passed current strict access checks; all four final model/Adam tensor digests passed an independent CPU check. The run stores 26 independent checkpoint files, 7.433 GiB total at registration, counting final/step168 hard links once. Full registration identity and current access evidence are in [registration receipt](../../../../../../../../UNAVAILABLE.md) and the artifact manifest. Availability, exact resume qualification and scientific utility remain separate.

## 8. Interpretation, coverage and next decision

Direct observations establish a real clipping-to-Adam effect with mixed prediction consequences. **AI interpretation:** the simple explanation that common suppresses routed learning by reducing total Adam movement is weakened; removing its denominator contribution is not a stable remedy in this experiment. The result leaves functional sharing, representation organization, coordinate-specific learning and other optimizer interactions unresolved. It cannot settle the advisor's Rank-one intuition or ordinary-MoE behavior.

| Requested work | Status | Evidence |
|---|---|---|
| Distinct mechanism subproblem | DONE_EXPLORATORY | A15_24_01 and frozen policy comparison |
| Historical observation audit | DONE_VALID | Original eight logs and saved_step_analysis.json |
| Four complete trainings | DONE_VALID | Four complete.json, 168 steps each |
| Twenty same-state comparisons | DONE_VALID | Steps 1/42/84/126/168; common equality 20/20 |
| Endpoint prediction comparison | DONE_EXPLORATORY | Two seed deltas, raw arrays, independent audit |
| Scientific mechanism judgment / closure | Unknown | Researcher-owned review, not inferred from execution |

The single researcher-owned next decision is **Unknown**: whether the measured mixed result justifies continuing this clipping policy. No additional training follows automatically. The exact unresolved bridge is from a demonstrable local optimizer effect to a reproducible predictive benefit. Input assets, actual output-registration status, source/config hashes, logs, checkpoints, analysis revision and their purposes are recorded in [artifact_manifest.json](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_24_frequency_composition_common_path/common_optimizer_coupling_20261022/artifact_manifest.json). No scientific figure is required to read this result; the source tables carry the decisive comparisons.
