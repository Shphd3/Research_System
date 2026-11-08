派生阅读副本；原件位置：`Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_12_distance_composition_anchor.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_12_distance_composition_anchor.md)；研究修改仍回到原件。

---

# Distance-associated changes in answer-position SAE combinations

## 1. Problem Definition

When the same object fact is16,64or128tokens from the answer position, how do the members, amplitudes and fact contrasts of its SAE representation change? This inherits the natural-language context-response question, using R19's behaviorally usable object-fact task. R19 established member overlap and six-member contrast direction; it did not establish unchanged magnitude. The present uncertainty is whether turnover accompanies retained or weaker fact differences, and how filler/position covariation limits attribution. The user's purpose is descriptive discrimination among these possibilities, not a mechanism presuming degradation. Support narrows the observed pattern; non-support rules out that operational claim only; insufficient evidence preserves uncertainty. Competition-error mechanisms, interventions and training are excluded.

## 2. Physical Priors

A nonnegative Top32 code has a fixed active budget: member changes, common-member strength changes and full-code scale are different observables. Unit normalization removes scale. Absolute evidence index e, answer index p and gap d obey d=p−e−1, so all three cannot vary independently. These are mathematical/implementation constraints; no causal memory-loss prior is assumed.

## 3. Falsifiable Hypotheses

AI operationalizations under the explicit complete-study scope: H1 membership is approximately stable (mean16→128retained fraction at least0.90). H2 the full-code fact-contrast norm, relative to total code scale, remains within[0.8,1.25]of near (a local tolerance, not a universal ability standard). H3 that relative fact contrast decreases by at least20%. These are distinct from positive contrast-direction alignment. Live alternatives are substantial turnover with stable/increased fact contrast, generic activation gain, Top32ranking, filler variation and position covariation. No threshold is changed after results. New controls are supporting checks of attribution, not new gates selected for passing.

## 4. Mathematical Model

For one dictionary, z is the30000-dimensional post-ReLU/Top32 vector at the last answer-prefix token; inactive coordinates equal observed post-truncation zero. Let S be its32positive indices. For factA/B at distance d, delta_d=z_A,d−z_B,d. Separate its raw norm from relative separation s_d=||delta_d||/sqrt((||z_A,d||²+||z_B,d||²)/2). The primary magnitude change is log(s_128/s_16); contrast direction is the cosine between deltas, reported independently. Common-member norm ratios and cosines distinguish amplitude from relative arrangement. Squared full coordinate change decomposes exactly into common-member changes plus entering amplitudes plus exiting amplitudes; it is not hidden-space energy or output attribution. Existing six IDs remain fixed with zeros and their strict-support sensitivity.

## 5. Computational Realization

Reuse144main R19prefixes (24families×2facts×3distances), their exact scores/h/Top32and the two native block27SAEs separately. Primary families are the old12heldout, already exposed; discovery12is exploratory, not refit. Re-encode saved h without an LM forward to verify Top32and inspect pre-truncation ReLU responses. Complete30000-coordinate post-Top32 is primary; untruncated responses and decoder/hidden differences are truncation/reconstruction diagnostics, not a replacement dictionary.

Execute228new forward conditions in the same frozen model:72reverse-order weather prefixes,72length-matched office-filler prefixes,48fixed-evidence-near/mid prefixes,36uniform+64position-index shifts in six template-covering families. Fixed-e128reuses24old far rows. Reverse/content keep p319/e302,254,190; fixed-e keeps e190and p207,255,319; uniform position shifts keep identical tokens/visible positions and change only supplied position IDs. The latter isolates an encoding-coordinate shift, not added visible context. New controls remain limited by filler amount/order and cannot identify a pure universal distance effect.

## 6. Minimal Falsification Tests

All12heldout families remain in full-code analyses; do not select by six-member support or behavior. Aggregate facts within family, then bootstrap8192families and report exact paired sign-swap tests with a six-test Holm family (two dictionaries×H1–H3). H1passes only with lower95%interval≥0.9and corrected p≤.05; an upper interval<0.9does not support it. H2requires a95%ratio interval entirely within[.8,1.25]and corrected two-boundary equivalence test; an interval wholly outside does not support it. H3requires upper ratio interval<.8and corrected boundary test; lower>.8does not support a20%decline. Otherwise insufficient. Preserve direction/raw norms, all three distance pairs and template sensitivities. Frequency changes use group base counts, at-risk exits, rank-matched exits and reference/discovery-weighted entry opportunities. No arbitrary group size becomes semantic importance.

## 7. Current Evidence

R20completed2026-11-04T16:02:55.941033+08:00. [Summary](../../../../experiments/A15/15_27_natural_language_feature_response/R20_20261104_distance_composition/summary.md) owns the bounded interpretation; all12old heldoutfamilies retained.16→128meancommon24.79/32and27.92/32;normalizedfact-separationratios1.0803and1.1989. H1≥90%retentionnot supportedboth;H2toleranceequivalence supportedAttention,MLPinsufficientbecauseuppergrowthexceeds1.25;H3≥20%attenuationnot supportedboth. All228controlscompletedwithoutweightchanges;reverse/content/fixed-emeanratiosremainabove1. F28reverse16isaretainedfailure;alloriginalmainpairedrates12/12. Fact-differencereconstructionerrors≈.994/.984limitsemanticinformationclaims. [Detailed](../../../../experiments/A15/15_27_natural_language_feature_response/R20_20261104_distance_composition/detailed.md) recordsmetadataA1/quality/lineage. ScientificacceptanceUnknown;nofunctionalintervention/training.


Template sensitivity qualifies this result: aggregating to six template means and enumerating64sign patterns gives Attention H2raw p0.03125,Holm p0.1875,insufficient; MLP is also insufficient. Family-primary verdicts stay unchanged, but equivalence is not confirmed across independent templates.

## 8. Claim Boundary And Next Decision

This round can describe within-family code changes in this task, model, hooks and16–128gap window, and test robustness to declared filler/position changes. It cannot establish a causal distance mechanism, semantic atom identity, general long-context law, intervention utility or router-training value. Old heldout is exposed and shared templates limit extrapolation. Deliver all raw pairs, four rule-chosen cases/counterexamples, main/audit figures and10/30second explanations, then stop for researcher review. The one next decision is which remaining explanation most needs a distinguishing check; no follow-up is launched automatically.
