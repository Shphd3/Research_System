# Execution certificate — R16

Job: pt-od3opbw5. Monitoring owner: current1031spectral conversation /root.
Stage: user-authorized embedded fit+smoke followed by frozen layer intervention sweep.
Resource profile: 5090-2-spot; workspace share-space; cluster computing-cluster-5090-01g; worker spec n12lp.nn.i10a.2; node count1; GPUs2; quota spot.
Image key shphd-lite-0911; expanded URL registry.cn-sh-01g.sensecore.cn/ccr-zhicheng-03/shphd-lite-0911:shphd-mig-20260910161423.
Runtime: scripts/runtime.sh reuses mounted SM120torch2.8/cu128 and pinned Qwen3transformers4.53.3. Never install into base.
Submission: Research_System/templates/execution/acp_submit_template.sh; envelope canonical ACP compatibility entry point; loopback port18095 uses inherited qualified compatibility bridge. Exact command/tuple in /data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/acp_receipts/submit-r16-layerwise-head64-20261102T055907Z.json.
Run root: /data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R16_20261102_layerwise_head64_intervention; command bash scripts/launch.sh. Durable logs acp_receipts/pod and logs/rank0.log, logs/rank1.log.
Weights/tokenizer frozen, no optimizer/model or classifier training; each worker handles an independent document shard after common TRAIN PCA/smoke. Verified terminal:SUCCEEDED, both90document shards completed;28PCAfits/smoke and249843measurementrecords validated. Worker evaluation times277.71/274.79s, GPUpeak1.314/1.315GB. Original max-tie ordering issue repaired onCPU with chunks/probabilities unchanged, all737no-op native states/NLL exact. Scientific acceptanceUnknown.
