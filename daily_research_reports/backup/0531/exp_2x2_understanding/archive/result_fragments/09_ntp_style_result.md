# 09 NTP-Style Top-1 Audit Result

Status: completed with PyTorch in `torch_geo`.

Setup:

```text
h_A = e1, h_B = e2
targets: A_next, B_next
loss: cross entropy
router: top-1 sparse, gradient through selected softmax gate
no attention
```

## Result

| condition | separated seeds | mean NMI | token acc | key result |
|---|---:|---:|---:|---|
| ntp_known_good | 3/3 | 1.0 | 1.0 | separation works with router prior |
| ntp_no_router_prior | 1/3 | 0.333 | 1.0 | no prior causes lock-in/collapse in most seeds |
| ntp_no_prior_no_expert_advantage | 1/3 | 0.333 | 1.0 | CE alone does not prevent lock-in |

Final rows:

| condition | seed | top1 A | top1 B | margin | NMI | CE | token acc | pattern |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| ntp_known_good | 0 | 0 | 1 | 0.8389 | 1.0 | 0.000012 | 1.0 | separated |
| ntp_known_good | 1 | 0 | 1 | 0.8434 | 1.0 | 0.000012 | 1.0 | separated |
| ntp_known_good | 2 | 0 | 1 | 0.8405 | 1.0 | 0.000012 | 1.0 | separated |
| ntp_no_router_prior | 0 | 0 | 0 | 0.9706 | 0.0 | 0.000054 | 1.0 | collapsed |
| ntp_no_router_prior | 1 | 1 | 1 | 0.9717 | 0.0 | 0.000054 | 1.0 | collapsed |
| ntp_no_router_prior | 2 | 1 | 0 | 0.7940 | 1.0 | 0.000007 | 1.0 | separated |
| ntp_no_prior_no_expert_advantage | 0 | 0 | 0 | 0.9709 | 0.0 | 0.000056 | 1.0 | collapsed |
| ntp_no_prior_no_expert_advantage | 1 | 1 | 1 | 0.9721 | 0.0 | 0.000056 | 1.0 | collapsed |
| ntp_no_prior_no_expert_advantage | 2 | 1 | 0 | 0.7761 | 1.0 | 0.000008 | 1.0 | separated |

## Interpretation

```text
Next-token CE does not force route-pattern separation.
Collapsed routing can still learn both targets perfectly.
Without router prior, initial top-1 choice locks in and becomes confident.
```

## Claim Boundary

Can claim:

```text
In this minimal NTP-style top-1 audit, CE loss alone does not solve top-1
router lock-in.
```

Cannot claim:

```text
full LM behavior
attention behavior
utility-aligned specialization
ABC synthetic failure explanation
```

## Evidence

```text
run_ntp_style_top1_audit.py
tables/ntp_style/
figures/ntp_style/
notes/ntp_style/
```

## Next

```text
Add one anti-lock-in mechanism, not a broad grid:
router prior / exploration noise / load-balancing.
```

