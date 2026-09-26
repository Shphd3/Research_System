# Sidecar activation distributions across natural-text domains

[Chinese result](summary_cn.md) · [Detailed evidence](detailed.md) · [Results](/data/250010109/MoE_Router/experiments/20260925_sae_domain_activation/analysis/results.json)

Completed user-requested bounded descriptive readout. AI interpretation; no researcher-owned scientific-state transition.

## 1. Purpose

Test reproducible domain-conditioned activation distributions of the existing frozen sidecar SAE, separately from answer-letter adaptation or interference prediction.

## 2. Hypothesis

Same-domain independent record batches should have more similar activation profiles than different domains, and fit-domain prototypes should identify heldout-batch domains. Lexical/style/source distinctions remain the strongest rival to a semantic interpretation.

## 3. Analysis method

- Reuse exact21B S7, final-block native attention-output observer, width30,000 and top32. No parameter or activity-counter update.
- Four academic domains, two subfields each;64 records/subfield/batch across existing fit/test source splits. Total1,024 records, each256 content tokens. Fixed hash selection; historical corpus, not fresh confirmation.
- Primary positive firing frequencies pooled within documents; normalized domain profiles compared by total variation. Fit-only cosine prototypes classify the512 test records. Use500 subfield-stratified test-record bootstrap draws,199 training-label permutations, and separate magnitude/last-position/lexical controls.

## 4. Conclusion

Mean same-domain cross-batch distance0.131919 versus cross-domain0.393723 (2.98×). Body-frequency domain classification458/512=89.45%,95% conditional record-bootstrap interval[86.72%,91.80%], versus25% chance; permutation p=0.005. All40 fit-selected domain-enriched features retain their enrichment sign in the second batch, descriptively. This supports stable domain-conditioned differences in these fixed panels.

Magnitude and last-position classification are89.84% and80.66%, separately. A same-text unigram lexical reference reaches91.80% [89.45%,93.95%]; no beyond-lexical semantic advantage or statistically significant model ranking is established. No feature-level semantic labels or same-data SAE-to-interference predictor were measured.

The fixed32 positive features per token is architectural, not a domain effect. Record IDs are not paper IDs; existing corpus exposure and one checkpoint limit generalization. TV bootstrap percentile ranges have nonlinear finite-panel bias and are not promoted to population confidence intervals; see statistical_audit.json. No figures or additional remote jobs.

One AI-proposed next decision: pair activation distance with actual cross-group update consequences on the same natural-text units, controlling lexical prediction. If SAE adds no predictive value beyond lexical features, stop using domain separability as justification for parameter partitioning. Not executed here.

## Direct distribution views requested after the initial readout

![Feature frequencies across both batches](../../figures/sae_domain_feature_frequency.png)

Rows are dictionary feature IDs; columns are domains; cells are percentages of tokens with positive activation. Five features per domain are chosen by Batch1 enrichment only. The20 rows contain19 unique IDs (feature36 appears in two groups), illustrating shared rather than disjoint features. Batch2 is not used for selection. These selected views do not establish feature-level semantic labels or dictionary-wide exclusivity.

![All-feature cross-batch distance](../../figures/sae_domain_full_distribution_distance.png)

All30,000 dimensions contribute. Each same-domain diagonal is closer than all mismatched entries in its row. This is a direct profile comparison without a classifier or low-dimensional projection; lexical/style confounds remain.
