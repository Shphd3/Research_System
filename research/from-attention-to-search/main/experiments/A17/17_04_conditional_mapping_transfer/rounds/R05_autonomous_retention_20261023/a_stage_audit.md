# A-stage supplement: audit and bounded configuration closure

**The implemented displacement attenuation is credible. The current top16, 0.1-to-0.01, 1200-update configuration does not meet the original utility criteria. AI recommends closing this configuration round; the broader research question and mechanism remain Unknown.** This supplement preserves the frozen Protocol and researcher-owned scientific state.

[Evidence package](/data/250010109/MoE_Router/experiments/20261023_autonomous_retention/exports/A_stage_audit_20261023.zip) · [中文](a_stage_audit_cn.md) · [All saved points](a_stage_curves.md)

Only existing A weights and data were used. Parameter supplements ran on CPU. One single-H100 reserved evaluation job, pt-tevljsgv, evaluated21 original step2 recovery snapshots and replayed one previously evaluated calibration state. No training was launched. The original25 input/family access checks and six supplemental dependencies passed current strict access. The three seeds are continuation orders of one acquired-old Qwen3-0.6B Base, not independent acquisition replicates. Only the final attention Q/K/V/O weights (6,291,456 scalars) were trainable.

## Coverage and missingness

| Request | Status | Delivered / boundary |
| --- | --- | --- |
| Projection, optimizer update, SVD object and name | ANSWERED_BY_EXISTING_EVIDENCE | Actual versions, formulas and source/freeze lineage. Functional preservation is not established; use “attenuation of top16 singular rank-one coefficient updates of full acquired weights.” Identifying preserved old computation requires new experiments. |
| Protected update fraction, filtering, cumulative C/R | ANSWERED + RECOMPUTED_FROM_SAVED_ARTIFACTS | 7200 scalar step records, 48 saved-state net displacements, three exact paired first-step update differences. Full historical candidate/filter vectors are missing. A newly instrumented reproduction would describe a new trajectory, not fill historical observations. |
| Saved-point accuracy/CE and first qualification | RECOMPUTED_FROM_SAVED_ARTIFACTS | 168 evaluations, 21 fixed endpoints and first saved passing point. Unsampled steps cannot be localized. No endpoint reselection. |
| Error destinations and paired examples | RECOMPUTED_FROM_SAVED_ARTIFACTS | 16,800 old-mode records and real mode pairs. Whether an internal old rule was erased remains untested. |

## Actual computation

Each full acquired matrix $W_0$, not its acquisition displacement from pretrained weights, undergoes an FP64 singular value decomposition (SVD). Each matrix selects 16 paired atoms $B_i=u_i v_i^T$, 64 coefficients over four matrices. With the Frobenius inner product,

$$P(X)=\sum_{i=1}^{16}\langle B_i,X\rangle_F B_i,\quad C_t=P(W_t),\quad R_t=W_t-C_t.$$

After gradient clipping and one ordinary AdamW moment step, let $d_t=\widetilde W_{t+1}-W_t$ denote its candidate displacement. TS applies

$$W_{t+1}=W_t+d_t+(a_t-1)P(d_t),\quad a_t=0.01+0.09(1+\cos(\pi t/1200))/2.$$

The pre-update index is $t=0,\ldots,1199$; the actual final multiplier is 0.01000015421248. C is never frozen. U applies $d_t$; UL applies $0.1d_t$; US applies $a_t d_t$; TC applies $d_t-0.9P(d_t)$; RS/LS use the same schedule with random/tail atoms. Moments advance once and are not attenuated. The code uses FP32 and measures addition roundoff.

Even zero selected coefficient displacement only implies $u_i^T\Delta Wv_i=0$. Preserving complete computation on input $v_i$ requires the stronger $\Delta Wv_i=0$. The algebraic counterexample $\Delta W=u_{17}v_1^T$ changes that output while all 16 selected coefficients remain fixed. This is a mathematical example, not a measured model intervention.

Actual v1 source: projector/SVD lines234–267; full acquired matrices passed at475–489; optimizer and filtering554–638; full-vocabulary evaluation380–411; endpoint sensitivity797–840. Source v2 changes only frozen guards for another parameterization; its A computation is identical. Both byte-identical actual versions and the patch are packaged.

Existing TS29 endpoint diagnostics restore C with old/new accuracy0%/100%, and restore R with100%/0%. Perturbation norms are0.0041886 and4.9643332; they are not comparable amplitudes. These interventions establish conditional endpoint sensitivity, not unique mediation of the training trajectory. All seven existing intervention readouts are retained. The specific endpoint selection was not fully verified as preregistered.

## Displacements: do not conflate the three definitions

The metric is the joint Frobenius norm over all four matrices. Per-update path length is $\sum\|P(\Delta W_t)\|_F$; sum squared steps is $\sum\|P(\Delta W_t)\|_F^2$; endpoint net displacement is $\|P(W_{1200}-W_0)\|_F$. Cancellation makes these noninterchangeable. The first two use actual step logs; the last uses saved weights. C denotes selected parameter coordinates, not an identified common function.

| seed | arm | Σ‖ΔC‖ | Σ‖ΔR‖ | Σ‖ΔC‖² | Σ‖ΔR‖² | C squared-step share % |
| --- | --- | --- | --- | --- | --- | --- |
| 29 | U | 0.305854 | 24.896179 | 0.000317779256 | 1.258338 | 0.025248 |
| 29 | TS | 0.028512 | 25.905965 | 3.06500203e-06 | 1.304566 | 0.000235 |
| 43 | U | 0.286580 | 21.915229 | 0.000304381223 | 1.153827 | 0.026373 |
| 43 | TS | 0.026180 | 23.835839 | 2.90397605e-06 | 1.174072 | 0.000247 |
| 71 | U | 0.489860 | 46.776925 | 0.000414441788 | 2.467811 | 0.016791 |
| 71 | TS | 0.036483 | 48.410055 | 3.51314723e-06 | 2.518774 | 0.000139 |


The final column is100 times the ratio of summed C squared steps to summed total squared steps, not a mean of per-step fractions. TS reduces C path length to roughly one tenth of U, while R path length is not similarly reduced. Step-level values and coarse saved-span values are separate tables. FP64 supplementary projections use saved FP32 frames; their maximum orthogonality error is about6.32e−8.

| seed | arm | ‖C1200−C0‖ | ‖R1200−R0‖ |
| --- | --- | --- | --- |
| 29 | U | 0.042986 | 4.860647 |
| 29 | TS | 0.004189 | 4.964333 |
| 43 | U | 0.040622 | 4.747234 |
| 43 | TS | 0.003880 | 4.749823 |
| 71 | U | 0.113266 | 6.398788 |
| 71 | TS | 0.008303 | 6.496903 |


The same-start first step has identical saved Adam moments and candidate norms across U/TS; U filtering roundoff is zero. The following is the exact difference between saved realized updates, not an endpoint reconstruction of later candidates:

| seed | U first-step C norm | TS first-step C norm | TS/U | paired actual update gap norm |
| --- | --- | --- | --- | --- |
| 29 | 0.003955429 | 0.000395543 | 0.100000030 | 0.003559886 |
| 43 | 0.003700958 | 0.000370094 | 0.099999432 | 0.003330865 |
| 71 | 0.004188755 | 0.000418876 | 0.100000205 | 0.003769879 |


Across the full trajectory, candidate minus actual sum squared displacement is0.000321658/0.000302464/0.000411284 for TS seeds29/43/71:0.024650%/0.025755%/0.016326% of candidate squared displacement. This scalar reduction is not the norm or squared norm of the removed vector. Exact per-step candidate projections/filter vectors were not saved. The CSV additionally labels an ideal-projector roundoff envelope; it is a secondary modeled bound, not a measured vector trajectory.

## Saved evaluations and the fixed primary endpoint

Accuracy uses an argmax over all151,936 vocabulary entries. Cross entropy (CE) is the negative natural log probability of one gold answer, in nats/answer. Every evaluation has800 old and800 new answers; command×panel cells each contain200. DEV was held out from training but already exposed to prior analysis; it is not independent TEST. Training used only20 new answers/update and24,000 exposures total. Batch training CE is not full-TRAIN accuracy or evaluation.

The first saved point at which all four new cells reach95% is:

| arm | seed29 | seed43 | seed71 |
| --- | --- | --- | --- |
| U | 120 | 240 | 1200 |
| UL | 600 | 1200 | NEVER |
| US | 1200 | 1200 | NEVER |
| TC | 120 | 240 | 1200 |
| TS | 120 | 240 | 1200 |
| RS | 120 | 240 | 600 |
| LS | 120 | 240 | 1200 |


RS71 passes at600 and fails at1200. Its600 state is not substituted for the primary endpoint. U and TS first pass at the same saved step for each seed; TS old accuracy at those points is2.875%,1.5%,0.5%. All168 original readouts are provided in the curve table. A further21 step2 engineering recovery snapshots existed without saved DEV evaluations. This audit evaluated every one using the same full-vocabulary forward; these are post-hoc readouts of original weights, not original saved evaluations. All21 fail new qualification, so first qualification remains unchanged. The combined189-row table labels provenance explicitly. The step1 U29 calibration reproduces all1600 predictions. Supplemental step2 results follow (same columns as the endpoint table):

| seed | arm | old correct /800 | new correct /800 | old CE | new CE | minimum new cell % | qualified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 29 | U | 797 | 43 | 0.021760 | 11.264378 | 0.000 | NO |
| 29 | UL | 800 | 0 | 0.000653 | 15.660234 | 0.000 | NO |
| 29 | US | 800 | 0 | 0.000653 | 15.660236 | 0.000 | NO |
| 29 | TC | 797 | 43 | 0.021730 | 11.268971 | 0.000 | NO |
| 29 | TS | 797 | 43 | 0.021730 | 11.268970 | 0.000 | NO |
| 29 | RS | 797 | 43 | 0.021759 | 11.264441 | 0.000 | NO |
| 29 | LS | 797 | 43 | 0.021756 | 11.264920 | 0.000 | NO |
| 43 | U | 796 | 73 | 0.024525 | 10.855613 | 0.000 | NO |
| 43 | UL | 800 | 0 | 0.000694 | 15.665346 | 0.000 | NO |
| 43 | US | 800 | 0 | 0.000694 | 15.665347 | 0.000 | NO |
| 43 | TC | 796 | 73 | 0.024428 | 10.862188 | 0.000 | NO |
| 43 | TS | 796 | 73 | 0.024428 | 10.862188 | 0.000 | NO |
| 43 | RS | 796 | 73 | 0.024526 | 10.855654 | 0.000 | NO |
| 43 | LS | 796 | 73 | 0.024522 | 10.855874 | 0.000 | NO |
| 71 | U | 791 | 73 | 0.044745 | 10.742849 | 0.000 | NO |
| 71 | UL | 800 | 0 | 0.000671 | 15.621916 | 0.000 | NO |
| 71 | US | 800 | 0 | 0.000671 | 15.621918 | 0.000 | NO |
| 71 | TC | 791 | 73 | 0.044511 | 10.749291 | 0.000 | NO |
| 71 | TS | 791 | 73 | 0.044511 | 10.749290 | 0.000 | NO |
| 71 | RS | 791 | 73 | 0.044746 | 10.742849 | 0.000 | NO |
| 71 | LS | 791 | 73 | 0.044760 | 10.742754 | 0.000 | NO |

 All21 initial evaluations are old100%,new0%.

The following complete1200-update table is the primary evidence. The last cell column is minimum new-cell accuracy; CE units are nats/answer.

| seed | arm | old correct /800 | new correct /800 | old CE | new CE | minimum new cell % | qualified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 29 | U | 0 | 800 | 15.079923 | 0.000192 | 100.000 | YES |
| 29 | UL | 1 | 794 | 8.936068 | 0.019457 | 98.000 | YES |
| 29 | US | 12 | 785 | 6.343915 | 0.063351 | 96.000 | YES |
| 29 | TC | 0 | 800 | 15.598887 | 0.000218 | 100.000 | YES |
| 29 | TS | 0 | 800 | 16.007463 | 0.000190 | 100.000 | YES |
| 29 | RS | 0 | 800 | 15.051037 | 0.000297 | 100.000 | YES |
| 29 | LS | 0 | 800 | 15.695918 | 0.000259 | 100.000 | YES |
| 43 | U | 0 | 800 | 15.916420 | 0.000382 | 100.000 | YES |
| 43 | UL | 0 | 793 | 8.926432 | 0.022893 | 98.000 | YES |
| 43 | US | 7 | 786 | 6.608769 | 0.055381 | 95.500 | YES |
| 43 | TC | 1 | 799 | 15.169899 | 0.001902 | 99.500 | YES |
| 43 | TS | 0 | 799 | 15.606381 | 0.001676 | 99.500 | YES |
| 43 | RS | 0 | 800 | 16.167131 | 0.000497 | 100.000 | YES |
| 43 | LS | 0 | 800 | 15.429326 | 0.001291 | 100.000 | YES |
| 71 | U | 7 | 789 | 14.580182 | 0.054221 | 95.500 | YES |
| 71 | UL | 7 | 782 | 7.981381 | 0.066913 | 94.000 | NO |
| 71 | US | 36 | 747 | 4.657434 | 0.187586 | 85.500 | NO |
| 71 | TC | 0 | 789 | 14.224364 | 0.049758 | 96.500 | YES |
| 71 | TS | 4 | 789 | 14.204625 | 0.038472 | 96.500 | YES |
| 71 | RS | 9 | 785 | 14.568898 | 0.049705 | 94.500 | NO |
| 71 | LS | 19 | 788 | 15.149106 | 0.064308 | 96.000 | YES |


Eighteen of21 trajectories qualify, including all three TS runs. UL71/US71/RS71 do not qualify and are not treated as competent controls for broad mechanism rejection. The original utility criteria require qualified TS, at most1 percentage point new-accuracy loss and at least5 points old gain. Five points correspond to40 of800 answers. TS minus control contrasts are:

| seed | control | old gain pp | 95% interval pp | new difference pp | control qualified |
| --- | --- | --- | --- | --- | --- |
| 29 | U | 0.000 | [0.000, 0.000] | 0.000 | YES |
| 29 | UL | -0.125 | [-0.375, 0.000] | 0.750 | YES |
| 29 | US | -1.500 | [-2.375, -0.750] | 1.875 | YES |
| 29 | RS | 0.000 | [0.000, 0.000] | 0.000 | YES |
| 29 | LS | 0.000 | [0.000, 0.000] | 0.000 | YES |
| 29 | TC | 0.000 | [0.000, 0.000] | 0.000 | YES |
| 43 | U | 0.000 | [0.000, 0.000] | -0.125 | YES |
| 43 | UL | 0.000 | [0.000, 0.000] | 0.750 | YES |
| 43 | US | -0.875 | [-1.625, -0.250] | 1.625 | YES |
| 43 | RS | 0.000 | [0.000, 0.000] | -0.125 | YES |
| 43 | LS | 0.000 | [0.000, 0.000] | -0.125 | YES |
| 43 | TC | -0.125 | [-0.375, 0.000] | 0.000 | YES |
| 71 | U | -0.375 | [-1.125, 0.375] | 0.000 | YES |
| 71 | UL | -0.375 | [-1.125, 0.375] | 0.875 | NO |
| 71 | US | -4.000 | [-5.500, -2.625] | 5.250 | NO |
| 71 | RS | -0.625 | [-1.500, 0.128] | 0.500 | NO |
| 71 | LS | -1.875 | [-3.125, -0.750] | 0.125 | YES |
| 71 | TC | 0.500 | [0.125, 1.000] | 0.000 | YES |


All three primary conjunctions fail. The qualified U comparisons already give0/0/−0.375pp old gain, without relying on unqualified controls. TS old CE is lower than U for43/71 and higher for29; CE cannot replace the registered accuracy criterion.

Each bootstrap uses2000 fixed-seed draws, paired across arms and stratified by panel. Each panel has200 unordered-list clusters, with both command records resampled together. Panels are equally weighted. All18 estimates and intervals independently reproduce the original aggregation. These are example intervals conditional on one old model and a continuation order, not population/model uncertainty. A[0,0] interval here is not universal equivalence. No best checkpoint, rank, seed or new criterion was selected.

## Error destinations and real paired examples

The mutually exclusive old-mode categories are correct, opposite-rule endpoint, wrong middle word, and outside list. The two middle columns are both within-list selection errors. The last column is the subset of opposite-endpoint errors with the paired new-mode answer also correct and identical; it must not be added again.

| seed | arm | correct | opposite endpoint | wrong middle | outside list | paired new correct/same |
| --- | --- | --- | --- | --- | --- | --- |
| 29 | U | 0 | 800 | 0 | 0 | 800 |
| 29 | UL | 1 | 796 | 3 | 0 | 794 |
| 29 | US | 12 | 780 | 8 | 0 | 776 |
| 29 | TC | 0 | 800 | 0 | 0 | 800 |
| 29 | TS | 0 | 800 | 0 | 0 | 800 |
| 29 | RS | 0 | 800 | 0 | 0 | 800 |
| 29 | LS | 0 | 800 | 0 | 0 | 800 |
| 43 | U | 0 | 800 | 0 | 0 | 800 |
| 43 | UL | 0 | 795 | 5 | 0 | 791 |
| 43 | US | 7 | 783 | 10 | 0 | 781 |
| 43 | TC | 1 | 799 | 0 | 0 | 799 |
| 43 | TS | 0 | 800 | 0 | 0 | 799 |
| 43 | RS | 0 | 800 | 0 | 0 | 800 |
| 43 | LS | 0 | 800 | 0 | 0 | 800 |
| 71 | U | 7 | 786 | 7 | 0 | 785 |
| 71 | UL | 7 | 780 | 13 | 0 | 776 |
| 71 | US | 36 | 739 | 25 | 0 | 730 |
| 71 | TC | 0 | 789 | 7 | 4 | 787 |
| 71 | TS | 4 | 790 | 5 | 1 | 787 |
| 71 | RS | 9 | 779 | 10 | 2 | 778 |
| 71 | LS | 19 | 768 | 3 | 10 | 768 |


The21 rows total16,800 repeated old-mode answers:103 correct,16,584 opposite endpoint,96 middle,17 outside list. This repeats one evaluation set and is not16,800 independent examples. All17 outside-list predictions are still inside the20-word pool; full-vocabulary accuracy is nevertheless unchanged.

Real TS pairs: seed29, command甲, list黄 红 鸟: mode1 gold黄 predicts鸟; mode2 gold鸟 predicts鸟. Seed71, command乙, 黑 黄 紫: both modes predict middle黄, while gold answers are紫/黑. Seed71, command乙, 龙 虎 银: both predict金 outside the list, gold银/龙. A contrary case is seed71, command乙, 龙 鱼 紫: both predict紫; old is correct but new gold龙 is missed. Exact prefixes, IDs, predictions and CE are in real_examples.json and the full paired CSV. “Overwrite” describes output behavior only; it does not prove irreversible erasure of an internal rule.

## Provenance and numerical qualification

A_U_29 source/config freeze:2026-10-22T16:24:42.578169Z; finish16:26:23.024619Z. V1 SHA256 ec28e43c3197c76da870895bbb027ff57912587db4c22f34257be3fd2137a8e5; config89b72bc43a63126a176d6dbd1f88a0a1e2cf105655797cb7b623bbf8c3b1d68c. All21 source/environment/config identities match available actual versions. Later per-task freezes occurred before their own starts, not all before the first A outcome. A29 uses v1; A43/71 use v2. V2 was registered16:28:53 after some A outcomes; the preserved diff changes only another parameterization's frozen guards, not A behavior.

The original Protocol copy has a matching input-manifest digest and an earlier filesystem modification time. Filesystem times are mutable, not external preregistration timestamps. Per-task code/config freezing is directly verifiable; full pre-first-outcome external sealing of the complete current analysis is not claimed. The current aggregation was revised after the initial freeze and is not represented as its original sealed version. Supplementary trajectory/error analysis is explicitly post hoc.

The CPU boundary receipt was recorded16:49:46 UTC, after some A outcomes; it is supplementary qualification, not evidence that every numerical check preceded launch. All48 checkpoints used here additionally passed current SHA256-to-manifest checks. Queue started timestamps refer to task claims/wrappers; both preserved scheduler sources write freezes before launching children.

Original numerical receipts include a=1 byte-exact Adam replay; a=0 selected-coordinate maximum6.16091e−8 and addition roundoff9.89676e−8; unaltered optimizer moment semantics; and actual A-TS external-process step1→2 continuation with exact weights/optimizer/order/RNG/counters. All21 install-noop/cache-shape/freeze/telemetry receipts are retained. Engineering qualification does not establish mechanism. Two pre-existing unrelated navigation issues remain, so no whole-repository navigation PASS is claimed. This supplement separately checks its own links, source math, tables, hashes and portable aggregation replay.

## Bounded decision

AI assessment: implementation credible; original utility hypothesis NOT_SUPPORTED for this configuration; close this specific A configuration round without further training. The remaining explanations include a selector that misses old computation, sufficient effects through R, nonzero C drift, and interactions among matrices and downstream computation. Small parameter movement is not proof of functional irrelevance; endpoint restoration is not unique trajectory mediation.

The proposed closure applies only to this parent/data/four matrices/top16/optimizer/schedule/1200-step endpoint. The broader value of selective protection remains open. Researcher-owned Focus/question state is not automatically closed or promoted, and no next run is authorized by this audit.

The first supplemental job pt-ps3wz0xw failed before loading the model because CUDA lacked an explicit index. The sole fix selected cuda:0; job pt-tevljsgv completed the same readout. Both were single-H100 reserved jobs, sequentially. Failed source, error log, fix receipt and both submissions are preserved.

A direct remaining rival is a change in how the mode condition controls first/last selection. The new task still requires both choices. Old-mode errors alone do not establish erasure of the selection computation; these records do not distinguish altered conditional use from changes in the old internal computation.
