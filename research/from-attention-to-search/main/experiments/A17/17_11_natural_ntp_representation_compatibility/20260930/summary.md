# Summary: natural NTP representation prediction of local update compatibility

Primary Anchor: [natural NTP compatibility](../../../../problem_anchors/17_shared_and_interference_learning/17_11_natural_ntp_representation_compatibility/17_11_natural_ntp_representation_compatibility_anchor.md)  
Frozen Protocol: [registered experiment](protocol.md)  
Full evidence: [Detailed](detailed.md) · [中文](summary_cn.md)  
Result: **eligible primary result, `NON_SUPPORT`; finite-step confirmation `NOT_RUN_BY_BRIDGE`; 14 structural readers `NOT_RUN_BY_GATE`**. Researcher scientific judgment: **Unknown**.

## 1. Purpose

Test whether representations available before seeing the true next token predict the continuous compatibility of two natural next-token-prediction updates at one shared attention matrix.

## 2. Hypothesis

On unseen documents, a predictor using only the frozen matrix-input representations will reduce mean squared error for the gradient inner product \(K\) by at least 5% relative to the TRAIN-set constant. The live rival is that the true targets and downstream error signals leave too little extractable information for these registered readers, even though \(K\) is exactly factorized by representation and error signal.

## 3. Analysis Method

- Freeze the S7 33B-training-token checkpoint and final attention output matrix; form one 256-token-prefix/one-real-target event per document, then 32,768 TRAIN pairs, 512 DEV pairs, and 1,024 endpoint-disjoint CONFIRM pairs. Fit a four-feature geometry reader and a full-\(c\) reader on true TRAIN \(K\), select with DEV, and seal predictions before releasing CONFIRM truth.
- On CONFIRM, score \(Q=1-\mathrm{MSE}(q_*)/\mathrm{MSE}(m_{\rm TRAIN})\), with 2,000 pair bootstrap draws and a registered support threshold of 0.05. A 95% interval wholly below 0.05 is `NON_SUPPORT`.
- Separately calibrate common temporary \(W\)-only SGD steps on DEV for finite loss effects; run the 14 structural readers only if the primary result supports the threshold.

## 4. Conclusion

**The registered representation-only prediction claim is not supported in this fixed setting.** DEV selected the full-\(c\) reader before opening CONFIRM. Its CONFIRM \(Q=-0.000138\), conditional 95% CI \([-0.002768,0.002294]\), lies wholly below the registered 0.05 threshold. The trained constant has MSE 0.638792 and the selected reader 0.638881 over 1,024 document pairs. The geometry reader has \(Q=-0.001285\), CI \([-0.003768,0.001165]\). All data, numerical, fit, sealing, and identity gates needed for this primary comparison passed; these are scientific `NON_SUPPORT` values, not an implementation failure. [Raw prediction and truth](/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/runs/full_20260929T175901Z/result/frozen/confirmation_predictions.npz) · [registered analysis](/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/runs/full_20260929T175901Z/result/analysis/primary.json).

Registered descriptive readings completed after unsealing, without reselection: Spearman correlation of predicted versus true \(K\) was −0.0043 for full-\(c\) and −0.0072 for geometry; mean pairwise gradient cosine was 0.00101, and 508/1,024 \(K\) labels were positive. Their conditional intervals and provenance are in [secondary.csv](/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/runs/full_20260929T175901Z/result/analysis/secondary.csv). These descriptive values do not alter the primary verdict.

| Registered decision | Observed value | Eligibility | Outcome | Evidence |
| --- | --- | --- | --- | --- |
| Primary \(Q\), CI lower >0.05 for support; upper <0.05 for non-support | full-\(c\) \(-0.000138\), CI \([-0.002768,0.002294]\) | Eligible, frozen DEV choice; 1,024 pairs | `NON_SUPPORT` | [primary.json](/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/runs/full_20260929T175901Z/result/analysis/primary.json) |
| Finite-step DEV bridge: both step sizes need ≥80% resolved first-order effects, plus other guards | Largest candidate: 62.5% at full step, 50% at half step; other tested candidates lower | Qualification failed only for the finite bridge | CONFIRM finite panel and \(Q_I\) `NOT_RUN_BY_BRIDGE` | [DEV finite rows](/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/runs/full_20260929T175901Z/result/finite/dev_finite.jsonl) |
| Structural panel requires primary support | Primary `NON_SUPPORT` | Prespecified gate | 14 readers `NOT_RUN_BY_GATE` | [condition ledger](/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/runs/full_20260929T175901Z/result/structure/condition_ledger.json) |

![Observed and predicted K, with conditional Q intervals](../../../../../../../daily_research_reports/backup/2026/09/0930/figures/primary_q_and_prediction.png)

**How to read:** the left panel shows predictions clustered near the training mean while observed \(K\) spans both signs; the right panel shows both Q intervals near zero, far below the registered 0.05 line. Each point is one CONFIRM document pair. [Figure source and provenance](../../../../../../../daily_research_reports/backup/2026/09/0930/figures/SOURCES.md).

**Claim boundary.** This rejects the 5% operational threshold for the specified 281-million-parameter S7 backbone, one 33B-token checkpoint, one matrix, this DCLM document-start population, and these trained readers. It does not identify irreducible conditional variance, exclude stronger readers or other representations, establish natural conflict groups, measure a qualified finite-step loss prediction, or justify shared/separate training or Router design. The 95% interval conditions on the fitted readers and this corpus; historical event exposure is not fully established.

**Next decision:** researcher judgment is **Unknown**. An **AI suggestion for discussion**, not an authorized experiment, is to decide whether this result closes the present operationalization or warrants one explicitly revised test of the most plausible remaining rival: limited predictor/sample capacity versus weak information in the matrix input. Any new test needs a fresh prospective contract and independent confirmation data; this run's CONFIRM cannot be used for tuning.
