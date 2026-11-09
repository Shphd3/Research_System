---
experiment_id: A15_02_01_E01_controlled_layer_information_profile
anchor_id: 15_02_01_controlled_layer_information_identity
status: completed_pass
verdict: pass_with_negative_composite_band_result
completed: 2026-07-31
---

# Complete Evidence Ledger

## 0. Registered Decision

The experiment asks whether the same relative covariance band carries different registered functional variables at different depths of a capability-valid four-layer MoE. A Pass requires all four models to pass capability and validity gates and at least one layer-band-variable cell to beat equal-rank random directions with a composition-over-control increment in both seeds.

The typed terminal audit returned `pass`, with 1,152 profile rows, 176 Gate-ablation rows, stable trained bases, and six replicated rows. Because H equals F1, these six rows represent four distinct layer-band-variable findings.

## 1. Dataset Contract

The finite-field mechanism is

\[
m=(x+a)\bmod17,\qquad y=(m+b)\bmod17.
\]

Eight shared shift tokens yield an \(8\times8\) \((a,b)\) grid. Final-query training excludes an eight-pair perfect matching while retaining every atom in the remaining seven partners. Mid-query examples cover all pairs. The registered context splits are mutually disjoint: train 0--15, validation 16--19, covariance calibration 20--23, probe fit 24--25, probe validation 26--27, and sealed test 28--31.

Dataset payload SHA-256 is `94cdfb3328a23017dc3da4371153858e94ef5942e22ff04f2d1a608a0032b7d1`; NPZ SHA-256 is `0b466fe2362919a8e900ab574510457da9f3604869b3d9eb48b252fa4d12e7ec`. All leakage, atom-coverage, answer-balance, oracle, shuffle, and additive-shortcut guards passed. The additive shortcut achieved 0.000 on composition and 0.118 on control, both below the registered 0.20 ceiling.

## 2. Model And Training Contract

Each model is a four-layer pre-norm causal Transformer-MoE with width 256, eight attention heads, eight top-1 experts per layer, and expert width 512. The Gate receives the actual MoE-normalized state. The selected softmax probability multiplies the chosen expert output, preserving the Gate learning path. There is no load-balancing auxiliary loss or capacity drop. A shared non-gradient load-free score bias uses learning rate 0.003 and clip 4.0.

The one-step control predicts \(m\) at the final query; the composition model predicts \(y\). Both also receive an equal-weight layer-2 training-only head predicting \(m\). Conditions share paired initialization, data order, and optimizer within each seed. Formal seeds are 17 and 29. The selected schedule was the first preflight candidate: at most 2,000 steps, learning rate \(10^{-3}\), AdamW betas (0.9, 0.95), weight decay 0.01, 100-step warmup, cosine decay, global batch 512, and gradient clipping at 1.0.

Config SHA-256 is `3eb530a1a99db5b561f50b1b96c455f5142c7771d31f07085176166bac19fb86`.

## 3. Execution And Attempt Ledger

All ACP runs used one node with eight 5090 GPUs, SPOT quota, workspace `share-space`, AEC2 `computing-cluster-5090-01g`, and spec `n12lp.nn.i10a.8`.

| Attempt | Job | Outcome | Scientific use |
| --- | --- | --- | --- |
| Original bias smoke | `om-liqwksqo` | Engineering success | Superseded after validation showed the old bias setting saturated |
| Amended-bias smoke | `om-8x6b91rj` | Engineering success | Validated the 0.003/4.0 bias setting |
| First no-aux full | `om-rlthshjv` | Stopped before sealed test | `insufficient_composition_capability`; retained as negative provenance |
| Intermediate-head smoke | `om-j9yvkcua` | Success, zero retries | Validated the capability amendment and full analyzer interface |
| Formal training/full analysis | `om-xwaiwu08` | Training complete; analyzer device mismatch caused terminal platform failure after one retry | Four valid checkpoints retained; no result was read from a mismatched computation |
| Analysis-only recovery | `om-2cy156ju` | Success | Recomputed the complete sealed analysis from frozen checkpoints after the GPU-device fix |

The analyzer defect allocated the ridge intercept and identity matrix on CPU while features were on GPU. The fix moved both to the feature device and added a GPU regression test. It did not change checkpoints, data, metrics, random controls, or thresholds.

## 4. Capability And Validity Evidence

The sealed capability table is [tables/capability.csv](tables/capability.csv).

| Condition | Seed | Selected step | Mid accuracy | Final unseen accuracy | Final unseen NLL | Recent max expert share | All experts used |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| One-step control | 17 | 1,100 | 1.000 | 1.000 | \(1.88\times10^{-8}\) | 0.568 | Yes |
| One-step control | 29 | 1,200 | 1.000 | 1.000 | \(3.73\times10^{-9}\) | 0.441 | Yes |
| Composition | 17 | 1,000 | 1.000 | 1.000 | \(2.85\times10^{-4}\) | 0.464 | Yes |
| Composition | 29 | 500 | 1.000 | 0.985 | 0.0279 | 0.515 | Yes |

Actual Gate-input replay error was exactly zero. Every selected checkpoint used all experts, remained below the registered 0.65 load ceiling, and kept the non-gradient bias below the clip.

## 5. Spectral Basis Audit

For each layer and model, the covariance basis was fitted only on the calibration split. Width 256 was divided into F1--F8 of rank 32; H=F1, M=F2--F4, and T=F5--F8. Every trained band passed its split-half stability guard.

Across all trained models/layers, minimum split-half overlaps were 0.997 for F1/H, 0.966 for F2, 0.951 for M, and 0.964 for T. Their matched random q95 values were approximately 0.13, 0.13, 0.38, and 0.50. H carried 90.2%--98.1% of centered energy; F2 carried 1.27%--7.13%; T carried \(7\times10^{-6}\)--0.71%. See [tables/basis_stability.csv](tables/basis_stability.csv).

## 6. Full-State Layer Profile

The primary low-sample readability value is the mean sealed-test accuracy across ridge probes fitted with 32, 64, 128, and 256 examples. Full-state means across the two seeds are in [tables/key_full_state_profile.csv](tables/key_full_state_profile.csv).

Under both objectives, coarse \(a\) is easiest at layer 1 and declines with depth; intermediate \(m\) rises sharply by layer 2 and is nearly complete by layer 3. Only the composition objective makes \(y\) readable: 0.113, 0.160, 0.427, and 0.784 over layers 1--4, versus 0.103, 0.136, 0.156, and 0.140 in the one-step control.

This establishes a capability-valid layerwise computation profile. It does not establish spontaneous emergence because the layer-2 \(m\) head is registered training supervision.

## 7. Band Specificity And Objective Contrast

For each real band, 64 equal-rank Haar-random subspaces provide a random-direction q95. Pair-level bootstrap intervals use 2,000 paired resamples. A cell is specific only if its real band beats q95 and its interval supports a positive difference. Composition specificity must also exceed the matched one-step control in both seeds.

The four distinct replicated results are listed in [tables/key_replicated_band_cells.csv](tables/key_replicated_band_cells.csv):

- L3-F1/head intermediate \(m\): mean \(\Gamma=+0.031\);
- L3-F2 coarse \(a\): mean \(\Gamma=+0.370\);
- L4-F1/head intermediate \(m\): mean \(\Gamma=+0.103\);
- L4-F2 coarse \(a\): mean \(\Gamma=+0.577\).

None passed at initialization. No composite-\(y\) cell passed in either coarse or fine resolution. At L4, for example, composition-model \(y\) AULC was 0.706 in H on average, but equal-rank random q95 averaged 0.750; M and T were even less specific. Thus strong full-state composition readability cannot be localized to a fixed covariance rank.

## 8. Native Gate-Use Audit

The audit removes one band's contribution from Gate logits while keeping expert inputs native. It measures answer-NLL change, route flip, and native-winner margin change. Equal-rank random subspaces supply q95 controls.

F1/head was causally used by the current Router: across composition models, mean route flips by layer were 0.377, 0.724, 0.718, and 0.743, with mean NLL increases 0.423, 1.177, 0.780, and 0.373. Both seeds exceeded random controls.

F2, M, and T did not pass this use criterion in both seeds. Their mean route flips were at most 1.47% and NLL changes were approximately zero. See [tables/key_gate_use.csv](tables/key_gate_use.csv) and the full [tables/gate_band_ablation.csv](tables/gate_band_ablation.csv).

The result separates two objects: F2 is a trained, reproducible coordinate for coarse \(a\) in deeper composition layers, but the native Gate does not rely on it. Readability is not use, and use is not training benefit.

## 9. Verdict Against Hypotheses And Rivals

- **H1 passes in its registered broad form:** composition induces replicated layer-band identity beyond random directions and the one-step control.
- **The monotonic rank-depth interpretation fails:** composed \(y\) is not specifically localized in deeper middle or tail.
- **R0 is rejected for the four passing cells:** they beat strong equal-rank random controls under low-sample evaluation.
- **R1 is rejected for full-state \(y\) formation:** the one-step control does not show the deep \(y\) rise. It remains a guard against interpreting supervised \(m\) as spontaneous emergence.
- **R2 is rejected operationally:** both composition seeds solve held-out \((a,b)\) recombinations, with no held-out answer token in training.

## 10. Figure Contract And Visual Audit

The central figure is [figures/final_knowledge_update.png](figures/final_knowledge_update.png).

- **Question:** Does layerwise computation create a reproducible layer-band information identity?
- **Metric/unit:** full-state low-sample AULC accuracy and composition-over-control specificity difference \(\Gamma\), both in accuracy points.
- **Source:** `spectral_profile.csv` and `gamma_composition_vs_control.csv`, averaged across seeds 17 and 29.
- **Aggregation:** full-state lines average two seeds; heatmap cells average two seed-level contrasts; stars require both seeds to pass the registered controls.
- **Allowed conclusion:** full-state composed information forms with depth; F1 and F2 acquire replicated intermediate/coarse identities at L3--L4.
- **Limitation:** absence of a star is not absence of information; it means no registered specificity beyond equal-rank random directions in both seeds. The figure does not show routing benefit.

The rendered figure was inspected at original resolution. Labels, legends, star semantics, and numerical annotations are legible. The broader H/M/T diagnostic heatmap is retained as [figures/layer_band_information_heatmap.png](figures/layer_band_information_heatmap.png), but it is not the primary inference path because coarse aggregation can hide the F2 effect.

## 11. Claim Boundary

Established:

1. the controlled dataset and four-layer MoE are capability-valid in two seeds per condition;
2. full-state functional content changes with depth;
3. fixed covariance rank has no invariant cross-layer meaning;
4. composition induces replicated F1-intermediate and F2-coarse specificity at L3--L4;
5. the composed result is not specifically localized to a fixed H/M/T or fine band;
6. native Gates remain dominated by F1/head even when F2 contains reproducible information.

Not established:

- natural-language semantic hierarchy;
- spontaneous intermediate-state formation without auxiliary supervision;
- cross-layer compatibility, expert specialization, or NLL/FLOP benefit;
- a deployable Router that avoids repeated eigendecomposition;
- that F2 should directly route a deeper expert.

## 12. Exactly One Next Decision

Decide whether to learn fixed layer-specific low-rank readouts for the replicated functional coordinates and submit them to the independent one-step compatibility gate. Only a readout that beats native-score, equal-dimensional random, token-shuffled, and wrong-layer controls should unlock matched cross-layer routing training.

## 13. Artifact Map

Curated project-local artifacts:

- [protocol.md](protocol.md) and [protocol_cn.md](protocol_cn.md)
- [summary.md](summary.md) and [summary_cn.md](summary_cn.md)
- [tables/capability.csv](tables/capability.csv)
- [tables/spectral_profile.csv](tables/spectral_profile.csv)
- [tables/gamma_composition_vs_control.csv](tables/gamma_composition_vs_control.csv)
- [tables/basis_stability.csv](tables/basis_stability.csv)
- [tables/gate_band_ablation.csv](tables/gate_band_ablation.csv)
- [figures/final_knowledge_update.png](figures/final_knowledge_update.png)

Worker evidence, checkpoints, manifests, unit-test logs, and the terminal audit remain under:

`Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_01_02_layer_band_information_profile/`

No raw checkpoints, caches, or cluster logs were promoted into the research mainline.
