# Detailed: A11_13 Downstream Semantic-State Validity

Primary anchor: [11_13_downstream_semantic_state_validity_anchor.md](../../../problem_anchors/11_informative_future_branch_mechanism/11_13_downstream_semantic_state_validity_anchor.md)
Protocol: [protocol.md](protocol.md)
Summary: [summary.md](summary.md)

## 0. Quick Recap

**Purpose:** define a downstream-relevant object for A11 before comparing MTP and NTP.

**Decision question:** does a paired long-horizon assistant task measure use of a distant semantic state rather than local evidence, answer position, or simple lexical matching?

**Conclusion:** supported for the declared controlled task. Five complete seeds have $Q_{task}=1.0$. Local and cue views each have Bayes accuracy `0.5` and mutual information `0`; every paired intervention guard passes; the strongest surface baseline is `0.5375`.

**Boundary:** this is construct validity, not model or method evidence.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete computation | Decision role | Cannot prove |
|---|---|---|---|---|
| semantic state $Z$ | early meaning that constrains a later valid action | one of two states in each assistant domain | causal object | all natural-language meaning |
| local context $L$ | current request and two candidate actions | exact shared suffix within a counterfactual group | local insufficiency | model attention locality |
| paraphrase group | four cues expressing the same state | fixed state, request, option order, filler, and horizon | surface invariance | perfect human equivalence |
| counterfactual group | two opposite states with identical later text | fixed request, option order, filler, horizon, and paraphrase index | causal dependence | real-user causality |
| empirical Bayes accuracy | best possible label accuracy from exact input signatures | $\sum_xp(x)\max_yp(y\mid x)$ | deterministic leakage audit | neural learnability |
| mutual information | statistical dependence between a view and answer index | empirical $I(Y;X)$ in bits | leakage audit | semantics by itself |
| $Q_{task}$ | weakest normalized validity component | minimum of six scores | primary decision | MTP benefit |

## 2. Why Existing Benchmarks Do Not Close This Decision

The task target is motivated by real long-context evaluation but requires stronger causal controls than the existing releases provide.

| Resource | Useful property | Missing for A11 causal identification |
|---|---|---|
| [NoLiMa](https://arxiv.org/abs/2502.05167) | removes literal query-needle matching | remains associative retrieval; no behavior-changing state pairs |
| [RULER](https://arxiv.org/abs/2404.06654) | includes variable tracing and aggregation beyond simple retrieval | synthetic task suite without paraphrase/counterfactual assistant constraints |
| [BABILong](https://arxiv.org/abs/2406.10149) | distributes reasoning facts through long natural text | no matched semantic-state intervention |
| [LongMemEval](https://arxiv.org/abs/2410.10813) | realistic assistant histories with preference, temporal, update, and abstention questions | no controlled paraphrase and state-counterfactual pairs |
| [LoCoMo-Plus](https://arxiv.org/abs/2602.10715) | directly targets implicit goals, states, values, and causal constraints under cue-trigger semantic disconnect | released cognitive subset has no unique reference action and no matched intervention pairs |

The official LoCoMo-Plus release contains 401 cue-trigger examples: 101 causal and 100 each for state, goal, and value. It is an important external target, but its open-ended judge-based setup cannot by itself determine whether an MTP/NTP difference came from the intended state intervention.

## 3. Protocol Compliance

| Protocol item | Actual | Status |
|---|---:|---|
| seeds | 971-975 | pass |
| examples per seed | 640 | pass |
| total examples | 3,200 | pass |
| semantic domains | 5 | pass |
| states per domain | 2 | pass |
| cue paraphrases per state | 4 | pass |
| later requests per domain | 4 | pass |
| option orders | 2 | pass |
| horizon targets | 256 and 1,024 words | pass |
| counterfactual groups | 320 per seed | pass |
| paraphrase groups | 160 per seed | pass |
| exact reproducibility | 5/5 | pass |
| central figure audit | readable, labels and thresholds visible | pass |

The only protocol extension after the first smoke run was a stronger shortcut control: cue-to-option TF-IDF similarity. It directly tests the rival explanation that the answer can be chosen by surface overlap. The decision threshold and task did not change after seeing the full run.

## 4. Data And Mathematical Contract

### 4.1 Factorial construction

For each seed:

$$
5\text{ domains}\times2\text{ states}\times4\text{ cues}
\times4\text{ requests}\times2\text{ orders}\times2\text{ horizons}=640.
$$

The answer is the position of the state-consistent action after independent option permutation. Filler depends only on seed, domain, request, and horizon. It never depends on state or answer.

### 4.2 Operational definition

$$
X=(C_Z,D,L),
\qquad
Y=f(Z,L).
$$

Paraphrase invariance:

$$
f(C_Z,D,L)=f(C'_Z,D,L).
$$

Counterfactual dependence:

$$
f(C_Z,D,L)\ne f(C_{Z'},D,L),
\qquad Z'\ne Z.
$$

Local insufficiency:

$$
I(Y;L)=0.
$$

Cue-only answer-index insufficiency:

$$
I(Y;C_Z)=0.
$$

The cue is semantically necessary, but the cue alone cannot reveal whether its preferred action was placed at A or B.

### 4.3 Primary score

For chance $c=0.5$:

$$
B_{view}=1-\frac{A^*_{view}-c}{1-c}.
$$

Distance score:

$$
H_d=\min\left(1,\frac{\min_i d_i}{256}\right).
$$

Joint validity:

$$
Q_{task}=\min\{A_{oracle},C_{para},S_{cf},B_{local},B_{cue},H_d\}.
$$

## 5. Complete Results

### 5.1 Per-seed construct metrics

| Seed | $A_{oracle}$ | $C_{para}$ | $S_{cf}$ | local Bayes | cue Bayes | local MI | cue MI | min distance | $Q_{task}$ |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 971 | 1.0 | 1.0 | 1.0 | 0.5 | 0.5 | 0 | 0 | 294 | 1.0 |
| 972 | 1.0 | 1.0 | 1.0 | 0.5 | 0.5 | 0 | 0 | 294 | 1.0 |
| 973 | 1.0 | 1.0 | 1.0 | 0.5 | 0.5 | 0 | 0 | 294 | 1.0 |
| 974 | 1.0 | 1.0 | 1.0 | 0.5 | 0.5 | 0 | 0 | 294 | 1.0 |
| 975 | 1.0 | 1.0 | 1.0 | 0.5 | 0.5 | 0 | 0 | 294 | 1.0 |

The answer is globally balanced and balanced within every domain, request, option order, exact local signature, and exact cue signature.

### 5.2 Pair audit

| Pair type | Groups per seed | Total groups | Valid groups | Score |
|---|---:|---:|---:|---:|
| counterfactual | 320 | 1,600 | 1,600 | 1.0 |
| paraphrase | 160 | 800 | 800 | 1.0 |

For counterfactual groups, filler and local text are byte-identical, states differ, and labels differ. For paraphrase groups, state, filler, and local text are identical, cue strings differ, and labels agree.

### 5.3 Shortcut baselines

| Condition | Mean accuracy | Maximum | Decision |
|---|---:|---:|---|
| majority | 0.5000 | 0.5000 | pass |
| local-only word/bigram | 0.5000 | 0.5000 | pass |
| cue-only word/bigram | 0.5000 | 0.5000 | pass |
| full-text word/bigram | 0.5000 | 0.5000 | pass |
| cue-option TF-IDF similarity | 0.5375 | 0.5375 | pass |

The linear full-text classifier cannot represent the state-by-option-order interaction reliably, so the cue-option similarity control was added to test a different and stronger lexical path. It remains below the `0.60` ceiling, but its nonzero advantage is a warning: the task still contains ordinary semantic lexical relations and is not an adversarial no-overlap benchmark.

## 6. Qualitative Sample Audit

The [sample sheet](sample_sheet.md) exposes one held-out cue for both states in every domain with the identical local decision and filler hash. The examples are grammatical, the two candidate actions are concrete, and state interventions change which action is appropriate without changing the later text.

Remaining qualitative limitations:

- cues and actions are manually templated rather than naturally logged conversations;
- binary choices simplify the action space;
- the filler is grammatical but generic and does not evolve the relevant state;
- the audit does not include contradictory later state updates;
- the supplied paraphrases are curated, not independently human-rated.

These limitations keep A11_13 below a claim about open-ended conversational memory.

## 7. Visualization Results

### Plot Contract

**Question:** does the task satisfy every construct clause while resisting declared surface shortcuts?
**Metrics:** six normalized validity components, held-out-paraphrase baseline accuracy, exact-view Bayes accuracy, minimum whitespace-token distance, and $Q_{task}$.
**Data source:** five complete generated datasets and their audit tables.
**Aggregation:** mean and seed standard deviation; exact per-seed values for Bayes, distance, and $Q_{task}$.
**Axes:** normalized score or accuracy on y; condition or seed on x.
**Allowed conclusion:** the fixed task passes its construct-validity gate.
**Limitation:** the figure contains no neural MTP/NTP result.

![A11_13 construct validity](figures/a11_13_construct_validity.png)

**Observed result:** all validity bars are 1.0. The similarity shortcut is slightly above chance at 0.5375 but below the 0.60 ceiling. Both exact-view Bayes bars equal chance. Minimum distance exceeds the declared 256-word window by 38 words.

**Rendered-artifact audit:** the figure renders, all labels and thresholds are readable, and the important values can be understood without reading source code.

## 8. Hypothesis Decisions

| Hypothesis | Evidence | Decision |
|---|---|---|
| H1 local and cue insufficiency | Bayes `0.5`; MI `0` in 5/5 | supported |
| H2 invariance and state dependence | all 2,400 groups pass | supported |
| H3 distance and shortcut guards | min distance `294`; max lexical `0.5375` | supported |

Overall status: **supported**.

## 9. Claim Boundary

**Established:** a fixed, auditable controlled natural-language proxy for distant assistant-state use.

**Not established:** neural solvability; representation quality; NTP or MTP learning efficiency; open-ended response validity; robustness to natural conversation; external benchmark transfer.

## 10. Artifact Map And Reproduction

Code workspace:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding
```

Config:

```text
configs/a11_13_downstream_semantic_state_validity.json
```

Runner and analyzer:

```text
scripts/run_a11_13_downstream_semantic_state_validity.py
scripts/analyze_a11_13_downstream_semantic_state_validity.py
```

Valid result directory:

```text
results/a11_13_downstream_semantic_state_validity/
a11_13_downstream_semantic_state_validity_20260710_171747
```

Execution surface: local CPU. Four remote GPUs were intentionally not used because this anchor has no neural workload.

Reproduction:

```bash
python scripts/run_a11_13_downstream_semantic_state_validity.py \
  --config configs/a11_13_downstream_semantic_state_validity.json \
  --output-dir results/a11_13_downstream_semantic_state_validity/<run_id>

python scripts/analyze_a11_13_downstream_semantic_state_validity.py \
  --run-dir results/a11_13_downstream_semantic_state_validity/<run_id> \
  --output-dir results/a11_13_downstream_semantic_state_validity/<run_id>/analysis
```

Canonical evidence files:

- [construct metrics](tables/construct_metrics.csv)
- [shortcut summary](tables/shortcut_baseline_summary.csv)
- [coverage audit](tables/coverage_audit.csv)
- [decision JSON](hypothesis_decision.json)
- [sample sheet](sample_sheet.md)
- [central figure](figures/a11_13_construct_validity.png)

## 11. Next Decision

Proceed to A11_14, but keep its claim narrow: a small causal language model on the fixed 256-word-horizon subset. Use the same standard H1 answer accuracy for both methods, and compare time-to-threshold and AUC under matched data tokens and backbone updates. If neither method solves held-out paraphrases, the result is a model-capacity or transfer failure and cannot adjudicate MTP efficiency.

