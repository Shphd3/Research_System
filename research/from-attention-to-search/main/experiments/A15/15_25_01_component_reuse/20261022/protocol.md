# Protocol: A15_25_01_E01 frozen component dependence and transfer

## 0. Approval Snapshot

Status: `APPROVED_FOR_FROZEN_ANALYSIS_AND_INTERVENTION`. Authority: the researcher's 2026-10-22 request to create the child owners, execute Qwen3-0.6B analyses/interventions and deliver the integrated explanation without intermediate approval or evaluation. Scope includes implementation, bounded smoke and full registered inference; no model/dictionary/expert training, remote resource fallback, publication or Git operation. The researcher authorized autonomous completion of this bounded experiment; the operational choices below are AI choices, not individually confirmed human judgments. A–G are AI-audited under that delegation. Scientific acceptance and question closure remain `Unknown`.

Primary owner: [A15_25_01](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_25_joint_feature_graph/subanchors/15_25_01_component_reuse_anchor.md). Parent: A15_25, inspectable feature relations before learning decisions. No new independent Focus is created. Role: operationalization/proxy test and functional audit. Question: do recurring final-residual components contribute and transfer across matched Boolean contexts, while a separate operator-related set redirects prediction? Rival: generic format/output components and nonspecific editing damage. Primary evidence: dependence beyond random edits, transfer equivalence, donor-directed shift beyond random edits. The entire conjunction requires the behavior and numerical gates below.

Execution: ACP; `resource_profile: h100-4-reserved`; `image_id: shphd-lite-0911`, resolved by the System execution envelope. One job; four disjoint extraction shards and one final analysis. A bounded local visible-MIG smoke checks implementation before submission. Active compute ceiling 60 minutes, output ceiling 5 GiB. No automatic resource switch. Exact frozen configuration and pre-run hashes are saved under the execution root.

## 1. Terminology / Definitions

A is integer parity (`n % 2 == 0`); B is comparison (`n > threshold` or the equivalent `threshold < n`). AND/OR combine the same atoms and value. A family fixes function name, variable, threshold and comparison spelling; its four truth assignments each produce A/B/AND/OR examples. These controlled adaptations have two motivating natural-code sources and shared templates; families are not natural-document independence.

H means candidate recurring features, not proven basic semantic operations. C means candidate operator-related features, not a proven composition algorithm. Frequency means binary positive activation in the fixed Tulu TRAIN reference. Literal code-pattern counts separately describe the reference text. Neither measures Qwen pretraining exposure. NLL is full-vocabulary correct-token negative log probability in nats; margin is correct minus alternative Boolean logit. A donor is the matched context supplying feature values.

## 2. Anchor Alignment

The child tests the parent's prerequisite that a statistical component description can become an inspectable functional object. It adds direct final-residual interventions under the current explicit authorization; it does not reopen the parent's frozen graph procedure or execute its future shared/separate learning H1. The sole tested interface is the final block residual before global normalization. Fourteen-layer descriptive decoding profiles remain joint-dictionary descriptions.

## 3. Tested Hypothesis

H attenuation harms prediction more than matched random attenuation; same-answer atomic H transfer preserves prediction within ±0.05 nat; C transfer between opposite-answer AND/OR pairs shifts predictions toward donor answers more than matched random transfer. All three primary conditions, numerical guards and native behavior qualification are required for the joint interpretation. A null transfer alone is not evidence for reuse.

## 4. Rival Explanations

Format/output information: all paired examples have the same final newline and controlled syntax; C selection uses same-answer AND/OR pairs, but operator surface cues and common templates remain live rivals. Nonspecific perturbation: random sets match changed-feature count, reference frequency decile and decoder norm within a factor of two, followed by exact per-example edit-norm rescaling. Reconstruction error: preserve it in every selective edit and separately measure full reconstruction quality. Weak base competence: report atomic and composed behavior before mechanism interpretation. Observational rarity: low literal counts cannot establish pretraining rarity or a rare-versus-common causal effect.

## 5. Data Construction And Provenance

Inputs: assets `model_qwen3_0p6b_base`, `tokenizer_qwen3_0p6b_base`, `crosscoder_qwen3_14layer_16384_bf16_a18_formal_14layer_batchtopk_a22_999997440_20261013`, `data_tulu_sft_route_20261019t012300z`, and `representation_tulu_sft_route_20261019t012300z`. The fixed Tulu split is revision `6248b175d2ccb5ec7c4aeb22e6d8ee3b21b2c752`; TRAIN has 1024 dialogues and 85,548 answer targets. Its complete sparse activations determine feature frequency. Code-source counts use its 156 CodeAlpaca dialogues. Record current asset checks and source/manifest hashes; saved checkpoint digest evidence is distinguished from a newly recomputed payload hash.

Natural motivating records are `code_alpaca_15313` (parity) and `code_alpaca_2663` (greater-than comparison). Freeze 96 generated families with seed 20261022; randomly assign 48 to discovery and 48 to confirmation before any model output. Four truth assignments × four conditions give 1536 examples, equally split 768/768. Each atom is evaluated in executable Python; all targets are the single next token `True` or `False`. Assert distinct full prompts, target correctness, split disjointness and balanced truth-case coverage. Changes to family identity, template, filtering or split after model outputs require an append-only amendment.

The natural reference counts use regexes `%\s*2\s*==\s*0` and `\w+\s*>\s*\w+` on assistant text, with document-level atom/joint counts and same-line conjunction/disjunction counts. Preserve the matching IDs and pattern limitations. Both unseen compositions cannot be relabeled common versus rare. Generated examples are a controlled test, not an untouched natural continuation benchmark.

## 6. Learning Task And Permitted Supervision

No learning task is run. Prediction is the next Boolean token after a Python REPL function call. Target truth comes only from executable generated expressions. Discovery labels and same-answer pairing may select components; confirmation values and outputs cannot select them. Original model and dictionary training data/parameters remain unchanged. No gradient optimization, classifier fit, PCA fit, exposure-controlled training or learned router is part of this experiment.

## 7. Model / Architecture And Frozen Variants

Original Qwen3-0.6B-Base: 28 blocks, hidden size 1024. CrossCoder: 14 residual-post layers at zero-based indices 1,3,...,27; 16384 shared features; original centered vector-RMS normalization; checkpoint at 999,997,440 positions. Load the actual saved threshold, scoring norm, strict `>` comparison, decoder bias and precision. Do not use per-token TopK or recalibrate on this task. Keep Base and dictionary parameters `requires_grad=False` and compare parameter version counters before/after.

Reuse `analysis_tools/relation_learning/data_routes.py` for model loading and frozen encoding, and the existing frozen final-head computation. The extractor's saved raw final residual is the intervention interface. Adapt task construction, component selection and effect analysis in this run's own code. Reject old expert training and cached learned-router replay as evidence for this question.

## 8. Training Objective And Optimization

Not applicable: zero trainable parameters, zero optimizer updates and no optimizer/checkpoint selection. Record inference example/target counts, execution time, GPU allocation and memory. NLL is an evaluation quantity, not a training loss. Statistical component selection is fixed discovery-only ranking. The numerical audit states why gradients, learning-rate schedules and resume optimizer states are not applicable.

## 9. Conditions, Seeds, And Checkpoints

One original Base and one original dictionary checkpoint. Candidate H: reference probability at least max(0.01, 90th percentile among observed feature probabilities), and discovery occurrence at least 0.5 in each of A/B/AND/OR; choose at most 32 by minimum condition occurrence, then mean decoded amplitude, then feature ID. Candidate C: exclude H; reference occurrence ≥0.0005 and discovery occurrence ≥0.1; rank absolute mean same-answer paired OR−AND activation difference divided by discovery activation standard deviation, then ID; choose at most 32. Fewer than eight in either set fails the joint interpretation; do not lower thresholds. Save all candidates and ranking values before reading confirmation effects.

Conditions: native/no-op; full reconstruction; H attenuation α=0.25/0.5/1; H transfer from same-family/same-value same-answer A or B (A wins a tie); H same-context transfer; C opposite-operator transfer; C same-context transfer; whole-vector opposite-operator transfer as a positive implementation control. For truth assignments with different atomic answers, also transfer H from the opposite-answer atom as a diagnostic. Three random-control seeds 11/22/33 for full H attenuation, same-answer H transfer and C transfer. Match each actually changed feature to a distinct eligible feature outside H∪C in the same reference-frequency decile and within ×2 decoder norm; restrict to active or donor-changing features as appropriate. Report unmatched examples explicitly. Rescale each complete control edit to the treatment's vector norm. These are edit seeds, not independently trained models.

## 10. Primary Metric And Frozen Analysis Plan

Primary dependence: on confirmation AND/OR examples, mean ΔNLL(H attenuation α=1) minus the mean of three complete random attenuation controls. Primary reuse: mean ΔNLL(same-answer atomic H transfer). Primary operator effect: on confirmation cases where AND/OR answers differ, donor-directed logit shift from C transfer minus mean random C transfer. Each quantity first averages within generated family, then weights families equally. Paired bootstrap resamples the 48 confirmation families 5000 times with seed 20261022. Two-sided intervals use quantiles 0.0083333 and 0.9916667 (Bonferroni three comparisons, familywise 0.05). Also provide ordinary 95% descriptive intervals where labeled.

Dependence supports its clause only if its adjusted interval is wholly above zero. Reuse supports its clause only if its adjusted interval lies wholly within [−0.05,+0.05] nat. Operator specificity supports its clause only if its adjusted interval is wholly above zero. No post hoc rank, layer, seed, α or subset selection. All missing/failed examples remain counted; matched-control comparisons use complete pairs and list the denominator and excluded IDs. No outlier trimming. Fewer than 90% complete matched controls makes the corresponding primary clause insufficient. Uncertainty is conditional on these shared-template families, not independent training seeds or all natural language.

## 11. Secondary Metrics And Guards

Report forced-choice accuracy, Boolean candidate probability mass, full-vocabulary NLL, correct-answer margin and all four truth cells. Native eligibility: each atom accuracy ≥0.8; each composition ≥0.7; mean Boolean probability mass ≥0.5 in each condition. Numerical eligibility: native versus cached correct-token NLL max error ≤0.02 nat and Boolean-margin max error ≤0.05; repeated same-batch no-op and same-context edits exactly zero; whole-vector donor replacement equals donor-head results in the same shape. Feature encoding uses the saved frozen threshold; compare two batch cuts, report exact event agreement and maximum activation discrepancy. Nonfinite values fail the dependent stage. Reconstruction FVE and decoded profiles are descriptive; poor reconstruction does not justify discarding residual error.

Report feature-set reference/task frequencies, H/C overlap (must be zero), feature count, realized changed-feature counts, edit norms, control matches, full-reconstruction error, 14-layer decoder profiles and operator-pair residual distances. A common decoded layer profile is not 14 independent feature activations or a causal contribution percentage. Show fixed examples and an adverse case where one exists; do not choose examples to replace aggregate evidence.

## 12. Known Good / Known Bad / Known Confusing Cases

Known good: executable targets, exact same-context/no-op replay and whole-vector donor transfer. Known bad: intentionally wrong donor-index or wrong-scale calculations must fail their algebra/identity check on a tiny synthetic tensor, without entering scientific data. Known confusing: AND and OR have identical outputs when both atoms agree; these pairs are useful for C discovery and a control, but cannot measure an opposite-answer donor shift. Retain them separately.

## 13. Scientific Procedure And Stage Contracts

1. Freeze data and reference counts without model outcomes; output examples, manifest and reference frequencies. Failure is data/provenance failure; no dependent inference on incorrect targets.
2. Bounded smoke on the first two discovery families only; qualify loaders, tensors, no-op/positive controls, runtime and unchanged weights. It is engineering evidence, not confirmation. A valid smoke permits the already authorized full job, not a new research scope.
3. Extract all registered examples with frozen models in four disjoint family shards; collect representations and native head statistics. Save extraction guards and failure receipts. Select H/C using discovery only and write the selection manifest before computing confirmation intervention results.
4. Execute all registered edits and controls; save per-example outcomes, aggregate paired intervals and validity flags. Independent descriptive analyses continue if a semantic prerequisite fails. Stop only the stages whose numerical/data prerequisites fail.
5. Finish coverage, three audits, bilingual Summary/Detailed, example walkthrough, curated figures and requested meeting synthesis; update local reading synchronization. Do not silently promote the parent's learning hypothesis.

## 14. Algorithm, Output, And Provenance Contract

Execution root: `/data/250010109/MoE_Router/experiments/20261022_qwen06b_component_reuse`. Code/config in `code/` and `config/`; generated examples in `data/`; smoke and formal outputs in separate `smoke/` and `full/`; access, source hashes, environment and submission receipts in `provenance/` and `acp_receipts/`. Save sparse/reference counts, raw selected-layer residuals, gated z, target IDs, feature sets, per-example edited predictions, match failures, bootstrap summaries and runtime certificate. Register actually saved reusable data/representations in the asset catalog; no new trained checkpoint is expected.

Apply \(h'=h+s(z'-z)_S D_S\), never replace h by the full reconstruction for selective edits. Record an algebra check against reconstruction-plus-residual on a tiny batch. Refuse mismatched tensor order, token positions, target lengths, output overwrite or nonfinite state. File hashes bind source/config/data and frozen Protocol. Existing byte-hash receipts for GB checkpoints are labeled copied evidence unless recomputed. No implicit download or input substitution.

## 15. Success / Failure / Insufficient Evidence

All validity gates and three primary clauses passing supports only this intervention-defined decomposition in the bounded task. A valid contrast outside the registered favorable branch weakens that clause or is inconclusive according to its interval; report the actual distinction. Behavior, candidate, frequency or matching insufficiency prevents a joint semantic conclusion while preserving valid measurements. Numerical/identity failure invalidates the affected effect. Do not make a negative statistical result into proof of no mechanism.

## 16. What This Cannot Claim

No pretraining frequency/exposure effect, broad natural-language generalization, semantic-pure feature, unique composition algorithm, online routing rule, parameter commonality, rank-one update, learning efficiency, shared-versus-separate expert advantage or MoE architecture recommendation. Final-layer edits concern the completed representation, not the computation that originally constructed it. The generated family split shares templates and motivating sources.

## 17. Block Confirmation, Freeze, And Amendment Ledger

2026-10-22: researcher approved the previously described frozen-model representation experiment and explicitly delegated uninterrupted completion. A–G are `AI_AUDITED_UNDER_USER_DELEGATION`; no claim of individual human confirmation of AI-chosen numeric thresholds. Cross-block consistency: PASS at registration. The current explicit instruction supersedes generic intermediate-confirmation/researcher-first two-pass pauses for this task. It does not grant scientific closure or training permission.

Freeze scientific body and config before smoke; store timestamp and SHA256 in `provenance/design_freeze.json`. After starting, only append execution receipts/result links and explicit amendments. Each amendment records old/new values, reason, already visible data, scope, authorization and eligibility effect. The original body remains recoverable. No result-dependent threshold or selection repair is permitted without labeling the affected evidence exploratory.

### Amendment A1 — prospective behavior qualification

Registered 2026-10-22T15:46:40.495925+00:00. Replace raw-accuracy eligibility by per-family balanced accuracy (mean of True-class and False-class accuracy), retaining 0.8 atomic / 0.7 composition thresholds and reporting raw accuracy. AND/OR labels are 25/75 percent; constant majority prediction would otherwise pass 0.7. Only source counts, truth tables and engineering numerical smoke guards were inspected; no smoke behavior values or formal outcomes were inspected. Primary estimands and populations are unchanged. Authorized under the current uninterrupted-completion request. Full record: execution `provenance/amendment_A1.json`.

### Execution and further-work status

The authorized run `pt-p5ory1zm` completed at 2026-10-22T15:48:29Z. On the subsequent user instruction, all further execution is on hold pending purpose and resource confirmation. The user reported availability of separate single-card or two-card resources; no new profile is selected and no new run is authorized. The requested next deliverable is the stage summary, progress and TODO from already saved evidence.
