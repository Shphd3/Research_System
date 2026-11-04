派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R15_20261102_natural_phenomena_output_geometry_v1/reproduce.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R15_20261102_natural_phenomena_output_geometry_v1/reproduce.md)；研究修改仍回到原件。

---

# R15复算与原始材料

先读[完整报告](report_cn.md)和[实际版本与修订](detailed_cn.md)。本目录不存大缓存、权重或训练环境；它们留在执行侧。科研接受Unknown。

## 可核对原始表
- [actual_change_direct_head_audit.csv](../../../../../../../../UNAVAILABLE.md)
- [band_case_metrics.json](../../../../../../../../UNAVAILABLE.md)
- [descriptive_token_category_document_effects.csv](../../../../../../../../UNAVAILABLE.md)
- [descriptive_token_category_summary.csv](../../../../../../../../UNAVAILABLE.md)
- [development_actual_changes.csv](../../../../../../../../UNAVAILABLE.md)
- [development_associations.csv](../../../../../../../../UNAVAILABLE.md)
- [development_document_effects.csv](../../../../../../../../UNAVAILABLE.md)
- [development_matched_positions.csv](../../../../../../../../UNAVAILABLE.md)
- [development_phenomenon_support.csv](../../../../../../../../UNAVAILABLE.md)
- [development_selection_candidates.csv](../../../../../../../../UNAVAILABLE.md)
- [discovery_actual_changes.csv](../../../../../../../../UNAVAILABLE.md)
- [discovery_associations.csv](../../../../../../../../UNAVAILABLE.md)
- [discovery_cards.jsonl](../../../../../../../../UNAVAILABLE.md)
- [discovery_document_effects.csv](../../../../../../../../UNAVAILABLE.md)
- [discovery_matched_positions.csv](../../../../../../../../UNAVAILABLE.md)
- [discovery_phenomenon_support.csv](../../../../../../../../UNAVAILABLE.md)
- [discovery_positive_strength_cards.jsonl](../../../../../../../../UNAVAILABLE.md)
- [document_source_index.csv](../../../../../../../../UNAVAILABLE.md)
- [h_direction_document_bootstrap_stability.csv](../../../../../../../../UNAVAILABLE.md)
- [head_gain_reference.json](../../../../../../../../UNAVAILABLE.md)
- [historical_basis_comparison.csv](../../../../../../../../UNAVAILABLE.md)
- [nonadditive_residual_ledger.csv](../../../../../../../../UNAVAILABLE.md)
- [pca_document_bootstrap_stability.csv](../../../../../../../../UNAVAILABLE.md)
- [phenomenon_output_gain_summary.csv](../../../../../../../../UNAVAILABLE.md)
- [postnorm_band_readout_geometry.csv](../../../../../../../../UNAVAILABLE.md)
- [representation_head_spectra.csv](../../../../../../../../UNAVAILABLE.md)
- [representation_head_subspace_overlap.csv](../../../../../../../../UNAVAILABLE.md)
- [selected_feature_document_support.csv](../../../../../../../../UNAVAILABLE.md)
- [signed_direction_associations.csv](../../../../../../../../UNAVAILABLE.md)
- [signed_direction_document_effects.csv](../../../../../../../../UNAVAILABLE.md)
- [signed_direction_sensitivity.csv](../../../../../../../../UNAVAILABLE.md)
- [signed_direction_validation.csv](../../../../../../../../UNAVAILABLE.md)
- [signed_sensitivity_document_effects.csv](../../../../../../../../UNAVAILABLE.md)
- [source_and_length_coverage.csv](../../../../../../../../UNAVAILABLE.md)
- [spectra_bands.csv](../../../../../../../../UNAVAILABLE.md)
- [text_case_selection.json](../../../../../../../../UNAVAILABLE.md)
- [text_case_slot_eligibility.json](../../../../../../../../UNAVAILABLE.md)
- [three_feature_geometry_views.csv](../../../../../../../../UNAVAILABLE.md)
- [validation_actual_changes.csv](../../../../../../../../UNAVAILABLE.md)
- [validation_associations.csv](../../../../../../../../UNAVAILABLE.md)
- [validation_band_map.csv](../../../../../../../../UNAVAILABLE.md)
- [validation_document_effects.csv](../../../../../../../../UNAVAILABLE.md)
- [validation_matched_positions.csv](../../../../../../../../UNAVAILABLE.md)
- [validation_phenomenon_support.csv](../../../../../../../../UNAVAILABLE.md)
- [validation_selected_verdicts.csv](../../../../../../../../UNAVAILABLE.md)
- [validation_source_robustness.csv](../../../../../../../../UNAVAILABLE.md)

## 完整执行来源

执行根：`/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R15_20261102_natural_phenomena_output_geometry_v1`；[输入文档](../../../../../../../../UNAVAILABLE.md)、[全部可见前文位置](../../../../../../../../UNAVAILABLE.md)、[配置](../../../../../../../../UNAVAILABLE.md)、[原始输入冻结](../../../../../../../../UNAVAILABLE.md)、[最终标签1.2](../../../../../../../../UNAVAILABLE.md)、[验证解释冻结](../../../../../../../../UNAVAILABLE.md)。每个figure的源表、对象、单位与资格在[图清单](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R15_20261102_natural_phenomena_output_geometry_v1/provenance/figure_manifest.json)。

## 已有缓存上的CPU复算

```bash
cd /data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R15_20261102_natural_phenomena_output_geometry_v1
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2
# Discovery/development stages write their own tables; preserve new versions before methodological changes.
/root/anaconda3/envs/spectral-hier/bin/python scripts/analyze.py discovery
# validation_selection_frozen.json already exists; do not reselect explanations after reading validation.
/root/anaconda3/envs/spectral-hier/bin/python scripts/analyze.py validation
/root/anaconda3/envs/spectral-hier/bin/python scripts/geometry.py
/root/anaconda3/envs/spectral-hier/bin/python scripts/signed_directions.py
/root/anaconda3/envs/spectral-hier/bin/python scripts/signed_robustness.py
/root/anaconda3/envs/spectral-hier/bin/python scripts/validate.py
/root/anaconda3/envs/spectral-hier/bin/python scripts/render.py
```


`extract.py`为新前向代码，不因本阅读文件自动启动；输入源、哈希和当前CPU环境均需按manifest恢复。A6本轮始终探索；重算不能消除事后指标资格。NO_SUPPORTED_DEV_INTERVENTION是门槛分支，不得重算成已做因果干预。
