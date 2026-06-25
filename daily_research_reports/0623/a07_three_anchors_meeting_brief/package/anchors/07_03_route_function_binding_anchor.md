---
anchor_id: A07_03_route_function_binding
parent_node: rq.expert_specialization
status: supported_controlled_synthetic
created: 2026-06-23
canonical_language: en
depends_on: A07_02_common_controlled_rare_interference
source_draft: 00_handwrite_anchor.md
---

# A07_03 Route-Function Binding Anchor

## 0. Thinking Card

父问题：rare loss 改善是否真的来自 expert specialization。
当前子问题：A07_02 通过后，routed experts 是否对对应 conflict group 有因果效用。
当前判断：controlled D07 上支持 route-function binding。
关键证据：selected-best `1.0000` vs chance `0.2500`；utility advantage 约 `0.950`；modal ablation delta `0.6800`。
最危险边界：expert id 跨 seed 置换，必须读 modal-aligned 表；不是真实语义专家证据。
下一步决策：决定先做 neural D07 training，还是迁移到真实 checkpoint 诊断。

Question:
After A07_02 passes, do routed experts have conflict-group-specific causal utility under forced-routing and fixed-routing ablation?

Physical prior:
Expert specialization requires assignment-function binding: routed expert use should beat alternative / uniform expert use, and fixed-route ablation should selectively hurt the corresponding group.

Core model:
For group $g$, use modal expert $a_g$ only if route concentration exceeds threshold; otherwise use route-distribution-weighted utility $CE_{g,\mathrm{route}}$.

Model term being tested:
Conflict-conditioned expert function, conditional on A07_02 passing.

Primary metric:
Route-conditioned utility advantage: modal utility gap if valid, otherwise route-weighted utility gap.

Falsifier:
Forced-routing utility is flat, selected-best rate is near chance, route-weighted utility does not beat uniform / alternatives, fixed-routing ablation is not group-specific, or forced routing changes non-expert paths.

Can claim:
A07_02's rare-loss improvement is supported by conflict-conditioned expert function in controlled synthetic D07.

Cannot claim:
Natural-language semantic experts, robust real-DCLM specialization, deployable routing, or one-feature-one-expert structure.

Next decision:
Decide whether to port the diagnostic to neural D07 training or a real trained checkpoint.

## 1. Problem Definition

Parent problem: feature-level expert specialization requires useful routing and expert-side function.

Sharper subproblem: test whether A07_02's rare-loss gain has route-function binding.

Decision question: do routed experts have conflict-group-specific causal utility?

Not in scope: D07 validation, common-control construction, real text, semantic discovery, or architecture deployment.

## 2. Physical Priors

P1: Assignment and utility can be unbound.
Meaning: route structure can exist while experts are interchangeable.
Could be wrong if: routed expert use consistently lowers group loss.

P2: A single assigned expert is valid only under route concentration.
Meaning: diffuse routing should be evaluated by route-distribution-weighted utility.
Could be wrong if: modal and route-weighted reads agree across groups.

P3: Fixed-routing ablation is needed for expert function.
Meaning: if ablation allows rerouting, damage may reflect redistribution rather than the original expert's function.
Could be wrong if: fixed-route and rerouting-enabled ablations give the same group-specific conclusion.

## 3. Falsifiable Hypotheses

H1: Routed expert use has group-specific utility.
Supported if: modal or route-weighted utility beats alternatives / uniform use and selected-best rate exceeds chance $1/E$.
Weakened if: utility is flat or near chance.

H2: Expert contribution is selective.
Supported if: fixed-routing ablation hurts associated groups more than unrelated groups.
Weakened if: fixed-routing ablation damages all groups equally.

H3: Utility is not only final co-adaptation.
Supported if: early and final utility reads agree, or utility is visible before final co-adaptation.
Weakened if: utility appears only at final checkpoint.

## 4. Mathematical Model

Objects: conflict group $g$, expert count $E$, route distribution $P(e\mid g)$, route threshold $\tau_{\mathrm{route}}$, forced loss $CE_{g,e}$.

Modal expert:
$$
a_g=\arg\max_eP(e\mid g)\quad\text{only if}\quad \max_eP(e\mid g)\ge\tau_{\mathrm{route}}
$$

Route-weighted utility:
$$
CE_{g,\mathrm{route}}=\sum_eP(e\mid g)CE_{g,e},\qquad
CE_{g,\mathrm{uniform}}=\frac{1}{E}\sum_eCE_{g,e}
$$

Mechanism relation: route-function binding requires routed/modal expert use to beat uniform or alternative expert use and fixed-route ablation to be group-specific.

Observable metrics: modal utility gap, route-weighted utility gap, selected-best rate, chance baseline $1/E$, utility entropy, fixed-routing ablation selectivity, early/final stability.

Falsifier: no utility advantage, selected-best near chance, flat utility matrix, nonselective fixed-routing ablation, or invalid forced routing.

## 5. Computational Realization

Input objects: A07_02-supported checkpoints, route assignments, expert IDs, conflict group IDs, and evaluation labels.

Computed variables: $P(e\mid g)$, forced-routing utility matrix, modal or route-weighted utility gap, selected-best rate, fixed-routing ablation matrix, early/final comparison.

Algorithm stages: choose A07_02-passing checkpoints; compute route concentration; run forced-routing preserving non-expert paths; run fixed-routing ablation; compare early and final reads.

Stage-local evidence: route distribution table, utility heatmap, selected-best table, fixed-routing ablation heatmap, early/final table.

Expected artifacts: `protocol.md`, `summary.md`, `detailed.md`, `tables/route_distribution_by_group.csv`, `tables/forced_utility_matrix.csv`, `tables/fixed_routing_ablation_selectivity.csv`.

## 6. Minimal Falsification Tests

Test: forced-routing utility binding.
Question: does routed expert use lower conflict-group loss?
Intervention / comparison: force each group through each expert while preserving non-expert paths.
Primary metric: modal utility gap when concentration passes threshold; otherwise route-weighted utility gap.
Supports: routed/modal use beats alternatives and selected-best exceeds chance.
Weakens: utility is flat or route-weighted use does not beat uniform.
Insufficient evidence: forced routing changes other computation paths or groups are too small.

Test: fixed-routing ablation.
Question: does the expert contribute selectively under fixed routes?
Intervention / comparison: fixed-routing ablation versus normal evaluation.
Guard metric: group-specific fixed-routing ablation damage.
Supports: damage is group-specific.
Weakens: all groups are damaged similarly.
Insufficient evidence: routing changes during primary ablation.

Test: co-adaptation guard.
Question: is utility visible before final co-adaptation?
Intervention / comparison: initialization / early / final utility reads.
Guard metric: early/final utility stability.
Supports: utility appears early or remains stable.
Weakens: utility appears only at final checkpoint.
Insufficient evidence: early checkpoints missing.

## 7. Current Evidence

Observation: A07 shared full run completed on 2026-06-23 with 8 seeds.
Interpretation: route-function binding is supported by modal-aligned metrics: selected-best rate is `1.0000` against chance `0.2500`, and route-conditioned utility advantage is `0.9498-0.9502` across groups.
Boundary: raw expert IDs permute across seeds, so raw expert-id averaged forced matrices are auxiliary only.
Evidence links: `../../experiments/A07/A07_03_route_function_binding/summary.md`, `../../experiments/A07/A07_03_route_function_binding/detailed.md`.

Observation: Fixed-route ablation is selective under modal alignment.
Interpretation: modal ablation delta is `0.6800` for every group, while nonmodal ablation delta is `0.0000`; early utility advantage is already `0.7408-0.7411`.
Boundary: this is controlled synthetic causal-utility evidence, not real-language semantic expert evidence.
Evidence links: `../../experiments/A07/A07_03_route_function_binding/tables/modal_ablation_selectivity.csv`, `../../experiments/A07/A07_03_route_function_binding/tables/early_final_utility.csv`.

Observation: A06_14 separates assignment from utility.
Interpretation: A07_03 is required before claiming causal expert specialization.
Boundary: A06_14 is real-DCLM parked evidence, not D07 evidence.
Evidence links: `../06_geometry_proxy_preservation/06_14_real_dclm_proxy_expert_utility_binding_anchor.md`.

Observation: A05/A06 show load and route structure can mislead.
Interpretation: utility and fixed-routing ablation are needed after A07_02.
Boundary: they do not answer D07 route-function binding.
Evidence links: `../05_failure_mechanism/05_03_uniform_collapse_common_offset_anchor.md`, `../06_geometry_proxy_preservation/06_07_label_free_common_residual_control_router_anchor.md`.

## 8. Claim Boundary And Next Decision

Can claim:
A07_02's rare-loss gain has controlled D07 route-function binding evidence.

Cannot claim:
Natural-language semantic experts, robust real-DCLM specialization, deployable routing, or one-feature-one-expert structure.

Next decision:
Choose the next surface: neural D07 training first, or direct real-checkpoint diagnostic.
