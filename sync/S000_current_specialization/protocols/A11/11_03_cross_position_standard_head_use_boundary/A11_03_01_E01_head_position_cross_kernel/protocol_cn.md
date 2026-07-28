# A11_03_01_E01 Head × 位置交叉核实验协议

完全复用 A11_17 的五条 NTP 轨迹和 seen 诊断 batch，只测：

$$
H2@h_T,\quad H1@h_T,\quad H2@h_{T+1},\quad H1@h_{T+1}.
$$

统一指标为：

$$
\widehat U_{a,p}
=-\frac{\langle\nabla M_{a,p},g_D^S\rangle}
{\|\nabla M_{a,p}\|\|g_D^S\|}.
$$

主判据是 burn-in 后 `20-200` AUC。`H1@hT` 只测换 head，`H2@hT+1` 只测换位置，`H1@hT+1` 是真实组合接口。中心差分、恢复、平衡和曲线复现先通过，再判定 head、位置或交互瓶颈。
