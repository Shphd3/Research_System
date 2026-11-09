# R04 Summary: similar O geometry does not establish retained old rules

## 1. Purpose

The parent question asks when conditional prediction requirements can share parameters and when conditional separation is useful. This supplement asks whether B, which forgets the old mapping after reversed-new learning, and C, which retains both mappings under joint supervision, occupy clearly distinct O-matrix geometries. A is the consistent-new reference. This is an existing-checkpoint analysis, not additional training or a utility comparison of separate modules.

## 2. Model

R02 trained only the final-layer Q/K/V/O of Qwen3-0.6B Base. Three continuation orders29/43/71 share one acquired-old endpoint. Old mode1 uses甲first/乙last; new mode2 is consistent for A and reversed for B/C. C continues from that same acquired-old endpoint with mixed old/new supervision, rather than training jointly from Base.

The1024×2048 O matrix maps attention readout c into output a=Wc. W0 is the acquired-old O; D_X=W_X-W0 is the continuation displacement. Analyze full W and D separately at fixed steps240/1200, with1200 primary. SVD decomposes a matrix into paired input/output directions with strengths. E16 is the first16 squared singular values divided by total squared energy. Left U and right V are O-output and O-input coordinate subspaces; overlap is mean squared principal cosine. They are not old-sensitive gradient directions or identified functional modules. See [Protocol](protocol.md) for exact formulas.

Recompute existing exposed-DEV records: CE is negative log correct-answer probability; accuracy is full-vocabulary top1; rule margin is correct minus opposite endpoint logit in nat. Report unfamiliar order, unfamiliar combination, and equal-weight combined panels. No new model forward or TEST.

## 3. Hypothesis

Candidate H: B/C leading O-displacement spaces may stably distinguish forgetting from joint retention. The strongest rival is that changed supervision, exposure, and optimization history alter Q/K/V–O computation, while coarse O geometry is insufficient to characterize compatibility. B has24000 new answers at1200; C has12000 old+12000 new. Their contrast is not an order-only intervention. Subspace overlap also loses signs: D and -D have identical spectra/subspaces.

## 4. Conclusion

All37 SVDs and independent numerical checks passed. **The result weakens full-O similarity or a leading16-dimensional subspace as a sufficient indicator of old-rule retention. These O spectra and rank8/16/32 statistics do not establish a stable branch partition; partitioning of all parameters was not tested.** The following are equal continuation-order means at1200, combined DEV; CE/margins are in nat.

| Branch | Old CE | Old accuracy | Old rule margin | New CE | New accuracy | New rule margin |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Acquired old | 0.000691 | 100% | +17.525 | — | — | — |
| A consistent | 0.000041 | 100% | +23.146 | 0.000041 | 100% | +22.851 |
| B reversed | 15.819206 | 0% | −15.793 | 0.031350 | 99.25% | +16.190 |
| C joint reversed | 0.004841 | 99.83% | +18.106 | 0.009108 | 99.67% | +15.650 |

| Geometry | A | B | C |
| --- | ---: | ---: | ---: |
| Full W first16 energy | 5.450% | 5.456% | 5.525% |
| Displacement D first16 energy | 93.361% | 80.852% | 81.908% |
| Displacement norm / old W0 norm | 4.136% | 7.149% | 8.522% |

| Same-order rank16 overlap | A–B | A–C | B–C |
| --- | ---: | ---: | ---: |
| Full W left/output | 0.9300 | 0.9143 | 0.9493 |
| Full W right/input | 0.9298 | 0.9124 | 0.9474 |
| D left/output | 0.5588 | 0.6218 | 0.8216 |
| D right/input | 0.0646 | 0.0835 | 0.4230 |

Three bounded updates follow. First, near-identical full-O spaces accompany a99.83-point old-accuracy difference. W0 first16 energy is5.402%; inherited full-matrix structure masks changes. Second, larger displacement and lower full-W overlap with W0 do not predict more forgetting here: C moves8.522% versus B7.149%, with old-relative left/right overlaps0.9124/0.9114 versus0.9368/0.9366, yet retains old rules. Third, the right-side displacement difference is not a stable task partition: in the three-order mean comparison, same-branch cross-order right overlaps are B0.2457 and C0.2296, below same-order B/C0.4230. B/C are also closer than A/B or A/C. The registered branch-separation-beyond-within-branch-variation condition is not met.

These are observations and bounded AI interpretations. Researcher mechanism acceptance and question closure remain `Unknown`; separate-module net utility is `NOT MEASURED`.

## 5. Analysis

This supplement stays on the mainline by testing whether geometric separation explains incompatible prediction behavior. C shows that the current shared module can realize both mappings. B forgetting is neither a capacity impossibility nor something established by full-weight distance or coarse leading subspaces. The functional question becomes which new changes are restricted to the new visible mode and which also change old-mode selection.

Existing [R03](../R03_mechanism_audit/summary.md) finite interventions supply causal-participation evidence, unlike this observational supplement. Rolling O back in B raises old accuracy from0% to32.67% while lowering new from99.25% to68.71%. Inserting B's O alone into the old background leaves old98.71% and new1.29%. O acts differently under different Q/K/V readout backgrounds. The exact attention relation

\[
\Delta a=\Delta Wc_0+W_0\Delta c+\Delta W\Delta c
\]

connects O change ΔW and readout change Δc; this algebra alone does not identify which component causes forgetting. Keep finite output interventions and geometric measurements at their distinct evidence levels.

Fixed rank8/16/32 B/C displacement overlaps are left0.5934/0.8216/0.8339 and right0.3409/0.4230/0.4334. Individual rank16 right overlaps are0.5080/0.5036/0.2573. Full-W relative16/17 gaps average only0.18%–0.25%, whereas D gaps average3.50%–5.95%. Rank16 is not uniquely meaningful. [Detailed](detailed.md) contains per-order, per-panel, earlier-state and verification evidence.

**AI suggestion, one next decision:** whether to cross-swap B/C O under the same readout backgrounds to test the functional consequence of the observed geometry. This would extend R03 and separate O change from Q/K/V background; this new intervention was not executed here.

[Knowledge update](../../../../../../../../../daily_research_reports/1012/a17_o_spectral_geometry/knowledge_update.md) · [Artifact manifest](artifact_manifest.json)
