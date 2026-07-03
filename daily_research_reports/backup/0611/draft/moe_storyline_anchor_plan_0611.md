# 0611 MoE Collapse Paper Storyline + Next Anchors Plan

> Time context: 2026-06-11 16:20.  
> Immediate purpose: help align with the mentor's paper-building logic before writing the next anchors.  
> This document does **not** write the final anchors. It provides the reasoning scaffold for completing them.

---

## 0. Current Decision

The project should now be organized around one paper spine and two next anchors.

**Paper spine:**

> Sparse top-1 dot-product MoE can enter early routing collapse because hidden-state common components become expert-specific routing bias through random router projections. This mechanism can be audited in synthetic and real representation spaces, and it motivates common-aware / residual-aware router initialization.

**Next two anchors:**

1. **Anchor A — Real Representation Initialization Geometry Audit**  
   Ask whether real or semi-real hidden representations contain the same initialization-time common-logit bias that we identified in the synthetic setting.

2. **Anchor B — Label-Free Common-Aware Router Initialization**  
   Ask whether we can use real hidden representations to construct a label-free router initialization that reduces common-induced imbalance and improves feature/residual-aligned routing.

Do **not** merge these into one anchor. Anchor A asks whether the problem exists outside the toy setting. Anchor B asks whether we can design a method from that geometry.

---

## 1. Mentor's Real Thought Process

### 1.1 What the mentor is really asking

The mentor is not primarily asking for another toy ablation. He is asking:

> If this common-bias mechanism is real, can we turn it into a simple router initialization principle, verify it in real representation space, and show that it matters more as the number of experts increases?

His implicit chain is:

```text
common/shared representation exists
-> random dot-product router projects common direction differently for each expert
-> some experts become easy to route to, others become hard to reach
-> top-1 routing amplifies early accessibility differences
-> unused experts do not learn
-> this becomes more serious as expert count increases
-> therefore router initialization should account for representation / expert geometry
```

The key phrase in his mind is not only “common-logit cancellation works”. It is:

```text
random router initialization does not respect the geometry of the representation/expert space.
```

### 1.2 What he probably likes in the current result

He likely likes these points:

- The phenomenon is simple and fundamental: common/shared directions can dominate routing before the router uses discriminative differences.
- There is a clear mathematical object: `w_e^T c`.
- The intervention is simple: remove/equalize common projection or initialize away from common bias.
- It naturally suggests scaling stress tests with more experts.
- It has a possible practical implication: better router initialization.

### 1.3 What he likely thinks is missing

He likely thinks the current version is still missing:

- **Real representation evidence:** Does this happen in real hidden states, not just synthetic ABC?
- **Initialization method:** Can we define an elegant router initialization rule?
- **Scaling test:** Does the failure get worse as `num_experts` increases?
- **Mathematical explanation:** Can we prove or at least derive why common projection creates expert accessibility imbalance?

### 1.4 What he does not want as the main story

He probably does **not** want the paper to become:

```text
A long synthetic source audit about B residual identity.
```

B residual is useful as supporting mechanism evidence, but it is not the paper's main selling point.

---

## 2. Where Our Cautious Writing Logic Differs from the Mentor's Logic

### 2.1 Mentor's framing

The mentor's framing is ambitious and method-oriented:

```text
This is a fundamental initialization problem.
Make a router initialization method.
Show it avoids collapse as expert count scales.
Push an arXiv draft quickly.
```

### 2.2 Our cautious framing

Our cautious framing has been:

```text
We have a controlled mechanism in synthetic setting.
We cannot yet claim full LM transfer.
We cannot yet claim deployable method.
Load balance is not feature specialization.
Common-control is not yet stronger than load balance.
```

This caution is scientifically correct, but if overemphasized, it will make the mentor feel we are under-selling the core insight.

### 2.3 Alignment strategy

We should align with the mentor by changing the paper's **front-facing grain size**:

```text
Front-facing story:
Common-logit bias reveals a router initialization failure mode.
We propose common-aware initialization as the natural mathematical correction.
We verify the geometry in real representations and stress-test expert scaling.

Internal boundary:
We do not claim full LM MoE is solved.
We do not claim load balance is unnecessary.
We do not claim causal expert functional specialization yet.
```

This lets us match the mentor's ambition without overclaiming.

---

## 3. Paper Storyline: Minimal arXiv Draft

### 3.1 Proposed title direction

```text
Common-Logit Bias Drives Early Routing Collapse in Sparse Top-1 MoE
```

Subtitle:

```text
A Mechanistic Study and Common-Aware Router Initialization
```

### 3.2 One-sentence thesis

```text
Even when discriminative features are represented and balanced, random dot-product top-1 routers can collapse because common hidden components induce expert-specific biases; this motivates common-aware router initialization and representation-space audits.
```

### 3.3 The paper should not claim

Do not claim:

```text
We solve MoE collapse.
We outperform load balance as an engineering replacement.
We prove feature specialization in full language models.
We scale to millions of experts in practice.
```

### 3.4 The paper can claim

Can claim, if the next anchors succeed:

```text
1. Common-logit bias is an early, predictive, intervention-relevant collapse mechanism in controlled top-1 dot-product MoE.
2. The same bias can be audited in frozen real/semi-real representation spaces.
3. Common-aware initialization reduces initialization-time route imbalance and can improve feature/residual-aligned routing.
4. Expert-count scaling increases the risk of extreme common-projection winners, making this an expert-scaling-relevant initialization issue.
```

---

## 4. How to Define “Feature” in Real Representation Space

### 4.1 Do not start with semantic philosophy

Do not ask:

```text
What is the true feature in a language model?
```

Use an operational definition:

```text
A feature is a controlled or measurable variation in hidden states that should be preserved by routing.
```

### 4.2 Three practical feature definitions

#### Option 1: Labeled controlled feature

Use semi-real prompts with known labels:

```text
relation type
question type
answer type
domain
template family
syntactic role
```

Then measure:

```text
feature_NMI
per-feature route purity
feature margin vs common margin
```

This is the best option for a first arXiv draft because it gives a clean metric.

#### Option 2: Residual cluster feature

If labels are unavailable:

```text
1. estimate common subspace C
2. remove common: h_res = P_perpC h
3. cluster h_res
4. evaluate whether routing preserves cluster identity
```

This supports “residual-structure-aligned routing”, not semantic feature specialization.

#### Option 3: Task-predictive feature

Train a linear probe on hidden states to predict a known target attribute. The feature is the target-predictive direction or class label.

This connects best to the synthetic slot setting.

### 4.3 Recommended for this week

Use Option 1 plus Option 2:

```text
primary: controlled labeled prompts
secondary: residual cluster audit
```

---

## 5. Anchor A — Real Representation Initialization Geometry Audit

### 5.1 Purpose

This anchor answers:

> Does the common-logit bias mechanism exist at initialization in real or semi-real hidden representation spaces?

This is the bridge from controlled toy mechanism to mentor's “真实表征空间” request.

### 5.2 Why this must be separate from the method anchor

If real representations do not show common-induced route imbalance, then initialization method is less motivated. So Anchor A is the validity gate for Anchor B.

### 5.3 Decision question

```text
In frozen real/semi-real hidden states, does random dot-product top-1 routing produce expert-specific common-logit bias that causes initialization-time route concentration, and does this risk increase with expert count?
```

### 5.4 What you should write in the anchor, section by section

#### Thinking Card

Write 3–5 lines:

```text
We know synthetic h decomposes into common + feature residual.
Now we test whether real/semi-real hidden states show the same router-side geometry at initialization.
This anchor does not test a new method yet; it audits whether the problem exists outside the toy setting.
```

#### Problem Definition

Write:

```text
Synthetic evidence is not enough for the paper claim.
The next decision is whether common-logit bias appears in frozen real representations under random router initialization.
```

Do not write:

```text
We test full LM MoE training.
```

#### Physical Prior

Use:

```text
Real hidden states contain large shared components: token identity, position/template, layernorm mean directions, domain/task common directions.
A random dot-product router can turn these shared components into expert-specific offsets.
```

#### Hypothesis

```text
Frozen hidden states can be decomposed as h_i = c + r_i.
Random router rows produce a_e = w_e^T c.
If common margin exceeds residual/feature margin, top-1 routing concentrates before any training.
```

#### Minimal Mathematical Model

Use one model only:

```math
z_{i,e} = w_e^T h_i = w_e^T c + w_e^T r_i
```

Define:

```text
common margin = top expert gap from w_e^T c
feature/residual margin = routing-relevant gap from w_e^T r_i
```

#### Minimal Tests

Test 1: Frozen random router audit

```text
input: hidden states H from real/semi-real model
router: random dot-product top-1, no training
measure: common margin, residual margin, max_load, entropy, active experts
```

Test 2: Expert-count scaling

```text
E = 4, 8, 16, 32, 64, 128
measure whether common winner / max_load worsens with E
```

Test 3: Common projection control

```text
compare random router on h vs P_perpC h
if route concentration drops after common removal, common geometry is implicated
```

#### Falsifiable Outcomes

Supported if:

```text
random router on real hidden states shows large common margin and route concentration;
common projection lowers route concentration;
expert-count scaling increases common-winner dominance.
```

Weakened if:

```text
common margin is not larger than residual/feature margin;
random routing is not concentrated;
common projection does not change routing.
```

Insufficient if:

```text
routing becomes more balanced but no feature/residual alignment metric exists.
```

#### Current Evidence

Write only synthetic current evidence:

```text
Synthetic common-logit is early and intervention-relevant.
Real representation evidence is not yet established.
```

#### Claim Boundary and Next Decision

```text
This anchor can only claim that the initialization-time geometry exists in real/semi-real representations.
It cannot claim a deployable initialization method or full MoE training improvement.
If supported, proceed to Anchor B: label-free common-aware initialization.
```

---

## 6. Anchor B — Label-Free Common-Aware Router Initialization

### 6.1 Purpose

This anchor answers:

> Can we construct a router initialization from hidden-state geometry, without slot labels, that reduces common-induced expert bias and improves feature/residual-aligned routing?

This directly aligns with the mentor's “router initialization method” direction.

### 6.2 Why this should be a second anchor

Anchor B depends on Anchor A. It is no longer asking “does the problem exist?” It asks “can we exploit the geometry to initialize better?”

### 6.3 Decision question

```text
Can a label-free common-aware initialization reduce or equalize w_e^T C in real/synthetic hidden spaces, improving initialization-time routing diversity and feature/residual alignment without using slot labels?
```

### 6.4 What you should write in the anchor, section by section

#### Thinking Card

```text
Synthetic results show slot-aware init can move routing into a specialization basin, but slot labels are unavailable in real settings.
This anchor tests label-free initialization from common/residual geometry.
The goal is not to beat load balance yet; the goal is to reduce common-bias-driven early route collapse.
```

#### Problem Definition

```text
Random router initialization ignores the hidden-state common subspace.
A better initialization should either equalize or remove common projection across experts.
```

#### Physical Prior

```text
Router should not assign traffic based on feature-independent common directions.
Router initialization should distribute experts across residual/unique variation rather than common variation.
```

#### Hypothesis

```text
If router rows are initialized in the common-orthogonal or residual-cluster subspace, then initialization-time common margin decreases and routing becomes less concentrated / more feature-aligned.
```

#### Minimal Mathematical Model

Use:

```math
H = C + R
```

```math
P_{\perp C} = I - C(C^T C)^{-1}C^T
```

Initialization options:

```math
w_e^{(0)} \leftarrow P_{\perp C} \xi_e
```

or common-equalized:

```math
w_e^T c \approx constant \quad \forall e
```

or residual-cluster:

```math
w_e^{(0)} \propto \mu_e(P_{\perp C}H)
```

#### Minimal Tests

Test 1: Synthetic label-free init

```text
baseline random init
oracle slot-init upper bound
common-orthogonal init
common-equalized init
residual-cluster init
oracle common-logit cancellation upper bound
```

Test 2: Real frozen init audit

```text
same initialization variants on real/semi-real hidden states
measure step-0 route concentration, common margin, feature/residual purity
```

Test 3: Small training sanity

```text
train only in synthetic setting first
optional: small real/semi-real MoE if time allows
```

Test 4: Load balance comparison

Use 2×2:

| | no common-aware init | common-aware init |
|---|---|---|
| no load balance | baseline | common init only |
| load balance | LB only | LB + common init |

Measure:

```text
max_load
active experts
feature_NMI / route purity
common margin
accuracy
```

#### Falsifiable Outcomes

Supported if:

```text
common-aware init lowers common margin;
it improves route diversity;
it improves feature/residual alignment at same or similar load;
LB + common-init improves alignment beyond LB alone.
```

Weakened if:

```text
common-aware init only improves max_load but not feature/residual alignment.
```

Failure if:

```text
common-aware init does not reduce common margin;
LB dominates both utilization and feature alignment;
method depends on oracle slot labels.
```

#### Current Evidence

Use:

```text
slot-init interpolation shows basin transition;
common cancellation improves slot_NMI;
no-attention-residual routing suggests common-source control improves routing but not perfectly.
```

#### Claim Boundary and Next Decision

```text
This anchor can support a mechanism-derived initialization principle.
It cannot claim full training stability unless persistent common-control is also tested.
If init-only helps early routing but final collapse returns, the next anchor should be persistent common-control / anti-lockin.
```

---

## 7. How to Compare with Load Balance

Do not frame it as:

```text
common-aware init beats load balance.
```

Frame it as:

```text
load balance controls how much traffic each expert receives;
common-aware init controls what information determines early assignment.
```

Use three types of metrics:

### Utilization metrics

```text
max_load
active experts
routing entropy
```

### Alignment metrics

```text
slot_NMI
feature_NMI
per-feature route purity
cluster-route mutual information
```

### Mechanism metrics

```text
common margin
residual/feature margin
common argmax predicts route winner
route lock-in step
```

The central comparison should be:

```text
At similar utilization, does common-aware initialization improve feature/residual alignment compared with load balance alone?
```

---

## 8. Mathematical Core for the Paper

### 8.1 Minimal derivation

Assume:

```math
h_i = c + r_i
```

Router score:

```math
z_{i,e} = w_e^T h_i = w_e^T c + w_e^T r_i
```

Define:

```math
a_e = w_e^T c
```

Then:

```text
a_e is feature-independent but expert-specific.
```

This is the key mathematical insight.

### 8.2 Scaling intuition

If:

```math
w_e \sim \mathcal{N}(0, \sigma^2 I)
```

then:

```math
a_e = w_e^T c \sim \mathcal{N}(0, \sigma^2 \|c\|^2)
```

As expert count `E` increases, the maximum common projection across experts tends to become larger. Therefore, larger expert pools are more likely to contain an extreme common-aligned expert that dominates early top-1 assignment.

This is the mathematical version of the mentor's scaling intuition.

### 8.3 What this proves and does not prove

It supports:

```text
common projection can create initialization-time expert accessibility imbalance.
```

It does not prove:

```text
full training collapse is completely solved by initialization alone.
```

---

## 9. Recommended Experiments for Agent Parallelization

### Agent Task A: Real Representation Geometry Audit

Deliverables:

```text
- hidden-state extraction pipeline
- feature labels or residual clusters
- random router step-0 audit
- expert-count sweep
- common projection ablation
```

Metrics:

```text
common margin
residual/feature margin
max_load
entropy
active experts
feature_NMI / cluster_NMI
```

### Agent Task B: Synthetic Label-Free Initialization

Deliverables:

```text
- common-orthogonal init
- common-equalized init
- residual-cluster init
- compare to random / slot-init / oracle cancellation
```

Metrics:

```text
slot_NMI
per-slot purity
accuracy
max_load
common margin
slot margin
```

### Agent Task C: Load Balance Comparison

Deliverables:

```text
2x2 table:
baseline
LB only
common-init only
LB + common-init
```

Goal:

```text
show whether LB and common-aware initialization solve different parts of the problem.
```

### Agent Task D: Expert Count Scaling

Deliverables:

```text
E = 4, 8, 16, 32, 64, 128
random init vs common-aware init
synthetic and frozen-real variants if possible
```

Main question:

```text
Does common-projection winner dominance grow with E, and does common-aware init suppress it?
```

---

## 10. Suggested Paper Section Plan

### Section 1: Introduction

Purpose:

```text
Introduce sparse top-1 MoE early collapse as a router initialization geometry problem.
```

Key message:

```text
Balanced data and readable features do not guarantee feature-specialized routing.
```

### Section 2: Controlled Setting

Purpose:

```text
Define synthetic ABC task as causal source of truth.
```

Include:

```text
SLOT_s B_CONST Y_s
position disabled
moving block
dot-product top-1 router
slot_NMI as primary specialization metric
```

### Section 3: Collapse Despite Feature Availability

Include:

```text
baseline accuracy 1.0 but slot_NMI low
slot probe accuracy 1.0
slot-init positive control high NMI
```

Claim:

```text
collapse is not missing-feature or impossible-specialization.
```

### Section 4: Common-Logit Bias Mechanism

Include:

```text
h = c + r
z = w_e^T c + w_e^T r
common-induced expert bias
scaling intuition with max over E experts
```

### Section 5: Early Evidence and Intervention

Include:

```text
step-0 common margin > slot margin
common argmax predicts final dominant expert
common-logit cancellation raises slot_NMI
```

Claim:

```text
common-logit is early, predictive, and intervention-relevant.
```

### Section 6: Real Representation Audit

Include results from Anchor A.

Claim:

```text
same geometry is visible / not visible in frozen real representations.
```

If weak, write honestly:

```text
real-representation evidence is preliminary.
```

### Section 7: Common-Aware Initialization

Include results from Anchor B.

Variants:

```text
random init
common-orthogonal
common-equalized
residual-cluster
oracle upper bounds
```

### Section 8: Load Balance and Boundary

Include:

```text
load balance controls utilization;
common-aware init controls assignment geometry;
they are complementary, not substitutes.
```

### Section 9: Discussion

Include:

```text
what is solved
what is not solved
future direction: persistent common-control / anti-lockin / functional expert specialization
```

---

## 11. What to Do at 17:30

### Step 1: Write Anchor A rough version first

Do not start with method. Start with real representation audit because it answers the mentor's “is it real?” question.

Write only rough bullets for:

```text
Thinking Card
Problem Definition
Physical Prior
Hypothesis
Minimal Mathematical Model
Minimal Tests
Falsifiable Outcomes
Current Evidence
Claim Boundary And Next Decision
```

### Step 2: Send Anchor A to review / critique

Do not polish it immediately. First check:

```text
Is there one decision question?
Is real representation feature definition clear?
Are metrics sufficient?
Is it not overclaiming real LM transfer?
```

### Step 3: Write Anchor B rough version

Use Anchor A result assumption:

```text
Assume common-logit bias exists in real/semi-real hidden states.
Can we initialize router label-free to suppress it?
```

### Step 4: Assign Agent experiments

Parallelize:

```text
Agent A: real representation audit
Agent B: synthetic label-free initialization
Agent C: load balance 2x2 comparison
Agent D: expert-count scaling
```

---

## 12. Current Best Alignment Message to Mentor

Use this wording when aligning with the mentor:

```text
我现在把故事线收紧成 router initialization geometry。
synthetic 部分已经说明 common component 会通过 w_e^T c 变成 expert-specific bias，解释 early collapse。
接下来我不继续做泛泛 toy audit，而是拆成两个 anchor：
第一，审计真实/半真实 hidden representation 里 random router 初始化是否也有 common-induced imbalance，并做 expert-count scaling；
第二，在这个几何上设计 label-free common-aware initialization，比如 common-equalized / common-orthogonal / residual-cluster init。
这样可以对齐您说的真实表征空间、初始化方法、以及专家数 scaling。
但文章里我会把 million-expert 作为 motivation，不直接 claim 已经解决 full-scale MoE。
```

---

## 13. Final Decision

Use two anchors:

```text
Anchor A: Real Representation Initialization Geometry Audit
Anchor B: Label-Free Common-Aware Router Initialization
```

Do not make the next anchor about B residual source. That is supporting evidence, not the paper center.

Do not make the next anchor about load balance comparison alone. Load balance is a baseline and boundary test, not the main scientific question.

Do not make the next anchor about full LM MoE training. That is too large before real representation geometry is audited.

The main paper center is:

```text
common-logit bias as a router initialization failure mode.
```

