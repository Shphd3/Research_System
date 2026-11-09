# Protocol: A06_01_04_E01 Real-DCLM Proxy Feature Operationalization

## 0. Approval Snapshot

Approval status: Pre-approved by explicit user goal for autonomous six-anchor iteration; smoke must pass before full run.
Purpose: decide whether real DCLM router-input residual hidden states contain stable label-free proxy features.
Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`
Anchor decision question: can real DCLM residual hidden states produce stable proxy clusters not mainly explained by nuisance variables?
Anchor physical prior tested: repeated real-text latent factors should leave stable residual hidden-state structure, but token id/frequency/position may explain it.
Anchor core model term tested: \(h_i=c_b+r_i\) and \(q_i=\operatorname{Cluster}(r_i)\).
Anchor falsifier: clusters are unstable across splits/checkpoints or mostly explained by token id/frequency/position.
Experiment role: operationalization / proxy test.
Primary metric from anchor: held-out split-to-split proxy assignment stability after center matching.
Claim boundary from anchor: real-data proxy definition only; no gating method or expert utility claim.
Minimal setup: small random-initialized Qwen-style DCLM top-1 MoE, DCLM packed stream, fixed audit splits, late layers 3--5.
Basic configuration: collect exact router inputs at checkpoints 0 and 10; cluster calibration residuals; evaluate held-out split stability and nuisance dependence.
Conditions to run: raw hidden k-means, residual k-means, spherical residual k-means, whitened residual k-means, random assignment control.
Pass: residual clustering has stable held-out assignments above random and nuisance NMI does not dominate.
Fail: instability, nuisance-dominated clusters, empty clusters, or batch artifact.
Insufficient: missing disjoint split audit, missing nuisance audit, no center matching, or no top-frequency removal guard.
Cannot claim: semantic feature discovery, expert utility, training preservation, or final routing method.
Approval decision: execute A06_01_04_E01 first; later anchors depend on this result.

## 1. Anchor Alignment

Decision question: whether a measurable real-data proxy feature exists.
Physical prior tested: stable latent factors should appear in residual hidden geometry.
Core model term tested: common-centered residual clusters.
Falsifier: unstable or nuisance-explained clusters.
Claim boundary: proxy audit only.

## 2. Tested Hypothesis

H1: residual clusters are more stable than raw/whitened/random controls.
H2: residual clusters are not reducible to token id, token frequency, or position.

## 3. Rival Explanations

- Token identity: separated by token-id and top-token audits.
- Token frequency: separated by top 1% / top 5% removal and frequency-bin NMI.
- Position: separated by position NMI.
- Batch artifact: separated by disjoint split stability.
- Load-only artifact: separated by stability and nuisance metrics.

## 4. Data / Model / Algorithm / Objective

Data: DCLM packed stream used by A06_01_01. Model: random-initialized Qwen-style top-1 MoE with exact router input capture. Algorithm: collect router inputs, estimate common vector on calibration split, cluster residual states, match centers across splits, and evaluate held-out assignments. Objective: no training intervention; proxy audit only.

## 5. Conditions, Seeds, And Checkpoints

Seeds: `0,1,2` if available in the DCLM runner. Checkpoints: `0,10` with `0` as primary and `10` as early-training guard. Layers: `3,4,5` plus layer `0` guard.

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| raw hidden k-means | P1 | no common removal | baseline | stability + nuisance | stable and clean | nuisance/batch | no split | `tables/proxy_cluster_summary.csv` |
| residual k-means | P1/P2 | \(r=h-c\) | main test | stability + nuisance | stable and clean | unstable | missing common | `figures/proxy_stability_by_condition.png` |
| spherical residual k-means | P1 | angular structure | norm guard | stability | matches residual | worse | no center audit | same |
| whitened residual | P3 | load-only control | A06_01_03_E01 warning | stability/NMI | stable and clean | load-only | missing whitening audit | same |
| random assignment | falsifier | chance floor | baseline | NMI/agreement | lower than residual | overlaps residual | missing | table |

## 6. Primary Metric

Held-out split-to-split proxy stability after center matching. It decides because a proxy must be reproducible before it can judge router specialization.

## 7. Secondary Metrics

Cluster load, active clusters, center margin, token-id NMI, frequency-bin NMI, position NMI, top-frequency removal stability, cluster token/context examples.

## 8. Known Good / Known Bad / Known Confusing Cases

Known good: synthetic A06_01_03_E02 residual k-means recovers labels.
Known bad: random assignment and A06_01_03_E01 load-only controls.
Known confusing: high load balance with high token-frequency NMI.

## 9. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| data audit | are splits disjoint and sized? | token ids / positions | counts match | `data_audit.csv` | required |
| hidden capture | are exact router inputs captured? | model hooks | finite tensors | `hidden_audit.csv` | required |
| clustering | are centers nonempty? | residuals | no empty clusters | `cluster_audit.csv` | required |
| stability | do centers transfer? | split centers | above random | `proxy_cluster_summary.csv` | required |
| nuisance | are clusters nuisance? | token/frequency/position | bounded NMI | `nuisance_audit.csv` | required |

## 10. Algorithm Specification, If Nontrivial

input: DCLM audit batches, model checkpoint, layer id, router inputs.
parameters: `K=8` experts/proxy clusters by default; `top_frequency_cutoffs={1%,5%}`; k-means `n_init=20`.
intermediate variables: common vector \(c\), residual matrix \(R\), centers \(\nu_k\), assignments \(q_i\), nuisance variables.
steps: collect inputs; split calibration/evaluation; compute common; cluster calibration residuals; match centers across splits; evaluate held-out assignments; compute nuisance metrics; save examples.
outputs: summary tables, stability plots, nuisance audit, examples.
debug artifacts: per-cluster token examples and center occupancy.
pass conditions: residual clusters stable and nuisance-bounded.
fail conditions: unstable, empty, or nuisance-dominated clusters.
failure reasons: data bug, hidden capture mismatch, no proxy structure, nuisance proxy, too few samples.

## 11. Success / Failure / Insufficient Evidence

Support: residual clustering gives stable proxy clusters above random and not dominated by nuisance.
Weaken: no stable clusters or nuisance dominates.
Insufficient: missing split, hidden, cluster, or nuisance audit.

## 12. What This Cannot Claim

No semantic feature claim, no router initialization claim, no expert utility claim, no full DCLM specialization claim.

## 13. Review Notes And Protocol Changes

2026-06-22: created as first real-data bridge after A06_01_03_E02/A06_02_01_E01 synthetic success and A06_01_01_E01/A06_01_01 real-DCLM bottlenecks.
