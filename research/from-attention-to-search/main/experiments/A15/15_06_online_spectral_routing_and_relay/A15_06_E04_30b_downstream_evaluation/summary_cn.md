---
experiment_id: A15_06_E04_30b_downstream_evaluation
status: complete
scientific_verdict: fail_broad_transfer_with_task_specific_local_hmt_gains
last_updated: 2026-08-09
---

# 最终结果摘要

## 直接结论

六个 30B 模型中，没有任何方案通过“相对 Centered-Full 的广泛下游迁移”判据。
Local-HMT 的八任务导航性宏平均最高（37.84%，Centered-Full 为 37.33%），
并在八项任务中的六项点估计更高；但逐题配对后，只有 ARC-Easy（+1.98 个百分点）
和 LAMBADA（+1.30 个百分点）的 95% 区间完全高于零。因此它是当前最好的
任务特异候选，而不是已经证明的普遍赢家。

频谱身份本身没有获得证书：Local-HMT 相对运动匹配的 Local-Random，在八项任务
中没有一项差异的配对区间排除零。浅层 Relay 也未获支持：Relay-HMT 相对
Local-HMT 在 ARC-Easy 低 3.20 个百分点、LAMBADA 低 1.55 个百分点，且没有
可靠更好的任务；它相对 Relay-Random 也没有可靠正收益，并在 ARC-Easy 更差。

## 决定性证据

准确率表示答对的样本比例，越高越好。下表均为百分比；Macro 只是八个异质任务
的无权平均，用于快速阅读，不代表统一能力。

| 模型 | ARC-C | ARC-E | HellaSwag | LAMBADA | PIQA | RACE | SIQA | WinoGrande | Macro |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Vanilla-Full | 22.70 | 39.23 | 28.79 | 24.68 | 61.04 | 25.45 | 36.23 | 51.38 | 36.19 |
| Centered-Full | 22.87 | 40.32 | 30.29 | 26.33 | **64.09** | 26.70 | 36.69 | 51.38 | 37.33 |
| Local-HMT | 22.87 | **42.30** | **30.49** | **27.63** | 62.84 | 27.27 | 36.85 | **52.49** | **37.84** |
| Local-Random | 22.95 | 41.04 | 29.98 | 26.70 | 63.98 | 26.89 | 36.23 | 49.96 | 37.22 |
| Relay-HMT | 23.98 | 39.10 | 30.01 | 26.08 | 63.22 | **28.04** | **36.90** | 50.36 | 37.21 |
| Relay-Random | **24.15** | 40.66 | 29.94 | 25.91 | 63.22 | 27.46 | 36.18 | 47.99 | 36.94 |

![八任务准确率](figures/figure1_task_accuracy_heatmap.png)

下图按相同题目做配对比较；星号表示 10,000 次重采样所得的 95% 区间不跨零。

![架构机制对比](figures/figure4_mechanism_contrasts.png)

相对 Vanilla，Centering 的证据最清楚：HellaSwag +1.50、LAMBADA +1.65、
PIQA +3.05 个百分点，三个配对区间均高于零。这与 30B DCLM 验证损失排序
定性一致，但不能据此证明二者由同一机制导致。

## 有效性与边界

六个 step-38,147 checkpoint 均通过评估态 Router 守卫：原生 logit 离线重放
误差为零、winner 一致率为 1.0、评估前后 Router buffer 不变、Local/Relay
投影确实改变部分路由、嵌套子空间数值有效，Relay 后层也精确读取已保存的第一层
来源。因此负结果不能归因于评估时漏掉 center 或投影。

本结果只有一个 seed、一个四层 H768 模型族和八项零样本任务，不能建立普遍迁移，
也不能仅凭准确率说明改进机制。另一个实现审计发现，源训练虽记录了
`lambda_LB=0.01`，但重计算路径使 LB 辅助张量没有真正参与反向；六模型比较仍然
有效，但不能把差异归因于有效的 LB 正则。

## 下一决策

不因当前下游点估计继续放大 Relay-HMT；A15 下一步应先检验由专家相对效用定义的
loss-aligned 坐标，是否在线性 Router 分数和同维随机坐标之外提供功能增量。

