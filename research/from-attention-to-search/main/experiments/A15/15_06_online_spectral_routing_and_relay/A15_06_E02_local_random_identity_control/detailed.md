# A15_06_E02 detailed evidence ledger

Status: `complete`

Legacy experiment identifier: `A15_00_E02_local_random_identity_control`.

Scientific verdict: `fail_no_stable_covariance_identity_advantage`

## 1. Registered question

Does Local-HMT retain a 10B-token held-out NLL advantage when its covariance-ranked nested subspaces are replaced by fixed ambient rotations that preserve the complete target-motion geometry?

## 2. Immutable execution contract

- New arm: `local_random_matched`.
- New seeds: 17 and 29; completed E01 Local-HMT and Centered-Full runs are reused.
- Endpoint: optimizer step 12,716 = 10,000,269,312 training tokens.
- Hardware: one `n12lp.nn.i10a.8` node per run, 8×RTX 5090, SPOT quota.
- Frozen worker source: `/data/250010109/MoE_Router/experiments/20260804_online_spectral_local_random_matched_v2`.
- Worker manifest SHA-256: `90d44303af9c1ed78229e250f25053d5dd0020afa9bdd9cc06dc3fb2da96d4fb`.

## 3. Smoke and repair ledger

The first immutable smoke (`pt-hfdlb0gh`, v1) stopped at the second online refresh. The persisted Haar matrix was FP32 and was incorrectly reused as the numerical master, producing nested-flag orthogonality errors of \(8.35\times10^{-8}\), \(4.16\times10^{-7}\), and \(1.86\times10^{-7}\). No scientific result was produced.

The repair regenerates the same seed- and layer-specific Haar matrix deterministically in FP64 at every refresh; the FP32 buffer remains only for checkpoint and audit. It changes no arm, data, target, update cadence, guard, or outcome threshold.

The v2 smoke (`pt-qa7m357w`) passed fresh steps 0–2 and exact resume to step 3. It reproduced the E01 seed-17 step-0 public-parameter SHA and achieved maximum target-motion isometry error \(4.43\times10^{-15}\) radians. Two nonempty TensorBoard streams, checkpoints/evaluations at steps 0/2/3, and all six registered refresh rows were present. See [smoke_verdict.json](smoke_verdict.json).

## 4. Full-run ledger

| Seed | Job ID | Display name | Step-0 public-parameter SHA | Initial state |
| ---: | --- | --- | --- | --- |
| 17 | `om-ujy5kkld` | `osrt-10b-local-random-matched-s17` | `dd25272ba2e8c61917f7178adb0844de8892d4eef1bdcdf140a4e6cfe33eb7fe` | `SUCCEEDED`, 10B, zero retries |
| 29 | `om-anvg9bmj` | `osrt-10b-local-random-matched-s29` | `f6b2b0f1a324d95ce6f494cfec90393b8d5a6742fe9f4c59b32eed60c641e980` | `SUCCEEDED`, 10B, zero retries |

Both runs use the same frozen statistics, continuity-guard, and validation tensors as E01. Their source artifact SHA is `5c8cca2b0821f25b8e7abc50d7653dfba8d71e9ccf167fee61b82624116a52e4`; statistics, guard, and validation SHA values are recorded in each run's `telemetry/frozen_data_manifest.json`.

## 5. Endpoint evidence

All three arms use the same 1,024 validation documents. NLL is in nat/token and
lower is better.

| Arm | Seed 17 | Seed 29 |
| --- | ---: | ---: |
| Centered-Full | 3.6038433315 | 3.6025874202 |
| Local-HMT | 3.5987395669 | 3.6020274415 |
| Local-Random-Matched | 3.6041090941 | 3.6007556743 |

The registered paired contrasts use 2,000 document bootstrap draws:

| Contrast | Seed | Mean | 95% CI | Direction |
| --- | ---: | ---: | ---: | --- |
| Local-HMT − Local-Random | 17 | -0.00536953 | [-0.00685830, -0.00396873] | HMT better |
| Local-HMT − Local-Random | 29 | +0.00127177 | [-0.00026492, +0.00292497] | unresolved |
| Local-Random − Centered | 17 | +0.00026576 | [-0.00120773, +0.00174069] | unresolved |
| Local-Random − Centered | 29 | -0.00183175 | [-0.00343299, -0.00031532] | random better |

The two-seed equal-weight mean is descriptive only: Centered 3.60321538,
Local-HMT 3.60038350, and Local-Random 3.60243238. It is not used as a
population-level seed confidence interval.

## 6. Trajectory reading

In seed 17, the HMT-minus-random difference becomes -0.00331 at 4B, reaches
-0.00577 at 8B, and ends at -0.00537. In seed 29, HMT is better at several
middle milestones, but the difference shrinks to -0.00008 at 8B and reverses
to +0.00127 at 10B. The completed budget therefore does not support a simple
"HMT only needs longer training" explanation.

Local-Random is indistinguishable from Centered at the seed-17 endpoint and
better in seed 29. This is not a reproducible generic dynamic-subspace effect.

## 7. Target-motion and tracker audit

| Arm | Seed | Median \(\gamma\) | \(\gamma=0\) fraction | U64 deployed-target | U320 deployed-target | Max target-motion error |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Local-HMT | 17 | 0.0625 | 0 | 0.759624 | 0.866304 | n/a |
| Local-Random | 17 | 0.5 | 0 | 0.999990 | 0.999752 | \(1.22\times10^{-14}\) rad |
| Local-HMT | 29 | 0.0625 | 0 | 0.762304 | 0.866181 | n/a |
| Local-Random | 29 | 0.5 | 0 | 1.000000 | 0.999999 | \(5.79\times10^{-15}\) rad |

The random target is an exact motion isometry and is easier, not harder, for
the continuity-constrained updater to track. All registered comparability
guards pass. The smaller HMT step size is interpretable as greater route/logit
sensitivity to covariance-ranked directions; it is not a measure of expert
utility.

## 8. Typed decision

- Covariance identity pass requires both seed intervals below zero: **not met**.
- Tracking validity: **met for both seeds**.
- Final verdict: `fail_no_stable_covariance_identity_advantage`.

This means the registered covariance-specific claim is not supported. It does
not mean that covariance directions contain no information or that all
loss-aligned subspaces are ineffective.

## 9. Figure audit

- [Figure 1](figures/figure1_nll_trajectory.png): two-seed trajectories render
  all registered milestones and correctly use lower-is-better NLL.
- [Figure 2](figures/figure2_endpoint_delta_nll.png): all four endpoint paired
  contrasts and 95% intervals are legible; this is the decision figure.
- [Figure 3](figures/figure3_tracking_comparability.png): U64/U320 overlaps and
  zero-step fractions are legible and show that the random tracker was not
  disadvantaged.

All three PNG files were opened and visually inspected at native resolution on
2026-08-05.

## 10. Artifact map

- `tables/trajectory_nll.csv`: 3 arms × 2 seeds × 11 milestones.
- `tables/paired_delta_nll.csv`: both registered contrasts at every milestone.
- `tables/tracking_comparability.csv`: final tracking and refresh summaries.
- `tables/typed_verdict.json`: machine-readable registered verdict.
- Raw checkpoints, TensorBoard streams, JSONL telemetry, and per-document
  arrays remain under
  `/data/250010109/MoE_Router/outputs/online_spectral_router_training/`.

## 11. Claim boundary and next decision

The experiment adjudicates only this four-layer H768, 8-expert, top-1 DCLM,
two-seed, 10B setting. It does not establish universal H/M/T semantics,
larger-scale behavior, or expert specialization as the unique mediator.

The next decision is whether a loss-aligned discriminative side—defined by
expert relative utility rather than covariance rank—predicts held-out expert
choice regret or cross-update compatibility beyond native scores and matched
random controls before any further matched training.
