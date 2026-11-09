# 公式、参数、代码与可追溯数据

当前对象与结果由[Protocol](protocol_cn.md)、[Summary](summary_cn.md)、[Detailed](detailed_cn.md)分别拥有。旧A22最后层独立编码接口预检仍保存在`provenance/interface_audit.json`；它描述原要求不匹配，不是本轮两套原生读数的失败。用户A01明确改变了这个对象。

## 从输入到数值

E16：h是block27 MLP输入，z=Top32(ReLU(Wenc h+b))，重构=decoder(z)，a_i=z_i||decoder[:,i]||。A22：x_l=(h_l−TRAINmean_l)/TRAINRMS_l，u=ReLU(Σ_l x_l E_l+b)，z_i=u_i 1[u_i Σ_l||d_li||>0.051281172782182693]。l为14个零起始奇数block，同位置可见前缀；最终层原空间feature向量v_i27=z_i TRAINRMS27 d_i27，贡献幅度a_i27=||v_i27||。**没有仅最后层encoder分支或人为置零。**

文档命中率=160个测量位置上z>0的比例；文档平均贡献=mean(a)。发现RMS_i=sqrt(mean_discoverytokens a_i²)，含零。上下文x_i=a_i/RMS_i，零RMS排除不补选。DCLM参考频率=65536个位置的命中计数/65536，与词频和强度分开。

主probe标准化+L2 logistic C=1，仅发现拟合；1000次原分割内标签置换重做筛选+读出；不足原k的draw规则BA=.5，本轮未触发。每组20随机集合保持发现命中率四分位×支持文档三分位分箱数，不放宽匹配。两角色字典内BH为主，补报四检验BH。每个feature的留出率比采用(hitsM+.5)/(hitsB+.5)，分母有效位置同为3200，0命中不写无穷。率比区间和频率误差条是描述性。

实验二s_i=sign(mean_6发现家族,2措辞[xM−xB])；每留出家族D=mean_i mean_r s_i(xMr−xBr)，U=mean_i(|xMU−xM1|+|xBU−xB1|)/2，E=D−U。对6个家族E做2000次bootstrap与64个符号翻转单侧检验。固定方向可能为0，全部候选都参与均值，不用少数激活坐标重新扩大效果。通过需两措辞总体方向正、E区间>0、BHq<.05。本轮均未满足。

## 代码与实际资产

- 执行根目录：`/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027`。
- 原生前向实现：[run_dual_forward.py](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/run_dual_forward.py)，重启恢复入口：[run_dual_forward_resume.py](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/run_dual_forward_resume.py)。原脚本冻结后未修改；恢复只导入其Runner与保存函数。
- 统计：[analyze_frozen.py](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/analyze_frozen.py)；原始归约审计：[audit_outputs.py](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/audit_outputs.py)；独立E/BA/随机分箱审计：[verify_statistics.py](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/verify_statistics.py)；画图：[render_figures.py](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/render_figures.py)。代码与权重属于执行侧，主仓只留证据。
- 文本与分割：`data/documents.jsonl`、`data/context_panel.jsonl`、`data/reference.jsonl`；完整来源/排除/分割摘要`data/source_manifest.json`。所有有词面预筛但未纳入的来源候选在`document_source_candidates.jsonl`，未按feature输出筛选。生物数学混合、代码/索引导航/不合格边界在数据构建前处理；source-window选择规则与人工式列表在`build_documents.py`，无事后文本删除。
- 全逐token稀疏原始激活：`forward/documents/*.npz`、`forward/reference/*.npz`、`forward/context/*.npz`。字段SAE/CC_ptr、ids、z为CSR式位置偏移、featureID和FP32原z；*_nmse存hook重构误差。未保存新全量原始h；本轮未做谱分析。
- 原始汇总：`forward/{documents,reference,context}_{SAE,CC}.npz`，含counts、sum_z、sum_z2、decoder_norm和有效位置数。**CC decoder_norm是最后层原空间范数**，并非所有层范数相加。`decoder_scales.npz`另外保留14层native范数与TRAIN统计，便于核查。
- 候选、所有坐标连续统计、原生贡献、归一化值、分类器参数、预测、1000置换值、20随机组ID、每家族E与方向：执行侧`analysis/`。主仓`tables/`保留完整结果与所选feature表。

| 资产 | SHA256 |
|---|---|
| Base权重（两原路径逐字节相同） | cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba |
| tokenizer.json | c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539 |
| E16 SAE | e4e2049aced8ba9a3b043bbb2b3308b497b7ec22f107531e37197873ee545b65 |
| A22 CrossCoder | 09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628 |

数据资产ID `data_a15_27_r04_domain_native_dual_20261027`；完整精度/hook/状态证据与当前访问检查见`provenance/`，不是由注册表通过推断科学结论。

## 局限与未测清单

| 内容 | 本轮状态 |
|---|---|
| 领域条件使用/固定读出/同目标编辑/最后层贡献 | 已测，见Detailed与3图 |
| 原始同token共同激活簇、decoder方向cosine簇 | 本轮未新建；旧R03定义未改写 |
| 新谱基、语义谱段、Attention、物理距离操纵 | 未测 |
| feature替换/删除、功能必要性/专家分工、训练形成原因 | 未测 |
| 全面自然语言普遍频率、源外泛化、独立双人领域标注 | 未建立 |

没有使用剩余56条预算扩样追显著。下一步测什么留待用户讨论；本轮不自动开始第三项实验。
