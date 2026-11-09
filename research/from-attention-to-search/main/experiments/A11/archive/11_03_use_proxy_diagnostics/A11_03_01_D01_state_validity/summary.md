# Summary: A11_13 Downstream Semantic-State Validity

Primary anchor: [11_13_downstream_semantic_state_validity_anchor.md](../../../problem_anchors/11_informative_future_branch_mechanism/11_13_downstream_semantic_state_validity_anchor.md)
Protocol: [protocol.md](protocol.md)
Detailed record: [detailed.md](detailed.md)

## Result Snapshot

**Verdict:** supported as a controlled natural-language task and metric audit.

**What was established:** the paired persistent-assistant task validly isolates a distant behaviorally relevant state under its declared construction. Across five seeds and 3,200 examples, the local request and the early cue are each individually insufficient to reveal the answer index, paraphrases preserve the answer, counterfactual state changes flip it, and every cue lies beyond the declared local window.

**Primary result:** $Q_{task}=1.0$ in 5/5 seeds. Local-only and cue-only empirical Bayes accuracy are both exactly `0.50`, with empirical mutual information `0` bits. All 1,600 counterfactual groups and 800 paraphrase groups pass exact identity/intervention guards. The strongest tested surface shortcut, direct TF-IDF similarity between the cue and each candidate action, reaches only `0.5375`, below the `0.60` ceiling.

**What we do next:** the task is now eligible for one matched-budget NTP versus K=2 MTP small-language-model experiment. This result does not itself compare the methods.

## Grounded Task Definition

The target downstream behavior is a persistent assistant using an earlier user goal, state, value, preference, or availability constraint to choose a later action after unrelated intervening conversation.

An example is:

$$
X=(C_Z,D,L),
\qquad
Y=f(Z,L),
$$

where $C_Z$ expresses the early state, $D$ is unrelated dialogue, and $L$ is the later request with two candidate actions. Long-horizon semantics is operationalized by three requirements:

$$
f(C_Z,D,L)=f(C'_Z,D,L)
$$

for meaning-preserving paraphrases,

$$
f(C_Z,D,L)\ne f(C_{Z'},D,L)
$$

for a matched state counterfactual, and

$$
I(Y;L)=0
$$

under the balanced construction.

This definition is narrower than general natural-language semantics. It measures whether a distant meaning changes a later valid action without being recoverable from the local request alone.

## Setup

Five assistant domains are used:

| Relation family | Two states | Later action decision |
|---|---|---|
| goal | minimize cost / minimize time | cheaper / faster plan |
| current state | low energy / high energy | restorative / active plan |
| value | protect privacy / enable sharing | private / shareable workflow |
| preference | quiet focus / social collaboration | quiet / collaborative setting |
| availability | mornings free / evenings free | morning / evening slot |

Each state has four cue paraphrases. Each domain has four later requests, both option orders, and two intervening-history lengths. Seeds are `971-975`, with 640 examples per seed.

## Primary Metric

$$
Q_{task}=\min\{A_{oracle},C_{para},S_{cf},B_{local},B_{cue},H_d\}.
$$

| Component | What it tests | Result |
|---|---|---:|
| $A_{oracle}$ | complete context and labels are deterministically consistent | `1.0` |
| $C_{para}$ | wording changes preserve the decision | `1.0` |
| $S_{cf}$ | state changes alter the decision | `1.0` |
| $B_{local}$ | local request does not reveal answer index | `1.0` |
| $B_{cue}$ | cue alone does not reveal randomized answer position | `1.0` |
| $H_d$ | cue lies outside the 256-word audit window | `1.0` |
| $Q_{task}$ | weakest construct-validity component | `1.0` |

The minimum measured cue-to-answer distance is `294` whitespace-delimited tokens.

## Shortcut Audit

All baselines are evaluated on paraphrase families excluded from the training split.

| Baseline | Input | Accuracy |
|---|---|---:|
| majority | no text | `0.5000` |
| local-only word/bigram | current request and actions | `0.5000` |
| cue-only word/bigram | early cue | `0.5000` |
| full-text word/bigram | complete sequence | `0.5000` |
| cue-option TF-IDF similarity | cue matched separately to each action | `0.5375` |

The similarity baseline is the strongest tested lexical rival. Its failure to exceed `0.60` protects the next experiment from a simple "choose the option sharing more words with the cue" explanation. It does not rule out every possible nonsemantic heuristic.

## Key Figure

![A11_13 construct validity](figures/a11_13_construct_validity.png)

**What the figure tests:** whether every component of the task-validity gate passes, whether either half reveals the answer, whether simple surface methods solve the task, and whether the declared horizon is satisfied.

**How to read:** the upper-left panel shows the six normalized validity components; upper-right shows held-out-paraphrase shortcut accuracy against chance and the `0.60` ceiling; lower-left shows exact local/cue Bayes accuracy; lower-right shows minimum distance and $Q_{task}$ by seed.

**Observed result:** all construct components equal `1.0`; local and cue Bayes accuracy stay exactly at chance; the strongest lexical method is `0.5375`; minimum distance is `294` in every seed.

**Allowed conclusion:** this fixed task is a valid controlled proxy for distant semantic-state use and can support a method comparison.

**Not allowed:** MTP is already better, the task is fully natural, or performance transfers to open-ended assistant benchmarks.

## Claim Boundary

**Can claim:** the task's answer is causally determined by a distant state and local option mapping; it is invariant to the provided paraphrases, sensitive to the provided counterfactuals, locally insufficient, balanced, reproducible, and not solved by the tested lexical shortcuts.

**Cannot claim:** pretrained LLMs use the intended mechanism; MTP learns faster than NTP; the task measures all long-horizon semantics; open-ended response quality is captured; external benchmark transfer follows.

## Next Decision

Create A11_14 with one primary metric shared by both methods:

$$
Q_{downstream}(t)=\min\{A_{H1}(t),C_{para}^{model}(t),S_{cf}^{model}(t)\},
$$

where $A_{H1}$ is standard next-token answer accuracy after the same answer prefix for NTP and MTP. Compare time-to-threshold and area under the learning curve under matched examples, text tokens, backbone updates, architecture, optimizer, and evaluation schedule. MTP's H2 head remains a secondary mechanism metric, not the downstream score.

