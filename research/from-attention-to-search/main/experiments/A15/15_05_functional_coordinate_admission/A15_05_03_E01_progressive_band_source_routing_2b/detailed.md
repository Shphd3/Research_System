# Detailed: A15_05_03_E01 Progressive Band Source Routing

Primary anchor: [A15_05_03](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_05_functional_coordinate_admission/subanchors/15_05_03_progressive_band_source_routing_anchor.md)  
Protocol: [protocol.md](protocol.md)  
Summary: [summary.md](summary.md)  
Chinese summary: [summary_cn.md](summary_cn.md)

## 0. Quick Recap

**Question:** did prior models fail to show hierarchical expert differentiation
merely because they were not explicitly routed through progressively deeper
covariance bands?  
**Intervention:** after a common 0.629B-token checkpoint, route blocks 2/3/4
through H64/M256/T448 from either each block's local Router input or a shared
block-1 source; compare both with a full-input native Router.  
**Direct result:** local-HMT was worse than native. Relay-HMT was slightly
better at the 2B endpoint in both paired continuations, but paid a large early
adaptation cost and had worse NLL AUC. Expert diagnostics changed, but did not
form a coherent specialization profile.  
**Typed verdict:** `specialization_only_without_quality_pass`.

## 1. Terms and Metrics

| Term | Plain meaning | Computation / unit | Decision role | Cannot prove |
| --- | --- | --- | --- | --- |
| native full | each Gate reads its complete 768-d local input | original Gate forward | matched quality reference | optimal routing |
| local-HMT | blocks 2/3/4 read local H64/M256/T448 | frozen branch projectors | depth-specific band treatment | semantic hierarchy |
| layer1-relay-HMT | blocks 2/3/4 read H/M/T from the same block-1 output | frozen branch projectors after RMS normalization | shared shallow-source treatment | covariance-specific value without random control |
| held-out NLL | average surprise on the correct next token | negative log probability, nat/token; lower is better | primary terminal quality | mechanism |
| NLL AUC | average held-out NLL over matched continuation tokens/FLOPs | trapezoidal curve integral divided by interval length, nat/token | training-efficiency support | asymptotic quality |
| route disagreement | fixed tokens assigned to another expert than native | fraction of token routes | manipulation check | benefit |
| load entropy | closeness of expert counts to uniform | entropy divided by \(\log 8\), range \([0,1]\) | collapse guard | function |
| forced-expert route regret | selected-expert loss minus the best forced-expert loss | nat/token; lower is better | route--utility binding | globally optimal routing or specialization alone |
| gradient conflict | whether held-out groups ask one expert to move oppositely | median gradient cosine and negative-pair fraction | within-expert compatibility | final quality |
| output redundancy | similarity of different experts on fixed tokens | mean pairwise expert-output cosine | functional differentiation | correctness |

For treatment \(a\) and the paired native model,

\[
\Delta L_{a:native}=L_a^{heldout}(2B)-L_{native}^{heldout}(2B).
\]

Negative values favor the treatment. Confidence intervals use 2,000 paired
document bootstraps within each continuation; the two continuations remain the
replication units.

## 2. Objective Judgment of the Hypothesis

The motivating claim was plausible but incomplete. A native full-input Router
does not implement the proposed H→M→T schedule, so absence of schedule-shaped
routes cannot refute what an explicit schedule would do. However, forcing a
schedule can generate route differences even when its coordinates are
functionally arbitrary. The decisive requirement was therefore not route
differentiation but paired held-out quality plus an independent functional
metric under matched load and compute.

The experiment supports only the weak clause: explicit scheduling does cause
route and functional changes. It rejects the strong clause that this omission
was the sufficient reason useful hierarchy was absent. Neither treatment
improved NLL over the full matched trajectory, and the expert evidence was not
coherently more differentiated.

## 3. Model, Branch, Data, and Training

| Item | Registered value |
| --- | --- |
| architecture | H768, 4 Transformer blocks, 8 sparse + 1 shared expert, top-1 |
| expert width | 1,536 |
| Router | linear Gate, running center, load-balancing coefficient 0.01 |
| branch | step 800; 629,145,600 nominal tokens |
| endpoint | step 2,544; 2,000,683,008 nominal tokens |
| post-branch exposure | 1,744 optimizer steps; 1,371,537,408 nominal tokens |
| replicas | continuation seeds 17 and 29; three arms paired within seed |
| training corpus | DCLM `global-shard_01_of_10` |
| sequence / batch | sequence 1,024; local batch 12/GPU; global batch 768 |
| hardware | one 8×RTX5090 SPOT node per arm/replica |
| optimizer | AdamW; LR \(10^{-4}\); betas (0.9,0.95); weight decay 0.01 |
| schedule | warmup 636; common 100B-token cosine horizon |
| precision / parallelism | BF16; ZeRO-1 |
| held-out evaluation | 1,024 fixed, disjoint DCLM documents × 1,024 tokens |
| diagnostic labels | 1,344 WOS abstracts; domain/topic results not used for verdict |
| active parameters | 152,108,800; same across arms |

Experts always received the complete local expert input. Only the Gate view
changed. All arms computed the same parameter-free block-1 source and matched
projection path, so measured median microbatch time differed by at most 0.45%.

## 4. Spectral Treatments

At the branch checkpoint, independent calibration tokens fitted source means
and covariance projectors. H64 denotes ranks 1--64, M256 ranks 65--320, and
T448 ranks 321--768. The source artifact was frozen during continuation.

| Arm | Block 1 | Block 2 Gate | Block 3 Gate | Block 4 Gate |
| --- | --- | --- | --- | --- |
| native-full | local full | local full | local full | local full |
| local-HMT | local full | local H64 | local M256 | local T448 |
| layer1-relay-HMT | local full | block-1 H64 | block-1 M256 | block-1 T448 |

Frozen expert-constant logit offsets matched each treatment's branch-time
expert marginal load to native without token-dependent information or
trainable parameters. The offset did not erase the intervention: final mean
block-2--4 route disagreement remained 7.12% for local and 19.70% for relay.

Artifact SHA-256:
`ba310373fc532b849f33056e4f40bf3418b7d98defba76f8798fe6f98e2f5ea3`.
Evaluation-token SHA-256:
`5c8cca2b0821f25b8e7abc50d7653dfba8d71e9ccf167fee61b82624116a52e4`.

## 5. Protocol Compliance

- exact branch model/optimizer/scheduler/data cursor: **passed**;
- exact-resume smoke, parameter/logit/top-1/NLL identities: **passed**;
- six registered full runs, 2.000683B tokens each: **passed**;
- all 8 optimizer shards and four registered continuation milestones: **passed**;
- identical rank-0 batch hashes within each paired seed at all 1,744 steps:
  **passed**;
- no dead expert, no capacity drop, milestone load guards: **passed**;
- treatment route manipulation above 2%: **passed**;
- DCLM, WOS, forced-expert, conflict, redundancy, and displacement evaluators:
  **passed**;
- four rendered figures opened at original resolution: **passed**.

The initial collector mistakenly evaluated the absolute load threshold over
every post-branch step instead of the registered milestones. Local-HMT had a
short adaptation transient around steps 822--825 (entropy 0.917--0.921; maximum
share 0.267--0.269), then recovered before the first milestone. The collector
was corrected to the approved 954/1272/1908/2544 rule without changing any
threshold; full-trajectory extrema remain in the tables as diagnostics.

At registered milestones, the worst entropy was 0.9741 and maximum share was
0.1786. Treatment--native milestone differences were at most 0.0118 entropy
and 0.0168 expert share, within the 0.02/0.05 paired limits.

## 6. Held-Out Quality Results

### Milestone trajectory averaged over the two continuations

| Nominal tokens | native | local-HMT | relay-HMT |
| ---: | ---: | ---: | ---: |
| 0.629B | 5.325824 | 5.694439 | 5.710958 |
| 0.750B | 5.129080 | 5.146610 | 5.151905 |
| 1.000B | 4.816859 | 4.825770 | 4.824062 |
| 1.501B | 4.452030 | 4.456142 | 4.450954 |
| 2.001B | 4.248598 | 4.250772 | 4.246841 |

The step-800 treatment values evaluate the new routing view on the common
branch weights before adaptation. They quantify the immediate structural cost,
not an initialization mismatch.

### Final paired effects

| Comparison | seed 17 \(\Delta\) [95% CI] | seed 29 \(\Delta\) [95% CI] | equal-replica pooled |
| --- | ---: | ---: | ---: |
| local − native | +0.003809 [0.003252,0.004367] | +0.000539 [−0.000040,0.001163] | +0.002174 [0.001758,0.002590] |
| relay − native | −0.000971 [−0.001769,−0.000091] | −0.002542 [−0.003424,−0.001617] | −0.001756 [−0.002352,−0.001119] |
| relay − local | −0.004779 [−0.005587,−0.003957] | −0.003081 [−0.003940,−0.002201] | −0.003930 [−0.004504,−0.003343] |

### Matched-trajectory NLL AUC

| Arm | seed 17 | seed 29 | two-replica mean | mean difference vs native |
| --- | ---: | ---: | ---: | ---: |
| native | 4.644284 | 4.645553 | 4.644919 | 0 |
| local-HMT | 4.668197 | 4.667600 | 4.667899 | +0.022980 |
| relay-HMT | 4.665253 | 4.667286 | 4.666269 | +0.021351 |

Thus relay has a reproducible late endpoint advantage but fails the registered
training-efficiency support metric. Local-HMT is worse at the pooled endpoint
and throughout the curve.

## 7. Route, Load, and Functional Results

### Manipulation

Final route disagreement relative to the separately continued native model:

| Arm | seed | block 2 | block 3 | block 4 | mean blocks 2--4 |
| --- | ---: | ---: | ---: | ---: | ---: |
| local | 17 | 3.95% | 7.38% | 9.81% | 7.05% |
| local | 29 | 3.94% | 7.45% | 10.21% | 7.20% |
| relay | 17 | 7.54% | 17.14% | 34.52% | 19.73% |
| relay | 29 | 7.71% | 17.05% | 34.23% | 19.67% |

The intervention was strong and became larger with depth, particularly for
relay. This alone does not identify useful hierarchy.

### Expert-function diagnostics

| Metric (two-replica mean) | native | local | relay | Better direction |
| --- | ---: | ---: | ---: | --- |
| route regret, nat/token | 0.42485 | 0.42304 | 0.41726 | lower |
| negative gradient-pair fraction | 0.5000 | 0.4635 | 0.4844 | lower |
| expert-output cosine redundancy | 0.04844 | 0.04808 | 0.05130 | lower |
| expert utility dispersion | 0.45679 | 0.45930 | 0.42865 | higher for differentiated utility |

Relay lowers route regret in both seeds by 0.00871 and 0.00647 nat/token. It
therefore changes route--utility binding in a favorable direction. However,
its best-expert match rate decreases, utility dispersion decreases, output
redundancy increases, and gradient-conflict directions disagree between seeds.
This is not a coherent claim that relay produced more specialized experts.

Local lowers negative gradient-pair frequency and output redundancy in both
seeds and lowers route regret slightly, but does not improve held-out quality.
The protocol therefore labels the overall result specialization-only rather
than quality or training-efficiency Pass.

WOS domain route-label accuracy showed no replicated ordering: local exceeded
native in seed 17 but not seed 29. Topic accuracy was not improved. These are
descriptive routing labels, not functional outcomes.

## 8. Frozen-Basis Drift

At 2B, frozen/current band overlap across sources, layers, and bands ranged
from 0.522 to 0.854, with medians near 0.70. The branch projectors retained
substantial identity but were not current-spectrum projectors. The experiment
therefore establishes the effect of a **frozen branch subspace schedule**, not
continuous online spectral decomposition.

## 9. Visualization Contracts and Audit

### Figure 1: held-out NLL versus matched FLOPs

![Held-out NLL versus FLOPs](figures/figure1_heldout_nll_vs_flops.png)

- **Question:** did either treatment improve the whole learning trajectory?
- **Data:** five registered checkpoints, 1,024 held-out DCLM documents, both
  paired continuations.
- **Axes:** analytic cumulative FLOPs using \(6N_{active}\) per token; held-out
  NLL in nat/token, lower is better.
- **Allowed conclusion:** both treatments pay a large immediate cost; relay
  recovers late but has worse curve area.
- **Limitation:** sparse macro checkpoints do not identify per-step dynamics.

### Figure 2: final paired effects

![Final paired NLL effects](figures/figure2_final_paired_nll.png)

- **Question:** what is the 2B endpoint ordering?
- **Metric:** left-arm minus right-arm NLL with paired 95% document intervals.
- **Reading:** values below zero favor the left arm.
- **Allowed conclusion:** relay beats both native and local at 2B; local does
  not beat native.
- **Limitation:** endpoint advantage does not imply training efficiency.

### Figure 3: manipulation and load

![Manipulation and load guards](figures/figure3_route_and_load_guards.png)

- **Question:** did the treatment act while preserving valid expert load?
- **Panels:** mean block-2--4 route disagreement; minimum registered-milestone
  entropy; maximum registered-milestone expert share. Dark/light bars are
  continuation seeds 17/29; red dashed lines are the load thresholds.
- **Allowed conclusion:** both treatments changed routes, and all registered
  load guards passed.
- **Limitation:** balance does not imply expert usefulness.

### Figure 4: expert-function diagnostics

![Expert-function diagnostics](figures/figure4_expert_function_mechanisms.png)

- **Question:** did route changes correspond to coherent functional
  differentiation?
- **Panels:** route regret, gradient cosine, negative gradient-pair fraction,
  and output redundancy in their native units; the two connected points per
  arm are seeds 17 and 29.
- **Allowed conclusion:** relay route regret improves consistently; local has
  some conflict/redundancy improvements; no treatment improves all panels.
- **Limitation:** two continuations do not estimate a population variance, and
  no single diagnostic replaces NLL.

All four PNGs were opened at original resolution. Axes, units, zero/threshold
lines, treatment colors, confidence bars, and endpoint markers were visible;
no clipping or unreadable overlap was found.

## 10. Execution Record

All full jobs used `workspace=share-space`,
`AEC2=computing-cluster-5090-01g`, worker spec `n12lp.nn.i10a.8`, one node,
8×RTX5090, SPOT quota, normal priority.

| Replica | Arm | Job ID | Final state | Retry |
| ---: | --- | --- | --- | ---: |
| 17 | native | `om-uijjq8d1` | SUCCEEDED | 0 |
| 17 | local | `om-lbg7tkmr` | SUCCEEDED | 0 |
| 17 | relay | `om-jjulv1f5` | SUCCEEDED | 0 |
| 29 | native | `om-p6r3j8zf` | SUCCEEDED | 0 |
| 29 | local | `om-d0hzvcti` | SUCCEEDED | 0 |
| 29 | relay | `om-ictqfoza` | SUCCEEDED | 0 |

Final checkpoints contained all eight optimizer shards. Median microbatch time
was 0.224--0.225 seconds. The six final checkpoint hashes are listed in
[run_evidence.csv](tables/run_evidence.csv).

## 11. Smoke and Invalid-Attempt Ledger

The accepted six-arm smoke was `om-0dzvmd4b`; exact-resume smoke
`om-ihi56617` passed parameter, logit, route, NLL, optimizer, RNG, and batch
identity. Earlier attempts remain recorded rather than overwritten:

| Job | Reason invalidated |
| --- | --- |
| `om-gpacljss` | local blocks 3/4 failed the original load-comparability smoke |
| `om-i5nrcelr` | resume comparison used independent pre-step-801 trajectories |
| `om-t8nx9jhu` | stopped after the load-neutral runtime amendment changed source |
| `om-n7z45cqd` | continuation RNG was incorrectly reset on post-branch resume |
| `om-f7lbrgea` | restart-level CUDA nondeterminism violated exact resume |
| `om-6v8puner` | valid load smoke superseded by deterministic-kernel source freeze |
| `om-z53ksfle` | shared entrypoint was replaced while the job was reading it |

These are engineering/provenance failures, not scientific observations.

## 12. Evidence Ledger

| Evidence | Location | Status |
| --- | --- | --- |
| typed verdict | [verdict.json](tables/verdict.json) | complete |
| paired NLL | [pairwise_nll.csv](tables/pairwise_nll.csv) | complete |
| trajectory/AUC | [heldout_trajectory.csv](tables/heldout_trajectory.csv), [heldout_auc.csv](tables/heldout_auc.csv) | complete |
| route/load | [final_arm_summary.csv](tables/final_arm_summary.csv), [paired_load_guards.csv](tables/paired_load_guards.csv) | complete |
| expert mechanisms | [expert_mechanism.csv](tables/expert_mechanism.csv) | complete |
| expert updates | [expert_update_per_token.csv](tables/expert_update_per_token.csv) | complete |
| jobs/checkpoints/data | [run_evidence.csv](tables/run_evidence.csv), [run_guard.json](tables/run_guard.json) | complete |
| worker package | `/data/250010109/MoE_Router/experiments/20260802_a15_01_04_progressive_band_source_2b_5090` | retained |

Raw checkpoints, logs, telemetry, per-document arrays, routes, and evaluation
caches remain on the worker surface; they are not promoted into the research
mainline.

## 13. Claim Boundary

The causal comparison is restricted to two post-0.629B continuations from one
four-layer DCLM checkpoint. It tests frozen branch subspaces, not online PCA.
It cannot establish that H→M→T is the correct semantic order, that covariance
rank is better than an arbitrary equal-dimensional schedule, that the same
result holds from initialization or at larger depth, or that training
efficiency improved.

The late relay advantage is real for the registered endpoint and documents,
but its mechanism is unresolved. It may reflect a stable shallow bottleneck,
regularization, easier Gate optimization, or covariance identity. The missing
equal-rank random and alternative schedule arms prevent separating these
explanations.

## 14. Next Decision

Close fixed progressive HMT rank scheduling as a self-sufficient routing
principle. A future cross-layer candidate must first use a learned functional
coordinate and pass held-out expert utility or update-compatibility gates
against equal-rank random and wrong-layer controls before another matched
training run.
