# A06_03_04_E01 Sparse Audition Duty-Cycle Protocol

Approval status: approved under the active long-run research instruction.

Purpose: identify the lowest challenger-audition rate that preserves reliable
rank-4 useful-expert discovery under full-sequence LM training.

Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_03_utility_binding_and_sparse_discovery/subanchors/06_03_04_tail_safe_phase_switch_anchor.md`.

## Terminology / Definitions

- **Audition update:** execute current top-1 and one rotating challenger, then
  train through their pair-renormalized mixture.
- **Selected-only update:** execute ordinary weighted top-1.
- **Duty cycle $\rho$:** fraction of discovery updates that are auditions.
  Mean expert forwards per token are $1+\rho$.
- **Retention:** a route that is corrected at discovery step 600 remains at
  useful-route accuracy at least `0.95` after 200 selected-only updates.

## Fixed Setup

- Reconstruct A06_03_03_E01 learned specialists and installed useful rank-4 routers.
- Freeze representation and experts; router-only SGD, learning rate `0.001`.
- Use full LM loss only: 16 task-dependent and 16 background targets.
- Discovery horizon: 600 updates. Retention horizon: 200 subsequent top-1
  updates with auditions disabled.
- Full run: 32 seeds and four tasks, or 128 cells per condition.

## Conditions

Use $\rho\in\{0,1/16,1/8,1/4,1/2,1\}$. A rational accumulator spaces audition
events uniformly. The challenger phase advances only on audition events and
cycles through a seed-specific permutation of the three nonselected experts.
The schedule uses no task, target, or useful-expert identity.

Generalist controls run at $\rho=1/8$ and $\rho=1$.

## Pressure Prediction

At the identical initial state, measure selected-only pressure $P_S$ and the
three-phase average audition pressure $P_A$ on the useful-versus-selected task
margin. Predict

$$
\rho_c=\frac{-P_S}{P_A-P_S}
$$

when $P_A>P_S$ and $P_S<0$. This is a local prediction. It is compared with the
finite-time transition but is not used to select or alter tested conditions.

## Primary Decision

For each $\rho$, report correction rate and a seed-clustered 95% bootstrap
confidence interval. The minimum viable duty cycle is the smallest tested
$\rho$ with:

1. observed correction rate at least `0.90`;
2. bootstrap lower bound at least `0.85`;
3. generalist arbitrary-target rate below `0.10` at the corresponding guard;
4. at least `0.90` retention among corrected cells.

Hypotheses:

- **H1 threshold law:** some $\rho<1$ is viable and the empirical transition is
  within one adjacent grid interval of median predicted $\rho_c$.
- **H2 continuous audition required:** no $\rho<1$ is viable.
- **H3 rare audition sufficient:** some $\rho\le1/8$ is viable, giving mean
  activated experts at most `1.125`.
- **H4 local pressure nonpredictive:** a subunit duty cycle is viable, but the
  predicted and empirical transitions disagree by more than one grid interval.

## Validity Guards

- all A06_03_03_E01 specialist/generalist utility, installed-rank, score-gap, balance,
  finite-value, and state-pairing guards pass;
- exact realized audition count differs from $600\rho$ by at most one;
- each audition activates exactly two experts; selected-only activates one;
- challenger phases differ by at most one count;
- $ho=1$ reproduces A06_03_03_E01 rank-4 correction within 5 percentage points;
- $ho=0$ reproduces the top-1 blind basin below 10% correction.

## Claim Boundary

This protocol can establish a controlled activated-compute/correction frontier
and test a local margin-drift threshold. It cannot establish pretrained-LLM
wall-clock savings, many-expert communication cost, adaptive MTP triggering, or
natural downstream specialization.
