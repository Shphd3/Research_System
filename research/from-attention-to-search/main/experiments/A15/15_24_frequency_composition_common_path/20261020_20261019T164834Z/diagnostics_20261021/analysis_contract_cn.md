# 冻结高频路径诊断：授权范围

这是用户要求的事后诊断。起点是：T_H 相对 T_F 没有稳定的额外收益；现有结果没有证明加入共同路径有害。不修改原 Protocol，不选新模型、不训练参数、不关闭科学问题。

来源：[原 Protocol](../protocol_cn.md)、[Summary](../summary_cn.md)、[Anchor](../../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_24_frequency_composition_common_path/15_24_frequency_composition_common_path_anchor_cn.md)。

## 三个检查及其区分作用

1. **没有新增有用能力：**在同一批低频位置上，保留搭档、关掉或打开被选 B4 专家的残差，比较答案 NLL。
2. **替换有代价：**核对 H 是否替换 F 原来的一个专家。固定同一个已训 checkpoint，比较原搭档与强制高频搭档；每路系数始终是 1/2。
3. **收益存在异质性：**直接查看同一位置的终点 NLL(T_H)−NLL(T_F) 分布及两种子一致性，不用新谱图替代预测效果。

三个解释可以同时存在。B4 是频率名单标签，不能预先称为已学会共同语义的专家。

## 固定数据和计算

- 原运行：`frequency_composition_common_path/20261019T164834Z`；T_F/T_H，第168步，种子11/22，不挑 checkpoint。
- 使用已有 DEV 的10,340个答案目标；固定 TRAIN-B1 定义，取其中1,701个含 B1 的位置。DEV 已暴露，本次不是独立确认。
- 复用缓存 h、target、feature 和路由，核对 block/position/target 对齐及所需资产访问。
- 配对分析直接读取原逐位置 NLL。分层仅按路由是否替换、被替换专家是否来自 B1 等结构定义，不按结果寻找赢家。
- 冻结前向保留原输入尺度、完整 h、专家、最终 RMSNorm 和输出头；每个启用专家仍乘1/2。关掉一路时不把它的系数补给另一路。
- 对真正替换的位置，F 调用记为(a,b)，H调用记为(a,c)，c是所选 B4 专家。在同一 checkpoint 内比较 Base、仅a/2、仅c/2、(a+b)/2和(a+c)/2；残差都加回 h。成本允许时同时复核已训 T_F/T_H 两种权重。
- CPU BF16 重放必须报告相对原 GPU 逐位置 NLL 的误差；与误差相当的小效应保留数值边界。不把调试主机的可见 GPU 当作预留算力。
- NLL 单位是每答案位置 nats；差值为负表示改善。按对话重采样仅作探索性描述，两种子不构成总体稳定性证明。

## 交付与边界

执行根目录：`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/common_path_hypothesis_checks/20261021T045000Z`，`paired`与`ablation`分开写入。保留输入/代码身份、访问记录、数值校准、逐位置数组、汇总表及双语事实记录；旧结果不变。

跨 T_H/T_F 的终点比较同时包含训练暴露、学习权重和调用变化；同 checkpoint 换路由只隔离冻结后的调用效果，不能代替另一条训练轨迹。高频残差有用也不等于共同语义能力得到证明。不更新 Focus/Anchor 科学状态，不重训，不 commit/push 或发布。
