# Source Index

本包基于以下材料整理：

- `0518 group meeting_原文.docx`: 重点时间段 00:00-24:20。
- `0518 group meeting_笔记.docx`: 记录了 major questions、oracle MoE setting、两阶段 reverse index 实验安排。
- `router_specialization_and_retrieval_report_ZH.pdf`: 之前汇报文档，结论为 `feature separability != router specialization` 与 `router specialization != KV index`，但需要审计其中不可靠处。
- `E2_theory_ai_package.zip`: 历史 mainline / consensus，保留“synthetic feature 可读回、router 不 clean、reverse index 未证实”的边界。

关键组会线索：

1. 00:56-01:55: 提出 inhibition / all-expert-forward 的想法，同时指出 NTP 本身没有 specialization 先验。
2. 02:34-03:14: 有效 specialization 可能需要 atomic feature / topic feature 的拆分；并且 attention softmax 选择性强，不一定需要完美 router。
3. 03:54-04:26: 数据分布是否均匀 / Zipfian 会影响 specialization 与 index 最优形式。
4. 05:02-07:12: supervised feature routing + reverse index 的汇报被指出 metric 不对：导师要看 NTP / influence loss，而不只是 attention output error 或 recall。
5. 07:27-07:44: 不能假设剩余 experts / missed KV 的贡献正交。
6. 10:08-12:23: 表征不是干净单一 feature；实现上 gate 用于分发的表征和送给 expert 计算的表征应区分。
7. 15:14-17:13: inhibition 可以产生“某 feature 不送某 expert”的压力，但不保证多个 features 不塌到同一 expert。
8. 17:13-22:10: 最终目标不是一个 expert 一个 feature，而是在大量 features 与有限 experts 中形成可控映射，降低 KV / memory 访问 latency；Zipf 下均匀分配未必最优。
9. 23:46-24:20: 推进方式必须 A->B->C，每一步先验证 work / not work，不能跳过中间链条。
