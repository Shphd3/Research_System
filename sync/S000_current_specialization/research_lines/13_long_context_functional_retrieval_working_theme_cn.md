# 长上下文功能检索工作主题

## 状态

这是 2026-07-17 组会的跨线工作主题，等待研究者确认；不是正式 A13
锚点，不授权实验，也不替代 A06 主线。

## 主题

**从检索命中到功能效用：长上下文 Router 到底应该优化什么？**

核心判断：

> 百万词元名义容量不等于可用上下文。固定计算预算下，被 Router 选中的
> 信息只有能够维持标准预测头的正确决策，才具有功能检索价值。

## 问题链

```text
名义容量
-> 必要证据可访问
-> 信息形成与传递
-> 标准头因果使用
-> 有序组合或多跳聚合
-> Router 预测功能效用
-> 专家产生稳定 held-out 单位成本效用
```

## 已有确定回答

R3/R4 已回答 Q0：在当前 all-trigram 受控设置中，即使特征与 Router
分桶完美对齐，稀疏输出质量仍弱于同数量局部基线。因此
one-feature-one-expert 不足以成为有效 KV 索引。

这个负结果不能外推到一般长上下文或真实 Agent，但它切断了“只要表征可分，
检索自然成立”的路线。

## 建议的最小下一问题

在现有检查点上，随机、局部、特征分桶和 attention 排序能否在相同 top-$k$
预算下预测记忆项的因果损失效用？

主指标：

$$
\Delta_s(k)
=
\mathbb E_q\left[
\ell\!\left(q;S_s^k(q)\right)-\ell(q;C_q)
\right].
$$

它衡量稀疏选择相对完整记忆增加多少标准头损失；越小越好。它不证明
百万词元尺度、记忆项独立效用或 MoE 专家价值。

## 当前唯一决策

研究者先填写机制猜想、最强竞争解释、最不确定点、改变判断的证据和唯一下一
决策，然后批准、修改或否决该 loss-utility 审计。批准前不得写正式 Protocol
或执行。

来源：[完整中文工作主题](../../../daily_research_reports/0716/docs/long_context_functional_retrieval_working_theme_cn.md) · [English working theme](../../../daily_research_reports/0716/docs/long_context_functional_retrieval_working_theme.md) · [R3](../../../Projects/from-attention-to-search/main/experiments/archive/R3_perfect_router_retrieval/summary.md) · [R4](../../../Projects/from-attention-to-search/main/experiments/archive/R4_attention_output_router_retrieval/summary.md)
