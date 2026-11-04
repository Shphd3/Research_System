派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R05_distance_attention_20261028/protocol.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R05_distance_attention_20261028/protocol.md)；研究修改仍回到原件。

---

# R05 frozen Protocol


Exact executable settings: [config.json](../../../../../../../../UNAVAILABLE.md). Frozen texts: [B.jsonl](../../../../../../../../UNAVAILABLE.md), [A.jsonl](../../../../../../../../UNAVAILABLE.md). All values below are fixed before forwards.

## 1. Identity and authorization

R05. Current integrated user message explicitly authorizes both experiments through analysis/delivery. No additional review gate.


## 2. Anchor alignment

Existing A15_27 owner revised under the explicit replacement; no new Focus/Work/Codex task.


## 3. Purpose and rivals

B distance-dependent content response; A extra endpoint coactivation. Frequency/lexical/order rivals remain.


## 4. Measurement objects

Native E16 local block27MLPinput and native14layerjoint A22 sharedz. Rawz, native norm contribution and normalized contribution separate.


## 5. Data and provenance

960 manually constructed controlled prefixes;24independent scenario families,12discovery12heldout.120unchanged real R04documents with original splits. No sealedTEST.


## 6. Supervision and fitting

No model/dictionary/classifier training. Discovery-only candidate selection/scaling; original domain labels are annotations.


## 7. Model and frozen variants

One frozen Qwen3Base. E16FP32Top32;A22BF16native saved normalization/gate,14inputs. Both extracted per Base forward.


## 8. Objectives and optimization

NOT APPLICABLE: inference only,allrequires_gradFalse,eval,no_grad. No optimizer or parameter updates.


## 9. Conditions seed and checkpoints

Seed20261028;Bfiveexactdistances,4versions,2wordings. Immutable hashes inconfig. ExistingMIGonly.


## 10. Primary B metrics

E=|cX-cY|-(|cX-cXU|+|cY-cYU|)/2,wordings averaged within family. Scale target RMS on480discoveryonly. Select positive top16at16/144 with>=4family activation support,unionno refill. Exact4096sign-flips aboutminimum.10;5000paired familybootstrap. PooledBH two dictionaries x all selectedfeatures x(5distances+nearfar). Stable requiresmean/CI>.10,q<.05,>=4heldoutfamilyactivation and bothwordingmeans>0.


## 11. Primary A metrics

Capture unmodified nativeSDPArotatedQK;selectedqueriesoftmax causal weights. EachbinN>=10,notfullytied;topceil10%,middle40–60%;nearestcontrolswithoutreplacement,caliper8,tokenidentitystatus/punctuation matched. Missing remainsNA. Feature averageincludingzeros;pair→head→query→documentequalweights.40heldoutprimary.2000docbootstrap,9999signflips about.001,min10matcheddocs. PooledBH freq3/Bcategories3/individualBcandidates x5bins x2wordstrata x2dicts. Punctuation/R04roles/low supportdescriptive.


## 12. Known good bad confusing

Replay identity and truncatedvisibleprefix invariance. Highfrequency joint hits can be trivial. Distantcontent response is not longrangeexclusive; no outputcorrectnesslabel is asserted.


## 13. Stage contracts

Freeze fulltexts/config/code/sourcehashes;qualify<=16;Bdiscovery;freeze scales,candidates;Bheldout;A120;statistics;fourfigures;readable/detailedreport. Failedbranchstopindependent branch continues. No tolerance adjustment after results.


## 14. Artifacts and provenance

Chargeeveryattemptbeforeforward;atomic outputs,resume skips verifiedcompleted sequences. Save fullBtargetz,CSRAtokenz,selectedqueryweights,pairs,rawdecoder/scalednorms,RMS,allstatistics,codehashes. No deletion.


## 15. Decisions

Bstablefar:far supported;nearstable and significantnear-far:near response with far attenuation;others insufficient. Astablepositivejointdiffsupportsassociation;nonpositive evidence may weaken if CI upperbelowminimum;otherwise insufficient. No nullproof.


## 16. Cannot claim

No causal transport,featurefunctionality,correctsemanticunderstanding,frequencyformationcause,independentlayeractivation,semanticdepthorexpertplacement.


## 17. Freeze and amendment ledger

User integrated replacement is run authority. Machine freeze is pre_forward_freeze.json. OldR04/R03protocols/results unchanged. Anyrepair records engineering deviation andspentbudget;no scientificthresholdchange.
