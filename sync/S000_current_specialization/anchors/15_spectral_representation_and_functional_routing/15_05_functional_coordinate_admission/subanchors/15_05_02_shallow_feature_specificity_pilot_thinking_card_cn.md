---
thinking_card_id: 15_05_02_shallow_feature_specificity_pilot
status: human_direction_approved_details_pending
human_language: zh
formalization_authorized: true
protocol_authorized: false
implementation_authorized: false
full_run_authorized: false
updated: 2026-07-30
---

# Thinking Card：四层浅层 head 指导 pilot

## 我的判断

- **具体现象：**研究者希望在受控四层模型中，让第 3、4 层使用第 2 层高方差
  部分训练，并与其他条件并行比较。
- **机制猜想：**如果第二层 head 已经稳定区分与深层专家兼容性相关的粗变量，
  该 side channel 可减少第 3、4 层的路由搜索成本。
- **最强替代解释：**`Unknown`，由 AI 提议后审核。
- **最不确定的一环：**浅层 head 的收益是否来自功能信息，而不是额外参数、
  特征能量、token identity 或负载变化。
- **什么证据会改变判断：**head 不超过同维 random 与 token-shuffle，或只在
  nuisance 任务获益，或匹配 FLOPs 后 held-out loss 无改善。
- **当前唯一决策：**逐项审核 pilot Approval Snapshot；不授权运行。

## AI 审核

- **最小 falsifier：**informative/nuisance 两任务下，先做独立 token 兼容性
  门，再做 head/random/shuffled 的匹配计算训练。
- **AI 建议实现：**第 1--2 层先形成并冻结表示；第 3--4 层使用 additive
  side channel，避免把“替换深层信息”与“增加浅层信息”混为一谈。
- **AI 建议：**`pursue`。

## 我的确认

- **已批准方向：**4 层；第 3、4 层使用第 2 层高方差部分；未来统一走
  8×5090 提交。
- **待确认：**以下 Protocol Snapshot 的全部配置与裁定规则。
- **是否允许实现或运行：**`no`。

