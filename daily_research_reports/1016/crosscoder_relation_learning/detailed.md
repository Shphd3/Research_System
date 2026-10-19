# Detailed: CrossCoder relation-to-learning R1

[Chinese companion](detailed_cn.md). Primary [Anchor](sources/02_ANCHOR_关系分组到学习验证.md); [Protocol](protocol.md), executed revision R1.8 plus the separately registered R1.9 numerical control repair and R1.10 auxiliary diagnostic; [amendments](execution_amendments.md).

Processor: Codex /root. All authorized computation has completed and the four-H100 worker exited at2026-10-15T17:39:48Z. Researcher scientific approval and question closure are Unknown and unchanged. Engineering guards do not assign scientific PASS.

## 0. Purpose and evidence scope

The question is whether joint feature events contain organization beyond marginal frequencies, and whether the chosen organization yields better terminal expert allocation at fixed learning capacity/exposure. Frequency-only geometry, load, input composition, initialization and generic specialization are competing explanations. The structural rerun is post-observation exploratory. Learning uses source-file-disjoint adapter TRAIN/EVAL within original CrossCoder TRAIN origin; original-document independence is Unknown. A midpoint intervention identifies a finite local update effect, not a full trajectory mechanism.

## 1. Objects and definitions

| Object | Actual computation | Meaning and boundary |
| --- | --- | --- |
| Feature | One coordinate of the shared final14/F16384 CrossCoder latent; its positive gated value defines an event at a position | No semantic or knowledge identity is assumed |
| Frequency | D positive-event count divided by D eligible positions | Feature frequency, not target rarity or prediction difficulty |
| Relationship group | Connected community of the D positive-phi mutual-q10 graph | Selected statistical organization, not an established natural expert |
| Matched N | Membership permutation within10 D frequency-quantile bins, exact group sizes/per-bin composition | Continuous frequencies are only approximately matched; not every statistic is identical |
| Route | Hit-only D-standardized group score, one winner, D load-constrained K4 mapping | Only the decision uses one winner; every expert still receives the entire h |
| Conditional loss | Mean true next-token CE over each fixed feature's hit positions, followed by equal feature average | Overlapping conditional populations, not disjoint tasks or feature knowledge mastery |
| Local intervention | Actual vs within-frequency-bin exchanged donor labels with exact expert token counts | Probe routing and checkpoint fixed; no update enters formal training |

## 2. Frozen setup and conformance

Execution root R is `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/relation_learning/20261015T164000Z`; code root is the experiment's `analysis_tools/relation_learning`. The only new allocation is `pt-szeffn72`, envelope keys `h100-4-reserved` / `shphd-lite-0911`. Four full80GB H100s passed device/BF16 preflight. Existing recovery jobs were untouched. Time ceiling6h/24GPUh; local structural work has a60-minute wall ceiling.

| Contract | Actual owner/evidence | Eligibility |
| --- | --- | --- |
| Frozen base/CrossCoder/norm/head | Model/checkpoint identities in Protocol; cache buffer checks and training version guards | Required guards, not scientific evidence |
| Exact real objective and causal placement | `data_eval512/native_zero_guard.json`, `data/prefix_precision.json`; terminal residual before final norm/head | Native fullmodel32-position logits/CE exact; no early-layer claim |
| Same inputs/parameters/exposure | `config/formal_R1_8.json`, per-run `run_contract.json`, `metrics.jsonl` | K4/rank32,262144 total/65536 active, paired seeds/order |
| Actual budget |6120updates×256=1566720 targets per arm;9arms |12 drop-last epochs; fixed learning budget, not convergence |
| Data | TRAIN130712/128contexts; EVAL523136/512contexts | Different source files; original documents/duplicates Unknown |
| Fixed low/high |3916each; min20 EVAL hits; low3737supported,179insufficient including7zero |95.429% low coverage; all high supported |
| Saved stages |0/510/1530/3060/4590/6120 |Complete adapter/optimizer/RNG/order/counters; external-process resume NOT_QUALIFIED |
| Training telemetry | Token/update TB tags, resource/gradient/load and component timings | Serial GPU next-update weights+Adam replay exact |
| Structural controls | `structure/full_group_controls.csv`, `method.json`, `triple_counting_repair/` | Full conditional controls and sampled pipeline calibration are distinct |
| Auxiliary | `data/first_direction/` |Uncentered raw H removal; posthoc centering control separately registered |

Optimizer is AdamW lr0.001, betas(0.9,0.999), eps1e-8, weight decay0, gradient clip1. Nonzero down/zero up initialization is paired across arms. Frozen full151936-vocabulary head projects in BF16; adapters and CE useFP32. All source h, true targets and complete gated CSR are identical across arms. No inference BatchTopK or outcome-driven gate fitting.

## 3. Amendments, failures and non-reinterpretation

[Amendments](execution_amendments.md) are the full history owner. Key eligibility changes: raw-score F tie degeneracy was repaired D-only before learning; size2/3 exact IID replaced slow/rare conditional sampling while retaining its uniform target; sample observed/null use a common enlarged Monte Carlo budget; file-local offset collisions were distinguished from source identity; strict BF16 cross-shape event equality failed and was preserved, while fixed-shape future changes were exactly invariant and FP32 truncation event differences were zero. Native head comparison used identical matrix shapes. One count-only EVAL expansion raised low-support coverage before formal learning, preserving the old cache and all learning settings.

The sample strict empirical log-frequency statistic remains undefined where V has zero support. Its Jeffreys-smoothed successor is exploratory, not original confirmation. Rare triple rejection reached its fixed ceiling; the complete repaired version resamples every frozen graph's small-group controls with exact triple counting, never just the missing draws. A dynamic-module Numba cache import failed on the reserved node; a separate empty cache directory enabled a fresh JIT without changing scientific code/settings.

## 4. Aggregation and uncertainty

Structural T_a is group-equal one-to-one nonsingleton Jaccard matching. Full T_b averages actual V within-group log10-frequency SD minus conditional-control mean SD. Report both group-equal and member-weighted versions and group sizes. Fixed-margin sampled null has99scheduled draws over two chains (50/49),32nnz proposal burn-in and4nnz spacing including rejected self-loops. Three workers only parallelize scoring. Finite mixing diagnostics and stationarity arguments do not prove global mixing or IID draws. Approximate tail probabilities have resolution0.01; nominal FWER is not guaranteed. A sampled null does not calibrate the complete10.49M-position graph.

Sample support is D≥25hits/8contexts, pair joint≥5; full-cache support is D≥100hits/10blocks, joint≥10. Positive estimable phi and mutualq10 feed weighted greedy modularity in every observed/null rerun. Donor frequency bins use complete active-feature average log10(Dp) with p_floor1e-12 for D-zero features; only3TRAIN/9EVAL gated events have Dp=0. The guard and its fixed cuts are common across arms and were not changed after outcomes.

For learning, let a_i(t) indicate fixed feature i at EVAL position t. A feature's conditional loss is the mean CE over its n_i hit positions. The primary loss averages those means over the M pre-count-supported low features. Seed-specific R−F/R−N differences use the same positions/features.

Paired intervals group each four consecutive contexts into one block (128blocks). For paired per-position difference Δ_t and per-feature difference μ_i, the fixed-feature ratio linearization has block influence

\[
u_b=\frac{1}{M}\sum_i\frac{\sum_{t\in b}a_i(t)\Delta_t-n_{ib}\mu_i}{n_i},
\qquad \sum_bu_b=0.
\]

Here n_ib counts feature i hits in block b. Draw2000 multinomial block weights w and compute d*=d+Σ_b w_bu_b. Quantiles give an approximate conditional paired interval. This preserves overlap and within-block pairing; it is not exact recomputed-ratio bootstrap, document independence, population generalization or seed uncertainty. Show all three paired seeds separately.

Practical R gain is0.01nat/feature against both F/N and overall noninferiority tolerance0.01nat/token; direction must agree across three seeds. Also compare every arm with its original zero-adapter baseline. A less harmful condition is not an absolute learning gain. Low-frequency conditions are not inherently difficult; their measured baseline must be reported.

The local intervention uses16fixed donor/probe batches per arm/seed. Every frequency-bin/expert token count stays identical; preflight minimum exchanged fraction0.640625. Fixed midpoint3060 and SGD lr0.1 (numerically selected before effects) are common. Each512-position probe averages only globally supported low features occurring in that probe; its support differs across batches but is identical across the paired updates. Batch bootstrap describes these fixed donor/probe variations, not independent documents or seed uncertainty. Raw/norm-matched absolute improvements and actual−exchange contrasts must both be shown.

## 5. Evidence lineage

| Claim | Raw owner | Computation | Boundary |
| --- | --- | --- | --- |
| Full-group frequency comparison | `structure/full_repair_summary.json`, `full_group_controls.csv` | Full186/186groups,13807/13807members; same size/D mean | Exposed within-bin, post-observation |
| Group stability depends on weights/graph | `structure/recheck_summary.json`, `q10_q20_member_stability.csv` | Group/member/pair weighting | No robust natural expert partition inference |
| Beyond-margin sampled organization | `structure/triple_counting_repair/null_results.json` and99draw tables | Full sampled pipeline rerun | Approximate finite-chain, sample-only calibration |
| Learning comparison | Per-run eval arrays/JSON and analysis CSV | Paired seeds and same supported feature cohort | Fixed terminal allocation/budget, no rare-knowledge claim |
| Local update consequence | `intervention/seed_*/*/effects.csv`, `norms.csv` | Same state/data, exact token counts, norm control | Trained specialization and finite local step remain distinct |
| First-direction sensitivity | `data/first_direction/summary.json`, fixed edges/features | Same raw-v/heldout contexts, no-op verified | No common semantics or random-direction control |
| Centering rival | `data/first_direction/centering_control/` | Same v/H, retain original mean before frozen normalization | Posthoc operator decomposition, not training mechanism |

## 6. Actual result ledger and delivery

| Component | Completed evidence | Result and eligibility |
| --- | --- | --- |
| Full matched controls |186/186groups,13807/13807members |Strict full T_b−0.25147064dex group-equal/−0.15500075member-weighted; post-observation within-bin result |
| Sample pipeline null |99/99draws,50/49chain allocation, complete repaired controls |T_a0.195311 vs null mean0.039274, range0.033353–0.059838; smoothed T_b−0.067770 vs null mean+0.015066; approximate p0.01each/Holm0.02, no nominalFWER; strict sampleT_bNA preserved |
| Local relationship/partition |Same old counts/graphs |86.60%D edges retained; edgeJaccard0.764; full member-weighted communityJaccard0.322; q10→q20 pair retention0.383 |
| Formal learning |9/9complete,54saved states/9finals |Low R/F/N means3.358713/3.342884/3.352730 vs zero2.439615; overall3.864719/3.866344/3.872289 vs zero2.949104; H2 not supported under fixed contract |
| Local intervention |9/9runs,16batches each, raw/norm-matched |All9mean actual-minus-exchanged low-loss-decrease contrasts negative; R norm-matched−0.019405/−0.013705/−0.008306; some intervals crosszero; finite within-condition SGD only |
| Expert phenotype |36expert cells×3metrics |All cells harmed; no single expert contributes more than29%; primary-weight contributions sum exactly to complete damage |
| Raw first-direction removal |8186fit/8182measure positions |L0249.527→512.147; eventJaccard0.394; sensitivity only |
| Center-preserving control |Same fixed raw-v/H; original outputs exactly reproduced |L0232.604; original-eventJaccard0.819; projectionL0change−16.923 plus fixed-offset effect+279.543; all-layer reconstruction still worse |
| Response-component control |9/9final states, zero/full arrays exact |R overall full/constant-only/TRAIN-centered-only damage0.915616/0.175456/0.858384; interaction−0.118224. F/N same pattern. Reject this TRAIN-constant-response-dominates explanation; retain EVAL shift/other training rivals |

The full-cache matched result, sampled calibration and H2 low-frequency cohort are different populations. In particular sample support25/4096 does not calibrate the rarest feature tail. Do not transfer its p-value to the complete graph or to all H2 low features. Member-weighted null itself has weak negative dispersion contrast (mean−0.010646), weaker than observed−0.060562; it does explain part of frequency organization.

The response control is post-observation. Because adapters are linear, constant U_eD_eμ_e equals TRAIN mean response and adapter(mean TRAIN hidden). TRAIN-centered response may still have nonzero EVAL mean. Loss is not additive; interaction is reported explicitly. CrossCoder reference-mean projection and adapter response decomposition intervene on different objects and cannot be called one common mechanism.

This round tested three bridges: joint-input organization, bounded learning allocation, and a local update consequence. Its observations support bounded extra organization, weaken hard natural-partition claims, and do not support the registered relation-route learning advantage. The local intervention rejects its predicted advantage at this midpoint but does not identify the Adam trajectory cause. A single next AI-proposed readout checks whether damage varies with source on contexts unused by adapters, holding feature lists/common count-supported cohorts fixed; it does not identify source causation or authorize a new experiment.

No result is inferred from a planned endpoint. Checkpoints remain in execution; `checkpoint_manifest.json` lists54actual formal saves and rehashed identities. Registered family: `checkpoint_family_crosscoder_relation_learning_20261015t164000z`; saved smoke: `checkpoint_crosscoder_relation_learning_smoke_20261015t164000z`. Cache versions: `representation_crosscoder_relation_learning_20261015t164000z` and `_eval512_`version. [Current saved-state access check](../../../assets/checks/2026-10-15_crosscoder_relation_learning_saved_states.json) passed. Figures and small CSVs carry origin manifests in this report directory. Raw contexts, full caches, matrices and weights are excluded from the discussion package; their addresses remain in the reproducibility entry.

Original result files and the preceding discussion package were preserved. No skills, unrelated dirty artifacts, Git commits/pushes, external messages, Focus or scientific state transitions were made.
