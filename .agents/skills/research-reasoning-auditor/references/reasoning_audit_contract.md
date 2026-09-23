# Research Reasoning Audit Contract

Use this contract to turn an initially mixed research story into an identifiable
scientific question. The objective is not to make the story sound coherent. The
objective is to make every important inference answerable.

## 1. Parse Before Interpreting

Read the user's raw statement sentence by sentence and classify each claim by
function:

- **Observation**: directly measured or externally established fact.
- **Unknown**: the unresolved scientific question.
- **Purpose**: which uncertainty the proposed work is intended to reduce.
- **Hypothesis**: one candidate answer to the unknown.
- **Mechanism**: the proposed causal or structural process connecting variables.
- **Prediction**: an observable consequence expected under a hypothesis.
- **Measurement**: a metric or proxy used to observe a construct.
- **Intervention**: the variable deliberately changed to identify an effect.
- **Conclusion**: the bounded update supported by observed evidence.
- **Decision**: what the researcher will do next because of that update.

Do not assume the user's labels are correct. A sentence titled "Purpose" may
actually be a hypothesis; a sentence titled "Hypothesis" may be a desired
outcome; a metric may be standing in for the construct it only imperfectly
measures.

## 2. Reconstruct The Direction Of Reasoning

Write the shortest valid chain:

~~~text
known observation
-> unresolved uncertainty
-> H1 versus strongest rival H2
-> prediction that differs between H1 and H2
-> measurement or intervention that can observe that difference
-> result
-> bounded update
~~~

Audit direction explicitly.

A common invalid reversal is:

~~~text
metric we plan to compute
-> result we hope to see
-> mechanism we then claim
-> research purpose retrofitted around that mechanism
~~~

The metric is downstream of the question. It cannot define the question merely
because it is convenient to compute.

## 3. Find The Real "Why"

For every explanatory statement, ask one level deeper:

- What exactly is being explained?
- Why should this mechanism produce the observation?
- Which intermediate variable carries the effect?
- What would look different if this mechanism were false?
- Which other mechanism could produce the same observation?

Stop when one of three states is reached:

1. a testable mechanistic link;
2. a clearly labeled assumption;
3. an unresolved unknown that should become the research question.

Do not hide state 2 or 3 with stronger prose.

## 4. Audit Causal Identification

For each proposed arrow A -> B, classify the support:

- **Direct intervention**: A is manipulated while relevant alternatives are
  controlled and B changes accordingly.
- **Temporal or structural evidence**: compatible with causality but not fully
  identifying it.
- **Association only**: A and B co-vary.
- **Narrative only**: no result directly bears on the arrow.

When support is not causal, replace causal wording with the strongest justified
relation: "associated with", "compatible with", "predicts", "co-occurs with",
or "remains a candidate explanation".

Explicitly check training history, architecture, data composition, optimization,
checkpoint choice, and measurement artifacts when any of them could explain
the same result.

## 5. Require A Strong Rival

A useful hypothesis is not just a story that fits the data. It must compete with
another explanation that also fits the current evidence.

Construct the strongest live rival, not a weak straw man. Prefer rivals that
differ at one decisive mechanism link.

Examples of useful rival forms:

- selective information organization **versus** global compression;
- semantic specialization **versus** load redistribution;
- model-internal use **versus** externally readable information;
- treatment effect **versus** training-history carryover;
- mechanistic improvement **versus** measurement or optimization artifact.

If no credible rival can be stated, the current hypothesis is probably too
vague to test.

## 6. Derive Separating Predictions

Before choosing a metric, write what each hypothesis predicts.

A prediction is useful only if the hypotheses disagree on it.

| Question | H1 predicts | Rival predicts | Observable separator |
| --- | --- | --- | --- |
| What changes? | specific direction | different direction or no change | named variable |
| Where? | specific samples/layers/groups | different localization | stratified readout |
| Under intervention? | response changes | response remains | controlled perturbation |
| Functional consequence? | target behavior changes | proxy changes only | task/intervention test |

If both hypotheses predict "metric increases", that metric is not a separator.

## 7. Audit Construct Validity

For every metric, write:

~~~text
metric -> directly measured quantity -> intended construct -> cannot prove
~~~

Examples:

- linear-probe accuracy -> information accessible to a linear readout ->
  representational accessibility -> does **not** prove the base model uses that
  information;
- Fisher ratio -> between-class separation relative to within-class spread ->
  one notion of class geometry -> does **not** by itself identify the mechanism
  producing that geometry;
- effective rank -> concentration of variance across directions ->
  global anisotropy or dimensional concentration -> does **not** tell which
  semantic information was retained;
- sparse-feature reuse -> overlap of activated SAE features across samples ->
  cross-sample reuse -> does **not** establish that reused features are
  beneficial, semantic, or task-selective.

Never let multiple proxies become convincing merely because they move in the
same narrative direction. Ask whether they are independent evidence for the
same construct or repeated views of the same underlying statistic.

## 8. Audit Experiment Value

Before execution, write three branches:

- **Supporting**: what result would increase belief in H1 relative to the rival?
- **Non-supporting**: what result would weaken H1 or favor the rival?
- **Insufficient**: what result would leave the comparison unresolved?

Then state the decision change for each branch.

If all three branches lead to the same next experiment or same conclusion, the
current experiment has low decision value and should usually be redesigned.

A minimal experiment is not the experiment with the fewest metrics. It is the
smallest experiment that can force a different scientific judgment.

## 9. Bound The Claim

After seeing a result, update only the tested link.

Use this ladder:

~~~text
observed metric change
< representational association
< discriminative accessibility
< model-internal use
< causal mechanism
< end-task consequence
~~~

Do not skip levels without direct evidence.

State:

- what is directly established;
- what interpretation is compatible;
- what rival remains;
- what cannot yet be claimed;
- what one next test would most reduce the remaining uncertainty.

## 10. Rewrite Purpose And Hypotheses Only After The Audit

A clean **Purpose** should name an uncertainty and, when useful, the rival
explanations that current evidence cannot distinguish.

A clean **Hypothesis** should specify the proposed mechanism and a prediction
that differs from the strongest rival.

Avoid embedding the desired conclusion in the purpose. Avoid using a metric name
as the scientific object unless the metric itself is genuinely the object of
study.

## 11. Default Audit Output

For substantial reasoning problems, return:

### Core question
One sentence naming the actual unknown.

### Reconstructed chain
The minimum observation-to-decision chain.

### Main logic breaks
Only the errors that materially change the experiment or claim.

### Hypothesis and strongest rival
State both at the same level of abstraction.

### Separating prediction
What must differ if one explanation is more plausible than the other.

### Minimal test
The smallest measurement or intervention that can separate them.

### Claim boundary
What the current or future result can and cannot establish.

Only after these are stable should the assistant provide polished meeting or
artifact wording.
