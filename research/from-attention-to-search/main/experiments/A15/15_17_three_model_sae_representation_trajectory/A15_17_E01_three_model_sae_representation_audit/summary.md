# Summary: A15_17_E01 Three-Model SAE Representation Audit

Primary Anchor: [A15_17](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/15_17_three_model_sae_representation_trajectory_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md)  
Detailed record: [detailed.md](detailed.md)  
Result status / eligibility: S2--S6 `PASS`; evidence `ELIGIBLE`; scientific verdict `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`.

> Job `pt-we1cni15` completed the full matrix and artifact audit. The values below are eligible observations. The bounded-support judgment still requires researcher confirmation and has not been promoted into the Anchor or the human-owned Focus conclusion.

## 1. Purpose

Determine whether M0 Dense, M1 detached-reconstruction SAE, and M2 live-reconstruction plus SAE-only AuxK develop different domain-readable and coarse/fine representation trajectories at the same 0--10B checkpoints, and whether any difference remains after fit-only removal of the dominant common direction.

## 2. Hypothesis

If SAE-mediated training changes residual accessible organization, at least one registered M1−M0, M2−M1, or M2−M0 contrast will form a coherent trajectory in raw \(h\) or actual final-MLP input and retain separation after B2 or B3 first-singular-direction removal.

The strongest rival is that any raw difference is explained by lexical composition, reconstruction error, probe variation, the global mean, or one dominant common direction; a second rival is that local gradients differ without a corresponding held-out representation difference.

## 3. Analysis Method

- Compare paired M1−M0, M2−M1, and M2−M0 results on identical P/N report units across 0, 0.5, 1, 3, 5, and 10B. Primary readings are global-fine balanced accuracy, parent-conditioned fine-class Fisher trace, and cosine relation margin on actual MLP input and raw \(h\), with 5,000-draw stratified paired bootstrap intervals.
- Independently apply fit-only B1 centering, B2 removal of the uncentered fit matrix's first right-singular direction, and B3 centering followed by first-direction removal. Refit probes after projection using the raw-selected \(C\).
- Audit M1/M2 sparse overlap and health, four fixed local-gradient batches per checkpoint, and 0B-inclusive atom/PCA/UMAP/t-SNE evolution figures. These diagnose SAE health and objective action without substituting for causal model use.

## 4. Conclusion

Verdict: `AI_DRAFT_SUPPORTING_BOUNDED_AWAITING_HUMAN_CONFIRMATION`.

1. **An eligible, checkpoint-coherent M1 geometry difference survives common-direction removal.** On P actual MLP input, the parent-conditioned fine Fisher M1−M0 deltas at 1/3/5/10B are `+0.0709 / +0.1045 / +0.0995 / +0.2777` raw and `+0.0757 / +0.1098 / +0.1141 / +0.2661` after B3; every corresponding pointwise 95% interval excludes zero. N B3 actual input likewise has positive M1−M0 deltas from 0.5B through 10B. This meets the registered bounded-support branch for residual geometry, not for functional use.

2. **Linear readability does not yield a global three-model ranking.** At P 3B actual input, M1−M0 is `+0.0778 [0.0333, 0.1222]` while M2−M1 is `−0.0667 [−0.1111, −0.0222]`; after B3 they remain `+0.0611 [0.0167, 0.1111]` and `−0.0611 [−0.1056, −0.0167]`. Most other checkpoints are unresolved, and every N raw-\(h\) global-fine probe comparison is unresolved. M1 3B is therefore the smallest candidate point; neither SAE model is generally superior, and M2 is not established as better than M1.

3. **The first common direction is not a sufficient explanation for the M1 Fisher trajectory.** B2 removes `73.0%--94.5%` of P actual-input fit energy at 3B and `75.4%--99.4%` at 10B; B3 removes `21.2%--24.9%` and `23.3%--82.9%`, respectively. The M1−M0 Fisher deltas remain close to raw and retain direction.

4. **Sparse and gradient diagnostics match the intended topology but are not causal evidence.** M1 reconstruction gradients are zero in backbone groups. M2 has nonzero 10B reconstruction gradients in backbone groups, with median reconstruction/LM weighted-norm ratio `0.0406` across recorded rows. M2 AuxK is SAE-only and reaches at most `0.0005707` at 10B; all four 0B batches have zero active AuxK examples and exact zero gradients.

Intervals are registered pointwise descriptive intervals without family-wise correction; checkpoints are not independent experimental replicates.

| Registered rule | Observed value | Guard / eligibility | Verdict | Evidence source |
|---|---|---|---|---|
| S2 runtime, hook, finite-value, and state-immutability qualification | 6/6 tasks pass; 17 remote tests pass; zero optimizer/buffer updates | four H100s visible; before/after state hashes match | `PASS` | [execution_receipt.md](execution_receipt.md) |
| Full 18-checkpoint coverage | 18 caches, gradients, and completion records; all content hashes match | four fixed gradient batches per record | `PASS` | [detailed.md](detailed.md#3-protocol-freeze-conformance-and-deviations) |
| Coherent paired raw trajectory | P actual Fisher M1−M0 positive at 1/3/5/10B | identical report units; 5,000 paired draws | `SUPPORTING_BOUNDED` | [paired_fisher_differences.csv](tables/paired_fisher_differences.csv) |
| Residual separation after B2 or B3 | same P trajectory survives B2/B3; N B3 also forms a positive M1−M0 trajectory | 216 complete fit-only transforms | `SUPPORTING_BOUNDED` | [paired_fisher_differences_B.csv](tables/paired_fisher_differences_B.csv) |
| Probe yields a consistent model ranking | only checkpoint/panel-specific separation; all N raw-\(h\) comparisons unresolved | all 2,100 probe metric cells eligible | `NOT_SUPPORTED_AS_GLOBAL_RANKING` | [raw probe deltas](tables/paired_probe_differences.csv), [B probe deltas](tables/paired_probe_differences_B.csv) |
| Required visual evidence | 16/16 figures present and decodable; A06 and all A09 variants include 0B | UMAP spectral-init warnings fell back to fixed-seed random initialization; descriptive use only | `PASS_WITH_DESCRIPTIVE_LIMIT` | [detailed.md](detailed.md#8-visualization-results) |

### Important Figures

![Actual final-MLP-input global-fine readability](figures/A03_actual_input_readability.png)

How to read: trained tokens are on the x-axis and report balanced accuracy on the y-axis. P M1 is above M0 and M2 at 3B, but the other points do not form one global ranking; use the paired source table for intervals.

![Raw-h readability after fit-only transforms](figures/B02_probe_after_direction_removal.png)

How to read: line styles are B1/B2/B3. Some P separations remain after first-direction removal while N curves stay close; the verdict comes from paired tables, not visual selection.

The requested 0B-inclusive descriptive figures are complete: [A06 atom activation](figures/A06_sae_health_and_features.png), [A09 PCA](figures/A09_representation_evolution_pca.png), [A09 UMAP](figures/A09_representation_evolution_umap.png), and [A09 t-SNE](figures/A09_representation_evolution_tsne.png). They are not used to select a model or checkpoint.

### Claim Boundary

Can claim: eligible evidence supports a parent-conditioned fine-class residual-geometry difference between M1 and M0 in frozen actual MLP inputs, coherent across multiple checkpoints and retained after fit-only B2/B3. Checkpoint-specific probe, sparse-use, and local-gradient observations may also be reported.

Cannot claim: native Gate or MLP causal use, expert specialization, downstream language-model improvement, general M1/M2 superiority, or semantic identity of SAE atom IDs across models or checkpoints.

### Next Step Analysis

Decision: `AI suggestion` — after confirming this bounded verdict, decide whether M1 3B should be the candidate for a separately designed causal functional intervention. This experiment does not authorize that follow-up.

Why it follows: at M1 3B, both actual-input probe (`+0.0778`) and Fisher (`+0.1045`) contrasts survive B2/B3, making it the smallest candidate not dependent on one metric.

Unresolved uncertainty: whether the standard model computation causally uses this readable geometry and whether intervention changes held-out function.

Completion criterion: the researcher confirms or corrects the direct result, claim boundary, and this one next decision.

Stop or redirect condition: if pointwise intervals plus development replication are not sufficient nomination evidence, or a later matched-cost intervention has no stable functional effect, stop treating the current SAE configuration as established mechanism evidence.

Resume action: read [detailed.md](detailed.md), then record the researcher judgment before any scientific Anchor update.
