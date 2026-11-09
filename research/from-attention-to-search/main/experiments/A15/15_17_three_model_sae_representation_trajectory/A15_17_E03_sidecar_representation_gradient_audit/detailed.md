# Detailed: A15_17_E03 Attention-Sidecar Representation, Variance, And Local-Gradient Audit

Primary Anchor: [A15_17](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/15_17_three_model_sae_representation_trajectory_anchor.md)  
Frozen Protocol and amendments: [protocol.md](protocol.md)  
Summary: [summary.md](summary.md) / [summary_cn.md](summary_cn.md)  
Result eligibility: `ELIGIBLE_READ_ONLY_MEASUREMENT_WITH_RECORDED_CPU_SYNTHESIS_REPAIR`; scientific interpretation `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`

## 0. Quick Recap

Purpose: add S7, S37, and SALL to the prior M0/M1/M2 representation audit and measure variance organization plus local sidecar/LM gradient geometry at common checkpoints.

Hypothesis: an accessible-organization change should appear in the native final state on both P and N and should not be explained solely by the fit-only first centered direction.

Experiment logic: reuse qualified M0/M1/M2 caches; collect S7/S37/SALL at 0/0.5/1/3B; analyze native final h and sidecar-internal states; compare normalized LM and local reconstruction gradients at the same Attention-output node.

Direct result: all 12 GPU collection cells and all registered guards passed. No sidecar condition has a 3B native-final advantage over M0 that holds on both panels. At 3B, support-only reconstruction/LM gradient angles are 89.91--90.17 degrees; magnitude ratios are 0.653 for S7 L7, 0.170/0.245 for S37 L3/L7, and 0.012--0.047 per SALL layer.

Eligibility: the first shared-root submission was stopped after a concurrent rewrite; the first isolated Smoke lacked the registered offline Transformers path; the second Smoke passed. The full GPU collection passed 12/12, then the combined ACP job failed before result creation because the CPU script expected semantic split names instead of the frozen file's literal names. The identity-preserving mapping was recorded in Protocol R004 and synthesis reran from hashed complete caches. No row membership, metric, or scientific setting changed.

Verdict: eligible descriptive measurement; no registered binary mechanism threshold existed. The bounded AI reading is no cross-panel native representation advantage and near-orthogonal local gradient geometry with placement-dependent scale.

Claim boundary: representation accessibility and instantaneous local objective geometry only; no functional-use, LM-benefit, routing, specialization, or long-run causal claim.

Endpoint boundary: the physical source audit found S7 milestones through 10B and S37/SALL milestones through 3B, with no 15B milestone in any of the three source trees at execution freeze. Only their real 0/0.5/1/3B intersection is eligible for the matched matrix.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete computation | Unit / formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| native final h | state actually used by the final native MLP | final block post-`norm2` | 1024-vector | common representation across all six models | functional use of a class direction |
| B / W / F | between-class energy, within-class energy, and separation ratio | class-balanced trace energies on report rows | `F=B/W` | separates mean movement from within-class spread | causal utility |
| B3 | remove fit mean and fit first centered singular direction | fit transform applied unchanged to tune/report | transformed 1024-vector | guards against a dominant direction | removal of every nuisance |
| participation ratio | effective spread of covariance energy | `(sum lambda)^2 / sum lambda^2` | effective dimensions | low values mean concentrated variance | semantic quality |
| support gradient | gradient restricted to the deterministic 32 SAE positions | four stratified N-fit batches | L2 norm / cosine / degrees | avoids dilution by structural zeros | parameter-level total update |
| local reconstruction gradient | one SAE's own reconstruction term at its own node | includes `1 / sidecar_count` training aggregation | activation-gradient tensor | exact local auxiliary push | sum over shared parameters or long-run dynamics |

## 2. Anchor Link And Decision Point

The Anchor's bounded question is whether trained SAE configurations exhibit different accessibility trajectories before any causal functional intervention. E03 changes the treatment family from final-MLP bottlenecks to Attention-output sidecars that do not enter the native LM forward. The next decision is therefore not whether a sidecar “works,” but whether the measured local gradients warrant a parameter-level aggregation audit before any new training.

## 3. Protocol Freeze, Conformance, And Deviations

| Registered item | Expected | Actual | Status | Evidence | Eligibility impact |
| --- | --- | --- | --- | --- | --- |
| models | M0/M1/M2 controls plus S7/S37/SALL | all six included | PASS | task manifest and control caches | none |
| checkpoints | common 0/0.5/1/3B only | 12 new cells plus matching controls | PASS | `config/task_manifest.json`; completion records | none |
| panels | P 360 and N 1,200 | exact frozen IDs and order | PASS | cache IDs; collection guards | none |
| GPU profile | one node, four RTX5090 Spot | `5090-4-spot`, four SM120 GPUs | PASS | receipts and GPU preflight | none |
| no updates | read-only checkpoints | `optimizer_updates=0` in every receipt | PASS | 12 completion JSON files | none |
| Smoke | all model families and heaviest trained all-layer path | S7 0B, S37 0B, SALL 0B/3B | PASS on v2 | `smoke_5090_4spot_v2` | none |
| gradients | same node; full/support norm, ratio, cosine, angle | four N-fit batches at every new cell | PASS | `gradient_metrics.csv` | none |
| structural zeros | reconstruction outside support and AuxK at node equal zero | exact zero in every batch/layer | PASS | raw gradient JSON | none |
| figures/tables | requested trajectories, spectra, internal variance, gradient views | 14 figures and 5 tables | PASS | S4-S5 receipt | none |
| first submission | approved code root | shared root concurrently rewritten; job stopped | DEVIATION R001/R002 | `pt-hxlku819` and pod log | ineligible operational record only |
| isolated Smoke v1 | registered local runtime dependencies | Transformers path absent | DEVIATION R003 | `pt-08dxw4r6` log | ineligible; fresh Smoke used |
| full combined terminal | collection plus CPU synthesis succeeds | collection passed; CPU split-name lookup failed | DEVIATION R004 | `pt-yuifv33t`, `COLLECTION_PASS.json` | GPU collection eligible; combined job terminal not a result receipt |
| synthesis repair | semantic fit/tune/report roles | literal fit/development/confirmation mapped 1:1 | PASS / BOUNDED REPAIR | script hash and synthesis receipt | no row or metric change; eligible with recorded repair |

Frozen Protocol revision: Protocol body plus append-only R001--R004.

Execution scope approved: implementation, four-RTX5090 Spot Smoke, full run, and completion supervision. No training, commit, push, or publication.

Retries and exclusions: `pt-hxlku819` and `pt-08dxw4r6` are ineligible operational evidence. `pt-mdmegr1t` is the eligible Smoke. `pt-yuifv33t` owns the eligible 12-task GPU collection; local S4-S5 owns the eligible result synthesis.

Post-hoc analyses: none. The split-name mapping happened before any result table or figure existed.

## 4. Actual Setup

Research question: do Attention-output sidecars alter native final-state variance/readability trajectories, and what is the local direction and scale of their reconstruction gradient relative to LM?

Data: P is the frozen 360-row controlled panel with 120 fit, 60 development/tune, and 180 confirmation/report rows. N is the frozen 1,200-row M2D2 panel with 600 fit, 200 tune, and 400 report rows.

Models: S7 hooks block 7; S37 hooks blocks 7 and 3; SALL hooks all blocks 0--7. Each sidecar is width 30,000, Top-32, reads the raw Attention output after `W_O`, and never replaces a native activation. M0/M1/M2 are predecessor controls.

Representation positions: P last valid token; N native final h averaged over positions 0--255; N internal Attention/reconstruction averaged over the deterministic 32 SAE positions.

Gradient batches: four frozen batches, each containing one N-fit row from each of eight classes. LM loss uses 256 targets per row. Local reconstruction uses 32 positions and the training layer-mean factor. AuxK is checked but is detached from the node.

Randomness: checkpoint lineage seed 17; deterministic split and position hashes; no stochastic update.

Code root: `/data/250010109/MoE_Router/experiments/20260917_multimodel_sidecar_representation_gradient_audit/`.

Result root: `/data/250010109/MoE_Router/experiments/20260917_multimodel_sidecar_representation_gradient_audit/runs/full_5090_4spot_v1/`.

Known limitation: one trained seed and two panels; checkpoint/layer/batch cells are repeated measurements, not independent experimental replicates.

## 5. Metrics And Registered Decision Rules

The primary descriptive measurements are native-final B, W, and F under raw and B3 coordinates. Covariance top-1/top-10 shares and participation ratio describe concentration. Frozen linear readout reports balanced accuracy. No equivalence margin or binary improvement threshold was registered, so the valid outcome is an eligible estimate and bounded pattern, not a statistical proof of equality or superiority.

Gradient norms are normalized-objective activation gradients. `reconstruction_to_lm_ratio=1` means equal L2 magnitude at the same tensor support; cosine zero or angle 90 degrees means no net first-order alignment in that high-dimensional activation tensor.

## 6. Evidence Lineage

| Claim or decision | Protocol criterion | Raw artifact | Computation | Aggregation | Observed value | Eligibility | Verdict | Limitation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| no cross-panel sidecar advantage | common native h, B3, P and N | 12 new caches + E01 controls | Fisher and frozen probes | class-balanced report rows | 3B P sidecar F 0.214/0.273/0.222 vs M0 0.297; N 0.203/0.205/0.205 vs 0.207 | ELIGIBLE | no descriptive cross-panel advantage | no superiority/equivalence test |
| P-specific SALL concentration | covariance distribution after B3 | final-state caches | report covariance eigenspectrum | rows within P or N | P top1/PR 0.204/14.69 vs M0 0.146/17.85; N 0.104/32.33 vs 0.103/31.45 | ELIGIBLE | panel-specific concentration | concentration is not quality |
| sidecar raw separation depends on first direction | raw and B3 F at 3B | final-state caches | B3/raw F ratio | one endpoint per model/panel | P S7/S37/SALL retain 52.1/53.6/55.0% | ELIGIBLE | dominant-direction dependence | does not identify direction semantics |
| local gradients near orthogonal | identical node and objective normalization | 144 new gradient batch/layer cells, each with full/support summaries | tensor dot product and norms | mean over four frozen batches for display | 3B support angles 89.91--90.17 degrees | ELIGIBLE | near-zero local alignment | not parameter aggregation or training trajectory |
| placement changes local magnitude | same gradient computation across models/layers | gradient JSON | reconstruction/LM norm ratio | four-batch mean | S7 0.653; S37 0.170/0.245; SALL 0.012--0.047 at 3B support | ELIGIBLE | scale differs strongly | SALL includes registered 1/8 layer mean |
| S37 L7 scale is non-monotonic | common 0/0.5/1/3B points | S37 L7 gradient JSON | support ratio | four-batch mean per point | 0.287, 1.196, 1.564, 0.245 | ELIGIBLE | checkpoint-sensitive | four batches, one seed |

## 7. Main Results

### Eligible decision evidence

At 3B, the new sidecar models do not exceed M0 on both panels under native-final B3 Fisher or readout. S37 is the strongest of the sidecar set on P and slightly higher in N readout, but its N Fisher remains near M0 and its P values remain below M0.

The covariance result is not uniformly “lower rank.” SALL is markedly more concentrated on P by both top-1 share and participation ratio, while all models converge to similar N concentration by 3B. The difference is therefore panel-conditioned.

All local reconstruction gradients are nonzero, exactly supported on the registered positions, and nearly orthogonal to the corresponding LM gradient. The magnitude is large enough to be locally relevant for S7 and checkpoint-dependent S37 L7, but each SALL local term is small after the objective's eight-layer mean.

### Bounded evidence

Internal SAE reconstructions usually reduce participation ratio relative to their Attention inputs and sometimes increase Fisher, especially in deeper SALL layers. The direction is not uniform across layers or panels and the reconstruction is not consumed by the LM. These are compression/accessibility observations only.

### Ineligible / failed operational evidence

The shared-root job and first isolated Smoke certify no scientific artifact. The failed combined terminal status of the full job reflects the pre-result split-name error, not a failed GPU measurement. No result is read from a failed partial analysis.

## 8. Visualization Results

### Native final-state B/W/F after first-direction removal

![B3 Fisher trajectories](figures/final_fisher_b3_trajectories.png)

Source: [final_representation_metrics.csv](tables/final_representation_metrics.csv). The x-axis is cumulative valid prediction tokens in billions. The figure shows that P separates the model trajectories more than N, but no sidecar is above M0 on both panels at 3B. It cannot establish functional use.

### Covariance concentration trajectory

![Variance distribution trajectories](figures/final_variance_distribution_trajectories.png)

Source: [final_representation_metrics.csv](tables/final_representation_metrics.csv). Higher top-1 share and lower participation ratio mean more concentrated variance. SALL is the most concentrated on P at 3B, while N values nearly overlap. It cannot label the concentrated directions as semantic.

### Gradient magnitude and angle on SAE support

![Support gradient trajectories](figures/gradient_magnitude_ratio_angle_support.png)

Source: [gradient_metrics.csv](tables/gradient_metrics.csv). Solid/dashed norm curves use a log scale; the middle column is the norm ratio; the right column is angle. Near-90-degree lines show near-zero local alignment, not absence of parameter-level interaction.

### All-layer internal variance map

![SALL internal variance maps](figures/sall_internal_variance_heatmaps.png)

Source: [sidecar_internal_metrics.csv](tables/sidecar_internal_metrics.csv). Rows are hook layers and columns are checkpoint tokens. Attention and reconstruction have distinct, layer- and panel-dependent concentration. The map is descriptive and cannot rank sidecar placement by LM utility.

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | Status | Failure reason | What this rules out | What remains live |
| --- | --- | --- | --- | --- | --- |
| S0/S1 | manifest, local tests, dry-run tuple | PASS | none | missing common checkpoints/profile ambiguity | runtime/import risk |
| first shared submission | `pt-hxlku819` | INELIGIBLE | concurrent shared-root rewrite | none scientifically | isolated-source execution required |
| isolated Smoke v1 | `pt-08dxw4r6` | FAIL / INELIGIBLE | offline Transformers path absent | model/checkpoint corruption not implicated | dependency activation |
| isolated Smoke v2 | `pt-mdmegr1t` | PASS | none | GPU/runtime/model-family/heaviest-path failures | full matrix |
| S3 collection | `pt-yuifv33t`, 12 completion records | PASS | none | missing checkpoint/panel/gradient/immutability cells | synthesis |
| first S4 | combined job terminal FAIL | FAIL before results | P literal split names differed | no scientific metric evaluated | identity mapping |
| repaired S4/S5 | synthesis receipt | PASS | none | incomplete table/figure lineage | human result judgment |

No physical prior or causal mechanism is falsified by this descriptive audit. The registered operationalization is valid for local gradient geometry and representation accessibility. The remaining rival is that parameter-space aggregation and longer-run optimization differ from node-local geometry.

## 10. Full Experiment Record

1. Question: do the three new Attention-sidecar trajectories change native variance/readability, and how do local reconstruction gradients compare with LM gradients?
2. Setup: six model conditions, four common token checkpoints, fixed P/N rows, fixed position and split rules, no updates.
3. Training data: no training occurred; checkpoints derive from the registered DCLM trajectories.
4. Testing data: P fit/development/confirmation and N fit/tune/report, with confirmation/report untouched by transforms and readout selection.
5. Result: 12/12 new GPU cells, 96 final-representation metric rows, 352 internal metric rows, 352 gradient rows, 4,600 spectrum rows, 14 figures, and 5 curated tables.
6. Insight: the sidecars visibly reshape concentration on P and create nonzero local gradients, but do not yield a cross-panel native-final advantage. The next uncertainty is the summed parameter-space effect.

## 11. Interpretation

The gradient angle result is easiest to interpret geometrically. If the LM gradient is one arrow and the local reconstruction gradient another arrow in a very high-dimensional activation tensor, their dot product is nearly zero: the sidecar is pushing mostly sideways relative to the immediate LM descent direction. This is neither cooperation nor direct opposition. Because a sideways step can still alter future representations and because different layer terms meet again in shared parameters, the result is a local description, not proof of harmlessness.

The variance result similarly distinguishes concentration from usefulness. SALL creates a sharper P spectrum, but sharper means fewer dominant directions, not better semantic organization. Its N spectrum is not comparably distinctive, and its native-final Fisher/readout does not establish a cross-panel gain.

## 12. Claim Boundary

Can claim: complete eligible measurement at registered points; dataset-conditioned concentration; near-orthogonal local gradients with placement-dependent magnitudes; exact structural-zero guards; no cross-panel descriptive sidecar advantage at 3B.

Cannot claim: equivalence, LM improvement, causal benefit/harm, native use of SAE reconstructions, semantic identity of eigenvectors or atoms, routing, expert utility, or specialization.

## 13. Next Decision

Decision: `AI suggestion pending researcher confirmation` — run a read-only parameter-space aggregation audit before any new training.

Completion criterion: at 0.5/1/3B, compute LM, summed reconstruction, and leave-one-layer-out gradient vectors for block Attention/MLP/Norm parameter groups on the same four batches; verify exact vector-sum identity and report norm/angle stability.

Stop condition: if the total reconstruction effect remains below one-tenth of LM and has no stable alignment/opposition across batches/checkpoints, stop treating sidecar gradients as a primary mechanism. If it survives, design a separate matched LM-only versus sidecar short continuation.

Resume action: obtain researcher confirmation of threshold, points, parameter groups, and compute budget; write a new Protocol before GPU execution.

## 14. Artifact Manifest

| Artifact | Purpose | Producer | Source inputs | Hash / identity | Complete | Claim-eligible | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [protocol.md](protocol.md) | frozen contract and amendments | Research_System | Anchor + researcher instruction | append-only R001--R004 | yes | yes | owns execution boundary |
| task manifest | 12-cell identity | isolated workspace | checkpoint manifests | `e25f8a...c94e` | yes | yes | 3 models x 4 points |
| completion records | per-cell hashes and guards | GPU collector | P/N + checkpoints | 12 PASS records | yes | yes | zero updates |
| [final representation table](tables/final_representation_metrics.csv) | B/W/F, spectrum summaries, probes | repaired S4 | qualified caches | `301038...de7` | yes | yes | 96 rows |
| [gradient table](tables/gradient_metrics.csv) | norms, ratios, cosines, angles | repaired S4 | gradient JSON | `267b27...127` | yes | yes | 352 rows |
| [internal table](tables/sidecar_internal_metrics.csv) | per-layer Attention/reconstruction variance | repaired S4 | sidecar caches | 352 rows | yes | bounded | descriptive |
| [final spectrum](tables/final_covariance_spectrum_3b.csv) | 3B covariance eigenvalues | repaired S4 | final caches | 2,400 rows | yes | yes | raw and B3 |
| [internal spectrum](tables/sidecar_internal_spectrum_3b.csv) | 3B internal spectra | repaired S4 | sidecar caches | 2,200 rows | yes | bounded | B3 only |
| [B3 Fisher figure](figures/final_fisher_b3_trajectories.png) | common-checkpoint variance trajectory | repaired S4 | final table | `08703f...8611` | yes | yes | central figure |
| [variance distribution figure](figures/final_variance_distribution_trajectories.png) | concentration trajectory | repaired S4 | final table | `8c9a30...452a` | yes | yes | central figure |
| [support gradient figure](figures/gradient_magnitude_ratio_angle_support.png) | magnitude and angle | repaired S4 | gradient table | `c24ca7...c37e` | yes | yes | central figure |
| synthesis receipt | repair and output identity | local S4/S5 | complete GPU caches | `synthesis_receipt.json` | yes | yes | 14 figures, 5 tables |

## 15. Links

anchor: `Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/15_17_three_model_sae_representation_trajectory_anchor.md`  
protocol: `Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_E03_sidecar_representation_gradient_audit/protocol.md`  
code workspace: `/data/250010109/MoE_Router/experiments/20260917_multimodel_sidecar_representation_gradient_audit/`  
runner: `scripts/run_remote.sh`  
config: `config/task_manifest.json`  
result dir: `runs/full_5090_4spot_v1/`  
pod logs: `acp_receipts/pod/`  
jobs: stopped `pt-hxlku819`; failed Smoke `pt-08dxw4r6`; passed Smoke `pt-mdmegr1t`; collection-PASS/synthesis-failed combined job `pt-yuifv33t`; repaired local synthesis PASS.

## 16. Post-hoc Per-Class Fisher And Loss-Scale Supplement

The researcher requested a per-class decomposition of the existing Fisher metric, an explicit raw-Attention versus SAE-reconstruction comparison on both panels, scalar LM-versus-regularization loss scales, and coefficient implications. This is labeled `POST_HOC_EXPLORATORY`: it uses the already qualified caches, gradient table, and immutable training ledgers and changes neither the frozen Protocol nor the registered verdict.

The per-class definition is (F_c=B_c/W_c), where (B_c) is the squared distance from the class mean to the class-balanced center and (W_c) is the class's mean squared within-class distance. The aggregate reconstruction check exactly reproduces every qualified global E03 Fisher value. At 3B, weighted regularization is 5.55%, 6.24%, and 6.33% of LM loss for S7, S37, and SALL, while local support-gradient ratios range across 0.099–0.763, 0.153–1.564, and 0.012–0.073 respectively. This mismatch blocks coefficient selection from scalar loss arithmetic alone.

Reader account and bounded coefficient proposal: [supplement_per_class_fisher_loss.md](supplement_per_class_fisher_loss.md) / [supplement_per_class_fisher_loss_cn.md](supplement_per_class_fisher_loss_cn.md).

Supplement artifacts: [per-class Fisher](tables/per_class_fisher_metrics.csv), [global Fisher reconstruction check](tables/global_fisher_recomputed.csv), [loss scales](tables/loss_scale_metrics.csv), [gradient summary](tables/local_gradient_scale_summary.csv), [surface Fisher ratio](figures/global_fisher_reconstruction_to_attention_ratio.png), [loss trajectory](figures/training_loss_scale_trajectories.png), and [coefficient sensitivity](figures/local_gradient_coefficient_sensitivity.png).

Supplement script SHA256: `b20517fba8cc7f42a0a1dec71bb9d10c345ae394cca164ad357666bc546571c8`. Supplement overview SHA256: `78015734a336c201509eca171d13e9beea4591daf770e155b21719d7a9111be4`.

## 17. Post-Hoc Fisher And Gradient-Null Reliability Audit

Status: POST_HOC_RELIABILITY_AUDIT. This audit began after E03 results existed, changes no frozen decision rule, performs zero optimizer updates, and supports only bounded interpretation repair.

The Fisher computation was restated and independently checked as

\[
B=C^{-1}\sum_c\lVert\mu_c-\bar{\mu}\rVert_2^2,\qquad
W=C^{-1}\sum_c\mathbb{E}_{x\mid c}\lVert x-\mu_c\rVert_2^2,\qquad
F=B/W.
\]

For every S7/S37/SALL model, 0/0.5/1/3B checkpoint, P/N panel, sidecar layer, raw/B3 transform, and raw-Attention/reconstruction surface, 256 class-stratified paired report-row bootstrap draws were computed. At 3B in raw coordinates, 256 balanced report-label permutations and fit/tune/report-separated linear probes were added.

At 3B, all 44 raw-coordinate surfaces exceeded the shuffled-label 95th percentile by 4.49--23.46 times; every one-sided permutation value was 1/257. All 22 raw-coordinate Attention-to-reconstruction comparisons reduced both between-class and within-class energy: B ratios were 0.532--0.911 and W ratios were 0.440--0.826. Across 44 raw/B3 held-out-probe pairs, reconstruction was lower in 42, tied in one, and higher in one. Therefore Fisher is non-random class geometry but cannot by itself rank representation accessibility.

The local-gradient support dimension was recovered from qualified artifacts as 8 samples x 32 positions x 1,024 hidden coordinates = 262,144. For two independent isotropic unit vectors in this dimension, squared cosine follows Beta(1/2, (d-1)/2). The exact null has cosine SD 0.001953 and a 95% angle interval of 89.781--90.219 degrees. Of 44 model-checkpoint-layer groups, 43 were compatible with the dimension-matched null after separate Benjamini--Hochberg adjustment for unusually small and large absolute cosine. No group was closer to exact orthogonality than random. SALL 1B L0 had larger absolute departure from zero (q=9.67e-6); all 11 groups at 3B were random-compatible.

The current files contain contractions rather than raw gradient vectors. Coordinate sign-flip/permutation, empirical effective-dimension, and cross-batch direction nulls remain unmeasured and are prospectively required by E05.

In complete shared 100M-token bins from 3.0B through 4.4B, mean LM-loss differences from Dense were M2 +0.00065, S7 +0.01254, S37 +0.00333, and SALL -0.00378 nats per valid token. These are single-trajectory descriptive differences, not coefficient or gradient-norm causal effects.

Reader account: [fisher_gradient_reliability.md](fisher_gradient_reliability.md) / [fisher_gradient_reliability_cn.md](fisher_gradient_reliability_cn.md).

New evidence tables: [Fisher bootstrap](tables/fisher_surface_bootstrap.csv), [paired Fisher/B/W ratios](tables/fisher_paired_logratio.csv), [permutation null](tables/fisher_permutation_null_3b.csv), [held-out probes](tables/internal_probe_3b.csv), [source-backed LM loss](tables/training_lm_loss_100m.csv), [LM loss minus Dense](tables/training_lm_loss_delta_vs_dense_100m.csv), [dimension-matched gradient null](tables/gradient_dimension_matched_random_null.csv), and [group random-null summary](tables/gradient_random_null_group_summary.csv).

New reader figures: [paired Fisher intervals](figures/fisher_delta_log_ci_trajectories.png), [B/W/F sources](figures/fisher_bw_ratio_3b.png), [permutation margin](figures/fisher_permutation_margin_3b.png), [held-out probes](figures/internal_probe_accuracy_3b.png), [training LM loss](figures/training_lm_loss_multimodel_100m.png), [dimension-calibrated gradient cosine](figures/gradient_cosine_vs_dimension_matched_random.png), and [pooled random-null comparison](figures/gradient_random_null_distribution.png).

Claim repair: replace “the gradients are specially orthogonal” with “the observed local cosines are near zero and are mostly compatible with independent random directions in the measured high dimension.” Gradient magnitude remains measured; parameter-space aggregation, non-isotropic nulls, and coefficient optimality remain unknown.
