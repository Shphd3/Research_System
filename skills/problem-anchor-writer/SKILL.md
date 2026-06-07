---
name: problem-anchor-writer
description: Use when writing or revising a compact research anchor as a decision card: one decision question, physical priors, falsifiable hypotheses, one minimal mathematical model, minimal tests, evidence, claim boundary, and next decision. Use when the user asks to write, polish, audit, shorten, or update an anchor.
metadata:
  short-description: Write compact anchor decision cards
---

# Problem Anchor Writer

Use this skill to write or revise a research anchor.

研究锚点（anchor）不是报告，而是决策卡：它让研究者在 3 分钟内看清正在研究的现象、当前假设、数学对象、最小实验、可证伪结果、证据边界和下一步。

决策问题（decision question）指本轮只裁定的一个问题。核心数学模型（core mathematical model）指能连接物理先验、实验对象和主要指标的最小公式或关系。主要指标（primary metric）指决定本轮判断的第一指标。可证伪条件（falsifier）指什么结果会让假设变弱或需要修改。

First apply `research-progress-core`. If the idea is still conceptually unclear, use `scholar-mode` before writing the anchor.

## Core Rule

锚点必须回答四个审查问题：

1. 是否只有一个决策问题？
2. 是否只有一个核心数学模型？
3. 每个实验是否只回答一个问题？
4. 是否清楚写了支持、削弱、证据不足三类结果？

不要把锚点写成 `detailed.md`、实验协议、会议记录、文献综述、运行手册或实现合同。命令、参数、调试步骤、长表格、原始日志、大范围消融和文献解释都放到锚点外。

## Length Limits

- 主体长度：英文约 600-900 words；如果写中文伴随版，控制在 1200-1800 中文字。
- `Tiny Summary`: at most 8 lines.
- 每节最多 3 条。
- 每条最多 2 行。
- 数学最多 1 个核心分解、1 个机制关系、1 组指标。
- 不加额外章节。

如果写不下，把细节移到 `execution_plan.md`、`summary.md`、`detailed.md`、`05_report_card.md` 或阅读笔记。

## Required Structure

使用这个固定结构：

```markdown
# Anchor Title

## 0. Tiny Summary
## 1. Problem Definition
## 2. Physical Prior
## 3. Hypothesis
## 4. Minimal Mathematical Model
## 5. Minimal Tests
## 6. Falsifiable Outcomes
## 7. Current Evidence
## 8. Claim Boundary And Next Decision
```

不要加额外章节。暂时不做的内容只写进 `Cannot claim` 或 `Next decision` 的一句边界。

## Section Requirements

### 0. Tiny Summary

只写：

```text
Parent problem:
Current subproblem:
Core hypothesis:
Minimal test:
Current boundary:
Next decision:
```

不要展开背景。

### 1. Problem Definition

必须包含：

```text
Parent problem:
Sharper subproblem:
Decision question:
Not in scope:
```

只能有一个 `Decision question`。

### 2. Physical Prior

物理先验（physical prior）指对系统、数据、机制或目标的可反驳直觉。只写 1-3 个。

Use:

```text
P1:
Meaning:
Could be wrong if:
```

不要写泛泛背景。

### 3. Hypothesis

假设（hypothesis）必须能被实验削弱。最多写 3 个。

Use:

```text
H1:
Supported if:
Weakened if:
```

每个假设都必须有可证伪条件。

### 4. Minimal Mathematical Model

只写影响本轮判断的数学。

必须包含：

```text
Objects:
Core decomposition:
Mechanism relation:
Observable metrics:
Falsifier:
```

规则：

- 不写装饰性公式。
- 不定义实验不会测的变量。
- 每个变量都必须对应实现对象。
- 每个公式都必须对应可观测指标。
- 不能导出实验判据的公式必须删除。

推荐形式：

```text
Objects:
h_f = ...
c = ...
r_f = ...
w_e = ...

Model:
h_f = c + r_f
z_{f,e} = w_e^T c + w_e^T r_f

Mechanism:
Collapse risk increases if common-score spread dominates residual-score spread.

Metrics:
common_score_rank, max_load, dominant_persistence, accuracy

Falsifier:
...
```

### 5. Minimal Tests

最多写 3 个主实验。每个实验只回答一个问题。

Use:

```text
Experiment:
Question:
Intervention:
Primary metric:
Supports:
Weakens:
```

不要把支撑性检查写成主实验。

### 6. Falsifiable Outcomes

必须包含：

```text
Supported:
Weakened:
Insufficient evidence:
```

每类最多 3 条。证据不足（insufficient evidence）指结果不能可靠支持或削弱假设。

### 7. Current Evidence

只写已经观察到的证据。不要把解释伪装成证据。

Use:

```text
Observation:
Interpretation:
Boundary:
```

观察（Observation）是直接看到的结果；解释（Interpretation）是它可能意味着什么；边界（Boundary）是解释停止的位置。

### 8. Claim Boundary And Next Decision

必须分开：

```text
Can claim:
Cannot claim:
Next decision:
```

只能有一个下一步决策。

## Deletion Rules

必须删除：

- 和决策问题无关的背景；
- 当前实验不能测的数学变量；
- 没有主要指标的实验；
- 没有可证伪条件的假设；
- 超过一个下一步决策；
- 把 toy setting 直接推广到真实数据的 claim；
- 塞进锚点的实验协议或实现细节。

## Post-Result Update

有结果后更新同一个锚点。只改：

- 当前证据；
- 支持、削弱、证据不足的状态；
- 结论边界；
- 下一步决策；
- `summary.md`、`detailed.md`、图表和可选 `05_report_card.md` 的链接。

长解释放在 `detailed.md`；结果第一阅读入口放在 `summary.md`；给导师快速读的压缩版放在 `05_report_card.md`。

不要创建单独的 `hypotheses/<id>/purpose_card.md`。

## Language And Naming Rules

- Canonical anchors are written in English by default.
- If a Chinese companion is needed, create a separate `<anchor_id>_cn.md`.
- The English anchor is the source of truth unless the user explicitly says the Chinese version is canonical.
- In conversation, define technical terms in Chinese before using English names or abbreviations.
- In the English anchor, define terms in plain English before using labels or abbreviations.
- Do not use labels as substitutes for explanation; write the concrete meaning first.
- Use precise, short bullets.
- Keep equations in `$...$` or `$$...$$`.
- Do not copy project-specific algorithm names, model names, or claims into a new anchor unless they are the actual current object.

## Relationship To Other Skills

- Use `experiment-card-writer` after the anchor identifies the minimal tests.
- Use `handoff-report-writer` only when the user explicitly asks to package existing anchor, `summary.md`, `detailed.md`, and optional `05_report_card.md`.
- Do not update root sync, external collaborator repo sync, graph manifests, commit, or push unless the user explicitly asks.
