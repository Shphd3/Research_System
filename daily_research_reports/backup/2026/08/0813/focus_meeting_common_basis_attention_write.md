# 公共基能否定位层新增信息？Mean Response 补充了什么？

```text
type: meeting_knowledge_update
status: AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
scope: one_problem
```

**来源范围：**[组内 feature 汇总](/root/.codex/attachments/f54505c8-3e5d-49df-86e3-b69a7c5b1972/feature.md)、[共享参数基结果](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E02_shared_parameter_basis_attention_projection/summary.md)、[语义粒度结果](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E03_shared_basis_semantic_granularity/summary.md)、[全相邻层结果](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E05_all_adjacent_depth_transitions/summary.md)。

**排除范围：**本次不设计或训练 Router，不讨论低秩充分性，也不把后续目标条件读出实验并入当前公共基结论。

## 1. 本次组会主题与核心问题

**主题：**从组内多种跨层比较实验出发，明确公共基的作用、失败边界及 Mean Response 的有限增量。

**核心问题：**现有证据是否支持用一组公共基定位不同层的“新增信息”；如果不支持，Mean Response 基仍然可靠地告诉了我们什么？

## 2. 当前认识更新

现有结果不支持把任意一组共享正交基上的方差后移直接解释为层新增信息。共享基解决的只是“让不同层投到同一批向量上比较”，并不保证同一方向在各层具有相同语义，也不定义旧状态中没有的目标信息。Mean Response 提供了一个比纯激活基更明确的参数侧标尺：它按照各层 MLP 对 residual 输入方向的平均归一化参数响应排序；在这把特定标尺上，语义越细，Attention-write 的归一化方差位置在整条深度轨迹上统计地越靠后。但该关系依赖基构造、不是逐层定律、不能定位唯一细粒度谱段，也不能把 Attention-write 直接认证为新增信息。

## 3. 递进回答

### 3.1 共享正交基能否稳定定位深层新增信息？

当前不能。ZX 使用最后层表征基、词表头坐标和跨层 pooled-SVD 基，均未观察到预期的稳定后移；残差的 raw variance 还系统性高于 Attention-write。这个结果否定的是“随便找到一把共享正交尺子，方差后移就会显现”的朴素路径，而不是证明深层没有新增信息。

CCA 路径进一步放松了“相同向量方向”的要求，改为寻找浅层和深层之间最大相关的成对方向，再把深层不可线性预测的残差当作候选。MLP 输入上候选残差包含非随机 domain 信号，但 raw Attention 输出上没有稳定超过 random/shared-old；同层 residual→Attention 的不可预测部分也没有表现出更强 domain 区分性。因此问题不只是某一种公共基选错了：二阶方差或线性不可预测残差本身都还不能定义新增语义。

这使下一问变成：能否构造一把至少具有清晰参数意义、而不是为了观察后移而选择的公共尺子？

### 3.2 Mean Response 为什么是一把有意义但有限的公共尺子？

每层定义

$$
K_\ell=W_{gate,\ell}^{\top}W_{gate,\ell}+W_{up,\ell}^{\top}W_{up,\ell}.
$$

对单位 residual 方向 $v$，$v^\top K_\ell v$ 等于 gate/up 两条 MLP 输入投影的总平方参数响应。逐层 trace 归一化、等层平均并特征分解后，公共 rank 表示“跨层平均归一化 MLP 参数响应由强到弱”。所有层使用同一个向量 $v_j$，所以方向身份在代数上相同；激活数据不参与造基，也避免为了得到某个现象而调坐标。

它不是各层真实共同特征谱。各层 $K_\ell$ 都是半正定矩阵，求和不会发生正负能量相消；真正风险是各层偏好的强方向不同，平均后各向异性被抹平。例如一层只偏好横轴、另一层只偏好纵轴，平均矩阵可能接近各向同性，从而失去唯一方向。正式坐标审计也只显示它比 Haar 随机方向略有更多局部谱结构，不是对所有层的同时对角化。

因此还必须问：在这把预先有意义的尺子上，观察到了什么可复述的结构？

### 3.3 Mean Response 上有哪些可靠结果？

第一，fine-only Attention-write 从浅层到深层的谱质心在 Mean Response 基上后移，但在丢弃参数增益、只保留跨层谱带秩共识的基上不后移。因此“随深度后移”是 basis-sensitive 描述，不是公共谱的不变量。全 35 个相邻层比较进一步呈现正负交替，没有单调深度斜率。

第二，在冻结 Mean Response 基内比较 coarse、medium、fine，轨迹级谱质心满足 coarse < medium < fine。fine−coarse 在 blocks 1--35 的中位质心差为 $+0.008175$，95% parent-bootstrap 区间为 $[+0.001964,+0.012620]$；两个表达半集同号。点估计在 28/35 个 block 为正，但若干逐层区间跨零。固定 `[0.50,0.75)` 的 fine−coarse 方差份额也为正，不过相邻区间同样为正，不能据此认证唯一的“细粒度谱段”。

这些结果只支持：在当前数据和 Mean Response 排序下，细粒度语义变化的归一化方差分布整体更靠后。它不支持绝对能量更多、每层都成立、某个具体方向具有稳定语义，或 Attention-write 已被证明是旧状态之外的新信息。

### 3.4 这些证据如何共同回答核心问题？

公共基仍有用，但角色必须降级并说清：它是跨层比较和描述“候选更新相对参数几何落在哪里”的标尺，不是新增信息的定义。ZX 的结果排除了简单的基不变后移叙事；CCA 结果表明放松成对坐标后，Attention 候选残差仍缺少稳定功能区分；Mean Response 则保留了一个更窄的正认识——参数响应排序与语义粒度存在 basis-conditioned 关联。

## 4. 边界与唯一下一决策

- **已经理解：**Mean Response rank 在当前 Qwen3-8B taxonomy 数据上具有可复现的语义粒度关联，因而可继续作为解释性参数坐标。
- **仍不能说：**它找到了跨层通用的新增信息谱带、证明深层逐层增加更细语义，或给出了可直接用于 Router 的方向。

**唯一下一决策：**是否结束“继续寻找能产生统一后移的公共基”这条主线，把 Mean Response 固定为描述性坐标，并把“新增信息”的主判据改为相对旧状态的留出目标增益。

**完成标准：**组会明确接受或拒绝上述角色划分；若接受，后续任何谱带都必须先证明在旧状态之外保留目标可访问性，再谈 Router。

**恢复动作：**把汇报中的“寻找新增信息公共基”改写为“公共坐标审计 + 新增信息定义仍待功能化”，并用下述个人补充口径结束本段。

**完整来源：**[A15 当前自包含 story](/data/250010109/Research_System/Projects/from-attention-to-search/main/stories/15_spectral_representation_and_functional_routing/02_spectral_representation_to_functional_routing_cn.md)。
