# Continual Learning 评测调研与执行建议

## 1. 目标
你现在的问题不是缺更多静态指标，而是缺一套**权威、标准、能直接执行**的 Continual Learning 评测协议，用来判断：

- 哪个 router 更不容易忘旧任务
- `low SI / low overlap` 是否真的兑现成更低 forgetting
- `quadratic_nosvd_debias` 是否只是在 proxy 上漂亮，还是对 CL 真有帮助

## 2. 标准 CL 指标

### 2.1 Accuracy Matrix
先定义标准矩阵：
$$
R_{i,j}
$$
表示：训练到第 `i` 个任务后，在第 `j` 个任务测试集上的表现。

这是后面所有指标的基础。

### 2.2 Average Accuracy
训练到最后一个任务 `T` 后：
$$
ACC = \frac{1}{T}\sum_{j=1}^{T} R_{T,j}
$$

- 含义：最终整体表现
- 优点：最直观
- 缺点：看不出忘了多少

### 2.3 Backward Transfer (BWT)
标准形式：
$$
BWT = \frac{1}{T-1}\sum_{j=1}^{T-1}(R_{T,j} - R_{j,j})
$$

- 含义：后续学习对旧任务的影响
- 通常在 forgetting 情况下为负
- 越大越好

### 2.4 Forgetting Measure
常见形式：
$$
F_j = \max_{k \in \{j,\dots,T-1\}} R_{k,j} - R_{T,j}
$$
$$
F = \frac{1}{T-1}\sum_{j=1}^{T-1} F_j
$$

- 含义：每个旧任务从历史最好点掉了多少
- 越小越好
- 这是最直接的 catastrophic forgetting 指标之一

### 2.5 Forward Transfer (FWT)
标准形式之一：
$$
FWT = \frac{1}{T-1}\sum_{j=2}^{T}(R_{j-1,j} - b_j)
$$
其中 `b_j` 是未见该任务时的基线表现。

- 含义：过去任务是否帮助未来任务
- 对你当前问题不是第一优先级

## 3. 对你当前课题最重要的指标组合
如果你现在是验证 router 对抗遗忘有没有帮助，我建议优先只看下面四个：

1. `Acc_A_after_A`
2. `Acc_A_after_B`
3. `ΔAcc_A = Acc_A_after_B - Acc_A_after_A`
4. `ACC_final` 或 `Avg_after_B`

对应关系：

- `ΔAcc_A`：最直接看 forgetting
- `ACC_final`：看最终总收益
- 如果资源允许，再补：
  - `BWT`
  - `F`

对你当前阶段，这样已经足够权威、也足够可执行。

## 4. 最小可执行协议

### 4.1 为什么先做 two-task
你现在模型是自己改过的，工程不一定和现成 benchmark 完全兼容。  
所以第一阶段最稳的方案不是直接上大 benchmark，而是：

- 先做一个 **two-task sequential forgetting test**
- 先把协议、指标、日志、结果表跑通
- 再决定是否扩大到 TRACE

### 4.2 推荐的最小协议
- 比较模型：
  - `linear_running_center`
  - `acp_lite`
  - `quadratic_nosvd_debias`

- 任务顺序：
  - `CS -> Medical`
  - `Medical -> CS`

- 每个顺序都记录：
  1. `Acc_A_after_A`
  2. `Acc_A_after_B`
  3. `Acc_B_after_B`
  4. `ΔAcc_A`
  5. `Avg_after_B`

- 最好再补：
  - 3 个 random seeds
  - loss curve
  - train/eval sample counts

### 4.3 决策规则
- 若 `quadratic_nosvd_debias` 的 `ΔAcc_A` 显著更接近 0：
  - 支持“低 SI 兑现成抗遗忘”
- 若 `acp_lite` 不差甚至更好：
  - 削弱或证伪 quadratic 的 CL necessity
- 若两边差异很小：
  - 说明静态 proxy 没有转化成明显 CL 优势

## 5. TRACE 是否值得做

### 5.1 结论
**值得，但应作为第二阶段，而不是第一步。**

### 5.2 为什么
TRACE 是一个面向 LLM continual learning 的综合 benchmark，包含多种高挑战数据，并且仓库里已经给出顺序训练与推理脚本。  
它适合作为：

- 第二阶段外部 benchmark
- stronger validation
- 对外报告时更有说服力的标准化实验

但它不适合作为你当前第一步，因为：

- 你的模型是改过 router 的自定义模型
- 直接接 TRACE 可能要改训练、数据、推理、评估接口
- 如果 two-task sanity test 都没有支持 quadratic，你没必要先花大资源接 TRACE

### 5.3 什么时候上 TRACE
建议满足以下任一条件再上：

1. two-task sequential test 支持 `quadratic_nosvd_debias`
2. 你需要一个外部 benchmark 来增强论文说服力
3. 集群资源充足，且工程接口已经打通

### 5.4 如果要做 TRACE，先确认三件事
1. 你的模型训练入口是否能适配其 sequential training protocol
2. 你的 tokenizer / model loading / checkpoint saving 是否兼容
3. 你是否只先挑其中 2-3 个子任务做轻量验证，而不是全量一口气跑完

## 6. 给 Agent 的建议口径
你现在最适合交给 Agent 的，不是“请做 CL benchmark”，而是：

- 先做最小 two-task forgetting test
- 输出标准 accuracy matrix
- 自动计算 `ACC / BWT / Forgetting / ΔAcc`
- 如果协议跑通，再评估 TRACE 接入成本

## 7. 现阶段推荐路线

### Phase 1
- 最小 two-task CL sanity test
- 回答：`low SI` 是否真的换来更低 forgetting

### Phase 2
- 如果支持 quadratic，再上 TRACE 或类似标准 benchmark

### Phase 3
- 如果 TRACE 也支持，再把 quadratic 重新抬升为 CL 主线

## 8. 你现在应该怎么用这份文档
- 把本文件交给理论 AI 或实验 AI 做协议收束
- 把 `v6.1` 交给 Agent 作为新 checkpoint
- 下一条实验指令只围绕：
  - `two-task sequential forgetting`
  - `ACC / BWT / Forgetting / ΔAcc`
  - `linear_running_center / acp_lite / quadratic_nosvd_debias`

## 9. 参考
- Continuum 指标文档：实现了 `accuracy`、`backward_transfer`、`forward_transfer`、`forgetting` 等常用 CL 指标，并给出 logger 用法。
- TRACE benchmark：一个面向 LLM continual learning 的综合 benchmark，包含顺序训练与推理脚本，适合第二阶段外部验证。
