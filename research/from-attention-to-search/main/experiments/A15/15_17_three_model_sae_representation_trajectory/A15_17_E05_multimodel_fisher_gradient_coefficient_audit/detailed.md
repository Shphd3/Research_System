# A15_17_E05 Detailed Record: Multimodel Fisher, Loss, and Gradient-Coefficient Audit

## Record Status

```text
experiment: A15_17_E05_multimodel_fisher_gradient_coefficient_audit
protocol: protocol.md
execution_state: COMPLETED
evidence_eligibility: ELIGIBLE_WITH_RECORDED_NULL_IMPLEMENTATION_DEVIATION
scientific_reading: AI_DRAFT_AWAITING_RESEARCHER_CONFIRMATION
execution_profile: 5090-4-spot
execution_image: shphd-lite-0911
optimizer_updates: 0
completed_at: 2026-09-18T05:57:47Z
```

Canonical first reading: [summary.md](summary.md) and [summary_cn.md](summary_cn.md).

Execution workspace:

```text
/data/250010109/MoE_Router/experiments/20260918_multimodel_fisher_gradient_coefficient_audit
```

Immutable result root:

```text
/data/250010109/MoE_Router/experiments/20260918_multimodel_fisher_gradient_coefficient_audit/runs/full_5090_4spot_10b_v1
```

## 1. Question And Hypothesis Tested

The tested question was whether a training-only SAE reconstruction sidecar changes the native language-model representation in a way that improves class separation and language-model optimization at matched cumulative valid tokens. The registered supporting pattern required Fisher geometry and held-out accessibility to improve together, survive direct uncentered top-direction removal, and not coincide with worse token-aligned language-model loss. The strongest rivals were within-class compression, a single dominant direction, probe mismatch, random high-dimensional near-orthogonality, and non-matched training trajectories.

## 2. Setup And Controlled Variables

### Models and checkpoints

The final manifest contained 30 exact read-only cells:

```text
models: M0, M2, S7, S37, SALL
tokens per model: 0, 0.5B, 1B, 3B, 5B, 10B
cells: 5 x 6 = 30
```

M0 was the only Dense reference. M2 was the serial mediated-SAE comparison. S7, S37, and SALL had one, two, and eight Attention-output sidecars. M1 was excluded. No nearest checkpoint or interpolation was used. The SALL 10B source was the complete milestone at

```text
/data/250010109/MoE_Router/experiments/20260918_attention_output_sidecar_all8_4h100_resume/runs/formal50b_all8_unit_weight_4h100_mbs16_resume/milestones/token_010000000000
```

with `complete=true`, 10,000,000,000 valid prediction tokens, optimizer step 38,150, and state SHA-256 `86cf7f06ab94db94ba15a50e15225994c64e688e1449a816e0c06f756d0d1db6`.

### Data and split discipline

- P: frozen 360-row synthetic panel, evaluated on its registered report split.
- N: frozen 1,200-row M2D2 academic panel with 600 fit, 200 tune, and 400 report rows.
- The same row identity, tokenizer, representation position, and split were used for every checkpoint.
- Standardization, the direct uncentered top singular direction, and probe hyperparameter choice used no report rows.
- P and N were never pooled into one metric.

### Representation and probe surfaces

- Primary cross-model surface: native final post-`norm2` representation.
- Sidecar-local surfaces: raw Attention output and SAE reconstruction at each registered layer.
- M2-local surfaces: its pre-SAE state and the reconstruction consumed by the final MLP.
- Linear probe: fit-only standardization and tune-selected logistic-regression regularization.
- Neural probe: fixed 1024-to-128-to-class architecture, five fixed initialization seeds, and tune-loss early stopping.

### Representation-cache lineage

The cross-model representation analysis intentionally combines two qualified cache roots; this must be preserved when reproducing the result:

- M0 and M2 representation arrays were reused from the prior qualified exact-checkpoint extraction at `/data/250010109/MoE_Router/experiments/20260915_three_model_representation_audit/runs/full_h100_reserved_v4/caches/{MODEL}_{TOKENS:012d}.npz`. M0 native-final fields are `P_h` and `N_h_mean`. M2 native/pre-SAE fields are `P_h` and `N_h_mean`; the reconstruction actually consumed by its MLP is `P_actual` and `N_actual_mean`.
- S7/S37/SALL arrays were extracted in E05 at `/data/250010109/MoE_Router/experiments/20260918_multimodel_fisher_gradient_coefficient_audit/runs/full_5090_4spot_10b_v1/caches/{MODEL}_{TOKENS:012d}.npz`. Their native-final fields are `P_final_h` and `N_final_h_mean`; sidecar raw and reconstructed fields are `P_attn_L{layer}` / `P_recon_L{layer}` and `N_attn_L{layer}` / `N_recon_L{layer}`.
- The E05 M0/M2 cache files under the latter root contain the newly measured frozen-M2D2 language-loss accumulators (`N_report_lm_loss_sum`, `N_report_lm_tokens`, and `N_report_lm_nll`) but are not the representation source consumed by `analyze.py`.
- Every cache carries `P_sample_ids` and `N_sample_ids`; synthesis requires exact equality with the frozen panel order before any metric is computed.

This mixed-root reuse does not change the registered cross-model representation coordinates because the reused M0/M2 arrays were the previously qualified exact-token extractions and sample-identity equality was rechecked. It is evidence provenance, not a new experimental condition. The main limitation is operational: reproducing the full result requires both cache roots rather than only the E05 result directory.

### Fisher definition

For class means \(\mu_c\) and balanced class count \(C\):

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

The implementation computes the ratio of the class-balanced means, not the mean of classwise ratios. The B2 transform removes \(x^\top v_1v_1\) using the first uncentered fit-split right-singular direction; it does not subtract a mean.

### Loss and gradient definitions

The source configs established that the three sidecar objectives use

\[
L_{\mathrm{total}}
=L_{\mathrm{LM}}
+\lambda_{\mathrm{rec}}\frac1K\sum_{l\in H}L_{\mathrm{rec},l}
+\frac1{32}\frac1K\sum_{l\in H}L_{\mathrm{AuxK},l},
\]

with \(\lambda_{\mathrm{rec}}=1\). AuxK is absent from the reconstruction-only ratio and has no backbone gradient. On the exact intersection of shared backbone parameters,

\[
\rho=\frac{\lVert g_A\rVert}{\lVert g_C\rVert},
\qquad
c=\frac{g_C^\top g_A}{\lVert g_C\rVert\lVert g_A\rVert}.
\]

The shared set excludes both legacy `sae.*` and newer `saes.*` parameters and contains 281,431,040 scalar parameters for S7/S37/SALL. Four fixed batches were used per model-checkpoint cell. A direction is reported only when both norms exceed the registered numerical threshold.

## 3. Execution, Failures, And Repairs

| Stage | Job / receipt | Result | Scientific effect |
| --- | --- | --- | --- |
| Smoke v1 | `pt-nblfsfgm` | stopped after the legacy M2 config lacked a newer hook field | no result; parser incompatibility only |
| Smoke v2 | local/remote qualification | operationally passed, then invalidated because legacy `sae.*` parameters were mistakenly included in the common set | no gradient claim retained |
| Smoke v3 | `pt-4z1uhh31` | PASS on 4/4 RTX 5090 Spot GPUs; shared dimension 281,431,040; peak allocated CUDA memory 8.99 GB | authorized the full collection |
| Full collection | `pt-6x2z6ot6` | 30/30 exact cells PASS; peak CUDA memory 11,362,489,856 bytes; zero optimizer updates | complete immutable caches and gradient JSON |
| Initial synthesis | same job | stopped after collection because probe work was imbalanced across GPUs | collection remained valid; no incomplete probe result retained |
| Recovery v1 | `pt-ky6wrdd3` | stopped after detecting that every shard eagerly repeated the expensive B2 SVD | no result change; scheduling defect only |
| Recovery v2 | `pt-8zbr996d` | 672/672 probe cells PASS in eight balanced shards; 13 original tables and 13 original figures; terminal receipt PASS | complete synthesis |
| Reader refinement | local CPU | generated three clearer reader figures and one compact 10B source table | no metric recomputation or source-row change |

The final result has 30/30 collection cells, 672/672 probe cells, 14 CSV tables, and 16 PNG figures. Local implementation tests passed `9/9`. No optimizer was created and no checkpoint was modified.

### Recorded protocol deviation

The protocol named 2,000 explicitly sampled isotropic directions, 2,000 coordinate randomizations, and cross-batch off-diagonal pairings. For the 281,431,040-dimensional whole-backbone vector, execution used the analytic high-dimensional isotropic normal quantile and an analytic magnitude-preserving Rademacher sign-flip distribution instead of materializing 2,000 full vectors. This is a more memory-stable estimate of the registered null at this dimension, but it is a method deviation and is recorded as such. Whole-backbone cross-batch off-diagonal pairings were not retained because full gradient vectors were not persisted. The result therefore supports “outside the isotropic and analytic sign-flip nulls,” not a claim based on all three originally listed null implementations.

## 4. Results

### 4.1 Fisher credibility and native representation

All exact-10B absolute Fisher values in P/N and raw/B2 coordinates exceeded their 1,000-draw balanced-label permutation distributions; every reported upper-tail value was \(1/1001=0.000999\). This establishes that the labels define measurable geometry in every model. It does not establish that model differences are useful.

Exact-10B native-final Fisher differences versus M0 were:

| Dataset | Transform | S7, estimate [95% CI] | S37, estimate [95% CI] | SALL, estimate [95% CI] |
| --- | --- | ---: | ---: | ---: |
| P | raw | +0.3275 [-0.0420, 0.3966] | +0.4299 [0.0316, 0.4932] | +0.4471 [0.0453, 0.5230] |
| P | B2 | +0.2922 [-0.0375, 0.3571] | +0.3793 [0.0317, 0.4448] | +0.3960 [0.0454, 0.4710] |
| N | raw | +0.0091 [-0.0012, 0.0190] | +0.0087 [0.0002, 0.0186] | +0.0205 [0.0137, 0.0291] |
| N | B2 | +0.0107 [0.0005, 0.0214] | +0.0113 [0.0033, 0.0208] | +0.0212 [0.0144, 0.0298] |

The large P endpoint gap is not a stable separation of sidecar trajectories. P-raw Fisher for M0 was 0.039/0.361/0.432/0.383/0.520/0.054 over 0/0.5/1/3/5/10B, while S37 was 0.039/0.317/0.429/0.509/0.524/0.484 and SALL was 0.039/0.337/0.450/0.404/0.464/0.501. The 10B difference is therefore heavily influenced by the M0 endpoint drop. N was smoother and showed small endpoint separation.

At exact 10B, P-raw linear/neural balanced accuracy was M0 0.9889/0.9967, S7 0.9833/0.9878, S37 0.9944/1.0000, and SALL 0.9889/0.9878. N-raw was M0 0.8100/0.8045, S7 0.8300/0.8145, S37 0.8300/0.8165, and SALL 0.8475/0.8145. The probe point differences are small relative to the P Fisher shift and have no training-seed uncertainty estimate.

### 4.2 Raw Attention output versus SAE reconstruction

Across the eleven terminal sidecar-layer pairs:

| Coordinate / dataset | Reconstruction Fisher higher | Reconstruction linear probe higher | Mean linear-probe difference |
| --- | ---: | ---: | ---: |
| P raw | 5/11 | 0/11 | -0.0742 |
| P B2 | 6/11 | 0/11 | -0.0732 |
| N raw | 8/11 | 1/11 | -0.0327 |
| N B2 | 8/11 | 1/11 | -0.0336 |

This separates geometry from accessibility: SAE reconstruction can increase \(B/W\) while reducing held-out linear readability. Sidecar reconstructions are not on the native S7/S37/SALL forward path, so these cells cannot establish native model use.

### 4.3 Token-aligned and held-out language loss

The last complete 100M-token training bin at or before 10B and the frozen M2D2 report panel gave:

| Model | Training NLL | Training delta vs M0 | Held-out NLL | Held-out delta vs M0 |
| --- | ---: | ---: | ---: | ---: |
| M0 | 3.34677 | 0 | 3.61427 | 0 |
| M2 | 3.34098 | -0.00579 | 3.60182 | -0.01245 |
| S7 | 3.35767 | +0.01091 | 3.62156 | +0.00729 |
| S37 | 3.35173 | +0.00496 | 3.63279 | +0.01853 |
| SALL | 3.34449 | -0.00227 | 3.62045 | +0.00619 |

SALL's slightly lower training NLL did not transfer to the frozen held-out panel. No sidecar condition improved the held-out loss at 10B.

### 4.4 Loss scale and shared-parameter gradient scale

| Model | K | Direct coefficient | Weighted reconstruction | Reconstruction / LM | \(\|g_C\|\) | \(\|g_A\|\) | \(\rho\) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| S7 | 1 | 1.000 | 0.10017 | 0.02983 | 2.67898 | 0.09493 | 0.03538 |
| S37 | 2 | 0.500 | 0.22083 | 0.06589 | 2.80670 | 0.08572 | 0.03055 |
| SALL | 8 | 0.125 | 0.17216 | 0.05148 | 2.72564 | 0.03377 | 0.01240 |

The loss ratio does not order the models like the gradient ratio. Layer-mean aggregation with common total coefficient one does not equalize total shared-backbone pressure. S7's 10B \(\rho\) is 2.85 times SALL's.

The \(\rho\) trajectories for 0/0.5/1/3/5/10B were:

- S7: 0.1853, 0.1495, 0.0292, 0.0392, 0.0347, 0.0354.
- S37: 0.1258, 0.0799, 0.0643, 0.0291, 0.0256, 0.0306.
- SALL: 0.0661, 0.0152, 0.0146, 0.0151, 0.0143, 0.0124.

The strong time dependence rules out one fixed coefficient as an exact whole-training balancer.

### 4.5 Direction and random calibration

At 10B, S7/S37/SALL had mean signed cosines 0.01348/0.00595/0.01208 and mean angles 89.23°/89.66°/89.31°. The dimension-matched isotropic 97.5% absolute-cosine bound for the full shared vector was 0.0001168. All 72 whole-backbone cells were direction-reliable and all 72 were outside this band; only 7/72 had analytic sign-flip two-sided \(p\ge0.05\). Batch-level cosine signs were S7 18 positive / 6 negative, S37 6 / 18, and SALL 12 / 12 across checkpoints.

The result is structured near-orthogonality, not random-compatible orthogonality and not stable alignment. At 10B, \(\rho c\) was 0.000477/0.000182/0.000150, so the measured first-order component parallel to the language gradient was small. The 72 `final_norm` control rows had exactly zero auxiliary gradient; cosine and angle were correctly blank and marked direction-unreliable.

### 4.6 Feature usage

On the N panel at 10B, active fractions included S7 layer 7 = 0.0207; S37 layer 3 = 0.9267 and layer 7 = 0.6163; SALL ranged from 0.4422 at layer 1 to 0.9657 at layer 0, with layer 7 = 0.6003. For example, SALL layer 7 retained 0.3187 of the dictionary, added 0.2816, and lost 0.0559 relative to 5B. These are panel usage statistics, not semantic feature identities.

## 5. Insight, Claim Boundary, And Next Decision

### Evidence-grounded insight

The SAE sidecar measurably reorganizes representation geometry, but the present evidence does not connect that reorganization to a stable improvement in native accessibility or held-out language modeling. Fisher remains useful only when reported with \(B\), \(W\), probe behavior, direct top-direction removal, and label-permutation credibility. The gradient analysis resolves the earlier ambiguity: angles near 90 degrees are not random-compatible in the full parameter dimension, yet their signed first-order component along the language gradient is tiny and unstable. This is a diagnostic fact, not a demonstrated optimization mechanism.

### Coefficient implication

Equal total `lambda_rec=1` with layer averaging does not equalize total shared-backbone gradient pressure. Equal direct per-sidecar weights (`0.1/0.2/0.8`) would also not equalize it under the measured Jacobians. A better controlled intervention targets total \(\rho\). A conservative AI-proposed target is 0.02 with calibration-window or EMA adjustment. Exact-10B scaling would suggest total coefficients 0.57/0.65/1.61 for S7/S37/SALL; the 3/5/10B median gives 0.57/0.69/1.40. These are initialization points for a test, not optima.

### Nearest claim boundary

This is a single-seed comparison of already trained, non-paired trajectories. It cannot establish increased parameter capacity, general language ability, a causal effect of sidecar count, semantic feature identity, native use of SAE reconstruction, or a special mechanism for escaping local optima. Probe and bootstrap uncertainty do not include training-seed uncertainty.

### AI-proposed next decision

Run one matched coefficient intervention on the two extremes, S7 and SALL: current `lambda=1` versus an online target \(\rho=0.02\), with identical initialization, token order, global batch, optimizer, and schedule. Measure 0/0.1/0.25/0.5/1B first. Continue to 3/5/10B only if both layer-count conditions reach the target range without worse frozen-M2D2 NLL. If balancing \(\rho\) does not remove the S7/SALL difference, stop attributing it to sidecar-count-induced gradient-norm imbalance.

## 6. Artifact Map

### Decisive figures

- [Native B/W/F trajectories](figures/13_geometry_trajectory_reader.png)
- [Exact-10B Fisher differences and bootstrap intervals](figures/14_fisher_10b_credibility_reader.png)
- [Linear-probe trajectories](figures/03_linear_probe.png)
- [Two-layer neural-probe trajectories](figures/04_two_layer_probe.png)
- [Training language loss](figures/05_language_loss.png)
- [Frozen M2D2 held-out loss](figures/12_heldout_m2d2_language_loss.png)
- [Reconstruction loss scale](figures/06_reconstruction_loss_scale.png)
- [Raw Attention versus SAE reconstruction](figures/10_terminal_raw_vs_reconstruction.png)
- [Shared-gradient magnitude and random calibration](figures/15_shared_gradient_random_calibration_reader.png)
- [Feature activity trajectory](figures/08_feature_activity_trajectory.png)

### Source tables

- [Exact-10B sidecar loss/gradient comparison](tables/exact_10b_sidecar_loss_gradient_comparison.csv)
- [Representation geometry](tables/representation_geometry.csv)
- [Fisher credibility](tables/fisher_10b_credibility.csv)
- [Linear probes](tables/linear_probe.csv)
- [Two-layer neural probes](tables/two_layer_neural_probe.csv)
- [Training loss and coefficient ledger](tables/loss_coefficient_checkpoint_ledger.csv)
- [Frozen M2D2 language loss](tables/heldout_m2d2_language_loss.csv)
- [Shared-parameter gradient batch rows](tables/shared_parameter_gradient_metrics.csv)
- [Shared-parameter gradient checkpoint summary](tables/shared_parameter_gradient_checkpoint_summary.csv)
- [Terminal raw/reconstruction rows](tables/terminal_raw_vs_reconstruction.csv)
- [Feature trajectories](tables/feature_trajectory.csv)

### Raw representation caches

- M0/M2 qualified representation cache root: `/data/250010109/MoE_Router/experiments/20260915_three_model_representation_audit/runs/full_h100_reserved_v4/caches/`.
- S7/S37/SALL E05 representation cache root: `/data/250010109/MoE_Router/experiments/20260918_multimodel_fisher_gradient_coefficient_audit/runs/full_5090_4spot_10b_v1/caches/`.
- File name rule: `{MODEL}_{TOKENS:012d}.npz`, for exact tokens `0/500000000/1000000000/3000000000/5000000000/10000000000`.
- Synthesis routing that selects the two roots and field names: `/data/250010109/MoE_Router/experiments/20260918_multimodel_fisher_gradient_coefficient_audit/scripts/analyze.py`, functions `cache_path` and `surfaces`.

### Runtime receipts

- `analysis_recovery_terminal_receipt.json`: terminal PASS, zero optimizer updates, `5090-4-spot`.
- `stages/COLLECTION_PASS.json`: 30/30 exact cells.
- `stages/ANALYSIS_PROBE_BALANCED_SHARD_{0..7}_PASS.json`: eight complete balanced shards.
- `stages/S4_SYNTHESIS_PASS.json`: final synthesis PASS.
