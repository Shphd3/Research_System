# S13 reproduction and files

The existing S11/S12 data are historical evidence, not new confirmation. S13 adds 6912 new prefixes and preserves their exact texts, all token IDs, span offsets, split/cluster labels and original SAE codes. The official Base model and both SAE checkpoints remain external; no checkpoint is bundled or modified.

## Read first

- `summary_cn.md` / `summary.md`: bounded result and decisive measurements.
- `detailed_cn.md` / `detailed.md`: definitions, controls, all statuses and limitations.
- `protocol.md`, `protocol_cn.md`, `frozen_plan.json`, `amendments.md`: rules fixed before confirmation. Do not edit them to match outcomes.
- `data/selection.json`: development-only fixed graph, category edges and migration candidate.
- `casebook_cn.md`, `data/cases.jsonl`, `results/case_member_values.csv`: literal texts, positions, raw feature strengths and two continuous reference axes.
- `external_files_index.json`: exact paths/bytes/hashes for execution-side files excluded from the portable bundle.

## Fast, model-free portable replay

Unzip the result bundle into a clean temporary directory. With Python and numpy/scipy/pandas:

```bash
OPENBLAS_NUM_THREADS=1 python code/portable_replay.py
```

This checks bundled hashes and independently recomputes shared-frequency point estimates, actual member intersections, relation four-cell counts, saved full-margin randomization states and statistical-readout loss. It does not rerun a model, declare scientific acceptance or regenerate every bootstrap trace. `bundle_manifest.json` lists what is actually inside the ZIP. Large external native-hidden/preactivation and reference-bootstrap caches remain indexed execution-side; a manifest is not a claim that those payloads are inside the package.

## Full analysis from saved native codes

The execution root is:

`/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S13_eight_category_independent_1105`

`code/common.py` resolves its owning directory. The full scripts additionally require the actual S11 reference-document metadata and the registered SAE/model paths. Statistical scripts use one BLAS/OMP thread. Existing null caches are checked against the exact candidate edge list before reuse.

Ordered stages used in this run:

1. `prepare.py`: all new texts, tokenizer positions, independent split and quality checks; executed before response extraction.
2. `infer.py`: old-prefix runtime calibration, new development forward; `check_variable_answers.py` qualifies all 16 complete answer sequences; `select_relations.py` and `readouts.py --fit-only` lock development candidates/parameters before confirmation; then new confirmation forward. Do not rerun into this evidence directory as a new experiment.
3. `analyze_frequency.py`: fixed mean/quantile/CDF, membership, reference/context uncertainty, primary status and controls.
4. `analyze_relations.py`: category-stratified exact-margin Curveball null, fixed local edges, global/category/parent-child/migration results.
5. `readouts.py`: evaluate frozen single/additive/interaction statistical readouts; no LM/SAE/router training.
6. `relation_scale_audit.py`, `cases_and_topk.py`, `report_tables.py`: raw-conditional/odds-scale diagnostic, actual preactivation exits and readable summaries.
7. `figures.py`, `verify.py`: PNG/SVG, raw-data replay and full saved margin checks.
8. Result interpretation, visual review, artifact registration, packaging and fresh-unpack portable replay.

Native CPU inference used torch 2.3.0a0+6ddf5cf85e.nv24.04, transformers 4.57.1, tokenizers 0.22.1, numpy 1.24.4, scipy 1.12.0. Missing inference packages were installed under `/tmp/s13_inference_deps`, not into checkpoints. The process used `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python`, `PYTHONPATH=/tmp/s13_inference_deps`, `OMP_NUM_THREADS=8`, `MKL_NUM_THREADS=8`, `OPENBLAS_NUM_THREADS=1`. Old/full-answer native calibration must use the same 8-thread configuration; one-thread engineering failures are preserved in `versions/`.

## Statistical units and boundaries

- 24 development frames belong to 8 context clusters; 48 confirmation frames belong to 16 clusters. Multiple labels/wordings/features in a cluster are not independent replicates.
- Q6000 question-frequency and G6000 DCLM-frequency axes are reused fixed reference corpora. They are not two independent S13 confirmations.
- Complete answer log-probability sum is the behavior primary score; token-average is a sensitivity. Parent labels have no invented fine-class gold answer.
- Top32 fixes each row count and forces gain=loss. Cached zero means exclusion from Top32; the preactivation audit separately measures whether the encoder response remained positive.
- The conditional-excess contrast is not a pure dependence parameter. `relation_scale_audit.csv` separates raw conditional changes, changes of null baseline and a sparse-cell-sensitive smoothed log odds ratio.
- Implicit text removes literal labels, but retains prototype/near-synonym/property clues. No independent lexical/length/source matching or functional intervention is claimed.
