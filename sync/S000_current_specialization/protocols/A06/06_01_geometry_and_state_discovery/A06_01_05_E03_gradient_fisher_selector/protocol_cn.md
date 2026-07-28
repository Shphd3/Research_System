# Protocol CN: A06_01_05_E03 梯度/Fisher 路由状态选择

## 最小审核信息

目的：检验在不使用 feature 标签的情况下，梯度或 Fisher 类信号能否从
all-position hidden states 中选出 route-relevant states，并用于初始化
router。

数据：沿用 A06_01_05_E01/A06_01_05_E02 的均匀 feature、无位置编码、slot synthetic
数据。4 个 feature 等频，slot start 平衡，route position 是重复 feature
slot 的最后一个 token。

模型：一层 causal self-attention + 一层 weighted top-1 MoE + LM head。

核心比较：

- `allpos_centered`：所有位置聚类，失败基线；
- `route_centered`：只用 route 位置聚类，正控制；
- `oracle_centered`：用 feature 标签中心，上界；
- `grad_h_*`：用 post-hidden 梯度做选择、加权或方向聚类；
- `grad_emb_*`：用 embedding 梯度做选择、加权或方向聚类；
- `fisher_*`：用梯度协方差方向定义 loss-sensitive 几何。

第一指标：初始化后的 feature NMI。

保护指标：margin p05、训练后 preserve fraction、slot-start NMI、selected
route/slot/target fraction。

通过：某个梯度/Fisher 方法明显超过 all-position，接近 route-position
control，并且 margin p05 为正。

失败：只提升 feature NMI 但 margin p05 仍为负，或者不超过 all-position。

边界：只支持 synthetic uniform no-position bridge；不能推出 real-DCLM、
semantic experts、common/rare routing 或 expert utility。
