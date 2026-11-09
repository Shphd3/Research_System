# A11_16 Pretrained Shared-Gradient Transmission: Summary

## What We Established

The extra K=2 H2 loss does not provide a stable positive shared-parameter direction for the held-out common-H1 semantic boundary. At the identical pretrained initialization, its normalized task usefulness is positive in only `1/5` seeds. Along the NTP trajectory from steps `0-200`, its usefulness integral is also positive in only `1/5`.

**Decision:** A11_15's strong private-H2 fitting without a reliable common-H1 gain can be explained by missing or signed cross-interface transmission. The theory must add positive downstream-interface transmission as a condition; horizon coverage alone is not enough for downstream efficiency.

## Terminology / Definitions

For a held-out example, define the standard H1 correct-versus-other answer margin:

$$
m_i(\theta)=\ell_{1,Y_i}(X_i;\theta)-\ell_{1,\bar Y_i}(X_i;\theta),
\qquad
M_E=\frac{1}{|E|}\sum_i m_i.
$$

Let $\theta_S$ contain all Qwen parameters shared by the H2 loss and the standard H1 path, excluding the private H2 head. With

$$
r_E^S=\nabla_{\theta_S}M_E,
\qquad
g_D^S=\nabla_{\theta_S}L_D,
$$

the primary metric is:

$$
\widehat U_D^E
=-\frac{\langle r_E^S,g_D^S\rangle}
{\|r_E^S\|\|g_D^S\|}.
$$

A positive value means an infinitesimal gradient-descent step on the extra H2 loss increases the held-out common-H1 margin. A negative value means it moves against that boundary. It is a local transmission diagnostic, not a global convergence or sample-efficiency result.

## Setup And Validity

- exact A11_15 Qwen3-0.6B task, objectives, optimizer, data split, seeds, and 300-step trajectories;
- NTP and K=2 MTP paths, diagnostic checkpoints `0,20,100,200,300`;
- fixed train/evaluation diagnostic batches covering all five domains and both states, with labels and paraphrase versions exactly balanced;
- ten paired four-H100 tasks, job `pt-rmyzkcq2`;
- all task, checkpoint, hash, processed-token, balance, finite-value, and restore guards pass;
- central finite-difference sign agrees in `5/5`; preregistered sign-plus-magnitude guard passes `4/5`;
- A11_15 condition-mean $Q$ curves reproduce within `0.0475`, below the `0.05` tolerance.

## Primary Evidence

| Decision metric | Result | Meaning |
|---|---:|---|
| step-0 $\widehat U_D^E>0$ | 1/5 | no stable initial downstream transmission |
| NTP-path usefulness AUC `0-200` positive | 1/5 | no stable counterfactual benefit along the standard path |
| MTP-path usefulness AUC `0-200` positive | 3/5 | H2 training changes geometry, but not consistently |
| step-0 mean $\widehat U_D^E$ | -0.0415 | extra H2 gradient points against held-out H1 margin on average |
| NTP step-200 mean $\widehat U_D^E$ | -0.1660 | negative direction strengthens late |
| central-difference sign agreement | 5/5 | autograd sign is validated |
| full finite-difference guard | 4/5 | derivative measurement is adjudicable |
| step-0 shared gradient squared-norm fraction | 0.9213 | failure is not lack of shared-gradient magnitude |

At step 200, all five NTP trajectories have negative usefulness. At step 300, all five remain negative, with mean `-0.1737`. The layer audit shows the negative step-0 contribution comes mainly from Transformer layers `0-20`; the tied embedding/interface contribution is small and slightly positive.

## Visualization Results

### Plot Contract

**Question:** does the extra H2 gradient move shared pretrained parameters toward the common-H1 held-out semantic boundary?  
**How to read:** values above zero in the upper-left panel are useful; the upper-right compares predicted and central finite differences; the lower-left shows how much H2-gradient norm is shared; the lower-right reproduces the common-H1 task curve.  
**Allowed conclusion:** local shared-gradient direction and its trajectory dependence.  
**Limitation:** this does not isolate whether the remaining mismatch comes from output interface/location transfer or unseen-paraphrase generalization.

![A11_16 shared-gradient transmission](figures/a11_16_pretrained_shared_gradient_transmission.png)

The NTP-path mean becomes negative after step 20 and stays negative. MTP co-adaptation eventually makes its own-path mean positive, but seed ranges cross zero and its trajectory AUC is positive in only `3/5`. More than `0.9` of the H2 gradient squared norm is shared at initialization, so the central failure is direction, not gradient routing volume.

## Theoretical Update

For two one-step updates from the same parameters,

$$
\theta_N'=\theta-\eta g_N,
\qquad
\theta_M'=\theta-\eta(g_N+g_D),
$$

the common downstream margin difference is:

$$
M_E(\theta_M')-M_E(\theta_N')
=\eta U_D^E+O(\eta^2).
$$

Therefore, informative-horizon coverage gives direct representation supervision, but a local downstream efficiency advantage additionally requires $U_D^E>0$ and controlled higher-order/background terms.

## Boundary And Next Decision

We can claim that this pretrained response-position experiment lacks stable positive raw-gradient transmission from the extra H2 objective to the held-out common-H1 boundary. We cannot claim that MTP is globally worse, that the same sign holds in pure MTP pretraining, or that a local derivative determines final benchmark performance.

The next minimal question is where the sign is lost: at the H2-to-H1 interface/position, or when moving from seen wording to unseen paraphrases. That requires a fixed 2-by-2 usefulness decomposition, not a new method or wider ablation.
