---
thinking_card_id: 15_00_02_centered_common_subspace_stability
status: full_execution_authorized
human_language: zh
formalization_authorized: true
protocol_authorized: true
implementation_authorized: true
full_run_authorized: true
updated: 2026-07-31
---

# Thinking Card：去均值后的公共子空间是否稳定

## 我的判断

- **具体现象：** decommon 去掉了 Router 表征的均值，但 Q1 仍观察到 Gate
  明显对齐去均值后表征的 covariance head；固定 M/T/N 又没有获得稳定功能
  证书。
- **机制猜想：** Router 表征包含全局均值、跨数据稳定的中心化公共变化，以及
  数据组特异残差。decommon 只删除第一项；真正的数据组残差可能随文档或
  batch 改变，难以形成统一路由坐标。
- **最强替代解释：** 残差子空间并不比公共子空间更不稳定；观察到的差异只是
  768 维 covariance 在有限 token 上的估计噪声。另一个解释是残差确实不稳定，
  但这与专家功能或训练收益无关。
- **最不确定的一环：** 在 DCLM 的独立文档组之间，去均值后的主子空间究竟
  能否跨组复现，以及移除这部分后剩余方向是否更不稳定。
- **什么证据会改变判断：** 独立文档组的 centered top 子空间不能超过同维
  Haar 对照跨组迁移；或移除 pooled top 子空间后，剩余局部子空间仍同样稳定。
- **当前唯一决策：** 与 A15_00_03 并行执行已批准的冻结 Protocol，并形成
  typed verdict；未批准新训练。

## AI 审核

- **需要保留的判断：** “去均值”不等于“去掉所有 common”，而且 residual
  需要用跨数据稳定性定义，不能用 covariance rank 名称代替。
- **隐藏假设：** batch mean 高余弦并不能证明 centered subspace 稳定；单个
  minibatch PCA 也可能只有估计噪声。
- **最小证伪：** 在不重叠文档组上交叉拟合、交叉评价 top-64 子空间，并与
  Haar、错误层和 sample-size curve 比较；随后对正交剩余空间做同维测试。
- **AI 提议的主量：** held-out cross-capture 超过同维 Haar q95 的差值；它
  只裁定几何稳定性，不裁定语义或训练价值。

## 我的确认

- **已授权：** subanchor、双语 Protocol、实现与完整冻结运行。
- **未授权：** 新训练、graph、root sync、commit 或 push。
