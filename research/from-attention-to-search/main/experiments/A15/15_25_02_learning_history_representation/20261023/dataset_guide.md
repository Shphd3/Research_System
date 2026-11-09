# Data guide: the same list under two conditional rules

Research question: How does learning history change conditional-rule representations, and which directions matter most for answering?

Each input contains a visible mode, a command and three distinct words. In old task A, mode one maps 甲 to the first word and 乙 to the last. In new task B, mode two reverses that mapping. For the actual example `模式：一。口令：甲。列表：绿 黑 马。答案：`, the answer is 绿. Changing only mode one to mode two makes 马 correct. Each example has one next-token answer target.

The source asset is `data_a17_conditional_mapping_v1`. This analysis uses all 1,600 old/reversed DEV records in 400 unordered-word groups and never reads TEST. Both modes and both commands of a group stay together. SHA256(group ID) modulo two gives 196 discovery groups / 784 rows and 204 evaluation groups / 816 rows. This separates the present selection from evaluation; it does not undo A17's prior DEV exposure.

| Source panel | Discovery rows | Evaluation rows | Meaning |
|---|---:|---:|---|
| order_new | 396 | 404 | New-order panel as defined by the original dataset |
| combination_new | 388 | 412 | New-combination panel as defined by the original dataset |

Each cell is equally divided between old/new worlds. Lists always contain three words; inputs have 19–21 tokens. Distance is not manipulated. Every input token, answer position and target ID is identical across model states.

Both continuation endpoints start from acquired A and run 1,200 updates. B-only sees 24,000 B answers; mixed continuation sees 12,000 A plus 12,000 B answers. These are controlled training exposures. Feature occurrence is the fraction of this analysis sample with nonzero CrossCoder activation. These frequencies are different, and neither measures pretraining exposure.

The [Protocol](protocol.md) fixes analysis and boundaries. Raw examples remain at `/data/250010109/MoE_Router/experiments/20261023_learning_history_representation/data/examples.jsonl`; the frozen manifest and execution receipt record its hash.
