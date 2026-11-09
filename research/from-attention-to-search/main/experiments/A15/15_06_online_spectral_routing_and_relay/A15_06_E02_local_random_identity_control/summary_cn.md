---
experiment_id: A15_06_E02_local_random_identity_control
legacy_experiment_id: A15_00_E02_local_random_identity_control
status: complete
scientific_verdict: fail_no_stable_covariance_identity_advantage
last_updated: 2026-08-05
---

# 最终结果摘要

## 直接结论

本实验**不支持 covariance 排名身份具有稳定训练优势**。Local-HMT 在 seed 17
明确优于运动量匹配的本层随机子空间，但 seed 29 的点估计方向相反且配对区间
跨零，因此没有跨两个 seed 复现。

这不是随机对照更难在线更新造成的：随机目标与 H/M/T 目标的相邻子空间运动在
数值上等距，随机臂的部署投影反而比 H/M/T 更接近各自当前目标，且两者均未出现
\(\gamma=0\) 的停更事件。注册裁定因此为
`fail_no_stable_covariance_identity_advantage`，而不是 insufficient。

## 实验究竟比较什么

- **Local-HMT：**第2、3、4层 Router 分别读取本层 covariance 排名中的
  64维 head、256维 middle、448维 tail。
- **Local-Random-Matched：**保持相同本层来源、维度、嵌套结构、统计刷新、
  子空间运动量和连续性更新器，只用固定正交旋转删除 covariance 排名身份。
- **Centered-Full：**Router 读取去均值后的完整本层表征，用于判断任意动态低维
  约束是否本身有益。

专家在三种条件下始终接收完整表征；变化只发生在 Gate 的观察坐标。

## 10B 决定性结果

NLL 是未见文档的平均 next-token 负对数似然，单位为 nat/token，越低越好。
\(\Delta\mathrm{NLL}(A-B)<0\) 表示 A 更好。每个 seed 在同一 1,024 篇文档上做
2,000 次配对 bootstrap。

| 比较 | Seed 17，95% CI | Seed 29，95% CI | 裁定 |
| --- | ---: | ---: | --- |
| Local-HMT − Local-Random | \(-0.005370\) [\(-0.006858,-0.003969\)] | \(+0.001272\) [\(-0.000265,+0.002925\)] | covariance 身份 **Fail** |
| Local-Random − Centered-Full | \(+0.000266\) [\(-0.001208,+0.001741\)] | \(-0.001832\) [\(-0.003433,-0.000315\)] | 一般动态子空间也未稳定胜出 |

绝对终点 NLL：

| Arm | Seed 17 | Seed 29 |
| --- | ---: | ---: |
| Centered-Full | 3.603843 | 3.602587 |
| Local-HMT | **3.598740** | 3.602027 |
| Local-Random-Matched | 3.604109 | **3.600756** |

![10B 终点配对差](figures/figure2_endpoint_delta_nll.png)

图中横轴是左臂减右臂的逐文档 NLL；负值偏向左臂，横线为95%区间。只有
seed 17 的 HMT 对随机差完整位于零左侧，seed 29 未复现。

## 训练轨迹与跟踪机制

Seed 17 的 HMT 优势约从4B后形成并保持到10B；seed 29 的中期 HMT 优势则在
8B--10B 消失并反转。延长到10B没有把两者收敛成同一方向。

随机旋转将目标的 principal-angle 运动保持到最大误差
\(1.23\times10^{-14}\) radians。10B 时随机臂的 U64/U320 部署—目标重合度接近
1.0，而 HMT 约为0.76/0.87；随机臂 median \(\gamma=0.5\)，HMT 为0.0625。
这说明 covariance 频带对现有 Gate 的路由更敏感，因此连续性守卫允许的更新更小；
它是“更受 Gate 影响”的证据，不是“更有功能价值”的证据。

![完整 NLL 轨迹](figures/figure1_nll_trajectory.png)

![在线跟踪可比性](figures/figure3_tracking_comparability.png)

## 认识更新与边界

1. H/M/T 排名身份没有获得跨 seed 的预测质量证书。
2. Seed 17 的收益是真实的逐文档差异，但属于 seed-conditioned 现象，不能升级为
   一般方法结论。
3. 任意动态低维本层子空间也没有稳定优于完整去均值 Router，因此当前结果不支持
   “低维动态约束本身普遍有益”。
4. 相同几何运动下，H/M/T 更强地扰动当前路由，和 Gate 偏向高方差方向的既有
   认识一致；但敏感度不等于专家效用。
5. 本实验不证明 covariance 方向没有信息，也不证明 Fisher/功能方向无效；它只
   关闭固定 covariance 排名作为功能坐标的当前证据缺口。

唯一下一决策是：不再扩大固定 H/M/T Router，转而先验证由专家相对效用定义的
区分性方向，是否在 held-out 数据上增量预测 expert choice regret 或共同训练兼容性。
