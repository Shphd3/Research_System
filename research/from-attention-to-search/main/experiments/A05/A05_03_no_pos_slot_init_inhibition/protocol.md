# A05_03 No-Position Slot-Init And Inhibition Supplement

## Goal

Test whether slot initialization or true token-conditioned inhibition can produce slot/feature-level routing specialization after absolute positional embedding is removed throughout training.

## Decision Question

When the fixed position source is excluded, do slot-init and/or inhibition make the router assign slots to experts in a seed-stable, non-collapsed way?

## Tested Hypothesis

If the earlier failure was mainly caused by positional common shift, then removing positional embedding should allow slot-init or inhibition to produce higher slot-expert alignment than the no-position random baseline.

## Rival Explanation

If final routing remains collapsed or seed-dependent after removing positional embedding, then position is not the only blocker; ordinary top-1 lock-in, router geometry, or assignment-utility mismatch still prevents stable specialization.

## Data And Model

- Original H0605a uniform multi-B setting.
- Full-sequence next-token prediction.
- Routed position: logical `B_i` position.
- Absolute positional embedding is set to zero and frozen from model initialization.
- Slot-init calibration also uses the no-position model.

## Conditions

All conditions are run with no positional embedding:

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

## Seeds

`20260521, 20260522, 20260523`

## Primary Metrics

- `route_slot_nmi_feature_eval`: whether expert assignment carries slot information on the balanced feature-key grid.
- slot×expert heatmap per seed: human-readable evidence for specialization or collapse.
- `expert_load_max_fraction`: collapse guard, not specialization.
- `target_accuracy_feature_eval`: validity guard.

## Secondary Metrics

- `route_feature_key_nmi`: whether exact `(slot, B_i)` feature identity is captured.
- `feature_key_consistency`: whether each exact feature key is routed consistently.
- `within_slot_main_expert_diversity`: whether B identities fragment routing inside a slot.

## Success

Slot-init and/or inhibition show high slot NMI with non-collapsed expert load and high target accuracy across seeds.

## Failure

Slot NMI remains low, or high NMI appears only in collapsed/low-accuracy seeds.

## Insufficient Evidence

Any condition lacks seed-level metrics, final heatmaps, or valid target accuracy.

## Claim Boundary

This experiment can test whether no-position slot-init/inhibition is sufficient for slot-level routing structure. It cannot prove functional expert specialization unless forced-routing utility also agrees with the routing partition.
