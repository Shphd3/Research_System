# Protocol: A15_17_E01 Three-Model SAE Representation Audit

## 0. Approval Snapshot

```text
Document status: APPROVED_FOR_IMPLEMENTATION_AND_FULL_EXECUTION
Approval status: HUMAN_CONFIRMED on 2026-09-15
Execution scope approved: local audit, implementation, S2 correctness qualification, full S3-S6 collection/analysis, figures, and execution records
Resource profile: one single-node h100-4-reserved job, four independent GPU workers (current after R003)
Image: shphd-lite-0911 and its qualified H100 runtime
No ETA scale gate: S2 failure stops; an S2 pass proceeds through the full registered scope regardless of estimate
Purpose: compare representation evolution of existing M0/M1/M2 checkpoints
Primary evidence: domain readability and coarse/fine geometry on paired report samples
Mandatory sensitivity: fit-only removal of the first singular direction, both uncentered and center-then-remove forms
Cannot claim: causal model use, Router use, expert utility, downstream LM gain, or cross-model atom identity
```

Active Focus: [focus_three_model_sae_representation_audit.md](../../../../focus/legacy/0915_focus_three_model_sae_representation_audit.md)  
Primary Anchor: [A15_17 Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/15_17_three_model_sae_representation_trajectory_anchor.md)  
Machine-readable freeze: [0915_three_model_analysis_spec_v1.json](../../../../research_notes/sae_representation/20260915/analysis_plan1/0915_three_model_analysis_spec_v1.json)

## 1. Purpose, Hypothesis, Analysis Method, And Outcome Branches

**Purpose.** Determine which accessible structures differ across M0 Dense, M1 detached-reconstruction SAE, and M2 live-reconstruction plus SAE-only AuxK at the same six training-token checkpoints, and whether any difference remains after removing the dominant common direction.

**Hypothesis.** An SAE-mediated training difference that changes residual domain organization should form a coherent paired trajectory in raw \(h\) or actual MLP input and survive at least one mandatory first-direction removal. The strongest rival is a lexical, reconstruction, probe, mean, or dominant-direction artifact.

**Analysis method.** Extract frozen final-block post-`norm2` \(h\), actual final-MLP input, and M1/M2 Top-k activations from P and N. Measure linear readability, cosine relation margins, Fisher ratios, sparse overlap, reconstruction health, and four fixed local-gradient batches. Keep Part A raw. In independent Part B, fit and apply B1 center-only, B2 remove the uncentered first right-singular direction, and B3 center then remove the centered first right-singular direction. Compare models with paired 5,000-draw stratified bootstrap intervals.

**Outcome branches.** Supporting evidence requires an eligible, coherent paired contrast that survives B2 or B3; non-supporting evidence includes unresolved contrasts or a raw pattern removed/reversed by both; any failed identity, split, hook, finite-value, convergence, transformation, immutability, uncertainty, or artifact guard yields `INSUFFICIENT` for the affected claim.

## 2. Frozen Inputs And Model Identities

The exact 18 checkpoint paths, manifest hashes, source-config hashes, panel paths, panel hashes, and task order are frozen in the machine-readable spec. The checkpoints are 0, 0.5, 1, 3, 5, and 10B tokens for each model.

- M0: Dense baseline; final MLP receives \(h\).
- M1: final SAE reconstruction is the MLP input; the reconstruction source is detached from the backbone; no AuxK objective.
- M2: final SAE reconstruction is the MLP input with live backbone gradient; AuxK acts on SAE parameters through its detached target path.

Every task loads with strict state identity in a fresh Python process. One checkpoint is one indivisible resume unit. All P and N representation shards are regenerated; historical caches are inventory evidence only.

## 3. Data, Splits, And Pooling

P is the frozen 360-sentence panel: 120 fit, 60 tune, and 180 report sentences, split by 72 independent families as 24/12/36. Text is read with the registered trailing newline and pooled at the last valid token. Domain readability is primary; the 144 frozen fact triplets are a secondary proposition-reuse diagnostic.

N is the academic M2D2 1,200-row panel with eight fine classes under four coarse parents. Per fine class, the hash-ordered first 75 original-fit rows are fit, the next 25 tune, and 50 original-development rows report. Inputs are token positions 0--255; targets are positions 1--256. Mean position 0--255 is primary and position 255 is secondary. N is development replication, not untouched confirmation.

## 4. Representations And Mandatory Common-Direction Removal

Hooks collect the output of the final block's `norm2` as raw \(h\) and require the gate and up projections to receive identical inputs. For M1/M2 that actual input must equal the exported mediated reconstruction. Sparse values must be nonnegative, within width, and use no more than the registered Top-k.

Part A remains the original uncentered representation. Part B is separate and fit-only:

| ID | Operation | Fit object | Required reading |
|---|---|---|---|
| B1 | subtract fit mean | fit rows only | isolates centering; never substitutes for B2 |
| B2 | remove first right singular direction | uncentered fit matrix | teacher-required common-representation removal |
| B3 | center, then remove first right singular direction | centered fit matrix | distinguishes mean from leading centered variation |

Each transform stores the fitted mean, direction, singular values, removed energy fraction, and first/second relative gap. The raw-selected probe \(C\) is reused and the probe is refit after projection. Part B applies only to dense P-last and N-mean representations.

## 5. Probe, Geometry, Sparse, And Gradient Contracts

Linear probes use seed 17, L2 logistic regression, `lbfgs`, tolerance \(10^{-4}\), maximum 2,500 iterations, and \(C\in\{0.001,0.01,0.1,1\}\). Fit rows train, tune rows select maximum balanced accuracy with smallest-\(C\) tie break, and report rows are opened once. Non-convergence makes that fitted cell ineligible. Dense scaling centers fit rows; sparse scaling uses `with_mean=False`. Per-sample labels, predictions, and class probabilities are saved for raw, B1/B2/B3, sparse, fixed \(h\)-probe-to-actual transfer, N-last, and TF-IDF controls.

Cosine margins use frozen positive/rival triplets and aggregate at the independent family or row unit. Fisher trace uses class-balanced between/within energy. All M1−M0, M2−M1, and M2−M0 comparisons reuse identical report units and stratum-preserving bootstrap draws. Intervals are pointwise descriptive, not an any-checkpoint significance claim.

M1/M2 sparse contribution shares use \(z_j\lVert d_j\rVert_2\) normalized within token. Report set overlap, weighted overlap, FVU, effective L0, and feature coverage are retained. Atom IDs are not aligned across models or independently trained checkpoints.

Four deterministic N-fit gradient batches contain one row per fine class and eight rows total. Each checkpoint records FP32 raw and objective-weighted gradient norms, RMS, weighted-to-LM ratios, and pairwise cosines by disjoint parameter group. LM, reconstruction, and AuxK denominators are 2,048, 256, and 256 tokens per eight-row batch. There are zero optimizer and buffer updates.

## 6. Figures And Reusable Artifacts

Required reader figures are A01--A09 and B01--B04. A09 contains separate PCA, UMAP, and t-SNE 3×6 model/checkpoint evolution grids and must include 0B. A06 contains M1/M2 atom-activation evolution across all six checkpoints including 0B, with independently selected columns declared in the title. B04 is one inspectable M2-10B N example comparing raw, B2, and B3; it cannot replace the registered metrics.

Reusable evidence includes all 18 verified representation shards, fit-only transforms, per-sample predictions, paired metric tables, 5,000-draw rules, gradient tables, and embedding coordinates. Failed attempts remain under `runs/full_h100_v2/`, `runs/full_h100_reserved_v1/`, `runs/full_h100_reserved_v2/`, and `runs/full_h100_reserved_v3/`; current raw execution material belongs under `/data/250010109/MoE_Router/experiments/20260915_three_model_representation_audit/runs/full_h100_reserved_v4/`. The eventual date-local reading copies belong under `daily_research_reports/0915/figures/` only after eligible results exist.

## 7. Stages, Stop Rules, And Restart

| Stage | Operation | Pass condition | Stop rule |
|---|---|---|---|
| S0/S1 | source/data/task audit and CPU tests | exact hashes/splits, 18 tasks, transform/probe tests pass | any mismatch stops submission |
| S2 | 0B/10B bounded qualification for all models | four visible SM90 H100 GPUs, strict load, hook, finite values, state unchanged, one gradient batch where required | any failure stops S3 |
| S3 | full collection and four gradient batches for 18 tasks | 18 atomic completion records and content hashes | failed task stops analysis; verified tasks resume |
| S4 | Part A raw analysis | all registered tables/predictions | no substitution from Part B |
| S5 | mandatory B1/B2/B3 | transform registry, predictions, B01--B04 | missing B2 or B3 makes common-direction question insufficient |
| S6 | paired synthesis and all figures | analysis receipt and required artifact list pass | missing artifact prevents result claim |

A restart may skip only a completed unit whose content hash matches its completion record. It may not drop a model, checkpoint, panel, B transform, bootstrap count, or figure. ETA is reported after startup observation but cannot shrink this approved scope.

## 8. Execution Tuple And Reproducibility

Resolve the current `h100-4-reserved` and `shphd-lite-0911` from `docs/execution_envelope.md` through `templates/execution/acp_submit_template.sh`. The current exact tuple is one node in `share-cluster`, worker spec `n6ls.iu.i40.4`, four H100 80GB GPUs, Reserved quota, and the registered `/data` mount. Four independent workers receive 5/5/4/4 whole-checkpoint tasks by `task_index % 4`; no DDP or gradient synchronization is used.

The Dense baseline H100 runtime uses the qualified current-image path. UMAP 0.5.6 and pynndescent 0.5.13 live in an execution-local dependency directory with recorded metadata hashes; the base image is not modified.

**Resource amendment R001 (2026-09-15, before either attempt started computation).** The researcher first selected `5090-4-spot`, then observed competing eight-RTX5090 use, ordered the pending job stopped, and explicitly returned this unchanged full protocol to `h100-2-spot`. Job `pt-7yis2se8` never received a host and is cancellation evidence only. R001 changes resource topology and task assignment from 5/5/4/4 to 9/9; it changes no model, checkpoint, sample, transform, metric, figure, bootstrap, stop rule, or claim boundary.

**Execution clarification R002 (2026-09-15T17:28Z, before H100 allocation).** Two stale textual references left by R001 were corrected: the result root is `runs/full_h100_v2`, not `runs/full_v1`, and S2 requires two SM90 H100 GPUs, not four SM120 GPUs. The submitted command and implementation already used the H100 values. This clarification changes no scientific object, analysis rule, artifact requirement, or eligibility criterion.

**Resource and failure-repair amendment R003 (2026-09-16, after failed S2 and before the reserved rerun).** Before: job `pt-20q3i7pd` used `h100-2-spot`, worker spec `n6ls.iu.i40.2`, two workers with 9/9 assignment, and run root `runs/full_h100_v2`. Actual failure: the job reached S2, passed the source audit and 13 CPU tests, exposed two H100 GPUs, then failed before any of the six qualification units completed because an advisory checkpoint-load lock was placed on AFS and `fcntl.flock` returned `EAGAIN`; no representation, gradient, metric, or figure result was visible. After: the researcher explicitly selected `h100-4-reserved`, worker spec `n6ls.iu.i40.4`, four workers with 5/5/4/4 whole-task assignment, and fresh run root `runs/full_h100_reserved_v1`. The engineering repair moves only the same-node serialization lock to container-local `/tmp`; checkpoint bytes and all scientific computations remain on registered storage. This changes resource topology, scheduling, and engineering synchronization only; it changes no model, checkpoint, data split, hook, transform, metric, uncertainty rule, artifact requirement, stop rule, or claim boundary. The failed attempt is `INELIGIBLE` for scientific claims; the fresh reserved run remains eligible if all S2--S6 guards pass. Approval: researcher instruction on 2026-09-16 to use four H100 Reserved and run immediately.

**Qualification hash repair R004 (2026-09-16, after failed reserved S2 and before its fresh rerun).** Job `pt-xsmaub14` verified four H100s, the repaired node-local lock, both M0 qualification tasks, and the M0 10B gradient path, but failed S2 before M1/M2 forward execution. The state digest attempted to reinterpret a zero-dimensional Long buffer directly as bytes; PyTorch requires flattening before a different-element-size view. Before: `tensor.contiguous().view(torch.uint8)`. After: `tensor.contiguous().reshape(-1).view(torch.uint8)` in both qualification and full collection. A new unit test covers a scalar Long buffer and bfloat16 tensor, and all 15 tests pass. Run root changes from `runs/full_h100_reserved_v1` to fresh `runs/full_h100_reserved_v2`; no v1 qualification artifact is reused. This is an implementation-eligibility repair only and changes no tensor bytes, state membership, model, checkpoint, data, metric, transform, bootstrap, artifact requirement, or claim boundary. The v1 attempt is `INELIGIBLE` for scientific claims.

**Read-only NumPy export repair R005 (2026-09-16, after v2 S3 failure and before fresh v3).** Job `pt-i2ofctjz` passed all six S2 qualification tasks and entered S3. Two M0 full shards completed, while M1/M2 workers failed at the first sparse activation export because the newly computed SAE value tensor still required grad when converted to NumPy. Before: sparse/dense exports called `.cpu().numpy()` directly after read-only collection. After: SAE encode is explicitly inside `torch.inference_mode()`, and every collector PyTorch-to-NumPy boundary goes through `tensor.detach().cpu().numpy()`. A regression test exports a `requires_grad=True` tensor, and all 16 tests pass. Run root changes from `runs/full_h100_reserved_v2` to fresh `runs/full_h100_reserved_v3`; no v2 qualification or shard artifact is reused. This changes graph retention and export eligibility only; it changes no numerical forward definition, model state, checkpoint, sample, transform, metric, bootstrap, figure, or claim boundary. The v2 attempt is `INELIGIBLE` for scientific claims despite its eligible engineering S2 evidence.

**Inactive-AuxK gradient repair R006 (2026-09-16, after v3 S3 failure and before fresh v4).** Job `pt-ix1stwdr` passed all six S2 tasks and began S3, but M2 0B stopped at the registered gradient decomposition: its frozen dead-feature mask is empty, so the model correctly returns a constant zero AuxK loss without a `grad_fn`, while the collector incorrectly called autograd on every listed component. Before: every LM, reconstruction, and AuxK scalar was forced through `torch.autograd.grad`. After: a component with `requires_grad=False` is recorded as structurally inactive with exact zero gradients and an `active_examples` count of zero; any active scalar still uses autograd with the previous failure visibility. A regression test distinguishes the inactive constant-zero branch from an active differentiable loss, and all 17 tests pass. The doomed v3 job was stopped after the durable failure was captured. Run root changes to fresh `runs/full_h100_reserved_v4`; no v3 qualification or shard artifact is reused. This changes only the representation of a mathematically absent AuxK term and changes no objective value, parameter group, model, checkpoint, sample, transform, metric, bootstrap, figure, or claim boundary. The v3 attempt is `INELIGIBLE` for scientific claims.

## 9. Completion And Claim Boundary

Completion requires S0--S6 receipts, 18 cache and gradient completion records, state-identity evidence, all raw and B tables/predictions, 5,000-draw uncertainty, A01--A09, B01--B04, and no optimizer or buffer update. A completed job does not itself select a scientific branch; the result Summary and Detailed record will be written only from eligible evidence.

The strongest admissible result is about frozen representation accessibility, residual geometry after common-direction removal, sparse usage, and local objective gradients. It cannot establish that the language model uses the readout, that one model is generally better, that atom IDs correspond across models, or that a causal functional intervention will work.
