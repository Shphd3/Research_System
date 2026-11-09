# 执行修订 02：普通可训练 top-2 MoE 对照

状态：`USER_AUTHORIZED_BOUNDED_CONTROLS`；科学判断：`Unknown`。研究者在 2026-10-21 当前对话中明确要求子 Agent 完成“普通 MoE”和“普通 MoE 加 load balance”。授权覆盖实现、必要工程检查和以下两个同预算对照，不改变 Focus/Anchor、原四臂及其冻结结果，也不增加调参、新数据、续训、提交 Git 或发布。

本修订补充[原 Protocol](../protocol_cn.md)。目的很窄：在完全相同的缓存、训练预算和评估位置上，测量可学习路由器的表现，并比较有无负载均衡辅助项。结果只能补足路由对照，不能单独证明高频共同路径机制。

## 固定计算与比较

两臂分别为 `MoE` 和 `MoE_LB`。路由器输入为第 28 层完整原始 hidden state 除以继承的 TRAIN RMS 尺度。一个无 bias 的 FP32 线性层把 1,024 维映射成八个 logits；完整 softmax 后选择概率最高的两个不同 expert，再把选中概率归一为和为一的权重。完全相等时优先较小 ID。各 expert 接收完整表示，SwiGLU 输出加权后乘回同一尺度并加回残差，最后使用原冻结 final norm 和输出 embedding。没有容量裁剪、丢弃 token、噪声或 z loss。

expert 形状和每个种子的初始化均与原实验逐张量一致，合计 25,165,824 参数。路由器另增 8,192 参数，总计 25,174,016；独立生成器 `seed + 741103`、正态标准差 0.02 初始化。新两臂在同一种子内共享 expert/router 初始化与数据顺序。down 矩阵初始为零，因此初始输出精确等于 Base。旧实验的两个 expert 固定各占 0.5，新实验会学习混合权重；故新旧对比同时改变选择规则、混合权重与少量参数，不能解释为只隔离了 feature 信息。

有效 batch 有 N 个有效答案预测位置。`P_i` 为完整 softmax 概率的 batch 均值；`f_i` 为 expert i 在 2N 次选中分配中所占比例。原始均衡项为 `L_LB = 8 sum_i f_i P_i`，选中计数 detach，仅概率传梯度；在完整有效 batch 上计算，不能把各 microbatch 的乘积再取平均。均匀路由时该值为一。目标为答案 CE 加 alpha 乘均衡项：`MoE` 的 alpha=0，`MoE_LB` 的 alpha=0.01。两臂均记录原始项和加权项。这是 [Switch Transformers 公式 4–6](https://jmlr.org/papers/volume23/21-0998/21-0998.pdf) 的明确 top-2 适配；原论文使用 top-1。系数是本次对照的固定常规实现选择，不以任何评估面板调参。

复用 TRAIN 1,024 对话 / 85,548 个答案目标、EVAL 256 / 22,446、DEV 128 / 10,340。只有 TRAIN 更新权重。DEV 已在上一轮暴露，本轮称固定复核面板，不称新确认集。原 feature 缓存仅用于保持低/高频评估定义一致，不进入新路由器，也不输入未来答案。

两臂各用种子 11、22，共四个模型。均为一 epoch、168 次更新、有效 batch 512、microbatch 128，同一种子使用原 PCG64 排列。AdamW 学习率 0.0003，betas=(0.9,0.95)，epsilon=1e-8，weight decay=0.01，梯度裁剪 1；前九步预热，再余弦衰减至峰值的 0.1。末 batch 为 44 个位置；终点累计计数恰为 85,548。保存第 0、42、84、126 步权重，第 168 步保存模型/router、optimizer、RNG、顺序、cursor、token 与调度信息。`latest.pt` 与 `final_resumable.pt` 指向同一终点文件，不进行最佳 checkpoint 选择。

五个共同取点评估完整 TRAIN/EVAL；四个新模型全部完成后统一评估终点 DEV，并读取原 Base/T_F/T_H/R_F/R_H 的同索引终点数组比较。报告 overall、固定低/高频 per-feature macro 和位置并集 NLL、每 feature 支持数、路由概率和分配计数、两种子及均值。较低 NLL 仅称描述性更好；种子方向相反或模型不全时证据不足。不新增推断阈值或科学 PASS/FAIL；LB 减 no-LB 是配对目标项对照，机制判断保留 `Unknown`。

## 工程、资源和交付

复用经检查的原 trainer 中 Expert、FrozenHead、尺度、数据与标签验证、学习率调度、RNG/序列化、指标和观测性；仅适配可学习 top-2、声明的 LB 目标和独立编排。已查看 clean trainer 作为工程参考，不复用其全模型/DCLM/shared-expert 架构或退役启动配置。CPU 检查验证配对初始化、零支路、加权 dispatch、确定性 tie、路由梯度与跨 microbatch 的 LB 等价。GPU Smoke 验证真实答案位置、Base 初始 logits 精确相等、有限梯度、有效 batch token 计数、实际磁盘状态恢复后下一步完全一致，以及两臂所需 TensorBoard 标签。仅 Smoke 通过后执行已授权的四模型训练。任何标签缺失、identity 改变、非有限值、目标缺失或资源越界均停止。

使用 ACP `h100-4-reserved`、`shphd-lite-0911`、单节点，每 GPU 一个 arm×seed；CPU 总八线程，worker RSS 合计 64 GiB，每 GPU allocated 16 GiB，新盘 16 GiB，远端 active 总 35 分钟含 Smoke 和最终复核。使用镜像原 Python，不安装依赖。一个支持的 submit-template job 先 Smoke 再按门槛训练，不把尚未通过的 Smoke 写成预先 PASS。无资源 fallback、自动 retry 或续训；短启动验证确认首进度后停止反复轮询，后续检查同一 job。

执行根目录：`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/standard_moe_controls/20261021T042742Z`。`config/frozen.json` 固定操作值及资产 ID；`code`、`training`、`logs`、`acp_receipts/pod`、`provenance` 保存实际证据。Smoke 和正式训练实际保存的 checkpoint 均需登记；缺失/部分状态明确保留。四个实际输入资产已在 2026-10-21 通过 selected strict 检查，见项目根目录 `assets/checks/2026-10-21_standard_moe_inputs.json`。

A–G 审计：问题不变；数据与暴露边界明确；原答案监督；架构/gate 差异明确；优化与预算配对；新两臂 LB 单项对照；资源与产物固定。CPU 工程一致性已通过，GPU 资格取决于实际 Smoke。原结果已暴露，本修订只增加四个新模型，不重写旧结果或科学状态。
