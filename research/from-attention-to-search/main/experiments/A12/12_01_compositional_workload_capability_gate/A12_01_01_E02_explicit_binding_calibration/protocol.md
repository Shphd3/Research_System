# Protocol: A12_01_01_E02 Explicit-Binding Calibration

## 0. Approval Snapshot

**Approval status:** approved under the user's blocker-resolution instruction.  
**Purpose:** remove within-row binding as the identified calibration blocker.  
**Primary metric:** minimum five-seed unseen-pair test answer accuracy.  
**Setup:** role-specific atomic pair tokens; two layers, width 64, at most 3000 NTP steps; globally disjoint splits.  
**Pass:** answer `>=0.70` and format `>=0.95` in `5/5`; each one-table control `<0.25`.  
**Fail:** full-task test remains below threshold with valid training.  
**Insufficient:** split overlap, missing rows, or control failure.  
**Cannot claim:** long-context or language behavior.

## 1. Definitions

`P1_i_j` and `P2_i_j` are atomic tokens encoding a mapping and its table role. This changes serialization, not the latent function \(Y=\pi_2(\pi_1(A))\).

## 2. Data And Model

Train/validation/test use globally disjoint individual permutations. Each input contains eight `P1` tokens, eight `P2` tokens, query entity, format instruction, and decision token. Model: two-layer, width-64, four-head causal Transformer; AdamW `3e-4`; batch 64; early stop at validation `0.70` or step 3000.

## 3. Decision

Judge only independent test accuracy and one-table replacement controls. Passing opens an A12_02 rerun; no capacity or curriculum claim follows directly.
