# 06_30 Noise-Free Full-Slot Preservation Anchor

## 0. Thinking Card

**Phenomenon:** In A06_28/A06_29, even ideal route/feature-center initialization can lose positive margin under long full-sequence language-model training.

**Mechanism guess:** The margin erosion may be caused by background-token gradient noise: non-feature positions dominate the all-position loss and push router rows away from the feature partition.

**Key variables:** background-token fraction, full-sequence loss, ideal feature-center router initialization, all-position feature-route NMI, margin p05.

**Causal relation:** If background gradient noise is the main cause, then removing background tokens and making every position feature-bearing should preserve ideal feature routing under the same full-sequence loss.

**Observable metric:** final all-position feature NMI and matched margin p05 after 2000 full-LM training steps.

**Rival Explanations:** margin erosion may instead come from selected-expert feedback, softmax/router competition, representation drift, optimizer dynamics, or expert shortcut learning.

**Decision:** If noise-free full-slot sequences preserve positive margin, pursue background/noise-gradient decomposition. If they still lose margin, background noise is not sufficient and the next anchor should move to one-step router dynamics.

## 1. Problem Definition

**Decision question:** Does removing background-token noise make ideal feature-center routing survive long full-sequence LM training?

**Parent relation:** This anchor is a root-cause audit before the A06 router-dynamics story proceeds to soft-router one-step analysis.

**Primary metric:** final all-position feature NMI with final matched margin p05 as the preservation guard.

## 2. Physical Priors

1. Full-LM training in the mixed-slot setting contains many non-feature positions.
2. Non-feature positions can send gradients that solve local token prediction while not preserving feature-to-expert binding.
3. A no-background sequence makes every supervised next-token position feature-bearing, so background-gradient noise should be removed.

## 3. Mathematical Model

For feature $f$, matched expert $a(f)$, and hidden state $h_{i,t}$ from a token position:

$$
m_{i,t}
=
\min_{e\ne a(f_i)}
(w_{a(f_i)}-w_e)^\top h_{i,t}.
$$

The audited claim is:

$$
\Pr[m_{i,t}(T)>0\mid \text{all positions are feature-bearing}]
$$

should remain high if background-token gradients are the dominant cause of margin erosion.

## 4. Computational Realization

Use the existing one-layer Transformer plus weighted top-1 MoE surface. Replace the mixed slot/background sequence with a 32-token sequence in which all 32 positions are the same feature token.

Four features are uniformly sampled. Each sequence is:

$$
x=(F_f,F_f,\ldots,F_f),\qquad |x|=32.
$$

Training uses full next-token LM loss over positions 0 to 30:

$$
L=\sum_{t=0}^{30}\operatorname{CE}(\ell_t,x_{t+1}).
$$

## 5. Minimal Tests

**Main test:** ideal all-position feature-center initialization, trained for 2000 full-LM steps.

**Guards:** ideal predictive-position centers, ideal last-predictive-position centers, and random initialization.

**Primary pass:** ideal centers retain high all-position feature NMI and positive final margin p05.

**Fail:** ideal centers still lose margin p05 or feature NMI under no-background sequences.

**Insufficient:** step-0 ideal routing does not work, target prediction fails, or results are seed-unstable.

## 6. Current Evidence

A06_28 long-train audit showed that under mixed full-LM data, oracle centers decay from step-0 feature NMI 1.000 and margin p05 11.669 to step-2000 feature NMI 0.845 and margin p05 -5.359. A06_29 showed mean-DNS does not solve the same preservation problem.

This anchor's full run completed 8 seeds with 32-token no-background full-slot sequences. Oracle all-position, predictive-position, and last-predictive-position centers all preserved all-position feature NMI 1.000 through 2000 full-LM steps and ended with margin p05 about 4.566. Random routing reached the repeated-token prediction task but remained weaker in feature NMI, about 0.789, and negative in final margin p05, about -2.964.

Evidence path:

- `../../../experiments/A06/A06_30_noise_free_full_slot_preservation/summary.md`
- `../../../experiments/A06/A06_30_noise_free_full_slot_preservation/detailed.md`

## 7. Claim Boundary

This anchor can test whether background-token noise is necessary for the observed synthetic full-LM margin erosion. It cannot prove real-DCLM behavior, semantic expert utility, or the full cause of preservation failure.

## 8. Next Decision

The no-background full-slot condition preserves margin. The next decision is to write a graded background-ratio margin-budget anchor that gradually adds neutral/background positions and measures when the correct feature signal is overtaken by background-signal, router-drift, or hidden-drift terms.
