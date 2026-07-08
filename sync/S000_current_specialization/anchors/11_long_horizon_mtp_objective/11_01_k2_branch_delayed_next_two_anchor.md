# 11_01 K=2 Branch-Delayed Next-Two Anchor

Status: supported by the minimal K=2 run on 2026-07-06.
Parent line: `11_long_horizon_mtp_objective`.
Source theory document: `daily_research_reports/0707/mtp_k2/mtp_k2_self_contained_theory_proof.md`.

## 0. Thinking Card

**Phenomenon:** In a minimal long-horizon branch distribution, the early branch key $B$ does not affect the first future token $Y_1$, but determines the second future token $Y_2$. Thus next-one at $T$ can learn the shared next token without exposing $B$ in the same prefix hidden state $h_T$.

**Mechanism guess:** Next-two attaches the branch-specific target $Y_2=S_B$ to the same $h_T$. If $h_T$ is branch-blind, the optimal second-token cross-entropy is still $\log m$.

**Key variables:** early branch key $B$; prefix hidden state $h_T$; shared token $Y_1=A$; branch-specific token $Y_2=S_B$; second-token loss $\lambda\operatorname{CE}(q_2(\cdot\mid h_T),S_B)$.

**Causal relation:** When $Y_1$ contains no branch information but $Y_2$ does, next-one at $T$ can be satisfied by branch-blind $h_T$; next-two forces branch-blind $h_T$ to pay at least $\lambda\log m$ expected loss.

**Observable metric:** Primary metric is `offset2_single_prefix_accuracy`: top-1 accuracy for predicting $S_B$ from the same $h_T$ when the prefix stops before $A$.

**Rival explanations:** Native offset-2 success could be a trained-head artifact; fixed-next-one might already encode $B$ through random identity leakage; rollout success could come from $h_{T+1}$ recomputing from the full prefix.

**Decision:** The clean K=2 mechanism is supported. Proceed to a minimal K>2 branch-controlled suffix extension; do not claim curriculum or natural-language transfer yet.

## 1. Problem Definition

**Parent problem:** Build a rigorous link between long-horizon language dependencies and multi-token prediction.

**Sharper subproblem:** In a minimal K=2 branch-delayed distribution, prove and test whether next-two imposes a direct branch-relevant requirement on the same $h_T$ that next-one at $T$ does not impose.

**Terminology / Definitions:**

| Term | Plain meaning | Concrete object or computation | Unit / formula | Why it matters | What it cannot prove |
|---|---|---|---|---|---|
| long-horizon dependency | Early information matters only later | $B$ determines $Y_2=S_B$ after filler and shared context | conditional relation | Matches the advisor's first-chapter / final-chapter structure | All natural-language long-range tasks |
| prefix hidden state $h_T$ | The decision state before future targets | $h_T=f_{\theta,T}(\operatorname{BR}_B,F_1,\ldots,F_L,U)$ | vector | Theory and experiment ask whether this state exposes $B$ | Whether $h_{T+1}$ exposes $B$ |
| branch-blind | $h_T$ does not distinguish branch | $h_T^{(1)}=\cdots=h_T^{(m)}$ | condition | Object of the lower-bound theorem | The whole model knows nothing about $B$ |
| next-one | Predict only $Y_1$ from $h_T$ | $L_1=\operatorname{CE}(q_1(\cdot\mid h_T),A)$ | loss | Control objective | All NTP training positions |
| next-two | Predict $Y_1,Y_2$ from the same $h_T$ | $L_2=\operatorname{CE}(q_1,A)+\lambda\operatorname{CE}(q_2,S_B)$ | loss | Main mechanism term | Guaranteed optimization success |
| single-prefix offset-2 accuracy | Direct prediction of $S_B$ from $h_T$ | top-1 accuracy of $q_2(\cdot\mid h_T)$ | 0 to 1 | Primary metric | Natural-language reasoning |
| frozen probe | Linear readout of branch from frozen $h_T$ | classifier $h_T\to B$ | accuracy | Guards against head-only interpretation | Native head usability |
| branch-swap consistency | Replace only early branch token and check suffix switch | `BR_b -> BR_c` should switch $S_b\to S_c$ | rate | Guards against local shortcuts | All memorization routes |

**Decision question:** In the clean K=2 branch-delayed distribution, does next-two make the same $h_T$ support branch-specific $S_B$ prediction better than capacity-matched fixed-next-one?

**Not in scope:** MTP always beats NTP; NTP cannot learn long horizon; curriculum is better than full-horizon; synthetic K=2 transfers to real LLMs; MoE expert specialization.

## 2. Physical Priors

**P1: Shared-next-token prior.**
If $Y_1=A$ for all branches, next-one at $T$ can be satisfied by branch-blind $h_T$.

**P2: Branch-delayed target prior.**
If $Y_2=S_B$ and $B\mapsto S_B$ is one-to-one, branch-blind $h_T$ cannot predict $S_B$ with low loss.

**P3: Direct second-token pressure prior.**
The next-two second-token loss acts directly on $h_T$ and provides a branch-dependent target pressure absent from next-one at $T$.

## 3. Falsifiable Hypotheses

**H1:** Fixed-next-one can predict shared $A$ but does not support $h_T\to S_B$.
Supported: fixed-next-one offset-1 accuracy is high while offset-2, frozen probe, and branch-swap are weak.

**H2:** Next-two makes the same $h_T$ support branch-specific second-token prediction.
Supported: next-two has high offset-2 accuracy, worst-branch probability, frozen probe, and branch-swap consistency.

**H3:** The difference comes from second-token supervision, not extra capacity.
Supported: both conditions use the same direct-head architecture, but only next-two succeeds.

## 4. Mathematical Model

Objects:

$$
B\sim\operatorname{Unif}\{1,\ldots,m\},\qquad X=(\operatorname{BR}_B,F_1,\ldots,F_L,U,A,S_B).
$$

Decision state:

$$
h_T^{(B)}=f_{\theta,T}(\operatorname{BR}_B,F_1,\ldots,F_L,U).
$$

Targets:

$$
Y_1=A,\qquad Y_2=S_B.
$$

Information conditions:

$$
I(B;Y_1)=0,\qquad H(S_B)=\log m.
$$

Losses:

$$
L_1(h_T)=\operatorname{CE}(q_1(\cdot\mid h_T),A).
$$

$$
L_2(h_T)=\operatorname{CE}(q_1(\cdot\mid h_T),A)+\lambda\operatorname{CE}(q_2(\cdot\mid h_T),S_B).
$$

If $h_T$ is branch-blind:

$$
\inf_{q_2}\mathbb E[-\log q_2(S_B\mid h_T)]=\log m.
$$

Therefore:

$$
\mathbb E[L_2(h_T)]\ge \lambda\log m.
$$

If:

$$
\mathbb E[-\log q_2(S_B\mid h_T)]\le \delta,
$$

then:

$$
I(h_T;B)\ge \log m-\delta.
$$

## 5. Computational Realization

Input objects:

```text
BR_b F00 F01 F02 F03 F04 F05 F06 F07 U00 U01 A_SHARED S_b STOP
```

The evaluation prefix stops before `A_SHARED`.

Implementation contract: one-layer causal Transformer, two direct heads from $h_T$, identical branch-token initialization, balanced deterministic data, seeds `971,972,973`.

Expected artifacts: `protocol.md`, `summary.md`, `detailed.md`, curated tables.

## 6. Minimal Falsification Tests

| Test | Question | Primary metric | Pass / fail / insufficient | Failure means |
|---|---|---|---|---|
| Direct-supervision test | Does next-two make $h_T$ predict $S_B$ better than fixed-next-one? | `offset2_single_prefix_accuracy` | Pass: next-two high and fixed weak; fail: matched | Operationalization weakened, theorem unchanged |
| Representation guard | Is success only a trained-head artifact? | `frozen_probe_accuracy` | Pass: next-two probe stronger; fail: no probe gain | Native head success is too narrow |
| Causal branch guard | Does prediction depend on early branch key? | `branch_swap_consistency` | Pass: suffix switches with branch; fail: no switch | Branch dependence not established |

## 7. Current Evidence

**Observation:** The formal proof gives the objective-level separation: branch-blind $h_T$ can solve next-one at $T$ but cannot solve next-two when $Y_2=S_B$ identifies branch.

**Experiment result:** A11_01 supports the operationalized mechanism. Across seeds `971,972,973`, fixed-next-one achieved offset-1 accuracy 1.000 but offset-2 accuracy 0.000, frozen probe 0.333, and branch-swap 0.000. Next-two achieved offset-1 accuracy 1.000, offset-2 accuracy 1.000, frozen probe 1.000, and branch-swap 1.000.

**Interpretation:** In the controlled K=2 setup, the second-token objective term is sufficient to make $h_T$ expose branch information, while the shared next-token objective is not.

**Boundary:** The experiment uses identical branch-token initialization and deterministic balanced data to isolate objective pressure. It does not prove robustness under random identity leakage, noisy filler, longer suffixes, curriculum, or real language.

Evidence links:

- `daily_research_reports/0707/mtp_k2/mtp_k2_self_contained_theory_proof.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_01_k2_branch_delayed_next_two/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_01_k2_branch_delayed_next_two/detailed.md`

## 8. Claim Boundary And Next Decision

**Can claim now:** In the controlled K=2 distribution and direct-head model, next-two supplies branch-relevant supervision on $h_T$ that next-one at the same state does not supply; the minimal experiment supports this mechanism.

**Cannot claim now:** MTP always beats NTP; NTP cannot learn long-horizon dependencies; curriculum is better than full-horizon; this synthetic K=2 mechanism transfers to natural language; optimization always succeeds without symmetry control.

**Next decision:** Move to a minimal K>2 branch-controlled suffix anchor/protocol. The first extension should test whether several future suffix tokens sharing the same early cause create the same pressure under weaker symmetry controls, before adding curriculum, noisy filler, or natural-language tasks.
