# 会议材料

单一当日研究中心的会前讲述默认直接使用当天 `focus.md`。会后记录放在：

```text
daily_research_reports/MMDD/meetings/
  meeting_notes.md
  slide_outline.md
```

只有跨多个 focus、跨研究线或明确要求独立提纲时，才使用：

```text
templates/meeting/meeting_outline_template.md
daily_research_reports/MMDD/meetings/<topic>_meeting_outline_cn.md
```

提纲按主题组织。AI 只提供讲述思路、结论与实验的对应关系和
待补问题；研究者用自己的话完成讲解，AI 再审计证据与边界。它不是
实验流水账，也不是 `summary.md` 或 `detailed.md` 的替代品。

涉及实验结果时，只按“问题—实验—结果—结论—边界—下一步”闭环
讲述。`summary.md` 和 `detailed.md` 仍必须能独立阅读；提纲只引用其中
已经成立的结论和核心证据。

会议材料应优先服务于结论边界：

- 当前可以强说什么；
- 当前只能弱说什么；
- 当前结论不覆盖什么；
- 下一步执行动作要关闭哪个边界。

分支内会议材料默认只保存在当天 meeting 文件夹。只有用户明确要求 handoff、
project sync 或 collaborator sync 时，才复制到项目同步目录。

默认 handoff 位置：

```text
daily_research_reports/MMDD/<topic>/handoff_report.md
daily_research_reports/MMDD/<topic>/<anchor_id>.md
```

显式请求项目或协作者同步时，才使用：

```text
Projects/<project>/<worker>/sync/MMDD_topic/
```

## 会后个人记录

`meeting_notes.md` 用于保存会后诊断和个人判断，不替代正式简报。

```markdown
# 会议记录

## 会议诊断

对方核心判断：

我同意的部分：

我仍然担心：

尚未放松的假设：

1.
2.
3.

## 主线更新

结论变化：

边界变化：

执行动作：

## 个人研究记录

新理解：

待确认问题：

下一步动作：
```
