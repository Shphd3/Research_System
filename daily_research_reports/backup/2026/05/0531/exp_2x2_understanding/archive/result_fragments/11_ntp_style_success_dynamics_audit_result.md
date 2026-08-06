# NTP-Style Success Dynamics Audit Result

## Conclusion

成功 seed 支持：

```text
如果 step 0 已经把 A/B 分到不同 expert，后续训练会稳定保持这个分发。
router logits/probability 会放大初始 top-1 选择。
selected expert 会形成对对应 token 的 counterfactual CE 优势。
```

## Scope

只审查已有 NTP-style top-1 实验中的成功 seed：

```text
ntp_no_router_prior seed 2
ntp_no_prior_no_expert_advantage seed 2
```

不新增实验条件。

## Main Evidence

| condition | step 0 top1 | step 300 top1 | final NMI | final selected gate | final CE gap selected-unselected | stable |
|---|---|---|---:|---|---|---:|
| ntp_no_router_prior | A->E1, B->E0 | A->E1, B->E0 | 1.0 | A 0.903, B 0.891 | A -3.899, B -3.981 | 1 |
| ntp_no_prior_no_expert_advantage | A->E1, B->E0 | A->E1, B->E0 | 1.0 | A 0.892, B 0.884 | A -4.547, B -4.644 | 1 |

Figure:

![NTP-style success dynamics audit](figures/ntp_style_success_dynamics_audit.png)

## Metric Meaning

selected logit margin:

```text
selected expert logit - unselected expert logit
```

It measures router preference before softmax.

selected gate probability:

```text
softmax probability of the selected top-1 expert
```

It measures router confidence after softmax.

CE selected - unselected:

```text
counterfactual CE if routed to selected expert
minus CE if routed to unselected expert
```

Negative means the selected expert is better for that token.

expert update norm:

```text
parameter change size of each expert after the previous step
```

It checks whether both selected experts are actually being trained.

## Interpretation

Observation:

```text
step 0 only weakly separates: selected gate is about 0.50.
by step 10, selected gate rises to about 0.73.
by step 50, selected gate is about 0.88-0.90 and stays stable.
selected logit margin rises from near 0 to about 2.
CE gap changes from slightly positive/near neutral to strongly negative.
```

Interpretation:

```text
the initial split does not need to be confident;
it only needs to give each feature a different top-1 expert early enough.
after that, each expert receives its own token updates,
and the router/expert pair co-amplifies the initial split.
```

## Claim Boundary

Can claim:

```text
In this minimal NTP-style top-1 setup, successful initial split is stable and
can produce token-specific counterfactual expert advantage.
```

Cannot claim:

```text
The learned expert advantage is utility-aligned specialization.
The same stability holds in full LM or attention settings.
The result explains ABC synthetic failure.
```

## Next Decision

The current mechanism picture is:

```text
initial same expert -> lock-in + starvation -> collapse
initial different experts -> co-amplification -> stable route-pattern separation
```

Next minimal test:

```text
add one anti-lock-in mechanism and check whether it increases the probability
that A/B are split at step 0/10 or prevents starvation after an initially bad split.
```

## Artifacts

```text
runner: run_ntp_style_success_dynamics_audit.py
csv: tables/ntp_style_success_dynamics_audit.csv
figure: figures/ntp_style_success_dynamics_audit.png
notes: notes/ntp_style_success_dynamics_audit.md
```
