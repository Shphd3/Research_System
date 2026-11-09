---
experiment_id: A14_02_E05_trajectory_jacobian_closure
status: completed_refuted
verdict: eight_dimensional_trajectory_closure_refuted
---

# Detailed Evidence: A14_02_E05 Trajectory Jacobian Closure

## 1. Decision Loop

**Question:** Does E04's local image cover the parameter directions actually
used during learning and the finite ROOT effect caused by those directions?

**Key comparison:** Eight-dimensional optimizer-trajectory parameter
projection versus endpoint-Jacobian projection of the exact block effect.

**Direct result:** Parameter projection was functionally exact, but
endpoint-image projection failed the registered closure rule in 4/5 seeds.

**Conclusion:** Low-dimensional learning and low-dimensional finite ROOT
change coexist with a rotating or otherwise nonlocal parameter-to-ROOT map.

**Cannot claim:** Endpoint H9 alone explains the finite learned effect.

**Decision:** Move the Jacobian to the block-reverted reference model and
measure the Taylor remainder directly in E06.

## 2. Registered Objects

The selected block parameter vector was recorded every five AdamW steps. For
increments

\[
u_t=\theta_{t+5}^{\mathrm{block}}-\theta_t^{\mathrm{block}},
\]

\(G_{\mathrm{traj}}\) is the top-eight right-singular subspace of the uncentered
increment matrix.

The exact block effect holds every other parameter at its final value:

\[
\Delta h_{\mathrm{block}}(x)
=
h_\rho(x;\theta_T)-h_\rho(x;\theta_{\mathrm{rev}}),
\]

where \(\theta_{\mathrm{rev}}\) reverts only the target block to initialization.
This finite difference is not a Taylor approximation.

The key closure test compares this exact effect to the calibration image of

\[
J_\rho(x;\theta_T)G_{\mathrm{traj}}.
\]

## 3. Frozen Realization

E05 retains E04's one-layer model, task, capability gates, context splits,
float64 central differences, and eight-direction budget. It uses fresh
development seed 110 and fresh confirmation seeds 10--14. All confirmation
seeds passed capability, numerical, full-replay, trajectory-energy, and
selected-block relevance gates.

| Provenance item | Value |
| --- | --- |
| Execution | local active container; configured device `cuda` |
| Visible hardware | 2 × NVIDIA H100 80GB HBM3; one serial runner |
| Python / Torch / CUDA | 3.10.12 / 2.3.0a0+nv24.04 / 12.4 |
| Bootstrap replicates | 10,000 |
| Config SHA-256 | `a49c26669183a9413509bf20c111abfc70ef286388de9dfc11924f5e800e9828` |

Confirmation command:

```text
python active/tree_low_rank/scripts/run_trajectory_jacobian_closure.py \
  --config active/tree_low_rank/configs/a14_02_e05_trajectory_jacobian_closure.yaml \
  --output-dir active/tree_low_rank/results/a14_02_e05_trajectory_jacobian_closure/confirmation_v1
```

The implementation was executed from the current uncommitted research
worktree; no Git revision is claimed. Exact source, resolved configuration,
per-seed metrics, spectra, training curves, and checkpoints remain in the raw
result directory.

## 4. Ordered Result Audit

### 4.1 Parameter trajectory

Mean top-eight increment-spectrum energy was \(0.9019\). The projection of the
complete block displacement into \(G_{\mathrm{traj}}\) captured \(0.9975\) of its
squared norm, with bootstrap 95% interval \([0.9950,0.9998]\).

Replacing the final block parameters by the projected displacement changed
answer CE by only \(0.00026\) nat on average, 95% interval
\([0.000005,0.000483]\), with zero accuracy drop in all seeds. Thus the
eight-dimensional parameter description is not a spectral artifact; it
preserves the trained function.

### 4.2 Block relevance

Reverting the complete block increased CE by \(1.3965\) nat and reduced accuracy
by \(0.2244\) on average. The selected block therefore made a nontrivial causal
contribution.

### 4.3 Endpoint Jacobian versus exact block effect

| Seed | Parameter capture | Endpoint \(J\) tail | Endpoint transfer | Exact effect tail | Endpoint image captures exact effect | Base-preserving excess CE |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | 0.9999 | 0.2330 | 0.7670 | 0.0020 | 0.4173 | 0.0988 |
| 11 | 0.9997 | 0.1003 | 0.8997 | 0.0481 | 0.3342 | 0.4788 |
| 12 | 0.9946 | 0.0870 | 0.9130 | 0.0057 | 0.3287 | 0.2047 |
| 13 | 0.9997 | 0.2520 | 0.7480 | 0.0028 | 0.2922 | 0.1654 |
| 14 | 0.9935 | 0.1052 | 0.8948 | 0.0076 | 0.4637 | 0.1584 |

The exact block effect had mean tail \(0.0132\) and calibration-to-test capture
\(0.9868\). The endpoint Jacobian image captured only \(0.3672\) of this effect,
bootstrap 95% interval \([0.3152,0.4266]\).

### 4.4 Functional closure

The base-preserving intervention

\[
\widetilde h
=
h_{\mathrm{rev}}
+P_J(h_T-h_{\mathrm{rev}})
\]

increased CE by \(0.2212\) nat on average, with bootstrap 95% interval
\([0.1333,0.3534]\), and reduced accuracy by \(0.0137\). Four seeds crossed at
least one registered closure-refutation threshold.

In contrast, fitting an eight-dimensional calibration image directly to the
exact block effect changed CE by only \(0.00020\) nat and never changed
accuracy. Projecting the complete final ROOT, rather than only the block
effect, increased CE by \(0.7381\) nat. Together these controls show that:

- the exact finite effect is low-dimensional and functionally sufficient;
- the endpoint Jacobian image is the failed object;
- base ROOT variation must remain outside the projected block effect.

Mean finite-difference disagreement was \(2.26\times10^{-5}\), excluding probe
noise as the explanation.

## 5. Gate Ledger

| Gate | Result |
| --- | --- |
| Capability and nuisance consistency | 5/5 pass |
| Trajectory top-eight energy | 5/5 pass |
| Parameter-delta capture | 5/5 pass |
| Block relevance | 5/5 pass |
| Finite-difference agreement | 5/5 pass |
| Projected-parameter functional replay | 5/5 pass |
| Endpoint-Jacobian closure | 4/5 refute |
| Formal verdict | `eight_dimensional_trajectory_closure_refuted` |

## 6. Artifact Map

### Curated

- [Seed table](tables/seed_summary.csv)
- [Central figure](figures/trajectory_closure.png)
- [Chinese summary](summary_cn.md)

### Frozen implementation

- [Configuration](../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/configs/a14_02_e05_trajectory_jacobian_closure.yaml)
- [Core utilities](../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/src/tree_low_rank/trajectory_jacobian_closure.py)
- [Runner](../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/scripts/run_trajectory_jacobian_closure.py)
- [Tests](../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/tests/test_trajectory_jacobian_closure.py)

### Raw confirmation evidence

- [Result directory](../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/results/a14_02_e05_trajectory_jacobian_closure/confirmation_v1)
- [Decision JSON](../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/results/a14_02_e05_trajectory_jacobian_closure/confirmation_v1/decision.json)

## 7. Visualization Audit

The central figure uses all five seeds and shows the registered parameter,
Jacobian-tail, and frozen-head functional thresholds. CE is measured in nat;
capture and spectral-tail values are dimensionless fractions. The plot does
not by itself distinguish H9 from H11; E06 performs that distinction.
