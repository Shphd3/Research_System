# Protocol: A06_01_04_E02 Real-DCLM Proxy-Center Router Initialization

## 0. Approval Snapshot

Approval status: A06_01_04_E01 supported with boundary; pre-approved by explicit user goal after dependency passes.
Purpose: decide whether A06_01_04_E01 proxy centers can initialize a valid linear top-1 router at step 0.
Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`
Anchor decision question: can proxy centers initialize a linear router whose assignments preserve the proxy partition?
Anchor physical prior tested: stable residual clusters should be linearly readable by equal-norm router rows.
Anchor core model term tested: \(w_e=\alpha\nu_e/\|\nu_e\|\) and \(NMI(q_i,a_i)\).
Anchor falsifier: load improves but proxy_route_NMI remains low, or routing is common/frequency dominated.
Experiment role: method construction.
Primary metric from anchor: held-out `proxy_route_NMI`.
Claim boundary from anchor: proxy-center-to-linear-router bridge only; step-0 source is the main initialization case, step-10 source is a warm-start/control boundary inherited from A06_01_04_E01.
Minimal setup: same DCLM audit surface as A06_01_04_E01, no training inside the router-initialization test except optional source checkpoint construction at step 10.
Basic configuration: build router rows from proxy centers; replay held-out exact router inputs; report actual raw-input routing and centered-input diagnostic routing separately.
Conditions to run: random, equal-norm random, raw proxy center, residual proxy center, whitened proxy center, label-shuffled proxy guard.
Pass: proxy-center init improves proxy_route_NMI over random with active experts and bounded common margin.
Fail: random-like NMI, empty experts, or common/frequency-driven success.
Insufficient: A06_01_04_E01 did not pass, missing proxy dependency audit, or no held-out split.
Cannot claim: training preservation, utility, semantic feature discovery.
Approval decision: execute only after A06_01_04_E01 dependency passes.

## 1. Anchor Alignment

The protocol tests the proxy-center-to-linear-router bridge, not proxy discovery itself.

## 2. Tested Hypothesis

H1: residual proxy centers are linearly readable and improve proxy_route_NMI.
H2: equal-norm residual centers reduce row-norm/common artifacts.

## 3. Rival Explanations

Load-only success, common-margin success, frequency bucket success, and label leakage.

## 4. Data / Model / Algorithm / Objective

Data/model from A06_01_04_E01. Algorithm: convert proxy centers into router rows, replay held-out tokens, evaluate proxy_route_NMI, load, margins, and nuisance dependence. No training.

## 5. Conditions, Seeds, And Checkpoints

Use A06_01_04_E01 seeds. Test proxy source checkpoints 0 and 10 because A06_01_04_E01 found step-0 late-layer proxy only modestly stable but step-10 late-layer proxy strongly stable. Step 0 remains the main pure-initialization case; step 10 is a stronger-proxy control.

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| random | baseline | chance routing | floor | NMI/load | lower | overlaps main | missing | table |
| equal-norm random | row-norm guard | A06_01_01_E04 | guard | NMI/load | lower | overlaps main | missing | table |
| raw proxy center | raw bridge | common capture | comparison | margins | useful | common dominated | missing | heatmap |
| residual proxy center | main bridge | proxy center | main | raw and centered proxy_route_NMI | high | low | no dep | figure |
| whitened proxy center | load-only guard | whitening | A06_01_03_E01 warning | NMI/load | clean | load-only | missing | figure |
| label-shuffled proxy | leakage guard | false labels | guard | NMI | low | high | missing | table |

## 6. Primary Metric

Held-out raw-input `proxy_route_NMI`. It decides whether the actual linear router assignment follows the proxy partition when applied to the same hidden states the router would see.

Centered-input `proxy_route_NMI` is a diagnostic, not the primary metric. If centered routing is high but raw routing is low, the bottleneck is common-logit bias rather than proxy center separability.

## 7. Secondary Metrics

Load \(L\), active experts, common margin, residual margin, proxy purity, nuisance NMI, margin p05.

## 8. Known Good / Known Bad / Known Confusing Cases

Known good: synthetic A06_01_03_E02/A06_02_01_E01 pseudo center.
Known bad: random/equal-norm random.
Known confusing: balanced load with low NMI.

## 9. Stage-Level Profiling Plan

Dependency audit, center construction audit, row-norm audit, replay audit, proxy heatmap, nuisance guard.

## 10. Algorithm Specification, If Nontrivial

input: A06_01_04_E01 proxy centers and held-out hidden states.
parameters: norm scale \(\alpha\) from random router mean row norm.
steps: normalize centers; initialize rows; compute raw scores; compute centered diagnostic scores; assign top-1 expert; compute metrics and audits.
outputs: tables, heatmaps, center audit.
failure reasons: dependency failed, low linear separability, common capture, nuisance capture.

## 11. Success / Failure / Insufficient Evidence

Support: high proxy_route_NMI with clean guards.
Weaken: low NMI or common/nuisance artifacts.
Insufficient: missing A06_01_04_E01 dependency or held-out audit.

## 12. What This Cannot Claim

No training preservation, expert utility, semantic discovery, or final method.

## 13. Review Notes And Protocol Changes

2026-06-22: conditional protocol created for sequential execution after A06_01_04_E01.
2026-06-22: updated after A06_01_04_E01 full01. A06_01_04_E01 supports proxy existence but weakens the common-centering discovery claim, so A06_01_04_E02 separates raw-input routing from centered-input diagnostic routing.
