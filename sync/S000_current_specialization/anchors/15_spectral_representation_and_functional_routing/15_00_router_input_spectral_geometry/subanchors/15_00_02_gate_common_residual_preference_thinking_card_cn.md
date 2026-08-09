---
thinking_card_id: 15_00_02_gate_common_residual_preference
status: full_execution_authorized
human_language: zh
formalization_authorized: true
protocol_authorized: true
implementation_authorized: true
full_run_authorized: true
updated: 2026-07-31
---

# Thinking Card：Gate 是否优先学习可迁移 common 而非局部 residual

## 我的判断

- **具体现象：** decommon 删除均值后，Gate 仍明显对齐中心化 covariance head。
- **机制猜想：** 统一线性 Gate 更容易累计跨数据重复出现的方向，而不是每组
  都改变的 residual；因此 decommon 改变的是 DC 归纳偏置，并没有迫使 Gate
  使用真正的数据组特异残差。
- **最强替代解释：** Gate 的 head 对齐仍只是输入能量、估计维度、错误层共享
  方向或已有 native logits 的结果；或者 Gate 偏稳定方向，但该方向恰好是有用
  共享功能，不能把它称为失败。
- **最不确定的一环：** 在完全等能并去除专家公共 logit 后，Gate 对 pooled
  centered-common candidate 的增益和实际 route dependence，是否都高于同维
  shard-local residual。
- **什么证据会改变判断：** pooled candidate 的等能增益不高于 local residual
  或 orientation null；或者 route ablation 显示 native 决策更依赖 local
  residual。
- **当前唯一决策：** 与 A15_00_01 并行执行已批准的冻结 Protocol，并形成
  typed verdict；未批准新训练。

## AI 审核

- **必要修正：** A15_00_01 尚未裁定 pooled candidate 是否真的稳定，所以本
  subanchor 只能先报告“Gate 偏 pooled 还是 local”；只有两个 subanchor 同时
  Pass，才能使用“Gate 偏稳定 common”的联合语言。
- **最小证伪：** 使用同维 64 维 pooled candidate 与 cross-fitted local
  residual bases，比较 equal-energy Gate gain、去带后的 native-margin
  support，并把 flip 作为辅助；在 30k/40k/80k 固定基底 crossing 中分离
  Gate 权重与表征变化。
- **AI 提议的主量：** $B_{P:L}=\log(G_P/G_L)$；它测 Gate 几何偏好，不测
  expert utility 或训练收益。

## 我的确认

- **已授权：** subanchor、双语 Protocol、实现与完整冻结运行。
- **未授权：** 新训练、graph、root sync、commit 或 push。
