# Detailed: A11_03 K=2 Semantic Efficiency

Status: completed on 2026-07-07.

## Decision

The experiment supports a narrow K=2 learning-efficiency claim. In the clean branch-delayed task, next-two improves guarded branch recovery over matched fixed-next-one while preserving immediate next-token learning. The main boundary is acquisition instability: the direct signal is useful but not always optimized successfully.

## Terminology / Definitions

| Term | Plain meaning | Concrete object or computation | Unit / formula | Why it matters | What it cannot prove |
| --- | --- | --- | --- | --- | --- |
| $Z$ | early branch variable | branch index in `BR_z` | categorical | controlled delayed cause | real semantics |
| $h_T$ | decision-prefix hidden state | final prefix state before targets | vector | representation being tested | all model states |
| $L_1$ | immediate next-token loss | CE for $Y_1$ | nats / CE | local learning guard | long-horizon learning |
| $L_2$ | second-token loss | CE for $Y_2$ | nats / CE | candidate MTP branch signal | universal auxiliary benefit |
| $Q_{\mathrm{eval}}$ | guarded recovery score | $\min\{A_{\mathrm{eval}},P_{\mathrm{eval}},S_{\mathrm{eval}}\}$ | accuracy score | primary branch-recovery evidence | full causal mechanism |
| `AUC_Q` | average guarded recovery over checkpoints | mean of checkpoint $Q_{\mathrm{eval}}$ | score | efficiency over training | threshold timing by itself |
| `T_0.9_eval` | time to guarded recovery | first consecutive checkpoint with $Q_{\mathrm{eval}}\ge0.9$ | steps | primary pass/fail timing | asymptotic ability |

## Theory Clause Tested

The K=2 clean construction sets:

$$
Y_1=A,\qquad Y_2=S_Z,
$$

so:

$$
I(Z;Y_1)=0,\qquad I(Z;Y_2\mid Y_1)=H(Z).
$$

The tested objective contrast is:

$$
L_{\mathrm{fixed1}}=L_1,\qquad
L_{\mathrm{next2}}=L_1+\lambda L_2.
$$

If the next-two signal is useful for learning, then $h_T$ should expose $Z$ earlier under $L_{\mathrm{next2}}$ than under $L_{\mathrm{fixed1}}$.

## Data Audit

Representative generated rows:

| Regime | Branch | Prefix | Targets |
| --- | ---: | --- | --- |
| clean | 0 | `BR_0 F_00 ... F_15 U_00 U_01 U_02 U_03` | `A_SHARED S_0` |
| clean | 1 | `BR_1 F_00 ... F_15 U_00 U_01 U_02 U_03` | `A_SHARED S_1` |
| noisy | 0 | `BR_0 F_00 ... F_15 U_00 U_01 U_02 U_03` | `A_SHARED NOISE_12` |
| redundant | 0 | `BR_0 F_00 ... F_15 U_00 U_01 U_02 U_03` | `S_0 T_0` |

Clean is the main long-horizon test. Noisy and redundant are controls.

## Experimental Setup

Run configuration:

| Item | Value |
| --- | --- |
| Objective scope | `decision_only` |
| Model | one-layer one-head Transformer |
| Hidden size | `d_model=64` |
| Branches | `4` |
| Filler length | `16` |
| Shared context length | `4` |
| Seeds | `971,972,973,974,975` |
| Initializations | `identical_branch`, `random` |
| Conditions | `fixed_next_one_2head`, `shared_trunk_next_two` |
| Regimes | clean, noisy, redundant |
| Remote quota | reserved 4-GPU |
| Job id | `pt-m5foezfm` |

## Main Tables

Full condition means:

| Regime | Condition | Init | n | Mean reached step | Reach rate | AUC $Q$ | Final $Q$ | Eval suffix | Probe | Swap | $Y_1$ acc | $Y_2$ acc | Native informative acc |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| clean | fixed next-one | identical | 5 | NA | 0.00 | 0.250 | 0.250 | 0.250 | 0.250 | 0.250 | 1.000 | 0.000 | NA |
| clean | fixed next-one | random | 5 | NA | 0.00 | 0.288 | 0.250 | 0.250 | 0.250 | 0.250 | 1.000 | 0.000 | NA |
| clean | next-two | identical | 5 | 1500 | 0.40 | 0.536 | 0.550 | 0.550 | 0.550 | 0.550 | 1.000 | 0.550 | 0.550 |
| clean | next-two | random | 5 | 1000 | 0.80 | 0.895 | 0.900 | 0.900 | 0.900 | 0.900 | 1.000 | 0.900 | 0.900 |
| noisy | fixed next-one | identical | 5 | NA | 0.00 | 0.250 | 0.250 | 0.250 | 0.250 | 0.250 | 1.000 | 0.025 | NA |
| noisy | fixed next-one | random | 5 | NA | 0.00 | 0.288 | 0.250 | 0.250 | 0.250 | 0.250 | 1.000 | 0.025 | NA |
| noisy | next-two | identical | 5 | NA | 0.00 | 0.257 | 0.250 | 0.250 | 0.250 | 0.250 | 1.000 | 0.048 | NA |
| noisy | next-two | random | 5 | 1000 | 0.20 | 0.436 | 0.350 | 0.400 | 0.350 | 0.400 | 1.000 | 0.048 | NA |
| redundant | fixed next-one | identical | 5 | 1500 | 0.80 | 0.821 | 0.850 | 0.850 | 0.850 | 0.850 | 0.850 | 0.000 | NA |
| redundant | fixed next-one | random | 5 | 1000 | 1.00 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | NA |
| redundant | next-two | identical | 5 | 1500 | 0.80 | 0.907 | 0.950 | 0.950 | 0.950 | 0.950 | 0.950 | 0.950 | 0.950 |
| redundant | next-two | random | 5 | 1000 | 1.00 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

Clean decision contrasts:

| Init | Contrast | $\Delta$ AUC $Q$ | $\Delta$ final $Q$ | $\Delta$ reach rate |
| --- | --- | ---: | ---: | ---: |
| identical | next-two minus fixed next-one | +0.286 | +0.300 | +0.400 |
| random | next-two minus fixed next-one | +0.607 | +0.650 | +0.800 |

## Hypothesis Audit

| Hypothesis | Result | Judgment |
| --- | --- | --- |
| H1: next-two improves recovery efficiency | Clean next-two improves AUC $Q$ and reach rate over fixed next-one | supported with instability |
| H2: next-two preserves $Y_1$ | Clean $Y_1$ accuracy is `1.00` for both conditions | supported |
| H3: noisy future targets do not mimic clean branch signal | noisy identical-init stays chance; noisy random-init weakly rises | partially supported; random-init false-positive risk remains |
| H4: redundant condition is not long-horizon evidence | redundant fixed next-one also recovers branch because $Y_1=S_Z$ | supported |

## Visualization Results

No standalone figure is promoted for this result. The central evidence is the condition-summary table above because the decision depends on exact threshold reach rates, AUC $Q$, final $Q$, and local guards. The table answers whether next-two changes branch recovery over training; it does not show natural-language transfer or all-position behavior.

## Interpretation

The K=2 theory says that low next-two loss requires $h_T$ to contain information about $Z$ when $Y_2=S_Z$ and $Y_1$ is shared. A11_03 adds a training-efficiency layer: in the clean task, this representation pressure is not only a final-state requirement; it also improves early guarded recovery compared with matched fixed-next-one.

However, the result is not a proof that MTP always optimizes better. Identical-branch next-two succeeds in only 2 of 5 seeds, so the correct phrasing is: the K=2 MTP objective supplies useful direct supervision that can improve acquisition, but shared-trunk optimization can still fail.

## Claim Boundary

Can claim:

- controlled K=2 decision-only next-two improves guarded branch recovery over matched fixed next-one;
- the gain is measured on $h_T$ branch recoverability, not natural-language loss;
- $Y_1$ learning is preserved in the clean runs.

Cannot claim:

- universal MTP superiority;
- NTP impossibility in all settings;
- K>2 coverage without A11_04;
- all-position efficiency;
- random-init evidence without leakage caution.

## Artifact Map

| Artifact | Path |
| --- | --- |
| Protocol | `Projects/from-attention-to-search/main/experiments/A11/A11_03_k2_semantic_efficiency/protocol.md` |
| Summary | `Projects/from-attention-to-search/main/experiments/A11/A11_03_k2_semantic_efficiency/summary.md` |
| Runner | `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a11_03_04_semantic_efficiency.py` |
| Config | `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a11_03_k2_semantic_efficiency.json` |
| Result dir | `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a11_03_k2_semantic_efficiency/a11_03_k2_efficiency_decision_only_4gpu_20260707_1708` |
| Main table | `tables/condition_summary.csv` |
| Contrast table | `tables/decision_contrasts.csv` |
| Per-seed table | `tables/efficiency_by_seed.csv` |
| Sample audit | `tables/sample_table.csv` |
| Curated local tables | `Projects/from-attention-to-search/main/experiments/A11/A11_03_k2_semantic_efficiency/tables/` |
| Log dir | `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/logs/acp/a11_03_k2_efficiency_decision_only_4gpu_20260707_1708` |
| Remote job | `pt-m5foezfm` |
