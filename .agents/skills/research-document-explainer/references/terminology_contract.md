# Terminology Contract

Consult the relevant entries in the repository-wide
[Research Terminology Registry](../../../../docs/research_terminology.md) only
when using a recurring English alias or resolving a naming conflict. A plain
Chinese answer does not require loading the registry.

## First-use definitions

Define indispensable English aliases in plain Chinese before reusing them.
Use the registered meaning when available. For a document-specific or
unregistered term, state its local meaning and scope inline; group several such
terms in a **本次术语** block only when that improves reading. A local definition
does not add or approve a global convention; proposed global mappings remain
`PROPOSED`. Define only terms used in the answer, rather than padding a short
answer with a registry or glossary.

A quoted source may contain an unregistered English name. Quote it only beside
its Chinese gloss, and do not adopt the quoted name as later shorthand unless
its local meaning has been defined.

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

The maintained authority for a first-use definition's operational content is the shared
[writing contract](../../../../docs/report_writing.md#objects-operations-and-first-use-terms):
include how the object is obtained and used and which question it answers.
Do not maintain a competing definition template here.

Do not define one unexplained English word using two more English words. For an
abbreviation, expand it in Chinese before or beside the original-language full
name. For a symbol, define the real object before giving its mathematical type
or dimension.

## Consistency Audit

Before delivery:

1. scan every English concept word and abbreviation in prose;
2. find its earlier definition in the explanation and check any reused registry meaning;
3. verify that later uses keep the same object and scope;
4. replace an unnecessary alias with Chinese;
5. separate same-spelled but different objects, especially representation,
   function, routing, and optimization terms.

An unexplained run ID, group code, metric label, or method name fails this audit
even when it appears in the source document.
