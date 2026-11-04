派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/provenance/A02_qualified_data_cn.md`。
[精确原始文件](../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/provenance/A02_qualified_data_cn.md)；研究修改仍回到原件。

---

# R11 A02：三域输入数据资格

[English](A02_qualified_data.md) · [执行修订](../protocol_A02_execution_cn.md)

**450篇全新的原始文档家族已通过资格审计，数学、生物、物理各150篇。** 文档、标签和划分在用新激活筛选成员之前冻结。原主题、文体、平台和独立留出配额全部保留。科研接受Unknown。

| Domain | Split | Families | Expository | QA | Measured positions |
|---|---|---:|---:|---:|---:|
| math | discovery | 60 | 45 | 15 | 9600 |
| math | development | 30 | 22 | 8 | 4800 |
| math | heldout | 60 | 45 | 15 | 9600 |
| biology | discovery | 60 | 45 | 15 | 9600 |
| biology | development | 30 | 22 | 8 | 4800 |
| biology | heldout | 60 | 45 | 15 | 9600 |
| physics | discovery | 60 | 45 | 15 | 9600 |
| physics | development | 30 | 22 | 8 | 4800 |
| physics | heldout | 60 | 45 | 15 | 9600 |

每篇输入192个真实token，不加聊天模板或BOS，分析第32–191位置，共160处，均值包含零。每域发现60篇、开发30篇、留出60篇；留出再分30篇熟悉平台的新家族、30篇新平台家族。新平台未进入任一域发现／开发，也未在旧120篇出现。每个留出来源层至少4个平台；每平台不超过相应划分／领域的25%。六个主题在每域发现、开发、留出分别各10、5、10篇。每个被选平台至少覆盖两个领域。

独立一遍、不见激活的AI阅读共核查1002个候选窗口，730个通过、272个排除；不声称人工审核。经家族、近重复和平台资格筛选后，660个候选进入固定配额、按家族哈希排序的选择，round05得到450篇最优可行组合。8篇另行核查的工程试读来自发现／开发平台，与450篇及旧文档家族分离，不计科学样本。首份未核查450篇组合中300篇通过、150篇排除，未运行该组合。

原文章、整本书／课程、原问答线程是家族单位。核查合并了DOI／文章／图注别名、牛津全局论文编号、维基移动版／镜像和整书课程路径；Springer、Nature、BMC和SpringerOpen合并为同一平台。排除与旧120篇、独立参考输入及新样本的完全重复窗口和token五元组Jaccard≥0.8近重复。全部排除、改标与理由保留。

来源为固定版本公开DCLM原文与公开科学、参考和问答文章。这是按配额构造的样本。词汇、格式、主题、发表时间仍可能随领域变化；新来源留出检验所抽来源层的迁移，不单独识别“来源效应”，也不证明模型预训练从未见过原文。

原网页与提取版本留在执行目录。针对明确正文节点去除目录表和分享控件，再取连续192token正文窗口；Tao来源中的数学图片保留原有alt公式文字。每篇保留token ID、原文、位置、来源哈希、标签和划分。

数据资产：`data_a15_27_r11_qualified_three_domain_A02_20261030`。Manifest SHA256：`c7d6abb9ad79ca2e732cdeeb3966812ffac4d4f90d54e7a11dc2757092f781c2`。

[450篇清单](../../../../../../../../../UNAVAILABLE.md) · [资格审计](../../../../../../../../../UNAVAILABLE.md) · [全部阅读记录](../../../../../../../../../UNAVAILABLE.md) · [输入候选池](../../../../../../../../../UNAVAILABLE.md)。

实际选中片段仍含部分标题、目录与站点导航残留；这些是原样输入的一部分，未根据响应再清洗。格式及来源风格解释仍须保留。
