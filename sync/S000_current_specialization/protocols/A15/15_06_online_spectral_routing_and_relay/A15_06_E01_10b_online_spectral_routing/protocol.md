---
experiment_id: A15_06_E01_10b_online_spectral_routing
legacy_experiment_id: A15_00_E01_10b_five_arm_training
anchor_id: A15_06_online_spectral_routing_and_relay
status: approved_for_implementation_smoke_and_full
approved_by: user
approval_date: 2026-08-03
resource_profile: 5090-8-spot
primary_metric: paired held-out NLL at 10B tokens
---

# Protocol: A15_06_E01 10B Five-Arm Online Spectral Router Training

## 0. Approval Snapshot

**Approval status:** approved for implementation, smoke, and ten full jobs.  
**Purpose:** decide whether dynamic covariance Relay-HMT has terminal value
beyond centering, local bands, and an equal-dimension random Relay.  
**Primary anchor:** [A15_06](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_06_online_spectral_routing_and_relay/15_06_online_spectral_routing_and_relay_anchor.md).  
**Physical prior tested:** online continuity-constrained bands reduce stale
coordinates, and a shared shallow source reduces deeper Router search drift.  
**Strongest rival:** any stable shallow bottleneck or centering gives the same
benefit.  
**Experiment role:** method construction with matched causal controls.  
**Primary metric:** per-document paired held-out NLL at 10B, nat/token.  
**Conditions:** Vanilla-Full, Centered-Full, Local-HMT, Relay-HMT,
Relay-Random at seeds 17 and 29.  
**Support:** Relay-HMT is lower than Centered-Full, Local-HMT, and Relay-Random
in both seeds with paired-document intervals in the same direction and no
load/compute explanation.  
**Not support:** any registered comparison lacks the reproducible ordering.  
**Insufficient:** an engineering or evidence guard prevents valid 10B paired
evaluation.  
**Cannot claim:** universal band semantics, model-scale transfer,
compositionality, or specialization as the unique mechanism.  
**Execution boundary:** submit all ten jobs after smoke; monitor through real
optimizer steps and one online refresh, then leave jobs running for a later
result-analysis turn.  No graph, sync, commit, or push.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit / formula | Decision role | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| running center | deployable mean removed only from the Gate view | existing distributed EMA mean, decay base 0.99 and scale 40 | activation | separates centering | semantic value |
| H/M/T | high-, middle-, low-background-variance directions | nested ranks 1--64, 65--320, 321--768 | subspace | spectral treatment | semantic hierarchy |
| Relay | deeper Gate reads the same token's block-1 output | parameter-free RMS-normalized block-1 residual output | 768-d activation | shared-source effect | immutable source representation |
| route flip | tokens whose winning expert changes after a projector refresh | old and candidate top-1 on fixed guard tokens | fraction | refresh continuity | quality |
| margin | winning logit minus second logit | old Gate on guard tokens | logit | confidence definition | correctness |
| terminal NLL | surprise on fixed unseen documents at 10B | mean negative log probability | nat/token, lower better | primary decision | mechanism |

## 2. Anchor Alignment

The experiment changes one uncertainty: whether online covariance identity,
rather than centering or an arbitrary smooth bottleneck, improves the 10B
endpoint.  The decisive falsifier is Relay-HMT failing to beat Relay-Random in
either seed.

## 3. Tested Hypothesis

Relay-HMT supplies a shared, dynamically maintained covariance coordinate that
reduces deeper Router search drift and yields lower 10B held-out NLL than
Centered-Full, Local-HMT, and Relay-Random.

Block 1 remains trainable and Relay gradients reach it.  The one logical
block-1 running mean is physically replicated in the three downstream Gates;
the run fails closed if their values or update counts ever diverge.

## 4. Rival Explanations

1. Centering alone explains improvement.
2. Any stable equal-dimension Relay is sufficient.
3. Local online bands are equally effective; source depth is irrelevant.
4. Apparent quality comes from load, capacity, extra FLOPs, or evaluation
   mismatch.
5. Continuity rejects almost every update, reducing the method to a stale
   fixed projector.

## 5. Data / Model / Algorithm / Objective

The model is the validated four-block H768 DCLM MoE: eight sparse experts, one
shared expert, top-1 routing, sparse expert width 1,536, sequence length 1,024,
global batch 768, BF16, ZeRO-1, AdamW $(\beta_1,\beta_2)=(0.9,0.95)$,
weight decay 0.01, LR $10^{-4}$, 636-step warmup, and the existing 100B-token
cosine horizon.  Each full job stops at step 12,716, or 10,000,269,312 nominal
tokens.  Load-balancing coefficient is 0.01 in every arm.  The validated MoE
implementation has no finite-capacity truncation: every top-1 assignment is
executed, so capacity-drop fraction is structurally zero and is recorded as a
milestone guard rather than treated as a varying outcome.

Training uses the same frozen DCLM shard, tokenizer, sample permutation, and
fixed 1,024-document held-out evaluation within each seed.  Statistics use at
least 65,536 disjoint fixed tokens; guard evaluation uses at least 16,384
additional disjoint fixed tokens.  Text/token order and SHA-256 are immutable.

## 6. Conditions, Seeds, And Checkpoints

| Item | Clause / rival | Changed term | Evidence | Support | Not support | Insufficient | Figure |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Vanilla-Full | standard baseline | $W_\ell h_\ell$ | primary | reference | reference | invalid endpoint | 1--2 |
| Centered-Full | centering rival | $W_\ell(h_\ell-m_\ell)$ | primary | beats vanilla descriptively | no centering effect | invalid endpoint | 1--2 |
| Local-HMT | local-source hypothesis | local dynamic H/M/T | primary | below centered in both seeds | otherwise | invalid tracker | 1--4 |
| Relay-HMT | main hypothesis | block-1 dynamic H/M/T | primary | below all required controls | otherwise | invalid Relay/tracker | 1--6 |
| Relay-Random | bottleneck rival | fixed Haar mixing of current full PCA frame | decisive control | Relay-HMT below it | no stable advantage | mismatched compute/state | 1--6 |

Seeds are 17 and 29.  Each seed creates one deterministic step-0 model and
optimizer state shared bit-for-bit across its five jobs.  Data, dropout/RNG,
optimizer, schedule, load loss, untruncated capacity, milestones, and validation order are
paired.  Online spectral buffers are deterministic arm-specific state.

Registered milestones map to nearest optimizer steps and record actual tokens:
0; 64 (50,331,648); 127 (99,876,864); 318 (250,085,376); 636
(500,170,752); 1,272 (1,000,341,504); 2,543 (1,999,896,576); 5,086
(3,999,793,152); 7,629 (5,999,689,728); 10,173 (8,000,372,736); and
12,716 (10,000,269,312).

## 7. Primary Metric

For arm $A$, control $B$, seed $s$, and the same validation documents,

$$
\Delta_{A-B}^{(s)}
=L_A^{(s)}(10B)-L_B^{(s)}(10B).
$$

Negative favors $A$.  Report each seed separately with 2,000 paired-document
bootstrap replicates.  Equal-seed pooling is a summary only.  This metric
answers terminal quality at the registered budget; it does not establish
training efficiency or mechanism.

## 8. Secondary Metrics

- 8B--10B NLL slope and descriptive NLL AUC;
- tokens/theoretical FLOPs to fixed NLL;
- wall-clock and throughput including separately itemized statistics/eval;
- load, capacity drop, route entropy, and route disagreement;
- expert gradient conflict, output redundancy, and forced-expert regret;
- covariance/projector drift, principal angles, gamma, flip, margin change,
  target--deployment lag, and rejected refresh count;
- Relay gradient norm reaching block 1.

## 9. Known Good / Known Bad / Known Confusing Cases

- **Known good:** identity/no-update gives exact replay, zero flip, zero
  continuity score, and unchanged load.
- **Known bad:** independently updated $P_{64}$ and $P_{320}$ that violate
  nesting; direct target replacement; resume without spectral buffers.
- **Known confusing:** gamma zero or poor NLL is a scientific result, not an
  engineering failure; a random Relay may outperform without validating
  covariance identity.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Pass | Debug artifact | Handoff |
| --- | --- | --- | --- | --- |
| S0 provenance | sources/data/config frozen? | all hashes present | manifests | unit |
| S1 unit | algebra/state deterministic? | tests and contract validator pass | test logs | single GPU |
| S2 single GPU | forward/backward/refresh/checkpoint works? | five arms and resume close | smoke JSON | 8 GPU |
| S3 8-GPU | DDP identity and refresh work? | five arms, fresh/resume, rank equality | smoke ledger | full |
| S4 full launch | ten jobs accepted? | job IDs and frozen source hash | job ledger | monitor |
| S5 early monitor | real optimization and one refresh valid? | telemetry/TensorBoard/checkpoint visible | early evidence | later analysis |

## 11. Algorithm Specification

### 11.1 Running statistics

At step 0, set $\bar\Sigma_0=\widehat\Sigma_0$.  Refresh at steps
0,128,...,1,152,1,280 and then every 512 steps from 1,280 through the 10B
endpoint.  Each refresh replays the same statistics tokens in eval mode with
RNG restored before training resumes.  For $k>0$ use $\rho=0.1$.

### 11.2 Nested deterministic tracker

The state is a nested flag $(U_{64},U_{320})$.  Procrustes-align targets,
update the 320-space, transport the 64-target into it, then update the 64-space
inside the candidate 320-space.  Candidate gamma is searched in
$\{1,1/2,1/4,1/8,1/16,1/32,1/64,1/128,0\}$.  Local sources choose gamma per
source layer; each Relay source chooses one gamma jointly guarded across
blocks 2--4.  Sign/SVD/QR operations use deterministic float64 CPU kernels;
deployment buffers are cast to model device/dtype after validation.

Because the Gate is linear, deployment computes $W_\ell P_B$ once per
forward and applies that effective $8\times768$ weight to all tokens; it does
not materialize $P_Bx$ for every token.  This is algebraically and
gradient-equivalent to token projection, which is covered by a unit test, and
keeps the online method's per-token Gate order equal to the full baselines.

Every accepted candidate must satisfy projector symmetry/idempotence,
$P_H P_{320}=P_H$, ranks 64/320, and
$P_H+P_M+P_T=I$ within $10^{-6}$ relative error.

### 11.3 Continuity guard

High-confidence tokens are the top old-margin quartile per target Router.
Accept the largest gamma whose high-confidence flip is at most 0.01, maximum
expert share changes by at most 0.01, and

$$
R_{cont}=\mathbb E_{x\in\mathcal H}
\frac{\|C_E\Delta z(x)\|_2^2}{m_{old}(x)^2+10^{-6}}\le0.01.
$$

Low-confidence flip is recorded but not rejected.  Statistics, eigendecomposition,
Procrustes, QR, gamma selection, and guards are non-differentiable.  Gamma zero
retains the old deployed flag.

### 11.4 Random Relay

For each seed, deterministically sample one full 768-dimensional Haar frame
$R_s$ and persist it.  At each refresh form target frame $U^*_kR_s$, take its
first64 and first320 directions, and pass the identical nested tracker and
guard.  The source, gradients, dimensions, refreshes, statistics, and state
cost match Relay-HMT.

### 11.5 Checkpoint and milestone contract

Every checkpoint contains model, optimizer, scheduler, RNG, sampler cursor,
running centers, covariance EMA, deployed and target flags, Haar frame,
refresh counters, gamma/guard state, and milestone completion state.  Every
milestone writes per-document NLL plus route/load/projector/gradient telemetry
and runs the registered expert-function evaluators with separate wall-clock
accounting.  TensorBoard mirrors all scalar trajectory fields.  Aggregation
may be rerun from any milestone without training.

## 12. Success / Failure / Insufficient Evidence

All engineering-valid arms train to 10B regardless of early performance,
load, flip, or gamma.  Relay-HMT is supported only under the ordering in
Section 0.  It is not supported if any required comparison lacks stable
two-seed evidence or Relay-Random matches it.  Missing pairing, corrupt or
inexact resume, non-nested projectors, data leakage, incomplete terminal jobs,
or missing per-document endpoint evidence is insufficient.

NaN/Inf, OOM/communication failure, data-hash drift, irrecoverable checkpoint,
rank-state divergence, projection reconstruction failure, or unreconstructable
artifacts stop for engineering repair.  Repairs may not alter arms, data,
thresholds, seeds, schedule, or primary metric.

## 13. What This Cannot Claim

The run cannot establish universal semantic H/M/T, generality beyond this
model/data/scale, compositionality, or expert specialization as the unique
cause of terminal quality.

## 14. Review Notes And Protocol Changes

- 2026-08-03: user approved the full five-arm design and 5090-8-spot profile.
- 2026-08-03: clarified that block 1 remains trainable; only source-layer
  identity is fixed.
- 2026-08-03: continuity is computed on the top-margin quartile with threshold
  0.01; nested flags update jointly; 10B remains the early point of the
  validated 100B cosine horizon; TensorBoard and complete milestone evidence
  are mandatory.
