# 05_02 P3 Protocol: Same-Expert Feature Relation

## 1. Purpose

This protocol relaxes the advisor's third toy assumption:

```text
A3. 不分析多个 features 进入同一个 expert 后的关系。
```

Question:

```text
当多个 features 进入同一个 expert 时，它们是 arbitrary bucket，还是 structured group？
```

This updates our router understanding because feature-level specialization cannot mean only same-feature consistency. If F > E, one expert must receive multiple features; their relation determines whether routing is meaningful or just hash-like lock-in.

---

## 2. Minimal Setup

Use a feature axis fixed by P1 or the current best 05_01 condition.

Construct:

```text
F features
E experts
F > E
uniform feature distribution
non-collapsed routing required
```

Avoid unnecessary B_i confound if the goal is slot-feature relation.

Recommended first version:

```text
feature = slot-like class
number of features > number of experts
same target rule across conditions
```

---

## 3. What To Measure

For each expert, collect the features mostly routed to it.

Measure four possible relations:

```text
1. geometry relation:
   hidden centroid similarity among same-expert features

2. target relation:
   whether same-expert features share target structure

3. trajectory relation:
   whether features enter the expert at similar training stages

4. seed stability:
   whether grouping is stable across seeds
```

Compare against:

```text
load-matched random grouping baseline
```

---

## 4. Metrics

Report:

```text
same-expert intra-group centroid similarity
random-baseline intra-group similarity
same-expert target-relation score
cross-seed grouping stability
expert load entropy
max load fraction
active experts
```

Required figures:

```text
expert → feature composition table
same-expert similarity vs random baseline
feature grouping heatmap
expert load histogram
```

---

## 5. Decision Rules

Supported if:

```text
same-expert features are more similar than load-matched random groups;
this relation appears in geometry, target relation, or training trajectory;
results pass collapse guard.
```

Weakened if:

```text
same-expert features are no more structured than random groups;
grouping changes strongly across seeds;
apparent structure disappears after removing collapsed runs.
```

Insufficient evidence if:

```text
feature axis is not fixed;
experts collapse;
too few features enter each expert;
only one seed is available.
```

---

## 6. What Not To Claim

Do not claim:

```text
utility-aligned specialization;
causal expert function;
real-data generality.
```

This protocol only tests whether many-to-one feature assignment has structure beyond arbitrary early lock-in.
