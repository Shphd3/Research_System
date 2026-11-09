# Frequency-contribution bridge and relation refinement: v0.1 intake

[中文](README_cn.md)

Received as a draft on2026-10-19, then explicitly approved for no-training A–C analysis. **Analysis is complete with recorded insufficiencies.** Start with [Summary](summary.md), [Chinese one-page](one_page_cn.md) or [Detailed](detailed.md). [Authorization](execution_authorization_20261019.json) freezes scope and settings; the original draft, old results and Focus remain intact. H3 learning remains NOT RUN.

The long-term aim is to learn and retain more content within matched parameter and compute budgets. This round first asks whether frequency and final-layer feature contributions provide a reproducible basis for input allocation beyond token identity. Learning benefit remains a subsequent hypothesis.

- H1: low-frequency feature contribution share is positively associated with the rarity of the current token ID; examine within-ID context variation separately.
- H2: within a frequency band, relation-based subgroups retain more coactivation in review conversations and greater actual input-composition consistency than matched random subgroups.
- H3: the organization improves held-out learning and retention at matched budgets. H3 is outside the current analysis stage.

The proposed progression is input profiles → token-frequency/context checks → within-band relation versus matched-random refinement → actual dispatch. The dispatch comparison crosses raw contribution versus normal-level calibration with relation versus random subgroups. Learning requires a separate frozen training protocol and authorization.

Feature frequency is the TRAIN fraction with shared activation positive. The contribution proxy is activation times the final-layer decoder norm, not the sum of 14 decoder norms. The shared activation still comes from joint 14-layer encoding. Band scores sum contributions without dividing by membership count. Calibration changes only the first band-selection step.

Four log-spaced bands, eight total receiving slots, two subgroups per band and average-linkage were accepted for this bounded analysis through the subsequent explicit authorization. Existing EVAL has already been inspected; subsequent reuse is exploratory. Input consistency and reception do not establish learning utility.

- [Extracted Anchor draft](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_22_frequency_contribution_relation_refinement/15_22_frequency_contribution_relation_refinement_anchor.md) / [Chinese](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_22_frequency_contribution_relation_refinement/15_22_frequency_contribution_relation_refinement_anchor_cn.md).
- [Protocol translation](protocol.md) / [received Chinese original](protocol_cn.md).
- [Unmodified combined report and Anchor source](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_22_frequency_contribution_relation_refinement/sources/feishu_report_anchor_v0.1_cn.md).
- [Intake, hashes and extraction record](intake_record.json).
- Prior results: [DCLM](../../15_21_activation_to_expert_learning/20261019_normalized_learning/summary.md), [Tulu SFT](../../15_21_activation_to_expert_learning/20261019_tulu_sft/summary.md), [paired TRAIN frequency plots](../../15_21_activation_to_expert_learning/20261019_tulu_sft/paired_train_frequency_20261019/README.md).
- [Full prior-result access after ZIP cleanup](../../15_21_activation_to_expert_learning/20261019_normalized_learning/full_results_access.md).

Prior evidence is not a measurement of the new H1/H2. The new measurements are inSummary/Detailed; work stops afterA–C, without learning.

## Three insights: concise redraw

[Four figures and interpretation](redraw_three_insights_20261019/README.md): member counts versus final-layer contribution, held-out phi, separate membership stability, and old T_S1 epoch1 regional NLL only. Includes PNG/SVG/PDF and source CSV files; no new experiment.
