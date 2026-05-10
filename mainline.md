# Mainline: Attention-as-Search / Dynamic Hierarchical KV Indexing

Last updated: 2026-05-10

## Long-Term Vision

把 long-context Transformer inference 从“对整个 KV cache 做 dense scan 的 attention 问题”，重新表述为“在动态生成的 KV memory 中做极端值检索的 search / indexing 问题”。

长期目标是设计一种 model-native 的 hierarchical KV memory indexing 机制，使模型在 million-token context 下不必线性扫描所有历史 token，而是先通过语义/结构索引生成小候选集，再做 exact sparse attention reranking。

## Mainline Shift

研究主线正式从 **Feature-Zipf Hierarchical MoE** 切换到：

> Long-context attention as search / hierarchical KV memory indexing.

旧 MoE 主线不删除，而作为前史和机制桥梁保留：

1. Feature-Zipf synthetic 让我们意识到，router/expert specialization 不能只看 routing frequency，必须问它是否对应真实机制、函数结构、以及可迁移的 memory partition。
2. Hierarchical MoE 的正确信号主要在 function-level recovery，而不是已经证明了 sparse feature division。
3. 这些结果把问题自然推向新的核心：MoE router / expert ID 是否可以从“稀疏计算路由”升级为“KV memory 的 learned semantic index”。

因此，MoE 现在是新方向中的一个候选 indexing mechanism，而不是主线本身的终点。

## Current Research Question

Long-context attention 的主要瓶颈是否可以被改写为动态检索问题？

更具体地说：

1. 标准 attention 在长上下文中是否主要是在寻找 softmax 后少数极端 winner，而不是均匀聚合所有 token？
2. 能否构造一个动态、分层、低延迟的 KV index，在 query time 先检索候选 KV，再对候选做 exact attention？
3. MoE router / expert ID 是否与 attention key-query geometry 对齐，足以作为 model-native inverted index？
4. 如果 routing geometry 与 attention geometry 不对齐，需要什么训练目标或结构让它们对齐？

## Background Assumptions

1. Softmax attention 是指数选择性的；在长上下文中，少数 high-logit token 对输出贡献最大。
2. 因此 long-context attention 可以近似看作 extreme-value retrieval，而不是 dense aggregation。
3. KV cache 是动态生成的 streaming vector memory，不是静态语料库；index 必须支持持续插入和低延迟查询。
4. 不同 layer/head 的 representation geometry 不同，不能假设存在一个全局共享索引。
5. MoE router 可能已经学习到某种语义/函数分区，但这是否对 attention retrieval 有用仍未证明。

## Core Hypothesis H1

如果 long-context attention 的有效贡献主要来自少数 softmax winners，那么可以用动态 hierarchical KV indexing 把 dense global scan 分解为：

1. coarse semantic / structural routing；
2. localized candidate retrieval；
3. exact sparse attention reranking。

在这个框架下，MoE router / expert ID 是一个重要候选：它可能同时承担 sparse computation routing 和 KV memory addressing。

## Current Evidence

Primary architecture note:

- `/data/250010109/from-attention-to-search/docs/architecture.md`

MoE 前史结果：

- `results/R002_correlation_aware_feature_zipf.md`
- `results/R001_dclm_moe_input_sparse_atom_summary.md`

Current transition experiment card:

- `experiments/E003_attention_as_search_kv_indexing.md`

## Current Safest Claim

可以安全地说：从计算结构上看，million-token attention 暴露了一个 memory search / indexing 问题；MoE routing 提供了一个自然的 model-native candidate index 设想。

但目前还不能说：MoE expert ID 已经与 attention softmax winners 对齐，也不能说 hierarchical KV indexing 已经在真实模型上带来端到端加速或质量保持。

## Current Claim Boundary

Can say:

- Long-context attention 可以被重新解释为 query-key ranking 后的极端值检索问题。
- Dense attention 在 million-token context 下的关键压力不仅是 FLOPs，也包括 memory movement 和全局 KV traversal。
- Dynamic KV indexing 的合理目标是 candidate generation + exact sparse attention，而不是直接替代 attention score 本身。
- MoE router / expert ID 是一个有动机的候选 inverted index，因为它可能代表模型内部的 learned partition。
- 旧 Feature-Zipf Hierarchical MoE 结果支持“router 语义和机制对齐需要被诊断”，但不支持“hierarchy 已经解决 specialization”。

Cannot yet say:

- MoE experts 天然对应稳定、可检索的语义区域。
- Expert ID 能高召回未来 attention softmax winners。
- Dynamic hierarchical KV indexing 能在真实 long-context inference 中保持质量并显著加速。
- 当前结论已经适用于所有 layer/head 或所有任务类型。
- 旧 synthetic MoE 结果已经直接证明真实语言 hidden states 的 KV indexing 可行。

## Open Questions

1. Attention softmax winners 在真实 long-context traces 中有多稀疏、多稳定？
2. Top attention keys 是否集中在少数 layer/head/router/expert buckets 中？
3. MoE routing geometry 与 attention dot-product geometry 的相关性有多强？
4. Index bucket imbalance 会不会让 retrieval 退化成 overloaded bucket 内线性扫描？
5. Temporal locality、recency、semantic routing 应如何组合成多级 memory hierarchy？
6. Candidate retrieval 的 recall / candidate size / latency trade-off 应该如何报告？
7. 是否需要训练目标显式鼓励 routing-to-attention alignment？

## Next Decisive Direction

先做最小诊断，不急于声称系统加速：

1. 在真实或半真实 long-context inference trace 中记录 query、top attention winners、layer/head、以及可用的 router/expert assignment。
2. 测量“用 expert/router bucket 取候选”对 dense attention top winners 的 recall。
3. 同时报告 bucket balance、candidate size、head/layer 差异、以及 temporal fallback 的增益。
4. 只有当 candidate recall 与 bucket balance 同时过关，才进入真实 sparse attention / latency 实验。
