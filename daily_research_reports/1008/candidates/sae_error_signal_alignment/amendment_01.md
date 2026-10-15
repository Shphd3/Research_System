# Amendment 01: Qwen numerical-replay repair

**The first job failed Qwen numerical qualification; the H2 data, metrics and decision rules are unchanged.** This is measurement-implementation failure, not scientific non-support. All 16,384 S7fresh positions were collected. Those gradient outcomes were not analyzed to adapt the second test.

ACP confirmed `pt-hsy9grzm` as `FAILED` at 2026-10-08 08:40:51 UTC. Runtime preflight verified four NVIDIA H100 80GB HBM3 devices, original asset identities and the prospective freeze. Across workers, Qwen full-hidden versus selected-position replay maximum absolute differences were 2.30e-5, 2.67e-5, 2.48e-5 and 4.58e-5, above the registered 2e-5 threshold; CE differences were all below 1.21e-5. No qualified Qwen primary result was produced.

The original replay evaluated only 16 selected positions per record, changing the MLP matrix-multiplication shape. Shape-dependent FP32 arithmetic is a plausible engineering explanation, not an established hardware cause. The repair replays the final MLP, residual addition and final norm at the native full batch×255 shape. It selects the same positions only before lm_head/CE and extracts their gradients after full-tensor differentiation. Hidden qualification now covers the complete prefix; CE, delta and parameter-gradient tolerances are unchanged.

The [Protocol](protocol.md) retains the hypothesis, assets, native interfaces, 1024 records, 16 positions, fit/readout split, input-only pairing, seeds, controls, coverage and verdict branches. Three additional CPU checks cover full replay shape, record-specific positions and zero gradient outside selected positions. Together with existing metric checks, 11 CPU tests passed; GPU qualification remains required.

The original [registration](evidence/registration.json) and configuration remain available. All 22 original frozen source files were hash-verified and preserved under the execution owner's `registrations/v1_snapshot/`. Original logs and failure receipt are retained. The repaired attempt uses `configs/h2_v2.json`, `configs/freeze_manifest_v2.json`, a separate run root, and a new prospective hash registration. The added figure module displays registered statistics only.

The user explicitly authorized direct analysis/execution of both models. This is one recorded implementation repair within that scope, not a new scientific condition or an automatic blind rerun. The old job is terminal. One corrective submission uses the same 4-H100 reserved profile. Its ceiling is reduced to 3 hours 45 minutes, with 15 minutes conservatively reserved for the first attempt; the aggregate budget remains at most 16 GPU-hours. A second qualification failure does not authorize further threshold changes or outcome selection.

This amendment does not certify repaired GPU qualification, completion or H2 support. Those require the new run's actual receipts. Researcher scientific judgment remains `Unknown`.
