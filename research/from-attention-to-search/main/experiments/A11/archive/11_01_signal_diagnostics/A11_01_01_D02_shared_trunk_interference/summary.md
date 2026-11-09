# Summary: A11_02 K=2 Two-Token Shared-Trunk Signal / Interference

Status: `decision_only` and `all_positions_lm_control` evidence completed locally on 2026-07-07. The reserved 4-GPU remote rerun is still a reproducibility action, not the source of the current evidence.

## What We Established

The K=2 second-token loss $L_2$ is a real branch-relevant signal in `A_clean`, and this conclusion survives the more language-model-like `all_positions_lm_control` objective. In `A_clean`, the shared-trunk all-position model reaches head-2 accuracy, branch-swap preference, and branch-probe accuracy of `1.00`; in `C_noisy`, head-2 accuracy stays near the noise chance level $1/16=0.0625$.

The all-position result refines the earlier `decision_only` result. The earlier decision-only run showed useful branch signal with shared-trunk acquisition instability. Under all-position training, the shared-trunk model solves `A_clean`, while shared embedding and attention still show strong negative $L_1/L_2$ gradient cosine. Therefore the supported claim is: $L_2$ can provide useful long-horizon branch supervision, but branch probe alone is not sufficient evidence and gradient conflict does not automatically imply $L_1$ performance damage.

## Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Why it matters | What it cannot prove |
| --- | --- | --- | --- | --- |
| MTP | multi-token prediction | one prefix state predicts more than one future token | parent objective family | universal improvement over NTP |
| NTP | next-token prediction | one prefix state predicts only $Y_1$ | baseline objective | inability to encode branch in all settings |
| `decision_only` | losses are applied only at the final prefix state | $h_T\to Y_1,Y_2$ at `prediction_site` | matches the clean theory object | ordinary LM behavior |
| `all_positions_lm_control` | losses are averaged over all valid token positions | offset-1 and offset-2 losses across the full sequence | tests whether the clean result survives LM-style background loss | K>2 or natural language |
| `A_clean` | useful second-token branch signal | $Y_1=U,\;Y_2=S_B$ | tests whether $L_2$ can carry branch information | general MTP usefulness |
| `B_redundant` | second token is predictable after the first | $Y_1=S_B,\;Y_2=R(S_B)=T_B$ | checks local/redundant explanations | absence of optimization effects |
| `C_noisy` | second token is branch-independent noise | $Y_1=U,\;Y_2=Z,\;Z\perp B$ | noisy control | all possible noisy objectives |
| `branch_probe_accuracy` | linear readability of branch from hidden states | frozen linear probe $h\to B$ | detects branch representation | usable head-2 prediction by itself |
| `single_prefix_head2_accuracy` | head-2 predicts true $Y_2$ from the decision prefix | top-1 accuracy | tests whether the $L_2$ target is learned | branch causality by itself |
| `branch_swap_preference` | head-2 follows a swapped branch token | swap success rate | causal guard against memorization | all possible shortcut routes |
| $c_s$ | cosine between $L_1$ and $L_2$ gradients | $\langle g_1,g_2\rangle/(\|g_1\|\|g_2\|)$ | diagnoses shared-parameter conflict | sufficient causal proof of final training state |

## Setup

Fixed configuration: `num_branches=4`, `filler_length=16`, `shared_context_length=4`, `train_samples_per_branch=16`, `eval_samples_per_branch=64`, seeds `{971,972,973,974,975}`, one-layer one-head Transformer, `d_model=64`, $\lambda=1.0$, 4000 training steps.

Model conditions:

| Condition | Active objective | Representation sharing |
| --- | --- | --- |
| `ntp_baseline` | $L_1$ only | true one-head baseline |
| `shared_trunk_two_token` | $L_1+\lambda L_2$ | embedding, attention, and MLP shared |
| `shared_attention_separate_expert` | $L_1+\lambda L_2$ | embedding and attention shared; horizon-specific experts |

## Main Result

All-position core condition means:

| Regime | Condition | Init | $Y_1$ acc | head-2 acc | branch probe | swap | Interpretation |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| `A_clean` | `shared_trunk_two_token` | random | 1.00 | 1.00 | 1.00 | 1.00 | branch-specific $L_2$ is learned |
| `A_clean` | `shared_trunk_two_token` | identical | 1.00 | 1.00 | 1.00 | 1.00 | signal survives symmetry-controlled init |
| `A_clean` | `shared_attention_separate_expert` | random | 1.00 | 0.95 | 0.95 | 0.95 | mostly learned; one partial seed |
| `A_clean` | `shared_attention_separate_expert` | identical | 1.00 | 1.00 | 1.00 | 1.00 | cleanly learned |
| `B_redundant` | `shared_trunk_two_token` | both | 1.00 | 1.00 | 1.00 | 1.00 | learnable but redundant with $Y_1$ |
| `C_noisy` | `shared_trunk_two_token` | both | 1.00 | 0.066 | 0.75/1.00 | NA | head-2 remains noise-level |
| `C_noisy` | `shared_attention_separate_expert` | both | 1.00 | 0.074 | 0.55/1.00 | NA | probe can be high even when $Y_2$ is useless |

Chance levels: branch chance is `0.25`; `C_noisy` head-2 chance is about $1/16=0.0625$.

Interpretation: the decisive contrast is not branch probe alone. The decisive contrast is that `A_clean` passes head-2 and swap, while `C_noisy` stays at chance-level head-2 accuracy.

## Gradient Evidence

All-position A/B shared-trunk gradients show strong negative $c_s$ in embedding and shared attention:

| Regime | Condition | Init | embedding $c_s$ | attention $c_s$ | MLP $c_s$ | Interpretation |
| --- | --- | --- | ---: | ---: | ---: | --- |
| `A_clean` | shared trunk | random | -0.943 | -0.943 | 0.091 | strong shared embedding/attention conflict |
| `A_clean` | shared trunk | identical | -0.938 | -0.946 | -0.125 | strong shared embedding/attention conflict |
| `B_redundant` | shared trunk | random | -0.945 | -0.949 | 0.239 | conflict also appears for redundant target |
| `C_noisy` | shared trunk | random | 0.002 | -0.064 | -0.028 | noisy target does not create the same strong conflict |

Interpretation: local gradient conflict exists, especially in embedding and shared attention. However, in the all-position run $Y_1$ accuracy remains `1.00`; therefore the supported claim is gradient conflict without observed $L_1$ performance damage.

## Hypothesis Status

| Hypothesis | Status | Reason |
| --- | --- | --- |
| H1 useful branch signal | supported under all-position control | `A_clean` shared trunk reaches head2/swap/probe `1.00`; `C_noisy` head2 stays near chance |
| H2 redundancy control | supported | `B_redundant` is easy, but NTP already has branch probe `1.00` because $Y_1$ is branch-specific |
| H3 shared-trunk interference | partially supported / refined | strong negative shared gradients exist, but $L_1$ accuracy does not degrade |
| H4 expert localization | not needed as rescue in all-position shared trunk | shared trunk already solves `A_clean`; separate expert remains a diagnostic, not a better method claim |
| H5 diagnostic validity | supported | `C_noisy` head2 stays chance while branch probe can be high, so probe-only judgment is invalid |

## Claim Boundary

Can claim:

- In this controlled K=2 construction, $L_2$ can carry useful branch-specific long-horizon supervision when $I(B;Y_2\mid Y_1)>0$.
- This useful-signal conclusion survives both `decision_only` and `all_positions_lm_control`, though the optimization behavior differs.
- Branch probe must be guarded by head-2 accuracy and branch-swap behavior.
- Shared-gradient conflict can exist without observed $L_1$ performance damage.

Cannot claim:

- MTP universally improves NTP.
- K>2 follows automatically.
- natural-language long-horizon reasoning improves.
- separate experts are generally better.
- gradient conflict alone proves harmful interference.

## Next Decision

The next decision is not to jump directly to a broad next-$K$ claim. The minimal next decision is whether the K=2 mechanism can be lifted to a falsifiable K-scaling statement:

Does a target at horizon $j>1$ improve recovery of a branch variable that is invisible or redundant at earlier horizons, and does the benefit persist under all-position training as $j$ increases?

The next protocol should use K=3 first, not a broad K sweep. It should define one first-informative horizon, keep all earlier targets shared or redundant, and test whether adding the informative horizon changes head accuracy, branch-swap behavior, branch probe, and shared-gradient conflict.

## Source Artifacts

- Code workspace: `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments`
- Runner: `active/synthetic_data_understanding/scripts/run_a11_02_two_token_shared_trunk_signal_interference.py`
- Config: `active/synthetic_data_understanding/configs/a11_02_two_token_shared_trunk_signal_interference.json`
- Decision-only result dir: `active/synthetic_data_understanding/results/a11_02_two_token_shared_trunk_signal_interference/a11_02_decision_only_local2gpu_20260707_0411`
- All-position result dir: `active/synthetic_data_understanding/results/a11_02_two_token_shared_trunk_signal_interference/a11_02_all_positions_lm_control_local2_20260707_0815`
- Curated tables: `Projects/from-attention-to-search/main/experiments/A11/A11_02_two_token_shared_trunk_signal_interference/tables/`
- Remote ACP job `pt-3qu9lxh9` was submitted with `spot` quota and remained in `STARTING`; reserved-quota submit scripts are now fixed for future runs.
