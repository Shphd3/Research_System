---
experiment_id: A15_01_02_E01_low_variance_functional_delay
anchor_id: 15_01_02_low_variance_functional_delay
status: approved_full_execution
execution_status: completed_weak_pass_delay_strong_fail
formal_job_id: pt-15rmvipu
canonical_language: en
approved_by: researcher_blanket_authorization
approved_at: 2026-07-31
---

# Protocol: Functional Stability Of H/M/T Routes

## 0. Approval Snapshot

The researcher authorized autonomous formalization, implementation, one-node
8-GPU execution, and result closure. This Protocol is approved before formal
seeds run. No graph edit, root publication, commit, or push is authorized.

## 1. Decision Question

At matched standardized SNR, is native low-variance tail routing functionally
random-like at the registered horizon, or does it eventually become correct
and persistent after a variance-induced delay?

## 2. Hypotheses And Rival

**Strong H1:** native T remains uncrossed and near a matched label-free random
control, while equal-energy T reaches functional stability.

**Weak H1:** all native bands cross, but functional stability time follows
\(H<M<T\) and equalization removes most of the delay.

**Strongest rival:** low-variance routes appear unstable only because raw churn
is measured before correctness. Tail contains the same learnable information
and is delayed, not randomized.

## 3. Synthetic Data Contract

- Balanced binary label \(z\in\{-1,+1\}\).
- Independent 8-D signal blocks
  \(x_b=s_b(zv_b+0.5\epsilon_b)\) with \((s_H,s_M,s_T)=(4,2,1)\).
- Fixed orthonormal signal directions and paired online minibatches.
- Fixed held-out panel: 8,192 examples per seed, generated before training.
- Label-free controls use independent Gaussian noise of the same dimension and
  scale, with no \(zv_b\) term.
- Native, equal-energy, and random conditions use identical labels and paired
  random streams wherever mathematically applicable.

## 4. Model And Optimization Contract

- One independent bias-free binary linear Gate per condition.
- Weight initialization has fixed norm 1.0 and a seed-specific random direction.
- SGD without momentum or weight decay; learning rate \(10^{-3}\).
- Binary cross-entropy loss, batch size 512, FP32.
- Formal horizon: 4,000 optimizer steps; evaluation every 20 steps including 0.
- Equal-energy M and T inputs are multiplied by 2 and 4 respectively so all
  signal conditions have H amplitude. Native H is reused as equal-energy H.
- A long-horizon continuation to 12,000 steps is allowed only for native T
  seeds censored at 4,000; it is a registered boundary diagnostic and cannot
  turn a strong-horizon Fail into a strong Pass.

## 5. Conditions

| Family | H scale | M scale | T scale | Label information |
| --- | ---: | ---: | ---: | --- |
| native | 4 | 2 | 1 | same \(z\), matched standardized SNR |
| equal_energy | 4 | 4 | 4 | same \(z\), matched standardized SNR |
| random | 4 | 2 | 1 | none; scale-matched noise |

There are nine logical conditions (`native/equal/random × H/M/T`), with native
H and equal H sharing an identical trace rather than being double-counted.

## 6. Primary Metric

On the fixed held-out panel, accuracy \(A_b(k)\) is the fraction of correct binary
routes. Flip rate \(F_b(k)\) is the fraction whose deterministic route differs
from the previous evaluation. Functional stability time is the first step at
which \(A_b\ge0.90\) and \(F_b\le0.02\) for three consecutive evaluations.

Uncrossed seeds are right-censored at step 4,000. Report crossing fraction,
Kaplan--Meier median when defined, and restricted mean time to stability over
\([0,4000]\). The unit is optimizer steps. The metric cannot prove semantic or
MoE expert utility.

## 7. Secondary Metrics

- Full accuracy and flip trajectories.
- Cosine-squared alignment between learned weight and the true signal direction.
- Final accuracy, final flip rate, logistic loss, and weight norm.
- Pairwise native \(T_{FS}\) contrasts and equalized-minus-native contrasts.
- Long-horizon native-T crossing time for censored seeds.
- Random-control traces are null calibration, not an alternative useful Router.

## 8. Controls And Hard Guards

1. Equal-energy H/M/T must each cross functional stability in at least 30/32
   formal seeds by step 4,000.
2. The mean final accuracy of every label-free random band must lie in
   \([0.47,0.53]\), and no random band may have more than 2/32 false crossings.
3. Native/equalized pairs must share labels, base noise, held-out panel, and
   initial weight direction.
4. Initial accuracy for every signal condition must lie in \([0.35,0.65]\) at
   the model median; no band may start functionally stable.
5. Losses, gradients, and weights must remain finite for every formal seed.

## 9. Seeds And Statistical Unit

- Local smoke seeds: 9200 and 9201.
- Distributed smoke seeds: 9210--9217, one per GPU.
- Formal seeds: 2000--2031, four complete seeds per GPU.
- The seed is the statistical unit. Evaluation examples and time points are not
  treated as independent replicates.
- All 32 formal seeds must complete; no silent seed filtering or replacement.

## 10. Execution Stages

1. S0: unit tests for data variance/SNR, paired scaling, random-label
   independence, flip computation, consecutive-crossing logic, and censoring.
2. S1: local smoke verifies known-good and known-bad guards without tuning LR.
3. S2: 8-GPU distributed smoke verifies rank ownership and deterministic merge.
4. S3: one 8-GPU formal run for 32 seeds through step 4,000.
5. S4: registered native-T continuation only for censored seeds.
6. S5: merge, survival summaries, paired bootstrap, figures, and typed verdict.

## 11. Pass, Fail, Partial, And Insufficient Rules

**Strong Pass (random-like finite-horizon T):** all guards pass; at least 24/32
native-T seeds are censored at 4,000; native-T final accuracy differs from its
matched random-T mean by less than 0.05; and at least 30/32 equal-energy-T seeds
cross. Long-horizon crossings must still be reported.

**Weak Pass / strong-claim Fail (delay only):** all guards pass; at least 26/32
native-T seeds cross by 4,000 or 12,000; native restricted mean time follows
\(H<M<T\) with paired-bootstrap positive H-to-M and M-to-T contrasts; and
equal-energy T reduces restricted mean time by at least 50%. This supports
finite-time delay and rejects random-like tail.

**Fail:** guards pass but neither the strong random-like pattern nor a stable
ordered delay is observed.

**Insufficient:** any hard guard fails, fewer than 32 seeds complete, pairing is
broken, or numerical failure compromises a registered condition.

If both strong-horizon and eventual-delay descriptions apply, the typed verdict
must state both: finite-horizon random-like behavior and later recovery.

## 12. Figure Contract

The central figure has accuracy and flip-rate panels versus optimizer step for
native H/M/T, equal-energy T, and random T, with seed median and 95% bootstrap
bands. Horizontal lines mark 0.90 accuracy and 0.02 flip. Censored crossing
fractions are printed in the legend. It distinguishes correct persistence,
delayed correction, and stable-wrong random routing; it cannot show semantic
specialization.

A compact survival plot may show the fraction not yet functionally stable. Its
time axis is optimizer steps and its endpoint is explicitly censored.

## 13. Artifact And Evidence Contract

The worker package stores source, tests, exact config, environment, rank-local
traces, merged tables, logs, and remote metadata. The Research System stores
curated Protocol, `summary.md`, `detailed.md`, central figures, and compact
tables. The detailed record owns every seed trace, censoring decision, guard,
command, job ID, hash, and artifact link.

## 14. Execution Authorization And Stop Rule

Implementation, smoke, formal 8-GPU execution, and registered continuation are
authorized. A smoke failure may trigger implementation repair but not metric,
threshold, LR, seed, or data changes. If a hard guard is impossible under this
contract, stop and report `insufficient` rather than tuning toward H1.

After completion, write the evidence records, update the Anchor, and integrate
the verified knowledge update into the sole 0731 daily focus surface.
