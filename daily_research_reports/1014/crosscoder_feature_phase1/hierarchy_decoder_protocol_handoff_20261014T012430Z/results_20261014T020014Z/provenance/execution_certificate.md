# Execution certificate: hierarchy_decoder_distribution

Job: pt-icv8hyi3. Run: 20261014T020014Z.

User explicitly approved one new four-card H100 Reserved allocation and GPU analysis, after resource clarification. This supersedes the draft CPU-only resource clause; scientific definitions remain frozen.

Profile: h100-4-reserved; ACP share-space/share-cluster; n6ls.iu.i40.4; one node; four GPUs; reserved; normal priority.

Image: registry.cn-sh-01g.sensecore.cn/ccr-zhicheng-03/shphd-lite-0911:shphd-mig-20260910161423. Dependencies: existing experiments/20261012_qwen3_crosscoder/scripts/runtime.sh; no install/download.

Command: bash code/run.sh (absolute command in submission receipt). Protocol and source hashes: execution_record.json and protocol_frozen.md.

Limits: CPU 8 cores; aggregate RSS 16GiB; new disk 1GiB; per-card allocated 4GiB; active computation 1800s, wall 5400s. Performance smoke NOT_RUN_USER_EXCLUDED; embedded correctness mandatory.

Monitor owner: original thread 01a1343f-32aa-7500-9835-000956218089 through complete requested analysis. Runtime hardware/env unverified until environment.json. Status is not scientific approval. Durable logs: pod_logs/; stages: events.jsonl; partial/terminal receipts: analysis_state.json, compute_completion_receipt.json.
