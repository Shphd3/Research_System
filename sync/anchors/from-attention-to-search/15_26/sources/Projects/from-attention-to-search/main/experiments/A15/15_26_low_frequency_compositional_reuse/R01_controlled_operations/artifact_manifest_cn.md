# R01产物与来源清单

科学事实见 [Summary](summary_cn.md) · [Detailed](detailed_cn.md)。可访问和完整保存不代表机制成立。

## 执行与代码

Execution root: `/data/250010109/MoE_Router/experiments/20261024_a15_26_compositional_reuse`. Frozen numerical config: [config](provenance/frozen_config.json). Dataset SHA256: `a394a65379adeea6f9498ee6ae8768681405d3e88575e2a2c09f820241c1614f`. [Protocol/source freeze](provenance/design_frozen.json), [main-job v3 source](provenance/actual_full_source_manifest_v3.json), [recovery v4 source](provenance/actual_full_source_manifest_v4.json), [engineering amendments](amendments.md). Raw sources are in `source/`; immutable operational snapshots in `versions/`. Reporting producer: `reporting/build_delivery.py`; aggregate producer: `source/aggregate.py`; source tables read every completion/evaluation/test JSON. Reports do not modify the frozen Protocol.

| Job | Purpose | Outcome |
| --- | --- | --- |
| pt-xmuc6iez | Native cache preparation | SUCCEEDED |
| pt-hh82grqg | External-process resume Smoke | SUCCEEDED |
| pt-r2c46vhp | Initial full | FAILED; output-path bug, completed cases preserved |
| pt-g61bfavm | Same-scope corrected full | FAILED during last revision save128; storage ENOSPC;81 complete cases retained |
| pt-uin52ssn | Qualified recovery32→1024 | FAILED on redundant save after complete final milestone; full updates/curve/hash verified |
| pt-jjxujh54 | Remaining locked measurements; zero further updates | Pipeline, aggregate, output audit and registration complete; see final platform receipt |

One H100 Reserved, image shphd-lite-0911; no four-GPU expansion. Durable receipts: `acp_receipts/certificate_*.json`; pod stdout: `acp_receipts/pod/`. Environment: `audit/environment_full.json`. These are execution evidence, not scientific acceptance. [Raw stdout quality](provenance/stdout_quality.json) records preserved NUL bytes: stdout is not claimed as a perfect complete transcript. Complete primary update metrics, TensorBoard and evaluation files passed separate audits.

## 实际保存与访问

| Asset | Role | Evidence |
| --- | --- | --- |
| model_qwen3_0p6b_base / tokenizer_qwen3_0p6b_base | Exact input model/tokenizer | Input strict checks; model hashes above |
| data_a15_26_20261024 | Frozen generated task | data/dataset.json;provenance/data_audit.json |
| representation_a15_26_20261024 | Native prefix cache | data/cache_manifest.json;zero replay error |
| checkpoint_family_a15_26_20261024_smoke | 8 Smoke state members at registration | audit/registration_smoke.json |
| checkpoint_family_a15_26_20261024_full | Actual full-family inventory:788 saved states including Smoke | /data/250010109/Research_System/assets/checks/20261024T182208Z_a15_26_full.json |
| analysis_a15_26_20261024 | Actual raw readouts, curves, intervention bases, aggregates and figures | provenance/registration_analysis.json;actual_analysis_files.json |
| checkpoint_a15_26_20261024_recovery_block_probe | One actual saved full-block1→2 resume probe; separate from family788 | provenance/recovery_resume_qualification.json |
| checkpoint_a15_26_20261024_<sha16> | Individual states consumed later | audit/checkpoint_input_registrations.jsonl |

Actual saved-state inventory: [manifest](provenance/actual_checkpoints_full.json), 788 members, 117,900,159,002 logical payload bytes; Smoke8, formal780. Each member binds path/hash/bytes/update/target counters/parent. All actual members were freshly hashed/deserialized during family registration; [receipt](provenance/registration_full.json) points to the selected strict check. Asset IDs validate only selected outputs, not the entire library. Parent-dependent deltas need exact Base and declared predecessor; loader `source/engine.py`.

Smoke exact continuation is shared engineering qualification, not independent continuation of each endpoint. The final family includes earlier Smoke states intentionally; formal aggregation excludes them. The separate recovery probe adds one saved state outside that family. Internal duplicate references preserve every state path and read hash; see E04. `seconds` for the recovered last case covers its resumed segment and is not total GPU accounting. Failed job remains failed. No missing saved payload is disguised as complete.

## 测量、审计和精选证据

[Every run](tables/all_runs.csv), [pair TEST](tables/pairs.csv), [curves](tables/learning_curves.csv), [help](tables/help.csv), [freeze](tables/freeze.csv), [exposure](tables/exposure.csv), [revision](tables/revisions.csv), [facts/qualification](tables/factual_results.json), [execution coverage](tables/coverage.json), [scientific eligibility](tables/scientific_coverage.json). [Final output audit](provenance/final_output_audit.json), [Smoke](provenance/smoke.json), [data counts](provenance/data_audit.json). See [figure origin/meaning](figures/SOURCES.md).

Primary raw results: `runs/*/metrics.jsonl`, `tensorboard/`, `curve.json`, `evaluations/`, `test.json`, `revision_evaluation.json`; interventions: `analysis/interventions/`. Raw prompts, checkpoints, caches and full logs remain execution-side. Selected small tables, figures and manifests are byte-identical copies covered by `main/curated_evidence.json`.

## 复现入口与范围

The original command used `source source/runtime.sh`, then `python source/pipeline.py full`, followed by aggregation/audit/registration. After E04 the recovery entry was `python source/finish_recovery.py`, then the same `aggregate.py`, `audit_outputs.py` and `register_assets.py full` sequence. The recovery entry continues one missing trajectory. Its final milestone completed before a redundant save failed; E05 certifies that actual saved milestone and uses `finish_saved_outputs.py` for remaining locked measurements only. No further training is performed;81 completed trajectories are not rerun. Existing completion receipts skip completed trajectories; rerunning is not claimed as independent replication. The reporting builder is CPU-only and reads completed outputs. New training still requires a new scope/identity if scientific settings change.

本轮完成R01授权范围，订单V2另有独立owner记录；没有替代其结果。仅本地记录与阅读同步，无commit/push/外部发布。
