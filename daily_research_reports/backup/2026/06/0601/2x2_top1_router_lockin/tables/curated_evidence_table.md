# Curated Evidence Table

| evidence | observation | interpretation | boundary | next decision |
|---|---|---|---|---|
| Early lock-in trajectory | Failed seeds 在 step 0 已经 A/B same expert，最终 NMI=0。 | Collapse 更像 early top-1 lock-in，不是 late optimization drift。 | 只说明 minimal 2x2 top-1 proxy。 | 检查能否通过显式 route-function binding 改变训练路径。 |
| Success dynamics trajectory | Successful seed 在 step 0 已经 A/B split，并保持 NMI=1。 | 初始 split 可以被训练稳定放大。 | 只说明 route-pattern separation，不说明 utility-aligned specialization。 | 下一步必须加入 expert utility 证据。 |
| No-router-bias diagnostic | 去掉 router bias 后 random-init split rate 从 3/10 提高到 6/10。 | Router bias 是 collapse 风险因子，但不是唯一原因。 | 不能 claim 去掉 bias 足以解决 lock-in。 | 不把初始化修补作为主线，转向 route-function binding。 |
| Metric mismatch | Token accuracy 可以为 1，但 routing NMI 可以为 0。 | Task learning 不等于 route-pattern specialization。 | 不说明真实 MoE 训练一定如此。 | 同时看 route assignment 和 forced expert utility。 |
