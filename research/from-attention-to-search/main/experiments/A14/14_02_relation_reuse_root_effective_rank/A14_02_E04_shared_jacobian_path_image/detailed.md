---
experiment_id: A14_02_E04_shared_jacobian_path_image
status: completed_supported
verdict: supported_registered_local_h9
---

# Detailed Evidence: A14_02_E04 Shared Jacobian / Path Image

## 1. Decision Loop

**Question:** Does one learned mapping have a shared low-dimensional local
ROOT Jacobian image across unseen alias--entity combinations and nuisance
contexts?

**Key comparison:** Calibration-estimated trained task-gradient directions
versus equal-dimensional random directions and the same task probe at
initialization.

**Direct result:** The trained task probe passed both H9 thresholds in 5/5
eligible seeds.

**Conclusion:** Local context sharing exists at the trained point.

**Cannot claim:** The same point image represents the finite optimizer path or
the complete final ROOT.

**Decision:** Follow the actual optimizer trajectory in E05.

## 2. Registered Objects And Metrics

For each example \(x\), let

\[
Z_x=J_\rho(x;\theta_T)G_m\in\mathbb R^{64\times8}.
\]

\(G_m\) is the top-eight right-singular subspace of per-example answer-loss
gradients for the first Transformer block, fit on calibration examples only.
The primary spectral-tail fraction is

\[
\tau_J^2(8)
=
\frac{\sum_{i>8}\lambda_i(C_{\mathrm{test}})}
{\sum_i\lambda_i(C_{\mathrm{test}})},
\qquad
C_{\mathrm{test}}
=
\frac1{8n}\sum_x Z_xZ_x^\top.
\]

It is dimensionless and measures energy outside the best joint
eight-dimensional test image. It does not measure task sufficiency.

Let \(\widehat B_{\mathrm{cal}}\) be the top-eight calibration image. Transfer is

\[
R_{\mathrm{cal}\to\mathrm{test}}
=
\frac{\sum_x\|
\widehat B_{\mathrm{cal}}\widehat B_{\mathrm{cal}}^\top Z_x
\|_F^2}
{\sum_x\|Z_x\|_F^2}.
\]

It is a dimensionless held-out energy fraction. It prevents fitting the image
on test but does not establish stability along training.

## 3. Frozen Realization

| Item | Value |
| --- | --- |
| Model | one pre-norm causal block, one head, width 64, FF 128 |
| Objective | full-position NTP cross-entropy |
| Sequence | `ALIAS ENTITY CONTEXT ROOT ANSWER` |
| Task | one shared non-identity permutation |
| Aliases / entities / contexts | 16 / 8 / 32 |
| Held-out cells | 2 of 8 entities per alias, balanced |
| Task/Jacobian dimension | 8 |
| Probe parameters | first block Q/K/V/O and MLP weights, 32,960 scalars |
| Confirmation seeds | 0--4 |
| Probe dtype / step | float64 / \(5\times10^{-3}\) versus half step |
| Bootstrap replicates | 10,000 |
| Execution | local active container; configured device `cuda` |
| Visible hardware | 2 × NVIDIA H100 80GB HBM3; one serial runner |
| Python / Torch / CUDA | 3.10.12 / 2.3.0a0+nv24.04 / 12.4 |
| Config SHA-256 | `7817f143e8440e088e7f8994716762035face88d9dc98db8bc56a0e67b12827d` |

Train, calibration, and test context sets are relation-specific and disjoint.
Every context token is trained elsewhere, avoiding an untrained-token
confound. The checkpoint is selected from calibration capability only.

Confirmation command:

```text
python active/tree_low_rank/scripts/run_shared_jacobian_path_image.py \
  --config active/tree_low_rank/configs/a14_02_e04_shared_jacobian_path_image.yaml \
  --output-dir active/tree_low_rank/results/a14_02_e04_shared_jacobian_path_image/confirmation_v1
```

The implementation was executed from the current uncommitted research
worktree; no Git revision is claimed. Exact source, resolved configuration,
per-seed metrics, spectra, and checkpoints are retained below.

## 4. Primary Result

| Seed | Test tail | Cal-to-test capture | Top-8 gradient energy | Eligible | H9 support |
| ---: | ---: | ---: | ---: | --- | --- |
| 0 | 0.0515 | 0.9485 | 0.9999 | yes | yes |
| 1 | 0.0146 | 0.9854 | 0.9337 | yes | yes |
| 2 | 0.0458 | 0.9542 | 0.9709 | yes | yes |
| 3 | 0.0339 | 0.9661 | 0.9808 | yes | yes |
| 4 | 0.0506 | 0.9494 | 0.9553 | yes | yes |

Aggregate:

| Metric | Mean | Bootstrap 95% interval | Frozen support rule |
| --- | ---: | ---: | --- |
| Test tail \(\tau_J^2(8)\) | 0.0393 | [0.0259, 0.0500] | \(\le0.10\) |
| Cal-to-test capture | 0.9607 | [0.9500, 0.9741] | \(\ge0.85\) |

The registered verdict is `supported_registered_model`.

## 5. Guard And Rival Audit

### Capability

All five seeds achieved 1.0 seen accuracy, 1.0 held-out calibration accuracy,
1.0 held-out test accuracy, and 1.0 nuisance consistency.

### Numerical validity

Mean central finite-difference disagreement was \(0.0113\) and every seed was
below \(0.05\). Exact fixed-image controls had effectively zero tail and unit
transfer; context-rotated controls had about \(0.856\) tail and \(0.12\) captured
energy. The metric therefore detected both registered extremes.

### Random and initialization controls

The equal-dimensional random parameter subspace had mean test tail \(0.2206\),
far above the task result. The task probe at initialization had mean tail
\(0.1421\). The improvement at the trained point is consistent with learned,
task-specific organization rather than an unavoidable architectural rank
ceiling.

### Output-visible versus head-null energy

![Output-visible and frozen-head-null Jacobian energy](figures/visible_null_energy.png)

Mean visible and null energy fractions were \(0.3617\) and \(0.6383\). The visible
tail was numerically zero because the answer-contrast row space has dimension
at most seven. The null component's mean tail was still only \(0.0313\), so the
complete H9 result is not explained solely by the answer bottleneck.

### Complete-ROOT projection

Projecting the complete final ROOT into \(\widehat B_{\mathrm{cal}}\) produced
mean excess CE \(0.6367\) nat and mean accuracy drop \(0.0357\). This guard
correctly rejects the stronger but unregistered claim
\(h_\rho(x;\theta_T)\in\operatorname{Col}(B_m)\).

## 6. Development-Only Numerical Repair

Development seed 100 exposed float32 cancellation for small random-direction
finite differences. Before any confirmation seed was inspected, probing was
changed to float64 and the step was frozen at \(5\times10^{-3}\) versus half
step, the first development pair below the \(0.05\) disagreement gate. No data,
model, scientific threshold, or confirmation result was used in this repair.

## 7. Artifact Map

### Curated

- [Seed table](tables/seed_summary.csv)
- [Primary figure](figures/jacobian_tail_and_transfer.png)
- [Visible/null figure](figures/visible_null_energy.png)
- [Chinese summary](summary_cn.md)

### Frozen implementation

- [Configuration](../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/configs/a14_02_e04_shared_jacobian_path_image.yaml)
- [Core probe](../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/src/tree_low_rank/jacobian_path_image.py)
- [Runner](../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/scripts/run_shared_jacobian_path_image.py)
- [Tests](../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/tests/test_jacobian_path_image.py)

### Raw confirmation evidence

- [Result directory](../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/results/a14_02_e04_shared_jacobian_path_image/confirmation_v1)
- [Decision JSON](../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/results/a14_02_e04_shared_jacobian_path_image/confirmation_v1/decision.json)

## 8. Visualization Audit

The primary figure shows all five seeds, both frozen decision thresholds, the
registered trained task probe, and the two named controls. Axes use
dimensionless energy fractions. The figure supports only local image sharing;
the functional boundary is stated in text rather than inferred from the
scatter.
