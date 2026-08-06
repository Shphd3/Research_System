# A11 模型内 K/V 因果使用实验收尾

日期：2026-07-16
实验：`A11_03_02_E01_model_local_kv_causal_use`
主要证据：[Protocol](../../../Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E01_model_local_kv_causal_use/protocol_cn.md)、[Summary](../../../Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E01_model_local_kv_causal_use/summary.md)、[Detailed](../../../Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E01_model_local_kv_causal_use/detailed.md)
正式任务：四卡 ACP job `pt-pz6zjzzn`，已成功完成。

## 实验

### 原本要回答的问题

在 A11 的短程 K=2 四分支任务中，相对于活跃头数、CE 项数、名义 loss 系数和标准主头能力匹配的 shared-aux，informative-MTP 是否增强了从第二层 `U03` 源 K/V 到后续 `A_SHARED` 标准下一词元主头答案的强行为因果通道？

“强行为因果通道”在本实验中被操作化为：把接收体的第二层 `U03` K/V 替换为真实异分支供体 K/V 后，标准主头的最终答案应稳定切换到供体分支；同分支替换不应改变答案。

唯一主要指标为

$$
\Gamma_{info}
=
C_{info\text{-}MTP}-C_{shared\text{-}aux},
\qquad
C_o=p_o^{diff}-p_o^{same}.
$$

### 原本预期的结果

若“信息性未来目标特异增强标准主头使用”成立，预期：

1. $C_{info\text{-}MTP}>C_{shared\text{-}aux}\approx C_{NTP}$；
2. 至少 `4/5` 个种子的 $\Gamma_{info}\ge0.10$；
3. 五种子均值 $\bar\Gamma_{info}\ge0.10$；
4. 效应覆盖注册的 branch 对，而不是只出现在单一种子或单一替换方向。

竞争结果预期：

- 若 $C_{info\text{-}MTP}\approx C_{shared\text{-}aux}>C_{NTP}$，说明增加辅助头/损失结构即可解释强通道，不支持信息内容特异增强；
- 若三个条件都接近零，说明没有观察到该接口上的稳定强答案控制；
- 若只改变 donor-answer margin、不改变最终答案，说明最多存在候选弱或冗余影响，不能算主要假设通过。

### 实际观察到的结果

五个种子都找到了共同能力匹配检查点：`500, 500, 900, 600, 700`。三个条件的标准主头确认集准确率均为 `1.0`；shared-aux 和 informative-MTP 的注册辅助目标准确率均为 `1.0`。

主要结果：

| Seed | $C_{NTP}$ | $C_{shared}$ | $C_{info}$ | $\Gamma_{info}$ |
|---:|---:|---:|---:|---:|
| 971 | 0 | 0 | 0 | 0 |
| 972 | 0 | 0 | 0.08374 | 0.08374 |
| 973 | 0 | 0 | 0 | 0 |
| 974 | 0 | 0 | 0 | 0 |
| 975 | 0 | 0 | 0 | 0 |
| mean | 0 | 0 | 0.01675 | 0.01675 |

因此 `0/5` 种子达到 `0.10`，强行为通道假设没有得到支持。自动判决程序输出 `fail`。

seed 972 的效应高度单向：informative-MTP 中 receiver branch 3 使用 donor branch 1 时为 `1024/1024` 次切换，反向只有 `5/1024`，其余有序 branch 对均为零。它不是跨种子、跨方向稳定机制。

次要 margin 结果中，informative-MTP 减 shared-aux 在 `4/5` 个种子为正，均值约为 `0.560`，但主要由 seed 972 的 `2.447` 主导。这只支持候选弱或冗余影响，不能覆盖主要指标。

能力和补丁实现守卫通过：cache replay 最大误差不超过 `2.36e-14`，自补丁误差为零，同分支答案变化率为零，最终隐藏状态正控制的供体答案切换率为 `1.0`。

需要保留两个人工审计结论：

1. 更准确的说法是“能力守卫和补丁实现守卫通过”。Protocol 中注册的精确第二层 `U03` K/V branch 可读性、分支内/分支间距离没有产出，因此尚未证明被干预的 K/V 本身携带 branch 信息。
2. Protocol 的分类文字存在重叠：本结果既满足“至多 `2/5` 达标，因此 fail”，又满足“$0<\bar\Gamma_{info}<0.10$，因此 insufficient”。代码通过判断顺序选择了 `fail`。因此最保守的研究表述是：注册的强假设未获支持；关于“信息已进入精确 K/V、但主头没有利用”的条件命题仍然证据不足。

### 最困惑的具体一点

informative-MTP 的 `q2` 能在 `U03` 最终隐藏状态上以 `1.0` 准确率预测 branch 答案，但替换第二层注意力计算前形成的 `U03` K/V，绝大多数种子和 branch 对都不改变标准主头答案。

当前无法区分：branch 信息没有进入精确 $[K_{2,T};V_{2,T}]$；信息进入了但 `A_SHARED` 没有读取；还是标准主头存在直接 `BR_z` 路径和高度饱和的答案 margin，使这条路径只有弱影响而无法翻转答案。

### 当前可能解释

#### 1. 实现或配置错误

- 大范围补丁错误不是首要解释：cache replay、自补丁、同分支控制和最终隐藏状态正控制均通过。
- 仍有一个关键配置/证据缺口：当前只确认提取和替换了正确位置的 K/V，没有确认这些 K/V 在每个条件和种子中实际携带稳定 branch 信息。
- 自动分类实现采用“先检查 `<=2/5` 再检查正但低于阈值的均值”的优先级，掩盖了 Protocol 文字中 `fail` 与 `insufficient` 的重叠；这影响结果标签，但不改变测得数值。

#### 2. 数据或指标问题

- 数据允许标准主头通过更早的 `BR_z` 或其他位置直接取得 branch，`U03` K/V 不是结构必要的唯一通道。因此即使它被使用，也可能只是冗余路径。
- 标准主头在共同检查点已高度饱和，答案位置 CE 大约为 `0.0007–0.0117`。argmax 答案切换是较强、较粗的指标，可能漏掉不足以跨过决策边界的真实 margin 变化。
- `q2(U03)` 测量的是第二层和最终 LayerNorm 之后的隐藏状态；它不能替代第二层注意力之前 $K_{2,T},V_{2,T}$ 的信息形成守卫。

#### 3. 随机性或训练不稳定

- 唯一非零答案切换集中在 seed 972，并且几乎只来自一个 branch 方向，说明表示几何和输出决策边界对初始化高度敏感。
- margin 在 `4/5` 种子为正，但效应量被 seed 972 主导；目前不能称为稳定弱机制。

#### 4. 原假设本身错误

- informative-MTP 可能增强 `U03` 最终状态中的 branch 信息，但不会自动把它变成后续标准主头稳定、独立且足以控制答案的 K/V 通道。
- 标准主头可能优先依赖更晚形成或更直接的普通 NTP 路径；MTP 提供的早期信息最多是弱的、冗余的，或者没有进入当前选定的第二层 K/V 接口。
- 因而“信息形成必然转化为标准主头强使用”这一强假设被明显削弱。

### 目前不能下的结论

- 不能说标准主头完全没有使用任何 MTP 信息。
- 不能说精确第二层 `U03` K/V 已经稳定包含 MTP 增强的 branch 信息。
- 不能把结果唯一归因于“主头没有读取”；形成、传递、检索和输出饱和仍混在一起。
- 不能把 seed 972 或 `4/5` 正 margin 写成稳定弱因果机制。
- 不能说 MTP 整体无效、劣于 NTP，或在真实语言任务上没有价值。
- 不能推出 K-only、V-only、源 Q、接收 Q、其他层或其他位置没有作用。
- 不能推出长程、组合任务、自然语言或 MoE 场景中的结论。

### 明天第一个检查动作

不重新训练模型。直接使用现有五个种子的共同检查点，补齐原 Protocol 已注册但遗漏的精确 source-information audit：

1. 分别从 NTP、shared-aux、informative-MTP 提取 calibration 与 confirmation 集的
   $$
   S_{2,T}=[K_{2,T};V_{2,T}]\in\mathbb R^{128}.
   $$
2. 每个模型内部独立使用 calibration 特征训练固定 L2 正则的四分类线性 probe，冻结后只在 confirmation 上评估 branch 准确率；随机水平为 `0.25`。标准化统计只由 calibration 计算。
3. 同时计算 confirmation 上的 branch 间/branch 内 Fisher 分离比，以及六个 branch 对的中心距离；按 nuisance ID 整组 bootstrap，检查分离是否稳定或只集中在 branch `3↔1`。
4. 不把 probe 或距离当作“主头使用”的证据，只用来定位失败阶段：
   - 若 informative-MTP 的精确 K/V 强可读、稳定分离，但补丁仍无稳定效应，则失败定位到接收端检索、冗余或输出决策边界；
   - 若精确 K/V 接近随机且分离很弱，则失败首先定位到 branch 信息没有稳定进入该被测 K/V，当前实验不能裁决“已有信息但主头未利用”。

完成这一步后，再决定是否为弱 margin 建立新 Protocol；在此之前不增加训练、层扫描、Q 干预或 K/V 组件 sweep。
