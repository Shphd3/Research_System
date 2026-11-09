# Detailed:A17 paired-rule answer margin

Primary Anchor:[A17_01_01](../../../../../../problem_anchors/17_shared_and_interference_learning/17_01_controlled_list_prediction_rules/subanchors/17_01_01_rule_conditioned_answer_margin_anchor.md). Frozen Protocol:[run snapshot](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/runs/analysis_20261010T141041Z/protocol.md). English Protocol SHA256:46eed833a9d92c0ea8424577ed0266757b0dc4ae9539bf5615bfb8da1dfe64b0. Summary:[English](summary.md).

Result eligibility:eligible within the registered exposed-development local-effect scope; not blind confirmation. Engineering PASS. Registered verdict:DESCRIPTIVE_HETEROGENEOUS_OR_INSUFFICIENT. Human mechanism/closure judgment:Unknown.

## 0. Quick Recap

18/18 source-effective and recipient-loss-helping;12/18 recipient margins improve and6 worsen;18/18 S improves. Frozen consistency criterion unmet; interpretation is AI-proposed, researcher judgment Unknown.

## 1. Terminology / Definitions

Pair margin:correct-minus-other-rule-answer logit; S:sum of both prompt margins; conditional20 CE:correct-answer CE renormalized over20 answer words; pool logmass:log of their total probability. Numerical resolution1e-6 for margins/loss; S2e-6. Negative CE delta is help; positive margin delta is preference improvement. Accuracy deltas in proportions, multiply100 for percentage points.

## 2. Anchor Link And Decision Point

Parent investigates useful/harmful shared learning; child checks whether observed loss help reaches relative answer selection, without redefining the question or adjudicating experts/SAE.

## 3. Protocol Freeze, Conformance, And Deviations

| Item | Expected | Actual | Status |
| --- | --- | --- | --- |
| Unique states / Full conditions | 7 /280 | 7 /280 | PASS |
| Smoke | four workers,8 conditions | four PASS,8 endpoints | PASS |
| Fixed dev pairs | 60, both rule prompts | 60/condition, complete | PASS |
| Source/recipient content groups | disjoint | overlap0 | PASS |
| No-op / frozen weights | exact repeat/restore, fixed non-target | drift0,all worker digests identical | PASS |
| Input/payload SHA256 | frozen bytes | 330/642 matched | PASS |
| Primary slice | u16,eta.01,m1,b2–4,3seeds,2directions | 18 cells | PASS |
| Test / training / SAE | no new access or training | none | PASS |

No amendments, retries, exclusions or missing conditions. Post-hoc arithmetic verification and panel/direction means summarize existing frozen readouts; no new hypothesis test or inference endpoints. This follow-up was itself motivated by exposed dev evidence, not prospectively blinded. Entrypoint checker returned1 for10 existing untracked paths (86 checked); no missing path reported. New document local links/math source checked; rendering NOT_CHECKED.

## 4. Actual Setup

Qwen3-0.6B Base official parent; only layer27 1024×2048 o_proj restored from saved direct checkpoints. Parent elsewhere frozen. One initial Base plus u16/u100 for seeds29/43/71. Complete deterministic FP32 native model, FP64 lognormalizer/differences, batch20. Forty actual matrices/state:FIRST/LAST×b0–4×eta{.001,.01}×multiplier{1,.5}. Saved update added to same W0, actual delta exact, each condition restored. Training/optimizer/resume NOT_APPLICABLE; zero training updates. No SAE branch.

[Code](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/source/run_margin.py) · [config](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/runs/analysis_20261010T141041Z/config.json) · [frozen inputs](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/runs/analysis_20261010T141041Z/freeze.json) · [input lineage](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/provenance/input_lineage.json) · [execution certificate](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/runs/analysis_20261010T141041Z/execution_certificate.md). No completed answer in input; use existing tokenizer/answer IDs. Nominal dev panels20 order-new/40 combination-new pairs; source groups disjoint. Both development partitions previously exposed; no test access.

## 5. Metrics And Registered Decision Rules

Pair margin and S defined above; also correct-minus-max(other two list words), list/full top1, full CE, conditional20 CE,pool logmass. Source own-rule heldout CE and cross-rule CE must each decrease beyond1e-6. Then margin delta>1e-6 improves;<−1e-6 worsens;otherwise unresolved. S resolution2e-6. Engineering thresholds do not define substantive importance. Primary support requires all18 qualified updates improve margins. All conditions/sensitivity preserved, not selected by sign. Three independent training seeds; three within-seed source batches are repeated measurements. Mean cells seed-equal and source-batch-equal; no population CI/p-value.

## 6. Evidence Lineage

| Claim | Source | Computation | Observation | Boundary |
| --- | --- | --- | --- | --- |
| Engineering complete | [verification](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/audit/completion_verification.json) | byte hashes/counts/receipts |7 states,280 endpoints,8 Smoke | platform success alone insufficient |
| Loss vs margin | [primary CSV](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/audit/primary_conditions.csv) | fixed primary slice,raw endpoint/pair files |18 CE helps;12 margins up,6 down | exposed dev,local update |
| Two prompt separation | [audit](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/audit/readout_audit.json) | sum two margins,same list |18/18 positive ΔS,mean.003115313 | may be source gain offsetting recipient decline |
| Separate/combined novelty | [panel CSV](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/audit/primary_panels.csv) | preserve nominal/actual panels |tables below | actual panel sizes differ by seed |
| CE decomposition | endpoint arrays |conditional20 CE−pool logmass |pool and within-pool changes | arithmetic identity,not causal mediation |

## 7. Main Results

| Source → recipient | ΔCE↓ | Δpair margin↑ | Improved/worsened | Δaccuracy (pp) |
| --- | ---: | ---: | ---: | ---: |
| FIRST → LAST | -0.002282 | 0.000545 | 4/9 · 5/9 | -0.370 |
| LAST → FIRST | -0.002436 | 0.000940 | 8/9 · 1/9 | +0.556 |


Seed×direction mean recipient Δmargin:29 FIRST→LAST+.000161542,LAST→FIRST+.001525413;43+.000421863/+.000874774;71+.001050864/+.000418801. All six means positive, but only two of six have every source batch improve. The primary verdict therefore remains heterogeneous/insufficient. S positive in18/18,range.002667014–.003472678. Conditional20 CE improves17/18, pool mass18/18. FIRST→LAST accuracy worsens2/9,unchanged7/9; reverse improves3/9,unchanged6/9.

| Direction | Nominal panel | Pairs/state | ΔCE | Δmargin | Δaccuracy(pp) |
| --- | --- | ---: | ---: | ---: | ---: |
| FIRST→LAST | nominal/combination_new | 40 | -0.002349 | -0.000043 | +0.000 |
| FIRST→LAST | nominal/order_new | 20 | -0.002149 | 0.001721 | -1.111 |
| LAST→FIRST | nominal/combination_new | 40 | -0.002938 | 0.001969 | -0.278 |
| LAST→FIRST | nominal/order_new | 20 | -0.001433 | -0.001119 | +2.222 |

| Direction | Actual exposure panel | Pairs/state | ΔCE | Δmargin | Δaccuracy(pp) |
| --- | --- | ---: | ---: | ---: | ---: |
| FIRST→LAST | actual/seen_group_unseen_order | 6,8,10 | -0.001220 | 0.001370 | +0.000 |
| FIRST→LAST | actual/unseen_group_in_this_training_round | 50,52,54 | -0.002387 | 0.000360 | -0.412 |
| LAST→FIRST | actual/seen_group_unseen_order | 6,8,10 | -0.001598 | -0.000752 | +0.000 |
| LAST→FIRST | actual/unseen_group_in_this_training_round | 50,52,54 | -0.002522 | 0.001138 | +0.634 |

Panel means equal-weight seeds then batches, not pooled observations from differently sized actual panels. Combined means use all60pairs per condition; nominal counts20/40, actual seen counts6/8/10 and unseen54/52/50. Source/recipient independent content groups remain preserved. Sparse actual seen panel limits generalization comparisons.

## 8. Visualization Results

Tables above carry the decisive signs/counts; no scientific figure generated. Raw per-pair evidence is linked by payload manifest.

## 9. Stage Evidence And Failure Decomposition

Local seven tests PASS; Smoke8 conditions PASS; Full280 PASS; 330input/642output hashes PASS; arithmetic280 endpoints/7baselines PASS,max difference1.4210854715202004e-14. No runtime recovery. Frozen scientific consistency criterion NOT_MET due6 negative recipient margins; not an implementation failure and not absence of shared functionality. Numerical resolution is not statistical uncertainty.

## 10. Full Experiment Record

2026-10-10 round:paired relative-choice question/hypothesis;seven saved native Qwen states versus exact no-update baselines;no new training data,source batches fixed selection-v2;fixed60paired dev lists,no test/confirmation opening;observed18 CE helps,12/6margin signs;AI-proposed boundary:local prediction help does not consistently imply relative-choice transfer. Job pt-hz9kc697 four H100 reserved,SUCCEEDED. Earlier bounded polling stopped after first progress; user requested results afterward, so this turn inspected the same completed job without resubmission.

<details><summary>Historical startup notes (preserved; not current status)</summary>

# A17 E03 paired-rule margin: execution record

## Question and hypothesis

Does a useful cross-rule update improve correct-versus-other-rule answer preference as well as loss? Compare the accepted margin hypothesis with candidate-pool adaptation and common positional-bias rivals. Scientific interpretation remains Unknown.

## Setup and controls

Seven saved Qwen direct-o_proj states;280 independent actual matrices;120 fixed dev rows/60 pairs; no new training/SAE/test access. Four H100 reserved, four independent processes, internal Smoke→Full. [Protocol](protocol.md) and [execution certificate](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/runs/analysis_20261010T141041Z/execution_certificate.md) own setup and environment.

## Data and provenance

Input checks PASS: exact checkpoint manifests,280 matrix shapes/dtypes/finite values and SHA256, source/recipient group independence, complete pairs,20 answer-ID mapping, actual-exposure ledger matches. [Freeze](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/runs/analysis_20261010T141041Z/freeze.json); [input lineage](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/provenance/input_lineage.json). Existing exposed dev, not blind confirmation. Seven local implementation tests PASS; math source and local links checked (no rendered verification).

## Execution state and deviations

Job pt-hz9kc697 submitted 2026-10-10T14:11:19Z through canonical ACP template. Platform:QUEUEING at 2026-10-10T14:12:45.060800+00:00. Smoke:NOT_RUN/NOT_VERIFIED. Full:NOT_RUN/NOT_VERIFIED. Scientific endpoint:NOT_RUN. No scientific-input deviation. No full completion inferred from submission.

[Submission receipt](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/runs/analysis_20261010T141041Z/acp_receipts/submit-a17-margin-analysis-20261010t141041z-20261010T141117Z.json); [startup describe](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/runs/analysis_20261010T141041Z/acp_receipts/describe_startup.json). Code adapts inspected Qwen loader/restore/collate and mounted runtime; unused S7/SAE/tail functions excluded. Runtime adds deterministic CUBLAS configuration.

## Results

NOT_RUN. No observed margin/CE conclusion yet. Expected:seven state summaries,280 condition endpoints and paired files, separate/combined novelty aggregates, four Smoke/Full receipts, results.json, manifest and completion.json. Actual outputs will be registered only after verification.

## Insight, boundary and next decision

Execution is authorized; mechanism/closure remain researcher-owned. After qualified completion, inspect both directional margins and S with CE/top1/pool mass. Mixed or unresolved cases remain visible. Current monitoring covers bounded startup/first progress only; do not resubmit a queued/live job.

## Last bounded observation:2026-10-10T14:13:43Z

Four H100 runtime identities verified. Four Smoke workers/gate PASS;8 Smoke updates complete. Full started automatically;50/280 conditions completed in the snapshot, with no immediate check failure. Remaining compute ETA1–3 minutes from first throughput, excluding final audit/registration. Stop polling; no automation. Full engineering completion and scientific verdict are unverified. [Startup evidence](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/runs/analysis_20261010T141041Z/startup_verification.json). Entrypoint checker returned1 for10 existing untracked entries, without absent paths; new local links/math-source checks PASS.


</details>

## 11. Interpretation And Reasoning Audit

The following is AI-proposed interpretation, not a researcher-confirmed mechanism. CE decrease raises correct-word probability but does not specify its ratio against a particular wrong word. Six direct counterexamples exclude a universal CE-help→pair-margin-help inference. Positive S18/18 excludes pure uniform answer-pool lifting and identical additive positional bias as sole explanations under the observed logit readout; it does not prove a learned internal rule algorithm. S can increase because source-rule improvement outweighs recipient decline. Conditional20 CE accounts for all20words; it need not track one competitor. Batch/state/direction sensitivity remains live. Mean improvement is not stable individual transfer or architecture utility.

Sensitivity slice u0,b2–4,eta.01,m1:6/6 qualified margin improvements. u100:7 improved,5 worsened,4 recipient-help-not-resolved,2 source-ineffective out of18. These do not rescue the registered u16 criterion. Each state is conditional on its training history; no broad state-dependence mechanism identified.

## 12. Claim Boundary

Can claim:actual saved interventions cause local endpoint prediction changes at the specified frozen states and independent lists;loss help and pair-margin signs differ;conditional separation increases in this primary set. Cannot claim:stable general rule transfer,natural-text pretraining gain,functional module partition,SAE feature mechanism,expert necessity or architectural superiority. Three seeds and exposed dev;small numerical changes;no blind replication. Mechanism judgment and closure Unknown.

## 13. Next Decision

Researcher adjudication of the bounded interpretation in Summary. Completion criterion:researcher states accepted answer and its boundary. Resume action:review18 source updates,especially6 CE-help/margin-decline cases. No next experiment submitted or authorized by this report.

## 14. Artifact Manifest

| Artifact | Purpose | Identity | Complete / eligibility |
| --- | --- | --- | --- |
| [frozen Protocol](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/runs/analysis_20261010T141041Z/protocol.md) | pre-run execution contract |SHA256 46eed833a9d92c0ea8424577ed0266757b0dc4ae9539bf5615bfb8da1dfe64b0| complete,registered scope |
| [freeze](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/runs/analysis_20261010T141041Z/freeze.json) |source/config/checkpoint/update/data identity|330 verified entries| complete |
| [payload manifest](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/runs/analysis_20261010T141041Z/payload_manifest.json) |endpoint/raw-pair/summary identities|642 verified entries| complete,local dev |
| [results](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/runs/analysis_20261010T141041Z/results.json) |frozen verdict/all280 summaries|producer run_margin.py| complete |
| [readout audit](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/audit/readout_audit.json) |independent arithmetic and direction/panel summaries|recompute_readouts.py| complete,derived |
| [completion verification](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/audit/completion_verification.json) |platform+bytes+counts|verify_and_prepare_registration.py| complete,engineering |
| [registration](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/audit/registration_request_registered_outputs.json) |actual reusable output ID|representation_a17_paired_rule_margin_20261010t141041z| complete |
| [strict access](/data/250010109/Research_System/assets/checks/2026-10-10_a17_outputs_20261010T144031Z.json) |current output access|selected asset only| PASS,not whole library |
| [job status](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/runs/analysis_20261010T141041Z/acp_receipts/describe_results.json) |same job inspected on result request|pt-hz9kc697 SUCCEEDED| complete |

No new model/SAE checkpoint;resume NOT_APPLICABLE. Original training/selection parent IDs remain in registration_request.json and run freeze. New audits stay execution-side and are not retroactively added to the original payload manifest.

## 15. Links

[Summary](summary.md) · [Protocol](protocol.md) · [Execution root](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin)
