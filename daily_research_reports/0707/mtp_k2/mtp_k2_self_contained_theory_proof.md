# A Self-Contained Theory Proof for the Minimal K=2 Long-Horizon MTP Task

**Date:** 2026-07-06  
**Scope:** Minimal theory document for a controlled K=2 comparison between next-one prediction and next-two prediction.  
**Main purpose:** Give a precise proof that next-two prediction can impose a direct requirement on a prefix hidden state to preserve early branch information, while next-one prediction need not impose that requirement in the same controlled setting.

---

## 1. Executive Summary

This document proves a minimal objective-level separation between next-one prediction and next-two prediction.

We study a sequence in which an early branch variable determines a later token, but the first future token after the decision point is shared by all branches. The sequence has the form

\[
X = (B, F_1, \ldots, F_L, U, A, S_B).
\]

Here:

- \(B\) is an early branch key.
- \(F_1, \ldots, F_L\) are intervening filler tokens.
- \(U\) is a shared local context.
- \(A\) is the first future token after the decision point, and it is the same for all branches.
- \(S_B\) is the second future token after the decision point, and it is determined by the early branch key \(B\).

Let \(h_T\) be the hidden state after the model has read \((B, F_1, \ldots, F_L, U)\). The first future token is

\[
Y_1 = A,
\]

and the second future token is

\[
Y_2 = S_B.
\]

The central result is:

> In this controlled K=2 distribution, next-one prediction only requires \(h_T\) to predict the shared token \(A\). It therefore does not force \(h_T\) to preserve the branch key \(B\). In contrast, next-two prediction also requires \(h_T\) to predict \(S_B\), which directly forces \(h_T\) to contain information about \(B\) if the loss is to be small.

This is not a proof that multi-token prediction is always better than next-token prediction. It is a proof of a narrower and cleaner statement: there exists a simple long-horizon setting in which the second future token contains branch information that the first future token does not contain, and next-two prediction directly supervises that information at the earlier hidden state.

---

## 2. The Research Question

The motivating question is about long-horizon language dependencies.

A long-horizon dependency occurs when information appears early in a sequence and is only needed much later. A simple example is a story in which the first chapter determines what must happen in the final chapter, while the middle chapters do not locally determine the ending by themselves.

The theoretical question is:

> Can next-two prediction create a stronger and more direct connection between an early variable and a later token than next-one prediction?

The phrase "stronger and more direct" means the following precise object in this document:

- Next-one prediction trains the hidden state \(h_T\) only to predict \(Y_1\).
- Next-two prediction trains the same hidden state \(h_T\) to predict both \(Y_1\) and \(Y_2\).
- If \(Y_1\) does not depend on the early branch key \(B\), but \(Y_2\) does, then next-two prediction adds a direct loss term from the branch-dependent future token to the same hidden state \(h_T\).

This is the minimal K=2 form of the broader multi-token prediction hypothesis.

---

## 3. Basic Definitions

This section defines every term used later in the proof.

### 3.1 Token sequence

A token sequence is a finite ordered list

\[
X_1, X_2, \ldots, X_n.
\]

Each \(X_t\) takes values in a vocabulary \(\mathcal V\).

### 3.2 Causal model

A causal sequence model computes a hidden state at each position using only the current and previous tokens. At position \(t\), the hidden state is

\[
h_t = f_{\theta,t}(X_{\le t}),
\]

where

\[
X_{\le t} = (X_1, \ldots, X_t).
\]

The subscript \(\theta\) denotes model parameters. The subscript \(t\) allows the function to depend on position. This covers ordinary causal Transformer behavior, where the hidden state at each position can attend to previous tokens.

This document does not assume a strict recurrent bottleneck of the form

\[
h_{t+1}=G_\theta(h_t, X_{t+1}).
\]

That distinction matters because a strict bottleneck would make \(h_t\) the only information channel into \(h_{t+1}\). In a causal Transformer-like model, the later state can recompute or attend to earlier tokens even if a particular earlier state did not expose a certain variable.

### 3.3 Prefix hidden state

The prefix hidden state is the hidden state after the model has read the prefix of interest. In this document, the key prefix ends immediately before the two future tokens \(Y_1\) and \(Y_2\). We denote that hidden state by \(h_T\).

### 3.4 Next-one prediction

Next-one prediction trains \(h_T\) to predict only the next token

\[
Y_1 = X_{T+1}.
\]

The loss at this position is

\[
L_1(h_T) = \operatorname{CE}(q_1(\cdot \mid h_T), Y_1),
\]

where \(q_1(\cdot \mid h_T)\) is the prediction distribution for the first future token.

### 3.5 Next-two prediction

Next-two prediction trains the same hidden state \(h_T\) to predict two future tokens:

\[
Y_1 = X_{T+1}, \qquad Y_2 = X_{T+2}.
\]

The loss at this position is

\[
L_2(h_T) = \operatorname{CE}(q_1(\cdot \mid h_T), Y_1) + \lambda\operatorname{CE}(q_2(\cdot \mid h_T), Y_2),
\]

where \(\lambda>0\) is the weight on the second-token loss, and \(q_2(\cdot \mid h_T)\) is the prediction distribution for the second future token.

### 3.6 Cross-entropy loss

For a true token \(y\) and a predicted distribution \(q(\cdot)\), the cross-entropy loss is

\[
\operatorname{CE}(q,y) = -\log q(y).
\]

All logarithms in this document use the natural base.

For a random target \(Y\), the expected cross-entropy is

\[
\mathbb E[-\log q(Y)].
\]

### 3.7 Autoregressive rollout

Autoregressive rollout means predicting one token, appending it to the context, recomputing the next hidden state, and then predicting the next token. For example,

\[
h_T \to Y_1,
\]

then after \(Y_1\) is available,

\[
h_{T+1} \to Y_2.
\]

This is different from asking the original state \(h_T\) to predict \(Y_2\) directly.

### 3.8 Single-prefix future prediction

Single-prefix future prediction asks whether the same earlier hidden state \(h_T\) can directly predict future tokens beyond the next one:

\[
h_T \to Y_1, \qquad h_T \to Y_2.
\]

This is the relevant test for multi-token prediction.

### 3.9 Branch-blind representation

Let \(B\) be the branch variable. A prefix representation is branch-blind if it does not distinguish the branch. In the clean deterministic form, this means

\[
h_T^{(1)} = h_T^{(2)} = \cdots = h_T^{(m)},
\]

where \(h_T^{(b)}\) is the prefix hidden state when the branch is \(B=b\).

A branch-blind representation cannot expose branch-specific information to any predictor that only receives \(h_T\).

---

## 4. The Minimal K=2 Distribution

We now define the controlled data distribution.

Let

\[
B \sim \operatorname{Unif}\{1,2,\ldots,m\}.
\]

The variable \(B\) is the early branch key. Each branch \(b\) has a corresponding branch-specific token \(S_b\). We assume the branch-specific tokens are distinct:

\[
S_b \neq S_{b'} \quad \text{whenever } b\neq b'.
\]

A sequence is generated as

\[
X = (\operatorname{BR}_B, F_1, \ldots, F_L, U, A, S_B).
\]

Here:

- \(\operatorname{BR}_B\) is the token that reveals the branch key.
- \(F_1, \ldots, F_L\) are filler tokens.
- \(U\) is a shared local context.
- \(A\) is a shared first future token.
- \(S_B\) is the branch-specific second future token.

Let \(T\) be the position immediately after \(U\). The prefix hidden state is

\[
h_T^{(B)} = f_{\theta,T}(\operatorname{BR}_B, F_1, \ldots, F_L, U).
\]

The two future targets are

\[
Y_1 = A,
\]

and

\[
Y_2 = S_B.
\]

The key information conditions are

\[
I(B;Y_1)=0,
\]

and

\[
I(B;Y_2\mid Y_1)=I(B;S_B)>0.
\]

Because the map \(B\mapsto S_B\) is one-to-one and \(B\) is uniform, we have

\[
H(S_B)=\log m.
\]

Thus the first future token contains no branch information, while the second future token fully identifies the branch.

---

## 5. Why the First Future Token Is Shared

The choice

\[
Y_1=A, \qquad Y_2=S_B
\]

is deliberate. It is not meant to claim that real language always has this form.

The reason is proof isolation. If the first future token already depended on the branch, then next-one prediction would already receive a branch-dependent target:

\[
h_T \to Y_1.
\]

In that case, next-one prediction would already have direct pressure to preserve branch information. The difference between next-one and next-two would be less clean.

The shared first token creates the cleanest possible separation:

\[
\text{next-one target: no branch information},
\]

but

\[
\text{next-two extra target: branch information}.
\]

Therefore, the K=2 construction tests exactly what the second-token loss adds beyond next-one prediction.

A natural language analogy is:

```text
BR_1 ... The answer is A
BR_2 ... The answer is B
BR_3 ... The answer is C
```

At the prefix ending in "The answer is", the next token may be a shared bridge token or format token, while the following token contains the branch-dependent choice. The model must remember the early branch key to predict that later choice from the same prefix state.

---

## 6. Training Objectives in the K=2 Distribution

At the decision position \(T\), the next-one loss is

\[
L_1(h_T) = \operatorname{CE}(q_1(\cdot\mid h_T), A).
\]

This loss asks only whether \(h_T\) predicts the shared token \(A\).

The next-two loss is

\[
L_2(h_T) = \operatorname{CE}(q_1(\cdot\mid h_T), A)
+ \lambda\operatorname{CE}(q_2(\cdot\mid h_T), S_B).
\]

This loss asks whether \(h_T\) predicts both the shared token \(A\) and the branch-specific token \(S_B\).

The second term is the essential difference:

\[
\lambda\operatorname{CE}(q_2(\cdot\mid h_T), S_B).
\]

It attaches the branch-specific future token directly to the earlier prefix state \(h_T\).

---

## 7. Lemma 1: A Branch-Blind State Cannot Predict the Branch-Specific Second Token

### Statement

Assume \(B\sim\operatorname{Unif}\{1,\ldots,m\}\), and the branch-specific tokens \(S_1,\ldots,S_m\) are distinct. If the prefix state is branch-blind, meaning

\[
h_T^{(1)}=\cdots=h_T^{(m)}=c,
\]

then any predictor \(q_2(\cdot\mid h_T)\) that only sees \(h_T\) has expected second-token cross-entropy at least

\[
\log m.
\]

That is,

\[
\inf_{q_2}\mathbb E[-\log q_2(S_B\mid h_T)] = \log m.
\]

Also, any deterministic top-1 predictor has expected accuracy at most

\[
\frac{1}{m}.
\]

### Proof

If \(h_T^{(1)}=\cdots=h_T^{(m)}=c\), then the predictor receives the same input \(c\) for every branch. Therefore it must use one common distribution

\[
q_2(\cdot\mid c)
\]

for all branches.

The target token \(S_B\) is uniformly distributed over the distinct set

\[
\{S_1,\ldots,S_m\}.
\]

The expected cross-entropy is

\[
\frac{1}{m}\sum_{b=1}^{m}-\log q_2(S_b\mid c).
\]

This quantity is minimized when

\[
q_2(S_b\mid c)=\frac{1}{m}
\]

for each \(b\). The minimum value is therefore

\[
-\frac{1}{m}\sum_{b=1}^{m}\log\frac{1}{m} = \log m.
\]

For top-1 accuracy, a deterministic predictor using the same input \(c\) must choose the same token for every branch. Since only one of the \(m\) branch targets can be correct for that chosen token, the average accuracy is at most \(1/m\).

This proves the lemma.

---

## 8. Lemma 2: Next-One Loss at the Decision Point Does Not Require Branch Information

### Statement

In the K=2 distribution, the next-one target at position \(T\) is the shared token \(A\). Therefore a branch-blind representation can achieve zero next-one loss at position \(T\).

### Proof

Set

\[
h_T^{(1)}=\cdots=h_T^{(m)}=c.
\]

Choose a next-one predictor \(q_1\) satisfying

\[
q_1(A\mid c)=1.
\]

Then for every branch \(b\),

\[
\operatorname{CE}(q_1(\cdot\mid h_T^{(b)}), A)
= -\log q_1(A\mid c)
=0.
\]

Thus the next-one loss at the decision point can be zero even when \(h_T\) contains no information about \(B\).

This proves the lemma.

---

## 9. Proposition 1: Next-One Success Does Not Imply Single-Prefix Second-Token Decodability

### Statement

In the K=2 distribution, low next-one loss at the decision point does not imply that the second future token \(S_B\) is predictable from the same prefix state \(h_T\).

More strongly, there exists a representation with zero next-one loss at position \(T\), but with optimal second-token prediction loss equal to \(\log m\).

### Proof

By Lemma 2, the branch-blind representation

\[
h_T^{(1)}=\cdots=h_T^{(m)}=c
\]

can achieve zero next-one loss because the next-one target is always \(A\).

By Lemma 1, the same branch-blind representation cannot predict \(S_B\) from \(h_T\) with expected cross-entropy below \(\log m\).

Therefore, zero next-one loss at \(T\) does not imply that \(h_T\) is a useful single-prefix predictor of \(Y_2=S_B\).

This proves the proposition.

---

## 10. Proposition 2: Autoregressive Rollout Success Does Not Imply Single-Prefix Future Prediction

### Statement

There exists a causal sequence model that achieves perfect next-token rollout on the K=2 distribution, while its prefix state \(h_T\) remains branch-blind and cannot predict \(S_B\) better than the \(\log m\) lower bound.

### Proof

We construct a causal model with two relevant states.

At position \(T\), define

\[
h_T^{(B)}=c
\]

for every branch \(B\). This state is branch-blind.

Choose the next-token predictor at position \(T\) so that

\[
p(A\mid h_T=c)=1.
\]

Therefore the model predicts \(Y_1=A\) perfectly.

At the later position \(T+1\), after the model has consumed \(A\), define the later state as

\[
h_{T+1}^{(B)}=r_B,
\]

where \(r_B\) is branch-specific. This is allowed in a causal Transformer-like model because the state at position \(T+1\) is computed from the full prefix

\[
(\operatorname{BR}_B, F_1,\ldots,F_L,U,A),
\]

and can attend back to the early branch token \(\operatorname{BR}_B\).

Choose the next-token predictor at position \(T+1\) so that

\[
p(S_B\mid h_{T+1}^{(B)})=1.
\]

Then the model also predicts \(Y_2=S_B\) perfectly during autoregressive rollout.

However, the earlier state \(h_T\) is branch-blind. By Lemma 1, any predictor that tries to predict \(S_B\) directly from \(h_T\) has expected cross-entropy at least \(\log m\).

Thus autoregressive next-token success does not imply that the earlier state \(h_T\) is a single-prefix predictor of the second future token.

This proves the proposition.

### Architectural boundary

This proposition assumes the later hidden state is not forced to be a deterministic function only of \(h_T\) and \(A\). If the model were a strict recurrent bottleneck

\[
h_{T+1}=G(h_T,A),
\]

then a branch-blind \(h_T\) could not be used to reconstruct \(B\) at \(T+1\). In that case, standard next-token training may also need \(h_T\) to carry branch information. The separation in this document is therefore an objective-level separation for causal models whose later positions can recompute from the full prefix, as causal Transformers can.

---

## 11. Proposition 3: Next-Two Loss Directly Excludes Branch-Blind Prefix States

### Statement

In the K=2 distribution, any branch-blind prefix state has next-two loss at least

\[
\lambda\log m
\]

above the zero first-token loss. Therefore, if next-two loss is small, \(h_T\) cannot be branch-blind.

### Proof

The next-two loss is

\[
L_2(h_T)=\operatorname{CE}(q_1(\cdot\mid h_T),A)
+\lambda\operatorname{CE}(q_2(\cdot\mid h_T),S_B).
\]

The first term can be zero even for a branch-blind state because \(A\) is shared.

The second term is different. If \(h_T\) is branch-blind, Lemma 1 gives

\[
\inf_{q_2}\mathbb E[-\log q_2(S_B\mid h_T)] = \log m.
\]

Therefore any branch-blind representation satisfies

\[
\mathbb E[L_2(h_T)] \ge \lambda\log m.
\]

In contrast, a branch-aware representation can achieve zero loss in the idealized realizable case. For example, let

\[
h_T^{(B)}=e_B,
\]

where \(e_B\) uniquely identifies the branch. Choose \(q_1\) so that

\[
q_1(A\mid e_B)=1
\]

for every branch, and choose \(q_2\) so that

\[
q_2(S_B\mid e_B)=1.
\]

Then both terms in \(L_2\) are zero.

Thus next-two loss distinguishes branch-blind and branch-aware prefix states, while next-one loss at \(T\) does not.

This proves the proposition.

---

## 12. Proposition 4: Low Second-Token Loss Forces Information About the Branch

### Statement

Suppose the second-token predictor from \(h_T\) satisfies

\[
\mathbb E[-\log q_2(S_B\mid h_T)] \le \delta.
\]

Then the prefix state \(h_T\) must contain information about the branch. More precisely,

\[
I(h_T;B) \ge \log m - \delta.
\]

### Proof

Because \(S_B\) is a deterministic one-to-one function of \(B\), it has entropy

\[
H(S_B)=\log m.
\]

For any predictor \(q_2\), the expected cross-entropy upper bounds the conditional entropy:

\[
H(S_B\mid h_T) \le \mathbb E[-\log q_2(S_B\mid h_T)].
\]

By assumption,

\[
H(S_B\mid h_T) \le \delta.
\]

Therefore

\[
I(h_T;S_B)
= H(S_B)-H(S_B\mid h_T)
\ge \log m - \delta.
\]

Since \(S_B\) is a function of \(B\), information that \(h_T\) has about \(S_B\) is information about \(B\). Thus

\[
I(h_T;B) \ge I(h_T;S_B) \ge \log m - \delta.
\]

This proves the proposition.

### Consequence for next-two training

If the second-token part of next-two loss is small, then \(h_T\) must contain almost all branch information. In particular, if

\[
\lambda\mathbb E[-\log q_2(S_B\mid h_T)] \le \epsilon,
\]

then

\[
I(h_T;B) \ge \log m - \frac{\epsilon}{\lambda}.
\]

---

## 13. Proposition 5: Next-Two Provides a Direct Branch-Dependent Gradient to the Prefix State

### Statement

For a direct-head model, next-two prediction sends a branch-dependent gradient from the second future token directly to \(h_T\). Next-one prediction at \(T\) does not include this term.

### Setup

Assume linear prediction heads:

\[
z_1 = W_1h_T+b_1,
\]

\[
z_2 = W_2h_T+b_2.
\]

Let

\[
p_1=\operatorname{softmax}(z_1),
\]

and

\[
p_2=\operatorname{softmax}(z_2).
\]

### Proof

The next-one loss is

\[
L_1 = \operatorname{CE}(p_1,A).
\]

The gradient with respect to \(h_T\) is

\[
\nabla_{h_T}L_1 = W_1^\top(p_1-e_A),
\]

where \(e_A\) is the one-hot vector for token \(A\).

Because \(A\) is the same for all branches, this target does not by itself distinguish \(B\).

The next-two loss is

\[
L_2 = \operatorname{CE}(p_1,A)+\lambda\operatorname{CE}(p_2,S_B).
\]

The gradient with respect to \(h_T\) is

\[
\nabla_{h_T}L_2
= W_1^\top(p_1-e_A)+\lambda W_2^\top(p_2-e_{S_B}).
\]

The second term

\[
\lambda W_2^\top(p_2-e_{S_B})
\]

explicitly depends on the branch-specific token \(S_B\). Therefore it is a direct branch-dependent training signal applied to the same prefix state \(h_T\).

This proves the gradient-path distinction.

### Boundary

This proposition does not prove that optimization always succeeds. It only proves that next-two changes the loss geometry by adding a direct branch-dependent error signal at \(h_T\).

---

## 14. Main Theorem: The Minimal K=2 Objective-Level Separation

### Statement

In the K=2 branch-delayed distribution

\[
X=(\operatorname{BR}_B,F_1,\ldots,F_L,U,A,S_B),
\]

where \(A\) is shared and \(S_B\) is branch-specific, the following hold:

1. Next-one loss at the decision position can be minimized by a branch-blind prefix state.
2. A branch-blind prefix state cannot predict the second future token \(S_B\) with expected cross-entropy below \(\log m\).
3. Next-two loss directly penalizes branch-blind prefix states through its second-token term.
4. If the second-token loss is small, then \(h_T\) must contain information about \(B\).
5. In a direct-head model, next-two adds a branch-dependent gradient term to \(h_T\), while next-one at the same position does not.

### Proof

Part 1 follows from Lemma 2.

Part 2 follows from Lemma 1.

Part 3 follows from Proposition 3.

Part 4 follows from Proposition 4.

Part 5 follows from Proposition 5.

Together these results prove that next-two prediction imposes a direct representation requirement on \(h_T\) that next-one prediction does not impose in the same controlled K=2 distribution.

This completes the proof.

---

## 15. Why This Answers the Adviser-Level Question in a Minimal Form

The adviser-level question asks for a rigorous link between long-horizon dependence and multi-token prediction. The minimal structure of long-horizon dependence is:

\[
\text{early information} \to \text{later target}.
\]

In this document, the early information is \(B\), and the later target is \(S_B\). The long gap is represented by filler tokens and shared local context.

The proof shows that next-one prediction can ignore \(B\) at the decision state when the immediate next token is shared. Next-two prediction cannot ignore \(B\) if it must predict the branch-specific second token from the same state.

Thus the proof captures the smallest possible version of the intended mechanism:

\[
\text{delayed relevance becomes immediate supervision under next-two prediction}.
\]

The proof does not solve the whole natural-language problem. Instead, it gives a clean mathematical anchor: if a future token contains early-branch information not present in the immediate next token, then next-two prediction creates a direct training signal for that information at the prefix state.

---

## 16. Relation to the More General Next-k Design

The broader next-k design considers a future suffix

\[
Y_{1:k}=(X_{T+1},\ldots,X_{T+k})
\]

that may contain multiple branch-dependent tokens.

The K=2 construction in this document is the smallest clean special case:

\[
Y_1=A,
\]

\[
Y_2=S_B.
\]

It satisfies

\[
I(B;Y_1)=0,
\]

but

\[
I(B;Y_{1:2})=I(B;Y_2)=\log m.
\]

This makes the additional information requirement of next-two completely explicit.

For larger \(k\), the analogous condition is

\[
I(B;Y_{2:k}\mid Y_1)>0.
\]

That condition means that future tokens beyond the first contain additional branch information not available in the first future token. Under that condition, next-k prediction imposes a stronger representation requirement than next-one prediction.

The K=2 proof is therefore the correct minimal anchor before moving to longer horizons.

---

## 17. What the Proof Does Not Claim

This proof is intentionally limited. It does not claim any of the following.

### 17.1 It does not claim that next-token prediction always fails

Next-token prediction may learn long-horizon dependencies in many settings. The proof only shows that next-one loss at a particular prefix state does not force that state to expose the second future token when the first future token is shared.

### 17.2 It does not claim that next-two prediction always outperforms next-one prediction

The proof shows a stronger representation requirement, not guaranteed better optimization or better downstream performance.

### 17.3 It does not claim that natural language always has the exact K=2 structure

The K=2 construction is a controlled mathematical test. Real language may distribute branch information over many tokens and many latent variables.

### 17.4 It does not prove curriculum training is better than full-horizon training

The proof concerns the presence of the second-token loss term, not the schedule by which future-token losses are introduced.

### 17.5 It does not rely on more parameters

The key comparison should keep architecture fixed and change only the active loss terms. This is why a fixed next-one baseline with the same extra heads is important experimentally.

---

## 18. Experimental Consequences

The proof suggests a minimal experiment. The experiment should directly test whether next-two training makes \(h_T\) contain branch information in the K=2 distribution.

### 18.1 Dataset

Use sequences of the form

```text
BR_b F00 F01 ... F{L-1} U0 U1 A_SHARED S_b
```

The evaluation prefix ends after

```text
BR_b F00 F01 ... F{L-1} U0 U1
```

At that prefix state:

```text
offset 1 target = A_SHARED
offset 2 target = S_b
```

### 18.2 Training conditions

Use the same architecture whenever possible.

| Condition | Active loss | Purpose |
|---|---|---|
| Fixed next-one | only offset 1 | tests whether architecture alone is enough |
| Next-two | offsets 1 and 2 | tests the effect of second-token supervision |
| Standard autoregressive LM | ordinary next-token loss | checks whether rollout can be learned |

The most important comparison is:

\[
\text{fixed next-one with future heads} \quad \text{vs.} \quad \text{next-two with the same future heads}.
\]

This controls for extra parameters.

### 18.3 Primary metrics

The primary metrics should evaluate single-prefix prediction, not only rollout.

1. **Offset-1 accuracy**  
   Measures whether both models can predict \(A\).

2. **Offset-2 single-prefix accuracy**  
   Measures whether \(h_T\) can directly predict \(S_B\).

3. **Offset-2 target probability**  
   Measures the probability assigned to the correct \(S_B\) from \(h_T\).

4. **Worst-branch offset-2 probability**  
   Detects brittle success hidden by averages.

5. **Branch-swap consistency**  
   Change only \(\operatorname{BR}_b\). The predicted \(S_B\) should change accordingly.

6. **Frozen probe from \(h_T\) to \(B\)**  
   Freeze the trained model and train a small probe to predict \(B\) from \(h_T\). This tests whether branch information is present in the representation, not only whether a particular head is trained.

7. **Gradient branch variation**  
   Measure whether the second-token loss creates branch-dependent gradients at \(h_T\).

### 18.4 Expected result pattern

The theory predicts the following pattern.

| Condition | Offset 1 | Offset 2 from same \(h_T\) | Branch swap | Frozen probe |
|---|---|---|---|---|
| Fixed next-one | high | low or unstable | weak | weak or unstable |
| Next-two | high | high | strong | strong |

The standard autoregressive model may pass rollout while not providing a direct offset-2 prediction from \(h_T\). That would support the distinction between rollout success and single-prefix future prediction.

### 18.5 What would weaken the hypothesis

The hypothesis would be weakened if, across seeds, the fixed next-one condition matches next-two on all of the following:

- offset-2 single-prefix accuracy,
- branch-swap consistency,
- frozen probe accuracy,
- and offset-2 target probability.

That outcome would suggest that, in this training setup, next-one already caused \(h_T\) to preserve branch information despite the absence of direct second-token supervision.

### 18.6 What would support the hypothesis

The hypothesis would be supported if:

- fixed next-one predicts \(A\) but fails to predict \(S_B\) from \(h_T\),
- next-two predicts both \(A\) and \(S_B\) from \(h_T\),
- branch-swap changes the next-two model's second-token prediction,
- and the frozen probe finds more branch information in next-two \(h_T\) than in fixed next-one \(h_T\).

This would show that the second-token loss changes the prefix representation in exactly the way predicted by the theorem.

---

## 19. Final Conclusion

The K=2 theory proves a clean objective-level separation.

The immediate next token is shared:

\[
Y_1=A.
\]

The second future token is branch-dependent:

\[
Y_2=S_B.
\]

Therefore next-one prediction at the decision state can be solved without preserving branch information in \(h_T\). However, next-two prediction cannot be solved with a branch-blind \(h_T\), because the second-token loss directly asks \(h_T\) to predict \(S_B\).

The resulting core claim is:

> In a minimal K=2 long-horizon branch distribution, next-two prediction imposes a direct requirement for the prefix hidden state to contain early branch information, while next-one prediction at the same prefix does not.

This is the correct minimal theoretical anchor for the experimental design.
