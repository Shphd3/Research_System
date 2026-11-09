# A13_00_03_E01 Detailed Evidence

## 1. Frozen Comparison

Task:

```text
[BOS] [FIXED] [A] [B] [RELAY] [ANSWER] [A]
```

Paths: two-layer relay-required and two-layer bypass-available.

Objectives: NTP, matched shared-aux, and informative Next-2. Only the ordinary
next-token head was evaluated. Eight paired seeds 1401--1408 trained for
3,000 steps; primary AULC used the frozen 0--1,000-step window.

## 2. Capability

| Cell | Mean final accuracy | Seeds \(\ge0.90\) | Verdict |
| --- | ---: | ---: | --- |
| relay NTP | 0.9712 | 7/8 | pass |
| relay shared-aux | 0.9736 | 7/8 | pass |
| relay Next-2 | 1.0000 | 8/8 | pass |
| bypass NTP | 1.0000 | 8/8 | pass |
| bypass shared-aux | 1.0000 | 8/8 | pass |
| bypass Next-2 | 1.0000 | 8/8 | pass |

## 3. Primary Candidate Effects

For each seed,

\[
U_r=\operatorname{AULC}_{\mathrm{SA},r}
-\operatorname{AULC}_{\mathrm{MTP},r},
\qquad
\Delta_{\mathrm{relay}}=U_{\mathrm{relay}}-U_{\mathrm{bypass}}.
\]

| Object | Mean | 95% paired bootstrap interval | Positive seeds |
| --- | ---: | ---: | ---: |
| \(U_{\mathrm{relay}}\) | 0.7127 nats | [0.4559, 1.0492] | 8/8 |
| \(U_{\mathrm{bypass}}\) | 0.0795 nats | [0.0334, 0.1323] | 8/8 |
| \(\Delta_{\mathrm{relay}}\) | 0.6333 nats | [0.3943, 0.9443] | 8/8 |

Per-seed \(U_{\mathrm{relay}}\) ranged from 0.2642 to 1.7801 nats;
per-seed interactions ranged from 0.2378 to 1.5568 nats. The direction is not
created by a single seed.

## 4. Causal-Use Guard Failure

| Objective | Capability-eligible seeds | Donor follow among eligible | Registered all-seed mean |
| --- | ---: | ---: | ---: |
| NTP | 7/8 | 1.0000 | 0.8846 |
| shared-aux | 7/8 | 1.0000 | 1.0000 |
| Next-2 | 8/8 | 1.0000 | 1.0000 |

The only failing intervention row was NTP seed 1401, whose intact accuracy was
already 0.7692. Including that model in the causal-use average conflicts with
the protocol's separate decision that only seven capability-passing seeds were
required. E01 therefore remains insufficient and triggers a fresh-seed
confirmation with coherent gate composition.

## 5. Gradient Diagnostics

At initialization, auxiliary and answer gradients had small, mixed cosine
similarities for both shared-aux and Next-2. This means the large learning
effect cannot be read directly from initial full-vector cosine. The diagnostic
does not localize which parameter subspace supplies the benefit and is not a
decision metric.

## 6. Artifact Map

- [Effects by seed](tables/effects_by_seed.csv)
- [Final metrics](tables/final_metrics.csv)
- [Relay intervention audit](tables/relay_patch_audit.csv)
- [Initial gradient diagnostics](tables/gradient_diagnostics.csv)
- [Learning curves](figures/objective_learning_curves.png)
- [Paired effect figure](figures/relay_interaction.png)
- Raw execution directory:
  `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/outputs/a13_00_03_e01_relay_necessity_interaction_full_20260716`

Runtime: 614.9 seconds on `cuda:0`.

## 7. Claim Boundary

E01 alone does not pass the parent hypothesis. It supplies an independently
confirmable candidate interaction and identifies a protocol-logic flaw. It
does not establish pure future-information causality, code/language transfer,
long-context value, composition, planning, or MoE utility.
