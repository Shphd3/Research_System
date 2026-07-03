---
anchor_id: A06_19_minimal_prior_margin_aware_center_search
parent_node: rq.feature_specialization.proxy_preservation
status: full_audit_updated
created: 2026-06-26
canonical_language: en
---

# A06_19 Minimal-Prior Margin-Aware Center Search Anchor

Document status: full-audit-updated anchor. M1/M2 sanity passed as an
execution check, but the full 8-seed controlled audit weakened the M2
continuous direction. M3 remains unapproved. The central constraint is minimal
prior: the method may not use feature labels, position labels, slot offset, or
route-position priors during fitting or selection.

## 0. Thinking Card

**Phenomenon:** A06_18 shows that raw all-token clustering and SAE/PCA/AE
representation clustering do not reliably find feature-controlling centers.
The only perfect controlled fits used a route-position or slot-offset prior,
which is not available in the intended setting.

**Mechanism guess:** Static all-token geometry is underidentified. A useful
center-search method needs a label-free signal that is closer to routing
control: stable assignment, non-collapsed load, margin buffer, and possibly
loss/gradient sensitivity.

**Key variables:** all-token hidden states $A$, per-token loss or hidden
gradient $u_i$, candidate center set $C$, induced assignment $a_C(h)$,
normalized top-1/top-2 gap $\rho_C(h)$, load, functional coherence, and final
controlled `feature_NMI`.

**Causal relation:** If a center set captures feature-controlling route
geometry, then its assignments should be stable and non-collapsed, and the
states it groups should have coherent functional signal before feature labels
are used.

**Observable metric:** the primary audit metric is held-out route-position
`feature_NMI` in the controlled bridge. Labels and route positions are used only
after center selection, for evaluation and leakage audit.

**Rival Explanations:** The selector may find stable background geometry,
frequency / difficulty structure, or gradient shortcuts instead of feature
centers. It is also possible that no label-free all-token signal identifies the
feature centers under this minimal-prior setting.

**Decision:** Full audit weakened M1/M2 as reliable minimal-prior
center-search methods. Do not test preservation with these centers. Next
diagnose why raw all-token improves with larger calibration size and why M2
continuous fails in several seeds.

## 1. Problem Definition

**Parent problem:** A06 asks how to initialize router rows so that a feature
partition can be preserved through early training.

**Sharper subproblem:** Correct route-position centers can preserve by positive
margin, but real center search cannot assume route-position knowledge. We need
to test whether any minimal-prior signal can find useful centers from all
tokens.

**Decision question:** Can a no-label, no-position, no-route-prior center
search produce hidden-space gate centers that recover the controlled
route-position feature partition better than raw all-token and SAE/PCA/AE
baselines?

**Not in scope:** real-DCLM semantic features, preservation through training,
expert utility, or a deployable initialization method.

## 2. Physical Priors

**P1: Static all-token geometry is underidentified.**  
Meaning: many stable partitions can exist in all hidden states, but most do not
control the feature route partition.  
Could be wrong if: a purely static, no-prior all-token selector reliably
recovers the controlled feature partition.

**P2: A margin buffer is necessary but not sufficient.**  
Meaning: A06_17_02 suggests successful preservation needs positive router
margins, but a label-free top-1/top-2 gap can also describe the wrong stable
partition.  
Could be wrong if: high label-free gap alone predicts final `feature_NMI`.

**P3: Functional signal may expose route relevance.**  
Meaning: loss or hidden-gradient sensitivity may mark states whose routing
choice matters more for the model objective than neutral background states.  
Could be wrong if: gradient-aware selectors behave like raw all-token
clustering or select only frequency / difficulty shortcuts.

## 3. Falsifiable Hypotheses

**H1: Pure static minimal-prior center search is insufficient.**  
Supported if all-token bootstrap / margin selectors match A06_18 baselines on
held-out route-position `feature_NMI`.  
Weakened if a static selector beats raw all-token and SAE/PCA/AE baselines
without using labels, positions, or route priors.

**H2: Functional-aware center search is a better proxy for route relevance.**  
Supported if gradient- or loss-aware selectors beat static baselines and keep
non-collapsed load and reasonable margin buffer.  
Weakened if they improve only label-free score, reconstruction, load, or
gradient coherence without improving final `feature_NMI`.

**H3: Minimal-prior center search may be unidentifiable in this bridge.**  
Supported if route-only positive controls remain perfect but every no-prior
selector fails.  
Weakened if any no-prior selector approaches route-only without leaking
position or feature information.

## 4. Mathematical Model

**Objects:** all-token hidden states $A=\{h_i\}$, optional per-token functional
signal $u_i=\nabla_{h_i}\ell_i$ or scalar loss / gradient norm, candidate
centers $C_m=\{c_{m,1},\ldots,c_{m,K}\}$, and controlled final audit labels
used only after selection.

**Core decomposition:**

$$
A = R \cup B,
$$

where $R$ is the unknown feature-controlling population and $B$ is background
or non-feature-dominant states. The method observes only $A$ and optional
functional signal $u_i$, not $R$.

**Induced routing:**

$$
a_m(h)=\arg\max_k c_{m,k}^{\top}h.
$$

**Normalized label-free gap:**

$$
\rho_m(h)=
\frac{
  c_{m,a_m(h)}^\top h-\max_{j\neq a_m(h)}c_{m,j}^{\top}h
}{
  \operatorname{std}_j(c_{m,j}^{\top}h)+\epsilon
}.
$$

This gap is not a feature margin. It is only a label-free proxy for whether a
state lies confidently inside some router cone.

**Selection score:**

$$
Q(C_m)=
\operatorname{Stability}(C_m)
+\eta\operatorname{FunctionalCoherence}(C_m)
-\gamma\operatorname{LowGap}(C_m)
-\lambda\operatorname{LoadCollapse}(C_m).
$$

The score must not use feature labels, position labels, slot offset, or
route-position membership. These are allowed only in post-selection audits.

**Falsifier:** high $Q(C_m)$ does not predict held-out route-position
`feature_NMI`, while route-only positive controls remain perfect.

## 5. Computational Realization

**Input objects:** controlled A06 no-position bridge hidden states, per-token
teacher-forced loss, optional hidden gradients, and held-out split metadata.

**Computed variables:** candidate centers, all-token held-out assignments,
normalized gaps, load, stability, functional coherence, and post-selection
feature / position / route audits.

**Algorithm stages:** generate candidate centers from all tokens; score them
without labels or positions; freeze the selected centers; then run controlled
audits using labels and route position only after selection.

**Stage-local evidence:** leakage audit, positive-control audit, center
degeneracy, load, gap distribution, functional-coherence table, and final
`feature_NMI`.

**Expected artifacts:** protocol, sanity tables, leakage checklist, method
failure table, and a later full-run summary only if the sanity check passes.

## 6. Minimal Falsification Tests

| Test | Question | Comparison | Primary metric | Pass / fail / insufficient | Failure means |
|---|---|---|---|---|---|
| Sanity check | Are the minimal-prior methods executable without leakage? | raw all-token, A06_18 best baselines, static margin, functional-aware selectors, route-only audit control | held-out route-position `feature_NMI`, interpreted only as a sanity audit | pass if methods run, no leakage is detected, route-only control passes, and centers are non-degenerate; fail if gradients/centers/metrics cannot be produced or route-only fails; insufficient if leakage cannot be ruled out | implementation or protocol validity is not ready |
| Minimal-prior center audit | Does any no-prior selector beat known baselines? | static vs functional-aware selectors against raw all-token and SAE/PCA/AE | held-out route-position `feature_NMI` | pass if a no-prior selector beats all known baselines and is not load-collapsed; fail if it only improves label-free score or load; insufficient if positive controls fail | the tested proxy is or is not a useful route-relevance signal |
| Shortcut guard | Is the selected partition a shortcut? | selected assignments vs post-hoc position, frequency, loss, and role audits | guard metrics plus selected-role composition | pass if feature gain is not explained by shortcuts; fail if high score is shortcut-dominated | functional signal selected background structure |

## 7. Current Evidence

**Observation:** A06_17 found that route-only and slot-offset-3 pools recover
the feature partition perfectly, while all-position clustering often merges
features.

**Observation:** A06_18 found that raw all-position, PCA, bottleneck AE, and SAE
code clustering do not approach the route-only / slot-offset-3 controls. SAE
can reconstruct well while failing the route-readout audit.

**Observation:** A06_17_02 found that correct center initialization preserves
feature routing by positive raw route margins, not by active center tracking.

**Observation:** A06_19 M1/M2 sanity passed. Route-only control stayed perfect
(`feature_NMI=1.0`). Raw all-token mean was `0.672`. M1 static bootstrap margin
was weak (`0.751`). M2 continuous gradient weighting was promising (`0.933`,
with one perfect seed and one `0.866` seed). M2 top-20% gradient weighting
failed (`0.634`) and was load-collapsed.

**Observation:** A06_19 full 8-seed audit weakened that sanity signal. Route-only
remained perfect (`1.000`). Raw all-token was stronger than expected (`0.863`).
M1 did not beat raw (`0.843`). M2 continuous underperformed raw and M1
(`0.784`, min `0.621`). M2 top-20% remained weak (`0.756`).

**Interpretation:** feature centers exist in the controlled bridge, but the
tested minimal-prior selectors do not reliably find them. Gradient norm can
reshape the all-token population, but it is not a stable route-relevance proxy
in this operationalization.

**Evidence links:**

- `../../experiments/A06/A06_17_all_position_route_relevant_feature_discovery/summary.md`
- `../../experiments/A06/A06_18_label_free_route_relevant_state_selector/summary.md`
- `../../experiments/A06/A06_17_02_router_center_tracking_preservation/summary.md`
- `../../experiments/A06/A06_19_minimal_prior_margin_aware_center_search/summary.md`
- `../../experiments/A06/A06_19_minimal_prior_margin_aware_center_search/detailed.md`

## 8. Claim Boundary And Next Decision

**Can claim now:** M1 and M2, as implemented here, do not provide a reliable
minimal-prior center-search method in the controlled bridge.

**Cannot claim now:** all functional signals fail, all gradient methods fail,
real-DCLM semantic feature discovery is impossible, training preservation is
impossible, or expert utility is impossible.

**Next decision:** do not proceed to preservation with M1/M2 centers. Diagnose
the sample-size effect and feature-merge structure of raw all-token versus M2
continuous before adding M3 or another method.
