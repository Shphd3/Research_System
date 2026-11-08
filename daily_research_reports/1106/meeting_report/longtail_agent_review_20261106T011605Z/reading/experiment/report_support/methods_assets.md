# Methods and assets: last-layer knowledge-learning experiment

This appendix specifies the tested system, data population, supervision, controls and evaluation contract. It records configurations and provenance, leaving efficacy and architecture interpretation to the main report. The [frozen protocol](../../../originals/experiment/protocol_frozen.json) records scientific acceptance as `Unknown` and question state as `Open`; this appendix changes neither state. The [Chinese companion](methods_assets_cn.md) covers the same scope.

## 1. Models, identities and loading

The trainable system consists of an original Qwen3-0.6B Base with a small added module. The backbone, final RMSNorm and original output head remain frozen. Qwen3-4B supplies training distributions; the post-trained 0.6B and 8B assets retain separate comparison roles.

| Role and local asset | Parameter scale | Layers / hidden width | Configured position limit | Use in this experiment |
|---|---:|---:|---:|---|
| Qwen3-0.6B-Base-official（[包外资料 E002](../../../EXTERNAL_REFERENCES.tsv)） |596,049,920 unique|28 /1024|32,768|Main frozen student and parent of the two standalone SAEs|
| Qwen3-0.6B（[包外资料 E003](../../../EXTERNAL_REFERENCES.tsv)） |596,049,920 unique|28 /1024|40,960|Separate post-trained capability comparison; prior DEV work|
| Qwen3-4B（[包外资料 E004](../../../EXTERNAL_REFERENCES.tsv)） |4,022,468,096|36 /2560|40,960|Post-trained teacher, native non-thinking chat invocation|
| Qwen3-8B（[包外资料 E005](../../../EXTERNAL_REFERENCES.tsv)） |8,190,735,360|36 /4096|40,960|Prior survey candidate; no new 8B teaching arm in this matrix|
| Qwen3-4B-Base（[包外资料 E006](../../../EXTERNAL_REFERENCES.tsv)） |4,022,468,096 stored elements|36 /2560|32,768|Located Base teacher candidate; metadata/tokenizer checks|
| Qwen3-8B-Base（[包外资料 E007](../../../EXTERNAL_REFERENCES.tsv)） |8,190,735,360 stored elements|36 /4096|32,768|Located Base teacher candidate; metadata/tokenizer checks|

The post-trained 0.6B weight file stores 751,632,384 tensor elements because it contains identical embedding and output-head tensors. The duplicate hashes and configured tying establish the smaller unique count above. This storage duplication is not additional model capacity. The six inspected model configs name `Qwen3ForCausalLM`, `model_type=qwen3`, and saved `transformers_version=4.51.0`. Cached download metadata is retained, while exact upstream weight revisions are not established uniformly. The Base parent's full weight SHA256 is `cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba`. [Configuration refresh](../../../originals/experiment/model_config_refresh.json), stored-element inventory（[包外资料 E008](../../../EXTERNAL_REFERENCES.tsv)）, duplicate/version evidence（[包外资料 E009](../../../EXTERNAL_REFERENCES.tsv)）.

Tokenizer metadata declares `Qwen2Tokenizer` and a maximum length of 131,072 for these assets. The configured model limits are those in the table; this experiment qualifies short prompts, not 131k-token operation. Full token-string→ID maps were checked, including special tokens. The native head has 151,936 rows and 151,669 common assigned IDs. Base termination uses ID151643 (`<|endoftext|>`); post-trained chat models terminate with ID151645 (`<|im_end|>`). Termination positions are excluded from answer supervision. These policies are recorded in the cache layout（[包外资料 E010](../../../EXTERNAL_REFERENCES.tsv)）.

The actual runtime is PyTorch 2.8.0+cu128, CUDA 12.8 and Transformers 4.53.3. `AutoTokenizer` and `AutoModelForCausalLM` load local files, with native SDPA and BF16 original weights. Added modules use FP32 parameters; their increments are cast to the hidden-state dtype at injection. No quantized replacement model or CPU weight offload is part of the main comparison. The teacher uses its native chat template with `enable_thinking=False`; the Base student receives a plain-text question/answer prompt. These prompt roles remain explicit instead of being attributed solely to model size. Loading/cache implementation（[包外资料 E011](../../../EXTERNAL_REFERENCES.tsv)）, prompt and identity definitions（[包外资料 E012](../../../EXTERNAL_REFERENCES.tsv)）.

## 2. SAE and smaller-model assets retained for later work

Both standalone 0.6B SAEs belong to the exact official Base parent above. Their dimensions match the student's 1024-wide states, but their hooks differ from the present injection site.

| SAE asset | Actual input and sparsity | Historical quality record |
|---|---|---|
| E16 final weights（[包外资料 E013](../../../EXTERNAL_REFERENCES.tsv)） |Zero-based layer 27, `model.layers[27].mlp` forward-pre-hook: MLP input after post-attention layernorm;1024→30,000, Top32|Normalized reconstruction MSE0.0533820926 in its original summary（[包外资料 E014](../../../EXTERNAL_REFERENCES.tsv)）|
| A17 raw-attention final weights（[包外资料 E015](../../../EXTERNAL_REFERENCES.tsv)） |Zero-based layer 27, `self_attn.o_proj` output before residual addition;1024→30,000, Top32|Global normalized MSE0.1684186278 in its original summary（[包外资料 E016](../../../EXTERNAL_REFERENCES.tsv)）|

These historical errors describe their original data, filtering and hooks. The main experiment trains and evaluates neither SAE. Applying them to the post-trained 0.6B or interpreting the final-RMSNorm increment through either dictionary requires separate validation. On a fixed input sequence, the present injection occurs downstream of both hooks; autoregressive changes to the generated prefix can subsequently change upstream states. [Current auxiliary audit](../../../originals/experiment/auxiliary_assets_refresh.json).

Additional local assets preserve the user's approximate 0.2B/0.5B baseline routes:

| Model / related SAE | Actual identity and path |
|---|---|
| Dense baseline |281,431,040 parameters,8 layers, hidden1024; exact 33B-token milestone（[包外资料 E017](../../../EXTERNAL_REFERENCES.tsv)）. That Dense checkpoint has no embedded SAE.|
| Separate S7 model with SAE |281,431,040 backbone plus61,471,024 embedded-SAE parameters; S7 milestone（[包外资料 E018](../../../EXTERNAL_REFERENCES.tsv)）. Its layer 7 attention-output dictionary belongs to this separate trained model.|
| Ordinary MoE baseline |507,988,992 total parameters:301,989,888 experts,65,536 router,205,933,568 shared;8 layers, hidden1024,8 experts/top2. Exact33B-token parent（[包外资料 E019](../../../EXTERNAL_REFERENCES.tsv)）.|
| MoE gate-input SAE |Final weights（[包外资料 E020](../../../EXTERNAL_REFERENCES.tsv)）, tied to that exact MoE33B parent; zero-based layer 7 `blocks.7.norm2` output/native router input,1024→30,000, Top32; historical global NMSE0.2267446200 in its summary（[包外资料 E021](../../../EXTERNAL_REFERENCES.tsv)）.|

Here 33B denotes training tokens, not parameters. These auxiliary assets were inspected through metadata/access records and do not enter the main training matrix. Stable IDs and exact parent relationships are in the asset catalog（[包外资料 E022](../../../EXTERNAL_REFERENCES.tsv)）.

## 3. Real-text task, splits and selected populations

The target fact is an explicitly stated person's birth year. The existing local Hotpot training cache（[包外资料 E023](../../../EXTERNAL_REFERENCES.tsv)） supplies Wikipedia-derived context sentences. The task extracts one atomic `born` relation; it does not reuse a multi-hop Hotpot question as a single fact. Records retain the original context, title and subject, canonical four-digit year, source record/document IDs, JSONL line and byte offset/length, context and sentence indices, and answer character span. The exact upstream Wikipedia revision remains unknown for this transformed local cache.

Factual v3 identifies 47,514 eligible declared families and fixes 24,096 facts:1,024 development,1,024 sentinel candidates,2,048 biography-reference candidates, and 10,000 each for A/B. Automatic rules require an explicit subject and exact born year 1600–2019, check names/titles and date structure, and preserve occupational disambiguation without exposing the answer in the question. All selected facts pass source-byte/span readback across 17,577 source records. A deterministic 112-fact sample was read by an agent; human review count is 0. Earlier extraction failures and rejected/conflicting families remain in the data ledger. These checks establish agreement with the supplied text, with external historical truth and complete entity linking outside their scope. [Data card](../data_prep/v3/DATA_CARD.md), [quality receipt](../../../originals/experiment/data_prep/v3/final_data_receipt.json).

Source/entity families are formed from normalized titles and explicit subject aliases before hash-based splits. Declared aliases, duplicate versions and conflicting birth-year records are audited together. The old 40-fact survey is DEV material; previously viewed source families, including the recorded 71-title exclusion set, stay outside the new confirmation pool. New method selection uses separate development families, including a 128-fact development panel. Automatic alias grouping is documented evidence of separation, not complete semantic entity resolution.

The original student and teacher are screened on two fixed questions before module training for the relevant scale. A teacher closed-book-correct fact takes priority; otherwise the teacher must answer both questions correctly with its excerpt. Students that answer both screening forms correctly, or have unresolved screening, are excluded. Screening questions differ from the two held-out evaluation templates. The largest 20,000-candidate screen yields 19,849 eligible facts; A has9,923 and B9,926, so three eligible B facts remain unused in the balanced maximum. [Frozen selection manifest and rule](../../../originals/experiment/cohorts/expanded_greedy_semantic_v4/manifest.json).

| Nested training scale | A / B independent facts | Teacher closed-known | Teacher source-conditioned |
|---:|---:|---:|---:|
|2,048|1,024 /1,024|38|2,010|
|8,192|4,096 /4,096|153|8,039|
|19,846|9,923 /9,923|364|19,482|

The union is 19,846 unique training facts, not the sum of the three rows. Each scale starts fresh modules and optimizer state; facts are deliberately reused across scales. Source text and selection rules are fixed before training; each actual scale roster is frozen before that scale's training. Expansion follows measured time/storage, with all six arms and both seeds retained, without choosing an arm from its score.

The teacher prompt follows the recorded mode: existing knowledge only for `closed_known`, original excerpt for `source_conditioned`. The student receives only its question during training and free generation. All CE targets come from independently extracted source answers. A source-conditioned teacher therefore supplies document-grounded supervision; its answer is not evidence that the fact came from its own parameters. Student screening failure also includes answer-format failure and is not a measure of pretraining exposure.

One fixed 128-fact sentinel subset receives zero supervision. A separate 128-paragraph WikiText panel supplies 15,560 original tokens and 15,432 next-token targets, with the first token of each paragraph used as context. Its source families are separate from the task/reference families under the recorded checks. The paragraphs retain local preprocessing and possible sentence truncation; their NLL is a bounded general-text check. Natural-text manifest（[包外资料 E024](../../../EXTERNAL_REFERENCES.tsv)）, LM cache layout（[包外资料 E025](../../../EXTERNAL_REFERENCES.tsv)）.

Natural fact/entity frequency and Qwen pretraining exposures are `Unknown`. The experiment's low-exposure variable is the controlled number of answer-supervision presentations,1 or8. No common/rare natural-frequency conclusion is defined by these labels.

## 4. Shared memory, controls and loss

At each answer-prediction position, let \(h\in\mathbb R^{1024}\) be the frozen last-block output before final RMSNorm. The memory computes a 64-dimensional query, 256 slot weights, and a 1024-dimensional increment:

\[
q=W_qh,\qquad a=\operatorname{softmax}(Kq/\sqrt{64}),\qquad
\Delta h=c\,\sigma(w_g^\top h+b_g)\,W_oV^\top a.
\]

Here \(K\) has shape 256×64, \(V\) has shape 256×1024, \(W_q\) is 64×1024, \(W_o\) is 1024×1024, and the gate has 1024 weights and one bias. The signed values and all these parameters are shared across facts. The fixed initialization scale \(c\) calibrates the increment norm to0.001 of the reference hidden-state norm. The model predicts through its frozen RMSNorm/head from \(h+\Delta h\), using the actual BF16-cast increment. This is a learned shared parameter module, with gradient-based updates rather than per-fact database writes. Module implementation（[包外资料 E026](../../../EXTERNAL_REFERENCES.tsv)）.

| Arm | Added parameters | Answer objective / control |
|---|---:|---|
|`none`|0|Original frozen Base; no optimizer updates|
|`adapter`|1,393,665|Gated ordinary SiLU bottleneck 680; CE+KL|
|`memory_ce`|1,393,665|Shared memory; CE only|
|`memory_kl`|1,393,665|Shared memory; CE+KL|
|`memory_head`|1,393,665|CE+KL plus head64 projection-energy penalty|
|`memory_random`|1,393,665|CE+KL plus fixed random64 projection-energy penalty|
|`memory_l2`|1,393,665|CE+KL plus all-direction increment-norm penalty|

The executed matrix contains one frozen baseline and six module arms. Standard LoRA, full-backbone fine-tuning and8B-supervised training are outside this matrix.

All trained arms use the same facts, canonical answers, masks, realized order/exposures and optimizer budget within a seed. AdamW uses LR 0.001, betas(0.9,0.999), epsilon1e-8, weight decay 0, constant LR, gradient clipping 1, global batch 16 and accumulation 1. The task loss is averaged over valid answer-content prediction tokens. CE uses the full native 151,936-row head. Teacher→student KL is exact on the common 151,669 assigned-ID support, with temperature 2 and its square factor, weighted 0.5. The 267 undefined rows are excluded from KL; no top-k truncation or renormalized top-k approximation is used.

For head/random penalties, each token contributes projected squared increment norm divided by the detached squared hidden norm, then valid-token averaging. The shared head/random coefficient is 3.107190799106226. The L2 coefficient is 0.19419942494413914, the fixed 64/1024 scaling of that coefficient. DEV gradient calibration targets a head/task gradient ratio 0.1; the recorded achieved medians are 0.1 for head,0.0373431 for random and0.0298862 for L2. Equal dimension/coefficient or isotropic energy scaling does not equalize observed gradient strength. [Calibration and frozen settings](../../../originals/experiment/protocol_frozen.json).

`semantic_content_v4` moves consecutive leading tokens that individually decode to pure whitespace into the known teacher-forcing prefix. It retains merged whitespace/content tokens whole, preserves both complete input-ID sequences, and excludes EOS. Each selected birth year has four supervised content tokens. Free generation receives the original question prompt, with no supplied answer/whitespace prefix, document or teacher cache. Earlier whitespace-mask and effective-generation-default failures remain versioned DEV evidence; corrected rules and genuine GPU formal caches precede formal updates. Mask definition（[包外资料 E012](../../../EXTERNAL_REFERENCES.tsv)）, [source amendment v4](../../../originals/experiment/source/source_manifest_amendment_v4.json).

## 5. Independent reference spectrum

The spectrum uses frozen-student states at the actual pre-final-RMSNorm injection hook, from independent reference text. Each document is truncated to at most 256 tokens, with at most 64 evenly spaced eligible positions. A globally centered matrix supplies the covariance eigenspace, equivalent to right singular vectors of centered activations. The formal matrix has 32,768 rows, hidden width 1024 and 903 distinct biography families. The source manifest lists candidate positions before the final row cap; the summary and matrix digest identify the actual 32,768-row fit. [Reference summary](../../../originals/experiment/spectrum/biographical_v3/summary.json), sampling implementation（[包外资料 E027](../../../EXTERNAL_REFERENCES.tsv)）.

Stability splits whole source families by SHA parity and compares their top64 subspaces using squared Frobenius overlap divided by 64. The biography overlap is 0.8998475671 against the predeclared 0.7 threshold; effective rank is 1024 using the 1e-6-relative eigenvalue threshold. A separate non-biographical attempt contains 432 paragraphs from 94 source families and 26,590 fitted positions; overlap 0.6794761419 fails the same threshold. That failed reference remains preserved. The accepted basis therefore has an explicit biography-distribution scope. Failed non-biographical reference（[包外资料 E028](../../../EXTERNAL_REFERENCES.tsv)）.

Head64 denotes the largest-variance reference directions. Penalizing those directions expresses a soft preference for the remaining subspace; it does not assign a semantic label to small singular directions or identify a particular tail band. The random64 basis uses a fixed QR construction with seed 1105001. The spectrum loss uses the returned, gated post-\(W_o\), BF16-cast increment. The arithmetic displacement \((h+\Delta h)-h\) is recorded separately from this nominal increment.

## 6. Exposure schedule, counters and resource transition

Seeds 1105 and 1106 use the same source/entity assignment seed 1105, with the1/8 assignment swapped for 1106. High-exposure facts receive seven earlier presentations; final low/high presentations are paired in an effective update when possible. Real schedule events store cache `index` and per-fact `exposure_index`. Global ledgers count realized facts/tokens, including partial batches, with no DDP padding or inferred epoch multipliers. Within a seed,1/8 groups contain different facts; source-family paired method comparisons remain within the same quota group.

| Scale | Facts per phase | Updates per phase / trajectory | Semantic-token budget per phase, seed 1105 | Seed 1106 |
|---:|---:|---:|---:|---:|
|2,048|1,024|288|18,432|18,432|
|8,192|4,096|1,152|73,728|73,728|
|19,846|9,923|2,792|178,628|178,600|

The largest phase has an odd family count:1105 has 4,961 one-presentation and 4,962 eight-presentation facts;1106 swaps those counts. This gives 44,657 versus 44,650 presentations. The common paired schedule still has 2,792 updates. Actual schedule boundaries determine this count; it is not inferred from a single ceiling of presentations divided by 16. Full A→B counters are cumulative: 5,584 updates with 357,256/357,200 semantic tokens for the largest-scale design. These are counter definitions/budgets; the separate completion evidence owns actual endpoint completion. Schedule and training source（[包外资料 E029](../../../EXTERNAL_REFERENCES.tsv)）, actual saved A counter audit（[包外资料 E030](../../../EXTERNAL_REFERENCES.tsv)）.

Initial qualification used two RTX5090 GPUs, each33,668,988,928 bytes of reported memory. Four-step versus two-step-plus-resume checks matched module, optimizer, scheduler, all-rank RNG, identities, cursor and ledgers exactly; one-versus-two-rank ledgers also matched. Main arms run independently at world size 1. The qualification record（[包外资料 E031](../../../EXTERNAL_REFERENCES.tsv)） separates this engineering evidence from training efficacy.

The largest A phase was trained on the 5090 allocation `pt-vbvlpop3`. Following renewed authorization and measured qualification, job `pt-5gno22e6` supplies four H100 80GB GPUs for B and matched pre/A/B evaluations. A module/Adam/scheduler/RNG state is loaded from its exact saved A parent. Four cards run four independent world size 1 arms; they do not change per-arm global batch or exposure. Cross-device BF16 future trajectories are not assumed bitwise identical. Original5090 pre/A outputs remain available alongside new H100 evaluations. [H100 qualification](../../../originals/experiment/resource_transition_20261106/qualify/qualification.json), [handoff manifest](../../../originals/experiment/resource_transition_20261106/handoff_manifest.json).

The exclusive B reservation lets H100 B overlap old 5090 read-only A evaluation. The old worker then reaches its existing B-directory guard and preserves a FAILED/RECOVERY_REQUIRED record. A new gate requires this history, actual H100 stage/queue completion, source hashes and all12 parent links; it never rewrites the old failure. Final statistics use explicitly selected matched-device plans and verified original-path references for completed legacy packages. Bridge contract（[包外资料 E032](../../../EXTERNAL_REFERENCES.tsv)）.

## 7. Generation, scoring and uncertainty

Student free generation uses the same plain-text short-answer template across arms. Explicit overrides enforce `do_sample=False`, `num_beams=1`, `use_model_defaults=False`, at most 32 new tokens and batch 64. It stops at the first completed nonempty answer line or native EOS. The physical baseline uses seed 1105; trained endpoints record their run seed 1105/1106 in the actual plans. Generation is greedy in both cases. The fixes explicitly avoid a Transformers generation-config default overriding the intended decoding mode. Live evaluator（[包外资料 E033](../../../EXTERNAL_REFERENCES.tsv)）.

Every full evaluation contains all A/B facts plus the same 128 sentinels, with the trained original wording and two fixed held-out templates. The primary fact endpoint requires both held-out answers correct. Original-wording accuracy and teacher-forced content-token NLL are separate secondary quantities. Known wrong plus unresolved gives a known failed conjunction; otherwise an unresolved view remains unknown. Unknowns remain in the roster, with conservative and identification-bound reporting. Normalized aliases, single unqualified years, uncertain/multiple-year answers and format failures retain their original score-status labels and raw outputs. A separate lexical review flags known question-mark, hedge/negation and year-format risks without changing labels. [Statistical contract](../analysis_tools/v2/README.md), review rules（[包外资料 E034](../../../EXTERNAL_REFERENCES.tsv)）.

After B, fixed 192-fact diagnostics comprise 64A,64B and 64sentinel facts. Active memory, memory-off, keys-only permutation and values-only permutation use identical rows/order/batches and an independently measured shape-matched baseline; intervention seed is 1105002. Jointly permuting K/V is a function-preserving identity check, not a destructive intervention. Sentinel generation has a complete roster; sentinel NLL is `NOT_RUN` because no sentinel cache was supplied.

Paired 95% intervals use 5,000 source-family bootstrap resamples, base seed 11050031 with recorded deterministic per-contrast seeds. Question forms do not increase fact denominators. Results remain separate by training seed, teacher mode, phase and quota; this fact/family interval does not estimate training-seed variation. A retention comparison reports both whole-A postB-minus-postA change and retention conditional on known postA success; a zero conditional denominator is undefined. General-LM NLL divides total natural-log loss by 15,432 valid targets. Intervals are descriptive and unadjusted for multiple comparisons.

## 8. Cost and audit reading boundaries

Matched parameters and student updates are controlled quantities. End-to-end cost also includes teacher/student forward caches, spectrum preparation, checkpoint I/O and full free generation. Teacher caches are shared once per scale across arms/seeds; they are not charged as separate teacher runs for each arm. The common trainer also computes the raw KL diagnostic for the CE-only arm, with zero KL objective weight; its measured cost reflects this shared implementation, not an optimized standalone CE trainer. Segment time is inside unit time, which is inside a parallel-stage envelope. Per-process allocator peaks do not establish a synchronized whole-node peak, and allocation-window×GPU count is not a billing or pure-kernel measurement.

All large weights, caches, checkpoints and raw outputs remain execution-side. The [frozen source manifest](../../../originals/experiment/source/source_manifest_amendment_v4.json), [dataset provenance](../../../originals/experiment/data_prep/v3/frozen_files_manifest.json), [READY source/plan hashes](../../../originals/experiment/resource_transition_20261106/HANDOFF_READY.json) and asset registry（[包外资料 E022](../../../EXTERNAL_REFERENCES.tsv)） provide the reproducibility route. Current access checks qualify addresses; actual completion, numerical efficacy, mechanism interpretation and researcher acceptance remain separate records.
