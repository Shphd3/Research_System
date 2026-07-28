# A06_04_01 Context-Conditioned Expert Utility in a Frozen Code MoE

Thinking Card source: [06_04_real_workload_utility_headroom_thinking_card.md](../06_04_real_workload_utility_headroom_thinking_card.md) (inherited from parent `A06_04`; this subanchor adjudicates one local clause of that approved question).

## 1. Problem Definition

**Parent problem:** determine whether real repository-code completion contains
held-out expert-function headroom that the native Router does not capture.

**Sharper subproblem:** determine whether the relevant cross-file evidence,
rather than raw target-token identity or extra prompt length, changes which
routed expert function is useful for the same completion target.

**Decision question:** when the in-file prefix and target tokens are held fixed,
does adding relevant cross-file context create a positive, split-stable change
in relative expert utility at the final MoE block, together with positive
headroom over native routing?

| Term | Plain meaning | Concrete computation | Decision role | Cannot prove |
| --- | --- | --- | --- | --- |
| Context-paired example | The same code prefix and target under different evidence | relevant cross-file context, no cross-file context, or length-matched irrelevant context precedes the same in-file prefix and target | Controls target and local-token identity | That the benchmark is unfiltered repository code |
| Contextual routing state | The token state actually seen by the Router | hidden vector $h_{i,t,l}^{c}$ at aligned target-predicting position $t$, layer $l$, and context condition $c$ | Defines the routed object | A sample-level semantic class |
| Matched slot swap | Replace one active routed-expert slot without changing active expert count | replace the lowest-weight native routed expert by candidate $e$, keep its gate weight and the other seven routed experts fixed; the registered Qwen checkpoint has no shared expert | Measures candidate expert function under matched activated compute | A deployable routing policy |
| Swap headroom | Loss reduction relative to native routing | $H_e^c=L_{native}^c-L_e^{swap,c}$, in nats per target token | Required evidence that native routing leaves useful expert capacity unused | That a learned Router can find $e$ |
| Context-expert interaction | Relevant context changes the relative ordering of two experts | held-out difference-in-differences $I_{ctx}$ | Primary metric | Semantic meaning of either expert |
| Route overlap | Two context conditions use similar experts | $\sum_e q(e\mid c_1)q(e\mid c_2)$, averaged over aligned positions | Secondary routing diagnostic | Helpful or harmful sharing by itself |

## 2. Physical Priors

1. **The Router acts on a contextual state, not a raw token ID.** If routed
   expert functions are genuinely condition-sensitive, changing necessary
   cross-file evidence while holding the target fixed can change their relative
   utility. This prior is false on the tested surface if expert-utility ordering
   does not change on held-out pairs.
2. **General context benefit is not expert specialization.** A relevant snippet
   may lower every condition's loss without changing relative expert utility.
   Length-matched irrelevant context and a difference-in-differences metric
   expose this rival.
3. **Activated-compute mismatch must not create the effect.** Replacing one of
   eight routed slots while retaining its weight
   isolates expert identity from active-expert count.

## 3. Falsifiable Hypotheses

**Primary hypothesis:** relevant cross-file evidence induces a held-out,
split-stable expert-by-context interaction, and the context-favored expert has
positive loss headroom over the native Router.

**Strongest rival:** apparent expert differences are caused by target identity,
prompt length, a generic benefit from more context, or calibration overfitting;
after target pairing, length matching, and held-out evaluation, no stable
expert-by-context interaction remains.

**Pass:** the native model first benefits from relevant context; the
calibration-selected expert pair is stable across two calibration halves; on
the untouched test split, both $I_{ctx}$ and relevant-context swap headroom are
positive with the registered practical and confidence thresholds.

**Fail:** the native context-capability guard passes, but no registered stable
expert pair has positive held-out interaction and positive headroom.

**Insufficient:** the model does not use the supplied relevant context, the
paired data or slot-swap implementation fails integrity checks, or resource
failure prevents complete evaluation of all 128 experts.

## 4. Mathematical Model

For example $i$, let $x_i^c$ be a prompt under context condition
$c\in\{rel,nuis,local\}$ and let $y_i$ be the identical teacher-forced target in
all three conditions. At final MoE layer $l=26$, the native routed contribution
for target-predicting position $t$ is

$$
m_{i,t,l}^{c}
=\sum_{j=1}^{8}w_{i,t,l,j}^{c}f_{e_{i,t,l,j}^{c}}(h_{i,t,l}^{c}),
$$

where the registered checkpoint has no shared expert. Let $r$ index the
smallest native routed weight. For candidate expert $e$ not already active,
define

$$
m_{i,t,l}^{c,(e)}
=m_{i,t,l}^{c}
-w_{i,t,l,r}^{c}f_{e_{i,t,l,r}^{c}}(h_{i,t,l}^{c})
+w_{i,t,l,r}^{c}f_e(h_{i,t,l}^{c}).
$$

If $e$ is already active at that position, the intervention is a no-op. Let
$L_i^c(e)$ be mean target-token negative log-likelihood after this intervention
and $L_i^c(native)$ the unmodified loss. Candidate headroom is

$$
H_e^c
=\mathbb{E}_i\left[L_i^c(native)-L_i^c(e)\right].
$$

Define the relevant-versus-nuisance utility shift

$$
\delta_e=H_e^{rel}-H_e^{nuis}.
$$

On calibration data only, choose an expert pair

$$
(a,b)
=\arg\max_{e\ne e'}\left(\delta_e^{cal}-\delta_{e'}^{cal}\right),
\qquad H_a^{rel,cal}>0.
$$

The primary held-out metric is the expert-by-context interaction

$$
I_{ctx}^{test}
=\left(H_a^{rel,test}-H_b^{rel,test}\right)
-\left(H_a^{nuis,test}-H_b^{nuis,test}\right).
$$

It is measured in nats per target token. It removes any context effect shared by
all candidate experts, but it cannot establish that a practical Router can
predict $a$ from $h$.

## 5. Computational Realization

- **Model:** frozen local `/data/share/Qwen3-Coder-30B-A3B-Instruct`, loaded
  with network access disabled. Its local config and actual module tree verify
  48 MoE layers, 128 routed experts, eight routed experts per token, and no
  shared expert. The preregistered intervention layer is the final discovered
  MoE block, zero-based layer `47`. The checkpoint fingerprints are frozen in
  the linked canonical protocol.
- **Workload:** the Python line-completion split of CrossCodeEval, using the
  non-oracle retrieval file `line_completion_rg1_unixcoder_cosine_sim.jsonl`.
  It supplies real repository code, a target line, and cross-file fragments
  retrieved without using the reference completion. The benchmark is
  intentionally cross-file-dependent and therefore is not an unfiltered
  repository-code sample.
- **Paired conditions:** relevant cross-file context, local-only context, and a
  different-repository nuisance context truncated to the exact same model-token
  length as the relevant context. The in-file prefix and target are identical.
- **Intervention:** all context positions and all other model layers retain
  native routing. Only positions whose logits predict target tokens receive the
  matched slot swap.
- **Execution:** four H100 GPUs each hold one frozen model replica and shard
  examples by deterministic sample index; each replica evaluates all 128
  candidate expert IDs for its examples. No parameter update occurs. The
  registered selected-pair gradient audit is secondary and was not needed for
  the primary verdict.

## 6. Minimal Falsification Tests

The decisive test uses 256 deterministic, model-utility-unfiltered Python
examples split by repository into calibration-A, calibration-B, and untouched
test sets of 64, 64, and 128 examples.

The subanchor passes only if all clauses hold:

1. **Context-capability guard:** native relevant context improves target loss
   over length-matched nuisance context with paired-bootstrap 95% confidence
   interval lower bound above zero.
2. **Split-stability guard:** expert $a$ is in the top eight $\delta_e$ values
   and expert $b$ is in the bottom eight in both calibration halves.
3. **Primary interaction:** $I_{ctx}^{test}\ge 0.01$ nats per target token and
   its paired-bootstrap 95% confidence interval lower bound is above zero.
4. **Absolute utility guard:** $H_a^{rel,test}\ge 0.01$ nats per target token
   and its paired-bootstrap 95% confidence interval lower bound is above zero.
5. **Implementation guard:** native replay and a formal no-op swap agree within
   the registered numerical tolerance; all 128 candidates and all three context
   conditions complete without missing shards.

The main falsifier is a passed context-capability guard followed by absent or
unstable held-out expert interaction/headroom. That result would reject this
context-conditioned functional-headroom clause at the final MoE block, not at
every layer or on every language.

## 7. Current Evidence

**Verdict: failed on the registered surface.** The run is complete and all
integrity guards passed, so this is not an insufficient-evidence result.

Direct evidence:

- 256/256 repository-disjoint examples, all three conditions, and all 128
  candidates completed; all losses were finite.
- Four-GPU full job `pt-loe1371e` succeeded. Peak allocation was
  57.07--57.15 GiB per H100.
- Cached final-layer replay, literal full forward, and formal no-op agreed with
  zero observed logit and token-NLL error after the BF16 addition-order fix.
- Native context gain passed:
  $L^{nuis}-L^{rel}=0.20370$, 95% CI [0.05908, 0.35929].
- Calibration selected $a=49$ and $b=53$. Expert 49 ranked 8th on cal-A but
  16th on cal-B, so the split-stability guard failed; expert 53 was bottom-eight
  on both halves.
- Held-out interaction passed:
  $I_{ctx}=0.01163$, 95% CI [0.00336, 0.02022].
- Absolute headroom failed:
  $H_{49}^{rel}=0.00540$, 95% CI [-0.00105, 0.01225].

Mechanism reading: expert 49's context shift was only 0.00082. Most of the
positive interaction came from expert 53 becoming more harmful under relevant
context, with shift -0.01081. The interaction therefore identifies
context-conditioned bad-expert sensitivity, not stable positive utility missed
by the native Router. Aggregate REL/NUIS expert-utility rankings were similar
on test (Spearman 0.891), while context shifts were not reproducible between
calibration halves (Spearman 0.083).

Result records:

- [summary.md](/Projects/from-attention-to-search/main/experiments/A06/06_04_real_workload_utility_headroom/A06_04_01_E01_context_conditioned_expert_utility/summary.md)
- [detailed.md](/Projects/from-attention-to-search/main/experiments/A06/06_04_real_workload_utility_headroom/A06_04_01_E01_context_conditioned_expert_utility/detailed.md)
- [primary_metrics.json](/Projects/from-attention-to-search/main/experiments/A06/06_04_real_workload_utility_headroom/A06_04_01_E01_context_conditioned_expert_utility/artifacts/primary_metrics.json)

## 8. Claim Boundary And Next Decision

**Supported now:** relevant evidence changes final-layer expert
counterfactual effects, and the native model distinguishes relevant from
length-matched nuisance context on this workload. The registered numerical and
resource methodology is validated.

**Weakened or rejected now:** the frozen final-layer expert pool does not
provide the registered split-stable, context-favored positive headroom that a
better Router could simply recover. A positive $I_{ctx}$ alone is not adequate
evidence because it can be caused by a candidate becoming more harmful.

**Not supported now:** unfiltered repository-wide headroom, a learned Router,
faster rare learning, common-information preservation, conflict isolation,
expert semantics, other layers, or long-context scaling.

**Exactly one next decision:** test whether training-time selective sharing can
create stable positive context-conditioned utility on an explicit real
rare/common workload, rather than continuing to mine this frozen last-layer
expert pool.
