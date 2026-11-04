派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R13_feature_presence_amplitude_20261101/reproduce.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R13_feature_presence_amplitude_20261101/reproduce.md)；研究修改仍回到原件。

---

# R13复现与完整结果入口

[中文结果](summary_cn.md) · [English Summary](summary.md) · [初版协议](protocol.md) · [辅助修订](protocol_amendments.md)

实际执行目录：`/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_feature_presence_amplitude_20261101`。本轮新增模型前向0、GPU0。全部科学初版在pre_fit_freeze.json和fit_freeze.json固定；原protocol英中字节相同，实际结果未覆盖它们。已完成目录不重跑fit/evaluate：它们有防覆盖门槛，且旧R12生产脚本也不能直接写回。

## 数据与定义

- [初版模型／字典／缓存身份和协议配置](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R13_feature_presence_amplitude_20261101/manifest.json)
- [当前资产访问](../../../../../../../../UNAVAILABLE.md)
- [输入hash和14层／归一化／尺度绑定](../../../../../../../../UNAVAILABLE.md)
- [逐任务原文、标签、来源、位置与D/V/H](../../../../../../../../UNAVAILABLE.md)
- [全部16384独立参考频率](../../../../../../../../UNAVAILABLE.md)
- [D支持池与冻结k](../../../../../../../../UNAVAILABLE.md)
- [完整数值规则](../../../../../../../../UNAVAILABLE.md)
- [拟合前冻结](../../../../../../../../UNAVAILABLE.md)
- [H前模型／成员hash冻结](../../../../../../../../UNAVAILABLE.md)

## 读出、成员、区间与失败

- [全部条件/种子/完整组/逐类正确数/logloss](../../../../../../../../UNAVAILABLE.md)
- [全部主条件中文表](metrics_cn.md)
- [可见格式修正基线](../../../../../../../../UNAVAILABLE.md)
- [15主对比及全部种子/完整组配对差](../../../../../../../../UNAVAILABLE.md)
- [逐文档配对差bootstrap原值](../../../../../../../../UNAVAILABLE.md)
- [每任务/种子/组的冻结ID及D正值统计](../../../../../../../../UNAVAILABLE.md)
- [同维追加的实际低中高人数](../../../../../../../../UNAVAILABLE.md)
- [642主体拟合条件与开发选参](../../../../../../../../UNAVAILABLE.md)
- [648原始冻结条件模型](../../../../../../../../UNAVAILABLE.md)
- [3可见性修正模型](../../../../../../../../UNAVAILABLE.md)
- [按冻结判据的全部阴性/不足状态](../../../../../../../../UNAVAILABLE.md)
- [幅值比例及无效分母率](../../../../../../../../UNAVAILABLE.md)
- [按H来源分层](../../../../../../../../UNAVAILABLE.md)
- [严格同来源位置匹配及不足](../../../../../../../../UNAVAILABLE.md)
- [不看响应的匹配文档ID](../../../../../../../../UNAVAILABLE.md)

## 错误与真实文本

- [逐文档全部主种子与完整组概率/正确性](../../../../../../../../UNAVAILABLE.md)
- [每比较全部文档：修正、新错、同对、同错](../../../../../../../../UNAVAILABLE.md)
- [预定known/普通/反例完整前文](../../../../../../../../UNAVAILABLE.md)
- [z/B/A与各读出正负分数项](../../../../../../../../UNAVAILABLE.md)
- [全部121条改变记录的真实前文与双方分数项](../../../../../../../../UNAVAILABLE.md)
- [全文阅读页](text_cases_cn.md)

## 实际谱、重构与残差

- [全部16384成员×任务：出现率、正值均值、整体均值、支持/NA、单位方向与有符号贡献](../../../../../../../../UNAVAILABLE.md)
- [先向量求和再平方的实际组谱能量](../../../../../../../../UNAVAILABLE.md)
- [逐PC带符号类别差与固定h分数项](../../../../../../../../UNAVAILABLE.md)
- [64PC段类差与分数贡献](../../../../../../../../UNAVAILABLE.md)
- [组内/组间净交叉项、正负判别抵消](../../../../../../../../UNAVAILABLE.md)
- [原h、完整重构、各组与残差：固定头/重拟合、误差](../../../../../../../../UNAVAILABLE.md)
- [固定h头逐文档判断保留与交换](../../../../../../../../UNAVAILABLE.md)
- [旧R12固定头原表精确重放](../../../../../../../../UNAVAILABLE.md)
- [谱和分数可加性数值核查](../../../../../../../../UNAVAILABLE.md)

## 复现方法

使用`/root/anaconda3/envs/spectral-hier/bin/python`及实际保存的NumPy/SciPy/scikit-learn环境，不能用不同NumPy的默认python直接反序列化models.pkl。步骤为prepare_audit.py→本轮协议/manifest→fit.py→evaluate.py→spectrum_supplement.py→validate_delivery.py→render_report.py；visible_metadata_audit.py是后追加的可见性修正，原基线保留。

重新完整计算时，复制精确input/config和scripts到新运行目录，把common.py中的A指向新输出；保持R12/R11/decoder/频率源hash不变，再按顺序执行，先建立新冻结；不得写回本轮或旧R12。仅重绘当前图可运行render_report.py，不拟合、不调用模型。旧R12全头精确重放只用其保存权重；当前新头训练规则不同，不把新旧比例直接合并。

脚本目录：[实际代码](../../../../../../../../UNAVAILABLE.md)。初版科学脚本、协议与模型hash见冻结文件；render/validate及可见性修正为后续展示/诊断，另留hash。图数据均直接来自上述表，图源hash为[figure_manifest.json](../../../../../../../../UNAVAILABLE.md)，小型阅读图来源为[payload_manifest.json](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R13_feature_presence_amplitude_20261101/figures/payload_manifest.json)。原始数组、pickle、字体与网页不进入项目阅读目录。

## 完整性补充

[完整词形/窗口边界](../../../../../../../../UNAVAILABLE.md) · [所有条件和种子的逐文档概率](../../../../../../../../UNAVAILABLE.md) · [所有编码/种子的修正与新错](../../../../../../../../UNAVAILABLE.md) · [非主比较的编码配对差](../../../../../../../../UNAVAILABLE.md)。初始JSON的完整the字段是被A02更正的注释；阅读使用word_audited版本，原始模型和数值未变。prepare_audit.py是原始支持盘点，正式k由冻结config与协议确定，不将初步预留诊断k替代它。
