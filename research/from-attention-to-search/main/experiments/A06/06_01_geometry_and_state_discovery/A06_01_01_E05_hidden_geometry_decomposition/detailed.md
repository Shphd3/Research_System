# Detailed: A06_01_01_E05 Synthetic Hidden-State Gate Geometry Decomposition

Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`
Protocol: `protocol.md`
Summary: `summary.md`

## 0. Quick Recap

Purpose:
Diagnose which initialized gate/hidden geometry term explains step-0 top-1 load imbalance after uniformly sampled synthetic `(slot,target)` pairs are mapped into router-input hidden states.

Hypothesis:
If router-row norm variation is causal, `NR` should reduce \(L\) relative to `RR`. If the hidden common component is causal, `RC` should reduce \(L\) relative to `RR`. If the two factors interact, `NC` should be distinctly lower than both single controls or show a non-additive effect.

Experiment logic:
Generate uniform synthetic pairs, extract final-block router-input hidden states at initialization, and replay four scoring conditions on the same hidden states and router rows: `RR`, `NR`, `RC`, and `NC`.

Conclusion:
The run supports hidden common component as the dominant tested source of initialized synthetic hidden-state load imbalance. Row-norm normalization is not supported as the main explanation in this setting, and the interaction readout is not stable enough to carry the main claim.

Evidence:
In the primary readout, mean \(L\) is `RR=0.5578`, `NR=0.5577`, `RC=0.2578`, and `NC=0.2407`. The common effect is positive in all 8 primary seeds; the norm effect is near zero and changes sign.

## 1. Anchor Link And Decision Point

Anchor decision question:
Under a uniform synthetic `(slot,target)` distribution, does initialized step-0 top-1 load imbalance come mainly from expert-center norm variation, hidden common component, their interaction, or neither?

Decision after this experiment:
Treat the hidden common component as the supported tested mechanism for the raw imbalance, and move the next diagnostic to the remaining load after common-centering.

## 2. Protocol Compliance Audit

approved conditions match actual conditions:
Yes. The run used `RR`, `NR`, `RC`, and `NC`, crossed with `num_layers=1,2,4` and `router_input_norm=post_ln,pre_ln_replay`.

primary metric exists:
Yes. Load imbalance \(L=m\max_e |p_e-1/m|\) is in `tables/results.csv` and summarized in `tables/aggregate_by_condition.csv`.

central figures/tables exist:
Yes. Central tables are `results.csv`, `aggregate_by_condition.csv`, `paired_effects.csv`, and `paired_effects_aggregate.csv`. Central figures are in `figures/`.

seeds/checkpoints recorded:
Yes. Seeds are `20260521,20260522,20260523,20260524,20260525,20260526,20260527,20260528`. The only checkpoint is initialization / step 0.

known good/bad/confusing cases reviewed:
Yes. The run does not use `SLOT_s B_CONST Y_s`. LayerNorm readout is treated as a side guard, not a method conclusion. The gate-only 06_03 norm result is not assumed to transfer.

success/failure/insufficient-evidence criteria applied:
Yes. `RC` supports the common mechanism. `NR` weakens row norm as the main explanation in this hidden-state setting. `NC` supports joint replay only insofar as it includes common-centering; the interaction term is not stable.

## 3. Setup

Data:

| Field | Value |
| --- | --- |
| sequence length | 32 |
| pairs | 4 `(SLOT_s,TARGET_s)` pairs |
| experts | 4 |
| samples per pair | 4096 |
| samples per seed/depth | 16,384 |
| pair distribution | exactly uniform |
| pair start | randomized over valid starts |
| route position | last slot position, equal to `pair_start` for one-token slots |
| background tokens | random disjoint background tokens, independent of pair id |

Model:
Initialized dot-product top-1 synthetic Transformer-MoE. No training, no optimizer, and no checkpoint beyond initialization.

Layer guard:
`num_layers=1,2,4`. For depth greater than one, only the final TransformerMoEBlock router input and final-router rows are used.

LayerNorm guard:

- `post_ln`: actual final-router input after the block LayerNorm.
- `pre_ln_replay`: final pre-router residual stream before that LayerNorm, scored by the same final-router rows.

Score replay:

| Condition | Formula | Tested term |
| --- | --- | --- |
| `RR` | \(w_e^\top h_i\) | raw baseline |
| `NR` | \(\bar{\rho}u_e^\top h_i\) | router-row norm scale \(\rho_e\) |
| `RC` | \(w_e^\top(h_i-c)\) | hidden common component \(c\) |
| `NC` | \(\bar{\rho}u_e^\top(h_i-c)\) | joint control and residual geometry |

## 4. Metrics And Decision Rules

Primary metric:
\(L=m\max_e |p_e-1/m|\).

Why it decides:
The question is whether uniform symbolic data become non-uniform expert load after hidden-state formation. \(L\) directly measures the worst expert-load deviation from uniform.

Effect diagnostics:

- \(E_{norm}=L^{RR}-L^{NR}\);
- \(E_{common}=L^{RR}-L^{RC}\);
- \(E_{joint}=L^{RR}-L^{NC}\);
- \(E_{interaction}=E_{joint}-E_{norm}-E_{common}\).

Decision rules:

- support norm mechanism if `NR` lowers \(L\) relative to `RR` and does not reverse under guards;
- support common mechanism if `RC` lowers \(L\) relative to `RR` and does not reverse under guards;
- support interaction if `NC` is distinctly lowest or \(E_{interaction}\) is stable;
- weaken tested terms if all controls stay close to `RR`.

## 5. Main Results

### Primary Readout

Primary readout: `num_layers=1`, `router_input_norm=post_ln`.

| Condition | Mean \(L\) | Mean max load | Mean entropy | Interpretation |
| --- | ---: | ---: | ---: | --- |
| `RR` | 0.5578 | 0.3739 | 0.9449 | raw load is imbalanced |
| `NR` | 0.5577 | 0.3755 | 0.9441 | row-norm normalization does not reduce \(L\) |
| `RC` | 0.2578 | 0.3113 | 0.9860 | common-centering gives the main reduction |
| `NC` | 0.2407 | 0.3084 | 0.9877 | joint replay is slightly lower, mostly through common-centering |

Primary paired effects:

| Effect | Mean | Direction across seeds | Interpretation |
| --- | ---: | --- | --- |
| \(E_{norm}\) | 0.0001 | 5 positive, 3 negative | near zero, unstable |
| \(E_{common}\) | 0.3000 | 8 positive, 0 negative | stable support |
| \(E_{joint}\) | 0.3170 | 8 positive, 0 negative | stable support through common-centering |
| \(E_{interaction}\) | 0.0169 | 5 positive, 3 negative | not stable |

### Guard Sweep

Mean \(L\) by layer and readout:

| Layers | Readout | `RR` | `NR` | `RC` | `NC` | Main read |
| ---: | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `post_ln` | 0.5578 | 0.5577 | 0.2578 | 0.2407 | common supported |
| 1 | `pre_ln_replay` | 0.5691 | 0.5606 | 0.2492 | 0.2442 | common supported |
| 2 | `post_ln` | 0.6494 | 0.6427 | 0.3462 | 0.3505 | common supported |
| 2 | `pre_ln_replay` | 0.6476 | 0.6421 | 0.3439 | 0.3520 | common supported |
| 4 | `post_ln` | 0.8498 | 0.8519 | 0.2469 | 0.2528 | common supported |
| 4 | `pre_ln_replay` | 0.8495 | 0.8509 | 0.2481 | 0.2482 | common supported |

Common-centering is robust across the guard sweep. Row-norm normalization is small and sometimes negative. The LayerNorm readout changes absolute values slightly but not the main conclusion.

### Residual Load After Common-Centering

Common-centering does not make \(L\) zero. After `RC` or `NC`, mean max load remains about 0.30 to 0.34 rather than the uniform value 0.25. This keeps residual hidden anisotropy, router-direction cell geometry, random-context structure, and finite-sample / position effects alive as next-step explanations.

## 6. Visualization Results

### Primary Load Imbalance By Replay Condition

![Primary load imbalance by replay condition](figures/load_imbalance_by_condition.png)

Purpose:
Show which replay control most reduces \(L\) in the primary readout.

Setup:
`num_layers=1`, `router_input_norm=post_ln`, 8 seeds, 4096 samples per pair per seed.

How to read:
Lower bars mean closer-to-uniform expert load. `RR` is raw, `NR` normalizes router-row norm, `RC` removes the hidden common component, and `NC` applies both controls.

Observed result:
`RR` and `NR` are nearly identical. `RC` and `NC` are much lower.

Take-home:
The hidden common component is the main tested source of load imbalance in the primary readout.

Remaining uncertainty:
`NC` remains imbalanced, so residual hidden geometry still matters.

What this figure does not prove:
It does not prove real-text behavior, training collapse, semantic specialization, expert utility, or a deployable router.

Anchor update implication:
Support the common-component branch and weaken row-norm-as-main for this hidden-state setting.

### Layer Guard Under Post-LayerNorm Readout

![Layer guard under post-LayerNorm readout](figures/load_imbalance_by_layer_post_ln.png)

Purpose:
Check whether the common-centering result survives the layer-depth guard under the actual final-router input.

Setup:
`num_layers=1,2,4`, `router_input_norm=post_ln`, 8 seeds.

How to read:
At each layer depth, compare the four replay conditions.

Observed result:
Raw imbalance increases with depth. Common-centering strongly reduces it at every tested depth. Row-norm normalization remains close to raw.

Take-home:
The result is not a one-layer-only artifact.

Remaining uncertainty:
The figure does not identify which hidden-state source creates the common component.

What this figure does not prove:
It does not prove a training-dynamics mechanism.

Anchor update implication:
Depth guard strengthens the common-component interpretation.

### Layer Guard Under Pre-LayerNorm Replay

![Layer guard under pre-LayerNorm replay](figures/load_imbalance_by_layer_pre_ln_replay.png)

Purpose:
Check whether the readout before the final block LayerNorm changes the mechanism judgment.

Setup:
`num_layers=1,2,4`, `router_input_norm=pre_ln_replay`, same final-router rows.

How to read:
The comparison is a readout guard. It is not an architecture proposal.

Observed result:
The ordering remains the same: `RC` and `NC` reduce \(L\), `NR` does not.

Take-home:
The main conclusion is not driven by one LayerNorm readout.

Remaining uncertainty:
LayerNorm affects scale and absolute common-score spread, so this remains a boundary qualifier.

What this figure does not prove:
It does not imply LayerNorm should be added or removed.

Anchor update implication:
Keep LayerNorm as a boundary note, not as the mainline conclusion.

### LayerNorm Readout Guard At One Layer

![LayerNorm readout guard at one layer](figures/load_imbalance_by_layernorm.png)

Purpose:
Compare `post_ln` and `pre_ln_replay` directly in the one-layer setting.

Setup:
`num_layers=1`, two readouts, same replay conditions.

How to read:
For each condition, compare the readout pair.

Observed result:
Absolute values shift slightly, but common-centering remains the only strong reduction.

Take-home:
The one-layer conclusion is stable to this readout change.

Remaining uncertainty:
This does not resolve where the common component originates.

What this figure does not prove:
It does not justify an architecture change.

Anchor update implication:
LayerNorm sensitivity is a side boundary, not the next main diagnostic.

## 7. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / failed / unclear | Failure reason | What this rules out |
| --- | --- | --- | --- | --- |
| pair audit | `tables/pair_audit.csv`; every pair count is 4096 for every seed/depth | passed | n/a | rules out non-uniform pair counts |
| position audit | `tables/position_audit.csv`; pair starts are randomized, with counts in the expected random range | passed | n/a | rules out fixed pair position |
| background audit | `tables/background_audit.csv`; construction uses disjoint random background tokens independent of pair id | passed | n/a | rules out old fixed-B contamination |
| state extraction | `tables/state_audit.csv`; every state tensor is `16384x128` | passed | n/a | rules out missing hidden states |
| router audit | `tables/router_audit.csv`; final-router row shape is `4x128` and final-block-only is true | passed | n/a | rules out wrong router shape |
| score replay | `tables/replay_audit.csv`; hidden states unchanged and model state unchanged | passed | n/a | rules out replay changing the model |
| primary metric | `tables/results.csv`; \(L\) exists for every condition | passed | n/a | rules out missing metric coverage |

Falsified physical prior:
None. The run supports the prior that uniform symbolic data can become non-uniform hidden-state routing geometry.

Weakened physical prior:
Router-row norm variation is weakened as the main explanation in this hidden-state setting.

Supported physical prior:
The hidden common component can behave like an expert-specific effective bias.

Falsified mathematical model:
No full model is falsified, but the norm-only explanation is not sufficient.

Falsified operationalization / proxy:
No. The four-condition replay produced valid matched comparisons.

Falsified implementation:
No. The protocol compliance audit passed.

Falsified metric:
No. \(L\) directly answers the load-imbalance question, though it does not explain residual geometry by itself.

Remaining rival explanations:

- residual hidden anisotropy after common-centering;
- router-direction cell geometry;
- random-context structure;
- finite-sample or pair-position effects;
- sources of the common component inside attention, embeddings, position, or LayerNorm.

## 8. Full Experiment Record

Run identity:

- ACP job id: `pt-sqq2jr6d`
- final state: `SUCCEEDED`
- run name: `a06_04_real_hidden_state_gate_geometry_decomposition_4gpu_20260621`
- run stage: `full`
- execution date: 2026-06-21

Command:

```bash
A0604_ALLOW_REAL_SUBMIT=1 bash active/synthetic_data_understanding/scripts/submit_a06_04_real_hidden_state_gate_geometry_decomposition_4gpu_acp.sh
```

Runtime command inside ACP:

```bash
python scripts/run_a06_04_real_hidden_state_gate_geometry_decomposition.py \
  --config "${CONFIG_PATH}" \
  --run-name "${RUN_NAME}" \
  --run-stage "${RUN_STAGE}" \
  --seeds "${SEEDS}" \
  --num-layers "${NUM_LAYERS}" \
  --router-input-norm "${ROUTER_INPUT_NORM}" \
  --score-conditions "${SCORE_CONDITIONS}"
```

Seeds:
`20260521,20260522,20260523,20260524,20260525,20260526,20260527,20260528`.

Conditions:
`RR,NR,RC,NC`.

Guard sweeps:
`num_layers=1,2,4` crossed with `router_input_norm=post_ln,pre_ln_replay`.

Result rows:
192 condition rows and 48 paired-effect rows.

## 9. Interpretation

Observation:
Raw initialized routing is imbalanced even though pair labels are exactly uniform.

Interpretation:
The imbalance is not primarily caused by router-row norm scale in this hidden-state setting. It is mainly carried by the hidden common component because subtracting the hidden mean consistently reduces \(L\).

Claim:
For this uniform synthetic `(slot,target)` task at initialization, hidden common component is the dominant tested source of step-0 top-1 load imbalance.

Speculation:
The remaining imbalance after common-centering may come from residual hidden anisotropy, router-direction cell geometry, random context, or position-dependent structure. This run does not decide among those residual explanations.

Boundary:
This is synthetic initialized hidden-state evidence only. It does not establish real-text behavior, training collapse, semantic specialization, expert utility, or a deployable router.

## 10. Claim Boundary

Can claim:

- Uniform symbolic pair sampling does not guarantee balanced initialized hidden-state routing.
- Hidden common-centering robustly reduces load imbalance across the tested seeds, layer depths, and LayerNorm readouts.
- Router-row norm normalization is not the main tested explanation in this run.
- The interaction term is not stable enough to become the main claim.

Cannot claim:

- Real text has the same hidden common component.
- Training will amplify or suppress this mechanism.
- This explains final MoE collapse.
- This creates semantic expert specialization.
- This binds routing to expert utility.
- This recommends a final router design.

## 11. Next Decision

Run the next residual diagnostic after common-centering. The smallest useful branch is to separate:

- residual hidden anisotropy;
- router-direction cell geometry;
- random-context or position structure;
- finite-sample effects.

The next protocol should keep common-centering as the baseline control and ask which residual term explains the remaining \(L\).

## 12. Links And Artifact Map

anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

protocol:
`protocol.md`

summary:
`summary.md`

code workspace:
`../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding`

runner:
`../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a06_04_real_hidden_state_gate_geometry_decomposition.py`

config:
`../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a06_04_real_hidden_state_gate_geometry_decomposition.json`

key code files:

- `../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/src/synthetic_data_understanding/tiny_moe.py`
- `../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/submit_a06_04_real_hidden_state_gate_geometry_decomposition_4gpu_acp.sh`

data / manifest:
synthetic data generated by the runner from the config; no external dataset.

result dir:
`../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a06_04_real_hidden_state_gate_geometry_decomposition/a06_04_real_hidden_state_gate_geometry_decomposition_4gpu_20260621`

figure dir:
`../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/figures/a06_04_real_hidden_state_gate_geometry_decomposition/a06_04_real_hidden_state_gate_geometry_decomposition_4gpu_20260621`

canonical tables:
`tables/`

canonical figures:
`figures/`

key tables:

- `tables/results.csv`
- `tables/aggregate_by_condition.csv`
- `tables/paired_effects.csv`
- `tables/paired_effects_aggregate.csv`
- `tables/pair_audit.csv`
- `tables/position_audit.csv`
- `tables/background_audit.csv`
- `tables/state_audit.csv`
- `tables/router_audit.csv`
- `tables/replay_audit.csv`

logs / checkpoints:

- submit log: `../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/logs/acp/a06_04_real_hidden_state_gate_geometry_decomposition_4gpu_20260621_submit_20260621_124911.log`
- runtime log: `../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/logs/acp/a06_04_real_hidden_state_gate_geometry_decomposition_4gpu_20260621_runtime_20260621_124953.log`
- checkpoints: none, initialization-only audit

repro command:

```bash
cd /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments
A0604_ALLOW_REAL_SUBMIT=1 bash active/synthetic_data_understanding/scripts/submit_a06_04_real_hidden_state_gate_geometry_decomposition_4gpu_acp.sh
```

job id:
`pt-sqq2jr6d`
