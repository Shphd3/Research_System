# A05_01 Uniform Feature Collapse Mechanism Audit

First read `summary.md`.

This folder audits routing collapse in the original uniform feature experiment before P1/P3 feature-assumption relaxation.

Core judgment:

**A. Early-geometry dominated collapse**, with common-direction alignment as a mechanism candidate.

Important boundary:

Original logs do not contain step 10/20/50 model states. Those early hidden/router diagnostics come from same-config diagnostic replay, not byte-identical original checkpoints.
