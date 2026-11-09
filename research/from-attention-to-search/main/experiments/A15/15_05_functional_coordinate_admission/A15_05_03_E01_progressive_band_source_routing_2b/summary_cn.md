---
experiment_id: A15_05_03_E01_progressive_band_source_routing_2b
status: completed_specialization_only_without_quality_pass
completed: 2026-08-02
canonical: summary.md
---

# 摘要：逐层频带来源的 2B 匹配训练

## 结论

显式构造频带 Router **能够迫使路由和部分专家功能发生变化**，但没有证明
“之前没有层级分化，只是因为模型没有按频带分发”。

- `local-HMT` 让第 2/3/4 层分别只看本层 head/middle/tail，最终平均比
  native **差 0.002174 nat/token**，95% CI 为
  \([0.001758,0.002590]\)。
- `layer1-relay-HMT` 让后三层分别读取第一层输出的 head/middle/tail，2B
  终点平均比 native **好 0.001756 nat/token**，95% CI 为
  \([-0.002352,-0.001119]\)，两个 continuation replicas 方向一致。
- 但是 relay 在刚分叉时损失显著升高，整个 0.629B--2B 续训区间的平均
  held-out NLL AUC 比 native **差 0.02135 nat/token**；它是后期恢复并略微
  反超，不是训练效率提高。
- relay 在两个 replicas 中都降低了 forced-expert route regret，说明它最终
  选择的专家更接近反事实最优专家；但专家效用离散度同时下降、专家输出更
  相似，其他冲突指标也不一致，因此没有形成一条一致的“专家更分工”证据链。

正式裁定：**Specialization-only without quality pass**。更准确的人话是：
显式频带结构改变了学习路径并留下部分功能差异，但没有改善全程 loss/FLOP，
也没有证明 H→M→T 是有益的层级分工。

## 指标先解释

- **Held-out NLL** 是模型预测未见 token 时的平均意外程度，单位为
  nat/token，越低越好。
- **NLL AUC** 是从公共分叉到 2B 之间整条 held-out 损失曲线的平均高度；
  越低表示用同样累计计算更快达到好模型，而不只是终点偶然更好。
- **路由分歧率** 是同一 token 相对 native 换专家的比例；它只证明干预生效。
- **Forced-expert route regret** 是实际 Router 选择专家的损失，相对把同一
  token 强制送给八个专家中最佳者多出的损失；越低表示选专家更接近当前
  反事实最优，但不能单独证明专家更专业或最终模型更好。

## 三组比较

| 比较 | 2B paired \(\Delta\) NLL | 全程 AUC 差 | 直接判断 |
| --- | ---: | ---: | --- |
| local − native | +0.002174 \([0.001758,0.002590]\) | +0.02298 | 同层 H→M→T 更差 |
| relay − native | −0.001756 \([-0.002352,-0.001119]\) | +0.02135 | 终点略好，但训练效率更差 |
| relay − local | −0.003930 \([-0.004504,-0.003343]\) | −0.00163 | 固定浅层 source 优于本层 source |

正的 NLL/AUC 差表示更差。终点区间来自 1,024 个配对 DCLM 文档和两个等权
replicas；replica 不是由文档数扩增出来的伪种子。

![匹配计算下的 held-out NLL 轨迹](figures/figure1_heldout_nll_vs_flops.png)

图中横轴是解析匹配的累计训练 FLOPs，纵轴是 held-out DCLM NLL。两种处理
从公共 0.629B 分叉点立即换用频带视图，因此最左侧的高损失是结构适应代价；
relay 到 1.5B 附近才追平并在 2B 略微反超。曲线整体面积仍高于 native。

![2B 终点的配对 NLL 差](figures/figure2_final_paired_nll.png)

纵轴为左侧模型减右侧模型的 NLL；负值更好。relay 的两个 replicas 及等权
汇总均低于零，local 则没有稳定收益。这张图只证明 2B 终点排序，不证明更高
训练效率。

## 操作与功能证据

- 第 2--4 层平均路由分歧率：local 为 **7.12%**，relay 为 **19.70%**；
  relay 的第 4 层约 34%。干预不是 no-op。
- 四个注册里程碑的最差归一化负载熵为 **0.974**，最大专家份额为
  **17.9%**；六条训练均无 dead expert、无 capacity drop，数据哈希完全配对。
- 两 replicas 平均 route regret：native/local/relay 为
  **0.42485/0.42304/0.41726 nat/token**，relay 同向更低。
- local 的负梯度对比例和输出冗余在两 replicas 中都略低，但 NLL 更差；
  relay 的输出冗余反而更高，说明“某个功能指标变好”不等于形成一致专业化。

![路由操作与负载护栏](figures/figure3_route_and_load_guards.png)

![专家功能机制指标](figures/figure4_expert_function_mechanisms.png)

## 客观判断与边界

这个实验支持一个窄结论：**缺少显式频带约束，确实会让我们看不到由该约束
强制产生的路由与功能变化；但这不是先前缺少有益层级分化的充分原因。**
显式 H→M→T 可以被模型适应，固定第一层 source 甚至有微弱晚期终点优势，
但它没有抵消早期代价，也没有形成一致的专家专业化画像。

不能声称：H→M→T 是正确语义层级、covariance rank 优于任意同维瓶颈、
第一层包含后三层所需全部信息、从初始化训练也会得到同样结果，或该方法提高
了训练效率。本实验没有同维随机日程 arm，因此终点 relay 优势不能唯一归因于
covariance 频带身份。

**下一决策：** 关闭“固定 H→M→T 频带日程本身就是功能路由原则”的候选；
若继续跨层路由，先要求可学习的浅层条件在 held-out 专家效用/兼容性上超过
同维随机与错误层，再进入匹配训练。

完整设置、运行记录和图像合同见 [detailed.md](detailed.md)。
