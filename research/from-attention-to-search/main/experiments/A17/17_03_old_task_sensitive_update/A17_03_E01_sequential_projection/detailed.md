# Detailed:A17_03 sequential sensitivity

[Summary](summary.md) · [Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_03_old_task_sensitive_update/17_03_old_task_sensitive_update_anchor.md) · [Protocol](protocol.md)

Eligibility:qualified exposed-development sequential comparisons;no blind confirmation. All cases NO_ORDINARY_FORGETTING;registered total verdict MIXED_OR_NON_SUPPORTING. Mechanism/closure Unknown.

## 0. Quick recap

Six ordinary cases improve both old/new CE;protected new gain exceeds ordinary in6/6but old accuracy worsens in5/6. Sensitivity estimate has heldout local coverage but is incomplete. No net CE forgetting to protect against.

## 1. Definitions

Old sensitivity:leading uncentered individual-CE parameter-gradient directions;unsigned response,not harmful conflict. Old D:post-B minus post-A CE;new G:post-A minus post-B CE. Pair margin:correct-minus-other-rule logit. Accuracy:full-vocabulary argmax correctness.

## 2. Anchor relation

Sibling A17_03 addresses sequential retention/acquisition,not another A17_01 core round. Earlier local/combined help does not imply sequential forgetting;this explicitly tests that bridge.

## 3. Freeze and conformance

| Item | Expected | Actual | Status |
| --- | --- | --- | --- |
| Parent / data | exact officialQwen,train/dev | identities matched,no test | PASS |
| Cases / trajectories | 3seeds×2orders,6old+18new | 6/24 | PASS |
| Scientific training | 48000answers,2400steps | independently recomputed | PASS |
| Smoke / externalresume | four workers each,exact1→2 | four PASS each | PASS |
| Stored input / output | all frozen SHA256 | 22 /426 checked | PASS |
| Actual sample order | same2000new records/strategy | exact frozen lists | PASS |
| Parameter scope | one o_proj,frozen others | identical frozen hashes | PASS |
| Norm / constraint | <=.002relative | norm<=3.73e-7,leak<=1.52e-6 | PASS |
| Saved states | old0/16/50/100;new0/1/16/50/100 | 114Full;44Smoke | PASS |
| Telemetry | seven tags,20answers/window |24Full/16Smoke verified | PASS |

Frozen English Protocol SHA256:546d729bafa36e721d21af4d813f817e27ff48b7cdcb569c18047f27c59b5a75. [Run-local contract](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/runs/sequential_20261010T171602Z/protocol.md) · [input freeze](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/runs/sequential_20261010T171602Z/freeze.json). No recovery,material amendment,rank/threshold tuning,missing condition or optimizer fallback. Posthoc transition counts and table aggregation use only already saved endpoints.

## 4. Actual setup

Official Base,only layer27o_proj [1024,2048]. FP32 complete native eval-mode gradients/inference,no tail or SAE. Manual SGD LR.01,clip1,no momentum/decay. Micro5×accum4,20validanswers/update. Fixed local rank16from60old training gradients,randomrank16,H100four independentcase workers. Old100,new100each,strategy norm schedule from ordinary. Exposed dev800,rule×panel200answers,all full-old groups observed;test untouched.

[Source](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/source/run.py) · [geometry](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/source/geometry.py) · [config](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/runs/sequential_20261010T171602Z/config.json) · [input lineage](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/provenance/input_lineage.json) · [environment/launch](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/runs/sequential_20261010T171602Z/execution_certificate.md). Reuse:inspected E03AnswerLM/collate/checkpoint trees/telemetry plus exact-parent carrier/runtime. Adapt:SGD and constrained geometry. Reject:SAE/S7/tail approximations and originalAdamW/probe loops.

## 5. Metrics and frozen branches

Old acquisition>=.01,new ordinarygain>=.01,ordinaryD>.01forforgetting;protectedgain>=90%ordinaryand>.01,oldDreduction>.01versusbothordinary/randomforconstructiveprotection. These delegated operational screens are not population significance. All six must support protection for registered consistency. Only3independentseeds,two within-seedorders;no p-value/CI.

Priority:oldacquisitioninsufficient,newacquisitioninsufficient,noordinaryforgetting,constructiveprotection,newlearningcost,nospecificprotection. All cases enter noordinaryforgetting before considering protection. Secondary gains cannot rescue the registered forgetting prerequisite.

## 6. Evidence lineage

| Claim | Source | Computation | Result / boundary |
| --- | --- | --- | --- |
| Complete engineering | [verification](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/audit/completion_verification.json) | counts/hashes/states/tags | complete,not scientific closure |
| Actual matching/exposure | [trajectory audit](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/audit/trajectory_contract_verification.json) | metrics IDs/20-answer windows/norms | same source order/old state |
| Old/new finite CE | [conditions](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/audit/conditions.csv) | same old reference,new endpoint |6noCEforgetting |
| Direction/seed/panel means | [derived](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/audit/derived_results.json) /[panels](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/audit/panels.csv) | seed equalweights,panel equalweights |no population inference |
| CE vs accuracy | [transitions](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/audit/old_accuracy_transitions.json) | fixed per-record correct flips/CE |old accuracy falls despite CE gains |
| Sensitive directions | full/<case>/subspaces.pt,sensitivity_qualification.json | fit/heldoutgradient energy,±finite RMS |partial local CE sensitivity |

## 7. Main results

| Order | New-learning strategy | Old ΔCE↓ | New CE gain↑ | Old Δaccuracy(pp) | New Δaccuracy(pp) |
| --- | --- | ---: | ---: | ---: | ---: |
| FIRST→LAST | ordinary | -0.078888 | 0.120197 | -1.083 | +5.417 |
| FIRST→LAST | protected | -0.087984 | 0.142648 | -1.167 | +4.167 |
| FIRST→LAST | random | -0.078887 | 0.120197 | -1.083 | +5.417 |
| LAST→FIRST | ordinary | -0.082602 | 0.135452 | +0.417 | +4.833 |
| LAST→FIRST | protected | -0.084757 | 0.156123 | -2.083 | +4.000 |
| LAST→FIRST | random | -0.082602 | 0.135452 | +0.417 | +4.833 |


| Seed/order | Old acquisition | Ordinary old D | Ordinary new G | Protected old D | Protected new G /ordinary | Frozen branch |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| 29 FIRST→LAST | 0.352756 | -0.080087 | 0.122501 | -0.097782 | 1.260040 | NO_ORDINARY_FORGETTING |
| 29 LAST→FIRST | 0.309410 | -0.080453 | 0.133805 | -0.080614 | 1.179325 | NO_ORDINARY_FORGETTING |
| 43 FIRST→LAST | 0.356378 | -0.079286 | 0.118272 | -0.080582 | 1.125715 | NO_ORDINARY_FORGETTING |
| 43 LAST→FIRST | 0.307560 | -0.084562 | 0.134664 | -0.089204 | 1.153423 | NO_ORDINARY_FORGETTING |
| 71 FIRST→LAST | 0.355724 | -0.077289 | 0.119818 | -0.085588 | 1.172165 | NO_ORDINARY_FORGETTING |
| 71 LAST→FIRST | 0.305796 | -0.082792 | 0.137887 | -0.084452 | 1.125879 | NO_ORDINARY_FORGETTING |

| Order | Strategy | Panel | Old D | New G |
| --- | --- | --- | ---: | ---: |
| FIRST→LAST | ordinary | order_new | -0.081403 | 0.120012 |
| FIRST→LAST | ordinary | combination_new | -0.076372 | 0.120382 |
| FIRST→LAST | protected | order_new | -0.088342 | 0.139370 |
| FIRST→LAST | protected | combination_new | -0.087627 | 0.145926 |
| FIRST→LAST | random | order_new | -0.081402 | 0.120012 |
| FIRST→LAST | random | combination_new | -0.076372 | 0.120381 |
| LAST→FIRST | ordinary | order_new | -0.082220 | 0.131583 |
| LAST→FIRST | ordinary | combination_new | -0.082985 | 0.139321 |
| LAST→FIRST | protected | order_new | -0.087017 | 0.152564 |
| LAST→FIRST | protected | combination_new | -0.082497 | 0.159682 |
| LAST→FIRST | random | order_new | -0.082220 | 0.131583 |
| LAST→FIRST | random | combination_new | -0.082984 | 0.139321 |

All reported means equal-weight3seeds,not six independent orders. Random CE endpoints differ from ordinary only≈1e-6;random removes an extremely small generic fraction of the2Mparameter space. This is a codimension control,not a matched-old-sensitivity-energy control.

## 8. Visual evidence

Tables suffice for distinct primary and accuracy questions;no generated scientific figure. Full curves/unsmoothed telemetry remain in trajectory TensorBoard/metrics.

## 9. Stage qualification and failure interpretation

Local4counterexample/controltests PASS;Smoke4workers,externalresume4workers,Full4workers PASS. No implementationfailure. Estimated directions capture80.9–83.6%fitgradientenergy,51.6–61.3%mean per-example heldoutgradientenergy on20olddevrecords;random6.27e-6–8.03e-6. First-vectorbidirectionalRMSratio176.9–528.4atnorm.01. This verifies a local signal,not all-oldinsensitivity or stablelaterbasis.

What was not supported:registered consistent forgetting-protection criterion,because ordinary netCEforgetting absent. What was not tested:globalnecessity,function partition,SAE,MoE/architectureutility,blindreplication,full endpoint externalcontinuation. Accuracy failures are observed predictions,not numeric failures.

## 10. Full round and execution record

Question:old-sensitive restriction in sequential opposite-rule learning. Setup:same officialBase and oldstate/three strategies,both orders,3seeds. Training:registeredpairedtrain4k,oneold/newruleepoch perstage. Evaluation:exposeddev800,nominal and actual qualifiedneworder/newgroup,testclosed. Result:6ordinaryoldCEimprovements,protectedhighernewCEgainall6butoldaccuracydeclines5/6. Insight:condition forgetting mechanism on actual metric deterioration;projectioncomplement remains only estimated. Researcher decides next mechanism/stop.

Job pt-ubjfxl7c one4H100reserved node submittedUTC2026-10-10T17:16:14 (Asia/Shanghai2026-10-11 01:16);STARTING pendingimage/runtime thenRUNNING;internalSmoke/externalresumePASS→Full. OriginaljobSUCCEEDED,no retry/resubmission. Supervised finite completion as requested;no automation.

## 11. Reasoning audit and interpretation

Unsigned sensitivity does not determine harmful update sign;these directions can carry useful old/new changes. NoCEforgetting blocks a CE anti-forgetting attribution,but does not erase partial accuracy deterioration. Protectedgains outsideQ refute necessity of this estimatedsubset in this finitepolicy,not necessity of every actualoldsensitivecoordinate. Sixpolicies with largerCEgain do not imply better overall task capability when argmax falls. Randommatching controlsstep/codimension,not arbitrarybasis choice/gradientenergy. FixedQsensitivitydrift and remaining48%heldoutgradientenergy remain live. No universal functionality inference from top directions.

## 12. Claim boundary

Allowed:specific sequential policy effects on savedold/newCE,accuracy,margins;estimatedQ has localoldCEsensitivity and itscomplement permits new learning. Not allowed:universalupdate necessity,all-oldinsensitive directions,common/unique modules,SAEclaims,naturaltextforgetting mechanism,shared/separatedexperts or computeefficiency. Exposeddev and3seeds;optimizer/model/rank/budget-specific. Mechanism/closureUnknown.

## 13. Next decision

Researcher decides whether this task pair closes the currentCE-forgetting entry or which measured property/rival warrants continuation. Completioncriterion:accepted bounded answer and targetproperty;resume with linkedcase/accuracy evidence. AI suggestion only,no new run authorized by this result.

## 14. Artifact manifest

| Artifact | Meaning | Identity/completion |
| --- | --- | --- |
| [Frozen Protocol](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/runs/sequential_20261010T171602Z/protocol.md) | pre-run body | 546d729bafa36e721d21af4d813f817e27ff48b7cdcb569c18047f27c59b5a75 |
| [Freeze](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/runs/sequential_20261010T171602Z/freeze.json) |code/data/parent/sourceattachments |22verifiedfiles |
| [Payload manifest](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/runs/sequential_20261010T171602Z/payload_manifest.json) |fullnativearrays/checkpoints/events |426verifiedfiles |
| [Results](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/runs/sequential_20261010T171602Z/results.json) |sixcases/frozenbranch |complete |
| [Byte/count audit](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/audit/completion_verification.json) |engineeringqualification |PASS |
| [Source/norm audit](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/audit/trajectory_contract_verification.json) |actualsequence/constraints |PASS |
| [Per-seed table](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/audit/conditions.csv) /[panel table](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/audit/panels.csv) |derivedexistingendpoints |complete |
| [Accuracy transitions](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/audit/old_accuracy_transitions.json) |oldcorrect flips |posthoc arithmetic |
| [Registration request](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/audit/registration_request.json) |40actualcheckpointfamilies+analysis |41assetIDs |
| [Registration receipt](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/audit/registration_request_registered_outputs.json) |actualIDs/318memberhashchecks |complete |
| [Current strict access](/data/250010109/Research_System/assets/checks/2026-10-10_a17_outputs_20261010T172742Z.json) |selected41newoutputs |PASS,notwholelibrary |
| [Execution certificate](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/runs/sequential_20261010T171602Z/execution_certificate.md) |resource/command/stategates |complete |
| [Platform terminal](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/runs/sequential_20261010T171602Z/acp_receipts/describe_terminal.json) |samejob |SUCCEEDED |

Checkpoint states are matrix adapters requiring exactBase,not standaloneLMs. Complete optimizer/RNG/counter/cursor/subspace/reference pointers saved;finalFullexternalresumeNOT_CHECKED. Smoke960answers do not enter scientific48000. Rawpayloads stay execution-side;noGit/publish.

## 15. Links

[Summary](summary.md) · [Protocol](protocol.md) · [Execution root](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update)
