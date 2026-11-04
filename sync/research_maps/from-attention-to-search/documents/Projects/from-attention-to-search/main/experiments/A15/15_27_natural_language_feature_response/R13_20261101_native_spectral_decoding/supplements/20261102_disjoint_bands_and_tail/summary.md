派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R13_20261101_native_spectral_decoding/supplements/20261102_disjoint_bands_and_tail/summary.md`。
[精确原始文件](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R13_20261101_native_spectral_decoding/supplements/20261102_disjoint_bands_and_tail/summary.md)；研究修改仍回到原件。

---

# Isolated spectral bands and tail: native decoding with full contexts

Same qualified frozenQwen3-0.6B-Base block27pre-finalnorm vectors/TRAINmean/PCA/nativeRMSNorm+tiedhead.175documents700naturalpositions,exploratory;37auxiliaryrows preserveR13batchshape butareexcludedfromprimaryanalysis. No training/newPCA/classifier/newtext/transformerforward.

One-basedhalf-openPCintervals:16–31,32–63,64–127,128–255,256–511,512–767,768–959,960–1024. IsolatedbandplusTRAINmean,notcumulativehead. Widthsdiffer;matched64d512–575,768–831,961–1024comparewith64–127. Literalindices/dimensionsandallstatisticsinthelinkedtables. Fullvisibleprefix,currentinputID/fragment,zero-basedtandone-basedt+1andtruesuccessorareexplicit. All700prefixescheckedagainstoriginaltokenwindows;futureoriginalsentence/referenceisclearlynotvisibleinput. Threeprespecifiedcases134:144,242:78,434:160and12oldoutput-blindcasespreventshowcaseselectionbynewoutputs.

NLLmeasuresactualsuccessorprobability,KL(full||band)fidelity,entropyuncertainty,top1/top10recoveryreferenceagreement. Mean-only/full/head64arefixedreferences. Top20recordsincludeactualprobabilitiesandlog-probabilityliftvsmean. Highentropy,rareforeignfragment,orasinglesemantic-lookingworddoesnotbyitselfidentifychaosorsemantics.

Boundedcontextcontrol:onefixedseed20261103derangescoefficientsacrossdifferentdocumentsWITHINexactcurrenttokenIDon312positions/158documents,keepingoriginaltargetandreference. Marginalsarepreservedonmatchedpositions. PositivepairedNLLgainshowscontext-linkedpredictiveassociationbeyondcurrentID/marginals,notcausalsemantics;source/style/syntax/frequencyremainrivals. Pointwise95%document-bootstrapintervals(2000draws,seed20261104)conditiononthisonepermutation;notmultiplicity-correctedconfirmation. Unmatchedpositionsremaininthe700primarypanel. No-gain/wideintervalisnotabsenceofinformation.

TheChineseSummarypreserveseverymaincontextandliteraldecodertable;theseareoriginalEnglishprefixes. Allnaturalpositioncasebooksandrawoutputsremainexecution-side,withselected12-casebookinproject. Nativeisolatedbandfailuredoesnotprovefullmodelstoresnoiseorwhatthebandcancontributewhencombined. Tailreferenceeigenvaluesarenonzero;basisreuseisnotindependentreplication. MechanismandsemantichierarchyacceptanceUnknown.

|单独保留区间|维数|训练参考方差|目标NLL↓|与原模型KL↓|原首选一致率|真实系数相对同token异文档的NLL增益 [95%区间]|
|---|---:|---:|---:|---:|---:|---:|
|PC16–31|16|8.64%|9.139|6.786|5.00%|0.889 [0.681, 1.113]|
|PC32–63|32|9.80%|9.299|6.951|6.71%|0.893 [0.699, 1.089]|
|PC64–127|64|11.03%|8.956|6.539|7.14%|1.073 [0.862, 1.296]|
|PC128–255|128|12.55%|8.662|6.304|7.71%|1.350 [1.161, 1.548]|
|PC256–511|256|13.41%|8.037|5.698|5.86%|1.941 [1.682, 2.200]|
|PC512–767|256|6.87%|8.769|6.368|3.00%|1.358 [1.151, 1.567]|
|PC768–959|192|2.77%|9.416|7.038|2.57%|0.942 [0.758, 1.132]|
|PC960–1024|65|0.54%|10.203|7.824|2.29%|0.235 [0.152, 0.323]|

[Chinese complete figures/contexts and bounded reading](summary_cn.md) · [fixed12casebook](../../../../../../../../../../UNAVAILABLE.md) · [all700contexts](../../../../../../../../../../UNAVAILABLE.md) · [protocol](../../../../../../../../../../UNAVAILABLE.md) · [rawstatisticstable](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R13_20261101_native_spectral_decoding/supplements/20261102_disjoint_bands_and_tail/evidence/summary_metrics.csv).

## Bounded factual reading

Thelast65PCs960–1024produceonlyfourtop1IDsacross700positions:openingparenthesis383,comma305,space11,NBSP1. This isconcentratedbackgroundformatbias,notalargevarietyofrandomgibberish. Yetlast64PCs961–1024improvetrue-targetNLLvsonefixedsame-tokenother-documentcontrolby0.2259nats[0.1384,0.3154],312positions/158documents;on109non-format/non-common-targetpositionsfrom90documents,0.3855[0.2076,0.5720]. Context-linkedpredictiveassociationexists,includingbeyondpunctuationtargets,butisnotanexternalsemantic-granularitylabel.

Fixed134:visibletriangle/polygoncontextrequiresaplausiblecategorycontinuation;isolatedbandtop3remainspunctuation/space/functionIDs. PC16–31raisespolygonsabout102timesvsmeanbutonlyto0.000647%andrank1088;last65to0.00000553%,rank9864,versusfull40.4467%,rank1. Repeatedpolygonsalreadyintheprefixalsoleavescopyingasarival. Fixed242:theorhuman-relatednounphrasescouldbeplausibleafteraffecting;fullactualhumansrank6,not1. IsolatedPC256–511gives0.001079%,rank1064,last65about0.000138%,rank3555,versusfull2.6457%. Thiscasehasnomatchedcurrent-tokencontrol. Fixed434:relationfragmentsamehasfull70.0425%,rank1;PC256–5110.050997%,rank77,about34timesmean;last650.002478%,rank453,withtop3format. Itsindividualtailcontrolisnegativeevenwhentheaggregateispositive.

Otherfixedcounterexamplesarepreserved:410wavesrises5.76timesmeanbutstill0.0000752%,rank5338;255thatimprovesyetremainsrank14;281The/419Whatworsenvsmean;096digit5is0.001954%,rank569,versusfull99.8784%. Nobest-case-selectionorsemanticorderclaim. Backgroundoutputsdominatewhilecontextualprobabilitymodulationremains;thisrounddoesnotdirectlyrecoverstableconcretecontentfromtailalone.
