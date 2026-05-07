# [调研]MoE - 迭代状态存档 v6.0

> 本版本的任务不是继续扩展理论，而是先收敛。
> 我们要回答三件事：
> 1. 现在到底已经知道了什么？
> 2. “专家低秩性 / 专一化 / 按方差分发”到底该怎么定义？
> 3. 下一轮究竟该继续推进 quadratic，还是先修定义与度量？

## 0. Checkpoint Metadata
- **项目**：MoE Router for Continual Learning
- **版本**：`v6.0`
- **日期**：2026-03-30
- **当前阶段**：`收敛整理 / 大版本升级 / report同步`
- **本次更新触发器**：`整合 0319-0327 的状态文档 + 0327 最新结果，并修正 ACP baseline 与 quadratic 证据范围的表述`
- **一句话 North Star**：为 Continual Learning 找到一种真正能诱导“有用专家专一化”的 Router。
- **本 checkpoint 的作用域**：本版本只负责冻结当前认知、修正定义、明确下一轮实验入口；不负责宣称 quadratic 已经胜出。

## 1. Executive Summary
- **当前最强主张**：对 CL 有用的 Router 不能用单一指标定义；它必须同时诱导 assignment concentration、几何紧致、跨域隔离和非坍塌负载。
- **当前最大不确定性**：我们还没有证明 quadratic router 是必要的，更没有证明它已经是最优路线。
- **本轮相较上轮的核心变化**：
  - 明确了 `linear_running_center` 才是严格 baseline，`acp_on` 只是参数增强 comparator。
  - 明确了当前训练态的 quadratic 证据只稳定存在于 `ckpt40000`。
  - 新增了 `acp_lite` 作为下一轮更公平的 mean-direction comparator 候选。

## 2. Stable Knowledge / Report-Ready Claims

| ID | Claim | Evidence Type | Confidence | Can Write to Report? | Notes |
| --- | --- | --- | --- | --- | --- |
| C1 | `center` 是必要条件；`no_center` 会产生极端刚性、过大 margin/CR，但不对应更好 CL 几何 | main exp | high | yes | 24L ckpt40000、12L ckpt60000/70000 一致支持 |
| C2 | Router 质量是多目标问题，结构指标与任务性能显著解耦 | main exp | high | yes | 低 SI / 低 ED 不自动带来最高 Avg |
| C3 | `linear_running_center` 是当前严格 baseline；`acp_on` 只能作为参数增强 comparator，而不能作为公平 baseline | main exp | high | yes | `acp_on` 在 logit 前增加了额外参数量 |
| C4 | `low_rank` 能改善部分结构指标，但不是当前唯一主线解释 | main exp | medium | partial | 结构有效，任务与 SI 未持续领先 |
| C5 | `quadratic_nosvd` 在鲁棒性和专家分离上有积极信号，但当前训练态证据只到 `ckpt40000`，其 CL 优势仍未被证明 | main exp | medium | partial | 训练不稳定，跨 checkpoint 证据不足 |
| C6 | `acp_lite` 是下一轮必须纳入的更公平 comparator：它测试“显式利用 mean direction”而不过度增加表达能力 | theory + exp | medium | partial | 目前待测 `ckpt40000` |
| C7 | “专家低秩性”目前还没有被我们定义好，`ED / ED_comp` 只能算过渡指标 | theory + exp | high | yes | 本版本明确修定义为下一轮主任务 |

## 3. Hypothesis

| ID | Hypothesis Statement | Status | Why It Matters | Current Evidence | Blocking Risk |
| --- | --- | --- | --- | --- | --- |
| H1 | 对 CL 有用的“专家专一化”必须由 assignment、compactness、isolation、balance 四部分联合定义 | supported | 解决“好分发是什么”这个根问题 | 多次出现单指标最好但整体最差的反例，尤其 `linear_no_center` | 还缺 assignment 的更好指标，如 NMI / purity |
| H2 | 更低的 occupied subspace + 更低的跨域子空间重叠会降低 forgetting proxy | active / partially supported | 这是“为什么低秩有助于抗遗忘”的数学桥梁 | SI、Overlap、ED 的经验结果支持方向正确，但还没有真实 CL 训练闭环 | 目前仍是 proxy，不是直接 forgetting 证明 |
| H3 | `linear_running_center` 是严格 baseline；`acp_on` 只能作为参数增强 comparator，`acp_lite` 才是更公平的 mean-direction 对照路线 | supported | 如果 baseline 定错，后续“谁更强”的结论会失真 | `acp_on` 在 logit 前增加额外参数，`acp_lite` 则更接近公平比较 | `acp_lite` 当前仍缺完整评测 |
| H4 | Debiased quadratic router 只有在 centered linear 确实错过了二阶可分性时才有必要 | active | 这是“我们到底需不需要 quadratic” 的核心判据 | 当前只有 intuition 和局部现象，没有 no-training discriminative test | 可能 quadratic 只是更稳，不是真的更会分发 |
| H5 | `d_tau_comp` 会比 `ED_comp` 更适合作为“专家低秩性”的主指标 | active | ED/ED_comp 对弱尾部过敏，会模糊“真正占用的方向数” | 数学上合理，且符合当前指标缺陷感受 | 需要固定 `tau` 选择协议并重算最新 checkpoint |

## 4. Mathematical Modeling

### 4.1 Core Objects and Definitions
- **输入与路由**：
  - token 表征：$x \in \mathbb{R}^d$
  - expert 随机变量：$E \in \{1,\dots,K\}$
  - domain / semantic cluster：$C$
- **运行中心化记号**：
  - 运行均值：$\mu_t \in \mathbb{R}^d$
  - 中心化特征：
    $$
    x_c = x - \mu_t
    $$
  - 其中 $\mu_t$ 可由 EMA 估计：
    $$
    \mu_t = (1-\beta)\mu_{t-1} + \beta \bar{x}_t
    $$
- **当前 specialization panel**：
  - assignment concentration：$H(E \mid C)$
  - geometric compactness：当前用 $ED_{\mathrm{comp}}$，下一轮主推 $d_{\tau,\mathrm{comp}}$
  - cross-domain isolation：$SI$
  - anti-collapse：$CV_{load}$
- **建议的新低秩指标**：
  - 统计维度：
    $$
    d_\tau(C_e) = \mathrm{Tr}(C_e(C_e+\tau I)^{-1}) = \sum_i \frac{\lambda_i}{\lambda_i+\tau}
    $$
  - 能量秩：
    $$
    r_\alpha(C_e) = \min\left\{k:\frac{\sum_{i\le k}\lambda_i}{\sum_j \lambda_j}\ge \alpha\right\}
    $$

### 4.1.1 Working Router Definitions
- **Centered linear router**：
  $$
  \ell_{\mathrm{linear}}(x) = W x_c,\qquad W \in \mathbb{R}^{K \times d}.
  $$
  这是当前严格 baseline；所有新路线都应首先与它做公平比较。

- **ACP-on router**：
  - 定义中心方向单位向量
    $$
    u_t = \mu_t / \|\mu_t\|_2 .
    $$
  - 将中心化特征分解为平行与正交部分
    $$
    x_{\parallel} = (u_t^\top x_c)u_t,\qquad x_{\perp} = x_c - x_{\parallel}.
    $$
  - 再做带参数的结构化组合
    $$
    \tilde{x}_{\mathrm{ACP}} = W_{\parallel} x_{\parallel} + W_{\perp} x_{\perp},
    $$
    $$
    \ell_{\mathrm{acp\_on}}(x) = G \tilde{x}_{\mathrm{ACP}},
    \qquad
    W_{\parallel}, W_{\perp} \in \mathbb{R}^{d \times d},\;
    G \in \mathbb{R}^{K \times d}.
    $$
  - 解释：`acp_on` 不是严格 baseline，因为它在最终 logit 前引入了额外参数化变换；它更适合作为 parameter-augmented comparator，用于测试 “mean-direction structure 是否有用”。

- **ACP-lite router**：
  - 仍然使用同样的几何拆分
    $$
    x_{\parallel} = (u_t^\top x)u_t,\qquad x_c = x - \mu_t.
    $$
  - 直接分别映射到 expert logit 空间后相加
    $$
    \ell_{\mathrm{acp\_lite}}(x) = A x_{\parallel} + B x_c,
    \qquad
    A,B \in \mathbb{R}^{K \times d}.
    $$
  - 解释：`acp_lite` 仍显式保留了 mean-direction 信息，但避免了 `acp_on` 那种更重的 pre-logit 参数化，因此是当前更公平的 mean-direction comparator。

- **Raw quadratic router**：
  - 定义逐维二阶特征
    $$
    q_{\mathrm{raw}} = x_c \odot x_c.
    $$
  - 对应 logits
    $$
    \ell_{\mathrm{quad\_raw}}(x) = W_1 x_c + W_2 q_{\mathrm{raw}},
    \qquad
    W_1, W_2 \in \mathbb{R}^{K \times d}.
    $$
  - 解释：它把去均值后的逐维方差信号直接暴露给 router，但尚未去除稳定的二阶偏置。

- **Debiased quadratic router**：
  - 定义二阶均值项
    $$
    \lambda_t = \mathbb{E}[x_c \odot x_c],
    $$
    实际可由 EMA 估计
    $$
    \lambda_t = (1-\gamma)\lambda_{t-1} + \gamma \overline{(x_c \odot x_c)}_t.
    $$
  - 定义去偏后的二阶特征
    $$
    q_{\mathrm{deb}} = x_c \odot x_c - \lambda_t.
    $$
  - 对应 logits
    $$
    \ell_{\mathrm{quad\_deb}}(x) = W_1 x_c + W_2 q_{\mathrm{deb}}.
    $$
  - 解释：如果不同 domain 的主要可分信息在 centered first-order statistics 中已经存在，则 debiased quadratic 不应是必要结构；只有当可分性主要残留在二阶统计中时，它才有结构性价值。

- **当前公平比较主线**：
  $$
  \texttt{linear\_running\_center}
  \;\; \text{vs} \;\;
  \texttt{acp\_lite}
  \;\; \text{vs} \;\;
  \texttt{debiased quadratic}.
  $$
  其中 `acp_on` 保留为辅助 comparator，用于判断显式 mean-direction 建模是否值得，但不再承担严格 baseline 的角色。

### 4.2 Main Derivation
- **目标**：把“专家低秩性有助于抗遗忘”从口号改成可检验的数学对象。
- **推导主线**：
  1. Router 决定哪些样本进入 expert $e$；
  2. 该划分决定 expert 内部协方差 $C_e$；
  3. 两个任务在同一 expert 中的干扰由子空间占用与重叠共同决定。
- **关键公式**：
  - 谱干扰：
    $$
    SI_e = \frac{\mathrm{Tr}(C_{e,A} C_{e,B})}{\|C_{e,A}\|_F \|C_{e,B}\|_F}
    $$
  - 干扰上界：
    若
    $$
    C_{e,\mathrm{old}} = U_o \Lambda_o U_o^\top,\quad C_{e,\mathrm{new}} = U_n \Lambda_n U_n^\top,
    $$
    则
    $$
    \mathrm{Tr}(C_{e,\mathrm{old}} C_{e,\mathrm{new}})
    \le
    \|\Lambda_o\|_2 \|\Lambda_n\|_2 \|U_o^\top U_n\|_F^2.
    $$
  - **解释**：occupied directions 更少、subspace overlap 更低，则跨任务冲突更小。

### 4.3 Assumptions and Failure Modes
- **显式假设**：
  1. Expert 更新主要受 routed feature 的协方差几何支配。
  2. 当前的 SI / compactness proxy 足够接近真正的 forgetting mechanism。
  3. 若 centered linear 缺失一阶可分性，而 domain 差异主要在对角二阶矩上，则 quadratic 才有结构性必要。
- **如果这些假设被打破，会出现什么现象**：
  - 低 SI / 低 rank 但无下游收益；
  - 高 margin / 高 CR 却依然高干扰；
  - quadratic 只带来更稳的边界，却不带来更好分发。
- **当前最脆弱的一步推导**：从“低 occupied subspace”到“真实抗遗忘”仍缺直接 CL 训练证据。

### 4.4 Observable Predictions
- **Prediction P1**：如果 H1-H2 正确，则真正好的 router 应在 specialization panel 上形成非支配优势，而不是只赢一个指标。
- **Prediction P2**：如果 H4 正确，则在 frozen-feature/no-training audit 中，debiased quadratic 应在 covariance-dominant domain pair 上显著优于 centered linear。
- **Prediction P3**：如果 H5 正确，则 `d_tau_comp` 会比 `ED_comp` 更稳定地区分“真紧致”和“尾部很多但能量弱”的 expert。

## 5. Experiment Design

### 5.1 Decision Target
- **本轮实验要区分的 competing explanations**：
  1. `centered linear / ACP` 已足够；quadratic 不是必要结构。
  2. centered linear 确实错过了二阶可分性；debiased quadratic 有必要。
- **实验结束后希望更新的假说**：H4、H5。

### 5.2 Setup
- **模型/数据集**：
  - 现有主要结果：24L `ckpt40000`；12L `ckpt60000/70000` 的 centered-family 对照
  - 当前重点模型：`linear_running_center`、`low_rank`
  - 参数增强 comparator：`acp_on`
  - 待纳入的更公平 comparator：`acp_lite`
  - 当前 quadratic 训练态证据：`quadratic_nosvd @ ckpt40000`
  - 数据集：WOS
- **控制变量**：
  - 相同层位：Layer 2 / 6 / 10
  - 相同长度截断：`max_length=128`
  - 相同 domain pair：优先 `CS vs Medical`，后续增加更强对比 domain pair
- **自变量**：
  - 路由形式
  - compactness 指标定义（`ED_comp` vs `d_tau_comp`）
- **可能的混杂因素**：
  - `acp_on` 相比 centered linear 在 logit 前增加了额外参数量，不能作为严格 baseline
  - `quadratic_nosvd` 当前只测到 `ckpt40000`，无法和 `ckpt60000/70000` 形成完全同口径趋势比较
  - `acp_lite` 结果尚未补齐
  - `quadratic_nosvd` 的 Round3 margin 导出口径异常
  - SI 当前是按 expert 平均，不是按 token 加权
  - 采样方式在部分实验中并非完全 round-robin

### 5.3 Metrics

| Metric | Operational Definition | Why This Metric | Expected Direction |
| --- | --- | --- | --- |
| `H(E\|C)` / NMI / Purity | cluster-domain 到 expert 的映射集中程度 | 定义“专一化”不能只看几何 | down / up |
| `d_tau_comp` | 补偿后的统计维度 | 更好地定义“真正占用的方向数” | down |
| `r_0.9_comp` | 90% 能量秩 | 提供直观的人类可解释量 | down |
| `SI` | 同一 expert 内 A/B 协方差干扰 | 最接近 CL 的结构指标 | down |
| `CV_load` | 专家负载均衡 | 防止 collapse 假阳性 | down |
| `Avg` | Round0 任务均分 | 结构收益必须保住能力 | up |
| `CR(0.5)` | 高噪声鲁棒性 | 检查稳定性而非主结论 | up |

### 5.4 Execution Plan
1. 对 `linear_running_center / low_rank / acp_on` 的已有结果重算 `d_tau_comp`、`r_0.9_comp`、NMI/Purity。
2. 补测 `acp_lite @ ckpt40000`，判断 mean-direction 显式拆分在更公平参数设定下是否仍有收益。
3. 做 frozen-feature/no-training audit：直接比较 centered linear 与 debiased quadratic 的可分性。
4. 做 Step-0 audit：`raw_linear` vs `centered_linear` vs `raw_quadratic` vs `debiased_quadratic`。
5. 修复 `quadratic_nosvd` 的 Round3 margin 导出后，再决定是否值得进入下一轮训练主线。

### 5.5 Expected Outcomes and Decision Rule

| Outcome Pattern | Interpretation | Hypothesis Update | Next Action |
| --- | --- | --- | --- |
| centered linear / ACP-lite 在新 panel 上仍最优，quadratic 无 no-training 优势 | quadratic 不是当前必要路线 | H4 降级 | 以 `linear_running_center` 为 baseline 推进真实 CL |
| debiased quadratic 在 no-training audit 上显著更优，且 Step-0 无塌缩 | quadratic 具备结构性必要 | H4 支持 | 进入正式训练版 debiased quadratic |
| `d_tau_comp` 与 `ED_comp` 排名差异大，且更符合视觉谱结构 | 旧低秩定义有偏 | H5 支持 | 用 `d_tau_comp` 替换主指标 |

## 6. Conclusion / Update

### 6.1 New Results
- **关于 baseline 的修正**：
  - `acp_on` 不能再被表述为严格 baseline，因为它在 logit 计算前增加了额外参数。
  - `linear_running_center` 应作为当前真正的 baseline。
- **关于 quadratic 的修正**：
  - 当前训练态的 `quadratic_nosvd` 结果只稳定存在于 `ckpt40000`。
  - 因此不能再把它和 `ckpt60000/70000` 上的 centered-family 结果写成完全同口径趋势比较。
- **关于下一轮 comparator 的修正**：
  - `acp_lite` 已被提出，作为更公平地测试 “显式利用 mean direction 是否有帮助” 的新对照。

### 6.2 Interpretation
- **结果支持/反驳了哪条假说**：
  - 支持 H1：Router 质量是 multi-objective，不是单指标。
  - 支持 H3：`linear_running_center` 应被固定为主 baseline，`acp_on` 只能作参数增强 comparator。
  - 仅部分支持 H2：compactness/isolation 的方向对，但离真实 CL 仍差一步。
  - 未支持 H4：目前没有足够证据说 quadratic 是必要结构。
- **最合理的解释是什么**：
  - `ACP` 说明“mean 方向不是简单该删掉的噪声”，而是可能要被结构化处理；但 `acp_on` 的效果不能直接当作公平 baseline 证据。
  - `quadratic_nosvd` 可能更多是在改变边界稳定性，而不是已经学会了“按方差正确分发”；而且当前证据范围仍不足。
- **还有哪些替代解释没有被排除**：
  - `acp_on` 的收益部分来自额外参数量，而不只是 mean-direction structure；
  - `acp_lite` 也许能保留主要收益，同时提供更公平的比较；
  - quadratic 的当前优势只是鲁棒性优势，不是分发优势；
  - `ED_comp` 的口径缺陷掩盖了真正的 compactness 排名；
  - 最新 quadratic margin 为 0 可能完全来自实现问题。

### 6.3 Anomalies and Hidden Variables
- **异常现象**：
  - `linear_no_center` 的高 margin / 高 CR 与高 SI 同时出现。
  - `quadratic_nosvd` Round3 margin 导出为 0。
  - `acp_on` 的比较口径在当前文档中被误当作 baseline。
- **可能的工程原因**：
  - `acp_on` 在 logit 前的额外参数层提高了表达能力；
  - margin logging 口径错误；
  - SI 的 expert-level averaging 掩盖 token-level 差异；
  - 采样顺序偏差。
- **可能的理论原因**：
  - “更确信”不等于“更专一化”；
  - “分开专家”不等于“压紧专家内部子空间”；
  - quadratic 当前可能尚未做真正的二阶去偏。

### 6.4 Hypothesis Update

| ID | Old Status | New Status | Why Updated |
| --- | --- | --- | --- |
| H1 | active | supported | 多个 checkpoint 持续证明单指标会误导 |
| H2 | active | active / partially supported | 方向合理，但还只是 proxy 链条 |
| H3 | active | supported / revised | baseline 与 comparator 的角色已重新划清 |
| H4 | active / core | active / downgraded | 目前没有足够证据支撑“quadratic 必要” |
| H5 | implicit | active | 指标缺陷已经成为主 bottleneck |

## 7. Version Upgrade / Pivot Decision
- **为什么当前子问题可以暂时收束**：
  - 旧的“低秩 = 抗遗忘 = 主线答案”叙事已经不够稳；
  - 最新 checkpoint 已经给出新的 practical anchors；
  - 当前最主要瓶颈已经从“再做更多实验”转为“先修定义与判据”。
- **哪些内容应被冻结为本版本结论**：
  - `center` 是必要条件；
  - specialization 是四维 panel；
  - `linear_running_center` 是当前严格 baseline；
  - `acp_on` 是参数增强 comparator，不是严格 baseline；
  - quadratic 仍是开放方向。
- **哪些问题被明确推翻或暂时搁置**：
  - “只要低秩就更适合 CL”不能再当主结论；
  - “margin 更大就是更专一化”被 `linear_no_center` 反例否定；
  - 旧版过长理论证明暂时不再扩展。
- **下一大版本准备切换到什么问题**：
  - 从“证明 quadratic 很强”切到“定义什么是 CL-friendly routing，并判断 quadratic 是否必要”。
- **这个切换与 North Star 的关系是什么**：
  - 它是回到主问题，而不是偏离主问题。

## 8. Prism Report Sync

### 8.1 Recent Updates
- **Update**：我们把项目主线从“找新 router”收束为“定义 CL-friendly routing”。
  - **Conclusion**：quadratic 现在是开放路线，不是已定主线。
- **Update**：我们修正了 comparator 口径：`linear_running_center` 才是 baseline，`acp_on` 只是参数增强 comparator。
  - **Conclusion**：后续新方法必须先击败 `linear_running_center`；`acp_on` 的作用是帮助理解 mean-direction structure，而不是提供公平 baseline。
- **Update**：我们决定修正“专家低秩性”的定义。
  - **Conclusion**：`ED_comp` 将不再被默认视为最终指标。

### 8.2 Background and Theoretical Critique
- 背景主线应改写为：
  - 我们的目标是 CL；
  - Router 的作用是塑造 expert covariance geometry；
  - 旧故事线的问题在于“specialization / low-rankness / variance routing”都定义不清。
- 旧叙述需要删改：
  - 过多与主线弱相关的长证明；
  - 把 quadratic 写得过早、过满的叙述。

### 8.3 Hypotheses and Mathematical **Modeling**
- 可进入正文：
  - specialization panel
  - `d_tau` 的定义
  - 干扰上界与 forgetting proxy 的桥梁
  - covariance-only setting 下 quadratic 的结构性必要条件
- 保留在 `\idea{}` 中：
  - 更强的 theorem 版本
  - 完整 CL 定理
  - 更复杂的二阶非对角项推广

### 8.4 Empirical Study
- **已完成并可写入正文的实验**：
  - 24L ckpt40000 四模型联合评测
  - 12L ckpt60000 centered-family 联合评测（含 `acp_on` comparator）
  - 12L ckpt70000 centered-family 联合评测（含 `acp_on` comparator）
  - 12L ckpt40000 的 `quadratic_nosvd` 结果
- **仍属于 next sub-iteration 的实验**：
  - `acp_lite @ ckpt40000`
  - frozen-feature quadratic necessity audit
  - Step-0 raw vs debiased quadratic audit
  - 新 low-rank metric 复算

### 8.5 Next Iteration
- 下一轮在 report 中应表述为：
  - “We now test whether quadratic routing is necessary, rather than assuming that it is.”

## 9. Open Problems and Immediate Next Actions
- **最关键未决问题**：我们仍没有一个被固定下来的、真正服务于 CL 的 specialization 定义与主指标。
- **下一轮只做这 1-3 件事**：
  1. 对 `linear_running_center / low_rank / acp_on` 重算 `d_tau_comp`、`r_0.9_comp` 与 NMI/Purity。
  2. 补测 `acp_lite @ ckpt40000`，判断 mean-direction 显式拆分在更公平设定下是否仍有收益。
  3. 做 centered linear vs debiased quadratic 的 no-training discriminative test，并修复 `quadratic_nosvd` Round3 margin 导出。
- **明确暂时不做的事**：
  - 不继续写与主线关系弱的长证明；
  - 不直接把 `acp_on` 当成公平 baseline；
  - 不直接把 quadratic 推成训练主线；
  - 不再把 `ED_comp` 单独当作“专家低秩性”的充分定义。

## 10. Key Insights
- **Insight 1**：真正的问题不是“哪个 router 新”，而是“什么 routing geometry 对 CL 真有用”。
- **Insight 2**：专家低秩性不能只用 `ED` 或 `ED_comp` 来说，必须引入 noise-aware occupancy 的定义。
- **Insight 3**：当前最重要的公平比较是 `linear_running_center` vs `acp_lite` vs debiased quadratic，而不是把 `acp_on` 直接当 baseline。
