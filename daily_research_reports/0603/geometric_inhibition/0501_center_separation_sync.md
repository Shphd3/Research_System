# 0501 Sync: Center Separation Does Not Reliably Bind Assignment

## Conclusion

严格按当前定义，`geometric separation = router-center separation only`。在这个定义下，05_01 的结论是：

**`slot-init + center separation only` 没有稳定地把同一个 feature 分发到同一个 expert。**

最强条件 K1 有几何信号，但不是稳定 assignment binding：两个 seed 出现较强 slot 分开，一个 seed 完全坍缩到单 expert。

如果把 C2/C5 也叫作 `inhibition`，结论会不同：C2/C5 确实达到 final route-slot NMI 1.000、std 0.000。但 C2/C5 使用 supervised token-margin / logit-margin，并且依赖外部 assignment $a(s,i)=s$。因此它们只能说明“外部指定 token-to-expert margin 可以强制稳定分发”，不能说明 center separation alone 可以自然发现或绑定 assignment。

## Definitions

| Term | Meaning in this sync |
|---|---|
| `feature` / `slot` | synthetic data 中的 slot label $s$ |
| `same feature to same expert` | 同一 slot 的 $B_i$ hidden states 在最终 top-1 routing 中主要进入同一 expert，并且跨 seeds 不出现 collapse 或 slot merge |
| `center separation only` | 只让 normalized router rows 彼此分开；不使用 supervised token-margin |
| `assignment binding` | 决定哪个 hidden state 应该进入哪个 expert 的机制；不等于只分开 expert centers |

## Key Conditions

| Code | Router | Init | Extra objective | Use for current claim? |
|---|---|---|---|---|
| C1 | dot-product | slot-init | none | baseline |
| C2 | dot-product | slot-init | supervised token-margin + center separation | not center-only evidence |
| C4 | cosine | slot-init | none | baseline |
| C5 | cosine | slot-init | supervised token-margin + center separation | not center-only evidence |
| D1 | dot-product | slot-init | center separation only | yes |
| K1 | cosine | slot-init | center separation only | yes; strongest but unstable |

## Main Evidence

Primary metric: final route-slot NMI with seed variance.

Why it decides this question: the question is not whether the model learns the prediction task, but whether routing itself forms a stable slot/feature partition. Accuracy is necessary sanity evidence, but not specialization evidence.

| Condition | Final route-slot NMI | Std | Accuracy | Interpretation |
|---|---:|---:|---:|---|
| D1 | 0.446 | 0.320 | 1.000 | dot + slot-init + center separation only is unstable |
| K1 | 0.566 | 0.491 | 1.000 | cosine + slot-init gives the strongest signal, but seed variance is too high |
| C2 | 1.000 | 0.000 | 1.000 | supervised token-margin succeeds, but this is not center-only |
| C5 | 1.000 | 0.000 | 1.000 | supervised token-margin succeeds, but this is not center-only |

## Does the Inhibition Group Route the Same Feature to the Same Expert?

Answer depends on which group is meant.

### If `inhibition` means center separation only: no

D1 and K1 do not stably assign the same feature to the same expert.

| Condition | Seed | Final route-slot NMI | Diagnostic assignment pattern | Judgment |
|---|---:|---:|---|---|
| D1 | 20260521 | 0.640 | slots 0/1/2 are mostly separated, slot 3 merges toward expert 2 | partial |
| D1 | 20260522 | 0.094 | all slots route to expert 3 by utility-best pattern | collapse |
| D1 | 20260523 | 0.634 | slot 0 and slot 2 merge toward expert 2 | partial |
| K1 | 20260521 | 0.858 | slots 0/1/2/3 align to experts 0/1/2/3 | strong |
| K1 | 20260522 | 0.000 | all slots route to expert 3 | collapse |
| K1 | 20260523 | 0.859 | slot 0 and slot 2 both route to expert 2; slots 1/3 separate | strong but not one-to-one |

The decisive counterexample is K1 seed `20260522`: despite cosine router, slot-init, and center separation only, all slots collapse to one expert. This prevents the claim that the method stably routes the same feature to the same expert.

### If `inhibition` means C2/C5 supervised token-margin: yes, but bounded

C2 and C5 have final route-slot NMI 1.000 with std 0.000. In that supervised setting, the same slot is stably forced toward the assigned expert.

Claim boundary: this does not show that the model discovered the assignment. The objective already supplies the assignment through $a(s,i)=s$.

## Why E-to-S Cosine Can Disagree With Dispatch

The prototype is the mean of qualifying hidden states, but final dispatch is top-1 over each individual hidden state. Therefore these are different objects:

| Object | What it measures | Why it can disagree |
|---|---|---|
| E-to-S cosine | cosine between router center and slot prototype mean | mean geometry can look aligned even when individual samples have variance or shared components |
| route heatmap | empirical top-1 dispatch of individual hidden states | top-1 competition can collapse or merge slots even if prototype directions are partly separated |

Interpretation: K1 has usable prototype geometry, but center separation only does not bind actual sample-level hidden states to distinct experts.

## Claim Boundary

Can claim:

Under the tested uniform multi-B setup, center separation alone is not a reliable mechanism for stable slot-specialized routing.

Cannot claim:

This does not refute all unsupervised geometry methods. It does not show that cosine slot-init is useless. It does not decide Zipfian behavior or real-data transfer. It does not prove expert utility specialization.

## Next Decision

Do not move to 05_02 as if center separation succeeded. The next anchor should first name the missing mechanism: assignment discovery / assignment binding / anti-merge. K1 should be used as the strongest baseline because it contains a real geometric signal but fails stability.
