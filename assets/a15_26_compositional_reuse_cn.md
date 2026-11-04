# A15_26 / R01 资产入口

归属是A15_26独立父Anchor的R01受控符号实验，区别于并行订单V2。

[事实Summary](../Projects/from-attention-to-search/main/experiments/A15/15_26_low_frequency_compositional_reuse/R01_controlled_operations/summary_cn.md) · [Detailed](../Projects/from-attention-to-search/main/experiments/A15/15_26_low_frequency_compositional_reuse/R01_controlled_operations/detailed_cn.md) · [Artifact manifest](../Projects/from-attention-to-search/main/experiments/A15/15_26_low_frequency_compositional_reuse/R01_controlled_operations/artifact_manifest_cn.md).

Execution root: `/data/250010109/MoE_Router/experiments/20261024_a15_26_compositional_reuse`. Required original inputs: `model_qwen3_0p6b_base`, `tokenizer_qwen3_0p6b_base`. Generated task: `data_a15_26_20261024`. Native prefix cache: `representation_a15_26_20261024`. Saved family: `checkpoint_family_a15_26_20261024_full`, 788 actual members including8 Smoke states and780 formal milestones. Original Smoke family remains `checkpoint_family_a15_26_20261024_smoke`. Consumed endpoint IDs use `checkpoint_a15_26_20261024_<sha16>`. Derived evidence: `analysis_a15_26_20261024`.

[Selected full-family strict access](/data/250010109/Research_System/assets/checks/20261024T182208Z_a15_26_full.json) · [Selected analysis strict access](/data/250010109/Research_System/assets/checks/20261024T182235Z_a15_26_analysis.json). Actual files/hashes/bytes and saved counters are enumerated in the manifest, not inferred from planned milestones. These are selected current-conversation checks, not a complete library refresh.

状态保存可续训字段，但只是依赖精确Base和父状态的增量；独立进程资格包括原Smoke和本次完整末层1→2精确验证，未对每个终点重跑。另有一个验证保存状态，单独登记为checkpoint_a15_26_20261024_recovery_block_probe。原生缓存精确回放与保存完整，不补足失败的组成跨问法/组合科学资格。机制诊断仍为探索性，研究者科学接受Unknown。
