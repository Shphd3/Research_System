# Conversation Memory: 1113-多账户分布式系统协同训练方案

Conversation name: 1113-多账户分布式系统协同训练方案
Processed by: Codex (harness: Codex; model: unknown)
Created at: 2026-11-13T13:33:46Z
Latest update at: 2026-11-13T13:39:51Z
Continues from: none
Environment: repo=`/data/250010109/Research_System`; exec=`/data/250010109/MoE_Router`

## 2026-11-13T13:33:46Z -- 建立记录：商汤多节点通信核查

- Summary: 暂停 SAE 瓶颈分析。本对话核实商汤 ACP 多 worker、独立 session、跨工作空间和跨账户通信，重点是四卡 Reserved 额度是否能和 H100 Spot 组成一个同步训练组。
- Current work: R07 的同作业四 rank 训练有历史回执。Reserved + Spot、独立 session 和跨账户的授权、网络与通信性能待确认。本轮只读核查，不新建 GPU 作业。
- Next action: 核对官方 API 配额字段、旧作业的物理宿主证据与本账号可见接口，随后按 L0–L4 给出可复用验证步骤；新作业需研究者确认。
- References: `docs/sco_reserved_training_guide_cn.md`、`docs/execution_envelope.md`；执行侧 `experiments/20261111_a5_continue/` 的提交回执、worker 证据和停止回执。

## 2026-11-13T13:39:51Z -- R07 复原与下一轮探针

- Summary: 只读 SCO 复查确认 R07 是同一 share-space / share-cluster Reserved ACP 作业，两个不同宿主地址，各两张 H100，四 rank 已续训到研究者停止点。现有 ACP API 配额为任务级单值；混用两类配额只能把独立端点组网当待核实方案。share 池看到 IB 和默认 Spot 配置，不能由此推出个人 Spot 配额、独立作业互通、性能或合同计费。
- Current work: L0–L4 的执行说明、固定地址 TCP 及 PyTorch 探针已放在执行侧；单机 CPU/Gloo 数值逻辑已自测。没有提交新作业或测试跨机连接，Reserved + Spot、跨 workspace/账户均待确认。旧 R07 未留准确 rendezvous 使用值及 NCCL 数据面日志。
- Next action: 完成 L0 权限与容量核对；若研究者批准两个真实节点各一张 H100 的短测，先做同一作业 Reserved 对照。混合组需独立确认授权和可同时分配，跨账户待管理员确认。
- References: `docs/sco_reserved_training_guide_cn.md`；执行侧 `experiments/20261111_a5_continue/evidence/{startup_h100_2x2,user_stop_20261112}.json` 与原提交回执；`experiments/20261113_sco_multinode_probe/README_cn.md`。
