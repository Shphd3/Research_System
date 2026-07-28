# Protocol: A11_19 Bridge-Token-Conditioned Transport

## 0. Approval Snapshot

**Purpose:** test whether A11_18's one-position sign reversal is specific to `Decision`.  
**Role:** robustness/root-cause audit.  
**Primary metric:** per-bridge normalized-usefulness AUC over steps `20-200`.  
**Conditions:** four fixed one-token bridges; five NTP trajectories.  
**Cannot claim:** all-token or long-generation transport.

## 1. Fixed And Changed Variables

Fixed: Qwen model, NTP trajectory, prompt, train examples, H2 loss gradient, H1 readout, state-position distance, seeds, checkpoints, optimizer, and parameter set.

Changed only during diagnostic teacher forcing:

| Bridge | Token ID | Role |
|---|---:|---|
| ` Decision` | 40425 | original |
| ` Answer` | 21806 | answer format |
| ` Therefore` | 15277 | discourse continuation |
| `:` | 25 | punctuation format |

## 2. Metric And Decision

$$
\widehat U_b
=-\frac{\langle\nabla M_{1,T+1}^{(b)},g_D^S\rangle}
{\|\nabla M_{1,T+1}^{(b)}\|\|g_D^S\|}.
$$

- robust negative transport: every bridge AUC positive in at most `1/5`;
- token-conditioned: `Decision` positive in at most `1/5` and at least one alternative positive in `4/5`;
- mixed otherwise;
- insufficient if central signs fail all four cells in fewer than `4/5`, hashes fail, or original `Decision` does not reproduce A11_18 within `0.02` mean normalized usefulness at shared checkpoints.

## 3. Outputs

- four bridge trajectories and per-seed AUC table;
- central derivative sign table;
- original-bridge reproduction audit;
- canonical summary, detailed, anchor, story update.

## 4. Boundary

Alternative bridges are diagnostic counterfactuals, not separately trained conditions. The result describes local pretrained transition geometry only.
