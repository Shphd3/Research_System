# Current Research Mainline

Last updated: 2026-05-07

## Mainline

Build a Hierarchical MoE route-and-expert structure that can support "learn quickly, forget less" by exploiting low-dimensional, Zipfian, and compositional feature structure rather than treating all tokens or mechanisms as flat.

## Core Hypothesis

If representations contain shared/common components plus tail or mechanism-specific low-dimensional components, then a well-designed hierarchical MoE should separate common computation from specialized expert computation and show measurable functional specialization, especially on middle and rare mechanisms.

## Most Important Evidence

- `daily_research_reports/0504/synthetic_mechanism_group_report_0504.md`: controlled synthetic mechanism recovery supports partial alignment between hierarchical structure and the generated mechanism, while showing current routing is not yet fully recovered.
- `daily_research_reports/0504/overall_plan_v4.md`: finalizes the cleaner synthetic recovery setup: hierarchical additive data, linear routing mainline, shared training protocol, and explicit metrics.
- `daily_research_reports/0428/current_status_brief_report_20260428.md`: synthetic natural Zipfian hierarchy results show oracle top-1 has strong potential, but learned top-1 routing has not yet established causal advantage over random routing.

## Current Bottleneck

The main open question is not whether hierarchical structure can be useful in principle. The bottleneck is whether learned routing can reliably recover useful mechanism structure beyond random or oracle diagnostic controls, and whether the evidence supports a claim stronger than partial specialization.

## Today

Current task: maintain a lightweight Codex-centered research workflow that keeps daily work anchored to the mainline and trains concise advisor-facing explanation.

Expected daily output: a compact daily report, a candidate `CURRENT.md` update if the mainline changes, and a 30 second meeting script.
