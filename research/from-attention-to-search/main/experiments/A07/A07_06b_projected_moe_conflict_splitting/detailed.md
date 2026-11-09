# Detailed: A07_06b Projected MoE Conflict Splitting

Primary anchor:
`../../../problem_anchors/07_features_overlap/07_06_projected_common_rare_conflict_splitting_anchor.md`

Protocol: `protocol.md`

## Protocol Compliance Audit

The run executed the approved 4GPU audit with the requested requirements:

- frequent common-update dilution was represented through a common confidence
  gate in the projected-update condition;
- both common and conflict projected router variants were included;
- both raw-gradient and AdamW-like conflict projector diagnostics were
  measured;
- dense shared was included as a required strong boundary.

The run is protocol-compliant as a controlled-surface audit. It is not a
real-DCLM utility test.

## Setup

Code workspace:
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding`

Runner:
`scripts/run_a07_06_conflict_projected_moe_audit.py`

Submitter:
`scripts/submit_a07_06_conflict_projected_moe_4gpu_acp.sh`

Config:
`configs/a07_06_conflict_projected_moe_audit.json`

Run name: `a07_06_conflict_projected_moe_full_20260628_1`

ACP job: `pt-gwnh6l71`

Result dir:
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a07_06_conflict_projected_moe_audit/a07_06_conflict_projected_moe_full_20260628_1`

Curated dir:
`/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A07/A07_06b_projected_moe_conflict_splitting`

Logs:

- `logs/acp/a07_06_conflict_projected_moe_full_20260628_1_submit_20260628_081203.log`
- `logs/acp/a07_06_conflict_projected_moe_full_20260628_1_shard0_runtime_20260628_081327.log`
- `logs/acp/a07_06_conflict_projected_moe_full_20260628_1_shard1_runtime_20260628_081327.log`
- `logs/acp/a07_06_conflict_projected_moe_full_20260628_1_shard2_runtime_20260628_081327.log`
- `logs/acp/a07_06_conflict_projected_moe_full_20260628_1_shard3_runtime_20260628_081327.log`
- `logs/acp/a07_06_conflict_projected_moe_full_20260628_1_aggregate_runtime_20260628_081343.log`

## Conditions

| Condition | Role |
| --- | --- |
| `dense_shared` | dense rare-loss boundary |
| `random_top1_moe` | ordinary top-1 MoE baseline |
| `centered_unsup_split_moe` | prior weak split baseline |
| `common_projected_router_moe` | coarse common projection control |
| `conflict_projected_router_moe` | conflict router projection only |
| `conflict_projected_router_update_moe` | full method: conflict router + projected AdamW-style update + common confidence gate |
| `oracle_split_moe` | positive-control solvability guard |

## Metrics

Primary metric:

\[
\mathcal{C}_{C,R}=\sum_e q_{C,e}q_{R,e}[-\cos(g_{C,e},g_{R,e})]_+.
\]

Primary guard: rare loss \(L_R\).

Strong boundary: full method must beat or close dense shared rare loss.

Diagnostic gate:

\[
\alpha_R^{\mathrm{conflict}}=
\frac{\|P_{\mathrm{conflict}}u_R\|^2}{\|u_R\|^2+\epsilon}.
\]

## Results

### Decision Summary

| Field | Value |
| --- | ---: |
| rare conflict fraction, raw | `0.7934` |
| rare conflict fraction, AdamW-like | `0.1690` |
| raw control ratio | `7.8535` |
| raw projector stability | `0.3309` |
| AdamW-like projector stability | `0.7327` |
| \(\Delta\mathcal{C}\) vs random | `0.0036` |
| \(\Delta\mathcal{C}\) vs centered | `0.0010` |
| rare-loss improvement vs random | `0.2848` |
| rare-loss improvement vs centered | `0.2155` |
| rare-loss margin vs dense | `-0.1538` |
| common-loss regression vs random | `0.0292` |

Automated decision: `weakened_or_insufficient`.

### Loss Table

| Condition | Rare loss | Common loss | Rare acc | Rare margin vs dense |
| --- | ---: | ---: | ---: | ---: |
| dense_shared | `1.7105` | `0.1069` | `0.1493` | `0.0000` |
| random_top1_moe | `1.8415` | `0.1117` | `0.1586` | `0.1310` |
| centered_unsup_split_moe | `1.7722` | `0.1109` | `0.1617` | `0.0617` |
| common_projected_router_moe | `1.7637` | `0.1132` | `0.1653` | `0.0532` |
| conflict_projected_router_moe | `1.7637` | `0.1132` | `0.1653` | `0.0532` |
| conflict_projected_router_update_moe | `1.5567` | `0.1409` | `0.1306` | `-0.1538` |
| oracle_split_moe | `0.0005` | `0.0004` | `1.0000` | `-1.7100` |

Interpretation: the full method improves rare loss and beats dense rare loss,
but rare accuracy is lower. This is a metric mismatch: the run supports a rare
loss improvement, not a rare classification-quality closure.

### Conflict Table

| Condition | Weighted conflict | Delta vs random | Delta vs centered |
| --- | ---: | ---: | ---: |
| dense_shared | `0.9979` | `-0.7571` | `-0.7597` |
| random_top1_moe | `0.2409` | `0.0000` | `-0.0026` |
| centered_unsup_split_moe | `0.2382` | `0.0026` | `0.0000` |
| common_projected_router_moe | `0.2369` | `0.0040` | `0.0013` |
| conflict_projected_router_moe | `0.2369` | `0.0040` | `0.0013` |
| conflict_projected_router_update_moe | `0.2372` | `0.0036` | `0.0010` |
| oracle_split_moe | `0.0000` | `0.2409` | `0.2382` |

Interpretation: route-level conflict barely moved. This weakens the intended
mechanism even though rare loss improved.

### Projector Diagnostic

Raw rare conflict fraction is high (`0.7934`) and above random controls
(`raw_control_ratio = 7.8535`), but raw projector stability is below threshold
(`0.3309`). AdamW-like projector stability is better (`0.7327`), but the rare
fraction is much smaller (`0.1690`).

Interpretation: there is a projection signal, but the stable object is not yet
cleanly identified.

### Update Suppression

The full method reduced selected update projection fraction:

| Step | Pre | Post | Delta |
| ---: | ---: | ---: | ---: |
| `0` | `0.3760` | `0.1111` | `0.2649` |
| `519` | `0.2661` | `0.0739` | `0.1922` |

Interpretation: the implementation did suppress the intended update component.
The unresolved question is whether that component is the causal reason for the
rare-loss gain.

## Visualization Results

### Conflict Versus Rare Loss

![Conflict versus rare loss](figures/conflict_vs_rare_loss.png)

Purpose: test whether the method moves both the mechanism metric and the rare
loss guard.

Setup: aggregate over 8 seeds and plot each condition by weighted conflict and
rare loss.

How to read: lower-left is better.

Observed result: full projected update has the lowest non-oracle rare loss but
does not materially reduce route-level conflict.

Take-home: rare loss improved without closing the mechanism chain.

Remaining uncertainty: the gain may come from confidence gating, update
regularization, or another optimization effect rather than conflict splitting.

### Update Projection Fraction

![Update projection fraction](figures/update_projection_fraction.png)

Purpose: test whether rare updates have mass in the proposed conflict
projector.

Setup: compare raw conflict, AdamW-like conflict, and random-control projection
fractions.

How to read: conflict bars should exceed random controls and be stable.

Observed result: raw mass is high, AdamW-like mass is modest, and only the
AdamW-like stability guard is strong.

Take-home: the diagnostic is suggestive but not clean enough for a mechanism
claim.

Remaining uncertainty: the correct frozen object may be optimizer-space rather
than raw-gradient space.

## Failure Decomposition

**Mechanism failure:** \(\Delta\mathcal{C}_{C,R}\) is too small. The method did
not demonstrate route-level conflict separation.

**Diagnostic weakness:** raw projector stability failed. A frozen raw conflict
projector is not justified by this run.

**Metric mismatch:** rare loss improved, but rare accuracy decreased for the
full method. This may indicate calibration/margin changes rather than clean rare
feature recovery.

**Alternative explanation still alive:** confidence-gated common updates or
generic update regularization may explain rare loss improvement.

## Claim Boundary

Can claim:

- the full projected-update method improved rare loss on the controlled surface;
- the full method beat dense shared rare loss under this loss metric;
- selected update suppression reduced conflict-projector update mass.

Cannot claim:

- the intended routing-weighted conflict mechanism is supported;
- projected MoE has functional expert specialization;
- dense-beating rare loss implies semantic experts or real-DCLM transfer;
- rare-feature recovery is solved, because rare accuracy did not improve.

## Next Decision

Run a mechanism separation follow-up before promoting the method:

1. `confidence_gate_only`: same common confidence gate, no conflict projection.
2. `update_projection_only`: conflict update projection without router
   projection.
3. `adam_conflict_projector`: use the more stable AdamW-like projector instead
   of the raw projector.
4. Calibration / threshold audit for rare accuracy versus rare loss.

Only if rare loss, rare accuracy, and \(\mathcal{C}_{C,R}\) move together should
the anchor be upgraded from insufficient to supported.
