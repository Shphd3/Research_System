# R13复现与完整结果入口

[中文结果](summary_cn.md) · [English Summary](summary.md) · [初版协议](protocol.md) · [辅助修订](protocol_amendments.md)

实际执行目录：`/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101`。本轮新增模型前向0、GPU0。全部科学初版在pre_fit_freeze.json和fit_freeze.json固定；原protocol英中字节相同，实际结果未覆盖它们。已完成目录不重跑fit/evaluate：它们有防覆盖门槛，且旧R12生产脚本也不能直接写回。

## 数据与定义

- [初版模型／字典／缓存身份和协议配置](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R13_feature_presence_amplitude_20261101/manifest.json)
- [当前资产访问](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/audits/asset_access.json)
- [输入hash和14层／归一化／尺度绑定](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/audits/asset_identity_audit.json)
- [逐任务原文、标签、来源、位置与D/V/H](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/data/task_metadata.json)
- [全部16384独立参考频率](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/data/reference_frequency.npz)
- [D支持池与冻结k](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/audits/training_support_inventory.json)
- [完整数值规则](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/config.json)
- [拟合前冻结](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/pre_fit_freeze.json)
- [H前模型／成员hash冻结](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/fit_freeze.json)

## 读出、成员、区间与失败

- [全部条件/种子/完整组/逐类正确数/logloss](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/analysis/metrics_all_conditions.csv)
- [全部主条件中文表](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R13_feature_presence_amplitude_20261101/metrics_cn.md)
- [可见格式修正基线](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/analysis/source_format_visible_prefix.csv)
- [15主对比及全部种子/完整组配对差](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/analysis/paired_contrasts.csv)
- [逐文档配对差bootstrap原值](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/analysis/paired_bootstrap.npz)
- [每任务/种子/组的冻结ID及D正值统计](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/analysis/frozen_members.csv)
- [同维追加的实际低中高人数](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/analysis/same_dimension_member_composition.csv)
- [642主体拟合条件与开发选参](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/analysis/fit_ledger.csv)
- [648原始冻结条件模型](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/models.pkl)
- [3可见性修正模型](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/visible_metadata_models.pkl)
- [按冻结判据的全部阴性/不足状态](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/analysis/decision_rules_result.json)
- [幅值比例及无效分母率](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/analysis/amplitude_logloss_fraction.csv)
- [按H来源分层](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/analysis/source_strata.csv)
- [严格同来源位置匹配及不足](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/analysis/strict_source_position_matching.csv)
- [不看响应的匹配文档ID](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/analysis/matched_documents.csv)

## 错误与真实文本

- [逐文档全部主种子与完整组概率/正确性](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/analysis/predictions.csv)
- [每比较全部文档：修正、新错、同对、同错](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/analysis/document_error_exchanges.csv)
- [预定known/普通/反例完整前文](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/analysis/text_cases_word_audited.json)
- [z/B/A与各读出正负分数项](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/analysis/case_readout_terms.csv)
- [全部121条改变记录的真实前文与双方分数项](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/analysis/exhaustive_error_texts_word_audited.json)
- [全文阅读页](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R13_feature_presence_amplitude_20261101/text_cases_cn.md)

## 实际谱、重构与残差

- [全部16384成员×任务：出现率、正值均值、整体均值、支持/NA、单位方向与有符号贡献](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/analysis/all_member_occurrence_amplitude_direction.csv)
- [先向量求和再平方的实际组谱能量](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/analysis/actual_group_spectral_energy.csv)
- [逐PC带符号类别差与固定h分数项](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/analysis/signed_class_perPC.csv)
- [64PC段类差与分数贡献](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/analysis/signed_class_spectral_bands.csv)
- [组内/组间净交叉项、正负判别抵消](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/analysis/cancellation.csv)
- [原h、完整重构、各组与残差：固定头/重拟合、误差](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/analysis/representation_reconstruction_residual.csv)
- [固定h头逐文档判断保留与交换](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/analysis/reconstruction_document_changes.csv)
- [旧R12固定头原表精确重放](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/analysis/R12_fixed_head_exact_replay.csv)
- [谱和分数可加性数值核查](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/analysis/reconstruction_numerical_checks.csv)

## 复现方法

使用`/root/anaconda3/envs/spectral-hier/bin/python`及实际保存的NumPy/SciPy/scikit-learn环境，不能用不同NumPy的默认python直接反序列化models.pkl。步骤为prepare_audit.py→本轮协议/manifest→fit.py→evaluate.py→spectrum_supplement.py→validate_delivery.py→render_report.py；visible_metadata_audit.py是后追加的可见性修正，原基线保留。

重新完整计算时，复制精确input/config和scripts到新运行目录，把common.py中的A指向新输出；保持R12/R11/decoder/频率源hash不变，再按顺序执行，先建立新冻结；不得写回本轮或旧R12。仅重绘当前图可运行render_report.py，不拟合、不调用模型。旧R12全头精确重放只用其保存权重；当前新头训练规则不同，不把新旧比例直接合并。

脚本目录：[实际代码](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/scripts)。初版科学脚本、协议与模型hash见冻结文件；render/validate及可见性修正为后续展示/诊断，另留hash。图数据均直接来自上述表，图源hash为[figure_manifest.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/figure_manifest.json)，小型阅读图来源为[payload_manifest.json](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R13_feature_presence_amplitude_20261101/figures/payload_manifest.json)。原始数组、pickle、字体与网页不进入项目阅读目录。

## 完整性补充

[完整词形/窗口边界](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/analysis/target_word_form_audit.csv) · [所有条件和种子的逐文档概率](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/analysis/predictions_all_seeds.csv) · [所有编码/种子的修正与新错](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/analysis/error_exchanges_all_encodings_seeds.csv) · [非主比较的编码配对差](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101/analysis/descriptive_encoding_pairwise_contrasts.csv)。初始JSON的完整the字段是被A02更正的注释；阅读使用word_audited版本，原始模型和数值未变。prepare_audit.py是原始支持盘点，正式k由冻结config与协议确定，不将初步预留诊断k替代它。
