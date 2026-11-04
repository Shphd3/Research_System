派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R06_functional_protection_20261025/deviations.md`。
[精确原始文件](../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R06_functional_protection_20261025/deviations.md)；研究修改仍回到原件。

---

# Execution differences (append only)

- Before results: S retains R05 original1200-step attenuation horizon, truncated at240 rather than compressed. All four matrices use joint F/D norm/dot. These clarify underspecified engineering details and preserve the requested science.
- Before results: historical R02/R05 are not equivalent controls; use new paired U/S/F/D matrix. Global navigation has7 preexisting untracked entries outside this round; scoped paths checked directly.
- After startup: inherited external carriers.py/runtime.sh digests were additionally recorded. They were reused unchanged; their digests were not part of the initial nine-file freeze. Main new source/config/contracts/order remained frozen before new evaluation. This is a provenance limitation, not a scientific setting change.
- Engineering audit during training (2026-10-25T17:57:45.130268+00:00): progress/optimizer_step was emitted on both update and token axes under one tag. Raw objective losses, scalar logs, checkpoint counters and scientific settings are unaffected. After terminal, preserve raw event directories and reconstruct canonical TensorBoard events from immutable step JSON with the correct single token axis. No new training or data selection; independently verify monotonic axes and raw-loss agreement.
- Post-run local event repair first import failed because the shell lacked the established PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python activation. It failed before touching event files. Reusing the existing runtime resolved it; all36canonical streams validated, all raw events preserved, no installed-package change or training retry.

- REPORT_HANDOFF_WALLCLOCK_DEVIATION: training ended18:15:27UTC, core analysis18:16:05, registration18:25:44 and core delivery check18:27:21, all within38minutes from17:50:16start. Final ZIP creation and archival happened in the later continuation after the21:50:16UTC deadline. End-to-end4h handoff was NOT met; elapsed gap is not subtracted. No training or new resources after the original job terminal. Full UTC evidence is in reproduce/report_budget_deviation.json.
