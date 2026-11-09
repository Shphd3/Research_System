# H0521 AB Feature Specialization

The legacy purpose card was removed; this experiment record is the surviving
source.

This experiment tests whether ordinary no-load-balance top-1 MoE routing forms
feature-level specialization for A-only, B-only, and AB-composite samples, or
whether one expert cell mixes them because they share a broader hidden-state
bundle.

Primary metric:

```text
class-specific expert ablation delta CE
```

Run workspace:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/
```
