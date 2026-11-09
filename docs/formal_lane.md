# Formal lane appendix

Load this only when a result is promoted (meeting conclusion, paper, long-term
map) or the researcher asks for a formal record, meeting brief, handoff, sync or
publication. The evidence standard is the same as the exploration lane; only
the record form differs. Promotion cites the exploration log's raw data instead
of rewriting history.

## Record ownership

| Record | Owns |
|---|---|
| `PROJECTS.md` / project roadmap | Project access, active question set, navigation |
| Anchor | Sole scientific design (eight sections, via `problem-anchor-writer`) |
| Protocol | Exact experiment contract, approval and amendments |
| Summary (+ `_cn`) | Purpose, necessary model, hypothesis, bounded conclusion, supporting analysis |
| Detailed / execution record | Setup, provenance, deviations, results, execution state |
| Story / Graph / sync / final report | Derived reading; never new authority |
| `docs/execution_envelope.md` | Profiles, images, submission, execution certificates |

- The Focus layer was retired on 2026-11-09 (originals archived, old links
  resolve via `docs/research_locations.json`). A question's next decision lives
  in `PROJECTS.md` (active set), its explore log, and Anchor section 8. Where an
  older skill or reference says "Focus", read it as that active-question entry
  plus Anchor section 8; do not create new Focus files.
- A completed Anchor round records question/hypothesis, setup/controls, data,
  confirmation split, result or `NOT RUN`, and insight/boundary/next decision.
- Canonical formal records are English with `_cn.md` companions unless the
  researcher chooses Chinese-only for that record.
- Question closure and its single final report need a researcher-confirmed
  bounded answer; negative or insufficient results are not polished into support.

## Meetings

A requested brief goes in `daily_research_reports/MMDD/meeting_report/` and is
linked from that day's index. Order: purpose, 2–3 conclusions (as knowledge
updates), hypotheses (expected knowledge update, not expected numbers),
analysis with decisive raw values, Q&A, `AI 建议` next steps. Drafts produced by
`tools/meeting_digest.py` stay pending until the researcher confirms them.

## Sync, handoff and publication (explicit trigger only)

- Anchor reading sync (`docs/anchor_sync.md`), handoff packages and external
  sync run only when the researcher asks in the current conversation. There is
  no standing sync authorization.
- Reuse `tools/build_reading_bundle.py`; preserve source bytes and pending
  states; verify links before delivery. Prefer a manifest of source paths and
  hashes over copying bytes when the reader has repository access.
- Commit, push, publish and Graph edits need an explicit request. Before a
  commit run `python tools/check_git_payload.py` and relevant tests.

## Storage

Track text, scripts, configs and small provenance manifests. Raw outputs,
caches, checkpoints and large payloads stay execution-side (`/data/.../MoE_Router`).
Cleanup moves payloads to a dated archive with a manifest; it never deletes the
only copy of frozen evidence.

## Writing references

[report_writing.md](report_writing.md) and [markdown_math.md](markdown_math.md)
apply to formal records and briefs. Changed math needs
`python tools/check_markdown_math.py <files>`.
