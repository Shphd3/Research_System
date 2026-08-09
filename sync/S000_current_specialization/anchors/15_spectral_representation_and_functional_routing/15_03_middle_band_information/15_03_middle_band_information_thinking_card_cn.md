---
thinking_card_id: 15_03_middle_band_information
status: human_judgment_transcribed_formalization_authorized
human_language: zh
formalization_authorized: true
execution_authorized: false
source: researcher_instruction_2026-08-09
---

# Thinking Card：middle-band 的平稳曲线是真稳定还是聚合假象

> 本卡逐项转写研究者 2026-08-09 的本轮指令。研究者判断保留在“我的判断”；AI 新增的操作定义只放在“AI 审核”并标为提案。

## 我的判断

- **所属研究方向或父问题：**A15_05_01 的冻结 Qwen3-8B 参数谱语义位置审计；这是独立的 middle-band 子问题，不并入 A15_04 shared-tail 实验。
- **具体现象：**把每层本地 MLP 参数谱等分为 16 段后，F2--F8 的归一化语义方差曲线随深度看起来变化最小。
- **机制猜想：**Unknown。需要区分中段真的稳定，还是归一化、middle 内部相反方向迁移、或跨层方向不稳定造成的秩平均假象。
- **最强替代解释：**绝对方差随深度增长但被总方差归一化抵消；F2--F8 内部左移与右移相互抵消；或每层占据不同的 middle 方向，按本地秩平均后才显得平。
- **最不确定的一环：**“曲线平”是否同时意味着绝对幅度、middle 内部秩形状和跨层方向身份都稳定。
- **什么证据会改变判断：**在同一 512 条样本和实际 $\Delta n$ 上，同时看到绝对每方向方差、全谱归一化份额、F2--F8 分段曲线，以及 local/shared middle 相对等维 Haar 随机空间的跨层捕获。
- **当前阻塞的不确定性：**尚无一个指标把绝对尺度变化与 F2--F8 内部形状变化分开，也没有证据证明相同秩段在不同层对应稳定方向。
- **为什么现在需要裁定：**在问 middle 承载什么信息、是否值得选择或用于更好路由之前，先确认“稳定 middle”是不是可识别的几何对象。
- **当前唯一决策：**先建立独立子 Anchor 和一个 `DRAFT_NOT_EXECUTABLE` Protocol 供审核；未经明确批准不实现、不 smoke、不 full run。
- **我依据的材料：**`daily_research_reports/0809/focus.md`、A15_02_06 Protocol/Summary/Detailed、A15_02_07 TAX/COMP 结果、A15_04 Anchor/Protocol。

## AI 审核

- **唯一未定义对象或隐藏假设：**“真实稳定”需要一个预先确认的实用等价阈值；研究者尚未指定允许多大的绝对 per-direction 漂移。主语义对象也需确认是 conditional-fine，还是要求 coarse/fine 共同通过。
- **最小反例或区分实验：**即使早晚层的 F2--F8 七段绝对曲线和归一化曲线完全相同，只要 local middle 超过 Haar、而用其他层构造的 shared middle 仍落在 Haar 区间，就足以反驳“同一 middle 信息跨层稳定”；相同秩曲线可以由层间旋转的方向产生。
- **需要补充或核验的来源链接：**现有 A15_02_06 原始 $\Delta n$ 文件是否保留全 4096 维向量；A15_04 已确认旧 response 文件只保留本地投影坐标，因此跨层 shared-middle 需要独立、可审计的 raw-$\Delta n$ 来源。
- **AI 建议：**pursue，定位为 `metric audit / root-cause audit`。主指标提议为 F2--F8 七段绝对 per-direction 方差的早晚层对数漂移；共同尺度与内部形状是其解析分解，shared-middle 对 Haar 是方向身份门，不是第二主指标。

## 我的确认

- **保留或修改后的判断：**研究者已明确授权建立独立 middle-band 子锚点和不可执行 Protocol；没有确认 AI 提议的等价阈值、主语义角色、随机次数或执行面。
- **是否允许写入正式 anchor：**yes；只允许写研究设计和待审 Protocol，不允许实现或运行。

本卡不是 Anchor、Protocol 或结果报告；正式文件只链接本卡，不复制它。
