# [一个稳定、可改变判断的研究问题]

```text
problem_key: <稳定问题标识>
task_state: DRAFT / ACTIVE / CLOSED
question_state: AWAITING_HUMAN_CONFIRMATION / HUMAN_CONFIRMED
design_state: NOT_REQUIRED / AWAITING_HUMAN_CONFIRMATION / HUMAN_CONFIRMED
result_state: NOT_AVAILABLE / AWAITING_HUMAN_CONFIRMATION / HUMAN_CONFIRMED
```

保存到首次创建日期的 `daily_research_reports/MMDD/focus_<problem>.md`；
同一问题跨日、跨组会、跨对话原位维护。每个活动工作流只在 `PROJECTS.md`
指定一个当前 Focus；语言伴随不算第二个。独立工作流可以各有自己的 Focus。

只有研究者确认独立问题及唯一下一决定，才创建或重置；新实验、模型切换或
准备汇报不触发创建。旧记录不强制迁移，历史问题不因整理被关闭。
状态不镜像 Protocol 批准或 Detailed 执行；未知判断保留 Unknown。

## 当前问题与边界

[具体研究对象、当前未知，以及它为什么服务于长期问题。
用一句话说清本轮不能回答的相邻问题。]

## 候选解释与区分依据

[当前判断及理由、最有力的竞争解释、什么观察能区分。
合格支持、合格不支持和证据不足分别怎样改变判断；已经证明的恒等式不硬造竞争解释。
只给必要的白话比较，通常一个实验；确有必要时最多三个。
精确设置、允许信息、数据切分和阈值链接到 Anchor/Protocol，不在此重复。]

## 研究者认识与唯一下一决定

**已确认的认识更新：** [没有确认就写 Unknown；AI可列事实来源，不代填科学裁决。]

**仍不能说：** [最重要的结论边界。]

**唯一下一决定：** [一个需研究者决定的科学选择；未确认的方案标“AI建议”。]

## 证据入口

- **设计：** [Anchor；Protocol按需链接]
- **当前结果：** [Summary / 中文伴随；Detailed按需追溯]

Focus不保存完整四要素、数值表、轮次账本或讲稿；这些分别由Protocol、
Summary、Detailed和组会短稿持有。无新证据时不重写状态。
请求汇报时使用 `MMDD/docs/meeting_brief_<topic>[_cn].md`，
不创建 `focus_meeting_*`，也不要求先得到新实验结果。
