# Deferred Protocol: 05_02_P2_zipfian_feature_frequency_routing_full

## 0. Conclusion For Review

P2 当前不进入实验文件夹，不作为 0605 本轮 runnable protocol。它保留为 future full-run protocol，只有 P1 和 P3 先给出可解释的 feature axis 与 same-expert relation 后再启动。

原因：

Zipfian frequency 会同时改变 feature sample count、tail feature coverage、expert load 和 training dynamics。如果 feature axis 尚未固定，P2 的结果无法区分 frequency effect、collapse、target learning failure 和 arbitrary lock-in。

## 1. Entry Gate

Do not run P2 until all conditions hold:

1. P1 has fixed a usable feature axis, or the user explicitly approves fallback to H0604b slot axis.
2. P3 has shown whether same-expert grouping is structured or random-level.
3. The approved token-conditioned inhibition candidate `I*` is specified.
4. `B0` baseline and `I*` comparison are both available.
5. The user explicitly asks to create a P2 experiment folder.

If any gate is missing, P2 remains parked.

## 2. Decision Question

When feature frequency becomes Zipfian rather than uniform, do head / middle / tail features show different route consistency, coverage, load pressure, or same-expert grouping?

## 3. Tested Hypothesis

If routing is frequency-sensitive, then relative to a matched uniform baseline:

- head features should keep higher route consistency and coverage;
- tail features should show lower consistency, higher assignment instability, or starvation;
- expert load may concentrate around head features;
- `I*` may either reduce tail instability or amplify head-feature lock-in.

## 4. Rival Explanations

1. Apparent tail failure is just lower sample count, not routing mechanism.
2. Collapse dominates all frequency groups.
3. The selected feature axis from P1/P3 does not survive frequency shift.
4. `I*` amplifies head-feature early lock-in instead of improving feature specialization.

## 5. Difference From Previous Experiments

| Previous result | What it tested | Why P2 must wait |
|---|---|---|
| H0604a/H0604b | feature-key consistency and feature axis under uniform setup | P2 changes feature frequency and needs the axis already fixed |
| H0605a | true inhibition collapse risk under old uniform multi-B setup | P2 must check whether frequency shift worsens that collapse risk |
| P1 | target-relevant route axis in compositional tokens | P2 needs P1's feature axis |
| P3 | structure of many-to-one grouping | P2 needs P3's grouping read to interpret head/tail expert sharing |

## 6. Future Full-Run Data

Use the feature definition fixed by P1/P3.

Construct two matched datasets:

| Dataset | Distribution | Purpose |
|---|---|---|
| `U` | uniform feature distribution | baseline |
| `Z` | Zipfian feature distribution | frequency stress test |

Keep matched:

- same feature set;
- same target rule;
- same model;
- same router condition families;
- same total training budget unless the later execution plan justifies otherwise.

Frequency groups:

- head features;
- middle features;
- tail features.

Groups must be defined by actual sample count, not by feature id.

## 7. Future Conditions / Seeds / Checkpoints

Full-run requirement when P2 is later approved:

- datasets: `U` and `Z`;
- condition families: `B0` and approved `I*`;
- seeds: `20260521`, `20260522`, `20260523` at minimum;
- full training steps match P1/P3 comparable setup;
- record early/mid/final route logs and feature coverage.

No one-seed pilot should be treated as evidence.

## 8. Primary Metric

The primary metric is tail-vs-head route stability after controlling for sample count and collapse.

Report separately for head / middle / tail:

- `Consistency(feature)`;
- feature coverage;
- assignment instability across checkpoints;
- `NMI(route; feature)`;
- expert load contribution.

Why this metric decides the judgment:

The question is not whether Zipf changes average consistency. The key issue is whether tail features lose stable routing or coverage relative to head features under a matched baseline.

## 9. Secondary Metrics

Report:

- `expert_load_entropy_norm`;
- `expert_load_max_fraction`;
- `active_experts`;
- head/mid/tail active experts;
- same-expert grouping relation by frequency group if P3 defines it;
- target accuracy by frequency group if available.

## 10. Required Figures And Tables

Figures:

- consistency vs log frequency;
- feature coverage vs log frequency;
- feature frequency vs assigned expert load;
- head/mid/tail route heatmaps;
- expert load histogram for `U` and `Z`;
- assignment instability across checkpoints.

Tables:

- head/mid/tail summary table;
- seed-level collapse table;
- frequency-controlled comparison table;
- excluded-seed table with collapse / missing-coverage reason.

## 11. Success / Failure / Insufficient Evidence

Success:

- Zipfian distribution creates a clear, collapse-filtered head/tail difference relative to uniform baseline;
- the difference remains after controlling for sample count;
- `I*` effect can be separated from baseline frequency effect.

Failure:

- head/mid/tail behave similarly after sample-count control;
- frequency shift does not change routing structure relative to uniform;
- `I*` mainly increases collapse or head-feature concentration.

Insufficient evidence:

- feature axis remains unclear;
- P3 grouping relation is not interpretable;
- tail coverage is too low to estimate routing;
- only one seed is available;
- collapse dominates all frequency groups.

## 12. What This Cannot Claim

This future protocol cannot claim:

1. real language Zipf behavior is solved;
2. tail failure is causal without matched controls;
3. frequency explains all collapse;
4. expert utility specialization;
5. robustness before P1/P3 establish the feature and grouping interpretation.

## 13. Current Action

Do not create a P2 experiment folder in this round. After P1/P3 are reviewed and executed, revisit this protocol and convert it into a runnable full-run `protocol_for_approval.md` only if the next decision is frequency robustness.
