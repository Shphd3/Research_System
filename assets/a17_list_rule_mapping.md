# A17 list rules and conditional mapping: source guide

[中文](a17_list_rule_mapping_cn.md) · [Root asset registry](catalog.json)

Read the complete Anchor, R02 contract/results and dataset guide in this repository’s [synchronized reading package](../sync/anchors/from-attention-to-search/17_04/README.md). Access to the independent project is not required for these copies; the package manifest records source and reading hashes.


The observed sequence—learn the old rules, lose them after new-only training, and retain both under mixed supervision—is **A17_04 → E01 → R02_single_layer_adamw**. This guide is self-contained for readers with only the Research_System repository. The [formal Anchor](../sync/anchors/from-attention-to-search/17_04/documents/Projects/from-attention-to-search/main/problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/17_04_conditional_mapping_transfer_anchor.md) owns the design and scientific boundary; the [R02 Summary](../sync/anchors/from-attention-to-search/17_04/documents/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R02_single_layer_adamw/summary.md) owns the results.

## Actual task

Each input has a visible mode, command 甲 or 乙, and a three-word list. Mode one maps 甲 to FIRST and 乙 to LAST. In the reversed new world, mode two swaps the mappings. The consistent control preserves them. Four real prefixes from `list_id=0-1-10` are:

| Input prefix; the answer starts after the final colon | Target |
|---|---|
| `模式：一。口令：甲。列表：红 黄 猫。答案：` | 红 |
| `模式：一。口令：乙。列表：红 黄 猫。答案：` | 猫 |
| `模式：二。口令：甲。列表：红 黄 猫。答案：` | 猫 |
| `模式：二。口令：乙。列表：红 黄 猫。答案：` | 红 |

Qwen3-0.6B Base updates only the final attention layer's q/k/v/o matrices: 6,291,456 trainable parameters. R01 did not acquire a qualified old mapping. R02 starts from E03's qualified old endpoint, with 100% old DEV accuracy; the earlier R01 result remains separate.

## R02 observations

Accuracy combines the two DEV panels equally. Triples below correspond to continuation-order seeds 29 / 43 / 71, all sharing one trained old endpoint.

| Continuation | Old accuracy | New accuracy |
|---|---|---|
| Old starting point | 100% / 100% / 100% | Before continuation |
| Consistent new only | 100% / 100% / 100% | 100% / 100% / 100% |
| Reversed new only | **0% / 0% / 0%** | **100% / 100% / 97.75%** |
| Old + reversed new | **100% / 99.75% / 99.75%** | **100% / 99.75% / 99.25%** |

For the displayed list, seed 29 predicts old-command 甲 as 红 → 猫 → 红 and old-command 乙 as 猫 → 红 → 猫, at the old endpoint, reversed-only endpoint and joint endpoint. This example was selected after inspection for explanation; the table supplies the aggregate evidence.

These are exposed-DEV diagnostics. R02 read no TEST, and three continuation orders are not three independent old-model acquisitions. Joint training receives old labels: at the same total 24,000 answer targets, it uses 12,000 old plus 12,000 new, while new-only uses 24,000 new. Joint success witnesses that shared parameters can express both visible mappings. It does not estimate equal-new-exposure rehearsal benefit or the value of separate parameters or experts. Researcher mechanism judgment and closure remain Unknown.

## Five data IDs, four physical releases

The IDs identify a predecessor and derived views, not five independent datasets or a simple upgrade chain. Counts, hashes, generation and split relationships are in the project's [formal dataset guide](../sync/anchors/from-attention-to-search/17_04/documents/Projects/from-attention-to-search/main/datasets/A17_04_list_rule_mapping/README.md) and [inventory.json](../sync/anchors/from-attention-to-search/17_04/sources/Projects/from-attention-to-search/main/datasets/A17_04_list_rule_mapping/inventory.json).

| Asset ID | Relationship and use | Execution-side parent directory |
|---|---|---|
| `data_a17_list_rules_v1` | A17_01 FIRST/LAST predecessor; TRAIN/DEV/TEST 4000/800/800 | `/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/data/list_rules_v1` |
| `data_a17_conditional_mapping_v1` | A17_04 three-world release; each world has TRAIN2400/DEV800/TEST800; **R02 uses its TRAIN/DEV** | `/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/data/conditional_mapping_v1` |
| `data_a17_mapping_acquisition_diagnostic_v1` | Neutral/explicit/normalized presentations derived from the parent old-mode TRAIN/DEV for acquisition diagnosis | `/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/data/acquisition_v1` |
| `data_a17_shared_routed_joint_v1` + `data_a17_shared_routed_mode_partition_v1` | Same later budget-comparison records: joint TRAIN4800/DEV1600, or TRAIN2400/DEV800 per mode | `/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/data/mapping_view_v1` |

The last two IDs share one directory and manifest: joint versus mode-partitioned views. They are not additional R02 training samples. Raw JSONL, model states and full per-example outputs remain execution-side and **are not included in this GitHub guide**. Absolute local paths describe storage locations. Remote readers can inspect the [dataset guide](../sync/anchors/from-attention-to-search/17_04/documents/Projects/from-attention-to-search/main/datasets/A17_04_list_rule_mapping/README.md), [inventory](../sync/anchors/from-attention-to-search/17_04/sources/Projects/from-attention-to-search/main/datasets/A17_04_list_rule_mapping/inventory.json) and [root registry](catalog.json) to resolve identity.

The formal owner directory is `main/problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/`. R02 lives at `main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R02_single_layer_adamw/`. Read [question and boundary](../sync/anchors/from-attention-to-search/17_04/documents/Projects/from-attention-to-search/main/problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/17_04_conditional_mapping_transfer_anchor.md) → [R02 facts and controls](../sync/anchors/from-attention-to-search/17_04/documents/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R02_single_layer_adamw/summary.md) → [dataset versions](../sync/anchors/from-attention-to-search/17_04/documents/Projects/from-attention-to-search/main/datasets/A17_04_list_rule_mapping/README.md). This source guide creates no parallel Anchor or scientific-state change.

Original project: [from-attention-to-search / Xingyu](https://github.com/BinaryCheater/from-attention-to-search/tree/Xingyu). Synchronized copies carry source paths and hashes; scientific edits return to that project.


### R06 step120 parameter × Adam-state exchange (2026-10-26)

[Summary](../Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R06_functional_protection_20261025/adam_swap_20261026/summary.md) · [all-seed/all-batch appendix](../Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R06_functional_protection_20261025/adam_swap_20261026/appendix_cn.md). Completed36independent temporary ordinary updates and10320sequence forwards. At fixed F parameters, U instead of F moments improves old CE change9/9contexts, with new-task tradeoffs and parameter interactions. No F filtering, full continuation or TEST. Not a long-term historical causal decomposition. Asset:`analysis_a17_r06_adam_swap_20261026`; durable output-access receipt in the delivery's `reproduce/output_access.json`.
