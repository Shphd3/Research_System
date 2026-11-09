# Reproduction and provenance

Executionroot:/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_equal64_bands_mean_control
Canonicalowner:/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_equal64_bands_mean_control
Parentinputs:/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R16_20261102_layerwise_head64_intervention

Frozen GPU runner adapts the already-qualified R16 native Qwen helper and continuation path; it reuses the actual checkpoint, layer hooks, full PCA bases and cachedtargetstates. It does not reuse a training engine or introduce optimization. The original failed runner and freeze remain in provenance; protocol amendment E1 records the matched-batch repair.

Entry is the canonical Research_System ACP template, profile5090-2-spot, imageshphd-lite-0911 and mountedSM120runtime. scripts/launch.sh runs embedded smoke then two document shards, never more than2GPUs. Profile/image expansion and actualjob IDs are in execution_certificate.md and acp_receipts. No unrelated job/config mutation.

CPU reproduction from this execution directory:

```bash
python scripts/analyze.py
python scripts/casebook.py
python scripts/render.py
python scripts/validate.py
```

The analysis requires all180 completed document chunks and matchingfreezeSHA. Statisticalplan/fixedcases are inprotocol. The outputs distinguish main andauxiliary panels, fixed andpostselected cases(no newpostselection), old andnewconditions, nativeprediction retention andtrue successorloss. Allpositions retain exacttokenIDs; tokenfragments are not fullsemanticwords.

The canonicalanchor may receive a factual completion appendix; executionanchor.md is the frozen pre-run design snapshot. GPUfreezehashes bind execution sources, not subsequent mutable scientific commentary. Finalartifact_manifest.json records actualscripts/results/hashes andselected_evidence_manifest.json records research-reading copies. Localreading sync does not implycommit/push/publication.
