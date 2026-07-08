# Long-Horizon Prediction and Next-k-Token Curriculum: Problem Definition, Mathematical Model, Formal Analysis, and Empirical Test

Created: 2026-07-06

## 1. Problem Definition

The central research question is whether multi-token prediction creates stronger learning pressure for long-horizon dependencies than ordinary next-token prediction.

Consider an extremely long context of length `T`, for example `T = 1,000,000`. The model observes:

```text
x_1, x_2, ..., x_T
```

and must predict:

```text
x_{T+1}
```

The prediction is long-horizon if `x_{T+1}` depends on an early token such as `x_1`, rather than only on the recent local context near `x_T`.

The simplest long-horizon dependency has the form:

`x_1 = branch key`, many filler tokens appear between the key and the prediction site, and `x_{T+1}` is determined by the branch key.

The stronger version, and the one most relevant to multi-token training, is:

`x_1 = branch key`, many filler tokens appear between the key and the prediction site, and a whole future suffix `x_{T+1:T+k}` is determined by the branch key.

The core hypothesis is:

**Next-k-token prediction can create stronger pressure than next-token prediction for the hidden state at position `T` to preserve early branch information, when multiple future tokens depend on the same early variable.**

Here, `next-k-token prediction` means that the same causal hidden state `h_T` is trained to predict several future tokens:

```text
h_T -> x_{T+1}
h_T -> x_{T+2}
...
h_T -> x_{T+k}
```

This differs from ordinary next-token language modeling, where the model is trained only to predict `x_{T+1}` from `h_T`.

## 2. Prior Intuition

Ordinary next-token prediction is not incapable of learning long-horizon dependencies. If `x_{T+1}` truly depends on `x_1`, then the next-token loss at position `T` does contain a long-horizon training signal.

The problem is signal dilution. In a long sequence, most next-token losses can be reduced by learning local structure:

```text
local syntax
local phrase continuation
local filler transitions
short-range semantic coherence
frequent templates
```

These local losses are dense and easy. They may dominate the optimization trajectory. The long-horizon signal exists, but it is sparse and can be weak relative to local gradients.

Next-k-token prediction changes the pressure at a prefix state. Instead of asking `h_T` to predict only the next token, it asks the same `h_T` to expose enough information for multiple future tokens. If those future tokens share the same early cause, then their losses create multiple aligned gradient signals toward preserving that early cause.

The important distinction is:

```text
next-token prediction:
  h_T only needs to support x_{T+1}

next-k-token prediction:
  h_T needs to support x_{T+1}, x_{T+2}, ..., x_{T+k}
```

If `x_{T+1:T+k}` is a branch-specific suffix, then next-k training increases the pressure for `h_T` to encode the branch key.

## 3. Minimal Generative Model

We define a controlled sequence distribution.

Let the early branch variable be:

**`B = X_1 \in \{1,2,\ldots,M\}`.**

Here, `B` is the first token or an early latent branch key; `M` is the number of possible branches.

The intermediate context is filler:

**`X_2,\ldots,X_T \sim P_{\mathrm{filler}}`.**

Here, `P_{\mathrm{filler}}` is a filler distribution that does not reveal the branch key. In the cleanest model, `X_2,\ldots,X_T` are conditionally independent of `B`.

The future suffix is determined by the branch:

**`Y_{1:k}=X_{T+1:T+k}=s_B`.**

Here, `Y_{1:k}` is the future suffix of length `k`, and `s_B` is the branch-specific suffix associated with branch `B`.

For example:

```text
B = BR_1 -> s_B = E F G H I J K L .
B = BR_2 -> s_B = M N O P Q R S T .
B = BR_3 -> s_B = U V W X Y Z AA AB .
```

The model is a causal sequence model. After reading the prefix, it produces a hidden state:

**`h_T=f_\theta(X_{\le T})`.**

Here, `h_T` is the hidden state at the prediction site, `f_\theta` is the causal Transformer or any causal encoder, and `X_{\le T}` is the observed context.

The question is whether `h_T` preserves the branch key `B` strongly enough to predict the suffix `s_B`.

## 4. Training Objectives

### 4.1 Ordinary next-token prediction

The next-token loss at the long-horizon position is:

**`L_1(\theta)=CE(p_{\theta,1}(Y_1\mid h_T),Y_1)`.**

Here, `Y_1=X_{T+1}` is the first future token, `p_{\theta,1}` is the offset-1 prediction distribution, and `CE` is cross-entropy.

This objective asks `h_T` to support only the first future token.

### 4.2 Next-k-token prediction

The next-k-token loss at the same prefix state is:

**`L_k(\theta)=\sum_{j=1}^{k}\lambda_j CE(p_{\theta,j}(Y_j\mid h_T),Y_j)`.**

Here, `Y_j=X_{T+j}` is the `j`-th future token, `p_{\theta,j}` is the prediction distribution for offset `j`, and `\lambda_j` is the weight assigned to offset `j`.

For the simplest version, set all weights to one:

**`\lambda_1=\lambda_2=\cdots=\lambda_k=1`.**

This objective asks the same hidden state `h_T` to support the full future suffix.

### 4.3 Deterministic curriculum next-k objective

A deterministic curriculum gradually increases the active horizon:

**`h(t)=\min(1+\lfloor t/S\rfloor,k_{\max})`.**

Here, `t` is the training step, `S` is the number of steps per horizon stage, and `k_{\max}` is the maximum prediction horizon.

The training loss at step `t` is:

**`L_{h(t)}(\theta)=\sum_{j=1}^{h(t)}\lambda_j CE(p_{\theta,j}(Y_j\mid h_T),Y_j)`.**

This objective begins as ordinary next-token prediction and periodically adds pressure from farther future tokens.

## 5. Formal Analysis: Gradient Signal Amplification

### 5.1 Branch-relevant gradient decomposition

Assume there is a branch-memory direction in representation space. Write the hidden state as:

**`h_T = u_B m_T + \epsilon_T`.**

Here, `u_B` is a direction or subspace carrying branch information, `m_T` is the strength of the memory of `B`, and `\epsilon_T` is the branch-irrelevant part of the representation.

For each future offset `j`, decompose the gradient with respect to `h_T` into a branch-relevant component and a residual component:

**`\nabla_{h_T} \ell_j = \alpha_j u_B + \eta_j`.**

Here, `\ell_j=CE(p_{\theta,j}(Y_j\mid h_T),Y_j)`, `\alpha_j u_B` is the component that pushes the model to encode or expose the branch key, and `\eta_j` is the branch-irrelevant or noisy component.

The next-token gradient is:

**`\nabla_{h_T} L_1 = \alpha_1 u_B + \eta_1`.**

The next-k-token gradient is:

**`\nabla_{h_T} L_k = \sum_{j=1}^{k}\lambda_j\alpha_j u_B + \sum_{j=1}^{k}\lambda_j\eta_j`.**

The branch-relevant signal magnitude is therefore proportional to:

**`A_k=\sum_{j=1}^{k}\lambda_j\alpha_j`.**

Here, `A_k` is the total branch-relevant gradient coefficient under next-k training.

If every active future token carries positive information about the branch, then `\alpha_j>0` for those offsets. Therefore:

**`A_k>A_1` for `k>1`.**

This is the basic gradient amplification result.

### 5.2 Theorem 1: next-k increases branch-relevant gradient under aligned future supervision

**Theorem 1.** Suppose future tokens `Y_1,\ldots,Y_k` are all branch-dependent, and their prediction losses produce branch-relevant gradient components with nonnegative coefficients `\alpha_j\ge 0`. If at least one future offset beyond the first has `\alpha_j>0`, then the next-k objective has strictly larger branch-relevant gradient magnitude than the next-token objective.

**Proof.** The branch-relevant coefficient for next-token prediction is `A_1=\alpha_1`. The branch-relevant coefficient for next-k prediction is `A_k=\sum_{j=1}^{k}\lambda_j\alpha_j`. If `\lambda_j>0`, `\alpha_j\ge 0`, and at least one `\alpha_j>0` for `j>1`, then `A_k=\alpha_1+\sum_{j=2}^{k}\lambda_j\alpha_j>\alpha_1=A_1`. Therefore next-k has a larger branch-relevant component. This proves the claim.

This theorem is intentionally simple. It captures the mechanism: multiple future losses that depend on the same early branch variable add aligned pressure to preserve that variable in `h_T`.

## 6. Formal Analysis: Signal-to-Noise Ratio

The previous theorem shows that the branch-relevant signal increases. But optimization depends on the ratio between branch-relevant signal and irrelevant gradient noise.

Define the branch signal-to-noise ratio as:

**`\mathrm{SNR}_k = \frac{\left\|\sum_{j=1}^{k}\lambda_j\alpha_j u_B\right\|}{\left(\mathbb{E}\left\|\sum_{j=1}^{k}\lambda_j\eta_j\right\|^2\right)^{1/2}}`.**

Here, the numerator is the norm of the aligned branch gradient, and the denominator is the root-mean-square norm of the branch-irrelevant gradient.

Assume residual gradients `\eta_j` are mean-zero and weakly correlated across offsets. Then the residual noise grows approximately as the square root of the number of offsets, while aligned branch signal grows approximately linearly:

**`\left\|\sum_{j=1}^{k}\lambda_j\alpha_j u_B\right\| \approx \sum_{j=1}^{k}\lambda_j\alpha_j`.**

**`\left(\mathbb{E}\left\|\sum_{j=1}^{k}\lambda_j\eta_j\right\|^2\right)^{1/2} \approx \left(\sum_{j=1}^{k}\lambda_j^2\sigma_j^2\right)^{1/2}`.**

Here, `\sigma_j^2=\mathbb{E}\|\eta_j\|^2` is the residual gradient variance for offset `j`.

If `\alpha_j=\alpha`, `\sigma_j=\sigma`, and `\lambda_j=1`, then:

**`\mathrm{SNR}_k \approx \frac{k\alpha}{\sqrt{k}\sigma}=\sqrt{k}\frac{\alpha}{\sigma}`.**

This gives a stronger result: next-k prediction improves the relative strength of the long-horizon branch signal by approximately `\sqrt{k}` under aligned signal and weakly correlated noise.

### Theorem 2: next-k improves branch SNR under independent residual noise

**Theorem 2.** Suppose each future offset contributes the same branch-relevant coefficient `\alpha>0`, and the branch-irrelevant residual gradients have equal variance `\sigma^2` and are uncorrelated across offsets. Then the branch-relevant gradient SNR under next-k prediction is `\sqrt{k}` times the SNR under next-token prediction.

**Proof.** For next-token prediction, the branch signal is `\alpha` and the residual noise scale is `\sigma`, so `\mathrm{SNR}_1=\alpha/\sigma`. For next-k prediction, the aligned branch signal is `k\alpha`. The independent residual noise scale is `\sqrt{k}\sigma`. Therefore `\mathrm{SNR}_k=k\alpha/(\sqrt{k}\sigma)=\sqrt{k}\alpha/\sigma=\sqrt{k}\mathrm{SNR}_1`. This proves the claim.

This theorem formalizes why multi-token prediction can be better for long-horizon learning: it can increase the relative strength of the branch-relevant gradient even when each individual future token is only weakly informative.

## 7. Formal Analysis: Information-Theoretic Pressure

Gradient analysis explains optimization pressure. Information theory explains representation requirements.

If the model can predict the future suffix `Y_{1:k}` from `h_T`, then `h_T` must contain information about the branch variable `B`, because `Y_{1:k}` is determined by `B`.

The data processing inequality gives:

**`I(B;h_T) \ge I(B;\hat{Y}_{1:k})` only when `\hat{Y}_{1:k}` is a recoverable function of `h_T` and the predictor is sufficiently accurate.**

A more operational statement uses prediction accuracy. If the branch suffixes are disjoint and the model predicts the correct suffix with error probability `p_e`, then Fano-style reasoning implies:

**`I(h_T;B) \ge \log M - H(p_e)-p_e\log(M-1)`.**

Here, `M` is the number of branches, `p_e` is the probability of choosing the wrong branch suffix from `h_T`, and `H(p_e)` is the binary entropy of the error event.

This means that high-accuracy single-prefix suffix prediction forces `h_T` to contain information about `B`.

Now compare next-token and next-k objectives. If only `Y_1` is supervised, the representation only needs to preserve information sufficient for the first future token. If the full suffix `Y_{1:k}` is supervised and suffixes are branch-specific, the representation must preserve information sufficient to distinguish the branch across the whole suffix.

The key monotonicity fact is:

**`I(B;Y_{1:k}) \ge I(B;Y_1)`.**

This follows from the chain rule for mutual information:

**`I(B;Y_{1:k}) = I(B;Y_1)+I(B;Y_{2:k}\mid Y_1)`.**

Since conditional mutual information is nonnegative, adding future tokens cannot reduce information about the branch.

### Theorem 3: multi-token suffix prediction imposes a stronger information requirement

**Theorem 3.** If future suffix tokens `Y_{1:k}` contain additional branch information beyond `Y_1`, meaning `I(B;Y_{2:k}\mid Y_1)>0`, then successful next-k prediction requires the hidden state `h_T` to expose more branch information than successful next-token prediction.

**Proof.** By the chain rule, `I(B;Y_{1:k})=I(B;Y_1)+I(B;Y_{2:k}\mid Y_1)`. If `I(B;Y_{2:k}\mid Y_1)>0`, then `I(B;Y_{1:k})>I(B;Y_1)`. A predictor that accurately recovers `Y_{1:k}` from `h_T` must encode enough branch information in `h_T` to distinguish the suffix. Therefore the representation requirement under next-k prediction is stronger than under next-token prediction. This proves the claim.

This theorem is especially relevant when the first future token is ambiguous or only weakly branch-specific, but the multi-token suffix is highly branch-specific.

## 8. Important Counterexamples and Claim Boundary

The desired claim is not universally true. The following counterexamples must be stated explicitly.

### Counterexample 1: the second token carries no branch information

If `Y_2` is independent of `B` given the local context, then its loss does not add branch-relevant signal. In the gradient notation, `\alpha_2=0`. Then next-two prediction does not improve long-horizon branch pressure.

### Counterexample 2: future losses create conflicting gradients

If `Y_1` and `Y_2` require incompatible features, their gradients may not align. In that case, adding `Y_2` can add optimization noise or interference rather than useful branch pressure.

### Counterexample 3: the next-token target already identifies the branch perfectly

If `Y_1` alone uniquely identifies `B`, and the model can already learn it easily, then next-k may not improve final accuracy. It may still affect training speed or spectral geometry, but the behavioral gain can saturate.

### Valid claim boundary

The rigorous claim should be:

**Next-k-token prediction is expected to improve long-horizon learning over next-token prediction when multiple future tokens share a common early cause and their branch-relevant gradients are positively aligned.**

This is a conditional theorem and a falsifiable empirical hypothesis, not an unconditional guarantee.

## 9. Connection to Real-World LLM Learning

In real LLM pretraining, long-horizon dependencies often have the same structure as the synthetic branch model.

Examples include:

```text
a character introduced early in a story controls later pronoun resolution
a variable defined early in a program controls later code generation
a legal condition introduced early in a contract controls a later clause
a user instruction at the beginning of a prompt controls a later answer format
a theorem assumption introduced early controls a later proof step
```

The local context near the prediction site may be insufficient. The model must preserve an earlier latent variable across many intervening tokens.

Ordinary next-token loss contains the signal in principle. However, most token positions reward local continuation. Multi-token prediction can increase pressure on a prefix hidden state to expose more of the future semantic continuation.

The synthetic branch dataset is a controlled laboratory version of this real challenge:

```text
BR_k ... A B C D -> suffix_k
```

Here, `BR_k` corresponds to an early semantic condition, `A B C D` corresponds to a shared local context, and `suffix_k` corresponds to the future continuation determined by the early condition.

The desired empirical signature is:

```text
standard next-token training:
  strong teacher-forced continuation
  weak single-prefix suffix prediction

next-k curriculum training:
  stronger single-prefix suffix prediction
  lower suffix-only loss after branch-specific horizons activate
  higher minimum target probability over the branch-specific suffix
```

## 10. Small Empirical Test

### 10.1 Dataset

Use a branch-controlled suffix dataset.

Template:

```text
BR_k F00 F01 ... F{m-1} A B C D R00 R01 ... R{d-1} suffix_k .
```

Recommended V1 parameters:

```text
num_branches = 3
branch_delay_len = 8
post_prefix_delay_len = 4
shared_prefix_len = 4
suffix_len = 8
max_horizon = 13
sequence_length = 96
structured_example_probability = 0.30
random_filler_probability = 0.70
```

The reason `max_horizon = 13` is:

```text
offsets 1..4: distractor tokens R00 R01 R02 R03
offsets 5..12: branch-specific suffix tokens
offset 13: stop token .
```

The first branch-specific horizon activates at:

**`h_{\mathrm{branch}}=\mathrm{post\_prefix\_delay\_len}+1=5`.**

With horizon interval `S = 100`, this occurs at step 400.

### 10.2 Model conditions

Use within-architecture comparisons.

```text
standard_lm + standard_next_token

direct_heads + fixed_next_token
direct_heads + deterministic_curriculum_next_k
direct_heads + fixed_full_horizon

latent_decoder + fixed_next_token
latent_decoder + deterministic_curriculum_next_k
latent_decoder + fixed_full_horizon
```

The key comparisons are:

```text
direct_heads:
  fixed_next_token vs deterministic_curriculum_next_k vs fixed_full_horizon

latent_decoder:
  fixed_next_token vs deterministic_curriculum_next_k vs fixed_full_horizon
```

For `fixed_next_token`, keep the full architecture unchanged and only fix `active_horizon = 1`.

### 10.3 Metrics

Primary prediction metrics:

```text
single_prefix_exact_match_suffix_only
single_prefix_min_prob_suffix_only
single_prefix_mean_prob_suffix_only
worst_branch_suffix_only_min_prob
branch_swap_suffix_preference
```

Primary training dynamics:

```text
global_active_loss
structured_active_loss
random_active_loss
single_prefix_suffix_loss
single_prefix_suffix_loss_by_offset
loss_by_offset_all_positions
```

Diagnostic metrics:

```text
teacher_forced_exact_match
autoregressive_rollout_exact_match
single_prefix_exact_match_all_offsets
```

Spectral diagnostics:

```text
singular values of LM head
singular values of direct future heads
singular values of decoder output head
singular values of encoder attention matrices
singular values of decoder self-attention and cross-attention matrices
```

### 10.4 Expected result pattern

Strong support for the hypothesis occurs if, within the same architecture:

```text
deterministic_curriculum_next_k > fixed_next_token
```

on suffix-only single-prefix metrics, especially:

```text
single_prefix_exact_match_suffix_only
single_prefix_min_prob_suffix_only
worst_branch_suffix_only_min_prob
```

and if training curves show:

```text
new horizon activation -> active loss jump -> newly activated offset loss decreases
```

especially after `h = 5`, the first branch-specific horizon.

A useful but weaker result occurs if curriculum improves over fixed-next-token but does not beat fixed-full-horizon. This would show that multi-token supervision matters, while the curriculum schedule may not be better than full-horizon training from step 0.

A negative result occurs if teacher-forced continuation is strong but single-prefix suffix-only prediction remains weak. This would indicate that the model learned local continuation chains but did not store the branch-specific suffix in `h_D`.

## 11. What Would Count as a Formal Empirical Falsification?

The hypothesis would be weakened if all of the following hold across seeds:

```text
fixed_next_token matches curriculum on suffix-only single-prefix prediction
curriculum does not reduce single_prefix_suffix_loss after branch-specific horizons activate
branch-swap suffix preference does not improve under curriculum
spectral diagnostics show no consistent difference in output-facing geometry
```

The hypothesis would also be weakened if improvement appears only in teacher-forced continuation but not in single-prefix metrics. That would mean the training method improves local rollout rather than long-horizon representation.

## 12. Summary

The theoretical mechanism is conditional but precise.

Next-token prediction contains long-horizon signal when the next token depends on an early variable. However, this signal can be diluted by many local losses.

Next-k-token prediction strengthens long-horizon learning when multiple future tokens depend on the same early variable. In that case, several future losses create aligned branch-relevant gradients on the same prefix hidden state. Under independent residual noise, the branch signal-to-noise ratio can improve by approximately `\sqrt{k}`. From an information-theoretic view, accurate suffix prediction requires the hidden state to contain enough information about the early branch key.

The empirical test should therefore focus on single-prefix suffix prediction, not ordinary perplexity alone.

The concise claim is:

**In branch-controlled suffix distributions, deterministic next-k-token curriculum can create stronger pressure than ordinary next-token prediction for a causal hidden state to preserve and expose long-horizon branch information.**
