# Terminology Contract

Read the repository-wide
[Research Terminology Registry](../../../../docs/research_terminology.md) before
writing a Chinese explanation. The register controls recurring English aliases;
this contract controls how they enter one explanation.

## Hard Gate

An English alias may appear in explanatory prose only after one of these two
pre-use definitions:

1. it is `APPROVED` in the global register and this explanation first writes
   `中文标准名称（alias）：一句定义`; or
2. it is document-specific and appears first in a **本次术语** block with its
   Chinese name, exact local meaning, and scope.

User pressure for speed, source wording, or brevity does not remove this gate.
If a term is unnecessary, use Chinese and omit the alias. If a recurring alias
is absent from the register, label its proposed mapping `PROPOSED`; do not
silently establish a new global convention.

A quoted source may contain an unregistered English name. Quote it only beside
its Chinese gloss, and do not adopt the quoted name as later shorthand unless
the gate above is satisfied.

In Chinese output, use `来源原文 / 已核验证据 / 解释 / AI 推断 / AI 建议 /
未知` as explanation-state labels. Uppercase internal state codes are not
reader-facing aliases; include one only when the user needs the exact artifact
status and define it beside the Chinese state first.

## First-Pass Term Budget

Introduce only the English aliases needed to understand the first reasoning
chain, normally no more than five. Additional terms belong in later zoom-in
layers. Familiarity to the writer is not evidence that the reader already owns
the term.

## Definition Shape

A useful first-use definition states:

```text
Chinese research object (approved or local alias)
what it is in this document
what role it plays
nearest object it must not be confused with
```

Do not define one unexplained English word using two more English words. For an
abbreviation, expand it in Chinese before or beside the original-language full
name. For a symbol, define the real object before giving its mathematical type
or dimension.

## Consistency Audit

Before delivery:

1. scan every English concept word and abbreviation in prose;
2. find its earlier definition in the explanation or approved registry;
3. verify that later uses keep the same object and scope;
4. replace an unnecessary alias with Chinese;
5. separate same-spelled but different objects, especially representation,
   function, routing, and optimization terms.

An unexplained run ID, group code, metric label, or method name fails this audit
even when it appears in the source document.
