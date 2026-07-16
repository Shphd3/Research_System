# Thinking Card — A06_04：真实工作负载中的专家效用余量

> Migrated from [06_04_real_workload_utility_headroom_anchor_cn.md](06_04_real_workload_utility_headroom_anchor_cn.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**现象：** 受控实验已经得到“一个 challenger 完成发现、下尾效用证书结束探索”的机制原型，但真实大语言模型任务中是否存在足够大的专家功能差仍未知。若不存在功能差，继续设计语义 Router 没有现实目标。

**机制猜想：** 仓库级代码补全中的跨文件符号、类型约束、应用程序接口族和编程语言可能产生不同的计算需求，使某些专家在独立测试集上对特定条件具有稳定的强制执行损失优势。

**关键变量：** 未筛选代码位置、条件分层 $z$、混合专家层 $l$、强制专家损失 $L_{z,l,e}^{cf}$、独立测试集上的最优专家稳定性、原生 Router 损失和激活计算量。

**因果关系：** 校准集选择每个条件下损失最低的专家；独立测试集判断该专家身份和优势是否重复，并且是否优于原生 Router 与负载匹配对照。

**主要指标：** 独立测试集上的 oracle routing headroom，即“原生 Router 损失减去校准集所选专家的测试损失”：

$$
G_{oracle,l}
=L_{native,l}
-\sum_z p(z)L_{z,l,a_l(z)}^{cf,test}.
$$

**竞争解释：** 差异只来自词元身份、长度、频率或负载；逐词元选择过拟合；强制专家造成分布外扰动；专家实际上功能可互换。

**决策：** 只有未筛选样本上的 held-out headroom 稳定为正且通过对照，才进入新的 Router 设计；否则停止该工作负载上的语义 Router。
