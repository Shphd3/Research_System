# Detailed Record: A01_04 Feedback Common Preservation Bridge Controlled Full Run

## 1. Result

The controlled run supports the feedback-common preservation bridge. In the
two main feedback regimes, feedback-common replay reproduces proxy-route
collapse and feedback-common removal rescues routing.

Primary result:

```text
pass = true
n_passed_main_feedback_regimes = 2 / 2
controls_ok = true
```

Interpretation: a shared feedback drift can causally overwrite a valid step-0
proxy partition in the controlled model.

Boundary: this is controlled evidence only. Real-DCLM feedback causality still
requires hidden/checkpoint drift tensors.

## 2. Protocol Alignment

Primary anchor:
`Projects/from-attention-to-search/main/problem_anchors/01_common_operator_mechanism/01_04_feedback_common_preservation_bridge_anchor.md`

Protocol:
`Projects/from-attention-to-search/main/experiments/A01_common_operator/A01_04_feedback_common_preservation_bridge_controlled_full_run/protocol.md`

Approval status: user requested execution on 2026-06-29.

Experiment role: root-cause / bridge audit.

Claim boundary: controlled feedback bridge only.

## 3. Reproduction

Working directory:

```bash
/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A01_common_operator/A01_04_feedback_common_preservation_bridge_controlled_full_run
```

Command:

```bash
python scripts/run_feedback_bridge_controlled_full_run.py --outdir .
```

Runtime: local CPU run; no cluster job id.

## 4. Data Generation

Step-0 hidden states are generated around group centers so a linear router can
recover the proxy labels. One router row also has a common-margin direction.

Feedback drift moves all examples along the common-margin direction:

\[
\Delta h_{\mathrm{fb}}\propto v_{\mathrm{common}}
\]

Residual drift moves examples along group-specific directions. Nuisance drift
is activation movement that is not aligned to the router common-margin channel.

The feedback projector is estimated from the drift second moment:

\[
P_{\mathrm{fb}}=\mathrm{TopEig}(\Delta h^\top \Delta h)
\]

## 5. Configuration

| Item | Value |
|---|---|
| hidden dimension | 32 |
| groups / experts | 8 |
| samples per group | 600 |
| seeds | 0-19 |
| center strength | 2.5 |
| common gate strength | 2.2 |
| step-0 noise | 0.25 |
| regimes | common_feedback, mixed_feedback_residual, residual_drift_control, nuisance_drift_control, weak_feedback |

Full configuration is stored in `tables/run_config.json`.

## 6. Metrics

Proxy-route NMI measures agreement between route assignments and proxy labels.

Primary metric:

\[
\mathrm{drop\_explained}=
\frac{\mathrm{NMI}_0-\mathrm{NMI}_{\mathrm{feedback\ only}}}
{\mathrm{NMI}_0-\mathrm{NMI}_{\mathrm{full}}+\epsilon}
\]

Rescue metric:

\[
\mathrm{rescue}=
\frac{\mathrm{NMI}_{\mathrm{residual\ only}}-\mathrm{NMI}_{\mathrm{full}}}
{\mathrm{NMI}_0-\mathrm{NMI}_{\mathrm{full}}+\epsilon}
\]

Guard metrics:

- `route_max_load`;
- random-projector explanation;
- random-projector removal rescue;
- `denominator_valid`, which is true only when the full NMI drop is at least
  0.05.

## 7. Aggregate Results

| Regime | Step0 NMI | Full NMI | Feedback-only NMI | Residual-only NMI | Full drop | Explain | Rescue | Denominator valid | Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| common_feedback | 1.0000 | 0.0205 | 0.0205 | 1.0000 | 0.9795 | 1.0000 | 1.0000 | 1.0 | pass |
| mixed_feedback_residual | 1.0000 | 0.1440 | 0.1028 | 1.0000 | 0.8560 | 1.0509 | 1.0000 | 1.0 | pass |
| residual_drift_control | 1.0000 | 0.9996 | 1.0000 | 0.9998 | 0.0004 | 0.0000 | 0.0002 | 0.0 | control ok |
| nuisance_drift_control | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0 | control ok |
| weak_feedback | 1.0000 | 0.9602 | 0.9650 | 1.0000 | 0.0398 | 0.1074 | 0.1343 | 0.1 | sensitivity only |

Random controls do not match feedback-common explanation in the main feedback
regimes. In small-denominator controls, fraction metrics are not interpreted as
evidence.

## 8. Visualization Results

### Figure 1: Proxy-Route NMI By Condition

![Proxy-route NMI by condition](figures/feedback_bridge_nmi_by_condition.png)

Question answered: Does feedback-common replay reproduce collapse, and does
feedback-common removal rescue routing?

Metric definition: NMI between proxy labels and router assignments.

Data source: `tables/feedback_bridge_intervention_nmi.csv`.

Aggregation level: mean and standard deviation over 20 seeds.

How to read: high `step0` means valid proxy routing; low `full_drift` means
collapse; low `feedback_only` means feedback replay explains collapse; high
`residual_only` means removing feedback rescues routing.

Observed result: common and mixed feedback regimes show the expected
collapse/replay/rescue pattern. Residual and nuisance controls do not collapse.

Take-home: feedback-common drift is sufficient for controlled proxy overwrite.

Limitation: controlled hidden states are not real DCLM hidden states.

### Figure 2: Feedback Explanation And Rescue

![Feedback explanation and rescue](figures/feedback_explain_rescue_by_regime.png)

Question answered: How much full-drift NMI drop is explained or rescued by
feedback common?

Metric definition: drop-explained and rescue fractions relative to full NMI
drop.

Data source: `tables/feedback_bridge_summary.csv`.

How to read: values above 0.75 pass in main feedback regimes; controls should
stay low or have invalid denominator.

Observed result: main feedback regimes pass. Controls stay low. Weak feedback
has a small denominator and is treated as sensitivity evidence only.

Take-home: feedback-common replay/removal is a valid controlled bridge.

Limitation: explanation fractions above 1 can occur when residual drift partly
counteracts common-feedback collapse.

### Figure 3: Route Max Load

![Route max load by condition](figures/feedback_bridge_max_load_by_condition.png)

Question answered: Is the NMI collapse associated with top-1 load collapse?

Metric definition: maximum fraction of samples assigned to one expert.

Data source: `tables/feedback_bridge_scores.csv`.

How to read: high max load indicates collapse into one expert.

Observed result: full and feedback-only drift create high max load in feedback
regimes; residual-only drift restores balanced load.

Take-home: feedback common acts through a common-margin collapse channel in
this controlled setup.

Limitation: balanced load is a guard only; it does not prove utility.

## 9. Rival Explanations

R1: Proxy labels or step-0 router are invalid.

Status: weakened in controlled run. Step0 NMI is 1.0 in all regimes.

R2: Collapse is caused by group-specific residual drift.

Status: weakened. Residual drift control does not collapse, and residual-only
replay rescues feedback regimes.

R3: Collapse is caused by activation nuisance drift.

Status: weakened. Nuisance drift control does not collapse.

R4: Feedback projector is no better than random.

Status: weakened. Random feedback replay does not explain main feedback
collapse, while estimated feedback common does.

## 10. Real-DCLM Artifact Audit

Local inspection of `A06_01_04_E03/E04` found:

- trajectory metrics;
- summaries and detailed records;
- figures;
- logs;
- partial JSONL records with route metrics by step, layer, seed, and variant.

Local inspection did not find:

- hidden-state tensors for \(h_0\) and \(h_t\);
- checkpoint-aligned gate-input tensors;
- saved \(\Delta h_t=h_t-h_0\) tensors;
- artifacts sufficient to replay or remove \(P_{\mathrm{fb}}\Delta h_t\).

Therefore the real-DCLM feedback bridge cannot be claimed complete from the
current local artifacts.

## 11. Stage-Level Evidence

Generation: complete. Step0 proxy routing is valid with NMI 1.0.

Drift: complete. Full drift collapses in feedback regimes and not in negative
controls.

Estimator: complete. Estimated feedback projector aligns with the controlled
common direction in feedback regimes.

Aggregation: complete. Main feedback regimes pass the explanation/rescue rule.

## 12. Artifact Map

| Artifact | Path |
|---|---|
| runner | `scripts/run_feedback_bridge_controlled_full_run.py` |
| protocol | `protocol.md` |
| Chinese protocol companion | `protocol_cn.md` |
| summary | `summary.md` |
| detailed record | `detailed.md` |
| run config | `tables/run_config.json` |
| per-seed scores | `tables/feedback_bridge_scores.csv` |
| aggregate summary | `tables/feedback_bridge_summary.csv` |
| intervention NMI | `tables/feedback_bridge_intervention_nmi.csv` |
| pass summary | `tables/feedback_bridge_winner_summary.json` |
| NMI figure | `figures/feedback_bridge_nmi_by_condition.png` |
| explanation/rescue figure | `figures/feedback_explain_rescue_by_regime.png` |
| max-load figure | `figures/feedback_bridge_max_load_by_condition.png` |

## 13. Claim Boundary

Can claim: feedback-common replay/removal is a controlled mechanism for
proxy-route collapse and rescue.

Cannot claim: real-DCLM feedback causality, real preservation rescue,
anti-feedback method success, or utility.

## 14. Next Decision

Recover or regenerate real-DCLM hidden/checkpoint drift artifacts for step 0,
step 5, and step 10, then run the same replay/removal design on real proxy
labels.
