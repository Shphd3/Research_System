# Five figures and interpretation

[中文](figures_cn.md) · [Summary](summary.md) · [Detailed](detailed.md)

All results concern final14/F16384 exposed D/V within one bin. No independent-document or learning claim is certified.

## Frequency rank

[PDF](../figures/figure1_frequency_rank.pdf) · [SVG](../figures/figure1_frequency_rank.svg) · [PNG](../figures/figure1_frequency_rank.png)

![Frequency rank](../figures/figure1_frequency_rank.png)

**How to read:** D fixes the feature order; V uses identical IDs. Frequency is percent on a log axis; zero hits are separate.

**Observation:** D353 and V393 zero hits; V-positive median0.380%, maximum99.264%.

**Meaning:** Unequal feature use and within-window agreement do not establish natural hierarchy or interpretability.

**Next step:** Retain reliability flags and unresolved rare features.

## Frequency stability

[PDF](../figures/figure2_frequency_stability.pdf) · [SVG](../figures/figure2_frequency_stability.svg) · [PNG](../figures/figure2_frequency_stability.png)

![Frequency stability](../figures/figure2_frequency_stability.png)

**How to read:** One feature per point; x=D and y=V percent, log axes, y=x reference; zero categories separate.

**Observation:** Spearman0.99792; D-only zero63,V-only zero103,both zero290.

**Meaning:** Global correlation does not establish rare-feature reliability or document independence.

**Next step:** Do not delete V-missing candidates; establish document eligibility separately.

## Relationships and groups

[PDF](../figures/figure3_relations_groups.pdf) · [SVG](../figures/figure3_relations_groups.svg) · [PNG](../figures/figure3_relations_groups.png)

![Relationships and groups](../figures/figure3_relations_groups.png)

**How to read:** Fixed300 IDs and D-group boundaries. Matrix phi and log-frequency strip have separate legends. Mask the self-correlation diagonal; saturate colors outside±0.1, retaining original values.

**Observation:** Full-data groups186/185 and matched Jaccard0.54838. Display has2 IDs from the first114 groups and1 from the remaining72.

**Meaning:** This subset cannot display complete within-group blocks. q20 yields65/61groups, showing scale dependence rather than unique natural experts.

**Next step:** Retain full partitions; complete null/document qualification before a stronger H1 claim.

## Group frequency and controls

[PDF](../figures/figure4_group_frequency_controls.pdf) · [SVG](../figures/figure4_group_frequency_controls.svg) · [PNG](../figures/figure4_group_frequency_controls.png)

![Group frequency and controls](../figures/figure4_group_frequency_controls.png)

**How to read:** Largest20 D groups in the main plot; actual V log-frequency SD and size-/mean-matched random95% ranges, not sampling CIs. All186 groups in the appendix PDF.

**Observation:** Equal-group real SD0.35331dex versus size-control0.67565dex. Only142 mean-controls qualify, covering48.37%members; primary TbNA and formalB0.

**Meaning:** Size-controls suggest closer frequencies but do not remove mean/phi preference. Missing44 controls are neither zero nor grounds for selected-subset inference.

**Next step:** Repair budget/size scheduling in a preregistered rerun rather than tuning current results.

## Inputs and activations

[PDF](../figures/figure5_inputs_activations.pdf) · [SVG](../figures/figure5_inputs_activations.svg) · [PNG](../figures/figure5_inputs_activations.png)

![Inputs and activations](../figures/figure5_inputs_activations.png)

**How to read:** All V coverage plus first3 D-size-ranked groups with one frozen random/high-score case each. Mark target token, member IDs/z and other-group hits.

**Observation:** No/unique/multiple hits34.66%/39.52%/25.82%.176groups supply1,760cases;10 thresholds unachievable.

**Meaning:** Cases do not establish semantics or utility. Context-uniform random examples are not uniform-token examples; overlap limits top1 mapping.

**Next step:** Define overlap/unassigned handling and K-expert capacity before H2.

[All186 groups,10-page PDF](../figures/figure4_all_groups.pdf). Source values, scripts and commands are preserved in [plot provenance](../evidence/figures/plot_provenance.json). Fixed-group SD bootstrap1000 has997 fully estimable repetitions; its conditional equal-group range is0.35267–0.35769dex. Missing repetitions remain stored; this is not a document-valid or primary matched-effect interval.
