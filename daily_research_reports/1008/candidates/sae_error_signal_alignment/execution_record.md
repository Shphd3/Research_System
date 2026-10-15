# H2 candidate diagnostic: execution record

**Final job `pt-c33caya0` SUCCEEDED: both measurements, registered analyses and three figure sets completed.** Researcher judgment remains Unknown; see [candidate results](summary.md). [Protocol](protocol.md), [Amendment 01](amendment_01.md), [Amendment 02](amendment_02.md) and [v3 registration](evidence/registration_v3.json) preserve scientific conditions and unchanged tolerances.

| Job | Submitted UTC | Terminal UTC | Outcome |
|---|---|---|---|
| pt-hsy9grzm | 08:32:35 | 08:40:51 | FAILED; S7 collected, Qwen hidden qualification failed |
| pt-ahl6i4wr | 08:49:02 | 08:56:13 | FAILED; S7 collected, Qwen single-target delta check failed |
| pt-c33caya0 | 09:02:41 | 09:06:00 | SUCCEEDED; both models complete |

Jobs were sequential, with each old job terminal before a correction. Original 22-file and v2 26-file snapshots remain hash-verified in execution. The final 30-file freeze is independently registered. Final runtime: 09:03:30–09:05:37 UTC, 127.18 seconds. The sum of each submit-to-terminal lifetime multiplied by four requested devices is a conservative 1.25 GPU-hour bound, below the planned sixteen GPU-hours.

Resolved and runtime-verified tuple: `h100-4-reserved`, ACP, `share-space` / `share-cluster`, `n6ls.iu.i40.4`, one node/four processes, reserved/normal, four actual NVIDIA H100 80GB HBM3. Image: `shphd-lite-0911`, expanded to `registry.cn-sh-01g.sensecore.cn/ccr-zhicheng-03/shphd-lite-0911:shphd-mig-20260910161423`. Mount: `01995892-d478-76d8-aec7-13fd8284477e:/data`. Runtime: torch `2.3.0a0+6ddf5cf85e.nv24.04`, CUDA 12.4.

Eight worker/model receipts passed. Per model: 1024×16=16384 measurement events; 512×16=8192 readout queries, all valid. LM/SAE updates were zero, parameter versions and asset identities unchanged, repeat measurements exact. Qwen numerical errors were zero; S7 maximum delta relative error was5.05e-6 and CE absolute error1.79e-5, within original thresholds. Twelve CPU checks also passed.

Submission used the repository ACP template and existing compatibility entry, with DRY_RUN=0, ALLOW_SUBMIT=1 and PROTOCOL_APPROVED=1 implementing user-direct authorization, not scientific approval or a fictitious external Smoke. Existing S7 runtime and mounted HF4.53.3 dependencies were reused.

Exact final entry:

```bash
timeout --signal=TERM --kill-after=30s 12600s env H2_CONFIG_PATH=/data/250010109/MoE_Router/experiments/20261008_sae_error_signal_alignment/configs/h2_v3.json bash /data/250010109/MoE_Router/experiments/20261008_sae_error_signal_alignment/scripts/run.sh /data/250010109/MoE_Router/experiments/20261008_sae_error_signal_alignment/runs/diagnostic_v3_20261008T090146Z
```

Run owner: `/data/250010109/MoE_Router/experiments/20261008_sae_error_signal_alignment/runs/diagnostic_v3_20261008T090146Z`. Worker/analysis logs and pod output remain under `logs/` and `pod/`; raw features under `collection/shard_*/{s7,qwen}/`; event/record/domain CSVs and statistics under `analysis/{s7,qwen}/`; PNG/SVG figures under `analysis/figures/`. Selected evidence is linked in the [completion](evidence/completion.json), [preflight](evidence/preflight.json), [final execution receipt](evidence/execution_receipt_v3.json) and [result manifest](evidence/result_manifest.json). Training comparison/TensorBoard: NOT_APPLICABLE. No Router, LoRA, Expert or SAE training.

Monitor owner: current thread `01a10a2a-b783-7752-9149-ed2ffd48a40a/root`. Terminal state and durable progress verified; no further polling/submission. Failures are engineering evidence, not scientific non-support. Registered SUPPORT_BOUNDED_H2 concerns weak average association; higher native-neighbor alignment and negative different-target advantages must accompany it. No commit, push or publication.
