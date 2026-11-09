# A15.13 E15 Protocol — Gold-label layerwise static audit

```text
status: APPROVED_EXECUTION_CONTRACT
problem_key: A15.gold_label_layerwise_static_audit
approval_source: codex-thread:01a0679c-7ee2-71f3-91b5-f4df234571db
approval_date: 2026-09-03
approval_scope: revised method set, implementation, smoke test, full run, figures, summary, and detailed evidence on one H100 SPOT GPU
not_authorized: SAE training; LoRA or expert training; causal activation intervention; graph edit; root sync; commit; push
```

## A. Decision Question And Claim Boundary

In frozen Qwen3-0.6B-Base, at which Transformer blocks do real M2D2 parent labels and real within-parent child labels first become stably readable from the exact current-token tensor that a future LoRA Router would receive?

This experiment directly measures representation readability and the ease, geometry, and robustness of a newly trained readout. It does not establish native causal use, online Router success, LoRA expert function, or next-token gain. Those require a separately approved Oracle LoRA intervention.

## B. Frozen Objects

| Object | Frozen identity |
|---|---|
| Model | `/data/250010109/model_cache/Qwen3-0.6B-Base-official` |
| Hugging Face revision | `da87bfb608c14b7cf20ba1ce41287e8de496c0cd` |
| `model.safetensors` SHA-256 | `cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba` |
| `config.json` SHA-256 | `504a6b58c4271583724e66584b6b7698aea18450209df6b2f7582df0e89cee59` |
| Structure | 28 blocks; hidden width 1,024 |
| Data | `/data/250010109/datasets/m2d2_wikipedia_3x3/processed/m2d2_3x3_seq256.pt` |
| Data SHA-256 | `8cd04d99ad2576d8a149dc145c83b29d5a977178419304c4490cf8e10cba51a8` |
| Cells | 3 parent domains × 3 local child domains |
| Windows per child | train 1,024; development 256; confirmation 512 |
| Positions | representation positions 63–254, predicting targets 64–255 |

Any mismatch is a hard stop. Domain names are never added to inputs. Existing window splits are immutable; tokens from one window never enter different data branches.

## C. One Representation Object

For zero-indexed block \(\ell\in\{0,\ldots,27\}\) and current prediction position \(t\), define

\[
z_{\ell,t}=\text{the first input tensor observed by a forward pre-hook on }\texttt{decoder\_layer.mlp}.
\]

The expected batch tensor is `[batch, 256, 1024]`; only positions 63–254 are audited. This is the post-attention-normalization tensor that the future Router is intended to read. No block output, layer-before state, residual update, prefix average, whole-window average, cross-layer centroid, or projected-away coarse direction is an experimental input.

## D. Tasks And Probe Families

### D1. Gold tasks

1. **Parent readout:** one 1,024-to-3 affine classifier per layer.
2. **Conditional child readout:** three separate 1,024-to-3 affine classifiers per layer, selected by the true parent and predicting the three local children. Every head reads the complete vector.

Gold labels are measurement rulers only; deployment is not given gold labels.

### D2. Linear primary readout

The primary selector is the affine readout above. All 28 layers use identical initialization distribution, optimizer, data order, updates, and parameter count per classifier.

### D3. Fixed nonlinear ceiling

For every layer and task, train a two-layer probe `1024 → 32 → 3` with GELU activation. Conditional child probes remain parent-specific. The nonlinear gap is

\[
\Delta^{\mathrm{NL}}_\ell=\mathrm{CE}^{\mathrm{linear}}_\ell-\mathrm{CE}^{\mathrm{MLP}}_\ell.
\]

A positive gap can show that label information exists in a folded form, but cannot promote a layer as linearly routable.

### D4. Nested sample-efficiency readouts

Train separate linear heads on nested, cell-stratified subsets containing `1%, 5%, 10%, 25%, 50%, 100%` of train windows. Counts per cell are respectively `10, 51, 102, 256, 512, 1024`. Subsets are fixed from seed `170906`; the smaller subset is contained in every larger subset. Report each layer's CE learning curve and the smallest budget whose recovered gain reaches 95% of its own 100% gain.

### D5. Probe-direction Fisher geometry

For a trained linear head, center its three weight rows and orthonormalize their transpose, yielding its at-most-two-dimensional discriminant basis. On held-out windows, project the exact current-token representations into that basis and compute ridge-regularized within-class and between-class scatter. Report the generalized Fisher eigenvalues and their sum. This diagnoses compact class separation only; it is not a LoRA-rank estimate.

### D6. Discriminant-subspace relations

Using the same orthonormal bases, report principal angles and normalized squared overlap between:

- the parent basis and each true-parent conditional child basis;
- every pair of true-parent conditional child bases.

These quantities diagnose whether coarse and fine Router directions, or different parents' fine directions, are geometrically interchangeable. They do not remove any direction from a probe input.

### D7. Position robustness

Evaluate the same frozen heads separately on positions `63–126`, `127–190`, and `191–254`, plus all 192 positions. This changes only aggregation, never the tensor seen by the Router.

### D8. Leave-one-child-out parent generalization

Train three additional parent classifiers. Fold \(k\) excludes local child \(k\) from every parent during training and evaluates only those three held-out child cells. Rotate \(k=0,1,2\). This asks whether parent readout transfers to unseen children rather than merely memorizing all nine child identities. No analogous fine-label fold is defined because holding out a fine class would remove the target class from training.

## E. Optimization Contract

- Seeds: head initialization and data order `170903`; bootstrap `170904`; shuffled labels `170905`; nested budgets `170906`.
- Base and language head: evaluation mode, bfloat16, `requires_grad=False`, no optimizer membership, no gradients.
- Probe computation: float32.
- Linear heads: AdamW, learning rate `1e-3`, weight decay `1e-4`.
- Nonlinear heads: AdamW, learning rate `3e-4`, weight decay `1e-4`.
- Exactly 3 deterministic passes over train windows; balanced batches contain four windows from each of the nine cells, batch size 36; no scheduler, early stopping, or development-selected checkpoint.
- Final optimizer updates define the checkpoints. All probe families stream the same frozen representations in one base-model pass; the complete token × layer representation tensor is never saved.
- SPOT resume state is atomically written after every optimizer update and contains probe states, optimizers, code hash, frozen configuration, and exact next update.

## F. Metrics And Selection

### F1. Window-first domain-balanced metrics

Token cross-entropy in nats is first averaged within each window. Window values are averaged within each of the nine parent-child cells, then the nine cell means are averaged equally. Accuracy uses the same order. The score margin is the true logit minus the strongest wrong logit, averaged within a window; report its 5th percentile over the balanced held-out windows.

### F2. Primary recovery and candidate

For each task,

\[
R_\ell=\frac{\log 3-\mathrm{CE}_\ell}{\log 3-\min_m\mathrm{CE}_m}.
\]

The primary candidate is the earliest layer whose own and next two recovery values are all at least `0.95`. Development selects parent candidate \(\ell_c\) and conditional-child candidate \(\ell_f\). The rule is frozen before confirmation is read once.

### F3. Diagnostic interpretation

The nonlinear gap, sample-efficiency budget, Fisher strength, subspace angles, position curves, and leave-one-child-out curve describe why the primary linear candidate is easy, folded, sample-fragile, position-fragile, or child-identity-dependent. They are reported for all layers and cannot be combined post hoc into a replacement selector.

Pre-registered fragility flags are: sample-fragile when the candidate needs more than 25% of train windows to recover 95% of its own full-data gain; position-fragile when any of the three position bins has no stable layer or differs from the all-position candidate by more than two blocks; and child-identity-fragile for the parent task when the mean leave-one-child-out candidate is undefined or differs by more than two blocks. These flags qualify interpretation but do not move the primary candidate after seeing results.

### F4. Bootstrap

Run exactly 2,000 replicates, resampling whole windows with replacement separately inside all nine cells and retaining all positions of a sampled window. Recompute full primary CE curves, recoveries, \(\ell_c\), \(\ell_f\), gap intervals, selection rates, and \(P(\ell_f-\ell_c\geq2)\) separately on development and confirmation. Undefined candidates do not satisfy the gap event.

## G. Controls And Smoke Gates

### G1. Window-level label shuffle

Permute parent labels across train windows while preserving global counts. Permute child labels separately inside each true-parent stratum. All positions in one window retain one shuffled target. Train identical linear heads and evaluate them against true held-out labels.

Full qualification requires, for parent and conditional-child heads separately, across-layer median shuffled accuracy in `[0.28,0.39]`, median shuffled CE within `0.05` nat of \(\log 3\), and no three-layer stable shuffled onset.

### G2. Smoke gates

1. Exactly 28 ordered hook hits and tensor shape `[batch,256,1024]`.
2. Exact position bounds and correct parent/conditional-child target routing.
3. Base parameter count frozen before and after; optimizer contains probes only.
4. Nested subset inclusion and exact per-cell counts.
5. Leave-one-child-out folds exclude and evaluate the registered cells exactly.
6. Analytic uniform-logit CE equals \(\log3\) and accuracy equals \(1/3\); trained small-data shuffle metrics remain finite and within `[0.20,0.47]` accuracy.
7. All losses, Fisher matrices, angles, and reported values are finite where mathematically defined.
8. Probe, optimizer, configuration, development freeze marker, and analysis artifacts reload; logits match within `1e-6` absolute tolerance.

## H. Registered Conclusion Branches

1. **Support coarse-before-fine linear readability:** both splits yield stable \(\ell_c<\ell_f\) and both bootstrap probabilities for a gap of at least two layers reach 0.95.
2. **No staggered-layer support:** candidates coincide, differ by one layer, or their order is unstable. A later functional test may compare same-layer candidates only.
3. **Information present but not linearly routable:** the nonlinear probe is strong where the linear probe has no qualified stable layer. Do not promote that layer to a linear Router candidate.
4. **Fragile candidate:** a primary linear candidate exists but is strongly sample-, position-, or held-out-child-dependent. Report the exact fragility; it remains only a provisional candidate.
5. **Insufficient:** no qualified stable linear layer exists. Stop the insertion route.

## I. Execution And Outputs

### I1. Approved resource

Only the following tuple is authorized:

```text
resource_profile=h100-1-spot-user-selected
execution_surface=ACP
workspace=share-space
aec2_cluster=share-cluster
worker_spec=n6ls.iu.i40.1
worker_nodes=1
quota_type=spot
visible_gpus=1
priority=normal
image=registry.cn-sh-01.sensecore.cn/lepton-trainingjob/ngc-pytorch:25.06-cu12.9-py3.12-ubuntu24.04
```

No 5090, reserved quota, multi-GPU, or CCI fallback is authorized.

### I2. Worker surface

All code, logs, checkpoints, caches, and raw outputs remain under:

`/data/250010109/MoE_Router/experiments/20260903_a15_13_e15_true_label_layerwise_static_audit/`

### I3. Required figures and records

1. Parent and conditional-child primary linear CE recovery curves.
2. Linear versus nonlinear CE and nonlinear-gap curves.
3. Sample-efficiency heatmap/curves over layers and budgets.
4. Fisher-strength and discriminant-subspace-angle curves.
5. Position-bin robustness curves.
6. Leave-one-child-out parent generalization curves.
7. Bootstrap candidate/gap table and shuffled-label qualification.
8. Reloadable machine artifacts, `summary.md`, `detailed.md`, embedded audited figures, complete command/job/image/code provenance, and a final four-part result reply.

### I4. Hard stops

Stop before the full run if identity checks or any smoke gate fail. Do not change methods, thresholds, budgets, layer count, seeds, or the primary selector in response to intermediate results. A scientific change requires renewed human confirmation.
