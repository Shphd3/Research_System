# A15_13_11: Does Structural Routing Support Bounded Incremental Learning?

## 1. Problem Definition

The decision question is whether the lower-decay structural Router produces a
functional organization that justifies a bounded local adaptation or growth
policy when tasks arrive after the initial adapter-training phase. A6R1 trained
the Router and eight low-rank experts jointly on all eight tasks; its best mean
arm, GMM-B, improved average internal loss but reversed sign at seed 43. That
result is enough to select a fixed diagnostic candidate, not enough to claim a
stable method advantage.

This Anchor therefore separates two objects. A *post-training mechanism audit*
tests whether the completed A6R1 checkpoints changed actual routes, expert
function, and local learning compatibility. A *sequential-task test* starts
again from the original adapter initialization, trains on six tasks, and then
reveals two held-out tasks in a fixed order. The smallest direction-changing
decision is whether a policy that can reuse or add local capacity improves the
new-task versus retained-task tradeoff beyond matched fixed-capacity adaptation.
It does not ask whether the frozen language-model backbone has never seen the
underlying knowledge.

Pass would justify testing the bounded policy on a longer and independent task
stream. Fail would retain fixed-capacity adaptation and stop capacity-growth
claims. Invalid parity, future-task leakage, unsupported groups, or intervals
that cross the registered decision regions are Insufficient.

## 2. Physical Priors

The researcher-confirmed prior is that examples which require incompatible
future updates should not be forced to share exactly the same writable expert
parameters. If the frozen GMM relation reaches actual routes and expert
functions, a local correction selected without future-task identity may
improve a newly arriving task while preserving old-task outputs better than
updating the same old capacity. The exposing variables are the cross-group
transfer matrix and the sequential new-task gain under a registered old-task
damage constraint.

This prior is false in the tested setting if experts are functionally
interchangeable, local updates transfer beneficially, a Router or old-expert
update reaches the same frontier, or a growth policy improves new loss only by
damaging retained tasks. A changed route distribution alone does not expose
the prior.

## 3. Falsifiable Hypotheses

The primary hypothesis is that GMM-B's permutation-invariant relation
regularization creates a useful learning partition: after six-task training,
its data-driven adaptation policy has larger held-out new-task gain than its
best fixed-capacity policy, and the growth-specific increment over fixed
capacity is larger than the same increment for task-only training. Each gain
must satisfy the old-task retention constraint.

The strongest rival is that task gradients already organize all useful
capacity. Under this rival, routing or expert diagnostics may differ, but
Router and old-expert adaptation matches or exceeds local correction, or any
apparent growth gain is reproduced by task-only training. A second live rival
is generic extra capacity: an input-gated correction cannot be credited when a
constant-gated correction reaches the same gain-damage frontier.

Pass requires an all-seed directional growth-specific advantage above the
registered practical threshold for at least one later task at no more than 16
unique support records, with retained-task damage within tolerance and no
permanent growth on the old-only or mixture-shift controls. Fail is the
registered opposite: fixed capacity matches or wins, the sign reverses, the
retention constraint fails, or the automatic policy cannot distinguish true
arrival from both controls. Other valid but nonseparating outcomes are
Insufficient for the structural-growth hypothesis and remain reportable.

## 4. Mathematical Model

For final-layer MLP pre-input state \(h_t\), the Router produces
\(p_t=\operatorname{softmax}(Wh_t+c)\) and selects
\(k_t=\arg\max_e[(Wh_t+c)_e+b_e]\), where \(b\) is the frozen load-balancing bias
during post-training adaptation. The deployed expert contribution is
\(p_{t,k_t}E_{k_t}(h_t)\); route identity and its probability coefficient are
not interchangeable.

For a treatment \(m\), later task \(j\), seed \(s\), and support size \(n\), define

\[
G^{new}_{m,j,s,n}=L^{new}_{K,j,s,n}-L^{new}_{m,j,s,n},\qquad
D^{old}_{m,j,s,n}=L^{old}_{m,j,s,n}-L^{old}_{K,j,s,n},
\]

in nat per answer token. \(K\) is the unchanged stage-start system. The best
eligible fixed-capacity treatment \(F^*\) is selected on development records
from Router-only, old-expert-only, and joint Router-plus-old-expert updates,
subject to the registered retained-loss constraint. The growth increment is

\[
I_{j,s,n}=G^{new}_{G^*,j,s,n}-G^{new}_{F^*,j,s,n},
\]

where \(G^*\) is the better eligible constant- or input-gated new rank-16
correction, also selected only on development records. The structural
difference-in-differences is

\[
I^{struct}_{j,s,n}=I^{gmm\_b}_{j,s,n}-I^{task\_only}_{j,s,n}.
\]

The practical threshold is \(\delta=0.001\) nat per answer token. These
quantities measure a bounded adaptation frontier; they cannot prove semantic
classes, universal capacity exhaustion, or long-horizon continual learning.

## 5. Computational Realization

The frozen Qwen3-0.6B-Base supplies layer-27 MLP pre-input states. Both lineages
start each seed from the same authenticated task-only update-zero Router,
shared rank-16 branch, and eight rank-16 experts. The task-only lineage uses
only answer-token loss. The GMM-B lineage additionally preserves pairwise
relations from a diagonal eight-component GMM fitted after PCA-64 on
training-only token states from the first six tasks. Neither GMM fitting nor
the six-task schedule may inspect the later HumanEval or MBPP task records.
The original SAE coverage rule is used only as the common causal-position mask
and does not fit to later tasks.

The eight real task IDs are sorted by
`SHA256("continual-v1|" + task_id)`: MMLU, MATH, GSM8K, GPQA, BBH, and
MMLU-Pro form stage 0; HumanEval and then MBPP arrive at stages 1 and 2. This
order is fixed independently of performance. Each later task uses nested
support sets of 1, 4, 16, and 64 unique training records; every size restores
the same stage-start state and performs 16 updates, recording checkpoints
0/1/4/8/16. A repeated record may provide many answer tokens, so record count,
token exposure, update count, and compute are reported separately.

Post-training S0--S5 uses all five A6R1/task-only conditions and all three
seeds for read-only stages, then the registered task-only/GMM-B subset for
short isolated copies. S6 uses task-only and GMM-B for seeds 17, 29, and 43.
Candidate actions are no update, Router-only update, routed-old-expert update,
joint Router-plus-old-expert update, a constant-gated rank-16 correction, and
an input-gated rank-16 correction. All receive the same target/replay records,
16 updates, token-normalized objective, and optimizer class. Old-only and
old-task-mixture-shift windows guard unnecessary permanent growth. The
automatic policy sees labeled answer loss in 32-record windows but never sees
task ID; two consecutive exceedances above the old-only 99th percentile only
open a support/validation comparison and do not force growth.

## 6. Minimal Falsification Tests

The decisive test is the S6 test-panel \(I^{struct}_{j,s,n}\) comparison for the
two fixed later tasks and four nested support sizes. The unit of observation is
a record and the independent training unit is seed. Loss is summed over answer
tokens, record-stratified bootstrap intervals preserve task identity, and seed
values are never replaced by bootstrap draws.

Primary Pass requires, for at least one later task with \(n\le16\): (i)
\(I^{struct}_{j,s,n}>\delta\) in all three seeds; (ii) each GMM-B growth treatment
has a 95% retained-task damage upper bound at most \(0.001\) nat/token; (iii) the
input-gated treatment improves the registered new/old frontier over the
constant-gated and fixed-capacity treatments; and (iv) the automatic policy
permanently grows on neither old-only nor mixture-shift control stream. A valid
one-record result is separately named one-record adaptation only when its
held-out new-task gain is above \(\delta\) in all three seeds; results at larger
\(n\) cannot supply that label.

Primary Fail is any all-seed fixed-capacity match or advantage under the same
retention constraint, any seed sign reversal in the claimed structural
increment, retention-bound failure, or systematic unnecessary growth on a
control stream. Insufficient covers a leaked teacher, invalid checkpoint,
failed no-op parity, fewer than the frozen support/probe minimum, no automatic
trigger, or a confidence interval crossing the decision region. A no-trigger
result is a failure of the automatic detector but does not invalidate the
known-boundary adaptation comparison.

## 7. Current Evidence

A6 with constant structural coefficient `0.1` completed twelve trajectories
and was worse than matched task-only in every seed. A6R1 changed only the
coefficient to a linear `0.01` to `0.001` decay and completed twelve more
trajectories. GMM-B had mean test NLL `0.694560` versus task-only `0.696578`,
with paired differences `-0.003897`, `-0.002480`, and `+0.000322` nat/token.
The sign reversal rejects an all-seed task-loss advantage but leaves a bounded
mechanism question worth auditing. No A6R1 S0--S6 result exists at Anchor
freeze time.

**Added 2026-09-10 (representation side, status `DERIVED_NOT_SCIENTIFIC_VERDICT`).**
The E20 v2 matrix (14 conditions x 3 seeds x 512 updates) was read on the frozen
development panel without retraining. Three observations are eligible as bounded
descriptions, not as mechanism: (i) under the open-attention conditions the
full-dimension cosine relation matrix of the router input \(h\) drifts by a small,
monotone amount, \(R(0,512)\approx0.038\)--\(0.045\), with the equal-span local rate
falling by roughly a factor of eight between the early and late windows; (ii) under
the fixed \(t_0\) partition both the within-group and between-group spreads rise,
with the between-group term rising faster, so the pre-registered direction
"within-class tightening" is rejected on this readout; (iii) the fixed \(K=8\)
membership change across checkpoints is not larger than the change produced by
re-running the same clustering on the identical \(h\) with a different solver seed,
so that readout cannot separate training change from analysis noise. A frozen
attention control (\(h\) bitwise constant) returns exactly zero drift and exact
agreement, which qualifies the pipeline. The strong boundary in Section 8 is
unchanged: none of this establishes semantic category formation, expert utility, or
a task benefit.

## 7b. Registered Follow-Up Design (E21, executed 2026-09-10)

`experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E21_dynamic_structural_teacher/protocol.md`
registers the second-round contrast that Section 8's mechanism question needs:
two new conditions, `dynamic_sae_b_u` and `dynamic_gmm_b_u`, re-derive the router
relation teacher from the current \(h\) at updates {32, 64, 128, 256} (SAE warm
start; GMM refit), while `task_u`, `sae_b_u` and `gmm_b_u` serve as untrained
controls. Everything else is inherited from the E20 matrix contract; the teacher
\(q\) is produced under `no_grad` from a detached \(h\) and the structural gradient
still reaches only the Router. The design was frozen before submission and its
pilot gate (dictionary reproducibility, gradient isolation, main-model invariance)
must pass before any arm comparison is read.

**E21 result (2026-09-10, `DERIVED_NOT_SCIENTIFIC_VERDICT`).** The pilot gate passed
(dictionary update cannot touch the main model; structural gradient reaches only the
Router; the frozen-attention control stays exact). Refreshing the teacher does change
it -- the record-pair relation of the teacher moves 0.273 (SAE) / 0.096 (GMM), which is
about 5x / 2x the same-`h` re-fit noise (0.056 / 0.049) -- and that change does reach the
Router. It does **not** reach the representation: the same-seed paired difference in
\(R(0,512)\) is at most 0.002 against arm values of 0.048--0.052 (about 4%), with mixed
signs for the SAE arm and a consistently but negligibly smaller drift for the GMM arm;
no stable task-loss difference survives the seed scatter of roughly 0.14 nat. Bounded
reading: under the "last attention open, structural gradient router-only" contract, the
teacher's *time semantics* (frozen versus refreshed) is not an effective knob on the
representation trajectory. This does not weaken the earlier finding that adding a
teacher at all changes the trajectory relative to task-only, and it says nothing about
semantic category formation or expert utility.



## 8. Claim Boundary And Next Decision

Current evidence supports lower structural pressure as a partial task-loss
recovery and rejects a stable all-seed GMM-B advantage. It does not yet support
functional expert specialization, update incompatibility, local growth, rapid
adaptation, or automatic continual learning. The post-training audit may
localize where the chain fails without rescuing the task-loss claim.

The one next decision is whether the bounded GMM-B local policy passes the
registered sequential-task difference-in-differences and retention guards
against task-only and fixed-capacity controls. Completion requires eligible
S0--S5 artifacts, the full S6 task/support/seed matrix or typed decision stops,
all control-stream trigger records, and an auditable cost ledger. On Pass,
resume by designing one longer independent task stream. On Fail, retain
fixed-capacity adaptation and stop local-growth promotion. On Insufficient,
repair only the named validity or measurement gap before reopening the same
decision.
