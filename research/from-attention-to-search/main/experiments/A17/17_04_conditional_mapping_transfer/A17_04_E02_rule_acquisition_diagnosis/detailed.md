# Detailed: A17_04_E02 rule acquisition diagnosis

Primary Anchor: [A17_04_01](../../../../problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/subanchors/17_04_01_rule_acquisition_diagnosis_anchor.md).  
Frozen Protocol: [protocol.md](protocol.md), revision `a17_04_e02_acquisition_diagnosis_v1`.  
Summary: [summary.md](summary.md). This record does not finalize scientific judgment.  
Result eligibility: CPU/data, historical readouts, Smoke and five-arm Full outputs are eligible for their bounded diagnostic/engineering roles. All finite budgets completed; independent analysis and selected strict Full access passed. Full platformSUCCEEDED and final physical-tensor/global-freeze checksPASS are separately recorded from scientific qualification. Researcher scientific judgment and question closure: `Unknown`.

## 0. Quick Recap

Purpose: identify whether the earlier old-rule failure is already present on seen training inputs, and compare finite optimization, trainable-scope and presentation repairs.

Hypothesis: at least one predeclared route can acquire both old command mappings within the budget. Credible rivals are inadequate exposure/optimization, unseen-input generalization difficulty and restrictive presentation/computation. No arm is required to succeed.

Experiment logic: inspect the three saved old endpoints on a fixed training panel and DEV, then independently restart five acquisition arms from the same Base. Each arm first performs tiny-set fitting and then restarts from Base for full acquisition. No new-mode update, sensitive-direction intervention, SAE or expert comparison is included.

Direct result so far: the historical endpoints have only44.5%–45.5% accuracy on seen training-panel inputs and44.375%–44.75% on DEV. Both-command success is4.5%–5.5% on training lists. Thus the earlier failure is not confined to unseen-list generalization. Five-arm Smoke and independent-process next-step recovery passed. All finite stages in Full job `pt-qsqimkvo` completed. Expanded-attention neutral armC and explicit-command armD qualify; A/B/E do not. C has100% in all four DEV cells at240 and1200 updates. D ends at86.75% combined with a minimum cell82%. This identifies practical routes, not a pure parameter-count mechanism.

Boundary: historical readouts are measurement of existing states, not new training replications. Smoke validates the implementation, not rule acquisition. All new arms use one seed and exposed DEV; this is diagnosis, not held-out confirmation or cross-task interference evidence.

## 1. Terminology / Definitions

| Term | Plain meaning and concrete computation | Unit | Why needed / cannot prove |
| --- | --- | --- | --- |
| Old mapping | Visible mode one; command甲 selects first word,乙 last word | One answer token | Both commands can be simultaneously satisfied; no contradictory full input labels |
| Training panel | Fixed200 training lists × two commands, evaluated without gradients |400 targets | Separates seen-input fitting from unseen-input performance; not independent confirmation |
| `order_new` | Unseen ordering of a familiar unordered triple |200 lists /400 targets | Tests order generalization; not entirely unseen content |
| `combination_new` | Previously unseen unordered triple |200 lists /400 targets | Tests new combinations from the same20-word vocabulary |
| Tiny fit |32 frozen training lists,64 targets, cycled for160 updates |3,200 targets processed | A fitting witness; success may be memorization |
| Paired success | Both command answers for the same list are full-vocabulary correct | Fraction of lists | Directly requires switching answer correctly, unlike a mean CE alone |
| Same argmax | The two commands produce the same full-vocabulary top answer | Fraction of lists | High values expose weak command-dependent switching; do not identify internal mechanism |
| Command response | Half the last-versus-first log-odds difference across commands | Nat | Positive mean alone is not reliable mapping acquisition |
| Qualification | Every command/panel DEV accuracy at least80% at the fixed endpoint | Minimum of four cell accuracies | Operational acquisition convention, not statistical confidence |

## 2. Anchor Link And Decision Point

The parent E01 could not interpret retention of an acquired rule because its old DEV cells were33%–54%. This child asks which bounded route can supply a qualified old-rule starting point. A/ B compares optimizer routes at fixed scope; B/C expands trainable attention; B/D changes command wording; B/E changes list separator. The decision is a future choice of acquisition route, not an expert split. No automatic transfer follow-up is authorized by a successful diagnostic arm.

## 3. Protocol Freeze, Conformance, And Deviations

Frozen at2026-10-11 21:18:16.854727 Asia/Shanghai (13:18:16.854727UTC);45 decision-bearing files are listed in [/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/freeze.json](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/freeze.json). Both language contracts were snapshotted before GPU execution.

| Registered item | Actual snapshot | Status / eligibility impact |
| --- | --- | --- |
| Delegated finite diagnosis, no intermediate approval | User authorized diagnosis, data/parameter assessment and feasible parameter-budget training | Authorized scope; no manufactured mechanism approval |
| Registered Base and original old TRAIN/DEV | Current strict input check passed for Base/tokenizer/source data and three saved old families | Qualified inputs |
| Derived three views, twelve files | Generated after contracts; actual manifest and strict derived-data check passed | Qualified diagnostic data |
| Five arms, common Base, seed29, batch20 | All five Smoke and Full arms completed the frozen specification | Conforms; one diagnostic training seed |
| FP32/nativeSDPA/freeze and exact resume | Smoke environments and five independent recovery receipts passed | Engineering role only |
| Full tiny160 plus independent main1200 | After qualified Smoke, all five arms reached160/1200 | Workers/analysisPASS;6,800updates/136,000targets |
| Formal TEST exclusion | Formal generator/trainer/analyzer do not load original TEST | Diagnostic scope preserved; prior exposure caveat below |
| Prior-endpoint artifact name | Protocol names a conceptual `prior_endpoint_diagnostic.json`; actual per-seed files are `audit/seed_N/{train_panel,dev,completion}.json` | File organization difference; same registered readout |
| Resume stage metadata | Recovery receipt says legacy `full_data`; actual restored directory and loop stage are `main` | Metadata alias only; exact replay still checked actual main state |
| Execution receipt at creation | Receipt says RUNNING and Full awaiting qualification; subsequent direct platform receipt records Smoke success and Full submission | Historical receipt preserved, not overwritten as final completion |

No training retry, arm exclusion or post-result budget amendment occurred. All five arms completed. Source/config/data remain frozen. Final physical-tensor and global-freeze checks separatelyPASS; platform success cannot replace them.

Exposure boundary: earlier CPU QA inspected the parent TEST schema/tokenization. An initial audit deserialized old evaluation JSON containing DEV and TEST prediction records while filtering all model-readout computations to `split == 'dev'`. Therefore TEST prediction records were previously opened; no TEST model result selected this diagnostic's settings or is reported as new evidence. This diagnosis is openly DEV exploratory. A future confirmatory transfer run needs new heldout data.

Host CPU qualification initially encountered an ONNX/protobuf import incompatibility. It passed under the inspected mounted runtime's `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python`; no Base-image package mutation or scientific setting change occurred.

## 4. Actual Setup

### Data and supervision

Derived data asset: `data_a17_mapping_acquisition_diagnostic_v1`, sourced from `data_a17_conditional_mapping_v1`. Each view has TRAIN2,400, DEV800, training-panel400 and tiny64 records. TRAIN is1,200 paired lists; DEV has400 pairs equally split between the two panels. The training panel consists of ten complete20-list word-rotation cycles, chosen deterministically before GPU results. Tiny uses32 fixed lists from its first two cycles. Panel/tiny record IDs are TRAIN subsets and stay identical underneath the presentation changes.

All records preserve mode1, old world, command alias甲/乙, underlying words, targets and source links. `neutral` preserves the spaced list and neutral command. `explicit` replaces甲/乙 text with `取第一项`/`取最后一项`, leaving command aliases in metadata. `normalized` preserves neutral commands and replaces list spaces by `、`. It does not combine the explicit wording change.

The20 answer words are 红、黄、蓝、黑、绿、白、紫、灰、金、银、猫、狗、鸟、鱼、牛、马、羊、虎、龙、花. Answer targets and prefix-plus-answer concatenation boundaries are verified single tokens. The original spaced input sometimes encodes a candidate differently from its answer token; this is not an answer-label boundary error. The normalized presentation passed all full-prefix candidate-ID guards. Source/split/label agreement, paired commands, balanced vocabulary/positions and TRAIN/DEV exclusions passed [/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/data/acquisition_v1/qualification.json](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/data/acquisition_v1/qualification.json).

Only the next answer token contributes CE. Input/padding tokens never enter the training-target denominator. Full-vocabulary argmax determines correctness.

### Architecture and conditions

Registered model/tokenizer: `model_qwen3_0p6b_base_official_a5`, `tokenizer_qwen3_0p6b_base_official_a5`; exact Base is `/data/250010109/model_cache/Qwen3-0.6B-Base-official`. Native28-layer Qwen3, FP32, SDPA, evaluation mode, deterministic algorithms, noTF32. No old adapter initializes a new arm.

| Arm | Input | Trainable tensors / parameters | Optimizer |
| --- | --- | --- | --- |
| A `o_sgd` | neutral | Final layer27 `self_attn.o_proj.weight`,1,024×2,048 /2,097,152 | Plain SGD,LR0.01 |
| B `o_adam` | neutral | Same one matrix /2,097,152 | AdamW,LR1e-4 |
| C `attn4_adam` | neutral | Layers24–27 attention q/k/v/o,16 weights /25,165,824 | AdamW,LR1e-4 |
| D `explicit_o_adam` | explicit | Same final o matrix /2,097,152 | AdamW,LR1e-4 |
| E `neutral_normalized_o_adam` | normalized | Same final o matrix /2,097,152 | AdamW,LR1e-4 |

C has12times as many trainable parameters, but changes trainable computation as well as count. Every forward pass recomputes native upstream processing; no fixed representation cache is reused. Biases, q/k norms, MLP, embeddings, final norm and output head stay frozen. Runtime tensor inventory is checked against the safetensors header audit.

Every update accumulates4microbatches×5records =20 valid answers, with aggregate gradient clipping1. AdamW uses betas(0.9,0.999),eps1e-8,decay0, foreach/fused false. SGD has no momentum/decay. Constant LR, no warmup/early stopping or adaptive extension.

### Budgets, saves and compute

Each arm independently performs tiny160updates=3,200targets, then resets exact Base/trainable weights, optimizer and RNG before main1,200updates=24,000targets. Actual five-arm totals are16,000 tiny and120,000 main targets. Tiny fitting does not warm-start main. Main records0,1,240,600,1200; tiny0,1,160. Tiny endpoints additionally evaluate training/DEV panels. Saved states require the immutable Base and include every trainable tensor, optimizer/RNG/schedule/counters/order/source identities.

Smoke ran3updates per stage per arm:30updates/600targets across five arms. The external-process replay added one update per stage per arm:10updates/200diagnostic targets. These are separate from Full budgets. Smoke produced30 saved states (0,1,3 for two stages × five arms).

Resources: one node/four H10080GB SXM5, `h100-4-reserved`, ACP `share-space`/`share-cluster`, spec `n6ls.iu.i40.4`, image `registry.cn-sh-01g.sensecore.cn/ccr-zhicheng-03/shphd-lite-0911:shphd-mig-20260910161423`. Lanes0/1/2/3 runA/B/C/D; lane0 thenE. Workers are independent arms, notDDP. Both jobs have a7,200-second ceiling. Answer exposures are matched, FLOPs/wall time/prefix token counts are not.

### Code, freeze and reuse

[/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/source/diagnose.py](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/source/diagnose.py) adapts the inspected parent AnswerLM/manualSGD/observability implementation. `native.py`, `carriers.py` and `runtime.sh` were copied from that inspected parent; new code expands named parameters, optimizer state, fitting controls and paired readouts. Clean-trainer source audit/reuse index and observability contracts were inspected; its MoE/DDP architecture and retired production configs are not reused. Source lineage is in [/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/provenance/reuse_decisions.json](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/provenance/reuse_decisions.json).

| Object | SHA256 |
| --- | --- |
| Run config | `2c3450225bac11384df53ac077f612dc64b964111ec745a6c97057ace8b8df1e` |
| Data manifest | `05dfb9ac05ebf20dcf560b51d880acdb9472596b2a0a346aa8401d0dc9438a89` |
| Trainer | `b9f73eb4d797a04f20e9b0aa7b6f4448daea5a3aebfda9b764ba8694ceef74f6` |
| Analyzer | `baa738e4908cf662ae7a6f9894bd4d93441eb6d46ec3436ad5162402f2eecb0f` |
| Frozen EN Protocol | `1ddc77dce61f26c5ef804d2375bf33c6dc1adfe1facf67b2e4895b04b76d0126` |
| Frozen CN Protocol | `86fbd7cc8c64cc050090eebe3752e87bf0953b8475212d5e6dbb990322ec4a7d` |

## 5. Metrics And Registered Decision Rules

For each command/panel, full-vocabulary accuracy is correct targets divided by200. The main primary quantity is the minimum of the four DEV accuracies at step1200. Qualification requires all four at least0.80; the combined mean cannot rescue a failed cell. Report both panels separately and combined, plus train-panel/tiny readings. Tiny has no new binary qualification gate.

For a list candidate set S and true answer y, measure CE, mass P(S), access loss and conditional selection:

\[
-\log p(y\mid x)=-\log P(S\mid x)-\log\frac{p(y\mid x)}{P(S\mid x)}.
\]

For paired commands, define s as last-versus-first log probability and command response:

\[
s_c=\log p(L_3\mid x_c)-\log p(L_1\mid x_c),\qquad a=(s_{乙}-s_{甲})/2.
\]

Save correct-versus-opposite margin, full-competitor margin/ID, paired success and same-argmax rate. CE accounting does not identify internal causal functions. Preserve exact counts and all milestones. One new training seed gives no population intervals or significance claim; historical three-seed readouts do not multiply the new-arm replication count.

Seven TensorBoard tags follow the observability contract. Actual20 answer targets/update set token coordinates; prefix tokens are separately counted. Per-step metrics include raw/clipped gradient norm, actual step norm, pre-step weight norm, relative displacement and throughput. Throughput includes gradient/update/norm/freeze-version checks and excludes evaluation/checkpoint/TensorBoard time. Frozen versions/bytes, finiteness, no-op evaluation, counters and independent recovery protect engineering eligibility.

## 6. Evidence Lineage

| Claim / decision | Criterion and raw source | Computation / aggregation | Observed value | Eligibility / boundary |
| --- | --- | --- | --- | --- |
| Failure already on seen lists | Fixed training panel at three original240-update states; `/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/audit/seed_N/train_panel.json` |400targets/state;200paired lists | Accuracy44.5%,44.5%,45.5%; joint4.5%,5.5%,4.5% | Eligible existing-state diagnosis; panel is not all training data |
| Commands often select the same answer | Same raw files and their `paired` field |Same full-vocabulary argmax on each pair |85.5%,85%,87% on training panel | Observable weak switching, not internal mechanism |
| DEV also low | `/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/audit/seed_N/dev.json` |800targets/state, two panels |44.5%,44.75%,44.375% | ExposedDEV diagnosis |
| Trainer/restore runs correctly | `smoke_gate.json`, worker telemetry/frozen manifests, five resume receipts |Five arms × two independent restarted stages |All worker/replay checksPASS | Engineering only |
| Actual Smoke saves available | Registration receipt and selected strict output check |30actual members/10families plus1nativeanalysis family |11IDs`REGISTERED_ACCESS_PASS` | Availability does not imply scientific acquisition |
| Which acquisition route works | Four-cell criterion and `analysis/results.json` |One training seed, fixed1200endpoint |C100% every cell;D minimum82%;A43%/B58%/E46% minima |Two operational routes qualify; no automatic follow-up approval |
| Complete independent readout check |`analysis/analysis_manifest.json`|91files/46,560records;40actual Full state hashes|Max loss identity error9.996755e-7|Actual hash/size and manifest validation; no claim of independently deserializing all tensors|

## 7. Main Results

### Historical old endpoints: eligible bounded diagnosis

| Original seed | Train CE | Train accuracy | Train both-command success | Train same argmax | DEV CE | DEV accuracy | DEV both-command success | DEV same argmax |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
|29|1.147346|44.50%|4.50%|85.50%|1.170393|44.50%|7.25%|85.00%|
|43|1.151172|44.50%|5.50%|85.00%|1.171855|44.75%|7.00%|85.25%|
|71|1.147121|45.50%|4.50%|87.00%|1.170798|44.375%|8.00%|80.75%|

These are direct aggregate readings from the per-seed files above. Low performance on this seen panel weakens an explanation based only on unseen-list generalization. It does not prove no training input was fitted or locate the restrictive computation.

### Smoke: engineering evidence

Job `pt-2x5gujhd` succeeded. All five arms completed tiny/main3updates from independent Base starts, finite native evaluations and exact fresh-process step1→2 recovery for both stages. Seven telemetry tags and frozen parameter guards passed.30state files were registered as10checkpoint families, plus one native-analysis family. No scientific accuracy threshold was applied toSmoke.

### Full acquisition

All five arms completed the frozen budget. Values below are from [independent results](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/analysis/results.json) and [complete trajectories](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/analysis/trajectories.csv). Each arm has one training seed; the seen panel has400 targets and DEV has400 per panel/800 combined. C/D qualification is operational, not researcher-owned question closure.

| Arm | Seen train panel | Order-new DEV | Combination-new DEV | Combined DEV | Minimum cell | DEV both-command correct | DEV same argmax | First saved qualified update |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
|o_sgd|51.75%|47.75%|51.5%|49.625%|43%|11%|80.75%|Not reached|
|o_adam|82.25%|64.25%|72.75%|68.5%|58%|39.5%|52.75%|Not reached|
|attn4_adam|100%|100%|100%|100%|100%|100%|0%|240|
|explicit_o_adam|97.25%|84.75%|88.75%|86.75%|82%|73.75%|22.75%|600|
|neutral_normalized_o_adam|81%|58.25%|72.75%|65.5%|46%|36.75%|50.5%|Not reached|

Endpoint command/panel cells,200targets each:

| Arm | 甲/order | 乙/order | 甲/combination | 乙/combination |
| --- | ---: | ---: | ---: | ---: |
|o_sgd|52.5%|43%|59.5%|43.5%|
|o_adam|58%|70.5%|77%|68.5%|
|attn4_adam|100%|100%|100%|100%|
|explicit_o_adam|82%|87.5%|90%|87.5%|
|neutral_normalized_o_adam|46%|70.5%|74.5%|71%|

Tiny and main are independent training trajectories. Separate tiny fitting from its own DEV generalization:

| Arm | Tiny64 accuracy | Tiny both-command success | DEV after tiny-only training |
| --- | ---: | ---: | ---: |
|o_sgd|51.562%|9.375%|46%|
|o_adam|85.938%|84.375%|48.75%|
|attn4_adam|100%|100%|100%|
|explicit_o_adam|100%|100%|61.75%|
|neutral_normalized_o_adam|81.25%|78.125%|45.125%|

B fits85.94% of tiny targets but its tiny trajectory reaches only48.75% DEV; D fits100% tiny but61.75% DEV. Fitting a small set is distinct from generalization. C reaches100% on both, providing a feasible conditional-learning witness for this task rather than an impossible-rule explanation.

Main endpoint output decomposition, means over800 DEV targets. Candidate mass is for the three list words; loss units are nat:

| Arm | Answer CE | List candidate mass | Access loss | Conditional selection loss | Command response a |
| --- | ---: | ---: | ---: | ---: | ---: |
|o_sgd|1.0319582|97.898%|0.021794|1.010164|0.110277|
|o_adam|0.70223597|99.747%|0.002567|0.699669|0.953971|
|attn4_adam|2.1249036e-07|100%|≈0|≈0|27.197257|
|explicit_o_adam|0.33283179|99.976%|0.000242|0.332590|2.423928|
|neutral_normalized_o_adam|0.78717761|99.858%|0.001430|0.785748|0.799155|

A already allocates97.90% mass to the list but achieves49.625% accuracy; B/E exceed99.7% mass yet achieve68.5%/65.5%. Candidate concentration therefore does not establish conditional selection. C reduces conditional selection error to approximately0. Its raw training-panel conditional mean is−2.95e-8 from mixed FP32 answer CE and double candidate-logmass arithmetic. Mathematical conditional CE is nonnegative; preserve the raw value but interpret it as approximately0, not negative-loss gain. The independent maximum identity error9.996755e-7 is below the registered2e-5 tolerance.

C already has100% in all four cells at the original240-update exposure; A/B/D then have44.5%/48.75%/71.875% combined DEV. Its success does not require1200updates, but trainable location, parameter count and optimization geometry remain confounded. D's Base DEV is already58.125%, versus33.25% for neutral wording. Its repair may exploit pretrained semantics and is not equivalent to acquiring the original neutral mapping. E falls below B and does not qualify; this weakens a sufficient-cause account based only on spaced input encoding, without ruling out all tokenizer effects.

Actual main mean step norms areA0.009976,B0.033880,C0.005446,D0.034135,E0.034078; cumulative path lengths are11.97078,40.65580,6.53505,40.96238,40.89403. C's near-zero later gradients lower its full-history mean; this is not a matched-state update-norm comparison. Full evidence is in [training_exposure.csv](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/analysis/training_exposure.csv).

### Final engineering, reproduction and precision checks

- [Platform terminal status](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/full_terminal_status.json): Full `pt-qsqimkvo` SUCCEEDED at2026-10-11 21:34:17 Asia/Shanghai (13:34:17UTC), created21:24:04 and started21:24:55. Smoke finished21:23:32. Neither job retried.
- [Post-execution freeze check](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/post_execution_freeze_check.json): all45 frozen file hashes match, including Base, old checkpoints, source, config, data and contract snapshots.
- [Independent tensor audit](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/independent_checkpoint_tensor_audit.json): after selected strict output accessPASS, ten actual tiny/main endpoints across five arms were deserialized. Weights/optimizer are finite and parameter counts/step/token coordinates match. NewA's240-update o_proj is byte-for-byte identical to the originalseed29 old240-update tensor. This verifies reproduction of the original path, not a scientific discovery.
- [Precision audit](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/precision_decomposition_audit.json): deriving conditionalCE from saved double `target_logp`/`list3_logmass` yields minimum0. The native mixed-precision single-record minimum−3.33077e-7 falls within the existing engineering tolerance. C's double DEV mean4.20291e-8 and training mean1.41525e-8 are approximately0. Frozen native values were not overwritten.

The frozen analyzer independently checks91prediction files/46,560records and all40Full state hashes/sizes/manifests. The additional audit deserializes ten actual endpoints; do not conflate this with independently deserializing all40states. No additional GPU update or subsequent transfer training occurred.

## 8. Stage Evidence And Failure Decomposition

| Stage | Evidence | State | Ruled out / remains live |
| --- | --- | --- | --- |
| CPU answer loss / Adam restore | `configs/cpu_qualification.json` |PASS; accumulated-vs-total gradient maxerror1.49e-8 on toy |Qualifies helper arithmetic, not real-model acquisition |
| Derived data | Manifest/qualification plus current strict assets |PASS |Wrong labels/pairs/answer boundary not observed; presentation remains a candidate learning factor |
| Prior seen/DEV readout | Three existing old states |Complete |Failure is not only DEV generalization; optimizer/scope/presentation unresolved |
| Real GPU Smoke / external replay | Smoke gate/receipts |PASS |Smoke validates finite trainer/freeze/replay; acquisition is separately read from Full endpoints |
| Full repair comparison | Five frozen endpoints |Complete; C/D qualify, A/B/E do not|A feasible route exists; universal capacity or count-only mechanism remains unidentified|
| Independent analysis / Full assets |91files/46,560records/40states;11Full IDs|AnalysisPASS,strictPASS|Single-seed DEV eligibility; final tensor/globalfreeze audit separately PASS|

No universal physical prior or mathematical capacity limit is falsified. The feasible C route counters a strong task-impossibility explanation. No observed bug explains the old learning failure. Positive candidate mass, positive mean response and lowCE remain inadequate substitutes for paired acquisition.

## 9. Full Experiment Record

Round2026-10-11:

1. Question: is the prior failure seen-input fitting or only unseen generalization, and can bounded optimizer/scope/presentation changes repair acquisition?
2. Setup: exact registeredBase; three existing old240states evaluated only, and five freshBase arms with frozen scope/optimizer/seed/budgets.
3. Training data: originalold TRAIN transformed into neutral/explicit/normalized views; identical list/target identities; tiny independent from main.
4. Evaluation: fixed400-target seen panel,800-target DEV with two panels, and64tiny fitting targets. No new confirmation set; originalTEST exposure caveat retained.
5. Result: CPU/data and Smoke/restorePASS; historical seen/DEV readings above; all finite arms completed,C/D qualify andA/B/E do not.40Full states, independent analysis and strict access are complete. PlatformSUCCEEDED and final tensor/freeze auditsPASS are separately recorded.
6. Insight/boundary/next: the old state often fails to switch on seen lists, so optimizing a qualified starting point is a warranted diagnostic. The frozen comparison is complete. AI recommendation: if preserving the neutral-command question, consider C's qualified240-update state. Researcher scientific next decision remainsUnknown.

## 10. Interpretation

The observed old-state pattern is compatible with candidate-word adaptation plus weak command-controlled selection. It is not enough to say the training rules were learned and only failed to generalize. The practical comparison is now available: extending originalSGD does not qualify; Adam improves but remains below threshold; expanded attention qualifies on neutral commands, explicit wording offers another route, and separator normalization alone does not qualify. C identifies a usable trainable computation range, not a pure parameter-count mechanism.

## 11. Claim Boundary

Can claim: historical seen fitting is also poor; five finite arms completed; C qualifies on this neutral task and D on explicit wording; complete payloads, independent readouts and current strict access checks pass.

Cannot claim: universal0.6B capacity limits, absolute impossibility of the last projection, pure count or isolated tokenization causation, acquired-rule interference, expert separation benefits, unseen confirmation or statistical replication.

## 12. Next Decision

Researcher scientific next decision: `Unknown`. Finite training and independent readout analysis are complete; final tensor/freeze verification also passed; bilingual delivery is operational closeout. AI recommendation: retest transfer from a qualified neutral-command starting point using new heldout data; this is not automatically in the current execution scope. No additional arm, seed, budget or transfer task is implied.

## 13. Artifact Manifest

| Artifact | Purpose / producer | Identity and completeness | Claim eligibility |
| --- | --- | --- | --- |
| [Frozen manifest](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/freeze.json) | Before-GPU45file binding |Actual hashes and timestamp present |Engineering provenance |
| [Run config](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/config.json) | Exact five-arm finite settings |SHA in§4; complete |Frozen diagnostic design |
| [Data manifest](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/data/acquisition_v1/manifest.json) | Source/derived views and IDs |SHA in§4;12files complete |Data provenance |
| [Data qualification](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/data/acquisition_v1/qualification.json) | Labels, splits, token boundaries, normalized offsets |PASS; actual generator output |Data eligibility, not learning |
| [Current inputs](/data/250010109/Research_System/assets/checks/2026-10-11_a17_acquisition_input_access.json) | Selected original assets |StrictPASS before use |Input access |
| [Derived access](/data/250010109/Research_System/assets/checks/2026-10-11_a17_acquisition_derived_data_access.json) | Derived release |StrictPASS |Derived data access |
| [Smoke gate](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/smoke_gate.json) | Worker/replay/historical availability |PASS, five arms |Engineering |
| [Smoke receipt](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/smoke_terminal_status.json) | Direct ACP state |`pt-2x5gujhd`,SUCCEEDED |Platform completion only |
| [Smoke registration](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/smoke_registration_receipt.json) |10checkpoint families +1native family |11IDs,30actualstates |Actual payload availability |
| [Smoke strict access](/data/250010109/Research_System/assets/checks/2026-10-11_a17_acquisition_20261011t130809z_smoke_outputs.json) | Selected actual Smoke outputs |PASS |Access/schema, not science |
| [Historical audit root](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/audit) | Three old-state train/DEV readouts |Complete per-seed files |Existing-state diagnosis |
| [Full launch](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/full_launch_contract.json) | Exact command/profile/scope |`pt-qsqimkvo` receipt in submit log |Submission, not completion |
| [Full outputs](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/full) | Finite tiny/main trajectories and actual states |Five arms complete;40actual states|Single-seed DEV diagnostic eligibility|
| [Analyzer](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/source/analyze.py) | IndependentCPU CE/paired/counter/manifest recomputation |Frozen source SHA in§4;actual independent analysisPASS|Not scientific approval |
| [Full platform terminal](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/full_terminal_status.json) | Direct ACP terminal |`pt-qsqimkvo`SUCCEEDED21:34:17Asia/Shanghai|Platform completion separate from learning gate|
| [Post-execution freeze](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/post_execution_freeze_check.json)|45frozen-file hash recheck|PASS|No design/source/input drift|
| [Actual endpoint tensors](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/independent_checkpoint_tensor_audit.json)|Ten deserialized endpoints plus A240 reproduction|PASS,A240 byte-exact|Engineering reproduction, not mechanism support|
| [Precision decomposition](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/precision_decomposition_audit.json)|Independent saved-logp64 recomputation|ConditionalCE nonnegative; native near-zero negatives are rounding|Original native records retained|

The Smoke IDs follow `adapter_a17_04_acquisition_20261011t130809z_smoke_{ARM}_{tiny|main}`. The native family is `analysis_a17_04_acquisition_20261011t130809z_smoke`. Individual member manifests retain paths, byte sizes and hashes. Full now has40actual states in10checkpoint families plus1native-analysis family,11IDs total. [Full registration](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/full_registration_receipt.json) and [current strict access](/data/250010109/Research_System/assets/checks/2026-10-11_a17_acquisition_20261011t130809z_full_outputs.json) pass. Smoke/Full total70actual states in20checkpoint families plus two native-analysis families. No bulk payload is copied into the research repository.

## 14. Links And Reproduction

- Protocol: [English](protocol.md), [Chinese](protocol_cn.md).
- Source: [/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/source](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/source).
- Reuse audit: [/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/provenance/reuse_decisions.json](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/provenance/reuse_decisions.json).
- Resource receipt: [/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/execution_certificate.md](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/execution_certificate.md).
- Run: [/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z); logs: [/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/logs](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/logs).
- Reproduction uses the frozen run config and registered immutableBase. Worker example: `python source/diagnose.py --config RUN/config.json --run RUN --arm o_adam --phase full --rank 1` under the inspected runtime. This is documentation, not authorization to duplicate an existing job.
- Jobs: Smoke `pt-2x5gujhd`; Full `pt-qsqimkvo`. No resubmission at this snapshot.
