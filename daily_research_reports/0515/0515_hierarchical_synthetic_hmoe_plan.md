# Next Iteration Plan - 0515

## Decision Question
Can a model trained on a synthetic next-token prediction dataset recover a two-level language-like hierarchy, and does H-MoE expose that hierarchy more cleanly than flat-MoE?

## Mainline Anchor
The experiment must first prove the data has controlled hierarchical compositional structure, then prove dense NTP can read it back, and only then compare flat-MoE vs H-MoE routing.

## Hypothesis
H1: In a token stream where low-level phrase units are reused inside high-level event units, H-MoE will route high-level event structure at the root router and low-level phrase/role structure at leaf experts.

Competing hypothesis H0: H-MoE and flat-MoE only memorize frequent n-grams; routing will not align with the planted hierarchy beyond frequency effects.

## 1. Data Construction

### 1.1 Vocabulary

Use integer tokens.

```text
V = {0, 1, ..., 127}
```

Reserve tokens:

```text
Entity phrase tokens: 1-16
Action phrase tokens: 17-24
Object phrase tokens: 25-32
Background tokens: remaining tokens
```

### 1.2 Level 1: phrase / role units

Each low-level unit is a 2-token phrase.

```text
Entities:
E1=[1,2], E2=[3,4], E3=[5,6], E4=[7,8]

Actions:
A1=[17,18], A2=[19,20], A3=[21,22], A4=[23,24]

Objects:
O1=[25,26], O2=[27,28], O3=[29,30], O4=[31,32]
```

L1 labels:

```text
L1_phrase_id: E1...E4, A1...A4, O1...O4
L1_role: entity / action / object
```

### 1.3 Level 2: event / relation units

Each high-level event is an ordered composition:

```text
S = Entity + Action + Object
```

Define four event families:

```text
F1 sports-like:   {E1,E2} + A1 + {O1,O2}
F2 research-like: {E1,E3} + A2 + {O3,O4}
F3 social-like:   {E2,E4} + A3 + {O1,O3}
F4 work-like:     {E3,E4} + A4 + {O2,O4}
```

Example events:

```text
S1 = E1 + A1 + O1 = [1,2,17,18,25,26]
S2 = E2 + A1 + O2 = [3,4,17,18,27,28]
S3 = E1 + A2 + O3 = [1,2,19,20,29,30]
```

L2 labels:

```text
L2_family_id: F1...F4
L2_event_id: exact triple, e.g. E1-A1-O1
position_in_event: entity/action/object token position
```

This is hierarchical because the same L1 phrase is reused across different L2 events, and the L2 family constrains which entities, actions, and objects can co-occur.

### 1.4 Frequency design

Use Zipf-like frequency at both levels.

```text
Family frequency:
F1: 5000
F2: 2000
F3: 800
F4: 300

Standalone L1 phrase frequency:
E1: 8000, E2: 4000, E3: 2000, E4: 1000
A1: 7000, A2: 3000, A3: 1200, A4: 500
O1: 6000, O2: 3000, O3: 1500, O4: 700
```

Within each family, sample exact triples with a second Zipf distribution.

### 1.5 Sequence generation

Generate a continuous token stream of length $N=1{,}000{,}000$.

```text
1. Sample chunks until sequence length reaches N.
2. With probability p_event=0.35, append one L2 event chunk.
3. With probability p_l1=0.20, append one standalone L1 phrase.
4. Otherwise append 1-6 random background tokens.
5. Record token labels for every position.
```

Do not add explicit separators in the main experiment. Use a separator-only ablation later if debugging is needed.

### 1.6 Data audit before training

Required plots / tables:

```text
1. L1 phrase frequency rank curve.
2. L2 family and event frequency rank curve.
3. Accidental collision rate for L1 and L2 n-grams in background.
4. Conditional entropy:
   H(next | L1 prefix)
   H(next | L2 prefix)
5. Prefix target table:
   [E1 first token] -> E1 second token
   [E1 + A1] -> O1/O2 family-consistent object tokens
```

If these fail, do not train MoE.

## 2. Task

All models train on next-token prediction.

Training input:

```text
x_1, x_2, ..., x_t
```

Target:

```text
x_{t+1}
```

Evaluation is not only global loss. Evaluate by planted structure:

```text
L1 readback: predict phrase continuation.
L2 readback: predict event-consistent continuation.
Counterfactual: compare correct object vs wrong object under same prefix.
Background: confidence should remain low on random background.
```

## 3. Models

### 3.1 Dense control

```text
1-layer Transformer
self-attention + dense FFN
same embedding, attention, context length as MoE models
```

Purpose: prove the data is learnable before interpreting routing.

### 3.2 Flat-MoE baseline

```text
1-layer Transformer
self-attention + flat MoE FFN
num_experts = 8
top-k = 1 or 2
load-balance loss enabled
```

Flat router output:

```text
expert_id in {1,...,8}
```

Purpose: test whether non-hierarchical experts specialize to planted features.

### 3.3 H-MoE model

```text
1-layer Transformer
self-attention + hierarchical MoE FFN
root groups = 4
leaf experts per group = 2
total leaf experts = 8
```

Routing:

```text
root_router: token hidden state -> group_id in {1,...,4}
leaf_router: token hidden state + group_id -> leaf_expert_id in {1,2}
```

Capacity must match flat-MoE:

```text
same active expert width
same total leaf expert count
same active experts per token
same training budget
```

## 4. Training Protocol

Run all models on the same datasets and seeds.

```text
Dataset sizes:
- smoke: 200k tokens
- main: 1M tokens
- stress: 5M tokens

Seeds:
- 5 random seeds per model

Context length:
- 64 tokens

Optimizer:
- AdamW

Primary comparison:
- dense vs flat-MoE vs H-MoE
```

Stop condition:

```text
same number of seen training tokens, not only same epochs.
```

## 5. Metrics

### 5.1 Prediction metrics

```text
Overall validation loss
L1 readback accuracy
L2 readback accuracy
L1 probability margin
L2 probability margin
Background confidence
```

Probability margin:

$$
\Delta = \log p(y_{correct} \mid prefix) - \max_{y_{wrong}} \log p(y_{wrong} \mid prefix)
$$

### 5.2 Routing alignment metrics

For flat-MoE:

```text
NMI(flat_expert_id, L1_phrase_id)
NMI(flat_expert_id, L2_family_id)
Purity(flat_expert_id, L1_phrase_id)
Purity(flat_expert_id, L2_family_id)
```

For H-MoE:

```text
NMI(root_group_id, L2_family_id)
NMI(root_group_id, L1_phrase_id)
NMI(leaf_expert_id, L1_phrase_id)
NMI(leaf_expert_id, L2_family_id)
```

Expected H-MoE signature:

```text
root router aligns more with L2 family than L1 phrase;
leaf experts align more with L1 phrase than root router;
flat-MoE has weaker or less interpretable separation.
```

### 5.3 Hierarchical consistency metrics

```text
Root event consistency:
within one L2 event, entity/action/object tokens route to the same root group.

Leaf role separation:
within that root group, entity/action/object phrases use distinct or stable leaf experts.

Expert-feature matrix:
rows = experts or groups
cols = L1 phrase / L2 family
value = routing probability or token count
```

Required figures:

```text
Figure 1: L1 and L2 frequency rank curves.
Figure 2: Dense / flat-MoE / H-MoE L1-L2 readback accuracy.
Figure 3: flat expert x L1/L2 label matrix.
Figure 4: H-MoE root x L2 matrix and leaf x L1 matrix.
Figure 5: routing alignment over training steps.
```

## 6. Success Criteria

H-MoE supports the hierarchy hypothesis only if all are true:

```text
1. Data audit confirms controlled L1/L2 hierarchy.
2. Dense model achieves strong L1 and L2 readback.
3. H-MoE root router has higher alignment with L2 family than flat-MoE expert id does.
4. H-MoE leaf experts align with L1 phrases or roles.
5. Expert-feature matrices show block structure.
6. Overall loss improvement alone is not used as evidence of hierarchy.
```

## 7. Failure Interpretation

```text
Dense fails:
Data construction or training setup is wrong. Do not interpret MoE.

Dense succeeds, MoE routing does not align:
The task is learnable, but routing is not recovering planted hierarchy.

Flat-MoE aligns as well as H-MoE:
Hierarchy may not require hierarchical routing in this setup.

H-MoE aligns but prediction is not better:
H-MoE may be interpretable but not more useful for NTP.

H-MoE improves loss but no routing alignment:
Cannot claim it learned hierarchy; only claim it optimized prediction better.
```

## 8. Minimal Next Action

Implement the generator and run only data audit first.

Deliverables before model training:

```text
1. generated token sequence
2. label arrays: L1_phrase_id, L1_role, L2_family_id, L2_event_id
3. frequency plots
4. collision table
5. conditional entropy table
```

Only after E0 data audit passes, run dense control, then flat-MoE and H-MoE.

## 9. Claim Boundary

Can claim after success:

```text
On controlled synthetic hierarchical sequence data, H-MoE routing aligns with planted high-level and low-level feature labels more cleanly than flat-MoE.
```

Cannot claim:

```text
H-MoE learns natural language syntax.
H-MoE discovers hierarchy in real language.
H-MoE routing is equivalent to semantic understanding.
Synthetic hierarchy proves real-language behavior.
```
