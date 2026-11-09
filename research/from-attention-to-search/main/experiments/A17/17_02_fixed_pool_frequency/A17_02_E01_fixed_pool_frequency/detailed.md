# Detailed: A17_02_E01 Fixed-Pool Frequency

[中文](detailed_cn.md) · [Summary](summary.md) · [Protocol](protocol.md)

## 0. Quick Recap

Full completed126 trajectories/90,000 trained answer tokens/4500 updates. Engineering1520/1520 PASS, actual-exposure qualification126/126 PASS. Confirmation n6 reached `REGISTERED_POSITIVE_MEDIAN_INTERACTION`, median0.066142 nat/answer. All extra-practice CE effects relative to B-only are beneficial; accuracy does not necessarily improve. Human mechanism/closure judgmentUnknown.

## 1. Terminology / Definitions

A is extra practice; B is the recipient. One presentation supervises exactly one next answer. FIRST/LAST are visible and simultaneously satisfiable. A/B identity is metadata, absent from prompts. Frequency repeats a fixed200-list pool. Order-new changes order within actually trained B content groups; combination-new uses content groups absent from actual A/B training. CE is full-vocabulary answer cross-entropy; accuracy is full-vocabulary argmax correctness. Their directions need not coincide.

## 2. Anchor Link And Decision Point

[Independent Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_02_fixed_pool_frequency/17_02_fixed_pool_frequency_anchor.md) owns the fixed-B rule×presentation interaction. [Frequency Focus](../../../../focus/focus_fixed_pool_frequency_shared_learning.md) owns the researcher's next mechanism decision. This report completes observed/statistical facts and does not close the question or approve an architecture.

## 3. Protocol Freeze, Conformance, And Deviations

The unique Protocol and source/config/data were archived before Smoke or exploration: [Full frozen sources](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/frozen_sources.json). Config SHA256 `a8bb067fa5f4b4fe47a7430576bc8fdfa25866c7a410fe43f02bd77fdfcf596d`; archived Protocol SHA256 `3c94773c97c12d5ce7fdbdd9aef7dc88f9625f64d13732941fe1807444cda3d0`. Completed execution uses archived `run/source`, not later mutable helpers.

Pre-submission amendment01: generated v1 was never submitted or model-evaluated in this experiment. Its test had40 rule rows overlapping the previously evaluated E01 dev. Preserve v1 and the original unsubmitted freeze. Actual v2 excludes every30 old content orbit, yielding zero content-group overlap with every old train/dev/test split. Filtering used list identities, not model results. Sizes, balance, conditions and estimands did not change. [Qualification](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/data/fixed_pool_v2/qualification.json).

No post-dev setting, condition, seed or threshold was selected. All valid adverse effects are retained. Both Full stages completed without a runtime repair or re-opening confirmation for tuning. Postflight exposure auditing, registered-output export, aggregation and figures are derived outputs separate from immutable training-source/artifact manifests. Full final-state external restore was NOT_CHECKED; actual state availability is not a new resume certificate.

## 4. Actual Setup

Inputs: `model_qwen3_0p6b_base`, `data_a17_fixed_pool_frequency_v2`; tokenizer is the Base tokenizer. A/B each400 paired-rule records=200 distinct ordered lists=100 unordered content groups. Dev/test each800 records: each rule×novelty cell200, every word at every position/answer count10. Both conditions use the same prompt template and20 qualified single-token Chinese answers.

Every trajectory starts from original Base. Only `model.layers.27.self_attn.o_proj.weight`, FP32[1024,2048],2,097,152 parameters, is trainable. AdamW LR1e-4 constant from update1, betas(.9,.95),eps1e-8,wd0,clip1. Micro5×accum4×DP1=20 valid answers/update; train BF16 autocast, primary evaluation native FP32, secondary BF16. Other weights retain exact worker before/after hashes and per-trajectory versions. No router, expert, LoRA or SAE changes the frequency learner.

| Condition | A presentations | B presentations | Updates |
|---|---:|---:|---:|
| b_only | 0 | 200 | 10 |
| same_200 / diff_200 | 200 | 200 | 20 |
| same_800 / diff_800 | 800 | 200 | 50 |
| same_budget / diff_budget | 500 | 500 | 50 |

Both B roles execute all seven conditions. Explore29/43/71:42 trajectories,30,000 answers,1500 updates, dev only. Confirm101/113/127/139/151/163:84 trajectories,60,000 answers,3000 updates, unopened model test. Same/different policies share pool identities and schedule placement within each seed/role/count. At500, two full repetitions plus100 from five complete cyclic-shift blocks retain exact marginals.

Hardware: ACP `h100-4-reserved`, share-space/share-cluster, n6ls.iu.i40.4, one reserved node/four independent GPU workers, no cross-policy DDP. Smoke pt-cgmiw5f3: UTC17:35:59→17:37:05. Full pt-ho4byzg4: UTC17:40:21→17:48:33,2026-10-09; Beijing01:40:21→01:48:33,2026-10-10. [Execution certificate](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/execution_certificate.md) and [platform terminal](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/platform_terminal.json).

## 5. Metrics And Registered Decision Rules

Let L be recipient B mean native FP32 answer CE for seed s, B role r, A count n, novelty p and rule relation. At B200, the sole primary is:

\[
I_s=\frac14\sum_{r\in\{\mathrm{FIRST},\mathrm{LAST}\}}\sum_{p\in\{\mathrm{order},\mathrm{combination}\}}
\left[(L^{\mathrm{different}}_{s,r,800,p}-L^{\mathrm{same}}_{s,r,800,p})-(L^{\mathrm{different}}_{s,r,200,p}-L^{\mathrm{same}}_{s,r,200,p})\right].
\]

The independent repetition is seed, n6. All six I>+0.01 or all six I<−0.01 meets the pre-frozen conservative two-sided sign rule, p=.03125. [min,max] is an at-least96.875% seed-median interval under independent iid seed effects, not a mean CI or population-of-datasets interval. Exploration n3 remains descriptive. All components must remain; none can rescue a failed primary.

Net addition compares each extra-A endpoint to B-only at B200, with unequal total compute. Allocation compares A800/B200 to A500/B500 at the same1000 supervised answers, with different B opportunities. These are secondary descriptions with no additional confirmatory tests. Useful A-source learning is not a gate on valid trajectory effects; a local update-mechanism claim would need its separate guard. Required telemetry retains answer-normalized losses, gradient norms, LR, batch/token/update counts, epoch-equivalents, elapsed time, peak memory and TensorBoard; no evaluation tokens enter trained-answer totals.

## 6. Evidence Lineage

Data qualification/manifest → current strict input checks →11 CPU quota/oracle/statistical counterexample tests → immutable source/config/Protocol freeze → Smoke external restart and no-op → all trajectory metrics/schedules/saved states → Full engineering audits and primary/secondary analyses → terminal/platform verification → independent actual-exposure audit → saved-family SHA checks/registry.

[Raw Full](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z) · [Confirmation](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/analysis_confirmation.json) · [Engineering](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/engineering_audit_confirmation.json) · [Terminal](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/terminal_verification.json) · [Platform](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/platform_terminal.json) · [Actual asset registration](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/asset_registration_request_registered_outputs.json)

[Exploration](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/analysis_exploration.json) · [Exposure qualification](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/actual_exposure_novelty_audit.json) · [Artifact manifest](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/artifact_manifest.json) · [Descriptive aggregates](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/descriptive_aggregates.json) · [Actual output request](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/asset_registration_request.json). Registry independently verified1008 member files across126 families; all126 strict output checks passed. Snapshot `assets/checks/2026-10-10_a17_outputs_20261009T175342Z.json`. Each family actually saves update0,2,middle,final; these are not planned placeholders. Original Base remains an external required parent.

Checkpoint loader: `state.pt['trainable_weights']` is the whole FP32 Tensor[1024,2048], not a name-keyed dict or delta. State carries AdamW, Python/NumPy/CPU/CUDA RNG, optimizer_step, tokens_seen, next_data_position, task, config_sha256, presentation_order_sha256, parent_asset_id and data_asset_id. Constant LR needs no scheduler. Smoke qualified independent restore2→3 exact; Full endpoints were saved, not individually restore-certified.

## 7. Main Results

Exploration I:29=0.084158,43=0.072401,71=0.080150; median0.080150, mean0.078903. Status `EXPLORATORY_ONLY`; these did not tune confirmation.

Confirmation median0.066142, mean0.066663, min0.051485, max0.078583. Six of six >δ; registered branch `REGISTERED_POSITIVE_MEDIAN_INTERACTION`, conservative two-sidedp=.03125. All24 rule/panel components are kept:

| Seed | FIRST/order | FIRST/combination | LAST/order | LAST/combination | Combined I |
|---|---:|---:|---:|---:|---:|
| 101 | 0.050108 | 0.058124 | 0.077245 | 0.085900 | 0.067844 |
| 113 | 0.049365 | 0.046607 | 0.043948 | 0.066021 | 0.051485 |
| 127 | 0.084904 | 0.080098 | 0.059640 | 0.089692 | 0.078583 |
| 139 | 0.049090 | 0.053218 | 0.070306 | 0.085149 | 0.064441 |
| 151 | 0.061409 | 0.065484 | 0.072749 | 0.095515 | 0.073789 |
| 163 | 0.062496 | 0.058504 | 0.050445 | 0.083892 | 0.063834 |


| B rule / panel | Median across six seeds | Minimum | Maximum |
|---|---:|---:|---:|
| FIRST/order_new | 0.055758 | 0.049090 | 0.084904 |
| FIRST/combination_new | 0.058314 | 0.046607 | 0.080098 |
| LAST/order_new | 0.064973 | 0.043948 | 0.077245 |
| LAST/combination_new | 0.085524 | 0.066021 | 0.095515 |


Positive I says same-rule extra practice has a larger incremental CE benefit from A200→800. It does not establish net harm. Descriptive policy endpoints below first average the two B roles within each seed/panel, then report the median over six seeds; combined averages both novelty panels before taking its median. Component medians do not algebraically add to a combined median.

| Policy | Order-new CE | Combination-new CE | Combined CE | Combined accuracy |
|---|---:|---:|---:|---:|
| b_only | 0.801364 | 0.796052 | 0.798928 | 83.4375% |
| same_200 | 0.708025 | 0.699505 | 0.703617 | 87.1875% |
| diff_200 | 0.725715 | 0.721578 | 0.723807 | 85.5000% |
| same_800 | 0.590033 | 0.574224 | 0.582623 | 89.1250% |
| diff_800 | 0.669000 | 0.666243 | 0.667780 | 83.2500% |
| same_budget | 0.576972 | 0.570751 | 0.573273 | 89.7500% |
| diff_budget | 0.629074 | 0.627753 | 0.627808 | 85.6875% |


Before any task update the untouched Base confirmation loss is1.007858, accuracy78.1250% across800 test rows; the Base has substantial partial ability and has not mastered this carrier. It is not a from-scratch learner.

| Extra A policy at B200 | Median seed combined CE minus B-only | Negative role/panel cells |
|---|---:|---:|
| same_200 | -0.095448 | 24/24 |
| diff_200 | -0.074815 | 24/24 |
| same_800 | -0.216990 | 24/24 |
| diff_800 | -0.131207 | 24/24 |


All96 extra-practice component CE differences are negative. Different A800/B200 improves CE versus B-only despite median accuracy83.2500% versus83.4375%; same A800/B200 has89.1250%. Accuracy and CE are retained as separate observations; a less-helpful effect is not called net interference.

| Relation | Median seed combined CE: A800/B200 minus A500/B500 | Positive role/panel cells |
|---|---:|---:|
| same | 0.008747 | 16/24 |
| diff | 0.040762 | 24/24 |


All six combined allocation differences are positive within each relation. Same-rule component differences have16 positive and8 negative cells; different-rule24 positive. These are descriptive allocation effects, not pure frequency, because B opportunities change. FP32 is the registered reader; every endpoint's `final_evaluation_bf16.json` remains available secondarily and does not replace FP32 or select a favorable precision.

Secondary BF16 description yields combined interaction median0.065845, all six values above0.01 descriptively. Maximum FP32/BF16 component CE difference across all confirmation policies is0.007634 nat/answer; accuracy differs by up to3 percentage points. These reader differences are retained, and no secondary significance test replaces the frozen FP32 primary. [Precision record](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/secondary_precision_description.json).

## 8. Visualization Results, When Decision-Relevant

![Frozen confirmation and separate net benefits](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/figures/frequency_confirmation.png)

Upper-left shows all six independent primary effects above0.01; upper-right retains FIRST/LAST×novelty components. Lower-left separates order-new, combination-new and combined median CE by policy; lower-right shows every seed's net CE effect below B-only. Dots are seeds, lines mark medians, not confidence bands. Categorical policy connections do not represent time. [Standalone PDF](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/figures/frequency_confirmation.pdf), [figure origins/hashes](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/figures/provenance.json); input sources and plotting-script SHA are recorded. No extra test was introduced by this plot.

## 9. Stage Evidence And Failure Decomposition

Data v2 PASS, CPU11/11 PASS. Smoke56/56 PASS for4×8-update trajectories=640 trained answers/32 updates; extra80 answers are restart calibration, not scientific training totals. Truncated Smoke had only partial actual exposure and could not qualify every planned order-new label; it remains engineering-only. [Smoke exposure audit](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/smoke_4h100_v2_20261009T172146Z/actual_exposure_novelty_audit.json).

Full exploration508/508 and confirmation1012/1012 PASS, all126 actual-exposure panels eligible. Platform SUCCEEDED is independently recorded, not inferred from a log. All126 required final checkpoints and milestone families were saved and registered. The v1 overlap is a repaired pre-submission qualification issue, not failed training or a scientific negative. Full external endpoint resume remains NOT_CHECKED; no unsupported capability is claimed. Human mechanism/utility/closure remainUnknown despite the passed registered statistical branch.

## 10. Full Experiment Record

Round2026-10-10 Asia/Shanghai: question/hypothesis is the fixed-B rule×presentation median interaction (§2,§5). Setup/controls are reset Base, direct final matrix, seven policies, balanced fixed pools, both B roles and constant20-answer updates (§4). Data and confirmation split are v2, dev-only exploration and six new-seed untouched model test (§3–4). Result is the completed positive statistical branch with net CE benefits and separate accuracy/allocation observations (§7). Insight is that differing rule practice can provide net CE benefit while same-rule practice provides greater incremental CE benefit. The next researcher's decision is whether this bounded interaction justifies a mechanism study; closure remainsUnknown.

Authorized downstream endpoint description uses all36 contrasts=9 seeds×2 B roles×A200/A800 diff-minus-same, all800 frequency dev rows, no test/effect-based endpoint selection. [Frozen selection](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/configs/frequency_endpoint_selection_frozen.json), [input configuration](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/configs/frequency_endpoint_selection.json), [independent module](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/source/analyze_frequency_endpoints.py), [CPU interface/algebra11-check PASS](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/configs/frequency_endpoint_interface_check.json). All72 endpoint IDs are registered. Matching raw-o_proj1B SAE asset is pending; actual analysisNOT_RUN. Native ΔW=Wdiff−Wsame, absolute SAE endpoint encodings plus explicit residual, same-endpoint loss-gradient accounting, actual finite loss difference/remainder and20-answer-pool mass/conditional CE will describe endpoints. This is not decomposition of the Adam trajectory or evidence of feature causality. [SAE analysis owner](../../17_01_controlled_list_prediction_rules/A17_01_E03_restricted_update_full/sae_analysis.md). No extra analysis job is submitted while SAE owns the4GPU slot.


## Appendix: completed matched-SAE endpoint description, 2026-10-10 Asia/Shanghai

This appendix asks whether the matched raw-projection SAE provides a compact loss account of the already observed frequency-policy endpoint differences. It changes no frequency training, original confirmation statistic, test evaluation or statistical branch. The frozen description includes every 9 seeds ×2 B roles ×A200/A800 pair:36 diff-minus-same endpoint contrasts, each on all800 frequency dev rows. The original test confirmation median0.0661424387 remains the primary result; the numbers below are a dev description and have no new significance test.

The actual SAE is `sae_a17_qwen_raw_o_proj_1b_valid_full_20261009t182142z`: Qwen layer27 raw `self_attn.o_proj` output before residual addition,30000 latents/TopK32,244380 updates and1000002960 valid prediction tokens. Its final state SHA is1e16759da1ef1bad953d3df1bcf641c01b81edc87ca6b56d61b32251f41ebe64. It is the qualified actual1B output, not the prior normalized-MLP-input SAE or Smoke checkpoint. The dictionary stays frozen throughout this analysis.

For each pair, h0 is the same-rule trained endpoint's projection output and h1 is the different-rule trained endpoint's output, both for the same dev input. The SAE encodes each absolute output once, giving z0/z1 and reconstruction residuals u0/u1. The signed change is accounted as decoder change D(z1−z0), explicit residual change u1−u0 and measured numerical defect. The CE gradient is evaluated at the same-rule endpoint. The actual finite CE difference is retained alongside the gradient-weighted decoder/residual changes and the finite Taylor remainder. Subtracting the A200 account from the A800 account describes the dev interaction. Because the two A levels have different reference endpoints, this is a difference of two endpoint accounts, not one linearization of the whole interaction or a decomposition of the Adam training path.

The following are arithmetic means across all9 seeds and both B roles, preserving separate novelty panels. Every contrast saves both rule readouts; the interaction uses only each contrast's B rule. Units are nats/answer. The three signed components add to the finite dev interaction up to recorded arithmetic error.

| Dev novelty panel | Finite interaction | SAE decoder linear term | Explicit residual linear term | Finite remainder |
|---|---:|---:|---:|---:|
| Order-new |0.114125|0.004599|0.051953|0.057573|
| Combination-new |0.051010|−0.000716|−0.006226|0.057952|
| Equal combined |0.082567|0.001942|0.022863|0.057762|

The nine seed-level combined dev interactions range0.0723689–0.0973117, median0.0823579. Separately computed component medians do not have to add. The combined conditional CE difference within the fixed20-answer pool is0.081613; the answer-pool log-mass difference is−0.000954, giving full-vocabulary CE0.082567. This arithmetic does not establish an internal task mechanism.

The SAE's raw-energy-normalized reconstruction MSE over the recipient B rule is substantial: across36 pairs, median0.548377 at same endpoints and0.537822 at different endpoints. These are list-task measurements, not the DCLM training validation metric. Residual-displacement norm divided by full-displacement norm has median1.48649, range1.37617–1.61853; cancellation makes this ratio able to exceed1, so it is not an unexplained-percent estimate. Under this frozen dictionary and reader, the decoded linear term alone does not cover the main finite dev loss difference. The residual and finite remainder are essential. A full explanatory mechanism, shared/unique functional partition, feature causality and expert benefit remain unsupported; this does not show that no relevant feature exists.

Execution and eligibility: fresh75 strict inputs,72 actual matrix loads/800 tokenizer-oracle checks/40 CPU native rows and actual1B CPU4 checks passed. The earlier GPU-NOT-RUN22-file freeze stayed byte-identical. Root inspected the old main-analysis job as FAILED and released the four-H100 slot; an immutable launch extension records that release. The sole submission template created `pt-h6ke4emg` on the unchanged `h100-4-reserved`/`shphd-lite-0911` tuple at2026-10-10 09:27:19UTC. The embedded first4×800 reader qualification passed211/211; all36×800 passed1683/1683, with an independent finalization recheck of1685 conditions. Maximum native-tail CE error was0.0000185966; maximum projection-displacement identity relative error3.10245e−6; maximum SAE accounting identity relative error6.79216e−7. Frozen upstream activations, restored Base bytes and dictionary bytes passed. The bounded payload ended after181.43 seconds with exit0, zero training updates/tokens. Platform SUCCEEDED at09:31:23UTC /17:31:23Asia/Shanghai. All91 manifest files and all22 frozen files were independently hashed successfully. The initial local CPU invocations omitted the existing runtime.sh and failed import before payload outputs; corrected runtime invocation changed no scientific inputs. No GPU retry was needed.

Actual artifacts: [full execution root](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/endpoint_description/runs/actual1b_36pairs_20261009T2118Z), [all9 dev account](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/endpoint_description/runs/actual1b_36pairs_20261009T2118Z/description/descriptive_aggregate.json), [derived facts and separate panels](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/endpoint_description/runs/actual1b_36pairs_20261009T2118Z/endpoint_result_facts.json), [terminal engineering receipt](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/endpoint_description/runs/actual1b_36pairs_20261009T2118Z/terminal_verification.json), [platform terminal observation](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/endpoint_description/runs/actual1b_36pairs_20261009T2118Z/supervision/terminal_observation.json), [91-file manifest](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/endpoint_description/runs/actual1b_36pairs_20261009T2118Z/artifact_manifest.json), [independent hash check](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/endpoint_description/runs/actual1b_36pairs_20261009T2118Z/independent_postflight_20261010T0933Z.json), [actual output registration request](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/endpoint_description/runs/actual1b_36pairs_20261009T2118Z/registration_request_current_execution.json). Actual payload includes36 JSON/NPZ pairs, sparse same-call absolute z0/z1 including coordinates canceled in delta-z, dense decoder/residual/true changes and gradient-weighted arrays; no re-encoding substitutes the saved results. Requested representation asset: `analysis_a17_frequency_sae_actual1b_36pairs_20261009t2118z`; central registration receipt is pending root's sole catalog write at this append time. Researcher mechanism judgment and next scientific decision remain Unknown.

Registration completion: root registered `analysis_a17_frequency_sae_actual1b_36pairs_20261009t2118z`, independently verified92 actual file hashes including the manifest, and passed the selected strict check. [Actual registration receipt](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/endpoint_description/runs/actual1b_36pairs_20261009T2118Z/registration_request_current_execution_registered_outputs.json) and [fresh strict snapshot](/data/250010109/Research_System/assets/checks/2026-10-10_a17_outputs_20261010T093323Z.json) complete the previously pending artifact step. No frequency-policy scientific verdict changed.
