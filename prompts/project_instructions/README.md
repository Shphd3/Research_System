# Project Instructions

Reusable prompts for recurring project-level work.

Current examples:

- `research_progress_project_prompt.md`: compact ChatGPT Project instructions
  for sync-anchor context, conclusion-first correction, creative exploration,
  and explanation followed by understanding checks.
- `paper_reading_project_prompt.md`: paper-reading AI prompt for paper/blog reading anchored to the current mainline.

Important: web-side AI may only see `Research_System`, not project subfolders
under `Projects/`. Prompts should tell the agent to read `PROJECTS.md` and
root `sync/` summaries first, then ask the user or Codex to expose
project-local graph, anchor, `summary.md`, or `detailed.md` files when needed.

When a prompt becomes stable and frequently reused, convert it into a Codex skill under `skills/` and install it into `C:\Users\250010109\.codex\skills\`.
