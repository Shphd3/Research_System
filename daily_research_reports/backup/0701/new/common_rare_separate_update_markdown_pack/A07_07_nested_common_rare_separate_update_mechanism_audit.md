# A07_07: Nested Common/Rare Separate-Update Mechanism Audit

Document status: draft anchor for review.

## 0. Thinking Card

**Phenomenon:**  
In nested prediction, common patterns are learned early and repeatedly. Rare or
tail patterns are learned later inside a geometry already shaped by common
high-gain directions. A07_06 showed rare-loss improvement under projected
update suppression, but did not cleanly prove that route-level conflict
reduction caused the gain.

**Mechanism guess:**  
Rare updates are partly absorbed by a common high-gain update subspace. A useful
separate-update implementation should reduce rare update mass inside this common
subspace, while preventing already-easy common examples from continuing to grow
common margins.

**Key variables:**  
common examples $C$, rare/tail examples $R$, frozen common projector $P_C$,
preconditioned update $u_t$, tail common-update fraction
$\alpha^C_{tail}$, tail loss $L_R$, common loss $L_C$, spectral mismatch
$G_{mis}$, route NMI if a routing surface is used.

**Causal relation:**  
If rare failure is caused by update-space reuse of common high-gain modes, then
confidence capping plus common-subspace update suppression should reduce
$\alpha^C_{tail}$, reduce spectral mismatch, improve tail loss, and preserve
common loss better than random capacity or projection-only controls.

**Observable metric:**  
Primary metric is reduction in tail common-update fraction:

$$
\Delta \alpha^C_{tail}
=
\alpha^C_{tail}(\text{ordinary})
-
\alpha^C_{tail}(\text{separate-update})
$$

Required guards: tail loss improvement, common loss stability, projector
stability, spectral mismatch $G_{mis}$, and rare accuracy calibration.

**Rival explanations:**  
Tail loss may improve from capacity, random split, loss reweighting,
regularization, load change, or suppressing useful common information rather
than true separate-update mechanism.

**Decision:**  
Pursue separate-update as a mechanism only if it changes the update mediator
$\alpha^C_{tail}$ and improves tail loss under common-loss guard. If loss
improves without mediator movement, keep as empirical trick, not mechanism. If
mediator moves but loss does not improve, park the implementation.

## 1. Problem Definition

**Parent problem:**  
A07 asks whether common/rare separation has functional value after or within a
controlled preserved partition surface.

**Sharper subproblem:**  
Before returning to real-DCLM utility, decide whether common/rare separate
updating is a valid computational mechanism on a nested controlled surface.

**Decision question:**  
Does separating common and rare update flow reduce tail update reuse of a
common high-gain subspace and improve tail loss without unacceptable common-loss
regression?

**Not in scope:**  
real-DCLM semantic experts, final MoE method, many-expert scaling, or claiming
that rare loss improvement alone proves specialization.

## 2. Physical Priors

**P1: Common examples form a high-gain update channel.**  
Frequent common patterns receive repeated gradient signal and can keep growing
margin after direction alignment is already stable.

**P2: Rare examples are learned inside that geometry.**  
Rare updates may reuse common high-gain modes because these modes give larger
local first-order descent.

**P3: Separate updating must be judged through a mediator.**  
Loss improvement alone is insufficient. The mechanism requires reduced
$\alpha^C_{tail}$ or reduced spectral mismatch.

## 3. Falsifiable Hypotheses

**H1: Tail update absorption exists.**  
Supported if $\alpha^C_{tail}$ is above shuffled/random controls during the
tail-learning window.

**H2: Separate updating redirects tail updates.**  
Supported if confidence capping plus update suppression lowers
$\alpha^C_{tail}$ more than confidence-only or projection-only controls.

**H3: Redirected updates matter functionally.**  
Supported if tail loss improves while common loss remains stable, and the
improvement cannot be explained by random split or capacity.

## 4. Mathematical Model

Let $P_C$ be the frozen common projector and $u_t$ the actual optimizer
update direction.

Tail update concentration:

$$
\alpha^C_{tail}
=
\frac{\|P_C u_{tail}\|^2}{\|u_{tail}\|^2+\epsilon}
$$

Separate update:

$$
\tilde u_t
=
r_t(I-\rho_tP_C)u_t
$$

where $r_t$ is a confidence / residual gate and $\rho_t$ controls common
suppression.

Spectral mismatch:

$$
G_{mis}(k)
=
C_{score}(k)-C_{disc}(k)
$$

where $C_{score}$ measures high-gain-band score mass and $C_{disc}$ measures
correct-vs-distractor discrimination contributed by that band.

**Mechanism relation:**  
If ordinary training lets tail updates reuse common high-gain modes, then
separate updating should reduce $\alpha^C_{tail}$, reduce $G_{mis}$, and
improve $L_R$ with bounded $L_C$ regression.

## 5. Computational Realization

**Input objects:**  
Controlled nested common/rare sequence task with known common and tail labels;
model checkpoints; optimizer states or reconstructable preconditioned updates;
common/tail validation sets.

**Conditions:**

1. ordinary AdamW;
2. confidence-cap only;
3. common-projection update suppression only;
4. confidence-cap + common-projection update suppression;
5. random projector control;
6. random split / same-capacity control;
7. oracle common projector if available.

**Computed variables:**  
$\alpha^C_{tail}$, projector stability, $L_R$, $L_C$, $G_{mis}$,
rare accuracy, common accuracy, update norm, load if router is present.

## 6. Minimal Falsification Tests

| Test | Primary metric | Pass | Fail |
|---|---|---|---|
| Tail update absorption | $\alpha^C_{tail}$ above controls | tail updates reuse common subspace | no absorption; separate update is unnecessary |
| Update redirection | $\Delta \alpha^C_{tail}$ | separate update lowers common-subspace tail update mass | suppression does not move update mediator |
| Functional guard | $L_R$ with $L_C$ stable | tail loss improves without common damage | geometry changes but no functional gain |
| Mechanism specificity | vs random projector / capacity | improvement is specific to common projector | random/capacity explains result |
| Calibration | rare accuracy and $G_{mis}$ | loss gain corresponds to better rare discrimination | loss improves but rare discrimination does not |

## 7. Current Evidence

A07_06 produced a controlled rare-loss positive signal, but route-level conflict
reduction was tiny and the projector was not cleanly identified. Therefore, the
next test should separate confidence gating, update projection, and AdamW
projector variants rather than promote the method.

A09_01 supports the controlled spectral mechanism: common high-gain band can
carry score mass without equivalent rare discrimination, and common/rare split
can reduce the mismatch on controlled data.

## 8. Claim Boundary And Next Decision

**Can claim if supported:**  
On a controlled nested surface, common/rare separate updating reduces tail
common-subspace update reuse and improves tail loss under common-loss and
specificity guards.

**Cannot claim:**  
real-DCLM expert specialization, dense-beating MoE utility, semantic experts,
or that routing conflict reduction is the causal explanation.

**Next decision:**  
If this passes, write a real-DCLM checkpoint-window bridge that applies the same
update mediator to the A06 step 0→5/10 preservation window. If it fails, park
separate updating and return to margin-budget decomposition.
