# Current Research Entry

Last updated: 2026-05-10

## Canonical Files

- Mainline: `mainline.md`
- Claim board: `claim_board.md`
- Current primary experiment: `experiments/E003_attention_as_search_kv_indexing.md`
- Architecture source: `/data/250010109/from-attention-to-search/docs/architecture.md`

## One-Sentence Mainline

把 long-context attention 视为 search：在动态生成的 hierarchical KV memory 中先做 model-native candidate retrieval，再对小候选集做 exact sparse attention，而不是对 million-token KV cache 做全局 dense scan。

## Current Safest Claim

当前可以安全主张：million-token attention 的核心瓶颈可以被重新表述为动态 KV memory indexing 问题；MoE router / expert ID 是一个自然但尚未验证的候选索引信号。

不能说 MoE experts 已经与 attention winners 对齐，也不能说 hierarchical KV indexing 已经在真实 inference 中完成质量保持和加速。

## Current Bottleneck

立即瓶颈是把概念从 architecture note 变成可验证诊断：测量 router/expert buckets 对 dense attention top winners 的 recall、bucket balance、candidate size，以及不同 layer/head 的差异。

## Relation to Previous MoE Mainline

Feature-Zipf Hierarchical MoE 阶段保留为前史/机制桥梁：

- 它提供了 router/expert specialization 的诊断语言；
- 它提醒我们不能把 routing frequency 当成机制分工；
- 它目前不支持“hierarchy 已经优于 flat MoE 做 sparse feature division”；
- 它现在服务于新问题：router/expert assignment 是否能成为 KV memory indexing 的 learned semantic partition。

## Today

Current task: 将 Research_System 主线从 Feature-Zipf Hierarchical MoE 正式迁移到 attention-as-search / dynamic hierarchical KV indexing，并建立第一张 claim boundary 与下一步实验卡。

Expected daily output: 更新 `mainline.md`、`CURRENT.md`、`PROJECT_INDEX.md`、`claim_board.md`，并新增一个最小实验条目作为下一阶段入口。
