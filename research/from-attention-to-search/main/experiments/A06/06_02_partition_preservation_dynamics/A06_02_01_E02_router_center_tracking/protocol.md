# Protocol: A06_02_01_E02 Router-Center Tracking Preservation

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

## 0. Approval Snapshot

**Approval status:** approved by user and completed locally on 2026-06-26.

**Purpose:** audit how clean feature routing is preserved in the controlled
A06 no-position bridge after feature-center or pseudo-center router
initialization.

**Primary anchor:** A06_02_01_E02 router-center tracking preservation.

**Anchor decision question:** in the controlled setting where feature-center
initialization preserves routing, does the router preserve the partition by
actively tracking feature centers, by staying inside a strong initial margin,
or by drifting through common-direction / norm-dominated effects?

**Anchor physical prior tested:** top-1 dot-product routers define cone-like
partitions over hidden states; a preserved feature partition should leave
feature centers inside the intended router regions over training.

**Anchor core model term tested:** movement and logit relation between router
rows \(w_e(t)\), common-centered route-position feature centers
\(\tilde{\mu}_f(t)=\mu_f(t)-c(t)\), and the common mean \(c(t)\).

**Anchor falsifier:** high final feature-route NMI without feature-specific
row-center tracking or stable margins; or preservation explained primarily by
common-direction projection / row-norm growth.

**Experiment role:** root-cause audit / preservation-mode classification.

**Primary metric from anchor:** matched movement-direction alignment

\[
A_{\mathrm{move}}(t)=
\frac{1}{F}\sum_e
\cos\left(\Delta w_e(t),\Delta \tilde{\mu}_{\pi(e)}(t)\right).
\]

**Claim boundary from anchor:** this protocol can classify the preservation
mechanism in the controlled A06 bridge. It cannot prove real-DCLM preservation,
semantic features, expert utility, or a deployable router initializer.

**Minimal setup:** reuse A06_01_03_E03 corrected no-position bridge checkpoints if
they contain router weights and route-position hidden states; otherwise rerun
the same bridge with additional snapshot logging.

**Basic configuration:** one-layer Transformer + top-1 MoE; 4 experts; route
on the last token of a movable feature slot; no learned absolute positional
embedding; balanced feature id, nuisance id, and slot start.

**Conditions to run / audit:** C0-C3 from A06_01_03_E03; pseudo-center or oracle-center
initialization as successful-preservation conditions; random Gaussian and
equal-norm random initialization as guards; label-shuffled center if available.

**Snapshots required:** step 0 before training, then steps 1, 2, 5, 10, 20, 50,
100, 200, 400, 800, and 1600. Each snapshot must store router rows,
route-position hidden states on the same balanced audit batch, route logits,
route assignments, feature labels, nuisance labels, slot-start labels, target
loss / accuracy, and load.

**Pass:** classify one preservation mode with enough evidence:
active tracking, static margin preservation, random rediscovery, or common /
norm drift.

**Fail:** the audit cannot separate the named rival explanations despite
apparently complete snapshots, or the primary metric contradicts route heatmaps
and margins in a way that exposes the metric as invalid.

**Insufficient:** missing required snapshots, missing random guards, unstable
row-feature matching, or absent route-position hidden states.

**Cannot claim:** real-language behavior, RoPE behavior, semantic features,
utility, or that final NMI alone proves active tracking.

**Approval decision:** approved in chat; full local two-GPU run completed as
`a06_17_02_router_center_tracking_full_20260626_024804`.

## 1. Anchor Alignment

**Decision question:** which geometric mode preserves feature routing after
good router initialization in the controlled A06 bridge?

**Physical prior tested:** if routing is preserved for a feature, its
route-position center should either remain inside a stable router cone or the
corresponding router row should move with the feature-center drift.

**Core model term tested:** \(w_e(t)\) relative to \(\tilde{\mu}_f(t)\) and \(c(t)\).

**Falsifier:** preservation is explained by expert permutation, common
projection, row-norm growth, or random rediscovery rather than feature-specific
tracking / margin.

**Claim boundary:** mechanism audit only for controlled no-position A06 bridge.

## 2. Tested Hypothesis

**H1 active tracking:** initialized router rows move in the same direction as
their matched common-centered feature centers while preserving route NMI.

**H2 static margin preservation:** initialized router rows move little, but raw
route margins and matched router-center dot products remain positive.

**H3 random rediscovery:** random or equal-norm random rows develop the same
tracking / margin profile as center-initialized rows.

**H4 common / norm drift:** row movement or logit growth is dominated by the
global common direction or row-norm growth, not by feature-specific center
tracking.

## 3. Rival Explanations

The protocol explicitly separates:

- active center tracking;
- static margin preservation;
- random rediscovery;
- common-direction drift;
- norm-dominated logit growth;
- expert permutation / matching artifact.

## 4. Data / Model / Algorithm / Objective

**Primary data source:** A06_01_03_E03 corrected no-position synthetic-to-realistic
bridge, C0-C3. C4 is not a preservation condition in this protocol because it
was an all-position discovery audit without same-model training preservation.

**Secondary reference:** A06_01_03_E04 defines the valid state population: route-only
or slot offset 3, the last slot token. All-position hidden states are not used
for center tracking in the primary analysis.

**Model:** same as A06_01_03_E03 canonical run: one-layer Transformer + top-1 MoE,
`d_model=128`, `ffn_dim=256`, 4 experts, 4 heads, sequence length 32, movable
feature slot length 4, route position `slot_start + 3`, no learned absolute
positional embedding.

**Objective:** original A06_01_03_E03 target training objective. The audit does not
change the loss.

**Audit batch:** fixed balanced evaluation batch per cell and seed. It must be
balanced over feature id, nuisance id, and slot start. Use the same batch for
all snapshots within a run so changes over time are not batch artifacts.

## 5. Conditions, Seeds, And Snapshots

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Pseudo-center init, C0-C3 | successful preservation mechanism | active tracking vs static margin | main condition where clean routing is known to preserve | primary | classified as active tracking or static margin with preserved NMI | dominated by common/norm drift | missing snapshots | tracking trajectory, margin table |
| Oracle-center init, if available | upper-bound preservation | same as pseudo-center | checks whether pseudo noise changes motion | secondary guard | same mode as pseudo | different mode without explanation | condition unavailable | mode comparison table |
| Random Gaussian init | random rediscovery | H3 | tests whether good init is mechanism-specific | required guard | does not match center-init tracking/margin profile | matches center-init profile | no comparable run | condition comparison |
| Equal-norm random init | norm confound | norm-dominated routing | separates random direction from norm scaling | required guard if available | lower tracking than center init | same profile as center init | unavailable | norm guard table |
| Label-shuffled center, if available | matching artifact | wrong feature-center prior | tests whether any center-like rows work | secondary guard | fails or tracks wrong centers | succeeds like true centers | unavailable | shuffled guard table |

**Seeds:** use all seeds available from A06_01_03_E03 C0-C3. If rerun is required, use
8 seeds to match A06_01_03_E03.

**Snapshot schedule:** collect the following checkpoints for every cell,
condition, and seed:

```text
step 0: after router initialization, before training update
step 1: after the first optimizer update
step 2: early lock-in check
step 5: early preservation checkpoint
step 10: early preservation checkpoint
step 20: short-window stabilization
step 50: post-early transition
step 100: mid training
step 200: mid training
step 400: late training
step 800: late training
step 1600: final A06_01_03_E03 training endpoint
```

**Snapshot contents:** each snapshot must include:

- full router weight matrix \(W_r(t)\) and row norms;
- route-position hidden states \(h_i(t)\) on the fixed audit batch;
- route logits \(W_r(t)h_i(t)\) and top-1 route assignments;
- feature id, nuisance id, slot start, and route-position index for every
  audit example;
- target loss and accuracy on the audit batch;
- per-expert load and active expert count;
- model step, cell, seed, initialization condition, and checkpoint path.

If any required snapshot content is missing, the result can only be marked
insufficient unless a rerun can reproduce the exact condition.

## 6. Primary Metric

Primary metric:

\[
A_{\mathrm{move}}(t)=
\frac{1}{F}\sum_e
\cos\left(\Delta w_e(t),\Delta \tilde{\mu}_{\pi(e)}(t)\right),
\]

with \(\Delta w_e(t)=w_e(t)-w_e(0)\) and
\(\Delta \tilde{\mu}_f(t)=\tilde{\mu}_f(t)-\tilde{\mu}_f(0)\).

Why it decides: active tracking specifically predicts that router-row movement
aligns with feature-center movement. Raw displacement alone cannot distinguish
tracking from common drift, and final NMI alone cannot distinguish active
tracking from static margins.

Matching rule:

- **Fixed step-0 matching:** match row \(e\) to feature \(f\) at step 0 using
  Hungarian matching on \(w_e(0)^\top \tilde{\mu}_f(0)\). Use this as the main
  trajectory identity.
- **Per-step matching guard:** also compute per-step Hungarian matching. If it
  disagrees with fixed matching, report expert permutation / matching
  instability instead of silently relabeling the trajectory.

Undefined case: if \(\|\Delta w_e(t)\|\) or
\(\|\Delta \tilde{\mu}_{\pi(e)}(t)\|\) is near zero, report movement alignment as
undefined for that row and classify using static-margin metrics.

## 7. Secondary Metrics

**Routing preservation:**

- feature-route NMI;
- per-feature route heatmap;
- active experts and max load;
- target loss and accuracy.

**Router-center dot-product evidence:**

\[
G_{\mathrm{raw}}(t)=
\frac{1}{F}\sum_e
w_e(t)^\top \tilde{\mu}_{\pi(e)}(t)
\]

and cosine-normalized row-center score

\[
G_{\cos}(t)=
\frac{1}{F}\sum_e
\cos(w_e(t),\tilde{\mu}_{\pi(e)}(t)).
\]

**Route margin at feature centers:**

\[
M_f(t)=
\min_{j\neq \pi(f)}
(w_{\pi(f)}(t)-w_j(t))^\top \mu_f(t).
\]

Use raw \(\mu_f(t)\) for this margin because the actual router routes raw hidden
states.

**Common-direction guard:**

\[
A_{\mathrm{common}}(t)=
\frac{1}{E}\sum_e
\cos(\Delta w_e(t),\Delta c(t)).
\]

Also report \(w_e(t)^\top c(t)\) and the common-logit share:

\[
R_{\mathrm{common}}(t)=
\frac{|w_e(t)^\top c(t)|}
{|w_e(t)^\top c(t)|+|w_e(t)^\top \tilde{\mu}_{\pi(e)}(t)|+\epsilon}.
\]

**Norm-growth guard:**

- \(\|w_e(t)\| / \|w_e(0)\|\);
- \(\|\tilde{\mu}_f(t)\| / \|\tilde{\mu}_f(0)\|\);
- \(\|c(t)\| / \|c(0)\|\);
- relation between row-norm growth and common-logit growth.

## 8. Known Good / Known Bad / Known Confusing Cases

**Known good:** A06_01_03_E03 C0-C3 pseudo-center preservation should keep final
feature NMI at 1.0. This is the successful-preservation regime to classify.

**Known bad:** random / equal-norm random should not be assumed to preserve the
same supported feature partition. If they do, the initialization-specific
claim is weakened.

**Known confusing:**

- final NMI is high but fixed step-0 matching and per-step matching disagree;
- router rows barely move, making movement cosine undefined;
- row norm grows and raw dot products improve while cosine alignment does not;
- common projection grows together with router norm;
- feature centers drift little, so active tracking is not observable even if
  preservation is real.

## 9. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| Snapshot audit | Do all required objects exist? | checkpoint files, hidden-state dumps, route logs | pass if every required snapshot field exists | snapshot inventory table | detailed.md |
| Matching audit | Is row-feature identity stable? | fixed and per-step Hungarian maps, route heatmaps | pass if mappings agree or disagreement is explained | matching heatmap | detailed.md |
| Movement audit | Do rows move with centers? | \(A_{\mathrm{move}}\), displacement norms | active tracking if high and defined | movement trajectory | summary.md if decisive |
| Margin audit | Could static margins explain preservation? | \(M_f(t)\), dot products, NMI | static margin if rows move little and margins stay positive | margin trajectory | summary.md if decisive |
| Common/norm audit | Is preservation common or norm dominated? | \(A_{\mathrm{common}}\), \(R_{\mathrm{common}}\), norm ratios | common/norm drift if these dominate feature evidence | common/norm table | summary.md if decisive |
| Guard audit | Does task performance remain valid? | target acc/loss, load, NMI | unclear if routing preserved but task fails | guard table | detailed.md |

## 10. Algorithm Specification

**Input:**

- checkpoints for each cell, seed, and init condition;
- fixed balanced audit batch;
- feature, nuisance, and slot-start labels;
- model code able to emit route-position hidden states and router logits.

**Parameters:**

- center population: route-position states only;
- common estimate: mean route-position hidden state over the fixed balanced
  audit batch at each step;
- feature center estimate: mean route-position hidden state for each feature
  over the fixed balanced audit batch at each step;
- matching: step-0 Hungarian matching as primary trajectory identity.

**Steps:**

1. Load checkpoint at snapshot step \(t\).
2. Run the fixed audit batch and save route-position hidden states, route
   logits, assignments, target loss, and accuracy.
3. Compute \(c(t)\), \(\mu_f(t)\), and \(\tilde{\mu}_f(t)=\mu_f(t)-c(t)\).
4. Extract router rows \(w_e(t)\) and row norms.
5. Compute fixed step-0 row-feature matching and per-step matching guard.
6. Compute primary and secondary metrics.
7. Assign a preservation-mode label per seed and aggregate across seeds.
8. Produce trajectory figures and tables.

**Outputs:**

- `tables/snapshot_inventory.csv`;
- `tables/router_center_metrics_by_step.csv`;
- `tables/preservation_mode_by_seed.csv`;
- `tables/common_norm_guard_by_step.csv`;
- `figures/movement_alignment_trajectory.png`;
- `figures/row_center_dot_product_trajectory.png`;
- `figures/route_margin_trajectory.png`;
- `figures/common_norm_guard_trajectory.png`;
- `figures/route_heatmap_by_condition.png`.

## 11. Success / Failure / Insufficient Evidence

**Active tracking:** center-initialized rows preserve feature NMI and show high
\(A_{\mathrm{move}}\) without common/norm dominance.

**Static margin:** center-initialized rows preserve feature NMI, move little,
and keep positive raw route margins and stable matched dot products.

**Random rediscovery:** random or equal-norm random reaches the same movement,
dot-product, margin, and NMI profile as center initialization.

**Common / norm drift:** common projection or row-norm growth explains raw
logit improvement better than feature-specific movement or margins.

**Failure:** metrics are internally inconsistent after complete snapshots, so
the current operationalization cannot classify preservation.

**Insufficient:** required snapshots or guards are absent.

## 12. What This Cannot Claim

This protocol cannot claim real-DCLM preservation, semantic feature discovery,
expert utility, RoPE behavior, or whole-slot compositional semantics. It also
cannot claim active tracking from final NMI alone, final alignment alone,
cosine alignment alone, or raw movement magnitude alone.

## 13. Review Notes And Protocol Changes

- Initial protocol written after user approved the compressed 06_17_02
  pre-anchor direction.
- User specifically requested clear snapshots and common / norm guards.
- User approved execution after protocol review.
- Full local two-GPU run completed on 2026-06-26 with run name
  `a06_17_02_router_center_tracking_full_20260626_024804`.
