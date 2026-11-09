# Text manifest: A15_27 R01

The authoritative full text, exact token IDs and controlled pairings are [qualified_cases.jsonl](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/panel/qualified_cases.jsonl) and [tokenized_sequences.jsonl](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/panel/tokenized_sequences.jsonl). Their bytes were fixed before the first model forward. [Case index](case_index.csv) records all base cases; [qualification](provenance/qualification.json) records token matching and split separation.

All 288 prefixes are Codex-assistant constructed natural-language text with controlled edits, not unmodified natural-corpus excerpts. The model sees the prefix ending at the target; no suffix is used. English follows the dictionary's DCLM source. Twelve discovery and twelve holdout cases in each of A/B/C give 72 base cases; all four versions of a case remain together. Template, entity-combination and source-group IDs are disjoint across the split. The source is one construction process, so this does not test cross-author or natural-corpus generalization.

A changes local collocations. B changes preceding explicit sense descriptions with the same target-local wording. C relocates the same neutral block while preserving each clue and target. Every case has matched token length and target position. Some A phrases change a/an for English grammar; they are local constructions, not edits of one token only. C distance is the number of complete tokens between the end of the saved full clue span and the target: near1, far40/41/45/46. Clue span width is separately retained. Distance and clause order move together.

The independent reference frequency is positive-hit count /261632 historical DCLM TRAIN discovery positions; panel hit rate is distinct. Its historical backbone digest is absent and SAE encoding used BF16 autocast rather than current FP32. These limits qualify frequency-matched nulls.

Predeclared candidate continuations for B/C are semantic compatibility diagnostics, with no unique correct answer or functional-success label. A has no reliable candidates and is NA. [Exclusion rules](provenance/exclusions.json) were written without feature results.

## Fixed illustrations

### A01

- base: Mara began a field note on Monday. In it, Mara described the river bank
- changed: Mara began a field note on Monday. In it, Mara described the savings bank

### B01

- base: Mara prepared an account in Ashford. The account describes land beside a river, with water washing against soft soil. The copy was filed on Monday. The bank
- changed: Mara prepared an account in Ashford. The account describes an office handling money, with clerks arranging new loans. The copy was filed on Monday. The bank

### C01

- near_base: Mara organized notes from Ashford. A separate notice listed the opening hours of the local library. It also recorded the date of the next town meeting. Someone checked the spelling of the street names and placed the notice in a folder. A stream runs past the strip of soil that forms its outer edge. The bank
- far_base: Mara organized notes from Ashford. A stream runs past the strip of soil that forms its outer edge. A separate notice listed the opening hours of the local library. It also recorded the date of the next town meeting. Someone checked the spelling of the street names and placed the notice in a folder. The bank

## Identity

Tokenized manifest SHA256: `945914b9007a4a576f6de99b00b791af56e8daf4464de9169959e733b20d2246`. [Pre-forward freeze](provenance/pre_forward_freeze.json) binds Protocol, text, code and analysis choices.
