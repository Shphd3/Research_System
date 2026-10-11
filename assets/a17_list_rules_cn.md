# A17列表规则资产

数据ID `data_a17_list_rules_v1` 为实际生成并核验的5,600行发布，原始数据在执行侧。分词器输入为`model_qwen3_0p6b_base`；训练输入为`model_dense_33b`与`model_qwen3_0p6b_base`；只读能力输入为`model_s7_fresh_lambda0p1_33b`。两种未见分别标明；模型Smoke只读取train/dev。

实际Smoke保存状态已在文件核验后登记，不把计划当产物。当前全库v4快照仍为原日期范围；[A17访问快照](checks/2026-10-09_a17_inputs.json)只覆盖本次四项必需依赖。

[English](a17_list_rules.md)

## 实际Smoke状态

- `model_a17_list_rules_dense_smoke_20261009t152323z_u32`: update32/2,048答案；实际16/32家族见catalog；16外进程恢复通过，32恢复NOT_CHECKED。
- `model_a17_list_rules_qwen_base_smoke_20261009t152323z_u32`: update32/2,048答案；实际16/32家族见catalog；16外进程恢复通过，32恢复NOT_CHECKED。

[输出访问快照](checks/2026-10-09_a17_smoke_outputs.json)；GB权重hash未重新计算，科学结果NOT_EVALUATED。

## E02受限更新Smoke状态

修复job pt-i3ianttt工程64/64 PASS；首job pt-bw3s1pxw在update0恢复守卫失败，正式训练0步，其初始状态仍保留并登记。L直接矩阵与R8共享LoRA各两档LR，最终每臂50步/1000答案；catalog family明确列出实际0/1/2/4/8/16/32/50共8成员。state完整SHA256核验，8步外进程及连续第9步精确一致；最终50步重新载入NOT_CHECKED。均需原model_qwen3_0p6b_base、匹配数据/config/loader，不是完整LM权重。科学NOT_EVALUATED。

- `adapter_a17_e02_l_lrminus5_smoke_4h100_retry01_20261009t163401z_u50`
- `adapter_a17_e02_l_lrminus4_smoke_4h100_retry01_20261009t163401z_u50`
- `adapter_a17_e02_r8_lrminus5_smoke_4h100_retry01_20261009t163401z_u50`
- `adapter_a17_e02_r8_lrminus4_smoke_4h100_retry01_20261009t163401z_u50`

[实际终点访问](checks/2026-10-10_a17_e02_outputs_163838.json) · [失败零步状态访问](checks/2026-10-10_a17_e02_outputs_163214.json)。两者仅检查新输出，不替代原日期全库v4快照。
