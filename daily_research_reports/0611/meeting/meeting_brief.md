# Meeting Brief: [Topic]

## Question

[Write the one question this meeting should answer.]

**Parent problem:**
[Why this matters to the mainline.]

**Current subproblem:**
[The exact uncertainty this result or discussion resolves.]

## Conclusion

> [Write the main conclusion in 1-2 sentences. State the result first; do not write a timeline.]

**Main update:**

1. [What changed in our belief.]
2. [Which previous explanation is supported, weakened, or refined.]
3. [What decision this points to next.]

## Key Evidence

[Expand the evidence enough that the conclusion is auditable without reading the full detailed record.]

1. **[Evidence title 1.]** [Metric / figure / condition.]  
   **Result:** [value or observation.]  
   **Interpretation:** [What this supports or weakens.]

2. **[Evidence title 2.]** [Metric / figure / condition.]  
   **Result:** [value or observation.]  
   **Interpretation:** [What this supports or weakens.]

3. **[Evidence title 3.]** [Metric / figure / condition.]  
   **Result:** [value or observation.]  
   **Interpretation:** [What this supports or weakens.]

## Detailed Setup

[State only the setup details needed to judge the evidence.]

**Data / task:**

- [Data source or synthetic task.]
- [Input construction.]
- [Target or objective.]
- [Which positions / tokens / examples are evaluated.]

**Model:**

- [Model family and size.]
- [Training stage: random init / pretrained / trained checkpoint.]
- [Important model dimensions.]

**Router / MoE:**

- [Router type.]
- [Top-k.]
- [Shared expert on/off.]
- [Load-balance loss.]
- [Other router choices that affect interpretation.]

**Run / audit:**

- [Seeds.]
- [Checkpoints.]
- [Audit sample size.]
- [Job id or run id if relevant.]

## Detailed Evidence

### 1. [Evidence Block 1]

[State the local question this block answers.]

| Metric | Result | Meaning |
|---|---:|---|
| [metric] | [value] | [what it answers] |
| [metric] | [value] | [what it answers] |

**Interpretation:**
[Separate observation from interpretation. State what this cannot prove.]

### 2. [Evidence Block 2]

[State the local question this block answers.]

| Metric | Result | Meaning |
|---|---:|---|
| [metric] | [value] | [what it answers] |
| [metric] | [value] | [what it answers] |

**Interpretation:**
[Separate observation from interpretation. State what this cannot prove.]

### 3. [Evidence Block 3]

[State the local question this block answers.]

| Metric | Result | Meaning |
|---|---:|---|
| [metric] | [value] | [what it answers] |
| [metric] | [value] | [what it answers] |

**Interpretation:**
[Separate observation from interpretation. State what this cannot prove.]

## Current Interpretation

**Observation:**
[What was directly measured.]

**Interpretation:**
[What the observation suggests.]

**Claim:**
[What is now safe to say.]

**Speculation:**
[What remains plausible but untested.]

## Boundary

**This conclusion covers:**

- [Data / task boundary.]
- [Model / router boundary.]
- [Training objective / checkpoint boundary.]
- [Metric boundary.]

**This conclusion does not cover:**

- [Stronger claim not tested.]
- [Setting not tested.]
- [Method or deployment claim not tested.]

## Next Step

**Next decision:**
[The smallest decision after this meeting.]

**Next iteration:**
[If continuing, write the minimal decisive experiment. If redirecting, state the replacement hypothesis.]

**Success criterion:**
[What result would support the next hypothesis.]

**Failure criterion:**
[What result would weaken it.]
