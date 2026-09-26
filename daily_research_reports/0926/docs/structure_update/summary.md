# Native structure and same-panel virtual updates

[Chinese reading surface](summary_cn.md) · [Detailed record](detailed.md)

Status: completed bounded exploratory measurement; AI analysis, not a researcher-owned mechanism verdict or a new confirmatory study.

## 1. Purpose

Connect shared-coordinate representation structure to actual local cross-domain update consequences on the same frozen natural-text panel.

## 2. Hypothesis

Domain-discriminable representations might accompany cross-domain update harm. The rival is that distinguishable domains retain compatible prediction adjustments and therefore help one another locally. Neither view implies long-run isolation benefit without a separate comparison.

## 3. Analysis Method

- Reuse the fixed 1,024-record, four-domain panel and exact fresh S7 checkpoint at 21 billion pretraining tokens. Extract native attention writes and the final down-projection inputs. Fit one common PCA basis per object on 512 fit records; display all 512 readout records. Keep body mean, last position, and unit-normalized mean distinct.
- Compute centered variance and uncentered second-moment spectra separately. Preserve all sample-visible components and report how much heldout energy the displayed two-dimensional plane captures.
- Form one full-down-weight gradient per domain on 128 fit records and make independent normalized virtual steps of relative norms 1e-4 and 5e-5. Read out 128 separate records/domain at 16 fixed next-token positions each. Help is baseline loss minus perturbed loss. Use 2,000 paired subfield-stratified record resamples, conditional on each fixed source direction; report every cell and controls.

## 4. Conclusion

1. Native mean-write raw energy is concentrated: its first uncentered component explains 92.33%, and the fit mean contributes 92.14% of average squared norm. Centered variation instead needs 108 components for 90%; the first two fit axes explain 29.42% of readout centered energy. Concentrated raw energy is not one-dimensional sample variation or semantics. [Structure results](/data/250010109/MoE_Router/experiments/20260926_structure_update_bridge/structure_results.json).
2. Actual down-input mean vectors also show domain structure: 95 components cover 90% of fit variance; two fit axes cover 32.56% of readout energy. These inputs differ from the attention vectors observed by the SAE. Gradient formation additionally depends on backward prediction-error signals. [Source and mathematical bridge](detailed.md#2-objects-and-mathematical-bridge).
3. All 12 cross-domain mean directions are helpful at both step sizes: 0.000532–0.002006 nats/target at the full size and 0.000276–0.001043 at half size. Every cross-domain marginal interval has a positive lower endpoint. All source self-improvement point estimates are positive, but computer-science self-improvement at full size has interval [−0.000006, 0.001748], so reliable source improvement is not established for every condition. [All cells](/data/250010109/MoE_Router/experiments/20260926_structure_update_bridge/update_summary.csv).

![Native geometry](../../figures/a_common_axes_and_spectrum.png)

Each point is one readout record; domains share fit-only axes. Centered and uncentered spectra answer different questions.

![Actual parameter inputs](../../figures/u_common_axes_and_spectrum.png)

The same records are shown at the updated matrix's actual input; axes are refit for this object, not equated with the attention axes.

![Actual local consequences](../../figures/same_panel_update_consequences.png)

Rows specify update sources and columns specify readout domains. Positive blue values indicate improvement; displayed losses are multiplied by 1,000.

Boundary: one frozen checkpoint and previously exposed panel; records need not be independent papers. Marginal intervals are not adjusted for 32 comparisons and omit source-gradient and seed uncertainty. Full-weight virtual gradient steps are not LoRA/Adam trajectories. No long-run shared-versus-isolated comparison was performed. Local help does not rule out other harmful states or individual records.

One AI-proposed next decision, revised for the researcher's 2026-09-26 mechanism-first discussion: select one empirically grounded learning consequence and its strongest rival explanation for a separating test. The observed local help is a possible target; a long-run sharing deficit requires its own matched-carrier evidence. Complete this decision by naming the effect, fixed scope, rival predictions and support/non-support/insufficient branches. If a local-harm hypothesis is chosen, both source improvement and independent target harm must qualify; continued help or insufficient evidence must stop using that condition to motivate isolation. Resume from the existing figures and evidence; finding harm is not the success criterion. The specific scientific choice awaits the researcher, and no follow-up run was started.
