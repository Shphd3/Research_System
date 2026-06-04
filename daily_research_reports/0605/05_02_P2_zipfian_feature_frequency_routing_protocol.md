# 05_02 P2 Protocol: Zipfian Feature Frequency Routing

## 1. Purpose

This protocol relaxes the advisor's second toy assumption:

```text
A2. feature distribution 是 uniform。
```

Question:

```text
当 feature frequency 变成 Zipfian 时，head features 和 tail features 的 route consistency 是否分化？
```

This updates our router understanding because it tests whether early lock-in and expert load are frequency-sensitive.

Status:

```text
Protocol ready, but experiment parked.
Run after P1 and P3 clarify feature definition and same-expert relation.
```

---

## 2. Minimal Data

Use the feature definition fixed by P1.

Construct two matched datasets:

```text
U: uniform feature distribution
Z: Zipfian feature distribution
```

Keep constant:

```text
same number of features
same target rule
same model
same router condition
same total training budget if possible
```

---

## 3. Frequency Groups

Split features into:

```text
head features
middle features
tail features
```

Use the actual sample count per feature to define groups.

---

## 4. Metrics

Report separately for head / middle / tail:

```text
Consistency(feature)
NMI(route; feature)
feature coverage
active experts per group
load entropy norm
max load fraction
```

Required figures:

```text
consistency vs log frequency
feature frequency vs assigned expert load
head/mid/tail route heatmaps
expert load histogram
```

---

## 5. Decision Rules

Supported if:

```text
head features keep stable routing;
tail features are less stable or starved;
expert load becomes more concentrated than uniform baseline.
```

Weakened if:

```text
head/mid/tail features behave similarly after controlling for sample count;
Zipfian frequency does not change routing structure relative to uniform.
```

Insufficient evidence if:

```text
feature definition is still unclear;
target learning fails;
collapse dominates all frequency groups;
results depend only on one seed.
```

---

## 6. What Not To Claim

Do not claim:

```text
Zipf explains all collapse;
tail failure is causal without controls;
real language frequency behavior is solved.
```

This protocol only tests whether constructed non-uniform feature frequency changes routing consistency and load structure.
