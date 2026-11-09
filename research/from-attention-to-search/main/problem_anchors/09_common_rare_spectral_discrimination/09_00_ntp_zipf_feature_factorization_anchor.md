---
parent_node: problem.moe_expert_specialization
---

# NTP Zipf Feature Write-In And Router Factor Attribution


## 1. Problem Definition

Broader question:

```text
MoE router 如何在 NTP 中形成稳定、可解释、可复用的 feature-level expert specialization？
```

Sharper question:

```text
Zipfian NTP 是否会造成 high-frequency feature write-in / routing dominance，从而使 tail/unique/slot feature 无法形成稳定 route-utility binding？
```

What we do not need to do now:

```text
不直接证明真实语料效果。
不继续增加 hierarchy 深度。
不把 non-NTP linear FFN toy 当作 NTP 结论。
不把高 Assign-Utility 单独当作 specialization。
不预设 common-residual 一定有效。
```

Operational definitions:

```text
feature: 会改变 next-token distribution 的受控生成因子。
write-in: 某 feature 对应的 expert/function 参数中确实有可测的 causal utility。
routing dominance: router logit 或 selected path 主要由某个 factor 解释。
route-utility binding: 被选中的 expert/path 同时与 feature 对齐，并且是该 feature 的 utility-best path。
```

## 2. Physical Priors

```text
1. NTP hidden state 是组合表征：同一位置可以同时包含 common context、B identity、family、slot、head/tail unique feature。
2. 语言中的 feature frequency 通常是 Zipfian；高频 feature 更频繁产生梯度，可能更早、更强地写入参数。
3. 但是 router failure 有多个可能来源：common dominance、head-frequency dominance、B identity dominance、slot/target feature 太弱、tail feature 根本没写入 expert function。
4. 因此下一步必须做 factor attribution，而不是直接把所有失败都解释成 common dominance。
```

## 3. Hypothesis / Mechanism

已有证据给出的最小链条是：

```text
slot-context NTP:
  slot 信息可见，oracle routing 可行，但 learned routing 不稳定。

H-MoE/common path:
  common_flat 有弱帮助，two-level hierarchy 本身不稳定。

linear FFN/KV toy:
  Zipf 频率足以造成 head write-in 和 tail underfit，但它不是 NTP。
```

因此现在的真正问题是：

```text
在 NTP 中，tail/slot feature 是没有写进 expert function，还是写进去了但 routing 被 high-frequency factors 干扰？
```

这两个机制对应不同解法：

```text
tail 没写入：需要 reweight / tail-write-in pressure / auxiliary objective。
routing 被干扰：需要 route-neutral / high-frequency-removed / residual leaf router。
```

## 4. Mathematical Model
受控 NTP factor：

\[
z=(c, g, i, s),
\]

其中：

\[
c: \text{common factor},\quad
 g: \text{B-family / group factor},\quad
 i: \text{B identity / unique factor},\quad
 s: \text{slot / target-deciding factor}.
\]

B 位置 hidden state 可写成：

\[
h_{g,i,s}=a_c c+a_g g+a_i b_i+a_s u_s+\epsilon.
\]

router logits：

\[
\ell_e(h)=r_e^\top h.
\]

factor contribution：

\[
\ell_e^{(F)}=r_e^\top P_F h,
\]

其中 \(P_F\) 是 common、head-frequency、B-family、B-identity 或 slot factor 的 probe/projector。

expert utility：

\[
\Delta CE(z,e)=CE_z(\operatorname{ablate}(e))-CE_z(\operatorname{full}).
\]

functional specialization 需要同时满足：

\[
\operatorname{route}(z) \approx \operatorname{feature}(z)
\quad\text{and}\quad
\operatorname{route}(z) \approx \arg\max_e \Delta CE(z,e).
\]

## 5. Computational Realization

### 5.1 Data Structure

保留上次 slot-context 数据风格：

```text
seq_len = 32
positions 10-14: slot/context prefix
position 15: B_i
position 16: Y_{slot, family, i}
```

slot context 两种：

```text
A_long_repeated:
slot 0: A A A A A + B_i -> Y_{0, g, i}
slot 1: C C C C C + B_i -> Y_{1, g, i}
slot 2: G G G G G + B_i -> Y_{2, g, i}
slot 3: K K K K K + B_i -> Y_{3, g, i}
```

```text
B_long_distributed:
slot 0: p0 q0 r0 t0 u0 + B_i -> Y_{0, g, i}
slot 1: p0 q1 r1 t1 u1 + B_i -> Y_{1, g, i}
slot 2: p1 q0 r1 t0 u1 + B_i -> Y_{2, g, i}
slot 3: p1 q1 r0 t1 u0 + B_i -> Y_{3, g, i}
```

Zipf factor：

```text
uniform: B_i or feature_i sampled uniformly
zipf: B_i or feature_i sampled with P(i) ∝ (i+1)^(-alpha)
zipf_reweight: sampling is Zipf, but target-position loss is inverse-frequency reweighted
```

True hierarchy 版本只在需要时加入：

```text
B families = 4
B per family = 16 or 64
slots = 4
root target = family / B-family
leaf target = slot / target-deciding feature
```

### 5.2 Models

最小模型组：

```text
A. flat_top1 MoE
B. common_flat: global common path + one-level leaf router
C. high-frequency-removed leaf router, only if factor attribution supports router interference
```

不要先跑更深 hierarchy。若要测试 hierarchy，必须让数据中有真实 root/leaf factor：

```text
root = B-family or feature-family
leaf = slot / target-deciding unique feature
```

## 6. Proposed Next Mechanism: High-Frequency Removal For Leaf Routing

导师的 KV 直觉可以写成：

\[
W \approx \sum_f \alpha_f v_f k_f^\top.
\]

对 query：

\[
q_i = k_c+k_i,
\]

输出：

\[
W q_i \approx \sum_f \alpha_f v_f\langle k_f,q_i\rangle.
\]

把 feature 分为 high-frequency 与 low-frequency：

\[
\mathcal H=\text{head/common factors},\qquad
\mathcal L=\text{tail/slot/unique factors}.
\]

理想分解：

\[
W=W_{\mathcal H}+W_{\mathcal L},
\]

其中：

\[
W_{\mathcal H}=\sum_{f\in\mathcal H}\alpha_f v_f k_f^\top,
\]

\[
W_{\mathcal L}=\sum_{f\in\mathcal L}\alpha_f v_f k_f^\top.
\]

如果问题是 high-frequency component 干扰 leaf routing，那么 leaf router 不应直接看 \(h\)，而应看：

\[
h_{leaf}=(I-P_{\mathcal H})h,
\]

或等价地使用 high-frequency-removed routing map：

\[
\ell_{leaf}=R_{leaf}(I-P_{\mathcal H})h.
\]

但是这个方法只有在以下诊断成立时才值得做：

```text
1. tail/slot feature 已经写入 expert function；
2. router logit 的主要解释量来自 common/head/B-identity subspace；
3. 去掉 high-frequency subspace 后，slot route alignment 和 utility binding 上升。
```

如果 tail/slot feature 根本没有写入 expert function，则 \(W_{\mathcal L}\) 本身很弱，单纯去掉 \(W_{\mathcal H}\) 或 \(P_{\mathcal H}\) 不会解决问题。

## 7. Minimal Falsifiable Test

### Test A: NTP Factor Attribution

训练 flat/common MoE 后，在 B position 计算：

```text
router logit factor contribution:
common / head-frequency / B-family / B-identity / slot
```

支持 router-interference 假设，如果：

```text
Zipf 下 router logits 主要由 common/head/B-identity 解释；
slot factor 对 logits 的解释量较弱；
但 forced/ablation 显示 slot expert utility 是可用的。
```

削弱，如果：

```text
router 并没有被 high-frequency factors 控制，或 slot utility 根本不可用。
```

### Test B: NTP Tail Write-In Test

按 head/middle/tail feature 分组，计算：

```text
forced expert loss
ablation utility
head/tail utility diagonal
```

支持 tail-write-in failure，如果：

```text
Zipf 下 head features 有清楚 utility-best expert，tail features 没有；
reweight 恢复 tail utility diagonal。
```

### Test C: High-Frequency-Removed Leaf Router

仅在 Test A/B 支持时运行：

```text
common_flat vs high-frequency-removed leaf router
uniform vs zipf vs zipf_reweight
64-B and 256-B stress
```

支持，如果：

```text
route-slot NMI ↑
Assign-Utility ↑
forced-loss diagonal ↑
target CE / accuracy 不下降
```

## 8. Current Evidence

```text
1. slot-context anchor:
slot 信息可见，oracle 可行，但 multi-B learned routing 不稳定。

2. H-MoE/common path NTP experiment:
common_flat 在 B_long 上 modestly improves；hierarchical_common 不稳定，因此不能声称 hierarchy alone works。

3. linear FFN/KV toy:
非 NTP setting 中，Zipf 造成 head-feature anisotropy 和 tail underfit，reweight 恢复；但它只能作为机制启发，不能直接证明 NTP router failure。

4. spectral decomposition:
非 NTP toy 中 tail failure 更像 tail write-in failure，而不是 high-frequency value interference；但这仍需在 NTP 中复验。
```

## 9. Claim Boundary And Next Decision

可以 claim：

```text
当前证据要求我们把问题从 “H-MoE 是否有效” 改写成 “NTP 中到底哪个 factor 控制 routing，tail/slot feature 是否写入 expert function”。
```

不能 claim：

```text
不能 claim H-MoE 已经解决 gating。
不能 claim non-NTP linear FFN 证明了 NTP router failure。
不能 claim remove high-frequency W 一定有效。
不能 claim Zipf 下 tail 失败一定来自 routing interference。
```

下一步决策：

```text
先跑 NTP factor attribution + tail write-in diagnostic。
若 router interference 成立，再做 high-frequency-removed leaf router。
若 tail write-in failure 成立，则优先做 reweight / tail-write-in objective。
```
