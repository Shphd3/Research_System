# Round3 实验分析报告：谱空间正交化与遗忘抵抗（含 Margin 分析）

## 1. 实验概述

### 1.1 实验目标
验证 **H1e（谱空间容量未饱和假说）**：
- 低秩路由通过压低 ED，使得每个专家仅在极少数 Spike 方向上建立激活响应
- 保留海量正交零空间 (Orthogonal Null Space)
- 当新任务（Domain Shift）到来时，新任务特征大概率落在未被占据的正交方向上
- 从而避免了对旧知识主轴的谱干扰（Spectral Interference）

### 1.2 新增需求：Margin 分析
根据用户需求，增加了对 **Router Margin** 的分析：
- **Margin 定义**：$Margin = \text{Top-1 Logit} - \text{Top-2 Logit}$
- **物理意义**：衡量路由决策的确信度。Margin 越大，路由决策越确信

### 1.3 核心指标

**谱干扰度 (Spectral Interference, $\mathcal{I}$)**：
$$\mathcal{I}_i = \frac{\text{Tr}(C_{A,i} \cdot C_{B,i})}{\|C_{A,i}\|_F \cdot \|C_{B,i}\|_F}$$

- $C_{A,i}$: Domain A (Engineering: CS, Civil, ECE, MAE) 数据在专家 $i$ 的输入协方差矩阵
- $C_{B,i}$: Domain B (Medical/Life Sciences: Medical, Psychology, biochemistry) 数据在专家 $i$ 的输入协方差矩阵
- $\mathcal{I}_i \in [0, 1]$：值越低表示两个领域的干扰越小

### 1.4 验证标准
- 如果 $\bar{\mathcal{I}}(low\_rank) \ll \bar{\mathcal{I}}(linear)$，则 H1e 成立。
- 如果 Low-rank 的 Margin 明显大于 Linear，说明低秩路由决策更确信。

---

## 2. 实验设置

### 2.1 数据集与领域划分

| 参数 | 值 |
|:--|:--|
| **Dataset** | WOS (Web of Science) |
| **Domain A** | CS, Civil, ECE, MAE (Engineering) |
| **Domain B** | Medical, Psychology, biochemistry (Medical/Life Sciences) |
| **max_samples_per_domain** | 64 |
| **batch_size** | 2 |
| **max_length** | 128 |
| **ed_chunk_size** | 256 |
| **layers** | 2, 6, 10 |
| **checkpoints** | 50000, 60000 |

### 2.2 模型对比

| 模型 | 描述 |
|:--|:--|
| **linear_running_center** | 全秩路由器，使用 center running 机制 |
| **low_rank_running_center** | 低秩路由器 (rank=115)，使用 center running 机制 |

---

## 3. 实验结果

### 3.1 总体结果

| 模型 | ckpt=50000 | ckpt=60000 | SI 变化 | Margin (ckpt=50000) | Margin (ckpt=60000) |
|:--|--:|--:|--:|--:|--:|
| **Linear** | 0.6687 | 0.6678 | -0.0009 | 1.7297 | 1.7531 |
| **Low-rank** | 0.7021 | 0.6990 | -0.0031 | 1.8284 | 1.8668 |
| **Delta (Low-rank - Linear)** | **+0.0333** | **+0.0312** | -0.0021 | **+0.0987** | **+0.1138** |

### 3.2 分层 Spectral Interference 结果

#### ckpt=50000

| Layer | Linear | Low-rank | Delta |
|:--|--:|--:|--:|
| L2 | 0.6782 | 0.7205 | +0.0423 |
| L6 | 0.6753 | 0.7238 | +0.0485 |
| L10 | 0.6526 | 0.6618 | +0.0092 |

#### ckpt=60000

| Layer | Linear | Low-rank | Delta |
|:--|--:|--:|--:|
| L2 | 0.6703 | 0.7248 | +0.0545 |
| L6 | 0.6873 | 0.7164 | +0.0290 |
| L10 | 0.6458 | 0.6558 | +0.0100 |

### 3.3 分层 Margin 结果

#### ckpt=50000

| Layer | Linear (A) | Linear (B) | Low-rank (A) | Low-rank (B) |
|:--|--:|--:|--:|--:|
| L2 | 1.7518 | 1.5671 | 1.7600 | 1.7351 |
| L6 | 0.9660 | 1.1424 | 1.5499 | 1.6489 |
| L10 | 2.4672 | 2.4836 | 2.1499 | 2.1267 |

#### ckpt=60000

| Layer | Linear (A) | Linear (B) | Low-rank (A) | Low-rank (B) |
|:--|--:|--:|--:|--:|
| L2 | 1.7858 | 1.5825 | 1.8100 | 1.7846 |
| L6 | 1.0013 | 1.1757 | 1.6206 | 1.6471 |
| L10 | 2.4378 | 2.5352 | 2.1701 | 2.1684 |

---

## 4. 关键发现

### 4.1 H1e 验证结果：**未获支持** ❌

**核心结论**：低秩模型的谱干扰度 **高于** 线性模型（Delta > 0），H1e 假设 **未获支持**。

具体表现为：
- 两个 checkpoint 上，Low-rank 的 $\mathcal{I}$ 均比 Linear 高约 **0.03**
- 在所有三层上，Low-rank 的干扰度均高于或接近 Linear
- Layer 6 差异最大（ckpt50000: Δ=+0.0485, ckpt60000: Δ=+0.0290）

### 4.2 Margin 分析：**Low-rank 路由更确信** ✅

**意外发现**：虽然 H1e 未获支持，但 Low-rank 模型的 Margin **显著高于** Linear 模型：
- ckpt=50000: Delta Margin = +0.0987
- ckpt=60000: Delta Margin = +0.1138

这说明低秩路由器在做路由决策时 **更加确信**。

### 4.3 深层分析

**为什么低秩路由的谱干扰更高？**

可能的解释：
1. **低秩约束强制路由决策依赖少数方向**：低秩路由器只利用 Spike 方向进行决策，当两个不同领域都落在相似的 Spike 方向上时，会被路由到同一个专家，导致干扰增加。

2. **全秩路由有更多自由度**：线性路由器可以同时考虑更多特征方向，能够更好地区分不同领域的细微差异，从而将它们分配给不同的专家。

3. **"容量未饱和"假设的反面**：H1e 假设低秩保留的正交零空间可以避免干扰，但实际数据显示这些正交空间可能并不是真正"空闲"的。

**为什么低秩路由的 Margin 更大？**

可能的解释：
1. **低秩投影产生更极值的 logits**：由于低秩投影（down_proj + up_proj）会压缩信息，可能导致 Top-1 与 Top-2 的差异更加明显。

2. **专家选择更极端**：低秩路由在少数方向上决策，可能导致路由结果更偏向特定专家，形成更大的 Margin。

### 4.4 与 H1b 的关联

| 假设 | 状态 | 说明 |
|:--|:--|:--|
| **H1b** (ED压缩) | ✅ 支持 | 低秩路由确实降低了 ED |
| **H1e** (谱干扰降低) | ❌ 不支持 | 低秩路由反而增加了谱干扰 |
| **H1e (Margin)** | ✅ 新发现 | 低秩路由决策更确信 |

这表明 **ED 降低 ≠ 谱干扰降低**，但 **ED 降低可能与 Margin 增大相关**。

---

## 5. 图表

![Spectral Interference Comparison](round3_spectral_interference_comparison.png)

**图表说明**：
- **左上**：ckpt=50000 分层 Spectral Interference 对比
- **右上**：ckpt=60000 分层 Spectral Interference 对比
- **左中**：两 checkpoint 的平均 Spectral Interference 对比
- **右中**：Delta SI 变化（>0 表示低秩干扰更大）
- **左下**：Router Margin 对比
- **右下**：Delta SI vs Delta Margin 对比

---

## 6. 结论与后续

### 6.1 主要结论

1. **H1e 未获支持**：低秩路由并没有减少跨领域谱干扰，反而略有增加（Delta SI ≈ +0.03）
2. **Margin 意外发现**：低秩路由的 Margin 显著高于线性模型（Delta Margin ≈ +0.1）
3. **训练曲线稳定**：两模型的 $\mathcal{I}$ 在 50k→60k 区间均略有下降，趋于稳定
4. **分层差异**：Layer 6 的差异最大，可能与该层的表征特性有关

### 6.2 假设更新

| 假设 | 状态 | 说明 |
|:--|:--|:--|
| H1a (Spike双重属性) | 活跃 | 继续指导后续研究 |
| H1b (ED压缩) | ✅ 已实证 | 低秩有效降低ED |
| H1c (参数更新限制) | 活跃 | 需进一步验证 |
| **H1e (谱干扰降低)** | ❌ **未获支持** | 需重新审视因果链 |
| **H1e (Margin)** | ✅ **新发现** | 低秩路由更确信 |
| H1d (抗噪性) | 降级 | Round2显示无显著差异 |

### 6.3 后续建议

1. **重新审视 H1e 的数学模型**：当前的 $\mathcal{I}$ 公式可能需要修正，考虑归一化或其他因素

2. **探索不同的 Domain 划分**：当前 Domain A 和 B 可能仍有较多重叠，选择更无交集的领域可能得到不同结果

3. **分析专家负载分布**：低秩路由的 CV_load 更低（Round1 结果），但这与谱干扰的关系需要进一步研究

4. **考虑 Margin 与谱干扰的关联**：Margin 增大可能是低秩路由的固有特性，但这与谱干扰增加的关系需要进一步研究

5. **考虑时间维度**：持续学习的防遗忘不仅涉及谱干扰，还涉及权重更新的方向与幅度

---

## 7. 产物路径

| 产物 | 路径 |
|:--|:--|
| 实验代码 | `/data/250010109/spectral_router/exp_expert_lowrank/scripts/round3/run_round3_spectral_interference.py` |
| RouterDataCollector 修复 | `/data/250010109/spectral_router/router_eval/eval_utils.py` |
| ckpt50000 结果 | `/data/250010109/spectral_router/exp_expert_lowrank/output/round3_spectral_interference_ckpt50000_v2` |
| ckpt60000 结果 | `/data/250010109/spectral_router/exp_expert_lowrank/output/round3_spectral_interference_ckpt60000_v2` |
| 结果图表 | `/data/250010109/spectral_router/exp_expert_lowrank/docs/round3_spectral_interference/round3_spectral_interference_comparison.png` |
| 本报告 | `/data/250010109/spectral_router/exp_expert_lowrank/docs/round3_spectral_interference/experiment_report.md` |

---

## 8. 技术细节

### 8.1 Margin 计算公式

```python
def compute_margin(logits: torch.Tensor) -> torch.Tensor:
    sorted_logits, _ = torch.sort(logits, dim=-1, descending=True)
    margin = sorted_logits[:, 0] - sorted_logits[:, 1]
    return margin
```

### 8.2 RouterDataCollector 修复

问题：原 `RouterDataCollector` 只支持 `gate` 和 `router` 属性，不支持 `low_rank_router`。

修复：增加了对 `low_rank_router.up_proj` 的 hook 注册。

```python
if hasattr(mlp, "low_rank_router"):
    self.register_hook(mlp.low_rank_router.up_proj, i, "low_rank")
elif hasattr(mlp, "router"):
    self.register_hook(mlp.router.router_linear, i, "spectral")
elif hasattr(mlp, "gate"):
    self.register_hook(mlp.gate, i, "standard")
```
