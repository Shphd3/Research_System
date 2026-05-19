# Reliability Checklist - Reverse Index Mainline

## P0: Implementation checks

- [ ] 用 full attention teacher 生成 `H_t` 时，layer/head/position 与 RI target 完全一致。
- [ ] causal mask 正确；不能 retrieve future KV。
- [ ] RI candidate set budget 与 local/random 完全匹配。
- [ ] random baseline 按相同有效位置采样，不偷看 future。
- [ ] local baseline same-count，而不是固定窗口导致不公平。
- [ ] layer1 guide 与 layer2 guide 明确区分。
- [ ] two-pass guide 不作为 speedup claim。
- [ ] gate input 是 attention output；expert input 不变。

## P1: Metric checks

- [ ] 报告 NTP loss delta，不只报告 attention output error。
- [ ] 报告 attention mass retained，不只报告 top-k recall。
- [ ] 报告 logit/target probability delta，解释 missed KV 是否重要。
- [ ] 报告 candidate count / memory bytes proxy。
- [ ] 对 uniform 与 Zipf 分布分开报告。

## P2: Interpretability checks

- [ ] 不把 feature oracle 当作 upper bound；真正 upper bound 是 attention top-M oracle。
- [ ] 不把 supervised routing 的 NMI=1 当作 retrieval success。
- [ ] 不把 local baseline strong 解释成 method dead；可能是数据短程性。
