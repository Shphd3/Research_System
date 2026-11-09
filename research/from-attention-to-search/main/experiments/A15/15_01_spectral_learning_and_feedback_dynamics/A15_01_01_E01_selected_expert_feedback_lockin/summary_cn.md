---
experiment_id: A15_01_01_E01_selected_expert_feedback_lockin
verdict: pass_feedback_lockin
completed: 2026-07-31
canonical_language: en
---

# 结果：已选专家反馈会锁定 head-first 分区

## 直接结果

**Pass。** 当 H/M/T 按生成真值共同决定损失最优专家时，只训练当前已选专家会
让 M/T 细分停在随机水平；每 token 计算量匹配的 oracle-functional coverage
则几乎恢复全部可读的 M/T 结构。

细粒度纠错准确率 \(C_{MT}\) 的含义是：head bit 已路由正确后，middle 与 tail bit
是否还能选对细专家。单位是\([0,1]\)准确率，不是语言模型loss或真实workload收益。

| step 6,000 结果 | selected-only | oracle coverage | 成对差值 |
| --- | ---: | ---: | ---: |
| \(C_{MT}\)种子中位数 | 0.500 | 0.977 | +0.477 |
| M-bit 纠错差 | — | — | +0.478 |
| T-bit 纠错差 | — | — | +0.477 |
| 八专家exact route | 0.244 | 0.933 | +0.689 |

\(\Delta C_{MT}\) 的paired-seed bootstrap 95%区间为\([0.476,0.479]\)，远高于
注册的0.10实质门槛。

## 为什么它能区分反馈机制

两主arm使用相同 Router 输入、初始head margin、在线batch、路由随机数、优化器、
每token两次专家前向和一次专家更新。唯一改变是谁获得更新：`selected_only`给
采样专家，`oracle_coverage`给损失最优专家。

32/32 selected-only种子中，早期正确challenger只获得0.030--0.049的合格更新，
低于四细专家下0.25的无饥饿参照；同时incumbent MSE比正确challenger低中位0.195。
这正是预注册的“incumbent效能优势+challenger饥饿”方向。

## 中心图

![功能覆盖恢复 middle/tail 纠错](figures/feedback_correction.png)

左图显示selected-only长期停在随机细分，而oracle coverage到达任务噪声上限；
右图32个成对种子全部高于0和0.10门槛。

## 运行有效性

- 32/32正式成对种子在单节点8×5090 SPOT上完成。
- 32/32有限数、计算匹配、初始head、oracle唯一性、监督可读性与成熟专家bandit
  护栏通过。
- 监督与成熟专家正控exact route约0.933，与解析Bayes上限
  \(\Phi(2)^3\approx0.933\)一致。
- 远程job `pt-15rmvipu`成功；每卡4个完整paired seeds。

## 认识更新与边界

本实验建立的是充分性结论：

> 在低方差变量确实有用的受控MoE中，selected-expert co-adaptation能够通过
> incumbent变强和细专家饥饿，保留早期head-only分区。

它不能证明自然DCLM的M/T有用、该机制已造成某个真实checkpoint，或oracle coverage
可部署。唯一下一决策是在已知层级变量的四层受控模型中，用稀疏challenger或
counterfactual coverage复核该反馈机制。
