# A16_01_01 效用蒸馏的条件增量路由


## 1. Problem Definition

A16_01 研究真实同层 Router 可见增量能否在可微负载均衡下改善路由。现有分支只通过语言模型损失与负载损失间接监督，到 20B 没有两个 seed 复现的优势；所有几何可读方向也在冻结 expert-choice regret 门失败。因此，当前最小不确定性是训练目标是否对齐专家效用，而不是再换一个谱坐标。

令 $x_{\ell,t}=n^{old}_{\ell,t}$ 为 Attention 写入前的归一化状态，$u_{\ell,t}=n^{new}_{\ell,t}-n^{old}_{\ell,t}$ 为实际同层增量，$r_{\ell,t}=u_{\ell,t}-A_\ell x_{\ell,t}$ 为不能由旧状态线性预测的部分。唯一问题是：**在两个冻结 Native-LB 10B checkpoint 上，用反事实专家效用训练的 rank-56 条件增量分支，能否在 held-out 文档上同时低于 Native、raw-$u$ 效用分支与同维 Haar 残差分支的目标 token 选专家遗憾？**

Pass 使该分支获得已条件批准的 10B→30B NLL 测试资格；Fail 在长训前关闭本实现；工程或数据身份失败为 Insufficient。本问题不预设冻结教师在专家共同演化后仍然正确。

## 2. Physical Priors

保留的物理先验是：若存在有用路由信号，它应体现为 token 条件下的专家相对优势，而不是 covariance rank 或语义可读性。去掉 $x$ 可预测的 $u$ 应减少增量分支与 Native 路径的重复。若条件残差不能在两个 seed 上超过 raw 与 Haar 对照，该先验在本实现中被证伪。

## 3. Falsifiable Hypotheses

**H1：** $r$ 含有冻结 Native logits 尚未使用、可跨文档泛化的相对专家效用，直接效用蒸馏能够把它绑定到路由；因此 Conditional-Utility 在两个 seed 上都应低于 Native、Raw-Utility 与 Conditional-Haar 的 held-out regret。

**最强竞争解释：** 教师只是局部噪声、残差化删除了有用信号，或任意低维旁路都同样有效。只优于 Native、不优于 Raw 只能支持效用监督；只优于 Raw、不优于 Haar 不能支持学习方向的身份价值。

## 4. Mathematical Model

只用 FIT 文档按文档交叉拟合 $A_\ell$。令 $P_\ell\in\mathbb R^{768\times56}$ 为学习或固定 Haar 的正交框架，$C_\ell=A_\ell P_\ell$。部署公式为：

$$
z_{\ell,t}=z^{native}_{\ell,t}+\alpha_{\ell,t}B_\ell\left(u_{\ell,t}P_\ell-x_{\ell,t}C_\ell\right).
$$

它等价于 $z^{native}+\alpha B(rP)$，但不在线执行 $768\times768$ 回归。对同一目标 token 逐个强制八个专家，得到下一 token loss $\ell_e$，教师为：

$$
q_e=\operatorname{softmax}_e\left(-\frac{\ell_e-\min_j\ell_j}{0.1}\right).
$$

主指标是选专家遗憾 $R=\ell_{\arg\max_e z_e}-\min_e\ell_e$，单位 nat/token。它衡量冻结专家下局部选错专家的代价，不能证明长期训练收益。

## 5. Computational Realization

每个 seed 使用自己的 Native-LB 10B checkpoint 和既有 384 文档功能 bank。FIT/DEVELOPMENT/CONFIRMATION 各 128 个完整文档，每文档八个固定目标位置。FIT 内做五折 document cross-fit；DEVELOPMENT 只选注册候选；CONFIRMATION 在全部选择冻结后只打开一次。

分支复用 Native checkpoint 已经存在的 dormant rank-56 projection 与 expert-logit 参数。标准化统计和 $C$ 从带 hash 的 artifact 重建，因此不增加可训练参数或缺失 optimizer slot。冻结蒸馏时 backbone、experts 与 Native Gate 不收梯度；长训在线路径不逐个强制专家。

## 6. Minimal Falsification Tests

决定性检验是两个 seed 的文档配对 confirmation 比较。每个文档先对四层和八个注册位置的 regret 取平均；Conditional-Utility 只有在两个 seed 中，相对 Native、Raw-Utility 和 Conditional-Haar 的三组配对 bootstrap 95% 上界均小于零，才通过。逐层结果只用于解释，不能用于选择有利层或替代注册聚合裁定。

完整合格数据不达标为 Fail。checkpoint 身份、数据隔离、局部反事实、cross-fit、数值或恢复护栏失败才是 Insufficient。

## 7. Current Evidence

父实验只建立了动机：Trainable-Innovation 的 20B 效应在两个 seed 上符号相反，2B/5B/10B 的 E2 均未发证书。Native checkpoint 与冻结功能 bank 已存在；条件分支和本门尚为 `NOT RUN`。最安全解释是几何或 NLL-only 增量路由尚未暴露专家效用，而不是条件增量已被否定。

## 8. Claim Boundary And Next Decision

E01 Pass 只支持当前四层 DCLM、冻结专家和当前教师定义下的局部功能价值；不能证明 30B NLL、专家专业化、普遍语义新增或公共谱基。Fail 会在长训前关闭本实现；Insufficient 只允许修复无效护栏，不能更改科学合同。

**唯一下一决策：** 执行已批准的两 seed 冻结 regret 门。**完成判据：** 生成合格 confirmation 数组和注册的 Pass/Fail/Insufficient verdict。**恢复动作：** 当且仅当 E01 Pass，自动执行已冻结的 A16_01_01_E02，续训到 30B 总 token。
