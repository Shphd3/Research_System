# A11_19 Bridge Token 条件化位置传递实验协议

完全固定 A11_18 的 NTP 轨迹、seen 样本、H2 梯度、H1 head 和一步位置，只在诊断时替换 bridge：

```text
Decision / Answer / Therefore / :
```

测每个 bridge 的：

$$
\widehat U_b
=-\frac{\langle\nabla M_{1,T+1}^{(b)},g_D^S\rangle}
{\|\nabla M_{1,T+1}^{(b)}\|\|g_D^S\|}.
$$

主判据为 `20-200` AUC。四项都至多 `1/5` 正则位置瓶颈稳健；某个替代 bridge 至少 `4/5` 正则说明 token-dependent。替代 token 不参与训练，因此不能当作新方法结果。
