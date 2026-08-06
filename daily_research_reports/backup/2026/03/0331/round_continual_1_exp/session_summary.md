# round_continual_1 Session Summary

## 用户 Request

- 用户要求基于当前理论状态，把最小 Continual Learning 实验真正落地到 `exp_TRACE`
- 用户指定模型加载过程参考 `exp_expert_lowrank/scripts/round0`
- 用户要求把本轮 session 的 request 与回复完整记录到 `exp_TRACE/docs`
- 用户指定本轮迭代命名为 `round_continual_1`

## 本轮回复与执行总结

- 已在 `exp_TRACE` 下建立 `round_continual_1` 的完整目录骨架：
  - `configs/round_continual_1/`
  - `scripts/round_continual_1/`
  - `docs/round_continual_1/`
- 已实现数据准备脚本，用 WOS 的 `abstract/domain` 导出 `CS` 与 `Medical` 两个任务的 train/eval JSONL
- 已实现最小 sequential CL 总控脚本，支持：
  - 数据准备
  - Stage A 训练
  - Stage B 训练
  - after A / after B 评测
  - `ΔAcc_A / Avg_after_B / BWT / Forgetting` 汇总
- 已实现评测脚本，模型加载复用 `router_eval/eval_utils.py` 的 `load_moe_model`
- 已修改训练入口 `train_qwen3_moe.py`，新增 `jsonl` 数据支持，避免只能依赖二进制训练集
- 已补充 `exp_TRACE/README.md` 与 `experiment_report.md`
- 已完成 smoke 级数据准备验证，成功导出 `CS` 与 `Medical` 的小样本 train/eval JSONL

## 关键实现选择

- 本轮把 `Acc` 的工程口径具体化为 held-out domain 语料上的 next-token `token_acc`
- 本轮任务 A/B 的训练数据定义为 WOS 中 `CS` 与 `Medical` 的 domain 子集
- 本轮沿用最小 sanity test 思路，不直接接 TRACE benchmark 主流程

## 关键路径

- README：`/data/250010109/spectral_router/exp_TRACE/README.md`
- 配置：`/data/250010109/spectral_router/exp_TRACE/configs/round_continual_1/ckpt40000_minimal.json`
- 总控：`/data/250010109/spectral_router/exp_TRACE/scripts/round_continual_1/run_round_continual_1.py`
- 数据准备：`/data/250010109/spectral_router/exp_TRACE/scripts/round_continual_1/prepare_round_continual_1_data.py`
- 评测：`/data/250010109/spectral_router/exp_TRACE/scripts/round_continual_1/evaluate_round_continual_1.py`
- 汇总：`/data/250010109/spectral_router/exp_TRACE/scripts/round_continual_1/compute_cl_metrics.py`
- 实验说明：`/data/250010109/spectral_router/exp_TRACE/docs/round_continual_1/experiment_report.md`
- smoke 数据输出：`/data/250010109/spectral_router/exp_TRACE/output/round_continual_1_smoke/data`

## 当前状态

- 已完成代码与文档落地
- 已完成 `py_compile`、`--help` 与小样本数据导出验证
- 待正式启动训练后回写数值结果与 H4 更新结论
