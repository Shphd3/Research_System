# Protocol: A15_13_E12 M2D2 Coarse-Removal And Parent-Freeze Ablation

## 0. Approval Snapshot

```text
Document status: APPROVED_FOR_FULL_RUN
Approval status: HUMAN_APPROVED_2026-09-02
Block audit status: A-G CONFIRMED
Cross-block consistency: PASS
Execution scope approved: IMPLEMENTATION, FULL TRAINING, EVALUATION, ANALYSIS, CURATED RESULT WRITING
Primary metric: equal-domain confirmation NLL after stage two
Seeds: 17 and 29
Resource: reserved four-H100 ACP job; no fallback
```

## 1. Purpose

Test whether fine routing fails because it rereads coarse/common information, because freezing the coarse experts prevents useful adaptation, or because neither implementation choice is causal.

## 2. Hypotheses And Rival

The first hypothesis is that subtracting the coarse Router row-space from the child Router input improves fine semantic dispatch without damaging next-token likelihood. The second is that allowing parent experts to continue updating during stage two improves likelihood. The strongest rival is that either change merely perturbs optimization or load and does not reproduce the hard-Oracle functional value.

## 3. Data And Task

Reuse the frozen M2D2-Wikipedia balanced three-by-three tensors: 9,216 training, 2,304 development, and 4,608 confirmation windows. Each window has 256 tokens; tokens 0--63 supply context and the 192 predictions for tokens 64--255 contribute standard next-token cross entropy. Domain names never enter the text. Development labels may tune no scientific threshold; confirmation labels are used only for semantic and paired subgroup audit.

## 4. Architecture And Exact Ablation

Freeze Qwen3-0.6B-Base and its language head. At zero-index block 14 MLP `down_proj`, insert rank-eight shared, three parent, and nine child LoRA banks plus causal token Routers.

Stage one trains the shared LoRA, parent experts, and parent Router for two full data passes. Stage two trains child experts and child Router for two additional passes. Cross two binary choices in stage two:

1. `native` versus `coarse_removed` child-Router input. `coarse_removed` centers the three parent-Router weight rows, obtains their nonzero orthonormal row-space by singular-value decomposition, projects each causal token state onto that coarse subspace, and subtracts the projection. The parent Router and all experts still receive the native state.
2. `freeze_parent` versus `update_parent`. The former freezes the parent Router and parent experts in stage two. The latter freezes the parent Router but keeps parent experts trainable. This isolates expert plasticity from route drift.

Run the full two-by-two matrix under correct hierarchical semantic supervision. Add the architecture-identical task-only and frequency-matched shuffled-label checkpoints as fixed references; do not reinterpret them as members of the two-by-two causal matrix.

## 5. Optimization And Smooth-Loss Contract

Use seeds 17 and 29, microbatch 8 per GPU condition, accumulation 16, AdamW, learning rate \(3\times10^{-4}\), weight decay 0.01, gradient norm clip 1.0, and a single 288-update schedule over four passes. The first five global updates warm up and cosine decay then continues across the stage boundary. Stage two consumes the next deterministic epoch orders rather than replaying stage-one orders. Save updates 0, 15, 29, 58, 116, 173, 230, and 288.

At every saved update evaluate the same equal-domain development subset. Raw training cross entropy remains diagnostic; fixed-development NLL versus seen target tokens is the learning-efficiency curve. Plots may overlay a three-point moving mean but must retain raw markers and never use the smoothed value for a verdict.

## 6. Analysis

Compare the four conditions using equal-domain confirmation NLL, development loss-curve area, fine route-label normalized mutual information, load entropy, and matched child deletion/substitution NLL. The two-by-two factorial contrasts estimate the average effect of coarse removal, parent-expert updating, and their interaction. Paired 2,000-replicate within-domain bootstrap intervals are required. A positive semantic metric without NLL or functional intervention improvement cannot establish useful semantic processing.

## 7. Guards And Completion

Unit tests must prove exact coarse-subspace removal, unchanged parent-Router input, trainable-parameter masks for all four cells, causal future invariance, continuous data order/schedule, and zero checkpoint mutation during evaluation. Completion requires both seeds, all four cells, every scheduled development evaluation, confirmation arrays, interventions, representation/routing arrays, hashes, and a completion audit.

The result may establish only a controlled M2D2 implementation effect. It cannot establish open-domain gain, base-representation reshaping, or deployment value.
