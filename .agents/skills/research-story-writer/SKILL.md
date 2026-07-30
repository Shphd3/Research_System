---
name: research-story-writer
description: "Write or revise a research-line story that synthesizes its problem, mechanism, mathematical and theorem state, evidence chain, claim boundary, and next anchor decomposition. Use for explicit line-level synthesis, story revision, or paper-like stage synthesis. Do not replace anchors, protocols, result records, or routine meeting notes."
---

# Research Story Writer

Use this skill to write or revise a research-line-level story. A story is a
living total document for one research line. It can be prospective,
retrospective, or synthesis-mode, but it must not replace anchors, protocols,
summaries, or detailed records.

## Core Rule

Use the normal research system:

```text
story -> anchors -> protocol / summary / detailed
```

Use story for the research-line argument. Use anchors for adjudicable nodes.
Use protocol, summary, and detailed for experiment execution and evidence.

Do not create a routine `final_report` layer. If the user asks for a final or
paper-like report, switch the story to synthesis mode unless the user
explicitly asks for a separate export.

## Required Reading

Before writing:

1. Read repository `AGENTS.md` and `PROJECTS.md`.
2. Read the line README and current story if one exists.
3. Read relevant anchors.
4. Read relevant protocols, summaries, detailed records, human-completed meeting outlines, and
   old story drafts.
5. Do not rely on chat history as the source of truth.

## File Placement

Prefer:

```text
Projects/<project>/main/stories/README.md
Projects/<project>/main/stories/<line_id>/README.md
Projects/<project>/main/stories/<line_id>/<NN>_<topic>.md
Projects/<project>/main/stories/<line_id>/<NN>_<topic>_cn.md
Projects/<project>/main/stories/<line_id>/anchor_threads/<anchor_id>/story_fragment.md
Projects/<project>/main/stories/<line_id>/archive/<snapshot_id>/<snapshot_id>.md
Projects/<project>/main/stories/<line_id>/archive/<snapshot_id>/<snapshot_id>_cn.md
```

Rules:

1. Do not create new generic `story.md` or `story_cn.md` files. Active story
   names use `<NN>_<topic>.md`, where `NN` is a two-digit reading-order number
   and `topic` states the document's actual subject.
2. A research line may contain multiple stories only when their scopes are
   genuinely different. The line `README.md` must provide the ordered registry
   and designate exactly one current primary synthesis.
3. Formal stories are bilingual by default. The English canonical file and
   Chinese companion use the same stem, with `_cn.md` added only to the Chinese
   file. Keep question, theorem state, evidence, boundary, and next decision
   synchronized. Do not promote an older Chinese snapshot as a companion when
   its argument differs from the current English story.
4. Historical snapshot filenames repeat the full snapshot-folder identifier so
   that the file remains identifiable when copied out of its directory.
5. Do not write one full story per anchor.
6. Use `anchor_threads/<anchor_id>/story_fragment.md` for anchor-specific
   narrative fragments.
7. Do not automatically update graph, root sync, commit, or push.

## Story Modes

Use prospective mode for a new research line, retrospective mode when anchors
and experiment results already exist, and synthesis mode when a stage is stable
and the user wants a group-meeting or paper-like summary.

## Story Structure

Use this structure unless the user asks otherwise:

```text
# Title

Status / 文档状态

## 0. Terminology / Definitions or 术语约定
## 1. Abstract / 摘要
## 2. Research Question / 研究问题
## 3. Why This Question Is Confusing / 为什么这个问题容易混淆
## 4. Concrete Data / Training Layout / 数据和训练布局
## 5. Physical Intuition / 物理直觉
## 6. Definitions And Metrics / 术语和指标定义
## 7. Mathematical Model / 数学模型
## 8. Theorems / Propositions / Proofs / 定理和证明状态
## 9. Mechanism Decomposition / 机制分解
## 10. Evidence From Anchors / Anchor 证据链
## 11. Experiment Evidence / 实验结果整合
## 12. Counterexamples And Rival Explanations / 反例和竞争解释
## 13. Claim Boundary / 结论边界
## 14. Anchor Decomposition / Next Anchors / Anchor 分解和下一步
## 15. Relation To Mainline / 与主线的关系
## 16. Next Decision / 下一步唯一决策
## Source Map
```

The data/training layout must appear before the theorem. The story must define
variables, conditions, metrics, abbreviations, and thresholds before using them
as evidence.

## Chinese Terminology Rule

For Chinese stories, use Chinese as the primary explanatory language.

Core abbreviations such as MTP, NTP, LM, MoE, AUC, and experiment identifiers
may be kept only after their Chinese meaning is defined before first use. Do
not use English labels such as "direct supervision", "indirect transfer",
"claim", "setup", "horizon", "probe", "native", "bridge", or "utility" as
substitutes for explanation.

Write the Chinese concept first, for example:

```text
直接语义监督
间接迁移
结论边界
实验设置
未来位置
探针
模型自身预测
桥接论证
收益
```

Include English only when it is a source-file name, condition label, formula
symbol, or unavoidable acronym. If an English condition label must remain,
define it in `术语约定` before using it in the argument.

## Writing Rules

Default conversation language is Chinese. Canonical story language is English
unless the user explicitly asks for Chinese canonical. Use the matching
`<NN>_<topic>_cn.md` file for the Chinese companion.

Use Research_System formula style:

```text
inline: $...$
display:
$$
...
$$
```

Write the current clearest argument, not a timeline. Do not bury raw logs or
detailed tables inside the story.

If evidence is insufficient, say insufficient. Do not complete the story by
making a stronger claim than the sources support.

If the story changes claim boundary or next decision, say which anchor, line
README, or `PROJECTS.md` may need synchronization. Do not perform graph, root
sync, commit, or push unless the user explicitly asks.

## Quality Check

Before finishing, verify:

```text
there is exactly one README-designated primary story pair for the line
the line README identifies one primary story pair and orders any additional stories
every formal English story has a synchronized `_cn.md` companion
filenames use a two-digit order and a subject-bearing topic rather than generic story names
the abstract states question, mechanism, conclusion, boundary, and next step
the story is self-contained and does not depend on meeting context
the data/training layout appears before the theorem
all terms, abbreviations, English labels, and metrics are defined before evidence
Chinese stories do not use English labels as substitutes for explanation
the theorem states assumptions and limitations
evidence is traced to source artifacts
story claims are no stronger than anchors/summaries/detailed records
anchor decomposition contains falsifiable next anchors
mainline relation is explicit
the next decision is singular and actionable
```
