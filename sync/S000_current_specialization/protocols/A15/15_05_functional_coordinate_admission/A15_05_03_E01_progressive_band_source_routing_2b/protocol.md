---
experiment_id: A15_05_03_E01_progressive_band_source_routing_2b
anchor_id: 15_05_03_progressive_band_source_routing
status: approved_with_load_neutral_calibration_for_smoke_and_full
approved_by: user
approval_date: 2026-08-02
resource_profile: 5090-8-spot
chinese_companion: protocol_cn.md
---

# Protocol: Matched 2B Progressive Band-Source Routing

## 0. Approval And Decision

The researcher authorized implementation, smoke, two runs per model, 2B full training, result audit, and an 0803 Focus without another approval stop. Any change to the three arms, HMT schedule, common branch, endpoint, load rule, or primary metric requires a stop; engineering-only repairs remain fail-closed.

## 1. Decision Question

After branching the same 0.629B-token four-layer DCLM MoE, does routing blocks 2/3/4 through H/M/T outperform native routing; and does useful differentiation require each layer's local spectrum or a common block-1 source?

## 2. Hypotheses And Rivals

H1 predicts a local-HMT benefit; H2 predicts a layer1-relay-HMT benefit when coordinate stability dominates. Rivals are distribution-only, information bottleneck, load/compute confounding, and stale projectors.

## 3. Model And Arms

The common model is H768, four blocks, eight sparse plus one shared expert per block, top-1, expert width 1536, running-centered linear Gate, and load-balance coefficient 0.01. Experts always receive the full local state.

| Arm | Block 1 | Block 2 | Block 3 | Block 4 |
| --- | --- | --- | --- | --- |
| native_full | full | full | full | full |
| local_hmt | full | local H64 | local M256 | local T448 |
| layer1_relay_hmt | full | block-1 H64 | block-1 M256 | block-1 T448 |

The block-1 source is the parameter-free RMS-normalized full residual output. All arms execute the same source and projection-shaped path; unused results enter through a zero dependency. No trainable parameters are added.

## 4. Branch, Replicas, Data, And Training

All arms resume the A15_05_05 step-800 checkpoint at 629,145,600 nominal tokens. Post-branch data/RNG seeds 17 and 29 give two paired continuations; arms within a replica share model, optimizer, scheduler, cursor, artifact, and data order.

Train on DCLM shard 01; evaluate 1,024 fixed independent DCLM documents. Use sequence length 1,024, local batch 12/GPU, eight GPUs, accumulation 8, global batch 768, and 786,432 nominal tokens/step. AdamW uses LR $10^{-4}$, betas (0.9,0.95), weight decay 0.01, warmup 636, and the existing 100B-token cosine horizon. Milestones are 800/954/1272/1908/2544; endpoint is 2,000,683,008 total nominal tokens and 1,371,537,408 post-intervention tokens.

## 5. Spectral Artifact

Fit local Gate-effective inputs and the normalized block-1 source on independent fixed DCLM calibration tokens. H/M/T are ranks 1--64, 65--320, and 321--768. Build projectors once offline. Split-half overlap must beat 256 same-rank Haar q95; symmetry, idempotence, trace rank, reconstruction, and final frozen/current overlap are audited.

### 5.1 Load-Neutral Calibration Amendment

The first 8x5090 smoke showed that `local_hmt` violated the preregistered load-comparability guard in blocks 3 and 4 within two post-branch steps. That attempt remains recorded as invalid engineering evidence and no load threshold is relaxed. To start all arms from comparable expert marginals, one frozen expert-constant logit offset is fitted for every treatment arm and layer on the same independent calibration tokens, targeting the branch-time native hard top-1 expert shares. The native offset is identically zero. Offsets are token-independent, add no trainable parameters, do not change the spectral projector or expert input, and remain fixed throughout the 2B continuation. The artifact must show both (i) post-calibration entropy and max-share differences from native no larger than 0.005 and (ii) more than 2% token-level route disagreement in blocks 2--4, so load matching cannot erase the intervention. The stricter post-update smoke guards in Section 8 remain unchanged.

## 6. Primary Metric

For each replica, compute paired held-out document NLL effects

$$
\Delta L_{a:native}^{(s)}=L_a^{(s)}(2B)-L_{native}^{(s)}(2B).
$$

NLL is in nat/token and lower is better. Use 2,000 paired document bootstraps per replica, report both replica effects and an equal-weight pooled effect, and require replica-level direction agreement. Token-normalized NLL AUC is the primary supporting trajectory metric.

## 7. Expert Function Metrics

Report per-routed-token expert update norm; held-out within-expert gradient cosine and negative-conflict rate; forced-expert counterfactual NLL, utility dispersion, calibration/test best-expert stability, and route regret; pairwise expert-output cosine redundancy; and route--utility binding. These explain mechanism and never replace NLL. WOS domain/topic purity is descriptive only.

## 8. Manipulation, Load, And Compute Guards

At least one of blocks 2--4 must exceed 2% fixed-token route disagreement versus paired native. Require no dead expert or capacity drop, milestone normalized load entropy at least 0.95, maximum share at most 0.25, treatment--native entropy difference below 0.02, and max-share difference below 0.05. Match active parameters, steps, tokens, capacity, data order, kernel path, and measured/analytic FLOPs. Native/source replay, top-1 identity, and exact resume are mandatory.

To prevent a SPOT recovery from becoming an unregistered stochastic arm, training uses deterministic CUDA algorithms and a fixed cuBLAS workspace. The continuation seed is overridden only at the shared step-800 branch; later resumes preserve checkpoint RNG. Every optimizer step records a SHA-256 of the actual rank-0 input batches. The shared-source continuous/resumed smoke must have the same batch hash, parameter relative error at most $2\times10^{-6}$, logit relative error at most $2\times10^{-5}$, exact top-1 identity, and NLL difference at most $2\times10^{-5}$. A runner restored at its requested terminal step must exit without another update.

## 9. Comparisons And Statistics

Primary contrasts are local-minus-native, relay-minus-native, and relay-minus-local. Compare blocks 2--4 and milestones 954/1272/1908/2544. The two continuations are replication units; documents are not training seeds.

## 10. Execution Stages

S0 provenance; S1 unit/local tests; S2 eight-GPU step800-to-802 smoke for all arms/replicas; S3 six independent jobs to step2544; S4 NLL/route/load/basis/update/conflict/utility/redundancy evaluation; S5 typed verdict and records. Smoke loss has no scientific role. Do not relax guards, shorten 2B, or remove an adverse replica.

## 11. Resource Contract

SCO ACP only: workspace `share-space`, AEC2 `computing-cluster-5090-01g`, worker spec `n12lp.nn.i10a.8`, one node, eight RTX5090 GPUs, SPOT, normal priority. Each arm/replica is one job with exact-resume support; debug cluster substitution is forbidden.

## 12. Figure And Table Contract

Create NLL-vs-FLOP trajectories, final paired NLL effects, per-layer route/load manipulation, and expert-function mechanism panels; plus compute/load and pairwise-verdict tables. Audit every rendered figure and state units, allowed conclusion, and limitation.

## 13. Verdicts

Pass with functional differentiation requires one treatment to have a paired 95% NLL upper bound below zero in both replicas, concordant NLL AUC, and at least one concordant expert-function improvement not explained by load. Quality-only and specialization-only are separate partial verdicts. Valid route change without stable quality/function benefit is distribution-only/Fail. Broken pairing, replication, completion, load/compute, basis/source, resume, forced-expert, or held-out evaluation is Insufficient.

## 14. Boundary And Deliverables

The experiment is a causal continuation from one shared early state, not a from-initialization law. It cannot establish optimal HMT order, universal semantic rank, superiority to a random schedule, or deep-model scaling. Deliver manifests, six job IDs, milestones, per-document NLL, route/load/update/conflict/utility/redundancy tables, central figures, summary, detailed record, Anchor update, and `daily_research_reports/0803/focus.md`. Do not edit the graph or commit/push.
