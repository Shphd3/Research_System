# A15_13_10: Can Initial SAE/GMM Structure Improve Online Expert Routing?

## 1. Problem Definition

The decision question is whether a frozen initial eight-group structure from a
sparse autoencoder (SAE) or token-level Gaussian mixture model (GMM) improves
answer prediction when the Router and low-rank experts learn jointly, compared
with an otherwise matched task-only Router. Completed A6 showed that a constant
structural coefficient of `0.1` made every tested arm worse than task-only in
all three seeds. The researcher-selected next test asks whether lower early
pressure that decays during training restores task adaptation. Missing,
invalid, or sign-reversing trajectories are insufficient evidence. This anchor
does not select a Transformer layer, expert count, or external benchmark winner.

## 2. Physical Priors

The researcher-confirmed prior is that initial grouping can bias different
feature or state profiles toward distinguishable routes while task gradients
remain free to adapt the Router and experts. The observable consequence is a
stable reduction in answer-token loss relative to matched task-only training.
The strongest rival is that ordinary task gradients already provide all useful
routing adaptation, or that preserving initial structure obstructs task
learning. A routing-pattern change alone cannot separate these explanations.

## 3. Falsifiable Hypotheses

The primary hypothesis predicts that at least one combination of SAE/GMM
teacher and fixed-ID/pairwise regularization has lower final internal-test
answer loss than task-only in all three matched seeds. Teacher-matched A-versus-B
comparisons test whether explicit expert-ID alignment or permutation-invariant
relations better preserve useful structure; scheme-matched SAE-versus-GMM
comparisons test which teacher construction works better under that constraint.
The rival predicts no cross-seed stable task benefit or a consistent loss
increase. Without a random structural teacher, a positive result cannot show
that semantic rather than generic regularization is uniquely necessary.

## 4. Mathematical Model

For final-layer MLP pre-input state $h_t$, the trainable Router produces
$p_t=\operatorname{softmax}(W h_t+c)$. A frozen teacher produces an eight-way
profile $q_t$ on causal answer-prediction positions with retained SAE mass. The
A6R1 follow-up minimizes

$$
L_u=L_{\mathrm{task}}+\lambda_uR,\qquad
\lambda_u=0.01+\frac{u-1}{511}(0.001-0.01),\quad u=1,\ldots,512,
$$

where $L_{\mathrm{task}}$ is total answer-token cross entropy divided by all
answer tokens in the effective batch. Scheme A sets $R$ to the token-weighted
$D_{KL}(q_t\Vert p_t)$ mean and therefore aligns teacher and expert IDs.
Scheme B attracts Router distributions for teacher-similar token pairs and
repels teacher-dissimilar pairs up to a fixed distance margin, so a global
expert-ID permutation leaves it unchanged. The structural term updates only
$W,c$ directly; task loss also reaches the Router through the unrenormalized
selected-expert probability. The discrete selected index itself has no
gradient.

## 5. Computational Realization

The frozen Qwen3-0.6B-Base supplies zero-indexed layer-27 MLP pre-input states.
The model retains one shared rank-16 branch, eight rank-16 experts, hard Top-1
selection, and a nonparameter count-based balancing bias. The backbone,
language head, SAE, SAE feature groups, and GMM teacher remain frozen. All four
A6R1 conditions load each seed's exact task-only update-zero adapter/Router
state and sample schedule, then initialize fresh optimizer state. They do not
resume completed A6 checkpoints.

The SAE teacher sums Top-32 nonnegative activations inside each retained feature
group and normalizes the eight group masses. The GMM teacher is fitted once on
training-only Router-subset token states after PCA-64 and returns frozen soft
posteriors; development and test states cannot enter teacher fitting. Both
teachers use the same SAE-coverage mask. Evaluation removes the structural
term, freezes balancing bias, and reports ordinary answer loss. Exact run-level
settings and stop rules are owned by the approved [A6R1 Protocol](/Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E20_sae_flat_router_eight_task_mixed_training/A6R1_online_regularized_router_decay/protocol.md).

## 6. Minimal Falsification Tests

The decisive quantity for each new condition and seed is
$\Delta=\operatorname{NLL}_{\mathrm{new}}-\operatorname{NLL}_{\mathrm{task-only}}$
on all matched internal-test answer tokens; lower is better. All three negative
deltas constitute a directionally consistent advantage under the registered
configuration. Any positive delta rejects an all-seed advantage, any sign
reversal means no stable ordering, and an invalid trajectory or failed baseline
equivalence makes the comparison incomplete. Teacher and constraint contrasts
use the same per-seed rule. These descriptive three-seed rules are not a
population significance test or an optimum-method claim.

Necessary guards are exact initialization and schedule reuse, training-only
teacher construction, causal position and common-mask alignment, effective-
batch normalization, nonzero structural Router gradients, post-initial-update
task Router gradients, frozen teachers/backbone, and complete fixed-checkpoint
evaluation. Lower structural loss alone cannot rescue worse task NLL.

## 7. Current Evidence

The completed A5 experiment found that task-only routing had the lowest mean
internal-test NLL, while its SAE/GMM Routers were frozen during expert training.
That result supports ordinary online Router adaptation as a strong baseline but
does not test matched online structural regularization. Its complete evidence
is recorded in the [A5 Summary](/Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E20_sae_flat_router_eight_task_mixed_training/A5_balanced_h/summary.md).
A6 then completed 12/12 registered trajectories and full internal evaluation.
All four constant-`0.1` online regularization conditions were worse than
task-only in every matched seed. The best new arm, SAE-B, had mean test NLL
`0.702514` versus task-only `0.696579`, a paired mean increase of `0.005936`
nats/token. This establishes the bounded task-loss failure, not its cause.

## 8. Claim Boundary And Next Decision

Current evidence supports task-only as the strongest inherited internal-loss
baseline and rejects an all-seed benefit for the tested constant-`0.1` A6
configuration. The researcher judges excessive structural pressure to be the
next explanation to test; this causal interpretation remains unconfirmed.
A6R1 changes only the coefficient schedule and can test whether loss recovers;
it cannot establish true semantic classes, causal feature disentanglement,
intervention-tested expert utility, external benchmark generalization, or
broad SAE/GMM superiority.

The one next decision is whether any lower, linearly decayed A6R1 arm both
improves over its old A6 counterpart and shows an all-seed directional
task-loss advantage over task-only. Completion requires twelve valid update-512
trajectories, complete internal tests, authenticated reuse of three task-only
baselines, and matched old-A6 contrasts. Resume from the approved A6R1
Protocol. After submission, stop for researcher review before post-training
S0--S6.
