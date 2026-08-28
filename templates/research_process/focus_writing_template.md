# [用一个完整问句写本轮组会要回答的核心问题]

```text
type: meeting_cycle_core_task
status: TASK_DRAFT / HUMAN_CONFIRMED_DESIGN / PROTOCOL_DRAFT_AWAITING_REVIEW / EXECUTION_APPROVED / AWAITING_HUMAN_RESULT / HUMAN_RESULT_CONFIRMED / CYCLE_CLOSED
core_question: AI_DRAFT_AWAITING_HUMAN_CONFIRMATION / HUMAN_CONFIRMED
plain_language_design: AI_DRAFT_AWAITING_HUMAN_CONFIRMATION / AI_REVISED_AWAITING_HUMAN_CONFIRMATION / HUMAN_CONFIRMED
cycle_start: YYYY-MM-DD
target_meeting: YYYY-MM-DD / Unknown
active_project: <精确项目路径>
anchor: <精确路径>
protocol: <精确路径或 NOT_YET_WRITTEN>
source_meeting: <精确会议记录路径>
core_experiment_count: 1 / 2 / 3
```

保存为：`daily_research_reports/MMDD/focus_<problem_slug>.md`。这是一个明确命名
工作流从一次组会延续到下一次组会的唯一活动核心任务，不是整个仓库的唯一状态，
也不是实验账本或 Daily Report 的摘要。多个工作流可以并行存在，但每个工作流
内部只能有一个当前问题和一个下一决策，并须全部登记在 `PROJECTS.md`。`MMDD`
取本卡首次创建日期；上一场组会日期写入 `cycle_start`，下一场目标组会写入
`target_meeting`。同一周期跨日时不移动文件。历史 Focus 不因新格式而迁移。

## 1. 核心问题

[只写一个可由本轮证据改变判断的问题。先定义不可缺少的英文术语或代号，再用
白话表述。说明它和长期研究方向的关系，但不要把 Router、专家专门化或其他
下游目标写成本轮已经回答的内容。]

## 2. 实验目的

[说明本轮要把核心问题解决到什么程度、按依赖关系回答哪些子问题，以及明确的
完成标准。一个核心实验优先，确有必要时最多三个。支持同一结论的对照、稳健性
检查和可信度护栏不另算核心实验。]

**本轮不回答：**[列出最容易越界的相邻问题。]

## 3. 分析方法

只允许一到三条，每条都用白话说明“做什么、比较什么、该比较排除什么解释”。
公式、完整超参数、随机种子、统计细节和运行步骤放在 Protocol。

1. [第一步]
2. [第二步]
3. [仅确有依赖时保留第三步]

## 4. 结论

### 执行前：两种预期结果

- **若支持：**[将观察到什么；它对核心问题允许说明什么；仍不能说明什么。]
- **若不支持或证据不足：**[将观察到什么；应停止、改写还是补哪一个必要条件；
  它如何防止主线继续建立在假象上。]

### 执行后：由研究者完成

- **直接结果：**[不要先写解释。]
- **我的结论：**[研究者自己的认识更新。]
- **仍不能说：**[最重要的一条边界。]
- **唯一下一决策：**[只能有一个。]

AI 只核对数字、证据资格和结论边界，不替研究者加强结论。研究者完成这一节且
canonical `summary.md` / `detailed.md` 可追溯后，AI 才写自包含的
`daily_report_<topic_slug>.md`，供研究者检查实验故事是否自洽。

## 路径

- **Protocol：**[链接；未写时标 `NOT_YET_WRITTEN`]
- **Summary：**[结果存在后补]
- **Detailed：**[结果存在后补]
- **Daily Report：**[研究者完成结果报告后再补]
- **Parking Lot：**[项目级 `main/parking_lot/README.md`]
