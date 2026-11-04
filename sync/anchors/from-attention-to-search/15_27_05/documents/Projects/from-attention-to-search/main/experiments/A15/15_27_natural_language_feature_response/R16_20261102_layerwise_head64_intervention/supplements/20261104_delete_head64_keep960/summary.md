派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_delete_head64_keep960/summary.md`。
[精确原始文件](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_delete_head64_keep960/summary.md)；研究修改仍回到原件。

---

# Deleting head64 while retaining960: paired native prediction results

## Purpose
Determine how removing the first64 centered PCA directions of one Qwen3-0.6B-Base layer changes its final next-token predictions, compared with retaining those directions. Use the exact same model, tokenizer,28 layer-specific PCA bases and737 fixed positions as R16. Separate current-position and whole-prefix interventions; continue the unchanged remaining blocks and native final norm/head. No model, classifier or PCA fitting.

## Observations and bounded recognition update
On175 documents/700 natural positions, current-only keep64 versus delete64 original-top1 preservation is77.43/50.71% at layer1,74.71/57.43% at14,34.29/51.43% at25,and23.00/32.57% at28. The paired delete-minus-keep differences are−26.71pp[−31.43,−21.71] at1,+17.14[11.43,22.71] at25,and+9.57[4.57,14.71] at28. Intervals are exploratory pointwise document bootstraps, not a confirmed ranking over28 layers. Whole-prefix deletion is especially destructive early: at4 it preserves1/700 versus78/700 under retention; at25 deletion/retention preserve40.29/30.14%.

Early keep64 wins despite retaining fewer dimensions and less average centered energy:49.37% versus50.63% at1,and44.97% versus55.03% at14. Its advantage cannot be explained by retaining more dimensions or greater mean energy alone. Later complement advantages remain confounded by larger rank/energy; this does not demonstrate that the same information moves from spectral head to tail.

At28, original other-nonformat IDs preserve27.60% under deletion versus2.00% under retention, a25.60pp difference[17.47,32.93]. Point differences for format/common-nonformat are7.41/3.89pp with intervals crossing0. These are frozen frequency categories, not semantic grain. Deletion still produces40.71% format and46.71% common-nonformat first choices; head64 is not an exclusive store of common predictions. At28,344/700 positions preserve neither operation,33 both,128 retention only,and195 deletion only. The shared mean/context/suffix prevents independent-information or functional-interaction claims.

Fixed X-ray text illustrates a reversal: same is preserved under shallow current-only keep64 but strongly weakened by deletion; at28 deletion selects same19.03%, while retention gives0.4729%, versus full70.04%. Same is a frequent ID expressing a contextual relation. Fixed polygons/humans examples retain failures: neither final-layer operation restores their original candidate support. Both keeping and deleting can still output generic function words. The stage-dependent mixed-support interpretation is an AI reading; intrinsic layer importance, coarse/fine semantics and researcher acceptance remain Unknown.

## Hypotheses and rivals
Head64 may contain patterns reused across many inputs. This is a working hypothesis, not the meaning of PCA variance. Deletion and retention change rank, energy and direction differently, and the remaining network may compensate or construct distinctions later. Three same-rank random deletions produce much higher fidelity but retain approximately94% energy, so energy and directional specificity remain unresolved.

## Procedure and validity
Main175/700 and auxiliary37/the panels are separate,180 physical documents in total. Each layer uses the original R16 TRAIN mean/basis fitted on60 discovery documents/9600 positions. New formula is h'=h−(h−mu)QQ^T; the TRAIN mean remains. Whole-prefix changes every valid position, target-only changes one independently replicated position. Native BF16, FP32 projection and probability metrics, FP64 algebra checks. Original28-layer target states and native NLL/top1 exactly replay on all737 positions. Old keep64 is replayed before reuse; grouped summaries reproduce within4.55e−13. Complement-versus960-basis error is3.13e−13; native hook/suffix guards pass. Deterministic max/boundary ties use ascending tokenID. Independent candidate/probability, prefix/shift and document regrouping checks pass.

## Boundary and reading
This is one frozen model and previously exposed English panel, with a narrow original reference cohort. Equal deleted rank does not equal energy. Higher fidelity is not higher actual-target accuracy or complete semantic preservation. Joint failures need not be functional interaction; successes need not be independent redundancy. No new experiment is automatically launched.

[Complete Chinese report](summary_cn.md), [full inputs and28-layer candidates](casebook_cn.md), [data and reproducibility](assets_and_data.md), [protocol](protocol.md). Job pt-ay14f1yi completed on two authorized5090spot GPUs; no training, H100, commit, push or publication.
