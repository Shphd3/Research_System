派生阅读副本；科学含义及 Unknown 状态不变。
原件：`Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R02_single_layer_adamw/protocol.md`。
[精确原始文件](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R02_single_layer_adamw/protocol.md)；仅引用目标改为包内读本或固定项目版本。

---

# Protocol: A17_04_E01 R02 single-layer AdamW mapping transfer

## 0. Approval Snapshot

Document status: APPROVED_FOR_BOUNDED_TRANSFER_AND_SMALL_OPTIMIZER_PROBE. The researcher explicitly authorized the final-layer Q/K/V/O AdamW continuation and a small optimizer diagnosis after the single-layer acquisition test. This later authorization supersedes E03's earlier instruction to wait, only within the finite scope below. Scientific mechanism judgment, adoption and question closure remain Unknown.

Revision: a17_04_e01_r02_single_layer_adamw_v1. This is a new round of E01, not a fourth core experiment. Preserve the original E01 Protocol, results and pre-run freezes. Freeze this bilingual round contract and current owning [Anchor](../../../../../../problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/17_04_conditional_mapping_transfer_anchor.md)/[Focus](../../../../../../focus/focus_conditional_mapping_transfer.md), actual sources/configs/input identities before GPU. Actual timestamp/hashes belong in the freeze manifest.

Purpose: after establishing an acquired old rule, test whether reversing a visible new mode's command mapping changes old-rule retention relative to a consistent mapping. A separate local probe asks how optimizer displacement, norm and carried moments affect the measured step; it does not explain an entire trajectory by itself. Role: root-cause audit. A–G consistency self-review PASS within delegated execution; engineering preflight/Smoke remains required.

Conditions: three continuation seeds29/43/71, each with consistent, reversed and joint_reversed branches from the **same saved E03 AdamW1200 old endpoint**. Each branch resets AdamW and trains1,200 updates×20 answers. Only layer27 q/k/v/o weights train:6,291,456 parameters. Probe:34 fixed local conditions over Base/SGD240/AdamW240 and two old TRAIN batches; its scope is defined below.

Primary quantity: reversed-minus-consistent change in old correct-versus-opposite answer margin at24,000 new answers, separate DEV panels then equal-weight combination. Support requires qualified old start, learned reversed new mapping and descriptively consistent negative primary effect. Net old harm additionally requires absolute worsening from the shared start; a smaller gain is not net harm.

Held fixed across primary branches: old weights, model/tokenizer/data, new prefixes and answer marginals, batch order within continuation seed, trainable scope, fresh optimizer settings and answer exposure. Changed: new mode's command-to-endpoint labels. DEV is previously exposed diagnostic data; original TEST is excluded. Joint has extra old labels and only12,000 new answers, so it is a feasibility control, not an equal-supervision utility winner.

Completion: qualified Smoke/replay, all nine finite branches and34 probe conditions or named partial failures, required saves/readers, actual asset registration and bilingual results. No success-selected extension, extra architecture, SAE, publication or commit/push. Subsequent action and scientific verdict remain researcher-owned.

## 1. Terminology / Definitions

Mode one is the old rule:甲 selects FIRST,乙 LAST. Mode two is new. Consistent keeps these mappings; reversed swaps them. Each world is separately label-consistent because mode is visible. Joint_reversed mixes old mode-one and reversed mode-two supervision.

One example is a prefix and its one next-answer target. One list pair includes both commands. order_new means an unseen permutation of a familiar unordered triple; combination_new means an unseen unordered triple, using familiar vocabulary. These are separate DEV panels, not novel answer words.

Continuation seed changes new-training list order only. All three paths share one trained old endpoint and do not represent three independently learned old models. Native update means the actual FP32 parameter displacement after the named clipped-gradient optimizer step. Norm matching rescales that displacement at the same model state, then remeasures FP32 rounding; it does not match accumulated training history.

## 2. Anchor Alignment

The parent asks whether conditional task relation changes shared-update effects. Original E01 could not establish old acquisition. E03 supplied a qualified one-layer AdamW old state. R02 repeats the task-relation intervention from that actual acquired state and uses the same output distinctions. The current Anchor replaces the old fixed-upstream O-only model with a full native forward over four trainable weights; the identity \(\Delta h=\Delta W a(x)\) cannot describe trained Q/K/V.

| Item | Anchor term/rival | Why/evidence role | Support / non-support / insufficient | Artifact |
|---|---|---|---|---|
| Consistent versus reversed | Mapping relation, primary \(E_s\) | Manipulate labels with matched primary inputs/exposure | Qualified stable negative / absent or opposite / acquisition or eligibility failure | Seed/panel effects |
| Common old endpoint | Acquired-rule premise | Prevent old acquisition failure from masquerading as retention | Four old DEV cells≥80% / not qualified / missing state | Baseline reader/asset |
| Comparable new skill | Difficulty/initial-skill rival | Read earliest saved four-cell new qualification | Available with path boundary / no crossing / invalid reader | Selection receipt |
| Joint reversed | Visible-mode feasibility | Check learning both mappings with old supervision | All old/new cells≥80% / failed control leaves feasibility Unknown / incomplete | Joint table |
| Local optimizer probe | Update direction/size/history rival | Measure actual displacement and finite recipient change at fixed states | Bounded step differences / none / invalid gradients/norm match | Probe summaries |
| CE and paired mode coordinates | Candidate adaptation rival | Separate candidate mass from conditional selection | Selection changes / access alone / invalid identities | Decomposition/mode tables |

## 3. Tested Hypothesis

Candidate H: at matched new-answer exposure, reversed mapping reduces old answer advantage more than consistent mapping. The stronger forgetting claim requires absolute old harm from the same learned endpoint. Candidate local question: native optimizer direction, displacement norm and carried moments can affect recipient predictions at fixed states. The probe measures these effects rather than presupposing their sign or projecting them onto long-term transfer.

The primary falsifier is no descriptively stable negative reversed-minus-consistent effect after eligible old/new acquisition. Positive effects remain evidence. If reversed training fails to learn or the old start fails qualification, retention interpretation is insufficient rather than hypothesis refutation.

## 4. Rival Explanations

1. Reversal is harder or initially less familiar. Report initial/new trajectories, final new four-cell qualification and earliest comparable-skill checkpoints; this does not equalize paths.
2. Candidate-word adaptation changes CE without preserving old selection. Read margins, paired switching, candidate-access and conditional-choice losses.
3. Initial old state or optimizer history determines the result. All primary branches share one old state and fresh AdamW; three orders expose path variation but not independent old-state uncertainty.
4. Actual optimizer steps differ in size/direction. Probe native and cross-norm updates within each fixed state. Equal norms do not remove state/history or preconditioning confounds globally.
5. The model cannot use visible modes. Joint success is a feasibility witness; failure mixes budget, supervision and optimization and cannot prove insufficient capacity.
6. Engineering, labels or batch bookkeeping create a false effect. Exact source/data/scope, no-op, freeze, replay and token-count guards protect eligibility.

## 5. Data Construction And Provenance

No new data generation or TEST evaluation. Reuse registered data_a17_conditional_mapping_v1 at /data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/data/conditional_mapping_v1, only train.jsonl and dev.jsonl. Each world has2,400 TRAIN records,1,200 lists×two commands. Each world has800 DEV records: two panels of200 lists×two commands. Original TEST has been exposed historically and is neither loaded nor called confirmation in this round.

All new-world prefixes/input IDs are identical between consistent and reversed; only target IDs flip FIRST/LAST by command. Every paired batch has identical answer marginals. Underlying training lists intentionally recur across modes, while full old/new inputs differ by mode. Preserve record/list/orbit/unordered-group/panel/mode/command/world/word/target/input identities. Existing order-panel group reuse and combination-panel disjointness remain unchanged; validate schema, targets, full-prefix boundaries and pairs before GPU.

Input assets: model_qwen3_0p6b_base_official_a5, tokenizer_qwen3_0p6b_base_official_a5, data_a17_conditional_mapping_v1, data_a17_mapping_acquisition_diagnostic_v1, adapter_a17_04_single_attention_20261011t145214z_full_attn1_adam_main and adapter_a17_04_single_attention_20261011t145214z_full_attn1_sgd_main. The AdamW family supplies1200 transfer weights and240 probe weights/moments; SGD family supplies240 probe weights. Probe uses the registered E02 neutral TRAIN/DEV files (data_a17_mapping_acquisition_diagnostic_v1), whose old prefixes/labels derive from the original mapping release; freeze their exact member hashes. Probe TRAIN batches are the first two20-record batches frozen in E03 Main step0's batch_order_record_ids, identical across states. Probe DEV takes the first20 sorted old-mode list IDs in each panel, both commands:80 records total. Freeze exact IDs and hashes. Smoke transfer panels take first10 sorted list IDs/panel, both commands/world; no TEST.

Consult the registry and run current selected strict checks before payload use. Exact Base is /data/250010109/model_cache/Qwen3-0.6B-Base-official. Registered checkpoint family membership, SHA and required Base must bind each actual1200/240/0 file; never use an ambiguous latest pointer.

## 6. Learning Task And Permitted Supervision

Predict one next answer token after the unchanged registered prefix. Train answer-only CE; prefix/padding are ignored. Input sees mode, command and three words, including the answer as a candidate, but never an explicit target, split marker or hidden world flag. Deterministic mapping supplies supervision. Mode-two branch worlds remain separate; never mix inconsistent labels for identical full inputs within one world. Joint supplies declared old and reversed-new labels. No SAE, routing, experts, auxiliary classifier, distillation or natural-text supervision.

## 7. Model / Architecture And Frozen Variants

The carrier is28-layer Qwen3-0.6B Base with exactly model.layers.27.self_attn.{q_proj,k_proj,v_proj,o_proj}.weight trainable. Shapes Q2048×1024,K/V1024×1024,O1024×2048; four tensors total6,291,456. All earlier weights, attention biases/q-k norms, MLP, embeddings, final norm and lm_head freeze. Runtime enumerate names/shapes/count and guard frozen versions during steps plus byte hashes at initialization/stage end.

Use FP32 native SDPA/evaluation mode/no dropout, deterministic algorithms, no TF32. Forward recomputes all trainable attention dependencies; no frozen-upstream activation cache. Transfer initializes all four weights from E03 AdamW Main update1200, requiring exact registered Base. Its old training optimizer/RNG/counters are not continued: each branch uses fresh AdamW, seed-specific order and stage-local coordinates. Exact recovery within a branch must restore that branch's own state; this differs from an intentional branch-start reset.

## 8. Training Objective And Optimization

For20 valid answers, minimize empirical \(L=20^{-1}\sum_i-\log p_\theta(y_i\mid x_i)\), in nat/answer. Four microbatches of five contribute loss sums divided by20. No prefix/padding denominator, regularizer or auxiliary term; component registry empty/NOT_APPLICABLE. One independent worker is DP1; four GPUs do not multiply a branch's20 targets/update.

All transfer branches use fresh AdamW learning rate1e-4, betas(0.9,0.999), epsilon1e-8, decay0, foreach=False/fused=False, constant rate. Clip aggregate gradient over all four tensors at global L2 norm1. Record raw/clipped norms and actual displacement. No skipped update, tuning, early stop or adaptive continuation.

Each consistent/reversed branch trains1200updates=24000 new answers, ten exposures of its2400 records. Each joint branch trains1200updates=24000 total answers,10old+10new per update: five list IDs, both commands in both modes. Joint receives12000 old and12000 reversed-new answers, five exposures of each world. Across three seeds, primary branches total144000 new targets; joint adds72000 total=36000old+36000new. Nine branches total216000 training answers. Preexisting old training, local gradients, Smoke, replay and evaluation are separate counts.

## 9. Conditions, Seeds, And Checkpoints

Continuation seeds29,43,71 each run consistent, reversed, joint_reversed from the same registered AdamW1200 weights. Within a seed consistent/reversed order is identical. Joint uses the corresponding seed-derived list stream, five complete old/new list quadruples per batch.

Save/evaluate0,1,16,50,120,240,600,1200 updates, corresponding to0,20,320,1000,2400,4800,12000,24000 stage targets. Joint separately records old/new counters, each half the total. Main retains all eight points/branch,72 states if every save completes. Do not select the endpoint from performance.

Smoke uses seed29 only, three branches×3updates×20=180 targets. External-process step1→2 replay runs for every branch,3×20=60 replay targets. Full branches restart from the registered learned old endpoint, not Smoke. Smoke uses smaller declared DEV panels; Full uses all fixed DEV.

Save all four weights, full AdamW moments/step, constant schedule, Python/NumPy/CPU/CUDA RNG, completed updates/valid targets, old/new counters, branch/seed, input endpoint identity, data cursor/order/next-batch IDs and source/config/parent hashes. Recoverable branch states remain adapters requiring Base, not standalone model exports.

## 10. Primary Metric And Frozen Analysis Plan

For old input \(x\), correct endpoint \(y\) and opposite endpoint \(o\), define \(m_A(x;\theta)=\log p_\theta(y\mid x)-\log p_\theta(o\mid x)\). Let \(M_A\) be its mean over fixed old DEV. At1200 updates,

\[
E_s=\big[M_A(\theta^{\mathrm{reversed}}_{s,1200})-M_A(\theta_0)\big]
 -\big[M_A(\theta^{\mathrm{consistent}}_{s,1200})-M_A(\theta_0)\big].
\]

\(\theta_0\) is the common learned old state; \(s\) is continuation order. Units are nat/answer. Report each panel, then equal-weight combined panels, equal command weight and equal seed weight. Report all three effects, arithmetic mean, min/max and sample SD. All three effects<0 with mean≤−0.01 nat is the inherited AI convention for descriptively consistent negative transfer cost; all>0 with mean≥0.01 is positive consistency. Mixed/smaller effects remain heterogeneous/weak, not equality. No p-values, independent-old-model inference, post-hoc seed/list exclusion or untouched-confirmation claim.

Old start must have each command/panel DEV accuracy≥80%. Final new qualification requires each of four new command/panel cells≥80%. Report baseline-to-final CE/accuracy/margin for each branch. An initially qualified consistent branch need not improve another0.01nat/1pp; explicitly retain its initial-skill ceiling. A negative-transfer interpretation of reversal requires its final acquisition and an actual rise in new target margin; failure leaves learned-signal interpretation insufficient. These guards never force successful learning.

Net old harm is separate: report absolute old CE increase, accuracy decline and margin decline from \(\theta_0\), each with direction and magnitude. Relative reversal cost alone is not net harm. Inherited material reporting conventions are0.005nat CE,1pp accuracy and0.01nat margin, descriptive rather than significance thresholds.

Secondary comparable-level reader selects the earliest saved point with all four new DEV cells≥80%, including step0 if already qualified. No crossing is unavailable, not a reason to extend. Read old/new outcomes at those saved points; paths and difficulty remain unmatched. Joint feasibility requires all four cells in each mode≥80% at its fixed endpoint; extra old labels and half new exposure prohibit equal-supervision winner claims.

Analysis uses only TRAIN/DEV and frozen rules after bounded completion/freeze checks. Record/list is observation unit; continuation seed is an order-variation unit conditional on one old state. Missing paired cells/checkpoints block the affected estimand; no imputation. Save primary seed/panel table, trajectories, comparable-level selection receipt, loss/mode/paired tables and engineering eligibility under run/analysis.

## 11. Secondary Metrics And Local Optimizer Probe

All transfer readers retain CE, full-vocabulary accuracy, correct/opposite margin, correct/strongest-full-competitor margin/ID, three candidate probabilities, pair-both-correct and same-argmax. For candidate set \(S\), access loss \(-\log\sum_{w\in S}p(w)\) plus conditional-choice loss \(-\log[p(y)/\sum_{w\in S}p(w)]\) equals CE exactly. This is output accounting, not internal modules.

For each matched list, \(s_{m,c}=\log p(L_3\mid x_{m,c})-\log p(L_1\mid x_{m,c})\). Define \(a_m=(s_{m,乙}-s_{m,甲})/2\), \(q_m=(s_{m,乙}+s_{m,甲})/2\), \(C=(a_1+a_2)/2\), \(K=(a_2-a_1)/2\). Expected old/consistent \(a>0\), reversed new \(a<0\). These exact output coordinates describe command/mode response and endpoint bias, not identified parameter components.

The separate probe uses three actual states: Base, E03 single-layer SGD240, E03 single-layer AdamW240. At each state and each of two fixed old TRAIN batches, restore all four weights and appropriate optimizer state before every condition. The five conditions are no-op, nativeSGD, nativeAdamFresh, nativeSGD rescaled to nativeAdamFresh norm, and nativeAdamFresh rescaled to nativeSGD norm. SGD/Adam settings match E03 (clip1, SGD.01, Adam1e-4/betas.9/.999/eps1e-8/decay0). AdamW240 adds nativeAdamCarry using its saved moments/step and AdamCarry rescaled to nativeSGD norm for each batch. Total Full conditions:3states×2batches×5+2batches×2carry=34. Smoke uses Base/first batch/five conditions only. Probe source gradients use old TRAIN; recipient readout/gradient uses80 fixed old DEV records. It does not measure mode-two transfer.

For each condition, source gradient \(g_{\mathrm{src}}\) is distinguished from actual FP32 applied displacement \(\delta=\theta_{\mathrm{after}}-\theta_{\mathrm{before}}\). Form cross-norm steps by scaling the native displacement then remeasuring actual rounded displacement; norm error must≤1%. Zero native displacement gives ZERO_NO_DIRECTION and unavailable direction matching, never arbitrary replacement. Save aggregate/per-projection gradient and displacement norms, inter-optimizer direction cosines and descent alignment \(\cos(-g_{\mathrm{src}},\delta)\). Cross-state differences are descriptive because the states already differ.

For recipient mean CE \(L_R\), compute its baseline gradient \(g_R=\nabla L_R(\theta)\) and report

\[
\Delta L_R=L_R(\theta+\delta)-L_R(\theta),\qquad
R_{\mathrm{finite}}=\Delta L_R-\langle g_R,\delta\rangle .
\]

This defines the measured finite-step remainder, with the actual applied four-tensor displacement and gradient at the same state. Probe CE is recomputed with float64 log-softmax over native FP32 logits, while its gradient uses the native FP32 answer CE; preserve the native-CE cross-check. The measured remainder includes nonlinear finite-step effects and any residual precision difference. It quantifies departure from first-order prediction at that step, not a pure numerical-error estimate or proof of the cause of that departure. Do not replace actual AdamW displacement by negative raw gradient. Small norm-matched local effects cannot identify why1200-step trajectories diverge.

Every transfer branch writes seven required TensorBoard tags for answer-weighted CE/total, learning rate, target/update coordinates and effective20 targets/update. Tags are tokens/train_lm_loss, updates/train_lm_loss, tokens/train_total_loss, updates/learning_rate, progress/tokens_seen, progress/optimizer_step, progress/effective_tokens_per_update. Counters are branch-local; record preexisting old24000 answers separately. Probe is fixed-state analysis, not an unlogged training trajectory.

Guards: finite quantities; no-op identical; runtime four-tensor inventory; frozen version/end-byte checks; no skipped windows; independent target/batch counts; all required finite tags; exact external resume including optimizer/RNG/order; CE identity error<2e-5nat; actual norm-match error≤1%; source/config/data/freeze hashes unchanged. Failure stops the affected branch/probe and preserves partial evidence.

## 12. Known Good / Known Bad / Known Confusing Cases

Good: mode-one甲→first/乙→last; consistent mode-two same, reversed swaps; new prefixes/paired answer marginals match. No-op and fresh branch starts reproduce their common state. Probe restores before each independent intervention.

Bad: missing mode while mixing conflicting labels, target in prefix, TRAIN/DEV group leakage beyond allowed order reuse, TEST access, independent order mismatch across primary worlds, training onlyO, carried Adam moments in a declared fresh branch, probe stacking or incorrect joint counters. Reject/ineligible.

Confusing: reversed is worse than consistent while both improve old predictions; old CE improves but correct selection worsens; consistent already qualified at step0; joint fails; equal-norm local changes differ but long-term origin is unresolved. Retain all outcomes.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal/input | How and why | Output/artifact | Status/failure/handoff |
|---|---|---|---|---|
| Preflight | Bind acquired old state, Base, TRAIN/DEV and probe states | Current strict access, SHA/member/schema/pair and actual four-tensor inventory | Input/access and label/order manifests | Invalid input/scope blocks dependent GPU work |
| Freeze | Prevent result-driven choices | Snapshot current owners/round contracts, code/config/data/IDs/environment | Freeze/certificate | Missing identity blocks start |
| Smoke/replay | Qualify transfer and probe code | Seed29 three branches×3updates, small DEV, every branch external1→2; Base five-condition probe | States/readouts/tags/gates | Engineering FAIL blocks Full until qualified repair |
| Full transfer | Compare relation after acquisition | Three orders×three fresh-Adam branches,1200steps each, common old weights | Eight saves/branch, old/new readers | Finite completion; retain poor learning as insufficient, no adaptive extension |
| Full probe | Measure local optimizer consequences | Three fixed states, two batches,34 independent interventions | Real deltas, recipient finite changes/remainders, norm/cosine table | Named nonfinite/zero/norm failure bounds comparison |
| Analysis/handoff | Produce auditable bounded answer | Primary relative/absolute effects, acquisition/skill/joint guards, register actual states/readouts | Summary/Detailed, registration/access and manifest | Finish factual delivery; science/next branch remain researcher-owned |

## 14. Algorithm, Output, And Provenance Contract

Execution root: /data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer. Bind unique timestamped run directory before submission. Code/config, raw predictions, optimizer-probe arrays/deltas, logs/TensorBoard/checkpoints remain execution-side; canonical round Protocol/Summary/Detailed/manifest remain here. No raw payloads in Git.

Reuse inspected E03 native four-tensor carrier, AnswerLM/collate, SGD/Adam semantics, exact resume, telemetry and freeze guards; adapt original E01 mapping-world data readers, matched branches, joint batching and mode coordinates. Reject original O-only fixed-feature assumptions, original TEST loader, prior unqualified old states as transfer starts, sensitive-direction projections, SAE/MoE and unrelated training. Inspect training_reuse_index and actual source; record reuse/adaptation/rejection before implementation.

Use root acp_submit_template.sh, h100-4-reserved, image key shphd-lite-0911, one actual four-H100 node,7200sec/job. GPU0/1/2 each run one continuation seed's three branches sequentially; GPU3 runs the bounded probe. Smoke runs seed29 only: GPU0/1/2 each run one of its three branches, while GPU3 runs the probe. These four independent workers do not create data-parallel replicas. Capture dry-run/resolved specification/image, direct job ID/command, durable pod log and actual device views. Full requires qualified Smoke; no hardware fallback or duplicate submission of an active job.

Per branch save checkpoints/update_<step>/state.pt plus member manifest under run/<phase>/seed_<seed>/<branch>/, or the exact equivalent bound in frozen config/source. Save scope, reached total/old/new targets, parent and input-endpoint hashes, full optimizer/RNG/order resume fields. Probe outputs live run/optimizer_probe/<phase>/<state_id>/batch_<index>/ and results.json/manifest.json; record frozen condition IDs, actual displacements/norms and no-op baseline.

Register actual Smoke/Full checkpoint families separately with explicit saved members, reached answers/steps, Base and learned endpoint dependencies, source/config/data/producer hashes and resume qualification. Register probe/analysis outputs with saved identity and current selected strict checks. Missing saves/partial probes remain explicit. Platform success alone does not establish scientific eligibility. Keep source and failed-attempt identity; no silent repair of frozen evidence.

## 15. Success / Failure / Insufficient Evidence

Primary support requires qualified common old start, final new four-cell acquisition in both primary worlds, reversal's actual new-margin improvement, engineering eligibility, and all three continuation effects negative with mean≤−0.01nat. This supports a relation-dependent old-margin cost conditional on one learned old state. Net harm needs separately measured absolute old worsening; it is not implied by support.

Qualified absent/opposite effects are local non-support. Mixed/small effects are weak/heterogeneous, not equality. Unqualified old start, failed reversed acquisition/improvement, missing paired endpoint or invalid guards leaves the learned-transfer claim insufficient/ineligible. An initially qualified consistent branch can participate without an arbitrary further-improvement requirement; report the ceiling.

Joint success means old/new all cells≥80%; failure leaves feasibility Unknown. Probe validity qualifies local measurement only; no direction or norm outcome can rescue missing primary transfer evidence. All finite unfavorable outcomes still complete the factual task if recorded.

## 16. What This Cannot Claim

No unavoidable task contradiction, universal forgetting, internal shared/differential module identification, expert/separate-training benefit, pure parameter-count or optimizer cause, natural-text transfer or independent old-state replication. Visible modes make both mappings jointly satisfiable in principle. Comparable-skill readings cannot fully remove path difficulty. Joint has different labels/exposure. Probe norms/cosines/remainders are local and cannot substitute for continuous-training evidence. Reusing exposed DEV is diagnosis, not fresh confirmation.

## 17. Block Confirmation, Freeze, And Amendment Ledger

The current researcher request authorizes the one-layer AdamW mapping continuation and bounded optimizer probe. Earlier suggestions mentioning four layers do not override the explicit current one-layer choice. The current owning Anchor/Focus must reflect that model before freeze; retain original E01 historical design/results.

| Block | Frozen scope | Basis/status |
|---|---|---|
| A | Existing conditional mapping question, relation intervention | Current researcher execution request; scientific verdict Unknown |
| B | Registered original TRAIN/DEV only, fixed probe IDs | Verified source, no new TEST/confirmation |
| C | Mode-visible neutral commands, answer-only pairs | Existing adopted task |
| D | Last-layer fourweights/common acquired endpoint | Explicit one-layer choice, actual E03 assets |
| E | Fresh AdamW,20targets/step,1200, joint10+10 | Delegated finite operationalization, inherited optimizer |
| F | Relative margin, absolute harm, acquired new cells, local probe | Existing Anchor readers plus bounded authorized diagnosis |
| G | Qualified Smoke/exact replay, nine branches/34probe,4H100reserved | Current authorized scope and resource envelope |

Cross-block self-review: question, allowed labels, native four-weight forward, matched primary exposures, joint difference, one old-state dependence, acquisition/primary branches, local-versus-long-term probe and noTEST boundaries agree. This audit is not researcher mechanism confirmation. Before GPU, resolve actual IDs/paths/runtime/source/config and freeze both languages; initial measurements remain NOT_RUN.

Before start, decision-bearing corrections update this single round Protocol and companion, then refreeze. After first execution, preserve the body and append any material amendment with ID/time, before/after, reason, visible evidence, affected blocks/conditions, authorization and eligibility impact. Later receipts/status/result links are allowed; do not overwrite old E01 or manufacture a new scientific verdict.
