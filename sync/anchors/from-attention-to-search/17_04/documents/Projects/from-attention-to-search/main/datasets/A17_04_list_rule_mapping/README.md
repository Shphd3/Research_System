派生阅读副本；原件位置：`Projects/from-attention-to-search/main/datasets/A17_04_list_rule_mapping/README.md`。
[精确原始文件](../../../../../../sources/Projects/from-attention-to-search/main/datasets/A17_04_list_rule_mapping/README.md)；研究修改仍回到原件。

---

# A17_04: first/last conditional list-rule data

[中文](README_cn.md) · [Verified file inventory](../../../../../../sources/Projects/from-attention-to-search/main/datasets/A17_04_list_rule_mapping/inventory.json) · [System-only reading entry](https://github.com/Shphd3/Research_System/blob/master/assets/a17_list_rule_mapping.md)

The remembered result belongs to **A17_04, E01, round R02**: after acquiring mode1, sequential reversed-mode training reduced old accuracy from100% to0%; joint old/new supervision learned both mappings at99.25–100%. The [Anchor](../../problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/17_04_conditional_mapping_transfer_anchor.md) owns the design and the [R02 Summary](../../experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R02_single_layer_adamw/summary.md) owns results. This guide organizes existing data; it changes no labels, splits or scientific state.

## A real example

All four rows use DEV list `0-1-10`. The model receives the prefix through `答案：` and predicts one answer token.

| World | Exact prefix | Target | Rule |
|---|---|---|---|
| old | 模式：一。口令：甲。列表：红 黄 猫。答案： | 红 | FIRST |
| old | 模式：一。口令：乙。列表：红 黄 猫。答案： | 猫 | LAST |
| reversed | 模式：二。口令：甲。列表：红 黄 猫。答案： | 猫 | LAST |
| reversed | 模式：二。口令：乙。列表：红 黄 猫。答案： | 红 | FIRST |

Mode and command are visible, so the two mappings are jointly satisfiable. A separate `consistent` condition keeps mode2 command甲=FIRST/乙=LAST. Its complete prefixes equal `reversed` prefixes but targets differ. These are alternative experimental worlds; select a world rather than train conflicting mode2 labels together.

The saved, post-hoc [illustrative predictions](../../../../../../UNAVAILABLE.md) show old command甲 predicting红 initially,猫 after reversed continuation, and红 after joint supervision. The example explains the result rather than supplying fresh confirmation.

## Existing releases and views

| Asset ID | Role and size | Existing directory |
|---|---|---|
| `data_a17_list_rules_v1` | A17_01 predecessor with explicit first/last instructions; TRAIN/DEV/TEST4000/800/800 | [list_rules_v1](../../../../../../UNAVAILABLE.md) |
| **`data_a17_conditional_mapping_v1`** | **Actual R02 data**: old,consistent,reversed worlds; total TRAIN/DEV/TEST7200/2400/2400, per world2400/800/800 | [conditional_mapping_v1](../../../../../../UNAVAILABLE.md) |
| `data_a17_mapping_acquisition_diagnostic_v1` | neutral/explicit/normalized old-mode views; each TRAIN2400/DEV800,tiny64,TRAIN-panel400; E03 acquired the old endpoint with neutral | [acquisition_v1](../../../../../../UNAVAILABLE.md) |
| `data_a17_shared_routed_joint_v1` and `data_a17_shared_routed_mode_partition_v1` | E04 joint old+reversed and equivalent mode partitions: joint4800/1600 TRAIN/DEV, each mode2400/800 | [mapping_view_v1](../../../../../../UNAVAILABLE.md) |

These five registered IDs describe four physical releases. E04 uses a different low-rank model configuration; its results cannot replace R02's full four-matrix results merely because data match.

## Mother release and split meaning

```text
/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/data/conditional_mapping_v1/
  manifest.json       generation seed, vocabulary, tokenizer, splits and hashes
  qualification.json  original generation qualification
  train.jsonl         7200 rows, 2400 per world
  dev.jsonl           2400 rows, 800 per world
  test.jsonl          2400 rows; not read in R02
```

Generation seed20261011. Answer vocabulary:红、黄、蓝、黑、绿、白、紫、灰、金、银、猫、狗、鸟、鱼、牛、马、羊、虎、龙、花. Each list contains three distinct words. Registered tokenizer answers have one token; loss supervises only that answer.

Each world has1200 ordered TRAIN lists with two command questions per list. Its800 DEV rows contain400 `order_new` rows (seen unordered group, unseen order) and400 `combination_new` rows (unseen unordered group, known vocabulary). Report each panel and their equal-weight mean. Old/new modes deliberately share underlying lists; visible mode changes the complete input. TRAIN/DEV are exposed. Mother TEST was used in R01; R02 did not read it and supplies no fresh confirmation set.

## Reuse the existing data

For R02 replay, load the mother release and filter TRAIN/DEV by `world`:

```python
import json
from pathlib import Path

root = Path('/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/data/conditional_mapping_v1')
with (root / 'train.jsonl').open() as stream:
    rows = [json.loads(line) for line in stream if line.strip()]
old = [row for row in rows if row['world'] == 'old']
new_reversed = [row for row in rows if row['world'] == 'reversed']
new_consistent = [row for row in rows if row['world'] == 'consistent']
assert len(old) == len(new_reversed) == len(new_consistent) == 2400
```

For directly packaged old/reversed views, existing `mapping_view_v1` contains:

| View | TRAIN file and rows | DEV file and rows |
|---|---|---|
| Mode1 | mode1_train.jsonl:2400 | mode1_dev.jsonl:800 |
| Reversed mode2 | mode2_train.jsonl:2400 | mode2_dev.jsonl:800 |
| Joint | joint_train.jsonl:4800 | joint_dev.jsonl:1600 |

Joint equals the two mode partitions' union, retaining mother record IDs, inputs and targets. R02 predates these packaged files and sampled the mother release directly. Its [original sampler](../../../../../../UNAVAILABLE.md) uses5 lists×2 commands×2 modes=20 answers in a joint batch. Preserve that sampler and [R02 Protocol](../../experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R02_single_layer_adamw/protocol.md) for training replay.

## Row fields

| Field | Meaning |
|---|---|
| record_id | split/world/command/ordered-list identity |
| list_id, words | ordered-list identity and three words; pairs commands |
| unordered_group_id | order-free content group for combination novelty |
| world, mode, command | experimental world, visible mode and visible command |
| panel, split | novelty panel and TRAIN/DEV/TEST identity |
| prefix, input_ids | original answer-free text and tokenizer output |
| target_word, target_id, rule | answer, answer token ID and FIRST/LAST rule |

Only `input_ids` enter the model; world/rule/target metadata organize supervision. A different tokenizer requires rechecking answer boundaries and regenerating IDs for that tokenizer.

## Matching the remembered finding

The common old endpoint has100% accuracy. Values below aggregate800 old/new DEV rows equally over two panels.

| Continuation-order seed | Reversed-only old/new accuracy | Joint old/new accuracy |
|---|---|---|
|29|0% /100%|100% /100%|
|43|0% /100%|99.75% /99.75%|
|71|0% /97.75%|99.75% /99.25%|

The three continuation orders share one acquired old endpoint. Single-task branches receive24000 new answers; joint branches receive24000 total answers,12000 old and12000 new. Joint success establishes a co-learning instance, not an equal-new-exposure architecture benefit. The R02 Summary retains complete facts and interpretation boundaries.

## Organization receipt

This update adds a discoverable dataset route, release lineage, real examples, fields and reuse instructions. [inventory.json](../../../../../../sources/Projects/from-attention-to-search/main/datasets/A17_04_list_rule_mapping/inventory.json) records current byte identities, counts and essential paired/view checks. Original releases already contained manifests and splits; their navigation and relationships were scattered. No frozen file was moved, regenerated or edited; no model was run. GitHub carries this guide and small metadata, while complete JSONL payloads remain execution-side.
