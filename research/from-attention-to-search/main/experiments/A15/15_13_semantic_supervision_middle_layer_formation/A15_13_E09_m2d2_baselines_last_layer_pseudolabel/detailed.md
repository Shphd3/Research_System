# Detailed: A15_13_E09 M2D2 Baselines And Last-Layer Pseudo-Label Routing

Primary Anchor: [A15_13_04](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_04_m2d2_causal_lm_semantic_routing_anchor.md)  
Frozen Protocol and registered revision: [protocol.md](protocol.md), SHA-256 `44c82a3094d9ba5ca839fb48688fc1e8804c25b5c4efabb3f7510f1165c9b6cd`  
Summary: [summary.md](summary.md)  
Result eligibility: `ELIGIBLE`; `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`

## 0. Quick Recap

Purpose: add strong simple Baselines and test whether labels discovered from the frozen final layer can train a useful causal semantic Router.  
Direct result: the pseudo-label hierarchy beat the strongest new simple Baseline by `0.001841 [0.001684,0.002003]` NLL, had held-out fine-domain NMI `0.237`, and had positive deletion and wrong-expert costs.  
Registered verdict: `PASS_PSEUDO_METHOD`.  
Boundary: the result supports a practical offline-teacher route, not online clustering or superiority over the reused staged task-only hierarchy.

## 1. Terminology And Definitions

| Term | Plain meaning | Concrete computation | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- |
| Token NLL | how surprised the model is by the correct next token | mean `-log p(target)` over positions 64--255, nats/target token | primary task endpoint; lower is better | semantic routing |
| Frozen final-layer teacher | the Base model's strongest available whole-window semantic summary | mean of final-normalized `hidden_states[-1]` over all 256 positions | constructs labels without human domain names | online causal availability |
| Direction-plus-radius label | a cluster based on projected direction and log vector norm | rank-64 train-only PCA, then 3 parents and 3 children per parent | registered unsupervised supervision | optimal clustering |
| Route NMI | naming-invariant route/domain association | normalized mutual information over confirmation target-token routes and gold fine domains | semantic dispatch | task gain or expert use |
| Matched macro-F1 | route classification quality after label-name alignment | mapping learned on development; scored on confirmation | readable semantic accuracy | causal value |
| Deletion cost | reliance on the selected child | deleted-child NLL minus intact NLL | expert use | correct semantic choice |
| Wrong-child cost | whether children are interchangeable | mean wrong-child NLL minus intact NLL | expert specialization | global task superiority |

## 2. Anchor Link And Decision Point

E07 showed that gold semantic loss increased route semantics and expert non-interchangeability but worsened NLL versus its task-only topology. E08 showed a small hard-Oracle benefit when the correct semantic path was forced. E09 asks whether the architecture survives stronger ordinary Baselines and whether an unsupervised final-layer teacher can turn the idea into a trainable method.

## 3. Protocol Freeze, Conformance, And Deviations

| Registered item | Expected | Actual | Status | Evidence | Eligibility impact |
| --- | --- | --- | --- | --- | --- |
| Approval | implementation, smoke, two-seed full run, reuse-only old models, analysis | explicitly approved before execution | Pass | Protocol approval ledger | none |
| Data | balanced M2D2 Wikipedia 3-by-3, fixed split | 9,216 train, 2,304 development, 4,608 confirmation windows | Pass | dataset SHA and teacher-state shapes | none |
| Task | sequence 256; first 64 context; last 192 next-token CE | exact registered mask | Pass | runtime and evaluation arrays | none |
| Frozen Base | Qwen3-0.6B-Base and language head frozen | only block-14 added modules optimized | Pass | parameter and checkpoint audit | none |
| Pseudo-label leakage | train-only fitting; gold only for audit | no gold passed to PCA, clustering, restart choice, or Router training | Pass | cluster implementation and saved assignments | none |
| Causality | online Router cannot read future tokens | flat and direct-nine max future-suffix error `0.0`; staged Router inherited E07 causal path | Pass | `guards/causal_future_invariance.json` | none |
| Seeds and completion | seeds 17 and 29; every fixed endpoint complete | 8 one-stage endpoints plus 4 pseudo-stage endpoints; 38 new evaluation files | Pass | corrected completion audit | none |
| Old models | reuse only | E07/E08 files recorded with immutable SHA-256 values; no old training invoked | Pass | `reuse/e07_e08_manifest.json` | none |
| Figures | four registered figures | all four generated; a fifth cluster-method figure added after the primary verdict | Pass plus post-hoc presentation | figure directory | fifth figure is descriptive only |
| Completion display | show both pseudo stages | first audit version displayed only the canonical stage-two count, although both histories/checkpoints existed | Corrected after root-cause audit | stage-one/stage-two histories and 16 passing tests | no training or statistic changed |
| Platform status lookup | terminal ACP status should be retrievable | current local SCO client rejected a new server workspace field; run artifacts and pipeline completion are intact | Operational limitation | job `pt-1htaqunm`; completion audit | no scientific eligibility change; platform terminal label not independently re-read |

No condition was retried, excluded, or selected using confirmation performance. The post-run completion-audit correction only reports both real pseudo stages explicitly. The post-run figure addition reruns the frozen analysis and does not alter a registered metric or verdict.

## 4. Actual Setup

### Data and task

- Culture and the arts: Mass media, Performing arts, Visual arts.
- Health and fitness: Exercise, Nutrition, Public health.
- Natural and physical sciences: Biology, Earth sciences, Physical sciences.
- Per fine domain: 1,024 train, 256 development, and 512 confirmation windows.
- Sequence length: 256. Positions 0--63 are context only. Positions 64--255 contribute standard next-token cross-entropy.
- Coarse and fine names never appear in model input.

### Model and added capacity

| Condition | Added structure | Active rank/token | Stored adapter parameters | Router parameters | Supervision |
| --- | --- | ---: | ---: | ---: | --- |
| Dense rank 24 | one always-on adapter | 24 | 98,304 | 0 | next-token only |
| Flat task-only rank 24 | 9 leaf adapters, learned top-1 Router | 24 | 884,736 | 9,225 | next-token only |
| Flat gold rank 24 | same flat topology | 24 | 884,736 | 9,225 | next-token plus gold 9-way route loss |
| Direct-nine hierarchy | shared + 3 parent + 9 child rank-eight adapters; one global 9-way Router | 24 | 425,984 | 9,225 | next-token plus gold 9-way route loss |
| Pseudo-label hierarchy | shared + 3 parent + 9 child rank-eight adapters; parent then conditional child Router | 24 | 425,984 | 12,300 | next-token plus unsupervised route loss |

Every original Qwen parameter and the tied language head remained frozen. The intervention is at zero-indexed block 14. The online Router reads the uncentered block-14 state at each token position. It never reads the offline final-layer teacher state.

### Clustering

The teacher averages all 256 final-normalized frozen-model states in each window. A rank-64 principal-component basis is fitted on train only. The registered clusterer fits three direction-plus-log-radius parent clusters, then three children within each parent, using 20 deterministic restarts, at most 100 expectation-maximization iterations, tolerance `1e-5`, and train likelihood for restart selection. Direction-only and diagonal Gaussian hierarchies are label-quality diagnostics only.

### Training behavior

| Training block | Genuinely staged? | Trainable objects | Frozen objects | Data passes / optimizer updates | Objective | Handoff |
| --- | --- | --- | --- | --- | --- | --- |
| Dense, flat, direct-nine conditions | no | all added adapters and available Routers | Base and language head | 4 passes / 288 updates | next-token CE; route CE added where registered | fixed update 288 |
| Pseudo stage one | yes, stage 1 | shared adapter, parent experts, coarse Router | Base, language head, child experts, fine Router | 2 passes / 144 updates | next-token CE + unit-weight pseudo-coarse route CE | save exact stage-one adapter state |
| Pseudo stage two | yes, stage 2 | shared adapter, child experts, fine Router | Base, language head, coarse Router, parent experts | 2 passes / 144 updates | next-token CE + unit-weight pseudo-child route CE | load stage one; reset optimizer/scheduler; fixed update 144 |

All blocks use microbatch 8, accumulation 16, effective batch 128 windows, AdamW learning rate `3e-4`, weight decay `0.01`, clipping `1.0`, five-update warmup, cosine decay, and seeds 17 and 29. Fixed final checkpoints are primary; development never selects a checkpoint. Route cross-entropy only differentiates Router parameters, while language loss trains the active adapter path and any differentiable route-probability coefficient.

## 5. Metrics And Registered Decision Rules

1. **Task gate:** the method must beat the strongest newly trained simple Baseline in both seeds, and the paired 10,000-draw bootstrap lower bound must be above zero.
2. **Semantic-route gate:** pseudo-trained confirmation routes must have positive fine-domain NMI; matched macro-F1 and load statistics explain the pattern but cannot replace the task gate.
3. **Expert-function gate:** deleting or replacing the selected child must increase confirmation NLL in both seeds and have a pooled 95% lower bound above zero.

Resampling preserves condition/seed pairing and samples windows within each of nine domains. Windows, not tokens, are the independent units used by the bootstrap. No post-hoc non-inferiority margin is used.

## 6. Evidence Lineage

| Claim or decision | Protocol criterion | Raw artifact | Computation | Observed value | Eligibility | Verdict | Limitation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Pseudo task gate | strongest simple Baseline minus method positive in both seeds and pooled lower bound | per-window confirmation NPZ arrays | equal-domain mean; 10,000 paired draws | `+0.001841 [0.001684,0.002003]`; seeds `+0.002524`, `+0.001158` | Eligible | Pass | Baseline is strongest simple topology, not reused task-only hierarchy |
| Direct-nine task comparison | same rule | same | same | `+0.002375 [0.002215,0.002535]` | Eligible | Pass | uses human gold route labels |
| Final-layer semantic accessibility | positive held-out cluster/domain association | frozen teacher arrays and assignments | train-fit assignment; confirmation NMI | registered `0.444`; direction-only `0.457`; diagonal Gaussian `0.524` | Eligible diagnostic | Positive | topical domains and offline full-window access |
| Pseudo semantic dispatch | positive route/domain association | per-token causal route arrays | seed mean NMI and development-mapped confirmation macro-F1 | NMI `0.237`; F1 `0.336` | Eligible diagnostic | Pass | less aligned than gold direct-nine routing |
| Pseudo expert function | positive deletion and wrong-child costs | paired confirmation intervention arrays | 10,000 paired within-domain draws | delete `+0.000932 [0.000853,0.001011]`; wrong `+0.000485 [0.000417,0.000552]` | Eligible | Pass | effects are small and do not prove correct routing |
| Pseudo versus same staged topology | descriptive boundary, not registered primary contrast | reused task-only and new pseudo arrays | mean NLL difference | pseudo is worse by `0.000903` | Eligible descriptive | No pseudo-loss gain | supervision and training labels differ; topology is comparable |
| Learning efficiency | no large language-fitting slowdown at matched updates | per-update train histories for flat task-only and pseudo hierarchy | two-seed mean; 12-update moving curve; final 24-update mean | pseudo `2.5001`, flat `2.5008`; held-out NLL also lower for pseudo | Post-hoc diagnostic | No large observed penalty | does not measure wall-clock, FLOPs, or strict sample-efficiency equivalence |

## 7. Main Results

### Task performance

| Condition | Seed 17 NLL | Seed 29 NLL | Mean NLL |
| --- | ---: | ---: | ---: |
| Frozen Base | — | — | `2.969889` |
| Dense rank 24 | `2.887650` | `2.887588` | `2.887619` |
| Flat task-only rank 24 | `2.883765` | `2.882457` | `2.883111` |
| Flat gold rank 24 | `2.890229` | `2.890138` | `2.890184` |
| Reused staged task-only hierarchy | `2.880171` | `2.880564` | `2.880368` |
| Reused shuffled hierarchy | `2.882454` | `2.882218` | `2.882336` |
| Reused learned semantic hierarchy | `2.881524` | `2.881320` | `2.881422` |
| Direct gold-nine hierarchy | `2.880942` | `2.880532` | `2.880737` |
| Pseudo-label hierarchy | `2.881241` | `2.881299` | `2.881270` |
| Reused hard common control | `2.879200` | `2.878953` | `2.879077` |
| Reused hard random control | `2.880279` | `2.879964` | `2.880121` |
| Reused hard semantic Oracle | `2.877732` | `2.877409` | `2.877571` |

The flat task-only model is the strongest newly trained simple Baseline in both seeds. Both new hierarchies beat it. The pseudo hierarchy is also slightly better than the reused learned-semantic hierarchy, but slightly worse than the reused task-only staged hierarchy. Thus the positive result is “practical semantic structure without losing to simple Baselines,” not “semantic supervision is the sole cause of the best NLL.”

### Route semantics

| Condition | Mean fine-domain NMI | Mean matched macro-F1 | Load entropy | Largest route share |
| --- | ---: | ---: | ---: | ---: |
| Flat task-only | `0.007` | `0.047` | `0.245` | `0.722` |
| Flat gold-nine | `0.366` | `0.534` | `0.958` | `0.181` |
| Reused staged task-only | `0.180` | `0.142` | `0.527` | `0.404` |
| Reused learned semantic | `0.265` | `0.451` | `0.971` | `0.176` |
| Direct gold-nine hierarchy | `0.370` | `0.545` | `0.960` | `0.173` |
| Pseudo-label hierarchy | `0.237` | `0.336` | `0.874` | `0.227` |

The pseudo labels create real held-out domain association, but do not recover the semantic agreement of gold supervision. Load entropy is reported separately because balanced use is not semantic alignment.

### Expert interventions

| Condition | Delete selected expert | Replace selected expert |
| --- | ---: | ---: |
| Flat gold-nine | `+0.079705` | `+0.049408` |
| Direct gold-nine hierarchy | `+0.002780` | `+0.002346` |
| Reused learned semantic hierarchy | `+0.001292` | `+0.000737` |
| Pseudo-label hierarchy | `+0.000932` | `+0.000485` |

Every reported intervention increases NLL. The pseudo child bank therefore participates in prediction and is not freely interchangeable, but its intervention effect is weaker than the gold-supervised controls.

## 8. Visualization Results

### Strict task contrast

![Strict simple-Baseline contrasts](figures/02_strict_baseline_contrasts.png)

Purpose: test the registered held-out task gate.  
Metric: strongest simple Baseline minus method NLL; positive favors the method.  
How to read: the pseudo point and its interval are fully above zero.  
Take-home: the pseudo hierarchy beats the strongest simple Baseline under the registered rule.  
Cannot prove: that pseudo supervision beats the same staged topology without semantic loss.

### Causal route semantics

![Route semantic diagnostics](figures/03_route_semantics.png)

Purpose: separate semantic dispatch from task performance.  
Metric: confirmation fine-domain NMI and development-mapped macro-F1, both from 0 to 1.  
How to read: pseudo routing is clearly above flat task-only routing, but below gold-supervised routing.  
Take-home: unsupervised labels transfer domain information into the causal Router.  
Cannot prove: expert utility or NLL gain.

### Expert function

![Expert intervention costs](figures/04_expert_utility.png)

Purpose: test whether the selected expert has functional consequences.  
Metric: NLL increase after deletion or replacement; positive is harmful.  
How to read: both pseudo bars are above zero, although smaller than the gold controls.  
Take-home: pseudo-trained experts are not freely interchangeable.  
Cannot prove: that the Router always chooses the semantically correct expert.

### Offline final-layer clustering

![Final-layer cluster-method comparison](figures/05_teacher_cluster_methods.png)

Purpose: test whether the registered unsupervised label generator is the best of the audited candidates.  
Metric: confirmation fine-domain NMI after train-only fitting; higher is better.  
How to read: diagonal Gaussian is highest at `0.524`; the trained direction-plus-radius source is `0.444`.  
Take-home: the final layer contains clear domain-readable structure, but the registered clusterer is not optimal.  
Cannot prove: that a diagonal-Gaussian-trained Router will improve NLL; that requires a new training comparison.

### Matched-update language fitting

![Matched-update language-loss trajectories](figures/06_learning_efficiency.png)

Purpose: check whether adding two-stage pseudo-semantic routing visibly slows ordinary language-loss fitting.  
Metric: training next-token cross-entropy, averaged over two seeds and smoothed across 12 optimizer updates; shading is the two-seed range.  
How to read: the pseudo and flat task-only curves remain close across 288 updates and end at nearly the same level; the dashed line marks the pseudo model's real stage transition.  
Observed result: final 24-update mean is `2.5001` for pseudo and `2.5008` for flat task-only; pass-four means are `2.5038` and `2.5048`.  
Take-home: no large language-fitting efficiency penalty is visible under matched updates, while the pseudo model has stronger semantic routing and lower held-out NLL than this simple Baseline.  
Cannot prove: faster wall-clock training, equal compute, strict sample-efficiency equivalence, or superiority over the same staged task-only hierarchy. This analysis was requested after the registered verdict and is secondary.

### Four-model matched-update language fitting

| Condition | Pass-four train CE | Final-24-update train CE | Confirmation NLL |
| --- | ---: | ---: | ---: |
| Single dense rank-24 LoRA | `2.5119` | `2.5078` | `2.887619` |
| Flat task-only rank-24 experts | `2.5048` | `2.5008` | `2.883111` |
| Final-layer pseudo-label hierarchy | `2.5038` | `2.5001` | `2.881270` |
| Direct gold-nine hierarchy | `2.5028` | `2.4986` | `2.880737` |

![Four-model matched-update language-loss trajectories](figures/07_four_model_learning_curves.png)

Purpose: place the user-requested single adapter, flat task-only experts, pseudo-label hierarchy, and direct gold hierarchy on one matched-update training plot.  
Metric: two-seed mean next-token training cross-entropy smoothed over 12 optimizer updates; shading is the seed range.  
How to read: the four trajectories finish in a narrow band; the dashed line is a stage boundary only for the pseudo model.  
Take-home: the pseudo hierarchy shows no large visible language-fitting slowdown and has lower confirmation NLL than both simple Baselines.  
Cannot prove: strict optimization equivalence, equal wall-clock or floating-point cost, or that semantic supervision causes the small NLL differences. This is a post-hoc descriptive audit.

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | Status | What this rules out | What remains live |
| --- | --- | --- | --- | --- |
| Final-layer extraction | three split files, fixed shapes, train-only fit | Pass | missing teacher object | full-window topical shortcut |
| Clustering | all nine leaves nonempty; saved fit and assignments | Pass | unusable pseudo-label construction | imbalance and cluster-method choice |
| Pseudo stage one | 144 updates in each seed | Pass | missing coarse handoff | imperfect coarse clusters |
| Pseudo stage two | exact stage-one load; frozen coarse Router and parent experts; 144 updates | Pass | continuous/non-staged training explanation | shared-adapter drift and label noise |
| Causal evaluation | future-suffix error zero; complete arrays | Pass | future-token leakage in online routing | offline teacher is still non-causal |
| Task gate | positive in both seeds and pooled lower bound | Pass | simple Baseline sufficiency | same-topology task-only remains slightly better |
| Semantic and function gates | positive route association and both interventions | Pass | labels ignored or experts unused | strength is below gold controls |

The main surviving rival is now narrower: hierarchical capacity and staged optimization may explain the NLL advantage over flat Baselines, while pseudo labels mainly add interpretable routing. E09 does not isolate a positive NLL contribution from pseudo semantics because the reused same-topology task-only model remains better.

## 10. Claim Boundary

Can claim: final-layer whole-window outputs expose M2D2 domain structure without labels; the registered labels can train a causal semantic Router; the resulting model passes the strict simple-Baseline NLL gate and both functional gates.

Cannot claim: online deployable clustering, abstract semantic discovery, native Base geometry improvement, total-parameter-matched superiority, universal domain benefit, or a pseudo-supervision NLL gain over the same staged task-only architecture.

## 11. Next Decision

Proposed decision, awaiting researcher confirmation: do not train another Router yet. Reuse cached frozen states to audit candidate teacher layers and direction-only, direction-plus-radius, and diagonal-Gaussian clustering with train-only fitting and development-only selection. The current confirmation split has already been opened for the post-hoc cluster-method comparison, so a method chosen from that table cannot obtain a fresh confirmatory verdict on the same split. Freeze one layer-and-clusterer choice first; only then decide whether a two-seed Router run with a new untouched holdout is warranted.

## 12. Artifact Manifest

| Artifact | Purpose | Identity | Complete | Claim eligible | Notes |
| --- | --- | --- | --- | --- | --- |
| Full run | all new checkpoints, arrays, logs, analysis | `/data/250010109/MoE_Router/experiments/20260902_a15_13_e09_m2d2_baselines_last_layer_pseudolabel/runs/full-20260902T023805Z` | yes | yes | ACP job `pt-1htaqunm` |
| Dataset | frozen processed M2D2 tensors | SHA `8cd04d99...51a8` | yes | yes | `/data/250010109/datasets/m2d2_wikipedia_3x3/processed/m2d2_3x3_seq256.pt` |
| Reuse manifest | prove old models were not retrained | `reuse/e07_e08_manifest.json` | yes | yes | SHA for every reused evaluation/checkpoint source |
| Teacher and labels | final-layer arrays, cluster fits, assignments | `teacher_states/`, `pseudo_labels/` | yes | yes | train-only fit boundary |
| Aggregate | primary estimates, diagnostics, typed verdict | SHA `56404356...2509fe` | yes | yes | deterministic analysis seeds |
| Completion audit | completeness, stage counts, causal guard | SHA `527aa97b...98d2e` | yes | yes | `complete: true`, no missing paths |
| Curated tables | NLL and route metrics | local `tables/` | yes | yes | copied from full run after audit |
| Curated figures | decision reading path | local `figures/` | yes | as labeled | cluster-method figure is post-hoc presentation |
| Post-run analysis revision | add cluster comparison figure only | `e09_analysis.py` SHA `d0e12c13...f0a8c` | yes | as labeled | all registered estimates recomputed unchanged |
| Post-run audit revision | report both 144-update pseudo stages | `completion_audit.py` SHA `10f2c708...f4f88` | yes | yes | reporting correction; no model change |
| Learning-efficiency audit | matched-update train language-loss trajectory | two-model figure SHA `dccdbb18...3a7f2`; four-model figure SHA `cc945c74...d12c`; local CSV tables | yes | secondary only | post-hoc; no model selection or verdict change |

## 13. Links And Reproduction

- Worker code: `/data/250010109/MoE_Router/experiments/20260902_a15_13_e09_m2d2_baselines_last_layer_pseudolabel`
- Full result root: `/data/250010109/MoE_Router/experiments/20260902_a15_13_e09_m2d2_baselines_last_layer_pseudolabel/runs/full-20260902T023805Z`
- Submission entry: `MODE=full DRY_RUN=0 ALLOW_SUBMIT=1 PROTOCOL_APPROVED=1 bash submit_h100_4_reserved.sh`
- Resource: one reserved four-H100 ACP node, one independent single-GPU worker per new condition shard; no distributed model training.
