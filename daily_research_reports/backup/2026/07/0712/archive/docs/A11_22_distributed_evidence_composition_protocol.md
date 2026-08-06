# A11_22 Distributed-Evidence Composition Paired Protocol

Status: proposed protocol; do not run before anchor approval.  
Anchor: `A11_22_distributed_evidence_composition_anchor.md`.  
Scope: one paired synthetic-real mechanism audit. No horizon sweep, Router method, MoE training, or LongBench v2 tuning.

## 1. Experiment Purpose

The experiment tests whether the workload model

$$
\text{distributed evidence}
+
\text{correct binding}
+
\text{operator composition}
+
\text{cross-position use}
$$

captures a mechanism that transfers from controlled data to a real multi-document QA task.

It compares:

1. NTP;
2. informative MTP (`MTP-info`);
3. masked informative MTP (`MTP-mask`).

The experiment is not a general benchmark comparison. It tests one causal statement:

> Direct future supervision of a necessary compositional variable improves a causally used decision representation, and the same improvement appears in both synthetic and real data.

## 2. Pre-Registered Decision Rule

Primary metric:

$$
T_{\mathrm{pair}}
=
\min(\Delta Q^{\mathrm{syn}},\Delta Q^{\mathrm{real}}),
$$

with

$$
\Delta Q^x
=
Q_{\mathrm{comp}}^x(\mathrm{MTP-info})
-
\max
\left[
Q_{\mathrm{comp}}^x(\mathrm{NTP}),
Q_{\mathrm{comp}}^x(\mathrm{MTP-mask})
\right].
$$

### Support

Declare support only if:

1. the paired bootstrap 95% confidence lower bound of $T_{\mathrm{pair}}$ is positive;
2. the sign is positive in at least 4/5 seeds;
3. the same condition improves causal intermediate-state use on synthetic and real data;
4. the decision-state improvement is preserved to the answer position;
5. all construct-validity and local-language guards pass.

### Falsify

Declare the workload-mechanism story falsified or weakened if:

1. synthetic gain does not transfer to real data;
2. `MTP-mask` matches `MTP-info`;
3. task accuracy improves without the declared representation/causal mechanism;
4. the real task is solvable from a single support document;
5. decision-state gains are erased before answer generation.

### Insufficient

Declare insufficient if the primary small model is near chance, the data controls fail, or confidence intervals cannot determine the sign.

## 3. Benchmark And Real-Data Source

### 3.1 Benchmark target

The target workload is the multi-document compositional QA family represented in LongBench.

### 3.2 Trainable real-data source

Use 2WikiMultiHopQA because it provides multiple supporting documents, annotated supporting evidence, a reasoning path, train/held-out splits, and a natural mapping to relation-composition variables.

Use the original training split for training and a held-out split for evaluation. Convert examples to the LongBench input/output format for scoring.

LongBench v2 is reserved for a later external transfer check. It must not be used for training, hyperparameter selection, prompt selection, or early stopping in A11_22.

## 4. Shared Structured Serialization

The synthetic and real tasks must use the same decision interface.

### 4.1 Input

```text
<CONTEXT>
[passage 1]
...
[passage n]
</CONTEXT>
<QUESTION>
...
</QUESTION>
<DECIDE>
```

### 4.2 Target

```text
<E1=...> <E2=...> <OP=...> <Z=...> <ANS=...>
```

The exact tokens may be implemented as reserved vocabulary tokens or canonical short strings. They must be unambiguous under the tokenizer.

Purpose of each field:

| Field | Meaning |
|---|---|
| `E1`, `E2` | selected supporting relations/entities |
| `OP` | required composition operator |
| `Z` | intermediate composition result |
| `ANS` | final answer |

The natural-language answer may follow the structured fields, but the primary task score uses `ANS`.

### 4.3 Informative horizons

At the hidden state of `<DECIDE>`, the future positions containing `E2`, `OP`, `Z`, or `ANS` are declared task-informative only after checking:

$$
I(Z;Y_{T+j}\mid Y_{T+1:T+j-1})>0
$$

under the generated data distribution.

The chosen $K$ must cover the first declared informative field needed for the hypothesis. Fix this $K$ before training. Do not sweep it.

## 5. Synthetic Data Construction

### 5.1 Evidence graph

Generate two evidence branches:

$$
r_1(a,b),\qquad
r_2(b,c),
$$

or an equivalent two-branch shallow tree when a final binary operator is required.

The answer is produced by a declared operator:

$$
Z=g_{\mathrm{op}}(E_1,E_2),\qquad
Y=h(Z,Q).
$$

Primary operator family:

- relation composition;
- one final comparison or selection operator only if needed to prevent direct endpoint lookup.

Do not mix many operator families in the first run.

### 5.2 Context

Each example contains:

- exactly two necessary support passages;
- topic-matched distractor passages;
- randomized support positions;
- randomized surface forms;
- controlled total length.

Primary fixed setting:

```text
support count: 2
composition depth: 2
context length: one fixed nontrivial length
decision-reveal latency: one fixed value
```

Do not sweep length, depth, or latency. Their independent control is an implementation guard; the first run uses one setting.

### 5.3 Shortcut controls

Create paired controls:

1. `one_support_1`: only first support retained;
2. `one_support_2`: only second support retained;
3. `support_delete`: one support deleted;
4. `support_order`: support order permuted;
5. `distractor_replace`: distractors replaced but supports unchanged;
6. `evidence_swap`: one support replaced with another valid support and answer recomputed;
7. `lexical_template_split`: held-out surface templates.

The generated data is valid only if a symbolic solver reaches 100% and each local-only control stays below the preregistered shortcut threshold.

## 6. Real Data Construction

### 6.1 Example filtering

Keep only examples with:

- complete annotated supporting path;
- exactly identifiable two-hop relation chain;
- answer recoverable from the declared path;
- no answer string trivially repeated in the question;
- no support annotation conflict.

Log all filtering counts and reasons.

### 6.2 Long-context packing

For each example:

1. retain all gold support documents;
2. add topic-matched non-support documents;
3. randomize document order;
4. place support documents across early, middle, and late context positions;
5. keep total token length within the model's supported window.

Use one fixed target context length in the primary run.

### 6.3 Real controls

Construct:

- one-support variants;
- support-deletion variants;
- support-order permutations;
- distractor replacements;
- evidence-swap variants where a valid answer can be recomputed or selected from a matched example.

Evidence-swap examples must be manually audited on a small random sample before full generation.

### 6.4 Split discipline

- training: original training examples only;
- validation: fixed held-out subset for early stopping;
- test: disjoint held-out examples;
- no LongBench v2 test use;
- no test-template or test-answer leakage into synthetic generation.

## 7. Model And Training

### 7.1 Primary backbone

Use the existing Qwen3-0.6B A11 infrastructure.

Reason:

- it already demonstrated nontrivial held-out task capability;
- it avoids repeating the random-small-model failure;
- it permits direct comparison with prior A11 observations.

### 7.2 Capability gate

Before objective comparison, evaluate the frozen/pretrained or minimally formatted model on a 100-example real pilot.

The full run is interpretable only if:

- output formatting succeeds on at least 90% of examples after supervised warm-up;
- full-context answer accuracy is measurably above the strongest local-only baseline;
- the model does not collapse to one output class.

Failure means the model/task pair is below the capability threshold. Do not interpret objective differences.

### 7.3 Parameter update

Primary: full-parameter training.

Parameter-efficient adaptation may be logged as exploratory, but cannot support shared-parameter gradient or capacity claims.

### 7.4 Matched training budget

Match across all three conditions:

- training examples;
- token order;
- batch composition;
- optimizer;
- learning-rate schedule;
- backbone update count;
- random seeds;
- evaluation checkpoints.

Report the extra head compute and loss terms for MTP separately. Do not call the comparison equal-FLOP unless it is explicitly normalized.

### 7.5 Seeds

Primary seeds:

```text
1201, 1202, 1203, 1204, 1205
```

Use identical data-order seeds across conditions.

## 8. Objective Conditions

### 8.1 NTP

$$
L_{\mathrm{NTP}}
=
\sum_t
\operatorname{CE}(q_1(\cdot\mid H_t),Y_{t+1}).
$$

### 8.2 MTP-info

$$
L_{\mathrm{MTP-info}}
=
\sum_t\sum_{j=1}^{K}
\lambda_j
\operatorname{CE}(q_j(\cdot\mid H_t),Y_{t+j}).
$$

At `<DECIDE>`, the declared informative horizons are active.

### 8.3 MTP-mask

Use the same architecture, $K$, heads, and ordinary all-position losses as `MTP-info`, but set the weights of the declared task-informative `<DECIDE>`-position horizons to zero.

This is the primary causal control.

### 8.4 No extra conditions

Do not add:

- alternative $K$;
- alternative bridge tokens;
- loss-weight sweep;
- head-freezing sweep;
- training-duration sweep;
- MoE or Router conditions.

## 9. Measurements

### 9.1 Full-context task accuracy

$$
A_{\mathrm{full}}
=
\Pr[\hat Y=Y]
$$

using exact match or the benchmark's canonical normalized answer metric.

### 9.2 Local-only excess accuracy

Let $A_{\mathrm{one}}$ be the stronger of the two one-support conditions.

$$
\operatorname{ExcessAcc}_{\mathrm{one}}
=
\max
\left(
0,
\frac{A_{\mathrm{one}}-A_{\mathrm{chance}}}
{1-A_{\mathrm{chance}}}
\right).
$$

This measures shortcut success beyond chance.

### 9.3 Evidence-swap consistency

For a valid evidence-swap pair $(x,y)\rightarrow(x',y')$,

$$
C_{\mathrm{swap}}
=
\Pr[\hat Y(x)=y\ \land\ \hat Y(x')=y'].
$$

This is stricter than ordinary accuracy because the model must respond correctly to a causal evidence change.

### 9.4 Guarded compositional score

$$
Q_{\mathrm{comp}}
=
\min
\left(
A_{\mathrm{full}},
C_{\mathrm{swap}},
1-\operatorname{ExcessAcc}_{\mathrm{one}}
\right).
$$

Primary task score for both synthetic and real data.

### 9.5 Necessary-evidence probe

Train a probe from $H_T$ to the declared evidence variables $E_1,E_2$.

Report:

- held-out probe accuracy;
- majority baseline;
- lexical-template held-out accuracy;
- probe regularization and dimensionality.

Probe accuracy is a decodability metric only.

### 9.6 Intermediate-variable probe

Train a probe from $H_T$ to $Z$.

Report accuracy and cross-template generalization.

### 9.7 Causal hidden-state patching

For matched examples differing only in one evidence variable:

1. extract the task-relevant representation component from the source;
2. patch it into the target at $H_T$;
3. measure whether the answer changes to the source-consistent answer.

Define:

$$
C_{\mathrm{patch}}
=
\Pr[\text{patched output follows patched }Z].
$$

Use a random-direction patch and norm-matched patch as controls.

### 9.8 Distractor invariance

For contexts with identical supports and different distractors:

$$
S_{\mathrm{inv}}
=
1-
\frac{
d(\Pi_{\mathrm{task}}H_T(E,D),\Pi_{\mathrm{task}}H_T(E,D'))
}{
d(\Pi_{\mathrm{task}}H_T(E,D),\Pi_{\mathrm{task}}H_T(E',D))+\epsilon
}.
$$

Clip only for visualization; retain raw ratios for analysis.

### 9.9 Decision-to-answer preservation

Let $v_{\mathrm{task}}$ be a fixed task direction estimated on training data.

$$
P_{T\rightarrow A}
=
\operatorname{corr}
\left(
v_{\mathrm{task}}^\top H_T,
v_{\mathrm{task}}^\top H_A
\right)
$$

across matched examples and checkpoints.

Also report sign preservation under evidence swaps.

### 9.10 Task-gradient alignment

At fixed checkpoints, compute:

$$
\Gamma_{\mathrm{task}}
=
\left\langle
-\nabla_\theta L_{\mathrm{extra}},
-\nabla_\theta L_{\mathrm{heldout\ task}}
\right\rangle
$$

and cosine-normalized alignment.

Use the same held-out minibatch across conditions.

This metric is a local mechanism guard. It cannot prove a finite-step gain.

### 9.11 Local language-model guards

Report:

- next-token cross entropy;
- structured-field accuracy;
- output format validity;
- answer-token frequency;
- train/validation gap.

A task gain bought by severe local degradation is not a clean mechanism gain.

## 10. Primary Analysis

For each seed and checkpoint, calculate:

$$
\Delta Q^{\mathrm{syn}}
=
Q_{\mathrm{comp}}^{\mathrm{syn}}(\mathrm{MTP-info})
-
\max\left[
Q_{\mathrm{comp}}^{\mathrm{syn}}(\mathrm{NTP}),
Q_{\mathrm{comp}}^{\mathrm{syn}}(\mathrm{MTP-mask})
\right],
$$

$$
\Delta Q^{\mathrm{real}}
=
Q_{\mathrm{comp}}^{\mathrm{real}}(\mathrm{MTP-info})
-
\max\left[
Q_{\mathrm{comp}}^{\mathrm{real}}(\mathrm{NTP}),
Q_{\mathrm{comp}}^{\mathrm{real}}(\mathrm{MTP-mask})
\right].
$$

Then:

$$
T_{\mathrm{pair}}
=
\min(\Delta Q^{\mathrm{syn}},\Delta Q^{\mathrm{real}}).
$$

Use paired bootstrap over examples within each seed and a seed-level sign report.

## 11. Mechanism Ordering Check

The intended causal ordering is:

$$
\text{positive task-gradient alignment}
\rightarrow
\text{better }H_T\text{ evidence/intermediate state}
\rightarrow
\text{preservation to }H_A
\rightarrow
\text{higher }Q_{\mathrm{comp}}.
$$

Log checkpoints densely enough to test ordering.

Support requires representation improvement to precede or coincide with task improvement. If task improvement appears first, the claimed representation mechanism is not established.

## 12. Construct-Validity Gates

The experiment is interpretable only if:

1. symbolic synthetic solver accuracy is 100%;
2. synthetic local-only controls are below threshold;
3. real one-support performance is substantially below full-context performance;
4. support deletion reduces accuracy;
5. distractor replacement does not change gold answers;
6. evidence-swap labels are valid;
7. formatting succeeds;
8. no condition sees different test examples or context lengths.

## 13. Stop Conditions

Stop and repair the data/model pair if:

- real full-context performance is at chance;
- one-support controls solve the task;
- evidence-swap generation is unreliable;
- output formatting collapses;
- test leakage is detected.

Stop and reject the current MTP mechanism if:

- `MTP-mask` matches `MTP-info`;
- decision-state gains disappear before the answer state;
- synthetic gains do not transfer to real data with passed capability gates.

Do not respond to failure by adding sweeps.

## 14. Required Outputs

Create only after execution:

```text
summary.md
detailed.md
figures/
```

`summary.md` must start with:

1. $T_{\mathrm{pair}}$;
2. synthetic and real $\Delta Q$;
3. causal-patch result;
4. decision-to-answer preservation;
5. verdict and claim boundary.

`detailed.md` must contain:

- data filtering ledger;
- construct-validity gates;
- all seed results;
- checkpoint trajectories;
- gradient alignment;
- local-language guards;
- failure decomposition.

## 15. Post-Result Decision

### If supported

Open a separate capacity/conflict anchor. Do not immediately design a Router.

### If synthetic-only

Revise the workload mapping or serialization. Do not claim downstream relevance.

### If real-only without mechanism

Search for a rival mechanism.

### If no gain with passed capability gate

Weaken or reject informative MTP as a solution for this workload under the tested setup.

### If capability gate fails

Change the model scale or simplify the real task in a new approved protocol; do not interpret the current comparison.

### Router gate

A Router anchor is permitted only after a later audit establishes:

$$
\langle g_o,g_{o'}\rangle<0
$$

for stable operator-conditioned gradients and shows that different experts have conditional task advantage.

## 16. References

- Bai et al., *LongBench: A Bilingual, Multitask Benchmark for Long Context Understanding*, 2023.
- Ho et al., *Constructing A Multi-hop QA Dataset for Comprehensive Evaluation of Reasoning Steps* (2WikiMultiHopQA), 2020.
- Bai et al., *LongBench v2: Towards Deeper Understanding and Reasoning on Realistic Long-context Multitasks*, 2024.
