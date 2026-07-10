# Problem Anchors

This folder stores the project-local source-of-truth anchors for
`from-attention-to-search`.

Canonical anchors are grouped by research line:

```text
Projects/from-attention-to-search/main/problem_anchors/00_foundation_definition/
Projects/from-attention-to-search/main/problem_anchors/01_common_operator_mechanism/
Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/
Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/
Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/
Projects/from-attention-to-search/main/problem_anchors/08_real_data_preserved_specialization/
Projects/from-attention-to-search/main/problem_anchors/09_common_rare_spectral_discrimination/
Projects/from-attention-to-search/main/problem_anchors/10_optimizer_learning_rate_mechanism/
Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/
```

Do not create a generic nested `anchors/` subfolder inside this project-local
source tree. Each folder above is a research-line folder. Root `sync/S000_*`
may copy these anchors into its own `anchors/` mirror when explicitly synced,
but the project-local files remain the source of truth.

Do not add placeholder `closure/` folders or per-folder closure README files.
Create `closure/` only for a line explicitly selected for current-state
synthesis. The closure report itself is the reading entry and should link to,
not duplicate, anchors and experiment records.

Current classification maps:

```text
00_foundation_definition/README.md
05_failure_mechanism/research_map.md
06_geometry_proxy_preservation/research_map.md
09_common_rare_spectral_discrimination/README.md
```

## Active Research Shape

Current mainline:

```text
definition / failure mechanism
-> common and hidden-geometry diagnosis
-> proxy discovery and router initialization
-> training preservation
-> common/rare interference and expert utility only after preservation succeeds
```

Current strongest judgment:

```text
Real-DCLM proxy geometry exists and is linearly routable at step 0, but
ordinary DCLM training does not preserve proxy routing. Controlled D07 supports
the value chain from metric surface to rare-interference reduction to
route-function binding, but neural A07_04 is still insufficient evidence. The
next active decision is preservation / anti-feedback, not a broader utility
claim.
```

## Anchor Groups

| Group | Anchors | Role | Current status |
|---|---|---|---|
| 00 foundation / definition | `00_foundation_definition/01_*` | Defines operational feature-level specialization and separates route consistency, non-collapse, feature identity, and expert utility. | Parent reading frame. It is not a method claim. |
| 01 common-operator mechanism line | `01_common_operator_mechanism/README.md`, `01_common_operator_mechanism/README_cn.md`, `01_common_operator_mechanism/closure/01_common_operator_mechanism_closure_report.md` | Plan and synthesize the mechanism-first line for defining, identifying, and validating a common operator before method construction. | Stage 1 supports criterion-dependent common (`criterion_winner_diversity=4`); Stage 2 supports gradient common over activation common (`n_passed_mismatch_regimes=4/4`); Stage 3 controlled bridge supports feedback replay/removal (`n_passed_main_feedback_regimes=2/2`). The bounded real-DCLM gate-logit bridge reproduces collapse but rejects simple low-rank logit common as the main explanation (`pass=false`). |
| 05 failure-mechanism line | `05_failure_mechanism/02_*`, `05_failure_mechanism/05_01_*` to `05_failure_mechanism/05_04_03_*` | Diagnose why ordinary top-1 fails: early top-1 lock-in, inhibition limits, feature-axis ambiguity, common offset, and common-logit feedback. | Mechanism evidence. It supplies the physical priors used by 06. |
| 06 geometry/proxy/init/preservation line | `06_geometry_proxy_preservation/06_01_*` to `06_geometry_proxy_preservation/06_27_*` | Build the staged pipeline: common control, residual geometry, label-free proxy, real-DCLM proxy, router bridge, training preservation, route-relevant state selection, margin-aware center search, routing-aware common estimation, router common/residual trajectory audit, no-position common/rare Transformer+MoE bridge, warmup spectral/router source audit, MPI baseline, and gradient/Fisher route-state selector. | Active mainline. A06_27 supports embedding-gradient route-state selection on the synthetic uniform bridge; bottleneck is now turning that selector into a margin-thick method and testing harder locality / common-rare transfer guards. |
| 06 sandbox / side checks | `06_geometry_proxy_preservation/06_2x2_*`, `06_geometry_proxy_preservation/06_08_slot_length_*` | Small geometry or robustness checks that support the 06 line but are not the current main decision. | Supporting evidence. |
| 07 interference / value line | `07_features_overlap/03_*`, `07_features_overlap/07.md`, `07_features_overlap/07_01_*` to `07_features_overlap/07_06_*` | Test whether a non-collapsed partition reduces common/rare feature interference or has expert utility. It also keeps the earlier hierarchy / route-utility-binding branch as historical support. | Controlled D07 and nested value diagnostics are useful; real utility remains gated by preservation. |
| 08 real-data preserved-specialization line | `08_real_data_preserved_specialization/08_*` | Turns preserved routing into a real-DCLM specialization target: stable singular directions, gate-forward anchors, preservation, and utility closure. | Candidate downstream line. It should not outrun the A06 preservation evidence. |
| 09 common/rare spectral-discrimination line | `09_common_rare_spectral_discrimination/04_*`, `09_common_rare_spectral_discrimination/09_*` | Tests frequency / high-gain common-band explanations for rare discrimination failure. | Mechanism side line. It can inform A06/A07 but does not by itself prove a routing method. |
| 10 optimizer learning-rate mechanism line | `10_optimizer_learning_rate_mechanism/10_*` | Seminar-driven optimizer root-cause line: test whether common / high-gain gradient directions constrain SGD-style critical learning rate before comparing Adam, Nesterov, or other optimizers. | Support line. It does not update the MoE preservation claim unless later bridged back through routing margin evidence. |
| 11 long-horizon MTP objective line | `11_long_horizon_mtp_objective/11_*`; story: `../stories/11_long_horizon_mtp_objective/story_cn.md` | Tests the advisor-requested objective-level link between long-horizon branch information and multi-token prediction. | Evidence-updated support line. Current A11 evidence supports a controlled representation guarantee and a mechanism boundary: K matters when it covers informative horizons with aligned centered readout directions; all-position `Q` can be probe-readable without native direct readout, so direct evidence needs native H3 and `M_Z_ref`. This line does not yet prove MoE routing preservation or expert utility. |

## Legacy Root Anchor Placement

| Early anchor | New location | Relation to later anchors | Experiment decision |
|---|---|---|---|
| `01_slot_context_dominance_router_specialization_anchor.md` | `00_foundation_definition/` | Parent definition and diagnostic frame for feature identity, non-collapse, and utility. Later 05/06/07 inherit its boundary. | Keep `A01_*` evidence as historical definition/failure evidence. |
| `02_ntp_style_top1_router_lockin_anchor.md` | `05_failure_mechanism/` | Mechanism precursor for 05 common/lock-in and 06 preservation failure. | Keep `A02_top1_router_lockin_2x2/`. |
| `03_hierarchical_route_utility_binding_anchor.md` | `07_features_overlap/` | Synthetic hierarchy / route-utility binding branch. It overlaps with A06_14 but stays parked until preservation succeeds. | Keep `A03_hierarchical_route_utility_binding/`. |
| `04_ntp_zipf_feature_factorization_anchor.md` | `09_common_rare_spectral_discrimination/` | Frequency/write-in attribution branch. It may inform common/rare spectral discrimination, but is not a duplicate of the proxy line. | Keep `experiments/archive/A04_parked_frequency/`. |

`07_high_dim_uniform_expert_geometry_gate_anchor.md` was removed as a
duplicate historical bridge. Its A07_E01/A07_E02 static-geometry experiment
records now point to `06_geometry_proxy_preservation/06_2x2_expert_geometry_gate_anchor.md`
as supporting geometry evidence.

## Experiment Folder Rule

Experiment folders remain one evidence surface per anchor clause or run role:

```text
../experiments/A<anchor_id>/<experiment_id>/
```

Do not merge separate experiment folders merely because they share an anchor
prefix. Merge only when two folders contain the same protocol/result record.
No safe duplicate experiment folder was found in the 01-04 vs 05/06 audit.

## Next Decision

Design the next preservation / anti-feedback protocol after A06_22:

```text
Which common operator, if any, is physically stable enough to explain
real-DCLM raw-center proxy-route collapse through router-update geometry?
```

Primary metric: common-over-residual router update dominance ratio
`\Lambda_{\mathrm{upd}}` at step 5/10 under the newly specified operator.

Required guards: `proxy_route_NMI`, LM loss, load concentration, active
experts, common margin, residual margin, and sign-flip rate.
