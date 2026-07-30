# Project Instructions

Reusable prompts for recurring project-level work.

Current examples:

- `research_progress_project_prompt.md`: compact ChatGPT Project instructions
  for sync-anchor context, conclusion-first correction, creative exploration,
  bounded convergence through human writing, and explanation followed by
  understanding checks.
- `paper_reading_project_prompt.md`: paper-reading AI prompt for paper/blog reading anchored to the current mainline.
- `a14_02_rare_common_rank_audit_and_execution_prompt_cn.md`: Chinese-first
  Thinking Card and execution gate for the improved active A14_02 E02
  frequency/mapping-rank experiment and E03 rare outside-common-subspace
  mechanism experiment; it preserves the old E02-v1 evidence through lossless
  archive migration and requires staged human authorization.

Important: web-side AI may only see `Research_System`, not project subfolders
under `Projects/`. Prompts should tell the agent to read `PROJECTS.md` and
root `sync/` summaries first, then ask the user or Codex to expose
project-local graph, anchor, `summary.md`, or `detailed.md` files when needed.

When a prompt becomes stable and frequently reused, convert it into a
repository Codex skill under `.agents/skills/`. Do not install or synchronize a
second personal-directory copy for this repository.
