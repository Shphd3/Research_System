# S18: Nesting Degree vs Reference Frequency of Discriminative Members ("discriminating" is not "rare")

[中文](summary_cn.md) · [Detailed (CN)](detailed_cn.md)

CPU-only post-hoc exploration on cached S13 data, 2026-11-08; no new forward pass, training or member re-selection. Researcher judgment: **Unknown**.

## Answer

Sibling-discriminative members come in two kinds. **Nested** members (most activation inside their own parent's texts) are rare in reference text. **Reused** members (also common under other parents) are frequent. A discriminative member's frequency follows its range of use, not its discriminative role. The pattern holds for both SAEs, three thresholds and two wordings.

## Definitions

- Discriminative members: S13's DEV-frozen sibling Top32 turnover candidates (66 Attention, 41 MLP member×pair units). Shared reference: S13 CONF sibling-intersection events.
- Nesting degree: the share of a member's presence across the 24 label texts that falls in its own parent group (parent + two children). Chance = 3/24. Computed on CONF, independent of the DEV definition.
- Reference frequency: S11 end-colon activation rate (Q: 6000 questions; G: 6000 DCLM docs).

## Results (explicit wording, threshold 0.5)

| SAE | nested / reused | Q mean nested → reused | difference, family bootstrap | member resampling | Spearman ρ(nest, Q) |
|---|---|---|---|---|---|
| Attention | 22 / 44 | 0.82% → 8.98% | 8.17pp [7.24, 8.57] | [4.54, 12.67] | −0.72 [−0.74, −0.69] |
| MLP | 20 / 21 | 0.48% → 45.32% | 44.84pp [42.79, 44.84] | [30.16, 58.85] | −0.78 [−0.81, −0.75] |

Example: MLP #8048 discriminates car/bicycle with nesting 0.15 (near chance) and Q = 74.68%. MLP #22958 (cat/dog) has nesting 0.92 and Q = 0.43%. Unexpectedly, shared sibling members are mostly not nested: their event-weighted nesting is 0.195 / 0.171, and nested ones are only about 5% of the shared mass.

## Interpretation and boundary

Frequency measures how widely a member is used. Discrimination is a relative property of one category pair. The two coincide only for nested members. At least half of the discriminative members are reused, so their high frequency needs no "not learned well" explanation. That explanation still stands as an alternative and was NOT RUN. The analysis has only 8 parents, uses template texts and reuses an exposed CONF split.
