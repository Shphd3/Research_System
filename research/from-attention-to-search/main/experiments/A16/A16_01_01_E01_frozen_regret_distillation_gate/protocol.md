---
experiment_id: A16_01_01_E01_frozen_regret_distillation_gate
anchor_id: 16_01_01_regret_distilled_conditional_innovation
status: approved_for_implementation_smoke_and_full
approved_by: user
approval_date: 2026-08-12
design_frozen_at: 2026-08-12
resource_profile: 5090-8-spot
primary_metric: document_paired_heldout_expert_choice_regret
---

# Protocol: A16_01_01_E01 Frozen Regret-Distillation Gate

## 0. Approval Snapshot

**Purpose.** Decide whether the actual same-layer increment contains conditional expert utility once the part predictable from the old state is removed.

**Primary Anchor.** A16_01_01 Regret-Distilled Conditional-Innovation Routing.

**Experiment role.** Functional admission gate before long method training.

**Treatments and controls.** On the same frozen Native-LB 10B checkpoint: Native; Raw-Utility; Conditional-Utility; Conditional-Haar-Utility. The only changed objects are residualization and the rank-56 feature frame; backbone, experts, Native Gate, functional documents, teacher losses, fit budget, and evaluation are held fixed.

**Primary metric.** Target-token-local expert-choice regret in nat/token, averaged within each document over eight positions and four layers, then compared by paired document bootstrap.

**Pass.** In seed 17 and seed 29 separately, Conditional-Utility minus Native, Raw-Utility, and Conditional-Haar each has a 95% upper bound below zero. **Fail.** Complete eligible evidence misses any required comparison. **Insufficient.** Checkpoint, data split, forced-expert locality, cross-fit, numerical, or artifact/recovery identity fails.

**Execution scope approved.** Protocol, implementation, unit tests, single-GPU smoke, one 8×5090 all-arm smoke, and two full frozen-gate jobs are approved. A16_01_01_E02 is conditionally approved and may be submitted without another review only if this Protocol returns Pass.

**Cannot claim.** A Pass does not establish 30B NLL improvement, long-term expert specialization, semantic novelty, or validity beyond the frozen local expert-loss teacher.

## 1. Terminology / Definitions

- **Old state \(x\):** normalized token state immediately before the current Attention write.
- **Increment \(u\):** actual post-Attention Router input minus \(x\).
- **Conditional innovation \(r=u-Ax\):** standardized increment not linearly predictable from standardized \(x\) by a FIT-only residualizer.
- **Target-token-local forced expert:** directly change only the registered token's sparse expert at the registered layer; all other positions and layers continue under the Native Router policy, so downstream routes may respond to the altered hidden state rather than being frozen to baseline route IDs. Candidate experts share the Native winner's top-1 mixture weight, isolating expert function at a matched mixture scale.
- **Expert-choice regret:** the forced-expert loss of the Router's chosen expert minus the minimum forced-expert loss for that token and layer.
- **Utility teacher:** \(q_e\propto\exp[-(\ell_e-\min_j\ell_j)/0.1]\), where \(\ell_e\) is next-token NLL under the local intervention.

## 2. Anchor Alignment

The parent branch failed to establish replicated 20B NLL improvement and every previous expert-utility admission. This experiment changes the supervision target, not the parent representation object: the Native Router remains and the same actual increment is exposed through a no-op-compatible branch. The strongest rival is that conditional residuals contain no generalizable expert utility or that any matched rank-56 side path is equivalent.

## 3. Tested Hypothesis

Direct utility supervision over \(r\) lowers held-out regret beyond Native, utility-supervised raw \(u\), and a utility-supervised Haar residual frame in both seeds.

## 4. Rival Explanations

| Rival | Separator |
| --- | --- |
| Native already uses all accessible utility | Conditional versus Native |
| Utility supervision helps but residualization does not | Conditional versus Raw-Utility |
| Any rank-56 residual view works | Conditional versus Conditional-Haar |
| A global best-expert bias explains the fit | Report intercept-only and document-shuffled teachers as guards |
| Teacher or local intervention is invalid | Forced-route replay and target-locality tests |

## 5. Data Construction And Provenance

Use the frozen A16 E2 bank containing 384 independent 256-token DCLM documents, with 128 whole documents each in FIT, DEVELOPMENT, and CONFIRMATION. Each document contributes eight arithmetic-grid target positions. The bank tensor and manifest must match the registered SHA-256 values `827129cdf5b1d44af06a034b607e40c98d5353ac8e5276b994b906c917479fd5` and `0a8a00d2370735821bb553fcc5f27a8c7c0006a749e4d5b4628c8df2ee6f0192`.

Seed 17 uses only Native checkpoint `checkpoint-12716` with model SHA-256 `3d7c945006bfcc93f3c071089e086c9a0d9e13766c23d17af50e09fac2f7946e`; seed 29 uses its own checkpoint with SHA-256 `c89ce4d8d78109fe27c44d89c80e96fa6334ae4ed4ea0cbf68aad39f4573998c`. Cross-seed checkpoint use is forbidden.

FIT supplies residualizer and branch fitting. DEVELOPMENT selects only the registered ridge candidate. CONFIRMATION is opened once after artifact hashes and model choices freeze. No confirmation document may affect a standardizer, residualizer, rank, frame, ridge, checkpoint, or threshold.

## 6. Learning Task And Permitted Supervision

For each target token and layer, predict the relative utility distribution over eight experts from the Native logits plus one low-rank feature. The allowed label is the local forced-expert loss vector. Taxonomy labels, endpoint NLL, confirmation outcomes, and future-layer states are forbidden.

## 7. Model / Architecture And Frozen Variants

Standardize \(x\) and \(u\) with FIT statistics. For Conditional arms, FIT-only five-fold document cross-fitting estimates \(A\) in \(u\approx xA\); deployment stores \(C=AP\) and computes

\[
f=uP-xC.
\]

The total logits are \(z=z^{native}+Bf\). Raw-Utility uses \(f=uP\). Conditional-Utility learns \(P\) from a reduced-rank fit to teacher-logit correction. Conditional-Haar uses a seed-fixed Haar \(P\) and fits only \(B\). All use rank 56 and the same tensor shapes. No model or expert parameter receives a gradient.

## 8. Training Objective And Optimization

The teacher temperature is frozen at \(\tau=0.1\) nat. The fit minimizes \(KL(q\|\operatorname{softmax}(z))\) through a deterministic ridge-reduced-rank solution. Residualizer and utility ridge candidates are `$10^{-4},10^{-3},10^{-2},10^{-1},1,10` after FIT standardization; DEVELOPMENT regret selects the smallest ridge among exact ties. Rank is fixed at 56 and cannot be selected.

The final residualizer refits on all FIT documents after the ridge freezes. The learned frame is computed from cross-fitted FIT residuals; the final \(C\) uses the all-FIT residualizer. Orthonormal padding directions have zero output weight and therefore cannot affect logits.

## 9. Conditions, Seeds, And Checkpoints

| Condition | Feature | Supervision | Decision role |
| --- | --- | --- | --- |
| Native | none beyond frozen Native logits | none | no-branch baseline |
| Raw-Utility | standardized \(u\) through learned rank-56 frame | same utility teacher | residualization control |
| Conditional-Utility | standardized \(u-Ax\) through learned rank-56 frame | same utility teacher | primary treatment |
| Conditional-Haar | standardized \(u-Ax\) through fixed Haar rank-56 frame | same utility teacher | dimension/capacity control |

Run all conditions inside each of seeds 17 and 29 from that seed's frozen Native 10B state.

## 10. Primary Metric And Frozen Analysis Plan

For each token-layer example,

\[
R=\ell_{\arg\max_e z_e}-\min_e\ell_e.
\]

First average regret over four layers and eight positions within each document. Within each seed, compute Conditional minus comparator for 128 confirmation documents. Use 2,000 paired document bootstrap draws and a two-sided percentile 95% interval; the registered Pass uses the upper bound \(<0\). Report seeds separately and an equal-seed descriptive mean. No token, layer, or position is treated as an independent replicate. Missing examples are not imputed; any missing registered document makes that seed Insufficient.

## 11. Secondary Metrics And Guards

Report native and treatment regret by layer; top-1 agreement with oracle; KL to \(q\); residual prediction \(R^2\); feature and logit RMS; route flips versus Native; expert shares; and intercept-only/shuffled-teacher regret. They explain failure modes but cannot rescue the primary result.

## 12. Known Good / Known Bad / Known Confusing Cases

- Known good: a synthetic teacher generated from one conditional residual direction must be recovered and beat Native/Haar.
- Known bad: shuffled loss vectors must not pass.
- Known confusing: lower KL without lower regret is not functional admission; one layer passing while aggregate regret fails is not Pass.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal | Input | Operation | Scale-up rule | Artifact |
| --- | --- | --- | --- | --- | --- |
| P0 | verify provenance | checkpoints and bank | hash, schema, split, route-locality audit | every guard passes | `preflight.json` |
| P1 | validate algorithms | synthetic tensors | red/green unit tests | full suite passes | test receipt |
| P2 | validate real path | small frozen subset | extract, distill, install, save/reload | exact no-op/tamper/gradient guards pass | single-GPU receipt |
| P3 | validate distributed execution | seed17, all arms | 8×5090 smoke with artifact broadcast | ranks agree; results rebuild | distributed receipt |
| P4 | scientific gate | full banks, two seeds | fit on FIT/DEV; unseal CONFIRMATION | typed E01 verdict | regret arrays and decision JSON |

## 14. Algorithm, Output, And Provenance Contract

The immutable utility artifact stores checkpoint and bank hashes, seed, FIT standardizers, residualizer ridge, \(P\), \(C\), initial \(B\), fixed teacher \(B_T\), Native Gate snapshot, condition label, layer index, and a whole-artifact SHA-256. Only this artifact may initialize E02. Outputs live under a new worker root; no A16_01_E01 result, checkpoint, or log may be overwritten.

## 15. Success / Failure / Insufficient Evidence

- **Pass:** all three registered aggregate regret contrasts pass in both seeds.
- **Fail:** eligible complete comparisons do not satisfy Pass, including no common direction of benefit.
- **Insufficient:** provenance, split, intervention, numerical, distributed, or artifact identity fails.

## 16. What This Cannot Claim

This experiment cannot establish online training benefit, global expert specialization, utility outside the fixed target-token intervention, universality across scales, or that residualization is semantic novelty.

## 17. Block Confirmation, Freeze, And Amendment Ledger

Blocks A-G are `CONFIRMED` by the user's 2026-08-12 instruction to implement this approved proposal, smoke it, and conditionally launch 30B. Cross-block consistency is `PASS`. The scientific body freezes before P1. Any post-start change to data, temperature, residualizer, rank, conditions, primary aggregation, or verdict rule requires an append-only amendment and eligibility audit. Git, graph, sync, commit, and push remain unauthorized.

### Amendment 2026-08-12-A: same-forward deployed-logit measurement

The first real execution stopped at the Native replay guard before CONFIRMATION was opened: each seed had 7/8192 near-boundary examples whose winner changed when BF16 state differences were reconstructed under a different batch shape. Audit confirmed that the Router object remained \(x+u\); this was not a scientific-object mismatch. The execution contract therefore changes only the measurement path: \(x,u\), deployed Native logits, and the winner must be captured jointly in the same batch-size-1 Native forward, and the stored winner must be an exact co-maximum of the stored logits. Reconstructing logits from \(x+u\) and the Gate weight becomes a numerical diagnostic rather than the authoritative deployed-logit replay. Data, conditions, supervision, rank, primary metric, thresholds, and verdict are unchanged. The old attempt remains preserved as Insufficient engineering evidence; the new schema and worker hash require full re-extraction under a new evidence root.
