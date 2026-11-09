# Explanation appendix: original itemized E00–E10 record

[Start with Summary](summary.md) · [Methods and evidence](detailed.md) · [中文完整逐项解释](explanation_appendix_cn.md)

This appendix preserves the pre-revision factual account and long tables within the same experiment. Summary is the current first reading; Detailed explains the measurement and evidence trail. Execution-time statements retain their historical scope. This editorial reorganization changes no measurements.

---

1. Behavior and factor controls: when predictions change.
2. Representations and layerwise organization: what is observable/readable.
3. Functional interventions and quality: whether replacements affect predictions and whether measurements are credible.

# Frozen-small-model relation audit V3: factual first pass

Scientific conclusion: **PENDING_RESEARCHER_REVIEW**. This is an exploratory audit of composition/distance and prediction use in the existing frozen Qwen3-0.6B Base (28 blocks, hidden1024), motivated by the MoE information-sharing question. It does not accept/refute a mechanism or rank architectures. The researcher approved the complete E00–E10 first flow, English spatial chains C=1/3, existing qualified dictionaries and capped H100 Reserved resources. No main-model or new dictionary training occurred.

The dataset has2048 variants of128 graph/entity families. TRAIN/DEV/TEST have1024/384/640 rows and64/24/40 independent families with disjoint template sets. Every family contains C×D×relation reversal×paraphrase variants. A directed-graph solver establishes unique answers and verifies each necessary edge by deletion. C is required relation count, not internal reasoning steps. D reorders the same12 facts by moving a fixed five-fact neighborhood, recording actual tokenizer distances; order remains a confound. Relation/combination exposure F is unavailable and stays BLOCKED. Word frequency and dictionary occurrence are not replacements. Eight actual example inputs have explicitly unassigned F, not eight measured frequency conditions.

The main observable is correct-candidate minus incorrect-candidate log probability in nat, comparing single-token No/Yes continuations. Family-paired deep far-minus-near minus shallow far-minus-near is the primary descriptive contrast. Bootstrap intervals resample40 TEST families2000 times and do not cover pretraining randomness. No practical-success threshold or posthoc scientific pass is supplied. Candidate scoring is not free generation.

## Reading guide: the measured objects

This frozen-model audit compares one versus three necessary relations and nearer versus farther evidence. It does not train the main model, assign experts, or test common-parameter update schedules.

For each input token position, every block produces1024 numbers. A **state** here is that vector at one specified layer and position for one specified input. A **complete state** retains all1024 coordinates of the block output before dimensional projection or dictionary reconstruction. Complete refers to this vector, not all positions, every internal tensor, the model parameters, or all model knowledge. It does not guarantee lossless text recovery or decodable relations. Main-model parameters are shared computation weights and remain fixed; input-dependent states change.

Actual row1408 has155 token positions. A whole-layer sequence state therefore has155 rows by1024 columns. This audit caches the answer-prefix final-position row plus the one or three necessary-evidence-end rows, rather than all155 rows. “Query position” means the final token before the answer begins. Its state subsequently passes through final normalization and the language-model head for candidate scoring.

A **block increment** subtracts the block input vector from its output vector at the same position. It measures the net numerical change, including additions, cancellations and recoding; it is not independently identified new relation knowledge. A representation space describes these vectors using coordinates, distances and directions; coordinates have no assumed one-to-one semantic labels.

DistanceD is a property of evidence placement within the current text: means are approximately33–36tokens near and104–106far. CompositionC counts one or three necessary relations, independently of distance. FrequencyF means learning exposure to a relation or full combination. Exposure may affect learned encoding or use, but this round has neither a reliable exposure estimate nor a controlled-frequency manipulation. It cannot identify high-frequency/short-distance/common or low-frequency/long-distance/specialized spaces. Reordering evidence can also change order effects.

E01–E02 check labels and answers; E03 compares saved vectors; E04 finds shared variation directions; E05 fits an external answer classifier; E06 compares aligned-layer organization; E07 examines existing dictionary codes with real text; E08 retains/removes directions; E09 swaps donor states; E00/E10 guard measurement and coverage. Numerical difference, external readability and actual model use are distinct questions.

A direct recount of the saved TEST rows gives320Yes/320No truths,611No selections including40 exact ties resolved by the frozen No-first rule, and329/640correct (51.41%). Actual relation-reversal rows1408/1412 both receiveNo. Internal differences alone do not establish stable relation use. Read this guide, the actual examples and E01–E03 before the spectral and intervention detail. Comprehension questions are deferred until the researcher finishes reading.

## E00 Calibration

Native/full versus read-hook scores and initial self-write scores differed by0 in both workers, against preregistered absolute tolerances.02/.005nat. Main-model trainable count was0 and complete before/after parameter hashes matched. Full block output, FP32 output-minus-input increments and layer27 normalized MLP input are distinct hooks. Later cross-batch cached self-write differences reached.25nat; affected functional outputs were INVALID and retained. The repair uses newly captured native states/scores in exactly the intervention batches, tests all chosen no-ops against unchanged tolerances, and provides a separate terminal receipt. Numerical replay is not evidence of relation reasoning.

## E01 Data and shortcuts

All2048 solver/necessity/split checks passed. The TRAIN-fitted word-bag baseline scored0.5000; the first/last-fact query-role/degree baseline scored0.5375. These do not exclude all shortcuts. Total facts/entity counts match; small token-length differences and template transfer remain. Actual token conditions:

| C | D | 测试题数 | token长度范围 | 证据距离均值/token | 每题平均距离范围/token |
|---|---|---|---|---|---|
| 1 | near | 160 | 155–160 | 35.531250 | 13.000–55.000 |
| 1 | far | 160 | 155–160 | 106.193750 | 83.000–128.000 |
| 3 | near | 160 | 155–161 | 33.327083 | 23.000–44.667 |
| 3 | far | 160 | 155–161 | 103.989583 | 93.000–115.667 |


## E02 Behavior

Every condition has160 TEST rows/40 families. Positive margin favors the correct candidate. Pair accuracy requires both reversed relations correct. All legal errors are retained.

| C | D | 题数/题族 | 正确答案优势 nat，95%区间 | 候选准确率，95%区间 | 反转两题均对，95%区间 |
|---|---|---|---|---|---|
| 1 | near | 160/40 | 0.005469 [-0.025020, 0.036719] | 0.531250 [0.500000, 0.562500] | 0.075000 [0.025000, 0.137500] |
| 1 | far | 160/40 | -0.000000 [-0.026563, 0.028125] | 0.537500 [0.506250, 0.575000] | 0.087500 [0.037500, 0.150000] |
| 3 | near | 160/40 | -0.007031 [-0.037500, 0.022656] | 0.481250 [0.450000, 0.512500] | 0.025000 [0.000000, 0.062500] |
| 3 | far | 160/40 | 0.011719 [-0.005469, 0.029687] | 0.506250 [0.500000, 0.518750] | 0.012500 [0.000000, 0.037500] |


| 配对差值 | 均值及95%题族区间，nat |
|---|---|
| distance_shallow | -0.005469 [-0.028926, 0.017187] |
| distance_deep | 0.018750 [-0.007813, 0.045332] |
| depth_near | -0.012500 [-0.057812, 0.028906] |
| depth_far | 0.011719 [-0.021094, 0.042969] |
| interaction | 0.024219 [-0.011719, 0.060937] |


The cell plot uses relation count on x, correct margin(nat) on y, near/far lines and family means; it has no error bars, so intervals are read from the table. The Chinese companion traces actual correct and incorrect inputs through solver labels, token positions and raw probabilities, without fabricated examples.

Exact candidate-score ties select No under the frozen candidate ordering [No, Yes], as implemented before execution; ties remain included. [Tie counts](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E02/tie_guard.json) provide a separate guard.

## E03 States and increments

All2048 rows,28 layers, query and all4096 actual necessary evidence ends are cached. Padded duplicate C1 slots are excluded from actual-position counts. Norms, relation reversal distances/cosines and same-relation rewrite distances are reported before/after unit normalization. Distances describe numbers, not semantic difference or task difficulty. The norm plot separates complete state and block increment; axes are layer and Euclidean norm.

## E04 PCA/SVD

Named sample×hidden matrices are analyzed separately by hook. Raw and TRAIN-centered spectra, entropy effective rank and TRAIN-fitted heldout retention are reported for every layer and equal256-row condition matrices. PCA estimates means/directions from TRAIN only; TEST energy/reconstruction is measured without refitting. Effective rank is exp(entropy of normalized squared singular values), limited by sample size. A sample-specific rank1 oracle retaining its own nonzero vector is an algebraic identity, not a shared deployable subspace. Removing PC1 is not removing common ability. Fixed-grid numeric examples:

| 对象 | 层 | 训练矩阵有效秩 | 测试rank1保留量 | 测试rank16保留量 | 测试rank64保留量 |
|---|---|---|---|---|---|
| residual | 0 | 5.803002 | 0.208681 | 0.567532 | 0.717169 |
| residual | 7 | 10.481549 | 0.053037 | 0.409322 | 0.683887 |
| residual | 13 | 17.143322 | 0.022206 | 0.364675 | 0.654635 |
| residual | 20 | 22.873104 | 0.035287 | 0.517294 | 0.707569 |
| residual | 27 | 33.863758 | 0.044920 | 0.478150 | 0.718719 |
| increment | 0 | 5.803137 | 0.208683 | 0.567535 | 0.717168 |
| increment | 7 | 11.776028 | 0.056953 | 0.414137 | 0.689467 |
| increment | 13 | 16.868679 | 0.057237 | 0.432433 | 0.725491 |
| increment | 20 | 18.617516 | 0.040696 | 0.524553 | 0.700641 |
| increment | 27 | 31.385487 | 0.067435 | 0.475185 | 0.721569 |


## E05 Linear readout

All28 query-state layers have1025-parameter logistic heads and same-capacity shuffled-TRAIN-label controls. TRAIN-only standardization, CE + lambda mean(weight squared), capacity and DEV choice over L2 .001/.01/.1 are unchanged. Initial AdamW and bounded L-BFGS attempts were INVALID for optimization and retained. Final CPU float64 exact-Hessian Newton fits qualify all168 candidates and56 selected heads at the unchanged gradient bound1e-5, maximum selected gradient8.672e-7; every accepted update is logged. The final DEV-selected layers are15/27 and only dependent E09 was rerun. Earlier TEST outputs had already been exposed: the entire round remains exploratory, not a fresh confirmation. Initial/per-update/final losses, finite gradients, counters, TensorBoard and actual head/numerical state are retained; classifier labels are not LM training tokens. Intermediate oriented-path labels duplicate final reversal labels in this task and no independent target was invented. Readability is not model use or computation onset.

| 层（从0计） | 真实标签准确率及95%区间 | 乱序训练标签准确率及95%区间 | 真实标签L2 |
|---|---|---|---|
| 0 | 0.487500 [0.467187, 0.506250] | 0.492188 [0.468750, 0.514062] | 0.1 |
| 1 | 0.500000 [0.500000, 0.500000] | 0.498437 [0.495312, 0.500000] | 0.1 |
| 2 | 0.482812 [0.456250, 0.507852] | 0.479687 [0.451562, 0.507812] | 0.1 |
| 3 | 0.500000 [0.500000, 0.500000] | 0.515625 [0.498437, 0.537500] | 0.1 |
| 4 | 0.498437 [0.495312, 0.500000] | 0.507812 [0.487500, 0.529687] | 0.1 |
| 5 | 0.500000 [0.500000, 0.500000] | 0.507812 [0.490625, 0.526563] | 0.1 |
| 6 | 0.500000 [0.500000, 0.500000] | 0.500000 [0.500000, 0.500000] | 0.1 |
| 7 | 0.493750 [0.465625, 0.521875] | 0.493750 [0.457813, 0.526602] | 0.1 |
| 8 | 0.493750 [0.468750, 0.520312] | 0.498437 [0.492188, 0.503125] | 0.1 |
| 9 | 0.501563 [0.500000, 0.504687] | 0.501563 [0.500000, 0.504687] | 0.1 |
| 10 | 0.500000 [0.475000, 0.523438] | 0.500000 [0.500000, 0.500000] | 0.1 |
| 11 | 0.518750 [0.490625, 0.548438] | 0.498437 [0.478125, 0.518750] | 0.1 |
| 12 | 0.498437 [0.490625, 0.504687] | 0.496875 [0.490625, 0.503125] | 0.1 |
| 13 | 0.514062 [0.490625, 0.539062] | 0.489063 [0.462500, 0.515625] | 0.1 |
| 14 | 0.493750 [0.468750, 0.518750] | 0.496875 [0.481250, 0.510977] | 0.1 |
| 15 | 0.493750 [0.453125, 0.534375] | 0.485938 [0.451562, 0.520312] | 0.1 |
| 16 | 0.512500 [0.498437, 0.528125] | 0.496875 [0.465625, 0.528125] | 0.1 |
| 17 | 0.500000 [0.470313, 0.529687] | 0.507812 [0.479687, 0.534375] | 0.1 |
| 18 | 0.504687 [0.481250, 0.529687] | 0.507812 [0.485938, 0.531250] | 0.1 |
| 19 | 0.501563 [0.485938, 0.515625] | 0.523438 [0.509375, 0.539062] | 0.1 |
| 20 | 0.515625 [0.484375, 0.546875] | 0.503125 [0.495312, 0.512500] | 0.1 |
| 21 | 0.495312 [0.482812, 0.507852] | 0.517188 [0.487500, 0.545312] | 0.1 |
| 22 | 0.514062 [0.492188, 0.535937] | 0.490625 [0.465625, 0.514062] | 0.1 |
| 23 | 0.506250 [0.482812, 0.529687] | 0.510938 [0.492188, 0.531250] | 0.1 |
| 24 | 0.507812 [0.479687, 0.534375] | 0.506250 [0.479687, 0.531250] | 0.1 |
| 25 | 0.503125 [0.462500, 0.543750] | 0.478125 [0.445312, 0.510938] | 0.1 |
| 26 | 0.521875 [0.501563, 0.545312] | 0.487500 [0.470313, 0.501563] | 0.1 |
| 27 | 0.517188 [0.484375, 0.551562] | 0.495312 [0.468711, 0.520312] | 0.1 |


## E06 Similarity and subspaces

Aligned-row linear CKA matrices cover all layers, four C/D cells, complete states/increments and relation-difference vectors. CKA normalizes the inner product of centered linear Gram matrices; it is not functional equivalence. TRAIN-estimated rank16 subspace overlap, TEST retained energy and ten random references are preserved, with separate condition-fitted bases. Heatmaps have layer on both axes, color denotes the statistic and no uncertainty bars. High similarity does not establish that a layer is unnecessary.

## E07 Existing dictionaries

A22 uses its saved TRAIN centered vector-RMS normalization and threshold,14 odd-index block outputs and16384 shared acausal features. Aggregate reconstruction FVE against the saved TRAIN mean is0.767563; each layer's error and same-batch reconstruction behavior are recorded. Occurrence probability/amplitude are measured at actual task positions, not training exposure. Representative features are selected on TRAIN and shown with real texts and inactive cases; none is named common from an ID or energy. SAE's different normalized MLP-input interface is separately checked; its task-TRAIN-mean FVE is-4.270350, statusINVALID, so its dependent feature interpretation is invalid. It does not cancel native/A22 work. Feature-level causal interventions remain BLOCKED without a separately qualified relation feature.

## E08 Projection/removal

Status:DONE_EXPLORATORY. The fixed five layers, ranks1/16/64, amplitudes.1/.5/1, mean-restored PCA, equal-rank random and PC1-removal conditions total105×80 receiver measurements. Report reconstruction error and correct-answer NLL/margin changes together. Positive NLL change lowers correct-answer probability; high retained energy does not establish functional retention. Earlier invalid batch-reference outputs are retained separately.

| 层 | 方法/rank | 幅度 | 题数 | 表征相对误差 | 正确优势变化nat及区间 | 答案NLL变化nat及区间 |
|---|---|---|---|---|---|---|
| 0 | PCA/16 | 1.0 | 80 | 0.496554 | -0.012500 [-0.028125, 0.003125] | 0.005838 [-0.002286, 0.012744] |
| 0 | random/16 | 1.0 | 80 | 0.979840 | 0.001563 [-0.015625, 0.020312] | -0.003124 [-0.013924, 0.005484] |
| 7 | PCA/16 | 1.0 | 80 | 0.655748 | 0.000000 [-0.015625, 0.017188] | -0.017109 [-0.025616, -0.008925] |
| 7 | random/16 | 1.0 | 80 | 0.981591 | -0.001563 [-0.017188, 0.012500] | -0.008550 [-0.016621, -0.000975] |
| 13 | PCA/16 | 1.0 | 80 | 0.633884 | -0.010938 [-0.025000, 0.004687] | -0.002716 [-0.010596, 0.004785] |
| 13 | random/16 | 1.0 | 80 | 0.990120 | -0.015625 [-0.031250, 0.000000] | 0.033574 [0.025914, 0.040972] |
| 20 | PCA/16 | 1.0 | 80 | 0.527372 | -0.003125 [-0.017227, 0.010938] | 0.007699 [-0.001692, 0.015920] |
| 20 | random/16 | 1.0 | 80 | 0.988487 | -0.006250 [-0.029688, 0.017188] | -0.009713 [-0.032212, 0.011211] |
| 27 | PCA/16 | 1.0 | 80 | 0.637550 | -0.000000 [-0.025000, 0.025000] | -0.048345 [-0.073902, -0.023194] |
| 27 | random/16 | 1.0 | 80 | 0.984532 | -0.007812 [-0.034375, 0.018750] | -0.061420 [-0.097792, -0.028371] |


## E09 Donor replacements

Status:DONE_EXPLORATORY. Two layers are selected only by DEV readout accuracy, ties earliest. Query and first-evidence ends have self, same-relation and reversed-relation donors, both reversal directions, and correct/incorrect receiver groups. Original alternate-template controls rarely match positions/length exactly and remain confounded exploratory observations. A separate same-relation irrelevant-fact-order rewrite preserves all relations/entities/answers and is selected by exact tokenizer length/all-hook alignment before model scoring; it provides80 matched controls. It is an order rewrite, not a lexical paraphrase or equal-size perturbation. Full state can transport answers/entities/context; an effect is not a specific relation mechanism, and wrong-prediction patches are not correct reasoning evidence.

| 层 | 位置槽 | 供体 | 题数 | 正确优势变化nat及区间 | 答案NLL变化nat及区间 | 原生正确/错误数 |
|---|---|---|---|---|---|---|
| 15 | 0 | self | 80 | 0.000000 [0.000000, 0.000000] | 0.000000 [0.000000, 0.000000] | 40/40 |
| 15 | 0 | same_relation_paraphrase | 80 | -0.001563 [-0.020313, 0.014062] | 0.012796 [-0.000937, 0.027459] | 40/40 |
| 15 | 0 | opposite_relation | 80 | -0.014063 [-0.032813, 0.007812] | 0.005648 [-0.007100, 0.015840] | 40/40 |
| 15 | 1 | self | 80 | 0.000000 [0.000000, 0.000000] | 0.000000 [0.000000, 0.000000] | 40/40 |
| 15 | 1 | same_relation_paraphrase | 80 | -0.007813 [-0.020313, 0.006250] | 0.002270 [-0.004894, 0.009268] | 40/40 |
| 15 | 1 | opposite_relation | 80 | -0.009375 [-0.031250, 0.010938] | 0.006041 [-0.003056, 0.015701] | 40/40 |
| 27 | 0 | self | 80 | 0.000000 [0.000000, 0.000000] | 0.000000 [0.000000, 0.000000] | 40/40 |
| 27 | 0 | same_relation_paraphrase | 80 | -0.000000 [-0.062500, 0.059375] | -0.088298 [-0.130415, -0.049128] | 40/40 |
| 27 | 0 | opposite_relation | 80 | -0.006250 [-0.050000, 0.034375] | 0.003125 [-0.017187, 0.025000] | 40/40 |
| 27 | 1 | self | 80 | 0.000000 [0.000000, 0.000000] | 0.000000 [0.000000, 0.000000] | 40/40 |
| 27 | 1 | same_relation_paraphrase | 80 | 0.000000 [0.000000, 0.000000] | 0.000000 [0.000000, 0.000000] | 40/40 |
| 27 | 1 | opposite_relation | 80 | 0.000000 [0.000000, 0.000000] | 0.000000 [0.000000, 0.000000] | 40/40 |


| 层 | 位置槽 | 严格匹配题数 | 平均正确优势变化/nat | 替换状态距离均值 |
|---|---|---|---|---|
| 15 | 0 | 80 | -0.000000 | 1.604903 |
| 15 | 1 | 80 | 0.001562 | 4.195558 |
| 27 | 0 | 80 | 0.001562 | 26.424279 |
| 27 | 1 | 80 | 0.000000 | 43.657113 |


[C/D-stratified E08](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E08/stratified_CD_results.json) has420 condition cells; [E09](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E09/stratified_CD_results.json) has64. Per-row requested and actual BF16 written-state errors/norm shifts are separate from condition-wide reconstruction errors. Evaluation-set centering in CKA defines the statistic and is not used to fit prediction or select layers; PCA directions remain TRAIN-only.

## E10 Reproduction and coverage

An independent scalar recomputation gives primary contrast0.024218754470nat versus registered0.024218753725, absolute difference7.45e-10. A256×1024 CPU FP64 Gram trace/eigenvalue check differs relatively by1.17e-16. An overly exact first comparison exposed float32 subtraction versus float64 recomputation; both values and a machine-epsilon-derived bound are retained, without changing any model/no-op tolerance. Successful platform exit is not scientific eligibility.

5 platform attempts served two logical workers, including bounded worker0 repairs; maximum concurrency stayed two single H100 Reserved allocations. Runtime GPU hours=0.2989; conservative submission-to-completion upper bound=0.6342<4GPUh, and each logical worker<2h. These are timestamps, not billing. All jobs ended.

T1 readout/T2 statistics ran; T3 new dictionaries did not. T4 controlled-exposure and T5 common/remaining are audit-only, with21 separate scientific/data/implementation audit records including the two numerical T1 amendments. A proposed complementary4:1 allocation balances atom marginals for three-atom binary combinations; C1 atom and complete-combination frequency cannot be varied independently. No training evidence is implied. The two existing analysis skills and shared review contract were minimally changed; installed routes and structural/link checks are evidenced, without claiming guaranteed future automatic invocation.

| 项目 | 最终状态 | 主要证据 |
|---|---|---|
| E00 | DONE_VALID | [资产与数值校准](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E00/status.json) |
| E01 | DONE_VALID | [任务与捷径](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E01/status.json) |
| E02 | DONE_EXPLORATORY | [全条件行为](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E02/status.json) |
| E03 | DONE_EXPLORATORY | [原始状态与层增量](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E03/status.json) |
| E04 | DONE_EXPLORATORY | [表征谱](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E04/status.json) |
| E05 | DONE_EXPLORATORY | [线性读出](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E05/status.json) |
| E06 | DONE_EXPLORATORY | [跨层比较](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E06/status.json) |
| E07 | DONE_EXPLORATORY | [现有字典](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E07/status.json) |
| E08 | DONE_EXPLORATORY | [低维保留与移除](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E08/status.json) |
| E09 | DONE_EXPLORATORY | [配对状态替换](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E09/status.json) |
| E10 | DONE_VALID | [独立计算与完整账本](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E10/independent_arithmetic.json) |


| 子项 | 状态 | 缺口/边界 |
|---|---|---|
| F | BLOCKED | 没有可靠的关系/组合学习暴露量；仅完成C×D四格。 |
| SAE | INVALID | 本任务重构误差比任务训练均值基准更大，相关特征解释无效。 |
| CrossCoder | DONE_EXPLORATORY | 覆盖登记的14层；是特征激活统计，不是学习暴露。 |
| E05_intermediate_readout | BLOCKED | 本任务中候选中间标签与最终标签重复，未另造读出目标。 |
| E09_feature_intervention | BLOCKED | 没有独立验证的关系特征；跨层联合编码不能直接当作层内因果目标。 |
| T3_new_dictionary_training | BLOCKED | 未授权，未运行；需要单独的字典训练协议。 |
| T4_frequency_training | BLOCKED | 仅完成设计审计；精确训练设置与独立批准仍缺失。 |
| T5_common_remaining_training | BLOCKED | common/remaining和调度尚未操作定义；只审计设计。 |
| E09_strict_same_relation | DONE_EXPLORATORY | 事实顺序改写对齐合格，但不是词句改写，也不是同幅度的关系扰动。 |


The applicable native C×D work is measured; explicit F/dictionary/optional blockers remain. DONE_EXPLORATORY is not scientific success; INVALID/FAILED/BLOCKED are retained. Read the factual evidence first and state your observations before AI interpretation. What patterns do you observe in behavior and all-layer readout? Which quantities describe geometry, readability or replacement effects without establishing successful relation use?
