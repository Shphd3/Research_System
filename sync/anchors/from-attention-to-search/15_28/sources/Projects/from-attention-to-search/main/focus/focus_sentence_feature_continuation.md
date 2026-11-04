# Do earlier sentence features persist, connect to later features, or disappear?

problem_key: `sentence_feature_continuation`
anchor_id: `15_28`
question_state: `USER_ACTIVATED`
design_state: `EXACT_PROTOCOL_CONFIRMED_FOR_BOUNDED_CACHE_ANALYSIS`
task_state: `CACHE_ANALYSIS_AND_LOCAL_DELIVERY_COMPLETE`
result_state: `EXPLORATORY_RESULTS_AVAILABLE_SAE_H2_BLOCKED`
human_result_judgment: `Unknown`
question_closure: `Unknown`

## Question, hypotheses, and boundary

The researcher activated this independent question on 2026-10-28: within one
sentence, do features active at an earlier token remain active at a later token,
or connect to later active features through the existing directed relation graph,
beyond frequency, repeated tokens, domain background, and active-set size?

H1 concerns the same coordinate. H2 concerns different coordinates connected by
an existing edge, especially when the earlier coordinate no longer activates.
Neither later position nor graph direction defines greater semantic abstraction.
SAE and CrossCoder use separate native coordinates. The existing A15_27 question
about fixed-target semantic responses retains its own design and results.

## Necessary comparison and available evidence

One cached analysis has three steps:

1. Bind texts, token positions, native dictionaries, DCLM frequency groups, and
   the old graph. Freeze sentence boundaries and matching rules before outcomes.
2. Compare within-sentence persistence and directed/reverse relation coverage
   with different-document positions in the same domain and fixed-margin nulls.
3. Read three figure types, two actual examples, and a counterexample together
   with coverage, document-level uncertainty, and missing branches.

The current preflight finds 120 math/biology documents with full token caches.
Both dictionaries support H1. The CrossCoder graph is compatible; the SAE graph
has an unqualified activation interface, so its H2 branch is blocked separately.
Those were the initial availability observations. Cached measurements are now complete and owned by Summary/Detailed. All texts have
already appeared in prior analyses; this round is exploratory reuse.

Completion of the later analysis requires a one-page factual answer, all three
figure types or explicit branch-specific unavailability, actual text examples,
tables, scripts, provenance, and the interpretation limits. Positive excess
supports bounded coordinate continuity or graph association. A result confined
to high-frequency/repeated-token strata favors those explanations. Disappearance
after controls weakens the measured extra sentence association. Missing matches, wide intervals, or incompatible graphs yield insufficient evidence, not forgetting.

## Researcher judgment and one next decision

The researcher specified the purpose, hypotheses, rivals, figures and cache-only boundary, then explicitly authorized execution using the discussed choices. The Protocol records that activation. Measurements, nulls and figures are complete with low coverage and branch-specific blocks retained. Summary interpretations are bounded AI readings, not researcher mechanism acceptance.

**One next decision:** after the bounded cached results, the researcher decides
whether a particular surviving pattern warrants a later context-replacement
intervention. This round neither performs nor pre-authorizes that intervention.
Resume discussion from the completed Summary; no intervention is automatically activated.

## Sources

[Anchor](../problem_anchors/15_spectral_representation_and_functional_routing/15_28_sentence_feature_continuation/15_28_sentence_feature_continuation_anchor.md)
· [Protocol](../experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/protocol.md)
· [Preparation record](../experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/preflight.md)
· [Reading entry](../experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/one_page_cn.md).
[Result Summary](../experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/summary.md) · [Full evidence](../experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/detailed.md). Human judgment and closure remain Unknown.
