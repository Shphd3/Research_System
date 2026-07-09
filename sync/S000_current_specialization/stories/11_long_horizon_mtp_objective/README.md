# Long-Horizon MTP Objective Story

This folder owns the project-local story for the A11 long-horizon MTP objective line.

Active story:

```text
story_cn.md
```

Current role:

```text
A11 is a supporting objective-mechanism line. It studies whether multi-token prediction can directly and efficiently shape a current prefix hidden state to retain a delayed semantic variable. It does not by itself prove natural-language benefit, MoE routing preservation, semantic expert identity, or expert utility.
```

Current completed-anchor decomposition:

```text
11_01_k2_branch_delayed_next_two_anchor.md
11_02_two_token_shared_trunk_signal_interference_anchor.md
11_03_k2_semantic_efficiency_anchor.md
11_04_k3_first_informative_horizon_anchor.md
11_05_semantic_efficiency_bridge_anchor.md
11_06_readout_effective_margin_efficiency_anchor.md
11_07_no_leakage_all_position_efficiency_anchor.md
11_08_general_k_readout_margin_dynamics_anchor.md
11_08b_output_geometry_dynamics_audit_anchor.md
11_09_next_k_inclusion_law_anchor.md
```

Current boundary:

```text
11_06 supports the first-order hidden readout-margin mechanism. 11_07 supports
direct decision-prefix horizon-3 supervision as stronger than indirect-only
controls under no-leakage all-position training. However, all-position indirect
transfer can still make Z probe-readable, so Q alone is not direct-supervision
evidence. A11_08 supports the general-K vector-sum mechanism: under fixed K=4
and the same two informative horizons, aligned output directions produce much
higher hidden-state semantic velocity than low/conflicting output directions.
A11_08b shows this hidden-velocity mechanism is not only a step-0 artifact
under frozen output heads. A11_09 supports the next-K inclusion law: semantic
velocity turns on when K first covers an informative horizon, shared added
horizons add no direct one-step semantic increment, aligned informative
horizons amplify, and low/conflict informative horizons weaken. This supports
direction-dependent next-K efficiency, not "larger K is always better."
```

Current next theoretical decision:

```text
Do not bridge to MoE in the next A11 step. First write A11_10 as a theory
closure problem: turn the K=2 minimal theorem, the tau=m covering rule, and the
general-K vector-sum / next-K inclusion law into one finite-step efficiency
statement. The missing link is from positive first-order semantic velocity to
smaller semantic-margin hitting time or higher early recovery AUC under explicit
optimization assumptions.
```

Versioned story snapshots:

```text
archive/YYYYMMDD_A11_<anchor-range-or-last-anchor>_<short_topic>/story_cn.md
```

Naming rule:

```text
YYYYMMDD: snapshot date.
A11: research line prefix.
<anchor-range-or-last-anchor>: use an anchor range such as 06_to_08 when the
snapshot summarizes several newly integrated anchors, or the last anchor id
such as 08 when the snapshot mainly records one new result.
<short_topic>: lower-case, underscore-separated, mechanism-bearing topic.
```

Current versioned snapshot:

```text
archive/20260709_A11_06_to_08_general_k_vector_sum/story_cn.md
```

Reading order:

1. `story_cn.md` for line-level synthesis.
2. `archive/20260709_A11_06_to_08_general_k_vector_sum/story_cn.md` for the 2026-07-09 A11_06-to-A11_08 versioned snapshot.
3. `../../problem_anchors/11_long_horizon_mtp_objective/README.md` for adjudicable anchors.
4. `../../experiments/A11/.../protocol.md`, `summary.md`, and `detailed.md` for execution and evidence.
