# A Minimal K=2 Story for Long-Horizon Multi-Token Prediction

Date: 2026-07-07

Status: self-contained meeting article for theory discussion.

Source of truth: this article summarizes the current A11 K=2 theory and experiments. It does not replace the project anchors, protocols, summaries, or detailed records.

## Abstract

The current evidence supports a narrow but useful claim: in a controlled K=2 branch-delayed task, two-token prediction can force a prefix hidden state to expose long-horizon branch information that next-token prediction at the same prefix does not need to expose. The clean proof shows an objective-level representation requirement: if the first future token is shared across branches and the second future token is branch-specific, then a branch-blind prefix representation can solve next-token prediction but cannot solve the second-token prediction loss. The experiments support this mechanism in a minimal Transformer and show that the second-token target is useful when it contains branch information, redundant when it is already explained by the first token, and useless as prediction target when it is branch-independent noise. However, the evidence does not yet prove that multi-token prediction is generally more efficient than next-token prediction for learning long-horizon relations. The next decision is to turn "better" into a measurable efficiency claim, first in K=2 learning curves and then in a minimal K=3 first-informative-horizon setting.

## 1. Background

The motivating question is whether multi-token prediction helps a language model learn long-horizon relations better than ordinary next-token prediction.

A long-horizon relation means that an early variable affects a later continuation after many intervening tokens. For example, an early story premise, program variable, theorem assumption, or user instruction may determine a later token even when the local context near the prediction site is ambiguous.

Ordinary next-token prediction is not incapable of learning such relations. If the immediate next token depends on the early variable, then the next-token loss contains long-horizon signal. The problem is more specific: many next-token losses are locally predictable, and a prefix state may not be forced to expose an early variable when the immediate next token is shared or locally determined.

The K=2 question isolates the smallest version of this issue:

Can the same prefix hidden state $h_T$ be forced to expose an early branch variable $B$ when the first future token $Y_1$ is shared but the second future token $Y_2$ depends on $B$?

## 2. Terminology / Definitions

| Term | Plain meaning | Concrete object or computation | Why it matters | What it cannot prove |
| --- | --- | --- | --- | --- |
| Next-token prediction, NTP | Predict only the immediate next token | $h_T \to Y_1$ | Baseline objective | That NTP can never learn long-horizon information |
| Multi-token prediction, MTP | Predict more than one future token from the same prefix state | Here $h_T \to Y_1,Y_2$ | Main objective under study | Universal improvement over NTP |
| Prefix hidden state | Representation after reading the prefix | $h_T=f_\theta(X_{\le T})$ | The state tested for long-horizon information | What later states can recompute |
| Branch variable | Early variable that determines the later suffix | $B\in\{1,\ldots,m\}$ | Clean long-horizon cause | Natural language semantics by itself |
| Branch-blind representation | A representation that does not distinguish branches | $h_T^{(1)}=\cdots=h_T^{(m)}$ in the clean deterministic case | Object of the lower-bound proof | That the whole model lacks branch information |
| Cross-entropy, CE | Prediction loss for the true token | $\operatorname{CE}(q,y)=-\log q(y)$ | Connects prediction success to information requirements | Optimization speed by itself |
| Single-prefix prediction | Predict future tokens directly from the same $h_T$ | $h_T\to Y_j$ without revealing intermediate tokens | Separates MTP from autoregressive rollout | Standard teacher-forced rollout quality |
| Head-2 accuracy | Accuracy of the second-future-token prediction head | Top-1 accuracy of $q_2(\cdot\mid h_T)$ on $Y_2$ | Tests whether the native MTP target is learned | Branch causality without branch-swap guard |
| Branch probe | Linear classifier from hidden state to branch label | Frozen linear probe $h\to B$ | Checks whether branch information is readable | That the native prediction head uses the information |
| Branch-swap preference | Swap only the early branch token and test whether the prediction follows the swap | Success rate or preference for the swapped branch suffix | Causal guard against static memorization | All possible shortcut exclusion |
| Gradient cosine $c_s$ | Directional alignment of $L_1$ and $L_2$ on shared parameters | $c_s=\langle g_1,g_2\rangle/(\|g_1\|\|g_2\|)$ | Detects local shared-gradient conflict | That $L_2$ is wrong or harmful by itself |
| Decision-only objective | Loss is applied only at the final prefix state | Train only at the selected prediction site $T$ | Matches the clean theoretical object | Standard language-model training |
| All-position control | Apply language-model losses at all valid positions | Average offset-1 and offset-2 losses across the sequence | Tests whether the clean result survives LM-style background loss | K>2 or natural language transfer |

## 3. Physical Priors

**Prior 1: Shared-next-token prior.** If the immediate next token $Y_1$ is the same for every branch, then next-token prediction at $T$ can be solved without exposing branch identity in $h_T$.

**Prior 2: Branch-delayed target prior.** If the second future token $Y_2$ is a one-to-one function of the early branch $B$, then a branch-blind $h_T$ cannot predict $Y_2$ with low cross-entropy.

**Prior 3: Data-information prior.** A future-token loss should help long-horizon representation only when that target contains branch information not already provided by earlier future tokens:

$$
I(B;Y_2\mid Y_1)>0.
$$

**Prior 4: Optimization-interaction prior.** A useful second-token loss may still create shared-gradient conflict with next-token loss. Therefore gradient conflict and long-horizon usefulness must be measured separately.

## 4. Mathematical Model

Let the early branch be

$$
B\sim\operatorname{Unif}\{1,\ldots,m\}.
$$

The sequence is

$$
X=(\operatorname{BR}_B,F_1,\ldots,F_L,U,A,S_B).
$$

Here $\operatorname{BR}_B$ reveals the branch, $F_1,\ldots,F_L$ are filler tokens, $U$ is shared local context, $A$ is a shared first future token, and $S_B$ is a branch-specific second future token. The map $B\mapsto S_B$ is one-to-one.

The decision prefix ends immediately after $U$:

$$
h_T^{(B)}=f_{\theta,T}(\operatorname{BR}_B,F_1,\ldots,F_L,U).
$$

The targets are

$$
Y_1=A,\qquad Y_2=S_B.
$$

The information structure is

$$
I(B;Y_1)=0,\qquad I(B;Y_2\mid Y_1)=H(B)=\log m.
$$

The next-token loss at this prefix is

$$
L_1(h_T)=\operatorname{CE}(q_1(\cdot\mid h_T),A).
$$

The two-token loss is

$$
L_2(h_T)=\operatorname{CE}(q_1(\cdot\mid h_T),A)+\lambda\operatorname{CE}(q_2(\cdot\mid h_T),S_B),
$$

where $\lambda>0$.

For shared-trunk optimization, write

$$
g_1=\nabla_{\theta_s}L_1,\qquad g_2=\nabla_{\theta_s}\operatorname{CE}(q_2(\cdot\mid h_T),S_B),
$$

where $\theta_s$ denotes shared trunk parameters. The combined two-token update uses $g_1+\lambda g_2$.

## 5. Mechanism Explanation

The clean mechanism is simple.

Next-token prediction at $T$ only asks $h_T$ to predict $A$. Since $A$ is shared across branches, a branch-blind state can solve this loss.

Two-token prediction at the same $T$ also asks $h_T$ to predict $S_B$. Since $S_B$ identifies $B$, this second loss creates a direct training signal from a branch-specific future token back to the same prefix state $h_T$.

This does not mean that next-token prediction can never learn $B$. A causal Transformer may expose $B$ in other states, later states may attend back to earlier tokens, and NTP can learn long-horizon dependencies when the immediate next target requires them. The precise claim is narrower: at the selected prefix state, if $Y_1$ is branch-blind and $Y_2$ is branch-specific, then the second-token loss adds a representation requirement that the next-token loss at that state does not impose.

The shared-trunk design adds a second question. Even if $L_2$ carries useful branch information, its gradient can conflict with $L_1$ on shared parameters. Therefore the current story has two layers:

1. Information layer: Does $Y_2$ contain branch information beyond $Y_1$?
2. Optimization layer: Can a shared Transformer trunk use $L_2$ without damaging $L_1$ learning?

## 6. Theoretical Results

### Proposition 1: Branch-blind states cannot solve the second-token target

Assume $h_T$ is branch-blind, so it is identical for all branches. Then $q_2(\cdot\mid h_T)$ cannot depend on $B$. Since $S_B$ is uniformly distributed over $m$ distinct branch-specific tokens, the best possible prediction distribution assigns probability $1/m$ to each possible $S_B$. Therefore

$$
\inf_{q_2}\mathbb E[-\log q_2(S_B\mid h_T)]=\log m.
$$

Thus a branch-blind representation can solve $Y_1=A$ but must pay at least $\lambda\log m$ expected second-token loss under the two-token objective.

### Proposition 2: Low second-token cross-entropy requires branch information

Suppose some predictor from $h_T$ achieves

$$
\mathbb E[-\log q_2(S_B\mid h_T)]\le \varepsilon.
$$

Cross-entropy upper-bounds the conditional entropy, so

$$
H(S_B\mid h_T)\le \varepsilon.
$$

Because $B\mapsto S_B$ is one-to-one, $H(B\mid h_T)=H(S_B\mid h_T)$. Hence

$$
I(h_T;B)=H(B)-H(B\mid h_T)\ge \log m-\varepsilon.
$$

Therefore, in the clean construction, successful single-prefix second-token prediction implies that $h_T$ contains information about the early branch.

### Proposition 3: The useful future-token condition is conditional information

For a future suffix, the branch information satisfies

$$
I(B;Y_{1:k})=I(B;Y_1)+I(B;Y_{2:k}\mid Y_1).
$$

Adding future targets can only increase the branch information required by accurate single-prefix suffix prediction when the conditional term is positive. For K=2, the decisive data-level condition is

$$
I(B;Y_2\mid Y_1)>0.
$$

If this term is zero, the second-token loss may still be learnable, but it does not add a new long-horizon branch signal beyond $Y_1$.

### Proposition 4: Negative gradient cosine is not equivalent to harmful learning

The shared-gradient cosine

$$
c_s=\frac{\langle g_1,g_2\rangle}{\|g_1\|\|g_2\|}
$$

measures whether the second-token gradient aligns with the next-token gradient on shared parameters. If $c_s<0$, then $L_2$ locally weakens the pure $L_1$ update direction.

However, this does not prove that $L_2$ is useless or harmful. A second-token gradient can be negative relative to $L_1$ and still point in a direction that increases branch recoverability. The more relevant long-horizon diagnostic is whether descending $L_2$ reduces a branch-recovery loss $R_\phi$:

$$
\langle \nabla_{\theta_s}R_\phi,g_2\rangle>0.
$$

This distinction explains why the experiments track both prediction/probe metrics and shared-gradient metrics.

## 7. Experimental Evidence

### 7.1 A11_01: Clean K=2 objective-level separation

The first experiment used the deterministic sequence

```text
BR_b F00 F01 F02 F03 F04 F05 F06 F07 U00 U01 A_SHARED S_b STOP
```

The evaluation prefix stops before `A_SHARED`. Therefore $Y_1=A$ is shared and $Y_2=S_B$ is branch-specific.

The model was a one-layer causal Transformer with two direct heads from $h_T$. Branch-token embeddings were initialized identically to remove random branch identity leakage. Seeds were `971, 972, 973`.

| Condition | Offset-1 accuracy | Offset-2 single-prefix accuracy | Frozen branch probe | Branch-swap consistency | Interpretation |
| --- | ---: | ---: | ---: | ---: | --- |
| Fixed-next-one | 1.000 | 0.000 | 0.333 | 0.000 | Solves shared $A$ but remains branch-blind |
| Next-two | 1.000 | 1.000 | 1.000 | 1.000 | Predicts $S_B$ and exposes branch in $h_T$ |

This supports the clean mechanism: the second-token loss is sufficient to make $h_T$ branch-separable in the controlled K=2 task, while next-token loss at the same prefix is not.

### 7.2 A11_02: Shared-trunk signal and interference

The second experiment asked whether $L_2$ is useful, redundant, noisy, or interfering in a shared-trunk Transformer.

Three data regimes were used:

| Regime | Construction | Intended role |
| --- | --- | --- |
| `A_clean` | $Y_1=U,\;Y_2=S_B$ | $Y_2$ contains branch information beyond $Y_1$ |
| `B_redundant` | $Y_1=S_B,\;Y_2=R(S_B)=T_B$ | $Y_2$ is predictable once $Y_1$ is known |
| `C_noisy` | $Y_1=U,\;Y_2=Z,\;Z\perp B$ | $Y_2$ is branch-independent noise |

Model conditions included an NTP baseline, a shared-trunk two-token model, and a shared-attention separate-expert diagnostic. The fixed configuration used `num_branches=4`, `filler_length=16`, `shared_context_length=4`, one-layer one-head Transformer, `d_model=64`, $\lambda=1.0$, 4000 training steps, and seeds `971` to `975`.

#### Decision-only result

The decision-only objective applied losses only at the final prediction site. It matched the clean theory object $h_T\to(Y_1,Y_2)$.

Key result: `A_clean` showed useful branch signal, but shared-trunk acquisition was unstable.

| Regime / condition | Init | $Y_1$ acc | Head-2 acc | Branch probe | Swap | Interpretation |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `A_clean`, NTP | identical | 1.00 | NA | 0.25 | NA | Branch-blind baseline |
| `A_clean`, shared trunk | identical | 1.00 | 0.65 | 0.65 | 0.65 | Useful but unstable acquisition |
| `A_clean`, shared trunk | random | 1.00 | 0.90 | 0.90 | 0.90 | Stronger but still not perfect |
| `A_clean`, separate expert | identical | 1.00 | 1.00 | 1.00 | 1.00 | Expert separation fixes this constrained case |
| `C_noisy`, shared trunk | both | 1.00 | 0.071 | 0.40 | NA | Head-2 stays near chance |

The noisy-control head-2 chance level is about $1/16=0.0625$. Therefore `C_noisy` does not support the idea that any auxiliary future loss creates useful head-2 learning.

The 12000-step completion diagnostic did not fully remove the shared-trunk failures. Some `A_clean` seeds remained at head-2/probe/swap values of `0.25` or `0.50`, so the instability was not merely a 4000-step budget artifact.

#### All-position language-model control

The all-position control applied offset-1 and offset-2 losses across all valid token positions. This tests whether the clean result survives a more language-model-like objective.

| Regime / condition | Init | $Y_1$ acc | Head-2 acc | Branch probe | Swap | Interpretation |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `A_clean`, shared trunk | random | 1.00 | 1.00 | 1.00 | 1.00 | Branch-specific $L_2$ is learned |
| `A_clean`, shared trunk | identical | 1.00 | 1.00 | 1.00 | 1.00 | Result survives symmetry-controlled init |
| `B_redundant`, shared trunk | both | 1.00 | 1.00 | 1.00 | 1.00 | Learnable but not new long-horizon evidence |
| `C_noisy`, shared trunk | identical | 1.00 | 0.066 | 0.750 | NA | Head-2 stays noise-level; probe alone is misleading |
| `C_noisy`, shared trunk | random | 1.00 | 0.066 | 1.000 | NA | Probe can be high even when $Y_2$ is useless |

The decisive contrast is not branch probe alone. The decisive contrast is:

1. In `A_clean`, head-2 accuracy, branch probe, and branch-swap preference all reach `1.00`.
2. In `C_noisy`, head-2 accuracy stays near chance even when branch probe is high.

Thus branch probe must be guarded by native head-2 prediction and branch-swap behavior.

#### Gradient diagnostics

All-position shared-trunk gradients show strong negative cosine in embedding and shared attention for `A_clean` and `B_redundant`:

| Regime | Condition | Init | Embedding $c_s$ | Attention $c_s$ | MLP $c_s$ | Interpretation |
| --- | --- | --- | ---: | ---: | ---: | --- |
| `A_clean` | shared trunk | random | -0.943 | -0.943 | 0.091 | Strong embedding/attention conflict |
| `A_clean` | shared trunk | identical | -0.938 | -0.946 | -0.125 | Strong embedding/attention conflict |
| `B_redundant` | shared trunk | random | -0.945 | -0.949 | 0.239 | Conflict also appears for redundant target |
| `C_noisy` | shared trunk | random | 0.002 | -0.064 | -0.028 | No comparable strong conflict |

However, $Y_1$ accuracy remains `1.00` in the all-position runs. Therefore the supported conclusion is not "negative cosine proves harm." The supported conclusion is "local shared-gradient conflict exists, but no observed $L_1$ performance damage was established in this setting."

## 8. Current Understanding

The current self-contained story is:

1. The clean K=2 theory proves a representation requirement. If $Y_1$ is shared and $Y_2$ identifies the branch, then a branch-blind $h_T$ can solve NTP but cannot solve the second-token loss.
2. The clean K=2 experiment supports this mechanism. Fixed-next-one solves $Y_1$ but stays branch-blind; next-two solves both targets and makes $h_T$ branch-readable and branch-swap-sensitive.
3. The shared-trunk experiment shows that the second-token signal is conditional. It is useful in `A_clean`, redundant in `B_redundant`, and useless as a prediction target in `C_noisy`.
4. Shared-gradient conflict is real but not decisive by itself. Negative $L_1/L_2$ cosine on embedding and attention does not imply that $L_2$ is a wrong update, because $L_2$ can still create branch-relevant representation pressure.

## 9. Claim Boundary

The current evidence can support the following claims:

- In the controlled K=2 branch-delayed construction, two-token prediction supplies branch-relevant supervision on $h_T$ that next-token prediction at the same state does not supply.
- This supervision is meaningful only when the second future token contains branch information beyond the first future token.
- In the minimal shared-trunk Transformer, the useful-signal conclusion survives both decision-only and all-position objectives.
- Branch probe alone is not sufficient evidence; head-2 accuracy and branch-swap behavior are required guards.
- Negative shared-gradient cosine is a conflict diagnostic, not a proof of harmful learning.

The current evidence cannot support the following claims:

- MTP universally outperforms NTP.
- NTP cannot learn long-horizon relations.
- The K=2 mechanism automatically extends to K>2.
- MTP is already proven more sample-efficient or step-efficient than NTP.
- The synthetic result transfers to natural language or large-scale pretraining.
- Separate experts are generally a better architecture.

## 10. What Remains Unproven

The original high-level question is about whether MTP is better at learning long-horizon relations. The K=2 result proves that MTP can impose a stronger representation requirement, but it does not yet prove learning efficiency.

To make "better" precise, the next stage must define an efficiency metric. Possible metrics are:

| Metric | Meaning | What it would support |
| --- | --- | --- |
| Time to branch recovery | First training step where branch probe or branch-swap exceeds a threshold such as 0.9 | Faster acquisition of long-horizon information |
| Area under branch metric curve | Average branch metric over training | More stable early representation learning |
| Single-prefix informative-horizon loss | Loss of the first future target that actually depends on $B$ | Better direct prediction of long-horizon target |
| Branch-gradient projection | Projection of each horizon gradient onto a branch-recovery direction | Whether the future-token gradient is useful even when its cosine with $L_1$ is negative |
| Local-loss guard | $Y_1$ accuracy or loss | Whether long-horizon gain sacrifices local next-token learning |

Without one of these efficiency metrics, the strongest honest statement remains representation pressure, not learning-speed superiority.

## 11. Next Decisions

### Next decision 1: K=2 efficiency curves

Question:

Does K=2 MTP acquire branch information in $h_T$ faster or more robustly than an NTP baseline under matched model, data, optimizer, and training budget?

Minimal protocol idea:

- Keep the `A_clean` construction.
- Track branch probe, branch-swap preference, and head-2 / evaluation-head performance over training steps.
- Compare time-to-threshold and area under curve.
- Guard local learning with $Y_1$ loss and accuracy.

Pass condition:

MTP reaches branch-recovery and branch-swap thresholds earlier than NTP or achieves higher branch-metric area without degrading $Y_1$ learning.

Fail condition:

MTP reaches the same final representation only at the same speed, or slower, or only by degrading $Y_1$ learning.

### Next decision 2: K=3 first-informative-horizon test

Question:

If the first branch-informative future token appears at horizon 3 rather than horizon 2, does adding that horizon create the same branch-representation pressure?

Minimal construction:

$$
Y_1=A,\qquad Y_2=C,\qquad Y_3=S_B.
$$

Here $Y_1$ and $Y_2$ are shared or redundant, while $Y_3$ identifies $B$.

Comparison:

- K=1 NTP: predicts only $Y_1$.
- K=2 MTP: predicts $Y_1,Y_2$ but still has no branch-informative target.
- K=3 MTP: predicts $Y_1,Y_2,Y_3$ and receives the first branch-informative horizon.

Expected falsifiable pattern:

K=3 should improve branch recovery, branch-swap preference, and informative-horizon accuracy beyond K=1 and K=2. If K=2 performs the same as K=3 despite no branch-informative target, then the proposed first-informative-horizon mechanism is weakened or the data construction leaks branch information.

## 12. Summary

The current K=2 work establishes a clean mechanism, not a universal method claim. The mechanism is that a future-token loss can attach branch-specific supervision directly to an earlier prefix state when the immediate next token is ambiguous. The proof shows why low second-token loss requires branch information in $h_T$. The experiments show that this mechanism appears in a minimal trainable Transformer and remains valid under all-position language-model-style training.

The next scientific step is not a broad K sweep. It is to define and test efficiency: whether MTP learns the long-horizon variable faster, more robustly, or with better branch-gradient signal than NTP. After that, the smallest K-scaling step is K=3 with a first-informative horizon at $Y_3$.

## Source Map

- K=2 self-contained proof: `daily_research_reports/0707/mtp_k2/mtp_k2_self_contained_theory_proof.md`
- Long-horizon next-k theory design: `daily_research_reports/0707/mtp_k2/long_horizon_next_k_theory_design.md`
- Two-token shared-trunk design: `daily_research_reports/0707/mtp_k2/two_token_shared_trunk_theory_experiment_design.md`
- A11_01 anchor: `Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_01_k2_branch_delayed_next_two_anchor.md`
- A11_01 summary: `Projects/from-attention-to-search/main/experiments/A11/A11_01_k2_branch_delayed_next_two/summary.md`
- A11_02 anchor: `Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_02_two_token_shared_trunk_signal_interference_anchor.md`
- A11_02 summary: `Projects/from-attention-to-search/main/experiments/A11/A11_02_two_token_shared_trunk_signal_interference/summary.md`
- A11_02 detailed record: `Projects/from-attention-to-search/main/experiments/A11/A11_02_two_token_shared_trunk_signal_interference/detailed.md`
