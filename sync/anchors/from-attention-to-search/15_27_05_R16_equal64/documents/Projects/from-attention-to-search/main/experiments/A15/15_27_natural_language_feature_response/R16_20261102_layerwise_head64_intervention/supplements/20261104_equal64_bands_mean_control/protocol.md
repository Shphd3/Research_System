派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_equal64_bands_mean_control/protocol.md`。
[精确原始文件](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_equal64_bands_mean_control/protocol.md)；研究修改仍回到原件。

---

# Protocol: equal64 spectral bands with/without reference mean

## 0. Authorization snapshot
APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_COMPLETE_FROZEN_ANALYSIS by current explicit user request. Existing15_27_05 Anchor/R16 question retained. No new Focus or training question. Role: robustness and operationalization test. Max2 authorized RTX5090 Spot, registered5090-2-spot/shphd-lite-0911 only; no H100, model training, classifier, PCA refit, new conversation, commit, push or publication. Scientific acceptance remains Unknown. A-F explicit current band/mean instruction plus inherited R16 data/measurement; G inherited resource authorization. Engineering batching, chunk layout and precision guards chosen within that authorization.

## 1. Objects, purpose and rival
Question: at equal rank64, do spectral position and mean restoration change the depth profile of final native top1 retention? Leading64 versus remaining960 previously changed rank/energy. This round fixes rank across16 disjoint contiguous PC bands. Main rival: mean/energy/native geometry rather than semantic generality or complexity drives results.
For row h:1x1024, TRAIN mu:1x1024, Q_B:1024x64, coefficients(h-mu)Q_B:1x64, reconstructed vector:1x1024. add_mean=mu+(h-mu)Q_BQ_B^T; no_mean=(h-mu)Q_BQ_B^T. No raw hQ projection, norm compensation, temperature or fitted readout. The two differ by mu, not only by a semantic label.

## 2. Frozen data and interfaces
Exact officialQwen3-0.6B Base, checkpoint hashcd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba,28blocks,D1024. Original R16 tokenizer and all28 means/full bases from same60TRAINdocs x160 positions32..191=9600. No R15 substitution or evaluation fitting. Main175independent doc families x4positions=700; auxiliary37/the positions separate,180physicaldocs total. Already exposed exploratory panels. Target current t predicts token[t+1].192valid tokens paddedto256ID0, native causal mask and positionIDs0..255. Valid prefix only is perturbed; padding unchanged.

## 3. Conditions and controls
For layers1..28, sixteen bandsPC1-64,65-128,...,961-1024, each add_mean/no_mean. Each run changes one layer only, then native remaining blocks/final RMSNorm/frozen lm_head. Separate all_prefix and target_only. Each target-only sequence changes exactly its one selected position; do not jointly change four target positions.
Controls: original identity; old mean-only and random64 reused; zero vector and full-centered h-mu newly measured. Truefullidentity via h and mu+(h-mu)I, separate from h-mu. Same TRAIN reference mean for every band and condition. Full1024direction PCA reconstructs identity numerically; no-mean allPC must instead equal h-mu. Band energy defined as ||(h-mu)P_B||^2/||h-mu||^2, identical for both mean modes. Also report actual original norm ratio, perturbation norm, reference-mean norm, output entropy and NLL; do not relabel ||g_B-mu|| as band energy.

## 4. Numerical stages and freeze
CPU: strict required asset checks, exact source hashes, shape/orthogonality/rank/eigengaps,all16 component sum, affine-vs-linear identity. BF16 native model; FP32 projection then castBF16; FP32 output logsoftmax; FP64 algebra checks<1e-8. Embedded GPU smoke must check all28 no-op suffix logits<=0.5 and NLL<=0.05, fullidentity cast relative error<=1e-6, actualhook vs suffix at1/14/28 for bands0/7/15 and both modes/scopes with same tolerances, causal prefix invariance<=0.5. Replay all737 original states exactly, baseline NLL<=1e-6/top1 exact. Lastlayer scopes identical. Recompute newhead64 against old rows and record discrepancies; no tolerance widening.
Condition batch4 is engineering only. Smoke compares batched and standalone logits<=0.5/NLL<=0.05 and records top1 changes; if discrepancies exceed guards, fall back to standalone condition batches before fullsweep. Freeze scientific protocol, config and code before GPU, amendments append only.

## 5. Metrics, aggregation and selection
Primary originaltop1ID agreement, doc-equal: average positions within eachdoc/group then average docs. Overall700positions has4/doc. Frozen format/common/other groups reuse original fullmodel reference groups: common=top1516validIDs out151651 by independent4194304TRAIN token counts, format precedence Unicode whitespace/P. Other is not finer semantics. Report both panels separately.
Secondary originaltop1P/rank; true successor P/rank/NLL(nat);KL(full||condition), entropy(nat); exacttop10 IDs/P; band energy and perturbation/norm. Deterministic max ties minimumID, top10 value desc/IDasc. Paired position/unit mapping unchanged.2000 doc bootstrap seed20261104 pointwise95% intervals, not simultaneous28x16 confirmation. Paired mean differences use identical documents. No selected optimal band is a confirmed winner; full matrix retained.
Case rules frozen before results: existing9fixed examples, especially index211polygons,284humans,676same. Show complete visibleprefix,0/1based position,current and successor ID, baseline and allbands; presentation layers1/14/25/28 fixed; all28 raw rows available. Outcome-selected examples, if any, explicitly separated. No new classifier/labels.

## 6. Resources, recovery and coverage
One single-node5090-2-spot job,2 independent document shards, embedded smoke first. Max GPU concurrency2. Expected about1.4million position conditions; numeric/top10 compressed per-document chunks, estimated<2GiB; model once/device, condition batches4, expected10-45minute active time depending measured throughput. CPU statistical analysis and plotting only after outputs. Atomicchunks bind scientific/code freeze and completion flag, can resume same freeze without recomputation; no duplicated live job. Source/data mismatch stops dependent work.
Coverage ledger: equalrank16bands x28layers x2scopes; paired add/no_mean; mean/zero/full-centered controls; group/energy analysis; fixedtext examples; integrity/artifact review. Each completed factual result EXPLORATORY; failed conditions retained.

## 7. Decision branches and deliverables
Support a bounded stage-dependent band preference only when actual paired results and doc intervals support it; if mid/tail does not outperform equalrankhead, narrow earlier960-rank inference. If mean removal changes the ordering, qualify mean-dependent claims. Mixed/flat outcomes weaken simple ordering. Numerical/asset failure or weak group coverage means insufficient evidence, not no semantics. No semantic hierarchy or compensation mechanism follows from retention alone.
Deliver three matched add/no_mean layer-by-band heatmaps and paired difference; selected-band layercurves; energy/norm/NLL controls; fixed fullcontext top10 cards/tables, all perposition compressed outputs/document summaries/config/code and execution receipt. Interpret observations, then conditional implications for researcher assumptions, rival energy/mean explanations and one unresolved boundary. Researcher current request explicitly authorizes combined results and AI recognition update; no additional approval questions.


## Amendment E1: engineering smoke, before any evaluation output
2026-11-04: initial smoke failed on layer1 band449-512 add_mean all_prefix: full-hook batch1 versus cached-suffix batch5 NLL difference0.082834nat, maxlogit0.375. Original failure and frozen source retained in provenance/freeze_attempt1.json and run_gpu_attempt1.py. This was a mismatched-batch numerical comparison, not an observed scientific result. Repair: compare actual full hook and cached suffix at identical batch1; separately audit four-condition versus standalone-condition suffix at all34conditions on fixed layers1/14/28. Keep original0.5logit/0.05targetNLL guards. If any such guard or top1 agreement fails, use condition_batch1 for all evaluation conditions; no result-dependent band selection or tolerance widening. The planned case, model, PCA, outputs and metrics remain unchanged. First batch-sensitivity implementation also compared every vocabulary logprob; the qualifying quantity is the registered true-target NLL. Effective batch is saved in smoke and completion. No evaluation chunk existed before repair. Routine implementation repair is within explicit user authorization.


## Amendment E2
See [singleton batch repair](amendments.md):5auxiliary-onlydocuments recomputed withoriginalbatchshape underunchanged numericalguards; mainpanel unchanged. Execution-sideprotocol remains original frozen snapshot.
