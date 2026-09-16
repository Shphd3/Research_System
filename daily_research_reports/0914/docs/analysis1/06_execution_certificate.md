# Run Receipt: analysis1 / dense-sae-analysis1-full

Owner: `daily_research_reports/0914/docs/analysis1/04_execution_scope.md`  
Status: SUCCEEDED

## Resolved tuple

| Field | Value |
| --- | --- |
| resource_profile | `5090-2-spot` |
| execution_surface | `acp` |
| workspace / aec2 | `share-space` / `computing-cluster-5090-01g` |
| worker_spec / worker_nodes / worker_processes | `n12lp.nn.i10a.2` / 1 / 2 |
| quota_type / priority | SPOT / normal |
| image_id | `shphd-lite-0911` |
| activation script | Dense SAE `runtime.sh` plus baseline `activate_5090_runtime.sh` |
| dependency layer | PyTorch 2.8.0+cu128 mounted layer, `sm_120` present |
| storage_mount | AFS mounted at `/data` |
| gpu_used | true, 2× RTX 5090 32GB |
| job id | `pt-lok5c11y` |
| retry count | 0 for this full job |
| submitted_at / terminal_at (UTC) | 2026-09-13T16:43:49Z / 2026-09-13T16:51:25Z |

## Entry point

Submitted through the registered `sco_acp_compat.sh` entry point via
`templates/execution/acp_submit_template.sh`.

Gates satisfied: `DRY_RUN=0`, `ALLOW_SUBMIT=1`, execution scope explicitly
authorized by the researcher, and `SMOKE_GATE_PASSED=1` from `pt-f2dgdcod`.

Remote command:

```bash
ANALYSIS1_SMOKE_PASSED=1 bash scripts/run_semantic_evolution_analysis1_full_2x5090.sh /data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/analysis_runs/analysis1_20260913/full
```

## Scope and roots

Approved scope: read-only semantic analysis of five existing SAE-mediated
checkpoints plus a frozen Qwen3-0.6B external endpoint. No training, optimizer
step, checkpoint write, or interruption of another job is allowed.

- Code root: `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining`
- Result root: `analysis_runs/analysis1_20260913/full`
- Pod log prefix: `acp_receipts/pod/dense-sae-analysis1-full-`
- TensorBoard: NOT_APPLICABLE; this is checkpoint analysis, not training.

## Training comparison contract

NOT_APPLICABLE. The job performs inference and analysis only and records
`optimizer_updates: 0`.

## Monitoring

`monitor_owner`: current Codex conversation. Monitoring was intentionally
bounded to startup health. The platform reached `RUNNING`, the worker Pod was
running with two GPUs, the 864-sample contract was present, and complete 0.5B
and 1B caches were observed. Polling then stopped without stopping the job.
The later result audit verified platform `SUCCEEDED`, terminal exit 0, and the
full artifact set; it did not supervise the intervening runtime.

## First diagnosis

Three preceding Smoke attempts exposed one missing detach and two stale,
unused optional-extension ABI conflicts. The final code detaches decoder norms
and disables FlashAttention/torchvision auto-imports for the text-only SDPA
reference path. Failed logs and outputs were preserved; no scientific input
was mutated.

## Eligibility

The terminal receipt and required outputs pass, so this job certifies that the
fixed analysis pipeline ran on the candidate panel. Its scientific outputs
remain `BOUNDED_EXPLORATORY_ONLY` because the panel is not researcher-reviewed
and Qwen3-0.6B is not a matched no-SAE baseline. It does not certify a causal
effect of SAE or abstract semantic formation.
