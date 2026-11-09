# Sanity Check: Real-Text Random-Init MoE Common-Logit Audit

Source drafts:

- `daily_research_reports/0611/draft/06_minimal_anchor_handwrite.md`
- `daily_research_reports/0611/draft/06_protocol_1.md`

Primary anchor lineage:

- `Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_04_02_dotproduct_common_logit_causality_anchor.md`

## Conclusion

Do not start the full experiment until the implementation patch and one-batch
smoke audit pass. The user has resolved the main design ambiguities: the main
run must disable the shared expert, use the exact linear-gate input as `h_i`,
use non-oracle hidden-state gating, force top-1 routing with no load-balance
loss, use a dedicated small config, and record DCLM samples as 257-token spans
with 256-token inputs.

## What Passed

- The DCLM binary data path exists and contains `.bin` shards.
- The protocol tests the right object: `w_e^T c` logit margin, not only
  `||c||`.
- The conclusion boundary is mostly correct: Phase 1 and Phase 2 can support
  initialization geometry, but not actual training dynamics.
- A reusable preflight script has been placed in this experiment folder.

## Resolved Decisions And Required Fixes

1. Shared expert mismatch:
   Main run disables shared expert. Patch source with an explicit
   `use_shared_expert=false` config/CLI path and log it.

2. Router-input object:
   `h_i` is the exact tensor passed into the active linear gate. Capture it
   inside the MoE block and verify `router_logits == h @ W.T`.

3. Default gating reference:
   Main run must be non-oracle, specifically `gating_reference=hidden_states`.

4. Top-k and load-balance defaults:
   Main run must explicitly set `--num_experts_per_tok 1 --lambda_lb 0.0`.

5. Small model config:
   Create a dedicated config. Do not reuse the existing 16-layer 4-head H512
   config except as a recorded fallback.

6. Data manifest stride:
   Manifest records `span_length=257`, `input_token_count=256`,
   `target_token_count=256`, and `sample_stride=257`.

7. Padding/non-padding rule:
   DCLM is a packed stream. All 256 input tokens are valid; do not drop token
   id 0 as padding.

8. Baseline 3 feasibility:
   Covariance-matched zero-mean Gaussian can be expensive if done naively at
   high token count and many layers. Keep it optional or define a streaming
   low-rank approximation before the full run.

9. Phase 3 checkpoint capture:
   `train_qwen3_moe.py` saves by interval/final checkpoint, while the protocol
   needs checkpoints `[0, 1, 10, 50, 100, 300]`. The runner must either add
   audit callbacks at those steps or run a custom short-training loop.

10. Source manifest git hash:
    Reading `/data/250010109/MoE_Router` git metadata currently fails under
    Git's safe-directory check. Use `git config --global --add safe.directory`
    before the formal run, or record file checksums as the source identity.

## Additional Issues Found After User Decisions

1. Top-1 output weighting:
   Current code multiplies the selected expert output by its softmax
   probability. For the main early-training audit, keep
   `norm_topk_prob=false` with `top_k=1`, because this probability is the
   differentiable path by which task loss reaches router logits. Setting
   `norm_topk_prob=true` would make the selected weight constant 1 and largely
   remove router task-loss gradients.

2. Real-vs-virtual router scale:
   Phase 2 samples virtual routers with `N(0, 1/d)`, while the real gate uses
   the model initializer. Record real gate weight standard deviation per layer
   and include a virtual-router scale matched to that value.

3. LayerNorm location:
   `output_hidden_states` is not sufficient evidence for `h_i`; the gate input
   is after `post_attention_layernorm` and any router preprocessing. Capture
   the actual gate input only.

4. Multihead exclusion:
   Main run must use `moe_type=moe`, not `multihead`, because multihead changes
   routing input dimension and expert-label shape.

5. Position aggregation:
   Primary metrics use all 256 input positions. Position buckets 0-63, 64-127,
   128-191, and 192-255 are required diagnostics. Per-position common vectors
   are optional diagnostics for separating global common bias from
   position-specific bias.

## Next Action

Implement the source patch, then run a tiny smoke audit: one batch, one layer,
one seed, and one virtual-router count. The smoke must verify the exact logit
decomposition before Phase 1/2 begins.
