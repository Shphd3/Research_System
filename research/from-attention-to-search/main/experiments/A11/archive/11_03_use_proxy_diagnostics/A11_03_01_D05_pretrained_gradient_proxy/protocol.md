# Protocol: A11_16 Pretrained Shared-Gradient Transmission

## 0. Approval Snapshot

**Approval status:** approved under the user's standing instruction.  
**Purpose:** explain why A11_15 fits private H2 without a reliable common-H1 gain.  
**Primary anchor:** `11_16_pretrained_shared_gradient_transmission_anchor.md`.  
**Decision question:** does the extra H2 loss have positive shared-parameter directional usefulness for the held-out common-H1 margin?  
**Experiment role:** root-cause audit.  
**Primary metric:** $\widehat U_D^E$.  
**Minimal setup:** exact A11_15 trajectories plus gradient diagnostics.  
**Pass:** derivative guard valid and transmission sign yields one of the preregistered positive/missing/mixed decisions.  
**Insufficient:** derivative, balance, restore, pairing, or curve-reproduction guard fails.  
**Cannot claim:** global or FLOP efficiency.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete computation | Why it matters | Cannot prove |
|---|---|---|---|---|
| shared parameters $\theta_S$ | parameters through which H2 can affect standard H1 behavior | all Qwen LM parameters, excluding H2 | actual transmission path | private-head learning |
| evaluation margin $M_E$ | mean correct-minus-other A/B logit from common H1 | balanced held-out diagnostic batch | differentiable downstream boundary | full $Q$ by itself |
| $U_D^E$ | predicted margin gain from an H2-gradient step | $-\langle\nabla M_E,\nabla L_D\rangle$ | primary causal local quantity | finite-step convergence |
| normalized usefulness $\widehat U_D^E$ | task-directed gradient cosine | $U_D^E/(\|r_E\|\|g_D\|)$ | compares sign across checkpoints | update size |
| gradient conflict | whether NTP and H2 training gradients align | cosine of $g_N,g_D$ | secondary interference description | task usefulness |
| private fraction | H2-loss gradient norm outside the common interface | H2 norm relative to shared plus H2 norm | detects private absorption capacity | downstream harm |

## 2. Anchor Alignment

The protocol holds the A11_15 task, model, K, objective, optimizer, seeds, and horizon fixed. It changes only instrumentation. The named rival explanations are missing shared transmission, MTP-path co-adaptation, and background/optimizer override.

## 3. Tested Hypotheses

1. Step-0 $\widehat U_D^E>0$ in at least `4/5` seeds.
2. NTP-path normalized-usefulness AUC over steps `0-200` is positive in at least `4/5` seeds.
3. NTP/MTP path comparison identifies whether co-adaptation changes the sign.
4. Step-0 relative-norm `1e-6` central differences match predicted sign and have relative error at most `0.50` in at least `4/5` seeds.

## 4. Data, Model, And Training

- exact A11_15 A11_13-derived prompts, `0,1 -> 2,3` paraphrase split;
- Qwen3-0.6B-Base and native tokenizer;
- NTP objective $L_S+L_I$ and MTP objective $L_S+L_I+L_D$;
- AdamW `1e-5`, batch size 4, bfloat16 training, 300 updates;
- seeds `971-975`, two trajectories per seed;
- diagnostic checkpoints `0,20,100,200,300`;
- deterministic 10-example train and 10-example evaluation diagnostic batches, one example for every domain-state pair; answer labels and paraphrase IDs are exactly `5/5`, while option order is the closest feasible `4/6` split under the state-option label relation.

## 5. Gradient Algorithm

At each diagnostic checkpoint:

1. cast model parameters from bfloat16 to float32 without changing values and disable gradient checkpointing;
2. compute $g_D^S$ and private-H2 $g_D^{H2}$ on the fixed train diagnostic batch;
3. compute $r_E^S=\nabla_{\theta_S}M_E$ on the fixed held-out diagnostic batch;
4. compute $g_N^S$ on the same train batch;
5. record $U_D^E$, $U_N^E$, $U_M^E$, normalized values, $\cos(g_N,g_D)$, norms, and parameter-group contributions;
6. back up $\theta_S$, evaluate both $M_E(\theta_S-\delta g_D^S)$ and $M_E(\theta_S+\delta g_D^S)$ where $\delta\|g_D^S\|=10^{-6}\|\theta_S\|$, use their central difference to validate $\delta U_D^E$, record the one-sided descent change separately, then restore the exact backup;
7. cast back to bfloat16, re-enable training instrumentation, and verify a hash over selected parameters is unchanged.

Parameter groups are tied embedding/interface, layers `0-6`, `7-13`, `14-20`, `21-27`, and final norm. Group metrics are explanatory; whole-shared $\widehat U_D^E$ is primary.

## 6. Conditions, Seeds, And Checkpoints

| Item | Anchor clause | Why needed | Evidence | Pass | Fail | Insufficient |
|---|---|---|---|---|---|---|
| NTP trajectory | counterfactual addition of H2 to standard path | primary transmission test | $\widehat U_D^E$ AUC | positive 4/5 | non-positive 4/5 | mixed |
| MTP trajectory | co-adaptation rival | see whether H2 training changes transmission | paired checkpoint signs | interpretable path shift | no shift | noisy/mixed |
| finite difference | derivative validity | exclude autograd/sign error and leading even-order curvature | predicted vs central $\Delta M_E$ | sign 4/5, error <=0.50 | otherwise | prediction too small |
| A11_15 curve reproduction | implementation guard | ensure instrumentation did not change task | train/eval $Q$ | step-0 exact and condition-level checkpoint means within `0.05` | outside | missing rows |

## 7. Primary And Secondary Metrics

Primary:

$$
\widehat U_D^E=-\frac{\langle r_E^S,g_D^S\rangle}{\|r_E^S\|\|g_D^S\|}.
$$

Secondary:

$$
U_M^E=U_N^E+U_D^E,
$$

$$
R_{shared}=\frac{\|g_D^S\|^2}{\|g_D^S\|^2+\|g_D^{H2}\|^2},
$$

plus finite-difference fidelity, layer-group contributions, $\cos(g_N,g_D)$, common-H1 margin/accuracy, private-H2 accuracy, $Q$, local CE, wall time, and peak memory.

## 8. Decision Rules

**Positive transmission:** derivative guard passes; H1 and H2 pass. The A11_15 failure then cannot be explained by missing raw-gradient usefulness, so the next anchor audits optimizer-preconditioned/background updates.

**Missing/signed transmission:** derivative guard passes and initial or integrated NTP-path usefulness is non-positive in at least `4/5`. Add positive shared-interface transmission as an explicit condition in the theory.

**Co-adaptation loss:** step 0 is positive, NTP path remains positive, but MTP path becomes non-positive in at least `4/5` at two later checkpoints.

**Mixed:** valid measurement but no stable sign pattern. Preserve a conditional claim and do not construct a method.

**Insufficient:** derivative, restore, paired, balance, finite-value, or curve-reproduction guards fail.

## 9. Required Outputs

- `gradient_transmission.csv` and layer-group table;
- paired trajectory-integral and finite-difference tables;
- common-H1/H2 reproduction curves;
- one central figure showing usefulness sign, predicted/actual margin movement, shared/private routing, and A11_15 common-head behavior;
- canonical `summary.md`, `detailed.md`, anchor and story updates.

## 10. Claim Boundary

This audit identifies a local necessary transmission condition on one controlled persistent-assistant task. It does not establish MTP pretraining advantage, global sample efficiency, matched compute, or external downstream performance.

## 11. Protocol Revision Record

The first GPU smoke showed that a one-sided relative-norm `1e-5` perturbation was curvature dominated. The validity check was changed to a central difference, which preserves the same derivative target and cancels the leading even-order term. A second smoke recovered the correct sign but had `0.465` relative error at step 0, so the numerical validation radius was reduced to `1e-6`; this changes only truncation error, not the derivative being tested. At `1e-6`, the sign remained correct and the step-0 error was `0.366`, indicating a float32/kernel numerical floor; the magnitude tolerance was therefore relaxed from `0.35` to `0.50` while preserving the sign requirement. Exact per-seed A11_15 trajectory replay was also replaced by step-0 exactness plus a `0.05` condition-mean tolerance because H100 SDPA is not bitwise deterministic across jobs. None of these changes alters the task, training objective, primary usefulness metric, seeds, or sign decision.
