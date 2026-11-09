---
anchor_id: 14_02_02_low_frequency_common_mapping_rank
status: parked_stopped
canonical_language: en
canonical_file: 14_02_02_low_frequency_common_mapping_rank_anchor.md
parent_anchor: 14_02_relation_reuse_root_effective_rank
experiment_id: A14_02_E03_low_frequency_common_mapping_rank
protocol_status: not_retained_stopped
---

# A14_02_02 已学 common mapping 的低频调用与 ROOT 功能秩

父 anchor：
[A14_02 共享组合规则与任务 ROOT 状态功能秩](/Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/14_02_relation_reuse_root_effective_rank_anchor_cn.md)

researcher judgment record：
14_02 relation-reuse ROOT effective-rank researcher judgment record

协议状态：E03 已在批准或执行前停止，实验目录不保留 protocol。

## 1. Problem Definition

父问题要判断：保持 NTP 任务所需的 `ROOT` 状态方向数，更直接受任务函数复用
控制，还是受原始样本频率控制。E03 只裁定一个更窄的非蕴含命题：

> 在两个 common-mapping 条件都已经学会并复用同一个映射的前提下，把目标
> exact relation 的频率从 $F=8$ 降到 $F=1$，是否不会使固定读出 `ROOT`
> 功能秩增加超过两个方向？

这里不定义“一个样本的秩”。秩属于包含多个目标 relation 与多个 context 的冻结
评估切片。

### 决策相关术语

| 术语 | 直白含义 | 预注册对象 | 不能据此证明 |
| --- | --- | --- | --- |
| exact relation | 一个表面 alias 与一个 entity 的配对 | cell $t=(r,a)$ | 它就是一个独立任务函数 |
| $F_{\mathrm{exact}}(t)$ | cell $t$ 实际进入优化器的次数 | 有限训练流中的 realized count | 函数总曝光 |
| $E_{\mathrm{function}}$ | 所有 alias 与 entity 对同一底层映射的总调用数 | common 条件计数矩阵之和 | 单 cell 频率 |
| $K_{\mathrm{map}}$ | 模型必须区分的底层映射数量 | common 为 $1$；independent 为 $16$ | 神经模块数量 |
| common-mapping reuse | 不同表面 alias 调用同一个映射 | 每个 $r$ 都满足 $y=\pi(a)$ | 特定内部算法 |
| 固定读出功能秩 | 保持原始冻结输出头行为所需的最少、仅由 calibration 选择的正交 `ROOT` 方向数，并在互斥 test 上验证 | $k_{\mathrm{func}}^{\mathrm{fix}}$ | 严格矩阵秩、非线性内在维数或普适的绝对“低秩” |

## 2. Physical Priors

**P1 — 函数复用可以比局部频率更直接。** 若许多表面分支调用同一个已学
mapping，只出现一次的目标 cell 可以使用从其他调用中学到的方向；局部 rare
不必新增任务方向。

**P2 — common function 的总剂量是必须控制的竞争变量。** LowF 可能仅仅因为
其他 cell 给 common mapping 提供了更多更新而更容易。因此 E03 在两个 common
条件间严格固定 $E_{\mathrm{function}}$、逐 alias 总量、逐 entity 总量、逐 answer
总量、context 边际、token 数、batch 数与 optimizer step 数。

**P3 — 先证明能力，才能解释秩。** 如果模型不能解决目标 cell 或完全未见的
alias–entity cell，更小的秩不是压缩。common-mapping held-out 能力与 full-state
效用是 hard gate。

**P4 — 重训读出头会吸收缺失信息。** 训练后的原输出头保持冻结；主干预位置是
紧邻该输出头的 post-final-normalization `ROOT`。

**P5 — mapping 数量是另一个变量。** 匹配的 $K_{\mathrm{map}}=16$ 条件只提供
mapping-union 效应的方向参考，不能替代 $K_{\mathrm{map}}=1$ 下 LowF 与 HighF
的主比较。

## 3. Falsifiable Hypotheses

对 paired seed $s$ 定义：

$$
D_s
=
k_{\mathrm{func},s}^{\mathrm{Common,LowF}}
-
k_{\mathrm{func},s}^{\mathrm{Common,HighF}}.
$$

主操作化假设是非劣效命题：

$$
\mathbb E[D_s]\le \tau,
\qquad
\tau=2\ \text{个 ROOT 方向}.
$$

它表示在当前生成器中，低目标频率没有强迫产生有意义的秩膨胀；它不要求二者
严格相等。

**支持：**至少 8 个 paired seeds 同时通过全部 capability 与 intervention
guards；$\mathbb E[D_s]$ 的单侧 95% paired upper confidence bound 不超过
$2$；10 个 seed 中至少 8 个 paired passing seeds 满足 $D_s\le2$；并且 LowF
通过 unseen-cell common-mapping 门。

**否定：**所有 gates 通过后，单侧 95% paired lower confidence bound 大于
$2$。

**证据不足：**少于 8 个有效 pair；capability、matching、realized frequency、
replay、shuffle 或 random-subspace guard 失败；或者置信区间跨越 margin。

次级方向假设为：

$$
k_{\mathrm{func}}^{\mathrm{Independent,HighF}}
>
k_{\mathrm{func}}^{\mathrm{Common,LowF}},
$$

但它不能决定主 verdict。

## 4. Mathematical Model

### 条件概率树与任务映射

对于 alias $r\in\{0,\ldots,15\}$、entity $a\in\mathbb Z_{17}$ 和 nuisance
context $c$，common 条件中的一条路径是：

$$
r\rightarrow a\rightarrow c\rightarrow \rho\rightarrow y.
$$

16 个 alias 分支汇聚到同一个 mapping node：

$$
p(y\mid r,a,c)
=
\mathbf 1\{y=\pi(a)\}.
$$

因此 $r$ 是表面条件，不是新的任务函数。independent 参考条件为：

$$
p(y\mid r,a,c)
=
\mathbf 1\{y=\pi_r(a)\},
$$

其中有 16 张不同的 permutation 表。这样，实验反事实改变的是 mapping union，
不是答案词表。

### 曝光变量

对有限 realized stream $\mathcal S$：

$$
F_{\mathrm{exact}}(r,a)
=
\sum_{x\in\mathcal S}\mathbf 1\{x\text{ 使用 }(r,a)\},
$$

并且对任一 common 条件：

$$
E_{\mathrm{function}}
=
\sum_{r=0}^{15}\sum_{a=0}^{16}F_{\mathrm{exact}}(r,a).
$$

manifest 行数不能替代实际 optimizer presentation count。

### 固定读出功能秩

令 $h_\rho(x)\in\mathbb R^{64}$ 为 post-final-normalization `ROOT` 状态，并
冻结训练后的输出头 $W_o$。只在 basis-fit calibration 数据上学习有序正交基
$U$ 与仿射中心 $\mu$；在另一份 calibration-selection split 上选择 rank：

$$
\widetilde h_\rho^{(k)}
=
\mu+U_kU_k^\top(h_\rho-\mu).
$$

注册的 $k_{\mathrm{func}}^{\mathrm{fix}}$ 是 calibration-selection 上 loss
增加不超过 $0.02$ nat、accuracy 下降不超过 $0.01$，并且所有更高 rank
持续通过时的最小 rank。读取 final-test 标签前冻结该 rank 与 projection。
互斥 final test 必须继续通过相同阈值，否则该 run 不具备 rank validity。

这个量依赖任务、split、干预位置和容忍阈值；它不是单样本秩，也不是所有中间
计算的秩。

## 5. Computational Realization

冻结 64 个 target cells：

$$
\mathcal T_s
=
\{(r,(4r+j+o_s)\bmod17):r=0,\ldots,15,\ j=0,\ldots,3\},
$$

其中 $o_s$ 是预注册 seed offset。每个 alias 有 4 个 target；每个 entity 有
3 或 4 个 target。

另有两组互斥、训练中完全不出现的 64-cell 集合：

$$
\mathcal U_s^{cal}
=
\{(r,(4r+j+o_s)\bmod17):j=4,\ldots,7\},
\qquad
\mathcal U_s^{test}
=
\{(r,(4r+j+o_s)\bmod17):j=8,\ldots,11\}.
$$

每个 alias 有 8 个 held-out cells 和 9 个 observed cells；每个 entity 仍在
其他 4 或 5 个 aliases 下出现。每张 independent permutation 留出 8 项后，
正确的 permutation-completion chance baseline 是 $1/8$；若只留出两项，基线
其实是会误导解释的 $1/2$。

冻结 baseline $B=19196$。Common-LowF 对 target 赋 count $1$，对 unseen
赋 $0$，其余 cell 赋 $B$。Common-HighF 对 target 赋 $8$，并通过只作用于
非 target、非 unseen cell 的整数 transportation table $X$ 移走新增的七次：

$$
0\le X_{r,a}\le8,\qquad
\sum_aX_{r,a}=28,\qquad
\sum_rX_{r,a}=7t_a,
$$

其中 $t_a$ 是包含 entity $a$ 的 target 数。

因此两个 common 条件都严格具有：

- 每个 alias $95{,}984$ 次呈现；
- $1{,}535{,}744$ 次 common-function 调用；
- batch size $256$ 下 $5{,}999$ 个 batches；
- 相同的 entity 与 answer 边际。

训练流只做一次确定性 shuffle 后的完整遍历，不重采样。另一个整数 context
分配器固定全局 context 边际，并让两个 common 条件对每个 target cell 都只
使用同一个 target-training context；HighF 新增的七次为 exact duplicates。
common mapping 仍通过其他 cells 在 family-level diverse context pool 上获得
大量曝光。

independent 参考条件使用 16 张不同的 seed-random permutation 表；为了精确匹配
type 与 answer 边际，它们只对注册边际做联合条件化。这里的“independent”指
16 个需要分别记忆的函数，而不是施加边际约束后仍然无条件 iid 抽样。第二个
整数表把逐 alias、entity、answer、context、token 与 batch 边际全部匹配到
Common-HighF。

模型、初始化、优化器与功能秩机制继承 E01 配置：2 层、1 个 attention head、
width $64$、FF width $128$、full-position NTP CE、AdamW、学习率 $0.002$、
无 weight decay，以及 10 个 paired seeds。

## 6. Minimal Falsification Tests

1. **精确 frequency/function-dose 审计：**materialized count 与 optimizer
   realized count 必须一致；target 必须恰好为 $1$ 或 $8$；全部注册的 common
   条件边际必须严格相同。
2. **common-mapping 能力：**seen-target/new-context accuracy 至少 $0.95$，
   unseen-cell accuracy 至少 $0.90$，semantic consistency 至少 $0.95$，
   full-state CE 至多 $0.10$ nat，并且 10 个 paired common seeds 中至少 8
   个同时通过。
3. **固定读出功能秩：**在 post-norm `ROOT` 上比较 Common-LowF 与
   Common-HighF；冻结输出头，并使用互斥的 basis-fit、rank-selection 与
   final-test splits。
4. **干预有效性：**full-rank identity replay 必须精确恢复；`ROOT` shuffle
   必须破坏任务；同 rank random subspace 的通过数必须为零。
5. **mapping-count 参考：**Independent-HighF 必须在新 context 中学会 seen
   entries；完全未见的随机表项必须保持在注册 leakage guard 以下。

E01 的 rank curve 具有一个方向的分辨率，因此 $\tau=2$ 可测。E01 中临界的
full-rank replay 是浮点 identity reconstruction 问题，不是两个方向的 rank
不确定性。E03 保留 $0.02$ nat 与 $0.01$ accuracy 阈值，并要求 full-rank
路径直接返回未修改的 cached state。

## 7. Current Evidence

[A14_02_E01](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E01_shared_rule_vs_lookup_root_rank/summary_cn.md)
表明：每个 exact relation 只观察一个 surface 时，shared 与 lookup 条件都没有
获得 new-context capability；family-level diverse exposure 能够带来 capability，
exact duplication 单独不能。对 capability-passing lookup tasks，随着独立
mapping 数从 $K=1$ 增至 $4$、$16$，post-norm functional rank 均值从 $10.2$
升至 $11.0$、$12.8$。这个三点趋势有提示性，但没有分开全部 exposure rivals。

[A14_02_E02 历史结果](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/archive/e02_v1_component_recombination_capability/summary_cn.md)
在两个条件中都通过了 seen-pair new-context capability，却没有通过更强的 unseen
component-pair recombination gate：shared recombination 为 $0/5$ seeds 通过，
均值 $0.2125$。因此 E02 不允许得出 component composition 的 rank 结论。

E03 不重新解释这个失败。它改变了操作化问题：teacher 明确定义所有 aliases
调用同一个 mapping，held-out alias–entity cells 用来检验模型是否学会该 common
mapping。只有该 gate 通过后，出现一次的 target relation 才能被解释为复用了
从其他 relation 学到的函数。

整数设计在观察任何模型结果前已经可行。即使每个 alias 预留 8 个 unseen
cells，仍有 5 个 compensation cells。对 17 个可能的 target offsets，这些
cell 上的 common 条件注册 flow 都存在 value 为 $448$ 的整数解，恰好等于需
搬移的剂量。margin-conditioned independent 构造及其整数 reduction table 也
在 10 个预注册 seed layouts 的设计审计中全部可行。实现仍必须重做这些检查；
该审计不授权运行。

## 8. Claim Boundary And Next Decision

**若得到支持，唯一允许的主张是：**

> 在这个受控合成 NTP 任务中，固定底层 common mapping、函数总曝光、训练预算、
> 输出分布与评估合同后，把目标 exact-relation frequency 从 8 降到 1，没有
> 强迫模型增加超过 2 个固定读出 `ROOT` 功能方向。因此，低 exact frequency
> 不必然蕴含高功能秩。

**不允许：**frequency 永远不影响 rank；所有自然语言 rare facts 都复用 common
function；模型实现了显式树；该绝对 rank 在所有任务中都叫低秩；root-state rank
等于 parameter rank；或者 independent reference 单独证明了因果关系。

**唯一下一决策：**本已停放子 anchor 当前没有活动决策。只有在先建立一个通过
组合能力门的 shared 任务表面、且研究者重新选择 exact-frequency 问题之后，才
重新打开它。
