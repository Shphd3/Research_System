# Run Receipt: A15_17_E01 / three-model-rep-audit-0916-h100-reserved-full-v4

Owner: `Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_E01_three_model_sae_representation_audit/protocol.md`  
Status: `SUCCEEDED`; S2--S6 and final artifact audit `PASS` (completed 2026-09-16T02:20:45Z)

## Resolved Tuple

| Field | Value |
|---|---|
| resource_profile | `h100-4-reserved` |
| execution_surface | `acp` |
| workspace / aec2 | `share-space` / `share-cluster` |
| worker_spec / worker_nodes / worker_processes | `n6ls.iu.i40.4` / 1 / 4 |
| quota_type / priority | `reserved` / `normal` |
| GPU / CPU / host memory | 4×H100 80GB / 88 vCPU / 960 GiB |
| image_id | `shphd-lite-0911` |
| image_url | `registry.cn-sh-01g.sensecore.cn/ccr-zhicheng-03/shphd-lite-0911:shphd-mig-20260910161423` |
| activation | Dense baseline `scripts/runtime.sh`; qualified current-image H100 path |
| analysis dependency layer | execution-local `deps/`: UMAP 0.5.6 and pynndescent 0.5.13 |
| storage_mount | `01995892-d478-76d8-aec7-13fd8284477e:/data` |
| job id | `pt-we1cni15` |
| retry count | 0 |
| submitted_at / started_at / terminal_at | `2026-09-16T01:31:21Z` / `2026-09-16T01:31:38Z` / `2026-09-16T02:20:45Z` |

## Entry Point

Submitted through `templates/execution/acp_submit_template.sh`, which resolved to the registered `sco_acp_compat.sh`. Gates satisfied: `DRY_RUN=0`, `ALLOW_SUBMIT=1`, `PROTOCOL_APPROVED=1`, and `SMOKE_GATE_PASSED=1`. Before submission, the updated source audit, Python compilation, shell syntax, 17 CPU tests, exact four-worker manifest, and a real two-process node-local `flock` test passed.

Exact analysis command inside the template wrapper:

```bash
RUN_ROOT=/data/250010109/MoE_Router/experiments/20260915_three_model_representation_audit/runs/full_h100_reserved_v4 bash scripts/run_full_remote_audit.sh
```

The template wrapper exports `RESOURCE_PROFILE=h100-4-reserved`, `IMAGE_ID=shphd-lite-0911`, changes to the execution root, and tees all stdout/stderr to the persistent pod-log directory.

## Scope And Roots

Approved scope is the complete frozen-checkpoint S2--S6 audit in the Protocol: six bounded qualification tasks; all 18 P/N representation and four-batch gradient tasks; Part A raw; mandatory fit-only B1/B2/B3; paired 5,000-draw evidence; A01--A09 and B01--B04 including 0B representation/atom evolution. It excludes all training, checkpoint mutation, resource fallback, commit, and push.

- Code root: `/data/250010109/MoE_Router/experiments/20260915_three_model_representation_audit/`
- Run/result root: `/data/250010109/MoE_Router/experiments/20260915_three_model_representation_audit/runs/full_h100_reserved_v4/`
- Submission receipt: `/data/250010109/MoE_Router/experiments/20260915_three_model_representation_audit/acp_receipts/submit-three-model-rep-audit-0916-h100-reserved-full-v4-20260916T013119Z.json`
- Persistent log directory: `/data/250010109/MoE_Router/experiments/20260915_three_model_representation_audit/runs/full_h100_reserved_v4/pod_logs/`
- TensorBoard: `NOT_APPLICABLE`.

## Training Comparison Contract

`NOT_APPLICABLE`: this is read-only checkpoint analysis with zero optimizer, scheduler, training-token, or model-buffer updates.

## Previous Attempts And First Failure

1. `pt-7yis2se8`: 4×RTX5090 Spot attempt stopped at researcher request while still pending; `SUSPENDED`, `start_time=null`, no scientific artifact.
2. `pt-20q3i7pd`: 2×H100 Spot attempt reached S2. The source audit and 13 then-current CPU tests passed and two H100s were visible. It failed before any of six qualification units completed because the same-node checkpoint-load advisory lock lived on AFS and `fcntl.flock` returned `BlockingIOError: [Errno 11] Resource temporarily unavailable`. Its run root `runs/full_h100_v2` is preserved as failure evidence and is `INELIGIBLE` for scientific claims.
3. `pt-xsmaub14`: first 4×H100 Reserved attempt verified the node-local lock repair, all four GPUs, both M0 qualification tasks, and the M0 10B gradient path. It then failed S2 because a zero-dimensional Long buffer was byte-viewed before flattening. Its two M0 qualification artifacts are engineering evidence only and are not reused by v2.
4. `pt-i2ofctjz`: second 4×H100 Reserved attempt passed all six S2 tasks and completed two M0 S3 shards, then failed because an SAE activation tensor that required grad was converted directly to NumPy. Its artifacts are engineering evidence only and are not reused by v3.
5. `pt-ix1stwdr`: third Reserved attempt passed all six S2 tasks, then hit the inactive-AuxK constant-zero autograd error on M2 0B. It was stopped after the durable failure was captured; seven partial completion records are engineering evidence only and are not reused by v4.

R003 moves only that synchronization lock to container-local `/tmp`, where kernel release semantics are reliable, and changes whole-task engineering assignment from 9/9 to 5/5/4/4 on the explicitly authorized Reserved node. R004 flattens each state tensor before its byte-view, with scalar Long and bfloat16 regression coverage. R005 puts SAE encode under inference mode and routes every PyTorch-to-NumPy export through detach. R006 records an inactive constant-zero AuxK component as an exact zero gradient while preserving normal autograd for active objectives. All model, checkpoint, panel, hook, transform, metric, bootstrap, figure, stop, and claim-boundary contracts are unchanged. The current v4 run uses a fresh root and does not reuse partial artifacts.

## Monitoring

`monitor_owner`: conversation `0915-3 models representation Audits`, Codex. The completion goal follows job `pt-we1cni15`, the persistent pod log, stage receipts, and the fresh v4 run root. Supervision audits S2--S6 and then fills the canonical result records. Stopping a polling window never stops or resubmits the job.

ACP started the job at 2026-09-16T01:31:38Z on one Reserved `n6ls.iu.i40.4` worker. At 2026-09-16T01:34:44Z S2 passed all six registered tasks: all four H100s were visible, 17 remote regression tests passed, hook and finite-value checks passed, the M0/M1/M2 10B gradient paths ran, every model state hash was unchanged, and optimizer/buffer updates were zero. At 2026-09-16T01:45:33Z S3 passed with 18 caches, 18 gradient records, and 18 matching completion records. The registered analyzer completed at 2026-09-16T02:20:40Z after 2,106.34 seconds, and the runner wrote a PASS terminal receipt at 2026-09-16T02:20:41Z. ACP marked the job `SUCCEEDED` at 2026-09-16T02:20:45Z.

The final read-only audit rehashed every cache and gradient against its completion record, verified four batches in each gradient file, counted 216 transform files and 19 nonempty tables, decoded all 16 required figures, and rechecked the 5,000-draw and zero-update receipts. No error remained.

## Eligibility

Fresh-v4 S2 certifies runtime, hook, finite-value, memory, state-immutability, and the earlier repaired boundaries. S3 certifies complete checkpoint collection and local-gradient records. S4--S6 and the final artifact audit certify the raw analysis, fit-only B1/B2/B3 transforms, paired 5,000-draw tables, and all required figures as `ELIGIBLE` for the Protocol's bounded representation claims.

Execution success does not own the scientific judgment. The current result reading is `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION` in [summary.md](summary.md), [summary_cn.md](summary_cn.md), and [detailed.md](detailed.md). No causal, downstream-use, or general-superiority claim is authorized.
