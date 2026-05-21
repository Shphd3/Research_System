# Current Research Mainline

Last updated: 2026-05-21

## Active Project

Primary project:

```text
Projects/from-attention-to-search/
Branch: Xingyu
Working context: Projects/from-attention-to-search/XingyuD/main/
```

Root `CURRENT.md` is only a compatibility pointer. Canonical state lives in:

```text
Projects/from-attention-to-search/main/current_mainline.md
Projects/from-attention-to-search/XingyuD/main/current_mainline.md
```

## One-Sentence Mainline

We are reframing long-context attention as search over dynamic KV memory, but
the current bottleneck is mechanism diagnosis: ordinary top-1 MoE may route
mixed token/context bundles rather than clean latent features.

## Core Question

```text
query token -> learned index / routing signal -> candidate KV tokens -> exact sparse attention
```

This now splits into two questions:

1. Can expert routing form functional feature specialization?
2. If yes, does that specialization help Reverse Index candidate generation?

Reverse Index means using a query-side bucket or learned index signal to retrieve
historical KV candidates before exact sparse attention.

## Current Evidence

Supported:

- dense attention is selective, so retrieval framing is meaningful;
- early flat / H-MoE / spectral router buckets were not sufficient KV indexes;
- E4 shows feature-aligned routing can be constructed, but natural NTP routing
  does not reliably learn clean one-feature-one-expert structure;
- R0/R1 shows same-bucket KV can beat random same-count KV in corrected
  post-attention RI;
- high feature-expert NMI is not enough to prove functional specialization or
  good retrieval.

## Active Hypothesis

```text
H0521_ab_feature_specialization
```

Question:

```text
在最小 AB synthetic setup 中，ordinary top-1 MoE routing 能否把 composite feature AB 从 atomic feature A/B 中分离出来？
```

Most important metric:

```text
class-specific expert ablation delta loss
```

It matters because assignment metrics show where samples go, while ablation
delta loss shows what each expert functionally supports.

## Roadmap

```text
Gate 1: AB feature-specialization diagnosis
Gate 2: specialization -> Reverse Index alignment
Gate 3: candidate generator tournament
Gate 4: train/infer mismatch
Gate 5: real representation transfer
```

## Claim Boundary

We can claim:

- attention-as-search remains a meaningful framing;
- expert buckets can contain retrieval signal above random;
- one-feature-one-expert is not sufficient for good Reverse Index;
- the next step is top-1 MoE mechanism diagnosis, not router architecture
  optimization.

We cannot claim:

- MoE routing is generally useless;
- top-1 MoE necessarily fails in all settings;
- top-k / soft routing will solve the issue;
- current same-bucket RI is enough to replace dense attention;
- any real-language transfer or speedup.

## Next Decision

Write and run:

```text
experiments/H0521_ab_feature_specialization/execution_plan.md
```

First run:

```text
dense baseline
top-1 MoE no-load-balance
routing assignment diagnostics
class-specific expert ablation
```
