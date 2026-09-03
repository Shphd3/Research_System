---
anchor_id: 15_05_03_progressive_band_source_routing
status: completed_specialization_only_without_quality_pass
canonical_language: en
parent_anchor: 15_05_functional_coordinate_admission
updated: 2026-08-02
---

# A15_05_03 Progressive Band Source Routing

## 1. Problem Definition

**Decision question:** after branching the same four-layer DCLM MoE at 0.629B tokens, can routing blocks 2, 3, and 4 through head, middle, and tail respectively form more functional experts and improve matched-compute 2B held-out NLL; and does the result depend on using each layer's local spectrum versus relaying every band from block 1?

Layer differentiation is not defined by route change or balanced load. It requires independent evidence from held-out counterfactual expert utility, route--utility binding, expert update conflict, or functional redundancy.

## 2. Physical Priors

1. Covariance anisotropy causally changes finite-time linear-Gate learning speed but does not specify the useful expert partition.
2. The same covariance rank can encode different variables at different depths, so local bands may provide depth-conditioned coordinates.
3. A fixed block-1 coordinate may reduce cross-layer drift, or may lock deep routing to information available too early.
4. A full native Router may dominate any hard band bottleneck.

## 3. Falsifiable Hypotheses

**H1:** local-HMT lowers 2B NLL and improves an independent expert-function measure relative to native. **H2:** layer1-relay-HMT beats local-HMT if coordinate stability matters, and loses if deep routing requires newly computed state.

The strongest rival is distribution-only: both treatments alter routes but do not improve expert utility or language modeling; apparent differences arise from load, compute, or continuation noise.

Pass requires a treatment to improve native 2B NLL in both paired continuations and show concordant functional evidence. Valid route change without such benefit is distribution-only. Broken pairing, load, compute, basis, resume, or replication guards is Insufficient.

## 4. Mathematical Model

Block 1 remains native. Let $r_\ell$ be the actual local Router input and let $s_1$ be the parameter-free RMS-normalized full output of block 1. With $B_2=H_{64}$, $B_3=M_{256}$, and $B_4=T_{448}$,

$$
z_\ell^{local}=W_\ell[\mu_{\ell,B_\ell}+P_{\ell,B_\ell}(r_\ell-\mu_{\ell,B_\ell})],
$$

$$
z_\ell^{relay}=W_\ell[\mu_{1,B_\ell}+P_{1,B_\ell}(s_1-\mu_{1,B_\ell})].
$$

Experts always receive the full local representation. The primary effect is $\Delta L_{a:native}=L_a^{2B}-L_{native}^{2B}$ in nat/token.

## 5. Computational Realization

Reuse the A15_05_05 H768, four-layer, eight-sparse-plus-one-shared-expert top-1 DCLM runner, running center, and $\lambda_{LB}=0.01$. Native-full, local-HMT, and layer1-relay-HMT branch from the same step-800 checkpoint and stop at step 2,544. Post-branch seeds 17 and 29 give two paired stochastic continuations. Each replica shares model, optimizer, scheduler, cursor, projectors, and data order across arms.

## 6. Minimal Falsification Tests

Require native no-op and source replay; projector rank, idempotence, reconstruction, and split stability; exact branch and resume pairing; matched tokens, parameters, capacity, FLOPs, and load; route manipulation; forced-expert utility, route regret, output redundancy, update norm, and within-expert gradient conflict; and final frozen/current band overlap.

## 7. Current Evidence

A15_02_01 established layer-specific F1-intermediate and F2-coarse identities in a capability-valid controlled model, while the composite result did not occupy a fixed band. A15_05_05 established that single fixed H/M/T/N views change dispatch but all lose to native 2B NLL. Neither experiment compares local progressive bands with a shared shallow source.

E01 completed both paired continuations for all three 2B arms with valid checkpoint, batch-identity, load, compute, and replication guards. Local-HMT had a pooled endpoint effect of +0.002174 $[0.001758,0.002590]$ nat/token versus native. Layer1-relay-HMT had a pooled endpoint effect of −0.001756 $[-0.002352,-0.001119]$, favorable in both continuations.

Relay nevertheless paid a large immediate switching cost and had worse NLL AUC in both continuations, with a mean +0.02135 nat/token disadvantage versus native. Local and relay changed mean block-2--4 routes by 7.12% and 19.70%. Relay reduced forced-expert route regret in both continuations, but utility dispersion fell, output redundancy rose, and other functional metrics were mixed. The typed result is `specialization_only_without_quality_pass`: explicit structure changed routes and partial function without establishing coherent beneficial specialization.

## 8. Claim Boundary And Next Decision

The result is restricted to two post-0.629B continuations of one four-layer DCLM branch. It cannot establish from-initialization formation, optimal HMT order, natural semantic hierarchy, or superiority to an arbitrary equal-dimensional schedule because no random-schedule training arm is included. The late relay endpoint advantage is not evidence of improved training efficiency.

**Next decision:** close fixed progressive HMT rank scheduling as a functional routing principle. Require any later cross-layer Router to pass held-out expert-utility or update-compatibility gates over equal-rank random and wrong-layer controls before matched training.
