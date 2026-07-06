# Project 2 Requirement Audit

## Verdict

The final package satisfies the visible Project 2 submission requirements.

## Requirement Checklist

| Requirement | Status | Evidence |
|---|---:|---|
| 10-page research manuscript | Pass | `paper/250010109_Deng_Xingyu_Project2_CVPR_Paper.pdf` is 10 pages. |
| CVPR format | Pass | Paper uses `cvpr.sty` with page numbers and student identity. |
| LaTeX source files | Pass | `paper/latex/` contains `main.tex`, section files, bibliography, style files, and figures. |
| Compiled PDF | Pass | `paper/250010109_Deng_Xingyu_Project2_CVPR_Paper.pdf`. |
| Presentation slides | Pass | `slides/250010109_Deng_Xingyu_Project2_Presentation.pptx`. |
| Poster | Pass | `poster/250010109_Deng_Xingyu_Project2_Poster.pdf` and source. |
| Zip-ready package | Pass | This folder is the source tree for the final zip. |

## Claim Boundary

The final paper should be read as a controlled theory-and-synthetic-experiment
manuscript. It supports the following claim:

```text
Uniform expert usage under an unconstrained top-1 router has a clean sufficient
geometric explanation when token directions are spherical and expert prototypes
induce equal-measure cells.
```

It does not claim:

```text
semantic expert identity;
downstream utility;
training-time preservation;
that spectral alignment alone guarantees balanced routing;
that covariance isotropy alone certifies directional uniformity.
```

## Build Verification

Paper:

```text
pdflatex main
bibtex main
pdflatex main
pdflatex main
```

Verified:

```text
pages: 10
page size: letter
LaTeX errors: none
undefined references/citations: none
overfull boxes: none in final log
```

Poster:

```text
pdflatex poster.tex
```

Verified:

```text
pages: 1
LaTeX errors: none
warnings/overfull boxes: none in final log
```
