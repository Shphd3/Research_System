# 今晚 Agent 执行计划：把主线推进到正式 CL 裁决

## 0. 今晚只做什么

今晚不要再扩谱空间，不要再开新 band，不要直接做 hierarchy。  
今晚只做一件事：

> **把当前主线推进到 formal matched forgetting comparison。**

也就是说，固定最合理的 CL 版 expert input 和最稳定的短 horizon，正式回答：

> 在学到同样多新知识时，`G2_u50_ext` 或 `G4_u50_ext` 是否比 `G0` 忘得更少，是否接近或超过 `G0_ER`。

---

# 1. 今晚的唯一主问题

## 研究问题
在 `u50_ext + short horizon` 的设置下，factorized block 是否比普通 dense block 更适合 continual learning？

## 判定标准
必须同时看：

1. 新知识学到了多少；
2. 旧知识忘了多少；
3. 在学到同样多新知识时，谁更少忘。

---

# 2. 固定不变项

## 模型与层位
- model: `Qwen3-0.6B`
- replace layer: `8`
- hook: `post_attention_layernorm`

## 表征定义
固定 expert input 为：

$$
x_{u50\_ext} = x_{u50} + 0.25\,x_{ext}
$$

今晚不要再比较 `u25`、`u75`、`full_tail`。

## 数据协议
沿用当前已固定的 old / new domain 划分。

- old domains: `CS, Civil, MAE, Medical, Psychology`
- new domains: `ECE, biochemistry`

每个 episode 固定：

- support: `1` 个 `256 tokens` 的 support chunk
- query: `16` 个 new-domain query chunks

如果已有固定 seed 和 episode 列表，今晚所有组必须共用同一份 episode 列表。

## adaptation regime
主 regime 固定：

$$
U = 8
$$

保留两个学习率倍率：

- `0.5x`
- `1.0x`

今晚不要再扫 `0.25x`，也不要再扫 `U=16/32`。

---

# 3. 今晚要跑的组

只跑四组：

1. `G0`
2. `G0_ER`
3. `G2_u50_ext`
4. `G4_u50_ext`

## 组定义

### G0：baseline FFN
作用：普通 dense 基线。

### G0_ER：baseline FFN + replay
作用：简单 continual learning 基线。  
它不是结构公平对照，但它决定我们能不能说“更适合 continual learning”。

### G2_u50_ext：split dense
$$
h_{\mathrm{out}}
=
h_{\mathrm{in}} + F_c(x) + F_t(x_{u50\_ext})
$$

作用：检验“只做共享分支 + 可塑分支分离”，有没有 CL 价值。

### G4_u50_ext：raw router + tail experts
$$
h_{\mathrm{out}}
=
h_{\mathrm{in}} + F_c(x) + \sum_e g_e(x)F_e(x_{u50\_ext})
$$

作用：检验在 `u50_ext` 上，routing 是否带来额外 CL 价值。

---

# 4. adaptation 时允许更新哪些参数

## 通用冻结规则
adaptation 期间统一冻结：

- backbone；
- 非第 8 层参数；
- attention block；
- layer norm；
- LM head；
- PCA / band projector；
- common branch 中不该更新的共享参数。

## 每组允许更新

### G0
只更新 replacement FFN。

### G0_ER
只更新 replacement FFN，但 loss 中加入 replay 项。

### G2_u50_ext
冻结 common 分支，只更新 tail branch。

### G4_u50_ext
冻结 common 分支，更新 router 与 tail experts。

如果代码里当前还有其他参数在更新，今晚必须先排查并关掉。

---

# 5. 必须输出的指标

## 新知识学习收益
$$
LG(U) = L_{\text{query,before}} - L_{\text{query,after }U}
$$

## 旧知识遗忘代价
$$
FC(U) = L_{\text{old,after }U} - L_{\text{old,before}}
$$

## 只惩罚遗忘
$$
FC^+(U)=\max(FC(U),0)
$$

## 综合分数
$$
RAS(U)=LG(U)-FC^+(U)
$$

## matched learning gain 比较
必须输出：

1. `ReachRate`
2. `matched forgetting`

即：

- 先用 `G0` 在该 episode 的 learning gain 作为 anchor；
- 再看其他组达到同样 learning gain 时，forgetting 有多少。

如果某组根本达不到 anchor，就不能只因为“忘得少”而说它更适合 CL。

---

# 6. 今晚的最小执行矩阵

## 主矩阵
- 组：`G0 / G0_ER / G2_u50_ext / G4_u50_ext`
- horizon：`U=8`
- lr multiplier：`0.5x / 1.0x`
- seeds：至少 `3`

总共：

```text
4 groups × 2 lr × 3 seeds
```

如果资源真的紧张，优先级如下：

### 优先级 1
- `G0 @ 0.5x, 1.0x`
- `G2_u50_ext @ 0.5x, 1.0x`
- `G4_u50_ext @ 0.5x, 1.0x`

### 优先级 2
- `G0_ER @ 0.5x, 1.0x`

如果第一优先级都没有稳定结果，今晚不要再跑任何扩展组。

---

# 7. 今晚必须产出的表和图

## 表
1. 每组每个 regime 的 `LG / FC / FC+ / RAS`
2. 每组的 `ReachRate`
3. 每组的 `matched forgetting`
4. 每组在 old-domain 各子集上的 forgetting
5. 每组在 new query 的 common / middle / rare token 上的 learning gain

## 图
1. `LG` 随 step 变化
2. `FC` 随 step 变化
3. `RAS` 柱状图
4. `matched forgetting` 柱状图
5. `ReachRate` 柱状图

如果时间紧，优先保证表 1、表 2、表 3 和图 1、图 4。

---

# 8. 今晚的判定门槛

## Gate A：split-dense CL block 是否成立
如果：

- `G2_u50_ext` 的 `RAS` 高于 `G0`
- 且 matched forgetting 低于 `G0`

则可以写：

> **共享分支 + 可塑 functional span 的单层结构，对 CL 有真实价值。**

## Gate B：routing 是否开始带来额外 CL 价值
如果：

- `G4_u50_ext` 的 `RAS` 高于 `G2_u50_ext`
- 且 matched forgetting 不高于 `G2_u50_ext`

则可以写：

> **在 `u50_ext` 上，input-dependent expert selection 开始带来额外 CL 价值。**

## Gate C：能不能说“更适合 continual learning”
只有在下面条件满足时才能讲得比较强：

1. `G2` 或 `G4` 明显优于 `G0`
2. 并且接近或超过 `G0_ER`

如果只赢 `G0`，但明显输 `G0_ER`，只能说：

> **结构有帮助，但还不能说比简单 CL baseline 更强。**

---

# 9. 今晚不要做什么

1. 不要再切 `u25`、`u50`、`u75`；
2. 不要再加新组；
3. 不要再开 `U=16/32`；
4. 不要开始真实 recursive；
5. 不要把 dictionary 直接塞进主线；
6. 不要为了单个组的结果临时改协议。

如果某组不稳定，记录失败，不要临场改实验定义。

---

# 10. 明早应该怎么读结果

## 如果 `G2_u50_ext > G0`
说明：

> 不需要 routing，光是“共享分支 + 可塑 functional span 分离”就已经有 CL 价值。

下一步：
- 保留 `G2` 作为强基线；
- 再判断 `G4` 是否值得继续。

## 如果 `G4_u50_ext > G2_u50_ext`
说明：

> routing 在 CL 中已经开始带来增益。

下一步：
- 才值得继续做 router calibration；
- 再考虑 advantage-aligned router。

## 如果 `G2` 和 `G4` 都不如 `G0`
说明：

> 当前 CL 主线还没站住。

下一步：
- 不要继续做 hierarchy；
- 回到 update rule / adaptation parameterization；
- 检查是不是 common branch 冻结方式或 update budget 还有问题。

## 如果赢 `G0` 但输 `G0_ER`
说明：

> 架构路线有希望，但还没有超过最简单的 CL 方法。

下一步：
- 可以继续做 router calibration 或更稳的 adaptation 规则；
- 但汇报时不能夸大。

---

# 11. 今晚执行顺序建议

## Step 1
确认数据、episode、projector、seed、更新参数规则全部固定。

## Step 2
先跑：
- `G0`
- `G2_u50_ext`
- `G4_u50_ext`

每组先出 `0.5x` 和 `1.0x` 的单 seed smoke，确认流程不炸。

## Step 3
补齐 `3 seeds`。

## Step 4
补 `G0_ER`。

## Step 5
统一统计：
- `LG`
- `FC`
- `RAS`
- `ReachRate`
- `matched forgetting`

## Step 6
只写一个结论：
- 是不是已经能进入正式 CL 结构排序；
- 还是仍需回到单层 adaptation 机制。

---

# 12. 一句话收尾

> **今晚不是继续探索，而是正式裁决：在 `u50_ext + U=8` 这个 regime 下，factorized block 能不能在 matched learning gain 下比普通 dense 更少遗忘。只要这一步答出来，主线就会一下子清楚很多。**
