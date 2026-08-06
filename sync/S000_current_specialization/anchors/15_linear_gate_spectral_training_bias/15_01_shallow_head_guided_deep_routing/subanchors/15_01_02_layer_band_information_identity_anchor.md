---
anchor_id: 15_01_02_layer_band_information_identity
status: completed_pass
canonical_language: en
companion_language: zh
thinking_card: 15_01_02_layer_band_information_identity_thinking_card_cn.md
parent: 15_01_shallow_head_guided_deep_routing
updated: 2026-07-31
---

# A15_01_02 Layer-Band Information Identity

## 1. Problem Definition

The single question is whether the same relative covariance band carries different functional variables at different depths of a capability-valid four-layer MoE. The registered variables are a coarse condition $a$, the one-step state $m=x+a$, and the two-step result $y=x+a+b$, all computed in a finite field.

The primary evidence is not raw label accuracy. It is the low-sample linear-readability increment of a layer-band cell over equal-dimensional random subspaces, together with the difference between a composition objective and a matched one-step objective.

## 2. Physical Priors

1. Spectral anisotropy changes Gate learning speed but does not identify functional content.
2. Layerwise computation can reorganize intermediate and composed variables with depth.
3. Redundant high-dimensional states make arbitrary random views readable; this cannot establish spectral specificity.

## 3. Falsifiable Hypotheses

**H1:** Composition training creates a depth- and band-specific readability increment for the intermediate or composed variable beyond equal-dimensional random directions, replicated in two seeds.

**Strongest rival:** Any depth trend is caused by output proximity, generic training progress, or random-projection preservation rather than layer-band identity.

**Falsifier:** The model is capable but no real band beats its random control; the pattern fails to replicate; or the same increment is already present in the one-step control and at initialization.

## 4. Mathematical Model

The data use $\mathbb Z_{17}$:

$$
m=(x+a)\bmod17,\qquad y=(m+b)\bmod17.
$$

For actual Gate input $g_\ell$, fit covariance basis $U_\ell$. Width 256 is divided into eight 32-dimensional fine bands, with head=`F1`, middle=`F2--F4`, and tail=`F5--F8`.

Let $A_{\ell,B,q}$ be the mean held-out probe accuracy across four registered low-sample fit sizes. Spectral specificity is

$$
S_{\ell,B,q}=A_{\ell,B,q}-Q_{0.95}(A_{\ell,R_{d_B},q}),
$$

and the objective contrast is

$$
\Gamma_{\ell,B,q}=S^{\rm compose}_{\ell,B,q}-S^{\rm one\text{-}step}_{\ell,B,q}.
$$

## 5. Computational Realization

Both conditions use the same four-layer causal Transformer-MoE: width 256, eight attention heads, eight top-1 experts per layer, expert width 512, no load-balancing auxiliary loss, and a shared non-gradient load-free score bias. Conditions differ only at the final query: the control predicts $m$, whereas the composition model predicts $y$. Each condition is trained with seeds 17 and 29.

Training, validation, covariance calibration, probe fit/validation, and sealed test use disjoint context IDs. Every atomic shift and value appears in training. Eight final-query $(a,b)$ pairs form a perfect matching and are absent from final-query training.

## 6. Minimal Falsification Tests

1. Audit leakage, atomic coverage, answer balance, oracle correctness, and shortcut baselines.
2. Require both seeds in both conditions to pass one-step capability; require composition seeds to pass unseen two-step recombination.
3. Replay actual Gate inputs and require stable split-half covariance bases.
4. Compare coarse and fine bands with equal-dimensional random directions, full state, and initialization.
5. Claim layer-band identity only when both seeds agree and sealed-test uncertainty supports it.

## 7. Current Evidence

A15_01_02_E01 completed with a registered Pass. The one-step control and two-step composition conditions were each trained with seeds 17 and 29. All four models passed unseen-combination, layer-2 intermediate-state, load, expert-use, and actual-Gate-input guards. Composition sealed-test accuracy on unseen $(a,b)$ pairs was 1.000/0.985.

Full-state readability of $y$ increased from 0.113 at layer 1 to 0.784 at layer 4 under composition, while the one-step controls remained at 0.103--0.156. This did not correspond to a composed result moving into tail: no $y$ H/M/T or fine-band cell beat equal-rank random directions in both seeds. The replicated identities were F1/head carrying intermediate $m$ at layers 3--4 and F2 retaining coarse $a$, with mean composition-over-control increments of 0.031/0.103 and 0.370/0.577.

Gate ablation showed that the native Router still relied primarily on F1/head; removing F2/M/T had negligible route and answer-NLL effects. The experiment therefore establishes both layer-specific information reorganization and a separation between encoding location and Router-use location. See the [result summary](/Projects/from-attention-to-search/main/experiments/A15/15_01_shallow_head_guided_deep_routing/A15_01_02_E01_controlled_layer_band_information_profile/summary.md).

## 8. Claim Boundary And Next Decision

This experiment establishes layer-specific band reorganization only in the registered controlled four-layer task. It cannot establish a natural-language semantic hierarchy, routing utility, or training-efficiency gains. The layer-2 intermediate state is explicitly supervised, so the result also does not establish fully spontaneous stage formation.

**Exactly one next decision:** distill the replicated layer-specific functional coordinates into fixed low-rank readouts that require no online PCA and submit them to an independent one-step compatibility gate. Matched cross-layer guidance remains blocked until a readout beats native-score, equal-dimensional random, token-shuffled, and wrong-layer controls.
