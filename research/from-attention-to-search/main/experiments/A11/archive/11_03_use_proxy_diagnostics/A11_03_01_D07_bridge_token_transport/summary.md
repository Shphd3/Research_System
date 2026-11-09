# A11_19 Bridge-Token-Conditioned Transport: Summary

## Conclusion

The preregistered decision is **insufficient**, because the step-20 central-difference sign guard passed all four bridges in only `3/5` seeds rather than the required `4/5`. The failure is localized to three near-zero first-order predictions, while all restore, curve, and A11_18 reproduction guards pass.

The trajectory evidence nevertheless strongly rejects a bridge-independent interpretation. Over updates `20-200`, normalized usefulness has positive AUC in `0/5` seeds for `Decision`, `0/5` for `Answer`, `4/5` for `Therefore`, and `4/5` for `:`. Cross-position semantic transport is therefore strongly **bridge-token conditioned**, but this is a descriptive mechanism result rather than a formally supported preregistered verdict.

## Terminology And Metric

For a fixed extra H2 loss gradient $g_D^S$ and a standard H1 semantic margin measured one position later after bridge token $b$, define

$$
\widehat U_b(t)
=-
\frac{\langle \nabla_{\theta_S}M_{1,T+1}^{(b)}(t),g_D^S(t)\rangle}
{\|\nabla_{\theta_S}M_{1,T+1}^{(b)}(t)\|\,\|g_D^S(t)\|}.
$$

- $\widehat U_b>0$: an infinitesimal H2-loss descent step increases the later H1 semantic margin under bridge $b$.
- AUC over `20-200`: average post-burn-in direction across the training trajectory; positive AUC is the primary per-seed judgment.
- This metric measures local shared-parameter alignment. It does not by itself prove a finite-step downstream accuracy gain.

## Exact Setup

The experiment reuses the five pretrained NTP trajectories from A11_18. Prompt, examples, checkpoints, H2 gradient, H1 readout, and the one-position distance are fixed. Only the diagnostic teacher-forced bridge token is changed among `Decision`, `Answer`, `Therefore`, and `:`. Alternative bridges are not trained conditions.

## Primary Evidence

| Bridge | Positive AUC seeds | Mean final $\widehat U_b$ | Interpretation |
|---|---:|---:|---|
| `Decision` | 0/5 | -0.289 | consistently adverse after burn-in |
| `Answer` | 0/5 | -0.189 | consistently adverse after burn-in |
| `Therefore` | 4/5 | +0.098 | usually favorable |
| `:` | 4/5 | +0.224 | usually favorable |

![Bridge-conditioned transport](figures/a11_19_bridge_token_conditioned_transport.png)

The left panel shows the seed-mean trajectory; the right panel gives the primary positive-AUC count. The figure tests whether changing only the bridge token changes transport sign. It supports token-conditioned transport, but covers only four one-token counterfactual transitions.

## Validity Audit

- all implementation and restore guards: pass;
- original `Decision` reproduction versus A11_18: pass, maximum difference `4.20e-05`;
- all-four-cell step-20 central-sign guard: `3/5`, preregistered threshold `4/5`;
- failing cells: seed 974 `Decision`, seed 974 `Therefore`, and seed 975 `Therefore`;
- the corresponding normalized first-order predictions are `-7.4e-05`, `1.36e-03`, and `1.88e-02`, so the failure is concentrated near zero rather than in the large-magnitude trajectory effects.

## Claim Boundary And Decision

Supported descriptively: the intervening token/state transition can reverse the sign of one-position semantic transport.

Not supported: every natural bridge has this pattern; MTP therefore improves generation; or the preregistered token-conditioned hypothesis formally passes.

Next decision: close this local mechanism phase. The theory should retain bridge-conditioned cross-position transport as an explicit condition, while any further claim of MTP superiority must be tested on a downstream task where the bridge/generation policy is part of the trained system.
