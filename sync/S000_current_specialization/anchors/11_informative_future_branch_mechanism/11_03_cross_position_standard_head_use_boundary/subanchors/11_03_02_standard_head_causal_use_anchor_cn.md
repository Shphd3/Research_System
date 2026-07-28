# 信息性未来目标的标准主头因果使用审计 Anchor

状态：已完成；所有守卫通过，信息内容的强行为因果使用增量按预注册规则失败。

Thinking Card source: [11_03_02_standard_head_causal_use_thinking_card_cn.md](11_03_02_standard_head_causal_use_thinking_card_cn.md)

## 1. 问题定义

父问题：[11_03 跨位置标准主头使用边界](../11_03_cross_position_standard_head_use_boundary_anchor_cn.md)。

父 Anchor 已经证明，当前位置形成有用信息不足以保证后续标准主头行为。本子 Anchor 询问一个更强、尚未解决的因果问题：相对于活跃头数、CE 项数和名义 loss 系数匹配的 shared-aux，信息性 K=2 MTP 是否增强了 `<DECIDE>` 源状态对后续普通下一词元主头的因果控制。NTP 只保留为次要系统基线。

### 术语解释

| 术语 | 通俗含义 | 具体对象或计算 | 决策作用 | 不能证明 |
|---|---|---|---|---|
| 源状态 | `<DECIDE>` 位置可供后续词元注意力读取的信息 | 预注册的源位置注意力记忆 $S_o(x)=\{K_{\ell,T},V_{\ell,T}\}_{\ell\in\mathcal L}$ | 因果干预对象 | 每个分量都只由 MTP 学成 |
| 接收体 | 保留自身输入、后续词元和标准主头输出的样本 | 分支为 $z$ 的样本 $r_z$ | 固定后续计算 | 泛化能力 |
| 异分支供体 | 提供不同分支源状态的真实样本 | 在同一个模型中把 $d_{z'}$（$z'\neq z$）补入 $r_z$ | 检验定向反事实控制 | 单独证明 MTP 特异性 |
| 同分支供体 | 与接收体分支相同的独立匹配样本 | 把 $d_z$ 补入 $r_z$ | 测量替换造成的无关扰动 | 清除所有分布外效应 |
| 标准主头因果使用 | 只改变源通道就使普通主头朝供体答案改变 | 正常处理 `<SHARED>` 后的反事实答案切换 | 强于可读性或梯度对齐 | 真实任务收益 |
| 受控切换效应 $C_o$ | 目标 $o$ 下，供体定向切换率减去无关变化率 | 第 4 节定义；单位为概率差 | 模型内部使用指标 | 目标函数间优势 |
| shared-aux | 第二头重复预测与主头相同的下一词元目标 | 两个活跃全词表 CE 头，loss 取平均 | 控制辅助头/辅助损失的存在 | 真实梯度相同 |
| 信息内容增量 $\Gamma_{info}$ | informative-MTP 受控效应减去 shared-aux 受控效应 | $C_{info\text{-}MTP}-C_{shared\text{-}aux}$；单位为概率差 | 唯一主要指标 | 被补状态完全由 MTP 独占 |
| 能力匹配 | 主比较两个标准主头以相近水平解出干净任务 | 预注册准确率区间和干净正确接收体集合 | 排除学习程度混杂 | 内部算法或真实梯度相同 |

**唯一决策问题：** 在受控 A11 K=2 分支任务中，相对于训练结构匹配的 shared-aux，信息性 MTP 是否增强了后续标准下一词元主头对 `<DECIDE>` 源状态的因果使用？

## 2. 物理先验

1. **使用必须表现为因果依赖。** 如果后续标准主头使用源状态中的分支通道，那么在保持接收体后续输入不变时，换入真实的异分支供体应使答案朝供体分支移动。若有效替换不改变主头，该先验被削弱。
2. **分别训练后的表示坐标只在模型内部有意义。** 结构相同不代表 NTP 与 MTP 训练后的隐藏基相同。干预必须分别在各模型内部完成，目标间只能比较标量因果效应。跨模型补状态只会破坏实现合同，不能证伪机制。
3. **辅助训练结构是仍然存活的竞争解释。** 仅比较 NTP/MTP 时，额外活跃头、第二项 CE 和未来目标内容同时变化。shared-aux 匹配前两者，因此区分“信息内容”的是 $\Gamma_{info}$；NTP 差异只能作为系统基线。

## 3. 可证伪假设

**主要假设：** 信息性 K=2 MTP 在匹配辅助训练结构之外，增强从 `<DECIDE>` 源状态到后续标准主头的因果通道。因此在能力匹配条件下，$\Gamma_{info}>0$，并满足预注册的种子一致性和高于控制噪声的最小效应要求。

**最强竞争解释：** 增强来自增加活跃辅助头/损失，而不是未来目标的信息内容，因此 informative-MTP 与 shared-aux 具有相同的源状态因果控制，$\Gamma_{info}\approx0$；即使两者的 $C_o$ 都为正，也不支持信息内容特异性。

**不利替代：** 信息性未来目标相对 shared-aux 削弱了可被标准主头使用的早期通道，因此 $\Gamma_{info}<0$。

**通过：** 所有有效性守卫通过；$\Gamma_{info}$ 在至少 4/5 个确认种子中超过由 Protocol 冻结的最小有效阈值，且确认均值达到该阈值。

**失败：** 所有守卫通过，但确认均值不为正，或至多 2/5 个种子通过最小效应标准。若 $C_{info\text{-}MTP}$ 与 $C_{shared\text{-}aux}$ 同样为正，只是否定信息内容特异增强，同时支持“两种辅助训练都使用该通道”的较弱判断。

**证据不足：** 恰好 3/5 个种子通过；均值为正但低于冻结阈值；任一模型能力不合格；两边能力明显不匹配；同分支替换不为零；双向切换失败；源张量未冻结；或完整性、配对、确认隔离守卫失败。

## 4. 数学模型

令 $o\in\{NTP,shared\text{-}aux,info\text{-}MTP\}$ 表示训练条件，$z\in\{1,\ldots,m\}$ 表示接收体分支，当前 A11 构造中 $m=4$。$r_z$ 是干净预测正确的接收体，$d_z$ 是独立匹配的同分支供体，$d_{z'}$ 是满足 $z'\neq z$ 的异分支供体。所有补状态操作都在模型 $o$ 内部完成。

令

$$
\hat y_o(r_z;S)
$$

表示接收体处理 `<SHARED>` 后，普通下一词元主头在 `<DECIDE>` 源记忆被设为 $S$ 时的预测。定义

$$
p_o^{diff}
=
\Pr\left[
\hat y_o(r_z;S_o(d_{z'}))=y_{z'}
\mid
\hat y_o(r_z;S_o(r_z))=y_z
\right],
$$

以及同分支无关变化率

$$
p_o^{same}
=
\Pr\left[
\hat y_o(r_z;S_o(d_z))\neq y_z
\mid
\hat y_o(r_z;S_o(r_z))=y_z
\right].
$$

模型内部受控切换效应为

$$
C_o=p_o^{diff}-p_o^{same},
$$

唯一主要跨条件指标为

$$
\Gamma_{info}=C_{info\text{-}MTP}-C_{shared\text{-}aux}.
$$

$C_o$ 检验单个模型内部的源状态是否控制普通主头；$\Gamma_{info}$ 检验信息性未来目标是否在匹配辅助训练结构之外增强这种控制。$\Gamma_{system}=C_{info\text{-}MTP}-C_{NTP}$ 仅作次要系统基线。供体答案相对接收体答案的 logit-margin 变化只作为连续次要诊断，不构成第二决策指标。

## 5. 计算实现

使用现有 A11 K=2 分支布局：

```text
BR_z F00 ... F15 U00 U01 U02 U03 A_SHARED S_z
```

更早的 `BR_z` 提供分支变量；`U03` 是决策位置 $T$（抽象记为 `<DECIDE>`）；`A_SHARED` 是所有分支相同的紧邻目标（抽象记为 `<SHARED>`）；`S_z` 是信息性答案。各分支只在决策位置附近保持局部匹配，并非整个因果前缀相同。

只增加产生同一 $Z$ 下独立匹配供体所必需的、与分支无关的实例变化。该变化不能改变答案或暴露捷径。本轮不增加序列距离、组合深度、自然语言变化或 K 扫描。

使用相同主干、两个已实例化预测头、数据流、优化合同和种子，分别训练 NTP、shared-aux 与 informative-MTP。先在校准数据上选择 shared-aux/informative-MTP 能力匹配的检查点，再在确认数据上执行补状态。决定性干预把真实供体在所有预注册源层中的 `<DECIDE>` 注意力记忆补入接收体，然后让接收体正常处理 `<SHARED>` 并由普通主头输出答案。

每个活跃预测头都使用普通全词表交叉熵。NTP 只激活标准一步头；shared-aux 与 informative-MTP 都激活同一个标准头和可训练第二头，并分别让第二头预测 $x_{t+1}$ 与 $x_{t+2}$。两个活跃头的损失取平均。该处理匹配头数、CE 项数和名义系数，但不匹配真实梯度范数、方向、目标难度或训练轨迹；这些差异是处理内容的一部分，只报告而不动态归一化。

本实验不替换源位置查询 $Q_T$。后续词元使用自己的接收位置查询 $Q_{T+1}$，与源位置键 $K_T$ 匹配并取回源位置值 $V_T$。$K_T$ 决定是否找到源位置，$V_T$ 决定取回什么内容。替换 $Q_T$ 会改变源位置怎样从更早上下文形成信息；替换 $Q_{T+1}$ 会改变接收位置的检索策略。K-only、V-only 和接收位置 Q 干预均停放到主结果之后。

必须在模型内部补状态；禁止把 MTP 状态直接补入 NTP 模型，反之亦然。

## 6. 最小证伪测试

### 决定性测试

在校准阶段冻结阈值、能力区间、源层和干预接口后，在 held-out 接收体—供体对上测量 $\Gamma_{info}$。

### 必要守卫

1. **干净能力：** 三种条件都通过标准主头任务能力门槛；主比较 shared-aux/informative-MTP 通过冻结的能力匹配规则，两个辅助头也学会各自目标。
2. **信息形成：** 源状态中存在分支变量；共同 held-out 读出可作守卫，但不能裁决使用。
3. **真实供体：** 每个被补状态都来自同一模型内的有效样本。
4. **同分支控制：** 独立同 $Z$ 补状态低于冻结的无关扰动阈值。
5. **双向控制：** 每个注册分支对的正向与反向替换都满足预期方向。
6. **配对控制：** 接收体后续、`<SHARED>`、目标间匹配数据和评价样本保持一致。
7. **确认隔离：** 在查看确认集的 informative-MTP—shared-aux 效应之前冻结阈值和层选择。

主要证伪结果是有效的 $\Gamma_{info}\le0$ 或只有控制量级的效应。能力或干预有效性失败只能判为证据不足。

## 7. 当前证据

**已建立的直接结果：** 信息性未来目标能产生更早的当前位置信号，该信号在受控条件下可以到达共享参数。见 [A11 主线注册表](../../README.md)。

**已建立的观察：** 既有跨位置核审计中，$h_T$ 上两个头的局部有用性在 5/5 种子为正，而 $h_{T+1}$ 上在 5/5 种子为负。见 [A11_03_01_E01](/Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_01_E01_head_position_cross_kernel/summary.md)。

**已建立的行为边界：** 桥接词元可以调节局部几何，但没有形成稳定的标准主头行为优势，端到端结果正式判为证据不足。见 [A11_03_01_E02](/Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_01_E02_end_to_end_use_boundary/summary.md)。

**A11_03_02_E01 直接结果：** 5/5 种子都通过共同能力检查点、缓存、自补丁、同分支、正控制和配对守卫。$\bar\Gamma_{info}=0.01675$，0/5 种子达到 `0.10`；只有 seed 972 为 `0.08374`，且集中在单一分支方向。因此信息内容的强行为因果使用增量按冻结规则失败。见 [summary](/Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E01_model_local_kv_causal_use/summary.md) 和 [detailed](/Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E01_model_local_kv_causal_use/detailed.md)。

**A11_03_02_E02 源信息审计：** same-contract replay 复现了 E01。三个条件、五个种子的精确第二层 `U03` K/V 都达到 held-out branch accuracy 和四类 recall `1.0`，因此绝对线性信息形成已经确认。注册的 informative-MTP 相对 shared-aux 可读性增量在 4/5 种子为负，均值为 `-0.002299` nat/样本，95% CI 为 `[-0.004502,-0.000173]`。由于单次标签打乱的最大准确率守卫失败，正式判定为证据不足。次要 Fisher 诊断在 5/5 种子更高，主要来自 branch 内 nuisance 波动收缩。见 [summary](/Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E02_exact_source_kv_information_audit/summary.md) 和 [detailed](/Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E02_exact_source_kv_information_audit/detailed.md)。

## 8. 结论边界与下一决策

当前可支持：MTP 可以产生更早的直接信号，但信息形成和有利局部几何不足以证明后续标准主头使用。

当前已裁决：在匹配辅助训练结构和标准主头能力后，信息性未来目标没有稳定增强该接口上的强答案切换控制。精确源 K/V 在所有目标下都能读出 branch，但注册审计没有识别出 informative-MTP 特异的可读性增量。

次要观察：informative-MTP 相对 shared-aux 的 donor-margin 变化在 4/5 种子为正，但均值被 seed 972 主导；其 branch 内 nuisance 几何也在 5/5 种子更紧。二者都只是候选机制，不是行为使用证据。

即使实验通过，也只能建立该受控 K=2 任务和该源状态接口上、相对 matched shared-aux 的信息性 K=2 全位置目标包因果使用增量；不能把效应仅归到 `U03` 的局部标签，也不能建立一般 MTP 优势、K 的尺度规律、长程或自然语言价值、组合推理、表征可拆分性或 MoE 价值。

**唯一下一决策：** 先验证一个没有答案直接绕行、且 shared-aux 基线不饱和的 `relay-required` carrier，再重新比较训练目标。在 carrier 通过前，K/V/Q/层和 shared-unembedding sweep 均保持后置。
