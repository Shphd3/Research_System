# Protocol：A14_E01 理论、稳定性与反例审计

## 0. 批准快照

批准状态：研究者已于 2026-07-18 明确授权直接实现与执行。

目的：验证代码严格实现低秩传播定理，量化含噪稳定性，并重现删除关键假设后的反例。

主 anchor：
[A14 中文 anchor](/Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_00_tree_low_rank_language_structure/14_00_tree_low_rank_language_structure_anchor_cn.md)

实验角色：指标与实现审计。

主要指标：

$$
V_{\max}=\max_{c,s,\ell}
\frac{\Delta_k(H_\ell)-B_\ell}{\max(\|H_\ell\|_F,10^{-12})}.
$$

- Pass：$V_{\max}\le10^{-5}$，且精确条件每层相对 $\Delta_k\le10^{-6}$。
- Fail：双精度复算后仍越界。
- Insufficient：运行不完整、出现非有限输入，或秩指标单元测试失败。
- 不能声称：真实语言或预训练 Transformer 满足定理前提。

## 1. 核心设置

使用 $d=128,k=8,L=6$、512 棵根树的平衡二叉 forest。叶子数为 32,768，避免 $n<d$ 的形状低秩。

$$
H_0=ZU^\top+\sigma N(I-UU^\top).
$$

父节点平均两个不重叠孩子，$\|A_\ell\|_2=1/\sqrt2$。令
$W_\ell=cQ_\ell$、$c=g\sqrt2$，从而实现目标 $g$。创新残差按实测范数进入理论界。

## 2. 条件

精确条件：$\sigma=0$、创新为 0，$g\in\{0.5,1,1.5\}$，3 个种子。

含噪条件：

- $\sigma\in\{0,0.01,0.03,0.1\}$；
- $\delta\in\{0,0.01,0.05,0.1\}$；
- $g\in\{0.5,0.9,1,1.1,1.5\}$；
- 种子 0--9。

反例：共享/节点特异变换、平均/求和的算子范数、逐层正交新方向、DAG 子节点复用 $q\in\{1,2,4,8\}$。

## 3. 可证伪规则

1. 精确低秩与零创新必须逐层保持 rank-$k$。
2. 所有含噪条件必须满足 $\Delta_k(H_\ell)\le B_\ell$。
3. 节点特异变换和正交创新必须能把秩提升到样本/环境上限。
4. 在固定噪声构造下，更大 $g$ 应产生更大的根部绝对传播残差。

## 4. 输出

`metrics.parquet`、`summary.json`、理论界/实际误差曲线、根部 tail-energy 热图和反例表。

## 5. 边界修正

原讨论中“求和必然比平均具有更高相对尾部能量”并非定理结论，因为共同缩放也会放大信号。这里冻结的有效检验是：求和提高聚合算子范数与绝对误差上界。
