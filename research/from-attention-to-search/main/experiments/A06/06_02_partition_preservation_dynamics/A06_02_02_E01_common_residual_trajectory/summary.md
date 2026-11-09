# Summary: A06_02_02_E01 Router Common-Residual Trajectory Audit

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

Protocol: `protocol.md`

## Result Snapshot

**Decision: H1 is weakened under the protocol's robustness rule.**

The four-GPU full run reproduced the A06_01_04_E03 real-DCLM proxy-route collapse:
`raw_center` starts with high proxy-route NMI at step 0, then collapses by
steps 5/10 while LM loss remains comparable to random. However, the collapse
is **not** robustly explained as common-dominated router-gap movement. The
mean-common projector shows \(\Lambda_{\mathrm{upd}}>1\), but the top hidden-PC
and router-row projectors show \(\Lambda_{\mathrm{upd}}<1\), meaning the
conclusion flips by common definition.

Therefore the updated hypothesis is narrower:

```text
real-DCLM collapse is real and margin/sign-flip fragility is visible,
but "router updates are common-dominated" is not yet a stable mechanism claim.
The next model must define the relevant common operator more sharply, likely
through the training objective or gradient/router-update geometry rather than
through a generic common subspace.
```

## Exact Setup

- Real-DCLM binary token stream: `/data/share/109_cache_dir/hf_data/dclm_bin`.
- Qwen3-style top-1 MoE, 6 layers, 8 experts, hidden size 512.
- Audit layers: 3, 4, 5.
- Seeds: `0, 1, 2`.
- Variants: `random`, `equal_norm_random`, `raw_center`, `residual_center`.
- Checkpoints: `0, 1, 2, 3, 5, 10, 20, 50`.
- Full run job: `pt-i3bkewya`.
- Run name: `a06_22_router_common_residual_trajectory_4gpu_20260630_full01`.
- Coverage: 864 trajectory rows, 48,384 pair rows, 288 snapshot rows.
- Maximum decomposition identity error: `8.37e-7`.

## Terminology / Definitions

**Proxy-route NMI:** normalized mutual information between fixed step-0 proxy
labels and top-1 expert routes. It measures route preservation, not expert
utility.

**Common-over-residual update dominance:** the ratio
\(\Lambda_{\mathrm{upd}}\) comparing router-gap update magnitude along a common
projector versus the corresponding residual feature direction.

**Common projector:** the chosen definition of the common subspace. This run
uses mean-common, top hidden-PC, and router-row subspace projectors.

## Key Evidence

### The real-DCLM proxy-route collapse was reproduced.

| Step | Proxy-route NMI | Matched preserve min | Max route load | LM loss |
|---:|---:|---:|---:|---:|
| 0 | 0.7549 | 0.6754 | 0.1812 | n/a |
| 5 | 0.0410 | 0.0037 | 0.9479 | 11.1926 |
| 10 | 0.0131 | 0.0002 | 0.9645 | 10.7222 |
| 50 | 0.0337 | 0.0000 | 0.7575 | 7.8827 |

Loss guard: raw-center minus random loss is only `+0.0040` at step 5 and
`+0.0032` at step 10. This is not a training crash.

![Proxy-route NMI reproduction](figures/full01_proxy_route_nmi_reproduction.png)

What this figure tests: whether the A06_02_02_E01 full run reproduces the A06_01_04_E03
collapse before interpreting common/residual decomposition.

Observed result: `raw_center` starts high and collapses by step 5/10.

Take-home: the audit is running on the correct failure regime.

### Common dominance appears only under the mean-common projector.

| Common projector | \(\Lambda_{\mathrm{upd}}@5\) | \(\Lambda_{\mathrm{upd}}@10\) | Step-0 residual margin min | Interpretation |
|---|---:|---:|---:|---|
| mean-common | 2.1507 | 1.9856 | 0.6493 | common-dominated under global mean |
| top hidden-PC | 0.7089 | 0.6666 | 0.0324 | residual-dominated under high-variance hidden subspace |
| router-row subspace | 0.4611 | 0.4332 | -0.1839 | residual-dominated under router-relative subspace |

![Projector lambda step 5 and 10](figures/full01_projector_lambda_step5_step10.png)

What this figure tests: whether common-over-residual dominance is stable
across common definitions.

Observed result: the sign of the judgment flips. Mean-common passes, while
top hidden-PC and router-row projectors fail.

Take-home: H1 does not pass the robustness rule.

### Sign flips and residual-margin fragility remain informative.

The `raw_center` sign-flip rate reaches `0.4147` at step 5 and `0.4782` at
step 10. Step-0 residual margin is also projector-sensitive: it is strongly
positive under mean-common, near zero under top hidden-PC, and negative under
router-row subspace.

![Raw-center lambda trajectory](figures/full01_raw_center_lambda_trajectory.png)

What this figure tests: the trajectory of \(\Lambda_{\mathrm{upd}}\) during the
same window in which NMI collapses.

Observed result: mean-common stays above 1, while the other two projectors
remain below 1.

Take-home: collapse aligns with margin/sign-flip fragility, but not with a
projector-robust common-dominated update claim.

## Interpretation

**H1 common-trajectory:** weakened. The full run supports a mean-common
version of the story but rejects the stronger claim that router-gap updates
are robustly common-dominated.

**H2 residual-margin insufficiency:** partially supported. The high-gain and
router-relative projectors expose weak or negative step-0 residual margin, but
the mean-common projector does not. This suggests residual fragility is real
but still depends on the common operator definition.

**H3 projector robustness:** weakened. The common definition is now an active
modeling bottleneck.

## Claim Boundary

Can claim:

- A06_02_02_E01 reproduces the real-DCLM raw-center proxy-routing collapse.
- The collapse is accompanied by large sign-flip rates and matched-preserve
  failure.
- The common-over-residual update interpretation is not robust across common
  projectors.

Cannot claim:

- Common-dominated router updates are the established root cause.
- Generic common subtraction will preserve routing.
- Residual long-tail directions are useless.
- The result validates a new gating method or expert utility.

## Next Decision

Do not proceed directly to a new gating method from the current H1. The next
research move should define a sharper common operator tied to the training
objective, gradient, or router-update geometry, and then rerun the same
common/residual decomposition with that operator.
