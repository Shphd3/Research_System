# A15_11: Counterfactual-Utility-Separable Residual Expert Growth

Thinking Card source: [15_11_gradient_consistent_hierarchical_routing_thinking_card_cn.md](15_11_gradient_consistent_hierarchical_routing_thinking_card_cn.md)

## 1. Problem Definition

The sole decision question is:

> When a rank-one common function is learned and frozen, does training a
> $1\rightarrow2\rightarrow4$ MoE only on its unexplained functional residual
> make the counterfactually useful expert linearly accessible inside each
> branch and improve sample efficiency over a matched flat nonlinear MoE only
> when the provided parent grouping agrees with expert utility; and does direct
> counterfactual-utility supervision add value beyond task loss alone?

Four claims are deliberately non-equivalent:

1. **semantic separability:** an externally named label is recoverable from a
   named representation under a named held-out readout;
2. **utility separability:** the equal-compute counterfactual expert ranking is
   recoverable from that representation;
3. **Router use:** the deployed Gate ranks and selects the useful action;
4. **functional benefit:** that action reduces held-out task loss or exposure
   to a fixed loss.

The Qwen audit measures only the first claim along the native Router interface.
The synthetic experiment supplies exact utility and functional objects and can
test the remaining arrows in a controlled setting.

## 2. Physical Priors

The 2026-08-24 advisor intuition has a concrete operational core: train one
low-rank common expert; freeze it; add two different low-rank specialists; make
them learn only what the common expert does not explain; freeze; then add four
leaf experts and repeat. Routing must use residual variation rather than the
common output itself. The meeting did not specify the exact common object,
projection operator, discovery rule, freeze time, or utility target. Those are
AI operationalizations and not attributed to the advisor.

The retained prior is conditional. Progressive residual growth helps only if
the residual functions grouped at a node admit the node's low-rank capacity.
Frequency and semantic labels do not guarantee this. Direct utility
supervision may shorten Router credit assignment, but cannot overcome a wrong
structural mask or an insufficient expert rank.

The 2026-08-28 meeting adds a second boundary: maximum variance is not maximum
discriminability, and a two-dimensional PCA plot cannot adjudicate high-
dimensional separability. The present work therefore measures held-out
readout, Gate access, counterfactual regret, and functional error separately.

## 3. Falsifiable Hypotheses

**H1 — native accessibility boundary.** In frozen Qwen3-30B-A3B, parent-label
accessibility may be retained or lost at either the native Gate projection or
top-eight selection. The five fixed confirmation blocks and two expression
panels must produce one typed profile; this profile cannot establish expert
utility.

**H2 — residual-tree mechanism.** In a balanced work generator whose teacher
decomposes as common plus parent plus child rank-one functions, the advisor
tree realizes low held-out error. A permutation-equivalent fail generator
places two orthogonal residual functions behind each fixed parent leaf and
therefore imposes an exact rank-one approximation floor.

**H3 — utility-supervision effect.** Within the same Router architecture,
counterfactual-utility cross entropy reduces normalized-MSE learning-curve
area relative to task-only routing without worsening the endpoint.

**H4 — hierarchy-specific effect.** Under the same counterfactual-utility
supervision, the conditional tree outperforms a parameter- and compute-matched
flat nonlinear Router in the aligned work condition. If the flat Router
matches it, utility supervision or generic nonlinearity is sufficient and the
hierarchy claim fails.

The strongest rivals are finite-sample regularization, extra pseudo-
supervision, generic nonlinear interaction learning, load imbalance, expert
estimation failure, and implementation leakage through rank, mask, or frozen
parameters.

## 4. Mathematical Model

### 4.1 Separability is a four-object statement

For label $Y$, representation $R$, readout family $\mathcal F$, and
generalization split $\mathcal S$, “linearly separable” abbreviates a statement
about

$$
(Y,R,\mathcal F_{linear},\mathcal S).
$$

Changing a semantic label to a native route ID or a counterfactual-best expert
changes the scientific object. Predicting a route ID from the input of the
linear Gate that created it is nearly circular; predicting a utility ranking
is not.

At fixed layer, checkpoint, token, and equal-compute action set, let
$C_i(a)$ be task cost. Relative to current action $a_0$, define

$$
U_i(a\leftarrow a_0)=C_i(a_0)-C_i(a).
$$

Utility separability concerns $\arg\max_a U_i(a)$ or the pairwise utility
ordering. There is no general implication

$$
\text{semantic separability}
\centernot\Rightarrow
\text{utility separability}
\centernot\Rightarrow
\text{native Router use}.
$$

Identical experts give perfect semantic separability but tied utility. Experts
specialized by difficulty rather than topic give utility structure without the
registered semantic taxonomy.

### 4.2 A fixed linear map cannot create linear separability

Let $z=Ax+c$. If transformed samples admit

$$
y_i(w^\top z_i+b)>0,
$$

then

$$
y_i((A^\top w)^\top x_i+w^\top c+b)>0
$$

already separates the original samples. Thus the transformed linear function
class is a subset of the original one. A full-column-rank map preserves linear
separability; a rank-deficient map can preserve or destroy existing separating
directions but cannot create one. A held-out improvement after linear
projection can arise from finite-sample regularization, denoising, conditioning,
or optimization bias, not new linear information.

Unconstrained raw margin is also non-identifying: scaling $A$ scales numerical
margin. Comparisons require normalized features and classifiers or an explicit
metric. The registered audits use balanced accuracy, negative log likelihood,
and a normalized fifth-percentile score margin.

### 4.3 X-MoE cosine normalization preserves linear pairwise boundaries

For X-MoE-style scores

$$
s_e(h)=\frac{(Wh)^\top e_e}{\|Wh\|\|e_e\|},
$$

the token denominator is common to every expert. With
$\bar e_e=e_e/\|e_e\|$,

$$
\operatorname{TopK}_e s_e(h)
=
\operatorname{TopK}_e h^\top W^\top\bar e_e.
$$

Every pairwise selection boundary remains a hyperplane. X-MoE can change the
Router-visible row space, remove expert-norm competition, change score scale,
and constrain routing gradients; cosine normalization alone does not make an
individual score or pairwise boundary nonlinear and does not guarantee the
target interaction or hierarchy. Several linear selection cells can still be
recombined through expert outputs into a non-convex task region, so this is not
a claim that the overall multi-expert function class is linear or cannot
represent XOR. The Qwen audit therefore borrows the row-space/accessibility
question rather than treating X-MoE's UMAP or collapse score as semantic
evidence. The source is Chi et al., *On the Representation Collapse of Sparse
Mixture of Experts*, NeurIPS 2022.

### 4.4 Nonlinear and conditional maps can expose an interaction

For independent $p,b\in\{-1,+1\}$ and $q=pb$, both $p$ and $q$ are affine-
linearly separable from $s=(p,q)$, while $b=pq$ is XOR and is not. Conditional
on $p$, however, $b=pq$ is a one-dimensional linear decision in $q$.
Therefore a parent-first conditional map can expose the interaction, and a
generic nonlinear flat map can also learn it. The latter is the decisive rival.

### 4.5 Hard common-subspace deletion has an additional assumption

Let $\mathcal C$ be the frozen common operator subspace and let $\Delta$ be a
useful residual operator. Restricting all later experts to
$\mathcal C^\perp$ leaves the isotropic-input approximation floor

$$
\min_{W\in\mathcal C^\perp}
\mathbb E\|(\Delta-W)z\|_2^2
=
\|P_{\mathcal C}\Delta\|_F^2.
$$

Thus hard removal is safe only for the component of useful residual function
orthogonal to the frozen span. Functional residualization
$r=y-\widehat y_{frozen}$ is distinct: it removes explained output while not,
by itself, forbidding later reuse of the same parameter direction. E03 tests
the orthogonal work case; it does not establish safety for non-orthogonal real
tasks.

### 4.6 Exact work/fail theorem

Choose doubly orthogonal rank-one $8\times8$ matrices $C,A,B$ with unit
Frobenius norm. Define

$$
\Theta^{work}_{p,b}=C+pA+bB,
\qquad
\Theta^{fail}_{p,b}=C+qA+bB.
$$

The mapping $(p,b)\leftrightarrow(q,b)$ is bijective, so work and fail have the
same teacher-function multiset, frequencies, noise, and mean signal energy.
After removing $C$, parent coherence is $1/2$ in work and zero in fail; the
$q$-grouping reverses those values.

The fixed $p$-first tree has the exact work decomposition
$C+pA+bB$. In fail, its level-one conditional mean is zero and each leaf must
fit $qA+bB=b(pA+B)$. This operator has two equal nonzero singular values.
The Eckart--Young theorem gives one unit of unavoidable rank-one error, hence

$$
NMSE^{oracle}_{H,fail}=\frac13.
$$

This floor is structural. Better Gate optimization and counterfactual utility
supervision cannot remove it without changing the tree, mask, or expert rank.

## 5. Computational Realization

### E01 — frozen Qwen native accessibility

At each registered block, let $H_\ell\in\mathbb R^{2048}$ be the exact BF16-
quantized native MoE input, $W_{g,\ell}\in\mathbb R^{128\times2048}$ the frozen
bias-free Gate, $Z_\ell=W_{g,\ell}H_\ell$, and $Q_\ell$ its renormalized top-8
route. C4 and C5 are separate panels. Complete template families A and B are
exchanged for held-out readout. Blocks 4/12/20/28/36 confirm; visible Block 44
is pilot only. Matching family-level bootstrap and label permutation preserve
the independence unit.

This experiment locates parent-label access loss along $H\rightarrow Z\rightarrow
Q$. Because $W_gH^\perp=0$ for the Gate-null component, the $H\rightarrow Z$
comparison is also an operational Router-row-space visibility audit. It does
not execute alternative experts and cannot measure utility.

### E03 — progressive residual MoE

E03 uses a single common expert, two level-one experts, and four level-two
experts. All are rank-one matrices; completed stages are frozen; new experts
fit the unexplained function residual; every inference activates three
experts. The same seven experts, initialization, batches, step budgets, hard
top-one estimator, candidate forward ledger, Router parameter count, and
inference compute are used in a $2\times2$:

| | task-only Router | counterfactual-utility Router |
| --- | --- | --- |
| fixed $p$-conditional tree | `H_task` | `H_util` |
| flat nonlinear Router | `F_task` | `F_util` |

For residual $r_i$ and candidate $e$,

$$
U_{ie}=\|r_i\|_2^2-\|r_i-W_ez_i\|_2^2.
$$

The utility arms distill the stop-gradient best candidate. Task-only arms
compute the same ledger with zero utility-loss weight. This matches candidate
compute but not supervision; within-architecture contrasts identify the
supervision effect, while `H_util` versus `F_util` identifies any additional
tree effect.

The primary metric is noise-free NMSE area under the learning curve over log
cumulative examples. Endpoint NMSE, utility regret, route agreement, normalized
low-tail margin, load, numerical rank, frozen hashes, projection leakage,
stored/active parameters, and training/inference FLOPs are guards or secondary
diagnostics.

The owning E01/E03 Protocols run only on one SPOT worker exposing exactly eight
RTX 5090 GPUs; H100 and automatic fallback are prohibited by that execution
contract. The separately frozen E01H/E03H successor Protocols use one reserved
worker with exactly four H100 GPUs and preserve the estimands under collision-
isolated provenance. They are sensitivity evidence, not a resource fallback or
execution of the owning Focus, and the Qwen and synthetic verdicts remain
scientifically separate in both lanes.

## 6. Minimal Falsification Tests

E01 returns one frozen accessibility profile. Invalid hashes, BF16/FP32 verdict
disagreement, an invalid cross-fit cell, or hidden accessibility below its
matched max-layer null makes it Insufficient. No descriptive plot, NLL result,
or pilot layer can rescue the line verdict.

E03 first verifies exact generator, oracle, rank, mask, freeze, pairing, load,
parameter, FLOP, and completion identities. The main falsifier is the
permutation-equivalent fail condition: a fixed parent-first rank-one tree must
retain its $1/3$ oracle floor. A value materially below this floor is evidence
of leakage, not a successful method.

`H_task` must realize low error in work and high error in fail before the
advisor mechanism is called implemented. Counterfactual utility is admitted
only by within-architecture AULC contrasts. Hierarchy gain under utility is
admitted only if `H_util` beats `F_util` in work with a positive paired lower
bound and no endpoint disadvantage. Eight paired optimizer seeds bound this
execution; they are not a population sample.

## 7. Current Evidence

A15_09_E01 found stable but permutation-null-subordinate coarse--fine
discriminant geometry: corrected overlap was 0.0596--0.1445 and every raw
overlap was below its matched null median. A15_10_E01 found 0/6 registered
layers with bidirectional C4/C5 cross-parent fine-function transfer; eligible
relative retention was 0.0339--0.1810 and only 1/24 directional cells exceeded
the full-pipeline null. These results motivate a conditional mechanism but do
not prove it.

X-MoE supplies a low-dimensional cosine-routing and routing-gradient prior, not
a theorem that semantic or utility labels become nonlinearly separable. A16_01_01
already owns a frozen-expert counterfactual-regret distillation question. The
novel object here is stagewise expert formation and the relation between
utility separability and progressive residual structure; generic
“counterfactual routing” is not a novelty claim.

E01 is complete and eligible. At confirmation Blocks 4/12/20/28/36, parent
balanced accuracy is 0.9948--1.0000 from $H$, 0.9417--0.9984 from native Gate
logits $Z$, and 0.4047--0.5635 from top-eight sparse routes $Q$. Blocks
4/12/20/28 satisfy projection preservation, material selection loss, and
retained route association in both C4 and C5; Block 36 misses only the C4
projection criterion. The BF16 and FP32 paths agree on
`TOP8_SELECTION_BOTTLENECK_WITH_RETAINED_ASSOCIATION`. This establishes a
semantic-access interface profile, not expert utility.

E03 is complete and eligible over eight paired optimizer seeds. All exact
generator, oracle, rank, projection, freeze, mask, pairing, compute, and
completion guards pass. `H_task` reaches median endpoint NMSE
$2.30\times10^{-5}$ in work and 0.33698 in fail; the paired fail-minus-work
AULC contrast is 0.05406 with 95% interval [0.05220, 0.05537]. The fixed tree
therefore realizes the aligned decomposition and retains the analytic $1/3$
floor under the wrong grouping.

H3 and H4 are not supported. In work, the tree utility contrast is
$S_H=-0.03860$ with interval [-0.06842, -0.00685], and `H_util` ends at median
NMSE 0.41693 versus $2.30\times10^{-5}$ for `H_task`. The matched flat models
reach near-zero endpoints in work and fail; neither a utility effect nor a
hierarchy-specific advantage is established. The registered layered verdicts
are `MECHANISM_SUPPORTED`, `NO_UTILITY_EFFECT_TREE`,
`NO_UTILITY_EFFECT_FLAT`, `NO_TREE_ADVANTAGE_TASK_ONLY`,
`NO_TREE_ADVANTAGE_UNDER_UTILITY`, and
`GENERIC_NONLINEARITY_OR_UTILITY_SUFFICIENT`.

The observed utility-tree failure is accompanied by zero minimum leaf load,
negative native and hidden-probe low-tail margins, and median target balanced
accuracy 0.625. A bounded AI explanation is that instantaneous utility labels
depend on sampled content $z$ and evolving experts while the hierarchical
Router sees only $p$ or conditional $q$; the target is therefore not guaranteed
to be a function of the Router-visible representation during co-adaptation.
This explanation was not independently intervened on and remains a successor
hypothesis.

The researcher accepted the collision-isolated four-H100 E01H/E03H lane as
non-owning sensitivity evidence under the current Focus, not as execution of
the eight-RTX-5090 contract. E01H reproduced the accessibility profile
(`4/5` projection-preserved, `5/5` selection-loss, `5/5` retained-association,
`0/5` near-total-retention). E03H reproduced the structural verdict: work
`H_task` endpoint $1.9403\times10^{-5}$, fail endpoint 0.336926, and paired
fail-minus-work AULC $0.053155$ with 95% interval [0.050140, 0.054230]. It
again found no positive tree or utility-supervision gain. The H100 records are
[E01H Summary](/Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E01H_qwen_native_router_access_gap_h100/summary.md)
and [E03H Summary](/Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E03H_counterfactual_utility_residual_tree_h100/summary.md).

E02 remains only as a superseded pre-run design. Its simultaneous two-bank
model lacked $1\rightarrow2\rightarrow4$ growth, stage freezes, ancestor
residualization, and counterfactual utility.

## 8. Claim Boundary And Next Decision

This Anchor establishes a frozen parent-accessibility profile for one Qwen
checkpoint and a complete controlled mechanism verdict for one four-leaf
rank-one teacher system, with a qualitatively agreeing four-H100 sensitivity
lane. It establishes neither a utility-supervision gain nor a hierarchy
advantage over generic nonlinear routing. It cannot infer Qwen's pretraining
mechanism, native expert utility, autonomous semantic hierarchy discovery,
safe deletion of all common directions, real-language-model NLL benefit, or
failure of every alternative utility objective.

The researcher-confirmed sole next decision is upstream of another Router
repair: test whether parent-related prediction-event frequency is sufficient
to form a held-out parent-discriminant direction, or whether frequency must be
combined with non-cancelling cross-child gradient consistency. The minimal
successor is a frequency (high/low) by gradient-consistency (high/low) $2\times
2$ next-token-prediction design. It must hold total tokens, total target
positions, parent/child counts, vocabulary, templates, and label entropy fixed
and return gradient consistency, parent between-class energy, held-out
fifth-percentile normalized margin, and discriminant-subspace spectral
location. Completion means those four cells have a frozen constructible
contract and Pass/Fail/Insufficient rules; only then may a successor Protocol
be reviewed. This decision does not authorize implementation, execution, or a
Qwen Router intervention. The earlier Oracle/Search route and soft expected-
utility repair are parked rather than run in parallel.
