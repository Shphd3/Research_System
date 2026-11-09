# Summary: A15_13_E14_P3 Matched Training and Semantic Supervision Comparison

Primary Anchor: [A15_13_05](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_05_gmm_pseudolabel_oracle_gap_anchor.md).  
Frozen Protocol: [P3 Protocol](protocol.md), revision `20260906-P3-v1` plus approved amendment `20260906-P3-A1`.  
Detailed record: [Detailed](detailed.md).  
Result status / eligibility: `COMPLETE / ELIGIBLE`; researcher-confirmed typed verdict `INSUFFICIENT`.

## 1. Purpose

Determine whether a train-only hierarchical pseudo-label teacher improves online reference-answer
likelihood over both task-only training and frequency-matched shuffled supervision after all hierarchy
arms are newly trained from matched initial states at one audited budget.

## 2. Hypothesis

True pseudo-label supervision should lower answer NLL relative to both H-task and H-shuf separately in
seeds 17 and 29. The strongest rival is that any apparent gain comes from auxiliary optimization,
label frequencies, routing load, or seed-specific optimization rather than the record-label relation.

## 3. Analysis Method

- Train D/F/SF/H-task/H-sem/H-shuf for both paired seeds on the clean split, with a frozen train-only
  PCA64 plus 3/3/2 hierarchical GMM teacher; use development only to freeze the common 512-update,
  load-off policy before opening test.
- Measure summed reference-answer negative log probability divided by summed answer tokens. For each
  seed and registered H contrast, use 2,000 paired-record bootstrap draws stratified by source; positive
  H-task-minus-H-sem or H-shuf-minus-H-sem favors H-sem.
- After preserving the registered verdict, perform one no-training, post-hoc audit of development
  checkpoints 128/256/384/512, per-source effects, route loads, auxiliary losses, gradients, and expert
  changes. This audit selects a follow-up branch but cannot repair or strengthen the primary result.

## 4. Conclusion

Verdict: `INSUFFICIENT`.

All 12 core arms are eligible and stable at the registered 512-update ceiling, but the necessary
H-task comparison reverses across seeds. At test, H-sem is better than H-task in seed 17 by
**0.010320 nat/answer token** (95% interval **[0.009795, 0.010890]**) and worse in seed 29 by
**0.002078** (H-task-minus-H-sem **-0.002078**, **[-0.002469, -0.001680]**). H-sem beats H-shuf in
both seeds, but the registered conjunction requires both controls in both seeds; the positive shuffled
comparison cannot rescue the failed task-only replication.

| Registered rule | Observed value | Guard / eligibility | Verdict | Evidence source |
| --- | --- | --- | --- | --- |
| Common configuration before test | 512 updates; load-off; all six final H late improvements below 0.002 | Development-only budget/load/stability gates passed | ELIGIBLE | [budget](tables/budget_512.json), [load](tables/load_trigger.json), [H stability](tables/formal_h_stability.csv) |
| H-task − H-sem, seed 17 | +0.010320 [0.009795, 0.010890] | 8,481 paired records; 562,954 answer tokens | favors H-sem | [primary effects](tables/primary_semantic_effects.csv) |
| H-task − H-sem, seed 29 | -0.002078 [-0.002469, -0.001680] | same identities and token counts | favors H-task | [primary effects](tables/primary_semantic_effects.csv) |
| H-shuf − H-sem, seeds 17 / 29 | +0.014645 [0.014138, 0.015128] / +0.005467 [0.005064, 0.005837] | fixed legal-pair shuffle; same objective weight | favors H-sem in both | [primary effects](tables/primary_semantic_effects.csv) |
| Four-effect conjunction | one of four necessary effects is reliably negative | 12/12 guards pass; no missing core arm | `INSUFFICIENT` | [typed verdict](tables/verdict.json), [execution audit](tables/execution_audit.json) |

### No-training reversal audit

The seed reversal is already present at development update 128 and remains in the same opposite
directions through update 512; all eight checkpoint intervals exclude zero.

| Update | Seed 17 H-task − H-sem | Seed 29 H-task − H-sem |
| ---: | ---: | ---: |
| 128 | +0.001272 [0.000897, 0.001636] | -0.003132 [-0.003524, -0.002737] |
| 256 | +0.010107 [0.009567, 0.010661] | -0.001964 [-0.002347, -0.001589] |
| 384 | +0.010178 [0.009635, 0.010722] | -0.002263 [-0.002630, -0.001905] |
| 512 | +0.010096 [0.009563, 0.010636] | -0.002310 [-0.002690, -0.001948] |

Source effects are heterogeneous rather than uniformly broad. At update 512, 6/8 source effects
match seed 17's pooled sign and 4/8 match seed 29's. Two sources account for 80% of absolute pooled
contribution in seed 17 and three in seed 29; GSM8K is the largest contributor in both (46.9% / 48.4%).
Nevertheless, removing any single source preserves the final pooled sign in both seeds. Thus the
reversal is magnitude-concentrated but not a one-source artifact at the final checkpoint. See
[source concentration](tables/reversal_source_concentration.csv) and
[source effects](tables/reversal_source_effects.csv).

The audit found no registered implementation, recovery, or evaluation anomaly. Histories are
contiguous and finite; same-seed H initial tensors match; all four eligibility guards pass; all parent,
leaf, and shared experts change; paired development/test identities and token counts match; and the
57-entry primary artifact manifest has zero hash mismatches. H-sem strongly changes routing: in the
last quarter, the largest parent share is 0.554/0.562 for seeds 17/29 versus 0.956/0.952 for H-task.
Its parent and child classification losses are positive, finite, and lower late than early. This load
shift is a candidate localization clue, not a registered anomaly or proof that supervision strength
causes the reversal. See [training segments](tables/reversal_training_segments.csv),
[expert updates](tables/reversal_expert_updates.csv), and the
[audit decision](tables/reversal_audit_decision.json).

### Important Figures

![Registered test effects](figures/primary_semantic_effects.png)

How to read: the vertical zero line separates effects favoring H-sem (right) from H-task/H-shuf
(left). The seed-29 H-task comparison is the single necessary effect on the wrong side; therefore the
registered conjunction is insufficient. The figure cannot identify why seeds differ.

![Persistent development reversal](figures/reversal_development_effects.png)

How to read: positive values favor H-sem. Blue remains positive and red remains negative from update
128 through 512. This rules out a reversal that appears only at the final checkpoint, but it does not
distinguish auxiliary-weight causation from other seed-specific optimization effects.

### Claim Boundary

Can claim: under this frozen base, clean split, train-only teacher, hierarchy, 512-update load-off
training, and two registered seeds, true pseudo-label supervision beats the shuffled-label control in
both seeds but does not show a replicated advantage over task-only training; the registered result is
therefore insufficient.

Cannot claim: that semantic supervision is generally helpful or harmful, that its current weight is
the cause of the reversal, that the groups are semantic truth, that hierarchy is necessary, that
experts have non-interchangeable functions, or that teacher-forced NLL implies free-generation or
decontaminated public-benchmark gains.

### Next Step Analysis

Decision: the researcher-selected branch is exactly one **matched semantic-supervision-strength
localization**. The AI-proposed exact operationalization, pending Protocol confirmation, is one
three-arm H matrix at 512 updates and load-off for seeds 17/29 from common initial states: H-task with
\(\lambda_p=\lambda_c=0\), H-sem-weak with \(\lambda_p=\lambda_c=0.25\), and current H-sem with
\(\lambda_p=\lambda_c=0.5\). Hold architecture, teacher, data order, optimizer, checkpoints, and
evaluator fixed; do not add seeds, H-hard/H-oracle, layers, or other methods in this experiment.

Why it follows: no registered anomaly was found, while the opposite development directions persist
from update 128 and H-sem materially changes route loads under a nontrivial auxiliary objective.

Unresolved uncertainty: whether the current auxiliary weight is too strong, rather than semantic
supervision itself lacking stable task value.

Completion criterion: pre-register a development-only localization rule before execution. The weak
arm must improve over the current weight in both seeds at update 512 under paired intervals; H-task
then determines whether the weaker signal retains task value. The already-open P3 test cannot serve
as a new confirmatory selection surface.

Stop or redirect condition: if the weak arm does not improve over the current arm in both seeds,
stop the over-strong-weight explanation; do not add seeds until a positive result appears.

Resume action: draft and obtain approval for that one follow-up Protocol. No follow-up training was
started in this task.
