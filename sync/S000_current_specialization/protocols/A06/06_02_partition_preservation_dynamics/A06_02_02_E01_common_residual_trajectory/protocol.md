# Protocol: A06_02_02_E01 Router Common-Residual Trajectory Audit

## 0. Approval Snapshot

**Approval status:** approved for execution by the user's explicit request to
write the protocol, submit the four-GPU full run, and update the hypothesis
after the result.

**Purpose:** decide whether real-DCLM proxy routing collapses because early
router-gap updates move mainly along common-mode directions rather than
feature-residual directions.

**Primary anchor:** `../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/subanchors/06_02_02_common_background_preservation_controls_anchor.md`

**Anchor decision question:** in real-DCLM proxy-init training, are early
router-gap updates dominated by common-mode hierarchy rather than
feature-residual directions, and does that dominance explain proxy-route
collapse?

**Anchor physical prior tested:** top-1 routing is controlled by router-gap
directions. If those gaps update along common directions, fixed proxy labels
can be lost even when feature residual information remains in hidden states.

**Anchor core model term tested:**

$$
\Lambda_{\mathrm{upd}}(t)
=
\operatorname{median}_{f,e}
\frac{
\left|\Delta u_{f,e}(t)^\top P_C\mu_f(0)\right|
}{
\left|\Delta u_{f,e}(t)^\top r_f(0)\right|+\varepsilon
}.
$$

**Anchor falsifier:** proxy-route NMI collapses while router-gap updates are
not common-dominated under multiple common projectors, or the conclusion flips
depending on the common projector.

**Experiment role:** root-cause audit / mechanism decomposition. This is not a
method construction experiment.

**Primary metric from anchor:** common-over-residual router update dominance
ratio $\Lambda_{\mathrm{upd}}$ at steps 5 and 10.

**Claim boundary from anchor:** early real-DCLM proxy-init training only. The
audit can explain the direction of router updates; it cannot prove expert
utility, semantic expert identity, or a final gating method.

**Minimal setup:** reuse the A06_01_04_E03 real-DCLM training configuration, collect
checkpoint hidden states and router rows during training, and compute
common/residual router-gap decompositions for fixed step-0 proxy labels.

**Basic configuration:** DCLM binary token stream, Qwen3-style top-1 MoE,
6 layers, 8 experts, audit layers 3/4/5, model seeds 0/1/2, checkpoints
0/1/2/3/5/10/20/50.

**Conditions to run:** `raw_center` is the primary condition; `random`,
`equal_norm_random`, and `residual_center` are guards inherited from A06_01_04_E03.

**Pass:** `raw_center` has high step-0 proxy-route NMI, collapses by step 5/10,
and shows $\Lambda_{\mathrm{upd}}(5)$ or $\Lambda_{\mathrm{upd}}(10)>1$ under
the robust common projectors, with LM loss comparable to random.

**Fail:** `raw_center` collapses but $\Lambda_{\mathrm{upd}}(5/10)\leq 1`, or
residual update terms dominate while NMI still falls.

**Insufficient:** hidden states, router rows, fixed proxy labels, checkpoint
coverage, or projector robustness checks are missing; decomposition fields are
not finite; or the run does not reproduce A06_01_04_E03's step-0 high NMI and
step-5/10 collapse.

**Cannot claim:** a new gating method, semantic specialization, expert
utility, common-removal success, or long-run pretraining behavior.

**Approval decision:** execute the full four-GPU audit after a smoke run
verifies code path, output schema, and finite decomposition metrics.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Fixed proxy label | The step-0 cluster id used as the target partition during training audit. | $y_i=f$ from raw hidden-state k-means before router initialization. | discrete label | Keeps the same partition while the model trains. | Semantic feature identity. |
| Router gap | Pairwise direction separating the matched expert from a competitor. | $u_{f,e}(t)=w_{a(f)}(t)-w_e(t)$, where $a(f)$ is the step-0 majority expert for proxy label $f$. | vector in hidden dimension | Routing changes when these pairwise directions move. | Expert usefulness. |
| Common projector | A subspace treated as shared or high-gain structure. | $P_C$ from mean direction, top hidden-state PCs, or router-row subspace. | orthogonal projection | Tests whether update direction is dominated by non-feature-specific structure. | That every large or shared direction is harmful. |
| Feature-residual center | Feature center after common projection is removed. | $r_f(0)=(I-P_C)\mu_f(0)$. | vector | Candidate direction carrying proxy-specific contrast. | Functional value. |
| Router update dominance | Whether router-gap updates align more with common terms than residual terms. | $\Lambda_{\mathrm{upd}}(t)$. | ratio | Primary metric deciding H1. | Causality without NMI/loss guards. |
| Proxy-route NMI | Agreement between fixed proxy labels and routed experts. | normalized mutual information between $y_i$ and top-1 route $a_i(t)$. | 0 to 1 | Guard that the run reproduced collapse or preservation. | Expert utility. |
| LM loss | Next-token cross-entropy during training. | standard training loss from A06_01_04_E03 runner. | nats / token-like cross entropy | Guards against calling an optimization crash a routing mechanism. | Specialization quality. |

## 2. Anchor Alignment

**Decision question:** are early real-DCLM router-gap updates common-dominated,
and does this align with proxy-route collapse?

**Physical prior tested:** router movement can preserve a partition only if
the router gaps keep reading residual feature directions rather than common
directions.

**Core model term tested:** $\Delta u_{f,e}(t)^\top P_C\mu_f(0)$ versus
$\Delta u_{f,e}(t)^\top r_f(0)$.

**Falsifier:** collapse occurs without common-dominated update terms under
multiple common projectors.

**Claim boundary:** mechanism audit for the early real-DCLM training window.

## 3. Tested Hypothesis

**H1: common-trajectory hypothesis.** Early router-gap updates in the
`raw_center` condition are dominated by common-mode directions.

**H2: residual-margin insufficiency hypothesis.** Step-0 raw-center routing is
fragile because residual margin is weak even when total proxy-route NMI is
high.

**H3: common-projector robustness hypothesis.** The conclusion is not an
artifact of a single common definition.

## 4. Rival Explanations

- **Weak residual margin:** step-0 NMI is high because the router reads
  common-aligned centers, while residual feature margins are small.
- **Feature-center drift:** hidden feature centers move across fixed router
  boundaries even if router rows do not become common dominated.
- **Router-boundary drift unrelated to common:** router gaps move, but the
  movement is not specifically common aligned.
- **Proxy instability:** fixed step-0 proxy labels are not a stable object
  across training.
- **Objective incompatibility:** ordinary next-token training rewards another
  routing partition even when residual proxy margins exist.
- **Projector artifact:** one common definition creates a false dominance
  ratio.

## 5. Data / Model / Algorithm / Objective

**Data:** the same DCLM binary token stream used by A06_01_04_E03:
`/data/share/109_cache_dir/hf_data/dclm_bin`.

**Model:** the same Qwen3-style real-DCLM top-1 MoE setup as A06_01_04_E03:
6 layers, hidden size 512, 8 experts, one expert per token, router input is
raw hidden states.

**Training objective:** standard next-token cross-entropy. The audit does not
change training loss or routing objective.

**Proxy construction:** for each model seed and layer, fit raw hidden-state
k-means on the calibration split at step 0, then hold the resulting eval
proxy labels fixed for all checkpoints.

**Router initialization:** use A06_01_04_E03 variants. The primary condition is
`raw_center`, where router rows are initialized from normalized raw proxy
centers.

**Audit population:** held-out eval tokens from the same indices at every
checkpoint. The primary layers are 3, 4, and 5.

## 6. Conditions, Seeds, And Checkpoints

Seeds: `0, 1, 2`.

Layers: `3, 4, 5`.

Checkpoints: `0, 1, 2, 3, 5, 10, 20, 50`.

Variants:

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `raw_center` | H1, H2 | main proxy-init collapse | Decisive condition from A06_01_04_E03. | primary | high step-0 NMI, collapse, common-dominated update | collapse without common dominance | missing checkpoints | trajectory and pair tables |
| `random` | guard | ordinary random routing | Provides loss/load and update baseline. | secondary | lower step-0 NMI | raw indistinguishable from random at step 0 | missing | guard table |
| `equal_norm_random` | guard | row-norm confound | Checks whether row norm explains the trajectory. | secondary | behaves like random | beats raw in NMI or loss without mechanism | missing | guard table |
| `residual_center` | guard | common-removal comparison | Tests whether residual-center init changes update dominance. | secondary | lower common dominance or different margins | same collapse with same terms | missing | robustness table |
| mean common projector | H3 | global common offset | Simplest common definition. | secondary | agrees qualitatively | flips conclusion alone | missing | projector table |
| top hidden-PC projector | H3 | high-variance common structure | Tests high-gain hidden directions. | secondary | agrees qualitatively | flips conclusion alone | missing | projector table |
| router-row projector | H3 | router-relative common structure | Tests whether router geometry defines common direction. | secondary | agrees qualitatively | flips conclusion alone | missing | projector table |

## 7. Primary Metric

Primary metric:

$$
\Lambda_{\mathrm{upd}}(t)
=
\operatorname{median}_{f,e}
\frac{
\left|\Delta u_{f,e}(t)^\top P_C\mu_f(0)\right|
}{
\left|\Delta u_{f,e}(t)^\top r_f(0)\right|+\varepsilon
}.
$$

It decides H1 because it directly compares router-gap movement along common
directions versus feature-residual directions. The main decision steps are 5
and 10, because A06_01_04_E03 showed the proxy-route NMI collapse happens in this
window.

False positive cost: a single bad projector may inflate common dominance.
Therefore a pass requires agreement across the robust common projectors and
the NMI/loss guards.

False negative cost: the raw-center collapse could be caused by residual
margin weakness rather than update direction. Therefore residual margins and
sign flips are reported as mechanism guards rather than ignored.

## 8. Secondary Metrics

- proxy-route NMI at each checkpoint;
- matched preserve fraction for step-0 proxy-to-expert matching;
- LM loss;
- max route load and active experts;
- total current margin $\gamma_{f,e}(t)$;
- common margin $\gamma^C_{f,e}(t)$;
- residual margin $\gamma^R_{f,e}(t)$;
- residual margin share;
- sign flip rate;
- feature-center drift term;
- router update common term and residual term;
- projector agreement rate.

## 9. Known Good / Known Bad / Known Confusing Cases

**Known good:** A06_01_04_E03 raw-center step-0 proxy-route NMI should be high in
layers 3/4/5.

**Known bad:** A06_01_04_E03 raw-center proxy-route NMI should fall by steps 5/10
while LM loss remains comparable to random.

**Known confusing:** random and equal-norm random can have large load
concentration, but they do not test proxy preservation because their step-0
proxy NMI is low.

**Known confusing:** a projector can report high common dominance even when it
captures most vector norm. Projector robustness and residual margin share are
required to interpret the ratio.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| Snapshot audit | Are hidden states, logits, routes, labels, and router rows available at every checkpoint? | run inventory | pass if every seed/variant/layer/step has rows | `snapshot_inventory.csv` | detailed.md |
| Reproduction audit | Does the run reproduce A06_01_04_E03 collapse? | `proxy_route_nmi` trajectory | pass if raw-center starts high and collapses by step 5/10 | `router_update_trajectory.csv` | summary.md |
| Projector audit | Are projector bases finite and non-degenerate? | basis rank and norm | fail if rank is zero or NaN | `common_projector_robustness.csv` | detailed.md |
| Pair decomposition audit | Are common/residual terms finite per feature/competitor pair? | pair table | fail if missing or non-finite | `common_residual_margin_by_pair.csv` | detailed.md |
| Decision audit | Does $\Lambda_{\mathrm{upd}}$ align with NMI collapse? | aggregate table and figures | pass/fail by section 12 rules | figures | summary.md |

## 11. Algorithm Specification

### Input

- A06_01_04_E03 training code and DCLM binary data;
- calibration hidden states at step 0;
- held-out eval hidden states and router logits at checkpoints;
- router rows at checkpoints;
- fixed proxy labels from step-0 raw hidden k-means;
- LM loss values from training.

### Parameters

- seeds: `0,1,2`;
- variants: `random`, `equal_norm_random`, `raw_center`, `residual_center`;
- layers: `3,4,5`;
- checkpoints: `0,1,2,3,5,10,20,50`;
- common rank for top hidden-PC and router-row projectors: `4`;
- numerical epsilon: `1e-8`.

### Intermediate Variables

For each seed, variant, layer, checkpoint, proxy label $f$, and competitor
expert $e\neq a(f)$:

$$
\mu_f(t)=\frac{1}{|\{i:y_i=f\}|}\sum_{i:y_i=f}h_i(t),
$$

$$
u_{f,e}(t)=w_{a(f)}(t)-w_e(t),
$$

$$
\Delta u_{f,e}(t)=u_{f,e}(t)-u_{f,e}(0).
$$

For each common projector $P_C$:

$$
\gamma^C_{f,e}(t)=u_{f,e}(t)^\top P_C\mu_f(t),
$$

$$
\gamma^R_{f,e}(t)=u_{f,e}(t)^\top (I-P_C)\mu_f(t),
$$

$$
\Delta \gamma^C_{\mathrm{router}}(t)
=
\Delta u_{f,e}(t)^\top P_C\mu_f(0),
$$

$$
\Delta \gamma^R_{\mathrm{router}}(t)
=
\Delta u_{f,e}(t)^\top (I-P_C)\mu_f(0).
$$

### Steps

1. Initialize model and fixed proxy labels exactly as in A06_01_04_E03.
2. Apply the selected router initialization variant.
3. At each checkpoint, collect held-out hidden states, router logits, route
   assignments, and router rows.
4. Define $a(f)$ as the step-0 majority route for each fixed proxy label.
5. Fit common projectors from step-0 audit data without using target labels
   for projector selection.
6. Compute per-pair common/residual margin and router-update terms.
7. Aggregate by seed, variant, layer, checkpoint, and projector.
8. Render decision figures and write run summary.

### Outputs

- `tables/router_update_trajectory.csv`;
- `tables/common_residual_margin_by_pair.csv`;
- `tables/common_projector_robustness.csv`;
- `tables/snapshot_inventory.csv`;
- `tables/run_config.json`;
- `tables/run_summary.json`;
- `figures/raw_center_lambda_vs_nmi.png`;
- `figures/raw_center_common_residual_update_terms.png`;
- `figures/projector_lambda_step5_step10.png`;
- `figures/proxy_route_nmi_reproduction.png`.

## 12. Success / Failure / Insufficient Evidence

**Support H1:** `raw_center` reproduces A06_01_04_E03 collapse and
$\Lambda_{\mathrm{upd}}(5)$ or $\Lambda_{\mathrm{upd}}(10)>1$ for mean,
top-hidden-PC, and router-row projectors, with common update terms larger than
residual update terms and LM loss comparable to random.

**Weaken H1:** `raw_center` collapses but $\Lambda_{\mathrm{upd}}(5/10)\leq 1`
for the robust projectors, or residual update terms dominate.

**Support H2:** step-0 residual margins are small or sign-fragile despite
high step-0 proxy-route NMI.

**Weaken H2:** step-0 residual margins are strong and collapse is explained
only by later update or center drift.

**Support H3:** the qualitative H1/H2 decision agrees across common
projectors.

**Weaken H3:** the decision flips by projector.

**Insufficient:** the run fails to reproduce A06_01_04_E03, misses checkpoint rows,
has non-finite decomposition values, or only one common projector is valid.

## 13. What This Cannot Claim

This audit cannot claim that common-mode updates causally cause collapse by
themselves; it can only support association within the measured training
trajectory. It cannot claim that common subtraction would fix training, that
long-tail residual directions are useless, that real semantic experts exist,
or that a new gating architecture is validated.

## 14. Review Notes And Protocol Changes

2026-06-30: protocol created from A06_02_02_E01 anchor after the user explicitly
requested the protocol, four-GPU full run, hypothesis update, and meeting
brief.
