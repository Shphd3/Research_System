# Deferred truth, year agreement and complete cases

`export_consistency_cases.py` is an independent postprocess tool. It does not
modify the frozen statistics v2 engine, score rules, source data or core eval
orchestration freeze. **Do not invoke it on real outputs until the owner begins
final analysis.** It was tested only on explicitly synthetic data.

```bash
python analysis_orchestration/export_consistency_cases.py \
  --mapping analysis_orchestration/mappings/2048.json \
  --out NEW_CONSISTENCY_AND_CASES --target-arm memory_head --max-cases 3
```

Optional `--target-run RUN_ID` limits the target checkpoint. `--case-ids ID...`
exports explicitly named target facts. Main and diagnostic mappings are processed
separately; overlapping populations and duplicate cases are not pooled.

Two objects remain separate:

- **Truth/correctness:** each original/heldout score remains frozen
  True/False/Unknown. The output records its three-character T/F/U pattern,
  original correctness and both-heldout success. Missing data and unresolved
  scores stay Unknown; a known wrong heldout view makes the joint event false.
- **Year-answer agreement:** a single unqualified four-digit ASCII year after
  Unicode compatibility normalization is extracted from each parsed answer.
  Two heldout years can agree while both differ from the standard answer.
  Missing/multiple/decade/uncertain/qualified answers yield Unknown agreement.
  Three-question agreement is also recorded. This is a year-token proxy, not
  a new semantic grader or knowledge-correctness definition.

`year_matches_gold` independently compares an extracted year with the canonical
source answer. Disagreement with the existing True/False score is an explicit
**review flag**; the tool never silently rescores it. For example, a Chinese year
suffix can expose a frozen format-grading limitation. Standard answers remain
from the verified real-text dataset, never from a tested model.

`fact_consistency.jsonl` contains one expected fact/run record with source family,
phase, quota, actual exposure when available, T/F/U pattern, years, agreement,
consistent-wrong indicator, parser reasons, missing views and grading-conflict
flags. `truth_and_agreement_separate.csv` reports each metric with its own fact
counts/Unknown range, per run/teacher source/phase/1vs8. Question forms never
increase the sample size. This tool adds no new uncertainty model; the primary
paired bootstrap remains in frozen stats v2.

Cases are selected **after aggregation** using fixed descriptive categories:

1. Target both-heldout success with known baseline nonsuccess.
2. Target known nonsuccess.
3. Equal wrong heldout years or loss of known baseline success.

Each category uses deterministic SHA ranking, up to the specified maximum.
Eligible counts are saved. A case satisfying multiple categories is stored once
per target run/fact with all category tags. These conditional examples do not
change denominators or estimate prevalence. Explicit IDs are also supported.
Successful, failed or contrary cases may be absent; the tool does not invent them.

`complete_cases.jsonl` preserves the complete source fact, including original
context, source path/record ID/byte offsets/answer span when present, gold answer,
training and heldout questions. It includes **all mapped arms and stages for that
seed**, with every available raw view, parsed answer, truth score and independent
year-agreement fields. The displayed source is evidence for the reader; it was
not thereby supplied during closed student generation. Missing raw views remain
visible. `postprocess_receipt.json` records input/code hashes and selection counts.

Four CPU tests cover equal-but-wrong agreement, multiple/decade/qualified/missing
answers, grading-conflict flags without rescoring, and full source-offset/raw-arm
case export. No actual model output has been opened during implementation.
