# Detailed: same-panel native structure and virtual-update bridge

[Summary](summary.md) · [中文摘要](summary_cn.md) · [Meeting explanation](../../focus_meeting_structure_update_cn.md)

This record owns the new 2026-09-26 exploratory measurement only. It does not replace earlier Anchors, Protocols, result records, or researcher-owned judgments.

## 0. Result and eligibility

The bounded local readout completed on one H100 MIG device. All 1,024 representation records and eight independently reset perturbation branches are present. Native and FP32-tail replay guards passed exactly; baseline repeats and final restoration differed by zero. No optimizer trajectory or model checkpoint was written.

Two observable facts coexist: domains occupy different locations in common representation coordinates, and all 12 cross-domain mean directions improve heldout-record loss at both tested step sizes. Full-step computer-science self-improvement has an interval slightly crossing zero. This prevents a blanket claim that every source-improvement qualification is statistically resolved.

Eligibility is **BOUNDED exploratory**: previously inspected source splits, one checkpoint, a specified hybrid numerical path, fixed source gradients, 16 target positions per record, no paper-level independence, and no long-run sharing/isolation comparison. The user explicitly requested completion and analysis of the figures and logic chain without another approval; this is the bounded local implementation of the minimum same-state update check. It is not a new human-owned scientific transition.

## 1. Scope fixed before readout

Parent question: how native representation structure can be connected to actual consequences of shared-parameter updates.

Design context: [natural-domain readout](../../../0925/docs/sae_domain_activation/detailed.md) and [existing shared-parameter question](../../../0925/docs/human_semantic_updates/anchor_cn.md). The earlier question Anchor still has historical draft wording; its newer execution/results are owned by its Protocol, Summary and Detailed record. No state was inferred from that stale wording.

The pre-readout [analysis contract](/data/250010109/MoE_Router/experiments/20260926_structure_update_bridge/analysis_contract.json) was written before model loading and observations at `2026-09-26T01:04:48.906428+00:00`; SHA256 `251e875b5081fd8a48d13f72bbbb0ec304e1194b241ef46f4b5f492cc718a340`. It freezes input identity, objects, position sampling, two step sizes, update/readout roles, uncertainty procedure and limitations. It is an execution specification for the requested exploratory analysis, not a retroactive confirmatory Protocol.

| Fixed item | Actual | Eligibility |
| --- | --- | --- |
| Same existing panel | 1,024 records from `20260925_sae_domain_activation/selected.jsonl` | No activation-based resampling or exclusions |
| One checkpoint | Fresh S7, reconstruction coefficient 0.1 from scratch, exactly 21 billion pretraining tokens | Not the historical reweighted S7 |
| Native objects | Last block attention output after output projection; actual down-projection input | Both extracted in the same forward |
| Plot axes | Fit-only, pooled balanced four-domain axes; independent readout batch | No per-domain axis fitting or test-based selection |
| Spectral definitions | Centered covariance spectrum and uncentered second moment | Distinct denominators; all sample-visible components retained |
| Updates | Four source directions × two relative norms, reset independently | All eight completed; no sequence of accumulating updates |
| Prediction positions | Input indices 14,30,…,254 predict token indices 15,31,…,255 | 16 valid next-token targets per record, zero-based indices |
| Primary interpretation | Every source/target consequence shown, source improvement separated | No selected negative subgroup or confirmatory claim |
| Numerical controls | Native replay, complete-forward FP32-tail replay, zero delta and exact restoration | All passed; no numerical failure excluded |

No data, metric or step size was changed after the results. No retry was needed. The original ChatGPT document bodies and mentor attachment are unavailable; only their visible conversation descriptions were used to reconstruct the requested visual deliverable. That limits fidelity to the original requested drawing, not the numerical identity of the new measurements.

## 2. Objects and mathematical bridge

Code source: `/data/250010109/MoE_Router/experiments/20260920_s7_lambda0p1_from_scratch_4h100/dense_sae/model/modeling_qwen3_sae.py`.

The sidecar observes the last block's attention output `a`, after `attn.o` and before the residual addition. It does not modify the forward language-model path. The input of the adapted `blocks[7].down` is instead

\[u=\operatorname{silu}(W_g\operatorname{norm2}(x+a))\odot W_{up}\operatorname{norm2}(x+a).\]

Here `a` has 1,024 coordinates, `u` has 3,072, and `down.weight` has shape 1,024×3,072. See the source's `attention_residual`, `mlp_input`, `finish_mlp`, and `forward_intermediates` methods. The native observer identity and captured pre-hook input were checked during extraction.

For one token and `y=Wu`, let `e` denote the loss derivative with respect to `y`, including downstream residual/norm/head effects. Then `d loss / d W = e u^T`. For two single-token gradients, their Frobenius inner product is `(e_A^T e_B)(u_A^T u_B)`. Group gradients average token outer products; a group mean vector does not substitute for that average. This is a chain-rule identity, not empirical identification of the semantic source of error signals.

The local loss change on a readout group is approximately `-eta <grad L_readout, G_source>`. Its finite-step outcome was actually evaluated. The plotted gradient cosine uses the two fit-source gradients, so it is not substituted for heldout-readout consequences.

## 3. Actual setup

Checkpoint directory:
`/data/250010109/MoE_Router/experiments/20260920_s7_lambda0p1_from_scratch_4h100/runs/S7_lambda0p1_from_scratch_4h100/milestones/token_021000000000`.

The checkpoint `state.pt` SHA256 was recomputed before loading:
`edd781c8f747477e9f236128d26423d435c800d37da2d446c85e4a6ebc206f33`.

Input source: the previous fixed natural academic-text panel, official source revision `6ae613ba744ee56f645aee9c577d04f7e3d48b30`. Computing uses cs.CL/cs.CV; mathematics math.AG/math.NT; physics physics.flu-dyn/physics.optics; biology q-bio.GN/q-bio.NC. Each subfield supplies 64 records per fit/readout split. Every record has 256 existing content token IDs; no injected labels or answer templates. Ordered selection file SHA256:
`7e8858adfbf1ead8330937dc147eee3eb815be9025e620e53c0af0fc86d155d9`.

Rows have unique sample IDs and full-input hashes. Paper IDs are unavailable and previous auditing exposed these corpus splits; neither record uniqueness nor fit/test separation proves independent papers or unseen pretraining content.

Primary representation: the mean of all 256 body positions. Last-position vectors and unit-normalized body-mean vectors are separate sensitivities. The norm plotted is the norm of the body-mean vector, not the average token norm. Each object/pooling owns its own fit mean and common basis; absolute axes and signs are not comparable across these bases.

Update loss: mean next-token cross entropy at the 16 prespecified positions; each group has 128×16=2,048 fit targets and 2,048 readout targets. Total representation extraction is 262,144 tokens; the loss reads a subset, not all 255 possible next-token positions. Baseline readout loss by domain is 3.558357, 3.490630, 3.564044 and 3.501418 nats/target respectively.

Only a functional additive full-matrix delta is differentiable. The original model parameters remain frozen. For source gradient `G`, set `delta=-rho*||W||F*G/||G||F`, with `rho=1e-4` and `5e-5`; `||W||F=62.9504433`. Each branch starts with delta zero and returns to zero. There is no optimizer, momentum, scheduler, gradient clipping, low-rank constraint or accumulated training trajectory. Therefore optimizer updates are zero even though eight real forward evaluations under virtual parameter changes were performed.

Numerics: original FP32 weights with BF16 upstream forward; captured down inputs are promoted to FP32, and down, residual, final norm and vocabulary head operate in FP32 with TF32 disabled. This deliberately explicit numerical path resolves steps that could be obscured by BF16 rounding. A complete forward with only the final down output overridden to FP32 exactly matched the replayed tail. This is not a claim that every FP32-tail value equals the earlier BF16-logit task outputs. Both baseline and perturbed measurements use the same numerical path.

Extraction microbatch is eight records. Gradient/readout chunks contain four records ×16 positions, reducing gradients with the correct 128-record source denominator. Torch deterministic operations use `CUBLAS_WORKSPACE_CONFIG=:4096:8`; source-gradient directions are fixed, not treated as random training seeds.

## 4. Computation and uncertainty

For each object/pooling, fit mean `mu` and right singular vectors `V` from the balanced 512-record first batch. Centered spectral shares are `s_i² / sum(s²)`. The uncentered shares use singular values of the raw first-batch matrix. Mean-energy fraction is `||mu||² / mean(||x||²)`. Readout two-axis coverage divides `sum(((X_readout-mu)V_2)²)` by `sum((X_readout-mu)²)`, including energy outside the fit subspace. No whitening or label-supervised axis selection is used.

The centered first-batch rank is at most 511. This sample rank is not an estimate that the population has no additional directions. Participation ratio and 90%-variance direction count measure different aspects; neither is a semantic-concept count.

Help is `baseline - after`, averaged over a target's 128 readout records. Bootstrap seed 20260926 draws 64 records with replacement within each of its two subfields, 2,000 times. The same draws are applied to all eight branches for that target, preserving the paired baseline and branch comparisons. Reported percentile intervals are marginal descriptive intervals, conditional on the four fixed source gradients and one model. No 32-cell multiplicity adjustment or paper-cluster sampling is claimed.

The full-dictionary activation distance uses the previous same-panel fit profiles: normalize each domain's 30,000 feature-frequency vector to sum one, then take half the L1 difference. All six unordered pairs are shown against their symmetric average local help. They share four source groups and are not independent replicates. No correlation test, predictive model or claim of incremental value beyond lexical baselines is made.

## 5. Main results

| Representation | 90% centered-variance directions | 90% raw-energy directions | Readout energy covered by two fit axes | Fit mean energy fraction |
| --- | ---: | ---: | ---: | ---: |
| Attention body mean | 108 | 1 | 29.4190% | 92.1356% |
| Attention last position | 161 | 20 | 19.7198% | 80.5662% |
| Unit-normalized attention body mean | 109 | 1 | 30.6308% | 92.3161% |
| Down-input body mean | 95 | 23 | 32.5640% | 66.4086% |
| Down-input last position | 213 | 185 | 12.5734% | 19.9363% |
| Unit-normalized down-input body mean | 99 | 24 | 30.4236% | 66.8549% |

The first uncentered attention-mean component explains 92.3315%; the first centered component explains 21.2909%. The large difference is compatible with a dominant common mean, not one-dimensional sample variation. The corresponding participation ratio is 16.4320, whereas the 90% count is 108: concentration and coverage counts must not be interchanged.

| Source self-improvement | Full step: mean [95% interval] | Half step: mean [95% interval] |
| --- | --- | --- |
| Computing | 0.000892 [−0.000006, 0.001748] | 0.000497 [0.000050, 0.000925] |
| Mathematics | 0.002837 [0.002142, 0.003546] | 0.001451 [0.001103, 0.001805] |
| Physics | 0.001487 [0.000715, 0.002253] | 0.000782 [0.000395, 0.001164] |
| Biology | 0.001538 [0.000703, 0.002408] | 0.000814 [0.000396, 0.001252] |

All 12 cross-group mean directions and their marginal interval lower bounds are positive at both sizes. Full-step cross help ranges 0.0005324858–0.0020056693; half-step 0.0002764876–0.0010430939. This is a local mean result: across individual cross-group cells, 31.25%–46.09% of readout records increase in loss. Their sign stability under independent updates was not tested, so those records are not labeled a discovered harmful subgroup.

Six source-gradient cosines range 0.122875–0.335316. Smaller cosine still does not imply negative transfer. The half/full mean-help ratios differ from exactly 0.5 by at most 0.05746, indicating that proportionality is approximate; no exact linear model or absence of curvature is claimed.

## 6. Evidence lineage and figure map

| Reading | Raw evidence | Transformation | Output | Boundary |
| --- | --- | --- | --- | --- |
| Native distribution | `representations.npz`, ordered original `selected.jsonl` | Fit-only common PCA, heldout scatter/ECDF | `common_axes.npz`, `structure_results.json` | Pooled records, limited displayed energy |
| Parameter-input distribution | Same-record `u_mean/u_last` | Same rule in separate object coordinates | Same structure outputs | Inputs are not weight-space gradients |
| Local update consequence | `fixed_tail_cache.pt`, `source_gradients.pt`, `update_losses.npz` | Independent normalized perturbations, target mean, paired bootstrap | `update_summary.csv`, `update_results.json` | One state and fixed source gradients |
| Activation/update association display | Previous `domain_profiles.npz`, new update outputs | All six fit-profile distances and symmetric mean helps | Pair rows in `update_results.json` | Descriptive; no learned or heldout predictor |

![Native shared-coordinate figure](../../figures/a_common_axes_and_spectrum.png)

Purpose: show actual heldout-record distribution and distinguish raw-energy concentration from centered variation. Coordinates are fit-only; four colors have the same axes. Top-right distributions are empirical cumulative fractions, not smoothed density estimates. Bottom-right normalization refits common axes and cannot be read as a direct coordinate displacement. The figure supports structural differences, not semantic purity or interference.

![Actual down-input figure](../../figures/u_common_axes_and_spectrum.png)

Purpose: identify the actual input of the affected matrix. The same records are retained; the parameter-input axes are distinct from native-attention axes. It cannot identify backward error signals or a mechanism of long-run shared loss.

![Same-panel consequences](../../figures/same_panel_update_consequences.png)

Purpose: read actual update consequences and prevent substituting gradient cosine or activation distances for loss change. Rows are update sources, columns are readout groups. Positive/blue means help; full and half panels share one color scale. Loss values in the image are multiplied by 1,000. The six-point panel is descriptive and shares source groups. Full-step computing self-improvement remains uncertain.

Evidence copies are under the execution root `figures/`; reading copies are in this date's `figures/`. Every source path and SHA256 appears in [figure_manifest.json](/data/250010109/MoE_Router/experiments/20260926_structure_update_bridge/figure_manifest.json) and the local [reading-copy manifest](../../figures/structure_update_manifest.json). Source and reading bytes must agree; no generated payload is staged for Git.

## 7. Execution and guards

[Completion receipt](/data/250010109/MoE_Router/experiments/20260926_structure_update_bridge/complete.json): elapsed 68.40 seconds, NVIDIA H100 80GB HBM3 MIG 3g.40gb, PyTorch 2.3.0a0+6ddf5cf85e.nv24.04. Peak allocated 2,049,991,680 bytes; reserved 2,206,203,904 bytes. This elapsed time excludes later CPU analysis and writing.

| Guard | Outcome |
| --- | --- |
| Checkpoint hash | Matches fresh exact-21B identity |
| Captured attention = native SAE input | Exact |
| Native tail = native full forward | Maximum absolute difference 0 |
| FP32 replay = full forward with FP32 final down | Maximum absolute difference 0 |
| Native RMS = previous same-record activation cache | Maximum absolute difference 0 |
| Ordered sample IDs | Exact alignment, 1,024 unique IDs/input hashes |
| Baseline repeat and zero-delta final return | Bitwise equal losses |
| Original down weight | Bitwise unchanged |
| Model sampled state and SAE activity buffers | Unchanged |
| Completion | 8/8 branches; finite gradients, losses and representations |

No engineering failure, excluded branch, remote job or formal confirmatory readout occurred. The existing 9月24日 confirmation seal was not opened; the unrelated 9月25日 choice-task confirmation had already been completed in its own experiment.

## 8. Full round record and interpretation

Question tested: does the existing natural-domain structure correspond to local cross-group harm at this checkpoint and final matrix?

Setup and controls: one fixed base, source panel, parameter position, numerical path, loss and position rule; all original weights frozen; paired baseline and independent perturbations.

Data: the 512 fit records provide common axes and update gradients. The distinct 512 readout records provide displayed points and local consequences. This is an exploratory role separation within previously exposed data, not newly sealed confirmation.

Result: complete as above; mean cross-help at both sizes, one uncertain source self-improvement interval, strong raw mean-energy contribution and broader centered variation.

Insight and boundary: domain-associated structure is compatible with local mean help. The result constrains the direct inference from separability to harm. It does not establish why help arises, prove semantic features, or show that isolation is always unnecessary. Earlier negative or insufficient comparisons are preserved in their owning records and not rescued by the new geometry.

One AI-proposed next decision, revised for the researcher's 2026-09-26 mechanism-first discussion: select one empirically grounded learning consequence and its strongest rival explanation for a separating test. The observed local help is a possible target; a long-run sharing deficit requires its own matched-carrier evidence. Complete this decision by naming the effect, fixed scope, rival predictions and support/non-support/insufficient branches. If a local-harm hypothesis is chosen, both source improvement and independent target harm must qualify; continued help or insufficient evidence must stop using that condition to motivate isolation. Resume from the existing figures and evidence; finding harm is not the success criterion. The specific scientific choice awaits the researcher, and no follow-up run was started.

## 9. Reproduction and artifact map

Execution root: `/data/250010109/MoE_Router/experiments/20260926_structure_update_bridge`.

Collection source: [collect_structure_update.py](../../report_assets/collect_structure_update.py); reuse: verified loader/capture helper and previous fixed panel; adapt: final-tail replay and functional additive perturbations; rejected: old domain-selected feature heatmaps as the native-structure plot, continuous training code, and any unsealed confirmation dataset. Source model and SAE digests are in the completion receipt. The collection script refuses to overwrite a completed result.

Analysis source: [analyze_structure_update.py](../../report_assets/analyze_structure_update.py). Raw output identities are in [raw_manifest.json](/data/250010109/MoE_Router/experiments/20260926_structure_update_bridge/raw_manifest.json); derived output identities and code hash are in the figure manifest. The associated [direct validation receipt](/data/250010109/MoE_Router/experiments/20260926_structure_update_bridge/validation.json) records independent numerical and file checks.

```bash
CUBLAS_WORKSPACE_CONFIG=:4096:8 OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 \
  timeout 1800 python /data/250010109/Research_System/daily_research_reports/0926/report_assets/collect_structure_update.py
OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 \
  python /data/250010109/Research_System/daily_research_reports/0926/report_assets/analyze_structure_update.py
```

Use a separately identified output root for any new measurement; do not delete this completed evidence just to rerun the fixed-root collector. No remote job ID applies. Original documents, memories, project maps, Graphs, user changes and frozen experiment contracts were left intact.
