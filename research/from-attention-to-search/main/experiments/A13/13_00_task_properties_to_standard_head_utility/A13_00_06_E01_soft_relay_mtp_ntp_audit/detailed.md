# A13_00_06_E01 Detailed Evidence

## 1. Verdict And Execution Boundary

Verdict: **Insufficient / Stage-0 stop**.

The job completed the registered NTP-only carrier audit and automatically
withheld Stage 1. No shared-aux or informative-MTP model was trained, so no
objective contrast exists to interpret.

- ACP job: `pt-ejtnc54g`;
- hardware: one `n6ls.iu.i40.4` worker, four NVIDIA H100 80GB GPUs;
- Stage-0 wall interval: 2026-07-17 02:03:44--02:05:32 UTC;
- registered seeds: 1801--1808;
- completed Stage-0 runs: \(8\) seeds \(\times 4\) penalties \(=32\);
- completed Stage-1 runs: 0, by gate rather than execution failure.

## 2. Frozen Objects

The sequence and answer remained

```text
[BOS] [FIXED] [A] [B] [RELAY] [ANSWER] [A]
```

with \(Y=A\). Model, data split, optimizer, batch stream, 3,000-step budget, and
answer rule were inherited unchanged from the A13 single-value carrier. The
only varying mask entry in both layers was `ANSWER` query to the \(A\) key:

| Path | Logit penalty | Pre-softmax multiplier |
| --- | ---: | ---: |
| `direct_0` | 0 | 1.000 |
| `soft_2` | 2 | 0.135 |
| `soft_4` | 4 | 0.018 |
| `hard` | \(+\infty\) | 0 |

`ANSWER` otherwise read only `RELAY` and itself. Thus `FIXED` and \(B\) were not
alternate direct paths.

## 3. Carrier Capability And Dynamic Range

Every path reached final mean accuracy 1.0 with 8/8 seeds above 0.90.

| Path | First-90% steps by seed | Within 1,000 | Dynamic-range gate |
| --- | --- | ---: | --- |
| `direct_0` | 20, 20, 20, 20, 20, 20, 20, 20 | 8/8 | **fail: saturated at first positive checkpoint** |
| `soft_2` | 60--280 | 8/8 | pass |
| `soft_4` | 120--460 | 8/8 | pass |
| `hard` | 140--1,480 | 7/8 | pass under registered 7/8 rule |

At step 20, mean answer accuracy was 0.9832 for `direct_0` but only 0.0721,
0.0577, and 0.0577 for `soft_2`, `soft_4`, and `hard`. This is not a common
comparison range at the registered 20-step resolution.

The NTP-only AULC values also show the difficulty gradient:

| Path | Mean AULC | 95% paired-seed bootstrap interval |
| --- | ---: | ---: |
| `direct_0` | 0.0730 | [0.0696, 0.0759] |
| `soft_2` | 0.2570 | [0.1724, 0.3831] |
| `soft_4` | 0.5115 | [0.4000, 0.6557] |
| `hard` | 0.8508 | [0.5794, 1.1847] |

## 4. Measured Causal Path Use

Nominal attention penalty was not treated as mechanism evidence. Two
interventions were evaluated at step 1,000:

1. **Direct deletion:** remove `ANSWER` \(\rightarrow A\) after training and
   measure answer-NLL increase.
2. **Wrong relay donor:** replace the layer-1 relay hidden state with an
   in-distribution different-\(A\) donor and measure answer-NLL increase.

The path means were:

| Path | Direct effect, nats [95% CI] | Relay effect, nats [95% CI] | Relay reliance [95% CI] |
| --- | ---: | ---: | ---: |
| `direct_0` | 9.276 [5.920, 12.660] | 0.000001 [0.000000, 0.000002] | 0.0000002 [0.0000000, 0.0000005] |
| `soft_2` | 6.459 [4.988, 8.060] | 0.000033 [0.000001, 0.000072] | 0.0000058 [0.0000004, 0.0000134] |
| `soft_4` | 4.363 [3.059, 5.694] | 2.728 [0.957, 4.744] | 0.345 [0.141, 0.557] |
| `hard` | 0 | 11.886 [10.988, 12.768] | 1.000 [1.000, 1.000] |

The paired path-rank slopes were:

| Object | Mean slope | 95% bootstrap interval | Directional seeds |
| --- | ---: | ---: | ---: |
| direct deletion effect | -2.9925 | [-4.0176, -2.0588] | 8/8 negative |
| wrong-relay effect | 3.8385 | [3.4287, 4.2367] | 8/8 positive |
| relay reliance | 0.3345 | [0.3136, 0.3556] | 8/8 positive |

Therefore Stage 0 succeeded at producing an ordered *causal* path shift. It
also showed why nominal penalty cannot be the moderator: the shift is strongly
nonlinear, with `soft_2` still almost fully direct and `soft_4` becoming mixed.

## 5. Gate Ledger

| Gate | Result | Meaning |
| --- | --- | --- |
| all paths ultimately learn | pass | no endpoint is structurally impossible |
| direct causal effect decreases | pass | deleting the direct edge matters less as penalty rises |
| relay causal effect increases | pass | the standard head increasingly depends on the patched relay state |
| relay-reliance statistic increases | pass | the two measured path effects shift in the intended direction |
| common non-saturated window | **fail** | `direct_0` is at 98.3% by the first positive checkpoint |
| Stage 1 authorization | **blocked** | objective results must not be generated or read |

The carrier is structurally valid and causally ordered, but not
comparison-ready under the frozen measurement window.

## 6. Why The Missing Stage-1 Objects Cannot Be Inferred

### MTP-specific utility

\(U_r\) is undefined because neither shared-aux nor informative-MTP ran. The
positive A13_00_05 hard-relay result cannot be copied into this graded design.

### Gradient dose

NTP-only answer gradients were recorded, but there was no active auxiliary
loss. Therefore realized shared-aux versus MTP gradient norms, cosines, and
dose-adjusted regressions do not exist.

### Hard-mask difficulty

Difficulty was not excluded. It covaries strongly with measured relay use:
median first-90% step rose from 20 to 310 and NTP AULC rose from 0.0730 to
0.8508 nats. This could mechanically make the easy endpoint's objective gap
near zero and create a spurious positive utility trend.

### Formation, transport, and use

The donor intervention establishes causal ordinary-head use of the layer-1
relay state at the hard endpoint and partial use at `soft_4`. It does not by
itself separate whether an absent relay effect at `direct_0` or `soft_2` comes
from non-formation, failed transport, or a standard head choosing the direct
path.

## 7. Figure Contracts And Visual Audit

### Stage-0 Learning Curves

- question: do all NTP-only path levels learn inside a common resolved window?
- metric/unit: held-out answer NLL in nats and answer accuracy;
- data source: all 32 Stage-0 trajectories, checkpoints every 20 steps;
- aggregation: arithmetic seed mean at each checkpoint;
- axes/legend: optimization step, NLL/accuracy, registered path color;
- allowed conclusion: all paths learn, but `direct_0` saturates at the first
  positive checkpoint and path difficulty increases strongly;
- limitation: it contains no active auxiliary objective.

Rendered artifact:
[stage0_ntp_learning_curves.png](figures/stage0_ntp_learning_curves.png).

### Causal Path Effects

- question: did the nominal penalties produce ordered actual direct and relay
  use?
- metric/unit: intervention-induced answer-NLL increase in nats and dimensionless
  relay reliance;
- data source: step-1,000 direct deletion and wrong-relay donor audits;
- aggregation: arithmetic seed means;
- allowed conclusion: direct use decreases and relay use increases, nonlinearly;
- limitation: two interventions do not establish exhaustive mediation.

Rendered artifact:
[stage0_causal_path_effects.png](figures/stage0_causal_path_effects.png).

Both rendered images were inspected for readable axes, correct condition order,
and consistency with the tables.

## 8. Artifact Map

- [Seed-level Stage-0 summary](tables/stage0_seed_summary.csv)
- [Path-level Stage-0 summary](tables/stage0_path_summary.csv)
- [Seed-level causal slopes](tables/stage0_causal_slopes_by_seed.csv)
- [Frozen gate decision](tables/stage0_decision.json)
- raw worker result directory:
  `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a13_00_06_soft_relay_mtp_ntp_audit/a13_00_06_e01_soft_relay_mtp_ntp_audit_4gpu_20260717_0204`
- raw runtime logs:
  `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/logs/acp/a13_00_06_e01_soft_relay_mtp_ntp_audit_4gpu_20260717_0204`

## 9. Claim Boundary And Exactly One Next Decision

No new MTP-versus-NTP claim is supported. The only update is that the four
penalties produce the required causal path ordering, but the frozen checkpoint
resolution makes the primary objective trend non-identifiable because the
normal direct endpoint saturates immediately.

**Exactly one next decision:** obtain researcher approval for the
measurement-only Stage-0 repair specified in `summary.md`; do not run Stage 1
or alter any path, seed, model, objective, or optimizer object before that
approval.
