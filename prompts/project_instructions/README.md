# Project Instructions

Reusable prompts for recurring project-level work.

Current examples:

- `research_progress_project_prompt.md`: ChatGPT Project prompt for web-side research reasoning, meeting transcript debrief, experiment planning, result sync, and pre-meeting convergence.
- `paper_reading_project_prompt.md`: paper-reading AI prompt for paper/blog reading anchored to the current mainline.

Important: web-side AI may only see `Research_System`, not project subfolders
under `Projects/`. Prompts should tell the agent to read
the relevant `PROJECT_SNAPSHOT_<project>.md` for the active project state,
when such a snapshot exists.

When a prompt becomes stable and frequently reused, convert it into a Codex skill under `skills/` and install it into `C:\Users\250010109\.codex\skills\`.
