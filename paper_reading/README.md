# Paper Reading Library

This folder is for accumulating literature understanding, not for storing every PDF.

Each paper should have its own folder under one category. Every paper folder must contain at least:

- `summary_card.md`

Optional files:

- `reading_record.md` for mainline-anchored reading notes
- `reading_notes.md` for section-level notes
- `math_notes.md` for definitions, equations, and proof sketches
- `experiment_notes.md` for experimental design and evidence checks

For blogs or essays, use the same category folders and create:

- `recordings.md` or `reading_record.md`
- `summary_card.md` only if the piece becomes important enough to cite later

Templates live in `_templates/`:

- `summary_card.md`: shortest first-pass card
- `paper_reading_record.md`: paper reading process template
- `blog_reading_record.md`: blog / essay reading process template

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

For any paper, blog, or essay, always end with a `Mainline Update Check`. The useful output is not that you read it, but whether it changes your hypothesis, modeling, experiment design, interpretation, or next decision.
