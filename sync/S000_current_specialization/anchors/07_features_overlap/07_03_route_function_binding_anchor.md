---
anchor_id: A07_03_route_function_binding
current_short_name: nested_route_function_binding
parent_node: rq.expert_specialization
status: diagnostic_positive_control_parked
created: 2026-06-23
retargeted: 2026-06-28
canonical_language: en
depends_on: A07_02_common_controlled_rare_interference
---

# A07_03 Nested Route-Function Binding Anchor


## 1. Problem Definition

**Parent problem:** A07_02 tests whether common-subspace control can reduce nested tail interference.

**Sharper subproblem:** Test whether MoE routing, if used, assigns child-specific function to experts rather than only sorting examples.

**Decision question:** Conditional on route preservation, do routed experts have nested-level-specific causal utility?

**Not in scope:** discovering the best router, proving real semantic experts, using load balance as utility, or bypassing the A06 preservation bottleneck.

## 2. Physical Priors

**P1: Assignment and function can be unbound.**  
Meaning: a route can align with a level while experts remain interchangeable.  
Could be wrong if: routed experts consistently lower their level's loss.

**P2: Causal utility requires fixed-route intervention.**  
Meaning: if routes are allowed to change during ablation, damage may reflect rerouting rather than expert function.  
Could be wrong if: fixed-route and rerouting-enabled ablations agree.

**P3: Utility should be child-specific.**  
Meaning: an expert useful for $ABC$ or $ABCD$ should hurt that level more than unrelated levels when ablated.  
Could be wrong if: ablation damages all levels uniformly.

## 3. Falsifiable Hypotheses

**H1: Routed experts improve their nested levels.**  
Supported if: route-conditioned forced use beats uniform or non-routed expert use.  
Weakened if: the forced-utility matrix is flat.

**H2: Expert function is selective.**  
Supported if: fixed-route ablation selectively damages the routed child level.  
Weakened if: all levels are damaged equally.

**H3: Route-function binding is not just load balance.**  
Supported if: load-matched controls do not show the same utility/selectivity.  
Weakened if: balanced random routing gives the same result.

## 4. Mathematical Model

**Objects:** nested level $\ell$, expert $e$, route distribution $P(e\mid \ell)$, forced loss $CE_{\ell,e}$, fixed-route ablation loss $CE_{\ell}^{-e}$.

**Core decomposition:**
$$
CE_{\ell,\mathrm{route}}=\sum_e P(e\mid \ell)CE_{\ell,e},
$$
$$
CE_{\ell,\mathrm{uniform}}=\frac{1}{E}\sum_e CE_{\ell,e}.
$$

**Mechanism relation:** useful routing requires routed expert use to beat uniform use and fixed-route ablation to selectively damage the associated nested level.

**Observable metrics:**
$$
U_\ell=CE_{\ell,\mathrm{uniform}}-CE_{\ell,\mathrm{route}},
$$
$$
A_\ell=CE_{\ell}^{-\mathrm{routed}}-\frac{1}{E-1}\sum_{e\ne \mathrm{routed}}CE_{\ell}^{-e}.
$$

**Falsifier:** no utility advantage, no selective ablation damage, or effect explained by load-matched random routes.

## 5. Computational Realization

**Input objects:** A06-preserved or A07_02-derived MoE checkpoints, nested level labels for audit, fixed routes, forced-route evaluation hooks.

**Computed variables:** route concentration, forced-utility matrix, route-conditioned utility $U_\ell$, fixed-route ablation selectivity $A_\ell$, load-matched control metrics.

**Algorithm stages:** choose a checkpoint with preserved routes; compute $P(e\mid \ell)$; run forced-route utility; run fixed-route ablation; compare against load-matched controls.

**Stage-local evidence:** route distribution table, forced-utility heatmap, ablation-selectivity table, load guard.

**Expected artifacts:** `protocol.md`, `summary.md`, `detailed.md`, `tables/a07_03_aggregate.csv`, `figures/a07_03_route_binding.png`.

## 6. Minimal Falsification Tests

**Test: nested route-function binding.**  
Question: does routed expert use causally help the nested level it receives?  
Intervention / comparison: forced routing and fixed-route ablation against uniform and load-matched controls.  
Primary metric: fixed-route ablation selectivity $A_\ell$.  
Pass / fail / insufficient: pass if routed expert ablation selectively damages its nested level and forced routed use beats uniform; fail if utility is flat or nonselective; insufficient if route preservation failed.  
Why it decides: it separates route-label alignment from expert-side function.  
Failure means: MoE routing may be structured but not functionally specialized for nested interference.

## 7. Current Evidence

**Observation:** A07_03 nested full run `a07_nested_full_20260628_2` completed with 8 seeds. Oracle nested route had ablation selectivity `0.5699`, route utility `0.1746`, selected-best rate `0.7500`, and route concentration `1.0000`; random load-matched route had ablation selectivity `0.0107`.
**Interpretation:** the forced-routing / fixed-route ablation diagnostic can detect nested route-function binding on a controlled positive-control surface.
**Boundary:** oracle routing is hand-coded; this does not prove learned or preserved top-1 MoE utility.
**Evidence links:** `../../experiments/A07/A07_03_nested_route_function_binding/summary.md`, `../../experiments/A07/A07_03_nested_route_function_binding/detailed.md`.

**Observation:** Prior A07_03 showed route-function binding on controlled D07 after common-control.  
**Interpretation:** the old and new diagnostics agree that forced routing plus fixed-route ablation is a useful utility reader.  
**Boundary:** neither result proves real-DCLM semantic expert utility.  
**Evidence links:** `../../experiments/A07/A07_03_route_function_binding/summary.md`.

**Observation:** PROJECTS currently marks Level 3 preservation as the active bottleneck.  
**Interpretation:** A07_03 must not run as a utility claim until a route partition is preserved through early training.  
**Boundary:** High route NMI or balanced load alone cannot justify A07_03.  
**Evidence links:** `../../experiments/A06/06_01_geometry_and_state_discovery/A06_01_04_E03_real_proxy_training_overwrite/summary.md`.

## 8. Claim Boundary And Next Decision

**Can claim:** the nested route-function diagnostic passes as a controlled positive control.

**Cannot claim:** MoE utility before preservation, semantic experts, real-DCLM utility, or scaling benefit.

**Next decision:** keep A07_03 parked for real utility until A06 provides a route partition that survives early training.
