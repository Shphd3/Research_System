# A11_14 自然语言语义学习效率实验协议

## 0. 目的

在固定 A11_13 的 256-word horizon 任务上，用两种方法共同的标准 H1 答案预测，比较 NTP 与 K=2 MTP 的学习速度。MTP 的 H2 只作为机制诊断，不计入下游主分数。

## 1. 固定条件

- 训练 paraphrase `0,1`，测试未见 paraphrase `2,3`；
- 每个 seed 训练 160、测试 160 个样本；
- 两层因果 Transformer，`d_model=128`，4 heads，`d_ff=512`；
- AdamW，`lr=3e-4`，weight decay `0.01`，batch size `16`；
- 条件仅 `ntp_all_h1` 与 `mtp_all_k2`；
- seeds `971-975`；
- 同 seed 的主干/H1/H2 初始化、文本、batch 次序、已处理 token 和更新数严格配对。

## 2. 目标函数

序列末尾是：

```text
<EOP> <DECIDE> <ANS_A or ANS_B>
```

NTP：

$$
L_{NTP}=L_1^{all}.
$$

MTP：

$$
L_{MTP}=L_1^{all}+L_2^{all}.
$$

两种方法都用 H1 在 `<DECIDE>` 预测答案；只有 MTP 额外用 H2 在 `<EOP>` 提前预测同一答案。

## 3. 指标

$$
Q_{downstream}
=\min\{A_{H1},C_{para}^{model},S_{cf}^{model}\}.
$$

- $A_{H1}$：标准下一词元答案准确率；
- $C_{para}^{model}$：同状态、同请求、不同未见改写的预测是否一致；
- $S_{cf}^{model}$：固定后续文本、改变早期状态时预测是否翻转；
- $T_{0.9}$：$Q_{downstream}\ge0.9$ 连续三次评估的最早时间；
- token-AUC：$Q_{downstream}$ 对累计文本 token 的归一化曲线面积；
- local H1 guard：排除答案位置后的 next-token CE/accuracy；
- H2 direct accuracy：只用于解释，不用于方法主判定。

## 4. 判定

可判定：至少一种方法在 `4/5` 个 seed 达到阈值。

支持 MTP 更高效需要同时满足：

1. MTP 的 $T_{0.9}$ 在至少 `4/5` 个 seed 更小；
2. MTP token-AUC 在至少 `4/5` 更高；
3. 最终共同 H1 分数在至少 `4/5` 不低于 NTP；
4. 每个 seed 的 local H1 accuracy 下降不超过 `0.01`，CE 增加不超过 `5%`。

若只有 H2 变好而共同 H1 不变，不能说 MTP 改善了下游任务。若两种方法都学不会未见改写，则证据不足，先解决模型能力或任务迁移问题，不能据此否定 MTP。

