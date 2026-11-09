# Protocol: A6 post-training routing-to-function decision tree

## 0. Approval Snapshot

Document status: `APPROVED_FOR_IMPLEMENTATION_SMOKE_CONDITIONAL_FULL_RUN`  
Approval status: researcher explicitly requested the complete decision-tree analysis, a four-GPU submission, supervision to completion, result analysis, and a self-contained story on 2026-09-08.  
Block audit status: `CONFIRMED`; all numerical defaults below are inherited from the researcher-approved decision-tree document.  
Cross-block consistency: `PASS_PENDING_IMPLEMENTATION_SMOKE`.  
Execution scope approved: S0--S3; S4 and S5 only when their frozen trigger is met; S6 is a separate continual-learning experiment and is not authorized by this run unless S5 first supports local conditional growth and a new resource amendment is recorded.  
Design frozen at: the scientific body in Sections 0--16 of this file.  
Purpose: locate why A6 structural routing changed task performance by separating teacher information, routing probability, selected path, expert function, and local learning compatibility.  
Primary Anchor: `15_13_10_sae_flat_router_functional_anchor.md`; this is a child analysis of A6, not a competing design.  
Anchor decision question: did the frozen SAE/GMM prior create useful functional specialization, merely alter routing, or impede task learning?  
Experiment role: root-cause audit followed, only when triggered, by a bounded local-capacity comparison.  
Primary metric: S1 paired answer-token NLL; later stages use diagnostic-panel routing relations and paired loss interventions without replacing S1.  
Claim boundary: internal held-out and post-hoc mechanism evidence only; no clean benchmark, semantic-causality, continual-learning, or universal capacity claim.  
Minimal setup: five conditions x three seeds at update 512, common frozen D/F panels, then isolated copies for short updates.  
Treatment and controls: four A6 regularized conditions; matched A5 `task_only`; within-model no-op, ablation, expert replacement, and conditional R/U/C/G controls.  
Changed variable: only the registered intervention or short-update parameter subset at each stage.  
Held fixed: backbone, data, record IDs, causal positions, teacher definitions, load bias during evaluation/short updates, checkpoints, output coefficient semantics, and all original A5/A6 artifacts.  
Pass: a stage's registered relation or effect satisfies its frozen direction, interval, and size rule.  
Fail: the registered opposite effect is measured or an implementation parity gate fails.  
Insufficient: missing data, invalid parity, inadequate fixed-panel support, or an interval crossing the decision region.  
Cannot claim: that routing structure itself is expert utility, that an oracle replacement is deployable, or that local growth is continual learning.  
Approval decision: execute without repeated approval questions inside the stated decision tree and resource ceilings.

## 1. Definitions

- `task_only`: the three completed A5 online task-loss runs with trainable router, reused only after identity/parity checks.
- `sae_a`, `gmm_a`, `sae_b`, `gmm_b`: the twelve completed A6 regularized trajectories.
- \(h_t\): final-layer MLP pre-input at causal position \(t\), predicting target token \(t+1\).
- \(p_t=\operatorname{softmax}(Wh_t+c)\): unbiased routing probabilities.
- \(k_t=\arg\max_e(z_{te}+b_e)\): actual route after frozen balance bias \(b\).
- \(k_t^0=\arg\max_e z_{te}\) and \(a_t=p_{t,k_t}\): unbiased route and actual selected coefficient.
- `D`: discovery half of development; `F_route`, `F_transfer`, `F_growth`: disjoint probe thirds of the other half; `U`: training support.
- `diagnostic panel`: at most 64 records per task and at most four causal answer positions per record. It is not the complete S1 test.
- \(\delta=0.001\) nat/answer-token: predeclared practical-effect threshold for S3--S5, not a universal standard.

## 2. Alignment and tested uncertainty

A6 directly found whether online structural regularization helps task NLL. It did not establish where an effect enters the chain

\[q\;\rightarrow\;p\;\rightarrow\;k\;\rightarrow\;E_k(h)\;\rightarrow\;\text{task loss}\]

or whether future learning should reuse, reroute, or isolate capacity. This protocol tests those missing links in order. A stop at any frozen branch is an informative completion, not an incomplete attempt.

## 3. Hypotheses and strongest rivals

- H1: the teacher contains non-constant relations and regularization transfers them to \(p\) and/or \(k\).
- H2: changed paths correspond to input-dependent expert-function differences under fixed coefficients.
- H3: if a persistent weak group remains, local updates reveal either beneficial sharing, interference, routing failure, or capacity-limited adaptation.
- Rival R1: the teacher is uninformative at these positions.
- Rival R2: only probability magnitudes change; discrete paths do not.
- Rival R3: experts are interchangeable or the shared branch carries the effect.
- Rival R4: existing experts or router can solve the local weakness under the same update/replay budget.

## 4. Immutable inputs and provenance

- A6 run: `/data/250010109/MoE_Router/experiments/20260908_online_sae_gmm_regularized_router/runs/full-20260908T183139Z`.
- A5 run: `/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z`.
- Data SHA256: `58e409ca9d903d146c9ae8e3cee834a4eb5f0e6f2e24de4fe521349d05e527f2`.
- SAE SHA256: `e4e2049aced8ba9a3b043bbb2b3308b497b7ec22f107531e37197873ee545b65`.
- Backbone: frozen Qwen3-0.6B-Base, layer 27, dimension 1024.
- Adapter: one shared rank-16 branch plus eight rank-16 experts, scale 1/8, Top-1 with unbiased selected probability coefficient.
- Seeds: 17, 29, 43; checkpoint: update 512 unless a stage explicitly requests an existing earlier checkpoint.

All original data, checkpoints, source, evaluations, and receipts are read-only. New writes go under the isolated analysis workspace and a unique A6 `analysis/<run-id>/` result directory.

## 5. Data construction and unsealing

For each development record, use its stable record ID as `group_id`; known cross-rewrite family metadata is unavailable, so cross-rewrite independence remains unknown.

1. D/F: parity of the first byte of `SHA256("A6-analysis-v1|" + group_id)`; even is D, odd is F.
2. F stage: integer `SHA256("A6-probe-v1|" + group_id)` modulo 3 maps to route, transfer, growth.
3. Within each panel, sort each task by `SHA256(panel-key + "|" + record_id)` and keep at most 64.
4. Keep the first causal answer prediction position plus up to three positions selected by a private stable hash. No target text affects selection.
5. D choices and candidate locks are written before the corresponding F artifact is read by the selection code.

No test record enters candidate selection, short updates, or threshold tuning.

## 6. Metrics and uncertainty

S1 NLL is total answer loss divided by total answer tokens. Seed is the independence unit for the original treatment comparison; all seed values and paired differences are shown.

S2 uses teacher entropy/max probability, \(KL(q\|p)\) for A, the original attraction/repulsion terms for B, loads, coefficient summaries, bias override, and

\[C_{same}=\frac{\sum s_{ij}\mathbf1[k_i=k_j]}{\sum s_{ij}},\quad
C_{diff}=\frac{\sum(1-s_{ij})\mathbf1[k_i=k_j]}{\sum(1-s_{ij})},\quad C_{rel}=C_{same}-C_{diff}.\]

Pairs are fixed before model comparison, cross-record only, at most 20,000. Zero denominators are `undefined`.

S3--S5 resample records within task 1,000 times and recompute token-weighted paired effects. Each seed is separate. Prespecified single comparisons use 95% intervals; the four-cell S4 matrix uses 98.75% cell intervals. Improvement requires interval lower bound \(>\delta\); damage requires upper bound \(<-\delta\) when expressed as before-minus-after; practical equivalence requires the complete interval inside \([-\delta,\delta]\). Everything else is uncertain.

## 7. Stage contract

| Stage | Goal | Exact operation | Gate / branch | Required artifact |
|---|---|---|---|---|
| S0 | establish eligibility and intervention fidelity | authenticate five conditions; verify init/schedule/optimizer semantics; reload-forward parity; validate tail reconstruction on at least two conditions and two checkpoints | parity failure invalidates affected intervention; cache-only failure falls back to full forward | `eligibility.json`, `input_manifest.json`, `tail_cache_parity.json` |
| S1 | establish task effect | reuse complete update-512 test records; compute paired NLL, per-task values, and normalized development AUC | descriptive direction; never a mechanism verdict | four tables and two figures |
| S2 | locate routing change | same D/F-route positions for q, p, k, k0, a, relation metrics, answer/structural/all-position load | run S3 only when teacher is informative and probability/path relation is changed enough to explain | three tables plus stage status |
| S3 | test current function | specialized/shared deletion; fixed-coefficient all-eight replacement; self-replacement parity; choice gap and D-locked group/expert contrasts | self-parity must pass; S4 if functional, eligible group candidate remains; S5 if unused old capacity is demonstrated | ablation, counterfactual, contrast, and gap artifacts |
| S4 | test local learning compatibility | D-lock one group pair; independent 0/1/8-step expert-only updates from each checkpoint; fixed routes, coefficients, shared branch, bias and backbone | proceed to S5 only for supported interference, persistent learning failure, or prior S3 routing failure | lock, transfer matrices, invariance and cost artifacts |
| S5 | choose reroute/reuse/grow | common 16-step 50/50 target/replay schedule; K, evidence-triggered R, mandatory U; C/G only if U is insufficient or capacity is the registered rival | report gain-damage-cost frontier; local conditional growth support requires G over C/U plus gate ablation | learning curves, gain-damage-cost, gate and initialization artifacts |
| S6 | separate continual-learning test | not part of this execution unless a later amendment authorizes new tasks, time order, and resources | `NOT_RUN_OUT_OF_SCOPE` is the correct state here | stage status only |

## 8. S0 implementation gates

Tail cache reconstructs selected target logits as

\[\operatorname{Head}(\operatorname{Norm}[r_t^0+S(h_t)+a_tE_{k_t}(h_t)]).\]

\(r_t^0\) is the frozen final-layer output without either adapter branch. The implementation must prove that the injection is in the last layer and no later token-mixing module exists. Compare full and reconstructed selected-token losses for at least: `task_only` and `sae_b`, update 0 and 512, at least four records each. Acceptance: identical target IDs and routes, max absolute selected-token loss error \(\le 2\times10^{-3}\) in deployed precision. Otherwise S3 uses full forward.

## 9. S1 frozen analysis

Report five conditions x three seeds, paired regularized-minus-task-only deltas, equal-seed mean/sample SD, all eight task deltas, and trapezoidal AUC over updates 0/128/256/384/512 divided by 512. Missing final evaluation is insufficient; no interpolation or best-checkpoint selection.

## 10. S2 frozen analysis

Compute both SAE and GMM q on the fixed causal states; the SAE nonzero retained-mass mask is common coverage. Report first-answer and later-answer positions separately. B comparisons are permutation-invariant; no fixed expert-ID accuracy is a B verdict. Actual path change is registered when a regularized condition's F-route \(C_{rel}(k)\) differs from matched task-only by at least 0.02 in the same direction for at least two seeds, or when bias override changes this relation by at least 0.02. Smaller effects are recorded but do not independently justify S4.

## 11. S3 frozen analysis

For each condition and seed on F-route:

\[D_E=L_{no\ expert}-L_{native},\qquad D_S=L_{no\ shared}-L_{native}.\]

For every selected position save fixed-coefficient target loss under each expert. Self-replacement must match native tail loss within the S0 tolerance. Define

\[G_{fixed}=\operatorname{mean}_t[\ell_{t,k_t}-\min_j\ell_{t,j}].\]

On D, lock at most two teacher-group/expert contrasts by largest cross-group reversal with at least 16 records per group; evaluate those only on F-route. A functional candidate requires self-parity, \(D_E\) or a locked group-dependent reversal beyond \(\delta\), and enough S4 support/probe records. Oracle minima are diagnostic lower bounds only.

## 12. S4 frozen short update

Select \(c^*\) by the smallest three-seed mean S1 NLL among the four regularized arms, tie order `sae_a,gmm_a,sae_b,gmm_b`, and write the lock before F-transfer access. Use its teacher for both models. High-confidence record group: maximum q at least 0.6 and top-minus-second at least 0.2 at the first covered answer position.

Using task-only seed 17 D, find teacher-group pairs sharing one actual expert, with at least 16 U and D records per group. Keep at most two by common occupancy, then use update-8 D exploration to choose one pair by two diagonal gains \(>\delta\) and largest worst cross-damage; ties use group IDs. If none qualifies, S4 ends `NO_ELIGIBLE_CONFLICT_CANDIDATE`, not `NO_CONFLICT`.

Each source-group update starts from an isolated copy, updates only actually routed old experts with AdamW lr \(2\times10^{-4}\), weight decay 0, clip 1.0, at most eight support records per step, fixed order cycling, and checkpoints 0/1/8. Router, shared branch, bias and backbone remain bitwise invariant. Confirm on F-transfer only after lock.

## 13. S5 frozen local alternatives

Enter when S3 supports unused old-expert capacity, S4 supports generalizing cross-damage, or a fixed weak group fails to learn under S4. Use at most 32 target U records, 32 conflict-retain records, and 32 background records. Every update has four target and four replay records and minimizes the equally weighted token-normalized losses. Run 16 updates; report 0/1/4/8/16 without probe-based early stopping.

- K: no update.
- R: update only old router; if direct task loss cannot exploit S3 gap, one separately labeled support-only oracle-label classifier diagnostic is allowed.
- U: update only routed old experts.
- C: freeze old system, add same-rank zero-output correction with learned scalar gate initialized at 0.5.
- G: same correction initialization plus learned input gate initialized at 0.5.

C/G are opened only if U is insufficient or capacity is the registered rival. Initialization must reproduce K within S0 tolerance. Retain damage upper interval must be \(\le0.001\) nat/token. G supports conditional local growth only if it improves the registered gain-damage tradeoff over U and C, and replacing its learned gate by the D mean degrades F-growth beyond \(\delta\). Otherwise stop without S6.

## 14. Preflight, smoke, resources and outputs

Before submission: unit tests for split/hash selection, causal positions, token-weighted metrics, permutation invariance, self replacement, branch deletion, copy isolation, and allowed-parameter masks; compile check; CPU synthetic smoke; GPU parity on the real model. Full scale-up requires all applicable gates pass.

Submit one job requesting the approved reserved four-H100 profile `n6ls.iu.i40.4` in `share-space/share-cluster`, using image `registry.cn-sh-01.sensecore.cn/lepton-trainingjob/ngc-pytorch:25.06-cu12.9-py3.12-ubuntu24.04`. Parallel workers may partition conditions/seeds, but all read the same frozen manifests. Ceiling: S0--S3 at most 2 GPU-hours, S4 another 2, S5 another 4. Stop with recoverable artifacts at the applicable ceiling; no setting change or sweep.

Machine-readable `stage_status.json` records `NOT_STARTED`, `RUNNING`, `COMPLETE`, `STOPPED_BY_DECISION_RULE`, `INSUFFICIENT`, or `FAILED_IMPLEMENTATION`. Raw execution material remains in the execution workspace. Canonical `summary.md` and `detailed.md` are written beside this protocol only after evidence is complete.

## 15. Verdict mapping

- S1 answers only task effect.
- S2 can establish information presence and route relation, not expert utility.
- S3 can establish current intervention dependence and group-dependent relative expert effects, not future learning.
- S4 can establish bounded local learning transfer under the specified optimizer and budget, not global gradient conflict.
- S5 can establish a local reroute/reuse/growth tradeoff, not continual learning or universal necessity of capacity.
- Any parity failure, unsupported group, or interval spanning decision regions yields `INSUFFICIENT`, never a favorable reinterpretation.

## 16. Cannot claim

No stage can identify a true semantic class from teacher labels alone, infer utility from routing agreement, convert target-aware oracle routing into a deployable score, claim clean external generalization, or treat S5 as evidence for unseen-task continual learning. Frozen shared parameters mean U failure cannot prove all old capacity is exhausted.

## 17. Approval, freeze, and amendment ledger

- 2026-09-08: the researcher approved the complete analysis chain in `A6_post_training_analysis_decision_tree_cn.md`, requested a four-GPU execution, supervision through completion, final analysis, and a self-contained story. Conditional stop branches remain part of the approved complete chain.
- 2026-09-08: original A5/A6 artifacts declared read-only; all short updates must operate on isolated state copies.
- Frozen scientific-body SHA256: `5435b040c9a82006de95bea8c65e59e59f1254869422565c963ec7e51a30e3b1`. The body is every byte before the Section 17 heading; this ledger is append-only.
