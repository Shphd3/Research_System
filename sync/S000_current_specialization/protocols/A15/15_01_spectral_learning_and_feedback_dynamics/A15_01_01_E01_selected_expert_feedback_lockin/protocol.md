---
experiment_id: A15_01_01_E01_selected_expert_feedback_lockin
anchor_id: 15_01_01_selected_expert_feedback_lockin
status: approved_full_execution
execution_status: completed_pass_feedback_lockin
formal_job_id: pt-15rmvipu
canonical_language: en
approved_by: researcher_blanket_authorization
approved_at: 2026-07-31
---

# Protocol: Selected-Expert Feedback And M/T Route Correction

## 0. Approval Snapshot

The researcher explicitly authorized autonomous Anchor--Protocol--implementation--
remote-execution--result closure for both 0731 conjectures. This Protocol is
approved before formal seeds are run. Operationalization seeds may choose only
among the registered numerical grid below and never enter scientific evidence.

Pre-formal amendment: with noise SD 0.5, each independent bit has Bayes
accuracy $\Phi(2)$ and exact eight-expert routing has analytic ceiling
$\Phi(2)^3\approx0.933$. The original supervised guard of 0.95 was impossible.
Before any formal seed or primary-arm result was inspected, it was corrected to
"within 0.02 of the analytic ceiling and at least 0.90." Data, arms, primary
metric, effect threshold, and formal seeds are unchanged.

Authorized resources: one 8-GPU 5090 SPOT node. No graph edit, root publication,
commit, or push is authorized.

## 1. Decision Question

When all three H/M/T variables are necessary for the loss-optimal expert, does
selected-only expert co-training suppress later M/T route correction relative
to one-update-per-token oracle-functional expert coverage?

## 2. Hypothesis And Strongest Rival

**H1:** head-first routing trains incumbents, starves correct fine challengers,
and creates a utility loop that reduces later M/T correction.

**Rival:** M/T correction is only delayed by input variance. Changing expert
coverage while keeping the identical Router process and active-update count
does not materially change the final partition.

The primary contrast changes expert update recipient, not Router input energy.

## 3. Synthetic Data Contract

- Independent balanced $h,m,t\in\{-1,+1\}$; oracle expert
  $e^*=4\mathbf1[h=1]+2\mathbf1[m=1]+\mathbf1[t=1]$.
- Three independent 8-D bands with fixed unit signal directions:
  $x_b=s_b(bv_b+0.5\epsilon_b)$ and $(s_H,s_M,s_T)=(4,2,1)$.
- Router dimension: 24. Standardized SNR is identical across bands.
- Payload and target dimensions: 8. Payload $p\sim\mathcal N(0,I)$.
- Eight fixed target maps $A_e$ are orthogonal matrices generated once from
  seed `20260731`; $y=A_{e^*}p$.
- Training minibatches are generated online. Each seed owns a fixed held-out
  panel of 16,384 examples generated before training and never optimized on.
- Evaluation uses deterministic argmax routes; training uses stochastic
  categorical top-1 routes.

## 4. Model And Optimization Contract

- Gate: one linear $24\rightarrow8$ map with bias.
- Experts: eight independent linear $8\rightarrow8$ maps, initialized at zero.
- Gate initialization: all experts in the correct head half receive the same
  head-aligned weight `0.35`; one registered incumbent in each head half gets
  bias `1.5`; all remaining entries receive paired seed noise with SD `0.01`.
- Router objective: selected-loss policy gradient with a batch-mean baseline
  and entropy regularization. Router optimizer: Adam.
- Expert objective: mean squared error. Expert optimizer: SGD without momentum.
- Batch size: 512. Formal horizon: 6,000 optimizer steps. Evaluation every 100
  steps, including step 0.
- Each token executes one selected-expert forward for Router feedback and one
  update-recipient expert forward; if recipients coincide the path is still
  counted twice. Exactly one expert backward/update occurs per token in both
  causal arms.
- Gradients are accumulated in FP32. Any nonfinite loss, parameter, or gradient
  makes the seed invalid and triggers `insufficient` if replacement is needed.

Operationalization grid:

- Router LR: $\{3\times10^{-3},10^{-2}\}$.
- Expert LR: $\{10^{-2},3\times10^{-2}\}$.
- Entropy coefficient: $\{0.01,0.03\}$.

On seeds 9000 and 9001, choose the lexicographically smallest
`router_lr, expert_lr, entropy` combination that passes both known-good guards,
keeps all losses finite, and leaves step-0 head accuracy above 0.95. The chosen
triple is written to `selected_config.json` before formal execution.

## 5. Conditions

| Condition | Router feedback | Expert receiving the one update | Decision role |
| --- | --- | --- | --- |
| selected_only | loss of sampled expert | sampled expert $a$ | native feedback treatment |
| oracle_coverage | loss of sampled expert | oracle expert $e^*$ | causal coverage contrast |
| oracle_experts_bandit | loss of sampled expert | none; $W_e=A_e$ fixed | known-good bandit feedback guard |
| supervised_router | cross-entropy to $e^*$ | none | H/M/T readability guard |

Only the first two conditions enter the primary effect. Guard conditions cannot
produce a scientific Pass by themselves.

## 6. Primary Metric

For a deterministic held-out route, decode predicted bits $(\hat h,\hat m,\hat
t)$ from the expert index. Fine correction accuracy is

$$
C_{MT}=\tfrac12[\Pr(\hat m=m\mid\hat h=h)+
\Pr(\hat t=t\mid\hat h=h)].
$$

It measures whether the initially correct coarse head partition was refined by
the two lower-variance variables. It does not measure language-model utility.

The primary paired effect at step 6,000 is

$$
\Delta C_{MT}=C_{MT}^{oracle\ coverage}-C_{MT}^{selected\ only}.
$$

Report the seed median, mean, and a 10,000-resample paired-seed bootstrap 95%
interval. The practical-effect threshold is 0.10 absolute accuracy.

## 7. Mechanism And Secondary Metrics

- Exact oracle-expert route accuracy and separate M/T bit accuracies.
- Correct-expert update share: fraction of expert updates sent to $e^*$.
- Challenger starvation: update share of the correct non-incumbent expert on
  examples initially assigned to an incumbent; below 0.25 is the registered
  directional threshold because four fine experts exist inside each head half.
- Utility gap: selected incumbent MSE minus correct challenger MSE, evaluated
  counterfactually on the held-out panel. Negative means the incumbent is
  currently better and can reinforce lock-in.
- Router entropy, load share, head accuracy, selected loss, expert update count,
  and expert forward count.
- Time curves are explanatory and cannot replace the final primary contrast.

## 8. Controls And Hard Guards

1. Paired seeds must use identical batches, held-out examples, initial Gate,
   expert initialization, and stochastic route uniforms across the two primary
   arms.
2. Active expert updates per token and registered expert forwards per token must
   match exactly.
3. `supervised_router` must reach exact route accuracy at least 0.90 and within
   0.02 of the analytic Bayes ceiling $\Phi(2)^3$ by step 2,000.
4. `oracle_experts_bandit` must reach exact route accuracy $\ge0.85$ by step
   6,000; otherwise selected-loss feedback is not operational.
5. At step 0, head-bit route accuracy must be $\ge0.95$ and both M/T bit
   accuracies must lie in $[0.40,0.60]$.
6. Held-out oracle expert must uniquely minimize expected MSE for all eight
   true mappings.

## 9. Splits, Seeds, And Statistical Unit

- Operationalization seeds: 9000, 9001. They select numerical settings only.
- Distributed smoke seeds: 9100--9107, one per GPU. They test orchestration only.
- Formal seeds: 1000--1031, four complete seeds per GPU.
- The seed, not the minibatch or evaluation example, is the statistical unit.
- Formal results are merged only if all 32 paired seeds and all conditions are
  complete. No failed seed may be silently dropped or replaced.

## 10. Execution Stages

1. S0: analytic/unit tests for label encoding, orthogonal target maps, route-bit
   decoding, update recipient, paired random streams, and metric computation.
2. S1: local operationalization grid on non-claim seeds; freeze config and hash.
3. S2: local single-seed smoke, then 8-GPU distributed smoke.
4. S3: one formal 8-GPU job for all 32 seeds.
5. S4: deterministic merge, guard audit, bootstrap, plots, and typed verdict.

No training checkpoint from S1/S2 enters S3.

## 11. Pass, Fail, And Insufficient Rules

**Pass:** all guards pass; the lower 95% paired-bootstrap bound for $\Delta
C_{MT}$ is above zero; the median effect is at least 0.10; both M and T component
effects are positive; and at least 24/32 selected-only seeds show the registered
early incumbent-better/challenger-starved mechanism direction.

**Fail:** all guards pass but the confidence interval includes zero, the median
effect is below 0.10, or one of M/T does not improve. This rejects the strong
feedback-lock-in conjecture under the registered system.

**Insufficient:** a known-good guard fails, compute/data pairing fails, losses
are nonfinite, fewer than 32 formal seeds complete, or implementation evidence
cannot distinguish update coverage from extra compute.

A positive effect below 0.10 is recorded as a sub-threshold observation, not a
Pass. A Pass does not authorize a real-DCLM training claim.

## 12. Figure Contract

The central figure has two panels. Left: held-out $C_{MT}$ versus optimizer step
for selected-only and oracle coverage, aggregated as seed median with 95%
paired bootstrap band. Right: final paired-seed $\Delta C_{MT}$ with zero and
0.10 reference lines. It answers whether expert coverage changes M/T correction.
It cannot show real-workload utility.

A mechanism figure may plot correct-challenger update share and incumbent-minus-
challenger MSE. It is explanatory and has no independent Pass authority.

## 13. Artifact And Evidence Contract

The worker package stores source, tests, exact config, environment, rank-local
JSON/NPZ files, merged CSV, logs, and job metadata. The Research System stores
only curated Protocol, `summary.md`, `detailed.md`, central figures, and compact
tables. `detailed.md` records commands, job ID, hashes, failures, guards, full
seed table, and artifact map.

## 14. Execution Authorization And Stop Rule

Implementation and full execution are authorized. Stop scientific execution if
S0 or S1 cannot satisfy known-good guards without leaving the registered grid.
Implementation bugs may be repaired and rerun with an explicit ledger. The
formal job may not change data, metrics, thresholds, seeds, or hyperparameters.

After formal completion, write the result even if negative; update this Anchor
and the single 0731 daily knowledge-update surface without requesting an
intermediate approval.
