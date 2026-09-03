# A16_00_02 Multistage Gradient-Pathway Audit


## 1. Problem Definition

This subanchor inherits A16_00's question of whether differentiable load control imposes a language-learning cost. It asks one narrower question: **across registered early, middle, and late states, does running-centering reduce load-control interference in the Router input path and Gate update, reduce incompatible language-model updates among documents co-routed to the same expert, and reduce the immediate held-out NLL cost of the LB component?**

The three objects are distinct. Router-path conflict is the cosine between LM and coefficient-scaled LB gradients on the actual upstream Router representation and Gate weights. Expert conflict is opposition among LM gradients induced by independently labeled WoS document groups inside the same expert; expert parameters have no direct LB gradient. Outcome cost is the difference between exact-state LM+LB and LM-only AdamW shadow steps on untouched text.

## 2. Physical Priors

1. A large token-shared component can make load control spend update magnitude correcting a common Router direction rather than preserving task descent; centering removes that component before the Gate.
2. Routing changes which document gradients meet inside each expert, so centering can change expert-update compatibility without a direct LB-to-expert derivative.
3. Reduced raw conflict is useful only if it reduces held-out shadow-step cost; otherwise it may be harmless geometry or beneficial regularization.

## 3. Falsifiable Hypotheses

- **H1, centered mediation:** relative to Vanilla at matched seed and checkpoint, Centered has less-negative LM/LB cosine on Router-source and Gate gradients, lower negative cosine mass among WoS expert-update groups, and a smaller LB-induced held-out NLL penalty.
- **Strongest rival, assignment-only or useful regularization:** centering changes loads and gradient geometry, but the LB shadow step is not more harmful in Vanilla, or expert conflict does not fall.
- **Control-mismatch rival:** the LB component does not improve hard load in the affected state, so any quality cost is ineffective interference rather than a balance--quality trade-off.

The outcome claim passes only if both seeds support a positive Centered mediation effect on the registered shadow-step metric. The shared-path and expert-conflict mechanisms receive separate typed verdicts. Invalid checkpoint pairing, incomplete optimizer reconstruction, non-identical batches, or missing Router/expert gradients is Insufficient.

## 4. Mathematical Model

For stage $t$, condition $a\in\{V,C\}$, and registered shared object $q$ (Router source or Gate), define

$$
c^{a}_{q,t}=\frac{\langle g^{a}_{LM,q,t},g^{a}_{LB,q,t}\rangle}
{\|g^{a}_{LM,q,t}\|\|g^{a}_{LB,q,t}\|+\epsilon}.
$$

Higher values mean less opposition but cannot prove better learning. For expert $e$ and WoS group $d$, let $g^{a}_{e,d,t}$ be the LM gradient on all sparse-expert parameters receiving tokens from that group. The negative cosine mass is

$$
I^{a}_{expert,t}=\mathbb E_{e,d\ne d'}
\left[\max\left(0,-\cos(g^{a}_{e,d,t},g^{a}_{e,d',t})\right)\right],
$$

weighted only over pairs with registered minimum routed-token support. Lower values mean fewer opposed expert updates. The primary outcome at one stage is

$$
\Delta NLL^{a}_{LB,t}=NLL_{WoS}\!\left(T(s^a_t,g_{LM}+g_{LB})\right)
-NLL_{WoS}\!\left(T(s^a_t,g_{LM})\right),
$$

and the Centered mediation effect is $M_t=\Delta NLL^{V}_{LB,t}-\Delta NLL^{C}_{LB,t}$. Positive $M_t$ favors the hypothesis.

## 5. Computational Realization

Use paired Vanilla-Full and Centered-Full four-layer DCLM checkpoints for seeds 17 and 29 at 50M, 6B, and 10B nominal tokens. The exact next DCLM global optimizer batch reconstructs the LM/LB shared-path gradients and AdamW shadow branches. A deterministic, domain-stratified WoS train subset measures expert-update conflict; an independent WoS validation subset measures shadow-step NLL. The WoS test split remains untouched.

Capture the pre-center Router source tensor at each layer and the Gate weight gradient. For experts, compute LM gradients by registered WoS domain shards and compare only expert/group cells with enough assigned tokens. Verify the direct LB gradient on expert parameters is numerically zero; a nonzero value is an implementation failure, not a finding.

## 6. Minimal Falsification Tests

The decisive outcome is the two-seed Centered mediation effect aggregated by a frozen median over the three registered stages, with paired WoS-document bootstrap intervals. Each seed must have positive point direction in at least two of three stages and a positive aggregate lower bound. Shared-path support additionally requires higher Centered LM/LB cosine for both Router-source and Gate groups in at least two stages per seed. Expert support requires lower Centered negative cosine mass in at least two stages per seed.

Known-good tests use constructed aligned/opposed objectives; known-bad tests use zero LB coefficient, shuffled LB gradients, and deliberately unpaired batches. Hard guards cover checkpoint/optimizer identity, batch hash, exact branch replay, WoS split/hash, gradient reconstruction, and no direct expert LB gradient.

## 7. Current Evidence

The complete 12-cell audit returned `fail_global_centering_mediation_with_early_stage_relief`. At 50M, Vanilla's effective LB shadow step raised WoS NLL by 0.000845/0.000617 nat/token, while Centered was indistinguishable from zero; the Centered mediation was +0.000839/+0.000630 with both paired intervals above zero. The effect was not stage-invariant: at 6B both mediation point estimates were negative, and at 10B only seed 29 had a positive interval. Seed 17's frozen three-stage median interval crossed zero, while seed 29 passed, so the two-seed outcome rule failed.

The shared-path and expert-conflict clauses also failed. Centering made Router-source and Gate gradients less opposed only at 50M; the gains were negative at 6B/10B. Centered did not lower token-weighted within-expert negative-cosine mass. Vanilla's near-zero mass coexisted with collapsed routing and is not evidence of healthier specialization. [Result record](/Projects/from-attention-to-search/main/experiments/A16/A16_00_02_E01_multistage_gradient_pathway_audit/summary.md).

An implementation audit established that the source 30B runs recorded $\lambda_{LB}=0.01$ but did not apply an effective LB gradient because re-entrant activation checkpointing detached the nested auxiliary tensor. A16 therefore measures a qualified counterfactual differentiable shadow step at frozen states, not the original trajectory effect.

## 8. Claim Boundary And Next Decision

This audit establishes a reproducible early-state relation between centering and lower immediate LB cost, but rejects a global multistage lower-interference explanation. It cannot prove that one-step effects explain the 30B trajectory, that lower measured expert conflict is healthier, or that dynamic expert bias is superior.

The single next decision is to compare Centered with dynamic expert bias, truly differentiable LB, and no added load controller. Completion requires matched hard-load and held-out NLL/FLOP evidence that separates non-gradient control from differentiable regularization.
