# Summary: A11_02b Advisor K=2 Design Completion Audit

Status: completed by remote 4-GPU full run on 2026-07-10. Final ACP job: `pt-27zjtage` (`SUCCEEDED`).

## What Was Established

The advisor's K=2 diagnostic design is now operationally complete in the controlled one-layer synthetic setting. The result strengthens the useful-signal claim and narrows the interference claim:

1. In `A_clean`, where $Y_1$ is shared and $Y_2=S_B$ identifies the early branch $B$, all-position shared-trunk K=2 training reaches head-2 accuracy, branch probe, and branch-swap consistency of `1.00`. In `C_noisy`, head-2 accuracy is `0.0656`, near the $1/16=0.0625$ noise chance level, even though the branch probe is `0.875`. K=2 therefore supplies usable branch supervision in `A_clean`; probe readability alone remains insufficient evidence.
2. The final second-token gradient is branch-directed in `A_clean`: $U_2>0$ in `10/10` matched runs and its cosine with the frozen-readout gradient is `0.983`. Redundant and noisy controls have mean cosines `-0.047` and `-0.028`. This is directional, first-order evidence, not a long-run optimization theorem.
3. Negative shared embedding/attention cosine is not an initialization fact. At step 0, mean $c_s$ is `0.016/0.004`; at step 200 it is `-0.889/-0.894`, after structured $L_1$ has already fallen near zero. Increasing $lambda$ from `0.25` to `1.0` raises normalized all-position $L_1$ area by `0.59%`, `0.83%`, and `1.07%` versus NTP, while final $Y_1$ accuracy remains `1.00`. Thus the run supports a small dose-dependent local cross-entropy slowdown, not task failure.
4. Expert or full trunk separation removes cross-horizon gradients from the separated parameter groups by construction. It does not provide a stable method advantage: decision-only head-2 means are `0.775` shared, `0.900` separate-expert, and `0.900` fully separated, but paired confidence intervals include zero; all-position shared K=2 already reaches `1.00`.

## Terminology / Definitions

| Term | Plain meaning | Formula / computation | Decision role | Cannot prove |
|---|---|---|---|---|
| `A_clean` | only the second future token identifies branch | $Y_1=U,\;Y_2=S_B$ | useful K=2 signal | natural-language benefit |
| `B_redundant` | the first token already identifies branch | $Y_1=S_B,\;Y_2=T_B$ | zero conditional information control | absence of all optimization effects |
| `C_noisy` | second token is branch-independent noise | $Y_1=U,\;Y_2=N,\;N\perp B$ | noisy-target guard | every kind of noisy supervision |
| head-2 accuracy | model-native prediction of $Y_2$ from $h_T$ | top-1 accuracy of head 2 | whether K=2 learns the target | causal branch use alone |
| branch probe | frozen linear readability of $B$ from $h_T$ | accuracy of $S_\phi(h_T)\to B$ | representation availability | use by the model's own head |
| branch swap | prediction follows an intervened branch token | fraction preferring the swapped branch target | causal shortcut guard | general causal reasoning |
| $U_2$ | whether descending $L_2$ lowers frozen branch-readout loss | $\langle\nabla_{\theta_s}R_\phi,\nabla_{\theta_s}L_2\rangle$ | task-directed gradient evidence | multi-step benefit |
| $c_s$ | horizon-gradient cosine on shared parameters | $\langle g_1,g_2\rangle/(\|g_1\|\|g_2\|)$ | local conflict geometry | realized harm by itself |
| $\rho$ | preservation of the $L_1$ update direction | $\langle g_1+\lambda g_2,g_1\rangle/\|g_1\|^2$ | first-order local $L_1$ progress | final performance |
| normalized $L_1$ AUC | average structured next-token loss over training | $T^{-1}\int_0^T L_1(t)\,dt$ | realized local learning cost | semantic efficiency |

## Setup

- Data regimes: `A_clean`, `B_redundant`, `C_noisy`.
- Models: NTP, shared-trunk K=2, shared-attention/separate-expert K=2, fully separated two-trunk K=2.
- Training scopes: `decision_only` and `all_positions_lm_control`.
- Initializations: random and tied branch embeddings.
- Seeds: `971,972,973,974,975`.
- Primary lambda audit: `A_clean` shared trunk with $\lambda\in\{0.25,0.5,1.0\}$.
- Fixed model: one layer, one attention head, $d=64$, 4000 steps.
- Completion: 240/240 tasks, 120 per training scope, 5/5 seeds for every condition.

## Main Evidence

All-position results aggregate both initialization modes (`n=10` per row):

| Regime / model | $Y_1$ acc | head-2 acc | branch probe | swap | Interpretation |
|---|---:|---:|---:|---:|---|
| A-clean / NTP | 1.000 | NA | 0.825 | NA | indirect readability can occur without head-2 supervision |
| A-clean / shared K=2 | 1.000 | 1.000 | 1.000 | 1.000 | useful second-token signal is natively learned |
| A-clean / separate expert | 1.000 | 0.975 | 0.975 | 0.975 | mostly solved; one partial seed |
| A-clean / fully separated | 1.000 | 1.000 | 1.000 | 1.000 | no-sharing upper bound solves |
| B-redundant / shared K=2 | 1.000 | 1.000 | 1.000 | 1.000 | learnable but adds no conditional branch information |
| C-noisy / shared K=2 | 1.000 | 0.0656 | 0.875 | NA | probe false positive; target remains noise-level |

The decisive result is the joint head-2/probe/swap contrast, not probe alone.

## Central Figure

![A11_02b core signal and interference](figures/a11_02b_core_signal_and_interference.png)

**Question:** Does K=2 provide branch-directed signal, and does its shared-gradient interaction create realized local cost?  
**How to read:** top-left contrasts native branch use with the noisy probe false positive; top-right shows paired $L_1$ AUC cost as $\lambda$ increases; bottom-left shows shared-gradient cosine over time; bottom-right shows final task-directed gradient cosine.  
**Observed:** A-clean passes native and swap guards; the local $L_1$ cost is small but monotonic; negative cosine emerges after the first training interval; only A-clean has a strongly branch-directed final $L_2$ direction.  
**Take-home:** useful semantic direction and local objective conflict coexist.  
**Does not prove:** general MTP efficiency, natural-language benefit, or that negative cosine alone causes harm.

## Hypothesis Status

| Hypothesis | Status | Evidence |
|---|---|---|
| H1 useful signal | supported, strongest under all-position | A-clean head-2/probe/swap `1.00`; C-noisy head-2 `0.0656`; final A-clean $U_2>0$ in `10/10` |
| H2 refinement explains difficulty/conflict | weakened | all-position $D_t$ falls `0.318 -> 1.1e-5`, but bucket effects are not monotonic and A/B have only four distinct branch-level $G_t$ values |
| H3 hidden-to-parameter rotation | insufficient | step-0 $c_h=-0.0058$ and parameter cosines are also near zero; final hidden gradients are only `4e-6/5e-6` |
| H4 harmful interference | supported only as a small local slowdown | all-position $L_1$ AUC cost rises `0.59% -> 1.07%`; final $Y_1$ accuracy remains `1.00` |
| H5 localization by separation | structural part supported; performance benefit insufficient | cross-gradients are zero in separated groups; decision-only mean improves but paired intervals include zero; all-position shared already solves |

## Claim Boundary

Can claim:

- In this controlled K=2 construction, branch-informative $L_2$ provides model-usable branch supervision and a branch-directed gradient after the representation forms.
- Shared embedding/attention gradients become strongly opposed during training and produce a small, dose-dependent slowdown in next-token cross-entropy convergence.
- This slowdown does not reduce final next-token accuracy in the tested setting.
- Probe-only and cosine-only arguments are invalid.

Cannot claim:

- K=2 or MTP is generally more sample-efficient than NTP.
- Negative cosine at initialization explains the result.
- Expert separation is a generally better method.
- Refinement gain explains the observed conflict.
- The result transfers to natural language or deeper models.

## Next Decision

Close the advisor K=2 audit. If the theory line continues, the only unresolved mechanism worth isolating is a finite-step proposition connecting $\lambda$, $\rho(t)$, and integrated $L_1$ cost while separately tracking branch-margin gain. Do not reopen a broad architecture or K sweep from this result.

## Source Artifacts

- Protocol: `protocol.md`
- Detailed evidence: `detailed.md`
- Curated tables: `tables/`
- Final run: `active/synthetic_data_understanding/results/a11_02b_advisor_design_completion_audit/a11_02b_advisor_design_completion_4gpu_20260710_034038`
- Final ACP job: `pt-27zjtage`
