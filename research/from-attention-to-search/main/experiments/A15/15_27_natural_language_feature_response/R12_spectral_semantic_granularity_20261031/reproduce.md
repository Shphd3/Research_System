# R12 reading and reproduction boundaries

Start at summary_cn.md and detailed_cn.md. All figures have CSV inputs in evidence and original source/table hashes execution-side. Raw producer root is `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R12_spectral_semantic_granularity_20261031`.

The recorded sequence was prepare.py → visible-prefix AI label review → analyze.py fit → frozen models/settings → H prefix label review → evaluate.py → validate.py → feature_validation.py → render.py → deliver.py. The last three stages are declared supplementary audit/formatting,not model selection. Initial code and Protocol bytes are preserved under execution `provenance/frozen_sources`,with mappings in `frozen_source_copies.json` and original freeze.json hashes.

Do not run these producer scripts over the completed directory: they contain writes. For a fresh deterministic audit, copy the frozen input metadata and use a new output directory before invoking any script. Do not rerun run_native_cc.py or consume new model forwards. R11's original 462-forward budget is exhausted and irrelevant to this cache-only round. Current new forward count0.

NumPy/SciPy/scikit-learn/Matplotlib CPU suffice;no torch/transformers/GPUis used. The external CJKfont path is recorded in the figure manifest and is not a repository payload. Actual original render environment versions are in the terminal receipt. The initial source semantics and operational metadata repairs are described in Protocol amendments and Detailed;do not omit validate.py's diagnostic-field correction from a full replay.
