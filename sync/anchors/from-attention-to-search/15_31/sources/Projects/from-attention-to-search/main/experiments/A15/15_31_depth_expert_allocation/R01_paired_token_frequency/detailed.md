# Detailed: R01 depth allocation and token frequency

**Status: both full budgets and required evaluations are complete, with final paired analysis produced; independent final audits PASS and formal asset registration/strict access PASS.** B has higher final low-frequency and overall NLL. Scientific acceptance, mechanism attribution and the researcher's next judgment remain Unknown.

[Summary](summary.md) · [中文](detailed_cn.md) · [Protocol](protocol.md) · [Freeze](joint_freeze.md) · [Execution history](execution_record.md) · [Audit](audit_review.md)

## Experiment and computation

Both causal decoders predict the next token from the visible prefix; all model parameters train. No teacher, SAE loss or pretrained checkpoint is used. A versus B changes only expert counts over depth, holding residual/expert width, attention, top-2 and tied vocabulary interfaces. The endpoint primary estimand is low-seen-token NLL(B)−NLL(A), in nat/token; negative favors B. High-frequency and overall costs remain alongside it. Frequency comes from actual target exposures, not semantic labels.

A concrete inspected case is token62204, `esktop`, appearing22 times in this training exposure and classified low under≤49. Its visible recent prefix includes `dbus-monitor` and `org.freed`. This is a subword-fragment frequency, not an entity/fact label. The[case record](/data/250010109/MoE_Router/experiments/20261106_depth_expert_allocation/audit/frequency_sample_spotcheck.json) was explicitly read by Codex after formalA began; timing is retained below.

## Full parameter and compute ledger

Bias-free SwiGLU has gate/up/down matrices:3×1024×1536=4,718,592 parameters/expert. Attention has16 query/8KV heads of dimension128; projections output2048Q/1024K/1024V. Matrix parameters6,291,456 plus QKnorm256 give6,291,712; two block norms add2,048. No shared experts, and every E>top-2.

| Arm | Layer | Hidden | FFN | E | top-k | Attention | Per expert | Experts total | Router | Other norms | Layer total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 1 | 1024 | 1536 | 8 | 2 | 6291712 | 4718592 | 37748736 | 8192 | 2048 | 44050688 |
| A | 2 | 1024 | 1536 | 8 | 2 | 6291712 | 4718592 | 37748736 | 8192 | 2048 | 44050688 |
| A | 3 | 1024 | 1536 | 8 | 2 | 6291712 | 4718592 | 37748736 | 8192 | 2048 | 44050688 |
| A | 4 | 1024 | 1536 | 8 | 2 | 6291712 | 4718592 | 37748736 | 8192 | 2048 | 44050688 |
| A | 5 | 1024 | 1536 | 8 | 2 | 6291712 | 4718592 | 37748736 | 8192 | 2048 | 44050688 |
| A | 6 | 1024 | 1536 | 8 | 2 | 6291712 | 4718592 | 37748736 | 8192 | 2048 | 44050688 |
| A | 7 | 1024 | 1536 | 8 | 2 | 6291712 | 4718592 | 37748736 | 8192 | 2048 | 44050688 |
| A | 8 | 1024 | 1536 | 8 | 2 | 6291712 | 4718592 | 37748736 | 8192 | 2048 | 44050688 |
| B | 1 | 1024 | 1536 | 6 | 2 | 6291712 | 4718592 | 28311552 | 6144 | 2048 | 34611456 |
| B | 2 | 1024 | 1536 | 6 | 2 | 6291712 | 4718592 | 28311552 | 6144 | 2048 | 34611456 |
| B | 3 | 1024 | 1536 | 6 | 2 | 6291712 | 4718592 | 28311552 | 6144 | 2048 | 34611456 |
| B | 4 | 1024 | 1536 | 8 | 2 | 6291712 | 4718592 | 37748736 | 8192 | 2048 | 44050688 |
| B | 5 | 1024 | 1536 | 8 | 2 | 6291712 | 4718592 | 37748736 | 8192 | 2048 | 44050688 |
| B | 6 | 1024 | 1536 | 10 | 2 | 6291712 | 4718592 | 47185920 | 10240 | 2048 | 53489920 |
| B | 7 | 1024 | 1536 | 10 | 2 | 6291712 | 4718592 | 47185920 | 10240 | 2048 | 53489920 |
| B | 8 | 1024 | 1536 | 10 | 2 | 6291712 | 4718592 | 47185920 | 10240 | 2048 | 53489920 |

The tied151,936×1024 embedding/output matrix contributes155,582,464 once; extra output head0; final norm1,024. Each arm totals507,988,992 unique/trainable parameters, including301,989,888 experts,65,536 routers and205,933,568 shared parameters. Difference0(0%). Conventional active parameters281,496,576 include all shared unique weights, all router weights and top-2 whole experts/layer, counting the tied vocabulary matrix once. This is an accounting convention; input lookup does not read the whole embedding matrix.[Actual ledger](/data/250010109/MoE_Router/experiments/20261106_depth_expert_allocation/audit/parameter_ledger.json)

Expert matrix work is150,994,944 forward FLOPs/token or452,984,832 forward/backward. Profiler-counted executed `aten::mm` shapes give 2,000,027,648 FLOPs/token, equal to6×(281,496,576−19,456norm)+2×155,582,464 for checkpointed-CE output recomputation. Fused SDPA QK/AV/backward, non-matrix kernels and communication remain excluded. This is not total measured training FLOPs.[Check](supporting_sources/matrix_flops_formula_check.json)

Formal throughput, memory, dispatch/communication and elapsed-time results appear below. Profiling's first step is excluded from throughput-budget medians; outside registration-I/O timing effects remain unmeasured.

## Data, buckets and exact training policy

The source is the first67,108,864 IDs of one verified DCLM pair-view file, not the full corpus. `<|im_end|>`151645 recovers document boundaries;8,827 fragment/short tokens are discarded and16 exact token-byte duplicate documents removed globally. Near duplicates are NOT_CHECKED. SHA-256 first64bits modulo100 assigns dev0/test1/train2..99. Train has53,813documents/65,766,910tokens; dev528/630,980 and test544/700,308. Full-split evaluation predicts630,979dev and700,307test targets. The complete split supplies general NLL/perplexity; the old115M holdout is NOT EVALUATED.[Manifest](supporting_sources/data_manifest.json)

The cyclic packed training stream supplies229,113,856 actual supervised targets/arm. Positive token-type frequency tertiles retain integer ties: low≤49, mid50–447, high>447; zero unseen. Type counts30,259/29,950/30,056/61,671 and final-test target counts1,481/20,752/677,902/172 respectively. Smoke/formal frequency files are separate.[Formal frequency](supporting_sources/frequency_manifest_formal.json)

| Training setting | Frozen common value |
| --- | --- |
| Initialization | fresh semantic-name SHA-derived, seed20261106, matrix normal(0,.02) |
| Batch | world4×micro16×accumulation2×seq2048=262,144 valid targets/update |
| Budget |874updates,229,113,856targets/arm; identical order |
| Optimizer |fused AdamW,lr3e-4,beta(.9,.95),eps1e-8 |
| Decay/clip |matrix.1,norm/scalar0; global gradient clip1 |
| Schedule |87-update/22,806,528-target warmup, then constant; initial update lr0 |
| Precision |BF16 autocast,FP32 optimizer state |
| Routing |no auxiliary loss/capacity drop; load-bias.001 sign(expected−actual) |
| Save/evaluate |steps0/437/874,targets0/114,556,928/229,113,856; full dev/test |
| Selection |fixed endpoint; final model metrics never select model/buckets/budget/checkpoint |
| Resources |single-node4H100 reserved,jobpt-ds9bdaxb,actual hardware verified |
| Seed2/C |not scheduled; prioritize one complete A/B pair |

[Actual config](supporting_sources/common_frozen.json)SHA`dd768489b9a58a49c09b85fedb9009bb80d7530a63dd235a9bb960265e16f3d5`. Non-first-smoke medians2.0798338661s(A)/2.0384610565s(B) select874even updates under the registered rule. Each trajectory contains roughly3.484training-stream lengths of target exposure, not independent new corpus data. Reliable entity/relation/fact evaluation is NOT RUN.

## Protocol conformance and deviations

| Registered object | Actual evidence | Eligibility/boundary |
| --- | --- | --- |
| Parameter/top-k/width fairness |actual enumeration and shared initial tensors |PASS; not identical initial functions |
| Actual initial seed |saved seed20261106 audit,242common parameter tensors |PASS; earlier seed17 hashes qualify implementation only |
| Dual smoke/recovery |A/B observed step3,786,432targets; A external replay/dev reload exact |PASS in that scope; not every B/formal recovery |
| Nominal4-step smoke config |orchestration stops at3; retain both fields |engineering scope,not formal budget |
| Sample review |pre-formal text/boundary and automatic examples; explicit Codex bucket reading after formalA |timing deviation; no external human review/rule changes |
| Timing background |34,545,588,066bytes sequential smoke-SHA reads overlap early formalA |unmeasured I/O impact; tokens/updates unchanged |
| FLOPs |matrix work measured,SDPA incomplete |not total measured model FLOPs |
| Deduplication/proxy |exact doc dedup,prefix/cyclic-exposure scope |near duplicates/semantic interpretation unverified |
| Paired endpoint completion |COMPLETE,874updates/229,113,856targets each |bounded engineering completion;scientific judgment Unknown |

## Complete measurements and learning curves

Both arms completed 874 updates/229,113,856 targets and all 12 planned arm×checkpoint×split evaluations (start/middle/end on dev/test). Every evaluation retains low/mid/high/unseen/overall. The endpoint test-low estimate is primary; remaining measurements describe registered costs/curves rather than rescue the primary outcome.

| Split | Step | Training targets | Bucket | Targets | A NLL | B NLL | B−A | 95% interval |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| dev | 0 | 0 | Low seen, primary | 1253 | 12.123834 | 12.114659 | -0.009175 | [-0.031376,+0.019469] |
| dev | 0 | 0 | Mid seen | 17259 | 12.127657 | 12.126628 | -0.001029 | [-0.007823,+0.005774] |
| dev | 0 | 0 | High seen | 612343 | 12.135714 | 12.129492 | -0.006222 | [-0.008683,-0.003649] |
| dev | 0 | 0 | Unseen | 124 | 11.977433 | 11.936586 | -0.040847 | [-0.105953,+0.016510] |
| dev | 0 | 0 | Overall | 630979 | 12.135439 | 12.129346 | -0.006093 | [-0.008520,-0.003532] |
| dev | 437 | 114556928 | Low seen, primary | 1253 | 13.799341 | 13.888605 | +0.089265 | [-0.009011,+0.217701] |
| dev | 437 | 114556928 | Mid seen | 17259 | 10.724088 | 10.758403 | +0.034314 | [+0.019149,+0.050036] |
| dev | 437 | 114556928 | High seen | 612343 | 4.730196 | 4.748679 | +0.018483 | [+0.015772,+0.021281] |
| dev | 437 | 114556928 | Unseen | 124 | 16.217555 | 16.165173 | -0.052382 | [-0.721564,+0.453996] |
| dev | 437 | 114556928 | Overall | 630979 | 4.914412 | 4.933455 | +0.019043 | [+0.016352,+0.021768] |
| dev | 874 | 229113856 | Low seen, primary | 1253 | 12.708120 | 12.912340 | +0.204220 | [+0.133821,+0.292902] |
| dev | 874 | 229113856 | Mid seen | 17259 | 9.048440 | 9.102330 | +0.053890 | [+0.031540,+0.075349] |
| dev | 874 | 229113856 | High seen | 612343 | 4.126327 | 4.132331 | +0.006004 | [+0.003548,+0.008805] |
| dev | 874 | 229113856 | Unseen | 124 | 16.039734 | 16.326879 | +0.287146 | [+0.041870,+0.558622] |
| dev | 874 | 229113856 | Overall | 630979 | 4.280343 | 4.288106 | +0.007763 | [+0.005433,+0.010421] |
| test | 0 | 0 | Low seen, primary | 1481 | 12.110444 | 12.108813 | -0.001631 | [-0.028095,+0.031923] |
| test | 0 | 0 | Mid seen | 20752 | 12.116739 | 12.113862 | -0.002877 | [-0.009434,+0.002924] |
| test | 0 | 0 | High seen | 677902 | 12.140313 | 12.131890 | -0.008423 | [-0.011397,-0.005619] |
| test | 0 | 0 | Unseen | 172 | 12.197198 | 12.202816 | +0.005617 | [-0.063097,+0.053312] |
| test | 0 | 0 | Overall | 700307 | 12.139565 | 12.131325 | -0.008241 | [-0.011128,-0.005502] |
| test | 437 | 114556928 | Low seen, primary | 1481 | 13.670386 | 13.769560 | +0.099174 | [+0.023346,+0.166672] |
| test | 437 | 114556928 | Mid seen | 20752 | 10.614290 | 10.673496 | +0.059206 | [+0.026605,+0.092060] |
| test | 437 | 114556928 | High seen | 677902 | 4.751133 | 4.763442 | +0.012309 | [-0.000218,+0.021132] |
| test | 437 | 114556928 | Unseen | 172 | 15.787790 | 16.038730 | +0.250939 | [+0.080628,+0.391998] |
| test | 437 | 114556928 | Overall | 700307 | 4.946447 | 4.960389 | +0.013941 | [+0.002069,+0.022456] |
| test | 874 | 229113856 | Low seen, primary | 1481 | 12.694702 | 12.911912 | +0.217210 | [+0.125969,+0.300351] |
| test | 874 | 229113856 | Mid seen | 20752 | 8.837688 | 8.886862 | +0.049174 | [+0.032819,+0.064679] |
| test | 874 | 229113856 | High seen | 677902 | 4.129341 | 4.142017 | +0.012677 | [+0.004328,+0.024499] |
| test | 874 | 229113856 | Unseen | 172 | 15.847674 | 16.134700 | +0.287026 | [+0.027684,+0.433047] |
| test | 874 | 229113856 | Overall | 700307 | 4.289854 | 4.304112 | +0.014258 | [+0.006160,+0.025677] |

Final test low B−A is +0.217210 [+0.125969,+0.300351], overall +0.014258 [+0.006160,+0.025677]; dev differences are +0.204220/+0.007763. Both test-low trajectories worsen then partially recover, ending above initialization: A 12.110444→13.670386→12.694702, B 12.108813→13.769560→12.911912, endpoint minus own start +0.584258/+0.803100. Unseen also ends above its start. Mid/high/overall improve. These patterns are observations; their cause is Unknown.

![Full frequency curves and differences](figures/all_frequency_curves_and_differences.png)

Rows are low/mid/high/overall; left panels show A/B NLL, right paired B−A intervals. Bottom axis is common valid targets, upper axis counted matrix operations. Endpoint low/overall intervals are above zero. B starts slightly better overall, so its endpoint disadvantage is not simply an inherited worse initial NLL. Sources:[curve values](supporting_sources/learning_curve_coordinates.csv),[origin](supporting_sources/all_frequency_curves_origin.json). Target coordinates 0/114,556,928/229,113,856 map to counted matrix work 0/229,117,023,269,945,344/458,234,046,539,890,688 FLOPs in both arms. This excludes fused SDPA and is not full equal-hardware-FLOP evidence.

Intervals use RNG seed 20261106 and 2,000 paired recovered-document resamples, summed paired losses divided by eligible target counts. They describe evaluation sampling, not training-seed uncertainty or all packed-context dependence. Low has only 1,481 test targets (0.2115%) across 246/544 documents; bootstrap draws all 544 including zero-bucket documents. Unseen has 172.

## Measured costs and complete routing receipts

| System quantity | A | B |
| --- | --- | --- |
| Training-step targets/s | 131723.8 | 130933.4 |
| Training-step seconds | 1739.351 | 1749.851 |
| Process wall seconds incl initialization/all eval/save | 1893.533 | 1898.450 |
| Completion elapsed incl middle/final eval/save, different origin | 1852.186 | 1861.293 |
| Peak allocated GiB | 37.568640 | 37.573787 |
| Peak reserved GiB | 45.343750 | 45.253906 |
| Gradient reduce seconds | 15.351152 | 15.433329 |
| First-step forward route/dispatch/combine CUDA ms | 102.766496 | 100.925632 |
| Smoke partially counted operator FLOPs/token | 2000648805.794 | 2000649829.184 |

Both graph estimates are 2,201,354,240–2,402,680,832 training FLOPs/token, or 5.04360758e17–5.50487470e17 per arm. This range discloses causal-attention/backward/recomputation assumptions, not hardware instruction counts. `aten::mm` is measured identically; partially counted smoke operators add identified add/mul work while still missing fused SDPA, so their small difference does not measure total-model FLOP difference.

Expert computation is local with zero expert all-to-all; gradient reduction remains about 15.35/15.43 seconds. The first-step route/dispatch/combine profiler measure differs from the full formal-step timing scope. B throughput is about 0.60% lower, training-step total 10.50 seconds longer, process time 4.92 seconds longer. These descriptive sequential runs include unmeasured outside I/O overlap; no stable speed ranking is established.

CV is expert receipt standard deviation/mean; entropy is mean router-probability entropy in nats; H/log(E) normalizes its count-dependent ceiling only. Every layer has 458,227,712 assignments =229,113,856×top-2. Dead means zero receipts over the entire run, not every short window. Drop is zero. Receipt lists follow expert IDs starting at zero; counts are not independent information or gradient signal quality.

| Arm | Layer | E | CV | Entropy nats | H/log(E) | Dead | Drop | Expert receipts in ID order |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 1 | 8 | 0.207975 | 0.888744 | 0.427396 | 0 | 0 | 58186759, 50158660, 88060697, 54118635, 49176328, 51874353, 53083566, 53568714 |
| A | 2 | 8 | 0.108555 | 1.055738 | 0.507703 | 0 | 0 | 54743419, 56408325, 54195260, 54527585, 55319526, 53972217, 73615812, 55445568 |
| A | 3 | 8 | 0.113318 | 1.198620 | 0.576415 | 0 | 0 | 57118008, 73175059, 60393772, 54542675, 53647123, 52997949, 54165252, 52187874 |
| A | 4 | 8 | 0.132666 | 1.313775 | 0.631792 | 0 | 0 | 54998821, 54510134, 77118701, 55009909, 52894263, 53425089, 53258319, 57012476 |
| A | 5 | 8 | 0.122035 | 1.256925 | 0.604453 | 0 | 0 | 60945689, 53140246, 74513504, 54243252, 55095350, 55169290, 52167385, 52952996 |
| A | 6 | 8 | 0.111561 | 1.234520 | 0.593679 | 0 | 0 | 50976062, 54380560, 53498764, 56772244, 54639481, 60218205, 72856331, 54886065 |
| A | 7 | 8 | 0.066468 | 1.393800 | 0.670276 | 0 | 0 | 57378931, 65162093, 53068311, 60908216, 53631411, 55966226, 54493680, 57618844 |
| A | 8 | 8 | 0.142634 | 1.411101 | 0.678596 | 0 | 0 | 56506854, 54214747, 53741015, 53838474, 78452695, 55965858, 50676353, 54831716 |
| B | 1 | 6 | 0.195729 | 0.724248 | 0.404210 | 0 | 0 | 73042437, 69003238, 109088048, 63940923, 70090021, 73063045 |
| B | 2 | 6 | 0.050900 | 0.824676 | 0.460261 | 0 | 0 | 74178472, 83910114, 72717866, 72675579, 77452905, 77292776 |
| B | 3 | 6 | 0.097592 | 0.929748 | 0.518902 | 0 | 0 | 70578947, 91690502, 79489733, 72983799, 71028352, 72456379 |
| B | 4 | 8 | 0.147334 | 1.277991 | 0.614584 | 0 | 0 | 52793535, 55769061, 79441397, 52813783, 53780100, 54650089, 53618323, 55361424 |
| B | 5 | 8 | 0.117947 | 1.282186 | 0.616601 | 0 | 0 | 54644436, 56235224, 74560759, 58242567, 54430045, 54917661, 52638483, 52558537 |
| B | 6 | 10 | 0.068411 | 1.438987 | 0.624944 | 0 | 0 | 41819507, 44759159, 42985504, 45751857, 50000310, 45110310, 47746561, 52098057, 45592688, 42363759 |
| B | 7 | 10 | 0.087022 | 1.489640 | 0.646942 | 0 | 0 | 53217524, 43252927, 42586820, 45557766, 39744468, 50569623, 47140705, 49472955, 43754010, 42930914 |
| B | 8 | 10 | 0.162835 | 1.594438 | 0.692456 | 0 | 0 | 40997414, 40756107, 42837304, 43900506, 43824038, 46521360, 42716229, 46198894, 42916841, 67559019 |

For example B layer2 has lower CV, layer8 higher; it is not uniformly more balanced. Larger E changes average receipts by a counting identity, not evidence of improved signal. No forced-route/deletion/swap intervention identifies causation.[Raw routing](supporting_sources/routing.json)

## Real contrary cases and observation-side anomaly

Effects are not uniform across documents. Test document `8bf0f4a06d1d4d99bdf0e2c9cdb0c0e66b138d5c3adfc7e39932a15449d560bb`, whose prefix is election news, has one low-frequency target and low NLL difference +3.031697: B is worse. Document `ed988b8735f2a459a06d01139d928a9c3bd9a394a1cb7899ffe5e15fc9bc8d96`, a question about anonymous suggested edits, also has one low target and difference −3.366316: B is better. These post-hoc extreme cases are not topic-specific knowledge or representative-population claims. A document prefix does not identify the particular erroneous token.[All six cases](supporting_sources/document_examples.json)

A remote file was once read just after creation, before closure/full visibility, producing temporary NUL/JSONDecodeError. Reading after durable closure was normal. No production data/model/metric was changed on that basis. This is an observation-side visibility/timing anomaly, not a demonstrated training-numerics failure; finite/counting audits are separate.

## Evidence lineage, outputs and incomplete scope

| Observation/check | Raw evidence and computation | State/eligibility |
| --- | --- | --- |
| Exact parameters |actual tensor numel,tied-weight de-duplication |DONE_VALID,507,988,992 each,difference0 |
| Actual initialization/order |saved seed20261106 audit;874formal batch hashes |DONE_VALID,all batch hashes match |
| Smoke recovery |actual_smoke_audit,A exact external replay/dev reduction |DONE_VALID in actual scope |
| Formal completion |A/B completion plus audit/pipeline_completion |DONE_VALID,874/229,113,856 each,12 evaluations |
| Primary measurements |frequency_results,raw document sums/counts |DONE_VALID;independent final numeric/statistics audits PASS |
| Frozen source/input identity |current source/provenance SHA audit |DONE_VALID;frozen/legacy source hashes PASS |
| Saved asset lifecycle |smoke strict registered;formal receipt |DONE_VALID;formal A/B/analysis strict PASS |
| Full hardware FLOPs |profiler omits fused SDPA/other kernels |BLOCKED;partial measurement/explicit estimates retained |
| Facts/entities,C,seed2,representation/causality,width training |no execution |NOT RUN,not fabricated negative outcomes |

Selected result byte hashes are in[result_metadata_manifest.json](supporting_sources/result_metadata_manifest.json). Complete code/logs/checkpoints/raw arrays remain at the execution root. The root-owned artifact manifest/actual registration receipts own final checkpoint IDs and saved payload lineage; this document does not create another asset ledger.

## Observation, explanation and researcher decision

Observed final B NLL is higher for low/mid/high/overall; both low-frequency endpoints exceed their own starts. Under the registered direction no rare-token advantage appeared, and no rare-token gain was obtained in exchange for an overall cost. Total/conventional active parameters, target exposure and data order match; B received no extra capacity/data.

Candidate routing sets, optimization dynamics, initialization sensitivity and proxy relevance remain causally unresolved. Do not choose an unmeasured explanation for the negative result. One seed, a small cycled prefix, unchecked near duplicates, rare-target coverage and context dependence remain. The result does not invalidate all hierarchical architectures or establish semantic long-tail representation/SNR causation.

The researcher's decision remains Unknown. AI suggestion: review this negative result and proxy relevance before choosing stronger entity/relation or representation/functional validation. No next architecture is trained automatically. The[393,283,584-parameter width sketch](next_width_sketch.md) is unimplemented/untrained; this pair does not approve its training. UI renaming is unavailable and incomplete; task-named append-only memory exists. External human sample review was not performed. The[coverage ledger](coverage_ledger.md) and[single meeting entry](../../../../../../../daily_research_reports/1106/meeting_report/meeting_brief_depth_expert_allocation_cn.md) preserve completed, exploratory, blocked and NOT RUN scope. Engineering completion does not close Focus or scientific judgment.

## Final independent audits and actual asset IDs

Independent final numeric, frozen/legacy-source, paired-statistics and actual formal-initial-state audits PASS. All 30 NLL/difference values reproduce exactly; alternative interval reduction differs by at most 6.94e-18, with low/overall intervals identical. Formal A/B checkpoint families and analysis assets are registered and strict-access PASS; see Detailed.

The independent method reweights the same 2,000 document resamples by multiplicity matrices. All 30 raw NLL/difference values match exactly; interval rounding differs by at most 6.938893903907228e-18, with primary low/overall values identical. After strict-checking both formal families, actual formal step0 files are fully SHA-verified and loaded: seed20261106,242common parameter/252state tensors and differently shaped router/bias overlaps exact, empty optimizer/zero bias/counters. Seed17 implementation and smoke states do not substitute for the formal states.

[Final numerics](supporting_sources/final_numeric_audit.json) · [Source/legacy freeze](supporting_sources/final_source_freeze_and_legacy_audit.json) · [Independent statistics](supporting_sources/independent_final_statistics.json) · [Formal initialization](supporting_sources/formal_initial_weight_match.json) · [Prior two-family access](supporting_sources/formal_initial_both_families_access.json).

Formal asset IDs: `checkpoint_family_depth_expert_allocation_A_20261106`, `checkpoint_family_depth_expert_allocation_B_20261106` (each full states at0/437/874), and `analysis_depth_expert_allocation_20261106`. All pass the[current strict snapshot](/data/250010109/Research_System/assets/checks/20261106T175506021038Z_depth_expert_allocation_full_outputs.json). Platform SUCCEEDED is verified; scientific acceptance remains Unknown. The root owns the full artifact manifest and final local reading sync; this record does not assert future handoff receipts.

[Artifact manifest](artifact_manifest.json) · [Delivery checks](delivery_completion_checks.json) · [Selected evidence payload manifest](selected_evidence_payload_manifest.json)
