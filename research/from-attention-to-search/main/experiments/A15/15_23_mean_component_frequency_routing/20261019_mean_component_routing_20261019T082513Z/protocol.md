# Protocol: frozen mean-component and frequency-routing comparisons

English companion; the received [Chinese Protocol](protocol_cn.md) owns exact original wording. The separate execution authorization and pre-result [numerical amendment](numerical_amendment_01_cn.md) record implementation scope; no experimental parameter was tuned to rescue an outcome.

## 0. Scope and assets

Reuse the latest four-band/eight-slot list, positions and verified predecessor assets at frequency_contribution_bridge/20261019T025630Z. Create a new timestamped directory. Freeze Base, CrossCoder and experts; no new external job, training, deletion, commit or push. Necessary frozen forwards are allowed only on the original text positions. Missing dependencies block their branch only. Already used EVAL is an exposed review, not independent confirmation.

## 1. Objects and coordinates

At a current token and visible prefix, h is actual target-layer residual-post; z is the original gated nonnegative shared activation; d is its target-layer decoder vector, b the effective decoder bias and hhat=b+sum(z*d). Residual e=h−hhat; TRAIN hit fraction p=Pr(z>0); c=z*||d||. Restore preprocessing offsets/scales consistently. Joint14-layer encoding must not be mislabeled as current-layer-only encoding. Freeze B1…B4 and two subgroups each; TRAIN-zero U remains separate and in complete-input statistics.

## 2. Alignment and validation

Use original TRAIN and review positions, document/dialogue IDs and token order. Means use only TRAIN. Verify original h/z alignment, preprocessing, labels and sampled original assignments before affected comparisons. Preserve zero/empty outcomes rather than adjusting thresholds.

## 3. A: true mean decomposition

mu=E_TRAIN[h], m_i=E[z_i], v_b=sum(m_i*d_i), ebar=E[h−hhat]. Check mu=b+sum(v_b)+v_U+ebar. Report signed alpha=dot(v_b,mu)/||mu||², vector norms, cosines, feature-level direction distributions and actual m-weighted projections. RetainNA if mu is numerically zero. Explain m=p*E[z|z>0] as a statistical decomposition. Repeat on review against the fixed TRAIN direction and report mean-angle/length drift. Negative alpha or values above one are valid and must not be clipped into energy fractions.

## 4. B: fixed encoding, different scores

M_b=sum(c in band); S_bk=sum(c in subgroup). Freeze TRAIN means a_b and a_bk. R0 chooses argmax M then raw subgroup sum; R1 chooses argmax M/a then the same raw subgroup sum; R2 chooses argmax(M−a), retaining negatives, then the same raw subgroup sum. Supplementary R2b subtracts means at both stages. Do not divide by subgroup cardinality or standard deviation. Positive ratio denominators must be reliably estimated; zero denominators are unavailable, not replaced by tiny amplification. Ties use minimum ID. A common preregistered fallback handles zero-total inputs, separately reported and excluded from mechanism statistics. The raw winner/runner margin may be additively decomposed into baseline and deviation differences without causal attribution.

## 5. C: true target-layer mean subtraction and re-encoding

Freeze current TRAIN mu. Change only the target layer in the actual14-layer encoder input to h−mu; retain other layers, original preprocessing, dictionary, gate, lists and raw R0 routing. Do not refit frequency bands or means. Experts retain original h. Compare original/centered reconstruction in identical units: per-coordinate MSE, error norms, activation counts, zero rate, U activation, total contributions, paired changes and reconstruct-plus-mu equivalence. Degraded encoding confounds mechanism interpretation. If original joint inputs cannot be recovered, C isNOT RUN; never fake this by subtracting means from z or substituting reconstructed h.

## 6. Common outcomes

For each split/strategy report expert counts/shares/dialogues/empty slots; feature-wise owner receipt, macro and event-weighted summaries; complete original-feature exposure q; active counts/contribution shares/outside-group content;8×8 transitions and low-band flows; and same-input scores/winners. Unobserved features areNA; observed but unreceived arezero. Composition always uses original z/c, including C. TRAIN-center similarity is optional. Use1,000 complete-dialogue/block bootstrap draws for reported intervals, noting unverified original-document independence and any omitted cells.

## 7. Figures and cases

At mostfive main figures: signed mean components with feature directions; expert loads; low-feature receipt plus original-input composition; R0→R1/R2 transitions; one preselected complete natural text plus a few hash-selected changed/unchanged cases. Store PNG/PDF and sourceCSV. Figure labels stay brief; explain measurement, observation, interpretation and limits outside figures. Future two-token context is a reading aid only, never a router input. Preserve negative outcomes and sampling rules.

## 8. Conclusion and one next decision

Every claim has minimal evidence, scope and a rival. Mean alignment, score effects and learning utility are distinct. Propose only one next scoring hypothesis for a separately approved learning comparison, or explain why evidence is insufficient. Uniform load cannot select a winner by itself. No claim about training loss, knowledge acquisition, capacity or optimal new-knowledge assignment is permitted.

## 9. Stages, outputs and audit

First verify assets/formulas and reproduce routing. Then report A and R0/R1/R2 before all figures finish. Finally complete R2b, feasible C, cases and reports. Deliver Chinese one-page/full reports, configs/logs, all source tables, plotting code, five main figures and explicitNA/NOT RUN entries. Audit mean versus first singular direction; true versus reconstructed h; four bands versus eight slots; receipt versus suitability for learning; common information retained in original input; and absence of review-driven tuning. Stop before any new training.
