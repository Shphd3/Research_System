# 共享更新与干扰机制：统一阅读入口

日期：2026-09-26。处理者：Codex。这里集中本次会话相关的研究思路、机制解释、原始指导和实验阅读副本。“所有文档”的范围是这轮共享更新与原子分析材料，不是整个研究仓库。新增解释使用中文；副本保留来源语言和结论。

**思维锚点：在明确模型状态、学习目标、参数和比较基线后，解释 A 的学习怎样通过共享计算帮助或伤害 B，再判断哪些数据属性与识别工具能够刻画这种作用。**

当前证据支持共同强原子、可复现领域偏好和部分方向的局部收益选择性。所测完整更新的12个跨领域均值仍为帮助。本轮补充理论并完成受控方向实验：方向改变削弱帮助，但目标均值仍获益，完整实际伤害判据未通过。当前缺口是可跨记录复现的有害干扰载体、造成它的数据条件，以及SAE的独立识别能力。原有建议是当时的AI分析。本轮新增受控机制实验由随后明确的用户委托授权；未创建Focus或改变项目科研判断。

## 1. 从哪里开始读

**2026-09-26后续补充：**研究者已明确委托补理论与初步实验，并允许直接提交。当前优先顺序如下，原有目录和历史副本继续保留。

1. **仔细阅读与审计：**[核心问题与机制思路](02_core_question_and_mechanism_cn.md)。只抓问题、解释、区分证据与认识更新；第8节列出三个审计问题。
2. **核对本轮补了多少：**[受控方向实验中文结果](experiments/20260926_direction_conflict/summary_cn.md)。
3. **理解公式时再读：**[理论推导](03_theory_derivation_cn.md)，从参数梯度连接到表征变化与任务后果。
4. 实验细节备查：[Protocol](experiments/20260926_direction_conflict/protocol.md)、[Detailed](experiments/20260926_direction_conflict/detailed.md)。

### 此前材料的阅读顺序

1. **看已经发生的事实：** [本轮中文结果副本](experiment_copies/20260926_atom_mechanism/summary_cn.md)。
2. **看你的顺序是否合理、还缺什么：** [机制分析与白话术语](01_mechanism_analysis_cn.md)。第2节讲顺序，第3—6节讲定义和缺环，第7节讲实际对照，第8节给机制假说的区分检验草稿。
3. **回查导师原话：** [0924会议记录副本](background_copies/0924_mentor_guidance.md)。
4. **需要核对实现时再读：** [实验契约副本](experiment_copies/20260926_atom_mechanism/protocol.md)与[完整证据副本](experiment_copies/20260926_atom_mechanism/detailed.md)。

推荐的思考顺序是：**工作定义与初步观察 ↔ 理论候选 → 受控机制验证 → 数据属性与适用范围 → SAE等识别方法 → 训练方法。** 理论与数据互相修正，SAE可以较早参与观察；它的识别能力必须另行验证。

## 2. 文档归档位置

```text
shared_update_reasoning/
  00_reading_guide_cn.md                  本入口
  01_mechanism_analysis_cn.md            上一版解释与原子对照术语
  02_core_question_and_mechanism_cn.md   本轮思路，优先阅读审计
  03_theory_derivation_cn.md             理论推导与有限步长边界
  experiments/20260926_direction_conflict/ 本轮唯一正式设计、契约、结果与证据
  background_copies/                    原始指导和此前讨论材料
  experiment_copies/
    20260926_structure_update/           前一轮结构与一步更新记录
    20260926_atom_mechanism/             本轮原子画像与干预记录
    future/README_cn.md                  后续实验副本的收录位置与规则
  source_manifest.json                  来源、时间、源文件与副本摘要值
```

这个目录是阅读集合。原始科研记录继续拥有其设计、结果与执行状态。副本有明确来源头和摘要值，可追溯复制时版本；不要在副本里修改实验结论或批准状态。新增解释没有取代正式研究设计。本轮新实验的唯一正式记录按研究者要求放在本集合的 experiments/20260926_direction_conflict/；experiment_copies/仍仅存此前实验的阅读副本。

图片继续位于当天的 `../figures/`，副本使用日期内相对路径引用它们；没有把原始数据、缓存、模型或日志复制进阅读集合。精确来源清单见[source_manifest.json](source_manifest.json)。

## 3. 已收录的实验材料

| 实验及作用 | 第一阅读面 | 核查材料 |
|---|---|---|
| 原始表征与一步更新：建立同数据的结构和后果对应 | [中文结果](experiment_copies/20260926_structure_update/summary_cn.md)、[英文结果](experiment_copies/20260926_structure_update/summary.md) | [Detailed](experiment_copies/20260926_structure_update/detailed.md) |
| 原子画像与方向干预：检验局部收益选择性 | [中文结果](experiment_copies/20260926_atom_mechanism/summary_cn.md)、[英文结果](experiment_copies/20260926_atom_mechanism/summary.md) | [Anchor](experiment_copies/20260926_atom_mechanism/anchor.md)、[Protocol](experiment_copies/20260926_atom_mechanism/protocol.md)、[Detailed](experiment_copies/20260926_atom_mechanism/detailed.md) |
| 此前原子结果后的路线解释 | [中文路线](experiment_copies/20260926_atom_mechanism/01_route_and_knowledge_update_cn.md)、[英文路线](experiment_copies/20260926_atom_mechanism/01_route_and_knowledge_update.md) | 其下一步是当时AI建议；当前思维顺序解析见本文第1节 |

新增受控方向实验见[中文结果](experiments/20260926_direction_conflict/summary_cn.md)及[Detailed](experiments/20260926_direction_conflict/detailed.md)，已完成4卡实验，完整实际伤害判据未通过。

Anchor副本中的“注册时尚未运行”是历史时间点，不能用来判断现在是否完成；请看 Summary 和 Detailed。Protocol中的参数形状按其 A2 修订读取。数学原子10171、4949的排除只针对数学目标集合角色，Detailed和Summary已说明，不能理解为它们都未参与任何比较。

## 4. 已收录的背景与讨论材料

| 材料 | 阅读用途与状态 |
|---|---|
| [0924导师指导](background_copies/0924_mentor_guidance.md) | 原始附件的阅读副本；转写有歧义处不自行补成导师的精确数学定义 |
| [早期思路纠偏与聊天计划](background_copies/01_reasoning_and_conversation_plan_cn.md) | 历史讨论框架；当时“未取得附件”等状态不代表现在仍未取得 |
| [早期组会图稿](background_copies/02_structure_update_meeting_figures_cn.md) | 原始表征、输入与梯度连接的解释；不是新的正式Focus |
| [此前研究推理审计](background_copies/03_prior_reasoning_audit.md) | 历史AI分析；结果与当前状态回查实验所有者 |
| [此前必交图与机制草稿](background_copies/04_prior_figure_and_mechanism_draft.md) | 历史AI方案，保留原有来源标记；不能当作新实验结果或授权 |

原文引用的其他日期结果保留到其正式来源的链接，未把跨课题的整套资料重复复制。现有材料中的未决判断、旧建议和转写歧义继续标为历史或未知。

## 5. 后续实验文档放在哪里

本轮正式记录：[Anchor](experiments/20260926_direction_conflict/anchor.md)、[Protocol](experiments/20260926_direction_conflict/protocol.md)、[中文Summary](experiments/20260926_direction_conflict/summary_cn.md)、[英文Summary](experiments/20260926_direction_conflict/summary.md)、[Detailed](experiments/20260926_direction_conflict/detailed.md)。后续新实验可直接在本集合的experiments目录维护唯一正式记录；已有其他正式来源的，继续只收录阅读副本。

下面是本集合初建时的收录规则与未执行状态，保留为历史说明；本轮实际状态以上述新实验记录为准。

[后续副本入口](experiment_copies/future/README_cn.md)已经建立。未来正式实验先在所属问题的原始位置维护 Anchor、Protocol、Summary 和 Detailed，再在 `experiment_copies/<日期_实验名>/` 放带来源的阅读副本，并更新本索引和来源清单。

尚未设计或运行的实验不会提前生成带有结果或批准状态的占位 Protocol。当前只有[机制假说与检验建议](01_mechanism_analysis_cn.md#8-下一步要验证的机制ai建议草稿不是已执行实验)。AI建议的下一决策是确定输入复用与纠错要求的关系，是否作为下一次局部机制区分检验的对象；没有在此改变科研状态或提交新任务。
