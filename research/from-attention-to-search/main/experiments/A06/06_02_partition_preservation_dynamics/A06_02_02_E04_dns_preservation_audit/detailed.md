# Detailed: A06_02_02_E04 DNS Routing Preservation Audit

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

Protocol: `protocol.md`

Summary: `summary.md`

## 0. Quick Recap

Purpose: test whether common-subtracted routing or simple router-side constraints preserve feature margins under full-LM long training.

Conclusion: DNS routing alone failed. Position-normalized gradient selection failed. Router-row projection gave the clearest partial improvement, but no tested condition preserved positive margin p05 at 2000 steps.

Primary evidence: final margin p05 is -10.702 for raw gradient top1, -12.271 for gradient top1 + DNS, -15.586 for denoised gradient + DNS, and -8.960 for denoised gradient + DNS + row projection.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit / formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| DNS routing | Route on common-subtracted hidden state | \(h_{\mathrm{dns}}=h-c\) | hidden vector | Tests common-input drift | True common operator |
| Common direction | Fixed common component | all-position hidden mean at warmup 40 | vector | Removed by DNS and used for row projection | Causal commonness |
| Denoised gradient selector | Normalize gradient energy per position | \(z_{i,p}=(E_{i,p}-\mu_p)/(\sigma_p+\epsilon)\) | z-score | Removes position-wide score bias | Feature relevance |
| Row projection | Remove common direction from router rows after updates | \(w\leftarrow w-(w^\top \hat c)\hat c\) | row update | Tests row-common constraint | Optimality |
| Router LR 0.1 | Lower router-row learning rate | router parameter group uses 0.1 base LR | LR scale | Tests router drift sensitivity | Common causality |
| Early freeze | Prevent router updates early | zero router gradients through step 160 | steps | Tests early-drift hypothesis | Long-run solution |

## 2. Protocol Compliance

Approved setup: full-LM loss, warmup 40, checkpoints 0/160/500/1000/2000, 10 conditions, 8 seeds, 4 slot lengths.

Actual setup: matched.

Coverage: 32/32 cells completed.

Rows: 1600 training trajectory rows.

Remote status: 4-GPU ACP submission failed twice because workspace member quota had 0 GPUs remaining. The full grid was completed locally on one H100 MIG GPU.

## 3. Data / Model / Objective

Data: synthetic no-position bridge inherited from A06_01_05_E04.

Model: one causal Transformer layer plus one weighted top-1 MoE layer.

Objective:

\[
\mathcal L^{full}_i=\sum_{p=0}^{T-2}\mathrm{CE}(\ell_{i,p},x_{i,p+1}).
\]

Common direction:

\[
c=\frac{1}{N T}\sum_{i,p}h_{i,p}
\]

computed on calibration hidden states after 40 full-LM warmup steps.

DNS router input:

\[
h_{\mathrm{dns}}=h-c.
\]

Row projection:

\[
w_e \leftarrow w_e - (w_e^\top \hat c)\hat c.
\]

## 4. Conditions

| Condition | Router input | Initial rows | Intervention | Role |
| --- | --- | --- | --- | --- |
| raw oracle | \(h\) | feature-label centers | none | clean upper bound |
| DNS oracle | \(h-c\) | feature-label centers in DNS coordinates | none | clean DNS control |
| raw route center | \(h\) | route-position k-means | none | route-state control |
| DNS route center | \(h-c\) | route-position k-means in DNS coordinates | none | route-state DNS control |
| raw gradient top1 | \(h\) | raw embedding-gradient top1 | none | A06_01_05_E04 baseline |
| gradient top1 + DNS | \(h-c\) | raw embedding-gradient top1 in DNS coordinates | none | DNS input test |
| denoised gradient + DNS | \(h-c\) | position-normalized gradient top1 | none | denoised selector test |
| denoised + DNS + row projection | \(h-c\) | position-normalized gradient top1 | project rows after updates | row constraint test |
| denoised + DNS + LR0.1 | \(h-c\) | position-normalized gradient top1 | router LR 0.1 | low LR test |
| denoised + DNS + freeze160 | \(h-c\) | position-normalized gradient top1 | freeze router first 160 steps | early freeze test |

## 5. Main Trajectory

| Condition | Checkpoint | Feature NMI | Margin p05 | Positive margin frac | Sign flip rate | Target accuracy | Router-common cosine |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| raw oracle | 0 | 1.000 | 11.670 | 1.000 | 0.000 | 0.248 | nan |
| DNS oracle | 0 | 1.000 | 8.773 | 1.000 | 0.000 | 0.248 | 0.450 |
| raw route center | 0 | 1.000 | 11.670 | 1.000 | 0.000 | 0.255 | nan |
| DNS route center | 0 | 1.000 | 8.773 | 1.000 | 0.000 | 0.257 | 0.450 |
| raw gradient top1 | 0 | 0.853 | 1.436 | 0.824 | 0.000 | 0.311 | nan |
| gradient top1 + DNS | 0 | 0.803 | -1.463 | 0.768 | 0.000 | 0.296 | 0.388 |
| denoised gradient + DNS | 0 | 0.729 | -4.519 | 0.669 | 0.000 | 0.282 | 0.230 |
| denoised + DNS + row projection | 0 | 0.792 | -2.537 | 0.738 | 0.000 | 0.283 | 0.000 |
| raw oracle | 160 | 1.000 | 6.273 | 1.000 | 0.000 | 0.524 | nan |
| DNS oracle | 160 | 0.982 | 4.095 | 0.989 | 0.011 | 0.516 | 0.435 |
| raw route center | 160 | 0.995 | 5.839 | 0.997 | 0.003 | 0.536 | nan |
| DNS route center | 160 | 0.989 | 4.012 | 0.993 | 0.007 | 0.529 | 0.434 |
| raw gradient top1 | 160 | 0.826 | -2.554 | 0.697 | 0.193 | 0.539 | nan |
| gradient top1 + DNS | 160 | 0.765 | -3.576 | 0.723 | 0.112 | 0.545 | 0.379 |
| denoised gradient + DNS | 160 | 0.635 | -6.627 | 0.501 | 0.304 | 0.530 | 0.230 |
| denoised + DNS + row projection | 160 | 0.809 | -3.865 | 0.593 | 0.298 | 0.526 | 0.000 |
| raw oracle | 2000 | 0.834 | -4.422 | 0.881 | 0.119 | 0.957 | nan |
| DNS oracle | 2000 | 0.820 | -4.105 | 0.868 | 0.132 | 0.957 | 0.385 |
| raw route center | 2000 | 0.852 | -3.980 | 0.898 | 0.102 | 0.950 | nan |
| DNS route center | 2000 | 0.811 | -5.064 | 0.874 | 0.126 | 0.959 | 0.382 |
| raw gradient top1 | 2000 | 0.684 | -10.702 | 0.647 | 0.281 | 0.956 | nan |
| gradient top1 + DNS | 2000 | 0.561 | -12.271 | 0.592 | 0.267 | 0.962 | 0.356 |
| denoised gradient + DNS | 2000 | 0.464 | -15.586 | 0.446 | 0.378 | 0.960 | 0.253 |
| denoised + DNS + row projection | 2000 | 0.608 | -8.960 | 0.482 | 0.455 | 0.973 | 0.000 |
| denoised + DNS + LR0.1 | 2000 | 0.522 | -10.063 | 0.462 | 0.354 | 0.955 | 0.231 |
| denoised + DNS + freeze160 | 2000 | 0.499 | -15.491 | 0.480 | 0.327 | 0.955 | 0.256 |

## 6. Slot-Length Boundary

Final margin p05 by slot length:

| Slot length | raw grad top1 | grad top1 + DNS | denoised + DNS | denoised + DNS + row projection | denoised + DNS + LR0.1 | denoised + DNS + freeze160 | raw oracle | DNS oracle |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | -10.844 | -11.389 | -13.259 | -6.232 | -7.988 | -12.761 | -1.003 | 0.266 |
| 2 | -6.166 | -4.976 | -16.571 | -9.106 | -12.497 | -15.839 | -4.993 | -6.139 |
| 4 | -14.424 | -14.872 | -18.041 | -9.770 | -11.600 | -22.391 | -7.609 | -8.729 |
| 8 | -11.373 | -17.846 | -14.474 | -10.734 | -8.168 | -10.973 | -4.084 | -1.818 |

The row-projection condition improves margin for slot lengths 1, 4, and 8 relative to denoised + DNS, but it does not produce a positive aggregate margin.

## 7. Selector Diagnostics

Raw gradient top1 selects route positions 26.7% of the time and slot positions 40.4% of the time.

The position-normalized denoised selector selects route positions only 8.3% of the time and slot positions 12.9% of the time. This explains why the current denoised selector underperforms: the normalization removes useful feature-slot signal along with position-wide bias.

## 8. Visualization Results

### Figure: DNS Margin Trajectory

![DNS margin trajectory](figures/a06_29_dns_margin_trajectory.png)

Purpose: test whether DNS or router constraints slow margin erosion.

Setup: full-LM loss, warmup 40, 32 cells, checkpoints 0/160/500/1000/2000.

How to read: positive margin p05 is required for preservation. NMI alone is not enough.

Observed result: all conditions eventually have negative margin. Row projection is the best gradient-selector intervention.

Take-home: simple mean-DNS routing is not sufficient; router-row constraints are more promising.

### Figure: Step-2000 Final State

![DNS final state](figures/a06_29_dns_final_step2000.png)

Purpose: compare final 2000-step outcomes.

Observed result: route/center controls remain best; row projection is the best non-center intervention; DNS and denoised selector alone are worse than raw gradient top1.

Take-home: the preservation path should focus on row constraints, not mean-DNS input alone.

## 9. Failure Decomposition

DNS input subtraction failed because it did not preserve the score gap. It may remove some common offset, but it does not stop full-LM optimization from finding a different low-loss routing geometry.

The denoised selector failed because the position-normalized score selected fewer route/slot positions than the raw score. This is a concrete operational failure of the current denoising rule, not evidence that all denoised selectors must fail.

Row projection partially succeeded because it directly controls the router-row component along the common direction. However, row projection alone cannot keep the gradient-selected partition margin-positive.

## 10. Claim Boundary

Can claim:

- Mean-DNS routing is not sufficient in this controlled full-LM bridge.
- Current position-zscore gradient denoising is worse than raw embedding-gradient top1.
- Router-row projection is the strongest tested preservation clue.

Cannot claim:

- Common drift is false in all forms.
- A better common operator or stronger projection method cannot work.
- The result transfers directly to real-DCLM.
- Row projection solves preservation.

## 11. Next Decision

Next minimal test: isolate row projection without the failed denoised selector.

Run clean comparisons:

- raw gradient top1;
- raw gradient top1 + row projection;
- route center + row projection;
- oracle center + row projection;
- optional router LR 0.1 on raw gradient top1.

This will decide whether the useful part is row projection itself or only an interaction with the denoised/DNS coordinate system.

## 12. Artifact Map

Experiment folder:
`Projects/from-attention-to-search/main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_02_E04_dns_preservation_audit/`

Runner:
`scripts/run_a06_29_dns_routing_preservation_audit.py`

Protocol:
`protocol.md`

Tables:

- `tables/training_trajectory.csv`
- `tables/condition_trajectory_aggregate.csv`
- `tables/condition_aggregate_final.csv`
- `tables/condition_final_by_slot.csv`
- `tables/selector_diagnostics_aggregate.csv`

Figures:

- `figures/a06_29_dns_margin_trajectory.png`
- `figures/a06_29_dns_final_step2000.png`

Execution:

- remote 4-GPU submission attempted but blocked by quota;
- full grid completed locally on one H100 MIG GPU;
- run name: `a06_29_dns_routing_preservation_full_local1gpu_20260706`.
