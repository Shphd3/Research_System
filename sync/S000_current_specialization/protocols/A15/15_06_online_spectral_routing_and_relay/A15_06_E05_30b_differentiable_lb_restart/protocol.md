---
experiment_id: A15_06_E05_30b_differentiable_lb_restart
anchor_id: 15_06_online_spectral_routing_and_relay
status: approved_for_implementation_smoke_and_full
approved_by: user
approval_date: 2026-08-09
resource_profile: 5090-8-spot
primary_metric: paired_seed17_30b_heldout_nll_across_five_arms_with_verified_lb_backward
---

# Protocol: A15_06_E05 Five-Arm 30B Restart With Differentiable Load Balancing

## 0. Approval And Repair Scope

The user approved a from-step-0 restart after the previous checkpoints were
deleted because their configured Switch load-balancing (LB) loss did not
backpropagate through re-entrant activation checkpointing.  This experiment
repairs only that autograd path, then compares five Router views under one
shared, verified differentiable LB objective.  It does not resume or reuse the
invalid source checkpoints.

The five arms are `vanilla_full`, `local_hmt`, `local_random_matched`,
`relay_hmt`, and `relay_random`.  Centered-Full is not part of this approved
run.  Seed 17 is fixed.  Each arm trains independently on one single-node
8x5090 SPOT worker to 30B tokens.

## 1. Decision Question

With identical model, data order, initialization, optimizer, token budget, and
a load-balancing loss that is proven to reach the Gate parameters, do Local-HMT
or Relay-HMT improve 30B held-out NLL over Vanilla-Full, and do the covariance
band identities beat their dimension- and dynamics-matched random controls?

The primary metric is paired held-out next-token NLL at 30B tokens in
nat/token; lower is better.  The run also records load, route entropy, online
projector behavior, and LB gradients, but none replaces terminal NLL.

## 2. Model, Data, And Optimizer

All arms use the same four-block Qwen-style top-1 MoE: hidden size 768, six
query heads, three key/value heads, head dimension 128, eight sparse experts
plus one shared expert per block, and expert intermediate size 1,536.  The
resolved model must report exactly 251,199,232 trainable parameters and
152,108,800 active parameters per token.  Router parameters total 24,576.

The tokenizer, DCLM source
`/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10`, sequence
length 1,024, global batch 768, and fixed seed-17 sample order are shared.
Each optimizer step consumes 786,432 tokens.  Training uses BF16, AdamW,
learning rate $10^{-4}$, betas $(0.9,0.95)$, weight decay 0.01, a 636-step
warm-up, the registered 100B-token scheduler horizon, ZeRO stage 1, and
activation checkpointing.

## 3. Five Router Arms

- **Vanilla-Full:** every Gate reads its uncentered full local representation.
- **Local-HMT:** blocks 2/3/4 read the current block's centered online
  head/middle/tail subspace; block 1 reads centered full input.
- **Local-Random-Matched:** identical to Local-HMT except a fixed Haar rotation
  removes covariance-rank identity while preserving dimensions and tracker
  motion.
- **Relay-HMT:** blocks 2/3/4 read centered head/middle/tail bands from the
  trainable block-1 source.
- **Relay-Random:** identical to Relay-HMT except for the matched fixed Haar
  rotation.

Experts always receive their full local hidden state.  Relay gradients may
reach the block-1 source.  Online covariance statistics, eigendecomposition,
and Grassmann updates remain non-differentiable control state.

## 4. Differentiable LB Contract

For each layer and microbatch, let $p_i(x)$ be the full softmax probability for
expert $i$ and let $f_i$ be the hard top-1 token fraction.  The registered
Switch objective is

$$
L_{LB}=E\sum_{i=1}^{E}
\left(\frac{1}{T}\sum_x p_i(x)\right) f_i,
\qquad E=8,
$$

and the optimized objective is

$$
L=L_{LM}+0.01\sum_{\ell=1}^{4}L_{LB,\ell}.
$$

The hard assignment fraction is treated as a stop-gradient coefficient; the
soft probability path must remain differentiable.  Activation checkpointing
must stay enabled.  The repair may change only the checkpoint/autograd
transport of auxiliary tensors, not the LB formula, assignment rule, model
forward values, data, or optimization hyperparameters.

Before any full submission, all five arms must pass:

1. every layer's `lb_loss` is finite and has an autograd function;
2. LB-only backward produces a finite, nonzero gradient on every layer Gate;
3. LM-only and LM+LB shadows share exact step-0 weights and batch, while the
   LB branch produces a nonzero Gate update delta;
4. checkpointed and uncheckpointed forward values agree within the registered
   BF16/FP32 tolerance;
5. activation checkpointing remains enabled in the full command.

Logging a nonzero LB scalar or setting `lambda_lb=0.01` is not sufficient.

## 5. Training Budget And Checkpoints

All runs start at optimizer step 0 and end at step 38,147, equal to
30,000,021,504 tokens.  Only full recovery milestones at the following steps
are retained:

| Label | Step | Actual cumulative tokens |
| --- | ---: | ---: |
| 2B | 2,544 | 2,000,683,008 |
| 5B | 6,358 | 5,000,134,656 |
| 10B | 12,716 | 10,000,269,312 |
| 25B | 31,790 | 25,000,673,280 |
| 30B | 38,147 | 30,000,021,504 |

Every milestone must include model, eight optimizer shards, scheduler, RNG,
data cursor, running means, covariance EMA, deployed nested bases, random
frames, refresh counters, and continuity telemetry.  A short continuous versus
save/resume comparison must verify restoration before full submission.  SPOT
preemption may resume only from the latest complete registered milestone.

## 6. Pairing, Evaluation, And Diagnostics

The five arms share the same step-0 common parameters, token hashes, dropout
and RNG sequence where architecturally applicable, learning-rate schedule,
evaluation documents, and milestone steps.  Arm-specific deterministic buffers
are initialized from the registered seed without consuming the common model
RNG stream.

At each retained milestone, save enough telemetry to reconstruct per-layer
expert fractions, route entropy, LB value and coefficient, LM/LB Gate-gradient
norms, projector gamma/flip/lag, throughput, and TensorBoard curves.  Terminal
evaluation uses the same held-out documents and document-level paired
bootstrap intervals.  Required contrasts are Local-HMT minus Vanilla,
Local-HMT minus Local-Random, Relay-HMT minus Vanilla, Relay-HMT minus
Local-HMT, and Relay-HMT minus Relay-Random.

## 7. Smoke And Exact-Resume Gates

The implementation first passes dependency-light unit tests, then a real
single-GPU model smoke, then five independent 8x5090 distributed smokes.  Each
distributed smoke must verify forward/backward, per-layer LB Gate gradients,
common step-0 parameter hashes, per-step token hashes, online projector
orthogonality/nesting, TensorBoard/JSONL output, complete checkpoint save, and
exact resume of model, optimizer, scheduler, RNG, data cursor, and online
state.  NaN/Inf, OOM, inconsistent distributed state, corrupt checkpoint, or
missing LB Gate gradient blocks submission.

Load concentration, NLL degradation, high flip, or gamma zero are scientific
outcomes and do not trigger performance early stopping if numerical and state
guards remain valid.

## 8. Verdict And Claim Boundary

This one-seed experiment can establish only a seed-17 30B ordering under an
effective microbatch Switch LB objective.  A covariance-identity advantage
requires HMT to beat its matched random arm at the paired terminal evaluation;
a Relay-source advantage requires Relay-HMT to beat Local-HMT.  Missing an arm,
irrecoverable state, failed LB backward, or missing terminal paired evaluation
makes the corresponding comparison insufficient.

The experiment cannot establish universal H/M/T semantics, cross-seed
generality, scale transfer, expert specialization as the unique mediator, or
that another global-batch/router-z-loss/load-bias implementation would behave
the same way.

## 9. Execution Contract

The approved resource tuple is: ACP, workspace `share-space`, AEC2
`computing-cluster-5090-01g`, worker spec `n12lp.nn.i10a.8`, one worker,
eight processes/GPUs, SPOT quota, normal priority.  After all gates pass, submit
exactly five full jobs without another approval round and monitor through
stable optimizer progress and one complete telemetry interval.  Raw logs,
checkpoints, and caches stay in the worker surface; Research_System receives
only the protocol, smoke verdict, job ledger, and later curated evidence.

## 10. Confirmation Ledger

- 2026-08-09: the user deleted the invalid prior checkpoints and approved a
  from-scratch five-arm single-seed 30B rerun with verified LB backward.
- 2026-08-09: the user fixed retained milestones to 2B, 5B, 10B, 25B, and 30B,
  required exact continuation, and selected the single-node 8x5090 profile.
- Cross-block consistency: passed before implementation.

## 11. Append-Only Amendment Ledger

### E05-AM01 — add a 20B recovery and evaluation checkpoint

- Amendment time: `2026-08-10T12:28:02Z`.
- Before: full checkpoints and milestone evaluations at steps `2544`, `6358`,
  `12716`, `31790`, and `38147` (approximately 2B, 5B, 10B, 25B, and 30B
  tokens).
- After: add step `25432` (`20,000,538,624` tokens); retain every previously
  registered checkpoint, including step `31790` at 25B.  The amended schedule
  is `2544,6358,12716,25432,31790,38147`.
- Reason: the five first recovery jobs had no complete checkpoint between 10B
  and 25B.  Adding 20B bounds future SPOT recovery loss and makes the middle of
  the 10B--25B interval independently evaluable.
- Results visible before amendment: the registered 10B endpoint and its
  interim evaluation were visible.  Five replacement jobs had also produced a
  short unsaved continuation beyond 10B; that prefix is not used for choosing
  the new milestone or for scientific comparison.
- Affected block: Block G only (checkpoint/evaluation and recovery schedule).
  The research question, arms, data, initialization, objective, optimization,
  training-token endpoint, primary metric, and verdict rules are unchanged.
- Approval: the user explicitly authorized adding 20B and 25B checkpoints and
  resubmitting when technically feasible.  The 25B checkpoint was already
  present, so only 20B is added.
- Eligibility impact: the complete common 10B checkpoints remain eligible.
  The unsaved post-10B prefixes from the superseded recovery jobs are excluded.
  New jobs must exact-resume from step `12716`; their 20B, 25B, and 30B
  checkpoints are eligible only after resume identity, common token hashes,
  checkpoint completeness, and unchanged scientific configuration pass.
- Execution scope: approved for an immutable implementation-only revision,
  stopping the superseded recovery jobs, resubmitting the same five arms on the
  already approved single-node 8x5090 SPOT profile, and monitoring exact resume.
