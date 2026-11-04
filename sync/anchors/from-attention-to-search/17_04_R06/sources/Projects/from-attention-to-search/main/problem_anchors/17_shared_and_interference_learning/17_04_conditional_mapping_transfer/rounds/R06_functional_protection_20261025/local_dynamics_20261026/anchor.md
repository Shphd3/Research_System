# A17_04 R06 supplement: Local update effects versus trajectory history

## 1. Problem Definition
Explain why F has limited relative retention at zero old replay but underperforms U at1:9, distinguishing same-state update effects from different-history endpoint comparisons. Same17_04/R06 scientific owner; no new independent question, architecture or training method search. Current user explicitly authorizes this bounded frozen diagnostic and routine internal checks without further review.

## 2. Physical Priors
Local probe gradients need not describe finite-step or independent old behavior. Four old objective labels alter joint optimization, but trajectories accumulate different parameters and Adam moments. Endpoint interactions are not same-state causal interactions.

## 3. Falsifiable Hypotheses
A: probe protection differs from independent old function. B: finite-step prediction error contributes. C: origin-state/optimizer history dominates current F-versus-ordinary contrast. D: magnitude alone explains the local effect. E: projection removes a locally beneficial component of the joint update. F: inconsistent or noise-scale observations leave evidence insufficient. These may coexist; use the user's A–F branches without forcing one winner.

## 4. Mathematical Model
At eachsavedstate(theta,Adam120), actualproposal d_k=AdamStep(sum36newCE+sum_koldCE over72)-theta, k=0or4, afterglobalclip1. Restoreallweights,optimizer,RNGfor eachproposal. Let g be64oldTRAINmeanlossgradient and g4themean4activeoldgradient. F(d)=d-g*(g·d)/||g||² ifg·d>0and||g||²>1e-24, else d. D4=d4*||F(d4)||/||d4||, zerod4=>zero. Actual displacement includesFP32writeback. Read finiteCEchange on sameprobe,new36andindependentoldDEV64. Pair localdifferences atsameθ; never add separateAdamsolutions. Scalingalpha1,.5,.25is frozen displacementdiagnosis, not tunedlearningrate.

## 5. Computational Realization
Sixfixedstates U1:9/F1:9 step120 acrossorders29,43,71; fullAdam required. Same nextbatch index120and same64probe perseed. IndependentoldDEV64is fixedhashbalanced16perpanel×command before anynewresults. Allobjectives/projections useTRAINonly. Reuseoriginalnativefinalblock,loss,clip,optimizer andgradient/FP32filters. OnlycurrentexistingGPU; noallocation orjob. Zero/no-op repeatscalibrateprecision. Atmost12000sequenceforwards; planned11424. Scalingreadoutsomitnew36tofitbudget; allsix maincomparisons retained.

## 6. Minimal Falsification Tests
Compare d0,d4,F0,F4,D4fromeachsameθ/moments; oldprobe,newbatch,independentoldCE and actualgradientdots. Compare d4/F4scaleswithoutlearning. Improvementofprobepredictionwithindependentoldharm supportsA locally. Worsefiniteprobeeffectreducedbyshrinking supportsB locally. Fnotworseinstate butordinaryeffects varybyoriginraisesC; noθversusmomentidentification. D4/F4closewithinnoiseweakensdirectionclaim. Erequiresrealfunctionalharmfromremoval, notgradientanglealone. Mixed/noise=>insufficient andstop.

## 7. Current Evidence
Prior240stepmatrix: U/Foldaccuracy0.125/11.292%at0:1,93.125/68.250%at1:9. Fixednewexposure; Fendpointsloseat1:9inallorders.90fixedchecksinclude69rawfiniteprobeincreaseswithoutbeyond-tolerancefinaldotviolation. Errorsmainlynewrule; U1:9oldbehaviorfallsandrecovers. Thosearetrajectoryfacts, notsame-stateeffect. CurrentlocaldiagnosticNOTRUNatfreeze.

## 8. Claim Boundary And Next Decision
Nofullcontinuation,hyperparametertuning,TEST,SAE,CrossCoder,MoE,newresourceorcheckpointmutation. Single-stepfindingdoesnotidentifylong-runrootcauseoroldknowledgeposition. Reportobservations,rivals,boundariesandonefollowupexperimentproposalonly; researcheracceptance/nextapprovalremainUnknown. IfassetsorGPUunavailabledeliverlogsandmarkdependentdiagnosticsblocked, nofallbackorretraining.
