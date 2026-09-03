# Protocol: A15_13_E04 Frozen Teacher, Router-Only Supervision, and Dynamic Expert Tree

## 0. Approval Snapshot

```text
Document status: APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_TWO_SEED_FULL_RUN
Approval status: direct researcher approval on 2026-08-31
Block audit status: A-G CONFIRMED
Cross-block consistency: PASS
Execution scope approved: Focus/Anchor/Protocol revision, implementation, unit tests, smoke, 4xH100 reserved two-seed full run, analysis, local result records
Design frozen at: amended and re-frozen after the 2026-08-31 Router audit
Purpose: test whether Router-only correct or frozen-third-layer supervision organizes an added effective second-layer representation through parent-first expert growth
Primary Anchor: A15_13 semantic supervision of effective middle representations
Anchor decision question: does correct Router supervision improve a frozen-teacher hierarchy over the architecture-identical next-token-only hierarchy?
Anchor physical prior tested: learn the parent split first, freeze it, then learn a local child split inside each parent
Anchor core model term tested: h2_eff = h2 + selected-probability-scaled parent residual + selected joint-probability-scaled leaf residual
Anchor falsifier: Hier-Oracle does not reproducibly improve TEST-OOD true parent-conditioned fine q05 margin over Hier-NoReg
Experiment role: method construction and minimal mechanism falsification
Primary metric: worse-parent TEST-OOD fifth-percentile normalized true fine-label margin on h2_eff
Claim boundary: added effective representation only; original h2 and all teacher parameters remain frozen
Minimal setup: repaired four-rule language data, one joint three-layer teacher per seed, six core conditions, three Oracle ablations
Treatment: Router-only Oracle or frozen-h3 pseudo-label cross entropy during coarse and fine growth
Controls: matched Hier-NoReg, Vanilla-Flat, Flat-Oracle, and Flat-Pseudo; FullRoute, SequentialExpert, and JointCoarse Oracle ablations
Changed variable: topology, Router supervision source, fine-Router input, leaf-expert input, or coarse freeze, one registered comparison at a time
Held fixed: teacher, data order, initialization family, total steps, optimizer, schedule, final-step checkpoint, analysis, and truth boundary
Pass: both seed deltas positive, pooled paired one-sided 95% lower bound > 0, and all language guards pass
Fail: both seed deltas <= 0 or pooled paired 95% upper bound <= 0 with all guards valid
Insufficient: mixed seed direction, interval overlaps zero, or any teacher, pseudo-label, fairness, completeness, test-seal, or language guard fails
Cannot claim: original Block 2 formation, complete coarse-information removal, native expert utility, functional specialization, open-domain semantics, or scale transfer
Approval decision: execute autonomously without another design review; do not commit, push, publish, or add unregistered losses or branches
```

Confirmed Focus: [0830 active Focus](/daily_research_reports/backup/2026/08/0830/focus_semantic_supervision_middle_layer_separability.md). Primary Anchor: [A15_13 Anchor](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/15_13_semantic_supervision_middle_layer_formation_anchor.md).

## 1. Terminology And Definitions

- **Original second-layer state, $h_2$:** the frozen output of Transformer Block 2 before any E04 module.
- **Effective second-layer state, $h_{2,\mathrm{eff}}$:** $h_2$ plus the selected added residual-expert outputs. It is the only representation that E04 can change.
- **Answer-prefix state:** the hidden state at the last position before the query answer token. Router labels and the primary representation metric use this position only.
- **Vanilla-Flat (`VF`):** one shared residual expert, one four-way Router, and four leaf residual experts trained only by next-token prediction.
- **Flat Oracle/Pseudo (`VF-O`, `VF-P`):** the identical Flat architecture and initialization, with four-leaf Router cross entropy from truth or frozen nested $h_3$ labels.
- **Hierarchy without semantic regularization (`H-NR`):** the same parent-first 1-to-2-to-4 architecture as the supervised hierarchy, trained only by next-token prediction.
- **Oracle hierarchy (`H-O-*`):** the hierarchy whose Routers receive generator truth labels.
- **Pseudo-label hierarchy (`H-P-RP-FZ`):** the main hierarchy whose Routers receive labels frozen from third-layer clustering without truth access.
- **Residual fine routing:** the coarse Router reads $h_2$, while the fine Router reads $r_2=(I-P_C)h_2$.
- **Parallel expert input:** parent and leaf experts both read original $h_2$ and their residual outputs add in parallel.
- **Sequential expert input:** the leaf expert reads $h_2+E_c(h_2)$.
- **Frozen coarse path:** the coarse Router, parent experts, and $P_C$ cannot update during fine training.

## 2. Anchor Alignment

The experiment tests the smallest causal link needed by the current direction: whether correct semantic supervision acting only on Routers can organize the representation created by newly added modules beyond the identical topology trained by language loss alone. The strongest rival is generic adaptation. The matched no-regularization hierarchy isolates supervision, and the flat system isolates topology. Pseudo-label and mechanism ablations are interpreted only after the Oracle link.

## 3. Tested Hypotheses

1. **Primary:** `H-O-RP-FZ - H-NR > 0` on the primary metric with both seeds and language guards.
2. **Coarse removal:** `H-O-RP-FZ - H-O-FP-FZ > 0`, where `R` means residual fine-Router input and `F` means full $h_2$ input.
3. **Expert input:** `H-O-RP-FZ` is not worse than `H-O-RS-FZ`, where `P` is parallel and `S` is sequential expert input.
4. **Topology:** `H-NR - VF > 0` tests whether parent-first growth itself helps.
5. **Pseudo source:** `H-P-RP-FZ - H-NR > 0` and has the Oracle direction only if the pseudo-label entrance passes.
6. **Freeze mechanism:** `H-O-RP-FZ - H-O-RP-JT` is secondary. A JointCoarse win cannot support the fixed-coarse mechanism.
7. **Matched Flat supervision:** `VF-O - VF` and `VF-P - VF` test label supervision without hierarchical growth; `H-O-RP-FZ - VF-O` and `H-P-RP-FZ - VF-P` compare topology under the same label source.

## 4. Rival Explanations

| Rival | Separating comparison or guard |
| --- | --- |
| Added parameters or more language updates explain the result | `H-O-RP-FZ` versus parameter- and step-identical `H-NR` |
| Hierarchical topology alone explains the result | `H-NR` versus `VF`; Oracle versus `H-NR` |
| Semantic labels help any four-way Router equally | `VF-O` versus `VF`, then `H-O-RP-FZ` versus `VF-O`; analogous frozen-pseudo contrasts |
| Any final-layer partition is semantic | truth-free stability, paraphrase, balance, and post-freeze permutation-alignment entrance |
| Fine improvement is caused by serial extra depth | parallel versus sequential expert input |
| Joint optimization rather than fixed coarse growth is responsible | FrozenCoarse versus JointCoarse |
| Probe geometry improves while language behavior breaks | full-sequence NLL, answer NLL, and answer-accuracy guards |
| Hidden truth leakage selects pseudo labels | clustering API and durable receipt forbid truth fields until assignments freeze |

## 5. Data Construction And Provenance

E04 reuses the immutable repaired E02-v2b data rather than regenerating a result-sensitive variant. Its registered SHA-256 is `586f53b12289beebe90f81fa1ecf33b7e865898613f3782e0c5452ec5751caca`.

The source process is four affine functions over $\mathbb Z_{11}$: leaves `0..3` are $u+1$, $u+3$, $-u+3$, and $-u+1$. Parent $c=0$ contains positive-slope rules and parent $c=1$ contains negative-slope rules; within-parent child $f$ distinguishes offsets. One semantic group fixes the rule, three demonstrations, and query, then renders four surface paraphrases. No $c$, $f$, or leaf label is visible.

| Split | Groups | Rows | Role |
| --- | ---: | ---: | --- |
| TRAIN | 25,000 | 100,000 | teacher, experts, Routers, pseudo centers, probes |
| DEV-ID | 2,000 | 8,000 | teacher capability audit |
| DEV-OOD | 2,000 | 8,000 | shared probe regularization and guards |
| TEST-ID | 3,000 | 12,000 | confirmation auxiliary |
| TEST-OOD | 6,000 | 24,000 | primary untouched confirmation |

Semantic keys are disjoint across splits. OOD splits use held-out complete template combinations. Truth may train Oracle Routers and evaluate all frozen systems. It may not construct, select, stabilize, permute, or freeze pseudo labels. Data preflight must reproduce counts, class balance, group completeness, no semantic-key overlap, no visible-label leakage, and the registered hash.

## 6. Learning Task And Permitted Supervision

The permitted visible input is the complete causal sequence prefix. The required language output is every next token; the primary task loss averages cross entropy over all non-padding next-token positions. The query answer depends on both parent and child rule attributes.

Stage 1 permits no coarse/fine labels, answer weighting, clustering, classifier, or auxiliary loss. Stage 2 permits truth only for Oracle Router cross entropy and permits frozen third-layer targets only for Pseudo Router cross entropy. `VF` and `H-NR` receive no route labels; `VF-O` and `VF-P` receive only four-leaf Router targets. Every route target is placed only at the answer-prefix position. Experts never receive a label-prediction head; they update only through selected-sample language loss.

## 7. Model, Architecture, And Frozen Variants

The teacher is a three-block causal decoder: vocabulary from the frozen generator, width 256, eight attention heads, SwiGLU width 1,024, rotary positions, pre-normalization, tied embedding/language head, maximum length 64, and zero dropout. Stage 1 jointly updates embeddings, all blocks, final normalization, and tied language head. At Stage 1 completion, all teacher parameters freeze.

Each residual expert returns only $E(h)=W_\mathrm{up}\operatorname{SiLU}(W_\mathrm{down}h)$; $W_\mathrm{up}$ starts at zero, making every E04 model exactly teacher-equivalent at initialization.

**Hierarchy:** two rank-64 parent experts, four rank-64 leaf experts, one linear two-way coarse Router, and two parent-conditional linear two-way fine Routers. Coarse and fine $\arg\max$ select exactly one predicted parent and leaf. The selected parent residual is multiplied by $p_c(c^*\mid h_2)$ and the selected leaf residual by $p_c(c^*\mid h_2)p_f(f^*\mid c^*,h_2)$. Thus the discrete selection is hard, the selected probability supplies Router gradients, and only selected experts receive language gradients.

After coarse training, $w_C=W_c[1]-W_c[0]$, $P_C=w_Cw_C^\top/\lVert w_C\rVert^2$, and $r_2=(I-P_C)h_2$. Main `H-*-RP-FZ` uses residual fine routing, parallel expert input, and frozen coarse path. `H-O-FP-FZ` changes only fine-Router input to full $h_2$; `H-O-RS-FZ` changes only leaf input to the selected parent-updated state; `H-O-RP-JT` keeps coarse Router and parent experts trainable during fine training.

**Vanilla-Flat family:** one rank-43 shared residual expert, four rank-85 leaf residual experts, and one linear four-way Router. With selected leaf probability $p(l^*\mid h_2)$, the state is $h_2+E_s(h_2)+p(l^*\mid h_2)E_{l^*}(h_2)$. All Flat variants train for the sum of coarse and fine steps. `VF` uses no semantic Router loss; `VF-O` and `VF-P` use truth or frozen nested pseudo four-leaf cross entropy.

Adapter parameters are 196,608 for both hierarchy and the intended flat match to within 512 parameters. Active adapter rank is 128 in both. The implementation audit includes Router parameters and multiply-adds; total trainable parameters and active expert compute must differ by at most 1%.

## 8. Training Objective And Optimization

The teacher minimizes only

$$
L_{\mathrm{NTP}}=-\frac{1}{N_{\mathrm{valid}}}\sum_t\log p(x_{t+1}\mid x_{\le t}).
$$

`VF` and `H-NR` minimize only $L_{\mathrm{NTP}}$. Oracle/Pseudo coarse training minimizes

$$
L=L_{\mathrm{NTP}}+0.1\,\operatorname{CE}(G_c(h_2),q_c),
$$

and fine training minimizes

$$
L=L_{\mathrm{NTP}}+0.1\,\operatorname{CE}(G_f^{(q_c)}(r_2),q_f).
$$

Here $q_c$ selects which parent-conditional fine Router receives label loss, while the predicted $c^*,f^*$ still selects the expert path used by $L_{\mathrm{NTP}}$. `VF-O` and `VF-P` use $L=L_{\mathrm{NTP}}+0.1\operatorname{CE}(G_{\mathrm{flat}}(h_2),q_{2c+f})$. FullRoute substitutes $h_2$ for $r_2$. The fixed shared coefficient is $\lambda_{\mathrm{route}}=0.1$ for all Oracle and Pseudo conditions; it is not calibrated per condition or after results.

AdamW uses learning rate $3\times10^{-4}$, betas $(0.9,0.95)$, weight decay 0.1, global batch 256, 5% linear warm-up followed by cosine decay, gradient clipping 1.0, bfloat16 CUDA computation, and float32 loss. Teacher trains 8,000 fixed steps. Hierarchies train 1,500 coarse plus 2,000 fine steps. Every Flat variant trains 3,500 steps. There is no root-training stage because the frozen teacher is the shared trunk and Stage 2 begins when the parent split is added.

All primary results use the fixed final step. Intermediate 500-step checkpoints exist only for curves. Development losses cannot select different checkpoints.

## 9. Conditions, Seeds, And Checkpoints

Teacher seeds are 1701 and 2903. Each seed runs all conditions below from its own final teacher. Within a teacher seed, related architecture families use the same seed-derived module tensors wherever shapes match and the same deterministic batch order.

| Code | Route labels | Fine input | Expert input | Coarse in fine stage | Role |
| --- | --- | --- | --- | --- | --- |
| `VF` | none | four-way $h_2$ | parallel | n/a | fair flat baseline |
| `VF-O` | truth four-leaf | four-way $h_2$ | parallel | n/a | Flat Oracle control |
| `VF-P` | frozen $h_3$ four-leaf pseudo label | four-way $h_2$ | parallel | n/a | Flat pseudo control |
| `H-NR` | none | $r_2$ | parallel | frozen | hierarchical topology control |
| `H-O-RP-FZ` | truth | $r_2$ | parallel | frozen | main Oracle treatment |
| `H-P-RP-FZ` | frozen $h_3$ pseudo labels | $r_2$ | parallel | frozen | main pseudo treatment |
| `H-O-FP-FZ` | truth | full $h_2$ | parallel | frozen | coarse-removal ablation |
| `H-O-RS-FZ` | truth | $r_2$ | sequential | frozen | expert-input ablation |
| `H-O-RP-JT` | truth | $r_2$ | parallel | joint | coarse-freeze ablation |

There are two teachers and eighteen condition runs. Every teacher and condition saves `final.pt`; intermediate checkpoints never replace it.

## 10. Pseudo-Label Entrance

Normalized TRAIN answer-prefix $h_3$ is hierarchically divided by exact-balance spherical two-way clustering: one parent split, then one two-way child split inside each frozen parent. Independent two-way and four-way fits are forbidden. Use 16 deterministic starts, 20 complete-group bootstrap refits, at most 20,000 TRAIN groups, and temperature 0.1 for soft cross-entropy targets. Centers, assignments, and receipt must be durable before truth is opened; frozen centers alone assign every later split.

Entrance is interpretable as semantic only when both seeds satisfy all clauses:

1. each frozen leaf fraction lies in `[0.20, 0.30]`;
2. same-group paraphrase agreement is at least 0.90;
3. median group-bootstrap adjusted mutual information is at least 0.80;
4. post-freeze TEST-OOD best-permutation parent accuracy has bootstrap lower bound above 0.50;
5. post-freeze TEST-OOD best-permutation four-leaf accuracy has bootstrap lower bound above 0.25.

Failure does not cancel `H-P-RP-FZ`; it makes the run diagnostic and forbids calling any downstream change semantic. Alignment truth never changes assignments, centers, temperature, or condition training.

## 11. Primary Metric And Frozen Analysis Plan

For every final teacher and condition, retain raw $h_2$, $h_{2,\mathrm{eff}}$, true labels, group identifiers, template identifiers, Router probabilities, and selected experts for all registered splits. Raw $h_2$ is shared once per teacher; each condition saves its own effective state.

For each parent, normalize TRAIN effective states, fit an L2 binary logistic readout for true child $f$, and compute the signed logit divided by the readout-weight norm. Choose one regularization value from `C={1e-4,1e-3,1e-2,1e-1,1,10}` using `H-NR` DEV-OOD mean parent-balanced accuracy pooled across seeds; freeze it and reuse it for every condition. The per-seed primary score is the smaller parent-specific TEST-OOD fifth percentile.

For each registered contrast, resample 2,000 complete paraphrase groups within true parent, keep treatment/control paired, compute seed-specific effects, and pool seeds equally. Report percentile 95% intervals and the one-sided 95% lower bound. No rows are removed; incomplete or nonfinite rows make the contrast Insufficient. There is one ordered decision chain, so later comparisons are gated rather than multiplicity-rescued.

## 12. Secondary Metrics And Guards

1. Parent-specific within-class covariance trace normalized by dimension, and the change from raw $h_2$ to $h_{2,\mathrm{eff}}$.
2. Coarse and fine Router truth accuracy, entropy, per-route load, collapse rate, and selected-expert distribution.
3. Pseudo-label best-permutation accuracy, adjusted mutual information, stability, paraphrase agreement, and balance.
4. Full-sequence NLL in nat/token, answer NLL in nat/query, and answer accuracy.

For every treatment-control comparison, language guards require the paired pooled 95% upper bound of full NLL delta at most `+0.02`, answer NLL delta at most `+0.05`, and the answer-accuracy 95% lower bound at least `-0.01`. Secondary metrics cannot rescue a failed primary comparison.

## 13. Known Good, Known Bad, And Known Confusing Cases

- Known good: the teacher must reach DEV-ID answer accuracy at least 95%, DEV-OOD answer accuracy at least 85%, and frozen $h_3$ true-parent linear-probe balanced accuracy at least 80% in each seed.
- Known bad: visible-label leakage, a zero-norm $w_C$, any non-selected expert parameter update, or teacher-parameter change stops execution.
- Known confusing: high true-label readout from $h_3$ does not imply unsupervised discoverability; pseudo alignment is therefore a separate entrance.
- Identity: zero-initialized E04 modules must reproduce teacher logits and layer outputs within `1e-6` in FP32 and `5e-3` in BF16.

Unlike E02-R, no upper bound is imposed on raw $h_2$ separability. The new question permits an already readable $h_2$ and asks whether $h_{2,\mathrm{eff}}$ becomes better than fair controls.

## 14. Scientific Procedure And Stage Contracts

| Stage | Goal | Input and operation | Why | Output | Pass / stop | Artifact and handoff |
| --- | --- | --- | --- | --- | --- | --- |
| P0 | verify immutable data and scope | reproduce hash, counts, labels, group and split audits | prevent shortcut or drift explanations | data audit | any mismatch stops | `data_audit.json` -> Teacher |
| P1 | learn one common language model | train all three blocks for 8,000 steps on full-sequence NTP only | establish frozen semantic source without label help | two final teachers and full states | either teacher gate fails: stop Stage 2 | `teachers/<seed>/final.pt`, evaluations |
| P2 | freeze pseudo targets | truth-free h3 clustering, centers, assignments, stability and balance | define model-generated supervision before truth | frozen pseudo receipts | construction failure stops Pseudo training only | `pseudo/<seed>/` -> condition trainer |
| P3 | verify implementation | unit tests, no-op, freeze, projection, path equivalence, selected-expert gradient, final save | rule out architecture and bookkeeping errors | smoke report | any failure stops full | `smoke_report.json` |
| P4 | train coarse modules | 1,500 steps, route CE only where registered, parent experts from selected language loss | learn and isolate parent path | coarse final, $P_C$, freeze hash | invalid projection or freeze stops fine | coarse checkpoint -> Fine |
| P5 | train fine modules | 2,000 steps; only registered fine/coarse modules update | learn within-parent residual path | fixed final checkpoints and curves | any missing condition is Insufficient | condition finals -> extraction |
| P6 | freeze analysis and open TEST | freeze common probe C, final hashes, then evaluate TEST once | protect confirmation boundary | representations, routes, metrics, bootstrap arrays | incomplete pair is Insufficient | aggregate -> result records |

## 15. Implementation, Output, And Reproducibility Contract

The worker workspace is `/data/250010109/MoE_Router/experiments/20260830_a15_13_semantic_supervision_hierarchical_experts`. E04 code uses new `e04_*` modules and does not modify E01/E02 result directories. Scientific runs use `runs/e04-full-<UTC stamp>`; smoke uses `runs/e04-smoke-<UTC stamp>`. Refusal to overwrite any receipt or final checkpoint is mandatory.

Required tests cover: base freeze, output-projection-only zero initialization, zero-initialization equivalence, probability-scaled hard Top-1 and Router gradient flow, supervised-parent fine-loss selection separated from predicted expert dispatch, answer-prefix-only targets, nested pseudo labels, $w_C^Tr_2\approx0$, coarse freeze unchanged, batched parallel path equal to explicit per-branch path, only selected experts receive parameter updates, flat/hierarchy parameter and active-compute tolerance, pseudo-label truth isolation, route-only loss ownership, and fixed-final checkpoint completeness.

The approved execution tuple is:

```text
resource_profile=h100-4-reserved
execution_surface=ACP
workspace=share-space
aec2_cluster=share-cluster
worker_spec=n6ls.iu.i40.4
worker_nodes=1
quota_type=reserved
priority=normal
visible_gpus=4
processes=4
```

Expected artifacts are configuration and source hashes, GPU audit, data audit, tests, smoke receipt, teacher and condition final checkpoints, training curves, pseudo-label receipts, representation arrays, Router arrays, metric tables, bootstrap samples, completion audit, one primary comparison figure, one mechanism/pseudo diagnostic figure if decision-relevant, and job receipts. Raw artifacts remain worker-side; only curated figures and result records enter Research_System.

## 16. Success, Failure, And Insufficient Evidence

Adjudication order is fixed:

1. Oracle versus Hier-NoReg.
2. ResidualRoute versus FullRoute.
3. ParallelExpert versus SequentialExpert.
4. Hier-NoReg versus Vanilla-Flat.
5. Flat-Oracle versus Vanilla-Flat, then Hier-Oracle versus Flat-Oracle.
6. Pseudo-label entrance.
7. Flat-Pseudo versus Vanilla-Flat, Hier-Pseudo versus Flat-Pseudo, and Hier-Pseudo versus Hier-NoReg relative to Oracle.

Oracle Fail or Insufficient stops scientific interpretation of steps 2--6, although all pre-approved runs remain recorded. Oracle Pass with pseudo entrance or downstream failure means representation organization is feasible but label discovery failed. Only Oracle Pass, pseudo entrance Pass, and a stable Pseudo improvement support the final-to-middle self-supervision claim.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | State | Grounding |
| --- | --- | --- |
| A question and boundary | CONFIRMED | direct researcher execution prompt and active Focus |
| B data and provenance | CONFIRMED | direct request plus verified immutable E02-v2b evidence |
| C task and supervision | CONFIRMED | direct full-sequence NTP and Router-only loss constraints |
| D architecture | CONFIRMED | direct equations, growth order, controls, and ablations |
| E objective and optimization | CONFIRMED | direct loss exclusions; shared `0.1` and fixed budgets selected once under execution delegation |
| F comparison and evidence | CONFIRMED | direct metric, ordered comparisons, and stop rules |
| G execution | CONFIRMED | two seeds, full artifacts, no overwrite, 4xH100 reserved authorization, no Git/publication |

Cross-block consistency is `PASS`: the immutable data exposes the registered hierarchy; supervision fields obey each condition; every objective maps to a Router or language path; architecture can realize every term; test truth cannot select pseudo labels or checkpoints; comparisons isolate one named rival; resources cover all conditions; and the ordered verdict yields one boundary update.

The scientific body is frozen before implementation. After implementation starts, only execution receipts, result links, or append-only amendments are permitted. Any material change must state before/after values, reason, evidence already visible, affected blocks and conditions, approval basis, and eligibility impact. Commit, push, root sync, graph edits, external publication, new losses, new branches, per-condition tuning, and result-dependent checkpoint selection are not authorized.

### Amendment A1: probability-scaled hard routing and matched Flat supervision controls

Researcher approval: direct instruction on 2026-08-31. Before: selected experts entered the forward residual path with coefficient one, and only `VF` represented the Flat family. After: $\arg\max$ still selects one expert, but its residual is multiplied by the selected softmax probability; `VF-O` and `VF-P` add truth and frozen-pseudo four-leaf Router cross entropy to the identical Flat architecture. The fine Router loss is explicitly indexed by supervised $q_c$, while expert dispatch remains predicted. The audit also makes answer-prefix-only supervision, nested `1-to-2-to-4` pseudo construction, and output-projection-only zero initialization explicit. Reason: close ambiguity identified before any condition run completed and provide same-label-source topology controls. Evidence already visible: the first full attempt had completed only the two teachers and no pseudo receipt or condition final. Affected blocks: C, D, E, F, and G; all E04 conditions are rerun in a new directory. Eligibility: the stopped attempt is engineering history only; only the amended smoke and fresh two-seed full run may support E04 conclusions.

### Amendment A2: exact group-row lookup optimization

Execution delegation: authorized autonomous debugging under the same 2026-08-31 instruction. Before: every bootstrap group occurrence located its rows by rescanning the complete group vector. After: one stable group-to-row lookup is computed once and reused; sampled group order, duplicated groups, rows within each group, random-number stream, clustering, metrics, draw counts, thresholds, and outputs are unchanged. A direct equivalence test compares cached rows with the legacy full scan including duplicated sampled groups. Reason: the old implementation made the registered 20 pseudo-label refits and 2,000 result draws unnecessarily superlinear; a 2,000-group diagnostic fell from 14.941 to 3.435 seconds without changing the estimator. In paired pre/post smoke runs, all hard labels, soft labels, parent centers, and child centers were exactly equal. Evidence already visible: job `pt-j5tvbxvo` had two passing teachers but no pseudo receipt or condition result when stopped. Affected blocks: G execution performance only. Eligibility: no scientific setting changed; only the fresh post-optimization run is claim-eligible.
