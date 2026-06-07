# 0607-0608 Research Schedule: Collapse Root-Cause Closure Before Monday 13:30 Meeting

> 时间假设：今天是 2026-06-06；“明日”是 2026-06-07；“后日组会”是 2026-06-08 13:30。  
> 目标：在 06-07 24:00 前完成 meeting brief 初版，并让最小实验至少跑起来；06-08 13:30 前完成可汇报的 decision report。

---

## 0. Highest-Level Objective

本次组会不要再讲大故事。只回答一个主问题：

```text
在原始 uniform feature setting 中，为什么线性 top-1 router 仍然 collapse？
是 data/init 实现问题，random geometry finite-sample imbalance，hidden common direction，还是 training-amplified lock-in？
```

周一 13:30 前最低可交付物：

```text
1. code/data/init audit 的 PASS / FAIL / UNCLEAR 初步结论；
2. random geometry baseline 或至少理论 baseline；
3. common-direction residual routing 是否已经跑起 / 初步结果；
4. meeting brief v1：observation -> interpretation -> claim boundary -> next decision。
```

---

## 1. Must-Finish List

### Task A — Paper Reading

```text
目标：完成论文主体阅读，不追求写长笔记。
输出：150-250 字中文 summary + 3 条与当前问题相关/无关的判断。
```

最低完成标准：

```text
- 读完 method / experiments / limitations。
- 写出：这篇论文是否帮助解释 routing collapse / initialization / anti-lockin。
```

### Task B — Monday Closure + Experiment

```text
目标：不要继续 P1/P3/P2；回到 uniform collapse root-cause。
输出：最小实验跑起来；睡前完成 meeting brief 初版。
```

实验优先级：

```text
1. source-code data/init audit；
2. random geometry baseline；
3. common-direction residual routing；
4. 如果 3 来不及，至少输出 full-vs-residual score decomposition。
```

### Task C — Gating Initialization + Anti-Lockin Research

```text
目标：不是泛泛查文献，而是形成 3 个可实验化候选。
输出：每个候选写 mechanism / expected effect / metric / confound。
```

候选列表：

```text
1. zero-bias / row-centered / orthogonal router initialization；
2. common-direction subtraction before routing；
3. early load balance / warmup / delayed hard top-1；
4. optional: forced-routing utility matrix。
```

### Task D — Research Workflow Review

```text
目标：把科研循环重新练熟。
输出：明天睡前写 6 行 review：
problem -> prior -> minimal test -> result -> claim boundary -> next decision。
```

---

## 2. 06-07 Detailed Schedule

### 09:00-09:30 — Wake / Setup

```text
不要直接打开代码乱跑。
先打开这三个文件：
- 05_03_collapse_root_cause_and_antilockin_anchor.md
- 05_03_code_data_init_audit_prompt.md
- 05_03_gating_theory_note.md
```

Output:

```text
写下今天唯一 decision question：
“verified uniform + correct init 后，common-direction residual routing 是否减少 collapse？”
```

### 09:30-10:10 — Research Loop Review

只做一页：

```text
Problem: uniform setting 下为什么 collapse？
Prior: uniform frequency 不等于 hidden zero-mean；linear gate 受 common offset 和 expert responsibility 控制。
Minimal test: data/init audit + random geometry + residual routing。
Claim boundary: 不 claim common 是唯一因果原因。
Next decision: residual routing / init / warmup 三选一。
```

### 10:10-11:20 — Paper Reading Block

目标：完成 paper method / experiments 的阅读。

Output:

```text
paper_note_0607.md:
- 这篇文章的核心机制是什么？
- 它是否提供 gating initialization / anti-lockin 线索？
- 它不能替我们证明什么？
```

### 11:20-12:30 — Code/Data/Init Audit Kickoff

把 `05_03_code_data_init_audit_prompt.md` 交给本地 AI / Codex。

你自己只确认四件事：

```text
1. dataset generator 路径；
2. dataloader shuffle / sampler；
3. router class 和 init；
4. step 0 checkpoint semantics。
```

Output by 12:30:

```text
- audit job 已启动；
- 至少拿到 router W/b init 文件路径；
- 至少确认 data generation script / config。
```

### 12:30-13:10 — Lunch + No New Ideas

只允许整理 checklist，不开新分支。

### 13:10-14:50 — Minimal Experiment Start

硬目标：15:00 前至少让一个实验跑起来。

优先顺序：

```text
Option 1: common-direction residual routing on original bad/recovery seeds
  seeds: 20260522 hard collapse, 20260523 recovery, plus one normal if cheap
  metrics: final max_load, load entropy, target accuracy, early margin

Option 2: if implementation too slow, run full-vs-residual score decomposition only
  checkpoints: 0, 10, 50, final
  output: full load vs residual-only load table

Option 3: if model run impossible, run random geometry baseline
  output: P(max_load >= observed), expected max_load, margin distribution
```

14:50 decision:

```text
If experiment is running:
  leave it running during 15:00-21:00.
If not running:
  reduce scope to random geometry baseline + code audit; do not keep debugging endlessly.
```

### 15:00-21:00 — Low-Control / Background Window

按“有事 / 低可控时间”处理。

允许做：

```text
- 让 experiments 后台跑；
- 每 1-2 小时看一次是否 crash；
- 用手机/纸笔写 meeting brief bullet；
- 不做复杂新实现。
```

Background checklist:

```text
- 记录 crash log；
- 记录 run id；
- 记录 ETA；
- 不加新变量。
```

### 21:00-22:10 — Result Triage

只分三类：

```text
Observation:
  数字 / 图 / crash / audit finding。

Interpretation:
  这支持 common direction、init、training amplification、还是 insufficient evidence？

Claim boundary:
  不能说什么。
```

Output:

```text
results_triage_0607.md
```

### 22:10-23:00 — Meeting Brief v0

结构必须是 decision report，不写时间线。

```text
1. Question
2. Why this question blocks P1/P3/P2
3. What we checked
4. Observation
5. Interpretation
6. Claim boundary
7. Monday decision request
```

v0 最低标准：

```text
即使实验没跑完，也要能汇报：
“我先确认 data/init/random baseline；现在 common-direction intervention 正在跑；
目前能/不能排除的是什么。”
```

### 23:00-23:30 — Gating Init / Anti-Lockin Note

写 3 个候选，不超过一页：

```text
Candidate 1: zero-bias / row-centered / orthogonal router init
- mechanism:
- metric:
- confound:

Candidate 2: common-direction residual routing
- mechanism:
- metric:
- confound:

Candidate 3: early warmup / load balance / delayed hard top-1
- mechanism:
- metric:
- confound:
```

### 23:30-23:50 — Workflow Review

写 6 行：

```text
Problem:
Prior:
Minimal test:
Observation:
Claim boundary:
Next decision:
```

### 23:50-24:00 — Shutdown

```text
- 确认 experiments 是否仍在跑；
- 记录明早第一步；
- 24:00 前睡觉。
```

---

## 3. 06-08 Morning Schedule Before 13:30 Meeting

### 09:00-09:30 — Wake / Check Runs

```text
不要先改代码。
先看：是否完成、是否 crash、是否有 output。
```

### 09:30-10:30 — Final Result Extraction

输出最小表：

| condition | seed | final max load | load entropy | target acc | early dominant lock-in | note |
|---|---|---:|---:|---:|---:|---|
| baseline | 20260522 | | | | | |
| residual routing | 20260522 | | | | | |
| baseline | 20260523 | | | | | |
| residual routing | 20260523 | | | | | |

如果没有 intervention result，改用：

```text
full-vs-residual score decomposition table
random geometry baseline table
code audit verdict table
```

### 10:30-11:30 — Meeting Brief v1

必须写清：

```text
Observation -> supports what -> cannot claim what -> next decision
```

不要写：

```text
“我觉得应该是 common direction。”
```

改写为：

```text
“当前证据支持 common direction 是 strong candidate；
但 causal claim 需要 residual routing intervention。
如果 residual routing 减少 collapse 且 accuracy 保持，才升级 claim。”
```

### 11:30-12:00 — Mentor-Facing 2-Minute Script

固定版本：

```text
老师，这次我把问题收缩回原始 uniform setting，先不继续 P1/P3/P2。
原因是 collapse 已经阻断了 feature-level routing 的解释。

我现在把 root cause 拆成三层：
1. data/init 是否真的 uniform 和随机；
2. random geometry 在 F/E/d 下本来会给多少 finite-sample load imbalance；
3. hidden common direction 和 top-1 training 是否把 early bias 放大成 lock-in。

目前我完成/正在完成的是：...

我今天希望决定的是：下一步优先测 residual routing，还是 initialization/warmup anti-lockin。
```

### 12:00-12:40 — Lunch / No New Experiments

只修 brief，不加实验。

### 12:40-13:10 — Dry Run

检查每句话是否有边界：

```text
- observation: 有数字/图/代码证据
- interpretation: 只解释当前 setting
- claim: 不超过证据
- next decision: 一个实验，不是大 sweep
```

### 13:10-13:25 — Package

准备：

```text
- meeting_brief_v1.md / pdf
- one result table
- one anchor update paragraph
- one next experiment protocol
```

### 13:30 — Meeting

核心目标：

```text
让导师看到你没有猜，而是在回答他要的基础问题：
为什么 uniform + random init 仍会 collapse？
```

---

## 4. Fallback Plan

### If code audit finds a data/init bug

Meeting claim:

```text
我现在不能再解释为模型机制；先修复 baseline，再重复 collapse audit。
```

Next decision:

```text
fixed baseline rerun。
```

### If experiment does not finish

Meeting claim:

```text
当前只能汇报 sanity audit + theory decomposition + running intervention，
不能声称 common direction causal。
```

Next decision:

```text
等 residual routing 完成后再更新 anchor。
```

### If residual routing reduces collapse

Meeting claim:

```text
这支持 common-direction routing shortcut；
但还不能说是唯一原因。
```

Next decision:

```text
扩大到 original 24 seeds 或加入 init/warmup comparison。
```

### If residual routing does not reduce collapse

Meeting claim:

```text
global common component 不足以解释 collapse；
下一步转向 random geometry + top-1 lock-in / initialization。
```

Next decision:

```text
test zero-bias/orthogonal init or delayed hard top-1。
```

---

## 5. Sleep Rule

```text
23:30 后不新增实验变量。
23:50 停止写作。
24:00 前睡觉。
```

原因：

```text
周一 13:30 要汇报的是清楚的 decision report，不是最多的实验数量。
```
