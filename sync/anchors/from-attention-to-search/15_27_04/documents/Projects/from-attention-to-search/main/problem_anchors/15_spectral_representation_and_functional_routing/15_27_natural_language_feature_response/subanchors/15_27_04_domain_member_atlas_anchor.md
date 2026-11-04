派生阅读副本；原件位置：`Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_04_domain_member_atlas_anchor.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_04_domain_member_atlas_anchor.md)；研究修改仍回到原件。

---

# A15_27_04: Frequency, common-spectrum geometry and input response of domain-biased members

## 1. Problem Definition

The parent asks how a native CrossCoder responds to natural and controlled context. The researcher now asks whether math/biology document discriminators occupy uncommon frequency or spectral locations, and whether their response recurs at fixed tokens. Earlier small lists and target-token decompositions do not answer the full-dictionary question. This continuation uses the existing natural-language response Focus and one cache-only experiment, R10. Its decision is which of three proposed intuitions survives a whole-dictionary, document-level description. A supported contrast changes the descriptive account; a background-matched null weakens specificity; missing support remains insufficient. Researcher acceptance and question closure are Unknown.

### R11 planning continuation

The researcher now requests a concrete math/biology/physics replication plan with the same model/dictionary and no training. This is a proposed R11continuation of the same descriptive question,not method implementation. Exact settings are AI_PROPOSAL;no execution or scientific acceptance is inferred.

## 2. Physical Priors

The researcher supplied three competing intuitions, not facts: discriminators could be uncommon or frequently reused with different intensity; their decoder directions could occupy different or similar spectral locations; their response could depend on context, vocabulary/format, or interaction. The dictionary is a fixed coordinate system, not a list of exclusive semantic atoms.

### R11 planning continuation

R11adds no assumption that a dictionary coordinate is a semantic atom. Shared mathematical expression/format and source signatures are rivals to categorical domain exclusivity.

## 3. Falsifiable Hypotheses

H1: low-reference-frequency members are relatively enriched compared with the support-qualified pool. Its rival is frequent reuse plus intensity differences. H2: math/biology mean squared unit-decoder projections differ within one common real-representation spectrum beyond frequency/support-matched dictionary variation. Its rival is similar spectral position despite different responses. H3: fixed-target domain response recurs across wordings and exposed family splits. Its rival is lexical/suffix sensitivity or inadequate target coverage. Context/target effects can coexist.

### R11 planning continuation

R11tests the account suggested by R10observations:main discriminators are more frequent than the pool,near-single-domain use is lower-frequency than the main set,and domain groups substantially overlap on the common spectrum relative to matched backgrounds. Physics can revise an old math-only label while math-vs-biology discrimination persists.

## 4. Mathematical Model

For native shared activation \(z_f\), document response is \(r_{df}=160^{-1}\sum_{t=32}^{191}z_{dtf}\), including zeros. Raw discrimination is \(A_f=P(r_{mf}>r_{bf})+\tfrac12P(r_{mf}=r_{bf})\) over equally weighted discovery documents. Support requires five active discovery documents in either domain. Freeze all support-qualified members with \(\max(A_f,1-A_f)\ge .75\); retain the discovery sign and ID ordering. This is a stable-rank metric, not every nonlinear discriminator.

Let \(u_f=d_f/\|d_f\|\) be the final-block decoder direction in the same model coordinates as real residual-post representations. A single pooled discovery covariance, with one shared mean and equal domains/documents/positions, defines descending orthonormal PCs \(p_j\). Unit geometry is \(q_{fj}=(u_f^Tp_j)^2\), with full sum one. Group distribution is the member-equal mean \(Q_{gj}\). Spectral overlap is \(O=\sum_j\min(Q_{mj},Q_{bj})\). Aggregating PCs can only increase this overlap; identical squared distributions need not mean identical directions.

Actual group reconstruction is separately \(v_{dtg}=\sum_{f\in g}z_{dtf}d_f^{model}\). Project and square this summed vector, retaining cross terms. Its normalized energy is neither unit geometry nor explained variance of the full representation.

### R11 planning continuation

For proposed R11keep zero-inclusive document responses.For bias d,define S as the minimum of its oriented document-AUCs against the other TWO domains;require>=5active discovery documents in d and S>=.75.Strict/near tags freeze on discovery.Fixed old16reference rates/decoder projections are constants,not new empirical replication.

## 5. Computational Realization

Reuse A22 native joint fourteen-layer shared z, the original gate and zero-index block27 residual-post decoder. R04 contains120 natural documents, 30/10/20 per-domain discovery/development/exposed-heldout,160 fixed positions each; independent DCLM frequency uses65,536 positions. R04 true-h discovery cache supplies9,600 pooled positions in1024 dimensions. R07 reuses that exact basis, so it is not an independent robustness corpus. R08 contains384 fixed-target rows for48 family pairs, two wordings and two target-plus-suffix endings. R09 supplies the frozen TRAIN-RMS decoder scale. No new forwards or training are authorized.

### R11 planning continuation

Propose150NEWdocument families/domain:60discovery,30development,60confirmation,192real tokens/160analysis positions.Confirmation separates30new documents on familiar platforms and30new platforms/domain.Reuse exact native A22/LM/gate.Primary basis stays R10;three-domain discovery PCA is secondary.Newmanifest/runtime NOT_BUILT/NOT_RUN.

## 6. Minimal Falsification Tests

One R10 experiment freezes the entire main set before further checks, then answers five figure questions: reference-frequency composition; unit geometry including PC1 split; spectral overlap versus conditional matched background and separate actual-use energies; corpus-token high-response composition; paired context and suffix response. Thresholds.70/.80 and Top16/64/128 are fixed sensitivity views, not replacement lists. Exposed-heldout AUC intervals and context tags are exploratory checks. Relative enrichment needs an eligible-pool comparison; special geometry needs a matched comparison; absent context activation is insufficient rather than token identity.

### R11 planning continuation

One proposed R11experiment:independent documents and old16transfer;full-dictionary symmetric discovery freeze;untouched confirmation/frequency/geometry/token checks.All old16remain,including physics-positive counterexamples.Proposed aggregate support requires high-share main>pool,near-use reference medians<main,and all spectral overlaps>=.80and within.05below matched medians,with prespecified uncertainty and heldout ranking/source guards.Margins are operational AI proposals.Negative directions narrow the relevant intuition;missing support stays insufficient.

## 7. Current Evidence

R10 cache-supported analysis completed:16,384 dictionary coordinates→10,076 support-qualified→433 math/527 biology main members; exposed-heldout interval support357/431, with every selected ID retained. Classified high-reference-frequency proportions66.7%/54.3% exceed pool44.1%; low is not enriched. Mean first64 unit shares10.03%/11.52% arise mainly in PC2–64. Both full-main head means lie inside the A01 finer occurrence/support-matched reference; specificity depends on the frozen rank/threshold sensitivity. PCwise overlap.9493 (band.9686) is not above matched reference. Summed group-vector energies change with input domain. Recurrent fixed-target context occurs for33/21 members at >=1 ending;789 members remain zero across all controlled splits. Raw-h numerical checks establish the archived R04/R07 pooled basis is exactly the requested common spectrum, not independent robustness evidence. [R10 Summary](../../../../experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/summary.md) owns all values/limits. These are descriptive/exploratory measurements; researcher acceptance remains Unknown.

### R11 planning continuation

R11results are NOT_RUN.The legacy7math/9biology all-cached-strict16are exposed descriptive members,not untouched confirmation.The[R11Protocol](../../../../../../../../UNAVAILABLE.md)proposes450documents and<=462futuresequence calls including checks;actual new calls0.R10results and its frozen Protocol stay unchanged.

### R11 A02actual evidence(superseding proposed-status snapshots above)

The researcher subsequently authorized completion of the original450-family three-domain plan. [A02result](../../../../experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/summary_A02.md)completes450new families/462forwards,no training. Main129/133/27,strictD1/0/0;primary per-PC overlaps.906/.825/.804. F1/Gintervals cross0,F2has insufficient near groups,mathnew-platform guardfails. All16legacy members have physicsHpositives,12recurrently. OldR10and originalProtocolbytes remain;these facts do not promote researcher mechanism acceptance.

### R13 feature presence/amplitude (2026-11-01)

The researcher activated occurrence/conditional-strength and bilateral-increment analysis. [R13actual result](../../../../experiments/A15/15_27_natural_language_feature_response/R13_feature_presence_amplitude_20261101/summary.md)uses exact R12targets/labels and86unique families,D16/V8per task,H37/17/18. Frozen independent-frequency groups,Dsupport and label-blind equal k3/4/10;all10seeds/dimensional references retained. Mainly-amplitude discrimination and unique bilateral complement are not established;mathfine has logloss-specific improvement without BAincrease. Known282/292/262are corrected by amplitude,297/090newly wrong. Source/position matching5/1/3pairs leaves lexical/format/source rivals. Joint14layerz,actual spectral reconstruction and residual remain distinct. New LMforwards/training/GPU0;scientific acceptance/mechanism Unknown.

R13whole-word audit additionally finds83observed standalone-the boundaries among86used documents,135as theorems prefix,and090/197window-end unknown. Exact token ID control holds,universal whole-word identity does not;future suffixes are not instantaneous explanations. Primary numerics unchanged,lexical/source boundaries qualified.

## 8. Claim Boundary And Next Decision

Allowed claims describe frequency, geometry, reconstruction energy and measured input association in these panels. They do not establish exclusive knowledge, identical functions, causal importance, learning interference or routing utility. Pure target-only replacement is missing; preserve that gap and write a minimal NOT RUN proposal without executing it. Finish all available statistics, tables, five figure groups and reproducible records, then stop for the researcher's assessment. [R10 Protocol](../../../../experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/protocol.md) owns exact operations.

### R11 planning continuation

The current planning decision is review of the complete R11data/selection/decision contract,then a separate determination of any execution scope.The[reading entry](../../../../experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/README.md)is DRAFT_NOT_EXECUTABLE.No automatic forwarding,training,methodprototype or closure follows.



### R11 A02delivery boundary

The authorized bounded experiment,five statistical figure groups and report are complete;see[A02Detailed](../../../../experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/detailed_A02.md). Earlier proposed next-execution wording is historical,superseded by A02authorization/results. PurelexicalB,human context labels,distance dependence and method benefit have no new confirming evidence. No further experiment is launched. Researcher mechanism judgment,closure and next-method choice remain Unknown.


### R13delivery and one next question

Measurements and AIinterpretations do not replace researcher acceptance. [Complete evidence](../../../../experiments/A15/15_27_natural_language_feature_response/R13_feature_presence_amplitude_20261101/detailed.md)retains initial Protocol,allconditions and failures. One AIsuggestion:do the increments generalize across new crossed-source/genre documents with sufficient positive low-frequency training support,beyond same-dimensional additions? No new panel,forward or expert design/training is launched.
