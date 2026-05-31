# 08 NTP-Style Top-1 Audit Plan

Status: plan for user audit. Do not run before approval.

Goal:

```text
Check whether a real next-token CE objective changes the top-1 sparse proxy result:
without anti-lock-in signal, top-1 routing tends to lock early.
```

## Question

```text
In a minimal NTP-style task, can top-1 sparse MoE learn feature-route separation
from next-token cross entropy?
```

Boundary:

```text
route-pattern only
not utility-aligned specialization
not full language modeling
no attention in first audit
```

## Data

```text
context types: A_ctx, B_ctx
fixed hidden: h_A = e1, h_B = e2
target tokens: A_next, B_next
samples: h_A -> A_next; h_B -> B_next
balanced A/B frequency
```

Use fixed one-hot hidden states, not trainable embeddings, in the first audit.
This keeps A/B orthogonal and aligned with the current anchor.

No position, slot, embedding drift, or frequency shortcut in the first audit.

## Model

Use PyTorch in `torch_geo`.

```text
h in {e1, e2}
router = Linear(d_model=2, 2)
top-1 sparse MoE block
LM head = Linear(d_model, vocab)
loss = cross_entropy(logits, next_token)
```

Experts:

```text
2 small Linear or MLP experts: d_model -> d_model
```

No embedding layer in the first audit.

## Top-1 Sparse Routing

Do not use naive argmax-only training.

```text
probs = softmax(router_logits)
top1 = argmax(probs)
selected_gate = probs[top1]
output = selected_gate * expert_top1(h)
```

Forward is sparse:

```text
only selected expert output is used
```

Router gets gradient:

```text
through selected_gate
```

## Conditions

Run only:

| condition | router prior | expert advantage | purpose |
|---|---|---|---|
| ntp_known_good | yes | yes | implementation sanity |
| ntp_no_router_prior | no | yes | test lock-in without router prior |
| ntp_no_prior_no_expert_advantage | no | no | test whether CE alone creates split |

No broad grid.

## Metrics

Primary:

```text
route-feature heatmap
```

Secondary:

```text
NMI / assignment accuracy
selected gate confidence
expert usage
cross entropy loss
per-feature next-token accuracy
```

Metric boundary:

```text
heatmap + NMI -> route-pattern claim
loss / accuracy -> task learned
loss does not prove routing caused learning
```

## Judgment

Success:

```text
A_ctx and B_ctx route to different experts across checkpoints/seeds;
CE loss decreases;
per-feature accuracy high.
```

Failure:

```text
both contexts route to same expert;
NMI = 0 or assignment accuracy = 0.5;
CE loss may still decrease.
```

Insufficient evidence:

```text
single seed only;
only final checkpoint;
CE does not learn;
route metric conflicts with feature accuracy.
```

## Outputs

```text
tables/ntp_style/<condition>/metrics_by_checkpoint.csv
tables/ntp_style/<condition>/seed_checkpoint_summary.csv
figures/ntp_style/<condition>/heatmap_*.png
figures/ntp_style/<condition>/trajectory_*.png
notes/ntp_style/<condition>/run_observations.md
```

## User Audit

Approve before execution:

```text
No attention in first audit? yes
Use selected_gate * expert_top1(h)? yes
Run only three conditions? yes
Primary metric remains route-feature heatmap? yes
Treat as NTP-style audit, not full LM? yes
```
