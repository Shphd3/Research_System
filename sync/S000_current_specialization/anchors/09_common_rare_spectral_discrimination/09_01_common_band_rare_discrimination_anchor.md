---
anchor_id: A09_01_common_band_rare_discrimination
parent_node: rq.expert_specialization
status: controlled_supported
created: 2026-06-29
canonical_language: en
companion_cn: 09_01_common_band_rare_discrimination_anchor_cn.md
source_docs:
  - ../../../../../daily_research_reports/0629/docs/nested_prediction_spectral_anisotropy_causal_rewrite_v4.md
  - ../../../../../daily_research_reports/0626/recordings/r1.md
  - ../06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/subanchors/06_01_06_spectral_reservoir_method_audit_anchor.md
---

# A09_01 Common High-Gain Band / Rare Discrimination Anchor

## 0. Thinking Card

**Phenomenon:** Common features can form high-gain directions. Rare information may still exist, but prediction can be dominated by the common direction.

**Mechanism guess:** The high-gain band contributes much of the score, but not necessarily the correct discrimination. The rare residual band is smaller, but may better separate the correct target from a common distractor.

**Key variables:** High-gain band, residual band, correct target, common distractor, rare loss, MoE split.

**Causal relation:** A large but weakly discriminative common band raises common distractor scores and suppresses rare-correct targets. A useful MoE split should reduce this mismatch.

**Observable metric:** Mismatch gap: high-gain score share minus high-gain discrimination share.

**Rival explanations:** Rare loss improvement may come from capacity, random splitting, load changes, or regularization rather than common/rare specialization.

**Decision:** Continue this mechanism only if the MoE split both lowers the mismatch gap and improves rare loss. Otherwise, park the method claim and keep the diagnostic.

## 1. Problem Definition

**Parent problem:** Real MoE specialization needs functional value, not just route-label similarity.

**Sharper subproblem:** Test whether a common high-gain band suppresses rare discrimination, and whether MoE splitting actually reduces this failure.

**Decision question:** Is the common high-gain band large but weakly discriminative, and can an effective MoE split reduce that mismatch?

**Not in scope:** Real semantic experts, a final method, long training, or scaling claims.

## 2. Physical Priors

**P1: A common high-gain band may dominate scores.**
Meaning: Common-feature directions can amplify output or attention scores.
Could be false if the high-gain band is also the strongest source of correct discrimination.

**P2: Rare information may be smaller but more discriminative.**
Meaning: Rare relations may live in the residual band; their scores are smaller, but they separate the correct target from the distractor.
Could be false if rare discrimination also comes mostly from the high-gain band.

**P3: Method gain must move the mechanism metric.**
Meaning: Rare loss improvement is not enough; the mismatch metric must also change.
Could be false if the mismatch gap is unrelated to rare loss.

## 3. Falsifiable Hypotheses

**H1:** Failed rare examples have a positive mismatch gap.
Supported if the high-gain band has high score share but low discrimination share.
Weakened if the high-gain band already provides correct discrimination.

**H2:** A useful common/rare split reduces the mismatch gap.
Supported if the split lowers both the mismatch gap and rare loss, while a same-capacity random split does not.
Weakened if rare loss improves but the mismatch gap does not move.

## 4. Mathematical Model

**Objects:** Hidden state $h$, readout matrix $W$, high-gain-band projector $P_k$, correct target $y$, common distractor $d$.

**Core decomposition:** Split the output score into high-gain and residual parts.

$$
z = W P_k h + W(I-P_k)h = z^{top}+z^{res}.
$$

**Mechanism metric:** Measure the "large score but weak discrimination" mismatch.

$$
G_{mis}(k)=C_{score}(k)-C_{disc}(k).
$$

$C_{score}(k)$ is the share of total score magnitude coming from the high-gain band.

$C_{disc}(k)$ is the share of correct-target-versus-distractor discrimination coming from the high-gain band.

**Falsifier:** The split improves rare loss but $G_{mis}(k)$ does not decrease, or a random split decreases it just as much.

## 5. Computational Realization

**Input objects:** Controlled nested data with known common and rare directions.

**Computed variables:** High-gain band, residual band, common distractor margin, rare loss, and comparison table across split conditions.

**Algorithm stages:** Train baseline -> decompose scores -> measure mismatch -> test split and controls.

**Stage-local evidence:** Score-share curve, discrimination-share curve, rare-loss table, capacity control.

**Expected artifacts:** `protocol.md`, `summary.md`, `detailed.md`, one main figure, one compact table.

## 6. Minimal Falsification Test

**Test:** Controlled common/rare spectral mismatch audit.

**Question:** Does the common high-gain band take a large score share without contributing comparable rare discrimination?

**Intervention / comparison:** Shared model, common/rare split, same-capacity random split, and oracle split.

**Primary metric:** Change in $G_{mis}(k)$ on matched rare examples.

**Pass / fail / insufficient:** Pass if the baseline mismatch gap is positive and the split lowers both mismatch and rare loss. Fail if there is no mismatch, or if the random split explains the gain. Insufficient if the common/rare directions are not auditable.

**Failure means:** The proposed common-band suppression mechanism has not been identified.

## 7. Current Evidence

**Result A09_01:** Supported on controlled synthetic data. At audit rank 4, the shared baseline has $G_{mis}=0.486$ with $C_{score}=0.819$ and $C_{disc}=0.332$. The estimated common/rare split reduces $G_{mis}$ to approximately zero, improves rare loss by 0.996, and preserves system common loss.

**Control:** The same-capacity random split improves rare loss more, but does not reduce mismatch and fails common preservation. This keeps the capacity explanation alive for rare loss alone, but not for the full mechanism pattern.

**Guard:** Shuffling rare labels also removes mismatch after projection, but rare loss gets worse. This shows mismatch reduction alone is not sufficient evidence.

**Observation:** `A06_01_06_E01/E02` support a controlled result: a stable direction can be converted into routing.

**Observation:** `A06_01_06_E03` and A07_06 warn that loss improvement alone can misidentify the mechanism.

**Observation:** A06 shows initialization can be made to work, but ordinary training does not preserve it on real DCLM.

**Interpretation:** The next question should test the common/rare functional mechanism, not only initialization.

**Boundary:** This is controlled-data evidence only. No real-data claim yet.

## 8. Claim Boundary And Next Decision

**Current supported claim:** On controlled data, common high-gain dominance is a measurable rare-discrimination failure mode, and an estimated common/rare split can reduce that mismatch while preserving common behavior.

**Cannot claim:** Real semantic experts, deployable MoE, or real-DCLM utility.

**Next decision:** Test whether an analogous $C_{score}$ / $C_{disc}$ mismatch can be measured on real model states or realistic proxy rare targets.
