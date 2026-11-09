# Detailed: A17_04_E01 conditional mapping transfer

Primary Anchor: [A17_04](../../../../problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/17_04_conditional_mapping_transfer_anchor.md).
Frozen Protocol: [Protocol](protocol.md), revision `A17_04_E01_r1`; frozen at `2026-10-11T09:53:00.623986+00:00`.
Summary: [Summary](summary.md).
Evidence: qualified measurements; insufficient for the registered learned-old-mapping retention hypothesis. Descriptive verdict: `INSUFFICIENT_OLD_MAPPING_NOT_ACQUIRED`. Scientific mechanism acceptance/closure: `Unknown`.

## 0. Quick Recap

Full completed three seeds and four stages each: 2,880 updates, 57,600 valid answer targets. Smoke, four independent exact replays, source freeze and Full worker checks passed. All 120 saved matrix/training states were verified and registered.

Old mapping did not meet the registered acquisition prerequisite: DEV command/panel accuracy33%–54% versus80%. On combined TEST, reversal gave −0.005165nat less old answer-advantage improvement than consistency, but both old CE and mean advantage improved. Old CE benefit was dominated by greater three-word candidate mass, while conditional three-word selection slightly worsened. New mapping qualification and joint feasibility also failed. Thus this run supplies bounded probability-update facts, not a retained-rule interference mechanism or a separation-utility conclusion.

## 1. Terminology / Definitions

| Term | Plain meaning / computation | Unit / role | Cannot prove |
|---|---|---|---|
| Old/new mode | Visible mode one/two in prefix | Conditional input | Internal routing |
| Consistent/reversed | Keep/swap 甲 FIRST and 乙 LAST | Mapping treatment | Intrinsic contradiction |
| Answer advantage | Correct endpoint log probability minus opposite endpoint | nat; primary reader | Full-vocabulary accuracy |
| List access/selection | Mass on three list words / correct share within them | CE, nat | Distinct internal functions |
| Mode-command response | Command difference of LAST-versus-FIRST log odds | Exact output coordinates | Parameter modules |
| Joint feasibility | Continue with both modes and extra old labels | Feasibility witness if successful | Equal-supervision winner or failed capacity proof |
| Unseen order/combination | New permutation of trained triple / unseen unordered triple | Separate heldout panels | Unseen vocabulary transfer |

## 2. Anchor Link And Decision Point

The user activated a sibling task-relation question, rather than a fourth experiment under A17_03. The merger means one consistent/reversed mapping intervention and its diagnostic readers. The earlier component/trajectory work kept tasks fixed; this experiment changes their relation. Both commands are old-supervised, so missing-position completion is not tested. One future researcher decision remains whether the conditional-mapping evidence warrants comparing shared/separate parameters. This insufficient result does not decide architecture utility.

## 3. Protocol Freeze, Conformance, And Deviations

| Registered item | Expected | Actual | Status / eligibility impact |
|---|---|---|---|
| Scope | Implementation/Smoke/Full, no intermediate approval | User's explicit adopted merger and completion request | Authorized; scientific verdict stays Unknown |
| Frozen scientific body/source | English/Chinese contracts, config/data/code snapshots |21 frozen files verified before/after Smoke and Full | PASS; no scientific change |
| Data |2,400 records/world train;800/world DEV/TEST | Physical train7,200/DEV2,400/TEST2,400 across three worlds | Data schema/split/balance PASS |
| Task/model/objective | Visible mode+neutral command; answer CE; only last o_proj | Frozen config and every worker's freeze guard | PASS engineering |
| Conditions/budget |3 seeds×4 stages×240 updates |2,880 updates,57,600 targets; stage-local records | Complete |
| Checkpoints | Milestones0/1/16/50/120/240; common old branch start |72 Full states,48 Smoke states;9 branch-zero byte checks | PASS |
| Resume/telemetry | Four external exact replays, required scalar tags | Four resume exits0 and stage telemetry checks | PASS |
| Old acquisition | DEV every command/panel≥80% |33%–54%, three seeds fail | Insufficient learned-rule interpretation; facts retained |
| Primary effect | Fixed240-new-update combined TEST paired margin |−0.005165nat; three negative seeds; magnitude<0.01 | Small descriptive relative effect, no support verdict |
| Comparable skill/joint | Prespecified DEV acquisition readers | Six comparable points NOT_REACHED; joint FEASIBILITY_UNKNOWN | Reader unavailable; no capacity proof |
| Asset gate/order | Strict saved-output check before analysis use | Initial enum error/strict exit2; analysis began prematurely; corrected gate and rerun | Recorded deviation; corrected factual analysis only |

The registry initially used invalid enum `CHECKPOINT_STATE_PRESENT` for28 adapter families. Correction to `MODEL_STATE_PRESENT` changed metadata only. Actual payloads/hashes, data/config/source and GPU training were unchanged. The initial strict check exited2; analysis nevertheless started. Its provisional outputs remain in `analysis/attempts/pre_access_enum_fix`. After schema correction, the30-output strict snapshot passed and deterministic analysis was rerun. `results.json`, `paired_table.csv` and `descriptive_sample_table.csv` are byte-identical to the provisional versions. This repairs the factual handoff; it does not erase the execution-order deviation. [Correction](/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/runs/mapping_20261011T095038Z/registration/schema_correction.json) and [reanalysis receipt](/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/runs/mapping_20261011T095038Z/registration/reanalysis_after_strict_access.json) preserve it.

No GPU retry, adaptive training extension, seed exclusion, scientific-body amendment or result-driven metric change occurred. Full platform job `pt-qs6ndgat` is SUCCEEDED with terminal update `2026-10-11T10:06:57.95841Z`. Worker completion and scientific eligibility remain separate from platform state.

## 4. Actual Setup

Run: `/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/runs/mapping_20261011T095038Z`.
Input IDs: `model_qwen3_0p6b_base_official_a5`, `tokenizer_qwen3_0p6b_base_official_a5`, `data_a17_conditional_mapping_v1`.
Parent: `/data/250010109/model_cache/Qwen3-0.6B-Base-official`.
Trainable: final attention `model.layers.27.self_attn.o_proj.weight`,1,024×2,048. Upstream/downstream weights frozen; FP32, native SDPA, deterministic, no dropout/TF32. Frozen upstream input is unchanged for a fixed input; projection displacement equals matrix increment times that input, while downstream prediction/loss changes remain nonlinear.
Objective: mean one-answer CE; manual SGD LR0.01, clip1, no momentum/decay/auxiliary loss. Micro5×accum4 gives20 valid answers/update. Four workers handle independent cases, not data-parallel replicas.

Full has training-order seeds29/43/71; all begin with identical pretrained weights, not different random weight initializations. Each old,consistent,reversed,joint stage has240 updates. Old and each primary new stage process4,800 answers, two deterministic passes. Joint processes2,400 old+2,400 new in one underlying-list pass: five lists/update, two commands/mode. It has extra old supervision and half the primary branch's new exposure. All save/eval milestones0/1/16/50/120/240 exist. Checkpoints store trainable matrix and optimizer/scheduler description, RNG, cursor/order, steps/targets, parent/config/stage identities. No full Base model was re-exported; each adapter needs its exact parent. Smoke has four cases including a duplicate seed29 case, three updates/stage,48 total updates/960 targets. Four independent resume next-steps process80 targets separately. Six equal-norm diagnostic updates use20 source answers each but are not counted as cumulative training trajectories.

20 answer words: 红、黄、蓝、黑、绿、白、紫、灰、金、银、猫、狗、鸟、鱼、牛、马、羊、虎、龙、花. Registered tokenizer IDs are in the data manifest. Generation seed20261011 partitions57 cyclic triple orbits:30 train,10 DEV-combination,10 TEST-combination,seven unused. Training gives1,200 lists/two commands; each DEV/TEST panel200 lists/two commands/world. Every world has2,400 train and800 DEV/TEST records; each physical file contains three worlds. Underlying content is shared across modes intentionally; primary new training contains no old full prefix. Two new worlds have identical prefixes/order and target histograms, differing only in mapping labels.

DEV and TEST use familiar words. Order panels reuse trained unordered triples with new permutations; combination panels use absent triples. DEV only selects the prespecified comparable point. Full mechanically records TEST at registered milestones, but those values select no stop, budget, labels, hyperparameters or checkpoints. Interpretation occurred after bounded training. Single template, pretrained parent and last-matrix-only learning bound the scope.

## 5. Metrics And Registered Decision Rules

Primary \(E_s=\Delta M_A^{reversed}-\Delta M_A^{consistent}\) uses old gold-versus-opposite log-probability margins after240 new updates, relative to the same old endpoint. Commands and panels equal; report panels separately and combined. Seed is the replication unit. Report individual effects, mean,range/sample SD without significance/population-confidence claims. Stable negative operational convention requires all3<0 and mean≤−0.01nat, plus qualified old/new learning. Old DEV qualification requires each command/panel≥0.80. New useful learning requires combined TEST CE gain≥0.01nat or accuracy gain≥1pp. The latter tests learning, not rule mastery.

Comparable-level secondary reader uses earliest saved new DEV point with both panels≥0.80. None exists. Joint success would require each mode/panel DEV≥0.80; failure leaves feasibility Unknown. Thresholds are delegated report conventions, not researcher scientific confidence judgments. Failure of the acquisition prerequisite takes precedence over using directional effects as retention evidence.

For list set \(S\), CE equals access \(-\log\sum_{w\in S}p(w)\) plus selection \(-\log[p(y)/\sum_{w\in S}p(w)]\) exactly. Also record pool20 mass/conditional CE, full argmax, strongest wrong token, endpoint/full-competitor margins. Define \(s_{m,c}=\log p(L_3)-\log p(L_1)\), \(a_m=(s_{m,乙}-s_{m,甲})/2\), \(q_m=(s_{m,乙}+s_{m,甲})/2\), \(C=(a_1+a_2)/2\), \(K=(a_2-a_1)/2\). These are output coordinates. With balanced old commands, \(a_1\) equals mean old endpoint margin; this identity is not independent mechanism evidence.

## 6. Evidence Lineage

| Claim / registered criterion | Raw artifact and computation | Aggregation / observed value | Eligibility / limitation |
|---|---|---|---|
| Old prerequisite | Full `old_endpoint.json`/DEV; `launch/analyze.py`, old_acquisition | Each seed/command/panel33%–54%; all fail80% | Measured, insufficient for well-acquired retention |
| Primary effect | Full branch `eval_00240.json`; `analysis/results.json` primary / `paired_table.csv` | Three paired seed effects, equal panel;mean−0.005165nat | Bounded relative probability effect; prerequisite fail |
| Candidate explanation | Same TEST records; pooled_endpoint_reader; exact list3 CE split | Old ΔCE/access/selection table below | Exact output accounting; no unique internal cause |
| Conditional new response | Same paired lists, pooled_endpoint_mode_contrasts | Reversed new \(a_2=+0.005931\), desirednegative | Conditional inversion not established |
| Comparable/joint readers | Saved DEV milestones and joint endpoint |6 NOT_REACHED;3 FEASIBILITY_UNKNOWN | Difficulty/capacity alternatives unresolved |
| Immediate mapping effect | Full seed `one_step/` readouts and qualification, results equal_norm_one_step | Three same-state same-norm effects below | Qualified local comparison; no trajectory mediation |
| Numeric identities |102 source readout files; independent recomputation in analysis |460,920 record occurrences; max1.0129319e−6nat | PASS numeric; repeated records are not independent samples |
| Saved-state identity | Checkpoint manifests and checkpoint_checks |120 states; common parent/old starts exact | Engineering/asset availability, not scientific approval |

The complete raw-readout hashes and analysis-script revision are in [analysis manifest](/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/runs/mapping_20261011T095038Z/analysis/analysis_manifest.json). Analyzer SHA256: `0148b327193c4f96aee7e732db5c7d0f02d1d1f43d913969df365236b3c84213`. Source transformations retain every registered seed/panel; no imputation or outcome exclusions.

## 7. Main Results

### Old acquisition and equal-budget endpoints

DEV old endpoint accuracies:

| Seed | 甲 order | 甲 combination | 乙 order | 乙 combination |
|---|---:|---:|---:|---:|
|29|52.5%|53.0%|33.5%|39.0%|
|43|51.0%|54.0%|34.0%|40.0%|
|71|50.0%|53.5%|33.0%|41.0%|

No cell reaches80%. This is not evidence that no partial information was learned. It is failure to establish the registered starting condition.

Three-seed old TEST means after equal-budget continuation:

| Panel | Old endpoint CE / accuracy / margin | Consistent endpoint CE / accuracy / margin | Reversed endpoint CE / accuracy / margin |
|---|---|---|---|
|order|1.106820 /49.4167% /.035938|1.032439 /49.1667% /.049357|1.034024 /49.5833% /.047828|
|combination|1.134068 /50.0833% /.055509|1.044758 /50.2500% /.079203|1.049448 /50.3333% /.070402|
|combined|1.120444 /49.7500% /.045724|1.038598 /49.7083% /.064280|1.041736 /49.9583% /.059115|

CE and margins are nat/answer; accuracy is full vocabulary. Both means improveCE/margin; this does not show net harm or mastered-rule retention.

| Panel | E seed29 | E seed43 | E seed71 | Mean / sample SD, nat |
|---|---:|---:|---:|---:|
|order|−.001569147|−.001480947|−.001536922|−.001529005 /.000044630|
|combination|−.008889108|−.008783555|−.008732896|−.008801853 /.000079697|
|combined|−.005229127|−.005132251|−.005134909|−.005165429 /.000055180|

All effects negative, all panel means below the0.01 operational magnitude. Registered descriptive verdict is insufficient because old mapping is unqualified. Directional replication is retained, not promoted to a stable learned-rule mechanism.

### Candidate access, new learning and conditional response

| Old combined change from old endpoint | Total CE | List3 access CE | List3 selection CE |
|---|---:|---:|---:|
|consistent|−.081845883|−.086274679|+.004428796|
|reversed|−.078708358|−.085027625|+.006319266|

List3 mass rises87.2696%→94.9785%/94.8624%. Access explains more than the entire CE benefit while conditional selection worsens slightly. Endpoint margin improving does not contradict this: middle-word competition and nonlinear averaging differ from endpoint mean log odds. This exact decomposition describes outputs, not causal partitioning of model parameters.

| New TEST panel | Consistent CE / accuracy, start→end | Reversed CE / accuracy, start→end |
|---|---|---|
|order|1.176080→1.069659 /46.50%→47.75%|1.169551→1.063201 /47.0833%→47.3333%|
|combination|1.208532→1.087370 /47.00%→46.6667%|1.225542→1.113271 /45.4167%→49.00%|
|combined|1.192306→1.078515 /46.75%→47.2083%|1.197546→1.088236 /46.25%→48.1667%|

All six new branches satisfy the operational useful-CE-learning rule, but none reaches the DEV comparable-level80% rule. Reversed TEST command response \(a_2\) is−.008390 on order,+.020251 on combination,+.005931 combined. The desired negative response is not consistently achieved. Thus CE gain is not proof of the intended conditional rule acquisition. Old \(a_1\) rises in both branches; mode-response difference changes, but these output coordinates cannot identify internal shared/unique processing.

Joint reversed TEST old/new combined accuracies50.2083%/47.50%, CE1.045236/1.103891. All three feasibility statuses are Unknown. Joint has extra old labels and only2,400 new targets; it is not a primary matched-new-exposure winner.

### Equal-norm immediate effects and actual update scale

| Seed | Consistent old ΔCE / Δmargin | Reversed old ΔCE / Δmargin | Reversed−consistent old Δmargin |
|---|---|---|---:|
|29|−.000507320 /+.000075006|−.000511443 /+.000058444|−.000016563|
|43|−.000949320 /+.000085437|−.000937606 /+.000070469|−.000014968|
|71|−.001088315 /+.000039830|−.001150055 /+.000026991|−.000012839|

Each probe has matched source input/order/target marginal and identical starting weights. Actual norm mismatch≤1.86265e−7relative. Both probeCE effects are helpful; the relative margins are small and do not provide complete trajectory mediation. Primary cumulative norm sums are consistency2.397132/2.393285/2.397529 and reversal2.397099/2.393728/2.397261. These are path lengths, not net displacement; primary SGD was not forced to have identical per-step scale. Full source metrics preserve that remaining rival.

### Post-hoc explanatory sample, not confirmation

Seed71, old mode-one 甲, list `马 花 猫`; correct answer is 马. This sample was selected after results to illustrate a prediction flip, not as an independent mechanism test.

| State | p(马) | p(猫) | Correct CE | Margin 马−猫 | Argmax |
|---|---:|---:|---:|---:|---|
|old endpoint|46.0013%|42.3474%|.776499|+.082764|马,correct|
|consistent|48.0829%|46.8537%|.732243|+.025898|马,correct|
|reversed|47.2847%|47.4714%|.748983|−.003941|猫,wrong|

Reversal increases correct-word probability and improves CE while the competing answer overtakes it. This explains why CE improvement alone cannot certify correct rule selection. One selected example cannot establish the frequency, specificity or internal cause of such effects. Source: `descriptive_sample_table.csv` and results descriptive_samples.

## 8. Supplementary Same-state Loss Derivation

This post-run exact derivation explains why reversed labels need not reverse the entire source gradient. It does not amend the frozen primary analysis. At the same matrix state \(W\), evaluate the same balanced mode-two input pairs under consistent and reversed labels. Let their mean full-vocabulary answer losses be \(L_s\) and \(L_r\), in nat. Define \(s_c=\log p(L_3\mid c,L)-\log p(L_1\mid c,L)\) and \(a_2=\mathbb E_L[(s_{乙}-s_{甲})/2]\), with mode two fixed. Pairing the two commands gives exactly:

\[
L_r-L_s=a_2,\qquad G=\frac{L_s+L_r}{2},\qquad
L_s=G-\frac{a_2}{2},\quad L_r=G+\frac{a_2}{2}.
\]

The corresponding raw gradients are \(g_s=\nabla_WG-\tfrac12\nabla_Wa_2\) and \(g_r=\nabla_WG+\tfrac12\nabla_Wa_2\). The label intervention changes one term's sign; a common term remains. For \(P_2(x)=p(L_1\mid x)+p(L_3\mid x)\),

\[
G=\mathbb E_x\left[-\log P_2(x)+\log\left(2\cosh\frac{s_x}{2}\right)\right].
\]

Here the expectation averages both commands and the paired lists. \(G\) contains endpoint access and endpoint balance; it is not pure candidate adaptation or an identified internal shared module. A small \(a_2\) does not imply a small gradient. If clipping or norm matching yields actual increments \(d_s=-\eta_sg_s\) and \(d_r=-\eta_rg_r\), then

\[
d_r-d_s=(\eta_s-\eta_r)\nabla_WG-\frac{\eta_s+\eta_r}{2}\nabla_Wa_2.
\]

Equal update norms do not imply equal effective scales \(\eta_s,\eta_r\). We did not measure component gradient sizes, angles or finite component interventions, so no parameter mechanism is inferred.

The [same-state identity check](/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/runs/mapping_20261011T095038Z/analysis/paired_loss_identity.json) passed 72 cells with maximum absolute discrepancy \(5.58794\times10^{-9}\) nat. At the common old endpoint, new-input \(L_s=1.192306\), \(L_r=1.197546\) and \(a_2=0.005240\). Never substitute losses from different trained states. This is an implementation check of algebra, not a new empirical mechanism discovery.

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | Outcome | What remains |
|---|---|---|---|
|Data preflight|manifest/qualification|PASS|One-template synthetic generalization scope|
|Smoke|`pt-jw3bhrzi`,gate,21-file verification|PASS|No scientific hypothesis result|
|External resume|four workers|PASS exact|Tested next-step recovery, not scientific evidence|
|Full|`pt-qs6ndgat`,qualification,freeze|SUCCEEDED/PASS|Old rule acquisition prerequisite fails|
|Asset/analysis gate|schema correction and strict reanalysis receipt|Corrected, deviation retained|Initial ordering error is not erased|
|Independent recomputation|102files/460,920record occurrences|maxerror1.0129319e−6,PASS|Identity checks do not prove mechanism|

No physical premise of universal interference was validated or falsified. The mathematical CE identity passed; it is not an empirical discovery. Implementation/training checks passed; registry schema/order failure was repaired. The operational premise of a sufficiently acquired old mapping failed. CE as a stand-alone rule-skill proxy is inadequate here. Difficulty, initial skill, frozen-matrix learning limits and optimization alternatives remain live.

## 10. Full Experiment Record

### 2026-10-11: merged conditional-mapping round

1. Question/H: whether new mapping reversal changes old prediction effects relative to consistency under equal exposure.
2. Setup/controls: official Base, last o_proj only; same old endpoint and matched new prefixes/order/answer marginals/budget; three seeds; reserved4H100 and registered image.
3. Training data: generated visible modes/neutral commands;2,400records/world. Old and primary new two passes; joint one underlying-list pass with both-mode labels.
4. Confirmation: frozen DEV/TEST order and combination panels. DEV selects only registered comparable point; TEST mechanically saved, no tuning; all bounded training completed before interpretation.
5. Result: Smoke/external replay/Full complete; primaryE−.005165nat; old qualification failed; all six comparable points absent, jointUnknown; candidate-access decomposition measured. Numeric, saved-state and strict-output checks qualified. Registry-order deviation/reanalysis retained.
6. Insight/boundary/next decision: a probability change cannot establish retained-rule transfer without an acquired old rule. No net meanCE/margin harm or separation benefit established. Scientific closureUnknown. AI suggests old-only acquisition qualification before further relation/separation work; no new run authorized by this suggestion.

## 11. Interpretation

The mapping intervention caused bounded prediction differences in the registered carrier, but their learned-rule meaning is insufficient. General candidate adaptation is directly compatible with the output decomposition; it is not excluded. Relative margin difference is smaller than the registered practical convention and cannot override acquisition failure. Failed comparable/joint readers leave difficulty and realizability unresolved. The earlier component experiment and present mapping experiment complement one another; neither establishes an expert separation advantage.

## 12. Claim Boundary

Can claim: all registered bounded training/readouts completed and qualified; actual states registered; neutral mapping acquisition failed its criterion; reversal gave small lower old-margin improvement; old combined CE benefit is dominated by list-access change.
Cannot claim: a well-learned old rule was forgotten; successful reversed-rule transfer; unavoidable task conflict; unique internal causal modules; insufficient full-model capacity; expert/parameter separation superiority; natural-language generalization. Scientific mechanism verdict and question closure remain Unknown.

## 13. Next Decision

Exactly one future researcher decision: whether sufficient conditional-mapping evidence warrants a shared/separate parameter comparison. Current evidence cannot settle it. AI suggests a bounded old-only acquisition diagnosis first, rather than costly separation or SAE expansion. This is not a new activated task. The current execution task is complete; resume by reading this Summary/registered measurements and obtaining any next scientific scope from the researcher.

## 14. Artifact Manifest

| Artifact | Producer / identity / sources | Complete | Eligibility / notes |
|---|---|---|---|
|Frozen contracts/config/code/data|`freeze.json`;09:53:00Z;config SHA `9d47a5c31821c1528d2de598e7a5735325a95c946d8834be4345762b3465d226`|Yes|21files unchanged before/after|
|Data manifest|`a17_conditional_mapping_v1`;generated seed20261011|Yes|Registered input; not learning evidence|
|Job/worker receipts|Smoke09:53:28Z/Full09:56:33Z;bothSUCCEEDED;worker qualification|Yes|Platform distinct from scientific result|
|Checkpoint payload/manifests|72Full+48Smoke states;parent required;weights/RNG/cursor/counters|Yes|28adapter families;no fullBase export|
|Native readout manifests|Smoke/Full perrecord readouts|Yes|Two representation families; bounded semantics|
|Strict output access|[30-output snapshot](/data/250010109/Research_System/assets/checks/2026-10-11_a17_mapping_output_access.json)|PASS30|Availability/probes, not scientific approval|
|Registered analysis|`results.json`,paired/descriptiveCSV,analysismanifest|Yes|Corrected strict-gate deterministic reanalysis|
|Schema/order correction|`registration/schema_correction.json`,reanalysis receipt,provisionaloutputs|Yes|Deviation retained;no payload/scientific changes|

Registration [receipt](/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/runs/mapping_20261011T095038Z/registration/receipt.json) names actual28 adapter/two readout families and links the [payload manifest](/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/runs/mapping_20261011T095038Z/payload_manifest.json). Derived analysis is separately registered as `analysis_a17_04_mapping_20261011t095038z` and passes its [selected access check](/data/250010109/Research_System/assets/checks/2026-10-11_a17_mapping_analysis_access.json); the 30-output access result above retains its own scope. Data SHA256: train `3b57c72970cba2a5478caab85369bfb53804094960422ba7e2fca9ddcf14ca03`;DEV `e382ae70dea12c65aeb9178e1c32ec1eb205039181be2dbc38b38ec9379a0471`;TEST `963b4f75d6c835fffbfb79860dc1e85d687b734086103dfe53fef3b551a5f1da`.

## 15. Links

Execution root: `/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer`; run `/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/runs/mapping_20261011T095038Z`.
Runner:`source/run.py`; analyzer:`launch/analyze.py`; config:run `config.json`; data:root `data/conditional_mapping_v1/manifest.json`; strictinputs:root `provenance/input_access.json`;sourcefreeze:run `freeze.json`.
Decisive result:[results](/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/runs/mapping_20261011T095038Z/analysis/results.json), [paired table](/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/runs/mapping_20261011T095038Z/analysis/paired_table.csv), [descriptive sample table](/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/runs/mapping_20261011T095038Z/analysis/descriptive_sample_table.csv), [analysis lineage](/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/runs/mapping_20261011T095038Z/analysis/analysis_manifest.json).
Jobs:Smoke`pt-jw3bhrzi`,Full`pt-qs6ndgat`;status snapshots,submission certificates and mountedlogs remain run-side. Reproduction command is frozen in run `full_launch_contract.json`; exactparent/data/runtime and explicit scope are required.
