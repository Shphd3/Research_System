# A14_02 改进后 E02–E03：研究者判断记录 审核与执行 Prompt

## 0. 研究者发送前填写

```text
研究者判断记录 审核状态：CARDS_APPROVED
E02 保留或修改：保留频率非劣效主问题；加入严格零曝光 unseen-cell 复用门，
  unseen-cell accuracy 因小样本与小模型下调并冻结为 0.75。
E03 保留或修改：保留 outside-common 四分解；主时间尺度冻结为一个实际
  AdamW step，并用 exact endpoint drop-new 前向干预替代单点 Jacobian 翻译。

Protocol 审核状态：PROTOCOLS_APPROVED
执行范围：E02_FULL_THEN_E03_IF_GATE
```

批准记录：研究者于 2026-07-26 明确批准上述修正、两份 Protocol、本地双卡
执行，以及 E02 gates 通过后自动继续 E03；confirmation 结果不得用于改变阈值。

默认值是 `DRAFT / NOT_WRITTEN / NONE`。AI 不得把空白或未填写状态解释为授权。

这是一份可反复发送的同一 Prompt：

1. `DRAFT` 时，AI 只解释和审核两张 研究者判断记录；
2. 研究者把状态改成 `CARDS_APPROVED` 后，AI 才整理历史归档方案、写正式
   研究者判断记录、更新 anchors，并生成短中文 Protocol 草案；随后停止；
3. 研究者实际阅读中文 Protocol 后，把状态改成 `PROTOCOLS_APPROVED` 并选择
   执行范围；AI 先生成完全一致的英文 canonical Protocol，再实现或运行；
4. 若选择 `E02_FULL_THEN_E03_IF_GATE`，先完成 E02。只有 E02 的能力、测量和
   common-space 识别门通过，才自动继续 E03；否则 E03 记为 parked，不靠调参
   强行继续。

---

## 1. 你的角色与读取顺序

你是 A14_02 的研究审核、Protocol 和实验执行 AI。默认语言为中文，正式研究
artifact 按仓库规范使用英文 canonical 与中文 companion。

先读取：

1. `AGENTS.md`
2. `PROJECTS.md`
3. `daily_research_reports/0726/focus.md`
4. A14_02 parent anchor、现有 E02/E03 subanchors
5. E01、旧 E02、E04–E06 的 `summary.md`、`detailed.md`
6. 理论包中的 H9-L、H9-F、H10、H11、H12 和 T6-L/T6-F
7. `.agents/skills/research-progress-core/`、`problem-anchor-writer/`、
   `experiment-card-writer/` 的完整说明

不要用聊天记录代替这些来源。

## 2. E02 名称与历史证据处理

改进后的实验直接命名为：

```text
A14_02_E02_frequency_mapping_rank_separation
```

不顺延为 E07。现有 `A14_02_E02_component_recombination_capability` 是旧问题的
E02-v1；它的生成器、Protocol、结果和 fail 判定都是真实历史证据，不得覆盖、
删除或改写。

在 `CARDS_APPROVED` 后，先提出并执行一次 lossless migration：

- 将旧 E02-v1 anchor、experiment folder 和引用移动到 A14_02 本线的
  `archive/e02_v1_component_recombination_capability/`；
- archive 内只保留一份完整历史版本，链接必须可读；
- active E02 路径只保留改进后的现象实验；
- parent anchor、line README、PROJECTS 当前状态必须明确区分“旧 E02-v1
  组件重组失败”和“改进后 E02 频率／mapping-rank 问题”；
- 不得因为归档而改变旧 E02 的任何数字或 claim boundary。

改进后的 E03 直接命名为：

```text
A14_02_E03_rare_common_subspace_reuse
```

旧 E03 在批准和执行前已经停止，没有正式 Protocol 或结果。将其旧 anchor 快照
移入 `archive/e03_v0_low_frequency_common_mapping_rank/`，再用审核后的 Thinking
Card 构建 active E03；不得同时保留两个 active E03 定义。

本节只定义未来迁移合同。`DRAFT` 状态下不得移动任何文件。

---

# 研究者判断记录 1：改进后 E02——频率、mapping 数量与三类秩现象

## 我的判断

- **具体现象：** E01 已观察到两件没有被同一实验裁定的现象：相同 exact
  sample 的重复曝光不能替代独立 context diversity；在 capability-passing
  lookup 条件中，独立 mapping 数 $K=1/4/16$ 时 ROOT 功能秩均值为
  $10.2/11.0/12.8$。因此，样本出现频率、context 多样性和独立任务函数数量
  不是同一个变量。
- **机制猜想：** 一个 rare exact relation 若调用已经由大量其他实例学到的
  common mapping，不需要为这个 rare surface 单独建立新的任务功能方向。方向
  预算更直接受已经学会的 mapping 并集控制，而不是受单个样本的 raw frequency
  控制。相反，高频数据如果只是 exact duplicate，或对应多个独立 mappings，
  也不自动产生低秩。
- **最强替代解释：** Common-LowF 看起来低秩，可能只是因为模型没有学会任务、
  输出词表形成瓶颈、raw ROOT 中的 nuisance 被主指标忽略，或者 LowF/HighF 的
  common-function 总剂量、答案边际、context 边际与 optimizer budget 没有真正
  匹配。Independent-HighF 的秩差也可能只是 capability 或 confidence 差异。
- **最不确定的一环：** 不要求强未见组件配对泛化后，怎样最低限度地确认模型
  正在使用 common mapping，而不是记住一个 rare 字符串？当前判断是：不要求
  unseen $\alpha$–$\beta$ 组合，但必须保留与训练样本互斥、底层 mapping 不变的
  小规模新 nuisance-context 任务守卫，并辅以后续 E03 的 leave-target-out
  子空间干预。
- **什么证据会改变判断：** 在所有任务与匹配守卫通过后，Common-LowF 的固定
  读出功能秩稳定高于 Common-HighF；或者 rare 条件需要有意义的新参数／ROOT
  任务方向。反过来，若 Common-LowF 与 Common-HighF 功能秩非劣，同时高频
  Independent 条件仍需要更多功能方向，将支持“frequency 不决定 rank，mapping
  reuse 更直接”的判断。
- **当前唯一决策：** 是否批准一个现象实验，在匹配 common-function 总剂量后
  比较 LowF/HighF 的固定读出 ROOT 功能秩，并把 raw ROOT effective rank 与
  参数更新有效维数作为明确分开的次级指标；Independent-HighF 只作预注册
  mapping-count 参考。

## AI 审核（AI 填写，研究者确认前不得写 anchor）

- **保留的研究者判断：**
- **唯一未定义对象或隐藏假设：**
- **主指标能否区分机制与 rival：**
- **最小反例或区分实验：**
- **AI 建议：** READY / REVISE / PARK

## 我的确认（研究者填写）

- **保留或修改后的判断：**
- **是否允许写入正式 E02 anchor：** yes / no

---

# 研究者判断记录 2：改进后 E03——rare 更新是否新增功能方向

## 我的判断

- **具体现象：** rare 样本调用 common mapping 时，它的梯度或实际 optimizer
  update 不必严格位于估计的 common 参数子空间中。common-space 外分量可能
  存在，但“存在”不等于它幅度大，也不等于它形成了新方向，更不等于这个新
  方向被模型用于任务。
- **机制猜想：** rare 样本的大部分任务有效更新复用 common 参数与 ROOT 功能
  空间。common 外更新若存在，主要有三种情况：幅度很小；幅度非小但复用训练
  历史中已经存在的 residual 方向；或者几何上新颖但只承载 nuisance/gauge，
  删除后不影响冻结读出任务。只有“相对完整更新幅度非小、相对既有 residual
  真正新颖、且删除后任务显著退化”才算新增了功能方向。
- **最强替代解释：** rare 样本确实需要新增一个 common mapping 无法提供的任务
  方向；或者所谓 outside-common 只是 $G_c$ 估计不足、历史 residual 样本不足、
  AdamW 逐坐标预条件、batch 混合或非线性训练分叉造成的测量假象。
- **最不确定的一环：** 如何把“某个 rare 样本造成的更新”从共同训练轨迹中
  单独归因出来。候选最小操作化是：从同一 reference checkpoint 和 optimizer
  state 出发，运行确定性配对短 continuation；两支只差一次 rare target 暴露
  与一个匹配 control，从两支参数和 ROOT 差分定义 target-attributable finite
  effect。rare 即时 per-example gradient 和实际 AdamW step 分开记录，不能
  混称 parameter update。
- **什么证据会改变判断：** 若 common 外的 target-attributable 更新相对完整
  更新不小，其中有稳定的历史 residual 空间外新分量，并且删除该分量后 rare
  target 的冻结读出 CE 显著增加，则需要承认 rare 调用新增了功能方向。若新
  分量绝对／相对幅度小，或删除后功能保持，则支持“rare 不必新增有意义方向”。
- **当前唯一决策：** 是否批准一个因果实验，用 leave-target-out common 空间、
  历史 residual 空间、配对反事实 continuation 和 base-preserving frozen-head
  replay，裁定 rare outside-common 更新的幅度、旧方向复用、新方向和功能。

## AI 审核（AI 填写，研究者确认前不得写 anchor）

- **保留的研究者判断：**
- **唯一未定义对象或隐藏假设：**
- **主指标能否区分机制与 rival：**
- **最小反例或区分实验：**
- **AI 建议：** READY / REVISE / PARK

## 我的确认（研究者填写）

- **保留或修改后的判断：**
- **是否允许写入正式 E03 anchor：** yes / no

---

## 3. 两个实验的最小形式（这是审核材料，不是 Protocol）

### 3.1 改进后 E02：现象与变量分离

**唯一主问题：** 在 common mapping、总 function dose、模型、训练预算、答案与
context 边际匹配后，把 target exact-relation frequency 从 $F=8$ 降到 $F=1$，
是否不会显著增加固定读出 ROOT 功能秩？

| 条件 | $K_{\mathrm{map}}$ | target $F$ | target context | 角色 |
|---|---:|---:|---|---|
| Common-LowF | 1 | 1 | 一个训练 surface；family 其余部分多样 | 主 treatment |
| Common-HighF-Duplicate | 1 | 8 | 新增七次 exact duplicate | 主 control |
| Common-HighF-Diverse | 1 | 8 | 八个独立 nuisance contexts | diversity 守卫 |
| Independent-HighF | 多个 | 8 | 与 common 匹配 | 次级 mapping-count 参考 |

Protocol 审核时必须尝试删去不区分 named rival 的条件；Independent-HighF 不得
与 LowF/HighF 非劣效问题并列成为第二主 verdict。

**三类 rank：**

1. 主指标——固定读出 ROOT 功能秩：

$$
k_{\mathrm{func}}^{\mathrm{fix}}
=
\min\{q:\Delta CE_q\le\epsilon_L,\ \Delta Acc_q\le\epsilon_A\}.
$$

投影由 calibration 冻结，final test 不选 rank，输出头不重训。

2. 次级——centered raw ROOT effective rank：描述完整状态几何；它包含 base 与
   nuisance，只有 residual-energy 守卫成立时才与 H12 关联。
3. 次级——参数更新有效维数：对注册 block 的 gradient matrix、AdamW increment
   matrix 或 trajectory delta 做 SVD；不得把完整 $\theta_T$ 的矩阵秩称为
   parameter rank，也不得把 gradient 与 optimizer update 混写。

**最低能力守卫：** 不要求未见组件配对；要求 full-state 模型在互斥但不改变
底层 mapping 的少量新 nuisance contexts 上保持任务效用。能力失败时功能秩
verdict 为 insufficient，raw/gradient 结果只能描述，不能升级为任务结论。

### 3.2 改进后 E03：outside-common 四分解与因果干预

从同一 $\theta_{\mathrm{ref}}$ 和 optimizer state 出发，构造两条确定性短
continuation：rare branch 注入一次 target，control branch 注入一个预注册匹配
样本，其余 batch 顺序完全相同。定义 target-attributable 参数有限效应：

$$
v_r
=
(\theta_T^{\mathrm{rare}}-\theta_{\mathrm{ref}})
-(\theta_T^{\mathrm{ctrl}}-\theta_{\mathrm{ref}}).
$$

这不是单步 gradient。另行记录 target 暴露前的 per-example gradient 与实际
AdamW-preconditioned step，用于定位 gradient-to-update 差异。

只用非 target common 样本或严格早于 target 的历史估计 common 参数空间 $G_c$。
将历史更新投影到 $G_c^\perp$ 后估计既有 residual 空间
$R_{\mathrm{old}}\subseteq G_c^\perp$。分解：

$$
v_{\parallel}=P_{G_c}v_r,
\qquad
v_{\perp}=(I-P_{G_c})v_r,
$$

$$
v_{\mathrm{old}}=P_{R_{\mathrm{old}}}v_{\perp},
\qquad
v_{\mathrm{new}}=(I-P_{R_{\mathrm{old}}})v_{\perp}.
$$

必须同时报告：

$$
\rho_{\perp}=\frac{\|v_{\perp}\|_2^2}{\|v_r\|_2^2},
\qquad
\rho_{\mathrm{new}}=\frac{\|v_{\mathrm{new}}\|_2^2}{\|v_r\|_2^2},
$$

$$
\nu_{\mathrm{new}}
=
\frac{\|v_{\mathrm{new}}\|_2^2}
{\max(\|v_{\perp}\|_2^2,\varepsilon)}.
$$

$\nu_{\mathrm{new}}$ 只是条件新颖度诊断。一个极小的 $v_\perp$ 即使 100%
新颖，也不能说明它新增了有意义的方向。

ROOT 侧使用 rare/control 两支的精确 counterfactual finite effect：

$$
\Delta h_r(x)
=
h_\rho(x;\theta_T^{\mathrm{rare}})
-h_\rho(x;\theta_T^{\mathrm{ctrl}}).
$$

common ROOT 空间与旧 residual ROOT 空间都必须 leave-target-out。用原冻结输出头
进行 base-preserving replay，主裁定量是删除“新分量”后的 target excess CE：

$$
\Delta CE_{\mathrm{drop\text{-}new}}
=
CE(h_{\mathrm{full}}-\Delta h_{\mathrm{new}})
-CE(h_{\mathrm{full}}).
$$

accuracy drop 与 logit-margin 只作守卫。若 rare/control 分支在完整状态上原本
没有可测功能差异，几何分解仍可报告，但“新方向是否必要”的因果 verdict 应为
insufficient 或“该 rare 暴露本身无可测功能增益”，不能强行宣称 common-only
充分。

**四类判读：**

| 几何与干预结果 | 解释 |
|---|---|
| $\rho_\perp$ 小 | common 外更新总体很小，不因 $\nu_{new}$ 高而升级 |
| $\rho_\perp$ 非小、$\rho_{new}$ 小 | 主要复用既有 residual 方向 |
| $\rho_{new}$ 非小、drop-new 功能不变 | 新几何方向存在，但非固定读出任务方向 |
| $\rho_{new}$ 非小、drop-new 明显伤害任务 | rare 调用新增功能上必要方向 |

---

## 4. AI 审核流程

### 当 `研究者判断记录 审核状态 = DRAFT`

不得改文件、写 Protocol 或执行。分别对两张卡只返回：

```text
E02：
保留的判断：
唯一阻塞点：
必须修改的一句话：
AI 最小修正：
判定：READY / REVISE / PARK

E03：
保留的判断：
唯一阻塞点：
必须修改的一句话：
AI 最小修正：
判定：READY / REVISE / PARK

两实验的逻辑顺序是否成立：
研究者下一步只需做什么：
```

并要求研究者闭卷回答：

```text
E02 真正问题：
E02 主指标与最强 rival：
E02 Pass / Fail / Insufficient：
E03 真正问题：
E03 为什么必须区分 outside 幅度、旧方向、新方向和功能：
E03 主因果指标：
两者不能声称：
```

### 当 `研究者判断记录 审核状态 = CARDS_APPROVED`

只有两张卡的“我的确认”均为 `yes` 时才继续：

1. 先展示 lossless E02-v1 / E03-v0 archive migration 的精确 source→target 表；
2. 执行迁移并更新所有链接，确保没有两个 active E02/E03，也没有历史证据丢失；
3. 把本 Prompt 中两张审核后 研究者判断记录 原样提取为独立、subject-bearing
   `researcher judgment record`；
4. 更新中英文 E02/E03 anchors，保持一个 decision question、一个 primary
   metric、一个 falsifier 和一个 next decision；
5. 只生成短中文 `protocol_cn.md` 草案；此时不生成英文 canonical Protocol；
6. 返回两个中文 Protocol 的 approval snapshot、两者依赖关系、唯一仍需研究者
   裁定的点；停止，不实现、不运行。

### 当 `Protocol 审核状态 = PROTOCOLS_APPROVED`

只有两个 Protocol 的 approval snapshot、conditions、primary metric、
Pass/Fail/Insufficient、seeds、checkpoint rule、test isolation 和执行范围都已由
研究者确认时才继续。

先把获批的两份中文 Protocol 翻译为完全一致的英文 canonical `protocol.md`，
逐项核对 question、conditions、metrics、thresholds、guards 与 claim boundary；
中英文不一致时停止，不得执行。

- `IMPLEMENT_AND_SMOKE`：只实现并验证生成器、频率计数、hooks、gradient/update
  区分、trajectory logging、投影、replay、artifact schema；不得读 confirmation
  test 来调主指标。
- `E02_FULL_THEN_E03_IF_GATE`：完成 smoke 后执行冻结的 E02 full run，写
  `summary.md` / `detailed.md`。只有 E02 capability、rank validity 与 common
  space stability gates 通过，才执行冻结的 E03；否则 E03 parked。
- 不得在看到 confirmation 结果后改变 threshold、condition、seed、checkpoint
  selection 或 primary metric。任何必要修复必须新版本化并说明原 verdict 是否
  仍有效。

结果完成后，先要求研究者闭卷填写：

```text
问题：
直接结果：
更新后的判断：
不能声称：
下一步唯一动作：
```

AI 只核对数字、证据边界和逻辑顺序，再更新最小 owning artifacts。

---

## 5. 统一 claim boundary

即使 E02/E03 都通过，最多可以说：在注册的受控 NTP 任务中，低
exact-relation frequency 没有强迫固定读出 ROOT 功能秩上升；rare 调用的
outside-common 更新是否新增功能方向，可由幅度、历史 residual 新颖性和冻结
读出因果干预共同裁定。

不能据此声称：

- 所有自然语言 rare facts 都复用 common mappings；
- frequency 永远不影响学习或 rank；
- raw hidden-state rank、ROOT 功能秩和参数更新维数相等；
- 完整参数矩阵低秩；
- H9-F 已由 NTP 自动推出；
- 一层合成任务已经证明自然语言或多层 LLM 的同一规律；
- 该结果已经推出 Router 或 MoE 价值。
