# Protocol: A12_03_E01 Intermediate-State Causal Use By The Standard Head

## 0. Approval Snapshot

**Approval status:** revised draft for user review; do not implement or run.
**Purpose:** decide whether informative Next-2 makes the intermediate state of
a learned depth-two task more causally used by the standard next-token head
than NTP-only continuation.
**Primary anchor:** `../../../../problem_anchors/12_structured_compositional_mtp_workload/12_03_standard_head_causal_use/12_03_standard_head_causal_use_anchor.md`
**Primary metric:** \(\Delta C_B\), the NTP-to-MTP change in intermediate-state-
specific counterfactual control of the standard head.
**Eligibility gate:** one shared NTP checkpoint must first solve held-out
full-context composition and pass single-table/evidence-swap controls.
**Conditions after the gate:** `NTP`, `MTP-info`, and secondary `MTP-mask`.
**Pass:** \(\Delta C_B\ge0.10\) in at least 4/5 seeds, clean MTP main-head
accuracy no more than 0.02 below NTP, and \(B\)-subspace ablation more damaging
than equal-rank random ablation.
**Fail:** valid task-capable runs give \(\Delta C_B\le0\) in at least 4/5 seeds,
or equal-rank random subspaces reproduce the effect.
**Insufficient:** task gate, paired-checkpoint, cross-fit stability, or
intervention-validity guard fails.
**Cannot claim:** universal MTP benefit, general tree reasoning, natural-
language transfer, a model-scale law, curriculum benefit, or Router/MoE value.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
|---|---|---|---|---|---|
| NTP | ordinary next-token training | standard loss at format and answer positions | nats | baseline | inability to learn long-range structure |
| informative Next-2 (`MTP-info`) | NTP plus correct direct future-answer supervision at the decision state | \(L_N+\lambda L_A\) | nats | tested objective intervention | standard-head use by itself |
| masked auxiliary control (`MTP-mask`) | same auxiliary machinery with the informative decision-state term removed | masked \(L_A\) | nats | separates information from extra machinery | perfect FLOP matching |
| intermediate state \(B\) | first lookup result that selects the second-table row | \(B=\pi_1(A)\) | entity label | identifies composition | linear neural code |
| final answer \(Y\) | second lookup result | \(Y=\pi_2(B)\) | entity label | common standard-head target | use of \(B\) |
| standard main head | ordinary next-token output head shared by all conditions | \(q_1(\cdot\mid h_{T+1})\) | probability / cross-entropy | fixes the final outcome | private-head quality |
| task gate | shared checkpoint solves unseen full-context examples and fails intended partial-evidence controls | accuracy and intervention thresholds | probability | makes comparison eligible | learning cause |
| intermediate-state subspace \(P_B\) | held-out-stable directions predictive of \(B\) | cross-fitted supervised low-rank projection | rank and probe accuracy | intervention target | causal use without intervention |
| \(C_B\) | standard-head control specific to \(P_B\) | counterfactual flip rate minus equal-rank random flip rate | probability points | primary use metric | real-task benefit |
| cross-fitting | fit \(P_B\) on different examples from those used to score patches | rotated train/test folds | fold stability | limits label leakage | fully on-manifold patches |

## 2. Anchor Alignment

**Decision question:** after capability is fixed, does informative Next-2
increase causal use of \(B\) by the common standard head?
**Physical prior:** decodability is presence, while functional use requires a
task-rule-consistent intervention on the model's own output.
**Core model term:**

\[
\Delta C_B=C_B^{MTP-info}-C_B^{NTP}.
\]

**Falsifier:** no positive \(B\)-specific standard-head control under valid
task-capable runs.
**Claim boundary:** controlled depth-two task and checkpoint-local continuation
only.

## 3. Tested Hypothesis And Rival Explanations

### Tested hypothesis

After one shared NTP checkpoint learns

\[
B=\pi_1(A),\qquad Y=\pi_2(B),
\]

adding correct direct answer supervision at \(h_T\) increases the causal control
that the intermediate state \(B\) exerts on the standard head at \(h_{T+1}\).

### Rival explanations

1. **Readable but inert:** \(B\) probe accuracy rises without standard-head
   causal control.
2. **Early answer code only:** an answer subspace \(P_Y\) controls the output,
   but \(P_B\) does not.
3. **Private-head-only gain:** the auxiliary head improves while the standard
   head is unchanged.
4. **Generic perturbation:** any equal-rank hidden perturbation produces the
   same flips.
5. **Capability mismatch:** one continuation simply knows the task better.
6. **Patch extrapolation:** patched states are off-manifold and produce
   arbitrary outputs.

## 4. Data, Model, And Objective

### 4.1 Data-generating process

Let \(\mathcal V=\{v_0,\ldots,v_7\}\). Independently sample two uniform random
permutations \(\pi_1,\pi_2\) and a query entity \(A\). Define

\[
B=\pi_1(A),\qquad Y=\pi_2(B).
\]

Each context contains both complete tables. The output is exactly three atomic
tokens:

```text
<DECIDE> <FMT_0> <ANS_Y>
```

Conditioned on \(A\), either table alone leaves \(Y\) uniform; the two tables
together determine \(Y\).

### 4.2 Splits and controls

- calibration train: 8,192 two-hop examples plus one fixed one-hop teaching
  set;
- validation: 1,024 examples;
- causal-use test: 2,048 examples;
- ordered permutation pairs are disjoint across splits;
- single-table, local-only, row-order, and evidence-swap controls are generated
  from the same latent examples.

For the primary counterfactual, construct recipient/donor pairs with the same
\(A\) and \(\pi_2\) but different first mappings. Modify \(\pi_1\) by a validity-
preserving output swap involving row \(A\), so

\[
B_r\ne B_d,
\qquad
Y_r=\pi_2(B_r),
\qquad
Y_{cf}=\pi_2(B_d).
\]

Sharing \(\pi_2\) is essential: it gives an unambiguous prediction for how a
changed intermediate state should affect the recipient's answer.

### 4.3 Shared calibration

- model: Qwen3-0.6B with newly registered atomic task tokens;
- full-model fine-tuning;
- fixed teaching schedule: 1,000 one-hop NTP updates, then at most 5,000
  two-hop NTP updates;
- provisional optimizer: AdamW, learning rate `2e-5`, batch size `64`, weight
  decay `0.1`, 100 warmup updates, cosine decay, gradient clipping `1.0`;
- gate: full-context validation answer accuracy \(\ge0.70\), format accuracy
  \(\ge0.99\), single-table accuracy \(\le0.20\), and evidence-swap consistency
  \(\ge0.90\).

If the gate fails, stop. Do not run objective continuations or representation
interventions.

### 4.4 Paired objective continuation

Clone the exact capable checkpoint into three 500-update continuations. Reset
optimizer state identically and use identical data order and seeds.

\[
L_{NTP}=L_N,
\]

\[
L_{MTP-info}=L_N+\lambda L_A,
\qquad \lambda=1,
\]

where \(L_N\) includes the standard format prediction at \(h_T\) and answer
prediction at \(h_{T+1}\), while \(L_A\) reads the correct answer directly from
\(h_T\). `MTP-mask` keeps the auxiliary path but removes the informative
decision-state term.

Final evaluation always uses the same standard unembedding after `<FMT_0>`.
Record auxiliary compute overhead; do not call equal update count equal FLOPs.

## 5. Conditions, Seeds, And Evidence Roles

| Condition or control | Question answered | Evidence role | Pass / guard | Insufficient condition |
|---|---|---|---|---|
| shared NTP calibration | is the model eligible? | validity gate | all gate thresholds pass | any gate fails |
| NTP versus MTP-info | does direct future supervision change use? | primary comparison | protocol pass rule | pairing or collapse failure |
| MTP-mask | is information, rather than extra machinery, responsible? | secondary control | below MTP-info | masking mismatch |
| equal-rank random patch | is the effect task-specific? | primary guard | \(B\) patch larger | unstable estimate |
| final-answer patch \(P_Y\) | is the result only an early answer code? | rival diagnostic | \(B\) remains independently effective | \(P_B\) unstable |
| \(B\)-subspace ablation | does clean performance rely on \(B\)? | convergent guard | larger harm than random ablation | off-manifold collapse |

Run one smoke seed. Only after the task gate and intervention pipeline pass,
run confirmation seeds `971--975`.

## 6. Primary Metric

For each condition \(o\), patch the cross-fitted \(B\) component from donor to
recipient at \(h_T\), pass the same `<FMT_0>` transition, and measure

\[
F_B^o=Pr\left[\arg\max q_1(\cdot\mid h_{T+1}^{patch})=Y_{cf}\right].
\]

Let \(F_{rand}^o\) be the same rate under an equal-rank random projection:

\[
C_B^o=F_B^o-F_{rand}^o.
\]

The decision metric is

\[
\Delta C_B=C_B^{MTP-info}-C_B^{NTP}.
\]

This directly tests whether MTP increases task-rule-consistent control of the
common standard target through the intermediate-state subspace. It cannot
show real downstream benefit or eliminate every off-manifold concern.

## 7. Secondary Metrics

- clean standard-head answer accuracy and answer cross-entropy;
- held-out probe accuracy for \(B\) and \(Y\) at \(h_T\) and \(h_{T+1}\);
- \(B\)-subspace versus \(Y\)-subspace patch effects;
- standard-head cross-entropy increase after task versus random ablation;
- counterfactual answer log-odds shift;
- `MTP-mask` contrast;
- subspace rank, cross-fit principal-angle stability, and intervention norm;
- relative compute and wall-clock overhead.

## 8. Known Good, Bad, And Confusing Cases

- **Known good:** full context, valid shared-\(\pi_2\) counterfactual, predicted
  \(Y_{cf}\) changes.
- **Known bad:** one table removed, local-only suffix, random checkpoint,
  training \(P_B\) on scored test labels, or donor/recipient with different
  \(\pi_2\).
- **Known confusing:** high \(B\) probe with zero \(C_B\); positive \(P_Y\) effect
  with zero \(P_B\) effect; random-subspace flips; positive \(C_B\) accompanied by
  clean accuracy loss.

## 9. Stage-Level Profiling Plan

| Stage | Local question | Rule | Required artifact | Handoff |
|---|---|---|---|---|
| 0 data audit | are tables jointly necessary and counterfactuals valid? | analytic identity plus chance guards | manifest and examples | calibration |
| 1 capability gate | does the shared model solve unseen composition? | all gate thresholds | curves and checkpoint map | clone or stop |
| 2 paired continuation | are conditions matched? | exact start/data/update match | pairing ledger | subspace audit |
| 3 subspace fit | is \(P_B\) stable off-test? | preregistered probe and angle guard | spectra and angles | patch or stop |
| 4 causal intervention | does the standard answer follow donor \(B\) under recipient \(\pi_2\)? | primary rule | task/random patch figure | ablation guard |
| 5 decision | is causal use higher without clean harm? | conjunctive pass/fail rule | summary table | anchor update |

## 10. Algorithm Specification

**Input:** shared-\(\pi_2\) counterfactual pairs \((x_r,x_d)\), trained checkpoint,
cross-fit split.
**Parameters:** \(P_B\) rank selected on calibration data only; equal-rank random
projections; atomic format token.
**Intermediate variables:** \(B_r,B_d,Y_{cf},h_T(x_r),h_T(x_d),P_B\).
**Steps:** fit \(P_B\) off-test; replace only the projected \(B\) component; apply
the same format-token transition; evaluate \(Y_{cf}\) with \(q_1\); repeat with
random projections, \(P_Y\), and ablation.
**Outputs:** \(C_B\), \(\Delta C_B\), clean main-head accuracy, ablation gap, probe
and subspace stability.
**Debug artifacts:** pair manifest, subspace spectrum, intervention norms,
output entropy, random-patch distribution.
**Failure reasons:** task not learned, leakage, unstable \(P_B\), off-manifold
collapse, or mismatched conditions.

## 11. Success, Failure, And Insufficient Evidence

**Success:** the full conjunctive pass rule in the approval snapshot holds.
**Failure:** the task gate and intervention guards pass, but the causal-use
advantage is absent or nonspecific.
**Insufficient:** any eligibility, pairing, cross-fit, or intervention-validity
guard fails.

## 12. What This Cannot Claim

This experiment cannot establish universal MTP superiority, a model-scale
law, curriculum benefit, a general branching-tree mechanism, natural-language
or code-benchmark transfer, or Router/MoE value.

## 13. Review Notes And Protocol Changes

This revision separates the intermediate state \(B\) from the final answer \(Y\).
The primary intervention now uses shared-\(\pi_2\) pairs and \(P_B\); \(P_Y\) is a
secondary early-answer-code diagnostic. No implementation or run should begin
before approval.
