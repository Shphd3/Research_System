# Protocol For Approval: A05_02_P3_same_expert_feature_relation

## 0. Purpose

P3 放松 minimal baseline setting 的第三个假设：不再只看 feature 是否稳定进入 expert，而是检查多个 features 进入同一 expert 后是否有 meaningful structure。

这里的 meaningful structure 指：same-expert features 是否比 load-matched random grouping 更 family-structured，而不是 arbitrary buckets。

## 1. Decision Question

当 $F>E$ 时，同一 expert 内的 features 是否共享 ground-truth family、hidden geometry 或 target relation？

## 2. Tested Hypothesis

Under non-collapse, same-expert features should be more family-structured than load-matched random grouping.

## 3. Rival Explanation

same-expert grouping 可能只是 arbitrary early-locking bucket、load artifact 或 collapse false positive。

## 4. Data Construction

Use a family-structured feature dataset:

- number of experts: $E=4$
- number of feature families: $G=4$
- features per family: $K=4$
- total features: $F=G\times K=16$, so $F>E$
- distribution: uniform

Define each feature as:

$$
f=(g,k)
$$

where:

- $g$ is the ground-truth family id;
- $k$ is the within-family feature id.

Use this sequence format:

$$
x=[r_{\mathrm{start}},
G_{g1},G_{g2},G_{g3},
F_{gk1},F_{gk2},F_{gk3},
Y_{gk},
r_{\mathrm{end}}]
$$

Do not include $B_i$ in the first P3 dataset unless P1 shows $B_i$ is part of the routed feature.

## 5. Route Logging Position

Use the last $F_{gk}$ token position for route logging in every condition. This is the pre-target position immediately before $Y_{gk}$.

Do not mix route logging positions across conditions.

## 6. Model / Conditions

Minimum condition families:

| Code | Meaning | Purpose |
|---|---|---|
| `B0` | no-inhibition baseline | tests family-structured grouping under assumption relaxation |
| `I*` | approved inhibition candidate, if available | condition comparison only |

Inhibition is not the main storyline. It is only a condition to compare against baseline.

## 7. Seeds / Checkpoints

Full run:

- uniform family-structured data;
- `B0` included;
- `I*` included only if implementation is already specified;
- at least seeds `20260521`, `20260522`, `20260523`;
- final checkpoint route logs;
- optional early/mid/final checkpoints for grouping trajectory.

Smoke checks are allowed, but they are not evidence.

## 8. Primary Metric

Primary metric: same-expert family structure over load-matched random baseline.

Use at least family purity:

$$
\Delta_{\mathrm{family}}=
\mathrm{Purity}_{actual}-\mathrm{Purity}_{random}
$$

If available, also report:

- hidden centroid similarity over random baseline;
- target-relation score over random baseline.

## 9. Required Figures / Tables

1. Expert × feature heatmap, with features ordered by family.
2. Expert × family composition heatmap.
3. Same-expert relation vs load-matched random baseline:
   include family purity, hidden centroid similarity, and target-relation score if available.
4. Expert load histogram by condition and seed.
5. Optional: checkpoint grouping trajectory.

## 10. Secondary Checks

- target accuracy;
- `active_experts`;
- `expert_load_max_fraction`;
- `expert_load_entropy_norm`;
- number of features per active expert;
- excluded seeds with collapse or insufficient-feature reason.

## 11. Decision Rule

Supported if same-expert features are more family-structured than load-matched random grouping under non-collapse.

Weakened if same-expert grouping is no more structured than random.

Invalid if routing collapses, target learning fails, or too few features remain per active expert.

## 12. What This Cannot Claim

P3 cannot claim:

- expert utility specialization;
- causal expert function;
- Zipfian robustness;
- real-data generalization;
- new router design.

## 13. User Approval Checklist

- [ ] Dataset uses $E=4$, $G=4$, $K=4$, $F=16$.
- [ ] Each feature is $f=(g,k)$.
- [ ] Sequence format matches this protocol.
- [ ] $B_i$ is excluded unless P1 requires it.
- [ ] Load-matched random baseline is included.
- [ ] Required heatmaps and relation-vs-random table are produced.
- [ ] Collapse and target learning are checked before interpretation.
