# A17 List-Rule Assets

Dataset `data_a17_list_rules_v1` is a generated and qualified 5,600-row release, stored in execution. Tokenizer input `model_qwen3_0p6b_base`; training inputs `model_dense_33b`, `model_qwen3_0p6b_base`; capability-only input `model_s7_fresh_lambda0p1_33b`. Both order-new and combination-new panels are explicit; model Smoke uses train/dev only.

Actual Smoke checkpoints are registered after saved files were verified. Scope is engineering, not scientific confirmation. Current whole-library counts/access remain dated in the existing v4 snapshot; A17 scoped snapshots cover named dependencies only.

[中文](a17_list_rules_cn.md) · [A17 scoped access](checks/2026-10-09_a17_inputs.json)

## Actual Smoke states

- `model_a17_list_rules_dense_smoke_20261009t152323z_u32`: update32/2,048 answers; actual16/32 family in catalog; external-process restore from16 qualified;32 restore NOT_CHECKED.
- `model_a17_list_rules_qwen_base_smoke_20261009t152323z_u32`: update32/2,048 answers; actual16/32 family in catalog; external-process restore from16 qualified;32 restore NOT_CHECKED.

[Output access snapshot](checks/2026-10-09_a17_smoke_outputs.json); GB payload SHA256 NOT_COMPUTED; science NOT_EVALUATED.

## E02 restricted-update Smoke states

Repaired job pt-i3ianttt completed engineering PASS64/64 after first job pt-bw3s1pxw failed at update0 with zero trajectory updates. Both original matrices L and shared rank8 LoRA factors R8 were saved, each at two LRs. Final selected state is update50/1000 answers per arm; each catalog family explicitly lists eight actual0/1/2/4/8/16/32/50 members. Exact state SHA256 verified; independent-process restore at8 plus uninterrupted-next-update9 exact parity qualified. Final50 restore NOT_CHECKED. All states require original model_qwen3_0p6b_base and the registered data/config/loader. They are restricted states, not complete LM weights. Science NOT_EVALUATED.

- `adapter_a17_e02_l_lrminus5_smoke_4h100_retry01_20261009t163401z_u50`
- `adapter_a17_e02_l_lrminus4_smoke_4h100_retry01_20261009t163401z_u50`
- `adapter_a17_e02_r8_lrminus5_smoke_4h100_retry01_20261009t163401z_u50`
- `adapter_a17_e02_r8_lrminus4_smoke_4h100_retry01_20261009t163401z_u50`

[Actual final-state access](checks/2026-10-10_a17_e02_outputs_163838.json) · [Actual failed zero-state access](checks/2026-10-10_a17_e02_outputs_163214.json). These scoped snapshots do not replace the dated whole-library v4 snapshot.
