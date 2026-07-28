# A11_03_01_E02 桥接状态条件化端到端语义效率 Protocol

## 审核摘要

**问题：** A11_19 测到的桥接词方向差异，能否预测标准 H1 最终行动的有限步学习效率？

**条件：** `NTP/MTP × Decision/Therefore`，五个种子，固定 Qwen3-0.6B、任务、样本、batch 和 300 次更新。

**主指标：**

$$
\Delta_{int}
=\big(AUC_Q(MTP,Therefore)-AUC_Q(NTP,Therefore)\big)
-\big(AUC_Q(MTP,Decision)-AUC_Q(NTP,Decision)\big).
$$

**支持：** $\Delta_{int}>0$ 至少 `4/5`，`Therefore` 下 MTP 增量为正至少 `4/5`，且平均交互量为正。

**不支持：** 有效运行下，交互量至多 `2/5` 为正或平均值不为正。

**证据不足：** 初始配对、样本/batch、有限值、本地学习或完整性守卫失败。

**不能声称：** 一般预训练或真实 benchmark 上 MTP 已经优于 NTP。
