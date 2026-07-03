# A06_17_05: Margin-Basin Robust Initialization

Document status: result-updated anchor. The full controlled run supports a
wide positive-margin basin around pseudo-center initialization.

## 0. Thinking Card

**Phenomenon:** A06_17_04 showed that exact center initialization has a large
positive margin and that forced boundary crossing breaks the original routing
region. The next question is whether exact centers are necessary.

**Mechanism guess:** There is a positive-margin basin around a good center
row. Initializations inside this basin should preserve feature routing through
early training; initializations outside it should fail or switch.

**Key variables:** pseudo center row $c_e$, perturbed row $w_e(\rho)$,
perturbation strength $\rho$, original feature-to-expert match $e(f)$,
initial margin $M_f(0)$, final margin $M_f(T)$, initial matched-region
preserve fraction, final matched-region preserve fraction, feature NMI.

**Causal relation:** Larger perturbation should reduce initial margin. If the
margin basin exists, preservation should stay high while initial margin is
positive and drop when initial margin becomes small or negative.

**Observable metric:** final matched-region preserve fraction versus minimum
initial margin.

**Rival Explanations:** exact center is required; NMI stays high only because
features remap to other experts; random perturbation changes load but not
feature regions; training re-discovers the partition independent of margin.

**Decision:** support a margin basin if nonzero perturbations preserve the
original matched region whenever initial margin remains positive.

## 1. Problem Definition

**Parent problem:** can route-relevant proxy centers support robust
initialization and preservation?

**Decision question:** Is exact feature-center initialization required, or is
there a positive-margin basin around the center that preserves routing?

**Not in scope:** real-DCLM semantic features, utility, or a deployable
label-free selector.

## 2. Physical Priors

**P1: Router regions are open sets.**  
If a row-center solution has positive margin, small perturbations should not
immediately change its routing region.

**P2: Margin is the basin coordinate.**  
Perturbation size matters mainly through how much initial margin it removes.

**P3: Preservation identity is stricter than NMI.**  
Feature NMI can remain high after an expert permutation; matched-region
preserve fraction is the primary identity-sensitive metric.

## 3. Falsifiable Hypotheses

**H1 margin basin:** nonzero perturbations preserve routing as long as minimum
initial margin stays positive.

**H2 exact-center requirement:** even small perturbations break preservation
despite positive initial margin.

**H3 remapping artifact:** feature NMI stays high but matched-region preserve
fraction drops, meaning the partition is not preserved in the original expert
identity.

## 4. Mathematical Model

Perturb each center row by mixing it with a random unit direction:

$$
w_e(\rho)=\alpha\cdot
\mathrm{normalize}\left((1-\rho)\hat c_e+\rho \hat r_e\right),
$$

where $\rho$ is perturbation strength, $\hat c_e$ is the center row direction,
$\hat r_e$ is a random row direction, and $\alpha$ is the original row norm.

For original match $e(f)$, initial margin is:

$$
M_f(0)=\min_{j\neq e(f)}
(w_{e(f)}(0)-w_j(0))^\top \mu_f(0).
$$

Matched-region preserve fraction is:

$$
P_f(t)=\Pr_{h\in f}\left[\arg\max_e w_e(t)^\top h=e(f)\right].
$$

## 5. Computational Realization

**Data/model:** controlled no-position bridge, C0-C3, slot length 4, route on
last slot token, no B token, uniform feature/nuisance/slot sampling.

**Conditions:** pseudo center rows perturbed at
$\rho\in\{0,0.05,0.1,0.2,0.35,0.5,0.7,1.0\}$ plus oracle center guard at
$\rho=0$.

**Training:** same objective and checkpoints as A06_17_04.

## 6. Minimal Falsification Test

**Primary metric:** final matched-region preserve fraction as a function of
minimum initial margin.

**Pass:** preserve fraction remains high for a nontrivial perturbation radius
and drops when initial margin becomes small or negative.

**Fail:** tiny perturbations break preservation despite positive margin, or
preservation has no relation to initial margin.

**Insufficient:** pseudo discovery fails or base center initialization does not
preserve routing.

## 7. Current Evidence

A06_17_04 showed that forced boundary crossing breaks preservation, but it did
not measure the robust basin around a good initialization.

A06_17_05 full run `a06_17_05_margin_basin_full_20260629_1` tested C0-C3 over
4 seeds. Pseudo-center row perturbations up to `rho = 0.7` preserve perfectly:
final matched-region preserve fraction `1.0`, final feature NMI `1.0`, and
positive final minimum margin (`2.142` at `rho = 0.7`). At `rho = 1.0`, rows
are pure random directions: step-0 margin is already negative (`-1.337`) and
final preserve fraction collapses to `0.219`.

**Interpretation:** exact centers are not required in the controlled bridge.
What matters is staying inside a positive-margin basin.

## 8. Claim Boundary And Next Decision

**Can claim:** exact center rows are not required in the controlled bridge; a
wide positive-margin neighborhood around the centers is enough for
preservation.

**Cannot claim:** real-data feature correctness, semantic expert value, or a
label-free method.

**Next decision:** design a label-free margin acceptance gate that rejects
candidate centers with insufficient pre-training margin.
