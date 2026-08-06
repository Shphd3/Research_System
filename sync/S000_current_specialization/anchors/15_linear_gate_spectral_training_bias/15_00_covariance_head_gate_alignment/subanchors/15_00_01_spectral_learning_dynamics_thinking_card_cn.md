---
thinking_card_id: 15_00_01_spectral_learning_dynamics
status: human_core_approved_details_pending
human_language: zh
formalization_authorized: true
protocol_authorized: false
implementation_authorized: false
full_run_authorized: false
updated: 2026-07-30
---

# Thinking Card：Router 频谱学习动力学

## 我的判断

- **具体现象：**实际 Router 输入上的线性 Gate 在最早的 10k checkpoint 已
  强烈对齐 covariance head，但 10k--30k 没有继续增强，middle/tail 相对追上。
- **机制猜想：**研究者已批准“条件性有限时间谱加速”：当专家优势在谱方向上
  可比、Gate 未饱和、优化器不白化且表征基底短时稳定时，大 covariance
  特征值使对应 Gate 模式更快学习；各向同性谱没有由 covariance 指定的方向
  偏好。
- **最强替代解释：**`Unknown`。研究者要求 AI 提出并逐项审核。
- **最不确定的一环：**真实 MoE 的 head alignment 是由专家优势本来偏 head、
  优化器、表征漂移还是 Router--Expert 反馈造成。
- **什么证据会改变判断：**在匹配专家优势信号后，各向异性不改变各频带学习
  时间；或 whitening 后速度差仍保留；或真实模型的 head alignment 不能在
  2B tokens 内被逐步定位。
- **当前唯一决策：**审核 E03-S 受控因果实验与 E03-R 真实早期轨迹的 Approval
  Snapshot；未批准实现和运行。

## AI 审核

- **最强活跃 rival：**方向差异来自专家优势信号 $A_t$，而非 covariance
  特征值；其次是 optimizer preconditioning 与 $U_t$ 表征漂移。
- **唯一隐藏假设：**“谱方向上可比”必须由注册的专家优势矩阵或独立功能目标
  保证，不能由观察到的 Gate 权重反推。
- **最小区分实验：**固定专家优势下比较 flat / anisotropic / whitened，并加入
  tail-only 反例；真实训练另行记录 raw gradient、实际 update 与 $W\times U$
  crossing。
- **AI 建议：**`pursue`，但把联合专家反馈保留为待检验扩展。

## 我的确认

- **已批准：**条件性有限时间谱加速定理核心。
- **待逐项确认：**受控谱比、专家状态、主指标、真实模型规模、seed 与保存
  密度。
- **是否允许实现或运行：**`no`，等待 Protocol Snapshot 批准。

