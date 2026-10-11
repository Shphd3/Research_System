# Amendment 02: preserve the single-target check and match LM-head shapes

**The second attempt stopped at Qwen single-target gradient qualification; it is not H2 non-support.** ACP confirmed `pt-ahl6i4wr` as `FAILED` at 2026-10-08 08:56:13 UTC. S7 collection completed. Three Qwen workers passed qualification and began collection; worker 1's relative native/replayed delta difference was 3.25095e-5, above the unchanged 2e-5 limit. No incomplete Qwen result was interpreted.

Full-prefix hidden/CE qualification from Amendment 01 passed. The remaining comparator used one position for the native LM head and sixteen for measurement. Shape-dependent FP32 forward/backward arithmetic is a candidate engineering explanation requiring real GPU validation. Native qualification now forms CE for the same sixteen positions but differentiates only the final event. The other fifteen CE entries must receive zero derivative. Projection outer-product, non-target zero-delta and native-versus-replayed last-event delta checks remain unchanged; no sum-loss replacement or tolerance relaxation occurs.

Only Qwen qualification in `collect.py` and one new CPU test change. `qwen_measure.py` retains Amendment 01; `analyze.py`, data, pairing, all metrics and scientific verdicts remain unchanged. Twelve CPU tests passed. All 26 v2 frozen originals were hash-verified and preserved under `registrations/v2_snapshot/`. Both failure attempts remain intact.

The user's explicit direct execution authorization covers this recorded numerical implementation repair. Both old jobs are terminal; one additional corrective attempt uses the same four reserved H100s and scientific conditions. It has independent `configs/h2_v3.json` and `configs/freeze_manifest_v3.json`, registered with real hashes before submission. No H2 primary outcomes have been analyzed to choose the repair.

The new ceiling is 3h30m, with fifteen minutes conservatively reserved for each old attempt: sixteen planned GPU-hours in total. A global shell timeout additionally covers preflight, final hashes and figures. The pipeline records TERM as failure and terminates its own children. Allocation overhead and actual total usage still require terminal-receipt verification.

Any remaining qualification failure must retain explicit measurement failure and each model's independent eligibility, without relaxed tolerances, replacement tokens or an H2-falsification claim. Engineering repair and scientific amendments remain separate. Researcher scientific judgment is `Unknown`.
