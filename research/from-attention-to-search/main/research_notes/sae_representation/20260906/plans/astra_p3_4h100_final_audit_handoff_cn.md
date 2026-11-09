# 给 Astra 的草稿：P3 四卡 512-only 完成结果独立复核

状态：`DRAFT_FOR_ASTRA_REVIEW`。这是一份供独立复核的交接草稿，不是 canonical
`summary.md` / `detailed.md`，也不代表研究者已经确认结果认识或下一决策。

## 请解决的唯一任务

请对 `A15.gmm_pseudolabel_oracle_gap` 的 P3 完成运行做一次独立的合同一致性、证据资格和
注册裁决复核。先从原始逐记录测试数组重算四个主效应，再判断机器裁决
`INSUFFICIENT` 是否正确。不要沿用 Sol 的解释作为证据，不新增实验，不运行
H-hard/H-oracle，也不要更新 Focus、Anchor、PROJECTS、Graph、Git 或外部同步。

## 科学问题和裁决边界

问题：从共同冻结 Qwen3-0.6B-Base 重新训练时，训练集拟合的真实层级伪标签监督
H-sem，是否在两个 seed 上同时降低在线参考答案 NLL，相对同架构 H-task 和保持合法
标签频数但打乱记录对应的 H-shuf？主指标单位为 nat / answer token，正差值表示 H-sem
更好。

注册规则：每个 seed 分别计算 `H-task - H-sem` 和 `H-shuf - H-sem`，用 2,000 次按来源
分层、整记录配对 bootstrap 得到 95% percentile interval。四个区间下界全部大于零才
Pass；某一个同名必要比较在两个 seed 的上界均不大于零才 Fail；其余合格模式均为
Insufficient。

不能宣称：伪标签是真实语义、教师层位最优、层级结构必要、专家不可互换、自由生成
改善、或公开基准无预训练污染。

## 必读来源

1. Focus：`Projects/from-attention-to-search/main/focus/focus_gmm_pseudolabel_handoff.md`
2. Anchor：`Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_05_gmm_pseudolabel_oracle_gap_anchor.md`
3. Protocol 与追加修订：`Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P3_matched_training_semantic_comparison/protocol.md`
4. Worker run：`/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p3_matched_training/runs/full-20260906T170500Z`
5. 运行后独立审计：`receipts/acp_and_postrun_audit.json`
6. 预审与正式回执：`receipts/preflight.json`、`receipts/formal.json`
7. 主效应：`analysis/primary_semantic_effects.csv`
8. 测试 NLL：`analysis/test_nll.csv`
9. 架构参照：`analysis/architecture_effects.csv`
10. 机器裁决与 artifact 哈希：`analysis/verdict.json`、`artifact_manifest.json`

以上第 5--10 项路径均相对于 Worker run。

## 实际执行事实

- ACP job：`pt-86wcqrbi`，2026-09-06 18:05:44 UTC 提交，18:57:28 UTC
  `SUCCEEDED`；单节点 `n6ls.iu.i40.4`，4×H100 80GB，reserved，retry 0。
- Amendment `20260906-P3-A1` 在恢复执行前由研究者批准：条件级最大并发 4，预算只允许
  512；若 384→512 注册触发器命中则预算不足并停止，不再跑 1024。
- 修订发生时只有数据/教师、smoke 与 D seed17 的 update-224 recovery 可见；尚无
  update-384/512 开发结果、load 选择、正式 checkpoint 或测试输出。
- D seed17 从原子 recovery 恢复；最终 12 个核心条件全部完成 512 updates。每条历史均为
  连续的 update 0--512，并有开发归档 0/128/256/384/512。
- 四基线 384→512 改善为 0.0000945--0.0001711，均低于 0.002 触发阈值，排序未触发；
  预算资格通过。
- H-task 虽存在负载集中，但没有 dead expert，且注册的 undertraining 条件未命中，因此
  不触发 load-on；最终政策为 load-off。
- 六个最终 H 条件的 384→512 改善为 0.0000441--0.0002179，均未命中 0.002 稳定性规则。
- 测试在全部稳定性检查后解封。12/12 测试数组均有 8,481 条记录和 562,954 个答案词元；
  record ID、source、token count 在条件间完全配对，且所有数值有限。
- 12/12 eligibility guards 通过；两个 seed 内 H-task/H-sem/H-shuf 初始张量哈希分别完全
  相同；57/57 artifact manifest 哈希复核匹配；无失败 condition 或异常日志。

## 需要重算的主结果

| Seed | 比较，正值支持 H-sem | 点差 | 95% CI | 直接观察 |
| ---: | --- | ---: | --- | --- |
| 17 | H-task − H-sem | +0.010320 | [0.009795, 0.010890] | H-sem 更低 |
| 17 | H-shuf − H-sem | +0.014645 | [0.014138, 0.015128] | H-sem 更低 |
| 29 | H-task − H-sem | −0.002078 | [−0.002469, −0.001680] | H-task 更低 |
| 29 | H-shuf − H-sem | +0.005467 | [0.005064, 0.005837] | H-sem 更低 |

测试 NLL 的最小必要核对：seed17 的 H-task/H-sem/H-shuf 分别为
0.686567/0.676247/0.690892；seed29 分别为 0.676168/0.678246/0.683713。

机器裁决为 `INSUFFICIENT`：H-sem 相对 H-shuf 在两 seed 都更好，但相对 H-task 的方向
在 seed17 为正、seed29 为负。它不满足四下界全正的 Pass，也不满足任一同名比较在两个
seed 都稳定反向的 Fail。

## 架构参照边界

F 相对 D 在两个 seed 均降低 NLL（+0.067174、+0.057843，正值支持 F）。但 SF 相对 F
以及 H-task 相对 SF 均发生 seed 方向反转：SF−F 的对应注册差为 +0.002468 / −0.005918；
SF−H-task 为 −0.003611 / +0.022849。因此只能把 F 优于 D 作为本设置内稳定描述，不能从
其余排名推出共享容量或层级结构的普遍优势；不同架构的存储参数、共享方式、门控深度和
缩放仍是混杂因素。

## 请 Astra 输出

1. 一张 Protocol conformance/deviation 表，特别审核 amendment 时点、D update-224 恢复、
   512-only 对资格的影响、preflight checkpoint 复用、测试解封顺序和四卡条件并行隔离。
2. 从 12 个 `.npz` 重算 pooled token-weighted NLL，并独立重跑 source-stratified paired
   bootstrap；报告是否逐位复现四个点差、区间和 typed verdict。
3. 分开写：直接结果、你的解释、可支持 claim、不能 claim、以及最强未解 rival。不要用
   H-sem 对 H-shuf 的两 seed 优势覆盖 H-task 比较的 seed disagreement。
4. 给研究者一个 closed-book judgment scaffold，等待研究者确认或修正后再写 canonical
   `summary.md` / `detailed.md` 和 Anchor/Focus 更新。
5. 将 H-hard/H-oracle 记为 `NOT_RUN_NOT_TRIGGERED`：核心结果虽非 Pass，但“下一决策确需
   分解 teacher value 与 online handoff”尚未由研究者确认，因此条件授权的第二部分未满足。

AI 建议供复核而非代替研究者决定：下一步先判断 seed29 的 H-task 反向是否值得做一个
严格复现性审计；在该判断前，不因 H-shuf 对照为正就升级为“语义监督有效”，也不自动
开放 privileged-path 分支。
