# Protocol — A12_0_E01 Short-Range Single-Step versus Two-Step Composition

## Status

- Stage: calibration complete; capability gate failed
- Confirmation: blocked until a revised calibration passes capability and the user then fixes the answer-accuracy threshold
- Code changes are limited to the experiment workspace; no model-production code is changed.
- Calibration job: `pt-3okyxyjm` (`reserved`, one `n6ls.iu.i40.4` worker, four GPUs), submitted 2026-07-14.
- Calibration result: all 24 runs completed; no scale is eligible for threshold comparison. Confirmation was not started.

## 1. Decision and Scope

This protocol tests whether standard two-head MTP with $K=2$ accelerates the common standard head more for a short-range two-rule composition than for a matched short-range one-rule task.

The completed run is **calibration**, not confirmation. It recorded full learning curves and checked capability. Because capability failed, it does not yet supply an eligible surface for threshold selection and cannot adjudicate the main hypothesis.

## 2. Definitions

| Item | Operational definition | Role | Limitation |
|---|---|---|---|
| Standard-head answer accuracy | Fraction of held-out examples for which $q_1(h_{\text{SHARED}})$ predicts `ANSWER_Y`. | Primary learning curve. | Does not show causal intermediate-state use. |
| Steps to threshold | First 100-step evaluation checkpoint reaching a fixed accuracy $\tau$. Linear interpolation is not used. | Primary confirmation metric. | Undefined in calibration because $\tau$ is pending. |
| Capability gate | Both NTP and MTP must show non-floor learning on both task structures at the scale; the exact numerical rule is **pending user decision after calibration**. | Eligibility guard. | Cannot perfectly equalize intrinsic difficulty. |
| Intermediate-state probe | Frozen final hidden state at `DECIDE` or `SHARED`, decoded by a held-out ridge classifier for $B$. | Secondary formation diagnostic. | Readout is not causal use. |

## 3. Independent Variables

1. **Task structure:** single-step or ordered two-step.
2. **Training objective:** NTP or standard two-head MTP with $K=2$.
3. **Transformer depth:** 1, 2, or 4 layers.

The 1-layer model is diagnostic only. The two formal model scales are 2 and 4 layers.

## 4. Controlled Variables

- Sequence length: 9 tokens.
- Decision-to-answer distance: 2 tokens.
- State vocabulary: 32 states.
- Rule vocabulary: 8 deterministic bijections.
- Ordered rule-pair split: 48 train, 8 validation, 8 test pairs.
- Evaluation examples: every state for every validation/test rule pair.
- Hidden width 128, 4 attention heads, feed-forward width 512, dropout 0, pre-layer normalization, learned position embeddings.
- Same vocabulary, tokenizer, answer position, output entropy, batch size, optimizer, schedule, initialization seed, sampled training examples, and maximum steps for paired conditions.
- Both objectives instantiate and evaluate both prediction heads. NTP sets the second-head loss coefficient to zero; MTP sets it to one. This matches parameter count and forward computation, but not backward computation or gradient dose. Those remain explicit rival explanations.

## 5. Data Contract

Sequence layout:

```text
[BOS, DEPTH_1|DEPTH_2, STATE_A, RULE_r1, RULE_r2, DECIDE, SHARED, ANSWER_Y, EOS]
```

- Single-step: $Y=r_1(A)$. `RULE_r2` is present but does not determine the answer.
- Two-step: $B=r_1(A)$ and $Y=r_2(B)$.
- Rules are fixed random permutations generated once from data seed 1200.
- Ordered rule pairs are deterministically split once and reused by every condition.
- Training samples uniformly draw a train pair and a state.
- Validation and test enumerate the full Cartesian product of held-out pairs and states.

This construction controls length, answer distance, label cardinality, and rule-pair exposure. It does not prove that single-step and two-step optimization difficulty are identical.

## 6. Model and Objective Contract

The model is a causal decoder-only Transformer trained from random initialization.

For every token position $t$:

$$
L_{\mathrm{NTP}}=\operatorname{CE}(q_1(h_t),x_{t+1}),
$$

$$
L_{\mathrm{MTP}}=\operatorname{CE}(q_1(h_t),x_{t+1})+1.0\,\operatorname{CE}(q_2(h_t),x_{t+2}).
$$

$q_1$ is the common standard head. $q_2$ is architecturally present in both objectives and is never used to define the primary result.

## 7. Training Contract

| Setting | Calibration value |
|---|---:|
| Optimizer | AdamW |
| Learning rate | $10^{-3}$ |
| Minimum learning rate | $10^{-4}$ |
| Betas | $(0.9,0.95)$ |
| Weight decay | 0.01 |
| Warmup | 200 steps |
| Schedule | cosine decay |
| Gradient clipping | 1.0 |
| Batch size | 512 |
| Precision | FP32 |
| Maximum steps | 20,000 |
| Evaluation interval | 100 steps |
| Calibration seeds | 1201, 1202 |

Calibration contains $3\times2\times2\times2=24$ runs. Four GPUs execute independent run shards. Every run reaches the full step budget; there is no threshold-based early stopping.

Confirmation seeds 1301–1305 are reserved and must not be run before the threshold and capability rule are frozen.

## 8. Metrics and Decision Logic

### Primary metric for confirmation

For a fixed threshold $\tau$:

$$
T_{d,c,o}(\tau)=\min\{s: \operatorname{Acc}^{q_1}_{d,c,o}(s)\ge\tau\}.
$$

The MTP gain and structure interaction are

$$
G_{d,c}=T_{d,c,\mathrm{NTP}}-T_{d,c,\mathrm{MTP}},\qquad
\Gamma_d=G_{d,2}-G_{d,1}.
$$

The threshold $\tau$, the numerical capability gate, and any inferential tolerance are **pending user decision**. Calibration results must not be relabeled as confirmation after these choices.

### Secondary calibration outputs

- Full test and validation standard-head answer-accuracy curves.
- Final standard-head answer loss and accuracy.
- Second-head answer accuracy from `DECIDE`.
- Standard-head format-token accuracy.
- Final-checkpoint intermediate-state ridge-probe accuracy at `DECIDE` and `SHARED` for two-step runs.

## 9. Capability and Stop Conditions

### Calibration stop

- Stop after all 24 runs complete 20,000 steps and their artifacts aggregate, or after a reproducible implementation/infrastructure failure prevents completion.
- Do not stop when an accuracy threshold is crossed.
- Do not issue a supported/weakened mechanism verdict from calibration.

### Confirmation stop

After a revised calibration passes capability, confirmation remains blocked until the user fixes:

1. one standard-head answer-accuracy threshold;
2. the numerical capability gate;
3. treatment of a run that does not reach the threshold within 20,000 steps.

All three are marked **pending user decision**.

Calibration outcome: threshold selection is now blocked by capability failure, not merely pending a numerical preference. Any capability repair changes the evaluation-support contract and requires a new approved calibration revision.

## 10. Artifact Contract

Calibration outputs are written under:

```text
active/synthetic_data_understanding/results/
  a12_0_short_range_single_vs_two_step_calibration/<run_name>/
```

Required artifacts: configuration snapshot, deterministic data manifest, per-shard logs, complete learning-curve table, final-metric table, aggregate summary, and learning-curve figure. Job identifier and exact output path are appended after submission.

Execution record:

```text
job: pt-3okyxyjm
run: a12_0_short_composition_calibration_20260714_174654
result: active/synthetic_data_understanding/results/
  a12_0_short_range_single_vs_two_step_calibration/
  a12_0_short_composition_calibration_20260714_174654/
logs: active/synthetic_data_understanding/logs/acp/
  a12_0_short_composition_calibration_20260714_174654/
```

## 11. Self-Critique and Claim Guard

The design directly blocks sequence-length, answer-position, vocabulary-size, label-entropy, parameter-count, and forward-compute explanations. It does **not** fully block:

- extra backward compute and larger gradient dose under MTP;
- generic auxiliary-loss regularization;
- residual intrinsic difficulty differences between one and two rule applications;
- a probe-readable but unused intermediate state;
- threshold sensitivity.

Therefore the strongest possible result is a controlled structure-by-objective interaction in standard-head training speed. It is not yet a causal mechanism result and does not replace anchor `12_03`.
