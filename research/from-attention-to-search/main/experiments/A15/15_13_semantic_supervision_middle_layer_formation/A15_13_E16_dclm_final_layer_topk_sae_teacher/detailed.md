# Detailed Record: A15_13_E16 DCLM final-layer Top-K SAE

```text
status: FULL_RUN_COMPLETE; AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
protocol_verdict: PASS
scientific_claim: technically qualified SAE dictionary only
```

## 1. Execution identity

| Item | Recorded value |
| --- | --- |
| Successful ACP job | `pt-mt4s38xi` |
| Display name | `a15-13-e16-sae-smoke-20260903T144600Z` |
| ACP state | `SUCCEEDED` |
| ACP start / terminal update | `2026-09-03T14:44:32Z` / `2026-09-03T14:45:43.705602Z` |
| Workspace / cluster | `share-space` / `share-cluster` |
| Worker | one `n6ls.iu.i40.4` node |
| GPU | 4×NVIDIA H100 80GB HBM3 |
| Quota | `RESERVED` |
| Container | `registry.cn-sh-01.sensecore.cn/lepton-trainingjob/ngc-pytorch:25.06-cu12.9-py3.12-ubuntu24.04` |
| Runtime | Python 3.12.3, PyTorch 2.8.0 NGC build, CUDA 12.9, Transformers 4.53.3 |

## 2. What actually ran

This was one training stage, not staged training. Qwen3-0.6B-Base and all Transformer parameters were frozen. The only trainable object was a 61,471,024-parameter SAE. Four synchronized data-parallel processes each consumed one 1,024-token window per update; there was no gradient accumulation. The run executed 100 optimizer updates and exposed 409,600 raw tokens globally.

The SAE used 1,024 input dimensions, 30,000 latent features, ReLU followed by Top-32 selection, and a learned linear decoder whose columns were renormalized after each update. The main objective was normalized reconstruction mean squared error. A dead-feature residual-reconstruction auxiliary objective had weight `1/32`, activated after 50 silent steps, and considered at most 512 dead features. AdamW used learning rate `3e-4`, zero weight decay, ten-update linear warmup, gradient clipping at 1.0, BF16 autocast, and seed 17. The base activation was the zero-based layer-27 MLP forward-pre-hook state. The largest 0.1% of state norms within each process batch were filtered.

There was no result-based checkpoint selection. Fixed validation windows were evaluated before and after the 100 updates. Rank zero saved the final SAE and immediately reloaded it for an exact-output identity check.

## 3. Registered comparisons and results

| Question protected | Comparison / guard | Result |
| --- | --- | ---: |
| Did held-out reconstruction improve? | final versus initial normalized error | `0.3367877454` versus `0.7890049927` |
| Is reconstruction nontrivial? | final error versus zero-output reference | `0.3367877454 < 1.0` |
| Was the base frozen? | trainable base parameters | `0` |
| Did Top-32 remain active? | positive features per held-out token | `32.0` |
| Did the dictionary collapse to a tiny support? | globally used features | `19,614 > 32` |
| Did serialization preserve output? | reload maximum absolute difference | `0.0` |
| Was optimization finite? | first / last total training loss | `0.7897408605` / `0.3511626422` |
| What was the realized norm filter rate? | train and held-out fraction | `0.001953125` |

All eight registered gates in `smoke_summary.json` are true. The typed protocol verdict is therefore `PASS`.

## 4. Engineering repair record

The first submitted job, `pt-uqiufy7f`, completed all 100 updates with the same finite loss trace but failed before producing a complete smoke summary. The saved weights were loaded into a CPU module while the reload probe remained on GPU. This was an implementation error in `TopKSAE.from_pretrained`, not a failed reconstruction or feature-use gate. The repair moves the reloaded module to the requested device and extends the checkpoint round-trip test to execute on CUDA whenever CUDA is available. No scientific parameter, data object, metric, threshold, or training budget changed. The replacement job reran the entire smoke from initialization and passed.

## 5. Artifacts

- Successful structured result: `/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/smoke-20260903T144600Z/smoke_summary.json`
- Successful training log: `/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/smoke-20260903T144600Z/logs/train.log`
- Successful preflight and tests: `/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/smoke-20260903T144600Z/logs/`
- Qualified checkpoint: `/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/smoke-20260903T144600Z/sae_smoke_final.pt`
- Checkpoint SHA-256: `3494fd56bef398b520093e49a12682fb67890d24425e33abea76042f2211971b`
- Submission receipt: `/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/submit-smoke-20260903T144600Z.txt`
- Failed-attempt log retained for audit: `/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/smoke-20260903T144200Z/logs/train.log`

## 6. Runtime projection

The measured pure-training rate is:

\[
\frac{409{,}600\ \text{tokens}}{3.367652\ \text{s}}=121{,}627.76\ \text{tokens/s}.
\]

At fixed four-GPU batch size, the projection is \(T=N/121{,}627.76\). This is an engineering extrapolation from a short run, not a guaranteed service-level time.

| Token budget | Updates at 4,096 tokens/update | Pure training | Conservative reserved-node budget |
| ---: | ---: | ---: | ---: |
| 100M | 24,415 | 13.7 min | 18–25 min |
| 300M | 73,243 | 41.1 min | 50–60 min |
| 1B | 244,141 | 2.28 h | 2.7–3.0 h |
| 3B | 732,422 | 6.85 h | 7.8–8.5 h |
| full 302.089B view | 73,752,318 | 689.9 h / 28.75 d | not recommended |

The recommended first full training contract is 1B tokens because it is large enough to expose each of 30,000 features to a broad DCLM sample while remaining a same-day run. This is a proposed budget, not evidence that 1B is statistically optimal. Checkpoint learning curves at 100M, 300M, and 1B should be retained so the later result can show whether reconstruction and dead-feature rates saturate.

## 7. Full-run prerequisites and boundary

The smoke read one 299,003,652-byte uint32 shard, or 74,750,913 tokens. A 1B run would wrap that shard repeatedly if the current stream were reused. Therefore deterministic traversal of the frozen 2,419-file, 302,089,493,820-token DCLM view is mandatory before scale-up. The full worker also needs resumable optimizer and scheduler state, checkpoint intervals, exact consumed-token accounting, and fixed held-out validation windows.

Passing this smoke establishes only trainer eligibility. It does not establish semantic feature identity, activation-containment hierarchy, coarse/fine alignment, layerwise Router accessibility, expert utility, or downstream task gain.

## 8. Figure contract and audit

The figure asks whether reconstruction passed and how the measured training-loop throughput scales with candidate token budgets. The left y-axis is normalized reconstruction error; the right x-axis is billions of tokens on a log scale and the right y-axis is projected pure training hours on a log scale. Inputs are the successful `smoke_summary.json` and the frozen DCLM manifest token count. It may support the engineering qualification and runtime decision only. It cannot support a semantic or routing claim. The rendered PNG was visually audited for readable labels, correct values, and explicit pure-training scope.

## 9. Full-run execution and conformance

The human separately approved Amendment F01's fixed 1B-token run after the smoke passed. The full run was one continuous stage from a fresh seed-17 SAE initialization; it did not load the smoke checkpoint. Qwen3-0.6B-Base remained frozen and only the SAE parameters were optimized. Four synchronized H100 processes each supplied one 1,024-token window per update, with no gradient accumulation. The run executed `244,141` optimizer updates and consumed `1,000,001,536` raw tokens. The objective, optimizer, learning rate, sparsity, activation site, norm filtering, and seed matched the amendment. Checkpoints were fixed by token count and were never selected by observed validation performance.

| Registered item | Expected | Actual | Status | Eligibility impact |
| --- | --- | --- | --- | --- |
| ACP resource | one reserved `n6ls.iu.i40.4` node, 4×H100 | job `pt-2lw02d0a`, 4×H100 80GB | Conformant | eligible |
| Data identity | 2,419 frozen DCLM files; `302,089,493,820` source tokens | exact counts recorded; semantic manifest hash `a82ee6a...886bbe4` | Conformant | eligible |
| Training budget | `244,141` updates; `1,000,001,536` raw tokens | exact | Conformant | eligible |
| Fixed milestones | `24,415`, `73,243`, `244,141` | all three present | Conformant | eligible |
| Model and SAE | frozen 28-layer/1,024-wide Qwen; layer-27 MLP pre-hook; 30,000/Top-32 SAE | exact; base trainable parameters `0` | Conformant | eligible |
| Optimization | AdamW `3e-4`, zero decay, 10-step warmup, clip `1.0`, fixed auxiliary settings | exact recorded contract | Conformant | eligible |
| Stop/selection | fixed final step; no early stopping or result-based selection | fixed final step | Conformant | eligible |
| Completion | structured summary, milestones, final and recovery checkpoints, exact reload | all present; ACP `SUCCEEDED` | Conformant | eligible |

No scientific configuration deviation or retry was recorded. The file-level SHA-256 of the pretty-printed `train_manifest.json` is `aa6346d043ef7de4f562340d50b14d1bc8876cfe15c446741385bfcbdd91edc7`; the semantic manifest hash inside the contract is computed from the canonical manifest object before adding its self-hash and is therefore intentionally different.

## 10. Full-run evidence lineage

| Decision | Raw artifact | Computation | Observed value | Eligibility | Limitation |
| --- | --- | --- | ---: | --- | --- |
| Full budget completed | `full_summary.json` and `train_manifest.json` | steps × 4 GPUs × 1,024 tokens | `1,000,001,536` | Eligible | token exposure is not semantic coverage |
| Reconstruction improved | fixed held-out validation fields in `full_summary.json` | normalized squared reconstruction error | `0.7890049927 → 0.0533820926` | Eligible | reconstruction is not interpretability |
| Improvement persisted across fixed milestones | `milestones.json` | same validation estimator at 100M/300M/1B | `0.0604918830 / 0.0575391222 / 0.0533820926` | Eligible | checkpoints are not independent replicates |
| Dictionary did not globally collapse | global feature-used union in `full_summary.json` | count of features firing at least once | `30,000/30,000` | Eligible | does not prove balanced or meaningful usage |
| Checkpoint is reproducible | saved checkpoint and fixed reload probe | maximum absolute reconstruction difference | `0.0` | Eligible | does not test another software stack |
| Platform run completed | ACP job record | terminal platform state | `SUCCEEDED` | Eligible | platform success alone is not a scientific result |

The final validation error is lower than the 100M and 300M values, but these checkpoints share one optimization trajectory and one validation stream. They show continued within-run improvement; they are not three independent demonstrations of generalization.

## 11. Full-run artifacts

- Structured result: `/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/full_summary.json`
- Final checkpoint: `/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/sae_full_final.pt`
- Final checkpoint SHA-256: `e4e2049aced8ba9a3b043bbb2b3308b497b7ec22f107531e37197873ee545b65`
- Fixed milestone ledger: `/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/milestones.json`
- Milestone checkpoints: `checkpoints/sae_step_24415.pt`, `checkpoints/sae_step_73243.pt`, `checkpoints/sae_step_244141.pt`
- Alternating recovery states: `checkpoints/recovery_0.pt`, `checkpoints/recovery_1.pt`, with `latest.json`
- Frozen train manifest: `/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/train_manifest.json`
- Preflight, test, and training logs: `/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/logs/`
- Submission receipt: `/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/submit-full-20260903T150734Z.txt`

## 12. Full-run boundary and next decision

The eligible result establishes a technically qualified final-layer SAE dictionary. It does not establish interpretable features, activation-containment hierarchy validity, coarse/fine semantic alignment, layerwise recoverability, online routing, expert utility, or task gain.

The one proposed next decision is whether to confirm a gated hierarchy-and-layer-recovery audit. Its first gate must use DCLM only to discover and independently replicate candidate feature relations. M2D2 labels may enter only after the hierarchy is frozen, for semantic interpretation and comparison with the separately owned gold-label audit. No Router or LoRA training is part of that decision.
