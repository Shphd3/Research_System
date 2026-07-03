# A06_25 Warmup Spectral Router Reinitialization Anchor

## 0. Thinking Card

**Phenomenon:** A06_24 shows that all-position clustering at step 0 is not a
reliable route initializer. A live rival explanation is that step-0 hidden
states and expert parameters are too unformed, so clustering or expert spectral
directions may become useful only after a short warmup.

**Mechanism guess:** Early training may create feature-aware geometry in hidden
states or expert input directions. If so, delayed router reinitialization from
warmup geometry should improve uniform feature-to-expert assignment. If not,
all-position clustering and expert top singular vectors are wrong objects for
feature routing, even after warmup.

**Key variables:** warmup step, hidden-state pool, expert input-side top
singular direction, router row, feature center, common/mean direction, feature
route assignment, margin, slot-start nuisance agreement.

**Causal relation:** Warmup can increase feature awareness in a candidate
geometry. Router rows reinitialized from a feature-aware geometry should raise
feature NMI and positive route margin; rows from common-aligned, near-parallel,
or feature-unaware directions should not.

**Observable metric:** The primary metric is feature-route NMI on balanced
route-position evaluation. Required guards are matched preserve fraction,
margin p05, max load, target accuracy, and slot-start NMI.

**Rival Explanations:** all-position failure may come from untrained hidden
states, wrong hidden-state population, position shortcut, current-router
feedback lock-in, expert singular directions being too similar, expert singular
directions aligning with common structure, or expert singular directions not
being feature-aware.

**Decision:** If warmup all-position clustering or warmup expert singular-vector
initialization approaches route-position clustering without position leakage,
promote delayed reinitialization as a method candidate. Otherwise keep
route-relevant state selection and margin preservation as the main bottlenecks.

## 1. Problem Definition

**Parent problem:** A06 studies whether uniform features can be routed to
different experts and preserved through training.

**Sharper subproblem:** Decide whether failed all-position and expert-spectral
initializations fail because geometry is unformed at step 0, or because those
geometries are not route-relevant / feature-aware.

**Terminology / Definitions:**

| Term | Plain meaning | Concrete object or computation | Unit / formula | Why it matters for the current decision | What it cannot prove |
| --- | --- | --- | --- | --- | --- |
| Uniform feature | Each synthetic feature appears equally often | Four feature ids sampled with probability 0.25 each | Probability | Keeps the question about routing geometry rather than frequency skew | Real language semantics |
| Route position | Task-relevant routed token | Last token of the repeated feature slot | Sequence index | Evaluation should be tied to the prediction site | A real route selector |
| All-position pool | Hidden states from every token position | Background, slot, and target-adjacent positions together | Set of vectors | Tests whether global hidden geometry is usable | Route relevance |
| Expert top singular direction | Main input direction of an expert FFN | Top right singular vector of the expert's first linear layer | Unit vector | Tests whether expert parameter geometry can initialize the router | Expert utility |
| Warmup | Short training before router reinitialization | Train the same no-position Transformer-MoE for 10 or 40 steps | Steps | Tests whether geometry becomes feature-aware after early learning | Long-run convergence |
| Feature NMI | Agreement between feature id and routed expert | NMI(feature id, route) on balanced route-position eval | 0--1 | Primary metric for uniform feature separation | Expert functional value |
| Matched preserve fraction | Fraction routed to the step-0 matched expert for its feature | Mean of assign == mapping(feature) | 0--1 | Detects identity preservation after reinit | Semantic utility |
| Margin p05 | Lower-tail matched route margin | 5th percentile of matched score minus best competitor | Logit difference | Tests whether the assignment is in a stable basin | Loss optimality |
| Slot-start NMI | Agreement between slot start and route | NMI(slot_start, route) | 0--1 | Position shortcut guard | Absence of all context effects |

**Decision question:** After a short warmup on the same no-position uniform
slot dataset, do all-position hidden-state clustering or expert top singular
directions become feature-aware enough to initialize router rows for uniform
feature distribution?

**Not in scope:** real DCLM transfer, semantic experts, deployable MPI router,
common/rare frequency imbalance, or proving spectral routing impossible.

## 2. Physical Priors

**P1: Early training may form feature geometry.**  
Meaning: hidden states and expert input directions at step 0 can be too random,
while step 10/40 may expose feature-relevant directions.  
Could be wrong if: warmup all-position or expert-spectral rows still do not
improve feature NMI or margin.

**P2: All-position geometry can remain the wrong population.**  
Meaning: even after warmup, all token positions can mix route and non-route
states, so the clustering objective may not serve route-position routing.  
Could be wrong if: warmup all-position clustering matches route-position
clustering with low slot-start NMI.

**P3: Expert top singular directions may be high-gain but not feature-aware.**  
Meaning: expert spectral directions can be near-parallel, common-aligned, or
locked to current router feedback instead of feature centers.  
Could be wrong if: warmup expert singular initialization approaches
route-position clustering and its diagnostics show low common alignment and
positive feature-center margins.

## 3. Falsifiable Hypotheses

**H1: Warmup rescues all-position hidden-state clustering.**  
Supported if: warmup all-position centered clustering improves strongly over
step-0 all-position and approaches warmup route-position clustering on feature
NMI and margin p05.  
Weakened if: warmup all-position remains far below route-position / oracle.

**H2: Expert top singular directions fail because they are not feature-aware.**  
Supported if: raw, orthogonalized, and common-projected expert SVD rows remain
low feature NMI or negative margin, while diagnostics show weak feature-center
alignment.  
Weakened if: one spectral correction closes the gap to route-position
clustering.

**H3: Warmup can make expert spectral directions usable.**  
Supported if: expert SVD initialization improves from warmup 0 to warmup 10/40
and gains positive margin without slot-start leakage.  
Weakened if: expert SVD rows mostly track current router feedback, common
alignment, or row similarity rather than feature centers.

## 4. Mathematical Model

**Objects:** route hidden state $h_{i,p}$, feature id $f_i$, route-position
feature center $\mu_f^{(k)}$, all-position mean $c_{\mathrm{all}}^{(k)}$,
expert first-layer matrix $A_e^{(k)}$, expert top input singular vector
$v_e^{(k)}$, router row $w_e$.

**Core decomposition:**

$$
h_{i,p}^{(k)} = c_{\rho(p)}^{(k)} + r_{f_i,p}^{(k)} + \eta_{i,p}^{(k)}.
$$

$$
A_e^{(k)} = U_e^{(k)}\Sigma_e^{(k)}V_e^{(k)\top},\qquad
v_e^{(k)} = V_e^{(k)}[:,1].
$$

**Mechanism relation:** Warmup helps only if candidate rows have positive
feature-center margins:

$$
\gamma_f^{(k)} =
w_{m(f)}^\top\mu_f^{(k)} -
\max_{e\ne m(f)}w_e^\top\mu_f^{(k)} > 0.
$$

**Observable metrics:** feature NMI, matched preserve fraction, margin p05,
row pairwise cosine, common alignment, feature-center alignment, max load,
target accuracy, and slot-start NMI.

**Falsifier:** warmup all-position or warmup expert SVD reaches route-position
feature NMI and positive margin while slot-start NMI remains low.

## 5. Computational Realization

**Input objects:** no-position synthetic slot sequences with four uniformly
sampled features, repeated feature slots, neutral background tokens, and
feature-specific target tokens.

**Computed variables:** warmup hidden states, all-position centers,
route-position centers, oracle centers, expert top singular vectors, corrected
spectral rows, route assignments, margins, and spectral diagnostics.

**Algorithm stages:**

1. Warm up the same no-position Transformer-MoE for 0/10/40 steps.
2. Extract hidden states and expert input singular directions.
3. Reinitialize router rows from all-position centers, route-position centers,
oracle centers, raw expert SVD rows, orthogonalized SVD rows, or
common-projected SVD rows.
4. Evaluate immediate routing and train after reinitialization.
5. Compare feature NMI, margin, load, and nuisance agreement.

**Stage-local evidence:** data audit, immediate reinit routing, final routing,
trajectory, spectral diagnostics, and central figures.

**Expected artifacts:** `protocol.md`, `summary.md`, `detailed.md`, tables,
figures, local 2-GPU run log, and meeting brief.

## 6. Minimal Falsification Tests

| Test | Question | Intervention / comparison | Primary metric | Pass / fail / insufficient | Why it decides | Failure means |
| --- | --- | --- | --- | --- | --- | --- |
| Warmup hidden clustering | Does early training rescue all-position clustering? | step-0 vs warmup all-position centered, with route-position as positive control | feature NMI and margin p05 | Pass if warm all-position approaches route-position; fail if it remains low | Distinguishes unformed representation from wrong population | Falsifies warmup-all-position operationalization |
| Expert SVD failure decomposition | Why does expert spectral init fail? | raw, orthogonalized, and common-projected SVD rows | feature NMI plus spectral diagnostics | Pass if a correction identifies the failure mode; fail if all remain feature-unaware | Separates row similarity, common alignment, and feature-unawareness | Falsifies naive expert-SVD router init |
| Warmup expert SVD | Does expert parameter geometry become route-aware after warmup? | expert SVD rows at warmup 0/10/40 | feature NMI and margin p05 | Pass if warmup SVD improves without slot leakage; fail if not | Tests MPI-like prerequisite | Falsifies this spectral source, not all spectral routers |

## 7. Current Evidence

**Observation before the run:** A06_24 showed that all-position clustering was
weaker than route-position / oracle centers on the trained no-position
Transformer-MoE surface. A06_23 showed that even initially correct routing
fails when the margin buffer is too thin. The 0703 MPI/spectral-router reading
motivated auditing whether spectral directions are feature-aware or
common-dominated before using them as router rows.

**Result after full local 2-GPU run:** Warmup improves both all-position
clustering and expert SVD feature awareness, but it does not close the
route-position gap. Immediate feature NMI for all-position clustering improves
from `0.774` at warmup 0 to `0.876` at warmup 40, while route-position
clustering reaches `0.996`. Raw expert SVD improves to `0.879` at warmup 40,
and common-projected expert SVD reaches `0.943` with positive immediate margin
p05 `0.514`. Orthogonalized expert SVD performs worse (`0.704` NMI and
`-5.311` margin p05 at warmup 40).

**Interpretation:** The "step-0 geometry is unformed" explanation is partly
right, but it is not enough. Route-relevant state selection remains the main
bottleneck. Expert spectral directions are not useless after warmup, but naive
SVD rows require common-alignment, feature-awareness, and margin audits before
becoming method candidates.

**Boundary:** This evidence does not validate a deployable spectral router and
does not transfer to real DCLM. It only establishes source quality on the
uniform no-position slot bridge.

**Evidence links:**

- `Projects/from-attention-to-search/main/experiments/A06/A06_24_synthetic_common_rare_transformer_moe/summary.md`
- `Projects/from-attention-to-search/main/experiments/A06/A06_23_top1_lockin_margin_threshold/summary.md`
- `Projects/from-attention-to-search/main/experiments/A06/A06_25_warmup_spectral_router_reinit/summary.md`
- `Projects/from-attention-to-search/main/experiments/A06/A06_25_warmup_spectral_router_reinit/detailed.md`
- `daily_research_reports/0703/docs/moe_0703.md`

## 8. Claim Boundary And Next Decision

**Can claim after this run:** warmup makes all-position hidden states and
expert SVD directions more feature-aware on the uniform no-position slot
dataset, but route-position centers remain the strongest tested source.
Common-projected expert SVD is the best tested spectral candidate, while simple
orthogonalization is not the fix.

**Cannot claim:** real DCLM transfer, semantic experts, final MPI router
validity, or spectral routing impossibility.

**Next decision:** Do not promote all-position delayed reinitialization or raw
expert SVD as a finished method. Open a nested-learning aligned anchor that
tests whether multi-token / long-horizon supervision can make route-relevant
hidden states feature-aware earlier and with thicker routing margins.
