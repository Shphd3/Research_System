# When Do Common Features Suppress Long-Tail Features?

## A Theory-and-Evidence Note on Effective Overlap in Transformer Training

## Abstract

This note studies when a high-frequency common feature can suppress the learning of a low-frequency long-tail feature during cross-entropy training. The key lesson is that **rarity is not the same as suppression**. A rare feature may learn slowly simply because it appears in fewer examples. Destructive suppression is stronger: it means that updates caused by common examples actively push the model in a direction that hurts the rare feature.

We begin with a clean baseline. Suppose the common feature and rare feature are statistically independent, their raw feature directions are orthogonal, and the model uses block-decoupled linear parameters. In that setting, common-feature examples do not directly update the rare-feature parameter. The rare feature may still learn slowly because its sample frequency is low, but this is sample scarcity rather than destructive interference.

The experiments then refine the theory. In controlled output-head and tiny-attention models, suppression appears when three conditions hold simultaneously: the common feature is much more frequent, the common and rare features share a prediction-relevant direction, and their targets conflict. For example, in the controlled output-head experiment, increasing overlap from $\rho=0$ to $\rho=0.6$ delayed rare learning from $T_{0.9}=140$ steps to $T_{0.9}=420$ steps under the same $90/10$ frequency ratio and conflicting targets. The gradient cosine became negative, showing that common-feature updates actively opposed rare-feature updates.

However, the later Transformer experiments revise the broad conjecture. Shared wording or shared semantic category alone is not enough to guarantee suppression. In semi-real text and semantic-fact Transformers, the model often separated common and rare examples in prediction-relevant hidden directions. Rare capital facts did not learn more slowly than equally rare mineral facts, even when common capital facts dominated the data. Therefore, the correct variable is not surface overlap or human-interpretable semantic relatedness. The correct variable is **persistent effective overlap** in the model's prediction-relevant subspace.

The final claim is:

$$
\boxed{
\text{common features suppress long-tail features only when frequency imbalance, target conflict, and persistent prediction-relevant effective overlap occur together.}
}
$$

The decision table below summarizes the refined conclusion.

| Persistent prediction-relevant overlap? | Target conflict? | Frequency imbalance? | Expected behavior |
|---|---|---|---|
| No | No | Any | No destructive suppression. Learning may be independent or beneficial. |
| No | Yes | Yes | Rare learning may be slow due to rarity, but common updates do not strongly suppress rare prediction. |
| Yes | No | Yes | Coupling is usually benign or helpful because common and rare features point toward the same target. |
| Yes | Yes | Weak or balanced | Interference may exist, but rare examples provide enough corrective updates to reduce delay. |
| Yes | Yes | Strong | Destructive suppression is expected: common updates can delay rare learning or push rare logits toward the wrong target. |
| Surface or semantic overlap only | Any | Any | No conclusion follows until prediction-relevant effective overlap is measured. |

---

## 1. Motivation

Long-tail learning is a central problem in modern machine learning. Language models, vision models, and multimodal systems are trained on distributions where some patterns occur extremely often while others occur rarely. It is natural to ask whether common patterns dominate the model and prevent rare patterns from being learned.

The initial conjecture can be written informally as

$$
\text{common features suppress long-tail features}.
$$

This statement is intuitive, but it is not precise enough. It mixes two distinct phenomena.

The first phenomenon is **sample scarcity**. A rare feature appears in fewer training examples, so it receives fewer direct gradient updates. This alone can make it learn later than a common feature.

The second phenomenon is **destructive interference**. A common-feature update changes the model parameters in a way that increases the rare-feature loss, reduces rare-feature probability, suppresses rare-feature attention, or moves the rare-feature logit toward the wrong target. This is a stronger and more interesting claim.

The purpose of this note is to separate these two phenomena. We want to know when rare learning is slow merely because of insufficient examples, and when it is slow because common-feature updates actively work against it.

The final answer is conditional. Common-feature suppression is real in controlled settings where the common and rare features remain entangled in a prediction-relevant direction and their targets conflict. But the broad claim does not hold automatically in Transformers, because a Transformer may learn to separate surface-similar or semantically related examples in hidden space.

---

## 2. Three Kinds of Overlap

The most important conceptual point is that there are several different notions of overlap. Confusing them leads to incorrect conclusions.

Let $z_c,z_r\in\{0,1\}$ denote whether a common feature and a rare feature occur in an example. Let $u_c,u_r\in\mathbb{R}^d$ denote their raw feature directions, with

$$
\|u_c\|_2=\|u_r\|_2=1.
$$

A simple input model is

$$
x=z_cu_c+z_ru_r+\epsilon,
$$

where $\epsilon$ represents background variation.

### 2.1 Statistical Co-Occurrence

The first notion is whether the two features occur together in the data. The two feature indicators are statistically independent if

$$
z_c\perp z_r,
$$

or equivalently,

$$
\mathbb{P}(z_c=1,z_r=1)
=
\mathbb{P}(z_c=1)\mathbb{P}(z_r=1).
$$

This condition says that observing the common feature does not change the probability of observing the rare feature. It says nothing about whether their feature vectors point in the same direction.

### 2.2 Raw Geometric Overlap

The second notion is raw feature-vector overlap. Define

$$
\rho_{\mathrm{raw}}
=
\langle u_c,u_r\rangle.
$$

If $\rho_{\mathrm{raw}}=0$, the raw feature directions are orthogonal. If $\rho_{\mathrm{raw}}\neq 0$, the common and rare features overlap in the input feature space.

This is the overlap controlled in the clean vector experiments.

### 2.3 Effective Prediction-Relevant Overlap

The third notion is the most important one for Transformers. A Transformer does not predict directly from raw feature vectors. It maps inputs through embeddings, LayerNorm, attention, MLPs, residual connections, and output heads. Therefore, two examples that are raw-orthogonal may become coupled inside the model. Conversely, two examples that share many words may become separated in hidden space.

Let $\phi_\theta(\cdot)$ denote a model representation, such as a hidden state, attention key, output-head feature, or high-gain subspace projection. An effective overlap can be defined as

$$
\rho_\phi(\theta)
=
\frac{
\langle \phi_\theta(u_c),\phi_\theta(u_r)\rangle
}{
\|\phi_\theta(u_c)\|_2\|\phi_\theta(u_r)\|_2
}.
$$

This quantity is model-dependent. It can change during training. It is not a fixed property of the raw data.

When the mechanism is output-logit interference, we write this overlap as $\rho_{\mathrm{out}}$. When the mechanism is attention interference, we write it as $\rho_{\mathrm{attn}}$. When speaking generally, we use $\rho_{\mathrm{eff}}$.

The experimental results show that this distinction is essential:

$$
\text{surface overlap}
\not\Rightarrow
\text{effective overlap}.
$$

Likewise,

$$
\text{same semantic category}
\not\Rightarrow
\text{same prediction-relevant direction}.
$$

---

## 3. The No-Interference Baseline

We first prove the clean baseline. This baseline is important because it shows that frequency imbalance alone does not prove destructive interference.

Consider a linear logit model

$$
s(x)=\theta_c a_c(x)+\theta_r a_r(x),
$$

where

$$
a_c(x)=\langle x,u_c\rangle,
\qquad
a_r(x)=\langle x,u_r\rangle.
$$

For binary labels $y\in\{+1,-1\}$, the cross-entropy loss is

$$
\mathcal{L}(x,y)
=
\log\left(1+\exp(-ys(x))\right).
$$

Define the margin

$$
m(x)=ys(x).
$$

Then

$$
\frac{\partial \mathcal{L}}{\partial m}
=
-\frac{1}{1+\exp(m)}
=
-\sigma(-m),
$$

where $\sigma$ is the sigmoid function.

Because

$$
\frac{\partial m}{\partial \theta_r}=y a_r(x),
$$

we have

$$
\frac{\partial \mathcal{L}}{\partial \theta_r}
=
-\sigma(-m)y a_r(x).
$$

Now consider a common-only example. In the simplest case,

$$
x=u_c.
$$

If the raw feature directions are orthogonal,

$$
\langle u_c,u_r\rangle=0,
$$

then

$$
a_r(x)=\langle u_c,u_r\rangle=0.
$$

Therefore,

$$
\frac{\partial \mathcal{L}}{\partial \theta_r}=0.
$$

This means a common-only example does not directly update the rare-feature parameter.

We can state the baseline precisely.

**Proposition 1.** In a block-decoupled linear model, if common and rare feature directions are raw-orthogonal, then common-only examples do not directly update the rare-feature parameter. Therefore, any slower rare learning in this model is due to sample scarcity rather than destructive interference.

This proposition is simple, but it is the logical anchor of the whole note. If we want to claim destructive interference, we need evidence that common updates affect the rare predictor. Rarity alone is not enough.

---

## 4. How Overlap and Target Conflict Create Interference

Now suppose the raw feature directions are not orthogonal:

$$
\rho_{\mathrm{raw}}
=
\langle u_c,u_r\rangle
\neq 0.
$$

For a rare-only example $x=u_r$,

$$
a_c(x)=\langle u_r,u_c\rangle=\rho_{\mathrm{raw}},
$$

and

$$
a_r(x)=\langle u_r,u_r\rangle=1.
$$

Therefore the rare-example logit is

$$
s_r=\theta_r+\rho_{\mathrm{raw}}\theta_c.
$$

The second term,

$$
\rho_{\mathrm{raw}}\theta_c,
$$

is the leakage of the common-feature parameter into the rare-feature logit. It becomes large when the common-feature strength $\theta_c$ becomes large. Since common examples occur frequently, cross-entropy training may increase $\theta_c$ much faster than $\theta_r$.

Let $y_r$ be the correct rare-feature label. The rare margin is

$$
m_r=y_rs_r
=
y_r(\theta_r+\rho_{\mathrm{raw}}\theta_c).
$$

The common-feature leakage is harmful if it points against the correct rare target:

$$
y_r\rho_{\mathrm{raw}}\theta_c<0.
$$

It dominates the rare-feature term if

$$
|\rho_{\mathrm{raw}}\theta_c|>|\theta_r|.
$$

Thus the sufficient condition for destructive logit interference is

$$
y_r\rho_{\mathrm{raw}}\theta_c<0
\qquad\text{and}\qquad
|\rho_{\mathrm{raw}}\theta_c|>|\theta_r|.
$$

This gives a precise mechanism:

$$
\boxed{
\text{overlap is harmful only when it points toward a conflicting target and dominates the rare signal.}
}
$$

If the common and rare targets agree, overlap can be beneficial. This is why target conflict is not a minor detail. It is the switch that determines whether shared directions help or hurt.

---

## 5. Gradient Interference: A Direct Test of Suppression

The logit derivation predicts that common updates may hurt rare learning when the two gradients point against each other.

Let

$$
g_c=\nabla_\theta L_c
$$

be the gradient from common examples, and let

$$
g_r=\nabla_\theta L_r
$$

be the gradient from rare examples. A first-order Taylor expansion gives

$$
L_r(\theta-\eta g_c)
\approx
L_r(\theta)-\eta\langle g_r,g_c\rangle.
$$

If

$$
\langle g_r,g_c\rangle<0,
$$

then the common update increases the rare loss to first order. This is a clean mathematical signature of destructive interference.

If

$$
\langle g_r,g_c\rangle=0,
$$

then there is no first-order interaction.

If

$$
\langle g_r,g_c\rangle>0,
$$

then the common update helps the rare loss to first order.

This is why gradient cosine is an important diagnostic:

$$
\cos(g_c,g_r)
=
\frac{\langle g_c,g_r\rangle}
{\|g_c\|_2\|g_r\|_2}.
$$

A negative gradient cosine is stronger evidence for suppression than a delayed rare threshold alone, because delayed learning could be caused merely by sample scarcity.

---

## 6. Controlled Evidence: Output-Head Model

The cleanest experiment directly tests the overlap-conflict-frequency mechanism.

The model is

$$
z=Wx.
$$

The common direction is

$$
u_c=e_1.
$$

The rare direction is

$$
u_r=\rho e_1+\sqrt{1-\rho^2}e_2.
$$

Therefore,

$$
\langle u_c,u_r\rangle=\rho.
$$

The common target is class $0$. In conflict conditions, the rare target is class $1$. In aligned controls, the rare target is also class $0$.

The results are:

| Condition | Final rare probability | Minimum gradient cosine | Maximum leakage ratio | First step rare $p\ge0.9$ |
|---|---:|---:|---:|---:|
| orthogonal conflict, $90/10$ | $0.978$ | $0.000$ | $0.00$ | $140$ |
| mild overlap conflict, $90/10$ | $0.970$ | $-0.250$ | $0.82$ | $200$ |
| strong overlap conflict, $90/10$ | $0.946$ | $-0.600$ | $2.08$ | $420$ |
| strong overlap aligned, $90/10$ | $0.990$ | $0.600$ | $6.37$ | $40$ |
| strong overlap conflict, $50/50$ | $0.988$ | $-0.600$ | $0.40$ | $80$ |

The important comparison is between orthogonal conflict and strong-overlap conflict under the same $90/10$ frequency ratio:

$$
T_{0.9}(\rho=0)=140,
$$

whereas

$$
T_{0.9}(\rho=0.6)=420.
$$

Rare learning is three times slower when the rare feature overlaps with a frequent conflicting common feature.

The gradient cosine confirms destructive interference:

$$
\cos(g_c,g_r)=0
$$

for the orthogonal conflict case, but

$$
\cos(g_c,g_r)=-0.6
$$

for the strong-overlap conflict case.

The aligned control is the key sanity check. It has the same strong overlap and frequency imbalance, but the targets agree. It learns quickly:

$$
T_{0.9}=40.
$$

Therefore overlap alone is not bad. Overlap becomes harmful when it points toward a conflicting target.

The balanced-frequency control confirms the role of frequency. Keeping strong overlap and target conflict but changing the mixture from $90/10$ to $50/50$ improves rare learning from

$$
T_{0.9}=420
$$

to

$$
T_{0.9}=80.
$$

The controlled conclusion is:

$$
\boxed{
\text{persistent overlap}+\text{target conflict}+\text{frequency imbalance}
\Rightarrow
\text{destructive rare-learning delay}.
}
$$

---

## 7. Controlled Evidence: Tiny Attention Model

The output-head model is deliberately simple. The next question is whether the same mechanism survives after adding attention.

The tiny attention model predicts from two-token prefixes. The common pattern is

$$
[A,B]\rightarrow 0,
$$

and the rare pattern is

$$
[X,Y]\rightarrow y_r.
$$

In the conflict condition, $y_r=1$. In the aligned condition, $y_r=0$. Rare token vectors overlap with common token vectors by $\rho$.

The results are:

| Condition | Final rare probability | First step rare $p\ge0.99$ | Minimum gradient cosine | Maximum rare-loss increase after one common step |
|---|---:|---:|---:|---:|
| orthogonal conflict, $90/10$ | $0.998$ | $140$ | $-0.002$ | $0.0000$ |
| mild overlap conflict, $90/10$ | $0.998$ | $180$ | $-0.289$ | $0.0003$ |
| strong overlap conflict, $90/10$ | $0.997$ | $240$ | $-0.636$ | $0.0007$ |
| strong overlap aligned, $90/10$ | $0.999$ | $140$ | $0.636$ | $-0.0000$ |
| strong overlap conflict, $50/50$ | $0.999$ | $120$ | $-0.636$ | $0.0007$ |

The same qualitative pattern appears. Strong-overlap conflict delays rare high-confidence learning:

$$
T_{0.99}=140
\rightarrow
240.
$$

The gradient cosine becomes more negative as overlap increases:

$$
-0.002
\rightarrow
-0.289
\rightarrow
-0.636.
$$

The aligned condition has positive gradient cosine:

$$
0.636.
$$

This means the same shared direction can help or hurt depending on the target relation.

The delay is smaller than in the output-head-only model. This is informative rather than problematic. Attention gives the model more ways to separate common and rare contexts. Therefore the mechanism survives attention, but attention can weaken it.

---

## 8. Causal and Robustness Tests

The follow-up experiments ask whether the controlled mechanism is causal and robust.

### 8.1 Causal Direction Intervention

After training a strong-overlap model, the rare input is modified by removing either the shared common component or the rare-only component.

| Condition | Intervention | Rare probability | Loss change |
|---|---|---:|---:|
| strong overlap conflict | original | $0.951$ | $0.000$ |
| strong overlap conflict | remove shared common component | $0.999$ | $-0.050$ |
| strong overlap conflict | remove rare-only component | $0.006$ | $5.029$ |
| strong overlap aligned | original | $0.990$ | $0.000$ |
| strong overlap aligned | remove shared common component | $0.791$ | $0.224$ |
| strong overlap aligned | remove rare-only component | $0.997$ | $-0.007$ |

In the conflict case, removing the shared common component improves rare prediction:

$$
0.951\rightarrow 0.999.
$$

In the aligned case, removing that same shared component hurts:

$$
0.990\rightarrow 0.791.
$$

This is strong causal evidence. The shared component is not intrinsically bad. It is bad when it carries pressure toward the wrong target.

### 8.2 Robustness Sweep

The sweep varies overlap and rare frequency. Each cell is the first step where rare probability reaches $0.9$.

| Rare frequency | $\rho=0.00$ | $\rho=0.25$ | $\rho=0.50$ | $\rho=0.70$ | $\rho=0.85$ |
|---|---:|---:|---:|---:|---:|
| $50\%$ rare | $40$ | $40$ | $80$ | $120$ | $240$ |
| $20\%$ rare | $80$ | $120$ | $200$ | $320$ | $680$ |
| $10\%$ rare | $160$ | $240$ | $360$ | $720$ | not reached |
| $5\%$ rare | $360$ | $520$ | $920$ | not reached | not reached |

The table has two monotonic directions. Moving left to right increases overlap and usually delays rare learning. Moving top to bottom decreases rare frequency and also delays rare learning. The worst case is rare, overlapping, and conflicting.

### 8.3 Mini-Batch Repeatability

With stochastic mini-batches, the mean threshold step is

$$
166.7
$$

for orthogonal conflict and

$$
493.3
$$

for strong-overlap conflict. The gap is much larger than the seed-to-seed standard deviation. Therefore the effect is not an artifact of deterministic expected-gradient training.

### 8.4 Learned Embeddings Can Escape Suppression

The learned-embedding test is a crucial bridge toward Transformers. With fixed embeddings, the rare feature remains close to the common feature and learns slowly:

$$
T_{0.9}=640.
$$

With learned embeddings, the model moves the rare embedding away from the common embedding and learns faster:

$$
T_{0.9}=120.
$$

The final embedding overlap changes from

$$
0.589
$$

to

$$
-0.622.
$$

This shows that overlap is not always permanent. A trainable model can sometimes reduce effective overlap and avoid suppression.

### 8.5 Multi-Token Pattern Control

The multi-token experiment shows that the mechanism is not limited to one-vector features. Strong-overlap conflict does not reach the $0.9$ rare threshold, while strong-overlap aligned reaches it at $160$ steps. This confirms that composed patterns can still suffer if they preserve a conflicting common direction.

---

## 9. Transformer Result I: Shared Wording Is Not Enough

The semi-real Transformer experiment tests whether shared surface wording is enough to create suppression.

The common sentence is

```text
the clinic code alpha means red .
```

The shared-wording rare conflict sentence is

```text
the clinic code xenon means blue .
```

The separated-wording rare conflict sentence is

```text
the archive symbol xenon means blue .
```

If surface overlap were sufficient for suppression, the shared-wording conflict case should learn more slowly than the separated-wording conflict case.

That did not happen.

For $d=64$ at $90/10$,

$$
T_{0.99}(\text{shared conflict})=500,
$$

and

$$
T_{0.99}(\text{separated conflict})=500.
$$

For $d=32$ at $90/10$,

$$
T_{0.99}(\text{shared conflict})=1000,
$$

and

$$
T_{0.99}(\text{separated conflict})=1000.
$$

Thus shared wording did not create extra rare delay.

However, target conflict still matters. The aligned shared-wording cases learn faster:

$$
T_{0.99}=300
$$

for $d=64$, and

$$
T_{0.99}=600
$$

for $d=32$.

The hidden-space probes explain why shared wording was not enough. In aligned cases, the top-subspace cosine is near $1$, which is fine because both examples want the same answer. In conflicting cases, the top-subspace cosine is near zero or modest, meaning the Transformer has separated the examples in the prediction-relevant subspace.

The conclusion is:

$$
\boxed{
\text{shared wording is not equivalent to shared prediction-relevant direction.}
}
$$

---

## 10. Transformer Result II: Shared Semantic Relation Is Not Enough

The semantic-fact experiment tests a more realistic hypothesis: do common capital facts suppress rare capital facts?

The common relation is

$$
\text{country}\rightarrow\text{capital city}.
$$

The rare families are rare capital facts and rare mineral-color facts. In the main condition, both rare families have the same frequency:

$$
p(\text{rare capital})=0.05,
\qquad
p(\text{rare mineral})=0.05.
$$

If common capital facts suppress rare capital facts, then rare capital facts should learn more slowly than rare mineral facts.

They did not.

In the common-capital-dominant condition,

$$
T_{0.9}(\text{rare capital})
=
T_{0.9}(\text{rare mineral})
$$

for both dimensions:

$$
d=64:\quad 400=400,
$$

and

$$
d=32:\quad 700=700.
$$

The common-direction intervention also did not support suppression. Removing the mean common-capital direction from rare capital examples did not improve rare capital prediction. It slightly hurt or barely changed it:

$$
\Delta p=-0.0003
$$

for $d=64$, and

$$
\Delta p=-0.0057
$$

for $d=32$.

The latent-direction probes suggest that rare capital and rare mineral examples were not forced into the same learned direction. Their hidden and top-subspace cosines were near zero or negative in several conditions.

Therefore the semantic-fact experiment falsifies the broad semantic-overlap claim:

$$
\boxed{
\text{common semantic relation exposure alone did not selectively suppress rare same-relation facts in this benchmark.}
}
$$

The safer statement is:

$$
\boxed{
\text{same semantic category does not necessarily mean same learned prediction direction.}
}
$$

---

## 11. Reconciling the Controlled and Transformer Results

The controlled experiments and Transformer experiments do not contradict each other. They test different notions of overlap.

In the controlled experiments, overlap is explicit and persistent. The model cannot easily move the rare feature away from the common feature unless the experiment allows learned embeddings. Therefore the mechanism appears clearly.

In the Transformer experiments, the inputs may share words or semantic relations, but the model can construct different hidden directions. When the model separates them, destructive interference is reduced or absent.

The correct reconciliation is:

$$
\boxed{
\text{controlled experiments show what happens if effective overlap persists.}
}
$$

and

$$
\boxed{
\text{Transformer experiments show that effective overlap need not persist.}
}
$$

This is the main scientific refinement. The theory should not be stated as a universal claim that common features suppress rare features. It should be stated as a conditional mechanism governed by persistent prediction-relevant overlap.

---

## 12. Revised Mechanism Statement

We can now state the refined mechanism.

**Revised Mechanism.** Consider a model trained by cross-entropy on common examples with probability $p_c$ and rare examples with probability $p_r$, with

$$
p_c\gg p_r.
$$

Common-feature learning destructively interferes with rare-feature learning when the following conditions hold.

First, the common and rare examples remain coupled in a prediction-relevant subspace. This can be measured by output-head overlap, attention-subspace overlap, high-gain singular-vector overlap, gradient cosine, or a causal intervention on the common subspace.

Second, the common and rare targets conflict:

$$
P(y\mid c)\neq P(y\mid r).
$$

Third, the common feature is frequent enough to shape the shared parameter trajectory before the rare feature receives enough corrective updates.

Under these conditions, common-feature updates can delay rare learning or increase rare loss.

At the logit level, this appears as

$$
s_r\approx \theta_r+\rho_{\mathrm{out}}\theta_c.
$$

If

$$
|\rho_{\mathrm{out}}\theta_c|>|\theta_r|
$$

and the perturbation has the wrong sign, the rare margin is dominated by the common feature.

At the attention level, the corresponding perturbation has the form

$$
\rho_{\mathrm{attn}}^2\beta_c.
$$

If this dominates the rare attention strength, the model may allocate too little attention mass to the rare feature. Through softmax, a score disadvantage $\Delta$ can suppress rare attention approximately as

$$
\alpha_r\approx \exp(-\Delta).
$$

This mechanism is conditional. If the model learns to reduce $\rho_{\mathrm{out}}$, $\rho_{\mathrm{attn}}$, gradient conflict, or high-gain subspace overlap, then suppression may disappear even when the examples look similar to humans.

---

## 13. What Earlier Conjectures Need to Change

The experiments force four revisions.

### 13.1 Frequency imbalance is necessary but not sufficient.

Rare examples learn slowly when they are rare. But destructive interference requires evidence that common updates hurt rare prediction. Negative gradient cosine, harmful subspace projection, or causal improvement after removing a common component are stronger evidence than delayed threshold crossing alone.

### 13.2 Raw overlap is sufficient in controlled models but not the whole story.

When raw overlap is forced and persistent, the mechanism is clear. But trainable embeddings and Transformers can change the representation. Therefore raw overlap should be treated as one possible source of effective overlap, not as the final explanatory variable.

### 13.3 Surface overlap is not enough.

The semi-real Transformer experiment shows that sentences sharing many words do not necessarily interfere. The model can map them into different prediction-relevant directions.

### 13.4 Semantic category is not enough.

The semantic-fact experiment shows that common capital facts did not selectively suppress rare capital facts. The model did not behave as if all capital facts shared one harmful common direction.

---

## 14. Recommended Next Experiments

The next experiments should directly measure and manipulate effective overlap.

### 14.1 Measure a Multi-Dimensional Common Subspace

Construct a common-feature subspace

$$
C_k=\operatorname{span}(v_1,\ldots,v_k),
$$

where $v_i$ are principal directions from common examples or high-gain output-head singular directions.

For a rare hidden state $h_r$, measure

$$
M_r(k)=\|P_{C_k}h_r\|^2.
$$

This measures how much of the rare representation lies in the common subspace.

### 14.2 Intervene on the Common Subspace

Evaluate

$$
h_r'=h_r-P_{C_k}h_r.
$$

If removing $C_k$ improves rare prediction in conflict cases, that is causal evidence for suppression. If it hurts or does nothing, the common subspace is not suppressing the rare feature.

### 14.3 Force Effective Overlap in a Transformer

The current Transformer can often separate rare facts. To stress the mechanism, make separation harder by reducing hidden dimension, freezing embeddings, freezing early layers, limiting attention heads, or designing rare examples that must reuse the same relation template.

### 14.4 Compare Model Classes

A useful progression is:

| Model | Purpose |
|---|---|
| bag-of-embeddings output head | little ability to separate contexts, so suppression should be strongest |
| MLP over averaged tokens | nonlinear separation possible, but no attention routing |
| one-layer causal Transformer | attention can route context and reduce overlap |
| two-layer causal Transformer | stronger separation capacity |

The prediction is:

$$
\text{suppression should be strongest when the model cannot reduce effective overlap.}
$$

---

## 15. Conclusion

The original broad conjecture was that common features suppress long-tail features. The experiments show that this is too broad. The refined conclusion is narrower and stronger:

$$
\boxed{
\text{common features suppress long-tail features only when their learned prediction-relevant directions remain entangled and their targets conflict.}
}
$$

In an ideal independent, raw-orthogonal, block-decoupled linear model, there is no direct first-order interference. Rare learning is slower only because the rare feature appears in fewer examples.

In controlled models where overlap is explicit and persistent, common-feature learning can destructively interfere with rare learning. The evidence includes negative gradient cosine, delayed rare threshold crossing, robustness across overlap and frequency, and causal improvement after removing the harmful shared component.

In flexible Transformers, surface similarity and semantic similarity are not enough. The model can sometimes separate examples in hidden space, avoiding suppression even when the examples look similar to humans.

Therefore the central object for future work is not surface overlap but effective overlap in the model's prediction-relevant subspace. This is what should be measured, manipulated, and theoretically modeled.
