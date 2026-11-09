# Summary: A15_13_E16 DCLM final-layer Top-K SAE

Primary Anchor: [A15_13_06](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_06_dclm_final_layer_topk_sae_teacher_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md)  
Detailed evidence: [detailed.md](detailed.md)  
Result status: `FULL_RUN_COMPLETE`; knowledge wording: `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`  
Registered typed verdict: `PASS`

## Result Snapshot

ACP job `pt-2lw02d0a` completed successfully with zero reported retries. The fresh seed-17 SAE consumed exactly `1,000,001,536` raw DCLM tokens in `244,141` optimizer updates on one reserved four-H100 node. All eleven registered full-run gates passed.

Held-out normalized reconstruction mean squared error fell from `0.7890049927` before training to `0.0604918830` at about 100M tokens, `0.0575391222` at about 300M tokens, and `0.0533820926` at 1B tokens. Zero reconstruction is `1.0`, so the final dictionary reconstructs the registered final-layer state nontrivially. All 30,000 features fired at least once over training, each held-out token retained 32 positive features, the base model had zero trainable parameters, and reloading the final checkpoint reproduced the original output with maximum absolute difference `0.0`.

This establishes a technically qualified final-layer SAE checkpoint. It does **not** establish that the features are semantic, that activation-containment edges form a valid hierarchy, that hierarchy depth means coarse or fine domain, that earlier layers can recover the teacher, or that a Router/LoRA expert gains language-model utility.

## Decision-Bearing Setup

The run was one continuous training stage, not staged training. Qwen3-0.6B-Base was frozen; only the 30,000-feature ReLU Top-32 SAE at the zero-based layer-27 MLP pre-hook was trainable. Four synchronized processes each read one 1,024-token DCLM window per update, for 4,096 raw tokens per optimizer update. AdamW used learning rate `3e-4`, zero weight decay, ten-step warmup, gradient clipping at `1.0`, and no result-based early stopping or checkpoint selection.

## Verdict Basis

| Registered rule | Observed value | Verdict |
| --- | ---: | --- |
| Exact full budget | `1,000,001,536` tokens; `244,141` updates | Pass |
| Complete frozen data manifest | 2,419 files; `302,089,493,820` source tokens | Pass |
| All fixed milestones retained | steps `24,415`, `73,243`, `244,141` | Pass |
| Final validation finite and better than initialization and zero | `0.0533820926 < 0.7890049927 < 1.0` | Pass |
| Sparse support non-collapsed | 30,000/30,000 features used; Top-32 positive count `32.0` | Pass |
| Frozen base and exact reload | zero trainable base parameters; reload difference `0.0` | Pass |
| Platform completion | ACP `SUCCEEDED` at `2026-09-03 18:03:14 UTC` | Pass |

The primary source is the worker-side [`full_summary.json`](/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/full_summary.json). The final checkpoint SHA-256 is `e4e2049aced8ba9a3b043bbb2b3308b497b7ec22f107531e37197873ee545b65`.

## Claim Boundary

Can claim: the fixed final-layer SAE training contract completed and produced a finite, non-collapsed, exactly reloadable dictionary that reconstructs held-out DCLM states substantially better than initialization and zero output.

Cannot claim: semantic meaning, valid parent-child feature relations, coarse/fine labels, layer placement, online Router recovery, expert utility, task gain, or seed stability.

## One Next Decision

Decide whether to confirm a single gated follow-up experiment: first qualify an unsupervised final-layer feature hierarchy on disjoint DCLM discovery/replication samples; only if that gate passes, freeze its teacher assignments and measure their layerwise recoverability on the exact current-token MLP-input states. No Router or LoRA training is included.
