# A06_25 warmup 谱方向 router 重初始化 anchor

## 0. Thinking Card

**现象：** A06_24 说明 step-0 的 all-position 聚类不能稳定初始化 router。但一个关键替代解释仍然存在：step-0 hidden state 和 expert 参数还太随机，训练 10/40 步后也许会出现可用 feature geometry。

**机制猜想：** 早期训练可能让 hidden state 或 expert 输入主奇异方向变得 feature-aware。如果成立，warmup 后再聚类或用 expert SVD 方向重置 router，应提升均匀 feature 到 expert 的分发。

**关键变量：** warmup step、hidden-state pool、expert top singular direction、router row、feature center、common/mean direction、feature route assignment、margin、slot-start nuisance。

**因果关系：** warmup 若增强 feature-aware geometry，则从该 geometry 初始化的 router row 应提升 feature NMI 和正 margin；若方向太相近、对齐 common 或不含 feature 信息，则不会提升。

**可观测指标：** 主指标是 balanced route-position eval 上的 feature-route NMI；guard 是 matched preserve fraction、margin p05、max load、target accuracy、slot-start NMI。

**替代解释：** all-position 失败可能来自 hidden state 未成形、样本池错误、位置 shortcut、当前 router feedback lock-in；expert SVD 失败可能来自方向太近、common 对齐或 feature-unaware。

**决策：** 如果 warmup all-position 或 warmup expert SVD 接近 route-position clustering 且没有位置泄漏，则进入 delayed reinit 方法候选；否则继续把 route-relevant state selection 和 margin preservation 作为主瓶颈。

## 1. Problem Definition

**父问题：** A06 研究均匀 features 能否进入不同 experts，并在训练中保持。

**更尖锐子问题：** 判断 all-position 和 expert-spectral 初始化失败，是因为 step 0 geometry 未成形，还是因为这些 geometry 本身不 route-relevant / feature-aware。

**术语解释：** 与英文 canonical anchor 保持一致；核心术语包括 uniform feature、route position、all-position pool、expert top singular direction、warmup、feature NMI、matched preserve fraction、margin p05、slot-start NMI。

**决策问题：** 在同一个 no-position uniform slot 数据集上，短 warmup 后，all-position hidden-state 聚类或 expert top singular directions 是否足够 feature-aware，可以初始化 router rows 完成均匀 feature 分发？

**不在范围：** real DCLM、语义专家、可部署 MPI router、common/rare 频率不均衡、证明 spectral routing 不可能。

## 2. Physical Priors

**P1：早期训练可能形成 feature geometry。** 如果成立，warmup 后 all-position 或 expert SVD 初始化会提升 feature NMI 和 margin。

**P2：all-position 仍可能是错误样本池。** 即使 warmup，所有位置混在一起仍可能不是 route-position routing 的正确对象。

**P3：expert top singular directions 可能是高增益但不 feature-aware。** 它可能太相近、对齐 common，或只反映当前 router feedback。

## 3. Falsifiable Hypotheses

**H1：warmup rescue all-position clustering。** warmup all-position 若接近 route-position，则支持；若仍低，则削弱。

**H2：expert SVD 失败来自 feature-unaware。** raw / orthogonalized / common-projected SVD 都不提升 feature NMI，则支持。

**H3：warmup 让 expert SVD 变可用。** warmup 10/40 后 expert SVD 明显优于 step 0，则支持。

## 4. Mathematical Model

$$
h_{i,p}^{(k)} = c_{\rho(p)}^{(k)} + r_{f_i,p}^{(k)} + \eta_{i,p}^{(k)}
$$

$$
A_e^{(k)} = U_e^{(k)}\Sigma_e^{(k)}V_e^{(k)\top},\qquad
v_e^{(k)} = V_e^{(k)}[:,1]
$$

$$
\gamma_f^{(k)} =
w_{m(f)}^\top\mu_f^{(k)} -
\max_{e\ne m(f)}w_e^\top\mu_f^{(k)}
$$

判断标准是候选 row 是否对 feature centers 给出正 margin。

## 5. Computational Realization

使用 no-position uniform slot synthetic dataset。warmup `0/10/40` 步后，分别从 all-position hidden states、route-position hidden states、oracle feature centers、expert input-side top singular vectors 构造 router rows，然后训练并评估。

## 6. Minimal Falsification Tests

1. warmup hidden clustering：检验 hidden state 未成形解释。
2. expert SVD failure decomposition：区分 row similarity、common alignment、feature-unaware。
3. warmup expert SVD：检验 expert 参数谱方向是否随训练变得 route-aware。

## 7. Current Evidence

A06_24 已说明 all-position clustering 弱于 route-position/oracle。A06_23 已说明 margin 太薄时初始化会失效。0703 谱空间 router 阅读提示：谱方向可能有用，但必须先审计它是否 feature-aware。

A06_25 full local two-GPU run 的结果是：warmup 会改善 all-position clustering 和 expert SVD 的 feature awareness，但不能补齐 route-position gap。Immediate feature NMI 中，all-position 从 warmup 0 的 `0.774` 升到 warmup 40 的 `0.876`；route-position warmup 40 为 `0.996`。Raw expert SVD warmup 40 为 `0.879`；common-projected expert SVD 为 `0.943`，且 immediate margin p05 为 `0.514`。orthogonalized expert SVD 更差，warmup 40 NMI 为 `0.704`，margin p05 为 `-5.311`。

解释：step-0 hidden state 未成形是部分解释，但不是完整解释。route-relevant state selection 仍是主瓶颈。expert spectral direction 不是完全无用，但必须经过 common-alignment、feature-awareness 和 margin 审计，不能直接当作已成立方法。

## 8. Claim Boundary And Next Decision

**可 claim：** warmup 让 uniform no-position slot dataset 上的 all-position hidden states 和 expert SVD directions 更 feature-aware；common-projected expert SVD 是当前最强 spectral candidate；简单正交化不是关键修复。

**不可 claim：** real DCLM、语义专家、最终 MPI router、spectral routing 不可能性，或 common projection 已经是最终方法。

**下一步：** 不把 all-position delayed reinit 或 raw expert SVD 升级为完成方法。建立 nested-learning aligned anchor，检验多词元/长时距监督能否让 route-relevant hidden states 更早 feature-aware，并产生更厚 margin。
