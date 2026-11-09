# R06 数据、参数、原生接口与缺项

## 实际计数
384条近距、128条条件性远距、5条检查，共517/528；新前向已经停止。64个完整措辞家族、32发现/32留出，每概念8/8，只有4概念对。全部文本240tokens、目标零起算239、近/远线索末尾223/95、d16/144。远配对中性句集合相同，移动128token块；前缀内无重复中性句。

## 读取哪些信号
E16：block27 MLP输入、FP32原生ReLU/Top32，30000坐标。A22：block1/3/.../27同位置residual-post，BF16编码、保存TRAIN中心化/RMS及门控0.051281172782182693，16384共享坐标，固定1024encoder位置；不修改编码器。CrossCoder最后层原空间贡献=z×TRAIN_RMS27×参数decoder27范数，明确不是最后层独立激活或功能重要性。沿用R04原生loader，未安装Attention接口。

Model SHA256 cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba；E16 e4e2049aced8ba9a3b043bbb2b3308b497b7ec22f107531e37197873ee545b65；A22 09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628。加载器重新校验以上大文件哈希，记录runtime及冻结buffers。

## 统计与冻结
完整定义在[冻结协议](protocol_cn.md)。每概念/字典最多8候选，发现固定方向和六版本贡献RMS；64新对象加2旧预指定，共66。近D/E/L/-L合并264检验；8家族、10000次家族重采样、256精确符号翻转、最小效应0.10、统一BH及4活跃/6正家族守卫。远52对象×3端点=156检验，全部条件性/探索性。检验假设家族效应关于边界对称；多feature相关性与有限标签/功效限制仍保留。

## 数据与计算源码
- [全部近距全文/分词/跨度/语义理由](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R06_fixed_target_semantics_20261028/data/near.jsonl)
- [预冻结远距全文](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R06_fixed_target_semantics_20261028/data/far_frozen.jsonl)
- [编辑量逐条统计](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R06_fixed_target_semantics_20261028/data/edit_amounts.csv)
- [家族/分割/语义理由](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R06_fixed_target_semantics_20261028/data/families.json)
- [发现候选及方向/尺度](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R06_fixed_target_semantics_20261028/analysis/candidate_freeze.json)
- [可读近结果与NA标记](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R06_fixed_target_semantics_20261028/analysis/near_results_readable.json)
- [可读远结果，明确条件性](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R06_fixed_target_semantics_20261028/analysis/far_results_readable.json)
- [生成文本源码](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R06_fixed_target_semantics_20261028/contexts.py)
- [构造与旧缓存审计](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R06_fixed_target_semantics_20261028/prepare.py)
- [实际原生前向](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R06_fixed_target_semantics_20261028/run_native.py)
- [冻结统计代码](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R06_fixed_target_semantics_20261028/analyze_semantics.py)
- [全部预算/失败尝试先记账](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R06_fixed_target_semantics_20261028/forward_ledger.jsonl)
- [独立离线重算审计](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R06_fixed_target_semantics_20261028/audit.json)

完整逐token CSR、全部目标坐标、逐token重构误差保存在执行目录forward/；没有覆盖旧R05缓存。原始near_results.json中零尺度对象的floor数字是排除的内部占位，不能当效应；可读JSON/CSV标NA。原始far_results.json通用helper的stable默认False不能作为独立确认状态；可读副本显式给conditional_criterion_met，不改变任何p/q或规则。见presentation_notes.json。

## 工程偏离及限制
R06前向无失败、无切换Attention实现、无额外资源和科学设置修订；全部初始冻结源码哈希与候选冻结哈希保持一致。新增的是输出可读性修正：零尺度统一标NA，远结果显式用条件性字段，保留原始诊断文件。真实例子另附预指定f8194的事后解释，标探索性，不用于新候选选择或确认。

R05遗留工程修订仍保留原文件，不据新结果改判。R05与R06同时变了文本、候选及对照，不能单因归因为固定目标。新面板相关编辑改动token中位13、两类无关为9/8，不完全匹配；AI语义审读、元文本否定、填充补偿与句序、有限目标词/foil集合仍限制含义解释。本轮没有测预测正确、模型实际利用、功能干预、一般概念模块或独立距离确认。
