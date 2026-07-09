# Research Stories

This folder stores line-level research stories for `from-attention-to-search`.

A story is a living synthesis for one research line. It connects the research
question, physical intuition, mathematical model, theorem state, anchor chain,
experiment evidence, claim boundary, and next decision. It does not replace
anchors, protocols, `summary.md`, or `detailed.md`.

## Active Stories

| Line | Story | Role |
|---|---|---|
| `06_geometry_proxy_preservation` | `06_geometry_proxy_preservation/story.md`, `06_geometry_proxy_preservation/story_cn.md` | Router training-dynamics story for the active preservation line; shifts A06 from center discovery to one-step router movement and signal/noise margin budget. |
| `11_long_horizon_mtp_objective` | `11_long_horizon_mtp_objective/story_cn.md` | Chinese line-level synthesis for the long-horizon MTP objective line. |

## Sync Rule

When a research line is explicitly synced, sync both:

```text
main/problem_anchors/<line>/
main/stories/<line>/
```

The project-local story remains the source of truth. Root sync may copy it for
external readers only when explicitly requested.
