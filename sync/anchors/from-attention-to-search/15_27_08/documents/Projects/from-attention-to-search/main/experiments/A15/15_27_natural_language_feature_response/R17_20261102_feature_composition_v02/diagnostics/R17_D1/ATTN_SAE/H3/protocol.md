派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/ATTN_SAE/H3/protocol.md`。
[精确原始文件](../../../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/ATTN_SAE/H3/protocol.md)；研究修改仍回到原件。

---

# Protocol R17_D1 ATTN_SAE H3: Equal-budget cross-frequency complementarity

Status: APPROVED_FOR_FROZEN_FORWARD_AND_CPU_PROBES by current direct user request2026-11-03. Originalpositivehypothesis is retained byA15_27_08; priorR17results remainunchanged.

## Question and comparison

Own naturaldiscovery positive/coverage counts,min20positions and5documents,integerthirdboundaries keepingties. LargestfeasibleK16/12/8. J=halfhigh/quartermiddle/quarterlow,H=Khigh,M=halfmiddle/halflow. BothH-J andM-J loglossadvantages required;2primarycomparisons.

## Data and fitting

Use corrected old384rows with original24/12/12family splits fordiscovery/development/diagnosticoldheldout. New24families/12theorem groups provide288mainrows(192fine)and48one-factorrows; allnewresponse islockedtest, neverfit/select. Record answercuepresence andparaphrase separately. Each dictionary usesnativehook,decoder,activation,frequency andindependentIDs; no cross-dictionaryatom alignment.

Primary repaired readouts train onmixed olddiscovery and selectthe5-choiceL2regularization ondescription-only olddevelopment. The originalmixed/mixed rule is firstrun forlocalization;threeprescribed schemes arecompared oncontinuousunion16,binaryunion16,high16. The sameprimaryrule applies toallfourhypotheses, not onlydiagnosticprobes. Thisreadout-target refinement is fixedbeforefreshaccess anddoesnot change thehypothesis.

L2logistic,lbfgs,max_iter5000,class_weightbalanced,C=.01/.1/1/10/100;scalerfitonlydiscovery;developmentunweightedlogloss;lowerC tie. Familybootstrap2000,seed20261103,theorem-sensitivity;Bonferronisimultaneous95%intervals asabove;randomseeds11021..11040. Positiveinterval lower>0 supports limitedreadability;upper<=0 opposes positiveincrement;crossing0orfailedcoverageisinsufficient. Keep counts,Brier,margins,per-example predictions andallgridchoices.

## Execution and guards

FrozenLM/dictionary,FP32primary;noLM/CC/routertraining. Nativehookandownreconstructionledger,positivecontrols,savedcoefficientreplayand24oldBF16/FP32pairsprotectmeasurement. Atmost2existingapproved5090spot GPUs;CPUprobes. Everycorrection records oldproblem,affectedH,actualchange,recalculationanddataexposure;neveroverwriteR17.

[Complete adoptedinstruction](../../../../../../../../../../../../UNAVAILABLE.md) · [Parentprotocol](../../protocol.md) · [Frozenplan](../../../../../../../../../../../../UNAVAILABLE.md) · [Correctionledger](../../../../../../../../../../../../UNAVAILABLE.md). Scientificacceptance andnextdecision are researcher's;no publicationornewtrainingauthority.
