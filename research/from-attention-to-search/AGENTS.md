# from-attention-to-search — research records

Inherit [root AGENTS](../../AGENTS.md). This directory is the project's research
history inside Research_System; code lives in the project repository
(`Projects/from-attention-to-search`, branch `Xingyu`), raw outputs and
checkpoints in `/data/250010109/MoE_Router/`.

## Layout
- `main/explore/MMDD_<slug>/` — exploration lane (default): `log.md` + a pointer
  to the script in the project repo or execution workspace.
- `main/problem_anchors/<line>/` — designs (section 8 holds the next decision);
  `main/experiments/A<line>/` — formal records; `main/research_notes/` —
  supporting notes, never a second design; `main/stories/<line>/` — Stories.
- Every formal Anchor is registered in `main/anchor_ownership.json` with a
  numbered identity (`06_02`, `06_02_03`); experiments inherit that ownership.
  No unnumbered parallel families. Renumbering or relocation changes no
  scientific state.
- Large figures/tables stay git-ignored (`.gitignore` here); select evidence
  explicitly. `XingyuD/` is a local link to the historical execution surface in
  the project repo.

## Formal lane extras (load with `docs/formal_lane.md`)
- The research map (`main/research_map.json` and readers) is updated when a
  promoted result changes a question link, evidence boundary or confirmed
  decision; not after every exploration step.
- Check organization with
  `python tools/check_anchor_organization.py --project-root research/from-attention-to-search`.
