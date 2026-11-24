
## 2026-11-12 | 启动归因分析与正对照
- A5 收益缩小与最低频残余优势的分析落在 `/data/250010109/MoE_Router/experiments/20261112_a5_shrink_attribution/`。同一步数和同一学习程度对齐分别报告。
- 按本轮附件仅授权 R1 短训，另做已有存档的离线读数。判定阈值写入分析目录的 `protocol_cn.md`。研究者判断 Unknown。

## 2026-11-12T10:27:37Z — 归因与 R1 交付

- Summary: M1 的 2000→3816 端点领先约 196→182 步，NLL 差收窄主要由曲线变平解释。11446 总体接近持平，最低频三档仍获益。19076 逐位置配对支持原生总体反超。M2 功能集中度未追上 A5。M3 两个坐标都看到后段相对他组帮助减少，下一词功能坐标 A+B 从领先转为落后。精确等学习程度因存档稀疏不可独立验证。科学判断 Unknown。
- Current work: 分析已落盘。R1 om-qk46lhzu 已跑满 600 步并成功退出。第 250→500 步 EVAL NLL 8.161782→10.204545，第 558 步达到与 HA5-T 同一告警条件。单项引擎诱因 Unknown。
- Next action: 等研究者讨论和决定。
- References: `/data/250010109/MoE_Router/experiments/20261112_a5_shrink_attribution/归因报告_cn.md`、同目录 `manifest.json`，以及 `/data/250010109/MoE_Router/experiments/20261112_hier_bisection_routing/runs/R1_positive_control/R1_速报_cn.md`。本轮资产 `analysis_a5_shrink_efficiency_attribution_20261112`、`checkpoint_family_r1_positive_control_20261112`、`checkpoint_r1_positive_smoke_step12_20261112` 均通过严格访问检查。
