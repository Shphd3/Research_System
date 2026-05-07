# Toy Experiment 报告（已执行）

## 背景主线
MoE 的核心不是把 token 分给更多 expert，而是先把表示中的共享部分和长尾语义部分分开，再让 router 在真正有区分力的 residual 上工作。  
Todo3 要验证：去掉 centered covariance 的 shared head 后，语义相关的 separability 是否提升。  
Todo2 要验证：global tail 之后，如果 residual 里仍有 local low-rank shared structure，继续做 local head removal 是否有帮助。

---

# 一、Todo3 实验报告

## 实验 1：Mean-only control

### 目标
验证“单纯去均值更可分”不是核心结论。

### 假设
如果数据里只有全局均值和语义均值，而没有 shared high-variance head，那么 centered 不应改变基于 scatter 的 separability，也不应系统性提升简单线性 router 的准确率。

### 数学建模
数据生成：

$$
x = \mu + m_z + \varepsilon
$$

其中：
- $\mu$：全局均值；
- $m_z$：第 $z$ 类的语义均值；
- $\varepsilon$：各向同性噪音。

比较：
1. raw $x$
2. centered $x-\mu$

### 指标
1. Fisher separability
2. 线性 router 准确率

### 步骤
1. 生成 4 类 synthetic 数据。
2. 分别在 raw 和 centered 表示上计算 Fisher separability。
3. 用线性分类器预测 $z$，比较准确率。

### 结果（5 个随机种子平均）
| 设置 | Fisher separability | 线性 router 准确率 |
|---|---:|---:|
| raw | 0.1938 | 82.23% |
| centered | 0.1938 | 82.23% |

### 结论
- 去均值本身几乎不改变 separability。
- 所以 Todo3 的关键不是“去均值更可分”，而是“去掉共享高方差 head 更可分”。

---

## 实验 2：Shared-head toy experiment

### 目标
验证真正有用的是去掉 centered covariance 的 shared high-variance head。

### 假设
若 shared head 主要携带组内共享高方差噪音，而语义信号主要在 tail 中，那么去掉 top-$k$ 主方向会提升语义 separability 和简单 router 的可路由性。

### 数学建模
数据生成：

$$
x = \mu + Uh + Vm_z + \varepsilon
$$

其中：
- $\mu$：全局均值；
- $U$：shared head 子空间；
- $h \sim \mathcal N(0,\alpha^2 I)$：head 上的共享高方差噪音；
- $V$：语义 tail 子空间；
- $m_z$：第 $z$ 类的语义原型；
- $\varepsilon$：小噪音。

### 指标
1. Fisher separability
2. 线性 router 准确率

### 对比设置
1. raw  
2. centered  
3. ours：centered + PCA 去掉 top-4 主方向  
4. random：centered + 随机删 4 个坐标  
5. oracle：centered + 去掉真实 head 子空间

### 步骤
1. 生成 4 类数据，head 方差远大于 tail。
2. 在训练集上估计 top-4 PCA 方向。
3. 对 5 种表示分别计算指标。

### 结果（5 个随机种子平均）
| 设置 | Fisher separability | 线性 router 准确率 |
|---|---:|---:|
| raw | 0.0030 | 32.83% |
| centered | 0.0030 | 38.64% |
| ours | 0.0638 | 52.43% |
| random | 0.0033 | 36.36% |
| oracle | 0.0640 | 52.54% |

### 解释
- raw 和 centered 几乎一样，说明“去均值”不是关键。
- ours 与 oracle 很接近，说明 PCA head removal 近似抓到了真正的共享 head。
- random 不稳定且明显差，说明不是“随便删几维都行”。

### 对主线的意义
这直接支持：

> router 不应该在 full representation 上工作，而应该先在 centered tail 上工作。

---

## 实验 3：Signal leakage sweep

### 目标
验证 head removal 不是 tautology，而是一个有条件成立的命题。

### 假设
如果语义信号本身逐渐泄漏进被删掉的 head 子空间，那么 head removal 的收益会下降；泄漏足够大时，head removal 会反而伤害 separability。

### 数学建模
数据生成：

$$
x = \mu + U(h+\rho q_z) + Vm_z + \varepsilon
$$

其中：
- $\rho$：语义信号泄漏到 head 的强度；
- $q_z$：第 $z$ 类在 head 上的语义偏移。

### 指标
1. Fisher separability
2. 线性 router 准确率

### 步骤
1. 固定其余参数，只 sweep $\rho$。
2. 比较 raw 和 ours 两种表示上的指标。

### 结果（3 个随机种子平均，准确率）
| leakage $\rho$ | raw | ours |
|---|---:|---:|
| 0 | 35.78% | 54.89% |
| 2 | 34.97% | 54.64% |
| 4 | 38.31% | 54.01% |
| 8 | 36.89% | 51.87% |
| 16 | 51.98% | 47.02% |
| 24 | 66.24% | 42.98% |

### 结论
- 当 head 主要是共享噪音时，去 head 明显有利。
- 当语义信号大量泄漏到 head 里时，去 head 会开始伤害路由。

这和理论条件完全一致：

$$
\frac{\delta_b}{b} < \frac{\delta_w}{w}
$$

只有在“删掉的噪音比例大于删掉的语义信号比例”时，head removal 才真正有益。

---

# 二、Todo2 实验报告

## 目标
验证：去掉 global head 之后，residual 里若仍有 local low-rank shared structure，那么继续做 local head removal 会提升 finer routing。

## 假设
存在两层潜在模式：
- $Z_1$：粗粒度模式；
- $Z_2$：细粒度模式。

global head 去掉以后，固定某个 coarse group，residual 里仍有 group-specific local nuisance。  
如果把这部分 local nuisance 再去掉，fine label 的 separability 会继续提升。

## 数学建模
数据生成分为 4 部分：

$$
x = \mu + x_{\text{global-head}} + x_{\text{coarse-signal}} + x_{\text{local-head}} + x_{\text{fine-signal}} + \varepsilon
$$

其中：
- global-head：所有样本共享的高方差部分；
- coarse-signal：区分粗粒度组 $Z_1$；
- local-head：在固定 coarse group 内共享，但不帮助区分 finer label；
- fine-signal：真正区分 $Z_2$ 的 deeper tail。

### 两种路由策略
1. **Flat after global tail**：只去掉 global head，然后直接做 fine routing。  
2. **Hierarchical**：先做 coarse routing，再在每个 coarse group 内去掉 local head，再做 finer routing。

## 指标
1. fine-label 准确率
2. coarse-label 准确率
3. global tail 后的 Fisher separability
4. local tail 后的平均 Fisher separability

## 步骤
1. 构造两层 latent synthetic 数据。
2. 先用 PCA 去掉 global top-4 head。
3. 方案 A：直接在 residual 上做 4 类 fine routing。
4. 方案 B：先做 coarse routing；在每个 coarse group 内再估计 local top-2 head 并去掉；最后做 2 类 finer routing。
5. 比较指标。

## 结果（5 个随机种子平均）
| 指标 | Flat after global tail | Hierarchical |
|---|---:|---:|
| coarse accuracy | — | 99.74% |
| fine accuracy | 85.55% | 91.83% |
| Fisher separability | 0.0486 | 0.1420 |

### 解释
- 仅仅做 global head removal，还不足以把 fine mode 完全分开。
- 在 coarse group 内继续去掉 local shared low-rank structure 后，fine separability 和 fine routing 准确率都明显提升。
- 这说明 Todo2 的“继续拆”不是拍脑袋，而是在 residual 的条件分布里仍然存在 local head。

---

# 三、实验结论怎么向外汇报

## Todo3 的一句话
去均值本身不是关键；真正有用的是去掉 centered covariance 的 shared high-variance head。它能让简单 router 更容易按语义模式分流，但只有在被删掉的子空间主要是共享噪音时才成立。

## Todo2 的一句话
global tail 之后，residual 里仍可能有 coarse-group 内部共享的 low-rank structure；继续做 local head removal，可以把 flat routing 变成更稳定的 coarse-to-fine routing。

## 和整体主线的连接
- Todo3 解决的是：**让 router 看见 tail**。  
- Todo2 解决的是：**即使进入 tail，仍要继续识别 local shared structure，逐层把更细的语义 mode 剥出来。**
