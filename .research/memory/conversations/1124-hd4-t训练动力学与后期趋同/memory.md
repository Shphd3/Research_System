# Conversation Memory: HD4-T训练动力学与后期趋同

Conversation name: 1124-HD4-T训练动力学与后期趋同
Processed by: Codex (harness: Codex Desktop; model: unknown)
Created at: 2026-11-23T17:50:19Z
Latest update at: 2026-11-23T18:04:19Z
Continues from: none
Environment: repo=/data/250010109/Research_System; exec=/data/250010109/MoE_Router/experiments/1124_hd4t_dynamics/HD4T

## 2026-11-23T17:50:19Z -- 建档

- Summary: 研究者要求解释 HD4-T 对 A0 的早期领先、后期纵向差距缩小及斜率与极限的区别。本轮延续活跃问题 #2。
- Current work: 当前会话标题已通过 app-server 读回复核。沿用附件范围，自主研究且不提交真实预训练。
- Next action: 用现有训练归档和可执行的反证核对动力学解释。
- References: /data/250010109/MoE_Router/experiments/1124_hd4t_dynamics/HD4T/研究入口.md

## 2026-11-23T18:04:19Z -- 交付

- Summary: A0 在斜率接近前已累计追回早期大部分领先。约 5B 差 +0.001143 nat，区间覆盖零，逐位置绝对差 0.5262 nat，两个最终 loss 下限 Unknown。只能配对到约 5B，6.5536B 无同预算实测。
- Current work: 完成真实训练轨迹及逐位置复核，历史梯度投影，四组真实 checkpoint 的 AdamW 局部回放，共享根和 A0 单专家定位，受控两专家实验及八个敏感性种子。step 25 的真实末层粗组效应不支持总体去冲突，step 250 的同类跨组回放改善。区分历史低频 DEV 一步、真实短回放、受控训练和正式预训练曲线。
- Next action: AI 建议冻结原模型，在同起始 logits 下对照真实关系、负载匹配打乱和共享分支的有限步迁移。研究者决定 Unknown。
- References: /data/250010109/MoE_Router/experiments/1124_hd4t_dynamics/HD4T/work/report.md；/data/250010109/MoE_Router/experiments/1124_hd4t_dynamics/HD4T-训练动力学研究-1124.zip；research/from-attention-to-search/main/explore/1124_hd4t_dynamics/log.md
