# Academic Writing Project 2 Final Submission

Student: Deng Xingyu  
Student ID: 250010109  
Date: 2026-07-05

## Contents

```text
paper/
  250010109_Deng_Xingyu_Project2_CVPR_Paper.pdf
  latex/
    main.tex
    preamble.tex
    main.bib
    cvpr.sty
    ieeenat_fullname.bst
    sec/
    figures/

slides/
  250010109_Deng_Xingyu_Project2_Presentation.pptx

poster/
  250010109_Deng_Xingyu_Project2_Poster.pdf
  poster.tex
  figures/

audit/
  requirements_audit.md
  slide_paper_logic_alignment.md
```

## Build Commands

Paper, from `paper/latex/`:

```bash
pdflatex main
bibtex main
pdflatex main
pdflatex main
```

Poster, from `poster/`:

```bash
pdflatex poster.tex
```

## Final Checks

- The manuscript is in CVPR format and compiles to a 10-page PDF.
- The paper source includes all referenced `.tex`, `.bib`, style, bibliography-style, and figure files needed by the manuscript.
- The poster compiles to a one-page PDF.
- The presentation deck is based on the 2026-06-15 Project 2 deck; the submission copy repairs a malformed text glyph on slide 9 without changing the research story.
- The paper claim is intentionally narrower than the presentation story: it proves and tests a static controlled routing geometry baseline, not real-model semantic expert specialization.
