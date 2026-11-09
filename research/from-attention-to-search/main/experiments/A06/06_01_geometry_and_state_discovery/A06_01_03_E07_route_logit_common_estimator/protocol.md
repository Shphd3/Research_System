# Protocol: A06_01_03_E07 Route-Logit Common Estimator Under Random-Init Training

## 0. Approval Snapshot

**Approval status:** approved by user and completed locally.

**Purpose:** decide whether a routing-aware common estimator can remove
load-driving directions under random-init training and make feature residual
geometry easier to cluster or route.

**Primary anchor:** `../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

**Anchor decision question:** does a route-logit common estimator recover
feature residual geometry better than mean, top-PC, load-only, and
random-direction controls?

**Anchor physical prior tested:** routing common is router-relative: the common
direction that matters is the direction that changes relative expert logits or
expert load, not necessarily the global mean or largest hidden-state variance.

**Anchor core model term tested:**

\[
S_{\mathrm{logit}}(v;t)
=\operatorname{Var}_i(v^\top h_i(t))
\left\|P_E W_t v\right\|_2^2.
\]

**Anchor falsifier:** route-logit subtraction changes load but does not improve
held-out route-position feature NMI or raw route margins beyond mean/top-PC/
random controls.

**Experiment role:** root-cause audit / common-estimator operationalization.

**Primary metric from anchor:** \(\Delta \mathrm{feature\_NMI}\) after
subtraction, measured on held-out route-position states.

**Claim boundary from anchor:** controlled no-position A06 bridge only. This
does not claim real-DCLM semantic features, expert utility, or a final
initializer.

**Minimal setup:** use existing A06_02_01_E02/A06_01_03_E06-style controlled no-position
bridge snapshots if they contain all-position hidden states and router rows;
otherwise rerun random-init training only to collect the required snapshots.

**Basic configuration:** one-layer Transformer + top-1 MoE, 4 experts,
feature slot length 4, route on last slot token, no learned absolute positional
embedding, balanced feature/nuisance/slot-start data.

**Conditions to run:** raw all-position baseline, mean subtraction, top-PC
subtraction, random-direction subtraction, load-sensitive ablation, route-logit
subtraction, and route-only positive control.

**Pass:** route-logit subtraction improves held-out route-position feature NMI
and/or raw route margin over all non-routing controls, without stronger
position/frequency/nuisance dependence.

**Fail:** it only changes load, matches top-PC/random controls, or selects
position/frequency/slot-role shortcuts.

**Insufficient:** missing all-position hidden states, missing router rows,
missing held-out route-position states, missing metadata guards, or fitting
uses feature labels / position labels / route-position labels.

**Cannot claim:** real-DCLM behavior, semantic features, utility, RoPE
behavior, or training preservation.

**Approval decision:** approved in chat; local full run completed as
`a06_20_route_logit_common_estimator_full_20260629_010533`.

## 1. Anchor Alignment

**Decision question:** Can routing-aware common subtraction reveal feature
residual centers under random-init training?

**Physical prior tested:** the common component that matters for top-1 routing
is a direction that changes relative route logits or expert load.

**Core model term tested:** \(S_{\mathrm{logit}}(v;t)\) and the residualized
state \(h_i'(t)=h_i(t)-P_C h_i(t)\).

**Falsifier:** load improves but feature NMI and margin do not improve.

**Claim boundary:** controlled bridge mechanism audit only.

## 2. Tested Hypothesis

**H1 route-logit common removal:** A direction ranked by route-logit influence
removes routing-common bias and improves feature readout.

**H2 top-PC shortcut:** top hidden-state variance is not the same as
routing-common bias; top-PC subtraction may change geometry or load without
improving feature readout.

**H3 load-only confound:** directions that strongly change expert load may not
recover feature residuals.

**H4 random-router artifact:** a direction that works for one random seed but
not across seeds/checkpoints is not a stable mechanism.

## 3. Rival Explanations

- True routing-common removal.
- Generic PCA / position / frequency / role shortcut.
- Load-only fix without feature recovery.
- Random-router-seed artifact.
- Route-position leakage: the estimator accidentally selects route-position
  states rather than a common direction.
- Feature geometry already present: apparent gain is small because raw
  all-position is already strong.
- Feature geometry erased: no common subtraction can recover it after training.

## 4. Data / Model / Algorithm / Objective

**Data:** controlled no-position A06 bridge. Use the same feature/nuisance/slot
construction as A06_01_03_E03-A06_01_03_E06:

- 4 features, 4 nuisance ids, 4 experts;
- feature slot length 4;
- movable slot starts;
- target depends on feature slot;
- route position is the last token of the slot.

**Model:** one-layer Transformer + top-1 MoE, no learned absolute positional
embedding. The audit uses random or equal-norm random router initialization.

**Training objective:** original slot-end target cross-entropy. The estimator
does not change training; it audits snapshots.

**Hidden-state population:** primary fitting pool is all-position hidden
states. Held-out evaluation is route-position states only. Route-position
membership and feature labels are not used during fitting.

**Main output object:** center sets fitted after subtracting candidate common
subspaces. Centers are evaluated by routing held-out route-position states.

## 5. Conditions, Seeds, And Checkpoints

**Seeds:** 8 controlled seeds, matching the A06_01_03_E03-A06_01_03_E06 seed family when
possible.

**Checkpoints:** primary snapshots are steps `0, 5, 10, 100, 1600`. Step 0
tests random-init geometry. Steps 5/10 test early training where routing
collapse usually appears. Steps 100/1600 test whether the effect persists.

**Subspace ranks:** primary rank \(m=4\), because there are 4 experts and the
common subspace may be multi-directional. Report \(m=1\) as a guard against
rank-choice artifacts.

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Raw all-position | baseline | no subtraction | defines difficulty | primary baseline | lower than route-logit | equals / beats route-logit | missing | estimator comparison table |
| Route-only control | positive control | feature geometry exists | proves task is possible | required guard | NMI near 1.0 | low NMI | missing | control table |
| Mean subtraction | common mean | global translation | checks simple common estimate | primary control | lower than route-logit | equals route-logit | missing | comparison table |
| Top-PC subtraction | high variance shortcut | position/frequency/role | tests PCA risk | primary control | lower than route-logit | equals route-logit | missing | direction audit |
| Random-direction subtraction | chance subspace | arbitrary removal | controls rank/removal effect | required guard | lower than route-logit | equals route-logit | missing | comparison table |
| Load-sensitive ablation | load-only fix | load confound | separates load from feature readout | secondary but required | improves only if feature improves too | load improves without NMI | missing | load vs NMI scatter |
| Route-logit subtraction | main estimator | routing-common removal | tests anchor mechanism | primary | best NMI/margin with clean guards | load-only or shortcut | missing | main figure |

## 6. Primary Metric

Primary metric:

\[
\Delta \mathrm{feature\_NMI}(t)
=
\mathrm{feature\_NMI}_{\mathrm{estimator}}(t)
-
\mathrm{feature\_NMI}_{\mathrm{raw}}(t).
\]

This metric decides the judgment because the anchor is not about making load
look better. It asks whether subtracting an estimated routing-common component
makes the route-position feature partition more discoverable.

False positive cost: load or PCA shortcuts could look good while feature
partition remains wrong. Therefore a pass requires feature NMI or raw margin
improvement plus shortcut guards.

False negative cost: raw all-position may already be strong at large sample
size. Therefore also report final raw margins and seed-level improvements, not
only mean NMI.

## 7. Secondary Metrics

- raw route margin using centers as router rows;
- centered-input diagnostic route margin;
- active experts and max load;
- change in expert load after subtracting the direction;
- nuisance / position / slot-start / frequency NMI;
- feature-purity heatmap;
- seed-level and checkpoint-level stability;
- cosine overlap between selected directions and top PCs, mean direction, and
  router-row subspace;
- selected direction transfer: fit directions on one calibration split, score
  on held-out split.

## 8. Known Good / Known Bad / Known Confusing Cases

**Known good:** route-only held-out feature NMI should be near 1.0 in the
controlled no-position bridge.

**Known bad:** raw all-position, PCA, AE, and SAE variants from A06_01_03_E05/A06_01_03_E06
do not reliably approach route-only.

**Known confusing:** raw all-position can become moderately strong with large
calibration size. A small mean NMI gain may not justify a new mechanism unless
the gain is seed-stable and margin-improving.

**Known confusing:** load can improve while feature NMI worsens. Load is a
guard, not the primary metric.

## 9. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| Snapshot audit | Do we have required hidden states and router rows? | snapshot inventory | pass if all-position and route-position states exist | `snapshot_inventory.csv` | detailed.md |
| Leakage audit | Did fitting use feature/position/route labels? | code path and metadata use | fail if labels enter fitting | `leakage_checklist.md` | detailed.md |
| Direction audit | What directions were selected? | direction scores and overlaps | pass if route-logit differs from top-PC/random | `direction_audit.csv` | detailed.md |
| Subtraction audit | Does subtraction change load only or feature readout? | load/NMI before-after | pass if NMI/margin improves | `estimator_comparison.csv` | summary.md |
| Shortcut audit | Is gain explained by nuisance/position/frequency? | NMI guards | fail if shortcut dominates | guard table | detailed.md |
| Stability audit | Does the effect hold across seeds/checkpoints? | seed/checkpoint table | pass if stable enough for mechanism claim | heatmap | summary.md |

## 10. Algorithm Specification

### Input

- calibration all-position hidden states \(H_{\mathrm{cal}}(t)\);
- held-out all-position hidden states \(H_{\mathrm{eval}}(t)\);
- held-out route-position hidden states \(R_{\mathrm{eval}}(t)\);
- router rows \(W_t\) from random-init training snapshot;
- post-hoc labels for evaluation only: feature id, nuisance id, slot start,
  position / role, and optional frequency bins.

### Parameters

- number of experts / clusters: \(K=4\);
- selected common rank: primary \(m=4\), guard \(m=1\);
- candidate top-PC count: \(K_{\mathrm{pc}}=32\);
- k-means restarts: use the same torch k-means backend as A06_01_03_E03/A06_01_03_E06 if
  available;
- held-out evaluation never enters fitting.

### Intermediate Variables

Expert-centering matrix:

\[
P_E=I-\frac{1}{E}\mathbf{1}\mathbf{1}^\top.
\]

For a unit candidate direction \(v\):

\[
s_v^2(t)=\operatorname{Var}_i(v^\top h_i(t)),
\]

\[
r_v^2(t)=\left\|P_E W_t v\right\|_2^2,
\]

\[
S_{\mathrm{logit}}(v;t)=s_v^2(t)r_v^2(t).
\]

Load-sensitive score:

\[
S_{\mathrm{load}}(v;t)
=
\left\|p_{\mathrm{expert}}(H;t)-
p_{\mathrm{expert}}(H-(Hv)v^\top;t)\right\|_1.
\]

### Candidate Direction Pool

Build directions without feature, position, or route labels:

1. normalized calibration mean;
2. top PCs of centered all-position hidden states;
3. normalized router rows and router-row contrast directions;
4. random orthonormal directions as controls.

The route-logit estimator ranks candidates by \(S_{\mathrm{logit}}(v;t)\).
The load-sensitive estimator ranks the same candidates by \(S_{\mathrm{load}}\).

### Route-Logit Estimator Steps

1. Collect \(H_{\mathrm{cal}}(t)\) and \(W_t\).
2. Generate the candidate direction pool.
3. Normalize every candidate direction.
4. Score each candidate with \(S_{\mathrm{logit}}(v;t)\).
5. Select \(m\) directions by orthogonal greedy selection:
   - choose the highest-score direction;
   - orthogonalize remaining candidates against selected directions;
   - rescore on the residual candidate direction;
   - repeat until \(m\) directions are selected.
6. Form \(C=[v_1,\ldots,v_m]\) with orthonormal columns.
7. Residualize calibration and evaluation hidden states:

\[
H' = H - HCC^\top.
\]

8. Fit k-means centers on residualized all-position calibration states
   \(H'_{\mathrm{cal}}\).
9. Assign held-out route-position residual states \(R'_{\mathrm{eval}}\) to the
   centers and compute feature NMI.
10. Map centers back to hidden-space rows and compute raw-input routing and
    margin guards on \(R_{\mathrm{eval}}\).
11. Repeat for mean, top-PC, random-direction, and load-sensitive controls.

### Outputs

- `tables/snapshot_inventory.csv`;
- `tables/direction_audit.csv`;
- `tables/estimator_comparison.csv`;
- `tables/seed_checkpoint_estimator_matrix.csv`;
- `tables/shortcut_guard.csv`;
- `figures/feature_nmi_by_estimator.png`;
- `figures/margin_by_estimator.png`;
- `figures/load_vs_feature_nmi.png`;
- `figures/direction_overlap_heatmap.png`.

### Pass Conditions

Route-logit estimator passes if:

- mean \(\Delta \mathrm{feature\_NMI}>0\) over raw and all non-routing controls;
- improvement is not driven by one seed;
- raw route margin improves or becomes less negative;
- nuisance / position / frequency guards do not increase enough to explain the
  gain;
- route-only positive control remains high.

### Fail Conditions

Fail if:

- route-logit subtraction only improves load;
- top-PC/random/load-sensitive controls match route-logit feature NMI;
- selected directions overlap almost entirely with top PCs and have the same
  failure profile;
- direction gains are seed-specific;
- feature NMI improves only through position/frequency/role shortcuts.

### Failure Reasons

- physical prior false: routing common is not captured by relative-logit
  direction scores;
- operationalization false: candidate pool or score is inadequate;
- data boundary: feature geometry is already absent or raw baseline already
  saturates;
- implementation insufficient: hidden states or router rows missing.

## 11. Success / Failure / Insufficient Evidence

**Support:** route-logit subtraction improves feature NMI or raw route margin
over raw, mean, top-PC, random-direction, and load-sensitive controls with
clean nuisance guards.

**Partial support:** route-logit improves only at early checkpoints or only
improves margins but not NMI. Next step would audit rank, sample size, and
whether margin is a better target than NMI.

**Not support:** route-logit subtraction behaves like PCA, random, or load-only
controls. Next step would park common subtraction and return to direct
route-readout / margin-aware center search.

**Insufficient:** required snapshots or leakage guards are missing.

## 12. What This Cannot Claim

This protocol cannot claim real-DCLM semantic features, expert utility,
training preservation, RoPE behavior, or that common subtraction is a final
router initialization method. It also cannot claim success from load balance
alone.

## 13. Review Notes And Protocol Changes

- 2026-06-29: protocol written from the 2026-06-26 research draft.
- The user specifically requested the route-logit estimator scheme and a clear
  explanation of how results update the mechanism.
- 2026-06-29: user approved the experiment and requested a local full run.
  The completed run used 8 seeds, checkpoints `0, 5, 10, 100, 1600`, and all
  protocol conditions. Results are recorded in `summary.md` and `detailed.md`.
