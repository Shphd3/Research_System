# Codex Web Setup

This repository is initialized as a local git repository, but it currently has no remote configured. To use it from Codex Web, first connect it to a GitHub repository.

Official OpenAI references:

- Codex overview: https://developers.openai.com/codex/
- Codex cloud environments: https://developers.openai.com/codex/cloud/environments/
- `AGENTS.md` project instructions: https://developers.openai.com/codex/guides/agents-md/
- Codex with ChatGPT / Codex Web GitHub requirement: https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan
- Codex remote connections: https://developers.openai.com/codex/remote-connections/

## Recommended Remote Setup

Create a private GitHub repository, for example:

```text
research-files
```

Then run:

```powershell
git remote add origin https://github.com/<owner>/<repo>.git
git push -u origin master
```

If you prefer the branch name `main`, rename before the first push:

```powershell
git branch -M main
git push -u origin main
```

## Codex Web Usage

After the GitHub repository exists and this local repository is pushed:

1. Open Codex Web.
2. Connect the GitHub account / repository.
3. Select this repository when starting a Codex task.
4. Keep `AGENTS.md` at the repository root so Codex can reuse the research-system rules.
5. Ask Codex Web to work on text artifacts here, not on remote-server experiment code unless that codebase is separately connected.

## Remote Server Note

This research workspace and the remote experiment server are two different things:

- Use this repository for research memory, reports, paper reading, claims, and PRISM documents.
- Keep heavy experiment execution on the remote server.
- If later you want Codex app to work directly on the remote server filesystem, use Codex remote connections over SSH instead of mixing server code into this repository. The official remote-connections documentation currently describes SSH remote connections as an alpha feature.

## What Should Be Tracked

Track:

- `AGENTS.md`, `CURRENT.md`, `mainline.md`, `claim_board.md`
- daily reports and experiment cards
- meeting reports and PRISM `.tex` sources
- paper reading cards and notes
- repo-tracked Codex skill sources

Avoid tracking:

- LaTeX build outputs
- large binary backups
- temporary archives
- raw experiment caches
- iCloud temporary files

## Current Local State

- Local git repository: yes.
- Remote configured: no.
- GitHub CLI available: no.

Once a GitHub remote URL is available, the only missing steps are `git remote add origin ...` and `git push -u origin ...`.
