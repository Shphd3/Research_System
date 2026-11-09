# Summary: A17_04_E04 implementation, Smoke and one-seed acquisition qualification

[中文](summary_cn.md) · [Child Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/subanchors/17_04_02_shared_routed_budget_anchor.md) · [Protocol](protocol.md) · [Detailed](detailed.md)

The authorized qualification task completed; the formal three-seed comparison was not submitted. Researcher mechanism and utility judgment remain Unknown.

## 1. Purpose

Qualify the three main allocation designs and two supporting controls, and check whether the specified low-rank updates learn both conditional rules before a formal separation-utility comparison.

## 2. Model

Freeze the entire acquired-old Qwen3-0.6B and train only final-layer Q/K/V/O factors. Main shared/private/hybrid arms each store163,840 trainable parameters, with16/8/12 active slots per input. Shared8/12 controls store81,920/122,880. All execute dense rank16 products. Mode1 maps甲FIRST/乙LAST; mode2 reverses this. Every arm uses the same joint20-answer batch,10 per mode, answer-only CE and fixed AdamW.

Seed29 only. Each arm completes8 Smoke steps and external exact replay. Acquisition starts fresh and checks240; because qualification fails, all continue from actual240 states to1200. Each pilot processes24,000 targets,12,000 per mode. Rule margin is correct-versus-opposite endpoint log probability, in nat; accuracy uses full-vocabulary argmax. Qualification requires all eight mode/command/unseen-panel cells≥95%.

## 3. Hypothesis

Engineering expects matched counts/exposure, prefix-only masks, frozen originals and exact replay. The acquisition candidate expects this factor budget/optimizer to learn both mappings. Effective rank and factorized optimization are live alternatives; failure cannot be called contradictory tasks or evidence against all separation. The formal utility hypothesis needs qualified three-seed evidence and is not tested here.

## 4. Conclusion

1. All five engineering Smokes pass, but all five acquisition configurations fail the registered floor. Budget, identical exposure, zero-update no-op, original/mask freeze, private isolation and five external replays pass. Main forward/backward matrix FLOPs differ by0.00002723%, below1%. [Smoke](/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/runs/qualification_20261012T053102Z/smoke_verdict.json) and [independent audit](/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/runs/qualification_20261012T053102Z/independent_results.json) own evidence.
2. At1200, old rules remain near-perfect but new rules are not uniformly learned. Hybrid has the highest mean new accuracy89.75%, while its weakest cell is78.5%. Every arm remains below95% in at least one cell. Combined panels give:

| Arm | Old accuracy | New accuracy | Old CE | New CE | Old margin | New margin | Weakest cell |
|---|---:|---:|---:|---:|---:|---:|---:|
| Fully shared16 | 99.750% | 87.500% | 0.011851 | 0.332006 | 11.581 | 5.929 | 75.00% |
| Private8/8 | 100.000% | 84.375% | 0.000054 | 0.411580 | 21.647 | 2.918 | 71.50% |
| Shared8 + private4/4 | 100.000% | 89.750% | 0.000852 | 0.275144 | 15.131 | 5.006 | 78.50% |
| Shared8 control | 99.125% | 72.750% | 0.033712 | 0.649917 | 9.342 | 3.236 | 45.50% |
| Shared12 control | 99.500% | 84.375% | 0.017920 | 0.416978 | 11.091 | 4.732 | 69.00% |


Each mode has800 DEV answers; panels are equally weighted; CE and margins are nat. [Independent raw-record reconstruction](/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/runs/qualification_20261012T053102Z/independent_results.json) owns the table.

3. Do not proceed directly to the original formal configuration. All arms also failed qualification at240;1200 cannot substitute for the fixed primary point. This is usable implementation without a qualified low-rank learning setting, not a rejection of MoE or proof that low rank cannot solve the task elsewhere.

## 5. Analysis

Candidate access is already high. Hybrid new candidate mass98.63% accompanies CE0.275144, of which0.260104 is within-candidate choice loss; remaining failure concerns choice rather than only access. Positive average margins do not establish every conditional rule. Hybrid improves mean new accuracy by2.25pp over shared16, while private loses3.125pp; neither unqualified one-seed contrast adjudicates utility. Private isolation is an architectural check, not a gain discovery.

Two equivalent prepared views and10 checkpoint families/55 actual states are registered and verified. All share one old model and exposed DEV; no fresh confirmation. [Artifact manifest](artifact_manifest.json) binds evidence. AI suggestion: retain data/code, distinguish fixed-rank update-scale calibration from fixed-optimizer rank expansion before formal comparison. Neither repair ran. The next researcher decision is which bounded qualification repair to adopt.
