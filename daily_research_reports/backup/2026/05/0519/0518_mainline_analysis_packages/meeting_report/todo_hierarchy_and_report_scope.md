# Todo Hierarchy and Report Scope

## 一句话结论

下一次组会只汇报两个闭环：`router 实际按什么分` 与 `reverse index 到底该优化什么指标`；不要扩散到“MoE 是否有语义”或“新架构已经解决”。

## P0 - 立刻做，决定实验是否可信

### Code / implementation

1. 打 hook 验证新模型：gate input = attention output；expert input = original hidden。
2. 验证 RI causal mask、layer alignment、candidate budget。
3. 重新跑 supervised feature routing + RI：同时报告 NTP loss delta、attention mass、output error。
4. 重新跑 oracle-MoE one-to-one match：区分 oracle routing 成功、expert utility 成功、RI retrieval 成功。

### Minimal figures

1. Gate/expert input hook diagram。
2. Router cell top-example table。
3. RI source decomposition bar chart。
4. Full vs RI NTP loss table。

## P1 - 推进研究主线

### Gating side

1. Expert cell exemplar analysis。
2. Counterfactual route flip test。
3. Boundary walk / interpolation。
4. Common component removal。
5. Expert utility landscape。

### Reverse-index side

1. Attention source decomposition。
2. Candidate generator tournament。
3. Layer1 guide vs layer2 two-pass guide。
4. RI train vs RI inference mismatch。
5. Zipf latency proxy。

## P2 - 后续架构方向

1. Inhibition + balance as diagnostic regularizer。
2. Common/specialized split gate。
3. Learned dual-index: query route predicts key bucket set。
4. Hybrid local + learned bucket retrieval。

## 组会报告范围界定

### 必须说

- 目标是降低 KV memory access / latency，不是追求漂亮的 one-feature-one-expert。
- 之前链条断在两处：feature 可分不等于 router 分，router 分不等于 KV index。
- 新模型改动是为了分离 gate representation 与 expert computation representation。
- 下一步用 NTP loss / attention mass / memory proxy 共同判断 reverse index。

### 不要说

- 不说 MoE router 没有语义。
- 不说 reverse index 不可能。
- 不说 inhibition 已经能保证 perfect specialization。
- 不说 supervised NMI=1 代表 retrieval 成功。
- 不说 full-attn train + RI infer 的失败代表 RI train 失败。

## 30s advisor version

我把现在的问题拆成两个闭环。第一，routing 闭环：在新 oracle-MoE 里，gate 用 attention output、expert 输入不变，我先不再用 feature-id probe 当主证据，而是反向分析 router cell、route flip、boundary walk 和 expert utility，弄清楚 router 实际按什么分。第二，reverse-index 闭环：我会在 2-layer 模型里只替换第二层 attention，比较 layer1 guide、layer2 two-pass guide、local、random、feature oracle、hidden/key/value nearest，并且用 NTP loss、attention mass、output reconstruction 和 memory proxy 一起判断。inhibition 只作为排他性诊断，不作为主线结论。
