# [调研]MoE

你好！你提出的关于“梯度更新受阻”的隐患以及“引入线性层 + Sigmoid 进行噪声抑制”的构想，非常深刻且直击要害。在将纯数学的 SVD 切分转化为可通过反向传播优化的网络结构时，我们确实面临着**几何约束（Geometric Constraints）与优化动力学（Optimization Dynamics）之间的权衡** 。

在给出具体的实验步骤之前，我们先用严格的数学语言来剖析你提出的这两种架构的优劣，这将直接决定我们实验中的对比模型设计。

---

### 1. 理论分析：低秩瓶颈 (Low-Rank) vs. 动态噪声抑制 (Noise Suppression)

假设输入特征为 $x \in \mathbb{R}^d$（已去均值），目标是输出路由概率（Logits） $z \in \mathbb{R}^E$，其中 $E$ 是专家数量。

#### A. 方案一：低秩路由 (Low-Rank Router)
设定 $W_g = A B^T$，其中 $A \in \mathbb{R}^{d \times r}, B \in \mathbb{R}^{r \times E}$，且 $r \ll d$。
$$z = (A B^T)^T x = B A^T x$$
* **几何本质**：这是一个显式的正交投影（如果 $A$ 被正交化）加仿射变换。网络强制先将 $x$ 投影到由 $A$ 的列向量张成的 $r$ 维子空间中，过滤掉剩下的 $(d-r)$ 维信息，然后再映射到 $E$ 个专家。
* **优化动力学（受阻分析）**：令损失函数为 $\mathcal{L}$。路由对输入特征的梯度为 $\nabla_x \mathcal{L} = A B^T \nabla_z \mathcal{L}$。由于 $A B^T$ 的秩最大为 $r$，这意味着**由 Router 传导回主干网络（LLM 中间层）的梯度永远被压缩在一个 $r$ 维的子空间内**。如果这个 $r$ 维空间与主干网络当前演化的主方向发生偏离，梯度就会被严重“截断”，导致上游表示无法根据路由结果进行充分的自我修正。

#### B. 方案二：动态噪声抑制 (Soft-Gated Denoising Router)
受你提及的特征门控（Gated Attention）等思想的启发，我们引入一个依赖于输入的动态阈值：
$$g = \sigma(W_d x) \in \mathbb{R}^d$$
$$x_{denoised} = g \odot x$$
$$z = W_{gate} x_{denoised}$$
其中 $W_d \in \mathbb{R}^{d \times d}$ 是降噪感知矩阵，$\odot$ 是逐元素乘法。
* **几何本质**：这是一个基于标准基底（Standard Basis）的各向异性缩放。Sigmoid 使 $g_i \in (0, 1)$。网络可以学习对噪声维度输出接近 0 的门控值。
* **优化动力学**：梯度流更加平滑，保留了全量维度 $d$ 的反向传播路径，不会遭遇硬性的低秩秩塌陷，收敛通常更稳定。
* **核心缺陷（坐标轴对齐限制）**：由于 $\odot$ 是逐特征维度（Feature-wise）的，**它只能沿着标准坐标轴（Standard Axes）进行过滤**。我们在 SVD 分析中发现，Spike 和 Tail 是由标准基底线性组合（旋转）而来的正交方向。如果一个纯粹的噪声方向 $v_{tail}$ 并不是恰好平行于某一个神经元特征轴，而是横跨了多个特征轴，逐元素 Sigmoid 将**无法在不伤害 Spike 信息的前提下，干净地切除该 Tail 噪声**。

#### C. 理论折中：正交软阈值化 (Orthogonal Soft-Thresholding)
为了兼顾 SVD 的正交过滤与 Sigmoid 的平滑梯度，数学上更优雅的形式是学习一个投影矩阵和对应的低维软门控，但这在工程上等价于带有 SwiGLU/GeLU 激活函数的两层 MLP。因此，我们本轮实验将包含**低秩**与**动态门控**两者的对比。

---

### 2. 实验设计 (Experiment Design: Round 4)

为了让实验 Agent 能够直接执行，以下是细化后的实验步骤与严密的量化指标。我们将以 WoS 分类任务作为“理想语义分发”的代理（Proxy），观察不同降噪策略如何影响负载均衡和专家特征的内在秩。

#### 2.1 实验对象与对照组 (Baselines & Models)
使用已提取并去均值的`layer_4``layer_18` `layer_30` 特征数据：$X \in \mathbb{R}^{N \times 128}$，标签 $Y \in \{0, 1, 2, 3\}$（模拟 4 个 Expert）。

定义三种 Router 结构（均不使用任何负载均衡 Auxiliary Loss）：
1.  **Baseline (Full-Rank)**: $\hat{Y} = W X$，其中 $W \in \mathbb{R}^{4 \times 128}$。
2.  **Variant A (Low-Rank, $r=16$)**: $\hat{Y} = B A^T X$，其中 $A \in \mathbb{R}^{128 \times 16}, B \in \mathbb{R}^{16 \times 4}$。
3.  **Variant B (Gated Suppression)**: $\hat{Y} = W_{gate} (X \odot \sigma(W_d X))$，其中 $W_d \in \mathbb{R}^{128 \times 128}, W_{gate} \in \mathbb{R}^{4 \times 128}$。

#### 2.2 训练规程 (Training Protocol)
* **目标函数**：标准的交叉熵损失 (Cross-Entropy Loss)。
* **训练细节**：划分 Train(80%)/Test(20%)。使用 AdamW 优化器，为了凸显梯度动力学差异，记录并保存每个 epoch 的 Test Loss 和 Test Accuracy。

#### 2.3 核心量化指标 (Quantitative Metrics)

**指标一：正确分发纯度 (Routing Accuracy)**
* 直接使用 Test Accuracy。
* *期望*：Variant A 和 B 应该接近 Baseline，证明过滤噪声并未损害核心语义。

**指标二：无辅助惩罚下的负载均衡度 (Unpenalized Load CV)**
* **定义**：将 Test 集样本送入训练好的模型，记录模型预测的最大概率类别作为其被分发的 Expert ID。统计 4 个 Expert 分配到的样本数 $[N_1, N_2, N_3, N_4]$。
* **公式**：计算变异系数 $CV = \frac{\sigma(N)}{\mu(N)}$。
* *数学意义*：越接近 0，说明在没有数学惩罚项的自然状态下，分发越均衡。
* *期望*：$CV(Variant A) \le CV(Variant B) < CV(Baseline)$。Baseline 因为受到 Deep Tail 的全秩干扰，极易在早期发生某个类别预测坍塌。

**指标三：专家输入特征有效维度 (Expert Intrinsic Effective Dimension)** 
这是本轮最具理论深度的指标，用于验证“专家低秩性”。
* **定义**：对于被模型分配给第 $m$ 个 Expert 的所有 Test 样本集合 $X^{(m)}$（注意，提取的是它们**原始的、未被 Router 降维的 128 维特征**）。
* **计算步骤**：
    1.  对 $X^{(m)}$ 计算协方差矩阵 $\Sigma^{(m)} \in \mathbb{R}^{128 \times 128}$。
    2.  计算 $\Sigma^{(m)}$ 的特征值 $\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_{128}$。
    3.  计算有效维度：$ED_m = \frac{(\sum \lambda_i)^2}{\sum \lambda_i^2}$。
* *数学意义*：如果 $ED$ 很低（如接近 10~20），说明该 Expert 接收到的数据**在原始几何空间中极度集中于一个低维流形上**。
* *期望*：对于纯净的语义分发，我们期望各专家的 $\text{Mean}(ED)$ 显著下降。

#### 2.4 Agent 伪代码指南

你可以将以下核心逻辑传达给 Agent：

```python
# 1. 定义三个模型
class FullRankRouter(nn.Module):
    def __init__(self): ...
class LowRankRouter(nn.Module):
    def __init__(self, r=16): ...
class GatedRouter(nn.Module):
    def __init__(self): ...

# 2. 训练循环 (只用 CE Loss, 绝无 Aux Loss)
for model in [FullRankRouter, LowRankRouter, GatedRouter]:
    train_model(model, train_loader, epochs=50)
    
    # 3. 计算指标
    preds = get_predictions(model, test_loader) # shape (N_test,)
    
    # 指标 1 & 2
    acc = accuracy_score(y_test, preds)
    counts = np.bincount(preds, minlength=4)
    cv = np.std(counts) / np.mean(counts)
    
    # 指标 3: 专家特征有效秩 (Effective Dimension)
    ed_list = []
    for expert_id in range(4):
        # 提取被分发到当前 expert 的原始 Test 特征
        expert_features = X_test[preds == expert_id] 
        if len(expert_features) > 10: # 避免空簇
            cov = torch.cov(expert_features.T)
            eigenvalues = torch.linalg.eigvalsh(cov)
            # 保证特征值非负 (数值稳定性)
            eigenvalues = torch.clamp(eigenvalues, min=0.0)
            ed = (torch.sum(eigenvalues)**2) / torch.sum(eigenvalues**2)
            ed_list.append(ed.item())
            
    mean_ed = np.mean(ed_list)
    print(f"Model: {model_name} | Acc: {acc:.4f} | Load CV: {cv:.4f} | Mean ED: {mean_ed:.2f}")
```

通过这套严密的体系，我们将能看到“纯粹的分类表现”与“底层流形结构变化”之间的联系。你认为这份包含梯度动力学剖析与三重指标构建的设计，是否足够支撑起 Round 4 的实验需求？