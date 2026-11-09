---
experiment_id: A14_02_E03_rare_common_subspace_reuse
status: parked_before_full_run
verdict: parked_e02_common_space_gate_failed
completed_date: 2026-07-26
---

# Summary: A14_02_E03 Rare–Common Subspace Reuse

Primary anchor: [A14_02_02](../../../../problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/subanchors/14_02_02_rare_common_subspace_reuse_anchor.md)  
Protocol: [approved conditional contract](protocol.md)

## Result Snapshot

**Verdict:** `parked_e02_common_space_gate_failed`; no full E03 treatment result
was produced.

**What we established:** the preregistered estimator did not identify a stable
leave-target-out common AdamW step-contrast space. Its held-out energy capture
ranged from 0.4780 to 0.6314 (mean 0.5717), so 0/10 seeds passed the 0.80 gate.

**What this means:** E02 can show common-mapping functional-rank reuse while raw
per-example optimizer contrasts remain broad or surface dependent. Under this
estimator, labeling a rare component “outside common” would be unstable.

**What we do next:** preserve the E03 protocol and parked result. Any repair
must be versioned and validated on fresh common probes; the current held-out
probe split cannot be used to choose a larger rank or a new space.

## Blocking Metric

For a common basis \(G_c\) fitted on 32 target-free step contrasts and 32 held-out
contrasts \(V_{test}\),

\[
C_{\mathrm{common}}
=
\frac{\|P_{G_c}V_{test}\|_F^2}{\|V_{test}\|_F^2}.
\]

This dimensionless fraction asks how much held-out common-update energy enters
the calibration-fitted space. The gate was \(C_{\mathrm{common}}\ge0.80\) in at
least eight seeds. Observed fitted ranks were 24--26, yet capture remained
below 0.632 in every seed.

## Key Figure

![Common parameter-space gate](figures/common_space_gate.png)

**How to read:** each bar is one LowF seed; the dashed line is the frozen 0.80
gate.  
**Observed:** every bar is below the gate.  
**Allowed conclusion:** the E03 common parameter-space operationalization is
not stable enough for causal outside/new labeling.  
**Does not prove:** rare effects require new functional directions.

## Unmeasured Primary Metrics

The approved E03 primary quantities remain

\[
v_r=\theta_T^{rare}-\theta_T^{ctrl},
\]

\[
\rho_{new}=\frac{\|v_{new}\|_2^2}{\|v_r\|_2^2},
\]

and

\[
\Delta CE_{drop-new}
=CE(\theta_T^{rare}-v_{new})-CE(\theta_T^{rare}).
\]

They were not measured in a full confirmation run because \(G_c\), and therefore
\(v_{new}\), was not validly identified.

## Claim Boundary

Can claim only that the registered common parameter-space estimator failed its
stability gate. Cannot claim parameter reuse, parameter novelty, functional
necessity, or refutation of the E02 state-level result.

## Next Decision

Choose between a fresh-probe raw-update-space repair and a ROOT-functional
common-space definition under a new protocol. The latter is better aligned
with the established E02 physical quantity.
