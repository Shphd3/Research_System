# 概率树与 full-position NTP 何时使完整参数低有效秩？

## 1. 核心问题

概率树中跨 contexts 共享的 $k$ 个 causal mappings、每个至多 $r$ 个任务自由度，能否通过 full-position NTP 的重复 exposure 和 pure SGD，在 Gaussian 满秩基座上形成主导能量的 rank-$q_0$ task spike，其中 $q_0:=kr$？

## 2. 结论

**在固定特征、线性可分的受控 contrast-NTP writer 中，证明链已经闭合：固定 mapping coordinates 给出实际任务维数 $q_\star\le q_0:=kr$，full-position NTP exposure 在共享正 margin 上相干累积，pure SGD 使该低维 task spike 持续增长；当 spike 压过固定 Gaussian bulk 时，完整 $W_T$ 虽一般仍满秩，但其 rank-$q_0$ 外相对谱能量趋零。**

**精确定理边界：** 受控模型采用“概率树事件 $\to a_e=\sum_{j\in\mathcal J_e}E_jc_{e,j}\to o_e=Wa_e\to$ NTP contrast loss”：$c_{e,j}$ 是事件调用 mapping $j$ 时的任务变量，固定矩阵 $E_j$ 将其写入 ambient feature space；$a_e$ 直接替代真实网络经 embedding 与 attention/MLP 形成的 hidden activation，且 $W$ 是唯一训练的 writer。因此 T1--T6 证明的是 fixed-feature writer，而不是端到端 learned representation；推广到 residual MLP 或一层 Transformer 还需验证稳定的 activation envelope、指定 $W_2$ 或 $W_O/W_2$ 持续承担 margin growth，以及累计空间外更新相对 task spike 消失。

full-position NTP 的作用由 mapping effective exposure 与 gradient coherence 定义；若 root-only 已提供无限相干 exposure，它也可能达到同一渐近极限，因此不能把 objective 名称本身写成优势。

## 3. 关键公式

$$
W_T=W_0+S_T+R_T,\quad \operatorname{rank}(S_T)\le q_\star\le q_0:=kr,\quad
\frac{\|W_0+R_T\|_F}{\|S_T\|_F}\to0
\ \Longrightarrow\
\tau_{q_0}(W_T)=\tau_{kr}(W_T)\to0.
$$

这里 $S_T$ 是概率树共享坐标内的相干 task spike，$R_T$ 是任务特异 bias、随机波动与 learned-coordinate leakage；$\tau_{q_0}$ 是最佳 rank-$q_0$ 外的相对谱能量。出现 task outlier 只要求算子范数越过 bulk edge，严格弱于完整权重低有效秩。

## 4. 定理流程图

~~~mermaid
flowchart TD
    subgraph EXACT["已证明：受控线性 writer"]
        A["概率树事件：调用共享 mappings；每个 ≤r freedoms"]
        B["固定任务坐标 a_e = Σ_j E_j c_ej；q★=dim U★≤q₀=kr；直接替代真实 hidden activation"]
        D["同一 writer 跨 prefixes/positions 复用：o_e = W a_e"]
        E["∇Wℓ_e = δ_e a_eᵀ；pure SGD 得 Row(ΔW_T)⊆U★、rank(ΔW_T)≤q★"]
        G["循环 NTP exposure + 共享正 margin"]
        H["低维 task spike S_T 持续增长"]
        I["W_T = W_0 + S_T；spike 压过固定 Gaussian 基座"]
        J["τ_q₀(W_T)=τ_kr(W_T)→0；但有限时刻 W_T 一般仍满秩"]
        A --> B --> D --> E
        D --> G --> H
        E --> H --> I --> J
    end
    subgraph OPEN["未证明：从真实 tokens 到任务坐标"]
        K["tokens"]
        L["learned embedding / MLP / Transformer 产生 activation m_e"]
        N{"m_e 是否跨 contexts 和训练路径稳定落入同一 U*？"}
        O["是：再验证指定 block 持续增长且 leakage=o(spike)"]
        P["否：证明在此停止；teacher tree 不推出 learned coordinates"]
        K --> L --> N
        N -- "待验证" --> O
        N -- "失败" --> P
    end
    O -. "条件满足后接入 writer 证明" .-> D
~~~

## 5. 唯一下一决策

审批 [A14-PU-01 Protocol](NTP_hierarchical_low_rank_parameter_update_theory_package/03_实验协议.md) 的 M0/M1 范围：用 shared/disjoint-tree × full-position/root-only 比较，同时测量 activation implementation、mapping exposure、gradient coherence、$\tau_{q_0}(\Delta W_T)$、task-spike/Gaussian-bulk ratios、$\tau_{q_0}(W_T)$ 和 frozen low-rank replay。

**完成判据：**M0 精确复现定理；M1 至少 4/5 seeds 同时通过 capability、activation、coherence、update-tail、complete-weight-tail 与 functional gates。若只出现低秩 update 或 task outlier，则分别停在较弱结论，不升级为完整 $W_T$ 低有效秩。
