# A06_26 MPI Uniform Feature Router Anchor

## 0. Thinking Card

**Phenomenon:** The Redesign MoE router paper proposes a dynamic spectral
router: align each router row with the corresponding expert's principal
input-side direction through manifold power iteration. A06_25 already showed
that expert spectral directions can become partly feature-aware, but they do
not match route-position centers.

**Mechanism guess:** Dynamic expert-spectrum alignment may amplify the weak
feature bias in expert weights. If that bias is route-relevant, the router
should distribute uniform features to different experts without label-known
route positions. If the expert spectrum is only a high-gain but not
feature-center-aware object, MPI should improve load or NMI only partially and
should leave lower-tail margins negative.

**Key variables:** expert input matrix, router row, manifold power iteration
(MPI), row retraction, scaling constant, route-position hidden state, feature
center, route assignment, margin, max load, slot-start nuisance agreement.

**Causal relation:** Expert-weight power iteration changes the effective
router row before scoring. A valid feature-specialization method must produce
feature-aligned rows with positive margins, not merely high router-expert
spectral alignment.

**Observable metric:** The primary metric is feature-route NMI. The decisive
guard is margin p05, because high NMI with negative lower-tail margin is not a
stable feature-specialization solution.

**Decision:** Use MPI as an audited spectral baseline. Promote it only if it
approaches route-position centers on feature NMI and obtains positive margin
without slot-start leakage.

## 1. Problem Definition

**Parent problem:** A06 studies whether hidden-state geometry and expert
parameter geometry can support label-free feature-level router initialization
and preservation.

**Sharper subproblem:** Decide whether the MPI router from the Redesign MoE
paper is a viable method for uniform feature-to-expert distribution on the
controlled no-position Transformer+MoE slot bridge.

**Terminology / Definitions:**

| Term | Plain meaning | Concrete object or computation | Unit / formula | Why it matters | What it cannot prove |
| --- | --- | --- | --- | --- | --- |
| Uniform feature | Each synthetic feature appears equally often | Four feature ids sampled with probability 0.25 | Probability | Removes frequency skew from the routing question | Real language semantics |
| Route position | The token whose hidden state is audited by the router | Last token of the repeated feature slot | Sequence index | This is the prediction site for the next target token | Automatic route discovery |
| MPI router | Dynamic router row computed from expert weights | Effective row from one power step on expert input matrix | $\hat r_e \propto r_e W_e W_e^\top$ | Tests the paper's spectral-router mechanism | Full paper-scale transfer |
| Row retraction | Normalizing the dynamic row back to a fixed norm | $\hat r_e=C'N^{-1/2}\tilde r_e/\|\tilde r_e\|$ | Logit scale | Separates norm control from feature awareness | Feature alignment by itself |
| Feature NMI | Agreement between feature id and routed expert | NMI(feature id, route) on balanced route-position eval | 0--1 | Primary metric for feature separation | Expert utility |
| Margin p05 | Lower-tail routing safety distance | 5th percentile of matched score minus best competitor | Logit difference | Tests whether the assignment is stable for weak samples | Task loss optimality |
| Max load | Largest fraction routed to one expert | $\max_e P(route=e)$ | 0--1 | Detects expert concentration | Feature identity |
| Router-SVD alignment | Whether router rows follow expert top singular directions | Mean diagonal absolute cosine between effective rows and expert SVD rows | 0--1 | Confirms MPI did what it was designed to do | Feature specialization |
| Slot-start NMI | Agreement between slot start and route | NMI(slot_start, route) | 0--1 | Guards against position shortcut | Absence of all context effects |

**Decision question:** Does MPI-style dynamic expert-spectral routing produce
stable uniform feature-to-expert separation on the no-position slot bridge,
without using label-known route-position centers?

**Not in scope:** real DCLM transfer, proving or disproving the Redesign paper,
semantic expert utility, common/rare imbalance, or long-horizon/nested
objectives.

## 2. Physical Priors

**P1: Expert spectra can contain useful but incomplete feature bias.**  
Reason: A06_25 found that expert SVD becomes more feature-aware after warmup,
especially after common projection.  
Could be wrong if: MPI matches route-position centers with positive margins.

**P2: Retraction controls scale, not feature identity.**  
Reason: normalizing a row can stabilize logits and load, but it does not create
feature-center alignment.  
Could be wrong if: retraction-only performs like MPI and route-position
controls.

**P3: Positive margin is required for preservation.**  
Reason: A06_23 showed that initially correct routing fails when the route
margin is below the finite safe basin.  
Could be wrong if: high NMI with negative margin still preserves feature
identity under longer training, which this anchor does not test.

## 3. Falsifiable Hypotheses

**H1: MPI is enough for uniform feature specialization.**  
Supported if: MPI reaches route-centered feature NMI within `0.05`, has
positive margin p05, balanced load, and near-zero slot-start NMI.  
Weakened if: MPI improves over vanilla but remains far below route-centered
or has negative margin.

**H2: The paper's retraction component is not sufficient by itself.**  
Supported if: retraction-only is close to vanilla and below MPI.  
Weakened if: retraction-only matches MPI.

**H3: Router-expert spectral alignment is not equivalent to feature
specialization.**  
Supported if: MPI has high router-SVD alignment but lower feature NMI and
negative margin compared with route-centered controls.  
Weakened if: router-SVD alignment and feature-margin quality rise together to
the route-centered level.

## 4. Mathematical Model

Let $h_i$ be the route-position hidden state, $f_i$ the feature id, $r_e$ the
learned base router row for expert $e$, and $W_e\in R^{D\times d}$ the
input-side first projection matrix of expert $e$ in this bridge.

The MPI effective row is:

$$
\tilde r_e = r_e W_e W_e^\top,
\qquad
\hat r_e =
\frac{C'}{\sqrt{N}}\frac{\tilde r_e}{\|\tilde r_e\|_2}.
$$

The route score is:

$$
s_e(h_i) = h_i^\top \hat r_e.
$$

For a matched feature-to-expert map $m(f)$, the feature-center margin is:

$$
\gamma_f =
s_{m(f)}(\mu_f) - \max_{e\ne m(f)}s_e(\mu_f).
$$

MPI can be treated as a method candidate only if feature-center and sample
margins are positive, not merely if $\hat r_e$ aligns with the expert top
singular direction.

## 5. Computational Realization

**Data:** The same uniform no-position slot dataset as A06_25. A sequence has
length `32`, neutral tokens `0--31`, feature tokens `32--35`, target tokens
`36--39`, slot starts `2,10,18`, slot lengths `1,2,4,8`, and four balanced
features. The audited route position is the final token in the repeated
feature slot; the training target is the feature-specific token immediately
after the slot.

**Model:** one causal self-attention layer plus one top-1 MoE layer with four
experts. Hidden size `64`, attention heads `4`, expert hidden size `128`.

**Methods:**

- `vanilla`: standard trainable linear router.
- `retract_c1`: row retraction only with $C'=1$.
- `mpi_c1`, `mpi_c2`, `mpi_c4`, `mpi_c8`: MPI with $C'\in\{1,2,4,8\}$.
- `static_svd_init`: static router initialization from initial expert SVD.
- `route_centered_init`: positive control using route-position k-means centers.
- `oracle_centered_init`: upper bound using feature labels for centers.

**Paper/code adaptation:** The Redesign paper code hint and the public
TorchTitan patch implement the same core step: multiply the router row by the
expert first-layer matrix and its transpose, then normalize/retract. This
bridge has a GLU-free expert FFN, so `W_e` is instantiated as the first expert
projection matrix transposed into input space. This is a faithful bridge for
the mechanism, not an exact large-model reproduction.

## 6. Minimal Falsification Tests

| Test | Question | Intervention / comparison | Primary metric | Decision rule | Failure meaning |
| --- | --- | --- | --- | --- | --- |
| MPI vs vanilla | Does dynamic expert spectrum help? | `mpi_c*` vs `vanilla` | feature NMI | Improve by at least `0.05` | Expert spectrum gives no useful routing bias |
| MPI vs route control | Is MPI a finished feature-specialization method? | best `mpi_c*` vs `route_centered_init` | feature NMI and margin p05 | NMI within `0.05` and positive margin | MPI is only partial source bias |
| Retraction ablation | Is normalization alone enough? | `retract_c1` vs `mpi_c1` | feature NMI and margin p05 | Retraction should not match route control | Scale control is not feature awareness |
| Spectral alignment diagnostic | Does the method actually align with expert spectra? | router-SVD cosine | alignment metric | MPI should be high | Low alignment means implementation mismatch |
| Position guard | Is route assignment using slot position? | slot-start NMI | NMI | Near zero | Position shortcut contaminates claim |

## 7. Current Evidence

**Full local two-GPU run completed:** `a06_26_mpi_full_local2gpu_20260703`.
The run used `8` seeds, slot lengths `1,2,4,8`, `160` train steps, and `288`
seed/slot/method cells.

| Method | Feature NMI | Margin p05 | Positive margin fraction | Max load | Effective experts | Slot-start NMI |
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

**Result:** MPI improves over vanilla as $C'$ increases, with best feature NMI
`0.832` for `mpi_c8`. It does not reach route-position centers (`0.979`) and
keeps strongly negative margin p05 (`-15.258`). Retraction-only is close to
vanilla. Slot-start NMI stays near zero.

**Extension result:** All-position initialization plus MPI-c8 does not correct
the mixed hidden-state source. `allpos_centered_init` reaches final feature NMI
`0.818` and margin p05 `-5.602`; `allpos_centered_mpi_c8` reaches NMI `0.830`
but worsens margin p05 to `-20.579`.

**Interpretation:** MPI confirms that expert spectra carry a weak route-relevant
bias in this bridge. However, high router-SVD alignment is not enough for
stable feature specialization: it improves NMI but does not create a positive
margin basin.

**Evidence links:**

- `Projects/from-attention-to-search/main/experiments/A06/A06_26_mpi_uniform_feature_router/summary.md`
- `Projects/from-attention-to-search/main/experiments/A06/A06_26_mpi_uniform_feature_router/detailed.md`
- `Projects/from-attention-to-search/main/experiments/A06/A06_26_mpi_uniform_feature_router/extensions/allpos_mpi/summary.md`
- Redesign paper source: <https://arxiv.org/abs/2606.12397>
- Public code source:
  <https://github.com/ericshwu/Router-with-Manifold-Power-Iteration/blob/main/torchtitan-patches/ttp/models/aoe4.py>

## 8. Claim Boundary And Next Decision

**Can claim:** On the uniform no-position slot bridge, MPI-style dynamic
expert-spectral routing is a useful baseline and improves feature-route NMI
over vanilla, especially at larger $C'$. It does not produce stable uniform
feature-to-expert specialization because its lower-tail margins remain
negative and it stays below the route-position positive control.

**Cannot claim:** The Redesign paper fails, MPI cannot work in its intended
large-model setting, expert spectra contain no feature information, or this
result transfers to real DCLM and common/rare settings.

**Next decision:** Do not replace the nested-learning mainline with MPI. Keep
MPI as a spectral-router baseline, and open the next method anchor around
route-relevant state formation: can nested / long-horizon supervision produce
feature-aware hidden states with positive margins without label-known route
position selection?
