# Detailed Record: A09_01 Common High-Gain Band / Rare Discrimination

Primary anchor: `../../../problem_anchors/09_common_rare_spectral_discrimination/09_01_common_band_rare_discrimination_anchor.md`

Protocol: `protocol.md`

## 0. Quick Recap

Purpose: test whether common high-gain score dominance can suppress rare discrimination.

Hypothesis: the baseline high-gain band has high score share but low same-common rare discrimination share.

Experiment idea: build controlled nested common/rare data, train a common-heavy shared model, audit its high-gain band, then compare estimated split, random split, oracle split, and shuffled-label guard.

Conclusion: supported on controlled data. The estimated split reduces mismatch and rare loss while preserving common performance. Random split improves rare loss but fails the mechanism and common guard.

Evidence: baseline \(G_{mis}=0.486\); estimated split \(\Delta G_{mis}=0.486\); estimated split rare loss improves by 0.996; system common loss remains low.

## 1. Protocol Compliance

The run followed the approved protocol with one clarified implementation detail:

- For split conditions, "common loss" is measured on the common branch, not on the rare branch. This matches the split contract: the rare branch should not be required to preserve common behavior by itself.

No extra method claim was added. The run remains a controlled mechanism audit.

## 2. Data Construction

The synthetic task has 4 common groups and 4 rare subclasses per common group.

Each class is a pair \((i,j)\), where \(i\) is the common group and \(j\) is the rare subclass.

Each hidden state is generated as:

\[
h = a_C c_i + a_R r_{i,j} + \epsilon.
\]

Full-run values:

| Quantity | Value |
|---|---:|
| input dimension | 64 |
| common groups | 4 |
| rare subclasses per common | 4 |
| common strength \(a_C\) | 2.6 |
| rare strength \(a_R\) | 0.85 |
| noise std | 0.55 |
| default subclass count per common | 4096 |
| rare subclass count | 96 |
| balanced split-train count per pair | 512 |
| eval default count per common | 512 |
| eval rare count per rare subclass | 512 |

The matched rare evaluation compares:

- correct target `y`: same common group and correct rare subclass;
- common distractor `d`: same common group and default subclass.

This makes common information insufficient. The model must use rare information for `y` to beat `d`.

## 3. Model And Training Setup

All models use linear heads.

Baseline:

- one 16-class linear head;
- trained on the common-heavy distribution.

Estimated common/rare split:

- estimate rank-4 common projector from baseline readout SVD;
- common branch uses \(P_{est}h\);
- rare branch uses \((I-P_{est})h\);
- rare branch is trained on balanced pair data.

Random split:

- same architecture and rank as estimated split;
- uses a random rank-4 projector.

Oracle split:

- same architecture;
- uses the true common basis projector.

Shuffled guard:

- same as estimated split;
- rare labels are shuffled during rare-branch training.

Training parameters:

| Parameter | Value |
|---|---:|
| seeds | 20260629-20260636 |
| optimizer | AdamW |
| steps | 900 |
| batch size | 256 |
| learning rate | 0.03 |
| weight decay | 0.0001 |
| device | CPU |

## 4. Metric Definitions

For a readout matrix \(W\) and baseline high-gain projector \(P_k\):

\[
z^{top}=WP_kh,\qquad z^{res}=W(I-P_k)h.
\]

For a matched pair, `y` is the correct target and `d` is the common distractor.

Score share:

\[
C_{score}(k)=\frac{|z_y^{top}|+|z_d^{top}|}{|z_y^{top}|+|z_d^{top}|+|z_y^{res}|+|z_d^{res}|}.
\]

Discrimination share:

\[
C_{disc}(k)=\frac{|(z_y^{top}-z_d^{top})|}{|(z_y^{top}-z_d^{top})|+|(z_y^{res}-z_d^{res})|}.
\]

Mismatch gap:

\[
G_{mis}(k)=C_{score}(k)-C_{disc}(k).
\]

Interpretation:

- high \(C_{score}\): the band is loud;
- low \(C_{disc}\): the band is not doing the rare discrimination;
- positive \(G_{mis}\): the common band is loud but not equally useful.

## 5. Main Results

Decision rank is 4, matching the common rank.

| Condition | \(G_{mis}\) | Rare loss | System common loss | Interpretation |
|---|---:|---:|---:|---|
| shared baseline | 0.486 | 2.708 | 0.009 | strong mismatch |
| estimated split | -0.000 | 1.713 | 0.006 | mechanism supported |
| random split | 0.501 | 0.863 | 1.044 | rare loss improves, but common breaks and mismatch remains |
| oracle split | -0.008 | 1.903 | 0.004 | positive control works |
| shuffled guard | -0.000 | 2.840 | 0.006 | mismatch alone is insufficient |

Condition comparison:

| Condition | \(\Delta G_{mis}\) | Rare loss improvement | Common loss regression |
|---|---:|---:|---:|
| estimated split | 0.486 | 0.996 | -0.003 |
| random split | -0.015 | 1.845 | 1.035 |
| oracle split | 0.495 | 0.806 | -0.005 |
| shuffled guard | 0.486 | -0.131 | -0.003 |

## 6. Visualization Results

![A09 decision metrics](figures/a09_decision_metrics_short_labels.png)

Anchor question: Is the common high-gain band large but weakly discriminative, and can splitting reduce the mismatch?

Protocol question: Does the split reduce \(G_{mis}\), improve rare loss, and preserve common loss?

Metric shown: \(G_{mis}\), rare loss, and system common loss.

Data source: `tables/a09_decision_table.csv`.

What this figure decides: It checks the joint pass condition. A single metric is not enough.

Observed result: Estimated split and oracle split remove mismatch and preserve common loss. Random split lowers rare loss but keeps mismatch high and destroys common loss. Shuffled guard removes mismatch but rare loss worsens.

Allowed claim: The controlled mechanism is supported.

What this figure does not prove: Real semantic experts, real-DCLM utility, or a deployable MoE method.

Anchor update implication: Add this as controlled positive evidence for the common-band / rare-discrimination mechanism.

## 7. Stage Evidence

### Stage 1: Baseline Mismatch

Baseline at rank 4:

- \(C_{score}=0.819\);
- \(C_{disc}=0.332\);
- \(G_{mis}=0.486\).

This is the target failure pattern: the high-gain band is large in score but weaker in rare discrimination.

Rank sensitivity:

| Audit rank | Baseline \(G_{mis}\) |
|---|---:|
| 1 | 0.088 |
| 4 | 0.486 |
| 8 | 0.402 |

This matters: strict top-1 is too narrow here. The common-rank band exposes the failure better.

### Stage 2: Projector Validity

| Projector | Common alignment | Rare alignment |
|---|---:|---:|
| estimated common projector | 0.730 | 0.048 |
| oracle common projector | 1.000 | 0.000 |
| random projector | 0.062 | 0.060 |

The estimated projector is not perfect, but it is strongly common-biased and mostly avoids rare directions.

### Stage 3: Split And Controls

Estimated split:

- removes baseline common-band mismatch;
- improves rare loss;
- preserves common branch.

Random split:

- improves rare loss more than the estimated split;
- does not reduce the mismatch;
- fails common preservation.

This means rare loss alone is not valid mechanism evidence.

Shuffled guard:

- removes mismatch by projection;
- rare loss gets worse.

This means mismatch reduction alone is also not enough.

## 8. Artifact Map

Code workspace:

`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments`

Runner:

`active/synthetic_data_understanding/scripts/run_a09_common_rare_spectral_discrimination.py`

Config:

`active/synthetic_data_understanding/configs/a09_common_rare_spectral_discrimination.json`

Raw result directory:

`active/synthetic_data_understanding/results/a09_common_rare_spectral_discrimination/a09_common_rare_spectral_full_20260629_1`

Curated result directory:

`/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A09/A09_01_common_band_rare_discrimination`

Key tables:

- `tables/a09_decision_table.csv`
- `tables/a09_condition_comparison.csv`
- `tables/a09_mismatch_summary.csv`
- `tables/a09_model_summary.csv`
- `tables/a09_projector_summary.csv`
- `tables/decision_metrics.json`

Key figures:

- `figures/a09_decision_metrics_short_labels.png`
- `figures/a09_mismatch_and_rare_loss.png`

Full command:

```bash
python active/synthetic_data_understanding/scripts/run_a09_common_rare_spectral_discrimination.py \
  --config active/synthetic_data_understanding/configs/a09_common_rare_spectral_discrimination.json \
  --run-name a09_common_rare_spectral_full_20260629_1 \
  --run-stage full \
  --device cpu
```

Job id:

Not applicable. This was a local CPU run in the active execution workspace.

## 9. Claim Boundary

Supported:

- controlled common-band score dominance exists;
- the common-band mismatch is measurable;
- an estimated common/rare split can remove mismatch and preserve common behavior in this controlled setup.

Not supported:

- real language semantics;
- real-DCLM expert utility;
- preservation through real early training;
- a deployable MoE method.

## 10. Next Decision

The next useful anchor should move from controlled known directions to real activations:

> Can an analogous \(C_{score}\) / \(C_{disc}\) mismatch be measured on real model states with matched or proxy rare targets?

If not, this remains a controlled teaching result only.
