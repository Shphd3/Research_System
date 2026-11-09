# A15_25_01: Common representation components in Boolean compositions

## 1. Problem Definition

Does frozen Qwen3-0.6B use recurring representation components when predicting a Boolean composition, and can those components be transferred from a matched single-condition context while an operator-related component changes the prediction?

The [parent A15_25](../15_25_joint_feature_graph_anchor_cn.md) prepares inspectable feature relations before judging shared versus separate learning. This child tests one prerequisite: whether a candidate statistical decomposition has a local predictive role. It does not run the parent's future learning comparison. On 2026-10-22 the researcher explicitly authorized this child Anchor, its Protocol, complete frozen-model analyses and interventions, and an integrated explanation without intermediate approval turns.

The example combines two familiar code operations: testing whether an integer is even and whether it exceeds a threshold. We compare each operation alone with their `and` and `or` compositions. Exact counts in the fixed reference corpus determine how much can be said about rarity. If neither composition has enough reference support, the experiment remains a composition/reuse test; it cannot establish a common-versus-rare composition contrast.

Support would justify retaining this decomposition as a candidate for later learning research. Failure of the controlled contrasts would weaken this particular decomposition. Poor native behavior, an invalid dictionary interface or inadequate frequency/control support yields insufficient evidence. The researcher retains the next scientific decision.

## 2. Physical Priors

AI operational hypothesis: recurring dictionary components may contribute to several contexts, while other components distinguish how two conditions are combined. Recurrence is measured occurrence, not evidence that a component implements parity, comparison or a reusable algorithm. The principal rival is generic format/output information or a nonspecific perturbation effect.

One formal assumption enables the edit: the saved CrossCoder's decoder and original centering/scaling define additive contributions in the final block's residual coordinates. The original reconstruction error must remain in every selective edit.

## 3. Falsifiable Hypotheses

The bounded hypothesis requires all three observations on held-out generated families: attenuating candidate recurring components hurts correct-token prediction more than matched random feature edits; importing those components from a same-answer atomic context preserves prediction within the registered equivalence margin; and transplanting operator-related components from the matched opposite operator shifts prediction toward the donor answer more than random feature transplants.

The rival predicts comparable effects for random edits, failed reuse, or shifts unrelated to the donor's condition. No single observation proves the conjunction. In particular, a harmless replacement without demonstrated dependence is not reuse evidence.

## 4. Mathematical Model

Let \(h\) be the 1024-dimensional final-block residual before final normalization, \(z\) the 16384 shared CrossCoder activations, \(D\) the final-layer decoder, \(s\) its saved TRAIN scale and \(\mu\) its saved TRAIN mean. Write \(h=\mu+s(b+zD)+e\), where \(e\) is the actual reconstruction error. An edit of feature set \(S\) is

\[
h'=h+s\sum_{f\in S}(z'_f-z_f)D_f.
\]

This identity retains every unedited feature, decoder bias, centering term and reconstruction error. Attenuation uses \(z'_f=(1-\alpha)z_f\); transfer uses the matched donor's \(z'_f\). The frozen final normalization and output head produce predictions. Correct-token negative log likelihood is measured in nats; a donor shift is the change in donor-answer versus recipient-answer logit difference. Decoder directions are not orthogonal and these interventions do not identify unique semantic parts.

## 5. Computational Realization

Use the registered original Qwen3-0.6B-Base and final 14-layer CrossCoder with its saved threshold, original normalization and 2/4/.../28 residual-post interfaces. Reuse the verified extraction and encoder implementations; adapt only data construction, component selection and intervention analysis. No parameter, optimizer or dictionary training occurs.

The natural-code sources motivate controlled Python REPL examples. A discovery family split selects up to 32 recurring components using fixed-reference frequency and recurrence across all four conditions. A disjoint set of up to 32 operator-related components is selected from `and`/`or` pairs with the same answer, reducing direct answer-label selection. Confirmation uses different generated families. These are shared-template families, not independent natural documents.

The [Protocol](../../../../experiments/A15/15_25_01_component_reuse/20261022/protocol.md) freezes the reference, exact rules, all controls and resource ceiling. Native model replay, same-context transfer, whole-vector transfer and matched random edits qualify interpretation before the final analysis.

## 6. Minimal Falsification Tests

Three primary quantities use family means and 5,000 family bootstrap resamples, with two-sided 98.333% intervals to conservatively account for three primary comparisons. Dependence requires the interval for attenuation harm minus random-edit harm to lie above zero. Reuse requires the whole interval for the same-answer atomic transfer's NLL change to lie within ±0.05 nats. Operator specificity requires the interval for donor-directed shift minus random transfer to lie above zero.

These numerical thresholds are AI operational choices under the researcher's authorization to complete the experiment autonomously, not established natural constants. Native atomic forced-choice accuracy must reach 80%, each composition 70%, and mean probability mass on the two Boolean answers 50%. At least eight candidate features per set and 90% successful matched controls are required for the joint interpretation. Otherwise report the completed measurements and the failed prerequisite. Descriptive findings remain usable within their own boundaries.

## 7. Current Evidence

At design registration: `NOT RUN`. The fixed Tulu TRAIN reference, model and dictionary are currently accessible. Parent statistical relations and previous frequency-routing results do not answer this intervention question. Results will be recorded in the owning Summary and Detailed files, without rewriting the registered Protocol.

## 8. Claim Boundary And Next Decision

This child can establish only intervention-defined dependence, transferability and operator-related prediction changes at the final residual interface of this frozen model on the specified controlled examples. It cannot establish pretraining exposure, semantic feature purity, a unique compositional mechanism, online routing feasibility, parameter sharing, reduced learning requirements or MoE utility.

One next decision remains researcher-owned: after reviewing the completed contrasts and their validity gates, retain or reject this candidate representation decomposition as an object for a separately designed learning experiment. Completion means the entire registered coverage ledger, including invalid and insufficient items, is reported and explained.
