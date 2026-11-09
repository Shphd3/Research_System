# Analysis1 execution record

**State:** FULL_SUCCEEDED — result audit completed  
**Scientific eligibility:** BOUNDED_EXPLORATORY_ONLY

## Implementation checks

- Checkpoint-only analyzer:
  `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/dense_sae/analysis/semantic_evolution.py`
- Frozen config:
  `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/configs/semantic_evolution_analysis1.json`
- Smoke runner and full runner are separate; the full runner requires
  `ANALYSIS1_SMOKE_PASSED=1`.
- The implementation has no optimizer construction or optimizer step. Every
  contract and terminal receipt records zero optimizer updates.
- UMAP is explicitly `NOT_RUN_dependency_unavailable`; t-SNE and PCA are not
  substituted as evidence for it.
- `python -m py_compile`, both runner `bash -n` checks, and the final focused
  checkpoint/semantic test set passed: 11 tests passed. A local full
  `Qwen3ForCausalLM` load also verified its 28-layer final MLP path.
- Pre-submission source snapshot:
  `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/analysis_runs/analysis1_20260913/source_snapshot/analysis1_source_20260913T162024Z.tar.gz`
  with SHA-256
  The final post-fix snapshot is `analysis1_source_20260913T164000Z.tar.gz`,
  SHA-256
  `cab649ea6e83d3d61a5d186e02b8271950fdab6dfdb7e8fadd26031e56981285`.

## Smoke attempts and result

- `pt-mm0ypzuk`: FAILED after both checkpoint forwards because decoder norms
  were converted to NumPy without detaching. No input or checkpoint changed.
- `pt-yidkc8i6`: FAILED after writing the 0.5B and 10B caches because the base
  image's unused FlashAttention extension was ABI-incompatible with the
  mounted PyTorch 2.8 runtime.
- `pt-wtlgw6dk`: FAILED after writing the same two caches because the base
  image's unused torchvision extension was also ABI-incompatible.
- `pt-f2dgdcod`: SUCCEEDED. The code explicitly disabled both unused optional
  extension paths and kept PyTorch SDPA. Its `smoke_receipt.json` is `PASS`,
  all three finite caches contain 24 samples, terminal exit is zero, and
  optimizer updates are zero.

Every attempt used one `n12lp.nn.i10a.2` node, 2× RTX 5090, SPOT, normal
priority, the current `shphd-lite-0911` image, and the isolated CUDA 12.8 / SM120
runtime. Failed directories and logs are retained as engineering evidence.

## Full job

- ACP job: `pt-lok5c11y`
- Submitted at: 2026-09-13T16:43:49Z, after the successful Smoke gate.
- Platform terminal state: `SUCCEEDED`; started 2026-09-13T16:44:01Z and
  completed 2026-09-13T16:51:25Z, with no platform retry.
- `analysis_receipt.json`: `PASS`, 864 samples, 216 facts, five requested
  checkpoints, and `optimizer_updates: 0`.
- `terminal_receipt.json`: exit code 0.
- All five SAE checkpoint caches, the Qwen endpoint cache, nine cross-reader
  caches, three result tables, and the required figure families exist.
- The prior ETA was consistent with the observed completion time; polling had
  already stopped after startup and did not keep this conversation alive.
- Scientific eligibility remains `BOUNDED_EXPLORATORY_ONLY`; operational
  completion is not a semantic verdict.
