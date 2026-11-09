# A10: Optimizer and learning-rate mechanisms

[中文](README_cn.md) · [Roadmap](../../roadmap.md) · [All Anchors](../README.md)

Common gradients, singular concentration and SGD stability.

This page registers existing designs without changing their scientific state, conclusions or next decisions. The line retains its registered_flat layout; reading dependencies do not create structural parenthood.

A10_03 adds a proposed numerical-gradient/update audit; natural replay is NOT RUN. A10_01/A10_02 retain their original questions, states and next decisions.

| Identity | Question as named by source | Formal design | Experiment records |
|---|---|---|---|
| A10_01 | 10_01 Common-Projected SGD Learning-Rate Anchor | [Source](10_01_common_projected_sgd_lr_anchor.md) · [Chinese companion](10_01_common_projected_sgd_lr_anchor_cn.md) | [Records](../../experiments/A10/A10_01_common_projected_sgd_lr_synthetic) |
| A10_02 | 10_02 Frequency-Singular SGD Instability Anchor | [Source](10_02_frequency_singular_sgd_instability_anchor.md) · [Chinese companion](10_02_frequency_singular_sgd_instability_anchor_cn.md) | [Records](../../experiments/A10/A10_02_frequency_singular_sgd_instability) |
| A10_03 | Does Router numerical error change a finite learning update? (proposal) | [Source](10_03_router_numerical_update_fidelity_anchor.md) · [Chinese companion](10_03_router_numerical_update_fidelity_anchor_cn.md) | [Source/calibration audit](../../research_notes/router_numerical_fidelity/20261024_scope_audit.md); natural replay NOT RUN |

[Complete ownership registry](../../anchor_ownership.json) · [Organization provenance](../../organization_migrations/20261022/README.md)
