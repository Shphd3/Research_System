# 22 October discussion: frequency routing, semantic combinations and rank-one intuition

[中文主讲入口](meeting_brief_moe_meeting_questions_cn.md) · [Day index](../README.md) · [Original experiment Summary](../../../Projects/from-attention-to-search/main/experiments/A15/15_18_context_relation_organization_use/first_flow_v3/summary.md)

**Current advance: ordinary MoE and load-balanced controls are complete and pass the saved-artifact audit. New natural-text analysis motivates particular rare/common combinations, while sparse matched support leaves their conflation by the old route unresolved. Section 10 contains the next question and speaking version.**

Sections 1–9 preserve the earlier meeting interpretation and constructed-relation evidence, concerning representation responses and behavior on a separate task. Following the researcher's current request, section 10 changes the immediate priority to semantic-atom combinations in natural text, deferring long/short-range labels and functional routing prediction. Candidate judgments do not change either line's formal Focus.

## 1. What the meeting asked, and what is already clear

The table groups themes from the four supplied documents. It paraphrases their discussion rather than quoting speakers verbatim; source passages appear at the end.

| Meeting question | Answer currently available | Question still open |
|---|---|---|
| **Does complex full computation rule out low-dimensional routing?** [Zhang Xin discussion 03:16–07:14, 11:40–14:49] | That inference does not follow. Selecting an expert and performing its computation have different information requirements. A result from an existing model in a particular basis does not determine the feasibility of a new training scheme. This is a logical distinction. | Whether a small contextual signal actually selects useful experts in a specified model was not tested here. |
| **How do multiple textual relations enter representations and jointly support prediction?** [Intuition 06:36–11:09, 17:04–18:26] | On these questions, the native model strongly preferred No, and external linear classifiers also achieved about one-half accuracy on new questions. We have not established an internal account of reliable relation solving. | Which components carry relations, where necessary composition occurs, and how the model uses them. |
| **Do distance and composition change internal organization?** [Intuition 05:04–07:48; operationalized here as necessary relation count and evidence distance] | Matched near/far vectors differ. The final-layer variance concentration is similar descriptively across the four conditions. | The effect of distance alone, separation of specific directions, and which changes affect correct relation use. |
| **Can a few shared directions preserve the required function?** [Intuition 02:20–06:36] | The final-layer top 16/64 TRAIN directions retain 47.81%/71.87% of centered TEST variation. A small set retains a substantial fraction of numerical variation. | Whether those directions suffice for correct answers or useful expert selection. Reconstruction percentages do not answer this. |
| **How are common components, frequency and semantic division of work related?** [Zhang Xin discussion 15:18–16:41; Intuition 22:00–23:24] | The existing CrossCoder reconstructs part of these representations and connects activations to actual texts. Feature occurrence on the measurement panel and relation exposure during model training are different quantities. | Whether the first principal direction represents shared grammar, and how training frequency shapes these directions. |
| **How does the old frequency-routing result constrain retaining common computation while learning the remainder?** [Reporting guidance 04:11–05:10; meeting recap section 4] | The routing signal, retained path and learning schedule must be compared. The old scheme's outcome does not automatically settle the new scheme's outcome or its cause. | An executable definition of common and the benefit of differentiated learning rates. The main model was not updated to test either. |

**The useful update for this meeting is that shared representation structure and useful computational division are now separate, assessable claims. The data answer part of the first claim and expose a concrete unresolved link in relation solving.**

## 2. A real question makes the research object concrete

The target question is: **Is Sam located to the left of Bob?**

| Necessary facts from an actual input, paraphrased | Correct answer | Comparison |
|---|---|---|
| Sam is left of Bob. | Yes | One relation suffices; row 1408. |
| Bob is left of Sam. | No | Reverse the relation while keeping the names and question; row 1412. |
| Carol is right of Sam; Carol is left of Mary; Bob is right of Mary. | Yes | Compose Sam→Carol→Mary→Bob; row 1416. |

Each full input contains 12 facts. The table extracts only the necessary facts. An external solver checked the answer and verified that removing any necessary relation makes that answer undetermined. The distance comparison keeps the same fact set and moves the necessary evidence: rows 1408 and 1410 have distances of 33 and 103 tokens. TEST means are approximately 33–36 tokens near and 104–106 tokens far.

The model is fixed Qwen3-0.6B Base. We compare the 1024-dimensional block output at the position immediately before the answer, and separately the block's modification, output minus input. There are 128 families and 2048 variants, with 64/24/40 TRAIN/DEV/TEST families. Each family includes shallow/deep, near/far, reversed and paraphrased variants. Entire families and template sets are held out. TRAIN is used to fit directions and external classifiers; main-model parameters stay fixed.

This instantiates the meeting's abstract question: **when the question still concerns Sam and Bob but necessary composition or evidence position changes, what does the model read, answer and change internally?** Here “far” means about one hundred tokens, and the scope is this constructed task. [Complete task, distance and split description](../../../Projects/from-attention-to-search/main/experiments/A15/15_18_context_relation_organization_use/first_flow_v3/detailed.md)

## 3. Does the model answer correctly when the relation reverses?

**The first finding is a strong No preference.** Row 1408 has correct answer Yes and row 1412 has correct answer No, but the model selects No for both. Showing only the second would confuse agreement with that preference with relation solving.

TEST has 320 Yes and 320 No labels. The model selects No 611 times, including 40 candidate ties assigned to No by the fixed rule. It answers 329/640 correctly, or 51.41%. Each cell below has 160 questions from the same 40 TEST families.

| Necessary relations | Near accuracy | Far accuracy | Both reversed variants correct: near / far |
|---|---:|---:|---:|
| One | 53.13% | 53.75% | 7.50% / 8.75% |
| Three | 48.13% | 50.63% | 2.50% / 1.25% |

Requiring both reversed variants to be correct checks whether the model answers each of the opposite facts correctly for the same entity pair. Its denominator is pairs, not individual questions.

We also measure the strength of the correct-answer preference. The **correct-answer margin** is log probability of the correct candidate minus log probability of the incorrect candidate, in nats; positive values favor the correct answer. Far minus near is −0.00547 [95% interval −0.02893, +0.01719] for one relation and +0.01875 [−0.00781, +0.04533] for three. Their difference, the prespecified composition-by-distance interaction, is +0.02422 [−0.01172, +0.06094]. These intervals cross zero: a stable distance effect or interaction is unresolved, rather than established absent. Paired resampling of 40 families captures question variation.

**Could an external classifier still read the correct answer from the representation?** A classifier of the same linear capacity was fitted at each layer to predict Yes/No. Across 28 layers, TEST accuracy is 48.28%–52.19%; classifiers fitted to shuffled TRAIN labels achieve 47.81%–52.34%. At the last layer, the real-label and shuffled-label values are 51.72% and 49.53%. Fits meet the numerical convergence requirement and fit TRAIN well, while performance on new families and templates remains as reported.

**The answer supplied by this part is that these inputs and readouts have not yielded reliable relation solving, either natively or through the fitted linear classifiers.** The following geometry therefore describes responses to these texts; it does not yet locate successful relation composition. Information could exist in forms these readouts do not capture, so its absence is not established. [Behavior and paired statistics](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E02/results.json) · [All-layer readouts](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E05/probes.json)

## 4. What does distance change in the representation?

**Moving and reordering evidence while preserving facts and answers changes the direction of the representation before the answer.** This directly compares 320 matched near/far pairs, all with aligned query positions.

Normalize each vector to length one, then measure the length of their difference. This removes overall magnitude differences: zero means identical directions and two means opposite directions. It is a vector distance, not a percentage of information lost.

| Network layer, execution index | One relation: near/far distance | Three relations: near/far distance |
|---|---:|---:|
| Layer 1, index 0 | 0.00833 | 0.00839 |
| Layer 14, index 13 | 0.07296 | 0.07026 |
| Layer 28, index 27 | 0.07711 | 0.07564 |

The final-layer 95% family intervals are [0.07456, 0.07965] and [0.07363, 0.07791]. Among these fixed early/middle/final examples, the middle and final differences are larger; all 28 layers are retained. Fact order changes together with distance, so the identified response is to **position and order changes**; distance alone is not isolated. This table is a supplementary aggregation of saved vectors. [Matched distance results](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E03/distance_pair_summary.json)

Does the far condition distribute variation over substantially more directions? Each cell uses 256 TRAIN examples. At the last layer, subtract its TRAIN mean and summarize variance concentration by **effective rank**: an equivalent direction count derived from the unevenness of directional strengths, not a count of neurons.

| Necessary relations | Near effective rank | Far effective rank | TEST variation retained by TRAIN top 16: near / far |
|---|---:|---:|---:|
| One | 30.42 | 31.08 | 48.27% / 47.82% |
| Three | 30.57 | 31.04 | 47.91% / 47.28% |

These descriptive values are close, without a large change in concentration for far or three-relation inputs. This is not an equivalence test. Equally concentrated sets can point in different directions, so the table does not determine whether they occupy the same subspace. [Condition spectra](../../../Projects/from-attention-to-search/main/experiments/A15/15_18_context_relation_organization_use/first_flow_v3/explanation_appendix.md) · [Condition TEST retention](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E04/condition_heldout_retention.json)

**This adds a concrete constraint to the meeting discussion: position/order changes reach the representation, but have not yet been linked to changes in correct relation solving.** The use of long-distance relations in deeper layers remains unresolved.

## 5. Do shared directions establish low-dimensional computation or routing?

The meeting separated **how much of the full vector must be retained** from **how much information must be read to select a computation**. A router could read a small signal to select an expert while that expert still receives the full vector. This defines a possible interface; task utility must establish whether the selection helps. No such router comparison occurred here.

This round first asked whether questions share some variation directions. Stack the vectors from 1024 TRAIN questions, subtract the TRAIN mean, fit principal directions with PCA, and freeze them for 640 unseen questions. The last-layer results are:

| Measured object | TEST variation retained by top 16 | TEST variation retained by top 64 |
|---|---:|---:|
| Representation at the block output | 47.81% | 71.87% |
| Block modification, output minus input | 47.52% | 72.16% |

Retained variation is the fraction of the centered numerical sum of squares. It answers **how much variation on new questions shared directions reconstruct**. It also provides a concrete comparison for the meeting intuition that the last layer only needs to add simple information: under this 16/64-dimensional comparison, retention for the block modification and block output is similar. The modification is not conspicuously easier to compress by this measure. That observation neither identifies its semantics nor determines what a retrained architecture would learn. [Full spectra and retention](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E04/spectra.json)

**We also replaced internal vectors to move toward a functional test.** At prespecified layer 28, retain the TRAIN mean and 16 principal directions, then continue the model. A random 16-dimensional space supplies an equal-dimensional control. The following conditions each use 80 fixed questions from 10 families and compare the intervention with its own same-batch native forward pass.

| Replacement | Correct-answer margin change, nats, 95% family interval | Relative numerical reconstruction error |
|---|---:|---:|
| Retain 16 principal directions | Approximately 0 [−0.02500, +0.02500] | 0.63755 |
| Retain 16 random directions | −0.00781 [−0.03438, +0.01875] | 0.98453 |

Principal directions reconstruct the vector substantially better, but margin changes do not establish preservation of reliable relation solving. Native answers already prefer No, and random directions also produce small margin changes. These errors concern the 80-question contemporaneous forward pass; they are not direct complements of the preceding 640-question retention fractions. The original table also records correct-answer negative log probability: mean changes are −0.04834/−0.06142 nats for principal/random directions. Both increase the correct candidate's probability without a clear accompanying improvement relative to the incorrect candidate. [All projection interventions and probability metrics](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E08/results.json)

A second intervention replaces the current representation with one from the opposite-relation question. At the answer position in layer 16, mean correct-answer margin change is −0.01406 nats [−0.03281, +0.00781]; at layer 28 it is −0.00625 [−0.05000, +0.03438], each on 80 questions. Writing the original vector back produces zero change. Strictly aligned controls preserving the relation while swapping irrelevant facts are also saved. Intervals still cross zero, and the whole vector carries entities and context as well, so a component specifically responsible for relations has not been located. [Replacement and controls](../../../Projects/from-attention-to-search/main/experiments/A15/15_18_context_relation_organization_use/first_flow_v3/detailed.md)

Cross-layer comparison adds a similarity observation. For the same 160 one-relation, near-distance questions, CKA between layers 14 and 15 is 0.995679: the pattern of which questions resemble one another is highly similar. This does not assign “word” or “sentence” functions to the layers. Methods and all-layer tables remain in Detailed.

**The definite answer here is that a few shared directions preserve substantial numerical variation. Whether they implement the required relation computation or support useful expert routing remains unverified.** These are the reconstruction, use and routing questions that the meeting distinguished.

## 6. Do text and feature analysis answer the common-information and frequency questions?

**Text analysis connects feature IDs to actual sentences, but has not independently established a relation feature.** The existing A22 CrossCoder jointly encodes and reconstructs 14 specified layers. Relative to its saved training mean, reconstruction FVE is 0.767563: squared reconstruction error is about 76.76% lower than that mean baseline. This qualifies numerical reconstruction; functional replay is recorded separately.

For example, feature 4300 activates on 85.16% of the task's TRAIN query positions. Its saved high-activation examples include rows 1537 and 1540, both asking whether Bob is left of Grace. Their correct answers are Yes and No, and activations are 0.05066 and 0.05017. The saved TRAIN row 0 has activation zero. **A frequently activated pattern can therefore occur in texts with opposite correct answers. These examples alone do not name it a “Yes relation” or shared grammar.** The examples explain saved observations rather than constituting a semantic test. [Feature selection, full texts and low-activation examples](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E07/crosscoder/representative_features.json)

This establishes a necessary distinction in the frequency discussion: **85.16% is activation occurrence on these inputs; the number of times a relation or composition appeared during model training is a different, unavailable quantity.** There was no high/low training-frequency comparison, so these activations do not identify how training frequency shaped representation space.

The question “is the largest direction common?” also requires a precise numerical object. Final-layer effective rank is 1.21 without mean subtraction and 33.86 after subtracting the mean. Including the average representation substantially changes concentration. The functional identity of that mean or first principal direction still needs independent evidence.

The separate single-layer SAE has reconstruction FVE −4.270350 relative to the task TRAIN mean: it reconstructs worse than that mean baseline. Its features are therefore not used to interpret this task. Its interface and mean baseline differ from the CrossCoder's, so the two values are not a dictionary ranking. [Dictionary qualification and functional replay](../../../Projects/from-attention-to-search/main/experiments/A15/15_18_context_relation_organization_use/first_flow_v3/detailed.md)

## 7. Which judgment should today's discussion advance?

The meeting required comparing the old scheme A and new idea B through their differences and the relevance of existing evidence.

| Object | Role in the discussion | Present evidence |
|---|---|---|
| Earlier frequency-based dispatch | Assign inputs using activation-frequency-related rules. A complete input sent to a “low-frequency expert” can still contain shared information. | This round neither reran that scheme nor identified its failure mechanism. |
| Low-dimensional contextual routing | Use a small contextual signal to select an expert, which may still process the full input. | Representation descriptions are available; actual expert selection and task utility have not been compared. |
| Retaining common computation with separate learning schedules | Preserve learned common computation and choose suitable learning arrangements for it and the remainder. Common is not assumed frozen. | The main model was fixed; the definition and learning benefit of the shared component are untested here. |

**The judgment this discussion can advance is that the measured geometry has not yet been connected to useful expert selection.** Between shared directions and improved selection, the missing link is functional evidence, not another definition of the 1024 numbers.

The specific next question should also use the completed natural-text expert-learning results. Section 10 makes that recommendation. Existing geometry remains a description of the model's input responses.

## 8. Two likely follow-up questions

**Why does this comparison address the meeting question more directly than a spectrum alone?**

The measurements attach to actual text operations: reverse a relation, move the same facts, or increase the necessary relation count, then inspect answers, vectors and intervention outcomes separately. Matched vocabulary, total facts, family splits and equal-dimensional random controls constrain particular alternatives. Distance still changes with order, and replacing a whole vector moves several types of content at once, so the response is not uniquely attributed to a relation mechanism.

**Why can we neither claim that low-dimensional routing works nor that it fails?**

No different routers selected different experts for a task-utility comparison. The experiment measured frozen representations and bounded replacements. Accurately reconstructing the whole vector still does not determine which expert is better. Conversely, failing to reconstruct the entire vector does not rule out preserving the information needed for expert selection. Feasibility must be tested against the routing task itself.

## 9. What the advisor means: an interpretation grounded in the documents

**My reading is that the advisor wants an account of how information divides the work of prediction, with experiments constraining that account.** The first three points below correspond to intelligible passages; the proposed research priority is my recommendation.

**First, the information that must be preserved and the information needed to select a computation are distinct.** [Zhang Xin discussion 11:40–12:38] The clearest passage allows experts themselves to be high-rank; the key is assigning inputs using context. Consider two hypothetical passages containing the Chinese word for “apple,” one about share prices and another about cutting fruit. Information distinguishing those contexts could be smaller than everything needed to predict their next words. The router reads the distinction while experts can receive full representations. This illustrates the idea; it does not identify actual finance or fruit experts.

**Second, “earlier details plus later relational composition” explains how rich full representations could coexist with specialization.** [Zhang Xin discussion 07:29–11:39; Intuition 09:51–11:09] A sentence's topic generally does not specify its exact next word; word identity, order and contextual relations must contribute together. Residual paths allow earlier information to remain available. This motivates measuring the existing representation separately from a block's modification. The account remains a hypothesis: it does not assign each layer to words, sentences or paragraphs, nor imply that deeper modifications must be low-rank. Zhang Xin's 10:52 challenge that his measurement may already concern the final-layer contribution remains relevant.

**Third, old results must impose explicit constraints on the new account.** [Reporting guidance 04:11–05:10; Intuition 18:31–20:55] Which observations does it explain? Which remain unexplained? What object differs between earlier frequency routing and the current division-of-work proposal? These questions permit support, revision or disagreement. Merely switching methods does not supply that judgment.

A proposed response is: **“I understand that the information for selecting a computation may be compressible without first compressing everything the expert processes. We previously used high-frequency membership as a proxy for shared computation, but have not qualified that proxy functionally. The present geometry establishes shared variation directions. The next question is whether those signals help select more useful computation.”** This is suggested speaking text, not a verbatim advisor quotation.

Retaining common computation and scheduling its learning require a separate answer: what computation is retained and how it should be updated. High frequency, the mean vector, the first principal direction and shared function have not been established equivalent. Shared information also does not automatically determine how shared parameters should be updated. Routing and this learning mechanism need distinct evidence to attribute any benefit.

## 10. Next question: does frequency routing conflate semantic combinations?

**Following the researcher's current request, the question is now about natural-text representation organization: does a rare semantic atom participate in reproducible combinations with particular common atoms, while old frequency routing assigns different combinations to the same place?** We adopt features as semantic building blocks as a working premise and defer long/short-range labels. This section continues the frequency-routing line. Sections 1–9 retain the separate constructed-relation evidence; populations and mechanisms are not pooled.

### Completed controls and checks

Ordinary MoE and load-balanced MoE completed both seeds on **four H100 Reserved GPUs**, each at 168 updates and 85,548 answer targets. The present audit checked paired initialization, frozen source/config, target alignment, counters, load-balancing calculations and saved metrics. It found no error requiring these four models to be rerun. The stale queued-status page and canceled-job producer metadata were corrected.

| Condition | Overall DEV NLL | NLL on the same rare-feature-active positions |
|---|---:|---:|
| Frozen Base | 1.248870 | 1.060492 |
| Ordinary MoE | 1.224985 | 1.054318 |
| MoE with load balance | 1.226042 | 1.055211 |
| Free frequency allocation T_F | 1.226137 | 1.061886 |
| Forced common partner T_H | 1.227138 | 1.062758 |

Values are two-seed means, lower being better; Base is fixed. Overall and rare-position denominators are 10,340 and 1,701 unique positions. They differ from feature-equal macro means. Ordinary MoE improves over Base; better load balance brings no extra DEV benefit here. T_H provides no stable rare-feature macro improvement over T_F. Learned and fixed models also differ in mixture weights and router parameters, so the comparison does not isolate a causal frequency effect. See [completed controls and audit](../../../Projects/from-attention-to-search/main/experiments/A15/15_24_frequency_composition_common_path/20261020_20261019T164834Z/standard_moe_controls_20261021/detailed.md).

The previous frozen diagnostic also ran. T_H retains the first expert and replaces the second, each with coefficient 1/2, while preserving the full Base path. There are 1,015 actual replacement positions. Its original-result replay gate failed, leaving common-residual benefit and partner-replacement cancellation unresolved. The present statistics do not bypass that gate. See [frozen diagnostic](../../../Projects/from-attention-to-search/main/experiments/A15/15_24_frequency_composition_common_path/20261020_20261019T164834Z/diagnostics_20261021/results.md).

### A representation-based explanation

**Frequency describes how often a component occurs, but does not determine its partners.** Equally rare atoms may participate in different computations; one common atom may be reused in many combinations. Group activation totals can compress different combinations into identical routing conditions.

A candidate explanation for unstable allocation benefit is therefore that different combinations share the same routing condition, providing poor separation for specialized learning. Both the combination differences and their learning consequences need evidence. Full representations still enter experts, so the router has not removed common information from their inputs. Coactivation also does not by itself demonstrate training interference. The old spectral pattern surviving feature-position shuffling already cautions that concentration alone does not identify combination structure.

We completed the first natural-text check. Original TRAIN-selected common partners were compared with frequency-matched random partners, then with matched positions in other dialogues. After matching current token and source, excess association is **+14.19 / +10.50 percentage points** in EVAL/DEV, across **551 / 150 rare-feature events**. On these exposed subsets, particular partner associations exceed the token/source controls used.

Also fixing the old expert pair leaves only **32 / 7 events**. Evidence that the old route actually conflates these combinations is therefore insufficient; positive point estimates do not settle it. See [definitions, support and contrary cases](../../../Projects/from-attention-to-search/main/research_notes/frequency_routing_rank_one_20261022_candidate_anchor.md).

A concrete pair asks for binary search versus constructing a dictionary from keys and values. Both are code examples, at a comma, with the same old route, but feature 12669 is active only at the former position. This grounds the question in actual operations without identifying a certified “binary-search atom.” The complete cases retain a negative Chrome-extension/travel comparison.

### Connecting the advisor's rank-one intuition

The four steps can be interpreted as arranging the initial spectrum, extracting threshold-reaching components, and learning the remainder orthogonally to extracted directions. Moving an exact component into the extracted part while subtracting it from the remainder preserves the sum and current output. This guarantees equivalence at transfer time. Whether future constrained updates retain ordinary training performance depends on the actual algorithm and objective. The senior's lossless result remains user-reported, without an inspectable implementation.

The key connection is that rank-one components are additive, while sparse MoE additionally decides which components can be omitted for an input. Two components producing (1,0) and (0,0.5) sum to (1,0.5); selecting only the first drops the second contribution. Flattening the spectrum or making parameter directions orthogonal does not make that contribution unnecessary.

The advisor's incompatibility intuition can therefore be narrowed to an explicit condition: if many components are jointly needed, they cannot be treated as interchangeable choices without a further check. Rank-one modules themselves can exist inside MoE. A future allocation should distinguish shared components from input-dependent combinations; sparse computation additionally needs small omitted terms or compensation through a retained path. See the [derivation and candidate objective](../../../Projects/from-attention-to-search/main/research_notes/frequency_routing_rank_one_20261022_candidate_anchor.md).

### Speaking version

“Our purpose is to find a better division of expert learning. I first audited the completed controls. Ordinary MoE and its load-balanced control have finished, and these checks found no training or saved-statistic error. Forcing a common expert gave no stable extra benefit, but that does not establish that common computation is harmful.

I am now examining relations among representation components. Taking features as semantic atoms, frequency tells us how often an atom appears, but not which other atoms form its current combination. My candidate explanation is that frequency totals assign different combinations to the same place and therefore may provide an unsuitable division. This has not yet been established as the performance cause.

The first natural-text check retains associations between rare atoms and particular common partners after matching the current token and source. However, too few comparable texts remain to decide whether the old allocation distinguished those combinations. The next question is which rare/common combinations recur across texts, and whether old frequency routing conflates them.

This connects to the rank-one intuition: extracting directions while retaining their sum preserves computation. Calling only a few directions additionally requires showing that omitted directions are dispensable for this input. We will study shared components and concrete combinations before deciding how to realize experts.”

The bilingual candidate Anchor remains an AI proposal. The next decision is whether preserving cross-frequency combination identity should guide the next allocation. Completion requires adequate matched natural texts and new-text evidence beyond token/source explanations and existing route distinctions. This paragraph records the state before the added-common extension; its completed results appear in section 11.

## 11. Completed extension: added common and hierarchy diagnosis

This requested extension preserves both routed experts and adds an always-on common, without parameter matching. Ordinary MoE and frequency routing each ran in a separate one-H100 Reserved job, with two paired seeds and eight models overall. Every model reached 168 updates and 85,548 valid targets. Saved states, paired initialization, counts and metric recomputation passed.

Paired low-feature macro NLL changes (negative is better) are +0.001619/−0.005810 for ordinary MoE and +0.002998/−0.000958 for frequency routing. Both families have opposing seed directions; all four overall DEV differences are slightly worse. TRAIN fit improves, while disabling common in trained models worsens overall prediction. Common contributes to the trained computation without establishing a stable net training gain. Global clipping also becomes much more frequent, leaving optimization as an unresolved rival.

Both low/high rosters span graph levels. Actual h1 input-event shares are 81.61%/81.57% for low E0/E1 and 83.54%/83.50% for high E6/E7. Every position contains h0, h1 and h2. A routing roster does not describe complete input composition, while similar level proportions do not establish identical features or computations. Mixture alone is not evidence of harmful interference. The fixed companion-count strata also show no monotonic common-benefit pattern.

The AI-proposed next question is which reproducible natural-text combinations share computation that can be retained, and which differences should be learned by later experts. Rank-one transfer can retain current computation before routing a residual, but frequency/depth labels do not establish the required grouping. This extension did not implement spectrum flattening, rank-one extraction or orthogonal training and does not reproduce the advisor's algorithm.

[Complete results and derivation](../../../Projects/from-attention-to-search/main/experiments/A15/15_24_frequency_composition_common_path/20261020_20261019T164834Z/shared_common_expert_20261022/summary.md) · [Execution protocol](../../../Projects/from-attention-to-search/main/experiments/A15/15_24_frequency_composition_common_path/20261020_20261019T164834Z/shared_common_expert_20261022/protocol.md)

## Sources and complete evidence

The four supplied meeting documents are preserved byte-for-byte in the day's `sources/` directory. They include conservative corrections and original transcription. No original audio was available; this brief uses intelligible discussion content without treating edited passages as verbatim speech. Emotional evaluations are excluded from the research argument.

- [1021_会议复盘与假设路线.txt](sources/1021_会议复盘与假设路线.txt): sections 3–6, meeting questions, H1–H4 and object distinctions.
- [1021_张鑫讨论_保守校对稿.txt](sources/1021_张鑫讨论_保守校对稿.txt): inference limits at 03:16–07:14, functional division at 07:29–11:39, routing at 11:40–14:49. The 10:52 challenge that the measurement may already concern the final layer's contribution is preserved.
- [1021_intuition讨论_保守校对稿.txt](sources/1021_intuition讨论_保守校对稿.txt): compression and multiscale composition at 02:20–11:09, representation at 17:04–18:26, explanatory models and common components at 18:31–23:24.
- [1021_汇报指导_保守校对稿.txt](sources/1021_汇报指导_保守校对稿.txt): coherent explanation versus testing at 00:41, and relevance of A/B evidence at 04:11–05:10.

The measurement owner for sections 1–9 is the project's `main/experiments/A15/15_18_context_relation_organization_use/first_flow_v3/`: [Summary](../../../Projects/from-attention-to-search/main/experiments/A15/15_18_context_relation_organization_use/first_flow_v3/summary.md) owns results, [Detailed](../../../Projects/from-attention-to-search/main/experiments/A15/15_18_context_relation_organization_use/first_flow_v3/detailed.md) owns methods and evidence lineage, and the [itemized appendix](../../../Projects/from-attention-to-search/main/experiments/A15/15_18_context_relation_organization_use/first_flow_v3/explanation_appendix.md) retains complete layer tables and cases. The [near/far supplement](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E03/distance_pair_summary.json) descriptively aggregates the same saved representations.

The [Focus](../../../Projects/from-attention-to-search/main/focus/focus_context_relation_organization_use.md) and [Anchor](../../../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_18_context_relation_organization_use/15_18_context_relation_organization_use_anchor.md) retain scientific ownership of the constructed task. Section 10 separately cites existing natural-text controls, current cache statistics and the candidate Anchor, without modifying those formal research objects. [The source manifest](source_manifest.json) records evidence and revision identities. Each line retains its exploratory boundary.
