# E003 Attention-as-Search / KV Indexing Minimal Diagnostic

Last updated: 2026-05-10

## Question

MoE router / expert assignment 是否能作为 long-context KV memory 的候选检索索引？

更具体地说：query token 的 router/expert bucket 能否高召回 dense attention 的 top key/value winners，同时保持候选集足够小、bucket 足够均衡？

## Hypothesis

如果 MoE routing geometry 与 attention query-key geometry 有足够对齐，那么用 router/expert ID 建立 inverted KV index 后，query-time 只检索相同或邻近 buckets，就能覆盖大部分 dense attention top winners。

## Why This Setup

新主线不是先做完整系统加速，而是先验证最关键的 claim boundary：

> expert/router buckets 是否真的能找到 attention softmax winners？

如果这个诊断失败，后续 hierarchical KV indexing 需要换索引信号或加入 training-time alignment objective；如果通过，才值得实现 sparse attention reranking 和 latency benchmark。

## Data / Setup

候选设置：

- 使用真实或半真实 long-context inference traces；
- 记录每个 layer/head 的 query、key、dense attention top-k positions；
- 同步记录可用的 MoE router / expert assignment，或用可替代的 learned partition label 做第一版诊断；
- 对每个 query 构造 candidate set：same expert bucket、top-r expert buckets、temporal fallback、以及二级 local bin。

## Compared Indexes

最小比较：

- Dense attention top-k: oracle reference；
- Random bucket index: negative control；
- Temporal window only: recency baseline；
- Expert/router bucket only: core hypothesis；
- Expert/router bucket + temporal fallback: practical hybrid；
- 如果可行，加入 layer/head-specific local bin refinement。

## Metrics

- Recall@K of dense attention top winners；
- Mass recall: covered dense attention probability mass；
- Candidate set size；
- Bucket size distribution / imbalance；
- Per-layer and per-head variance；
- Insertion/update overhead proxy；
- Failure cases: long-range semantic dependency vs local context dependency。

## Results

Not run yet.

## Interpretation

通过标准不应只看 recall。若 expert bucket recall 高但 bucket 极不均衡，检索仍可能退化为大桶内线性扫描。若 temporal baseline 已经解释大部分 winner，则主线需要区分“recency cache”与“semantic KV index”的贡献。

## Claim Strength

当前实验卡只定义诊断。尚不能支持“MoE expert ID 已经是有效 KV index”或“hierarchical KV indexing 已加速 inference”。

## Limitations

- 不同模型是否有 MoE router 会影响可测信号；
- dense attention top-k 不完全等价于最终生成质量；
- 真实 latency 还取决于 GPU sparse memory access 和 kernel 实现；
- layer/head 的异质性可能要求多个 index，而不是一个全局 index。

## Next Experiments

1. 先跑 trace-level recall / balance diagnostic。
2. 若 recall 足够高，加入 exact sparse attention reranking，比较 dense attention logits/output error。
3. 若 output error 可控，再做 latency/memory benchmark。
4. 若 recall 不足，设计 routing-to-attention alignment objective 或改用 hybrid semantic/temporal index。
