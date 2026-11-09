# Protocol: A15_17_E05 0--10B Sidecar-SAE Regularization Measurement

## 0. Approval Snapshot

Document status: `APPROVED_ACTIVE_EXACT_10B`  
Approval status: on 2026-09-18 the researcher confirmed that all five exact 10B checkpoints are available and explicitly requested the overall measurement, a 4xRTX5090 Spot Smoke, and pass-gated full execution  
Block audit status: A--G `CONFIRMED`  
Cross-block consistency: `PASS`  
Execution scope approved: one `5090-4-spot` read-only Smoke followed only after audited PASS by one same-profile full run; no optimizer, checkpoint mutation, fallback profile, commit, push, or publication  
Design frozen at: `2026-09-18T04:26:00Z`, before the resumed exact-10B Smoke produces data  
Purpose: determine whether an SAE sidecar used only as a training regularizer changes representation separability and token-aligned language-model training loss  
Primary Anchor: [A15_17](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/15_17_three_model_sae_representation_trajectory_anchor.md)  
Experiment role: read-only frozen-checkpoint trajectory measurement  
Primary checkpoints: exact physical checkpoints at `0/0.5/1/3/5/10B` for M0/M2/S7/S37/SALL  
Primary datasets: frozen synthetic panel P and frozen academic M2D2 panel N, reported separately  
Primary representation outcome: class-balanced Fisher geometry together with held-out linear and two-layer neural-probe balanced accuracy  
Primary optimization outcome: token-aligned language-model negative log-likelihood; perplexity is derived as `exp(NLL)`  
Cannot claim: causal benefit from one seed and unmatched trained trajectories, native use of sidecar reconstructions, increased parameter capacity, semantic feature identity, or general downstream capability  

The completed E03 evidence remains unchanged and is read first through
[summary_cn.md](../A15_17_E03_sidecar_representation_gradient_audit/summary_cn.md).
This E05 protocol does not retroactively change E03. Its authorization is limited to the read-only scope and profile recorded above.

## 1. Plain-Language Scientific Contract

### Purpose

Check whether making raw Attention outputs easier for sparse autoencoders to reconstruct acts as a useful training regularizer: does the native language-model representation become more separable, and does the model reach a lower language-model loss at the same number of training tokens?

### Hypothesis

If the sidecar reconstruction pressure usefully reorganizes the backbone, sidecar models should show stronger held-out class separation than the Dense reference across training checkpoints. A useful change should not appear only as a larger Fisher ratio: it should also be visible in a held-out probe, survive direct removal of the largest uncentered singular direction, and not coincide with worse token-aligned language-model loss.

The strongest rivals are:

1. Fisher rises only because within-class variance contracts.
2. One dominant uncentered direction creates the apparent separation.
3. A linear probe misses nonlinear accessibility, or a neural probe overfits the small panel.
4. Near-90-degree gradient angles are ordinary high-dimensional random geometry.
5. Apparent training improvement comes from unmatched models, missing token bins, or a duplicated baseline label.

### Analysis Method

1. Follow the same frozen examples from 0 to 10B and compare raw and direct-top-direction-removed representations with Fisher, a linear probe, and a fixed two-layer neural probe.
2. Put language-model loss, reconstruction-only loss, their ratio, gradient norms, gradient ratios, and gradient angles on the same token axis; compare angles with dimension-matched random references.
3. Track which SAE features are active, retained, newly active, or no longer active between adjacent checkpoints, without treating feature IDs as semantic labels or matching IDs across independently trained models.

### Pre-Registered Reading Branches

- **Representation support:** Fisher and held-out probe accessibility improve together at the common exact five-model 10B endpoint and the effect survives direct uncentered top-direction removal. A claim covering both datasets requires the pattern on both P and N; otherwise only a dataset-specific statement is allowed.
- **Geometry only:** Fisher changes but both held-out probes do not improve. Report a geometric reorganization, not better representation quality.
- **Training only:** token-aligned language-model loss improves but separability does not. Report an optimization observation without the proposed separability mechanism.
- **Non-support:** neither accessibility nor token-aligned loss shows the registered pattern.
- **Insufficient:** an exact checkpoint, identity, split, fit-only transform, probe-convergence, source-loss, gradient-support, random-null, or artifact-completeness guard fails.

## 2. Conditions And Naming

`M0` is the Dense baseline. The phrase “Dense baseline” does not create a second condition unless a distinct checkpoint manifest is supplied before unsealing.

| Condition | Exact meaning | Role |
| --- | --- | --- |
| M0 | eight-layer Dense language model | common native-representation and loss reference |
| M2 | final bottleneck SAE model with live reconstruction-to-backbone gradient and SAE-only AuxK | prior mediated-SAE comparison |
| S7 | one raw-Attention-output SAE sidecar at zero-based block 7 | final-layer sidecar |
| S37 | raw-Attention-output SAE sidecars at zero-based blocks 3 and 7, i.e. human layers 4 and 8 | two-site sidecar |
| SALL | one raw-Attention-output SAE sidecar at every zero-based block 0--7 | all-eight-layer sidecar |

M1 is explicitly excluded. “Full-course sidecar” is currently interpreted as a sidecar condition trained with its registered sidecars from token 0; it is not a sixth model. A genuinely distinct late-insertion or staged-sidecar model is `BLOCKED` until its manifest, insertion token, initialization, and objective are named.

The exact physical grid for every condition is

\[
\{0,\ 0.5,\ 1,\ 3,\ 5,\ 10\}
\quad\text{billion valid prediction tokens}.
\]

No nearest checkpoint, interpolation, recovery point at a different coordinate, or incomplete rolling checkpoint may substitute. Cross-model endpoint claims use the exact shared 10B coordinate. The earlier 9.174381056B SALL recovery point remains historical provenance and is not a result cell in this resumed run.

## 3. Data, Splits, And Representations

P is the frozen 360-row synthetic panel with 120/60/180 fit/tune/report rows and the last valid token. N is the frozen 1,200-row academic M2D2 panel with 600/200/400 fit/tune/report rows and the registered mean-position rule. Row identity, label, text, split, tokenizer, and representation position are immutable.

Report these surfaces separately:

1. common native final post-`norm2` representation for all five models;
2. M2's pre-SAE state and reconstruction actually consumed by its final MLP;
3. each sidecar's raw Attention output and SAE reconstruction.

The native final state is the primary cross-model surface. Sidecar reconstructions are not on the native language-model forward path and cannot establish native use.

## 4. Direct Uncentered Top-Direction Removal

The researcher requested direct removal of the largest singular direction without mean centering. For each model, checkpoint, dataset, and representation surface, fit the first right singular vector only on the fit split:

\[
H_{\mathrm{fit}}=U\Sigma V^\top,\qquad v_1=V_{1,:}.
\]

Apply the same direction unchanged to fit, tune, and report rows:

\[
x_{\mathrm{B2}}=x-(x^\top v_1)v_1.
\]

Do not subtract a mean before the singular-value decomposition. Do not fit a direction on tune or report rows. “Removing the first singular value” means removing its rank-one right-singular direction from each row, not merely deleting one scalar from a stored spectrum.

## 5. Fisher Geometry

For `C` classes,

\[
\bar\mu=\frac1C\sum_c\mu_c,
\]

\[
B=\frac1C\sum_c\lVert\mu_c-\bar\mu\rVert_2^2,
\qquad
W=\frac1C\sum_c\mathbb E_{x\mid c}\lVert x-\mu_c\rVert_2^2,
\qquad
F=\frac BW.
\]

Always report `B`, `W`, and `F` together for raw and B2 coordinates. The global Fisher ratio is `mean_c(B_c) / mean_c(W_c)`, not `mean_c(B_c/W_c)`. A Fisher increase without probe improvement is geometry only.

Use paired, class-stratified report-row bootstrap intervals for model differences and balanced label permutations as the geometry-null guard. P and N are separate evidence panels.

## 6. Linear And Two-Layer Neural Probes

### Linear probe

Reuse the E03 fit/tune/report contract: fit-only standardization, logistic regression, `C in {0.01, 0.1, 1, 10}` selected on tune, and one report evaluation. Report balanced accuracy, macro-F1, minimum class recall, and the mean predicted probability assigned to the correct class.

### Two-layer neural probe

AI-proposed fixed architecture, awaiting review:

```text
fit-only StandardScaler
-> Linear(1024, 128)
-> GELU
-> Dropout(0.1)
-> Linear(128, number_of_classes)
```

Use class-balanced cross-entropy, AdamW, learning rate `1e-3`, weight decay `1e-4`, batch size 32, at most 500 epochs, tune-loss early stopping with patience 30, and five fixed initialization seeds `17/31/47/61/79`. Select no width or architecture on report data. Report the seed mean and range of report balanced accuracy plus correct-class probability.

The neural probe checks nonlinear accessibility only. It does not show that the language model itself uses the class information.

## 7. Training Loss And Coefficient Ledger

Language-model loss is globally normalized negative log-likelihood per valid prediction token. Perplexity is

\[
\mathrm{PPL}=\exp(L_{\mathrm{LM}}).
\]

Do not call perplexity itself a loss. Use complete 100M-valid-token bins and preserve gaps. For each model and exact checkpoint, retain the last complete 100M-token bin ending at or before that checkpoint, with the bin endpoints recorded.

For the sidecar models, the verified training objective is

\[
L_{\mathrm{total}}
=L_{\mathrm{LM}}
+\lambda_{\mathrm{rec}}\frac1K\sum_{l\in H}L_{\mathrm{rec},l}
+\frac1{32}\frac1K\sum_{l\in H}L_{\mathrm{AuxK},l}.
\]

The report's reconstruction ratio uses reconstruction only:

\[
R_{\mathrm{loss}}=
\frac{\lambda_{\mathrm{rec}}\,\operatorname{mean}_l L_{\mathrm{rec},l}}
{L_{\mathrm{LM}}}.
\]

AuxK is listed separately and never included in the reconstruction-only ratio.

Every result row must read the actual coefficient and layer aggregation from the checkpoint's resolved config. The current coefficient-design explanation is:

- layer losses are averaged, not summed;
- one sidecar's explicit direct coefficient is `lambda_rec / K` before token normalization and Jacobians;
- the proposed future local-balance rule is a direct coefficient near 0.1, corresponding to total coefficients `0.1/0.2/0.8` for `K=1/2/8`;
- this proposal is not retroactively assigned to checkpoints trained with another coefficient and is not tested by this read-only experiment.

Required raw table columns:

```text
model, checkpoint_tokens, bin_start_tokens, bin_end_tokens,
hook_count, actual_lambda_rec, aggregation,
lm_nll, ppl, reconstruction_raw_layer_mean,
reconstruction_weighted, reconstruction_to_lm_ratio,
auxk_raw_layer_mean, auxk_weighted,
source_event_file, source_step_count, eligibility
```

## 8. Gradient Magnitude, Direction, And Random Reference

Use the actual training normalization. For each sidecar layer, measure the language-model gradient and that layer's weighted reconstruction contribution at:

1. the common sampled raw-Attention support;
2. the immediately upstream block representation;
3. for multi-sidecar models, the combined reconstruction gradient actually received at every upstream block representation.

Report norms, reconstruction/LM norm ratio, dot product, signed cosine, absolute cosine, and angle. The per-layer reconstruction gradient must include the actual `lambda_rec / K` factor. AuxK must have zero gradient to the backbone representation.

Compare observed absolute cosine with:

1. 2,000 independent isotropic random directions in the exact measured dimension;
2. 2,000 coordinate sign-flip/permutation draws preserving observed magnitudes and support;
3. off-diagonal cross-batch LM/reconstruction pairings.

Near 90 degrees is called “random-compatible near-zero cosine” unless the observed absolute cosine is unusually small under all registered references. It is never described as a mechanism for escaping a local optimum from this measurement alone.

## 9. Feature-Trajectory Measurements

Within each model and layer, feature IDs remain comparable across checkpoints of the same training run. Do not match IDs across independently initialized models.

On the unchanged report panel, record:

- active-feature fraction: dictionary features firing at least once;
- dead-on-panel fraction: features never firing on the panel;
- retained fraction between adjacent checkpoints: active at both points;
- newly active fraction: inactive at the earlier point and active at the later point;
- disappeared fraction: active earlier and inactive later;
- activation-frequency quantiles and mean positive Top-K count.

These are usage dynamics, not semantic identity. P and N remain separate.

## 10. Required Figures And Tables

Every trajectory uses cumulative valid prediction tokens in billions on the x-axis, names the dataset, representation, transform, metric, and unit, and preserves missing points.

Required reader figures:

1. raw `B/W/F` trajectories for native final representations;
2. B2 `B/W/F` trajectories after direct uncentered top-direction removal;
3. raw and B2 linear-probe balanced accuracy;
4. raw and B2 two-layer neural-probe balanced accuracy;
5. shared exact-10B model-minus-M0 differences for all five models;
6. token-aligned language-model NLL and perplexity, plus NLL difference from M0;
7. reconstruction-only loss, reconstruction/LM ratio, and actual coefficient ledger;
8. gradient norms and reconstruction/LM norm ratios at hook and upstream representations;
9. standardized gradient cosine against all random-reference bands;
10. active/retained/new/disappeared feature fractions over tokens.

Required tables:

1. checkpoint and source-manifest eligibility matrix;
2. full `B/W/F` and probe table for every model/checkpoint/dataset/surface/transform;
3. raw loss-and-coefficient ledger defined in Section 7;
4. gradient magnitude, ratio, angle, and random-reference percentile table;
5. feature-trajectory proportion table.

Each figure must have a source table, aggregation rule, uncertainty definition, one-sentence reading instruction, allowed conclusion, and nearest limitation.

## 11. Scientific Stages And Stop Rules

| Stage | Goal | Required input | Output | Stop rule |
| --- | --- | --- | --- | --- |
| S0 | resolve identities | exact model/config/checkpoint manifests for the registered model-specific grids | eligibility matrix | any unregistered substitution, incomplete milestone, or duplicate condition blocks the affected claim |
| S1 | qualify formulas and schemas | known-answer synthetic arrays and existing E03 cells | local test receipt | any Fisher/B2/probe/loss/gradient identity failure stops |
| S2 | bounded measurement Smoke | exact SALL/S7/M0/M2 10B checkpoints on one `5090-4-spot` node, one task per GPU | finite cache, no mutation, complete schema, held-out-NLL scalar, shared-parameter gradient receipt, memory/runtime receipt | any mutation, missing surface, unreliable required gradient direction, random-null failure, or nonconforming resource tuple stops; only PASS permits full submission |
| S3 | full read-only collection | every eligible exact cell | immutable caches and gradient summaries | no nearest-point substitution or scientific-setting retry |
| S4 | synthesis | complete source tables | all registered figures and result tables | missing cells remain visible and force `INSUFFICIENT` where applicable |
| S5 | report fill | eligible tables and figures | `summary.md`, `summary_cn.md`, `detailed.md`, and 0918 meeting reading copy | no result wording before evidence lineage passes |

No optimizer is constructed and no checkpoint is changed in this experiment. A later coefficient-training experiment would require a separate approved Protocol.

## 12. Claim Boundary

Can claim after eligible completion: checkpoint-dependent changes in class geometry, linear and nonlinear accessibility, feature usage, source-backed training loss, and activation-gradient scale/direction for the registered single seed and panels.

Cannot claim: increased parameter capacity, better general language ability, causal benefit of the sidecar count, semantic identity of individual features, native use of sidecar reconstructions, special learned orthogonality from a near-90-degree angle, or full-training coefficient optimality.

## 13. Block Audit And Review Items

| Block | State | Review item |
| --- | --- | --- |
| A: question and boundary | `CONFIRMED` | “capacity” remains motivation rather than a measured conclusion |
| B: data | `CONFIRMED` | frozen P and M2D2 N panels, reported separately |
| C: supervision | `CONFIRMED` | labels enter fit/tune/report analyses only; never training or gradient losses |
| D: models/checkpoints | `CONFIRMED` | M0 is Dense; M1 excluded; no separate late-insertion arm; all five conditions use exact `0/0.5/1/3/5/10B` milestones |
| E: objective/coefficient | `CONFIRMED` | layer mean and actual config coefficient are source-backed; `0.1/0.2/0.8` remains explanatory future design only |
| F: metrics/decision rules | `CONFIRMED` | fixed neural probe; shared exact-10B five-model endpoint; frozen M2D2 report NLL; activation and shared-parameter gradient guards |
| G: execution | `APPROVED_ACTIVE` | one 4xRTX5090 Spot Smoke, then one same-profile full read-only run only after Smoke PASS |

Researcher confirmation and resumed exact-10B execution authorization were recorded on 2026-09-18 before the new Smoke. The scientific body and decision rules are now frozen. Commit, push, publication, training, and checkpoint mutation remain outside this approval.

## 14. Confirmation And Amendment Ledger

| Time (UTC) | Event | Before | After | Eligibility impact |
| --- | --- | --- | --- | --- |
| 2026-09-18T01:43:03Z | pre-execution confirmation and SALL availability correction | all five models expected at exact 10B; no execution scope | M0/M2/S7/S37 retain 10B; SALL may use its latest complete rolling checkpoint; shared endpoint becomes 5B; 4xRTX5090 Spot Smoke and pass-gated full read-only run approved | no result was visible; the correction is pre-execution and eligible, but no five-model 10B claim is allowed |
| 2026-09-18T01:50:00Z | preflight resolved latest SALL checkpoint | provisional 7B milestone | complete recovery checkpoint `step_00034000`, `tokens_seen=8912237056`, manifest-created `2026-09-18T01:18:23.276080+00:00` | no E05 result was visible; exact checkpoint identity became more specific and remains eligible |
| 2026-09-18T02:09:31Z | researcher-directed pre-Smoke resource and checkpoint amendment | submitted `5090-4-spot` job `pt-6a4glbg6`; frozen SALL `step_00034000` | old job suspended before workload results; use `h100-2-spot`; freeze newly available complete recovery checkpoint `step_00035000`, `tokens_seen=9174381056` | no E05 Smoke result was visible; resource-only change and newer exact SALL identity preserve the scientific design; five-model 10B remains disallowed |
| 2026-09-18T03:34:56Z | researcher stopped analysis and deferred the overall comparison | H100 Spot Smoke passed; 18/18 sidecar collection cells completed; synthesis job failed because its running process retained the old SALL 8.912B coordinate; recovery job `pt-7clscrt2` was queued | recovery job stopped and confirmed `SUSPENDED` at `2026-09-18T03:35:03Z`; wait for exact SALL 10B, then use a separately frozen RTX 5090 profile for the overall analysis | retained collections are operational evidence only; no completed probe tables, figures, four-part result, or scientific conclusion is eligible from this interrupted round |
| 2026-09-18T04:26:00Z | exact-10B resumption and shared-parameter-gradient amendment | SALL stopped at the historical 9.174381056B recovery coordinate; only activation-gradient geometry was registered | exact SALL 10B milestone is frozen; all five models share 0/0.5/1/3/5/10B; add frozen M2D2 report NLL and the shared-parameter metrics below; run one `5090-4-spot` Smoke followed only on PASS by one same-profile full run | no result from the resumed run was visible; the amendment is eligible prospectively and does not rehabilitate the interrupted synthesis |
| 2026-09-18T04:31:07Z | exact-10B Smoke v1 | old M2 bottleneck code has no configurable hook-layer field | job `pt-nblfsfgm` stopped after the identity guard failed; explicitly resolve that registered legacy bottleneck to final block 7 | no measurement PASS; no scientific result |
| 2026-09-18T04:41:47Z | exact-10B Smoke v2 post-gate audit | shared-parameter filter excluded `saes.*` only | v2 operational receipt passed, but post-gate audit found legacy S7 `sae.*` parameters in the purported common backbone; v2 marked `INVALID_FOR_FULL_GATE` | S7 shared-parameter values in v2 are ineligible; no full submission from v2 |
| 2026-09-18T04:50:31Z | exact-10B Smoke v3 and full submission | filter covers both legacy `sae.*` and multisite `saes.*`; common-backbone dimension equality is a hard gate | v3 passed 4/4 cells on `5090-4-spot`, common sidecar dimension `281431040`, zero optimizer updates; pass-gated full job `pt-6x2z6ot6` submitted on the same profile | v3 authorizes the registered full read-only run; scientific results still await full synthesis |
| 2026-09-18T05:34:34Z | full collection PASS and probe-only load balancing repair | full job completed and hash-qualified all 30 collection cells, but order-modulo-four assigned P cells to GPUs 0/1 and larger N cells to GPUs 2/3 | stop only the incomplete probe stage of `pt-6x2z6ot6`; ignore its partial progress files; job `pt-ky6wrdd3` recomputes all 672 cells as eight balanced shards on the same four-RTX5090 Spot profile, two light processes per GPU | no probe matrix or result synthesis existed; models, data, splits, transforms, seeds, architecture, and metrics are unchanged; the 30-cell collection remains eligible |
| 2026-09-18T05:41:20Z | probe-only eager-transform repair | first balanced recovery revealed that each shard eagerly computed fit-only B2 SVDs before checking shard ownership, multiplying CPU work by eight | stop `pt-ky6wrdd3`; in `pt-8zbr996d`, check assignment first, compute only owned B2 transforms, and cap each of eight probe processes at four CPU BLAS threads | scientific settings are unchanged; two already completed balanced cells remain eligible because their numerical computation is identical; no merged probe table or scientific result existed |
| 2026-09-18T08:54:00Z | post-hoc P mean-token and outlier-sensitivity supplement | registered P representation is the last valid token and the Dense 10B P Fisher endpoint is unusually sensitive to three report rows | keep the registered result unchanged; add a read-only supplement that averages all non-padding P-token representations, applies one frozen exclusion list to every model/checkpoint, retains a whole-family exclusion guard and matched random-removal reference, and runs a two-RTX5090 Spot Smoke followed only after PASS by a same-profile full extraction | post-hoc sensitivity evidence only; it cannot replace or retroactively qualify the registered last-token primary result |

## 15. Exact-10B And Shared-Parameter-Gradient Amendment

The SALL terminal cell is the complete milestone
`20260918_attention_output_sidecar_all8_4h100_resume/runs/formal50b_all8_unit_weight_4h100_mbs16_resume/milestones/token_010000000000`,
with `tokens_seen=10000000000`, optimizer step `38150`, and state SHA256
`86cf7f06ab94db94ba15a50e15225994c64e688e1449a816e0c06f756d0d1db6`.
Its fork lineage starts from the complete 9.174381056B SALL checkpoint and preserves
262,144 valid prediction tokens per optimizer update.

On the common non-SAE backbone parameters, define the language-model gradient
and the already weighted, layer-mean reconstruction gradient by

\[
g_C=\nabla_{\theta_{\mathrm{shared}}}L_{\mathrm{LM}},\qquad
g_A=\nabla_{\theta_{\mathrm{shared}}}
\left(\lambda_{\mathrm{rec}}\frac1K\sum_{l\in H}L_{\mathrm{rec},l}\right).
\]

AuxK is excluded from \(g_A\). Report

\[
\rho=\frac{\lVert g_A\rVert_2}{\lVert g_C\rVert_2},\qquad
c=\frac{g_C^\top g_A}{\lVert g_C\rVert_2\lVert g_A\rVert_2}
\]

for all shared parameters together and for the embedding, each transformer block,
and the final norm separately. Measurements use the same frozen four gradient
batches at every sidecar checkpoint. Let

\[
\tau=\max\left(10^{-20},10^{-8}\max(\lVert g_C\rVert_2,\lVert g_A\rVert_2)\right).
\]

If either norm is at most \(\tau\), retain the norms and any defined scale ratio,
but leave cosine and angle empty and mark
`DIRECTION_NOT_RELIABLY_DEFINED`. Compare reliable cosines with the exact
parameter dimension's isotropic scale \(1/\sqrt d\) and with the analytic
coordinate-sign-flip null whose dot-product standard deviation is
\(\sqrt{\sum_i(g_{C,i}g_{A,i})^2}\). This high-dimensional analytic reference
supplements, rather than replaces, the registered 2,000-draw activation-space
random references.

The functional held-out loss is causal LM NLL on the frozen 400-row M2D2 report
split, exactly 102,400 valid prediction tokens per checkpoint. This is reported
separately from the source training-loss curve. The new full collection contains
30 read-only cells: 18 sidecar cells and 12 M0/M2 held-out-loss controls. The
qualified earlier M0/M2 representation caches remain the geometry/probe inputs;
new M0/M2 reads exist to measure held-out loss and recheck identity without
changing the frozen representation panel.

Fisher credibility at the shared exact-10B endpoint uses 1,000 paired,
class-stratified report-row bootstrap draws for model-minus-M0 differences and
1,000 balanced-label permutations for each model's absolute Fisher null. Report
\(B\), \(W\), and \(F=B/W\) together, the paired 95% interval for every difference,
and the upper-tail permutation probability. These guards qualify the 10B endpoint
claim; trajectory points remain descriptive unless the same direction is visible
at more than one checkpoint.
