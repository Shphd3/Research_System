# Thinking Card: Incremental-Information Routing Under Differentiable Load Balance

Status: researcher-confirmed design translated from the 2026-08-10 approval

Parent research direction or problem:
A16 asks how a sparse MoE can preserve usable expert load without sacrificing language-model learning. This card adds a long-run Router intervention under verified differentiable load balance; it does not reopen the completed A16_00 gradient audit.

Phenomenon:
The Router normally receives the complete post-attention normalized state. The attention-induced change that became visible at the current layer is therefore mixed with the pre-existing state and may be hard for a finite-capacity Gate to exploit explicitly.

Mechanism guess:
Preserving the native full-state Gate while adding a zero-initialized low-rank branch over the actual same-layer increment may expose newly written information without deleting existing context. A trainable projection is the most direct engineering realization. A frozen direction that first passes representation and expert-utility admission is the scientific realization.

Strongest rival explanation:
Any improvement could come from extra low-rank parameters, regularization, or optimization geometry rather than from the identity of a certified incremental-information direction. A dimension-matched Haar branch is therefore required.

Most uncertain point:
Whether either incremental branch improves 30B held-out next-token NLL under a truly differentiable Switch-style load objective, and whether a certified branch outperforms its Haar control.

Evidence that would change my mind:
Two seed-matched 30B runs in which the engineering branch consistently beats Native-LB, or an eligible certified branch consistently beats both Native-LB and Haar-LB. Opposite seed directions, a missing admission certificate, or invalid LB backward prevents the corresponding conclusion.

Current blocking uncertainty:
The implementation has not yet been built or smoked. The certified direction also does not exist until the registered E1 representation gate and E2 expert-utility gate pass at a 2B, 5B, or 10B Native checkpoint.

Why this decision is needed now:
Fixed covariance bands did not receive a functional certificate. The next operational question is whether an explicitly represented same-layer increment is useful when its direction is either learned end-to-end or independently certified.

Current next decision:
Implement and smoke the four registered conditions with differentiable LB, then submit all eight jobs from step 0. Certified-Innovation-LB and Haar-Innovation-LB remain exact dormant Native behavior until the first common eligible 2B/5B/10B checkpoint. If no common certificate exists by 10B, both remain dormant through 30B and the scientific identity comparison is insufficient rather than fabricated.

Known source material:
- [Layerwise incremental-information routing method](/daily_research_reports/0810/docs/layerwise_incremental_information_routing/README.md)
- [A15_07 conditional-fine direction design](../../15_spectral_representation_and_functional_routing/15_07_layerwise_conditional_fine_discriminant_directions/15_07_layerwise_conditional_fine_discriminant_directions_anchor.md)
- [Verified differentiable-LB 30B execution contract](/Projects/from-attention-to-search/main/experiments/A15/15_06_online_spectral_routing_and_relay/A15_06_E05_30b_differentiable_lb_restart/protocol.md)
