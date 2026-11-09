# Purpose Card: E3 Synthetic vs Real Data Statistics

## 1. Purpose / Main Reason

比较 synthetic 数据假设和真实语言数据统计之间的相同与不同，避免把 toy 结果直接误认为 real data 结论。

## 2. Known Narrative / Premise

Synthetic data is useful only as a controlled mirror of a hypothesized real-data property. After synthetic validation, compare properties, not model performance first.

## 3. Hypothesis To Decide

H3: 真实语言也包含 repeated sequential patterns 和 heavy-tailed popularity，但真实数据的 hierarchy、ambiguity 和 context dependence 会比 toy synthetic 数据复杂。

## 4. Experiment Question

Synthetic generator 捕捉到了真实数据的哪些统计属性？哪些没有捕捉到？

## 5. Data And Task Construction

Synthetic side:

- n-gram / phrase frequency distribution。
- conditional entropy $H(x_{t+1}\mid x_{t-k:t})$。
- repetition and burstiness。
- context-dependent next-token certainty。
- hierarchical composition。

Real side:

- same audit columns as synthetic `data_audit.json` where possible。

## 6. What This Can Prove

它可以 claim synthetic generator 是否捕捉了 selected real-data statistical properties。

## 7. What This Cannot Prove

它不能 claim MoE expert specialization in real LLMs unless real model routing and attention diagnostics are measured.

## 8. Next Step

Create a real-data audit table with the same columns as synthetic audit.
