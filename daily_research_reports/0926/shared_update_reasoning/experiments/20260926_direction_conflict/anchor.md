# Directional conflict under shared local updates

## 1. Problem Definition

Can changing the relation of a small shared-parameter update to a target task's gradient cause target harm beyond an equally sized change with the same first-order source learning benefit? This is one controlled sufficiency test within the researcher's shared-learning mechanism question. Prior natural-domain updates helped every cross-domain mean; destructive natural-domain interference is not established. The present intervention deliberately constructs a counterfactual update, rather than claiming a new ordinary-data gradient. Its decision is whether this directional mechanism survives independent-record readout in the real nonlinear model. Positive evidence retains a sufficient local mechanism; non-support stops its transfer interpretation; an unconstructible comparison or uncertain harm leaves the question unresolved.

The researcher explicitly requested theory and initial experiments without further review on 2026-09-26. Operational definitions below are AI choices within that delegated exploration, not individually confirmed human mechanism judgments. No new Focus or project-state transition is made. This design owns this new bounded comparison and does not revise the completed atom-enrichment experiment.

## 2. Physical Priors

Candidate prior: shared computation couples examples, but the signed relationship between an update and target loss sensitivity determines its local effect. Equal update magnitude or equal first-order source progress need not determine the target effect. The live rival is that apparent directional effects are merely generic step-size or source-learning-strength effects, or fail to transfer from construction records to other records.

## 3. Falsifiable Hypotheses

H1: a source-descent update reflected along the target construction gradient harms target readout more than equally sized, equally source-descent matched reflections; removing that constructed adverse component mitigates harm more than uniform shrinkage of the same resulting norm. H0: the target-specific contrast does not survive readout, or any rescue is explained by generic shrinkage. No natural-data semantic or SAE identification hypothesis is tested.

## 4. Mathematical Model

Use Frobenius inner products on one attention output matrix. Let unit construction gradients be u for source A and v for target B, c=<u,v>, and gamma the fixed update size. Full update is -gamma*u. With 0<c<1/sqrt(2), target reflection is dT=gamma*(-u+2*c*v): its norm remains gamma and its source derivative is -gamma*||gA||*(1-2*c^2)<0, but its target construction derivative is +gamma*||gB||*c. Choose a unit random r orthogonal to u and v, q=c*u+sqrt(1-c^2)*r, and dC=gamma*(-u+2*c*q). dC has the same norm, distance from full update, and source derivative as dT, while its target construction derivative is -gamma*||gB||*c*(1-2*c^2). These are algebraic facts on construction gradients; readout effects require measurement.

Primary M is mean target loss change under dT minus mean change under three dC controls, equally averaged across twelve ordered A!=B pairs. Units are nats/prediction. A positive M separates these matched directional interventions, not the natural occurrence of conflict.

## 5. Computational Realization

Reuse fixed fresh-S7 after21 billion training tokens, four natural-text domains, and verified last-attention FP32 tail caches/gradients from the completed atom experiment. Source and target construction gradients use only the first128 records per domain. Separate128-record readout batches assess all branches; these records were previously inspected, so this is exploratory and not fresh confirmation. W is1024x2048 and a=Wc. Directly replay the unchanged nonlinear residual/MLP/head after each virtual delta. No optimizer trajectory, new checkpoint or SAE intervention is introduced. An analytic squared-loss example independently checks overlap, error-direction and finite-step terms.

## 6. Minimal Falsification Tests

At full and half step, require construction/identity guards, independent source learning for every branch, positive conditional95% lower bounds for M and mean dT target harm. Rescue removes the v component from dT; its comparator uniformly shrinks dT to the rescue norm. Positive rescue-minus-shrink relief lower bounds are also required. All twelve ordered pairs remain included. Qualified non-support is M upper bound<=0 at both steps; failure of transfer/harm/rescue or mixed evidence is INSUFFICIENT, not a repaired positive result. Full rules and numerical guards belong to Protocol. No criterion can be rescued by the analytic example.

## 7. Current Evidence

The prior [atom result](../../../docs/atom_mechanism/summary_cn.md) reports a small aggregate functional selectivity and average help in all twelve cross-domain full updates. That motivates testing controlled sufficiency without claiming spontaneous negative transfer. The new reflection comparison is NOT RUN at registration. Derivations are given in the [theory appendix](../../03_theory_derivation_cn.md), with assumptions separated from empirical propositions.

## 8. Claim Boundary And Next Decision

Maximum claim: constructed, local, directional harm can or cannot be demonstrated on this fixed model and exposed panel beyond the stated matching controls. It cannot establish that ordinary source-data training generates these reflected updates, which intrinsic data attribute causes conflict, that every hidden representation norm is matched, or that SAE/isolation training is useful. The one next decision after eligible results is whether to investigate a pre-specified natural-data condition that generates the same mechanism without using the target gradient to construct an adverse update. Human final interpretation remains Unknown pending review; result records own actual execution.
