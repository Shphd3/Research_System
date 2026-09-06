---
name: sidecar-thinking
description: "Use only when the user explicitly asks to open, show, inspect, or call the local Thinking Sidecar app."
---

# Sidecar Thinking

Use this skill to connect Codex with the local Thinking Sidecar app. The app is a workspace-aware web UI with chat sessions, a manifest-backed research graph, Markdown/HTML previews, and restricted workspace tools.

## Start Or Find The App

If the project provides a Sidecar helper script, use it from that project root:

```bash
scripts/open_sidecar.sh
```

This starts or reuses the Sidecar for that repository, opens the graph UI, and
loads `graph.yaml`. Useful variants:

```bash
scripts/open_sidecar.sh --no-open
SIDECAR_PORT=4318 scripts/open_sidecar.sh
scripts/open_sidecar.sh --graph graph.yaml
```

If the server is not already running:

```bash
cd sidecar
npm run dev
```

Default URL: `http://localhost:4317`.

The app can live inside a research repository or be installed elsewhere. Set `SIDECAR_WORKSPACE_ROOT=/path/to/research-repo` when the app directory is not inside the research repo.

## Default Handoff

Prefer staging a session for the user:

```bash
cd sidecar
npm run codex:call -- --title "Review" --context "Codex summary..." --file research/graph.yaml --question "What is the weakest assumption?"
```

Use automatic ask mode only when the user explicitly wants Codex to relay the answer:

```bash
cd sidecar
npm run codex:ask -- --title "Review" --context "Codex summary..." --question "What should Codex do next?"
```

## Research Graph

The graph is manifest-first:

- `graph.yaml` is the authority for nodes, edges, UI defaults, and file pointers.
- Markdown and HTML files hold node content.
- Markdown frontmatter can supply local metadata, but `graph.yaml` wins on conflicts.
- Graph file links may be workspace-relative, or manifest-relative with `./`, `../`, or a bare filename.

Default manifest path: `research/graph.yaml`. Override with `SIDECAR_GRAPH_MANIFEST` or `.side/config.json` at `graph.manifestPath`.

## API Quick Reference

- `GET /api/config`
- `GET /api/workspace`
- `GET /api/workspace/file?path=<workspace-relative-path>`
- `GET /api/workspace/raw?path=<workspace-relative-path>`
- `GET /api/research-graph`
- `GET /api/sessions`
- `POST /api/sessions`
- `GET /api/sessions/:id`
- `PATCH /api/sessions/:id`
- `POST /api/sessions/:id/files`
- `POST /api/sessions/:id/messages`
- `POST /api/sessions/:id/stream`

All workspace paths are constrained to the configured workspace root.
