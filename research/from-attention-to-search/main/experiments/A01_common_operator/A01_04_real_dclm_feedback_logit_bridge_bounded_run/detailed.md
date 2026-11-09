# Detailed Record: A01_04 Real-DCLM Feedback Logit Bridge Bounded Run

## 1. Result

The bounded real-DCLM gate-logit bridge is a negative result for the simple
low-rank feedback-logit common hypothesis.

The run recovered real gate-logit artifacts from a raw-center A06-style
training run and reproduced the proxy-route collapse. But rank-1 feedback-logit
replay did not explain enough of the collapse, and rank-1 feedback-logit
removal did not rescue routing.

Primary pass result:

```json
{
  "pass": false,
  "total_cells": 18,
  "denominator_valid_cells": 18,
  "mean_explain_valid": 0.42301904760573794,
  "mean_rescue_valid": 0.16248624510051982,
  "mean_random_explain_valid": 0.33547826373608225,
  "mean_random_rescue_valid": 0.11774766188140123
}
```

## 2. Protocol Alignment

Primary anchor:
`Projects/from-attention-to-search/main/problem_anchors/01_common_operator_mechanism/01_04_feedback_common_preservation_bridge_anchor.md`

Protocol:
`Projects/from-attention-to-search/main/experiments/A01_common_operator/A01_04_real_dclm_feedback_logit_bridge_bounded_run/protocol.md`

Run directory:
`runs/real_dclm_logit_bridge_20260629_full01`

Experiment role: real-data bridge audit.

Claim boundary: gate-logit drift bridge only.

## 3. Reproduction

Working directory:

```bash
/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A01_common_operator/A01_04_real_dclm_feedback_logit_bridge_bounded_run
```

Environment:

```bash
/root/anaconda3/envs/spectral-hier/bin/python
```

Command:

```bash
/root/anaconda3/envs/spectral-hier/bin/python scripts/run_real_dclm_feedback_logit_bridge.py --run-name real_dclm_logit_bridge_20260629_full01
```

Rank sweep command:

```bash
/root/anaconda3/envs/spectral-hier/bin/python scripts/reanalyze_real_feedback_logit_artifacts.py --run-dir runs/real_dclm_logit_bridge_20260629_full01 --ranks 1 2 3 4 5 6 7
```

## 4. Data / Model / Captured Artifacts

Data: DCLM-bin under `/data/share/109_cache_dir/hf_data/dclm_bin`.

Model: 6-layer Qwen3-MoE toy model from `/data/250010109/MoE_Router`.

Variant: raw-center router initialization.

Seeds: 0, 1, 2.

Layers: 3, 4, 5.

Checkpoints: 0, 5, 10.

Captured artifact:

\[
z_{\ell,t}=W_{\ell,t}h_{\ell,t}
\]

Artifact files:

```text
runs/real_dclm_logit_bridge_20260629_full01/artifacts/gate_logits/seed_*/step_*/layer_*_gate_logits.npz
```

Each artifact stores gate logits, fixed proxy labels, token ids, and positions.

## 5. Metrics

Primary metric:

\[
\mathrm{drop\_explained}=
\frac{\mathrm{NMI}(z_0)-\mathrm{NMI}(z_0+P_{\mathrm{fb}}\Delta z_t)}
{\mathrm{NMI}(z_0)-\mathrm{NMI}(z_t)+\epsilon}
\]

Rescue metric:

\[
\mathrm{rescue}=
\frac{\mathrm{NMI}(z_0+(I-P_{\mathrm{fb}})\Delta z_t)-\mathrm{NMI}(z_t)}
{\mathrm{NMI}(z_0)-\mathrm{NMI}(z_t)+\epsilon}
\]

Denominator-valid cells require full NMI drop at least 0.05.

## 6. Main Aggregate Results

| Step | Cells | Valid cells | Step0 NMI | Full NMI | Feedback-only NMI | Residual-only NMI | Full drop | Explain | Rescue | Random explain |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 5 | 9 | 9 | 0.7549 | 0.0410 | 0.4327 | 0.1933 | 0.7139 | 0.4423 | 0.2105 | 0.3344 |
| 10 | 9 | 9 | 0.7549 | 0.0131 | 0.4509 | 0.0982 | 0.7418 | 0.4037 | 0.1145 | 0.3365 |

Per-cell result table:
`runs/real_dclm_logit_bridge_20260629_full01/tables/real_feedback_logit_bridge_scores.csv`

## 7. Rank Sweep

| Rank | Valid cells | Explain | Rescue | Random explain | Random rescue | Pass |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 18 | 0.4230 | 0.1625 | 0.2852 | 0.0995 | false |
| 2 | 18 | 0.6341 | 0.2793 | 0.4915 | 0.1494 | false |
| 3 | 18 | 0.7526 | 0.4177 | 0.5985 | 0.2418 | false |
| 4 | 18 | 0.8565 | 0.5375 | 0.7056 | 0.3387 | false |
| 5 | 18 | 0.9168 | 0.6362 | 0.7732 | 0.3889 | false |
| 6 | 18 | 0.9582 | 0.7465 | 0.8446 | 0.5037 | false |
| 7 | 18 | 0.9845 | 0.8640 | 0.9251 | 0.6801 | false |

Interpretation: higher ranks reconstruct more of the collapse, but random
subspaces also reconstruct much of it. The effect is not specific enough to
support a low-rank feedback-logit common operator.

## 8. Visualization Results

### Figure 1: Real-DCLM Logit Bridge NMI

![Real-DCLM logit bridge NMI](runs/real_dclm_logit_bridge_20260629_full01/figures/real_feedback_logit_bridge_nmi_by_step.png)

Question answered: Does full logit drift reproduce collapse, and do rank-1
feedback replay/removal explain or rescue it?

Metric definition: proxy-route NMI under step0, full, feedback-only, and
residual-only logit states.

Data source:
`runs/real_dclm_logit_bridge_20260629_full01/tables/real_feedback_logit_bridge_by_step.csv`

Observed result: full drift collapses NMI; rank-1 feedback-only replay explains
only part of the drop; residual-only removal remains low.

Take-home: recovered real logit drift reproduces collapse, but rank-1 feedback
common does not rescue it.

### Figure 2: Explanation And Rescue

![Real-DCLM logit bridge explanation and rescue](runs/real_dclm_logit_bridge_20260629_full01/figures/real_feedback_logit_bridge_explain_rescue.png)

Question answered: Does the rank-1 feedback-logit projector pass the bridge
threshold?

Metric definition: fraction of full NMI drop explained or rescued.

Observed result: explanation is below 0.5 and rescue is far below 0.5.

Take-home: rank-1 feedback-logit common is insufficient.

### Figure 3: Rank Sweep

![Real-DCLM feedback logit rank sweep](runs/real_dclm_logit_bridge_20260629_full01/figures/real_feedback_logit_rank_sweep.png)

Question answered: Is failure only due to using rank 1?

Metric definition: explanation/rescue fractions for ranks 1-7.

Observed result: higher ranks improve explanation/rescue, but random subspaces
also improve substantially.

Take-home: real collapse appears distributed across logit dimensions or mixed
with non-common drift; high-rank reconstruction is not a specific common
mechanism.

## 9. Rival Explanations

R1: Collapse is not visible in gate logits.

Status: weakened. Full logit drift reproduces the collapse.

R2: Collapse is distributed across residual logit drift rather than common
logit drift.

Status: supported relative to the low-rank common hypothesis. Residual-only
removal does not rescue at rank 1, and high-rank behavior is not specific.

R3: Top logit-drift subspace is no better than random.

Status: partly supported. Top drift is better than random at low rank, but the
margin is too small for the pass rule and shrinks in interpretability at high
rank.

R4: Step-0 proxy labels are not stable enough.

Status: weakened. Step0 NMI is 0.7549 on average, matching the known A06
aligned proxy surface.

## 10. Artifact Map

| Artifact | Path |
|---|---|
| protocol | `protocol.md` |
| runner | `scripts/run_real_dclm_feedback_logit_bridge.py` |
| rank sweep script | `scripts/reanalyze_real_feedback_logit_artifacts.py` |
| run directory | `runs/real_dclm_logit_bridge_20260629_full01` |
| source manifest | `runs/real_dclm_logit_bridge_20260629_full01/config/source_manifest.json` |
| run config | `runs/real_dclm_logit_bridge_20260629_full01/config/run_config.json` |
| gate-logit artifacts | `runs/real_dclm_logit_bridge_20260629_full01/artifacts/gate_logits/` |
| per-cell score table | `runs/real_dclm_logit_bridge_20260629_full01/tables/real_feedback_logit_bridge_scores.csv` |
| by-step summary | `runs/real_dclm_logit_bridge_20260629_full01/tables/real_feedback_logit_bridge_by_step.csv` |
| pass summary | `runs/real_dclm_logit_bridge_20260629_full01/tables/real_feedback_logit_bridge_summary.json` |
| rank sweep table | `runs/real_dclm_logit_bridge_20260629_full01/tables/real_feedback_logit_rank_sweep_summary.csv` |
| NMI figure | `runs/real_dclm_logit_bridge_20260629_full01/figures/real_feedback_logit_bridge_nmi_by_step.png` |
| explanation/rescue figure | `runs/real_dclm_logit_bridge_20260629_full01/figures/real_feedback_logit_bridge_explain_rescue.png` |
| rank sweep figure | `runs/real_dclm_logit_bridge_20260629_full01/figures/real_feedback_logit_rank_sweep.png` |

## 11. Claim Boundary

Can claim:

- real gate-logit drift artifacts were recovered;
- full real logit drift reproduces the A06 proxy-route collapse;
- low-rank feedback-logit common is insufficient as the main explanation or
  rescue target.

Cannot claim:

- hidden-state feedback common is false;
- gate-weight drift and hidden-state drift have been separated;
- expert feedback or optimizer geometry has been ruled out;
- any anti-feedback method will or will not work.

## 12. Next Decision

The next test should decompose:

```text
z_t - z_0 = W_t h_t - W_0 h_0
```

into:

```text
(W_t-W_0)h_0
W_0(h_t-h_0)
(W_t-W_0)(h_t-h_0)
```

This separates gate-weight drift from hidden-state drift. Without that
decomposition, a method that removes low-rank logit common is not justified.

