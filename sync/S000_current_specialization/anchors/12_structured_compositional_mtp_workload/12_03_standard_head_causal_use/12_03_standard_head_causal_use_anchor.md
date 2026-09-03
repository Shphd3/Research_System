# Intermediate-State Causal Use By The Standard Head

Status: active design; revised protocol exists; no run is authorized.


## 1. Problem Definition

### Terminology / Definitions

| Term | Plain meaning | Concrete object | Why it matters | Cannot prove |
|---|---|---|---|---|
| representation present | a held-out decoder can recover a task variable | probe on $h_T$ | prerequisite | model reliance |
| intermediate state $B$ | first-stage result required to select the second-table row | $B=\pi_1(A)$ | identifies composition rather than an early answer code | that the network must encode $B$ linearly |
| final answer $Y$ | root result after the second mapping | $Y=\pi_2(B)$ | common prediction target | intermediate-state use |
| causal use | changing only the fitted $B$ component changes the standard answer to $\pi_2(B')$ | cross-fitted counterfactual patch | separates presence from function | real-task transfer |
| standard head | ordinary next-token output head shared by NTP and MTP | $q_1(\cdot\mid h_{T+1})$ | fixes the final comparison target | full language-model quality |
| task gate | the shared starting checkpoint solves unseen full-context examples and passes partial-evidence guards | full-context accuracy and single-table controls | makes objective comparison eligible | why learning succeeded |

**Single decision question:** At one shared task-capable checkpoint, does
informative Next-2 increase causal use of the intermediate state $B$ by the
standard next-token head relative to NTP-only continuation?

## 2. Physical Priors

1. Decodability is presence, not use.
2. Patching the final-answer direction $Y$ tests an early answer code; it does
   not by itself test intermediate composition through $B$.
3. NTP and MTP must be scored by the same standard head at the same answer
   position and start from the same capable checkpoint.
4. The network is not assumed to encode $B$ in a linear subspace; cross-fit
   stability is an eligibility guard rather than a theorem.

## 3. Falsifiable Hypotheses

The causal-use hypothesis predicts that informative Next-2 produces a larger
$B$-specific counterfactual standard-head effect than NTP, without lower clean
standard-head accuracy. The readable-but-inert rival predicts a better probe
but no task-specific causal effect. The early-answer-code rival predicts a
$Y$-patch effect without a stable $B$-patch effect.

The hypothesis is weakened if equal-rank random subspaces reproduce the
effect, if the $B$ subspace is not stable out of sample, or if only the private
auxiliary head changes.

## 4. Mathematical Model

The task factorizes as

$$
B=\pi_1(A),
\qquad
Y=\pi_2(B).
$$

The standard head predicts after the shared format token:

$$
h_{T+1}=F_\theta(h_T,e_{fmt}),
\qquad
p(y\mid x)=q_1(y\mid h_{T+1}).
$$

Construct recipient and donor examples that share $\pi_2$ but have different
first-stage results $B_r$ and $B_d$. The predicted counterfactual answer is

$$
Y_{cf}=\pi_2(B_d).
$$

Fit an intermediate-state subspace $P_B$ on separate data and patch

$$
h_T^{patch}=h_T(x_r)+P_B\bigl(h_T(x_d)-h_T(x_r)\bigr).
$$

Let $F_B$ be the fraction whose standard-head answer changes to $Y_{cf}$ and
$F_{rand}$ the same fraction under an equal-rank random projection. Define

$$
C_B=F_B-F_{rand},
$$

and compare

$$
\Delta C_B=C_B^{MTP-info}-C_B^{NTP}.
$$

A separately fitted final-answer subspace $P_Y$ is a secondary diagnostic,
not the primary composition claim.

## 5. Computational Realization

Use the exact $M=8$ two-permutation task with atomic decision, format, and
answer tokens. First train one shared NTP checkpoint until it passes the task
gate. Only then clone it into NTP, informative Next-2, and a masked-information
auxiliary control. All primary outcomes use the same standard head after the
format token.

## 6. Minimal Falsification Tests

1. **Capability gate:** full-context held-out accuracy at least 0.70; format
   accuracy at least 0.99; single-table/local controls near chance 0.125;
   evidence swaps change the correct answer.
2. **Primary causal test:** compare cross-fitted $C_B$ for informative Next-2
   and NTP using shared-$\pi_2$ counterfactual pairs.
3. **Specificity guards:** equal-rank random patches, $P_B$ versus $P_Y$,
   task-subspace ablation, clean standard-head accuracy, and cross-fit
   subspace stability.

Supported means $\Delta C_B\ge0.10$ in at least 4/5 seeds, clean MTP accuracy
is no more than 0.02 below NTP, and $B$-subspace ablation is more damaging than
random ablation. A failed task gate or unstable $P_B$ is insufficient evidence,
not a negative causal-use result.

## 7. Current Evidence

A11 supports earlier signal formation and conditional parameter transmission,
while its cross-position result shows that formation may fail to reach the
answer state. A12 has a valid depth-two workload, but the current from-scratch
learner failed its task gate. The rank result is only a controlled linear
mechanism. No completed experiment directly measures causal control through
the intermediate state $B$ at a task-capable neural checkpoint.

The detailed test surface is
[protocol.md](/Projects/from-attention-to-search/main/experiments/A12/12_03_standard_head_causal_use/A12_03_E01_standard_head_causal_use/protocol.md).

## 8. Claim Boundary And Next Decision

Passing this anchor would support only: on the controlled two-permutation
task, after capability is established, informative Next-2 increases
intermediate-state-specific causal control of the standard next-token answer.

It would not prove natural-language benefit, universal MTP superiority, a
model-scale law, curriculum benefit, a general branching-tree mechanism, or
Router/MoE value.

**Exactly one next decision:** review the revised protocol, then run only the
shared capability gate. Do not open the objective comparison if the gate
fails.
