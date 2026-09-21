# Conversation Memory: 0921-表征分析

Conversation name: 0921-表征分析
Processed by: Codex (harness: Codex desktop; model: unknown)
Created at: 2026-09-21T05:00:00Z
Latest update at: 2026-09-21T05:08:08Z
Continues from: `.research/memory/conversations/0920-sae表征空间审计/memory.md`
Environment: `repo=/data/250010109/Research_System` `exec=/data/250010109/MoE_Router`; both roots readable.

## 2026-09-21T05:00:00Z -- 领域主线组会重构、真实激活折线与交接

- Summary: 研究者要求紧急重构组会，暂不主讲特别构造关系和不同语序/复述实验，聚焦“SAE正则后是否让不同领域分得更开”，并解释S7/SALL原子差距、Top-K=32合理性、CKA标定、同模型跨层测试、训练演化及原实验Agent后续任务。已读取来源累计memory、通过read_thread读取任务`01a0bd8d-fe25-7003-8c9a-15af54823d7f`（host `remote-ssh-codex-managed:mig`），再核对Focus/Anchor/E06 Protocol与E06—E08合格运行根。报告是AI解释草案，不拥有科学批准。
- Evidence navigation: 三批既定运行的本地terminal/collection/analysis均PASS；此次未查询远端状态。领域结论须同时看线性可读性与B/W：21B第8层均值SALL有小幅准确率正差，但B/W低于Dense；S7原子更集中却领域可读性更差。具体数值与边界在新会议稿和合格JSON中，不由memory拥有。此前旧报告的主要激活统计来自P关系面板，新稿严格使用N8对应统计；三条件排序缓存的样本ID、输入哈希、词元位置逐一一致。S7指重加权续训21B，不能与新从零S7或旧原版曲线混接。
- Artifacts: `daily_research_reports/0921/focus_meeting_sae_domain_separation_cn.md` 是本次领域组会入口，含四段式正文、测试覆盖矩阵、测量决策建议、按优先级交接清单和8分钟讲述顺序。`figures/domain_01...04*.png/.pdf` 分别是领域读出与几何、领域训练轨迹、真实1—128名激活折线、子空间直觉与证据对照；`figures/domain_figure_manifest.json` 记录来源哈希和配对验证；`report_assets/build_domain_meeting_figures.py` 只读已有合格结果及缓存。旧会议稿、Focus、Anchor和Protocol未修改。
- Decisions and boundaries: 已落实领域为本次讲述主线、折线优先、P/N8不混面板、稀疏得分质量不当语义/重构能量。AI建议不用通用CKA阈值，利用已有全局/类内置换并补采样不确定性；建议先补21B N8同模型8×8跨层比较，保留均值与末词；K=32保留为训练预算、最优性未知。多子空间及SAE特征对应未直接检验，实际模型使用未干预验证。上述新增分析建议与科学最小效应阈值尚未由研究者确认，不从本memory取得执行授权。未附独立“这张图”，报告明确只能对照旧图框架和本次假设，不能保证另一个未见原图逐项覆盖。
- Current work: 组会基本材料与交接清单已写出，图由现有缓存生成，四个顶层段落和本地链接通过检查。没有新模型前向、字典/主干训练、远程提交、跨任务发送、commit或push。E06—E08正式Summary缺失、旧Focus/Anchor和部分Detailed仍写无结果的冲突已在稿中列为交接P0，未替研究者更新机制判断。当前领域小差值没有现成N8配对区间，不能称确认改善。
- Next action: 原实验Agent先读取本稿4.6交接清单，补P0结果记录与N8配对统计最小实现计划；若N8逐题预测未保存，须从已有池化缓存复现冻结C的探针，不能重选超参数。随后按需做N8原子领域/位置分层与21B同模型跨层定位。唯一AI建议的下一决策是：经来源、尺度和不确定性标定后，是否仍值得直接检验领域子空间。若仅剩局部可读性或观察器变化，就不升级语义子空间/功能使用主张；新的低秩拟合、干预或昂贵运行先按所属合同明确范围。
- References: `daily_research_reports/0921/focus_meeting_sae_domain_separation_cn.md` 拥有本次派生阅读与未批准建议；`daily_research_reports/0920/focus_three_model_sae_representation_audit.md` 及其A15_17 Anchor拥有原科学边界；E06/E07/E08各自Protocol拥有执行范围。合格证据根分别为`/data/250010109/MoE_Router/experiments/20260920_sae_representation_21b_audit/runs/full_4x5090_retry2_20260921T0200Z/`、`/data/250010109/MoE_Router/experiments/20260920_sae_representation_15b_early_audit/runs/full_15b_4x5090_20260920_wave1/`、同执行包`runs/full_early_4x5090_20260920_wave1/`；第一批21B两个失败根不得混用。

## 2026-09-21T05:08:08Z -- 按新增要求完成补充实验科学内容

- Summary: 研究者追加“继续分析，完成报告和补充实验内容书写”。已在原领域会议稿中补充真实预处理、谱与观察器边界，并新增`daily_research_reports/0921/sae_domain_supplementary_experiments_cn.md`，把补实验写成A领域差异标定、B原子/位置/跨层定位、C条件性领域子空间检验。每部分含目的、假设、数据/统计、竞争解释、结果分支与停止标准；均为`AI_PROPOSED_NOT_RUN`，不是新Protocol或执行批准。
- Analysis clarification: 分类器实际使用fit均值中心化和单一全局RMS归一化，不可把S7下降简单归于整体幅值。`mean_vector_norm`是均值向量范数，不是样本范数均值。无32断崖不证明K太小，非入选得分尾部也不等于可恢复语义信息。不同子空间可有相同类均值，且不一定全局线性可分，所以现有B/W与分类并不直接检验子空间并集；附录C用留出投影及匹配容量/随机分组对照补这一环，并区分子空间存在与SAE改善两个假设。
- Implementation handoff: 已核实完整N8原生池化缓存可用于A/B/C，观察器有前128名得分但只有前32名ID，K>32重构及完整逐词元原生子空间仍缺字段。新增领域/位置统计须逐shard把`token_local_row`映射到全局记录；旧`load_observer`仅拼接局部索引，不能直接拿来做新标签映射。N8逐题预测缺失，建议复现已冻结C，不重新挑选。科学最小效应阈值、C的主秩/多秩解释与计算预算仍是提案，不借memory填成确认。
- Current work: 四张新图与PNG/PDF输出、来源清单、报告/附录本地链接和脚本哈希已检查；原子缓存逐token身份验证PASS。交付包含主报告、补充实验附录、图和本次memory。没有执行补充探针拟合、重采样、跨层新统计、PCA、模型加载、新提取或远程任务；本次仅读既有指标/源码并汇总已有rank缓存制图。原对话memory的已有工作区修改未动，未commit/push。
- Next action: 原实验Agent读取本次报告和附录，先处理现有结果记录与A/B缓存分析范围，再由研究者决定是否推进C；对旧test新分析必须标探索，对缺字段/资源未实测明确标不足。不要把本次“报告完成”解读为“补充实验已完成”。
- References: `daily_research_reports/0921/focus_meeting_sae_domain_separation_cn.md`为组会入口；`daily_research_reports/0921/sae_domain_supplementary_experiments_cn.md`为唯一补充内容详细入口；`daily_research_reports/0921/figures/domain_figure_manifest.json`为新图谱系；E06合格运行根、原`analyze_primary.py`、`analyze_geometry.py`、`analyze_observer.py`、`observe_online.py`拥有本次核对的字段与真实计算口径。原Focus/Anchor/Protocol未变化。
