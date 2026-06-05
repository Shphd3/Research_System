# Protocol For Approval: 05_02_A05_02_P1_compositional_token_feature_routing

## 0. Purpose

P1 放松 minimal baseline setting 的 single-feature token 假设。它测试：当 input token context 同时包含多个 candidate features 时，router 是否跟随 target-relevant factor，而不是固定 surface axis 或 nuisance $B_i$。

这不是 utility binding、Zipfian experiment、real-data test 或 new router design。

## 1. Decision Question

在同一数据格式下改变 target rule 时，dominant route axis 是否随 target-relevant factor 改变？

## 2. Tested Hypothesis

Under non-collapse:

- C1: $Y=Y(S1)$ 时，route aligns with $S1$；
- C2: $Y=Y(S2)$ 时，route aligns with $S2$；
- C3: $Y=Y(S1,S2)$ 时，route aligns with $(S1,S2)$。

## 3. Rival Explanation

router 可能始终跟随同一 surface axis，或跟随 nuisance $B_i$，即使 $B_i$ 不决定 target。

## 4. Data Construction

Use this exact sequence format:

$$
x=[r_{\mathrm{start}},
S1_{a1},S1_{a2},S1_{a3},
S2_{b1},S2_{b2},S2_{b3},
B_i,
Y,
r_{\mathrm{end}}]
$$

Required sizes:

- $|S1|=4$
- $|S2|=4$
- $|B_i|=64$ or $256$
- $B_i$ is nuisance in C1/C2/C3
- keep a nuisance variant dimension if already supported

## 5. Target Rules

| Condition | Target rule | Target-relevant axis | Nuisance axes |
|---|---|---|---|
| C1 | $Y=Y(S1)$ | $S1$ | $S2$, $B_i$ |
| C2 | $Y=Y(S2)$ | $S2$ | $S1$, $B_i$ |
| C3 | $Y=Y(S1,S2)$ | $(S1,S2)$ | $B_i$ |

Do not add C4 in the first run.

## 6. Route Logging Position

Use the $B_i$ position for route logging in every condition. This is also the pre-target position immediately before $Y$.

Do not mix logging positions across C1/C2/C3. Do not compare routes logged from $S1$ or $S2$ positions with routes logged from $B_i$ position.

## 7. Model / Conditions

Use the current matched MoE setup from the 05 line.

Minimum condition families:

| Code | Meaning | Purpose |
|---|---|---|
| `B0` | no-inhibition baseline | tests whether assumption relaxation works without candidate inhibition |
| `I*` | approved inhibition candidate, if available | condition comparison only, not the main storyline |

## 8. Seeds / Checkpoints

Full run:

- C1/C2/C3 all included;
- `B0` included;
- `I*` included only if implementation is already specified;
- at least seeds `20260521`, `20260522`, `20260523`;
- final checkpoint plus early/mid/final route logs if supported.

Smoke checks are allowed, but they are not evidence.

## 9. Primary Metric

Primary metric: target-rule × route-axis NMI matrix.

Rows:

- C1
- C2
- C3

Columns:

- $S1$
- $S2$
- $B_i$
- $(S1,S2)$

Normalized mutual information, 即归一化互信息（NMI）, decides the route axis because consistency alone can be high under collapse.

## 10. Required Figures / Tables

1. Target-rule × route-axis NMI matrix:
   rows = C1/C2/C3; columns = $S1$/$S2$/$B_i$/$(S1,S2)$.
2. Target-relevant feature × expert heatmap:
   C1: $S1 \times expert$;
   C2: $S2 \times expert$;
   C3: $(S1,S2) \times expert$.
3. Expert load histogram by condition and seed.
4. Target accuracy table.

## 11. Secondary Checks

- route consistency for $S1$, $S2$, $B_i$, $(S1,S2)$;
- `active_experts`;
- `expert_load_max_fraction`;
- `expert_load_entropy_norm`;
- excluded seeds with collapse reason.

## 12. Decision Rule

Supported if dominant route axis changes with target rule under non-collapse:

- C1 aligns with $S1$;
- C2 aligns with $S2$;
- C3 aligns with $(S1,S2)$.

Weakened if route always follows the same surface axis or $B_i$ despite $B_i$ being nuisance.

Invalid if target learning fails or routing collapses.

## 13. What This Cannot Claim

P1 cannot claim:

- expert utility specialization;
- Zipfian robustness;
- real-data generalization;
- new router design;
- that inhibition is the explanation unless `I*` passes the same target-learning and non-collapse guards.

## 14. User Approval Checklist

- [ ] Sequence format and sizes match this protocol.
- [ ] Route logging uses only the $B_i$ / pre-target position.
- [ ] C1/C2/C3 are all included.
- [ ] C4 is not included.
- [ ] Required NMI matrix and heatmaps are produced.
- [ ] Collapse and target learning are checked before interpretation.
