# Thinking Card：Local-HMT 的弱优势是否来自 covariance 身份

- **现象：** 在已完成的两 seed 10B 训练中，Local-HMT 的终点 NLL 点估计均最低，但相对 Centered-Full 只有 seed 17 的逐文档配对区间明确低于零。
- **机制判断：** 本层 covariance 排名得到的 H/M/T 可能提供了普通动态低维约束不能复现的路由归纳偏置。
- **最强竞争解释：** Local-HMT 的弱优势只来自去均值、平滑更新或动态低维瓶颈，而不是 covariance 排名身份。
- **最不确定点：** 旧实验没有 Local-Random；旧 Relay-Random 又通过完整特征基底右混合，目标运动量明显更大，不能作为严格的本层随机对照。
- **改变判断的证据：** 在目标子空间运动量、维度、统计语料、刷新频率、EMA、Grassmann 更新和连续性守卫匹配后，Local-HMT 在 seed 17、29 中都以逐文档配对区间优于 Local-Random。
- **当前下一决策：** 直接补跑两个 seed 的 Local-Random-Matched 10B 训练，并与既有 Local-HMT、Centered-Full 做配对裁定。

