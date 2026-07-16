# 跨位置标准预测头使用边界 Anchor

状态：模型内 K/V 因果使用审计已完成；强行为信息内容增量失败，弱 margin 影响待决定是否审计。

Thinking Card source: [11_03_cross_position_standard_head_use_boundary_thinking_card_cn.md](11_03_cross_position_standard_head_use_boundary_thinking_card_cn.md)

## 1. 问题定义

### 术语解释

| 术语 | 通俗含义 | 具体对象 | 为什么重要 | 不能证明 |
|---|---|---|---|---|
| 当前状态形成 | $h_T$ 中已经出现任务方向 | 正的局部有用性或 margin | 使用的前提 | 后续真的使用 |
| 跨位置传递 | 任务方向经过中间词元后仍保留到 $h_{T+1}$ | 跨位置核 $J_{T+1}J_T^T$ | 标准头从后一个状态作答 | 一般因果使用 |
| 标准头使用 | 普通下一词元头在答案位置受益 | $h_{T+1}$ 上的 H1 margin 或行为 | NTP/MTP 共同结果 | 真实任务迁移 |

**唯一决策问题：** 当前位置形成正的任务方向，是否足以改善答案位置的标准下一词元头？

## 2. 物理先验

1. 探针能读出不等于模型在使用。
2. 更换输出头和更换状态位置是两种不同干预。
3. 下一词元状态转移可能丢失或反转当前的有用方向。

## 3. 可证伪假设

若当前位置形成足够，则标准头在 $h_T$ 和 $h_{T+1}$ 都应为正，并产生稳定行为收益。位置瓶颈解释则预测 $h_T$ 为正、$h_{T+1}$ 不为正。

## 4. 数学模型

对输出头 $a$ 和状态位置 $p$，局部有用性定义为

$$
U_{a,p}=v_a^T J_pJ_T^T d_2,
$$

其中 $d_2$ 是额外未来损失的下降方向。同位置自核与跨位置核的符号不必相同。

## 5. 计算实现

固定训练轨迹、诊断批次和额外损失梯度，只交叉改变输出头和状态位置；再小范围改变中间词元；最后检查标准头的 held-out 行为。

## 6. 最小证伪测试

1. 比较 H1/H2 在 $h_T$ 与 $h_{T+1}$ 的有用性。
2. 只改变中间词元，判断传递是否依赖状态转移。
3. 要求有利的局部交互同时产生稳定的 held-out 标准头收益。

## 7. 当前证据

在 $h_T$，两个头的有用性均在 5/5 种子为正；到 $h_{T+1}$ 后，两者均在 5/5 为负，说明直接瓶颈来自位置而非头。中间词元会改变局部几何，但有利的局部交互没有形成稳定行为优势。见[跨位置审计](/Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_01_E01_head_position_cross_kernel/summary.md)、[端到端审计](/Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_01_E02_end_to_end_use_boundary/summary.md)与[子锚点 11_03_01](subanchors/11_03_01_cross_position_proxy_falsification_anchor.md)。

已完成的[子锚点 11_03_02](subanchors/11_03_02_standard_head_causal_use_anchor_cn.md)在 matched shared-aux 对照下直接替换模型内部 K/V。所有守卫通过，但 $\bar\Gamma_{info}=0.01675$，0/5 种子达到 `0.10`，因此强行为增量失败；4/5 正向 margin 变化仅是候选弱影响。

## 8. 结论边界与下一决策

可支持：$h_T$ 的形成不保证 $h_{T+1}$ 的有用性；跨位置传递是额外必要条件。局部传递几何也不足以保证行为优势。

不可支持：普适的负传递定律、普适桥接词解释或 MTP 下游效率。

**唯一下一决策：** 决定是否为弱 margin 影响建立新 Protocol；否则关闭该接口并转向早期状态具有结构必要性的任务。当前不授权层、Q、K-only 或 V-only 扫描。
