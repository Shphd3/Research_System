# Protocol: A15_13_E16 DCLM Final-Layer Top-K SAE Smoke

## 0. Approval Snapshot

- Document status: `APPROVED_FOR_FULL_RUN`
- Approval status: human approved the fixed 1B-token full run on `H100-4-reserved` on 2026-09-03; hierarchy construction remains unauthorized.
- Block audit status: A--G `CONFIRMED`
- Cross-block consistency: `PASS`
- Execution scope approved: completed smoke plus implementation and execution of Amendment F01's single 1B-token four-H100 reserved full run.
- Design frozen at: 2026-09-03 before ACP submission.
- Problem key: `A15.sae_hierarchical_teacher_construction`
- Conversation owner: `codex-thread:01a06773-49c8-7e32-b504-00f3e5ddaad0`
- Confirmed Focus: [focus_sae_hierarchical_teacher_construction.md](../../../../focus/focus_sae_hierarchical_teacher_construction.md)
- Purpose: qualify the exact final-layer SAE trainer and obtain measured throughput for the later full-run decision.
- Primary Anchor: [A15_13_06](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_06_dclm_final_layer_topk_sae_teacher_anchor.md)
- Anchor decision question: does the registered SAE pipeline pass every engineering gate required before full DCLM training?
- Experiment role: method construction and smoke qualification.
- Primary metric: held-out normalized reconstruction mean squared error before versus after training, with zero reconstruction equal to one.
- Minimal setup: frozen Qwen3-0.6B-Base, final layer-27 MLP pre-hook states, frozen DCLM training and validation binary files, 30,000 SAE features, Top-32 activation, 100 optimizer updates.
- Treatment and controls: trained SAE versus its initialization; zero reconstruction reference; save/reload identity control.
- Changed variable: 100 SAE optimizer updates.
- Held fixed: model, layer, activation site, DCLM files, SAE width and sparsity, seed, validation samples, and gate definitions.
- Pass: every smoke gate in Section 15 is true.
- Fail: at least one verified smoke gate is false.
- Insufficient: execution or provenance artifacts are missing or unauditable.
- Cannot claim: feature semantics, hierarchical structure, Router usability, expert utility, layer placement, or language-model gain.
- Approval decision: run one smoke only; do not start full SAE training automatically.

## 1. Terminology / Definitions

The sparse autoencoder (SAE) reconstructs a 1,024-dimensional model state from a 30,000-feature dictionary. Top-32 means that at most 32 positive encoder activations remain for each token. The router-input state is the tensor passed into the target decoder layer's MLP, captured by a forward pre-hook. Normalized reconstruction error divides reconstruction mean squared error by the target state's mean squared magnitude; zero reconstruction therefore scores one. A smoke is an engineering eligibility test and supplies no semantic conclusion.

## 2. Anchor Alignment

The parent evidence shows that correct coarse--fine expert paths have task value but current final-window clustering does not transfer reliably to an online causal Router. This experiment tests only the prerequisite that the senior-style SAE object can be trained reproducibly on the intended final-layer tensor. It leaves the gold-label layerwise audit and all semantic, routing, expert, and task claims untouched.

## 3. Tested Hypothesis

After 100 updates, held-out normalized reconstruction error will be finite, below one, and below its pre-training value while the base remains frozen, feature use does not collapse to 32 or fewer dictionary entries, and a saved checkpoint reproduces identical output after reload.

## 4. Rival Explanations

The apparent training signal may come from a wrong activation hook, incompatible DCLM tokens, hidden base-model updates, non-finite optimization, a collapsed dictionary, validation reuse, or a checkpoint that cannot reproduce the model. Each rival has an explicit gate.

## 5. Data Construction And Provenance

- Training population: the existing DCLM binary corpus view at `/data/250010109/training_data_views/dclm_pair_v1/train/`.
- Smoke training file: `global-shard_01_of_10/local-shard_0_of_10_shard_00000000_processed.bin`, uint32 Qwen3 token IDs.
- Validation file: `/data/250010109/training_data_views/dclm_pair_v1/validation/validation.bin`, a symlink to the separately registered validation shard.
- Example unit: one contiguous 1,024-token window.
- Sampling: deterministic rank-disjoint windows keyed by seed 17 and optimizer step.
- Norm filtering: remove the largest 0.1% of token-state L2 norms within each process batch and record the realized rate. This follows the Qwen-Scope stability principle; it is not a semantic filter.
- Forbidden information: M2D2 labels, task names, domain names, future validation statistics, or any semantic truth.

## 6. Learning Task And Permitted Supervision

Input is the frozen final-layer MLP pre-hook state for one DCLM token. Output is a reconstruction of the same state. The only supervision is the state itself. Validation states do not contribute gradients or checkpoint selection in the smoke; they are evaluated before and after the fixed 100 updates.

## 7. Model / Architecture And Frozen Variants

- Base: `/data/250010109/model_cache/Qwen3-0.6B-Base-official`, loaded locally in BF16 and fully frozen.
- Target layer: zero-based layer 27 of 28.
- Activation site: `decoder_layer.mlp` forward pre-hook.
- SAE encoder: linear 1,024 to 30,000, learned bias, ReLU, then Top-32.
- SAE decoder: linear 30,000 to 1,024 with learned bias; decoder columns are renormalized after each update.
- Distributed form: four synchronized data-parallel SAE replicas, one on each H100; the base is replicated and frozen.

## 8. Training Objective And Optimization

The main loss is normalized reconstruction mean squared error. A dead-feature auxiliary term has weight `1/32`; after a feature has not fired for 50 steps, up to 512 dead features are selected to reconstruct the detached residual. This term is a stability aid and cannot rescue a failed main reconstruction gate. Optimization uses AdamW, learning rate `3e-4`, zero weight decay, ten-update linear warmup, gradient clipping at 1.0, BF16 autocast, and fixed seed 17.

## 9. Conditions, Seeds, And Checkpoints

One smoke condition and one seed are registered. Per GPU microbatch is one sequence of 1,024 tokens. Four GPUs therefore expose 4,096 raw tokens per optimizer update and 409,600 raw tokens over 100 updates. Four fixed validation batches are evaluated before and after training. Rank zero saves `sae_smoke_final.pt`; no intermediate checkpoint or result-based early stopping is allowed.

## 10. Primary Metric And Frozen Analysis Plan

The primary comparison is final versus initial held-out normalized reconstruction error on the identical deterministic validation windows. Pass requires the final value to be finite, strictly below one, and strictly below the initial value. Tokens are the observation units for loss aggregation; the single smoke run is not an independent scientific replicate. No uncertainty interval or multiple-comparison procedure is used because this is an engineering gate. The analysis unseals when `smoke_summary.json` is written.

## 11. Secondary Metrics And Guards

Record training first/last loss, mean positive features per token, total used/dead features, outlier-filter rate, gradient norm, peak per-GPU allocated memory, global tokens per second, base trainable-parameter count, model dimensions, token-ID range, checkpoint hash, and reload maximum absolute difference. These diagnose failures and cannot substitute for the primary gate.

## 12. Known Good / Known Bad / Known Confusing Cases

- Known good: CPU unit tests show exact Top-K behavior, unit zero-reconstruction error, deterministic rank-disjoint token windows, and checkpoint round-trip identity for a small SAE.
- Known bad: zero reconstruction has normalized error one; a final value at or above one fails.
- Known confusing: low reconstruction error with collapsed features or wrong activation provenance is not eligible and does not show semantics.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal | Input and assumptions | How | Why | Expected output | Pass / fail / insufficient | Named failure | Artifact | Handoff |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Preflight | verify the execution identity | frozen files and reserved node | record GPU, runtime, model/data existence, and unit tests | prevents wrong-environment evidence | preflight and test logs | all checks complete or stop | environment/data mismatch | `logs/preflight.log`, `logs/tests.log` | eligible trainer launch |
| Initial validation | define the untrained reference | fixed validation windows | evaluate normalized error and positive Top-K count | separates learning from initialization | initial metrics | finite or stop | hook/model/numerical failure | training log | fixed training |
| Training | exercise the full path | frozen base and DCLM train shard | run 100 synchronized SAE updates | tests optimization and throughput | step logs and trained weights | finite completion or stop | NaN/OOM/distributed failure | `logs/train.log` | final validation |
| Final validation and reload | qualify scale-up | fixed validation windows and saved checkpoint | repeat metrics and compare original versus reloaded output | rules out trivial reconstruction and serialization failure | summary and checkpoint | all gates true = Pass | reconstruction/collapse/reload failure | `smoke_summary.json`, `sae_smoke_final.pt` | full-run planning only |

## 14. Algorithm, Output, And Provenance Contract

Worker code and raw artifacts live under `/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/`. The ACP tuple is one node in `share-space`, `share-cluster`, worker spec `n6ls.iu.i40.4`, four H100 GPUs, normal priority, reserved quota, and the same NGC PyTorch image previously used by E14. The installed ACP component has a verified workspace-schema incompatibility, so the prior loopback compatibility bridge is reused and recorded as an engineering deviation. The bridge removes unsupported billing-cycle fields from workspace responses; it does not change the submitted training command.

## 15. Success / Failure / Insufficient Evidence

Pass requires all of: base trainable parameters equal zero; finite last training loss; finite final validation error; final validation error below one; final validation error below initial; mean positive features per token at least 31.99; more than 32 dictionary features used; exact reload maximum absolute difference equal zero; complete job receipt and artifacts. Any false verified item is Fail. Missing execution, identity, summary, log, or checkpoint evidence is Insufficient. Pass authorizes only an estimated full-run plan for human approval.

## 16. What This Cannot Claim

No outcome establishes interpretable features, feature implication hierarchy, held-out hierarchy stability, coarse/fine semantic alignment, causal Router recovery, LoRA expert placement, selective expert utility, or language-model task gain.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | State | Grounding |
| --- | --- | --- |
| A. Question and boundary | `CONFIRMED` | human-confirmed experiment-two purpose and explicit smoke authorization |
| B. Data and provenance | `CONFIRMED` | human selected DCLM; frozen local manifest verified |
| C. Learning task and supervision | `CONFIRMED` | self-reconstruction only; M2D2 truth excluded |
| D. Model and architecture | `CONFIRMED` | senior-project object plus human-confirmed 30,000/Top-32 plan |
| E. Objective and optimization | `CONFIRMED` | human-confirmed smoke parameters and Qwen-Scope stability adaptation |
| F. comparison and evidence | `CONFIRMED` | pre/post held-out reconstruction plus collapse/reload guards |
| G. execution and reproducibility | `CONFIRMED` | human explicitly selected four-H100 reserved ACP smoke |

Cross-block consistency passed before execution. Any post-start scientific change requires an append-only amendment. Full training, hierarchy construction, M2D2 semantic audit, Router/LoRA training, graph edits, sync, commit, and push are not authorized.

### Engineering repair ledger

- 2026-09-03, job `pt-uqiufy7f`: all 100 training updates completed with finite decreasing loss, but the smoke remained `Insufficient` because the checkpoint-reload model was instantiated on CPU while the fixed reload probe was on GPU. The repair moves the reloaded module to the requested `map_location`. No data, model, SAE, optimization, metric, gate, or full-training authorization changed. A replacement smoke is permitted solely to complete the originally approved engineering gates.
- 2026-09-03, replacement job `pt-mt4s38xi`: ACP state `SUCCEEDED`; every Section 15 gate is true; structured verdict `PASS`. This closes the approved smoke scope. Full training remains unauthorized and requires a separate frozen contract.

### Amendment F01: approved 1B-token full run

```text
amendment_time: 2026-09-03 after smoke completion and before full-run submission
before: smoke-only execution; one 74,750,913-token training shard; 100 updates; final checkpoint only
after: one from-initialization full run; sorted traversal over all 2,419 frozen DCLM training files; 244,141 updates; 1,000,001,536 raw tokens; fixed 100M, 300M, and 1B milestones plus resumable recovery state
reason: every smoke gate passed and the human explicitly instructed the task to enter training
evidence_visible_before_change: the complete smoke result and measured throughput were visible and formed the registered scale-up gate
affected_blocks: B data scale and traversal; E training duration only; G checkpoint and execution scope
unchanged: base model; zero-based layer 27 MLP pre-hook; 1,024 dimensions; 30,000 latents; ReLU Top-32; normalized reconstruction objective; auxiliary weight 1/32; dead-after 50; auxiliary Top-512; AdamW learning rate 3e-4; zero weight decay; ten-step warmup; gradient clip 1.0; BF16 autocast; norm filter; seed 17; fixed held-out validation source; no result-based selection
approval: HUMAN_APPROVED_FULL_RUN in the owning conversation
resource: one ACP node in share-space/share-cluster, n6ls.iu.i40.4, four H100 80GB processes, reserved quota, normal priority
eligibility: full-run evidence is eligible only if consumed-token accounting is exact, the full sharded manifest is recorded, all scheduled milestones are retained, and final smoke-derived reconstruction/freeze/collapse/reload gates remain true
```

The full run starts from a fresh seed-17 SAE initialization; the smoke checkpoint is not a training input. Milestone validations at steps `24,415`, `73,243`, and `244,141` use the same fixed DCLM validation stream and are diagnostic only. No early stopping or checkpoint selection is permitted. Recovery checkpoints may be written more frequently and retain only the latest two complete states; resumption must preserve the next optimizer step, SAE and optimizer state, dead-feature state, feature-used mask, immutable configuration, and deterministic data position. The full run produces `full_summary.json`, `sae_full_final.pt`, milestone metric records, the frozen training-file manifest, preflight/tests/train logs, and the ACP receipt. It does not authorize hierarchy construction, M2D2 semantic scoring, Router/LoRA training, graph edits, sync, commit, or push.

### Full-run execution ledger

- Submitted at `2026-09-03 15:07:35 UTC` as ACP job `pt-2lw02d0a`, with run stamp `20260903T150734Z` and output directory `runs/full-20260903T150734Z`.
- The single reserved `n6ls.iu.i40.4` worker reached `RUNNING` at `2026-09-03 15:08:14 UTC`; this is the start of the requested ten-minute launch-health observation window.
- The requested launch-health observation ended at `2026-09-03 15:18:23 UTC`. At step `13,000/244,141`, the job had consumed `53,248,000/1,000,001,536` raw tokens; total loss was `0.098891`, reconstruction loss `0.078840`, gradient norm `0.039824`, and segment throughput `102,108.64 token/s`. ACP remained `RUNNING`, and the observed log contained no OOM, NCCL, traceback, or data-read error. Active observation stopped while the training job continued. This is launch-health evidence only, not a full-run result.
- ACP job `pt-2lw02d0a` reached `SUCCEEDED` at `2026-09-03 18:03:14 UTC`. The frozen run completed all `244,141` updates and `1,000,001,536` raw tokens, retained all three registered milestones, and wrote the final summary and exactly reloadable checkpoint. The structured full-run verdict is `PASS`; see [summary.md](summary.md) and [detailed.md](detailed.md). This receipt does not authorize or report hierarchy construction.
