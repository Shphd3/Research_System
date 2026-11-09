# Detailed: Frequency-interval residual MoE branch

## Purpose and actual stopping point

The question was whether fixed routing based on equal-width feature-frequency intervals improves next-token prediction (NTP) learning on inputs containing low-frequency features, relative to random groups with identical sizes, while freezing Qwen3-0.6B Base and CrossCoder. The user authorized audit, smoke and bounded execution after the gates passed, without changing the earlier φ results.

**Only same-window representation completion, grouping/routing diagnostics and necessary engineering smoke completed. Formal A/B and C/D learning comparisons were NOT RUN.** The prespecified TRAIN coverage gate failed. This was not budget exhaustion, numerical divergence or an observed absence of learning benefit. Learning utility remains `Unknown`.

This English companion follows the [Chinese Detailed](detailed_cn.md). The [Protocol](protocol.md) owns the frozen contract; [Summary](summary.md) provides the short reading entry. Execution artifacts reside at `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z`, called RUN below.

## Hypothesis, controls and actual setup

The primary support rule required endpoint A−B low-frequency validation-position NLL ≤ −0.005 nats and overall difference ≤ 0.005 for each paired seed, 20261018 and 20261019. Mixed directions, inadequate support or failed testability yield insufficient evidence. A/B tests the complete grouping strategy, not a frequency-homogeneity mediator. C/D isolates LB in its router setting; A/D compares complete methods.

A uses eight linear intervals on the original TRAIN probability scale. B shuffles the same feature pool and preserves each group size without matching within-group frequencies. Both use fixed top-1 unit gates. C/D use trainable bias-free linear softmax routers with the selected probability multiplying expert output. Only D adds 0.01 LB. Over the complete 256-position batch, LB is eight times the sum of detached expert load fractions times mean softmax probabilities. C/D add 8,192 router parameters; total parameter counts differ across conditions.

The Base is `/data/share/Qwen3-0.6B-Base`. The dictionary is the A22 checkpoint at `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/runs/formal_14layer_batchtopk_a22/checkpoint_000999997440.pt`: 14 layers, 16,384 features, original TRAIN normalization and threshold `0.051281172782182693`. Extraction uses zero-based blocks 1,3,…,27. Final h is block-28 residual-post before final RMSNorm.

TRAIN contains contexts 8192–8319, 130,712 valid positions, from global01/local-shard5/shard41. EVAL contains contexts 117658–117721, 65,402 positions, from global01/local-shard2/shard247. Each source starts at file offset 8,388,608; equal offsets in different files are distinct identities. Targets are actual t+1 tokens, excluding current/next special tokens and context-final positions, with no padding targets. Numeric z and h were saved together; h, targets, CSR pointers/IDs, contexts and absolute offsets passed same-dtype elementwise exact equality against the old cache. Original-bin SHA values were inherited, with current stat/content checks; full source bins were not rehashed. Producer output hashes are fresh. [Extraction receipt](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/provenance/cache_preparation_receipt.json)

Smoke used eight independent bias-free full FFNs, 1024→256→GELU→1024: 4,194,304 expert parameters, 524,288 active per position, approximately 1,048,576 matrix FLOPs/position, excluding head, teacher, GELU and indexing. C/D add approximately 16,384 router FLOPs/position. Formal width/budget selection among 64/128/256 was **not completed**; `width_timing` is empty. Inputs use TRAIN centering/scalar RMS; random up and zero down projections produce a residual added to original h. Frozen native BF16 norm/head semantics and FP32 CE preserve expert gradients. Routing uses the jointly encoded 14-layer teacher representation, not a free intermediate-layer router.

## Frequency construction and coverage failure

The 9,615-feature pool requires TRAIN hits ≥200, coverage ≥20 original 1,024-token contexts, and hits below N_train. Frequency is the TRAIN proportion with z_i>0. Eight intervals are equal-width in raw probability, left-closed/right-open except the last. B uses the same member counts.

The group score averages all members, including zeros, after converting each feature to c_i = z_i × the sum of its 14 decoder-vector norms. This removes positive feature-rescaling ambiguity, not activation-frequency differences; it is decoding amplitude, not semantic/function contribution. Stateless source-qualified hashes resolve ties/all-zero scores. All four fixed routing schemes had zero fallback; A had no ties.

| Expert | TRAIN frequency interval | Members | A positive-score positions | A routed | B seed18 | B seed19 |
|---|---|---:|---:|---:|---:|---:|
|0|[0.1530%,12.4424%)|9,253|130,712|0|8,239|11,388|
|1|[12.4424%,24.7319%)|183|130,700|0|5,728|4,183|
|2|[24.7319%,37.0213%)|124|130,712|0|26,589|5,973|
|3|[37.0213%,49.3107%)|34|130,712|129|11,791|6,622|
|4|[49.3107%,61.6001%)|7|128,235|201|61,270|51,372|
|5|[61.6001%,73.8895%)|3|125,395|646|3,499|1,741|
|6|[73.8895%,86.1790%)|2|119,722|9,893|3,231|18,887|
|7|[86.1790%,98.4684%]|9|130,583|119,843|10,365|30,546|

Intervals are rounded; [grouping.json](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/cache/grouping.json) retains exact values. A is identical across seeds. All bins exist, but A experts 0–2 receive no inputs; expert 3 receives only 129 positions across 128 contexts. Thus A fails the preregistered ≥200 positive-score routes/≥20 contexts per expert. Experts 4–7 and both B groupings pass. The 200/20 rule is a local minimum-learning-opportunity gate, not a universal statistical theorem.

## Three figures and their denominators

![Membership, hits and actual routing](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/figures/analysis_members_hits_routes.png)

Figure 1 separates member counts, positions hitting each scheme's own groups, and actual selected experts. Hit columns overlap and cannot be added as token totals. Route columns count each position once and sum to 130,712. A's first three groups hit almost every position yet receive none: feature absence does not explain their zero exposure.

![Feature-event allocation](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/figures/analysis_event_allocation_train.png)

Figure 2 uses the same A-frequency groups as rows in every panel, plus outside-pool features. Columns are actual experts. Cells count feature activation events routed to each expert, normalized by row events; multiple coactive features contribute separately. Only adjacent load bars count positions. A sends 91.6848% of TRAIN positions to expert 7. Among 95,544 low-feature positions, routes are `[0,0,0,0,136,603,6281,88524]`: 92.6526% go to expert 7, although all 964 low-frequency features belong nominally to group 0. EVAL routes `[0,0,0,0,69,175,4439,44608]` are descriptive, not validation-based tuning.

![Within-expert actual feature frequency](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/figures/analysis_within_expert_q_train.png)

Figure 3 plots empirical cumulative distributions across 9,615 eligible features of q_i,e: feature-i hits divided by positions actually routed to expert e. Zero means no hit among received inputs. Experts 0–2 have zero denominators, hence entire `NA` columns and no curves. Expert 3 has only 129 positions; curves are not significance evidence. Separately saved allocation_share divides by all feature-i hits and answers where that feature went; it cannot replace q. NPZ/CSV cover all 16,384 features. These q denominators describe one pass over the fixed cache, **not accumulated training exposure**. Future training q requires saved per-update routes and order, allowing a source position to change experts between updates. [Analysis provenance](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/provenance/analysis_receipt.json)

## Smoke qualification

The shape-matched 32-position native/cache guard had zero logit/CE error; branch initialization also matched exactly. Base/CrossCoder parameter versions and buffers were unchanged; head hashes matched. Down projections received first-step gradients. Initial up/task-router gradients were expected zeros, then became nonzero. Unrouted experts legitimately had no gradients.

One seed, 20261018, used common initialization/order and 128 TRAIN positions repeated for 32 updates. Another fixed 128 EVAL positions checked finite loss/trajectory only. Learning rate was 3e-4, without retry.

| Condition | TRAIN NLL: initial→32 | Separate EVAL NLL: initial→final | Engineering |
|---|---|---|---|
|A|3.642010→2.183547|3.039889→3.058244|PASS|
|B|3.642010→1.333752|3.039889→3.056395|PASS|
|C|3.642010→1.176653|3.039889→3.056019|PASS|
|D|3.642010→1.192075|3.039889→3.059398|PASS|

Falling repeated-set TRAIN loss with slightly rising EVAL loss shows fitting without guaranteed generalization, not a strategy ranking or simple sign/shift error. Persisted JSONL/TensorBoard valid-token coordinates passed. Serialized same-process next-update replay was exact; external-process recovery is `NOT_QUALIFIED`. Each arm had 4,096 repeated target exposures, 128 unique positions, plus a 128-position replay diagnostic. Its saved checkpoint is step16/2,048 exposures, not an endpoint. [Smoke receipt](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/smoke/smoke_receipt.json)

## Baselines, missing results and limitations

Low-frequency evaluation features have TRAIN p≤0.002455780647530449, the pool's 10th percentile; high-frequency p≥0.045861129812106, its 90th percentile. Low unions cover 73.10% of TRAIN and 75.37% of EVAL. The 962 high-frequency features cover every position; cohorts overlap. EVAL qualifies 944/964 low features and 962/962 high features at support≥20; insufficient features retain NA. These cohorts do not measure mastery of rare knowledge.

Current strict full-EVAL Base loss is **NOT_MEASURED**; full-window TRAIN Base loss is `Unknown`. The table above contains only 128-position diagnostics. Archived zero NLL from 512 contexts has an exact 65,402-row cache prefix matching this EVAL. Aggregating it gives historical overall 3.023366253, low-position 2.886969903 and qualified low-feature macro 2.585700217. Old head batch256 differs from current128, including tail shape: `HISTORICAL_REFERENCE_ONLY / BATCH_SHAPE_NOT_QUALIFIED`, excluded from formal comparison. Old overall 2.949103620 uses all 512 contexts. [Reuse receipt and mapping](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/provenance/baseline_reuse_receipt.json)

Paired A−B differences, per-feature learning gains, formal curves, C−D effects, cumulative training q/update counts, and endpoint W/ΔW spectra are `NOT RUN`/`NOT PRODUCED`. Leading-direction removal was not executed or automatically authorized. Source files/token positions are disjoint; document/near-duplicate independence remains `Unknown`. CrossCoder previously saw these texts. Two planned seeds and this limited window cannot establish population stability.

## Actual cost, provenance and next question

Job `pt-vv7zkyxf` was accepted at 10:52:51 UTC, started at 10:58:26, verified four H100 80GB GPUs at 10:58:31 and ended `SUCCEEDED`. Cache preparation took 35.50 seconds; the controlled pipeline took 72.46 seconds; formal updates were zero. Teacher Base forward took 1.765 seconds, CrossCoder encoding 0.521 and native guard forward 0.085, covering 196,608 raw tokens plus 8,192 guard tokens. Loading, CPU processing, saves and checks are not all GPU core compute. Only GPU0 performed extraction/necessary smoke; the two formal four-GPU waves never started.

CPU postprocessing took 22.55 seconds with at most four threads and no model forward. Peak Torch allocated memory was 8.381 GiB, excluding non-Torch memory; smoke RSS peaked near 2.82 GiB. Two-second supervision checked aggregate RSS≤64 GiB, disk≤8 GiB and wall≤90 minutes. No continuous pipeline CPU peak was recorded; final 0.385 GiB is not a peak.

Before any smoke update, an observation-only patch added per-position route logging. Old source/freeze remain archived in the [amendment receipt](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/provenance/freeze_observability_amendment.json). English Protocol completion followed initial freeze without changing Chinese design SHA. Exact A22-ID strict access verification occurred after extraction, not beforehand. A run-local SCO response patch handled a new workspace field without changing submission identity, permissions or profile.

The bounded finding is inadequate eight-expert exposure under these lists plus mean-contribution argmax, not rejection of frequency grouping, mediation, semantic function or pretraining capacity. Frequency/amplitude coupling remains a rival. **AI suggestion, not executed:** retain the exact bins, A/B memberships, data and tie rule; preregister one TRAIN-mean calibration s_g/mean_TRAIN(s_g), first checking cached exposure coverage against original s_g. Do not append training to this round. If the researcher rejects that score meaning, discuss it before any new run. Figures actually saved are PNG/PDF; SVG was not produced. No commit/push, new experiment or prior scientific-state update occurred.
