# 11_02 Two-Token Shared-Trunk Signal / Interference Anchor

Status: canonical anchor, `decision_only` and `all_positions_lm_control` evidence completed locally.  
Parent line: `11_long_horizon_mtp_objective`.  
Prior evidence: `11_01_k2_branch_delayed_next_two_anchor.md` supports the clean K=2 objective-level separation.  
Source design document: `daily_research_reports/0707/mtp_k2/two_token_shared_trunk_theory_experiment_design.md`.

## 0. Thinking Card

**Phenomenon:** The clean K=2 result shows that when $Y_1$ is shared and $Y_2$ is branch-specific, next-two loss $L_2$ can supply branch-relevant supervision that next-one loss $L_1$ lacks. This does not yet say whether $L_2$ is useful, redundant, noisy, or interfering in a shared-trunk Transformer.

**Mechanism guess:** The effect of $L_2$ depends on three layers: whether $Y_2$ contains branch information beyond $Y_1$; whether $g_2=\nabla_{\theta_s}L_2$ improves branch recoverability from hidden states; and whether $g_2$ conflicts with $g_1=\nabla_{\theta_s}L_1$ on shared trunk parameters.

**Key variables:** branch key $B$; hidden states at multiple positions; target relation between $Y_1$ and $Y_2$; shared trunk parameters $\theta_s$; gradient pair $(g_1,g_2)$; parameter groups: embedding, shared attention, shared MLP, expert_1, expert_2, head_1, head_2.

**Causal relation:** If $I(B;Y_2\mid Y_1)>0$, $g_2$ improves branch recoverability, and $g_2$ is not destructively opposed to $g_1$ on critical shared parameters, then $L_2$ is useful branch signal. If $Y_2$ adds no branch information, or if $g_2$ strongly conflicts with $g_1$ in the shared trunk, then $L_2$ may be redundant, noisy, or useful-but-interfering.

**Observable metric:** The primary decision object is `two_token_signal_class`, classified from data-regime contrast, branch representation gain, and shared-gradient compatibility. The first primary scalar is `A_vs_C_branch_probe_gain_at_prediction_site`. The `decision_only` result shows this scalar must be guarded by `single_prefix_head2_accuracy` and `branch_swap_preference`; branch probe alone is not sufficient.

**Rival explanations:** $L_2$ success may come from local predictability rather than branch information; Regime C may leak branch identity or be memorized; probe improvement may not correspond to usable head-2 prediction; head-2 success may hurt $L_1$; separate experts may help only through extra parameters rather than reduced horizon interference.

**Decision:** `decision_only` classifies $L_2$ as branch-specific useful signal with shared-trunk acquisition instability. `all_positions_lm_control` preserves the useful-signal conclusion and solves A-clean in the shared trunk, while still showing shared-gradient conflict. The next decision is to formulate the smallest K-scaling test, starting with K=3, rather than a broad next-$K$ sweep.

## 1. Problem Definition

**Parent problem:** Build a rigorous link between long-horizon dependencies and multi-token prediction. A11_01 already answered whether there exists a clean K=2 construction where $L_2$ supplies branch signal that $L_1$ lacks.

**Sharper subproblem:** In a minimal K=2 shared-trunk Transformer, determine whether second-token loss $L_2$ is useful branch signal, redundant signal, noisy target, or useful-but-interfering gradient source under different target-information regimes.

**Decision question:** In a K=2 one-layer causal Transformer, does branch-relevant $L_2$ become a usable shared-trunk representation without harming $L_1$ learning? If it does harm $L_1$, does shared-attention separate-expert structure localize and reduce the interference?

**Not in scope:** Re-proving A11_01 objective-level separation; curriculum; K>2; MoE routing complexity; real LLM long-range reasoning; natural-language transfer; proving that MTP universally outperforms NTP.

**Terminology / Definitions:**

| Term | Plain meaning | Concrete object or computation | Unit / formula | Why it matters | What it cannot prove |
|---|---|---|---|---|---|
| multi-token prediction | A prefix state predicts more than one future token | here $h_T\to Y_1,Y_2$ | objective family | parent object of the advisor question | universal improvement |
| next-token prediction | A prefix state predicts only the immediate next token | here $h_T\to Y_1$ | objective family | baseline | inability to learn long horizon |
| shared trunk | Causal representation path shared by horizon losses | embedding + shared attention + shared MLP, or a subset | parameter set | $L_1,L_2$ can cooperate or conflict here | all model structures |
| Regime A-clean | $Y_1$ shared and $Y_2$ branch-specific | $Y_1=U,\;Y_2=S_B$ | data regime | tests useful branch signal | absence of shared-trunk interference |
| Regime B-redundant | $Y_2$ adds no branch information after $Y_1$ is known | unique tokens $S_b,T_b$ with $Y_1=S_B,\;Y_2=R(S_B)=T_B$ | data regime | tests whether $L_2$ is redundant with $L_1$ | zero optimization effect |
| Regime C-noisy | $Y_2$ is branch-independent irreducible noise | $Y_2=Z,\;Z\perp B$, $Z$ sampled iid per occurrence from a fixed noise-token distribution | data regime | noisy control | all noise forms |
| branch recoverability | Whether branch label is readable from a hidden state | frozen linear probe $h\to B$ | accuracy / CE | checks branch retention | native head usability |
| branch-swap preference | Whether prediction changes when only early branch token changes | `BR_b -> BR_c` should prefer $S_c$ | rate / logit margin | causal guard | all memorization routes |
| gradient compatibility | Whether $L_1,L_2$ cooperate in a parameter group | $c_s,r,\rho$ | scalar | decides whether useful signal harms shared training | long-term training result alone |
| branch init mode | How branch-token embeddings start | normal random init or identical branch-token init | condition label | separates realistic behavior from symmetry-controlled mechanism | robustness across all architectures |
| objective scope | Which positions produce training loss | `decision_only` or `all_positions_lm_control` | condition label | separates the clean theory object from LM-style background supervision | K>2 or natural language |
| loss site | Where training losses are computed in `decision_only` | final prefix state `prediction_site` only | position | tests the theory object $h_T\to(Y_1,Y_2)$ directly | standard LM loss over every token |
| parameter unification | Holding all non-target factors fixed | same data size, seeds, architecture config, optimizer, steps, loss weights, probe config, and evaluation split within a comparison | implementation contract | prevents ablations from changing several causes at once | all hidden implementation effects |
| fully separated control | No shared representation path between horizons | independent horizon-1 and horizon-2 trunks | model condition | upper-bound for removing shared interference | fair capacity-matched method comparison |
| two_token_signal_class | Anchor-level classification | useful / redundant / noisy / useful-but-interfering / attention-bottleneck / invalid | categorical | summarizes the experiment decision | theorem proof |

## 2. Physical Priors

**P1: Data-information prior.**  
$L_2$ has a principled reason to improve long-horizon branch representation only when $Y_2$ contains branch information beyond $Y_1$:

$$
I(B;Y_2\mid Y_1)>0.
$$

Could be wrong if data construction leaks branch through local context, or if Regime B/C is not clean.

**P2: Representation-usefulness prior.**  
Branch information in $Y_2$ does not guarantee that the model uses it. $L_2$ is useful representation signal only if its learning direction reduces branch-probe loss:

$$
\langle \nabla_{\theta_s}R_\phi,g_2\rangle>0,
$$

where $R_\phi=\operatorname{CE}(S_\phi(h),B)$ is branch-probe loss.

Could be wrong if the probe is unreliable, the split is too small, or branch information is nonlinear while only a linear probe is used.

**P3: Shared-gradient compatibility prior.**  
Useful $L_2$ may still hurt $L_1$ because both losses update shared trunk parameters:

$$
c_s=\frac{\langle g_1,g_2\rangle}{\|g_1\|\|g_2\|},\qquad
\rho=\frac{\langle g_1+\lambda g_2,g_1\rangle}{\|g_1\|^2}.
$$

Could be wrong if short-run gradient conflict does not predict training degradation, or if conflict is dominated by harmless head parameters.

## 3. Falsifiable Hypotheses

**H1: Useful branch-signal hypothesis.**  
In Regime A-clean, shared-trunk two-token should beat the NTP baseline on `branch_probe_accuracy_prediction_site`, `single_prefix_head2_accuracy`, and `branch_swap_preference`. Regime C-noisy should not show the same gains.

Supported if: `A_vs_C_branch_probe_gain_at_prediction_site > 0`, A-clean has high head2/swap, and C-noisy stays near chance.  
Weakened if: A-clean and C-noisy behave similarly, or C-noisy also produces branch gain.

**H2: Redundancy hypothesis.**  
In Regime B-redundant, $Y_2$ should not provide strong branch representation gain beyond what $Y_1$ already provides. Head-2 can be accurate, but branch gain should be explained by $Y_1$ or local predictability.

Supported if: B branch gain is lower than A, or B gains are already present in NTP through $Y_1$.  
Weakened if: B matches A without a clear $Y_1$ explanation, meaning Regime B is not a clean redundancy control or $L_2$ has an unexpected optimization effect.

**H3: Shared-trunk acquisition-interference hypothesis.**  
In Regime A-clean, $L_2$ may be branch-useful but fail to be acquired reliably through shared parameters. The failure can appear either as $L_1$ degradation or as persistent partial $Y_2$ branch learning while $L_1$ is already solved. This should coincide with negative $c_s$ or low $\rho$ in shared attention, shared MLP, or embedding.

Supported if: branch metrics are unstable or partial across seeds while critical shared groups show $c_s<0$ or $\rho<1$.  
Weakened if: branch metrics are stable and high without $L_1$ degradation and without destructive shared-gradient evidence.

**H4: Expert-separation localization hypothesis.**  
H4 is not the first test of whether next-two causes shared-trunk gradient interference. That is H3. H4 asks whether, once interference exists, separating horizon-specific expert/MLP paths reduces the harmful part while keeping the useful branch signal.

Supported if: `shared_attention_separate_expert` improves or preserves `L1_structured_loss` relative to `shared_trunk_two_token` while keeping `single_prefix_head2_accuracy` and branch probe.  
Weakened if: separate-expert has the same $L_1$ degradation as shared-trunk two-token and conflict remains in shared attention or embeddings.

**H5: Diagnostic validity hypothesis.**  
Regime C-noisy should be diagnosed as useless/noisy primarily by head-2 behavior: head-2 accuracy should remain near noise chance, and no branch-swap preference should be defined. Branch probe is a representation diagnostic, not a sufficient validity test.

Supported if: C-noisy head-2 remains near chance and cannot pass swap.  
Weakened if: C-noisy head-2 learns branch-specific targets, which would imply leakage, memorization, or invalid data construction.

## 4. Mathematical Model

### 4.1 Sequence regimes

Let:

$$
B\sim\operatorname{Unif}\{1,\ldots,M\},\qquad
h_T=f_{\theta_s}(X_{\le T}).
$$

All regimes share:

$$
X_{\le T}=(\operatorname{BR}_B,F_1,\ldots,F_L,U_1,\ldots,U_s).
$$

**Regime A-clean: useful second-token branch signal**

$$
Y_1=U,\qquad Y_2=S_B,\qquad I(B;Y_2\mid Y_1)=H(B).
$$

**Regime B-redundant: second token adds little branch information beyond $Y_1$**

$$
Y_1=S_B,\qquad Y_2=R(S_B)=T_B,\qquad R(S_b)=T_b,\qquad I(B;Y_2\mid Y_1)=0.
$$

Implementation rule: create two branch-indexed token sets $\{S_b\}_{b=1}^M$ and $\{T_b\}_{b=1}^M$, and set

$$
R(S_b)=T_b.
$$

Thus $Y_2$ may be branch-specific marginally, but it is deterministic once $Y_1$ is known. This makes Regime B a redundancy control, not a noisy control.

**Regime C-noisy: second token is branch-independent**

$$
Y_1=U,\qquad Y_2=Z,\qquad Z\sim P_Z,\qquad Z\perp B.
$$

Implementation rule: sample $Z$ iid per occurrence from a fixed noise-token distribution $P_Z$, independent of $B$, the prefix, and the seed-specific branch table. Train and evaluation both use the same $P_Z$ but independent draws. Do not use a fixed branch-to-noise or prefix-to-noise table, because that would make memorization possible.

### 4.2 Objectives

NTP baseline:

$$
L_{\mathrm{NTP}}=L_1=\operatorname{CE}(p^{(1)}_\theta(Y_1\mid h_T),Y_1).
$$

Shared-trunk two-token:

$$
L_{\mathrm{2tok}}=L_1+\lambda L_2
=\operatorname{CE}(p^{(1)}_\theta(Y_1\mid h_T),Y_1)
+\lambda\operatorname{CE}(p^{(2)}_\theta(Y_2\mid h_T),Y_2).
$$

Shared-attention separate-expert:

$$
a_T=f_{\theta_{\mathrm{attn}}}(X_{\le T}),
$$

$$
h_T^{(1)}=e_1(a_T),\qquad h_T^{(2)}=e_2(a_T),
$$

$$
L_{\mathrm{sep}}=
\operatorname{CE}(p^{(1)}_\theta(Y_1\mid h_T^{(1)}),Y_1)
+\lambda\operatorname{CE}(p^{(2)}_\theta(Y_2\mid h_T^{(2)}),Y_2).
$$

### 4.2.1 Loss sites and optimization targets

The first implementation is not a full language-modeling objective over every token. For each example, losses are computed only at the final prefix representation, `prediction_site`, immediately before $Y_1$.

For the NTP baseline:

$$
L_{\mathrm{active}}=L_1.
$$

No $L_2$ gradient is used. If a second head exists for code symmetry, its weight is zero and it is not part of the optimization objective.

For shared-trunk two-token:

$$
L_{\mathrm{active}}=L_1+\lambda L_2.
$$

Both heads read the same hidden state $h_T$. The gradients from $L_1$ and $L_2$ both update embedding, shared attention, and shared MLP parameters; each loss also updates its own head.

For shared-attention separate-expert:

$$
L_{\mathrm{active}}=L_1+\lambda L_2.
$$

$L_1$ updates embedding, shared attention, expert_1, and head_1. $L_2$ updates embedding, shared attention, expert_2, and head_2. Therefore this condition separates MLP/expert paths but still allows interference in embedding and shared attention.

Branch-probe losses and gradient-profiling losses are diagnostic only. They must not update the main model.

Optional all-position control:

$$
L_{\mathrm{allpos}}^{(1)}=\frac{1}{|\mathcal P_1|}\sum_{t\in\mathcal P_1}
\operatorname{CE}(p^{(1)}(x_{t+1}\mid h_t),x_{t+1}),
$$

$$
L_{\mathrm{allpos}}^{(2)}=\frac{1}{|\mathcal P_2|}\sum_{t\in\mathcal P_2}
\operatorname{CE}(p^{(2)}(x_{t+2}\mid h_t),x_{t+2}).
$$

This control tests whether the decision-site conclusion survives ordinary LM-style background losses. It changes the objective scope, so it is a robustness check, not the primary evidence for the clean theorem.

### 4.3 Gradient diagnostics

For each parameter group $G$:

$$
g_1^G=\nabla_G L_1,\qquad g_2^G=\nabla_G L_2.
$$

$$
c_s(G)=\frac{\langle g_1^G,g_2^G\rangle}{\|g_1^G\|\|g_2^G\|},
$$

$$
r(G)=\frac{\|g_2^G\|}{\|g_1^G\|},
$$

$$
\rho(G)=\frac{\langle g_1^G+\lambda g_2^G,g_1^G\rangle}{\|g_1^G\|^2}.
$$

Interpretation:

- $c_s(G)<0$ means local gradient conflict.
- $r(G)\gg 1$ means second-token gradient may dominate the update.
- $\rho(G)<1$ means $L_2$ weakens the $L_1$ update direction; $\rho(G)<0$ means it reverses it.

### 4.4 Primary decision object

Define:

$$
\Delta_{\mathrm{probe}}(R,C)
=\operatorname{ProbeAcc}_{R,C}^{\mathrm{2tok}}-\operatorname{ProbeAcc}_{R,C}^{\mathrm{NTP}},
$$

where $R$ is regime and $C$ is hidden-state position.

The first primary scalar is:

$$
\operatorname{A\_vs\_C\_branch\_probe\_gain}
=\Delta_{\mathrm{probe}}(\mathrm{A},\mathrm{prediction\_site})
-\Delta_{\mathrm{probe}}(\mathrm{C},\mathrm{prediction\_site}).
$$

The final categorical result is `two_token_signal_class`:

| Class | Meaning |
|---|---|
| useful | A-clean improves branch metrics; C-noisy does not; no material $L_1$ harm |
| useful-but-acquisition-unstable | A-clean carries real $L_2$ branch signal, but shared-trunk branch acquisition is seed-unstable or partial while $L_1$ is solved |
| useful-but-interfering | A-clean improves branch metrics but harms $L_1$ with negative shared-gradient evidence |
| redundant | B-redundant accounts for gains through $Y_1$ or local predictability |
| noisy | C-noisy produces no branch gain and may show unstable / high-norm $g_2$ |
| attention-bottleneck | separate-expert does not help and conflict remains in shared attention / embedding |
| invalid | C-noisy or branch-swap reveals leakage or memorization |

## 5. Computational Realization

**Experiment role:** root-cause / metric audit for two-token shared-trunk dynamics after A11_01 closed the clean objective-level separation.

**Code boundary:** create a new A11_02 runner; do not overwrite A11_01.

Expected paths:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a11_02_two_token_shared_trunk_signal_interference.py
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a11_02_two_token_shared_trunk_signal_interference.json
Projects/from-attention-to-search/main/experiments/A11/A11_02_two_token_shared_trunk_signal_interference/
```

**Data variables to review before protocol approval:**

| Variable | Proposed value / rule | Why it matters |
|---|---|---|
| `num_branches` | first run 4 | chance baseline 0.25 while still cheap |
| `filler_length` | first run 16 | tests branch retention across a nontrivial delay |
| `shared_context_length` | 4 | enforces ambiguous local context |
| objective scope | primary `decision_only`; optional `all_positions_lm_control` | separates theory-test evidence from LM-style robustness |
| Regime A-clean | $Y_1=U,\;Y_2=S_B$ | useful branch signal |
| Regime B-redundant | $Y_1=S_B,\;Y_2=R(S_B)=T_B$ with $R(S_b)=T_b$ | $Y_2$ adds no branch information beyond $Y_1$ |
| Regime C-noisy | $Y_1=U,\;Y_2=Z$, $Z\sim P_Z$ iid per occurrence and $Z\perp B$ | noisy control without fixed memorization table |
| branch init | normal random init plus identical branch-token init | separates realistic behavior from symmetry-controlled objective pressure |
| train/eval split | required for all metrics | prevents memorization and probe overfit |

All comparisons must obey parameter unification: for a given comparison, only the named factor may change. The fixed parameters include number of branches, filler length, shared context length, vocabulary construction rule, model depth/width/head count, optimizer, learning rate, weight decay, training steps, $\lambda$, probe settings, profiling interval, seeds, and evaluation split. If `all_positions_lm_control` is run, losses must be averaged over active positions before applying horizon weights so that loss scale is not a hidden confound.

**Model conditions:**

| Condition | Required first protocol | Purpose |
|---|---|---|
| `ntp_baseline` | yes | true one-head $L_1$ baseline |
| `shared_trunk_two_token` | yes | ordinary two-token shared-trunk interaction |
| `shared_attention_separate_expert` | yes | localize MLP/expert interference |
| `fully_separated_control` | no, park | independent horizon-1 and horizon-2 trunks; upper-bound only; add after first failure if needed |

**Representation probe positions:**

| Position name | Concrete position |
|---|---|
| `after_branch_token` | immediately after `BR_b` |
| `middle_filler` | halfway through filler |
| `shared_local_context` | after shared context but before prediction endpoint |
| `prediction_site` | prefix endpoint before $Y_1$ |

**Gradient parameter groups:**

```text
embedding
shared_attention
shared_mlp
expert_1
expert_2
head_1
head_2
```

## 6. Minimal Falsification Tests

| Test | Question | Comparison | Primary metric | Pass | Fail | Failure meaning |
|---|---|---|---|---|---|---|
| Data-regime specificity | Is $L_2$ useful only when $Y_2$ carries branch information? | A-clean vs C-noisy | `A_vs_C_branch_probe_gain_at_prediction_site` | A improves, C does not | A and C same | branch usefulness not established or leakage |
| Redundancy control | Does $Y_2$ add branch information beyond $Y_1$? | B-redundant vs A-clean | B branch gain lower than A or explained by $Y_1$ | B behaves like redundant control | B equals A without explanation | Regime B not clean or hidden extra effect |
| Interference audit | Does useful $L_2$ harm $L_1$? | shared-trunk two-token vs NTP in A-clean | `L1_structured_loss_delta`, $c_s$, $\rho$ | branch gain with no harm, or classified useful-but-interfering | unexplained harm or no branch gain | shared-trunk interaction unresolved |
| Expert localization | Does separate expert reduce MLP/expert conflict? | separate-expert vs shared-trunk two-token | $L_1$ preservation + branch metric retention | separate-expert preserves $L_1$ and branch metrics | no improvement; attention conflict persists | bottleneck likely attention / embedding |
| Diagnostic validity | Does noisy control stay noisy? | C-noisy behavior | head2/probe/swap near chance | C remains chance | C branch gain high | leakage, memorization, or invalid metric |
| Objective-scope robustness | Does the conclusion survive LM-style background loss? | `decision_only` vs `all_positions_lm_control` | same primary metrics at `prediction_site` | same qualitative class | class changes | claim must be restricted to decision-site objective |

## 7. Current Evidence

**A11_01 baseline evidence:** Clean A-style K=2 with tied branch initialization supports the objective-level mechanism. Fixed-next-one solved $A$ but stayed branch-blind; next-two predicted $S_B$ and passed prediction-site probe/swap.

**A11_02 `decision_only` evidence:** The first full A11_02 implementation ran A/B/C regimes, three model conditions, two branch-init modes, and five seeds. Main result: `two_token_signal_class = useful branch signal with shared-trunk acquisition instability`.

Key measured facts:

| Observation | Evidence | Meaning |
|---|---|---|
| `A_vs_C_branch_probe_gain_at_prediction_site` is positive | `0.25` for identical branch init; `0.50` for random init | A-clean has branch signal beyond noisy auxiliary loss |
| A-clean shared trunk is unstable | head-2/probe/swap mean `0.65` in identical init and `0.90` in random init | $L_2$ signal is useful but not reliably acquired |
| 12000-step completion does not fix failures | identical seeds 973/975 remain `0.25`; random seed 973 remains `0.50` | not merely a 4000-step budget artifact |
| A-clean $L_1$ is solved | $Y_1$ accuracy `1.00`; $L_1$ near zero | no evidence that $L_2$ harms $L_1$ here |
| separate expert fixes the constrained A-clean case | identical init mean head-2/probe/swap moves from `0.65` to `1.00` | MLP/expert sharing is a plausible bottleneck |
| C-noisy head-2 stays chance | head-2 around `0.066-0.071`, chance about `0.0625` | noisy target is not learned |
| C-noisy probe can be high | separate-expert probe reaches `0.80/0.95` while head-2 stays chance | branch probe alone is not a valid decision metric |
| all-position A-clean shared trunk solves the target | head-2, branch probe, and swap all reach `1.00` in both init modes | useful $L_2$ signal survives LM-style background loss |
| all-position C-noisy remains chance-level for head-2 | head-2 is about `0.066/0.074`, near $1/16$ chance | noisy control still falsifies arbitrary auxiliary-signal explanations |
| all-position shared gradients remain conflicting | A/B embedding and shared-attention $c_s\approx -0.94$ | gradient conflict exists, but it does not imply observed $L_1$ damage |

Evidence links:

- `Projects/from-attention-to-search/main/experiments/A11/A11_02_two_token_shared_trunk_signal_interference/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_02_two_token_shared_trunk_signal_interference/detailed.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_02_two_token_shared_trunk_signal_interference/tables/`
- `Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_01_k2_branch_delayed_next_two_anchor.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_01_k2_branch_delayed_next_two/summary.md`
- `daily_research_reports/0707/mtp_k2/two_token_shared_trunk_theory_experiment_design.md`

## 8. Claim Boundary And Next Decision

**Can claim now:** A11_01 supports the clean K=2 objective-level mechanism. A11_02 adds that, in the controlled shared-trunk Transformer, $L_2$ is branch-specific useful signal in A-clean under both `decision_only` and `all_positions_lm_control`. Decision-only shared-trunk acquisition can be unstable; all-position shared trunk solves A-clean while preserving the noisy-control contrast. Branch probe alone is not a valid decision metric; head-2 accuracy and branch-swap behavior are required guards.

**Cannot claim now:** MTP universally improves NTP; K>2 or curriculum behavior follows automatically; natural-language long-horizon reasoning improves; expert separation is generally useful; gradient conflict alone proves harmful interference.

**Next decision:** Define the smallest K-scaling anchor and protocol. Start with K=3 and one first-informative horizon: earlier targets are shared or redundant, while a later target is branch-specific. The first falsifier is whether the informative farther-horizon loss improves head prediction, branch-swap behavior, and branch recovery beyond NTP and shorter-horizon controls under all-position training.
