---
story_id: A15_spectral_representation_to_functional_routing
status: current_primary_synthesis
updated: 2026-08-09
canonical_language: en
companion_cn: 02_spectral_representation_to_functional_routing_cn.md
---

# From Spectral Representation Geometry To Functional Routing

## 1. The Organizing Question

A15 asks three questions in order:

1. Which spectral coordinates exist and are accessible?
2. What representation information, if any, is reproducibly carried by a
   named coordinate?
3. Does selecting that information improve routing under matched functional
   controls?

The order is a claim boundary, not a chronology. A geometric pattern cannot
skip the information test, and an information pattern cannot skip functional
admission.

## 2. Three Coordinate Systems

The line uses three matrices that must not be conflated:

$$
C^{router}=\operatorname{Cov}(x^{router}),\qquad
C^{rep}=\operatorname{Cov}(z),\qquad
K_\ell=W_{gate,\ell}^{\top}W_{gate,\ell}+W_{up,\ell}^{\top}W_{up,\ell}.
$$

$C^{router}$ defines what a linear Gate can access in its actual input.
$C^{rep}$ describes variation in one explicitly named activation object, such
as a residual state or the actual MLP-input increment $\Delta n$.
$K_\ell$ defines one layer's local MLP-input parameter geometry. Equal rank in
two layers is not direction identity.

## 3. What Is Established

### 3.1 Router-input geometry is non-uniform but not universally head-only

[A15_00](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_00_router_input_spectral_geometry/15_00_router_input_spectral_geometry_anchor.md)
establishes that Router-input covariance is a useful access geometry. The
actual-input and onset tests bound a strong but qualified head preference,
while the common/residual tests show transferable and condition-local
structure. This is evidence about access and Gate preference, not semantic
function.

### 3.2 A controlled learning-speed mechanism exists; real formation remains bounded

[A15_01](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_01_spectral_learning_and_feedback_dynamics/15_01_spectral_learning_and_feedback_dynamics_anchor.md)
contains the controlled covariance-driven finite-time learning result. The
real-trajectory comparison is insufficient because the load guard failed
before a valid formation verdict. Selected-expert feedback can lock in a
head-first partition in its controlled setting, while low variance delays but
does not randomize a learnable route. These results explain possible dynamics;
they do not identify useful semantic coordinates.

### 3.3 Layerwise semantic objects change with depth without yielding one universal rank coordinate

[A15_02](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/15_02_layerwise_representation_spectral_atlas_anchor.md)
collects controlled and natural hierarchy atlases, attention-head and channel
concentration audits, MLP-parameter geometry, and matched semantic-complexity
tests. Several named objects show depth-dependent readability or variance
profiles. The evidence does not validate “later rank” or “middle/tail” as a
universal semantic hierarchy coordinate, and it does not define
compositionality by depth, effective rank, or band position.

## 4. The Two Independent Band Questions

### 4.1 Middle band

[A15_03](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_03_middle_band_information/15_03_middle_band_information_anchor.md)
asks whether the apparently least-changing normalized F2--F8 curve reflects
real stability or one of three rivals: total-variance normalization,
within-middle left/right cancellation, or unstable layer-local directions
erased by rank averaging. Its draft fixes one 512-example bank and actual
$\Delta n$, and compares absolute per-direction variance, normalized share,
within-middle rank curves, and local/shared capture against matched Haar
spaces. It is independent and `DRAFT_NOT_EXECUTABLE`.

### 4.2 Tail band

[A15_04](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_04_tail_band_information/15_04_tail_band_information_anchor.md)
asks whether a target-common local-rank relocation enters a cross-layer shared
F9--F16 orientation. Its controls distinguish shared tail geometry from local
rank relocation and dimension alone. It is the active draft, remains
`DRAFT_NOT_EXECUTABLE`, and makes no functional claim.

Middle and tail are sibling parent questions. Neither is a control arm or
mechanistic clause of the other.

## 5. Functional Admission Is A Separate Gate

[A15_05](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_05_functional_coordinate_admission/15_05_functional_coordinate_admission_anchor.md)
owns capability, compatibility, and matched-dispatch evidence. The shallow
pilot was capability-insufficient; the fixed-band cross-update compatibility
test found no admissible candidate; the matched 2B dispatch test changed
routing distributions without passing the registered quality claim. An older
conditional training Protocol was therefore never run and is archived.

The current functional conclusion is negative only at these registered
interfaces: A15 has not shown that selecting middle or tail information gives
a model-quality gain. It has not shown that no spectral routing method can
work.

## 6. Online Routing Does Not Back-Prove Band Meaning

[A15_06](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_06_online_spectral_routing_and_relay/15_06_online_spectral_routing_and_relay_anchor.md)
owns online spectral routing, relay, the local-random identity control, and the
single-seed extension. Those records evaluate an online method under their
own contracts. Their outcomes cannot be used backward to declare that a
middle or tail band carries a stable semantic function.

## 7. Mathematical And Theorem State

There is no theorem that orders semantic usefulness by spectral rank. The
controlled learning result supports a finite-time mechanism under its frozen
assumptions; it is not a theorem about trained Transformers. The current
middle and tail objects are empirical subspaces with matched random controls,
not invariant modules.

## 8. Current Boundary And Next Anchor Decision

The bounded line claim is:

> Spectral geometry constrains access and learning, and layerwise
> representations vary non-uniformly in named spectral coordinates; the
> identity and routing utility of middle/tail information remain unresolved.

The one next decision is whether to approve or correct the A15_04 primary
metric, resampling design, and conjunctive verdict rule. Only after that
geometry decision should the line choose between reopening A15_03 or advancing
a named coordinate to A15_05 functional admission.
