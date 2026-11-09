# Protocol: A06_02_01_E06 Margin-Budget Preservation Audit

## 0. Approval Snapshot

**Approval status:** approved for execution by the active goal request to
complete the full run from the 0630 margin-budget documents.

**Purpose:** decide whether early feature-to-expert preservation can be
explained as initial routing margin being consumed by measurable training
drift.

**Primary anchor:** `../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

**Anchor decision question:** can early preservation or collapse be explained
by initial routing margin being consumed by router drift, feature-center drift,
interaction drift, or common-over-residual overwrite?

**Experiment role:** root-cause audit / mechanism decomposition.

**Minimal setup:** controlled no-position A06 bridge; one-layer Transformer +
top-1 MoE; 4 features, 4 nuisances, 4 experts; feature slot length 4; route on
the last token of the slot; movable slot starts; no learned absolute
positional embedding; slot-end target cross-entropy.

**Conditions:** `pseudo_center_init`, `oracle_center_init`,
`random_gaussian_init`, `equal_norm_random_init`,
`label_shuffled_center_guard`.

**Seeds / cells:** 8 seeds (`20260623`-`20260630`) x C0-C3 bridge cells.

**Checkpoints:** `0, 1, 2, 5, 10, 20, 50, 100, 200, 400, 800, 1600`.

**Primary metric:** feature-route NMI at step 5/10.

**Mechanism metrics:** pairwise initial margin, current margin, actual margin
consumption ratio, norm-bound consumption ratio, sign flip rate, router drift
term, feature-center drift term, interaction term, common term, residual term,
cluster-aware margin, target loss, and expert load.

**Pass:** preserved conditions show positive margins, low sign flip, low
actual consumption, and step 5/10 NMI near 1.0; failed/guard conditions show
negative or consumed margins, sign flips, or high common dominance.

**Fail:** NMI falls while center-level and cluster-aware margins remain
positive and consumption is low, or NMI stays high despite widespread sign
flips after strict preserve-fraction guards.

**Insufficient:** hidden states, router rows, fixed feature labels, or
checkpoint route assignments are missing; the script cannot reproduce A06_01_03_E04
positive controls; or the decomposition identity has large numerical error.

**Cannot claim:** real-DCLM behavior, semantic features, expert utility, or a
new initialization method.

## 1. Anchor Alignment

This protocol tests the anchor equation:

\[
\gamma_{f,e}(t)
=
\gamma_{f,e}(0)
+
\Delta u_{f,e}(t)^\top \mu_f(0)
+
u_{f,e}(0)^\top \Delta \mu_f(t)
+
\Delta u_{f,e}(t)^\top \Delta \mu_f(t).
\]

The full run must verify that the computed right-hand side reconstructs the
current margin up to numerical tolerance.

## 2. Data And Model

Use the same controlled bridge family as A06_02_01_E02/A06_02_01_E03:

- balanced feature id, nuisance id, and slot start;
- feature slot token length 4;
- route and evaluation on the last token of the feature slot;
- no B token;
- no learned absolute positional embedding.

The model is a one-layer Transformer with one top-1 MoE block and 4 experts.
Training objective is slot-end target cross-entropy.

## 3. Algorithm

For each seed, cell, condition, and checkpoint:

1. collect held-out route-position hidden states and router rows;
2. compute feature centers \(\mu_f(t)\) and common center
   \(c(t)=\frac{1}{F}\sum_f \mu_f(t)\);
3. compute residual centers \(r_f(t)=\mu_f(t)-c(t)\);
4. fix the step-0 feature-to-expert matching \(a(f)\);
5. compute every pairwise competitor margin
   \(\gamma_{f,e}(t)\) for \(e\neq a(f)\);
6. compute router drift, feature drift, interaction drift, norm-bound budget,
   actual consumption ratio, sign flip, common term, residual term, and
   cluster-aware margin;
7. aggregate by condition, step, seed, and cell.

## 4. Known Good / Bad / Confusing Cases

**Known good:** pseudo-center and oracle-center should preserve feature NMI
near 1.0 in the controlled bridge.

**Known bad:** random Gaussian and equal-norm random should be less stable and
often have negative margins or lower preserve fraction.

**Known confusing:** label-shuffled center can have center-like norms but
wrong matching; it guards against claiming norm or center magnitude is enough.

**Known confusing:** norm-bound consumption may be conservative. If it is too
loose, actual consumption ratio and cluster-aware margin decide the
interpretation.

## 5. Output Tables

- `margin_budget_by_pair.csv`: every feature/competitor pair at each snapshot.
- `margin_budget_metrics_by_step.csv`: per seed/cell/condition/step aggregate.
- `margin_budget_metric_aggregate.csv`: aggregate by condition and step.
- `condition_final_margin_budget.csv`: final row per seed/cell/condition.
- `condition_final_margin_budget_aggregate.csv`: final aggregate table.
- `drift_attribution_final.csv`: final drift-term attribution.
- `common_residual_final.csv`: final common/residual decomposition.
- `snapshot_inventory.csv`: run coverage and protocol compliance.

## 6. Central Figures

- feature-route NMI trajectory;
- actual consumption ratio trajectory;
- margin trajectory;
- sign flip trajectory;
- final drift attribution;
- common versus residual final terms;
- final NMI versus actual consumption scatter.

## 7. Result Interpretation Rules

**Support H1:** high NMI aligns with positive margins, low sign flips, and low
actual consumption; guards fail when initial or current margins are negative.

**Support H2:** router drift term is the largest negative contributor in
fragile or failed conditions.

**Support H3:** feature-center drift term is the largest negative contributor.

**Support H4:** common term grows relative to residual term and coincides with
load concentration or route failure.

**Revise model:** route failure appears without center-level or token-level
margin loss, suggesting expert feedback, objective mismatch, or missing
hidden-state population.

## 8. Execution Plan

Run a smoke first on a small condition subset. If the decomposition identity
passes and figures render, run the full two-GPU local audit with two shards and
aggregate. Then copy curated tables/figures into the project experiment folder
and write `summary.md` plus `detailed.md`.
