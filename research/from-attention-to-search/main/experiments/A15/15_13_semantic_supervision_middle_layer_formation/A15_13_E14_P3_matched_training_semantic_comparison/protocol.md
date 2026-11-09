# Protocol: A15_13_E14_P3 Matched Training and Semantic Supervision Comparison

## 0. Approval Snapshot

```text
Document status: APPROVED_FOR_IMPLEMENTATION_SMOKE_PREFLIGHT_AND_CORE_FULL
Approval status: P-BDATA, P-AUX, P-BUDGET, P-LOAD, P-VERDICT, and G HUMAN_CONFIRMED on 2026-09-06
Block audit status: A--G CONFIRMED
Cross-block consistency: PASS
Execution scope approved: implementation, disposable smoke, 3.2 preflight, 3.3 core baselines, and 3.4 H-sem/H-shuf; conditional H-hard/H-oracle only if the registered trigger and decision need both occur
Design frozen at / registered revision: 20260906-P3-v1 immediately before implementation; registered scientific body is immutable after execution starts
Purpose: determine whether true train-only pseudo-label supervision improves online answer likelihood over task-only and shuffled supervision in the same sufficiently trained hierarchy
Primary Anchor: 15_13_05_gmm_pseudolabel_oracle_gap_anchor.md
Anchor decision question: does sample-specific semantic supervision add online task value after the historical missing-parent-supervision defect is removed from the comparison?
Anchor physical prior tested: train-only final-layer groups contain task-relevant information beyond their class frequencies
Anchor core model term tested: positive H-task minus H-sem and H-shuf minus H-sem answer-NLL effects
Anchor falsifier: an eligible necessary contrast reliably favors the control in both seeds
Experiment role: method construction with matched controls, preceded by a training-sufficiency validity gate
Primary metric from Anchor: summed reference-answer NLL divided by summed answer tokens, nats per answer token
Claim boundary from Anchor: local online likelihood only; no semantic-truth, hierarchy-necessity, expert-function, free-generation, or public-decontamination claim
Minimal setup: frozen Qwen3-0.6B-Base; block-14 down_proj low-rank modules; clean eight-source split; two paired seeds
Treatment and controls: H-sem versus H-task and H-shuf; D/F/SF/H-task establish contextual architecture baselines
Changed variable: within H, whether the same legal pseudo-label pairs are correctly or randomly associated with training records
Held fixed: base, data, teacher, hierarchy, initialization, order, budget, online coefficients, load policy, evaluator, checkpoint rule
Conditions to run: core D/F/SF/H-task/H-sem/H-shuf x seeds 17/29; H-hard/H-oracle are conditional and not part of the initial matrix
Pass: both registered semantic effects have positive 95% lower endpoints in each seed
Fail: at least one same necessary contrast has a nonpositive 95% upper endpoint in both seeds
Insufficient: every other eligible pattern, including seed disagreement or budget-limit instability
Cannot claim: teacher optimality, semantic reasoning, pure hierarchy causality, expert non-interchangeability, or uncontaminated benchmark generalization
Approval decision: execute the complete registered 3.2--3.4 core plan in this task and produce full canonical analysis; candidate G ceilings accepted
```

The researcher approved the five decision-bearing P3 groups and G ceilings in the 2026-09-06 merged
execution instruction. Implementation, smoke, preflight, and the complete 12-run core matrix may proceed
continuously in this task, subject to every registered qualification and stop rule. Smoke evidence must
still pass before scale-up; approval does not waive guards or turn an ineligible run into evidence.

## 1. Terminology / Definitions

- **Answer NLL:** total negative log probability assigned to reference answer tokens, divided by their
  total token count. Unit: nat per answer token; lower is better. It is teacher-forced likelihood, not
  free-generation accuracy.
- **Online route:** a route selected from the current causal block-14 state without a supplied teacher
  path. Previous reference-answer tokens remain available under ordinary likelihood evaluation.
- **Pseudo-label teacher:** a frozen PCA plus hierarchical diagonal Gaussian mixture fitted only to
  training-record final-layer whole-window means. It uses reference answers and is privileged
  training supervision, not semantic truth.
- **Parent / child:** one of three coarse groups / one of eight leaves, with children allocated 3/3/2.
- **Shared expert:** a low-rank residual used by every token. A selected expert is one chosen by a
  flat or hierarchical Router.
- **LowRankTokenBank expert:** for input \(x\), a rank-\(r\) branch is
  \(E_r(x)=B(Ax)/r\). Every D/F/SF/H branch uses its own rank in this division:
  D/F use \(r=24\); SF uses \(r=8\) for shared and \(r=16\) for selected branches; H uses \(r=8\) for
  shared, parent, and child branches. Equal active rank therefore controls capacity rank, not equal-
  scale optimization dynamics.
- **Loss-free route bias (P-LOAD):** a non-gradient bias used only to choose an argmax route from
  raw Router logits. It is not an auxiliary loss and does not enter the raw-softmax coefficient that
  scales a selected online expert.
- **Train / development / test:** train contributes gradients and teacher fitting; development chooses
  the common budget and load policy; test remains sealed until all models and analysis rules freeze.
- **Eligible:** all data, causal-input, gradient, frozen-weight, checkpoint, mask, and artifact guards
  pass. Missing or invalid evidence never becomes scientific Fail.

Condition names:

| ID | Meaning | Auxiliary supervision | Training path | Formal evaluation path |
| --- | --- | --- | --- | --- |
| D | one dense rank-24 adapter | none | single adapter | same |
| F | eight rank-24 flat experts, one selected | none | online | online |
| SF | one shared rank-8 plus one of eight rank-16 experts | none | online | online |
| H-task | shared/parent/child rank-8 hierarchy | none | online | online |
| H-sem | same hierarchy with true pseudo-label pair | parent and teacher-parent-conditional child | online | online |
| H-shuf | same hierarchy with fixed record-shuffled legal pair | same as H-sem | online | online |
| H-hard | optional shadow-Router reference | same as H-sem | fixed pseudo path, unit coefficients | forced and online rows |
| H-oracle | optional source-privileged reference | none required | fixed source path, unit coefficients | forced path |

## 2. Anchor Alignment

P1 and P2 showed that the old benchmark hard-pseudo branch omitted parent supervision and that adding
only that supervision repaired its online answer loss. P3 does not reuse those adapted experts. It
restarts every formal model from the same frozen base and asks the narrower unresolved question:
whether pseudo-label supervision adds online likelihood value over sufficiently trained same-
architecture controls.

The exact historical comparison boundary is preserved in
[`historical_e14_p1_p2_audit.csv`](tables/historical_e14_p1_p2_audit.csv): old E14 benchmark training
was 128 single-stage updates and four passes/911,644 answer-token exposures, whereas P2 optimized only
the 3,075-parameter parent Router for the same update/exposure budget with all expert objects frozen.
P3 must not call either historical object a matched simultaneous parent-plus-conditional-child baseline.

The historical E14 verdict combined final NLL, curve area, macro task score, and selective expert
interventions. P3 changes the decision object to clean-split, reference-answer NLL and uses development
curves only to fix budget. This is confirmed group **P-VERDICT**, synchronized in the Anchor and this
Protocol. P1/P2 remain eligible evidence about the old checkpoints only.

## 3. Tested Hypothesis

The primary hypothesis is that the correct sample-to-pseudo-label association supplies task-relevant
information beyond training time and label frequencies. It predicts, separately in seeds 17 and 29,

\[
\Delta_{task}=L_{H\text{-task}}-L_{H\text{-sem}}>0,
\qquad
\Delta_{shuf}=L_{H\text{-shuf}}-L_{H\text{-sem}}>0.
\]

The strongest rival predicts that any gain is explained by extra auxiliary optimization, class
frequencies, load, or stochastic training rather than the record-label relation. H-task controls the
absence of auxiliary classification; H-shuf controls its objective form and exact example-level pair
counts while breaking the relation.

## 4. Rival Explanations

1. **Old leakage or memorized duplicates:** construct record-ID- and normalized-content-disjoint
   train/development/test sets before fitting any teacher.
2. **Training duration:** choose one common 512 or 1024 update budget from development evidence only;
   never give a semantic arm extra updates.
3. **Expert starvation:** log answer-token and valid-token load, every expert gradient, and parameter
   change; use one predeclared H-task load-bias policy check only if its trigger fires.
4. **Frequency or loss-shape effect:** H-shuf preserves complete legal label-pair counts and uses the
   same auxiliary loss and weight.
5. **Architecture capacity:** D/F/SF/H-task are contextual baselines, but their storage, sharing,
   coefficient, and gate-depth differences prevent a pure hierarchy claim.
6. **Online handoff rather than teacher value:** H-hard/H-oracle are not initial rescue arms. They may
   run only after H-sem fails or is insufficient and the next decision specifically requires this
   decomposition, or after a new explicit request for a matched-budget privileged reference.

## 5. Data Construction And Provenance

Raw root: `/data/250010109/datasets/a15_e14_raw`. Frozen sources are MMLU, MMLU-Pro, BBH,
GSM8K, MATH, GPQA Diamond, HumanEval, and MBPP, rendered with the verified E14 record adapters.
One example is one rendered prompt, reference answer, metadata object, source, and immutable raw
record ID. Sequence length is at most 512; prompt tokens are masked and the answer suffix plus EOS is
retained under truncation.

Confirmed group **P-BDATA**:

1. Build a normalized-content key as collapsed-whitespace prompt plus a delimiter plus collapsed-
   whitespace answer. Deduplicate record IDs, then content globally. For cross-source duplicates retain
   the earlier source in `(mmlu, mmlu_pro, bbh, gsm8k, math, gpqa, humaneval, mbpp)`; within a source
   retain the lexicographically smallest record ID. Preserve a removed-to-retained map.
2. Sort each source by `sha256("20260906|{source}|{record_id}")`, then record ID. With
   \(h=\lfloor0.15n+0.5\rfloor\), assign the first \(n-2h\) records to train, next \(h\) to development,
   and final \(h\) to test.
3. Use natural retained source proportions in training and the pooled primary NLL. Bootstrap within
   source while preserving each source's record count. Per-source effects are descriptive because
   GPQA and HumanEval test sets have only 30 and 25 records.

The verified candidate counts are:

| Source | Train | Development | Test | Retained unique content |
| --- | ---: | ---: | ---: | ---: |
| MMLU | 11,002 | 2,357 | 2,357 | 15,716 |
| MMLU-Pro | 8,180 | 1,753 | 1,753 | 11,686 |
| BBH | 4,557 | 976 | 976 | 6,509 |
| GSM8K | 6,154 | 1,319 | 1,319 | 8,792 |
| MATH | 8,750 | 1,875 | 1,875 | 12,500 |
| GPQA | 138 | 30 | 30 | 198 |
| HumanEval | 114 | 25 | 25 | 164 |
| MBPP | 681 | 146 | 146 | 973 |
| **Total** | **39,576** | **8,481** | **8,481** | **56,538** |

Preflight must reproduce these counts and prove pairwise zero overlap for both record IDs and content
keys. It must hash every raw file and revision marker, the split manifest, record order, tokenized
tensors, and answer masks. No cyclic copying is permitted during dataset construction. Repeated use
of a training record across optimizer epochs is allowed and recorded as exposure, not a new example.

Only training-record final-layer whole-window means fit PCA64 and a three-component diagonal GMM.
The two largest fitted parent clusters receive three children and the smallest receives two, with
numeric component ID breaking count ties. Each GMM fit uses 20 deterministic restarts, at most 100 EM
iterations, regularization `1e-6`, and train mean likelihood alone for selection. Every chosen model
must converge and every parent/child cluster must be nonempty. The fitted objects and train input hash
freeze before development or sealed test assignments are inspected. Test pseudo labels, if generated
for route diagnostics, remain sealed with test outputs and cannot affect training, budget, or load.

Known boundary: content-key uniqueness does not detect semantic paraphrases or model-pretraining
contamination. Natural source proportions change the old equal-source mixture and therefore P3 is a
new clean comparison, not a replay of historical E14.

## 6. Learning Task And Permitted Supervision

At every position predicting an unmasked answer token, the model outputs next-token probabilities.
All conditions optimize reference-answer NLL. H-sem and H-shuf additionally predict the example's
pseudo parent and child from the 1024-dimensional causal block state at that prediction position.
No source ID, future-token state, full-window mean, teacher posterior, answer label, or teacher route is
an online Router feature.

H-shuf uses one NumPy permutation of complete `(parent, global_child)` pairs over training records,
seed 20260906, reused for both model seeds. The pair is permuted once, not per epoch or token. This
preserves legal parent-child pairs and exact example-level counts. Report answer-token-weighted class
counts separately; they need not match because record lengths differ.

The child target is represented by its global leaf ID but its CE denominator includes only leaves
inside the **teacher target parent**. It is computed even when the predicted parent is wrong, so the
loss stays finite and both Router heads receive direct supervision. H-task receives neither parent nor
child targets in its objective. All conditions use identical answer masks.

## 7. Model / Architecture And Frozen Variants

Freeze Qwen3-0.6B-Base, its embeddings, and language head. Replace only zero-indexed block 14 MLP
`down_proj` with its frozen original projection plus a low-rank residual. A pre-forward hook on the
whole block captures the `(batch, token, 1024)` block input for every Router. Experts read the
down-projection input `(batch, token, 3072)` and emit 1024-dimensional residuals. Router and expert
inputs are distinct tensors and remain so in every condition.

For every bank, \(E_r(x)=B(Ax)/r\) using that bank's own rank \(r\). For flat raw logits \(z\), route
\(k=\arg\max z\), raw probability \(p=softmax(z)\), and selected rank-24 expert \(E_{24,k}\),

\[
\Delta_D(x)=E_{24}(x),\qquad
\Delta_F(x)=p_kE_{24,k}(x),\qquad
\Delta_{SF}(x)=E_8^{shared}(x)+p_kE_{16,k}(x).
\]

For hierarchy, parent \(c\), allowed child \(f\), parent probability \(p_c\), and conditional probability
\(p_{f\mid c}\),

\[
\Delta_H(x)=E_8^{shared}(x)+p_cE_{8,c}^{parent}(x)+p_cp_{f\mid c}E_{8,f}^{child}(x).
\]

H-task/H-sem/H-shuf use this identical online rule for training and formal evaluation. Hard forced
paths use unit coefficients and therefore change both selection and scaling; they cannot be interpreted
as label-only interventions. In the optional P-LOAD policy, \(k\) is selected by biased logits but \(p\)
remains the raw softmax: \(k=\arg\max_j(z_j+b_j)\) and \(p=softmax(z)\) (and analogously within a selected
parent for a child). Thus a route bias changes selection, never the probability coefficient.

| Model | Expert bank and per-branch scale | Expert params | Router params | Total trainable | Per-token selected expert params | Active rank |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| D | one rank 24, \(1/24\) | 98,304 | 0 | 98,304 | 98,304 | 24 |
| F | eight rank 24, selected \(1/24\) | 786,432 | 8,200 | 794,632 | 98,304 | 24 |
| SF | shared rank 8, \(1/8\); eight rank 16, selected \(1/16\) | 557,056 | 8,200 | 565,256 | 98,304 | 24 |
| H | shared/three parent/eight child rank 8, each \(1/8\) | 393,216 | 11,275 | 404,491 | 98,304 | 24 |

“Active rank” and selected expert parameters exclude the always-evaluated Router parameters and are
not FLOP equality. They also do not make D/F/SF/H a same-scale dynamical control: the \(1/r\) factors,
shared residual, total stored parameters, and gate depth differ. All actual tensor counts must be
asserted after construction. Low-rank A matrices use Kaiming-uniform initialization, B matrices start
at zero, and Router linear layers use the runtime PyTorch default. Seed 17 or 29 is set before
constructing each complete adapter; conditions in the same seed use the same data order.
H-task/H-sem/H-shuf must have byte-identical initial state hashes.

[`training_object_contract.csv`](tables/training_object_contract.csv) separately records allocated,
`requires_grad`, and optimizer-member parameters. In particular, conditional H-oracle allocates the
11,275 Router parameters but has zero Router optimizer parameters; its 393,216 expert parameters alone
are trainable/optimized. H-hard and H-oracle are explicitly `conditional_not_triggered`, so this is a
construction contract rather than a claim that either arm has run.

## 8. Training Objective And Optimization

For answer mask \(M\), all losses are means over valid answer-prediction positions within each
microbatch. H-sem/H-shuf use confirmed group **P-AUX**:

\[
L=L_{answer}+0.5L_{parent}+0.5L_{child\mid teacher\ parent}.
\]

The historical E14 route term had coefficient 1.0 but only one global eight-way CE. No old run used
simultaneous parent and conditional-child CE. This confirmed average preserves total auxiliary weight
one without claiming historical identity. H-task, D, F, and SF optimize \(L_{answer}\) only. Task loss
also reaches learned route probabilities and selected experts. No load-balancing loss is added.

Use AdamW, betas `(0.9, 0.999)`, epsilon `1e-8`, weight decay 0.01, gradient-norm clip 1.0,
adapter LR `2e-4`, and Router LR `5e-4`. Microbatch is 8 records, accumulation is 16, effective batch
128, max sequence length 512. All conditions share the exact record order within each seed; order is
a deterministic full-train permutation per epoch, continued until the registered optimizer-update
count. Log actual records and answer tokens exposed at every update.

The schedule has linear warmup for exactly 5% of the registered total updates, rounded to the nearest
integer with halves rounded up (26 at 512; 51 at 1024), followed by cosine decay to zero at the final
update. The final registered checkpoint is selected; development never selects among checkpoints.
Save update 0, 128, 256, 384, and 512 for the first preflight. A 1024 rerun saves those plus 768 and
1024. Resume checkpoints must contain model, optimizer, scheduler, scaler if any, RNG states, sampler
epoch/permutation/cursor, completed microbatches, update, and exposure counters. Otherwise restart from
initialization and label the prior run incomplete.

## 9. Conditions, Seeds, And Checkpoints

Budget and load-policy selection are ordered and development-only:

1. Run unbiased D/F/SF/H-task at seed 17 for 512 updates from recorded common initial states.
2. Apply the registered four-baseline curve rule in Section 15 to choose one common budget. If it is
   1024, rerun **all four** unbiased baselines from their recorded initial states under the 1024-update
   schedule; no 512 checkpoint is continued after its LR reached zero.
3. At the selected budget, evaluate the P-LOAD trigger on the corresponding unbiased H-task run. Only
   if triggered, rerun H-task load-on from its same initial state under that selected total schedule and
   compare the paired development NLL using the registered 0.002 rule. Select one final H policy.
4. If load-on is selected, the prior H-task load-off run is not a formal H-task checkpoint. H-task,
   H-sem, and H-shuf must all be trained/retrained under load-on. If 1024 is selected, load policy is
   selected again at 1024 and may not be inherited from 512.

Only a 512 selection with final load-off permits the original four 512 preflight runs to serve as formal
seed-17 baselines. All other formal models begin from their recorded common initial states at the final
budget and policy.

Core formal matrix: D/F/SF/H-task/H-sem/H-shuf at seeds 17 and 29, 12 runs total, all at the same
final budget. P2 models are historical diagnostics only. A failed or smoke model never initializes a
formal run. No third seed, multi-GPU model, teacher change, or architecture swap is allowed.

H-hard and H-oracle are `NOT_APPROVED_NOT_TRIGGERED`. If the registered semantic verdict is not Pass
and the researcher needs to distinguish teacher value from online handoff, an append-only amendment
may authorize each at seeds 17/29. H-hard must train experts plus both shadow Router heads from scratch
under the same budget; H-oracle requires a frozen legal source-to-parent/child map. No source map is
approved in this revision.

## 10. Primary Metric And Frozen Analysis Plan

For condition \(m\), record \(i\), stored loss sum \(s_i^m\), and answer-token count \(n_i\),

\[
L_m=\frac{\sum_i s_i^m}{\sum_i n_i}.
\]

The unit of observation and resampling is a complete test record. The unit of replication is a model
seed. For each seed separately compute H-task minus H-sem and H-shuf minus H-sem. Positive favors
H-sem. Use 2,000 percentile paired bootstrap draws with NumPy seed 20260906. Within every draw,
resample records with replacement separately inside each of the eight sources, keeping original source
counts, then recompute the pooled ratio of total loss to total tokens. Report the point effect and
two-sided 2.5/97.5 percentiles. The two contrasts and two seeds are a conjunction; no multiplicity
adjustment is used because no individual positive contrast can pass the experiment.

Missing/failed conditions, changed answer-token counts, nonfinite values, post-hoc exclusions, or
checkpoint mismatch yield Ineligible/Incomplete, never imputation. There is no outlier removal or seed
pooling. Test is unsealed only after code, data, teacher, initial states, budget, load policy,
checkpoints, and analysis script hashes freeze. Per-source effects and unweighted seed means are
descriptive and cannot rescue the primary conjunction.

Confirmed group **P-VERDICT** is this narrower rule:

- `SEMANTIC_ONLINE_INCREMENT_SUPPORTED`: all four 95% lower endpoints exceed zero.
- `SEMANTIC_ONLINE_INCREMENT_NOT_SUPPORTED`: at least one named contrast has upper endpoint at most
  zero in both seeds; name that contrast and do not imply every effect is negative.
- `INSUFFICIENT`: every other eligible pattern, including seed disagreement or intervals spanning zero.
- `BUDGET_LIMITED_INSUFFICIENT`: at the 1024 ceiling any preflight baseline meets the registered
  late-improvement rule, or at the selected common budget any final-policy H-task/H-sem/H-shuf condition
  meets it. This qualification outcome takes precedence over Pass or Fail and does not authorize more
  updates.
- `INELIGIBLE` / `INCOMPLETE`: a qualification guard fails / an approved arm is missing.

This rule does not overwrite historical E14 A/B/C.

## 11. Secondary Metrics And Guards

Report development and test NLL by source; answer-token accuracy as descriptive; parent and child
pseudo-label CE/agreement; parent loads; child loads conditional on parent; valid-token and answer-
token route counts; per-module gradient norms and parameter deltas; total and selected parameters;
peak memory, records/s, tokens/s, and elapsed time. None substitutes for primary task loss.

Confirmed group **P-LOAD** defines the sole hierarchy load-policy branch. Its **bias-update count
domain** is every non-padding prediction position (`attention[:, :-1]`) in all 16 microbatches of one
optimizer update; prompt positions count here even though answer NLL and the trigger use answer-token
positions. Let \(c_a\) be parent-\(a\) selections and \(c_{a,j}\) child-\(j\) selections within parent \(a\);
let \(n_a\in\{3,3,2\}\) be the number of children of that parent. With \(\eta=10^{-3}\),

\[
f_a=\frac{c_a}{\sum_b c_b},\qquad
\tilde b_a^p=b_a^p+\eta\left(\frac13-f_a\right),\qquad
b_a^{p,+}=\operatorname{clip}_{[-0.1,0.1]}\left(\tilde b_a^p-\operatorname{mean}_b\tilde b_b^p\right),
\]

\[
f_{a,j}=\frac{c_{a,j}}{\sum_{k=1}^{n_a}c_{a,k}},\qquad
\tilde b_{a,j}^{\ell}=b_{a,j}^{\ell}+\eta\left(\frac1{n_a}-f_{a,j}\right),\qquad
b_{a,j}^{\ell,+}=\operatorname{clip}_{[-0.1,0.1]}\left(\tilde b_{a,j}^{\ell}-\frac1{n_a}\sum_{k=1}^{n_a}\tilde b_{a,k}^{\ell}\right).
\]

Use denominator `max(sum, 1)` in code, so an empty count group receives its finite zero-count update.
The parent bias is centered across all three parents; each leaf bias is centered only within its own
3/3/2 parent group. This is not the old E14 global-eight-leaf frequency update. At selection time,

\[
k_p=\arg\max_a(z_a^p+b_a^p),\quad p^p=\operatorname{softmax}(z^p),\qquad
k_\ell=\arg\max_{j\in k_p}(z_j^\ell+b_{k_p,j}^\ell),\quad
p^{\ell\mid k_p}=\operatorname{softmax}_{j\in k_p}(z_j^\ell).
\]

Biases therefore enter argmax selection only, never either raw-softmax probability coefficient. They
are buffers updated after `optimizer.step()`, have no gradient, and are not a load-balancing loss.

The **trigger detection domain** remains answer-token selections, so it is comparable with the task
metric. In the final 25% window of the selected-budget unbiased H-task run, a dead expert has zero
answer-token selections; concentration is parent share above 0.80 or within-parent child share above
0.90; undertraining is below 1% of eligible answer-token selections plus parameter-delta norm below
10% of same-level-peer median. Run the same-seed, same-total-schedule H-task load-on comparison only
if a dead expert exists or concentration and undertraining coexist. Select load-on only if paired
development NLL improves by at least 0.002 nat/token with positive 95% lower endpoint and all
parameters/gradients remain eligible; otherwise select load-off. The selected policy applies equally
to formal H-task/H-sem/H-shuf. This one-seed policy selection is not evidence that load balancing is
generally effective.

Mandatory guards:

- exact raw, split, tokenized-data, teacher, configuration, code, protocol, and base-model hashes;
- zero record-ID/content overlap and exact candidate split counts;
- finite selected GMMs with all eight leaves represented in train;
- constructed parameter counts equal Section 7; base/embedding/head hashes unchanged;
- after at least one optimizer step and at two-update smoke completion, every expected bank has finite
  gradients and actual parameter change in both A and B, or the run records a named, justified failure;
  B-zero initialization may make A's *first backward* gradient zero and is not itself a failure;
- hard smoke updates both parent and child shadow Routers;
- SF shared branch is evaluated for every valid token;
- identical answer masks and per-record token counts across conditions;
- block input and down-projection token alignment are exact; padding never enters answer loss;
- changing a suffix cannot change an earlier captured state or Router logit above `1e-5` in matched
  runtime and batch shape;
- teacher-parent conditional child loss stays finite for deliberately wrong predicted parents;
- online evaluation does not read teacher labels or source IDs.

## 12. Known Good / Known Bad / Known Confusing Cases

Known good: zero-initialized low-rank B matrices reproduce the frozen base at update zero; a legal
teacher-parent child loss updates both Router heads; a selected expert receives task gradient.

Known bad: duplicate content across splits, an impossible parent-child pair, a changed frozen hash,
an online path that consumes teacher labels, or a hard path whose shadow parent has zero gradient must
stop the affected run.

Known confusing: better route agreement with worse answer NLL is not semantic value; lower NLL with a
different answer mask is ineligible; H beating SF does not isolate hierarchy because storage and gate
depth differ; absence of statistical significance is not equivalence or convergence.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal | Input and assumptions | How | Expected output | Gate / named failure | Handoff |
| --- | --- | --- | --- | --- | --- | --- |
| 3.1 contract | make the comparison constructible | Focus, Anchor, P1/P2, raw/code audits | freeze A-G and actual object table | this Protocol and contract CSV | unresolved proposal would keep `DRAFT_NOT_EXECUTABLE` | confirmed design |
| data/teacher | remove direct split leakage and freeze supervision | researcher-confirmed P-BDATA; raw snapshots | render, dedupe, split, tokenize, extract frozen means, fit train-only PCA/GMM | manifests, tensors, teacher, traces, hashes | overlap, count, convergence, or nonempty-cluster failure stops | implementation smoke |
| smoke | prove code paths and recovery | researcher-confirmed A--F and G implementation/smoke scope; disposable tiny subset | unit/integration tests and two-update arms, one single-H100 job, at most 60 minutes | tests, gradients, invariants, resumable state, receipt, measured throughput | any mandatory guard fails; smoke weights discarded | researcher reviews receipt and resource estimate |
| G resource check | verify the approved ceilings remain feasible | successful smoke receipt and estimate | append receipt/estimate and compare with approved ceilings | measured estimate and go/stop receipt | an estimate beyond a ceiling stops before that scope | approved preflight when within ceiling |
| 3.2 preflight | choose one budget/load policy without test | approved G scope; D/F/SF/H-task seed17 | first unbiased 512 four-baseline curves, then selected-budget H-task policy check | curves, gradients, loads, throughput, policy table | budget/load rule cannot yield a unique policy | frozen formal configuration |
| 3.3 baselines | establish contextual architecture performance | frozen budget/load; two seeds | complete D/F/SF/H-task matrix | eight checkpoints and paired outputs | missing/ineligible arm prevents architecture table | 3.4 core |
| 3.4 semantic | test sample-specific supervision | same H setup; true/shuffled pairs | train H-sem/H-shuf in both seeds and evaluate sealed test | four new checkpoints, per-record arrays, verdict inputs | no arm-specific extra budget; failures retained | canonical results |
| optional hard | localize a failed semantic result only if triggered | explicit amendment and legal mapping | train H-hard/H-oracle from scratch | forced/online reference rows | not running is not failure before trigger | independent audit |

## 14. Algorithm, Output, And Provenance Contract

Canonical Research_System directory is this Protocol's directory. Worker root is proposed as
`/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p3_matched_training` and must not already
exist at implementation start. Raw datasets, tensor caches, checkpoints, logs, and complete run
directories stay in the worker root or `/data/250010109/datasets/`; only curated tables, figures,
Summary, Detailed, and an artifact map enter Research_System.

Expected worker artifacts:

- `protocol_snapshot.md`, code/config diff manifest, base/environment/raw-file hashes;
- `data_manifest.json`, deduplication map, split IDs/hashes, tokenized tensors and mask audit;
- frozen teacher states or cache map, PCA/GMM object, restart traces, assignments and hashes;
- tests and smoke logs, eligibility guard JSON, initial-state hashes;
- per-condition checkpoint directories, recovery states, training history, gradients, parameter deltas,
  loads, throughput, and failures;
- `run_manifest.json` with job IDs, commands, resource, seeds, state, hashes, and exclusions;
- per-record test arrays containing record ID, source, condition, seed, loss sum, token count, path
  mode, and route diagnostics;
- frozen analysis outputs, comparison tables, figures, completion audit, and artifact manifest.

G resource boundary: the approved smoke scope uses one H100 for at most 60 minutes. The approved
preflight ceiling is one H100 for at most 18 hours; the approved core-full ceiling is one H100 for at most 36 hours.
Preflight and core full may be sequentially split into jobs, but concurrency is one, automatic retry is
zero, and their combined GPU-hour ceiling is 54 hours. These are ceilings, not runtime targets. The
merged execution instruction explicitly accepted them. After smoke, append its receipt and measured-
throughput estimate; continue only when the next approved scope remains within its ceiling. Any estimate
beyond a ceiling requires new authority.

Canonical outputs after eligible evidence exists: `summary.md`, `detailed.md`, `tables/`, and
`figures/`. The required figures are development NLL versus seen answer tokens and the two primary
semantic effects with intervals. A load figure is included only if P-LOAD triggers and affects the
policy. Every figure records data source, unit, aggregation, axes, observed result, allowed conclusion,
and limitation.

## 15. Success / Failure / Insufficient Evidence

Success, Fail, and Insufficient follow Section 10 only after every approved condition is eligible.
Architecture comparisons report F minus D, SF minus F, and H-task minus SF per seed with intervals,
but no threshold promotes them to a structural theorem. Training sufficiency is a development-policy
decision, not a scientific method verdict. Preflight must not announce the final method ranking.

Confirmed group **P-BUDGET**:

1. Run unbiased D/F/SF/H-task seed-17 curves to 512 and compute each development effect from update
   384 to 512 with the same source-stratified paired-record bootstrap.
2. Select 1024 if any point improvement is at least 0.002 nat/token and its lower endpoint exceeds
   zero, or if any pairwise architecture ordering changes between 384 and 512 with an absolute
   difference at least 0.002 at either checkpoint. Otherwise select 512.
3. If 1024 is selected, rerun all four unbiased baselines from their recorded initial states under the
   1024 schedule. Apply the same improvement and ordering rule over updates 768--1024. If any baseline
   still meets it, label the experiment `BUDGET_LIMITED_INSUFFICIENT` and stop before load selection or
   the formal matrix; the ceiling is not expanded. Otherwise select P-LOAD again using that 1024
   H-task run. The common policy cannot be inherited from 512.
4. At the selected common budget, apply the same point-improvement rule to every final-policy
   H-task/H-sem/H-shuf development curve: updates 384--512 for a 512 budget, or 768--1024 for a 1024
   budget. The H-task check is repeated when load-on is selected; the stable unbiased H-task need not be
   duplicated when load-off remains final. If any checked condition meets the 0.002 rule, label the
   complete comparison
   `BUDGET_LIMITED_INSUFFICIENT`; give neither Pass nor Fail, add no extra updates, and do not alter
   the budget after the test phase begins. This qualification decision has priority over the scientific
   verdict.

If the selected common budget is 512 and a final-policy H condition meets the rule after the common
budget has frozen, this is not an automatic escalation to 1024: the formal budget may not be changed
after entering the test phase.

The 0.002 threshold is a minimum practically relevant development change, not an equivalence margin
or proof of convergence.

## 16. What This Cannot Claim

Even Pass cannot show that clusters encode reasoning semantics rather than source/topic regularities,
that final-layer whole-window teachers are optimal or deployable, that hierarchy is necessary, that
selected experts are functionally non-interchangeable, that free generation improves, or that public
benchmark contamination has been eliminated. The clean split removes direct snapshot duplication
under one content key only. Failure cannot prove absent causal information because teacher choice,
linear Router capacity, objective weighting, and the 1024-update ceiling remain bounded rivals.

## 17. Block Confirmation, Freeze, And Amendment Ledger

### Candidate audit ledger

| Block | State | Grounding and unresolved decision |
| --- | --- | --- |
| A question/boundary | CONFIRMED | researcher activated the exact P3 handoff plan; boundaries retained |
| B data | CONFIRMED | clean 70/15/15 natural-proportion split is frozen as P-BDATA |
| C task/supervision | CONFIRMED | simultaneous 0.5/0.5 parent plus teacher-parent-conditional-child CE is frozen as P-AUX |
| D architecture | CONFIRMED | D/F/SF/H construction and per-branch rank scaling are specified; implementation remains subject to smoke guards |
| E optimization | CONFIRMED | common-budget ordering and conditional P-LOAD policy selection are frozen before test |
| F evidence | CONFIRMED | answer-NLL conjunction, late stability qualification, and verdict precedence are frozen |
| G execution | CONFIRMED | smoke 1 H100-hour, preflight 18 H100-hours, core full 36 H100-hours; concurrency one, retry zero |

Cross-block consistency audit: `PASS`. Data exposes the question; teacher
fields obey the supervision boundary; all objective terms are constructible; H controls change only
label association; development cannot inspect test; common budget precedes common load policy; and a
semantic late-instability qualification blocks scientific verdict. The approved scopes are executable
in sequence, but every registered stage guard remains binding.

### Approval and change control

2026-09-06, merged execution approval: the researcher instructed Sol to execute the plan in one task,
complete preflight, formal training, and result analysis, and treat completion as all protocol-required
experiments plus the full report. This confirms P-BDATA, P-AUX, P-BUDGET, P-LOAD, P-VERDICT, and G as
written. It authorizes implementation, one disposable smoke, 3.2, 3.3, and 3.4 within the registered
ceilings. H-hard/H-oracle are authorized only conditionally: the registered core trigger and a need to
separate teacher value from online handoff must both occur; a non-trigger is recorded as protocol-correct
`NOT_RUN_NOT_TRIGGERED` rather than missing work.

After successful smoke, append a receipt (job identity, elapsed time, measured records/tokens per
second, guard result, and discarded-weight declaration) and a preflight/core-full GPU-hour estimate.
The approved preflight ceiling is 18 H100-hours, the approved core-full ceiling is 36 H100-hours,
concurrency is one, total is at most 54 GPU-hours, and retry is zero. Continue only while the measured
estimate fits these ceilings. After the first approved execution starts, no hypothesis,
data, objective, architecture, condition, metric, threshold, exclusion, or stopping rule may be
silently changed. Every material change requires an append-only amendment with before/after values,
reason, timing, affected conditions, approval, and eligibility impact.

### Amendment 20260906-P3-A1: four-H100 reserved, condition parallelism, and 512-only ceiling

```text
Amendment time: 2026-09-06T18:00Z
Before resource: one H100, concurrency one, quota surface not fixed to reserved
After resource: one ACP worker node, n6ls.iu.i40.4, four H100 80GB GPUs, reserved quota,
  at most four independent conditions running concurrently, automatic retry zero
Before budget branch: a triggering 384-to-512 baseline rule selected a four-baseline 1024 rerun
After budget branch: 512 is the only approved total-update budget; if the registered 384-to-512
  trigger fires, stop before load selection and the formal matrix with BUDGET_LIMITED_INSUFFICIENT
Reason: the researcher supplied a four-card reserved allocation, requested condition-level saturation,
  and explicitly limited this execution to the 512 load-off or conditional load-on path
Evidence visible before amendment: data/teacher and disposable smoke receipts; D seed-17 training had
  reached recovery update 224/512; no update-384 or update-512 development evidence, load decision,
  formal checkpoint, or test output existed
Affected blocks: E budget stopping branch and G execution/reproducibility boundary
Affected conditions: preflight D/F/SF/H-task and the complete core matrix only through scheduling;
  every condition remains an independent single-GPU run with unchanged seed, initialization,
  data order, optimizer, schedule, update count, objective, and artifact contract
Approval: HUMAN_CONFIRMED by the researcher on 2026-09-06 before resumed execution
Eligibility impact: the existing update-224 D recovery remains eligible because its scientific
  configuration is unchanged. Condition-level parallelism changes no within-condition computation.
  If the 512 trigger does not fire, the original 512 load-off/load-on analysis remains eligible. If it
  fires, no 1024 evidence is collected and the only eligible conclusion is budget-limited
  insufficiency under this amended 512 ceiling; a semantic Pass or Fail is prohibited.
GPU-hour ceilings: unchanged at preflight <=18, core full <=36, combined <=54 H100-hours
```

This amendment supersedes only the resource/concurrency and 512-to-1024 transition clauses for the
current execution. It does not retrospectively change the registered scientific body, and it does not
authorize H-hard/H-oracle, publication, Git commit, push, or external synchronization. The four GPUs
parallelize conditions rather than one model: each child process sees exactly one GPU, and the parent
orchestrator freezes each decision gate before launching dependent conditions. The load-on policy
check remains a single H-task condition; idle GPUs during that decision dependency are not filled with
unapproved or not-yet-frozen formal runs.

### Execution receipt for Amendment 20260906-P3-A1

ACP job `pt-86wcqrbi` ran on one reserved `n6ls.iu.i40.4` worker from 2026-09-06 18:05:44 UTC and
reached platform state `SUCCEEDED` at 18:57:28 UTC with no automatic retry. The worker root is
`/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p3_matched_training/runs/full-20260906T170500Z`.
The preflight selected 512 updates and load-off; all 12 core conditions completed, the final stability
gate passed, and 12 paired test arrays were produced. The machine analysis recorded typed verdict
`INSUFFICIENT`. This paragraph records execution status only; result interpretation and researcher-owned
judgment remain outside the Protocol. Complete operational evidence is in
`receipts/acp_and_postrun_audit.json`, and the decision-bearing machine output is in
`analysis/verdict.json`, both relative to the worker root.
