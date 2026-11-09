# Summary: A11_03 K=2 Semantic Efficiency

Status: completed on 2026-07-07 with reserved 4-GPU remote job `pt-m5foezfm`.

## What We Established

In the controlled K=2 decision-only task, next-two learns the branch-relevant state earlier and more often than matched fixed-next-one. The clean-regime evidence supports a narrow efficiency claim: when the immediate next token is shared but the second token identifies the early branch variable, the next-two loss can make $Z$ recoverable from the same prefix state $h_T$ earlier than next-one.

The claim is not universal. Under symmetry-controlled `identical_branch` initialization, next-two succeeds in only 2 of 5 seeds, so the result supports useful direct supervision with acquisition instability, not guaranteed optimization success.

## Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Why it matters | What it cannot prove |
| --- | --- | --- | --- | --- |
| `fixed_next_one_2head` | capacity-matched next-token baseline | same trunk and two heads, but loss is only $L_1$ | controls extra heads | all NTP behavior |
| `shared_trunk_next_two` | K=2 MTP condition | same trunk predicts $Y_1,Y_2$ with loss $L_1+\lambda L_2$ | main test condition | universal MTP superiority |
| clean regime | second token carries branch information | $Y_1=A,\;Y_2=S_Z$ | target-information condition | natural-language semantics |
| noisy regime | second token is branch-independent | $Y_2\perp Z$ | false-positive guard | all noisy objectives |
| redundant regime | immediate token already reveals branch | $Y_1=S_Z,\;Y_2=T_Z$ | separates new horizon information from local information | long-horizon advantage |
| guarded score $Q_{\mathrm{eval}}$ | conservative branch-recovery score | $\min\{A_{\mathrm{eval}},P_{\mathrm{eval}},S_{\mathrm{eval}}\}$ | primary recovery metric | full causal proof |
| `T_0.9_eval` | time to guarded recovery | first step where $Q_{\mathrm{eval}}\ge0.9$ for consecutive evaluations | primary efficiency metric | final capability |

## Setup

Clean data:

```text
BR_z F_00 ... F_15 U_00 ... U_03 A_SHARED S_z
```

Targets:

$$
Y_1=A,\qquad Y_2=S_Z,\qquad I(Z;Y_1)=0,\qquad I(Z;Y_2\mid Y_1)>0.
$$

Objectives:

$$
L_{\mathrm{fixed1}}=L_1,\qquad
L_{\mathrm{next2}}=L_1+\lambda L_2.
$$

Configuration: one-layer one-head Transformer, `d_model=64`, `num_branches=4`, `filler_length=16`, `shared_context_length=4`, seeds `971-975`, `decision_only` objective, both `identical_branch` and `random` initialization.

## Main Result

Clean-regime mean results:

| Init | Condition | Reach rate for $Q_{\mathrm{eval}}\ge0.9$ | Mean reached step | AUC $Q$ | Final $Q$ | Final $Y_1$ acc | Final native $Y_2$ acc |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| identical | fixed next-one | 0.00 | NA | 0.250 | 0.250 | 1.000 | NA |
| identical | next-two | 0.40 | 1500 | 0.536 | 0.550 | 1.000 | 0.550 |
| random | fixed next-one | 0.00 | NA | 0.288 | 0.250 | 1.000 | NA |
| random | next-two | 0.80 | 1000 | 0.895 | 0.900 | 1.000 | 0.900 |

Decision contrast:

| Init | $\Delta$ AUC $Q$ | $\Delta$ final $Q$ | $\Delta$ reach rate |
| --- | ---: | ---: | ---: |
| identical | +0.286 | +0.300 | +0.400 |
| random | +0.607 | +0.650 | +0.800 |

Interpretation: next-two improves branch recovery while preserving immediate next-token accuracy. Fixed next-one learns $Y_1$ perfectly but remains at chance-level guarded branch recovery in the clean condition.

## Control Results

| Regime | Main observation | Interpretation |
| --- | --- | --- |
| clean | next-two beats fixed next-one on AUC $Q$ and final $Q$ | supports direct branch supervision from $L_2$ |
| noisy | identical-init next-two stays at chance; random-init next-two has a weak false-positive bump | random initialization can leak branch-readable structure, so random-init claims need guarded interpretation |
| redundant | both objectives can recover branch because $Y_1$ already reveals it | not evidence for long-horizon MTP advantage |

## Hypothesis Status

| Hypothesis | Status | Reason |
| --- | --- | --- |
| H1: K=2 efficiency | supported with instability | clean next-two improves AUC $Q$, final $Q$, and reach rate over matched fixed next-one |
| H2: local preservation | supported | final $Y_1$ accuracy is `1.00` for all clean conditions |
| H3: metric validity | partially supported / guarded | noisy identical-init is negative, but noisy random-init shows a weak false-positive signal |

## Claim Boundary

Can claim:

- In this controlled decision-only K=2 task, next-two provides a useful branch-specific learning signal that matched fixed next-one lacks at $h_T$.
- The advantage is measured as faster or more frequent guarded recovery of $Z$ from $h_T$, not as lower language-model loss.
- The result strengthens the prior representation-requirement theorem into a controlled learning-efficiency result.

Cannot claim:

- MTP universally beats NTP.
- NTP cannot learn long-horizon variables in general.
- K>2 follows automatically.
- Random-init branch recovery is clean causal evidence by itself.
- This proves natural-language long-horizon improvement.

## Next Decision

Use A11_04 to test whether the mechanism is better described by first-informative-horizon coverage: MTP should help when $K$ reaches the first future token whose target contains new information about the early variable.

## Source Artifacts

- Protocol: `Projects/from-attention-to-search/main/experiments/A11/A11_03_k2_semantic_efficiency/protocol.md`
- Detailed record: `Projects/from-attention-to-search/main/experiments/A11/A11_03_k2_semantic_efficiency/detailed.md`
- Code workspace: `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments`
- Runner: `active/synthetic_data_understanding/scripts/run_a11_03_04_semantic_efficiency.py`
- Config: `active/synthetic_data_understanding/configs/a11_03_k2_semantic_efficiency.json`
- Result dir: `active/synthetic_data_understanding/results/a11_03_k2_semantic_efficiency/a11_03_k2_efficiency_decision_only_4gpu_20260707_1708`
- Remote job: `pt-m5foezfm`
