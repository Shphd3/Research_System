# Protocol Card: A07_common_update_interference_diagnostic

Draft status: pending user / experiment-AI approval. Do not run before approval.

## 0. Approval Snapshot

**Approval status:** Draft / not approved.

**Purpose:** Test whether common-example updates causally hurt rare/conflict
loss on a controlled nested-conflict surface, then run a small real-data
observational bridge if the causal perturbation passes.

**Primary anchor:** `A07_common_update_interference_anchor.md`

**Anchor decision question:** Do common-example updates causally hurt rare loss
beyond norm-matched controls?

**Anchor physical prior tested:** common examples create a stable update
subspace that can interfere with rare examples.

**Anchor core model term tested:** $\Delta L_{R|C}$, guarded by
$\alpha_R^C$.

**Anchor falsifier:** common updates do not hurt rare loss more than matched
controls.

**Experiment role:** root-cause audit / mechanism diagnostic.

**Primary metric from anchor:** `common_to_rare_loss_effect`.

**Claim boundary from anchor:** Passing supports common-update interference only
on the tested controlled surface. A compatible real-data bridge only supports
transfer plausibility for the next anchor.

**Minimal setup:** one controlled nested-conflict dataset and one small model
with reconstructable update directions.

**Basic configuration:** one-step perturbation from the same checkpoint,
norm-matched controls, fixed rare/common validation, and no MoE method
construction.

**Conditions to run:** common update, unrelated update, norm-matched random
update, optional rare update sanity check, and a gated real-data observational
bridge only after controlled pass.

**Pass:** common update increases rare loss more than matched controls during a
rare-underlearning window. The real-data bridge is compatible if the same
projection/group signal is visible above nuisance controls.

**Fail:** common update has no extra rare-loss harm, or controls explain the
effect.

**Insufficient:** no stable rare validation, no update reconstruction, no
common warmup, or no stable real-data proxy/common/rare groups for the bridge.

**Cannot claim:** real-DCLM utility, semantic experts, MoE partition value, or
scaling.

**Approval decision:** approve data surface, update block, projector rank,
perturbation step size, and whether to include the gated real-data bridge.

## 1. Anchor Alignment

**Decision question:** same as approval snapshot.

**Physical prior tested:** common updates can become a harmful direction for
rare loss.

**Core model term tested:** $\Delta L_{R|C}$.

**Falsifier:** common update is not worse than matched controls.

**Claim boundary:** controlled mechanism only; real-data bridge is observational
and cannot prove utility.

## 2. Tested Hypothesis

Common-update interference is active when common updates causally increase rare
loss and rare updates also project into the common-update subspace.

## 3. Rival Explanations

1. Rare data are too scarce.
2. Rare validation is noisy.
3. Capacity, not update interference, explains rare failure.
4. The common projector is unstable.
5. Update norm, not direction, explains the perturbation effect.

## 4. Data / Model / Algorithm / Objective

**Data:** controlled nested-conflict sequence task with common parent patterns
and rare exception patterns. Optional gated input: real-DCLM proxy/common/rare
groups if they already exist from A06-style artifacts.

**Model:** small transformer or matched small model with saved update
directions or optimizer state.

**Algorithm:** estimate common projector after common warmup; compute rare
projection; apply one-step perturbations; measure rare/common loss change. If
the causal test passes, compute an observational bridge on the real-DCLM groups
without promoting it to a perturbation or utility claim.

**Objective:** standard next-token loss; no method construction yet.

## 5. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
|---|---|---|---|---|---|---|---|---|
| Common update | common updates may hurt rare loss | $\Delta L_{R|C}$ | primary causal test | primary evidence | rare loss increases vs baseline | no rare harm | noisy rare validation | perturbation table |
| Unrelated update | harm should be direction-specific | unrelated-direction rival | separates common direction from any update | guard | less rare harm than common | matches common harm | control unavailable | perturbation table |
| Norm-matched random update | norm may explain harm | update-norm rival | separates direction from magnitude | guard | less rare harm than common | matches common harm | norm matching fails | perturbation table |
| Rare update sanity | rare direction should be meaningful | bad rare surface rival | checks rare validation and update sign | diagnostic | rare loss does not worsen | rare update worsens rare loss | no stable rare batch | sanity table |
| Gated real-data observational bridge | mechanism should be worth porting | transfer / nuisance rival | prevents controlled-only promotion | secondary bridge | signal above shuffled/frequency/position controls | absent or nuisance-driven signal | no stable real groups | bridge table |

Use a smoke seed first; scale only if update reconstruction and rare validation
are stable.

## 6. Primary Metric

`common_to_rare_loss_effect` is:

$$
\Delta L_{R|C}=L_R(\theta-\eta \bar u_C)-L_R(\theta).
$$

It decides the anchor because overlap alone does not prove harm.

## 7. Secondary Metrics

`rare_common_update_fraction`, projector drift, rare loss, common loss, update
norm, perturbation variance, and real-data bridge projection / nuisance
metrics.

## 8. Known Good / Known Bad / Known Confusing Cases

**Known good:** rare update sanity should not hurt rare loss.

**Known bad:** random update should not systematically mimic common-update harm.

**Known confusing:** high $\alpha_R^C$ with no rare-loss harm; controlled harm
with no real-data observational signal.

## 9. Stage-Level Profiling Plan

| Stage | Local question | Debug artifact |
|---|---|---|
| Data audit | is rare underlearned after common warmup? | rare/common loss curves |
| Projector audit | is $P_C$ stable enough to use? | projector drift table |
| Perturbation audit | does common update hurt rare loss? | perturbation table |
| Real-data bridge | is the controlled mechanism visible on real groups? | bridge table |

## 10. Algorithm Specification, If Nontrivial

**input:** common/rare batches, checkpoint, optimizer/update state, and
optional real-DCLM proxy/common/rare group metadata.

**parameters:** update block, projector rank, perturbation step size.

**steps:** estimate $P_C$; compute $\alpha_R^C$; construct perturbation
directions; apply one-step perturbations; measure loss deltas; if controlled
pass holds, compute real-data bridge metrics against nuisance controls.

**outputs:** causal perturbation table, rare-loss effect plot, and optional
real-data bridge table.

**failure reasons:** unstable projector, no rare conflict, update reconstruction
failure, norm confound, or noisy rare validation.

## 11. Success / Failure / Insufficient Evidence

**Success:** common update hurts rare loss more than matched controls. The
real-data bridge is compatible if its signal is above nuisance controls.

**Failure:** common update is harmless or control-matched.

**Insufficient:** measurement surface cannot distinguish the directions, or no
stable real groups exist for the bridge.

## 12. What This Cannot Claim

This protocol cannot claim MoE partition utility. It only tests whether
common-update interference is a valid mechanism candidate. The real-data bridge
can only justify or weaken the next transfer decision.

## 13. Review Notes And Protocol Changes

If the controlled perturbation passes and the real-data bridge is compatible,
write a separate partition-value anchor. If perturbation fails, park
common-update interference and revisit data scarcity, capacity, or
route-function mismatch. If perturbation passes but bridge fails, revise the
real-data group definition before utility claims.
