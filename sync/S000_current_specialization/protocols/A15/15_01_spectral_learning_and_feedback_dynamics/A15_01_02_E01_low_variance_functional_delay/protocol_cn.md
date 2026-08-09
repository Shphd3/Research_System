---
experiment_id: A15_01_02_E01_low_variance_functional_delay
anchor_id: 15_01_02_low_variance_functional_delay
status: approved_full_execution
execution_status: completed_weak_pass_delay_strong_fail
formal_job_id: pt-15rmvipu
canonical_language: en
approved_by: researcher_blanket_authorization
approved_at: 2026-07-31
---

# Protocol：H/M/T 路由的功能稳定性

## 0. Approval Snapshot

研究者已授权自主正式化、实现、单节点8卡运行与结果收口。本 Protocol 在正式种子
运行前批准；未授权 graph edit、root publication、commit 或 push。

## 1. Decision Question

在标准化信噪比匹配时，原生低方差 tail 在注册时限内是否功能上接近随机，还是
经过方差造成的延迟后最终会同时达到正确和持续？

## 2. Hypotheses And Rival

**强H1：** native T 到时限仍未通过，表现接近匹配无标签随机对照；equal-energy
T 则达到功能稳定。

**弱H1：** native 三带最终都通过，但功能稳定时间满足$H<M<T$，均衡后延迟
大幅缩小。

**最强rival：** tail漂移只因在正确率形成前观察raw churn；它含同等可学信息，
只是延迟而非随机化。

## 3. Synthetic Data Contract

- 平衡二分类标签 $z\in\{-1,+1\}$。
- 三个独立8维信号 block：$x_b=s_b(zv_b+0.5\epsilon_b)$，
  $(s_H,s_M,s_T)=(4,2,1)$。
- 固定正交信号方向与成对在线 minibatch。
- 每种子先冻结8,192个 held-out 样本。
- 无标签对照使用相同维度/尺度的独立高斯噪声，不含 $zv_b$。
- 数学允许处，native/equal/random 复用标签与paired random stream。

## 4. Model And Optimization Contract

- 每个条件一个独立、无bias二分类线性Gate。
- 初始权重范数固定为1.0，方向由种子随机决定。
- SGD，无momentum/weight decay，学习率$10^{-3}$。
- BCE，batch 512，FP32。
- 正式时限4,000步，每20步评估（含0）。
- equal-energy将M/T分别乘2/4达到H幅度；native H直接复用为equal H。
- 只有4,000步仍删失的native T允许继续到12,000步；这是注册边界诊断，不能把
  强时限Fail改成强Pass。

## 5. Conditions

| family | H尺度 | M尺度 | T尺度 | 标签信息 |
| --- | ---: | ---: | ---: | --- |
| native | 4 | 2 | 1 | 同一$z$，标准化SNR匹配 |
| equal_energy | 4 | 4 | 4 | 同一$z$，标准化SNR匹配 |
| random | 4 | 2 | 1 | 无标签、尺度匹配噪声 |

逻辑上是`native/equal/random × H/M/T`九条件；native/equal H共享同一轨迹，不
重复计数。

## 6. Primary Metric

固定held-out上，$A_b(k)$是二分类正确比例；$F_b(k)$是相对上一次评估预测发生
变化的比例。连续三次满足$A_b\ge0.90$且$F_b\le0.02$的首次step为功能稳定
时间。未通过者在4,000步右删失。

报告通过比例、可定义时的Kaplan--Meier中位数，以及$[0,4000]$内restricted
mean time to stability。单位是optimizer step；不能证明语义或专家效用。

## 7. Secondary Metrics

- 完整accuracy/flip曲线。
- 学得权重与真值信号方向的cosine-squared。
- 最终accuracy、flip、logistic loss、weight norm。
- native带间与equalized-minus-native的成对时间差。
- 被删失native T的长时限通过时间。
- 随机曲线只校准null，不是候选有用Router。

## 8. Controls And Hard Guards

1. equal-energy H/M/T每个都至少30/32种子在4,000步通过。
2. 每个无标签随机频带的最终平均准确率在$[0.47,0.53]$，误通过不超过2/32。
3. native/equal配对共享标签、基础噪声、held-out和初始权重方向。
4. 各信号条件step-0模型中位准确率在$[0.35,0.65]$，且没有频带起始已稳定。
5. 所有正式种子的loss、梯度与权重有限。

## 9. Seeds And Statistical Unit

- 本地smoke：9200、9201。
- 分布式smoke：9210--9217，每卡一个。
- 正式：2000--2031，每卡四个完整种子。
- 统计单位是种子，评估样本与时间点不是独立重复。
- 32个正式种子必须全部完成，不得静默过滤或替换。

## 10. Execution Stages

1. S0：数据方差/SNR、paired scaling、随机标签独立、flip、连续通过和删失单测。
2. S1：本地smoke验证正负控，不调LR。
3. S2：8卡smoke验证rank ownership与确定性合并。
4. S3：8卡正式运行32种子至4,000步。
5. S4：只延长仍删失native-T种子。
6. S5：合并、生存汇总、paired bootstrap、图和typed verdict。

## 11. Pass, Fail, Partial, And Insufficient Rules

**强Pass（有限时限tail随机化）：** 全护栏通过；至少24/32 native-T在4,000步
删失；其最终准确率与random-T均值差<0.05；至少30/32 equal-energy-T通过。
长时限恢复仍必须报告。

**弱Pass/强命题Fail（只有延迟）：** 全护栏通过；至少26/32 native-T在4,000
或12,000步通过；native restricted mean满足$H<M<T$且H-to-M、M-to-T成对
bootstrap为正；equal-energy T将restricted mean至少降低50%。这支持有限时间
延迟并否定tail随机化。

**Fail：** 护栏通过但既无强随机模式，也无稳定有序延迟。

**Insufficient：** 任一硬护栏失败、正式种子不足32、配对破坏或数值失败。
若“注册时限随机样”与“更晚恢复”同时存在，typed verdict必须同时写出。

## 12. Figure Contract

中心图用accuracy和flip两个panel画native H/M/T、equal-energy T与random T，
显示种子中位数和95% bootstrap带；横线标0.90/0.02，图例写删失比例。它区分
正确持续、延迟纠正和稳定错误随机路由，不能证明语义专门化。

可补未达到功能稳定比例的生存图；时间单位optimizer step，终点明确标删失。

## 13. Artifact And Evidence Contract

worker保存代码、测试、精确配置、环境、rank-local轨迹、合并表、日志和远程metadata。
Research System只保存Protocol、summary、detailed、中心图与紧凑表。详细账本拥有
所有seed轨迹、删失决定、护栏、命令、job ID、hash和artifact link。

## 14. Execution Authorization And Stop Rule

实现、smoke、8卡正式运行和注册延长均已授权。smoke失败可修复实现，但不能修改
指标、门槛、LR、种子或数据。若当前合同下正控不可能通过，必须停并报告
`insufficient`，不得为H1调参。完成后直接写证据、更新Anchor并写入0731唯一focus。
