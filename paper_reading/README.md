# Paper Reading Library

This folder is for accumulating literature understanding, not for storing every PDF.

Each paper should have its own folder under one category. Every paper folder must contain at least:

- `summary_card.md`

Optional files:

- `reading_record.md` for mainline-anchored reading notes
- `reading_notes.md` for section-level notes
- `math_notes.md` for definitions, equations, and proof sketches
- `experiment_notes.md` for experimental design and evidence checks

For blogs or essays, use `reading_record.md`; create `summary_card.md` only if
the source becomes important enough to retrieve or cite later.

Reusable templates live only under the repository root:

- `templates/reading/paper_summary_card.md`: shortest first-pass card;
- `templates/reading/paper_reading_record.md`: deeper paper record;
- `templates/reading/paper_blog_reading_record.md`: deeper blog or essay record.

For web-side paper-reading AI, use:

```text
prompts/project_instructions/paper_reading_project_prompt.md
```

That prompt starts from the named paper or article. Provide `PROJECTS.md`, a
current Anchor, or a root `sync/` entry only when the question asks how the
reading changes a particular research line.

## Categories

- `01_moe_routing/`: MoE, routing, expert specialization, sparse computation
- `02_continual_learning/`: continual learning, forgetting, replay, fast adaptation
- `03_representation_features/`: representation geometry, features, sparse dictionary, probes
- `04_zipfian_long_tail/`: Zipfian structure, long-tail data, frequency effects
- `05_training_dynamics/`: optimization, training dynamics, scaling behavior
- `06_evaluation_methods/`: diagnostics, metrics, causal audits, benchmark design
- `99_other/`: useful papers that do not yet fit a stable category

## Naming

Use a compact folder name:

```text
YYYY_firstauthor_shorttitle
```

Example:

```text
2024_author_sparse_moe_routing/
```

## Reading Rule

The summary card is enough for first-pass reading. Only create deeper notes when the paper changes the mainline, exposes a risk, or becomes necessary for a report.

Perform a mainline-update check only when the user asks about project impact or
the reading materially challenges a current hypothesis, design, interpretation,
boundary, or next decision. Otherwise a concise explanation is complete.
