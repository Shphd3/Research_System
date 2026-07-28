# Protocol For Approval: A05_04_02 No-Attention-Residual B-Routing Audit

Primary anchor: `main/problem_anchors/05_failure_mechanism/05_04_02_dotproduct_common_logit_causality_anchor.md`

Goal: test whether the direct residual path from the routed `B_CONST` token into the MoE/router input is sufficient to drive common-logit dominance and route collapse.

Decision question: If the attention-block residual into the router input is removed during training, does the original `SLOT_s B_CONST Y_s` task form slot-to-expert specialization?

Tested hypothesis: the direct `B_CONST` residual identity in `h_B = LN(x_B + attention_output_B)` is a major common source. Removing `x_B` from this path should reduce common-logit dominance and improve route-slot NMI.

Rival explanation: collapse persists because common dominance is produced by attention output, LayerNorm geometry, top-1 feedback, shared target loss, or another routed-position common stream rather than direct residual identity.

Data:
- Use the original Round-1 data: `prefix filler + SLOT_s B_CONST Y_s + suffix filler`.
- Keep `SLOT_s B_CONST Y_s` contiguous.
- Disable positional encoding as in Round 1.
- Loss and routing metrics are computed at the `B_CONST` position.

Model:
- Same tiny no-position dot-product sparse top-1 MoE as Round 1 / Round 2.
- Router is dot-product only: `score_e(h) = w_e^T h`.
- Sparse top-1 routing only.
- No soft routing, no top-k with `k > 1`, no probability-weighted expert mixtures beyond the existing selected-gate scalar used by the Round-1 model.

Intervention:
- Replace the first transformer block residual into the MoE/router input:

  `standard: h = LN(x + attention_output)`

  `no-attention-residual: h = LN(attention_output)`

- Keep the post-MoE residual `LN(h + MoE(h))` unchanged to avoid confounding router-input residual removal with output-head learning failure.

Conditions:
- `NoAttnResidual_B_baseline`: random initialization, no common cancellation, original B-position task.
- Seeds: `20260521` to `20260528`.
- Checkpoints: `0, 1, 2, 5, 10, 20, 50, 1600`.

Primary metric: final route-slot NMI, because it measures slot-level specialization rather than load balance.

Secondary metrics: per-slot route purity, max load, active experts, target accuracy, component variance ratios, dot-product margin decomposition, route heatmap.

Expected interpretation:
- If final NMI rises substantially while accuracy remains high, the direct attention residual path is a causal contributor to collapse.
- If collapse persists, the common source is not only direct `B_CONST` residual identity.
- If accuracy fails, the intervention is too destructive to interpret as a clean routing result.

Cannot claim:
- This does not remove every residual connection.
- This does not identify the full common source.
- This does not prove real-language-model transfer.
- This does not prove expert computation is causally slot-specialized.
