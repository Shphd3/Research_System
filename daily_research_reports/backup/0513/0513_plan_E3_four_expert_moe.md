# Experiment Plan 3 - Four-Expert MoE Specialization

## Decision Question
Can MoE routing recover four known planted features under the easiest controlled setting?

## Mainline Anchor
This is not yet a real-language claim. It is a diagnostic of whether a router can separate known synthetic mechanisms.

## Hypothesis
With four planted features and four experts, each expert should specialize to one feature if router learning aligns with feature identity.

## Setup
- Dataset: four-feature corpus that passed Plan 1.
- Model: same as dense baseline, replace FFN with 4-expert MoE.
- Routing: top-1 first; top-2 optional.
- Train multiple seeds.

## Metrics
- Expert purity: $P(f\mid e)$.
- Routing concentration: $P(e\mid f)$.
- NMI / ARI between feature ID and expert ID.
- Per-feature next-token accuracy.
- Expert load.
- Seed stability.

## Baselines
- Random routing.
- Hash/token-ID routing.
- Dense Transformer.
- Oracle feature router.

## Expected Outcomes and Claim Updates
Clean one-to-one expert-feature mapping:
- Claim: MoE can recover these synthetic features in an easy setting.
- Strength: supported for controlled synthetic data.

Mixed but better-than-random routing:
- Claim: weakly supported.
- Need further analysis of frequency, load balance, and token identity leakage.

No alignment:
- Claim: unsupported.
- Debug whether router sees the right signal or whether load balancing destroys specialization.

## Minimal Next Action
Run 5 seeds and produce a 4x4 matrix: rows = planted features, columns = experts, values = routing probability.
