---
parent_node: problem.moe_expert_specialization
source_anchor: Projects/from-attention-to-search/main/problem_anchors/03_ntp_zipf_feature_factorization/04_ntp_zipf_feature_factorization_anchor.md
updated_from: hierarchical_route_utility_binding result + linear FFN Zipf evidence
---

# NTP Factor Attribution And Tail Feature Write-In

## 汇报前 Summary

一句话结论：

```text
这次问题不应再表述成 “H-MoE / hierarchy 能不能解决 gating”，而应表述成：
在 NTP 中，router 到底被哪个 factor 控制，以及真正决定 target 的 tail/slot feature 有没有写进 expert function。
```

为什么要这样改：

```text
hierarchical_route_utility_binding 结果只说明 common path 有弱帮助；
它没有证明两层 hierarchy 本身能稳定解决 route-utility binding。

linear FFN / KV toy 进一步提示：
Zipf 频率会让 head feature 更强写入，tail feature 写入不足；
所以失败可能不只是 router 看错方向，也可能是 tail/slot function 根本没写进 expert。
```

当前决策问题：

```text
下一步不是继续加 hierarchy 深度，也不是直接做 Zipf stress。
下一步应先做 NTP factor attribution + tail write-in diagnostic。
```

最小判断：

```text
如果 tail/slot feature 已经有 expert utility，但 router logits 被 common/head/B-identity 控制，
则测试 common-residual / high-frequency-removed leaf router。

如果 tail/slot feature 本身没有写入 expert function，
则优先做 reweight / tail-write-in pressure，而不是只改 router。
```

## 1. Problem Definition

父问题：

```text
MoE router 如何在 NTP 中形成稳定、可解释、可复用的 feature-level expert specialization？
```

当前更尖锐的子问题：

```text
在受控 NTP synthetic 中，route-utility binding failure 到底来自 routing interference，
还是来自 tail/slot feature write-in failure？
```

这里的核心对象不是 architecture，而是两个因果环节：

```text
feature -> expert function write-in -> expert utility
feature -> router logit / selected route -> route assignment
```

只有两个环节都成立，才能叫 functional specialization。

当前不解决：

```text
不证明真实语料 specialization。
不证明端侧 swapping 收益。
不证明 H-MoE 已经有效。
不把 linear FFN toy 直接当作 Transformer/MoE 结论。
不把 route NMI 或 Assign-Utility 单独当作 specialization。
```

Operational definitions:

```text
feature: 会改变 next-token distribution 的受控生成因子。
write-in: 某 feature 对应的 expert/path 对该 feature 预测有可测 causal utility。
routing dominance: router logit 或 selected route 主要由某个 factor 解释。
route-utility binding: route 与 feature 对齐，并且 route 选中的 expert/path 是 utility-best。
tail-write-in failure: tail/slot feature 在 forced/ablation utility 中没有形成清楚 utility-best path。
routing interference: tail/slot utility 存在，但 router 被 common/head/B-identity factor 带偏。
```

## 2. Physical Priors

Prior 1: NTP hidden state 是组合表征。

```text
B-position hidden state 不只含 slot，也含 B identity、family、common context、head/tail frequency 信息。
因此 router 可能读到可预测但不是目标 feature 的 dominant component。
```

可被削弱的证据：

```text
factor attribution 显示 router logits 不能被这些 factor 解释，或者 slot factor 已经主导 routing。
```

Prior 2: frequency 会改变 function write-in。

```text
Zipfian feature 更频繁地产生梯度；head feature 可能更早、更强地写入参数，
tail feature 即使在数据生成规则中重要，也可能没有形成足够强的 expert utility。
```

可被削弱的证据：

```text
Zipf 与 uniform 在 head/tail utility diagonal、forced loss、ablation utility 上没有差异；
或 reweight 不能恢复 tail utility。
```

Prior 3: hierarchy 不是机制本身。

```text
多一层 router 只有在它把 common/head factor 与 slot/tail factor 分开时才有意义。
如果 hierarchy 只是增加路径结构，而没有改变 router 看到的 causal factor，它不会稳定解决 binding。
```

可被削弱的证据：

```text
two-level hierarchy 在 matched compute、matched data、多个 seeds 下稳定提升 route-slot alignment 与 utility diagonal。
```

## 3. Mechanistic Motivation

已有证据形成的链条：

```text
slot-context NTP:
  slot 信息可见，oracle routing 可行，但 learned top-1 routing 在 multi-B 下不稳定。

hierarchical/common path:
  common_flat 在 64-B uniform 下有弱帮助；
  hierarchical_common 没有稳定超过 common_flat。

linear FFN / KV toy:
  Zipf 频率足以造成 head feature 强写入、tail feature underfit；
  spectral decomposition 更支持 tail write-in failure，而不是简单 high-frequency value interference。
```

因此当前不是问：

```text
H-MoE 能不能 work？
```

而是问：

```text
在 NTP MoE 里，tail/slot feature 是已经写进 expert 但 router 没选对，
还是它根本没有被写进 expert function？
```

这一区分决定下一步方法：

```text
routing interference -> 改 router input / remove common-head subspace / common-residual leaf router。
tail write-in failure -> 改 training pressure / reweight / auxiliary tail write-in objective。
```

## 4. Mathematical Modeling

令一个受控样本的 factor 为：

$$
z=(c,g,i,s)
$$

其中：

$$
c=\text{common factor},\quad
g=\text{B-family factor},\quad
i=\text{B identity / unique factor},\quad
s=\text{slot / target-deciding factor}.
$$

B-position hidden state 写成：

$$
h_{g,i,s}=a_c c+a_g g+a_i b_i+a_s u_s+\epsilon.
$$

router logits：

$$
\ell_e(h)=r_e^\top h.
$$

factor attribution 要估计：

$$
\ell_e^{(F)}=r_e^\top P_F h,
$$

其中 $P_F$ 对应 common、head-frequency、B-family、B-identity 或 slot 子空间。

expert utility 用 ablation / forced loss 测：

$$
\Delta CE(z,e)=CE_z(\operatorname{ablate}(e))-CE_z(\operatorname{full}).
$$

functional specialization 的必要条件是：

$$
\operatorname{route}(z)\approx \operatorname{feature}(z)
\quad \text{and} \quad
\operatorname{route}(z)\approx \arg\max_e \Delta CE(z,e).
$$

如果：

$$
\arg\max_e \Delta CE(z,e)
$$

对 tail/slot 不清楚，则问题是 write-in failure。

如果 utility-best path 清楚，但：

$$
\operatorname{route}(z)
$$

主要由 common/head/B-identity 解释，则问题是 routing interference。

## 5. Computational Realization

数据结构保留 slot-context NTP 形式：

```text
seq_len = 32
positions 10-14: slot/context prefix
position 15: B_i
position 16: Y_{slot, family, i}
```

需要显式控制的 factor：

```text
common context
B-family / group
B identity / unique id
slot / target-deciding factor
head/middle/tail frequency rank
```

最小模型组：

```text
flat_top1 MoE
common_flat
high-frequency-removed or common-residual leaf router, only after attribution supports routing interference
```

暂时不做：

```text
更深 hierarchy sweep
真实语料
reverse index utility
系统侧 swapping
```

## 6. Minimal Decisive Test

### Test A: NTP factor attribution

目的：

```text
判断 router logits / selected route 被哪个 factor 控制。
```

观测：

```text
factor -> router logit R2 / explained variance
factor -> selected expert MI / NMI
factor removal -> route flip rate
```

支持 routing interference，如果：

```text
slot/tail utility 存在；
但 router logits 主要由 common/head/B-identity 解释。
```

### Test B: tail write-in diagnostic

目的：

```text
判断 tail/slot feature 是否真的写进 expert function。
```

观测：

```text
forced expert loss
ablation utility matrix
head/middle/tail utility diagonal
tail/head utility gap
```

支持 tail-write-in failure，如果：

```text
Zipf 下 head features 有清楚 utility-best path；
tail/slot features 没有清楚 utility-best path；
reweight 能恢复 tail utility diagonal。
```

### Test C: mechanism intervention

只在 Test A/B 指明机制后做：

```text
如果是 routing interference:
  common_flat vs common-residual / high-frequency-removed leaf router

如果是 tail write-in failure:
  uniform vs zipf vs zipf_reweight
  或加 tail-write-in pressure / auxiliary objective
```

## 7. Falsifiable Outcomes

支持当前 anchor，如果：

```text
NTP factor attribution 能把 failure 分成 routing interference 或 tail-write-in failure；
并且对应 intervention 改善 route-feature alignment 与 utility diagonal。
```

削弱当前 anchor，如果：

```text
router logits 不被 common/head/B-identity/slot 等 factor 明显解释；
tail/slot utility 也没有系统性 frequency 差异；
则当前 factor decomposition 不足，需要重新定义 feature 或任务。
```

重定向，如果：

```text
所有模型 target accuracy 都高，但 route/utility 指标互相矛盾；
说明当前 synthetic 的 specialization metric 仍有 proxy mismatch，需要先做 metric audit。
```

仍不能证明：

```text
真实语料中的专家分工。
端侧部署收益。
expert id 可直接作为 KV reverse index。
```

## 8. Current Evidence

Evidence 1: slot-context dominance。

```text
slot 信息在 h_B 中可见，oracle routing 可行；
multi-B learned top-1 routing 仍不能稳定绑定 slot 与 utility-best expert。
```

Evidence 2: hierarchical_route_utility_binding。

```text
uniform 64-B 下 common_flat 有弱帮助；
B_long Assign-Utility: flat_top1 0.880, common_flat 0.918, hierarchical_common 0.878。
因此 common path 值得保留，但 two-level hierarchy 本身没有被支持为稳定解法。
```

Evidence 3: linear FFN frequency anisotropy。

```text
Zipf-normal 产生更尖的 spectrum、更低 effective rank、更高 tail/head error；
inverse-frequency reweight 基本恢复到 uniform。
```

Evidence 4: linear FFN spectral decomposition。

```text
Zipf-normal 下 head->head component 强，tail->tail component 弱；
remove-top / W_low 对 tail error 改善很小。
这更支持 tail feature 没写入，而不是 tail 已写入但被 top directions 污染。
```

证据边界：

```text
linear FFN 不是 NTP Transformer/MoE；
hierarchical result 是 uniform 64-B moderate stress；
所以二者只能决定下一步诊断，不足以直接下 NTP router 机制结论。
```

## 9. Claim Boundary And Next Decision

最安全 claim：

```text
当前证据把问题从 “H-MoE 是否有效” 收窄为：
NTP 中 route-utility binding failure 到底来自 factor-level routing interference，
还是来自 tail/slot feature write-in failure。
```

不能 claim：

```text
不能 claim H-MoE 已经解决 gating。
不能 claim common-residual 一定有效。
不能 claim Zipf 下 tail failure 一定会出现在 NTP MoE。
不能 claim linear FFN toy 直接解释 Transformer router。
不能 claim high Assign-Utility 单独证明 specialization。
```

下一步最小决策：

```text
先跑 NTP factor attribution + tail write-in diagnostic。
```

判断分叉：

```text
若 utility 存在但 route 被 common/head/B-identity 控制：
  做 common-residual / high-frequency-removed leaf router。

若 tail/slot utility 不存在或很弱：
  做 reweight / tail-write-in pressure。

若两者都不成立：
  重新审查 synthetic feature 定义和 specialization metric。
```

