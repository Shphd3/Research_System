# A17: Why Measure Shared Learning, And What SAE Can Explain

Derived explanation, AI proposal, 2026-10-10. [中文](A17_shared_learning_logic_cn.md). Scientific authority remains in the [Anchor](../problem_anchors/17_shared_and_interference_learning/17_01_controlled_list_prediction_rules/17_01_controlled_list_prediction_rules_anchor.md), [E02 Protocol](../experiments/A17/17_01_controlled_list_prediction_rules/A17_01_E02_restricted_update_calibration/protocol.md) and [E03 Protocol](../experiments/A17/17_02_fixed_pool_frequency/A17_02_E01_fixed_pool_frequency/protocol.md). This note neither approves experiments nor creates a second design. SAE analysis is planned, NOT RUN.

We want to understand when learning one conditional prediction rule improves another, and when it impairs another, under specified resources. FIRST/LAST lists make the rules and correct answers explicit. They share vocabulary, list-generation process, format and answer distribution; they differ in the instructed selection operation. For “red blue green”, FIRST answers red and LAST green. Their complete prefixes differ, so both labels can be satisfied by one conditional model. Task difference is not itself conflict.

| Step | Question | Required evidence | Nearest boundary |
|---|---|---|---|
| Behavior | What happens to B when A is practiced more? | Same/different-rule trajectories; fixed-B addition and separate fixed-budget allocation | Policy effect, not an isolated count mechanism |
| Native update | What does a useful A update change on B? | Actual effective matrix change, recipient displacement and finite CE | One state/location/step, not long-term harm |
| SAE description | Which frozen dictionary directions describe that change? | Before/after encoding plus reconstruction residual | Description/attribution, not functional independence |
| Intervention | Does keeping/removing a candidate change the effect? | Held-out finite interventions with rank/amplitude/restoration controls | Conditional local use, not an expert architecture |
| Later design | Does basic processing plus conditional corrections improve learning? | Capacity/compute/data/opportunity-matched training comparison | A later decision; currently Unknown |

The immediate priority is the first two steps. SAE is useful only if its description changes our explanation or next decision; native update analysis does not require it. Helpful effects, harmful effects and rule-dependent differences in help can all be legitimate targets. Do not require a harmful result before analysis, or force SAE to succeed.

## Direct Projection And LoRA

“Final projection” here means layer27 Attention `o_proj`, not the vocabulary `lm_head`. Direct training changes its1024×2048 matrix with2,097,152 free parameters. Rank8 LoRA freezes that matrix and adds sBA with24,576 trainable factor parameters. Its cumulative added matrix has rank at most8, and its optimizer path differs. Same LR is not equal functional displacement. Both preserve the chosen location and permit reading the actual effective ΔW. Prefer direct-matrix training as an AI candidate for the main frequency study; treat LoRA as a capacity sensitivity. E02 Smoke qualifies implementation, not this scientific choice.

Freezing upstream lets us define a as this matrix's input, h as its output and r_in as the incoming residual. For a fixed record, a is unchanged, so

\[
h_0=W_0a,\quad h_1=(W_0+\Delta W)a,\quad \Delta h=\Delta W a.
\]

This identity is exact. The native answer CE sensitivity e_h gives a first-order attribution e_hᵀΔh; define R as actual finite CE minus that attribution. A helpful negative or harmful positive finite change is the measured outcome. Existing shared-update derivations already establish these local relations; the missing evidence is their behavior in this new carrier. Only the selected final location is allowed to learn, so no result identifies all shared functions throughout the model.

## Frequency: What Each Comparison Means

Use fixed disjoint200-list A/B pools. Same-rule and different-rule arms use the same pool contents. Hold B at200 presentations and increase A from200 to800: this asks what additional A practice does, including its extra training budget. For each count, match same/different budgets. Their difference-of-differences asks whether the relative rule effect changes with A practice. A positive value can mean that different-rule A helps less; net harm additionally needs an appropriate B-only/local reference.

Separately compare800A/200B with500A/500B at1,000 answers. That asks how to allocate a common budget; B opportunities change. Neither comparison simultaneously isolates frequency, B exposure and compute. Constant LR avoids source-dependent warmup exposure. Report both B target roles and both novelty types, each separately and as the frozen combined primary. Order-new retains training-seen unordered content but changes order; combination-new contains an entirely unseen unordered group. Both are task-training novelty, not unseen pretraining text.

Three independent seeds provide exploratory effects, not a confirmatory significance claim. Optional six NEW seeds and unopened test follow a separately frozen median-interaction rule. δ=0.01nat/answer and two-sided confirmation are AI candidates for review. Exact arms, counters, statistics and proposed resource ceilings live in E03, NOT RUN.

## SAE: How To Describe The Change Without Losing It

A frozen SAE represents a vector using a sparse set of learned decoder directions. It is a measuring dictionary, not a new predictive task or a proposed expert partition. For a matching observer at raw h, encode actual before/after states separately, z_k=E(h_k). Let D be the decoder, b its bias and u_k=h_k−Dz_k−b the uncaptured part. Then

\[
\Delta h=D(z_1-z_0)+(u_1-u_0).
\]

The first part is the dictionary-described change; the second is the remaining change. This bookkeeping is exact even if the dictionary is imperfect. Encoding Δh itself is different because the encoder is nonlinear. Shared activation or a readable name supplies a candidate only. Analyze which signed components accompany actual improvement or impairment and retain the loss-weighted residual and finite nonlinear remainder. Good absolute reconstruction does not establish good reconstruction of a small, consequential update.

SAE-difference activation patches test an input-specific change. A realizable global matrix intervention instead orthogonalizes selected decoder directions into a projector P, then tests PΔW and(I−P)ΔW. This changes every input by PΔh/complement, which is generally different from the input-specific SAE encoding contribution. Do not conflate those interventions.

## Available SAE Interfaces And Minimal Analysis Plan

The current S7 exact33B embedded SAE matches raw last-block Attention output. It belongs to a separate model and cannot be transferred to Qwen/Dense because vector widths agree. Current Qwen E16 SAE reads normalized final MLP input v=N(r_in+h). Its parent is official-a5; full SHA256 verified current share Base/parent config and weights byte-identical, without loading models ([receipt](../experiments/A17/17_01_controlled_list_prediction_rules/A17_01_E03_fixed_pool_frequency/sources/sae_parent_identity_20261010.json)). This resolves parent identity, not hook mismatch or observer qualification on adapted states. No matching Qwen raw-o_proj-output SAE has been verified within the inspected registry and source families.

For the existing Qwen observer, the downstream state is t=r_in+h+MLP(v). SAE can describe Δv in the MLP branch; the direct residual Δh bypass remains. First-order terms are g_tᵀΔh+g_vᵀΔv, where g_t and g_v are native CE sensitivities at t and v. Total e_h already contains both paths: adding the second term again double-counts. A v patch intervenes only on the MLP branch, not the entire matrix update.

AI plan:

1. Establish native actual effects at unsaturated, useful states using balanced independent sources, full-vocabulary CE, no-op/repeat precision and exact restores. A source guard qualifies local mechanism statements; it does not delete a valid frequency-policy endpoint.
2. Choose and bind the observer: Qwen native first, then verified existing MLP-input SAE for a branch analysis, or S7 plus its matched raw-output SAE as independent replication. A new Qwen raw-output SAE is an additional decision, not this round's execution.
3. Check absolute and displacement reconstruction, loss-weighted omission and model-state drift. If residuals carry the effect, report reader ineligibility/non-support rather than train until expected features appear.
4. On independent discovery groups select candidate directions, freeze them, then evaluate removal/retention on held-out groups/batches. Use full/no-op/restore/replay, native PCA/SVD and same-rank random spaces, actual amplitude matching, unscaled removal and norm-restored redirection, full/half steps, source-usefulness checks and all rule×novelty panels.
5. Compare actual finite effects. Nonlinear finite contributions need not add; report interactions. Loss-selected directions are post-hoc discoveries, not prospective predictors. Support establishes conditional local use; failure of the SAE does not erase native behavioral evidence.

## Where The Basic-Module / Unique-Direction Intuition Fits

Your intuition is a candidate functional decomposition at the description/intervention steps, then a later architecture to compare. A sample can require both list reading and rule-dependent selection; it is not assigned entirely to a common or unique bucket. A direction useful for both tasks is a candidate shared-useful channel; one with different conditional effects is a candidate rule-related channel. Neither name proves it is the whole basic processor or a unique expert.

“Different from the basic module” should be operationalized as a useful conditional correction to a defined baseline, not orthogonality to the baseline weight matrix. Distinct parameter directions may perform the same function; shared directions may have different effects on different inputs. A final-layer finding also cannot inventory functions already computed in frozen upstream layers. Even a successful local channel intervention leaves capacity, routing, generalization and long-term learning utility for a later matched architecture comparison.

## Decisions For Researcher Audit

- Accept direct `o_proj` as the primary candidate and LoRA as a separate capacity comparison? The intended location is explicit; it is not `lm_head` tuning.
- Adopt both B directions, seven conditions each, three exploratory seeds and a constant-LR policy? This is42 proposed trajectories, not an execution queue.
- Adopt the combined interaction as the sole primary, retain all panel disagreements, and reserve optional six-new-seed confirmation? Practical δ and alternative direction remain your judgment.
- Limit SAE to locating an already measured effect; choose the legitimate Qwen branch observer or independent matched S7 observer? No automatic new SAE training.
- Accept that functional candidates precede architecture decisions, and that common activation/orthogonality alone cannot identify basic modules or unique experts?

Current authorization update (2026-10-10): the researcher adopted direct o_proj/LoRA capacity control, independent A17_02 frequency and matched raw-output1B SAE with complete supervision. Current Focus/Protocols govern; earlier candidate/no-run wording here remains explanatory history.
