# Common Anchor Sync - 2026-07-01

## Scope

This folder is a dated reading package for anchors related to common-mode,
common-logit, common/residual geometry, and common/rare interference in the
expert-specialization line.

It is a synchronized reading surface, not a new source of truth. The canonical
anchors remain under:

```text
Projects/from-attention-to-search/main/problem_anchors/
```

## Reading Order

1. `anchors/01_common_operator_mechanism/`
   - Defines the common-operator mechanism line and its current closure.
   - Read first when the question is what "common" means mechanistically.

2. `anchors/05_failure_mechanism/`
   - Shows how common offset and common logits can produce routing collapse or
     misleading early specialization signals.
   - Read after the common-operator overview when diagnosing failure.

3. `anchors/06_geometry_proxy_preservation/`
   - Connects common/residual geometry to proxy discovery, initialization, and
     preservation.
   - The newest relevant diagnostic is
     `06_22_router_common_residual_trajectory_anchor.md`.

4. `anchors/07_features_overlap/`
   - Uses common/rare conflict to connect preservation to functional
     interference and utility questions.

5. `anchors/08_real_data_preserved_specialization/`
   - Keeps the real-data method-side common-direction split candidate.

6. `anchors/09_common_rare_spectral_discrimination/`
   - Stores the spectral common-band / rare-discrimination modeling line.

## Included Source Files

### 01 Common Operator Mechanism

- `README.md`
- `README_cn.md`
- `01_01_common_operator_identifiability_anchor.md`
- `01_03_gradient_common_vs_activation_common_anchor.md`
- `01_03_gradient_common_vs_activation_common_anchor_cn.md`
- `01_04_feedback_common_preservation_bridge_anchor.md`
- `closure/01_common_operator_mechanism_closure_report.md`
- `closure/01_common_operator_mechanism_closure_report_cn.md`

### 05 Failure Mechanism

- `05_03_uniform_collapse_common_offset_anchor.md`
- `05_04_02_dotproduct_common_logit_causality_anchor.md`
- `05_04_03_real_text_common_logit_initialization_anchor.md`

### 06 Geometry, Proxy, Initialization, And Preservation

- `06_01_common_filtered_expert_spectrum_router_initialization_anchor.md`
- `06_02_early_training_common_logit_amplification_anchor.md`
- `06_05_common_centered_residual_geometry_diagnostic_anchor.md`
- `06_07_label_free_common_residual_control_router_anchor.md`
- `06_20_route_logit_common_estimator_random_init_feature_recovery_anchor.md`
- `06_22_router_common_residual_trajectory_anchor.md`
- `06_22_router_common_residual_trajectory_anchor_cn.md`

### 07 Common/Rare Interference And Value

- `07_01_common_rare_conflict_metric_audit_anchor.md`
- `07_02_common_controlled_rare_interference_anchor.md`
- `07_04_common_rare_gradient_conflict_splitting_anchor.md`
- `07_05_common_update_interference_diagnostic_anchor.md`
- `07_06_projected_common_rare_conflict_splitting_anchor.md`

### 08 Real-Data Preserved Specialization

- `08_03_common_direction_split_reservoir_anchor.md`

### 09 Common/Rare Spectral Discrimination

- `09_01_common_band_rare_discrimination_anchor.md`
- `09_01_common_band_rare_discrimination_anchor_cn.md`

## Claim Boundary

This package organizes existing anchors for reading. It does not introduce a
new claim, update the project graph, or replace project-local anchors,
protocols, summaries, or detailed experiment records.
