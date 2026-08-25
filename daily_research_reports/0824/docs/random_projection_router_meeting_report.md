---
status: AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
meeting_topic: qwen30b_all_layer_gain_and_random_projection_closure
date: 2026-08-24
canonical_result: ../../../Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_09_E02_qwen30b_all_layer_gain_and_preservation/summary.md
---

# 随机投影 Router：Qwen3-30B-A3B 全层重做后的理论—实验闭环

## 结论先行

**层选错确实是旧协议的问题，但不是旧结果失败的唯一原因。** 全 48 层重做后，$R_U$ 在 31 层对同层输入 $X$ 有统计稳定的新增标签预测效用，说明它绝不是“没有信息”。净增益最高的是 block 39，0.10994 nat/样本，48 层同时 95% 区间 [0.09872, 0.12080]。

但是，**新增信息不等于已经形成可独立路由的几何。** 按预注册规则从 H0 合格层中选出的 H3 主层是 block 48，重复层是 block 38；两层的 TEST 5% true-label margin 及其置信区间全部为负，H3 都 `Fail`。因此 H4 按理论依赖记为 `SKIPPED_H3_NOT_PASS`。这不是漏做投影实验，而是不能在负 margin 分母上解释“margin 保留率”。

最准确的认识更新是：

> **Qwen3-30B-A3B 的 $R_U$ 已携带相对 $X$ 的条件增量信息，但这些信息尚未被组织成 $R_U$ 单独可用的稳定正-margin Router 空间。**

所以建议确定开启“表征空间学习”，但目标要改准：不是从零创造信息，而是把已有的条件信息组织成与真实专家效用对齐的稳健路由表征，并与 joint $(X,R_U)$ 基线比较。当前 preservation 分支不再通过换层、换 probe 或改阈值重开。

外部边界仍在：19,200 条数据的机器守卫完成，64 条逐类 AI review 完成，但独立人工语义 review 未完成，所以 H1 总体仍为 `Insufficient`。本报告的认识更新与下一决策等待研究者确认。

## 1. 核心问题与对象

在 Qwen3-30B-A3B 的 block $\ell$ 和统一 `Answer:` 最后 token，定义

$$
R_{U,\ell}=U_\ell-(X_\ell\widehat B_\ell+\widehat b_\ell),
$$

其中 $X_\ell$ 是 Attention 写入前的同层归一化状态，$U_\ell$ 是 Attention 写入带来的归一化更新，括号内是 TRAIN 上由 $X$ 线性预测的更新。$R_U$ 因而表示“不能由写入前状态线性预测的更新部分”。

本轮分开回答两个问题：

1. $R_U$ 是否在同层 $X$ 之外增加标签预测效用？
2. $R_U$ 单独是否已经形成稳定正 margin 的线性 Router 空间？

前者是 H0 全层定位；后者是冻结层上的 H2/H3。只有后者 H3 通过，随机投影保持 H4 才有定义。

## 2. 理论证据

1. **已有结构的保持。** 对抽取随机矩阵前已经冻结的数据与 Router，足够维数的稠密高斯投影能以高概率近似保持有限样本的距离和正 logit margin。
2. **不能创造线性可分性。** 投影后线性 Router 可通过 $R^T$ 拉回原空间；线性投影后接线性分类器没有超出原空间线性函数族。
3. **实验依赖。** H4 的 normalized margin retention 需要正的完整空间 margin 分母，所以 H3 是硬门槛。
4. **“均匀”的边界。** 低相干只服务于随机谱坐标抽样，不是稠密高斯投影的前提；高谱熵也不能替代最大 leverage 相干度。

因此理论没有被实验“证伪”。实验只是在检查现实对象是否满足理论前提。

## 3. 为什么不能再固定 block 24/28

旧 24/28 层来自另一模型/旧扫描，不能直接迁移到 48 层 Qwen3-30B-A3B。E02 因此在 19,200 条冻结输入上重新抽取全部 48 层，并在 TEST 标签被删除的视图上完成选层。

每层先计算只用 $X$ 的基础预测，再加入 matched $R_U$；同时用重复 $X$ 排除“只是多一组线性参数”，用 30 个错配 $R_U$ 排除无样本对应关系时的偶然收益。受控净增益为

$$
T_\ell=G_\ell^{\mathrm{true}}-
\max\left(G_\ell^{\mathrm{dupX}},Q_{.95}\{G_{\ell,j}^{\mathrm{mis}}\}\right).
$$

H0 要求某层的 $T_\ell$ 在覆盖 48 层的同时置信下界严格大于 0。

## 4. 两种“最佳层”必须分开

| 含义 | Block | 直接结果 | 用途 |
|---|---:|---|---|
| 净增益最高层 | 39 | 0.10994 [0.09872, 0.12080] nat/样本 | 回答“哪里 $R_U$ 对 $X$ 增加信息最多” |
| 冻结 H3 主层 | 48 | 增益 0.01369 [0.00248, 0.02456]；DEV margin -0.52554 | 在 H0 合格层中最接近正低尾 margin，用于主 TEST 门槛 |
| 冻结重复层 | 38 | 增益 0.06442 [0.05320, 0.07529]；DEV margin -0.53000 | 与主层相隔 10 层的稳健性复现 |

为什么主层不是 39？因为下游要检验的是 $R_U$ **单独**的正 margin，而不是相对 $X$ 的最大新增交叉熵收益。冻结规则先要求 H0 合格，再按 standalone DEV 5% margin、准确率和较小层号排序。这个区分是本轮最重要的协议修正。

![Qwen3-30B-A3B 全层增益与门槛图](../../../Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_09_E02_qwen30b_all_layer_gain_and_preservation/figures/qwen30b_ru_layer_gain_curve.png)

读图：上图说明 block 12 以后出现一段广泛的正增益区，峰值为 39；下图说明所有层的 standalone DEV 低尾 margin 仍小于 0。紫线/金线分别是冻结重复层 38 和主层 48。

## 5. 全部实验与终态

| 顺序 | 实验或守卫 | 回答什么 | 终态 |
|---:|---|---|---|
| 1 | 冻结 taxonomy 与 19,200 条 binding 数据机器复核 | 是否存在直接词汇、重复或切分捷径 | 机器守卫 Pass；人工 review 未闭合 |
| 2 | unigram+bigram 词袋基线 | 廉价文本能否直接读标签 | TEST-same/new 0.1270/0.1195 |
| 3 | reserved 4×H100 48 层抽取 | 是否真正得到全部 $X_\ell,U_\ell$ | 48×19,200 完成；身份与代数守卫 Pass |
| 4 | 48 层 residualizer | 是否每层重算完整 $R_U$ | 48/48 完成，0 零方差坐标 |
| 5 | H0 逐层增益与控制 | $R_U$ 是否在 $X$ 之外增信息 | Pass；31/48 合格，峰值 block 39 |
| 6 | TEST-blind 层冻结 | 防止用 TEST 选层 | 主 48、重复 38，回执 Pass |
| 7 | H2 完整空间 accessibility | 是否高于 1/8 机会 | block 48 Fail；block 38 Pass |
| 8 | H3 正 margin admission | 是否已有稳健独立 Router 几何 | block 48/38 均 Fail |
| 9 | H4 高斯维数扫描 | 是否保持已存在的正 margin | `SKIPPED_H3_NOT_PASS` |
| 10 | 置乱、identity、common-offset 控制 | 排除实现与标签偶然性 | 全部 Pass |
| 11 | 全 TEST 样本对精确距离 | 是否存在类间大于类内的距离 gap | 四项 extreme/robust 比值全部 <1 |
| 12 | 监督正交功能秩 | fine-label 读出最小学习秩 | block 48/38 均 $r_{90}=64$ |
| 13 | 相干度与谱坐标资格 | “均匀”是否支持坐标抽样 | bound 83,892/114,975，正确跳过 |
| 14 | 图形与完整性审计 | 是否所有理论任务有终态 | 全部 artifact/semantic checks Pass |

正式作业 `pt-bo87sah1` 使用 reserved 单节点 4×H100，状态 `SUCCEEDED`。第一轮 smoke `pt-hilwjbo0` 因旧 BF16 tolerance 过严而失败并保留；修订后的 smoke `pt-y34d399q` 通过。实现测试为 51/51 通过。

## 6. 核心 TEST 结果

| Block | TEST | 平衡准确率 [95% CI] | 5% margin [95% CI] | H2/H3 |
|---:|---|---|---|---|
| 48 | same | 0.17125 [0.16484, 0.17813] | -5.82955 [-5.95216, -5.74825] | Fail / Fail |
| 48 | new | 0.12969 [0.12445, 0.13500] | -11.19046 [-11.40759, -11.06038] | — |
| 38 | same | 0.31016 [0.30203, 0.31805] | -3.52356 [-3.59236, -3.46685] | Pass / Fail |
| 38 | new | 0.23125 [0.22429, 0.23859] | -6.66276 [-6.79532, -6.54119] | — |

block 48 的 H2 Fail 来自 TEST-new 准确率下界 0.12445 没有严格高于机会水平 0.125。H3 的失败更直接：四个 margin 区间全部低于 0，并且准确率下界远低于 0.90。

## 7. 辅助证据

每个 TEST 面板精确枚举 3,275,520 个无序样本对：block 48 的 extreme $D_{out}/D_{in}$ 为 0.3321/0.2027，block 38 为 0.2314/0.2205；robust 比值范围 0.5315--0.7026。全部低于 1，说明类内/类间距离集合严重重叠。

监督正交 fine-label 学习在两层都得到 $r_{90}=64$，但完整 64 类 TEST 准确率仍弱。相干度为 block 48 的 2.04、block 38 的 3.56，对应 Haar 均值约 1.71；高熵不等于完全均匀。TRAIN-only 坐标抽样充分维数远超 1,024，因此扩展分支停止。这些都只是诊断，不能改变 H0--H4。

## 8. 证据链与认识更新

$$
\text{排除词袋捷径}
\rightarrow \text{48 层 H0 增量信息存在}
\rightarrow \text{standalone DEV 低尾 margin 全负}
\rightarrow \text{冻结层 TEST H3 失败}
\rightarrow \text{精确距离无 gap}
\rightarrow \text{H4 无合法前提}.
$$

旧认识“要压缩的结构完全没有形成”太粗。新认识要分两层：

- **信息层面：形成了一部分。** $R_U$ 相对 $X$ 确实增加了标签可预测性，而且不是单点层现象。
- **几何层面：还没形成。** $R_U$ 单独没有稳定正低尾 margin，也没有类间—类内距离 gap。

所以当前根本问题不是“随机投影维数选错”，也不只是“block 24/28 选错”，而是：**条件信息没有被组织成与路由决策一致的独立稳健空间。**

## 9. 能说、不能说、下一决策

可以说：Qwen3-30B-A3B 的多层 $R_U$ 对 $X$ 有受控增量信息；在冻结的最佳 H3-readiness 层和分离重复层，standalone $R_U$ 没有通过稳定正 margin 门槛，所以本轮没有可解释的随机投影保持结论。

不能说：$R_U$ 无信息；48 层都已在 TEST 上被穷举判定不可分；joint $(X,R_U)$ 没用；非线性 Router 不可能；parent taxonomy 就是真实专家效用；满足正 margin 前提时高斯投影仍会失败。

**建议确认开启表征空间学习。** 最小新实验应以真实专家效用或可审计 proxy 为目标，比较 learned standalone representation 与 joint $(X,R_U)$，先要求真正 held-out 两面板的 5% margin 置信下界 $>0$。若不通过就停止；若通过再讨论随机压缩。该决策与认识措辞仍需研究者确认，且独立 H1 review 必须闭合。

## 10. 证据位置

- 理论正文：[`random_projection_router_proof_protocol (1).md`](random_projection_router_proof_protocol%20(1).md)
- E02 [`protocol.md`](../../../Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_09_E02_qwen30b_all_layer_gain_and_preservation/protocol.md)
- E02 [`summary.md`](../../../Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_09_E02_qwen30b_all_layer_gain_and_preservation/summary.md)
- E02 [`detailed.md`](../../../Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_09_E02_qwen30b_all_layer_gain_and_preservation/detailed.md)
- 全 48 层表：[`layer_scan.csv`](../../../Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_09_E02_qwen30b_all_layer_gain_and_preservation/tables/layer_scan.csv)
- 正式 raw run：worker root 下 `runs/e02-all-layer-full-20260824T014000Z/`
