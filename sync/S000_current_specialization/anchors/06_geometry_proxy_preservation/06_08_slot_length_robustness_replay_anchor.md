---
anchor_id: A06_08_slot_length_robustness_replay
status: active
parent: A06_04_to_A06_07_router_geometry_sequence
---

# A06_08 Slot-Length Robustness Replay Anchor

## 0. Thinking Card
当前问题：A06_04-A06_07 的结论是否只是 `slot_token_len=1` 的短 slot artifact？

当前判断：A06_04-A06_07 的结论对 repeated slot length `1,2,4` 稳定。长 slot 没有让 simple label-free global controls 恢复 feature specialization。

关键证据：A06_08 full run 中 route audit 全通过，split 每个 pair 都是 2048/2048，label-free leakage 为 0，A06_07-style label-free gate 是 `0/1008` pass。Primary readout 下 `slot_len=4` 的 calibration mean 只把 NMI 从 `0.1894` 提到 `0.2072`，oracle-gap fraction 只有 `0.0199`；oracle centroid 仍是 NMI `1.0`、load `0.0`。

最危险边界：这里只测试 repeated `SLOT_s` token 的长 slot，不测试 distributed multi-token slot code，也不测试训练稳定性或真实 DCLM。

下一步决策：保持主线方向，进入 feature discovery 或 anti-lockin；不要把 simple global centering / projection / whitening 推成 feature-specialization 方法。

## 1. Problem Definition

A06_04-A06_07 established a staged initialized-router geometry story in the one-token slot setting:

1. hidden common component is the dominant tested load-bias source after hidden-state formation;
2. common-centering does not remove all residual load;
3. oracle feature centroids can recover the feature partition;
4. simple label-free global common / residual controls improve load but not feature_NMI.

This anchor asks whether that story remains stable when the slot cue is longer.

Decision question:
Do the A06_04-A06_07 conclusions remain stable when `slot_token_len` changes from `1` to `2` and `4`?

## 2. Physical Priors

P1:
Longer slot spans may strengthen feature information at the routed slot position because the final slot token attends to more repeated same-slot context.

P2:
If A06_07 failed only because one-token slot signal was too weak, longer slots may let label-free global controls recover more feature_NMI.

P3:
If A06_07 failed because global common / covariance controls are not feature-discovery mechanisms, longer repeated slots may improve oracle margins but should not make random-row global controls recover the oracle partition.

## 3. Falsifiable Hypotheses

H1:
A06_04 common-component dominance remains stable across `slot_token_len in {1,2,4}`.

Supported if common-centering gives the main load reduction at each slot length.

Weakened if row-norm control or another term becomes the main load reduction when slot length grows.

H2:
A06_05 residual geometry remains after common-centering across slot lengths.

Supported if centered residual replay still has nontrivial load and whitening / matched isotropic controls reduce it.

Weakened if centered residual load becomes near zero for long slots.

H3:
A06_06 oracle feature-centroid reachability remains stable and may gain margin with longer slots.

Supported if oracle centroid conditions keep feature_NMI near 1 and load near 0.

Weakened if long slots break held-out oracle reachability.

H4:
A06_07 label-free global controls remain load controls rather than feature-specialization controls.

Supported if calibration mean / heldout mean / projection / whitening improve load but fail to close the oracle feature_NMI gap.

Weakened if one label-free global control improves feature_NMI by at least `+0.25` over baseline and closes at least `50%` of the oracle gap for long slots.

## 4. Mathematical Model

For each slot length $l$, generate hidden states $h_i^{(l)}$ at the last slot position.

Common/residual decomposition:

$$
h_i^{(l)} = c^{(l)} + r_i^{(l)}
$$

Raw router score:

$$
z_{i,e}^{RR,l} = w_e^\top h_i^{(l)}
$$

Common-centered score:

$$
z_{i,e}^{RC,l} = w_e^\top (h_i^{(l)} - c^{(l)})
$$

Label-free controlled score:

$$
z'_{i,e,l} = w_e^\top \phi_l(h_i)
$$

where $\phi_l$ is calibration mean-centering, heldout batch mean-centering, top-PC projection, or whitening.

Oracle feature-centroid score:

$$
z^{oracle}_{i,e,l}= \mu_{e,l}^\top (h_i^{(l)}-c^{(l)})
$$

where $\mu_{e,l}$ is estimated using calibration samples and `pair_id` labels. This is a non-label-free upper bound.

## 5. Computational Realization

Data:
Use the same A06 synthetic hidden-state replay surface, with `slot_token_len in {1,2,4}`. For `slot_token_len>1`, the current generator repeats the same `SLOT_s` token across the slot span, then places `TARGET_s` immediately after the slot span.

Route position:
last slot position, computed as `pair_start + slot_token_len - 1`.

Model:
Initialized Transformer-MoE replay, four experts, no training.

Core outputs:

- A06_04-style common/norm replay table;
- A06_05-style residual geometry table;
- A06_06-style oracle centroid table;
- A06_07-style label-free control table;
- slot-length comparison figures.

## 6. Minimal Falsification Tests

Primary test:
Compare feature_NMI and load $L$ across slot lengths for A06_07-style conditions.

Main falsifier for current A06_07 boundary:
A label-free global control passes at `slot_token_len=2` or `4` by improving held-out feature_NMI by at least `+0.25` over baseline and closing at least `50%` of the oracle gap.

Validity guards:

- pair counts must remain uniform;
- route position must be last slot position;
- target position must be after slot span;
- background tokens must remain independent of pair id;
- calibration/evaluation split must be balanced by pair id;
- label-free controls must not use `pair_id` labels.

## 7. Current Evidence

A06_04:
One-token slot setting supports hidden common component as the dominant tested source of initialized hidden-state load imbalance.

A06_05:
Residual covariance / structured residual geometry remains after common-centering.

A06_06:
Oracle feature-centroid initialization reaches perfect held-out feature routing.

A06_07:
Simple label-free global common / residual controls improve load but do not improve feature_NMI enough to pass the step-0 gate.

A06_08:
The robustness run completed for `slot_token_len in {1,2,4}` with 8 seeds, depths `1,2,4`, and readouts `post_ln,pre_ln_replay`.

Protocol and reports:
`../../experiments/A06/A06_08_slot_length_robustness_replay/protocol.md`
`../../experiments/A06/A06_08_slot_length_robustness_replay/summary.md`
`../../experiments/A06/A06_08_slot_length_robustness_replay/detailed.md`

Validity:
All route-position audit rows are valid; all calibration/evaluation splits are balanced at 2048/2048 per pair; label-free control leakage is zero.

Primary readout:

| Slot len | A06_04 RR $L$ | A06_04 RC $L$ | A06_05 centered $L$ | A06_07 calibration NMI | A06_07 calibration gap | Oracle NMI |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.5577 | 0.2577 | 0.2577 | 0.2079 | 0.0107 | 1.0000 |
| 2 | 0.5533 | 0.2784 | 0.2784 | 0.2040 | 0.0146 | 1.0000 |
| 4 | 0.5789 | 0.2776 | 0.2776 | 0.2072 | 0.0199 | 1.0000 |

Interpretation:
Longer repeated slots do not change the decision chain. Common-centering remains the main load reduction; residual geometry remains after centering; oracle feature partition remains reachable; simple label-free global controls still improve load without recovering feature_NMI.

## 8. Claim Boundary And Next Decision

Can claim:
The A06_04-A06_07 conclusions are robust to repeated-slot length `1,2,4` in the same synthetic initialized replay setting.

Cannot claim:
Real DCLM transfer, trained stability, distributed multi-token slot codes, semantic feature discovery, or expert utility.

Next decision:
Proceed to feature discovery / anti-lockin. Do not promote simple global common-centering, top-PC projection, or whitening as a feature-specialization method.
