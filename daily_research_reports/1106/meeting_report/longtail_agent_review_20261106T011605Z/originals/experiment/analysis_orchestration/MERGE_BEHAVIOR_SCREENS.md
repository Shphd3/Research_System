# Merge two frozen initial behavior screens

```bash
python analysis_orchestration/merge_behavior_screens.py \
  --data FULL_CONFIRM_CANDIDATES_20000.jsonl \
  --sources FIRST4096_SCREEN REMAINING15904_SCREEN \
  --out NEW_MERGED_SCREEN
```

Arguments above are path placeholders. Run once per **identical mode/model**,
only after both source screen directories are complete. This tool was not invoked
on real outputs during implementation. Root queues any later merge after the
initial complete matched experiment; it never submits inference or training.

The CLI requires exactly20000 unique full-roster facts and two disjoint source
batches of4096/15904 facts. Their union must equal the full roster. Every fact
must have exactly `train_question` and `eligibility_question`; eligibility is a
screening form,not a held-out test form. All expected rank receipts must be
COMPLETE, cover ranks0..world−1 and match raw-file hashes/row counts. Different
source worlds are recorded rather than falsely relabeled as a new execution.

All receipts must agree on mode, model path, model-config SHA, seed, full resolved
generation config and explicit greedy overrides (`use_model_defaults=False,
do_sample=False,num_beams=1`, max32). Behavior-screen and imported scoring/
generation-helper hashes must agree. Within a batch, declared input-data SHA is
constant; between distinct batches it may differ and remains recorded.

A cache_io.py full-file hash difference is permitted **only with known exact
source snapshots**. Current v4 and the preserved exact v3 snapshot are available.
The tool compares ASTs of student_prompt/teacher_prompt across every used
snapshot. Encoding-mask changes are recorded without pretending the whole file
was unchanged. Every actual raw prompt is also checked against its original
full-roster question/context and the fixed student or locally observed Qwen3
no-tools/nonthinking serialized teacher contract. Prompt, gold/source, mode or
view mismatch is an error. No tokenizer/model library is imported.

Output records follow the **original full-roster order**, with train then
eligibility view. Original JSON record bytes are copied verbatim, including raw
text, parsed answer, correctness, status, token IDs and unknown extra fields.
Original fact_scores rows are copied verbatim in the same fact order. No score
function runs, no truth/aggregate score is recomputed, and no correctness-rate
interpretation is produced. A missing final newline is appended only to maintain
JSONL; this is counted explicitly. Source line hashes/locations are retained.

Outputs:

- `outputs_rank000.jsonl`: compatibility filename for select_cohorts;
  **not a newly executed GPU rank**.
- `fact_scores.jsonl`: original frozen rows,not regenerated scoring.
- `summary.json` and `merge_receipt.json`: status
  **CPU_MERGE_NO_NEW_INFERENCE**, inference_executed=false, parent file hashes,
  source-function proof, configuration and coverage.
- `row_provenance.jsonl`: each output record's original file/line/hash.

No `receipt_rank*.json` is created. No original file or frozen plan/core is
modified; an existing output directory is refused. Parent batch_size was not
recorded in behavior-screen receipts, so the merge makes no bitwise batch-shape
invariance claim. All original parent inference evidence remains linked.

Five small synthetic CPU tests cover exact byte/order preservation, v3/v4
cache_io prompt equivalence, duplicate/missing views, greedy/model-config
mismatch, incomplete receipts, and teacher prompt tampering. Internal test helpers
use4fake facts; the production CLI has no reduced-size override. No real model
output has been read or merged for these tests.
