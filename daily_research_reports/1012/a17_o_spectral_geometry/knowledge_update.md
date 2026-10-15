# O spectral supplement: knowledge update

[中文](knowledge_update_cn.md) · [Canonical Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R04_o_spectral_geometry/summary.md) · [Detailed](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R04_o_spectral_geometry/detailed.md) · [Protocol](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R04_o_spectral_geometry/protocol.md)

## Purpose

Determine whether forgetting versus retention is adequately described by different leading O-matrix spaces, as a bounded part of the question of shared versus conditional learning. This is a derived reading note, not scientific approval.

## Model

The original Qwen3-0.6B experiment trained only last-layer Q/K/V/O. Old mode uses甲first/乙last. A learns the same mapping in the new mode; B learns a reversed mapping there; C starts from the same acquired-old state and mixes old supervision with reversed-new supervision. C is not joint training from Base. For list red/blue/green, old甲 selects red, whereas B/C new甲 selects green; the visible mode makes both requirements compatible.

Analyze saved O and its displacement from the common acquired-old O at240/1200. SVD pairs input/output directions with strengths; E16 is squared leading16 energy fraction; U/V overlap measures input/output subspace proximity, not rule function. Three continuations share one old state.37 CPU FP64 SVDs, six numerical tests and independent Gram/540-overlap/81-behavior checks passed. No training, new forward or TEST. At1200 B sees24000 new answers; C sees12000 old+12000 new.

## Hypothesis

Candidate: stable distinct O-displacement spaces accompany forgetting and retention. Rival: old supervision, optimization history and Q/K/V readout background determine different functions that coarse O geometry cannot characterize. Shared inherited weights may also dominate full-W similarity.

## Conclusion

1200 combined-DEV continuation-order means; CE and margins are in nat:

| Branch | Old CE / accuracy / rule margin | New CE / accuracy / rule margin |
| --- | --- | --- |
| A consistent | 0.000041 / 100% / +23.146 | 0.000041 / 100% / +22.851 |
| B reversed | 15.819206 / 0% / −15.793 | 0.031350 / 99.25% / +16.190 |
| C joint reversed | 0.004841 / 99.83% / +18.106 | 0.009108 / 99.67% / +15.650 |

B/C full-O U16/V16 overlaps are0.9493/0.9474, displacement overlaps0.8216/0.4230. Displacement E16 is80.852%/81.908%, relative old norm7.149%/8.522%, signed displacement cosine0.6170. A/B and A/C displacement V16 overlaps are only0.0646/0.0835: B/C are closer to each other despite sharply different old performance.

## Analysis and mainline update

Full-O proximity cannot substitute for old function. C moves farther from the old matrix yet retains old rules, contradicting a simple endpoint-magnitude explanation here. In the three-order mean comparison, B/C input-space differences do not exceed within-branch order variation: right overlaps B/B0.2457 and C/C0.2296 are below B/C0.4230. These O spectra and rank8/16/32 spaces do not establish a stable branch partition; all-parameter partitions were not tested. Fixed ranks8/16/32 also differ, so16 is not uniquely meaningful.

![Spectra](/data/250010109/MoE_Router/experiments/20261012_a17_o_spectral_geometry/runs/spectral_20261012_r04_v1/figures/01_o_singular_spectra.png)

X is singular index; Y is raw or Frobenius-normalized singular value. Separate full W from displacement D, which contains the actual continuation change.

![Energy and overlap](/data/250010109/MoE_Router/experiments/20261012_a17_o_spectral_geometry/runs/spectral_20261012_r04_v1/figures/02_top16_energy_and_subspaces.png)

X is branch/pair and step; Y is energy percent or overlap0–1. Points are order means and whiskers are ranges, not confidence intervals.

![Behavior](/data/250010109/MoE_Router/experiments/20261012_a17_o_spectral_geometry/runs/spectral_20261012_r04_v1/figures/03_old_new_behavior.png)

X is branch and step; Y is CE, accuracy or rule margin. Upper/lower rows are old/new tasks: these are the functional outcomes the parameter explanation must explain.

R03 already measured O-background dependence: rolling O back in B gives old32.67%/new68.71%; inserting B O alone into the old Q/K/V background gives old98.71%/new1.29%. This supplement narrows a simplistic geometric partition story and directs attention to how mode conditions restrict actual predictive effects. A shared module can realize both mappings here; separate-module net utility is still unmeasured.

AI suggestion, one next decision: cross-swap B/C O under fixed readout backgrounds to test actual prediction consequences. This new intervention is not executed. Researcher mechanism acceptance/closure remain Unknown. Figures are execution-host payloads, with [provenance](/data/250010109/MoE_Router/experiments/20261012_a17_o_spectral_geometry/runs/spectral_20261012_r04_v1/figures/provenance.json), not a newly uploaded portable Web package. No commit/push this turn.
