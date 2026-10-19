# Epoch-one regions and learning efficiency

At equal exposure, old frequency routing T_S1 shows no heldout advantage over the learned-router references. All comparisons here use epoch one: 85,548 answer targets, 168 updates and model seeds 11/22. Regional gains are heterogeneous: experts 1/3 benefit in both seeds under existing descriptive intervals; expert 7 worsens in both.

A receiving region consists of prediction positions selected by old T_S1. One dialogue can contribute positions to several regions. Experts receive complete hidden vectors, not only their feature-list content. These old eight groups are distinct from the new four-band/relation analysis.

## Regional interpretation

All eight experts pass the original exposure floor and participate in 168 updates. Region 7 receives 8,546 TRAIN positions across 834 dialogues, substantially reduces TRAIN loss, but worsens EVAL. Region 3 receives fewer positions (6,704) and benefits. The result cannot simply be attributed to no training; generalization and update strength remain live explanations, without an identified gradient-interference mechanism.

Base EVAL difficulty varies across regions, approximately 1.0415–1.5637 NLL, so absolute regional losses cannot rank expert ability. Compare each region against its own zero-branch baseline. Existing bootstrap intervals are copied unchanged in the [region table](tables/T_S1_region_profile.csv); intervals crossing zero leave direction uncertain.

Every region includes approximately 46%–55% ShareGPT positions. Region 0 enriches CodeAlpaca to 19.3% of its positions (1.92 times global); region 5 has 18.7% WizardLM (1.42 times global). These are source preferences, not semantic expertise.

New descriptive decomposition of original saved GPU NLL finds that region 1 has mean two-seed changes of −0.24803 on CoT (511 positions/61 dialogues), −0.16792 on CodeAlpaca (472/41), and −0.00306 on ShareGPT (1,755/76). Region 7 changes +0.01811 on ShareGPT (1,172/72, 54.8% of region) and +0.02605 on CodeAlpaca (79/28). These subgroup point estimates have no new source-specific intervals and do not identify causal content effects. All source rows and support counts are retained in the [source decomposition](tables/T_S1_region_source_loss.csv); zero support is NA. This uses original GPU losses, not the numerically bounded auxiliary CPU expert-replacement branch.

## Equal-exposure comparison

![Epoch-one comparison](figures/epoch1_efficiency_table.png)

Mean overall EVAL NLL: frequency T_S1 1.229207, learned router 1.224635, learned router plus load balancing 1.224534; Base 1.242698. Reference-low macro NLL is 1.217047, 1.209216 and 1.209894 respectively; Base 1.218116. The reference-low metric uses the old L964 (960 estimable), not the new lowest-frequency band.

T_S1 has higher overall NLL by 0.004572/0.004673 versus the two references; both model seeds have the same comparison direction. T_S1 fits TRAIN more strongly but has less heldout improvement. The [comparison table](tables/epoch1_method_comparison.csv) and [individual seeds](tables/epoch1_method_comparison_per_seed.csv) retain actual values. With two seeds and previously inspected EVAL, this is descriptive, not a new confirmatory significance claim.

All branches share frozen Qwen3 Base, eight width-1024 SwiGLU experts, top1, supervision, initialization/data order and optimizer budget. Learned routers are linear hidden-to-eight softmax top1 gates; the balancing reference adds its original load objective. These are matched frozen-Base final residual branches, not full multilayer end-to-end MoEs. T_S1 uses multiplier 1 whereas learned branches multiply by the chosen softmax probability and add 8,192 router parameters. Routing and effective branch strength therefore change together; the comparison cannot isolate frequency grouping causally.

End-to-end compute/time efficiency is NA: cached training excludes CrossCoder extraction cost and no matched full-path benchmark was performed. Learning efficiency of the new four-band final-contribution/relation router is also NA because it has no corresponding trained states. AI suggestion: match branch strength and a common DEV-selected budget, evaluate on unselected holdout, and count complete extraction/routing costs if that causal/efficiency judgment becomes the next question. No such run was started.

[Artifact provenance](artifact_manifest.json). Researcher mechanism judgment remains Unknown.
