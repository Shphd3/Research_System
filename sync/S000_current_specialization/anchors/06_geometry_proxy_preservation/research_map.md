# A06 Geometry, Proxy, Initialization, And Preservation Research Map

This is a mutable research map for the A06 line. The canonical A06 anchors live
in this folder.

## Parent Question

Can hidden-state geometry support label-free feature/proxy-level gating
initialization, and can that routing survive training?

## Current Judgment

A06 has localized the current bottleneck:

```text
real-DCLM proxy geometry exists;
proxy centers can initialize a strong raw-input linear router;
ordinary DCLM training quickly overwrites that proxy routing.
controlled synthetic-to-realistic bridge shows the earlier discovery failure
was caused by learned absolute positional geometry; without learned absolute
positional embeddings, C0-C3 route-position residual k-means discovery and
same-model preservation both pass. A06_17 shows that C4 all-position clustering
is not a reliable route-initialization proxy because it mixes route and
non-route hidden-state populations. A06_17_02 further shows that successful
center initialization is preserved by positive route margins, not by active
router-center tracking. A06_17_03 quantifies the observed boundary: successful
center-init trajectories consume only part of the initial boundary buffer and
do not switch experts. A06_17_04 shows that margin predicts static boundary
crossing; ordinary stress only lowers the margin, while forced post-hoc row
crossing breaks the original feature-to-expert region. A06_17_05 shows that
exact centers are not required in the controlled bridge: perturbations remain
preserved as long as they stay inside a positive-margin basin.
A06_21 closes the controlled preservation mechanism: pseudo/oracle center
initialization is preserved because current and cluster-aware margins stay
positive with zero sign flips, while random, equal-norm random, and
label-shuffled guards show negative margins and poor matched preservation.
The main negative pressure in the successful controlled bridge is
feature-center drift, but it stays inside the positive margin buffer.
A06_22 completed the real-DCLM common/residual router-trajectory audit. It
reproduces the raw-center proxy-route collapse, but weakens the strong
common-trajectory hypothesis because the common-over-residual update judgment
flips across common projectors. Mean-common is common-dominated, while top
hidden-PC and router-row subspace are residual-dominated.
A06_23 sharpens the controlled preservation mechanism: top-1 preservation is
not guaranteed by any positive step-0 margin. Row-gap scaling shows a finite
safe basin in the controlled no-position bridge: $q\ge 0.05$ preserves, while
$q=0.02$ starts correct but crosses boundaries during training.
A06_24_toy keeps the old vector-only common/rare residual proxy result as
mechanism background rather than decisive model evidence. A06_24_synthetic
then reruns the question in a no-position one-layer Transformer plus one-layer
MoE. It supports the negative method boundary: global all-position common
subtraction can improve some load/common-vs-rare symptoms but does not provide
reliable rare-feature expert separation. Route-position centers and oracle
centers separate features cleanly; after training, target accuracy reaches
1.0 across conditions, so accuracy cannot certify specialization. The strongest
preservation candidate in this synthetic bridge is row-projected routing after
a valid route-relevant initialization, not residual-input common subtraction.
A06_25 returns to the uniform no-position slot bridge and tests whether short
warmup makes all-position hidden states or expert spectral directions usable
for router reinitialization. Warmup improves source quality, but it does not
close the route-position gap: all-position immediate feature NMI rises from
0.774 to 0.876 by warmup 40, while route-position reaches 0.996.
Common-projected expert SVD is the strongest tested spectral candidate
(0.943 immediate NMI and 0.514 margin p05 at warmup 40), but raw SVD and
orthogonalization are not finished methods. The next method question is no
longer "wait a few steps and cluster all positions"; it is whether nested /
long-horizon supervision can make route-relevant hidden states feature-aware
and margin-thick without label-known route selection.
A07_E01 and A07_E02 are retained only as static expert-geometry support for
the `06_2x2_expert_geometry_gate_anchor.md` metric line. The old
`07_high_dim_uniform_expert_geometry_gate_anchor.md` anchor has been removed
to avoid a duplicate value-line reading path.
A06_26 audits the Redesign-style MPI spectral router on the same uniform
no-position slot bridge. MPI improves feature-route NMI over vanilla
(`mpi_c8` 0.832 vs vanilla 0.686), but it remains below route-position centers
(0.979) and has strongly negative lower-tail margin (`mpi_c8` margin p05
-15.258). The all-position initialization extension reaches only `0.830` NMI
with MPI-c8 and worsens margin p05 to `-20.579`, so MPI also does not correct
the mixed all-position source. Therefore MPI is retained as a useful
spectral-router baseline, not as the next mainline solution.
A06_27 tests gradient/Fisher route-state selection on the same uniform
no-position slot bridge. The full run supports a bounded positive result:
embedding-gradient top1 and embedding-gradient direction select a route-relevant
population without feature labels and reach perfect warmup-40 feature routing
(`feature_NMI=1.000`, positive margin p05, matched preserve `1.000`, final NMI
`1.000`). Fisher-only subspace clustering improves NMI but keeps negative
margin, so it is a diagnostic rather than the method. The claim boundary is
important: post-hidden gradients are route-local by the pointwise objective,
and embedding gradients mostly identify the route/slot region; this supports
route-state selection, not semantic feature discovery.
A06_30 tests whether mixed full-LM ideal-center erosion requires background or
non-feature positions. In a no-background full-slot sequence where all 32
positions are the same feature token, oracle all-position / predictive-position
/ last-predictive-position center initialization all preserve all-position
feature NMI `1.000` and final margin p05 about `4.566` after 2000 full-LM
steps. Random routing learns the repeated-token task but remains negative in
margin. This supports background / non-feature positions as a necessary
mechanism candidate in the previous mixed full-LM failure, while not proving
the full causal decomposition.
```

Therefore preservation is not the bottleneck in the controlled no-pos bridge
when the initial margin is above the finite safe threshold. A06_27 adds a
positive synthetic selector: embedding-gradient top1/direction can identify the
route-relevant population and initialize a stable uniform feature router. The
current bottleneck is real-DCLM preservation and transfer beyond the synthetic
pointwise-loss bridge: A06_22 shows the collapse is reproducible
and margin/sign-flip fragility is visible, but generic common-mode dominance is
not a stable mechanism target. A06_23 adds that the real-DCLM audit must judge
whether step-0 proxy margins exceed measured early drift, not merely whether
they are positive. A06_24_synthetic further says that simple common subtraction
is not the next method by itself. A06_25 adds that warmup helps but does not
solve route-relevant state selection. A06_26 adds that Redesign-style MPI
spectral routing improves over vanilla but does not create a stable
positive-margin feature partition. A06_27 changes the next method target from
"find any selector" to "turn embedding-gradient selection into a margin-thick
method and add harder locality guards," with row-projected preservation and MPI
retained as guards/baselines after a valid initialization exists.
RoPE / position encoding, whole-slot composition, semantic feature meaning,
and utility remain separate boundaries.

## Stage Map

```text
Common and real-DCLM failure priors
-> A06_01, A06_02

Synthetic hidden-state geometry
-> A06_03, A06_04, A06_05

Synthetic reachability and label-free discovery
-> A06_06, A06_07, A06_08, A06_09

Real-DCLM proxy and router bridge
-> A06_10, A06_11

Real-DCLM training preservation and failure localization
-> A06_12, A06_13, A06_22

Mechanism bridge back to controlled settings
-> A06_16, A06_17, A06_17_02, A06_17_03, A06_17_04, A06_17_05, A06_18, A06_19, A06_20, A06_21, A06_23, A06_24_toy, A06_24_synthetic, A06_25, A06_26, A06_27

Static expert-geometry support
-> A06_2x2, A07_E01, A07_E02

Utility binding
-> A06_14, A06_15 parked until preservation succeeds

Line closure
-> [`closure/06_geometry_proxy_preservation_closure_report.md`](closure/06_geometry_proxy_preservation_closure_report.md)
```

## Anchor Index

| Anchor | Stage | Main update | Decision status |
|---|---|---|---|
| [`06_01_common_filtered_expert_spectrum_router_initialization_anchor.md`](06_01_common_filtered_expert_spectrum_router_initialization_anchor.md) | Real common-filtered init | Expert-spectrum/common-filtered init is not enough. | Negative / informative |
| [`06_02_early_training_common_logit_amplification_anchor.md`](06_02_early_training_common_logit_amplification_anchor.md) | Real early dynamics | Early common/load amplification is a real DCLM risk. | Mechanism prior |
| [`06_03_high_dimensional_gaussian_gate_norm_variation_anchor.md`](06_03_high_dimensional_gaussian_gate_norm_variation_anchor.md) | Gate-only baseline | Row-norm variation can fake imbalance; equal-norm guard is needed. | Guard |
| [`06_04_real_hidden_state_gate_geometry_decomposition_anchor.md`](06_04_real_hidden_state_gate_geometry_decomposition_anchor.md) | Synthetic hidden geometry | Common component can dominate load. | Mechanism evidence |
| [`06_05_common_centered_residual_geometry_diagnostic_anchor.md`](06_05_common_centered_residual_geometry_diagnostic_anchor.md) | Residual geometry | Feature-like residual structure remains after common centering. | Supports discovery |
| [`06_06_feature_level_initialization_positive_control_anchor.md`](06_06_feature_level_initialization_positive_control_anchor.md) | Oracle reachability | Feature partition is reachable with oracle information. | Positive control |
| [`06_07_label_free_common_residual_control_router_anchor.md`](06_07_label_free_common_residual_control_router_anchor.md) | Simple label-free controls | Centering/projection/whitening mostly fix load, not feature NMI. | Weakened |
| [`06_08_label_free_feature_discovery_initialization_anchor.md`](06_08_label_free_feature_discovery_initialization_anchor.md) | Synthetic label-free discovery | Route-position residual clustering can recover synthetic feature partition. | Supported with synthetic boundary |
| [`06_09_training_basin_preservation_anchor.md`](06_09_training_basin_preservation_anchor.md) | Synthetic preservation | Synthetic pseudo init can be preserved under the simple training setup. | Supported with synthetic boundary |
| [`06_10_real_dclm_proxy_feature_operationalization_anchor.md`](06_10_real_dclm_proxy_feature_operationalization_anchor.md) | Real proxy definition | Real DCLM hidden states contain stable proxy clusters. | Supported with boundary |
| [`06_11_real_dclm_proxy_center_router_initialization_anchor.md`](06_11_real_dclm_proxy_center_router_initialization_anchor.md) | Real router bridge | Raw-center equal-norm gives strong raw-input proxy routing. | Supported with boundary |
| [`06_12_real_dclm_proxy_init_training_preservation_anchor.md`](06_12_real_dclm_proxy_init_training_preservation_anchor.md) | Real training preservation | Ordinary DCLM training does not preserve proxy routing. | Weakened |
| [`06_13_real_dclm_proxy_init_failure_decomposition_anchor.md`](06_13_real_dclm_proxy_init_failure_decomposition_anchor.md) | Failure localization | First failed contract is training feedback override. | Supported |
| [`06_14_real_dclm_proxy_expert_utility_binding_anchor.md`](06_14_real_dclm_proxy_expert_utility_binding_anchor.md) | Utility binding | Cannot test until routing is preserved. | Parked |
| [`06_15_real_dclm_utility_aware_gating_initialization_anchor.md`](06_15_real_dclm_utility_aware_gating_initialization_anchor.md) | Utility-aware init | Depends on A06_14 utility table. | Parked |
| [`06_16_synthetic_to_realistic_proxy_bridge_anchor.md`](06_16_synthetic_to_realistic_proxy_bridge_anchor.md) | Mechanism bridge | Learned absolute positional geometry caused the old C0 discovery failure; same-model no-pos C0-C3 discovery and preservation pass, while C4 all-position mostly passes but remains imperfect. | Supported with corrected boundary |
| [`06_17_all_position_route_relevant_feature_discovery_anchor.md`](06_17_all_position_route_relevant_feature_discovery_anchor.md) | All-position robustness | Route-only and slot offset 3 recover feature perfectly; all-position fails by whole-feature merges, so the clustering population is wrong. | Supported |
| [`06_17_02_router_center_tracking_preservation_anchor.md`](06_17_02_router_center_tracking_preservation_anchor.md) | Center preservation mechanism | Correct center initialization preserves by positive raw route margins, not by active router-center tracking. | Supported with controlled boundary |
| [`06_17_03_feature_drift_margin_boundary_anchor.md`](06_17_03_feature_drift_margin_boundary_anchor.md) | Drift margin boundary | Observed center drift consumes only part of the initial boundary buffer; center-init has zero switches and positive dynamic margins. | Supported with observed-trajectory boundary |
| [`06_17_04_margin_crossing_causal_stress_anchor.md`](06_17_04_margin_crossing_causal_stress_anchor.md) | Margin crossing stress | Static crossing validates margin as a geometric ruler; forced post-hoc row crossing breaks the original feature-to-expert region. | Supported for controlled mechanism |
| [`06_17_05_margin_basin_robust_initialization_anchor.md`](06_17_05_margin_basin_robust_initialization_anchor.md) | Margin basin robustness | Exact pseudo-center rows are not required; perturbations through `rho=0.7` preserve if margin stays positive, while random rows fail. | Supported for controlled mechanism |
| [`06_18_label_free_route_relevant_state_selection_anchor.md`](06_18_label_free_route_relevant_state_selection_anchor.md) | Route-relevant state selection | Split-stability selectors do not beat all-position; route-only remains perfect, so the selector operationalization failed. | Weakened / informative |
| [`06_19_minimal_prior_margin_aware_center_search_anchor.md`](06_19_minimal_prior_margin_aware_center_search_anchor.md) | Minimal-prior center search | Tested M1/M2 margin-aware selectors do not reliably beat raw all-position clustering; route-only remains the positive control. | Weakened / informative |
| [`06_20_route_logit_common_estimator_random_init_feature_recovery_anchor.md`](06_20_route_logit_common_estimator_random_init_feature_recovery_anchor.md) | Routing-aware common estimator | Route-logit common subtraction changes load but does not recover feature residual geometry; route-only remains high, so feature geometry is present but this estimator is wrong. | Weakened / informative |
| [`06_21_margin_budget_preservation_audit_anchor.md`](06_21_margin_budget_preservation_audit_anchor.md) | Margin-budget preservation audit | Controlled center-init preservation is explained by positive current and cluster-aware margins with zero sign flips; random/shuffled guards have negative margins and poor matched preservation. | Supported for controlled mechanism |
| [`06_22_router_common_residual_trajectory_anchor.md`](06_22_router_common_residual_trajectory_anchor.md) | Real-DCLM router trajectory audit | Full run reproduces raw-center collapse but weakens strong common-trajectory H1: mean-common is common-dominated, while top hidden-PC and router-row projectors are residual-dominated. | Weakened / informative |
| [`06_23_top1_lockin_margin_threshold_anchor.md`](06_23_top1_lockin_margin_threshold_anchor.md) | Margin threshold stress | Row-gap scaling shows controlled top-1 preservation has a finite safe margin: $q\ge0.05$ preserves, while $q=0.02$ starts correct but loses matched identity through sign flips. | Supported with threshold boundary |
| [`06_24_toy_common_rare_residual_proxy_anchor_cn.md`](06_24_toy_common_rare_residual_proxy_anchor_cn.md) | Vector toy common/rare proxy | Old A06_26 vector-only result is retained as mechanism background and renumbered to A06_24_toy; it is not decisive for the Transformer+MoE setting. | Supporting / toy boundary |
| [`06_24_synthetic_common_rare_transformer_moe_anchor.md`](06_24_synthetic_common_rare_transformer_moe_anchor.md), [`06_24_synthetic_common_rare_transformer_moe_anchor_cn.md`](06_24_synthetic_common_rare_transformer_moe_anchor_cn.md) | No-position Transformer+MoE common/rare bridge | Full run shows all-position common subtraction is not reliable rare-feature expert separation; route-position/oracle centers and row-projected preservation are stronger candidates, with slot-position leakage excluded. | Supported with synthetic boundary |
| [`06_25_warmup_spectral_router_reinit_anchor.md`](06_25_warmup_spectral_router_reinit_anchor.md), [`06_25_warmup_spectral_router_reinit_anchor_cn.md`](06_25_warmup_spectral_router_reinit_anchor_cn.md) | Warmup spectral/router reinit source audit | Full local two-GPU run shows warmup improves all-position and expert-SVD feature awareness, but route-position centers remain the strongest source; common-projected SVD is a candidate diagnostic, while simple orthogonalization is not the fix. | Partially supported / next nested-state anchor |
| [`06_26_mpi_uniform_feature_router_anchor.md`](06_26_mpi_uniform_feature_router_anchor.md) | MPI spectral router baseline | Full local two-GPU run shows Redesign-style MPI improves feature NMI over vanilla (`mpi_c8` 0.832 vs 0.686) but stays below route-centered control (0.979) and has negative margin p05 (-15.258); all-position + MPI-c8 also fails to correct the source (NMI 0.830, margin p05 -20.579). | Partially supported / baseline only |
| [`06_27_gradient_fisher_route_state_selector_anchor.md`](06_27_gradient_fisher_route_state_selector_anchor.md) | Gradient/Fisher route-state selector | Full local two-GPU run shows embedding-gradient top1/direction can select route-relevant states without feature labels and reach warmup-40 feature NMI `1.000` with positive margin and preserve, while Fisher-only subspace clustering keeps negative margin. | Supported with synthetic route-state boundary |
| [`06_30_noise_free_full_slot_preservation_anchor.md`](06_30_noise_free_full_slot_preservation_anchor.md) | No-background full-slot preservation audit | Full local H100 run shows that when all 32 positions are feature-bearing and background tokens are removed, oracle all-position / predictive-position / last-predictive-position center initialization preserves all-position feature NMI `1.000` and final margin p05 about `4.566` after 2000 full-LM steps; random learns the task but stays negative-margin. | Supported as background/noise necessity check |

## Current Next Decision

After A06_22, A06_23, A06_24_synthetic, A06_25, A06_26, and A06_27, the selected
mainline direction is to stop treating common subtraction, all-position warmup
clustering, raw expert SVD, MPI spectral routing, or Fisher-only metric changes
as standalone solutions. A06_27 promotes embedding-gradient selection as the
next method candidate:

```text
method decision:
can an embedding-gradient selected route-state pool be turned into a
margin-thick router initialization / refresh method, and does it survive harder
objective-locality guards before common/rare transfer?
```

Primary next metric on the uniform bridge: feature route `NMI` with margin p05
as the preservation guard. Decision guards: matched preserve fraction,
current/cluster-aware margin, sign-flip rate, max load, slot-position `NMI`,
selected route/slot/target fraction, and task loss. If the next bridge returns
to common/rare imbalance, restore the joint rare-feature `NMI` times
common-vs-rare `NMI` score.

A06_30 updates the immediate next mechanism decision: before designing another
gate, run a graded background-ratio margin-budget audit. The question is no
longer whether no-background full-LM can preserve ideal routing; it can. The
question is which added background / non-feature signal term first consumes the
positive margin.

Related side mechanism: A06_20 tested a routing-aware common estimator under
random-init training. It failed as a feature-recovery estimator: selected
router-contrast directions changed load but did not improve held-out
route-position feature NMI or margin. Therefore the next main path should not
be route-logit common subtraction unless the estimator is redesigned to block
load-only router-contrast wins.

Parked until preservation:

- A06_14 utility binding;
- A06_15 utility-aware initialization.

## Maintenance Notes

Update this map when an A06 result changes:

- the active stage contract;
- the current bottleneck;
- whether utility binding is still parked;
- the next concrete preservation decision.
