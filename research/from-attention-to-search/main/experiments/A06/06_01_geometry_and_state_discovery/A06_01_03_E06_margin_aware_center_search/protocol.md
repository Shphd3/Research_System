# Protocol: A06_01_03_E06 Minimal-Prior Margin-Aware Center Search

## 0. Approval Snapshot

**Approval status:** approved by user on 2026-06-26 for M1/M2 sanity check
only. Full 8-seed M1/M2 controlled audit approved by user on 2026-06-26 after
the sanity result. M3 remains unapproved.

**Purpose:** Check whether minimal-prior center-search methods are executable
and test whether the M2 continuous sanity signal is stable across eight
controlled seeds.

**Primary anchor:**
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

**Anchor decision question:** Can a no-label, no-position, no-route-prior
center search recover the controlled route-position feature partition better
than raw all-token and SAE/PCA/AE baselines?

**Anchor physical prior tested:** static all-token geometry is underidentified;
loss / gradient signal may add route relevance.

**Anchor core model term tested:** the label-free score
\(Q(C)=\operatorname{Stability}+\eta\operatorname{FunctionalCoherence}
-\gamma\operatorname{LowGap}-\lambda\operatorname{LoadCollapse}\).

**Anchor falsifier:** high label-free score does not improve held-out
route-position `feature_NMI`, while route-only positive controls remain
perfect.

**Experiment role:** operationalization / proxy test, first as a sanity check
and then as an 8-seed controlled audit of the promising M2 continuous signal.

**Primary metric from anchor:** held-out route-position `feature_NMI`.

**Claim boundary from anchor:** controlled bridge only; no real-DCLM,
preservation, utility, or deployable-method claim.

**Minimal setup:** reuse A06_01_03_E04/A06_01_03_E05 controlled no-position bridge with all
tokens available to the method and route-position labels hidden until audit.

**Basic configuration:** one-layer Transformer plus top-1 MoE, `d_model=128`,
`n_heads=4`, `ffn_dim=256`, four features, four experts, sequence length 32.
Route offset 3 is used only for final audit and positive control.

**Conditions to run:** raw all-token baseline, route-only positive control for
audit only, M1 static bootstrap margin selector, M2 continuous
gradient-weighted center search, and M2 top-20% gradient-weighted center
search. A06_01_03_E05 PCA/SAE values may be used as historical references. M3
hidden-gradient consensus is not run.

**Pass:** full audit supports the M2 continuous direction if it beats raw
all-token and M1 on mean held-out route-position `feature_NMI`, has better or
comparable load guards, and does not show shortcut domination.

**Fail:** full audit weakens the M2 continuous direction if it matches raw
all-token / M1, is seed-unstable, improves only load / margin / score, or
uses forbidden label / position / route-position information.

**Insufficient:** sanity is insufficient if leakage cannot be audited, hidden
states do not match A06_01_03_E05, or the run cannot reproduce known bad baselines.

**Cannot claim:** method success, real feature discovery, preservation, or
utility.

**Approval decision:** user approved the full 8-seed M1/M2 audit on 2026-06-26.

## 1. Anchor Alignment

**Decision question:** Test whether a minimal-prior proxy can select
feature-controlling gate centers.

**Physical prior tested:** generic hidden-state geometry is not enough; a
functional signal may be closer to routing relevance.

**Core model term tested:** \(Q(C)\) and its functional-coherence component.

**Falsifier:** the selector gets high \(Q(C)\) but matches raw all-token or
A06_01_03_E05 representation baselines on final `feature_NMI`.

**Claim boundary:** sanity only. A pass approves a full run; it does not update
the research claim by itself.

## 2. Tested Hypothesis

Gradient- or loss-aware center search can produce less degenerate and more
feature-relevant center candidates than static all-token clustering under the
minimal-prior rule.

## 3. Rival Explanations

**R1: Stable background partition.** The selector may find position, token
frequency, or neutral-state geometry.

**R2: Difficulty shortcut.** Gradient or loss may select hard tokens rather
than route-relevant states.

**R3: Load-only success.** Better balance may raise the label-free score
without improving feature identity.

**R4: Implementation artifact.** Center conversion or hidden-state capture may
break the comparison.

## 4. Data / Model / Algorithm / Objective

**Data:** A06_01_03_E04/A06_01_03_E05 `C4_all_position_scope` controlled no-position bridge.

**Model:** the same one-layer Transformer plus top-1 MoE used in A06_01_03_E05.

**Allowed method inputs:** all-token hidden states, per-token teacher-forced
loss, optional hidden gradients, and train/held-out split identifiers.

**Forbidden method inputs:** feature labels, position labels, slot offset,
route-position membership, or any metric computed from them.

**Final audit inputs:** after centers are frozen, controlled feature labels,
positions, and route offset may be used to compute `feature_NMI` and shortcut
guards.

**Objective:** select hidden-space center rows that maximize label-free
stability, functional coherence, margin buffer, and non-collapse.

## 5. Conditions, Seeds, And Checkpoints

Sanity seeds: `20260623` and `20260624`. Full audit seeds: `20260623` to
`20260630`. The full audit runs M1 and M2, plus raw all-token and route-only
controls. M3 remains parked.

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Raw all-token k-means | A06_01_03_E05 baseline boundary | static all-token geometry | known bad reference | primary comparison | reproduces known baseline range | silently improves because setup changed | missing baseline table | `tables/sanity_methods.csv` |
| PCA q=4 and SAE L1 8x | A06_01_03_E05 representation boundary | reconstruction / variance proxy | historical known failed controls, not rerun in M1/M2 sanity | secondary reference | previous A06_01_03_E05 values are cited correctly | report treats them as newly rerun | missing historical reference | `summary.md` |
| Route-only k-means | positive control only | task is possible | confirms route geometry exists | audit control | near-perfect `feature_NMI` | below expected control | route-state audit unavailable | `tables/positive_controls.csv` |
| Static bootstrap margin | H1 static selector | stability + low-gap + load | tests pure minimal-prior geometry | primary comparison | produces non-collapsed centers | matches collapse or invalid centers | score cannot be computed | `tables/sanity_methods.csv` |
| Gradient-weighted center search | H2 functional proxy | gradient norm / loss sensitivity | tests whether functional signal helps | primary comparison | non-degenerate and at least not worse than static | selects difficulty shortcut or collapses | gradients unavailable | `tables/sanity_methods.csv` |
| Hidden-gradient consensus | H2 functional proxy | hidden + gradient coherence | parked until M2 mechanism is understood | not run | remains unclaimed | accidentally run in this full audit | not applicable | later protocol change |
| Post-selection shortcut audit | R1/R2/R3 | shortcut guards | checks false positives | secondary evidence | no obvious shortcut dominates | gain explained by shortcut | guard labels missing | `tables/shortcut_audit.csv` |

## 6. Primary Metric

Held-out route-position `feature_NMI` decides whether selected centers recover
the controlled feature partition. The cost of a false positive is high: a
method that only improves balance, gap, or gradient coherence would lead to a
wrong initialization claim. The cost of a false negative is lower in the sanity
run: a weak result can still motivate failure decomposition before parking the
idea.

## 7. Secondary Metrics

- max load and active experts;
- normalized gap distribution: median and 5th percentile of \(\rho_C(h)\);
- split stability: assignment NMI across bootstrap splits on held-out tokens;
- functional coherence: within-cluster gradient-direction concentration and
  gradient-norm enrichment;
- post-selection position NMI, role composition, loss-bin composition, and
  token-frequency composition;
- reconstruction error only for PCA/SAE reproducibility, not as success.

## 8. Known Good / Known Bad / Known Confusing Cases

**Known good:** route-only k-means should be close to `feature_NMI=1.0`.

**Known bad:** raw all-token, PCA q=4, and SAE L1 8x should behave like A06_01_03_E05,
not like the route-only control.

**Known confusing:** a selector may have high stability, balanced load, and
large gap while still having low final `feature_NMI`.

## 9. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| Hidden-state load | Are states and splits aligned with A06_01_03_E05? | counts, dimensions, seed IDs | pass if shapes and seed metadata match | `tables/state_manifest.csv` | method inputs |
| Leakage audit | Did selection see forbidden information? | code-path checklist and saved score inputs | fail on any feature/position/route field in selection | `tables/leakage_checklist.csv` | validity gate |
| Gradient extraction | Are per-token functional signals available? | loss/gradient shape and finite-value checks | fail if gradients are missing or mostly invalid | `tables/gradient_profile.csv` | M2/M3 inputs |
| Center generation | Do all methods output K hidden centers? | center count, norm, empty cluster count | fail if K is wrong or empty clusters dominate | `tables/center_profile.csv` | audit centers |
| Label-free scoring | Does \(Q(C)\) compute without labels? | stability, gap, load, functional score | fail if score uses forbidden fields | `tables/score_profile.csv` | selected centers |
| Final audit | What does the frozen center set recover? | held-out route-position labels after selection | sanity only; no final claim | `tables/sanity_methods.csv` | next decision |

## 10. Algorithm Specification

### Common Center Conversion

**Input:** token hidden states and cluster assignments.

**Parameters:** `K=4`, matching the number of experts in the controlled bridge.

**Steps:** assign each token to one cluster; compute each hidden-space center
as the mean of original hidden states in that cluster; use these means as gate
rows for held-out assignment.

**Outputs:** one \(K \times d_\text{model}\) center matrix per method.

**Fail conditions:** empty clusters, wrong center shape, non-finite centers, or
use of forbidden fields.

### M1: Static Bootstrap Margin Selector

**Input:** all-token hidden states only.

**Parameters:** `B=16` bootstrap candidate banks, `K=4`, fixed random seeds.

**Steps:** fit k-means on bootstrap samples; compute held-out all-token
assignments; score candidates by split stability, normalized gap, and load;
select the highest-scoring center set.

**Outputs:** selected centers and label-free score table.

**Failure reasons:** high score caused by load collapse, unstable assignments,
or no reproducible candidate.

### M2: Gradient-Weighted Center Search

**Input:** all-token hidden states plus per-token loss or hidden-gradient norm.

**Parameters:** gradient weight mode in `{continuous, top20}`; gradient norms
are clipped at the 95th percentile before weighting.

**Steps:** compute token weights from loss/gradient norm; fit weighted k-means
on hidden states; convert clusters to hidden-space centers; score by \(Q(C)\).

**Outputs:** selected centers, gradient profile, and score table.

**Failure reasons:** gradients unavailable, high-gradient tokens dominated by a
known shortcut, or weighted centers collapse.

### M3: Hidden-Gradient Consensus

**Input:** hidden states and hidden-gradient vectors.

**Parameters:** gradient projection dimension `q=8` if full vectors are too
large; concatenation scale `alpha=0.5`.

**Steps:** standardize hidden states and gradient features separately; cluster
the concatenated representation; convert each cluster back to the mean original
hidden state; score by stability, gap, load, and gradient coherence.

**Outputs:** centers, hidden/gradient cluster agreement, and final audit table.

**Failure reasons:** gradient vectors are too noisy, concatenation scale
dominates hidden geometry, or consensus selects a shortcut partition.

## 11. Success / Failure / Insufficient Evidence

**Sanity success:** the run produces all required tables, reproduces known
good/bad controls, passes leakage audit, and shows that M1/M2 can generate
valid center sets.

**Full-audit support:** M2 continuous beats raw all-token and M1 on mean
held-out route-position `feature_NMI`, has better or comparable load guards,
and does not show shortcut domination.

**Sanity failure:** any required stage fails before final audit, or the
candidate methods are degenerate before comparison.

**Full-audit weakening:** functional-aware selectors improve only label-free
scores or load, match / underperform raw all-token `feature_NMI`, or are
seed-unstable.

**Insufficient evidence:** implementation runs but cannot rule out leakage or
shortcut selection.

**Full-audit support:** M2 continuous beats raw all-token and M1 on mean
held-out route-position `feature_NMI`, has better or comparable load guards,
and does not show shortcut domination.

**Full-audit weakening:** M2 continuous matches raw all-token / M1, is
seed-unstable, or improves only load / margin / score without improving
`feature_NMI`.

## 12. What This Cannot Claim

This sanity check cannot claim that the method works, that real-DCLM features
are found, that early training preserves the partition, or that experts become
useful. It can only decide whether the proposed minimal-prior methods are
defined and executable enough for a full controlled run.

## 13. Review Notes And Protocol Changes

Review notes:

1. Confirm that loss / hidden-gradient signal is allowed under the
   minimal-prior rule. Approved for M1/M2 sanity and full audit.
2. Confirm that post-selection position and route-position audits are allowed
   as guards, not as method inputs. Approved.
3. Sanity used two seeds first. Full eight-seed run approved after sanity.
4. Confirm whether M3 should use gradient vectors or only gradient norms if
   memory becomes the first blocker. Still parked.
