# Reproduction and audit map

Run from this S09execution folder, CPU2threads, no model/SAE loads. Original S08root in frozen_plan.json supplies read-only panel/activations. A portable input subset is included in the review packet, and portable_replay.py uses that subset without the original execution path or model.

```bash
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
python code/calibrate.py
python code/run_null.py ATTN_SAE discovery position
python code/run_null.py MLPIN_SAE discovery position
python code/lock_directions.py
python code/run_null.py ATTN_SAE heldout position
python code/run_null.py MLPIN_SAE heldout position
python code/run_null.py ATTN_SAE heldout position_token3
python code/run_null.py MLPIN_SAE heldout position_token3
python code/run_frequency.py
python code/analyze.py
python code/verify.py
python code/supplement.py
python code/figures.py
python code/report.py
```

Sampler needs g++/C++17; engine.py compiles curveball.cpp locally and omits the compiled shared library from delivery. NumPy/SciPy/pandas/matplotlib are analysis dependencies. Native input caches, exact text IDs and asset hashes remain S08-owned. prepare.py must not be rerun over a frozen plan; it creates metadata split and discovery-only feature universe once. Null/frequency scripts refuse overwrite. Reproduce in a new execution copy, preserve source inputs/frozen config, and do not replace old result paths. Longer mixing run is available only via --long under the pre-fixed protocol; no extension was required.

Data: data/document_split.jsonl retains every source ID, original index, full/visible length,8positions/token IDs/decoded tokens and whole-document split; discovery_marginals.npz includes all30000coordinate frequencies separately for8positions and3sources; feature_universe.json and discovery_directions.npz bind24IDs/all276directions and12example pairs/top8bit patterns. No heldout feature reselection.

Tables: A_overlap_references.csv keeps each source side, cross, pooled gap and two references; A_intersection_identity.csv audits exact expectations and nonlinear term; B_own_structure.csv/B_dataset_differences.csv contain all primary/exploratory outputs and separate Holm6families; B_all276_components.csv retains every pair, B_selected_pairs.csv every selected result including zero/adverse cases. Candidate count and exact bit-pattern distributions retain denominators. Each raw native source sparse activation is implied zero outside its positiveTop32IDs.

Nullcache: four-chain256panels summarized in qnull/Jnull/etc, exact seeds/constraints and8full audit snapshots per condition retained execution-side. Full per-draw intermediate states not saved. Large arrays and original source corpora/weights are indexed separately and excluded from the small review packet; selected raw cache inputs, all joint trace samples, actual example coordinates and all tables remain portable. Package manifest says exactly which files are included. Conditional bootstrap intervals do not integrate discovery-selection or all null-center/probability-estimation uncertainty. No feature semantic labels or router claims.
