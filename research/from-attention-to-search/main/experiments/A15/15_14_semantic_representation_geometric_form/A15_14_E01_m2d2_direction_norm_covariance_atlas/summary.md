# Summary: A15_14_E01 M2D2 Direction, Radius, and Covariance Atlas

Primary Anchor: [A15_14 Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_14_semantic_representation_geometric_form/15_14_semantic_representation_geometric_form_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md)  
Detailed record: [detailed.md](detailed.md)  
Result status / eligibility: `ELIGIBLE_FULL_RUN`; knowledge wording is `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`.

## Result Snapshot

**Registered verdict:** `RADIUS_CONTRIBUTING` for both coarse and parent-
conditional fine tasks at the fixed mean-pooled block-14-output cell.

**What is established:** direction carries the larger share of accessible
domain structure, but radius is also label-associated and observed radius
improves the registered full-vector density model over a radius-permuted
control. Independent covariance-shape contribution does not pass its threshold.

**Critical boundary:** the same directional analysis at the final token is
near zero. The established signal belongs to a whole-window mean-pooled
representation, not yet to the per-token state consumed by a token Router.

**What we do next:** before choosing a token-Router geometry, compare current-
token state with deployable causal-prefix pooling under a lexical-control
audit at block 14.

## Decision-Bearing Setup

Question: Is M2D2 coarse/fine domain information carried by direction, radius,
or class-dependent shape in frozen Qwen3-0.6B-Base states?  
Treatment and control: direction-only vMF mixture, radius-only mixture, full-
vector centroid/density models, and observed radius versus radius permutation.  
Changed variable: which geometric information the unsupervised model receives.  
Held fixed: data, frozen model, mean pooling, hidden-state index 15, train-only
rank-64 PCA basis, three clusters, splits, and 20 restarts.  
Primary metric: confirmation normalized mutual information (NMI), from 0 to 1.  
Known limitation: the statistical unit is a packed text window, not an
independent source document; M2D2 domain labels can be partly lexical/topic
signals.

## Verdict Basis

| Registered rule | Coarse result | Fine result | Verdict |
| --- | ---: | ---: | --- |
| Directional vMF NMI exceeds shuffled-label 97.5% null | 0.1289 vs 0.0014 | 0.3223 vs 0.0028 | readable |
| Radius-only NMI exceeds shuffled-label 97.5% null | 0.0315 vs 0.0011 | 0.1397 vs 0.0025 | radius-associated |
| Observed minus permuted-radius diagonal-GMM NMI, 95% CI lower bound > 0.02 | [0.1237, 0.1451] | [0.0321, 0.0619] | radius contribution gate passes |
| Shape minus direction and centroid lower bounds both > 0.02 | [0.0094, 0.0360] and [0.0088, 0.0338] | [0.0162, 0.0520] and [0.0276, 0.0627] | independent shape gate fails |

## Central Evidence

![Fixed-cell carrier and radius meaning](figures/primary_geometry_and_radius_meaning.png)

How to read: in the left panel, direction is much more semantic than radius
alone, while the diagonal density model is highest; in the right panel, larger
projected radius tracks lower model surprise much more than lexical rarity
after domain means are removed.

![Pooling location guard](figures/pooling_location_guard.png)

How to read: the solid whole-window mean curve contains domain structure, while
the dashed final-token curve remains near zero at almost every layer.

## Claim Boundary

Can claim: at the fixed block-14-output, mean-pooled, rank-64 coordinate,
direction is the primary accessible carrier and radius contributes additional
registered model-family evidence for M2D2 domain semantics.

Cannot claim: semantic information is uniformly present in each token state;
covariance is independently necessary; the native Gate uses these quantities;
experts benefit; next-token loss improves; or the signal is abstract semantics
rather than aggregated lexical/topic evidence.

## Next Decision

Decision: audit block-14 current-token direction/radius against a causal-prefix
pooled state with lexical controls before selecting a token-Router input.  
Completion criterion: one held-out comparison identifies a Router-visible
causal object that retains the mean-pooled direction/radius signal beyond
lexical composition.  
Resume action: formalize that one token-versus-causal-prefix experiment only
after the researcher confirms or corrects this result wording.

