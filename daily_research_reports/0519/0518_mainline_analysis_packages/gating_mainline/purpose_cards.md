# Purpose Cards - Gating Mainline

## G0. Implementation Sanity: Attention-output Gate, Original Expert Input

**Purpose:** 确认新 oracle-MoE 实现符合组会修改。

**Hypothesis:** 如果 gate input 和 expert input 被混淆，后续所有 routing 结论不可信。

**Setup:**

```text
z_t = attention_output_t  -> router/gate
h_t = original hidden_t   -> expert FFN
output = gate(z_t) selects Expert(h_t)
```

**Metrics:**

- printed tensor hooks confirm `gate_input != expert_input` unless intended;
- ablate attention output only affects gate logits, not expert input tensor;
- ablate expert input affects expert output, not gate logits.

**Decision:** 未通过则不做任何 main experiment。

---

## G1. Router Partition Reverse Engineering

**Purpose:** 解释 router 实际分类边界。

**Hypothesis:** Router 不是按人工 feature id，而是按 attention-output geometry / utility / common component 划分。

**Setup:** 1-layer Transformer + MoE；full attention；MoE gate 用 attention output。

**Metrics:**

- expert-cell top examples;
- route flip rate under counterfactual edits;
- boundary-walk switch point;
- routing stability after common-component removal;
- selected-vs-best expert utility gap.

**Expected outcomes:**

- If route follows attention-source: route flip aligns with changed attention top keys.
- If route follows common component: removing common PCs changes routing.
- If experts are redundant: forced utility matrix has many near-best experts per sample.

**What this can prove:** ordinary / oracle-style routing partition is or is not aligned with attention-output structure.

**What this cannot prove:** reverse index is useful; that requires stage 2.

---

## G2. Inhibition as Diagnostic, Not Main Solution

**Purpose:** 测试 inhibition 是否能让 features 更排他，同时判断它是否只是制造人为 partition。

**Hypothesis:** Inhibition 可以增加 exclusivity，但不能保证 many-feature-to-few-expert 的 collision control，也不能保证 reverse-index usefulness。

**Setup:** all-expert forward；对 selected expert 降低 CE，对 non-selected experts 做 ranking margin，使 selected expert 比 others 更好。

**Safer loss form:**

```text
L = CE_selected + beta * sum_e!=s max(0, margin - (CE_e - CE_selected)) + gamma * balance
```

不要直接最大化 non-selected CE，避免训练发散或制造反机制。

**Metrics:**

- one-feature exclusivity: entropy P(expert | feature)
- multi-feature collision: number of features per expert
- NTP loss/readback
- forced utility gap
- reverse-index recall if passed to stage 2

**Decision:** 如果 inhibition 只提高 exclusivity 但 NTP 或 RI 不好，不能作为主线正结果。
