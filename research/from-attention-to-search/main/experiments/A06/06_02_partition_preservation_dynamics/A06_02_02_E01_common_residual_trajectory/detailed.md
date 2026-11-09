# Detailed: A06_02_02_E01 Router Common-Residual Trajectory Audit

## 0. Quick Recap

Purpose: decide whether early real-DCLM proxy-route collapse is explained by
router-gap updates moving along common-mode directions rather than
feature-residual directions.

Hypothesis: `raw_center` collapse should coincide with
\(\Lambda_{\mathrm{upd}}>1\) under robust common projectors.

Experimental idea: rerun the A06_01_04_E03 real-DCLM proxy-init training audit, but
collect checkpoint hidden states and router rows, then decompose router-gap
updates into common and residual terms.

Conclusion: the strong common-dominated trajectory hypothesis is weakened.
The collapse is reproduced, but common dominance is projector-dependent.

Evidence: `raw_center` NMI falls from `0.7549` at step 0 to `0.0410` at step 5
and `0.0131` at step 10; mean-common \(\Lambda_{\mathrm{upd}}>1\), while top
hidden-PC and router-row projectors stay below 1.

## 1. Protocol Compliance

Protocol: `protocol.md`.

Status: completed.

The full run executed the approved setup:

- model seeds: `0, 1, 2`;
- variants: `random`, `equal_norm_random`, `raw_center`, `residual_center`;
- audit layers: 3, 4, 5;
- checkpoints: `0, 1, 2, 3, 5, 10, 20, 50`;
- common projectors: mean-common, top hidden-PC, router-row subspace;
- full run job id: `pt-i3bkewya`;
- ACP state: `SUCCEEDED`;
- run name: `a06_22_router_common_residual_trajectory_4gpu_20260630_full01`.

Coverage:

| Table | Rows |
|---|---:|
| `tables/full01_router_update_trajectory.csv` | 864 |
| `tables/full01_common_residual_margin_by_pair.csv` | 48,384 |
| `tables/full01_snapshot_inventory.csv` | 288 |
| `tables/full01_common_projector_robustness.csv` | 24 |

Decomposition identity audit:

\[
\gamma_{f,e}(t)
=
\gamma_{f,e}(0)
+
\Delta u_{f,e}(t)^\top\mu_f(0)
+
u_{f,e}(0)^\top\Delta\mu_f(t)
+
\Delta u_{f,e}(t)^\top\Delta\mu_f(t).
\]

Maximum absolute reconstruction error:

```text
8.37e-7
```

This is below the protocol tolerance needed for interpreting the decomposition.

## 2. Setup

Experiment folder:

```text
Projects/from-attention-to-search/main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_02_E01_common_residual_trajectory
```

Runner:

```text
scripts/run_a06_22_router_common_residual_trajectory_audit.py
```

Submit script:

```text
scripts/submit_a06_22_router_common_residual_trajectory_4gpu_acp.sh
```

Full run command inside ACP:

```text
torchrun --standalone --nproc_per_node=4 \
  scripts/run_a06_22_router_common_residual_trajectory_audit.py \
  --run-name a06_22_router_common_residual_trajectory_4gpu_20260630_full01 \
  --run-stage full \
  --output-dir Projects/from-attention-to-search/main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_02_E01_common_residual_trajectory
```

Runtime log:

```text
logs/acp/a06_22_router_common_residual_trajectory_4gpu_20260630_full01_runtime_20260630_165023.log
```

Raw run directory:

```text
runs/router_common_residual_trajectory/a06_22_router_common_residual_trajectory_4gpu_20260630_full01
```

## 3. Metric Definitions

**Proxy-route NMI:** normalized mutual information between fixed step-0 proxy
labels and current top-1 expert routes. It measures preservation of the proxy
partition, not expert utility.

**Matched preserve fraction:** for each proxy label, the fraction of tokens
still routed to that label's step-0 majority expert. The summary uses the
minimum across proxy labels because a single collapsed feature is important.

**Router gap:** for proxy label \(f\) and competitor expert \(e\),

\[
u_{f,e}(t)=w_{a(f)}(t)-w_e(t),
\]

where \(a(f)\) is the step-0 majority expert for proxy label \(f\).

**Current margin:**

\[
\gamma_{f,e}(t)=u_{f,e}(t)^\top\mu_f(t).
\]

**Common/residual update dominance:**

\[
\Lambda_{\mathrm{upd}}(t)
=
\operatorname{median}_{f,e}
\frac{
\left|\Delta u_{f,e}(t)^\top P_C\mu_f(0)\right|
}{
\left|\Delta u_{f,e}(t)^\top (I-P_C)\mu_f(0)\right|+\varepsilon
}.
\]

Values above 1 mean common-projected update terms are larger than residual
update terms under the chosen projector. Values below 1 mean residual terms
are larger.

**Sign flip rate:** fraction of feature/competitor pairwise margins with
\(\gamma_{f,e}(t)\leq 0\).

## 4. Result Tables

### Raw-Center Collapse Reproduction

| Step | Proxy-route NMI | Matched preserve min | Max route load | LM loss |
|---:|---:|---:|---:|---:|
| 0 | 0.7549 | 0.6754 | 0.1812 | n/a |
| 1 | 0.5037 | 0.3550 | 0.2523 | 12.0343 |
| 2 | 0.3271 | 0.1333 | 0.3801 | 11.9200 |
| 3 | 0.1901 | 0.0360 | 0.5839 | 11.7440 |
| 5 | 0.0410 | 0.0037 | 0.9479 | 11.1926 |
| 10 | 0.0131 | 0.0002 | 0.9645 | 10.7222 |
| 20 | 0.0048 | 0.0000 | 0.9832 | 9.2196 |
| 50 | 0.0337 | 0.0000 | 0.7575 | 7.8827 |

Loss delta raw-center minus random:

| Step | Loss delta |
|---:|---:|
| 5 | +0.0040 |
| 10 | +0.0032 |

### Raw-Center Projector Decision Table

| Projector | Step | \(\Lambda_{\mathrm{upd}}\) | Mean abs common update | Mean abs residual update | Step-0 residual margin min | Sign flip rate |
|---|---:|---:|---:|---:|---:|---:|
| mean-common | 5 | 2.1507 | 0.0236 | 0.0120 | 0.6493 | 0.4147 |
| mean-common | 10 | 1.9856 | 0.0312 | 0.0163 | 0.6493 | 0.4782 |
| top hidden-PC | 5 | 0.7089 | 0.0157 | 0.0189 | 0.0324 | 0.4147 |
| top hidden-PC | 10 | 0.6666 | 0.0197 | 0.0265 | 0.0324 | 0.4782 |
| router-row subspace | 5 | 0.4611 | 0.0104 | 0.0236 | -0.1839 | 0.4147 |
| router-row subspace | 10 | 0.4332 | 0.0137 | 0.0317 | -0.1839 | 0.4782 |

Interpretation: the main NMI collapse is real, but the common/residual
decomposition is not projector-robust. Mean-common supports common dominance;
top hidden-PC and router-row subspace support residual-dominated updates.

## 5. Visualization Results

### Proxy-Route NMI Reproduction

![Proxy-route NMI reproduction](figures/full01_proxy_route_nmi_reproduction.png)

Purpose: verify that this run reproduces the A06_01_04_E03 failure before interpreting
new decomposition metrics.

Setup: variants from A06_01_04_E03, seeds 0/1/2, layers 3/4/5, checkpoints through
step 50.

How to read: higher NMI means expert routes preserve the fixed step-0 proxy
labels.

Observed result: `raw_center` begins high and collapses by step 5/10.

Take-home: the run is in the intended real-DCLM collapse regime.

Remaining uncertainty: NMI collapse does not by itself reveal which margin
term caused the collapse.

### Projector Lambda Step 5 And Step 10

![Projector lambda step 5 and 10](figures/full01_projector_lambda_step5_step10.png)

Purpose: test H3, whether common-over-residual dominance is stable across
common definitions.

Setup: `raw_center` only, three common projectors, decision steps 5 and 10.

How to read: \(\Lambda_{\mathrm{upd}}>1\) supports common-dominated updates
under that projector.

Observed result: mean-common is above 1; top hidden-PC and router-row subspace
are below 1.

Take-home: H1 fails the robustness rule.

Remaining uncertainty: a more physical common operator tied to gradients or
objective geometry may still show a stable common trajectory.

### Raw-Center Lambda Trajectory

![Raw-center lambda trajectory](figures/full01_raw_center_lambda_trajectory.png)

Purpose: show whether the projector split appears only at one checkpoint or
persists through the collapse window.

Observed result: mean-common stays above 1; the other two projectors remain
below 1 from step 5 through step 50.

Take-home: the disagreement is stable, not a one-step fluctuation.

### Raw-Center Lambda Versus NMI

![Raw-center lambda versus NMI](figures/full01_raw_center_lambda_vs_nmi.png)

Purpose: relate the decomposition metric directly to route collapse.

Observed result: NMI falls while mean-common lambda is high, but the other
projectors remain below 1.

Take-home: NMI collapse cannot be attributed to a projector-independent
common-dominated router update.

## 6. Hypothesis Updates

**H1 common-trajectory hypothesis:** weakened. A mean-common version is
supported, but the stronger projector-robust claim is not supported.

**H2 residual-margin insufficiency hypothesis:** partially supported. The
top hidden-PC projector gives near-zero step-0 residual margin, and the
router-row projector gives negative step-0 residual margin. This is consistent
with residual fragility, but the mean-common projector gives positive
residual margins, so the claim is not yet operator-independent.

**H3 common-projector robustness hypothesis:** weakened. The full run shows
that common definition is the active modeling bottleneck.

## 7. Failure Analysis

The failed part is not real-DCLM reproduction. The run clearly reproduces
A06_01_04_E03.

The failed part is the mechanism generality. The anchor's H1 required the
common-over-residual update dominance result to hold across common definitions.
It does not.

This means the phrase "common mode" is still under-defined for this real-DCLM
training trajectory. A global mean direction, a high-variance hidden subspace,
and a router-row subspace do not represent the same physical object.

## 8. Claim Boundary

Can claim:

- The A06_01_04_E03 real-DCLM proxy-init collapse is reproduced in the A06_02_02_E01 audit.
- Collapse is accompanied by rising load concentration, falling matched
  preserve fraction, and large pairwise sign-flip rates.
- Common-over-residual dominance is projector-dependent.

Cannot claim:

- common-dominated update is the established root cause;
- generic common removal will fix preservation;
- long-tail residual directions are meaningless;
- real semantic experts or expert utility have been validated.

## 9. Artifact Map

Code workspace:

```text
/data/250010109/Research_System
```

Experiment folder:

```text
Projects/from-attention-to-search/main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_02_E01_common_residual_trajectory
```

Runner:

```text
scripts/run_a06_22_router_common_residual_trajectory_audit.py
```

Submit script:

```text
scripts/submit_a06_22_router_common_residual_trajectory_4gpu_acp.sh
```

Run directory:

```text
runs/router_common_residual_trajectory/a06_22_router_common_residual_trajectory_4gpu_20260630_full01
```

Job id:

```text
pt-i3bkewya
```

Runtime log:

```text
logs/acp/a06_22_router_common_residual_trajectory_4gpu_20260630_full01_runtime_20260630_165023.log
```

Curated tables:

```text
tables/full01_key_decision_metrics.csv
tables/full01_router_update_trajectory.csv
tables/full01_common_residual_margin_by_pair.csv
tables/full01_common_projector_robustness.csv
tables/full01_snapshot_inventory.csv
tables/full01_run_summary.json
tables/full01_run_config.json
```

Curated figures:

```text
figures/full01_proxy_route_nmi_reproduction.png
figures/full01_projector_lambda_step5_step10.png
figures/full01_raw_center_lambda_trajectory.png
figures/full01_raw_center_lambda_vs_nmi.png
figures/full01_common_residual_update_terms_mean_common.png
figures/full01_common_residual_update_terms_top_hidden_pc.png
figures/full01_common_residual_update_terms_router_row_subspace.png
```

Repro command:

```text
A06_22_ALLOW_REAL_SUBMIT=1 \
RUN_NAME=a06_22_router_common_residual_trajectory_4gpu_20260630_full01 \
JOB_NAME=ats-a06-22-router-trajectory-4gpu \
bash scripts/submit_a06_22_router_common_residual_trajectory_4gpu_acp.sh
```

## 10. Next Decision

Do not move directly to a new gating method from A06_02_02_E01. The next research
decision is to define a sharper common operator that is tied to the training
objective, gradient, or router-update geometry, then rerun this exact
decomposition. If that operator gives a stable \(\Lambda_{\mathrm{upd}}>1\)
during collapse, a preservation method can target that operator. If it does
not, the main mechanism should shift toward residual-margin fragility or
objective-incompatible routing rather than common overwrite.
