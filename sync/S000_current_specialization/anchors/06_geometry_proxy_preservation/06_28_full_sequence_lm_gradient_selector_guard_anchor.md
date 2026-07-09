# Anchor: A06_28 Full-Sequence LM Gradient Selector Guard

## 0. Thinking Card

**Phenomenon:** A06_27 showed that embedding gradients can select route-relevant states under route-position loss, but that loss may leak the supervised route position.

**Mechanism guess:** if embedding-gradient selection is a real route-state selector, it should still recover feature-relevant states when the gradient is computed from a full next-token LM loss rather than only the route-position loss.

**Key variables:** embedding gradient $g^{emb}_{i,p}$, gradient energy $E^{emb}_{i,p}=\|g^{emb}_{i,p}\|_2^2$, selected top-k positions, selected hidden states $h_{i,p}$, feature NMI, and margin p05.

**Causal relation:** cleaner route-relevant gradient energy should produce a cleaner selected hidden-state pool; cleaner selected states should produce router rows with higher feature NMI and positive margin.

**Observable metric:** immediate feature NMI after router reinitialization, guarded by margin p05, selected route/slot fractions, and slot-start NMI.

**Rival explanations:** the A06_27 success may be route-position loss leakage; full LM loss may be dominated by random neutral-token prediction noise; top-1 selection may be too narrow while top-k may retain signal but also add noise.

**Decision:** the full-LM guard is weakened, not supported. Raw embedding-gradient selection contains feature signal but does not pass stable margin preservation.

## 1. Problem Definition

**Parent problem:** determine whether feature-level router initialization can be discovered without feature labels or manually selected route positions.

**Sharper subproblem:** test whether A06_27's embedding-gradient selector survives when route-only loss is replaced by full-sequence next-token LM loss.

**Terminology / Definitions:**

| Term | Plain meaning | Concrete object or computation | Unit / formula | Why it matters | What it cannot prove |
| --- | --- | --- | --- | --- | --- |
| Full-sequence LM loss | Predict every next token | CE over all next-token positions | $\mathcal L^{full}_i=\sum_p \mathrm{CE}(\ell_{i,p},x_{i,p+1})$ | Removes route-only locality shortcut | Real language transfer |
| Embedding-gradient energy | Token-level sensitivity of the loss to the input embedding | $E^{emb}_{i,p}=\|\nabla_{e_{i,p}}\mathcal L_i\|_2^2$ | squared norm | Candidate selector score | Feature identity |
| Feature NMI | Agreement between feature id and routed expert | NMI(feature, route) | 0 to 1 | Primary separation metric | Utility |
| Margin p05 | Low-tail matched expert score gap | 5th percentile of target expert score minus strongest competitor | router-logit gap | Stability guard | Optimality |

**Decision question:** Can embedding-gradient selection identify feature-relevant hidden states under full-sequence LM loss?

**Not in scope:** real-DCLM transfer, semantic expert utility, common/rare routing, and attention-context claims.

## 2. Physical Priors

**P1: Causal feature-token prior.** If the feature slot causally determines a later target token, its token states should receive structured gradient signal even under full-sequence LM loss.

Could be wrong if: neutral-token prediction dominates the gradient field and hides feature-dependent signal.

**P2: Selection-cleanliness prior.** Router initialization needs a selected hidden-state pool whose centers are route-relevant and feature-separated.

Could be wrong if: high-gradient positions contain a mixture of route states, target states, and unrelated background states.

## 3. Falsifiable Hypotheses

**H1:** Full-LM embedding-gradient top-k selection can initialize feature-specialized router rows.

Supported if: it beats all-position clustering, approaches route-position control, has positive margin p05, and does not route by slot start.

Weakened if: it improves feature NMI but margin p05 is zero or negative.

**H2:** Raw top-k enlargement is enough to recover the missing feature signal.

Supported if: top-4 or top-8 improves both NMI and margin over top-1.

Weakened if: larger top-k improves or preserves NMI but worsens margin.

## 4. Mathematical Model

**Objects:**

- Hidden state at position $p$: $h_{i,p}$.
- Embedding gradient: $g^{emb}_{i,p}=\nabla_{e_{i,p}}\mathcal L_i$.
- Gradient energy: $E^{emb}_{i,p}=\|g^{emb}_{i,p}\|_2^2$.
- Selected hidden-state pool: $\mathcal H_{sel}=\{h_{i,p}:p\in\mathrm{TopK}(E^{emb}_{i,p})\}$.

**Core decomposition:**

Route-only loss:

$$
\mathcal L^{route}_i=\mathrm{CE}(\ell_{i,r_i}, y_i).
$$

Full-sequence next-token loss:

$$
\mathcal L^{full}_i=\sum_{p=0}^{T-2}\mathrm{CE}(\ell_{i,p}, x_{i,p+1}).
$$

Full-LM gradient mixture:

$$
\nabla_e \mathcal L^{full}
=\nabla_e \mathcal L^{feature-target}
+\nabla_e \mathcal L^{neutral-background}
+\nabla_e \mathcal L^{other-token}.
$$

**Mechanism relation:** if the useful feature-target component dominates the selected positions, k-means on $\mathcal H_{sel}$ should produce router rows with high feature NMI and positive margin. If neutral/background components dominate, feature NMI may improve but margin will be thin or negative.

**Observable metrics:** feature NMI, margin p05, selected route/slot fraction, and slot-start NMI.

**Falsifier:** full-LM top-k fails to beat all-position clustering, or beats it only with negative/unstable margin.

## 5. Computational Realization

**Input objects:** balanced synthetic no-position slot sequences with four features, three slot starts, slot lengths 1/2/4/8, and feature-specific target tokens.

**Computed variables:** hidden states, embedding gradients, hidden gradients, top-k selected positions, k-means centers, router assignments, feature NMI, and margin p05.

**Algorithm stages:**

- warm up the one-layer Transformer-MoE under `route_ce` or `full_lm`;
- compute per-position gradients on calibration data;
- select top-k positions per sample by gradient energy;
- cluster selected hidden states and initialize router rows;
- evaluate immediate and post-training routing.

**Stage-local evidence:** positive controls, selector locality, slot-start NMI, slot-length breakdown, and final training trajectory.

**Expected artifacts:** `protocol.md`, `summary.md`, `detailed.md`, tables, and central figures in the A06_28 experiment folder.

## 6. Minimal Falsification Tests

**Test:** full-LM objective-locality guard.

**Question:** does embedding-gradient top-k still work when the loss is full next-token LM rather than route-only CE?

**Intervention / comparison:** compare `route_ce` and `full_lm` across all-position clustering, route-position control, oracle centers, hidden-gradient top-k, and embedding-gradient top-k.

**Primary metric:** immediate feature NMI after router reinitialization.

**Guard metrics:** margin p05, preserve fraction, slot-start NMI, selected route/slot fraction, and final feature NMI.

**Pass:** full-LM embedding-gradient top-k beats all-position clustering, approaches route-position control, and has positive margin p05.

**Fail:** full-LM embedding-gradient top-k does not beat all-position clustering.

**Weakened:** full-LM embedding-gradient top-k improves NMI but fails the margin guard.

**Failure means:** the raw full-LM gradient-energy operationalization is insufficient; it does not falsify the possibility of denoised full-LM gradient scores.

## 7. Current Evidence

**Observation:** the four-GPU full run completed 32/32 seed-slot cells. Under full LM at warmup 40, embedding-gradient top-1 improves immediate feature NMI from the all-position baseline 0.738 to 0.823 and has immediate margin p05 0.782. After 160 post-reinit steps, its feature NMI is 0.845 but margin p05 is -1.828. Top-4 and top-8 have similar immediate NMI but negative immediate margin. Route-position control under the same full-LM setting reaches immediate NMI 0.988 and margin p05 10.111.

**Long-train audit:** a follow-up four-GPU audit trained the same full-LM warmup-40 conditions to 2000 post-reinit steps. It completed 32/32 seed-slot cells. Embedding-gradient top-1 did not recover: feature NMI changed from 0.845 at step 160 to 0.717 at step 2000, and margin p05 changed from -1.828 to -9.142. Clean controls also lost low-tail margin by long training: oracle center margin p05 changed from 6.221 at step 160 to -5.359 at step 2000; route-position center margin p05 changed from 5.550 to -4.531.

**Interpretation:** full-LM gradients contain feature signal, but raw gradient energy does not isolate a clean enough state pool for stable router initialization. Increasing top-k adds noise rather than fixing the margin. Longer full-LM training is not a rescue; it introduces an additional preservation problem because the LM objective can erode even clean center margins while target accuracy improves.

**Boundary:** this is a synthetic balanced no-position setting. Full-LM selection does not use route position to select tokens, but route position is still used for evaluation and positive controls.

**Evidence links:**

- `../../experiments/A06/A06_28_full_sequence_lm_gradient_selector_guard/summary.md`
- `../../experiments/A06/A06_28_full_sequence_lm_gradient_selector_guard/detailed.md`
- `../../experiments/A06/A06_28_full_sequence_lm_gradient_selector_guard/figures/a06_28_guard_core_reinit_w40.png`
- `../../experiments/A06/A06_28_full_sequence_lm_gradient_selector_guard/figures/a06_28_full_lm_slot_len_boundary_w40.png`
- `../../experiments/A06/A06_28_full_sequence_lm_gradient_selector_guard/figures/a06_28_selector_locality_w40.png`
- `../../experiments/A06/A06_28_long_train_margin_audit/summary.md`
- `../../experiments/A06/A06_28_long_train_margin_audit/detailed.md`
- `../../experiments/A06/A06_28_long_train_margin_audit/figures/a06_28_long_train_nmi_margin_trajectory.png`
- `../../experiments/A06/A06_28_long_train_margin_audit/figures/a06_28_long_train_final_step2000.png`

## 8. Claim Boundary And Next Decision

**Can claim:**

- Full-sequence LM gradients carry measurable feature-routing signal in this synthetic no-position setting.
- A06_27's route-only result remains a strong positive control but has a narrower claim boundary.
- Raw embedding-gradient top-k is not yet a stable unsupervised router-initialization method because the margin guard fails.
- Training the raw selector longer to 2000 full-LM steps does not recover margin.
- Clean feature/route center initialization remains stronger than raw gradient selection, but long full-LM training can erode even clean center margins.

**Cannot claim:**

- The current method solves unsupervised feature discovery in real language data.
- Selected gradient positions are semantic features.
- Attention context, full-LM gradient signal, and rare-feature routing are equivalent.
- Larger top-k fixes the selector; here it often worsens margin.
- Feature centers are useless; they are strong at initialization and early training.
- The long-train margin erosion necessarily transfers to real language data or larger models.

**Next decision:** split the next step into two decisions: first test whether a denoised full-LM gradient score can isolate feature-slot signal from neutral-token prediction noise without using route-position labels; then test a preservation intervention that keeps clean center margins under longer full-LM optimization.
