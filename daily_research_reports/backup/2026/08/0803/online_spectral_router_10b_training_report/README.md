# Online Spectral Router 10B Training Report

This directory is the curated 2026-08-03 reading surface for the completed
five-arm, two-seed A15 training experiment.

Final verdict: Relay-HMT is not supported. Local-HMT is the point-estimate
leader in both seeds but not a decisive two-seed winner; the online updater
passes continuity while failing to deliver Relay endpoint utility.

- `report.md`: self-contained Chinese result and mechanism report.
- `evaluation_contract.md`: frozen post-training evaluation definitions.
- `plot_contracts.md`: question, metric, axes, and claim boundary for every figure.
- `figures/`: audited rendered figures.
- `tables/`: compact, reproducible aggregate tables.
- `MANIFEST.sha256`: byte-level integrity for the curated report surface.

Raw checkpoints, fixed-token arrays, TensorBoard files, and full telemetry stay
under `/data/250010109/MoE_Router/outputs/online_spectral_router_training/`.
