# A15_13_05: Does Semantic Supervision Improve a Sufficiently Trained Online Hierarchy?

## 1. Problem Definition

The current decision question is whether a train-only hierarchical pseudo-label teacher improves
online reference-answer prediction over both task-only training and frequency-matched shuffled
supervision in the same hierarchical architecture. “Online” means that inference routes use only a
causal state available at zero-indexed block 14; no teacher path is supplied. This is the smallest
remaining decision because P1/P2 already localized and repaired the historical missing-parent-
supervision defect, but did not compare newly initialized models at an audited common budget.

The comparison is limited to frozen Qwen3-0.6B-Base, answer-only continuation on eight frozen data
sources, and low-rank modules in block 14 `down_proj`. It does not test teacher-layer optimality,
semantic truth, free-generation accuracy, public-benchmark decontamination, or full-model training.
Pass would retain semantic supervision as a candidate online training signal; Fail would stop using
label agreement alone to motivate it; budget or eligibility ambiguity yields Insufficient.

## 2. Physical Priors

The active prior is that full-window final-layer states contain a train-only partition whose
sample-specific assignments add task-relevant information beyond class frequencies. The observable
exposing this prior is lower test answer negative log-likelihood for true pseudo-label supervision
than for both task-only and example-shuffled supervision under a held-fixed hierarchy. The prior is
falsified locally if the true assignment is reliably worse than either control; a null or unstable
difference leaves information value unresolved.

## 3. Falsifiable Hypotheses

The primary hypothesis predicts positive online answer-loss reductions from task-only to semantic
supervision and from shuffled to semantic supervision in each of two seeds. The strongest rival is
that apparent value comes from optimization time, class frequencies, load, or architecture rather
than the sample-to-label relation. Task-only controls extra supervision, while a fixed permutation of
legal parent-child label pairs controls the auxiliary objective and example-level label counts.

Architecture baselines answer a separate contextual question: dense rank 24, flat eight-expert rank
24, shared-flat rank 8 plus selected rank 16, and shared-parent-child rank 8+8+8 are compared at equal
per-token active rank. Their stored parameters, sharing, gate depth, and coefficient structure differ,
so their ranking cannot establish a pure causal advantage of hierarchy.

## 4. Mathematical Model

For test records \(i\), let \(s_i^m\) be the summed reference-answer negative log probability under
condition \(m\), and let \(n_i\) be its answer-token count. The task quantity is

\[
L_m=\frac{\sum_i s_i^m}{\sum_i n_i}\quad\text{nats per answer token}.
\]

The decision effects are \(\Delta_{task}=L_{H\text{-task}}-L_{H\text{-sem}}\) and
\(\Delta_{shuf}=L_{H\text{-shuf}}-L_{H\text{-sem}}\); positive values favor true pseudo-label
supervision. Each interval resamples whole records within source and recomputes the ratio of summed
loss to summed tokens. This measures teacher-forced likelihood, not free-generation correctness.

For semantic training, the candidate auxiliary objective is

\[
L=L_{answer}+\lambda_p L_{parent}+\lambda_c L_{child\mid teacher\ parent}.
\]

Confirmed P-AUX sets \(\lambda_p=\lambda_c=0.5\) so the two classification terms together retain the
unit auxiliary weight used by the historical single-term route loss. The child loss is masked to the
teacher parent and remains finite even when the predicted parent is wrong. This weighting has no
historical simultaneous-loss precedent.

## 5. Computational Realization

The base, embedding, and language head are frozen. Routers read the block-14 input state of dimension
1024, while low-rank experts read the same block's MLP down-projection input of dimension 3072 and
return a 1024-dimensional residual. Learned flat routing scales one selected expert by its route
probability. Learned hierarchy adds an unscaled shared residual, a selected parent residual scaled by
parent probability, and a selected child residual scaled by parent times within-parent child
probability.

Confirmed P-BDATA renders all 57,099 raw rows using the frozen E14 adapters, deduplicates by record ID and
normalized prompt-plus-answer content, then use all 56,538 retained rows in deterministic source-
stratified 70/15/15 train/development/test splits. This yields 39,576/8,481/8,481 records with zero
record-ID and normalized-content overlap. Training uses the resulting natural source proportions;
source-specific results are descriptive. Only training records fit final-layer whole-window PCA64
and a three-parent diagonal GMM with 3/3/2 child allocation; frozen teachers alone label development
and test. Reference answers are privileged teacher input during label construction, never an online
Router feature.

All new models start from the same frozen base under paired seeds. Training is joint from update one:
all shared/parent/child low-rank modules participate, and online H-task/H-sem/H-shuf use the same
coefficient rule. No historical P2 adapter initializes or enters the new ranking. AdamW with separate
adapter and Router learning-rate groups is the approved optimization class; exact schedules,
checkpoints, load policy, and resource limits belong to the Protocol.

## 6. Minimal Falsification Tests

The decisive test compares H-sem with H-task and H-shuf on the untouched test split, separately for
seeds 17 and 29. Confirmed P-VERDICT uses 2,000 source-stratified paired-record bootstrap draws with seed
20260906. Pass requires both 95% interval lower endpoints to exceed zero in both seeds. A necessary
contrast whose upper endpoint is at most zero in both seeds is local Fail; every other eligible
pattern is Insufficient. No seed pooling, checkpoint selection on test, or per-record mean in place
of the token-weighted ratio is allowed.

Before opening test results, development-only checks freeze one common training budget and one common
hierarchy load policy. Confirmed P-BUDGET first runs unbiased D/F/SF/H-task to 512 and chooses 512 or
1024 from their development curves using the 0.002 nat/token rule; a 1024 choice reruns all four from
initialization under the 1024 schedule. Confirmed P-LOAD then tests a selection-only, conditional
3/3/2 load-bias policy on H-task at that selected budget and applies the selected policy equally to
H-task/H-sem/H-shuf. It may not inherit a 512 policy at 1024. If any preflight baseline remains
unstable at the 1024 ceiling, or any final-policy H-task/H-sem/H-shuf condition still meets the same
late-improvement rule at the common budget, the result is
`BUDGET_LIMITED_INSUFFICIENT`, not Pass or Fail, and no arm gets extra steps. Data overlap, nonfinite
loss, changed frozen hashes, absent required gradients, mask drift, checkpoint mismatch, or causal-
prefix failure makes affected evidence ineligible.

## 7. Current Evidence

Historical E14 found that the gold source path had lower mean answer NLL than hierarchical task-only
(0.794920 versus 0.806323), while the learned diagonal-GMM route was worse (0.817358). Its hard-pseudo
deployment was 0.836757 but improved to 0.805028 when the frozen pseudo path was externally supplied.
These values establish path headroom and a handoff failure only on the old overlapping data.

P1 then found that supplying only the teacher parent recovered 98.24% and 93.96% of that deployment
gap and that the old benchmark hard-pseudo parent Router had no gradient. P2 trained only the existing
3,075 parent-Router parameters and reduced mean online NLL from 0.836757276 to 0.804182618; both seeds
beat original routing and a matched shuffled-label control on full and record-ID-disjoint subsets.
The safe interpretation is that missing parent supervision, not causal-state inaccessibility alone,
explains the historical gap. The unresolved question is whether semantic supervision adds value when
all experts and Routers are newly and sufficiently trained on cleanly separated records.

P3 now supplies that matched comparison. The audit retained 56,538 globally content-unique records in
39,576/8,481/8,481 train/development/test splits with zero record-ID and normalized-content overlap.
The 12-arm D/F/SF/H-task/H-sem/H-shuf matrix completed at 512 updates and load-off; all eligibility,
stability, identity, finite-value, frozen-weight, and artifact-hash guards passed. Test H-task-minus-
H-sem is +0.010320 [0.009795, 0.010890] in seed 17 but -0.002078 [-0.002469, -0.001680] in seed 29.
H-shuf-minus-H-sem is positive in both seeds. The registered conjunction therefore yields
`INSUFFICIENT`, not support or local non-support.

A no-training post-hoc audit finds the opposite H-task/H-sem development directions already at update
128 and unchanged through 512, with every checkpoint interval excluding zero. At update 512, source
signs are mixed and 80% of absolute contribution comes from two sources in seed 17 and three in seed
29, while every leave-one-source-out pooled effect preserves its seed's sign. H-sem also has much less
concentrated parent load, finite declining auxiliary losses, and larger parent/leaf bank movement; all
experts change and the registered load trigger remains false. These observations localize candidates
but do not prove that supervision strength causes the reversal.

## 8. Claim Boundary And Next Decision

Current evidence supports the historical parent-supervision repair and an eligible but seed-unstable
P3 semantic comparison. It does not support a replicated semantic-supervision increment, teacher
optimality, semantic truth, hierarchy necessity, expert non-interchangeability, free-generation gain,
or uncontaminated benchmark generalization. Architecture rankings remain active-rank context with
storage, sharing, scale, and gate-depth confounds. Post-hoc checkpoint, source, load, loss, gradient,
and parameter-change diagnostics cannot strengthen the `INSUFFICIENT` verdict or prove a mechanism.

The researcher-selected next branch is one matched supervision-strength localization at the same H
architecture, frozen teacher, 512-update load-off budget, and seeds 17/29. The AI-proposed exact
operationalization, pending Protocol confirmation, compares H-task \((\lambda_p=\lambda_c=0)\),
H-sem-weak \((0.25,0.25)\), and current H-sem \((0.5,0.5)\) from common initial states and data orders.
Freeze a development-only rule before execution; the already-open P3 test is not a new confirmatory
surface. If the weak arm does not improve over the current arm in both seeds, stop the over-strong-
weight explanation. Do not add seeds, H-hard/H-oracle, layers, or another mechanism to this experiment.
