# 0518 Mainline Analysis Packages

## 一句话结论

当前主线应被重写为两个可验证问题：

1. **Gating 主线**：在新 oracle-MoE 形式下，router 的分类边界到底由 routed representation 的哪些结构决定；目标不是再证明 feature 可线性读出，而是解释“为什么当前路由分区是一个低损失分区”。
2. **Reverse Index 主线**：MoE bucket 是否能作为 KV index，关键条件不是 one-feature-one-expert，而是 `高 attention mass 的历史 KV 是否会落入 query 选择的候选 bucket`；必须用 NTP loss / attention mass / output reconstruction / latency proxy 分开验证。

## 当前模型定义

新模型设置需要严格区分两条输入流：

```text
x_t / h_t: expert computation input，保持原始 hidden/residual 表征，不做简化。
z_t = AttnOut_t: router/gating input，用 attention 输出做分发。
e_t = Gate(z_t): expert id 或 top-k expert set。
y_t = Expert_{e_t}(h_t): expert 对原始 hidden 表征做计算。
```

这点是代码审计的第一优先级：**gate input 可以变，但 expert input 不能跟着被简化**。否则实验测到的是“被简化输入的 expert 能否预测”，不是“attention-informed routing 能否分发”。

## 包结构

```text
gating_mainline/
  mainline_analysis.md
  purpose_cards.md
  experiment_cards.md
  reliability_checklist.md
reverse_index_mainline/
  mainline_analysis.md
  purpose_cards.md
  experiment_cards.md
  reliability_checklist.md
meeting_report/
  logic_audit_and_correct_derivation.md
  todo_hierarchy_and_report_scope.md
  inhibition_logic_note.md
source_index.md
```

## 最重要的 claim boundary

可以说：在 controlled synthetic setting 中，feature representation 可分、监督路由可 clean，但当前证据还没有证明 learned routing bucket 能成为有用 KV reverse index。

不能说：MoE router 没有语义、reverse index 不可能、H-MoE 无效、inhibition 一定能解决 specialization。
