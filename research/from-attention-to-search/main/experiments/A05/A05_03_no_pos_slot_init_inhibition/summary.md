# A05_03 No-Position Slot-Init And Inhibition Summary

## 0. One-Line Verdict

After removing absolute positional embedding throughout training, cosine slot-init alone produces the clearest seed-stable slot-level routing structure, while inhibition alone still drives near-collapse.

## 1. Question

Does slot initialization or true token-conditioned inhibition produce feature-level expert specialization once the fixed position source is removed?

Operational answer:

- slot-level specialization means expert assignment carries slot identity, measured by `route_slot_nmi_feature_eval` and seed-level slot x expert heatmaps.
- exact feature-level specialization means expert assignment carries exact `(slot, B_i)` identity, measured by `route_feature_key_nmi`.
- load balance is only a collapse guard; it is not specialization.

## 2. Setup

- Data: original H0605a uniform multi-B setting.
- Training: full-sequence next-token prediction, 1600 steps.
- Seeds: `20260521`, `20260522`, `20260523`.
- Device/job: 4GPU ACP job `pt-rzr278jh`, status `SUCCEEDED`.
- Position intervention: `pos_emb.weight` was zeroed and frozen from initialization for every model, including slot-init calibration.
- Audit: all 24 final checkpoints have `pos_emb.weight` norm 0.0 and max absolute value 0.0.

## 3. Primary Result

| Condition | Slot-init | Inhibition | Router | Slot NMI mean/std | Exact feature NMI mean | Max-load mean | Accuracy mean | Verdict |
|---|---:|---:|---|---:|---:|---:|---:|---|
| `R0-dot` | no | no | dot | 0.239 / 0.065 | 0.391 | 0.400 | 0.997 | weak baseline structure |
| `S0-dot` | yes | no | dot | 0.395 / 0.048 | 0.397 | 0.432 | 0.988 | slot-init helps, but weak |
| `R1-dot` | no | yes | dot | 0.080 / 0.021 | 0.220 | 0.912 | 0.998 | inhibition-only collapse |
| `S1-dot` | yes | yes | dot | 0.564 / 0.135 | 0.388 | 0.509 | 0.996 | partial and seed-dependent |
| `R0-cos` | no | no | cosine | 0.274 / 0.102 | 0.390 | 0.462 | 0.994 | weak baseline structure |
| `S0-cos` | yes | no | cosine | 0.741 / 0.028 | 0.416 | 0.385 | 0.996 | strongest slot-level result |
| `R1-cos` | no | yes | cosine | 0.069 / 0.045 | 0.215 | 0.922 | 0.999 | inhibition-only collapse |
| `S1-cos` | yes | yes | cosine | 0.431 / 0.068 | 0.331 | 0.712 | 0.999 | inhibition weakens slot-init |

## 4. Key Figure

![Final no-position slot-level heatmaps](figures/a05_03_no_pos_slot_init_inhibition_4gpu_20260608/slot_level_heatmaps/multi_b_primary_slot_level_heatmaps_final.png)

Reading: rows are slots and columns are experts; `S0-cos` keeps a near one-slot-to-one-expert pattern across all three seeds, while `R1-dot` and `R1-cos` concentrate most slots into one dominant expert.

## 5. Interpretation

Slot-init:

- `S0-cos` gives the clearest positive evidence that, after position removal, slot-aligned initialization can sustain slot-level routing structure.
- `S0-dot` improves over the dot baseline but remains weak.

Inhibition:

- Inhibition alone does not create specialization under no-position training.
- Instead, `R1-dot` and `R1-cos` have very high final max-load, so inhibition still amplifies selected-expert lock-in.
- Adding inhibition to slot-init is not reliably helpful: `S1-dot` is partial and seed-dependent; `S1-cos` is worse than `S0-cos`.

## 6. Claim Boundary

Can claim:

- Removing position does not make inhibition sufficient.
- Cosine slot-init without inhibition is the strongest current no-position route-structure intervention.
- The supported positive result is slot-level routing structure, not exact `(slot, B_i)` feature-level specialization.

Cannot claim:

- Functional expert specialization, because forced-routing utility agreement was not the primary success criterion here.
- Exact feature-level specialization, because `route_feature_key_nmi` remains modest.
- That position removal alone solves final specialization.

## 7. Next Decision

Use `S0-cos` as the positive no-position slot-structure control, and do not continue inhibition as the main anti-collapse intervention without a separate lock-in fix.

