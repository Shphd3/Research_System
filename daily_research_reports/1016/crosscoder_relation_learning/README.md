# CrossCoder relation-to-learning · 2026-10-16

All computation is complete. Bounded structural organization survives margin controls, but the chosen relation allocation does not yield learning gains. Local update and response interventions narrow the explanation without identifying the complete training cause. Scientific approval and closure remain Unknown.

Read the [one-page brief](summary.md), [full report](report.md), [Detailed](detailed.md), [Protocol](protocol.md), [amendments](execution_amendments.md), and [Chinese reading entry](README_cn.md).

Five main figures and supplements are in [figures](figures/). Raw plotted/diagnostic CSVs are under [evidence](evidence/): complete group controls,99pipeline-null draws,9paired training runs,9local intervention runs,9response controls and first-direction/centering diagnostics. The [origin manifest](evidence_origin_manifest.json) identifies their sources.

Run `python code/replot.py --output-dir /tmp/crosscoder_replot` with NumPy/Matplotlib to recreate plots from included small files without GPUs, checkpoints or full caches. [Verification](replot_verification.json) records the actual check. The [artifact manifest](artifact_manifest.json) and [change manifest](change_manifest.json) provide byte identities and task-owned writes.

Execution root: `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/relation_learning/20261015T164000Z`. Code: the same experiment's `analysis_tools/relation_learning`. Exact config: `config/formal_R1_8.json`. Checkpoints: `learning/seed_<seed>/<arm>/checkpoints/update_<step>.pt`, steps0/510/1530/3060/4590/6120. `checkpoint_manifest.json` lists54actual saves and9finals. Logs/TensorBoard remain beside each run. Complete optimizer/RNG/order/counters are distinct from external-process resume qualification; the latter is NOT_QUALIFIED.

The sole four-H100 Reserved job was `pt-szeffn72`; its worker exited at17:39:48UTC. Current access/resource evidence is in [provenance](provenance/). Raw text, full caches, matrices, model states and logs are not bundled; addresses are retained. Selected plotting/audit NPZs are explicit manifest exceptions. No skills changes, base/CrossCoder training, commits, pushes, external sending or scientific-state transitions occurred.
