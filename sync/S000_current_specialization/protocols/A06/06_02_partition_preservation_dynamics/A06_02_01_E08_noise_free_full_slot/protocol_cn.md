# Protocol 中文摘要：A06_02_01_E08 无背景 full-slot preservation

**问题：** 之前 full-LM 长训练会破坏 oracle / route center 初始化后的 feature routing。现在测试这是否主要来自背景 token 梯度噪声。

**数据构造：** 序列长度 32。每个样本只含一个 feature，32 个位置全是该 feature token：

$$
x=(F_f,F_f,\ldots,F_f).
$$

没有 neutral/background token。四个 feature 均匀采样。

**训练目标：** 全序列下一 token 预测，对位置 0 到 30 求 cross entropy。

**模型：** 一层 causal Transformer + 一层 weighted top-1 MoE，沿用 A06 synthetic surface。

**条件：**

- random router；
- oracle all-position center；
- oracle predictive-position center；
- oracle last-predictive-position center。

**主指标：**

- all-position feature NMI；
- margin p05 作为稳定性 guard。

**判定：**

- 如果 oracle center 在 2000 步后仍保持高 NMI 和正 margin，说明背景噪声是假设中的关键因素，下一步做 signal/noise margin budget。
- 如果 oracle center 仍被破坏，说明背景噪声不是充分解释，下一步应进入 router one-step dynamics。

