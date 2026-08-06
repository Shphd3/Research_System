# 实验协议：Router 输出反事实审计

## 0. 审批摘要

**状态：** 用户于 2026-07-29 明确要求执行，已授权协议、实现、smoke 与完整运行。

**决策问题：** 固定实际 Router reference、专家输入、专家参数、Native token 权重、八个专家负载、shared expert 和其他层路由，只改变目标层的专家身份，是否显著改变稀疏专家输出与最终预测？

**实验性质：** Router 即时表征影响的操作化审计；不是专家效用实验，也不更新 A06 功能主张。

**主指标：**

$$
R_\ell=
\frac{1-\operatorname{CKA}(Y_{native},Y_{center})}
{1-\operatorname{CKA}(Y_{native},Y_{shuffle})}.
$$

**条件：** Native、冻结中心且严格负载匹配的反事实路由、严格负载匹配的随机标签、Native no-op replay。

**模型与数据：** 严格限定两个 step-40k 模型；使用 `global-shard_02_of_10` 中已经冻结的32个校准文档和64个评估文档，每篇256 token；逐层检查12层。

**不能声称：** LB/decommon 因果差异、训练中表征形成、专家语义效用、树状或长程能力、验证损失/FLOP。

## 1. 关键实现定义

- 两个模型都是 Top-1，但实际配置 `norm_topk_prob=False`。为了只改变专家身份，所有反事实条件都复用每个 token 的 Native top-1 softmax 权重。
- 两个 checkpoint 都设置 `gating_reference=oracle`：Router 读取 attention branch 输出，而专家读取 post-attention normalized hidden state。实验分别捕获并固定这两个张量，不能用专家输入代替 Router 输入。
- Centered 路由先用 $W(h-\hat\mu)$ 排序，再以最小分数损失把超额专家的 token 移给缺额专家，直到八个专家负载与 Native 完全相同。
- Shuffle 直接置换 Native 专家标签，严格保持负载。
- Shared expert 在所有条件中完全不变。
- 只干预一层；后续层按反事实 hidden state 自然传播并使用原生路由。

## 2. 必要护栏

原始 $R_\ell$ 会受到 route flip 数量影响。Centered 若只翻转20%，shuffle 翻转近90%，小 $R_\ell$ 可能只是因为改变的 token 更少。因此除用户指定指标外，必须同时报告：

1. 仅在 Centered 已翻转 token 上计算的 sparse-output CKA；
2. 按 Centered/shuffle flip-rate 比例校正的 $R_\ell$；
3. 每个 token 的 cosine 与归一化 Frobenius 变化。

## 3. 指标

- 主对象：稀疏专家输出 CKA、flip-only CKA、$R_\ell$、flip-adjusted $R_\ell$。
- 谱结构：能量定义的 effective rank、90%能量秩、归一化谱距离、top-32 主角度。
- 功能护栏：block CKA、final-hidden CKA、logit KL、held-out NLL 变化。

## 4. 预注册闸门

层有效条件：Centered flip $\ge0.20$；shuffle flip $\ge0.50$；shuffle sparse CKA $<0.99$；负载严格相等；no-op KL 和 NLL 误差不超过 $10^{-6}$。

单个模型支持 H0 需要至少8层有效，并同时满足：median $R\le0.25$、median flip-adjusted $R\le0.50$、median flip-only CKA $\ge0.90$、谱距离和主角度相对 shuffle 的 median ratio 均不超过0.25、logit-KL ratio 不超过0.25，且每层 $|\Delta$NLL$|\le0.01$ nat/token。

单个模型否定 H0：至少8层有效，且 median $R\ge0.75$、或 flip-only CKA $\le0.50$、或 KL ratio $\ge0.75$、或任一有效层出现可重复的 $|\Delta$NLL$|\ge0.02$。两个模型结论相反则总结果为证据不足。

这些数值界限在读取反事实结果前冻结；用户草案只给出了20% flip gate，因此其余界限属于 AI 的预注册操作化。

## 5. 结论边界

即使即时影响很大，也只能说明现有专家对路由身份不具有可交换性；即使即时影响很小，也不能证明 Router 没有塑造训练过程。完整英文合同见 [protocol.md](protocol.md)。
