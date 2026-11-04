派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_25_02_learning_history_representation/20261023/protocol.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_25_02_learning_history_representation/20261023/protocol.md)；研究修改仍回到原件。

---

# A15_25_02_E01 Protocol: learning history and task-important directions

**Research question: How does learning history change conditional-rule representations, and which directions matter most for answering?**

Revision v1, frozen before extraction on 2026-10-23. The researcher authorized completion of Anchor, Protocol, analysis and explanation in the current conversation, after fixing the four-state plan. Ordinary implementation and control choices are delegated. This authorizes frozen inference and representation edits only. It does not authorize model/dictionary training, new data collection, TEST access, publication or question closure.

## Purpose and exact comparison

The [Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_25_joint_feature_graph/subanchors/15_25_02_learning_history_representation_anchor.md) asks whether task-relevant changes can be distinguished from generic displacement. We compare Base, acquired A, A→B-only (`sequential`), and A→mixed A+B (`mixed`). A visible mode determines whether 甲/乙 selects the first/last list word or the reversed mapping. Same examples, model architecture, unchanged parameters, output head and tensor interfaces are paired across states. These saved endpoints differ in B exposure (24k versus 12k); they do not identify curriculum causality or joint learning from Base.

## Inputs and identity

Execution owner: `/data/250010109/MoE_Router/experiments/20261023_learning_history_representation`. Exact config: `config/frozen.json`; sample manifest: `data/examples.jsonl`. Only three-word lists and `old`/`reversed` worlds in the existing DEV split are read for inference. TEST is not read. The original manifest and train/dev hashes are checked; TRAIN metadata may establish counts but does not select inference examples.

| State | Weight source | SHA256 |
|---|---|---|
| base | `None` | `exact official Base; cd2a5120...` |
| A | `/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/full/attn1_adam/main/checkpoints/update_01200/state.pt` | `48595673c24579164e271cfeb1b86be6a234e2dfc06218b74d8ca07e16411b75` |
| sequential | `/data/250010109/MoE_Router/experiments/20261023_autonomous_retention/runs/A/seed_29/U/checkpoints/update_01200/state.pt` | `e3b12604b7f3f205b7e219a85f0c7826e9453caa6663b024ed4228798e7b82b1` |
| mixed | `/data/250010109/MoE_Router/experiments/20261023_autonomous_retention/runs/B/seed_29/Full/checkpoints/update_01200/state.pt` | `97473f54f80a96a16f5758527f010b6eea2d56c2ba6b7b05a25664865642b963` |

Each adapted state overwrites exactly `model.layers.27.self_attn.{q,k,v,o}_proj.weight` on the official Base. Native model computation stays FP32 as in A17. The fixed CrossCoder has 16,384 features, fourteen residual-post layers at zero-based blocks 1,3,...,27, saved TRAIN centering/vector RMS, saved inference threshold and BF16 computation. Its Base and the official A17 Base must have the same safetensors SHA256; actual equality is checked. Computation dtype differs from original CrossCoder training and is disclosed in qualification. No parameter gradient or optimizer exists.

Required registered assets (strict current access plus loader-level identity):
- `model_qwen3_0p6b_base_official_a5`
- `tokenizer_qwen3_0p6b_base_official_a5`
- `data_a17_conditional_mapping_v1`
- `adapter_a17_04_single_attention_20261011t145214z_full_attn1_adam_main`
- `checkpoint_family_a17_r05_20261023_a_seed_29_u_1d84de189a55`
- `checkpoint_family_a17_r05_20261023_b_seed_29_full_8de66cb62ec4`
- `crosscoder_qwen3_14layer_16384_bf16_a18_formal_14layer_batchtopk_a22_999997440_20261013`
- `model_qwen3_0p6b_base`

## Data split and independent unit

There are 1,600 rows in 400 unordered-word groups, each containing old/new worlds and both commands for one ordered list. SHA256 of `unordered_group_id`, interpreted as an integer modulo two, assigns even groups to discovery and odd groups to evaluation: 784/816 rows, 196/204 groups. All variants of a group remain together. No selection uses evaluation outcomes. DEV was already used by A17; every statistical result is exploratory exposed-DEV evidence, even with this analysis split.

## Stage 1: behavior and instrument qualification

Extract one position per row: the last input token, immediately before predicting the answer. Save all fourteen raw residuals and shared CrossCoder activations for every state. Measure full-vocabulary accuracy, first-versus-last forced choice, correct NLL in nats, correct-minus-opposite-endpoint logit margin and first/last/middle/remaining probability. Record answers for four deterministic evaluation list examples under all modes and commands.

Check native forward against residual replay (maximum margin error ≤0.001, full-vocabulary predictions agree); identical-input earlier selected layers across states (exact equality expected); zero edit and same-context transfer (exact logits); whole-vector transfer (donor logits reproduced within 0.001); finite tensors; fixed encoder threshold and weight immutability within extraction/intervention stages. Explicit state loading is the only parameter copy and is not learning. Log tensor-version guards separately around each state.

For each state/layer record centered variance explained, relative squared reconstruction error, raw-versus-reconstructed behavior, active-feature count and sample occurrence rate. Strong dictionary decomposition qualification requires final-layer centered variance explained ≥0.8 and absolute full-vocabulary accuracy change ≤0.05. A failed dictionary gate does not erase native behavior or raw geometry. Residual-preserving interventions remain measurements of named directions; they cannot establish that the dictionary captures the full mechanism.

## Stage 2: paired geometry and discovery selection

Report paired change norm relative to original norm, cosine similarity, unchanged-layer maximum difference, and singular spectra of final-residual mixed-minus-sequential changes. Keep descriptive occurrence, conditional strength and co-occurrence separate. Frequency is occurrence in these examples, not exposure during pretraining or a semantic label. A compact heatmap shows selected feature activation by state and task; high-frequency features are a descriptive comparison, not an importance definition.

Use the exact frozen head to calculate the gradient of correct-versus-alternative margin with respect to the final residual. Feature score is the discovery mean of the positive first-order contribution `z_f * scale * dot(decoder_f, gradient)`. Rank by descending score with feature ID as tie breaker. Select 32 features separately for acquired-A old examples, sequential new examples, mixed old examples and mixed new examples; also retain the mixed state's 32 highest-occurrence features. The mixed old/new sets are primary. First-order ranking only nominates candidates.

Fit SVD on discovery mixed-minus-sequential residual differences without centering away the mean change. Freeze ranks 1,4,16. This tests how much of the observed state difference these subspaces carry. Save candidate IDs, scores, matching diagnostics and bases before evaluating interventions.

## Stage 3: finite interventions and controls

For each candidate set and model state, attenuate feature activations by 0.5 and 1.0 while preserving the original reconstruction error: `h_edit = h + scale * (z_edit-z) @ D_last`. Evaluate both tasks, even when a feature set was selected on one. Do not modify other layers. For each primary set draw eight random feature sets, exclude all selected candidate IDs, and match discovery occurrence and decoder-row norm by nearest standardized log-frequency/log-norm distances (randomly select within the nearest twenty unused candidates). Use the same feature count. Rescale each example's random edit to the candidate edit's Euclidean norm. Record zero-support controls; a random zero edit with nonzero target norm receives a seeded isotropic direction and is explicitly counted as a fallback, never hidden as a matched feature result.

Transfer mixed-state candidate coefficients into sequential, acquired-A and Base recipients for identical inputs. Compare matched random feature transfers, zero/same-context transfer and complete donor-vector replacement. Full replacement is a positive implementation control, not evidence of sparse localization or cross-task reuse.

For raw geometry, transfer the observed mixed-minus-sequential difference projected onto discovery SVD ranks 1,4,16. Compare eight seeded random orthonormal subspaces of equal rank, with per-example perturbation norm equalized. Also evaluate the rank-16 complement and the complete difference. Projection is a state-difference localization intervention, not deletion of the recipient's entire subspace. No claim of universal most-important directions is permitted.

## Estimators and three primary decisions

All means are first aggregated within unordered-word group, then across groups. Primary comparisons are on evaluation only: (1) margin damage from mixed-old candidate half attenuation on old rows minus the eight-control mean; (2) the analogous mixed-new contrast on new rows; (3) old-task margin improvement from rank-16 mixed-to-sequential transfer minus the equalized random-subspace mean. Bootstrap the same 204 groups 5,000 times with seed 20261023; report 98.333% two-sided percentile intervals for the three primary contrasts. Strictly positive lower bound supports the local contrast; nonpositive upper bound weakens it; otherwise insufficient. This is a small fixed family of comparisons, not a search for the best evaluated rank/feature count.

All other attenuation strengths, recipients, sets, individual features, probabilities, co-occurrence and accuracy effects are descriptive with 95% group intervals where useful. A single training seed is not training replication. Do not select the winning rank after evaluation. Any later selection is post hoc and requires a separate label.

## Resources, reuse and stop rules

Use one single-node `h100-1-reserved` ACP allocation, image `shphd-lite-0911`, mounted CrossCoder runtime, maximum 3,600 seconds for the full analysis. This respects the researcher's one/two-card availability and supersedes the unrelated four-card default for this scope. Perform a bounded local MIG engineering smoke on discovery-only examples before submission. It checks numerics and interfaces, not the H100 full-node runtime. Use the repository submission template, dry run first, and record its receipt. The user requests completed analysis, so follow this job through completion; never duplicate a live job or switch resources automatically.

Reuse `carriers.QwenCarrier` for exact official FP32 loading, `FrozenQwenExtractor` for selected residual-post hooks, `data_routes.encode` for frozen thresholding and existing normalization/decoder classes. Adapt analysis-specific selection and interventions. Do not reuse the previous four-GPU launcher or Boolean task logic. A zero-edit, identity, nonfinite, changed-frozen-weight, missing-example or timeout failure stops the affected stage. Repair engineering errors within this frozen scope with an explicit attempt/deviation record; preserve failed outputs. No scientific gate is silently relaxed.

## Deliverables and audit

Save native/raw/feature cache, per-example intervention metrics, candidate selections, geometry, qualification, bootstrap results, complete receipt, code/config/data hashes and plots execution-side. Register reusable representation outputs. The canonical bilingual Summary explains purpose→models→observations→controlled edits→bounded answer. Detailed owns conformance, science/data/implementation audits, deviations and full evidence lineage. Figures are a sample-answer card, compact feature heatmap and intervention comparisons with uncertainty; original raw data and source scripts are linked. Synchronize exact Anchor/Protocol/Summary/Detailed reading copies locally using the existing builder. No commit or push is included.
