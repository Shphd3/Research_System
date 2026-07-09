# 06 研究线：proxy discovery、router initialization 与 preservation

## 裁定

06 线把“形成 feature-level expert partition”拆成阶段合同：

```text
feature/proxy 是否存在
-> proxy 是否能转成 router rows
-> routing 是否能被 training preservation 保持
```

当前结论是：

```text
controlled route-position geometry 可发现、可路由、可保持；
controlled center initialization 的保持来自有限厚度的 positive margin buffer，
而不是 active tracking；
real-DCLM proxy clusters 可发现且 step 0 可线性路由；
但 ordinary real-DCLM training 会在 step 5/10 覆盖 proxy routing；
A06_22 已复现这个真实崩塌，但 common/residual dominance 随 common
projector 翻转，所以 common 是候选机制，不是已闭合根因。
```

2026-06-25 local two-GPU full02 复现：

```text
A06_10 real-DCLM proxy discovery: completed, 96 proxy rows + 72 hidden rows
A06_11 proxy-center router bridge: completed, 264 router rows + 48 hidden rows
A06_12 proxy-init preservation: completed, 12/12 tasks + 288 trajectory rows
```

复现结论没有改变主线判断：

```text
A06_10 step-10 raw/residual proxy stability NMI = 0.5211
A06_11 step-10 raw-center proxy_route_NMI = 0.8811
A06_12 raw-center proxy_route_NMI: 0.7549 at step 0 -> 0.0410 at step 5 -> 0.0131 at step 10
```

解释：

```text
proxy 存在，step-0 router bridge 存在；
当前失败点仍是 preservation：ordinary training 覆盖 proxy routing。
```

## 阶段证据

### 1. Controlled route-position geometry

A06_16/A06_17 说明：在 corrected no-position bridge 中，route-position
hidden states 有干净 feature geometry。

关键判断：

```text
route-only / slot offset 3: feature_NMI = 1.0, 8/8 seeds pass
all-position: mean feature_NMI = 0.797, only 1/8 strict pass
```

解释：

```text
all-position clustering 的失败不是 feature geometry 不存在，而是把非路由状态
混进了拟合样本池。真正需要的是 route-relevant state selector。
```

A06_18 revision 进一步测试了 PCA latent clustering、bottleneck AE latent
clustering、SAE-code clustering：

```text
route-only / slot offset 3: feature_NMI = 1.0, 8/8 seeds pass
raw all-position: mean feature_NMI = 0.831, 2/8 strict pass
best revision selector: PCA q=4 mean feature_NMI = 0.871, 2/8 strict pass
SAE L1 8x reconstruction MSE = 0.0034, but feature_NMI = 0.729
```

判断：

```text
generic representation learning 不能替代 route-relevant selector；
reconstruction quality 不是 route-readout quality；
下一版 selector 必须显式加入 route-local 或 route-readout constraint。
```

### 1.5 Controlled margin preservation mechanism

A06_17_02 到 A06_17_05 说明：在 corrected no-position bridge 中，center
initialization 的保持不是因为 router rows 主动追踪 feature centers，而是
因为初始化给出了正间隔安全区。

关键判断：

```text
A06_17_02: pseudo/oracle center final feature_NMI = 1.0, but movement alignment < 0
A06_17_03: worst boundary consumption < 0.70, dynamic switch rate = 0.000
A06_17_04: forced crossing breaks the matched region
A06_17_05: perturbations through rho=0.70 preserve, pure random fails
```

解释：

```text
positive margin is a geometric safety region in this controlled bridge;
good initialization is not a guarantee forever, but it can place the system
inside a margin basin that the tested training trajectory does not exhaust.
```

当前新增疑问：

```text
这个 positive margin 是 feature residual margin，还是 high-gain common-band
margin？如果主要来自 common band，它只能说明 routing 稳定，不能说明
feature-specific specialization 可信。
```

A06_21 已完成 full margin-budget audit：

```text
full run: 8 seeds x C0-C3 x 5 conditions x 12 checkpoints
decomposition identity max error = 1.37e-6
pseudo/oracle center at step 10: feature_NMI = 1.0, sign flip = 0,
positive min margin > 5.6, positive cluster-aware margin > 4.5
random/equal-norm random: negative min margin and sign flip about 0.23
label-shuffled center: NMI can be moderate, but matched preserve fraction is low
```

解释：

```text
controlled bridge 中，真正保持的是正 current margin / cluster-aware margin，
不是 NMI alone；
center-init 的负向 margin pressure 主要来自 feature-center drift，
但初始 margin buffer 足够大，所以没有跨 expert boundary；
common share 在 center-init 条件中很低，因此 common overwrite 不是这个
controlled preservation 的解释。
```

A06_23 进一步完成 margin threshold audit：

```text
row-gap scaling: w'_e = mean(w) + q(w_e - mean(w))
q>0 时 step-0 assignment 不变，initial margin 按 q 成比例缩小
q>=0.05: final matched preserve = 1.000, sign flip = 0
q=0.02: final matched preserve = 0.375, sign flip = 0.159,
        final current margin = -0.588
q=0 guard / crossed guard: 原始 feature-to-expert identity 失败
```

解释：

```text
controlled bridge 中 positive margin 不是二值保险；
它必须足够厚，才能扛过 early training 的 router/feature drift。
NMI alone 不能作为 preservation 主指标，因为 q=0.02 和 crossed guard
仍可能有较高 feature NMI，但已经丢失原始 feature-to-expert 映射。
```

### 2. Real-DCLM proxy discovery

A06_10 支持真实 DCLM hidden states 中存在稳定 proxy clusters。

关键边界：

```text
proxy stability 高于 random、frequency 和 position nuisance；
但 proxy cluster 不是语义 feature 证明，也不是 expert specialization 证明。
```

### 3. Step-0 router bridge

A06_11 支持 proxy centers 能转成 linear top-1 router rows。

关键边界：

```text
raw-center raw-input 是当前最强 actual bridge；
residual-center centered-input 是诊断，不是直接可部署 raw router。
```

### 4. Training preservation

A06_12 是当前 bottleneck：

```text
raw-center step-0 proxy_route_NMI = 0.7549
step 5 NMI = 0.0410
step 10 NMI = 0.0131
LM loss 与 random 接近
```

解释：

```text
这不是 proxy discovery failure，也不是 step-0 linear bridge failure；
它是 ordinary next-token training 覆盖了 proxy routing。
```

### 5. Common/residual trajectory bottleneck

A06_22 对 A06_12-style real-DCLM collapse 做了 router-gap common/residual
trajectory audit。

关键结果：

```text
raw-center proxy_route_NMI: 0.7549 at step 0 -> 0.0410 at step 5 -> 0.0131 at step 10
LM loss 与 random 接近，所以不是 training crash
mean-common projector: Lambda_upd@5 = 2.1507, Lambda_upd@10 = 1.9856
top hidden-PC projector: Lambda_upd@5 = 0.7089, Lambda_upd@10 = 0.6666
router-row subspace projector: Lambda_upd@5 = 0.4611, Lambda_upd@10 = 0.4332
```

解释：

```text
真实 collapse 存在；
mean-common 下 common update 看起来主导 margin movement；
但 top hidden-PC 和 router-row subspace 下 residual update 反而更大。
因此当前不能 claim common-dominated router update 是 projector-robust root cause。
```

这更新了 06 线下一步：

```text
不要直接做 common-subtraction method；
先定义更物理、更贴近 nested learning / training objective 的 common operator；
然后再比较 raw h 与 (I-P_C)h 的 routing 是否改善 rare-feature margin。
```

## 合成到真实的边界

controlled synthetic / bridge 能证明：

- route-position feature geometry 是可达对象；
- all-position sample pool 不合法；
- 在可控目标下 pseudo initialization 可以被保持。

real-DCLM proxy 能证明：

- 真实语料 hidden states 中有可重复 proxy；
- step-0 gate 可以对 proxy routing；
- ordinary training 会覆盖这个 routing。

两者之间仍缺少：

```text
label-free route-relevant state selector for real text；
stable common operator tied to training objective or nested-learning geometry；
common-subtracted routing audit: raw h vs (I-P_C)h；
anti-feedback / preservation objective；
proxy partition 的 expert utility 证据。
```

相关支持线：

```text
A11 long-horizon MTP objective 说明，在受控构造中，覆盖第一个包含早期变量
的未来目标可以直接迫使当前 hidden state 写入该变量。它还没有证明 MoE
preservation。A11_05 进一步支持：在 clean tau=3 all-position 训练中，
decision-prefix 上的 horizon-3 直接监督是更快、更稳定恢复变量的一个机制
成分，但 all-position 间接迁移仍然存在。A11_06 / A11_07 进一步支持：
direct horizon-3 监督给出正的 hidden readout-margin velocity、更强 native
H3 和 M_Z_ref；同时也确认 Q alone 不能证明 direct supervision。它为后续
“objective-level route-relevant state formation”提供了一个可建模入口，但
桥接 MoE 时必须另测 route margin / sign flip。
```

## 下一步

优先写 nested-learning-inspired common/rare routing audit，不要直接设计
utility method 或 common-subtraction method。

最小问题：

```text
能否定义一个稳定 common operator P_C，使得 routing on (I-P_C)h 相比
raw h 提高 rare-feature margin、降低 sign flip，并且不恶化 LM loss？
```

若结论仍随 common projector 翻转，则说明 common definition 仍是建模瓶颈；
不能进入方法 claim。

## Source Links

```text
Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/
Projects/from-attention-to-search/main/experiments/A06/A06_10_real_dclm_proxy_feature_operationalization/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_11_real_dclm_proxy_center_router_initialization/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_12_real_dclm_proxy_init_training_preservation/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_real_dclm_full02_rerun_report.md
Projects/from-attention-to-search/main/experiments/A06/A06_17_all_position_route_relevant_feature_discovery/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_17_02_router_center_tracking_preservation/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_17_03_feature_drift_margin_boundary/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_17_04_margin_crossing_causal_stress/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_17_05_margin_basin_robust_initialization/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_18_label_free_route_relevant_state_selector/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_20_route_logit_common_estimator_random_init_feature_recovery/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_21_margin_budget_preservation_audit/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_22_router_common_residual_trajectory_audit/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_23_top1_lockin_margin_threshold/summary.md
Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/README.md
Projects/from-attention-to-search/main/stories/11_long_horizon_mtp_objective/story_cn.md
Projects/from-attention-to-search/main/experiments/A11/A11_04_03_k3_efficiency_advantage/summary.md
Projects/from-attention-to-search/main/experiments/A11/A11_05_semantic_efficiency_bridge/summary.md
Projects/from-attention-to-search/main/experiments/A11/A11_06_readout_effective_margin_efficiency/summary.md
Projects/from-attention-to-search/main/experiments/A11/A11_07_no_leakage_all_position_efficiency/summary.md
daily_research_reports/0629/docs/nested_prediction_spectral_anisotropy_causal_rewrite_v4.md
daily_research_reports/0701/meeting_brief.md
```
