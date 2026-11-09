# Protocol: A15_08_04_E01 DCLM Transition-Object Spectrum Comparison

## 0. Approval Snapshot

- **Document status:** `APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN`
- **Approval status:** researcher explicitly replied “按此执行” on 2026-08-17 after the eight object definitions were surfaced, then explicitly requested continued execution and result display.
- **Block audit status:** A--G `CONFIRMED`
- **Cross-block consistency:** `PASS`
- **Execution scope approved:** implementation, 128-token smoke, 2,048-token full run, analysis, and local result figures; no commit, push, publication, graph edit, or root-sync publication.
- **Design frozen at:** 2026-08-17 before model execution.
- **Purpose:** test whether centered covariance spectra are sensitive to transition-object and RMSNorm definitions under identical natural-text tokens.
- **Primary Anchor:** [A15_08_04](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_04_transition_object_spectrum_sensitivity_anchor.md)
- **Experiment role:** metric/object-definition audit.
- **Primary metric:** matched layerwise difference in \(r_{80}/2047\) for three raw-versus-RMSNorm contrasts.
- **Treatment and controls:** RMSNorm-transformed matrices versus their raw counterparts; same model forward, tokens, layer, centering, spectrum estimator, rank cap, and axes.
- **Pass:** any registered contrast has median absolute paired difference at least 0.05 and directional consistency at least 0.70.
- **Fail:** every contrast has median absolute paired difference below 0.02 and directional consistency below 0.70.
- **Insufficient:** intermediate outcome or any validity-guard failure.
- **Cannot claim:** new information, semantic function, causal use, population-intrinsic rank, expert identity, or Router utility.

## 1. Terminology / Definitions

For block \(\ell\), \(h_\ell\) is the raw residual entering Attention; \(a_\ell\) is the raw Attention write at `self_attn.o_proj`; \(r_\ell=h_\ell+a_\ell\) is the post-Attention raw residual; \(N_\ell\) is the block's `post_attention_layernorm`; \(X_\ell=N_\ell(h_\ell)\); \(Z_\ell=N_\ell(r_\ell)\) is the actual MLP input; and \(U_\ell=Z_\ell-X_\ell\).

The **covariance spectrum** is the descending eigenvalue share of the token-centered sample covariance. \(r_{80}\) is the minimum number of directions containing 80% of its total variance. It measures geometric concentration only.

## 2. Anchor Alignment

The experiment tests A15_08_04's object-definition sensitivity clause. It does not reopen A15_08_02 functional admission or A15_08_03 functional compression. The strongest rival is that spectrum shape is robust after data, sample count, estimator, and axes are aligned.

## 3. Tested Hypothesis

`H-SENS`: RMSNorm placement or transition-object identity produces a material and layer-systematic change in normalized \(r_{80}\). The operational Pass/Fail/Insufficient mapping is frozen in Sections 10 and 15.

## 4. Rival Explanations

1. **R-DATA:** previous differences came from different token populations or sample sizes. Controlled by one shared DCLM slice.
2. **R-ESTIMATOR:** previous differences came from centering, normalization, rank truncation, or plot scaling. Controlled by one shared estimator and axes.
3. **R-HOOK:** an apparent difference comes from a wrong hook identity. Controlled by native MLP-input reconstruction, \(Z=X+U\), replay, and layer-coverage guards.

## 5. Data Construction And Provenance

- Source file: `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_0_of_10_shard_00000000_processed.bin`.
- Encoding: raw `uint32` token IDs.
- Full-run slice: offset 0, exactly 2,048 consecutive IDs.
- Smoke slice: the first 128 IDs of the same frozen slice.
- Observation row: one token position in the contiguous causal sequence.
- Independence boundary: token rows are correlated; no population confidence interval is reported.
- Provenance: record source size, SHA-256, slice SHA-256, token count, minimum/maximum ID, and model tokenizer vocabulary bound.

## 6. Learning Task And Permitted Supervision

There is no learning task, label, fitting, split selection, or supervision. The only output is a deterministic activation-spectrum atlas and registered sensitivity table.

## 7. Model / Architecture And Frozen Variants

- Model: local `/data/share/Qwen3-8B`, 36 decoder blocks, hidden width 4,096.
- Precision: model weights/forward in bfloat16; spectrum matrices and eigendecomposition in float32.
- Attention implementation: SDPA, `use_cache=False`, inference/eval mode.
- Hook sites: each block forward pre-hook for \(h_\ell\); each `self_attn.o_proj` forward hook for \(a_\ell\); each MLP forward pre-hook for native \(Z_\ell\) identity.
- One GPU; no sharding, compilation, gradient, or stochastic sampling.

## 8. Training Objective And Optimization

Not applicable. No parameters are changed. Random seeds are fixed only for deterministic environment setup; the data slice is not sampled.

## 9. Conditions, Seeds, And Checkpoints

| Condition | Matrix | Curves |
| --- | --- | ---: |
| `adjacent_attention_write_difference` | \(a_{\ell+1}-a_\ell\) | 35 |
| `adjacent_pre_attention_raw_residual_difference` | \(h_{\ell+1}-h_\ell\) | 35 |
| `adjacent_pre_attention_rmsnorm_difference` | \(X_{\ell+1}-X_\ell\) | 35 |
| `adjacent_post_attention_raw_residual_difference` | \(r_{\ell+1}-r_\ell\) | 35 |
| `adjacent_actual_mlp_input_rmsnorm_difference` | \(Z_{\ell+1}-Z_\ell\) | 35 |
| `same_layer_normalized_update_u` | \(U_\ell=Z_\ell-X_\ell\) | 36 |
| `post_attention_raw_residual_state` | \(r_\ell\) | 36 |
| `actual_mlp_input_rmsnorm_state` | \(Z_\ell\) | 36 |

The layer labels are 1--36; adjacent labels are 1→2 through 35→36. Seed is 8170401 for framework determinism only. There are no checkpoints.

## 10. Primary Metric And Frozen Analysis Plan

For each \(M\in\mathbb R^{2048\times4096}\), subtract the column mean, compute \(G=MM^\top/2047\), use `eigvalsh`, sort descending, clip negative roundoff to zero, and normalize \(p_j=\lambda_j/\sum_k\lambda_k\). Reject traces below \(10^{-12}\) or non-finite outputs.

Compute \(r_{80}/2047\) for every curve. For the three matched contrasts \((\Delta X,\Delta h)\), \((\Delta Z,\Delta r)\), and \((Z,r)\), report:

1. median absolute paired layer difference;
2. median signed difference;
3. positive and negative directional fractions, with directional consistency their maximum.

No statistical interval is claimed because layers and token positions are not population-independent. Missing or failed curves make the full verdict `INSUFFICIENT`; no imputation or outlier exclusion is allowed.

## 11. Secondary Metrics And Guards

- Effective rank \(\exp(-\sum_jp_j\log p_j)\).
- Covariance trace before normalization, to expose scale removed from spectrum shape.
- Rank-50%, rank-90%, and top-1/top-16 variance shares.
- Exact layer coverage, matrix shape, finite-value, eigenspectrum monotonicity, and normalized-sum guards.
- Identity guards: native MLP input versus reconstructed \(Z\); \(Z-X-U\); repeated 128-token forward replay.

## 12. Known Good / Known Bad / Known Confusing Cases

- Known good: a synthetic rank-\(k\) matrix must return \(r_{80}\le k\) and finite normalized spectrum.
- Known bad: a constant matrix must be rejected for negligible centered trace.
- Known confusing: centering 2,048 rows forces rank at most 2,047; rank 2,048 is displayed at the log floor and never counted as signal.
- Known confusing: normalized spectra compare shape, not total variance; trace is reported separately.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal | Input / how | Required output and gate |
| --- | --- | --- | --- |
| Preflight | verify data/model/environment | hash source, load slice, check CUDA/model/token IDs | `preflight.json`; all guards pass |
| Unit tests | verify spectrum/objects/plots | synthetic tensors and exact formulas | focused tests pass |
| Smoke | verify 128-token hooks and identities | one short forward, all 36 layers | replay and reconstruction guards pass |
| Full extraction | collect shared 2,048-token activations | one frozen forward | activation manifest and hashes |
| Spectrum analysis | compute all 283 registered curves | centered float32 Gram eigenspectra | NPZ and full metric table |
| Rendering | create per-condition and aggregate figures | frozen spectra and axes | 8 individual figures, grid, median overlay |
| Verdict | apply registered matched-contrast rule | metric table only | verdict, summary, detailed record |

Any failed earlier gate stops later interpretation. A retry may correct an implementation or resource failure without changing the scientific body; any data, object, metric, or threshold change requires an append-only amendment and renewed approval.

## 14. Algorithm, Output, And Provenance Contract

- Code root: `Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_08_04_e01_dclm_transition_object_spectrum_comparison/`.
- Raw run root: `/data/250010109/MoE_Router/experiments/20260817_a15_08_04_e01_dclm_transition_object_spectrum_comparison/runs/a15-08-04-e01-20260817-full/`.
- Canonical result root: this Protocol directory.
- Raw outputs: `preflight.json`, `extraction_manifest.json`, `arrays/spectra.npz`, `tables/spectrum_metrics.csv`, `tables/paired_contrasts.csv`, `figures/*.png`, `figures/*.pdf`, `verdict.json`, and artifact manifest.
- Canonical outputs after eligible execution: `summary.md`, `detailed.md`, selected figures/tables, and result links in the Anchor.

## 15. Success / Failure / Insufficient Evidence

- `DEFINITION_SENSITIVE`: any primary contrast reaches both median absolute \(r_{80}\)-fraction difference \(\ge0.05\) and directional consistency \(\ge0.70\).
- `DEFINITION_ROBUST_WITHIN_TOLERANCE`: every primary contrast has median absolute difference \(<0.02\) and directional consistency \(<0.70\).
- `INSUFFICIENT`: any intermediate numerical pattern or validity/conformance failure.

Secondary spectra cannot rescue or overturn this rule.

## 16. What This Cannot Claim

This audit cannot call any object new information, identify semantic directions, establish model-native use, estimate population-intrinsic rank, compare downstream task utility, or justify a Router. It also cannot generalize beyond Qwen3-8B and the frozen contiguous DCLM slice without a new Protocol.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | State | Grounding |
| --- | --- | --- |
| A Question/boundary | `CONFIRMED` | researcher requested separate Anchor/Protocol and approved exact objects |
| B Data/provenance | `CONFIRMED` | researcher fixed DCLM and 2,048 tokens; deterministic canonical slice is execution choice |
| C Task/supervision | `CONFIRMED` | geometry-only spectrum audit, no labels |
| D Model/architecture | `CONFIRMED` | same Qwen3-8B and approved hook definitions |
| E Objective/optimization | `CONFIRMED` | no learning |
| F Comparison/evidence | `CONFIRMED` | full-layer figures, common axes, aggregate comparison, frozen sensitivity rule |
| G Execution/reproducibility | `CONFIRMED` | implementation, smoke, full run and local figures explicitly approved |

Cross-block consistency: `PASS`. Scientific body frozen before execution. Post-start changes require append-only amendment with eligibility impact.

