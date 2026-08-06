# Phase7-Phase8 联合实验报告

## 0. 一页结论

`Phase7-Phase8` 这条线的核心任务，不是再证明 single-layer tail-conditioned block 在静态 NTP 上是否成立，而是回答一个更具体的问题：

$$
\text{进入 continual learning 之前，expert 到底该看什么输入；进入 CL 之后，失败首先来自哪里。}
$$

当前最稳的结论是：

1. 不能再把
   $$
   x_t = (I - V_{16}V_{16}^{\top})(x-\mu)
   $$
   这个 `full PCA tail residual` 直接当作 CL-MoE 的第一版 expert input。
2. `tail` 这条方向没有被否掉；真正有前景的是 `mid/upper-mid family`。
3. 静态 old-stage block replacement 更偏向更窄、更稳的 `u25`；但进入 CL 后，更偏向更完整的 functional span：
   $$
   u50\_ext.
   $$
4. 当前 CL 失败的第一原因不是 band 选错，而是 `adaptation horizon` 过长，`U=16/32` 会系统性 over-update。
5. 因此下一步不应直接进入 full `Phase8` 或 hierarchy，而应回到 `matched forgetting` 主线，在固定 `u50_ext`、短 horizon 的 regime 上做正式比较。

---

## 1. 研究问题与这条线的定位

在 `Phase1-Phase6`，我们已经走到下面这一步：

- 真实 hidden 中存在 `shared head`；
- single-layer tail-conditioned block 在真实模型上成立；
- `expert-tail input` 比 `router-only tail input` 更重要；
- 完整单层 block 已出现 `LM-relevant specialization`。

此时自然进入下一个问题：

$$
\text{这种 tail-conditioned 结构，是否也更适合少样本 continual learning？}
$$

但在进入 CL 之前，必须先固定一个 expert input。  
因此 `Phase7-Phase8` 的逻辑链是：

1. 先检查当前的 `PCA tail residual` 定义是否靠谱；
2. 如果不靠谱，就先重定义 expert input；
3. 再把新的 candidate input 带入 CL smoke；
4. 最后把问题收束到正式 `matched forgetting` 比较。

---

## 2. 统一符号

我们研究的是 `Qwen3-0.6B` 第 `8` 层、`post_attention_layernorm` 位置的 hidden state，记为：

$$
x \in \mathbb{R}^d.
$$

对 calibration hidden 估计均值：

$$
\mu.
$$

对 centered hidden

$$
x-\mu
$$

做 PCA，前 `16` 个主方向记为：

$$
V_{16}.
$$

于是最早的 `full PCA tail residual` 定义是：

$$
x_t = (I - V_{16}V_{16}^{\top})(x-\mu).
$$

再定义累计解释方差达到 `95%` 的谱位置：

$$
r95 = 781.
$$

如果某个 band 对应一组 PCA 维度索引 \(B\)，其投影记为：

$$
P_B(x-\mu).
$$

---

## 3. Phase7：表征基础 gate

### 3.1 目标

`Phase7` 只回答一个 gate 问题：

$$
\text{PCA tail residual 是否仍然足以作为 CL-MoE 第一版 expert input？}
$$

### 3.2 固定设置

- model: `Qwen3-0.6B`
- layer: `8`
- hook: `post_attention_layernorm`
- `k = 16`
- calibration / probe / dictionary / intervention 共用同一批 hidden states

### 3.3 做了什么

1. 把谱空间拆成：
   - `head = [1,16]`
   - `mid = [17,r95]`
   - `ext = [r95+1,d]`
   - `full_tail = [17,d]`
2. 做 probe，检查这些 band 里是否还有可读的语义信息；
3. 做 functional intervention，检查移除某个 band 是否会恶化 next-token loss；
4. 比较 `PCA top-K` 与 `sparse dictionary top-K` 的重构与统计性质。

### 3.4 正式结果

gate 为：

- `R1_pass = false`
- `R2_pass = false`
- `R3_continue_with_pca_tail = false`

功能性上最关键的结果是：

$$
\Delta L_{\mathrm{remove\;mid}} \gg \Delta L_{\mathrm{remove\;ext}}.
$$

具体地：

- `remove_mid_delta_loss = 0.0542`
- `remove_ext_delta_loss = 0.0038`

dictionary 与 PCA top-K 的重构对比：

$$
\mathrm{MSE}_{\mathrm{PCA-top16}} = 0.3831
$$

$$
\mathrm{MSE}_{\mathrm{dict}} \approx 0.2379 \pm 0.0009
$$

dictionary atom 到 PCA band 的 overlap 结果：

- `head_ratio_mean ≈ 0.065`
- `mid_ratio_mean ≈ 0.786`
- `ext_ratio_mean ≈ 0.149`
- `ext_dominant_fraction = 0`

### 3.5 结论

`Phase7` 否掉的不是 “tail 方向”，而是：

$$
\text{把 top-16 之外的整块 residual 直接当作 expert input。}
$$

更准确地说：

- `full_tail` 有语义、有功能，不是纯噪声；
- 但真正稳定的主功能区主要在 `mid-band`；
- dictionary 比 PCA top-K 更像 token-level sparse feature basis；
- 但 dictionary 还没有长成一个可直接替代主线的 residual 定义。

因此：

$$
\text{暂停 CL 主线，先重新定义 expert input。}
$$

---

## 4. Phase7.5：candidate input 预筛选

### 4.1 目标

既然 `full_tail` 太粗，就先用静态 old-stage block replacement 做一个便宜的 candidate screening。

### 4.2 候选输入

1. `full_tail`
2. `mid_only`
3. `mid_plus_small_ext`

其中：

$$
x_{\mathrm{midext}} = x_{\mathrm{mid}} + 0.25\,x_{\mathrm{ext}}.
$$

### 4.3 结构族

1. `split_dense`
   $$
   h_{\mathrm{out}} = h_{\mathrm{in}} + E_c(x) + E_t(x_{\mathrm{candidate}})
   $$

2. `raw_router_expert`
   $$
   h_{\mathrm{out}} = h_{\mathrm{in}} + E_c(x) + \sum_i g_i(x)E_i(x_{\mathrm{candidate}})
   $$

这里 routed 组固定：

$$
\text{router input} = x,
$$

只改变 `expert input`。

### 4.4 结果

gate 为：

- `beats_full_tail_in_both_structures = true`
- `best_split_variant = split_dense_mid_plus_small_ext`
- `best_routed_variant = raw_router_expert_mid_only`
- `should_enter_phase8 = false`

额外做的 `mid_fraction` 扫描显示：

- `split_best_mid_fraction = 0.5`
- `routed_best_mid_fraction = 0.5`

### 4.5 结论

这一轮把 candidate 范围从：

$$
\text{full tail}
$$

收缩到：

$$
\text{mid family}.
$$

---

## 5. Phase7.6：mid-band refinement

### 5.1 目标

既然 `mid family` 才是重点，就继续把 `mid` 细切，看：

1. 哪个子带最适合作为 expert input；
2. 当前是否已经出现了 hierarchy-ready 的 coarse/fine 证据。

### 5.2 band 定义

固定：

- `k = 16`
- `r95 = 781`

定义：

$$
W = r95 - 16 = 765
$$

$$
m25 = 207,\qquad m50 = 398,\qquad m75 = 589.
$$

于是：

- `u25 = [17, 207]`
- `u50 = [17, 398]`
- `u75 = [17, 589]`
- `l50 = [399, 781]`
- `ext = [782, d]`

候选输入：

$$
x_{u25}=P_{u25}(x-\mu)
$$

$$
x_{u50}=P_{u50}(x-\mu)
$$

$$
x_{u75}=P_{u75}(x-\mu)
$$

$$
x_{u50\_l50}=x_{u50}+0.25\,x_{l50}
$$

$$
x_{u50\_ext}=x_{u50}+0.25\,x_{ext}
$$

### 5.3 结果

gate 为：

- `best_split_variant = split_dense_u25`
- `best_routed_variant = raw_router_expert_u25`
- `beats_full_tail = true`
- `best_single_band = u25`
- `lower_mid_is_complementary = false`
- `hierarchy_ready = false`
- `recommended_phase8_smoke_inputs = ["u25", "u50_ext"]`

Frozen intervention 结果：

- `remove_u50_delta_all = 0.0576`
- `remove_l50_delta_all = 0.0159`
- `remove_u50_delta_middle = 0.0765`
- `remove_l50_delta_middle = 0.0237`
- `remove_u50_delta_rare = 0.0875`
- `remove_l50_delta_rare = 0.0277`

### 5.4 结论

这轮出现了一个关键张力：

- 从静态 block replacement 的“最稳可学习输入”看：
  $$
  u25
  $$
  最优；
- 从 frozen intervention 的“功能负载”看：
  $$
  u50
  $$
  承载了更多的 next-token 功能质量。

因此，当前拿到的是：

$$
\text{core band vs functional span}
$$

的张力，而不是：

$$
\text{hierarchy-ready coarse/fine evidence}.
$$

---

## 6. Phase8-smoke：把 `u25` 和 `u50_ext` 带入 CL

### 6.1 目标

`Phase7.6` 已经把问题收束成一个二选一：

- `u25`：更窄、更干净、更稳的 core band
- `u50_ext`：更宽、带一点外延、功能更完整的 span

因此 `Phase8-smoke` 只问：

$$
\text{在 CL setting 里，模型最终偏向 u25 还是 u50\_ext？}
$$

### 6.2 固定协议

- old domains: `CS, Civil, MAE, Medical, Psychology`
- new domains: `ECE, biochemistry`
- support: `1 support chunk of 256 tokens`
- query: `16` 个 new-domain chunks
- adaptation steps: `U = 32`

### 6.3 组别

1. `G0 = baseline_ffn`
2. `G0_ER = baseline_ffn + replay`
3. `G2_u25 = split_dense_u25`
4. `G2_u50_ext = split_dense_u50_ext`
5. `G4_u25 = raw_router_expert_u25`
6. `G4_u50_ext = raw_router_expert_u50_ext`

其中：

$$
G4\_u50\_ext:\;
h_{\mathrm{out}} = h_{\mathrm{in}} + F_c(x) + \sum_e g_e(x)F_e(x_{u50\_ext})
$$

也就是说：

- router 仍看 raw `x`
- experts 看 `u50_ext`

### 6.4 结果

gate 为：

- `best_split_input = u50_ext`
- `best_routed_input = u50_ext`
- `best_model_group = G4_u50_ext`
- `routing_adds_cl_value = false`
- `best_model_over_g0 = false`
- `should_expand_to_full_phase8 = false`

### 6.5 结论

进入 CL 后，模型更偏向：

$$
u50\_ext > u25.
$$

这说明：

> 对 CL 而言，更重要的不是最窄的 core，而是更完整的 functional span。

但这轮还不能进入 full `Phase8`，因为所有组最终都没有进入稳定正 `LG` 区间。

---

## 7. Phase8.1：stabilization smoke

### 7.1 目标

这轮不再问 band，而是固定：

$$
\text{expert input} = u50\_ext
$$

只问：

$$
\text{CL 失败主要来自 horizon 太长，还是 LR 太大？}
$$

### 7.2 固定组

1. `G0`
2. `G0_ER`
3. `G2_u50_ext`
4. `G4_u50_ext`

### 7.3 sweep

$$
U \in \{4,8,16,32\}
$$

$$
\text{lr multiplier} \in \{0.25\times, 0.5\times, 1.0\times\}
$$

### 7.4 核心指标

新知识 query 上的 learning gain：

$$
LG(U) = L_{\text{query,before}} - L_{\text{query,after }U}
$$

old-domain forgetting cost：

$$
FC(U) = L_{\text{old,after }U} - L_{\text{old,before}}
$$

只惩罚遗忘的形式：

$$
FC^+(U)=\max(FC(U),0)
$$

综合分数：

$$
RAS(U)=LG(U)-FC^+(U)
$$

此外还报告：

- `ReachRate`
- `matched forgetting`

其中 `ReachRate > 0` 表示：已经进入“可按 matched-LG 做 forgetting 比较”的区间。

### 7.5 结果

gate 为：

- `best_group = G4_u50_ext`
- `best_U = 8`
- `best_lr_multiplier = 1.0x`
- `any_group_LG_nonnegative = true`
- `any_group_reachrate_positive = true`
- `should_return_to_matched_forgetting_stage = true`

必须区分两个概念：

1. 全局最优 `RAS` regime：
   $$
   G4\_{u50\_ext} @ U=8,\; 1.0\times
   $$

2. 第一个真正进入可比较 CL 区间的代表性 regime：
   $$
   G4\_{u50\_ext} @ U=8,\; 0.5\times
   $$

### 7.6 结论

这轮最重要的结果不是 “LR 太大”，而是：

$$
\text{adaptation horizon 太长。}
$$

具体表现为：

- `U = 4/8` 时，多组已经进入 `LG(U)\ge 0`
- `U = 16/32` 后，几乎系统性转负

所以当前更像是：

> 模型前几步能学到东西，但后几步发生了 over-update。

---

## 8. 现在可以稳讲的范围

`Phase7-Phase8` 现在可以稳讲的范围，是下面这 6 条：

1. `full PCA tail residual` 已经不再适合作为 CL expert input v1。
2. `tail` 方向没有被否掉；真正有前景的是 `mid/upper-mid family`。
3. 静态 old-stage 更偏更窄的 core：
   $$
   u25
   $$
4. 进入 CL 后，更偏更完整的 functional span：
   $$
   u50\_ext
   $$
5. 当前 CL 的第一瓶颈不是 band 选错，而是 `adaptation horizon` 过长。
6. 现在终于进入了“可以做 matched forgetting 比较”的区间，因此下一步应回到正式 CL 比较，而不是继续做 band slicing 或直接进 hierarchy。

---

## 9. 还不能讲满的边界

下面这些目前还不能讲得太满：

1. 不能说 dictionary 已经是主线可部署的 expert input。
2. 不能说 router input 现在必须从 raw `x` 改成 tail-like input。
3. 不能说 routing 已经带来本质性的 CL 增益；目前 `G4_u50_ext` 最强，但优势还依赖短 horizon regime。
4. 不能说 hierarchy ready。
5. 不能说 full `Phase8` ready；目前只是回到了 `matched forgetting` 的正式比较入口。

---

## 10. 与主线的关系：我们走到哪一步了

把整条研究主线压缩成一句话：

1. `Phase1-Phase6` 证明了：
   - shared head 存在；
   - single-layer tail-conditioned block 在真实模型上成立；
   - expert-tail input 更重要；
   - 单层 block 已有 functional specialization。

2. `Phase7-Phase8` 进一步证明了：
   - 原始 `full tail` 输入定义不够好；
   - CL 更偏 `u50_ext` 而不是 `u25`；
   - 当前真正卡住的第一瓶颈是短 support 下的 over-update。

所以我们现在 reach 到的，是：

$$
\text{已经找到更合理的 CL expert input，并找到了可比较的短-horizon CL regime。}
$$

但我们还没有 reach 到：

$$
\text{matched forgetting 的正式结构排序}
$$

更没有 reach 到：

$$
\text{hierarchical MoE 已成立}
$$

---

## 11. 下一步建议

最自然的下一步不是：

- full `Phase8`
- hierarchy
- 再做一轮 `u25 vs u50_ext`

而是：

1. 固定 expert input：
   $$
   u50\_ext
   $$
2. 以
   $$
   U=8
   $$
   为主，保留 `0.5x / 1.0x` 两个 regime；
3. 回到正式 `matched forgetting` 比较：
   - `G0`
   - `G0_ER`
   - `G2_u50_ext`
   - `G4_u50_ext`

换句话说，当前更该做的是：

$$
\text{formal matched forgetting comparison}
$$

而不是：

$$
\text{more band slicing or hierarchy expansion}.
$$
