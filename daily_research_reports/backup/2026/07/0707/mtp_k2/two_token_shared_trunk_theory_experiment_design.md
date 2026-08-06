# Two-Token Prediction, Shared-Trunk Gradient Interaction, and Minimal One-Layer Transformer Experiment

Created: 2026-07-07

## 1. Problem Definition

The goal is to understand, in the simplest possible setting, how multi-token prediction changes representation learning compared with ordinary next-token prediction.

The specific question is not whether a model can predict future tokens in principle. Ordinary next-token prediction already contains long-horizon signal whenever the next token depends on a distant earlier variable. The more precise question is:

**Does predicting an additional future token create useful learning pressure for a shared causal trunk, or does it inject difficult, noisy, or interfering gradients into the same shared representation?**

This matters because the multi-token prediction architecture uses one shared trunk and multiple prediction heads. For two-token prediction, the same hidden state must support both:

**$h_t \rightarrow x_{t+1}$**.

Here, $h_t$ is the causal hidden state after reading prefix $x_{\le t}$, and $x_{t+1}$ is the next token.

**$h_t \rightarrow x_{t+2}$**.

Here, the same $h_t$ is also asked to predict the second future token $x_{t+2}$, even though the intermediate token $x_{t+1}$ has not yet been revealed to the model at position $t$.

This design creates a central theoretical tension. The second-token loss may help if $x_{t+2}$ depends on a latent long-horizon variable already present in the prefix. But it may hurt if $x_{t+2}$ is too uncertain from $x_{\le t}$, or if its gradient conflicts with the next-token gradient on shared trunk parameters.

Our objective is to build a minimal theory and a minimal experiment that distinguish these possibilities.

## 2. How Two-Token Training Actually Feeds Data

Two-token prediction does not consume the training corpus two tokens at a time. It still uses the standard causal language-modeling layout, sliding one token at a time.

Given a token sequence:

$x_1,x_2,\ldots,x_T$,

ordinary next-token prediction trains each position $t$ to predict $x_{t+1}$. Two-token prediction trains each position $t$ to predict both $x_{t+1}$ and $x_{t+2}$.

The training targets are therefore overlapping:

| Position | Prefix represented by trunk | Head 1 target | Head 2 target |
|---|---|---|---|
| $t$ | $x_{\le t}$ | $x_{t+1}$ | $x_{t+2}$ |
| $t+1$ | $x_{\le t+1}$ | $x_{t+2}$ | $x_{t+3}$ |
| $t+2$ | $x_{\le t+2}$ | $x_{t+3}$ | $x_{t+4}$ |

Thus $x_{t+2}$ appears twice as a supervised target: once as the second-token target from prefix $x_{\le t}$, and once as the next-token target from prefix $x_{\le t+1}$.

This duplicate-target structure is important. The two distributions are not supposed to be identical, because they condition on different information:

**$p^{(2)}_\theta(x_{t+2}\mid x_{\le t})$**.

Here, $p^{(2)}_\theta$ is the second-token head, which predicts $x_{t+2}$ before seeing $x_{t+1}$.

**$p^{(1)}_\theta(x_{t+2}\mid x_{\le t+1})$**.

Here, $p^{(1)}_\theta$ is the next-token head, which predicts the same token after $x_{t+1}$ has been revealed.

The correct probabilistic relationship is a refinement relationship, not equality:

**$p(x_{t+2}\mid x_{\le t})=\sum_a p(x_{t+2}\mid x_{\le t},x_{t+1}=a)p(x_{t+1}=a\mid x_{\le t})$**.

Here, $a$ ranges over possible next tokens. This equation follows from the law of total probability. It says that the second-token prediction from $x_{\le t}$ is a marginal forecast over possible next-token branches, while the next-token prediction at $t+1$ is a refined forecast after the actual next token has been revealed.

This gives a sharper interpretation of the second-token loss. It is not merely asking the model to guess a farther token. It asks the current hidden state $h_t$ to encode enough information to forecast the future continuation distribution before the intermediate token is known.

## 3. Minimal Mathematical Model

We use a branch-controlled sequence distribution because it isolates the kind of long-horizon dependency that multi-token prediction is supposed to help.

Let $B$ be an early branch variable:

**$B\in\{1,2,\ldots,M\}$**.

Here, $B$ is the latent or explicit branch key, and $M$ is the number of possible branches.

The model observes a long prefix containing $B$, followed by filler tokens that do not reveal new branch information. Near the prediction site, all branches share the same local context. Then the future suffix depends on $B$:

**$Y_{1:k}=X_{T+1:T+k}=s_B$**.

Here, $Y_{1:k}$ is the future suffix, $s_B$ is the branch-specific suffix, and $T$ is the prediction position.

A typical synthetic sequence is:

```text
BR_i  filler filler filler ...  A B C D  R0 R1  suffix_i
```

The shared local context $A B C D$ is deliberately identical across branches. Therefore, a model that relies only on local context cannot know which suffix should follow. It must preserve information about $BR_i$.

The causal trunk produces:

**$h_T=f_{\theta_s}(x_{\le T})$**.

Here, $f_{\theta_s}$ is the shared trunk with parameters $\theta_s$, and $h_T$ is the hidden state used by the prediction heads.

For two-token prediction, the losses at position $T$ are:

**$L_1=\mathrm{CE}(p^{(1)}_\theta(Y_1\mid h_T),Y_1)$**.

Here, $L_1$ is next-token cross-entropy, $p^{(1)}_\theta$ is the offset-1 head, and $Y_1=X_{T+1}$.

**$L_2=\mathrm{CE}(p^{(2)}_\theta(Y_2\mid h_T),Y_2)$**.

Here, $L_2$ is second-token cross-entropy, $p^{(2)}_\theta$ is the offset-2 head, and $Y_2=X_{T+2}$.

The combined two-token objective is:

**$L=L_1+\lambda L_2$**.

Here, $\lambda$ controls how strongly the second-token loss contributes.

## 4. What Does the Future-Token Gradient Mean?

The gradient from $L_1$ says: update the model so that $h_T$ better predicts the immediate next token $Y_1$.

The gradient from $L_2$ says: update the model so that $h_T$ better predicts $Y_2$ before $Y_1$ is observed.

These are not equivalent learning signals. If $Y_2$ depends on the same branch variable $B$ as $Y_1$, then $L_2$ may push $h_T$ to preserve $B$. If $Y_2$ is random or mostly determined by $Y_1$, then $L_2$ may be noisy from the perspective of $h_T$.

The relevant shared-trunk gradients are:

**$g_1=\nabla_{\theta_s}L_1,\quad g_2=\nabla_{\theta_s}L_2$**.

Here, $g_1$ is the next-token gradient on shared parameters, and $g_2$ is the second-token gradient on the same shared parameters.

The combined shared-trunk update direction is:

**$g=g_1+\lambda g_2$**.

Here, $g$ is the gradient used by two-token training on shared parameters.

The first-order effect of adding $L_2$ on next-token optimization is determined by:

**$\langle g_1,g\rangle=\|g_1\|^2+\lambda\langle g_1,g_2\rangle$**.

Here, $\langle g_1,g\rangle$ measures whether the combined update preserves progress along the next-token gradient. This equation follows from expanding the inner product between $g_1$ and $g_1+\lambda g_2$.

If $\langle g_1,g_2\rangle>0$, the second-token loss is locally compatible with next-token learning on shared parameters. If $\langle g_1,g_2\rangle<0$, the second-token loss interferes with next-token learning. If the inner product is close to zero but $\|g_2\|$ is large, the second-token gradient may behave like high-variance auxiliary noise.

This is not yet the whole story. A second-token gradient can interfere with $L_1$ and still be useful for long-horizon representation, or it can be compatible with $L_1$ but irrelevant to the branch variable. Therefore we need a second diagnostic: whether $L_2$ increases branch information in $h_T$.

Let $S_\phi(h_T)$ be a linear probe or classifier trained to recover $B$ from $h_T$. Define a branch-recovery objective:

**$R_\phi=\mathrm{CE}(S_\phi(h_T),B)$**.

Here, lower $R_\phi$ means branch information is more recoverable from $h_T$.

The useful long-horizon representation condition is:

**$\langle \nabla_{\theta_s}R_\phi,g_2\rangle>0$** under gradient descent on $L_2$ if both gradients are defined as loss gradients.

Here, $g_2=\nabla_{\theta_s}L_2$. Since gradient descent moves in direction $-g_2$, the branch-recovery loss $R_\phi$ decreases when $\langle \nabla_{\theta_s}R_\phi,g_2\rangle>0$. This is a first-order Taylor statement: moving by $-\eta g_2$ changes $R_\phi$ by approximately $-\eta\langle \nabla R_\phi,g_2\rangle$.

Thus $L_2$ is useful for long-horizon representation if it points in a direction that reduces branch-probe loss, even if it is not always aligned with $L_1$.

## 5. Target-Level Information: When Should $L_2$ Help?

The second-token loss cannot help long-horizon representation unless $Y_2$ contains branch information not already captured by local continuation.

A clean data-level condition is:

**$I(B;Y_2\mid Y_1)>0$**.

Here, $I(B;Y_2\mid Y_1)$ is conditional mutual information. It measures whether the second future token contains information about the branch variable $B$ beyond the first future token $Y_1$.

If $I(B;Y_2\mid Y_1)=0$, then $Y_2$ adds no branch information once $Y_1$ is known. In that case, the second-token loss may still help local continuation, but it should not add a new long-horizon branch signal.

If $I(B;Y_2\mid Y_1)>0$, then successful two-token prediction has a stronger information requirement than next-token prediction alone.

For a suffix of length $k$, the monotonic information statement is:

**$I(B;Y_{1:k})=I(B;Y_1)+I(B;Y_{2:k}\mid Y_1)$**.

Here, the second term is nonnegative by the chain rule for mutual information. Therefore adding future suffix tokens cannot reduce branch information, and it increases branch information when $I(B;Y_{2:k}\mid Y_1)>0$.

This explains when multi-token prediction has a principled reason to help: the future tokens must reveal a shared latent cause that is not already fully revealed by the immediate next token.

## 6. Hidden-State and Shared-Trunk Interaction

There are two different places where horizon losses can interact.

First, they interact at the hidden state:

**$c_h=\frac{\langle \nabla_{h_T}L_1,\nabla_{h_T}L_2\rangle}{\|\nabla_{h_T}L_1\|\|\nabla_{h_T}L_2\|}$**.

Here, $c_h$ measures whether the two heads ask the same hidden state to move in compatible directions.

Second, they interact after passing through the shared trunk Jacobian:

**$c_s=\frac{\langle \nabla_{\theta_s}L_1,\nabla_{\theta_s}L_2\rangle}{\|\nabla_{\theta_s}L_1\|\|\nabla_{\theta_s}L_2\|}$**.

Here, $c_s$ measures whether the two horizon losses cooperate or conflict on shared trunk parameters.

The chain rule links them:

**$\nabla_{\theta_s}L_j=J_{\theta_s}(h_T)^\top\nabla_{h_T}L_j$**.

Here, $J_{\theta_s}(h_T)$ is the Jacobian of the hidden state with respect to shared parameters. This equation explains why hidden-state alignment and shared-parameter alignment are not necessarily identical. The trunk geometry can amplify, suppress, or rotate horizon-specific gradients.

This is the core reason we need profiling rather than verbal explanation. Multi-token prediction may be useful at the target-information level but still difficult at the shared-optimization level.

## 7. Expert Separation: What It Can and Cannot Fix

Our design adds separate experts for different prediction horizons. This changes the gradient interaction structure.

A simplified parameter decomposition is:

**$\theta=(\theta_{\mathrm{attn}},\theta_{e,1},\theta_{e,2},\theta_{h,1},\theta_{h,2})$**.

Here, $\theta_{\mathrm{attn}}$ is the shared self-attention trunk, $\theta_{e,1}$ and $\theta_{e,2}$ are horizon-specific expert parameters, and $\theta_{h,1}$ and $\theta_{h,2}$ are output heads.

Under a separated-expert design, $L_1$ updates $\theta_{e,1}$ and $\theta_{h,1}$, while $L_2$ updates $\theta_{e,2}$ and $\theta_{h,2}$. But both losses still update the shared attention parameters $\theta_{\mathrm{attn}}$, unless attention is also separated.

Therefore expert separation can reduce interference in expert or MLP subspaces, but it cannot fully remove interference in shared attention.

This gives a falsifiable mechanism:

If the harmful interaction between $L_1$ and $L_2$ is mainly located in expert/MLP parameters, then separate experts should preserve next-token performance while allowing $L_2$ to learn branch-relevant features.

If the harmful interaction is mainly located in shared attention, then separate experts will not fully solve the problem. We should still observe negative or unstable $c_s$ on $\theta_{\mathrm{attn}}$.

## 8. Theoretical Claim Boundary

The theory should not claim that two-token prediction always helps. The valid claim is conditional.

**Claim.** Two-token prediction should improve long-horizon representation when $Y_2$ contains additional branch information, when the second-token gradient increases branch recoverability from $h_T$, and when its projected gradient on shared trunk parameters is not destructively opposed to the next-token gradient.

This claim depends on three measurable conditions:

**$I(B;Y_2\mid Y_1)>0$**.

This is the data-level condition: the second future token must contain additional branch information.

**$\langle \nabla_{\theta_s}R_\phi,g_2\rangle>0$**.

This is the representation condition: descending $L_2$ should reduce branch-probe loss.

**$\langle g_1,g_2\rangle$ is not strongly negative on critical shared parameters.**

This is the optimization condition: the second-token gradient should not destroy the next-token update direction in the shared trunk.

These conditions also produce clean falsification criteria. If $Y_2$ contains branch information but $g_2$ does not increase branch recoverability, then the model is failing to use the future supervision. If $g_2$ increases branch recoverability but strongly conflicts with $g_1$, then two-token prediction may help long-horizon features while hurting local next-token learning. If expert separation fixes the conflict outside attention but not inside attention, then the remaining bottleneck is the shared attention layer.

## 9. Minimal Experiment

The simplest experiment should use a one-layer causal Transformer and two-token prediction. The purpose is not to beat a benchmark. The purpose is to expose the interaction between future-token supervision, shared representations, and expert separation.

### 9.1 Dataset

Use a branch-controlled suffix dataset with three regimes.

#### Regime A: useful second-token branch signal

Each sequence contains an early branch key and a shared local prefix before the prediction site:

```text
BR_i  F_1 F_2 ... F_m  A B C D  Y_1^{(i)} Y_2^{(i)}
```

Both $Y_1^{(i)}$ and $Y_2^{(i)}$ depend on $BR_i$. This regime tests whether two-token prediction strengthens branch memory.

A stronger variant makes $Y_1$ partially ambiguous but $Y_2$ branch-specific:

```text
BR_1 ... A B C D  U  P
BR_2 ... A B C D  U  Q
BR_3 ... A B C D  U  R
```

In this variant, next-token prediction at the branch point sees the same $Y_1=U$ across branches, while second-token prediction must distinguish $P,Q,R$. This directly tests whether $L_2$ creates branch-learning pressure that $L_1$ lacks.

#### Regime B: redundant second-token signal

Both $Y_1$ and $Y_2$ are locally predictable, and $Y_2$ adds little branch information beyond $Y_1$. This regime tests whether two-token prediction is merely redundant.

#### Regime C: noisy second-token target

$Y_1$ is predictable, but $Y_2$ is random or independent of $B$ given the prefix. This regime tests whether the proposed diagnostics can identify harmful or useless future-token supervision.

### 9.2 Model Conditions

Train the following models with identical data and optimizer settings.

| Condition | Description | Purpose |
|---|---|---|
| NTP baseline | one-layer Transformer, one head, loss $L_1$ | baseline local and branch learning |
| Shared-trunk two-token | one-layer Transformer, shared trunk, two heads, loss $L_1+\lambda L_2$ | test ordinary two-token interaction |
| Shared-attention separate-expert | shared attention, separate horizon experts, two heads | test whether expert separation reduces interference |
| Fully separated control | separate branches after embedding or after attention | upper-bound separation benefit |

The main comparison is between the NTP baseline, the shared-trunk two-token model, and the shared-attention separate-expert model.

### 9.3 Architecture

Use a minimal one-layer causal Transformer:

```text
token embedding + position embedding
one causal self-attention layer
one MLP or expert block
LayerNorm / residual path
prediction head(s)
```

For the shared-trunk two-token model:

```text
shared attention + shared MLP -> h_t
h_t -> head_1 -> x_{t+1}
h_t -> head_2 -> x_{t+2}
```

For the separate-expert model:

```text
shared attention -> a_t
expert_1(a_t) -> h_t^{(1)} -> head_1 -> x_{t+1}
expert_2(a_t) -> h_t^{(2)} -> head_2 -> x_{t+2}
```

This architecture isolates the question: does separating the horizon-specific MLP/expert subspace reduce conflict while leaving attention shared?

### 9.4 Training Setup

Use small models and short runs so that many seeds can be tested quickly.

Recommended default settings:

| Parameter | Suggested value |
|---|---:|
| vocab size | 64 to 128 |
| number of branches | 3 to 8 |
| sequence length | 64 or 128 |
| branch delay | 16 to 64 tokens |
| model dimension | 64 or 128 |
| attention heads | 2 or 4 |
| layers | 1 |
| batch size | 128 or 256 |
| training steps | 5k to 20k |
| optimizer | AdamW |
| learning rate | $10^{-3}$ to $3\times 10^{-4}$ |
| seeds | at least 5 |
| $\lambda$ for $L_2$ | 0.25, 0.5, 1.0 |

The run should be cheap enough that Codex can implement it and run sweeps over regimes, seeds, and $\lambda$.

## 10. What to Monitor

The experiment should monitor ordinary losses, long-horizon behavior, and gradient geometry.

### 10.1 Basic Loss Metrics

Track:

**$L_1$**: next-token loss.

**$L_2$**: second-token loss.

**$L_1+\lambda L_2$**: total active training loss.

These should be logged separately for all tokens and for structured branch-controlled positions only. The structured-position metrics are more important than global average loss, because global loss can be dominated by filler tokens.

### 10.2 Branch-Specific Prediction Metrics

At the shared local context position, evaluate whether the model predicts the branch-specific suffix from the single prefix.

Monitor:

```text
single_prefix_head1_accuracy
single_prefix_head2_accuracy
single_prefix_joint_two_token_accuracy
branch_suffix_exact_match
branch_swap_preference
```

The most important metric is head-2 branch accuracy in the ambiguous-$Y_1$ regime. If $Y_1$ is identical across branches but $Y_2$ differs, ordinary next-token loss has no direct branch signal at that position, while two-token loss does.

### 10.3 Duplicate-Target Refinement Metrics

Because $x_{t+2}$ is predicted by head 2 at position $t$ and by head 1 at position $t+1$, monitor their relationship.

Define:

**$D_t=\mathrm{KL}\left(p^{(1)}_\theta(\cdot\mid x_{\le t+1})\,\|\,p^{(2)}_\theta(\cdot\mid x_{\le t})\right)$**.

Here, $D_t$ measures how much the refined next-token distribution at $t+1$ differs from the earlier second-token distribution at $t$. Large $D_t$ means the intermediate token $x_{t+1}$ reveals substantial information about $x_{t+2}$.

Define:

**$G_t=-\log p^{(2)}_\theta(x_{t+2}\mid x_{\le t})+\log p^{(1)}_\theta(x_{t+2}\mid x_{\le t+1})$**.

Here, $G_t$ is the refinement gain: how much easier the target becomes after revealing $x_{t+1}$. High $G_t$ positions are positions where the second-token task is intrinsically harder than the next-token task one step later.

These metrics turn the vague statement “future-token prediction is hard” into a measurable quantity.

### 10.4 Gradient Interaction Metrics

At profiling intervals, compute gradients from $L_1$ and $L_2$ separately before the optimizer step.

For each parameter group, compute:

**$c_s=\frac{\langle g_1,g_2\rangle}{\|g_1\|\|g_2\|}$**.

Here, $g_1$ and $g_2$ are gradients on the same parameter group from $L_1$ and $L_2$, respectively.

Compute $c_s$ separately for:

```text
embedding parameters
shared attention parameters
shared MLP parameters
expert_1 parameters
expert_2 parameters
head_1 parameters
head_2 parameters
```

For separated experts, cross-horizon expert gradient conflict should be absent or strongly reduced by construction. The remaining important interaction is in embeddings and shared attention.

Also monitor:

**$r=\frac{\|g_2\|}{\|g_1\|}$**.

Here, $r$ measures whether the second-token gradient is too large or too small relative to the next-token gradient.

**$\rho=\frac{\langle g_1+\lambda g_2,g_1\rangle}{\|g_1\|^2}$**.

Here, $\rho$ measures how much the combined update preserves the next-token update direction. If $\rho<1$, the second-token gradient weakens next-token progress. If $\rho<0$, it reverses the next-token direction.

### 10.5 Representation Metrics

Train or periodically fit a linear probe from $h_T$ to branch label $B$:

```text
branch_probe_accuracy
branch_probe_cross_entropy
```

Measure this at several positions:

```text
after branch token
middle of filler
shared local context A/B/C/D
prediction site before suffix
```

The key metric is whether branch information survives until the prediction site.

Also compute representation separation:

**$\Delta_h=\mathbb{E}_{B\ne B'}\|\mu_B-\mu_{B'}\|^2$**.

Here, $\mu_B$ is the mean hidden state at the prediction site for branch $B$. Larger $\Delta_h$ means branches are more separated in representation space.

### 10.6 Conditional Profiling by Refinement Difficulty

Bucket structured positions by $G_t$: low, medium, and high refinement gain.

For each bucket, report:

```text
L1
L2
head2 accuracy
gradient cosine between L1 and L2
gradient norm ratio
branch probe accuracy
```

This is important because the second-token gradient may be useful on low-$G_t$ positions and harmful on high-$G_t$ positions early in training. The experiment should reveal that structure instead of averaging it away.

## 11. Expected Outcomes and Interpretation

### Outcome 1: Two-token prediction improves branch representation

Expected pattern:

```text
shared-trunk two-token > NTP baseline on head2 branch accuracy
shared-trunk two-token > NTP baseline on branch probe accuracy
c_s is positive or mildly negative, not destructive
G_t decreases over training on structured positions
```

Interpretation: second-token supervision provides useful long-horizon pressure that the shared trunk can absorb.

### Outcome 2: Two-token prediction has useful signal but causes shared interference

Expected pattern:

```text
L2 improves branch probe accuracy
but L1 worsens or learns slower
c_s is negative on shared MLP or attention
rho < 1 or rho < 0 during early training
```

Interpretation: future-token supervision is useful but conflicts with next-token optimization in shared parameters. This supports expert separation or loss scheduling.

### Outcome 3: Separate experts reduce interference

Expected pattern:

```text
separate-expert model preserves L1 better than shared-trunk two-token
separate-expert model keeps or improves head2 branch accuracy
conflict disappears in expert parameters
remaining conflict is mostly in shared attention or embeddings
```

Interpretation: the expert design works because it separates horizon-specific gradient subspaces, while still allowing shared attention to carry common context information.

### Outcome 4: Separate experts do not help

Expected pattern:

```text
separate-expert model still shows L1 degradation
shared attention gradient conflict remains strong
branch probe does not improve
```

Interpretation: the bottleneck is not the expert/MLP subspace. The interference lives in attention, embeddings, or the data does not contain useful second-token branch information.

### Outcome 5: Noisy second-token control is correctly identified

Expected pattern in Regime C:

```text
I(B;Y2 | Y1) approximately zero
head2 branch accuracy near chance
branch probe does not improve from L2
c_s unstable or near zero
r may be large while useful progress is small
```

Interpretation: the diagnostics can distinguish useful future supervision from noisy auxiliary targets.

## 12. Falsification Criteria

The main conjecture is weakened if the following hold across seeds:

```text
Y2 contains branch information, but L2 does not improve branch probe accuracy.
Two-token prediction improves neither head2 branch accuracy nor suffix prediction.
Gradient conflict metrics do not correlate with L1 degradation.
Separate experts do not reduce any measured conflict or improve any branch metric.
Duplicate-target refinement metrics do not distinguish useful and noisy regimes.
```

The expert-separation conjecture is specifically weakened if:

```text
shared-trunk and separate-expert models have the same L1 degradation
shared attention conflict dominates all conditions
expert separation does not improve branch retention or head2 prediction
```

The future-token-usefulness conjecture is specifically weakened if:

```text
Regime A and Regime C behave similarly
head2 performs no better when Y2 is branch-specific than when Y2 is random
branch probe accuracy is unchanged by two-token loss
```

## 13. Implementation Notes for Codex

The implementation should prioritize diagnostic clarity over scale.

Required components:

```text
synthetic dataset generator with regimes A/B/C
one-layer causal Transformer
NTP baseline
shared-trunk two-token model
shared-attention separate-expert model
loss logging by horizon and by structured positions
gradient profiling for L1 and L2 separately
branch probe evaluation
refinement metrics D_t and G_t
multi-seed experiment runner
CSV/JSON logging for all metrics
simple plotting script
```

Important implementation detail: gradient profiling should not change training. At a profiling step, compute $L_1$ and $L_2$ on the same batch, run separate backward passes or use autograd gradients to collect $g_1$ and $g_2$, compute metrics, then clear gradients and run the normal training backward pass.

For the first implementation, use $n=2$ only. Do not add curriculum, MoE routing complexity, or long horizons yet. The purpose is to establish the basic theory-to-measurement bridge.

## 14. Summary

Two-token prediction creates an overlapping supervision structure: the same token $x_{t+2}$ is predicted as a second-token target from $x_{\le t}$ and as a next-token target from $x_{\le t+1}$. This means the second-token head is trained to make an earlier marginal forecast, while the next-token head one step later makes a refined conditional forecast.

The future-token loss helps long-horizon learning only under specific conditions. The future target must contain additional information about a latent branch variable. Its gradient must increase branch recoverability from the shared hidden state. And its projected gradient on shared trunk parameters must not destructively oppose the next-token gradient.

The minimal one-layer Transformer experiment is designed to test exactly these conditions. It should reveal whether second-token prediction is useful, redundant, noisy, or interfering, and whether separate experts reduce the harmful part of the interaction.
