派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_24_frequency_composition_common_path/common_optimizer_coupling_20261022/summary.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_24_frequency_composition_common_path/common_optimizer_coupling_20261022/summary.md)；研究修改仍回到原件。

---

# Summary: separating common-gradient clipping from routed learning

[中文](summary_cn.md) · [Frozen Protocol](../../../../../../../../UNAVAILABLE.md) · [Detailed evidence](../../../../../../../../UNAVAILABLE.md)

**All four models completed. Excluding common from the routed experts' clipping denominator changed actual AdamW updates, but did not consistently improve low-feature prediction.** Final low-feature macro NLL changes were -0.000332 for seed 11 and +0.000529 for seed 22. The registered two-seed improvement criterion is not met. This is an exploratory result on an already exposed DEV panel; researcher-level mechanism judgment and question closure remain Unknown.

## Purpose and distinct contribution

The earlier common-expert experiment improved TRAIN fit without stable low-feature DEV benefit, while global gradient clipping became much more frequent. This round asks whether that optimization coupling helps explain the result. It owns a rival explanation under [A15_24_01](../../../../../../../../UNAVAILABLE.md). The referenced A15_25 discussion investigates feature relations and frozen representations; here the feature groups, inputs, routes and architecture are unchanged.

The contribution is an executed separation of three quantities: **gradient scaling, actual optimizer movement, and prediction quality**. This makes a plausible explanation testable before attributing the common result to the representation space.

## Comparison and primary result

Both conditions train the same T_F model: eight experts with fixed top-2 routes and weights 0.5/0.5, plus one always-on common expert with coefficient one. They read the full frozen final-layer hidden state and predict next answer tokens through a frozen head. `global` uses one clipping coefficient for all trainable parameters. `route_isolated` calculates the routed coefficient from the routed gradients alone; common retains the original global coefficient.

Each paired seed uses equal initialization, order and budget: one epoch, 168 updates and 85,548 valid targets. Both controls and treatments were run on the same **local H100 MIG 3g.40gb**, without a new remote allocation. Qualification, four runs and evaluation consumed 307.25 seconds of summed process execution time, within the 1,200-second limit.

The primary metric first averages prediction NLL over each supported low feature's active DEV positions, then weights features equally. It covers 838 of the original 1,694 features; 856 lack DEV support. The same 10,340-position panel contains 1,701 unique low-feature positions. NLL is in natural-log units (nats) per valid answer target under the stated weighting; lower is better.

| Seed | Global: low-feature macro | Route-isolated: low-feature macro | Paired change | Overall change | Low-position-union change |
|---|---:|---:|---:|---:|---:|
| 11 | 1.056352688 | 1.056020660 | -0.000332028 | -0.000098819 | +0.000137646 |
| 22 | 1.057152509 | 1.057681732 | +0.000529222 | +0.000007026 | +0.000411952 |
| Paired mean | 1.056752598 | 1.056851196 | +0.000098597 | -0.000045897 | +0.000274799 |

All changes are route-isolated minus global. Seed directions are mixed, and the low-position union worsens in both seeds. A small mean improvement in overall NLL cannot replace the primary criterion. These are descriptive two-seed effects, without a significance claim. [Conditions](../../../../../../../../UNAVAILABLE.md) · [Paired comparisons](../../../../../../../../UNAVAILABLE.md)

## What the mechanism measurements establish

More clipping did not mean less total parameter movement in the original experiment. The completed historical audit found that adding common increased routed cumulative update path length by 1.916%–2.309%. First-step clipped-gradient scaling fell about 40%–44%, while the actual routed update norm fell only 0.032%–0.042%. Path length measures movement, not useful learning. [Historical audit](../../../../../../../../UNAVAILABLE.md)

Adam explains why those quantities differ. At the first step with zero moments, multiplying a gradient by a positive coefficient \(c\) gives an adaptive update proportional to \(cg/(|cg|+\epsilon)\). Except near zero-gradient coordinates, the scale nearly cancels. Later varying coefficients interact with accumulated first and second moments and can alter the update direction.

The new experiment tested this directly. At seed 11, step 1, the same raw gradients and Adam state gave routed clipped-gradient norms **0.562684 versus 0.999999**, while actual update norms were **0.096449567 versus 0.096484435**, only a 0.0362% norm increase. At step 42 of the global trajectory, the two policy updates differed by **9.979% of the global update norm**, with an angle of **5.373 degrees**. Common's shadow update was exactly equal across policies at all 20 registered comparisons. These are genuine optimizer effects at fixed state, measured without an extra backward pass. [Seed-11 step records](../../../../../../../../UNAVAILABLE.md)

Across full training, routed clipping dropped from 161/160 steps to 21/18. Yet cumulative routed movement decreased from 37.5284/37.4601 to 36.5212/36.4992, and final TRAIN overall NLL increased in both seeds. Thus a larger permitted gradient does not monotonically produce greater movement or better prediction. Full diagnostics and all five shadow checkpoints are in [Detailed](../../../../../../../../UNAVAILABLE.md).

## Bounded reading and next decision

**Direct result:** common participates in a real optimizer coupling; removing this particular coupling did not produce the registered stable low-feature gain. **AI interpretation:** the simple account that common starves routed experts by shrinking their overall Adam steps is weakened by both the historical movement audit and the intervention. Other functional interactions, moment histories and representation-related explanations remain open.

The new global runs are not numerically identical to the historical remote runs. Only within-round, same-environment policy pairs identify the intervention here; combining a new treatment with an old baseline would confound it. Neither this result nor the original common experiment establishes a Rank-one mechanism or a universal MoE architecture verdict.

The researcher-owned next decision is **Unknown**: whether this policy remains worth pursuing after the measured mixed result. The current task has completed its registered comparison; no additional training is implied. [Artifact identities and registration status](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_24_frequency_composition_common_path/common_optimizer_coupling_20261022/artifact_manifest.json)
