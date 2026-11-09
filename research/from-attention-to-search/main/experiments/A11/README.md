# A11 Experiment Registry

A11 experiments inherit the parent-anchor identifier. The active format is:

```text
A11_<parent>_<subanchor>_E<experiment>
```

| Parent group | Main decision evidence | Canonical anchor |
|---|---|---|
| [`11_01_informative_horizon_supervision/`](11_01_informative_horizon_supervision) | Does an informative future target create a direct current-state signal, and how do output directions combine? | [`11_01`](../../problem_anchors/11_informative_future_branch_mechanism/11_01_informative_horizon_supervision/11_01_informative_horizon_supervision_anchor.md) |
| [`11_02_hidden_to_parameter_transmission/`](11_02_hidden_to_parameter_transmission) | Can the signal reach shared parameters under signed all-position background? | [`11_02`](../../problem_anchors/11_informative_future_branch_mechanism/11_02_hidden_to_parameter_transmission/11_02_hidden_to_parameter_transmission_anchor.md) |
| [`11_03_cross_position_standard_head_use_boundary/`](11_03_cross_position_standard_head_use_boundary) | Does current-state formation survive to standard-head behavior? | [`11_03`](../../problem_anchors/11_informative_future_branch_mechanism/11_03_cross_position_standard_head_use_boundary/11_03_cross_position_standard_head_use_boundary_anchor.md) |

Completed decision record under `11_03`:

- [`A11_03_02_E01_model_local_kv_causal_use/summary.md`](11_03_cross_position_standard_head_use_boundary/A11_03_02_E01_model_local_kv_causal_use/summary.md): matched shared-aux model-local K/V audit; all guards passed, but \(\bar\Gamma_{info}=0.01675\) and `0/5` seeds reached `0.10`, so the strong behavioral increment failed.
- [`A11_03_02_E02_exact_source_kv_information_audit/summary.md`](11_03_cross_position_standard_head_use_boundary/A11_03_02_E02_exact_source_kv_information_audit/summary.md): exact K/V was perfectly branch-readable under all objectives; the registered MTP-specific CE increment was nonpositive in `4/5` seeds, the formal verdict was insufficient because the shuffle guard failed, and a `5/5` Fisher nuisance-compaction pattern remains secondary.

Only decision-bearing experiments remain on this reading path. Earlier derivations, proxy attempts, and bounded repair variants are under [`archive/`](archive).
