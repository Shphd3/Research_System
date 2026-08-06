# 模型架构构建文档：Hierarchical MoE 与 Baseline 消融

## 0. 本文目的

本文定义第一版 synthetic Zipfian hierarchy 实验中的模型架构和消融对象。

核心要求：

1. base model 约 0.6B；
2. backbone 冻结，只训练 layer-8 replacement / adapter block；
3. 第一阶段主模型必须验证真正的 conditional hierarchy：先按 coarse group 路由，再在 group 内继续拆 conditional-common / conditional-tail；
4. 所有模型 trainable parameter count 必须 matched；
5. 必须包含两个关键消融：是否需要 group 内 common/tail 分化，以及不同层级 expert 是否需要接收不同 band input；
6. 必须和普通 flat routing + load-balance loss 比较。

---

## 1. 统一符号

设 frozen model 某层 hidden state 为：

$$
h \in \mathbb{R}^{d}
$$

校准后得到均值：

$$
\mu
$$

和 PCA/SVD directions：

$$
V=[v_1,\dots,v_r]
$$

middle band 定义为：

$$
M=[17,207]
$$

middle-band representation：

$$
x_M = P_M(h-\mu)
$$

其中：

$$
P_M(h-\mu)=V_MV_M^\top(h-\mu)
$$

实际进入 router 前使用 LayerNorm：

$$
\tilde{x}_M=\operatorname{LN}(x_M)
$$

为了验证“middle band 内部仍然存在 conditional-common / conditional-tail 结构”，在 $M$ 内部再定义两个可配置子 band：

$$
M_{\text{cc}} \subset M
$$

$$
M_{\text{tail}} \subset M
$$

对应表示为：

$$
\tilde{x}_{M_{\text{cc}}}
=\operatorname{LN}(P_{M_{\text{cc}}}(h-\mu))
$$

$$
\tilde{x}_{M_{\text{tail}}}
=\operatorname{LN}(P_{M_{\text{tail}}}(h-\mu))
$$

其中：

- $M$ 用于第一层 coarse routing；
- $M_{\text{cc}}$ 用于 group 内 conditional-common / conditional-tail routing；
- $M_{\text{tail}}$ 用于 fine / tail routing 或 conditional-tail expert input。

第一版如果不确定 $M_{\text{cc}}$ / $M_{\text{tail}}$ 的具体边界，可以先按 $M$ 内部方差顺序切分，并在报告中记录实际 index。

---

## 2. 统一输出形式

所有 replacement block 都采用 residual form：

$$
h_{\text{out}} = h + \Delta h
$$

不同模型只改变 $\Delta h$ 的计算方式。

---

## 3. 参数量匹配原则

### 3.1 统一预算

先定义主模型 Hierarchical MoE 的 trainable parameter count：

$$
P_{\text{main}}
$$

所有 baseline 的 trainable parameter count 都必须满足：

$$
\left|
\frac{P_{\text{group}}-P_{\text{main}}}{P_{\text{main}}}
\right|
\leq 1\%
$$

如果不能精确匹配，报告实际参数量和误差。

---

### 3.2 MLP expert 参数估算

每个 expert 使用 bottleneck MLP：

$$
E(x)=W_2\sigma(W_1x)
$$

参数量近似为：

$$
P_E \approx 2dr
$$

其中：

- $d$ 是 hidden size；
- $r$ 是 expert intermediate size。

dense baseline 也使用相同形式，只是调整 $r_{\text{dense}}$ 来匹配总参数量。

### 3.2.1 主模型内部 expert 容量分配

Conditional hierarchy 主模型中有三类 expert：

```text
1 个 global common expert
C 个 conditional-common experts
C × F 个 conditional-tail / fine experts
```

第一版不建议所有 expert 完全等大。容量应按层级功能分配：

```text
global common expert        最大
conditional-common experts  中等
conditional-tail/fine experts 较小
```

推荐 bottleneck 比例：

```text
r_global_common : r_conditional_common : r_fine_tail = 4 : 2 : 1
```

例如：

```text
r_global_common = 256
r_conditional_common = 128
r_fine_tail = 64
```

此时 expert 部分的 effective bottleneck 为：

$$
r_{\text{eff}}
=
r_0
+
C r_{\text{cc}}
+
C F r_{\text{tail}}
$$

代入 $C=4,F=4$：

$$
r_{\text{eff}}
=
256
+
4 \times 128
+
16 \times 64
=1792
$$

expert 参数量近似为：

$$
P_{\text{experts}}
\approx
2d
\left(
r_0
+
C r_{\text{cc}}
+
C F r_{\text{tail}}
\right)
$$

这样做的理由：

1. global common expert 覆盖最多 token，需要最大容量；
2. conditional-common expert 覆盖某个 coarse group 内的共享结构，需要中等容量；
3. fine/tail expert 数量最多，每个 expert 负责较窄细粒度信号，所以单个容量较小；
4. fine/tail expert 不能按 token 频率严格缩得过小，否则容易把 underfit 误判成 hierarchy 失败。

因此第一版不要按 $\rho_{\text{common}},\rho_{\text{coarse}},\rho_{\text{fine}}$ 严格分配容量。$\rho$ 控制数据中 token source 的出现频率，不应直接决定 expert 参数量。

所有 baseline 通过调整 bottleneck size 来匹配主模型总 trainable parameter count，而不是匹配某一类 expert 的容量。

---

### 3.3 Router 参数也要计入

router 参数包括：

- coarse router；
- group 内 conditional common/tail router；
- fine router；
- optional routing projection；
- load-balance 不增加参数，但影响 objective。

主模型参数量约为：

$$
P_{\text{hier}}
=P_{\text{common}}
+
C \cdot P_{\text{conditional-common}}
+
C \cdot F \cdot P_{\text{expert}}
+
P_{\text{coarse-router}}
+
P_{\text{source-router}}
+
P_{\text{fine-router}}
$$

其中：

- $C$ 是 coarse expert 数；
- $F$ 是每个 coarse 下的 fine expert 数；
- $C \times F$ 是 leaf experts 总数。
- 每个 coarse group 额外有 1 个 conditional-common expert。

第一版推荐：

```yaml
num_coarse: 4
num_fine_per_coarse: 4
num_leaf_experts: 16
num_conditional_common_experts: 4
```

---

## 4. 第一阶段主模型：Conditional Common/Tail Hierarchical MoE

### 4.1 结构

数据生成中的三类来源对应模型结构：

```text
global common tokens  -> global common expert
coarse-source tokens  -> conditional-common expert inside coarse group
fine-source tokens    -> conditional-tail / fine expert inside coarse group
```

第一层 coarse router 使用 middle band：

$$
g_c = \operatorname{softmax}(W_c \tilde{x}_M)
$$

其中：

$$
g_c \in \mathbb{R}^{C}
$$

对于每个 coarse group，先计算 group 内 source router：

$$
g_{s|c}
=\operatorname{softmax}(W_{s,c}\tilde{x}_{M_{\text{cc}}})
$$

其中：

$$
s \in \{\text{conditional-common}, \text{conditional-tail}\}
$$

对于 conditional-tail 分支，再计算 fine router：

$$
g_{f|c}
=\operatorname{softmax}(W_{f,c}\tilde{x}_{M_{\text{tail}}})
$$

因此 route probability 为：

$$
\pi_{c,\text{cc}}
=g_c(c)g_{s|c}(\text{conditional-common})
$$

$$
\pi_{c,f}
=g_c(c)g_{s|c}(\text{conditional-tail})g_{f|c}(f)
$$

输出为：

$$
\Delta h
=E_0(z_0)
+
\sum_{c=1}^{C}
\pi_{c,\text{cc}}E_{c,\text{cc}}(z_{\text{cc}})
+
\sum_{c=1}^{C}
\sum_{f=1}^{F}
\pi_{c,f}E_{c,f}(z_{\text{tail}})
$$

其中：

- $E_0$ 是 global common expert；
- $E_{c,\text{cc}}$ 是 coarse group 内 conditional-common expert；
- $E_{c,f}$ 是 coarse group 内 conditional-tail / fine expert；
- $z_0,z_{\text{cc}},z_{\text{tail}}$ 是不同层级 expert 的输入。

第一版主设置：

$$
z_0=z_{\text{cc}}=z_{\text{tail}}=h
$$

理由：

> 先验证 conditional hierarchy routing 是否有效，不把 expert input 分层作为唯一解释。

### 4.2 Level-specific expert input 消融

为了验证“不只是 router 分层，expert 接收的输入也应分层”，增加 level-specific input 版本：

$$
z_0=P_{1:16}(h-\mu)
$$

$$
z_{\text{cc}}=P_{M_{\text{cc}}}(h-\mu)
$$

$$
z_{\text{tail}}=P_{M_{\text{tail}}}(h-\mu)
$$

如果该版本强于 raw expert input，说明不同层级 expert 需要看到不同 representation band。

---

### 4.3 为什么第一版用 soft hierarchy

hard hierarchy 是：

$$
\hat c=\arg\max g_c
$$

$$
\hat s=\arg\max g_{s|\hat c}
$$

如果：

$$
\hat s=\text{conditional-tail}
$$

再计算：

$$
\hat f=\arg\max g_{f|\hat c}
$$

问题是 coarse router 一旦错，fine router 全错。

第一版训练使用 soft hierarchy，评估时可以同时报告 hard top-1 route。

---

## 5. Main model variants

### H-CondCT-Soft

第一阶段主模型：

```text
coarse router input = middle band
group source router input = middle-inside-middle band
fine/tail router input = tail-inside-middle band
expert input = raw hidden
routing = conditional common/tail soft hierarchy
LB = no
```

---

### H-CondCT-Soft-LB

同主模型，但加入 hierarchical LB：

$$
L=L_{\text{LM}}+\lambda_{\text{LB}}L_{\text{LB}}
$$

需要分别报告：

1. coarse expert usage；
2. conditional common/tail usage；
3. fine / leaf expert usage。

---

### H-CondCT-LevelInput

消融 expert input 是否也需要分层：

```text
global common expert input = high/common band
conditional-common expert input = middle-inside-middle band
conditional-tail expert input = tail-inside-middle band
```

目的：

> 检查收益来自 conditional routing，还是 expert 也必须接收不同层级的 projected input。

---

### H-Mid-Soft

旧版浅层 hierarchy baseline：

```text
coarse router input = middle band
fine router input = middle band
expert input = raw hidden
no conditional common/tail split
```

目的：

> 检查 group 内 common/tail 分化是否真的必要。

---

### H-Rand-CondCT

随机谱空间对照。

构造与 middle band 同维度的 random orthonormal subspace：

$$
x_R=P_R(h-\mu)
$$

router 输入：

$$
\tilde{x}_R=\operatorname{LN}(x_R)
$$

其余结构不变。

目的：

> 排除“只要投影一下就行”的解释。

---

### H-Oracle-CondCT

oracle hierarchical router。

直接用 synthetic dataset 的真实 labels 和 token source：

$$
c_{\text{true}}, f_{\text{true}}
$$

```text
token_source = common -> global common expert
token_source = coarse -> E_{c,true,cc}
token_source = fine -> E_{c,true,f,true}
```

目的：

> 上界。如果 oracle 都不强，说明数据任务或 expert 结构不需要 hierarchy。

---

## 6. Baseline 设计

### G0: Matched Dense

单个 dense adapter / replacement block：

$$
\Delta h = F_{\text{dense}}(h)
$$

调整 intermediate size，使参数量匹配 $P_{\text{main}}$。

目的：

> 排除“只是参数更多”。

---

### G1: Flat MoE Raw + LB

普通 MoE baseline。

router 和 experts 都看 raw hidden：

$$
g=\operatorname{softmax}(W_g h)
$$

$$
\Delta h
=\sum_{e=1}^{K}
g_e(h)E_e(h)
$$

其中：

$$
K=C\times F
$$

加入 load-balance loss。

目的：

> 和普通 MoE + LB loss 比较。

---

### G2: Flat MoE Middle + LB

flat MoE，但 router 看 middle band：

$$
g=\operatorname{softmax}(W_g \tilde{x}_M)
$$

experts 仍看 raw hidden：

$$
\Delta h
=\sum_{e=1}^{K}
g_e(\tilde{x}_M)E_e(h)
$$

目的：

> 区分“middle-band routing 有用”与“hierarchy 有用”。

如果 G2 接近 H-CondCT-Soft，说明 flat middle router 已经够了，conditional hierarchy 不是必要。

---

### G3: Uniform Expert Mixture

有 $K$ 个 experts，但没有 learned routing：

$$
\Delta h
=\frac{1}{K}
\sum_{e=1}^{K}
E_e(h)
$$

目的：

> 排除只是多 expert capacity。

---

### G4: Random Flat MoE + LB

flat MoE router 使用 random subspace：

$$
g=\operatorname{softmax}(W_g \tilde{x}_R)
$$

目的：

> 排除 middle band 特异性。

---

### G5: Hard Conditional Hierarchical MoE

训练或评估 hard top-1 hierarchical route：

$$
\hat c=\arg\max g_c
$$

$$
\hat s=\arg\max g_{s|\hat c}
$$

如果 $\hat s=\text{conditional-tail}$，再取：

$$
\hat f=\arg\max g_{f|\hat c}
$$

$$
\Delta h
=
E_0(h)
+
\mathbf{1}[\hat s=\text{conditional-common}]E_{\hat c,\text{cc}}(h)
+
\mathbf{1}[\hat s=\text{conditional-tail}]E_{\hat c,\hat f}(h)
$$

目的：

> 测试 hard conditional hierarchy 是否发生 coarse routing 或 source routing cascade。

第一版建议只作为 evaluation / ablation，不作为主训练版本。

---

## 7. 消融对象

第一版消融必须围绕以下问题：

### Ablation 1: group 内 common/tail 分化是否必要

比较：

```text
H-CondCT-Soft
vs
H-Mid-Soft
```

如果 H-CondCT-Soft 明显强于 H-Mid-Soft，说明 coarse group 内 conditional-common / conditional-tail 分化是必要的。

---

### Ablation 2: hierarchy 是否必要

比较：

```text
H-CondCT-Soft
vs
Flat MoE Middle + LB
```

如果 flat middle 接近 H-CondCT-Soft，说明层级结构本身没有明显必要。

---

### Ablation 3: middle band 是否必要

比较：

```text
H-CondCT-Soft
vs
H-Rand-CondCT
vs
Flat MoE Raw + LB
```

如果 random 或 raw 接近 middle，说明 middle-band routing 不是关键。

---

### Ablation 4: LB 是否必要

比较：

```text
H-CondCT-Soft
vs
H-CondCT-Soft-LB
Flat MoE Raw no-LB
vs
Flat MoE Raw + LB
```

如果 LB 只提高 usage balance 但不提高 NTP / expert advantage，不能认为 LB 支持 hierarchy。

---

### Ablation 5: level-specific expert input 是否必要

比较：

```text
H-CondCT-Soft, expert input = raw hidden
H-CondCT-LevelInput, expert input = level-specific bands
```

如果 H-CondCT-LevelInput 更好，说明不仅 router，expert 也需要层级对应的 representation band。

如果 H-CondCT-Soft 更好，说明 projected expert input 可能 underfit，或者当前 band 定义不对。

---

### Ablation 6: hard hierarchy 是否级联失败

比较：

```text
soft hierarchy
hard hierarchy
oracle coarse + learned fine
learned coarse + oracle fine
oracle full hierarchy
```

如果 oracle coarse + learned fine 明显好于 learned hard hierarchy，说明 coarse router 是瓶颈。

---

## 8. 第一版模型矩阵

| ID | Model | Router input | Expert input | Routing | LB | Purpose |
|---|---|---|---|---|---|---|
| G0 | Matched Dense | none | raw | none | no | 参数量基线 |
| G1 | Flat MoE Raw + LB | raw | raw | flat soft | yes | 普通 MoE + LB |
| G2 | Flat MoE Middle + LB | middle band | raw | flat soft | yes | 检查 middle routing 是否够用 |
| G3 | H-Mid-Soft | middle band | raw | coarse/fine soft | no | 浅层 hierarchy 基线 |
| G4 | H-CondCT-Soft | middle + nested middle/tail | raw | conditional hierarchy soft | no | 第一阶段主模型 |
| G5 | H-CondCT-Soft-LB | middle + nested middle/tail | raw | conditional hierarchy soft | yes | LB 消融 |
| G6 | H-CondCT-LevelInput | middle + nested middle/tail | level-specific bands | conditional hierarchy soft | no | expert input 消融 |
| G7 | H-Rand-CondCT | random subspace | raw | conditional hierarchy soft | no | 随机谱空间对照 |
| G8 | H-Oracle-CondCT | true labels/source | raw | oracle conditional hierarchy | no | 上界 |
| G9 | Uniform Expert Mixture | none | raw | uniform | no | 多 expert 容量对照 |
| G10 | Hard-H-CondCT | middle + nested middle/tail | raw | conditional hierarchy hard | optional | cascade 诊断 |

---

## 9. 必须报告的指标

### Main NTP metrics

```text
test NLL
common-token NLL
coarse-token NLL
fine-token NLL
middle-frequency-token NLL
rare-token NLL
```

---

### Router recovery

```text
coarse router accuracy
conditional common/tail router accuracy
fine router accuracy
leaf expert accuracy
NMI(route, true coarse)
NMI(source route, true token_source)
NMI(route, true fine)
```

---

### Expert advantage

$$
A(t)
=\ell_{\text{second-best}}(t)
-\ell_{\text{selected}}(t)
$$

按以下分桶报告：

```text
common tokens
coarse-specific tokens
fine-specific tokens
rare tokens
```

---

### Oracle regret

$$
\operatorname{Regret}(t)
=\ell_{\text{selected}}(t)
-\min_e \ell_e(t)
$$

---

### Load balance diagnostics

```text
expert usage entropy
coarse usage entropy
fine usage entropy
leaf expert usage distribution
```

注意：

> usage balance 不是成功标准，只是诊断指标。

---

## 10. 通过标准

主模型 H-CondCT-Soft 通过的最低标准：

1. test NLL 优于 matched dense 或接近 oracle；
2. coarse router accuracy 明显高于随机；
3. conditional common/tail router accuracy 明显高于随机；
4. fine router accuracy 明显高于随机；
5. selected expert advantage 为正；
6. H-CondCT-Soft 优于 H-Mid-Soft；
7. H-CondCT-Soft 优于 H-Rand-CondCT；
8. H-CondCT-Soft 优于 Flat MoE Raw + LB；
9. H-CondCT-Soft 至少不弱于 Flat MoE Middle + LB。

如果只满足 1，不满足 2-4，说明只是性能提升，不是 hierarchy 学出来。

如果只满足 router recovery，不满足 expert advantage，说明 route 看起来对，但 expert 没有功能专一性。

---

## 11. 最重要的解释规则

### Case 1: Oracle strong, learned weak

说明：

> hierarchy 有潜力，但 learned router 不行。

下一步修 router。

---

### Case 2: Flat middle matches hierarchical middle

说明：

> middle-band routing 有用，但 hierarchy 不是必要结构。

下一步不该直接加层级，而应先研究 flat router。

---

### Case 3: Random matches middle

说明：

> middle band 不是关键，当前谱空间假设不成立。

---

### Case 4: LB improves balance but not NLL

说明：

> LB 只是让 usage 更均匀，不代表专家更有用。

---

### Case 5: Hard hierarchy worse than soft

说明：

> coarse route cascade 是问题。

下一步保留 soft hierarchy 或引入 teacher-aided coarse router。

---

## 12. 第一版推荐实现顺序

1. 实现 matched dense；
2. 实现 flat MoE raw + LB；
3. 实现 flat MoE middle + LB；
4. 实现 H-Mid-Soft 浅层 hierarchy 基线；
5. 实现 H-CondCT-Soft 主模型；
6. 实现 H-Oracle-CondCT；
7. 再补 H-Rand-CondCT；
8. 最后补 LB / hard / level-specific expert-input 消融。

不要第一天同时实现所有组。
