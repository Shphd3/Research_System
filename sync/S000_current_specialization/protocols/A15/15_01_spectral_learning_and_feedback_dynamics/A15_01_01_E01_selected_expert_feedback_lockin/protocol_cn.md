---
experiment_id: A15_01_01_E01_selected_expert_feedback_lockin
anchor_id: 15_01_01_selected_expert_feedback_lockin
status: approved_full_execution
execution_status: completed_pass_feedback_lockin
formal_job_id: pt-15rmvipu
canonical_language: en
approved_by: researcher_blanket_authorization
approved_at: 2026-07-31
---

# Protocol：已选专家反馈与 M/T 路由纠错

## 0. Approval Snapshot

研究者已明确授权两个0731 conjecture 自主完成 Anchor、Protocol、实现、远程运行
与结果收口。本 Protocol 在正式种子运行前批准。operationalization 种子只能在
预注册数值网格中选择，不进入科学证据。

正式运行前修订：噪声SD=0.5时，单比特Bayes准确率为$\Phi(2)$，八专家exact
route的解析上限是$\Phi(2)^3\approx0.933$，原0.95监督门不可能达到。在查看任何
正式种子或主arm结果前，护栏修正为“至少0.90且距离解析上限不超过0.02”。数据、
arms、主指标、效应门槛和正式种子均未改变。

授权资源为一个8卡5090 SPOT节点；未授权 graph edit、root publication、commit
或 push。

## 1. Decision Question

当 H/M/T 都是损失最优专家不可缺少的真值变量时，相比每 token 一次更新的
oracle-functional coverage，只训练当前已选专家是否会压制后续 M/T 路由纠错？

## 2. Hypothesis And Strongest Rival

**H1：** head-first 路由训练 incumbent、饿死正确细粒度 challenger，由此形成
效能反馈闭环并降低 M/T 纠错。

**最强 rival：** M/T 只因输入方差而学得慢；当 Router 过程和专家更新数固定时，
改变专家覆盖不会实质改变最终分区。

主对照不改变 Router 输入能量，只改变专家更新接收者。

## 3. Synthetic Data Contract

- 独立平衡 $h,m,t\in\{-1,+1\}$；oracle expert 为
  $e^*=4\mathbf1[h=1]+2\mathbf1[m=1]+\mathbf1[t=1]$。
- 三个独立8维频带：$x_b=s_b(bv_b+0.5\epsilon_b)$，
  $(s_H,s_M,s_T)=(4,2,1)$。
- Router 共24维；三带标准化信噪比相同。
- payload/target 均8维，$p\sim\mathcal N(0,I)$。
- 八个固定正交目标映射 $A_e$ 由 seed `20260731` 一次生成，$y=A_{e^*}p$。
- 训练数据在线生成；每种子先冻结16,384个 held-out 样本，永不用于优化。
- 训练用随机 top-1；评估用确定性 argmax。

## 4. Model And Optimization Contract

- Gate：线性 $24\rightarrow8$，带 bias。
- 专家：八个独立线性 $8\rightarrow8$，零初始化。
- Gate 初始化：正确 head 半区内所有专家获得相同 head 权重`0.35`；每个 head
  半区一个注册 incumbent 的 bias 为`1.5`；其余参数用 paired seed 的 SD=0.01
  小噪声。
- Router：带 batch-mean baseline 与熵正则的 selected-loss policy gradient，
  Adam 优化。
- Expert：MSE，SGD、无 momentum。
- batch 512；正式训练6,000步；每100步评估（含step 0）。
- 每 token 都执行一次已选专家前向供 Router 反馈，另一次更新接收者前向；即使
  二者相同也按两次路径计数。两因果 arm 都只有一次专家 backward/update。
- FP32 梯度；任意非有限 loss/参数/梯度使种子无效，若需替换则整体 insufficient。

operationalization 网格：Router LR $\{3\times10^{-3},10^{-2}\}$，Expert LR
$\{10^{-2},3\times10^{-2}\}$，entropy $\{0.01,0.03\}$。只用9000/9001种子，
选择同时通过两个正控、loss有限、step-0 head准确率>0.95的字典序最小组合；正式
运行前写入 `selected_config.json`。

## 5. Conditions

| 条件 | Router 反馈 | 获得唯一专家更新者 | 作用 |
| --- | --- | --- | --- |
| selected_only | 采样专家损失 | 采样专家 $a$ | 原生反馈 treatment |
| oracle_coverage | 采样专家损失 | 真值专家 $e^*$ | 因果覆盖对照 |
| oracle_experts_bandit | 采样专家损失 | 无；固定 $W_e=A_e$ | bandit 正控 |
| supervised_router | 对 $e^*$ 的交叉熵 | 无 | H/M/T 可读性正控 |

只有前两组进入主效应；正控自身不能产生科学 Pass。

## 6. Primary Metric

从 held-out argmax expert 解码 $(\hat h,\hat m,\hat t)$：

$$
C_{MT}=\tfrac12[\Pr(\hat m=m\mid\hat h=h)+
\Pr(\hat t=t\mid\hat h=h)].
$$

它表示早期已正确的 head 粗分区是否被两个低方差变量进一步细分，不能代表语言
模型收益。主效应为step 6,000时

$$
\Delta C_{MT}=C_{MT}^{oracle\ coverage}-C_{MT}^{selected\ only}.
$$

报告种子中位数、均值与10,000次 paired-seed bootstrap 95%区间；实质门槛为
0.10绝对准确率。

## 7. Mechanism And Secondary Metrics

- oracle expert exact route accuracy，以及 M/T 分量准确率。
- 正确专家更新份额。
- challenger starvation：初始误送 incumbent 的样本中，正确非-incumbent
  获得的更新比例；每个head半区有四个细专家，因此低于0.25是注册方向门。
- utility gap：held-out 反事实评估的 incumbent MSE 减正确 challenger MSE；
  负值表示 incumbent 当前更好，能够强化锁定。
- Router entropy/load/head accuracy、selected loss、专家更新与前向计数。
- 时间曲线只作解释，不能替代最终主对比。

## 8. Controls And Hard Guards

1. 两主 arm 成对复用 batch、held-out、Gate/专家初始化和采样随机数。
2. 每 token 活跃专家更新数与注册前向数必须完全匹配。
3. `supervised_router` 必须在2,000步前达到至少0.90，且距离解析Bayes上限
   $\Phi(2)^3$不超过0.02。
4. `oracle_experts_bandit` 必须在6,000步达到 exact route accuracy $\ge0.85$。
5. step 0 head准确率 $\ge0.95$，M/T 准确率分别在$[0.40,0.60]$。
6. 八种真值映射上，oracle expert 必须是唯一期望MSE最小者。

## 9. Splits, Seeds, And Statistical Unit

- operationalization：9000、9001，只选数值设置。
- 分布式 smoke：9100--9107，每卡一个。
- 正式：1000--1031，每卡四个完整种子。
- 统计单位是种子，不是 minibatch 或样本。
- 只有32个成对种子与所有条件齐全才合并；不得静默丢弃或替换失败种子。

## 10. Execution Stages

1. S0：标签、正交映射、expert-bit解码、更新接收者、paired random stream、指标单测。
2. S1：本地非claim种子选择配置并冻结hash。
3. S2：本地单种子与8卡分布式smoke。
4. S3：一个8卡正式作业完成32种子。
5. S4：确定性合并、护栏、bootstrap、图表和typed verdict。

S1/S2 checkpoint 不进入 S3。

## 11. Pass, Fail, And Insufficient Rules

**Pass：** 全护栏通过；$\Delta C_{MT}$ 的paired-bootstrap下界>0；中位效应
$\ge0.10$；M和T分量均为正；至少24/32 selected-only种子出现注册的早期
“incumbent更优/challenger饥饿”方向。

**Fail：** 护栏通过，但区间跨0、中位效应<0.10，或M/T任一未改善。

**Insufficient：** 正控失败、计算/数据配对失败、非有限数、正式种子不足32，
或无法排除额外计算。低于0.10的正效应只作次门槛观察。Pass也不授权真实DCLM结论。

## 12. Figure Contract

中心图左侧画 selected-only/oracle coverage 的 held-out $C_{MT}$ 随step变化，
用种子中位数和95% paired-bootstrap带；右侧画最终逐种子 $\Delta C_{MT}$，标注
0与0.10。它回答专家覆盖是否改变M/T纠错，不能回答真实workload收益。

机制图可画正确challenger更新份额和 incumbent-minus-challenger MSE，只作解释。

## 13. Artifact And Evidence Contract

worker保存代码、测试、精确配置、环境、rank-local JSON/NPZ、合并CSV、日志与
job metadata。Research System只保存Protocol、summary、detailed、中心图和紧凑表。
`detailed.md`记录命令、job ID、hash、失败、护栏、完整seed表和artifact map。

## 14. Execution Authorization And Stop Rule

实现与完整运行已授权。S0/S1若无法在注册网格内通过正控，应停止科学运行。
实现bug可修复并留账；正式作业不得改变数据、指标、门槛、种子或超参数。
正式完成后无论正负都写结果、更新Anchor和0731唯一日常认识面，不再中间请示。
