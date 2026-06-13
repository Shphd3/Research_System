# Slides

Immediate task: prepare the Project 2 presentation slides for 2026-06-15.

## Chosen Workflow

Use the local `Presentations` plugin as the production tool for creating and
checking the editable PPTX file.

Use this template:

```text
Projects/academic_writing/resources/ppt_templates/hetau_college_ppt_template_0709.pptx
```

Use the school template as the visual and layout source. Preserve its typography,
spacing, footer/header style, and slide-frame logic unless a specific slide
cannot communicate the evidence clearly.

Use `Gabberflast/academic-pptx-skill` as the academic communication reference:

```text
https://github.com/Gabberflast/academic-pptx-skill
```

Apply these rules from that skill:

```text
1. Every content slide uses an action title: a complete sentence that states
   the slide's takeaway.
2. The ghost deck test must pass: reading only the action titles should tell
   the full argument.
3. Use one main exhibit per result slide.
4. Annotate the key finding directly on the figure/table/diagram.
5. Cite borrowed figures or claims on the slide, with a references slide.
6. End the main deck on conclusions, not on a blank "Thank You" slide.
7. Keep body text large enough for the back of the room; remove content before
   shrinking text below readable size.
```

## Working Title

```text
Diagnosing MoE Gating Specialization: From Route Consistency To Expert Utility
```

## Slide Story

1. Problem: MoE gating should route different predictive features to useful
   experts, but route patterns alone are ambiguous.
2. Motivation: high route purity or consistency can be caused by shortcut,
   collapse, or deterministic lock-in.
3. Research question: what evidence is needed before claiming feature-level
   expert specialization?
4. Diagnostic decomposition: feature axis, non-collapse, composition, and
   route-utility binding.
5. Evidence: same-feature consistency can be high under current diagnostics.
6. Boundary: high same-feature consistency does not prove functional
   specialization.
7. Current conclusion: the research line has reduced the uncertainty but has
   not closed the full specialization claim.
8. Next step: test whether assignments bind to utility-best experts under the
   chosen feature axis.

## Minimum 15-Minute Structure

```text
1 title slide
1 problem and motivation slide
1 definition slide
2 method/diagnostic slides
2 evidence slides
1 claim-boundary slide
1 next-step slide
1 backup or question slide
```

## Production Rule

Before building the PPTX, first write a slide-by-slide outline with:

```text
slide number
action title
main exhibit
speaker purpose
source file or figure need
```

After the outline passes the ghost deck test, build the editable PPTX with the
local `Presentations` plugin in template-following mode.
