# A16_00_01_E01 detailed evidence ledger

Status: `complete`

Scientific verdict: `necessary_only`

## 1. Registered question

With model parameters, tokens, layers, and checkpoints frozen, is the true
token-shared Router-input component a direction-specific immediate cause of
Vanilla-Full's deep hard-route concentration, and is restoring the saved
center sufficient to damage a separately trained Centered-Full Router?

The primary test changes only a constant input/logit component. It does not
run counterfactual experts or estimate language-model loss.

## 2. Immutable contract

- Protocol revision: `2026-08-09-v1`, approved before implementation.
- Model: four Transformer blocks, hidden size 768, eight sparse experts, one
  shared expert, top-1 routing, linear bias-free Gate.
- Arms: `vanilla_full` and `centered_full`, seed 17.
- Registered steps: 0, 64, 127, 318, 636, 1272, 12716, 25432.
- Primary cells: layers 3/4 at all registered nonzero steps, 14 cells per arm.
- Source training objective in both arms: \(L_{LM}+0.01L_{LB}\) from step 0.
- Counterfactuals: independent-mean removal for Vanilla; saved-center add-back
  for Centered; cyclic wrong-layer and 256 matched random shifts.
- Random shifts match \(\|C_EWd\|_2\), not raw input norm.
- Independent unit: one of 1,024 validation documents; layers/checkpoints are
  fixed repeated views, not replicates.

The checkpoint list and every SHA-256 are in
[checkpoint_manifest.csv](tables/checkpoint_manifest.csv).

## 3. Data identity

Immutable tensor source:
`/data/250010109/MoE_Router/experiments/20260802_a15_01_04_progressive_band_source_2b_5090/artifacts/eval_tokens.pt`.

| Object | Selection | Tokens | SHA-256 |
| --- | --- | ---: | --- |
| source artifact | full file | n/a | `5c8cca2b0821f25b8e7abc50d7653dfba8d71e9ccf167fee61b82624116a52e4` |
| statistics | `wos[0:512,:128]` | 65,536 | `6dd7b83df791c75dd62307b4256acc9d399ed2df8df32ef79e68cb0fb16b930f` |
| validation | `dclm[0:1024,:1024]` | 1,048,576 | `91acad820e5521832a4e54033fd062d4d275819856725d9803981c0c972a289c` |

Statistics activations fit means only. Validation activations produce all
route, margin, LB, bootstrap, and random-null evidence.

## 4. Implementation and execution ledger

Worker root:
`/data/250010109/MoE_Router/experiments/20260808_online_spectral_router_30b_v2/`.

Raw result root:
`/data/250010109/MoE_Router/outputs/online_spectral_router_training/analysis/A15_00_E04_vanilla_centered_lb_dc_audit/`.

The raw path retains the legacy A15 identifier; the curated record migrated to A16 without renaming immutable worker artifacts.

Execution used two local NVIDIA H100 80GB GPUs, one arm per GPU. There was no
remote job submission and no source training was modified. The full extraction
finished at 2026-08-09 04:16 UTC in the first pass; all 16 cells were re-run
after the secondary-output conformance repair described below.

Representative full command pattern:

```bash
PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python \
PYTHONPATH=/data/250010109/dependency_packages/hf_transformers_qwen3:src:runtime \
python scripts/evaluate_lb_dc_counterfactual.py \
  --arm <vanilla_full|centered_full> --step <registered_step> \
  --device <cuda:0|cuda:1> --batch-size 16 \
  --statistics-docs 512 --validation-docs 1024 --random-draws 256
```

Registered aggregation used 2,000 bootstrap draws and seed `2026080901`.

Core final source SHA-256 values:

| Source | SHA-256 |
| --- | --- |
| `lb_dc_audit.py` | `1cf7223ea48656af32f1d3038a5534b092083e9e7c71ec06d06ffb5886ef28e4` |
| `test_lb_dc_audit.py` | `1fd8affa3af75b18d4d5361dee49ddf5355af06d5a70603f0adacaff85336533` |
| `evaluate_lb_dc_counterfactual.py` | `db1fa6e754738cea491381ba37329cb68d93c554c9e0e2d01fba6445048cb61d` |
| `aggregate_lb_dc_audit.py` | `e2e05e2ce6482f1d5e7d7e91641c2df9d75037cc7e41d8c1c123917b1c716e71` |
| `plot_lb_dc_audit.py` | `9342895b5f00343b244478bb95b355667ed20796c285636f912dfcbaf5571070` |

## 5. Test, smoke, and conformance ledger

The math core was implemented test-first. Seven initial tests passed for hard
use, margins, Switch loss, analytic gradient, gradient saturation, matched
random shifts, wrong-layer rescaling, document bootstrap, and typed verdict.
Together with routing/runtime regression tests the initial suite passed 17/17.

Both arms passed step-127 smoke: actual Router-input relation error 0, native
logit replay error 0, and native top-1 agreement 1.0. The aggregator also
rejected an intentionally incomplete smoke tree rather than aggregating a
subset.

After first unseal, a contract audit found that two registered secondary
fields—route flip and DC native-margin support—were not persisted. Amendment
A1 records the post-unseal status and non-decision-bearing scope. A new literal
test failed by missing import before implementation and passed afterward. The
final combined suite passed 18/18. Both step-127 smokes and all 16 full cells
were then re-extracted. Every compressed primary array retained its original
SHA-256; the registered point estimates, intervals, random q95 values, and
typed verdict reproduced exactly.

## 6. Registered primary result

For Vanilla, the effect is deployed max share minus mean-removed max share.
For Centered, it is center-added max share minus deployed max share.

| Direction | Point | 95% CI | Random q95 | True-effect percentile | Wrong-layer mean | Pass? |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Vanilla mean removal | 0.68677868 | [0.68434587, 0.68921626] | 0.18326419 | 100.00% | 0.42767252 | yes |
| Centered center add-back | 0.14224522 | [0.14009882, 0.14446344] | 0.22587986 | 6.64% | 0.22070244 | no |

Typed verdict: `necessary_only`.

The label means immediate necessity for maintaining the registered frozen
Vanilla collapse. It does not mean historical causal necessity throughout
training. The inverse failure is informative: Centered learned a different
\(W\)/representation state, so adding a constant center after training is not
the inverse of training without centering.

## 7. Checkpoint trajectory

| Tokens | Vanilla L3 deployed → mean removed | Vanilla L4 deployed → mean removed | Centered L3 deployed → center added | Centered L4 deployed → center added |
| ---: | ---: | ---: | ---: | ---: |
| 50M | 0.9869 → 0.6630 | 0.9775 → 0.5488 | 0.2152 → 0.5962 | 0.1999 → 0.3858 |
| 100M | 0.9992 → 0.2767 | 0.9991 → 0.2999 | 0.2058 → 0.9188 | 0.2441 → 0.4709 |
| 250M | 1.0000 → 0.2325 | 1.0000 → 0.3350 | 0.3541 → 0.5412 | 0.2104 → 0.3258 |
| 1B | 1.0000 → 0.1856 | 0.9988 → 0.3955 | 0.2917 → 0.3584 | 0.1989 → 0.2580 |
| 10B | 0.9998 → 0.1858 | 0.9971 → 0.2511 | 0.2732 → 0.2271 | 0.2315 → 0.2398 |
| 20B | 0.9991 → 0.2050 | 0.9978 → 0.2150 | 0.2702 → 0.2256 | 0.2393 → 0.2065 |

The Centered treatment is large during the earliest interval but is not
direction-specific relative to matched random shifts; at 10B/20B it is near
zero or reverses. This is a path-adaptation signature, not bidirectional static
sufficiency.

## 8. Secondary route and margin diagnostics

Across the 14 primary cells:

| Arm | Mean treatment route flip | Mean fraction whose native winner is favored by true DC | Mean of cell median DC/native-margin ratio |
| --- | ---: | ---: | ---: |
| Vanilla | 0.726342 | 0.997545 | 1.090161 |
| Centered | 0.269998 | 0.560165 | 0.187814 |

For Vanilla, the same DC-only expert matches the deployed dominant expert in
all primary layer-3/layer-4 cells. The high support fraction and ratio show
that the constant offset coherently sustains current winners; they do not show
which training gradient created that alignment.

## 9. LB penalty and local leverage

The registered mean over primary cells is:

| Arm/condition | Switch LB | Sample-scaled LB logit-gradient RMS | Mean margin |
| --- | ---: | ---: | ---: |
| Vanilla deployed | 6.86062 | 0.27368 | 5.05920 |
| Vanilla mean removed | 1.10182 | 0.10341 | 0.43586 |
| Centered deployed | 1.15585 | 0.05786 | 2.45916 |
| Centered center added | 1.59856 | 0.14473 | 2.46888 |

The aggregate gradient value does not support the broad H3 prediction that
native Vanilla always has less local leverage than the centered
counterfactual. The trajectory is heterogeneous. At 50M--100M, native
Vanilla leverage can be large while collapse forms. At 250M/500M, layer 4 has
LB near 7.94/7.99 but gradient RMS only 0.0335/0.0311, demonstrating local
softmax saturation in that layer. Layer 3 later rises again to 0.335/0.356 at
10B/20B. A high penalty is therefore not a direct measure of corrective force,
but gradient death is not universal either.

These derivatives are \(N\,\partial L_{LB}/\partial z\) before multiplying by
\(\lambda_{LB}=0.01\). They deliberately exclude the LM gradient, Gate-input
Jacobian, AdamW moments, and expert feedback.

## 10. Figure audit

- [Figure 1](figures/figure1_route_concentration_counterfactual.png) uses a
  symlog token axis so 50M--1B and 10B--20B remain visible; it shows frozen
  concentration, not NLL or historical causality.
- [Figure 2](figures/figure2_registered_effect_vs_random_null.png) is the
  decision figure. Green bars are document-bootstrap intervals and purple
  lines are matched-random q95 thresholds.
- [Figure 3](figures/figure3_lb_penalty_and_gradient_dynamics.png) separates LB
  penalty magnitude from analytic local logit leverage.

All three images were opened at native resolution after final rendering on
2026-08-09. Titles, axes, legends, early-stage spacing, and allowed-claim
boundaries were visually checked. Plot contracts are in
[plot_contracts.json](figures/plot_contracts.json).

## 11. Artifact map

- [condition_metrics.csv](tables/condition_metrics.csv): all arm × checkpoint
  × layer × condition route, margin, LB, and local-gradient metrics.
- [cell_effects.csv](tables/cell_effects.csv): true/random/wrong-layer effects,
  center geometry, route flip, and DC-margin support.
- [typed_verdict.json](tables/typed_verdict.json): registered aggregate,
  bootstrap interval, random q95, and typed decision.
- [checkpoint_manifest.csv](tables/checkpoint_manifest.csv): exact source
  checkpoints and SHA-256 values.
- Worker `cells/`: 16 JSON records plus 16 compressed per-document/random-null
  arrays, 5.2 MB total.
- Worker `analysis/input_manifest.json`: SHA-256 map of all decision inputs.

Raw arrays, logs, checkpoints, and model states remain in the worker/output
surfaces and are not copied into Research_System.

## 12. Claim boundary and next decision

Established: the true common component is a direction-specific immediate
sustainer of current Vanilla collapse; Centered training changes the learned
state enough that center add-back is not direction-specific sufficiency.

Not established: historical unique causality, expert/NLL consequences of the
offline reassignment, optimal centering estimator, optimal LB coefficient, or
whether the LM gradient, LB gradient, optimizer, or expert feedback first
creates the DC alignment.

Exactly one next decision is an early step-0--127 paired gradient/optimizer
audit. It must measure LM-only and LB-only Gate gradients, DC/residual
projections, the applied AdamW update, hard \(f\), soft \(p\), margins, and expert
loss advantage on the same batches. Its completion criterion is to identify
which term explains the growth of the dominant expert margin before selecting
one matched repair.
