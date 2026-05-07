# Decoupled Architecture vs Coupled Architecture Toy Report

## 0. 现在在主线的哪里

我们现在不再只是分别讨论两个局部机制：

1. **稳态上限问题**：统一 Weight Decay 会压低低频、低方差 tail 的最终可学幅值。  
2. **动力学时间窗问题**：全局 Cosine Learning Rate 会在 tail 还没积累够有效更新之前就把步长降得太小。

现在进入的是**架构级合流阶段**：

> 不是再问 “WD 会不会伤 tail” 或 “LR decay 会不会让 tail 来不及学”，  
> 而是问：**如果把 Common 和 Tail 物理分开，并给 Tail 独立、宽松的优化条件，能不能在不伤 Common 的情况下把 Tail 救回来。**

这一步是从 **理论分解** 进入 **架构证明** 的第一个闭环 toy。

---

## 1. 目标

设计一个 **容量匹配** 的 PyTorch toy，对比：

- **Flat / Coupled**：Common 和 Tail 共享一套参数块、统一 Weight Decay、统一 Cosine LR。
- **Decoupled / Hierarchical**：Common 和 Tail 走不同分支，但整体函数类不变；Tail 分支拥有更小的 WD 和更长的 LR 时间窗。

我们要证明的不是 “多加参数更好”，而是：

> **同样的线性表达能力下，只要把 Common 和 Tail 物理分开，并给 Tail 独立优化条件，就能显著恢复 Tail 学习，而 Common 几乎不受影响。**

---

## 2. 假设

### H1. Coupled 会优先学满 Common
因为 common 特征高频、持续出现，Flat 模型在训练前期会很快把 common 权重推到接近 teacher。

### H2. Coupled 的 Tail 会在两重干扰下停住
- **Weight Decay** 持续把 tail 权重往 0 拉；
- **全局 Cosine LR** 很快把步长降小，使 rare tail 概念来不及积累够更新。

因此 Flat 的 tail curve 会表现为：**前期略涨，后期明显停住。**

### H3. 只松 WD 或只延长 Tail 的 LR，都只能部分救援
- 只降 WD：稳态 ceiling 变高，但时间窗仍受限；
- 只延长 LR：时间窗变长，但统一 WD 仍压着 tail 的最终幅值。

### H4. 同时做两件事，才会出现完整救援
即：
- Tail 分支更小的 WD
- Tail 分支延迟/独立的 LR 衰减

则 tail 学习曲线会继续上升到更高平台，而 common 基本不变。

---

## 3. 数学建模

### 3.1 数据生成

把输入拆成两部分：

$$
x = [c; t]
$$

其中：

- $c \in \mathbb{R}^{d_c}$：**Common 特征**，表示高频、共享、每步都能看到的模式。  
- $t \in \mathbb{R}^{K_t}$：**Tail 特征**，表示稀有语义概念；每个样本大多数时候没有 tail，少数时候只激活一个 tail 概念。

#### Common 分支
设：

$$
c_j \sim \mathcal{N}(0, \lambda^c_j)
$$

这里 $\lambda^c_j$ 是 common 第 $j$ 个方向的方差，表示这个方向在训练里有多常见、多稳定。

本 toy 使用：

$$
\lambda^c = [1.5, 1.0, 0.7, 0.5]
$$

#### Tail 分支
总 tail 出现概率设为：

$$
p_{tail} = 0.15
$$

一旦 tail 出现，就从 $K_t=12$ 个 tail 概念里按 Zipf 分布采样：

$$
q_k \propto k^{-1.5}
$$

然后只激活对应的一个维度：

$$
t = a \cdot e_k, \qquad a \sim \mathcal{N}(0,1)
$$

这意味着：

- 越稀有的概念，出现频率越低；
- 对应坐标的**有效方差**也越低；
- rare tail 概念天然需要更多训练步才能积累足够更新。

#### Teacher
标签由 common 和 tail 两部分共同决定：

$$
y = \beta_c^\top c + \beta_t^\top t + \epsilon
$$

其中：

- $\beta_c$：common teacher 权重
- $\beta_t$：tail teacher 权重
- $\epsilon \sim \mathcal{N}(0, 0.05^2)$：小噪声

在实现里，我们把 $\beta_c, \beta_t$ 采样为正值，并缩放到：

- common 输出方差约为 1
- tail 输出方差约为 1

这样可以保证：**tail 不是“本来就不重要”**，它只是更稀有、更难学。

---

### 3.2 两种架构

#### Coupled / Flat
用一个线性层同时处理 common 和 tail：

$$
f_{flat}(x) = w^\top x = w_c^\top c + w_t^\top t
$$

#### Decoupled / Hierarchical
显式拆成两个分支，再把输出相加：

$$
f_{dec}(x) = w_c^\top c + w_t^\top t
$$

注意：**函数形式和 Flat 完全一样。**

区别不在表达能力，而在于：

- Flat：只有一套优化条件；
- Decoupled：可以给 $w_c$ 和 $w_t$ 不同的 WD 和 LR schedule。

这正是我们想要证明的点：  
> **改进来自物理解耦后的优化自由度，而不是来自额外容量。**

---

### 3.3 优化设置

总训练步数：

$$
T = 1500
$$

基础学习率：

$$
\eta_0 = 0.2
$$

Common 的 Weight Decay：

$$
\gamma_c = 5 \times 10^{-3}
$$

Tail 的低 WD 设置：

$$
\gamma_t = 2 \times 10^{-4}
$$

#### Flat 的 LR
Flat 用统一 Cosine：

$$
\eta_{flat}(t) = \frac{\eta_0}2\Bigl(1 + \cos(\pi t / T)\Bigr)
$$

#### Decoupled Tail 的 LR
Tail 用“先保持，再衰减”的 schedule：

- 前 $80\%$ 训练步保持高 LR
- 最后 $20\%$ 再做 Cosine 衰减

记 hold ratio 为 $r=0.8$，则：

$$
\eta_t(t)=
\begin{cases}
\eta_0, & t < rT \\
\frac{\eta_0}2\left(1+\cos\left(\pi \frac{t-rT}{(1-r)T}\right)\right), & t \ge rT
\end{cases}
$$

它的物理含义非常直接：

- Common 早就该学完了，所以全局 LR 可以早点降；
- Tail 由于概念稀有、更新稀疏，必须保留更长的有效学习窗口。

---

### 3.4 理论解释：为什么 rare tail 在统一 WD / LR 下学不到

为了把 toy 的结论说清楚，可以先看单个坐标 $j$ 的期望动力学。

设 teacher 为：
$$
y = \beta^\top x + \epsilon
$$

student 为线性模型：
$$
\hat y = w^\top x
$$

对单个坐标 $j$，记其输入方差为：
$$
\sigma_j^2 = \mathbb{E}[x_j^2]
$$

在平方损失加 Weight Decay $\gamma$ 下，该坐标对应的目标可写为：
$$
\mathcal{L}_j(w_j)
= \frac12 \sigma_j^2 (w_j-\beta_j)^2 + \frac{\gamma}{2} w_j^2
$$

因此其梯度为：
$$
\frac{\partial \mathcal{L}_j}{\partial w_j}
= \sigma_j^2 (w_j-\beta_j) + \gamma w_j
= (\sigma_j^2+\gamma)w_j - \sigma_j^2 \beta_j
$$

若第 $s$ 步学习率记为 $\eta(s)$，则梯度下降更新满足：
$$
w_j(s+1)
= \bigl(1-\eta(s)(\sigma_j^2+\gamma)\bigr) w_j(s)
+ \eta(s)\sigma_j^2 \beta_j
$$

这个公式直接给出两条结论。

#### 结论 1：Weight Decay 会压低 low-variance 坐标的稳态上限

若先看恒定学习率下的平衡点 $w_j^*$，则有：
$$
w_j^* = \frac{\sigma_j^2}{\sigma_j^2+\gamma}\beta_j
$$

因此：
- 对 common 坐标，$\sigma_j^2$ 大，所以 $w_j^* \approx \beta_j$；
- 对 tail 坐标，$\sigma_j^2$ 小，所以 $w_j^*$ 会被明显压低。

在本 toy 中，common 坐标始终出现，其方差就是预设的 $\lambda_j^c$；而第 $k$ 个 tail 坐标只在少数样本上被激活，满足：
$$
t_k =
\begin{cases}
a, & \text{以概率 } p_{\text{tail}} q_k \\
0, & \text{否则}
\end{cases}
\qquad a \sim \mathcal{N}(0,1)
$$

所以：
$$
\sigma_k^2 = \operatorname{Var}(t_k) = p_{\text{tail}} q_k
$$

又因为 $q_k$ 服从 Zipf 分布，越 rare 的 tail 概念，$q_k$ 越小，于是：
$$
w_k^* = \frac{p_{\text{tail}} q_k}{p_{\text{tail}} q_k+\gamma}\beta_k
$$

这说明统一 WD 对 rare tail 的压制最强。

#### 结论 2：全局 LR 衰减会提前关闭 tail 的有效学习窗口

将误差定义为：
$$
e_j(s) = w_j(s) - w_j^*
$$

则有：
$$
e_j(s+1)
= \bigl(1-\eta(s)(\sigma_j^2+\gamma)\bigr)e_j(s)
$$

展开到第 $T$ 步：
$$
e_j(T)
= e_j(0)\prod_{s=0}^{T-1}\bigl(1-\eta(s)(\sigma_j^2+\gamma)\bigr)
$$

当学习率较小时，可近似写成：
$$
e_j(T)
\approx e_j(0)\exp\left(-(\sigma_j^2+\gamma)\sum_{s=0}^{T-1}\eta(s)\right)
$$

这说明坐标 $j$ 能否学出来，取决于它获得的有效学习预算
$$
\sigma_j^2 \sum_{s=0}^{T-1}\eta(s)
$$

对 common 坐标，这个量较大，因此在全局 Cosine 早期就能迅速收敛；  
对 tail 坐标，尤其是 rare tail，这个量很小，因此它需要更长的高学习率时间窗来积累更新。

因此，rare tail 学不到，不是因为它在 teacher 中“不重要”，而是因为：
- 它的出现概率低，导致 $\sigma_j^2$ 小；
- 每一步得到的有效梯度弱；
- 统一 WD 持续把它往 0 拉；
- 全局 LR decay 又在它积累够更新之前提前关窗。

这正是本 toy 中 `Decoupled-WD`、`Decoupled-LR` 与 `Decoupled-Full` 三组对照成立的动力学基础。

---

### 3.5 指标

我们主要跟踪 **Coefficient Survival Rate**：

对某个组 $G$（Common、Tail 或 Rare-Tail），定义：

$$
S_{coef}^G(t) = \frac{\langle w_G(t), \beta_G \rangle}{\|\beta_G\|_2^2}
$$

#### 这个指标的物理意义
- $\beta_G$：teacher 真正需要的那组权重；
- $w_G(t)$：模型在第 $t$ 步学出来的那组权重；
- 内积越大，说明模型越接近 teacher；
- 归一化后，$S_{coef}^G(t)=1$ 表示“完全恢复 teacher”。

本 toy 里 teacher 权重取正值，所以这个指标很好读：

- 接近 1：这一组信号基本学到了；
- 明显低于 1：这一组还没学满，或被 WD/LR 干扰压住了。

另外还看测试集上的：

- **Overall MSE**
- **Common MSE**
- **Tail MSE**

其中 Tail MSE 是最重要的功能性指标，因为它直接告诉我们：  
> **Tail 分支到底有没有被学出来。**

---

## 4. 实验

### 4.1 配置

我们跑了 4 组配置，3 个随机种子取均值和标准差。

1. **Flat**
   - 单一线性层
   - 统一 WD = $5e-3$
   - 统一 Cosine LR

2. **Decoupled-WD**
   - Common / Tail 两个分支
   - Common WD = $5e-3$
   - Tail WD = $2e-4$
   - 两个分支都用同一个 Cosine LR

3. **Decoupled-LR**
   - Common / Tail 两个分支
   - Common WD = Tail WD = $5e-3$
   - Common 用 Cosine LR
   - Tail 用延迟衰减 LR

4. **Decoupled-Full**
   - Common / Tail 两个分支
   - Common WD = $5e-3$
   - Tail WD = $2e-4$
   - Common 用 Cosine LR
   - Tail 用延迟衰减 LR

### 4.2 实验步骤

1. 采样 teacher 和 Zipf tail 分布。  
2. 生成训练流：每步 64 个样本，共 1500 步。  
3. 对每个配置，用 SGD 训练。  
4. 每一步记录：
   - Common survival
   - Tail survival
   - Rare-tail survival
   - train loss
   - common / tail LR
5. 在独立测试集上评估：
   - overall MSE
   - common MSE
   - tail MSE
   - final survival

---

## 5. 结果

### 5.1 汇总表

| 配置 | Overall MSE | Common MSE | Tail MSE | Common Survival | Tail Survival | Rare-Tail Survival |
|---|---:|---:|---:|---:|---:|---:|
| Flat (统一WD + 全局Cosine) | 0.0664±0.0037 | 0.000046±0.000023 | 0.0637±0.0039 | 0.9956±0.0028 | 0.5900±0.0150 | 0.3519±0.0172 |
| Decoupled-WD (尾部分支低WD) | 0.0326±0.0037 | 0.000026±0.000011 | 0.0300±0.0039 | 0.9967±0.0017 | 0.7278±0.0162 | 0.4786±0.0252 |
| Decoupled-LR (尾部分支延迟LR衰减) | 0.0527±0.0016 | 0.000040±0.000018 | 0.0501±0.0018 | 0.9956±0.0025 | 0.6359±0.0071 | 0.4385±0.0233 |
| Decoupled-Full (低WD + 延迟LR) | 0.0120±0.0018 | 0.000014±0.000005 | 0.0094±0.0019 | 0.9969±0.0009 | 0.8535±0.0093 | 0.6829±0.0272 |

### 5.2 结果读法

#### 结论 1：Common 几乎不受影响
四个配置的 common survival 都在 **0.995~0.997** 左右，common MSE 都接近 0。  
这说明：**Decoupled 并没有靠牺牲 Common 来换 Tail。**

#### 结论 2：Flat 的 Tail 明显停住
Flat 的最终：
- Tail survival = **0.5900**
- Rare-tail survival = **0.3519**

这说明在统一 WD + 全局 Cosine 下，tail 只学到一部分，而且越稀有的 tail 越难学。

#### 结论 3：只改一项，只能部分救援
- Decoupled-WD：Tail survival = **0.7278**
- Decoupled-LR：Tail survival = **0.6359**

二者都比 Flat 好，但都没有达到 Full 的效果。  
这正好对应你们现在的两条干扰机制：

- WD-only 主要放松了稳态 ceiling；
- LR-only 主要延长了 tail 的动力学时间窗；
- 两者缺一不可。

#### 结论 4：Full Decoupling 才是完整救援
Decoupled-Full 的最终：
- Tail survival = **0.8535**
- Rare-tail survival = **0.6829**
- Tail MSE = **0.0094**

相对 Flat：

- Tail survival 从 **0.5900** 提升到 **0.8535**
- Rare-tail survival 从 **0.3519** 提升到 **0.6829**
- Tail MSE 从 **0.0637** 降到 **0.0094**

这是非常直接的架构级证据：

> **只要把 Common 和 Tail 物理分开，并给 Tail 更小的 WD 和更长的 LR 时间窗，就能大幅恢复 Tail 学习，而且 Common 基本不受伤。**

---

## 6. 证明 thesis 最关键的曲线形状

给导师汇报时，最该强调的是这三种形状：

### Shape A：Flat-common 先冲顶
Flat 的 common survival 在前 100 步左右就接近 1。  
这说明 common 是“容易、频繁、先学完”的那部分。

### Shape B：Flat-tail 先涨后停
Flat 的 tail survival 在前期会涨，但随着 Cosine LR 下降，后面逐渐进入平台。  
这是 **“时间窗提前关闭”** 的直接形状证据。

### Shape C：Decoupled-full 的 tail 持续上升更久
Full decoupling 下，tail curve 会在 Flat 已经停住的时候继续上升。  
这对应两件事同时发生：

- 小 WD 让 tail 的稳态 ceiling 更高；
- 持续 LR 让 rare tail 还有时间继续积累更新。

---

## 7. 结论

这个 toy 已经给出一个很干净的架构级闭环：

1. **表达能力不是关键差别**  
   Flat 和 Decoupled 的函数类完全一样，都是线性和式。

2. **优化条件才是关键差别**  
   一旦 Tail 拥有独立的 WD 和 LR 时间窗，它就能显著恢复，而 Common 不受影响。

3. **这直接支持 Hierarchical MoE 的物理主张**  
   不是“多几个 expert 就好”，而是：
   - Common 和 Tail 必须物理分开
   - Tail 必须拥有独立、宽松的优化生存条件

---

## 8. 文件说明

- 代码：`code/toy_decoupled_vs_coupled.py`
- 逐 seed 结果：`results/per_seed_results.csv`
- 汇总结果：`results/final_results_mean_std.csv`
- 平均曲线：`results/mean_curve_*.csv`
- 关键图：
  - `figures/common_survival_curve.png`
  - `figures/tail_survival_curve.png`
  - `figures/rare_tail_survival_curve.png`
  - `figures/lr_common_curve.png`
  - `figures/lr_tail_curve.png`
  - `figures/train_loss_curve.png`

---

## 9. 汇报摘要

[exp1：toy model]

目的：完成 Common / Tail 在统一 Weight Decay 与全局 Learning Rate 衰减下的 long-tail 仿真实验，验证“物理解耦 + 优化解耦”能够显著恢复 tail 学习。

假设：
- 统一 Weight Decay 会压低低频 tail 的稳态上限。
- 全局 Cosine Learning Rate 会过早关闭 tail 的有效学习时间窗。
- 仅放松 WD 或仅延长 tail 的 LR 时间窗，都只能部分救援。
- 只有同时解耦 WD 与 LR，才能显著恢复 tail，而不牺牲 common。

建模：
- 输入分解为 $x = [c; t]$。其中 $c$ 表示高频 common 特征，$t$ 表示稀有 tail 特征。
- Tail 总出现概率设为 $p_{tail}=0.15$，并在 $K_t=12$ 个概念上按 Zipf 分布 $q_k \propto k^{-1.5}$ 采样。
- 教师模型为 $y=\beta_c^\top c+\beta_t^\top t+\epsilon$，并将 common / tail 输出方差归一到同量级，保证 tail 是“重要但稀有”，而不是“天然不重要”。
- 对比 Flat 与 Decoupled 两种线性结构。二者函数类相同，唯一区别是 Tail 是否拥有独立的 WD 与 LR schedule。

具体实验：
1. 实验步骤：
   - 固定总训练步数为 1500，batch size 为 64，使用 3 个随机种子。
   - 比较 4 组配置：Flat、Decoupled-WD、Decoupled-LR、Decoupled-Full。
   - Flat 使用统一 `WD=5e-3` 与全局 Cosine LR；Decoupled-Full 使用 `common WD=5e-3`、`tail WD=2e-4`，common 用 Cosine，tail 用“前 80% 保持高 LR、后 20% 再 Cosine”的 schedule。
2. 实验指标：
   - Overall / Common / Tail MSE。
   - Common / Tail / Rare-tail coefficient survival。
   - Survival 曲线与 LR 曲线形状。
3. 实验结果：
   - Flat：Tail survival = 0.5900，Rare-tail survival = 0.3519，Tail MSE = 0.0637。
   - Decoupled-WD：Tail survival = 0.7278，Rare-tail survival = 0.4786，Tail MSE = 0.0300。
   - Decoupled-LR：Tail survival = 0.6359，Rare-tail survival = 0.4385，Tail MSE = 0.0501。
   - Decoupled-Full：Tail survival = 0.8535，Rare-tail survival = 0.6829，Tail MSE = 0.0094。
   - 四组配置的 Common survival 均稳定在约 0.996 附近，说明 Tail 的恢复并未以牺牲 Common 为代价。
4. 实验结论：
   - Flat 的失败不是表达能力不足，而是统一优化条件导致 tail 同时遭受“稳态压制”与“时间窗冻结”。
   - WD 解耦与 LR 解耦各自只解决一半问题；二者必须同时存在。
   - 该 toy 已形成对命题 C 的直接架构级证据，并为后续 Hierarchical / Decoupled MoE 提供必要性支撑。

Next Step：
- 进入冻结真实表征验证阶段：使用 Qwen3-8B 提取 hidden states，在 Wiki / WoS 上验证 shared head 是否存在，并比较 raw / centered / tail residual 三种空间上的 probe 准确率与 routing purity。
