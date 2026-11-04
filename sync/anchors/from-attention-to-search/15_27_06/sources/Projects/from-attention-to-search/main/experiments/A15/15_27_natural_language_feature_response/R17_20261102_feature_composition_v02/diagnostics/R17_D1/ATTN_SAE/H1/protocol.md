# Protocol R17_D1 ATTN_SAE H1: Common members plus new fine-information members

Status: APPROVED_FOR_FROZEN_FORWARD_AND_CPU_PROBES by current direct user request2026-11-03. Originalpositivehypothesis is retained byA15_27_06; priorR17results remainunchanged.

## Question and comparison

C<=8 andF<=8 selected on corrected old discovery; extraA=F\C. Three common-vs-nonmatrix score contrasts and two losses C-vs-union and matchedsamecount-random-vs-union;5primary tests. Reportactual0-to-positive separatelyfrompositive-amplitudechanges; C16/32 truncation sensitivity.

## Data and fitting

Use corrected old384rows with original24/12/12family splits fordiscovery/development/diagnosticoldheldout. New24families/12theorem groups provide288mainrows(192fine)and48one-factorrows; allnewresponse islockedtest, neverfit/select. Record answercuepresence andparaphrase separately. Each dictionary usesnativehook,decoder,activation,frequency andindependentIDs; no cross-dictionaryatom alignment.

Primary repaired readouts train onmixed olddiscovery and selectthe5-choiceL2regularization ondescription-only olddevelopment. The originalmixed/mixed rule is firstrun forlocalization;threeprescribed schemes arecompared oncontinuousunion16,binaryunion16,high16. The sameprimaryrule applies toallfourhypotheses, not onlydiagnosticprobes. Thisreadout-target refinement is fixedbeforefreshaccess anddoesnot change thehypothesis.

L2logistic,lbfgs,max_iter5000,class_weightbalanced,C=.01/.1/1/10/100;scalerfitonlydiscovery;developmentunweightedlogloss;lowerC tie. Familybootstrap2000,seed20261103,theorem-sensitivity;Bonferronisimultaneous95%intervals asabove;randomseeds11021..11040. Positiveinterval lower>0 supports limitedreadability;upper<=0 opposes positiveincrement;crossing0orfailedcoverageisinsufficient. Keep counts,Brier,margins,per-example predictions andallgridchoices.

## Execution and guards

FrozenLM/dictionary,FP32primary;noLM/CC/routertraining. Nativehookandownreconstructionledger,positivecontrols,savedcoefficientreplayand24oldBF16/FP32pairsprotectmeasurement. Atmost2existingapproved5090spot GPUs;CPUprobes. Everycorrection records oldproblem,affectedH,actualchange,recalculationanddataexposure;neveroverwriteR17.

[Complete adoptedinstruction](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/inputs/NEXT_ROUND_PROMPT.md) · [Parentprotocol](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/protocol.md) · [Frozenplan](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/frozen_diagnostic_plan.json) · [Correctionledger](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/correction_ledger.json). Scientificacceptance andnextdecision are researcher's;no publicationornewtrainingauthority.
