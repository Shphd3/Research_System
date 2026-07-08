# Meeting Brief: MTP 为什么可能更高效地学习长程语义信息

Status: draft v1
Audience: advisor / senior student
Principle: start from plain mechanism, then claim boundary, then next decision

---

## 0. 开场 60 秒版本

老师，我们现在的结论要比“MTP 一定比 NTP 好”更精确。

我们不说 NTP 学不到长程信息。事实上，在全位置 LM 训练里，NTP 也可能通过后面的位置和共享参数间接把早期信息学进来。

我们现在能确定证明的是另一件事：

> 如果一个早期语义变量 `Z` 不是决定下一个 token，而是决定更远的第 `tau` 个 token，那么只要 MTP 的预测范围覆盖到这个位置，它就会把这个远处 token 的误差直接打到当前 hidden state `h_T` 上。低 MTP loss 会数学上强迫 `h_T` 含有 `Z`。

所以 MTP 的确定优势不是“唯一能学”，而是：

> 监督路径更短、更直接。

接下来我们要把这个推进成“高效性”问题：

> 这条更短的路径是否让模型更快、更稳地恢复长程语义信息，同时不损伤 next-token 学习？

这可以用 `time-to-recovery`、AUC、local-loss guard、以及 future-token gradient 是否降低 branch-recovery loss 来测试。

---

## 1. 我们现在要回答的总问题

导师问题：

> MTP 在学习长程语义信息上比 NTP 好，好在哪？如果最终相当，为什么相当？如果不好，卡在哪里？

我们的回答拆成三层：

| 层次 | 对导师的表述 | 当前状态 |
|---|---|---|
| 为什么好 | MTP 把远处语义目标直接监督到当前状态 | 已证明 |
| 为什么高效 | 直接监督缩短 credit assignment path；若梯度有用，则一步更新更快降低语义恢复 loss | 有条件理论桥梁，需实验 |
| 如果相当 | NTP 在全位置训练中也可能通过 indirect transfer 学到；这说明上限可能相同，差别在路径和效率 | 已观察到边界 |

---

## 2. 本科生能懂的类比

假设第一章告诉你“凶手是谁”，第二到第九章很多内容一样，最后一章才需要揭示凶手。

NTP 像是每次只问：

> 下一句话是什么？

如果下一句话只是“于是他说”，那它不一定需要记住凶手。

MTP 像是在这个位置还问：

> 再往后两三句话会出现谁？

如果再往后那句话第一次需要“凶手是谁”，MTP 就会直接要求当前状态记住这个早期信息。

所以 MTP 的作用不是魔法，而是：

> 把未来才用到的信息，提前变成现在的训练目标。

---

## 3. 关键术语

| 术语 | 中文解释 | 当前具体对象 | 不能证明什么 |
|---|---|---|---|
| 长程语义变量 `Z` | 早期出现、未来才用的信息 | branch key `B` | 真实自然语言语义全部情况 |
| 当前状态 `h_T` | 读完 prefix 后的 hidden state | decision prefix hidden state | 后面所有状态的信息 |
| 第一个语义显现位置 `tau` | 第一个真正需要 `Z` 的 future token | K=2 中 `tau=2`；K=3 中 `tau=3` | 自然语言中固定唯一位置 |
| 表示监督优势 | 低 loss 数学上要求 `h_T` 含 `Z` | `I(h_T;Z)` 下界 | 学习速度必然更快 |
| 效率优势 | 更快、更稳恢复 `Z` | `T_theta`, AUC | 最终上限一定更高 |
| 可用表征 | `Z` 不只是能 probe，还能影响输出或 gating | output alignment / route NMI | 真实 MoE utility |

---

## 4. 我们已经证明的内容

### 4.1 K=2 最小证明

构造：

\[
Y_1=A,
\qquad
Y_2=S_Z.
\]

`A` 是所有 branch 共享的 token；`S_Z` 是由早期变量 `Z` 决定的 token。

NTP 在当前状态只需要预测：

\[
h_T\to A.
\]

所以不要求 `h_T` 记住 `Z`。

MTP / next-two 还要求：

\[
h_T\to S_Z.
\]

如果 `h_T` 不含 `Z`，预测 `S_Z` 的最优 CE 下界是：

\[
\log m.
\]

如果 CE 很小：

\[
\mathbb E[-\log q_2(S_Z\mid h_T)]\le\varepsilon,
\]

则：

\[
I(h_T;Z)\ge H(Z)-\varepsilon.
\]

这说明：

> next-two 的低 loss 必然要求 `h_T` 含有早期长程语义变量。

### 4.2 NextK 推广

定义第一个含信息位置：

\[
\tau=\min\{j:I(Z;Y_j\mid Y_{<j})>0\}.
\]

如果 `K < tau`，active targets 还没有碰到真正需要 `Z` 的 token。

如果 `K >= tau`，并且：

\[
Y_\tau=S_Z,
\]

那么低 horizon-`tau` loss 推出：

\[
I(h_T;Z)\ge H(Z)-\varepsilon.
\]

所以 NextK 的精确优势条件是：

\[
K\ge\tau.
\]

---

## 5. 我们还没有证明的内容

没有证明：

> MTP 一定比 NTP 最终上限更高。

原因：全位置 LM 训练里，NTP 可以通过后面的位置学到 `Z`，然后通过共享参数间接影响 `h_T`。

所以正确解释是：

> NTP 可能也能学到，但路径更间接；MTP 的确定优势是更直接。效率优势需要用训练曲线验证。

---

## 6. 高效性的理论桥梁

我们定义一个语义恢复损失：

\[
R_\phi=\operatorname{CE}(s_\phi(h_T),Z).
\]

它衡量从 `h_T` 中读出 `Z` 有多难。

NTP update：

\[
\theta_N^+=\theta-\eta g_1.
\]

MTP update：

\[
\theta_M^+=\theta-\eta(g_1+\lambda g_\tau).
\]

如果 future-token gradient 满足：

\[
\langle\nabla R_\phi,g_\tau\rangle>0,
\]

那么 MTP 一步更新比 NTP 多降低一项：

\[
\eta\lambda\langle\nabla R_\phi,g_\tau\rangle.
\]

这就是“更直接”到“更高效”的最小桥梁。

但是还需要 local guard：

\[
\langle g_1,g_\tau\rangle
\]

不能太负，否则 MTP 可能学到了长程语义，但破坏了本地 next-token 学习。

所以高效性要同时看：

```text
semantic recovery improves faster
local next-token loss does not degrade
future gradient has positive semantic-recovery projection
```

---

## 7. 三个叙述方向

### 方向 1：更快学进表征空间

问题：

> MTP 是否更早让 `h_T` 能恢复 `Z`？

指标：

```text
T_theta: 达到 Q(t) 阈值的步数
AUC_Q: 训练早期语义恢复曲线面积
```

这是最直接回答“高效”的方向。

### 方向 2：更容易发现并固定

问题：

> MTP 学到的 `Z` 是否更线性、更稳定、更 output-facing？

指标：

```text
frozen probe margin
branch-output alignment
future-token logit margin
sign flip rate
representation drift
```

这回答“为什么 MTP 不是只把信息藏起来，而是把它变成可用表征”。

### 方向 3：对模型更有帮助

问题：

> MTP 的长程语义方向是否能服务 downstream 或 MoE gating？

当前不能直接 claim 下游任务，但可以先做 gating proxy：

```text
route NMI with Z
route margin
gate sign flip rate
LM loss guard
branch-specific expert utility proxy
```

这和之前 MoE / nested learning 主线可以接上。

---

## 8. 现有实验的正确解释

### K=2

结论：next-two 确实提供了 NTP 没有的 direct representation supervision。

边界：还没有证明更快。

### K=3 decision-only

结论：如果第一个语义 token 在 horizon 3，只有 K=3 有 direct signal。

边界：这是 isolated decision-prefix scope。

### K=3 all-position

结论：K=3 仍然最强，但 K=1/K=2 也可能恢复 `Z`。

解释：全位置训练中存在 indirect transfer。

边界：不能说 non-covering K 永远学不到。

---

## 9. 汇报时不要说的话

不要说：

```text
MTP 一定比 NTP 好。
NTP 学不到长程语义。
K 越大越好。
现在已经证明学习效率优势。
现在已经证明自然语言提升。
```

应该说：

```text
MTP 的直接表示监督优势已证明。
NTP 也可能通过间接路径学习。
真正要比较的是学习效率、稳定性、表征可用性。
下一步实验专门测这个。
```

---

## 10. 建议向导师提出的 next decision

我们建议下一步不再扩大到更多 K，而是固定一个判定问题：

> MTP 的直接长程语义监督，是否在全位置训练中转化为更快、更稳、更可用的长程语义表征？

两组 protocol：

1. **Semantic efficiency protocol**：测 `T_theta`、AUC、local guard。
2. **Representation/gating protocol**：测 alignment、margin、gradient usefulness、route NMI。

如果通过，我们可以 claim：

> MTP 不只是多了一个表示要求，而且在受控任务中更高效地形成可用的长程语义表征。

如果不通过，我们也有清楚结论：

> MTP 的理论优势停留在 direct representation supervision；在该训练条件下，NTP 的间接路径足够强，效率优势不成立。
