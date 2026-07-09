# Protocol: 11_09 All-Position Indirect-Transfer Dynamics

Status: proposed daily protocol.  
Anchor: `../anchors/11_09_all_position_indirect_transfer_dynamics_anchor.md`.

## 1. Purpose

Explain all-position indirect transfer:

```text
Why can K1/K2 or masked K3 make Z probe-readable even without direct h_T -> S_Z supervision?
```

The protocol separates direct native prediction from cross-position shared-parameter transfer.

## 2. Dataset

Use the clean `tau=3` data from A11_07:

```text
BR_z F00 ... F{L-1} U00 U01 U02 U03 A_SHARED C_SHARED S_z STOP
```

Decision prefix ends after `U03`.

## 3. Conditions

Reuse A11_07 conditions:

```text
K1_fixed_3head
K2_active
K3_full
K3_mask_decision_prefix_L3
K2_plus_decision_prefix_L3
```

Primary initialization:

```text
identical_branch / no-leakage initialization
```

## 4. Position Groups

Group losses into:

```text
decision_prefix_direct
positions_before_decision
positions_after_decision_before_A
positions_A_C
positions_at_or_after_Sz
shared_filler_positions
all_other_positions
```

The exact grouping may be adapted to the existing runner, but the direct decision-prefix term must be isolated.

## 5. Metrics

### 5.1 Group update contribution

For each condition, checkpoint, and position group:

1. clone model;
2. update only by that group's loss;
3. measure one-step finite differences.

Record:

```text
Delta_M_Z
Delta_E_Z
Delta_Q_proxy
Delta_native_H3_accuracy
Delta_local_Y1_CE
Delta_local_Y2_CE
```

### 5.2 Cross-kernel proxy

If feasible, compute Jacobian-vector product proxies for:

$$
\langle \nabla_{h_T}M_Z,-J_TJ_s^\top\nabla_{h_s}\ell_s\rangle.
$$

If exact Jacobians are too expensive, use the group finite-difference contribution as the decision metric.

### 5.3 Native / probe split

At every checkpoint report:

```text
Q(t)
native_H3_accuracy
M_Z_ref(t)
E_Z(t)
probe_accuracy
branch_swap
```

## 6. Procedure

1. Run or load A11_07-like checkpoints.
2. Verify leakage gate at step 0.
3. At selected checkpoints:

```text
step 0
first Q rise
T_0.9 if reached
final step
```

4. Run group-update diagnostics.
5. Compare predicted indirect-transfer source with actual `Q`, native H3, and `M_Z` trajectories.

## 7. Pass / Fail

### Support

```text
direct group dominates native_H3 and M_Z in direct conditions
non-direct conditions have positive Q-related transfer from non-decision groups
non-direct conditions remain low on native_H3 / M_Z
position-group contributions explain masked-vs-full differences
local guard passes
```

### Weaken

```text
no position group explains indirect recovery
direct group is not stronger than indirect groups for native_H3 / M_Z
Q and native_H3 are indistinguishable across conditions
local loss degradation explains recovery
```

## 8. Output Artifacts

Required:

```text
summary.md
detailed.md
group_contribution.csv
native_probe_split.csv
local_guard.csv
figures/group_delta_M.png
figures/native_vs_Q.png
figures/position_transfer_heatmap.png
run_config.json
```

## 9. Interpretation Boundary

If this protocol passes, the claim is:

```text
All-position non-direct recovery can be explained by cross-position shared-parameter transfer, while direct decision-prefix supervision is the path that reliably trains native h_T -> S_Z prediction and readout-effective margin.
```

It still does not prove indirect recovery is useless or that natural-language MTP is better.
