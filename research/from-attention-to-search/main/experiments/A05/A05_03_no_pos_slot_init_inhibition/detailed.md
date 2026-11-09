## 0. Quick Recap

Purpose: test slot-init and true token-conditioned inhibition after removing absolute positional embedding throughout training.

Hypothesis: if fixed position/common shift was the main blocker, no-position slot-init or inhibition should produce seed-stable slot/feature-level expert specialization.

Experiment logic: run the H0605a uniform multi-B setting with `pos_emb.weight` zeroed and frozen from initialization; compare random vs slot-init and no-inhibition vs inhibition under dot-product and cosine routers.

Conclusion: cosine slot-init alone (`S0-cos`) produces the clearest seed-stable slot-level routing structure; inhibition alone collapses, and inhibition added to slot-init is not reliably helpful.

Evidence: 24/24 full runs completed on 4GPU ACP job `pt-rzr278jh`; all final checkpoint positional embeddings remain exactly zero; final slot x expert heatmaps and seed-level NMI/load/accuracy tables are complete.

## 1. Question

Does slot initialization or true token-conditioned inhibition produce feature-level expert specialization after the fixed position source is excluded?

Operational definitions:

- Slot-level routing structure: expert assignment carries slot identity. Primary metric: `route_slot_nmi_feature_eval`.
- Exact feature-level routing structure: expert assignment carries exact `(slot, B_i)` identity. Primary metric: `route_feature_key_nmi`.
- Collapse guard: `expert_load_max_fraction`, `active_experts`, and load entropy. These do not by themselves prove specialization.
- Validity guard: `target_accuracy_feature_eval`.

## 2. Implementation Contract

The no-position intervention is implemented at model construction:

```python
with torch.no_grad():
    model.pos_emb.weight.zero_()
model.pos_emb.weight.requires_grad_(False)
```

This is not post-hoc subtraction from the gating hidden state. It removes absolute positional embedding from the embedding sum before attention, residual stream, MoE routing, and target prediction. The wrapper patches the H0605a model factory inside each spawned worker, so reliability audit, slot-init calibration, training, and evaluation all use the no-position model.

## 3. Conditions

| Condition | Router metric | Slot-init | Inhibition |
|---|---|---:|---:|
| `R0-dot` | dot product | no | no |
| `S0-dot` | dot product | yes | no |
| `R1-dot` | dot product | no | yes |
| `S1-dot` | dot product | yes | yes |
| `R0-cos` | cosine | no | no |
| `S0-cos` | cosine | yes | no |
| `R1-cos` | cosine | no | yes |
| `S1-cos` | cosine | yes | yes |

Seeds: `20260521`, `20260522`, `20260523`.

Training: 1600 steps, batch size 384, full-sequence NTP.

Mode: `multi_b_primary`.

## 4. Execution Audit

| Item | Result |
|---|---|
| ACP job id | `pt-rzr278jh` |
| ACP status | `SUCCEEDED` |
| Completed condition/seed runs | 24 / 24 |
| Final model files | 24 |
| `pos_emb.weight` final max norm | 0.0 |
| `pos_emb.weight` final max absolute value | 0.0 |
| `metrics.json` count | 24 |
| Slot heatmap PNG count | 50 |
| Target accuracy validity | all final feature-eval accuracies 0.981-1.000 |

## 5. Primary Metrics By Seed

| condition   |     seed |   route_slot_nmi_feature_eval |   route_feature_key_nmi |   expert_load_max_fraction |   active_experts |   target_accuracy_feature_eval |
|:------------|---------:|------------------------------:|------------------------:|---------------------------:|-----------------:|-------------------------------:|
| R0-dot      | 20260521 |                         0.328 |                   0.418 |                      0.303 |            4.000 |                          0.996 |
| R0-dot      | 20260522 |                         0.217 |                   0.358 |                      0.507 |            4.000 |                          0.997 |
| R0-dot      | 20260523 |                         0.173 |                   0.399 |                      0.391 |            4.000 |                          0.997 |
| S0-dot      | 20260521 |                         0.376 |                   0.409 |                      0.412 |            4.000 |                          0.981 |
| S0-dot      | 20260522 |                         0.347 |                   0.388 |                      0.528 |            4.000 |                          0.999 |
| S0-dot      | 20260523 |                         0.461 |                   0.395 |                      0.355 |            4.000 |                          0.984 |
| R1-dot      | 20260521 |                         0.092 |                   0.232 |                      0.900 |            4.000 |                          0.997 |
| R1-dot      | 20260522 |                         0.051 |                   0.164 |                      0.962 |            3.000 |                          1.000 |
| R1-dot      | 20260523 |                         0.098 |                   0.263 |                      0.873 |            4.000 |                          0.998 |
| S1-dot      | 20260521 |                         0.755 |                   0.391 |                      0.462 |            3.000 |                          0.997 |
| S1-dot      | 20260522 |                         0.480 |                   0.374 |                      0.580 |            3.000 |                          0.994 |
| S1-dot      | 20260523 |                         0.458 |                   0.398 |                      0.485 |            4.000 |                          0.997 |
| R0-cos      | 20260521 |                         0.412 |                   0.415 |                      0.333 |            4.000 |                          0.999 |
| R0-cos      | 20260522 |                         0.240 |                   0.375 |                      0.520 |            4.000 |                          0.995 |
| R0-cos      | 20260523 |                         0.169 |                   0.380 |                      0.534 |            4.000 |                          0.990 |
| S0-cos      | 20260521 |                         0.781 |                   0.431 |                      0.318 |            4.000 |                          0.999 |
| S0-cos      | 20260522 |                         0.722 |                   0.389 |                      0.523 |            4.000 |                          0.997 |
| S0-cos      | 20260523 |                         0.720 |                   0.427 |                      0.316 |            4.000 |                          0.991 |
| R1-cos      | 20260521 |                         0.066 |                   0.186 |                      0.943 |            4.000 |                          0.999 |
| R1-cos      | 20260522 |                         0.015 |                   0.202 |                      0.934 |            4.000 |                          1.000 |
| R1-cos      | 20260523 |                         0.124 |                   0.258 |                      0.889 |            4.000 |                          1.000 |
| S1-cos      | 20260521 |                         0.336 |                   0.247 |                      0.848 |            2.000 |                          1.000 |
| S1-cos      | 20260522 |                         0.490 |                   0.350 |                      0.679 |            3.000 |                          0.997 |
| S1-cos      | 20260523 |                         0.467 |                   0.395 |                      0.609 |            4.000 |                          0.999 |

## 6. Summary By Condition

| condition   |   route_slot_nmi_feature_eval_mean |   route_slot_nmi_feature_eval_std |   route_feature_key_nmi_mean |   expert_load_max_fraction_mean |   target_accuracy_feature_eval_mean |
|:------------|-----------------------------------:|----------------------------------:|-----------------------------:|--------------------------------:|------------------------------------:|
| R0-dot      |                              0.239 |                             0.065 |                        0.391 |                           0.400 |                               0.997 |
| S0-dot      |                              0.395 |                             0.048 |                        0.397 |                           0.432 |                               0.988 |
| R1-dot      |                              0.080 |                             0.021 |                        0.220 |                           0.912 |                               0.998 |
| S1-dot      |                              0.564 |                             0.135 |                        0.388 |                           0.509 |                               0.996 |
| R0-cos      |                              0.274 |                             0.102 |                        0.390 |                           0.462 |                               0.994 |
| S0-cos      |                              0.741 |                             0.028 |                        0.416 |                           0.385 |                               0.996 |
| R1-cos      |                              0.069 |                             0.045 |                        0.215 |                           0.922 |                               0.999 |
| S1-cos      |                              0.431 |                             0.068 |                        0.331 |                           0.712 |                               0.999 |

## 7. Figures

### Step 0 Slot-Level Routing

![Step0 no-position slot-level heatmaps](figures/a05_03_no_pos_slot_init_inhibition_4gpu_20260608/slot_level_heatmaps/multi_b_primary_slot_level_heatmaps_step0.png)

Interpretation: random-init conditions start near balanced and low slot NMI; slot-init conditions start with visible slot-aligned structure before learning, but target accuracy is still near zero at step 0.

### Final Slot-Level Routing

![Final no-position slot-level heatmaps](figures/a05_03_no_pos_slot_init_inhibition_4gpu_20260608/slot_level_heatmaps/multi_b_primary_slot_level_heatmaps_final.png)

Interpretation: `S0-cos` keeps a clear slot x expert structure across all seeds, while `R1-dot` and `R1-cos` route most slots to one dominant expert despite high target accuracy.

## 8. Condition-Level Interpretation

`R0-dot` and `R0-cos`:

Baseline no-position routing is not clean specialization. Some seeds are balanced, but slot NMI remains weak to moderate and heatmaps are not stable one-slot-to-one-expert partitions.

`S0-dot`:

Dot-product slot-init improves slot NMI over `R0-dot`, but the effect remains modest and not clean enough to call robust specialization.

`S0-cos`:

Cosine slot-init is the strongest positive condition. All three seeds show high slot NMI, four active experts, high accuracy, and visually interpretable slot x expert structure. This supports slot-level routing specialization after removing positional embedding.

`R1-dot` and `R1-cos`:

Inhibition alone fails. It produces high feature-key consistency but low slot NMI and very high max-load. The heatmaps show one dominant expert column rather than slot specialization.

`S1-dot`:

Slot-init plus inhibition gives partial slot structure in dot-product routing, especially seed `20260521`, but the result is seed-dependent and not cleanly four-expert.

`S1-cos`:

Adding inhibition to cosine slot-init weakens the strongest condition. Final max-load rises and some seeds use only two or three experts, so this is not an improvement over `S0-cos`.

## 9. Answer To The Experiment Questions

Question: under no-position training, can slot-init produce specialization?

Answer: yes for slot-level routing when slot-init is paired with cosine routing. The best condition is `S0-cos`, with slot NMI 0.720-0.781 across seeds and accuracy 0.991-0.999. Dot-product slot-init is weaker.

Question: under no-position training, can inhibition produce specialization?

Answer: no. Inhibition alone collapses under both dot and cosine routers. It gives high consistency because assignments lock in, but the locked assignment is mostly a dominant-expert bucket.

Question: does slot-init plus inhibition improve over slot-init alone?

Answer: not reliably. `S1-dot` is partial and seed-dependent; `S1-cos` is clearly worse than `S0-cos`.

Question: is this exact feature-level specialization?

Answer: not yet. Exact `(slot, B_i)` NMI remains modest, including in `S0-cos`. The supported claim is slot-level route structure, not exact feature-key specialization or functional utility specialization.

## 10. Claim Boundary

Can claim:

- Absolute positional embedding is not required for target learning in this toy setting.
- After position removal, cosine slot-init alone can sustain seed-stable slot-level route structure.
- True token-conditioned inhibition does not solve collapse under no-position training and can amplify selected-expert lock-in.

Cannot claim:

- Inhibition is categorically useless; this only tests the current H0605a inhibition formulation and weights.
- `S0-cos` proves functional expert specialization; forced-routing utility is not the primary success criterion here.
- Exact `(slot, B_i)` feature-level specialization is solved.
- Removing position alone is enough for specialization.

## 11. Artifact Map

- Experiment dir: `Projects/from-attention-to-search/main/experiments/A05/A05_03_no_pos_slot_init_inhibition`
- Runner: `scripts/run_a05_03_no_pos_slot_init_inhibition.py`
- Submit script: `scripts/submit_a05_03_no_pos_slot_init_inhibition_4gpu_acp.sh`
- Config: `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/h0605a_true_token_conditioned_inhibition_replay.json`
- Full result dir: `results/a05_03_no_pos_slot_init_inhibition_4gpu_20260608`
- Full figure dir: `figures/a05_03_no_pos_slot_init_inhibition_4gpu_20260608`
- Primary seed table: `results/a05_03_no_pos_slot_init_inhibition_4gpu_20260608/tables/primary_metrics_by_seed.csv`
- Primary summary table: `results/a05_03_no_pos_slot_init_inhibition_4gpu_20260608/tables/primary_metrics_summary.csv`
- Final overview heatmap: `figures/a05_03_no_pos_slot_init_inhibition_4gpu_20260608/slot_level_heatmaps/multi_b_primary_slot_level_heatmaps_final.png`
- Step0 overview heatmap: `figures/a05_03_no_pos_slot_init_inhibition_4gpu_20260608/slot_level_heatmaps/multi_b_primary_slot_level_heatmaps_step0.png`
- ACP runtime log: `logs/acp/a05_03_no_pos_slot_init_inhibition_4gpu_20260608_runtime_20260608_064058.log`
- ACP job id: `pt-rzr278jh`

## 12. Next Decision

Treat `S0-cos` as the current positive no-position slot-structure control. Do not continue true token-conditioned inhibition as the main route to specialization unless the next experiment explicitly changes the lock-in mechanism or inhibition target.
