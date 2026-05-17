# ChatGPT Project + GitHub + Codex Cloud Workflow

This workflow separates three roles:

- ChatGPT Project: high-reasoning discussion, transcript debrief, mainline planning, claim audit, meeting convergence.
- GitHub connector: read/search the latest `Research_System` repository state from ChatGPT Project.
- Codex cloud: edit repository files in an isolated cloud task and return diffs.

Official references:

- GitHub connector for ChatGPT: https://help.openai.com/en/articles/11145903-connecting-github-to-chatgpt
- Codex cloud environments: https://developers.openai.com/codex/cloud/environments/
- `AGENTS.md` guidance for Codex: https://developers.openai.com/codex/guides/agents-md/

## GitHub Index Setup

If ChatGPT Project shows `Shphd3/Research_System` but says it is not indexed:

1. Open GitHub search in the browser.
2. Search exactly:

```text
repo:Shphd3/Research_System import
```

3. Wait about 5-10 minutes.
4. Return to ChatGPT Project and refresh the GitHub connector dropdown.
5. Test with:

```text
Use GitHub to read Shphd3/Research_System. First find PROJECT_INDEX.md, then summarize CURRENT.md with file citations.
```

If it cannot cite or find these files, the connector has not indexed the repository yet or GitHub app access is not configured for this repository.

## What "Index" Means Here

This is not a vector database that we build manually. ChatGPT's GitHub connector uses GitHub access/search to locate relevant repository content. We make this easier by keeping:

- `PROJECT_INDEX.md` at repo root
- short canonical files with stable names
- dated daily folders
- predictable meeting paths

## ChatGPT Project Usage

For high-reasoning discussion, use the ChatGPT Project named `ResearchProgress` with the GitHub connector enabled.

At the start of a serious task, ask it to read:

```text
PROJECT_INDEX.md
CURRENT.md
AGENTS.md
```

Then provide the current material:

- meeting transcript
- experiment report from remote agent
- daily card
- reading note
- PRISM draft

ChatGPT Project should only propose updates. It should not be treated as the source of truth until the user copies or delegates the update into the repository.

According to the OpenAI GitHub connector documentation, the ChatGPT GitHub app is read-only for repository analysis/search. Use Codex cloud when repository edits or commits are needed.

## Codex Cloud Usage

Use Codex cloud when the task requires repository edits:

- update templates
- create a new daily card file
- create a PRISM report folder
- revise prompt files
- update docs

Codex cloud should write under:

```text
daily_research_reports/MMDD/
```

Meeting files should go under:

```text
daily_research_reports/MMDD/meeting/
```

PRISM files should go under:

```text
daily_research_reports/MMDD/meeting/prism/
```

Core files such as `CURRENT.md` and project-local mainline/result files should be updated only when the user explicitly accepts the proposed mainline or claim change.
