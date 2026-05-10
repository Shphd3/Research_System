# Model Design: Flat / Hierarchical Routing for One MoE Layer + One Attention Layer

本文档描述当前实验实际使用的模型架构，而不只停留在 routing 概念层面。当前主线是 **attention-as-search / hierarchical KV indexing**：把历史 KV cache 组织成可检索的 bucket，query 到来时先召回候选 KV，再在候选集合内做 exact attention。

当前实验使用同一个 block：**一层 causal self-attention + 一层 MoE transformation**。要比较的是 full attention、flat 16 leaf routing，以及在同样 16 个 leaf experts / buckets 上增加层级结构的 hierarchical routing。

需要明确的约束：

- flat expert/router 是 **16 个 leaf experts / 16 个 index buckets**；
- hierarchical expert/router 是在 flat 16 leaf experts 的基础上增加 coarse/fine 两级结构，不是改成 100 个 experts；
- hierarchical 默认可取 $C=4,F=4,M=C F=16$，也可以使用任意满足 $C F=16$ 的 factorization；
- leaf expert id 和 leaf bucket id 始终写成 $m\in\{0,\ldots,15\}$。

本文区分以下五类设置：

1. **Full attention baseline**；
2. **Flat MoE routing / indexing with 16 experts**；
3. **Hierarchical MoE routing / indexing variant A**：双层级分发，但 coarse / fine 都用同样表征；
4. **Hierarchical MoE routing / indexing variant B**：我们设计的谱段 / 分层表征 routing；
5. **Optional oracle routing / oracle_topm controls**。

---

## 0. 统一架构和记号

设输入 token 表征为：

$$h_t^{(0)}\in\mathbb{R}^{d}$$

attention 使用 pre-norm：

$$x_t=\operatorname{LN}(h_t^{(0)})$$

并计算：

$$q_t=x_t W_Q,\qquad k_t=x_t W_K,\qquad v_t=x_t W_V$$

每个 attention head 维度为 $d_h$，head 数为 $H_a$，总维度满足 $d=H_a d_h$。

给定候选历史位置集合 $S_t\subseteq\{1,\ldots,t\}$，attention 必须使用原始 query / key / value 做精确计算：

$$\alpha_{t i}
=
\frac{\exp(q_t^\top k_i/\sqrt{d_h})}
{\sum_{j\in S_t}\exp(q_t^\top k_j/\sqrt{d_h})},
\qquad i\in S_t$$

$$a_t=\sum_{i\in S_t}\alpha_{t i}v_i$$

$$u_t=h_t^{(0)}+a_t W_O$$

MoE 输入为：

$$r_t=\operatorname{LN}(u_t)$$

每个 leaf expert 是一个 token-wise MLP：

$$E_m(r)=W_{2,m}\sigma(W_{1,m}r+b_{1,m})+b_{2,m}$$

其中：

$$m\in\{0,\ldots,M-1\},\qquad M=16$$

top-1 MoE 输出为：

$$h_t^{(1)}=u_t+E_{m_t}(r_t)$$

top-$K_e$ MoE 输出为：

$$h_t^{(1)}
=
u_t+\sum_{m\in T_t}\pi_{t,m}E_m(r_t)$$

其中 $T_t$ 是 router 选出的 expert 集合，$\pi_{t,m}$ 是归一化 gate weight。

KV indexing 与 MoE expert 共享 leaf id 记号，但 router 输入可以不同：

- MoE routing 输入通常是 $r_t$；
- key 建桶输入通常是 $k_i$ 或产生 key 的 hidden state；
- query 查桶输入通常是 $q_t$ 或产生 query 的 hidden state。

下文统一把 router 输入写成：

$$z\in\mathbb{R}^{d_r}$$

实际使用时可取：

$$z=z_t^{\text{moe}}=r_t$$

或：

$$z=z_i^{\text{key}}=k_i,\qquad z=z_t^{\text{query}}=q_t$$

index bucket 定义为：

$$\mathcal I_{\ell,a,m}
=
\{i:\operatorname{route}_{\text{key}}(z_i^{\text{key}})=m\}$$

其中 $\ell$ 是 layer，$a$ 是 attention head 或 KV head，$m$ 是 leaf bucket id。

query 来时先路由：

$$m_q=\operatorname{route}_{\text{query}}(z_t^{\text{query}})$$

再取候选集合：

$$S_t=\mathcal I_{\ell,a,m_q}$$

最后在 $S_t$ 上做 exact attention。routing / indexing 只负责候选召回，不能替代 attention logit。

---

## 1. Full Attention Baseline

Full attention baseline 不使用 router，也不使用 index bucket。它用于给 sparse routing / indexing 提供准确率、loss 和速度参照。

### 1.1 输入

输入为：

$$h_t^{(0)}\rightarrow x_t=\operatorname{LN}(h_t^{(0)})$$

并计算：

$$q_t=x_t W_Q,\qquad k_t=x_t W_K,\qquad v_t=x_t W_V$$

### 1.2 Router 公式

无 router：

$$\operatorname{route}(z)=\varnothing$$

### 1.3 Expert / Index Bucket 公式

无 sparse expert 选择，无分桶。等价地，所有历史 token 都在同一个全局 bucket：

$$\mathcal I_{\ell,a,\text{all}}=\{1,\ldots,t\}$$

### 1.4 Attention 计算方式

候选集合为完整 causal history：

$$S_t^{\text{full}}=\{1,\ldots,t\}$$

attention 为：

$$\operatorname{Attn}_{\text{full}}(q_t,K,V)
=
\sum_{i=1}^{t}
\operatorname{softmax}_i(q_t^\top k_i/\sqrt{d_h})v_i$$

### 1.5 参数规模

attention projection 参数：

$$P_{\text{attn}}=4d^2$$

若计入 bias：

$$P_{\text{attn+bias}}=4d^2+4d$$

baseline 没有 router 参数：

$$P_{\text{router}}=0$$

如果 baseline 不接 MoE：

$$P_{\text{expert}}=0$$

如果为了控制变量而接一个公共 dense MLP，设 hidden width 为 $d_e$，则：

$$P_{\text{dense}}=2dd_e+d_e+d$$

这个公共 dense MLP 不属于 flat / hierarchical routing 的差异项。

---

## 2. Flat MoE Routing / Indexing with 16 Experts

Flat 版本是当前实验的主要对照组。它只有一层 router，直接从输入表征 $z$ 选择 16 个 leaf experts / buckets 之一。

### 2.1 输入

flat router 使用单一表征：

$$z\in\mathbb{R}^{d_r}$$

对于 MoE：

$$z=r_t$$

对于 KV indexing：

$$z=k_i\quad\text{或}\quad z=q_t$$

### 2.2 Router 公式

router logits：

$$g(z)=W_R z+b_R,\qquad W_R\in\mathbb{R}^{16\times d_r}$$

概率：

$$p(m\mid z)=\operatorname{softmax}(g(z))_m$$

top-1 leaf：

$$m^*=\arg\max_{m\in\{0,\ldots,15\}}p(m\mid z)$$

top-$K_e$ expert routing：

$$T(z)=\operatorname{TopK}_{K_e}(p(m\mid z))$$

### 2.3 Expert / Index Bucket 公式

MoE expert 输出：

$$\operatorname{MoE}_{\text{flat}}(r_t)
=
\sum_{m\in T(r_t)}\pi_{t,m}E_m(r_t)$$

top-1 时：

$$\operatorname{MoE}_{\text{flat}}(r_t)=E_{m_t}(r_t)$$

index bucket：

$$\mathcal I_{\ell,a,m}
=
\{i:\operatorname{route}_{\text{key}}(k_i)=m\},
\qquad m\in\{0,\ldots,15\}$$

query 候选集合：

$$S_t^{\text{flat}}
=
\mathcal I_{\ell,a,\operatorname{route}_{\text{query}}(q_t)}$$

如果 query 使用 top-$B$ buckets：

$$S_t^{\text{flat-topB}}
=
\bigcup_{m\in \operatorname{TopB}(p(m\mid q_t))}
\mathcal I_{\ell,a,m}$$

### 2.4 Attention 计算方式

flat indexing 只改变 $S_t$，attention logit 不变：

$$\operatorname{Attn}_{\text{flat}}(q_t,K,V)
=
\sum_{i\in S_t^{\text{flat}}}
\operatorname{softmax}_{i\in S_t^{\text{flat}}}
(q_t^\top k_i/\sqrt{d_h})v_i$$

### 2.5 参数规模

flat router 参数：

$$P_{\text{router-flat}}=16d_r+16$$

单个 expert 参数：

$$P_E=2dd_e+d_e+d$$

16 个 leaf experts：

$$P_{\text{experts-flat}}=16P_E$$

总的 routing / expert 差异项：

$$P_{\text{flat-extra}}=(16d_r+16)+16P_E$$

index bucket 本身不引入 trainable 参数，只引入运行时存储：

$$O(T)\ \text{bucket ids}$$

或按 layer / head 记为：

$$O(LH_aT)\ \text{bucket ids}$$

---

## 3. Hierarchical Variant A: 同表征双层级分发

Variant A 是最直接的 hierarchical 对照：它在 flat 16 leaf experts / buckets 上增加 coarse $\rightarrow$ fine 两级决策，但 coarse router 和 fine router 都看同一个输入表征 $z$。

该版本用于回答：

> 仅仅把 flat 16-way routing 拆成两层，是否就能带来收益？

### 3.1 输入

coarse 和 fine 共享同一表征：

$$z_{\text{coarse}}=z_{\text{fine}}=z\in\mathbb{R}^{d_r}$$

默认：

$$C=4,\qquad F=4,\qquad M=C F=16$$

### 3.2 Router 公式

coarse logits：

$$g_C(z)=W_C z+b_C,\qquad W_C\in\mathbb{R}^{C\times d_r}$$

coarse id：

$$c^*=\arg\max_{c\in\{0,\ldots,C-1\}}\operatorname{softmax}(g_C(z))_c$$

每个 coarse group 有自己的 fine router：

$$g_F^{(c)}(z)=W_F^{(c)}z+b_F^{(c)},\qquad
W_F^{(c)}\in\mathbb{R}^{F\times d_r}$$

fine id：

$$f^*=\arg\max_{f\in\{0,\ldots,F-1\}}
\operatorname{softmax}(g_F^{(c^*)}(z))_f$$

leaf id：

$$m^*=F c^*+f^*\in\{0,\ldots,15\}$$

### 3.3 Expert / Index Bucket 公式

MoE expert 输出：

$$\operatorname{MoE}_{\text{hier-A}}(r_t)=E_{F c_t+f_t}(r_t)$$

top-$K_e$ 时可以在 leaf probability 上取 top-k。leaf probability 为：

$$p(m=(c,f)\mid z)=p_C(c\mid z)\ p_F(f\mid c,z)$$

index bucket：

$$\mathcal I_{\ell,a,c,f}
=
\{i:\operatorname{route}_{\text{key}}(k_i)=(c,f)\}$$

也可写成 flat leaf bucket：

$$\mathcal I_{\ell,a,m}
=
\mathcal I_{\ell,a,\lfloor m/F\rfloor,m\bmod F}$$

query 候选集合：

$$S_t^{\text{hier-A}}
=
\mathcal I_{\ell,a,c_q,f_q}$$

### 3.4 Attention 计算方式

hierarchical routing 只负责召回候选集合：

$$\operatorname{Attn}_{\text{hier-A}}(q_t,K,V)
=
\sum_{i\in S_t^{\text{hier-A}}}
\operatorname{softmax}_{i\in S_t^{\text{hier-A}}}
(q_t^\top k_i/\sqrt{d_h})v_i$$

### 3.5 参数规模

coarse router：

$$P_C=Cd_r+C$$

fine routers：

$$P_F=C(Fd_r+F)=CFd_r+CF$$

因为 $CF=16$：

$$P_{\text{router-hier-A}}=(C+16)d_r+(C+16)$$

当 $C=4,F=4$：

$$P_{\text{router-hier-A}}=20d_r+20$$

expert 数量仍是 16：

$$P_{\text{experts-hier-A}}=16P_E$$

总差异项：

$$P_{\text{hier-A-extra}}
=
((C+16)d_r+(C+16))+16P_E$$

Variant A 相比 flat 只多出 coarse router 的参数量级：

$$P_{\text{router-hier-A}}-P_{\text{router-flat}}=Cd_r+C$$

---

## 4. Hierarchical Variant B: 谱段 / 分层表征 Routing

Variant B 是本项目的目标设计：不只是把 16-way routing 拆成两层，而是让 coarse / fine router 看到不同层级的表征。

该版本使用谱空间拆分：

- coarse router 不看最通用的 head 成分；
- fine router 进一步去掉 middle-head 成分，只看更细粒度、长尾相关的 tail 信息；
- expert 和 final attention 仍使用完整原始表示，不使用 conditional input 改写 expert 输入。

### 4.1 输入

对训练集中的 router 输入估计 PCA：

$$s=(z-\mu)P$$

其中 $\mu$ 和 $P$ 只由训练集估计。将谱空间分成：

- `head`：最前面的全局主成分，维度为 $H$；
- `middle-head`：偏粗粒度的中间前段，维度为 $G$；
- `tail`：更细粒度和长尾相关的部分。

设 $s_{a:b}$ 表示谱坐标切片，则：

$$z_{\text{coarse}}=s_{H+1:d_r}$$

$$z_{\text{fine}}=s_{H+G+1:d_r}$$

其维度为：

$$d_c=d_r-H$$

$$d_f=d_r-H-G$$

注意：谱段只用于 routing。expert 输入仍是完整 $r_t$，attention logit 仍使用原始 $q_t,k_i$。

### 4.2 Router 公式

coarse router：

$$g_C(z)=W_C z_{\text{coarse}}+b_C,\qquad
W_C\in\mathbb{R}^{C\times d_c}$$

$$c^*=\arg\max_c\operatorname{softmax}(g_C(z))_c$$

fine router：

$$g_F^{(c)}(z)=W_F^{(c)}z_{\text{fine}}+b_F^{(c)},\qquad
W_F^{(c)}\in\mathbb{R}^{F\times d_f}$$

$$f^*=\arg\max_f\operatorname{softmax}(g_F^{(c^*)}(z))_f$$

leaf id：

$$m^*=F c^*+f^*\in\{0,\ldots,15\}$$

### 4.3 Expert / Index Bucket 公式

MoE 输出仍由 16 个完整 leaf experts 计算：

$$\operatorname{MoE}_{\text{hier-B}}(r_t)=E_{F c_t+f_t}(r_t)$$

也就是说，routing 使用谱段：

$$r_t\rightarrow s_t\rightarrow (z_{\text{coarse}},z_{\text{fine}})
\rightarrow (c_t,f_t)$$

但 expert 计算使用完整输入：

$$E_{F c_t+f_t}(r_t)$$

KV index bucket：

$$\mathcal I_{\ell,a,c,f}
=
\{i:\operatorname{route}_{\text{key}}(k_i)=(c,f)\}$$

query 候选集合：

$$S_t^{\text{hier-B}}
=
\mathcal I_{\ell,a,c_q,f_q}$$

如果需要更高 recall，可以 union top-$B$ leaf buckets：

$$S_t^{\text{hier-B-topB}}
=
\bigcup_{(c,f)\in \operatorname{TopB}(p_C(c\mid q_t)p_F(f\mid c,q_t))}
\mathcal I_{\ell,a,c,f}$$

### 4.4 Attention 计算方式

attention 仍是候选集合内 exact attention：

$$\operatorname{Attn}_{\text{hier-B}}(q_t,K,V)
=
\sum_{i\in S_t^{\text{hier-B}}}
\operatorname{softmax}_{i\in S_t^{\text{hier-B}}}
(q_t^\top k_i/\sqrt{d_h})v_i$$

谱空间只决定搜索范围，最终 score 必须回到原始 attention：

$$q_t^\top k_i/\sqrt{d_h}$$

### 4.5 参数规模

coarse router：

$$P_C=Cd_c+C=C(d_r-H)+C$$

fine routers：

$$P_F=C(Fd_f+F)=CF(d_r-H-G)+CF$$

因为 $CF=16$：

$$P_{\text{router-hier-B}}
=C(d_r-H)+16(d_r-H-G)+C+16$$

expert 数量仍是 16：

$$P_{\text{experts-hier-B}}=16P_E$$

总差异项：

$$P_{\text{hier-B-extra}}
=C(d_r-H)+16(d_r-H-G)+C+16+16P_E$$

PCA 统计量不是 trainable router 参数。若需要计入额外存储，可记为：

$$P_{\text{pca-storage}}=d_r+d_r d_{\text{pca}}$$

其中 $d_{\text{pca}}$ 是实际保留的 PCA 维度。

---

## 5. Optional Oracle Routing / oracle_topm Controls

oracle 控制项只用于分析 routing / indexing 的上限，不作为可部署模型。

### 5.1 Oracle Expert Routing

如果合成任务有真实机制标签 $m_t^{\text{true}}$，可以直接设置：

$$\operatorname{route}_{\text{oracle}}(r_t)=m_t^{\text{true}}$$

MoE 输出：

$$\operatorname{MoE}_{\text{oracle}}(r_t)=E_{m_t^{\text{true}}}(r_t)$$

如果没有真实标签，也可以用 loss 最小的 expert 作为离线 oracle：

$$m_t^{\text{oracle}}
=
\arg\min_m \mathcal L(E_m(r_t),y_t)$$

该设置用于估计 expert capacity 上限，不用于真实推理。

### 5.2 Oracle Indexing / oracle_topm

对于 attention search，可以用 full attention score 定义 oracle bucket 选择。先计算全量 score：

$$s_{t i}=q_t^\top k_i/\sqrt{d_h},\qquad i\le t$$

如果 oracle 直接选择 token：

$$S_t^{\text{oracle-token}}
=
\operatorname{TopM}_{i\le t}(s_{t i})$$

如果 oracle 选择 buckets，设每个 bucket 的最佳 full-attention score 为：

$$b_{t,m}=\max_{i\in\mathcal I_{\ell,a,m}}s_{t i}$$

则：

$$B_t^{\text{oracle-topm}}
=
\operatorname{TopM}_{m\in\{0,\ldots,15\}}(b_{t,m})$$

候选集合：

$$S_t^{\text{oracle-topm}}
=
\bigcup_{m\in B_t^{\text{oracle-topm}}}\mathcal I_{\ell,a,m}$$

其中 `oracle_topm` 控制 oracle 可以选择多少个 leaf buckets。

### 5.3 Attention 计算方式

oracle 仍只改变候选集合：

$$\operatorname{Attn}_{\text{oracle}}(q_t,K,V)
=
\sum_{i\in S_t^{\text{oracle}}}
\operatorname{softmax}_{i\in S_t^{\text{oracle}}}
(q_t^\top k_i/\sqrt{d_h})v_i$$

如果 `oracle_topm=16`，则 oracle bucket union 等价于 full attention：

$$S_t^{\text{oracle-topm}=16}=\{1,\ldots,t\}$$

### 5.4 参数规模

oracle routing 不引入 trainable router 参数：

$$P_{\text{router-oracle}}=0$$

如果 oracle 只替换 router，仍使用同一组 16 experts：

$$P_{\text{experts-oracle}}=16P_E$$

如果 oracle 只用于 indexing 上限评估，则无额外 trainable 参数，只有离线 full-score 计算成本。

---
