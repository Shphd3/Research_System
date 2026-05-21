---
name: hypothesis-closure
description: Use when evidence from an experiment, result summary, meeting note, or analysis needs to close or update a hypothesis by writing a concise, self-contained closure from the original hypothesis purpose card, including claim-boundary audit and meeting/sync-ready wording.
metadata:
  short-description: Close research hypotheses
---

# Hypothesis Closure

Use this skill after evidence exists. The closure should answer: what did the
purpose card ask, what did the experiment show, what changed in the claim
boundary, and what should happen next?

Default language is Chinese. Use English only for code identifiers, metric
names, file paths, or quoted terms.

## Required Inputs

Read, in order:

1. `hypotheses/<hypothesis_id>/purpose_card.md`
2. linked `experiments/<experiment_id>/summary.md`
3. `detailed.md` or figures only if needed to audit the conclusion

Do not write a closure only from chat history.

## Location Rule

Write the closure beside the purpose card:

```text
Projects/<project>/main/hypotheses/<hypothesis_id>/hypothesis_closure.md
```

For branch-local work:

```text
Projects/<project>/<worker>/main/hypotheses/<hypothesis_id>/hypothesis_closure.md
```

The experiment folder keeps execution evidence:

```text
experiments/<experiment_id>/summary.md
experiments/<experiment_id>/detailed.md
```

## Closure Template

```markdown
# Hypothesis Closure: <hypothesis_id>

## 1. 目的

这轮实验为什么必须做？它服务于哪个问题层级和下一步决策？

## 2. 假设

H:

Rivals:

## 3. 数学建模

Objects:

Variables:

Expected relation:

Metric decision rule:

## 4. 实验设置

说明 setup 是否真的测试了 H，而不是只测试了弱 proxy。

## 5. 结论

一句话结论。

## 6. 证据

只写改变判断的结果。每条证据要说明它支持什么。

1.
2.
3.

## 7. 结论边界

能说：

不能说：

最弱点：

导师最可能攻击的缺口：missing control / ambiguous metric / weak baseline /
limited data / train-infer mismatch / layer specificity / synthetic-only。

## 8. 下一步决策

继续 / 修改 / 停止 / 换假设，并说明原因。

## 9. 结果文档

summary / detailed / figures / runtime artifacts。
```

## Reporting Sync

After a closure is finished, also decide whether to sync:

- branch-local collaborator sync:
  `Projects/<project>/<worker>/sync/MMDD_topic/`
- project-level collaborator sync, only when shared consensus changes:
  `Projects/<project>/sync/`
- daily reporting brief: `daily_research_reports/MMDD/01_reporting/`
- mainline files: `current_mainline.md`, `consensus.md`, `status.md`
- research graph: `graph.yaml`

For group-meeting preparation, also create a daily reporting card:

```text
daily_research_reports/MMDD/01_reporting/<hypothesis_id>_reporting_card.md
```

This file is the user's meeting-prep surface. Put an empty oral report card at
the top for the user to write in their own words, then include or link the
closure snapshot below. The project-local `hypothesis_closure.md` remains the
source of truth; the daily copy is for fast meeting access.

If the closure uses figures, copy the report-ready figures into a local folder
beside the daily reporting card, for example
`<hypothesis_id>_figures/`, and update image links to that local folder. Do not
use cross-project relative image links from daily reporting cards.

Use this shape:

```markdown
# Reporting Card: <hypothesis_id>

Source closure:
`Projects/<project>/<worker>/main/hypotheses/<hypothesis_id>/hypothesis_closure.md`

## Oral Report Card - Fill Before Meeting

目的：

假设：

结论：

证据：

1.
2.
3.

## Closure Snapshot
```

Do not make the user write another full report for meetings. Closure provides
the logic; the daily reporting card provides the oral script space.

For meeting-facing sync, create a folder named by date and topic, for example:

```text
Projects/from-attention-to-search/XingyuD/sync/0521_router_diagnosis/
  README.md
  report.md
  figures/
```

The sync document should be written from the closure and use the same detailed
research-judgment structure:

```markdown
## 1. 目的
## 2. 假设
## 3. 数学建模
## 4. 实验设置
## 5. 结论
## 6. 证据
## 7. 结论边界
## 8. 下一步决策
## 9. 结果文档
```

`结果文档` should include the artifact / repro map: code workspace, runner,
config, data or manifest, result dir, figure dir, key files, checkpoints or
logs, and repro command.

When figures are central to the claim, copy report-ready figures into the sync
folder's local `figures/` directory and embed them with one-sentence evidence
interpretation.

The sync is not complete if a collaborator can understand the conclusion but
cannot tell where the code, data, outputs, and figures are. Keep the map compact;
do not paste raw logs.

If no sync is needed, write `No sync update` with a one-sentence reason.

## Purpose Card Backfill

After writing `hypothesis_closure.md`, update the original
`purpose_card.md`. This is required.

Backfill:

- `Result`: direct result in one short paragraph.
- `Conclusion`: one-sentence hypothesis decision.
- `Next Step`: next decision.
- `Result Documents`: links to `experiments/<experiment_id>/summary.md`,
  `detailed.md`, important figures, and this `hypothesis_closure.md`.

Do not duplicate long evidence in the purpose card. Link the result documents
and keep the card readable as the hypothesis lifecycle record.

## Rules

- A closure must be self-contained but not long.
- Start from the purpose card; do not rewrite the experiment as a chronology.
- Closure is not complete until the purpose card links the result documents and
  has updated `Result`, `Conclusion`, and `Next Step`.
- Do not upgrade a claim unless the setup directly tests it.
- Always separate public claim, private interpretation, and speculation.
- If the setup only tests a boundary condition, say so.
- Put long tables, commands, and raw logs in `experiments/.../detailed.md`.
- Copy report-ready figures into the closure `figures/` folder when figures are
  needed for explanation.
- Markdown formulas must use `$...$` or `$$...$$`.
