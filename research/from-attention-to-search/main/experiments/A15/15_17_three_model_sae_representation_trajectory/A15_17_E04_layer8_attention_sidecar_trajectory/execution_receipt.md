# Execution Receipt: A15_17_E04

## Eligible execution

| Field | Value |
| --- | --- |
| Scope | S7 only; 0/0.5/1/3/5/10B; read-only representation, sparse contribution, gradient, reconstruction, and loss analysis |
| Smoke job | `pt-4zcfwzwp` |
| Full job | `pt-ub07t6fc` |
| Full job name | `sidecar-s7-rep-audit-0917-5090x4-full-v1` |
| Platform terminal state | `SUCCEEDED` at `2026-09-17T10:53:41Z` |
| Resource profile | `5090-4-spot`; one node; four NVIDIA GeForce RTX 5090; Spot |
| Image | `shphd-lite-0911` |
| Runtime layer | `/data/250010109/dependency_packages/dense_baseline_torch280_cu128_py310` |
| PyTorch / CUDA | `2.8.0+cu128` / `12.8`, `sm_120` present |
| Transformers | mounted offline `4.53.3` |
| Full run root | `/data/250010109/MoE_Router/experiments/20260917_sidecar_representation_gradient_audit/runs/full_5090_4spot_v1` |
| Final curated analysis | `/data/250010109/MoE_Router/experiments/20260917_sidecar_representation_gradient_audit/runs/full_5090_4spot_analysis_v2` |
| Pod log | `/data/250010109/MoE_Router/experiments/20260917_sidecar_representation_gradient_audit/acp_receipts/pod/sidecar-s7-rep-audit-0917-5090x4-full-v1-20260917T104023Z.log` |
| Completion | 6/6 checkpoints; 360 P rows and 1,200 N rows per checkpoint; four gradient batches per checkpoint |
| Optimizer updates | `0` |
| Peak CUDA memory | 3.42--3.49 GB per task |
| Curated artifacts | 16 PNG + 16 SVG figures; 13 source tables; overview JSON |

## Qualification and retries

- Local qualification: 5/5 tests PASS; direct 0B hook load PASS; hook layer 7; Attention/final shapes `[1,3,1024]`; SAE width 30,000; Top-32.
- `pt-hxlku819`: overbroad queued/suspended attempt; no eligible cache, gradient, or metric.
- `pt-aafi4o85`: hardware preflight passed but tokenizer dependency was absent; stopped before reading a panel; no eligible scientific artifact.
- The fresh Smoke `pt-4zcfwzwp` passed all registered checkpoints, state immutability, structural-gradient zeros, and zero optimizer updates before the full job was submitted.

## Analysis revision

The full job produced all raw caches, gradients, 16 figures, and 11 original tables. Local `analysis_v2` reused those immutable artifacts and corrected only probe comparability: the raw-selected regularization strength is now reused for B1/B2/B3. Two missing figure-source tables were also exported. No GPU recomputation, row reselection, checkpoint change, or model mutation occurred.

Key source hashes:

- `analyze.py`: `833b08e70da5a415637bf90ee6345455fd88d1f649db188bfb2e11f7c50b0c2b`
- `reanalyze_fixed_probe.py`: `2ce81ad8c1a82665920d8d815c3dcd34a09e4548fe3af0aff033b9c609fa4b91`
- `export_figure_source_tables.py`: `9dc4ce68e6532aaaf43cc1445d52b599e1d193d87594eff00e96850b93c102b1`
- final overview: `04cda2aa059dd732bb570ac227ac0490a9019766659a7b0f2f7142eec63ca3cb`
- final representation table: `da1896f83464ad6ba4c1162755c99748de270393728e271f97e58e53f13a22dd`
- paired Fisher table: `a4c190d70c20651ec1bf4b900ea27505c158374dfd37d25fc7d3ad2d9bfe5e56`
- paired probe table: `46788c1e2f88828d7ec5e39617128424620b91e320fea29bd00e8844ca7301fb`
- fixed-atom trajectory table: `2614aa41e40c374f5f6fb8a2f9df405149d99bbf6de75afd7036f1e16bdb6c05`
- loss trajectory table: `8674e24eb63d30ce310c43857a336b5e05ac0dd3e5c549ec364326081b2e0d0e`
