# A05_04_02 Common Source B-Path And No-B Detailed Record

## 0. Quick Recap

Purpose: audit whether the fixed `B_CONST` token is a major source of common-logit dominance in the original B-position sparse top-1 MoE task.

Hypothesis: the direct `B_CONST` residual identity entering the routed hidden state is a major common source; B self-attention value contribution is a rival source; residual common/top-1 lock-in may persist even without B.

Experiment logic: P1 applies counterfactual patches to existing Round-1 B-position checkpoints. P2 removes `B_CONST` from the sequence and retrains dot-product top-1 MoE variants.

Conclusion: the direct B residual path is a major contributor to common-logit collapse. B self-value attention is not the main source. Deleting B improves specialization but does not eliminate collapse under random initialization.

Evidence: P1 `no_b_residual` raises final NMI from `0.080` to `0.797` and reduces common margin from `2.316` to `0.271`; P1 `no_b_self_value` leaves NMI at `0.080`; P2 no-B baseline reaches mean NMI `0.802` but has one collapsed seed; P2 no-B early cancellation reaches mean NMI `0.930` and minimum NMI `0.843`.

## Source Files

- Protocol: `protocol_for_approval.md`
- Runner: `scripts/run_common_source_b_path_and_no_b.py`
- Submit script: `scripts/submit_common_source_b_path_and_no_b_4gpu_acp.sh`
- Reference Round-1 checkpoints: `../A05_04_01_round1_slot_specialization_protocol_dot_product/results/round1_slot_specialization_dot_product_4gpu_20260609`

## Run Metadata

- Run name: `common_source_b_path_and_no_b_4gpu_20260610`
- ACP job id: `pt-8wd06kh3`
- Job status: `SUCCEEDED`
- Seeds: `20260521` to `20260528`
- Checkpoints: `0, 1, 2, 5, 10, 20, 50, 1600`
- Result dir: `results/common_source_b_path_and_no_b_4gpu_20260610`
- Figure dir: `figures/common_source_b_path_and_no_b_4gpu_20260610`
- Runtime log: `logs/acp/common_source_b_path_and_no_b_4gpu_20260610_runtime_20260610_053846.log`
- Submit log: `logs/acp/common_source_b_path_and_no_b_4gpu_20260610_submit_20260610_053805.log`

## Data

P1 uses the original Round-1 task:

```text
prefix filler + SLOT_s B_CONST Y_s + suffix filler
```

- `SLOT_s B_CONST Y_s` is contiguous.
- Positional encoding is disabled by zeroing and freezing positional embeddings.
- Loss and routing metrics are at the `B_CONST` position.
- P1 is diagnostic only: it does not retrain under the patch.

P2 uses the no-B task:

```text
prefix filler + SLOT_s Y_s + suffix filler
```

- Loss and routing metrics are at the `SLOT_s` position.
- The target is still `Y_s`.
- The dataset keeps the Round-1 slot/start balancing logic, adjusted for the shorter contiguous block.

## Model And Training

- Model: same tiny no-position transformer + sparse top-1 MoE used in Round 1 and Round 2.
- Router: dot-product router, `score_e(h) = w_e^T h`.
- Routing: sparse top-1 only.
- No soft routing, no top-k with `k > 1`, no probability-weighted expert mixtures beyond the existing selected-gate scalar in the Round-1 model implementation.
- Full training steps: `1600`.
- Seeds: `8`.
- Train repeats per pair: `500`.
- Eval repeats per pair: `32`.
- Batch size: `384`.
- Eval batch size: `512`.

## P1 B-Path Attribution

P1 loads each Round-1 `P1_clean_baseline` dot-product checkpoint and recomputes routed hidden states under four conditions:

| condition | operation | purpose |
|---|---|---|
| `original` | use standard `h_B = LN(x_B + attention_output_B)` | reference collapse state |
| `no_b_residual` | replace the routed-position residual `x_B` with zero, keep attention output | isolate the direct B residual path |
| `no_b_self_value` | subtract only B's self-value contribution through attention | test whether B self-attention value is the source |
| `no_b_full_embedding` | zero B embedding and recompute attention | test full B embedding removal, with known destructiveness risk |

Final aggregate:

| condition | final NMI | max load | active experts | common margin | slot margin | mean hidden delta |
|---|---:|---:|---:|---:|---:|---:|
| `original` | 0.080 | 0.969 | 1.125 | 2.316 | 0.556 | 0.000 |
| `no_b_residual` | 0.797 | 0.550 | 2.875 | 0.271 | 0.434 | 8.346 |
| `no_b_self_value` | 0.080 | 0.969 | 1.125 | 2.259 | 0.542 | 1.129 |
| `no_b_full_embedding` | 0.256 | 0.812 | 3.125 | 0.378 | 0.180 | 14.515 |

Interpretation:

- `no_b_residual` is the cleanest positive source evidence: it sharply reduces common margin and improves NMI.
- `no_b_self_value` is the cleanest negative source evidence: the self-value path barely matters.
- `no_b_full_embedding` is not a clean success because it also damages slot margin.

## P2 No-B Training

P2 retrains on `SLOT_s Y_s` under three variants:

| variant | intervention | purpose |
|---|---|---|
| `NoB_baseline` | no B, random initialization, no cancellation | test whether deleting B alone is sufficient |
| `NoB_cancel_0_10` | no B, common cancellation through step 10 | test early anti-common lock-in prevention |
| `NoB_cancel_0_final` | no B, common cancellation through all steps | test persistent cancellation |

Final aggregate:

| variant | mean NMI | min NMI | max load | active experts | accuracy | common margin | slot margin |
|---|---:|---:|---:|---:|---:|---:|---:|
| `NoB_baseline` | 0.802 | 0.083 | 0.497 | 3.125 | 1.000 | 1.396 | 2.841 |
| `NoB_cancel_0_10` | 0.930 | 0.843 | 0.372 | 3.625 | 1.000 | 0.898 | 3.158 |
| `NoB_cancel_0_final` | 0.918 | 0.613 | 0.372 | 3.625 | 1.000 | 0.905 | 3.215 |

Seed-level final results:

| variant | seed | NMI | max load | active experts | accuracy | common margin | slot margin |
|---|---:|---:|---:|---:|---:|---:|---:|
| `NoB_baseline` | 20260521 | 1.000 | 0.250 | 4 | 1.000 | 0.491 | 3.217 |
| `NoB_baseline` | 20260522 | 0.866 | 0.500 | 3 | 1.000 | 1.248 | 3.068 |
| `NoB_baseline` | 20260523 | 0.083 | 0.977 | 2 | 1.000 | 4.249 | 0.480 |
| `NoB_baseline` | 20260524 | 0.866 | 0.500 | 3 | 1.000 | 1.422 | 2.998 |
| `NoB_baseline` | 20260525 | 0.866 | 0.500 | 3 | 1.000 | 1.430 | 3.442 |
| `NoB_baseline` | 20260526 | 0.866 | 0.500 | 3 | 1.000 | 0.469 | 2.677 |
| `NoB_baseline` | 20260527 | 0.866 | 0.500 | 3 | 1.000 | 1.356 | 3.367 |
| `NoB_baseline` | 20260528 | 1.000 | 0.250 | 4 | 1.000 | 0.506 | 3.477 |
| `NoB_cancel_0_10` | 20260521 | 1.000 | 0.250 | 4 | 1.000 | 0.402 | 3.196 |
| `NoB_cancel_0_10` | 20260522 | 0.866 | 0.500 | 3 | 1.000 | 1.555 | 3.118 |
| `NoB_cancel_0_10` | 20260523 | 0.866 | 0.500 | 3 | 1.000 | 0.858 | 3.170 |
| `NoB_cancel_0_10` | 20260524 | 1.000 | 0.250 | 4 | 1.000 | 0.288 | 3.260 |
| `NoB_cancel_0_10` | 20260525 | 0.843 | 0.477 | 4 | 1.000 | 1.483 | 2.956 |
| `NoB_cancel_0_10` | 20260526 | 0.866 | 0.500 | 3 | 1.000 | 2.118 | 2.804 |
| `NoB_cancel_0_10` | 20260527 | 1.000 | 0.250 | 4 | 1.000 | 0.087 | 3.218 |
| `NoB_cancel_0_10` | 20260528 | 1.000 | 0.250 | 4 | 1.000 | 0.394 | 3.545 |
| `NoB_cancel_0_final` | 20260521 | 1.000 | 0.250 | 4 | 1.000 | 0.389 | 3.186 |
| `NoB_cancel_0_final` | 20260522 | 0.866 | 0.500 | 3 | 1.000 | 1.920 | 3.108 |
| `NoB_cancel_0_final` | 20260523 | 0.866 | 0.500 | 3 | 1.000 | 0.525 | 3.096 |
| `NoB_cancel_0_final` | 20260524 | 1.000 | 0.250 | 4 | 1.000 | 0.399 | 3.244 |
| `NoB_cancel_0_final` | 20260525 | 1.000 | 0.250 | 4 | 1.000 | 0.398 | 3.306 |
| `NoB_cancel_0_final` | 20260526 | 0.613 | 0.727 | 3 | 1.000 | 2.798 | 2.974 |
| `NoB_cancel_0_final` | 20260527 | 1.000 | 0.250 | 4 | 1.000 | 0.513 | 3.351 |
| `NoB_cancel_0_final` | 20260528 | 1.000 | 0.250 | 4 | 1.000 | 0.299 | 3.453 |

Interpretation:

- No-B baseline is much better than the original B baseline, so B is a strong collapse amplifier.
- No-B baseline is not fully robust, so B is not the only possible common source.
- Early cancellation is more robust than full-run cancellation in this run, so the intervention is better interpreted as early anti-lock-in rather than permanent common removal.

## Figures

![P1 B-path common margin](figures/common_source_b_path_and_no_b_4gpu_20260610/p1_b_path_common_margin.png)

![P2 no-B final routing](figures/common_source_b_path_and_no_b_4gpu_20260610/p2_no_b_final_routing.png)

## Claim Boundary

This audit can identify source contributors, but it does not identify the full common source. It does not prove real-language-model transfer, does not prove expert computation is causally slot-specialized, and does not treat load balance alone as specialization.

## Artifact Map

- Curated summary: `summary.md`
- Curated detailed record: `detailed.md`
- Run-local summary: `results/common_source_b_path_and_no_b_4gpu_20260610/summary.md`
- Run-local detailed record: `results/common_source_b_path_and_no_b_4gpu_20260610/detailed.md`
- P1 metrics: `results/common_source_b_path_and_no_b_4gpu_20260610/p1_b_path_metrics_by_seed_step.csv`
- P1 routes: `results/common_source_b_path_and_no_b_4gpu_20260610/p1_b_path_route_confusion.csv`
- P1 margins: `results/common_source_b_path_and_no_b_4gpu_20260610/p1_b_path_margin_decomposition.csv`
- P2 metrics by step: `results/common_source_b_path_and_no_b_4gpu_20260610/p2_no_b_metrics_by_step.csv`
- P2 final metrics: `results/common_source_b_path_and_no_b_4gpu_20260610/p2_no_b_final_metrics.csv`
- P2 routes: `results/common_source_b_path_and_no_b_4gpu_20260610/p2_no_b_route_confusion.csv`
- P2 margins: `results/common_source_b_path_and_no_b_4gpu_20260610/p2_no_b_margin_decomposition.csv`
- Figure directory: `figures/common_source_b_path_and_no_b_4gpu_20260610`
