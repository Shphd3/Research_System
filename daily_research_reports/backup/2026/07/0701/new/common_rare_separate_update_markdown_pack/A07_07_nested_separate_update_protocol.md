# Protocol: A07_07 Nested Common/Rare Separate-Update Mechanism Audit

## Purpose

Test whether common/rare separate updating changes the actual update mediator
behind tail failure.

Primary question:

```text
Does separate updating reduce tail update mass in the common high-gain subspace
and improve tail loss without damaging common loss?
```

## Setup

Use controlled nested data:

```text
common prefix / common context = frequent parent pattern
rare or tail condition = nested specific continuation
```

Use fixed labels only for audit:

```text
common examples C
tail examples R
```

Fit $P_C$ from common examples or known oracle common direction during the
common warmup window. Freeze $P_C$ before tail-learning evaluation.

## Conditions

| Condition | Purpose |
|---|---|
| ordinary AdamW | baseline |
| confidence cap only | tests whether stopping easy common updates is enough |
| projection only | tests whether suppressing $P_Cu_t$ is enough |
| confidence cap + projection | main separate-update implementation |
| random projector | specificity control |
| same-capacity random split | capacity control |
| oracle projector | positive control, if available |

## Primary metric

$$
\Delta \alpha^C_{tail}
=
\alpha^C_{tail}(\text{ordinary})
-
\alpha^C_{tail}(\text{method})
$$

where:

$$
\alpha^C_{tail}
=
\frac{\|P_Cu_{tail}\|^2}{\|u_{tail}\|^2+\epsilon}
$$

## Required guards

| Guard | Required reading |
|---|---|
| tail loss $L_R$ | must improve |
| common loss $L_C$ | must not regress beyond threshold |
| rare accuracy | must not contradict loss gain |
| $G_{mis}$ | should decrease if spectral mechanism is active |
| projector stability | frozen $P_C$ must be meaningful |
| random projector control | must not match main result |
| same-capacity control | must not explain full gain |

## Pass rule

Pass if all hold:

```text
1. alpha_tail_common decreases materially vs ordinary AdamW.
2. confidence+projection beats confidence-only and projection-only on the joint
   mediator + tail-loss criterion.
3. tail loss improves.
4. common loss remains within guard.
5. random projector and same-capacity controls do not explain the result.
```

## Fail rule

Fail if any decisive condition holds:

```text
1. alpha_tail_common does not decrease.
2. tail loss does not improve.
3. common loss regresses materially.
4. random projector gives the same effect.
5. rare accuracy or G_mis contradicts the claimed mechanism.
```

## Expected artifacts

```text
summary.md
detailed.md
tables/update_projection_fraction.csv
tables/loss_guard.csv
tables/spectral_mismatch.csv
tables/projector_stability.csv
figures/alpha_tail_common_over_training.png
figures/tail_loss_vs_update_fraction.png
figures/spectral_mismatch_curve.png
```

## Claim boundary

This protocol can support:

```text
controlled nested separate-update mechanism evidence
```

It cannot support:

```text
real-DCLM utility
semantic experts
deployable MoE
general dense-beating claim
```
