# Detailed: A15_05_05_E01 Matched 2B Fixed-Band Dispatch

Primary anchor: [15_03](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_05_functional_coordinate_admission/subanchors/15_05_05_matched_fixed_band_dispatch_anchor.md)  
Protocol: [protocol.md](protocol.md)  
Summary: [summary.md](summary.md)

## 0. Quick Recap

**Purpose:** determine whether fixed H/M/T/N Gate views causally alter dispatch
and improve matched-compute 2B language-model training.  
**Hypothesis:** at least one true covariance band both changes routing and
beats native plus its equal-rank random view on held-out NLL.  
**Direct result:** all four true bands changed routing; all four had worse NLL
than native. Only head beat its random control.  
**Verdict:** completed Fail / distribution-only.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete computation | Unit | Decision role | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| native | Gate sees the complete 768-d input | original Gate forward | condition | quality reference | optimal Router |
| H/M/T/N | fixed covariance-rank views | ranks 1--64 / 65--320 / 321--768 / 65--768 | dimensions | true spectral treatments | semantics |
| equal-rank random | random orthogonal view of matching rank | Haar basis fixed at branch | condition | separates spectrum from reduction | functional null for every learned feature |
| held-out NLL | average surprise on correct next tokens | mean negative log probability | nat/token | primary quality metric; lower is better | expert specialization mechanism |
| route disagreement | frozen tokens assigned to another expert than native | mean route inequality | token fraction | manipulation check | benefit |
| load entropy | closeness of expert counts to uniform | entropy divided by \(\log 8\) | [0,1] | load-collapse guard | semantic quality |
| frozen/current overlap | whether the frozen projector still matches the final spectrum | normalized projector overlap | [0,1] | basis-staleness guard | utility |
| paired CI | uncertainty over the same held-out documents | 2,000 paired document bootstraps | nat/token | sign stability | cross-seed generality |

## 2. Anchor Link And Decision Point

A15_05_05 deliberately bypassed the earlier failed one-step compatibility admission
only because the researcher authorized a new terminal causal ablation. The
question was not whether M/T/N are statically novel; it was whether forcing
dispatch through them changes the expert learning path and improves held-out
language modeling.

## 3. Protocol Compliance Audit

- common branch checkpoint and optimizer/scheduler/data/RNG resume: **passed**;
- nine registered arms and equal-rank controls: **passed**;
- 2B endpoint for every arm: **passed**;
- actual Gate-input projection and native replay: **passed**;
- matched token count, capacity, active parameters, and training kernel:
  **passed**;
- load and runtime guards: **passed**;
- paired DCLM held-out evaluation and WOS diagnostics: **passed**;
- result rule applied without threshold changes: **Fail / distribution-only**.

## 4. Setup

**Model:** H768, four transformer layers, eight sparse experts plus one shared
expert, top-1, running center, load-balancing coefficient 0.01. Experts receive
the full hidden state in every arm.  
**Branch:** step 800, 629,145,600 nominal tokens.  
**Endpoint:** step 2,544, 2,000,683,008 nominal tokens.  
**Training:** DCLM shard 01; sequence length 1,024; global batch 768; AdamW
\(10^{-4}\), weight decay 0.01; warmup 636; common 100B-token scheduler horizon.  
**Evaluation:** 1,024 disjoint DCLM documents of length 1,024; WOS contains
1,344 labeled 128-token abstracts and is diagnostic only.  
**Projection:** per layer, freeze branch mean \(\mu\) and projector \(P\), then
compute \(z=W\mu+(WP)(r-\mu)\).  
**Projection SHA-256:**
3b55b4eb22d193b57bd709e8e22342afd263e4f58daeb9ab57549eaebf2ce402.

One branch seed is a strict paired causal comparison for this trajectory.
Layers, documents, and nine arms are not independent training seeds.

## 5. Metrics And Decision Rules

The primary effect is

\[
\Delta L_{a:b}=L_a^{heldout}(2B)-L_b^{heldout}(2B).
\]

Positive values mean arm \(a\) predicts held-out tokens worse. Band-specific Pass
required a route manipulation plus a paired upper confidence bound below zero
against both native and the equal-rank random arm. All true arms failing that
criterion with valid guards is Fail. Route change without quality gain is
classified as distribution-only.

## 6. Main Results

### Primary paired effects

| True arm | NLL | \(\Delta\) vs native [95% CI] | \(\Delta\) vs random [95% CI] | Verdict |
| --- | ---: | ---: | ---: | --- |
| head64 | 4.248453 | +0.001784 [0.001359, 0.002202] | -0.004375 [-0.005152, -0.003576] | worse than native; better than random64 |
| middle256 | 4.252269 | +0.005600 [0.004656, 0.006498] | +0.002709 [0.001867, 0.003540] | worse than both |
| tail448 | 4.250366 | +0.003697 [0.002816, 0.004542] | +0.000765 [-0.000094, 0.001619] | worse than native; indistinguishable from random |
| nonhead704 | 4.249977 | +0.003308 [0.002567, 0.004019] | +0.001811 [0.001084, 0.002527] | worse than both |

Native NLL was 4.246669. All random views were also worse than native:
random64 +0.006159, random256 +0.002892, random448 +0.002932, and random704
+0.001497 nat/token, with paired intervals above zero.

### Manipulation and pathway evidence

True-arm route disagreement versus the independently trained native endpoint
was 4.98% (H), 19.80% (M), 21.88% (T), and 13.26% (N). Within each trained
model, comparing its projected Gate with its counterfactual full Gate produced
5.06%, 15.61%, 14.98%, and 11.85% disagreement. The intervention therefore
remained behaviorally active.

Normalized DCLM load entropy was 0.9974--0.9983. Mean expert-relative parameter
displacement was 0.277--0.282 across arms, and per-microbatch median time varied
by only 1.05%. Neither load collapse nor material compute mismatch explains
the primary ordering.

Frozen/current overlap at 2B was 0.689 (H), 0.572 (M), 0.772 (T), and 0.968
(N). A fixed branch basis is not identical to the final spectrum, especially
for middle, but all retain substantial identity; staleness cannot turn the
observed positive NLL effects into evidence of benefit.

### Trajectory and WOS evidence

Held-out NLL at steps 954/1,272/1,908/2,544 never showed a sustained true-band
advantage over native. Token-normalized NLL AUC was lowest for native
(4.64457), with random704 close (4.64494).

At 2B, WOS domain cross-validated route accuracy was 0.246--0.288 across arms
(chance 0.143) and topic accuracy 0.096--0.121 (chance 0.036). No true band
meaningfully improved these diagnostic labels; WOS was not used for the
training verdict.

## 7. Visualization Results

### Final held-out NLL effects

![Final held-out NLL effects](figures/final_nll_effects_vs_native.png)

**Purpose:** decide whether any true band improves the primary outcome.  
**Setup:** 1,024 paired DCLM documents at the common 2B endpoint.  
**Metric:** treatment minus native NLL, nat/token; lower is better.  
**How to read:** an interval must lie below zero to indicate benefit.  
**Observed:** all true-band intervals lie strictly above zero.  
**Take-home:** no fixed true band beats native.  
**Limitation:** one branch seed.

### Routing change versus quality

![Routing change versus quality](figures/routing_change_vs_nll.png)

**Purpose:** separate an ineffective manipulation from a harmful alternative
partition.  
**Setup:** frozen DCLM tokens at 2B.  
**Axes:** expert disagreement versus native and NLL effect versus native.  
**Observed:** true M/T/N cause large route changes while remaining above zero
in NLL effect.  
**Take-home:** the negative result is distribution-only, not no-manipulation.  
**Limitation:** route identity does not reveal token compatibility.

### Held-out trajectory

![Held-out NLL trajectories](figures/heldout_nll_trajectories.png)

**Purpose:** check whether the final comparison hides a transient or late
reversal.  
**Setup:** shared branch point and four registered later checkpoints.  
**Metric:** held-out NLL versus nominal tokens.  
**Observed:** curves remain close, but no true band develops a durable
advantage; native is best at 2B and in token-normalized AUC.  
**Limitation:** sparse checkpoints are a macro trajectory, not per-step
dynamics.

## 8. Stage Evidence And Failure Decomposition

| Stage | Evidence | Verdict | What it rules out |
| --- | --- | --- | --- |
| S0 | branch/config/data/projection hashes | passed | provenance drift |
| S1 | two-arm smoke job om-d2q5k5sz | passed | invalid projection/resume |
| S2 | nine jobs, step 2544, 2.000683B each | passed | incomplete exposure |
| S3 | load, timing, checkpoint, error guards | passed | collapse/compute artifact |
| S4 | DCLM/WOS routes and NLL at milestones | passed | missing manipulation/evaluation |
| S5 | 2,000 paired document bootstraps | passed | held-out document sign fragility |

**Falsified for this branch:** fixed H/M/T/N band-only dispatch improves 2B
held-out NLL; M/T/N spectral identity beats generic equal-rank views.  
**Not falsified:** learned additive or task-conditioned coordinates may carry
useful expert-update information.

## 9. Full Experiment Record

All jobs used one 5090-8-spot node with eight RTX5090 GPUs, workspace
share-space, AEC2 computing-cluster-5090-01g, worker spec n12lp.nn.i10a.8,
spot quota, normal priority.

| Arm | Job ID | Final step | Tokens |
| --- | --- | ---: | ---: |
| native | om-obg9hxlp | 2544 | 2,000,683,008 |
| head64 | om-2f20fhhf | 2544 | 2,000,683,008 |
| random64 | om-efcji238 | 2544 | 2,000,683,008 |
| middle256 | om-832yq6kn | 2544 | 2,000,683,008 |
| random256 | om-2sv8y5gi | 2544 | 2,000,683,008 |
| tail448 | om-jjydcaxm | 2544 | 2,000,683,008 |
| random448 | om-45lqfz2g | 2544 | 2,000,683,008 |
| nonhead704 | om-0w47unue | 2544 | 2,000,683,008 |
| random704 | om-vtawzcli | 2544 | 2,000,683,008 |

All jobs succeeded with zero retry. Checkpoint hashes, timing, sampled load, and
full job names are in [run_evidence.csv](tables/run_evidence.csv).

## 10. Interpretation

The experiment separates three statements. First, fixed bands can control
dispatch: this passed. Second, a band may be more structurally aligned than a
random subspace: head passed this comparison. Third, the resulting partition
must improve expert learning: no band passed. The failure of the third clause
means covariance rank is not, by itself, a sufficient functional routing
target.

The condition-stratified residual audit explains why fixed residual bands can
remain geometrically meaningful while failing functionally: shared or
condition-varying geometry does not specify which tokens have compatible
expert updates.

## 11. Claim Boundary

The causal claim is restricted to one H768 four-layer DCLM branch seed and
band-only Gate views frozen at 0.629B tokens. It cannot be generalized to all
initializations, larger models, additive spectral features, dynamically
updated projectors, or supervised task-conditioned Router objectives.

## 12. Next Decision

Close fixed covariance-rank band-only dispatch. Before another large matched
training, require the candidate representation to pass a held-out functional
gate tied directly to expert-update compatibility or task utility.

## 13. Links And Artifact Map

- anchor: [15_03 anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_05_functional_coordinate_admission/subanchors/15_05_05_matched_fixed_band_dispatch_anchor.md)
- protocol: [protocol.md](protocol.md)
- summary: [summary.md](summary.md)
- curated tables: [final_arm_summary.csv](tables/final_arm_summary.csv),
  [heldout_trajectory.csv](tables/heldout_trajectory.csv),
  [heldout_auc.csv](tables/heldout_auc.csv),
  [run_evidence.csv](tables/run_evidence.csv), and
  [verdict.json](tables/verdict.json)
- worker package:
  /data/250010109/MoE_Router/experiments/20260731_a15_03_2b_band_dispatch_5090
- full run/evaluation outputs remain on the worker surface under runs/
