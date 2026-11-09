# Protocol: A11_17 Interface-Paraphrase Usefulness Decomposition

## 0. Approval Snapshot

**Approval status:** approved under standing instruction.  
**Purpose:** split A11_16's negative held-out common-H1 usefulness into interface/position and paraphrase-transfer components.  
**Experiment role:** root-cause audit.  
**Primary metric:** four-cell sign table $\widehat U_{a,s}$.  
**Minimal setup:** five NTP trajectories only; no new method or ablation.  
**Cannot claim:** global MTP efficiency or external transfer.

## 1. Fixed Contract

- exact A11_16 model, tokenizer, prompt task, train/eval paraphrase split, H2 copy, NTP training objective, AdamW configuration, seeds, batch schedule, and checkpoints;
- conditions: only `ntp_all_h1`, seeds `971-975`;
- diagnostic checkpoints `0,20,100,200,300`;
- same 10-example train and 10-example evaluation diagnostic batches;
- labels/paraphrases `5/5`, option order `6/4`, all five domains and two states.

## 2. Four Margins And One Gradient

At each checkpoint, compute one shared gradient:

$$
g_D^S=\nabla_{\theta_S}L_D(D_{tr}).
$$

Compute four margins and gradients:

| Cell | Interface / position | Wording split | Question |
|---|---|---|---|
| H2-train | H2 at $h_T$ | seen | does direct supervision help its own training margin? |
| H2-eval | H2 at $h_T$ | unseen | does H2 direction generalize across paraphrases? |
| H1-train | standard H1 at $h_{T+1}$ | seen | does the direction transfer across interface/position? |
| H1-eval | standard H1 at $h_{T+1}$ | unseen | full downstream transport; reproduces A11_16 |

For each cell:

$$
\widehat U_{a,s}
=-\frac{\langle\nabla_{\theta_S}M_{a,s},g_D^S\rangle}
{\|\nabla_{\theta_S}M_{a,s}\|\|g_D^S\|}.
$$

## 3. Numerical Validation

- cast to float32 during diagnostics;
- use relative shared-parameter norm `1e-6` central perturbations along $g_D^S$;
- evaluate all four margins under the same minus/plus perturbations;
- require predicted/measured sign agreement for all four cells in at least `4/5` step-0 seeds;
- restore exact selected-parameter hashes;
- reproduce A11_16 NTP condition-mean $Q$ at shared checkpoints within `0.05`.

## 4. Decision Rules

Use step-0 sign count and normalized-usefulness AUC over `0-200`.

**Direct self-usefulness passes:** H2-train positive in at least `4/5` for both step 0 and AUC.

**Interface/position bottleneck:** direct self-usefulness passes, but H1-train is positive in at most `1/5` at step 0 or by AUC.

**Paraphrase bottleneck for interface $a$:** the train cell passes, but the corresponding evaluation cell is positive in at most `1/5`.

**Mixed transport:** valid but pass/fail counts fall between these thresholds.

**No local bottleneck:** all four cells are positive in at least `4/5`; next audit optimizer/background terms.

**CE/margin mismatch:** H2-train is positive in at most `1/5`; inspect full-vocabulary versus A/B margin geometry before any downstream claim.

**Insufficient:** numerical, restore, balance, coverage, finite-value, or curve guards fail.

## 5. Required Outputs

- four-cell usefulness table at every checkpoint;
- per-seed step-0 and `0-200` AUC table;
- central finite-difference sign table;
- one central 2-by-2/trajectory figure;
- canonical summary, detailed, anchor, and story updates.

## 6. Claim Boundary

The protocol identifies where a local task-directed gradient sign is lost. It does not establish global optimization efficiency, pure MTP pretraining benefit, matched compute, or external benchmark behavior.
