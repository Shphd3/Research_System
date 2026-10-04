# Research graph format

Use the existing repository vocabulary. This reference defines representation, not scientific approval:

| Node type | Use for |
| --- | --- |
| `question` | research questions and decomposed subquestions |
| `claim` | hypotheses, mechanism claims, rival explanations |
| `concept` | definitions, variables, scope, boundary conditions |
| `method` | experiments, operationalization, identification strategy |
| `evidence` | observations, results, patterns, counterexamples |
| `source` | papers, datasets, documents, external materials |
| `task` | next research action |
| `output` | draft conclusions, reports, paper sections |

| Edge kind | Use for |
| --- | --- |
| `decomposes` | breaks a question into subquestions |
| `answers` | a claim answers a question |
| `operationalizes` | a method makes a claim observable |
| `supports` | evidence/source supports a claim |
| `contradicts` | evidence/source/rival weakens a claim |
| `depends_on` | a claim or method relies on a premise |
| `cites` | a node uses a source |
| `leads_to` | a result creates a task or next step |

Use only the edge kinds in this table. Do not invent near-synonyms such as
`motivates`, `uses`, `contextualizes`, or `informs`; map them to the closest
allowed kind instead:

- `motivates` -> `leads_to` when a result opens a next question/task; otherwise `supports`
- `uses` or `contextualizes` -> `cites` when pointing to a source; otherwise `supports`
- `informs` -> `supports` when it bears on a claim, or `leads_to` when it creates a next step

## YAML Contract

When creating or editing `graph.yaml`, keep it valid, boring YAML. Use two-space indentation, arrays with `-`, no tabs, and quote strings only when they contain characters that could confuse YAML (`:`, `#`, `{}`, `[]`, leading `*`, or multiline text).

Top-level shape:

```yaml
root: rq.main

ui:
  layout: LR
  expanded: [rq.main]

nodes:
  - id: rq.main
    title: Core research question
    type: question
    summary: One sentence is enough when no note exists yet.
    status: active
    tags: [framing]

edges: []
```

Required:

- `root`: id of an existing node.
- `nodes`: array of node objects.
- each node: `id`, `title`, `type`.
- `edges`: array, empty is fine.
- each edge: `from`, `to`, `kind`; both ids must exist in `nodes`.

Optional node fields:

- `summary`: use for short, one-sentence nodes that do not need a document yet.
- `file`: one linked Markdown/HTML/text document.
- `files`: multiple linked documents. Use either strings or `{ path, title }` objects.
- `status`: `active`, `draft`, `blocked`, or `done`.
- `tags`: array of short labels.

Valid document-link patterns:

```yaml
nodes:
  - id: claim.short
    title: Short claim
    type: claim
    summary: This node is intentionally just one sentence for now.

  - id: evidence.single
    title: Single note
    type: evidence
    file: ./evidence.md

  - id: source.bundle
    title: Source bundle
    type: source
    files:
      - ./paper.md
      - path: ./appendix.html
        title: Appendix preview
```

Do not force every node to link to a document. Add `file` or `files` only when the longer note exists or when creating the link improves navigation. Missing linked files are allowed while drafting, but they should be intentional and called out in the change report.

