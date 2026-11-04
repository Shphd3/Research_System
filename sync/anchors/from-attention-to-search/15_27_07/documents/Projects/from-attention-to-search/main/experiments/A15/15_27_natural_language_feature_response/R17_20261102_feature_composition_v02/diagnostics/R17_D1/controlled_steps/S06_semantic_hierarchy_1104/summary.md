派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S06_semantic_hierarchy_1104/summary.md`。
[精确原始文件](../../../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S06_semantic_hierarchy_1104/summary.md)；研究修改仍回到原件。

---

# SAE combinations and semantic hierarchy: S06

Behavior/factor controls, representation combinations, then function/quality are kept separate. This round observes frozen dictionary coordinates; no causal intervention or router training occurs. These are AI operational verdicts under the registered rules; researcher acceptance and closure remain Unknown.

New bounded observations: only some member events repeat (MLPIN cat recruitment #22958 8/8, #11234 0/8; bicycle #16830 8/8). Higher within-domain overlap does not establish stable relative strengths: MLPIN vehicle has only5/8eligible heldout sibling pairs. Animal property cat behavior is3/8versus dog8/8. Common-list strict frequency matching yields0/256complete random lists, so no common-list specificity advantage over matched lists is established.

Purpose: inspect member recruitment/loss/shared use (round H1) and joint relative strength (round H2) for animal→cat/dog and vehicle→car/bicycle. Sixteen authored frames/domain, shared across domains, form16 correlated frame clusters;8 discovery/8 heldout. Explicit/synonym/property variants plus chair/stone yield384 prefixes, all retained. Both native30000/ReLU-Top32 dictionaries use the same official Qwen3-0.6B Base but different final-block tensors and unrelated feature IDs.

The bounded update is category/wording/dictionary-conditional organization. A successful explicit condition remains local unless frozen patterns and behavioral eligibility persist under lexical controls. The H1 primary contrast evaluates within-versus-cross-domain overlap, not the entire hierarchy hypothesis. H2 requires identical support on the fixed small list and>=2 active members; whole-dictionary support remains distinct.

| SAE | 大类 | 预测 | 估计 | 95%家族区间 | 可用/8 | Holm p |
| --- | --- | --- | --- | --- | --- | --- |
| ATTN_SAE | animal | H1 | 0.2212 | [0.1868, 0.2500] | 8 | 0.0020 |
| ATTN_SAE | animal | H2 | 0.0401 | [0.0186, 0.0572] | 8 | 0.0234 |
| ATTN_SAE | vehicle | H1 | 0.1341 | [0.0966, 0.1740] | 8 | 0.0020 |
| ATTN_SAE | vehicle | H2 | 0.0275 | [0.0136, 0.0444] | 8 | 0.0156 |
| MLPIN_SAE | animal | H1 | 0.1884 | [0.1508, 0.2254] | 8 | 0.0020 |
| MLPIN_SAE | animal | H2 | 0.0048 | [0.0031, 0.0065] | 7 | 0.0234 |
| MLPIN_SAE | vehicle | H1 | 0.1595 | [0.0884, 0.2416] | 8 | 0.0020 |
| MLPIN_SAE | vehicle | H2 | 0.0530 | [0.0350, 0.0711] | 5 | 0.0312 |

| SAE | 大类 | H | 显式条件 | 跨措辞 |
| --- | --- | --- | --- | --- |
| ATTN_SAE | animal | H1 | LOCAL_SUPPORT | INSUFFICIENT |
| ATTN_SAE | animal | H2 | LOCAL_SUPPORT | INSUFFICIENT |
| ATTN_SAE | vehicle | H1 | LOCAL_SUPPORT | SUPPORT_IN_THIS_PANEL |
| ATTN_SAE | vehicle | H2 | LOCAL_SUPPORT | NOT_SUPPORTED |
| MLPIN_SAE | animal | H1 | LOCAL_SUPPORT | INSUFFICIENT |
| MLPIN_SAE | animal | H2 | LOCAL_SUPPORT | INSUFFICIENT |
| MLPIN_SAE | vehicle | H1 | LOCAL_SUPPORT | SUPPORT_IN_THIS_PANEL |
| MLPIN_SAE | vehicle | H2 | INSUFFICIENT | INSUFFICIENT |

H1 estimate is the mean3 within-domain Jaccards minus mean9 cross-domain Jaccards within a frame. H2 estimate is the sibling q difference projected along its frozen discovery mean direction; q uses exact fixed-list L2. Intervals resample8 family clusters4096times. Eight explicit primary tests use Holm.

| 措辞 | 类别 | 同父二选一/8 | 四选一/8 |
| --- | --- | --- | --- |
| explicit | cat | 8 | 8 |
| explicit | dog | 8 | 8 |
| explicit | car | 8 | 8 |
| explicit | bicycle | 8 | 8 |
| synonym | cat | 7 | 7 |
| synonym | dog | 8 | 8 |
| synonym | car | 8 | 8 |
| synonym | bicycle | 8 | 8 |
| property | cat | 3 | 3 |
| property | dog | 8 | 8 |
| property | car | 8 | 8 |
| property | bicycle | 8 | 8 |

Behavior is sibling constrained continuation and four-candidate scoring, not free generation. Parents/negatives have preferences, not fabricated fine gold labels. All candidates have2tokens including period; per-token log probabilities sum in nats with no correction. Synonym/property descriptions retain lexical cues, and absolute positions can vary.

Common features and replacement patterns are reported separately from relative-strength changes. Equal recruitment/loss counts follow fixed32-positive supports. Coordinate squared differences and decoder-norm weighted activations are not semantic or output contributions. Matched random candidate failures remain explicit; shared-parent cosines have a role-reassignment structural reference. No classifier/SVD/model training. H3/H4 and real router work remain parked.

AI mechanistic intuition: relative amplitude redistribution and encoder-rank competition can coexist. The current measurements do not establish native functional use. Lexical cues, remaining template/position effects, dictionary reconstruction and finite stimulus selection remain alternatives. One next researcher decision is whether any conditional fixed-list pattern merits an independently controlled lexical/position study; no such follow-up is started.

[Complete procedure and audit](detailed.md) · [中文完整说明](detailed_cn.md) · [Literal cases and failures](casebook_cn.md) · [Protocol](protocol.md) · [Reproduction](reproduce.md)
