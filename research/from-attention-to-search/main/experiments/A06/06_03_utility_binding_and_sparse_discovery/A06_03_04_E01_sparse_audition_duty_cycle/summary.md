# A06_03_04_E01 Sparse Audition Duty Cycle: Summary

## What We Established

Fixed low-frequency audition does not preserve reliable rank-4 discovery in the
current full-LM system. Duty cycles from `0` through `1/4` correct `0/128` cells.
At `rho=1/2`, correction reaches only `79/128` (`61.7188%`, seed-clustered 95%
CI `[53.9063%,69.5313%]`). Only continuous audition, `rho=1`, reaches `128/128`.

However, audition is not needed forever. Every cell corrected at `rho=1/2` or
`rho=1` remains corrected after auditions are disabled and 200 ordinary top-1
updates are applied. The result supports a **discover-then-exploit phase
transition**: continuous counterfactual utility is needed before identity is
established; selected-only top-1 reinforces the route after crossing.

## Setup

- A06_03_03_E01 learned specialists with useful expert installed at rank 4.
- Frozen experts and representation; router-only SGD `0.001`; full LM loss.
- Duty cycles `0, 1/16, 1/8, 1/4, 1/2, 1` for 600 discovery updates.
- Then 200 selected-only updates with audition disabled.
- 32 seeds, four tasks per seed; 128 cells per condition.
- Remote four-H100 job `pt-gr8wy1gt` succeeded; all validity guards passed.

## Primary Results

| Duty cycle | Mean active experts | Correction | 95% CI | Retention among corrected | Median final discovery margin |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 1.0000 | 0.0000 | `[0,0]` | n/a | -1.8875 |
| 1/16 | 1.0625 | 0.0000 | `[0,0]` | n/a | -1.7030 |
| 1/8 | 1.1250 | 0.0000 | `[0,0]` | n/a | -1.4525 |
| 1/4 | 1.2500 | 0.0000 | `[0,0]` | n/a | -0.8527 |
| 1/2 | 1.5000 | 0.6172 | `[0.5391,0.6953]` | 1.0000 | +0.6026 |
| 1 | 2.0000 | 1.0000 | `[1,1]` | 1.0000 | +0.7835 |

![Duty-cycle frontier](figures/duty_cycle_frontier.png)

The left panel shows that reliable correction has not been reached at any
subunit tested duty cycle. The right panel shows the corresponding correction
time and regret. This is a training activated-compute frontier, not a measured
wall-clock or communication frontier.

![Margin dynamics and retention](figures/margin_dynamics_and_retention.png)

At `rho<=1/4`, median margin stays negative and decays after audition stops. At
`rho=1/2` and `rho=1`, margin crosses zero and then grows faster under ordinary
top-1 after step 600. Thus top-1 is not globally destructive: it is destructive
from the wrong identity basin and reinforcing inside the useful identity basin.

## Theory Update

The initial stationary-pressure prediction fails quantitatively. Median initial
selected-only pressure is `-2.6052`, audition pressure is `+12.1621`, predicting
`rho_c=0.1802`. Yet no condition through `rho=1/4` corrects any cell, and
`rho=1/2` remains below the reliability threshold. The gradient field changes
with route identity, candidate probability, and accumulated margin; a single
step-0 average pressure cannot predict finite-time discovery.

## Decision

- H1 fixed threshold law: rejected at the preregistered reliability criterion.
- H2 continuous audition required: supported over the tested 600-step horizon.
- H3 rare audition sufficient: rejected.
- The broader state-independent pressure model is weakened by a three-grid
  mismatch between predicted and empirical viable duty cycle.

The next Router should use continuous audition only during discovery and stop
when a label-free utility certificate indicates that the incumbent expert has
become functionally dominant. This targets cumulative extra auditions rather
than lowering a fixed duty cycle everywhere.

## Claim Boundary

The experiment does not prove that every subunit duty cycle fails at arbitrary
horizons, that continuous audition is needed in pretrained LLMs, or that a
label-free stopping certificate already exists. It establishes the tested
fixed-schedule frontier and the post-cross retention asymmetry.
