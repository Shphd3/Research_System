# A06_02_04_E04 Summary: Post-Cross Recovery Is Redundant And Path-Dependent

## What We Established

In the controlled fixed-expert bridge, post-cross representation updates are **not necessary** for most router-boundary re-entry, and post-cross router updates are **not necessary at all**. From 84 identical first-crossing states, joint continuation re-enters in 84/84 cases, representation-frozen continuation in 79/84, and router-frozen continuation in 84/84.

The original population-level hypothesis that representation is required mainly by indirectly shaping future router updates is rejected. The sharper result is that router and representation provide mostly redundant recovery paths, while their functional roles differ: router-only continuation restores the boundary but leaves substantially higher LM loss, whereas representation-only continuation restores both the boundary and nearly all task learning achieved by joint continuation.

## Terminology / Definitions

| Term | Plain meaning | Computation | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- |
| Critical pair | Feature and competitor fixed at first crossing | \((f,b_c)\) at \(t_c\) | keeps the recovered boundary fixed | all other boundaries are safe |
| Re-entry | The fixed crossed margin becomes positive within 50 updates | \(m_{f,b_c}(t_c+\tau)>0\) | primary recovery event | expert utility |
| Representation frozen | Continue router updates from the identical crossing state but stop upstream updates | causal path deletion | tests representation necessity | representation has no effect |
| Router frozen | Continue upstream updates but do not apply router-row updates | causal path deletion | tests direct representation sufficiency | router is never useful |
| Router-update replay | Freeze representation and apply the exact joint router updates | oracle mediation diagnostic | tests whether the joint router trajectory carries recovery | deployable method |
| Freeze necessity | Joint recoveries removed by deleting one path | \(N_k(re)\) | identifies necessary paths | sufficiency |
| Direct representation contribution | Center-motion and finite-step interaction term within one trajectory | cumulative \(C\) | tests direct geometric repair on that trajectory | intervention-invariant contribution |

## Exact Setup

- Four uniform features and four fixed function-matched experts.
- Static batch of 32 sequences, sequence length 33, and all 32 next-token losses.
- Critical regimes contain 8/32 or 4/32 signal sequences; remaining sequences are class-0 background.
- One causal Transformer layer, residual connection, layer normalization, one weighted-top-1 MoE, and no positional embedding.
- Representation AdamW learning rate 0.002.
- Router uses current raw-gradient direction scaled to the full AdamW candidate norm.
- Initial center-margin p05 target 0.5.
- Trigger the first nonpositive margin for features 1--3 within 50 updates, clone the complete post-update state, then run every branch for 50 updates.
- 32 seeds, 84 eligible event units, remote four-GPU job `pt-gq034aru`.

## Primary Result

| Post-cross branch | Critical-pair re-entry | Freeze necessity | Median re-entry | Mean loss after 50 updates |
| --- | ---: | ---: | ---: | ---: |
| Joint continuation | 84/84 = 100% | -- | 1 | \(1.57\times10^{-4}\) |
| Representation frozen | 79/84 = 94.05% | \(N_{repr}=5.95\%\) | 1 among recovered | \(3.08\times10^{-3}\) |
| Router frozen | 84/84 = 100% | \(N_{router}=0\) | 5.5--6 by regime | \(1.69\times10^{-4}\) |
| Representation frozen + joint-router replay | 80/84 = 95.24% | diagnostic | 1 among recovered | \(3.10\times10^{-3}\) |

The seed-clustered 95% confidence interval for \(N_{repr}\) is \([0,12.09\%]\). Representation freezing therefore fails the preregistered necessity threshold of 75%. Router freezing removes no recovery events.

## Mechanism Classification

The 84 events separate into:

| Path class | Events | Operational meaning |
| --- | ---: | --- |
| Either single path recovers | 79 | router-only and representation-only branches both re-enter |
| Representation-required direct recovery | 4 | router-only and router-replay fail; router-frozen representation motion re-enters; joint \(C>0\) at re-entry |
| Representation-required indirect router shaping | 1 | router-only fails; replaying joint router updates succeeds while joint \(C\le0\) |

This rejects one global recovery mechanism. Most events have redundant paths, while five events require representation learning under the native router trajectory.

## Central Figures

### Recovery After The Identical Crossing State

![Post-cross recovery curves](figures/recovery_curves.png)

- **Question:** Which post-cross path is necessary for re-entry?
- **How to read:** The y-axis is the fraction of events not yet re-entered; lower is faster and more complete recovery.
- **Observed:** Joint and router-update replay recover almost immediately. Router-frozen representation recovery is slower but reaches 100%. Representation-frozen router recovery plateaus with five failures.
- **Take-home:** Router and representation are largely redundant for route recovery; router motion accelerates recovery but is not necessary.
- **Does not prove:** Equal task-learning value across paths.

### Trajectory-Local Margin Contributions

![Router and representation margin contributions](figures/budget_mediation.png)

- **Question:** How do the exact router and direct representation terms evolve after crossing?
- **How to read:** Values are cumulative margin changes divided by the initial pairwise margin. Positive values repair the boundary.
- **Observed:** Joint router contribution becomes strongly corrective. Under router freeze, direct representation contribution alone becomes strongly positive. Under joint training, the median direct term is initially negative and only later turns positive.
- **Take-home:** Direct representation motion is path-dependent. The joint-trajectory \(C\) term cannot be reused as the counterfactual \(C\) after router freezing.
- **Does not prove:** A transferable controller or real-LLM mechanism.

## Hypothesis Update

| Hypothesis | Verdict | Reason |
| --- | --- | --- |
| H1: representation is necessary after crossing | rejected | \(N_{repr}=5.95\%\), far below 75% |
| H2: router updates are necessary after crossing | rejected | router-frozen re-entry is 100% |
| H3: population-level indirect router shaping | rejected | H1/H2 fail; only one event matches the strict indirect class |
| H4 operational criterion: representation is not necessary for re-entry | supported | re-entry drop is 5.95% and median paired delay is zero |

The preregistered phrase "representation matters only before crossing" is too strong. Representation is not necessary for most **routing re-entry**, but router-frozen continuation shows that post-cross representation learning is sufficient for every event and is the main task-learning path.

## Updated Mechanism

The exact within-trajectory identity remains:

\[
\Delta m=R+C.
\]

The new causal result is:

\[
R^{joint}\ne R^{repr\ frozen},
\qquad
C^{joint}\ne C^{router\ frozen}.
\]

Deleting one parameter block changes future hidden states, losses, and gradients, so \(R\) and \(C\) are trajectory-local contributions rather than intervention-invariant causal quantities.

## Claim Boundary

**Established:** Mostly redundant post-cross recovery in the fixed-expert synthetic bridge; five representation-required events; route recovery and task learning are not equivalent; trajectory-local budget terms change under intervention.

**Not established:** Learned-expert utility formation, real-text preservation, deployable routing control, MTP benefit, downstream specialization, or compute-efficiency value.

## Next Decision

Do not continue decomposing recovery in the fixed function-matched expert table. The next anchor should remove that strongest oracle assumption:

> Given a correct initial feature partition but trainable experts without predefined feature functions, does route-conditioned data exposure create a positive feature-expert utility gap that subsequently stabilizes the same routing identity?

This moves the line from geometric recovery toward actual MoE specialization, where route identity must acquire functional expert value.

