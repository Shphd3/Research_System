# 频率贡献桥梁与关系细分：v0.1 阅读入口

2026-10-19 先接收并归档v0.1，随后研究者明确认可并授权无训练A→B→C分析，现已完成并保留不足。**先读[白话一页](one_page_cn.md)或[结果概要](summary_cn.md)，再看[完整报告](detailed_cn.md)。** [执行授权与澄清](execution_amendment_01_cn.md)记录冻结参数和预算；收到的草稿正文及旧结果不覆盖，H3学习仍NOT RUN，Focus科学判断不变。

## 本轮要弄清什么

长期目的是在相同参数和计算预算下，让专家分工帮助模型学好并保留更多内容。本轮先检查一个前提：**根据输入中的 feature 频率与末层贡献来组织分发，是否形成了超出词片身份、且可复核的输入分工？** 学习收益是后续问题。

1. **目的。** 为专家分工建立可检查的依据，依次连接输入画像、关系细分和实际接收，避免把名单组织直接当成学习收益。
2. **问题。** 低频 feature 的贡献是否对应低频词片？同一词片的不同上下文是否有不同画像？同频段内的 φ 关系，是否比匹配随机子组提供额外共现和实际组成一致性？
3. **假设。** H1 预测低频贡献份额与当前词片稀有程度正相关；H2 预测同频段的关系子组在复核对话中优于匹配随机组；H3 预测最终留出学习与保留更好，但本轮不检验 H3。
4. **推进。** 先定义各频率段的末层贡献份额；检查词频与同词片上下文；构造同频关系组及匹配随机组；最后比较实际分发。只有另行冻结训练协议和预算后，才进入学习对照。

## 两个关键定义

feature 频率 \(p_i\) 是 TRAIN 中共享激活 \(z_i>0\) 的位置比例。末层贡献幅度代理为 \(c_i=z_i\|d_{28,i}\|_2\)，其中 \(d_{28,i}\) 是该 feature 的末层 decoder 向量。共享激活仍由原14层联合编码产生；换成末层 decoder 范数不等于获得了末层独立编码。

每个频率段把组内 \(c_i\) **求和，不除成员数**，得到 \(M_b\)；再除全字典贡献总和，得到原始份额 \(R_b\)。主规则先选贡献总量最大的频率段，再按段内子组贡献选择专家。校准对照只把第一步改为 \(M_b/\mu_b\)，其中 \(\mu_b\) 是 TRAIN 平均段贡献。

## 文件与边界

- [提取后的 Anchor 中文草稿](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_22_frequency_contribution_relation_refinement/15_22_frequency_contribution_relation_refinement_anchor_cn.md) · [English](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_22_frequency_contribution_relation_refinement/15_22_frequency_contribution_relation_refinement_anchor.md)。
- [Protocol 中文原文](protocol_cn.md) · [英文翻译](protocol.md)。中文与收到的附件逐字节一致。
- [飞书报告与 Anchor 原始合并稿](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_22_frequency_contribution_relation_refinement/sources/feishu_report_anchor_v0.1_cn.md)：保留组会背景、来源说明和原第九节讲述，不作为另一份现行设计。
- [接收及提取记录](intake_record.json)：原文件哈希、提取范围、未执行状态及仍待确认项。

接收时建议的四个log等宽频率段、总计八个接收槽位、每段两个子组、average-linkage，已经在后续明确认可后用于本轮有界分析。使用同一Tulu TRAIN的85,548个答案预测位置及已有缓存计算统计，没有重新推理提取激活；完整参数与权限以执行授权记录为准。

现有 EVAL 已被多次查看，后续复核只能称探索性复核。\(\varphi\)、组成相似度、接收率和专家内频率各回答不同问题，均不能单独证明共同学习有益。专家仍接收完整末层表征，高频信息不会因路由改变自动消失。

## 上一轮结果入口

- [DCLM 归一化路由与学习结果](../../15_21_activation_to_expert_learning/20261019_normalized_learning/summary_cn.md)。
- [Tulu SFT 学习结果](../../15_21_activation_to_expert_learning/20261019_tulu_sft/summary_cn.md)。
- [既有 TRAIN 频率图与迁移说明](../../15_21_activation_to_expert_learning/20261019_tulu_sft/paired_train_frequency_20261019/README_cn.md)。
- [旧完整结果的项目访问入口](../../15_21_activation_to_expert_learning/20261019_normalized_learning/full_results_access_cn.md)：大 ZIP 删除后仍可访问完整阅读目录和来源。

这些是前序证据，不移作本轮结果；本轮新实测见Summary/Detailed，停止于A–C，无专家训练。

## 三个认识的简洁重画

[四张图与逐图解释](redraw_three_insights_20261019/README_cn.md)：成员数与末层贡献、留出φ及独立的成员稳定性小图、仅旧T_S1第一轮的逐专家留出ΔNLL。每图提供PNG/SVG/PDF及源CSV；新分发分析与旧训练检查点分开标注。无新实验。
