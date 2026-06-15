# 0615 Expert-Spectrum Sync Package

## Read Order

1. `meeting_brief.md`
2. `meeting_talk_plan.md`
3. `06_01_common_filtered_expert_spectrum_router_initialization_anchor.md`
4. `summary.md`
5. `detailed.md`
6. `sources/0614_meeting_brief_anchor2_final.md`

## Scope

这个包记录 0615 会议需要看的 A06_01 当前状态。0614 的 early-training common-logit 结果只作为背景支撑放入，不替代 A06_01 的结论。

## Main Conclusion

去共同方向后的专家谱线性初始化能改善第 0 步路由均匀性，但不能阻止第 10 步负载集中。当前最可能的瓶颈不是“专家谱完全没有信息”，而是从谱分数到线性 top-1 router 的实现桥太弱。

## Boundary

证据只覆盖 DCLM packed text 上的小型随机初始化 Qwen-style top-1 MoE：6 层、8 专家、无负载均衡损失、训练 0--300 步。它不能证明专家谱无用，也不能直接迁移到预训练、top-2/top-4 或大模型 MoE。

## Included Files

- `meeting_brief.md`：0615 中文会议简报，使用模板英文标题。
- `meeting_talk_plan.md`：会上的讲法、边界和导师追问应答。
- `06_01_common_filtered_expert_spectrum_router_initialization_anchor.md`：当前项目 anchor 副本。
- `summary.md`：实验结果第一阅读路径。
- `detailed.md`：完整实验记录。
- `sources/0614_meeting_brief_anchor2_final.md`：0614 支撑结论。
- `figures/`：A06_01 文档引用的三张图。
- `tables/`：会议简报和实验文档使用的关键小表。

## Excluded

raw logs、checkpoints、datasets、完整 run 目录、临时输出和实验代码都没有放入这个 sync 包。
