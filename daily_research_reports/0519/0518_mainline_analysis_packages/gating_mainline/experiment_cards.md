# Experiment Cards - Gating Mainline

## Experiment Card G1: Router Cell Map

### 1. Hypothesis To Decide

Router cell 由 attention-output 的实际聚合来源 / common geometry 决定，而不是人工 feature label。

### 2. Experiment Question

每个 expert cell 的高置信样本共享什么？

### 3. Setup

Model: 1-layer Transformer + MoE。

Data: synthetic trigram; uniform first, Zipf later。

Signal source: router input $z_t = AttnOut_t$; expert input $h_t$ unchanged。

### 4. Baselines

Random expert; feature-oracle expert; token-identity grouping; local/difficulty buckets。

### 5. Metrics

Top-margin examples per expert; boundary examples; within-cell attention-source agreement; token-pattern agreement; loss distribution。

### 6. Expected Outcomes

如果 expert cell 内 attention top-key pattern 一致，支持 router as attention-source classifier。

### 7. What This Can Prove

能说明 router cell 的经验语义是什么。

### 8. What This Cannot Prove

不能说明这些 cell 可作为 KV index。

---

## Experiment Card G2: Counterfactual Route Flip

### 1. Hypothesis To Decide

Router 对 feature relation 不敏感，而对 token/common/noise/attention source 更敏感。

### 2. Experiment Question

什么最小改变会翻转 expert id？

### 3. Setup

构造配对样本：same feature diff tokens; diff feature same target; same prefix diff distractor; same attention source diff label。

### 4. Metrics

route flip rate; logit margin delta; NTP loss delta; attention top-key overlap delta。

### 5. Decision

feature edit 不翻转而 token/noise edit 翻转 => router 不是 feature classifier。

---

## Experiment Card G3: Common Component Removal

### 1. Hypothesis To Decide

Common directions 支配 routing，specific feature directions 被淹没。

### 2. Experiment Question

去掉 common component 后，routing 是否更接近 feature / attention-source？

### 3. Setup

对 $z_t$ 进行 mean/top-PC/token-centroid/local-position component removal。

### 4. Metrics

route change rate; expert load; feature/expert NMI as secondary metric; attention-source/expert NMI; NTP loss under original route vs modified route。

### 5. Decision

去 common 后 feature alignment 上升但 NTP 下降：feature 存在但不是低损失主方向。

---

## Experiment Card G4: Expert Utility Landscape

### 1. Hypothesis To Decide

当前 routing 不 clean 是因为多个 experts 对同一 feature 都可用，one-feature-one-expert 没有 loss 必要性。

### 2. Experiment Question

每个 sample/feature 是否存在唯一最佳 expert？

### 3. Setup

对每个 routed position force route to every expert。

### 4. Metrics

selected-best gap; feature-oracle-best gap; number of near-best experts; utility entropy。

### 5. Decision

如果 near-best experts 多，说明 specialization failure 是 utility degeneracy，不是 representation failure。
