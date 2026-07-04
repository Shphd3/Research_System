# Spectral Partition Router CVPR 2026 Draft

This workspace contains a CVPR-format draft of:

```text
Spectral Partition Routing for Uniform Feature Dispatch in Mixture-of-Experts
```

## Template Source

The LaTeX template is copied from the official CVPR/CVF author-kit repository:

```text
https://github.com/cvpr-org/author-kit
```

The template was checked against the CVPR 2026 author guidelines:

```text
https://cvpr.thecvf.com/Conferences/2026/AuthorGuidelines
```

Relevant format constraints from the official guideline:

- CVPR style, two-column, 10pt, letter paper.
- Review mode uses `\usepackage[review]{cvpr}`.
- Main paper limit is eight pages excluding references.

## Current Files

```text
latex/main.tex
latex/preamble.tex
latex/cvpr.sty
latex/ieeenat_fullname.bst
latex/main.bib
latex/sec/
latex/figures/
latex/tables/
```

The figures and tables are copied from the completed V2 full-run workspace:

```text
papers/spectral_partition_router_v2/
```

## Current Status

This is a first CVPR-format draft.  It is self-contained and should be reviewed
for:

1. CVPR page length after compilation.
2. Whether the synthetic-only evidence is appropriate for a CVPR framing.
3. Whether E5 should be framed more narrowly as controlled hard-routing
   training rather than general MoE training.
4. Whether the paired-direction E2 boundary case should move to appendix or
   remain in the main paper.
