# Summary: A06_01_05_E02 MPI Uniform Feature Router

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Protocol:
`protocol.md`

## Result Snapshot

Verdict: MPI improves feature-route agreement over vanilla, but it is not a
stable uniform feature-specialization solution on this bridge.

What was established: The Redesign-style manifold power iteration router
creates a stronger expert-spectral routing bias than a vanilla router. The
best MPI condition, `mpi_c8`, reaches final feature NMI `0.832`, compared with
vanilla `0.686` and retraction-only `0.673`. However, route-position centers
reach `0.979`, oracle centers reach `1.000`, and `mpi_c8` has strongly
negative margin p05 `-15.258`.

What the experiment shows: Dynamic alignment to expert spectral directions is
not equivalent to feature-center-aware routing. MPI can raise feature NMI and
improve load, but it does not form a positive-margin basin for stable feature
assignment.

Extension update: all-position initialization plus MPI-c8 does not solve the
source-selection problem. `allpos_centered_init` reaches final feature NMI
`0.818` with margin p05 `-5.602`; `allpos_centered_mpi_c8` reaches `0.830`
with margin p05 `-20.579`.

What to do next: Keep MPI as a spectral-router baseline and diagnostic. Do not
replace the nested-learning mainline with MPI. The next method anchor should
still target route-relevant state formation with positive margins.

Execution: Full local two-GPU run completed successfully.

- run name: `a06_26_mpi_full_local2gpu_20260703`
- completed cells: `288` seed/slot/method cells
- training rows: `1440`
- seeds: `0--7`
- slot lengths: `1,2,4,8`
- train steps: `160`

## Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| MPI | Router row dynamically moved through expert weights | \(\tilde r_e=r_eW_eW_e^\top\) | Vector | Tests the Redesign paper mechanism | Full paper transfer |
| Retraction | Normalizing the dynamic row to fixed scale | \(\hat r_e=C'N^{-1/2}\tilde r_e/\|\tilde r_e\|\) | Router row | Controls logit scale | Feature awareness |
| Feature NMI | Agreement between feature id and routed expert | NMI(feature, route) | 0--1 | Primary metric for feature separation | Expert utility |
| Margin p05 | Weakest 5% matched route safety distance | 5th percentile of matched score minus best competitor | Logit difference | Decides whether the routing is stable | Task optimality |
| Max load | Largest fraction sent to one expert | \(\max_e P(route=e)\) | 0--1 | Detects expert concentration | Feature identity |
| Slot-start NMI | Agreement between slot position and route | NMI(slot_start, route) | 0--1 | Position leakage guard | All nuisance absence |

## Exact Setup

Data: no-position synthetic slot sequences with four balanced features. The
sequence length is `32`; neutral tokens are `0--31`; feature tokens are
`32--35`; target tokens are `36--39`. Slot starts are balanced over `2,10,18`;
slot lengths are `1,2,4,8`. The route position is the final token of the
feature slot. The model predicts the feature-specific target token after the
slot.

Model: one causal attention layer, one top-1 MoE layer with four experts,
hidden size `64`, four heads, expert hidden size `128`, and one LM head.

Method: the paper and public TorchTitan patch implement MPI by multiplying
each router row through the corresponding expert first-layer matrix and then
normalizing/retracting it. This bridge adapts that operation by using the
first expert projection as the input-side expert matrix \(W_e\) and computing
\(\hat r_e=C'N^{-1/2}r_eW_eW_e^\top/\|r_eW_eW_e^\top\|\) before routing.

Sources: <https://arxiv.org/abs/2606.12397> and
<https://github.com/ericshwu/Router-with-Manifold-Power-Iteration/blob/main/torchtitan-patches/ttp/models/aoe4.py>.

## Main Result

| Method | Feature NMI | Margin p05 | Positive margin frac | Max load | Effective experts | Slot-start NMI |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| vanilla | 0.686 | -3.019 | 0.617 | 0.617 | 2.325 | 0.0005 |
| retract_c1 | 0.673 | -2.170 | 0.594 | 0.609 | 2.255 | 0.0004 |
| static_svd_init | 0.815 | -5.154 | 0.672 | 0.484 | 2.591 | 0.0008 |
| mpi_c1 | 0.705 | -3.047 | 0.609 | 0.609 | 2.288 | 0.0006 |
| mpi_c2 | 0.728 | -5.325 | 0.625 | 0.562 | 2.386 | 0.0006 |
| mpi_c4 | 0.794 | -8.870 | 0.672 | 0.523 | 2.560 | 0.0007 |
| mpi_c8 | 0.832 | -15.258 | 0.711 | 0.500 | 2.708 | 0.0008 |
| route_centered_init | 0.979 | 1.953 | 0.961 | 0.289 | 3.817 | 0.0010 |
| oracle_centered_init | 1.000 | 3.190 | 1.000 | 0.250 | 4.000 | 0.0010 |

Interpretation: MPI has a real effect, because increasing \(C'\) improves
feature NMI from `0.705` to `0.832`. But this improvement is not a solved
routing method: the lower-tail margin remains negative, and the route-centered
positive control is much stronger.

## Key Figures

### Figure: Final Feature NMI

![Final feature NMI by router method](figures/final_feature_nmi_by_method.png)

What this tests: whether each method separates uniform features into different
experts.

Observed result: MPI improves as \(C'\) increases, but it remains below
route-centered and oracle controls.

Take-home: expert spectra provide a partial feature bias, not a finished
feature router.

### Figure: Final Margin Lower Tail

![Final margin p05 by router method](figures/final_margin_p05_by_method.png)

What this tests: whether the weakest feature assignments sit inside a stable
positive-margin basin.

Observed result: only route-centered and oracle-centered controls have positive
margin p05. MPI margins are negative and become more negative with larger
\(C'\).

Take-home: feature NMI alone overstates MPI readiness. The margin guard rejects
MPI as a stable specialization method in this bridge.

### Figure: Feature NMI Trajectory

![Feature NMI trajectory by router method](figures/feature_nmi_trajectory_by_method.png)

What this tests: whether MPI improves through training or only gives an
initial bias.

Observed result: MPI-c8 rises over training, while route-centered and oracle
controls are already high.

Take-home: dynamic spectral alignment can accumulate partial feature agreement,
but it does not close the route-position gap.

## Claim Boundary

Can claim:

- MPI improves uniform feature-route NMI over vanilla on this no-position
  Transformer+MoE bridge.
- Retraction alone does not explain the improvement.
- All-position initialization plus MPI-c8 does not produce stable uniform
  feature specialization in this bridge.
- High router-expert spectral alignment is not sufficient for stable feature
  specialization.
- Position leakage is not the visible explanation, because slot-start NMI is
  near zero.

Cannot claim:

- the Redesign paper fails in its intended setting;
- MPI cannot work at scale;
- expert spectra contain no feature information;
- real-DCLM or common/rare transfer;
- semantic expert utility.

## Next Decision

Treat MPI as a baseline to include when testing future router methods. The
mainline next anchor should still ask whether nested / long-horizon supervision
can form route-relevant hidden states with positive feature margins without
label-known route selection.
