# Atom usage and update channels

[Anchor](anchor.md) · [Protocol](protocol.md) · [Detailed evidence](detailed.md) · [Chinese reading version](summary_cn.md)

**Static figures and the four-H100 Reserved experiment are complete:176/176 branches.** A shared dominant atom coexists with distributed domain preferences; intervention supports an aggregate conditional local functional role for matchable enriched spans. This identifies a candidate channel of benefit, not destructive interference or a long-run isolation advantage.

## 1. Purpose

Operationalize the advisor's atom-use/concentration intuition, then test whether domain-enriched directions carry selective consequences of a shared parameter update.

## 2. Hypothesis

Domain-dependent atom usage and concentrated contributions may coexist with a common dominant component. The functional hypothesis is that enriched directions carry preferential learning benefit for their associated domain; the rival is descriptive enrichment without selective functional relevance beyond generic perturbation effects.

## 3. Analysis Method

- Frozen fresh-S7 exact-21B-token checkpoint, final native attention output, fixed 30,000-atom Top-32 dictionary; 1,024 natural-text records, 256 tokens each, four domains and two previously exposed batches. Fit chooses order/sets; readout shows replication.
- Separate positive frequency, zero-inclusive mean coefficient, and coefficient-square contribution proxy. Runtime atoms are unit length; nonorthogonality prevents interpreting summed squares as an original-representation energy decomposition.
- The registered functional experiment changes only the final attention output projection, measures attention-output/SAE/loss changes, and contrasts full updates with equal-norm redirection away from enriched and matched control spans.

## 4. Conclusion

The same atom, 24605, fires on all 262,144 tokens and accounts for 85.83%–90.50% of readout-domain squared coefficients. Across records 14,192/30,000 atoms are used. Excluding this common atom and renormalizing the remainder, 700–1,898 atoms are needed for 90% of readout remainder contribution. The imposed 32-per-token limit is not a discovered sparsity law. The original fit-enriched top32 atoms retain positive enrichment 32/32 in every readout domain; frequency-profile correlations are 0.972–0.992. This descriptive set is separate from the matchable set used for intervention.

![Common identity atom-use portrait](../../figures/atom_usage_portrait.png)

Read: all domains share one fixed fit-derived atom order. The bottom panels retain explicit atom IDs and compare two record batches, with frequency and magnitude separate.

![Contribution concentration](../../figures/atom_contribution_concentration.png)

Read: full contributions and the common atom remain visible; the lower-right remainder is explicitly renormalized. It cannot replace the full profile.

Sources: [static statistics](/data/250010109/MoE_Router/experiments/20260926_atom_mechanism/analysis/static_statistics.json), [full profiles](/data/250010109/MoE_Router/experiments/20260926_atom_mechanism/analysis/atom_profiles.npz), [lineage manifest](/data/250010109/MoE_Router/experiments/20260926_atom_mechanism/analysis/static_manifest.json).

Intervention job `pt-2lj66pne` SUCCEEDED on four reserved H100s; four sources x two steps x22 conditions completed in about104 seconds including aggregation, with unchanged base parameters/dictionary/buffers and no optimizer trajectory or checkpoint write. The registered aggregate outcome is SUPPORT. Enriched-span redirection removes more target-relative benefit than matched-span redirection at the same parameter-step norm: $M=9.42\times10^{-6}$ nats/token, conditional95% interval$[5.50,13.49]\times10^{-6}$; half-step$4.68\times10^{-6}$, interval$[2.71,6.74]\times10^{-6}$. All eight source-improvement gates pass, all four target-average points are positive at both steps, and the unrescaled removal guard is positive. Biology's individual interval still crosses zero; physics-to-computing has a negative point contrast. Aggregate support does not establish every pair separately. Source: [mechanism results](/data/250010109/MoE_Router/experiments/20260926_atom_mechanism/analysis/mechanism_results.json).

![Local benefit and decoder-span selectivity](../../figures/atom_update_consequences.png)

Read: upper-left shows full-update help, upper-right enriched-minus-control selectivity, lower-left the two primary pooled contrasts, lower-right target heterogeneity. Plot units are millinats/token. All twelve cross-domain full-update means remain helpful at both steps; the full-step range is0.000104–0.000325 nats/token. Removing some benefit relative to the full update is not harm relative to no update. Affected attention outputs, SAE coefficients and losses were directly recorded, but why the update demands are compatible is not fully explained.

Post-hoc descriptive analysis connects the response to representation displacement and loss sensitivity: first-order help approximates their negative inner product. Relative absolute prediction error over16 source/readout means is0.52% for the full step and0.27% for the half step. This is neither a sample-level error guarantee nor a new support gate. It describes small-step directional consistency, not how domain preferences formed. Sources: [supplementary readout](/data/250010109/MoE_Router/experiments/20260926_atom_mechanism/analysis/mechanism_supplementary_readout.json), [derived research route](01_route_and_knowledge_update.md).

The effect is small and conditional on one checkpoint, fit gradients, selected spans and three controls. Intervened objects are overlapping decoder spans, not independent semantic atoms. Atoms10171/4949 were not included as mathematics target-set members, so their function as mathematics-enriched atoms is untested;4949 still occurs in other target/control sets. There is no Gaussian, semantic-purity or long-run interference claim. The single AI-proposed next decision is whether to freeze this selection/intervention rule and replicate its functional selectivity on new article-independent text. Support would justify deeper input/error-signal decomposition; failure would stop treating the rule as a transferable locator. That follow-up was not run.
