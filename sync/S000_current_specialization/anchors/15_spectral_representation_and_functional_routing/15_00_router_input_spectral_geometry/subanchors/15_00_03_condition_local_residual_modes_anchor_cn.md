---
anchor_id: 15_00_03_condition_local_residual_modes
parent_anchor: 15_00_router_input_spectral_geometry
status: complete_pass_conditional_modes_shared_envelope
created: 2026-07-31
canonical_language: en
thinking_card: 15_00_03_condition_local_residual_modes_thinking_card_cn.md
---

# A15_00_03 条件分层 residual 模式

## 1. Problem Definition

随机文档分片上，centered top-64 与去除它后的 residual top-64 都高度重合；这
不能区分“真正全局 residual”与“多个条件模式被随机混合后形成稳定 envelope”。

**唯一决策问题：** 在 Web of Science 的真实 domain/topic 标签下，同条件
independent halves 的 residual-64 projector 是否比跨条件 projector 更重合，
同时跨条件 basis 是否仍能捕获高于随机的 residual 能量？

## 2. Physical Priors

1. 同一条件重复出现的低维变化会形成可复现 projector。
2. 不同条件的 projector 可以旋转，但仍位于共同的高维 residual envelope。
3. 只有 overlap 低不足以说明条件模式；估计噪声也会同时降低 within overlap。

## 3. Falsifiable Hypotheses

**H1：条件低维模式。** within-condition overlap 高于 cross-condition overlap，
但 cross-capture 仍超过同维 complement-Haar q95；domain 主分析和 topic 嵌套复核
方向一致。

**R0：全局共享 residual。** within 与 cross overlap 都高且无稳定差距。

**R1：估计不稳定。** within 与 cross 都低，cross-capture 也不过随机。

**R2：标签样本伪影。** 标签置换或同样大小的随机组得到相同 within-cross gap。

**Pass：** domain 主分析的模型级 paired bootstrap 下界满足
$\Delta O=O_{within}-O_{cross}>0$，且 cross-capture 相对 Haar q95 的余量为正；
topic 方向复现。**Fail：** 精确支持 R0 或真实标签不超过置换/随机组。
**Insufficient：** within reliability、actual-input replay、样本量或谱秩护栏失败。

## 4. Mathematical Model

在独立、domain-balanced training abstracts 上估计 pooled top-64 $U_P$。对条件
$c$ 的两个独立训练半组 $A/B$，先投影到 $I-U_PU_P^\top$，再各拟合 residual
top-64 $U_c^A,U_c^B$。

$$
O(c,d)=\frac{\|U_c^{A\top}U_d^B\|_F^2}{64},\qquad
\Delta O=\operatorname{median}_cO(c,c)-
\operatorname{median}_{c\ne d}O(c,d).
$$

cross-capture 用 source condition basis $U_c^A$ 捕获 target condition $d$ 的独立
test residual covariance，并减去 target-specific complement-Haar q95。Overlap
回答“具体方向是否相同”；capture 回答“方向虽不同，是否仍落在可迁移 envelope”。

## 5. Computational Realization

[A15_00_03_E01 Protocol](/Projects/from-attention-to-search/main/experiments/A15/15_00_router_input_spectral_geometry/A15_00_03_E01_condition_local_residual_modes/protocol_cn.md)
使用 Gate 真正接收的表征、LB/decommon 40k/80k、全部 12 层。输入只包含
abstract；domain/area 标签只用于分组。domain 为 7 类主分析；每个 domain 取
跨 train/validation/test 均充足的前 4 个 area，组成 28 个嵌套 topic 复核。

## 6. Minimal Falsification Tests

1. 每个条件 A/B 文档互斥，均值来自 validation，capture target 来自 test。
2. 比较真实标签、标签置换、同大小随机组与 complement-Haar。
3. 同时报 centered top-64 与 residual-64，防止把所有谱方向都旋转误写成 residual 特异。
4. domain/topic 分开汇总；层不是独立种子。
5. 40k/80k 与 LB/decommon 分开报告，二者只作复现而非单变量因果对照。

## 7. Current Evidence

[条件分层实验](/Projects/from-attention-to-search/main/experiments/A15/15_00_router_input_spectral_geometry/A15_00_03_E01_condition_local_residual_modes/summary_cn.md)
在有边界的意义上通过 H1。LB/decommon 40k/80k 的 domain residual within
overlap 为 0.754--0.777，cross overlap 为 0.698--0.725；basis-refit bootstrap
区间为 0.032--0.044，2,000 次 domain-block 区间仍为正（0.019--0.069），而
相同大小随机分组 q95 只有 0.0012--0.0015。28 个嵌套 topic 方向复现。

但跨 domain basis 仍保留本地 capture 的 95.1%--96.4%，topic 层面保留
92.2%--93.8%。centered top-64 的绝对 overlap 更高，也同样随条件变化。因此
证据支持“高度共享 envelope 中的条件特异旋转”，不支持条件空间彼此隔离，也不
支持这种结构是 residual 独有。

已批准的单文档补测进一步细化了结论。Residual rank-64 overlap 在同 domain
文档间为 0.301--0.308、跨 domain 为 0.295--0.302，而 Haar q95 为 0.0939。
跨 domain capture 是同 domain 的 97.8%--98.1%，但只达到目标文档自身最优
rank-64 capture 的 32.7%--34.1%。不相交 token 的 rank-32 护栏显示：同一
文档两半 overlap 为 0.516--0.534，同 domain 不同文档为 0.173--0.181，跨
domain 为 0.168--0.177。因此精确局部模式确实变化，粗 domain 只解释小部分，
而总体 envelope 仍然共享。

## 8. Claim Boundary And Next Decision

本 anchor 只裁定条件分层后的表征几何；不能证明条件模式是语义因果、能改善
专家训练，或标签本身应输入 Router。结果否定了“decommon 失败是因为每个条件
暴露彼此不兼容 residual 空间”的强解释。

独立 2B 匹配频带实验现已显示：固定频带改变了路由，但没有改善相对 native
的 NLL。

**唯一下一决策：** 关闭固定 residual-band dispatch；未来 Router 表征必须先
通过直接面向专家更新或任务效用的功能准入。
