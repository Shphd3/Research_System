# Run Receipt: A15_17_E02 / sae-grad-followup-0916-h1004-full-v2

Owner: [protocol.md](protocol.md)  
Status: `SUCCEEDED`; Smoke, full matrix, synthesis, and reader-artifact audit `PASS`.

## Resolved Tuple

| Field | Value |
|---|---|
| resource profile | `h100-4-reserved` |
| execution surface | ACP |
| workspace / AEC2 | `share-space` / `share-cluster` |
| worker spec / nodes | `n6ls.iu.i40.4` / 1 |
| allocation | 4× NVIDIA H100 80GB HBM3, 88 vCPU, 960 GiB host memory |
| quota / priority | `reserved` / `normal` |
| image | `shphd-lite-0911` |
| image URL | `registry.cn-sh-01g.sensecore.cn/ccr-zhicheng-03/shphd-lite-0911:shphd-mig-20260910161423` |
| runtime activation | `/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/scripts/runtime.sh` |
| storage | `01995892-d478-76d8-aec7-13fd8284477e:/data` |
| successful Smoke | `pt-eweyxti7` |
| successful full job | `pt-d6swd6xd` |
| submitted / started / terminal | `2026-09-16T07:27:16Z` / `07:28:01Z` / `07:31:07Z` |

The four GPUs were allocated and visible. The frozen single-process implementation used `cuda:0`; it did not distribute the small audit matrix over all four devices. Peak memory on that device was 9,759,047,680 allocated bytes and 15,097,397,248 reserved bytes. This affects resource efficiency, not the registered scientific comparison.

## Entry Point

Submitted through `templates/execution/acp_submit_template.sh`, resolving to the registered `sco_acp_compat.sh`. Gates satisfied: `DRY_RUN=0`, `ALLOW_SUBMIT=1`, `PROTOCOL_APPROVED=1`, and `SMOKE_GATE_PASSED=1`.

Exact inner command:

```bash
source /data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/scripts/runtime.sh && \
python3 scripts/run_gpu_followup.py --run-root runs/full_h100_4reserved_v2 && \
python3 -c 'import json; x=json.load(open("runs/full_h100_4reserved_v2/terminal_receipt.json")); assert x["visible_cuda_devices"]==4; assert x["status"]=="PASS"; assert x["optimizer_updates"]==16'
```

## Scope And Roots

- Approved scope: local L1--L4 supplements; M2 G0/G1 at 10B and 15B; frozen M0/M1/M2 N-report NLL at 10B and 15B; 15B sensitivity; complete supervision to terminal state.
- Code root: `/data/250010109/MoE_Router/experiments/20260916_sae_gradient_parameter_followup/`
- Eligible full root: `/data/250010109/MoE_Router/experiments/20260916_sae_gradient_parameter_followup/runs/full_h100_4reserved_v2/`
- Successful submission receipt: `/data/250010109/MoE_Router/experiments/20260916_sae_gradient_parameter_followup/acp_receipts/submit-sae-grad-followup-0916-h1004-full-v2-20260916T072715Z.json`
- Persistent log: `/data/250010109/MoE_Router/experiments/20260916_sae_gradient_parameter_followup/acp_receipts/pod/sae-grad-followup-0916-h1004-full-v2-20260916T072803Z.log`
- TensorBoard: `NOT_APPLICABLE`; this was frozen analysis plus isolated one-step counterfactual updates, not a language-model training run.

## Monitoring And Completion

`monitor_owner`: current Codex task. Monitoring followed ACP state, persistent pod logs, intermediate caches, terminal receipt, and CPU synthesis through completion.

- Smoke v2 passed in 31.59 s with four visible H100s, finite G0/G1 values, exact zero reconstruction gradient outside the registered positions, and unchanged SAE state.
- Full v2 wrote three 15B caches, the complete NLL table, two checkpoint G0/G1 records, and a PASS terminal receipt in 175.65 s.
- Matrix count: 2 checkpoints × 4 batches × 2 conditions = 16 isolated optimizer updates; all 16 retained identical SAE state.
- Synthesis passed with 21 caches, 336 Fisher component rows, 144 15B paired component rows, 18 focused 10B paired rows, and 6 NLL comparisons.
- ACP marked `pt-d6swd6xd` `SUCCEEDED` at `2026-09-16T07:31:07Z`.

## Failed Attempts And Repairs

1. `pt-vyrf07oi`: original one-H100 Spot Smoke never allocated a worker and produced no pod log or scientific artifact. It was stopped after the researcher selected Reserved.
2. `pt-mwjknz0d`: first Reserved Smoke failed before an optimizer update because G0 omitted the source-required checkpoint-derived AuxK dead-feature mask. R002 repaired only that call contract; the failed root is `INELIGIBLE`.
3. `pt-eweyxti7`: fresh Reserved Smoke v2 passed and supplied the full-run gate.
4. `pt-tthi96r1`: full v1 failed during frozen NLL evaluation, before G0/G1, because an inference tensor was consumed outside an inference context. R003 placed the numerically identical linear projection and CE calculation under `torch.inference_mode()` with a detached weight view. A CPU equality regression passed. The failed root is `INELIGIBLE`.
5. `pt-d6swd6xd`: fresh full v2 passed; no partial artifact from a failed root was reused.

## Integrity And Eligibility

- Full persistent log SHA-256: `0d3f3c23cb6f0fd95255bee0e36f9457359682c0e90734968684e8a55a5b6417`.
- Terminal receipt SHA-256: `ee8db53bde3401efe5cb06cb56056859bba69a6fd9ceb01c735468b166352abf`.
- G0/G1 result SHA-256: `752ba503a9767faea25e8783c2e5c52201acec02439a0d0e36cf4ed5a34cc9ad`.

The successful Smoke certifies the runtime guards. Fresh full v2 and the PASS synthesis are `ELIGIBLE` for the Protocol's bounded local-gradient, local-utility, parameter, representation, and N-report claims. The failed attempts certify engineering history only. Execution success does not own the scientific judgment; the result wording remains `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`.
