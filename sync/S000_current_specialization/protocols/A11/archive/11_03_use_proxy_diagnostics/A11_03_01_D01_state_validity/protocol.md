# Protocol: A11_13 Downstream Semantic-State Validity

## 0. Approval Snapshot

**Approval status:** approved for implementation under the user's standing instruction for subsequent A11 anchors.  
**Purpose:** decide whether a paired persistent-assistant task is a valid downstream proxy for long-horizon semantic-state use.  
**Primary anchor:** `11_13_downstream_semantic_state_validity_anchor.md`.  
**Decision question:** does the task isolate a distant behaviorally relevant state rather than retrieval, local context, or answer-position shortcuts?  
**Physical prior:** meaning relevant to A11 should be paraphrase invariant, counterfactually state dependent, and locally insufficient.  
**Core model:** $X=(C_Z,D,L)$ and $Y=f(Z,L)$.  
**Falsifier:** valid implementation but $Q_{task}<0.95$, local/cue Bayes accuracy above chance, failed pair intervention, or held-out-paraphrase lexical accuracy above `0.60`.  
**Experiment role:** task and metric construct-validity audit; no method comparison.  
**Primary metric:** $Q_{task}=\min\{A_{oracle},C_{para},S_{cf},B_{local},B_{cue},H_d\}$.  
**Minimal setup:** five binary assistant domains, four cue paraphrases per state, four local requests per domain, two option orders, two horizon lengths, five seeds.  
**Pass:** all exact guards pass and every seed has $Q_{task}\ge0.95$; all lexical baselines are `<=0.60`.  
**Fail:** any intended intervention relation is false or local/cue context contains the answer index.  
**Insufficient:** missing pairs, unbalanced options, incomplete coverage, or nonreproducible data.  
**Cannot claim:** MTP superiority, LLM sample efficiency, natural open-ended assistant quality, or transfer to external benchmarks.

## 1. Terminology / Definitions

| Term | Plain meaning | Computation | Unit | Decision use | Cannot prove |
|---|---|---|---|---|---|
| cue $C_Z$ | early language expressing a user state | one of four paraphrases for state $Z$ | text | provides distant semantic evidence | realism by itself |
| local context $L$ | final request and two actions | exact shared suffix within a counterfactual pair | text | local-insufficiency test | attention locality |
| paraphrase pair | same state, different wording | same domain/request/order/filler and $Z$ | pair | surface-invariance test | perfect semantic equivalence |
| counterfactual pair | opposite state, same later text | same domain/request/order/filler, $Z\ne Z'$ | pair | causal-state test | real-world causality |
| empirical Bayes accuracy | best accuracy possible from exact input signatures | $\sum_xp(x)\max_y p(y\mid x)$ | proportion | detects deterministic leakage | neural learnability |
| empirical mutual information | answer-index dependence on an input view | $I(Y;X)$ | bits | detects statistical leakage | semantic quality |
| lexical baseline | word/bigram logistic classifier | held-out paraphrase family | accuracy | detects simple wording shortcuts | all possible shortcuts |

## 2. Anchor Alignment

This protocol tests only the construct validity of one downstream task. It does not train NTP or MTP. Passing licenses A11_14; failing blocks it.

## 3. Data Contract

Five domains each contain two opposite behaviorally relevant states:

| Relation family | $Z=0$ | $Z=1$ | Later decision |
|---|---|---|---|
| goal | minimize cost | minimize time | choose cheaper or faster plan |
| state | low energy | high energy | choose restorative or active plan |
| value | protect privacy | enable sharing | choose private or shareable workflow |
| preference | quiet focus | social collaboration | choose quiet or collaborative setting |
| availability | mornings free | evenings free | choose morning or evening slot |

For each domain:

- four cue paraphrases per state;
- four request templates with two semantically distinct candidate actions;
- both candidate-action orders;
- target filler lengths `256` and `1024` whitespace-delimited tokens;
- every state is crossed with every request, order, and horizon.

The answer label is the position of the state-consistent action after option permutation. Filler text is generated independently of state and answer.

Expected examples per seed:

$$
5\times2\times4\times4\times2\times2=640.
$$

## 4. Metrics

### 4.1 Primary construct-validity score

$$
Q_{task}=\min\{A_{oracle},C_{para},S_{cf},B_{local},B_{cue},H_d\}.
$$

For binary chance $c=0.5$:

$$
B_{view}=1-\frac{A^*_{view}-c}{1-c}.
$$

`view` is either local suffix or cue alone. Values are clipped to $[0,1]$.

### 4.2 Pair metrics

$$
C_{para}=|P|^{-1}\sum_{(i,j)\in P}\mathbf1[Y_i=Y_j],
$$

$$
S_{cf}=|F|^{-1}\sum_{(i,j)\in F}\mathbf1[Y_i\ne Y_j].
$$

Pair guards additionally require all nonintervened fields to be byte-identical.

### 4.3 Horizon score

$$
H_d=\min(1,\min_i d_i/W),\qquad W=256.
$$

Distance $d_i$ counts whitespace-delimited tokens between the end of the cue and the answer marker. This is a dataset-audit unit, not a claim about a specific model tokenizer.

### 4.4 Shortcut metrics

- empirical Bayes accuracy and empirical mutual information for `local_text`, `cue_text`, and `option_order`;
- answer balance globally, per domain, and per exact local signature;
- word/bigram logistic regression on local-only, cue-only, and full text;
- unsupervised cue-to-option TF-IDF similarity, which chooses the candidate with larger lexical cosine;
- train paraphrase indices `{0,1}`, test indices `{2,3}`;
- five model seeds `971-975`.

## 5. Conditions And Comparisons

| Condition | Input to baseline | What it tests | Expected result |
|---|---|---|---|
| majority | no text | global label balance | `0.50` |
| local-only | request and options | local leakage | `<=0.60`, Bayes exactly `0.50` |
| cue-only | early cue | answer-index leakage through cue | `<=0.60`, Bayes exactly `0.50` |
| full lexical | cue, filler, request, options | simple noncompositional word shortcut | `<=0.60` on unseen paraphrases |
| cue-option similarity | cue versus each candidate action | direct lexical matching shortcut | `<=0.60` on unseen paraphrases |
| metadata oracle | state and option mapping | deterministic solvability | `1.00` |

The full lexical baseline is a shortcut guard, not an expected capable model. A future neural model may legitimately solve the task by composing cue meaning with candidate actions.

## 6. Exact Validity Guards

1. exactly 640 examples per seed and complete factorial coverage;
2. every counterfactual pair has identical filler/local text and opposite state/label;
3. every paraphrase pair has identical state/filler/local text and equal label;
4. global, domain, request, and exact-local answer balance is `0.50`;
5. filler hashes are independent of state and label within matched groups;
6. minimum cue-to-answer distance is at least 256 whitespace tokens;
7. no answer label or state identifier appears in rendered text or sample IDs exposed to baselines;
8. generated data and aggregate tables are byte-reproducible from config and seed.

## 7. Implementation And Run Plan

Code workspace:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/
active/synthetic_data_understanding/
```

Planned files:

```text
configs/a11_13_downstream_semantic_state_validity.json
scripts/run_a11_13_downstream_semantic_state_validity.py
scripts/analyze_a11_13_downstream_semantic_state_validity.py
```

Execution stages:

1. syntax/config validation;
2. one-seed reduced smoke run;
3. full five-seed CPU run because the audit contains no neural GPU workload;
4. aggregate analysis and rendered-figure inspection;
5. write `summary.md`, `detailed.md`, and update the anchor/story.

Using four remote GPUs would not add evidence to this anchor and is therefore intentionally deferred to A11_14.

## 8. Required Outputs

- `dataset.jsonl` for each seed;
- `construct_metrics.csv`;
- `pair_audit.csv`;
- `shortcut_baselines.csv`;
- `coverage_audit.csv`;
- `sample_sheet.md`;
- `hypothesis_decision.json`;
- `figures/a11_13_construct_validity.png`;
- canonical `summary.md` and `detailed.md`.

## 9. Decision Rules

**Supported:** every exact guard passes; every seed has $Q_{task}\ge0.95$; local/cue Bayes accuracy is `0.50`; their mutual information is at most `1e-10` bits; all held-out-paraphrase lexical baselines are `<=0.60`.

**Weakened:** exact causal construction passes but at least one lexical baseline exceeds `0.60`; A11_14 remains blocked until the shortcut is repaired.

**Falsified:** local/cue Bayes accuracy exceeds chance, $C_{para}<1$, $S_{cf}<1$, or oracle accuracy is below `1`.

**Insufficient:** coverage, pair identity, horizon, or reproducibility guard fails.

## 10. Claim Boundary And Next Action

Passing this protocol establishes a valid controlled natural-language downstream proxy, not an MTP result. The next and only next action is A11_14: compare NTP and K=2 MTP on the frozen task under matched examples, tokens, architecture, optimizer, and evaluation schedule.
