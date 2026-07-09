# A06 Router Training Dynamics Story

Status:
- Type: research-line story.
- Line: `06_geometry_proxy_preservation`.
- Canonical language: English.
- Current mode: theory-forward synthesis.
- Chinese companion: `story_cn.md`.

## 0. Terminology / Definitions

| Term | Plain meaning | Concrete object or formula | Why it matters | Cannot prove |
|---|---|---|---|---|
| Feature-to-expert binding | A feature keeps being routed to the same intended expert. | $P(e=a(f)\mid f)$ and matched route margin. | The preservation question is about stable binding, not only cluster visibility. | Expert utility. |
| Route margin | Score gap between the matched expert and the strongest competitor. | $m_f=\min_{e\ne a(f)}(w_{a(f)}-w_e)^\top\mu_f$. | Positive margin is the local safety buffer. | Global token safety without tail/spread audit. |
| Soft router | A continuous router that mixes all experts. | $p_e(h)=\operatorname{softmax}(w_e^\top h/\tau)$. | It gives a clean gradient formula before top-1 discontinuities. | Behavior of every sparse implementation. |
| Expert advantage | Whether expert $e$ would reduce loss more than the current mixture. | $A_e(h,y)=-\langle\nabla_{\hat y}\ell,\ E_e(h)-\hat y\rangle$. | It decides the direction of the router row update. | It does not identify semantic features. |
| Noise update | A router update not aligned with the target feature margin. | Update component with zero or weak conditional mean for feature $f$. | It can erode a finite margin by random walk or biased drift. | That all non-feature updates are harmless. |
| Top-1 router | A sparse router that selects one expert. | $r(h)=\arg\max_e w_e^\top h$. | It changes correction from continuous expert comparison to selected-expert feedback. | A differentiable comparison among all experts. |

## 1. Abstract

A06 has shown that route-relevant feature centers can be discovered in controlled
synthetic settings and can initialize a top-1 router, but preservation depends on
a finite positive margin buffer. The next missing object is not another
initializer. The missing object is a minimal training-dynamics model for how the
router row vectors move after initialization.

The proposed story is:

```text
initial score asymmetry
-> routed expert receives a loss-derived advantage or disadvantage signal
-> router rows move along the current hidden state direction
-> correct feature-aligned signals increase the matched margin
-> noise/common/background signals consume the margin
-> sparse top-1 feedback weakens correction because unselected experts are not
   individually evaluated by the task loss
```

The next minimal anchor should test the one-step soft-router gradient formula
and then use it as the baseline for top-1 sparse-router dynamics.

## 2. Research Question

Current A06 question:

> In a simple synthetic MoE training surface, how does the router move after
> initialization, and which update components increase or destroy feature
> margin?

This replaces the weaker question "can we find a feature center?" with the more
mechanistic question "what is the first-order router movement induced by a
sample?"

## 3. Why This Question Is Confusing

High feature NMI can be caused by a good initial boundary even if training is
not learning the boundary. High task accuracy can be reached while the feature
partition is being erased. A soft router has a smooth gradient that compares
expert outputs through the mixture. A top-1 router only receives feedback
through the selected expert, and the unselected experts are not individually
tested by the task loss for that token.

Therefore, discovery, initialization, correction, and preservation must be
separated.

## 4. Concrete Data / Training Layout

The minimal target is the existing controlled no-position synthetic bridge:

```text
one causal Transformer layer
-> one MoE layer
-> uniformly sampled synthetic features
-> route-position hidden states
-> feature target loss or full-sequence LM loss, depending on the guard
```

For theory, freeze the hidden representation first:

$$
h=\mu_f+\epsilon,
$$

where $\mu_f$ is the feature center and $\epsilon$ is within-feature spread. Then
add hidden drift later:

$$
\begin{aligned}
\Delta m_f
&=
(\Delta w_a-\Delta w_e)^\top\mu_f \\
&\quad+
(w_a-w_e)^\top\Delta\mu_f \\
&\quad+
(\Delta w_a-\Delta w_e)^\top\Delta\mu_f.
\end{aligned}
$$

## 5. Physical Intuition

The router row is a movable decision boundary. A training sample moves the row
according to the expert advantage seen on that sample. If the selected or
preferred expert is useful for feature $f$, the row should move toward
$\mu_f$. If the update is caused by background/common tokens, the row may move
toward directions that are frequent but not feature-discriminative. Top-1
sparsity makes this more fragile because the task loss does not compare all
experts for the token.

## 6. Definitions And Metrics

For feature $f$ and matched expert $a(f)$:

$$
m_f(t)=\min_{e\ne a(f)}(w_{a(f)}(t)-w_e(t))^\top\mu_f(t).
$$

The router is preserved if the low-tail token margin stays positive, not merely
if the center margin is positive.

For one sample $(h,y)$, define soft-router mixture output:

$$
\hat y=\sum_e p_e(h)E_e(h),
\qquad
p_e(h)=\frac{\exp(w_e^\top h/\tau)}{\sum_j\exp(w_j^\top h/\tau)}.
$$

Define expert advantage:

$$
A_e(h,y)=-\left\langle \nabla_{\hat y}\ell(\hat y,y), E_e(h)-\hat y\right\rangle.
$$

If $A_e>0$, increasing expert $e$'s routing weight locally reduces loss. If
$A_e<0$, increasing that expert's routing weight locally increases loss.

## 7. Mathematical Model

### 7.1 Soft Router

For the soft router,

$$
\frac{\partial L}{\partial w_e}
=
\frac{p_e}{\tau}
\left\langle \nabla_{\hat y}\ell, E_e(h)-\hat y\right\rangle h.
$$

Gradient descent gives:

$$
\Delta w_e
=
\eta\frac{p_e}{\tau}A_e(h,y)h.
$$

Thus the router row update has three factors:

1. routing probability $p_e$;
2. local expert advantage $A_e$;
3. hidden-state direction $h$.

For a matched expert $a$ against competitor $b$:

$$
\Delta m_{f,a,b}
\approx
\eta\frac{1}{\tau}
\left[p_aA_a-p_bA_b\right]h^\top\mu_f.
$$

This is the minimal "how does router move" equation.

### 7.2 Correct Signal Versus Noise Signal

A correct feature signal for feature $f$ satisfies:

$$
\mathbb E[p_aA_a-p_bA_b\mid f] > 0.
$$

A pure noise signal satisfies:

$$
\mathbb E[p_aA_a-p_bA_b\mid f]\approx 0,
$$

but its variance can still erode margin over many steps. A biased common signal
has nonzero mean along a direction that is frequent but not feature-specific.
That is more dangerous than zero-mean noise because it creates systematic row
drift.

### 7.3 Top-1 Sparse Router

Let:

$$
r(h)=\arg\max_e s_e(h),\qquad s_e=w_e^\top h.
$$

If the implementation uses a probability-weighted selected output,

$$
\hat y=p_r(h)E_r(h),
$$

then:

$$
\frac{\partial L}{\partial w_j}
=
\frac{p_r}{\tau}
\left(1_{j=r}-p_j\right)
\left\langle\nabla_{\hat y}\ell,E_r(h)\right\rangle h.
$$

With $B_r=-\langle\nabla_{\hat y}\ell,E_r(h)\rangle$:

$$
\Delta w_j
=
\eta\frac{p_r}{\tau}(1_{j=r}-p_j)B_r h.
$$

If the selected expert is useful, the selected row moves toward $h$ and
unselected rows move away from $h$. If the selected expert is bad, the selected
row moves away and all unselected rows move weakly toward $h$, but the update
does not identify which unselected expert would have been best.

This is the basic correction gap between soft and top-1 routing.

## 8. Propositions / Proof State

**Proposition 1: Soft-router row movement is advantage-weighted movement along
the current hidden state.** This follows by differentiating the softmax mixture.

**Proposition 2: A feature margin increases in expectation if the matched
expert has greater conditional advantage than competitors on that feature.**
This follows from the one-step margin equation above.

**Proposition 3: Top-1 task feedback is selected-expert feedback, not full
expert comparison.** In probability-weighted top-1, unselected rows only receive
the denominator effect. In hard argmax without a selected probability multiplier,
task gradients to router scores can be zero and only auxiliary losses move the
router.

**Empirical proposition:** The A06 controlled preservation results are
consistent with a finite signal-noise margin budget, but A06 has not yet
directly measured one-step router advantage terms.

## 9. Mechanism Decomposition

The synthetic router training dynamics should be decomposed into:

1. Initial row-feature alignment.
2. Initial route margin.
3. Per-sample expert advantage.
4. Feature-aligned margin update.
5. Noise/common/background margin update.
6. Hidden-center drift.
7. Sparse-router correction gap.
8. Boundary crossing and sign flip.

The minimal audit should measure these terms before proposing another gate.

## 10. Evidence From Anchors

A06 provides the prior evidence:

- A06_17/A06_21: correct route-position centers preserve when current and
  cluster-aware margins stay positive.
- A06_23: top-1 preservation has a finite safe margin; small positive margin is
  not sufficient.
- A06_24_synthetic: common subtraction improves some symptoms but is not a
  reliable feature separator.
- A06_27: embedding-gradient selection can identify route-relevant states in a
  pointwise synthetic bridge.
- A06_28/A06_29: full-sequence LM gradients and DNS-style preservation do not
  yet preserve safe margin through long training.

## 11. Related Work Used As Modeling Borrowing

- Jacobs, Jordan, Nowlan, and Hinton (1991), [Adaptive Mixtures of Local
  Experts](https://www.cs.toronto.edu/~fritz/absps/jjnh91.pdf): classic
  responsibility/competition view for soft gating.
- Jordan and Jacobs (1994), [Hierarchical Mixtures of Experts and the EM
  Algorithm](https://direct.mit.edu/neco/article/6/2/181/5779/Hierarchical-Mixtures-of-Experts-and-the-EM):
  EM responsibility view for hierarchical gates.
- Shazeer et al. (2017), [Outrageously Large Neural Networks](https://arxiv.org/abs/1701.06538):
  practical sparse top-k MoE routing.
- Chen, Deng, Wu, Gu, and Li (2022), [Towards Understanding the MoE Layer in
  Deep Learning](https://proceedings.neurips.cc/paper_files/paper/2022/file/91edff07232fb1b55a505a9e9f6c0ff3-Paper-Conference.pdf):
  cluster-structured theory where routers can learn cluster-center features.
- Nguyen, Nguyen, and Ho (2023), [Demystifying Softmax Gating Function in
  Gaussian MoE](https://arxiv.org/abs/2305.03288): softmax-gate identifiability
  and gate-expert interaction.
- Nguyen, Akbarian, Yan, and Ho (2023), [Statistical Perspective of Top-K
  Sparse Softmax Gating MoE](https://arxiv.org/abs/2309.13850): top-k partitions
  create distinct input regions with different behavior.
- Nguyen, Ho, and Rinaldo (2024), [Sigmoid Gating is More Sample Efficient than
  Softmax Gating](https://arxiv.org/abs/2405.13997): softmax competition can
  create sample-efficiency and collapse issues.
- Chi et al. (2022), [On the Representation Collapse of Sparse MoE](https://arxiv.org/abs/2204.09179):
  routing can encourage hidden representations to cluster around expert
  centroids.

These papers do not solve A06 because they do not directly analyze our
synthetic Transformer + top-1 route-margin preservation surface. They provide
the mathematical vocabulary for responsibility, gate-expert interaction,
top-k partitioning, and collapse.

## 12. Claim Boundary

Can claim:

- The next A06 theory target should be one-step router movement and cumulative
  margin budget.
- Soft routing gives a clean advantage-weighted row-update equation.
- Top-1 routing weakens correction because only the selected expert is directly
  evaluated by the task path.

Cannot claim:

- A new gating method is established.
- MTP is needed for this step.
- Real-DCLM collapse is fully explained by the synthetic one-step model.
- Any high-NMI route is functionally useful.

## 13. Anchor Decomposition / Next Anchors

1. `06_30_noise_free_full_slot_preservation_anchor.md`
   - Decision question: Does ideal feature-center routing survive long full-LM
     training when all positions are feature-bearing and background tokens are
     removed?
2. `06_31_soft_router_one_step_gradient_dynamics_anchor.md`
   - Decision question: Does measured soft-router one-step movement match the
     advantage-weighted margin equation?
3. `06_32_top1_discrete_router_update_dynamics_anchor.md`
   - Decision question: Does top-1 selected-expert feedback explain lock-in and
     weak correction of wrong initial assignments?
4. `06_33_signal_noise_margin_budget_anchor.md`
   - Decision question: Can cumulative correct-signal, noise, common, and hidden
     drift terms predict margin crossing?
5. `06_34_soft_to_sparse_temperature_bridge_anchor.md`
   - Decision question: Does lowering soft-router temperature smoothly approach
     the top-1 correction gap?

## 14. Relation To Mainline

This story keeps A06 before A07 utility and before A11 MTP. It asks the basic
router-dynamics question first. MTP may later be used as a source of better
feature-aligned signals, but it should not enter until the router update model
is clear.

## 15. Next Decision

Write and audit `06_33_signal_noise_margin_budget_anchor.md`.

The minimum experiment should start from the no-background full-slot condition,
gradually add background positions, and measure when correct feature signal,
background signal, router drift, or hidden drift first predicts margin crossing.

## Source Map

- A06 map: `../../problem_anchors/06_geometry_proxy_preservation/research_map.md`
- A06 closure: `../../problem_anchors/06_geometry_proxy_preservation/closure/06_geometry_proxy_preservation_closure_report.md`
- A06_28 summary: `../../experiments/A06/A06_28_full_sequence_lm_gradient_selector_guard/summary.md`
- A06_29 summary: `../../experiments/A06/A06_29_dns_routing_preservation_audit/summary.md`
