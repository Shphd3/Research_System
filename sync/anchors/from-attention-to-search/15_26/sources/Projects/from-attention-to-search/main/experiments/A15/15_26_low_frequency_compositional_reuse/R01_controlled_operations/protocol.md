# Protocol: A15_26 R01 controlled operations

## 0. Approval Snapshot

Document status: **APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_AND_ANALYSIS**. Freeze: 2026-10-24T15:53:59Z. Owner: A15_26; one integrated experiment R01 with learning/exposure, reuse diagnostics and stronger freezing comparisons. [Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_26_low_frequency_compositional_reuse/15_26_low_frequency_compositional_reuse_anchor.md) · [Focus](../../../../focus/focus_low_frequency_compositional_reuse.md).

The researcher explicitly instructed completion of all experiments and result analysis, then “this might happen because…” mechanism conjectures and a separate recognition update. The subsequent resource reply states no total compute ceiling, one Reserved GPU preferred and four if necessary. These instructions delegate exact implementation choices; no repeated A–G approval turn is imposed. A–G are recorded as **CONFIRMED_BY_EXPLICIT_DELEGATION**, not individually researcher-selected numerical values. Cross-block consistency: PASS after the audits below and Smoke gates. Scientific result acceptance and closure remain Unknown.

Execution: `execution_surface: acp`, `resource_profile: h100-1-reserved`, `image_id: shphd-lite-0911`; activation `/data/250010109/MoE_Router/experiments/20261024_a15_26_compositional_reuse/source/runtime.sh`. The envelope resolves tuple and image URL. No fallback, new encoder, full MoE or unrelated environment. Allowed concurrency4 is unused initially. Role: operationalization/proxy test of atomic learning and functional coupling, with a bounded causal-interface audit.

## 1. Terminology / Definitions

An operation is one permutation of32 answer symbols. A pair is an ordered F then G. Atomic mastery is measured per operation in a second phrasing, including all32 symbols; it is format-held-out, not knowledge-held-out. Composition generalization means held-out inputs of seen pairs. Reuse is not defined by frequency or correct answers alone.

## 2. Anchor Alignment

R01 tests learning help, exposure effect, selective functional transfer and the stronger frozen strategy separately. Atomic rule revision constrains an independent pair-table rival; internal exchange tests a proposed shared carrier. Neither establishes a unique historic circuit or MoE utility. All outcome-dependent factual reporting is completed even if mechanism qualification fails.

## 3. Tested Hypothesis

H-help: relevant atomic training beats untrained and alternative-operation controls under equal combination supervision. H-exposure: the same pair performs better when its exposure changes from low to high with fixed marginals. H-transfer: a successful, selective atomic revision changes affected composition outputs to the externally computed revised answers without revised composition teaching. H-carrier: original atomic-parent states cause receiver-specific recombined answers above matched random edits. H-freeze: rank32 frozen adaptation passes behavioral thresholds while retaining atomic behavior and approaching joint updating.

## 4. Rival Explanations

Generic format/answer adaptation: B untrained and C same-format alternate permutations. C negative transfer is explicitly possible; require P>B as well. Intrinsic pair difficulty: exchange pair frequency identities. Input/answer symbol imbalance: exact model-independent integer allocation balances both during training. Memorizing320 training mappings:96 held-out mappings. General damage or answer copying: unaffected operations/combinations, sham revision, prespecified new answers, donor-answer disagreement and equal-norm random state edits. Capacity/optimization differ between U/F/J and are reported, not declared equal.

## 5. Data Construction And Provenance

Data seed20261024;32 single-token Chinese symbols verified against the exact local tokenizer and actual answer suffixes. F0–F3 and G0–G3 are eight distinct nonidentity random permutations. C uses eight additional fixed permutations, matching format/vocabulary/exposure. Generator rejects duplicate composed functions. Each pair has20 TRAIN,6 VAL,6 TEST inputs, no mapping overlap. Atomic TRAIN and second-format checks each have256 rows. A feasible integer allocation yields each input and output symbol five times within each eight-pair frequency group in TRAIN. VAL/TEST each have three instances per input/output symbol globally. This conditioning is disclosed; one operation universe is studied.

Combination exposure cycle2880 answers: balanced each pair180; skew high320/low40; swap reverses identities. Every F/G receives720 per cycle; every input/output symbol90. Within a pair its20 training inputs cycle equally. Sixteen cycles=46080 answers=1440 updates of32. Primary acquisition seeds29,43,71 are independent training trajectories over the same operations, not independent task universes.

Dataset `/data/250010109/MoE_Router/experiments/20261024_a15_26_compositional_reuse/data/dataset.json`; hash `a394a65379adeea6f9498ee6ae8768681405d3e88575e2a2c09f820241c1614f`. Model-independent pre-freeze v1 imbalance remains in `data/pre_freeze_v1/`; it is not used. Model-dependent test performance is never used for hyperparameter choice.

## 6. Learning Task And Permitted Supervision

Atomic prompt “操作 F2。输入：红。答案：”; format check rephrases the same mapping. Combination prompt “先执行 F2，再执行 G3。输入：红。答案：”. Only the final symbol is supervised. One target token per example; loss/accuracy use full151936 vocabulary. No intermediate supervision or chain-of-thought. Revision training contains only atomic labels, including rehearsal of unmodified atomic operations; no combination labels or examples. TEST is read only at fixed final checkpoints and for locked diagnostic confirmation.

## 7. Model / Architecture And Frozen Variants

Exact registered Qwen3-0.6B Base and tokenizer; FP32 native SDPA, deterministic algorithms, TF32 disabled. Freeze first27 blocks, cache their input to block27 using the same native interface. Replay qualification maximum logits error≤2e-4 and exact argmax agreement. Default acquisition/update range last q/k/v/o weights (6291456 elements); other parameters frozen. Atomic seed29 pilot1440 updates; if any operation format accuracy<95%, use the single predeclared repair: entire final block,2880 updates, all P/C seeds. Reset from Base for repaired acquisition; preserve original failure. No further acquisition search.

U updates the chosen original range, no adapter. F freezes all parent parameters and trains h+B GELU(Ah) residual at native attention output, A width32 and B zero initialized. J same adapter and also updates U range. Same initial adapter values for paired F/J. All use the identical order per seed/distribution. Z is parent evaluation without training. If any rank32 F balanced TRAIN accuracy<95%, run exactly one capacity check rank128 F/J balanced across all seeds; retain original rank32 as primary. No new capacity sweep.

## 8. Training Objective And Optimization

Answer-only cross entropy, natural-log units per valid answer token, no auxiliary/regularization losses. AdamW lr1e-4, betas(.9,.999), epsilon1e-8, weight_decay0, foreach/fused False, global gradient clip1, constant learning rate. Batch32, microbatch8×accumulation4, one GPU; every completed update counts32 valid targets, no skipped finite failures. All fresh stages reset optimizer; exact resume restores optimizer/RNG/order/counters. Freeze versions and missing/nonfinite gradients are hard engineering failures.

TensorBoard under each case/tensorboard: tokens/train_lm_loss, updates/train_lm_loss, tokens/train_total_loss, updates/learning_rate, progress/tokens_seen, progress/optimizer_step, progress/effective_tokens_per_update; gradient norm supplemental. No invented auxiliary tags. Primary learning curve coordinate is completed answer tokens.

## 9. Conditions, Seeds, And Checkpoints

Acquisition P/C×3 plus original seed29 qualification branch if repaired. Combination P×U/F/J×balanced/skew/swap×3=27; B/C×U×balanced×3=6; total33 distinct trajectories. P-U-balanced reused for transfer. Optional rank128 adds6. Every combination1440 updates. Atomic qualification1440 or repaired2880. No maximum GPU hours, but fixed stage counts and only these repairs.

Revision: from each P-U-balanced endpoint, F0 and G0 each with three fixed output derangements (601/607/613), edit and sham paired=36 trajectories. Each1024 updates. Each batch16 revised-operation examples and16 original other atomic examples; identical indices across edit/sham. Edit targets replace only the named atomic operation. No selection by composition scores. Even unqualified initial endpoints get bounded descriptive revisions; all are marked ineligible for the mechanism claim.

Saves:0/1/2/8/32/128/360/720/half/final when in range; final plus resume states include trainable weights, optimizer, RNG, step,32×step tokens, order digest/data cursor, scheduler, parent identity. Exact registered Base/parent required; adapter is not standalone. Raw paths `/data/250010109/MoE_Router/experiments/20261024_a15_26_compositional_reuse/runs/<case>/checkpoints/step_*.pt`. Training-stage conditions do not use TEST to select a checkpoint. Main endpoint is always final.

## 10. Primary Metric And Frozen Analysis Plan

All16 pairs equally weighted; report all seeds and pair accuracies/CE, high/low separately and curves. Help: final P−B and P−C and normalized trapezoid VAL learning-curve area difference; report direction per acquisition seed. Support requires both final mean improvements≥5pp and consistent positive directions across3 seeds; ceiling or broad uncertainty is insufficient, not equivalence. Exposure: pairwise high−low accuracy from skew/swap, averaged equally across16 pairs then seeds; support requires mean≥5pp with same seed direction. These are practical descriptive criteria, not universal statistical constants.

Transfer eligibility: parent P each atomic operation≥95%; composition endpoint≥95% TEST macro and atomic format mean≥95%. Edit operation≥95%, each unchanged atomic operation≥95%, and unaffected combinations lose≤2pp relative to sham. Primary affected answers with y'≠y: new-correct fraction edit−sham, require≥20pp and≥80% new-correct at every eligible seed/direction after averaging edits. Report old-answer and other-answer rates. Every failed guard is explicit insufficiency for mechanism, not silent exclusion.

Carrier: rank8/16 in last-attention output, basis from centered32 intermediate-symbol means in128 atomic-parent F states. Select rank using96 VAL predicted recombination accuracy, tie smallest; no fit on TEST. Block output same ranks is only a late-answer diagnostic and never eligible as the causal intermediate. On96 TEST cases choose alternate z' from the fixed tables so g_j(z') differs from both old receiver answer and donor answer z'. Main contrast is recombination accuracy minus five equal-rank/equal-norm random edits; support requires native95% guards, directed accuracy≥80%, contrast≥20pp, same-intermediate and other-surface retention loss≤2pp, no-op exact. Carrier selection/qualification failure cannot establish absence of all reuse.

Frozen: combination macro≥95%, low-frequency group≥90%, atomic average loss≤1pp and every operation≥95%, F−J macro≥−2pp. A96-item TEST grid cannot reliably establish2pp equivalence; intervals and resolution are reported, no nonsignificance-as-equivalence claim.

Uncertainty:5000 fixed-seed20261024 paired resamples over input-symbol groups, within each saved parent; report per-parent intervals and conditional aggregate. Same-task seeds are displayed rather than turned into an independent-world claim. Three primary domains help/exposure/transfer use98.333% conditional intervals as a multiplicity guard where estimable;95% descriptive intervals for secondary displays. Report effect thresholds and intervals separately; intervals cannot rescue failed qualifications. Missing/failed outputs stay in coverage ledger. No outlier or seed removal.

## 11. Secondary Metrics And Guards

Atomic accuracy/CE per operation, all pair mappings, answer probability/margin, training fit, zero-shot composition, train/VAL/TEST gaps, actual parameter count, exposure and throughput. Positive controls: two successive calls to learned atomic predictor, true intermediate supplied to G, wrong intermediate with predictable G output. They add calls/information and are not fair single-call baselines.

## 12. Known Good / Known Bad / Known Confusing Cases

Teacher lookup composes exactly; same-input no-op must reproduce logits/argmax. Shuffled/random outputs cannot qualify. Whole-state or late answer replacement may improve behavior without identifying reuse; mark diagnostic only. Atomic mastery with composition failure is a legitimate insufficient mechanism result. TEST is tiny per pair and uncertainty must remain visible.

## 13. Scientific Procedure And Stage Contracts

Data preflight→cached native replay→Smoke/external-process resume→atomic qualification/one repair→all33 matched composition trajectories→optional fixed capacity repair→all36 revision diagnostics→locked state interventions→aggregation and separate reporting. Each stage saves its inputs, operation, counts, validity reason and downstream handoff. Native or edit qualification failure does not cancel independent learning/exposure/frozen/descriptive checks. Numerical corruption stops the affected run and is repaired with an append-only engineering record before resuming; configuration changes start separate labeled rounds.

## 14. Algorithm, Output, And Provenance Contract

Entry source/pipeline.py prepare/smoke/full; data.py exact counts; engine.py native learner; interventions.py locked edits. Reuse audit binds selected older source SHA, but old checkpoints/data/projector science are not reused. Runtime source/config/data/protocol hashes are frozen in audit/design_frozen.json before GPU execution. CPU-generated data and all actually saved checkpoints/cache/analysis outputs are registered with required parents and fresh strict access. Resource change is separately recorded; no automatic fallback.

Evidence paths: `/data/250010109/MoE_Router/experiments/20261024_a15_26_compositional_reuse/audit`, `/data`, `/runs`, `/analysis`, `/acp_receipts/pod`. A durable certificate includes actual GPU/image/source hashes, job ID and this conversation as sole monitoring owner. Raw outputs stay execution-side. Canonical results here: Summary factual findings; result_analysis comparison explanations; mechanism_conjectures explicit “this might happen because…” plus rivals; recognition_update revises only AI beliefs; Detailed full procedures/deviations; artifact_manifest asset/evidence indexes. English plus Chinese companions. No final scientific report or question closure without researcher judgment.

## 15. Success / Failure / Insufficient Evidence

Every condition receives DONE_VALID, DONE_EXPLORATORY, INVALID, FAILED or BLOCKED with counts and reasons. Finish all bounded conditions and factual delivery even under negative results. A trained mapping can succeed without held-out composition; this is reported as memorization-compatible, not a mechanism refutation. Exact-resume/telemetry/data defects make affected comparisons ineligible until repaired.

## 16. What This Cannot Claim

No unique historic circuit, complete semantic modularity, natural language learning benefit, optimal frequency routing, shared/separate expert ranking, or new data-universe replication. Transfer edit success is functional coupling, state exchange tests a proposed carrier, and freezing is a distinct stronger claim. Recognition-update conjectures are future suggestions, not evidence or run approval.

## 17. Block Confirmation, Freeze, And Amendment Ledger

A–G CONFIRMED_BY_EXPLICIT_DELEGATION from current user instructions; all numerical details are transparent AI operational choices within that delegation. Cross-block scientific/data/implementation audit records are separate audits/ files. Frozen at 2026-10-24T15:53:59Z, before any model task performance or GPU training. Subsequent scientific-body changes are append-only amendments with before/after, reason, visible results, scope and eligibility; original contract preserved. Small pure engineering repairs preserve scientific values and retain failed evidence. Resource ceiling: none, by explicit user reply; one H100 Reserved preferred. Implementation, Smoke, complete formal conditions and analysis authorized. Git/publication not authorized.
