# Current Research Entry

Last updated: 2026-05-07

## Canonical Files

- Mainline: `mainline.md`
- Claim board: `claim_board.md`
- Current primary experiment: `experiments/E001_feature_zipf_synthetic.md`
- Current raw report: `daily_research_reports/0507/feature_zipf_synthetic_brief_report_0505.md`

## One-Sentence Mainline

Build a Hierarchical MoE route-and-expert structure that can support "learn quickly, forget less" by exploiting low-dimensional, Zipfian, and compositional feature structure rather than treating all tokens or mechanisms as flat.

## Current Safest Claim

On feature-Zipf synthetic data, Hierarchical MoE recovers part of the hierarchical computation mechanism, especially in function recovery. However, the evidence does not yet support the stronger claim that Hierarchical MoE is better than flat middle spectral MoE at sparse feature division.

## Current Bottleneck

The immediate bottleneck is to separate feature-level specialization from function-level specialization, and to explain why flat middle spectral routing currently gives the strongest sparse feature division signal.

## Today

Current task: turn the 0507 feature-Zipf synthetic experiment into mainline files, claim boundaries, and meeting-ready report materials.

Expected daily output: a compact daily report, a candidate `CURRENT.md` update if the mainline changes, and a 30 second meeting script.
