# Uniform Feature Routing CVPR 2026 Workspace

This folder contains a CVPR-format workspace for the controlled uniform feature
routing paper.

## Layout

```text
latex/main.tex              CVPR entry point
latex/preamble.tex          shared packages and theorem definitions
latex/sec/                  paper sections
latex/figures/              copied paper figures from the source workspace
latex/main.bib              bibliography
latex/cvpr.sty              CVPR 2026 style file
latex/ieeenat_fullname.bst  CVPR bibliography style
```

The source research workspace remains:

```text
papers/uniform_feature_moe_initialization/
```

## Build

From `latex/`, use a standard LaTeX toolchain, for example:

```bash
pdflatex main
bibtex main
pdflatex main
pdflatex main
```

The local Codex environment currently may not include a LaTeX compiler, so this
folder is prepared as source.
