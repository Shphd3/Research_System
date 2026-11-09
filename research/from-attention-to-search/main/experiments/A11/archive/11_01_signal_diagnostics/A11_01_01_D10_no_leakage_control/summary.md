# A11_07 No-Leakage All-Position Efficiency Summary

## What We Established

A11_07 supports the refined A11 efficiency story under clean `tau=3`
all-position training: direct decision-prefix horizon-3 supervision makes
semantic recovery more stable and more readout-effective, but it is not the
only path by which all-position training can make `Z` probe-readable.

The leakage gate passed for every condition:

```text
Q(0)=0.25, M_Z(0)≈0, E_Z(0)=0, native horizon-3 accuracy at step 0 = 0.
```

Direct conditions were strongest:

- `K3_active`: reach rate 1.00, early AUC Q 0.965, final Q 1.00, native H3 1.00.
- `K2_plus_decision_prefix_L3`: reach rate 1.00, early AUC Q 0.969, final Q 1.00, native H3 1.00.

Indirect-only and non-covering controls can still recover `Z` in `Q`, but they
do not learn native `h_T -> S_Z` prediction:

- `K3_mask_decision_prefix_L3`: reach rate 0.60, early AUC Q 0.817, final Q 0.70, native H3 0.00.
- `K2_active`: reach rate 0.60, early AUC Q 0.771, final Q 0.85, native H3 0.00.
- `K1_fixed_3head`: reach rate 0.60, early AUC Q 0.838, final Q 0.85, native H3 0.05, but it does not train `Y2`.

## Terminology / Definitions

| Term | Plain meaning | Concrete object / formula | Why it matters | Cannot prove |
|---|---|---|---|---|
| direct decision-prefix L3 | current `h_T` directly predicts `S_Z` | $\lambda_3\operatorname{CE}(q_3(\cdot\mid h_T),S_Z)$ | tests the proposed efficiency mechanism | only possible recovery path |
| indirect transfer | other all-position losses make `Z` readable from `h_T` | shared-parameter updates outside direct `h_T -> S_Z` | explains K1/K2/masked recovery | direct native prediction |
| `Q(t)` | guarded semantic recovery | $Q(t)=\min\{A(t),P(t),S(t)\}$ | primary multi-step recovery metric | native model prediction |
| `T_0.9` | time-to-reliable recovery | first eval where `Q>=0.9` for 3 consecutive evals | speed and stability | final capability alone |
| early AUC Q | early recovery area | average `Q(t)` over steps 0-3000 | early efficiency | causal gradient source |
| `M_Z_ref` | fixed readout-effective semantic margin | $\frac1m\sum_z(u^0_{S_z}-\bar u^0)^\top h_z$ | links A11_07 to A11_06 | current output-head adaptation |
| native H3 accuracy | direct model prediction of `S_Z` from `h_T` | $\Pr[\arg\max q_3(\cdot\mid h_T)=S_Z]$ | distinguishes direct prediction from probe-readable `Q` | downstream utility |

`A(t)` is suffix-decoder accuracy from frozen `h_T` to `Z`; `P(t)` is an
independent frozen probe; `S(t)` is branch-swap consistency.

## Conditions

| Condition | Loss scope | Role |
|---|---|---|
| `K1_fixed_3head` | all-position offset 1 only | NTP baseline with matched heads |
| `K2_active` | all-position offsets 1 and 2 | non-covering MTP baseline |
| `K3_active` | all-position offsets 1, 2, and 3 | full direct + indirect condition |
| `K3_mask_decision_prefix_L3` | K3 all-position but removes only direct `h_T -> S_Z` | indirect-only K3 control |
| `K2_plus_decision_prefix_L3` | K2 all-position plus direct `h_T -> S_Z` | direct-term sufficiency test |

Run:

```text
job id: pt-nkdwrd8k
run name: a11_07_no_leakage_all_position_efficiency_4gpu_20260708_170032
scope: all-position LM-style training
seeds: 971, 972, 973, 974, 975
steps: 15000
eval interval: 250
```

## Main Result Table

| Condition | Reach rate | Mean reached `T_0.9` | Early AUC Q | Full AUC Q | Final Q | Native H3 | Early AUC `M_Z_ref` | Final `M_Z_ref` | Final `E_Z` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| K1 fixed 3-head | 0.60 | 250 | 0.838 | 0.834 | 0.85 | 0.05 | 0.001 | -0.000 | 0.002 |
| K2 active | 0.60 | 333 | 0.771 | 0.731 | 0.85 | 0.00 | -0.000 | -0.000 | 0.005 |
| K2 plus direct L3 | 1.00 | 250 | 0.969 | 0.994 | 1.00 | 1.00 | 3.381 | 3.735 | 82.573 |
| K3 full | 1.00 | 300 | 0.965 | 0.993 | 1.00 | 1.00 | 1.888 | 2.430 | 50.922 |
| K3 masked direct L3 | 0.60 | 833 | 0.817 | 0.750 | 0.70 | 0.00 | 0.005 | 0.004 | 0.010 |

## Comparisons

### Direct-Term Sufficiency

Compare `K2_active` with `K2_plus_decision_prefix_L3`.

Adding only the direct decision-prefix horizon-3 term improves:

- reach rate: +0.40;
- reached-only `T_0.9`: 333 -> 250;
- early AUC Q: +0.198;
- full AUC Q: +0.263;
- final Q: +0.15;
- native H3 accuracy: +1.00;
- final `M_Z_ref`: +3.735.

This supports the claim that the direct term is sufficient to create the main
K3-like efficiency pattern.

### Direct-Term Necessity Within K3

Compare `K3_active` with `K3_mask_decision_prefix_L3`.

Removing only direct `h_T -> S_Z` from K3 weakens:

- reach rate: 1.00 -> 0.60;
- reached-only `T_0.9`: 300 -> 833;
- early AUC Q: 0.965 -> 0.817;
- final Q: 1.00 -> 0.70;
- native H3 accuracy: 1.00 -> 0.00;
- final `M_Z_ref`: 2.430 -> 0.004.

This supports direct horizon-3 supervision as a mechanism component. It also
shows that masked K3 can still recover some probe-readable `Z` through
indirect transfer, so direct supervision is not the only all-position path.

### Full K Comparison

K3 full is stronger than K2 active and K1 fixed in native H3 and readout margin.
However, K1/K2 can still reach high `Q` in several seeds. Therefore the allowed
claim is not "K1/K2 cannot learn `Z`"; the allowed claim is that direct
horizon-3 supervision gives stronger native readout and more stable recovery.

## Visualized Results

### Guarded Recovery Curves

![Guarded recovery curves](figures/q_curves.png)

This figure tests multi-step recovery efficiency. Direct conditions quickly
reach and keep `Q=1`. Non-direct controls can recover but are less stable and
lower on average.

### Readout-Effective Margin Curves

![Readout margin curves](figures/margin_curves.png)

This figure tests whether A11_06's margin mechanism appears in all-position
training. Direct conditions have large positive `M_Z_ref`; non-direct controls
stay near zero.

### Final Q Versus Native H3

![Final Q versus native H3](figures/final_q_vs_native_h3.png)

This figure separates probe-readable recovery from native direct prediction.
K1/K2 and masked K3 can have nontrivial final Q, but native H3 remains near or
at zero. Direct conditions have both final Q and native H3 at 1.0.

### Local Guard

![Local guard accuracy](figures/local_guard_accuracy.png)

K2, K3, masked K3, and K2 plus direct L3 preserve local `Y1/Y2` learning. K1
only trains `Y1`, so its `Y2` accuracy is not expected to pass.

## Hypothesis Update

Supported:

```text
Direct decision-prefix informative-horizon supervision improves semantic
recovery efficiency and native horizon-3 readout under no-leakage clean tau=3
all-position training.
```

Refined:

```text
All-position indirect transfer is strong enough that K1/K2 or masked K3 can
make Z probe-readable. Q alone is therefore not direct-supervision evidence.
Native H3 and M_Z_ref are required to identify the direct path.
```

Not supported:

```text
Only K3 can recover Z.
K larger is necessarily better.
The result proves natural-language MTP benefit or MoE expert utility.
```

## Artifacts

- Runner: `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a11_03_04_semantic_efficiency.py`
- Config: `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a11_07_no_leakage_all_position_efficiency.json`
- Remote result: `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a11_07_no_leakage_all_position_efficiency/a11_07_no_leakage_all_position_efficiency_4gpu_20260708_170032/`
- Curated tables: `tables/`
- Figures: `figures/`
