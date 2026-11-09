---
anchor_id: 15_06_online_spectral_routing_and_relay
legacy_anchor_id: 15_06_dynamic_online_spectral_routing
parent_line: 15_spectral_representation_and_functional_routing
status: completed_30b_downstream_evaluation_recorded
canonical_language: zh
companion_en: 15_06_online_spectral_routing_and_relay_anchor.md
updated: 2026-08-09
---

# A15_06 在线频谱路由与接力


归属说明：本父 Anchor 从临时编号 `A15_00_dynamic_relay_hmt` 迁入；不可变的
worker 作业和原始产物保留历史编号，项目编号为 `A15_06`。

## 1. Problem Definition

唯一决策问题是：动态 covariance 频带路由能否在四层 DCLM MoE 的10B终点改善预测质量；统一使用第一层来源的 Relay-HMT 是否稳定优于去均值完整输入、本层动态频带和同维随机 Relay。Head、middle、tail 是64/256/448维的层内 covariance 排名区间，不预设语义层级。

主指标是10B held-out next-token NLL，单位 nat/token，越低越好。它裁定终点预测质量，但不能单独识别机制。

## 2. Physical Priors

1. 表征持续变化时，冻结频带会成为陈旧坐标；确定性的在线更新可能降低该误差。
2. 同一浅层来源给后层 Router 提供共享的因果坐标，本层坐标则随层计算分别变化。
3. 任意稳定瓶颈都可能正则化 Router，因此必须用同维随机 Relay 排除这一解释。

追踪有效、谱身份价值和终点收益分别判定；终点未胜出不否定全部先验。

## 3. Falsifiable Hypotheses

- H1：动态 Local-HMT 优于 Centered-Full。
- H2（`AI_PROPOSAL`，收窄解释）：Relay-HMT 优于 Local-HMT。漂移减少只是候选解释，不能由该比较单独识别。
- H3（决定性）：Relay-HMT 优于 Relay-Random，说明 covariance 排名身份具有随机稳定旁路不能复现的价值。
- H4：EMA、嵌套 Grassmann 与回溯守卫使高置信 token 的刷新翻转率不超过1%。
- 最强 rival：收益完全来自去均值或任意稳定低维旁路。

只有两个 seed 及其文档配对区间都支持 Relay-HMT 优于三个对照，才支持 Relay-HMT；否则为不支持；终点或工程证据缺失则为 insufficient。

## 4. Mathematical Model

固定统计语料给出当前 covariance \(\widehat\Sigma_{\ell,k}\)，并以 \(\rho=0.1\) 更新 EMA。部署频带由嵌套 \(P_{64}\) 与 \(P_{320}\) 得到。Procrustes 对齐后，只通过候选 \(\gamma\in\{1,1/2,\ldots,1/128,0\}\) 更新，不对统计与分解反向传播。

高置信集合是旧 margin 的层内前25%。候选必须同时满足：高置信翻转率不超过1%、最大专家份额变化不超过0.01、且高置信集合上的 margin-normalized 专家相对 logit 变化 \(R_{cont}\le0.01\)。

## 5. Computational Realization

五臂均为四层 H768、8 稀疏加 1 共享专家的 top-1 MoE；专家接收完整本层输入。固定来源层身份，第一层仍训练并接收 Relay 梯度。

checkpoint 保留训练、统计和追踪状态以支持精确续训；遥测覆盖质量、路由和追踪，字段由 Protocol 保存。

## 6. Minimal Falsification Tests

决定性测试为两 seed 配对 10B NLL。护栏包括初始参数与数据一致、精确续训、投影正交/嵌套/完备、统计隔离及完整里程碑与逐文档 NLL。负载集中、高翻转或 \(\gamma=0\) 不自动停止；NaN、状态损坏或不可重建则使证据失效。

## 7. Current Evidence

既有 A15 已证明线性 Gate 的有限时间 covariance 学习速度偏置。冻结频带2B训练中，Local-HMT 更差；第一层 Relay-HMT 仅有小幅晚期终点优势、全程更差，且缺少随机 Relay 对照。因此在线频谱 Relay 仍未建立。

五臂合同 smoke 与最终 Relay 源码 smoke 均已通过，十个注册任务全部完成10B，零重试，终点逐文档配对证据齐全。Centered-Full 在两个 seed 中都明确优于 Vanilla-Full。Local-HMT 在两个 seed 上都是最低终点点估计，但相对 Centered-Full 只在 seed 17 明确改善。Relay-HMT 在两个 seed 中都明确劣于 Local-HMT 和 Centered-Full，也没有稳定优于 Relay-Random。因此 H2、H3 与完整 Relay-HMT 主张均不获支持。

在线更新器独立通过 H4：部署的 HMT 子空间比从不更新更接近当前 EMA 目标，所有注册实际刷新中的高置信 token 翻转率均为0；直接硬切换则会造成大幅路由不连续。也就是说，平滑追踪这一工程机制成立，但没有转化成 Relay-HMT 的终点效用。

补充的 Local-Random-Matched 两个10B任务也已完成。它以固定正交旋转删除
covariance 排名身份，同时把相邻目标的全部 principal-angle 运动保持到数值精度。
Local-HMT 相对该随机对照只在 seed 17 明确改善；seed 29 点估计反转且区间跨零。
随机臂并不更难追踪。因此固定 H/M/T 排名身份同样没有获得跨 seed 的功能证书。

30B 延长训练还暴露了另一类 Router 失败：虽然配置和日志均记录
\(\lambda_{LB}=0.01\)，A16 后续实现审计发现重计算路径使嵌套 LB 辅助张量没有
进入反向，因此这些源训练没有收到有效 LB 参数更新。Vanilla 深层仍在约
50M--100M token 已接近单专家，而 Centered 保持广泛使用。冻结 E04
根因审计裁定为 `necessary_only`：Vanilla 去独立真实均值使深层最忙专家占比
下降 0.68678 [0.68435, 0.68922]，高于匹配随机 q95 0.18326；给独立训练的
Centered 加回保存中心则未超过随机 q95。因此公共分量即时维持当前 Vanilla
坍缩，但学习路径适配使简单的双向静态偏置解释不成立。

seed 17 的 30B 八任务下游评估也已完成。没有任何模型通过相对 Centered-Full
的广泛迁移规则。Local-HMT 的导航性宏平均最高，并在 ARC-Easy、LAMBADA 上
获得配对区间高于零的改善，但其 covariance 身份在任何任务上都没有可靠优于
Local-Random。Relay-HMT 相对 Local-HMT 或 Relay-Random 都没有可靠正收益，
且在 ARC-Easy 明确更差。因此下游证据仍是任务特异的，不支持恢复 H2 或 H3。

Protocol：[A15_06_E01](../../../experiments/A15/15_06_online_spectral_routing_and_relay/A15_06_E01_10b_online_spectral_routing/protocol_cn.md)

身份对照结果：[A15_06_E02](../../../experiments/A15/15_06_online_spectral_routing_and_relay/A15_06_E02_local_random_identity_control/summary_cn.md)

30B 下游结果：[A15_06_E04](../../../experiments/A15/15_06_online_spectral_routing_and_relay/A15_06_E04_30b_downstream_evaluation/summary_cn.md)

迁入 A16 的负载控制结果：[A16_00_01_E01](../../../experiments/A16/A16_00_01_E01_dc_sustainer_audit/summary_cn.md)

## 8. Claim Boundary And Next Decision

证据仅覆盖四层 DCLM、两 seed 的 10B 终点及 seed 17 的 30B 下游结果；不支持 H/M/T 普遍语义、规模外推、组合计算或专业化的唯一因果解释。E02 不支持 covariance 身份优势。

历史议程把频谱/Relay 与负载控制分开；
[A16_00](../../16_load_control_gradient_interference/16_00_switch_lb_gradient_conflict/16_00_switch_lb_gradient_conflict_anchor_cn.md)
仍拥有后者，不授权继续试新方法。

**下一决策（`AI_PROPOSAL`，待研究者确认）：** 保留有界方法结果；重开须选定一个未识别机制，如漂移如何影响损失，并给出能排除来源信息与训练适配解释的比较。终点结果未完成区分，不授权执行。
