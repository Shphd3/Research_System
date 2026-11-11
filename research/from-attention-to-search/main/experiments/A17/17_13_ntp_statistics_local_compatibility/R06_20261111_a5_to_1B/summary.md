# R06 A5 continuation to the native1B optimizer step

AI analysis; researcher judgment Unknown. A5 continued the complete R04 update-2000 state for1816updates to update3816, read from the native baseline's1B manifest. A5 processed1000341504validtokens versus1000000000for the original baseline, a0.03415% difference. Model, optimizer, scheduler, RNG, cursor and bias were retained. H100microbatch16/accumulation2, or authorized5090microbatch8/accumulation4, retains262144validtokens per update.

| pair            | band    |   difference |    ci95_low |   ci95_high |   documents |   replicates |
|:----------------|:--------|-------------:|------------:|------------:|------------:|-------------:|
| A5-MoE_baseline | overall |  -0.01630202 | -0.01911774 | -0.01267266 |        1871 |         2000 |
| A5-Dense        | overall |  -0.10852696 | -0.11271646 | -0.10355351 |        1871 |         2000 |

P10: 支持. Native-trajectory P12 remains insufficient because the exact native update-2000 checkpoint was not retained. The R03 full-batch A0 proxy yields post-window Jaccard0.281250, compared with prior-pair median0.630952; its numeric branch is 支持. Historical partial masks and different window durations remain confounds.

A5 endpoint NLL3.763121999, native3.779426355, Dense3.871651564; hard concentration medians1.338417415/1.049242805. Complete learning, forgetting, hysteretic mastery, gross flows, concentration and step-lead tables are in the accompanying Chinese Detailed record. Paired document bootstrap measures evaluation sampling only. Sparse native checkpoints can miss hidden acquisition/forgetting cycles. Single seed; teacher-dependent dispatch; hint leakage not excluded. Analysis ran inside the retained Reserved job, not MIG; existing native1B caches were reused. No other training, old-asset edits, commit or push.
