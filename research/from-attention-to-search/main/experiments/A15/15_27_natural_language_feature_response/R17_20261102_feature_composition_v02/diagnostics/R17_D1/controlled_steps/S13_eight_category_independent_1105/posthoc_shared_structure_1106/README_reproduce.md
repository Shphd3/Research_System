# Reproduction

Inputs are exact paths with hashes in evidence/input_manifest.json. They must remain readable for the full cache-only replay. No model weights or inference runtime is needed.

```bash
OPENBLAS_NUM_THREADS=1 python code/analyze.py
OPENBLAS_NUM_THREADS=1 python code/verify_and_cases.py
OPENBLAS_NUM_THREADS=1 python code/repair_denominators.py
OPENBLAS_NUM_THREADS=1 python code/figures.py
OPENBLAS_NUM_THREADS=1 python code/write_reports.py
```

Scripts use the original S13 common.py for dictionary/label names; output is this supplement only. If working from a portable packet, `code/portable_replay.py` independently replays the decisive set/mean/label examples from included CSR/panel/count inputs. Full extraction and original S13 statistical inference are not rerun. The portable packet content and outside files are listed precisely in package_manifest.json and external_files_index.json.

Tables: decomposition_family/summary = both shared-list sets; seven_regions_family/summary = own parent and two children; seven_region_proportions = true three-way union and per-side32 denominators; member_events = IDs/frequencies/four native amplitudes per event; feature_label_statistics = every ever-active feature, label, wording and split; extra_parent_bridge = distinguish absent coarse intersection from absent own parent; all_dev_candidates and representative_wording_checks = frozen reused-DEV rule and same-ID wording outcomes. Empty groups have missing frequency means. All new checks are exploratory and conditional on fixed reference counts. The original unused cross-partition fraction columns were repaired with original bytes preserved in versions/; membership, frequency, amplitude, candidates and main effects were not changed.
