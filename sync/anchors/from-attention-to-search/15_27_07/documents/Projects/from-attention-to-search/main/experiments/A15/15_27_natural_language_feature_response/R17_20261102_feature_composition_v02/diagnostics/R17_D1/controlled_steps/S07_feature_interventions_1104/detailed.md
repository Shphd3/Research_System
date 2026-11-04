派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S07_feature_interventions_1104/detailed.md`。
[精确原始文件](../../../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S07_feature_interventions_1104/detailed.md)；研究修改仍回到原件。

---

# Detailed: S07

# S07: combination interventions and native decoding

S06 was completed, independently audited and packaged before this supplement. All original inputs/caches/candidates/results remain unchanged. This intervention-unseen supplement uses original observationally exposed heldout families; no hidden semantic confirmation claim. Parameters stay frozen.

There is a small local effect of the Attention animal relative-pattern direction: opposite-patternalpha.5reduces correct-sibling margin by.01236nats averaged over8families; same-member norm-matched shuffled patterns reduce it by.00613. Difference.00623,95%family interval[.00135,.01340],Holm p=.03125. All16texts remain correct. Other-domain scores also move, so this is not a pure semantic conversion. Attention vehicle shifts oppose the predicted margin loss; MLP animal fails the comparator test and MLP vehicle has only5/8eligiblefamilies.

Deleting large common groups usually increases correct margins (.849/1.493nats for MLP animal/vehicle, respectively) and changes broad vocabulary distributions. Every common-group strict frequency/intensity deletion comparator fails matching, so deletion specificity remains insufficient. Equal-norm random additions are separately named, not misrepresented as matched deletions. Stable observational coactivation is therefore not equivalent to necessity for candidate discrimination.

Injection is h'=h+Wdecoder(z'-z), bias cancelled and original reconstruction residual retained. Common patterns and recruit/loss groups are selected only from the original64explicit discovery rows.96unchangedheldoutprefixes cover64explicit(alllabels) and32propertyfineconditions.14976actualconditions include deletion/count/norm controls, strengthalpha0/.25/.5/1, same-member shuffled/own-side/other-member controls and single-member localization. Report full2token candidate scores, correct margin, full-vocabulary first-word ranks/probabilities,top20+remaining mass,entropy/KL and normalized4-sequence probabilities.

The final-block tail is exact for these post-attention single-prefix-position edits, verified against12fullhookforwards (max6.44e-6nats). Period terms are invariant under this architecture-specific intervention. Every96nativebaseline matches S06exactly. Offline checks preserve original FP32 arithmetic, no tolerance relaxation. Edited latent targets need not equal re-encoded features; the claim concerns actual decoder-direction sensitivity, not unique natural mechanisms or MoE expert dispatch. Researcher acceptance and closure Unknown.

| SAE | 大类 | 干预 | 原始边际损失 | 相对对照差[95%区间] | 合格家族/8 | Holm p | 裁决 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ATTN_SAE | animal | strength | 0.01236 | 0.00623 [0.00135, 0.01340] | 8 | 0.03125 | LOCAL_DIRECTION_SPECIFIC_EFFECT |
| MLPIN_SAE | animal | strength | 0.00241 | -0.00597 [-0.01571, 0.00405] | 6 | 1.00000 | NOT_SUPPORTED_BY_PRIMARY |
| ATTN_SAE | animal | delete | -0.04532 | NA [NA, NA] | 0 | 1.00000 | INSUFFICIENT_MATCH_OR_SUPPORT |
| ATTN_SAE | vehicle | delete | -0.07467 | NA [NA, NA] | 0 | 1.00000 | INSUFFICIENT_MATCH_OR_SUPPORT |
| ATTN_SAE | vehicle | strength | -0.00276 | -0.00373 [-0.00541, -0.00197] | 8 | 1.00000 | NOT_SUPPORTED_BY_PRIMARY |
| MLPIN_SAE | animal | delete | -0.84929 | NA [NA, NA] | 0 | 1.00000 | INSUFFICIENT_MATCH_OR_SUPPORT |
| MLPIN_SAE | vehicle | delete | -1.49317 | NA [NA, NA] | 0 | 1.00000 | INSUFFICIENT_MATCH_OR_SUPPORT |
| MLPIN_SAE | vehicle | strength | -0.08476 | -0.11220 [-0.14623, -0.06980] | 5 | 1.00000 | INSUFFICIENT_MATCH_OR_SUPPORT |

| SAE | 大类 | 对照 | 条件数 | 发现频率/强度合格 | 同成员支持保持 | 实际范数比合格 |
| --- | --- | --- | --- | --- | --- | --- |
| ATTN_SAE | animal | delete_matched | 80 | 64 | 54 | 1 |
| ATTN_SAE | animal | norm_random_add | 80 | 80 | 80 | 39 |
| ATTN_SAE | animal | strength_shuffle | 16 | 16 | 16 | 16 |
| ATTN_SAE | animal | strength_own | 16 | 16 | 16 | 11 |
| ATTN_SAE | animal | strength_other | 16 | 0 | 4 | 12 |
| ATTN_SAE | vehicle | delete_matched | 48 | 32 | 21 | 2 |
| ATTN_SAE | vehicle | norm_random_add | 48 | 48 | 48 | 35 |
| ATTN_SAE | vehicle | strength_shuffle | 16 | 16 | 16 | 16 |
| ATTN_SAE | vehicle | strength_own | 16 | 16 | 16 | 13 |
| ATTN_SAE | vehicle | strength_other | 16 | 0 | 12 | 10 |
| MLPIN_SAE | animal | delete_matched | 64 | 48 | 23 | 4 |
| MLPIN_SAE | animal | norm_random_add | 64 | 64 | 64 | 52 |
| MLPIN_SAE | animal | strength_shuffle | 16 | 16 | 13 | 16 |
| MLPIN_SAE | animal | strength_own | 16 | 16 | 13 | 16 |
| MLPIN_SAE | animal | strength_other | 16 | 0 | 5 | 15 |
| MLPIN_SAE | vehicle | delete_matched | 64 | 32 | 26 | 1 |
| MLPIN_SAE | vehicle | norm_random_add | 64 | 64 | 64 | 43 |
| MLPIN_SAE | vehicle | strength_shuffle | 16 | 16 | 13 | 16 |
| MLPIN_SAE | vehicle | strength_own | 16 | 16 | 13 | 16 |
| MLPIN_SAE | vehicle | strength_other | 16 | 0 | 0 | 13 |

The complete owned execution ledger, figure explanations, all competing controls, raw cases, counterexamples and posthoc reencoding diagnostic are in [Detailed Chinese companion](detailed_cn.md). Exact frozen definitions are in [Protocol](protocol.md); all raw14976rows and full candidate rank/probability tables are portable. No new primary selection followed effects. [Reproduction and exclusions](reproduce.md).

Posthoc control-geometry audit: the two-member Attention-vehicle list has only one angular degree of freedom at fixed norm. Some matched shuffles coincide with or reverse actual target perturbations. The contrast concerns these chosen directions, not arbitrary independent compositional changes. Category differences can therefore reflect list dimension/control sensitivity. No original statistic or selection changed; per-text delta cosines are retained.
