# 本轮仓库来源与代码读取记录

仓库：`Shphd3/Research_System`。以下来自本轮通过 GitHub 连接读取的文件内容；运行资产仍位于研究者执行环境，本包不包含权重和原始激活。

## 结果与身份

`daily_research_reports/0921/meeting_domain_final/备查与证据_cn.md`

- 文件 blob SHA：`5590c0c55491cbc5c7d4d11a10a1d75287f204e7`。
- 本轮读取第 1—65 行，核对四读点领域准确率、配对区间、B/W 分解、词面基线及数据／模型身份。
- 关键读取：21B 第 8 层正文均值 Dense/SALL/S7 准确率为 87.0625%/87.8125%/74.9375%；SALL−Dense 为 +0.7500 个百分点，[−0.5625,+2.0625]；S7−Dense 为 −12.1250，[−14.2500,−10.0625]。
- SALL 的 B/W 从 Dense 的 0.468927 变为 0.430392；第 8 层末词元的 SALL−Dense 为 +2.0000，[+0.1250,+3.8766]。
- 文件把 S7 记作系数从 1 改为 0.1 的重加权谱系，说明旧 PDF 的“当前系数 1”标注不可直接沿用。

以上为文件报告内容，不是本包重新采集或独立重算。fileciteturn27file0L2-L2

## 代码与配置：已读，不夸大复用资格

| 路径 | blob SHA | 本次读取与可复用边界 |
|---|---|---|
| `AGENTS.md` | `e40472e7ced8f33cf447443acee373d791eb7e2c` | 本轮重读前 105 行；其余规则已在当前对话读取。生成独立交付，不更改科学状态或提交仓库。 |
| `docs/training_reuse_index.md` | `da5183fec5ee33073456cdde7b6de7569cb88346` | 索引与运行边界；不将其中旧串联 SAE 训练包移植为本轮旁路分析。 |
| `daily_research_reports/0920/docs/atten执行资料/config.yaml` | `6f4b62d79c1c4001c1a7a93d7e8809fedbf29847` | 旧 N8、线性分类器和聚类建议参数；其中仍有 null，不能把它称为本轮已解析配置。 |
| `daily_research_reports/0920/docs/atten执行资料/pool_attention.py` | `74f793311487e1103213974553ae8e88b05308fd` | 已读完整函数和合成测试；它只做掩码汇聚，不能证明输入张量来自正确模块。 |
| `daily_research_reports/0921/report_assets/build_domain_meeting_figures.py` | `cc99dcab626e964e3263606ea82a31d306e9d5db` | 已读第 1—135 行；确认正式结果 JSON 路径、PASS 检查和原子缓存身份规则。它不加载模型。 |

17B 审计的独立源码／清单本轮未取得；按上传报告提供的 `analysis/result.json` 入口由执行 Agent 本地解析，不虚构其字段名。旧早期资产审计只用来识别 1,200 条旧自然面板、norm2 读点和新 N8 的区别，不用其旧状态覆盖后来的完成记录。

## 方法接口的外部核对范围

只核对实现接口，没有用外部文献改写本项目的科学主张：

- 多类别逻辑回归的 L2 配置、C、收敛和新版参数方式：官方 scikit-learn 文档。citeturn221104view2
- K-means 的固定初始化次数、按簇内平方距离选择初始化及预测接口：官方 scikit-learn 文档。citeturn193805view1
- 调整兰德指数的簇编号不变性及随机一致性含义：官方 scikit-learn 文档。citeturn221104view0
- M2D2 的来源登记、按领域配置和 `text` 字段：数据集官方数据卡；该页面也提示旧加载脚本需要额外执行审查。citeturn193805view2

完整重建与统计规则是本次提出的实验规格，不是声称旧实验已经采用这些精确规则。所有软件版本须由实际执行环境记录，不要求为本轮盲目升级环境。
