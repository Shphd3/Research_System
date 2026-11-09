# Detailed: A17_04_E01 R02 single-layer AdamW mapping transfer

Primary Anchor: [conditional mapping transfer](../../../../../../problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/17_04_conditional_mapping_transfer_anchor.md). Protocol: [round Protocol](protocol.md), revision `a17_04_e01_r02_single_layer_adamw_v1`. Summary: [result summary](summary.md).

Execution state: `ENGINEERING_COMPLETE; REGISTERED_ACCESS_PASS; BOUNDED_EXPOSED_DEV`. Researcher mechanism judgment and next scientific decision: `Unknown`.

## 0. Quick recap

Purpose: after old-rule acquisition, change only the new mode's command-to-position relation and test when shared updates preserve or damage the old mapping. The separate local probe measures actual optimizer direction, norm and moment effects.

**Consistency preserves the old rule. Learning the reversed new rule reduces old accuracy to 0% in all three continuation orders. Joint supervision nevertheless lets the same single-layer four-weight scope fit both mappings.** With equal DEV-panel and continuation-order weighting, consistent old CE is 0.00004081, accuracy 100%, and margin +23.14596; reversed old CE is 15.81921, accuracy 0%, and margin −15.79310; reversed new CE is 0.03135015, accuracy 99.25%, and margin +16.18983. Joint old/new accuracy is 99.833%/99.667%, with all eight command-by-panel cells passing.

Primary E values are −38.38544/−41.28473/−37.14703 nat, with mean −38.93906 and sample SD 2.12368. This relative reversal cost accompanies absolute old CE/accuracy/margin harm. Native decomposition locates most worsening in within-candidate correct selection rather than disappearance of candidate probability mass.

Engineering: Smoke `pt-022fae06` and Full `pt-x0czuelx` SUCCEEDED. Nine 1,200-step branches consumed 216,000 fitting targets and produced 72 actual Full states, 72 native readouts and 115,200 evaluation-record occurrences. Seven telemetry tags, exact replay, 42 frozen files, actual output registration and current strict access checks pass. All 34 Full probe conditions and the independent audit pass.

Eligibility/boundary: `BOUNDED_EXPOSED_DEV`; three orders share one old endpoint. The descriptive result supports relation-dependent retention cost in this setting; researcher mechanism judgment/formal verdict remains `Unknown`. Joint has extra old labels and half the new-task exposure; it does not measure split-expert utility. The probe counters a simple “enlarge SGD” account; it does not identify the sole mechanism behind long-run AdamW success.

## 1. Terminology and computation

| Object | Plain meaning and construction | Use and boundary |
|---|---|---|
| Old mode1 | 甲 selects FIRST,乙 LAST | Acquired rule; old evaluation labels remain fixed |
| Consistent mode2 | Same command-to-position mapping | New mode with reusable mapping |
| Reversed mode2 | 甲 selects LAST,乙 FIRST | Identical new prefixes to consistency, swapped targets; visible modes allow a joint solution |
| joint_reversed | Ten old plus ten reversed-new targets/update, same five lists and both commands/modes | Feasibility control; extra old labels and half new exposure prohibit equal-supervision utility claims |
| Unseen order | New permutation of a familiar unordered triple | Separate from unseen combinations |
| Unseen combination | Previously absent triple of familiar words | Not unseen vocabulary; each panel400targets, equal combined weighting |
| CE | Negative log probability of correct answer, nat/answer | Lower CE need not improve answer ranking |
| Rule margin | Correct endpoint log probability minus opposite endpoint | Measures endpoint selection; full-vocabulary accuracy checks other competitors |
| Actual displacement | Four tensor differences after optimizer operation | AdamW displacement is not negative raw gradient |
| Continuation seed | Seeds29/43/71 change new list order | Conditional variation around one common old state |

## 2. Anchor link and decision point

Original E01 did not acquire the old mapping reliably. E03 supplied an acquired last-layer Q/K/V/O AdamW endpoint. R02 retains the neutral commands/list task and repeats the relation intervention from that actual endpoint. It can measure retention costs of shared updates under two relations; it cannot directly choose an expert split.

Original E01 Protocol/results retain their historical identities. This record owns only R02. Scientific closure and later architecture decisions remain researcher-owned.

## 3. Freeze, conformance and deviations

Frozen at 2026-10-11 16:10:08.549730 UTC. The 42-file freeze binds bilingual owner snapshots, sources/configs, data, parent and acquired-state identities. Freeze SHA256 `accb6e360d935278dfa2bbdd3a27e776896eea46482a4730cb7580db97136950`; English frozen Protocol SHA256 `dc1da949870f36bbb50f41d2b04e28833c7a748219b4b046d85a80972e515a21`; transfer config SHA256 `5bb5754ce2f8622ec31265a605f6563c1021950c42b70f0d884a414faeeddc1d`.

| Registered item | Expected | Actual and eligibility |
|---|---|---|
| Authorization/owners | Current one-layer transfer/probe; retain original E01 | Bilingual snapshots/revision match; no unauthorized conditions |
| Data/supervision | Original TRAIN/DEV,no TEST; matched new prefixes/order/marginals | Data guard/consumed rows PASS; exposed DEV |
| Old/four-weight scope | Common AdamW1200,6291456; other tensors freeze | All nine step0weights exactly match; old four cells100%; frozen bytes/versions PASS |
| Objective/optimizer | Fresh AdamW,clip1,micro5acc4/20targets | No old moments carried; actual counts/all seven tags PASS |
| Full budget |3orders×3branches×1200updates | Nine complete paths,10800updates/216000targets; no extension |
| Smoke/replay |3branches×3updates,external1→2 each |180targets plus60replay; weights/optimizer/RNG/metric/counters exact |
| Saves/outputs |9Smoke/72Full states |81actual states;5Smoke/11Full assets registered/current strict PASS |
| Probe |5Smoke/34Full independent conditions | Complete;maxnormerror2.13057e-5;all no-ops zero |
| Analysis | E/absolute changes/acquisition/skill/joint | Original analyzer loads72states/checks115200records PASS; independent logit audit PASS |
| Immutability |42frozen files | freeze_end_verification PASS42; frozen source/data/contract snapshots unchanged |

Corrections/deviations: before freeze, panel arithmetic was clarified as 40 records/world and 80 old-plus-new records; code always selected 10 lists/panel. A bare CPU invocation hit the preexisting protobuf environment conflict; sourcing the existing runtime environment passed without dependency changes. There was no post-freeze contract amendment, GPU retry, condition exclusion, missing save or adaptive extension. Post-hoc output-error categories and illustrative selection are explicitly descriptive, not replacement primary or confirmation evidence.

Numeric boundary: native FP32 CE is retained, while candidate access uses an FP64 lognormalizer. Subtraction can produce approximately 1e-7 negative conditional-choice CE near zero. This is a precision mismatch, not negative loss or a functional gain. The independent maximum native-CE-versus-FP64-log-probability error is 3.87e-6, below the frozen 2e-5 tolerance. Raw values are preserved without clipping.

## 4. Actual setup and provenance

Carrier: 28-layer Qwen3-0.6B Base; only layer 27 Q/K/V/O weights train. Shapes are Q 2048×1024, K/V 1024×1024 and O 1024×2048, totaling 6,291,456 parameters. Q/K norms, all other attention parameters, earlier blocks, MLP, embeddings, final norm and lm_head freeze. FP32/native SDPA/eval/no dropout/deterministic/no TF32; no fixed activation cache over trainable dependencies.

Inputs: model_qwen3_0p6b_base_official_a5, tokenizer_qwen3_0p6b_base_official_a5, data_a17_conditional_mapping_v1, adapter_a17_04_single_attention_20261011t145214z_full_attn1_adam_main. Probe additionally uses registered SGD main240 and E02 neutral TRAIN/DEV. Current access and exact source membership belong in the root artifact manifest/execution provenance.

Common old input: E03 AdamW Main `update_01200/state.pt`, SHA256 `48595673c24579164e271cfeb1b86be6a234e2dfc06218b74d8ca07e16411b75`. Load four weights; intentionally reset old Adam moments/RNG/counters. Stage-local counters exclude the prior 24,000 old-task answers. Exact recovery inside a branch restores its complete branch state.

Each original world has 2,400 TRAIN targets/1,200 lists and 800 DEV targets, 400 per panel. Every list has two commands. Primary consistent/reversed consume identical new prefixes/order and per-batch answer marginals. Lists recur across modes deliberately; full inputs differ by visible mode. DEV is previously exposed diagnosis, not fresh confirmation. No TEST is loaded.

Objective: one answer token after the prefix; 20 targets/update through microbatch 5 × accumulation 4, with each summed microbatch loss divided by 20. No prefix/padding loss, regularizer or auxiliary. AdamW uses learning rate 1e-4, betas (0.9, 0.999), epsilon 1e-8, decay 0, foreach/fused=False and a constant rate; one global norm clip of 1 applies across the four tensors.

Each primary branch has 1,200 updates/24,000 new answers. Six primary paths total 144,000 new answers. Three joint paths add 72,000 total answers: 36,000 old and 36,000 new. Full totals 216,000 fitting targets. Smoke consumes 180 targets; external replay separately consumes 60. Prior acquisition, fixed-state gradient/evaluation and probe work are not added to new-training exposure.

Save/evaluate at updates 0, 1, 16, 50, 120, 240, 600 and 1,200. States contain four weights, complete Adam/RNG/schedule, target/update/cursor/order and parent/config/data/frozen identities. Independent GPU lanes are DP1; four GPUs do not multiply targets/update.

Resources: one reserved node with four H100 80 GB GPUs, image `shphd-lite-0911`, and 7,200 seconds/job. Smoke GPU0/1/2 each run one branch, GPU3 the probe. Full GPU 0/1/2 each sequentially run one continuation seed's three branches; GPU 3 performs 34 probe conditions. Actual device topology and receipts qualify resource facts.

Reuse: adapt E03 native four-matrix training/recovery/TB and E01 paired-world reader. Reject O-only restore, original TEST loader, tiny acquisition, SAE/LoRA/experts. Source/IMPLEMENTATION.md and configs/cpu_qualification.json retain exact decisions.

## 5. Metrics and registered decision rules

For old input x, correct endpoint y and opposite endpoint o, define \(m_A=\log p(y\mid x)-\log p(o\mid x)\), a logit difference in nat. M averages fixed old DEV at equal command/panel weight. Per continuation order,

\[
E_s=\Delta M_{A,s,\mathrm{reversed}}-\Delta M_{A,s,\mathrm{consistent}}.
\]

Both changes subtract the same acquired start. Negative E means a relative reversal cost, not necessarily net harm. Report three effects and their mean/sample SD/min/max for each panel and the equally weighted combination. All E < 0 and mean ≤ −0.01 is a descriptive convention, not a significance test.

Old start and final new mapping each require all four command×panel cells ≥ 80%. Reversal must actually increase new margin for learned-signal interpretation. Separately report old CE/accuracy/margin changes from start; material conventions are 0.005 nat CE, 1 percentage point accuracy and 0.01 nat margin. Joint feasibility requires all eight old/new cells ≥ 80%.

Comparable-level reader chooses the first saved point meeting all four new cells≥80%, including step 0 when consistency is initially qualified. This is a common minimum gate, not exact equal attained skill or learning paths.

For candidate setS, CE equals access loss−logP(S) plus choice loss−log[p(y)/P(S)]. Margins/full-vocabulary accuracy prevent candidate-mass gains from being labeled rule learning. Paired command/mode coordinates are exact output descriptions, not parameter mechanisms.

The probe uses Base, SGD240 and AdamW240, two fixed 20-target old TRAIN batches and 80 fixed old DEV targets. Conditions: no-op, nativeSGD, nativeAdamFresh, SGD scaled to AdamFresh norm, AdamFresh scaled to SGD norm; AdamW240 adds nativeAdamCarry and Carry scaled to SGD norm. Each condition restores original weights/moments. Full has 34 conditions; Smoke has five. Actual applied four-tensor displacement δ defines

\[
\Delta L_R=L_R(\theta+\delta)-L_R(\theta),\qquad R_{\mathrm{finite}}=\Delta L_R-\langle\nabla L_R(\theta),\delta\rangle.
\]

The remainder includes nonlinearity and residual precision mismatch; it does not identify the cause alone. Equal displacement norms do not match 1,200-step histories. Norm matching error must be ≤ 1%; native CE identity error must be < 2e-5 nat.

## 6. Evidence lineage

| Claim | Registered criterion | Raw evidence/computation | Observation/eligibility |
|---|---|---|---|
| Old acquired | Four start cells≥80% | step0weights/nativeeval | Four cells100%,PASS |
| Relation-dependent retention | Acquired new/allEnegative/mean≤−.01 | Paired primary endpoints/primary_contrast | Mean−38.93906nat,allnegative; descriptive relative cost |
| Absolute old harm | CE/accuracy/margin versus common start | Endpoints/native records | Reversal oldCE+15.81852,accuracy−100pp,margin−33.31776; actual harm |
| Candidate rival | Access/choice plus margin | Per-record probabilities | Oldaccess+.00877,choice+15.80974nat; predominantly selection worsening |
| Learned new rule | Four new cells≥80% and new margin gain | Qualification/native endpoints | All reversed paths qualify;newmarginmean+32.22485 |
| Joint feasibility | Eight old/newcells qualify | Joint endpoints/fourway | AllPASS;fourway100%/99.5%/98.25%;different supervision/exposure |
| Local optimizer effects | Same state/source,actualδ,norm/cosine/ΔCE | Probe payload/independentaudit |34conditionsPASS;state-dependent direction/norm/history effects |
| Engineering/assets | Saves/replay/freeze/telemetry/strict |72stateaudit/registrationreceipts | AllPASS;scientificscope remains oneold/exposedDEV |

Complete evidence: [Main analysis](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/analysis/results.json),[Independent mapping audit](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/independent_mapping_audit.json),[Probe audit](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/optimizer_probe/full/independent_audit.json). Continuation orders describe conditional path variation, not uncertainty across independently trained old models.

## 7. Main transfer results

Each row is an actual 1,200-update endpoint. CE uses nat/answer, margin uses nat, and accuracy uses the full vocabulary. Unseen panels are reported separately and in an equally weighted combination: 400 old and 400 new targets per panel/order, 800 of each in the combination. The old baseline is identical across branches. Consistent new baseline accuracy is 99.875%; reversed baseline accuracy is 0%. Consistency largely reinforces an existing mapping, so new-rule difficulty is not symmetric from scratch.

### order_new

Common old start: CE 0.00127738, accuracy 100.00%, margin +17.772339.

| Order | Branch | Old CE | Old accuracy | Old margin | New CE | New accuracy | New margin |
|---|---|---:|---:|---:|---:|---:|---:|
|29|consistent|0.00006588|100.00%|+23.49333|0.00006418|100.00%|+23.27145|
|29|reversed|15.68115433|0.00%|-15.68097|0.00013121|100.00%|+16.19936|
|29|joint_reversed|0.00066337|100.00%|+18.01054|0.00210712|100.00%|+16.21053|
|43|consistent|0.00007171|100.00%|+24.01831|0.00008870|100.00%|+23.69150|
|43|reversed|18.04170294|0.00%|-18.04156|0.00016271|100.00%|+18.32382|
|43|joint_reversed|0.00986870|99.75%|+19.17451|0.00546464|99.75%|+16.77371|
|71|consistent|0.00003527|100.00%|+22.58500|0.00005406|100.00%|+22.27763|
|71|reversed|14.98203873|0.00%|-14.88023|0.12231636|97.00%|+15.22662|
|71|joint_reversed|0.00451493|99.75%|+17.52288|0.01617212|99.25%|+15.24384|

### combination_new

Common old start: CE 0.00010468, accuracy 100.00%, margin +17.276967.

| Order | Branch | Old CE | Old accuracy | Old margin | New CE | New accuracy | New margin |
|---|---|---:|---:|---:|---:|---:|---:|
|29|consistent|0.00003465|100.00%|+23.12525|0.00001572|100.00%|+22.86536|
|29|reversed|14.47183299|0.00%|-14.47133|0.00043789|100.00%|+15.01100|
|29|joint_reversed|0.00086448|100.00%|+17.81123|0.00105215|100.00%|+15.16046|
|43|consistent|0.00000892|100.00%|+23.58619|0.00000606|100.00%|+23.25453|
|43|reversed|16.92403853|0.00%|-16.92340|0.00029296|100.00%|+17.24498|
|43|joint_reversed|0.01004807|99.75%|+19.07236|0.00617058|99.75%|+15.83166|
|71|consistent|0.00002839|100.00%|+22.06770|0.00001717|100.00%|+21.74756|
|71|reversed|14.81447115|0.00%|-14.76112|0.06475976|98.50%|+15.13319|
|71|joint_reversed|0.00308751|99.75%|+17.04616|0.02368015|99.25%|+14.68096|

### combined

Common old start: CE 0.00069103, accuracy 100.00%, margin +17.524653.

| Order | Branch | Old CE | Old accuracy | Old margin | New CE | New accuracy | New margin |
|---|---|---:|---:|---:|---:|---:|---:|
|29|consistent|0.00005027|100.00%|+23.30929|0.00003995|100.00%|+23.06840|
|29|reversed|15.07649366|0.00%|-15.07615|0.00028455|100.00%|+15.60518|
|29|joint_reversed|0.00076393|100.00%|+17.91089|0.00157963|100.00%|+15.68549|
|43|consistent|0.00004032|100.00%|+23.80225|0.00004738|100.00%|+23.47302|
|43|reversed|17.48287074|0.00%|-17.48248|0.00022783|100.00%|+17.78440|
|43|joint_reversed|0.00995838|99.75%|+19.12343|0.00581761|99.75%|+16.30268|
|71|consistent|0.00003183|100.00%|+22.32635|0.00003561|100.00%|+22.01260|
|71|reversed|14.89825494|0.00%|-14.82068|0.09353806|97.75%|+15.17991|
|71|joint_reversed|0.00380122|99.75%|+17.28452|0.01992613|99.25%|+14.96240|

### Primary contrast and absolute harm

| Panel | E29 | E43 | E71 | Mean | Sample SD |
|---|---:|---:|---:|---:|---:|
|order_new|-39.174297|-42.059870|-37.465231|-39.566466|2.322288|
|combination_new|-37.596576|-40.509583|-36.828826|-38.311662|1.941778|
|combined|-38.385436|-41.284726|-37.147029|-38.939064|2.123679|

Every E is negative in all panels, well beyond the −0.01 descriptive convention. Reversal increases old mean CE by 15.81852 nat, reduces accuracy by 100 percentage points, and reduces margin by 33.31776 nat; new margin rises by 32.22485 nat. This is actual old-rule loss rather than only reduced repair. It does not establish a result for all reversal tasks.

### First new-rule qualification points

| Order/branch | Saved step | Total/new answers | Old CE/accuracy/margin | New CE/accuracy/margin |
|---|---:|---:|---|---|
|29/consistent|0|0/0|0.000691/100.00%/+17.5247|0.002756/99.88%/+16.0350|
|29/reversed|120|2400/2400|5.360900/2.88%/-5.2348|0.125393/96.00%/+5.3643|
|29/joint_reversed|240|4800/2400|0.050897/98.50%/+9.2351|0.072754/98.00%/+7.7939|
|43/consistent|0|0/0|0.000691/100.00%/+17.5247|0.002756/99.88%/+16.0350|
|43/reversed|120|2400/2400|5.285163/2.50%/-5.1767|0.109601/96.62%/+5.2495|
|43/joint_reversed|240|4800/2400|0.042722/98.50%/+9.3520|0.092443/96.75%/+6.9561|
|71/consistent|0|0/0|0.000691/100.00%/+17.5247|0.002756/99.88%/+16.0350|
|71/reversed|240|4800/4800|7.885022/2.75%/-7.7300|0.153205/95.12%/+8.0192|
|71/joint_reversed|600|12000/6000|0.005058/99.88%/+14.2557|0.219132/93.12%/+10.3064|

Consistency qualifies at step 0; reversal qualifies at 120 for orders 29/43 and 240 for order 71. Old damage remains visible at these gates, but difficulty, initial skill and paths are not fully matched. Joint gate readers are secondary and do not provide the primary equal-new-exposure comparison. At joint endpoints, all eight cells are ≥ 98.5%, with four-way joint correctness of 100%/99.5%/98.25%.

### Output response shared across modes versus mode dependence

| Order/branch | a1 old | a2 new | C mean response | K mode difference | Four-way correct |
|---|---:|---:|---:|---:|---:|
|29/consistent|+23.30929|+23.06840|+23.18885|-0.12044|100.00%|
|29/reversed|-15.07615|-15.60518|-15.34067|-0.26452|0.00%|
|29/joint_reversed|+17.91089|-15.68549|+1.11270|-16.79819|100.00%|
|43/consistent|+23.80225|+23.47302|+23.63763|-0.16462|100.00%|
|43/reversed|-17.48248|-17.78440|-17.63344|-0.15096|0.00%|
|43/joint_reversed|+19.12343|-16.30268|+1.41037|-17.71306|99.50%|
|71/consistent|+22.32635|+22.01260|+22.16947|-0.15688|100.00%|
|71/reversed|-14.82068|-15.17991|-15.00029|-0.17962|0.00%|
|71/joint_reversed|+17.28452|-14.96240|+1.16106|-16.12346|98.25%|

Balanced commands imply old M = a1, consistent new M = a2 and reversed new M = −a2; C = (a1+a2)/2 and K = (a2−a1)/2. Reversal makes both a1 and a2 negative: an across-mode command-response flip. Joint has a1 > 0 and a2 < 0: a mode-dependent mapping response. These exact output identities do not identify parameter modules or causal directions. The independent raw-logit audit checks 72 files, 115,200 records and 466,011 scalars, with maximum algebra error 3.77e-15: PASS.

### Concrete sample and post-hoc error categories

For seed 29, list “红 黄 猫” and command 甲, 红 is FIRST and 猫 is LAST. Expected answers depend on the visible mode and branch mapping; neither word is intrinsically correct or wrong. The sample was selected post-hoc for correct-start/wrong-after-reversal/correct-after-joint behavior. It illustrates that behavior, not its frequency.

| Stage | World/mode | Target | Prediction | pFIRST | pLAST | Margin |
|---|---|---|---|---:|---:|---:|
|old_start|old/1|红|红|0.99999876|8.9285774e-08|+16.23142|
|old_start|consistent/2|红|红|0.99998824|4.0021251e-07|+14.73126|
|same_end|old/1|红|红|0.99999901|2.8717369e-08|+17.36576|
|same_end|consistent/2|红|红|0.99999844|3.1520116e-08|+17.27264|
|reverse_end|old/1|红|猫|2.1545547e-06|0.9999899|-13.04792|
|reverse_end|reversed/2|猫|猫|6.201953e-07|0.99999103|+14.29322|
|joint_end|old/1|红|红|0.99999987|6.773877e-09|+18.81019|
|joint_end|reversed/2|猫|猫|1.3060646e-06|0.99999276|+13.54848|

Post-hoc categories show that every old reversal error selects the opposite endpoint for orders 29/43. For order 71, combined fractions are 97.5% opposite endpoint, 1.5% middle item, 1% outside the list and 0% correct. Old accuracy of 0% alone therefore does not imply that every sample only flips endpoints. These categories are neither the registered primary estimand nor fresh confirmation.

[Sample](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/analysis/illustrative_sample.json) · [Post-hoc categories](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/analysis_posthoc_rule_choice.json) · [Full trajectories](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/analysis/trajectories.csv) · [Mode coordinates](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/analysis/mode_command_trajectories.csv).

### Training trajectories

![Old/new mapping trajectories](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/analysis/figures/transfer_trajectory.png)

The top row shows the old task and the bottom row the new task. Columns show answer CE, full-vocabulary accuracy and the correct-versus-opposite margin. The x-axis counts continuation updates with 20 total answers each; joint has 10 new answers/update. Colors distinguish consistency, reversal and joint. Curves average the three orders; shading is their minimum–maximum range, not a confidence interval. Reversal learns the new task while losing the old one; joint recovers both after early costs. The native trajectory CSV supplies the figure. The rendered PNG was inspected for title, legend and axis clipping. Trajectories describe measurements, not causal parameter-module attribution.

[Figure provenance](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/analysis/figures/provenance.json).

## 8. Stage evidence and failure decomposition

CPU qualification, Smoke, Full training, independent analysis, the probe, registration and current strict access checks all PASS. Smoke job is `pt-022fae06`. Full job `pt-x0czuelx` completed at 2026-10-11 16:30:49 UTC (2026-10-12 00:30:49 Shanghai). All 72 Full states were actually deserialized and checked for four weights, Adam moments, counters, shape, dtype and finiteness. All seven telemetry tags and consumed target/batch counters pass. All 42 frozen files remain unchanged. The 81 actual Smoke/Full states are registered through 12 adapter families and four analysis/probe families.

Weakened rivals are an unacquired old start, an unlearned reversed new task, candidate-mass disappearance as the sole cause, and inevitable inability of this four-weight scope to accommodate both mappings. Open questions are why new-only updates fail to retain mode discrimination, which update components cause cross-mode response changes, and whether split learning helps under matched supervision, parameters and compute. Joint changes supervision and new-task exposure; it cannot adjudicate those latter mechanism or utility questions.

## 9. Complete round record

1. Question: after old acquisition, does reversal alter retention cost? The probe asks only about local update effects.
2. Setup: one AdamW 1,200-update old endpoint, four last-layer weights, fresh Adam moments and three continuation orders with three branches each; primary controls remain fixed.
3. TRAIN: the same mode-2 prefixes and swapped labels; joint has 10 old plus 10 new answers/update.
4. Evaluation: exposed DEV panels separately/equally combined; no TEST/fresh confirmation.
5. Result: nine Full paths complete; consistency retains the old task, reversal yields 0% old accuracy, and joint yields near-100% old/new accuracy. All 34 probe conditions are complete; 81 actual states and 16 registered assets have strict PASS. Full tables appear above and below.
6. Insight/boundary/decision: there is a relation-dependent actual retention cost and a conditional-compatibility witness. Split-architecture utility and a parameter mechanism are not established. The bounded authorization is complete; the next scientific decision remains `Unknown`.

## 10. Interpretation and claim boundary

Observation: changed mapping labels produce an acquired new rule and actual old harm, while joint qualifies both. Derivation: E and the CE decomposition distinguish relation costs from candidate adaptation. AI interpretation: shared-update utility depends on retaining visible condition distinctions; different mappings alone do not imply inability to share. Researcher mechanism judgment remains `Unknown`; parameter-level necessity is not identified.

Can claim: under this task, common old endpoint, four-weight scope, fresh AdamW and budget, reversal causes a descriptively stable relative old-margin cost and actual old-prediction loss. The same model scope can learn both modes with joint supervision. Cannot claim: inevitable reversal conflict, split-expert utility, identified parameter modules, the cause of long-run AdamW success, independent old-model replications, natural-text transfer or fresh confirmation.

## 11. Next decision

Scientific next decision: `Unknown`, pending researcher assessment. Authorized training, analysis, saves and registration are complete. No extra architecture, SAE, data or training budget was used.

## 12. Artifact manifest and reproduction links

Execution root: /data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer. Run: runs/transfer_20261011T160256Z. Root owns [artifact manifest](artifact_manifest.json). Actual output IDs and current strict receipts follow actual saves in the Smoke/Full registration receipts; plans are not assets.

| Artifact | Purpose | Identity/completeness | Current eligibility |
|---|---|---|---|
| Bilingual owner snapshots | Contract/scope |42-filefreeze | Frozen |
| config.json/freeze.json | Exact settings/immutable inputs | SHAabove/42fileendcheck | PASS |
| Old update1200 | Common weights | Exact stateSHA above/registered family | Input access PASS |
| CPU qualification | Implementation | configs/cpu_qualification.json | PASS; not science |
| Smoke receipt | Engineering execution | pt-022fae06,submitted2026-10-11 16:10:25UTC | SUCCEEDED/engineeringPASS |
| Smoke outputs |9states/native readers/5probeconditions | smoke_registration_receipt.json,5assets | REGISTERED_ACCESS_PASS |
| Full states/readouts | Primary evidence | pt-x0czuelx;actual72states/72readouts | REGISTERED_ACCESS_PASS |
| Probe payload | Deltas/finite changes | Actual34conditions/results/manifests/independentaudit | REGISTERED_ACCESS_PASS |

[Protocol](protocol.md) · [Summary](summary.md) · [Run config](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/config.json) · [Freeze](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/freeze.json) · [Implementation](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/source/IMPLEMENTATION.md).

Worker reproduction: source runtime.sh then transfer.py --config CONFIG --run RUN --seed SEED --branch BRANCH --phase smoke|full|resume_verify in the authorized H100 environment. This is not a new submission. analyze.py reads durable records without model training.

## 14. Completed local optimizer probe

These are actual independent fixed-state interventions. Main transfer and probe work are complete, and actual output registration/current strict access pass. Each row restores its original state; the 34 rows do not form a training trajectory. Source batches match across optimizers, and recipient readouts use 80 fixed old DEV targets. Delta means after minus before. CE/access/choice use nat/answer; margin uses nat; accuracy uses the full vocabulary.

Independent numeric audit PASS: 34 conditions, six state/batch combinations, 54 original manifest entries, 40 readout files/3,200 record occurrences and 17,152 scalars. Maximum recomputation error is 3.55e-15; maximum relative norm-match error is 2.13057e-5, below 1%. All six no-ops have exact zero displacement and unchanged readouts. This audit did not independently regenerate model forward/backward outputs.

### base

Baseline CE 2.48594952; conditional-choice CE 1.05783763; accuracy 31.25%.

| Batch | Condition | Actual norm | Delta CE | Delta access CE | Delta choice CE | Delta margin | Accuracy after |
|---|---|---:|---:|---:|---:|---:|---:|
| 1 | no_op | 0.00000000 | +0.00000000 | +0.00000000 | +0.00000000 | +0.00000000 | 31.25% |
| 1 | sgd_native | 0.01000000 | -0.08928511 | -0.09512305 | +0.00583794 | -0.00009819 | 30.00% |
| 1 | adam_fresh_native | 0.24970120 | -0.34151231 | -0.36363134 | +0.02211903 | +0.00196093 | 38.75% |
| 1 | sgd_direction_adam_norm | 0.24970120 | -0.65049217 | -0.90394093 | +0.25344876 | +0.00634164 | 40.00% |
| 1 | adam_direction_sgd_norm | 0.01000004 | -0.01555123 | -0.01545294 | -0.00009830 | -0.00003591 | 31.25% |
| 2 | no_op | 0.00000000 | +0.00000000 | +0.00000000 | +0.00000000 | +0.00000000 | 31.25% |
| 2 | sgd_native | 0.01000000 | -0.08887200 | -0.09738725 | +0.00851526 | +0.00060871 | 30.00% |
| 2 | adam_fresh_native | 0.24976435 | -0.33157214 | -0.38150294 | +0.04993080 | +0.00366417 | 35.00% |
| 2 | sgd_direction_adam_norm | 0.24976435 | -0.61713265 | -0.90427491 | +0.28714226 | +0.01214031 | 31.25% |
| 2 | adam_direction_sgd_norm | 0.00999993 | -0.01536337 | -0.01652385 | +0.00116049 | -0.00000131 | 31.25% |

### sgd_240

Baseline CE 1.12111264; conditional-choice CE 1.06732633; accuracy 41.25%.

| Batch | Condition | Actual norm | Delta CE | Delta access CE | Delta choice CE | Delta margin | Accuracy after |
|---|---|---:|---:|---:|---:|---:|---:|
| 1 | no_op | 0.00000000 | +0.00000000 | +0.00000000 | +0.00000000 | +0.00000000 | 41.25% |
| 1 | sgd_native | 0.01000000 | -0.01346762 | +0.00170648 | -0.01517409 | +0.00176554 | 40.00% |
| 1 | adam_fresh_native | 0.24971328 | +0.02691839 | +0.01672923 | +0.01018915 | +0.01048062 | 41.25% |
| 1 | sgd_direction_adam_norm | 0.24971328 | +0.97544721 | +0.24170962 | +0.73373759 | +0.04586498 | 33.75% |
| 1 | adam_direction_sgd_norm | 0.01000008 | -0.00439561 | +0.00038841 | -0.00478402 | +0.00044768 | 41.25% |
| 2 | no_op | 0.00000000 | +0.00000000 | +0.00000000 | +0.00000000 | +0.00000000 | 41.25% |
| 2 | sgd_native | 0.01000000 | -0.00454064 | +0.00080609 | -0.00534673 | +0.00146341 | 38.75% |
| 2 | adam_fresh_native | 0.24975745 | +0.06879095 | +0.01136036 | +0.05743059 | +0.01540835 | 40.00% |
| 2 | sgd_direction_adam_norm | 0.24975746 | +1.53273929 | +0.24565940 | +1.28707990 | +0.03777144 | 26.25% |
| 2 | adam_direction_sgd_norm | 0.01000001 | -0.00200071 | +0.00013966 | -0.00214037 | +0.00063355 | 41.25% |

### adam_240

Baseline CE 0.00922627; conditional-choice CE 0.00912325; accuracy 100.00%.

| Batch | Condition | Actual norm | Delta CE | Delta access CE | Delta choice CE | Delta margin | Accuracy after |
|---|---|---:|---:|---:|---:|---:|---:|
| 1 | no_op | 0.00000000 | +0.00000000 | +0.00000000 | +0.00000000 | +0.00000000 | 100.00% |
| 1 | sgd_native | 0.00554498 | +0.00010287 | -0.00000186 | +0.00010473 | +0.02055962 | 100.00% |
| 1 | adam_fresh_native | 0.22784859 | +0.00479873 | +0.00002195 | +0.00477677 | +0.22594852 | 98.75% |
| 1 | sgd_direction_adam_norm | 0.22784858 | +0.76863069 | +0.54020321 | +0.22842749 | -2.64858398 | 85.00% |
| 1 | adam_direction_sgd_norm | 0.00554486 | +0.00007263 | -0.00000085 | +0.00007348 | +0.00961094 | 100.00% |
| 1 | adam_carry_native | 0.02815626 | +0.00082547 | -0.00001789 | +0.00084336 | -0.00516751 | 100.00% |
| 1 | adam_carry_direction_sgd_norm | 0.00554498 | +0.00013241 | -0.00000467 | +0.00013708 | -0.00077660 | 100.00% |
| 2 | no_op | 0.00000000 | +0.00000000 | +0.00000000 | +0.00000000 | +0.00000000 | 100.00% |
| 2 | sgd_native | 0.00699001 | -0.00045633 | -0.00000259 | -0.00045374 | +0.03915598 | 100.00% |
| 2 | adam_fresh_native | 0.23073323 | +0.00068687 | -0.00001011 | +0.00069698 | -0.12724063 | 100.00% |
| 2 | sgd_direction_adam_norm | 0.23073321 | +0.36452944 | +0.02498934 | +0.33954010 | -2.89275424 | 90.00% |
| 2 | adam_direction_sgd_norm | 0.00698992 | -0.00010639 | -0.00000076 | -0.00010564 | +0.00277281 | 100.00% |
| 2 | adam_carry_native | 0.03141858 | +0.00021756 | -0.00001819 | +0.00023575 | +0.01923754 | 100.00% |
| 2 | adam_carry_direction_sgd_norm | 0.00699001 | -0.00000563 | -0.00000538 | -0.00000025 | +0.00517023 | 100.00% |

### Local interpretations and boundaries

1. Enlarging SGD is insufficient as a simple explanation or repair of long-run failure. Scaled SGD changes CE by −0.65049/−0.61713 at Base, but +0.97545/+1.53274 at SGD240 and +0.76863/+0.36453 at Adam240. This counters “larger is always better”; no training with an alternative SGD learning rate was run.
2. Larger Base CE gains remain candidate-access dominated: access CE falls by 0.90394/0.90427 while choice CE rises by 0.25345/0.28714. Candidate adaptation remains a live explanation; CE gain alone is not rule learning.
3. SGD/fresh-Adam direction cosines are approximately 0.192–0.306; fresh/carry-Adam cosines at Adam240 are 0.0862/0.2104. Direction and history differ beyond scalar step size. Local ordering depends on state, batch and metric; it does not identify the sole mechanism behind 1,200-step AdamW success.
4. Mean endpoint margin also cannot replace all prediction outcomes: scaled SGD at SGD240, batch 2 raises margin by 0.03777 but worsens CE by 1.53274 and lowers accuracy to 26.25%. Margin compares only two endpoints, and its mean hides individual variation. Retain CE, margin and full-vocabulary accuracy together.

### First-order prediction and finite remainder

| State | Batch | First-order CE, SGD to Adam norm | Actual deltaCE | Finite remainder |
|---|---:|---:|---:|---:|
| base | 1 | -2.43499633 | -0.65049217 | +1.78450416 |
| base | 2 | -2.43282950 | -0.61713265 | +1.81569685 |
| sgd_240 | 1 | -0.42982354 | +0.97544721 | +1.40527074 |
| sgd_240 | 2 | -0.18309738 | +1.53273929 | +1.71583668 |
| adam_240 | 1 | +0.00273537 | +0.76863069 | +0.76589532 |
| adam_240 | 2 | -0.02291621 | +0.36452944 | +0.38744566 |

At these larger steps the first-order prediction sometimes has the wrong sign. Measure actual displacement and finite change instead of relying only on gradient dot products. The remainder cannot by itself separate nonlinearity from residual numeric mismatch or establish a long-run mechanism.

[Raw results](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/optimizer_probe/full/results.json) · [Independent audit](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/optimizer_probe/full/independent_audit.json) · [Full probe reading record](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/optimizer_probe/full/independent_audit_cn.md).

## 15. Completion and asset handoff

Five Smoke and 11 Full assets are actually registered and pass the selected strict access checks. Full has nine adapter families with eight members each, totaling 72 complete states, plus mapping and probe analysis families. Smoke has three adapter families with nine states total, plus two analysis families. Adapters require the exact registered Base; they are not standalone language models. Stage qualification and read-only consistency audits remain separate.

[Smoke registration](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/smoke_registration_receipt.json) · [Full registration](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/full_registration_receipt.json) · [Current Full access](/data/250010109/Research_System/assets/checks/2026-10-11_a17_transfer_20261011t160256z_full_outputs.json) · [72-state payload audit](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/analysis/checkpoint_verification.json) · [Freeze verification](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/freeze_end_verification.json).

Task completion describes execution and evidence delivery. Scientific transitions, mechanism confirmation, the next experiment and question closure remain researcher-owned. No commit, push or publication was performed.
