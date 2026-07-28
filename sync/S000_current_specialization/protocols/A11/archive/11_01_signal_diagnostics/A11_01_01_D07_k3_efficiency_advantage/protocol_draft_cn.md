# Protocol Draft CN: A11_04_03 K=3 Efficiency Advantage

状态：草案，等待审核。
当前阶段：只设计 protocol，不写代码，不提交实验。
所属实验线：`A11_04_k3_first_informative_horizon`。
目的：补齐“表示监督优势是否转化为学习效率优势”的证据。

## 0. 审核快照

**研究问题：** 在早期语义变量 $Z$ 不影响 $Y_1,Y_2$、但第一次影响 $Y_3=S_Z$ 的任务中，覆盖 $\tau=3$ 的 MTP 是否比 NTP 或非覆盖 MTP 更快、更稳地学到 $Z$？

**已有理论：** 若 $K\ge\tau$ 且 $Y_\tau$ 能识别 $Z$，低 MTP 损失会迫使当前状态 $h_T$ 含有 $Z$；若 $K<\tau$，目标函数没有这个直接表示要求。

**本实验要补的缺口：** 理论证明的是表示要求，不是优化速度。本实验只判断这种直接表示监督是否带来经验上的效率优势。

**实验角色：** 效率判定实验 + 梯度机制审计。

**主指标：** 达到可靠语义恢复阈值的时间 $T_\theta$，其中 $\theta=0.9$，连续次数 $r=2$。

**辅助主指标：** early AUC of $Q_K(t)$ over $0$-$3000$ steps。

**关键解释指标：** extra-horizon gradient usefulness，即 $g_\tau$ 是否能预测未来窗口内 $Q$ 的上升，而不是只看它和 $g_1$ 的 cosine。

**最小设置：**

- 数据：clean $\tau=3$，即 $Y_1=A,\;Y_2=C,\;Y_3=S_Z$。
- 条件：K=1、K=2、K=3。
- 训练范围：decision-only 与 all-position 两个 scope。
- 控制：noisy control 和 redundant control。
- 模型和参数：沿用 A11_04，除 eval/profile 频率外不改架构和数据超参。

**通过：** clean $\tau=3$ 中 K=3 相比 K=1/K=2 有更小 $T_\theta$、更高 early AUC，local-loss guard 通过，noisy control 不复现同样效率效果，并且 gradient usefulness 能解释至少一部分早期 $Q$ 上升。

**失败：** K=1/K=2 在 all-position 中同样快、同样稳，且 $g_\tau$ 的 usefulness 不支持后续 $Q$ 提升。

**不足证据：** K=3 最终更好但早期曲线不稳定；或梯度指标噪声过大，不能解释学习过程。

**不能声称：** 不能声称自然语言上 MTP 已经更好；不能声称 larger K always helps；不能把 gradient cosine 小于 0 直接解释为坏。

**审核决策：** 待用户审核。

## 1. 术语解释

| 术语 | 中文含义 | 具体对象或计算方式 | 单位或公式 | 为什么影响判断 | 不能证明什么 |
|---|---|---|---|---|---|
| 表示监督优势 | 目标函数迫使 $h_T$ 保存 $Z$ | 低 $L_\tau$ 推出 $I(h_T;Z)$ 高 | 信息约束 | 已有理论结论 | 学得更快 |
| 学习效率优势 | 更早、更稳地恢复 $Z$ | $T_\theta$ 更小、early AUC 更高 | steps / score area | 本实验核心 | 自然语言收益 |
| 语义恢复分数 $Q$ | 保守判断 $h_T$ 是否含 $Z$ | $Q=\min\{A,P,S\}$ | 0 到 1 | 避免 probe-only 假阳性 | 完整因果证明 |
| 达阈值时间 $T_\theta$ | 第一次可靠达到语义恢复阈值 | $T_\theta=\inf\{t:Q(t)\ge\theta \text{ for } r \text{ consecutive evals}\}$ | training steps | 判断“更早” | 最终性能 |
| early AUC | 早期语义恢复曲线面积 | $\operatorname{AUC}_{Q,[0,3000]}$ | score area | 判断“整体早期更快” | 最终收敛 |
| local-loss guard | 局部预测没有被牺牲 | $Y_1/Y_2$ loss 和 accuracy | CE / accuracy | 防止长程提升来自局部退化 | 长程机制 |
| extra-horizon gradient | 来自第 $\tau$ 个未来目标的梯度 | $g_\tau=\nabla_\theta L_\tau$ | gradient vector | 解释 MTP 额外监督 | 单独代表好坏 |
| gradient usefulness | 梯度对未来 $Q$ 提升的预测力 | $u_\Delta=\langle g_\tau,\Delta\theta_\Delta\rangle$ 或与 $\Delta Q$ 的相关 | correlation / signed projection | 判断额外梯度是否有用 | 严格因果充分性 |

## 2. Anchor 对齐

**上游结论：** A11_04 已经支持：decision-only 下，K=3 覆盖 $\tau=3$ 后能恢复 $Z$，K=1/K=2 不能；all-position 下，K=3 仍最强，但 K=1/K=2 也能间接恢复 $Z$。

**本实验的新问题：** 既然 all-position 中 NTP 也可能最终学到 $Z$，MTP 的直接监督是否让 $Z$ 更早、更稳地出现？

**核心模型项：**

$$
L_K(h_T)=\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_T),Y_j).
$$

clean $\tau=3$ 中：

$$
Y_1=A,\qquad Y_2=C,\qquad Y_3=S_Z.
$$

K=3 比 K=1/K=2 多出的关键项是：

$$
\lambda_3\operatorname{CE}(q_3(\cdot\mid h_T),S_Z).
$$

**本实验 falsifier：** 如果 K=3 没有更小 $T_\theta$、没有更高 early AUC，且 gradient usefulness 不能解释早期 $Q$ 上升，则不能声称 MTP 在当前任务中有学习效率优势。

## 3. 待检验假设

**H1：decision-only 效率优势。**
在 clean $\tau=3$ decision-only 中，K=3 比 K=1/K=2 更早达到 $Q\ge0.9$，并有更高 early AUC。

**H2：local-loss guard。**
K=3 的长程恢复不以牺牲 $Y_1/Y_2$ 为代价；$Y_1/Y_2$ accuracy 接近 `1.0`，loss 不显著高于 K=1/K=2。

**H3：all-position 效率优势或边界。**
在 all-position 中，K=3 可能不是唯一能恢复 $Z$，但如果 MTP 更高效，K=3 应该更早、更稳，或者在 noisy control 中更少出现假阳性。

**H4：gradient usefulness。**
$g_\tau$ 的大小、方向或 forward-looking 指标应能解释后续 $Q$ 的上升；如果不能，则不能说 MTP 的 extra-horizon gradient 更有用。

## 4. 对照解释

| 替代解释 | 如何排除或限制 |
|---|---|
| 多一个预测头天然提升表示 | noisy control：$Y_3\perp Z$ 不应复现 clean 的效率优势 |
| horizon 编号本身有优势 | redundant control：若 $Y_2=S_Z$，K=2 提升应被解释为早期目标已含信息 |
| K=3 牺牲局部预测换来长程恢复 | local-loss guard：检查 $Y_1/Y_2$ loss 和 accuracy |
| all-position 中 NTP 通过间接路径学到 $Z$ | 比较 $T_\theta$、early AUC、假阳性率，而不是只看 final $Q$ |
| cosine 小于 0 就说明梯度坏 | 不用 cosine 单独判定；用 forward-looking usefulness 看后续 $Q$ |
| early AUC 高只是初始噪声 | 要求连续阈值、多个 seeds、noisy guard 和曲线稳定性 |

## 5. 数据、模型、目标函数

**主数据：clean $\tau=3$**

$$
Y_1=A,\qquad Y_2=C,\qquad Y_3=S_Z.
$$

信息结构：

$$
I(Z;Y_1)=0,\qquad I(Z;Y_2\mid Y_1)=0,\qquad I(Z;Y_3\mid Y_1,Y_2)>0.
$$

**noisy control：**

$$
Y_3\perp Z.
$$

用途：如果 noisy 下也出现同样早的 $Q$ 提升，说明效率指标可能在读噪声或背景泄漏。

**redundant control：**

$$
Y_2=S_Z.
$$

用途：如果 K=2 在 redundant 下更快恢复 $Z$，这不是反例，而是说明优势来自“目标含有 $Z$ 信息”，不是来自 K 编号。

**模型：** 沿用 A11_04，一层一头 Transformer，`d_model=64`。
**种子：** 沿用 `971-975`，必要时增加到 `971-980` 作为稳健性扩展，但主 protocol 先以 5 seeds 为默认。
**训练步数：** `15000`。
**评估频率：** 建议 `eval_every=250`，至少保证 $0$-$3000$ early window 有足够点；如果算力紧张，可保持 `500`，但 early AUC 分辨率较低。
**梯度 profiling 频率：** 建议 `profile_every=500`，重点覆盖 `0,500,...,5000`，后期可稀疏记录。

## 6. 条件、seeds、checkpoints

| 条件 | 训练范围 | regime | 为什么需要 | 主要证据 | 通过 | 失败 | 不足证据 |
|---|---|---|---|---|---|---|---|
| K=1 | decision-only | clean | NTP baseline | $T_\theta$, early AUC | 低于 K=3 | 同 K=3 一样快且无泄漏解释 | 曲线噪声大 |
| K=2 | decision-only | clean | 非覆盖 MTP control | $T_\theta$, early AUC | 低于 K=3 | 匹配 K=3 | 目标泄漏不清 |
| K=3 | decision-only | clean | 覆盖 $\tau$ 主条件 | $T_\theta$, early AUC, local guard | 更早更高 | 不优于 K=1/K=2 | 优化失败 |
| K=1/2/3 | all-position | clean | 真实训练边界 | $T_\theta$, early AUC, final $Q$ | K=3 更早或更稳 | K=1/K=2 同样快 | 间接路径无法分解 |
| K=1/2/3 | both | noisy | 假阳性控制 | noisy $T_\theta$, noisy early AUC | 不复现 clean | 复现 clean | 高方差 |
| K=1/2/3 | both | redundant | 信息结构控制 | K=2/K=3 恢复模式 | 由 $Y_2=S_Z$ 解释 | 无法解释 | 数据混淆 |

## 7. 主指标

### 7.1 Time-to-threshold

定义：

$$
T_\theta(K)=\inf\{t:Q_K(t)\ge \theta \text{ for } r \text{ consecutive evaluations}\}.
$$

默认：

$$
\theta=0.9,\qquad r=2.
$$

如果某个 run 从未达到阈值，记为 censored / NA；统计时同时报告 reach rate，不能只报告已达到者的平均时间。

**判定：**

- 支持效率优势：K=3 reach rate 更高，且达到阈值时间更早。
- 不支持：K=1/K=2 与 K=3 同样早，或 K=3 只在少数 seed 达到。

### 7.2 Early AUC

定义：

$$
\operatorname{AUC}_{Q,[0,3000]}(K)
=\frac{1}{3000}\int_0^{3000}Q_K(t)\,dt.
$$

同时保留 full AUC：

$$
\operatorname{AUC}_{Q,[0,T_{\max}]}(K).
$$

**优先级：** early AUC 高于 final $Q$，因为本实验问的是效率，不是最终可达性。

### 7.3 稳定性

记录：

- reach rate；
- seed-level $T_\theta$；
- seed-level early AUC；
- bootstrap CI 或 seed mean/std；
- K=3 是否只由个别 seed 支撑。

## 8. Local-loss guard

记录每个 checkpoint 的：

- $Y_1$ accuracy；
- $Y_1$ loss；
- $Y_2$ accuracy；
- $Y_2$ loss；
- all-position 中的 local LM loss。

通过标准：

- K=3 的 $Y_1/Y_2$ accuracy 接近 `1.0`；
- K=3 的 $Y_1/Y_2$ loss 不显著高于 K=1/K=2；
- 若 K=3 长程恢复更好但局部 loss 明显恶化，只能说“有 tradeoff”，不能说无代价更高效。

## 9. Gradient usefulness 设计

### 9.1 梯度对象

在 profiling step $t$，对同一批样本分别计算：

$$
g_1(t)=\nabla_\theta L_1(t),
$$

$$
g_\tau(t)=\nabla_\theta L_\tau(t),
$$

$$
g_{\mathrm{MTP}}(t)=g_1(t)+\lambda g_\tau(t).
$$

这里 clean $\tau=3$ 中 $g_\tau=g_3$。

### 9.2 基础梯度量

记录：

$$
c(t)=\frac{\langle g_1(t),g_\tau(t)\rangle}{\|g_1(t)\|\|g_\tau(t)\|},
$$

$$
r(t)=\frac{\|g_\tau(t)\|}{\|g_1(t)\|},
$$

$$
\rho(t)=\frac{\langle g_1(t)+\lambda g_\tau(t),g_1(t)\rangle}{\|g_1(t)\|^2}.
$$

解释规则：

- $c<0$ 不自动等于坏；它只说明两个 loss 的即时参数更新方向不一致。
- $r$ 大不自动等于有用；它可能只是 noisy target 或大 loss。
- $\rho$ 只说明 MTP 总梯度保留了多少 local-gradient 分量，不说明长程恢复。

### 9.3 参数组

至少按以下组记录：

- embedding；
- shared attention；
- shared MLP；
- head_1；
- head_2；
- head_3。

如果当前模型没有 separate expert，则不记录 expert_1/expert_2；不要凭空加架构变量。

### 9.4 Forward-looking usefulness

只看 cosine 不够。本实验增加未来窗口指标。

定义未来语义提升：

$$
\Delta Q_\Delta(t)=Q(t+\Delta)-Q(t).
$$

默认窗口：

$$
\Delta\in\{500,1000,2000\}\text{ steps}.
$$

定义梯度 usefulness 的三种读法：

**U1：相关性。**

在 seed 和 checkpoint 上计算：

$$
\operatorname{corr}\big(r(t),\Delta Q_\Delta(t)\big),
$$

以及

$$
\operatorname{corr}\big(\|g_\tau(t)\|,\Delta Q_\Delta(t)\big).
$$

**U2：分组比较。**

把 profiling points 按 $g_\tau$ 强弱或 $r$ 高低分成 high/low 两组，比较未来 $\Delta Q$。

**U3：目标特异性。**

比较 clean 与 noisy：

- 如果 clean 中 $g_\tau$ 指标预测 $\Delta Q$，但 noisy 中不预测，说明 extra-horizon gradient 的 usefulness 来自目标信息结构。
- 如果 noisy 也同样预测，则可能是 metric leakage 或背景训练假阳性。

### 9.5 注意事项

K=1/K=2 的 inactive head-3 梯度不可直接作为同等优化信号解释。主梯度 usefulness 判断应集中在 K=3 active horizon；K=1/K=2 可作为 counterfactual diagnostic，但不能和 K=3 的 active $g_\tau$ 做强因果比较。

## 10. 输出表格与图

必须输出：

1. `efficiency_summary.csv`
   - scope；
   - regime；
   - K；
   - init；
   - reach rate；
   - mean/median $T_\theta$；
   - early AUC；
   - full AUC；
   - final $Q$；
   - $Y_1/Y_2$ loss and accuracy。

2. `gradient_profile_summary.csv`
   - step；
   - scope；
   - regime；
   - K；
   - parameter group；
   - $c$；
   - $r$；
   - $\rho$；
   - $\Delta Q_{500}$；
   - $\Delta Q_{1000}$；
   - $\Delta Q_{2000}$。

3. `gradient_usefulness_summary.csv`
   - correlation / grouped comparison；
   - clean vs noisy；
   - parameter group；
   - interpretation flag: supports / weakens / insufficient。

建议图：

- Figure 1: clean $\tau=3$ $Q(t)$ curves, decision-only and all-position separated。
- Figure 2: early AUC and $T_\theta$ bar/point plot with seed dots。
- Figure 3: local-loss guard curves。
- Figure 4: gradient usefulness scatter or binned plot: $g_\tau$ indicator vs future $\Delta Q$。
- Figure 5: clean vs noisy gradient usefulness contrast。

## 11. 成功、失败、不足证据

### 支持“MTP 更高效”

必须同时满足：

1. clean $\tau=3$ 中 K=3 的 $T_\theta$ 显著小于 K=1/K=2，或 K=1/K=2 大量 NA 而 K=3 稳定达到；
2. K=3 的 early AUC 高于 K=1/K=2；
3. local-loss guard 通过；
4. noisy control 不复现同样效率优势；
5. gradient usefulness 显示 $g_\tau$ 的某些指标与后续 $\Delta Q$ 正相关，或至少能解释 K=3 的早期恢复。

### 不支持“MTP 更高效”

满足任一核心失败：

1. all-position 中 K=1/K=2 与 K=3 同样快、同样稳；
2. K=3 early AUC 不高于 K=1/K=2；
3. K=3 的 local loss 明显恶化；
4. noisy control 复现 clean 的早期优势；
5. gradient usefulness 不支持 extra-horizon gradient 与未来 $Q$ 提升有关。

结论应收缩为：

> MTP 有直接表示监督优势，但当前实验不支持学习效率优势。

### 不足证据

- K=3 有趋势但 seed 方差大；
- $T_\theta$ 大量 censored，无法比较；
- gradient profile 噪声太大；
- early AUC 和 final $Q$ 给出相反判断；
- noisy control 与 clean 难以区分。

## 12. 当前 protocol 的审核点

请确认以下点后才能进入实现：

1. $\theta=0.9,r=2$ 是否接受？如果觉得过严，可同时报告 $\theta=0.8$ 作为敏感性分析，但主判定仍用 $0.9$。
2. early window 是否固定为 $0$-$3000$ steps？如果全位置学习太快，可增加 $0$-$1500$ 作为更早窗口。
3. 是否保持 5 seeds，还是扩展到 10 seeds 以提高效率统计稳定性？
4. gradient profiling 是否只在 K=3 active horizon 上做主解释，K=1/K=2 只作为 counterfactual diagnostic？
5. all-position 中是否仍保留 noisy control 作为强 guard？我建议必须保留，因为已有结果显示 noisy random 偏高。

## 13. 不能声称

本实验即使通过，也不能声称：

- MTP 在自然语言任务上已经更好；
- 所有更大的 K 都更好；
- gradient cosine 为正就是好、为负就是坏；
- all-position 中只有 K=3 能学到 $Z$；
- final $Q$ 高就代表效率优势。

## 14. 批准后执行计划

批准后执行顺序：

1. 将本中文草案转为英文 canonical `protocol.md`。
2. 审计现有 runner 是否已有 $T_\theta$、early AUC、local loss、gradient profile 支持。
3. 只补最小必要代码：early AUC、local loss table、gradient profiling、future $\Delta Q$ merge。
4. smoke test。
5. reserved 4-GPU full run。
6. 产出 canonical `summary.md` 和 `detailed.md`，并更新 A11_04 anchor 的 next-decision 状态。
