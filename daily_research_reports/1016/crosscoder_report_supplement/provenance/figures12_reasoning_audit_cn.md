# 图 1、图 2 定义与推断审计

审计范围仅限已有结果的重新呈现；未访问训练参数、重新训练或修改建图。按 `research-reasoning-auditor` 和 `visual_evidence_contract` 检查。

- 图 1 的对象是 186 个完整关系组。重新读取 `full_group_controls.csv`，验证 186 行 `qualified=True` 且 `strict_qualified=True`；对 `observed_strict_SD` 和 `meanmatched_strict_SD` 逐组等权重算，均与 `full_repair_summary.json` 一致。没有用旧的 142 组子集或平滑版本。两柱不含误差条；“更小”是本次统计描述，不升级为排除了 phi 选择偏好。
- 图 2 的对象是同一低频 feature 名单上的条件预测损失。读取 54 行，确认三规则、三种子、六测点一一配对，所有起点相同，横轴 `tokens_seen=step×256`。低频 feature、低频输出 token 与知识准确率没有互换。种子细线和均值粗线都保留，总体损失另表。
- 观察并未被期望反向选择：三种规则最终均高于原模型，关系分发在本轮没有取得预定收益。这不证明所有同频学习方案无效，也不从图 1 直接推出图 2 必须改善。
- 已实际查看两张最终 PNG：中文正常，轴名、刻度、图例和数值不裁切；白底、大字号、固定蓝橙绿配色，没有双纵轴、长句曲线标注、复杂拼图或误差条。PDF 由同一 Matplotlib figure 写出，未单独进行 PDF 渲染核验。

字体为既有运行资源 `/data/250010109/Research_System/daily_research_reports/0921/report_assets/fonts/NotoSansCJKsc-Regular.otf`，其文件字节与 SHA256 见 `source_manifest.json`；本次不复制或打包字体。
