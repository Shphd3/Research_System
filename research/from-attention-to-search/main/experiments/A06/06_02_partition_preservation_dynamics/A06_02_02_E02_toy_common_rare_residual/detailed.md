# Detailed: A06_02_02_E02_toy_common_rare_residual

Primary anchor:
`Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

Protocol:
`protocol.md`

Summary:
`summary.md`

## 0. Quick Recap

Purpose: Test the A06_02_02_E02.a--A06_02_02_E02.g common-removed differential expert proxy chain
on synthetic data before any real-DCLM claim.

Hypothesis: Raw principal expert proxies are common-dominated; residual or
differential residual proxies improve rare routing; early common recapture
requires residual input or row projection; differential rare-step updates are
feasible only when common recapture is controlled.

Conclusion: Supported on synthetic data. The strongest remaining boundary is
that the run uses oracle synthetic rare directions and synthetic common
recapture, not real hidden states or real LM loss.

## 1. Protocol Compliance Audit

approved conditions match actual conditions: yes for the synthetic protocol.

primary metric exists: yes, rare margin at step 0 and step 10 plus sign-flip
rate.

central figures/tables exist: yes, see `figures/` and `tables/`.

seeds/checkpoints recorded: yes, seeds 0--7; synthetic checkpoints step 0 and
step 10.

known good/bad/confusing cases reviewed: yes.

success/failure/insufficient-evidence criteria applied: yes, in `summary.md`.

remote execution compliance: incomplete. The user requested remote 4-GPU
execution. The synthetic experiment completed in the current environment, but
remote 4-GPU execution was blocked by unavailable / unauthorized configured
remote entrances.

## 2. Setup

Data construction: For each sample, hidden state
\(h_i=\alpha c+\beta r_{y_i}+\epsilon_i\), where \(c\) is the common direction and
\(r_{y_i}\) is the group-specific rare direction.

Model / router / algorithm: Four expert rows are generated from random,
raw-principal, residual-principal, or differential-residual proxy definitions.

Expert gain matrix:

\[
M_e=g_c cc^\top + g_r r_er_e^\top+\xi_e.
\]

Raw principal proxy:

\[
u_e^{raw}=\mathrm{TopEig}(M_e).
\]

Residual principal proxy:

\[
u_e^{res}=\mathrm{TopEig}(P_RM_eP_R).
\]

Differential residual proxy:

\[
u_e^{diff}=\mathrm{TopEig}^+(P_R(M_e-\bar M)P_R).
\]

Parameters: dimension 64, 4 experts, 2048 samples per group, seeds 0--7,
common strength 4.0, rare strength 1.6, common gain 8.0, rare gain 3.0,
common recapture strength 3.5.

Runner:
`scripts/run_synthetic_common_removed_differential_proxy.py`

Result path:
`tables/all_experiment_summary.csv`

## 3. Metrics And Decision Rules

rare margin: target expert score minus strongest competing expert score.

proxy-route NMI: normalized mutual information between synthetic labels and
routes.

sign-flip rate: fraction of samples whose step-0 positive rare margin becomes
non-positive at step 10.

synthetic loss: cross-entropy over synthetic expert labels.

selected utility: route equals the synthetic ground-truth expert.

## 4. Main Results

| Stage | Supported / weakened / insufficient | Key evidence | Boundary |
| --- | --- | --- | --- |
| A06_02_02_E02.a sanity split | Supported | hidden-centering improves load but not rare margin; differential proxy reaches accuracy 1.0 | synthetic labels are oracle |
| A06_02_02_E02.b projector robustness | Mostly supported | oracle/mean/perturbed pass; top-PC weaker but positive | top-PC estimator still degrades |
| A06_02_02_E02.c raw critique | Supported | raw common overlap 0.9999 and rare margin -2.9990 | constructed common-dominated synthetic gain |
| A06_02_02_E02.d initialization | Supported with caveat | residual and differential both pass | this toy does not separate residual principal from differential residual |
| A06_02_02_E02.e preservation | Supported | init-only sign flips 0.5260; residual controls 0.0060 | synthetic common recapture |
| A06_02_02_E02.f functional binding | Supported | load-only utility 0.2552; preserved differential 0.9940 | synthetic utility is label-defined |
| A06_02_02_E02.g step sizes | Partially supported | common-zero passes; common-small rare-4x needs residual input or row projection | does not estimate real stable learning rate |

## 5. Visualization Results

### A06_02_02_E02.a Rare Margin

![A06_02_02_E02.a rare margin](figures/a06_26a_rare_margin_mean.png)

Purpose: Separate load-only effects from rare-margin specialization.

Observed result: Hidden-centering improves load but leaves rare margin
negative. Residual and differential proxies produce positive rare margin.

Take-home: load balance is not enough.

### A06_02_02_E02.c Common Overlap

![A06_02_02_E02.c common overlap](figures/a06_26c_common_overlap.png)

Purpose: Test whether raw principal proxy is common-dominated.

Observed result: raw principal common overlap is 0.9999; differential residual
overlap is near zero.

Take-home: the synthetic MPI-style raw proxy reads common gain, not rare
function.

### A06_02_02_E02.e Sign Flip

![A06_02_02_E02.e sign flip](figures/a06_26e_sign_flip_rate.png)

Purpose: Test whether step-0 initialization survives common recapture.

Observed result: init-only sign flip rate is 0.5260; residual input / row
projection / symmetric residual routing are 0.0060.

Take-home: preservation requires residual control in this synthetic surface.

### A06_02_02_E02.g Rare Margin

![A06_02_02_E02.g rare margin](figures/a06_26g_rare_margin_mean.png)

Purpose: Test the two user-proposed differential step-size schemes.

Observed result: common-small / rare-base improves loss but does not preserve
the route. Common-zero variants pass. Common-small / rare-4x passes only after
residual input or row projection.

Take-home: rare can use a larger step when common recapture is controlled.

## 6. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / failed / unclear | Failure reason | What this rules out |
| --- | --- | --- | --- | --- |
| hidden-centering | max load 0.3103 but route accuracy 0.2552 | passed as negative control | only removes bias/load | rules out load as specialization evidence |
| raw principal | common overlap 0.9999, rare margin -2.9990 | passed as critique | common-dominated gain | rules out raw principal as sufficient in this toy |
| differential proxy | rare margin 1.3881, accuracy 1.0 | passed | none | supports residual proxy target |
| init-only preservation | sign flip 0.5260 | failed | common recapture | rules out initialization-only |
| residual control | sign flip 0.0060 | passed | none | supports residual input / row projection |
| common-small rare-large | rare margin 0.0381, sign flip 0.5178 | insufficient alone | remaining common recapture | shows larger rare step alone is not enough |
| common-small rare-large + residual | rare margin 1.3094, sign flip 0.0 | passed | none | supports differential step-size with common control |

## 7. Remote 4-GPU Execution Record

Current environment: one H100 is visible to PyTorch. `torch.cuda.device_count()`
returned 1.

Local `sco`: unavailable.

Configured remote entrances checked:

- `118.145.32.132:11109`: permission denied.
- `118.145.32.132:10109`: SSH preflight hung with no output and was
  interrupted.
- `118.145.32.132:12109`: SSH preflight hung with no output and was
  interrupted.

Therefore the requested remote 4-GPU execution was not completed. The synthetic
run itself completed locally and does not require 4 GPUs.

## 8. Claim Boundary

Can claim: synthetic evidence supports the mechanism chain and the feasibility
of differential step sizes when common recapture is controlled.

Cannot claim: real-DCLM transfer, real LM loss preservation, real expert
utility, or final router design.

## 9. Next Decision

Move to a real-DCLM audit only after choosing the real common operator and
proxy labels. The real audit should be narrower than this synthetic suite:
raw principal versus residual differential proxy, projector robustness, early
margin preservation, sign flips, and LM loss.

## 10. Artifact Map

anchor:
`Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

protocol:
`Projects/from-attention-to-search/main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_02_E02_toy_common_rare_residual/protocol.md`

summary:
`Projects/from-attention-to-search/main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_02_E02_toy_common_rare_residual/summary.md`

code workspace:
`Projects/from-attention-to-search/main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_02_E02_toy_common_rare_residual`

runner:
`scripts/run_synthetic_common_removed_differential_proxy.py`

key tables:
`tables/all_experiment_summary.csv`

figures:
`figures/`

repro command:

```bash
python Projects/from-attention-to-search/main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_02_E02_toy_common_rare_residual/scripts/run_synthetic_common_removed_differential_proxy.py \
  --out-dir Projects/from-attention-to-search/main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_02_E02_toy_common_rare_residual
```
