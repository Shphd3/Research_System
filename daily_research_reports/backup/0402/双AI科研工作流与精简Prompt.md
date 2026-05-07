# 双AI科研工作流与精简 Prompt

## 目标

把你和两个 AI 的协作，从“每轮临时组织语言”变成“固定输入包 + 固定输出包”的流程。

核心原则只有一句：

`理论 AI 负责收缩问题，实验 AI 负责执行问题，用户只维护唯一 checkpoint 和三种标准卡片。`

---

## 一、你真正需要的三个包

以后不要给实验 AI 一整段聊天记录。

你只维护三种标准包：

1. `Theory Pack`
2. `Experiment Pack`
3. `Result Pack`

这三个包分别对应：

1. 理论讨论收束后，发给实验 AI 的执行输入
2. 实验运行前，实验 AI 自己锁协议用的执行包
3. 实验完成后，实验 AI 回给理论 AI 的结果包

---

## 二、推荐工作流

### Step 1：先和理论 AI 多轮讨论

这一步允许你自由讨论，但目标不是“聊得深入”，而是最终收束出一个 `Theory Pack`。

理论对话结束的唯一完成标准：

- 当前问题被压缩成一句话
- 当前目标假说只剩 1-2 条
- 最小实验被定义清楚
- 指标和 decision rule 明确
- 产出一张标准 `Theory -> Experiment Card`

如果没有这张卡，就不进入实验阶段。

### Step 2：把理论讨论收束成 `Theory Pack`

`Theory Pack` 必须包含 6 块信息：

1. `Checkpoint Snapshot`
   - 当前主线问题
   - 当前已知结论
   - 当前开放假说

2. `Discussion Distillate`
   - 理论 AI 多轮讨论后新增的关键认识
   - 只保留 3-6 条
   - 不保留聊天过程

3. `Target Experiment`
   - 这一轮实验到底要回答什么

4. `Metrics and Decision Rule`
   - 指标定义
   - support / falsify / unclear 规则

5. `Implementation Constraints`
   - 模型路径
   - checkpoint
   - 脚本目录
   - 输出目录
   - 必须沿用的旧框架

6. `Theory -> Experiment Card`
   - 给实验 AI 的最小交接卡

### Step 3：实验 AI 先生成 `Experiment Pack`

实验 AI 不应该拿到理论包就立刻跑。

它先要输出一个 `Experiment Pack`，作用是锁定：

- 它理解的任务
- 它要改什么代码
- 它要产出什么文件
- 它怎么保证和理论定义一致
- 哪些地方可能跑偏

你看过这个包，确认没有 drift，再让它执行。

### Step 4：实验 AI 执行并产出 `Result Pack`

实验结束后，实验 AI 不应该只给你日志和表格。

它要统一整理成一个 `Result Pack`，至少包含：

1. 实际跑了什么
2. 核心结果表
3. 异常检查
4. 假说更新建议
5. 建议回写 checkpoint 的增量

### Step 5：把 `Result Pack` 发给理论 AI

理论 AI 这时不再重新开题，只做三件事：

1. 更新假说状态
2. 更新 checkpoint
3. 决定下一步是：
   - 继续补实验
   - 进入下一子迭代
   - 或者停止某条线

---

## 三、你以后不要再即时拼装 prompt

你真正要做的不是“每次重新写 prompt”，而是固定 4 个模板。

### 模板 A：发给理论 AI 的讨论开局 prompt

用途：
- 开始新一轮理论讨论
- 允许多轮来回
- 但要求最后收束出 `Theory Pack`

```text
我们现在开始一轮新的理论讨论。目标不是立刻写代码，而是把当前问题收束成一个可以交给实验 AI 的执行包。

附上当前 checkpoint：
[贴相关部分]

本轮我真正想推进的问题是：
[一句话问题]

请按以下顺序推进：
1. Current Problem
2. State Classification
3. Hypothesis
4. Mathematical Modeling
5. Minimal Experiment

这次允许多轮讨论，但当你认为问题已经收束后，必须额外输出：

## Theory Pack
- Checkpoint Snapshot
- Discussion Distillate
- Target Experiment
- Metrics and Decision Rule
- Known Risks

## Theory -> Experiment Card
- Current problem
- Target hypothesis
- Minimal mathematical definition
- Minimal experiment
- Metrics
- Decision rule
- Implementation constraints
```

### 模板 B：发给实验 AI 的执行开局 prompt

用途：
- 理论讨论结束后
- 把完整但浓缩过的信息交给“完全不知道你们聊了什么”的实验 AI

```text
下面是当前这一轮实验的完整执行输入。请不要重新定义研究问题，也不要要求我重复背景。你的任务是先锁定执行协议，再开始实现。

[贴 Theory Pack]
[贴 Theory -> Experiment Card]

附加工程信息：
- 代码目录：
- checkpoint：
- 模型列表：
- 输出目录：
- 必须沿用的旧框架：

请先输出：

## Experiment Pack
1. Task Restatement
2. Implementation Plan
3. Protocol Lock
4. Output Contract
5. Risk Check
6. Execution Checklist

只有在 `Protocol locked, ready for execution` 后，才进入正式执行。
```

### 模板 C：发给实验 AI 的结果整理 prompt

用途：
- 实验完成后
- 强制实验 AI 形成标准结果包

```text
实验已经完成。现在不要继续跑新实验，也不要重新讨论理论。请进入结果整理模式。

附上：
- 运行日志 / 输出表 / json / 图
- 当前 Theory Pack

请严格输出：

## Result Pack
1. What was actually run
2. Core result table
3. Reliability / anomaly audit
4. Theory-implementation mismatch
5. Hypothesis update suggestion
6. Recommended checkpoint delta
7. Report-ready summary

最后必须额外输出：

## Experiment -> Theory Card
- What was actually run
- Key findings
- Reliability grade
- support / falsify / unclear
- What should be written back to checkpoint
- Immediate next action
```

### 模板 D：发给理论 AI 的结果回写 prompt

用途：
- 拿实验结果回到理论侧
- 不重新开题，只做收束

```text
下面是本轮实验完成后的标准结果包。请不要重新发散讨论，而是进入理论回写模式。

[贴 checkpoint 相关部分]
[贴 Result Pack]
[贴 Experiment -> Theory Card]

请严格输出：
1. Hypothesis Update
2. Mathematical Interpretation
3. Checkpoint Delta
4. Next-Step Decision

最后补一个：
## Minimal Theory Decision
- What is established
- What remains unresolved
- What should be done next
```

---

## 四、实验 AI 为什么总“失忆”

不是它真的失忆，而是你给它的输入经常混了三层东西：

1. 长聊天记录
2. 当前任务
3. 工程约束

实验 AI 最怕这种输入，因为它会自己重建上下文，然后很容易 drift。

所以以后给实验 AI 时，永远只给：

1. `Theory Pack`
2. `Theory -> Experiment Card`
3. 附加工程信息

不要直接给：

- 多轮理论聊天全文
- 过时版本 checkpoint
- 模糊的自然语言愿望

---

## 五、你最该简化的不是内容，而是“每轮固定栏目”

你以后每轮实验，固定只维护下面这些栏目。

### 给实验 AI 的输入固定栏目

1. `Current Problem`
2. `Why This Matters`
3. `Target Hypothesis`
4. `Minimal Experiment`
5. `Metrics`
6. `Decision Rule`
7. `Implementation Constraints`
8. `Expected Deliverables`

### 实验 AI 回传固定栏目

1. `Actual Run`
2. `Core Table`
3. `Reliability`
4. `Mismatch`
5. `Hypothesis Suggestion`
6. `Checkpoint Delta`

只要栏目固定，你就不需要每次重新组织语言。

---

## 六、推荐你立刻做的 prompt 简化

把你现在复杂的实验 prompt 压成下面这个骨架。

### 简化后的实验执行 prompt 骨架

```text
你现在是实验 AI。不要重新定义问题。

## Current Problem
[一句话]

## Target Hypothesis
[一句话]

## Minimal Experiment
[一句话]

## Metrics
- metric 1:
- metric 2:

## Decision Rule
- if A -> support
- if B -> falsify
- else -> unclear

## Implementation Constraints
- code dir:
- checkpoint:
- model list:
- output dir:
- reuse:

## Your task
先输出 Experiment Pack，再执行，不要跳过协议锁定。
```

这比你现在很多“即时性 prompt”稳定得多。

---

## 七、推荐你立刻新增的两个固定文档

为了进一步提效，我建议你每轮都新增两个文件，而不是把信息散在对话里。

### 1. `theory_pack.md`

这个文件由你和理论 AI 讨论结束后产出。

固定结构：

- Current Problem
- Why This Matters
- Current Best Explanation
- Target Hypothesis
- Minimal Mathematical Definition
- Minimal Experiment
- Metrics
- Decision Rule
- Known Risks
- Implementation Constraints

### 2. `result_pack.md`

这个文件由实验 AI 在实验结束后产出。

固定结构：

- What Was Actually Run
- Output Paths
- Core Result Table
- Reliability Audit
- Theory-Implementation Mismatch
- Hypothesis Update Suggestion
- Checkpoint Delta
- Report-Ready Summary

---

## 八、最简执行建议

如果你现在就想提高生产力，不要先大改所有旧 prompt。

直接从今天开始只做三件事：

1. 理论讨论结束后，强制产出 `theory_pack.md`
2. 实验结束后，强制产出 `result_pack.md`
3. 只用 4 个固定模板，不再临场写 prompt

这会比继续堆更多 prompt 更有效。

---

## 九、你现在最适合的下一步

下一轮你可以直接这样跑：

1. 和理论 AI 继续深入讨论
2. 让它最后输出 `Theory Pack`
3. 把 `Theory Pack` 发给实验 AI
4. 让实验 AI 先输出 `Experiment Pack`
5. 跑完后输出 `Result Pack`
6. 再把 `Result Pack` 发回理论 AI

这个流程稳定后，你的即时 prompt 需求会大幅下降。
