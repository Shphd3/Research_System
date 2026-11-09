# A15_27_04: Frequency, common-spectrum geometry and input response of domain-biased members

## 1. Problem Definition

The parent asks how a native CrossCoder responds to natural and controlled context. The researcher now asks whether math/biology document discriminators occupy uncommon frequency or spectral locations, and whether their response recurs at fixed tokens. Earlier small lists and target-token decompositions do not answer the full-dictionary question. This continuation uses the existing natural-language response Focus and one cache-only experiment, R10. Its decision is which of three proposed intuitions survives a whole-dictionary, document-level description. A supported contrast changes the descriptive account; a background-matched null weakens specificity; missing support remains insufficient. Researcher acceptance and question closure are Unknown.

## 2. Physical Priors

The researcher supplied three competing intuitions, not facts: discriminators could be uncommon or frequently reused with different intensity; their decoder directions could occupy different or similar spectral locations; their response could depend on context, vocabulary/format, or interaction. The dictionary is a fixed coordinate system, not a list of exclusive semantic atoms.

## 3. Falsifiable Hypotheses

H1: low-reference-frequency members are relatively enriched compared with the support-qualified pool. Its rival is frequent reuse plus intensity differences. H2: math/biology mean squared unit-decoder projections differ within one common real-representation spectrum beyond frequency/support-matched dictionary variation. Its rival is similar spectral position despite different responses. H3: fixed-target domain response recurs across wordings and exposed family splits. Its rival is lexical/suffix sensitivity or inadequate target coverage. Context/target effects can coexist.

## 4. Mathematical Model

For native shared activation \(z_f\), document response is \(r_{df}=160^{-1}\sum_{t=32}^{191}z_{dtf}\), including zeros. Raw discrimination is \(A_f=P(r_{mf}>r_{bf})+\tfrac12P(r_{mf}=r_{bf})\) over equally weighted discovery documents. Support requires five active discovery documents in either domain. Freeze all support-qualified members with \(\max(A_f,1-A_f)\ge .75\); retain the discovery sign and ID ordering. This is a stable-rank metric, not every nonlinear discriminator.

Let \(u_f=d_f/\|d_f\|\) be the final-block decoder direction in the same model coordinates as real residual-post representations. A single pooled discovery covariance, with one shared mean and equal domains/documents/positions, defines descending orthonormal PCs \(p_j\). Unit geometry is \(q_{fj}=(u_f^Tp_j)^2\), with full sum one. Group distribution is the member-equal mean \(Q_{gj}\). Spectral overlap is \(O=\sum_j\min(Q_{mj},Q_{bj})\). Aggregating PCs can only increase this overlap; identical squared distributions need not mean identical directions.

Actual group reconstruction is separately \(v_{dtg}=\sum_{f\in g}z_{dtf}d_f^{model}\). Project and square this summed vector, retaining cross terms. Its normalized energy is neither unit geometry nor explained variance of the full representation.

## 5. Computational Realization

Reuse A22 native joint fourteen-layer shared z, the original gate and zero-index block27 residual-post decoder. R04 contains120 natural documents, 30/10/20 per-domain discovery/development/exposed-heldout,160 fixed positions each; independent DCLM frequency uses65,536 positions. R04 true-h discovery cache supplies9,600 pooled positions in1024 dimensions. R07 reuses that exact basis, so it is not an independent robustness corpus. R08 contains384 fixed-target rows for48 family pairs, two wordings and two target-plus-suffix endings. R09 supplies the frozen TRAIN-RMS decoder scale. No new forwards or training are authorized.

## 6. Minimal Falsification Tests

One R10 experiment freezes the entire main set before further checks, then answers five figure questions: reference-frequency composition; unit geometry including PC1 split; spectral overlap versus conditional matched background and separate actual-use energies; corpus-token high-response composition; paired context and suffix response. Thresholds.70/.80 and Top16/64/128 are fixed sensitivity views, not replacement lists. Exposed-heldout AUC intervals and context tags are exploratory checks. Relative enrichment needs an eligible-pool comparison; special geometry needs a matched comparison; absent context activation is insufficient rather than token identity.

## 7. Current Evidence

R10 cache-supported analysis completed:16,384 dictionary coordinates→10,076 support-qualified→433 math/527 biology main members; exposed-heldout interval support357/431, with every selected ID retained. Classified high-reference-frequency proportions66.7%/54.3% exceed pool44.1%; low is not enriched. Mean first64 unit shares10.03%/11.52% arise mainly in PC2–64. Both full-main head means lie inside the A01 finer occurrence/support-matched reference; specificity depends on the frozen rank/threshold sensitivity. PCwise overlap.9493 (band.9686) is not above matched reference. Summed group-vector energies change with input domain. Recurrent fixed-target context occurs for33/21 members at >=1 ending;789 members remain zero across all controlled splits. Raw-h numerical checks establish the archived R04/R07 pooled basis is exactly the requested common spectrum, not independent robustness evidence. [R10 Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/summary.md) owns all values/limits. These are descriptive/exploratory measurements; researcher acceptance remains Unknown.

## 8. Claim Boundary And Next Decision

Allowed claims describe frequency, geometry, reconstruction energy and measured input association in these panels. They do not establish exclusive knowledge, identical functions, causal importance, learning interference or routing utility. Pure target-only replacement is missing; preserve that gap and write a minimal NOT RUN proposal without executing it. Finish all available statistics, tables, five figure groups and reproducible records, then stop for the researcher's assessment. [R10 Protocol](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/protocol.md) owns exact operations.
