# R01 joint engineering freeze receipt

A/B smoke and uninterrupted-versus-external-resume exact replay passed. Each formal arm has **229,113,856 valid prediction tokens and 874 updates**. Required saves/evaluations are at steps 0/437/874, or tokens 0/114,556,928/229,113,856. Freeze time: 2026-11-06T16:50:35Z. No final-test model metric selected the design or budget; test metadata/examples were inspected.

The common batch is 262,144 targets:4 ranks ×16 sequences ×2 accumulation ×2048 positions. Warmup is 87 updates /22,806,528 targets, followed by constant3e-4. The first update uses zero LR, retaining the verified trainer convention. Full hyperparameters are in the [frozen configuration](supporting_sources/common_frozen.json), SHA256 `dd768489b9a58a49c09b85fedb9009bb80d7530a63dd235a9bb960265e16f3d5`. Non-profiler median step times were 2.0798338661s (A) and2.0384610565s (B); the registered even-step budget rule reserved one hour for paired training plus one hour for evaluation/IO. Wall time selects this bounded budget; quality uses the matched token coordinate.

Frequency is exact supervised-target exposure in this round's cyclic training stream. Positive-frequency type tertiles have integer thresholds 49/447; ties remain together, and zero exposure is separate. NLL is token-weighted, with the entire frozen test split also evaluated.

| Bucket | Token types | Test tokens | Test coverage |
| --- | ---: | ---: | ---: |
| low | 30259 | 1481 | 0.21147868% |
| mid | 29950 | 20752 | 2.96327182% |
| high | 30056 | 677902 | 96.80068884% |
| unseen | 61671 | 172 | 0.02456066% |

The [source freeze receipt](supporting_sources/joint_freeze_receipt.json) and [formal frequency manifest](supporting_sources/frequency_manifest_formal.json) preserve source bytes. Separate execution data/frequency_smoke and data/frequency_formal retain both definitions. Config/source hashes currently match the freeze.

The CPU initial_parameter_hashes.json used seed 17 and qualifies the implementation rule. Actual saved initial states use seed 20261106 and receive their own tensor/overlapping-router-row audit. Exact A smoke recovery does not automatically qualify external recovery of every B/formal checkpoint.

Job pt-ds9bdaxb uses one 4-H100 reserved node. Formal A had started at this receipt’s registration time; this engineering receipt alone did not establish paired completion, a final comparison or scientific acceptance. Later completion/results have their own records. Scientific acceptance remains Unknown.
