# Protocol CN: A06_01_05_E01 warmup 谱方向 router 重初始化

## 0. 审核快照

目的：在 no-position uniform slot 数据集上，测试短 warmup 后 all-position hidden-state 聚类或 expert top singular direction 是否能作为 router 重初始化来源。

主 anchor：`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

决策问题：训练 0/10/40 步后，全位置 hidden geometry 或 expert 参数谱方向是否足够 feature-aware，可以让四个均匀 features 分到四个 experts？

主指标：balanced route-position eval 上的 feature NMI。

关键 guard：matched preserve fraction、margin p05、max load、target accuracy、slot-start NMI。

运行设置：seeds 0--7，slot length 1/2/4/8，warmup 0/10/40，post-reinit checkpoints 0/10/40/80/160，本地两卡 full run。

条件：

- all-position centered k-means；
- route-position centered k-means；
- oracle centered feature centers；
- raw expert SVD rows；
- common-projected expert SVD rows；
- orthogonalized expert SVD rows；
- no-reinit warmup control。

通过：某个 warmup all-position 或 expert SVD 条件接近 route-position clustering，margin p05 为正，slot-start NMI 低。

失败：warmup 后 all-position 和 expert SVD 仍明显低于 route-position / oracle。

不足：route/oracle positive controls 失败、target accuracy 失败、slot-start NMI 高、或 full coverage 不完整。

不能 claim：real DCLM、语义专家、可部署 MPI router、spectral routing 不可能。
