# Detailed: how the relation audit was measured and how to trace its values

[Start with Summary](summary.md) · [Itemized appendix](explanation_appendix.md) · [中文](detailed_cn.md) · [Frozen Protocol](protocol.md)

**This round measures a fixed model's behavior, representations and response to state replacements.** TEST accuracy is 329/640; the primary four-cell interaction is +0.024219 nat [−0.011719, 0.060937]. The sections follow the reader's dependencies: task, scoring, internal tools, validity repairs and provenance. Mechanism judgment remains PENDING_RESEARCHER_REVIEW. The [appendix](explanation_appendix_cn.md) retains the complete E00–E10 A–F account, all-layer tables, eight full inputs and two traced cases.

## 1. Why four cells, rather than eight?

Encode “A is left of B” as a directed edge from A to B. Each item contains 13 entities and 12 facts. The external solver labels Yes or No only when one query direction is reachable; ambiguity is not converted to No. It deletes every necessary edge to verify that the answer requires that relation.

**C counts necessary relations.** A direct fact suffices for C=1; C=3 requires three edges. Actual row 1416 contains Carol right of Sam, Carol left of Mary, and Bob right of Mary, yielding Sam→Carol→Mary→Bob and answer Yes. The [appendix](explanation_appendix_cn.md) gives the full English input. Both depths retain 12 facts and matched entity counts and approximate length; relevant-path and distractor composition still differ.

**D measures evidence placement.** Reorder the identical fact set, moving a fixed five-fact neighborhood containing both query endpoints' incident relations. Rows 1408/1410 keep facts and answer while the necessary-evidence distance changes from 33 to 103 tokenizer positions. TEST mean distances for C1 near/far are 35.531250/106.193750; C3 gives 33.327083/103.989583. Lengths are 155–161 tokens. Fact order remains a confound of distance.

**F means learning exposure.** No traceable relation-exposure estimate or controlled training intervention exists here. Only C×D is measured. The appendix's eight requested F slots all have unknown actual F; word frequency and dictionary activation probability do not fill them.

Each family has 2C×2D×2 relation directions×2 wordings, or 16 variants. There are 128 families/2,048 rows, with 64/24/40 TRAIN/DEV/TEST families and 1,024/384/640 rows. Template sets are 0–3/4–5/6–7. Entity/rendering assignments vary across families, but all share a 13-node chain topology. This is entity/template holdout, not topology generalization. TRAIN-fitted word-bag and first/last-fact entity-role/degree baselines score 50.00% and 53.75% on TEST; they audit specified shortcuts, not every possible strategy.

[Data and balance](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/data/data_audit.json) · [Complete inputs](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/data/dataset.jsonl) preserves generation, necessity and balance; [Token positions](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E01/token_metadata.json) preserves actual positions. All legal difficult items and incorrect predictions remain.

## 2. From candidate probabilities to the four-cell comparison

For the same prefix, read conditional log probabilities of single-token ` No` and ` Yes`, IDs 2308/7414. They are probabilities in the full vocabulary, not renormalized to sum to one across the two candidates.

**Correct-answer margin** = log p(correct) − log p(incorrect). Row 1408 has truth Yes, No=−0.685887814, Yes=−1.310887814 and margin −0.625. Reversed row 1412 has truth No, No=−0.650239527, Yes=−1.400239468 and margin +0.749999940. Both select No, so one reversal pair has only one correct item. Opposite correct-answer signs can cancel in a near-zero cell mean without making individual items near ties.

**Candidate accuracy** checks the larger candidate, with the frozen No-first tie rule. **Reversal-pair accuracy** requires both relation directions to be correct at the same family/C/D/wording. TEST truths are balanced 320/320, selections include 611 No with 40 exact ties, and 329/640 items are correct. Four-cell pair accuracies are 7.50%, 8.75%, 2.50% and 1.25%, using a different denominator from item accuracy.

**Correct-answer negative log likelihood (NLL)** = −log p(correct). A positive intervention-minus-native NLL change lowers correct-answer probability. Because other vocabulary items also carry probability, Yes and No may rise together with little change in their contrast. Intervention tables therefore retain both NLL and margin.

Average variants within each family, then weight the 40 TEST families equally. The primary comparison is

\[
I=(M_{3,far}-M_{3,near})-(M_{1,far}-M_{1,near}),
\]

where M is the family-equal margin. Shallow far-minus-near is −0.005469 and deep is +0.018750, giving I=+0.024219 nat [−0.011719,0.060937]. The 2,000 bootstrap draws resample whole paired families; they do not treat 640 items as independent or represent training-seed variation. No practical-success threshold was registered. [Per-item scores](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E02/per_row.jsonl) · [Cell and paired statistics](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E02/results.json) · [Tie counts](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E02/tie_guard.json)

## 3. Which internal vector is saved?

Each token has 1,024 numbers at each layer. A **complete state** is the specified block-output vector at one position. A **block increment** subtracts its same-position block input in FP32. The complete state accumulates prior content; the increment records this block's numerical change. These are separate matrix objects.

The primary position is the last prefix token before the answer. Necessary-fact ends are also saved. Row 1408 has 155 tokens, query index 154 and necessary-evidence end 121. The cache saves these registered rows, not all 155 sequence positions. Four padded slots unify array shape; duplicate C1 evidence slots are not counted again. Coverage is 2,048 query positions, 4,096 actual evidence ends and all 28 blocks. Indices are zero-based; blocks 15/27 mean the 16th/28th block. SAE separately reads normalized final-layer MLP input, not block output. [Tensor interfaces](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E00/interfaces.json) · [All evidence ends](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E03/all_evidence_norms.jsonl)

## 4. What geometry tools measure: E03, E04 and E06

### How relation reversal changes the state

E03 subtracts matched state vectors and takes the square root of summed squared coordinates: Euclidean distance. The same operation on one vector is its norm, or overall magnitude. Unit-normalized distances and cosines provide a comparison after removing overall scale.

For C1-near, state norms at blocks 0/13/27 are 6.702474/38.302616/583.017944. Reversal distances are 0.048744/1.611201/43.490314; unit-normalized distances are 0.007217/0.041760/0.074064. Raw distances grow with scale; 43.49 is not a semantic-distance unit. All layers and actual evidence positions are in [All-layer statistics](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E03/layer_statistics.json).

### Shared directions: PCA and SVD

E04 places each query vector in one row. Principal component analysis (PCA) subtracts the TRAIN mean and finds orthogonal directions of largest TRAIN variation. Singular value decomposition (SVD) supplies directions and strengths. The spectrum contains squared singular values; energy is the sum of squared centered values. TEST only projects into frozen TRAIN directions.

Every C/D TRAIN matrix has 256 rows; pooled TRAIN has 1,024. States/increments and raw/centered spectra remain distinct. Entropy effective rank exponentiates the entropy of normalized spectral energy, giving an equivalent direction count, limited by sample size. It is not integer matrix rank. State effective rank at blocks 0/27 is 5.803002/33.863758, while leading 64 TRAIN directions retain TEST energy 0.717169/0.718719. Block-27 rank-16 retention is 0.478150 for states and 0.475185 for increments.

Held-out retention tests sharing more directly than selecting a separate direction for each sample: any nonzero sample retains 100% in its own rank-one direction by construction. Mean and PC1 removal are specified statistical diagnostics. [Spectra and retention](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E04/spectra.json) · [Cellwise held-out retention](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E04/condition_heldout_retention.json)

### Cross-layer geometry: CKA and subspaces

E06 builds a sample-by-sample inner-product table within each layer and compares two centered tables. Centered kernel alignment (CKA) is their inner product divided by their norms. It compares the geometry of aligned samples without equating individual coordinates. Evaluation-set centering defines the statistic; it fits no predictor and selects no layer.

The C1-near matrix containing the traced cases has block-13/14 CKA 0.995679. This is a 160-row statistic, not a per-item CKA. Four cells, two vector objects and state/reversal-difference versions yield 16 complete 28×28 matrices. Separately, fixed-rank-16 TRAIN subspaces receive projector overlap, TEST retention and ten random references. Equal rank controls dimension, but high CKA does not establish equal function or layer dispensability. [CKA and subspaces](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E06/results.json) · [Cellwise subspaces](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E06/condition_subspaces.json)

## 5. Readout fitting and generalization: E05

A probe is a small classifier that predicts Yes/No from the 1,024 query-state values. Each layer has true-TRAIN-label and shuffled-TRAIN-label fits. Read TRAIN, DEV and TEST together first. Fixed blocks 0/13/27 appear below; all 28 blocks and intervals remain in the [appendix](explanation_appendix.md).

| Block | TRAIN CE | DEV CE | True-label TEST accuracy, % | Shuffled-label TEST accuracy, % |
|---|---|---|---|---|
| 0 | 0.122844 | 14.719437 | 48.750 | 49.219 |
| 13 | 0.109730 | 3.497388 | 51.406 | 48.906 |
| 27 | 0.132951 | 4.312807 | 51.719 | 49.531 |

Cross-entropy (CE) is the average negative log probability assigned to the true label; lower means greater probability on that label. TRAIN describes fit to seen items, DEV selects regularization, and TEST accuracy describes unseen families/templates. Shuffled-label fits randomize TRAIN targets but score true TEST labels, providing an equal-capacity chance reference. Here TRAIN loss is low, DEV loss is high, and true/null TEST ranges are around 48%–52%. Family and template holdouts occur together, so they do not identify which transfer causes failure.

The classifier applies 1,024 weights and one bias, then sigmoid, giving 1,025 parameters per head. Its probability belongs to this external classifier. TRAIN alone standardizes coordinates; DEV cross-entropy selects L2 from 0.001/0.01/0.1. Every candidate finally reaches the specified numerical precision on the same binary-cross-entropy-plus-λ-mean-squared-weight objective. This qualification and TEST generalization are separate. Solver and gradient details appear in [section 9](#9-validity-repairs-and-excluded-measurements-e00-and-e10).

Earlier TEST outputs were already exposed; repaired results remain exploratory. [All fits](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E05/probes.json) · [Optimization diagnostics](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E05/optimization_diagnostic.json) · [Per-item readouts](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E05/test_predictions.npz)

Intermediate oriented-path labels duplicate the final reversal target, so no independent middle label was invented. Final DEV accuracy alone selects E09 blocks 15/27: both 0.513021, ties earliest. The selection locates measurements and does not depend on TEST intervention effects.

## 6. Reconstruct before describing dictionary features: E07

A **CrossCoder** uses a shared sparse code to reconstruct several specified layers. Existing A22 has 16,384 features and jointly reads 14 block outputs at indices 1/3/…/27. Its saved TRAIN centering, scale and gate threshold are loaded without recalibration on these items. The joint encoder is acausal across layers, not an online early-layer local feature.

Reconstruction fraction of variance explained (FVE) is one minus reconstruction squared error divided by a mean-reference squared error. Aggregate A22 FVE against its saved TRAIN mean is 0.767563. Twelve split/C/D groups retain activation probabilities, amplitudes and real high/low-activation examples. Activation probability is code-positive frequency at measured positions, not model learning exposure. IDs locate features within this dictionary; they are not assigned common or relation-mechanism names.

The separate **sparse autoencoder (SAE)** reads normalized final-layer MLP input. Its model parent matches, but task-TRAIN-mean FVE is −4.270350: reconstruction is worse than that mean reference. Feature interpretation is INVALID. The two FVE references differ and do not form a same-object leaderboard.

Dictionary behavior replacements separately use 16 same-batch DEV diagnostic items at each covered layer. No independently qualified relation feature exists, so feature intervention stays BLOCKED. No dictionary was trained to fill the ledger. [A22 reconstruction/behavior](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E07/crosscoder_calibration.json) · [SAE qualification](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E07/sae_calibration.json) · [Real feature cases](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E07/crosscoder/representative_features.json)

## 7. Retain or remove directions and continue prediction: E08

With TRAIN mean μ and direction basis V, replace TEST state h by μ+VVᵀ(h−μ), then continue the model. Restoring the mean separates its offset from retained variation. Equal-rank random bases test a generic dimensional bottleneck; PC1 removal tests the largest statistical direction. Partial intervention is h+α(replacement−h), with α=0.1/0.5/1 all reported.

Preregistered blocks 0/7/13/20/27, ranks 1/16/64 and PC1 removal yield 105 conditions. Receivers are 80 wording-0 items from the first ten TEST families, covering C/D and reversal. The complete five-block rank-16, full-amplitude slice follows. Remaining ranks/amplitudes are in the appendix and original table; this slice does not select favorable results.

| Block / directions | Relative state error | Margin change, nat (95% interval) | Correct-answer NLL change, nat (95% interval) |
|---|---|---|---|
| 0 / PCA16 | 0.496554 | -0.012500 [-0.028125, 0.003125] | 0.005838 [-0.002286, 0.012744] |
| 0 / random16 | 0.979840 | 0.001563 [-0.015625, 0.020312] | -0.003124 [-0.013924, 0.005484] |
| 7 / PCA16 | 0.655748 | 0.000000 [-0.015625, 0.017188] | -0.017109 [-0.025616, -0.008925] |
| 7 / random16 | 0.981591 | -0.001563 [-0.017188, 0.012500] | -0.008550 [-0.016621, -0.000975] |
| 13 / PCA16 | 0.633884 | -0.010938 [-0.025000, 0.004687] | -0.002716 [-0.010596, 0.004785] |
| 13 / random16 | 0.990120 | -0.015625 [-0.031250, 0.000000] | 0.033574 [0.025914, 0.040972] |
| 20 / PCA16 | 0.527372 | -0.003125 [-0.017227, 0.010938] | 0.007699 [-0.001692, 0.015920] |
| 20 / random16 | 0.988487 | -0.006250 [-0.029688, 0.017188] | -0.009713 [-0.032212, 0.011211] |
| 27 / PCA16 | 0.637550 | ≈0 [-0.025000, 0.025000] | -0.048345 [-0.073902, -0.023194] |
| 27 / random16 | 0.984532 | -0.007812 [-0.034375, 0.018750] | -0.061420 [-0.097792, -0.028371] |

State error is a condition-wide ratio of summed squared replacement displacement to summed native centered energy. It is not an identical per-item error. The row-level file separately retains requested states, actual BF16 writes and roundoff. Margin/NLL use freshly obtained native references in identical batches; intervals resample ten families. Projection may shift the state distribution. Correct-answer NLL does not measure full-context language loss. [105 conditions](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E08/results.json) · [Per-item state error](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E08/per_row_with_state_errors.jsonl) · [420 C/D cells](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E08/stratified_CD_results.json)

## 8. Replace a state with another item's state: E09

At DEV-selected blocks 15/27, replace either the query or first necessary-evidence end. The donor supplies the vector; the receiver continues to be scored. Self-write checks the operation; same-relation wording checks general change; opposite-relation donors test movement toward the donor answer. Bidirectional means both relation directions, not training replication.

Opposite donors match entities, C/D, template, length and position; all 160 position comparisons match exactly. All 80 receivers remain, grouped as 40 natively correct and 40 incorrect. Every opposite-donor condition is shown:

| Block / replacement site | Margin change, nat (95% interval) | Correct-answer NLL change, nat (95% interval) |
|---|---|---|
| 15 / query | -0.014063 [-0.032813, 0.007812] | 0.005648 [-0.007100, 0.015840] |
| 15 / first evidence end | -0.009375 [-0.031250, 0.010938] | 0.006041 [-0.003056, 0.015701] |
| 27 / query | -0.006250 [-0.050000, 0.034375] | 0.003125 [-0.017187, 0.025000] |
| 27 / first evidence end | 0.000000 [0.000000, 0.000000] | 0.000000 [0.000000, 0.000000] |

A negative correct-margin change moves toward the opposite donor answer. The zero at block 27's evidence end is also timing-limited: it replaces final-block output, followed only by positionwise normalization/scoring, with no later attention to mix that position into the query. It cannot test whether evidence was used earlier.

Only 4/160 original same-relation alternate-template donors match length/position exactly; those outputs remain explicitly confounded. The added control swaps two irrelevant facts and chooses the first exact length/all-hook match before scoring. All 80 qualify. This is an order rewrite, not a lexical paraphrase or equal-displacement control. Its mean query-margin changes are approximately 0/+0.001562 nat at blocks 15/27.

A complete vector also carries entities, answers and context; a replacement effect does not isolate one content. Correct/incorrect receiver groups avoid portraying changes to an incorrect prediction as evidence of a successful reasoning path. [Donor table](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E09/results.json) · [Original alignment](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E09/donor_alignment.json) · [Strict donor texts](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E09/strict_same_relation_donors.jsonl) · [Strict per-item controls](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E09/strict_same_relation_per_row.jsonl) · [64 stratified cells](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E09/stratified_CD_results.json)

## 9. Validity repairs and excluded measurements: E00 and E10

| Issue | Repair and retained record | Consequence |
|---|---|---|
| New platform metadata could not be parsed | An execution-local compatibility proxy filters an unknown field; failure preceded job creation | Same image/environment/Reserved profile; failed receipt retained |
| NumPy integer JSON serialization | Convert row IDs to built-in integers; preserve failed source/status | Computed but unsaved results are not fabricated |
| Cross-batch cached-state replay error 0.25 nat | Affected E08/E09 and dictionary behavior batches INVALID; recapture native states/scores in identical batches | Final selected no-ops all zero; original 0.005-nat score/0.01-nat margin bounds unchanged |
| AdamW oscillation, L-BFGS iteration cap | Keep both INVALID attempts; use Newton for the same objective/capacity | All candidates stationary; prior TEST exposure remains explicit |
| Repaired DEV selection changes layers | Replace 24/2 by 15/27; rerun dependent E09 only | Earlier layers are preserved, not averaged into final output |
| Same-relation donor misalignment | Preserve original controls; add exact fact-order controls | The added control has its stated scope, not complete content isolation |
| Overstrict FP32/FP64 arithmetic equality | Preserve failure; derive check bound from operands and machine precision | Primary independent difference 7.45e-10; no model tolerance changed |

The readout repair chain remains visible: initial AdamW oscillation and the bounded L-BFGS iteration cap invalidate those attempts. Final float64 Newton uses the objective’s curvature matrix and a line search to select a decreasing step. All 168 candidates and 56 selected heads satisfy the unchanged maximum-gradient-component bound 1e-5; the selected maximum is 8.67e-7. This tests optimization precision, not generalization.

Native references must belong to the intervention batch. For example, row 1408 has initial E02 margin −0.625000 and freshly obtained functional-phase native margin approximately −0.750000. E08/E09 subtract their own phase references; those absolute values are not interchangeable.

Initial native/read-hook error is zero against 0.02 nat; initial and final same-batch self-write errors are zero. Main-model trainable count is zero and complete before/after parameter hashes match. A separate 256×1,024 FP64 spectral-energy check has relative error 1.17e-16. [Append-only amendments](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/amendments.jsonl) · [Final no-op replay](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E00/functional_noop_replay.json) · [Independent arithmetic](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E10/independent_arithmetic.json)

## 10. Run boundary, coverage and unexecuted training

One experiment owns E00–E10. E00/E01/E10 are DONE_VALID and E02–E09 DONE_EXPLORATORY; the [coverage ledger](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/coverage.json) retains individual evidence/counts/gaps. F BLOCKED, SAE INVALID, duplicate intermediate labels and unqualified feature intervention remain visible. All registered layers, amplitudes and correct/incorrect items remain.

Only T1 probe and T2 statistical fitting ran. T3 new dictionaries, T4 controlled-exposure model training and T5 common/remaining updating did not. T4's complementary 4:1 three-atom combination allocations can match atom marginals, but a C1 combination is the atom itself, preventing independent manipulation of its combination count at fixed atom exposure. T5 lacks an operational split. Five protocols each have three audits; two numerical amendments add six, totaling 21 records.

Approved limits were two logical single-H100 Reserved workers, two hours each, four aggregate GPU hours, three-hour global wall and 20-GiB outputs. Five platform allocations served those workers with maximum concurrency two. Runtime totals 0.2989 GPUh; the conservative submission-through-completion bound is 0.6342, each worker below two hours. All jobs ended. These timestamps are not a bill. CPU supplements did not use the local GPU. [Job certificate](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/execution_certificate.json) · [21 fitting-audit records](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/protocols)

## 11. Trace an observation to its evidence

| Observation / object | Raw record and transformation | Verification path |
|---|---|---|
| 329/640, 611 No, four cells and interaction | [Raw logp](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E02/per_row.jsonl) → [Family statistics](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E02/results.json) | Join labels and two logp by row_id; within-family means, then four-cell difference |
| All-layer distances, spectra, CKA | [128 captures and logs](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/runs) → [Distances](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E03/layer_statistics.json) / [Spectra](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E04/spectra.json) / [CKA](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E06/results.json) | Same row/layer/position; TRAIN directions, TEST projections |
| Every readout and generalization result | [Head states](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E05/probe_states.pt) / [Predictions](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E05/test_predictions.npz) / [All candidates](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E05/optimization_all_candidates.json) | 1,025-parameter heads, TRAIN transform, DEV selection, per-TEST-row predictions and accepted-step logs |
| 105 projection and 12 donor conditions plus strict controls | [E08 per-item](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E08/per_row.jsonl) / [E09 per-item](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E09/per_row.jsonl) / [Joined real cases](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/case_traces.json) | Each phase's own same-batch reference; retain C/D and correctness groups |
| Assets, outputs and amendments | [Initial freeze](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/run_manifest.json) / [Artifact identities](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/artifact_manifest.json) / [Amendments](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/amendments.jsonl) | Hashes identify code/data/fitted states; some large arrays have path/size only |

Output asset family: `representation_context_relation_audit_v3_qwen06b_20261022`. Actual model/tokenizer/dictionary identities are in [Input identities](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E00/resolved_input_identity.json) · [Output asset](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/output_asset_manifest.json). Raw arrays, fitted heads, TensorBoard, job logs and figures stay execution-side and are located through manifests.

The editorial revision preserves the previous Summary as this experiment's appendix. Exact copies and SHA256 of all four prior records are in the [pre-revision archive manifest](/data/250010109/MoE_Router/research_record_archives/20261022_readability/A15_18_pre_readability_manifest.json). No Protocol, data, model, threshold or scientific state changed. After the researcher states observations, AI mechanism judgment may follow.
