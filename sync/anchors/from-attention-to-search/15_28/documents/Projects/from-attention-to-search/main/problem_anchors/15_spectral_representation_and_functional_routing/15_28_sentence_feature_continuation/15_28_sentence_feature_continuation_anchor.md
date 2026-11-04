派生阅读副本；原件位置：`Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_28_sentence_feature_continuation/15_28_sentence_feature_continuation_anchor.md`。
[精确原始文件](../../../../../../../sources/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_28_sentence_feature_continuation/15_28_sentence_feature_continuation_anchor.md)；研究修改仍回到原件。

---

# A15_28: Within-sentence feature persistence and existing-graph association

## 1. Problem Definition

Within one math or biology sentence, do features at an earlier token recur at a
later token, or connect to different later active features through the existing
graph, beyond comparable unrelated positions? The researcher fixed this question
on 2026-10-28. The [Focus](../../../focus/focus_sentence_feature_continuation.md)
owns that activated question; the [Protocol](../../../experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/protocol.md)
contains proposed exact analysis rules.

This independent A15 question studies coordinate continuity across token
positions. A15_27 studied responses at a fixed target under changed prefixes;
its findings and scientific states are preserved. Reusing its texts does not
make its domain readout, attention association, or semantic-response results
evidence for this new estimand. The immediate uncertainty is whether apparent
continuity exceeds frequency, repetition, shared domain, and active-set size.

Positive excess would establish a bounded sequence association worth inspecting.
Nonpositive contrasts would weaken that measurement, while inadequate matches or
wide intervals leave it unresolved. The later researcher decision is whether a
surviving pattern warrants a separate context intervention. This round uses
existing caches only: no training, clustering, new large forwards, or intervention.

## 2. Physical Priors

1. **Researcher hypothesis:** features can recur or change along a sentence.
   No assumption requires a later token to contain every earlier feature.
2. **Measurement assumption:** a native positive dictionary activation defines
   an active coordinate for that dictionary and hook. A missing coordinate is
   not equivalent to missing information in the full model representation.
3. **Comparison assumption:** same-domain unrelated documents matched on token
   identity, position, and activity are useful backgrounds. They do not guarantee
   exchangeability of syntax, topic, or semantic role. Residual confounding remains.

## 3. Falsifiable Hypotheses

**H1:** the fraction of an earlier active set still active later in the same
sentence exceeds the matched unrelated-position fraction.

**H2:** when an earlier feature is no longer active, it connects by a non-self
edge in the old graph to later active features more often than controls. Forward
and reverse graph directions are separate. The precise lost-feature denominator
is an **AI_PROPOSAL** formalization of the researcher's “even if no longer present”
clause; all-source non-self coverage is retained beside it.

The strongest rivals are high feature prevalence, repeated token IDs, common
domain/topic, unequal active-set sizes, and graph hubs. High-frequency-only or
same-token-only excess favors those narrower accounts. Identity persistence and
graph association can coexist; neither implies causal transmission.

## 4. Mathematical Model

Fix one dictionary with coordinate universe \(\mathcal F\). At token position \(i\), native activation is \(z_{if}\)
for feature \(f\), and its active set is \(A_i=\{f:z_{if}>0\}\).
For two positions \(i<j\) in the same complete sentence, distance is
\(d=j-i\), and \(E\) is the existing directed, non-self edge set.

The readout is the fraction of source coordinates with a specified continuation:

\[
C_R(B,A_j)=\frac{1}{|B|}\sum_{f\in B}
\mathbf{1}\{\exists g\in A_j:(f,g)\in R\}.
\]

This is a fraction from 0 to 1, computed separately for each position pair.
For H1, \(B=A_i\) and \(R=\{(f,f):f\in\mathcal F\}\), giving
\(S_{ij}=|A_i\cap A_j|/|A_i|\). For the proposed H2 replacement readout,
\(B=A_i\setminus A_j\), and \(R=E\) or its reversed edges. Also report
\(C_E(A_i,A_j)\) and its reverse as all-source association; these can overlap
with persistence. Empty denominators are NA, not zero. Source frequency strata
restrict \(B\) before division; no union of all earlier positions is used.

For each domain, dictionary, frequency stratum, distance, and token-ID status,
the decisive quantity is the document-weighted real-minus-matched contrast
\(\Delta_R\). Its exact weighting, matching coverage and document dependence
are fixed in the Protocol before computing outcomes. Both \(|A_i|\) and
\(|A_j|\), lost-source counts, and unmatched counts accompany every contrast.
The equation is a descriptive observable, not a model of information transport.

The old CrossCoder arrow has a different observation unit: at the **same token**,
\(A\to B\) passes support and asymmetric conditional-coactivation thresholds.
The old rule requires \(P(B\mid A)\ge0.8\), \(P(A\mid B)\le0.5\), and
\(n_B\ge2n_A\). It saves frequency-corrected diagnostics but does not require
them for admission. Applying these old edges between tokens creates this round's
new observable; the old probabilities are not cross-position transition probabilities.

## 5. Computational Realization

| Goal | How | Why |
|---|---|---|
| Preserve coordinate identity | Reuse E16 SAE at block-27 MLP input and A22 CrossCoder native shared z over 14 residual-post hooks, separately | Same feature numbers across dictionaries do not denote the same object; shared z is not an independent activation per layer |
| Define actual sentence pairs | Reuse 120 cached math/biology document prefixes; annotate and freeze complete sentence boundaries from text before outcomes | Same-document or attended endpoints are not automatically in the same sentence |
| Separate recurrence from association | Compute identity, lost-source graph coverage, and all-source graph coverage with complete source denominators | A self-loop or a repeated coordinate cannot supply evidence of replacement |
| Separate rivals | Match unrelated same-domain document positions; split same/different token IDs and whitespace/punctuation; use fixed DCLM frequency groups, margin-preserving incidence nulls and degree-preserving graph nulls | Prevalent coordinates, dense target sets and graph hubs can make coverage high without sentence specificity |
| Make cases interpretable | Show all sentence tokens, a fixed feature selection rule, omitted-feature counts, two actual examples and a counterexample | A few appealing heatmaps cannot establish the aggregate hypothesis |

The current audit establishes input feasibility for testing H1 in both
dictionaries and old-graph H2 in CrossCoder. SAE H2 is `INCOMPATIBLE_INTERFACE_UNQUALIFIED`: its historical graph
counts selected indices under an older precision/filtering interface, whereas
this cache uses native positive FP32 activations. It is not silently substituted
with the CrossCoder graph or a newly built SAE graph. Details and identities are
in the [preflight](../../../experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/preflight.md).

*Towards Monosemanticity* offers a useful sequence-level motivation: its
[finite-state-automata discussion](https://transformer-circuits.pub/2023/monosemantic-features/index.html#phenomenology-fsa)
describes recurring and alternating features. **Adaptation:** inspect recurrence
and changes along complete sentences. **Boundary:** the paper's feature-to-logit,
next-token, next-feature account is not tested by our cached coactivation readout.
Its feature splitting across dictionary widths is also not a definition of
within-sentence semantic upgrading. The [literature note](../../../experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/literature_methods.md)
distinguishes the paper's evidence from these proposed analysis choices.

## 6. Minimal Falsification Tests

One cached experiment separates the two hypotheses without adding a learning
task. H1 compares identity persistence with matched unrelated positions. H2
compares non-self old-edge coverage, in both directions, after removing retained
source coordinates from its replacement denominator. Fixed-margin and graph
degree nulls test whether prevalence, activity, or hub structure suffice.

**AI_PROPOSAL decision rule:** a positive real-minus-control interval after
registered multiplicity handling is supporting evidence only for its qualified
stratum; require compatible null diagnostics before attributing excess beyond
the stated rivals. An interval wholly at or below zero is non-supporting for
positive excess; an interval crossing zero, failed matching, failed null mixing,
or unavailable graph is insufficient. Zero is the directional null, not a
power-justified useful-effect threshold. No minimum scientifically useful effect
has been specified, so statistical separation alone does not decide usefulness.
Exact parameters and the review ledger belong to the Protocol, which remains a draft.

## 7. Current Evidence

The following is the initial design-preflight snapshot; the execution update at the end of this section links current results.

The two named conversations and current owners were inspected. They establish
the provenance and prior scope summarized in the [source audit](../../../experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/provenance/conversation_sources.md).
They do not already answer H1/H2.

The current asset check finds 120 documents × 192 cached tokens = 23,040 positions,
with native CSR activations for both dictionaries. SAE has 32 active coordinates
per position; CrossCoder ranges from 29 to 637. Independent DCLM frequency
reference data contain 65,536 positions from 254 document groups. The existing
CrossCoder validation-passed raw graph has 206,136 edges; its maximum in-degree is
15,439, making hub control consequential. Its absence of cycles follows from the
frequency-doubling rule, not independently established semantic hierarchy.

Sentence IDs are not yet annotated. The reused texts were previously exposed,
so no fresh confirmation claim is available. **New H1/H2 measurements, three
result figure types, and the new two-example/one-counterexample selection are
NOT RUN.** This is the requested design-and-feasibility endpoint.

**Execution update (2026-10-28):** The NOT RUN statement above is the design-stage snapshot, superseded here for execution status only. Both native H1 branches, CC H2, frozen controls, nulls and three figure types are complete; SAE H2 remains separately blocked. [Summary](../../../experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/summary.md) and [Detailed](../../../experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/detailed.md) own the result facts and bounded AI reading. Completion does not supply human mechanism acceptance or question closure.

## 8. Claim Boundary And Next Decision

Excess identity supports sentence-local coordinate continuity. Excess old-edge
coverage without identity is compatible with associated-coordinate replacement.
Effects limited to high-frequency or repeated-token conditions favor public
patterns or lexical continuity. Disappearance after background adjustment fails
to support extra association under this measurement; it does not show forgetting.
Subset effects remain subset effects.

This round cannot establish complete preservation of earlier information,
causal transfer, semantic hierarchy, why clusters form, or utility for experts.
Mechanism acceptance and closure remain `Unknown`.

**One next decision:** after the three figure types, actual cases, complete
coverage tables and uncertainty are available, the researcher decides whether a
specific pattern warrants a separate context-replacement intervention. Resume
by reviewing the exact Protocol choices, freezing text-only boundaries, and
then running the authorized bounded cache analysis. A15_27 remains unchanged.
