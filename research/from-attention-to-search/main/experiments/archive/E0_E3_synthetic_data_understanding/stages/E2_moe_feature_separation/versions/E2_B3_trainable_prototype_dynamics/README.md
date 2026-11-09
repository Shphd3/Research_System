# E2-B3 Trainable Prototype Dynamics

本实验修正 E2-B / E2-B2 的关键可信度问题：旧 prototype top-1 routing 使用 hard `argmax` 选择 expert，但没有用 gate probability 加权 expert output，因此自然 NTP loss 不能反传到 router/prototype centers。

E2-B3 改为 gate-value top-1：

$$
y_t = p_{t,e^*} \cdot \mathrm{Expert}_{e^*}(h_t),
\quad
e^*=\arg\max_e p_{t,e}
$$

这样 NTP loss 能通过 $p_{t,e^*}$ 更新 prototype centers $c_e$。本轮只跑 3 seeds，用来判断 trainable centers 在真实梯度动力学下是否自然形成 one-feature-one-expert。

Read:

- `purpose_card.md`
- `execution_plan.md`
- `summary.md`
- `detailed.md`
