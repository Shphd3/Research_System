# Execution Plan: E4 Hierarchical Phrase Extension

## 1. Run Goal

Extend the synthetic corpus from flat planted patterns to nested phrase patterns.

## 2. Setup

- Dataset: controlled phrases with nested subpatterns and Zipf-like counts.
- Models: dense Transformer first, then MoE.
- Task: next-token prediction.

## 3. Metrics

- Low-level n-gram recovery.
- Higher-level phrase recovery.
- Error by hierarchy level.
- Attention pattern over earlier phrase tokens.
- Expert routing by hierarchy level, if MoE is used.

## 4. Gate

Run only after E0-E2 are clean.
