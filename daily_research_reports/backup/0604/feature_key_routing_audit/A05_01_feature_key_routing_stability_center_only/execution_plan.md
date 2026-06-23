# Execution Plan: H0604a Feature-Key Routing Stability Center-Only

Anchor:
`../../problem_anchors/05_failure_mechanism/05_01_geometric_inhibition_anchor.md`

Approved protocol:
`protocol_for_approval.md`

## 1. Run Goal

本实验是 05_01 的 follow-up。05_01 已经说明 center separation alone 不能稳定产生 slot-level routing；H0604a 进一步检查更细粒度的问题：

同一个具体 feature key $(slot_id=s,b_id=i)$ 是否稳定 route 到同一个 expert？

这里 feature key 明确定义为：

$$
f=(s,i)=(slot\_id,b\_id)
$$

random initialization 也必须接受同样标准：如果 random init 真的学到 feature-key-stable routing，那么同一个 $(s,i)$ 的多个 eval variants 也应该进入同一个 expert；但必须排除 all-to-one collapse。

## 2. Data / Material / Case Construction

Base sequence:

$$
x_{s,i}=[r_{\mathrm{start}},C_s,B_i,Y_{s,i},r_{\mathrm{end}}]
$$

Feature key:

$$
(s,i)=(slot\_id,b\_id)
$$

Eval variants:

$$
x_{s,i,r}
$$

where $r$ is a nuisance variant id. A valid variant keeps:

- same `slot_id=s`;
- same `b_id=i`;
- same target $Y_{s,i}$;
- same target position;
- changed nuisance tokens outside the slot cue, B token, and target position.

If current code cannot support meaningful variants, the result is downgraded to checkpoint/seed stability and cannot claim sample-level robustness. The implementation should attempt variant eval directly.

## 3. Conditions

| Code | Router | Init | Extra loss | Equivalent 05_01 condition |
|---|---|---|---|---|
| R0-dot | dot | random | NTP only | C0 |
| R1-dot | dot | random | center separation only | D0 |
| S0-dot | dot | slot init | NTP only | C1 |
| S1-dot | dot | slot init | center separation only | D1 |
| R0-cos | cosine | random | NTP only | C3 |
| R1-cos | cosine | random | center separation only | K0 |
| S0-cos | cosine | slot init | NTP only | C4 |
| S1-cos | cosine | slot init | center separation only | K1 |

No condition uses feature separation objective or supervised token margin.

## 4. Primary Metric

For each feature key:

$$
\mathrm{consistency}(s,i)=\max_e P(e\mid s,i)
$$

Aggregate:

$$
\mathrm{FeatureKeyConsistency}
=
\frac{1}{|\mathcal{F}|}
\sum_{(s,i)}
\max_e P(e\mid s,i)
$$

This metric answers:

Does each concrete feature key route stably to one expert?

It cannot answer:

Whether different feature keys use different experts, or whether the chosen expert is causally useful.

## 5. Collapse Guard

Report expert load:

$$
P(e)=\frac{1}{|\mathcal{F}|R}\sum_{s,i,r}\mathbf{1}[\mathrm{route}(s,i,r)=e]
$$

and entropy:

$$
H(E)=-\sum_e P(e)\log P(e)
$$

Normalized entropy:

$$
H(E)/\log E
$$

If feature-key consistency is high but expert-load entropy is low, the result is collapse and does not support specialization.

## 6. Secondary Metrics And Figures

| Artifact | Question |
|---|---|
| `feature_key_consistency_by_condition.csv` | Which condition improves feature-key consistency? |
| `feature_key_consistency_by_seed.csv` | Is the effect seed-stable? |
| `feature_key_route_matrix.csv` | Which expert is selected for each $(s,i)$? |
| `expert_load_by_condition.csv` | Does high consistency come from collapse? |
| `checkpoint_feature_drift.csv` | Does each feature key keep the same main expert across checkpoints? |
| `feature_key_consistency_histogram.png` | Are most keys near consistency 1? |
| `expert_load_distribution.png` | Is expert usage non-collapsed? |
| `feature_key_route_heatmap.png` | Is routing structured by slot, B identity, or collapse? |
| `checkpoint_feature_drift.png` | When do feature-key assignments change? |

## 7. Pass / Fail Criteria

Success:

1. S1-cos or S1-dot improves FeatureKeyConsistency over its NTP-only baseline.
2. Most keys have $\max_e P(e\mid s,i)\ge 0.95$.
3. Expert load entropy is not collapsed.
4. Target accuracy does not drop.
5. All three seeds avoid single-expert collapse.

Failure:

1. FeatureKeyConsistency does not exceed baseline.
2. High consistency is explained by single-expert collapse.
3. Only one seed succeeds.
4. Feature main expert drifts heavily across checkpoints.
5. The result only holds for deterministic duplicate eval without variants.

## 8. Implementation Contract

Runner should:

1. reuse H0603 geometric runner model, router init, center-separation loss, and ACP launch pattern;
2. map H0604 condition names to H0603 condition semantics;
3. generate eval variants for each $(s,i)$ with variant id `r`;
4. dump route logs at step 0, mid checkpoints, and final;
5. compute feature-key consistency and collapse guard from route logs;
6. preserve selected-gate top-1 router and `bias=False`;
7. produce all required tables/figures.

## 9. Result Location

Research record:

```text
Projects/from-attention-to-search/main/experiments/A05_01_feature_key_routing_stability_center_only/
```

Code workspace:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/
```

Expected raw result dir:

```text
results/h0604a_feature_key_routing_stability_center_only/
```

Expected raw figure dir:

```text
figures/h0604a_feature_key_routing_stability_center_only/
```
