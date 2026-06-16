# Protocol: A06_16_E01_2x2_geometry_oracle_gate

Primary anchor: `A06_16_2x2_expert_geometry_gate`  
Anchor decision question: Does a simple expert-aware 2D oracle gate exist, and can it be implemented as a linear router initialized from expert geometry?  
Experiment role: Minimal decisive static test for the 2x2 expert-geometry gate.

## 1. Decision Question

```text
Can two initialized 2x2 experts induce a routing rule that simultaneously gives balanced load and metric-defined specialization under uniform 2D input?
```

This protocol does not test training stability, real text, transformer hidden states, high-dimensional routing, common removal, or causal expert utility.

## 2. Tested Hypothesis

H1. Expert prototypes computed from initialized expert directions can define a compatibility score.

```math
q_e(x)=x^\top m_e
```

H2. The prototype gate

```math
g(x)=\arg\max_e q_e(x)
```

partitions uniform 2D input into two equal-measure regions.

H3. The same rule is implementable as a linear Switch-style router by setting

```math
w_e=m_e.
```

## 3. Rival Explanations

R1. Load balance can be achieved by arbitrary random splitting, without specialization.

```text
Protection:
compare against a random 50/50 router and require positive compatibility margin.
```

R2. The expert geometry metric may be degenerate.

```text
Protection:
test m_1≈m_2, undefined prototypes, and full-span distance.
```

R3. The observed balance may come only from a hand-picked easy example.

```text
Protection:
use many random expert-vector seeds and report seed-level metrics.
```

R4. The oracle may not correspond to an actual router initialization.

```text
Protection:
explicitly implement linear-router rows w_e=m_e and measure oracle agreement.
```

## 4. Data / Model / Algorithm / Objective

Data:

```text
Input x is sampled uniformly from S^1.
Optional visualization may also sample a grid over the unit disk.
```

Experts:

```text
Each seed samples four unit vectors a_1,a_2,a_3,a_4 in R^2.
Expert 1: A_1=[a_1,a_2].
Expert 2: A_2=[a_3,a_4].
```

Expert prototype:

```math
m_1=\frac{a_1+a_2}{\|a_1+a_2\|}, \qquad
m_2=\frac{a_3+a_4}{\|a_3+a_4\|}
```

Oracle router:

```math
g_{\mathrm{oracle}}(x)=\arg\max_e x^\top m_e
```

Linear-router implementation:

```math
w_1=m_1,\qquad w_2=m_2
```

```math
g_{\mathrm{router}}(x)=\arg\max_e w_e^\top x
```

Objective:

```text
Verify that the expert-induced oracle gate gives balanced load, positive compatibility margin, and exact agreement with the corresponding linear router initialization.
```

## 5. Conditions, Seeds, And Checkpoints

Conditions:

| Condition | Purpose |
| --- | --- |
| C1_prototype_oracle | Main condition: route by expert prototype compatibility. |
| C2_linear_router_equivalence | Implement the same rule as router rows w_e=m_e. |
| C3_random_50_50_router | Shows load balance alone is not specialization. |
| C4_near_identical_prototypes | Predicted low-margin degenerate case. |
| C5_undefined_prototype | Predicted invalid case where a_i+a_j≈0. |
| C6_full_span_distance | Shows distance to full span is degenerate in 2D. |

Seeds:

```text
expert_geometry_seeds: 100
input_samples_per_seed: 10000
boundary_tolerance: 1e-6 for exact agreement checks
near_boundary_exclusion: |x^T(m_1-m_2)| < 1e-4
```

Checkpoints:

```text
No training checkpoints.
This is a static geometry and router-initialization test.
```

## 6. Primary Metric

Primary metric:

```text
joint_partition_validity
```

A non-degenerate seed passes if:

```text
load_error = |load_1 - 0.5| <= 0.02
mean_margin > 0
router_oracle_agreement >= 0.999 after excluding boundary-tie points
```

Why this decides the judgment:

```text
The anchor requires both uniformity and specialization. Load error tests uniformity; mean margin tests metric-defined specialization; router-oracle agreement tests whether the oracle can be realized as a Switch-style linear initialization.
```

False-positive cost:

```text
Accepting random 50/50 routing as specialization.
```

False-negative cost:

```text
Rejecting a valid geometric gate because of finite-sample noise or boundary ties.
```

## 7. Secondary Metrics

```text
load_1, load_2
mean_margin
median_margin
min_margin_off_boundary
prototype_angle_deg
tie_fraction
router_oracle_disagreement_rate
random_router_margin
degenerate_case_status
```

## 8. Known Good / Known Bad / Known Confusing Cases

Known good:

```text
m_1 and m_2 are clearly separated.
Expected: load near 50/50, positive mean margin, router-oracle agreement near 1.0.
```

Known bad:

```text
m_1 = m_2 or m_1≈m_2.
Expected: load may remain near 50/50, but margin becomes zero or tiny.
```

Known bad:

```text
a_1+a_2≈0 for one expert.
Expected: prototype is undefined; the metric should reject this case rather than silently produce a claim.
```

Known confusing:

```text
random 50/50 routing.
Expected: load is balanced, but compatibility margin is not guaranteed. This protects against confusing load balance with specialization.
```

Known confusing:

```text
distance to span(A_e).
Expected: if both experts span R^2, distance is zero to both and cannot define routing.
```

## 9. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| S0: expert generation | Are expert vectors valid unit vectors? | norms of a_i | pass if all norms ≈ 1 | `tables/vector_norms.csv` | continue or regenerate |
| S1: prototype construction | Are prototypes defined and non-degenerate? | \|\|a_1+a_2\|\|, \|\|a_3+a_4\|\|, angle(m1,m2) | fail if prototype norm too small; unclear if angle too small | `tables/prototype_stats.csv` | mark degenerate |
| S2: uniform input sampling | Is input distribution uniform on S^1? | angle histogram | pass if angle bins are close to uniform | `figures/input_angle_hist.png` | continue |
| S3: oracle routing | Does oracle partition load evenly? | load_error | pass if <= 0.02 | `tables/oracle_metrics.csv` | evaluate margin |
| S4: specialization margin | Does selected expert have higher compatibility? | mean_margin, min_margin_off_boundary | pass if mean_margin > 0 and off-boundary margins nonnegative | `figures/margin_hist_seed_<id>.png` | decide specialization |
| S5: router equivalence | Does linear router reproduce oracle? | agreement | pass if >= 0.999 excluding ties | `tables/router_agreement.csv` | confirms initialization |
| S6: degenerate controls | Do known bad cases fail correctly? | degenerate-case metrics | pass if failure reason matches prediction | `figures/degen_cases.png` | boundary update |

## 10. Algorithm Specification, If Nontrivial

input:

```text
n_expert_seeds
n_input_samples
epsilon_load
epsilon_margin
boundary_tolerance
degenerate_norm_threshold
```

parameters:

```text
n_expert_seeds = 100
n_input_samples = 10000
epsilon_load = 0.02
epsilon_margin = 0.0
boundary_tolerance = 1e-6
degenerate_norm_threshold = 1e-4
```

intermediate variables:

```text
a_1,a_2,a_3,a_4
A_1,A_2
m_1,m_2
q_1(x), q_2(x)
g_oracle(x)
g_router(x)
Delta(x)
load_error
prototype_angle
```

steps:

```text
1. For each expert seed, sample four random angles and convert them to unit vectors.
2. Pair vectors into A_1 and A_2.
3. Compute m_1 and m_2.
4. If a prototype is undefined, record degenerate status and skip main-pass judgment.
5. Sample x uniformly from S^1.
6. Compute q_1(x), q_2(x).
7. Route by oracle argmax.
8. Compute load_error and margin.
9. Set router rows w_1=m_1, w_2=m_2.
10. Route with the linear router and compute agreement with oracle.
11. Run known bad and confusing controls.
12. Save tables and figures.
```

outputs:

```text
tables/metrics_by_seed.csv
tables/aggregate_metrics.csv
tables/degen_case_metrics.csv
figures/partition_seed_<id>.png
figures/margin_hist_seed_<id>.png
figures/degen_cases.png
```

debug artifacts:

```text
input angle histogram
prototype direction plot
decision boundary plot
seed-level metric table
```

pass conditions:

```text
Most non-degenerate random seeds satisfy joint_partition_validity.
Known bad cases fail for predicted reasons.
Linear-router implementation agrees with oracle.
```

fail conditions:

```text
Non-degenerate seeds show systematic load imbalance.
Margins are not positive under the oracle rule.
Linear router does not reproduce oracle assignment.
Degenerate cases are not detected.
```

failure reasons:

```text
physical prior false: expert initialization does not provide usable geometry.
mathematical model false: prototype metric does not induce the claimed partition.
operationalization false: prototype is a bad proxy for expert geometry.
implementation false: router implementation does not match oracle.
metric false: load/margin do not capture the intended judgment.
```

## 11. Success / Failure / Insufficient Evidence

Success:

```text
For non-degenerate prototypes, the proof and simulation both show near-50/50 load.
The selected expert has positive compatibility margin away from the boundary.
The linear router initialized with w_e=m_e reproduces the oracle assignment.
Known degenerate and confusing cases behave as predicted.
```

Failure:

```text
The prototype gate does not balance load under uniform input.
The prototype gate balances load but does not produce positive compatibility margin.
The linear router fails to reproduce the oracle.
Known degenerate cases do not expose the expected failure modes.
```

Insufficient evidence:

```text
Only one seed is shown.
Only a visual partition is shown.
Only load balance is reported.
No margin is reported.
Degenerate cases are not tested.
Router-initialization equivalence is not checked.
```

## 12. What This Cannot Claim

```text
This does not solve real MoE collapse.
This does not prove semantic feature-level specialization.
This does not prove high-dimensional scalability.
This does not prove training preserves the partition.
This does not prove common removal is sufficient.
This does not prove expert functional utility alignment.
```

## 13. Approval Status

```text
status: proposed_for_user_review
approved_to_run: no
approval_needed_from_user: yes
next action after approval: implement the static 2D oracle-gate script and generate the required tables/figures.
```
