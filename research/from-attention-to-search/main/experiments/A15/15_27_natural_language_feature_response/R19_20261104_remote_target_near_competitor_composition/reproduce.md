# Reproduction

## Without model inference

Extract the ZIPand run `python code/offline_replay.py` from its root. Python3.10+,NumPy1.24.4andSciPy1.12.0suffice. The script independently reconstructs sparse vectors from every saved ID/value, verifies all raw token sums and paired memberships, recomputes primary effect means/intervals/p/Holm and four joint-null projections/p-values. No absolute data path,model,GPUor network is needed. This does not regenerate conditional-null draws; their full statistic traces, seeds and source code are included for audit.

## Exact forward environment and algorithm

Original execution uses torch2.3.0a0+6ddf5cf85e.nv24.04and the existingQwen3-capable Transformers tree. Set `PYTHONPATH=/data/250010109/dependency_packages/hf_transformers_qwen3`, `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python`, `TOKENIZERS_PARALLELISM=false`; use2CPUthreads,FP32,SDPAand2×328physicalshape. Model/tokenizer and both nativeSAEweights/loaders/hashes are in config.json; omitted_assets.jsonstates which external payloads are required. Existing inference completed; rerunning a stage requires a fresh output location, because run.pyrefuses to overwrite saved scores/caches.

The actual sequence was prepare.py→record_design.py→run.py smoke→run.py discovery→select.py→candidate/analysis hash gates→run.py heldout→analyze.py+joint_heldout.py→supplement.py→quality_coverage.py→figures.py→verify.py→offline_replay.py→reports/curation/package. NativeSAEencoding is encoder(x),ReLU,Top32without input normalization/decoder-bias subtraction. Hooks capture block27o_projoutputand actualMLPpreinputat319,with no activation modification. Full candidate conditional scores include every item token and period. Complete source and numerical checks are retained.

## What can be audited

See evidence/freeze.jsonandpre_result_ownersfor exact pre-run owner/Protocolbytes; design_result_resolution.jsonresolves later factual-owner updates without erasing old hashes. candidates_and_joint_frozen.jsonandanalysis_code_frozen_before_heldout.jsonprecede heldout starts. reference validation replays old natural counts/groups. verification.jsonchecks292tokenizations,196score replays,136protected old files and6144degree constraints. Presentation correction changes no hypothesis/test. Package receipt checksCRC,size,SHA,links,new-directory extraction and offline replay. Scientific acceptance remainsUnknown; no intervention/training is run or designed automatically.
