# A06_01_01_E01 Detailed: Common-Filtered Expert-Spectrum Router Initialization

## 0. Quick Recap

Purpose:
Test whether expert-spectrum router initialization becomes useful after common directions in the initial router-input representation are removed or isolated.

Hypothesis:
Random expert FFNs may have distinct high-gain input subspaces, but raw spectrum routing may be common/high-energy contaminated. A common-filtered residual-spectrum initialization should reduce early common-logit amplification if the computation and its linear-router implementation are both valid.

Experiment logic:
Run a full 4-GPU ACP experiment with six initialization variants, seeds 0--2, 0--300 training steps, exact router-input audits, cross-checkpoint replay, expert-spectrum/common-overlap audit, oracle-to-linear assignment audit, and forced-routing utility correlation.

Conclusion:
The direct method is not supported. Common-filtered spectrum initialization lowers replay `A_interaction`, especially in layer 5, but it does not lower the primary step-10 common-margin spike or top-1 load concentration relative to random initialization.

Evidence:
V4 common-filtered spectrum has late-layer `A_interaction=0.1543`, lower than V0 random at 0.2795, but V4 has worse step-10 `common_margin_delta=0.5203` versus 0.3878, worse `raw_max_load=0.9374` versus 0.8344, and fewer effective experts, 1.2177 versus 1.5636.

## 1. Source Files

- Protocol: `protocol.md`
- Runner: `scripts/run_common_filtered_expert_spectrum_init.py`
- Submit script: `scripts/submit_common_filtered_expert_spectrum_init_4gpu_acp.sh`
- Raw run directory: `runs/common_filtered_expert_spectrum_init/a06_01_common_filtered_expert_spectrum_init_4gpu_20260614_full01/`
- Curated tables: `tables/`
- Curated figures: `figures/`

## 2. Execution

ACP job:

```text
job_id: pt-tjk7oil5
state: SUCCEEDED
resource: 4 x N6lS-80GB GPUs
run_name: a06_01_common_filtered_expert_spectrum_init_4gpu_20260614_full01
```

Submit command:

```bash
A06_01_ALLOW_REAL_SUBMIT=1 RUN_NAME=a06_01_common_filtered_expert_spectrum_init_4gpu_20260614_full01 \
  Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_01_E01_common_filtered_spectrum/scripts/submit_common_filtered_expert_spectrum_init_4gpu_acp.sh
```

Runtime log:

```text
logs/acp/a06_01_common_filtered_expert_spectrum_init_4gpu_20260614_full01_runtime_20260614_174618.log
```

## 3. Run Integrity

The full run completed with expected row counts:

| artifact | actual | expected |
|---|---:|---:|
| trajectory rows | 1188 | 1188 |
| checkpoint rows | 198 | 198 |
| gradient rows | 198 | 198 |
| replay rows | 13068 | 13068 |
| replay fraction rows | 108 | 108 |
| spectrum overlap rows | 864 | 864 |
| oracle assignment rows | 432 | 432 |
| forced utility rows | 72 | 72 |
| variant summary rows | 6 | 6 |

Exact router-logit reconstruction was audited:

```text
max_gate_reconstruction_error = 0.0
```

## 4. Model And Data Contract

Model:

```text
Qwen-style random-initialized decoder-only MoE
layers = 6
hidden_size = 512
num_attention_heads = 8
num_key_value_heads = 4
num_experts = 8
expert_hidden_dim = 2048
router = bias-free linear gate
top_k = 1
load_balance_loss = 0.0
pretrained = false
```

Data:

```text
dataset = DCLM packed binary stream
init_sequences = 8192
audit_sequences = 8192
train_sequences = 32768
sequence length = 256 input tokens + shifted targets
seeds = 0, 1, 2
checkpoints = 0, 1, 2, 3, 5, 10, 20, 50, 100, 200, 300
```

Implementation caveat:
The protocol intended `use_shared_expert=false`, matching the earlier A06_01_01 contract. However, the minimal MoE source at `/data/250010109/MoE_Router/src/model/qwen3_moe/myqwen.py` constructs and adds `shared_expert` unconditionally. The router audit is still exact for the top-1 gate, but model-loss and hidden-state dynamics include the shared expert path.

## 5. Initialization Variants

- V0: `random_init`
- V1: `common_orthogonal_random_init`
- V2: `representation_residual_init`
- V3: `raw_spectrum_linear_init`
- V4: `common_filtered_spectrum_linear_init`
- V5: `hybrid_spectrum_to_linear_init`

Expert spectrum was operationalized through the input-side energy matrix:

\[
G_e = W_{gate,e}^{\top} W_{gate,e} + W_{up,e}^{\top} W_{up,e}.
\]

The top eigenvectors define \(S_e\). Common filtering uses a rank-8 common basis estimated from initial router inputs.

## 6. Main Results

Late layers mean layers 3--5, averaged over seeds 0--2.

| variant | cm delta | step10 load | eff. experts | A interaction | step300 loss | residual utility rho |
|---|---:|---:|---:|---:|---:|---:|
| V0 random | 0.3878 | 0.8344 | 1.5636 | 0.2795 | 7.0007 | 0.0952 |
| V1 common-orthogonal random | 0.4435 | 0.9618 | 1.1905 | 0.2699 | 6.9912 | n/a |
| V2 representation residual | 0.6485 | 0.9159 | 1.3808 | 0.2831 | 7.0139 | n/a |
| V3 raw spectrum | 0.6970 | 0.9144 | 1.3197 | 0.3268 | 7.0172 | 0.2328 |
| V4 common-filtered spectrum | 0.5203 | 0.9374 | 1.2177 | 0.1543 | 7.0049 | 0.1164 |
| V5 hybrid spectrum-to-linear | 0.5971 | 0.8872 | 1.3932 | 0.2529 | 7.0204 | 0.0608 |

Interpretation:

V4 is a partial mechanism improvement but not a successful initialization. It lowers replay interaction while worsening the primary early-training surface. V3 has the strongest residual utility signal, but it amplifies the common-margin problem most strongly.

## 7. Layer-5 Replay

Layer 5 was the most important layer in A06_01_01, so it is reported separately.

| variant | A actual | A gate | A hidden | A interaction |
|---|---:|---:|---:|---:|
| V0 random | 0.8086 | 0.0141 | 0.2171 | 0.5773 |
| V3 raw spectrum | 1.5368 | -0.0309 | 0.6092 | 0.9585 |
| V4 common-filtered spectrum | 0.7862 | 0.0320 | 0.4978 | 0.2564 |
| V5 hybrid spectrum-to-linear | 1.1134 | 0.0612 | 0.4703 | 0.5819 |

Interpretation:

Common filtering has a real interaction effect in layer 5: V4 lowers `A_interaction` from 0.5773 to 0.2564. But V4's hidden-only term is higher than random, so the final common-margin path is not solved.

## 8. Oracle-To-Linear Bridge

Residual-spectrum oracle assignments are well-balanced:

```text
residual_oracle max_load: about 0.144
residual_oracle effective_experts: about 7.96
```

But the linear bridge is weak:

```text
V3 residual_oracle_to_linear_agreement = 0.2038
V4 residual_oracle_to_linear_agreement = 0.2157
V5 residual_oracle_to_linear_agreement = 0.2465
```

Interpretation:

The residual-spectrum score is a quadratic subspace score. Compressing it into a linear top-1 router row loses most of the oracle assignment structure. This is a plausible reason the method fails as an initialization even though it is computationally definable.

## 9. Spectrum And Utility

Forced-routing utility was measured only for V0, V3, V4, and V5 at steps 0 and 10 on layers 3--5.

| variant | residual utility Spearman | residual top-1 match |
|---|---:|---:|
| V0 random | 0.0952 | 0.2222 |
| V3 raw spectrum | 0.2328 | 0.3889 |
| V4 common-filtered spectrum | 0.1164 | 0.2778 |
| V5 hybrid spectrum-to-linear | 0.0608 | 0.2778 |

Interpretation:

Expert spectrum contains a weak residual utility signal, strongest in V3. However, the variant with the best utility signal is also the variant that most worsens common-margin amplification.

## 10. Figures

![Step-10 common margin by variant](figures/step10_common_margin_by_variant.png)

![Step-10 raw max load by variant](figures/step10_raw_max_load_by_variant.png)

![Replay A interaction by variant](figures/replay_A_interaction_by_variant.png)

## 11. Token-Frequency Routing Audit

Question:
Does step-0 routing under different initializations mainly differ because high-frequency token ids route differently?

Audit design:
Reuse the completed step-0 checkpoints. Define high-frequency tokens from the init split token-id counts, then measure step-0 route load separately on all tokens, high-frequency tokens only, and tokens with high-frequency ids removed.

Definitions:

| definition | value |
|---|---:|
| observed token types in init split | 50785 |
| top 1% observed token types | 508 ids |
| top 1% token mass in init split | 0.6145 |
| top 5% observed token types | 2540 ids |
| top 5% token mass in init split | 0.7739 |

Execution:

```bash
python Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_01_E01_common_filtered_spectrum/scripts/audit_step0_token_frequency_routing.py \
  --token-audit-batch-size 64 \
  --frequency-count-batch-size 256 \
  --top-token-count 64 \
  --output-dir Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_01_E01_common_filtered_spectrum
```

Outputs:

- `tables/token_frequency_routing/frequency_group_definition.csv`
- `tables/token_frequency_routing/step0_frequency_group_route_summary.csv`
- `tables/token_frequency_routing/step0_top_token_route_distribution.csv`
- `tables/token_frequency_routing/frequency_group_late_layer_summary.csv`
- `tables/token_frequency_routing/frequency_group_high_minus_without_delta.csv`
- `tables/token_frequency_routing/top64_token_late_layer_summary.csv`
- `tables/token_frequency_routing/step0_step10_late_layer_rank_distribution_summary.csv`
- `tables/token_frequency_routing/without_top1pct_highfreq_late_layer_rank_distribution_key.csv`
- `tables/token_frequency_routing/step10_minus_step0_late_layer_rank_distribution_delta.csv`

Late layers are layers 3--5, averaged over seeds 0--2.

| variant | all-token max load | high-frequency max load | without-high-frequency max load | high-minus-without |
|---|---:|---:|---:|---:|
| V0 random | 0.2010 | 0.2018 | 0.1998 | 0.0020 |
| V1 common-orthogonal random | 0.1394 | 0.1401 | 0.1392 | 0.0009 |
| V2 representation residual | 0.1448 | 0.1458 | 0.1440 | 0.0017 |
| V3 raw spectrum | 0.1681 | 0.1687 | 0.1673 | 0.0014 |
| V4 common-filtered spectrum | 0.1393 | 0.1406 | 0.1397 | 0.0009 |
| V5 hybrid spectrum-to-linear | 0.1622 | 0.1628 | 0.1617 | 0.0010 |

Top-64 frequent token audit:

| variant | top64 mean max load | top64 mean effective experts | single-expert token fraction |
|---|---:|---:|---:|
| V0 random | 0.2253 | 7.2702 | 0.0000 |
| V1 common-orthogonal random | 0.1886 | 7.6563 | 0.0000 |
| V2 representation residual | 0.1651 | 7.8430 | 0.0000 |
| V3 raw spectrum | 0.2017 | 7.5271 | 0.0000 |
| V4 common-filtered spectrum | 0.1891 | 7.6479 | 0.0000 |
| V5 hybrid spectrum-to-linear | 0.1834 | 7.7018 | 0.0000 |

Interpretation:

High-frequency tokens are a large fraction of the token mass, but they do not explain the initialization comparison. Removing the top 1% observed token types preserves the qualitative ordering of the variants, and the high-minus-without-high `max_load` gap is at most 0.0020 in late layers. Top-64 frequent tokens are somewhat more concentrated than all tokens, especially for V0, but none of the top-64 tokens is single-expert collapsed at step 0.

Rank-distribution audit:
The sharper audit sorts experts by their load within each variant, seed, step, layer, and token group. This answers how much token mass is assigned to the rank-1 expert, rank-2 expert, and so on, independent of fixed expert id.

Command:

```bash
python Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_01_E01_common_filtered_spectrum/scripts/audit_token_frequency_rank_routing.py \
  --steps 0 10 \
  --token-audit-batch-size 64 \
  --frequency-count-batch-size 256 \
  --output-dir Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_01_E01_common_filtered_spectrum
```

After removing the top 1% high-frequency token ids, the late-layer sorted route distribution is:

| variant | step | rank1 | rank2 | rank3 | rank4 | rank5 | rank6 | rank7 | rank8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| V0 random | 0 | 19.98 | 16.81 | 14.08 | 12.63 | 11.26 | 9.62 | 8.18 | 7.44 |
| V0 random | 10 | 83.16 | 13.48 | 2.86 | 0.34 | 0.05 | 0.04 | 0.04 | 0.03 |
| V1 common-orthogonal random | 0 | 13.92 | 13.39 | 12.88 | 12.71 | 12.35 | 12.05 | 11.70 | 11.00 |
| V1 common-orthogonal random | 10 | 96.23 | 2.97 | 0.53 | 0.12 | 0.05 | 0.04 | 0.04 | 0.03 |
| V2 representation residual | 0 | 14.40 | 13.95 | 13.29 | 12.83 | 12.30 | 11.76 | 11.13 | 10.35 |
| V2 representation residual | 10 | 91.27 | 5.37 | 2.52 | 0.39 | 0.27 | 0.09 | 0.05 | 0.04 |
| V3 raw spectrum | 0 | 16.73 | 14.95 | 13.83 | 13.07 | 12.13 | 11.16 | 9.84 | 8.31 |
| V3 raw spectrum | 10 | 91.33 | 7.55 | 0.48 | 0.40 | 0.11 | 0.07 | 0.04 | 0.03 |
| V4 common-filtered spectrum | 0 | 13.97 | 13.31 | 12.90 | 12.63 | 12.43 | 12.10 | 11.52 | 11.15 |
| V4 common-filtered spectrum | 10 | 93.51 | 6.04 | 0.14 | 0.12 | 0.08 | 0.05 | 0.04 | 0.03 |
| V5 hybrid spectrum-to-linear | 0 | 16.17 | 15.02 | 13.56 | 12.76 | 12.12 | 10.98 | 10.07 | 9.31 |
| V5 hybrid spectrum-to-linear | 10 | 88.64 | 10.39 | 0.41 | 0.26 | 0.14 | 0.07 | 0.05 | 0.03 |

Interpretation:
At step 0, common-filtered and representation-residual initializations do reduce the initial sorted-load imbalance after high-frequency tokens are removed: their rank-1 experts are near 14%, close to the uniform 12.5% baseline. Random initialization is already more imbalanced at 19.98%, and raw/hybrid spectrum are intermediate at 16--17%.

However, this initial balance does not protect the early training trajectory. By step 10, every variant concentrates most non-high-frequency tokens in the rank-1 expert. V4 common-filtered spectrum reaches 93.51% rank-1 load, worse than V0 random at 83.16%. Therefore the failure is not that common-filtered initialization cannot reduce step-0 imbalance; it can. The failure is that the training dynamics amplify a dominant route even from a balanced initial distribution.

Claim boundary:

This audit covers initial token-id frequency groups only. It does not prove that high-frequency tokens are irrelevant after training begins, because hidden-state drift can make the same token id occupy different representation regions across steps.

## 12. Hypothesis Status

H1: Expert high-gain input subspaces contain non-random routing information.

Status:
Weakly supported. V3 has higher residual utility correlation and top-1 utility match than random. The signal is too weak to justify a full method claim.

H2: Raw expert-spectrum routing is vulnerable to common-direction capture.

Status:
Partially supported but with a revised mechanism. Direct overlap between \(S_e\) and the rank-8 common basis is low, about 0.0166, but the raw spectrum linear row obtains much larger common projection, with mean \(|w^\top c|\) about 0.2116. The common contamination appears in the linear compression/row construction, not in simple subspace overlap alone.

H3: Common-filtered spectrum initialization is the more plausible method.

Status:
Weakened as a direct initialization. It lowers `A_interaction`, but fails the primary early-training metrics and does not preserve better effective expert usage.

Frequency-token rival explanation:
Weakened. The post-hoc step-0 token-frequency audit shows that the initial route distribution differences are not driven by a small high-frequency-token subset.

## 13. Claim Boundary

Can claim:

- The full A06_01_01_E01 method is implemented and audited on a 4-GPU ACP run.
- Common-filtered spectrum initialization lowers replay interaction in late layers and layer 5.
- It does not reduce the step-10 common-margin spike or raw top-1 load concentration relative to random initialization.
- Linear compression is a likely bottleneck because residual-spectrum oracle assignment is balanced but poorly matched by the linear top-1 router.
- Step-0 route distribution differences across initialization variants are not explained by isolating or removing high-frequency token ids.

Cannot claim:

- Expert spectrum is useless in general.
- The advisor's idea is impossible.
- A quadratic, oracle, or learned classifier router would fail.
- The result transfers to pretrained, large, top-2/top-4, or load-balanced MoEs.
- High-frequency tokens play no role during training; the audit only rules out a step-0 token-id-frequency explanation.

## 14. Artifact Map

Curated artifacts:

- `summary.md`
- `detailed.md`
- `tables/run_integrity_summary.csv`
- `tables/variant_summary_late_layers.csv`
- `tables/layer5_replay_decomposition.csv`
- `tables/oracle_linearization_summary.csv`
- `tables/spectrum_common_overlap_summary.csv`
- `tables/utility_correlation_summary.csv`
- `tables/token_frequency_routing/frequency_group_definition.csv`
- `tables/token_frequency_routing/frequency_group_late_layer_summary.csv`
- `tables/token_frequency_routing/frequency_group_high_minus_without_delta.csv`
- `tables/token_frequency_routing/top64_token_late_layer_summary.csv`
- `tables/token_frequency_routing/step0_step10_late_layer_rank_distribution_summary.csv`
- `tables/token_frequency_routing/without_top1pct_highfreq_late_layer_rank_distribution_key.csv`
- `tables/token_frequency_routing/without_top1pct_highfreq_late_layer_collapse_key.csv`
- `tables/token_frequency_routing/step10_minus_step0_late_layer_rank_distribution_delta.csv`
- `figures/step10_common_margin_by_variant.png`
- `figures/step10_raw_max_load_by_variant.png`
- `figures/replay_A_interaction_by_variant.png`

Raw run artifacts:

- `runs/common_filtered_expert_spectrum_init/a06_01_common_filtered_expert_spectrum_init_4gpu_20260614_full01/results/`
- `runs/common_filtered_expert_spectrum_init/a06_01_common_filtered_expert_spectrum_init_4gpu_20260614_full01/checkpoints/`
- `runs/common_filtered_expert_spectrum_init/a06_01_common_filtered_expert_spectrum_init_4gpu_20260614_full01/partials/`
- `runs/common_filtered_expert_spectrum_init/a06_01_common_filtered_expert_spectrum_init_4gpu_20260614_full01/config/`

## 15. Next Decision

Do not promote V4 common-filtered expert-spectrum linear initialization as a successful method.

The only useful follow-up is a narrow computation-vs-implementation split:
run a residual-spectrum oracle gate, or a stronger fitted classifier bridge, for the first 10 steps. If that also fails to reduce common-margin and load concentration, expert-spectrum routing should be parked for this random-init DCLM top-1 setting.
