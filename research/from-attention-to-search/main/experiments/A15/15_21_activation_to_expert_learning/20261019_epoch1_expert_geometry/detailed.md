# Detailed: epoch-one expert geometry and learning evidence

[Summary](summary.md) owns the reading result; [Protocol](protocol.md) owns the frozen analysis contract. Primary evidence and SVD/PCA are complete. Thirteen auxiliary CPU replacement conditions are numerically BOUNDED. Researcher mechanism judgment and next decision remain Unknown. No Focus, Anchor or original epoch-three result is changed.

## Identity and actual setup

Parent: Tulu answer SFT,10 conditions × seeds11/22. Upstream revision6248b175d2ccb5ec7c4aeb22e6d8ee3b21b2c752; TRAIN/DEV/EVAL are1,024/128/256 normalized-question-hash-separated dialogues,85,548/10,340/22,446 answer/EOS targets. Only the first user/assistant pair is retained; prompt≤256 tokens, answer including EOS8–256, total≤512, without answer truncation. Prompt/template/padding carry no target loss. Near-duplicate isolation and Base pretraining contamination are Unknown. EVAL is previously exposed, not a fresh confirmation set.

Original T/R11 lists and L964 stay fixed. T groups old-reference log frequencies; R11 is a fixed group-size-matched random organization. New TRAIN recalibrates p, m, group means and branch scale only. S0 uses original summed score; S1 group-mean calibration; S2/S3 retain the parent's extended scoring and floors. Learned uses trainable top1 dispatch; LearnedLB retains its load penalty. All20 selected checkpoints are epoch1,168 steps/85,548 targets. The parent's registered epoch3 endpoint remains504 steps/256,644 targets.

Base28 blocks,14-layer/F16384 CrossCoder and original final norm/head remain frozen. The branch is after the complete28th block and before final norm. For hidden h∈R^1024 and TRAIN RMS scale a, compute u=h/a and h_out=h+a*g*E_k(u). Fixed routing uses g=1; learned routing uses the selected softmax probability. Each bias-free SwiGLU expert has1024×1024 gate/up/down weights. Eight experts total25,165,824 trainable parameters; a learned router adds8,192. Gate/up initialize randomly and down at zero. Every expert receives full h; feature lists only choose dispatch.

This analysis reads existing epoch1 and matched actual epoch0 states. It creates no optimizer, trains nothing, changes no route and performs no new Base/CrossCoder extraction. Initial weights come from same-seed T_S0 epoch0 and matched initialization was checked. [Input checkpoint manifest](evidence/input_checkpoints.json) binds all20 paths and reached counters; each execution-side complete.json records freshly computed checkpoint SHA256.

Run: `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/epoch1_expert_geometry/20261019T030056Z`. Parent: `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/sft_route_learning/20261019T012300Z`.

## Freeze, conformance and deviations

|Contract|Actual evidence|Eligibility impact|
|---|---|---|
|Eligibility before spectra|preflight130/160; preliminary49 benefit labels before SVD|No spectral-shape selection|
|20 epoch-one states|All complete;168 steps/85,548 targets each|Primary matrix complete|
|No training or rerouting|No optimizer or input writes|Parent states retained|
|Full W0/W1/increment spectra|682 unique decompositions,1,024 values each,1,170 metric rows|Shared initialization and identical down increment reused|
|Common-coordinate rank16|Gate/up right; down left; response output directions|No arbitrary intermediate-neuron comparison|
|Native GPU replay|First256 saved EVAL NLL positions agree exactly in all20 models|Primary benefit arithmetic qualified|
|One CPU postprocessing failure|A one-expert model legitimately has no pair file; reader incorrectly assumed one|Old failure retained; repaired empty-file handling, CPU summary only rerun|
|Auxiliary cached CPU replacement|13 fail predeclared0.01 agreement floor;7 pass|13 BOUNDED; excluded from primary49 labels and fine specialization claims|

[Freeze](evidence/freeze.json) binds unchanged English/Chinese Protocols, config and parent loader. The [auxiliary amendment](amendment_probe_checks_cn.md) preceded its result inspection and did not alter primary rules. Epoch-one selection itself is post hoc; labels and comparisons are exploratory without multiplicity control.

## Metrics and dependence

Exposure requires≥2,048 actual unique TRAIN prediction positions,≥20 different dialogues,≥20 expert update steps and nonzero down change. Epoch one sees each position once. Fixed dispatch is reconstructed exactly. Learned-router historical dialogue diversity is bounded below using sorted TRAIN dialogue capacities and actual cumulative counts; endpoint routes do not replace training history. Historical learned-router source diversity is Unknown.

Benefit additionally requires≥200 natural EVAL positions from≥20 dialogues, negative endpoint natural-region TRAIN change, and negative EVAL change with a1,000-dialogue-bootstrap descriptive95% upper bound below zero. Zero branch is the comparator. Natural regions differ by expert/model, so their average NLLs cannot rank intrinsic expert ability. All failures, insufficiencies and zero exposures remain in the table.

Actual FP32 matrices are promoted to FP64 and decomposed with CUDA gesvd. q_j=σ_j²/Σσ_i²; stable rank=1/q1; effective rank=exp(−Σq_j logq_j). Full weights, initialization and increments are separate. Zero matrices have undefined normalized spectra and directions. Endpoint increments do not recover update trajectories.

Response PCA uses the same1,024 positions, four per EVAL dialogue, sampled with seed20261019. Responses are aE(h/a), excluding router g and shared h, centered along positions. Rank16 overlap is ||Q_a^T Q_b||_F²/16 for1024×16 orthonormal bases in a common coordinate system. First-direction absolute cosine, principal-angle cosines and the16/17 spectral gap are retained. Numerical rank<16 remains NA.16/1024 is a geometric reference, not a significance test.

Experts share data and training; pairs share endpoints. Experts, tokens, directions and pairs are not independent experimental replicates. Seeds are reported separately. Group curves average experts within seed then weight the two seeds equally, without artificial confidence bands.

## Evidence lineage and complete results

|Result|Raw evidence → computation|Aggregation|Boundary|
|---|---|---|---|
|130 exposure,49 benefit|Preflight + per-model expert evidence → expert_training_evidence.csv|All160; dialogue bootstrap|Primary usable, labels exploratory|
|Different output directions|Per-model saved responses/bases → within_model_similarity.csv|Same1,024 inputs, rank16|Geometry, not semantic function|
|Gate/up do not flatten|Saved spectra → paired_initial_changes.csv|Within-expert initial/epoch1; all130 and benefit49|FP64 numerical checks pass|
|Down post-training only|Saved spectra → matrix_summary_by_seed.csv|Within-model expert means|Zero initial normalized baseline is NA|
|Source NLL differences|Parent original GPU EVAL → epoch1_source_learning.csv|Token and dialogue averages separately|Dataset origins, not pure domains|
|Auxiliary replacements bounded|Saved responses → cached_probe_NLL.npz → probe_loss_checks.json|7PASS/13BOUNDED|Maximum discrepancy0.12491; no fine functional ranking|

|Condition|seed|Exposure-qualified|Benefit IDs|Zero-exposure IDs|
|---|---|---|---|---|
|T_S0|11|1|7|0,1,2,3,4,5,6|
|T_S0|22|1|7|0,1,2,3,4,5,6|
|T_S1|11|8|0,1,3|none|
|T_S1|22|8|1,3|none|
|T_S2|11|1|7|0,1,2,3,4,5|
|T_S2|22|1|7|0,1,2,3,4,5|
|T_S3|11|8|1,3|none|
|T_S3|22|8|1,3|none|
|R11_S0|11|8|0,4,6|none|
|R11_S0|22|8|0,4,6|none|
|R11_S1|11|8|0,4,6|none|
|R11_S1|22|8|4,6|none|
|R11_S2|11|8|0,1,4|none|
|R11_S2|22|8|0,1,4,6|none|
|R11_S3|11|8|4|none|
|R11_S3|22|8|0|none|
|Learned|11|8|1,3|none|
|Learned|22|6|2,4,6|none|
|LearnedLB|11|8|0,1,3,7|none|
|LearnedLB|22|8|1,2,3,4,5,6,7|none|

The [160-row expert table](tables/expert_training_evidence.csv) retains TRAIN changes, EVAL counts/intervals and labels. [Similarity summaries](tables/similarity_summary.csv), [4,350 pair rows](tables/within_model_similarity.csv) and [1,170 spectral rows](tables/parameter_spectral_metrics.csv) cover all130 exposed experts, not only49 selected winners. Summary reports decisive values and counterexamples.

## Numerical qualification and resources

Job pt-96wch7l2 reached platform SUCCEEDED on h100-4-reserved/shphd-lite-0911 using existing runtime. Coordinator active wall time153.238 seconds is not pure kernel time. CPU summarization/rendering took30.694 seconds; cached auxiliary CPU evaluation55.341 seconds with4 threads. No additional GPU or training job was submitted. Actual outputs:682 unique FP64 decompositions,130 response PCAs,4,350 pairs and1,170 metric rows.

Maximum relative reconstruction error on four fixed test vectors is1.07164e−14; top16 orthogonality error2.66454e−14; singular-energy identity error3.11894e−15. These qualify arithmetic, not scientific discovery. Primary natural EVAL replay matches saved GPU NLL exactly. [Runtime](evidence/runtime.json), [completion](evidence/completion.json) and [summary checks](evidence/summary.json) bind actual execution; per-model complete.json retains resource details and hashes.

Auxiliary CPU analysis restores the BF16 expert intermediate from cached responses, then applies original g/a multiplication order and one frozen head. Natural NLL differs from production GPU by up to0.124913; Base-only discrepancy is0.000566.13 models are BOUNDED and7PASS. BF16, batch shape and CPU operators are possible causes, not uniquely diagnosed. All auxiliary outputs remain saved; they do not determine49 benefit labels or overturn primary geometry. See [checks](evidence/probe_loss_checks.json) and [status](evidence/probe_loss_status.json).

## Figures, round record and inference

Thirteen figure sets are supplied as PNG/PDF/SVG. The Chinese [figure index](figures_cn.md) specifies data, axes, aggregation, result and claim limit; all primary panels were visually inspected. Full-EVAL source dispatch and NLL reuse parent GPU outputs, retaining both token/dialogue weighting and small-source support. Endpoint source dispatch is not learned-router training history.

This round asks which epoch-one experts received sufficient training and show heldout benefit, whether principal responses differ, and whether spectra flatten. It fixes the20 saved models, matched initial states and original routes. No training occurs and EVAL is exposed. The observed130/49 qualification, differing response directions and slightly more concentrated gate/up spectra quantify geometry but do not establish frequency routing's unique functional advantage. Down lacks a normalized initial comparator.

No physical prior or formal mechanism is adjudicated. Weight change or flat spectra cannot substitute for useful specialization. Shared data, initialization, exposure and routing multipliers remain credible explanations. Claims of convergence, semantic division, greater effective capacity, long-term isolation or general model benefit are unsupported.

Researcher mechanism judgment and next decision: Unknown. One AI suggestion is same-input replacement among beneficial experts after natural replay passes on a uniform GPU arithmetic path, to test whether content selectivity changes task loss. This follow-up is NOT_RUN; this analysis stops here.

## Artifact navigation

[Manifest](artifact_manifest.json) records selected repository evidence, source paths, hashes, roles and allowed claims. Arrays, checkpoints and full code/logs remain execution-side. `analysis_tulu_epoch1_expert_geometry_20261019t030056z` is distinct from `representation_tulu_epoch1_expert_pca_svd_20261019t030056z`; neither creates a new checkpoint or scientific approval.

Actual execution code/config paths and hashes are listed in the manifest. Reproduction navigation grants no automatic rerun approval. [Delivery receipt](completion_receipt.json) records final identity, input preservation and access checks.
