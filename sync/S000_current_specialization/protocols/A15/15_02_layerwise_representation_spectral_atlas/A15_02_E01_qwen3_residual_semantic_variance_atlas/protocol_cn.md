---
experiment_id: A15_02_E01_qwen3_residual_semantic_variance_atlas
anchor_id: 15_02_layerwise_representation_spectral_atlas
status: approved_for_implementation_smoke_and_full
approved_by: user
approval_date: 2026-08-04
canonical_language: en
---

# Protocol：Qwen3-8B 粗细语义的层间方差与 16 带画像

## 0. Approval And Confirmation Ledger

用户于 2026-08-04 完整审核并批准问题、两级语义定义、8×8 数据、冻结模型、16 带边界、指标、统计、热力图、implementation、smoke 与 full。发布、commit、push 未获授权。

| Block | Status | Frozen decision |
| --- | --- | --- |
| A Question / boundary | CONFIRMED | 冻结 Qwen3 的粗细相对区分度与谱位置 |
| B Data / provenance | CONFIRMED | 8 parents × 8 children × 8 definitions；独立 DCLM basis |
| C Diagnostic task | CONFIRMED | 同一状态的八分类 coarse 与 conditional fine |
| D Model / representation | CONFIRMED | Qwen3-8B embedding + 36 raw block residual outputs |
| E Objective / optimization | CONFIRMED | 模型不训练；ridge probe 只作能力门 |
| F Comparison / evidence | CONFIRMED | $R_\ell$、16-band $b/q/j/e$、nested controls |
| G Execution | CONFIRMED | smoke 后 full；Figures 0--3 必须视觉审计 |

跨块一致性：PASS。数据同时暴露粗细变量；任务、表示与指标兼容；confirmation 不参与选择；主指标区分深度假设与尺度/随机方向 rival；资源与产物覆盖全部条件。

## A. Question And Claim Boundary

唯一问题：粗类别是否在浅层已较易区分、细类别是否随深度获得更大的相对区分度，以及两者的类别间语义方差是否表现为共同 head-dominance、细语义 middle/tail 相对富集。

实验是冻结静态审计。允许结论是层特异表征画像；禁止升级为组合计算、Router 设计或训练收益。

## B. Data Construction And Provenance

### B1. Balanced taxonomy

冻结 8 个父类，每类 8 个子类：

| Parent | Children |
| --- | --- |
| mathematics | algebra; analysis; geometry; topology; number theory; combinatorics; probability; statistics |
| physics | mechanics; electromagnetism; thermodynamics; optics; quantum physics; relativity; condensed matter physics; particle physics |
| chemistry | organic; inorganic; physical; analytical; electrochemistry; nuclear; polymer; theoretical chemistry |
| biology | genetics; ecology; evolutionary biology; cell biology; molecular biology; microbiology; developmental biology; physiology |
| computer science | algorithms; operating systems; networks; databases; artificial intelligence; programming languages; graphics; cybersecurity |
| economics | microeconomics; macroeconomics; econometrics; international; labor; public; development; financial economics |
| medicine | cardiology; neurology; oncology; immunology; endocrinology; gastroenterology; pulmonology; nephrology |
| linguistics | phonetics; phonology; morphology; syntax; semantics; pragmatics; sociolinguistics; psycholinguistics |

每个子类建立至少六条人工审核的事实原子，不含 parent/child 正确标签字符串。四个模板族各使用两个不重叠事实组合，共 8 条定义，总计 512 条。

共同形式：

```text
Topic description: <definition without label names>
Identify the broad academic field and the specific subfield.
Classification:
```

读出最终冒号 token。生成器在看结果前做 tokenizer-aware 长度与位置匹配；若某条失败，只允许语义等价的最小措辞修复，禁止按模型结果筛选概念。

结果开启前的实现澄清：使用被 attention mask 屏蔽的左侧 padding 和显式 position ids，把所有最终冒号放在同一绝对 RoPE 位置，不向正文加入可见 filler。自然文本长度作为 nuisance 完整记录；长度单变量分类器以及对长度、模板、事实 bundle 的无标签残差化都不得解释主方向。

### B2. Split and provenance

- design：模板 T1/T2，每类 4 条；
- sealed confirmation：模板 T3/T4，每类 4 条；
- 标签、文本、token ids、readout span、模板、事实原子、来源、split 与 SHA-256 全部固化；
- confirmation 只在规则、probe、统计和图合同冻结后开启一次；
- 原 32 条链不进入主统计，只作外部描述性对照。

### B3. Background covariance

复用 A15_02_02_E02 的 128 篇独立 DCLM 文档、65,536 token 和 token hash `5c2e9f6b7d307436eda018b7719bc38cddab6387881d77f89bc74fb717b2f792`。必须验证新定义句无逐句泄漏。

## C. Diagnostic Task And Supervision

同一 $h_{\ell,p,c,t}$ 同时形成：

1. 八分类 coarse 标签 $p$；
2. 固定 $p$ 后的八分类 fine 标签 $c\mid p$。

Ridge multinomial probe 只确认变量可读。Fine probe 每个父类独立拟合八分类后平均；coarse probe 反复匹配抽样到相同每类样本数。模型不接收梯度。

## D. Model And Representation

- path: `/data/share/Qwen3-8B`；
- architecture: `Qwen3ForCausalLM`；
- 36 blocks，hidden size 4096；
- bfloat16 forward，FP64 moments/eigendecomposition/statistics；
- sites：embedding output + blocks 1--36 raw residual output before final model norm；
- object：共同 `Classification:` token；
- 禁止读取概念词 token，禁止在本轮加入 attention-head 或 MLP-update 对象。

模型、tokenizer 与权重 hash 必须与既有 `model_manifest.json` 一致。

## E. Objective And Optimization

Qwen 无训练、无 optimizer、无 checkpoint selection。Probe 标准化、ridge strength 和任何操作阈值只由 design split 选择；confirmation 标签不得进入拟合、选层、选频带、阈值或停机决定。

## F. Comparison And Decision Evidence

### F1. Depth metric

$$
D_{\ell,g}=\frac{\operatorname{tr}(B_\ell^g)}{\operatorname{tr}(W_\ell^g)+\epsilon},
\quad
R_\ell=\log\frac{D_{\ell,\mathrm{fine}}}{D_{\ell,\mathrm{coarse}}}.
$$

主差分：

$$
T_{\mathrm{depth}}
=\operatorname{median}_{25:35}R_\ell
-\operatorname{median}_{1:12}R_\ell.
$$

Depth Pass 要求 nested-bootstrap 95% 下界大于零、四模板方向一致、leave-one-parent-out 同号，且 matched held-out probe 给出同向 fine-relative gain。Block 36 单列。

### F2. Sixteen bands

每层按背景 $\lambda$ 递减切分：F1 ranks 1--256；F2--F8 ranks 257--2048；F9--F16 ranks 2049--4096。主推断逐带完成，H/M/T 只是预注册摘要。

每方向实际语义方差：

$$
b_{\ell,g,k}=\frac{\operatorname{tr}(U_{\ell,k}^\top B_\ell^gU_{\ell,k})}{256}.
$$

同时报告：相对背景方差 $q$、相对类内噪声 $j$、相对全谱每方向均值的 $e$。

Head-dominance 要求模型级 $b_{F1}$ 高于 F2--F16 每方向平均，并报告 F1 是否为 16 带 argmax。

Fine non-head enrichment：

$$
\Delta_{\ell,M}=\log\frac{\operatorname{mean}_{2:8}e_{\ell,\mathrm{fine},k}}
{\operatorname{mean}_{2:8}e_{\ell,\mathrm{coarse},k}},
$$

$$
\Delta_{\ell,T}=\log\frac{\operatorname{mean}_{9:16}e_{\ell,\mathrm{fine},k}}
{\operatorname{mean}_{9:16}e_{\ell,\mathrm{coarse},k}}.
$$

Spectral Pass 要求 late layers 的 $\Delta_M,\Delta_T$ 下界均大于零，并在 $q,j$、封存模板、三种 eigenvalue floor、half-split basis 和同维随机方向下保持。

### F3. Statistics and controls

- 2,000 次 parent→child→template nested bootstrap；
- 5,000 次层级标签置换；
- 256 个同维 Haar 随机子空间；
- 37×16 family 的 BH-FDR；
- leave-one-parent-out；
- calibration half-split 与 wrong-layer basis；
- 16 个细带全部报告 half-split projector overlap。若某一细带在两半 calibration 中旋转，即使热力图单元很大，也不能支撑该细带身份结论；宽 H/M/T 结论还必须在两个独立半基底下保持语义画像方向；
- eigenvalue floors $10^{-6},10^{-5},10^{-4}\lambda_1$；
- 统计单位是语义家族/子类，不是 512 条独立句子。

### F4. Verdict

- Joint Pass：Depth 与 Spectral 均通过；
- Clause-specific result：只通过一项时分别报告，不升级为联合结论；
- Fail：有效性门均通过但相应命题不成立；
- Insufficient：数据、capability、basis、token、数值或 confirmation 门失败。

## G. Execution And Reproducibility Boundary

### G1. Stages

1. S0：固化 taxonomy、fact bank、文本、model/calibration manifest；
2. S1：2 parents ×2 children ×2 texts，层 0/12/24/35/36 smoke；
3. S2：完成 512 条全层状态提取与 probe capability gate；
4. S3：复用或重算 basis，完成 16 带 $b/q/j/e$、bootstrap、permutation、random null；
5. S4：生成 Figures 0--3 并实际打开审计；
6. S5：写 summary/detailed，更新 Anchor Current Evidence 与 Claim Boundary。

### G2. Stop rules

若 label leakage、读出位置、粗细八分类平衡、full-state probe、basis stability、energy reconstruction 或 tail-floor guard 失败，先停止解释并修复数据/工程；不得删除不利概念、模板、频带或降低随机对照。

近简并 tail 中单个 projector 不稳定，不会抹去不依赖 basis 的深度区分度命题；但该细带只能描述，且只有预注册的宽频带画像在两个半基底下仍同向时，频谱命题才有资格裁定。

### G3. Required figures

**Figure 0，奇异值/特征值谱：**x=rank 1--4096；y=$\sqrt\lambda$ 或 $\lambda$（log）；展示早、中、晚、block 35/36 并标 16 带；另给 layer×rank normalized spectrum heatmap。

**Figure 1，粗细区分度深度轨迹：**x=layer 0--36；y=$D_{coarse}$、$D_{fine}$、$R_\ell$；95% nested-bootstrap 区间；block 36 单列。

**Figure 2，决定性热力图：**rows=37 representation sites；columns=F1--F16；分别绘制 coarse、fine、fine-minus-coarse 的 $b$、$q$、$j$。Colorbar 必须解释单位、正负与不能证明。

**Figure 3，代表层 16 带曲线：**展示 embedding、early、middle、late、block 35/36；粗细不同颜色及置信区间；标出 head/middle/tail。

图像必须实际打开，检查轴、单位、色条、动态范围、末层和符号可读性。

### G4. Artifacts

Worker 保存代码、原始 states、moments、basis 和日志。Research mainline 只保存 taxonomy/fact/text/model/calibration manifests、小型 CSV、Figures 0--3、`summary.md` 与 `detailed.md`。

### G5. Approval scope

Implementation、smoke 与 full：approved。Publication、graph、root sync、commit、push：not approved。
