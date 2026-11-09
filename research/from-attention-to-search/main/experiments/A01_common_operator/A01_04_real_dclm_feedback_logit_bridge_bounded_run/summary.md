# Summary: A01_04 Real-DCLM Feedback Logit Bridge Bounded Run

## Conclusion

The bounded real-DCLM gate-logit bridge does not support a low-rank
feedback-logit common explanation for the A06 proxy-route collapse.

The run successfully recovered real gate-logit artifacts and reproduced the
`A06_01_04_E03` collapse surface: mean proxy-route NMI drops from 0.7549 at step 0 to
0.0410 at step 5 and 0.0131 at step 10. However, rank-1 top logit-drift replay
explains only 0.4230 of the full NMI drop on average, and rank-1 removal
rescues only 0.1625. Random controls are close enough that the feedback-logit
subspace is not a strong specific explanation.

Primary result:

```text
pass = false
denominator_valid_cells = 18 / 18
mean_explain_valid = 0.4230
mean_rescue_valid = 0.1625
mean_random_explain_valid = 0.3355
mean_random_rescue_valid = 0.1177
```

Interpretation: the controlled feedback bridge remains valid, but the real
A06 collapse is not explained by a simple low-rank gate-logit common drift.
The next real mechanism test should separate hidden-state drift, gate-weight
drift, and expert-update feedback rather than treating the gate-logit drift as
one low-rank common object.

## Setup

The run reuses the `A06_01_04_E03` real-DCLM proxy-center setup:

- DCLM-bin data;
- 6-layer Qwen3-MoE toy model;
- raw-center router initialization;
- model seeds 0, 1, and 2;
- audit layers 3, 4, and 5;
- 65,536 eval tokens per layer;
- checkpoints 0, 5, and 10.

Captured object:

\[
z_{\ell,t}=W_{\ell,t}h_{\ell,t}
\]

Replay/removal uses logit drift:

\[
\Delta z_{\ell,t}=z_{\ell,t}-z_{\ell,0}
\]

## Main Results

| Step | Step0 NMI | Full NMI | Feedback-only NMI | Residual-only NMI | Explain | Rescue | Random explain |
|---|---:|---:|---:|---:|---:|---:|---:|
| 5 | 0.7549 | 0.0410 | 0.4327 | 0.1933 | 0.4423 | 0.2105 | 0.3344 |
| 10 | 0.7549 | 0.0131 | 0.4509 | 0.0982 | 0.4037 | 0.1145 | 0.3365 |

The full logit drift reproduces the preservation failure. The top rank-1
feedback-logit drift explains part of the collapse, but not enough to pass the
bridge rule. Removing it also does not rescue routing.

## Rank Sweep

Higher logit ranks explain more of the collapse, but random subspaces also
improve as rank increases:

| Rank | Explain | Rescue | Random explain | Pass |
|---:|---:|---:|---:|---|
| 1 | 0.4230 | 0.1625 | 0.2852 | false |
| 2 | 0.6341 | 0.2793 | 0.4915 | false |
| 3 | 0.7526 | 0.4177 | 0.5985 | false |
| 4 | 0.8565 | 0.5375 | 0.7056 | false |
| 5 | 0.9168 | 0.6362 | 0.7732 | false |
| 6 | 0.9582 | 0.7465 | 0.8446 | false |
| 7 | 0.9845 | 0.8640 | 0.9251 | false |

This weakens the low-rank feedback-logit common explanation. High-rank replay
mostly approaches the full drift and is not specific enough.

## Central Figures

![Real-DCLM logit bridge NMI](runs/real_dclm_logit_bridge_20260629_full01/figures/real_feedback_logit_bridge_nmi_by_step.png)

This figure shows that the recovered artifacts reproduce the A06 collapse:
full drift collapses NMI, while rank-1 feedback-only replay explains only part
of the drop and residual-only removal does not rescue the route.

![Real-DCLM logit bridge explanation and rescue](runs/real_dclm_logit_bridge_20260629_full01/figures/real_feedback_logit_bridge_explain_rescue.png)

This figure tests the primary pass rule. Rank-1 explanation stays below 0.5,
and rescue is substantially lower.

![Real-DCLM feedback logit rank sweep](runs/real_dclm_logit_bridge_20260629_full01/figures/real_feedback_logit_rank_sweep.png)

This figure shows that higher ranks reconstruct more collapse, but random
subspaces also approach the same effect. The result is not a specific low-rank
feedback-common mechanism.

## Claim Boundary

This run supports: real gate-logit artifacts were recovered, and the A06
step-0 to step-5/10 collapse was reproduced in the bridge surface.

This run weakens: a simple low-rank gate-logit feedback common as the main
explanation or rescue target.

This run does not decide: hidden-state feedback common, separate gate-weight
versus hidden-state drift, expert feedback, optimizer geometry, or
LM-loss-neutral anti-feedback intervention.

## Next Decision

The next mechanism test should decompose the real collapse into:

```text
hidden-state drift
gate-weight drift
expert-update feedback
```

The current result argues against jumping directly to a residualized MoE method
based only on low-rank gate-logit common.
