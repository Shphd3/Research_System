# A15_13_E20 Result Summary

[Protocol](protocol.md) · [Complete training report, full configuration, loss audit and evaluation figures](detailed.md)
Execution: COMPLETE; job `pt-os72i446` SUCCEEDED at 2026-09-08 06:27:46 UTC.
Evidence: primary internal-test comparison eligible under E20-A1–A4; generation bounded to the implemented evaluator.
Scientific interpretation: AI analysis requested by researcher; mechanism judgment and Focus transition await human confirmation.

The full report includes SAE pretraining and feature clustering, flat GMM, all nine offline Router selections, exact expert position/parameter counts, answer-only SFT loss location, all 15 per-task evaluation rows, three-seed means and evaluation figures. All 15 SFT conditions use no load-balancing loss; task-only additionally updates its 8,200-parameter Router. Post-hoc route concentration and gate-coefficient observations are reported as diagnostics, not established mechanisms.

## Purpose

Test whether final-layer sparse-autoencoder (SAE) co-activation grouping provides useful expert routing beyond matched random grouping and ordinary task-trained routing.

## Hypothesis

Task-relevant SAE structure should lower answer-token loss relative to random grouping in every seed; full method advantage additionally requires outperforming task-only routing. The strongest rival is that ordinary task optimization is sufficient and frozen semantic structure adds no competitive advantage.

## Analysis method

- Hold model, audited split, paired sample schedules and 512 updates fixed across five conditions and seeds 17/29/43. Score the fixed final checkpoint, not the best test checkpoint.
- Compare answer-token negative log likelihood (NLL; nats/token, lower is better) on 8,481 paired internal-test records. Use 2,000 source-stratified record-bootstrap draws separately per seed.
- Keep greedy generation scores and SAE/GMM expert-selection interventions separate from primary loss and from semantic or causal mechanism claims.

## Conclusion

The registered numerical branch is **STRUCTURE_ONLY**: SAE beats random grouping in all seeds, but loses to task-only routing in all seeds. This label means a narrow comparative loss advantage over the random control, not proof of semantic truth.

| Seed | Random minus SAE [95% CI] | Task-only minus SAE [95% CI] |
|---:|---:|---:|
| 17 | 0.002793 [0.002503, 0.003077] | -0.047482 [-0.048594, -0.046405] |
| 29 | 0.002088 [0.001809, 0.002363] | -0.045996 [-0.047092, -0.044922] |
| 43 | 0.000682 [0.000356, 0.000999] | -0.041096 [-0.042105, -0.040068] |

Source: [aggregate primary contrasts](/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z/results/aggregate.json), computed from paired per-record loss sums and answer-token denominators; [verification](/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z/report_20260908/verification.json).
The smallest SAE advantage over random is 0.000682 nats/token (seed 43; CI 0.000356–0.000999). Task-only has 0.041096–0.047482 lower NLL than SAE.

| Condition | Mean test NLL | Mean generation macro % |
|---|---:|---:|
| sae | 0.734773 | 19.77 |
| random_features | 0.736627 | 20.73 |
| gmm | 0.720896 | 20.68 |
| task_only | 0.689914 | 20.50 |
| dense_r16 | 0.737787 | 19.85 |

Means across three seeds are descriptive, not pooled inference. Generation macro gives each of the eight tasks equal weight and is not an overall per-record accuracy. Its ranking differs from NLL; SAE does not show consistent generated-answer improvement over random. Full per-model and task results are in [Detailed](detailed.md#completed-model-results).

### Claim boundary

All 15 models completed 512 updates, 75 checkpoint files, 15 test-loss evaluations, 15 generation evaluations and 30 pairwise analyses. This is one base model, final layer, eight experts, and a post-dedup internal split—not official benchmark performance. Partial grouping diagnostics do not prove full stability/null mixing. Generation uses 4/64/256-token source-specific caps and simplified answer normalization; do not call it a uniform-512-token or official evaluation. Native-route intervention sensitivity does not establish semantic specialization.

### Next step analysis — AI proposal, not a confirmed decision

Review whether the narrow SAE-versus-random loss gain warrants further mechanism work given the much stronger task-only control and absent consistent generation gain. The unresolved question is whether frozen partition information helps beyond what ordinary task learning obtains; this run does not isolate why task-only wins. Completion criterion: researcher confirms the bounded result and one separating question. Stop or redirect if the purpose requires broad task performance superiority, which this run does not support. No new training is proposed for automatic execution.
