# Protocol: A09_01 Common High-Gain Band / Rare Discrimination

## 0. Approval Snapshot

**Approval status:** Approved by user on 2026-06-29; start execution.

**Purpose:** Test whether the common high-gain direction dominates score while rare directions carry the decisive discrimination.

**Primary anchor:** `../../../problem_anchors/09_common_rare_spectral_discrimination/09_01_common_band_rare_discrimination_anchor.md`

**Anchor decision question:** Is the common high-gain band large but weakly discriminative, and can an effective MoE split reduce that mismatch?

**Anchor physical prior tested:** Common features can create a high-gain score band; rare residual directions can be smaller but more discriminative.

**Anchor core model term tested:** $G_{mis}(k)=C_{score}(k)-C_{disc}(k)$.

**Anchor falsifier:** Rare loss improves but $G_{mis}(k)$ does not decrease, or a same-capacity random split explains the same gain.

**Experiment role:** Mechanism audit, not method proof.

**Primary metric from anchor:** $\Delta G_{mis}=G_{mis}^{baseline}-G_{mis}^{split}$ on matched rare examples.

**Claim boundary from anchor:** Controlled-data mechanism only; no real semantic expert or real-DCLM utility claim.

**Minimal setup:** Synthetic nested common/rare data with known directions, matched rare target/distractor pairs, and four model conditions.

**Conditions to run:** Shared baseline, common/rare split, same-capacity random split, oracle split, plus shuffled-rare-label guard.

**Pass:** Baseline rare failures have positive $G_{mis}$; common/rare split lowers $G_{mis}$ and rare loss beyond the random split; common loss does not regress materially.

**Fail:** No positive mismatch exists, or rare loss improves without mismatch reduction, or the random split matches the main condition.

**Insufficient:** Common/rare directions are not auditable, target/distractor pairs are not matched, or the result changes completely with the high-gain band size.

**Cannot claim:** Real language semantics, real-DCLM preservation, final MoE method, or that all common high-gain directions are harmful.

## 1. Plain Question

The run does not ask only whether rare loss improves.

It asks:

> Does common take too much score while rare carries the needed discrimination?

If yes, a useful MoE split should reduce this mismatch.

## 2. Data Construction

### 2.1 Features

Build two known feature directions:

| Part | Meaning | Frequency | Role |
|---|---|---:|---|
| common feature `C` | shared prefix / background | high | forms the high-gain direction |
| rare feature `R` | specific relation / suffix | low | decides the correct target |

Each example is generated as:

$$
h = a_C c + a_R r + \epsilon.
$$

where $c$ is the known common direction, $r$ is the known rare direction, $\epsilon$ is noise, and $a_C$ is usually larger or more frequent than $a_R$.

### 2.2 Matched Rare Evaluation

Each rare example has two candidate targets:

| Candidate | Shares common? | Has correct rare relation? | Expected result |
|---|---|---|---|
| correct target `y` | yes | yes | should win |
| common distractor `d` | yes | no | should lose |

Common alone cannot solve this pair. The model must use rare information for `y` to beat `d`.

### 2.3 Train / Evaluation Split

Training is common-heavy:

- many `C` examples;
- fewer `C+R` examples;
- one balanced rare evaluation set is held out.

Evaluation focuses on rare discrimination:

- compare `y` against `d`;
- keep the common background fixed;
- vary only the rare relation.

## 3. Models And Conditions

| Condition | Role |
|---|---|
| shared baseline | one model sees all examples |
| common/rare split | main condition: common and rare paths are separated |
| same-capacity random split | capacity control |
| oracle split | positive control using known common/rare assignment |
| shuffled-rare-label guard | negative control |

Parameter counts should be as close as possible. If they cannot be equal, record the difference and treat capacity as a rival explanation.

## 4. Experiment Flow

### Stage 1: Train Baseline

Train the shared model on common-heavy synthetic data.

Save the model checkpoint and final readout matrix $W$.

### Stage 2: Find High-Gain Band

Compute singular directions of $W$.

Choose a high-gain band $P_k$ from the largest singular directions.

Test at least two $k$ values:

- strict high-gain band, such as top 1%;
- wider high-gain band, such as top 64 or top 128 when dimension allows.

### Stage 3: Measure Score Share

For matched rare examples, decompose the output score:

$$
z^{top}=WP_kh,\qquad z^{res}=W(I-P_k)h.
$$

Compute $C_{score}(k)$:

> the share of total score magnitude coming from the high-gain band.

### Stage 4: Measure Discrimination Share

For correct target `y` and common distractor `d`, compute:

$$
\Delta z = z_y-z_d.
$$

Compute $C_{disc}(k)$:

> the share of correct-target-versus-distractor discrimination coming from the high-gain band.

### Stage 5: Compute Mismatch Gap

Compute:

$$
G_{mis}(k)=C_{score}(k)-C_{disc}(k).
$$

Bad pattern:

- high $C_{score}$;
- low $C_{disc}$;
- positive and large $G_{mis}$.

Meaning: the high-gain band is loud but not useful enough for rare discrimination.

### Stage 6: Test MoE Split

Train split conditions:

1. common/rare split;
2. same-capacity random split;
3. oracle split.

Measure:

- rare loss;
- $G_{mis}(k)$;
- common loss;
- max route load;
- route identity if routing is present.

## 5. Primary Metric

The primary metric is:

$$
\Delta G_{mis}=G_{mis}^{baseline}-G_{mis}^{split}.
$$

It answers:

> Does splitting reduce common high-gain suppression of rare discrimination?

This metric decides the card because loss improvement alone can be misleading.

## 6. Secondary Metrics

| Metric | Meaning | Why needed |
|---|---|---|
| rare loss | whether rare examples become easier | functional guard |
| common loss | whether common examples are preserved | common retention guard |
| random-split rare loss | whether gain is just capacity | main control |
| oracle-split rare loss | known good upper bound | data validity check |
| max load | whether the split collapses | fake-split guard |

## 7. Success / Failure / Insufficient Evidence

**Success:**

- shared baseline has positive $G_{mis}$ on matched rare examples;
- common/rare split lowers $G_{mis}$;
- rare loss improves;
- same-capacity random split cannot explain the same effect;
- common loss does not materially regress.

**Failure:**

- no positive $G_{mis}$ exists;
- the high-gain band already discriminates correctly;
- rare loss improves but $G_{mis}$ does not move;
- random split matches or beats the main condition.

**Insufficient evidence:**

- candidate pairs are not matched;
- common and rare directions are unknown;
- conclusion changes completely under a different high-gain band size;
- the main condition has materially larger capacity.

## 8. Known Good / Known Bad / Known Confusing Cases

**Known good:** Oracle split should lower rare loss and mismatch gap.

**Known bad:** Shuffling rare labels should remove rare discrimination.

**Known confusing:** Random split may improve rare loss by capacity alone, so it must be included.

## 9. What This Cannot Claim

This experiment cannot claim:

- real language semantics;
- real-DCLM expert utility;
- final preservation method;
- all common high-gain directions are harmful.

It can only claim:

> On controlled data, whether common high-gain dominance is a causal rare-discrimination failure mode.

## 10. Execution Notes

Write raw run outputs under the runnable experiment workspace. Promote only curated tables, figures, `summary.md`, `detailed.md`, and anchor updates into `main/experiments/A09/A09_01_common_band_rare_discrimination/`.
