# 0513 Cognitive Correction - What The Initial Experiment Should Mean

## One-Sentence Correction
The initial experiment is not “extract accurate token representations, mix them with random representations, and train an FFN classifier”; it is “construct a toy language stream with planted sequential patterns, train next-token prediction, and test whether the model recovers those patterns from context.”

## Correct Mental Model

### Data
A corpus is a sequence of token IDs.  
Most positions are random background.  
A small set of token combinations are planted with controlled frequencies.

Example:
```text
Vocabulary: 100 tokens
Feature 1: A B appears 10000 times
Feature 2: C D E appears 5000 times
Feature 3: F G appears 500 times
Feature 4: H I appears 100 times
Rest: random tokens
```

### Feature
A feature is not a single token.  
A feature is a recurring combination/context relation:
```text
A -> B
C D -> E
```

### Task
The task is next-token prediction:
```text
input prefix: A
target: B
```

### Model
First use a dense model without MoE.  
Only after readback succeeds, replace FFN with MoE and test expert specialization.

### What FFN/MoE Is Supposed To Reveal
The FFN/MoE is not given the true feature labels.  
It must learn from next-token loss.  
The diagnostic is whether internal activations or experts align with the planted feature IDs.

## Minimal Correct Pipeline
```text
generate controlled sequence
-> audit feature statistics
-> train dense next-token model
-> read back predictions and representations
-> train 4-expert MoE
-> measure feature-expert alignment
-> compare synthetic statistics with real data
```

## Common Failure
If loss decreases but the model does not output the planted next token after the planted prefix, then the experiment has not shown feature learning.
