# Experiment Pack: RoundA Coarse (domain5x50, K-Medoids, L2)

## 1) 实验配置与执行内容

- 数据集：Web of Science
- 采样策略：`coarse_grained_profile=domain5x50`（样本数最多的 5 个 domain，每类 50 条，共 250 条）
- 层：`4, 12, 20, last`
- 表征：
  - `raw_x_raw`
  - `first_order_raw`
  - `first_order_pca`
  - `second_order_raw`
  - `second_order_pca`
  - `subspace_first_pca`
  - `subspace_second_pca`
  - `energy_first_pca`
- PCA 维度：`r in {32,64,128,256}`
- 聚类：`K-Medoids`
- 距离：`L2`
- 指标：`Silhouette / NMI / ARI / PMA`

取去均值后的表征的前r个特征子空间，然后进行语义聚类，查看聚类的准确率。
  设中心化特征为：
  $$x_c = x - \mu$$
  设一阶 PCA 投影为 $$P_r$$，二阶 PCA 投影为 $$Q_r$$，其中 $$r\in\{32,64,128,256\}$$（也可自定义）。
  - first_order_raw
    $$z = x_c$$
  - first_order_pca
    $$z = P_r x_c$$
  - second_order_raw
    $$z = x_c \odot x_c$$
  - second_order_pca
    $$z = Q_r (x_c \odot x_c)$$
  - subspace_first_pca（与 first_order_pca 同定义）
    $$z = P_r x_c$$
  - subspace_second_pca
    $$z = (P_r x_c)\odot(P_r x_c)$$
  - energy_first_pca
    $$z = \|P_r x_c\|_2$$



结果根目录：`/data/250010109/spectral_router/exp_quadratic_semantics/output/roundA/coarse_domain5x50_kmedoids_l2`

---

## 2) 关键结果总览

### 2.1 按“全组合平均值”统计（层 × r）

| Representation | Silhouette↑ | NMI↑ | ARI↑ | PMA↑ |
| --- | ---:| ---:| ---:| ---:|
| raw_x_raw | 0.0234 | **0.3114** | **0.2230** | **0.4670** |
| first_order_raw | 0.0234 | **0.3114** | **0.2230** | **0.4670** |
| first_order_pca | 0.0014 | 0.0669 | 0.0256 | 0.2975 |
| second_order_raw | -0.0349 | 0.0465 | 0.0011 | 0.2245 |
| second_order_pca | 0.0120 | 0.0428 | 0.0066 | 0.2588 |
| subspace_first_pca | 0.0014 | 0.0669 | 0.0256 | 0.2975 |
| subspace_second_pca | 0.0367 | 0.0399 | 0.0080 | 0.2573 |
| energy_first_pca | **0.5005** | 0.0277 | 0.0052 | 0.2712 |

### 2.2 你关注的问题：为什么 energy_first 看起来“分得很开”

- `energy_first_pca` 的输入是 1 维标量：`||P_r x_c||_2`，K-Medoids 在 1 维上容易形成间隔明显的簇，因此 **Silhouette 很高**。
- 但它只保留“能量大小”，丢掉方向与细粒度结构，因此与真实语义标签对齐能力弱，表现为 **NMI/ARI/PMA 明显低于 raw_x_raw/first_order_raw**。
- 结论：energy_first 更像“半径分段”而不是“语义分群”。

---

## 3) 分层观察（简述）

- `raw_x_raw / first_order_raw` 在各层的 NMI/ARI/PMA 一直最强，说明在 coarse 设定下，原始向量信息最直接地保留了类别结构。
- `first_order_pca / subspace_first_pca` 一致（定义相同），说明降维后有一定信息损失，但仍优于二阶系列的多数配置。
- `second_order_*` 与 `subspace_second_pca` 在 coarse 任务上没有体现出稳定优势。

---

## 4) 可视化与索引

- 汇总 JSON：`rank_layer_by_rep/rank_layer_by_rep_summary.json`
- 图：
  - `rank_layer_by_rep/rank_layer_by_rep_silhouette.png`
  - `rank_layer_by_rep/rank_layer_by_rep_nmi.png`
  - `rank_layer_by_rep/rank_layer_by_rep_ari.png`
  - `rank_layer_by_rep/rank_layer_by_rep_pma.png`

---

## Experiment -> Theory Card

- What was actually run:
  - Web of Science coarse 设定（Top-5 domain，每类 50 条）
  - 层：4/12/20/last
  - r：32/64/128/256
  - 表征：raw_x/raw_xc/first_pca/second_raw/second_pca/subspace_first/subspace_second/energy_first
  - 聚类：K-Medoids + L2
  - 指标：Silhouette + NMI + ARI + PMA

- Key findings:
  - 语义对齐指标（NMI/ARI/PMA）最优是 `raw_x_raw` 与 `first_order_raw`
  - `energy_first_pca` 的 Silhouette 显著最高，但 NMI/ARI/PMA 偏低
  - 二阶表征在该 coarse 任务中未显示稳定主导优势

- Reliability grade:
  - **B-（中等可信）**
  - 原因：多层、多 r、多指标一致性较好；但样本规模（250）偏小，且聚类随机种子次数有限

- Theory-implementation mismatch:
  - 目标若是“语义分群”，仅看 Silhouette 会误判 `energy_first_pca`
  - 需要把 PMA/NMI/ARI 作为主指标，Silhouette 作为几何辅助指标

- support / falsify / unclear:
  - 对“二阶整体优于一阶”的主张：**unclear / 偏不支持**
  - 对“energy 可把点分开”的主张：**support（几何层面）**
  - 对“energy 代表语义分群”的主张：**falsify（在当前 coarse 设定）**

- What should be written back to checkpoint:
  - 记录一条实验注记：`energy_first` 仅作几何分层信号，不能单独作为语义聚类质量结论依据
  - 在后续 checkpoint 比较中，把 PMA/NMI/ARI 设为主判据，Silhouette 设为辅助判据

- Immediate next action:
  - 运行同构配置的 `kmedoids + cosine` 与当前 L2 做并排结论表（已可直接读取）
  - 增加 fine 设定（如 25×10）复验 `raw_x` 与 `first_pca` 的稳定性
  - 对 energy 分支增加“与方向信息联用”的变体，而非单独 1 维能量聚类
