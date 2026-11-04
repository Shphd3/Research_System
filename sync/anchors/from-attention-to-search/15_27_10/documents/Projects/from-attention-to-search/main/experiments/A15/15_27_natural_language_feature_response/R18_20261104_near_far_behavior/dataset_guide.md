派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R18_20261104_near_far_behavior/dataset_guide.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R18_20261104_near_far_behavior/dataset_guide.md)；研究修改仍回到原件。

---

# Dataset guide

Constructed English container/object records, not a sampled external corpus. [Protocol](protocol.md) owns definitions and freeze. Actual text+token IDs+offsets+candidate sequences: /data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R01_behavior/data/panel.jsonl; family/split/templates: /data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R01_behavior/data/families.json; complete grammar/filler inventory: /data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R01_behavior/data/templates.json. Panel SHA256=77594e13a72d16b340c34a21d04328a8dab1e3aa8276fdc9f04713a81ac100da. Keep all444prefixes, including failures. No-fact baseline has no gold label. Deliberate lure is separately marked. Input weights and any pre-existing dataset are not copied into this panel. Asset IDs only for model/tokenizer in config. A/B and distances are repeated within family; heldout template groups are absent from smoke; no train/test fit occurs.
