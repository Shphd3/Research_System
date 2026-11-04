派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_24_frequency_composition_common_path/common_optimizer_coupling_20261022/dataset_guide.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_24_frequency_composition_common_path/common_optimizer_coupling_20261022/dataset_guide.md)；研究修改仍回到原件。

---

# Dataset identity for A15_24_01

[中文](dataset_guide_cn.md) · [Result](summary.md) · [Procedure and evidence](../../../../../../../../UNAVAILABLE.md)

This round reuses the Tulu SFT data and frozen Qwen3-0.6B block-28 residual-post cache from the original frequency-routing experiment. It creates no new split, feature roster or CrossCoder. Only the residual adapter experts and common branch train; the cached input, final norm and prediction head remain frozen.

| Split | Dialogues | Valid answer targets | Source JSON SHA256 |
|---|---:|---:|---|
| train | 1024 | 85548 | `5530f9676c3d7941150e404c045ad62815a11310d8b1ec4904c209121ddb8ad5` |
| eval | 256 | 22446 | `63a31b625a8b55c709c777d50f12db44fa8ca05d6b611f8a1d2998485d320962` |
| dev | 128 | 10340 | `56d6f03425dafffe7b5345e472a4e3d7c932a5914761d6867ef9791e07ac5b0a` |

Targets are answer-only, shifted exactly once; qualification found no prompt or padding targets. Normalized prompt overlap between the three splits is zero. Near-duplicate independence and overlap with Base pretraining remain Unknown. DEV was exposed in earlier work and is exploratory, with no new confirmation set.

Each training model consumes the same 85,548 targets once: 167 updates of 512 targets and one update of 44. Final DEV is evaluated only after all four models complete, at the fixed step-168 checkpoint.

The TRAIN-derived low-frequency roster contains 1,694 CrossCoder features. In DEV, 838 have at least one active position; 856 have none and remain NA. No low feature has support of at least 20 positions. Their union covers 1,701 distinct positions among 10,340 targets. Feature macro NLL first averages losses within each supported feature, then averages the 838 means equally. The position-union mean instead counts each covered position once. Shared dialogues and overlapping memberships prevent treating features or positions as independent observations.

Registered input identities:

- `data_tulu_sft_route_20261019t012300z`
- `representation_tulu_sft_route_20261019t012300z`
- `model_qwen3_0p6b_base`
- `tokenizer_qwen3_0p6b_base`
- `analysis_crosscoder_frequency_composition_common_path_20261019t164834z`

Current access and label checks are saved in [input receipt](../../../../../../../../UNAVAILABLE.md), [qualification](../../../../../../../../UNAVAILABLE.md) and [independent recomputation](../../../../../../../../UNAVAILABLE.md). Raw text, activations and checkpoints stay in execution storage. The source hashes above identify exact input JSON files without redistributing those payloads.
