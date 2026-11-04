派生阅读副本；原件位置：`Projects/from-attention-to-search/main/research_notes/frequency_routing_rank_one_20261022_candidate_anchor.md`。
[精确原始文件](../../../../../sources/Projects/from-attention-to-search/main/research_notes/frequency_routing_rank_one_20261022_candidate_anchor.md)；研究修改仍回到原件。

---

# Candidate Anchor: does frequency routing conflate different semantic combinations?

<!-- A15_24_02 ownership handoff -->
**2026-10-23 ownership update:** the researcher requested a formal Anchor, Protocol and bounded analysis. The candidate-direction / local predictive effect / remaining-update clause now has one current owner, [A15_24_02](../problem_anchors/15_spectral_representation_and_functional_routing/15_24_frequency_composition_common_path/subanchors/15_24_02_frequency_complement_anchor.md), with [completed factual results](../experiments/A15/15_24_frequency_composition_common_path/frequency_complement_20261023/summary.md). Other combination proposals and NOT RUN wording below are retained as pre-test history; they neither replace the new local design nor describe its current execution. Combination-update compatibility remains untested. Scientific judgment awaits researcher review.

[中文](frequency_routing_rank_one_20261022_candidate_anchor_cn.md) · [Meeting brief](../../../../../UNAVAILABLE.md)

Status: AI_PROPOSAL. This candidate follows the researcher's present question. It is not a registered current Anchor and does not replace a Focus or training contract. Completed work comprises a control audit, cached natural-text activation analysis, algebra checks and a saved-weight direction diagnostic. New model training is NOT RUN.

**Scope refined on 2026-10-23:** reuse this candidate under [A15_24](../problem_anchors/15_spectral_representation_and_functional_routing/15_24_frequency_composition_common_path/15_24_frequency_composition_common_path_anchor.md), alongside the clipping question; no formal child ID is assigned. Following the researcher's response, separate preference for common input directions from conflict between combination-specific updates. The former has a bounded endpoint diagnostic; the latter remains AI_PROPOSAL / NOT RUN. Neither is established as the cause of the old learning result. No new training is authorized or executed.

**Researcher scope, 2026-10-23 follow-up:** keep the decomposition organized by feature activation frequency. Do not expand this candidate into a general forgetting question. The requested connection is from a candidate direction, to its predictive role, to a controlled restriction of future updates. A helpful shared update is positive transfer in the tested comparison; it does not by itself settle all opportunity-cost comparisons.

## 1. Problem Definition

**Does a low-frequency semantic atom participate in reproducible combinations with particular high-frequency atoms across natural texts, while existing frequency routing assigns different combinations to the same place?**

The refined working conjecture is: **frequency-contribution scores determine which expert receives an input, but do not determine which components of that full input its parameter changes learn to use. Even low-band experts may develop a preference for shared major input directions. Whether this helps rare-feature examples or competes with their learning remains open.** The existing combination hypothesis supplies a separate possible explanation: different combinations sent to one expert may require different updates. It is not a necessary continuation of the directional conjecture. Compatible combinations and useful common-direction learning are live rivals; “same frequency is sufficient” is another candidate, not the default conclusion when conflict is absent.

The parent purpose is to find a representation organization suitable for shared and specialized expert learning. We adopt the researcher's working premise that features are semantic building blocks and examine which components occur together. The measured objects are coordinates of the fixed CrossCoder; concrete interpretations of individual coordinates remain constrained by their source texts.

Ordinary MoE, load-balanced MoE and frequency-routing controls have completed. Forcing a high-frequency expert did not give stable additional benefit over the original allocation. The present uncertainty is whether organizing inputs by occurrence frequency omits relations among their components. We examine natural-text combinations before choosing another expert architecture. Long/short-range labels and interpretations of activation frequency as knowledge difficulty are outside this candidate.

Reproducible differences within the same route would motivate preserving combination identity. Differences explained by current token and corpus source would narrow or weaken this candidate. Sparse matched support leaves it unresolved and calls for more comparable texts. None of these outcomes alone identifies the cause of prediction-loss differences.

## 2. Physical Priors

1. **Researcher-specified working premise:** semantic atoms participate in combinations. An atom may participate in multiple combinations, and common atoms may be shared. Frequency is activation rate on the current TRAIN panel.
2. **Candidate explanation:** combinations may be more suitable organizational units than frequency bands. Similar frequencies do not mathematically determine similar combinations. Their stability and usefulness on actual texts remain empirical.
3. **Advisor intuition and reported senior result:** the four-step rank-one procedure is the supplied structural intuition. Lossless low-precision training is user-reported. The user confirmed that no readable implementation or result record is available; its objective, precision scheme and comparison scope are Unknown. The formalization below is not a reproduction of that implementation.

## 3. Falsifiable Hypotheses

**H-D, refined from the researcher's 2026-10-23 conjecture:** even experts allocated to low-frequency features show net input-matrix changes preferentially aligned with shared leading TRAIN input directions. The completed diagnostic addresses only this alignment. The stronger claim that it diverts useful learning from rare components is untested. Full input permits shared-direction learning but does not logically require it. Useful sharing remains a credible explanation.

**Frequency sufficiency as a rival:** equally helpful transfer between different same-frequency combinations would weaken H-U below. It would not show that frequency caused compatibility: different-frequency combinations or matched random groups might transfer equally well. A sufficiency claim needs a defined population, those comparisons and adequate equivalence precision.

**H:** particular high-frequency partners selected alongside a low-frequency atom on TRAIN retain excess coactivation in other texts. This association persists after matching current token, corpus source and old route, so the route assignment has not fully distinguished those combinations.

**Main rivals:** the partners are generally active; their selection mainly captures token identity, formatting or corpus source; or the existing route already distinguishes the combination differences. The successive controls address these explanations. A shared source is not a shared task, and topic, syntax and templates remain possible explanations.

H concerns representation organization. A further claim that conflated combinations cause training interference and worse NLL needs separate evidence connecting organization to learning. Experts still receive the full hidden state and can distinguish combinations internally. Compression by the routing interface does not imply complete information loss by the model.

**H-U, added on 2026-10-23 and untested:** within one old expert, local parameter updates transfer less helpfully between predefined feature combinations than within a combination, after accounting for sample count, update scale and text conditions. Helpful transfer means that an actual update computed from one sample group lowers prediction loss on another independent group; an increase is a locally adverse effect. This was neither a prediction registered before the original training nor a finding of the clipping experiment. Equally helpful transfer across combinations, or internal separation using the full input, would weaken the proposed shared-learning conflict.

## 4. Mathematical Model

### Frequency, representation and routing

Let \(h(t)\) be the full representation at a natural-text position, \(z_i(t)\geq0\) feature activation, and \(d_i\) its decoder direction. CrossCoder gives \(h(t)\approx b+\sum_i z_i(t)d_i\). An activation is a reconstruction-coordinate strength, not a probability or expert-benefit score. Frequency is \(p_i=\Pr_{\mathrm{TRAIN}}[z_i(t)>0]\). Ten positive activations among 100 positions give frequency 10%, independently of their ten magnitudes.

With a fixed decoder whose columns form \(D\),

\[
\operatorname{Cov}(\hat h)=D\operatorname{Cov}(z)D^\top.
\]

Representation variation depends on activation magnitudes, joint variation and decoder geometry. Occurrence rates do not determine these quantities. Even for binary activations, rates determine only covariance diagonal entries; off-diagonal entries depend on joint occurrence.

An exact counterexample uses two common atoms with frequency 50% and two rare atoms with frequency 10%. Rare A can always accompany common A and rare B common B, or their partners can be exchanged. All marginal rates remain identical. If the common atoms share one group and the rare atoms another, position-wise group totals can also be identical. The [algebra receipt](../../../../../UNAVAILABLE.md) records this constructed example, not an observed text result.

The existing router forms four TRAIN-frequency bands and two subgroups per band. It sums \(z_i(t)\lVert d_i\rVert\) into eight subgroup contributions, adds the two subgroups within each band, and divides by that band's mean TRAIN contribution. T_F first selects the two highest-scoring distinct bands, then selects the subgroup with the larger raw contribution in each. These scores do not measure or predict the two fastest loss-decreasing bands. For example, activation 0.2 and decoder norm 3 give a contribution of 0.6; frequency is still counted separately from positive occurrences. The rule uses both frequency and current activation magnitudes. Different within-group atoms producing identical totals cannot be distinguished by these scores alone. Each selected expert still reads full \(h(t)\). The concrete candidate is that this compressed allocation signal may not preserve combination identity.

### Input direction is not an update requirement

Leading input directions refer to right singular directions of a centered batch matrix of hidden states, equivalently covariance eigenvectors. They are not defined by a single input, and activation frequency alone does not identify them. For a matrix reading \(u=h/s\), the gradient is \(N^{-1}\sum_t\delta_tu_t^\top\), where \(\delta_t\) depends on prediction errors and subsequent computation. Large input variance does not ensure a large gradient or actual AdamW update.

The [direction diagnostic and checked teaching examples](frequency_routing_input_update_direction_20261023.md) make these distinctions concrete. In one linear example, the highest-variance component is already predicted correctly and has zero gradient. In another, the same two combinations and frequencies give helpful or harmful transfer solely by changing the second target. A full-input expert may also distinguish the combinations internally. Different combination identities and equal band scores therefore do not determine whether separate experts are useful.

### Observable combination statistic

For each rare atom \(i\), reuse its original TRAIN-selected set \(C_i\) of at most eight common partners and its frequency-bin-matched random set \(R_i\). Define \(B_i(t)\) as the difference between the two sets' active fractions. Subtract its mean at matched positions in other dialogues where atom \(i\) is inactive:

\[
\Delta=\operatorname{mean}_{(i,t)\in\mathcal E}
\left[B_i(t)-\operatorname{mean}_{s\in\mathcal M(i,t)}B_i(s)\right].
\]

\(\mathcal E\) contains eligible rare-feature events; several events may share one position. \(\mathcal M\) is the matched control set. The statistic is an activation-fraction difference, or percentage points after multiplication by 100. It measures excess coactivation of particular partners relative to random partners. Coactivation is not equated with jointly accomplishing a task. Lists are fixed from old TRAIN, without selecting on this analysis's losses or future target tokens.

### What was normalized, and what can be held fixed

The completed direction diagnostic uses unit-length PCA basis columns and divides projected net-change squared norm by total net-change squared norm. It does not divide activation coordinates by their singular values, whiten the inputs, compare weight-SVD vectors with input vectors, or use a task-loss measurement. Singular values determine the ordering of the input basis; they do not weight the reported parameter-change share. A direction's projection score therefore does not name its task.

For a candidate input basis \(V\), let \(P=VV^\top\), let \(W_*\) be the saved current input matrix, and let \(\Delta W=W_*-W_{\mathrm{init}}\). A proposed finite diagnostic is \(W_\epsilon=W_*-\epsilon\Delta WP\): partially back out the observed net change along these inputs while holding all other parameters and routes fixed. Compare predictions with the unmodified checkpoint and a same-rank random-direction edit matched for actual parameter-change norm. This is a diagnostic of the selected saved change, including its optimizer history; it does not uniquely locate task knowledge or show what a future update will do. Selection uses discovery data, and evaluation uses separate samples; the current exposed panels cannot supply fresh confirmation.

A subsequent candidate learning constraint is defined separately. Decompose \(W_*=C+R_0\), with \(C=W_*P\) and \(R_0=W_*(I-P)\). Keep \(C\) in the forward computation. For a proposed complete optimizer displacement \(U_t\), including AdamW history and weight decay, apply

\[
W_{t+1}=W_t+U_t(I-P).
\]

Because \((I-P)V=0\), this preserves \(W_tV=W_*V\) exactly in real arithmetic for this one matrix with a fixed basis. It freezes this matrix's response to the selected input directions. It does not guarantee unchanged high-frequency-example predictions: real inputs mix directions, and downstream nonlinear computations may use their interactions. High-frequency and overall prediction quality must be measured. An alternative implementation is \(W=W_*+A(I-P)\), initialized with \(A=0\); this also preserves the matrix action, but optimizer initialization/history requires a matched control. Projecting only the raw gradient does not guarantee the same restriction after AdamW's coordinate-wise transformation and weight decay.

This input-side constraint is one AI formalization. It differs from the two-sided rank-one remainder below and is not a recovered implementation of the advisor's algorithm. Prefer one predetermined gate or up matrix for a first local comparison; other weights, router, scale and mixture coefficients stay fixed. Extension to multiple matrices or long training is a separate decision.

### Connection to the rank-one intuition

For one linear matrix, write \(W=C+R\), where \(C\) contains extracted components and \(R\) is the remainder. Transferring \(D_j=\sigma_j u_jv_j^\top\) by \(C'=C+D_j\), \(R'=R-D_j\) preserves \(C'+R'=W\). This exact re-expression preserves the output and loss at transfer time.

Intuitively, flat initialization gives parameter directions similar starting scales, extraction specifies how a component is retained, and orthogonality specifies where the remainder can vary. None of these operations yet specifies which component a natural-text input should select.

One strong interpretation of learning an orthogonal remainder is \(U^\top R=0\) and \(RV=0\), where \(U,V\) contain orthonormal extracted directions. With \(P_U=I-UU^\top\), \(P_V=I-VV^\top\), parameterize \(R=P_U A P_V\). If the extracted component is fixed, one candidate objective is

\[
\min_A\;\mathbb E_{x,y}\,
\ell\!\left(F\!\left((C+P_U A P_V)x\right),y\right).
\]

Here \(x\) is the layer input, \(F\) the subsequent computation, \(y\) the target and \(\ell\) the original task loss. Two-sided orthogonality and fixed \(C\) are AI formalization choices, not known properties of the senior's algorithm. They restrict updates and may restrict attainable solutions relative to ordinary training. Reaching singular value one does not itself certify learning: a scalar weight fixed at one cannot fit a required output of two for unit input.

The flat initialization scale, normalization underlying threshold one, extraction timing, continued updates to extracted components and optimizer-state transfer are unknown. If initialization sets every singular value to one, the literal rule immediately extracts all directions. Flattening an existing matrix generally changes its computation; initialization and exact extraction are different operations. Repeated singular values also admit basis rotations and do not uniquely identify semantic atoms.

Adding all rank-one components and selecting only a few per input are different computational arrangements. For an exact decomposition with orthonormal output directions, retaining original coefficients and dropping unselected terms gives squared output error

\[
\lVert e(x)\rVert^2=
\sum_{j\notin S(x)}\sigma_j^2(v_j^\top x)^2.
\]

\(S(x)\) is the selected set. A flat spectrum or singular values reaching one does not make omitted input coefficients vanish. For \(W=\operatorname{diag}(1,0.5)\), \(x=(1,1)\), the full output is \((1,0.5)\), while selecting only the first component yields \((1,0)\), with output error 0.5. This is exact algebra, not a language-model loss experiment.

The advisor's intuition can therefore be expressed as: components needed jointly in a sum cannot be treated as interchangeable expert choices without an additional condition. Rank-one modules can occur inside MoE; there is no general logical incompatibility. Lossless sparse selection additionally requires small omitted contributions or compensation by a retained path. Parameter orthogonality also does not imply semantic independence: orthogonal readout directions can have perfectly correlated activations when input coordinates are equal. Existing SwiGLU experts are nonlinear; a single-matrix identity does not directly decompose their whole computation.

## 5. Computational Realization

**Frequency decomposition requested on 2026-10-23; AI proposal, NOT RUN:**

1. **Define the frequency-linked candidate.** Keep the original TRAIN activation-rate definition and fixed low/high feature lists. The existing global PCA directions are candidates with measured frequency-band contributions; they are not certified high-frequency-only directions. Do not require a complete semantic label for every parameter before a bounded test.
2. **Identify the current functional role.** On the same prediction problem, evaluate the partial rollback above using predefined low-feature, high-feature and overall loss readouts, retaining the overlap between frequency-conditioned position sets. A high-frequency feature may occur at a low-feature position, so these are not disjoint tasks. If rollback harms both groups, retain shared utility; if its effects differ, retain that local functional difference. A random edit of the same actual norm, exact no-op replay, support and independent selection/evaluation samples distinguish direction-specific effects from generic damage. Insufficient support or replay failure gives no verdict. This is the recommended immediate question.
3. **Test whether restricting future updates helps.** From identical saved model and optimizer states and the same batch, compare an unconstrained actual update, its selected-subspace restriction and a same-rank random restriction. Report natural step sizes and a norm-matched comparison. Measure separate-sample low-feature loss and high-feature/overall preservation, rather than inferring benefit from orthogonality. If the selected restriction beats both controls at comparable update size, retain this local update policy for a later equal-budget continuation; if it only preserves the high-frequency readout without improving low-feature learning, the intended benefit is unsupported. Longer-training utility remains a subsequent question. These are design proposals, not authorization or executed updates.

The meeting recap explicitly separates low-dimensional routing from the learning mechanism of keeping extracted components and training a remainder (H1 versus H4). It also distinguishes a retained forward path from deleting a component. See the [original supplied recap, sections 4 and 6](../../../../../UNAVAILABLE.md). Holding the router fixed here follows that separation; it is an AI proposal for the present frequency question.



**Completed bounded H-D diagnostic:** compare initialization-to-step-168 gate/up weight changes for original T_F seeds 11/22 with the previously saved global TRAIN PCA and random bases, at fixed ranks 1 and 16. Report every expert/matrix and initial-weight controls. No forward, backward or optimizer step was taken. The [diagnostic](frequency_routing_input_update_direction_20261023.md) defines the norm share, identities and limits; endpoint movement is not useful learning.

**Candidate check for the new bridge, NOT RUN:** fix combination definitions without looking at intervention benefit, compute an actual sample-group update from identical model parameters and optimizer state, and evaluate its effect on other independent sample groups. Compare within- and between-combination effects with sample-count, old-expert, text-condition and perturbation-scale controls. Raw gradient angles do not replace actual optimizer updates. Combinations, saved states, update scale, confirmation data and decision rules remain unspecified. The table below describes completed representation analyses, not this new check.

| Goal | Completed computation | Why |
|---|---|---|
| Establish interpretable controls | Audit four ordinary-MoE endpoints, digests, metrics, target counts, frozen source, initialization and LB normalization | Separate record errors from scientific explanation |
| Measure combination specificity | Reuse TRAIN partner/random lists; separately evaluate exposed EVAL and DEV | Avoid reselecting partners from present outcomes |
| Address token, source and route rivals | Successive exact matching; controls in other dialogues with the rare atom inactive | Make alternative explanations explicit |
| Reconnect coordinates to text | Hash-selected examples from the strict matching pool; preserve visible prefixes and current tokens | Give concrete objects and retain unfavorable cases |
| Check rank-one reasoning | Exact transfer identity, sparse-omission and equal-frequency counterexamples | Separate algebra from training efficacy |

Matching requires at least ten control positions across three other dialogues. These guards were fixed before calculation and are not scientific effect thresholds. The existing Tulu subset contains TRAIN 1,024 dialogues/85,548 targets, EVAL 256/22,446 and DEV 128/10,340. Analysis used local CPU and saved caches, with no model forward, training or remote submission. The [scope](../../../../../UNAVAILABLE.md) and [asset access check](../../../../../UNAVAILABLE.md) preserve identity.

## 6. Minimal Falsification Tests

For H-D's bounded endpoint question, consistently greater PCA than random projection retains directional preference; values near the reference weaken that specified preference; inconsistent or invalid measurements are insufficient. This is a descriptive branch without a researcher-confirmed practical-effect threshold. The functional next question is whether shared-direction changes help rare examples. Helpful sharing would contradict treating alignment itself as suppression. Competition needs a controlled change that improves rare learning against matched alternatives, not merely a large projection share. No such functional comparison was run here.

The decisive comparison asks whether excess coactivation of fixed partners recurs across dialogues within predefined token/source/route conditions. Zero is a directional reference. The minimum practically meaningful effect, required coverage and confirmation panel are not researcher-confirmed, so this pilot does not adjudicate method acceptance.

- **Supporting direction:** adequately supported new texts retain positive excess association and distinguishable combinations within one old route. This supports investigating combination preservation, not training benefit.
- **Non-supporting direction:** with sufficient precision, token/source explains the association or the old route already distinguishes combinations. Lower the priority of the omitted-combination explanation without denying all semantic combinations.
- **Insufficient:** sparse matched support, mainly formatting examples, inconsistent dialogue directions or only exposed panels. Keep the question open without relaxing matching to obtain a verdict.

Because the old route is computed from activations, conditioning on it can introduce selection effects. This comparison describes remaining within-route structure; it is not a feature intervention. Before formal activation, coverage, uncertainty estimation and a meaningful effect threshold should be fixed ahead of new outcomes. This candidate authorizes no additional expensive run.

For H-U, support requires reproducibly worse between-combination update effects than matched within-combination effects. Non-support includes equally helpful between-combination transfer measured with adequate precision, or differences explained by exposure and update scale. Sparse matching, failed numerical replay, or effects confined to data used to select combinations give insufficient evidence. Even a valid local effect would require a subsequent controlled grouping intervention to explain the original full-training difference; these are not combined into an established cause here.

## 7. Current Evidence

**New post hoc direction diagnostic, 2026-10-23:** in original T_F checkpoints, the first 16 global input directions contain 15.16%/15.33% of pooled gate/up net-change squared norm for seeds 11/22, against 1.49%/1.48% for 16 random directions. Low-band E0/E1 shares are 14.85%/14.05%, against 1.48%/1.52%. All 32 individual matrices exceed their random reference. This is preferential alignment, not most of the parameter change or proof of suppressed rare learning. The [full diagnostic](frequency_routing_input_update_direction_20261023.md) retains all rows, initial controls, scope and freshly verified checkpoint digests. Its global basis and endpoint displacement do not explain per-step learning or expert-local covariance; weight-decay effects are included.

**Local progress verified on 2026-10-23:** the separate [A15_24_01 clipping intervention](../experiments/A15/15_24_frequency_composition_common_path/common_optimizer_coupling_20261022/summary.md) completed four models and twenty same-state update comparisons. Shared clipping changes actual updates, but removing that coupling changed rare-feature macro loss by -0.000332 and +0.000529 nat, without stable improvement. This weakens that specific clipping remedy; it does not establish combination organization as the cause. The original combination analysis retains the same-token/source/route support limitations below. H-U has no results.

**Saved controls are audited.** Both seeds of ordinary MoE and MoE_LB completed 168 steps on four H100 Reserved GPUs. Configuration, target alignment, paired initialization, endpoint tensors and saved metrics agree. Two-seed overall DEV means are Base 1.248870, MoE 1.224985, MoE_LB 1.226042, free frequency allocation T_F 1.226137 and forced-high allocation T_H 1.227138. T_H did not achieve the registered stable extra benefit; its rare-feature macro direction differs across seeds. Learned and fixed routes also differ in mixture weights and router parameters, preventing attribution solely to the grouping basis. See [control Detailed](../../../../../UNAVAILABLE.md).

The old frozen diagnostic confirms actual partner replacement at 1,015 of 1,701 rare-feature positions. T_H keeps the first expert and replaces the second; each coefficient is 1/2, with the full Base path retained. Its replay gate failed, leaving residual benefit and cancellation mechanisms unresolved. Recomputing saved metrics does not repair that failure. See [diagnostic results](../experiments/A15/15_24_frequency_composition_common_path/20261020_20261019T164834Z/diagnostics_20261021/results.md).

**The new contribution is conditional natural-text combination analysis.** Original EVAL/DEV contain 4,709/2,131 rare-feature events. Means below weight eligible events equally, and events can overlap positions. Matching levels select different subsets; subtracting rows does not estimate how much effect a control explains.

The lowest-frequency band B1 contains 1,694 features, each active only 1–17 times on TRAIN. This sparse support directly limits same-token/source/route comparisons; the analysis is not a precise negative test.

| Matching | EVAL: excess association; events/positions/dialogues | DEV: excess association; events/positions/dialogues |
|---|---|---|
| Current token and source | +14.19 percentage points; 551 / 461 / 119 | +10.50 points; 150 / 129 / 49 |
| Also the same old expert pair | +4.54 points; 32 / 32 / 24 | +5.13 points; 7 / 7 / 5 |

For the first row, positive/negative dialogue means number 100/18 in EVAL, with one zero, and 35/14 in DEV. Directional heterogeneity remains. The second row has too little coverage to establish widespread combination conflation by the old route. EVAL and DEV were already exposed, with no independent confirmation interval. See [full statistics and denominators](../../../../../UNAVAILABLE.md).

**A concrete text pair:** one DEV CodeAlpaca prompt requests binary search; the current token is the comma after the arr function parameter. A same-source, same-comma, same-route control requests a nested dictionary from keys and values, at the comma after dictionary(list_keys. Feature 12669 is active in the former and inactive in the latter. These texts use familiar code components for different operations. This illustrates why text-grounded combinations matter; it does not identify a “binary-search feature” or require separate experts. This event's excess association over all 15 matched controls is only +2.50 points. A same-punctuation, same-route Chrome-extension/Japan-travel example is negative and is retained. See [all DEV cases](../../../../../UNAVAILABLE.md).

**Constraints from updates since October 16:** old group-contribution PC1 shares were 35.94%/44.19% for same/mixed-frequency groups and remained 35.37%/44.11% after independent feature-position shuffling. Marginal statistics and decoder geometry can therefore plausibly account for much of that spectral pattern. Later full-hidden hit-sample spectra differed in direction but used another window, so they are not same-position causal counterevidence. See the [October 16 supplement](../../../../../UNAVAILABLE.md). October 19 calibration raised rare-feature reception while one low-band expert's full inputs still averaged 1.38 rare and 195.54 common active features; counts are not influence. See the [bridge result](../../../../../UNAVAILABLE.md). October 22 constructed relation questions are a separate task; their shared directions and response bias do not explain the natural-text training differences. See the [separate task](../../../../../UNAVAILABLE.md).

## 8. Claim Boundary And Next Decision

This advance yields two meeting-ready judgments. First, frequencies and group totals do not uniquely determine combination structure; the matched token/source subsets retain particular partner associations. Second, an additive rank-one decomposition preserves current computation, while sparse MoE needs an additional condition specifying what can be omitted. Together they motivate studying shared components and context-specific combinations, rather than defining experts solely by frequency or singular-value magnitude.

The performance cause of old routing remains unresolved, and the advisor algorithm's lossless training has not been established here. An exclusive relation-based atom partition could still split combinations across groups; renaming the grouping criterion does not resolve that issue.

If the next check supports this structure, the concrete candidate unit is the combination active at the current position, allowing one common atom to be shared by several combinations. Compare its cross-text organization stability with frequency grouping before choosing an expert implementation. No new router or training loss has been selected here.

**One next decision refined on 2026-10-23, AI proposal:** prioritize whether the observed common-direction changes help rare-feature examples or compete with their learning. The researcher correctly identified full-input access; the remaining distinction is between parameter movement and functional benefit. H-U remains an alternative, without assuming that different combinations must conflict. If between- and within-combination updates are equally compatible with adequate precision, lower that explanation's priority; do not automatically conclude that frequency is sufficient. Fix exact saved states, independent samples, controls and meaningful precision before a functional intervention. Existing matching gaps remain. This revision adds a static diagnostic and refines the candidate, without selecting a router, launching training or changing scientific closure.