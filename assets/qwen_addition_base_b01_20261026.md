# Qwen3 base-addition B01 LoRA states

The bounded base-only run passed its DEV gate at steps20 and40 and stopped at40. This is DEV-selected qualification, following exposed DEV errors; TEST and A/B were not measured. [Chinese guide](qwen_addition_base_b01_20261026_cn.md).

| Asset ID | Actual saved state | Progress |
|---|---|---|
| `adapter_qwen_addition_base_b01_20261026_seed20261025_initial` | zero-output LoRA plus initial recovery state | step0,0 tokens |
| `adapter_qwen_addition_base_b01_20261026_seed20261025_endpoint` | confirmed endpoint LoRA plus optimizer/RNG/data recovery state | step40,9,217 valid tokens,2,560 sample exposures |

Payload owner: `/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/base_training/b01_lora14_seed20261025/checkpoints/`. Both states require `model_qwen3_0p6b_base` and `tokenizer_qwen3_0p6b_base`; training data is `data_qwen_addition_qualification_20261025_seed20261025_v1`. These adapters contain no complete parent model.

Only zero-based block14 Q/K/V/O rank8/alpha16/dropout0 LoRA is present,81,920 FP32 parameters over frozen BF16 parent weights. Endpoint SHA-256: `e0b5321c343d88aac3c8118fb400086ee853f2157c58a12d53a3ad77ea1aecbb`. [Strict access receipt](checks/20261025T161625Z_qwen_addition_b01_actual_checkpoints.json) covers these two actual outputs.

[Chinese result](/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/base_training/b01_lora14_seed20261025/summary_cn.md), [config](/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/base_training/b01_lora14_seed20261025/config.json), and [loader](/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/base_training/b01_lora14_seed20261025/source/load_start.py) retain full identities and use boundaries. Future authorized branches must load the identical endpoint and initialize their optimizers uniformly afresh, without inheriting this run's Adam state. Same-task external-process exact resume is NOT_CHECKED; same-process state roundtrip and exact adapter reload passed. Registration/access grants no new execution authority.
