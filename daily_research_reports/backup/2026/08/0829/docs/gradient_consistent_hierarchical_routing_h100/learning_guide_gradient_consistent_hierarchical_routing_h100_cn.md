---
type: learning_guide
status: HUMAN_CONFIRMED
created: 2026-08-29
scope: A15_11 E01H and E03H H100 successor evidence
---

# 学习导读：从“语义方差”走到“功能残差与专家效用”

## 0. 你最终要真正想透的一句话

> **正确层级可以把一个全局非线性问题拆成局部简单问题，但只有“可拆”还不够；必须相对一个能学同一非线性交互的平坦基线证明更省样本，并且必须把语义可读、Router 可读、专家有用和功能变好分别测量。**

如果只记一个学习提示，就从下面这个反问开始：

> work 与 fail 明明包含完全相同的四个教师函数，为什么只改变它们与父类标签 $p$ 的配对，父类优先树就从近零误差变成约 $1/3$，而平坦非线性 Router 两边都能到近零？

能独立回答这个问题，再解释 Qwen 的 $H\rightarrow Z\rightarrow Q$ 为什么只是一条“访问链”而不是“效用链”，你就掌握了本轮全部工作的主轴。

## 1. 先认清五个对象

| 对象 | 白话定义 | 本轮怎么测 | 不能替代什么 |
| --- | --- | --- | --- |
| 语义标签 | 研究者给出的父类或细类名字 | `parent_id`、$p$、$b$ | 不等于模型功能 |
| 隐藏表征可访问性 | 固定读出器能否在未见模板上读出标签 | Qwen 隐藏状态 $H$ 的跨模板线性探针 | 不等于 Router 使用 |
| Gate 可访问性 | 原生门控接口是否保留该读出 | 128 维 Gate 分数 $Z$ 与 top-8 稀疏路由 $Q$ | 不等于专家有用 |
| 反事实专家效用 | 同一样本改用等算力候选专家能减少多少损失 | 合成任务的逐候选损失改善 | 不等于自然语义 |
| 功能收益 | 方法是否以更少样本或同预算得到更低测试误差 | 无噪声归一化均方误差及学习曲线面积 | 不等于几何重叠 |

本导读中的缩写第一次出现时按下面理解：

- **平衡准确率（balanced accuracy，BA）：**先算每个类别的召回率，再取类别平均；八类随机机会值为 $1/8=0.125$。
- **归一化均方误差（normalized mean-squared error，NMSE）：**预测平方误差除以目标信号平方能量；0 是精确预测，$1/3$ 表示遗漏总信号能量的三分之一。
- **学习曲线面积（area under the learning curve，AULC）：**在累计训练样本数的对数坐标上积分 NMSE；越小表示越早学会。
- **混合专家（mixture of experts，MoE）：**由 Router 选择少数专家处理每个样本的条件计算模型。
- **Gate：**Router 中产生专家分数的门控层；Qwen 此处是 2048 维到 128 维的无偏置线性投影。
- **C4 / C5：**两个各含 1,920 行的受控表达面板；它们共享同一批语义原子，必须分别得到相容判决，但**不是**两个统计独立的重复实验。
- **机会校正 Gate 保留率 $R_Z$：**$R_Z=(BA(Z)-0.125)/(BA(H)-0.125)$；它把 Gate 分数高于八类随机机会值的可访问性，除以隐藏状态高于机会值的可访问性，不能解释为因果信息保留比例。
- **路由—标签关联 $I_Q(Y;E)/H(Y)$：**先把每个样本的 top-8 路由质量看成对专家索引 $E$ 的条件分布，计算父类标签 $Y$ 与 $E$ 的互信息，再除以父类熵；它只测关联，不测所选专家的功能效用。
- **置换空参照（permutation null）：**保持路由与样本不变、打乱父类标签后得到的关联或准确率参考分布；超过它只能排除当前标签交换参照，不能建立因果使用。

## 2. 第一遍：只用 20 分钟建立全景

先读 [组会主线](focus_meeting_gradient_consistent_hierarchical_routing_h100.md)，只回答四个问题，不查公式：

1. 08:28 组会否定的是哪条“语义层级 $\rightarrow$ 方差层级”推理？
2. Qwen 审计定位的是哪个接口，不定位哪个功能？
3. 合成实验中“机制通过”和“方法优势失败”为什么可以同时成立？
4. 本轮为什么应该停止架构推广，而不是追加超参数补救？

读完后，请尝试用自己的话复述：

```text
原错误前提是什么？
唯一问题是什么？
两个直接结果是什么？
唯一认识更新是什么？
不能声称什么？
下一决策是什么？
```

如果这六句还会混用“可分”“相关”“有用”，不要进入代码，先回到第 1 节。

## 3. 第二遍：用 60--90 分钟想透理论

### 问题 1：父类覆盖更广，为什么不保证在主成分头部？

总协方差可以写成

$$
\Sigma_H
=\Sigma_{between\ parent}
+\Sigma_{between\ child\mid parent}
+\Sigma_{within\ child}.
$$

混合父类会增加第一项，但主成分分析只看三项之和的最大特征值。父类能量还可能分散在最多 $K-1$ 个均值方向，而一个词元、模板或细类因素可以独占更大的单一特征值。因此

$$
\text{父类贡献方差}
\not\Rightarrow
\text{父类方向是最大方差方向}.
$$

自测：构造一个二维协方差，其中父类只在纵轴相差，但横轴的类内变化为纵轴的十倍。第一主成分会选哪个轴？父类还能否被纵轴分开？

### 问题 2：出现频率为什么也不够？

设父类相关梯度在不同细类和语境中的条件平均为

$$
m=\mathbb E[g\mid parent].
$$

频率增加的是梯度样本数。若 $m\neq0$，更频繁会更快积累稳定方向；若不同细类的梯度正负抵消使 $m=0$，更多样本只会把估计更准确地压向零。于是更准确的链是

$$
\text{任务持续需要某因素}
+\text{跨语境梯度不抵消}
\rightarrow
\text{共享特征形成},
$$

而不是“语义更粗或出现更多，所以激活方差必然更大”。

### 问题 3：固定线性映射为什么不能创造线性可分性？

若 $z=Ax+c$ 后存在分类器 $w^\top z+b$，那么

$$
w^\top(Ax+c)+b=(A^\top w)^\top x+(w^\top c+b)
$$

已经是原空间的线性分类器。因此线性投影可以删除方向、改善有限样本正则化或数值条件，却不能扩大线性函数族。

自测：为什么“投影后 held-out 准确率变高”仍不反驳这个命题？提示：区分函数类的可实现性与有限样本估计误差。

### 问题 4：什么映射能真正暴露新决策？

取独立二值变量 $p,b\in\{-1,+1\}$，令 $q=pb$，Router 看见 $s=(p,q)$。细类 $b=pq$ 是异或关系，不能由一个全局仿射超平面恢复；固定 $p$ 后却有

$$
b=pq,
$$

即分支内只需读取 $q$ 的符号。非线性交互特征 $pq$ 或父类条件化都能暴露它，但平坦非线性 MLP 也能学会。因此决定性基线不是线性模型，而是参数和计算匹配的平坦非线性 Router。

### 问题 5：X-MoE 式余弦 Gate 为什么也没有自动解决异或？

若专家分数为

$$
s_e(h)=\frac{(Wh)^\top e_e}{\|Wh\|\|e_e\|},
$$

同一样本的 $\|Wh\|$ 对所有专家相同。专家 $i,j$ 的比较只取决于

$$
h^\top W^\top
\left(\frac{e_i}{\|e_i\|}-\frac{e_j}{\|e_j\|}\right),
$$

任意两专家的边界仍是超平面。它能改变 Router 可见的行空间、去掉专家向量范数竞争和改变优化条件，但余弦归一化本身没有给单个分数加入 $pq$ 这样的非线性交互，因而**不自动保证**恢复异或或目标层级。这里不能再加强成“一般多专家 Router 无法实现异或”：多个线性选择 cell 若被不同专家输出重新组合，可以形成非凸决策区域；一标签一专家的二选一边界与多专家整体函数类不是同一个命题。参考原始论文：[Chi et al., NeurIPS 2022](https://papers.nips.cc/paper_files/paper/2022/file/df4f371f1f89ec8ba5014b3310578048-Paper-Conference.pdf)。

### 问题 6：$1/3$ 下界到底依赖什么？

先固定解析 oracle 的全部条件：$p,b\in\{-1,+1\}$ 独立等权、四个状态各占 $1/4$、$q=pb$；输入是各向同性标准高斯且无噪声；误差是四状态算子 Frobenius 误差的精确高斯期望；共同专家精确为 $C$，后继残差与冻结祖先方向精确正交。再取三个单位秩一算子

$$
C=u_0v_0^\top,\quad A=u_1v_1^\top,\quad B=u_2v_2^\top,
$$

并要求左右奇异向量分别正交：$u_i^\top u_j=0$ 且 $v_i^\top v_j=0$。这叫**双正交**，比仅有 Frobenius 内积为零更强。

> 重要勘误：仅说 $\langle A,B\rangle_F=0$，不能推出 $A+B$ 的秩为二；两个秩一矩阵可以 Frobenius 正交但共享左向量或右向量，使和仍为秩一。E03H Protocol 和实际生成器使用前三个对角坐标投影，满足双正交，所以本次定理与实验有效。共享理论速记中的简写不能作为证明。

定义

$$
\Theta^{work}_{p,b}=C+pA+bB,
\qquad
\Theta^{fail}_{p,b}=C+qA+bB.
$$

work 和 fail 的四个教师函数多重集完全相同，只改变与 $p$ 的配对。work 有精确分解

$$
C\longrightarrow pA\longrightarrow bB.
$$

fail 先按 $p$ 分支时，由 $b$ 在每个固定 $p$ 内等权，父层条件均值为零，叶层必须拟合

$$
qA+bB=b(pA+B).
$$

双正交使 $A+B$ 有两个都等于 1 的非零奇异值。由 Eckart--Young 最佳低秩逼近定理，任何秩一叶至少遗漏一个单位能量；$C,A,B$ 的总信号能量为 3，所以

$$
NMSE^{oracle}_{H,fail}=\frac13.
$$

这是解析 oracle 的精确值。实际 float32 训练的注册护栏是 learned fail 端点不得低于 $1/3-10^{-4}$；观测中位端点为 $0.336926$，只应说它通过容差护栏并贴近 oracle，而不是训练值精确等于 $1/3$。

自测：这个下界为什么不能外推到状态不平衡、非各向同性输入、可复用祖先方向、秩二叶专家、可改第一层分组或不冻结的普通 MoE？

## 4. 第三遍：用 60 分钟读懂 Qwen 审计

先读 [E01H Summary](../../../../Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E01H_qwen_native_router_access_gap_h100/summary.md)，再读 [E01H Detailed](../../../../Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E01H_qwen_native_router_access_gap_h100/detailed.md)。

### 4.1 三个矩阵对象

对每个固定层和最终决策 token：

- $H\in\mathbb R^{1920\times2048}$：缓存的原生 MoE 输入；
- $Z=HW_g^\top\in\mathbb R^{1920\times128}$：冻结 Gate 的 BF16 分数；
- $Q\in\mathbb R^{1920\times128}$：只保留 top-8 softmax 权重并重新归一化的稀疏路由。

对三个对象使用相同样本、标签、完整模板族划分、交叉拟合探针、正则选择和评分。这样 $H-Z$ 只定位 Gate 投影损失，$Z-Q$ 只定位稀疏选择损失。

### 4.2 看图时回答的问题

读 [平衡准确率阶梯图](../../../../Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E01H_qwen_native_router_access_gap_h100/figures/balanced_accuracy_ladder.png)：

1. 黑线 $H$ 是否在五个确认层都高于八类机会值 0.125？
2. 蓝线 $Z$ 与黑线的差是否小？
3. 红线 $Q$ 是否大幅下降但仍高于机会值？
4. 为什么第 44 层灰色标记不能进入结论？答案：它在 Protocol 冻结前已被看过，是 `PILOT_NOT_BLIND`。

读 [访问性缺口图](../../../../Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E01H_qwen_native_router_access_gap_h100/figures/accessibility_gaps.png)：蓝柱是 $BA(H)-BA(Z)$，红柱是 $BA(Z)-BA(Q)$。判决不用肉眼大小，而用成组自举区间：

- 投影保留：$R_Z$ 的 95% 下界至少 0.90，且投影损失 95% 上界至多 0.05；
- 实质选择损失：选择损失 95% 下界至少 0.10；
- 路由关联保留：$I_Q(Y;E)/H(Y)$ 高于五确认层最大统计量的 97.5% 标签置换阈值。

下文表格中的 `P/S/A/N` 依次表示：Gate 投影保留（projection preserved）、top-8 实质选择损失（material selection loss）、路由关联保留（retained association）、近乎完全稀疏保留（near-total sparse retention）。前三项共同定义主判决；`N` 是“其实没有瓶颈”的竞争轮廓。

### 4.3 结果要会复述到什么精度

- 五个确认层中 4/5 在 C4、C5 同时满足投影保留、实质选择损失和关联保留；两个面板共享语义原子，所以这是跨表达面板一致性要求，不是两次独立复现；
- 5/5 有实质选择损失，5/5 有关联保留，0/5 近乎完全保留；
- $BA(H)=0.9948$--$1.0000$，$BA(Z)=0.9417$--$0.9984$，$BA(Q)=0.4047$--$0.5635$；
- BF16 和 FP32 给出同一行判决；
- 所以结论是“top-8 selection bottleneck with retained association”，不是“Gate 不含语义”，也不是“专家有正确功能”。

自测：为什么 $Q$ 与父类有关联仍不能说明该父类对应专家能降低语言模型损失？请构造“Router 按主题分，但所有专家函数相同”的反例。

## 5. 第四遍：用 90 分钟读懂合成实验

先读 [E03H Summary](../../../../Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E03H_counterfactual_utility_residual_tree_h100/summary.md)，再读 [E03H Detailed](../../../../Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E03H_counterfactual_utility_residual_tree_h100/detailed.md)。

### 5.1 四个实验臂

| 名称 | Router 结构 | Router 监督 |
| --- | --- | --- |
| `H_task` | 给定父类的 $1\rightarrow2\rightarrow4$ 条件树 | 只用任务损失 |
| `H_util` | 同一条件树 | 任务损失加在线反事实效用交叉熵 |
| `F_task` | 参数匹配的平坦非线性 Router | 只用任务损失 |
| `F_util` | 同一平坦 Router | 任务损失加相同效用交叉熵 |

四臂拥有相同七个秩一专家、初始化、数据流、每阶段 128 步、候选前向次数、Router 参数和推理激活专家数。每格参数为 550，其中专家存储参数 448、激活专家参数 192、Router 参数 102；训练候选专家 FLOPs 为 7,340,032，单样本推理总 FLOPs 为 544。

### 5.2 五个对比的符号

$$
S_H=A(H_{task})-A(H_{util}),\qquad
S_F=A(F_{task})-A(F_{util}),
$$

$$
A_T=A(F_{task})-A(H_{task}),\qquad
A_U=A(F_{util})-A(H_{util}),
$$

$$
X=S_H-S_F.
$$

因为 AULC 越小越好，$S_H,S_F>0$ 才表示效用监督有益，$A_T,A_U>0$ 才表示层级有益。先判断符号，再看 95% 区间是否完全高于零，最后检查端点没有恶化。

### 5.3 三层裁定

1. **机制：通过。**`H_task` work 端点 $1.94\times10^{-5}$，fail 端点 0.336926；fail-minus-work AULC 为 0.053155，区间完全为正。
2. **效用监督：不通过。**work 的 $S_H=-0.012057$、$S_F=-0.005792$，两个区间均在零下方；额外效用项反而减慢训练。
3. **层级收益：未建立。**work 的 $A_T=-8.21\times10^{-5}$，区间跨零；本次注册检验没有建立 `H_task` 相对 `F_task` 的正收益，也不是两者普遍等价的证明。$A_U$ 同样未建立正收益。

机器的汇总标签是 `GENERIC_NONLINEARITY_OR_UTILITY_SUFFICIENT`。不要机械翻译成“效用监督足够”：独立效用判决全部失败。更窄的读法是“在这个生成器与固定预算中，平坦非线性已足以达到近零误差，且没有建立层级正收益”；这不是普遍充分性或方法等价定理。

## 6. 第五遍：用 45--60 分钟理解失败底层原因

看 [逐种子失败模式图](../../../../Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E03H_counterfactual_utility_residual_tree_h100/figures/companion_seed_failure_modes.png)，不要只看中位学习曲线。work 的 `H_util` 八个种子分成：

- 1 个用齐四叶，到近零；
- 4 个只用三个叶，停在约 $1/6$；
- 3 个在父层单路坍缩，最终只用一个叶，停在约 $2/3$。

与逐种子能量、负载和遗憾账本相容的**最窄解释链**是：

```text
当前尚未学好的专家产生效用标签
-> argmax 标签停止梯度，只直接训练 Router
-> hard top-1 只把任务梯度送给被选专家
-> 未选专家得不到学习，平衡批中的相反残差还会相消
-> 零或已有专家继续被判为当前最优
-> Router 与专家形成自我强化的饥饿状态
-> 阶段冻结把早期错误永久传给下一层
```

这条链不是唯一因果定理。本实验没有分别干预效用交叉熵、任务直通梯度、负载平衡、初始化与阶段冻结，也没有固定 oracle 效用标签、强制探索或专家预训练修复臂；这些因素的份额需要新的已注册实验才能拆开。

关键认识不是“Router 看不懂效用”。一些失败种子对**当前候选集合**仍有很高路由准确率和很低遗憾，但候选集合本身没有学全函数。因此

$$
\text{正确选择当前候选}
\not\Rightarrow
\text{候选集合完整}.
$$

自测：为什么同初始化、同数据流的 `H_task` 在 work 中 8/8 成功，使“容量不足”不是最强解释？为什么它仍不能证明其他稳定化效用目标必然失败？

## 7. 第六遍：用 30 分钟练习组会表达

不要从实验设置开始。按下面六句练习，每句都必须带边界：

1. 我们原先把语义层级误写成了方差层级；父类分类依赖共享属性，不要求父类方向支配 PCA。
2. 冻结 Qwen 中，父类在隐藏状态和 Gate 分数里几乎可读，主要访问损失发生在 top-8 选择，但这不是专家效用。
3. 我们用同一组四个函数只改变父类配对，构造了 work 和 fail；正确树有精确分解，错误树有 $1/3$ 秩一下界。
4. 任务损失树复现了这个机制，所以导师 intuition 的条件容量版本成立。
5. 平坦非线性 Router 同样到近零，在线效用监督降低表现并伴随专家饥饿模式；饥饿是最窄证据相容解释而非已分离的唯一原因，所以当前方法优势未成立。
6. 研究者已确认停止架构推广，先用“每个样本中父类相关预测事件的重复次数（高/低）乘以跨细类梯度一致性（高/低）”检验父类方向与未见模板低尾间隔如何形成；总预测位置数保持不变，低频条件的其余位置换成匹配的中性事件。08:28 的 Oracle/Search 路线和此前 Anchor 的软期望效用路线已停放。

如果导师追问“那 Qwen 呢”，只回答：

> Qwen 结果定位了语义访问接口，不执行替代专家，所以真实专家效用和语言模型损失仍未知；本轮没有把两条证据拼成因果结论。

## 8. 36 小时可执行阅读表

| 时间 | 任务 | 必须产出的自答 | 停止条件 |
| --- | --- | --- | --- |
| 0--2h | 读组会主线和两份 Summary | 六句主线初稿 | 能分开直接结果与解释 |
| 2--6h | 手推协方差、频率平均梯度、线性映射边界 | 三个反例各一页 | 不再说“粗语义必在 PCA 头部” |
| 6--10h | 手推 XOR 与双正交 $1/3$ 定理 | 从 $b=pq$ 推到 Eckart--Young | 能指出仅 Frobenius 正交为何不足 |
| 10--14h | 读 E01H Protocol/Summary/Detailed 和三张图 | 独立填写 10 个确认单元的 P/S/A/N 表 | 能说清 H、Z、Q 与 null |
| 14--20h | 读 E03H Protocol/Summary/Detailed | 手算五个对比的正负含义 | 不再把机制通过说成架构通过 |
| 20--24h | 读逐种子表和 companion 图 | 画出 $0,1/6,1/3,2/3$ 的来源 | 能复述专家饥饿解释及未分离的竞争原因 |
| 24--28h | 检查 guards、资源和产物清单 | 一张“什么会使证据无效”的清单 | 能区分失败结果与无效运行 |
| 28--32h | 对照 08:28 组会原文和 PDF 审慎清单 | 写出三条被否定的旧假设 | 不引用二维图替代高维证据 |
| 32--35h | 两次五分钟口述和一次反方追问 | 录下或写下最终汇报 | 每层结论都有 cannot claim |
| 35--36h | 用自己的话复述已确认边界并冷读日报 | 直接结果、更新判断、不能声称、H100 非 owning 归属和唯一 $2\times2$ 下一决策 | 能从日报数字回到 Summary/Detailed，并指出它不是 5090 的 H100 执行 |

## 9. 来源地图

按“先结论、后证据、再实现”的顺序：

1. [组会主线](focus_meeting_gradient_consistent_hierarchical_routing_h100.md)
2. [理论补充](theory_supplement_separability_and_residual_routing_h100_cn.md)
3. [Qwen E01H Summary](../../../../Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E01H_qwen_native_router_access_gap_h100/summary.md)
4. [Synthetic E03H Summary](../../../../Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E03H_counterfactual_utility_residual_tree_h100/summary.md)
5. [Qwen E01H Detailed](../../../../Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E01H_qwen_native_router_access_gap_h100/detailed.md)
6. [Synthetic E03H Detailed](../../../../Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E03H_counterfactual_utility_residual_tree_h100/detailed.md)
7. [E01H Protocol](../../../../Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E01H_qwen_native_router_access_gap_h100/protocol.md)
8. [E03H Protocol](../../../../Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E03H_counterfactual_utility_residual_tree_h100/protocol.md)
9. [08:28 组会逐句校订](../../../0828/docs/0828组会_逐句校订与下一步研究方向.md)

[feature (9).pdf](<../../../0828/docs/feature (9).pdf>) 只作为观点清单，不作为决定性证据。阅读时逐条守住：稀疏自编码不自动证明局部低秩；线性判别分析的 $K-1$ 是类均值子空间的代数上界，不是语义内在秩；二维可视化、距离比例或单一探针 margin 都不能越过各自的测量边界。

对话 `学习可分性理论` 已于 2026-08-30 通过连接器完整读取，共五个已完成回合且无更早分页。它把上游机制问题明确写成“频率 $\rightarrow$ 跨细类梯度一致性 $\rightarrow$ 判别方向形成 $\rightarrow$ 谱位置”，并把表示形成检验置于 common、残差树和完整 MoE 之前。本轮 E01H/E03H 是用户随后明确要求的下游压力测试；不能据此改写原组会顺序。对话内附件正文未随线程返回，附件证据仍以本地文件为准。所有数值和判决以冻结 Protocol、最终 H100 Summary/Detailed 与原始完成审计为准。

### 9.1 `feature (9).pdf` 应该怎样审慎使用

| PDF 位置 | 它直接记录了什么 | 本轮允许怎样使用 | 不能推出什么 |
| --- | --- | --- | --- |
| 第 2、13--15 页 | 去掉粗类方向后 loss 变差，完整表征路由基线未被超过，最大方差方向不是粗类判别方向 | 作为旧的线性删除与 PCA 路线失败背景 | 不能据此证明任何非线性层级 Router 必然成功或失败 |
| 第 3 页 | 稀疏自编码器用少量字典原子重构单个 token，并观察到跨 token 激活差异 | 作为“局部稀疏字典可能存在”的候选观察 | 稀疏重构不等于局部低秩，更不证明字典层级就是语义树 |
| 第 7、21--22 页 | 有监督判别方向不在 PCA 头部；粗细 Fisher 判别子空间及跨父类细分空间缺少超空参照重合或迁移 | 支持“方差、监督读出与跨域复用必须分测” | 不能把 Fisher 的至多 $K-1$ 维代数上界称为语义内在秩，也不能从低重合推出功能完全不同 |
| 第 23--24 页 | 平均探针准确率高于随机，但 5% 低尾 margin 为负，距离比小于 1；固定线性降维不能创造可分性 | 支持“信息存在不等于严格正间隔”与线性映射边界 | 一个注册探针下的负 margin 不能证明所有线性读出都失败，更不能证明语义不存在 |
| 第 25--26 页 | 有标签低秩投影可在较小秩恢复分类表现，方向更靠近中谱段 | 作为监督低维任务子空间的存在性证据 | 不能当作无监督可发现性、原生 Router 使用或因果功能收益 |
| 第 27--28 页 | 两个选定层的新增更新在受控读出中带来增益，且少量 PCA 维保留部分效果 | 作为层间访问性候选证据和后续审计线索 | 不能外推到所有层、训练机制、专家效用或真实 MoE 收益 |

因此，这份 PDF 在本轮承担的是**问题清单与负面边界**，不承担 E01H/E03H 的判决；后者只由冻结协议、最终 H100 原始产物和完成审计裁定。

## 10. 最终自测答案边界

你准备好汇报的标准不是能背数字，而是能同时说出：

- **直接结果：**Qwen top-8 是访问性瓶颈；合成机制通过，但注册检验未建立层级或在线效用监督的正收益。
- **解释：**正确分组解决了条件容量，但平坦非线性已经能学交互；逐种子模式与“在线效用标签和未成熟专家共同自我强化”的最窄解释相容，但未证明它是唯一原因。
- **不能说：**不能外推自然语义树、真实 Qwen 专家效用或语言模型损失。
- **已确认的唯一下一决策：**停止当前架构推广，先做频率乘以跨细类梯度一致性的最小表示形成检验；只有四个条件都不能形成正间隔时，才进入层级语义先验比较。Oracle/Search 与软期望效用路线已停放。

你已经确认结果、边界、路线裁定与 H100 归属：当前 5090 Focus 只接纳 H100 为碰撞隔离、non-owning 的敏感性证据，不把它写成该 Focus 的 H100 执行。本目录的 daily report 因而可以形成，但在你完成整篇冷读前仍保持 `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`。
