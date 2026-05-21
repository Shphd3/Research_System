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

## 1. 原始问题层级与目的

从 purpose card 压缩：这轮原本要判定什么？

## 2. 待判定假设

H:

Rivals:

## 3. 实验设置是否有效

说明 setup 是否真的测试了 H，而不是只测试了弱 proxy。

## 4. 直接结果

只写改变判断的结果，不写流水账。

## 5. 解释

Result -> Interpretation -> Boundary.

## 6. Claim Update

支持：

削弱：

仍不清楚：

不能说：

Public wording:

Private speculation:

## 7. 最弱点

导师最可能攻击的缺口：missing control / ambiguous metric / weak baseline /
limited data / train-infer mismatch / layer specificity / synthetic-only。

## 8. 下一步决定

继续 / 修改 / 停止 / 换假设，并说明原因。

## 9. 30s Explanation / Sync Version

一句话目的 + 结果 + 边界 + 下一步。
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

For meeting-facing sync, create a folder named by date and topic, for example:

```text
Projects/from-attention-to-search/XingyuD/sync/0521_router_diagnosis/
  README.md
  report.md
  figures/
```

The sync document should be written from the closure and contain only:

- purpose and hypothesis;
- result and interpretation;
- key figure(s) with one-sentence evidence interpretation when figures are
  central to the claim;
- claim boundary;
- weakest point;
- next decision;
- artifact / repro map: code workspace, runner, config, data or manifest,
  result dir, figure dir, key files, checkpoints or logs, and repro command;
- 30s / 1min explanation when useful.

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
