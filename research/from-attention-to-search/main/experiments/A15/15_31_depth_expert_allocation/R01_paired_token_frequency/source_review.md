# Sources, advisor intuition and established boundaries

The currently verified facts concern provenance and parameter accounting, not the new allocation's performance. The question, H1–H3, fairness conditions, four-reserved-H100 execution and claim boundary come from the researcher's explicit6November request.

The [byte-preserved user source](supporting_sources/meeting_1106_source.md) is corrected text transcription plus a meeting summary. Original audio was not supplied. Uncertain words remain uncertain, and summary/user supplements are not reconstructed verbatim speech. Its SHA-256 and source role are in[source_manifest.json](supporting_sources/source_manifest.json).

The advisor's discussion in main segment1,06:26–11:38 and segment2,00:00–01:00 proposes fewer/narrower shallow experts and more/wider deep experts, with hierarchy, memory and compression as motivations. It does not establish that shallow layers only learn coarse concepts, that deep experts are independent memories, or that tenfold compression has occurred. The signal-to-noise explanation in segment1,01:49–02:31 and the separately attributed summary is a mechanism hypothesis rather than measured gradient evidence.

The senior's oral report in segment1,00:03–01:35 describes larger improvements on data associated with low-frequency teacher features. The supplied material lacks complete quantitative metrics, counts and controls; it cannot establish this round's numerical benefit. The researcher's own report at02:16–02:48 describes a small memory-task benefit with a larger general-task cost; no complete numerical result is provided here, and frequency/capacity/routing causation is not established.

The independent[R17_D1 SAE result](../../15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/summary.md) preserves answer/readout dependence, failure of the two-SAE frequency mixtures to beat both baselines, and insufficient support/content coverage. Its two dictionaries retain independent IDs. It cannot establish a depth-to-frequency mechanism or identify rare SAE configurations with semantic long-tail knowledge.

The[A15_30 owner](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_30_checkpoint_evidence_use/15_30_checkpoint_evidence_use_anchor.md) records native Dense281,431,040 total/active parameters and ordinary MoE507,988,992 total parameters. Their older data-order match has a bounded endpoint and their total capacities differ; they do not replace this round's matched A/B comparison.

The preferred architecture source is execution-side`20261101_moe_baseline_speedup/moe_baseline/model.py`;`speedup/train_fixed.py` supplies fixed-DDP reduction/training references. The new package must adapt fixed-eight-expert assumptions, ROOT/initialization paths, logging loops and config checks in isolation. Reuse is not proof of a working variable-expert trainer. The exact adapted files, current data access and dual-model smoke are audited execution-side.

## Actual run provenance addendum

The source CPU initialization hash file used seed17; the actual experiment uses seed20261106 and has a separate saved-state PASS audit. Smoke recovery and partial matrix-FLOP evidence, bucket-review timing and outside registration I/O are recorded in the [execution addendum](execution_record.md). The distinction is retained instead of rewriting old evidence. Formal paired results remain pending.
