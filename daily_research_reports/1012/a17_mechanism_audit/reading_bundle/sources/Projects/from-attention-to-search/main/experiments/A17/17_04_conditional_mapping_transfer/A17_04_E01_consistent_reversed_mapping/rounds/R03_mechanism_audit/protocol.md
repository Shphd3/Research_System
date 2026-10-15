# Protocol: A17_04_E01 R03 finite mechanism audit of R02

## 0. Scope and authority

Revision: `a17_04_e01_r03_mechanism_audit_v1`. Execution is authorized by the researcher's current request to complete the attached mechanism analysis using four reserved H100 GPUs without further approval. This is an additional analysis round of E01, not a new Focus or training experiment. The R02 Protocol, outputs and existing scientific states remain unchanged. Researcher mechanism acceptance and question closure remain `Unknown`.

Owners: [parent Anchor](../../../../../../problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/17_04_conditional_mapping_transfer_anchor.md), [Focus](../../../../../../focus/focus_conditional_mapping_transfer.md), [R02 Summary](../R02_single_layer_adamw/summary.md). The three attached files motivate the audit; executable model and checkpoint interfaces come from the actual frozen R02 sources. No new training, TEST access, SAE, SVD scan or separate-expert architecture is authorized by this round.

## 1. Purpose, hypotheses and rivals

Parent uncertainty: under a limited budget, which learning demands can use shared parameters and which need conditional processing? This round asks which actual final-layer parameter changes participate in the observed simultaneous reversal of old and new command responses. It also tests implementation error and simple over-displacement explanations. It does not compare the net utility of separate experts.

H0: label, prefix, checkpoint or evaluation errors created the apparent old 0% accuracy. Independent data/identity/logit checks plus GPU no-op reproduction distinguish this from a valid measured effect.

H1: B-only reversal changed computation used by both visible modes rather than restricting the changed command response to the new mode. Output signs already support this description; same-state finite parameter rollback tests participation of particular matrix changes, without assigning unique functions.

H2: simply reducing the existing total displacement can retain both rules. Five-point interpolation tests this particular weight segment, not smaller-learning-rate optimization. A compatible point supports segment feasibility; no compatible point weakens only the sampled segment explanation.

Strongest surviving rival: reversal starts at 0% new accuracy whereas consistency starts at 99.875%; B-only optimization has no old supervision, and joint learning changes both supervision and new exposure. This audit cannot isolate those causes or eliminate optimization-history alternatives.

## 2. Actual system and input identities

Reuse Qwen3-0.6B Base with only `model.layers.27.self_attn.{q_proj,k_proj,v_proj,o_proj}.weight` changed, 6,291,456 parameters. All other weights and q/k normalization remain fixed. Native FP32 SDPA forward and the answer-position logits are reused from R02. No optimizer is stepped.

Required registered assets: `model_qwen3_0p6b_base_official_a5`, `tokenizer_qwen3_0p6b_base_official_a5`, `data_a17_conditional_mapping_v1`, `adapter_a17_04_single_attention_20261011t145214z_full_attn1_adam_main`, all nine `adapter_a17_04_transfer_20261011t160256z_full_seed_{29,43,71}_{consistent,reversed,joint_reversed}` families, and `analysis_a17_04_transfer_20261011t160256z_full_mapping`. Current selected strict access is [recorded here](../../../../../../../../../assets/checks/2026-10-12_a17_r02_mechanism_inputs.json); readers must verify membership hashes rather than use latest.

R02 root: `/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z`. Common old state is the registered E03 AdamW1200 actual checkpoint. Analyze R02 reversed step240 and1200 for each of three continuation orders. These orders share one old trained state, not independent old-model replicates. Existing trajectories may use saved0/1/16/50/120/240/600/1200 readouts.

Only registered TRAIN and DEV are permitted. No TEST reader or hidden target in input. Full finite interventions use all800 old and800 reversed-new DEV records:200 lists per panel, both commands. Panels are `order_new` (new order of a familiar unordered triple) and `combination_new` (new unordered triple). Report both and their equal-weight combination; no data-derived sample exclusion.

## 3. Audit and finite interventions

1. Independently check all TRAIN/DEV label mappings, true token prefixes, paired new inputs and target marginals. Check common four-matrix step0 identity, actual checkpoint parents, fresh branch optimizer state and frozen nontrainable source. Independently reconstruct cached four-corner metrics for three seeds, three branches and steps0/240/1200.
2. Compute CPU float64 displacement norms per Q/K/V/O and overall for reversed240/1200; relative norm divides by the common old matrix norm. Cosines compare the same seed/step displacement against consistent and joint, without functional attribution.
3. For each reversed seed/step restore all four target weights before each condition. Evaluate complete reversed, repeated no-op/restoration, four single-matrix rollbacks to old, common old baseline, and four reverse displacements inserted individually into old. Only one matrix differs from the designated reference in each treatment; save exact restored tensor identities.
4. Evaluate the existing weight segment `old + alpha*(reversed-old)` for alpha0,0.25,0.5,0.75,1 with all four matrices interpolated together. This is forward-only parameter interpolation. Endpoints duplicate the designated baselines deliberately as controls.
5. Fixed supplementary representation panel: seed29/step1200, first10 sorted DEV list IDs in each panel, both commands and both modes (80 records), selected before outcomes. Read answer-position o_proj input `c`, output `a`, final normalized hidden `h`, and native endpoint logits for old, complete reversal, reversal with O rolled back, and old with only reversed O inserted. Do not choose favorable heads/features or fit a probe.

## 4. Mathematics, measurements and decision rules

CE is negative log probability of the correct answer; accuracy uses full-vocabulary top1. Endpoint margin is correct minus opposite endpoint logit; full margin is correct minus strongest incorrect vocabulary logit. Natural-log units are nat. For each paired list define last-minus-first logit difference `s`; command response is `a_m=(s_m,乙-s_m,甲)/2`. Positive means甲first/乙last; negative means甲last/乙first. These are output coordinates, not parameter modules.

For each condition report old/new CE, accuracy, both margins, candidate mass, paired switching, a1/a2 and their differences from the corresponding reference. Matrix participation means a finite intervention changes these actual outputs beyond numerical no-op tolerance, not that the matrix is uniquely necessary. Report changes for both tasks, including failure to preserve the new task. No significance or universal mechanistic identification claim.

Interpolation compatibility requires **every command/panel accuracy cell in each mode at least80%** at a sampled alpha; combined80% alone is insufficient. Report failed cells. Failure at the five samples does not exclude unsampled alpha values or other parameter paths; joint already supplies another compatible solution.

The preceding layers are frozen, so the same input has the same last-attention input. Q/K/V change the vector `c` reaching O; O converts it to `a=Wc`. On the supplementary panel the exact attention displacement decomposition is

\[
\Delta a=\Delta Wc_0+W_0\Delta c+\Delta W\Delta c.
\]

The four finite O/readout conditions evaluate `(W0,c0)`, `(WR,c0)`, `(W0,cR)`, `(WR,cR)`. For an output statistic F, report the nonadditive contrast `F11-F10-F01+F00`; it is state-dependent interaction, not a unique attribution. The frozen output-head difference `w_last-w_first` maps the final normalized hidden vector to endpoint logit difference; verify the exact bridge and record its residual. Norms and identities describe computation, not standalone discoveries of shared representations.

Aggregation: equal record weights within each command/panel, equal command/panel weights, then equal continuation-order weight. Report individual seeds and range/sample SD where useful; do not pool records as independent model replicates. This is exposed-DEV diagnostic evidence, not untouched confirmation. Missing cells or failed guards are `INSUFFICIENT`/`INELIGIBLE` for affected comparisons; no imputation or scientific extension.

Audit status is `VALID`, `BUG_FOUND` or `UNABLE_TO_VERIFY`. Exact restored weights must match bytewise. CPU algebra recomputation tolerance1e-8 nat, paired identities1e-8; GPU cached no-op tolerance1e-3 nat on CE/response/margins and identical top1, with measured errors retained. Any larger error blocks downstream mechanism claims pending a documented repair and a new freeze. The worker must prove finite logits, complete four-corner pairing and no state contamination.

## 5. Execution, freeze and outputs

Reuse actual R02 `transfer.load_model`, `native.AnswerLM/collate` and native evaluation; adapt four-tensor loading and independent statistics. Reject the old one-O restore helper for four-matrix checkpoints. Adapt the supplied API-independent helpers after inspecting real tensor keys. Execution root: `/data/250010109/MoE_Router/experiments/20261012_a17_r02_mechanism_audit/`. Unique run roots, frozen input/source/config/Protocol digests and durable logs are required. No old file is overwritten.

Use root `templates/execution/acp_submit_template.sh`, envelope `h100-4-reserved`/`shphd-lite-0911`, one node. Independent GPU lanes, not data-parallel copies: three seed lanes, with the representation panel evaluated in the seed29 lane and the fourth allocated device unused. A bounded same-profile Smoke checks real four-weight loading, signs, no-op, restoration and finite outputs on the small fixed panel before Full; toy tests include exact four-corner signs and exception-safe no-op restore. No optimizer/token/resume-training telemetry is applicable because this round performs zero training updates; evaluation record counts and checkpoint steps must remain explicit.

Preserve submitted receipts, actual topology/runtime, first-progress and terminal evidence. User requests experiment completion and result delivery; monitor through finite completion without adding an automation. Hard budget: no new training; no adaptive sweeps, no hardware fallback. On errors, preserve evidence, diagnose and repair only the same authorized analysis scope; no silent scientific-result replacement.

Deliver `mapping_audit_results.json`, `delta_stats.csv`, `parameter_rollback.csv`, interpolation/trajectory/representation tables, actual raw native readouts and source/run manifests execution-side. Register reusable analysis/representation outputs with actual parent/data/split/hook identities; no new trained checkpoint is produced. Canonical bilingual Summary and Detailed live here; the requested group-meeting script lives in the dated meeting folder. Include original numbers, labeled-axis figures and per-figure provenance. No commit/push is requested in this turn.

## 6. A–G audit and completion

A purpose: local parameter participation and sampled-path explanation, not separate-expert utility. B comparison: fixed-state actual matrix interventions; nonlinear cooperation remains possible. C data: fixed TRAIN/DEV and registered weights. D estimation: actual finite outputs with two panels and three conditional orders. E rivals: implementation/segment explanations testable; supervision/difficulty/history remain live. F engineering: hashes, no-op and restoration before claims. G reporting: support/non-support/insufficient branches preserved, mechanism acceptance `Unknown`.

Current result before execution: `NOT RUN`. Completion requires audit status, all planned finite conditions or named failures, actual evidence/registration and clear bilingual results plus meeting script. A null or distributed matrix effect is a valid outcome. No automatic scientific state transition.
