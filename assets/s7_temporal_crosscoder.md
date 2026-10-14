# S7 temporal CrossCoder inputs and queued producers (A24)

[中文](s7_temporal_crosscoder_cn.md). Read `catalog.json` for exact addresses and identities; this guide does not supersede the registry or any scientific owner.

Each family uses the actually saved1B,5B,15B,31Bnative pretraining milestones.31B is the nearest common substitute for30B; pretraining tokens are not CrossCoder exposures. Fresh is the original lambda0.1 last-Attention SAE sidecar-pretrained8layer/hidden1024 model; Dense is the original no-SAE8layer/hidden1024 trajectory, including its later continuation.

Exact input IDs: `model_s7_temporal_fresh_{1,5,15,31}b_a24_20261013`, `model_s7_temporal_dense_{1,5,15,31}b_a24_20261013`. Full names are enumerated in [current selected strict access](checks/2026-10-13_s7_temporal_A24_inputs.json). CPU native loads and freshly verified state hashes are bound under each entry's `A24_current_CPU_qualification`; runtime GPU checks remain pending. [Input selector](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/docs/s7_temporal_inputs_A24.json).

Required data/tokenizer assets: `dclm_crosscoder_direct_bins_1b_a15_20261013`, `tokenizer_qwen3_0p6b_base`. Data reuses existing DCLM file holdout, not a newly verified original-document/nearduplicate split.32checkpoint-layer spaces are paired observations of one text/token position, not32independent samples.

Authorized queued producers: fresh`pt-5akx5toz`, Dense`pt-lful461t`, each8RTX5090Spot,F32768,32spaces, approximately1Bpositions. [Execution contract](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/docs/s7_temporal_scope_A24.md), [current handoff](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/docs/current_s7_temporal_handoff_A24.json). Submission alone creates no trained output asset. Actual saved immutable states will be registered by the producer, with weights/Adam/RNG/cursors/normalization and progress.0.5B save is required, not yet observed.

Later checkpoint states participate in joint encoding. Decoder profiles describe this dictionary's reconstruction coverage; feature causal origin, learning mechanism and expert/routing utility are unestablished. Future input use needs a fresh strict access check.
