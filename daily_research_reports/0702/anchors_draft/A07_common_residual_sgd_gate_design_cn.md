# A07 Common-Residual SGD Gate Design

## 0. Purpose

**目标：** 判断 Adam / SCALE / SGD-LL 的有效性是否主要来自抑制 high-gain common component，使 rare / residual component 获得足够更新；若成立，设计一种 common-aware SGD / MoE 更新规则，在不使用 Adam 全状态的情况下提高 SGD 最大稳定学习率并降低 rare loss。

---

## 1. Phenomenon

1. LLM 预训练中 SGD 的全局有效步长很小；直接增大学习率会由少数 loud layer / loud token 先触发不稳定。
2. SGD-LL 用 layer-wise 与 per-token clipping 让 SGD 使用大 LR，说明问题不只是 loss landscape，而是更新空间中存在局部过大方向。
3. SCALE 显示 column-wise normalization + last-layer momentum 已能接近 Adam，说明 output-dimension / token-column scale 是关键轴。
4. 既有 gating line 显示：common component、early feedback 与错误 hidden population 会破坏 routing preservation；controlled D07 中 common-control 可降低 rare interference，但 real-DCLM 上 common operator 仍不稳定。

---

## 2. Mechanism Guess

**核心猜想：** common feature 形成 high-gain subspace；频繁 token 与 shared linguistic component 的梯度沿该子空间更大、更稳定，从而在 SGD / gate update 中占据过多更新预算。rare token 即使本身含有正确 residual signal，也会被其 common part 带偏或淹没。

将输出层梯度写为：

\[
G_j=\frac{1}{B}\sum_i h_i(p_{i,j}-1\{y_i=j\}) .
\]

令 \(P_C\) 为 hidden-side common projector，则：

\[
G_j=P_CG_j+(I-P_C)G_j=G_{C,j}+G_{R,j}.
\]

如果 \(\|G_{C,j}\|\gg \|G_{R,j}\|\)，普通 SGD 更新主要服务 common component；rare-specific residual 更新不足。

---

## 3. Candidate Method

### 3.1 Common-residual update split

对每个输出 token column 或每个 expert block：

\[
\Delta W_j=-\eta_C G_{C,j}-\eta_R G_{R,j},\qquad \eta_R>\eta_C.
\]

更保守版本：

\[
G'_j=(I-P_C)G_j+\alpha P_CG_j,\qquad 0\leq \alpha<1.
\]

其中 \(\alpha\) 控制 common 保留量，避免直接抹去有用 common signal。

### 3.2 MoE gating version

1. Gate 使用 residual representation：

\[
g(h)=\arg\max_e w_e^\top (I-P_C)h.
\]

2. Experts 可接收 full hidden state \(h\)，但 expert 更新分解为 common / residual 两个 LR。
3. 允许 common expert 与 rare experts 使用不同 LR 或 clipping 阈值。

---

## 4. Main Metrics

| Metric | Meaning |
|---|---|
| \(\eta_{\max}\) | 不发散的最大 SGD LR |
| \(\rho_j=\eta\|G_j\|/\|W_j\|\) | token-column 局部相对更新 |
| \(\rho_{R,j}=\eta_R\|G_{R,j}\|/\|W_j\|\) | rare residual 有效更新 |
| rare loss | 是否真正改善 rare token / rare feature |
| common loss / total loss | common 抑制是否伤害主任务 |
| conflict readability | \((I-P_C)h\) 是否保留 rare/conflict signal |
| projector stability | mean-common、top-PC、router-row projector 结论是否一致 |

---

## 5. Minimal Experiments

### E1. Synthetic token experiment

构造 token：

\[
h_i=c+r_i+\epsilon_i,
\]

其中 \(c\) 是 shared common component，\(r_i\) 是 rare-specific component。控制 token frequency，使 frequent tokens 有更强 common update。

比较：SGD、SGD-LL、column-normalized SGD、common-residual SGD、MoE residual gate。

**Primary readout:** \(\eta_{\max}\)、rare loss、common loss、\(\rho_C/\rho_R\)。

### E2. Controlled D07 bridge

在已验证 rare-conflict surface 上，比较 raw gate 与 residual gate：

\[
h \quad \text{vs.} \quad (I-P_C)h.
\]

要求 load matched，并检查 conflict signal preservation。

### E3. Real-DCLM proxy audit

复用 gating line：raw routing vs common-subtracted routing。只 claim preservation / margin，不 claim semantic expert utility。

---

## 6. Decision Rule

**Support:**

1. common-residual update 使 \(\eta_{\max}\) 显著上升；
2. rare loss 改善，common / total loss 不恶化；
3. gain 在 load-matched baseline 下仍存在；
4. conflict readability 不下降；
5. 结论不随 reasonable \(P_C\) 定义翻转。

**Revise / park:**

1. LR ceiling 没提高；
2. 改善只来自 load balance；
3. residualization 抹掉 rare signal；
4. mean-common / top-PC / router-row projector 得出相反结论。

---

## 7. Claim Boundary

可以 claim：common-residual decomposition 是否提高 SGD 稳定 LR 与 rare update。

不能 claim：真实语义 expert、自然形成的 MoE specialization、部署级 optimizer、或 Adam 优势完全来自 common component。

---

## 8. Route

1. 先做 synthetic token + full-batch/noise/minibatch 三种条件，建立 LR ceiling 机制。
2. 再做 controlled D07，与现有 common-control rare-interference line 对齐。
3. 若通过，再做 real-DCLM proxy preservation；不直接跳到 utility。
4. 方法层先实现 common-residual SGD；再与 SCALE column normalization、SGD-LL clipping、EMA-Nesterov wrapper 组合。
