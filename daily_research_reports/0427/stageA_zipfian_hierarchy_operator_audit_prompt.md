# Experiment Prompt: Stage A - Zipfian-to-Hierarchy Representation Audit

## 0. Goal

This Stage A experiment tests whether Zipfian / long-tail token statistics actually induce recoverable and functional hierarchical factors in real LLM hidden states.

This is not yet a full hierarchical MoE experiment.

The key question is:

> Can we find evidence that common, domain-specific, and token-specific factors are separable in hidden representations, and that these factors affect next-token prediction?

If Stage A fails, we should not directly move to many-branch or hierarchical MoE.

---

## 1. Main Hypothesis

### H-main

Zipfian token distribution does not directly imply domain-specific hierarchy.

The testable hypothesis is:

> Because token frequencies are highly uneven, some token groups or feature groups may have uneven domain concentration and uneven activation frequency. If this is true, pretrained LM hidden states may contain common factors plus domain-specific or token-specific residual factors. These factors may be useful inputs for experts or routers.

The mechanism chain is:

$$
\text{Zipfian token distribution}
\rightarrow
\text{uneven token / feature frequency}
\rightarrow
\text{domain-concentrated tokens or features}
\rightarrow
\text{recoverable representation factors}
\rightarrow
\text{functional contribution to NTP loss}
$$

Stage A tests the middle three arrows.

---

## 2. Fixed Setting

Use the same base setting as previous H3 / Phase8-H3 bridge experiments.

- Base model: Qwen3-0.6B
- Layer: 8
- Hook point: `post_attention_layernorm`
- Main dataset: WoS
- Calibration dataset: DCLM + WoS
- Backbone: frozen
- Objective for functional tests: next-token prediction
- Unit of analysis:
  - token hidden state $x$
  - target token $y$
  - document domain $d$

Use the same tokenizer and preprocessing as previous experiments.

---

## 3. Required Definitions

Use these definitions in the final report.

- **Token frequency**: how often a token appears in the corpus.
- **Domain concentration**: how strongly a token or feature is concentrated in one WoS domain.
- **Signature token**: a token that appears often enough and is strongly concentrated in one domain.
- **Hidden representation**: hidden state at Qwen3-0.6B layer 8, hook `post_attention_layernorm`.
- **Representation operator**: a method that maps hidden state $x$ into one or more components.
- **Functional contribution**: change in next-token prediction loss after removing or keeping a component.
- **Random split**: a random subspace with matched dimension, used as a control.

Do not call a feature “semantic” or “specialized” unless it has functional evidence.

---

## 4. Stage A Overview

Stage A has three parts.

1. **A0: Token-statistics audit**
   - Does token frequency correlate with domain concentration?

2. **A1: Representation operator audit**
   - Which operator exposes domain-specific or token-specific information better than random?

3. **A2: Functional ablation audit**
   - Does removing the discovered component change NTP loss in the expected token groups?

Only after all three parts show useful evidence should we move to routers or experts.

---

# A0. Token-Statistics Audit

## A0.1 Build token-frequency table

Use WoS train corpus.

For each token $v$, compute:

$$
n(v)=\text{count of token }v
$$

Build frequency buckets:

- common tokens
- middle-frequency tokens
- rare tokens

Use quantiles or pre-existing bucket definitions from H3. Report the exact threshold.

---

## A0.2 Compute domain concentration for each token

For each token $v$, compute:

$$
p(d \mid v)
=
\frac{n(v,d)}{\sum_{d'} n(v,d')}
$$

Define domain concentration:

$$
C_{\text{dom}}(v)
=
\max_d p(d \mid v)
$$

Also compute domain entropy:

$$
H_{\text{dom}}(v)
=
-\sum_d p(d \mid v)\log p(d \mid v)
$$

A token is more domain-specific if $C_{\text{dom}}(v)$ is high and $H_{\text{dom}}(v)$ is low.

---

## A0.3 Define signature tokens

A token $v$ is a signature token if:

$$
n(v) \ge n_{\min}
$$

and

$$
C_{\text{dom}}(v) \ge \tau_{\text{dom}}
$$

Suggested defaults:

- $n_{\min}=20$
- $\tau_{\text{dom}}=0.7$

Report how many signature tokens each domain has.

---

## A0.4 A0 output tables

Produce:

1. Token frequency bucket statistics:

| bucket | num_tokens | mean_count | mean_domain_concentration | mean_domain_entropy |
|---|---:|---:|---:|---:|

2. Top signature tokens per domain:

| domain | token | count | domain_concentration |
|---|---|---:|---:|

3. Frequency bucket vs domain concentration plot or table.

---

## A0.5 A0 interpretation

### If mid / rare tokens are more domain-concentrated

This supports the idea that long-tail statistics may induce domain-specific factors.

### If token frequency and domain concentration are unrelated

Then Zipfian does not support domain-specific hierarchy in this dataset. We should not build hierarchy around domain labels.

---

# A1. Representation Operator Audit

## A1.1 Collect hidden states

For each selected WoS and DCLM token position, save:

- hidden state $x$
- target token $y$
- document domain $d$
- token frequency bucket of $y$
- whether $y$ is a signature token

Use the same layer and hook:

- model: Qwen3-0.6B
- layer: 8
- hook: `post_attention_layernorm`

---

## A1.2 Calibration

Use DCLM + WoS calibration hidden states.

Compute:

$$
\mu = \mathbb{E}[x]
$$

$$
\bar{x}=x-\mu
$$

Run PCA/SVD on centered hidden states:

$$
V=[v_1,\dots,v_r]
$$

For a set of directions $S$, define projection:

$$
P_S(\bar{x})=V_SV_S^\top \bar{x}
$$

---

## A1.3 Candidate operators

Evaluate the following operators.

### O0: raw hidden

$$
T_{\text{raw}}(x)=x
$$

Purpose: baseline.

---

### O1: centered hidden

$$
T_{\text{centered}}(x)=x-\mu
$$

Purpose: check whether mean removal alone helps.

---

### O2: head16

$$
T_{\text{head16}}(x)=V_{1:16}V_{1:16}^{\top}(x-\mu)
$$

Purpose: common / high-variance component.

---

### O3: full tail residual

$$
T_{\text{tail-resid}}(x)
=
(I-V_{1:16}V_{1:16}^{\top})(x-\mu)
$$

Purpose: remove common head, keep residual.

---

### O4: u50

$$
T_{u50}(x)=P_{17:207}(x-\mu)
$$

Purpose: middle variance band.

---

### O5: ext

$$
T_{\text{ext}}(x)=P_{782:r}(x-\mu)
$$

Purpose: extreme low-variance band.

---

### O6: u50_ext

$$
T_{u50\_ext}(x)
=
P_{17:207}(x-\mu)+0.25P_{782:r}(x-\mu)
$$

Purpose: previous main candidate.

---

### O7: random matched subspace

Generate random orthonormal subspaces with the same dimension as `u50_ext`.

Use at least 3 random seeds.

Purpose: control for arbitrary projection.

---

### O8: SAE / sparse dictionary on raw hidden

Train sparse dictionary:

$$
x-\mu \approx Da
$$

where $a$ is sparse activation.

Purpose: test whether sparse features on raw hidden are domain-specific.

---

### O9: SAE / sparse dictionary on tail residual

First compute:

$$
r=(I-V_{1:16}V_{1:16}^{\top})(x-\mu)
$$

Then train:

$$
r \approx Da
$$

Purpose: main learned-decomposition candidate.

This tests whether removing common head before dictionary learning yields more specific features.

---

## A1.4 Probe tasks

For each operator, train simple probes.

Use train / validation split by documents, not by tokens, to avoid leakage.

### Probe 1: domain prediction

Predict WoS domain:

$$
\hat d = q(T(x))
$$

Report accuracy and macro-F1.

---

### Probe 2: signature-token prediction

Predict whether target token is a domain signature token:

$$
\hat s = q(T(x))
$$

Report AUC and F1.

---

### Probe 3: token-frequency bucket prediction

Predict target token bucket:

- common
- middle
- rare

Report accuracy and macro-F1.

---

## A1.5 Feature statistics for SAE operators

For each dictionary feature $j$, define activation:

$$
s_j(x)=\mathbf{1}[a_j(x)>0]
$$

Compute:

### Activation frequency

$$
p_j=\mathbb{P}[s_j(x)=1]
$$

### Domain specificity

$$
C_{\text{dom}}(j)=\max_d p(d \mid s_j=1)
$$

### Mutual information with domain

$$
I(s_j;D)
$$

### Mutual information with token-frequency bucket

$$
I(s_j;B_{\text{freq}})
$$

Report top features by domain specificity and frequency-bucket specificity.

---

## A1.6 A1 output tables

### Operator probe table

| operator | dim | domain_acc | domain_macro_f1 | signature_auc | freq_bucket_acc | notes |
|---|---:|---:|---:|---:|---:|---|

### SAE feature table

| feature_id | activation_freq | top_domain | domain_concentration | MI_domain | MI_freq_bucket | top_tokens |
|---:|---:|---|---:|---:|---:|---|

---

## A1.7 A1 interpretation

### Supportive result

If tail residual or SAE-on-tail-residual beats raw, PCA bands, and random split on domain / signature / frequency probes, then we have evidence that a useful decomposition operator exists.

### Negative result

If random split matches the proposed operators, then the decomposition is not specific.

### Important warning

Probe accuracy alone is not enough. A component must also show functional contribution in A2.

---

# A2. Functional Ablation Audit

## A2.1 Goal

A component is useful only if removing it changes next-token prediction loss.

For each operator, test whether the component affects NTP loss on:

- common tokens
- middle-frequency tokens
- rare tokens
- signature tokens
- each domain

---

## A2.2 Forward intervention

For each hidden state $x$ at layer 8, create modified hidden states and continue the model forward from layer 8.

### For PCA component removal

For component $z=T(x)$, define:

$$
x' = x - z
$$

Then compute NTP loss using $x'$.

### For tail residual preservation

To keep only component $z$, define:

$$
x' = \mu + z
$$

Then compute NTP loss.

### For SAE feature removal

If residual is:

$$
r \approx Da
$$

and selected feature set is $S$, remove those features:

$$
r' = r - D_S a_S
$$

Then reconstruct:

$$
x'=\mu+V_{1:16}V_{1:16}^{\top}(x-\mu)+r'
$$

Then compute NTP loss.

---

## A2.3 Ablation metric

For bucket or group $B$:

$$
\Delta L_B
=
L_B(\text{modified hidden})
-
L_B(\text{original hidden})
$$

Positive $\Delta L_B$ means the removed component was useful for that group.

---

## A2.4 Required A2 tables

### Component ablation table

| operator | component_removed | common_delta | middle_delta | rare_delta | signature_delta | domain_specific_delta |
|---|---|---:|---:|---:|---:|---:|

### SAE feature-group ablation table

Group SAE features by:

1. top-domain features;
2. high activation frequency features;
3. low activation frequency features;
4. token-frequency-specific features.

| feature_group | num_features | common_delta | middle_delta | rare_delta | signature_delta | top_domain_delta |
|---|---:|---:|---:|---:|---:|---:|

---

## A2.5 Expected results

### Expected result that supports hierarchy

We expect:

1. common / head components affect common tokens broadly;
2. tail residual or SAE residual features affect signature / middle / rare tokens more;
3. domain-specific feature groups hurt their own domain more when removed;
4. these effects are stronger than random split.

This would support:

> hidden states contain recoverable and functional common/specific factors.

### Result that rejects domain-specific hierarchy

If removing domain-specific or tail features does not change NTP loss, or random features have the same effect, then the domain-specific hierarchy hypothesis is not supported.

### Result that suggests a different hierarchy

If token-frequency effects appear but domain-specific effects do not, then the hierarchy should be based on token/function frequency rather than domain.

---

# 5. Stage A Pass / Fail Gates

## Gate A0: Zipfian-to-domain link

Pass if middle / rare tokens show higher domain concentration or lower domain entropy than common tokens.

If fail:

> Zipfian does not support domain-specific hierarchy in this dataset.

---

## Gate A1: Operator recoverability

Pass if at least one non-random operator beats raw and random controls on domain / signature / frequency probes.

If fail:

> We have no evidence that the operator exposes useful hierarchical factors.

---

## Gate A2: Functional contribution

Pass if component ablation causes targeted NTP loss changes, especially on signature or rare tokens, and this effect is stronger than random.

If fail:

> The component may be statistically separable but not functionally useful.

---

## Gate A3: Candidate for Stage B

A candidate operator enters router / expert experiments only if it passes:

1. A0 or gives another clear non-domain factor;
2. A1;
3. A2.

If only A1 passes but A2 fails, do not build hierarchy yet.

---

# 6. Final Report Template

Produce a markdown report with these sections:

1. Objective
2. Hypothesis being tested
3. Dataset and token statistics
4. Token frequency vs domain concentration
5. Hidden-state calibration
6. Operator definitions
7. Probe results
8. SAE / dictionary feature statistics
9. Functional ablation results
10. Random control comparison
11. Gate decisions
12. What can be claimed
13. What cannot be claimed
14. Recommended next step

---

# 7. Interpretation Rules

Use these exact interpretations.

## Case 1: A0 fails

Conclusion:

> Zipfian token frequency alone does not produce a domain-specific hierarchy in this dataset. Do not build domain hierarchy based only on Zipfian.

## Case 2: A0 passes, but A1 fails

Conclusion:

> Domain-concentrated tokens exist, but current representation operators do not recover them cleanly.

## Case 3: A1 passes, but A2 fails

Conclusion:

> The operator exposes statistically separable factors, but they are not yet proven to matter for NTP loss.

## Case 4: A2 passes only for SAE-on-tail-residual

Conclusion:

> Fixed PCA bands may be too crude. Learned sparse residual features are a better candidate for expert/router inputs.

## Case 5: Random split matches all operators

Conclusion:

> The current decomposition is not specific. More branches or hierarchy are not justified.

## Case 6: A0, A1, and A2 pass

Conclusion:

> There is evidence for recoverable and functional common/specific factors. Proceed to Stage B: router/expert audit using the best operator.
