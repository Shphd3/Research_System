# Detailed Result: R4 Attention-Output Router Retrieval

## Run Records

Initial submit:

- `pt-f6qb97t6`: failed before training.
- `pt-ozignh9p`: failed before training.
- Cause: submit-script heredoc kept `${RUN_NAME}` unexpanded inside the ACP command, so the container hit an unset variable before child runs started.

Successful retry:

| Data | ACP job | State | Start | Complete | Child runs |
|---|---|---:|---:|---:|---:|
| uniform | `pt-hmaan5mc` | SUCCEEDED | 2026-05-18 07:07:07 UTC | 07:10:20 UTC | 4 |
| longtail | `pt-inv9rx4o` | SUCCEEDED | 2026-05-18 07:09:31 UTC | 07:12:32 UTC | 4 |

Each successful job used one 4-GPU worker and launched:

```text
GPU0: attn_route_ntp_only, seed 20260522
GPU1: attn_route_ntp_only, seed 20260523
GPU2: attn_route_router_ce, seed 20260522
GPU3: attn_route_router_ce, seed 20260523
```

## Metrics

Training and alignment:

| Data | Variant | Best valid CE | Final valid CE | Feature prob | Feature acc | Router NMI |
|---|---:|---:|---:|---:|---:|---:|
| uniform | NTP only | 6.631 | 6.735 | 0.999 | 1.000 | 0.720 |
| uniform | NTP + RouterFeatureCE | 6.629 | 6.718 | 0.994 | 1.000 | 1.000 |
| longtail | NTP only | 6.685 | 6.780 | 0.961 | 1.000 | 0.187 |
| longtail | NTP + RouterFeatureCE | 6.683 | 6.765 | 0.982 | 1.000 | 1.000 |

Feature-query retrieval, router cumulative top-K:

| Data | Variant | K | Recall | Mass | L2 | CE delta | Candidate KV |
|---|---|---:|---:|---:|---:|---:|---:|
| uniform | NTP only | 1 | 0.273 | 0.390 | 1.161 | 0.701 | 7.6 |
| uniform | NTP only | 2 | 0.526 | 0.643 | 0.663 | 0.425 | 15.8 |
| uniform | NTP only | 4 | 1.000 | 1.000 | 0.000 | -0.000 | 32.0 |
| uniform | NTP + RouterFeatureCE | 1 | 0.308 | 0.380 | 1.100 | 2.311 | 8.8 |
| uniform | NTP + RouterFeatureCE | 2 | 0.604 | 0.738 | 0.530 | 0.808 | 18.6 |
| uniform | NTP + RouterFeatureCE | 4 | 1.000 | 1.000 | 0.000 | 0.005 | 32.0 |
| longtail | NTP only | 1 | 0.187 | 0.286 | 1.242 | 0.301 | 4.2 |
| longtail | NTP only | 2 | 0.454 | 0.518 | 0.838 | 0.434 | 13.8 |
| longtail | NTP only | 4 | 1.000 | 1.000 | 0.000 | -0.001 | 32.0 |
| longtail | NTP + RouterFeatureCE | 1 | 0.324 | 0.453 | 1.125 | 2.868 | 8.7 |
| longtail | NTP + RouterFeatureCE | 2 | 0.485 | 0.575 | 0.926 | 2.644 | 14.1 |
| longtail | NTP + RouterFeatureCE | 4 | 1.000 | 1.000 | 0.000 | -0.001 | 32.0 |

K=4 是 full-prefix sanity，因为本轮只有 4 buckets 且 `seq_len=32`，top-4 buckets 覆盖全部 prefix KV。

Baseline at K=1 same-count:

| Data | Baseline | Recall | L2 | CE delta |
|---|---|---:|---:|---:|
| uniform | random | 0.256 | 1.182 | 1.259 |
| uniform | local | 0.366 | 0.610 | 0.124 |
| uniform | oracle | 0.435 | 0.374 | 0.001 |
| longtail | random | 0.202 | 1.210 | 1.059 |
| longtail | local | 0.291 | 0.724 | 0.069 |
| longtail | oracle | 0.368 | 0.445 | -0.000 |

The CSV tables are:

```text
r4_run_summary.csv
r4_feature_query_retrieval_summary.csv
r4_dense_sparsity_summary.csv
```

## Figures

- `figures/r4_uniform_topk_retrieval_quality.png`: uniform feature-query retrieval quality.
- `figures/r4_longtail_topk_retrieval_quality.png`: longtail feature-query retrieval quality.
- `figures/r4_training_readback_alignment.png`: training CE, feature readback, and router-feature NMI.

## Failure Analysis

R4 did not produce a useful reverse index.

Most likely explanation:

```text
feature identity is learnable and route-alignable,
but block2 attention in this NTP setup is not primarily selecting KV by feature identity.
```

Evidence:

- RouterFeatureCE gives perfect feature-router NMI but worsens sparse CE at low K.
- Local same-count has much smaller CE delta despite weaker dense top-16 recall.
- Oracle same-count has near-zero CE delta, so the evaluation path itself can preserve output quality when candidates match dense attention.

This separates three notions:

```text
feature readback works != router specialization works != KV reverse index works
```
