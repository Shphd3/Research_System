# E002 Minimal Next Experiment — Correlation-Aware Feature-Zipf Routing

Audience: research agent after cloning `Shphd3/Research_System`.

## One-Sentence Mission

Run one decisive synthetic experiment to test whether explicit feature-correlation routing helps MoE recover correlated Feature-Zipf mechanisms better than the current strongest routing baselines.

## Background Anchor

Current mainline:

> Build a Hierarchical MoE route-and-expert structure that exploits low-dimensional, Zipfian, compositional feature structure rather than treating all tokens or mechanisms as flat.

Current evidence boundary:

- Feature-Zipf synthetic data is a useful controlled diagnostic.
- Hierarchical MoE shows a weak function-level recovery signal.
- Current evidence does **not** support the claim that Hierarchical MoE is better than Flat middle spectral MoE at sparse feature division.
- Flat middle spectral routing currently gives the strongest sparse atom division signal.
- 0508 meeting update: features should not be treated as independent; the next question is whether semantic/feature correlation should guide routing.

## Decision Question

When hidden representations are generated from Zipfian sparse features that are **correlated** rather than independent, does an explicit feature-correlation router recover the true coarse/fine mechanism better than:

1. Flat middle spectral routing;
2. existing Hierarchical conditional_input routing;
3. a matched feature-only hierarchical router without correlation input?

## Core Hypothesis

**H2: Correlation-aware routing hypothesis**

If sparse features have common → group → unique correlation structure, then a token-wise linear gate or spectral gate may capture some frequency/separability signal but may fail to preserve the feature-relation structure. A router that explicitly uses feature-feature correlation should improve tail-feature routing and function-level recovery.

This is a hypothesis, not an established claim.

## Do Not Do

Do **not** run a broad model sweep.

Do **not** add real-data experiments yet.

Do **not** tune many hyperparameters.

Do **not** claim continual-learning benefit.

Do **not** claim "semantic correlation" unless it is operationalized as a measurable feature relation.

The only goal is to answer the decision question above.

---

# Minimal Experiment Design

## Dataset: Correlated Feature-Zipf Synthetic

Start from the existing Feature-Zipf synthetic setup.

Keep the same basic dimensions unless the existing code forces a different default:

```text
hidden_dim d = 1024
common features = 16
coarse groups = 10
group features per coarse = 6
unique features per coarse = 10
train = 20000
valid = 5000
test = 5000
seeds = [0] for pipeline check, then [0,1,2] for final result
```

Sample types:

```text
common-only: 0.40
group-only: 0.35
group+unique: 0.25
```

Feature frequency:

```text
common / group / unique feature occurrence follows Zipf-like frequency.
```

Add one new variable:

```text
rho = feature-correlation strength
```

Use only one value for the main experiment:

```text
rho = 0.8
```

Interpretation:

- With probability `rho`, group and unique features are sampled from the same coarse semantic block.
- With probability `1-rho`, sample a mismatched group/unique feature as relation noise.
- This creates correlated sparse features without making the task fully oracle-easy.

## Output Function

Use the existing variable-A setting:

```text
y = (A_common + 1[c] A_c + 1[f] A_{c,f}^{tail}) h + eta
```

This is the main setting because different feature groups require different computations.

## Built-in Negative Control

Use a **shuffled relation matrix** control for the new router.

Do not make this a second big experiment. It is a built-in causal check:

```text
C_correct: relation matrix estimated from true training feature activations.
C_shuffled: same matrix with feature indices permuted.
```

If `C_correct` and `C_shuffled` perform similarly, the router is not using the correct relation structure.

Optional only if the main result is positive:

```text
shared-A control: y = A_common h + eta
```

This checks whether the router only clusters correlated inputs without recovering functional specialization.

---

# Models to Compare

Run exactly these four arms.

## M1: Flat middle spectral + common

Purpose: strongest current feature-division baseline.

Do not remove this baseline.

## M2: Hierarchical conditional_input

Purpose: current hierarchical baseline.

## M3: Hierarchical feature-only z-gate

Purpose: matched baseline for the new router.

Router input:

```text
z
```

where `z` is the true latent sparse feature activation vector in the synthetic data.

This is a diagnostic baseline, not a deployable method.

## M4: Hierarchical correlation-aware z-gate

Purpose: test explicit relation-aware routing.

Estimate feature relation matrix `C` from training feature activations.

Use positive PMI or normalized co-activation:

```text
C_ab = max(PMI(z_a, z_b), 0)
```

Remove diagonal and row-normalize.

Keep only top-k neighbors per feature to avoid popularity dominance:

```text
top_k_edges = 16
```

Compute relation summary:

```text
r = C z
```

Router input:

```text
[z ; r ; z * r]
```

where `*` is elementwise product.

Use the same expert count / path count as the existing Hierarchical conditional_input model:

```text
10 coarse × 10 fine paths
```

Important:

- Primary comparison is **M4 vs M3**.
- Secondary comparison is **M4 vs M1/M2**.
- If M4 only beats M2 but not M3, correlation is not proven to matter.
- If M4 beats M3 but loses to M1, the result supports relation bias but not yet the full architecture.

---

# Metrics

Report only the following metrics.

## Primary Metrics

### 1. Tail Leaf NMI

Measure route/path alignment with true fine mechanism on group+unique samples, especially low-frequency unique features.

```text
tail_leaf_NMI ↑
```

### 2. Function Cosine

Compare learned expert/path function with the true generating function.

```text
function_cos ↑
```

### 3. Atom Diversity / Top Atom Overlap

Use the same sparse atom profile metrics as E001.

```text
atom_diversity ↑
top_atom_overlap ↓
```

### 4. Group+Unique Ablation Delta

Remove group+unique features and keep routes fixed.

```text
ablation_loss_delta ↑ in variable-A
```

This shows whether model output actually depends on group/unique features.

## Control Metric

### Correct-C vs Shuffled-C Gap

For M4:

```text
gap = score(C_correct) - score(C_shuffled)
```

Use this for tail_leaf_NMI and function_cos.

If gap is near zero, do not claim relation-aware routing.

---

# Decision Rule

Declare **H2 weakly supported** only if all conditions hold:

1. M4 beats M3 on `tail_leaf_NMI` in at least 2/3 seeds.
2. M4 beats M3 on `function_cos` in at least 2/3 seeds.
3. Mean `tail_leaf_NMI` improvement is at least `+0.03`.
4. Mean `function_cos` improvement is at least `+0.02`.
5. M4 does not worsen test loss by more than 2% relative to M3.
6. `C_correct` beats `C_shuffled`; otherwise the relation input is not validated.

If only feature metrics improve:

> Claim only feature-level routing improvement, not mechanism recovery.

If only function_cos improves:

> Claim weak function-level signal, but inspect route/path alignment before architecture claims.

If M4 does not beat M3:

> Do not continue architecture variants. The current relation-aware design is not the right next step.

If M1 Flat middle spectral still wins on atom diversity:

> Keep current claim boundary: middle spectral remains the strongest sparse feature division baseline.

---

# Required Output

Create one result file:

```text
results/R002_correlation_aware_feature_zipf.md
```

Include:

```markdown
# R002 Correlation-Aware Feature-Zipf Routing

## Decision Question
## Setup
## Models
## Metrics
## Main Result Table
## Correct-C vs Shuffled-C Control
## Interpretation
## Claim Audit
## What Cannot Be Claimed
## Weakest Point
## Next Minimal Action
```

Also save figures if available:

```text
results/R002_fig_relation_matrix.png
results/R002_fig_route_confusion.png
results/R002_fig_path_atom_profile.png
```

Do not produce more than three figures.

---

# Claim Boundary

Can claim only if supported:

> In correlated Feature-Zipf synthetic data, explicit feature-correlation routing improves recovery of tail feature routing and/or function-level mechanism over a matched feature-only hierarchical router.

Cannot claim:

- real language semantic routing is solved;
- attention provides the true semantic measurement;
- correlation-aware routing improves continual learning;
- Hierarchical MoE is generally better than Flat MoE;
- feature-level routing improvement proves mechanism recovery.

---

# 30s Report Template

The next experiment asks whether the missing ingredient in MoE routing is feature correlation. In the previous Feature-Zipf experiment, Hierarchical MoE showed weak function recovery but did not beat Flat middle spectral routing at sparse feature division. Now we add correlated sparse features and compare a matched feature-only router against a correlation-aware router using the same hierarchy. If the correlation-aware router improves tail Leaf NMI and Function Cos, and the improvement disappears with a shuffled relation matrix, then we have evidence that explicit feature-relation bias helps routing. If not, we should not pursue correlation-aware architecture yet.
