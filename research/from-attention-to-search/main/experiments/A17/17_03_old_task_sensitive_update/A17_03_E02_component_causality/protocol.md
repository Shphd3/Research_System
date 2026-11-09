# Protocol: A17_03_E02 — Component causality at a fixed old-task state

[中文](protocol_cn.md)

## 0. Approval snapshot

Document status: `APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_AND_RESULT_ANALYSIS`. Pre-run registration date: 2026-10-11 UTC / 2026-10-11 Asia/Shanghai; actual freeze time is recorded by the run manifest. Execution state at registration: `NOT_RUN`. Scientific mechanism and question closure: `Unknown`. Registered run: `causal_20261011T020424Z`.

On 2026-10-11 the researcher explicitly delegated deeper analysis, necessary experiments on four reserved H100 GPUs, and a meeting report without further approval. This authorizes the bounded operational choices below. It does not mean that the researcher confirmed a mechanism or that a favorable result is expected. A–G are `USER_DELEGATED_OPERATIONAL_CHOICES`; cross-block consistency has been audited. Implementation, Smoke, separate Full submission, supervision and result analysis are in scope; publication and Git changes are not implied.

The [component-causality sub-Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_03_old_task_sensitive_update/subanchors/17_03_01_component_causality_anchor.md) defines this round. It inherits the [old-task-sensitive-update Focus](../../../../focus/focus_old_task_sensitive_update.md), rather than creating another question. The [E01 result](../A17_03_E01_sequential_projection/summary.md) remains a separate sequential-training result.

Purpose: determine whether a fixed-state restriction effect comes from deleting estimated old-sensitive update components, amplifying the remainder, or is not present at this initial state. Role: **root-cause audit**. Primary evidence: signed new-development-CE deletion and amplification gains, accompanied by old-rule margin and full-vocabulary accuracy costs. Minimal setup: six saved old endpoints, three fixed new-source batches each, seven directions, five frozen scales. Full has 630 nonempty intervention cells. Smoke has 140 cells and independent-process replay. These are parameter interventions and evaluations, not training trajectories.

Supporting evidence identifies a qualified finite contrast at the registered state. Opposite or absent primary contrasts weaken the corresponding local explanation. Numerical or restoration failure makes affected evidence insufficient. No local outcome proves a 100-step mechanism, functional modules or expert utility.

## 1. Terminology and definitions

A **case** is one old endpoint from seed 29, 43 or 71, with old FIRST/new LAST or the reverse. A **source batch** contains 20 new-rule training records whose average answer CE defines a single update. A **cell** is an independent intervention at that saved endpoint, using one source batch, direction and scale. Cells do not follow one another as training steps.

For a prefix, let the correct answer probability be \(p_y\), the opposite-rule answer probability be \(p_o\), and the correct-versus-opposite margin be \(m=\log(p_y/p_o)\). Correct answers are distinct because all three list words differ. The answer CE, in nat per answer, decomposes exactly as

\[
\ell=\ell_{access}+\ell_{choice}
=-\log(p_y+p_o)+\log(1+e^{-m}).
\]

`access` is the sub-Anchor's `mass` term: probability assigned to the two possible rule answers. `choice` measures their relative selection. These are output objectives; the names do not assert separate internal functions.

For a paired list, let \(m_F,m_L\) be the correct-answer margins under FIRST and LAST. Define \(b=(m_F+m_L)/2\), \(c=(m_F-m_L)/2\), and \(h=c\) for new FIRST or \(h=-c\) for new LAST. Thus \(m_{new}=b+h\), \(m_{old}=b-h\). Here \(b\) is rule-prompt differential response, and \(h\) is the prompt-averaged bias toward the new answer. The former is previous \(S/2\), not a new discovery. Both margins increase iff \(\Delta b>|\Delta h|\); both pair decisions are correct iff \(b>|h|\), with strict ties excluded. Full-vocabulary correctness additionally depends on other tokens.

## 2. Anchor alignment

This tests sub-Anchor H1's local deletion/amplification explanation and H2's measured bias-versus-rule-response occurrence. It does not revise E01's absence of ordinary CE forgetting. The parent unknown is why shared updates help particular predictive requirements while harming others. The three analysis steps are: decompose existing outputs descriptively; intervene on fixed-source parameter components; interpret qualified finite contrasts and their bounds.

## 3. Tested hypotheses

H1 candidate: deleting sensitive components itself improves new development CE; amplification may add benefit. Its primary distinguishing comparison keeps the retained component unchanged while removing the sensitive component, then separately amplifies that same remainder.

H2 candidate: an update can increase rule-prompt response while increasing new-answer bias more, reducing old-rule margin. The inequality is an algebraic fact; whether these interventions produce it, on which lists, and with what CE/accuracy effects is empirical. Record \(\Delta b,\Delta h\) and per-list outcomes rather than treating the identity as a discovery.

## 4. Rival explanations

Amplification alone may produce the local benefit. The initial fixed state may show no corresponding advantage, leaving the sequential endpoint explanation unresolved. Probability assigned to the two answers may improve without their relative choice improving. Other list words or vocabulary tokens may cause an accuracy loss that the two-answer comparison misses. Random codimension removal is a generic geometric control, but its removed gradient energy is not matched to the sensitive basis. Access/choice gradients can overlap geometrically; they are not independent parameter modules. All these alternatives remain explicit in interpretation.

## 5. Data construction and provenance

Use registered `data_a17_list_rules_v1`: train 4,000 records (2,000 ordered lists, each with both rules); dev 800 records (400 paired lists). Each dev rule has 200 `order_new` and 200 `combination_new` records. Train/dev ordered lists are disjoint; the completed old training epoch supplies the intended seen-content status for `order_new`. Test remains unread. Dev was exposed in E01; this is a frozen new intervention on exposed development data, not blind confirmation.

Use the original E01 case ordering and `new_order`. Source batches are slices `[0:20]`, `[20:40]`, `[40:60]`, not selected by measured effect. Smoke uses only the first batch. Smoke dev uses the first ten sorted pair IDs in each panel, then preserves original dev row order: 20 pairs, 40 answers. Freeze exact record IDs, rules, panels, tokenizer encodings and payload hashes. Evaluate the same source 20 records separately from dev in every cell; never merge source and dev losses.

Required inputs: `model_qwen3_0p6b_base_official_a5`, `tokenizer_qwen3_0p6b_base_official_a5`, `data_a17_list_rules_v1`, `representation_a17_03_sequential_20261010t171602z_native_and_subspaces`, and the six checkpoint-family IDs formed by `adapter_a17_03_full_sequential_20261010t171602z_` plus `s29_first_to_last_old`, `s29_last_to_first_old`, `s43_first_to_last_old`, `s43_last_to_first_old`, `s71_first_to_last_old`, `s71_last_to_first_old`. Use each old update-100 member. Perform a fresh strict registry check and hash the actual loaded members; older access receipts are insufficient.

## 6. Learning task and permitted supervision

The complete prefix includes the visible FIRST/LAST rule, the three distinct list words and the answer marker. The model predicts the next answer token. Only the oracle answer and opposite-rule answer IDs enter the defined losses; answers are not appended to the prefix. The data, 20-word pool and tokenizer follow E01. No SAE, router, expert, replay objective or additional labels are introduced. `access` and `choice` use the exact native full-vocabulary logits, not detached probabilities or a separately normalized proxy.

## 7. Model, architecture and frozen variants

Load official Qwen3-0.6B Base, then restore the registered old matrix. Only `model.layers.27.self_attn.o_proj.weight`, shape [1024, 2048], is perturbed. Use native full FP32 forward, evaluation mode, fixed attention backend and deterministic settings recorded with library versions. All other parameters remain frozen. Beginning/end frozen hashes, parameter version counters and the exact trainable-name audit qualify this boundary.

Load the original case's rank-16 old-sensitive basis \(Q\) and rank-16 random basis \(R\), with orthonormal rows; do not refit or select them on the new results. This preserves the original estimated geometry. Source identities, basis hashes and orthonormality are recorded. Sensitivity is unsigned and incomplete.

## 8. Objective and displacement construction

At the saved state, compute average source gradients \(g=\nabla L_{CE}\), \(g_a=\nabla L_{access}\), \(g_c=\nabla L_{choice}\), each normalized by exactly 20 valid answer tokens. Use the original manual-SGD rule with learning rate 0.01 and clip norm 1. For nonzero \(g\), define \(\eta_{eff}=0.01\min(1,1/\|g\|)\) and \(d=-\eta_{eff}g\). There is no momentum, decay, schedule, optimizer history or cumulative update.

Construct \(d_{in}=Q^\top Qd\), \(d_{out}=d-d_{in}\), and \(d_{outnorm}=d_{out}\|d\|/\|d_{out}\|\). Construct the random remainder and normalize it to \(\|d\|\) using \(R\). Access and choice directions are \(d_a=-\eta_{eff}g_a\) and \(d_c=-\eta_{eff}g_c\), using the **same** CE-derived coefficient without separate clipping or normalization. Hence \(d_a+d_c=d\) up to numerical error. Zero/nonfinite or unusable remainder directions fail qualification; do not silently skip a cell.

At fixed source \(g\) and norm \(s=\|d\|\), the ordinary and normalized-remainder source CE slopes are \(-s\|g\|\) and \(-s\|P_{out}g\|\). Their ordering is a proved first-order property. Its implementation check is distinct from finite source or dev outcomes.

This is analysis: training updates and new training-token counts are `NOT_APPLICABLE`/zero. Record evaluated answers, source-gradient answers, cells and actual displacement norms. Do not fabricate training curves or token progress.

## 9. Conditions, seeds and checkpoints

Directions are exactly `full`, `in`, `out`, `out_norm`, `random_norm`, `access`, `selection`. The `selection` output directory denotes the mathematical `choice` objective and its direction \(d_c\); they are the same condition. Scales are exactly \(\alpha\in\{-0.1,0.1,0.25,1,4\}\). Each cell independently evaluates \(W+\alpha d_k\) after restoring the same saved \(W\). The primary scale is 1; no best-scale selection. Negative 0.1 is a diagnostic reverse perturbation, not a training policy.

Full: seeds 29/43/71, both sequential orders, three source batches, seven directions, five scales = **630 cells**, each with 800 dev and 20 source answers, plus baselines/restoration checks. Smoke: seeds 29/43, both orders, first source batch, seven directions, five scales = **140 cells**, each with 40 dev and 20 source answers. Only the original old endpoint is used; no intermediate trajectory state or fresh training enters this round.

## 10. Primary metrics and frozen analysis

Let \(L_{new,k}\) be mean new-rule dev CE after direction \(k\) at scale 1. Define, in nat per answer,

\[
G_{delete}=L_{new,full}-L_{new,out},\quad
G_{amp}=L_{new,out}-L_{new,out\_norm},\quad
G_{total}=G_{delete}+G_{amp}.
\]

Positive gain means lower new CE. Retain both signed terms when they cancel or oppose. Do not divide by a near-zero total to manufacture an attribution percentage. For each comparison report corresponding old margin and full-vocabulary accuracy changes; increases in old error or decreases in old margin are costs, even when CE improves.

For any per-example or aggregate readout \(Y\), report the geometric four-corner interaction \(I_Q=Y_{full}-Y_{in}-Y_{out}+Y_0\). Also report \(\Delta b,\Delta h\), pair access/choice CE and the fraction of lists with both margins improving. These decompose measured output consequences; they do not establish independent functional mechanisms.

Aggregate records within rule and panel, with 200 records per full rule/panel and equal panel weighting for combined. Average the three source batches equally within each seed/order case. Report both orders and all three seed values; any pooled mean gives seeds equal weight. Batches, lists and orders within one seed are not independent training replications. Use descriptive values and counts; no population significance claim, multiple-testing winner, or unregistered confidence threshold. Failed/missing cells stay explicit and make dependent comparisons incomplete; do not impute, discard outliers or replace batches.

The primary analysis transformations and decision rules are frozen in this Protocol before GPU execution; raw GPU results cannot be used to adjust them. Freeze the GPU code/config/input manifest before execution. Save the aggregation script's hash before its first formal summary and independently recompute the contrasts. Primary interpretation is fixed at scale 1 on exposed dev. Other directions/scales and source results cannot rescue a non-supporting primary finding. Preserving a false favorable mechanism is the relevant interpretive risk; continuous signs and numerical bounds are kept instead of forcing a single favorable label.

## 11. Secondary metrics and guards

At every cell save full CE, access CE, choice CE, correct-versus-opposite margin, correct-versus-best-other-list margin, full-vocabulary prediction and correctness, paired \(b,h\), and inherited candidate-pool readers when available. Distinguish old correct-to-wrong transitions caused by an opposite-rule competitor, a middle-list competitor, or a token outside the list; retain cases not resolvable from stored fields. Means do not replace per-list distributions.

For each direction, \([Y(0.1)-Y(-0.1)]/0.2\) is a central finite slope with respect to scale, not an exact derivative. Compare it with computable first-order source predictions and with scale 0.25/1/4 effects. Finite nonlinearity does not itself invalidate a qualified finite contrast. CE-component interaction \(I_{obj}=Y_{full}-Y_{access}-Y_{choice}+Y_0\) is secondary and not the primary geometric interaction. No direction is selected as an optimal policy from these results.

Engineering bounds: relative gradient recomposition \(\|g-g_a-g_c\|/\|g\|<2\times10^{-4}\); per-record CE decomposition maximum absolute error < \(2\times10^{-5}\); original old-baseline reader maximum absolute difference < \(2\times10^{-5}\); actual-versus-requested displacement relative error < \(10^{-2}\), including small scales; sensitive-complement leakage \(\|Q\delta W\|/\|\delta W\|<2\times10^{-3}\) for `out`/`out_norm`, with analogous random-basis check. Record the measured values and actual displacements. Bounds qualify computation; they are not scientific effect thresholds.

## 12. Known good, bad and confusing cases

Known good: the restored baseline repeats exactly, CE components sum correctly, source objective gradients recompose and the ordinary source first-order slope is at least as descending as normalized projection. Known bad: altering a frozen parameter, using different source gradients across component controls, or separately normalizing access/choice invalidates the intended contrast. Known confusing: lower CE with worse argmax is valid; an increased mean margin with some negative per-list changes is valid; cancellation of deletion and amplification is informative, not a failed measurement. A numerical identity passing is not evidence for H1 or H2.

## 13. Stage contracts and execution

| Stage | Operation and purpose | Required artifact / transition |
| --- | --- | --- |
| Preflight | Check current assets, schemas, exact source/dev IDs, source/config/Anchor/Protocol hashes, layer/basis identity and resource contract. | Frozen input manifest; unresolved identity blocks payload use. |
| Smoke | Four independent GPU workers execute all 140 cells and numerical/restoration checks. | Complete finite readouts and qualification; no scientific verdict from the small panel. |
| Independent replay | Four new processes reload each Smoke case and reproduce batch 0, `out_norm`, scale 1, including full source/dev fields. | Exact field equality; any mismatch blocks Full. This is replay of analysis, not optimizer continuation. |
| Full | After Smoke and replay pass, submit a **separate** job for all 630 frozen cells. | Complete cell manifest and per-record readouts; no automatic condition changes. |
| Audit and report | Recompute contrasts, verify payload identity, register actual analysis outputs, write bilingual results and meeting report. | Qualified bounded interpretation; mechanism/closure not auto-approved. |

Each remote job uses one `h100-4-reserved` node and the repository default image resolved in the execution receipt. Use four independent GPU workers, not DDP. Per-job timeout is 7,200 seconds. The exact expanded image identity, job ID and timestamps belong in the receipt; do not infer them from a friendly image alias. Reuse the current mounted environment. Root supervises these explicitly requested stages. Inspect an existing job before retrying; preserve failure outputs and use a new attempt identity for a repair.

## 14. Algorithm, outputs and provenance

For each case: restore its old matrix; verify baseline twice and against E01; load fixed bases; compute each frozen source's three objective gradients; construct seven directions; for each scale/direction restore \(W\), apply the actual FP32 displacement, measure source/dev readers, then restore \(W\) byte-for-byte. After **each cell**, repeat the original source-20 complete readout exactly. Beginning/end frozen hashes and version checks must agree. Save progress and failure reason atomically; partial outputs cannot be relabeled complete.

Execution root: `/data/250010109/MoE_Router/experiments/20261011_a17_component_causality`. Unique `runs/causal_<UTC>/` owns config, frozen source and contracts, inputs/asset receipts, environment and job receipts, Smoke/replay/Full qualifications, original states/basis pointers, per-source gradients or their retained provenance and norm diagnostics, per-cell predictions, contrasts, payload manifest and completion evidence. Payloads stay execution-side. Canonical result owners are this directory's `summary.md`, `summary_cn.md`, `detailed.md`, `detailed_cn.md` after measurement. Record actual saved files; reusable analysis outputs receive asset registration and a fresh access receipt. No new trained checkpoint is claimed.

## 15. Supporting, non-supporting and insufficient outcomes

Engineering eligibility is evaluated separately from science. All required guards and cells must qualify before claiming the complete comparison. A failure blocks or narrows the affected comparison; it does not make a hypothesis false.

At scale 1, positive \(G_{delete}\) supports a local deletion benefit for that case; positive \(G_{amp}\) identifies a local amplification benefit. Positive total with nonpositive deletion specifically favors amplification over H1 for that case. Opposing signs identify a tradeoff. No local total advantage limits an immediate-old-state explanation of the observed sequential endpoint advantage; it does not prove a particular later cause. Report six case means and heterogeneity without inventing a requirement that all six have a favorable sign. Effects near measured numerical resolution remain unresolved.

For H2 report the occurrence of increased \(b\), still larger increased \(h\), and resulting old-margin changes on actual paired lists, alongside access/choice CE and full accuracy. Such occurrence establishes the specified output pattern under the intervention. Its algebraic necessity is not independently counted as supporting evidence. If other competitors dominate accuracy changes, report the two-answer explanation's incomplete coverage.

## 16. What this cannot claim

This round cannot prove old-task functional directions, a shared/unique parameter partition, intrinsic task incompatibility, SAE necessity, expert benefit, natural-language pretraining behavior, or a complete explanation of the original 100-step trajectories. A fixed-source causal contrast is conditional on the saved state, chosen gradient, geometry, scale and reader. Source first-order identities, finite policy effects, heldout development responses and architecture utility remain distinct.

## 17. Delegation, freeze and reasoning audit

| Block | Operational choice and authority | Audit boundary |
| --- | --- | --- |
| A | User-delegated fixed-state mechanism audit aligned to sub-Anchor | No new Focus or mechanism approval |
| B | Existing exposed train/dev, fixed IDs and both novelty panels | No blind-confirmation wording; test closed |
| C | Native single-answer CE and exact two-answer decomposition | Output components are not internal modules |
| D | Saved Qwen old endpoint, one final o_proj, original Q/R | No geometry refit or architecture change |
| E | Seven fixed-source directions, common CE clipping coefficient, five scales | No cumulative training or separately normalized objective gradients |
| F | Signed finite deletion/amplification gains plus old-selection costs | No best-scale or all-six favorable-sign gate |
| G | Separate four-H100 reserved Smoke and Full jobs, independent replay | Engineering completion is not scientific confirmation |

Freeze the scientific body and run-local snapshot before execution. Append receipts, qualification facts, amendments and result links after start; do not overwrite frozen settings. The specific seeds, scales and tolerances are AI operational choices made under the researcher's explicit delegation, not retrospectively attributed to a human mechanism judgment.

Reasoning audit: the comparison fixes state and source update, so deletion and amplification are separately realizable finite interventions. Access/choice and \(b,h\) are exact output coordinates with specified boundaries. Additive losses imply additive gradients, but each objective gradient can change both output terms through the parameter mapping; the seven-direction interventions measure those cross-effects rather than assuming two independent mechanisms. Full-vocabulary competitors prevent pair-margin overclaim. Existing endpoint differences motivate this experiment but do not predetermine its signs. A central slope checks a local approximation; finite contrasts remain measured even when that approximation is poor. Both positive and unfavorable outcomes can narrow the explanation without manufacturing functional separation. Current measurement state: **NOT_RUN**.

### Submission receipt / 提交回执

Smoke `pt-1gvachp3`, 2026-10-11T02:11:55Z, h100-4-reserved. Full NOT_RUN; separate submission requires exact Smoke/replay gate. Scientific body snapshot and hashes were frozen before submission. [Execution certificate](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/execution_certificate.md).

### Full submission receipt / 正式提交回执

2026-10-11T02:22:24.058179+00:00: Smoke `pt-1gvachp3` completed 140/140 cells and four independent exact replays; `smoke_gate.json=PASS`. Separate Full job `pt-majgvu5m` submitted on `h100-4-reserved`, unchanged frozen source/config. Full scientific outcomes remain pending.

### Completion receipt / 完成回执

2026-10-11T02:33Z: Full `pt-majgvu5m` reached `SUCCEEDED`; all630/630 cells qualified, no skips or retries. Smoke140/140 and four independent replays passed. Independent raw-record recomputation agrees with1,296 primary scalar comparisons within1.11e-16. Factual results and AI bounded interpretation are in [Summary](summary.md), [中文总结](summary_cn.md), [Detailed](detailed.md), [完整记录](detailed_cn.md); identities and actual output registration are in [artifact manifest](artifact_manifest.json). This receipt does not change the frozen scientific body or promote human mechanism/closure judgment.
