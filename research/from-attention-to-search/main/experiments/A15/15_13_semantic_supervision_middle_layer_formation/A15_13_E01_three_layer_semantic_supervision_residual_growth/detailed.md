---
experiment_id: A15_13_E01_three_layer_semantic_supervision_residual_growth
status: EVIDENCE_COMPLETE
interpretation_status: AI_EVIDENCE_DRAFT_AWAITING_HUMAN_RESULT
eligibility: INSUFFICIENT_TEACHER_AND_SEARCH_ENTRANCE
completed: 2026-08-30
acp_job: pt-exbyxhne
run_stamp: 20260830T181100Z
resource_profile: h100-4-reserved
---

# Detailed: Final-Layer Semantic Supervision And Staged Middle-Layer Expert Growth

Primary Anchor: [A15_13 Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/15_13_semantic_supervision_middle_layer_formation_anchor.md)

Frozen Protocol: [protocol.md](protocol.md), SHA-256
`d90da0f617a970b905072443744a4006ef76ed0f489dc8f52f43dc3fb4d881ac`

Summary: [summary.md](summary.md)

Raw full-run root:
`/data/250010109/MoE_Router/experiments/20260830_a15_13_semantic_supervision_hierarchical_experts/runs/full-20260830T181100Z`

## 0. Quick Recap

- **Purpose:** test whether final-layer semantic information can shape a
  second-layer coarse-to-fine representation through parent-first expert
  growth, freezing, and residual fine routing.
- **Hypothesis:** `B1 -> O-F -> O-HF -> O-HR` should form a positive chain;
  the corresponding learned-label chain should reproduce it and beat
  parent-preserving shuffled labels.
- **Direct result:** execution completed, but both teachers failed the
  registered final-layer semantic-readability entrance, both learned
  partitions failed the registered bootstrap-stability entrance, their
  separate post-freeze truth alignment was near chance, and all eight
  registered contrasts were `INSUFFICIENT`. All relative language guards
  passed.
- **Bounded conclusion:** the current realization did not provide an eligible
  positive test of the advisor mechanism. It cannot support either a general
  positive claim or a general refutation.
- **Next decision:** repair and revalidate the teacher entrance before another
  full hierarchy/Search run.

## 1. Objects And Metrics

| Object | Plain meaning | Concrete computation | Decision role | Cannot prove |
| --- | --- | --- | --- | --- |
| Parent label \(c\) | coarse rule family | sign of the affine coefficient: \(+u\) versus \(-u\) | first hierarchy split | natural semantic taxonomy |
| Fine label \(f\) | rule identity inside one parent | offset choice inside the fixed parent | within-parent split | global four-way linearity |
| Oracle label | generator truth | stored metadata \((c,f)\), never visible in text | positive-control supervision | autonomous discovery |
| Learned label | teacher-only candidate grouping | balanced spherical \(2\times2\) split of frozen normalized TRAIN \(h_3\) | tests label discovery | semantic truth without alignment guards |
| Effective second-layer state | representation after the inserted block-two module | pre-answer token state passed into frozen block three | primary probe input | native Gate use |
| Conditional-fine q05 margin | difficult-case within-parent readability | fit one binary L2 probe inside each true parent; compute signed margin divided by weight norm; take TEST-OOD fifth percentile and then the worse parent | primary metric; higher is better | expert utility or LM gain |
| Language guard | relative functional non-degradation | treatment-minus-control full NLL, answer NLL, and answer accuracy with paired group intervals | vetoes a geometric gain that breaks language behavior | good absolute task performance |

The probe penalty was selected once on pooled `B1` DEV-OOD candidate scores
and frozen at \(C=0.001\). Complete four-row paraphrase groups were the
independence units. Every interval used 2,000 paired bootstrap draws with equal
group counts from the two teacher seeds.

## 2. Data And Task

Each causal sequence contains an opening, three demonstrations, one query, its
answer, and an end token. The four hidden rules over \(\mathbb Z_{11}\) are
\(u+1\), \(u+3\), \(-u+3\), and \(-u+1\). Three demonstrations uniquely identify the
leaf. Coarse/fine labels remain metadata and no semantic head or probe sees the
answer token or a later state.

| Split | Rows | Complete paraphrase groups | Template role |
| --- | ---: | ---: | --- |
| TRAIN | 100,000 | 25,000 | 16 training combinations |
| DEV-ID | 8,000 | 2,000 | same 16 combinations, new contents |
| DEV-OOD | 8,000 | 2,000 | 4 unseen combinations |
| TEST-ID | 12,000 | 3,000 | same 16 combinations, new contents |
| TEST-OOD | 24,000 | 6,000 | 4 untouched combinations |

The data preflight passed rule uniqueness, exact leaf balance, complete group
size four, causal indexing, split isolation, no visible label token, and the
registered bag-of-token-count leakage limit. Dataset SHA-256 is
`ac035f9e231e534360cfdfe1e66a6612c681c700aeaad6935a4690ce0a6684cf`.

### 2.1 Post-run template-coverage audit

This diagnostic was not a result-selection rule. It locates a data confound
that matters for the next decision. Its frozen sources, hashes, computation
rule, exact template-wise accuracies, and non-verdict boundary are recorded in
[posthoc_template_coverage.json](evidence/posthoc_template_coverage.json).

- TRAIN templates `0--15` expose all demonstration/query/link markers and the
  openings `START`, `BEGIN`, and `NOTICE`, but never expose the opening token
  `CONSIDER`.
- DEV-OOD templates `16--17` contain only seen tokens in unseen combinations;
  templates `18--19` additionally contain the untrained `CONSIDER` embedding.
- Every primary TEST-OOD template `20--23` contains `CONSIDER`.
- On DEV-OOD templates `16--17`, which contain only TRAIN-seen tokens in new
  combinations, seed 1701/2903 answer accuracies were 30.23%/30.97%. The
  untrained opening is therefore not a complete explanation. Nevertheless,
  the sole primary TEST-OOD surface conflates combination generalization with
  one never-trained token embedding and must be repaired before the next
  causal test.

## 3. Model And Training

The shared teacher is a three-block decoder-only Transformer with hidden width
256, eight attention heads, feed-forward width 1,024, pre-normalization,
SwiGLU, rotary positions, tied input/output embeddings, and maximum length 64.
Both teacher seeds train for 8,000 updates using mean full-sequence next-token
cross entropy.

Every second-stage model clones and freezes its seed-matched teacher. New
modules are inserted after block two; language gradients pass through frozen
block three into the new module. Flat and hierarchical adapters match total
trainable parameters within \(9.94\times10^{-6}\) relative difference and active
adapter path multiply-adds exactly under the registered ledger.

The hierarchy trains for 500 root-only steps, 1,500 parent steps, and 2,000
fine steps. At the fine transition, the coarse Gate and parent experts are
frozen. The residual arm removes only the learned coarse Gate discriminant
direction from the fine Gate input; experts and the main residual stream keep
the full state. All hierarchical receipts recorded the registered
root/coarse/fine sequence and every coarse-freeze identity check passed.

The full registered grid ran for both seeds:

`B0`, `B1`, `O-F`, `O-HF`, `O-HR`, `O-S`, `S-F`, `S-HF`, `S-HR`,
`S-S`, `L1-SEQ`, and `L1-JOINT`, in addition to the frozen teacher `T0`.

## 4. Execution And Conformance

| Item | Registered / required | Actual | Status | Evidence |
| --- | --- | --- | --- | --- |
| ACP job | one reserved four-H100 node | `pt-exbyxhne`; `SUCCEEDED` | PASS | [execution receipt](receipts/execution_receipt.json) |
| Resource | `n6ls.iu.i40.4`, 4 H100 80GB, reserved/normal | exact match; 88 CPU, 960 GiB RAM | PASS | [execution receipt](receipts/execution_receipt.json) |
| Runtime | full scientific run | 18:11:48--18:34:10 UTC; 1,342 s | PASS | [execution receipt](receipts/execution_receipt.json) |
| Environment | CUDA-capable four-rank run | PyTorch `2.8.0a0+5228986c39.nv25.06`, CUDA 12.9, four H100 devices | PASS | raw runtime and GPU logs |
| Tests | all worker tests | 101 passed in 10.69 s | PASS | raw `logs/tests.log` |
| Final preflight | protocol, data, hardware, capacity, registry, source hashes | all checks passed; 26 source files frozen | PASS | [preflight receipt](receipts/preflight_receipt.json) |
| Teachers | two seeds, 8,000 steps | 2/2 complete; five split evaluations each | PASS | [completion receipt](receipts/completion_receipt.json) |
| Conditions | 24 full second-stage runs, 4,000 steps | 24/24 complete; five split evaluations each | PASS | [completion receipt](receipts/completion_receipt.json) |
| Distributed workers | world size four | four completion JSON records | PASS | raw `workers/rank-*.json` |
| Final artifacts | aggregate, two tables, two figures, contracts, receipts | present and hash-audited | PASS | [artifact manifest](receipts/artifact_manifest.json) |

The ACP job used no retries. Log scans found no traceback, OOM, CUDA failure,
non-finite loss, NaN, killed process, or premature exit. Warnings were limited
to scikit-learn deprecation, tensor detachment, and NCCL device-map notices;
the distributed barriers and final audit completed normally.

The copied [artifact manifest](receipts/artifact_manifest.json) is the
immutable raw-run manifest. Its internal paths such as
`results/aggregate.json` and `preflight_receipt.json` are resolved relative to
the raw full-run root stated at the top of this record, not relative to this
curated canonical directory.

## 5. Entrance Results

### 5.1 Teacher entrance

| Seed | DEV-ID answer accuracy | DEV-OOD answer accuracy | frozen \(h_3\) parent-probe balanced accuracy | raw \(h_2\) conditional-fine q05 | Entrance |
| --- | ---: | ---: | ---: | ---: | --- |
| 1701 | 1.0000 | 0.2999 | 0.5096 | -1.1308 | FAIL |
| 2903 | 1.0000 | 0.2915 | 0.5035 | -1.3084 | FAIL |

The raw second layer was not saturated, so improvement room existed. The two
required positive premises did not: neither unseen-template answer accuracy
reached 0.85 and neither third-layer parent probe reached 0.80. The global
causal verdict is therefore `INSUFFICIENT` regardless of any later local
contrast flag.

The ID/OOD gap also clarifies the full-sequence-loss question. Full-sequence
cross entropy was sufficient to reach 100% answer accuracy on new contents
under seen templates, but it did not produce compositional template
generalization in this small scratch-trained model. This run does not isolate
loss dilution from template coverage and architectural inductive bias.

### 5.2 Learned-label registered entrance and post-freeze alignment diagnostic

| Seed | Leaf fractions | Paraphrase agreement | Bootstrap AMI stability | TEST-OOD parent alignment | TEST-OOD leaf alignment | Entrance |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| 1701 | 0.2149--0.2765 | 0.9964 | 0.5377 | 0.5046 | 0.2625 | FAIL |
| 2903 | 0.2272--0.2746 | 0.9967 | 0.7628 | 0.5072 | 0.2611 | FAIL |

The candidate partitions were frozen before any Oracle field was read. Their
balance and paraphrase consistency passed, but both registered bootstrap
stability values were below 0.80, so the Search entrance failed without using
truth labels. Only after freezing, the separate Oracle-alignment diagnostic
found near binary/four-way chance agreement. The Search conditions therefore
test optimization under balanced, paraphrase-consistent but
bootstrap-unstable candidate groups, not semantic supervision by the target
hierarchy.

## 6. Primary Representation Results

All deltas are treatment minus control. Positive favors the treatment. The
registered `STABLE_POSITIVE` rule additionally requires both paired seed
deltas to be positive and the pooled 95% lower bound to exceed zero.

| Contrast | Primary delta [95% CI] | Seed 1701 / 2903 | Status | Global qualification |
| --- | ---: | ---: | --- | --- |
| `B1 -> O-F` | -0.130936 [-0.145225, -0.117843] | +0.068932 / -0.179721 | `INSUFFICIENT` | teacher entrance failed |
| `B1 -> S-F` | -0.014824 [-0.019909, -0.006437] | +0.014392 / -0.026720 | `INSUFFICIENT` | teacher and Search entrances failed |
| `O-F -> O-HF` | -0.441858 [-0.451985, -0.425010] | -0.222005 / -0.494056 | `INSUFFICIENT` | both seeds worsened; teacher entrance failed |
| `S-F -> S-HF` | -0.100163 [-0.109648, -0.092407] | -0.009137 / -0.119891 | `INSUFFICIENT` | both seeds worsened; both entrances failed |
| `O-HF -> O-HR` | +0.000537 [-0.002207, +0.002100] | +0.018272 / +0.000449 | `INSUFFICIENT` | interval crosses zero; teacher entrance failed |
| `S-HF -> S-HR` | -0.001589 [-0.003090, +0.001884] | -0.000373 / +0.000390 | `INSUFFICIENT` | seed disagreement; both entrances failed |
| `O-S -> O-HR` | -0.554912 [-0.564454, -0.538265] | -0.061431 / -0.656635 | `INSUFFICIENT` | correct labels did not beat shuffled; teacher entrance failed |
| `S-S -> S-HR` | +0.003657 [-0.000633, +0.010233] | -0.010141 / -0.001693 | `INSUFFICIENT` | interval crosses zero and both seed deltas are negative; both entrances failed |

There were no `STABLE_POSITIVE` contrasts. The absolute pooled q05 interval
for every one of the 13 conditions was below zero; see
[primary_metrics.csv](tables/primary_metrics.csv). Parent-conditioned balanced
accuracies were approximately 0.50 across conditions, consistent with the
failed low-tail geometry rather than a hidden positive result rescued by a
different threshold.

The learned-label conditions all ran as explicitly authorized even though the
Oracle and Search chains failed. They cannot be promoted by selecting a
numerically best condition after the fact.

## 7. Language-Function Guards

All eight relative guards passed. The table reports treatment-minus-control
changes. Answer-accuracy changes are percentage points.

| Contrast | Full NLL [95% CI], nats/token | Answer NLL [95% CI], nats/query | Answer accuracy [95% CI], pp | Guard |
| --- | ---: | ---: | ---: | --- |
| `B1 -> O-F` | -0.013779 [-0.014204, -0.013350] | +0.006090 [+0.002427, +0.009817] | +0.185 [+0.063, +0.304] | PASS |
| `B1 -> S-F` | -0.002826 [-0.003487, -0.002177] | -0.001464 [-0.007117, +0.004134] | +0.104 [-0.031, +0.242] | PASS |
| `O-F -> O-HF` | +0.017203 [+0.016338, +0.018038] | -0.024043 [-0.032511, -0.015339] | -0.150 [-0.325, +0.029] | PASS |
| `S-F -> S-HF` | +0.010074 [+0.009276, +0.010829] | +0.041147 [+0.034648, +0.047702] | -0.035 [-0.202, +0.113] | PASS |
| `O-HF -> O-HR` | +0.000833 [+0.000803, +0.000862] | -0.000767 [-0.001020, -0.000523] | -0.006 [-0.033, +0.021] | PASS |
| `S-HF -> S-HR` | +0.000481 [+0.000450, +0.000511] | +0.001017 [+0.000809, +0.001229] | +0.004 [-0.019, +0.027] | PASS |
| `O-S -> O-HR` | +0.005456 [+0.005266, +0.005653] | -0.010818 [-0.012461, -0.009250] | +0.017 [-0.052, +0.088] | PASS |
| `S-S -> S-HR` | -0.003394 [-0.003570, -0.003226] | +0.002169 [+0.000649, +0.003649] | +0.104 [+0.040, +0.173] | PASS |

The `O-F -> O-HF` full-NLL upper bound of 0.01804 remained below the 0.02
limit, and the `S-F -> S-HF` answer-NLL upper bound of 0.04770 remained below
the 0.05 limit. Passing these guards says only that the treatment did not add
more than the registered degradation relative to its matched control. Absolute
TEST-OOD answer accuracy remained roughly 28%--31%.

## 8. Layer-One Conditions

Both `L1-SEQ` and `L1-JOINT` completed for both seeds. Their pooled *effective
second-layer* q05 values were -1.6495 and -1.5315. They are not used to answer
whether the first layer gained target semantics because:

1. their prerequisite `S-HR` learned-label chain was ineligible;
2. the frozen primary aggregate evaluates \(h_2\), not a registered \(h_1\)
   contrast; and
3. no post-result metric is allowed to replace that missing registered test.

## 9. Figure Audit

![Primary low-tail margin](figures/primary_margin.png)

The primary figure uses the frozen condition order, one color mapping for label
source, one marker mapping for architecture, a labeled normalized-margin axis,
and a visible zero reference. The intervals are small but visible at original
resolution. Allowed conclusion: compare held-out synthetic second-layer
low-tail geometry only.

![Language guard](figures/language_guard_nll.png)

The auxiliary figure uses the same registered contrast order, identifies full
and answer NLL markers, and displays both upper guard lines on one common NLL
axis. It omits the answer-accuracy guard; the full three-part judgment comes
from Section 7 and [aggregate.json](evidence/aggregate.json).

The frozen plot contracts are preserved in
[figure_contracts.json](figures/figure_contracts.json). Both rendered images
were visually inspected after completion. Neither plot can establish native
Router readability, expert utility, or open-domain semantics.

## 10. Result Interpretation

### Direct observation

- The approved execution is complete and reproducible at the receipt level.
- The teachers learned perfect ID answer behavior but failed unseen-template
  answer and third-layer parent-semantic entrances.
- Correct flat semantic supervision did not give a stable paired-seed gain.
- The staged hierarchy was worse than flat supervision in both Oracle seeds.
- Residual fine-Gate input was statistically indistinguishable from full-state
  fine-Gate input.
- Correct Oracle fine labels did not beat the shuffled-fine control.
- Learned labels failed the registered stability entrance; their separate
  post-freeze target-alignment diagnostic was near chance, so every Search
  comparison is diagnostic only.

### Bounded inference

The current experiment cannot adjudicate the advisor's intended
final-layer-semantic-to-earlier-layer mechanism because it did not establish
the registered DEV-OOD linear-readability entrance for target parent semantics
at the final layer. The Oracle branch adds a second warning: even directly
supplied truth did not make this particular frozen-backbone, adapter,
objective, and template split produce robust OOD \(h_2\) fine separation. That
narrows the failure to the present data/model/supervision/optimization package;
it does not show that target information was absent under every possible
readout, and it does not identify which component is causal.

### Strongest rival explanations still open

- template-combination generalization and the untrained `CONSIDER` embedding;
- full-sequence cross entropy emphasizing surface prediction rather than a
  reusable explicit rule identity;
- a three-block scratch model solving ID answers without linearly organizing
  the registered parent/fine semantics;
- semantic-gradient calibration at the registered fixed strength;
- the inserted module and hard routing optimization rather than the advisor's
  abstract mechanism.

No post-run evidence separates these rivals. They must not be collapsed into
one causal story.

## 11. Claim Boundary

- The q05 margin measures linear probe readability of the effective second
  layer. It does not prove the deployed Gate reads the same variable.
- A passed language guard is non-degradation relative to a matched poor OOD
  baseline, not language-function gain.
- Unseen templates are not unseen rules, natural-language semantics, or
  open-domain generalization.
- `O-F -> O-HF` tests a package of hierarchy, staging, and freezing; it does
  not isolate the necessity of freezing.
- Residual routing removes one learned coarse discriminant only; it is not a
  complete common-semantic-subspace removal.
- Frozen Search clusters cannot be called semantic when their stability and
  Oracle alignment fail.
- Two paired seeds establish neither a broad seed-population theorem nor
  equivalence between conditions.
- This experiment provides no evidence about expert functional specialization,
  expert utility, native Gate behavior, training speed, or compute savings.
- Failure of this realization cannot refute the advisor's general intuition.

## 12. Next Decision And Stop Rule

The next experiment is an entrance repair, not another full hierarchy sweep.

1. Rebuild the template split so every surface token occurs in TRAIN while
   DEV-OOD and TEST-OOD hold out only compositional combinations.
2. Keep the three-block teacher and full-sequence cross entropy fixed, so the
   first comparison isolates the data entrance rather than changing several
   mechanisms together.
3. Run only the two teachers. Stop if either fails DEV-OOD answer accuracy
   0.85 or frozen \(h_3\) parent balanced accuracy 0.80.
4. If both pass, run only `B1` and `O-F`. Stop unless the paired-seed q05 delta
   is positive in both seeds, its pooled lower interval exceeds zero, and all
   function guards pass.
5. Reopen `O-HF/O-HR` and learned-label Search only after this positive control
   passes.

This is one decision: establish a valid high-layer semantic and Oracle
positive-control entrance before spending another full run on the advisor's
staged mechanism.

## 13. Artifact Map

### Canonical curated evidence

- [aggregate.json](evidence/aggregate.json)
- [post-hoc template-coverage diagnostic](evidence/posthoc_template_coverage.json)
- [primary_metrics.csv](tables/primary_metrics.csv)
- [registered_contrasts.csv](tables/registered_contrasts.csv)
- [primary_margin.png](figures/primary_margin.png)
- [language_guard_nll.png](figures/language_guard_nll.png)
- [figure_contracts.json](figures/figure_contracts.json)
- [preflight receipt](receipts/preflight_receipt.json)
- [completion receipt](receipts/completion_receipt.json)
- [raw-run artifact manifest copy](receipts/artifact_manifest.json) (internal
  paths resolve against the raw full-run root)
- [data manifest](receipts/data_manifest.json)
- [execution receipt](receipts/execution_receipt.json)
- [Search receipts](receipts/search_1701.json),
  [seed 2903](receipts/search_2903.json), and post-freeze alignment ledgers for
  [1701](receipts/search_alignment_1701.json) and
  [2903](receipts/search_alignment_2903.json)

### Raw evidence retained in the worker run

The raw root preserves all teacher and condition checkpoints, five-split
representation arrays, training curves, semantic-lambda ledgers,
root/coarse/fine stage ledgers, coarse-freeze checks, four distributed worker
receipts, and complete logs. These large artifacts are intentionally not
copied into the research mainline.
