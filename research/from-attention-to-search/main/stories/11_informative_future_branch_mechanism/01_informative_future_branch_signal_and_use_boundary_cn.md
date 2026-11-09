# 信息性未来分支信号及其使用边界

## 摘要

A11 只隔离下一词元预测和多词元预测之间一个精确的目标函数差异：在同一当前位置，下一词元预测只直接监督紧邻词元；多词元预测还可能直接监督一个更晚出现、并首次暴露分支变量的词元。受控实验支持这类信息性未来目标会更早地给当前位置表征施加一阶任务信号，而且该信号能够传到共享参数。但实验同时给出关键边界：当前位置形成了信息，不代表普通下一词元主头在下一个位置会使用它。因此 A11 关闭的是目标函数层面的机制问题，不是长文本或下游收益问题。

## 1. 术语解释

| 术语 | 直观含义 | 具体对象或计算 | 为什么重要 | 不能证明什么 |
|---|---|---|---|---|
| 下一词元预测（NTP） | 每个状态只训练预测紧邻的下一个词元 | \(Y_{t+1}\) 的交叉熵 | 基准目标 | 后续信息从未通过其他位置进入训练 |
| 多词元预测（MTP） | 同一共享状态同时训练预测多个未来词元 | \(Y_{t+1},\ldots,Y_{t+K}\) 的损失 | 增加更早的监督路径 | 一定提升性能 |
| 分支变量 \(Z\) | 紧邻词元相同，但稍后词元会随之变化的隐藏选择 | 最小数据中 \(Z\in\{0,1\}\) | 精确隔离新增未来信息 | 一般自然语言语义 |
| 信息性未来位置 | 已知当前前缀和更早未来词元后，目标仍随 \(Z\) 变化的位置 | \(I(Z;Y_{t+j}\mid X_{\le t},Y_{t+1:t+j-1})>0\) | 决定 MTP 从何时开始增加直接信号 | 后续主头真正使用 |
| 表征形成 | 当前位置状态沿能区分 \(Z\) 的方向移动 | 隐状态 margin 或语义速度 | 使用的前提 | 主头依赖 |
| 标准主头使用 | 普通下一词元主头在实际答案位置获得收益 | \(h_{t+1}\) 上的损失或因果输出变化 | NTP 与 MTP 的共同评价对象 | 真实任务迁移 |

## 2. 最小数据模型

两个分支拥有完全相同的当前前缀和紧邻词元，只有第二个未来词元不同：

```text
分支 Z=0：<DECIDE> <SHARED> <BRANCH_0>
分支 Z=1：<DECIDE> <SHARED> <BRANCH_1>
```

在 `<DECIDE>` 产生的隐藏状态上，紧邻词元 `<SHARED>` 不含 \(Z\) 的信息，而后续 `<BRANCH_Z>` 含有。这里故意使用短序列，以排除检索、语言歧义和树状组合，只检验目标函数本身的差异。

当前位置的两个训练目标是

\[
L_{NTP}^{(t)}=\operatorname{CE}(q_1(h_t),Y_{t+1}),
\]

\[
L_{MTP}^{(t)}=L_{NTP}^{(t)}+
\lambda\operatorname{CE}(q_2(h_t),Y_{t+2}).
\]

因为 \(Y_{t+1}\) 在两个分支中相同，它的直接梯度不能区分 \(Z\)；因为 \(Y_{t+2}\) 随分支变化，第二项可以区分 \(Z\)。

## 3. 核心机制

对每个信息性未来位置 \(j\)，令 \(u_{j,z}\) 表示分支 \(z\) 的输出方向，\(\bar u_j\) 表示分支共有部分。预测范围为 \(K\) 时，任务相关的一阶方向为

\[
v_z^{(K)}=
\sum_{j\le K:\,j\text{ 含新信息}}
\lambda_j(u_{j,z}-\bar u_j).
\]

它给出三个可证伪预测：

1. 覆盖第一个信息性词元之前，当前位置没有直接分支信号；
2. 覆盖该词元时，信号出现；
3. 新增目标的输出方向若对齐则增强，若没有新信息则不产生直接增量，若冲突则削弱。

因此关键变量不是数字 \(K\) 本身，而是预测范围是否覆盖新信息，以及多个输出方向如何叠加。

## 4. 证据链

### 4.1 当前位置的直接信号

受控分支实验固定所有局部信息，只改变未来目标。结果显示：第一个信息性位置之前隐状态任务移动为零；覆盖后变为正；新增共享词元没有一步增量；新增对齐或冲突的信息性目标时，变化方向符合理论预测。

结论：MTP 在 \(h_t\) 得到 NTP 在同一状态上没有的直接一阶任务信号。

### 4.2 信号能否传到共享参数

只有共享参数能够沿有用方向更新，隐状态信号才具有训练意义。参数审计把更新拆成 MTP 的更早直接路径和普通全位置损失背景。直接路径可以到达共享参数，也能预测小步真实更新；但其他语言模型梯度有正有负，可能抵消直接路径。

结论：该信号不是固定输出头的假象，但直接路径为正不等于总更新一定为正。

### 4.3 形成不等于使用

标准下一词元主头要在读入共享中间词元之后才预测分支答案。实验中，\(h_t\) 上的作用为正，但 \(h_{t+1}\) 上在所有被测种子中反号。更换输出头不能消除反号，而更换状态位置会改变结果。进一步修改桥接词元也没有产生稳定的 held-out 行为收益。

结论：当前位置形成信息，不足以推出后续标准主头使用；跨位置状态转移必须单独检验。

后续模型内 K/V 审计把这个问题变成了因果检验。相对活跃头数和名义 loss 系数匹配的 shared-aux，所有能力与补丁守卫都通过，但强行为增量失败：\(\bar\Gamma_{info}=0.01675\)，0/5 种子达到 `0.10`。informative-MTP 在 4/5 种子改变了 donor margin，但该弱效应受单一种子主导，不能稳定控制答案。

精确源信息审计进一步拆开了信息形成与信息使用。NTP、shared-aux 和 informative-MTP 在五个种子上都能从精确第二层 `U03` K/V 以 `100%` held-out 准确率读出 branch，因此绝对线性源信息为空被排除。但没有识别出 informative-MTP 特异的可读性增量：平均 \(\Gamma_{\mathrm{read}}=-0.002299\) nat/样本，4/5 种子非正；由于注册的单次标签打乱守卫失败，正式判定仍为证据不足。次要 Fisher 分离比在 5/5 种子提高，主要来自 branch 内 nuisance 波动压缩，更像是已可读信息的几何整理，而不是新增了可解码的 branch 内容。

## 5. A11 的确定结论

> 当 MTP 的预测范围首次覆盖一个包含分支新信息、而紧邻词元不包含该信息的未来词元时，MTP 会在当前位置产生 NTP 同位置没有的直接一阶任务信号。该信号在受控条件下可以传到共享参数，但信号存在不保证普通下一词元主头在后续答案位置使用它。

## 6. 结论边界

A11 没有证明该分支变量构成长程工作负载，没有证明多证据组合，没有解释神经模型尺度或课程学习，也没有证明任何自然语言基准提升。K/V 审计否定的是一个注册接口上的稳定强答案控制增量，也没有识别出 MTP 特异的额外 branch 可读性。次要 nuisance 压缩不能升级为“主头使用了几何”，也不能升级为“主头完全没有使用 MTP 信息”。

## 7. 交给 A12 的问题

在把组合问题交给 A12 前，A11 还有一个 carrier 设计门槛：先构造可学习的 `relay-required` 任务，使答案不能绕过早期消息，并且匹配对照不能已经饱和；通过后才能重新检验标准主头是否消费该消息。多证据结构组合仍由 A12 负责。

## 8. 父锚点链与证据入口

1. [信息性未来范围监督](../../problem_anchors/11_informative_future_branch_mechanism/11_01_informative_horizon_supervision/11_01_informative_horizon_supervision_anchor_cn.md)：决定性证据见[信息位置纳入规律](../../experiments/A11/11_01_informative_horizon_supervision/A11_01_01_E01_next_k_inclusion_law/summary.md)。
2. [隐藏状态到共享参数的传递](../../problem_anchors/11_informative_future_branch_mechanism/11_02_hidden_to_parameter_transmission/11_02_hidden_to_parameter_transmission_anchor_cn.md)：决定性证据见[参数传递](../../experiments/A11/11_02_hidden_to_parameter_transmission/A11_02_01_E01_semantic_tangent_transmission/summary.md)与[全位置分解](../../experiments/A11/11_02_hidden_to_parameter_transmission/A11_02_01_E02_all_position_path_decomposition/summary.md)。
3. [跨位置标准头使用边界](../../problem_anchors/11_informative_future_branch_mechanism/11_03_cross_position_standard_head_use_boundary/11_03_cross_position_standard_head_use_boundary_anchor_cn.md)：决定性证据见[位置审计](../../experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_01_E01_head_position_cross_kernel/summary.md)、[端到端边界](../../experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_01_E02_end_to_end_use_boundary/summary.md)、[模型内 K/V 因果使用结果](../../experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E01_model_local_kv_causal_use/summary.md)与[精确源信息审计](../../experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E02_exact_source_kv_information_audit/summary.md)。

不再改变上述结论的辅助变体统一放在 [A11 实验归档](../../experiments/A11/archive/README.md)。
