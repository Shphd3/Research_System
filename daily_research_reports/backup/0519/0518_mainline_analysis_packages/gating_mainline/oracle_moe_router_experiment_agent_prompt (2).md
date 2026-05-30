# Experiment Agent Prompt - Oracle MoE Router Analysis

## Goal

Run a controlled **Router mechanism analysis** before doing any Reverse Index experiment.

The immediate question is:

> In the new Oracle-MoE setting, what does the router actually use to divide tokens/representations among experts, and can any gating/inhibition design make different synthetic features go to different experts without destroying NTP loss?

Do **not** treat this as a Reverse Index experiment yet.

---

## Model Definition: Oracle MoE

Use the new Oracle-MoE form exactly:

```text
gate_input   = attention_output
expert_input = original hidden / residual representation entering the MoE block
```

Important sanity check:

```text
assert gate_input is attention_output
assert expert_input is NOT attention_output
assert gate_input and expert_input are logged separately
```

Architecture for this phase:

```text
1-layer Transformer + 1 MoE block
No Reverse Index
Full attention only
Synthetic dataset with known planted features
```

---

## Required Files / Inputs

Use the current experiment repository/codebase that contains the synthetic MoE experiments.

Required code components to locate or implement:

```text
synthetic dataset generator
1-layer Transformer + MoE model
router / gating module
expert module
training script
evaluation script
checkpoint loader
```

Search the repository for classes/functions containing:

```text
MoE
Router
Gating
Expert
Synthetic
Feature
ReverseIndex
```

Use prior context documents only as guidance, not as experiment data:

```text
0518_gating_mainline_package/gating_mainline/mainline_analysis.md
0518_gating_mainline_package/gating_mainline/experiment_cards.md
0518_gating_mainline_package/gating_mainline/reliability_checklist.md
router_specialization_and_retrieval_report_ZH.pdf
E2_theory_ai_prompt.md
E2_theory_ai_package.zip
```

If exact filenames differ in the repo, locate equivalent files by keyword search.

---

## Experimental Conditions

Train/evaluate at least the following router variants.

### C0. Standard Oracle Linear Router

```text
logits_e = W_router * gate_input
route = top-1(logits)
```

Purpose:

```text
Baseline: what does ordinary learned routing do when its input is attention_output?
```

---

### C1. Parameter-Center Router, Fixed Centers

Initialize experts differently. Compute one normalized center vector per expert from expert parameters.

Suggested center definition:

```text
For expert e, take the first expert input projection W_in,e.
c_e = normalize(mean over hidden-facing rows or leading PCA direction of W_in,e)
```

Then route by similarity:

```text
logits_e = tau * cosine(normalize(gate_input), c_e)
route = top-1(logits)
```

Centers are fixed after initialization.

Purpose:

```text
Test whether explicitly separated expert parameter centers create separated routing cells.
```

---

### C2. Trainable Center Router + Repulsion

Each expert has a trainable normalized center c_e.

```text
logits_e = tau * cosine(normalize(gate_input), normalize(c_e))
route = top-1(logits)
```

Add center repulsion:

```text
L_repulsion = mean_{e != e'} max(0, cosine(c_e, c_e') - margin)^2
```

Total loss:

```text
L = L_NTP + alpha * L_balance + rho * L_repulsion
```

Purpose:

```text
Test whether maintaining separated routing centers helps feature-to-expert specialization.
```

---

### C3. Inhibition / Margin Router

Implement the teacher-proposed inhibition idea as a diagnostic, not as the final method.

For each training sample, after routing selects expert e*, compute per-expert CE loss by forwarding all experts on the same expert_input.

Define:

```text
CE_selected = CE from routed / selected expert e*
CE_other_e  = CE from non-selected expert e
```

Add a margin term:

```text
L_inhibit = mean_{e != e*} max(0, margin - (CE_other_e - CE_selected))
```

Total:

```text
L = L_NTP + beta * L_inhibit + alpha * L_balance
```

Purpose:

```text
Test whether forcing the selected expert to outperform non-selected experts creates functional specialization.
```

---

### C4. Center Router + Inhibition

Combine C2 and C3:

```text
L = L_NTP + alpha * L_balance + rho * L_repulsion + beta * L_inhibit
```

Purpose:

```text
Test whether geometric separation plus functional exclusivity is stronger than either alone.
```

---

## Required Metrics

Report all metrics for each condition.

### 1. NTP / Task Performance

```text
train loss
validation NTP loss
target-token accuracy / readback accuracy
```

Meaning:

```text
Does the routing method still solve the language modeling task?
```

Expected interpretation:

```text
Good routing purity but bad NTP loss means the artificial partition hurts learning.
Good NTP loss but bad routing purity means the task does not require feature-aligned routing.
```

---

### 2. Expert Load

```text
P(expert)
load entropy
load Gini
dead expert count
```

Meaning:

```text
Does routing collapse into one/few experts?
```

---

### 3. Feature-to-Expert Assignment

Use direct contingency, not linear probe.

```text
P(expert | feature)
P(feature | expert)
NMI(feature, expert)
purity
ARI if applicable
```

Meaning:

```text
Are planted synthetic features actually assigned to different experts?
```

Important:

```text
This is not evidence that experts learned the feature. It only measures routing assignment.
```

---

### 4. Router Confidence

```text
router entropy
top1-top2 margin
mean max probability
```

Meaning:

```text
Is the router making confident partitions or arbitrary weak choices?
```

---

### 5. Center Geometry

For center-based routers:

```text
center cosine matrix
mean pairwise center cosine
min pairwise center angle
```

Meaning:

```text
Are expert centers actually separated?
```

Expected interpretation:

```text
Separated centers but poor feature routing means center separation alone does not define semantic/feature partitions.
```

---

### 6. Assigned Representation Geometry

For each expert cell, compute on gate_input:

```text
within-expert cosine similarity
between-expert cosine similarity
silhouette score
cell centroid distances
```

Meaning:

```text
Do routed examples form coherent regions in attention-output space?
```

---

### 7. Expert Utility Matrix

For each feature f and expert e, force all feature-f examples through expert e.

Compute:

```text
U[f,e] = mean target probability
CE[f,e] = mean cross-entropy
```

Plot heatmaps.

Meaning:

```text
Does each feature have a unique best expert, or can many experts solve it equally?
```

Interpretation:

```text
Diagonal utility + non-diagonal routing = router training failure.
Non-diagonal utility + good NTP = expert redundancy / no functional specialization.
Diagonal routing + non-diagonal utility = routing purity without expert specialization.
```

---

### 8. Inhibition Diagnostics

For C3/C4:

```text
mean CE_other - CE_selected
inhibition margin violation rate
selected expert win rate
```

Meaning:

```text
Does the inhibition loss actually make selected experts functionally better than non-selected experts?
```

---

### 9. Counterfactual Route Flip

Construct matched samples:

```text
same feature, different surface tokens
same surface tokens, different feature if possible
same target, different feature
same feature, different context filler
```

Measure:

```text
route change rate
logit margin change
```

Meaning:

```text
What minimal input change flips the route?
```

Interpretation:

```text
If route flips with token identity but not feature, router follows token shortcut.
If route flips with feature while tokens are controlled, router uses feature-like information.
```

---

## Required Outputs

Create a result folder:

```text
results/oracle_moe_router_analysis_<date>/
```

Include:

```text
config.yaml
training_logs.jsonl
metrics_summary.csv
feature_expert_contingency.csv
expert_load.csv
center_cosine_matrix.csv
utility_matrix_ce.csv
utility_matrix_target_prob.csv
inhibition_diagnostics.csv
counterfactual_flip_results.csv
fig_feature_expert_heatmap.png
fig_utility_matrix.png
fig_center_cosine.png
fig_load_bar.png
analysis.md
```

---

## Required `analysis.md` Structure

```markdown
# Oracle MoE Router Analysis

## 1. Question
What does the router use to divide representations among experts?

## 2. Model Sanity
- gate_input source:
- expert_input source:
- verified by hook: yes/no

## 3. Conditions Compared
- C0 standard oracle linear router
- C1 fixed parameter-center router
- C2 trainable center router + repulsion
- C3 inhibition router
- C4 center + inhibition

## 4. Key Results
Table:
condition | val NTP loss | readback acc | NMI(feature, expert) | load entropy | utility diagonality | inhibition win rate

## 5. Interpretation
Choose one or more:
- routing collapse
- feature-aligned routing but no expert functional specialization
- expert redundancy
- artificial routing hurts NTP
- center separation not aligned with planted feature
- inhibition works only as exclusivity regularizer
- ordinary NTP does not require feature-aligned routing

## 6. Claim Boundary
What this proves:
What this does not prove:

## 7. Next Step
Whether to proceed to 2-layer Reverse Index experiments.
```

---

## Decision Rules

### Case A

```text
High NMI(feature, expert)
Low NTP loss
Diagonal utility matrix
```

Conclusion:

```text
Router method can create feature-aligned functional specialization in synthetic setting.
Proceed to Reverse Index stage.
```

### Case B

```text
High NMI(feature, expert)
Low NTP loss
Non-diagonal utility matrix
```

Conclusion:

```text
Routing assignment looks clean, but experts are functionally redundant.
Do not claim expert specialization.
```

### Case C

```text
Low NMI(feature, expert)
Low NTP loss
Non-diagonal utility matrix
```

Conclusion:

```text
NTP is solved without feature-aligned routing.
Ordinary objective does not require specialization.
```

### Case D

```text
High NMI(feature, expert)
High / worse NTP loss
```

Conclusion:

```text
Forcing feature-aligned routing harms the task or implementation is unstable.
Need debug before Reverse Index.
```

### Case E

```text
Separated centers
Low NMI(feature, expert)
```

Conclusion:

```text
Separating expert centers is not sufficient; centers are not aligned with planted features.
```

---

## Hard Rules

- Do not run Reverse Index in this phase.
- Do not report only NMI or routing purity.
- Do not claim expert specialization without utility / ablation evidence.
- Do not use feature-id linear probe as main evidence.
- Always separate routing assignment from expert functional contribution.
- All experiments must use Oracle-MoE gate/expert input separation.
