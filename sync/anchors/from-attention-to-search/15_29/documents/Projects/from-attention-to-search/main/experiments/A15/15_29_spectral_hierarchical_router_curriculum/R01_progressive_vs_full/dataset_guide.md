派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_29_spectral_hierarchical_router_curriculum/R01_progressive_vs_full/dataset_guide.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_29_spectral_hierarchical_router_curriculum/R01_progressive_vs_full/dataset_guide.md)；研究修改仍回到原件。

---

# Calibration, teacher and training identity

Final V5 uses the existing dclm_pair_v1 first30B training view and tokenizer_qwen3_0p6b_base. Source manifest SHA256 is8a91bdbb0eb537bd80612015b99f178ca1cbb54a2fa7cf8442ab1eae7f0a2f2d. It samples262144/262144/16384valid positions for A/B/C5 across1152/1174/72physicaldocuments, maximum256positions/document. C5 seed103121; A/B unchanged from seed103120. Complete original2048input contexts are retained. Physical document boundaries are observed151645 separators, not a new training attention mask. Context documents do not cross calibration splits; C5 also excludes priorC1/C2/C3/C4. Semantic near-duplicate separation is unverified. Calibration never reads final validation.

Exact teacher is model_dense_33b at token033000000000, stateSHA256a0b21cb3b8c5217aa5638101ed60c28747edf474bd33ae62f91cda57952586cd. Each layer's actual learned post-norm2 FFN input is saved as1024dimensional FP32 arrays from RTX5090BF16 inference. The actualV4extraction ran in om-qwhewj2p;30.08s excludes loading/hash/startup/fitting. These arrays are inputs to fitting and independentchecks; their existence does not certify stable targets.

Final production qualification, passed for all8layers, is audit/offline_target_qualification_v5.json. V1–V4 failures remain execution-side. The fixed tree is an artificial contextual supervision target, not discovered natural semantic levels or static token-ID labels. Formal training generates targets online from the same full causal context, with no materialized50Bcache. Bothgroups use the same frozen tree/scales/temperatures and expert numbering4rootbit+2middlebit+tailbit.

The formal train/validation/dataorder/mask/optimization contract is the corrected ordinaryMoE baseline, including actualDensehistorical batch/mask fingerprint checks through10B. Validation uses the same first32sequences/65536targets and cannot change tree/bias/weights. A small calibration panel does not certify complete50Bdistribution coverage.

Actualpayloads remain under /data/250010109/MoE_Router/experiments/20261031_spectral_hierarchical_router/{inputs,targets,runs}. Registered actual calibration assets are data_spectral_router_calibration_v5_20261031 andrepresentation_spectral_router_dense33b_calibration_v5_20261031. Read access snapshot: assets/checks/20261031_spectral_hierarchy_v5_targets_actual.json. Production trees/checkpoints are registered only after actual saves.
