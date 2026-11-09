# A11_06 Readout-Effective Margin Efficiency Detailed Record

## Conclusion

A11_06 passes as a first-order mechanism diagnostic. The decisive metric is
activation-space readout-effective hidden margin velocity:

$$
G_M^{hidden}=\frac{1}{m}\sum_z (u^0_{S_z}-\bar u^0)^\top(-\nabla_{h_z}L_K).
$$

K3 has positive velocity; K1/K2 are zero up to numerical precision. This is the
closest implementation of the theorem's gradient-flow claim. Parameter-space
finite differences are retained as a self-check but are too small and unstable
to be the primary metric in this Transformer parameterization.

## Protocol Compliance

| Protocol item | Status | Evidence |
|---|---|---|
| clean `tau=3` data | passed | `sample_table.csv`; `Y1=A`, `Y2=C`, `Y3=S_Z` |
| decision-only objective | passed | config `objective_scopes=["decision_only"]` |
| K1/K2/K3 only | passed | `condition_summary.csv` |
| seeds 971-975 | passed | `efficiency_by_seed.csv`, 5 seeds per condition |
| one-step diagnostic | passed | `one_step_metrics.csv`, `one_step_summary.csv` |
| leakage gate | passed | `Q(0)=0.25`, `M_Z(0)\approx0`, `E_Z(0)=0` |
| local Y1/Y2 guard | passed for active local targets | CE decreases after one step |

## Metrics

### Fixed Readout-Effective Margin

$$
M_Z^{ref}(h)=\frac1m\sum_z (u^0_{S_z}-\bar u^0)^\top h_z.
$$

It measures whether hidden states move toward the output directions that
initially correspond to the correct delayed token. It does not measure current
head adaptation; `M_Z_current` is recorded separately for that.

### Hidden Gradient Velocity

$$
G_M^{hidden}=\frac{d}{ds}M_Z^{ref}(h(s))\bigg|_{s=0},
\qquad \dot h_z=-\nabla_{h_z}L_K.
$$

This is the primary metric for A11_06. It directly tests whether the active
loss creates a semantic update direction at the decision hidden state.

### Branch Separation Energy

$$
E_Z(h)=\frac{1}{2m^2}\sum_{z,z'}\|h_z-h_{z'}\|^2.
$$

This is a secondary metric. It can show branch separation, but separation alone
does not prove that the model's output head can use the separated direction.

### Guarded Recovery

$$
Q(t)=\min\{A(t),P(t),S(t)\}.
$$

`A(t)` is frozen suffix-decoder accuracy from `h_T` to `Z`; `P(t)` is an
independent frozen linear probe; `S(t)` is branch-swap consistency. `Q` guards
against one-readout artifacts, but it is not a proof of the exact optimization
path.

## Main Tables

### One-Step Summary

Source: `tables/one_step_summary.csv`.

| Condition | Eta | `G_M_hidden` | `G_E_velocity` | `Delta M / eta` | `Delta Y1 CE` | `Delta Y2 CE` |
|---|---:|---:|---:|---:|---:|---:|
| K1 fixed 3-head | 0.0003 | `7.28e-12` | 0.00000 | 0.000027 | -0.024084 | -0.000205 |
| K2 active | 0.0003 | `-1.16e-11` | 0.00000 | 0.000032 | -0.024295 | -0.024185 |
| K3 active | 0.0003 | 0.003816 | 0.000060 | -0.000705 | -0.024303 | -0.024243 |

The sign pattern is stable in `G_M_hidden`: K1/K2 are zero, K3 is positive.
The finite-difference parameter margin is not stable and should not be used as
the theorem-facing metric.

### Short Curve Summary

Source: `tables/condition_summary.csv`.

| Condition | Reach rate | Mean reached `T_0.9` | Early AUC Q | Final Q | Final `M_Z_ref` | Final `E_Z` |
|---|---:|---:|---:|---:|---:|---:|
| K1 fixed 3-head | 0.00 | NA | 0.250 | 0.25 | 0.000000 | 0.000 |
| K2 active | 0.00 | NA | 0.250 | 0.25 | -0.000000 | 0.000 |
| K3 active | 0.40 | 100 | 0.535 | 0.55 | 1.356 | 22.649 |

## Visualization Results

### One-Step Hidden Margin

![One-step hidden readout-margin velocity](figures/one_step_hidden_margin.png)

Purpose: test the first-order hidden-state update direction.  
Observed result: only K3 has positive velocity.  
Take-home: the informative horizon creates the direct semantic update at
`h_T`.  
Limitation: this is activation-space, not a full sample-complexity theorem.

### Q Curves

![Short guarded recovery curves](figures/q_curves.png)

Purpose: check whether the one-step mechanism appears in short training.  
Observed result: K3 rises above K1/K2; K1/K2 remain at chance.  
Take-home: short-run behavior is consistent with the one-step mechanism.  
Limitation: short decision-only curves do not decide all-position indirect
transfer.

### Margin Curves

![Readout margin curves](figures/margin_curves.png)

Purpose: show the trajectory of `M_Z_ref`.  
Observed result: K3 grows; K1/K2 remain near zero.  
Take-home: K3 moves `h_T` into the fixed readout direction.

## Self-Checks

1. Full run completeness: 15 condition-seed curves, 21 evals each; 45
   one-step rows.
2. No missing `Q`, `M_Z_ref`, or `E_Z` values.
3. Step-0 leakage gate passed for all conditions.
4. Parameter finite difference was inspected and found numerically unstable;
   the report therefore uses `G_M_hidden` as the theorem-facing metric.

## Artifact Map

| Object | Path |
|---|---|
| Job id | `pt-57nu5dv1` |
| Remote result | `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a11_06_readout_effective_margin_efficiency/a11_06_readout_effective_margin_efficiency_4gpu_20260708_165829/` |
| Remote logs | `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/logs/acp/a11_06_readout_effective_margin_efficiency_4gpu_20260708_165829/` |
| Config | `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a11_06_readout_effective_margin_efficiency.json` |
| Runner | `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a11_03_04_semantic_efficiency.py` |
| Curated tables | `tables/` |
| Figures | `figures/` |

## Claim Boundary

A11_06 supports a first-order mechanism claim, not the full all-position
learning-efficiency claim. A11_07 is needed to test whether the mechanism
survives under all-position indirect transfer.
