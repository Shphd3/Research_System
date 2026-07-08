# Protocol: A11_07 No-Leakage All-Position Efficiency

Status: proposed follow-up protocol after A11_06.  
Anchor: `Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_07_no_leakage_all_position_efficiency_anchor.md`.

## 1. Purpose

Test whether the readout-effective margin mechanism from A11_06 becomes a multi-step semantic-efficiency advantage in all-position LM-style training, after controlling initialization leakage.

The protocol asks:

```text
Does direct decision-prefix horizon-3 supervision reduce time-to-recovery or improve early AUC beyond indirect all-position transfer, while preserving local Y1/Y2 learning?
```

## 2. Dataset

Use clean `tau=3` data:

```text
BR_z F00 ... F{L-1} U00 U01 U02 U03 A_SHARED C_SHARED S_z STOP
```

Targets at decision prefix:

```text
Y1 = A_SHARED
Y2 = C_SHARED
Y3 = S_z
```

## 3. Conditions

| Condition | Loss scope | Purpose |
|---|---|---|
| `K1_fixed_3head_all_position` | all-position offset 1 | NTP baseline with matched heads |
| `K2_active_all_position` | all-position offsets 1,2 | non-covering MTP baseline |
| `K3_full_all_position` | all-position offsets 1,2,3 | direct + indirect condition |
| `K3_mask_decision_prefix_L3` | K3 all-position, but remove decision-prefix `h_T -> S_z` term | indirect-only K3 control |
| `K2_plus_decision_prefix_L3` | K2 all-position plus only decision-prefix horizon-3 term | direct-term sufficiency test |

Use identical branch / branch-collapsed initialization as primary. Random initialization is only a boundary diagnostic.

## 4. Leakage Gate

Before interpreting any speed metric, require:

```text
Q(0) <= 0.35 for m=4 branches
native horizon-3 accuracy near chance
M_Z(0) near 0
E_Z(0) near 0
branch-swap consistency near chance
```

If this gate fails, report the run as leakage-saturated and do not use `T_0.9` as evidence.

## 5. Metrics

### 5.1 Guarded recovery

$$
Q(t)=\min\{A(t),P(t),S(t)\}.
$$

Report:

```text
T_0.9: earliest step where Q(t) >= 0.9 for 3 consecutive evals
early AUC_Q: average Q over the early window
final Q
reach rate across seeds
```

### 5.2 Readout-effective margin trajectory

$$
M_Z(t)=\frac1m\sum_z(u_{S_z}^{(3)}-\bar u)^\top h_T(z,t).
$$

Report:

```text
M_Z(0)
M_Z(t) curve
early AUC_M
Delta M_Z from step 0 to first eval
```

### 5.3 Branch separation energy

$$
E_Z(t)=\frac{1}{2m^2}\sum_{z,z'}\|h_T(z,t)-h_T(z',t)\|^2.
$$

Report:

```text
E_Z(0)
E_Z(t) curve
```

### 5.4 Local guard

Report:

```text
Y1 CE and accuracy
Y2 CE and accuracy
global active loss
structured-position active loss
```

### 5.5 Native informative prediction

Report:

```text
native_h3_accuracy
native_h3_target_probability
worst_branch_h3_probability
```

## 6. Training Setup

Default:

```text
num_branches = 4
filler_length = 16 and optionally 64
shared_context_length = 4
max_horizon = 3
seeds = 971, 972, 973, 974, 975
steps = 15000
eval_interval = 250 or 500
lambda3 = 1.0, optional second-stage sweep {0.25, 0.5, 1.0}
```

Do not run broad K sweeps. Do not add MoE routing in this protocol.

## 7. Main Comparisons

### 7.1 Direct term sufficiency

Compare:

```text
K2_active_all_position
K2_plus_decision_prefix_L3
```

Support if adding only the decision-prefix horizon-3 term improves `T_0.9`, early AUC_Q, and M_Z trajectory.

### 7.2 Direct term necessity within K3

Compare:

```text
K3_full_all_position
K3_mask_decision_prefix_L3
```

Support if masking the direct term delays recovery or lowers early AUC / final Q.

### 7.3 Full K comparison

Compare:

```text
K1_fixed_3head_all_position
K2_active_all_position
K3_full_all_position
```

Support if K3 remains strongest after leakage gate and local guard.

## 8. Pass / Fail Criteria

### Strong support

```text
leakage gate passes
K2_plus_direct matches or approaches K3_full
K3_masked is weaker than K3_full
K3_full has smaller T_0.9 or higher early AUC_Q than K1/K2
M_Z(t) separates in the same direction as Q(t)
Y1/Y2 local guard passes
```

### Partial support

```text
Direct conditions improve M_Z but Q does not separate clearly.
```

Claim only mechanism-level geometry, not training efficiency.

### Weaken

```text
indirect-only controls match direct conditions after leakage control
M_Z does not predict Q
local targets degrade under direct conditions
```

### Insufficient evidence

```text
Q(0) is saturated or leakage gate fails.
```

## 9. Output Artifacts

Required:

```text
summary.md
detailed.md
condition_summary.csv
leakage_audit.csv
q_curves.csv
margin_curves.csv
local_guard.csv
native_h3.csv
figures/q_curves.png
figures/margin_curves.png
figures/leakage_gate.png
figures/local_guard.png
run_config.json
```

`summary.md` must begin with leakage-gated `T_0.9` and early AUC, not final Q alone.

## 10. Interpretation Boundary

If the protocol passes, the claim is:

```text
In controlled clean tau=3 all-position training without initialization leakage, direct decision-prefix informative-horizon supervision improves semantic recovery efficiency beyond indirect transfer.
```

It still does not prove natural-language benefit, larger-K monotonicity, or MoE expert utility.
