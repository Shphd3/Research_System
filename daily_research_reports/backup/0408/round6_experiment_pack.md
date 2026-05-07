# Round 6 Experiment Pack

## 1. Task Restatement

本轮实验名称为：

**Instance-level PPL Divergence Audit**

本轮实验只回答一个问题：

**在真实句子级别上，一阶去均值解耦模型与二阶 / hybrid 模型到底在什么样的样本上出现分歧，这种分歧是否反映了二阶路由的真实必要性？**

当前理论背景：

- 我们已经有较强证据表明，当前表征空间在中心化后主要是 mean-separable。
- `acp_lite` 是当前最强一阶 baseline。
- 二阶项并非完全“饿死”，但当前没有显示出足够独立的几何收益。
- 因此，现在需要一个实例级实验去检查：
  - 两类模型在绝大多数样本上是否其实行为一致；
  - 那些真正分歧的样本是否揭示了二阶模型的适用边界。

---

## 2. Experiment Goal

通过句子级 PPL / loss 差异和路由熵，找出：

1. 一阶模型与二阶模型的共识区；
2. 一阶模型优势区；
3. 二阶模型优势区；

并据此判断：

- 当前“二阶必要性”是否只存在于极少数复杂句子；
- 还是说在真实数据中，二阶模型整体上并没有形成稳定优势。

---

## 3. Models

- Model 1: `acp_lite`
- Model 2: `hybrid` 或 `quadratic_low_rank`

要求：

- 两个模型必须使用相同训练步数 checkpoint；
- 若首选 checkpoint 不存在，回退时必须明确记录。

---

## 4. Data

- 数据来源：当前验证集优先；若可行，可附加 WikiText-103 作为辅助 sanity check
- 样本规模：10,000 个完整句子或固定长度序列
- 必须保证两个模型使用完全相同的 token IDs

---

## 5. Procedure

1. 在 `torch.no_grad()` 下加载两个模型。
2. 对每个句子 $S_i$，分别记录：
   - 平均 loss
   - 句子级 PPL
   - 所有 MoE 层 router 的平均信息熵
3. 计算
   $$
   R_i=\frac{PPL_{1,i}-PPL_{2,i}}{PPL_{1,i}}.
   $$
4. 按如下规则分组：
   - Group A: $|R_i| \le 0.05$
   - Group B: $R_i < -0.05$
   - Group C: $R_i > 0.05$
5. 对每组统计：
   - 规模占比
   - 平均 PPL 差异
   - 平均路由熵
   - 代表性句子样本

---

## 6. Output Contract

必须输出以下结果：

1. JSONL
   - `ppl_divergence_audit.jsonl`
   - 每条记录包含：
     - sentence text
     - `PPL_1`
     - `PPL_2`
     - `H_1`
     - `H_2`
     - `R_i`
     - `group`

2. Markdown summary
   - 三组样本规模占比
   - 平均 PPL 差异
   - 平均路由熵

3. Case study
   - 从 Group B 和 Group C 各随机采样 3 个句子

4. `Experiment Return`
   - 直接按状态文档格式产出：
     - Result summary
     - Reliability audit
     - Hypothesis update
     - Suggested checkpoint delta

---

## 7. Risk Check

- 显存风险：
  - 不保存梯度；
  - 控制 batch size；
  - 必要时做分块推理。

- 对齐风险：
  - 两模型必须推理相同 token IDs；
  - 不允许一边截断、一边不截断。

- 解释风险：
  - 若 Group C 极少，不可夸大二阶项必要性；
  - 若 Group C 规模明显，必须检查是否与更高路由熵或更复杂语义结构相关。

---

## 8. Execution Rule

请先输出一份：

**Protocol Lock / Pre-Run Audit**

必须包含：

1. Task Restatement
2. Protocol Lock
3. Metric Lock
4. Output Contract
5. Risk Check

只有在我确认：

**Protocol locked, ready for execution**

之后，才能正式开始执行。
