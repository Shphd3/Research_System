---
thinking_card_id: 15_05_04_fixed_band_cross_update_compatibility
parent_anchor: 15_05_functional_coordinate_admission
status: human_approved_for_execution
human_language: zh
formalization_authorized: true
protocol_authorized: true
implementation_authorized: true
full_run_authorized: true
updated: 2026-07-30
---

# Thinking Card：A15_05_04 一步交叉更新兼容性准入

## 我的判断

- **具体现象：** middle / long-tail 可以改变表示邻域，但现有冻结结果不知道
  这种新划分是否把共同训练时互相帮助的 token 放在一起。
- **机制猜想：** 若频带保留了功能关系，则频带内相似的两个独立 token 组，
  更新同一专家时应比 native logits 所预测的更少冲突或更互相促进。
- **最强替代解释：** 兼容性差异完全由 native expert、logits、token loss、
  梯度范数、文档或 batch 决定；频带增量不超过随机同维方向。
- **最不确定的一环：** 小步长、固定路由的一步交叉 loss 是否稳定且可复现。
- **什么证据会改变判断：** held-out compatibility $\Delta R^2$ 的文档级区间
  高于零，并超过同维随机 q95 与错误层；步长、route replay、self-update 和
  数据独立性护栏全部通过。
- **当前唯一决策：** 该频带是否获得进入匹配联合训练的资格。

## AI 审核

- **唯一未定义对象或隐藏假设：** 兼容性是目标层、目标专家和局部步长条件下
  的量，不能直接外推为全模型长期收益。
- **最小反例或区分实验：** 静态邻域可以很新，但 $\Delta R^2$ 不高于随机；
  这足以否定“额外几何就是功能分辨率”。
- **AI 建议：** pursue，静态新颖度只作诊断，held-out $\Delta R^2$ 才是准入
  主指标。

## 我的确认

- **保留或修改后的判断：** 研究者已确认 A/B 双向一步更新、三个 non-head
  treatment 和随机/错误层对照的总体设计合理。
- **是否允许写入正式 anchor：** yes；具体数据量、统计聚合与执行授权待审核。
