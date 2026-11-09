# Protocol: A15_17_E03 Attention-Sidecar Representation, Variance, And Local-Gradient Audit

## 0. Approval Snapshot

```text
Document status: APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL_EXECUTION
Approval status: HUMAN_CONFIRMED by the researcher's 2026-09-17 instruction
Block audit status: A-G CONFIRMED for this read-only measurement extension
Cross-block consistency: PASS
Execution scope approved: local implementation and tests; four-RTX5090 Spot Smoke; after Smoke PASS, one four-RTX5090 Spot full run supervised to terminal completion
Design frozen at: 2026-09-17 before GPU computation
Purpose: add the newly trained final-layer, layers-3+7, and all-eight-layer Attention-output SAE sidecar models to the existing representation audit, on the synthetic and M2D2 panels, with explicit variance and local-gradient trajectories
Primary Anchor: A15_17 three-model SAE representation trajectory
Experiment role: robustness check and measurement extension
Primary measurement: native final-block post-norm2 Fisher B/W/F and covariance-spectrum summaries at common 0, 0.5, 1, and 3B-token checkpoints
Gradient measurement: LM-loss versus local SAE-reconstruction gradient at the same raw Attention-output node, including norm, norm ratio, cosine, and angle
Treatment conditions: one layer-7 sidecar (S7), layers-3+7 sidecars (S37), and all-eight-layer sidecars (SALL)
Controls: existing M0 Dense, M1 bottleneck SAE, and M2 live-gradient bottleneck SAE caches for the same panels and checkpoints
Changed variable: sidecar placement/count and its resulting trained checkpoint state
Held fixed: model size, seed, tokenizer, DCLM training view, checkpoint token coordinate, P/N panels, row alignment, representation position rule, fit/report split, transforms, and plotting axes
Common checkpoints: 0, 0.5, 1, and 3B valid prediction tokens; no later unmatched point enters the comparison
Pass: all registered tasks and guards complete and the frozen tables/figures are reproducible
Fail: a Smoke guard or full-run implementation guard fails
Insufficient: any model/checkpoint identity, hook, data alignment, finite-value, immutability, or artifact-completeness guard fails
Cannot claim: causal long-run benefit, semantic feature identity, native model use of SAE reconstructions, routing or expert specialization, or that sidecar count alone caused an observed checkpoint difference
Resource profile: 5090-4-spot; image key shphd-lite-0911 plus the registered SM120 runtime layer; no fallback profile
```

The active Focus predates these three sidecar trajectories. The researcher explicitly activated this bounded extension in the current instruction without changing the Anchor's causal claim boundary. This Protocol therefore does not rewrite the completed E01/E02 result or the Focus-level scientific judgment.

## 1. Terminology And Definitions

- `P` is the frozen 360-row controlled synthetic panel, using its family-disjoint 120/60/180 fit/tune/report split and the last valid token.
- `N` is the frozen 1,200-row M2D2 academic panel, using 600/200/400 fit/tune/report rows and the mean over positions 0--255.
- `native final h` is the final block's post-`norm2` vector. It is on the native LM path for every model and is the common cross-model representation.
- `Attention output` is a hooked block's native return after `W_O` and before residual addition.
- `sidecar reconstruction` is the Top-32 SAE reconstruction of the hooked Attention output. It never enters the native LM forward path in S7/S37/SALL.
- `B`, `W`, and `F` are class-balanced between-class trace energy, within-class trace energy, and their ratio `F=B/W`.
- `B3` subtracts a fit-only mean and the fit-only first centered singular direction, then applies that frozen transform to tune/report rows.
- `participation ratio` is `(sum eigenvalues)^2 / sum(eigenvalues^2)` on the centered report covariance; it is a descriptive effective-dimension statistic.
- `local reconstruction gradient` is the gradient of one sidecar's own normalized reconstruction term at its own Attention-output node, including the training objective's `1 / number_of_sidecars` aggregation factor.
- `main LM gradient` is the normalized next-token cross-entropy gradient at the same node.

## 2. Anchor Alignment

The Anchor asks whether trained SAE configurations have different accessibility trajectories while warning that readability and geometry do not prove functional use. E03 extends the condition set from the earlier bottleneck models to sidecars that leave the native LM forward unchanged. This separates two observations: changes in the native final representation, and the local direction in which the auxiliary reconstruction objective pushes the hooked Attention output.

The strongest rival is that visually different trajectories arise from a dominant common direction, panel-specific lexical/domain structure, unmatched checkpoint endpoints, or an angle computed over positions where the reconstruction gradient is structurally zero. B3, two panels, common checkpoints, paired rows, and separate full-node/support-only gradient summaries address these rivals.

## 3. Tested Hypothesis

If Attention-output sidecar training changes accessible organization, at least one of S7/S37/SALL will show a coherent change relative to the common Dense reference in native final-h B/W/F or covariance-spectrum summaries over the registered checkpoints, and the direction will not be solely an unremoved first centered direction. If it does not, the bounded conclusion is that this audit did not detect such a native representation difference.

The gradient subquestion is descriptive: at each sidecar layer and checkpoint, measure whether the local reconstruction gradient is negligible, aligned, orthogonal, or opposed to the main LM gradient, and on what magnitude scale. No angle threshold is promoted into a causal success rule.

## 4. Rival Explanations

1. A single common direction creates the apparent variance or Fisher change. Guard: raw and B3 are reported separately.
2. A result is specific to constructed text or to natural academic text. Guard: P and N remain separate; neither rescues the other.
3. Gradient cosine is diluted by reconstruction zeros outside sampled positions. Guard: full-node and support-only results are both required.
4. A multi-sidecar gradient looks larger merely because terms were summed. Guard: each local reconstruction gradient carries the exact layer-mean factor used in training.
5. Different training ages create the comparison. Guard: only 0/0.5/1/3B common physical milestones are eligible.

## 5. Data Construction And Provenance

P is `/data/250010109/MoE_Router/experiments/20260914_semantic_feature_reuse_analysis/data/panel_frozen_v1.jsonl`. N is `/data/250010109/MoE_Router/experiments/20260914_sae_mediated_live_auxk/data/natural_panel_v1/natural_domain_panel.jsonl`. Their existing rows, labels, text/token content, splits, and IDs are reused without filtering or resampling. P uses tokenizer `/data/share/Qwen3-0.6B-Base`; N reuses its frozen 257-token prefixes. Labels enter only the read-only analysis.

The four N-fit gradient batches reuse E01's frozen class-balanced sample-ID manifest. For every row, 32 of 256 positions are selected by the existing deterministic sample-ID hash rule. No report label or report row enters gradient construction.

## 6. Learning Task And Permitted Supervision

There is no training task, optimizer, checkpoint selection, or parameter update. Forward caches use only inputs. Representation analyses use fit/tune labels to fit transforms and linear readouts, then score report rows. Gradient analyses use next-token targets and the model's self-reconstruction target; no class label enters either loss.

## 7. Model / Architecture And Frozen Variants

All new conditions are eight-layer hidden-1024 Qwen3-style Dense LMs with width-30,000 Top-32 SAEs on raw Attention outputs. S7 has one sidecar at block 7; S37 has sidecars at blocks 3 and 7; SALL has one at every block. Reconstruction is absent from the native LM forward. AuxK is SAE-only and must have zero gradient at the Attention-output node.

The controls M0/M1/M2 are the already-qualified E01 caches at matching checkpoints. Their common representation is E01 `h`, the final block post-`norm2` state. No old SAE-specific representation is equated with a sidecar reconstruction.

## 8. Training Objective And Optimization

Not applicable to execution: every checkpoint is frozen and no optimizer is constructed. For interpreting gradients only, the trained sidecar objective is `L_LM + mean_layer(L_rec) + (1/32) mean_layer(L_AuxK)`. The local-gradient audit differentiates `L_LM` and each layer's contribution to `mean_layer(L_rec)` at the same Attention-output node. AuxK's node gradient is checked as structurally absent.

## 9. Conditions, Seeds, And Checkpoints

| Condition | Hook layers | Checkpoints | Evidence role |
| --- | --- | --- | --- |
| M0 | none | 0, 0.5, 1, 3B | common Dense cache control |
| M1 | final bottleneck | 0, 0.5, 1, 3B | prior detached-reconstruction cache control |
| M2 | final bottleneck | 0, 0.5, 1, 3B | prior live-gradient cache control |
| S7 | 7 | 0, 0.5, 1, 3B | new final-layer Attention sidecar |
| S37 | 7, 3 | 0, 0.5, 1, 3B | new two-site sidecar |
| SALL | 7, 6, 5, 4, 3, 2, 1, 0 | 0, 0.5, 1, 3B | new all-layer sidecar |

All runs use seed 17 lineage. A physical complete manifest is required at every new-model point. The later S7 checkpoints and future S37/SALL checkpoints are outside this frozen matrix and cannot be added after results are visible.

## 10. Primary Metric And Frozen Analysis Plan

For native final h, compute B, W, and F on report rows for raw and B3 coordinates, separately for P and N. Fit-only mean/direction is frozen before report use. The unit of observation is one panel row; classes receive equal weight. Checkpoints are displayed on the x-axis in billions of valid prediction tokens.

This is an estimation audit rather than a thresholded method-selection trial. The scientific outputs are typed as `difference observed`, `no eligible difference detected`, or `insufficient`. A visual separation alone is not a verdict. Any later binary decision must be made in an updated Anchor or a separately approved intervention protocol.

## 11. Secondary Metrics And Guards

- Native final-h covariance eigenvalue share, top-1 share, top-10 share, and participation ratio.
- Frozen linear-probe balanced accuracy under raw and B3 coordinates.
- Per-sidecar-layer Attention-output and reconstruction B/W/F and covariance summaries.
- At 3B, covariance scree curves for all six native final states and for each sidecar's internal Attention/reconstruction surfaces.
- Four class-balanced gradient batches: LM norm, local reconstruction norm, reconstruction-to-LM norm ratio, cosine, and angle in degrees, for the full node and the 32-position SAE support.
- Finite values, exact hook-layer set, exact sample IDs, deterministic position mask, checkpoint-manifest integrity, and sampled state immutability.

No secondary metric can establish causal language-model use or semantic feature identity.

## 12. Known Good / Known Bad / Known Confusing Cases

- Known good: 0B backbones share the registered initialization lineage; native final-h collection must be finite and dimension 1024.
- Known bad: a missing hook layer, nonfinite metric, changed activity buffer, unmatched sample ID, or nonzero AuxK node gradient fails the affected task.
- Known confusing: cosine over the full node can be near zero because reconstruction is supported only on 32 positions. It must never be shown without the support-only cosine and norm ratio.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal | Input / operation | Expected output | Gate / named failure | Handoff |
| --- | --- | --- | --- | --- | --- |
| S0 | freeze identities | resolve all 12 new checkpoint manifests, panel hashes, old-cache root, source hashes | task manifest and provenance | missing or mismatched checkpoint/panel stops | immutable task list |
| S1 | local qualification | CPU schema/unit tests and dry-run submission resolution | local audit and exact command | test or profile mismatch stops | Smoke package |
| S2 | highest-risk Smoke | four independent short tasks on one 4x5090 node, including SALL 3B | finite caches/gradients, layer set, zero AuxK node gradient, peak memory | any guard fails; no full submission | Smoke receipt |
| S3 | full collection | 12 whole checkpoint tasks, statically assigned across four GPUs | caches, gradient JSON, completion hashes | no scientific-setting retry | complete evidence matrix |
| S4 | synthesis | merge new caches with qualified E01 controls | tables, figures, plot manifest | missing row/point/layer is insufficient | reader artifacts |
| S5 | eligibility audit | verify hashes, task count, axes, terminal receipt | eligibility JSON | incomplete lineage is insufficient | canonical result records |

## 14. Algorithm, Output, And Provenance Contract

Each checkpoint loads in a fresh process through its own frozen source tree. P stores native final h plus every sidecar layer's Attention output and SAE reconstruction at the last valid token. N stores native final h means over positions 0--255 and Attention/reconstruction means over the deterministic 32-position sidecar support. Gradients are never written as full tensors; only registered scalar contractions are saved.

Expected execution root: `/data/250010109/MoE_Router/experiments/20260917_sidecar_representation_gradient_audit/runs/`. Expected subtrees are `caches/`, `gradients/`, `completed/`, `tables/`, `figures/`, `stages/`, `task_specs/`, and a terminal receipt. Source checkpoints and prior E01 outputs are read-only. The run records resolved resource/image/runtime, exact command, source/config/panel/checkpoint hashes, peak memory, timing, and zero optimizer updates.

## 15. Success / Failure / Insufficient Evidence

- `PASS` means the requested measurement matrix and visualizations are complete and eligible; it does not mean the hypothesis is scientifically supported.
- `FAIL` means the implementation or Smoke cannot meet the frozen contract.
- `INSUFFICIENT` means execution finished but one or more evidence-eligibility guards failed or a registered cell is missing.
- `difference observed` requires the corresponding numeric table and plot; `no eligible difference detected` is allowed; `Unknown` remains valid.

## 16. What This Cannot Claim

The experiment cannot show that the LM uses SAE features, that a sidecar improves language modeling, that any SAE atom has a semantic identity, that multi-layer placement is better, or that the observed endpoint was caused only by sidecar count. It does not intervene on the native forward, train a router, or measure expert utility.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | State | Grounding |
| --- | --- | --- |
| A | CONFIRMED | current researcher request plus unchanged A15_17 claim boundary |
| B | CONFIRMED | researcher named synthetic and M2D2; exact frozen panels verified |
| C | CONFIRMED | read-only inputs and self-supervised gradients |
| D | CONFIRMED | current instruction plus verified S7/S37/SALL source/config/checkpoints |
| E | CONFIRMED | no update; gradient components reproduce the registered training objective |
| F | CONFIRMED | requested variance and gradient trajectories; prior E01 metric definitions reused |
| G | CONFIRMED | explicit four-RTX5090 Spot, Smoke, full execution, and completion instruction |

Cross-block audit: `PASS`. Data expose both controlled and natural domain structure; all models share row/checkpoint coordinates; native and sidecar-only surfaces remain distinct; gradient magnitudes and angles use the same node and exact training aggregation; no report label enters gradient computation; artifacts cover every registered condition.

Post-start scientific changes require an append-only amendment. Commit, push, publication, new training, checkpoint mutation, profile fallback, and later checkpoint expansion remain unauthorized.

## Appendix A01 — Scope Correction Before Any Evidence Was Produced (2026-09-17)

The researcher’s controlling instruction names one new model only: the model with a single raw-Attention-output SAE sidecar at the eighth transformer block (`S7`). The broader S7/S37/SALL matrix above was an AI scope error. Job `pt-hxlku819` was submitted against that broader Smoke matrix but produced no pod log, cache, gradient record, or visible result before entering `SUSPENDING`; none of its state is eligible evidence.

This human-confirmed amendment supersedes the execution matrix, while preserving the scientific question and claim boundary:

- treatment: `S7` only;
- control: the qualified E01 Dense `M0` caches at the same anatomical final pre-MLP state;
- common checkpoints: 0, 0.5, 1, 3, 5, and 10B cumulative valid prediction tokens;
- primary surfaces: native final pre-MLP state, raw block-8 Attention output, its sidecar reconstruction, its Top-32 contribution shares, and local LM-versus-reconstruction gradient geometry;
- transforms: raw, fit-only centering, removal of the uncentered fit-matrix first singular direction, and centering followed by removal of the centered first singular direction;
- required reader figures: topology, readability trajectories, paired Fisher/readability differences with paired intervals, fixed-atom contribution trajectories including 0B, usage/reconstruction and FVU, full-node and support-only gradient plots, raw and de-common Fisher trajectories, token-aligned training loss and auxiliary-loss curves, and jointly fitted PCA/UMAP/t-SNE descriptive views;
- output rule: PNG and SVG plus source tables, manifests, hashes, and terminal receipts in the isolated E03 run root;
- resource: one single-node `5090-4-spot` Smoke followed only after PASS by one single-node `5090-4-spot` full run; no fallback;
- execution remains read-only: zero optimizer updates, no checkpoint mutation, no training.

Because this correction was recorded before any eligible computation or visible metric existed, it does not select conditions in response to results. Blocks D, F, and G are amended to the values above and remain `CONFIRMED`; cross-block consistency remains `PASS`. The original broader matrix is historical only and must not be executed as E03 evidence.

## Appendix A02 — Offline Tokenizer Runtime Repair (2026-09-17)

Corrected S7 Smoke job `pt-aafi4o85` passed the four-RTX5090/SM120 preflight but its first collection task stopped before reading a panel because `transformers` was absent from the base image plus SM120-only layer. No cache, gradient record, or scientific metric was produced. The runner now sources the previously qualified Dense runtime script, which retains the same immutable PyTorch 2.8/CUDA 12.8 SM120 layer and additionally appends the mounted offline Transformers 4.53.3/tokenizer package. A local import check passed.

Before: source only the multi-site SM120 activation script.  
After: source the qualified Dense runtime, which activates the same SM120 layer for `5090-4-spot` and exposes the offline tokenizer dependency.  
Reason: the P panel requires the frozen Qwen tokenizer; the base image does not package `transformers`.  
Visible result at change time: GPU identity/preflight only; zero representation, gradient, loss-analysis, or plot result.  
Affected block: G engineering runtime only.  
Eligibility: `pt-aafi4o85` is an ineligible implementation failure; a fresh Smoke root/job is required. Scientific scope, panels, checkpoints, hooks, transforms, metrics, and verdict boundaries are unchanged.

## 18. Append-Only Amendments

### R001 — Isolated execution workspace after concurrent-write detection

```text
amendment time: 2026-09-17T10:05Z, before any GPU replica was allocated and before any scientific artifact existed
before execution root: /data/250010109/MoE_Router/experiments/20260917_sidecar_representation_gradient_audit/
after execution root: /data/250010109/MoE_Router/experiments/20260917_multimodel_sidecar_representation_gradient_audit/
reason: the first shared root was concurrently rewritten after submission into an S7-only scope and contained a syntax-invalid duplicate argument; allowing the queued pod to start would not execute this Protocol
first job: pt-hxlku819, stopped while STARTING with zero allocated replicas
visible data before amendment: none; no pod log, cache, gradient, metric, optimizer update, or scientific result
implementation identity clarification: SALL's checkpoint-native ModuleDict order is [7, 3, 0, 1, 2, 4, 5, 6]; this is the same registered all-blocks-0--7 set and the objective remains the unweighted mean over eight layers
affected block: G artifact root and exact source snapshot only
unchanged: models, panels, 0/0.5/1/3B checkpoints, representations, gradient definitions, metrics, figures, resource profile, image, Smoke gate, full-run scope, and claim boundary
approval: safety-preserving operational repair within the explicitly approved execution scope
eligibility impact: pt-hxlku819 is scheduling/failure-ledger evidence only and certifies no Smoke or scientific result; all eligible evidence must originate in the isolated after-root
```

### R002 — First-job stop race observation

```text
amendment time: 2026-09-17T10:09Z
earlier observation: the stop request was accepted while pt-hxlku819 reported STARTING with zero replicas
later observation: ACP briefly reported SUSPENDING with one replica and a durable pod log containing only the environment line and BLACKWELL_RUNTIME_PASS
scientific work reached: none; no task spec was executed and no cache, gradient, metric, stage PASS, or terminal scientific receipt exists
eligibility impact: unchanged; pt-hxlku819 remains ineligible operational evidence only
```

### R003 — Registered offline tokenizer dependency activation

```text
amendment time: 2026-09-17T10:15Z, after the isolated Smoke reached model loading but before any cache or gradient artifact
before: activate the registered SM120 PyTorch layer only
after: activate the same SM120 layer and append /data/250010109/dependency_packages/hf_transformers_qwen3 to PYTHONPATH with offline Transformers flags
reason: the image plus SM120 layer does not expose transformers by default; tokenizer import failed after checkpoint load
visible data before amendment: hardware preflight and ModuleNotFoundError only; no representation, gradient, metric, optimizer update, or scientific result
affected block: G runtime dependency activation only
unchanged: source, checkpoint, tokenizer identity, panels, task matrix, numerical computation, metrics, resource/image tuple, and claim boundary
approval: engineering repair within the approved implementation/Smoke scope
eligibility impact: pt-08dxw4r6 is ineligible Smoke-failure evidence; a fresh run root is required
```

### R004 — Synthetic split-name normalization in CPU synthesis

```text
amendment time: 2026-09-17T10:40Z, after all 12 GPU collection tasks passed and before any result table or figure was produced
before: analysis expected literal P split labels fit/tune/report
after: map the frozen file's literal labels fit/development/confirmation to the already registered semantic roles fit/tune/report
reason: the frozen panel physically stores development and confirmation even though the predecessor protocol and this Protocol describe their roles as tune and report
visible data before amendment: all read-only caches and gradients were complete; CPU analysis stopped on an empty report mask before computing or writing any result table, figure, or interpretation
affected block: F/G implementation vocabulary only
unchanged: row membership, labels, split sizes 120/60/180, fitting boundary, report boundary, metrics, checkpoints, gradients, and claim boundary
approval: identity-preserving repair to match the verified frozen source
eligibility impact: pt-yuifv33t certifies the complete 12-task GPU collection but its combined terminal receipt is FAIL because S4 stopped; S4-S5 must run afresh from the hashed complete caches and write a separate synthesis receipt
```

### R005 — Concurrent S7-only appendix provenance and endpoint clarification

```text
recorded at: 2026-09-17T10:54:45Z; authority and filesystem reconciliation only, after results; no metric or selection rule changed
current controlling instruction: include the newly trained multi-site models and the final-layer-only sidecar model in one same-evaluation-point audit
eligible E03 matrix: S7, S37, and SALL at the physical intersection 0/0.5/1/3B, as frozen in Sections 2, 9, and 12 and executed from the isolated multimodel workspace
concurrent text: Appendix A01 and Appendix A02 came from the separate S7-only shared-root workflow identified by R001; retain them as provenance of the collision, but they do not supersede the current multimodel matrix and their jobs/artifacts are not E03 evidence
endpoint audit: the S7 source has physical milestones through 10B, while S37 and SALL have physical milestones through 3B; none of these three source trees has a 15B milestone at the execution freeze
15B eligibility: absent from the common physical intersection and therefore not silently substituted, interpolated, or mixed into the registered comparison
evidence used to resolve this note: current researcher instruction, physical source manifests, isolated task manifest, completion records, and R001
scientific impact: none; this amendment makes the already executed authority and endpoint boundary explicit
```
