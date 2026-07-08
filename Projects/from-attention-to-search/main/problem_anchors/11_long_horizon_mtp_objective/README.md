# Long-Horizon MTP Objective Anchors

This folder owns adjudicable anchors for the A11 long-horizon MTP objective line.

Current active story:

```text
../../stories/11_long_horizon_mtp_objective/story_cn.md
```

## Current Boundary

A11 can claim a controlled representation guarantee and a controlled efficiency-mechanism direction:

```text
If K covers the first informative future horizon tau and the covered target is a one-to-one code S_Z for the early variable Z, low loss at that horizon forces h_T to contain Z. In the minimal trainable-prefix model, the covering horizon also gives strictly positive first-order readout-effective semantic margin growth, while non-covering horizons give zero under the collapsed-prefix assumptions.
```

A11 cannot claim:

```text
MTP universally outperforms NTP.
NTP cannot learn long-horizon information.
Larger K is always better.
The controlled result proves natural-language benefit or MoE expert utility.
```

## Active Anchors

Existing completed or evidence-updated anchors:

```text
11_01_k2_branch_delayed_next_two_anchor.md
11_02_two_token_shared_trunk_signal_interference_anchor.md
11_03_k2_semantic_efficiency_anchor.md
11_04_k3_first_informative_horizon_anchor.md
11_05_semantic_efficiency_bridge_anchor.md
```

New next anchors:

```text
11_06_readout_effective_margin_efficiency_anchor.md
11_07_no_leakage_all_position_efficiency_anchor.md
```

## Next Decision

Run 11_06 first. Do not broaden to K>3 or MoE routing before the one-step readout-effective margin mechanism is adjudicated.
