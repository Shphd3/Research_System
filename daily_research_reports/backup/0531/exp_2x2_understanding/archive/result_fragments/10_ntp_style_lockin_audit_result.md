# NTP-Style Early Lock-In Audit Result

## Conclusion

本次 audit 支持：

```text
失败 seed 的 collapse 在 step 0 已经发生，不是训练中从分离逐渐 drift 成 collapse。
训练主要是在放大 step 0 的 top-1 选择：selected gate 快速上升，未选 expert 被 starvation。
```

## Scope

只审查已有 NTP-style top-1 实验：

```text
ntp_no_router_prior
ntp_no_prior_no_expert_advantage
```

审查 seeds：

```text
failed controls: seed 0, seed 1
success control: seed 2
```

Checkpoints:

```text
0, 10, 50, 100, 200, 300
```

## Main Evidence

| condition | seed | step 0 top1 | step 300 top1 | final NMI | final selected gate | tag |
|---|---:|---|---|---:|---|---|
| ntp_no_router_prior | 0 | A->E0, B->E0 | A->E0, B->E0 | 0.0 | A 0.985, B 0.986 | early_lock_in |
| ntp_no_router_prior | 1 | A->E1, B->E1 | A->E1, B->E1 | 0.0 | A 0.986, B 0.985 | early_lock_in |
| ntp_no_router_prior | 2 | A->E1, B->E0 | A->E1, B->E0 | 1.0 | A 0.903, B 0.891 | success_control |
| ntp_no_prior_no_expert_advantage | 0 | A->E0, B->E0 | A->E0, B->E0 | 0.0 | A 0.986, B 0.985 | early_lock_in |
| ntp_no_prior_no_expert_advantage | 1 | A->E1, B->E1 | A->E1, B->E1 | 0.0 | A 0.986, B 0.986 | early_lock_in |
| ntp_no_prior_no_expert_advantage | 2 | A->E1, B->E0 | A->E1, B->E0 | 1.0 | A 0.892, B 0.884 | success_control |

Figure:

![NTP-style lock-in audit](figures/ntp_style_lockin_audit.png)

## Interpretation

Observation:

```text
失败 seed 在 step 0 就已经把 A/B 分到同一个 expert。
step 10 selected gate 已经升到约 0.88。
step 300 selected gate 约 0.985。
失败 seed 的 expert usage 始终是 1/0 或 0/1。
```

Interpretation:

```text
top-1 选择先随机锁定。
随后 selected gate 变自信。
未选 expert 对这些 token 没有 usage，也几乎没有 update。
最后 selected expert 学会同时预测 A_next 和 B_next。
```

Counterfactual CE:

```text
collapse seed 中，selected expert 对 A/B 的 CE 接近 0。
unselected expert 的 CE 明显更高。
success seed 中，A/B 各自 selected expert 的 CE 接近 0，反向 expert 的 CE 很高。
```

这说明失败不是因为线性 router 无法表达分离；更像是 early top-1 lock-in 加上 expert starvation。

## Claim Boundary

Can claim:

```text
在当前最小 NTP-style top-1 实验中，collapse 主要由 step-0/10 early lock-in 和 starvation 放大。
```

Cannot claim:

```text
完整 LM 一定如此。
attention 场景一定如此。
utility-aligned specialization 成立。
ABC synthetic failure 已被完整解释。
```

## Next Decision

下一步只加一个 anti-lock-in 机制，然后看它是否改变 step 0/10 的轨迹：

```text
router prior / exploration noise / load-balancing 三选一
```

如果目标是先最小验证机制，优先试：

```text
exploration noise 或 load-balancing
```

因为它们直接针对 early lock-in / starvation，而不是重新给 router 一个正确答案。

## Artifacts

```text
runner: run_ntp_style_lockin_audit.py
csv: tables/ntp_style_lockin_audit.csv
figure: figures/ntp_style_lockin_audit.png
notes: notes/ntp_style_lockin_audit.md
```
