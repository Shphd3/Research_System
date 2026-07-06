# Slide-Paper Logic Alignment

## Conclusion

The presentation and the final manuscript do not logically conflict, but they
operate at different claim strengths.

## Presentation Story

The 2026-06-15 presentation is a broader research update. It discusses:

- early routing concentration before specialization;
- common-logit bias;
- real-text step-0 bias;
- step-10 router-hidden-state amplification;
- expert-spectrum initialization as a stress test.

Its safe conclusion is:

```text
Routing geometry is meaningful, but initialization alone does not solve early
training-time concentration.
```

## Manuscript Story

The final manuscript is narrower and more specific. It discusses:

- static controlled top-1 routing;
- spherical token directions;
- equal-measure expert cells;
- finite-token sampling versus prototype-cell geometry;
- spectral diagnostics and capacity assignment controls.

Its safe conclusion is:

```text
Uniform load can be explained by a two-sided geometric sufficient condition,
but load balance alone does not prove semantic expert specialization.
```

## How To Present Them Together

Use the slides as the broader motivation and research context. Use the paper as
the submitted, self-contained theory baseline. Do not say that the paper proves
the real-text step-10 training dynamics from the slides. Do not say that the
slides invalidate the paper: they motivate why the paper's static baseline is
needed before interpreting load or route consistency.

## Main Boundary Sentence

```text
The slides study why early training may amplify routing bias; the paper
isolates the static geometry that must be checked before uniform load is
interpreted as meaningful routing.
```
