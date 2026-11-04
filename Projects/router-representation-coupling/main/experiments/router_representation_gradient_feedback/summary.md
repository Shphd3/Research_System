# Summary: Router-to-representation gradient feedback

> **Storage update, 2026-10-30:** At the researcher's request, all 24 binary weight, training-state and RNG files from the two A3 formal arms were deleted (20.393929 GiB). Code, configs, logs, manifests, historical results and common initial-state inputs are retained. These trained arms are no longer available for evaluation or continuation; future work focuses on new MoE training. Historical completion and NOT RUN findings are unchanged. [Deletion receipt](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/storage_cleanup_receipts/20261030T154131Z/completion.json).


**Both arms completed 7629 updates / 1,999,896,576 valid targets, platform SUCCEEDED, supervisor exit 0, with complete endpoint artifacts. A has lower final 64-update training CE by 0.014371 nat/target; B has lower balancing cost. Training comparison is complete; independent TEST and functional analyses remain NOT_RUN.**

[Anchor](../../problem_anchors/router_representation_gradient_feedback/anchor.md), [Protocol A3](protocol.md), [analysis Protocol](analysis_protocol.md), [Detailed](detailed.md). Snapshot 2026-10-07T01:33:37.835761+00:00.

## 1. Purpose

Test whether direct LM gate feedback into shared representations helps finite-budget prediction and useful expert allocation or produces harmful competition. Current arms share balancing; preserve the separate failed zero-aux history.

## 2. Hypothesis

Feedback can help or harm prediction/function. More uniform load is not utility. Expert exposure, gradient scale/Adam and hardware numerical paths remain rivals. Lower training CE does not establish better representations or semantic specialization. Researcher mechanism/adoption/closure judgment remains Unknown.

## 3. Analysis method

Define the activations first. \(r\) is attention output before residual addition; \(h\) is the post-residual, normalized expert input. Router matrix W maps r to scores and weights for eight experts, selecting two. The always-active shared expert and selected experts compute from full h.

Both arms share the 342,097,408-parameter model, saved random initialization, seed 1005, DCLM data order, AdamW and 262144 valid targets per update. A allows LM-loss gradients through router scores to return to r. At the same parameter state and input, B reads numerically identical r with that return path blocked (`stop_gradient(r)`). Router weights, experts and other backbone paths continue learning. The optimizer updates parameters, not activation r directly: an activation gradient affects upstream parameter gradients, and their update may change the next forward representation.

Both optimize CE plus 0.01 times sequence-local balancing averaged over 12 layers. Both auxiliary paths read detached r but retain router-weight gradients, so only the LM feedback edge differs. A uses 4 H100 GPUs and B 8 RTX 5090 GPUs; algorithm and hardware are completely confounded.

Verify completion and endpoint artifacts, then align 7629 training records by cumulative valid targets. Preserve raw values and the same 64-update moving mean. Trailing 32/64/128/256 windows are post-hoc descriptions, not independent replications or significance tests. The registered 0.01 TEST criterion is not applied to training CE.

## 4. Conclusion

The losses below come from training batches evaluated before each parameter update. The last 64 updates cover 16,777,216 valid targets; this is not endpoint-checkpoint loss on sealed TEST documents. SUCCEEDED records platform completion; NOT_RUN means an assessment has not occurred, not zero effect. Training fit and generalization require separate answers.

A pt-txeitsor completed 2026-10-06T21:47:33Z; B pt-3u6bcqbq completed 13:10:33Z. Both 100%; no recorded health guard failures, latest fixed-layer load streak 0 and no globally unused experts at endpoint. [Completion and comparison](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261007T013337Z/comparison.json).

| Final64-update mean | A: live LM gate feedback | B: detached LM gate input | B−A |
| --- | --- | --- | --- |
| LM CE, nat/valid target | 4.109270 | 4.123641 | +0.014371 |
| Weighted balancing | 0.013589 | 0.012073 | −0.001516 |
| Total training objective | 4.122859 | 4.135714 | +0.012855 |

Window steps 7566–7629 covers 16,777,216 valid targets. Trailing 32/128/256 CE differences +.014477 / +.014643 / +.014735 agree in the current tail. Difference at ~1B is +.011823, at ~2B +.014371: this observed training gap did not disappear in the latter half, but this is not seed robustness. [Milestone descriptions](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261007T013337Z/milestone_training_description.json).

[Full plot](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261007T013337Z/loss_comparison.png), [7629 paired records](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261007T013337Z/aligned_updates.csv), [provenance/inspection](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261007T013337Z/figure_provenance.json). Positive B−A means lower A training CE. Lower B aux measures balancing, not useful division of labor.

Bounded analysis: in this paired trajectory, A fits training data slightly better while B distributes load more uniformly. Task-aligned adaptation is a candidate explanation, not established mechanism; exposure/optimization/hardware remain live rivals. Primary TEST/function/gradient/geometry analyses are NOT_RUN. Researcher judgment Unknown. AI suggestion: evaluate both endpoints on the registered independent document panel; retained advantage supports bounded generalization, disappearance/reversal weakens it, wide interval is insufficient. Functional intervention and hardware control are further requirements for causal mechanism claims. No new training/GPU analysis launched; both supervisors ended normally.
