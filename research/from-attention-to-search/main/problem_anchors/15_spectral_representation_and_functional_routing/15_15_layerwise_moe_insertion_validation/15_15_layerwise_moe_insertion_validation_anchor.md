# A15.15 — Layerwise Readability-Guided MoE Insertion Validation

```text
problem_key: A15.layerwise_moe_insertion_validation
conversation_owner: codex-thread:01a07a07-159a-7893-9f2f-0f120349f4b3
ownership_status: CLAIMED
status: E02_RESULT_AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
```

## 1. Problem Definition

The decision question is which of zero-indexed blocks `{0,10,13}` makes correct parent/child specialization produce both additional next-token task value and matched child-expert function, and whether that functional ordering agrees with the static-readability ordering `10 > 13 > 0`. Static readability is held-out label cross-entropy from a newly fitted classifier on a frozen state. Functional value requires held-out next-token negative log-likelihood and fixed-model wrong-expert interventions; route-label agreement cannot substitute for either.

This is an independent exploratory functional experiment. It preserves the A15.13 E19 `QUALIFICATION_FAILED` result rather than reclassifying it, and it keeps the deployed Router input at the Transformer block input, called site A. The post-attention MLP input, site B, remains out of scope. Passing can identify only a functional position among the three tested candidates; it cannot identify the best or earliest position among all 28 blocks.

## 2. Physical Priors

1. Correct semantic specialization has task value at a layer only if it improves next-token loss over both an active-rank-matched ordinary adapter and the same hierarchical topology with a legal within-parent shuffled child partition.
2. A trained child expert is functionally matched to its assigned child only if replacing it, with all parameters fixed, by either same-parent alternative child expert worsens next-token loss.
3. Static readability is a useful candidate generator only if the resulting functional ordering is reproducible across seeds; readable labels or semantic routes alone are insufficient.

These priors are locally falsified if correct grouping lacks either matched task gain or both wrong-child penalties, or if the functional ordering reverses across seeds.

## 3. Falsifiable Hypotheses

The primary hypothesis is that block 10 has stronger paired task and expert-match value than blocks 13 and 0 because it has the highest site-A joint linear readability of the three candidates. The strongest rival is that static accessibility only describes information availability, while optimization and expert function favor another tested block or no block consistently.

A supporting hypothesis is that correct grouping outperforms legal shuffled grouping at the same topology, separating semantic match from extra parameter capacity. The task-only online hierarchy measures the remaining learned-path gap but does not by itself establish correct semantic function.

## 4. Mathematical Model

For layer \(\ell\in\{0,10,13\}\) and seed \(s\in\{17,29\}\), let \(N^D_{\ell,s}\), \(N^T_{\ell,s}\), \(N^C_{\ell,s}\), and \(N^S_{\ell,s}\) be historical-confirmation next-token negative log-likelihood in nats per target token for the ordinary rank-24 adapter, task-only online hierarchy, correct forced hierarchy, and legally shuffled forced hierarchy. Define

\[
A_{\ell,s}=N^D_{\ell,s}-N^C_{\ell,s},\qquad
F_{\ell,s}=N^S_{\ell,s}-N^C_{\ell,s},\qquad
G_{\ell,s}=N^T_{\ell,s}-N^C_{\ell,s}.
\]

\(A>0\) is overall specialization value relative to ordinary adaptation; \(F>0\) is correct semantic grouping value relative to the matched shuffled topology; \(G\) is an auxiliary learned-path gap and mixes routing, probability-coefficient, and joint-training effects.

For the correct forced model, let \(N^{W1}_{\ell,s}\) and \(N^{W2}_{\ell,s}\) be losses when the selected child expert is replaced by each of the two same-parent alternatives. Define \(W^k_{\ell,s}=N^{Wk}_{\ell,s}-N^C_{\ell,s}\). The conservative paired-function score is

\[
H_{\ell,s}=\min(A_{\ell,s},F_{\ell,s},W^1_{\ell,s},W^2_{\ell,s}).
\]

A layer has replicated matched function only if \(H_{\ell,s}>0\) in both seeds. Among such layers, the two-seed mean \(H\) orders the tested candidates; ties within the paired article-component uncertainty are reported as unresolved. Static-order agreement is reported by the exact ordering and Spearman correlation across the three candidates, without treating three layers as a universal depth law.

## 5. Computational Realization

- Freeze Qwen3-0.6B-Base and use the unchanged M2D2 Wikipedia balanced `3×3` windows. Positions 63--254 predict tokens 64--255.
- Insert one adapter at block 0, 10, or 13. The Router always reads that block's input A; experts always consume the MLP down-projection input.
- The ordinary adapter has active rank 24. Each hierarchy activates shared rank 8, one parent rank 8, and one child rank 8. Correct and shuffled forced conditions have no Router and use unit coefficients; shuffled children come from the existing within-parent balanced seed-specific maps while the parent remains correct.
- The task-only hierarchy learns parent and child Routers only from language-model gradients through selected route probabilities. All adapters start independently from the same seed-controlled initialization family; the base and language head remain frozen.
- Every condition receives 512 optimizer updates with microbatch 8, accumulation 16, expert learning rate `2e-4`, Router learning rate `5e-4`, 26-update warmup, cosine decay, weight decay `0.01`, and gradient clipping `1.0`. Train, development, and historical confirmation handling is identical across layers.
- After training, evaluate all four conditions under their native paths. Then freeze every correct forced model and evaluate intact plus both same-parent wrong-child substitutions on exactly the same windows and aggregation.

## 6. Minimal Falsification Tests

The decisive test computes \(H_{\ell,s}\) for all three layers and both seeds from one frozen evaluator. Necessary guards are identical model/data hashes, exact A-site Router capture, down-projection expert injection, zero trainable base parameters, legal forced paths and unit coefficients, matched active rank and exposure, finite losses/gradients, complete 512-update recovery checkpoints, and identical evaluation row order.

`FUNCTIONAL_POSITION_AMONG_TESTED` requires exactly one layer with \(H>0\) in both seeds whose mean \(H\) exceeds the others outside the paired article-component interval. `MULTIPLE_TESTED_FUNCTIONAL_POSITIONS` means more than one layer passes but no unique winner is resolved. `NO_MATCHED_FUNCTIONAL_POSITION` means every layer has at least one non-positive component in both seeds. Seed reversals, overlapping top-layer uncertainty, missing arms, or failed guards are `INSUFFICIENT`. None of these outcomes changes the old E19 static verdict.

## 7. Current Evidence

A15.15 E01 compared blocks 1 and 9. Block 9 improved learned route-label accuracy but the learned-to-Oracle interaction was `+0.000625` nat/token in seed 17 and `-0.000911` in seed 29, while wrong-child effects did not uniformly favor block 9. Its registered result was `INSUFFICIENT`: readability predicted route accessibility, not reproducibly better function.

A15.13 E19 then measured the actual Router input A with two probe seeds. Its A-only point selector produced `{0,10,13}`, with primary block 10 and seed-specific primaries `10/10`; the static ordering within the set is `10 > 13 > 0`. Five of sixteen shuffled-probe qualification checks failed, so E19 remains `QUALIFICATION_FAILED`. The researcher explicitly preserves that failure but authorizes the three layers as exploratory functional candidates, judging the old all-null-pass rule too strict to block a direct functional comparison.

E02 completed all 24 update-512 conditions and 12 fixed-model wrong-child evaluations with all eligibility guards passing. Each tested block has \(H>0\) in both seeds: block 0 has `0.003425/0.002930`, block 10 `0.003967/0.004001`, and block 13 `0.004196/0.004260` nat per target token. The point order is therefore `13 > 10 > 0`, but block 13's paired lead intervals overlap zero against block 10 (`[-0.000054,0.001263]`) and block 0 (`[-0.000414,0.002093]`). The mechanically registered verdict is `MULTIPLE_TESTED_FUNCTIONAL_POSITIONS`: correct forced specialization is functional at all three candidates, but no unique insertion point is resolved. The complete evidence and eligibility audit are in the E02 [Summary](../../../experiments/A15/15_15_layerwise_moe_insertion_validation/A15_15_E02_exploratory_functional_candidate_test/summary.md) and [Detailed record](../../../experiments/A15/15_15_layerwise_moe_insertion_validation/A15_15_E02_exploratory_functional_candidate_test/detailed.md).

## 8. Claim Boundary And Next Decision

Verified evidence supports replicated forced-path task value and same-parent expert matching at all three tested blocks. It weakens the hypothesis that static readability uniquely orders functional insertion points: the static top two reverse descriptively, their functional difference is unresolved, and the three-item Spearman correlation is `0.5`. The task-only online Routers remain near chance and load-collapsed, so forced expert function cannot be promoted to learned semantic dispatch. The evidence cannot identify a unique tested layer, a 28-layer optimum, an earliest specialization layer, or retroactively qualify E19.

The one next decision is researcher confirmation or correction of the `MULTIPLE_TESTED_FUNCTIONAL_POSITIONS` boundary and whether any downstream implementation truly requires choosing between blocks 10 and 13. Completion is an explicit Focus-level result, cannot-claim boundary, and choice to stop or request a separately approved fresh replication. The resume action is to read the E02 Summary first; no further run is authorized by this Anchor update.
