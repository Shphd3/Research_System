# A11_08 General-K Readout-Margin Dynamics Detailed Record

## Conclusion

A11_08 supports the minimal general-K vector-sum mechanism and does not falsify
the anchor. With fixed `K=4`, fixed active loss count, and fixed two informative
horizons, the aligned output geometry produces high hidden-state semantic
velocity, while the low/conflicting geometry produces low velocity. The result
is seed-stable and passes the zero, positive, geometry, and local-language
guards.

This is a first-order synthetic mechanism result. It should be used to decide
the next-K inclusion-law anchor, not a MoE bridge yet.

## Terminology / Definitions

| Term | Plain meaning | Concrete object or computation | Unit / formula | Why it matters | Cannot prove |
|---|---|---|---|---|---|
| Early variable `Z` | Prefix branch information | Synthetic branch id, four classes | Categorical | Controlled semantic variable | Natural language meaning |
| Current state `h_T` | Hidden state after the decision prefix | Transformer hidden vector at the decision site | Vector | Object being updated by future-token losses | All-position behavior |
| Horizon `j` | A future prediction offset | `Y_j` predicted from `h_T` | Offset index | Defines which future target enters the objective | Natural discourse horizon |
| Informative horizon | A future target that one-to-one encodes `Z` | `Y_j=S_z` or `Y_j=T_z` | Set membership in `I_K` | Should create branch-specific update | Utility of the token |
| Centered output row | Correct output row after subtracting branch mean | `u_{j,z}-bar u_j` | Vector | Removes common update direction | Downstream accuracy |
| Aggregate semantic direction | Sum of covered informative centered rows | $v_z^{(K)}=\sum_{j\in I_K}\lambda_j(u_{j,z}-\bar u_j)$ | Vector | The mechanism model's core object | Multi-step convergence |
| Predicted geometry score | Expected first-order score from output rows | $G_K^{pred}=\frac1{m^2}\sum_z\|v_z^{(K)}\|^2$ | Scalar | Precondition for interpreting the falsifier | Observed optimization |
| Batch-scaled predicted score | Geometry score after full-batch CE averaging | $G_{K,batch}^{pred}=G_K^{pred}/n_{branch}$ | Scalar | Matches implementation loss reduction | Theory without batch scaling |
| Hidden-gradient semantic velocity | Observed activation-space movement toward `v_z^(K)` | $G_K^{hidden}=\frac1m\sum_z v_z^{(K)\top}(-\nabla_{h_z}L_K)$ | Scalar | Primary decision metric | Parameter-space learning speed |
| Finite-difference margin velocity | Margin change after one small parameter step | $\Delta M_K/\eta$ | Scalar / learning-rate unit | Auxiliary implementation check | Primary mechanism if unstable |
| `Q_eval` | Conservative readability of `Z` from `h_T` | $\min\{A(t),P(t),S(t)\}$ | Accuracy | Secondary semantic-state guard | Direct supervision |
| `A(t)` | Suffix decoder accuracy | Linear classifier from frozen `h_T` to `Z` | Accuracy | One readability check | Causality |
| `P(t)` | Independent probe accuracy | Separate linear probe from frozen `h_T` to `Z` | Accuracy | Reduces decoder overfit concern | Causality |
| `S(t)` | Branch-swap consistency | Whether suffix decoder reacts consistently under branch swaps | Accuracy / consistency | Guards shortcut decoding | Full invariance |
| Local guard | Whether shared targets remain learned | `Y1`, `Y2` CE and accuracy | CE / accuracy | Rules out local-target damage | Full LM quality |

## Decision Question

Does first-order readout-effective semantic margin under next-K prediction equal
the contribution predicted by the active informative horizons?

For A11_08, the sharp falsifier is:

```text
same K=4
same active horizons {1,2,3,4}
same two informative horizons {3,4}
different centered output-row geometry at horizon 4
```

If output geometry predicts `aligned_h3_h4` should exceed
`low_conflict_h3_h4`, but observed hidden-gradient semantic velocity does not
separate them, then the minimal general-K vector-sum mechanism is falsified or
strongly weakened.

## Exact Setup

Data template:

```text
BR_z F00 ... F15 U00 U01 U02 U03 Y1 Y2 Y3 Y4 STOP
```

Conditions:

| Condition | `Y1` | `Y2` | `Y3` | `Y4` | Informative horizons | Role |
|---|---|---|---|---|---|---|
| `shared_only_k4` | `A` | `C` | `A` | `C` | none | zero guard |
| `single_h3` | `A` | `C` | `S_z` | `A` | 3 | positive control |
| `aligned_h3_h4` | `A` | `C` | `S_z` | `T_z` | 3, 4 | aligned vector-sum case |
| `low_conflict_h3_h4` | `A` | `C` | `S_z` | `T_z` | 3, 4 | low/conflicting vector-sum case |

Configuration:

| Item | Value |
|---|---|
| Experiment id | `A11_08_general_k_readout_margin_dynamics` |
| Run name | `a11_08_general_k_readout_margin_full_20260709_051147` |
| Scope | decision-only |
| Branch count `m` | 4 |
| Train samples per branch | 16 |
| Eval samples per branch | 64 |
| Filler length | 16 |
| Shared context length | 4 |
| Noise vocab size | 16 |
| `Kmax` | 4 |
| Active horizons | `{1,2,3,4}` |
| Horizon weights | all 1.0 |
| Seeds | `971, 972, 973, 974, 975` |
| Model | one layer, `d_model=64`, one attention head, dropout 0 |
| Optimizer setting | learning rate 0.003, weight decay 0 |
| Training length | 2000 steps |
| Evaluation interval | 100 steps |
| One-step etas | `1e-4`, `3e-4`, `1e-3` |
| Decoder / probe | 200 steps, learning rate 0.05, weight decay 0.001 |

Implementation note: `aligned_h3_h4` copies the centered horizon-3 semantic
rows into the horizon-4 semantic rows. `low_conflict_h3_h4` sets the horizon-4
centered rows in a low/conflicting direction. This geometry-controlled
construction is intentional because random target-code permutation may fail to
create a decisive geometry gap in high dimension.

## Run Record

Execution workspace:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments
```

Primary commands:

```text
RUN_NAME=a11_08_general_k_readout_margin_full_20260709_051147

python active/synthetic_data_understanding/scripts/run_a11_03_04_semantic_efficiency.py \
  --config active/synthetic_data_understanding/configs/a11_08_general_k_readout_margin_dynamics.json \
  --run-name "$RUN_NAME" --device cuda:0 --num-shards 2 --shard-index 0

python active/synthetic_data_understanding/scripts/run_a11_03_04_semantic_efficiency.py \
  --config active/synthetic_data_understanding/configs/a11_08_general_k_readout_margin_dynamics.json \
  --run-name "$RUN_NAME" --device cuda:1 --num-shards 2 --shard-index 1

python active/synthetic_data_understanding/scripts/run_a11_03_04_semantic_efficiency.py \
  --config active/synthetic_data_understanding/configs/a11_08_general_k_readout_margin_dynamics.json \
  --run-name "$RUN_NAME" --device cuda --aggregate-only
```

Job id: local CUDA run, no SCO/ACP job id.

Smoke check before full run: seed 971 produced the expected direction
`aligned > single > low/conflict > shared`, and the geometry precondition was
valid. Full run then used all five seeds.

## Metric Formulas

Primary geometry prediction:

$$
v_z^{(K)}=\sum_{j\in I_K}\lambda_j(u_{j,z}-\bar u_j)
$$

$$
G_K^{pred}=\frac1{m^2}\sum_z\|v_z^{(K)}\|^2
$$

Implementation batch-scaled prediction:

$$
G_{K,batch}^{pred}=\frac{G_K^{pred}}{n_{branch}}
$$

Observed hidden-gradient semantic velocity:

$$
G_K^{hidden}=\frac1m\sum_z v_z^{(K)\top}(-\nabla_{h_z}L_K)
$$

Fixed readout-effective semantic margin:

$$
M_Z^{ref}=\frac1m\sum_z v_z^{(K)\top}h_z
$$

Branch separation energy:

$$
E_Z=\frac{1}{2m^2}\sum_{z,z'}\|h_z-h_{z'}\|^2
$$

Conservative semantic readability:

$$
Q_{eval}(t)=\min\{A(t),P(t),S(t)\}
$$

Local losses:

$$
CE(Y_j)=-\log p_\theta(Y_j\mid h_T)
$$

## Falsification Criteria

Geometry precondition:

$$
G^{pred}_{aligned}-G^{pred}_{low/conflict}
\ge 0.5G^{pred}_{single}
$$

Falsified if, after the geometry, zero, positive, and local guards pass:

$$
\operatorname{mean}(G^{hidden}_{aligned})
\le
\operatorname{mean}(G^{hidden}_{low/conflict}).
$$

Strongly weakened if fewer than 4 of 5 seeds support
`aligned > low/conflict`, or if the observed gap is less than 25% of the
predicted batch-scaled gap.

Supported if the geometry precondition passes, the observed direction matches,
at least 4 of 5 seeds support the direction, `single_h3` is positive,
`shared_only_k4` is near zero, and local shared-target losses remain healthy.

## Output Geometry Audit

The output geometry audit passed. The aligned construction produced cosine 1.0
between centered horizon-3 and horizon-4 semantic rows; the low/conflict
construction produced cosine -1.0 and a much smaller aggregate score.

| Condition | `G_pred_batch_scaled` | centered H3-H4 dot | centered H3-H4 cosine | semantic row norm |
|---|---:|---:|---:|---:|
| `aligned_h3_h4` | 0.015262 | 0.244194 | 1.000000 | 0.983753 |
| `low_conflict_h3_h4` | 0.000954 | -0.122097 | -1.000000 | 0.245938 |
| `single_h3` | 0.003816 | NA | NA | 0.491877 |
| `shared_only_k4` | 0.000000 | NA | NA | 0.000000 |

The geometry gap is:

$$
0.015262-0.000954=0.014308,
$$

which is much larger than:

$$
0.5G^{pred}_{single}=0.001908.
$$

## Primary One-Step Evidence

| eta | `G_pred_single` | `G_pred_aligned` | `G_pred_low_conflict` | `G_hidden_single` | `G_hidden_shared` | `G_hidden_aligned` | `G_hidden_low_conflict` | aligned > low seeds | zero guard | verdict |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0.0001 | 0.003816 | 0.015262 | 0.000954 | 0.003816 | 0.000000 | 0.015262 | 0.000954 | 5 / 5 | pass | support |
| 0.0003 | 0.003816 | 0.015262 | 0.000954 | 0.003816 | 0.000000 | 0.015262 | 0.000954 | 5 / 5 | pass | support |
| 0.0010 | 0.003816 | 0.015262 | 0.000954 | 0.003816 | 0.000000 | 0.015262 | 0.000954 | 5 / 5 | pass | support |

Per-seed hidden-gradient semantic velocity at `eta=1e-4`:

| Seed | `shared_only_k4` | `single_h3` | `aligned_h3_h4` | `low_conflict_h3_h4` | aligned - low |
|---:|---:|---:|---:|---:|---:|
| 971 | 0.000000 | 0.004051 | 0.016205 | 0.001013 | 0.015192 |
| 972 | 0.000000 | 0.004368 | 0.017473 | 0.001092 | 0.016381 |
| 973 | 0.000000 | 0.004241 | 0.016966 | 0.001060 | 0.015905 |
| 974 | 0.000000 | 0.003588 | 0.014353 | 0.000897 | 0.013456 |
| 975 | 0.000000 | 0.002828 | 0.011314 | 0.000707 | 0.010607 |

Interpretation: every seed supports the aligned-minus-low/conflict direction.
The primary observation matches the batch-scaled geometry prediction almost
exactly.

Finite-difference note: $\Delta M_Z^{ref}/\eta$ is not used as the decisive
metric here. As in A11_06, the parameter finite-difference signal is small and
step-size sensitive in this parameterized Transformer; the protocol names
hidden-gradient semantic velocity as primary.

## Local Language-Modeling Guard

| Condition | early `Y1` loss | early `Y2` loss | early `Y1` acc | early `Y2` acc | final `Y1` loss | final `Y2` loss | final `Y1` acc | final `Y2` acc |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `aligned_h3_h4` | 0.393800 | 0.358616 | 0.909091 | 0.909091 | 0.000016 | 0.000016 | 1.0 | 1.0 |
| `low_conflict_h3_h4` | 0.394021 | 0.358784 | 0.909091 | 0.909091 | 0.000017 | 0.000017 | 1.0 | 1.0 |
| `shared_only_k4` | 0.393641 | 0.358459 | 0.909091 | 0.909091 | 0.000013 | 0.000012 | 1.0 | 1.0 |
| `single_h3` | 0.393683 | 0.358472 | 0.909091 | 0.909091 | 0.000011 | 0.000010 | 1.0 | 1.0 |

Interpretation: the primary semantic-velocity difference is not explained by
the aligned condition harming the shared local targets.

## Short Training Curve Evidence

The 2000-step curves are supportive but secondary. They show that the aligned
condition has a stronger readout-facing margin and better guarded readability
than low/conflict on average, while `shared_only_k4` stays at chance.

| Condition | threshold reach rate | reached-only `T_0.9` | early AUC `Q_eval` | AUC `Q_eval` | final `Q_eval` | final `M_Z_ref` | final `M_Z_current` |
|---|---:|---:|---:|---:|---:|---:|---:|
| `aligned_h3_h4` | 0.4 | 100 | 0.5350 | 0.54250 | 0.55 | 2.922875 | 6.992929 |
| `low_conflict_h3_h4` | 0.2 | 400 | 0.3875 | 0.44375 | 0.50 | 0.487142 | 6.532347 |
| `single_h3` | 0.2 | 100 | 0.3925 | 0.39625 | 0.40 | 0.636958 | 1.630620 |
| `shared_only_k4` | 0.0 | NA | 0.2500 | 0.25000 | 0.25 | 0.000000 | 0.000000 |

Seed-level final `Q_eval` is uneven; this is why the curve is a guard, not the
primary decision metric. The one-step hidden-gradient result remains the
falsifier-facing evidence.

## Visualization Results

### Figure 1: One-Step Prediction Versus Observation

![One-step prediction versus observation](figures/a11_08_one_step_prediction_vs_observation.png)

Plot contract:

| Item | Contract |
|---|---|
| Question answered | Does observed hidden-state semantic velocity match output-geometry prediction across conditions? |
| Metric | `G_pred_batch_scaled` and `G_hidden` |
| Data source | `one_step_summary.csv`, eta `1e-4`; values are identical across tested etas for this gradient quantity |
| Aggregation | Mean over five seeds |
| Axis meaning | x-axis: condition; y-axis: semantic direction score |
| Allowed conclusion | The primary first-order quantity matches the predicted vector-sum geometry |
| Limitation | Does not establish long-run or natural-language benefit |

Observed result: predicted and observed bars match; aligned is high, single is
positive, low/conflict is small, shared-only is zero.

### Figure 2: Aligned Versus Low/Conflict By Seed

![Aligned versus low/conflict by seed](figures/a11_08_aligned_low_gap_by_seed.png)

Plot contract:

| Item | Contract |
|---|---|
| Question answered | Is the aligned-minus-low/conflict gap stable across seeds? |
| Metric | `G_hidden` |
| Data source | `one_step_metrics.csv`, eta `1e-4` |
| Aggregation | No aggregation; one point per seed |
| Axis meaning | x-axis: seed; y-axis: hidden semantic velocity |
| Allowed conclusion | All five seeds support aligned greater than low/conflict |
| Limitation | Does not test more natural target geometries |

Observed result: every seed has a large positive aligned-minus-low/conflict gap.

### Figure 3: Training Curve Guard

![Training curve guard](figures/a11_08_training_curve_guard.png)

Plot contract:

| Item | Contract |
|---|---|
| Question answered | Does the one-step mechanism appear in short training as a semantic-state guard? |
| Metric | `Q_eval` and `M_Z_ref` |
| Data source | `curve_metrics.csv` |
| Aggregation | Mean over five seeds at each logged step |
| Axis meaning | x-axis: training step; y-axis: guarded readability or fixed readout margin |
| Allowed conclusion | Aligned geometry has stronger average semantic-state evidence than low/conflict |
| Limitation | Training curves are noisy and secondary; they do not replace the one-step falsifier |

Observed result: aligned rises earlier and higher than low/conflict in mean
`Q_eval` and `M_Z_ref`; shared-only remains at chance / zero margin.

Rendered-artifact audit: all three PNG figures were opened locally after
generation. They render nonblank, labels and legends are readable, and no
central evidence depends on source-code knowledge beyond the metric definitions
in this document.

## Result / Interpretation / Claim Boundary

Result:

```text
geometry precondition: pass
single positive control: pass
shared zero guard: pass
local Y1/Y2 guard: pass
aligned > low/conflict: 5 / 5 seeds
final verdict: support
```

Interpretation: the result strengthens the A11 mechanism from a single
first-informative-horizon story to a multi-informative-horizon vector-sum story.
Additional future horizons help only through the readout-effective directions
they add; an additional informative horizon can be weak or counterproductive if
its centered output direction conflicts with the existing aggregate direction.

Supported claim:

```text
In this controlled decision-prefix first-order setup, general next-K semantic
velocity is governed by the aggregate centered output-row direction over the
covered informative horizons.
```

Not supported:

```text
Larger K is always better.
MTP is better than NTP in natural language.
K1/K2 cannot learn Z in all-position training.
Q_eval alone proves direct supervision.
MoE routing geometry or expert utility follows.
Random natural target geometry will match this controlled construction.
```

## Failure Analysis

The intended falsifier did not fire. The most relevant residual uncertainty is
naturalness of the output geometry. A11_08 deliberately controlled output rows
to make the falsifier sharp. The next-K storyline still needs a less artificial
K-sweep that varies which horizons are included by K and whether added horizons
are informative or uninformative.

Finite-difference margin changes remain small and step-size sensitive. This is
not treated as a contradiction because the anchor and protocol designate
activation-space hidden-gradient velocity as primary. A later protocol can
separately test parameter-space conversion if that becomes the next decision.

## Artifact Map

| Artifact | Path |
|---|---|
| Protocol | `Projects/from-attention-to-search/main/experiments/A11/A11_08_general_k_readout_margin_dynamics/protocol.md` |
| Summary | `Projects/from-attention-to-search/main/experiments/A11/A11_08_general_k_readout_margin_dynamics/summary.md` |
| Detailed record | `Projects/from-attention-to-search/main/experiments/A11/A11_08_general_k_readout_margin_dynamics/detailed.md` |
| Figure directory | `Projects/from-attention-to-search/main/experiments/A11/A11_08_general_k_readout_margin_dynamics/figures/` |
| Runner | `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a11_03_04_semantic_efficiency.py` |
| Config | `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a11_08_general_k_readout_margin_dynamics.json` |
| Result directory | `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a11_08_general_k_readout_margin_dynamics/a11_08_general_k_readout_margin_full_20260709_051147/` |
| Core tables | `.../tables/general_k_falsifier_summary.csv`, `output_geometry.csv`, `one_step_summary.csv`, `one_step_metrics.csv`, `condition_summary.csv`, `local_loss_guard_summary.csv`, `curve_metrics.csv` |
| Job id | Local CUDA run; no remote job id |

## Next Decision

Create the next anchor for next-2 / next-3 / next-K inclusion law before moving
to MoE. Minimal decision question:

```text
When K increases, does first-order semantic velocity change exactly when K
includes an informative future horizon, remain near zero when the added horizon
is uninformative, and equal the predicted vector increment when the added
horizon is informative?
```

Recommended minimal conditions:

```text
K2 without informative horizon: zero guard
K3 first-informative horizon: positive turn-on
K4 adds uninformative horizon: no material semantic increment
K4 adds second aligned informative horizon: positive vector increment
K4 adds second low/conflicting informative horizon: weak or reduced increment
```

This keeps the storyline on next-K semantics and postpones route-relevance /
MoE until the K-inclusion law is established.
