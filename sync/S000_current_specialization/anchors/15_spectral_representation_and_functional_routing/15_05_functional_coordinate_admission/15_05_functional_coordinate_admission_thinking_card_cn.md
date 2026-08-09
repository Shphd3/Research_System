---
thinking_card_id: 15_05_functional_coordinate_admission
status: human_approved_for_execution
human_language: zh
formalization_authorized: true
protocol_authorized: true
implementation_authorized: true
full_run_authorized: conditional_on_e01_pass_and_pilot_guards
updated: 2026-07-30
---

# Thinking Card：A15_05 middle / long-tail 频谱是否具有功能分辨率

> 本卡整理自研究者在 2026-07-30 对 Q2 的直接判断；它保留人的研究意图，
> 不等同于正式 anchor 或 Protocol。

## 我的判断

- **具体现象：** Q1 已表明训练后的线性 Router 主要依赖 covariance head，
  但 middle 和 long-tail 仍可访问且会改变一部分 native 路由。
- **机制猜想：** 线性 Gate 的少量 logits 可能压缩掉 middle 或 long-tail 中与
  专家共同训练兼容性有关的结构；使用这些频带可能提供 native Router 之外的
  额外功能分辨率，并进一步改变 Router--Expert 的联合学习路径。
- **最强替代解释：** middle / long-tail 只提供高维几何上的不同划分；任何
  同维随机子空间、表示范数、离群值、文档来源或 batch 结构都能产生类似现象，
  但它们不预测专家更新兼容性，也不会改善匹配计算下的训练。
- **最不确定的一环：** 一步交叉更新兼容性是否真能区分功能信息与几何噪声，
  以及它是否有资格作为 1--2B-token 联合训练的准入门槛。
- **什么证据会改变判断：** 在独立 DCLM 文档上，middle、long-tail 或二者
  联合必须在 native logits、margin、专家、负载、容量、token 数、范数和
  batch 控制后，增量预测共同训练兼容性，并稳定超过同维随机与错误层基底；
  随后的匹配 8×5090 训练还必须改善 held-out loss/FLOP。
- **当前唯一决策：** 先批准、修改或拒绝局部功能准入 Protocol；准入未通过
  前不运行频谱分发训练。

## AI 审核

- **唯一未定义对象或隐藏假设：** “额外划分”不等于“功能收益”；一步兼容性
  也只是长期训练收益的代理，不能替代匹配联合训练。
- **最小反例或区分实验：** 在完全相同的独立 token-group pair 上，以实际
  交叉更新 loss 为目标，比较 native baseline 加入 middle / tail /
  middle+tail 后的 held-out 增量，并与同维随机和错误层比较。
- **AI 建议：** pursue；把局部兼容性准入和 8 卡联合训练写成两个独立、顺序
  阻塞的 Protocol。

## 我的确认

- **保留或修改后的判断：** 研究者确认上述总体设计合理；要求复用实际 Router
  输入频谱，明确 A/B 更新步骤，完整比较 middle、long-tail、middle+long-tail，
  并预先设计但不提前运行 8 卡训练。
- **是否允许写入正式 anchor：** yes；具体 Protocol 条件与指标边界仍需研究者
  逐项审核。
