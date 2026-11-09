# Sanity Check: A06_01_01_E02 Cross-Checkpoint Replay

Source drafts:

- `daily_research_reports/0614/draft/06_02_Early-Training Common-Logit Amplification in Real Top-1 MoE.md`
- `daily_research_reports/0614/draft/A06_01_01_E02_cross_checkpoint_common_replay_protocol.md`

Formalized files:

- Anchor: `Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`
- Protocol: `Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_01_E02_cross_checkpoint_common_replay/protocol.md`

## Conclusion

The protocol is scientifically well-targeted, but it should not be launched as one large replay-plus-freeze grid yet. The safe formal path is:

```text
Phase A/B first: normal 300-step trajectory + cross-checkpoint replay.
Phase C includes required final-layer-only freeze_hidden_producer.
Broader freeze variants are selected after replay attribution is known.
```

The final-layer-only decision makes `freeze_hidden_producer` implementable without turning the whole model into a different experiment. Its claim boundary is final-layer-only.

## What Passed

1. The decision question matches the current claim boundary: the previous run established common load bias and step-10 amplification, but not the causal source.
2. Cross-checkpoint replay is the right first diagnostic because \(W_aH_b\) separates gate-weight movement from hidden-state movement without changing training.
3. The protocol keeps the critical previous-run constraints: exact gate input, no shared expert, top-1 routing, no load-balance loss, non-oracle hidden-state gating.
4. Using `common_margin` as the primary replay scalar is correct because `dominance_ratio` can explode when residual margin is small.
5. Centered replay conditions remain necessary to test whether the step-10 spike is still mediated by the mean common channel.

## Blocking Issues Before Formal Run

1. Hidden-state storage is too large if implemented naively.

   With 8192 sequences, 256 positions, hidden size 512, 6 layers, 11 checkpoints, and 3 seeds, saving all full `H_t` tensors costs roughly:

   ```text
   bf16/fp16: about 425 GB for H only
   fp32: about 850 GB for H only
   ```

   This excludes logits, residuals, route ids, optimizer state, figures, and CSVs. Final decision: do not store all full `H_t` tensors. The formal runner should stream or recompute `H_b` and immediately evaluate all needed `W_aH_b` metrics, while storing only aggregated metrics and small debug shards.

2. `freeze_hidden_producer` is final-layer-only.

   Freezing the producer of each layer's gate input is layer-dependent. Final decision: do not attempt an all-layer hidden-producer freeze. For the last layer only, freeze all modules that can change the final layer's gate input before the MoE gate: token embeddings, layers before the final layer, and the final layer's pre-gate attention / layernorm path. Keep the final layer gate and expert path trainable. Final norm / LM head may remain trainable because they do not change the final layer gate input. Record the exact frozen/trainable module list.

3. `freeze_experts` does not fully remove expert-output feedback.

   Freezing expert MLP weights tests whether expert parameter updates are necessary. It does not remove the effect of routing tokens through fixed expert outputs. A stronger `block_expert_output_feedback` diagnostic changes the LM computation and should not be interpreted as a deployable method.

4. Cross-batch stability is hypothesized but not fully tested by one fixed audit batch.

   The fixed audit batch is necessary for checkpoint replay, but P1 also claims common-direction stability. Add a small secondary audit batch or explicitly narrow the claim to within-batch checkpoint stability.

5. Attribution thresholds need approval before the run.

   The draft says "most amplification" and "strongly suppresses" but does not define thresholds. Recommended defaults:

   ```text
   path dominant: fraction >= 0.60 of common_margin amplification
   path minority: fraction <= 0.30
   freeze suppression: >= 50% reduction in step-10 common_margin increase and raw_max_load increase
   interaction dominant: F_gate <= 0.40 and F_hidden <= 0.40 while actual amplification is large
   ```

   These thresholds should be marked as decision rules before formal execution.

6. Gradient norms must be captured during training.

   Router and expert gradient norms cannot be recovered from checkpoint-only replay. If they remain protocol deliverables, the training loop must log them after backward and before optimizer step at the audited checkpoints or at every step.

7. Reconstruction tolerance must account for precision.

   The ideal check is `max_abs(H_t W_t^T - logged_router_logits) <= 1e-6` in fp32. If the formal runner uses bf16/fp16 capture, record dtype and use both max error and relative error. Do not relax the check without logging the reason.

8. Full pairwise replay can be larger than needed.

   A full 11 x 11 checkpoint grid is useful for heatmaps, but the decision mostly needs:

   ```text
   W0_H0, W10_H10, W10_H0, W0_H10,
   W300_H300, W300_H0, W0_H300,
   centered versions for H0/H10/H300
   ```

   If runtime is tight, run the decision subset first and generate the full heatmap only after the subset passes.

## Recommended Protocol Tightening

1. Make Phase A/B the primary approved formal run and include final-layer-only `freeze_hidden_producer` as the required freeze validation.
2. Add a one-batch preflight check before the 4-GPU full run:

   ```text
   1 seed, 1 layer, checkpoints 0 and 1, 1 small audit batch
   checks: exact gate reconstruction, W_aH_b replay, centered replay, output schema
   ```

3. Add a secondary small audit batch only for common-direction stability metrics, not for primary replay.
4. Define dominance and suppression thresholds before submitting.
5. Keep broader Phase C freeze variants in the protocol, but select `freeze_gate`, `freeze_experts`, or feedback blocking after Phase B attribution.

## Actual Execution Problems To Resolve

| Issue | Risk | Required Resolution |
|---|---|---|
| Full `H_t` storage | Disk blow-up and slow sync | Stream/recompute or shard only debug tensors |
| `freeze_hidden_producer` ambiguity | Causal claim becomes unclear | Use final-layer-only freeze and record exact frozen/trainable module list |
| Expert feedback intervention | May test a different LM | Separate `freeze_experts` from `block_expert_output_feedback` |
| No replay thresholds | Result can be argued post hoc | Approve numeric decision thresholds |
| One fixed audit batch | Cannot prove batch-stable common direction | Add small secondary audit batch or narrow claim |
| Gradient norms | Not recoverable after training | Log during backward at checkpoint steps |
| Precision tolerance | False reconstruction failures or false passes | Log dtype plus max and relative error |
| Phase B/C disagreement | Ambiguous interpretation | Require implementation sanity table before claim update |

## Mainline Impact Gate

```text
affects hypothesis: yes
affects claim boundary: yes
affects next decision: yes
recommendation: pursue, but staged as Phase A/B before freeze split
```

## Approval Recommendation

Approve Phase A/B plus final-layer-only `freeze_hidden_producer`. Do not approve broader freeze variants as part of the same formal run until:

1. the replay runner passes the preflight reconstruction test;
2. storage policy is fixed;
3. attribution thresholds are accepted;
4. Phase B indicates which broader causal path needs freeze validation.

## Final-Layer Freeze Claim Boundary

The final-layer freeze can answer:

```text
When the final layer's router-input distribution is fixed by freezing its producer,
can the final layer gate/expert path still amplify common logits by step 10?
```

It cannot answer:

```text
Whether hidden-producer drift is necessary for all layers.
Whether earlier-layer expert feedback reshapes later router inputs.
Whether a full-model hidden freeze would behave the same way.
```

## Final Audit Before Formal Run

These are the remaining points that could damage the conclusion if implemented incorrectly:

1. Exact gate input must be audited, not `output_hidden_states`.

   Required guard:

   ```text
   max_abs(H_t W_t^T - logged_router_logits) and relative error are logged per layer/checkpoint/seed.
   ```

2. Freeze variants must start from the same initialization/data order as the normal run.

   Required guard:

   ```text
   same model seed, data order, optimizer config, checkpoint schedule, and audit batch.
   ```

   Otherwise a freeze run can differ for random reasons rather than causal intervention.

3. Final-layer hidden-producer freeze has a final-layer-only conclusion.

   Required guard:

   ```text
   report final-layer metrics separately; do not average final-layer freeze evidence into all-layer causal claims.
   ```

4. Streaming replay must be deterministic.

   Required guard:

   ```text
   model.eval() during audit/replay, dropout disabled, no training-state mutation during replay.
   ```

5. Distributed aggregation must avoid double-counting tokens.

   Required guard:

   ```text
   each rank audits disjoint sample indices, then all-reduce counts/sums once.
   ```

6. `dominance_ratio` must not be the only decision scalar.

   Required guard:

   ```text
   primary replay attribution uses common_margin; dominance_ratio is reported with epsilon/log form only as secondary evidence.
   ```

7. Gradient norms must be logged before optimizer zeroing.

   Required guard:

   ```text
   router/expert gradient norms are captured after backward and before optimizer.step()/zero_grad().
   ```

8. The DCLM packed-token contract must remain unchanged.

   Required guard:

   ```text
   span_length=257, input_token_count=256, target_token_count=256, no padding drop, fixed audit indices.
   ```

If all eight guards pass in preflight, the protocol is ready for the formal four-GPU Phase A/B plus final-layer hidden-producer freeze run.
