# Academic Writing

This project manages Academic Writing course deliverables that are based on the
ongoing MoE gating research line. It is a course-delivery wrapper, not a
replacement for the research mainline.

## Current Course Project

```text
Project 2: Original Research Manuscript and Presentation
Topic: MoE gating and feature-level expert specialization
```

Immediate deliverable:

```text
Presentation slides for the Week 16 class session on 2026-06-15.
Student: 250010109, Deng Xingyu
Presentation order: Week 16, order 10
Time budget: about 15 minutes
```

Final deliverables:

```text
10-page CVPR-format manuscript
presentation slides
poster
LaTeX source files and compiled PDF packaged as a ZIP
deadline: 2026-07-05 23:59
submission link: https://pan.sjtu.edu.cn/web/collect/a54034b1f97b92ab0661ca869da885cb
```

## Source Research Boundary

The course story should use the current `from-attention-to-search` evidence as
ongoing research. The defensible claim is not that functional expert
specialization is solved. The safer current claim is:

```text
Current diagnostics show that weak same-feature routing consistency can be
achieved, but high consistency alone can be caused by collapse or deterministic
lock-in. The next research uncertainty is how to bind route assignment to
non-collapsed expert utility.
```

Primary source:

```text
Projects/from-attention-to-search/main/problem_anchors/01_slot_context_dominance_router_specialization_anchor.md
```

Graph context:

```text
Projects/graphs/expert_specialization.graph.yaml
```

## Folder Map

```text
resources/
  course_requirements/   copied assignment schedule and requirement files
  ppt_templates/         reusable presentation template
main/
  course_requirements.md extracted Project 2 requirements
  roadmap.md             delivery sequence for slides, paper, poster
  research_source_map.md source research files and claim boundary
  notes/                 local course-writing notes
  slides/                slide planning and future slide source
  paper/                 manuscript planning and future LaTeX source
  poster/                poster planning and future poster source
```

## Git Rule

Commit course notes, source files, reusable resources, and small curated
figures. Do not commit generated builds, final submission ZIPs, raw logs,
checkpoints, datasets, or large experiment outputs by default.
