# Qwen3 addition qualification dataset

Only zero-update DEV measurement was executed. The strict-output basic-task gate failed; training and TEST inference were not run.

- Dataset ID: `data_qwen_addition_qualification_20261025_seed20261025_v1`.
- Payload: `/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/data`.
- Seed: 20261025. Inputs are integers 10–99 with equal pairs allowed. Split 2,400/300/300 unordered pairs before generating base/A/B tasks; sums may overlap.
- Parent model/tokenizer: `model_qwen3_0p6b_base` / `tokenizer_qwen3_0p6b_base`.
- Generator, complete distributions, byte hashes, and Chinese execution records remain with the execution package. See the [Chinese guide](qwen_addition_qualification_20261025_cn.md).

Data bytes were frozen and verified before inference, but registry addition was completed afterward. TEST was generated, hashed, and checked for pair overlap; no TEST tokenizer/model call occurred. No adapters or trained checkpoints were produced. Accessibility grants neither future execution approval nor scientific eligibility.
