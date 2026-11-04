派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R06_functional_protection_20261025/local_dynamics_20261026/summary.md`。
[精确原始文件](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R06_functional_protection_20261025/local_dynamics_20261026/summary.md)；研究修改仍回到原件。

---

# Local F effects versus origin-state history

Purpose: explain the R06 zero-replay versus1:9endpoint pattern by separating localcounterfactuals from differenttraining histories. Sixpreselected U1:9/F1:9step120states retain completeAdam120/RNG and identicalnext36new/4old/64probe batches. IndependentoldDEV64was fixedhash16perpanel×command before outcomes. Original72slotdenominator,clip1,AdamWlr1e-4andFP32writeback reproduced;2independentAdamproposals/state and deterministicF0/F4/D4transformations, everybranchrestored. No continuation, no candidate checkpoints, noTEST/resourceallocation.11424/12000sequenceforwards.

**Finding: no state shows F4 harming independentoldloss relative to d4.** Uorigin all3andForigin43do not triggerF4, hence exactd4=F4=D4. Forigin29/71triggerF4 and improve botholdprobeandindependentoldloss relative to d4 while reducing the newlossimprovement. D4staysclosetod4, so those2activecaseshave direction-specificlocaleffect beyondshrinkage, notcapacityrelease.

| seed | origin | candidate | probe_delta_CE | independent_old_delta_CE | new_delta_CE |
| --- | --- | --- | --- | --- | --- |
| 29 | U | d0 | 0.017923 | -0.002595 | -0.002327 |
| 29 | U | d4 | -0.001796 | -0.043870 | 0.000642 |
| 29 | U | F0 | 0.004962 | -0.009974 | -0.001953 |
| 29 | U | F4 | -0.001796 | -0.043870 | 0.000642 |
| 29 | U | D4 | -0.001796 | -0.043870 | 0.000642 |
| 29 | F | d0 | 0.211213 | 0.191661 | -0.034133 |
| 29 | F | d4 | 0.122321 | 0.107916 | -0.026512 |
| 29 | F | F0 | -0.002597 | -0.038293 | -0.018855 |
| 29 | F | F4 | -0.000185 | -0.026341 | -0.017067 |
| 29 | F | D4 | 0.121748 | 0.107423 | -0.026412 |
| 43 | U | d0 | -0.022897 | -0.037087 | -0.016297 |
| 43 | U | d4 | -0.052460 | -0.072463 | -0.013595 |
| 43 | U | F0 | -0.022897 | -0.037087 | -0.016297 |
| 43 | U | F4 | -0.052460 | -0.072463 | -0.013595 |
| 43 | U | D4 | -0.052460 | -0.072463 | -0.013595 |
| 43 | F | d0 | 0.001570 | 0.076109 | -0.054928 |
| 43 | F | d4 | -0.123835 | -0.036755 | -0.043197 |
| 43 | F | F0 | 0.001570 | 0.076109 | -0.054928 |
| 43 | F | F4 | -0.123835 | -0.036755 | -0.043197 |
| 43 | F | D4 | -0.123835 | -0.036755 | -0.043197 |
| 71 | U | d0 | 0.005416 | -0.004354 | -0.036200 |
| 71 | U | d4 | 0.000754 | -0.004588 | -0.032361 |
| 71 | U | F0 | 0.004416 | -0.005292 | -0.036186 |
| 71 | U | F4 | 0.000754 | -0.004588 | -0.032361 |
| 71 | U | D4 | 0.000754 | -0.004588 | -0.032361 |
| 71 | F | d0 | 0.045314 | 0.101410 | -0.038020 |
| 71 | F | d4 | 0.036342 | 0.085813 | -0.032060 |
| 71 | F | F0 | 0.001080 | 0.047558 | -0.036952 |
| 71 | F | F4 | -0.000214 | 0.041265 | -0.030732 |
| 71 | F | D4 | 0.036249 | 0.085579 | -0.031987 |

Ordinaryd4 independentoldΔCEfromUorigins=-.043870,-.072463,-.004588;fromForigins=+.107916,-.036755,+.085813. EachForiginislessfavorable than correspondingUorigin, raisingjointstate/historypriority, withoutseparatingparametersfromAdammoments. F4Forigin71keepsprobeCEslightlylowerbutindependentoldCErises+.041265, stillbetterthand4+.085813; scopegapexistslocallybutbranchA(strictF4worsethand4)notmet.

Finiteabsolute remaindersshrinkwith1,.5,.25inall12state×candidatecases. Uorigin71hasnegativefirstorder−.003927butpositiveactualprobechange+.000754;halfstepturnsnegative. F4=d4there, so thisdoesnotshowprojection-specificharm. BranchB(worseF4thand4probe)notobserved. Allg4/g64cosinespositive(.165–.772);no rawopposite-gradientpattern. Removedg4dotspositive in2activeF4cases, so no evidencehereforremovinganold-beneficialcomponent. Newlearningcostremains.

Two no-op evaluations giveexactper-itemagreement atall18state×groups;maximumprecisionτ4.7731e−8nat/answer;comparisonuses2τ, notstatisticalCI.6checkpointbefore/afterSHAidentical, modelnon-targetbytesunchanged. Oldtrajectorylosses/accuracy/confusionandprojectionlogsareassociational; fulltrajectoryendpointlogitmarginsNOT_SAVED. Fixed6stateones-stepcannotexplain240stependpointsorsweepstate/batchpopulations.

Only proposedfollowup(notrun): pairedAdam-momentexchange atfixedoriginaltheta andsamebatch, comparingnative/cross-originmoments with d4/F4 andindependentoldloss. Effectfollowingmomentsraisesmoment-historycontribution; effectfollowingtheta raisesparameterhistory; artificialhybridstatesstilllocal.

[Chineseone-page/fullrecord](summary_cn.md),[completeappendix](appendix_cn.md),[figures](figures_cn.md),[plan](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R06_functional_protection_20261025/local_dynamics_20261026/reproduce/plan.json).

Same-stateoldtargetinteraction:4/6states show a smaller marginal F benefit with4oldobjectives,2/6no-ops; none changesintoharmrelativeordinary. d4improvesindependentoldloss comparedwithd0inall6states. These branches areallfrom1:9historicalstates; theydoNOTreplayactual0:1originstates.

Noise-schema clarification: same_prediction_all in the original diagnostic CSV compares per-item correctness flags, not saved rawargmaxIDs. No-op evidence is exact per-itemCEandcorrectness agreement; rawpredictionIDequality was not independently logged.
