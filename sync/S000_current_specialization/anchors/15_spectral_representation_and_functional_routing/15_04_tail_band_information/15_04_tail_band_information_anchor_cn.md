---
anchor_id: 15_04_tail_band_information
legacy_anchor_id: 15_01_11_shared_tail_semantic_relocation
status: researcher_band_partition_confirmed_metric_pending
canonical_language: en
companion_language: zh
thinking_card: 15_04_tail_band_information_thinking_card_cn.md
parent_line: 15_spectral_representation_and_functional_routing
updated: 2026-08-09
---

# A15_04 共同参数秩后移是否进入跨层共享的广义 tail

研究者判断：[Thinking Card](15_04_tail_band_information_thinking_card_cn.md)。英文主 Anchor：[anchor](15_04_tail_band_information_anchor.md)。

## 1. 问题定义

A15_02_07 没有得到稳定的复杂减简单参数秩后移，也没有证明条件新增线性信息。当前保留的现象是：实际 MLP 输入增量中的条件细类语义方差，随深度共同移向本层较后的参数秩。A15_02_06 同时观察到 U 形的跨层参数几何，最低增益端尤其对齐；但这两个观察可以同时成立而彼此无关。

研究者现已固定完整频谱为 16 个等宽的 256 维参数段：F1 是 **head**，F2--F8 是 **middle**，F9--F16 是 **tail**。这取代了旧稿中“只把 bottom-256 称为 tail”的提案。

**唯一决策问题：**

> 对冻结 Qwen3-8B 中 attention 引起的实际 MLP 输入增量，晚层条件细类方差是否比早层更富集于跨层共享的广义 tail F9--F16，并且超过同维随机几何、共享 head F1 和共享 middle F2--F8，同时完整显示 F1--F16 的变化形状？

表征固定为 $\Delta n_\ell=RMSNorm_\ell(x_\ell+a_\ell)-RMSNorm_\ell(x_\ell)$。语义对象是每个大类内部的小类中心方差，再对八个大类等权平均。样本固定为 A15_02_06 的 512 条，结论只对这组有限样本成立。

通过只允许另立功能 Protocol；失败关闭广义共享 tail 解释；证据不足只允许修复来源或估计。

## 2. 物理先验

1. 向后参数秩迁移是完整频谱上的质量重分配，因此必须给出全部 16 个 band；单看最低端不能区分“广泛迁移”与“只在一个端点集中”。
2. head、middle、tail 的原始捕获比例不能直接比较，因为维度分别是 256、1,792、2,048。任意固定协方差在同维随机空间中的期望捕获分别为 $1/16$、$7/16$、$8/16$，公平比较必须除以各自的随机期望。
3. 几何富集不等于 MLP 使用。低增益空间可以包含可读方差，却几乎不改变当前 MLP 输出。

16 段及 H/M/T 划分是 `HUMAN_CONFIRMED`。下面的“随机期望归一化”广义参数段指标是等待 Protocol 审核的 `AI_PROPOSAL`。

## 3. 可证伪假设

**G0——现象门。** 条件细类 $\Delta n$ 方差的完整本地 F1--F16 频谱，仍呈现正的早层到晚层秩重心后移，并在两组封存表达中同向。

**G1——广义共享 tail 几何。** 校正参数段维度后，晚层条件细类方差在跨层共享 F9--F16 tail 中的富集增量，大于共享 F1 head、共享 F2--F8 middle，也大于匹配随机频谱分区。

**最强竞争解释。** tail 的表面优势仅来自维度更大、一般的跨层共享方向，或只存在本地参数秩重分配而没有共同方向。它预言维度校正后不存在 tail 特异富集。

F1--F16 的单段曲线负责定位形状，不是 16 个独立主假设，也不能挽救失败的广义 tail 判定。

## 4. 数学模型

令 $P_{\ell,k}$ 为本层第 $k\in\{1,\ldots,16\}$ 个 rank-256 参数段投影。定义本地广义投影

$$
P_{\ell,H}=P_{\ell,1},\qquad
P_{\ell,M}=\sum_{k=2}^{8}P_{\ell,k},\qquad
P_{\ell,T}=\sum_{k=9}^{16}P_{\ell,k},
$$

其秩分别为 $r_H=256$、$r_M=1792$、$r_T=2048$。把层划为两个深度平衡且互不重叠的层组。测量层位于组 $f$ 时，只用另一组构造共享广义空间：

$$
M_G^{(-f)}=\frac{1}{|-f|}\sum_{j\in-f}P_{j,G},\qquad
Q_G^{(-f)}=\operatorname{TopEig}_{r_G}(M_G^{(-f)}),
$$

其中 $G\in\{H,M,T\}$。每个 F1--F16 也按同样方法单独构造 rank-256 的共享投影 $Q_k^{(-f)}$ 并完整报告。

对条件细类协方差 $B_{\ell,F}$，广义空间的原始捕获和维度归一化富集为

$$
c_{\ell,G}=\frac{\operatorname{tr}(Q_GB_{\ell,F})}{\operatorname{tr}(B_{\ell,F})},
\qquad
e_{\ell,G}=\frac{c_{\ell,G}}{r_G/4096}.
$$

$e=1$ 是同维随机期望。定义早层到晚层的富集变化

$$
T_G=\operatorname{median}_{\ell=25:35}e_{\ell,G}
-\operatorname{median}_{\ell=1:12}e_{\ell,G},
$$

以及提议的主 tail 特异统计量

$$
D_T=T_T-\max(T_H,T_M).
$$

$D_T>0$ 表示维度校正后，广义 tail 随深度的增长超过另外两个参数区域；它不能证明功能。

## 5. 计算实现

1. 固定 A15_02_06 的 512 条样本；由于旧 response 产物只有本层特征坐标，必须用确定性回放补存原始 4096 维 $\Delta n_\ell$。
2. 固定 16 个宽度为 256 的本地参数段。每层、每段都报告：类别间绝对每方向方差、本地归一化方差份额、共享-band 捕获，以及相对随机期望的共享-band 富集。
3. H/M/T 的共享广义空间按上式单独构造。不能把 16 个独立共享-band 的 capture 直接相加，因为这些跨层共识空间未必仍相互正交。
4. 1--35 层按奇偶分为互斥构造/测量组；第 36 层只描述。
5. 每次随机抽样构造一个正交的随机 16-band 分区；其 F1、F2--F8、F9--F16 的并集分别提供同维 H/M/T 随机对照。同一个随机分区用于所有层。
6. 使用封存的 design/confirmation 表达半集，并按 parent/template 分组估计不确定性；方向和层不能当独立样本。

完整 16-band 数据是强制证据；广义 H/M/T 汇总承担唯一裁定。

## 6. 最小证伪测试

| 裁定 | 可检查规则 | 路线含义 |
| --- | --- | --- |
| Pass：`broad_shared_tail_geometry` | G0 成立；广义 tail 的 $T_T$ 为正并超过同维随机区间；$D_T$ 的 95% 下界为正；奇偶待测层和两组表达不反转广义 tail 符号 | 允许另立功能检验 |
| Fail：`local_random_or_nontail_relocation` | G0 成立，但广义 tail 不超过同维随机，或维度归一化增量不大于 head/middle，或只有本地 F1--F16 重分配 | 关闭广义共享 tail 解释 |
| Insufficient | 原始 $\Delta n$ 回放、G0、共享 tail 估计或表达/层组可靠性不稳定 | 只修复来源或估计 |

决定性反例不是“F16 是否很高”，而是维度匹配后，F9--F16 广义共享空间是否具有 tail 特异的深度富集。

## 7. 当前证据

1. A15_02_06 的 native rank-256 head/middle/tail 重合度为随机期望的 2.20/1.04/3.26 倍；完整 band 曲线呈 U 形，最低增益端最强。这只提供动机，不能证明新的广义 F9--F16 语义结论。[结果摘要](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E01_mlp_parameter_geometry_and_semantic_location/summary.md)
2. 实际 $\Delta n_\ell$ 的 raw 条件细类本地参数秩重心从早层 0.370 移到晚层 0.471。这是本地秩重分配，不是跨层方向身份。
3. A15_02_07 的 [TAX](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_07_E01_matched_taxonomy_full/summary.md) 与 [COMP](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_07_E02_controlled_composition_full/summary.md) 都没有得到稳定的复杂特异后移或条件新增线性信息。

广义共享 tail 几何检验尚未执行。

## 8. Claim 边界与下一决策

即使 Pass，也只能声称：在这 512 条冻结样本上，晚层条件细类几何比早层更富集于跨层共享 F9--F16 低增益空间，并超过同维随机、F1 head 和 F2--F8 middle。不能声称知识存储、非线性编码、MLP 传递、任务效用或 Router 收益。

**唯一下一决策：**批准或修正改版后的 16-band Protocol 指标与裁定规则。**完成标准：**Protocol 强制给出全部 F1--F16 的 raw 与 normalized 数据，另报 H/M/T 的 raw capture 与随机期望归一化富集，冻结同维随机分区，并且不从 16 个 band 中事后挑选结果来决定广义 tail verdict。**恢复动作：**全部 Protocol 块显式确认后，再分别申请实现与 smoke 权限。
