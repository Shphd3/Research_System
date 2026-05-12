# 4. `1sketch`：Weight Decay 对长尾信息的影响

下面我按你要的顺序来：**物理建模 → 假设构建 → 数学建模 → 实验设计**。

---

## 4.1 先把命题写准确

不要写成：

> “weight decay 的信号淹没了长尾信号。”

建议改写为：

> **在一个各向异性的表示空间中，数据驱动力沿第 $i$ 个方向的强度与该方向的有效信号强度成正比，而统一 weight decay 提供各向同性收缩。因此当 $p_e\lambda_i \ll \gamma_e$ 时，该方向的参数无法建立稳定幅值，tail 模态会被系统性压制。**

这里：

- $\lambda_i$：该方向上的特征能量 / 协方差特征值
- $p_e$：expert $e$ 的路由占用率
- $\gamma_e$：该 expert 的 weight decay 强度

---

## 4.2 物理建模

把每个特征方向看成一个独立模态。

- **数据项**像驱动力，强度和该模态的可观测能量成正比；
- **weight decay**像各向同性摩擦；
- **head 模态**能量大，驱动力强，容易活下来；
- **tail 模态**能量小，驱动力弱，更容易被摩擦压住；
- **稀有 expert**因为只在少数 token 上被更新，相当于驱动力出现频率也更低。

所以真正的控制量不是单独的 $\lambda_i$，也不是单独的 $p_e$，而是：

$$
p_e \lambda_i
$$

这就是某个 expert 在某个方向上的**有效信号强度**。

---

## 4.3 假设构建

### H1：谱生存律
在固定 feature 的最小模型中，expert $e$ 在第 $i$ 个方向上的信号保留率满足：

$$
s_{e,i}=\frac{p_e\lambda_i}{p_e\lambda_i+\gamma_e}
$$

### H2：存在明确的死亡边界
定义临界特征值：

$$
\lambda_c^{(e)}=\frac{\gamma_e}{p_e}
$$

则当 $\lambda_i \ll \lambda_c^{(e)}$ 时，该方向基本死亡。

### H3：静态统一 WD 会系统性伤害 rare expert 和 tail modes
因为 rare expert 的 $p_e$ 更小，所以它们的临界值更高，更容易大面积丢失谱尾。

### H4：动态 WD 或 common/tail 解耦 WD 能救回来
若取：

$$
\gamma_e=\rho p_e
$$

则：

$$
\lambda_c^{(e)}=\rho
$$

occupancy 带来的额外惩罚被抵消。  
若再对 tail branch 使用更小基准 decay，则 tail 的生存条件进一步改善。

---

## 4.4 数学建模

### 4.4.1 最小 teacher-student 模型

考虑 expert $e$ 的输入表征 $x \in \mathbb R^d$，条件协方差为：

$$
\Sigma_e = U \Lambda U^\top,\qquad \Lambda=\operatorname{diag}(\lambda_1,\dots,\lambda_d)
$$

teacher 为线性函数：

$$
y=\beta^\top x+\epsilon
$$

我们把全局目标写成：

$$
\mathcal L_e(w_e)
=\frac{1}{2}\mathbb E\big[\mathbf 1(r(x)=e)(y-w_e^\top x)^2\big]
+
\frac{\gamma_e}{2}\|w_e\|^2
$$

如果 $P(r(x)=e)=p_e$，则：

$$
\mathcal L_e(w_e)
=\frac{p_e}{2}\mathbb E\big[(y-w_e^\top x)^2\mid r=e\big]
+
\frac{\gamma_e}{2}\|w_e\|^2
$$

最优解满足：

$$
w_e^*=(p_e\Sigma_e+\gamma_e I)^{-1}p_e\Sigma_e\beta
$$

投到特征向量基上，记 $a_{e,i}=u_i^\top w_e$、$\beta_i=u_i^\top \beta$，则：

$$
a_{e,i}^*
=\frac{p_e\lambda_i}{p_e\lambda_i+\gamma_e}\beta_i
$$

这就是闭式谱生存律。

---

### 4.4.2 动力学版本：为什么叫 gradient starvation

若用梯度流近似，单个方向上的演化为：

$$
\dot a_{e,i}(t)=-(p_e\lambda_i+\gamma_e)a_{e,i}(t)
+
p_e\lambda_i\beta_i
$$

解为：

$$a_{e,i}(t)=
\frac{p_e\lambda_i}{p_e\lambda_i+\gamma_e}
\big(1-e^{-(p_e\lambda_i+\gamma_e)t}\big)\beta_i
$$

这条式子告诉你两件事：

1. **tail 起得慢**：因为驱动力 $p_e\lambda_i\beta_i$ 小；  
2. **tail 长不高**：因为最终幅值上限就是那个 shrinkage factor。

所以“gradient starvation”不是一句比喻，而是一个有动力学含义的事实。

---

### 4.4.3 Tail Survival Rate 的定义

建议直接定义：

$$ S_T = \frac{\sum_{i\in T} a_{e,i}^{*2}}
{\sum_{i\in T}\beta_i^2}
\quad\text{或}\quad
\widetilde S_T=\frac{\sum_{i\in T} a_{e,i}^{*2}\lambda_i}
{\sum_{i\in T}\beta_i^2\lambda_i}
$$

其中：

- $S_T$：参数层面的 tail coefficient survival
- $\widetilde S_T$：功能层面的 tail signal survival

后者更好，因为它对应的是该方向对输出的有效贡献。

---

### 4.4.4 为什么这直接支持 Hierarchical / Dynamic WD

在 Flat MoE 里，head 和 tail 共用一个 $\gamma$。  
如果为了控制 head 而把 $\gamma$ 设大，那么 tail 的生存因子就变成：

$$
s_{tail}
=\frac{p_e\lambda_{tail}}{p_e\lambda_{tail}+\gamma}
\ll 1
$$

而在 Hierarchical / Compositional 架构里可以写成：

$$
h_{out}=E_{common}(x)+\sum_j g_j(x)\,E_{tail,j}(P_{tail}x)
$$

总 loss 写成：

$$
\mathcal L
=\mathcal L_{task}
+
\frac{\gamma_c}{2}\|\theta_{common}\|^2
+
\sum_j \frac{\gamma_j}{2}\|\theta_{tail,j}\|^2
$$

其中可以取：

$$
\gamma_c \gg \gamma_j
\quad\text{或}\quad
\gamma_j=\rho p_j
$$

这就把“为什么要 common/tail 解耦”从经验直觉变成了优化定律。

---

## 4.5 实验设计

这里我建议你做成 **一个主实验 + 两个消融**，而且**第一版不要用可学习 router**。  
因为你现在要钉死的是 weight decay 的机制，不是 routing 机制。  
router 一进来，因果就混了。

---

### 主实验：Flat vs Hierarchical under Weight Decay

#### 数据构造
设：

- head 维度 $d_h=4$
- tail 维度 $d_t=4$

协方差谱取：

$$
\lambda_H=[100,50,20,10]
$$

$$
\lambda_T=[1,0.5,0.2,0.1]
$$

令输入为高斯：

$$
x_i \sim \mathcal N(0,\lambda_i)
$$

teacher 系数取：

$$
\beta_i=\frac{1}{\sqrt{\lambda_i}}
$$

这个选择很关键，因为它使得每个方向对标签的理论贡献近似相同。  
这样一来，tail 若死掉，就不能再解释成“它本来就没那么重要”。

令标签为：

$$
y=\beta^\top x+\epsilon,\qquad \epsilon\sim\mathcal N(0,\sigma^2)
$$

#### 模型对比
1. **Flat**：所有方向共用同一个 decay $\gamma$  
2. **Hierarchical**：head 方向用 $\gamma_h$，tail 方向用更小的 $\gamma_t$

#### sweep
- Flat: $\gamma \in \{0.1,1,10\}$
- Hierarchical: 固定 $\gamma_h=10,\ \gamma_t=0.1$

#### 指标
- Head coefficient survival
- Tail coefficient survival
- Head signal survival
- Tail signal survival
- test MSE
- tail-only MSE

#### 判别标准
若主线正确，应看到：

- Flat 随 $\gamma$ 增大时，tail survival 先塌；
- head 还活着时，tail 已经接近死亡；
- Hierarchical 在几乎不损 head 的情况下，大幅恢复 tail survival。

---

### 消融 1：occupancy effect

这是专门为了体现 rare expert 的。

#### 设定
做两个 expert：

- frequent expert: $p_e=0.5$
- rare expert: $p_e=0.05$

它们看到同样的 tail covariance、同样的 teacher。  
比较：

1. 静态 WD：$\gamma_e=0.1$
2. 动态 WD：$\gamma_e=0.2p_e$

#### 指标
- 每个 expert 的 tail coefficient survival

#### 判别标准
若理论正确：

- 静态 WD 下 rare expert 明显更差；
- 动态 WD 下两者 survival 被拉齐。

---

### 消融 2：动力学曲线

用 SGD 或直接画理论曲线，比较 head 和 tail 的：

$$
\frac{a_i(t)}{\beta_i}
=\frac{p_e\lambda_i}{p_e\lambda_i+\gamma_e}
\big(1-e^{-(p_e\lambda_i+\gamma_e)t}\big)
$$

如果你想把“gradient starvation”这个词讲得更硬，这个图非常有用。  
因为它展示的不是最后结果，而是学习过程本身：

- head 学得快、幅值高；
- tail 学得慢、幅值低；
- rare expert 更严重。

---

## 4.6 我补跑的最小 synthetic 结果

下面这些是最小线性 toy simulation 的结果，目的是验证上面的闭式规律是否干净成立。  
它不是 LLM 证据，但足以作为 `1sketch` 的封闭验证。

---

### 结果 1：静态 WD 会优先压死 tail

设谱为：

- head: $[100,50,20,10]$
- tail: $[1,0.5,0.2,0.1]$

teacher 取 $\beta_i=1/\sqrt{\lambda_i}$。

| Weight Decay $\gamma$ | Head 平均系数生存 | Tail 平均系数生存 | Head 信号生存 | Tail 信号生存 |
|---|---:|---:|---:|---:|
| 0.1 | 99.6% | 72.7% | 99.1% | 55.38% |
| 1.0 | 95.8% | 27.3% | 91.9% | 9.93% |
| 10.0 | 72.7% | 4.2% | 55.4% | 0.28% |

这个表非常强。  
因为它说明即使所有方向对 teacher 的理论贡献被设计成“同等重要”，统一 WD 仍然会先杀 tail。

---

### 结果 2：rare expert 在静态 WD 下天然更惨

固定 tail 特征值为 $\lambda=1$。

| Expert 占用率 $p_e$ | 静态 WD $\gamma_e=0.1$ 下的 tail 生存 |
|---|---:|
| 0.50 | 83.3% |
| 0.05 | 33.3% |

这正好符合：

$$
s_{e,i}=\frac{p_e\lambda_i}{p_e\lambda_i+\gamma_e}
$$

---

### 结果 3：动态 WD 可以把 rare expert 拉齐

若改成：

$$
\gamma_e=0.2p_e
$$

则：

| Expert 占用率 $p_e$ | 动态 WD $\gamma_e=0.2p_e$ 下的 tail 生存 |
|---|---:|
| 0.50 | 83.3% |
| 0.05 | 83.3% |

这说明 occupancy-scaled decay 不是拍脑袋，而是直接来自 survival law。

---

### 结果 4：Flat vs Hierarchical 的最小对比

我又跑了一个最小对比：

- Flat：$\gamma_{head}=\gamma_{tail}=10$
- Hierarchical：$\gamma_{head}=10,\ \gamma_{tail}=0.1$

结果：

| 模型 | Head 系数生存 | Tail 系数生存 | Head 信号生存 | Tail 信号生存 |
|---|---:|---:|---:|---:|
| Flat | 90.7% | 9.1% | 82.3% | 0.83% |
| Hierarchical | 90.9% | 90.9% | 82.6% | 82.6% |

这个结果几乎就是你们 architecture claim 的最小版证明：

> 在不牺牲 head 的情况下，仅仅通过正则化解耦，就可以把 tail 从几乎死亡拉回到几乎完整存活。

---

## 4.7 这部分现在可以安全 claim 到什么程度

### 现在可以安全 claim 的
1. 在最小线性 / 固定特征模型下，统一 WD 对 tail 的压制有闭式公式。  
2. 这个压制由 $p_e\lambda_i/\gamma_e$ 控制。  
3. rare expert 和 low-variance tail modes 会优先死亡。  
4. 动态 WD 和 common/tail decoupled WD 都有明确的理论救援机制。

### 现在还不要过早 claim 的
1. 不要直接说“所有真实 LLM 层都严格 obey 这条闭式律”。  
2. 不要说“LB 完全无用”。更准确是：**LB 不能替代 subspace decoupling 和 regularization decoupling。**  
3. 不要说“去掉 head 后 tail 一定线性可分”。这需要 ToDo 3 里的 separability 定义。

---

# 本轮结论 / Update

这轮最值得写回 checkpoint 的，我建议就是三句话：

1. **主线被进一步压实为两步失败机制：**  
   Flat MoE 先因 shared head 导致 routing blindness，再因统一 WD 导致 tail starvation。

2. **`1sketch` 的核心公式已经明确：**  
   对 expert $e$ 的第 $i$ 个模态，存活率为  
   $$
   s_{e,i}=\frac{p_e\lambda_i}{p_e\lambda_i+\gamma_e}
   $$
   临界边界为  
   $$
   \lambda_c^{(e)}=\frac{\gamma_e}{p_e}
   $$
