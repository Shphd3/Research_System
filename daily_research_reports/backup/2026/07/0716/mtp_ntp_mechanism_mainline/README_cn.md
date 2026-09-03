# MTP–NTP 机制主线：当前阅读入口

日期：2026-07-16

状态：理论澄清工作包；不是正式 anchor，也不是获批的实验 Protocol。

英文 companion：[README.md](README.md)

## 当前汇报主题

> **什么任务属性使 MTP 的提前监督在有限优化中可能优于 all-position NTP，
> 并且最终被标准 next-token 主头使用？**

更短的汇报标题：

> **MTP 什么时候真的需要“提前学”，而标准头又真的会用？**

## Keep in mind：只记五句话

1. all-position NTP 最终也会监督答案；MTP 的候选优势是更早的 direct credit，
   不是 NTP 永远看不到答案。
2. token distance 不是因果属性；核心是 local insufficiency、delayed
   counterfactual dependence 和 multi-evidence composition。
3. 提前形成信息不等于信息被运输，也不等于普通标准头因果使用。
4. MTP 可能有利的任务更像“确定性的状态 relay”，而不是抽象的 `code`
   标签；自然语言也可能具备，代码也可能不具备。
5. 当前没有有效 carrier：先冻结定义和 validity gate，再谈 NTP/MTP。

## 当前证据怎么放

| 来源 | 已支持 | 尚未支持 |
| --- | --- | --- |
| A11_01 | horizon 首次覆盖 informative target 时出现较早 direct signal | next-two 一般优于 next-one |
| A11_02 | direct path 可达共享参数，且在受控点可强于 later NTP component | full MTP 总梯度总是更好 |
| A11_03 | source K/V 可读；强 standard-head 信息特异 use 增量失败 | formation 自动成为标准头 use |
| A12 E04 | 当前 learner/carrier capability 和 row-removal validity 失败 | NTP/MTP 的组合能力高下 |
| 0713 录音 | 提出代码/规划、状态组合、可拆分表征和 MoE 的问题链 | 上述机制已经得到证明 |

项目角色不变：

- **A11：**future supervision 的 signal、reachability 与 use boundary；
- **A12：**compositional carrier validity；
- **A06：**最终 Router 的 held-out expert utility；
- **A07/common–rare：**保留为前一轮背景，不是本轮主要判据。

## 阅读顺序

1. [本轮理论澄清、命题、反例与九项 carrier gate](06_long_horizon_compositional_workload_theory_cn.md)
2. 本轮待研究者填写的 研究者判断记录
3. [前一轮 common/rare 理论](05_theory_clarification_and_meeting_anchor_cn.md)
4. [录音驱动的 low-hanging fruit](04_recording_driven_low_hanging_fruit_cn.md)
5. [广义 MTP/NTP 背景理论](01_general_mtp_vs_ntp_theory_cn.md)

## 当前唯一下一决定

> **先冻结 long-horizon/compositional 的操作定义与九项 carrier validity
> test；现有证据不足以直接进入 NTP/MTP Protocol。**

请先填写
researcher judgment record。
收到研究者判断前，不创建正式 anchor、Protocol、代码或实验，不更新 graph、
root sync，不 commit 或 push。
