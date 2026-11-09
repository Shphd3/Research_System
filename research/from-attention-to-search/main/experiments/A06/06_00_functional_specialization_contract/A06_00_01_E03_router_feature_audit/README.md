# A06_00_01_E03 Router Feature Specialization Audit

This folder groups early router feature-specialization diagnostics under
`../../../../problem_anchors/06_geometry_proxy_preservation/06_00_functional_specialization_contract/06_00_functional_specialization_contract_anchor.md`.

## Sub-Experiments

| ID | Purpose | Status |
|---|---|---|
| `A06_00_01_E03_01_seq2_ab_feature_specialization/` | 最小 `seq_len=2` A/B/AB setup，判断 routing 是否形成干净 feature bucket | completed |
| `A06_00_01_E03_02_seq32_contiguous_ab/` | `seq_len=32` 连续 `[A,B]` setup，判断 source-token routing purity | completed |
| `A06_00_01_E03_03_router_factor_audit_seq32/` | `seq_len=32` router factor audit，拆 token id、position、left context、rule/function、target shortcut | completed |
| `A06_00_01_E03_04_svd_feature_mixing_seq32/` | 已训练 `seq_len=32` MoE 的 AB-dominant expert SVD 和 mask ablation | completed |
| `A06_00_01_E03_05_cb_context_b_routing_seq32/` | 加入等频 `CB`，比较 B source token 在 `B-only / AB / CB` context 下的 routing | completed |
| `A06_00_01_E03_06_trainable_router_a_reproduction/` | soft-mixture trainable-router correction | completed |
| `A06_00_01_E03_07_top1_sparse_router_failure_mode/` | selected-gate top-1 sparse router failure-mode diagnosis | completed |
| `A06_00_01_E03_08_router_initialization_trajectory/` | random init vs semantic/context prototype init trajectory | completed |
| `A06_00_01_E03_09_hidden_geometry_audit/` | hidden geometry audit for shortcut explanations | completed |
| `A06_00_01_E03_10_route_swap_and_frozen_semantic_router/` | route swap and frozen semantic-router diagnostic | completed |
| `A06_00_01_E03_11_router_prior_decay_audit/` | final-checkpoint audit of semantic prior decay | completed |
| `A06_00_01_E03_12_semantic_router_refresh_continuation/` | semantic-router refresh continuation | completed |

## Current Combined Judgment

Ordinary no-load-balance top-1 MoE learns the synthetic tasks, but its expert
buckets are not clean feature-level buckets. H0521a shows mixed assignment in
the minimal setup; H0521b shows source-token buckets are not clean in the
longer context setup; H0522 SVD shows the prediction-position AB-dominant
expert is not a stable clean AB specialist; H0522 factor audit shows
position/token-id/target shortcuts explain router behavior better than a stable
rule/function bucket. H0522b shows B source-token routing keeps a strong B
identity anchor after adding equally frequent CB, with context modulation only
seed-dependent.

## Current Boundary

This grouped diagnostic family is closed. Its historical follow-up was a pure
expert forced-utility audit; that question has since been absorbed into the
completed functional-specialization and utility-binding parents. It is not a
current project decision. Use the A06 registry for the current next step:

[`A06 experiment registry`](../../README.md).
