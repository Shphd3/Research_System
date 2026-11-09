# Protocol For Approval: H0604b Feature-Axis Audit On Existing Logs

Anchor:

```text
../../../problem_anchors/05_failure_mechanism/05_01_geometric_inhibition_anchor.md
```

Goal:

用最小 audit 决定当前所谓 `feature` 到底是什么：`slot`、`B_i`，还是原子组合 `(slot,B_i)`。

Decision question:

在 H0604a 的 uniform multi-B route logs/checkpoints 中，router 更像是按哪个 feature label 分发？

Tested hypothesis:

如果当前 router 已经有可用的 weak route consistency，那么至少有一个 operational feature label \(f\in\{slot,B_i,(slot,B_i)\}\) 会满足较高的

\[
\mathrm{mean}_f\max_e P(route=e\mid f)
\]

并且该结构不能由 collapse 解释。

Rival explanation:

1. `exact feature unstable`: 连 `(slot,B_i)` 都不稳定，说明 weak route consistency 本身不可靠。
2. `composite identity`: `(slot,B_i)` 稳定但 `slot` 不稳定，说明 router 绑定的是 atomic predictive state，不是 slot-level feature。
3. `collapse false positive`: consistency 高但 expert load entropy 低，说明是 all-to-one / near-all-to-one routing。
4. `B_i shortcut`: `B_i` 比 `slot` 更解释 route，削弱 slot-specialization 表述。

Data:

不重新训练。读取 H0604a 已有 route logs/checkpoints：

```text
Projects/from-attention-to-search/main/experiments/H0604a_feature_key_routing_stability_center_only/
```

Required fields:

```text
condition, seed, step, slot_id, b_id, variant_id, expert_id
```

Model:

沿用 H0604a 的 `SparseTinyTransformer` / top-1 selected-gate MoE；本实验不改模型。

Routing / algorithm:

For each condition, seed, checkpoint:

1. define three feature labels:
   - \(f=slot\);
   - \(f=B_i\);
   - \(f=(slot,B_i)\).
2. estimate \(P(e\mid f)\) from route logs;
3. compute \(\max_e P(e\mid f)\) and aggregate over features;
4. compute NMI between route and each feature label;
5. compute expert load entropy, max load, active experts;
6. build per-expert composition tables for `slot`, `B_i`, and `(slot,B_i)`.

Loss / objective:

No training objective. This is an analysis-only audit.

Conditions:

Use all H0604a conditions:

| Code | Router | Init | Extra loss |
|---|---|---|---|
| R0-dot | dot | random | NTP only |
| R1-dot | dot | random | center separation only |
| S0-dot | dot | slot init | NTP only |
| S1-dot | dot | slot init | center separation only |
| R0-cos | cosine | random | NTP only |
| R1-cos | cosine | random | center separation only |
| S0-cos | cosine | slot init | NTP only |
| S1-cos | cosine | slot init | center separation only |

Checkpoints / seeds:

Use H0604a checkpoints:

```text
step 0, step 800, step 1600
seeds: 20260521, 20260522, 20260523
```

Primary metric:

For each feature label type \(F\in\{slot,B_i,slot+B_i\}\):

\[
\mathrm{Consistency}(F)=
\frac{1}{|F|}
\sum_{f\in F}
\max_e P(route=e\mid f)
\]

Read this only after collapse filtering.

Secondary metrics:

1. `NMI(route; slot)`;
2. `NMI(route; B_i)`;
3. `NMI(route; slot+B_i)`;
4. expert load entropy norm;
5. max load fraction;
6. active experts;
7. per-expert composition entropy for slot / \(B_i\) / `(slot,B_i)`;
8. checkpoint drift of the dominant feature axis.

Known good case:

`S0-cos` / `S1-cos` non-collapsed seeds should show stronger slot-related structure than random baselines if previous interpretation is valid.

Known bad case:

Single-expert collapse seeds, e.g. `S1-cos seed=20260522`, should score high on consistency but fail load entropy / max load guard.

Known confusing case:

High `(slot,B_i)` consistency with weak `slot` NMI: this supports weak route consistency but not slot-level specialization.

Success:

This audit succeeds if it assigns the current evidence to exactly one next branch:

| Branch | Condition | Next decision |
|---|---|---|
| 2A | exact feature `(slot,B_i)` is not stable after non-collapse filtering | diagnose why weak route consistency fails |
| 2B | `(slot,B_i)` stable but slot unstable | treat routed feature as composite identity / atomic predictive state |
| 2C | exact feature stable and non-collapsed, with clear slot or slot+B_i structure | proceed to “multiple features entering one expert: what relation do they share?” |

Failure:

The audit weakens the current line if all non-collapsed seeds have low consistency for `slot`, \(B_i\), and `(slot,B_i)`, or if all apparent structure is explained by collapse.

Insufficient evidence:

1. route logs do not contain enough fields to reconstruct feature labels;
2. too many seed-condition pairs are collapsed to compare feature axes;
3. NMI and consistency disagree without a readable composition table;
4. checkpoint route logs are missing, so drift cannot be checked.

What this cannot claim:

1. It cannot claim expert utility specialization.
2. It cannot claim Zipf / frequency robustness.
3. It cannot decide whether multiple features inside one expert share a semantic, geometric, or functional relation.
4. It cannot justify route-utility binding until the feature axis is fixed.

Required outputs after approval:

```text
tables/feature_axis_consistency_by_condition.csv
tables/feature_axis_consistency_by_seed.csv
tables/feature_axis_nmi_by_condition.csv
tables/feature_expert_matrix_slot.csv
tables/feature_expert_matrix_b_id.csv
tables/feature_expert_matrix_slot_b_id.csv
tables/per_expert_composition_slot.csv
tables/per_expert_composition_b_id.csv
tables/per_expert_composition_slot_b_id.csv
tables/collapse_filtered_branch_decision.csv
figures/feature_expert_heatmap_slot.png
figures/feature_expert_heatmap_b_id.png
figures/feature_expert_heatmap_slot_b_id.png
figures/feature_axis_consistency_comparison.png
figures/feature_axis_nmi_comparison.png
figures/expert_load_histogram.png
figures/feature_axis_checkpoint_drift.png
summary.md
detailed.md
```

User approval checklist:

1. Confirm this is analysis-only on existing H0604a logs.
2. Confirm the three feature labels are exactly `slot`, `B_i`, and `slot+B_i`.
3. Confirm the decision must choose branch 2A / 2B / 2C rather than mechanically running all later stages.
