# 05_02 P1 Protocol: Compositional Token Feature Routing

## 1. Purpose

This protocol relaxes the advisor's first toy assumption:

```text
A1. 一个 token 只有一个 feature。
```

Question:

```text
当 token 同时包含多个 candidate features 时，router 是否跟随 target-relevant factor？
```

This updates our router understanding because it tests whether route consistency is tied to the predictive factor, rather than a fixed surface axis or arbitrary lock-in.

---

## 2. Minimal Data

Each sample contains two slot-like feature groups and one identity token:

```text
x = [r_start,
     S1_a1, S1_a2, S1_a3,
     S2_b1, S2_b2, S2_b3,
     B_i,
     Y,
     r_end]
```

Design choice:

```text
S1 uses 3 tokens.
S2 uses 3 tokens.
```

Reason:

```text
This reduces the chance that routing is dominated by one short random context token.
```

---

## 3. Conditions

Use the same architecture and router setup as the current clean 05_01 condition.

Start with:

```text
S0-cos or S1-cos
1 seed pilot first
then 3 seeds if the pilot is valid
```

---

## 4. Target Rules

Run three minimal datasets:

### C1: S1-only target

```text
Y = Y(S1)
```

S1 is target-relevant. S2 and B_i are nuisance.

### C2: S2-only target

```text
Y = Y(S2)
```

S2 is target-relevant. S1 and B_i are nuisance.

### C3: compositional target

```text
Y = Y(S1, S2)
```

The target requires both slot groups.

Optional later:

```text
C4: Y = Y(S1, S2, B_i)
```

Do not run C4 in the first pilot unless C1-C3 are clear.

---

## 5. Metrics

For each condition, report:

```text
Consistency(S1)
Consistency(S2)
Consistency(B_i)
Consistency(S1,S2)
NMI(route; S1)
NMI(route; S2)
NMI(route; B_i)
NMI(route; S1,S2)
load entropy norm
max load fraction
active experts
```

Required figures:

```text
feature × expert heatmap for S1
feature × expert heatmap for S2
expert load histogram
NMI bar plot
```

---

## 6. Decision Rules

Supported if:

```text
C1 routes align with S1;
C2 routes align with S2;
C3 routes align with (S1,S2) or a clear target-relevant composite axis;
all results pass the collapse guard.
```

Weakened if:

```text
router always follows the same surface axis regardless of target rule;
router follows B_i even when B_i is nuisance;
high consistency only appears under collapse.
```

Insufficient evidence if:

```text
the model does not learn the target;
load is collapsed;
NMI patterns are inconsistent across seeds;
no axis is clearly dominant.
```

---

## 7. What Not To Claim

Do not claim:

```text
expert utility specialization;
real-data feature discovery;
Zipf robustness;
causal utility alignment.
```

This protocol only tests whether routing follows the target-relevant feature factor in a constructed compositional-token setting.
