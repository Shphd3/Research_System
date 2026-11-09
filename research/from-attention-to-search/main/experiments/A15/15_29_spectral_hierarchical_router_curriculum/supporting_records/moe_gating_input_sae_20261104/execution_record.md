# Frozen MoE33B final gating-input SAE

The researcher explicitly authorized training on2026-11-04:freeze the ordinary MoE exact33B checkpoint and train only one independent SAE on the final layer router-input, following the original28layerQwen MLP-input E16 recipe and1Brawactivationposition budget. Complete4H100Reserved Smoke and real-process resume before formal submission.

This is a diagnostic-tool supporting record, not a change to P/F or a new scientific result. Dense is not retrained. SAE utility/semantics remain Unknown.

- [Execution contract](/data/250010109/MoE_Router/experiments/20261104_moe_gate_input_sae_33b/docs/protocol.md) ([Chinese](/data/250010109/MoE_Router/experiments/20261104_moe_gate_input_sae_33b/docs/protocol_cn.md))
- [Actual configuration](/data/250010109/MoE_Router/experiments/20261104_moe_gate_input_sae_33b/configs/formal.json)
- [Source/config freeze](/data/250010109/MoE_Router/experiments/20261104_moe_gate_input_sae_33b/audit/source_freeze.json)
- [Input access](/data/250010109/Research_System/assets/checks/20261104_moe_gate_sae_inputs.json)
- Smoke job:pt-28etcz4j; qualification pending.
- Formal job:NOT_SUBMITTED_PENDING_SMOKE.

Actual receipts and outcomes are recorded execution-side. Registration lists only actually saved outputs.


## Actual execution receipt

Revision 2 Smoke job pt-3l4080ju passed, including real all-process restart. Continuous 100 updates and a separate 60-update run followed by process exit and restart to 100 matched bitwise for losses, samples, SAE parameters, Adam, learning rate, all four ranks' RNG/activity/data states, counters and frozen biases. The first attempt failed a scalar fingerprint conversion before any optimizer update; its source and logs remain preserved.

Formal job **pt-zgngnz9q** was accepted for one node with four H100 Reserved GPUs. Target: 244141 updates / 1,000,001,536 raw activation positions. See the [receipt](/data/250010109/MoE_Router/experiments/20261104_moe_gate_input_sae_33b/docs/receipt.md) and [platform certificate](/data/250010109/MoE_Router/experiments/20261104_moe_gate_input_sae_33b/audit/formal_execution_certificate.json) for current verification. At this snapshot the node is starting; formal updates are not verified.

Measured compute throughput is approximately 254000 positions/s. Plan 1.5–2.5 training hours, excluding queue and startup; full-budget throughput is not measured. All 13 saved Smoke payloads and qualification evidence are registered and pass [strict access](/data/250010109/Research_System/assets/checks/20261104_moe_gate_sae_smoke_outputs.json). This is engineering qualification, not a semantic feature result. Formal 1B endpoints are not yet saved.
