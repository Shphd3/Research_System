# 05/06 Anchor One-Page Logic Map

## 1. 先定结论

当前主线不是“减 common 后解决了”，而是：

```text
real-DCLM proxy geometry 存在；
raw-center equal-norm 能做出很强 step0 routing；
但普通 DCLM training 会在 step5/10 把这个 routing 覆盖掉。
```

下一步应做 preservation / anti-feedback，不应直接做 utility binding。

## 2. 三个名词

`raw-center equal-norm`：直接用原始 hidden state $h$ 的 cluster center 初始化 router row，并把所有 row 调成同样长度。它是当前真实 raw-input router 的主条件。

`residual-center`：先减 common mean $c$，得到 $r=h-c$，再用 residual 的 cluster center 初始化 router。它主要是诊断 residual 里有没有结构。

`common bias`：真实 router 看 $h$，打分是 $w^\top h=w^\top c+w^\top r$。即使 $w^\top r$ 能分 proxy，$w^\top c$ 也可能让某些 expert 对所有 token 都有共享优势，从而压低 residual-center 的 raw-input routing。

所以：residual-center 在 centered-input 诊断里好，不等于真实 raw-input router 好。

## 3. 我们做过什么、没做什么

做过：

| Stage | 结论 |
| --- | --- |
| A06_10 proxy discovery | real hidden states 有稳定 proxy；raw 和 residual k-means 几乎一样，减 common 不是发现 proxy 的关键原因。 |
| A06_11 router bridge | raw-center equal-norm 是最强 raw-input 初始化；residual-center 主要在 centered-input 诊断中强。 |
| A06_12/A06_13 training | 普通 DCLM training 不保持 proxy routing；失败点是 training feedback override。 |

没做完：

```text
训练时持续让 router 使用 h - running_mean / calibration_mean，
并检查 step5/10/50 的 proxy_route_NMI 和 LM loss。
```

因此不能 claim “减均值能让普通 DCLM 保持特征分类”。

## 4. 05 与 06 的分工

| Line | 父问题 | 更新了什么 |
| --- | --- | --- |
| 05 | ordinary top-1 为什么坏？ | common、early lock-in、common-logit feedback 是核心失败机制；inhibition/center separation 不能直接当解决方案。 |
| 06 | 能否构造真实 proxy gating initialization 并保持？ | proxy 存在，linear bridge 成功，但 ordinary training preservation 失败。 |

一句话：

```text
05 解释为什么会坏；
06 定位哪一步已经能做、真正卡在哪里。
```

## 5. 01-04 与后续是否重复

不重复，关系如下：

| Anchor | 和后续关系 | 处理 |
| --- | --- | --- |
| 01 | 父定义：feature identity、non-collapse、utility boundary | 保留 |
| 02 | early lock-in 机制，被 05/06 继承 | 保留为支持证据 |
| 03 | synthetic/hierarchical utility binding；和 06_14 概念相关，但依赖不同 | parked，暂不合并 |
| 04 | Zipf/frequency write-in 分支；不是 real-proxy 分支的替代 | parked，暂不合并 |

真正的结构整理：05 anchors 已迁入 `problem_anchors/05_failure_mechanism/`，06 anchors 已迁入 `problem_anchors/06_geometry_proxy_preservation/`；`problem_anchors/README.md` 作为总入口，两个子文件夹里的 `research_map.md` 作为可继续更新的研究线地图。
