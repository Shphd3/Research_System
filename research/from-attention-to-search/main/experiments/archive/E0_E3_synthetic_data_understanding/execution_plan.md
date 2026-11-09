# Execution Plan: E0-E3 Synthetic Data Understanding

## 1. Run Goal

Run the 0513 data-understanding line as a gated sequence, where each stage must
make the next stage interpretable.

## 2. Stage Gates

```text
E0_data_sanity
-> E1_dense_feature_readback
-> E2_moe_feature_separation
   -> versions/E2_0_moe_feature_separation
   -> versions/E2_1_router_input_geometry
   -> versions/E2_2_specialization_pressure
   -> versions/E2_3_router_behavior_decomposition
-> E3_synthetic_vs_real_statistics
-> optional E4_hierarchical_phrase_extension
```

Gate rules:

- If E0 fails, do not train dense or MoE models.
- If E1 fails, do not discuss MoE specialization.
- Treat E2 as a package: E2.0 tests feature-expert alignment, E2.1 diagnoses router input geometry, and E2.2 tests specialization pressure.
- If E2.1 shows router input is separable but boundaries are weakly aligned, do not claim one-feature-one-expert.
- If E2.2 shows pressure does not improve alignment, run router behavior decomposition before adding more synthetic complexity.
- E2.3 shared-B control is complete. It weakens the simple `B_token` shortcut
  explanation. Next use shared-target / crossed-target data if target-token
  shortcut remains plausible.
- E3 compares statistics, not model transfer.
- E4 is optional and only starts after E0-E2 are clean.

## 3. Operational Workspace

Runnable scripts and generated artifacts live outside `main`:

```text
../../../Attention_Search_Experiments/active/synthetic_data_understanding/
```

Mainline-safe planning and later summaries live here:

```text
experiments/E0_E3_synthetic_data_understanding/
```

## 4. Source Notes

The original 0513 planning notes are copied under `source_notes/`. Treat them as
raw material, not as claim-safe results.

## 5. Result Promotion

After each stage, add:

```text
stages/<stage_id>/summary.md
stages/<stage_id>/detailed.md
```

Only update project `current_mainline.md`, `consensus.md`, or `status.md` if a
stage changes the safest claim, hypothesis status, claim boundary, or next
decision.
