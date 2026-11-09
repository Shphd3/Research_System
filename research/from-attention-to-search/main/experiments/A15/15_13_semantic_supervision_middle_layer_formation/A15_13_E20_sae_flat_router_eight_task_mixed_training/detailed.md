# A15_13_E20 Detailed Evidence Ledger

[Summary](summary.md) · [Frozen Protocol and amendments](protocol.md)

## Current result and eligibility

Job `pt-os72i446`: SUCCEEDED, 2026-09-08 06:27:46 UTC (14:27:46 China time).
15/15 models completed 512 updates. 75 registered checkpoint files, 15 final checkpoint receipts, 15 test evaluations, 15 generation evaluations, 6 SAE/GMM interventions and 30 paired comparisons exist.
Registered numerical branch: **STRUCTURE_ONLY**. Human-owned mechanism judgment and Focus result remain awaiting confirmation; no Anchor/Focus scientific transition is performed by this report.

Primary NLL is eligible under amendments E20-A1–A4 and the verified identity bridge. Generation scores are BOUNDED to the actual shorter-cap, simplified scoring implementation; engineering completion is not a claim of exact full Protocol conformance. Sources: [completion receipt](/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z/completion.receipt.json), [verification](/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z/report_20260908/verification.json), [aggregate](/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z/results/aggregate.json).

## Full training process, architecture and loss audit

This section answers the researcher's full-report request from frozen source code, saved checkpoint configuration and per-record evaluation artifacts. It does not modify training, add a loss, rebalance experts or run new model evaluations. SAE pretraining below is the reused E16 predecessor, not another stage retrained for each E20 seed.

### Stage 0: pretrained sparse autoencoder (SAE)

The reused dictionary was trained previously on DCLM with the same frozen Qwen3-0.6B-Base, at zero-based layer 27's MLP input (1,024 dimensions). It has a 1,024→30,000 encoder and 30,000→1,024 decoder, with biases. Encoding is

\(a(h)=\operatorname{Top32}(\operatorname{ReLU}(W_eh+b_e)),\qquad \hat h=W_da(h)+b_d.\)

Pretraining minimizes normalized reconstruction MSE plus a dead-feature residual-reconstruction auxiliary term:

\(\mathcal L_{\mathrm{SAE}}=
\frac{\operatorname{mean}[(\hat h-h)^2]}{\max(\operatorname{mean}[h^2],10^{-12})}
+\frac1{32}
\frac{\operatorname{mean}[(\hat r-r)^2]}{\max(\operatorname{mean}[r^2],10^{-12})},
\quad r=\operatorname{stopgrad}(h-\hat h).\)

The auxiliary branch selects up to 512 features silent for at least 50 updates, uses their ReLU activations and decoder weights without decoder bias, and reconstructs the detached residual. It is zero when no dead features qualify. This is **not an MoE expert-load-balancing objective**.
The largest state norms above the process-batch 0.999 quantile are excluded; decoder columns are unit-normalized after each optimizer update. SAE weights are FP32 with BF16 autocast during pretraining; encoder uses Kaiming-uniform initialization with zero bias, decoder starts from normalized transposed encoder weights and zero bias.

One seed-17 run consumed 1,000,001,536 raw tokens in 244,141 updates, four synchronized GPUs × one 1,024-token sequence per GPU = 4,096 raw tokens/update. AdamW lr 3e-4, zero decay, ten-step linear warmup then constant lr, clip 1.0, no early stopping. Fixed validation normalized MSE: 0.789005 initially, 0.060492 at 100M, 0.057539 at 300M, 0.053382 at 1B tokens. There is no per-E20-seed SAE refitting.
Source: [E16 full summary](/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/full_summary.json), [SAE implementation](/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/sae_core.py), [training objective](/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/train_sae_full.py:265).

The full saved predecessor contract is:

| Pretrained SAE setting | Recorded value |
| --- | --- |
| aux_k | `512` |
| aux_weight | `0.03125` |
| contract | `"a15-e16-full-1b-v1"` |
| d_model | `1024` |
| dead_after_steps | `50` |
| grad_clip | `1` |
| k | `32` |
| layer | `27` |
| learning_rate | `0.0003` |
| manifest_sha256 | `"a82ee6a3f6dd5b56259a6bc384481ddf6522c48307f57cb8569752f82886bbe4"` |
| micro_batch_size | `1` |
| milestone_steps | `[24415,73243,244141]` |
| model_config_sha256 | `"504a6b58c4271583724e66584b6b7698aea18450209df6b2f7582df0e89cee59"` |
| n_latents | `30000` |
| outlier_quantile | `0.999` |
| seed | `17` |
| sequence_length | `1024` |
| steps | `244141` |
| warmup_steps | `10` |
| weight_decay | `0` |
| world_size | `4` |

E20 freezes this checkpoint, uses its encoder offline, and does not place its 61,471,024 parameters in the task-training expert parameter budget or require running the SAE online during model generation.

### Stage 1: audited data and cached states

The eight-task supervised fine-tuning (SFT) data have 39,571 training, 8,480 development and 8,481 internal-test records after six exclusions. Inputs are prompt followed by gold answer, right-padded to 512. Prompt and padding labels are -100. Train records are deterministically split within source by sorting SHA256("20260907|" + record_id): 19,784 discovery records, 19,787 offline-router-fit records. Discovery and router-fit are disjoint; expert training uses the full training split.

The frozen last-layer MLP-pre state is cached with padding excluded. The discovery view yields 23,520 nonempty segments, lengths up to 256. The router-fit view has 1,303,384 answer-prediction states; development has 572,496. This is not clustering over task IDs, and no task ID is an input to task-only routing.

### Stage 2A: SAE feature co-activation clustering

**Statistical unit:** a nonempty contiguous segment of at most 256 valid tokens from a discovery record, including available prompt and answer tokens. The objects being clustered are SAE features, not documents, tokens or class labels.

For segment \(s\) and feature \(i\), define \(X_{si}=1\) when the feature has any positive Top-32 activation in that segment. Repeated firing inside one segment is counted once. Let \(N=23,520\) segments, \(c_i=\sum_sX_{si}\), \(p_i=c_i/N\) and \(p_{ij}=N^{-1}\sum_sX_{si}X_{sj}\). Retain features with both \(c_i\ge32\) and \(N-c_i\ge32\). Similarity is binary Pearson/Phi correlation:

\(\phi_{ij}=\frac{p_{ij}-p_ip_j}{\sqrt{p_i(1-p_i)p_j(1-p_j)}}.\)

Remove the self-edge, keep each feature's 50 strongest strictly positive neighbors, break ties by feature ID and symmetrize by maximum: \(A_{ij}=\max(A^{\mathrm{directed}}_{ij},A^{\mathrm{directed}}_{ji})\). Remove isolated nodes. Construct

\(L=I-D^{-1/2}AD^{-1/2}.\)

Use the eight smallest-eigenvalue eigenvectors, row-normalize the embedding (floor \(10^{-12}\)), then K-means with eight clusters, seed 17, 20 initializations. Sparse eigensolver uses tolerance \(10^{-7}\), maximum 10,000 iterations and seeded initial vector; nine eigenpairs are requested for the eigengap diagnostic. Canonical group IDs are ordered by smallest retained feature index. Graph fragmentation into more than eight components or an empty output cluster is a failure.

Actual retained features: **29,471/30,000**. Group feature counts: **[4305, 4184, 4291, 3840, 2156, 8842, 1034, 819]**. These are feature counts, **not balanced token dispatch counts**.

For a causal answer-prediction state \(h_t\), convert feature activations into a soft teacher:

\(q_{t,g}=\frac{\sum_{i:G(i)=g}a_i(h_t)}{\sum_{i:G(i)\ge0}a_i(h_t)}.\)

Excluded features contribute zero; states with zero retained mass are masked out. There is no per-feature-frequency or group-size normalization in this teacher. This matters because larger activation mass can favor some groups; clustering alone does not enforce equal expert load.

### Stage 2B: matched random feature grouping

Sort retained features by their segment support, split into ten approximately equal-size frequency bins and permute group labels within each bin using seed 2718 (=17+2701). This preserves each group size exactly and approximately preserves feature-frequency composition, while destroying co-activation grouping. Observed adjusted Rand agreement with SAE grouping is approximately 0.0089. The soft teacher formula is unchanged. Matching feature counts is not matching token load or gate confidence.

### Stage 2C: flat prompt-state GMM clustering

**Statistical unit:** one discovery record's mean prompt-position MLP-pre state, excluding its answer. This differs from the full-segment SAE feature construction. Reduce its 1,024-dimensional vector to 64 principal components and fit **one eight-component diagonal Gaussian mixture**:

\(p(z)=\sum_{g=1}^8\pi_g\mathcal N(z;\mu_g,\operatorname{diag}(\sigma_g^2)).\)

PCA uses randomized SVD, no whitening, seed 17029. GMM uses 20 K-means-initialized restarts, maximum 100 EM iterations, convergence tolerance 0.001 and diagonal covariance floor \(10^{-6}\). Require convergence and all eight components occupied; canonicalize component IDs by lexicographically ordered means. **There is no parent/child hierarchy in the completed experiment.**

PCA explains 0.972756 of variance. Actual record cluster sizes are **[2728, 1425, 2298, 3504, 2443, 2030, 4993, 363]**. Assign each router-fit record to its maximum-posterior component; repeat its one-hot label for every valid answer-prediction state. GMM therefore supplies a record-level hard teacher, whereas SAE supplies a token-state soft teacher. The comparison does not isolate clustering algorithm alone.

Saved PCA defaults: copy=true, n_oversamples=10, iterated_power=auto, power_iteration_normalizer=auto, tol=0, whiten=false. Saved GMM defaults: init_params=kmeans, weights_init/means_init/precisions_init=null, warm_start=false, verbose=0, verbose_interval=10.
Sources: [graph.py](/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/graph.py), [teacher.py](/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/teacher.py), [gmm.py](/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/gmm.py), [observed group report](/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z/groups/group_report.json).

### Stage 3: nine offline router fits, then freeze

For SAE/random/GMM and seeds 17/29/43, fit a linear router \(p_t=\operatorname{softmax}(Wh_t+b)\), with \(W\in\mathbb R^{8\times1024}\) and \(b\in\mathbb R^8\). Optimize

\(\mathcal L_{\mathrm{offline}}=
\frac{1}{|\mathcal V|}\sum_{t\in\mathcal V}D_{\mathrm{KL}}(q_t\Vert p_t)
+\frac{\lambda_W}{2}\|W\|_F^2.\)

\(\mathcal V\) contains covered same-position states predicting supervised answers. The ridge penalty excludes bias. Adam lr=0.001, weight decay=0, batch=4,096 states (last per-shard batch can be smaller), up to 20 epochs per ridge candidate, clipping=1.0. Each ridge candidate restarts from identical seed-specific initialization and batch order; epoch shuffle seed is training_seed+1009×epoch. Select lowest development KL; stop each candidate after three non-improving epochs. No test selection.

| Teacher | Seed | Selected ridge | Best epoch | Dev KL | Teacher top-1 agreement % | KL gain over constant prior | Coverage % |
| --- | --- | --- | --- | --- | --- | --- | --- |
| sae | 17 | 0.0 | 1 | 0.055616 | 90.40 | 0.156507 | 100.0 |
| sae | 29 | 0.0 | 2 | 0.054182 | 88.61 | 0.157940 | 100.0 |
| sae | 43 | 0.001 | 1 | 0.073333 | 79.26 | 0.138789 | 100.0 |
| random_features | 17 | 0.001 | 1 | 0.050369 | 87.71 | 0.097938 | 100.0 |
| random_features | 29 | 1e-05 | 3 | 0.051833 | 86.87 | 0.096474 | 100.0 |
| random_features | 43 | 0.001 | 1 | 0.055237 | 83.87 | 0.093070 | 100.0 |
| gmm | 17 | 0.0001 | 7 | 0.801984 | 71.64 | 0.898918 | 100.0 |
| gmm | 29 | 0.0 | 2 | 0.792659 | 71.54 | 0.908243 | 100.0 |
| gmm | 43 | 1e-05 | 3 | 0.798155 | 70.58 | 0.902747 | 100.0 |

All nine selected routers have nonzero hard occupancy in eight groups and positive development KL improvement over their fixed teacher prior. This is a qualification guard, **not a balancing penalty or evidence of balanced usage**. Full four-candidate epoch counts and occupancy are in [router_selections.csv](/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z/report_20260908/router_selections.csv) and per-router selection.json. Task-only has no offline teacher fit.

### Stage 4: identical injection position, exact parameter budget

All five conditions modify **only the last Transformer layer, zero-based layer 27 (the 28th layer), at** \`model.layers[27].mlp.down_proj\`. They add a parallel low-rank residual to the existing 3,072→1,024 projection; they do not replace the whole MLP with eight full MLPs. The router reads the 1,024-dimensional MLP input after attention and normalization, while adapters read the 3,072-dimensional input to down_proj. Those are different tensors.

For gated MLP intermediate vector \(u_t\) and router input \(h_t\),

\(\Delta y_t=
\tfrac18B_sA_su_t+
p_{t,k_t}\,\tfrac18B_{k_t}A_{k_t}u_t,\qquad
k_t=\arg\max_g p_{t,g},\quad
y_t=W_{\mathrm{down}}u_t+\Delta y_t.\)

Shared and expert ranks are eight. The selected softmax coefficient is retained; **Top-1 is not renormalized to coefficient 1**. The dense control is \(\Delta y_t=\tfrac18BAu_t\) with rank 16. A matrices use Kaiming-uniform initialization; B matrices start at zero; no adapter bias or dropout is added.

Each rank-eight branch has \(8(3072+1024)=32,768\) parameters. Eight expert branches contain 262,144; the shared branch contains 32,768; the router adds \(8(1024+1)=8,200\).

| Condition | Expert-bank parameters | Shared parameters | Router parameters | SFT-trainable total | Added total including frozen router |
|---|---:|---:|---:|---:|---:|
| SAE | 262,144 | 32,768 | 8,200 frozen | 294,912 | 303,112 |
| Random features | 262,144 | 32,768 | 8,200 frozen | 294,912 | 303,112 |
| GMM | 262,144 | 32,768 | 8,200 frozen | 294,912 | 303,112 |
| Task-only | 262,144 | 32,768 | 8,200 trainable | 303,112 | 303,112 |
| Dense rank 16 | no expert bank | no shared branch | 0 | 65,536 | 65,536 |

All four routed models have exactly the same expert tensors. Task-only has only 8,200 extra trainable router parameters (+2.78% versus frozen-router SFT), not a bigger expert bank. Routed versus dense stored/trainable parameter counts are **not matched**: the frozen-router trainable bank is 4.5× the dense adapter. Per-token selected adapter rank is matched (shared 8 + selected 8 versus dense 16), excluding the separately computed router. This is not proof of exactly matched FLOPs or throughput.

Sources: [insertion](/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/model.py:89), [Top-1 coefficient and residual](/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/model.py:42), each final checkpoint's adapter tensor shapes and training.json parameter_contract.

### Stage 5: where the SFT loss is computed

SFT here means teacher-forced next-token learning on the answer only. The model sees the prompt and **gold answer prefix**, but causal attention does not expose the future answer token. The main loss is computed **after the final model normalization and language-model vocabulary head**, from output.logits; it is not computed locally on expert activations, at the SAE decoder, or on the route labels.

At zero-based position \(t\), compare \`logits[:, t, :]\` to \`labels[:, t+1]\`:

\(m_{i,t}=\mathbf1[\mathrm{attention}_{i,t}=1]\mathbf1[\mathrm{labels}_{i,t+1}\ne-100],\)
\(\mathcal L_{\mathrm{SFT}}=
-\frac{\sum_{i,t}m_{i,t}\log P_\theta(y_{i,t+1}\mid x_{i,\le t})}
{\sum_{i,t}m_{i,t}}.\)

The final prompt state predicts the first answer token and is included. Prompt targets, padding and the unavailable target beyond the final sequence position are excluded. The language head and backbone weights remain frozen, but gradients propagate through their operations to the injected adapters; freezing weights does not detach the computation graph.

Each effective batch has 128 records = 16 microbatches of eight. Compute the **total answer-token denominator for all 128 records first**; each microbatch backpropagates its summed cross entropy divided by that same denominator. This is not averaging 16 microbatch means or giving equal weight to each document/task. The numerical cross entropy is FP32. Formal code passes no labels to a built-in model loss and backpropagates only the explicitly constructed scalar.

Exact source: [causal mask and cross entropy](/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/train.py:19), [effective-batch backward call](/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/train.py:173).

### Explicit load-balancing-loss verdict

**All 15 E20 SFT runs have NO load-balancing loss.** There is no expert-uniformity term, entropy objective, router z-loss, capacity constraint, token-dropping loss or online semantic KL in the backward scalar. In notation, \(\lambda_{\mathrm{balance}}=0\) means the term is absent, not a configured positive term that happened to become zero.

| Stage / term | Present? | Meaning |
|---|---|---|
| E20 answer-only SFT cross entropy | yes, all five conditions | final vocabulary prediction |
| MoE load-balancing auxiliary loss | no, all 15 runs | not used |
| Online SAE/GMM teacher KL during SFT | no | frozen routers do not continue teacher training |
| Offline router KL + W ridge | yes, nine offline fits | teacher imitation and weight regularization, not load uniformity |
| AdamW adapter weight decay | yes, 0.01 | optimizer regularization, not load balancing |
| Predecessor SAE dead-feature auxiliary reconstruction | yes, weight 1/32 | SAE feature reconstruction support, not eight-expert balancing |
| All-eight-occupied qualification check | yes, offline router check | pass/fail guard only; no gradient contribution |

The conclusion follows from the actual loss expression and optimizer membership, not from a text search alone. The full-report verification also matches current source hashes to all 15 saved evaluation identities; A4's exact bridge preserves old checkpoint provenance.

### Stage 6: optimization, checkpointing and evaluation

All train 512 optimizer updates with fixed final selection. AdamW expert/shared lr=2e-4, weight decay=0.01; task-only router lr=5e-4, weight decay=0. Warmup is 26 updates then cosine decay, clipping norm=1.0, betas=(0.9,0.999), eps=1e-8, amsgrad=false. The saved final optimizer groups verify these defaults. There is no adapter/router dropout or label smoothing. Schedule samples 128 training indices per update uniformly with replacement, paired across arms by seed; it is not task-balanced sampling.

For zero-based optimizer step \(s\), the exact multiplier is \((s+1)/26\) for \(s<26\), otherwise \(\tfrac12[1+\cos(\pi(s-26)/(512-26))]\). At the final executed step 511 the lr is very small but not exactly zero. Stage-2 routers were frozen before stage-5 SFT; task-only's router is freshly initialized and optimized only via SFT. No straight-through estimator for argmax is used: its gradient flows through the gathered selected softmax coefficient, and routing choices can change as logits update.

The base is loaded BF16 with SDPA and kept in eval mode; added adapter/router parameters and inner arithmetic are FP32 with deltas cast back to the base dtype. Cached states/SAE values are stored FP16, indices INT32, positions INT16; router fitting converts states/targets to FP32. Training uses use_cache=false. All original model weights and language head are frozen. The four GPUs run four independent one-GPU conditions, not synchronized four-GPU training of each E20 model.

Save at 0/128/256/384/512 and recovery every 32 updates. Evaluate fixed dev at all five points; test is evaluated at fixed final only. No best-test selection or per-task hyperparameter tuning is performed. The registered per-record paired bootstrap and generation evaluator details remain below.

### Complete frozen configuration

These are all keys in the saved E20 Config, identical across the 15 evaluation manifests. They include operational values and immutable identities so no hidden config field is omitted. **Effective overrides:** bootstrap_fits=20 and graph_nulls=20 remain historical config values but only 14 repetitions per diagnostic were retained under A3; max_generation_tokens=512 is not used as a uniform decoding cap because generation_eval.py sets source-specific 4/64/256 limits.

| Frozen configuration key | Recorded value |
| --- | --- |
| accumulation | `16` |
| adapter_scale | `0.125` |
| artifact_limit_bytes | `100000000000` |
| audit_cluster_seeds | `[17,29,43,59,71]` |
| bootstrap_draws | `2000` |
| bootstrap_fits | `20` |
| cache_batch | `8` |
| cache_shard_records | `256` |
| checkpoints | `[0,128,256,384,512]` |
| cluster_seed | `17` |
| d_model | `1024` |
| data_seed | `20260907` |
| dense_rank | `16` |
| expert_lr | `0.0002` |
| expert_weight_decay | `0.01` |
| generation_batch | `8` |
| gmm_components | `8` |
| gmm_max_iter | `100` |
| gmm_mode | `"flat_diagonal_8"` |
| gmm_n_init | `20` |
| gmm_pca_dim | `64` |
| gmm_reg_covar | `0.000001` |
| gmm_seed | `17029` |
| grad_clip | `1` |
| graph_chunk | `128` |
| graph_nulls | `20` |
| groups | `8` |
| layer | `27` |
| max_generation_tokens | `512` |
| micro_batch | `8` |
| min_support | `32` |
| model_path | `"/data/250010109/model_cache/Qwen3-0.6B-Base-official"` |
| n_features | `30000` |
| n_init | `20` |
| neighbors | `50` |
| online_router_lr | `0.0005` |
| rank | `8` |
| raw_root | `"/data/250010109/datasets/a15_e14_raw"` |
| recovery_interval | `32` |
| ridge_grid | `[0,0.00001,0.0001,0.001]` |
| router_batch | `4096` |
| router_epochs | `20` |
| router_lr | `0.001` |
| router_patience | `3` |
| sae_k | `32` |
| sae_path | `"/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/sae_full_final.pt"` |
| sae_sha256 | `"e4e2049aced8ba9a3b043bbb2b3308b497b7ec22f107531e37197873ee545b65"` |
| seeds | `[17,29,43]` |
| segment_length | `256` |
| sequence_length | `512` |
| source_data | `"/data/250010109/datasets/a15_e14_p3_clean/processed.pt"` |
| source_data_sha256 | `"b2e1b4c5d43599c2d48736955a1532a8bd1b2a69787a4fed6da37cfaf793ac13"` |
| updates | `512` |
| warmup_updates | `26` |

Additional implementation-level constants: random-control frequency bins=10, permutation seed=2718; spectral eigensolver tolerance=1e-7 and maxiter=10000; normalization floor=1e-12; K-means uses init=k-means++, max_iter=300, tol=1e-4, algorithm=lloyd, copy_x=true and verbose=0 in the fitting environment, in addition to the explicit eight clusters, 20 initializations and seed 17. Phi graph uses strictly positive edges, max-symmetrization and graph chunk 128. Null edge switches request five attempts per edge but are capped at 5,000,000 attempts per retained diagnostic; mixing is not proven. Bootstrap and intervention seed for record comparisons=20260907; route-permutation seed=training_seed+314159. Generation is greedy (do_sample=false), batch eight, no sampling temperature/top-p intervention, EOS/PAD=151643, full reconstructed prompts left-padded at evaluation; caps MMLU/MMLU-Pro/GPQA=4, BBH=64, all other tasks=256. Code sandbox wall timeout=3s, CPU limit=2s, address-space limit=512MiB, output-file limit=1MiB, process limit=1.

Frozen base model configuration (checkpoint metadata, not a claim about the current runtime package version):

~~~json
{
  "architectures": [
    "Qwen3ForCausalLM"
  ],
  "attention_bias": false,
  "attention_dropout": 0,
  "bos_token_id": 151643,
  "eos_token_id": 151643,
  "head_dim": 128,
  "hidden_act": "silu",
  "hidden_size": 1024,
  "initializer_range": 0.02,
  "intermediate_size": 3072,
  "max_position_embeddings": 32768,
  "max_window_layers": 28,
  "model_type": "qwen3",
  "num_attention_heads": 16,
  "num_hidden_layers": 28,
  "num_key_value_heads": 8,
  "rms_norm_eps": 0.000001,
  "rope_scaling": null,
  "rope_theta": 1000000,
  "sliding_window": null,
  "tie_word_embeddings": true,
  "torch_dtype": "bfloat16",
  "transformers_version": "4.51.0",
  "use_cache": true,
  "use_sliding_window": false,
  "vocab_size": 151936
}
~~~

[Machine-readable frozen config](/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z/report_20260908/frozen_config.json). No GMM/SAE grouping hyperparameter or SFT loss was changed during reporting.

## Across-seed data totals and evaluation figures

All means use seeds 17/29/43 with equal seed weight. SD is sample standard deviation across the three seeds, **not a confidence interval**. Training loss uses the last 32 updates within each seed before averaging; test NLL remains answer-token weighted within each seed.

| Condition | Completed seeds | Train last-32 mean ± SD | Final dev mean ± SD | Test NLL mean ± SD | Generation macro %, mean ± SD |
| --- | --- | --- | --- | --- | --- |
| sae | 3/3 | 0.739514 ± 0.005823 | 0.744544 ± 0.001312 | 0.734773 ± 0.001347 | 19.77 ± 0.81 |
| random_features | 3/3 | 0.741395 ± 0.005266 | 0.746778 ± 0.002279 | 0.736627 ± 0.002398 | 20.73 ± 0.23 |
| gmm | 3/3 | 0.724972 ± 0.007497 | 0.730475 ± 0.001005 | 0.720896 ± 0.001094 | 20.68 ± 0.44 |
| task_only | 3/3 | 0.693783 ± 0.009057 | 0.700691 ± 0.002101 | 0.689914 ± 0.002028 | 20.50 ± 0.62 |
| dense_r16 | 3/3 | 0.742645 ± 0.005581 | 0.747749 ± 0.001271 | 0.737787 ± 0.001275 | 19.85 ± 0.20 |

[Full precision seed_means.csv](/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z/report_20260908/seed_means.csv).

![Evaluation overview](/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z/report_20260908/evaluation_overview.png)

Left: final answer-token NLL, lower is better. Right: generated eight-task macro score, higher is better. Bars are three-seed means, dots are individual seeds, whiskers are sample SD. This makes the disagreement between NLL ranking and generation ranking explicit; whisker overlap is not a significance test. Source: models.csv → seed_means.csv, producer report_full.py.

### Eight-task generation averages, with the final mean column

Percent scores; first average within a task over the three seeds, then average the eight task columns equally. No task-size weighting in the last column.

| Condition | mmlu | mmlu_pro | bbh | gsm8k | math | gpqa | humaneval | mbpp | Mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sae | 49.71 | 21.94 | 19.43 | 25.35 | 10.13 | 25.56 | 4.00 | 2.05 | 19.77 |
| random_features | 49.74 | 22.42 | 22.03 | 24.79 | 11.06 | 31.11 | 2.67 | 2.05 | 20.73 |
| gmm | 49.94 | 22.65 | 23.05 | 19.71 | 11.40 | 36.67 | 0.00 | 2.05 | 20.68 |
| task_only | 49.61 | 23.45 | 24.08 | 21.81 | 13.24 | 27.78 | 1.33 | 2.74 | 20.50 |
| dense_r16 | 49.58 | 21.43 | 17.28 | 25.37 | 10.83 | 27.78 | 4.00 | 2.51 | 19.85 |

![Task evaluation means](/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z/report_20260908/evaluation_tasks.png)

Cells show mean percentages; the last column is the arithmetic average of the eight preceding task scores using unrounded values. MMLU-like and small code/GPQA tasks have different difficulties and sample counts; color is not a statistical significance claim. Source: verified prediction correct/total counts → task_scores.csv → evaluation_means.csv, producer [report_full.py](/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/local_checks/report_full.py).

### All 15 per-seed task score rows

Each row has all eight task scores and its equal-task mean. The correct-count denominators and descriptive Wilson intervals remain in [task_scores.csv](/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z/report_20260908/task_scores.csv).

| Condition | Seed | mmlu | mmlu_pro | bbh | gsm8k | math | gpqa | humaneval | mbpp | Mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sae | 17 | 49.94 | 22.02 | 17.32 | 24.26 | 10.08 | 23.33 | 4.00 | 1.37 | 19.04 |
| sae | 29 | 49.55 | 21.91 | 20.90 | 25.25 | 10.13 | 23.33 | 4.00 | 2.05 | 19.64 |
| sae | 43 | 49.64 | 21.91 | 20.08 | 26.54 | 10.19 | 30.00 | 4.00 | 2.74 | 20.64 |
| random_features | 17 | 49.94 | 22.19 | 21.82 | 25.63 | 10.40 | 30.00 | 4.00 | 1.37 | 20.67 |
| random_features | 29 | 49.68 | 22.59 | 22.85 | 25.70 | 11.68 | 33.33 | 0.00 | 2.05 | 20.99 |
| random_features | 43 | 49.60 | 22.48 | 21.41 | 23.05 | 11.09 | 30.00 | 4.00 | 2.74 | 20.55 |
| gmm | 17 | 50.06 | 22.36 | 22.13 | 19.18 | 10.93 | 36.67 | 0.00 | 2.74 | 20.51 |
| gmm | 29 | 49.81 | 22.76 | 24.08 | 20.32 | 11.79 | 40.00 | 0.00 | 0.68 | 21.18 |
| gmm | 43 | 49.94 | 22.82 | 22.95 | 19.64 | 11.47 | 33.33 | 0.00 | 2.74 | 20.36 |
| task_only | 17 | 49.34 | 22.82 | 25.20 | 21.46 | 12.27 | 26.67 | 4.00 | 2.74 | 20.56 |
| task_only | 29 | 50.02 | 23.56 | 23.05 | 19.26 | 13.55 | 26.67 | 0.00 | 2.74 | 19.86 |
| task_only | 43 | 49.47 | 23.96 | 23.98 | 24.72 | 13.92 | 30.00 | 0.00 | 2.74 | 21.10 |
| dense_r16 | 17 | 49.55 | 21.33 | 16.60 | 26.00 | 10.51 | 26.67 | 4.00 | 2.74 | 19.68 |
| dense_r16 | 29 | 49.51 | 21.51 | 18.14 | 25.40 | 10.51 | 26.67 | 4.00 | 2.74 | 19.81 |
| dense_r16 | 43 | 49.68 | 21.45 | 17.11 | 24.72 | 11.47 | 30.00 | 4.00 | 2.05 | 20.06 |

### All 15 per-seed task NLL rows

NLL units are nats/answer token. **Task mean** averages the eight task NLLs equally; **token-weighted overall** is the registered primary metric and is generally different. Do not replace one with the other.

| Condition | Seed | mmlu | mmlu_pro | bbh | gsm8k | math | gpqa | humaneval | mbpp | Task mean | Token-weighted overall |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sae | 17 | 0.70918 | 1.27748 | 1.25538 | 0.70904 | 0.72849 | 0.77997 | 0.83632 | 1.07185 | 0.92096 | 0.73562 |
| sae | 29 | 0.72589 | 1.26076 | 1.24887 | 0.70867 | 0.72848 | 0.79357 | 0.82382 | 1.07267 | 0.92034 | 0.73548 |
| sae | 43 | 0.66672 | 1.24239 | 1.25287 | 0.70092 | 0.72928 | 0.77044 | 0.82489 | 1.07422 | 0.90772 | 0.73322 |
| random_features | 17 | 0.80429 | 1.37778 | 1.16786 | 0.71363 | 0.73003 | 0.84639 | 0.82334 | 1.04842 | 0.93897 | 0.73841 |
| random_features | 29 | 0.80631 | 1.38258 | 1.17454 | 0.70960 | 0.72977 | 0.86583 | 0.82171 | 1.07296 | 0.94541 | 0.73757 |
| random_features | 43 | 0.81949 | 1.28256 | 1.28432 | 0.69585 | 0.73044 | 0.77847 | 0.81373 | 1.05426 | 0.93239 | 0.73390 |
| gmm | 17 | 0.65188 | 1.19103 | 1.18020 | 0.67431 | 0.72529 | 0.73569 | 0.75808 | 1.05360 | 0.87126 | 0.72141 |
| gmm | 29 | 0.63560 | 1.14053 | 1.15492 | 0.67405 | 0.72443 | 0.73944 | 0.79649 | 1.01792 | 0.86042 | 0.71964 |
| gmm | 43 | 0.64935 | 1.16349 | 1.18179 | 0.67587 | 0.72533 | 0.73249 | 0.76738 | 1.04778 | 0.86794 | 0.72164 |
| task_only | 17 | 0.59520 | 1.13731 | 1.04960 | 0.57894 | 0.72037 | 0.73161 | 0.75956 | 1.00892 | 0.82269 | 0.68813 |
| task_only | 29 | 0.59772 | 1.12082 | 1.12891 | 0.58080 | 0.72062 | 0.72412 | 0.71769 | 1.02799 | 0.82733 | 0.68949 |
| task_only | 43 | 0.60993 | 1.12533 | 1.14335 | 0.58409 | 0.72197 | 0.74896 | 0.83530 | 1.04302 | 0.85149 | 0.69212 |
| dense_r16 | 17 | 0.77506 | 1.36809 | 1.32380 | 0.70757 | 0.73120 | 0.82064 | 0.81820 | 1.07530 | 0.95248 | 0.73859 |
| dense_r16 | 29 | 0.77621 | 1.36643 | 1.31247 | 0.70705 | 0.73140 | 0.82136 | 0.81580 | 1.07344 | 0.95052 | 0.73846 |
| dense_r16 | 43 | 0.77356 | 1.36671 | 1.32371 | 0.70015 | 0.73111 | 0.82097 | 0.82107 | 1.07240 | 0.95121 | 0.73632 |

## Post-hoc routing diagnostics and why task-only may win

These are newly summarized **observations from already saved test arrays**, not new model runs or a registered causal test. Each record array already contains all 562,954 answer-prediction routes and coefficients.

| Condition | Mean selected coefficient | Mean top-two token share % | Mean entropy-effective experts |
| --- | --- | --- | --- |
| sae | 0.5500 | 93.73 | 2.44 |
| random_features | 0.3826 | 81.44 | 3.02 |
| gmm | 0.7567 | 57.33 | 5.08 |
| task_only | 0.8573 | 72.90 | 4.14 |

Top-two share is calculated separately within each seed by ranking that model's occupied expert counts, then averaging the shares; expert IDs are not assumed semantically aligned across task-only seeds. Entropy-effective expert count is \(\exp[-\sum_k f_k\log f_k]\), a descriptive concentration measure, not the count of physical experts.

![Routing concentration and coefficient](/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z/report_20260908/routing_diagnostics.png)

Left: fraction of answer positions dispatched to each model's two most-used experts; right: mean native selected softmax coefficient. Dots are seeds, horizontal segments their means. This shows severe SAE concentration and larger task-only coefficients; it does not prove either causes the NLL gap.

### Full per-seed expert dispatch counts

| Condition | Seed | Expert 0 | Expert 1 | Expert 2 | Expert 3 | Expert 4 | Expert 5 | Expert 6 | Expert 7 | Top-two % | Mean coefficient |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sae | 17 | 581 | 239776 | 11744 | 308566 | 1496 | 713 | 39 | 39 | 97.40 | 0.5523 |
| sae | 29 | 266 | 221531 | 21848 | 315143 | 3798 | 282 | 62 | 24 | 95.33 | 0.5569 |
| sae | 43 | 498 | 246953 | 61729 | 251007 | 1930 | 604 | 78 | 155 | 88.45 | 0.5407 |
| random_features | 17 | 813 | 257269 | 85459 | 209487 | 122 | 9586 | 2 | 216 | 82.91 | 0.3793 |
| random_features | 29 | 139 | 276737 | 85574 | 188256 | 358 | 11560 | 3 | 327 | 82.60 | 0.3861 |
| random_features | 43 | 408 | 232134 | 110108 | 211583 | 129 | 8459 | 5 | 128 | 78.82 | 0.3826 |
| gmm | 17 | 165049 | 111106 | 19936 | 2702 | 2602 | 180780 | 21842 | 58937 | 61.43 | 0.7805 |
| gmm | 29 | 159452 | 118799 | 19913 | 4229 | 4350 | 171712 | 19318 | 65181 | 58.83 | 0.7499 |
| gmm | 43 | 138116 | 121649 | 58042 | 3218 | 2715 | 153182 | 19704 | 66328 | 51.74 | 0.7399 |
| task_only | 17 | 6931 | 6959 | 9317 | 13421 | 262771 | 180506 | 68752 | 14297 | 78.74 | 0.8940 |
| task_only | 29 | 6702 | 21820 | 116460 | 10929 | 16350 | 326596 | 19535 | 44562 | 78.70 | 0.8457 |
| task_only | 43 | 4153 | 12606 | 52330 | 88533 | 256302 | 79564 | 12722 | 56744 | 61.25 | 0.8323 |

Each row sums to 562,954. All physical experts are visited, but some SAE/random experts receive only tens or single-digit test answer tokens. This is why an all-groups-nonempty guard must not be described as balanced routing. These are held-out counts, not recovered exact training dispatch counts; training exposure concentration is a hypothesis, not a measured training ledger.

### Evidence-grounded explanation and strongest rival

1. **Direct implementation difference:** task-only updates its router to reduce the same SFT loss used to judge success. Frozen SAE/random/GMM routers optimize teacher imitation offline and cannot adapt their assignment or coefficient to expert utility during SFT. The comparison therefore includes optimization freedom, not only semantic versus nonsemantic information. Task-only does not receive dataset/task labels.
2. **Observed coefficient difference:** selected coefficients average 0.8573 for task-only versus 0.5500 for SAE, 0.3826 for random and 0.7567 for GMM. Because these multiply the expert output without Top-1 renormalization, task-only may learn a stronger expert contribution. **Rival:** its gain may reflect output scaling and update magnitude rather than discovering better expert categories. Comparing coefficients alone cannot establish realized residual norms or causality because trained A/B matrices differ.
3. **Observed concentration difference:** SAE's top two experts receive 93.73% of answer positions versus 72.90% for task-only. Thus eight stored experts are not equivalent to eight comparably used experts. Less concentrated task-only dispatch may allow broader useful capacity, but GMM is still less concentrated (57.33%) and loses to task-only; balance alone is not a sufficient explanation.
4. **Objective/proxy mismatch:** SAE reconstructs general DCLM hidden states and groups mixed prompt/answer co-activation; those groups need not be optimal partitions for supervised answer prediction. GMM and SAE teachers also differ in information and target softness. This is an explanation hypothesis, not evidence that SAE features are meaningless.
5. **Loss is not whole-answer accuracy:** SFT test NLL conditions on gold answer prefixes and weights every answer token. Generation evaluates an autoregressive answer with source-specific caps and answer extraction, then macro-averages tasks. Task-only's lower NLL does not imply the largest probability mass moves to a fully correct decoded answer; its mean generation score (20.50%) is not the best (random 20.73%).

No load-balancing-loss difference can explain the comparison: **all arms lack it**. The extra 8,200 trainable router parameters are real (+2.78%) but do not change expert-bank size. We have not isolated their capacity effect from end-to-end adaptation, gate coefficients or training dynamics; do not attribute the entire gap to any one of them.

**AI proposal, not a confirmed experiment:** if continuing mechanism work, the nearest separating question is whether task-only retains its NLL advantage when selected-expert output scaling is controlled. A matched-coefficient intervention would distinguish a scaling explanation from an assignment/adaptation explanation; if the gap largely disappears, stop claiming the result demonstrates better expert partitioning. Such an intervention is not executed or automatically authorized by this report.


## Completed model results

NLL is answer-only cross entropy divided by answer-token count; lower is better. Train last 32 is token-weighted over optimizer updates 481–512, not a full-training-set evaluation. Development and test use fixed sets. All rows have finite histories and gradients, 512 consecutive logged updates and strictly decreasing development NLL at the five measured checkpoints. This rules out observed divergence, not all overfitting or a guarantee of convergence.

| Model | Seed | Updates | Train last 32 | Final dev NLL | Test NLL | Eight-task macro % |
|---|---:|---:|---:|---:|---:|---:|
| sae | 17 | 512 | 0.739127 | 0.745375 | 0.735616 | 19.04 |
| sae | 29 | 512 | 0.733894 | 0.745225 | 0.735483 | 19.64 |
| sae | 43 | 512 | 0.745522 | 0.743032 | 0.733219 | 20.64 |
| random_features | 17 | 512 | 0.741882 | 0.748540 | 0.738409 | 20.67 |
| random_features | 29 | 512 | 0.735902 | 0.747591 | 0.737571 | 20.99 |
| random_features | 43 | 512 | 0.746401 | 0.744204 | 0.733901 | 20.55 |
| gmm | 17 | 512 | 0.724378 | 0.730976 | 0.721413 | 20.51 |
| gmm | 29 | 512 | 0.717791 | 0.729319 | 0.719639 | 21.18 |
| gmm | 43 | 512 | 0.732748 | 0.731131 | 0.721636 | 20.36 |
| task_only | 17 | 512 | 0.689149 | 0.698811 | 0.688134 | 20.56 |
| task_only | 29 | 512 | 0.687980 | 0.700303 | 0.689487 | 19.86 |
| task_only | 43 | 512 | 0.704219 | 0.702959 | 0.692122 | 21.10 |
| dense_r16 | 17 | 512 | 0.742348 | 0.748568 | 0.738589 | 19.68 |
| dense_r16 | 29 | 512 | 0.737219 | 0.748395 | 0.738455 | 19.81 |
| dense_r16 | 43 | 512 | 0.748369 | 0.746285 | 0.736316 | 20.06 |

Machine-readable source: [models.csv](/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z/report_20260908/models.csv).
All development curves start at 0.869630. The final measured point is lowest for every run, but the final checkpoint was preselected by update count.
SAE, random and dense achieve their lowest test NLL at seed 43; GMM at seed 29; task-only at seed 17. These are descriptive observations, not post-hoc checkpoint selection.

### Per-condition analysis

- **SAE:** stable small loss gain over matched random in all three seeds, but worse than GMM and task-only in all seeds. Generated-answer macro is below random in seeds 17/29 and slightly above it in seed 43. The loss advantage is not a consistent answer-accuracy advantage.
- **Random features:** near dense-rank-16 on loss, while its descriptive generation macro is highest on average (20.73%). This is not statistically established global superiority; GPQA and code tasks have small denominators.
- **GMM:** lower loss than SAE in every seed and second-best mean NLL, but below task-only. It uses prompt-level Gaussian grouping, not an isolated swap of clustering algorithm under otherwise identical teachers.
- **Task-only:** lowest test NLL in every seed; mean 0.689914 versus SAE 0.734773. Its router is trained online along with experts, so adaptation versus fixed routing remains a live explanation. Generation macro does not track the large NLL improvement. No causal explanation is established.
- **Dense rank 16:** highest mean NLL (0.737787), though close to random. It has 65,536 trainable parameters versus 294,912 frozen-router adapter parameters and 303,112 task-only parameters. Active low-rank capacity is aligned; total stored/trainable parameter counts are not equal.

## Loss curves

![All 15 training histories](/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z/report_20260908/training_loss_15.png)

Rows identify conditions; columns identify seeds. X: optimizer updates 1–512. Y: minibatch answer-token NLL, nats/token. Pale lines are raw minibatches; solid lines are 32-update trailing means weighted by answer-token counts. No seeds are averaged and no confidence band is implied. All runs decline early and flatten later; same-seed shared fluctuations reflect paired batches. The curves do not adjudicate held-out utility.

![Development loss by seed](/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z/report_20260908/development_loss.png)

X: updates 0/128/256/384/512; Y: fixed development NLL on 8,480 records and 572,496 answer tokens. Colors identify conditions; panels identify seeds. No smoothing or seed pooling. Task-only is consistently lowest after training; GMM is next. These development curves explain training behavior, not test-set significance.
Source for both figures: [loss_curves.csv](/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z/report_20260908/loss_curves.csv), extracted from each `conditions/<arm>__seed<seed>/training.json`; producer [report_completed.py](/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/local_checks/report_completed.py), whose hash is in verification.json.

## Primary paired evaluation

For each fixed seed, subtract SAE from its control's total loss and divide by the common 562,954 test answer tokens. Bootstrap resamples 8,481 records within source, 2,000 draws, seed 20260907. Records—not tokens or seeds—are bootstrap units; training seeds are never pooled. Positive favors SAE.

| Seed | Random minus SAE [95% CI] | Task-only minus SAE [95% CI] |
|---:|---:|---:|
| 17 | 0.002793 [0.002503, 0.003077] | -0.047482 [-0.048594, -0.046405] |
| 29 | 0.002088 [0.001809, 0.002363] | -0.045996 [-0.047092, -0.044922] |
| 43 | 0.000682 [0.000356, 0.000999] | -0.041096 [-0.042105, -0.040068] |

Random contrasts have positive lower bounds in all seeds; task-only contrasts are negative throughout. Thus `STRUCTURE_ONLY`, not `FULL_METHOD_ADVANTAGE`, follows the frozen numerical rule. No multiplicity-adjusted claim is made for the 30 secondary comparisons.

## Generated-answer evaluation

All 8,481 records have saved prompt-only greedy predictions for each of 15 models. Task denominators per model: MMLU 2,357; MMLU-Pro 1,753; BBH 976; GSM8K 1,319; MATH 1,875; GPQA 30; HumanEval 25; MBPP 146.
The table gives arithmetic means of three per-seed scores, in percent, without pooling seeds:

| Condition | mmlu | mmlu_pro | bbh | gsm8k | math | gpqa | humaneval | mbpp |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sae | 49.71 | 21.94 | 19.43 | 25.35 | 10.13 | 25.56 | 4.00 | 2.05 |
| random_features | 49.74 | 22.42 | 22.03 | 24.79 | 11.06 | 31.11 | 2.67 | 2.05 |
| gmm | 49.94 | 22.65 | 23.05 | 19.71 | 11.40 | 36.67 | 0.00 | 2.05 |
| task_only | 49.61 | 23.45 | 24.08 | 21.81 | 13.24 | 27.78 | 1.33 | 2.74 |
| dense_r16 | 49.58 | 21.43 | 17.28 | 25.37 | 10.83 | 27.78 | 4.00 | 2.51 |

[All 120 per-model/task scores, denominators, descriptive Wilson 95% intervals and per-task NLL](/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z/report_20260908/task_scores.csv).
Intervals are newly derived descriptive binomial intervals within a fixed model/task, not registered cross-model significance tests or uncertainty across training seeds. Small HumanEval/GPQA denominators make rankings unstable.

MMLU/MMLU-Pro/GPQA extract answer letters; GSM8K extracts the last numeric answer; MATH extracts simple boxed content or normalized strings; BBH uses normalized exact match; code tasks use the supplied tests in an isolated sandbox with timeout. This does not supply a full symbolic-equivalence MATH evaluator or every official BBH task scorer.
Actual maximum new tokens: 4 for MMLU/MMLU-Pro/GPQA, 64 for BBH, 256 for the remaining tasks. Scores therefore describe this capped evaluator only. Per-example outputs lack generation token counts and sandbox failure categories, so truncation rates and code-failure decomposition are UNKNOWN from saved metrics; no missing detail is invented.
Task-only's NLL advantage is measured under gold answer prefixes, whereas generated answers depend on autoregressive decoding and answer extraction. Their disagreement is observed; its mechanism remains unresolved.

## Expert-selection intervention

Within answer-prediction positions, selected experts were shuffled across records while preserving native coefficients and expert counts. Positive delta means native selection has lower loss.

| Condition | Seed | Shuffled minus native NLL [95% CI] | Changed routes % |
|---|---:|---:|---:|
| sae | 17 | 0.028417 [0.027464, 0.029437] | 50.67 |
| sae | 29 | 0.028063 [0.027178, 0.029018] | 52.03 |
| sae | 43 | 0.022082 [0.021316, 0.022861] | 58.54 |
| gmm | 17 | 0.042684 [0.041497, 0.043872] | 72.09 |
| gmm | 29 | 0.047142 [0.045879, 0.048484] | 72.99 |
| gmm | 43 | 0.043722 [0.042543, 0.044965] | 75.97 |

Source: `aggregate.all_pairwise.seed<seed>__sae__vs__gmm.left_intervention` and `seed<seed>__gmm__vs__dense_r16.left_intervention`, derived from native and intervention per-record loss arrays. All intervals are positive. This supports dependence on native expert selection for SAE/GMM, not superiority over task-only or semantic truth. Different changed-route fractions prevent treating raw effect magnitudes as matched intervention strength. Full singular values and pairwise adapter matrix cosines remain in per-model evaluation manifests as diagnostics, not evidence of semantic specialization.

## Actual training and conformance

| Registered item | Actual evidence | Status / effect |
|---|---|---|
| Frozen base, final layer 27, answer-only objective | All training receipts base_frozen=true; common model/data identities in paired evaluations | PASS for recorded contract |
| 5 arms × 3 seeds × 512 updates | 15 consecutive histories, 75 checkpoint paths, final hashes verified | PASS |
| Paired schedule | Same schedule hash and cumulative token count within each seed across all arms | PASS |
| Final checkpoint and sealed test | Fixed update-512 receipts used by test and generation; hashes match | PASS for final-checkpoint identity; no new test-driven selection |
| Data and denominators | All record IDs/source IDs/answer counts exactly paired; 8,481 records, 562,954 answer tokens | PASS |
| GMM hierarchy | Replaced with direct eight-component GMM under A1 before functional evidence | Approved amendment; old hierarchy ineligible |
| Repeated grouping audits | Five initializations and 14 repetitions retained; 18 outstanding repetitions cancelled under A3 | BOUNDED diagnostics; no null mixing/stability proof |
| Evaluation repair and reused checkpoints | A4 exact four legacy checkpoint hashes unchanged; common repaired evaluator identities in all pairs | PASS bridge; old failed evaluation ineligible |
| Generation cap and scoring | 4/64/256 source-specific caps; simplified score extraction | BOUNDED; not uniform 512-token or official evaluator reproduction |
| Per-task score intervals | Not emitted in original metrics; Wilson intervals derived from saved correct/total counts in this report | Explicit post-hoc descriptive completion, not new significance criterion |
| Full outcome | Aggregate hash matches completion receipt; predictions/records/checkpoint hashes match manifests | PASS integrity |
| Human scientific judgment | Not supplied for completed evidence yet | AWAITING_HUMAN_CONFIRMATION; no Focus or Anchor promotion |

Two stages are distinct: (1) nine offline linear routers fit to frozen teachers, dev-selected ridge, then frozen; (2) 512 task-training updates of low-rank adapters. Task-only instead trains its router during stage 2. No SAE or base-model training occurs here.
Stage 1: Adam lr 0.001, batch 4,096 valid answer states, up to 20 epochs, patience 3, ridge grid 0/1e-5/1e-4/1e-3. Stage 2: microbatch 8 × accumulation 16 = 128 records/update, AdamW adapter lr 2e-4, decay 0.01, task-only router lr 5e-4 with no decay, 26-step warmup then cosine decay, gradient clipping 1.0. Objective is answer-token cross entropy only; no online semantic loss. Optimizer starts fresh for task training; fixed offline router state is loaded.
Per-seed cumulative answer tokens: 17 = 4,339,651; 29 = 4,346,922; 43 = 4,351,700. Each condition samples 65,536 records across 512 updates, about 1.66 train-set-size equivalents, not 1.66 guaranteed unique passes.

## Evidence lineage and artifact map

| Evidence | Raw source | Transformation / verification | Eligible use |
|---|---|---|---|
| Completion | Platform SUCCEEDED; training.json; checkpoints; manifests | 512-step histories, 75 checkpoint existence, final/NPZ/prediction SHA256 checks | Engineering completion |
| Curves and model table | training.json history and validation_curve | No imputation; 32-step token-weighted display smoothing only; CSV extraction | Training behavior |
| Primary contrasts | evaluations/*/test/records.npz | Exact paired IDs/targets, token-weighted difference, source-stratified bootstrap; analysis.py | Registered internal NLL branch |
| Task scores | generation/*/predictions.jsonl | Recount correct/total per source; match metrics and aggregate; descriptive Wilson intervals | Bounded implemented generation scores |
| Expert intervention | native/intervention loss_sum arrays | Same record-stratified paired bootstrap | Native selection dependence only |
| Final aggregation | results/aggregate.json | SHA256 70323e0a309d02359c9c98ff980d6fd779b815e25bf1d9fe333f2b6fce200a9a matches completion.receipt.json | Complete machine result, not human mechanism judgment |

Execution root: `/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate`.
All raw outputs remain in [the run root](/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z); no checkpoints or logs are copied into the research repository. [Verification manifest](/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z/report_20260908/verification.json) records per-condition source hashes and reporting-script identity. Reproduce derived tables/figures with `python /data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/local_checks/report_completed.py`.
The remote job finished in approximately 4 hours after resumed startup. Historical failed jobs and qualified inputs are preserved below; these are not extra completed model seeds.

## Claim boundary and next decision

Primary answer-token comparison is eligible for the internal setting under the amendments. Generation is bounded to the actual evaluator. No official benchmark, clean-test contamination, semantic truth, optimal layer/expert count or causal reason for task-only superiority is established. Native-route intervention is not proof of semantic specialization. The dense control matches active rank, not total parameter count.

AI proposal: researcher reviews whether the small random-control gain warrants further mechanism work given the stronger task-only control and inconsistent generation gain. Completion criterion: confirm the bounded result and one separating question; stop or redirect if broad task superiority is required. No new run is automatically authorized. Focus/Anchor judgment remains awaiting human confirmation.

## Historical execution ledger (superseded snapshots)

The following text is preserved for provenance. Its STARTING, failed, missing and pending statements refer only to earlier snapshots; the current verified state and results above supersede them.

# A15_13_E20 Detailed Evidence Ledger

## 1. Execution state

```text
execution_status: EVALUATION_REPAIRED_RESUME_SUBMITTED
current_snapshot: 2026-09-08T02:27:13Z
historical_failure_stage: group construction / prompt-only hierarchical GMM
functional_training_started: true
formal_job_submitted: true
formal_job_id: pt-os72i446
formal_job_current_state: STARTING
scientific_verdict_available: false
protocol_amendment_applied: E20-A1, E20-A2, E20-A3, E20-A4
```

The first attempt stopped at the hierarchical-GMM gate. The researcher then
approved direct eight-group GMM and a minimal remaining audit. Amended Router
qualification passed, but the full job subsequently failed during intervention
evaluation after four completed training conditions. Sections 5-9 preserve the
earlier attempts and startup snapshots; section 10 owns the latest failure and
partial evidence. Section 11 owns the repaired continuation. No completed
functional comparison exists yet.

## 2. Provenance

- Execution root: `/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate`
- Run root: `/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z`
- Immutable source: `/data/250010109/datasets/a15_e14_p3_clean/processed.pt`
- Source SHA-256: `b2e1b4c5d43599c2d48736955a1532a8bd1b2a69787a4fed6da37cfaf793ac13`
- Derived data SHA-256: `58e409ca9d903d146c9ae8e3cee834a4eb5f0e6f2e24de4fe521349d05e527f2`
- SAE SHA-256: `e4e2049aced8ba9a3b043bbb2b3308b497b7ec22f107531e37197873ee545b65`

Source-code hashes, model shard hashes, configuration, cache input site, and
predecessor identities are embedded in each cache manifest.

## 3. Data and leakage audit

The raw renderer reproduced every retained processed identity, content hash,
token sequence, prompt length, answer-only label, and attention mask before
the cross-split audit was applied.

| Split/view | Records after audit |
|---|---:|
| train | 39,571 |
| discovery | 19,784 |
| Router-fit | 19,787 |
| development | 8,480 |
| internal test | 8,481 |

Six lower-priority records were excluded under the registered
`test > development > train` rule: five from train and one from development.
The audit found six cross-split groups under prompt-only or truncated-token
identity and five prompt groups with differing rendered answers. The exclusion
ledger is append-only and the source file was not overwritten. Exhaustive
near-duplicate absence is not claimed.

Prompt-left-truncation counts were 1,476/39,571 train, 330/8,480 development,
and 330/8,481 test. This reports the fixed source tokenization behavior; it was
not changed during execution.

Evidence:

- `/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z/data/audit.json`
- `/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z/data/exclusions.jsonl`
- `/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z/data/receipt.json`

## 4. Eligible activation-cache stages

All three cache receipts passed model, SAE, data, and configuration identity
checks. Attention padding was excluded. Router caches contain same-position SAE
activations and the causal state at \(t\) only when `labels[t+1]` is an answer
target.

| Cache | Records | Additional unit |
|---|---:|---:|
| discovery | 19,784 | 23,520 nonempty segments |
| Router-fit | 19,787 | 1,303,384 answer-prediction states |
| development | 8,480 | 572,496 answer-prediction states |

Discovery used independent 0:256 and 256:512 segments and retained nonempty
short tails. It contained 26,749,694 binary segment-feature incidences, an
average of 1,137.317 appearing SAE features per segment.

Evidence:

- `/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z/cache/discovery/manifest.json`
- `/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z/cache/router/manifest.json`
- `/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z/cache/development/manifest.json`

## 5. Decisive qualification failure

The registered prompt-only teacher used discovery-record mean layer-27 MLP-pre
states, PCA-64, three diagonal parent components, child allocation 3/3/2 by
parent size, seed 17029, 20 deterministic restarts per mixture, maximum 100 EM
iterations, and `reg_covar=1e-6`.

PCA retained 0.9727564872 of variance. The parent model converged and produced
canonical sizes `[5724, 13697, 363]`. Child results were:

| Canonical parent | Requested children | Occupied counts | Converged | Iterations |
|---:|---:|---|---|---:|
| 0 | 3 | `[1237, 2753, 1734]` | yes | 27 |
| 1 | 3 | `[7182, 3729, 2786]` | yes | 11 |
| 2 | 2 | `[363, 0]` | yes | 2 |

The last fit is numerically converged but structurally collapsed. Seven
occupied leaves cannot instantiate the frozen eight-expert GMM comparison.
The pipeline therefore stopped before saving qualified groups or fitting any
Router. No fallback, component reseeding, reassignment, or condition removal
was applied.

Evidence:

- `/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z/failure.json`
- `/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z/groups.failure.receipt.json`

## 6. Tests and implementation evidence

The v2 unit and small integration suite passed 13/13 before full-data
qualification. It covers data schema and causal alignment, padding-free short
segments, hierarchical GMM reload prediction, dense-rank-16 scaling, total-
answer-token gradient normalization, paired schedules, attention-mask
propagation, evaluator known cases, an isolated no-network chroot code sandbox,
one-update base freezing, and validation-only offline Router selection.

A separate real-GPU cache smoke on eight audited records passed before the
full-data qualification run. These checks establish implementation readiness
only and do not override the failed GMM construction gate.

## 7. First-attempt missing evidence and claim boundary

The following required outputs do not exist: nine offline Routers, five-arm
one-update qualification smoke, 15 update-512 checkpoints, validation learning
curves, paired internal-test losses, eight-task generation scores, SAE/GMM
selection interventions, and expert update geometry. Their absence is expected
after the registered stop.

No claim can be made about SAE functional utility, superiority to random or
task-only routing, comparison with GMM, task performance, expert function, or
the best layer/expert count. The only direct conclusion is constructibility
failure of the frozen GMM control on this audited split.

## 8. Amended qualification and minimal audit

At 2026-09-08 01:06 UTC the detached continuation process was fitting
`sae__seed17`. No completed Router receipt or formal job receipt existed at
this snapshot. Current operational source: `continuation.status.json` and
`continuation.log` under the run root above. The continuation script is
`continue_qualified.sh` in the execution workspace; it runs the retained gates
and calls `submit_full.sh` only after a PASS qualification receipt. It records
submission intent before the external call to prevent accidental duplicate jobs.

| Item | Verified observation | Evidence / boundary |
|---|---|---|
| E20-A1 construction | PCA-64, one diagonal eight-component GMM; occupied counts `[2728,1425,2298,3504,2443,2030,4993,363]` | `groups/group_report.json`; counts are constructibility, not utility |
| Qualified groups | SHA256 `69ec7cb174c548b02958109f2472e5e96b38cc36c8c7e761b7c2bd637a57f099` | `groups/receipt.json` and `groups/groups.pt` |
| Partial grouping diagnostics | five initializations and 14 bootstrap/null/GMM-bootstrap repetitions; no recorded failures | `group_audit/audit.json`; original preserved with `AUDIT_RUNNING`, not relabeled full PASS |
| E20-A2 scope | six remaining repetitions deferred, nonblocking | `amendments/E20-A2-MINIMAL-AUDIT/receipt.json` authenticates the partial report and implementation |
| Null validity | mixing not proven | descriptive diagnostics only; no null-significance claim |
| Data/cache identity | derivative hash unchanged and all three approved cache manifest hashes matched | E20-A1 exact-cache reuse receipt plus continuation checks |
| Implementation checks | 16/16 local tests pass | includes amended flat-GMM and partial-audit failure rejection; does not replace real training smoke |
| Remaining submission gates | nine Router fits: positive development KL improvement over constant prior and all eight hard selections occupied; five one-update smokes with frozen base | all mandatory; no waiver of an observed failure |

The researcher explicitly requested audit simplification before any Router or
functional result was available. The primary five-arm, three-seed, 512-update
comparison, supervision, test boundary, and metrics are unchanged. The partial
grouping checks cannot establish the originally requested full stability audit.
No scientific conclusion is promoted. The next action remains qualified full
submission under the existing 4xH100 reserved authorization.

Engineering continuation note (2026-09-08): the first Router attempt repeatedly
read immutable activation shards (about 35 GB read within several minutes).
It was interrupted before any Router receipt, with its output directory moved
to `interruptions/router-io-cache-20260908T010800Z/`. The replacement caches
unchanged shard tensors in host memory; tests verify exact equality of shuffled
batch order, states, and targets against direct loading and invalidate a changed
file. Objectives, optimizer steps, and selection rules are unchanged. Per-epoch
progress is now recorded. The 18-test suite passes. The worker synchronization
timeout is aligned to the existing 12-hour outer job limit so a rank assigned
three conditions does not prematurely kill a rank assigned four; no resource
or training budget is increased.

The smoke-only initial evaluation uses the first eight development records;
the actual smoke update still uses the paired 128-record effective batch and
the same gradient, parameter-freeze, mask, and numerical checks. The full run
continues to evaluate the entire development split at update zero and all
registered checkpoints. This removes an unnecessary full-split traversal from
each one-update check and is covered by a regression test. Suite: 19/19 PASS.

## 9. Full submission after retained gates passed

- Job: `pt-b32i9y4r`; display name `a15-13-e20-sae-flat-five-arm-20260908T012237Z`.
- Created: `2026-09-08T01:22:38Z`; scheduler start: `2026-09-08T01:22:49Z`.
- Verified scheduler state at 01:23 UTC: `RUNNING`, one worker replica.
- Resources: `share-space`, `share-cluster`, `n6ls.iu.i40.4`, 4 H100 GPUs,
  reserved quota, normal priority, retries 0, external wall ceiling 12 hours.
- Command: `timeout --signal=TERM 12h bash /data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/formal_run.sh /data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z`.
- Qualification receipt: `qualification/receipt.json`, status PASS, nine
  authenticated Routers, five passed smokes, 15-condition formal matrix.
- Every smoke used 7,032 answer tokens; frozen base checks passed. Initial
  one-update loss was identical across conditions (zero-initialized adapters),
  0.864446278725061 nats/token. This is not a functional comparison result.
- Submission evidence: `submit-20260908T012237Z.txt` and
  `submission.receipt.json` in the run root. The latter authenticates the
  qualification and submitted implementation.
- Runtime logs: `logs/formal-tests.log`, `logs/formal-workers.log`; training
  progress: `conditions/<arm>__seed<seed>/progress.json`.

Scheduler RUNNING is not yet a claim that any optimizer step has completed.
No update-512, generation score, paired primary contrast, or scientific verdict
is available at this snapshot. The earliest submission objective is met; startup
and bounded supervision continue without changing the registered experiment.

### Launcher failure and exact-input resubmission

The first job `pt-b32i9y4r` passed 19 remote tests, then failed before creating
any condition artifact: `torchrun` parsed the pipeline's `--run` as an ambiguous
abbreviation for its own `--run-path`. The actual launcher arguments reproduce
the failure in a regression test. Adding `--` before the training script fixes
the parsing; the expanded local suite passes 20/20. This is an engineering-only
launch correction, not a new training condition or scientific amendment.

The failed job reached platform state FAILED before resubmission. Its logs,
original submission receipt, and intent record were moved intact under
`interruptions/pt-b32i9y4r-launcher-failure/`; the failure receipt records zero
optimizer steps and the corrected launcher hash. Data, groups, nine Routers,
smokes, and qualification receipt were not modified or refitted.

Replacement job: `pt-zkpfj2zm`, created `2026-09-08T01:25:04Z`, scheduler start
`2026-09-08T01:25:13Z`, verified RUNNING. It uses the identical resource tuple,
matrix, and command entry point with the corrected launcher. Current
`submission.receipt.json` identifies the replacement and its predecessor.

### Confirmed optimizer progress

At `2026-09-08T01:29:43Z`, job `pt-zkpfj2zm` was RUNNING and the first four
assigned conditions had completed actual optimizer updates:

| Condition | Update / 512 | Latest minibatch NLL | Gradient norm | Recovery checkpoint |
|---|---:|---:|---:|---|
| SAE seed 17 | 107 | 0.816117 | 0.040320 | present |
| SAE seed 29 | 108 | 0.842922 | 0.032665 | present |
| SAE seed 43 | 106 | 0.817094 | 0.029809 | present |
| Random features seed 17 | 106 | 0.729911 | 0.036274 | present |

Source: `conditions/<condition>/progress.json`, frozen into
`startup.receipt.json` at the run root, plus the job status query. These are
non-paired minibatch progress values, not held-out scientific comparisons.
The replacement container passed 20/20 tests with one nonfatal PyTorch warning
from a test scalar conversion. No runtime error was present in its worker log.
Final update-512 checkpoints: 0/15 at this snapshot. Remaining conditions and
registered evaluations will run through the unchanged four-worker matrix.
The submission and actual-start objective is complete; the ACP job continues
independently. Completed experiment results and scientific judgment remain
pending, with the internal-held-out claim boundary unchanged.

## 10. Evaluation failure and partial training evidence

Live query at `2026-09-08T02:13:21Z`: ACP job `pt-zkpfj2zm` is FAILED.
Worker log records the first error at `2026-09-08T01:39:31Z`: `train.py:283`
calls `torch.flatnonzero(valid[:, position])`, but PyTorch has no such API.
This is an implementation error in expert-selection intervention, not a
scientific qualification failure or observed lack of SAE utility. Other ranks
were terminated by the shared launcher after one rank failed.

The worker sequence is training -> test/intervention -> generation -> next
condition. Therefore this evaluation error prevents the other eleven conditions
from starting. There are four completed `training.json` records and four
`final.pt` checkpoints, but zero complete test manifests, zero generation
metric files, and no completion receipt. Checkpoint hashes match each training
record; base-freeze checks passed and all four histories contain 512 updates.

| Condition | Development loss at 0 | 128 | 256 | 384 | 512 |
|---|---:|---:|---:|---:|---:|
| SAE seed 17 | 0.869630 | 0.765033 | 0.750439 | 0.746127 | 0.745375 |
| SAE seed 29 | 0.869630 | 0.764162 | 0.749992 | 0.745856 | 0.745225 |
| SAE seed 43 | 0.869630 | 0.763386 | 0.748434 | 0.743702 | 0.743032 |
| Random features seed 17 | 0.869630 | 0.768912 | 0.753443 | 0.749206 | 0.748540 |

Lineage: `conditions/<condition>/training.json` -> `validation_curve` -> full
development answer-token loss in nats/token, aggregated by total answer tokens.
The only same-seed completed control pair is seed 17: random minus SAE equals
`0.7485398650169373 - 0.745375394821167 = 0.0031644701957702637` nats/token.
No uncertainty interval is claimed for these aggregate development values.
All four curves decrease, which establishes that these runs optimized the
development loss; it does not adjudicate the registered held-out criterion.
Training-loop elapsed times were approximately 610-615 seconds, excluding
subsequent evaluation and generation.

E20-A3 cancels the three sets of six outstanding grouping repetitions (18
total). Existing diagnostics and frozen identities remain intact; no files were
deleted. Primary confidence intervals, controls, and intervention remain in scope.

AI recommendation, not an executed repair: replace the invalid nonzero-index
operation with its supported equivalent and test the actual intervention path;
record an evaluation-only code-change receipt permitting exact checkpoint reuse;
preserve incomplete evaluation artifacts, then rerun missing evaluations and
continue the remaining eleven conditions. The evaluator currently compares a
full source identity against checkpoint identity, so silently editing code and
relaunching would also cause an identity mismatch. No new job was submitted in
this turn. Final scientific interpretation remains unknown.

## 11. E20-A4 repaired continuation

Researcher authorization: repair, test, preserve four completed checkpoints,
continue missing evaluation and eleven training conditions, inspect every ten
minutes quietly, and report after completion.

- Invalid `torch.flatnonzero` calls in intervention and source-wise generation
  are replaced by `torch.nonzero(..., as_tuple=True)[0]`.
- The actual SAE/GMM intervention evaluator and eight-source generation path
  are covered by regression tests. Permutation masks, per-position counts,
  deterministic replay, and exact old/new checkpoint comparison are covered.
- Identity drift is not generally permitted: only the exact four registered
  checkpoint hashes and repaired implementation can use the E20-A4 bridge.
  Manifests preserve original checkpoint training identity separately from
  current evaluation identity. Twenty-six unchanged-source/function checks
  verify that training/optimizer/model behavior was not changed.
- The auxiliary in-memory Router cache now detects atomic replacement by inode;
  no existing cache was modified and no offline Router was refitted.
- Local regression suite: 28/28 PASS. Real-model engineering probe: eight
  records, one per source, passed intervention and generation. Probe outputs
  under `repair_smoke/` are explicitly ineligible as formal results.
- All four checkpoint hashes were checked before repair and before submission;
  originals remain untouched in `conditions/`.
- Failed job logs and incomplete evaluation directories were moved intact to
  `interruptions/pt-zkpfj2zm-intervention-failure/` before continuation.
- Repair receipt: `amendments/E20-A4-EVALUATION-REPAIR/receipt.json`, SHA256
  `df70313a98298cba672decc9db74734e506190657a3db9d99bd9c15844f9ca12`.
- Replacement job: `pt-os72i446`, created `2026-09-08T02:26:32Z`; queried at
  `2026-09-08T02:27:13Z` as STARTING. Resources remain one-node 4xH100 reserved,
  no automatic job retry, twelve-hour execution ceiling.
- Supervision: `local_checks/monitor_10min.py`, read-only checks every 600
  seconds; snapshots under `monitoring/pt-os72i446/`. Checks platform state,
  optimizer progress, artifact counts and preservation of four checkpoints;
  terminal events require complete evidence or a recorded failure. It never
  submits or stops a job.

No complete test/generation verdict is available yet. E20-A3's 18 cancelled
grouping repetitions are not reinstated by this repair or supervisor.
