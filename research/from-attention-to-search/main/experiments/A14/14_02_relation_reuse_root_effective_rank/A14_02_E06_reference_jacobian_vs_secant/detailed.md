---
experiment_id: A14_02_E06_reference_jacobian_vs_secant
status: completed_decisive
verdict: h11_finite_displacement_linearization_refuted
---

# Detailed Evidence: A14_02_E06 Reference Jacobian Versus Learned Secant

## 1. Decision Loop

**Question:** Did E05 fail because the reference-point Jacobian lacks a
shared cross-context image, or because one-point linearization cannot represent
the finite training displacement?

**Key comparison:** The reference-point trajectory Jacobian, its first-order
finite-update prediction, and the exact learned secant under the same
eight-direction budget.

**Direct result:** The secant positive control passed in 5/5 seeds; H11
refutation passed in 5/5 seeds; reference H9 was intermediate.

**Conclusion:** The finite-training failure is a large linearization remainder,
not evidence that the learned finite ROOT effect is high-dimensional.

**Cannot claim:** A single fixed instantaneous image exists along the entire
path or that NTP derives the finite-image condition.

**Decision:** Replace the finite-training point-Jacobian bridge with a
secant/path-integrated bridge.

## 2. Reference Construction And Metrics

The registered reference model holds embeddings, norms, output head, and all
non-target parameters at their final values while reverting the target block
to initialization. Thus

\[
\Delta\theta
=
\theta_T^{\mathrm{block}}-\theta_0^{\mathrm{block}}
\]

is the only finite displacement between reference and endpoint.

The point prediction is

\[
\widehat{\Delta h}(x)
=
J_\rho(x;\theta_{\mathrm{ref}})
G_{\mathrm{traj}}G_{\mathrm{traj}}^\top\Delta\theta,
\]

and the exact secant is

\[
\Delta h_{\mathrm{sec}}(x)
=
h_\rho(x;\theta_T)-h_\rho(x;\theta_{\mathrm{ref}}).
\]

H11 error is the dimensionless Frobenius ratio

\[
R_{\mathrm{lin}}
=
\frac{\|
\widehat{\Delta H}-\Delta H_{\mathrm{sec}}
\|_F}
{\|\Delta H_{\mathrm{sec}}\|_F}.
\]

It measures the complete finite Taylor mismatch; it does not identify which
internal attention or normalization term caused curvature.

## 3. Frozen Realization And Eligibility

E06 retains E05's data, model, optimizer-trajectory subspace, block
intervention, eight-direction budget, and numerical contract. Development
seed 120 was excluded. Confirmation seeds 20--24 were fresh.

All five seeds:

- achieved 1.0 seen, held-out calibration, and held-out test accuracy;
- achieved 1.0 nuisance consistency;
- passed top-eight trajectory-energy and parameter-delta-capture gates;
- passed block relevance, full replay, and finite-difference gates;
- passed the exact-secant spectral, transfer, CE, and accuracy positive
  controls.

| Provenance item | Value |
| --- | --- |
| Execution | local active container; configured device `cuda` |
| Visible hardware | 2 × NVIDIA H100 80GB HBM3; one serial runner |
| Python / Torch / CUDA | 3.10.12 / 2.3.0a0+nv24.04 / 12.4 |
| Bootstrap replicates | 10,000 |
| Config SHA-256 | `3e7b44f1b984ee8e535df8fedac434984d74e694c782205924b978a755f12105` |

Confirmation command:

```text
python active/tree_low_rank/scripts/run_reference_jacobian_vs_secant.py \
  --config active/tree_low_rank/configs/a14_02_e06_reference_jacobian_vs_secant.yaml \
  --output-dir active/tree_low_rank/results/a14_02_e06_reference_jacobian_vs_secant/confirmation_v1
```

The implementation was executed from the current uncommitted research
worktree; no Git revision is claimed. Exact source, resolved configuration,
per-seed metrics, spectra, training curves, and checkpoints remain in the raw
result directory.

## 4. Per-Seed Results

| Seed | Reference tail | Reference transfer | Secant tail | Secant transfer | Secant captured by reference | \(R_{\mathrm{lin}}\) | H11 refuted |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 20 | 0.1834 | 0.8166 | 0.0099 | 0.9901 | 0.3723 | 1.0970 | yes |
| 21 | 0.1753 | 0.8247 | 0.0365 | 0.9635 | 0.3809 | 1.0335 | yes |
| 22 | 0.1294 | 0.8706 | 0.0023 | 0.9977 | 0.2445 | 0.8010 | yes |
| 23 | 0.2020 | 0.7980 | 0.0078 | 0.9922 | 0.2332 | 1.6959 | yes |
| 24 | 0.0829 | 0.9171 | 0.0289 | 0.9711 | 0.2367 | 1.6704 | yes |

Reference H9 support required tail at most \(0.10\) and transfer at least \(0.85\)
in four seeds. Only seed 24 passed. Refutation required tail at least \(0.25\)
or transfer at most \(0.70\) in four seeds; no seed failed that strongly.
Reference H9 is therefore intermediate.

## 5. Aggregate Decision

| Metric | Mean | Bootstrap 95% interval |
| --- | ---: | ---: |
| Reference tail | 0.1546 | [0.1123, 0.1892] |
| Reference transfer | 0.8454 | [0.8108, 0.8877] |
| Secant tail | 0.0171 | [0.0060, 0.0292] |
| Secant transfer | 0.9829 | [0.9708, 0.9940] |
| Secant captured by reference | 0.2935 | [0.2369, 0.3503] |
| Linearization relative error | 1.2595 | [0.9532, 1.5659] |
| Linearized excess CE | 0.4797 nat | [0.1259, 0.8872] |
| Secant-projection excess CE | 0.00022 nat | [0.00002, 0.00046] |

The frozen H11 refutation threshold was \(R_{\mathrm{lin}}\ge0.50\), reference
capture at most \(0.70\), linearized excess CE at least \(0.20\) nat, or accuracy
drop at least \(0.05\), conditional on the secant positive control. Every seed
crossed at least one criterion, yielding
`h11_finite_displacement_linearization_refuted`.

Mean linearized accuracy drop was \(0.1090\), whereas secant-image projection
changed accuracy in zero seeds. Direct projection into the reference image
increased CE by \(0.4041\) nat on average. Mean central-difference disagreement
was \(7.64\times10^{-6}\), excluding Jacobian probe error.

### 5.1 Post-registered complete-displacement rival audit

The registered linear prediction uses
\(G_{\mathrm{traj}}G_{\mathrm{traj}}^\top\Delta\theta\). Although that subspace
captured mean \(0.9975\) of parameter-delta energy and E05 established its
functional sufficiency, a small high-gain residual remained a possible rival.
Using the same saved E06 checkpoints, a post-registered guard therefore
computed the directional derivative along the complete normalized block
displacement and multiplied it by \(\|\Delta\theta\|_2\).

| Guard | Mean | Seed agreement |
| --- | ---: | ---: |
| Full-delta linearization relative error | 1.2441 | H11 refuted 5/5 |
| Full-delta linearized excess CE | 0.4148 nat | Registered refutation remains |
| Eight-dimensional projected-parameter excess CE | 0.00180 nat | Function preserved 5/5 |
| Full-direction finite-difference disagreement | \(1.39\times10^{-6}\) | Numerical guard passes 5/5 |

Thus the omitted trajectory-subspace residual does not explain the
linearization failure. The projected parameter model remains functionally
equivalent, while the complete-direction point derivative still fails. This
audit uses the same checkpoints and final-test split, so it is a rival
separation check rather than independent confirmation; it does not alter the
frozen E06 decision rule or verdict.

## 6. Mathematical Interpretation

Along the straight target-block path

\[
\theta(t)=\theta_{\mathrm{ref}}+t\Delta\theta,
\]

the fundamental theorem of calculus gives

\[
\Delta h_{\mathrm{sec}}(x)
=
\int_0^1
J_\rho(x;\theta(t))\Delta\theta\,dt.
\]

A point hypothesis

\[
J_\rho(x;\theta_{\mathrm{ref}})G
\approx B_{\mathrm{ref}}A_x
\]

does not constrain the integrated effect unless the Jacobian remains stable or
the Taylor remainder is bounded. E06 directly measures that missing remainder
and finds it order one.

The empirically supported finite object is instead

\[
\Delta h_{\mathrm{sec}}(x)
\approx B_{\mathrm{sec}}a_x,
\]

where \(B_{\mathrm{sec}}\) is fit on calibration secants and transfers to test.
This is a sufficient bridge to fixed-readout functional rank without a
one-point Taylor approximation. It remains an empirical condition, not a
deduction from NTP alone.

## 7. Gate Ledger

| Gate | Result |
| --- | --- |
| Capability / nuisance consistency | 5/5 pass |
| Trajectory energy / parameter capture | 5/5 pass |
| Block relevance | 5/5 pass |
| Finite-difference / full replay | 5/5 pass |
| Secant positive control | 5/5 pass |
| Reference H9 support | 1/5; intermediate |
| Reference H9 refutation | 0/5 |
| H11 finite-displacement refutation | 5/5 |

## 8. Artifact Map

### Curated

- [Seed table](tables/seed_summary.csv)
- [Complete-displacement guard table](tables/full_delta_guard_seed_summary.csv)
- [Complete-displacement guard decision](tables/full_delta_guard.json)
- [Central figure](figures/reference_jacobian_vs_secant.png)
- [Chinese summary](summary_cn.md)

### Frozen implementation

- [Configuration](../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/configs/a14_02_e06_reference_jacobian_vs_secant.yaml)
- [Runner](../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/scripts/run_reference_jacobian_vs_secant.py)
- [Post-registered full-delta guard](../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/scripts/audit_e06_full_delta_guard.py)
- [Shared trajectory utilities](../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/src/tree_low_rank/trajectory_jacobian_closure.py)
- [Tests](../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/tests/test_trajectory_jacobian_closure.py)

### Raw confirmation evidence

- [Result directory](../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/results/a14_02_e06_reference_jacobian_vs_secant/confirmation_v1)
- [Decision JSON](../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/results/a14_02_e06_reference_jacobian_vs_secant/confirmation_v1/decision.json)

## 9. Visualization Audit

The central figure uses all five confirmation seeds and shows frozen green
support and red refutation thresholds. Spectral tails, captures, and relative
errors are dimensionless; CE effects are reported in the tables in nat. The
figure directly supports the contrast between an intermediate point image and
a concentrated finite secant; it does not claim pathwise basis constancy.
