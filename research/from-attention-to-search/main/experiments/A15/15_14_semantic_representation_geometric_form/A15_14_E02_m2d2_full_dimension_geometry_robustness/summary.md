# Summary: A15_14_E02 M2D2 Full-Dimension Geometry Robustness

Primary Anchor: [A15_14 Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_14_semantic_representation_geometric_form/15_14_semantic_representation_geometric_form_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md)  
Detailed record: [detailed.md](detailed.md)  
Result status / eligibility: `ELIGIBLE_FULL_RUN`; knowledge wording is `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`.

## Result Snapshot

**Registered verdict:** `RADIUS_CONTRIBUTING` for both coarse and parent-
conditional fine tasks in the centered original 1,024-dimensional coordinate.

**What is established:** removing PCA does not change the typed carrier
verdict. Direction remains the larger stand-alone carrier and radius remains
label-associated and important to the registered full-density model. The
independent shape gate still fails.

**What changes:** the fine-domain diagonal-Gaussian NMI falls from 0.3569 at
PCA-64 to 0.3151 at raw-1,024, while directional NMI changes only from 0.3223
to 0.3180. The apparent fine-domain shape advantage is therefore projection-
sensitive rather than strengthened by retaining all coordinates.

**Critical boundary:** the raw full-dimensional final-token direction NMI is
0.0014 coarse and 0.0060 fine at the fixed layer. The positive result still
belongs to a whole-window mean, not a demonstrated token-Router state.

**What we do next:** stop. Do not begin the current-token semantic-object
screen or the second geometry gate until the researcher explicitly approves
that next scope.

## Decision-Bearing Setup

Question: Does the E01 direction/radius/shape conclusion depend on PCA
compression?  
Treatment: subtract the training mean and retain all 1,024 hidden dimensions.  
Reference: the same cell after train-only PCA to 64 dimensions.  
Changed variable: projection and dimension only.  
Held fixed: 16,128 saved windows, frozen Qwen states, splits, labels, block-14
output, mean pooling, five model families, three clusters, 20 restarts,
radius permutation, 1,000 label nulls, and 10,000 window bootstraps.  
Primary metric: confirmation normalized mutual information (NMI), from 0 to
1.  
Known limitation: the uncertainty unit is a packed text window, and M2D2
domain labels can be recovered partly from aggregated lexical/topic content.

## Verdict Basis

| Registered rule | Raw-1,024 coarse | Raw-1,024 fine | PCA-64 reference | Verdict |
| --- | ---: | ---: | ---: | --- |
| Directional vMF NMI exceeds its 97.5% label null | 0.1298 vs 0.0013 | 0.3180 vs 0.0027 | 0.1289 / 0.3223 | readable and dimension-robust |
| Radius-only NMI exceeds its 97.5% label null | 0.0321 vs 0.0010 | 0.1283 vs 0.0025 | 0.0315 / 0.1397 | radius-associated in raw space |
| Observed minus permuted-radius diagonal NMI, 95% CI lower bound > 0.02 | [0.1424, 0.1705] | [0.1666, 0.1996] | [0.1237, 0.1451] / [0.0321, 0.0619] | radius contribution gate passes |
| Shape beats direction and centroid by both lower bounds > 0.02 without radius explaining it | [0.0198, 0.0441] and [0.0179, 0.0440] | [-0.0198, 0.0144] and [-0.0132, 0.0191] | gate also failed at PCA-64 | independent shape gate fails |

## Central Evidence

![Raw 1,024 dimensions versus PCA-64](figures/raw1024_vs_pca64_primary_geometry.png)

How to read: orange raw-dimension direction and radius bars stay close to the
blue PCA-64 bars, while the fine-domain diagonal-density bar drops below the
direction bars after all 1,024 coordinates are retained.

![Raw full-dimensional pooling guard](figures/raw1024_pooling_location_guard.png)

How to read: whole-window means carry visible domain agreement across layers;
the final-position curves remain near zero, including at the fixed dotted
layer.

## Claim Boundary

Can claim: at the fixed whole-window mean-pooled block output, the E01 reading
is not created by PCA compression; centered raw-1,024 M2D2 domain information
is direction-primary and radius-contributing under the registered model
families.

Cannot claim: PCA is irrelevant to every estimator; raw coordinates improve
semantic recovery; radius supplies unique conditional information; covariance
is necessary; individual token states are semantically clustered; the native
Gate uses the signal; experts specialize; or language modeling improves.

## Next Decision

Decision: await explicit researcher approval before opening the current-token
semantic-object screen; the second geometry gate remains downstream and also
unauthorized.  
Completion criterion: the researcher names and approves the next screening
scope.  
Resume action: if approved, formalize the current-token versus causal-prefix
screen before any execution.
