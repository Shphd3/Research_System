# Protocol For Approval: A05_04_02 Common Source B-Path And No-B Audit

Primary anchor: `main/problem_anchors/05_failure_mechanism/05_04_02_dotproduct_common_logit_causality_anchor.md`

Goal: determine whether the Round-2 common component mainly comes from the `B_CONST` token path into the routed hidden state.

Decision question: If the B token path is removed or the B token is deleted from the task, does route-slot NMI improve and does common-logit dominance fall?

Tested hypothesis: the common component is partly caused by B token identity entering `h_B` through residual and attention paths, then being amplified by sparse top-1 feedback.

Rival explanation: common dominance is not B-specific; it comes from routed-position role, LayerNorm/mean-stream geometry, shared target objective, or top-1 feedback.

Data:
- P1 uses the original Round-1 `prefix filler + SLOT_s B_CONST Y_s + suffix filler` data and existing Round-1 dot-product baseline checkpoints.
- P2 uses `prefix filler + SLOT_s Y_s + suffix filler`, with loss and routing metrics at the slot position.

Model: same tiny no-position dot-product sparse top-1 MoE as Round 1 / Round 2.

Routing / algorithm:
- P1 counterfactual patching conditions: original, no B residual, no B self-value attention contribution, no full B embedding path.
- P2 training conditions: no-B baseline, no-B common-cancel 0-10, no-B common-cancel 0-final.

Loss / objective: original P1 is diagnostic only; P2 predicts `Y_s` at the `SLOT_s` position.

Conditions: 8 seeds; checkpoints `0,1,2,5,10,20,50,1600`; full no-B training uses 1600 steps.

Primary metric: final route-slot NMI, because it measures slot-level specialization rather than load balance.

Secondary metrics: mean absolute common margin, mean absolute slot margin, max load, active experts, accuracy, attention self-mass, common hidden norm, route heatmaps.

Known good case: common cancellation should improve NMI in the original Round-2 setting.

Known bad case: original random-init dot-product baseline should collapse.

Known confusing case: removing B may reduce common margin but still not create slot-specialized routing.

Success: B-path ablation or no-B data increases slot NMI while preserving accuracy and reducing common margin.

Failure: common margin and collapse persist after removing B paths.

Insufficient evidence: NMI improves only by load balancing, accuracy drops, or patching changes hidden states in a way that cannot be compared to the original router.

Cannot claim: this does not identify the full common source, prove real-language transfer, or prove expert computation is causally slot-specialized.
