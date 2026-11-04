# Pre-inference amendment: fixed16 context

2026-11-04T01:10:21.489566+00:00

Full-question-length matching leaves only11 Magicoder/GSM8K documents per group. Add equal16-token causal-prefix secondary control for all257 documents before reading any activation. This controls observed context length, not full source-question length or lexical content.

Original protocol, frozen plan and panel remain unchanged. Add position15 as cache axis9, after the original eight main positions and fixed32 axis8. No new model forward is required. Report this secondary comparison separately; it cannot rescue a primary failure. Use the original document-level bootstrap/permutation and pair rule.
