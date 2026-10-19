# What co-occurrence relationships establish so far

This round retains the limited judgment that feature co-occurrence contains statistical organization beyond simple frequency margins. It withdraws a definite account in which that organization directly provides a better allocation for joint learning. Nine paired runs did not support the predeclared low-frequency benefit, and all three allocations harmed the original model's evaluation performance. Local interventions and two additional refutation controls narrow the explanation to input-dependent updates, while the separate causal contributions of text repetition, sampling origin and optimization remain unidentified.

These are bounded AI interpretations of this round's evidence, not researcher scientific approval. Original results, failures and NA values remain preserved. The [Protocol](protocol.md), [amendments](execution_amendments.md) and [complete evidence record](detailed.md) trace the operations. Sections 6–9 provide a short route to findings and the next decision.

## 1. Larger purpose: allocating inputs for useful joint learning

We want to understand which inputs are suited to sharing parameter updates, beyond drawing groups of similarly activated features. Here a feature is one coordinate of the frozen CrossCoder dictionary; gated z_i(t)>0 defines its activation event at position t. Frequency statistics have not established that coordinate's identity as knowledge, a function or an expert. Useful allocation must improve real prediction at equal parameters, computation and text exposure.

## 2. This round's question: three bridges require separate tests

First, does co-occurrence contain organization beyond individual feature hit frequencies and each position's activation count? Second, when relationship groups become four-expert input allocations, do they outperform frequency rules and random groups matched by frequency bins? Third, if benefit or harm appears, can the way inputs jointly update experts explain it? Reproducible structure does not automatically imply transferable learning, and a local one-step effect does not automatically explain the training trajectory.

## 3. Hypotheses and strongest rivals

The structural hypothesis predicts better replication than random matrices with the same margins, and closer validation frequencies among real group members than controls with the same size and discovery-set mean frequency. The rival is that phi and the grouping procedure already prefer similar frequencies.

The learning hypothesis predicts that relationship allocation R beats both frequency F and matched random N by at least0.01 nat on a fixed low-frequency feature-conditional loss, while keeping overall loss within a0.01 nat noninferiority tolerance. Load, frequency composition, initialization and generic expert specialization can produce similar rankings. A more basic rival is that, regardless of grouping, terminal adapters repeatedly fit a small text cache without learning transferable changes.

## 4. Relationships and allocations: measured groups are not natural experts

The final 14-source CrossCoder jointly produces one16384-dimensional latent. It observes Qwen3 block outputs2,4,…,28 with original TRAIN normalization and a fixed gate. Positive phi measures whether two features co-occur more often than their independent frequency background predicts. After mutual top10-neighbor selection, one weighted community procedure forms groups. Original D contains 186 nonsingleton groups covering13,807 features.

R keeps those memberships. F orders features by D frequency and uses exactly the same group sizes. N permutes original group labels within D frequency deciles, exactly preserving each group's membership count per bin; continuous frequencies are not identical. All conditions calibrate hit-group scores by D means/SDs, choose one winning group and use the same D load-constrained mapping to K=4 experts.

This changes actual allocations rather than merely renaming experts. Even after optimal expert relabeling, conditions agree on only about 26% of positions. N retains only 2.88% of original within-group edges. However, one winner excludes other group scores from the routing decision, and winning group sizes differ. These limit this operationalization. Unselected score mass is neither representation deletion nor measured information loss: every expert still receives the entire hidden state.

## 5. Controls: what is fixed and what remains uncontrolled

Freeze Qwen3-0.6B-Base, CrossCoder, final normalization and the complete-vocabulary output head. Train only four rank32 biasless residual adapters after the deepest source, with 262144 total parameters and 65536 active per position. Down projections are nonzero and up projections start at zero; all conditions begin with identical logits/loss. Position t is allocated using only its prefix through t to predict the true t+1 token. Sampled native-model and cached-terminal logits/CE reproduce exactly.

Each condition runs three paired seeds, nine runs total. Every run uses 6120 updates and 1,566,720 valid-target exposures with identical input order, batch256, AdamW lr0.001 and other settings. TRAIN has 130,712 positions repeated for 12 drop-last epochs; EVAL has 523,136 positions. They come from different original TRAIN source files and a different file from structural VAL. Original-document and near-duplicate independence remain Unknown; CrossCoder encountered this TRAIN origin. Learning is therefore exploratory within-distribution evidence.

Fixed low/high lists each contain3916 features, defined only by D frequency. Of the low list,3737 reach the predeclared 20 EVAL hits,95.43% coverage; the remaining179 are explicitly unestimable. The primary metric averages true next-token loss over each feature's hit positions and then averages features equally. It is not a measure of rare target tokens or knowledge mastery. Features can co-occur and are not independent tasks.

Primary intervals use paired blocks of four consecutive contexts, fixed-feature ratio linearization and an approximate bootstrap:128 blocks and 2000 draws. Show the three seeds separately. These are not document-independent intervals and do not encompass all seed uncertainty. D expert loads are approximately 25%, but learning-source loads still differ by 1–4 percentage points; trajectory-wide load differences were not removed exactly.

## 6. Main phenomena: relationships, partitions and learning give different answers

### 6.1 Local relationships replicate better than hard community boundaries

Of the full D edges,86.60% survive in V; edge Jaccard is 0.764. Community matching has group-equal Jaccard0.548 but member-weighted Jaccard only 0.322. After changing q10 to q20, only 0.383 of original within-group pairs remain together. Partition sensitivity does not refute all co-occurrence relationships, while186 groups do not establish186 natural experts.

Repaired mean-matched controls cover all 186 groups/13,807 members. Actual validation log-frequency SD is 0.353 dex versus 0.605 dex for controls, a−0.251 dex contrast. The member-weighted contrast remains−0.155 dex and large groups also retain a difference. Numerous two-member groups therefore do not explain the entire similar-frequency pattern.

![Structural controls](figures/figure1_structure.png)

Figure 1's upper row uses full-cache size/mean-matched controls; its lower row uses full-pipeline row/column-margin nulls on 4096 positions per side. These scopes are distinct. Sample observed stability is 0.1953 versus a99-null range0.0334–0.0598. The smoothed frequency contrast is−0.06777 dex versus a null mean+0.01507 dex. All 99 draws are valid. Both approximate tail probabilities reach the resolution floor0.01; approximate Holm adjustment is 0.02, without nominal FWER guarantees. Original strict sampled Tb remains undefined because V contains zero counts. Smoothed Tb is a supplementary exploration introduced after viewing the old results; its p-value is not part of the original strict test.

These findings weaken the explanation that margins and the common pipeline suffice for every readout. They do not distinguish text regularities, encoding geometry and feature redundancy. Sample candidates require at least25/4096 hits: this does not calibrate the dictionary's rarest tail, the full graph or independent documents.

### 6.2 Relationship allocation does not provide the predeclared learning benefit

The table gives mean endpoint losses across three seeds in nat; lower is better. Low/high losses are feature-equal conditional averages; overall loss is token-equal.

| Condition | Low-frequency conditional | Overall | High-frequency conditional |
| --- | ---: | ---: | ---: |
| Original frozen model / zero adapters |2.4396|2.9491|2.8725|
| Relationship R |3.3587|3.8647|3.8748|
| Frequency F |3.3429|3.8663|3.8702|
| Matched random N |3.3527|3.8723|3.8779|

![Learning curves](figures/figure3_learning_curves.png)

Figure 3 uses the same EVAL and fixed exposure axis: thin lines are seeds, thick lines means, and dashed lines the original model. Every registered nonzero evaluation endpoint is worse than the original model. Harm is already about 0.03–0.04 nat at the earliest one-epoch endpoint and about 0.9 nat at the final endpoint. Decreasing training loss confirms adapters learn the current exposure; it does not establish transferable changes.

![Paired endpoints](figures/figure4_paired_endpoints.png)

Figure 4 shows R minus its control with the same seed, inputs and supported features. Negative values favor R. The three low-frequency R−F values are+0.00289,+0.03003,+0.01457; R−N values are−0.00903,+0.01180,+0.01518. Neither the predeclared benefit against both controls nor seed-direction agreement is met. This does not prove all relationship uses ineffective. It does not support learning utility for this winner→K4 terminal-adapter construction; small overall rankings cannot turn harm into benefit.

The original model's low-frequency conditional loss is lower than its high-frequency conditional loss. This directly limits the explanation that infrequent features necessarily carry harder-to-predict knowledge. Frequency here concerns representation events; knowledge rarity and learning difficulty were not measured directly.

## 7. Cause analysis: which explanations the evidence excludes

### 7.1 Actual-route one-step updates harm probes more after matching counts and norms

At the predeclared midpoint, every seed/condition uses 16 common donor/probe batches. Exchange donor route labels within frequency bins, preserving exact per-expert and per-bin token counts; probes retain their original routes. Match each expert's exchanged one-step adapter-parameter displacement L2 norm to the actual update. Hidden/logit displacement and functional-change magnitude are not matched. Every virtual SGD step resets from the same checkpoint and never enters formal training. Actual/exchanged updates are paired at the same seed/condition parameters. R/F/N have different checkpoints, so differences across conditions are not same-parameter causal routing comparisons.

![Local updates](figures/figure5_local_update.png)

Figure 5's upper row shows absolute probe-loss decreases for actual/exchanged updates; positive means improvement. The lower row shows their contrast. Every run's mean actual-step decrease is negative, as is every actual-minus-exchange point estimate, including norm-matched versions. R's three norm-matched seed contrasts are−0.01941,−0.01370,−0.00831 nat. R/F/N mean contrasts are approximately−0.0138/−0.0126/−0.0132, giving no relationship-specific compatible-update advantage. Some intervals cross zero; nine point estimates are not nine independent population proofs.

This excludes differing token counts or update norms as the sole explanation of these local contrasts. It does not exclude trajectory-wide load effects or establish the complete Adam trajectory's root cause. Probes equally average low features that occur in that batch and have full-EVAL support; this is not the same supported set as C's complete-EVAL primary metric.

The mechanism bridge is explicit. An input co-occurrence graph measures joint input-event distributions; the adapter output-matrix gradient also contains true-target-dependent error signals. Similar activation sets can yield joint updates unsuited to a probe when prediction errors differ. A local one-step SGD approximation relates probe-loss change to negative step size times the sum of donor/probe gradient inner products. Actual post-update loss decides this round's result rather than an inner-product substitute. [Derivation and boundaries](local_update_model.md) provide the full account.

### 7.2 A learned constant offset is insufficient to explain the main harm

Because every allocation harmed evaluation, a separate posthoc, no-training response decomposition tests this explanation. Each expert's linear response is δ_e(h)=U_eD_eh. The mean μ_e uses TRAIN hidden states with original route=e, giving δ_e(h)=U_eD_eμ_e+U_eD_e(h−μ_e). Hold final parameters, original routes and the full h fixed; retain either the constant response or the response to input deviations from the TRAIN mean. Zero/full losses reproduce the original arrays exactly. The constant is adapter(mean hidden), which by linearity also equals TRAIN mean(adapter response); this introduces no assumption about nonlinear experts.

R's mean overall full-response harm is+0.9156 nat. Constant-only harm is+0.1755, while input-dependent-only harm remains+0.8584. F/N agree in direction. Removing the constant restores only about 0.05–0.06 nat and cannot explain most harm; the input-dependent response at these checkpoints is itself sufficient for substantial harm. Loss interaction is negative, about−0.1182 nat for R, so component effects are not additive causal percentages. The [supplement](figures/supplement_response_decomposition.png) and CSV give all nine runs.

This rejects a convenient mean-based root-cause account. The result concerns this TRAIN-mean decomposition: the input-dependent component has zero expert-conditional TRAIN mean but can acquire an offset on EVAL if means shift. It neither excludes all calibration issues nor establishes a pure-variance mechanism. The functional consequences of these components at fixed parameters are identified; why training produced them remains unknown. Small-cache repetition, sampling-origin differences and optimization remain rivals.

Harm is not concentrated in one bad expert. Under fixed primary-metric weights, all 36/36 expert cells worsen on overall, low and high metrics; one expert contributes at most about 29% of total harm. Nonzero gradients were recorded throughout all 6120 updates. This broad failure to transfer cannot be explained solely by one starved expert or a low-frequency-specific issue.

### 7.3 Doubled first-direction activation concerns preprocessing offsets, not a transferable learning root cause

![First-direction sensitivity](figures/figure2_direction_sensitivity.png)

Figure 2 shows original shared latents, latents after raw first-direction removal at every layer, and their difference, with fixed texts/features and a common scale for the first two panels. The256 plotted positions are a slice of 8182 measurement positions, not separate per-layer feature plots. Directions were fit on uncentered raw H. Removing about 30%–99% of raw energy nevertheless raisesL0 from 249.53 to 512.15.

An explanation cannot stop at deleting common content changing features. Raw projection followed by subtraction of the old TRAIN mean mu equals projected centered variation plus an additional fixed offset. Keep directions/texts fixed and project around the original TRAIN reference mean: L0 becomes232.60 and event Jaccard increases0.394→0.819. NetL0 change decomposes into−16.92 from centered-direction projection and+279.54 from the fixed offset conditional on that projection. Two new high-value stripes also match the encoder constant-offset prediction. The [control figure](figures/supplement_centering_control.png) shows all three conditions.

The original implementation followed the requested operation; this is not a bug repair. The control identifies components of that sensitivity operation. Mean-preserving removal still worsens reconstruction at all 14 layers, and common semantics have not been established. This intervenes on CrossCoder input preprocessing; Section 7.2 intervenes on terminal adapter responses. Their means and objects differ and do not establish one shared mechanism.

## 8. Belief update: retained, narrowed and unconfirmed judgments

| Prior judgment / candidate explanation | This round's update |
| --- | --- |
| Co-occurrence is only frequency margins and graph-selection preference | Insufficient on the bounded sample; margins explain some similar-frequency organization, not all observed organization |
| Replicated relationships establish hard communities as natural experts | Narrowed: local edges replicate better, while hard boundaries and scales remain more sensitive |
| Co-occurring inputs are suited to joint learning | Unsupported by this operationalization; fixed-budget learning and local one-step interventions show no relationship-specific benefit |
| Low-frequency features identify rare, difficult knowledge | This proxy account fails; representation events, supervised targets and knowledge difficulty require separate definitions |
| Doubled activation demonstrates common-content removal | Narrowed to joint sensitivity of raw projection and frozen centering, with a large offset contribution identified by control |
| Learning harm mainly reflects the same kind of constant offset | This TRAIN-mean response cannot explain most harm; response to input deviations from TRAIN mean remains substantially harmful |

Root causes are identified only at the level of local update consequences and response components. Dead initialization, empty experts, mere expert relabeling, token-count/norm-only accounts of local differences, and dominant harm from this TRAIN-constant response are excluded. The evidence does not establish whether repetition, origin or optimization is the principal cause. Unknown is more accurate than presenting overfitting as a complete mechanism.

## 9. One next decision: check whether harm varies with origin

**AI recommendation: next use frozen-checkpoint readouts.** On fixed contexts from the same source file as TRAIN but not used for adapter training, evaluate paired zero/full adapters and compare their harm with the existing other-file evaluation. Hold parameters, routing construction and the D-defined feature list fixed; recompute paired metrics over features with estimable support in both text cohorts. Compare each setting's harm relative to its original model rather than raw losses across texts. Severe harm on same-source texts not used for adapter training would refute the requirement that harm needs cross-file evaluation. Clear variation with origin would locate an association, without identifying transfer causality from file comparisons.

File origin does not establish a semantic domain, and original-document independence must remain recorded. This minimal refutation will inform whether intervening on text repetition or optimization is worthwhile. Current evidence is enough to stop treating plausible-looking co-occurrence groups as a substitute for learning-utility evidence; it does not close every use of relationship information.

See the [delivery entry](README.md) and [Detailed record](detailed.md) for reproduction, CSVs, code, checkpoints and logs. The researcher's next decision and scientific approval remain Unknown.
