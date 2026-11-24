# 1119_hd4_fr：从第一步学习频率层级路由，撤教师后能否保住收益？

活跃问题 #2：特征层级与 expert 分发。执行侧：[HD4-FR](/data/250010109/MoE_Router/experiments/1119_hd4_fr/run-notes.md)。

## 1119 02:37　提交 50B 主训练

- 假设：在不改变 HD4-T 的激活专家宽度时，频率分组与可学习条件路由能保住早期学习优势，并在撤去教师后维持收益。
- 先验→模型→计算：高低频 feature 有不同分工 → 对共同骨架学习整条条件路径，真实选择来自学生，教师只提供有盖度位置的叶分布 → 同 token、同 EVAL，对比整体及两类互不替代的频段。
- 跑前预测：早期差距收敛且撤教师后维持改善 → 再拆分频率分组和软蒸馏；有足量训练仍无改善 → 查选路可读性、路由负载和覆盖；评估点不匹配或未抵达阶段 → 保留未知。
- 竞争解释：频率分档得到的标签与早期学生可读信息不匹配，或高频负载占主导，低频收益只是桶内表面现象。
- 结果：ACP 作业 `pt-gk03iqt6` 已接受，原账户单节点 H100 4 卡 Reserved。[作业回执](/data/250010109/MoE_Router/experiments/1119_hd4_fr/acp/1119-hd4-fr-50b-reserved.json) · [状态](/data/250010109/MoE_Router/experiments/1119_hd4_fr/acp/status.json)。未用科研指标作为正式开跑门槛。
- 资产：`dclm_pair_v1`、`checkpoint_moe_baseline_dense_aligned_initial_20261030`、`sae_qwen3_0p6b_e16_layer27_final_1b`、`dataset_teacher_routing_dev_eval_20261109`、`representation_e16_train_replay_1115_20261119_index`、`routing_hd4_fr_train_frequency_tree_20261119`、`analysis_hd4_fr_historical_eval_alignment_20261119`。
- 研究者决定：Unknown（科研判定）。
- 链条位置：routing·架构含义 → loss·训练效果。

今日认识更新：主作业已提交；已有同 token 全量基线读数到 524,288,000 targets，不能用近邻检查点替代严格配对。

## 1119 02:53　保留四卡预算改排双节点

- 假设／先验／跑前预测：沿用上条，改动的是资源放置。
- 结果：单节点 `pt-gk03iqt6` 未获主机，0 步；确认 `SUSPENDED` 后，同账户另排 `pt-170s8viu`（2 节点 × 2 H100 Reserved），不并发申请。正式 NCCL 通信必须核验 IB/GDRDMA，工程检查不含科学门槛。[作业回执](/data/250010109/MoE_Router/experiments/1119_hd4_fr/acp/1119-hd4-fr-50b-reserved-2x2.json)。
- 研究者决定：Unknown。
- 链条位置：训练执行，未形成科学读数。

## 1119 02:59　四卡开始真实更新并完成首个三方固定 EVAL

- 假设／先验／跑前预测：沿用首条。
- 结果：`pt-170s8viu` 实际 2 台主机各 2 张 H100 80GB。正式 train NCCL 回执显示 32/32 跨节点通道走 IBext_v8/GDRDMA、0 Socket。第 1 步 262,144 有效 targets，训练 LM CE 12.1415 nat；前 8 步有序样本和 mask SHA 与 A0 一致。首个完整恢复存档为 step 5、1,310,720 targets；step 25 存档已写。第 25 步 6,553,600 targets，2,097,152 位置：FR 11.26015、A0 11.23802、HD4-T 11.18872；此点不判断斜率或撤教师效果。[启动实证](/data/250010109/MoE_Router/experiments/1119_hd4_fr/acp/startup_receipt.json) · [对照](/data/250010109/MoE_Router/experiments/1119_hd4_fr/baseline-comparison.json)。
- 资产：`checkpoint_hd4_fr_first_update_boundary_20261119`；首个 checkpoint 完整恢复字段已读取验证，未主动中断来测试恢复。
- 研究者决定：Unknown。
- 链条位置：routing·架构含义 → loss·训练效果。

今日认识更新：HD4-FR 已真实训练。首个同 token 点整体落后，低频词 NLL 接近；低频 SAE 贡献主导仅 1,865 位置，样本数必须单列。当前 hard route 高度偏高频半树，下一步观察一次性校准后分布及 loss 斜率。

## 1119 03:06　校准后检查点与 100 步评估

- 假设／先验／跑前预测：沿用首条。
- 结果：第 58 步起 `lambda0=0.1`、`beta=0.000251797`；第 100 步完整恢复存档同时保存四次梯度探测以及系数。[恢复回执](/data/250010109/MoE_Router/experiments/1119_hd4_fr/train/latest_checkpoint.json)。26,214,400 targets 上三方全量 NLL：A0 8.811331、HD4-T 8.548127、FR 8.815002。FR 与 A0 的差在三个共同点上为 +0.022127、+0.046052、+0.003671 nat；与 HD4-T 为 +0.071429、+0.195776、+0.266875。100 步低频词比 A0 低 0.006678 nat，比 HD4-T 高 0.022721 nat；单种子早期读数，不外推。最新进度由 [监控](/data/250010109/MoE_Router/experiments/1119_hd4_fr/acp/status.json) 持续更新。
- 研究者决定：Unknown。
- 链条位置：routing·架构含义 → loss·训练效果。

今日认识更新：FR 到 100 步总体接近 A0，但没有保住 HD4-T 的同 token 早期领先；不能把系统差异归因给软蒸馏单项。

## 1119 08:55　总体评估曲线快照

- 假设／先验／跑前预测：沿用首条，本条只汇总新读数。
- 结果：HD4-FR 已有 29 个全量 EVAL 点，截至 1,638,400,000 targets 的 NLL 为 3.627325。最近三方严格同 token 点为 524,288,000：A0 4.083143、HD4-T 4.030618、HD4-FR 4.102437。HD4-T 和 FR 最近严格同 token 点为 1,310,720,000：3.629559、3.668792。[图与数据](/data/250010109/MoE_Router/experiments/1119_hd4_fr/analysis/three-model-eval-loss.pdf)，资产 `analysis_hd4_fr_three_model_eval_plot_20261119`。
- 研究者决定：Unknown。
- 链条位置：loss·训练效果。

今日认识更新：FR 的总体 NLL 持续下降；在最近同预算点仍落后于 HD4-T，尚未形成超越 A0 或 HD4-T 的证据。

## 1119　少量 prompt 对照（跑前记录）

- 假设：同一个 token 在不同上下文可能被后四个 block 路由到不同叶子；架构选择满足联合叶概率最大。
- 先验→模型→计算：各 block router 分别读上下文表征 → 同 token ID 不必有相同路径 → 冻结 HD4-FR step 7250，三组同末 token、上下文不同的英文前缀，逐 block 记录左右条件概率、联合概率和专家 ID。另用同前缀、不同追加后缀检查原位置的因果不变性。仅 CPU 前向，不训。
- 跑前预测：同 token ID 若至少一组在某 block 变路，支持该 router 可使用上下文；全未变只说明此小样本无证据。若路径或概率复算不一致，先查实现；少量 prompts 不估容量或普遍语义分工。
- 竞争解释：模型在训练早期可能仍以负载占优的少数叶为默认，或者用局部词面线索而非语义；变路也不证明 SAE 分组机制。
- 资产：`checkpoint_hd4_fr_step7250_prompt_probe_20261119`、`tokenizer_qwen3_0p6b_base_official_a5`。
- 研究者决定：Unknown。
- 链条位置：routing·架构含义（读数）。

## 1119　少量 prompt 对照（结果）

- 假设／先验／跑前预测：沿用上一条。
- 结果：HD4-FR 真实第 7,250 步存档（1,900,544,000 targets），CPU FP32 六条 prompt，无参数更新。三个末词分别为 bank、cell、charge；只在 cell 的显微镜/监狱对照换路，发生在 block 6/7，路径从叶 8 换为叶 12。六条 prompt × 四个 block 的 24 组叶概率与手动相乘及 argmax 全一致。同前缀追加后缀后，前缀所有路由未变，最大 log 概率误差 2.86e-6。[原始读数](/data/250010109/MoE_Router/experiments/1119_hd4_fr/analysis/prompt-probe-07250/result.json)，资产 `analysis_hd4_fr_cpu_prompt_probe_20261119`。
- 研究者决定：Unknown。
- 链条位置：routing·架构含义（读数）。

今日认识更新：能观察到同一个 token 随上下文切换细路径，但此小样本仍集中在高频半树；不据此推出稳定语义分工或输出协方差容量。

- 补充位置对照：固定末 token ID 2779 与 0 基绝对位置 9，显微镜前缀仍为叶 [8,8,12,12]；四个不同监狱前缀均为 [8,8,8,8]。[位置对照](/data/250010109/MoE_Router/experiments/1119_hd4_fr/analysis/prompt-probe-07250/position-control.json)。这排除了末 token 绝对位置不同即可解释此次换路；局部词面与语义解释尚未拆分。

## 1119 09:55　检验 SAE 频率分组是否传到专家的输出谱

- 假设：同层同宽的低频叶，其实际输出的协方差参与率高于高频叶。
- 先验→模型→计算：同组方向的尺度更接近才会让谱变平 → 测量中心化写回协方差参与率 → 固定 FR 7250 步，同量真实路由、打乱路由、同输入遍历各叶，另测 teacher SAE 重构。
- 跑前预测与竞争解释：[测量口径](/data/250010109/MoE_Router/experiments/1119_hd4_fr/analysis/sae-to-output-spectrum/plan.md)；支持则构造谱平整分组；只随路由出现则优先查输入条件；反向则考虑功能方向；支持样本不足时保留未知。
- 结果：待测；资产 、、、。
- 研究者决定：Unknown。
- 链条位置：表征现象 → 机制 → 固定权重干预。

## 1119 10:02　谱的桥梁与固定秩写回原型

- 假设／先验→模型→计算：沿用上条；原型保持实际路径、同秩 32，把每组写回投影到共享或组内方向，再实际计算全词表的预测损失。
- 跑前预测：如正确组内投影能同时改善低频 NLL 和预测 KL，且不恶化高频，下一轮改为可学习低秩写回；如未达门槛，先以预测误差而非输出能量拟合。最强竞争解释是分组方向不同，但其差异不足以影响下一词判断。
- 结果：教师低高频重构参与率 195.56 / 4.22。FR 真实路由的低减高写回参与率，block 4–7 为 −11.28、−20.22、−6.02、+0.56；打乱实际路由作诊断后差值改变。共享 32 与分组 32 的低频 ΔCE 为 +0.05553 / +0.05685，未达门槛。前一条的输入资产 ID 为 checkpoint_hd4_fr_step7250_prompt_probe_20261119、routing_hd4_fr_train_frequency_tree_20261119、dataset_teacher_routing_dev_eval_20261109、sae_qwen3_0p6b_e16_layer27_final_1b；输出资产 analysis_hd4_fr_sae_to_output_spectrum_20261119。[结果与下一版](/data/250010109/MoE_Router/experiments/1119_hd4_fr/analysis/sae-to-output-spectrum/summary.md)。
- 研究者决定：Unknown。
- 链条位置：表征 → 固定权重干预 → 方法含义，训练收益未测。

今日认识更新：频率分组能在教师重构空间制造显著谱差，这个差没有自然传到学生写回；组内方向互换会伤到低频预测，但能量拟合原型未胜共享投影。下一版拟合方向要直接以预测为目标。

## 1119 10:09　预测导向的写回基

- 假设／先验→模型→计算：有用的组内方向应保住下一词相对分数 → 固定活动宽度和路径 → 在 DEV 上按固定候选 KL 各优化 48 步，EVAL 计算全词表 ΔCE 与 KL。
- 竞争解释与分支：相同活跃秩下共享 32 已够，或 32 维组内收益来自多存方向。若同时达到低频 ΔCE 降 0.01 nat、KL 降 10%，且高频不受明显损失，再扩窗并对照同存储；否则保留共享基线。
- 结果：同为学习投影，分组 32 的低频 ΔCE 优于共享 32 约 0.00419 nat，KL 改善 8.5%，未过门槛，也未胜 PCA 共享 32。资产 analysis_hd4_fr_predictive_writeback_20261119。[读数](/data/250010109/MoE_Router/experiments/1119_hd4_fr/analysis/sae-to-output-spectrum/predictive-result.md)。
- 研究者决定：Unknown。
- 链条位置：固定权重介入；训练收益未测。

今日认识更新：有条件的子空间能减少同库错配，但现有固定秩分组和预测拟合都没有显示足够的收益来替换共享方向。

## 1119 10:40　同批次训练损失追踪

- 假设／跑前预测：沿用首条与正式运行口径。本次读取既有训练日志，区分 FR 自己追近 A0 与 HD4-T 的原有领先缩小。
- 先验→模型→计算：若 FR 的相对训练收益扩大，同批次纯 LM NLL 差值应持续向负方向移动。按固定顺序匹配三组整批，排除 A0 两个遮罩步，对同一窗口计算 NLL 及差值，另核对严格同 token 的全量 EVAL。
- 竞争解释与分支：三组绝对 loss 共同下降，或 T 对 A0 的优势收缩，也会让 FR 的曲线看起来在追。若 FR 对 A0 的差值翻转并在留出集复现，才更新对系统收益的判断；若差值维持正值，优先保留基线判断；缺严格匹配点时留空。
- 结果：FR 第 8,302 步，2,176,319,488 有效 targets。最近同批 500 步平均 NLL 为 A0 3.50542、T 3.49739、FR 3.52474。FR 对 A0 的差约 +0.01932 nat，对 T +0.02735 nat。与 0.524–1.049B 相比，FR 对 T 的差缩小约 0.02271，其中约 0.01968 来自 T 对 A0 的领先缩小。相同 1.31072B 的全量 EVAL 中，FR 对 T 总体 +0.03923，低频词 +0.05778，SAE 低频贡献主导桶 −0.17152（1,865 位置）。[计算回执](/data/250010109/MoE_Router/experiments/1119_hd4_fr/analysis/training-loss-comparison/verification.txt)。
- 资产：`analysis_hd4_fr_matched_training_loss_20261119`、`analysis_hd4_fr_historical_eval_alignment_20261119`。
- 研究者决定：Unknown。
- 链条位置：loss·训练效果（单种子趋势跟踪）。

今日认识更新：FR 对 A0 仍稳定落后约 0.02 nat，追近 T 主要来自 T 原有领先衰减；自主路由在低频 SAE 贡献主导小桶中显示局部信号，完整长尾与总体收益仍待共同 EVAL。

## 1119 10:58　诊断低频贡献主导桶的收益

- 假设：低频主导位置的改善来自改变专家分工，并依赖其实际路由。
- 先验→模型→计算：旧树有可能把多个稀有模式合并在同一大流量分支 → 用冻结标签复算桶，查 T 归档路径、用 CPU 复算 FR 的同位置 NLL 与路径 → 同存档固定权重，在同一位置比较自然路径、低侧换叶、高侧换叶。
- 跑前预测与竞争解释：同位置切到高侧应较自然路径及低侧换叶更伤 NLL；若等量损伤，只支持具体路线；若无损伤，优势可能由共享分支或位置难度解释。各阶段的[跑前记录](/data/250010109/MoE_Router/experiments/1119_hd4_fr/analysis/low-sae-dominant/plan.md)。
- 结果：全量 1,865 个位置分布于 704 个 EVAL 序列。T 只用旧叶 2/3。FR 3816 步重放 96 序列 242 位置，实际任一 block 走低侧时对 T 的平均 ΔNLL 为 −0.405，四层均走高侧时为 +0.296。固定 42 个自然四层都走低侧、每序列一个位置，低侧换叶使 NLL 升 1.181，高侧换叶升 2.010，高减低 +0.829 nat，区间 [0.280,1.410]。[详细结果](/data/250010109/MoE_Router/experiments/1119_hd4_fr/analysis/low-sae-dominant/summary.md)。
- 资产：`checkpoint_hd4_fr_step3816_20261119`、`analysis_hd4_fr_low_sae_dominant_path_intervention_20261119`、`analysis_hd4_fr_historical_eval_alignment_20261119`、`dataset_teacher_routing_dev_eval_20261109`。
- 研究者决定：Unknown。
- 链条位置：读数 → 固定权重路由干预 → 架构含义。

今日认识更新：低频侧及具体路径在自然命中子样本上有可测预测贡献。频率分组和蒸馏如何在训练中创造这项收益，需要单因素对照。

## 1119 11:10　频率根划分与软蒸馏消融，及高低频梯度诊断

- 假设：根的频率约束和软目标分别参与低频 SAE 主导桶收益。高频分支可能因过度聚集而造成负梯度干扰。
- 先验→模型→计算：将同骨架的建树规则与教师目标因子正交化，FS/FH/CS/CH 的固定 EVAL 桶不随臂变。读实际派发后同下投影参数的 LM 梯度 Gram、跨序列等量 SNR 和分布集中度。
- 跑前预测与竞争解释：保留单因素差值及交互。不确定项包括路由负载、信号形状与上下文本身。聚集高而冲突相近时不接受简单梯度解释；正式对照未跑则保留未知。[跑前口径](/data/250010109/MoE_Router/experiments/1119_hd4_fr_factorial/plan.md)。
- 结果：共现对照树拟合并通过分组不变量检查，四臂本地 2,048 targets 两步优化成功。主作业 pt-170s8viu 占用预约 4 卡，FH/CS/CH 未正式提交。梯度测量在 FR 3816 步完成，最后 block 一级子专家高/低侧的同频前十原子质量 17.17%/9.20%，负余弦比例 50.61%/50.26%，A0 八专家中位 51.06%；共享 root 低高均值梯度余弦 −0.00132。跨序列有效信号近零，无法排序 SNR。FR 1B 的高侧派发约 98%，前两叶约六成。[运行与证据](/data/250010109/MoE_Router/experiments/1119_hd4_fr_factorial/summary.md)。
- 资产：`analysis_hd4_fr_factorial_and_gradient_readout_20261119`、`checkpoint_hd4_fr_step3816_20261119`、`checkpoint_moe_baseline_1b_routing_probe_20261101`。
- 研究者决定：Unknown。
- 链条位置：表征现象 → 机制读数；因子训练效果待测。

今日认识更新：高侧同档 SAE 激活更集中，但局部测量未见高侧额外的方向冲突。路由占用高度偏斜比“高侧梯度冲突”更有直接证据，仍缺训练因果检验。

## 1119 11:23　检验 SAE 路由正则与主 LM 更新是否相消

- 假设：频率根先压低低侧标签先验，蒸馏在路由根上与 LM 局部相消。竞争解释是仅由选路统计和负载造成，梯度方向仍一致。
- 先验→模型→计算：对同一个 router 分别求 LM/SAE 梯度，同位置分别统计教师、学生软质量和叶 MAP。另用同样数据对照原频率树与共现树。[跑前约定](/data/250010109/MoE_Router/experiments/1119_hd4_fr_factorial/diagnostics/router-conflict/plan.md)。
- 跑前预测：首要冲突限于根则把根 KL 系数做成单因素；换共现切分仅改善根流量则不能据此认定叶拥挤解决；两份冻结读数不外推训练结论。
- 结果：步 5 的根 SAE/LM 加权范数比 527–1105，9–11/16 序列的一阶投影反向，所测浅层矩阵保留 0.989 投影。步 3816 的根合成投影 0.938–0.986，无序列反向。频率树教师 MAP 根约 97/3，共现树约 80/20；教师 MAP 最忙两叶仍约 61%。相同 4096 位置上教师和学生的低侧软质量约 6.7%，学生低侧实派发 1.42%–1.81%。[结果](/data/250010109/MoE_Router/experiments/1119_hd4_fr_factorial/diagnostics/router-conflict/summary.md)。
- 资产：`analysis_hd4_fr_router_lm_sae_gradient_conflict_20261119`。
- 研究者决定：Unknown。
- 链条位置：机制读数；独立训练效应未测。

今日认识更新：早期 root 的训练方向会被 SAE 目标主导，1B 的冲突已弱。根频率硬约束可解释大部分路由偏斜，改变根不足以解释或解决叶流量过度集中。

## 1119 12:53　A0 上的 SAE 条件关系离线估计

- 假设：超额共现可提供稳定的专家分工信号。最强替代解释是共现主要由词频、位置或单片稀有事件造成，或者关系导入新的派发失衡。
- 先验→模型→计算：TRAIN cache input token 词频三档 × 序列位置四档，扣条件均值，阈值与共现支持收缩后构图。在前片选 768 atom、拟合八组，后片查稳定性、负载和带角色质量权重的教师协方差。真实与按频档置换的分组对比。额外实现不绑定专家 ID 的关系损失，打乱目标在同一块内置换以保持成对目标多重集。
- 跑前预测：后一片复现且超出空模型才进入三臂准备；若图几乎不变，当前背景控制无法说明额外作用；训练收益用 A0 对照另测。[跑前约定](/data/250010109/MoE_Router/experiments/1119_a0_sae_relations/plan.md)。
- 结果：拟合、检查各 131,072 位置。4,393 条边中 92.7% 检查片仍正，所选最低频档相关边 89.3%；中位条件相关 0.02385。真实组留住 53.8% 正相关质量，频档/组大小匹配置换为 18.0%–19.8%；原始与扣背景后的边 Jaccard 0.978。候选目标覆盖 92.7%；背景扣除后教师 top-1 最忙两组从 42.8% 到 40.0%，有效组数 5.61 到 6.28。八组固定训练基在检查片保留 90% 方差需要 10–120 维；是教师读数。用户要求先估计，三臂尚未启动。[对照及角色监督设计](/data/250010109/MoE_Router/experiments/1119_a0_sae_relations/comparison.md)。
- 资产：`analysis_a0_conditional_sae_relations_pilot_20261119`、`representation_e16_train_replay_1115_20261119_index`、`sae_qwen3_0p6b_e16_layer27_final_1b`。
- 研究者决定：Unknown。
- 链条位置：表征读数 → 路由监督可行性。训练效果待测。

今日认识更新：有关联可供学生学习，但第一个粗背景扣除几乎未改变边图，组内可能需要很不一样的读写维数。三臂优先拆关系净收益；角色和谱的显式辅助目标单设对照。

## 1119 13:35　3B 训练监控与同批次对照

- 假设／跑前预测：沿用主训练记录。本次读取既有历史基线与在线 FR。
- 结果：`pt-170s8viu` 2 台各 2 张 H100 Reserved，worker 均 Running。FR 写完第 11,446 步、3,000,500,224 targets 的可恢复里程碑并评估，同步确认第 11,458 步真实更新。到 11,446 步附近最近 500 步约 80,441 targets/s。最近范围排除 A0 精确 3B 遮罩步，499 个同样完整批次纯 LM NLL 为 A0 3.40141、HD4-T 3.39845、FR 3.42117。冻结同 token EVAL FR 3.41302、T 3.39109，低频 SAE 主导桶 FR 比 T 低 0.15912 nat，低频词高 0.03298 nat。A0 只有邻近实际 3.000000B 点 3.39428。TensorBoard 已在新容器恢复，最新可读到 11,446 步的 EVAL。
- 关系监督对照：仍无作业回执或训练曲线，平台当前账号名单无相应提交。既有 A0/HD4-T 曲线为历史对照。
- 资产：`checkpoint_hd4_fr_step11446_20261119`、`analysis_hd4_fr_training_monitor_3b_20261119`。[更新对比](/data/250010109/MoE_Router/experiments/1119_hd4_fr/analysis/monitor-3b/matched-training-loss.pdf)。
- 研究者决定：Unknown。
- 链条位置：loss 与训练效果跟踪。

今日认识更新：FR 追近 T，仍落后 A0 的训练 NLL 约 0.02 nat；低频主导收益延续到 3B，整体 NLL 与低频词仍有缺口。

## 1119 14:34　按研究者要求暂停主训练

- 结果：`pt-170s8viu` 依据训练器 STOP 机制在完成步边界平滑退出，于第 12,500 步、3,276,800,000 targets 保存可恢复完整状态。暂停回执北京时间 14:34:48，平台 14:34:56 进入 `SUCCEEDED`，worker 分别 `Succeeded`、`Deleted`，账号 RUNNING 查询为空。此状态表示平滑退出。最后一次同集全量 NLL 3.429805，低频 SAE 主导 2.036380，低频词 5.903267。[停止回执](/data/250010109/MoE_Router/experiments/1119_hd4_fr/acp/pt-170s8viu-pause-step12500.json)。
- 下一项安排：沿用 A0 三臂同 1B 预算方案。先做正式训练器集成及真实数据 Smoke，再在现有四张 reserved H100 上跑 A0 原版、真实关系、分层打乱关系。固定角色及协方差谱独立做后续消融。当前未开新作业。[比较口径](/data/250010109/MoE_Router/experiments/1119_a0_sae_relations/comparison.md)。
- 资产：`checkpoint_hd4_fr_paused_step12500_20261119`。
- 研究者决定：停止当前训练。科学判断 Unknown。
- 链条位置：训练执行。

## 1119 14:37　更正 A0 基线复用

- 研究者决定：A0 原版已训，直接复用。同预算新增臂为真实 SAE 关系、分层打乱关系，各从同初始化训 1B。
- 核对：历史正式 A0 在 1908/3816 步保存精确 0.5B/1B 存档，同全量 EVAL 实测 NLL 4.1129299/3.7794264。新增臂继承 0.5B/1B 遮罩、样本顺序和 warmup，在同坐标比较；历史缺失的中间 EVAL 优先用存档补评估。此更正替代 14:34 条的三个新训练作业安排。未提交新作业。
- 资产：`checkpoint_moe_baseline_1b_routing_probe_20261101`、`analysis_hd4_fr_historical_eval_alignment_20261119`。[修正后的对照](/data/250010109/MoE_Router/experiments/1119_a0_sae_relations/comparison.md)。

## 1119 14:57　A0 真实 SAE 关系与分层打乱两臂启动

- 假设／跑前预测：沿用条件共现离线估计和两新增臂比较。维持同输入、历史 A0 初始化与原生 8 选 2 路由。真实关系若比历史 A0 与同监督强度的打乱臂省 token，则支持利用真实关系；否则按原口径解释。
- 结果：用户授权的同账户 2 节点 × 2 H100 Reserved 作业 `pt-vhfxty92` 已启动。两臂按流水串行，先各保存 2 步再继续。真实臂首步北京时间 14:51:49，打乱臂 14:53:51，各 262,144 有效 targets，纯 LM NLL 均 12.146187，历史 batch/mask 指纹一致。第二步均达到 524,288 targets、LR 3e-7，检测到实际 router 权重变化。两臂正式 NCCL 均 32/32 经 IB/GDRDMA，0 Socket。真实臂断点续训的四 rank RNG 恢复通过，14:57:09 真实第 3 步，14:57:26 时已读到第 8 步。打乱臂从第 2 步等待真实臂完成后继续。两臂目标各 1B，在 0.5B、1B 进行同历史 A0 的 2,097,152 位置全量 EVAL。[启动回执](/data/250010109/MoE_Router/experiments/1119_a0_sae_relations/acp/startup-receipt.json)。
- 资产：`execution_a0_conditional_sae_relations_two_arm_startup_20261119`。
- 研究者决定：执行两条新增训练。科学判断 Unknown。
- 链条位置：训练执行，尚待效果。

## 1119 18:14　A0 关系监督进度与同批次 loss

- 状态：`pt-vhfxty92` 为 RUNNING，2×2 H100 Reserved 的两台 worker 均 Running。真实臂图表读数 3,726 步 / 976,577,792 targets。最新可恢复边界 3,000 步 / 786,261,248。打乱臂完成初始两步，等待真实臂完成后续跑。
- 结果：0.5B 同集全量 EVAL，真实臂 4.10785577、历史 A0 4.11292988（−0.00507411 nat）。图表结尾 100 步同批次纯 LM NLL 3.66454284 / 3.66740907，500 步均值差 −0.00104216 nat。近 300 步端到端吞吐 83,137 targets/s。1B 真实臂与打乱臂实测全量 EVAL 待出。[图表与数据](/data/250010109/MoE_Router/experiments/1119_a0_sae_relations/analysis/progress-20261119/loss-comparison.pdf)。
- 资产：`analysis_a0_sae_relation_progress_20261119_1814`。
- 研究者决定：Unknown。
- 链条位置：训练执行与早期实测，尚无真实关系对打乱的因果判断。

## 1119 21:46　A0 SAE 关系监督 1B 完成与专家读数

- 假设／竞争解释：沿用原三臂对照，若真实关系确能指导分工，应在保持均衡边际的同时提高相关位置的实际 Top‑2 重合。竞争解释是任意辅助项改变 softmax 熵和总体负载，或低频词被混作低频 SAE 证据。
- 先验→模型→计算与跑前判读：读两臂精确 0.5B/1B，按相同批指纹对历史 A0；用冻结 EVAL 标签分桶并对齐 128 条序列的实际路由。同背景下检查单原子的双向交叉验证专家亲和力。[读数口径](/data/250010109/MoE_Router/experiments/1119_a0_sae_relations/analysis/final-20261119/readout-plan.md)。
- 结果：两臂 3,816 步、10 亿有效 targets，ACP `pt-vhfxty92` SUCCEEDED。A0/真实/打乱在 0.5B 的全量 EVAL 4.11293/4.10786/4.11268，1B 为 3.77943/3.77729/3.78313。最后 500 步每个专家平均接近 12.5% 派发槽，零丢弃。1B 真实关系与实际 Top‑2 重合相关 A0/真实/打乱 0.10235/0.14198/0.08925，真实在单 feature 绑定上没有普遍超出 A0。真实对 A0 在低频 SAE 主导桶为 −0.04491/+0.02463，两点区间均跨零。监督选中 768 个原子全部落在全局高频半区。[解释与数值](/data/250010109/MoE_Router/experiments/1119_a0_sae_relations/analysis/final-20261119/interpretation.md)。
- 资产：`analysis_a0_sae_relation_final_1b_20261119`、`checkpoint_a0_sae_relation_true_500000000_20261119`、`checkpoint_a0_sae_relation_true_1000000000_20261119`、`checkpoint_a0_sae_relation_shuffle_500000000_20261119`、`checkpoint_a0_sae_relation_shuffle_1000000000_20261119`。
- 研究者决定：Unknown。
- 链条位置：实际专家派发读出 → 同预算训练效果。专家功能的干预和训练种子复测尚缺。

今日认识更新：真实 SAE 共现关系引导了组级实际派发并小幅降低同 token NLL。高频 SAE 主导位置贡献绝大部分总体收益；低频词受益没有确认全局低频 SAE 的迁移，后者未被直接监督。

## 1120　三层 Common–Tail 专家对照的跑前约定

- 假设：全局共同成分和尾部共同成分可以各自共享更新。竞争解释是常见 token 因共享根及宽 M 变好，尾部未获得功能分工。
- 先验→模型→计算：沿用活跃问题 #2。后四个 block 替换为 C+M 或 C+E+F。保持 A0 整体参数及每条路径激活宽，纯 LM 从 A0 时间零的同参数样本池训练至 1B。0.5B 和 1B 比相同 EVAL，另测按 SAE 频率的条件访问、尾叶覆盖和 loss。
- 跑前预测：尾部条件访问与低频 NLL 均改善才继续定位 E 的作用。总体单独改善按系统级读数处理。样本或使用不足保留 Unknown。[运行约定与分支](/data/250010109/MoE_Router/experiments/1120_a0_common_tail/plan.md)。
- 研究者决定：按三层结构在 4 张 H100 Reserved 上训一轮并比较 A0。科学判断 Unknown。
- 链条位置：假设 → 架构干预 → loss 与训练效果。

## 1120 19:47　三层 Common–Tail 提交

- 结果：作业 `pt-ik1qcjkj` 在原账户 share-space 申请单节点 4 张 H100 Reserved。CPU 模型核对通过，总参数 507,988,992，每条路径的整模型名义激活参数 281,496,576。初次提交遇到旧桥接器 `service_time_expression` 解析错误，核对没有创建同名任务后，用已登记 workspace 兼容桥接器提交成功。检查时为 `STARTING`，worker Pending，未见实训步。[平台状态](/data/250010109/MoE_Router/experiments/1120_a0_common_tail/acp/state-observed.json)。
- 资产：`execution_a0_common_tail_1b_20261120`。作业内先做两步实训与恢复检查，随后在原作业内继续，计划精确 0.5B、1B 两次全量 EVAL。
- 研究者决定：训练已授权。科学判断 Unknown。
- 链条位置：架构干预的执行，效果待评估。

今日认识更新：common 早停和 tail 继续细分可以在每条路径的激活宽度均保持 A0 水平时实现。实际低频富集、共享节点预测收益和省数据量需要训练和同预算对照。

## 1121　三层 Common–Tail 1B，对历史 A0 的同批次结果

- 假设／先验→模型→计算：沿用 1120 约定。全局根和尾部父节点独立共享，同 active 参数比较 A0。核对 3,816 个批次的样本与目标 mask 指纹，按有效 token 加权的 100 步训练窗口与精确 0.5B、1B 全量 EVAL 对齐。
- 结果：`pt-ik1qcjkj` SUCCEEDED，实际单节点四张 H100 80GB；11 月 20 日北京时间 22:46 完成 1B。0.5B NLL 4.13436 对 A0 4.11293（+0.02143 nat）；1B 3.82106 对 3.77943（+0.04163）。最后 100 步训练差 +0.03322 nat。SAE 低频主导桶 0.5B 差 −0.01477、1B +0.31544。1B EVAL 各改动层的整体深路径访问为 23.54%、12.41%、8.63%、28.60%；训练访问目标与跨数据集访问不同。[图与原始评估](/data/250010109/MoE_Router/experiments/1120_a0_common_tail/analysis/training-loss.pdf)。
- 资产：`checkpoint_family_a0_common_tail_milestones_20261120`、`analysis_a0_common_tail_matched_loss_1b_20261121`。[可读性检查](/data/250010109/Research_System/assets/checks/2026-11-21_common_tail_1b_access.json)。
- 跑前分支：总体落后且低频收益未维持，保留系统级结论。低频路由的功能因果和跨种子泛化待检验。
- 研究者决定：Unknown。
- 链条位置：架构干预 → 同预算 loss。

今日认识更新：同参数、同激活宽度下，当前纯 LM 三层实现没有改善 A0 的 1B 学习效果。训练时的深路径负载目标没有约束冻结偏置后留出数据的访问率。

## 1121　三层 Common–Tail 的负载与专家容量

- 假设与竞争解释：沿用三层模型实验。训练平均负载可能掩盖实际深路径漂移和叶样本不足；另一解释是固定共享/专用宽度及组合数量改变导致损失，独立于路由漂移。
- 先验→模型→计算：对齐 A0 的 3816 个训练批指纹并聚合实际 E/M/F 访问次数。在相同全量 EVAL 读取保存的硬派发、同位置 NLL 和频率桶。由二分类 softmax 后的负载偏置直接计算深路径阈值，并按序列配对重采样 NLL。
- 结果：最后 500 步训练深路径 21.80%–23.96%，叶子占全部 token 2.51%–4.97%，A0 同层每专家约 25%。四层末状态进深路径阈值 99.7997%、99.9997%、99.9997%、99.5997%。block 5/6 低频 SAE 主导位置在 0.5B 到 1B 的深路径访问从 92.17%/83.91% 降到 23.65%/24.66%。1B 有一叶在 EVAL 全程零访问。总体 ΔNLL +0.04163 nat，按桶贡献高频主导 +0.03307、混合 +0.00828、低频主导 +0.00028 nat。[核对表](/data/250010109/MoE_Router/experiments/1120_a0_common_tail/analysis/load-capacity-audit.json)。
- 判读与下一分支：现有读数支持偏置饱和、留出路由漂移和叶数据稀释是待拆因素。对同冻结权重和位置只动路由阈值或做负载匹配换路，可以区分选路与专家能力；若不恢复 NLL，再查结构与训练暴露。该干预尚未执行。
- 资产：`analysis_a0_common_tail_load_capacity_20261121`。研究者决定：Unknown。
- 链条位置：训练与评估读出 → 机制假设；干预未测。

今日认识更新：同激活参数量与训练平均访问量接近目标可以同时伴随路由饱和、尾专家少样本和留出流量漂移。

## 1123　HIFER 启发的 feature 层级与预训练对照

- 假设与竞争解释：复合原子的组成集合可以指导样本共享父专家。竞争解释为层级约束、负载或普通辅助目标造成变化，与真实组成关系无关。
- 先验→模型→计算：TRAIN 因果 E16 二值激活统计频率非对称关系，传递约简后以共同组成集合归并成 2×3 路由树。后四层执行一父一叶，继承未训练 A0 权重，以及总参数和激活参数。学生因果 LM 加 sampled feature 软监督，按节点限制 logit 负载偏置并记录软硬流量。[跑前约定](/data/250010109/MoE_Router/experiments/1123_hifer_pretrain/plan.md)。
- 跑前分支：先比较精确 0.5B/1B 的 A0 全量 EVAL、低频主导桶和访问率。若改善再拆真实关系；只恢复访问率未改善则查共享约束和标签学习；若低覆盖或负载不稳定，保留科学结论未知。
- 结果：786,432 TRAIN 位置拟合，27,312 条约简边、14,961 个复合原子，其中 5,278 个为全局低频半区。独立 TRAIN 检查片上 27,007 条可核验边中 24,538 通过同一方向比率条件。原始六叶软质量 1.7%–46.2%，TRAIN 有界校正后 10.4%–21.2%。[固定树](/data/250010109/MoE_Router/experiments/1123_hifer_pretrain/tree/tree-summary.json)。
- 研究者决定：在四卡 H100 Reserved 上训练。科学判断 Unknown。
- 链条位置：表征建图 → 路由干预 → 预训练效果待测。

## 1123 10:00　HIFER-PT 开跑与短窗负载

- 结果：同账号 ACP 作业 `pt-ow8uzzww` RUNNING，实际单节点四张 H100 Reserved。前两步工程检查通过，全四 rank 由第 2 步恢复；第 3 个更新 786,432 有效目标，纯 LM NLL 12.12254 nat，实际 router 权重变化。首三步批次指纹与历史 A0 相同。[启动回执](/data/250010109/MoE_Router/experiments/1123_hifer_pretrain/acp/startup-receipt.json)。
- 同批次读数：10:00:50 第 135 步、35,389,440 有效 targets。最近 50 步约 95,832 targets/s，采样标签覆盖 99.96%，无丢派发或整步空叶。最忙父节点约 75.8%，最冷叶约 1.16%，偏置到 0.35。近 100 同批纯 LM 差值 +0.00989 nat。0.5B、1B 尚未评估，按配置继续。[实际负载](/data/250010109/MoE_Router/experiments/1123_hifer_pretrain/analysis/load-135.json)。
- 资产：`analysis_hifer_hierarchy_train_20261123`、`execution_hifer_pt_1b_20261123`、`analysis_hifer_pt_1b_startup_20261123`。
- 研究者决定：Unknown（科学判定）。
- 链条位置：已启动的架构及路由干预，完整训练收益待测。

今日认识更新：真实组成图与有界标签先验可送入等预算因果预训练，早期真实训练与恢复已核对。teacher mass 较均匀，实际父叶流量仍存在偏斜。

## 1123　HIFER-PT 1B 完成，三模型 loss 对比

- 假设、竞争解释和跑前预测：沿用上条。先核对同预算的整体效果，架构与路由监督的分项归因需另做对照。
- 先验→模型→计算：A0 与 HIFER-PT 的 3,816 次更新逐步核对样本和目标 mask 指纹。HD4-T 历史日志以参考采样器、更新步和 LR 对齐。训练取纯 LM NLL，100 个完整更新的滚动均值，排除两个目标被遮罩的里程碑更新。全量 EVAL 统一 2,097,152 个留出位置，按各自实际 token 数落点。
- 结果：HIFER-PT 作业 `pt-ow8uzzww` 为 SUCCEEDED，3,816 步、1B 有效目标。HIFER-PT/A0 在 0.5B 为 4.135859/4.112930、在 1B 为 3.805983/3.779426，差 +0.022929/+0.026556 nat。HD4-T 在 0.524288B 和 1.000341504B 的实测为 4.030618 和 3.750810。最后 100 个完整更新里，HIFER-PT 训练 NLL 相对 A0、HD4-T 分别高 0.023242、0.042774 nat。[对比图与原始评估表](/data/250010109/MoE_Router/experiments/1123_hifer_pretrain/analysis/loss-comparison-20261123/loss-comparison.pdf)。
- 资产：`analysis_hifer_pt_a0_hd4t_loss_1b_20261123`、`checkpoint_family_hifer_pt_milestones_20261123`。
- 研究者决定：Unknown。
- 链条位置：路由与架构干预 → 单次训练的整体效果。

今日认识更新：这条 HIFER-PT 训练曲线在后半程较 A0 高约 0.02–0.03 nat，两个同预算全量评估点差距未缩小。

## 1123　HIFER-PT 1B 分频、父叶派发与绑定

- 假设与竞争解释（AI）：当前学生派发只部分实现教师 2×3 分组。竞争解释是同等活跃宽度下，双父互斥使共性样本失去全局参数共享，或真实组成关系本身与预测任务不匹配。
- 先验→模型→计算：若存在真实分工，应在控制输入词频档和位置的背景后，依然在未用于挑选专家的一半序列上看到原子超额派发。用两个实测点的同位置 NLL 拆总体差，并从日志、持久化派发、固定 SAE 激活计算专家访量和绑定。HD4-T 保留实际 token 坐标。[事后读数约定及预测](/data/250010109/MoE_Router/experiments/1123_hifer_pretrain/analysis/diagnosis-1b/readout.md)。
- 结果：1B 相比 A0 高、低、混合主导位置分别 +0.02291、+0.16590、+0.08978 nat，高频贡献总 gap 的 81.6%，混合 17.8%，低频 0.6%。低频只有 1,865 位置，序列配对区间 +[0.11850,0.21342] nat。0.5B 低频也高 +0.06968 nat。训练末 500 步较忙父收到 58.6%–59.1%，全量 EVAL 65.0%–67.1%，全局无空专家或丢派发。1B 教师最大组一致率父 78.7%–81.4%、叶 55.9%–59.3%。低频原子的背景扣除叶绑定超额中位数 22.2–23.7 个百分点，同时低频桶集中于同一叶 L1。各层高频桶的六个实际叶子都比同位置 A0 损失高。[诊断与图](/data/250010109/MoE_Router/experiments/1123_hifer_pretrain/analysis/diagnosis-1b/summary.md)。
- 判读（AI）：先测试同树同骨架的 teacher 直接派发和 student 派发。若追回早期差距再研究交接；否则先在匹配边际的打乱树下检验分组，再考虑等预算全局共享根。训练未执行。
- 资产：`analysis_hifer_pt_frequency_route_diagnosis_20261123`。
- 研究者决定：Unknown。
- 链条位置：同预算 loss 与实际路由读出 → 机制假设，等待架构与路由干预。

今日认识更新：现有 HIFER 树有可复现的原子派发富集，低频主导位置仍落后；总体差主要由覆盖近 95% 的高频主导位置贡献。
