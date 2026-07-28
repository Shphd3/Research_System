# Protocol（中文 companion）：A06_02_03_E02 Top-1 Counterfactual Correction Dynamics

## 0. 审核快照

状态：用户已明确授权。英文 `protocol.md` 为 canonical。

目的：判断 weighted top-1 是否因为不能比较未选 experts 的各自 utility，而形成 rank-dependent correction。

设置：冻结正交 feature states、固定 class-specialized experts、matched expert 初始 rank 1/2/4；soft 与 weighted top-1；router-only SGD 200 步；32 seeds。

主指标：matched expert 首次成为 top-1 的 correction step。

通过：top-1 的 rank-4 减 rank-2 correction penalty 明显大于 soft，并且 top-1 的未选 row update 不按各自 utility 区分。

失败：top-1 和 soft 一样直接、一样对 rank 不敏感。

边界：不能声称永久 lock-in、soft router 更优或真实 MoE 行为。

## 1. 术语解释

- counterfactual comparison：在未实际选择 expert 时，评估它若被使用会怎样改变 loss。
- correction step：正确 expert 首次成为 top-1 的训练步。
- boundary count：selected expert 发生变化的次数。

## 2. 核心公式

$$
\Delta w_j
=\frac{\eta}{\tau}p_r(\mathbf 1[j=r]-p_j)B_rh.
$$

未选 row 可以因 softmax denominator 获得更新，但该更新不含自己的 $E_j$。实验检验的是“没有 utility-specific correction”，不是“没有梯度”。

## 3. 条件与指标

方法：soft / weighted top-1。初始 rank：1/2/4。辅助指标：unselected utility gap、boundary count、final margin、formula closure error。

## 4. 不可声称内容

不能声称所有 top-1 都失败、错误路由永不恢复、或已经得到可部署方法。

