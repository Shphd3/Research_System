---
anchor_id: A07_01_common_rare_conflict_metric_audit
current_short_name: nested_common_backbone_reproduction
parent_node: rq.expert_specialization
status: supported_controlled_nested_reproduction
created: 2026-06-23
retargeted: 2026-06-28
canonical_language: en
thinking_card_source: 07_01_common_rare_conflict_metric_audit_thinking_card.md
depends_on: A07_nested_singular_interference_mainline
---

# A07_01 Nested Common Backbone Reproduction Anchor

Thinking Card source: [07_01_common_rare_conflict_metric_audit_thinking_card.md](07_01_common_rare_conflict_metric_audit_thinking_card.md)

## 1. Problem Definition

**Parent problem:** A07 needs a valid surface for testing whether common-feature reuse becomes interference.

**Sharper subproblem:** First check whether our benchmark reproduces the mentor's common-backbone formation mechanism.

**Decision question:** Does standard CE/AdamW on nested-prefix data produce a stable common singular subspace whose gain continues to grow after common-feature accuracy saturates?

**Not in scope:** C3S improvement, MoE routing, expert utility, or real-language transfer.

## 2. Physical Priors

**P1: Frequency creates the first learned backbone.**  
Meaning: because $\pi_A$ is largest, $A$ should be learned before $AB$, $ABC$, and $ABCD$.  
Could be wrong if: all levels are equally easy or child labels do not require $A$.

**P2: Direction and gain separate.**  
Meaning: singular-vector alignment should stabilize earlier than singular-value growth.  
Could be wrong if: the top subspace keeps rotating as fast as the gain grows.

**P3: The surface must be nested, not marker-based.**  
Meaning: child features must inherit the parent constraint.  
Could be wrong if: an independent rare token predicts the child target.

## 3. Falsifiable Hypotheses

**H1: Common parent is learned first.**  
Supported if: $A$ accuracy saturates before $ABCD$ accuracy.  
Weakened if: all levels learn together or tail learns first.

**H2: Common subspace stabilizes before gain stops growing.**  
Supported if: $\delta_C(t)$ is low after $T_0$ while $S_C(t)$ continues to increase.  
Weakened if: no stable projector or no late singular-gain growth exists.

**H3: The task requires nested reuse.**  
Supported if: shortcut-only and independent-marker probes fail on child levels.  
Weakened if: the child task is solved without parent information.

## 4. Mathematical Model

**Objects:** levels $\ell$, frequencies $\pi_\ell$, selected matrix $W(t)$, common feature direction or common top-$k$ basis $V_C(t)$.

**Core decomposition:**
$$
W(t)=\sum_i \sigma_i(t)u_i(t)v_i(t)^\top,\qquad
P_C(t)=V_C(t)V_C(t)^\top.
$$

**Mechanism relation:** if $A$ creates the backbone, then $P_C(t)$ should stabilize near common warmup while $\sum_{i\in C}\sigma_i(t)^2$ keeps growing.

**Observable metrics:**
$$
\delta_C(t)=\|P_C(t)-P_C(T_0)\|_2,
$$
$$
S_C(t)=\sum_{i\in C}\sigma_i(t)^2.
$$

**Falsifier:** common accuracy does not precede tail accuracy, $P_C$ is not stable, or $S_C$ does not grow after warmup.

## 5. Computational Realization

**Input objects:** nested-prefix train/eval data, level labels for audit, CE/AdamW checkpoint sequence, selected matrix blocks.

**Computed variables:** per-level accuracy/loss, $P_C(t)$, $\delta_C(t)$, $S_C(t)$, shortcut probe accuracy.

**Algorithm stages:** build nested data; train baseline; select $T_0$ when $A$ saturates; compute projector drift and singular energy; run shortcut guards.

**Stage-local evidence:** per-level learning curves, singular drift/gain curves, nesting-validity table.

**Expected artifacts:** `protocol.md`, `summary.md`, `detailed.md`, `figures/a07_01_backbone_curves.png`, `tables/a07_01_aggregate.csv`.

## 6. Minimal Falsification Tests

**Test: two-phase common-backbone reproduction.**  
Question: does $A$ produce a stable high-gain common subspace under CE/AdamW?  
Intervention / comparison: nested-prefix baseline plus shuffled or marker-only guards.  
Primary metric: stable-late-gain signature: low post-$T_0$ $\delta_C(t)$ with positive $S_C(T)-S_C(T_0)$.  
Pass / fail / insufficient: pass if the signature appears and nesting guards pass; fail if the signature is absent; insufficient if $P_C$ cannot be estimated reliably.  
Why it decides: without this geometry, A07 cannot test the mentor mechanism.  
Failure means: the benchmark or the mechanism import must be revised.

## 7. Current Evidence

**Observation:** A07_01 nested full run `a07_nested_full_20260628_2` completed with 8 seeds. The stable-late-gain pass rate was `1.0000`, post-warmup max drift was `0.1373`, late common energy gain was `1.5115`, final $A$ accuracy was `1.0000`, and child-only tail shortcut accuracy was `0.6187`.
**Interpretation:** the controlled rank-one nested surface reproduces the mentor's common-backbone / late-gain geometry.
**Boundary:** this is a minimal controlled reproduction, not wide-transformer or real-language evidence.
**Evidence links:** `../../experiments/A07/A07_01_nested_common_backbone_reproduction/summary.md`, `../../experiments/A07/A07_01_nested_common_backbone_reproduction/detailed.md`.

**Observation:** The balanced-frequency guard had lower true-$A$ alignment (`0.2121`) and lower pass rate (`0.3750`) than the skewed nested condition.
**Interpretation:** the learned common backbone depends on frequency-skewed nesting rather than appearing equally under balanced training.
**Boundary:** the guard does not prove natural-language nesting; it only weakens a frequency-free explanation on this surface.
**Evidence links:** `../../experiments/A07/A07_01_nested_common_backbone_reproduction/tables/a07_01_aggregate.csv`.

**Observation:** The mentor notes predict two-phase singular learning and common-subspace stability diagnostics.  
**Interpretation:** A07_01 now instantiates those diagnostics in this codebase.  
**Boundary:** the reproduction is intentionally rank-one; a wide-MLP smoke before finalization showed more subspace drift.  
**Evidence links:** `../../../../../daily_research_reports/0625/docs/two_phase_singular_mode_learning_proof_and_test.md`, `../../../../../daily_research_reports/0625/docs/c3s_adamw_merged_rigorous_proof_with_negative_results.md`.

**Observation:** Prior A07_01 validated D07 as a controlled common/rare conflict audit.  
**Interpretation:** That result is now legacy evidence for audit tooling, not evidence for nested singular interference.  
**Boundary:** It should not be used to claim mentor-mechanism reproduction.  
**Evidence links:** `../../experiments/A07/A07_01_common_rare_conflict_metric_audit/summary.md`.

## 8. Claim Boundary And Next Decision

**Can claim:** A07_01 reproduces the nested common-backbone / late-gain mechanism on a controlled rank-one synthetic surface.

**Cannot claim:** tail interference, C3S benefit, MoE utility, or real-language transfer.

**Next decision:** use the frozen common projector surface for A07_02 tail update-control testing.
