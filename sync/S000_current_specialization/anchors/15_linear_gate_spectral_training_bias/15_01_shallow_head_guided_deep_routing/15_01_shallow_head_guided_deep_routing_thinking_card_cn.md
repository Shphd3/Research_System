---
thinking_card_id: 15_01_shallow_head_guided_deep_routing
status: human_direction_approved_details_pending
human_language: zh
formalization_authorized: true
protocol_authorized: false
implementation_authorized: false
full_run_authorized: false
updated: 2026-07-30
---

# Thinking Card：浅层 head 指导深层 Router

## 我的判断

- **具体现象：**组会提出使用前面层已经形成的高方差信息指导后面层分发；这与
  使用本层 middle/tail 分发是两个相反且必须分开的机制。
- **机制猜想：**浅层 head 可能较早形成稳定的粗粒度领域或共同结构；将同一
  token 的浅层 head 系数提供给深层 Gate，可能减少路由抖动，让深层专家更早
  接收兼容 token。
- **最强替代解释：**`Unknown`。研究者要求 AI 提出后逐项审核。
- **最不确定的一环：**高方差是否真是深层专家兼容性的增量信息，而不是位置、
  长度、公共语义或负载集中信号。
- **什么证据会改变判断：**控制深层 native Router 分数、参数、负载、容量和
  token 数后，浅层 head 不能超过同维随机、token-shuffle 或 nuisance 对照；
  或虽然路由更稳定，却不改善匹配 FLOPs 的 held-out loss。
- **当前唯一决策：**审核受控四层 pilot 的 subanchor 与 Approval Snapshot；
  未批准实现和 8×5090 运行。

## AI 审核

- **最强活跃 rival：**收益来自额外参数、边际尺度、负载变化或共享 token
  identity，而不是浅层 head 的 token-specific 功能信息。
- **隐藏假设：**浅层 $U_{2,H}$ 不能直接投影深层 $g_3/g_4$；合法对象必须是
  同一 token 在第二层的系数 $U_{2,H}^\top(g_2-\mu_2)$，或另行定义 transport。
- **最小区分实验：**先在受控任务上比较 head、同维随机和 token-shuffled
  side channel；用独立 token 组的一步兼容性作为训练硬门。
- **AI 建议：**`pursue`，但先固定前两层和第二层基底，避免表示漂移与功能
  价值同时变化。

## 我的确认

- **已批准方向：**四层受控模型，第 3、4 层使用第二层高方差信息；未来统一
  通过 8×5090 提交，但必须先批准 Protocol。
- **待逐项确认：**side-channel 形式、受控任务、对照、能力门、主训练指标、
  seed 和预算。
- **是否允许实现或运行：**`no`。

