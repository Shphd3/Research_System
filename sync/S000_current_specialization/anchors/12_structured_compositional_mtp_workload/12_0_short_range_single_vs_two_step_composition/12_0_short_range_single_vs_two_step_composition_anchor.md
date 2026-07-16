# Anchor 12_0 — Short-Range Single-Step versus Two-Step Composition

Thinking Card source: [12_0_short_range_single_vs_two_step_composition_thinking_card.md](12_0_short_range_single_vs_two_step_composition_thinking_card.md)

## 1. Problem Definition

**Parent problem:** what substantive difference does next-two-token prediction introduce relative to next-token prediction in training signal and learned function?

**Sharper subproblem:** with answer distance, sequence length, fact count, vocabulary, output format, and model held fixed, does MTP accelerate standard-head learning more when answering requires two ordered relation applications rather than one?

### Terminology / Definitions

| Term | Plain meaning | Concrete object or computation | Unit / formula | Why it matters | Cannot prove |
|---|---|---|---|---|---|
| fresh graph instance | every example supplies two maps that exist only in that example | five active nodes, two relation aliases, two bijections, and fresh row/block order per sample | one 31-token sequence | removes a fixed global truth table | that the model uses an explicit symbolic algorithm |
| composition depth | number of ordered relation applications needed for the answer | $Y=r_1(A)$ or $B=r_1(A),\;Y=r_2(B)$ | 1 or 2 | structural independent variable | long physical distance or deeper-tree behavior |
| balanced dual-map carrier | both tasks read the exact same two tables and query | one-step outputs $B=\pi_1(A)$; two-step outputs $Y=\pi_2(B)$; inputs differ only at `DEPTH` | two five-row bijection tables | matches serialization, query, map content, and answer position | that the second table is necessary evidence in a genuine one-step task |
| standard head | common next-token prediction head | $q_1(h_{\mathrm{SHARED}})$ predicts `ANSWER_Y` | answer accuracy | deployment-equivalent output surface | causal reliance on $B$ |
| steps to threshold | first evaluation step reaching a frozen accuracy level | $T_{d,c,o,s}(\tau)$ on the sealed final-confirmation set | optimizer steps | primary learning-speed measure | wall-clock or FLOP efficiency |
| capability gate | all compared conditions can learn before their speed is interpreted | stable final-window $q_1$ accuracy at the frozen threshold | pass / fail | prevents floor effects from becoming mechanism claims | why a condition learned |

**Logical clarification:** a genuine one-step answer cannot causally depend on the second map. E04 therefore shows both tasks the same two tables, while the second table is only a matched control in the one-step condition. Making it determine the one-step answer would turn that condition into a two-step task and destroy composition depth as the independent variable.

**Decision question:** after NTP-only difficulty calibration and threshold freezing, is the paired composition interaction $\Gamma_d(\tau)$ reproducibly positive on untouched graph instances and confirmation seeds at eligible model scales?

**Not in scope:** fixed finite truth-table fitting, more than two steps, long token distance, natural-language transfer, explicit output of $B$, hidden-state intervention, or causal proof that the standard head uses $B$. The last question remains owned by `12_03`.

## 2. Physical Priors

**P1 — Per-example regeneration removes the fixed-map shortcut.** If active nodes, relation labels, both bijections, and serialization order are resampled independently for every example, no stable tuple $(A,r_1,r_2)$ determines $Y$ across the dataset. The model must condition on the current maps. This prior would be wrong if a generator-aware query-hidden predictor reaches the frozen mastery threshold, alias imbalance predicts the answer, or base instances repeat across splits.

**P2 — Matched layout makes the objective-by-depth interaction informative.** Both tasks expose the same query, two maps, final-answer position, and token count. A pure answer-distance or generic extra-loss effect should therefore act similarly on the two tasks; a larger two-step gain is more consistent with structure-dependent usefulness. This prior would be wrong if second-map relevance, residual difficulty, or token-statistic differences interact with MTP.

**P3 — Learnability is a prerequisite.** Steps-to-threshold is interpretable only when both NTP and MTP stably learn both tasks. Failure to reach the frozen threshold is a capability failure, not evidence about intermediate-state use.

## 3. Falsifiable Hypotheses

**$H_1$ — Structure-dependent speed interaction:** for an eligible scale, MTP reduces steps-to-threshold more on the two-step task than on the matched one-step task.

**Supported if:** untouched confirmation seeds show a reproducibly positive $\Gamma_d(\tau)$ under the protocol's frozen rule.

**Weakened if:** both tasks are learnable but the MTP gain is similar across depths, seed-unstable, or larger for the one-step task.

**Capability null:** at least one task/objective condition cannot stably reach the frozen threshold within budget. In that case $H_1$ is not adjudicated.

## 4. Mathematical Model

For composition depth $c\in\{1,2\}$, draw a graph instance

$$
g\sim\mathcal{D}_c(\theta),
$$

where $\theta$ fixes five active nodes, two five-row bijections, the vocabulary, a 31-token serialization, and the answer position. Each draw independently samples active aliases, both maps, relation aliases, row order, and table-block order.

For model depth $d$, objective $o$, and seed $s$, define

$$
T_{d,c,o,s}(\tau)
=
\min\{t:\operatorname{Acc}^{q_1}_{d,c,o,s}(t)\ge\tau\}.
$$

The MTP speed gain and composition interaction are

$$
G_{d,c,s}(\tau)
=
T_{d,c,\mathrm{NTP},s}(\tau)
-T_{d,c,\mathrm{MTP},s}(\tau),
$$

$$
\Gamma_{d,s}(\tau)
=
G_{d,2,s}(\tau)-G_{d,1,s}(\tau).
$$

Positive $\Gamma_{d,s}$ means the MTP step advantage is larger for two-step examples. It does not identify whether the advantage comes from an explicit internal $B$, general extra supervision, or another optimization effect.

## 5. Computational Realization

- Serialize every example as `[DEPTH, A, R1, R2, MAP1..., MAP2..., DECIDE, SHARED, ANSWER]` with exactly 31 tokens; the final `ANSWER` is the only emitted answer.
- Resample five active aliases, two relation aliases, both bijections, their row order, and table-block order for every example; online training, Stage-A calibration, and Stage-B final-confirmation fingerprints must be disjoint.
- One-step and two-step inputs share the exact query and map tokens and differ only at `DEPTH` and the final answer; no intermediate $B$ is emitted before the answer.
- Two and four layers qualify separately as formal scales; one failed scale neither invalidates nor gets averaged into another scale.
- Train a causal decoder from scratch with full-position language-model cross-entropy.
- Instantiate the same $q_1$ and $q_2$ heads for NTP and MTP. NTP optimizes $q_1$ only; MTP adds full-position $q_2$ prediction at horizon two with weight 1.
- Stage A uses only NTP to qualify the carrier and model scales and to freeze $\tau$; Stage B remains blocked until those objects are frozen and separately approved.
- Store generator manifests, graph-overlap audits, complete learning curves, and the frozen-decision record as the decision artifacts.

## 6. Minimal Falsification Tests

| Test | Question | Comparison | Primary evidence | Pass / fail / insufficient | Failure means |
|---|---|---|---|---|---|
| generator validity guard | does each answer depend on the current query and maps rather than a global tuple or generator-constraint leak? | answer balance, base-fingerprint overlap, necessary-map corruption, relation order, and generator-aware query-hidden prediction | exact audit plus query-hidden accuracy | exact guards pass and query-hidden prediction remains below the frozen threshold / reaches it or deterministic leakage exists / audit incomplete | invalid operationalization, not a failed MTP prior |
| NTP-only eligibility calibration | can each formal scale separately learn both tasks without immediate saturation? | the fixed five-node dual-map carrier under NTP only | complete Stage-A calibration $q_1$ curves | at least one scale satisfies the frozen rule / none does / incomplete trajectories | capability or workload difficulty remains unresolved; do not run MTP |
| untouched confirmation | is MTP's speed gain larger for two-step composition? | NTP versus MTP after generator and $\tau$ are frozen | paired $\Gamma_{d,s}(\tau)$ | protocol-defined positive stability / no positive interaction / capability failure | supports or weakens only a structure-dependent speed interaction |

## 7. Current Evidence

**Observation:** E01 used fixed global rules with held-out ordered pairs and failed the shared two-step capability gate. E02 moved all pairs in support; every scale fit the finite map exactly, but the positive interaction appeared only at exact accuracy `1.0`, and even one layer succeeded. E03 was rejected because its direct-edge one-step and unique-chain two-step examples had asymmetric query-relevant structure. E04 then completed all 12 approved NTP trajectories. No formal scale passed: 2-layer two-step accuracy finished near `0.250` across seeds; 4-layer two-step finished near `0.329`; and 4-layer one-step was itself seed-unstable (`0.999`, `0.838`, `0.998`). A post-run audit also found that deleting one row from a complete bijection does not make the answer unidentifiable because the missing value is recoverable by elimination.

**Interpretation:** E01 was confounded by unseen-pair generalization, E02 was vulnerable to finite-table memorization and an exact-tail metric, E03 had asymmetric query-relevant structure, and E04 fails both an individual-fact necessity guard and the shared NTP capability gate. E04 therefore cannot support a formal NTP/MTP speed comparison.

**Boundary:** E04 establishes a negative carrier-eligibility result under the approved 2/4-layer, 20,000-step contract. It does not weaken or support the MTP interaction hypothesis because MTP was not run and the prerequisite capability gate failed.

**Evidence links:** [E01 summary](/Projects/from-attention-to-search/main/experiments/A12/12_0_short_range_single_vs_two_step_composition/A12_0_E01_short_range_single_vs_two_step/summary.md), [E02 summary](/Projects/from-attention-to-search/main/experiments/A12/12_0_short_range_single_vs_two_step_composition/A12_0_E02_in_support_capability_calibration/summary.md), [E04 summary](/Projects/from-attention-to-search/main/experiments/A12/12_0_short_range_single_vs_two_step_composition/A12_0_E04_balanced_per_sample_dual_map/summary.md), and [E04 detailed record](/Projects/from-attention-to-search/main/experiments/A12/12_0_short_range_single_vs_two_step_composition/A12_0_E04_balanced_per_sample_dual_map/detailed.md).

## 8. Claim Boundary And Next Decision

**Can claim now:** the approved E04 realization is ineligible for objective comparison: neither formal scale gives shared cross-seed NTP capability, no mastery threshold can be frozen, and a complete bijection makes the proposed necessary-row corruption guard invalid.

**Cannot claim now:** that two-step composition is generally unlearnable, that MTP is faster or slower, that any gain is composition-specific, that the model forms or uses $B$, or that the result transfers beyond short synthetic graphs.

Even a positive future result would support only a structure-dependent optimizer-step interaction on fresh short graphs. Full-position MTP adds supervision at many positions and more backward computation, so the result would not by itself establish wall-clock efficiency or isolate an intermediate-state mechanism.

**Exactly one next decision:** decide whether to close E04 under its frozen contract or reopen carrier/capability design in a new Protocol. Stage B and all MTP runs remain blocked until a structurally valid carrier has at least one NTP-eligible scale and a frozen threshold.
