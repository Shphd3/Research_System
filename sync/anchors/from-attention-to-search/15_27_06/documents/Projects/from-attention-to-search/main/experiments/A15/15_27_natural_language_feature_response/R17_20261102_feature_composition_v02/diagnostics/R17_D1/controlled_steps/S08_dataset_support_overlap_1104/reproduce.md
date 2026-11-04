派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S08_dataset_support_overlap_1104/reproduce.md`。
[精确原始文件](../../../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S08_dataset_support_overlap_1104/reproduce.md)；研究修改仍回到原件。

---

# Reproduction and saved evidence

All execution paths are bound in frozen_plan.json and data/sources.json. Native model/SAE weights and full source Arrow files are intentionally excluded. CPU2threads, no GPU, training or interventions.

```bash
export PYTHONPATH=/data/250010109/dependency_packages/hf_transformers_qwen3
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 TOKENIZERS_PARALLELISM=false
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
python code/extract.py
python code/analyze.py
python code/verify.py
python code/figures.py
python code/describe.py
python code/report.py
```

The extraction refuses to overwrite an existing activation cache. For full fresh rerun, copy this folder to a new execution location and remove generated caches only in that new copy; original freezes and source paths remain. prepare.py also refuses to replace the frozen plan. No re-preparation is needed for the saved771-document panel. For a quick model-free numerical replay, analyze.py uses cache/activations.npz and writes only derived analysis outputs; verify.py checks independent set/edge arithmetic after kernels are regenerated. Empty optional short fixed32records are marked invalid and never used in that control.

Raw data inventory: data/panel.jsonl contains every selected original question, source row, metadata, token IDs/pieces/offsets and sampling positions; sample_ids.csv/exclusions.jsonl retain selection; pair_graphs.npz stores all original graph endpoints with global document IDs; cache/activations.npz stores all771x10x32 native IDs/values per dictionary and measured quality; tables/overlap_summary.csv stores every primary/control estimate/CI/count/seed; document_resamples.npz stores complete document-bootstrap/permutation values; deterministic_examples.jsonl contains fixed unselected within/cross examples with concrete shared IDs/values. Large derived kernels stay execution-side if excluded; exact path/size/hash in large_files_index.json. Package payload manifest states exactly which files are portable.

Protocols were frozen before extraction; fixed16amendment is explicitly timestamped before first forward and preserves original files. Scientific approval/closure Unknown; no publication or commit.
