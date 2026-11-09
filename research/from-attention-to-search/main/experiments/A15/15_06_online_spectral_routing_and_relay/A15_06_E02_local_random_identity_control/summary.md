---
experiment_id: A15_06_E02_local_random_identity_control
legacy_experiment_id: A15_00_E02_local_random_identity_control
status: complete
scientific_verdict: fail_no_stable_covariance_identity_advantage
last_updated: 2026-08-05
---

# Final result summary

## Direct conclusion

The registered experiment does **not support a stable benefit from covariance-rank
identity**. Local-HMT clearly beat the motion-matched local random subspace in
seed 17, but seed 29 reversed in point estimate and its paired interval crossed
zero. The random target preserved the HMT target motion to numerical precision
and was not harder for the online tracker to deploy, so the typed verdict is
`fail_no_stable_covariance_identity_advantage`, not insufficient.

## Decisive 10B evidence

NLL is held-out next-token negative log likelihood in nat/token; lower is
better. Each contrast pairs the same 1,024 validation documents and uses 2,000
bootstrap draws.

| Contrast | Seed 17, 95% CI | Seed 29, 95% CI | Verdict |
| --- | ---: | ---: | --- |
| Local-HMT − Local-Random | \(-0.005370\) [\(-0.006858,-0.003969\)] | \(+0.001272\) [\(-0.000265,+0.002925\)] | covariance identity fail |
| Local-Random − Centered-Full | \(+0.000266\) [\(-0.001208,+0.001741\)] | \(-0.001832\) [\(-0.003433,-0.000315\)] | no stable generic-subspace benefit |

![Endpoint paired contrasts](figures/figure2_endpoint_delta_nll.png)

The fixed ambient rotation preserved target principal-angle motion with maximum
error \(1.23\times10^{-14}\) radians. Random deployed-target U64/U320 overlap was
approximately 1.0, versus 0.76/0.87 for HMT, and neither arm selected
\(\gamma=0\). Thus the negative verdict is not caused by a harder random tracker.
HMT required smaller accepted update steps, which shows greater routing
sensitivity to covariance-ranked directions but does not establish utility.

## Boundary and next decision

This closes only the registered four-layer, two-seed, 10B attribution: fixed
covariance H/M/T identity is not a reproducible functional routing coordinate.
It does not show that covariance directions contain no information, nor does it
test loss-aligned Fisher or expert-utility coordinates. The next decision is to
test whether an expert-utility discriminative side predicts held-out expert
regret or cross-update compatibility beyond native Router scores and matched
random controls before any further matched training.
