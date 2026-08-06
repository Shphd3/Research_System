# round_continual_1 实验说明

## 1. 实验目标

- 用最小 two-task sequential forgetting test 更新 H4：
  - `quadratic_nosvd_debias` 的低 `SI` 是否真的转化为更低 forgetting
- 区分两种解释：
  - `acp_lite` 的一阶 mean-direction buffering 已经足够，quadratic 的低 `SI` 不会转化为更低 forgetting
  - `quadratic_nosvd_debias` 的低 `SI` 代表真实 anti-forgetting structure，因此在顺序学习中能更好保留旧任务性能

## 2. 当前实现口径

- 起始 checkpoint：`ckpt40000`
- 比较模型：
  - `linear_running_center`
  - `acp_lite`
  - `quadratic_nosvd_debias`
- 任务顺序：
  - `CS -> Medical`
  - `Medical -> CS`
- 数据来源：WOS 数据集中的 `abstract` / `domain`
- 训练任务定义：按 domain 子集做 causal LM 顺序训练
- 评测任务定义：对 held-out domain 语料计算 next-token `token_acc`
- CL 指标定义：
  - `Acc_A_after_A = token_acc(Task A eval | after stage A)`
  - `Acc_A_after_B = token_acc(Task A eval | after stage B)`
  - `Acc_B_after_B = token_acc(Task B eval | after stage B)`
  - `ΔAcc_A = Acc_A_after_B - Acc_A_after_A`
  - `Avg_after_B = (Acc_A_after_B + Acc_B_after_B) / 2`
  - `BWT = ΔAcc_A`
  - `Forgetting = Acc_A_after_A - Acc_A_after_B`

## 3. 代码结构

- 配置：`/data/250010109/spectral_router/exp_TRACE/configs/round_continual_1/ckpt40000_minimal.json`
- 数据准备：`/data/250010109/spectral_router/exp_TRACE/scripts/round_continual_1/prepare_round_continual_1_data.py`
- 训练总控：`/data/250010109/spectral_router/exp_TRACE/scripts/round_continual_1/run_round_continual_1.py`
- 单任务评测：`/data/250010109/spectral_router/exp_TRACE/scripts/round_continual_1/evaluate_round_continual_1.py`
- 指标汇总：`/data/250010109/spectral_router/exp_TRACE/scripts/round_continual_1/compute_cl_metrics.py`
- 训练入口复用：`/data/250010109/spectral_router/train_qwen3_moe.py`
- 模型加载复用：`/data/250010109/spectral_router/router_eval/eval_utils.py`

## 4. 输出目录

- 输出根目录：`/data/250010109/spectral_router/exp_TRACE/output/round_continual_1`
- 数据缓存：
  - `data/<Task>/train/data.jsonl`
  - `data/<Task>/eval/data.jsonl`
  - `data/manifest.json`
- 单次运行：
  - `runs/<model>/seed_<seed>/<TaskA>_to_<TaskB>/stage_a_train/`
  - `runs/<model>/seed_<seed>/<TaskA>_to_<TaskB>/stage_b_train/`
  - `runs/<model>/seed_<seed>/<TaskA>_to_<TaskB>/eval_after_a/`
  - `runs/<model>/seed_<seed>/<TaskA>_to_<TaskB>/eval_after_b/`
  - `runs/<model>/seed_<seed>/<TaskA>_to_<TaskB>/sequence_result.json`
- 汇总输出：
  - `summary/per_run_results.json`
  - `summary/per_sequence_summary.json`
  - `summary/overall_summary.json`
  - `summary/tables.md`

## 5. 运行方式

### 5.1 标准执行

```bash
python /data/250010109/spectral_router/exp_TRACE/scripts/round_continual_1/run_round_continual_1.py \
  --config /data/250010109/spectral_router/exp_TRACE/configs/round_continual_1/ckpt40000_minimal.json
```

### 5.2 仅汇总

```bash
python /data/250010109/spectral_router/exp_TRACE/scripts/round_continual_1/run_round_continual_1.py \
  --config /data/250010109/spectral_router/exp_TRACE/configs/round_continual_1/ckpt40000_minimal.json \
  --aggregate_only
```

### 5.3 干跑

```bash
python /data/250010109/spectral_router/exp_TRACE/scripts/round_continual_1/run_round_continual_1.py \
  --config /data/250010109/spectral_router/exp_TRACE/configs/round_continual_1/ckpt40000_minimal.json \
  --dry_run
```

## 6. 结果表模板

| Sequence | Model | Acc_A_after_A ↑ | Acc_A_after_B ↑ | Acc_B_after_B ↑ | ΔAcc_A ↑ | Avg_after_B ↑ |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| CS_to_Medical | linear_running_center | 待运行 | 待运行 | 待运行 | 待运行 | 待运行 |
| CS_to_Medical | acp_lite | 待运行 | 待运行 | 待运行 | 待运行 | 待运行 |
| CS_to_Medical | quadratic_nosvd_debias | 待运行 | 待运行 | 待运行 | 待运行 | 待运行 |
| Medical_to_CS | linear_running_center | 待运行 | 待运行 | 待运行 | 待运行 | 待运行 |
| Medical_to_CS | acp_lite | 待运行 | 待运行 | 待运行 | 待运行 | 待运行 |
| Medical_to_CS | quadratic_nosvd_debias | 待运行 | 待运行 | 待运行 | 待运行 | 待运行 |

## 7. 当前实现状态

- 已完成脚本落地
- 已完成目录与配置落地
- 已完成 session 文档落地
- 已完成训练入口对 `jsonl` 数据的支持
- 当前仍待正式运行完整训练与结果回写

## 8. 验证状态

- 新脚本已通过 `python -m py_compile`
- 四个入口脚本已通过 `--help` 参数检查
- 数据准备脚本已完成小样本 smoke 导出，产物位于：
  - `/data/250010109/spectral_router/exp_TRACE/output/round_continual_1_smoke/data`
