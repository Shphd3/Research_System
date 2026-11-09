---
story_id: A15_spectral_representation_to_functional_routing
status: current_primary_synthesis
updated: 2026-08-15
language: zh-CN
canonical_en: 02_spectral_representation_to_functional_routing.md
---

# 从谱重分配走向目标条件下的层新增信息

## 0. 术语约定

| 术语 | A15 中的具体含义 | 不代表什么 |
| --- | --- | --- |
| 旧 token 局部状态 | 当前 attention 写入前，这个 token 已经可用的状态 | 前一层完整序列包含的全部信息 |
| 层更新 | 在一个明确表征位置上，本层实际写入的变化 | 已证明上一状态中不存在的知识 |
| 实际 \(\Delta n_\ell\) | MLP 输入位置的 \(RMSNorm_\ell(h_\ell+a_\ell)-RMSNorm_\ell(h_\ell)\) | 原始 attention 输出或 MLP 因果使用 |
| 层新增信息 | 相对旧 token 局部状态，对一个冻结目标产生留出预测增益的信号 | 更大方差、协方差差值或更后谱秩 |
| 本地谱秩 | 在某一层独立求基、独立排序后的位置 | 另一层中的同一方向 |
| 方向身份 | 在共同隐藏坐标中可复现的投影空间重合 | 语义身份或功能身份 |
| 功能使用 | 保留、删除或替换候选信号后，任务损失或专家相对收益发生受控变化 | 仅仅能够线性读出 |
| 精确 transition \(U\) | 同一 token、hook、归一化和隐藏坐标下的 \(Z-X\) | 定义上就是新知识 |
| 条件残余更新 \(R_U\) | 冻结残差模型下，\(U\) 中不能由旧状态 \(X\) 线性预测的部分 | \(X\) 中不存在的全部非线性区分 |
| 条件创新矩阵 \(K_{new}\) | 从 \(R_U\) 中选择目标残差方向的有监督算子 | 装着知识的矩阵或可部署 Router |
| 表征有效秩 | 一个具名更新 covariance 的熵有效秩或 80% 方差秩 | 保留目标读出增益所需的任务秩 |
| 公共激活基 | 对各层 TRAIN 长程交互更新 covariance 先做 trace normalization、再等层权汇总后得到的同一特征基 | 参数基、目标充分基或 Router 坐标 |

## 1. 摘要

A15 起源于一个路由直觉：不同 Transformer 层可能暴露不同信息，因此
有效 Router 可能需要逐层不同的输入。当前主线已经得到关于协方差访问、
学习速度、语义谱重分配和路由干预的受限事实；A15_08 现在还给出了一个
具名层 transition 相对旧 token 状态的合格“定义 + 存在性”结果。

方法包含三个受审核角色，不是三套竞争定义。TRAIN-only pooled basis 是一条
旁路诊断，把匹配的旧状态与新状态放进同一描述坐标。真正的决策链用
\(U=Z-X\) 记录精确归一化 attention transition，再从 \(U\) 中去除旧状态可线性
预测的部分，并要求它在全新留出目标上超过旧状态读出和目标独立同预算对照。
只有这条决策链裁定新增可访问性；公共基和原始差分本身都不能裁定。

A15_02_06 把此前混在一起的描述性步骤拆成了四步：先用两种参数公共基审核
坐标依赖，再在冻结 Mean Response 基中比较每层 Attention-write 方差谱，随后
比较粗、中、细语义的谱重心与同层曲线形状，最后扫描全部相邻层。结果是：
深度后移依赖基；粗到细只呈现轨迹级后移；曲线差异分散而不构成唯一连续谱段；
相邻层正负交替。由此停止研究固定 band，并把公共基降为描述性标尺。

E03 不能承载这个结论：最终冷读发现它缺少带命名空间的
`episode_id` 和 `map_id`、结构化特征提取回执、完整的简单条件
episode/bootstrap 数组，以及覆盖全部注册证据族的 manifest。它的
数值只能作诊断。E04 是一次使用全新数据、只修复合规性的实验，
也是首个合格结果。在受控两跳目标上，完整残余更新带来
0.767207 nats/example 的留出增益，区间为
\([0.751296,0.785146]\)。注册的两个创新方向并非空方向，却只保留
33.24% 增益，因此二维充分性 H1' Fail。组会的全局低秩 H1 仍未
检验，本地结果也不建立模型原生使用或 Router 价值。研究者已经暂停本地
任务读出秩阶梯。当前已提交的子问题是：远程必要桥接事实的新增可访问性
是否在注册 blocks 2--36 中随深度增强，以及匹配交互更新的表征秩在一个激活数据公共
基中如何变化。

## 2. 研究问题

根问题是：

> 相对一次明确层写入前的 token 局部状态，该写入使哪个与目标有关的
> 区分新变得可访问；还需要什么独立证据，才能说明模型或 Router 真正
> 使用了这个区分？

这个问题包含两个不能混为一谈的部分：

1. **条件新增可读性：**在一个明确读出器族下，加入层更新是否比只用
   旧状态更好地预测冻结目标，并在未参与拟合的数据上保持优势；
2. **功能使用：**对层更新做受控干预，是否改变任务损失、专家相对收益
   或其他预先注册的功能目标。

第一个部分已经在一个受控第 25 层 attention transition 和线性读出器族上
得到回答；第二部分仍在下游。当前方向把第一个部分扩展到逐层比较；暂不检验
任务充分检索秩，也不训练或评估 Router。

## 3. 为什么这个问题容易混淆

此前有五种不同现象都曾被称为“新增信息”：

1. 非零 residual update；
2. 协方差或谱形状发生改变；
3. 只用更新就能读出语义标签；
4. 在旧状态之外加入更新后，语义标签更容易读出；
5. 对更新做干预会改变模型或专家功能。

只有第 4、5 项能回答当前问题，而且二者回答的是不同层面。非零更新是
计算事实；协方差改变是二阶统计事实；更新单独可读仍可能与旧状态完全
冗余；功能使用必须由干预或与损失一致的反事实目标确认。

Transformer 各 block 的 residual stream 共享同一个环境坐标，所以在
token、hook 位置和归一化位置都匹配时，向量相减在代数上有意义。但每层
独立拟合的特征基并不相同。相减相同谱秩只能比较两条排序曲线，不能比较
两条已经确认身份的方向。

还必须区分两种相减对象。在匹配的 raw residual 边界上，
\(r_{\ell+1}-r_\ell\) 是完整 block 的精确写入；而
\(RMSNorm_{\ell+1}(r_{\ell+1})-RMSNorm_\ell(r_\ell)\) 还混入了逐层
normalization 映射的变化。若问题是 attention 给随后 MLP 增加了什么，
应对 attention 写入前后的匹配状态使用同一个 \(RMSNorm_\ell\)，得到下文
定义的 actual \(\Delta n_\ell\)。

## 4. 数据与证据布局

| 证据块 | 对象 | 已经支持的决策 |
| --- | --- | --- |
| A15_00 | 实际 Router 输入与训练后 Gate | 存在非均匀谱访问；head 偏好不只是原始能量效应 |
| A15_01 | 受控 Gate 学习与反馈 | 协方差尺度改变有限时间学习速度；真实训练迁移结论仍受限 |
| A15_02 | 冻结 Qwen3-8B 状态、两种参数公共基与 attention 引起的更新 | Mean Response 中粗<中<细，但深度后移依赖基、曲线差异分散、相邻层变化非单调；未建立统一 fine-specific 谱秩规律或条件新增线性信号 |
| A15_04 | 本地及跨层 MLP 参数空间 | 本地后移不是共享语义 tail；稳定终端参数几何与晚层细语义占据增长解耦 |
| A15_05 | 兼容性与固定频带匹配分发 | 改变几何或分发本身不能获得功能准入 |
| A15_06 | 在线本地/浅层转发谱路由 | 协方差谱秩身份没有跨随机种子的可复现功能优势 |
| 2026-08-10 方差区间审核 | 投影到逐层参数秩的 residual/input 与原始 attention 输出 | 方差增长区间未稳定定位更具 domain 区分力的子空间，也不能定义新增信息 |
| A15_08 | 一个归一化第 25 层 attention transition、条件残余更新和全新留出目标读出 | E04 是首个合格的局部新增可访问性 Pass；注册二维充分性在 33.24% 保留率下失败 |
| A15_08_01，E02 结果 | 匹配的一跳/两跳 × 近程/远程关系世界、blocks 2--36 归一化 attention 更新和一个激活数据公共基 | 合格 typed Fail：\(T_{depth}>0\) 但 \(A_{2F}<0\)；表征秩非单调且只作描述 |

这些证据使用不同模型、表征位置、目标和坐标系。它们约束同一论证，但
不能被当作一个合并实验。

## 5. 物理直觉

确定性网络层只会变换和聚合前一完整模型状态中的信息；严格按 Shannon
信息论，它不必“创造”新的外部信息。但是对于只观察一个 token 局部状态
的 Router，attention 可能把上下文区分新带到这个 token，或让已有区分
对一个受限读出器变得更容易访问。

因此可保留的直觉不是“深层方差更大”，而是：

> 一次层更新可能重新组织或引入上下文，使某个与目标有关的区分相对旧
> token 局部状态新变得可访问。

表征秩是另一个几何假设，可以在同一批冻结更新上测量，但在批准阈值以前只作
描述，不能替代留出增益检验。任务充分压缩是更后面的另一问题，当前已暂停。
谱位置从来不是新增可访问性的定义。

## 6. 定义与指标

令 attention 写入前的 residual 为 \(h_\ell\)，attention 写入为 \(a_\ell\)：

\[
n_\ell^{old}=RMSNorm_\ell(h_\ell),
\qquad
\Delta n_\ell=RMSNorm_\ell(h_\ell+a_\ell)-n_\ell^{old}.
\]

\(\Delta n_\ell\) 是 MLP 输入位置上的具体计算更新。它不能仅凭定义就被
称作新增语义信息。

对一个冻结目标 \(Y\) 和读出器族 \(\mathcal F\)，令
\(\mathcal R_{test}\) 表示留出风险。候选条件新增可读性为

\[
G_\ell(Y;\mathcal F)
=
\mathcal R_{test}\!\left(f_0(n_\ell^{old})\right)
-
\mathcal R_{test}\!\left(f_1(n_\ell^{old},\Delta n_\ell)\right).
\]

拟合和模型选择不得使用留出数据。\(G_\ell>0\) 只表示：在指定目标、读出
器族和数据拆分下，层更新提供额外预测价值。它不能证明信息论意义上的
新增，也不能证明模型原生使用。

功能指标必须另外比较完整计算与对候选更新所做的匹配干预。其单位和
目标取决于获批问题：若问语义功能，则看任务损失；若问路由功能，则看
反事实专家遗憾。可读性不能代替这一步。

已经执行的 A15_08 对象在前后使用同一个第 25 层 post-attention
normalization：

\[
X=N_{25}(h),\qquad Z=N_{25}(h+a),\qquad U=Z-X.
\]

历史 E04 无标签公共基 \(V_{pool,E04}\) 只用 TRAIN 中 episode-centered 的 \(X\) 与 \(Z\)
拟合。它描述旧状态、新状态和更新的方差在哪里，不裁定新增性。承担决策的
更新是

\[
R_U=U-\widehat{\mathbb E}_{lin}[U\mid X],
\]

对中心化 one-hot 目标 \(Y_c\)，再定义

\[
R_Y=Y_c-\widehat{\mathbb E}_{lin}[Y_c\mid X].
\]

具体确认集增益为

\[
G_{true}=CE(f_X(X))-CE(f_X(X)+g_{full}(R_U)),
\]

\[
G_{state}=CE(f_X(X))-CE(f_Z(Z)),\qquad
G_2=CE(f_X(X))-CE(f_X(X)+g_2(P_2^{\top}R_U)).
\]

单位均为 nats/example，正值表示留出损失降低。令
\(Q_{mis},Q_{random},Q_{perm}\) 为每次 paired episode bootstrap 内 64 个匹配
对照族的 higher-method 95% 分位，则

\[
T_{cap}=G_{true}-Q_{mis},\qquad
D_{80}=G_2-0.8G_{true},
\]

\[
T_{random}=G_2-Q_{random},\qquad
T_{perm}=G_2-Q_{perm}.
\]

H2 要求 \(G_{true}\)、\(G_{state}\) 和 \(T_{cap}\) 的 95% 下界均为正。门控 H1'
要求 \(D_{80}\)、\(T_{random}\) 和 \(T_{perm}\) 的下界均为正；任一上界不为正即
H1' Fail。这些指标只建立有边界的线性可访问性，不建立模型原生使用。

当前 A15_08_01 提案在每个 block 复用同一层内表征身份，但不复用 E04 的
任务秩阶梯。对条件 \(c\in\{1N,1F,2N,2F\}\)，令 \(G_{\ell,c}\) 表示：把基于
\(R_{U,\ell,c}\) 的冻结修正加入冻结旧状态读出器后，留出交叉熵降低多少。定义
必要性×距离交互：

\[
I_\ell
=(G_{\ell,2F}-G_{\ell,2N})
-(G_{\ell,1F}-G_{\ell,1N}).
\]

冻结主对比是第 25--36 层的 \(I_\ell\) 中位数减去第 2--12 层中位数。blocks
2--36 的 \(G_{\ell,c}\) 和 \(I_\ell\) 必须绘图；相邻层差只描述局部斜率，不是
独立样本。

## 7. 数学模型

令中心化旧状态为 \(H\)、中心化层更新为 \(U\)，若下一状态为 \(H'=H+U\)，则

\[
\Sigma_{H'}-\Sigma_H
=
\Sigma_U
+\operatorname{Cov}(H,U)
+\operatorname{Cov}(U,H).
\]

协方差变化包含更新自身方差和两个带符号交叉项，通常不是半正定矩阵，
因此不是“新增知识的协方差”。即使 \(\Sigma_U\) 也只能叫作计算更新的
协方差；要称为新增信息，仍须指定目标并完成条件比较。

若每层独立分解自己的协方差或参数算子，

\[
K_\ell=V_\ell\Gamma_\ell V_\ell^\top,
\]

则 \(V_\ell\) 的第 \(j\) 秩和 \(V_{\ell+1}\) 的第 \(j\) 秩并不是一对已经对齐的
方向。特征值差或谱秩曲线差只能描述谱重分配。若要检验方向身份，需要在
共同环境坐标中比较投影空间重合或主夹角；但方向相同仍不能证明语义或
功能相同。

对中心化目标残差 \(R_Y\)，A15_08 定义

\[
K_{new}=C_{UY}S_Y^+C_{UY}^{\top},\qquad
C_{UY}=n^{-1}R_U^{\top}R_Y,\qquad
S_Y=n^{-1}R_Y^{\top}R_Y.
\]

\(K_{new}\) 相对 \(\Sigma_{R_U}+\rho I\) 的广义特征方向是合法的有监督候选
方向。\(K_{new}\) 是方向选择器，不是新知识本身；只有全新留出增益能准入
这些坐标。A15_07 的跨表达判别方案是另一个问题，继续保持暂停且未运行。

A15_08_01 明确不延伸这些广义特征方向。它在同一匹配世界和目标内定义不使用
目标 code 标签的长程交互更新：

\[
D_\ell
=(R_{U,\ell,2F}-R_{U,\ell,2N})
-(R_{U,\ell,1F}-R_{U,\ell,1N}).
\]

在每个 world 内对目标中心化后，令 \(\Sigma_{D,\ell}^{tr}\) 为 TRAIN
covariance；完整特征谱给出熵有效秩和覆盖 80% 方差所需的秩。跨层比较使用
拟议公共激活算子：

\[
\Sigma_{common}
=\frac1{36}\sum_{\ell=1}^{36}
\frac{\Sigma_{D,\ell}^{tr}}{\operatorname{tr}(\Sigma_{D,\ell}^{tr})},
\qquad
\Sigma_{common}=V_{common}\Lambda_{common}V_{common}^{\top}.
\]

trace normalization 防止一个高能量层垄断公共基，等层权使深浅层对基的定义
对称。每层在冻结公共秩中的累计能量只描述表征几何，不是对
\(G_{\ell,c}\) 的逐方向分解。

## 8. 命题状态

**命题 1——残差相减。**在严格匹配的 residual-stream hook 位置，
\(h_{\ell+1}-h_\ell\) 或一个具名 \(\Delta n_\ell\) 是有效计算差；它不自动
成为知识差。

**命题 2——协方差相减。**协方差差混合更新方差与旧状态—更新交叉项。
没有目标条件检验时，其特征方向不能被称为新增信息方向。

**命题 3——逐层本地谱秩。**相似本地谱形状不推出共同方向；共同方向也
不推出共同语义或功能。

**命题 4——条件新增可读性。**留出风险的正增益只支持目标、读出器和
数据范围内的结论；功能使用仍是独立条款。

**命题 5——当前有边界结果。**在首个合格记录 E04 中，对注册的
受控两跳目标与第 25 层 transition，条件新增可访问性在旧状态和同预算
竞争解释之外为正。两个注册方向有用但不充分：只保留 33.24%，低于
冻结的 80% 门槛。E03 是不合格的资格教训，不是本命题的证据。

**命题 6——已完成的扩展。**匹配的必要性×距离交互已在 blocks 2--36
隔离一般位置移动和一般两跳效应；TRAIN pooled 激活基可以让对应更新谱在
描述意义上可比。设计与一次四卡运行已获批并提交；在合格证据完成以前，
不存在深度规律或低秩结论。

这些是避免对象混淆的命题，不是“深层存在或不存在新增语义信息”的定理。

## 9. 机制分解

正确的因果顺序是：

\[
\text{参数公共坐标审核}
\rightarrow
\text{Attention-write 方差谱与粗中细 shape}
\rightarrow
\text{描述性语义几何}
\not\Rightarrow
\text{层新增信息}.
\]

真正裁定新增信息与功能的顺序是：

\[
\text{旧 token 局部状态}
\rightarrow
\text{具名层更新}
\rightarrow
\text{逐层目标条件下的增量可读性}
\quad + \quad
\text{描述性的表征秩轨迹}
\rightarrow
\text{可选的任务充分检索检验}
\rightarrow
\text{功能干预}
\rightarrow
\text{Router 设计}.
\]

跳过任一步都会重现 A15 的旧问题：把方差当信息、把信息当方向身份、把
方向身份当功能，或把功能当训练收益。

## 10. Anchor 证据链

| Parent | 当前最安全的认识 | 对主线的含义 |
| --- | --- | --- |
| A15_00 | 训练后 Gate 偏好可迁移高方差结构，同时仍能较弱地访问非 head | 访问几何真实，但不是语义选择器 |
| A15_01 | 受控系统中协方差各向异性会因果影响有限时间学习 | 学习速度不能替代有用目标 |
| A15_02 | Mean Response 基中粗<中<细，但深度后移依赖基、粗细曲线高度重叠且相邻层变化非单调 | 保留公共基作描述，停止用秩位置、固定谱段或归一化方差定义新增信息 |
| A15_04 | 注册的共享 broad tail 和预固定深 tail 语义进入解释均已关闭 | 参数稳定不是语义生成顺序 |
| A15_05 | 固定频带未通过兼容性或匹配质量准入 | 改变分发不是有用分发 |
| A15_06 | 本地谱方法存在单种子效果，但无可复现协方差身份凭证 | 不能用方法点估计反证频带语义 |
| A15_07 | 技术上已写明，研究者已暂停且未运行 | 作为独立非活跃方案保留，不拥有 A15_08 |
| A15_08 | E04 是首个合格的局部 H2 Pass 与二维 H1' Fail；A15_08_01 E01 为标准化 Insufficient，E02 为 `H2_LC_FAIL_CONTROL_DEGRADATION` | 决定是否用绝对 \(G_{\ell,2F}\) 替代交互增长；任务秩与功能继续暂停 |

## 11. 决定性实验事实

A15_02_06 的公共坐标链先给出一个正、一个负结果。Mean Response 基中的
fine-only 谱质心从早到晚增加 \(+0.03171\)，但 Rank Consensus 基为
\(-0.00755\) 且区间跨零，因此“深层后移”依赖公共基。冻结 Mean Response 后，
粗、中、细的轨迹级谱重心有序，fine-minus-coarse 为 \(+0.008175\)，但同层
coarse/fine 曲线大部分重叠：平均差异主要表现为谱头份额减少和较后多个离散
位置的小幅增加，而不是一个连续、唯一的 fine band。全部 35 个相邻层比较又
得到 16 个正、11 个负、8 个未决，否定逐层单调后移。该链支持参数响应排序与
语义粒度存在条件关联，但不支持用方差重分配定位新增信息。

在实际 \(\Delta n\) 中，平衡 taxonomy 审核得到可靠条件细粒度残差，但
fine-minus-coarse 的晚减早谱秩变化为 \(-0.009573\)，注册区间完全非正。
在匹配十层 taxonomy 实验中，更新单独可读，而它在旧状态之外的线性增益
近似为零。这直接说明“更新可读”与“条件新增”是不同对象。

共享 tail 审核复现本地后移，却发现全局共享 tail 富集从早到晚下降。
随后对预固定 128、256、512、2,048 维终端空间的审核发现：每个空间的
跨层参数重合都高于随机，但条件细粒度富集在每个宽度上都下降。稳定参数
几何不能追踪晚层语义进入。

固定频带匹配分发改变了 4.98%--21.88% 的路由，但所有真实频带的留出
next-token loss 都比完整模型自身 Router 更差。运动匹配的在线对照也没有
发现协方差谱秩身份跨两个随机种子的可复现优势。

2026-08-10 方差区间审核发现：选中区间内原始 attention 输出方差只有
residual/input 方差的 0.060--0.140，且相对同维随机方向没有稳定的
domain 来源分类优势。这关闭了当前方差增长选择器，但没有否定层新增
信息，因为方差大小和数据来源分类都不是目标条件新增性的必要度量。

A15_08 随后直接评估目标条件对象。E01 的 cyclic 对照是可逆目标重标记，
因此科学资格不合格；E02 修复了代数，却在 selection freeze 前打开了
confirmation labels，所以其数字仍只是诊断。E03 在全新 confirmation set 前
冻结了预定科学选择，但最终资格冷读发现四项 Protocol 合同没有实例化：
带命名空间的 `episode_id` 和 `map_id`、结构化特征提取回执、完整的简单条件
episode/bootstrap 数组，以及覆盖全部注册证据族的 manifest。因此 E03 为
`INELIGIBLE_GUARD`，它的所有数值只能作诊断。

E04 使用全新数据并只修复合规性：E02 冻结的科学对象、读出器、方向、
秩、阈值、对照族和决策规则都不变，只补齐上述四项合同。它是首个合格的
`H2_PASS_H1_FAIL` 记录。在 128 个复杂条件 episode 上，
\(G_{true}=0.767207\) \([0.751296,0.785146]\)、
\(G_{state}=0.754508\) \([0.738226,0.773069]\)、
\(T_{cap}=0.766839\) \([0.750643,0.784307]\)，因此局部 H2 Pass。两个
方向的 \(G_2=0.255052\) \([0.244938,0.264427]\)，保留完整点增益的 33.24%。
\(D_{80}=-0.358713\) \([-0.369760,-0.348675]\) 使注册的 80% 门槛失败。
\(T_{random}=0.034265\) \([0.024293,0.040979]\) 和
\(T_{perm}=0.234832\) \([0.224277,0.244831]\) 均为正，说明这两个方向在两类
注册同秩对照下并非空信号，但它们都不能挽救二维充分性。

另外的 E02 TRAIN-only 公共基诊断解释了为什么方差优先选择会误导；它只用于
描述，不是 E04 的资格门。复杂更新方差有 98.41% 落在 pooled ranks 1--256，
但两个目标条件候选方向在那里只有 37.90% 的平方质量，其质量中位秩为 374。
七个非零 \(K_{new}\) 特征值也较平，前两个只占总量的 31.17%。安全认识不是
“新增信息位于中段”，而是“原始更新能量在谱头集中，目标相关候选几何分布得
更广；完整功能位置仍未知”。

## 12. 反例与竞争解释

- **小方差但独有信号：**更新方差很小，仍可能稳定改变目标决策。
- **大方差但冗余信号：**更新单独容易读出，却不比旧状态提供更多信息。
- **谱形状稳定但方向旋转：**相似谱秩画像可与近乎正交的原始方向共存。
- **方向稳定但语义占据改变：**共享参数空间可保持稳定，语义富集却下降。
- **语义可分但没有功能：**有监督判别方向可以区分 child，却不能预测
  任务或专家收益。
- **有功能但没有预设谱身份：**有效干预不必对齐某个预选协方差频带。

合格 E04 在这个局部线性对象上排除了注册的“目标独立同预算支路”竞争解释。
E03 因记录不合格，在科学上不排除任何竞争解释。非线性新增、模型原生使用和
迁移仍是当前结论之外的开放竞争解释。

## 13. 结论边界

**已经建立：**A15 存在真实谱访问与学习动力学对象；语义表征随层变化；
本地谱秩、共享参数几何、固定频带分发和方差增长都不足以定义新增或有用
信息。对一个注册的第 25 层 transition，合格 E04 建立了目标和线性读出器族
限定的新增可访问性，并否定了注册的二维充分性。E03 只提供资格教训和诊断图样。

**尚未建立：**普遍的深层相对浅层规律；整个表征是低秩还是高秩；增量
普遍更长程或更细粒度；直接相减状态或协方差本身能够分离知识；任一方向
被模型原生使用；逐层 Router 能改善专家功能。

A15_08_01 已完成裁定。E01 暴露 block-1 旧状态结构性恒定，结论为
`H2_LC_INSUFFICIENT_STANDARDIZATION`。E02 评估 blocks 2--36 并通过全部资格
guard；\(T_{depth}=0.006102\)，区间 \([0.004119,0.007669]\) 为正，但
\(A_{2F}=-0.011422\)，区间 \([-0.013994,-0.009812]\)，注册 verdict 为
`H2_LC_FAIL_CONTROL_DEGRADATION`。表征秩非单调且只作描述。

**不得推出：**\(\Sigma_U\) 自动等于新增知识 covariance；conditional-fine
标签就是正确路由目标；方差选择器失败说明不存在层新增信号。

## 14. Anchor 分解与当前状态

- A15_03 未运行，现已归档并退出 active route；后续不再把 band 位置作为规划节点。
- A15_04 对共享 broad tail 和预固定终端 tail 的语义进入主张保持关闭。
- A15_07 保持 `parked_by_researcher_unrun`，没有科学 verdict。
- A15_08 是当前 active parent。E01、E02 和 E03 都是资格失败记录；E03 因没有
  实例化冻结的身份和记录完整性合同，保持 `INELIGIBLE_GUARD`。只修复合规性的
  全新 E04 是首个合格的 `H2_PASS_H1_FAIL` 记录。
- 旧状态、更新、目标、条件新增判据和二维门槛已经冻结并裁定；二维以上的
  最小充分任务读出秩仍未知，并已由研究者暂停。
- A15_08_01 E02 已在一个 TRAIN-only 激活数据公共基中完成 blocks 2--36。
  更强的必要性×距离交互没有对应更大的远程两跳绝对增益，因此交互增长不能
  充分证明深层拥有更多长程新增信息。

## 15. 与主线的关系

A15 通过判断一个表征坐标是否值得进入功能审核，服务于更大的功能专门化
主线。它不替代 A06 的专家收益合同，也不替代 A16 的负载控制机制。E02 已
表明相对交互趋势不足以进入功能审核；下一度量必须先保护目标单元的绝对增益。

## 16. 唯一下一决策

决定后续是否直接裁定逐层绝对 \(G_{\ell,2F}\)，并继续使用目标无关同预算修正
作为匹配对照。描述性表征秩以及暂不进入任务秩和 Router 的边界保持冻结。

## Source Map

- [A15 主线索引](../../problem_anchors/15_spectral_representation_and_functional_routing/README.md)
- [A15_02_05 平衡 taxonomy 结果](../../experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_05_E01_balanced_taxonomy_attention_write_atlas/summary.md)
- [A15_02_06 共享参数基与 Attention 投影](../../experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E02_shared_parameter_basis_attention_projection/summary.md)
- [A15_02_06 粗中细语义位置与曲线 shape](../../experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E03_shared_basis_semantic_granularity/summary.md)
- [A15_02_06 全相邻层变化](../../experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E05_all_adjacent_depth_transitions/summary.md)
- [0813 粗细曲线与 Top-K 候选日报](../../../../../daily_research_reports/backup/2026/08/0813/docs/daily_report_coarse_fine_spectral_shape_and_topk.md)
- [A15_02_07 匹配 taxonomy 结果](../../experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_07_E01_matched_taxonomy_full/summary.md)
- [A15_04 共享 tail 结果](../../experiments/A15/15_04_tail_band_information/A15_04_E01_shared_tail_geometry/summary.md)
- [A15_04 终端空间解耦结果](../../experiments/A15/15_04_tail_band_information/A15_04_E02_deep_tail_parameter_semantic_decoupling/summary.md)
- [A15_05 固定频带匹配分发](../../experiments/A15/15_05_functional_coordinate_admission/A15_05_05_E01_2b_matched_band_dispatch/summary.md)
- [A15_06 本地随机身份对照](../../experiments/A15/15_06_online_spectral_routing_and_relay/A15_06_E02_local_random_identity_control/summary.md)
- [A15_07 暂停且未运行 Anchor](../../problem_anchors/15_spectral_representation_and_functional_routing/15_07_layerwise_conditional_fine_discriminant_directions/15_07_layerwise_conditional_fine_discriminant_directions_anchor_cn.md)
- [A15_08 当前 Anchor](../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/15_08_target_conditioned_layer_innovation_anchor_cn.md)
- [A15_08_01 子 Anchor](../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_01_layerwise_long_range_compositional_innovation_anchor_cn.md)
- [A15_08_01 E02 结果](../../experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_01_E02_layerwise_long_range_gain_and_representation_rank_blocks_2_36/summary.md)
- [A15_08 E02 TRAIN-only 公共基记录](../../experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_E02_fresh_balanced_mismatch_repair/detailed.md)
- [A15_08 E03 资格教训](../../experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_E03_fresh_confirmation_freeze_repair/summary.md)
- [A15_08 E04 Protocol](../../experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_E04_strict_conformance_repair/protocol.md)
- [A15_08 E04 Summary](../../experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_E04_strict_conformance_repair/summary.md)
- [A15_08 E04 Detailed](../../experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_E04_strict_conformance_repair/detailed.md)
- [2026-08-10 组会记录](../../../../../daily_research_reports/backup/2026/08/0810/meeting_notes/note.md)
- [2026-08-10 方差区间报告](../../../../../daily_research_reports/backup/2026/08/0810/docs/DAILY_SUMMARY_ADVISOR_VARIANCE_INTERVAL_20260810.md)
