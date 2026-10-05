# Understand the Recent Research in One Day: From Update Effects to Learning Allocation

[中文](learning_guide_cn.md) · [Daily entry](README.md)

**Today is organized around eight hours of active study. The goal is to reconstruct the research reasoning independently, derive the key relations, check selected evidence, and explain why the next step is worth taking.** Rebuild the October 2 starting point, focusing on the work from October 3 through early October 5. Reading to the end is not the same as understanding: each session requires a calculation or a closed-book explanation, which you will use to identify remaining gaps.

This is the teaching plan and derived reading guide requested by the user. The original Summaries own the results; the Anchor and Protocol own the design. Exercises and suggested learning criteria are not scientific decision thresholds. The researcher's mechanism judgment, practical benefit threshold, and next scientific decision remain Unknown. Execution status refers to the archived observations through 2026-10-04 17:48:35 UTC, or October 5 at 01:48:35 Beijing time. No GPU status was queried again and no GPU job was started for this guide.

## 1. How to Study Today, and What to Be Able to Do

Start with this document alone. In each session, read the explanation, check one decisive piece of evidence in the specified source, then close the document and complete the task. When a formula is difficult, return to its objects and assumptions rather than expanding immediately to all 17 papers. Consult long proofs, complete result tables, and execution logs as needed.

Prepare a page called “My research map,” with four columns: **Why this step was taken / What was actually done / What we learned / What we still cannot claim**. Use your own words rather than copying whole paragraphs. Reserve two more pages for derivations and tonight's next decision.

The schedule contains 480 minutes of study plus 110 minutes of breaks and meals. The example starts at **12:00 and ends at 21:50 on October 5, Beijing time**. If you start at a different time, shift the whole schedule while keeping the session durations. Breaks are 12:40–12:50, 14:00–14:10, 15:00–15:10, 16:10–16:25, 17:35–18:20, 19:25–19:35, and 20:35–20:45.

| Session and example time | Minutes | Question you must resolve | Output to leave behind |
|---|---:|---|---|
| Session 1, 12:00–12:40 | 40 | Where were we stuck? Which comparison objects changed over these two days? | A diagram of the three objects; five known/unknown statements |
| Session 2, 12:50–14:00 | 70 | How does source text change another text's prediction? Why can SAE coordinates not directly replace the true displacement? | Two derivations: gradient to loss, and the SAE residual |
| Session 3, 14:10–15:00 | 50 | What remains stable when the source changes? Why does reproducibility after observing the target not imply predictability beforehand? | An explanation of the two A/B splits and 99.02% |
| Session 4, 15:10–16:10 | 60 | Why are prediction, selection, and future specialization different questions? | A conditional-risk equation and two counterexamples |
| Session 5, 16:25–17:35 | 70 | What did the new panel, within-category control, and amplitude check each rule out? | A table of three controls and two numerical checks |
| Session 6, 18:20–19:25 | 65 | What can sharing and private learning each offer? What do the six arms actually compare? | A finite-sample example and a six-arm comparison table |
| Session 7, 19:35–20:35 | 60 | How do Adam and future training change today's effect? | A hand calculation of 0.5→0.405→0.57245 and the retention decomposition |
| Session 8, 20:45–21:50 | 65 | Can I explain, verify, and choose the next step independently? | Three evidence checks, 12 questions, and a one-page next decision |

Today's target is to explain the main line for 10 minutes without looking at the material; state assumptions while deriving relations rather than merely reciting formulas; ask “relative to what, on which data, and answering which question?” whenever you see a positive number; and know that **there is currently no winner from completed shared/private training**. If a central conceptual error remains, use the remaining time to repair that session rather than hiding the gap under more reading.

## 2. Session 1: Draw the Right Problem Map First (40 Minutes)

### 2.1 The Starting Point Was Not a Blank Slate

The original concern was how relationships in natural-language data affect shared parameter updates, and whether SAE analysis could help explain them. Representation, gradient, and sensitivity analyses already existed; it would be wrong to say these had never been studied. Two earlier formal conclusions still stand: the natural-statistics primary test was INSUFFICIENT, with statistic 0.006637 and interval [−0.003738, 0.017012]; the primary test of predicting the gradient inner product between two DCLM events before seeing their targets was NON_SUPPORT, with Q of −0.000138. Later questions and new data cannot retroactively rewrite either verdict.

We then posed a more directly operational question: **Given a source batch, how does one specific update produced by it affect other texts? Can these differences be used before the target appears?** This was a concrete research choice, not the only next step logically permitted by the earlier negative result. The researcher subsequently focused the goal on whether small experts could approach a larger Dense model under limited resources, and whether placing specialized computation after a common module would help. That required studying actual learning and retention.

### 2.2 Keep Three Objects Separate Throughout

| Object | What is held fixed, and what changes? | Progress over these two days |
|---|---|---|
| Update effects and selection among existing actions | Freeze the model and candidate updates; change the source or select an action from the input | Native finite-loss measurements, prediction, and selection diagnostics are available |
| Learning allocation | From a common starting point, let data update shared parameters or private copies | Six-arm design and implementation checks; 0/12 formal trajectories |
| The future effect of one update | Accept or reject the current update, then execute the same future training | Computational relations and analytical counterexamples; no corresponding causal LM trajectory result |

The research route can be drawn as:

```text
Representation description → Actual update effects → Response prediction before the target → Fixed-library action selection
                                                                                                      │
                                                                          Current selection cannot replace future specialization
                                                                                                      ↓
                                                    Shared/private learning → Optimizer and subsequent training → Acquisition and retention
```

An arrow means that evidence must be added or the comparison object must change. It does not mean that the preceding item has already established the next.

Also distinguish four kinds of evidence: **description** says that a difference exists; **prediction** says it can be forecast from permitted information; **intervention** says what finite effect a specified change produces; and **utility** asks whether adopting a scheme beats an available control. These are different questions, not a ranking of results from low to high.

### 2.3 Objects You Will Encounter Repeatedly Today

| Term | Meaning in this research | Common misreading |
|---|---|---|
| NTP / CE | Next-token prediction / cross-entropy loss, usually lower is better | Response-prediction Q is not the percentage reduction in CE |
| SAE | Sparse autoencoder: describes activations through a small set of active coordinates | Encoding coordinates are not automatically true update channels |
| Source / receiving event | Data that produce a gradient / a prediction position at which the update's effect is evaluated | Source A/B and FIT/DEV are two different split axes |
| FIT / DEV | Records for fitting and selection / records for reading out results | Previously exposed DEV is not a new confirmation set |
| Action library | A set of already computed parameter perturbations, including a common action | A fixed action library is not an already trained MoE |
| Ridge | An estimator fitted using squared error and a coefficient penalty | Failure of a particular ridge estimator does not prove that its input lacks information |
| 33B | A checkpoint after 33 billion training tokens | Not 33 billion parameters |
| Common action / common module | One perturbation formed by averaging raw gradients / a trainable FFN module | These terms cannot be used interchangeably |

**Check the sources:** [Initial report](../1002/candidates/ntp_representation_update_channels/research_report.md) §1, [research process](../1002/candidates/ntp_representation_update_channels/research_process.md), October 3, 04:14–04:53 UTC, and [understanding update](../1004/cognition_update.md) §1.

**Closed-book task, final 10 minutes:** Draw the three-object diagram and explain why “fixed-library routing failed” cannot answer “is training private experts useful?” Reference answer: the latter changes the future experts themselves, whereas the former only selects among existing actions. The possibility of the latter does not turn the former's negative result into success.

## 3. Session 2: Derive the Actual Effect from the Gradient, Then Check the SAE (70 Minutes)

### 3.1 Why We Started at This Level

Seeing an SAE coordinate activate frequently only tells us what it describes. Seeing sensitivity along a direction only tells us that moving along it could matter. We still need to know: **Does source learning actually move the model in that direction, and how does the receiving event's loss change?** We therefore derive the actual update chain first, then check whether the analysis tool tracks it faithfully.

Fix the final block's attention output matrix W. Its input is a column vector c and its output is a=Wc. For a source event, let e be the gradient of the loss with respect to a. The chain rule gives the matrix gradient G=ecᵀ. Write M_A for the average gradient of source batch A and η for the learning rate. In this diagnostic, only this matrix changes; other parameters and the receiving event's input c remain fixed:

\[
\Delta W=-\eta M_A,\qquad
\Delta a=\Delta Wc=-\eta M_Ac.
\]

**This displacement relation is exact under the fixed-interface conditions above.** The first-order loss expression, however, is only an approximation. Let ℓ be the receiving event's loss after the remaining network computation, and let e_r be its gradient with respect to a:

\[
\Delta\ell=\ell(a+\Delta a)-\ell(a),\qquad
\Delta\ell\approx e_r^\top\Delta a
=-\eta\langle e_rc^\top,M_A\rangle_F.
\]

The F subscript denotes the sum of products of corresponding matrix entries. The gradient inner product between two events also factors into the input inner product times the error-signal inner product: \(\langle G_i,G_j\rangle_F=(c_i^\top c_j)(e_i^\top e_j)\). Input similarity alone does not determine update compatibility; e also depends on downstream computation and the actual target.

\(-\eta\langle e_rc^\top,M_A\rangle_F\) is a first-order compatibility proxy; \(\ell(a+\Delta a)-\ell(a)\) is the finite effect obtained by sending the new a through the native remaining network. A first-order expression cannot eliminate finite-step curvature effects. We therefore first checked that replaying the native remaining computation agreed with temporarily updating the full matrix, then expanded the measurement. This does not replay a complete AdamW training step and does not update the whole model.

**Measured result:** On the old S7 panel, mean finite CE decreased in all 16 source-domain × receiving-domain combinations. At the same time, about 43.97%–52.81% of events in each cell had a loss increase greater than 10⁻⁵ nat. Average help can coexist with harm to some events. Teaching example: if 60% of events improve by 0.02 and 40% worsen by 0.01, the average change is −0.008. The fact that 40% are harmed does not by itself justify separate training.

### 3.2 Why We Then Audited the SAE

The SAE expresses an activation as its decoder reconstruction plus a residual. Let α be the sparse encoding, D the decoder matrix, b the decoder bias, and ε the reconstruction residual. Freezing D and b before and after the update gives the exact relations:

\[
a=b+D\alpha+\varepsilon,\qquad
\Delta a=D\Delta\alpha+\Delta\varepsilon.
\]

A small static residual constrains ε at one endpoint. It does not imply that the change Δε between two nearby endpoints is small relative to Δa. When the TopK active set stays fixed and the encoder stays on the same affine branch, the encoding displacement is obtained by applying that set's encoder matrix E_S to Δa. Hence:

\[
D\Delta\alpha=D_SE_S\Delta a,\qquad
\Delta\varepsilon=(I-D_SE_S)\Delta a.
\]

Here TopK is 32, so D_SE_S has rank at most 32. It cannot equal I in every direction of a high-dimensional space. This is a linear-algebra limitation under the stated conditions, not proof that every actual update is inexpressible. When the active set switches, the encoding can also undergo a larger discrete change. The two components are generally not orthogonal, so their squared norms cannot be treated as explanatory shares that sum to 100%.

**Measured result:** Static relative squared reconstruction error was about 6.51%. With a stable active set, dynamic residual energy was about 0.979–1.000 times the true displacement energy; including active-set switches, the overall ratio reached about 48–82. The conclusion is that analysis of real updates must retain the native displacement and residual, rather than following only the encoding. It does not establish that SAEs are useless for other tasks.

### 3.3 Why the Prediction Checks Needed Several Controls

The initial finite-response prediction Q was about 1.41%, versus 2.26% for PCA320 and 2.53% for random projection320. Q measures the reduction in prediction error relative to a baseline, not the reduction in language-model loss. After a stronger prefix baseline, the SAE's incremental improvement for first-order responses was about 1.11% / 1.21%. Adding the actual target improved prediction by about 21%–24%; adding the SAE after the target brought no improvement.

These controls separately ask whether the result is only lexical and scale information, whether it is specific to SAE features, and whether the actual target carries much of the explanation. The actual target can be used in analysis and as training supervision. If the action must be selected before predicting that target, however, the decision input cannot look ahead to it.

**Check the source:** [Initial report](../1002/candidates/ntp_representation_update_channels/research_report.md) §3.1, §4.1, and §4.3–4.5.

**Hand calculation, final 20 minutes:** Let W be 2×3, c be 3×1, and e be 2×1. Write the shapes of G and Δa; derive the two loss expressions; then subtract the SAE identities at the two endpoints to obtain the dynamic residual. Also calculate a finite-step counterexample: initially w=0, the source loss is ½(w−1)², and the old loss is ½(w−0.1)². The two gradients are −1 and −0.1, with a positive inner product. A source step size of 0.5 moves w to 0.5, yet the old loss rises from 0.005 to 0.08. Explain why first-order compatibility does not guarantee help at this step size. Return to this section if you equate finite Δℓ with its first-order proxy unconditionally, or substitute 6.51% directly for dynamic error.

## 4. Session 3: Source Stability and Information Available Before the Target (50 Minutes)

### 4.1 Why We Changed the Source Samples

A “list of victims” produced by one fixed source update might reflect properties of that particular source batch. The first check swapped the two halves of F as sources while keeping receiving events fixed. Average help remained, but about 20.87%–36.36% of events resolved in both measurements changed sign. This means that a single observed effect cannot be named a stable task conflict.

A subsequent, stricter transfer check split F-half0 again into source A/B, fitted the readout on F-half1, and transferred the frozen readout to the other source. **This is a different split from the earlier swap of the two F halves.** Frozen-transfer Q was about 0.481% / 0.602%, showing a small amount of information. We then needed to separate what it was actually predicting.

### 4.2 What Exactly Was 99.02%?

For source A/B within the same domain, let the receiving event's responses be h_A and h_B. Define:

\[
\bar h=(h_A+h_B)/2,\qquad d=(h_A-h_B)/2,
\qquad h_A=\bar h+d,\quad h_B=\bar h-d.
\]

Apply the same transformation to prediction errors. The cross terms cancel in the sum of squares:

\[
\frac{(h_A-\widehat h_A)^2+(h_B-\widehat h_B)^2}{2}
=(\bar h-\widehat{\bar h})^2+(d-\widehat d)^2.
\]

In this check, 99.02% of the same-source absolute MSE improvement came from **the average of the A/B responses within each domain**; the source-difference component contributed very little. This does not mean that the four domains have 99.02% common knowledge, or that 99.02% of their update effects are identical. Reading out “this event is generally sensitive to updates” is different from reading out “which source action should this event choose?”

### 4.3 Why We Also Restricted Prediction to Earlier Prefixes

Two source effects evaluated on the same already observed target can be correlated because both depend on that target. Stable responses after observing the outcome do not automatically provide decision ability beforehand. When strictly earlier prefixes were used to predict the next eight targets, incremental SAE Q was only 0.0766% / 0.2892%, and ordinary projections were stronger. After removing amplitude along the selected common axis, 68.53% of the cross-half derivative-response inner product remained. That addresses a different question about structure observed after the outcome; both results can hold at once.

There is also an information issue: a=Wc may have discarded directions used by the update M. For a teaching counterexample, take W=(1,0), M=(0,1), and inputs c₁=(0,1), c₂=(0,−1). Both current outputs a are 0, but Mc is 1 and −1 respectively. The current output alone may therefore be insufficient to distinguish the effects of a particular update. This is an existence counterexample; it does not show that all such information is lost on actual inputs.

**Check the sources:** [Source-transfer addendum](../1002/candidates/ntp_representation_update_channels/source_transfer_addendum.md) §3–4 and [cross-domain response structure](../1002/candidates/ntp_representation_update_channels/domain_response_structure.md) §4–6.

**Closed-book task, final 10 minutes:** Explain 99.02% in no more than 150 Chinese characters, then state what is still missing between “reproducible on the same observed target,” “predictable from an earlier prefix,” and “deployable action selection.” Explicitly distinguish the source-batch split from the fitting/evaluation-record split.

## 5. Session 4: From Prediction to Decisions, Then to Learning (60 Minutes)

### 5.1 Decisions Require Relative Costs

Let h denote information available at decision time, a a candidate action, and C_a the actual cost observed after executing it. Risk-neutral selection should compare conditional expected costs:

\[
q_a(h)=\mathbb E[C_a\mid h],\qquad
a^*(h)\in\arg\min_a q_a(h).
\]

This is not argmin C_a after the actual target has been observed. An actual estimator also has estimation error. Teaching counterexample: when true costs are (0,0.1), predictions (1,1.1) have a large offset but select correctly; predictions (0.1,0) have lower MSE but select incorrectly. A common offset across actions does not change their ranking, whereas relative error can change the decision.

Write R_fixed for the ideal fixed-action risk, R_X for the ideal risk using only information X available before the target, and R_oracle for risk under an oracle that sees the outcome:

\[
R_{\rm fixed}-R_{\rm oracle}
=(R_{\rm fixed}-R_X)+(R_X-R_{\rm oracle}),
\qquad R_{\rm fixed}\ge R_X\ge R_{\rm oracle}.
\]

These are ideal population quantities; the action selected from finite FIT data is not treated as the known population optimum. Large oracle headroom may largely reflect the additional information obtained by observing the actual outcome. It does not guarantee that the first term is positive. Failure of the current fitted estimator does not directly estimate R_X either.

### 5.2 The Router and Experts Need Not Preserve the Same Information

Suppose the input contains a sign S and a numerical value ξ, the target is Sξ, and two experts output ξ and −ξ. The router needs only S to select correctly, while an expert still needs ξ to perform the computation. A routing representation may compress details irrelevant to selection without contradicting experts' use of complete inputs. With finite samples, worse performance by a full-input estimator also does not prove that the complete input contains less information.

When actual action selection was evaluated on the old S7 cache, none of the 16 pooled policies stably beat the FIT-fixed action. For example, x-PCA64 gained +13.94 micronats relative to the fixed action, with an interval crossing zero, but +193.62 micronats relative to within-category random allocation, with a positive interval. The new panel therefore explicitly added a stronger common action and re-established controls for model identity, records, and finite costs. This was a choice of further diagnostic, not the only possible route.

### 5.3 Why Fixed-Library Failure Does Not Establish Failure of Future Specialization

Teaching example: the input is only an equiprobable sign S, the target is always 1, and two experts without biases both output θ_eS, initially with θ_e=0. At this point, selecting either gives loss 1/2, so selection offers no advantage. Predetermine allocation by input sign and let each group learn from its own conditional mean gradient:

\[
\theta_\pm(t+1)=(1-\eta)\theta_\pm(t)\pm\eta,
\quad \theta_\pm(t)=\pm[1-(1-\eta)^t],
\quad R_t=\tfrac12(1-\eta)^{2t}.
\]

For 0<η<2, separate learning creates useful differences that did not previously exist. A single shared parameter stays at 0 under the symmetric population gradient. The limitations are explicit: allocation is predetermined, the function class is restricted, conditional step sizes are compared, and parameter cost is omitted. A single expert with a bias could solve this problem. The example does not prove that a standard MoE will learn specialization.

**Check the sources:** [Sharing and routing report](../1002/candidates/ntp_representation_update_channels/sharing_routing_report.md) §4.3–4.4 and §5.3, and [understanding update](../1004/cognition_update.md) §2.

**Hand calculation, final 15 minutes:** Compute the MSE and selected loss for both sets of predictions. Set η=0.5 and calculate the experts' parameters and risk after two learning rounds. Reference: θ_±=±0.75, risk 0.03125. Explain aloud why this does not conflict with the current negative fixed-action result.

## 6. Session 5: Why the New Results Look Contradictory but Are Consistent (70 Minutes)

### 6.1 First Identify the Three Sets of Research Materials

| Material | Identity and operation | What must not be conflated |
|---|---|---|
| October 2 old panel | One S7 checkpoint, itself trained for 33B tokens; the old receiving panel | Not a 21B model; the strong fixed action among the old four actions is not the new common action |
| New fixed-library panel | Three exact 33B-token states: Dense, fresh S7, and SALL; new records and a common action | No new MoE was trained; this is not a parameter-count experiment |
| Six capacity arms | Randomly initialized eight-layer small models; mixed training followed by sequential domain training | 0/12 formal trajectories; fixed-library results cannot supply the missing training comparison |

Sources A/B in the new panel each produce four domain actions and one common action. There are 512 FIT records for fitting and 1,024 DEV records for evaluation, with 16 positions per record. The common action is formed by **averaging raw gradients first, then normalizing that average separately**. Teaching example: for raw gradients (3,0) and (0,1), the unit direction after averaging is (3,1)/√10. Normalizing each first and then averaging instead gives a direction along (1,1). Nor can the average loss of four actions be treated as the common action's loss.

### 6.2 Three Controls Answer Three Different Questions

| Control | Construction | Question it answers |
|---|---|---|
| No update | Loss of the original model | How does this intervention compare with leaving the model unchanged? |
| FIT-fixed action | Select one action using FIT only, then use it on every DEV event; here FIT selected the common action | Is the adaptive policy worth adopting instead of a simple available scheme? |
| Usage-matched random allocation | Preserve the policy's action proportions but remove the correspondence between inputs and choices | Does input matching have value? This is not uniform random allocation |

Let L_C, L_π, and L_rand denote the average costs of the common action, the policy, and usage-matched random allocation. Then exactly:

\[
L_C-L_\pi=(L_{\rm rand}-L_\pi)-(L_{\rm rand}-L_C).
\]

A policy may allocate a relatively costly mixture of actions more intelligently, yet still be worse than always using the common action. Teaching values: L_C=1, L_π=1.02, L_rand=1.05 give matching gain 0.03 and adoption gain −0.02. The identity itself is not a new mechanism discovery.

**Measured result:** All 92 pooled cross-source conditions beat global usage-matched random allocation and lost to the FIT-fixed common action; their conditional intervals were correspondingly all positive and all negative. The 92 conditions share models, records, and action libraries, so they are not 92 independent replications. All 92 pooled same-source conditions also lost. Gains were all positive within FIT and all negative on same-source DEV. Thus “changing the source caused failure” is insufficient on its own. The result is compatible with limited generalization, but does not uniquely identify overfitting, composition differences, or unpredictable target variation.

### 6.3 Why We Added a Within-Category Control

Global matching gains might arise simply because different categories prefer different actions overall. To test this explanation, preserve the policy's action usage within each domain/category and compute the expected cost of random allocation there. No refitting or new LM execution is required.

**Measured result:** The within-category matching intervals remained positive for all 184 pooled same-/cross-source conditions, while intervals relative to the common action remained negative. In the Dense base-feature A→B example, global matching gain +133.49 micronats equals category composition +40.15 plus within-category matching +93.34, yet the gain relative to the common action is −386.77. Coarse categories therefore do not explain all matching association, but adopting the current policy still does not pay off. A positive overall weighted residual does not mean that each individual category has a positive residual.

The switching audit further asks why departures from the common action lose value. Let S indicate a switch and D the additional cost relative to the common action. Because D=0 without a switch, E[D]=P(S)E[D|S]. In the Dense A→A example, about 75.46% of events switch. The prediction says each switch saves 1,467 micronats; the actual average extra cost is 352 micronats. About 49% of switches do improve loss. The issue is that the probabilities and magnitudes of gains and losses still sum to a loss, not that every choice is wrong.

### 6.4 Why We Checked Amplitude on Held-Out FIT Folds

The original estimator was too optimistic within FIT. We therefore shrink its input-dependent predictions toward action means and ask whether using the same information more conservatively helps. This check contains only five fixed update actions, with no no-update action: 12 selections = 3 models × 2 input families × 2 source libraries, and the 24 evaluations multiply this again by same-/cross-source evaluation. The original 92 conditions also include other input families and action sets containing no update, so the two grids' “success proportions” cannot be compared. Let μ_a be action a's mean on the training fold and q̂_a its input-dependent prediction:

\[
\widehat q_a^{(\alpha)}=\mu_a+\alpha(\widehat q_a-\mu_a),
\qquad\alpha\in\{0,0.1,0.25,0.5,1\}.
\]

Split FIT into four folds by **whole record**, fit on the training folds, and evaluate the actual selected costs on the held-out fold. Choose α from those readings only. Within a fold, α=0 selects the action with the best mean on that training fold, and α=1 uses predictions refitted for that fold. After freezing the selection, final DEV evaluation uses the original full-FIT means and predictions: at this point α=0 returns exactly to the common action, and α=1 reproduces the original policy event by event. Splitting a record's 16 positions across folds would break record-level separation. Bootstrap resampling likewise keeps those 16 positions together, and each within-group control recomputes frequencies in every resample.

**Measured result:** Eleven of 12 selections chose 0; only SALL/base/A chose 0.1. All 24 pooled same-/cross-source evaluations improved over the old policy, but 22 merely used the common action. The other two gains relative to common were −6.23 and −19.72 micronats. The first interval crossed zero and the second was negative. Improving a poor policy is not the same as finding a stronger adaptive policy. The only slightly positive point among 96 nonzero amplitudes was not chosen on FIT; it cannot be selected retroactively from DEV.

This locates the failure more precisely: the input-dependent components of the current two estimator families are mostly not worth retaining after the held-out-fold check. It does not establish that all prefix information has zero ideal value. DEV had already been exposed, so this remains a post-hoc diagnostic rather than new confirmation.

**Check the sources:** [New-panel Summary](../1002/candidates/ntp_representation_update_channels/probe_33b_summary.md), [within-category Summary](../1002/candidates/ntp_representation_update_channels/probe_33b_group_summary.md), and [amplitude Summary](../1002/candidates/ntp_representation_update_channels/router_shrinkage_summary.md). Each has a corresponding Detailed record.

**Closed-book task, final 15 minutes:** Recalculate 0.03−0.05=−0.02 and 133.49=40.15+93.34. Explain why 11/12 selections falling back to common both improve the old policy and fail to establish adaptive superiority. Write one sentence about interval scope: conditional on the models, sources, and fitted estimators; record resampling does not cover the entire source population, does not refit, and has no multiple-comparison correction.

## 7. Session 6: Why Sharing Can Help, and Why Private Learning Can Also Help (65 Minutes)

### 7.1 First Derive a Learning Model with Explicit Conditions

Fix a common initialization and a grouping K based on information available before the target. Let p_k be group probabilities, G_k group mean gradients, and G=Σp_kG_k the population mean. Shared parameters update by −ηG; each private copy updates by −ηG_k. Temporarily ignore copying costs and assume ordinary SGD, equal conditional step sizes, and smooth risks. First-order risk improvements are η‖G‖² and ηΣp_k‖G_k‖² respectively, so:

\[
R_{\rm shared}-R_{\rm private}
=\eta\sum_kp_k\|G_k-G\|^2+O(\eta^2).
\]

The derivation only requires expanding the square and using Σp_k(G_k−G)=0. The opportunity comes from **different average learning demands across groups**, not from all single-event gradient noise. If the target is randomly positive or negative while every prefix is identical, gradients can oppose each other after observing the target, yet no permitted prefix-based grouping has different conditional means.

### 7.2 Finite Data Can Change Which Scheme Is Better

Replace G_k with an estimate. Each group has n_k samples, mutually independent both within and across groups, with gradient mean μ_k and covariance Σ_k; group risks are exact quadratic functions with the same positive semidefinite curvature B. Let μ=Σp_kμ_k and define mean-gradient heterogeneity V, curvature-weighted heterogeneity V_B, and the additional noise cost of separate estimation N_B:

\[
V=\sum_kp_k\|\mu_k-\mu\|^2,\quad
V_B=\sum_kp_k(\mu_k-\mu)^\top B(\mu_k-\mu),\quad
N_B=\sum_k\frac{p_k(1-p_k)}{n_k}\operatorname{tr}(B\Sigma_k).
\]

The noise covariance of the shared mean contains p_k², whereas the weighted noise in private risk contains p_k. Their difference produces p_k(1−p_k). Substitution into the expected quadratic risk gives the exact relation:

\[
\mathbb E[R_{\rm shared}-R_{\rm private}]
=\eta V-\frac{\eta^2}{2}(V_B+N_B).
\]

For a hand calculation, use two equiprobable groups with means ±1, variance 4, n samples per group, and B=η=1. Then V=V_B=1 and N_B=2/n, giving a difference of 0.5−1/n. At n=1 it is −0.5, so sharing is better; at n=4 it is +0.25, so private learning is better. The same true group differences can lead to different outcomes at different sample sizes. Repeated token exposure is not the same as additional independent samples.

This is not a grouping threshold already validated in the current LM. Different curvatures, correlated samples, choosing groups on the same data, AdamW, or global normalization all change the derivation. In particular, private gradients in the actual mixed batch include p_k=1/4, whereas the equation compares equal conditional step sizes. It cannot be applied directly to the six-arm endpoints.

### 7.3 What Does the Common Structure Actually Change?

A common module may save repeated storage or pool data to reduce estimation error; these are distinct from expanding the function class. In a linear residual example, the parallel form is I+C+E_d and the serial form is (I+E_d)(I+C). If I+C is invertible, setting Ẽ_d=E_d(I+C) reparameterizes the same function while preserving the corresponding matrix rank. The appearance of a cross term does not automatically establish greater expressivity. Finite nonlinear networks require a separate check, and equivalent function classes do not guarantee equivalent learning dynamics.

In the actual six-arm design, z is the FFN input, C the common FFN, E_d the private FFN selected by known domain, and T the remaining shared trunk:

| Arm | Main construction/control | What it can distinguish |
|---|---|---|
| common_parallel | C(z)+E_d(z) | Common and private channels operating together |
| common_serial | C(z)+E_d(z+C(z)) | Changes to expert input and gradient paths; depth is also a rival explanation |
| private_active | Copy the C channels into each domain, matching parallel's initial function and active width | Untying shared channels, with 4,718,592 additional stored parameters |
| private_total | Private scheme matched by total parameter count | A comparison at similar storage, not necessarily equal active computation |
| dense_active | Dense matched by active FFN width | The same nominal active-computation coordinate |
| dense_total | Dense matched by total parameter count | The same storage coordinate, with greater nominal computation |

No pair controls all resources, update histories, and structures simultaneously. Nominal MLP multiply-add counts are not actual speed or memory usage. The private arms still share T; they are not four independent models. Freezing old expert parameters does not guarantee that their inputs remain unchanged, let alone their outputs. The six arms can compare complete schemes, but one endpoint cannot uniquely attribute a difference to “reuse of common knowledge.”

**Check the sources:** [Sharing and routing report](../1002/candidates/ntp_representation_update_channels/sharing_routing_report.md) §4.4–4.6 and §5.6; [capacity report](../1002/candidates/ntp_representation_update_channels/capacity_report.md); and, for the long derivations, [mathematical notes](../1002/candidates/ntp_representation_update_channels/sharing_routing_mathematics.md).

**Hand calculation and explanation, final 20 minutes:** Derive the first-order gain from the variance identity, then calculate 0.5−1/n. Without the document, explain why private_active is needed, why matching the initial function still does not uniquely isolate a mechanism, and why nominal computation cannot replace measured costs.

## 8. Session 7: How Future Training Changes Today's Help (60 Minutes)

### 8.1 Adam's State Is Part of the Learning State

AdamW stores not only parameters but also exponential first- and second-order gradient statistics. Shared parameters aggregate gradients before squaring; private copies square their own gradients and accumulate them separately. Under fixed external gradient streams, synchronized counts, equal decay, and zero initialization, let the common gradient be ḡ=Σp_dg_d. Coordinate by coordinate:

\[
\sum_dp_dg_d^2-\bar g^2
=\sum_dp_d(g_d-\bar g)^2.
\]

Multiplying each time point by the same exponential weight and summing gives “the weighted average of private second-order states minus the common second-order state equals the exponentially weighted history of gradient differences.” Teaching example: for equally weighted gradients +1 and −1, the common gradient is 0 and its square is 0; each individual square is 1. A smaller second-order state does not imply a better effect: the numerator, epsilon, clipping, and active-step counts also affect the update.

Actual private gradients in mixed batches also have a 1/4 scaling. Under ideal fixed scaling, this can cancel in Adam's first-/second-order normalization, so it is not a quarter step size. Actual counts and trajectories differ; the external-gradient identity above cannot directly be treated as an equality between two real checkpoints.

### 8.2 Hand-Calculate an Exact Example of Immediate Help and Future Harm

This is a **mathematical teaching example, not a language-model measurement**. Two parameters begin at w=(0,0), with old-task risk L_old(w)=½(w₁+w₂−1)², hence risk 0.5. The source loss is ½[(w₁−2)²+(w₂+1)²]. One gradient step with learning rate 0.1 gives w=(0.2,−0.1), making the old risk ½(−0.9)²=0.405.

Next, both the branch that accepted the source update and the branch that rejected it take one learning-rate-1 step on the same future loss L_future(w)=½(0.9w₁²+0.1w₂²):

\[
w'=(0.1w_1,0.9w_2).
\]

The accepting branch becomes (0.02,−0.09), with old risk ½(−1.07)²=0.57245. The rejecting branch remains at 0, with old risk 0.5. Both directions contract stably. Future training removes the helpful coordinate faster while retaining more of the harmful coordinate. Immediate advantage −0.095 therefore becomes future disadvantage +0.07245. If optimization of this future loss continues indefinitely, both branches converge to 0. The counterexample concerns a finite evaluation time.

It refutes the unconditional claim that positive transfer now guarantees positive transfer later. It does not show that the current LM exhibits this mechanism.

### 8.3 The General Relation Follows from the Chain Rule on the Complete State

Fix coordinates for the same model, and let s include the complete state, including parameters and optimizer moments. Fix future data, randomness, and a common smooth branch. Write one future step as s_{u+1}=U_u(s_u) and the final risk as R(s_N). After propagating a small current perturbation δs:

\[
\Delta R_N=\nabla R(s_N)^\top
DU_{N-1}\cdots DU_t\,\delta s+O(\|\delta s\|^2).
\]

Future updates reweight today's directions. Hard routing, clipping boundaries, and different counts limit this linearization; parameters from different architectures cannot simply be subtracted. Preserving the first-order sign for every perturbation in the whole space requires the future sensitivity propagated back to the current state to be a positive multiple of current sensitivity. Stable contraction alone does not ensure this. If the future program is unknown, expected subsequent utility still has to be estimated from the permitted information. A derivative computed after the outcome is not an already deployed decision signal.

### 8.4 Which Losses Must Actual Training Read Out?

Each contracted trajectory has 512 mixed-training steps followed by four stages of 1,024 steps each. Shared parameters participate in 4,608 steps and each expert in 1,536. The learning rate decays with the global step, and the ratio of summed learning rates in the first versus last single-domain stage is 6.608. This is not 6.608 times as much learning. The two seeds are coupled to domain orders, so seed and order effects cannot be estimated independently either.

For the same domain, let L_M, L_pre, L_post, and L_F be its losses after mixed training, before its own stage, after its own stage, and at the end:

\[
L_M-L_F=(L_M-L_{\rm pre})+(L_{\rm pre}-L_{\rm post})
-(L_F-L_{\rm post}).
\]

The three terms are transfer before the domain's own stage, acquisition during that stage, and subsequent forgetting. Teaching values 2.0, 1.8, 1.2, and 1.4 give net improvement 0.6=0.2+0.6−0.2. The first domain has no prior-stage transfer and the last has no subsequent forgetting. These zeros arise from the order of stages, not from superior capability. Absolute losses and these components must be compared together.

**At the final archived cutoff:** Four-GPU job pt-scl8ek3y passed the hardware check and all 42 resume checks for the six seed1003 arms. For seed1004, however, 1 of 524,288 elements in the initial FP32 equivalence check failed the original tolerance. Qualification failed and formal training did not start. The amended qualification conditions passed CPU checks. GPU recovery job pt-c44kwvx3 remained pending, was then stopped, and was verified as SUSPENDED. There were 0/12 formal trajectories and 0/18 endpoint mechanism readouts. No architecture won. Numerical qualification failure and queue waiting are not scientific counterevidence.

**Check the sources:** [Understanding update](../1004/cognition_update.md) §4–7 and [final status receipt](../1004/evidence/final_window_status.json).

**Closed-book task, final 15 minutes:** Independently calculate 0.405 and 0.57245 and explain which coordinate causes the change. Write the retention identity. Report training status in two sentences without turning partial Smoke passes into completed formal training.

## 9. Session 8: Evidence Checks, Closed-Book Questions, and the Next Decision (65 Minutes)

### 9.1 Three Evidence Checks (15 Minutes)

For each check, follow “claim → Summary method → number or receipt → permitted conclusion.” Do not judge credibility by the number of files.

1. **Matching and adoption value.** Compare the [within-category Summary](../1002/candidates/ntp_representation_update_channels/probe_33b_group_summary.md), [understanding update](../1004/cognition_update.md) §2, and [independent recomputation receipt](../1004/evidence/group_decomposition_independent_audit.json). Check 133.49, 40.15, 93.34, and −386.77. Explain why the two controls produce opposite signs. Intervals resample whole records; 184 rows are not independent replications.
2. **Amplitude check.** Compare the [amplitude Summary](../1002/candidates/ntp_representation_update_channels/router_shrinkage_summary.md) and [independent readout audit](../1004/evidence/crossfit_readout_independent_audit.json). Check 12 selections, 11 at zero, 24 evaluations, and 22 equal to common. Confirm that α was not reselected on DEV. Check the two comparison baselines for “improved over the old policy” and “beat the common action.”
3. **Completion.** Open the [final-window receipt](../1004/evidence/final_window_status.json) and check the two job IDs, cutoff time, and formal-trajectory inventory. Explain aloud what is missing between “computational/implementation qualification” and “formal results.” Then inspect the provenance boundary in the [amplitude Detailed record](../1002/candidates/ntp_representation_update_channels/router_shrinkage_detailed.md), confirming that a small JSON record does not contain all raw arrays.

All decisive numbers and derivations are explained in the text. The Git delivery includes text and small audit records. Figures, CSV files, raw arrays, checkpoints, and external execution directories are not supplied by cloning this repository. Manifests record their sources and hashes; they do not mean that every referenced file is in Git.

### 9.2 Twelve Closed-Book Questions (20 Minutes to Answer, 10 to Correct)

Score each question as 0 for an incorrect answer or inability to explain, 1 for a correct conclusion with incomplete conditions, or 2 for a correct conclusion, reason, and boundary. **20/24 with none of the critical misreadings below** is a suggested target for tonight's explanation. This is a learning check, not scientific certification of mastery. Critical misreadings include treating Q as CE improvement, treating an outcome-aware oracle as routing before the target, equating beating random allocation with beating common, treating a mathematical example as an LM result, and treating an unrun experiment as a negative result.

| Question | Reference answer points; hide this column before answering |
|---|---|
| 1. Why are activation frequency and gradient sensitivity insufficient? | Neither gives the actual update displacement and its finite loss effect; the source-gradient → receiving-displacement → native-loss chain is needed. |
| 2. Which update relation is exact, and which is approximate? | Under a fixed interface, Δa=−ηM_Ac is exact; Δℓ≈e_rᵀΔa is first order. State that only the specified W is updated. |
| 3. Why does 6.51% static SAE error not guarantee dynamic fidelity? | Δa=DΔα+Δε; small endpoint errors do not guarantee a small residual change. Even the stable-active-set map need not equal I. |
| 4. What object does 99.02% concern? | The contribution of within-domain average A/B responses to improvement in absolute prediction MSE; not a proportion of common domain knowledge or action utility. |
| 5. Why can an outcome-aware oracle do well while prefix-based selection has no value? | Total headroom contains value available before the target plus the extra advantage of seeing the actual outcome; the first term can be zero. |
| 6. Is it contradictory for a policy to beat usage-matched random allocation but lose to common? | No. Matching gains can be smaller than the extra cost of its action mixture relative to common. The common action averages raw gradients first. |
| 7. Why split/bootstrap by whole record, and why not choose α on DEV? | Positions within a record are dependent; preserve record separation and the sampling unit. DEV is already used for evaluation, and repeatedly selecting from it does not create new confirmation. |
| 8. What does 11/12 selecting α=0 establish? | The current two estimator families and grid mostly favor a return to the means. This neither proves zero value for all information available before the target nor establishes adaptive superiority. |
| 9. Why can future specialization matter when current actions are identical? | Allocation during training changes future parameters. Give the sign-expert example and state the restricted-function-class/predetermined-grouping conditions. |
| 10. Why can the SGD variance gain not directly predict the six-arm outcome? | It assumes conditional step sizes, fixed groups, and, for the quadratic result, common curvature and independent data. Actual AdamW, global normalization, counts, and resources differ. |
| 11. Why can immediate help reverse, and why is final loss alone insufficient? | Future training preserves different directions differently. Calculate the counterexample and decompose net change into prior-stage transfer + acquisition − forgetting. |
| 12. What evidence is most missing next? Can architectures be ranked now? | Qualified complete shared/private trajectories and resource measurements are missing. Formal completion is 0/12, so there is no winner. The researcher confirms the concrete next decision. |

If you fall below the suggested target, do not reread everything. Map each wrong answer to Sessions 2–7, redo an example, and answer in new words. Use the remaining time tonight to correct critical misreadings first.

### 9.3 What to Do Next (20 Minutes)

**AI suggestion: prioritize completing the original shared/private learning comparison, rather than adding more router tuning on the same exposed DEV.** The researcher is concerned with learning and retention under limited resources. Fixed-library diagnostics have already produced a clear, bounded negative utility result, while the decisive evidence about actual learning allocation is still missing. This is a priority suggestion, not scientific confirmation or new run authorization.

| Uncertainty to resolve | Next concrete check/comparison | What result would change our understanding? |
|---|---|---|
| Is the implementation qualified? | First inspect existing jobs and durable outputs; complete exact GPU qualification for both seeds and all six arms under the recorded amended conditions; do not duplicate existing submissions | Passing restores technical qualification to continue execution; failure is still an implementation issue |
| Which complete shared/private scheme is better at the specified budget? | Complete the existing 12 frozen trajectories within valid authorization; with limited resources, first ensure complete parallel/private_active pairs, then complete the other resource controls | If the shared scheme improves absolute loss and retention at the specified budget, it supports benefits within this contract; if the private scheme is better, it weakens that shared-benefit claim. Unrun conditions, qualification failure, or insufficient readings remain unknown. Interpret mixed results using domain × stage outcomes and measured costs; the researcher still needs to confirm the practical threshold |
| If outcomes differ, which explanations remain possible? | Read the already designed C/T rollbacks, expert swaps, and serial-path diagnostics | These constrain specified endpoint functional explanations but cannot alone reconstruct the full causal training path |
| What if the research instead follows selection information available before the target? | First specify a new candidate estimator, strong fixed control, permitted information, and prospective unexposed evaluation; do not choose a winner on old DEV | Beating common supports that selector's net utility; failure constrains only the tested contract |

The researcher specifies the scientific route, practical effect scale, resource weights, and whether to adopt an architecture. Existing authorization remains valid only within its original scope; today's study and document submission do not add run permission.

On the final page, complete these six sentences, using one to three lines each:

1. My current question is …; the evaluation time and resource constraints I care about are ….
2. What I can now state from evidence is …; its most direct evidence is at ….
3. I still cannot claim …, because … is missing.
4. I choose to prioritize … and defer …, because ….
5. The smallest distinguishing comparison is …; under support / non-support / insufficient evidence, I would update my understanding by ….
6. The scientific judgments I need to confirm are …; execution scope and scientific judgment are recorded separately.

Finally, speak for 10 minutes without the material: **why the work moved from representations to update effects, why it moved from prediction to selection, why selection is still insufficient to answer learning allocation, and why complete acquisition–retention evidence is now needed.** Independently connecting these four “whys” is today's test of whether you have built an understanding that can support further research.

## 10. Return by Question Instead of Getting Lost Among Files

| Where you are stuck | Open first |
|---|---|
| Why each step was taken at the time, and in what order | [Research process](../1002/candidates/ntp_representation_update_channels/research_process.md), at the time interval corresponding to this guide |
| The initial relation between actual updates and SAE analysis | [Initial report](../1002/candidates/ntp_representation_update_channels/research_report.md) |
| Source changes and information available before the target | [Source addendum](../1002/candidates/ntp_representation_update_channels/source_transfer_addendum.md) and [domain structure](../1002/candidates/ntp_representation_update_channels/domain_response_structure.md) |
| Conditional risk, grouping gains, and the distinction between representation and learning | [Main stage report](../1002/candidates/ntp_representation_update_channels/sharing_routing_report.md) §4; open [mathematical notes](../1002/candidates/ntp_representation_update_channels/sharing_routing_mathematics.md) only when you need the full proof |
| How the new-panel numbers were measured | [33B Summary](../1002/candidates/ntp_representation_update_channels/probe_33b_summary.md) and its corresponding Detailed record |
| Latest understanding, amplitude/within-category checks, and final execution status | [Understanding update](../1004/cognition_update.md); it is later than the [daily summary](../1004/daily_summary.md) and early execution snapshots in the stage report |
| How the six arms were designed, and what remains unrun | [Capacity report](../1002/candidates/ntp_representation_update_channels/capacity_report.md) and [Protocol](../1002/candidates/ntp_representation_update_channels/protocol.md), with status checked against the latest receipt |
| How this relates to external research | [Literature comparison](../1002/candidates/ntp_representation_update_channels/sharing_literature_20261004.md); choose the group relevant to your current question first, rather than requiring all 17 papers today |

The old panel defined event harm as ΔCE>10⁻⁵ nat; the new panel's frozen harm_fraction used ΔCE>0. Their harm proportions cannot be compared directly. Historical snapshots retain their meanings at the time. This guide does not change earlier formal conclusions, relocate the Anchor, create a new Focus, or close the question.
