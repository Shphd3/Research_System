# Research Document Explanation Contract

## Goal

Rebuild the explanation in the order a reader needs, not the order the author
wrote it. Assume a capable researcher who lacks the document's local context.
Do not assume that difficulty means low intelligence.

## Source Lock

Treat the exact named file or passage as the first explanation source. Apply
root entrypoint checks only when relying on active-workstream routing; no
separate `Start Here` precheck is required.

1. Read that exact named file or passage.
2. Identify what kind of artifact it is and whether its conclusions are human
   confirmed, AI draft, proposal, frozen contract, direct evidence, or history.
3. Open a linked source only when it is needed to define a central object,
   verify a decision-bearing number, or resolve a claim boundary.
4. State a missing or conflicting source as `未知` (internal state `UNKNOWN`);
   do not repair it from chat memory or general plausibility.

## Reader And Writing Calibration

Default to a capable researcher who lacks this document's local context. If the
user states a different background or names the point of confusion, adapt the
vocabulary, example, and depth to that information without talking down to the
reader.

Build each explanation layer in this order:

```text
what it is
-> why it is needed
-> one concrete example when useful
-> how it works
-> what the source or evidence supports
-> what it does not support
-> what it changes for the current research decision
```

Use one main relation per sentence. Put purpose before implementation. Prefer a
concrete example to a decorative analogy; use an analogy only when it preserves
the causal structure and state where it stops matching. Match length to the
reader's requested depth, but never trade away an assumption, evidence status,
or claim boundary for simplicity.

## Progressive Output

### First Pass: default

Keep the first pass to roughly one screen unless greater depth was requested.
Cover the question, current answer or uncertainty, essential objects, decisive
reasoning and boundary. These are content checks, not required headings or item
counts; combine them in natural paragraphs and define only objects that matter.

Distinguish source statements from AI interpretation where confusion is likely.
Use a separate status block only when it helps track several different claims.
Offer specific zoom-in choices when teaching or guided exploration is requested;
an ordinary explanation needs no follow-up menu. Answer a narrow question directly.

### Deep Pass: only when requested

Keep the first-pass summary, then expand in dependency order:

```text
problem and why it exists
-> objects and their roles
-> mechanism or proof roadmap
-> experiment or evidence chain
-> direct result
-> allowed inference and strongest rival
-> proof, experiment, or research proposals requested by the user
```

Do not repeat the same conclusion at several depths. Each deeper layer must add
a missing relation, justification, example, or boundary.

## Explanation Units

Use the shared [operational first-use and formula meaning contract](../../../../docs/report_writing.md#objects-operations-and-first-use-terms).
This reference controls explanation depth and source handling; it does not maintain
a second terminology or loss/risk convention.

For a paragraph, formula, figure, or gate, explain:

```text
plain meaning
why it is present
what inputs or assumptions it needs
what changes or is compared
what it supports
what it cannot establish
```

For every non-obvious term, give its plain Chinese meaning before reusing the
English name, abbreviation, or symbol. Do not create a glossary dump; define
terms at the first point where the reasoning needs them.

For a formula:

1. say in words what quantity or relation it represents;
2. define every symbol and its type or unit;
3. explain the operation from inside outward;
4. give one tiny concrete or limiting example when it helps;
5. state the exact claim and the nearest tempting overclaim.

Use an analogy only when it preserves the relevant structure. State where the
analogy stops matching. Prefer a direct concrete example when an analogy would
add another conceptual layer.

Use a small diagram only when three or more objects or dependent gates are hard
to hold in prose. Every node must carry semantic content; do not draw a diagram
merely to decorate the explanation.

## Status Language

Use the Chinese labels at the smallest useful section level. The internal code
is shown here for implementation consistency and should not replace the Chinese
label in Chinese output:

| 中文标签 | Internal code | Meaning |
|---|---|---|
| 来源原文 | `SOURCE` | The named document explicitly says this. |
| 已核验证据 | `VERIFIED_EVIDENCE` | A canonical result or source was opened and supports it. |
| 解释 | `EXPLANATION` | Same claim translated into a clearer dependency order. |
| AI 推断 | `AI_INFERENCE` | A conclusion derived from named premises but not stated by the source. |
| AI 建议 | `AI_PROPOSAL` | A new experiment, proof route, counterexample, or research direction. |
| 未知 | `UNKNOWN` | The material does not establish it or the required source is missing. |

An AI-written or unconfirmed source remains unconfirmed after explanation.
Readable wording must not upgrade its epistemic status.

## Compact Example

Suppose a document says: “加入表示 \(R\) 后，开发集损失降低。” The explanation
must not silently rewrite this as “\(R\) contains new information.” Use the
states to preserve the gap:

```text
来源原文：在注册的读出模型下，加入 R 后开发集损失降低。
解释：当读出模型可以使用 R 时，预测变好。
AI 推断：R 可能带有有用信号；但在没有匹配对照前，额外容量或信息泄漏也能产生同一现象。
AI 建议：设原有表示为 X，在留出数据上比较“X 加 R”和“X 加同容量重复 X”两个条件。这是建议的检验，不是已有结果或已批准的实验方案。
```

## Comprehension Check

For a requested teaching session, one check can target the central dependency,
for example:

> 如果去掉对照组 B，这个结果为什么不能再区分“新增信息”和“多一组参数”？

For a narrow answer, stop once the question is answered. When interaction is
requested and more useful than a quiz, offer a precise zoom-in
menu: `对象关系 / 公式第 2 步 / 实验判据 / 结论边界`. Do not end with an
unbounded offer to explain everything again.

## Common Failures

- A correct encyclopedia answer that is too long to enter.
- Defining symbols while leaving the research object undefined.
- Following document chronology instead of reader dependency.
- Using a cute analogy as a substitute for the real mechanism.
- Mixing a new experiment or proof idea into the document's own conclusion.
- Calling a proxy observation a mechanism, a theorem, or a capability result.
- Repeating the verdict without explaining the comparison that supports it.
