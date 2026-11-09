# Execution certificate: R16 complement deletion

Job:pt-ay14f1yi. Currentconversation/root issolecompletionmonitorowner.
Authority:2026-11-04directuserrequest, inheritedatmost2RTX5090spot, noH100/training.
Profile:5090-2-spot;workspace:share-space;cluster:computing-cluster-5090-01g;workerspec:n12lp.nn.i10a.2;nodes1;GPU2;quota:spot.
Image:shphd-lite-0911;expandedURL:registry.cn-sh-01g.sensecore.cn/ccr-zhicheng-03/shphd-lite-0911:shphd-mig-20260910161423.
Entry:Research_System/templates/execution/acp_submit_template.sh;canonicalenvelopeACPcompatentry;privatequalifiedloopback18097. Dryrunverifiedsame tuple.
Activation:scripts/runtime.sh reusesR16mountedSM120Torch2.8/cu128 pluspinnedQwen3Transformers, noinstallinbase.
Command:bash scripts/launch.sh,rank0smoke then2independentdocument shards.
Runroot:/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_delete_head64_keep960;logs:acp_receipts/pod andlogs/rank0.log,logs/rank1.log;atomicresults:analysis/chunks;smokeevidence:audit/03_numerics_smoke.json.
Initial platform state: STARTING; runtime progress was not yet verified at submission. ScientificacceptanceUnknown.

Verified completion: platformSUCCEEDED;both90documentshards complete. Evaluation340.63/329.96s;GPUpeak1.310/1.310GB;newPCA/training0.207097combinedrecordsvalidated. All737originaltargetstates/NLL/top1 replayexact. Seeaudit/validation.json andcompletion_manifest.json.
