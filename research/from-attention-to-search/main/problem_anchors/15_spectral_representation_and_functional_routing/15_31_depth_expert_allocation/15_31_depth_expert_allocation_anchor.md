# Expert capacity across depth and token frequency

## 1. Problem Definition

Does moving a fixed amount of expert capacity from shallow to deep layers improve the learning of relatively infrequent training tokens, while retaining general language modeling, under the same training exposure and closely matched computation? The researcher activated this independent question on 6 November 2026 within the MoE and long-tail learning direction. The decision is whether this allocation has enough measured potential to justify later entity/relation and representation tests.

Here, low frequency means a token type's count in the actual training exposure selected for this round. It is an operational proxy. Rare token types, rare entities or relations, rare sparse-autoencoder features, and semantic long-tail knowledge are distinct objects. This round changes the number of experts across depth; it holds residual width fixed. It does not test whether deep experts are independent memories.

A supporting result motivates further validation; a trade-off motivates assessing the cost; no measured advantage weakens this particular allocation; missing fairness or data support leaves the question unresolved. None closes the broader architecture question.

## 2. Physical Priors

**Researcher-endorsed hypothesis, not established fact:** the capacities needed for learning information may differ across depth, so allocating experts uniformly need not be optimal. The advisor's shallow/few-expert and deep/many-expert intuition motivates this hypothesis. The source is a corrected text transcript and meeting summary; no audio was supplied, and uncertain words remain uncertain.

**Experimental assumption:** equal expert counts in total, equal expert matrix shapes and equal top-k remove a major total-capacity and selected-capacity explanation. They do not equate dispatch cost, attention work, communication, throughput or elapsed time.

**Measurement assumption:** a training-only frequency statistic and a held-out token loss can measure this round's frequency-conditioned predictive behavior. They do not identify semantic knowledge or gradient signal-to-noise ratio.

## 3. Falsifiable Hypotheses

H1: at the frozen common token budget, deep-increasing capacity reduces low-frequency token negative log likelihood relative to the uniform model. H2: the improvement can be absent or can accompany worse high-frequency or overall loss. H3: routing loads and effective token receipts can change; this is measured rather than assumed to mediate H1.

The strongest live rival is that reallocating the same experts has no low-frequency advantage, or simply exchanges one frequency group's performance for another's. Unequal starting weights, data order, total parameters and actual compute are additional explanations to guard or quantify. Load changes alone cannot distinguish causal mediation.

## 4. Mathematical Model

A layer is a causal attention block followed by a top-k mixture of independent feed-forward experts. Let layer index be \(\ell\), expert count \(E_\ell\), residual width \(h\), expert intermediate width \(m\), and selected experts per token \(k\). Each bias-free SwiGLU expert has three matrices and \(3hm\) parameters. With unchanged attention, normalization, shared components and tied vocabulary interfaces, expert and router parameter counts depend on \(\sum_\ell E_\ell\). Therefore matching this sum exactly matches their total parameters. The expert matrices selected for one token have \(3hmkL\) parameters across \(L\) layers. All router rows are evaluated, rather than only the selected rows. These are accounting identities, not evidence of equal execution cost.

The decision quantity compares predictive losses on the same held-out positions. For frequency bucket \(b\), define

\[
\Delta_b=\frac{1}{N_b}\sum_{i\in b}\left[-\log p_B(y_i\mid x_{<i})+\log p_A(y_i\mid x_{<i})\right].
\]

Here A is uniform allocation, B is increasing allocation, \(N_b\) is the number of eligible target positions, and the unit is natural-log units per token. A negative \(\Delta_b\) favors B. Bucket membership uses training counts only. Unseen types receive a separate bucket. This estimand is token-weighted; any type-weighted diagnostic is separately labeled. It says nothing by itself about a token's meaning or a routing mechanism.

## 5. Computational Realization

1. **Verify accounting and a common start.** Reuse the inspected native ordinary-MoE source, adapt only per-layer expert counts and required bookkeeping, and enumerate actual parameter tensors. A uses eight experts at every layer. B uses `[6,6,6,8,8,10,10,10]`, splitting eight layers into stages of 3/2/3 layers. Both have 64 experts in total. Residual width 1024, expert width 1536 and top-2 remain fixed. Shared structures and shared expert identities receive aligned random weights; additional or removed experts use a frozen initialization mapping. This prevents accidentally testing a pretrained transplant or extra capacity.
2. **Freeze exposure and measurement.** Select the available verified training source, data order, deduplication and split contract; count the actual common exposure without test answers. Freeze buckets and inspect examples before final evaluation. Use an isolated output root and never mutate old checkpoints or corpus files. If document boundaries cannot be recovered, report the resulting limitation and do not label sequence-based intervals as document-level intervals.
3. **Train and compare.** Qualify both architectures on the requested four-H100 reserved allocation, freeze one jointly feasible configuration and budget, and complete both. Evaluate start, middle and endpoint at common tokens; report frequency-bucket and overall losses, uncertainty, measured compute, throughput, memory and routing loads. Initialization, checkpoint and data-order checks support interpretability; routing statistics remain observational.

The exact stages, choices and run evidence belong to [R01 Protocol](../../../experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/protocol.md). A width-varying shallow-narrow/deep-wide model is an untrained accounting sketch, not another tested arm.

## 6. Minimal Falsification Tests

The primary comparison is final low-frequency token NLL, B minus A. Report the paired difference and a two-sided 95% resampling interval using document units when verified, otherwise the declared available units with their dependence limitation. Zero is the no-difference reference, not an invented practical-benefit threshold. Intervals describe evaluation sampling; they do not replace multiple training seeds.

A negative difference with an interval below zero is evidence of potential in this measured proxy. Report high-frequency and overall differences alongside it, including any cost; do not select a favorable secondary metric to rescue the primary result. A nonnegative point estimate is no observed low-frequency advantage; an interval spanning zero leaves its sign uncertain. Missing runs, broken fairness, no eligible low-frequency coverage, or unverified exposure make the intended comparison insufficient. These branches guide the researcher's next decision rather than declare a universal mechanism.

## 7. Current Evidence

The inspected ordinary-MoE source has 8 layers, residual width 1024, SwiGLU width 1536, 8 experts per layer and top-2 routing. It has 507,988,992 unique trainable parameters, with 4,718,592 per expert; embeddings and output head share weights. The proposed pair has exactly equal expert and router parameter totals. The execution-side accounting will independently verify the adapted tensors and forwards before training.

The [meeting source](../../../experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/supporting_sources/meeting_1106_source.md) reports an advisor intuition and oral prior observations, without the complete controls, counts or numerical effects needed to establish this allocation's benefit. The distinct [R17_D1 SAE result](../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/summary.md) retains answer/readout dependence, missing two-baseline frequency advantages and insufficient content coverage. It does not establish a depth-to-frequency mechanism.

This pair's training and test result is **NOT RUN at registration**. Scientific acceptance and mechanism judgment are **Unknown**. Later execution facts and eligible observations belong to the round's result records.

### R01 execution facts (6 November 2026; researcher judgment pending)

A and B each completed 229,113,856 valid prediction targets, 874 updates and all initial/midpoint/endpoint evaluations. Both have 507,988,992 total/trainable parameters and 281,496,576 theoretical active parameters, with frozen shared exposure and order. Endpoint low-frequency NLL is A 12.694702 versus B 12.911912: B minus A is +0.217210, with paired document 95% interval [+0.125969,+0.300351]. Overall NLL is 4.289854 versus 4.304112. This measured pair shows no low-frequency advantage and worse overall NLL. Preserve the one-seed, 1,481-low-frequency-target, finite cyclic corpus and document-dependence limits. Semantic long-tail representation and causal routing mechanisms were not tested. Scientific acceptance, mechanism judgment and question closure remain Unknown.

The [R01 Summary](../../../experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/summary.md) and [Detailed](../../../experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/detailed.md) own exact procedure, eligibility and independent audit. The registration-time NOT RUN statement remains historical. This adds execution facts, not revised H1–H3 or automatic next training.

## 8. Claim Boundary And Next Decision

Even a positive result shows potential only for this data, allocation, token budget and tested seeds. It cannot establish semantic long-tail representation, independent expert memories, improved gradient signal-to-noise ratio, a causal routing explanation or general superiority of depth-varying architectures. A negative result cannot invalidate all such architectures.

The one next researcher decision is whether the completed paired token-frequency evidence justifies later entity/relation and representation or functional validation. Completion requires both frozen budgets, full evaluation, parameter and exposure audits, measured costs, raw metrics and an explicit record of failures or missing items. Resume through R01's recorded outputs; no automatic next architecture or causal intervention is authorized.
