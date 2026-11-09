---
anchor_id: 15_06_02_router_expert_specialization
parent_anchor: 15_06_online_spectral_routing_and_relay
status: completed_mixed_not_supportive
canonical_language: en
updated: 2026-08-10
---

# A15_06_02 Router--Expert 专业化与利用


## 1. Problem Definition

本子 Anchor 判断五个具有可微负载均衡损失的训练臂，是否不仅终点语言模型损失不同，还表现出两种可分离的功能性质：专家对同一输入形成不可互换的变换；Router 能选择具有最佳反事实下一词效用的专家。它继承父 Anchor 对 covariance H/M/T 与同维随机路由的比较，不重开父 Anchor 的终点 NLL 裁定，也不替换当前 A15 主线。

唯一问题是：在配对的 2B、5B、10B checkpoint 上，Local-HMT 或 Relay-HMT 是否比其随机匹配对照形成并利用更强的专家专业化？Pass 将父结论从一般架构效应推进到 covariance 身份的功能证据；Fail 继续不支持 covariance 身份；缺少反事实或配对证据则为 Insufficient。

## 2. Physical Priors

如果一种路由坐标确实有助于划分可学习功能，专家在同一输入上的变换应逐渐不可互换，而且 Router 分数应能按 token 特异的下游效用排序专家。仅仅参数重叠下降并不够，因为任意瓶颈、置换、噪声或冗余参数化都可能制造几何差异，却不改善专家选择。若 HMT 只产生几何差异、但不改善反事实选择质量，该先验在本模型上不成立。

## 3. Falsifiable Hypotheses

**H1，covariance 特异的功能路由：** 相比匹配随机臂，HMT 在 10B 时具有更低的 Router 选专家遗憾，以及更高的 Router 分数—强制专家效用秩一致性；参数几何、同输入专家输出与替换代价提供同方向的辅助证据链。

**最强竞争解释，任意瓶颈导致分化：** HMT 和随机对照都可能让专家看起来不同，但都不能改善 Router 选择；也可能只是一个专家对所有 token 普遍更好，从而产生替换代价，却没有条件化专业分工。

## 4. Mathematical Model

对 token \(x\)、目标层 \(\ell\)、Router 原生选择 \(s(x)\)，以及只在该 token 和该层强制使用专家 \(e\) 时得到的下一词 NLL \(L_{\ell,e}(x)\)，定义选专家遗憾：

\[
r_\ell(x)=L_{\ell,s(x)}(x)-\min_e L_{\ell,e}(x)\quad\text{nat/token}.
\]

\(r=0\) 表示 Router 在八个专家中选到了反事实最优者；数值越大，表示当前选择即时多付出了更多预测损失。它不能识别长期训练因果，因为干预只发生在冻结 checkpoint 的一个 token、一个层。

## 5. Computational Realization

冻结五个 seed-17 模型在 2B、5B、10B 的 checkpoint。在固定 held-out 文档和位置上依次强制八个稀疏专家，主分析保持原生 Router 概率作为共同输出幅度，并以单位幅度作敏感性分析。Router logits 与负的强制专家 NLL 做 token 内秩相关。专家专业化进一步拆成：主参数子空间重叠；同一批专家输入上的线性 CKA；反事实替换代价与 oracle 最优专家的 token 间多样性；以及 Router 分数与专家主输入参数方向激活的经验耦合。共享专家固定不变并单列报告。

## 6. Minimal Falsification Tests

决定性比较是 10B 的 Local-HMT 对 Local-Random-Matched，以及 Relay-HMT 对 Relay-Random。主指标是以文档为独立单位、四层等权平均的选专家遗憾配对差。covariance 特异功能证书要求：HMT 的遗憾差 95% 配对区间低于零，同时 Router 分数—效用秩相关差的区间高于零。两个匹配比较使用 Holm 校正的配对符号翻转检验。参数重叠或 CKA 单独变化不能判 Pass。

强制路由 no-op、模型 buffer 不变、held-out token 身份一致、checkpoint provenance 一致、CKA 使用同输入、参数重叠采用同维 Haar null，以及 oracle 最优专家不是全局单一专家，都是必要护栏。护栏失败判 Insufficient，而不是科学 Fail。

## 7. Current Evidence

已完成的 [E06 审计](../../../../experiments/A15/15_06_online_spectral_routing_and_relay/A15_06_E06_2b_10b_router_expert_specialization_audit/summary_cn.md) 对冻结、seed-17 结论有效，typed verdict 为 `mixed_not_supportive`。10B 时，Local-HMT 减 Local-Random 的遗憾为 \(-0.01042\) nat/token，配对 95% 区间 \([-0.02878,0.00753]\)；分数—效用差为 \(-0.00022\)，区间 \([-0.01313,0.01278]\)。Relay-HMT 减 Relay-Random 的两个点估计都不利：遗憾 \(+0.01352\)、区间 \([-0.00361,0.03052]\)；分数—效用差 \(-0.01121\)、区间 \([-0.02745,0.00481]\)。两条路径均未通过联合区间与 Holm 校正 sign-flip 规则。

功能证书失败并不是因为专家可以互换。五臂的同输入专家输出 CKA 均值为 \(0.326\)--\(0.335\)，强制专家 NLL spread 为 \(0.467\)--\(0.505\) nat/token，oracle entropy 为 \(0.996\)--\(0.997\)，Router 选中反事实最优专家约 \(34\%\)，高于 \(12.5\%\) 机会水平。因此专家已有 token 条件化功能差异，Router 也利用了一部分；covariance H/M/T 身份没有比匹配随机瓶颈更好地利用这些差异。

## 8. Claim Boundary And Next Decision

现有证据支持冻结、单 seed 条件下“专家不可互换但 Router 利用不完整”，并否定注册尺度上的 covariance 特异功能证书。它不能证明专业化导致终点 NLL，不能建立跨 seed/尺度规律，不能证明 H/M/T 的普遍语义，不能推出随机路由普遍更优，也不能判定 PCGrad 的训练收益。

本子 Anchor 已完成，不替换当前 A15_07 主路由。唯一下一决策是：A15_07 是否能找到跨表达复现的 conditional-fine 方向，先通过语义证书，再进入独立的专家效用准入。完成条件是 held-out 方向证书与后续功能准入；恢复动作是审核 A15_07 Section 8 的六项待定设计。
