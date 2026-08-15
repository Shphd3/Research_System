---
thinking_card_id: 15_02_05_balanced_taxonomy_attention_write_atlas
status: researcher_judgment_confirmed_formal_anchor_revision_requested
human_language: zh
formalization_authorized: true
execution_authorized: false
updated: 2026-08-09
---

# Thinking Card：粗—细粒度语义的逐层谱定位

> 本卡保存研究者在 0807 会议记录和 2026-08-09 复核中明确表达的判断。标注 `AI_PROPOSAL` 的数据、变量、指标和裁定规则仍待研究者审核；本卡不批准实现或执行。

## 我的判断（研究者确认）

- **父问题：**已经看到语义谱随深度发生变化，但还没有弄清不同层、不同谱段之间是什么关系，以及较粗类别和更细类别的语义差异怎样出现在当前层写入中。
- **本实验角色：**这是粗—细粒度语义层间定位的认知更新实验，不是 Router、expert utility、训练增益或功能验证实验。
- **已观察现象：**语义方差的局部谱位置随深度总体后移；已有结果还不能说明这是细粒度语义特有的定位变化、粗细语义共同增强、归一化造成的表象，还是多个细类相互抵消后的平均曲线。
- **当前阻塞：**只画总体 TAX 曲线和谱重心，可能仍然不知道“粗细差值”具体代表什么，也看不到 `combinatorics - mathematics`、`linear algebra - mathematics` 这类具体细类是否具有相同的逐层结构。
- **本轮必须部分回答的三个问题：**
  1. 粗粒度和条件细粒度语义的绝对强度、归一化谱分配及二者差值怎样随层变化；
  2. 把粗细表征作差时，尺度、归一化、样本共享、类数、谱基变化和聚合抵消会造成哪些缺陷；
  3. 具体细类相对父类的逐层差值是否可靠、是否跨层保持相关，以及不同细类是否共享同一个“更细”方向。
- **最强竞争解释：**晚层只是让所有学科语义共同增强或共同重排；总体 fine-minus-coarse 曲线可能由分母、共享父类均值、少数 child、模板噪声或局部谱基不稳造成，并不对应一致的细类定位规律。
- **什么证据会改变判断：**若绝对可靠信号存在，但粗细归一化谱位置的深度交互为零或反向，则撤回“细粒度语义具有额外后移”；若总体效应存在但预注册细类曲线不可靠或互相矛盾，则只保留“聚合异质性”，不声称统一的细粒度谱规律；若绝对量、归一化位置和具体细类均一致，才允许形成一个受限的表征定位认识更新。
- **当前下一决策：**审核本 Anchor 与 `DRAFT_NOT_EXECUTABLE` Protocol 中的数据版本、粗细差值定义、唯一主指标和具体语义图合同；未经明确批准不实现、不运行。

## AI 审核与操作化建议

- **方向归属：**保留 `A15_02_05`，作为 A15_02 表征图谱的独立子问题；不并入 A15_03 shared-middle 或 A15_04 shared-tail，也不进入 A15_05 功能准入。
- **“更细语义差值”的安全定义：**`AI_PROPOSAL` 使用 child 中心减去同一 parent 内其他 children 的中心，得到 sibling-relative residual。它避免 child 被包含在自己的 parent 参照中，但仍不是可分解出的“纯细粒度 feature”。
- **禁止操作：**不同层的 covariance、RMS 或 eigenvector 不直接相减；相同 local rank 不视为同一方向。跨层只比较预先定义的标量谱分布，以及在共同残差坐标中的 split-half 方向相关。
- **`AI_PROPOSAL` 主指标：**以 16 段归一化谱分配的秩重心表示谱位置，比较 fine-minus-coarse 的晚层中位数与早层中位数之差；绝对每方向方差和完整 F1--F16 曲线是强制解释证据，不能由重心替代。
- **`AI_PROPOSAL` 具体语义图：**分别画 `combinatorics - mathematics` 与 `linear algebra - mathematics` 的逐层绝对/归一化谱图、跨层 split-half 方向相关矩阵，以及两者的同层相关曲线。单一概念只能解释案例异质性，不能代表全部细粒度语义。
- **数据冲突：**已审计的旧 512 条学科描述包含 `combinatorics` 和 `algebra`，不包含 `linear algebra`；旧自然层级语料虽包含 `linear algebra`，但不是同一批状态。`AI_PROPOSAL` 是保持 8×8×8=512 的结构，将 mathematics 下的 `algebra` 替换为 `linear algebra` 后重新冻结整个 manifest。若研究者要求逐条复用旧 512，则具体案例必须改为 `algebra - mathematics`，不能伪称 `linear algebra`。
- **最小反例：**细粒度的 normalized 谱重心看似后移，但绝对可靠能量不增加或 calibration half 改变符号；或者总体曲线通过而两个预注册数学细类均不复现。前者只允许“相对重分配”，后者只允许“聚合平均掩盖异质性”。

## 我的确认

- 实验只负责粗—细语义层间定位认知更新：已由研究者明确确认。
- 上述三个问题和两类数学案例必须进入设计：已由研究者明确要求。
- 固定 512 总样本、实际 attention-induced MLP-input increment $\Delta n$ 为主表示、isolated post-`o_proj` write 为来源边界：`AI_PROPOSAL`，待审核。
- 旧 512 逐条复用，或以 `linear algebra` 替换 `algebra` 后冻结新 512：待研究者选择。
- 主指标、split-half 相关、Haar/标签重排 controls 与裁定规则：`AI_PROPOSAL`，待审核。
- implementation / preflight / smoke / full run：未批准。
