# A11_07 No-Leakage All-Position Efficiency Detailed Record

## Conclusion

A11_07 gives partial-to-strong support for the all-position efficiency claim,
with an important boundary. Under a clean no-leakage `tau=3` setup, direct
decision-prefix horizon-3 supervision improves reach rate, early AUC, final Q,
native H3 prediction, and fixed readout-effective margin. But all-position
indirect transfer remains real: non-direct conditions can make `Z`
probe-readable, so `Q` alone cannot identify direct supervision.

## Protocol Compliance

| Protocol item | Status | Evidence |
|---|---|---|
| clean `tau=3` data | passed | `sample_table.csv` |
| all-position LM-style training | passed | config `objective_scopes=["all_positions_lm_control"]` |
| no broader K sweep | passed | K1/K2/K3 plus two direct-term controls only |
| no filler/lambda sweep | passed | filler length 16, `lambda3=1.0` |
| seeds 971-975 | passed | 5 seeds per condition |
| leakage gate | passed | all conditions have `Q(0)=0.25`, `M_Z(0)\approx0`, `E_Z(0)=0`, native H3 0 |
| local guard | passed for conditions that train Y1/Y2 | K2/K3/direct/masked final Y1/Y2 accuracy 1.0 |

## Metrics

### Guarded Recovery

$$
Q(t)=\min\{A(t),P(t),S(t)\}.
$$

`A(t)` is suffix-decoder accuracy from frozen `h_T` to `Z`; `P(t)` is an
independent frozen probe; `S(t)` is branch-swap consistency. It measures
conservative probe-readable recovery, not native model prediction.

### Time To Reliable Recovery

$$
T_{0.9}=\min\{t_i:Q(t_i),Q(t_{i+1}),Q(t_{i+2})\ge0.9\}.
$$

This measures speed and stability. If a seed never reaches the threshold, it is
excluded from the reached-only mean and counted against reach rate.

### Early AUC

$$
\operatorname{AUC}_{early}=\frac{1}{3000}\int_0^{3000} Q(t)\,dt.
$$

This measures early recovery strength without relying only on a threshold.

### Fixed Readout-Effective Margin

$$
M_Z^{ref}(t)=\frac1m\sum_z(u^0_{S_z}-\bar u^0)^\top h_T(z,t).
$$

This links A11_07 back to A11_06. It checks whether the hidden state moves in a
direction readable by the initial horizon-3 output rows. It does not use
current head movement.

### Native Horizon-3 Accuracy

$$
\Pr[\arg\max q_3(\cdot\mid h_T)=S_Z].
$$

This separates direct model prediction from external probe-readable recovery.

### Local Guard

Local guard records native `Y1/Y2` CE and accuracy at `h_T`. It tests whether
semantic recovery sacrifices the branch-shared local targets. K1 does not train
`Y2`, so its `Y2` failure is expected and is not a failure of the direct-term
comparison.

## Main Results

Source: `tables/condition_summary.csv`.

| Condition | Reach rate | Mean reached `T_0.9` | Early AUC Q | Full AUC Q | Final Q | Native H3 | Early AUC `M_Z_ref` | Final `M_Z_ref` | Final `E_Z` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| K1 fixed 3-head | 0.60 | 250 | 0.838 | 0.834 | 0.85 | 0.05 | 0.001 | -0.000 | 0.002 |
| K2 active | 0.60 | 333 | 0.771 | 0.731 | 0.85 | 0.00 | -0.000 | -0.000 | 0.005 |
| K2 plus direct L3 | 1.00 | 250 | 0.969 | 0.994 | 1.00 | 1.00 | 3.381 | 3.735 | 82.573 |
| K3 full | 1.00 | 300 | 0.965 | 0.993 | 1.00 | 1.00 | 1.888 | 2.430 | 50.922 |
| K3 masked direct L3 | 0.60 | 833 | 0.817 | 0.750 | 0.70 | 0.00 | 0.005 | 0.004 | 0.010 |

## Seed-Level Notes

Source: `tables/efficiency_by_seed.csv`.

- `K3_active`: all 5 seeds reach threshold; four seeds reach at step 250, one
  at step 500.
- `K2_plus_decision_prefix_L3`: all 5 seeds reach threshold at step 250.
- `K3_mask_decision_prefix_L3`: 3 of 5 seeds reach; reached seeds have steps
  250, 250, and 2000; final native H3 is 0 for every seed.
- `K2_active`: 3 of 5 seeds reach; final native H3 is 0 for every seed.
- `K1_fixed_3head`: 3 of 5 seeds reach, but `Y2` is not trained and native H3
  is near zero.

## Comparisons And Interpretation

### Direct-Term Sufficiency

`K2_plus_decision_prefix_L3` versus `K2_active`:

| Metric | Delta |
|---|---:|
| reach rate | +0.40 |
| reached-only `T_0.9` | -83 steps |
| early AUC Q | +0.198 |
| full AUC Q | +0.263 |
| final Q | +0.15 |
| native H3 | +1.00 |
| final `M_Z_ref` | +3.735 |

Interpretation: adding only the direct decision-prefix L3 term is sufficient
to produce the K3-like pattern.

### Direct-Term Necessity Within K3

`K3_active` versus `K3_mask_decision_prefix_L3`:

| Metric | Delta |
|---|---:|
| reach rate | +0.40 |
| reached-only `T_0.9` | -533 steps |
| early AUC Q | +0.148 |
| full AUC Q | +0.243 |
| final Q | +0.30 |
| native H3 | +1.00 |
| final `M_Z_ref` | +2.426 |

Interpretation: removing only the direct decision-prefix L3 term strongly
weakens direct readout and stability. However, masked K3 can still recover
some `Q`, proving that indirect transfer remains a live path.

### Full K Comparison

K3 full outperforms K2 active in reach rate, early AUC, final Q, native H3, and
readout margin. K3 full also outperforms K1 in native H3 and readout margin, but
K1 has surprisingly high `Q` in some seeds. This is a boundary result: `Q` can
measure probe-readable branch recovery through indirect training, but it does
not prove direct horizon-3 prediction.

## Visualization Results

### Q Curves

![Guarded recovery curves](figures/q_curves.png)

Purpose: compare semantic recovery speed and stability.  
Observed result: direct conditions quickly reach and stay at `Q=1`; non-direct
conditions are weaker and less stable.  
Take-home: direct supervision improves multi-step guarded recovery, but
indirect transfer is not absent.

### Readout Margin Curves

![Readout margin curves](figures/margin_curves.png)

Purpose: test whether A11_06's readout-margin mechanism appears in all-position
training.  
Observed result: direct conditions show large positive `M_Z_ref`; non-direct
conditions remain near zero.  
Take-home: the direct path is visible in hidden-state geometry.

### Native H3 Curves

![Native H3 curves](figures/native_h3_curves.png)

Purpose: distinguish direct native prediction from `Q`.  
Observed result: direct conditions reach native H3 accuracy 1.0; non-direct
conditions remain at or near 0.  
Take-home: probe-readable recovery is not equivalent to native direct
prediction.

### Final Q Versus Native H3

![Final Q versus native H3](figures/final_q_vs_native_h3.png)

Purpose: show the boundary of `Q`.  
Observed result: K1/K2/masked K3 can have nontrivial final Q while native H3 is
0 or near 0.  
Take-home: future reports should not use `Q` alone as evidence for direct
semantic supervision.

### Local Guard

![Local guard accuracy](figures/local_guard_accuracy.png)

Purpose: check whether direct semantic recovery damages local targets.  
Observed result: K2, K3, masked K3, and K2 plus direct L3 all preserve final
Y1/Y2 accuracy at 1.0. K1 fails Y2 because it does not train offset 2.  
Take-home: direct horizon-3 supervision does not sacrifice local Y1/Y2 learning
in the tested setup.

## Self-Checks

1. Full run completeness: 25 condition-seed curves, 61 evals each, 1525 curve
   rows total.
2. No missing `Q`, `M_Z_ref`, or `E_Z` values.
3. All step-0 leakage metrics are at chance or zero.
4. Native H3 is recorded for every condition, including non-active H3 controls.
5. The result reproduces the A11_05 direct-term pattern while removing the
   random-initialization leakage issue.

## Artifact Map

| Object | Path |
|---|---|
| Job id | `pt-nkdwrd8k` |
| Remote result | `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a11_07_no_leakage_all_position_efficiency/a11_07_no_leakage_all_position_efficiency_4gpu_20260708_170032/` |
| Remote logs | `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/logs/acp/a11_07_no_leakage_all_position_efficiency_4gpu_20260708_170032/` |
| Config | `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a11_07_no_leakage_all_position_efficiency.json` |
| Runner | `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a11_03_04_semantic_efficiency.py` |
| Curated tables | `tables/` |
| Figures | `figures/` |

## Claim Boundary

Can claim:

```text
Under no-leakage clean tau=3 all-position training, direct decision-prefix
informative-horizon supervision improves native horizon-3 prediction,
readout-effective margin, and guarded-recovery stability beyond indirect-only
controls.
```

Cannot claim:

```text
K1/K2 cannot recover Z.
Q alone proves direct supervision.
This proves natural-language MTP benefit.
This proves MoE routing preservation or expert utility.
```

Next decision: update the A11 storyline. A future bridge to MoE routing should
use `M_Z_ref` or native H3-like direct readout, not `Q` alone, as the semantic
state evidence.
