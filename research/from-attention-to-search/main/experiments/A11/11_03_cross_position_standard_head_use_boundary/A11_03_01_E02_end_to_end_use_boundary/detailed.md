# A11_03_01_E02 End-to-End Bridge-Conditioned Semantic Efficiency: Detailed Record

## 1. Decision Question

Does the bridge-conditioned local transport observed in A11_19 predict whether K=2 MTP learns a standard downstream semantic action more efficiently than NTP?

## 2. Operational Long-Horizon Semantics

An example contains an early persistent assistant state \(Z\), a long intervening context, and a later action. The construct requires:

\[
I(Z;Y\mid W_T)>0,
\]

plus paraphrase invariance and state-counterfactual dependence. The evaluation score is

\[
Q_{real}=\min\{A_{H1},C_{para},S_{cf}\}.
\]

This prevents high native accuracy from hiding failures to preserve meaning across wording or react to a changed early state.

## 3. Experimental Design

| Condition | Bridge | Training loss |
|---|---|---|
| `ntp_decision` | `Decision` | bridge H1 + final action H1 |
| `mtp_decision` | `Decision` | NTP losses + earlier H2 action loss |
| `ntp_therefore` | `Therefore` | bridge H1 + final action H1 |
| `mtp_therefore` | `Therefore` | NTP losses + earlier H2 action loss |

The pretrained model, data, held-out paraphrases, answer tokens, optimizer, examples, batch schedule, and 300-update budget are fixed. Five paired seeds are used.

## 4. Primary Metric

Normalized update AUC and the interaction are

\[
A_{o,b}^{(s)}=\frac1{300}\int_0^{300}Q_{real}^{(s)}(o,b,t)\,dt,
\]

\[
\Delta_{int}^{(s)}
=\big(A_{MTP,Therefore}^{(s)}-A_{NTP,Therefore}^{(s)}\big)
-\big(A_{MTP,Decision}^{(s)}-A_{NTP,Decision}^{(s)}\big).
\]

The preregistered support rule requires positive interaction in `4/5`, positive `Therefore` MTP gain in `4/5`, and positive mean interaction.

## 5. Per-Seed Results

| Seed | \(\Delta_Q\) `Decision` | \(\Delta_Q\) `Therefore` | \(\Delta_{int,Q}\) | \(\Delta_{int,H1-margin}\) |
|---:|---:|---:|---:|---:|
| 971 | +0.0208 | -0.0160 | -0.0368 | +1.3125 |
| 972 | -0.0703 | -0.1193 | -0.0490 | +0.4966 |
| 973 | +0.0568 | +0.1806 | +0.1238 | +1.2442 |
| 974 | -0.2272 | +0.0046 | +0.2319 | +5.5396 |
| 975 | -0.1180 | -0.0602 | +0.0579 | +1.6657 |
| Mean | -0.0676 | -0.0020 | +0.0656 | +2.0517 |

The margin interaction is directionally consistent, but the conservative behavioral interaction is not. Moreover, mean MTP gain is negative under both bridges.

## 6. Condition-Level Results

| Condition | Mean Q AUC | Mean final Q | Mean H1-margin AUC | Mean final H1 margin | Mean final H2 native |
|---|---:|---:|---:|---:|---:|
| NTP / `Decision` | 0.4328 | 0.8250 | 5.3547 | 12.0311 | 0.0000 |
| MTP / `Decision` | 0.3652 | 0.8125 | 2.7074 | 8.4947 | 0.9025 |
| NTP / `Therefore` | 0.1502 | 0.6138 | 1.5324 | 9.1705 | 0.0000 |
| MTP / `Therefore` | 0.1481 | 0.5025 | 0.9368 | 4.8788 | 0.7413 |

No run reaches \(Q_{real}\ge0.9\) for three consecutive evaluations. MTP's private H2 is learned, but the common H1 interface is not improved.

## 7. Local-Learning Guard

The local guard requires MTP final local accuracy to remain within `0.01` of paired NTP, final local CE within `5%`, and MTP local CE not to regress by more than `10%` from initialization. At least one bridge fails a tolerance in every seed, so the guard passes `0/5`.

Mean final local results are:

| Condition | Local CE | Local accuracy |
|---|---:|---:|
| NTP / `Decision` | 2.3737 | 0.5686 |
| MTP / `Decision` | 2.6095 | 0.5288 |
| NTP / `Therefore` | 2.0475 | 0.6556 |
| MTP / `Therefore` | 2.1141 | 0.6517 |

The tradeoff is larger under `Decision`; it prevents a claim of efficiency without local cost.

## 8. Implementation And Failure Audit

### Completed training

- `20/20` condition-seed tasks completed;
- `200/200` expected checkpoint rows exist;
- all numeric values are finite;
- step-0 NTP/MTP pairing passes in both bridges for `5/5` seeds;
- sample and batch-schedule hashes match;
- within-bridge selected-parameter initialization hashes match.

### Inherited aggregator mismatch

The inherited A11_14 aggregator sets `paired_hash_pass=false` because it compares selected embedding hashes across all four conditions. Since `Decision` and `Therefore` are different token IDs, their selected embedding rows should differ. The A11_03_01_E02 analyzer replaces this with the preregistered within-bridge NTP/MTP equality check. This is a protocol-aligned implementation correction, not a post-hoc metric change.

### Formal status

The experiment is formally **insufficient** because the local guard fails. Independently of that gate, the primary behavioral support criterion also fails: `3/5` interaction-positive and `2/5` positive MTP gain under `Therefore` are below the `4/5` thresholds. Therefore removing the local guard would not turn the main hypothesis into a pass.

## 9. Visualization Results

![A11_03_01_E02 end-to-end interaction](figures/a11_20_end_to_end_bridge_conditioned_efficiency.png)

- **Question:** does bridge-conditioned local transport selectively improve finite-step MTP behavior?
- **Reading:** left gives mean held-out \(Q_{real}\); center gives within-bridge MTP-minus-NTP AUC by seed; right gives the difference-in-differences.
- **Observed:** three positive and two negative behavioral interactions; mean `Decision` trajectories are stronger than `Therefore`; MTP does not consistently exceed NTP.
- **Take-home:** bridge state changes the relative geometry, but local alignment is not sufficient for robust behavioral efficiency.
- **Remaining uncertainty:** longer training or different loss weighting could change behavior, but testing those would answer an optimization-design question rather than validate the preregistered mechanism claim.

## 10. Hypothesis Assessment

- **Bridge-conditioned margin modulation:** supported empirically (`5/5` positive interaction).
- **Bridge-conditioned end-to-end MTP efficiency:** not supported (`3/5` behavioral interaction; `2/5` favorable-bridge gain).
- **MTP sample/update efficiency on this proxy:** not established; no sustained threshold event.
- **No local cost:** contradicted by the preregistered guard.

## 11. Artifact Map

- successful full training job: `pt-oiawef4n`;
- full run: `a11_20_end_to_end_bridge_conditioned_efficiency_4gpu_20260711_023943`;
- earlier smoke-only failed job: `pt-ocf0jnqv`;
- raw result directory: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a11_20_end_to_end_bridge_conditioned_efficiency/a11_20_end_to_end_bridge_conditioned_efficiency_4gpu_20260711_023943`;
- runner: `scripts/run_a11_20_end_to_end_bridge_conditioned_efficiency.py`;
- analyzer: `scripts/analyze_a11_20_end_to_end_bridge_conditioned_efficiency.py`;
- config: `configs/a11_20_end_to_end_bridge_conditioned_efficiency.json`;
- submitter: `scripts/submit_a11_20_end_to_end_bridge_conditioned_efficiency_4gpu.sh`;
- canonical tables: `tables/trajectory_summary.csv`, `tables/interaction_summary.csv`;
- central figure: `figures/a11_20_end_to_end_bridge_conditioned_efficiency.png`.
