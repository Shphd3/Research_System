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
For general K, the first-order hidden-state semantic velocity is governed by
the vector sum of centered output directions over the covered informative
horizons, not by K size alone.
```

Latest evidence from 11_06 / 11_07 / 11_08 / 11_08b / 11_09:

```text
11_06 supports the one-step hidden-state margin mechanism: K3 has positive
G_M_hidden while K1/K2 are near zero. 11_07 supports direct decision-prefix
horizon-3 supervision as the stronger all-position path: direct conditions
reach native H3=1.0 and large M_Z_ref, while K1/K2/masked K3 can still recover
nontrivial Q through indirect transfer. Therefore Q alone is not direct
supervision evidence.
11_08 supports the general-K vector-sum mechanism: with the same K=4 and the
same two informative horizons, aligned horizon-3/horizon-4 output geometry has
G_hidden=0.015262, low/conflicting geometry has G_hidden=0.000954, and 5/5
seeds support aligned greater than low/conflict.
11_08b shows this is not only a step-0 artifact for the primary velocity
metric: with frozen heads, aligned still has early AUC G_hidden_ref=0.002660
while low/conflict has 0.000184, with 5/5 seed support. Trainable heads drift,
so trainable curves must record current geometry.
11_09 supports the next-K inclusion law: K2 is zero before the informative
horizon, K3 turns on at S_z, adding a shared H4 gives no one-step increment,
aligned H4 amplifies, and low/conflict H4 weakens.
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
11_06_readout_effective_margin_efficiency_anchor.md
11_07_no_leakage_all_position_efficiency_anchor.md
11_08_general_k_readout_margin_dynamics_anchor.md
```

Latest mechanism anchors:

```text
11_08b_output_geometry_dynamics_audit_anchor.md
11_09_next_k_inclusion_law_anchor.md
```

## Next Decision

Do not bridge to MoE yet. The current A11 line can now claim a controlled
next-K inclusion law for direct semantic velocity:

```text
Increasing K matters only when it newly includes an informative future horizon,
and the increment depends on centered output-direction alignment. Larger K by
itself is not the causal object.
```

Next decision: open A11_10 as a theory-closure problem for A11 itself. The
target is to prove or sharply bound when positive first-order semantic velocity
implies smaller semantic-margin hitting time or higher early recovery AUC:

```text
K=2 minimal theorem -> tau=m covering theorem -> general-K vector-sum /
next-K inclusion law -> finite-step efficiency under explicit optimization
assumptions.
```
