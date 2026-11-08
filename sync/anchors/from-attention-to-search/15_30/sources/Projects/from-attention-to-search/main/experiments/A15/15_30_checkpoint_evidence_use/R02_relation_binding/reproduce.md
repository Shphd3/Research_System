# Recheck this completed round

The round is complete; no additional inference or training is needed. For a CPU-only arithmetic review, the following commands regenerate tables/plot from retained raw files and replay input/label/score/immutability checks. They do not load model weights. They write R02 analysis products only; do not run preparation or inference just to inspect the report.

```bash
cd /data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use_r02_relation_binding/code
python analyze.py
python verify.py
```

`common.py` owns paths, hash/JSON utilities and the R01 byte snapshot. `audit_inputs.py` replays R01 evidence and selects exact states. `prepare.py` constructs and validates the frozen panel. `run.py` adapts the R01 native loader read-only (`sys.dont_write_bytecode=True`), with new FP32 candidate scoring and greedy generation. Its `smoke` and `full` stages are already complete. `analyze.py` retains all family metrics, paired statistics and measured plots. `verify.py` replays labels/positions/score arithmetic and protected bytes. `report.py` and `finish_docs.py` write review material only; report selection adds curated payload entries and is deliberately not an idempotent inference command. The frozen code/data/protocol hashes precede the first score; post-run reporting/analysis files are separately inventoried in the final manifest.

Do not rerun `audit_inputs.py` over the preserved pre-run R01 snapshot or rerun preparation over frozen data. A future approved independent repetition needs a new output location, an explicit frozen contract and current input checks; it must not overwrite this round or R01. No such repetition is started here.

Verification passed: six state outputs, 576 binding and 576 reference records, all world swaps/labels/token endpoints, frozen plan/data/code, native CE calibration and 308 directly comparable generation first-token probabilities (maximum error 1.69e-5 nat). All protected R01 noncache bytes and file-set identity are unchanged. This is engineering verification, not independent scientific replication. [Detailed](detailed.md) owns actual cost, limitations and NOT RUN ledger. [Artifact manifest](artifact_manifest.json) indexes code/config/data/scores/receipts/tables/figures by hash; [original unchanged R01 snapshot](/data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use_r02_relation_binding/audit/r01_before.json).
