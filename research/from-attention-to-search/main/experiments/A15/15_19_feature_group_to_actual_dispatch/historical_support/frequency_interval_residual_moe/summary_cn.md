# 频率区间残差MoE旁支：一页概要

**本轮结论：线性分组均非空，但固定评分没有把输入充分分给八个专家，正式学习收益比较未启动。** 工程检查通过与研究假设得到支持是两件事。任务`pt-vv7zkyxf`已SUCCEEDED，停止点为事前TRAIN覆盖门槛。

## 目的、假设与对照

检验冻结Qwen3-0.6B Base表征上的频率区间固定路由，是否比保留八组人数的随机分组改善包含低频feature输入的下一token预测（NTP）。A按TRAIN原始激活概率线性等宽分8段；B只随机重分成员、保各组人数。C/D是可学习router的无／有负载均衡参考。学习收益待检验，不是φ分组或预训练容量结论。

## 现象与关键证据

9615个合格feature的八组人数为**9253、183、124、34、7、3、2、9**。A每组都广泛命中输入，但实际top-1路由为**0、0、0、129、201、646、9893、119843**；最高频组专家得到**91.68%**位置。B两次随机分组各八专家都通过覆盖门槛。A无并列或全零fallback，两种子的A路由完全相同；这不是两次学习复现。

包含低频feature的95544个TRAIN位置中，88524个（**92.65%**）进入最高频组专家，0个进入低频名单所在的专家0。名单中分到哪个专家，不代表携带该feature的输入会进入那个专家。

[图1：名单、命中与路由](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/figures/analysis_members_hits_routes.png) · [图2：频率组到实际专家](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/figures/analysis_event_allocation_train.png) · [图3：专家内实际频率](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/figures/analysis_within_expert_q_train.png)

## 解释与结论边界

冻结模型／头／CrossCoder、同窗缓存、下一token标签、零旁支等价、梯度及小样本拟合均通过。A前三专家零暴露，第四仅129位置，未达到预定每专家≥200位置且≥20上下文；据此停止正式A/B及次要C/D，未换分箱、调阈值或挑替代结果。**主指标A−B低频验证NLL、两seed学习曲线、正式C−D、训练后谱全部NOT RUN；不能判频率分组没有收益。**

低频输入覆盖TRAIN约73%、EVAL约75%，高频输入覆盖全部位置，两者重叠；这里不直接测某条低频知识。验证源文件／位置不重叠，但原文档及近重复独立性Unknown，冻结CrossCoder曾见这些文本。

## 本轮改变的认识、竞争解释与下一步

改变的是：原线性名单＋贡献均值评分在本窗口不足以形成八个有学习机会的专家，不应直接进入收益检验。仍存竞争解释：评分对常见feature的响应优势压过分组；这与“频率组织本身是否有益”不同。

**AI建议的唯一下一检验，未执行：**保留这八段与已存A/B名单，只事前登记一种TRAIN均分校准评分，与原评分在同缓存比较路由覆盖，先判断是否能恢复有效暴露；不立刻增加训练。

远程流程72.46秒，CPU图表汇总22.55秒；正式训练0步。完整[Protocol](protocol_cn.md)、[Detailed与读图说明](detailed_cn.md)、[原始收据](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/provenance/pipeline_receipt.json)已保存。未commit/push，未自动继续实验。
