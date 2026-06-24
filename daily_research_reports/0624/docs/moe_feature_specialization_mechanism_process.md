# MoE Feature Specialization: Mechanism And Research Process

## Abstract

The current problem is not merely whether expert load can look uniform. The real
question is whether uniformly occurring features can enter an expert partition
that is non-collapsed, interpretable, preserved after training begins, and
functionally useful.

The strongest mechanism hypothesis is that hidden states contain a shared
cross-feature component, denoted by $c$. A linear top-1 router scores expert
$e$ by $w_e^\top h$. Even without an explicit bias term, $w_e^\top c$ acts as
an implicit expert-specific common bias. The expert selected early by this
common bias receives more tokens and gradients, so the initial advantage can be
amplified by early training feedback.

On real text, proxy features can be discovered and linearly routed at step 0,
but ordinary training overwrites this partition by steps 5/10. Therefore the
current bottleneck is early-training preservation, not pure step-0
initialization.

## 0. Decision

**Decision.** The research line should be framed as anti-common-component,
anti-early-lock-in, feature-partition preservation, and functional-value
verification, rather than as load balancing alone.

**Blocking issue.** In real-text training, a proxy feature partition that is
already linearly routable at step 0 disappears in the early training window.
The structure exists at step 0, but is overwritten by steps 5/10.

**Retained evidence.**

- The common-component explanation for early collapse remains the strongest
  mechanism prior.
- Known feature centers and pseudo-feature centers can form clean partitions in
  controlled settings.
- The A07 line provides controlled evidence that a good partition can reduce
  rare-feature interference and bind routing to expert utility.

**Still unclear.**

- The exact source of the common component in real text.
- How to select route-relevant hidden states without labels.
- How to preserve the route partition during training without hurting language
  modeling loss.

**Minimal next step.** Write and execute a real-text early-preservation
protocol: test whether common-component control or anti-lock-in interventions
can let the proxy feature partition survive the step-5/10 window.

## 1. How The Research Question Should Be Stated

### 1.1 Parent Question

Can the router in a sparse MoE model make experts form stable, interpretable,
and reusable feature-level specialization?

Feature-level specialization requires at least four properties:

1. **Same-feature consistency.** Samples with the same feature should tend to
   enter the same expert or expert group.
2. **Non-collapse.** Most samples should not be absorbed by a small number of
   experts.
3. **Clear feature identity.** The route group should correspond to an
   operationally defined feature axis. In the current controlled setting, the
   preferred axis is the slot. If the constant token $B_i$ also varies, the
   minimal consistency key is $(\mathrm{slot}, B_i)$.
4. **Functional value.** The selected expert should actually contribute to the
   loss or ablation behavior of the corresponding sample group.

### 1.2 Current Subproblem

The current subproblem is:

**Why does ordinary random-initialized top-1 routing collapse at initialization
or early training even when feature frequencies are uniform, and how can we
construct a non-collapsed, feature-aligned partition that is preserved after
training begins?**

This is more precise than asking how to distribute features uniformly across
experts:

- uniform load only rules out single-expert collapse;
- uniform load does not imply same-feature consistency;
- same-feature consistency does not imply expert utility;
- therefore the A07 utility line must remain part of the main story.

### 1.3 Safest Meeting Sentence

The current claim is not that sparse MoE already forms semantic experts. The
claim is that we are decomposing why uniformly occurring features still fail to
enter a stable expert partition, what mechanism can preserve that partition
during early training, and whether the partition reduces feature interference.

## 2. Mechanism Model: Why Uniform Features Can Still Collapse

### 2.1 Variables

| Symbol | Meaning |
| --- | --- |
| $f$ | feature identity, for example a slot in the controlled task |
| $e$ | expert index |
| $h_f$ | mean route-position hidden state for feature $f$ |
| $c$ | common component shared across features |
| $r_f$ | feature-specific residual component |
| $w_e$ | router scoring vector for expert $e$ |
| $z_{f,e}$ | router logit for sending feature $f$ to expert $e$ |

The core decomposition is:

$$
h_f = c + r_f .
$$

The router score is:

$$
z_{f,e} = w_e^\top h_f
        = w_e^\top c + w_e^\top r_f .
$$

Define the common-bias term:

$$
a_e = w_e^\top c .
$$

The quantity $a_e$ is shared across all features. It is not feature signal; it
is an implicit common bias for expert $e$.

### 2.2 A Sufficient Condition For Step-0 Collapse

Let $e^\star$ be the expert with the largest common bias:

$$
e^\star = \arg\max_e w_e^\top c .
$$

For any other expert $e$, the score gap is:

$$
z_{f,e^\star} - z_{f,e}
= (w_{e^\star}-w_e)^\top c
  + (w_{e^\star}-w_e)^\top r_f .
$$

The first term is the common-component advantage. The second term is the
feature-residual correction. If for every feature $f$ and every other expert
$e$,

$$
(w_{e^\star}-w_e)^\top c
>
\left| (w_{e^\star}-w_e)^\top r_f \right|,
$$

then

$$
z_{f,e^\star} > z_{f,e}.
$$

All features are routed to the same expert $e^\star$. This shows why uniform
feature frequency does not guarantee uniform expert usage: if the common
component dominates router scores, the router can collapse even when the data
distribution is perfectly balanced.

### 2.3 Early Lock-In

The common bias explains the seed of collapse. Final collapse also needs a
training-dynamics explanation.

The intuition is:

1. At step 0, an expert wins because of $w_e^\top c$ or random geometric
   alignment.
2. A top-1 router sends more samples to the winning expert.
3. That expert receives more gradient updates and becomes more adapted to those
   samples.
4. The router and experts co-adapt to the early assignment.
5. A small initial bias becomes a stable partition or collapse basin.

A minimal amplification model is:

$$
\delta_{t+1} \approx (1+\rho)\delta_t + \xi_t,\qquad \rho > 0 ,
$$

where $\delta_t$ is the expert advantage at step $t$, and $\xi_t$ is training
noise. If $\rho>0$, early advantage is amplified unless an anti-lock-in
mechanism intervenes.

### 2.4 Router-Gradient Mechanism Under Sparse Top-1 Gating

The implementation used in the controlled A06/A07 training runs is sparse
top-1 routing with a selected gate probability, not full soft routing and not a
purely discrete argmax update. For one token with hidden state $h$, router
logits are

$$
z_e = w_e^\top h,\qquad
p_e = \frac{\exp(z_e)}{\sum_j \exp(z_j)} .
$$

The routed expert is the top-1 expert

$$
k = \arg\max_e z_e .
$$

Only expert $k$ computes the expert output, but that output is multiplied by
the selected softmax probability:

$$
y = p_k E_k(h).
$$

Let $\bar{y}=\partial \mathcal{L}/\partial y$ be the upstream gradient and
define the scalar

$$
s = \left\langle \bar{y}, E_k(h) \right\rangle .
$$

Then the router-logit gradient is

$$
\frac{\partial \mathcal{L}}{\partial z_j}
=
s\,\frac{\partial p_k}{\partial z_j}
=
s\,p_k\left(\mathbf{1}[j=k]-p_j\right).
$$

Therefore the router-row gradient is

$$
\frac{\partial \mathcal{L}}{\partial w_j}
=
s\,p_k\left(\mathbf{1}[j=k]-p_j\right)h .
$$

This has two important consequences:

1. **All router rows can receive gradient.** Even unselected router rows
   $j\neq k$ receive the gradient term $-s\,p_k p_j h$ through the softmax
   denominator.
2. **Only the selected expert receives this token's expert-function gradient.**
   The expert MLP update is sparse, because only $E_k$ is evaluated for this
   token.

Thus early lock-in is not a purely discrete argmax story. The discrete top-1
choice controls which expert receives function-learning signal, while the
selected gate probability supplies a continuous router-gradient signal to all
router rows. If an expert wins many early tokens and its expert output lowers
loss, the scalar $s$ can repeatedly move the selected row and competing rows in
a direction that increases the winning probability for similar hidden states.
This is a plausible micro-mechanism for the amplification term $\rho>0$ in the
early-lock-in model.

The implementation contract is:

$$
\text{hard dispatch: one expert per token}
\quad+\quad
\text{selected gate: } y=p_kE_k(h).
$$

This boundary matters. The result should not be described as full soft routing,
because unselected experts do not compute outputs. It also should not be
described as an argmax-only router update, because router weights still receive
continuous gradients through $p_k$.

### 2.5 Spatial Interpretation Of Collapse

In representation geometry, collapse does not necessarily mean that hidden
states themselves collapse into one point. It means that the router's decision
regions assign most of the hidden-state population to the same expert.

For a dot-product router, expert $e$ wins when

$$
w_e^\top h > w_j^\top h
\qquad \text{for all } j\neq e .
$$

Equivalently, expert $e$ owns the region

$$
\mathcal{R}_e
=
\left\{
h:
(w_e-w_j)^\top h > 0,\ \forall j\neq e
\right\}.
$$

These regions are conic decision cells in hidden-state space. The router rows
$w_e$ determine the separating hyperplanes

$$
(w_e-w_j)^\top h = 0 .
$$

Under the decomposition

$$
h_f = c + r_f ,
$$

all feature clusters share the same offset $c$ and differ by residual directions
$r_f$. If the residuals are small relative to the common component, then the
feature clusters form a cloud around $c$. If one router row $w_k$ is more
aligned with $c$ than the others, then

$$
(w_k-w_j)^\top c
>
\left|(w_k-w_j)^\top r_f\right|
$$

for many or all features. Geometrically, the whole feature cloud lies inside
$\mathcal{R}_k$, so many feature identities are routed to the same expert.

Training can then enlarge this collapsed region. For a token with hidden state
$h$ routed to expert $k$, the selected-gate gradient has the form

$$
\frac{\partial \mathcal{L}}{\partial w_j}
=
s\,p_k\left(\mathbf{1}[j=k]-p_j\right)h .
$$

If the selected expert's output helps reduce loss, the gradient-descent update
typically moves $w_k$ toward $h$ and pushes competing rows away from $h$. When
many early tokens share the common direction $c$, repeated updates move
$w_k$ toward the high-density common direction and rotate competing decision
boundaries away from it. The margin

$$
m_{k,j}(h)=(w_k-w_j)^\top h
$$

then increases for similar hidden states. This makes expert $k$ win even more
often in the next batch, producing a geometric feedback loop:

$$
\text{early route advantage}
\rightarrow
\text{more expert updates for } E_k
\rightarrow
\text{router row } w_k \text{ aligns more with the dense hidden region}
\rightarrow
\text{larger route margin for } k .
$$

This is the spatial version of early lock-in. The hidden representation may
still contain feature residuals $r_f$, but the router's decision cells no longer
separate those residual directions. In that case, collapse is a failure of
router-space partitioning over the hidden manifold, not necessarily a failure
of the hidden representation to contain feature information.

This distinction explains why feature probes or residual clustering can succeed
while ordinary top-1 routing still collapses: the feature information is present
in $r_f$, but the router rows and decision boundaries are aligned with the
common or dense direction instead of with the feature-residual directions.

The boundary is important. If the selected expert's output hurts the loss, the
sign of the scalar $s$ can reverse the update, so the winner may be pushed away
from $h$. Collapse therefore requires not just an early route advantage, but
also training feedback that does not immediately punish that advantage strongly
enough. In real models, both router rows and hidden states can move, so the
full phenomenon is a coupled geometry problem:

$$
\{w_e(t)\}_{e=1}^E
\quad\text{and}\quad
\{h_i(t)\}_{i=1}^N
$$

co-evolve during training.

### 2.6 Load Imbalance Is Not Feature Specialization

Observed load imbalance has multiple sources:

$$
\Delta_{\mathrm{load}}
= \Delta_{\mathrm{decision\ region}}
+ \Delta_{\mathrm{finite\ sample}}
+ \Delta_{\mathrm{router/hidden\ geometry}} .
$$

Therefore random routing and load imbalance are mechanism-audit objects, not
final specialization evidence. High-dimensional normalized random directions
lower the random floor; unequal row norms in Gaussian router initialization can
also produce imbalance. A specialization claim must jointly inspect feature
consistency, load, task loss, common-component scores, and functional utility.

## 3. Link To The Advisor's Scale-Free Representation Route

The advisor's scale-free representation route suggests a broader picture:
language reuses previously learned structures, while cross-entropy optimization
prefers high-gain directions. A high-gain direction is one with a large
singular value, so a small hidden-state movement along that direction produces
a large output or attention-score change.

For an output matrix

$$
W = U\Sigma V^\top,
$$

the loss decrease from a gradient step along hidden-side singular direction
$v_i$ is roughly:

$$
\Delta \mathcal{L}_i
\approx
-\eta \, \sigma_i^2 \, \langle u_i, p-y\rangle^2 .
$$

This means a direction is selected by optimization not merely because it looks
geometrically clean, but because it has large gain $\sigma_i$ and aligns with
the current prediction error.

For the MoE specialization line, this gives a clear role: expert partitions
should prevent all features from being forced through the same high-gain
subspace. Ideally, different features enter different experts, and each expert
forms a local subspace, reducing interference between common and rare features.

This also exposes the bottleneck: if the router collapses first, the expert
partition never forms. Therefore the current line first studies why routing
collapses and how a partition can be preserved, then uses the A07 line to test
whether the partition has value.

## 4. Evidence Chain

| Stage | Question | Main Result | Current Boundary |
| --- | --- | --- | --- |
| 05 common mechanism | Why do uniform features still prefer a few experts at step 0? | In $h_f=c+r_f$, the term $c$ creates implicit expert bias through $w_e^\top c$; common scores predict early dominant experts. | Explains the early seed; not a final solution. |
| 05/06 early training | Does step-0 bias get amplified by training? | Common control can improve early load, but ordinary training can still reconcentrate. | Initialization geometry and training feedback must be separated. |
| 06 positive control | If feature centers are known, can uniform features be evenly assigned? | In controlled data, feature-center initialization reaches feature consistency 1.0 and load imbalance 0. | Labeled positive control; not a label-free method. |
| 06 label-free discovery | Can pseudo-feature centers be found without feature labels? | In controlled data, residual clustering recovers pseudo-feature centers and enters a preservable partition. | Controlled setting; not natural text. |
| 06 real proxy features | Does real text contain evaluable proxy features? | Real hidden states contain stable proxy clusters; step-0 linear routing is possible. | Proxy clusters are not semantic features. |
| 06 real preservation failure | Does step-0 proxy routing survive early training? | Step-0 proxy NMI is about 0.75, but step-5/10 NMI becomes near-random. | Current bottleneck is training overwrite. |
| 06_17 sample-pool audit | Why does all-position clustering merge features? | Route-relevant positions recover features perfectly; all-position clustering mixes too many non-route states. | Needs a label-free route-relevant state selector. |
| 07 utility line | Does the partition reduce interference? | In controlled D07, common control reduces rare-feature loss under matched load and shows expert-function binding. | Controlled causal evidence only; not real-language transfer. |

## 5. Current Claim Boundary

### Claims That Are Supported

1. In controlled uniform-feature settings, collapse is not caused by feature
   absence or by feature partition impossibility.
2. The common component creates implicit expert bias through $w_e^\top c$ and
   is a strong explanation for early dominant experts.
3. Top-1 training can amplify early advantage into early lock-in.
4. Real text contains stable proxy features that can be linearly routed at
   step 0.
5. Ordinary real-text training overwrites this proxy partition, so
   preservation is the current bottleneck.
6. Controlled D07 evidence shows that a good partition can reduce rare-feature
   interference and bind route assignment to expert utility.

### Claims That Are Not Supported

1. Collapse is solved.
2. Uniform load is expert specialization.
3. Proxy features are natural-language semantic features.
4. The source of the common component is fully identified.
5. Common-component control is a deployable architecture.
6. Controlled D07 results transfer directly to real large language models.

## 6. How Results Should Be Presented

### 6.1 Main Metrics

| Metric | Question It Answers | Do Not Misread As |
| --- | --- | --- |
| Feature or proxy-feature consistency | Does the same feature enter the same expert? | Expert utility by itself. |
| Maximum load or load imbalance | Are a few experts absorbing most tokens? | Feature alignment. |
| Task loss or accuracy | Does the model still learn the task? | Routing specialization. |
| Common-component advantage | Is step-0 routing dominated by $w_e^\top c$? | Final performance. |
| Step-0/5/10 trajectory | Does the partition survive early training? | A complete training solution. |
| Expert ablation utility | Is the selected expert functionally useful? | Meaningful without preserved routing. |

### 6.2 Suggested Figures

1. **Mechanism diagram.** Show $h_f=c+r_f$ and how $w_e^\top c$ becomes an
   implicit expert bias.
2. **Stage-contract diagram.** Feature exists $\rightarrow$ step-0 routing
   $\rightarrow$ step-5/10 preservation $\rightarrow$ functional value.
3. **Early trajectory plot.** Feature consistency, max load, and common
   advantage at steps 0, 5, and 10.
4. **Value plot.** Rare-feature loss under dense, load-matched, common-control,
   and positive-control expert conditions.

## 7. Next Mechanism Step

### 7.1 Main Priority

The fastest mainline step is a real-text early-preservation / anti-feedback
protocol.

The question is not whether another method makes load look better. The question
is:

**Can the step-0 proxy feature partition survive the step-5/10 training window
without materially hurting language modeling loss?**

### 7.2 Rival Explanations Separated By This Protocol

| Rival Explanation | If True, We Should See | Decision Needed |
| --- | --- | --- |
| The proxy feature is unstable | Low cluster stability and weak step-0 routing | Existing evidence weakens this as the first failure point. |
| The linear bridge is too weak | Low step-0 proxy consistency | Existing evidence shows the step-0 bridge passes. |
| Ordinary training feedback overwrites the partition | Strong step-0 partition, collapse by steps 5/10, normal loss decrease | This is the current leading explanation. |
| Load balance alone is enough | Improved load also preserves proxy consistency | If load improves but proxy consistency does not, this fails. |
| Common component is the main driver | Common control improves step-5/10 consistency | Supported only if loss stays acceptable. |

### 7.3 Minimal Protocol Sketch

Fix real-text data, the small top-1 MoE model, the step-0 proxy centers, and
the training budget.

Candidate variants are mechanism interventions, not a method competition:

1. **Ordinary training baseline.** Reproduce strong step-0 routing and step-5/10
   collapse.
2. **Router common-logit cancellation.** Experts still consume the full hidden
   state; router logits subtract the bias induced by the common component.
3. **Common-controlled router input.** Experts consume the full hidden state,
   while the router sees a common-controlled representation.
4. **Early anti-lock-in.** Use softened routing or load constraints only in the
   step-0 to step-10 window, then return to ordinary training.
5. **Positive preservation control.** Use fixed or slow-updated proxy centers as
   an upper bound, not as a deployable method.

### 7.4 Success And Failure Criteria

Success is not better-looking load. Success requires:

- step-10 proxy-feature consistency is clearly above the random baseline;
- max load is not excessively concentrated;
- language modeling loss does not materially worsen;
- early common-component advantage decreases or is explicitly explained;
- the result is stable across the same seed set used by the baseline.

Failure is also informative:

- If load improves but proxy consistency does not, the intervention is load
  control rather than feature preservation.
- If consistency improves but loss worsens, the intervention damages predictive
  learning.
- If step-5 improves but step-10 fails, the anti-lock-in window is too short or
  expert-function co-adaptation still overwrites the partition.
- If the positive control fails, the proxy feature may be incompatible with the
  real training objective.

## 8. How To Extract Mechanism Like The Advisor

For every result, do not first ask what the next method is. Fill in five lines:

| Field | Question |
| --- | --- |
| Observation | What was directly measured? Use numbers and figures only. |
| Interpretation | Which mechanism term does the observation support? |
| Rival explanation | Which rival explanation is ruled out, and which remains open? |
| Claim boundary | How far can the claim move? |
| Next decision | What is the next single uncertainty to adjudicate? |

Example:

| Field | Content |
| --- | --- |
| Observation | Real-text proxy consistency is about 0.75 at step 0, near-random by steps 5/10, and loss does not crash. |
| Interpretation | Proxy discovery and step-0 linear routing are not the first failed stage; training feedback overwrite is the bottleneck. |
| Rival explanation | Weakens "there is no routable proxy feature"; does not rule out "the proxy has no functional value." |
| Claim boundary | The pipeline fails at preservation; this does not prove real expert specialization is impossible. |
| Next decision | Test whether early anti-feedback preserves the proxy partition. |

This template prevents two common mistakes:

1. treating debug figures as core evidence;
2. treating load improvement as expert specialization.

## 9. Core Meeting Sentence

The common component explains why uniform features can still produce a dominant
expert at step 0; early lock-in explains why this advantage can be amplified by
training; the stage contract explains why the real-text bottleneck is not proxy
feature discovery but preservation; and the A07 line explains why this
partition is worth preserving, because in a controlled setting it reduces
rare-feature interference and creates expert utility.
