# [用一个完整问句写本轮要回答的核心问题]

```text
type: meeting_cycle_core_task
task_state: DRAFT / ACTIVE / CLOSED
problem_key: <项目内稳定且不随文件改名变化的问题标识>
focus_role: PRIMARY / SECONDARY
question_state: AWAITING_HUMAN_CONFIRMATION / HUMAN_CONFIRMED
design_state: NOT_REQUIRED / AWAITING_HUMAN_CONFIRMATION / HUMAN_CONFIRMED
result_state: NOT_AVAILABLE / AWAITING_HUMAN_CONFIRMATION / HUMAN_CONFIRMED
cycle_start: YYYY-MM-DD
target_meeting: YYYY-MM-DD / Unknown
active_project: <精确项目路径>
anchor: <精确路径>
protocol: <精确路径或 NOT_YET_WRITTEN>
source_meeting: <精确会议记录路径>
core_experiment_count: 1 / 2 / 3
```

这四个状态互不替代：`task_state` 只说明本轮问题是否活动，`question_state` 只说明
核心问题是否经研究者确认，`design_state` 只说明设计是否确认，`result_state` 只说明
研究者是否确认了结果与边界。Protocol 的草稿/批准状态只由 `protocol.md` 保存，执行的
未开始/运行中/完成/失败状态只由 `detailed.md` 或执行记录保存；Focus 不复制这两类状态。
旧的历史 Focus 不要求自动迁移。

保存为：`daily_research_reports/MMDD/focus_<problem_slug>.md`。这是一个明确命名工作流
从一次组会延续到下一次组会的唯一活动核心任务，不是整个仓库的唯一状态，不是实验账本，
也不是每日研究报告的摘要。多个工作流可以并行存在，但每个工作流内部只能有一个当前问题
和一个下一决策，并须全部登记在 `PROJECTS.md`。日期目录（`MMDD`）取本卡首次创建日期；
上一场组会日期写入 `cycle_start`，下一场目标组会写入 `target_meeting`。同一周期跨日时
不移动文件。

主优先级（`PRIMARY`）与次优先级（`SECONDARY`）只表示当前注意力顺序，不合并问题。
研究问题属于研究者与项目，不属于某一个对话。多个对话可以绑定同一个稳定问题标识
（`problem_key`）并处理不同部分。修改已登记的科研问题前，使用仓库根目录的
`./researchctl context <problem_key> --task "<具体部分>"` 登记当前任务，并在已知时用
`--path` 标记预计涉及的路径。`researchctl` 只提醒同问题或路径重叠，不加锁、不设租约、
不决定所有权；是否需要协调由研究者判断。Focus 不保存 conversation owner。

创建或重置核心任务卡（Focus）必须由研究者明确决定。人工智能不得因为新增实验、对照、
诊断、复现、失败分析、结果解释或报告而创建 Focus。只有研究者明确宣布一个独立核心问题
进入新的组会周期，并确认稳定的 `problem_key` 和唯一下一决策后，才能创建或重置。服务
同一核心问题的工作继续写在本 Focus 中。

正文书写采用 `research-document-explainer` 的讲解规则：先解释研究对象和目的，再写实现；
英文代称、缩写、指标和方法名先用中文定义；使用自然、完整的句子，一句话只承担一个主要
关系；直接证据、解释和推断必须分开。

**本卡只回答四件事：问题是什么、预测什么、什么信息可用、研究者裁决了什么。**
详细的实验四要素与结果四要素分别由 `protocol.md`（执行前）和 `summary.md` /
`summary_cn.md`（执行后）承载；完整轮次记录由 `detailed.md` 承载。本卡不复制它们。

## 1. 核心问题与它的边界

[只写一个可由本轮证据改变判断的问题。先定义不可缺少的英文术语或代号，再用白话表述。
说明它和长期研究方向的关系，但不要把路由器（Router）、专家专门化或其他下游目标写成
本轮已经回答的内容。]

**本轮不回答：** [列出最容易越界的相邻问题。]

## 2. 可证伪的预测与最强竞争解释

[写出预测会出现的关键差异、最强竞争解释，以及什么观察能够区分二者。不要把希望看到的
结果写成已经成立的事实。]

## 3. 允许与禁止的信息

[哪些数据、字段或标签可以进入拟合、降维、聚类、层选择与阈值判断；哪些绝对不能进入，
只能用于最终评分。写明开发/确认的切分边界。]

## 4. 本轮实验（只列，不展开）

- **实验 1：** [白话名] — 目的：[一行]；能分开的结果：[一行] → `protocol`: [路径或 `NOT_YET_WRITTEN`]
- **实验 2 / 3：** [只有共同回答核心问题且确有依赖时才增加，最多三个；否则删除本行]

## 5. 轮次滚动摘要

[由 `detailed.md` 的轮次记录**压缩**而来，一轮一行。完整轮次记录留在 `detailed.md`，
此处不复制。]

| 日期（UTC） | 本轮问题 | 结果或 `NOT RUN` | 认识更新 |
|---|---|---|---|
| | | | |

## 6. 待研究者决定

- [ ] [需要研究者一句话裁决的事项。写事实与待决点，不写猜测的结论。]

## 7. 本轮总结论（研究者完成审计后填写）

- **我的认识更新：** [综合本轮已完成的实验，回答核心问题。]
- **仍不能说：** [最重要的一条边界。]
- **唯一下一决策：** [只能有一个。]

人工智能只核对数字、证据资格和结论边界，不替研究者加强结论。研究者完成本节，且
规范结果摘要（`summary.md` / `summary_cn.md`）与完整证据（`detailed.md`）可以追溯后，
人工智能才写自包含的每日研究报告，供研究者检查实验故事是否自洽。

## 路径

- **实验协议：** [链接；未写时标 `NOT_YET_WRITTEN`]
- **结果摘要：** [`summary.md` / `summary_cn.md`，结果存在后补]
- **完整证据：** [`detailed.md`，结果存在后补]
- **每日研究报告：** [研究者确认结果后再补]
- **待研究问题清单：** [项目级 `main/parking_lot/README.md`]

## 自检（任一命中即 FAIL）

1. 任一状态字段镜像了 `protocol.md` 的批准状态，或 `detailed.md` 的执行状态。
2. 第 4、5 节复制了 `protocol.md`、`summary.md` 或 `detailed.md` 已有的完整内容。
3. 第 7 节由 AI 填写，或把 AI 草稿当作研究者结论。
4. 出现两个或更多「唯一下一决策」。
5. 记录了 conversation owner 或某个对话的名字。
