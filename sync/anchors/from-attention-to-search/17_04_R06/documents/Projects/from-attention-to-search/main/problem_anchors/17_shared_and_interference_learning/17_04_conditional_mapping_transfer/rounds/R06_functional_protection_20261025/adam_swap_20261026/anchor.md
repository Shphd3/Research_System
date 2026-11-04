派生阅读副本；原件位置：`Projects/from-attention-to-search/main/problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/rounds/R06_functional_protection_20261025/adam_swap_20261026/anchor.md`。
[精确原始文件](../../../../../../../../../../sources/Projects/from-attention-to-search/main/problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/rounds/R06_functional_protection_20261025/adam_swap_20261026/anchor.md)；研究修改仍回到原件。

---

# R06 supplement: Parameter versus Adam state in ordinary one-step effects

## 1. Problem Definition
Atstep120,ordinaryupdatesfromF-historyharmindependentoldDEVmorethanfromU-history. Thisroundonlyasks whethercurrentparameters,Adammomentsortheirinteractionparticipate. ItdoesnotretestFprojectionoroptimizeaccuracy. Currentuserexplicitlyauthorizesboundedautomaticdiagnostics. Same17_04/R06owner, nonewindependentquestionortraining.

## 2. Physical Priors
ActualAdammovementdependsjointlyoncurrentgradientandhistoricalfirst/secondmoments. Parametersaffectcurrentgradientandlosscurvature. Swappingmomentscreatescounterfactualcombinationsthatmayneveroccurinnaturaltraining; localeffectsarenotlong-termhistorydecomposition.

## 3. Falsifiable Hypotheses
A: momenteffectsareconsistentacrossseeds/batchesatfixedtheta. B: effectmainlyfollowsthetaandmomenteffectsmall. C: momenteffectdependsontheta. D: effectsreversewithbatch, limitingstability. E: oldimprovementcostsnewlearning. These cancoexist andmustbecheckedwithold/newCEseparately.

## 4. Mathematical Model
Forseed s,batch b,thetaorigin p andmomentorigin m in{U,F}, restoretheta_pandAdam120withnamedexp_avg/exp_avg_sqfromm. Keepstep,learningrate,betas,eps,decayandgroupsfixed. L=(sum36new+sum4old)/72; globalclip1thenordinaryAdamstep,actuald=theta_afterFP32copy-theta_before. Define Delta_old/new(p,m,b)=meanfixedDEVCEafter-before. Momenteffectatp=Delta(p,F)-Delta(p,U);thetaeffectatm=Delta(F,m)-Delta(U,m); interaction=Delta(F,F)-Delta(F,U)-Delta(U,F)+Delta(U,U). Thesearerandomized-freefinitesame-stateoperationsconditionalonfixedassets, notuniversalcausalhistoryparameters.

## 5. Computational Realization
Threeseeds29/43/71,sixoriginalcomplete120states,fourcellsperseed,3prelockedTRAINbatchesindices120/121/122. Everybatch independentlystartsstep120; neverthreestepcontinuation. ReuseprioroldDEV64anditspre-existingpairednewDEV64, noTESToroutcome-basedselection. OldTRAIN4/objective,originaloldTRAINprobe64/replayonlyandindependentoldDEV64/diagnosticgradientdistinct. Namedoptimizer mappingreconstructedfromverifiedoriginalproducer/liveparameterobjectsandvalidatedbyshapes,notblindlistpositions. All6nativefirstbatchesmustreplaypreviousunprojectedd4beforehybrids. ExistingGPUonly,planned10320sequenceforwards,cap12000.

## 6. Minimal Falsification Tests
Reportall36candidatesandpairedmoment/thetaeffectsin9seed×batchcontexts;donotcountbatchesasindependentmodels. All3seedsand3batchesresolvedsamesignrequiredforstablewithin-scopeeffect. OpposingmomenteffectsacrossthetasorlargeDiDsupportsinteraction;batchreversalweakensstability. NewCEreportsprotectagainstmistakingstoppedlearningforretention. No-oprepeatscalibrateprecision; naturalUU/FFfirstbatchmustagreewithpriorlocald4. Failedmapping/replayblocksdependentinterpretation, notfixedbytraining.

## 7. Current Evidence
Previoussix-stateF4versusd4independentoldcomparison:2improvements,4noops,0harms. Ordinaryd4fromForiginwaslessfavorablethanUorigininall3seeds;thetaandAdamwereconfounded. Current2x2resultNOTRUNatfreeze. OriginalR06endpointsandpriorlocalrecordsremainunchanged.

## 8. Claim Boundary And Next Decision
NoFprojection,fullcontinuation,hyperparametersearch,TEST,newresources,candidateendpointsororiginalfilechanges. Syntheticcross-statecombinationonlymeasurescurrentstatesensitivity;futureperformanceandlong-runrootcauseunknown. Deliveronepage,onefour-cellfigure,allseed/batchtables/replayandoneoptionalnextproposalonly,notautorun. Researcheracceptance/closureunknown.
