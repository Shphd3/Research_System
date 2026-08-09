---
story_id: A15_spectral_representation_to_functional_routing
status: current_primary_synthesis
updated: 2026-08-09
canonical_language: zh-CN
companion_en: 02_spectral_representation_to_functional_routing.md
---

# 从频谱表征几何到功能路由

## 1. 整线问题

A15 依次问三个问题：

1. 哪些频谱坐标真实存在并可被 Router 访问？
2. 一个具名坐标是否稳定承载可复现的表征信息？
3. 在匹配功能对照下，选取这些信息是否改善路由？

这个顺序是 claim boundary，不是实验时间线。几何现象不能跳过信息检验，信息现象也不能跳过功能准入。

## 2. 三种不可混用的坐标系

$$
C^{router}=\operatorname{Cov}(x^{router}),\qquad
C^{rep}=\operatorname{Cov}(z),\qquad
K_\ell=W_{gate,\ell}^{\top}W_{gate,\ell}+W_{up,\ell}^{\top}W_{up,\ell}.
$$

$C^{router}$ 描述 Gate 实际输入的可访问几何；$C^{rep}$ 描述一个明确激活对象（例如 residual 或实际 MLP 输入增量 $\Delta n$）的变化；$K_\ell$ 描述第 $\ell$ 层本地 MLP 输入参数几何。跨层同秩不等于同方向。

## 3. 已建立的认识

### 3.1 Router 输入几何不均匀，但不是无条件 head-only

[A15_00](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_00_router_input_spectral_geometry/15_00_router_input_spectral_geometry_anchor_cn.md)
说明 Router 输入协方差是有意义的访问坐标。实际输入、早期对齐和 common/residual 结果共同限定了 head 偏好、可迁移公共空间与条件局部结构。它们说明“能访问什么”，不说明“哪个频带具有语义功能”。

### 3.2 受控学习速度机制成立，真实形成过程仍有边界

[A15_01](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_01_spectral_learning_and_feedback_dynamics/15_01_spectral_learning_and_feedback_dynamics_anchor_cn.md)
保留协方差驱动的有限时间学习机制。真实轨迹比较因 load guard 失败而不足；selected-expert feedback 在受控任务中可锁定 head-first 分区；低方差会延迟而不会把可学习路由随机化。这些是形成动力学，不是频带语义。

### 3.3 表征随深度变化，但尚无统一参数秩语义坐标

[A15_02](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/15_02_layerwise_representation_spectral_atlas_anchor_cn.md)
整合受控/自然层级、attention head/channel、MLP 参数几何与匹配语义复杂度实验。若干具名对象存在深度可读性或方差画像变化，但证据没有把 later rank、middle 或 tail 验证为统一语义层级坐标，也不能用深度、effective rank 或频带位置直接定义组合性。

## 4. 两个独立的频带问题

### 4.1 Middle

[A15_03](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_03_middle_band_information/15_03_middle_band_information_anchor.md)
检验归一化 F2--F8 曲线“变化最小”究竟是真稳定，还是总方差归一化、middle 内部左右抵消、或逐层方向不稳定被按秩平均抹平。草案固定同一 512 样本与实际 $\Delta n$，比较绝对每方向方差、归一化份额、middle 内部细分曲线，以及 local/shared 对匹配 Haar 空间的捕获。它是独立的 `DRAFT_NOT_EXECUTABLE`。

### 4.2 Tail

[A15_04](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_04_tail_band_information/15_04_tail_band_information_anchor_cn.md)
检验本地参数秩后移是否进入跨层共享 F9--F16 方向，而不是只存在于各层本地排序或维数效应。它是当前活跃草案，仍为 `DRAFT_NOT_EXECUTABLE`，不具有功能结论。

Middle 与 tail 是两个同级父问题，互不作为对方的机制分支或实验 arm。

## 5. 功能准入是另一道门

[A15_05](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_05_functional_coordinate_admission/15_05_functional_coordinate_admission_anchor_cn.md)
拥有能力、兼容性与匹配 dispatch 证据。浅层 pilot 因能力饱和而不足；固定频带 cross-update compatibility 没有合格候选；匹配 2B dispatch 改变了路由分布，但没有通过注册的质量主张。旧条件训练 Protocol 因此从未运行并已归档。

目前只能说：已注册接口没有证明选取 middle/tail 信息带来模型质量增益。不能说所有频谱路由方法都无效。

## 6. 在线方法不能反推频带意义

[A15_06](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_06_online_spectral_routing_and_relay/15_06_online_spectral_routing_and_relay_anchor_cn.md)
拥有在线频谱路由、relay、本层随机身份对照与单 seed 扩展。这些结果只在各自合同下评价方法，不能倒推出 middle 或 tail 是稳定语义功能模块。

## 7. 数学与定理状态

当前没有“语义有用性随频谱秩排序”的定理。受控学习结果只支持冻结假设下的有限时间机制，不是训练后 Transformer 的定理。middle/tail 当前是带匹配随机对照的经验子空间，不是不变功能模块。

## 8. 当前边界与下一决策

整线当前可保留的结论是：

> 频谱几何会约束访问与学习，逐层表征在具名频谱坐标中呈非均匀变化；middle/tail 信息的方向身份与路由效用仍未解决。

唯一下一决策是审核 A15_04 的主指标、重采样设计和合取式 verdict。只有完成该几何决策后，才选择重开 A15_03，或把一个具名坐标送入 A15_05 功能准入。
