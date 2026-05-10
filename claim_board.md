# Claim Board

Last updated: 2026-05-10

Use this board before reports and meetings. Do not present a claim more strongly than its current status.

Status labels:

- `supported`
- `weakly supported`
- `unsupported`
- `contradicted`
- `unclear`

## Claim A: Long-context attention can be interpreted as search over KV memory.

Status: supported as conceptual reframing.

Evidence: Standard attention ranks all historical keys by query-key dot product, then softmax makes the largest logits dominate. At million-token scale this resembles extreme-value retrieval over a dynamically generated memory, not uniform aggregation over all tokens.

Meeting boundary: say this is a computational interpretation and research framing. Do not claim it already gives an implemented speedup.

## Claim B: Dynamic hierarchical KV indexing is a plausible architecture direction for million-token inference.

Status: weakly supported.

Evidence: The architecture note identifies a natural decomposition: candidate retrieval, then exact sparse attention reranking. This matches the structure of search systems and addresses the global KV scan bottleneck.

Meeting boundary: plausible direction only. Need real trace diagnostics for recall, bucket balance, update overhead, and hardware behavior.

## Claim C: MoE router / expert ID can serve as a model-native inverted index.

Status: unclear.

Evidence: MoE routing already partitions token representations for sparse computation, so expert IDs could in principle index KV positions by learned semantic region. However, previous MoE work did not prove that expert partitions align with true mechanisms strongly enough, and it did not test attention winner recall.

Meeting boundary: present as the central hypothesis, not as a result.

## Claim D: Expert/router buckets are aligned with attention softmax winners.

Status: unsupported.

Evidence: No current result yet measures whether query-time router assignments retrieve dense-attention top keys with high recall.

Meeting boundary: this is the first decisive diagnostic for the new mainline.

## Claim E: Hierarchical KV indexing can preserve dense-attention quality while reducing inference cost.

Status: unsupported.

Evidence: No current end-to-end sparse attention experiment has shown quality preservation, latency reduction, or hardware-efficient dynamic insertion.

Meeting boundary: do not make performance claims until after recall diagnostics and sparse-attention implementation tests.

## Claim F: Feature-Zipf Hierarchical MoE remains useful as mechanism bridge.

Status: supported.

Evidence: Earlier Feature-Zipf work clarified that specialization must be evaluated by feature/function alignment and not only routing frequency. It also exposed the gap between learned routing and true mechanism recovery.

Meeting boundary: keep this as motivation for why router-index alignment must be diagnosed carefully.

## Claim G: Hierarchical MoE is already better than flat MoE at sparse feature specialization.

Status: unsupported.

Evidence: Previous synthetic diagnostics did not show a clear advantage over flat middle spectral MoE on sparse feature division metrics.

Meeting boundary: this remains an old-branch boundary. Do not import it as a positive premise for the new KV indexing mainline.

## Claim H: Current safest mainline claim.

Status: supported.

Evidence: The safe claim combines only the architectural reframing and the open hypothesis: million-token attention exposes a memory search/indexing bottleneck, and MoE routing is a natural candidate signal for model-native indexing.

Meeting boundary: say “natural candidate” and “needs trace-level validation,” not “validated solution.”
