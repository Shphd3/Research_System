# [调研]MoE - 迭代状态存档 v6.1

> 本版本的任务不再是继续扩展静态 proxy。  
> 我们现在要回答三件事：  
> 1. 静态 routing geometry 到底已经告诉了我们什么？  
> 2. 哪些结论仍然只是 proxy，不能直接等同于抗遗忘？  
> 3. 下一步应如何用最小 Continual Learning 实验，对 quadratic 做最终判决？

## 0. Checkpoint Metadata
- **项目**：MoE Router for Continual Learning
- **版本**：`v6.1`
- **日期**：2026-03-31
- **当前阶段**：`收束完成 -> 切回 CL 主线 -> 设计 closing follow-up`
- **本次更新触发器**：`12L / ckpt40000 五轮综合结果 + Round3 修正结果 + 理论回写`
- **一句话 North Star**：不是继续寻找“新 router”，而是判断什么样的 routing geometry 真正能减少 catastrophic forgetting。
- **本 checkpoint 的作用域**：冻结当前静态结论，明确 proxy 的边界，并把下一步主实验切换到真正的 Continual Learning 验证。

## 1. Executive Summary
- **当前最强主张**：`acp_lite` 已经成为当前最强的公平静态 comparator；它证明显式 mean-direction buffering 本身就足以带来很强的单点任务表现。
- **当前最大不确定性**：`quadratic_nosvd_debias` 在静态 cross-domain interference 上给出了最低 `SI`，但这是否会兑现成更低 forgetting，尚未被真实 CL 序列证明。
- **本轮相较 v6.0 的核心变化**：
  - `acp_lite` 的完整静态评测已经补齐，并成为当前公平比较中的强基线。
  - Round3 的 `acp_lite` margin 异常已不再作为主结论前提；修正后应以 `SI / downstream / interference` 的整体关系为准。
  - Round4 directional sensitivity 已完成，但应降级为弱机制证据。
  - 主线正式从“静态 necessity 辩论”切到“真实 CL 中 forgetting 能否被降低”的 closing follow-up。

## 2. Stable Knowledge / Report-Ready Claims

| ID | Claim | Evidence Type | Confidence | Can Write to Report? | Notes |
| --- | --- | --- | --- | --- | --- |
| C1 | `center` 是必要条件；`linear_no_center` 会产生 collapse 式高 margin / 高 CR / 高 SI，但这些不是健康 routing | main exp | high | yes | 五轮结果一致支持 |
| C2 | Router 质量是 multi-objective 问题；`downstream avg`、`SI`、`CR`、`load balance` 不能互相替代 | main exp | high | yes | 已有多个反例 |
| C3 | `linear_running_center` 是严格 baseline；`acp_lite` 是当前最强公平 comparator | main exp | high | yes | `acp_lite` 在 `O(Kd)` 级别比较中成立 |
| C4 | `acp_lite` 最擅长静态任务表现与表征复用，但不在 `SI` 上最优 | main exp | high | yes | `Round0` 最优，`Round3` 非最优 |
| C5 | `quadratic_nosvd_debias` 在当前静态分析中给出最低 `SI`，说明它可能更强地压低跨域子空间重叠 | main exp | medium | partial | 仅 `ckpt40000`，尚未转化为 forgetting 证据 |
| C6 | `low SI != best downstream performance`，`high margin != good specialization` | main exp | high | yes | `linear_no_center` 与 `acp_lite / quadratic_debias` 对照已足够 |
| C7 | Round4 directional sensitivity 的 `DSI` 量级极小，应视为弱或近零机制证据 | main exp | medium | partial | 适合 Appendix / Ablation |
| C8 | 静态 proxy 不能单独充当 catastrophic forgetting proof | theory + exp | high | yes | 这是本版本的核心边界条件 |

## 3. Hypothesis

| ID | Hypothesis Statement | Status | Why It Matters | Current Evidence | Blocking Risk |
| --- | --- | --- | --- | --- | --- |
| H1 | 对 CL 有用的 expert specialization 必须由 assignment / compactness / isolation / balance 联合定义 | supported | 定义“好分发” | 静态五轮结果已经足够 | assignment 仍可进一步增强 |
| H2 | 更低 overlap / 更低 SI 可能降低 forgetting，但与静态任务表现存在 trade-off | active / partially supported | 建立 routing geometry 到 CL 的桥梁 | `quadratic_debias` 最低 SI，`acp_lite` 最好任务 | 仍缺真实顺序学习证据 |
| H3 | `linear_running_center` 是严格 baseline，`acp_lite` 是当前最强公平静态 comparator | supported | 防止比较口径错误 | 当前 `ckpt40000` 结果支持 | 仍需更多 checkpoint 外推谨慎 |
| H4 | `quadratic_nosvd_debias` 只有在其低 SI 能真正转化成更低 forgetting 时，才算对 CL 具备结构必要性 | active / narrowed | 这是 quadratic 主线的最终判据 | 目前只看到静态隔离信号，未见 CL 判决 | 可能只是 robustness 路线而非 CL-necessary 路线 |
| H5 | `d_tau_comp` 比 `ED_comp` 更适合做 noise-aware occupancy 指标 | active | 修复低秩性指标缺陷 | 理论上更合理，尚未全量重算 | 需固定 `tau` 并跑完重算 |
| H6 | 静态 proxy 可以筛选候选 router，但不能完成抗遗忘判决 | supported | 解释为什么现在必须切回 CL | 当前所有证据都仍停在 proxy | 若继续只做静态分析会偏题 |

## 4. Mathematical Model
### 4.1 Current Interpretation of the Three Main Routes
- **`linear_running_center`**：
  - 一阶中心化 baseline。
  - 作用：提供最干净、最便宜的 centered routing 基线。

- **`acp_lite`**：
  $$
  \ell_{\mathrm{acp\_lite}}(x) = A x_{\parallel} + B x_c
  $$
  - 作用：显式把 mean-direction 单独暴露给 router。
  - 当前解释：它更像“domain shift buffer”，把全局偏移吸收进独立的一阶分支，因此在静态任务表现上收益最强。

- **`quadratic_nosvd_debias`**：
  $$
  \ell_{\mathrm{quad\_deb}}(x) = W_1 x_c + W_2 (x_c \odot x_c - \lambda_t)
  $$
  - 作用：把逐维二阶偏差暴露给 router。
  - 当前解释：它更像“cross-domain variance isolator”，在静态 proxy 上更倾向于压低跨域重叠，但是否对最终 forgetting 有帮助仍待验证。

### 4.2 What the Static Results Actually Mean
- **`acp_lite` 最好，不等于它最抗遗忘**：
  - 当前只能说明它最擅长静态表征复用与单点任务收益。
- **`quadratic_debias` 最低 SI，不等于它最好**：
  - 当前只能说明它更擅长压低跨域子空间重叠。
- **`linear_no_center` 的高 margin 不是优势**：
  - 这更像未中心化导致的 logit 标量膨胀与单专家主导，而非健康 specialization。

### 4.3 Refined Bridge to Continual Learning
- 设 Task A 与 Task B 在某 expert 内的 routed covariance 分别为
  $$
  C_{e,A},\; C_{e,B}.
  $$
- 当前干扰 proxy 仍为
  $$
  SI_e = \frac{\mathrm{Tr}(C_{e,A}C_{e,B})}{\|C_{e,A}\|_F \|C_{e,B}\|_F}.
  $$
- 低 `SI` 的合理解释是：后续任务更新更可能落在较少重叠的子空间上，因此旧任务被覆盖的风险下降。
- 但这条链条目前仍缺最后一步：
  - `low SI` 是否真的对应更小的 `\Delta Acc(old task)`？
- 因此，本版本正式把“抗遗忘证明”从静态 proxy 切换为真实顺序学习指标。

### 4.4 Main Assumption Now Under Test
- **新的核心假设**：
  > 如果 `quadratic_nosvd_debias` 的低 `SI` 真的代表更强的 anti-interference 结构，那么在最小 sequential CL 设置中，它应当比 `acp_lite` 保留更多旧任务性能。

## 5. Experiment Design

### 5.1 Decision Target
- **本轮 closing follow-up 要区分的 competing explanations**：
  1. `acp_lite` 的一阶 mean-direction buffering 已足够；更低 `SI` 并不会显著减少 forgetting。
  2. `quadratic_nosvd_debias` 的低 `SI` 代表真实的 anti-forgetting structure，因此在顺序学习中能更好保留旧任务。

### 5.2 Minimal CL Follow-up Protocol
- **比较模型**：
  - `linear_running_center`
  - `acp_lite`
  - `quadratic_nosvd_debias`

- **最小任务流**：
  - Sequence 1: `CS -> Medical`
  - Sequence 2: `Medical -> CS`

- **训练与评测点**：
  1. Train on Task A for `N` steps
  2. Evaluate on Task A -> `Acc_A_after_A`
  3. Continue training on Task B for `N` steps
  4. Evaluate on Task A and Task B -> `Acc_A_after_B`, `Acc_B_after_B`

- **核心指标**：
  - **Forgetting on old task**:
    $$
    \Delta Acc_A = Acc_A^{after\ B} - Acc_A^{after\ A}
    $$
    方向：越接近 0 越好
  - **Average retained performance after Task B**:
    $$
    Avg_{after\ B} = \frac{Acc_A^{after\ B} + Acc_B^{after\ B}}{2}
    $$
  - 可选：
    - `BWT`
    - `Forgetting Measure`
    - loss curve stability

### 5.3 Decision Rule

| Outcome Pattern | Interpretation | Hypothesis Update | Next Action |
| --- | --- | --- | --- |
| `quadratic_nosvd_debias` 的 `\Delta Acc_A` 明显更小，且 `Avg_after_B` 不劣化太多 | 低 `SI` 兑现成抗遗忘收益 | H4 support | 保留 quadratic CL 主线，并扩大验证 |
| `acp_lite` 的 forgetting 不差于甚至优于 `quadratic_nosvd_debias` | 低 `SI` 未兑换成真实 CL 优势 | H4 weakened / falsified | 关闭 quadratic necessity 主线，回到 centered + ACP-lite |
| 三者差异不稳定或高度依赖顺序/seed | 当前证据不足 | H4 remains unresolved | 再考虑 TRACE 或更规范 benchmark |

### 5.4 What Not to Do Right Now
- 不再扩展更多静态 proxy。
- 不再新增 router。
- 不直接上大规模全任务 continual learning。
- 不把 Round4 继续升级成主机制叙事。

## 6. Conclusion / Update

### 6.1 New Results Integrated
- `acp_lite` 已成为当前最强的公平静态 comparator。
- `quadratic_nosvd_debias` 在当前静态 Round3 中给出最低 `SI`。
- `Round4` 已完成，但 `DSI` 效应量极小，应降级为 weak evidence。

### 6.2 Interpretation
- 当前结果最支持的解释不是“quadratic 已经赢了”，而是：
  - `acp_lite` 更适合静态任务表现与表征复用；
  - `quadratic_nosvd_debias` 更可能只是在 anti-interference 结构上有潜在价值；
  - 这两个方向可能构成一个 CL 中的 trade-off，而不是单点胜负。

### 6.3 Stable vs Tentative
- **可冻结为稳定结论**：
  - `linear_no_center` collapse；
  - `acp_lite` 是当前公平静态最强 comparator；
  - `low SI != best downstream avg`；
  - static proxy 不能替代 forgetting proof。
- **仍然只是 tentative evidence**：
  - `quadratic_nosvd_debias` 的低 `SI` 是否带来真实 CL 优势；
  - quadratic family 的高噪声稳定性是否在更多 checkpoint 中普遍成立。

### 6.4 Hypothesis Update

| ID | Old Status | New Status | Why Updated |
| --- | --- | --- | --- |
| H2 | active / partially supported | active / narrowed | 现在明确需要真实 forgetting 指标闭环 |
| H4 | active | active / narrowed | 必要性问题从“静态 separability”收缩为“低 SI 是否换来更低 forgetting” |
| H6 | implicit | supported | 静态 proxy 的边界已被明确识别 |

## 7. Version Upgrade / Pivot Decision
- **为什么可以从 v6.0 升到 v6.1**：
  - 静态比较框架已经基本收束；
  - `acp_lite` 的角色已经明确；
  - 下一步主问题已从“解释 proxy”切换到“验证 forgetting”。

- **这次 pivot 的本质**：
  - 从 `proxy-heavy static routing analysis`
  - 切到 `minimal but real continual learning validation`

- **这不是重新开题**：
  - 这是主线回到最初 North Star：Continual Learning。

## 8. Prism Report Sync

### 8.1 Recent Updates
- **Update**：`acp_lite` 已成为当前最强公平静态 comparator。
  - **Conclusion**：显式 mean-direction buffering 是一条真正有效的一阶路线。
- **Update**：`quadratic_nosvd_debias` 在静态 cross-domain interference 上给出最低 `SI`。
  - **Conclusion**：quadratic 的剩余价值更可能体现在 anti-interference，而非单点任务表现。
- **Update**：Round4 directional sensitivity 完成，但效应极弱。
  - **Conclusion**：方向敏感性不是当前主机制。
- **Update**：主线正式切回真实 CL。
  - **Conclusion**：下一步应以 minimal forgetting test 作 closing follow-up。

### 8.2 What Can Enter the Main Report
- `no_center` collapse 结论
- 公平比较下 `acp_lite` 的强表现
- `low SI != best task performance`
- static proxy 与 real CL claim 之间必须区分

### 8.3 What Should Stay in Appendix / Idea
- Round4 directional sensitivity 的细节
- quadratic 的强必要性叙事
- 在真实 forgetting 证据到位之前的任何“最终判决”

## 9. Open Problems and Immediate Next Actions
- **当前唯一关键未决问题**：
  - `quadratic_nosvd_debias` 的低 `SI` 能否转化成真实更低 forgetting？

- **下一步只做这 1-3 件事**：
  1. 设计并运行最小 `Sequential Two-Task Forgetting Test`
  2. 固定比较 `linear_running_center / acp_lite / quadratic_nosvd_debias`
  3. 如果 two-task test 支持 quadratic，再考虑上 TRACE 或更完整 benchmark

- **暂时不做的事**：
  - 不训练新 router
  - 不继续新增静态指标轮次
  - 不把 quadratic 直接推进成主线答案

## 10. Key Insights
- **Insight 1**：`acp_lite` 证明一阶 mean-direction routing 远比原先预期更强。
- **Insight 2**：`quadratic_nosvd_debias` 的价值如果存在，最可能体现在 anti-interference / anti-forgetting，而不是静态任务表现。
- **Insight 3**：你现在真正要测的不是“哪个 router 更漂亮”，而是“哪个 router 更不容易忘”。
