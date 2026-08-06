# NTP-Style No Router Bias Result

## Conclusion

去掉 router bias 有改善，但不是完整解决方案。

```text
with bias:  random router initial split 3/10 -> final split 3/10
no bias:    random router initial split 6/10 -> final split 6/10
router prior: known-good split 10/10 -> final split 10/10
```

关键解释：

```text
bias 会给 A/B 共享同一个 expert 偏移，增加 delta_A 和 delta_B 同号的机会。
去掉 bias 后，A/B 的初始 top-1 更接近独立随机，因此 split 率提高到约一半。
但如果初始化仍然让 A/B 的 delta 同号，top-1 lock-in 仍会发生。
```

## Setup

只改一件事：

```text
router = Linear(2, 2, bias=False)
```

其它保持不变：

```text
fixed h_A=e1, h_B=e2
2 experts
top-1 sparse routing
CE next-token objective
300 training steps
seeds 0-9
```

## Result

| condition | router bias | initial split | final split | mean final NMI | token acc |
|---|---|---:|---:|---:|---:|
| ntp_known_good | yes | 10/10 | 10/10 | 1.0 | 1.0 |
| ntp_known_good | no | 10/10 | 10/10 | 1.0 | 1.0 |
| ntp_no_router_prior | yes | 3/10 | 3/10 | 0.3 | 1.0 |
| ntp_no_router_prior | no | 6/10 | 6/10 | 0.6 | 1.0 |
| ntp_no_prior_no_expert_advantage | yes | 3/10 | 3/10 | 0.3 | 1.0 |
| ntp_no_prior_no_expert_advantage | no | 6/10 | 6/10 | 0.6 | 1.0 |

Figure:

![No router bias summary](figures/ntp_style_no_router_bias/summary_by_seed.png)

## Mechanism

For this setup:

```text
logits = W_r h + b
h_A = e1, h_B = e2
delta_A = logit_A_E1 - logit_A_E0
delta_B = logit_B_E1 - logit_B_E0
```

Decision rule:

```text
delta > 0 -> E1
delta < 0 -> E0
```

Collapse condition:

```text
delta_A and delta_B have the same sign.
```

Split condition:

```text
delta_A and delta_B have opposite signs.
```

With bias:

```text
delta_A = column difference for A + shared bias difference
delta_B = column difference for B + shared bias difference
```

The shared bias difference moves both deltas in the same direction, so it can
make A/B collapse to the same expert.

Without bias:

```text
delta_A and delta_B depend only on separate router columns.
```

That reduces shared drift, but a random matrix can still make both deltas same
sign.

## Interpretation

Observation:

```text
No-bias improves initial split from 3/10 to 6/10 in the random-router settings.
Final split exactly follows initial split.
Token accuracy is 1.0 even when routing collapses.
```

Interpretation:

```text
removing bias helps by reducing common expert preference,
but the deeper issue is still top-1 early lock-in.
```

## Claim Boundary

Can claim:

```text
In this minimal NTP-style top-1 setup, router bias worsens random-init collapse
by adding a shared expert preference across A/B.
```

Cannot claim:

```text
No-bias guarantees specialization.
No-bias solves full MoE load collapse.
No-bias produces utility-aligned specialization.
```

## Next Decision

Keep this result as a diagnostic, not as the final fix.

Candidate next mechanisms:

```text
structured router initialization
exploration noise
load-balancing
```

Among these, structured initialization is the cleanest test of your hypothesis:

```text
good initial token-router geometry can preserve expert specialization.
```

## Artifacts

```text
runner: run_ntp_style_no_router_bias_audit.py
comparison runner: run_ntp_style_router_bias_comparison.py
tables: tables/ntp_style_no_router_bias/
comparison: tables/ntp_style_router_bias_comparison.csv
figures: figures/ntp_style_no_router_bias/
notes: notes/ntp_style_no_router_bias_audit.md
comparison note: notes/ntp_style_router_bias_comparison.md
```
