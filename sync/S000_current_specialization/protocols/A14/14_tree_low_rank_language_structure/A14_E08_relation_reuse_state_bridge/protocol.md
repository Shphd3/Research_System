# Protocol: A14_E08 Relation-Reuse Parameter-to-State Bridge Audit

## 0. Approval Snapshot

**Approval:** provisionally approved by the researcher on 2026-07-22 for
implementation, smoke testing, and one full run. All thresholds below were
frozen before the evidential run. Post-run review may reject the contract and
authorize a revised rerun, but it does not retroactively move this run's gates.

**Decision question:** at matched full-model capability, does `share16` require
fewer attention-update directions than `random_unshared` to preserve held-out
first-C-token loss?

**Primary metric:**

$$
C_H=
\frac{k_H(\texttt{random\_unshared};0.02)
-k_H(\texttt{share16};0.02)}{64}.
$$

Here $k_H$ is the smallest persistent rank: that rank and every larger rank
must keep the first-C-token cross-entropy increase at or below 0.02 nat.

**Main falsifier:** after provenance, capability, split, and intervention
guards pass, $C_H\le0$, the direction is not positive in all three seeds, or
`share16` needs more than 16 of 64 state directions.

**Claim boundary:** a pass would establish only a state-side bridge in this
controlled composite share manipulation. It would not isolate frequency,
prove a monotonic reuse-rank law, establish a tree mechanism in language, or
justify a Router.

## 1. Alignment And Objects

A14 proves how the dimension of a conditionally active tree propagates once
low-dimensional local sources and linear path maps are given. It does not
prove that NTP training learns such sources.

The inherited ABCD study reports that high-reuse `share16` learns faster and
is more robust to Q/K tail truncation than lower-share conditions. That is a
parameter/function observation. E08 tests the missing state object:

```text
QK functional compression
        ?
        v
reusable task-sufficient attention-update compression
```

The four share settings are treated as composite conditions. They jointly
change relation reuse, context reuse, independent rule count, and function
complexity.

## 2. Registered Hypotheses

1. `share16` has a smaller held-out functional state rank than
   `random_unshared`.
2. Every `share16` seed satisfies $k_H\le16$.
3. At the selected rank, the calibration-fitted PCA space preserves held-out
   loss while the median of 32 equal-rank Haar-random spaces does not.
4. The ordering of combined-QK functional ranks is a secondary bridge
   diagnostic, not a pass/fail substitute.

## 3. Provenance And Capability Gates

The source generator, exact mapping tables, model code, checkpoints, and
training code must be recovered for a registered source replay. If any are
missing, a reconstruction may be run for exploratory evidence, but the formal
registered verdict is **insufficient evidence**.

The primary model is width 64, one layer, one attention head, three seeds, and
the four share conditions. Every run must reach A-to-C and B-to-D
cross-entropy at or below 0.02 for three consecutive 25-step observations.

## 4. Data And Split

Each example is an eight-token sequence consisting of two-token A, B, C, and D
fields. A, B, C, and D marginals, sequence length, sample count, model, and
optimizer are held fixed across conditions. D is determined by B. A-to-C is a
permutation owned by a B-family of size 16, 4, 2, or 1.

Calibration and test sets are disjoint by B identity. `share4` and `share2`
are split within every mapping family. A deterministic split swap is the
robustness check. No test state may be used to fit the evidential PCA basis.

## 5. State Intervention

The primary state is the attention residual update at the B-end position. For
condition $s$, fit a calibration mean $\mu_s$ and ordered PCA basis $U_{s,k}$.
Replace a test update $g$ with

$$
\Pi_{s,k}(g)=
\mu_s+U_{s,k}U_{s,k}^{\top}(g-\mu_s).
$$

Run the remainder of the model and measure teacher-forced first-C-token
cross-entropy. Full-basis and direct-update replay must reproduce the original
loss. Diagnostics include energy rank, shuffled state, test-fitted PCA as a
leakage ceiling, and 32 equal-rank random spaces.

## 6. Parameter-Side Diagnostic

Compute the combined score operator $B_{QK}=W_Q^\top W_K$ under the actual
implementation convention. Its functional rank is the smallest persistent
truncated rank that keeps first-C-token $\Delta CE\le0.02$. Individual
$W_Q/W_K/W_V/W_O$ truncations are source-localization diagnostics only.

## 7. Statistical Rule

- Report all ranks by condition and seed.
- Require $C_H>0$ in 3/3 paired seeds.
- Use 5,000 hierarchical paired bootstrap replicates over seed and held-out B
  identity; require the 95% percentile interval lower bound to exceed zero.
- Require every `share16` rank to be at most 16.
- Require the learned PCA space to pass at its selected rank and the median
  equal-rank random space to fail.
- Require the split swap not to reverse the extreme-condition contrast.

## 8. Verdict Rules

**Success:** every provenance, capability, replay, statistical, budget,
random-control, and split-swap gate passes.

**Failure:** all hard guards pass, but any primary state-rank, budget, random
control, or split-stability criterion fails.

**Insufficient evidence:** source artifacts are unavailable, source replay
cannot be established, matched fit or intervention replay fails, or execution
is incomplete.

## 9. Central Figures

1. State functional-rank curves: rank on the x-axis and first-C-token
   $\Delta CE$ on the y-axis, with the 0.02 threshold.
2. Combined-QK rank versus state rank: one point per condition and seed.

Neither figure may be used to assign the effect to pure frequency or to infer
a Router architecture.

## 10. Approved Execution Record

- 2026-07-22: provisional approval granted for direct execution.
- Frozen values: attention residual update, $\epsilon=0.02$ nat, rank budget
  16/64, 3/3 seed direction, hierarchical bootstrap, random-subspace and
  split-swap guards.
- Required post-run review: provenance fidelity, exact hook location,
  B-disjoint leakage protection, persistent-rank definition, random-control
  interpretation, and composite-condition claim boundary.
- 2026-07-22: the full run completed. The S0 provenance hard gate failed
  because the public source lacks the generator, training code, and
  checkpoints; the formal verdict is therefore `insufficient_evidence` even
  though all remaining reconstruction gates passed. See [summary.md](/Projects/from-attention-to-search/main/experiments/A14/14_tree_low_rank_language_structure/A14_E08_relation_reuse_state_bridge/summary.md).
