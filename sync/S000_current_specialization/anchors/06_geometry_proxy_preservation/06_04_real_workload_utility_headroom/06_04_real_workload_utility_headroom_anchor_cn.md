# A06_04：真实工作负载中的专家效用余量

状态：当前待审核 anchor；尚未批准 protocol 或实验。

Thinking Card source: [06_04_real_workload_utility_headroom_thinking_card_cn.md](06_04_real_workload_utility_headroom_thinking_card_cn.md)

## 审核边界

- 代码语言、接口族和跨文件依赖只用于分层，不是正确专家标签。
- 样本不得按专家效用或多词元预测语义延迟预筛选。
- 本 anchor 只判断真实工作负载是否存在可捕获的专家功能异质性，不设计新 gate，不训练多词元预测目标，不声称下游加速。
- 唯一下一决策是：是否批准最小的 held-out 功能余量 protocol。
