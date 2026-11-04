派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_25_02_learning_history_representation/20261023/detailed.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_25_02_learning_history_representation/20261023/detailed.md)；研究修改仍回到原件。

---

# A15_25_02_E01 Detailed: learning history and task-important directions

**Research question: How does learning history change conditional-rule representations, and which directions matter most for answering?**

The frozen analysis is complete: four states × 1,600 extracted examples and 253 intervention conditions × 816 evaluation examples. Rank-16 raw difference transfer yields old/new accuracy 80.882%/98.284%; equal-rank, equal-norm random controls average 0.123% old accuracy. Two CrossCoder half-attenuation contrasts have excess margin damage 1.130 and 1.427 logits, while every whole-dictionary reconstruction gate fails. These are local numerical comparisons; mechanism judgment and question closure remain with the researcher. [Summary](summary.md) · [Complete tables](evidence_tables.md)

| State dimension | Record |
|---|---|
| task_state | COMPLETE: requested analysis and factual delivery, including failed qualification |
| question_state | OPEN |
| design_state | EXECUTION_AUTHORIZED_V1; engineering repairs A1/A2 do not change science |
| result_state | EXPLORATORY; complete dictionary decomposition INELIGIBLE; residual-preserving direction effects BOUNDED |
| Researcher mechanism judgment / next decision | Unknown |

## Actual system, data and computation

Inputs are saved A17 R05 seed-29 states. The official Qwen3-0.6B Base safetensors hash is `cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba`. The CrossCoder Base path has the same freshly verified hash. Acquired A uses the 20261011 four-projection endpoint; sequential and mixed use R05 `A/seed_29/U` and `B/seed_29/Full`, both update_01200. [Protocol](protocol.md) and frozen config bind full paths and hashes.

Source training changed only the final attention Q/K/V/O matrices, 6,291,456 parameters. This analysis freezes all parameters and copies only those four tensors when switching saved states. Earlier 27 blocks, final-block MLP, global norm and output head are common. Changed attention gives the same frozen MLP different inputs; different final residuals do not imply MLP weight updates.

The old/reversed DEV subset contains 400 unordered-word groups / 1,600 rows. Group-hash splitting gives 196 discovery groups / 784 rows and 204 evaluation groups / 816 rows. Both modes and commands remain together; groups do not overlap. Both source panels, order_new and combination_new, occur in each split. DEV was already exposed, and templates/vocabulary are shared. Bootstrap units are word groups, not independent documents or training replicates. [Data guide](dataset_guide.md)

Each example contributes its final answer-prefix position from residual-post blocks 1,3,…,27 (zero-based), giving fourteen 1024-dimensional residuals. The model runs FP32; the fixed CrossCoder uses saved BF16 GEMMs, TRAIN mean/vector RMS and threshold to produce one shared 16,384-dimensional activation. No threshold/normalization refit or evaluation-batch TopK competition occurs. Precision relative to original dictionary training remains part of qualification, not an established cause of failure.

Margin is correct-token minus opposite-list-endpoint logit. Accuracy uses the full-vocabulary argmax. Correct-token NLL is in nats. Forced first/last choice is auxiliary and cannot replace full-vocabulary accuracy.

## Why these computations address the question

Paired geometry subtracts states for identical inputs. Cosine measures directional similarity; difference norm measures displacement. Neither alone measures task importance. Earlier measured layers have maximum paired difference zero; final mixed/sequential cosine averages 0.8562 and relative change norm 0.5041.

With the dictionary decomposition \(h=\mu+s(b+zD)+e\), edits use

\[
h'=h+s(z'-z)D.
\]

The actual reconstruction error is retained. This defines a finite directional intervention, not unique semantic parts; decoder directions are not orthogonal.

Discovery ranking uses positive first-order margin contribution. For RMSNorm, let \(q=(W_y-W_a)\odot w\) and \(r=\sqrt{\|h\|^2/d+\epsilon}\). Then

\[
M=\frac{q^\top h}{r},\qquad
\nabla_hM=\frac{q}{r}-\frac{h(q^\top h)}{d r^3}.
\]

Feature score is the discovery mean of \(\max(0,z_fsD_f^\top\nabla_hM)\). An autograd check validates the derivative with respect to input h; no parameter gradients are taken. Actual half/full attenuation tests finite effects. Evaluation does not reorder primary candidates.

Raw subspaces use uncentered SVD of discovery \(\Delta(x)=h_{mixed}(x)-h_{sequential}(x)\), at fixed ranks 1/4/16. Evaluation adds \(\Delta V_kV_k^\top\). The basis is fixed, but coefficients require each same-input donor. The complete recipient residual remains. This localizes a state difference; it is not a sixteen-dimensional standalone classifier or deployable model repair.

## Contract conformance and execution deviations

| Registered item | Actual | Eligibility |
|---|---|---|
| Four exact states and paired inputs | Four caches of 1,600 rows; hashes, parameter keys and saved steps pass | Conforming |
| Frozen model/dictionary | Zero trainable parameters and optimizer updates; tensor versions unchanged within computation stages | Conforming |
| Native/cached replay | First 20 rows/state: maximum logit error zero and equal predictions; all evaluation-head replay margin errors zero | Conforming; extra full native-forward comparison is first-batch only |
| No-op | Evaluation margin difference zero in all states | Conforming |
| Complete donor replacement | Maximum evaluation margin error 0.0000191, identical argmax | Below 0.001 gate |
| Dictionary qualification | Final FVE −1.0452, −0.8642, −0.8647, −0.9710; all FAIL | Complete decomposition ineligible; raw geometry and selective edits separately retained |
| Selection/evaluation separation | 196/204 nonoverlapping groups; candidates and random sets identical before/after repair | Conforming; prior DEV exposure remains |
| Three primary contrasts | 5,000 paired group bootstraps; 98.333% intervals all positive | Numerical local support, not fresh confirmation or human mechanism judgment |
| Controls/coverage | Eight random sets per primary set, 32 features; all 253 conditions complete | Conforming; nearest-neighbor feature matching is approximate |
| Perturbation magnitude | Equalized per example; primary candidate/control mean norm differences zero; no isotropic fallbacks | Rules out a merely larger edit |
| Resources | Sequential single-node one-H100 reserved attempts, same image and tuple | No resource substitution; within original compute ceiling |
| Engineering errors | One pre-create schema failure, then import and deterministic-cumsum failures | Retained and repaired without changing scientific choices |

Execution chain: first create failed before creating a job; `pt-d40a98vs` passed all extraction checks then FAILED at a same-named module import; `pt-5wd8maxg` selected discovery candidates then FAILED at strict-determinism CUDA cumsum; `pt-mpgpsupe` resumed only remaining analysis and **SUCCEEDED**. Final receipt is COMPLETE, all 253 conditions exist and cache hashes are unchanged. Extraction took 77.54 seconds; successful analysis resumption took 81.01 seconds. The failed resumption mostly spent time loading; it contributes no intervention result. [Amendments](amendments.md) record both fixes and the full strict-determinism engineering rerun. Original sources are retained under execution-side `source_versions/extraction_v1/` with the frozen hashes.

Observed torch is `2.3.0a0+6ddf5cf85e.nv24.04`, device NVIDIA H100 80GB HBM3. Peak allocated bytes were 5,307,836,928 for extraction and 4,668,407,296 for successful resumption. Existing exact model loader, residual hooks, threshold encoder and normalization are reused; selection, pairing and interventions are adapted. The old four-card launcher and Boolean task logic are not reused.

## Evidence lineage and unsupported interpretations

| Row | Question / rule | Raw artifact and computation | Observation and eligibility |
|---|---|---|---|
| L01 | Behavioral state differences | Cached native-head metrics → behavior.json, all DEV | Base 33.25/26.25%; A 100/0%; sequential 0/100%; mixed 99.625/99.75%. DONE_EXPLORATORY |
| L02 | Response to visible mode | 800 same-list/same-command mode pairs → behavior_factor_checks.json | A/sequential/mixed prediction change 0.125/0/99.625%. Behavioral, not internal mechanism |
| L03 | Location of representation changes | Paired raw residuals → geometry.json | Thirteen earlier measured layers exactly equal; final mixed/sequential cosine 0.8562. DONE_VALID description |
| L04 | Dictionary fidelity | Same head on reconstructed versus native h → qualification.json | Mixed accuracy 99.6875→56.75%; all FVE fail. Complete decomposition INELIGIBLE |
| L05 | Old-task candidates beyond random | Residual-preserving half attenuation; groupwise excess damage | 1.130 [1.037,1.228] logits. BOUNDED direction effect |
| L06 | New-task candidates beyond random | Same design on new examples | 1.427 [1.274,1.575] logits. BOUNDED direction effect |
| L07 | Low-rank recovery | Discovery rank16, evaluation transfer and eight equal-norm random subspaces | Excess margin improvement 17.808 [16.739,18.897]; old accuracy 80.882%, 95% CI 77.451–84.314%. DONE_EXPLORATORY |
| L08 | Influence versus sufficient transfer | Both 32-feature coefficient sets from mixed to sequential | Old accuracy remains 0%. Current candidate transfer is insufficient. DONE_EXPLORATORY |

L05–L07 primary intervals are 98.333%, distinct from the separately reported 95% accuracy interval. [Evidence tables](evidence_tables.md) retain every condition, candidate ID, spectrum and source hash. Weak conditions are not removed: rank1 carries 28.34% of difference energy but yields 0.245% old accuracy; rank4 gives 15.931%. The rank16 complement alone yields 12.010%, so useful changes are not entirely confined to those sixteen directions.

The two primary lists share 30/32 IDs and cause similar margin damage across tasks. They cannot be named separate A/B modules. Half attenuation of the 32 most frequent features does not lower accuracy, but that different feature-set intervention is not norm-equalized against the primary candidate sets; it is a descriptive counterexample, not another strict set-ranking test.

Feature matching is approximate: old candidate/control mean discovery occurrence is 0.7144/0.6647 and scaled decoder-row norm 742.28/688.90. New-set values are 0.7105/0.6625 and 752.39/705.78. Final perturbation norms are equalized per row, but original attributes are not identical. This limits feature-level interpretation without affecting the independent raw-subspace comparison.

## Three audits

**Scientific identification.** Finite interventions connect the question to its rival. Raw directions outperform equal-size random edits, weakening the claim that any equally large perturbation suffices. They may still carry concrete answer-word information rather than a mode-selection computation. Dictionary failure is separate from selective direction effects. Same-input cross-state transfer is not cross-task, vocabulary or dataset reuse. Parameter separation, MoE utility, long-term learning and curriculum-only causality are untested.

**Data/statistics.** File hashes, counts, group isolation, and mode/command balance are checked. Selection/SVD use discovery only; thresholds, counts, ranks and primary contrasts are not changed after evaluation. Random replicates are averaged within example before paired group aggregation. Bootstrap measures word-group variability, not seed variability. Shared templates and exposed DEV remain. Sample feature occurrence, controlled training exposure and unknown pretraining frequency are distinct.

**Implementation/numerics.** Inputs come from registered assets and no parameters are learned. Autograd only verifies the analytic input derivative; frozen model parameters have no `.grad`. Exact replay, same-shape no-op, full donor control, earlier-layer identity, finite values and version checks pass. Initial engineering smoke missed script-entry naming and strict determinism; both deviations are retained, and the final 253-condition smoke passes with the formal settings. Operator repairs do not change data or thresholds. An independent output audit verifies complete finite arrays, paired signs/means, set separation and cache hashes.

## Figures, examples and limits

All four measured PNGs were rendered and inspected for labels, scales, legends and clipping. Behavior uses all DEV; interventions use evaluation groups with margin-loss and accuracy axes and 95% group error bars. The feature heatmap scales each row separately; spectral energy is not task importance. Execution-side `full/figures/manifest.json` records exact sources, script and hashes. Selected copies have a [payload manifest](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_25_02_learning_history_representation/20261023/payload_manifest.json).

[Sample cards](sample_cards.md) retain all sixteen conditions from four predeclared lists and one post-hoc lexicographic failure illustration. For mode one, 乙, list 黄 龙 白, rank16 still predicts 黄 instead of 白. This failure example did not select directions.

Provisional AI interpretation: these fixed endpoints have a directional state difference that restores old answers more effectively than random edits. This does not identify a unique/minimal/universal direction set or reusable rules from frequent CrossCoder nodes. The researcher-owned next decision remains Unknown. The proposed next question separates mode conditions from answer-word identity before judging whether recovery persists.

## Coverage and artifacts

| Requested work | Coverage | Status | Evidence |
|---|---:|---|---|
| Independent bilingual Anchor/Protocol and fixed question | Four documents | DONE_VALID | A15_25_02 registration and frozen hashes |
| Four-state native behavior / factors | 4×1600 rows; 800 mode pairs/state | DONE_EXPLORATORY | L01–L02 |
| Paired fourteen-layer raw geometry | 4×1600×14×1024 | DONE_VALID description | L03 |
| Complete dictionary qualification | Four failures | INVALID for complete decomposition | L04; independent work completed |
| Feature occurrence, strength, co-occurrence and heatmap | All 16,384 statistics; twelve displayed rows | DONE_EXPLORATORY | feature_statistics / feature_display |
| Residual-preserving feature interventions | All registered sets/states/strengths/controls | DONE_EXPLORATORY / BOUNDED | L05–L06, L08 |
| Raw transfer, random controls and complement | Ranks1/4/16, eight controls/rank, whole and complement | DONE_EXPLORATORY | L07 |
| Figures, cards, tables, registration and local reading sync | Four figures, sixteen fixed cards plus one failure, 253 conditions | DONE_VALID delivery | [Artifact map](artifact_manifest.md) |

Asset `representation_a15_25_02_learning_history_20261023` registers the four actual caches and passes strict access checks. Payloads remain execution-side. Local generated reading copies preserve project scientific ownership and are not publication. No authorized analysis subtask remains unexecuted; failed dictionary qualification is a result boundary.
