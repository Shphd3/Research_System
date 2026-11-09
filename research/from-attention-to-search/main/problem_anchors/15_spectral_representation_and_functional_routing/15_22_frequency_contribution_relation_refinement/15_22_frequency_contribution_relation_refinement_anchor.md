# Frequency-Contribution Bridge and Within-Band Relation Refinement

Status: **DRAFT_NOT_EXECUTABLE / awaiting researcher confirmation**. This is an eight-section extraction of the user-supplied attachment, not authorization for a new experiment or a report of newly executed results. The attachment records raw last-layer contribution share as the primary rule and calibration against the usual level as the control; this extraction does not independently verify that historical approval or promote proposed defaults to researcher decisions. The complete original is preserved in the [source copy](sources/feishu_report_anchor_v0.1_cn.md). Execution settings and unresolved choices belong to the [Protocol](../../../experiments/A15/15_22_frequency_contribution_relation_refinement/20261019_bridge_dispatch/protocol.md).

## 1. Problem Definition

**Can the contributions of different feature-frequency bands to the current last-layer representation describe inputs beyond the current token ID, and can φ-based refinement within a frequency band further improve reproducible organization of the inputs actually received?**

The parent problem is to help a model learn and retain more content through expert specialization under fixed parameter and compute budgets. Existing records distinguish membership organization, actual reception, and learning benefit: calibration improving reception did not guarantee better held-out learning. This round chooses to inspect the basis for specialization first; it does not make this route a necessary condition for improving learning.

The current position consists of the current token and visible prefix used to predict the next token. Low frequency means a feature has a low hit rate on TRAIN effective prediction positions; it does not mean a rare token, rare knowledge, or difficult learning. The objects in scope are input profiles, relations, and fixed routing under a frozen base and dictionary. This round does not automatically train experts or estimate capacity multipliers.

If profiles vary beyond token identity and relation refinement retains reproducible organization beyond matched random controls, retain this route for subsequent design discussion. If the predicted token-frequency direction is contradicted, withdraw that directional prediction. If relations add no evidence, retain a frequency baseline without adding relation complexity. Inadequate support or isolation remains insufficient evidence, not proof of absent structure.

## 2. Physical Priors

1. **Candidate intuition:** contextual representations contain features of different frequencies. Their last-layer contribution composition may describe an input more finely than its token ID. This is a proposed representation profile, not an identified semantic function.
2. **Candidate intuition:** selecting the most prominent frequency band and then refining receivers by its concrete feature relations may avoid routing solely by token identity or assigning all low-frequency content to one expert. Similar frequency and co-occurrence do not guarantee compatible joint learning.
3. **Measurement assumption:** the frozen dictionary and original gate provide shared feature coordinates; last-layer decoder amplitude constructs a contribution proxy. This proxy does not measure information, causal effect, or gradient benefit. The complete representation still carries high-frequency information; routing does not remove common content.

## 3. Falsifiable Hypotheses

**H1: token-frequency bridge.** The last-layer contribution share of low-frequency features is positively associated with the rarity of the current token ID. A rival is that the profile primarily repeats token identity, format, or position. A weak or reversed association challenges the proposed positive bridge. Variation across contexts for a fixed ID only indicates additional variation; it does not make all residual variation semantic.

**H2: incremental relation organization.** Within the same frequency band, with the same expert count and matched subgroup sizes and fine frequency distributions, φ-based subgroups retain additional co-occurrence in review dialogues and produce more consistent atomic composition among received inputs than matched random subgroups. A rival is that high TRAIN φ follows only from construction, finite samples, or marginal-frequency preferences without reproducible differences used by routing.

**H3: subsequent learning value, NOT RUN.** Under common training budgets and evaluation rules, frequency-first routing with relation refinement improves held-out task performance relative to matched random refinement while retaining existing capabilities. Raw routing and calibration are compared separately. H1/H2 do not imply H3; the current analysis without training does not fill in an H3 conclusion.

## 4. Mathematical Model

**Inputs and frozen state.** TRAIN contains \(N\) effective answer-prediction positions and the full dictionary contains \(F=16{,}384\) features. \(x_t\) is the current token with its visible prefix, \(v_t\) the current token ID, and \(v_{t+1}\) the prediction target. \(h_{28}(x_t)\) is the last-layer representation. \(z_i(x_t)\) is the nonnegative shared activation after the frozen CrossCoder's original gate, still jointly encoded from 14 layers; \(d_{28,i}\) is feature \(i\)'s last-layer decoder vector. The gate is not replaced by exactly Top256 at every position.

**Frequency and contribution are distinct.** Define the hit indicator \(A_i(x_t)=\mathbf 1[z_i(x_t)>0]\), feature frequency \(p_i=N^{-1}\sum_t A_i(x_t)\), and current-token frequency \(f(v)=N^{-1}\sum_t\mathbf 1[v_t=v]\). Both denominators are the specified TRAIN effective prediction positions. Frequencies over complete input sequences are only auxiliary definitions.

The last-layer contribution-amplitude proxy and band profile are

\[
c_i(x_t)=z_i(x_t)\lVert d_{28,i}\rVert_2,\qquad
M_b(x_t)=\sum_{i\in F_b}c_i(x_t),\qquad
R_b(x_t)=\frac{M_b(x_t)}{\sum_{j=1}^{F}c_j(x_t)}.
\]

\(F_b\) denotes a positive-frequency band frozen from TRAIN and ordered from low to high. \(M_b\) is total contribution, not divided by membership count; \(R_b\) is raw contribution share, not a calibrated score or explained variance. Features with zero TRAIN hits belong to the unknown-frequency set \(U\), not the lowest band. \(F_1,\ldots,F_B,U\) cover the full dictionary. The profile denominator retains both \(U\) and the most frequent features. Contributions from \(U\) in review data are reported separately, without redefining bands using review frequencies. Shares are not estimable when total contribution is zero. \(B\), boundaries, and other settings remain unresolved in the Protocol.

**Primary raw-contribution rule.** Let \(G_{b,k}\) be subgroup \(k\) within band \(b\). Every positive-frequency feature belongs to exactly one subgroup, with \(\sum_b K_b=K\). Select the band with the largest total contribution, then its subgroup with the largest contribution:

\[
b^*=\operatorname*{arg\,max}_{b}M_b(x_t),\qquad
k^*=\operatorname*{arg\,max}_{k}\sum_{i\in G_{b^*,k}}c_i(x_t).
\]

For positive total contribution, the first step is equivalent to maximizing \(R_b\) over TRAIN-observed bands. Send the **complete** \(h_{28}(x_t)\) to expert \((b^*,k^*)\), rather than only the subgroup components. Ties and positions with zero contribution from all known candidates use a previously frozen position hash independent of answer labels. Report fallback separately; it is not evidence of effective routing.

**Calibration control.** Replace only the first step by maximizing \(M_b(x_t)/\mu_b\), where \(\mu_b=\mathbb E_{\mathrm{TRAIN}}[M_b(x_t)]\). The second step and all other conditions remain unchanged. This compares largest absolute contribution with greatest prominence relative to the usual level. \(\mu_b\) must be estimable with adequate support; zero or unestimable denominators are blockers rather than opportunities for arbitrarily small denominators. Equalizing mean scores does not ensure equal loads.

**Within-band relation.** With \(p_{ij}=\mathbb E_{\mathrm{TRAIN}}[A_iA_j]\), binary activation correlation is

\[
\phi_{ij}=\frac{p_{ij}-p_ip_j}
{\sqrt{p_i(1-p_i)p_j(1-p_j)}}.
\]

Only within-band \(w_{ij}=\max(\phi_{ij},0)\) is used as a positive co-occurrence candidate. If \(p_i\) or \(p_j\) equals 0 or 1, φ is undefined and must be reported as such rather than as evidence of no relation. Banding does not eliminate all marginal-frequency preferences; random controls therefore also match fine frequency distributions.

**Actual reception.** For expert assignment \(e(x_t)\) within a split, \(q_{i,e}=P(A_i=1\mid e(x_t)=e)\) is the feature hit frequency inside the expert, while \(r_{i,e}=P(e(x_t)=e\mid A_i=1)\) is the reception rate when the feature is active. All features, including out-of-group frequent features, enter these counts. Empty experts have q = NA; active features with zero reception retain r = 0. Within the same split and with estimable denominators,

\[
q_{i,e}=\frac{p_i(\mathrm{split})\,r_{i,e}}
{P_{\mathrm{split}}(e(x_t)=e)}.
\]

This conditional-probability identity explains the distinction between reception and within-expert frequency; it is not a new empirical mechanism.

## 5. Computational Realization

**Profiles and the token-frequency bridge:** the source proposes reusing the same 85,548 answer-prediction positions from current Tulu SFT TRAIN. First verify position-wise alignment of raw h, shared z, sample IDs, targets, and causal positions. Flag first-answer prediction positions that may still lie at the end of the prompt. Freeze p, f, bands, and calibration means on TRAIN. Retain current/target IDs, dialogue, source, answer position, band M/R, total contribution, nonzero feature count, and U contribution. Targets and future text never enter routing. This stage makes profiles traceable to positions without assigning semantic labels first.

**Bridge checks:** compare low-frequency share against current-ID rarity and examine contextual variation within the same ID. Predict review shares with per-ID TRAIN means and compare errors against a TRAIN global-mean predictor; residual error is not automatically semantic. Estimate descriptive uncertainty by dialogue rather than independent positions. Distinguish random text from high/low-share examples, retain visible prefixes, and use right context only for reading.

**Relation review:** recompute current-TRAIN relations within bands and freeze candidate subgroups before comparing review co-occurrence and actual input composition against random groups matched for size and fine frequency. Old DCLM relations are historical references only. Clustering, banding, randomization, reliability diagnostics, complexity, and stability checks belong to the Protocol. Proposed defaults are not approved and this Anchor introduces no alternative execution settings.

**Actual routing:** compare crossed raw/calibrated and relation/random conditions while retaining the same inputs, bands, expert count, and raw within-band selection. Report q, r, enrichment, load, zero reception, unknown frequencies, fallback, and random/high-contribution text. Use normalized contribution vectors restricted to the selected band to inspect composition consistency; this measures neither semantic sameness nor compatible learning.

These are planned analyses. Subsequent learning requires separately frozen common budgets, paired initialization, supervision targets, optimizer, an independent DEV procedure, and a fresh held-out set unused for selection. It must not start automatically or present the best epoch chosen from an already viewed EVAL as formal success.

## 6. Minimal Falsification Tests

| Judgment | Comparison and observable | Supporting, non-supporting, and insufficient branches |
|---|---|---|
| H1's positive token-frequency bridge | Review Spearman between \(s_t=-\log_{10}f(v_t)\) and low-frequency share \(R_1\), supplemented by ID-equal weighting and within-ID variation; unseen TRAIN IDs reported separately | Under the Protocol's exploratory dialogue intervals, entirely positive supports the proposed direction; entirely negative contradicts it; crossing zero is unresolved. Report magnitude and do not label a tiny correlation a strong bridge. |
| H2's incremental relation organization | Review within-group φ and received-input composition consistency for frozen φ groups relative to matched random groups | High TRAIN φ alone is not supporting evidence. No review improvement over random leaves additional evidence insufficient. Reproducible relations with nearly unchanged routing support structure without demonstrating that routing uses it. Inadequate estimable pairs, exchangeable members, or review support remain insufficient. |
| Realization of membership organization | Per-feature r, q, q/p enrichment, and random text, retaining common features and zero reception | Higher r with persistent q disparities indicates improved delivery only, not learning harm caused by common features. More consistent composition still does not adjudicate H3. |

Unexpected H1/H2 outcomes retain the original definitions; thresholds or scores are not changed to preserve a positive narrative. Positive association does not establish routing utility, while weak or reversed association does not establish that feature routing is always useless. H3 criteria, practical effect thresholds, and resources require a later learning protocol and are not invented here.

## 7. Current Evidence

**This round: NOT RUN.** This file extracts the proposed design from the source; it introduces no newly computed profiles, co-occurrences, routing, or learning results.

The source summarizes earlier records as follows: raw scoring left low-frequency memberships almost unreceived; calibration substantially improved reception, while complete expert inputs still mixed frequent information. Frozen last-layer sidecar experiments on DCLM and Tulu SFT did not improve held-out performance at their fixed endpoints. Some Tulu metrics improved early and then rebounded. The conservative interpretation is that reception and learning remain unconnected, with budget, overfitting, and update strength among unresolved rivals—not that frequency organization is proven useful or useless. Existing records are the [DCLM summary](../../../experiments/A15/15_21_activation_to_expert_learning/20261019_normalized_learning/summary.md) and [Tulu SFT summary](../../../experiments/A15/15_21_activation_to_expert_learning/20261019_tulu_sft/summary.md). Their different settings are not results for the current new rule.

The source also limits prior φ to binary activation correlation, not decoder contribution or learning assistance. Earlier observations and construction preferences do not establish a natural same-frequency law. Current DEV/EVAL have been viewed repeatedly; reuse is exploratory. Normalized-question deduplication does not establish document independence, paraphrase isolation, or absence of pretraining contamination.

## 8. Claim Boundary And Next Decision

The current state is a candidate mechanism and untested design. It does not establish profiles beyond token/format information, incremental relation value, learning benefits caused by low-frequency reception, or capacity gains. Experts receive complete h. Extracting joint z from 14 layers and computing routes incur costs; this is not a free online router deployable at arbitrary intermediate layers. Earlier-layer deployment requires a separate encoder that does not access later layers.

**The one next decision is whether the researcher confirms these definitions and the Protocol's unresolved choices and authorizes bounded, training-free A→B→C analysis.** Completion requires a clear raw primary rule and calibration control, band/subgroup settings, exploratory review status, and compute budget. After confirmation, resume with asset and position-alignment checks and then inspect profiles, relations, and actual reception in order. The current request to read and archive does not authorize that analysis; learning always requires separate confirmation.
