# A06_03_04_E01 Sparse Audition Duty Cycle: Detailed Record

## Decision

Only `rho=1` meets the preregistered reliability criterion. Fixed sparse
audition is not a viable replacement for continuous discovery-phase audition in
the tested horizon. Corrected routes are fully retained after audition stops.

## Protocol Compliance

| Guard | Result | Status |
| --- | ---: | --- |
| completed seeds | 32 | pass |
| specialist utility gap | `8.894682` | pass |
| generalist absolute gap | `0.004236` | pass |
| minimum installed-rank accuracy | `1.0` | pass |
| minimum adjacent score gap p05 | `0.473113` | pass |
| initial load spread | `0` | pass |
| maximum audition-count error | `0.5` | pass |
| maximum challenger phase-count spread | `1` | pass |
| rho=0 blind-basin reproduction | `0/128` | pass |
| rho=1 A06_03_03_E01 reproduction | `128/128` | pass |
| generalist arbitrary-target guards | `0/128` at rho 1/8 and 1 | pass |
| ACP job | `pt-gr8wy1gt`, `SUCCEEDED` | pass |

## Exact Construction

Each condition starts from the same learned-specialist rank-4 router. At
discovery update \(t\), a rational accumulator decides whether to audition. If
yes, the Router executes current top-1 and one rotating challenger; otherwise
it executes weighted top-1. Challenger phase advances only on audition events,
so the three alternatives differ by at most one evaluation. All conditions use
the same full LM loss.

After 600 discovery updates, audition is disabled for every condition. Training
continues for 200 selected-only updates. Correction requires useful-route
accuracy at least `0.95` for five consecutive discovery checkpoints. Retention
requires final step-800 route accuracy at least `0.95` among corrected cells.

## Full Results

| rho | Correction | CI95 | Median capped time | Median regret | Margin at 600 | Retention | Margin at 800 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0.0000 | `[0,0]` | 601 | 1.0200 | -1.8875 | n/a | -1.8952 |
| 0.0625 | 0.0000 | `[0,0]` | 601 | 1.0131 | -1.7030 | n/a | -1.7674 |
| 0.125 | 0.0000 | `[0,0]` | 601 | 1.0058 | -1.4525 | n/a | -1.6108 |
| 0.25 | 0.0000 | `[0,0]` | 601 | 0.9949 | -0.8527 | n/a | -1.2609 |
| 0.5 | 0.6172 | `[0.5391,0.6953]` | 556 | 0.8553 | +0.6026 | 1.0000 | +1.3927 |
| 1 | 1.0000 | `[1,1]` | 192.5 | 0.3791 | +0.7835 | 1.0000 | +1.6144 |

Generalist controls remain at zero arbitrary-target correction. Their loss and
margin movement cannot be interpreted as specialization because forced-expert
utility gaps remain approximately zero.

## Visualization Results

### Compute/Correction Frontier

![Duty-cycle frontier](figures/duty_cycle_frontier.png)

- Question: does lowering mean activated experts preserve reliable discovery?
- Result: no tested subunit duty cycle reaches 90%; rho 1/2 is partial.
- Limitation: activated expert count is not measured wall-clock or communication.

### State-Dependent Margin Dynamics

![Margin dynamics](figures/margin_dynamics_and_retention.png)

- Question: what happens after audition stops?
- Result: negative-margin conditions decay; corrected positive-margin conditions
  continue to strengthen under top-1.
- Take-home: selected-only dynamics change sign across the identity boundary.
- Limitation: the plot aggregates over tasks; event-level stopping rules still
  require a label-free observable.

## Failure Of The Stationary Pressure Model

The preregistered local model was

\[
\mathbb E[\Delta m(\rho)]
=\eta[\rho P_A+(1-\rho)P_S].
\]

At step 0, median \(P_S=-2.6052\), \(P_A=12.1621\), and predicted
\(\rho_c=0.1802\). The closest tested grid point is `0.125` or `0.25`, but both
have zero correction. The empirical viable point is `1.0`, three grid indices
away. The local model misses at least three effects:

1. audition pressure changes as candidate probabilities and selected identity
   change;
2. positive average drift need not be large enough to cross every task's finite
   barrier within 600 updates;
3. intermittent selected-only updates can undo audition progress before the
   useful identity becomes self-reinforcing.

The refined model requires state \(m\) and incumbent identity \(r\):

\[
\mathbb E[\Delta m_t]
=\rho_tP_A(m_t,r_t)+(1-\rho_t)P_S(m_t,r_t).
\]

The observed sign asymmetry suggests a phase-adaptive policy: keep \(\rho_t=1\)
until a functional certificate indicates that the incumbent is useful, then set
\(\rho_t=0\).

## Claim Boundary

Supported: continuous audition is required for the preregistered reliability
criterion within the tested 600-step frozen-specialist system; corrected routes
are retained for 200 selected-only updates.

Not supported: universal continuous-audition necessity, a deployable stopping
certificate, joint-training preservation, pretrained LLM transfer, or systems
efficiency.

## Artifact Map

- Anchor: `main/problem_anchors/06_geometry_proxy_preservation/06_03_utility_binding_and_sparse_discovery/06_03_utility_binding_and_sparse_discovery_anchor.md`
- Protocol: `main/experiments/A06/06_03_utility_binding_and_sparse_discovery/A06_03_04_E01_sparse_audition_duty_cycle/protocol.md`
- Runner: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a06_43_sparse_audition_duty_cycle.py`
- Config: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a06_43_sparse_audition_duty_cycle.json`
- Raw result: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a06_43_sparse_audition_duty_cycle/a06_43_full_4gpu_20260711_01/`
- Curated figures: `figures/duty_cycle_frontier.png`, `figures/margin_dynamics_and_retention.png`
- Curated table: `tables/condition_summary.csv`
- Job: `pt-gr8wy1gt`
