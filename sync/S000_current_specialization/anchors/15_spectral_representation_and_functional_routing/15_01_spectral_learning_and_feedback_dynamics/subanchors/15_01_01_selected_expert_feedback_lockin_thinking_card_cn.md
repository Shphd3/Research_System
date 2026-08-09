---
thinking_card_id: 15_01_01_selected_expert_feedback_lockin
status: human_authorized_full_cycle
human_language: zh
formalization_authorized: true
protocol_authorized: true
implementation_authorized: true
full_run_authorized: true
source: /daily_research_reports/backup/2026/07/0731/conjectures.md
created: 2026-07-31
---

# Thinking Card：专家反馈是否锁定 head 路由并压制 M/T 纠正

> 本卡从研究者的 `conjectures.md` 提取判断。人类判断与 AI 操作化分开记录。

## 人类判断

- **现象：** 线性 Gate 起初对 head 响应更强；middle/tail 虽可能在后续追赶，
  但已选专家在共同训练中会形成效能优势。
- **机制猜想：** 早期 head 分配与专家优势构成正反馈，使 Router 更可能继续
  选择原专家，并掩盖 middle/tail 对路由的纠正，最终使 Router 行为变差。
- **明确的隐含判断：** middle/tail 含有真正有用的信息，MoE 原本可以利用该
  信息形成更细的专家分工。
- **原始最强不确定性：** 上述现象究竟来自专家反馈，还是只来自小方差方向学习
  更慢，尚未区分。
- **授权：** 研究者允许 AI 自行修正问题、写 Anchor/Protocol、实现并完成正式
  运行，不再要求中间审批。

## AI 操作化提案

- **定义“有用”：** H/M/T 三个平衡二值变量共同、且缺一不可地决定损失最优
  专家；因此 M/T 功能不是事后推断，而是数据生成真值。
- **最强 rival：** M/T 纠正慢完全由输入方差造成，与专家是否获得功能覆盖无关。
- **最小区分实验：** 保持 Router 输入、初始 head margin、数据、优化器和每个
  token 的活跃专家更新数不变，只比较“按当前选择训练专家”和“按真值给专家
  功能覆盖”。
- **会改变判断的证据：** 只有功能覆盖显著恢复 M/T 条件内路由，同时原生
  selected-only arm 出现 incumbent 优势与 challenger 饥饿，才支持反馈锁定。
- **当前决策：** pursue；将方差慢学习与专家反馈锁定分成独立对照。

