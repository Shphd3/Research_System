# Protocol: A13_00_06_E01 Soft-Relay MTP-versus-NTP Audit

## 0. Approval Snapshot

Approval status: **approved** by the researcher on 2026-07-17.

The researcher explicitly authorized implementation and execution after a
contract-consistency self-audit. Any change to the objects frozen below
requires stopping and obtaining new approval.

## 1. Terminology / Definitions

- **Soft relay:** the direct `ANSWER`-to-$A$ attention edge remains available
  but receives a finite attention-logit penalty in both layers.
- **Hard relay:** that edge receives $-\infty$ and is unavailable.
- **Causal use:** answer loss changes under an in-distribution path
  intervention. Attention weight alone is not causal use.
- **AULC:** the trapezoidal area under ordinary-head answer NLL from step 0
  through step 1,000, divided by 1,000, in nats. Lower is better.
- **Gradient dose:** the realized auxiliary-loss gradient norm reaching the
  shared Transformer trunk; matching nominal loss weight does not guarantee
  matching this value.

## 2. Anchor Alignment

Primary anchor:
[13_00_06 soft-relay mechanism](/Projects/from-attention-to-search/main/problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_06_soft_relay_mtp_ntp_audit_anchor.md)

Decision question: does information-specific MTP utility grow with measured
causal relay dependence before the direct path is fully cut?

## 3. Tested Hypothesis

For path level $r$,

$$
U_r
=
\operatorname{AULC}_{\rm shared\text{-}aux,r}
-
\operatorname{AULC}_{\rm informative\text{-}MTP,r}.
$$

The registered hypothesis is that $U_r$ has a stable positive relation to
NTP-only measured relay reliance across all four path levels and across the
three finite levels. The hard endpoint must not be the sole source of the
effect.

## 4. Rival Explanations

1. finite penalties do not induce ordered causal path use because the model
   compensates their logits;
2. MTP gains only when a hard mask creates an artificial graph regime;
3. $U_r$ merely tracks slower NTP learning as the task becomes harder;
4. informative-MTP supplies a larger realized auxiliary gradient dose than
   shared-aux;
5. the auxiliary target forms information that is not transported or used by
   the ordinary head;
6. a treatment arm lacks capability, making AULC contrasts uninterpretable.

## 5. Frozen Data, Model, And Training

### Data

```text
[BOS] [FIXED] [A] [B] [RELAY] [ANSWER] [A]
```

- answer rule: $Y=A$;
- $A,B$ are iid uniform over 16 value tokens;
- evaluation split: $(A+2B)\bmod 5=0$;
- no query, composition, multiple evidence, added distance, code, language,
  or MoE object;
- the answer token is a target and not part of the prediction prefix.

### Attention graph

- positions 0--3 use their frozen causal prefix;
- `RELAY` reads `[FIXED,A,B,RELAY]`;
- `ANSWER` always reads `[RELAY,ANSWER]`;
- the only variable edge is `ANSWER`-query to the $A$ token at position 2;
- `FIXED` and $B$ are never alternate direct inputs to `ANSWER`;
- the same additive mask is applied in both Transformer layers.

The four frozen penalties are:

| Path label | Penalty $\beta$ | Direct-edge multiplier before softmax |
| --- | ---: | ---: |
| `direct_0` | 0 | 1.000000 |
| `soft_2` | 2 | 0.135335 |
| `soft_4` | 4 | 0.018316 |
| `hard` | $+\infty$ | 0 |

No pilot or objective result may change these values.

### Model

- decoder-only Transformer;
- width 64, two layers, four attention heads, FFN width 256;
- dropout 0;
- standard head tied to token embeddings;
- the auxiliary head is instantiated and trainable in every condition;
- no parameter changes across path or objective conditions.

### Training

- AdamW, learning rate 0.003, cosine decay to 0.0001;
- betas $(0.9,0.95)$, weight decay 0.01, gradient clip 1.0;
- batch size 256, maximum 3,000 steps;
- evaluation every 20 steps;
- fresh paired seeds 1801--1808;
- paired objectives use identical initialization, batch-index stream,
  training tokens, and checkpoints.

## 6. Frozen Objectives

1. **NTP-only:** ordinary head predicts next token; auxiliary head exists but
   its loss is inactive.
2. **Matched shared-aux:** ordinary head and auxiliary head both predict the
   next token; total loss is the mean of the two all-position CE losses.
3. **Informative-MTP:** ordinary head predicts next token; auxiliary head
   predicts the next-two token; total loss is the mean of the two all-position
   CE losses.

The primary causal comparison is informative-MTP versus matched shared-aux.
NTP-only versus informative-MTP is secondary.

## 7. Two-Stage Execution Contract

### Stage 0: NTP-only carrier audit

Run NTP-only for every seed and penalty. Compute at step 1,000 and final step:

$$
D_{\rm direct}
=L_{\rm delete\ direct}-L_{\rm native},
$$

$$
D_{\rm relay}
=L_{\rm wrong\ relay\ donor}-L_{\rm native},
$$

and

$$
\rho
=
\frac{\max(D_{\rm relay},0)}
{\max(D_{\rm relay},0)+\max(D_{\rm direct},0)+10^{-8}}.
$$

The wrong relay donor comes from an evaluation example with a different $A$
and the same carrier format. Report both receiver-label accuracy and donor-$A$
follow accuracy. The direct intervention changes only the registered edge.

Stage 0 passes only if all conditions hold:

1. each penalty has final mean answer accuracy $\ge0.95$ and at least 7/8
   seeds at $\ge0.90$;
2. each penalty has at least 7/8 seeds reaching 90% answer accuracy by step
   1,000, and no penalty is solved before the first positive checkpoint in all
   eight seeds;
3. the seed-paired slope of $D_{\rm direct}$ versus path rank is negative,
   its 95% bootstrap upper bound is below zero, and at least 7/8 seed slopes
   are negative;
4. the slopes of $D_{\rm relay}$ and $\rho$ versus path rank are positive,
   their 95% bootstrap lower bounds are above zero, and at least 7/8 seed
   slopes are positive.

If any item fails, the run writes a Stage-0 stop record and does not launch or
read Stage 1.

### Stage 1: objective comparison

Only after Stage 0 passes, run all three objectives under all four penalties.
NTP-only may reuse the registered Stage-0 runs; shared-aux and informative-MTP
must use the identical paired contract.

## 8. Primary Metric And Trend Tests

For each seed and penalty,

$$
U_{i,r}=\operatorname{AULC}_{\rm SA,i,r}
-\operatorname{AULC}_{\rm MTP,i,r}.
$$

Compute per-seed least-squares slopes of $U$ on the Stage-0 NTP-only $\rho$:

- `overall_slope`: all four penalties;
- `finite_slope`: penalties 0, 2, and 4 only.

Use 10,000 paired seed bootstraps. The main pass requires:

1. both mean slopes have 95% lower bounds above zero;
2. at least 7/8 individual seed slopes are positive for both objects;
3. at least one of $U_{\rm soft\_2}-U_{\rm direct\_0}$ or
   $U_{\rm soft\_4}-U_{\rm direct\_0}$ has a paired-bootstrap lower bound
   above zero;
4. all treatment cells satisfy final capability: mean accuracy $\ge0.95$ and
   at least 7/8 seeds at $\ge0.90$.

## 9. Difficulty And Gradient-Dose Guards

Let $H_{i,r}$ be NTP-only AULC. Let $G_{i,r}$ be the log ratio of informative-
MTP to shared-aux auxiliary shared-trunk gradient norms, averaged over
registered checkpoints $\{0,100,200,400,600,800,1000\}$.

Fit within-seed centered regressions:

$$
U=\alpha_i+b_\rho\rho+b_HH+\epsilon,
$$

and

$$
U=\alpha_i+b_\rho\rho+b_HH+b_GG+\epsilon.
$$

Bootstrap whole seeds 10,000 times. A Pass requires the 95% lower bound for
$b_\rho$ above zero in both models. Standardize predictors before fitting; if
either design condition number exceeds 100 or a bootstrap fit is singular,
the result is Insufficient rather than Pass.

These guards can rule against the measured gross dose and baseline-difficulty
accounts. They cannot prove that no unmeasured optimization confound exists.

## 10. Registered Diagnostics And Secondary Metrics

- NTP-only minus informative-MTP AULC as a secondary system contrast;
- answer NLL and accuracy every 20 steps;
- final answer NLL and accuracy;
- first registered checkpoint reaching 90% answer accuracy;
- direct deletion and relay donor-patch effects at steps 1,000 and 3,000;
- ordinary answer-loss and auxiliary-loss gradient norms at the layer-1 relay
  state and shared trunk at steps $\{0,100,200,400,600,800,1000\}$;
- answer/auxiliary shared-trunk and relay-state gradient cosine;
- every seed-level effect and no selectively omitted seed.

## 11. Pass / Fail / Insufficient

**Pass:** Stage 0 passes; all Stage-1 capability and trend criteria pass; the
positive trend is present before the hard endpoint; and the measured relay
coefficient survives both difficulty and gradient-dose guards.

**Fail / Stop:** Stage 0 passes and uncertainty is adequate, but $U$ is
unrelated or oppositely related to measured relay reliance, only the hard mask
has benefit, or the benefit disappears after baseline-difficulty adjustment.

**Insufficient:** Stage 0 does not create ordered actual dependence; any key
condition fails capability or common-window requirements; trend intervals
cross zero; or the registered regression is too collinear/singular to
distinguish relay reliance from difficulty or dose.

No failed or insufficient result may be relabeled as MTP success.

## 12. Figure Contracts

### Core learning curves

- question: how quickly does the ordinary head learn under each objective and
  penalty?
- metric/unit: answer NLL in nats; accuracy is secondary;
- source: all registered checkpoints and seeds;
- aggregation: seed mean with 95% paired-bootstrap band;
- layout: four penalty panels, objective color, step 0--1,000 primary window;
- allowed conclusion: descriptive trajectory and AULC origin;
- limitation: visual separation is not the registered trend test.

### Path-dependence figure

- question: does information-specific utility grow with measured causal relay
  reliance?
- x-axis: NTP-only $\rho$ at step 1,000;
- y-axis: paired $U$ in nats;
- points: every seed/penalty, with penalty-specific symbols; mean trend shown
  separately;
- allowed conclusion: direction and continuity of the registered moderator;
- limitation: $\rho$ is based on two interventions, not exhaustive mediation.

## 13. Artifact Contract

The result folder will contain `summary.md`, `detailed.md`, tables for Stage-0
gates, primary effects, capability, causal patches, gradients, and seed-level
trajectories, plus the two registered figures. Raw logs and checkpoints remain
in the worker output directory and are linked, not copied into the research
mainline.

## 14. Scope And Stop Rules

Do not add penalties, seeds, model sizes, objectives, tasks, or follow-up
diagnostics after reading results. Do not enter query binding, composition,
code, natural language, long context, planning, or MoE. Do not edit the graph,
root sync, commit, or push.

## 15. Protocol Self-Audit

- one changed object: `ANSWER`-to-$A$ logit penalty;
- literal primary comparison: informative-MTP versus matched shared-aux;
- NTP-only used for the pre-treatment carrier gate and secondary comparison;
- penalties, seeds, metric, gates, and stop logic frozen before execution;
- information formation, transport, and standard-head use kept distinct;
- no result-contingent expansion authorized.

Verdict: the protocol matches the researcher-frozen contract and is approved
for direct implementation and four-GPU execution.
