# 科研迭代 Prompts

## 0. 用法

这个文件只做一件事：
**给你快速复制科研 prompt。**

固定科研范式不变：

`Hypothesis -> Mathematical Modeling -> Experiment Design -> Conclusion/Update`

固定协作原则不变：

- 唯一持续记忆源：当前迭代状态存档
- theory agent 最后要更新状态文档里的理论部分
- experiment agent 最后要更新状态文档里的实验部分
- 所有独立公式统一用 `$$ ... $$`

---

## 1. 什么时候用哪个 Prompt

### 1.1 初始开题

适用：
- 新问题刚开始
- 还没有形成稳定主线
- 需要 AI 帮你梳理研究问题、假说和方向

### 1.2 理论推进

适用：
- 已有状态文档
- 想继续和 theory agent 讨论几轮
- 等你判断可以收束时，再让它收束

### 1.3 理论收束为实验设计

适用：
- 已经讨论几轮
- 现在要让 theory agent 输出清晰实验设计

### 1.4 发给实验 Agent

适用：
- 理论端已经收束
- 现在要让 experiment agent 规划并执行实验

### 1.5 实验结束后整理结果

适用：
- 实验跑完
- 需要 experiment agent 输出实验报告并回写状态文档

---

## 2. 初始开题 Prompt

```text
我现在要开启一个新的科研问题讨论。请你作为一名严谨的计算数学与深度学习研究员，帮助我梳理问题，并严格按照：
Hypothesis -> Mathematical Modeling -> Experiment Design -> Conclusion/Update
的范式推进。

【1. 核心背景与符号定义】
- 领域：[填写领域]
- 具体问题：[一句话概括问题]
- 符号约定：[填写当前使用的核心符号]

【2. 现状与已知结果】
- 经典/前沿方法：[业界通常怎么做]
- 我的已有实验/发现：[已有观察、数据或现象]

【3. 痛点与瓶颈】
- 当前困境：[现有方案的缺陷]

【4. 我的直觉与初步假设】
- 核心猜想：[你的直觉]
- 支撑依据：[为什么有这个直觉]

【5. 目标与期望】
- 短期目标：[当前最想完成什么]
- 终极目标：[更大的研究目标]

【6. 约束与假设条件】
- 必须满足的前提：[复杂度、兼容性、工程约束等]

【7. 请你执行的任务】
1. 顺着我的直觉，用严谨的数学语言重写我的问题与假说。
2. 指出我这个问题设置中最可能的理论漏洞、定义漏洞或工程漏洞。
3. 帮我提出 2-3 个更清晰、更可推进的子问题。
4. 如果当前信息足够，请给出一个最小实验方向；如果不够，请明确还缺什么。

输出要求：
1. Hypothesis
2. Mathematical Modeling
3. Experiment Design
4. Conclusion/Update
5. 最后额外给我一个：Single Decision Question
```

---

## 3. Theory Agent Prompt

```text
我现在继续当前主线，而不是重新开题。

下面是当前迭代状态文档，请先阅读：
[上传或粘贴当前迭代状态文档]

本轮 focus：
- 当前主线：[一句话]
- 这轮唯一想推进的问题：[一句话]
- 这轮不要发散到：[一句话]
- 这轮希望最后收束成：[一句话]

请先和我继续讨论，严格按：
Hypothesis -> Mathematical Modeling -> Experiment Design -> Conclusion/Update

要求：
1. 先帮我把问题讲清楚，不要急着过早收束。
2. 如果你判断还不该收束，请继续讨论定义、假说、建模和可能的实验。
3. 如果你判断已经可以收束，请明确告诉我，并直接：
   - 给出本轮实验设计
   - 更新迭代状态文档里的理论部分

请始终围绕当前主线，不要重新发明新的大题。
```

---

## 4. Theory 收束 Prompt

```text
我们刚才已经讨论了几轮。现在请你不要继续发散，而是开始收束。

请严格按：
Hypothesis -> Mathematical Modeling -> Experiment Design -> Conclusion/Update
把当前讨论收束成一个可执行版本。

要求：
1. 明确本轮唯一的 Single Decision Question。
2. 明确当前支持的假说、待证的假说、不能过度宣称的部分。
3. 给出一个最小实验设计，而不是一组松散想法。
4. 直接更新迭代状态文档中的：
   - Current Mainline
   - This-Round Focus
   - Experiment Handoff Block

输出时请额外单独给我：
1. 实验目标
2. 实验具体步骤
3. 预期结果
4. 什么结果会支持 / 削弱 / 否定当前假说
```

---

## 5. Experiment Agent Prompt

```text
我现在要执行当前这一轮实验。

下面是当前迭代状态文档，请先阅读：
[上传或粘贴当前迭代状态文档]

下面是本轮已经由理论端收束好的实验设计：
[粘贴当前轮实验设计]

执行信息如下：
- Code directory: [路径]
- Data directory: [路径]
- Checkpoint / model path: [路径]
- Output directory: [路径]
- Existing scripts / framework to reuse: [路径]
- Hard boundaries:
  1. [不能改什么]
  2. [不能改什么]
  3. [不能改什么]

请先不要直接开跑，而是先输出一份完整实验方案，至少包含：
1. 实验目标：这轮实验验证什么假说
2. 实验具体步骤：具体做什么，先后顺序是什么
3. 结果产物：表格、图、json、markdown 各输出到哪里
4. 风险与阻塞点

只有当你确认：
Protocol locked, ready for execution
之后，才进入正式执行。

执行完成后，请直接更新迭代状态文档中的 Experiment Return，内容必须包括：
1. 实验目标
2. 实验具体步骤
3. 实验结果
4. 实验结果分析
5. 更新了什么假设
```

---

## 6. Experiment 结果整理 Prompt

```text
现在实验已经完成。请你不要继续执行新实验，而是整理这轮结果，并直接更新迭代状态文档中的 Experiment Return。

请严格按以下结构输出：
1. 实验目标
2. 实验具体步骤
3. 实验结果
4. 实验结果分析
5. 更新了什么假设

要求：
- 结果要结构化，不要只给日志
- 要明确哪些结果可靠，哪些结果需要谨慎解释
- 要明确这些结果支持 / 削弱 / 否定了什么
- 最后直接给出可回写状态文档的版本
```

---

## 7. 最简工作流

1. 上传状态文档给 theory agent
2. 讨论几轮
3. 你判断可以收束时，用“Theory 收束 Prompt”
4. 再把状态文档 + 实验设计发给 experiment agent
5. 实验完成后，让它直接更新状态文档里的 `Experiment Return`

一句话版：

**先围绕状态文档和 theory agent 把问题讲清楚，再收束出实验设计；然后把状态文档和实验设计交给 experiment agent 执行，最后让它把结果写回状态文档。**
