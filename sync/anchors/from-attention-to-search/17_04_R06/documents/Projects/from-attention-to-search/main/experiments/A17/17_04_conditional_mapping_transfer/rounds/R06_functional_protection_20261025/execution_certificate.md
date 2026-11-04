派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R06_functional_protection_20261025/execution_certificate.md`。
[精确原始文件](../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R06_functional_protection_20261025/execution_certificate.md)；研究修改仍回到原件。

---

# Execution certificate: A17 R06

Job: pt-f2wnbino. Status: RUNNING. Operator: current conversation /root, gpt-6.1-sol. One reserved H100, no quota expansion.

| Field | Actual value |
|---|---|
| AEC2 | share-cluster |
| ENVELOPE | docs/execution_envelope.md |
| EXECUTION_SURFACE | acp |
| GPUS | 1x H100 80GB |
| GPU_USED | true |
| IMAGE_CUDA | 12.4 |
| IMAGE_ID | shphd-lite-0911 |
| IMAGE_INTERPRETER | Python 3.10 |
| IMAGE_TORCH | 2.3 |
| IMAGE_URL | registry.cn-sh-01g.sensecore.cn/ccr-zhicheng-03/shphd-lite-0911:shphd-mig-20260910161423 |
| PRIORITY | normal |
| QUOTA_TYPE | reserved |
| RESOURCE_PROFILE | h100-1-reserved |
| STORAGE_MOUNT | 01995892-d478-76d8-aec7-13fd8284477e:/data |
| SUBMISSION_ENTRY_POINT | /data/250010109/MoE_Router/experiments/20260808_online_spectral_router_30b_v1/scripts/sco_acp_compat.sh |
| WORKER_NODES | 1 |
| WORKER_PROCESSES | 1 |
| WORKER_SPEC | n6ls.iu.i40.1 |
| WORKSPACE | share-space |

Activation: /data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/scripts/runtime.sh. Exact command: bash ops/run.sh. Submitted through templates/execution/acp_submit_template.sh with R05 SCO compatibility component. One job, zero retries.

Step0 oldDEV replay100%; new microbatch cache/native maxlogit error8.392333984375e-5, equalargmax, below frozen2e-4. Embedded numerical, TensorBoard and external-process step1->2 replay PASS before remaining training. Actual GPU/runtime from provenance/environment.json.

Training batch72input slots;36new and k old active targets; microbatch12, one process, accumulation6, denominator72. Extra64old probes in four16-example batches. Loss tokens are36+k, probe labels excluded and separately counted; curves compare36newtargets/update. Fresh AdamW1e-4, all moments retained after displacement filtering.

StartUTC: 2026-10-25T17:50:16.741554+00:00. Global14400sec budget, stop new training at13800sec. Main source/config/order/contracts freeze predates first new DEV evaluation and first update. Source paths/root/logs remain in execution root; tensorboard in runs/seed_*/old_*/METHOD/tensorboard. Full planned coverage36runs. No TEST, addition, SAE, CrossCoder or MoE.

## Terminal

COMPLETED at 2026-10-25T18:15:27.657718+00:00; 36/36 step240 runs, wallclock 1510.916sec. Frozen bytes unchanged, other model tensors unchanged; output family registered. TensorBoard tag-axis repair preserves originalevents; canonical reconstructedevents all checked.
