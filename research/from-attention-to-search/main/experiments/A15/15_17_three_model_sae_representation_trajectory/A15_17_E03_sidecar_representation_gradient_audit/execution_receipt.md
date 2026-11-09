# Execution Receipt: A15_17_E03

Owner: [protocol.md](protocol.md)  
Overall evidence status: `ELIGIBLE_READ_ONLY_MEASUREMENT_WITH_RECORDED_CPU_SYNTHESIS_REPAIR`  
Scientific interpretation: `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`

## Resolved execution tuple

| Field | Value |
| --- | --- |
| resource profile | `5090-4-spot` |
| execution surface | ACP, `share-space` |
| AEC2 / worker spec | `computing-cluster-5090-01g` / `n12lp.nn.i10a.4` |
| topology | one node, four RTX 5090 32GB GPUs |
| quota / priority | Spot / normal |
| image | `shphd-lite-0911` |
| runtime layer | `/data/250010109/dependency_packages/dense_baseline_torch280_cu128_py310` (`torch 2.8.0+cu128`, SM120) |
| offline tokenizer layer | `/data/250010109/dependency_packages/hf_transformers_qwen3` |
| storage mount | registered AFS mount at `/data` |
| optimizer updates | 0 |

## Job ledger

| Job | Scope | Terminal state | Scientific artifact | Eligibility |
| --- | --- | --- | --- | --- |
| `pt-hxlku819` | first Smoke submission | stopped / allocation race | runtime line only | INELIGIBLE |
| `pt-08dxw4r6` | isolated Smoke v1 | stopped after import failure | GPU preflight only | INELIGIBLE |
| `pt-mdmegr1t` | isolated Smoke v2 | SUCCEEDED | 4/4 Smoke tasks; peak 5,232,389,120 bytes | ELIGIBLE Smoke |
| `pt-yuifv33t` | full collection plus initial synthesis | FAILED at CPU synthesis | 12/12 GPU tasks PASS; initial result analysis none | collection ELIGIBLE; combined terminal is not result PASS |
| local S4/S5 repair | synthesis only | PASS | 5 tables, 14 figures | ELIGIBLE with Protocol R004 |

## Completion audit

- New-model matrix: 3 models x 4 checkpoints = 12/12.
- Panels per cell: P 360/360; N 1,200/1,200.
- Gradient batches per cell: 4/4; all eight N classes represented per batch.
- Structural guards: zero reconstruction gradient outside selected positions; zero AuxK gradient at Attention output; exact hook set; finite values; sampled state hash unchanged.
- Peak allocated GPU memory: 5,297,049,600 bytes.
- Collection receipt: `runs/full_5090_4spot_v1/stages/COLLECTION_PASS.json`.
- Synthesis receipt: `runs/full_5090_4spot_v1/synthesis_receipt.json`.
- Final result overview SHA256: `0f0d93b85d3b6c311f2be842da721e9c819b0ed95977665078af15bbc275ca2a`.

## Failure and repair boundary

The first full synthesis selected no P report rows because it used semantic names `tune/report` as literal file values. The frozen file uses `development/confirmation`. Protocol R004 records the one-to-one role mapping. The error occurred before any result table, figure, or interpretation existed; the repair changed no row membership, metric, threshold, checkpoint, or model output. GPU caches and gradient artifacts were not regenerated.

## Monitoring

Monitoring owner: current Codex task. Smoke and full collection were supervised through terminal receipts; the separate CPU synthesis was supervised through `S4_S5_PASS.json` and the synthesis receipt.
