# Summary: A06_02_02_E04 DNS Routing Preservation Audit

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

Protocol: `protocol.md`

## Result Snapshot

Verdict: **DNS routing alone is not supported; router-row projection gives the clearest partial improvement, but no tested condition preserves positive margin through 2000 full-LM steps.**

What we established: subtracting the all-position mean from the router input does not by itself prevent long full-LM margin erosion. The strongest tested intervention is row projection away from the common direction, which improves the denoised-gradient condition's final margin from -15.586 to -8.960, but the margin remains negative.

What the experiment shows: the hypothesis "routing collapses because the router sees a common component" is too strong in its simple mean-DNS form. Common direction matters as a row constraint, but DNS input subtraction alone does not solve preservation.

What we do next: keep router-row projection / router-side constraint as a promising preservation clue, but do not use mean-DNS routing alone as the next method.

## Purpose

A06_01_05_E04 showed that full-LM long training erodes feature margins. This run tests whether DNS-style common-subtracted routing, a denoised gradient selector, router-row projection, lower router learning rate, or early router freezing can preserve margin under the same full-LM objective.

## Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| DNS routing | Route on a common-subtracted hidden state | router input \(h-c\) | hidden vector | Tests whether common input drives collapse | True causal common operator |
| Common direction | Operational common component | all-position hidden mean at warmup 40 | vector | Component removed by DNS | Semantic commonness |
| Denoised gradient selector | Position-normalized embedding-gradient selector | \(z_{i,p}=(E_{i,p}-\mu_p)/(\sigma_p+\epsilon)\) | z-score | Tests whether position-wide gradient bias hurts selection | Feature labels |
| Row projection | Remove common direction from router rows | \(w\leftarrow w-(w^\top \hat c)\hat c\) | row update | Tests row drift into common direction | Optimal constraint |
| Margin p05 | Low-tail matched expert score gap | 5th percentile of matched expert score minus competitor | router-logit gap | Primary preservation guard | Expert utility |

## Exact Setup

Data/model: same A06_01_05_E04 synthetic no-position bridge, one causal Transformer layer, one weighted top-1 MoE layer, four uniformly sampled features, four experts.

Objective: full-sequence next-token LM loss only.

Warmup: 40 steps.

Post-reinit training: 2000 steps.

Checkpoints: 0, 160, 500, 1000, 2000.

Coverage: 8 seeds × 4 slot lengths = 32 cells, 1600 trajectory rows.

Execution: remote 4-GPU submission was blocked by workspace quota, so the full grid was completed locally on one H100 MIG GPU.

## Primary Result

At step 2000:

| Condition | Feature NMI | Margin p05 | Positive margin frac | Target accuracy |
| --- | ---: | ---: | ---: | ---: |
| raw route center | 0.852 | -3.980 | 0.898 | 0.950 |
| DNS oracle | 0.820 | -4.105 | 0.868 | 0.957 |
| raw oracle | 0.834 | -4.422 | 0.881 | 0.957 |
| DNS route center | 0.811 | -5.064 | 0.874 | 0.959 |
| denoised + DNS + row projection | 0.608 | -8.960 | 0.482 | 0.973 |
| denoised + DNS + router LR 0.1 | 0.522 | -10.063 | 0.462 | 0.955 |
| raw gradient top1 | 0.684 | -10.702 | 0.647 | 0.956 |
| gradient top1 + DNS | 0.561 | -12.271 | 0.592 | 0.962 |
| denoised gradient + DNS + freeze160 | 0.499 | -15.491 | 0.480 | 0.955 |
| denoised gradient + DNS | 0.464 | -15.586 | 0.446 | 0.960 |

## Interpretation

DNS routing alone worsens the raw gradient selector: raw gradient top1 has final margin -10.702, while gradient top1 + DNS has -12.271.

The denoised position-normalized selector is worse than raw selection in this implementation: denoised + DNS has final margin -15.586 and NMI 0.464.

Row projection is the strongest preservation intervention: denoised + DNS + row projection improves final margin to -8.960 and NMI to 0.608. This does not solve the problem because margin remains negative, but it supports a weaker claim that constraining router rows away from the common direction can reduce damage.

Lower router LR gives a smaller partial improvement: final margin -10.063. Early freeze for 160 steps does not help.

## Key Figures

### Figure: Margin And NMI Trajectory

![DNS margin trajectory](figures/a06_29_dns_margin_trajectory.png)

What this tests: whether DNS or router interventions slow full-LM margin erosion.

Observed result: all conditions eventually go negative in margin p05. Clean center controls remain best. Row projection is the best gradient-selector intervention.

Allowed claim: row projection is a preservation clue; mean-DNS routing is not sufficient.

### Figure: Step-2000 Final State

![DNS final step](figures/a06_29_dns_final_step2000.png)

What this tests: final routing quality after 2000 full-LM steps.

Observed result: raw route / oracle controls still dominate NMI and margin. Row projection is the best among gradient-selector variants but remains negative-margin.

Allowed claim: none of the tested DNS/gradient variants preserve a safe margin.

## Claim Boundary

Can claim:

- Mean-DNS routing alone does not solve the full-LM preservation problem in this synthetic bridge.
- Position-normalized gradient selection, as implemented here, does not improve over raw embedding-gradient top1.
- Router-row projection provides the clearest partial improvement among tested router-side interventions.

Cannot claim:

- Common components are irrelevant. Row projection suggests row-common interaction still matters.
- DNS with a better common operator cannot work.
- This result transfers directly to real language data.
- Row projection is sufficient; it improved margin but did not make it positive.

## Next Decision

Do not continue with mean-DNS routing alone. The next minimal step should test **row-projected clean centers and row-projected raw gradient top1** directly, separating row constraint from denoised selector failure.
