# A13_00_03_E02 Detailed Evidence

## 1. Independent Confirmation Contract

E02 retained the E01 task, six objective/path cells, model, optimizer,
3,000-step budget, 1,000-step AULC horizon, and every numerical threshold. It
used new paired seeds 1501--1508 and evaluated donor use only among models at
or above the registered 0.90 per-seed capability threshold.

## 2. Capability Results

| Cell | Mean final accuracy | Seeds \(\ge0.90\) | Verdict |
| --- | ---: | ---: | --- |
| relay NTP | 0.9712 | 7/8 | pass |
| relay shared-aux | 0.8990 | 5/8 | fail |
| relay Next-2 | 1.0000 | 8/8 | pass |
| bypass NTP | 1.0000 | 8/8 | pass |
| bypass shared-aux | 1.0000 | 8/8 | pass |
| bypass Next-2 | 1.0000 | 8/8 | pass |

Shared-aux relay seeds 1502, 1504, and 1508 ended at 0.7692, 0.7308, and
0.7692. This is path-specific: the same objective reached 1.0 in all bypass
seeds.

## 3. Candidate Primary Effects

| Object | Mean | 95% paired bootstrap interval | Positive seeds |
| --- | ---: | ---: | ---: |
| \(U_{\mathrm{relay}}\) | 1.4703 nats | [0.9957, 2.0099] | 8/8 |
| \(U_{\mathrm{bypass}}\) | 0.0802 nats | [0.0236, 0.1721] | 8/8 |
| \(\Delta_{\mathrm{relay}}\) | 1.3901 nats | [0.8996, 1.9553] | 8/8 |

Together with E01, all 16 paired seeds have positive relay utility and
positive relay interaction. This is a stable descriptive pattern, but neither
registered run passes its complete original gate conjunction.

## 4. Causal-Use Results

Every capability-eligible model in all three relay objectives followed a
different-label donor state with accuracy 1.0. The shared-aux causal-use guard
was insufficient only because there were five eligible models, not because
eligible models ignored the relay.

## 5. Why Another Budget/Capacity Sweep Is Not the Next Step

The carrier was independently validated under NTP before objective treatment,
and NTP again passed in E01 and E02. Tuning until shared-aux also passes 7/8
would condition the task definition on the control arm's realized outcome.
That can suppress a genuine harmful interaction between an uninformative
relay target and a relay-required path.

The causal uncertainty is now smaller: only one auxiliary label must be
changed while all other Next-2 targets remain fixed.

## 6. Artifact Map

- [Effects by seed](tables/effects_by_seed.csv)
- [Final metrics](tables/final_metrics.csv)
- [Relay intervention audit](tables/relay_patch_audit.csv)
- [Initial gradient diagnostics](tables/gradient_diagnostics.csv)
- [Learning curves](figures/objective_learning_curves.png)
- [Paired effect figure](figures/relay_interaction.png)
- Raw execution directory:
  `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/outputs/a13_00_03_e02_gate_coherent_confirmation_full_20260716`

Runtime: 608.6 seconds on `cuda:1`.

## 7. Claim Boundary

E02 independently repeats the direction and shows path-specific shared-aux
instability. It does not, under its original contract, establish the parent
mechanism. It motivates the new one-label causal intervention without changing
either prior verdict.
