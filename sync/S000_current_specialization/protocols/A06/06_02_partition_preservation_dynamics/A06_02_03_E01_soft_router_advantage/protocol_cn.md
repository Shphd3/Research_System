# Protocol（中文 companion）：A06_02_03_E01 Soft-Router Advantage-To-Margin Dynamics

## 0. 审核快照

状态：用户已明确授权重构并执行。英文 `protocol.md` 为 canonical。

目的：判断 matched expert 的功能优势是否产生正的 feature margin 压力。

最小设置：4 个均匀 feature、冻结 hidden、固定 expert output、soft router、只对 router 做一步 SGD。

条件：matched utility、identical experts、permuted utility；32 seeds；学习率 0.01/0.05。

主指标：feature-seed cell 中 geometry-matched margin 一步增量为正的比例。

通过：matched 条件正比例至少 0.90；identical update 为数值零；permuted 条件的 pressure 转向 utility-aligned expert。

失败：matched 正比例低于 0.75，或 negative control 假阳性。

边界：只能裁定 frozen soft-router 的局部机制，不能证明 top-1、长期保持或真实文本。

## 1. 术语解释

- expert advantage：增加某 expert mixture weight 对当前 loss 的一阶收益。
- matched margin：指定 expert 相对最强 competitor 的 router score 差。
- formula closure：解析更新和 autograd 更新的一致性；只做实现守卫，不做机制证据。

## 2. 假设与竞争解释

假设：功能匹配使 margin 增厚；相同 expert 消除信号；功能置换使压力转向真正有用的 expert。

竞争解释：row norm 增长、chain-rule 恒等式或高 route purity 可能制造假支持。

## 3. 数据、模型与算法

16 维正交 feature centers，每个 feature 采样 256 个 hidden，噪声标准差 0.05。固定 expert 输出强度 4.0。保持 hidden、expert 和 labels 不变，只改变 expert utility mapping。

## 4. 指标与判定

主指标为 positive matched-margin rate。辅助指标包括 utility-redirection gap、update norm 和 formula closure error。判定阈值以英文 protocol 为准，不做事后修改。

## 5. 不可声称内容

不能声称 sparse correction、trainable representation preservation、semantic expert 或新 gating 方法。

