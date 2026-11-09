# A15.13.07 — Gold-label layerwise static audit

```text
problem_key: A15.gold_label_layerwise_static_audit
conversation_owner: codex-thread:01a07a07-159a-7893-9f2f-0f120349f4b3
ownership_status: CLAIMED
status: E19_COMPLETE_AWAITING_HUMAN_RESULT_CONFIRMATION
```

## 1. Problem Definition

The decision question is which Transformer blocks expose real M2D2 parent and within-parent child labels strongly enough at the exact tensor read by the current causal Router to nominate shallow, primary, and deep positions for a separate functional pilot. The exact Router input, called site A, is the current-token block input. Site B is the post-attention, normalized input to the block MLP and is a paired representation control; it is not the original attention increment or a proposed replacement Router input.

The smallest blocking uncertainty is whether the old block-9 description survives two readout seeds, correct A/B tensor identification, article-level dependence control, and the unchanged shuffled-label qualification. Passing permits only the frozen functional pilot. Failure or insufficient evidence stops that launch; it does not justify changing the selector or using B to rescue A.

## 2. Physical Priors

1. Domain information usable by the present Router should be directly readable from site A; greater readability at site B can describe within-block formation but cannot by itself justify changing the architecture.
2. A coarse/fine routing position must support both parent and conditional-child readout. A layer that is strong for only one task is not a joint candidate.
3. A small nonlinear probe can reveal folded label information missed by a linear head, but nonlinear success is only an upper-bound diagnostic because the planned Router remains linear.

These priors are falsified locally if A has no qualified stable joint candidate, if its selected layer changes materially across the two frozen seeds, or if the null and data-independence guards fail.

## 3. Falsifiable Hypotheses

The primary hypothesis is that site A has a reproducible middle-layer region where both parent and conditional-child linear recovery remain at least 95% of their own best layer for three consecutive blocks. The strongest rival is that the apparent middle-layer onset is a one-seed, shuffled-label, window-dependence, or wrong-tensor artifact.

A secondary representational hypothesis is that site B or a fixed two-layer nonlinear readout may expose label information earlier or slightly more strongly than the site-A linear readout. This can describe representation formation, but it cannot select or move the functional candidates.

Pass requires all pre-registered qualification gates and an A-only candidate set. Failure means an explicit null, identity, article-provenance, numerical, or seed-stability gate fails. Insufficient means the data or execution cannot adjudicate a gate without changing the frozen contract.

## 4. Mathematical Model

For block \(\ell\) and current prediction position \(t\), let \(A_{\ell,t}\) be the first tensor passed to the block and \(B_{\ell,t}\) the first tensor passed to its MLP. Separate parent and true-parent-conditioned child heads are fitted to each site. For task \(q\) and seed \(s\), linear recovery is

\[
R^{q,s}_{\ell}=\frac{\log 3-\mathrm{CE}^{q,s}_{\ell}}{\log 3-\min_m\mathrm{CE}^{q,s}_{m}},
\qquad
J^{s}_{\ell}=\min(R^{\mathrm{parent},s}_{\ell},R^{\mathrm{child},s}_{\ell}).
\]

If the denominator is non-positive, that task has no candidate. The primary layer is the earliest start of three consecutive blocks where the two-seed development mean of \(J^s_\ell\) is at least 0.95; each seed must independently yield a primary layer within two blocks of the other. The shallow and deep references are respectively the lowest-\(J\) block at least three blocks before and the highest-\(J\) block at least three blocks after the primary, with shallower ties preferred.

The fixed nonlinear ceiling is a `1024 → 32 → 3` GELU classifier. Its gap from the linear head is descriptive and never enters \(J\) or the selector.

## 5. Computational Realization

- Freeze Qwen3-0.6B-Base and the existing M2D2 Wikipedia `3×3` windows. Positions 63--254 predict positions 64--255.
- Register a forward pre-hook on every block for A and on every MLP for B. A/B use the same labels, window order, initialization tensors, optimizer class, update budget, masks, and evaluation weights.
- Fit independent float32 linear real-label and fixed-shuffle heads plus the fixed nonlinear ceiling for seeds 170903 and 170907. Gold labels measure accessibility only; they do not train the base model or an online Router.
- Reconstruct every old window from its source records, retain every contributing article identity and packed-stream offset, and use connected article components when a window mixes articles. Development and the historically viewed confirmation split are both reported; the latter is not presented as new independent confirmation.
- Use site A alone for candidate selection. Site B remains a paired control, and functional training remains under the separate A15.15 Anchor.

## 6. Minimal Falsification Tests

The decisive test is the A-only two-seed joint-recovery selector. Necessary guards are: exact model/data hashes; 28 ordered A and B hook hits with distinct expected tensors; frozen-base and probe-only optimization checks; identical A/B head initialization; finite losses and gradients; zero known cross-split article/title overlap with traceable identities; 2,000 paired article-component bootstrap replicates; and the unchanged null rule for each site, seed, split, and task. The null rule requires median shuffled accuracy in `[0.28,0.39]`, median shuffled cross-entropy within 0.05 nat of \(\log3\), and no three-layer stable shuffled onset.

This test can nominate three positions for a functional pilot. It cannot establish native causal use, online routing success, expert utility, next-token gain, a universal depth law, or a reason to replace A with B.

## 7. Current Evidence

The completed E15 experiment read only site B. It estimated parent and conditional-child stable layers `(9,9)` on both development and confirmation, with bootstrap layer-difference intervals `[0,0]`. The nonlinear ceiling also selected `(9,9)`, the child readout needed 50% of the training windows, and leave-one-child-out parent transfer found no stable layer. The safest interpretation is a descriptive middle-layer label-readability peak, not distinct coarse-before-fine formation.

E15 remains formally `UNQUALIFIED_SHUFFLE_CONTROL`: confirmation conditional-child shuffled-label median cross-entropy was `1.148744`, which exceeded the frozen upper edge by `0.000132` nat. Its accuracy was near chance and it had no shuffled stable onset, but the hard guard still failed. The [E15 Summary](../../../../experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E15_true_label_layerwise_static_audit/summary.md) and [Detailed record](../../../../experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E15_true_label_layerwise_static_audit/detailed.md) preserve that result.

E19 completed the full A/B two-seed static matrix. The immutable registered review gives the A-only point candidate set `{0,10,13}` with primary block `10`, seed-specific primaries `10/10`, and site-B onset `9`; the fixed nonlinear A readout does not provide a reproducible earlier onset. Article identities were recovered with zero ambiguous selected occurrences and zero known cross-split normalized-title or exact-content overlap, although several packed-window cells contain only 1--5 connected article components.

The registered E19 result is `QUALIFICATION_FAILED`: 5 of 16 shuffled-label checks fail at least one frozen CE or accuracy component. The [E19 Summary](../../../../experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E19_ab_paired_router_input_readout_reaudit/summary.md) and [Detailed record](../../../../experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E19_ab_paired_router_input_readout_reaudit/detailed.md) preserve the values and lineage. This is an AI-recorded contract outcome awaiting the researcher's result interpretation; it is not a human-confirmed strengthening of the scientific claim.

## 8. Claim Boundary And Next Decision

The completed evidence supports only that real M2D2 labels are descriptively readable near site-A block 10 and site-B block 9 under the frozen probe contract. It does not qualify `{0,10,13}`, show a coarse-before-fine gap, establish an architecture change, or demonstrate Router or expert function.

The researcher-confirmed branch decision is `STOP_NO_FUNCTIONAL_LAUNCH`, because E19 names five hard-gate failures. That branch is complete: no criterion was relaxed, B did not replace A, and no A15.15 job was submitted. The next scientific decision is `UNKNOWN` pending researcher confirmation of the E19 result boundary; no follow-on experiment is authorized by this Anchor at this revision.
