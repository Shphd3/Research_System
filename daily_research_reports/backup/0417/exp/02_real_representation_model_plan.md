# 从 Toy 到真实表征空间 / 真实模型：实验规划文档

## 背景

Toy 已经回答了一个核心问题：

> **如果 Common 和 Tail 被物理分开，并且 Tail 拥有更宽松的 WD / LR 条件，那么 Tail 可以被明显救回来，而 Common 几乎不受影响。**

接下来的任务不是立刻上大规模完整 MoE，而是分 3 个阶段，把 toy 的结论一层层搬到真实语言模型里：

1. **先看真实表征空间**：确认真实 hidden state 里确实存在 shared head / semantic tail 结构。  
2. **再做无路由的分支解耦**：先把 Common / Tail branch 做出来，验证 decoupled optimization 在真实模型里是否有效。  
3. **最后再上层级式 MoE**：把 tail branch 换成 tail-MoE，并测试 specialization 是否真的更纯。

---

## 本轮默认执行设置（Qwen3-8B）

- 模型：使用本地 `Qwen3-8B`，冻结原始 backbone。实验 A 仅做前向提取 hidden states，不更新任何模型参数。
- 提取位置：默认取每个 Transformer block 的 `post-attention / pre-FFN` hidden state，因为它与后续 `F_c(h) + F_t(h_{tail})` 的改造位置一致。
- 层位：记总层数为 $L$，首轮固定扫描 4 个层位：$\lfloor 0.15L \rfloor$、$\lfloor 0.40L \rfloor$、$\lfloor 0.65L \rfloor$、$\lfloor 0.90L \rfloor$。
- Common 数据：Wiki 通用文本。
- Tail 数据：WoS 四个领域文档，首轮固定为 `Medical / Psychology / CS / Biochemistry`。
- 文档规模：Wiki 先取 2,000 篇，WoS 每类先取 1,000 篇，统一 `max_length = 512`。
- 协方差估计：用混合 token 池估计 $\mu$ 与 $\Sigma$，默认 `Wiki:WoS = 4:1` 采样，以保留 common-dominant 的统计结构。
- 几何统计口径：每层每个 WoS 类别最多保留 2,048 个 token hidden states；文档级 probe / router 使用 mean pooling 表征。
- 评估划分：WoS 文档级任务使用 `70/15/15` 的 train / val / test 划分，重复 5 个随机种子。
- $k$ 扫描：首轮固定 $k \in \{4, 8, 16, 32, 64\}$；若 top-k explained variance 仍偏低，再补一组 $\{96, 128\}$。
- 数值精度：模型前向可用 `bfloat16`，均值、协方差、SVD 与 probe 训练统一转 `float32`。
- A 阶段成功判据：若在至少一个层位和一个 $k$ 上，$h_{tail}$ 相对 $h-\mu$ 在 WoS domain probe accuracy 或 purity / NMI 上稳定提升，而单独去均值增益有限，则认为真实表征解耦假设成立。

---

# 实验 A：真实表征空间诊断

## 目的
验证真实 hidden state 是否满足你们理论里的几何前提：  
top 主方向主要承载共享高频结构，而 tail residual 更适合承载语义区分信息。

## 假设
1. 在 FFN 输入或 attention 输出处，hidden state 的协方差谱呈现明显 head-heavy 结构。  
2. 做
$$
h_{\text{tail}} = (I - V_kV_k^\top)(h - \mu)
$$
以后，某些“语义相关的 proxy 任务”会更容易被简单线性 probe / router 分开。  
3. 单纯只做去均值，不会带来同等级的提升。

## 数学建模

### 表征
对某一层 hidden state 记为：
$$
h \in \mathbb{R}^d
$$

估计 detached mean 与 covariance：
$$
\mu = \mathbb{E}[h], \qquad
\Sigma = \mathbb{E}[(h-\mu)(h-\mu)^\top]
$$

令 $V_k$ 为 $\Sigma$ 的 top-$k$ 主方向，则：
$$
h_c = h - \mu
$$
$$
h_{\text{tail}} = (I - V_kV_k^\top) h_c
$$

### 指标
对任一 proxy 标签 $z$，定义：

- 组间散度：
$$
B_z = \sum_c \pi_c (\mu_c - \mu)(\mu_c - \mu)^\top
$$

- 组内散度：
$$
W_z = \sum_c \pi_c \operatorname{Cov}(h \mid z=c)
$$

- Fisher 型可分性：
$$
\mathrm{Sep}_F(P; z) = \frac{\operatorname{tr}(P B_z P^\top)}{\operatorname{tr}(P W_z P^\top)}
$$

实验里还看：
- 线性 probe 准确率
- router purity / NMI
- eigenspectrum

## 实验

### 数据与模型
- 按“本轮默认执行设置”使用冻结的 `Qwen3-8B`。
- Common 侧使用 Wiki；Tail 侧使用 WoS 四领域文档。
- 本轮只做 frozen representation probing，不做任何 finetune。

### 步骤
1. 对 Wiki 与 WoS 文档分词并前向，在选定层提取 `post-attention / pre-FFN` hidden states。  
2. 用 `Wiki:WoS = 4:1` 的混合 token 池估计每层的 $\mu$、$\Sigma$、eigenspectrum 与 $V_k$。  
3. 对 WoS 文档构造三种表示：
   - raw: $h$
   - centered: $h-\mu$
   - tail: $(I - V_kV_k^\top)(h-\mu)$
4. 用 mean pooling 得到文档级表征，并在三种表示上训练相同的 4-way 线性 probe / 线性 router。  
5. 对比 raw、centered、tail 三种空间在 WoS 领域标签上的 probe accuracy、purity / NMI 与 $\mathrm{Sep}_F$。

### Proxy 标签怎么取
真实语言里没有唯一“语义标签”，所以这里不要求人工精确标签，而是用**一组可操作的 proxy 任务**。  
本轮主 proxy 固定为 **WoS domain label**；其余 proxy 作为补充分析：

1. **领域 / 来源标签**  
   直接使用 WoS 的四类领域标签。  
   这是本轮主评估任务，用来看 tail 是否更利于 domain-specific routing。

2. **稀有 token bucket**  
   把 token 按频率分桶，或对 rare token 做 cluster。  
   用来看 tail 是否更利于 rare lexical / semantic distinction。

3. **局部语义簇**  
   对某个词后上下文 embedding 做聚类，得到 latent cluster。  
   用来看 tail 是否更利于局部概念区分。

### 指标
- explained variance / 谱陡峭度
- $\mathrm{Sep}_F$
- linear probe accuracy
- router purity / NMI

## 预期结果
- centered 相比 raw：变化不大  
- tail 相比 centered：某些 proxy 任务的 $\mathrm{Sep}_F$ 和 linear probe accuracy 明显升高  
- 若删掉过多 top-$k$，性能会下降，说明这不是“删得越多越好”

## 结论用途
这一步决定两件事：
1. 哪些层最适合做 common / tail 分解  
2. projector 的 $k$ 取值范围

---

# 实验 B：真实模型里的无路由分支解耦（先不上 MoE）

## 目的
在真实模型里先验证：  
**即便先不引入 expert routing，只要把 Common / Tail branch 分开，并给 Tail 独立 WD / LR，rare 部分就能改善。**

## 假设
1. 把 FFN 块改成 common branch + tail branch 后，rare token / rare continuation 的性能会提升。  
2. 若 Tail branch 仍用统一 WD / LR，则改进有限。  
3. Tail branch 使用更小 WD + 更长 LR 时间窗后，提升明显。

## 数学建模

把某一层 FFN 块改成：
$$
h_{\text{out}} = h + F_c(h) + F_t(h_{\text{tail}})
$$

其中：
$$
h_{\text{tail}} = (I - V_kV_k^\top)(h-\mu)
$$

这里：
- $F_c$：common dense MLP，处理共享高频结构
- $F_t$：tail dense MLP，处理 residual tail 结构

注意：这一阶段还不引入 MoE，只验证**分支解耦 + 优化解耦**是否有用。

## 实验

### 数据
- 直接使用冻结的 `Qwen3-8B` 作为 backbone，不再单独训练小模型。
- 训练语料使用 `Wiki + WoS` 混合语料，默认 token 比例 `4:1`，以保留 common-dominant 分布。
- 首轮只改造实验 A 中表现最好的 1 个层位；若效果稳定，再扩展到 2 个层位。
- 为控制变量，冻结原始 `Qwen3-8B` 权重，只训练新增的 `common branch / tail branch` 参数。

### 对比配置
1. **Baseline FFN**
   - 标准 MLP
   - 统一 WD / LR

2. **Split-FFN / coupled-optim**
   - $F_c(h) + F_t(h_{\text{tail}})$
   - 仍然统一 WD / LR

3. **Split-FFN / decoupled-optim**
   - $F_c(h) + F_t(h_{\text{tail}})$
   - common: 原 WD / 原 LR schedule
   - tail: 更小 WD + 延迟或更慢 LR 衰减

### 指标
- overall validation perplexity
- frequent-token perplexity
- rare-token perplexity
- rare-token top-1 / top-k accuracy
- tail branch activation norm
- tail branch parameter norm
- tail branch gradient/update count

### 关键实现点
- projector $V_k$ 和 $\mu$ 先离线估计，训练期固定  
- 这样先把“projector 学习不稳定”这个变量拿掉

### 伪代码
```python
# h: [batch, seq, d]
h_center = h - mu.detach()
h_tail = h_center - (h_center @ V_k) @ V_k.T

y_common = common_mlp(h)
y_tail = tail_mlp(h_tail)

h_out = h + y_common + y_tail
```

### 优化器
```python
opt_common = AdamW(common_params, lr=lr_common, weight_decay=wd_common)
opt_tail   = AdamW(tail_params,   lr=lr_tail,   weight_decay=wd_tail)
```

### 调度器
- common: 原 Cosine
- tail: 持平更久，再衰减；或使用更长 T_max

### 首轮默认超参
- `lr_common = 1e-4`, `wd_common = 1e-2`
- `lr_tail = 3e-4`, `wd_tail = 1e-4`
- `hold_ratio = 0.8`
- common 用 Cosine；tail 用“前 80% 保持、后 20% Cosine”的 schedule

## 预期结果
- Baseline 和 Split/coupled-optim 差距不大  
- Split/decoupled-optim 的 rare-token ppl 明显更好  
- frequent-token ppl 基本不变

## 结论用途
若这一步成立，说明：
> **即便不靠 routing，只靠表示解耦 + 优化解耦，真实模型里的 tail 已经能被更好地保住。**

这会给后续 MoE 一个很稳的底座。

---

# 实验 C：真实模型里的 Hierarchical MoE

## 目的
验证最后的完整命题：

> **router 不应该在 full hidden state 上直接分发，而应该在 tail residual 上分发；同时 tail experts 需要独立的 WD / LR。**

## 假设
1. 在 $h_{\text{tail}}$ 上做 router，会比在 raw $h$ 上做 router 得到更高的 expert purity。  
2. common 分支负责高频共享结构，tail-MoE 负责 rare / domain-specific residual；这比 flat MoE 更稳。  
3. 给 tail experts 更小 WD + 更长 LR 时间窗后，rare 专家的“存活”明显提高。

## 数学建模

最终块形式：
$$
h_{\text{out}} = h + F_c(h) + \sum_{e=1}^E g_e(h_{\text{tail}})\,E_e(h_{\text{tail}})
$$

其中：
$$
h_{\text{tail}} = (I - V_kV_k^\top)(h-\mu)
$$

这里：
- $F_c$：common dense branch
- $g_e$：tail router
- $E_e$：tail experts

### Flat MoE 对照
$$
h_{\text{out}}^{\text{flat}} = h + \sum_{e=1}^E \tilde g_e(h)\,\tilde E_e(h)
$$

### 关键差别
- Flat：router 在 raw hidden state 上工作；common / tail 混在一起；统一 WD / LR  
- Hierarchical：common / tail 先分解，再让 router 只看 tail；tail experts 独立 WD / LR

## 实验

### 数据
- 沿用实验 B 的 `Wiki + WoS` 混合语料与 `Qwen3-8B` tokenizer。
- 只在实验 A / B 选出的 1~2 个关键层引入 tail-MoE，不一次性改造全模型。
- 冻结原始 `Qwen3-8B` 权重，只训练新增的 common branch、tail router 与 tail experts。

### 对比配置
1. Flat MoE / raw router / uniform WD+LR  
2. Tail-router only / raw common path  
3. Tail-router + decoupled WD  
4. Tail-router + decoupled WD + decoupled LR（完整版本）

### 首轮默认结构
- `E = 4` 个 tail experts，使用 `top-1` routing。
- common path 保持 dense；tail path 只接收 projector 后的 $h_{tail}$。
- optimizer 默认沿用实验 B 的 common / tail 超参。

### 指标
- validation perplexity
- frequent / rare-token perplexity
- domain-specific perplexity
- router purity / NMI 对 proxy 标签
- expert occupancy
- per-expert effective update count
- per-expert parameter norm
- per-expert gradient norm
- rare expert survival ratio

### 关键实现点 1：EMA projector
```python
with torch.no_grad():
    batch_mu = h.mean(dim=(0, 1))
    mu.mul_(1 - ema).add_(ema * batch_mu)

    hc = h - mu
    cov_batch = torch.einsum('btd,bte->de', hc, hc) / (h.shape[0] * h.shape[1])
    cov.mul_(1 - ema).add_(ema * cov_batch)

if step % eig_every == 0:
    eigvals, eigvecs = torch.linalg.eigh(cov)
    V_k.copy_(eigvecs[:, -k:])
```

### 关键实现点 2：tail projection
```python
hc = h - mu.detach()
proj = (hc @ V_k.detach()) @ V_k.detach().T
h_tail = hc - proj
```

### 关键实现点 3：块结构
```python
y_common = common_mlp(h)
router_logits = tail_router(h_tail)
y_tail = tail_moe(h_tail, router_logits)

h_out = h + y_common + y_tail
```

### 关键实现点 4：优化器
```python
opt_common = AdamW(common_params, lr=lr_common, weight_decay=wd_common)
opt_tail   = AdamW(tail_params,   lr=lr_tail,   weight_decay=wd_tail)
```

## 预期结果
- 在相同专家数下，Hierarchical 的 router purity 更高  
- rare / domain token 的 ppl 更低  
- tail experts 的 update count 更均衡，rare experts 不再提前死亡  
- common 侧性能基本不掉

## 结论用途
这一步如果成立，就能把你们当前主线完整闭环成：

1. **表示解耦**：去 shared head，让 router 看见 tail  
2. **架构解耦**：common 和 tail 物理分支化  
3. **优化解耦**：tail 拥有独立 WD / LR  
4. **最终 specialization**：专家接收的信号更纯，rare 语义被真正保住

---

# 推荐推进顺序

1. **A：真实表征空间诊断**  
   先找到层和 $k$，证明 projector 值得做。

2. **B：Split-FFN（无 MoE）**  
   先把 decoupled optimization 在真实模型里钉死。

3. **C：Hierarchical MoE**  
   最后再引入 tail router / experts，把完整 specialization 做出来。

这个顺序的好处是：  
每一步只多引入一个变量，不会把 projector、routing、optimizer 三件事一次性搅在一起。

---

# 本文档的用途

这份文档不是结果报告，而是**真实模型实验规划**。  
toy 已经跑完；真实模型阶段建议严格按 A → B → C 推进。  
这样每一步都能清楚回答一个单独问题，方便和导师、学长同步。

---

## 汇报摘要

[exp2：real representation probe / Qwen3-8B]

目的：在冻结的 Qwen3-8B 上验证真实 hidden state 是否存在“shared head 遮蔽 semantic tail”的几何结构，并据此确定后续 split-FFN 与 Hierarchical MoE 的层位与 projector 设置。

假设：
- 真实 hidden state 的协方差谱呈现明显的 head-heavy 结构。
- 单纯去均值不足以显著释放 tail 语义；切除 top-$k$ shared head 后，残差空间的可分性会提高。
- 如果后续把 common / tail 分支分开，并给 tail 独立 WD / LR，则 rare / domain-specific 部分会先于完整 MoE 获得改善。

建模：
- 在 Qwen3-8B 的 `post-attention / pre-FFN` hidden state 上估计 $\mu$ 与 $\Sigma$，构造
$$
h_{tail} = (I - V_kV_k^\top)(h-\mu).
$$
- Common 数据使用 Wiki，Tail 数据使用 WoS 四领域文档；协方差由 `Wiki:WoS = 4:1` 的混合 token 池估计。
- 文档级线性 probe / router 采用 WoS domain label 作为主 proxy，比较 raw、centered 与 tail 三种空间。

具体实验：
1. 实验步骤：
   - 冻结 Qwen3-8B，扫描 4 个代表性层位，提取 `post-attention / pre-FFN` hidden states。
   - 在混合 token 池上估计每层的 $\mu$、$\Sigma$、eigenspectrum 与 $V_k$，并扫描 $k \in \{4, 8, 16, 32, 64\}$。
   - 对 WoS 文档构造 raw、centered、tail 三种表征，使用 mean pooling 得到文档级向量。
   - 在统一的 train / val / test 划分上训练同构线性 probe / router，比较三种空间的表现。
2. 实验指标：
   - eigenspectrum 与 explained variance。
   - $\mathrm{Sep}_F$。
   - WoS domain linear probe accuracy。
   - routing purity / NMI。
3. 实验结果：
   - 当前尚未运行；本文件给出的是真实模型阶段的首轮可执行设置。
   - 实验 A 的通过标准是：在至少一个层位和一个 $k$ 上，tail 空间相对 centered 在 probe accuracy 或 purity / NMI 上稳定提升，而单独去均值增益有限。
4. 实验结论：
   - 若实验 A 成立，则说明“表示层必须切除 shared head”不仅是 toy 现象，而是 Qwen3-8B 真实表征中的稳定结构。
   - 若实验 B 再成立，则说明“优化解耦”可以在真实模型中先于 MoE 直接保住 tail。

Next Step：
- 先执行实验 A，确定最优层位与 $k$；随后只在 1 个最佳层位上做 Split-FFN / decoupled-optim，对 rare / domain 指标做最小闭环验证。
