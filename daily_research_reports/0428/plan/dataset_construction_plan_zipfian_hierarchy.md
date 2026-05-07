# 数据集构建计划：Synthetic Natural Zipfian Hierarchy Dataset

## 0. 本文目的

本数据集不是为了证明真实语言一定有 hierarchy，而是为了构造一个“真相已知”的实验世界。

核心问题是：

> 如果数据本身真的具有 Zipfian + hierarchical latent structure，那么 Hierarchical MoE 能不能学出来？

这里先固定数据假设，排除“真实世界到底是不是这样”的不确定性。

---

## 1. 基座数据集选择

### 推荐方案：Qwen tokenizer + DCLM / WoS word-phrase inventory

使用：

- `Qwen3-0.6B` tokenizer；
- `DCLM` 用于抽取 general / common word-phrase pool；
- `WoS` 用于抽取 scientific / domain-style word-phrase pool；
- 但不直接使用原始句子作为训练样本。

也就是说：

> 基座数据集只提供可读词、短语、实体和频率统计；真正训练样本由我们用模板和层级标签生成，最后再用 Qwen tokenizer 编码。

这样做的原因：

1. synthetic 数据的真实层级由我们控制；
2. 文本仍然是可读自然语言，避免完全随机 token 对 pretrained 0.6B 模型过于离谱；
3. token id 仍然来自真实 tokenizer，训练接口不需要特殊处理；
4. 可以检查生成文本在 tokenizer 后是否满足 Zipfian rank-frequency law；
5. 可以知道每个 phrase/span/token 来自 common / coarse / fine 哪一层。

---

## 2. 数据生成总结构

每条 synthetic document 有两个 latent labels：

$$
c \in \{1,\dots,C\}
$$

$$
f \in \{1,\dots,F\}
$$

其中：

- $c$ 是 coarse category；
- $f$ 是 fine category；
- 每个 coarse 下面有若干 fine。
- `common` 不是 document-level label，而是 token/span-level source，表示所有 coarse / fine 都共享的通用语言成分。

第一版建议：

```text
C = 4
F_per_coarse = 4
F_total = 16
sequence_length = 128
train_docs = 50000
valid_docs = 2000
test_docs = 5000
```

每条 document 先采样一个 coarse label，再在该 coarse 下采样一个 fine label。

第一版建议 `coarse_label` 和 `fine_label` 均匀采样。Zipfian 控制的是 word / phrase / token 的出现频率，不控制类别采样频率，避免把 class imbalance 混入第一版解释。

随后用自然语言模板生成若干句子。每个模板包含三类 slot：

```text
common slot: 通用句式、连接词、方法词
coarse slot: 大领域词或大主题短语
fine slot: 细主题词、实体、动作或属性
```

例如：

```text
In this study, the {coarse_method} examines {fine_entity} under {fine_condition}.
The report shows that {fine_process} changes when {coarse_context} is adjusted.
```

最终 document 是可读文本，而不是随机 token 序列。`sequence_length = 128` 指 tokenizer 编码后的目标长度，可以通过截断或补充模板句子控制。

### 2.1 模板多样性要求

第一版虽然使用模板，但不能让模板本身成为 shortcut。生成器需要满足：

1. 每个 coarse / fine 至少覆盖多种模板；
2. document 内句子顺序随机；
3. common / coarse / fine slot 的位置不能固定；
4. 随机加入 optional clause、背景句、转折句或结果句；
5. `template_id` 只用于分析，不喂给模型。

最低配置：

```text
templates_per_coarse >= 8
templates_per_fine >= 4
optional_clause_prob = 0.3
sentence_shuffle = true
slot_position_shuffle = true
```

---

## 3. Word / Phrase Pool 构造

把 synthetic vocabulary 分成三层，但 pool 中放的是可读 word / phrase / entity，而不是任意 token id：

1. `common words / phrases`
   - 所有 document 都可能出现；
   - 对应通用句式、功能词、学术表达、报告表达。

2. `coarse-specific words / phrases`
   - 只在某个 coarse category 下高概率出现；
   - 用于制造大领域差异，例如 medicine / computer science / physics / materials。

3. `fine-specific words / phrases`
   - 只在某个 fine category 下高概率出现；
   - 用于制造更细粒度差异，例如 insulin / tumor / transformer / optimizer / alloy / crystal。

推荐第一版 pool：

```text
common_pool_size = 512
coarse_pool_size_per_coarse = 256
fine_pool_size_per_fine = 128
```

总 word / phrase item 数约为：

$$
512 + 4 \times 256 + 16 \times 128 = 3584
$$

这些 item 可以从 DCLM / WoS 中抽取并人工过滤，也可以先手写小规模 seed list，再用规则扩展。生成文本后统一用 Qwen tokenizer 编码。

### 3.1 Overlap / Noise 设计

为了避免模型只靠 token identity shortcut 完成任务，pool 之间需要少量共享和噪声：

1. `shared_coarse_items`：少量 item 在多个 coarse 中出现，但概率不同；
2. `shared_fine_items`：少量 item 在同一个 coarse 下的多个 fine 中出现，但概率不同；
3. `background_noise_items`：少量与当前 coarse / fine 无关的词短语，低概率插入；
4. fine-specific item 不应 100% 只出现在单一 fine 中，可以保留高 concentration，但不要完全 deterministic。

第一版建议：

```text
coarse_overlap_rate = 0.10
fine_overlap_rate = 0.15
background_noise_rate = 0.05
max_signature_concentration_target = 0.85
```

这样数据仍有真实 hierarchy，但不会退化成简单查表。

---

## 4. 如何满足 Zipfian 定律

### 4.1 Zipfian 定义

给 word / phrase item 排名 $r$，采样概率满足：

$$
p(r) \propto \frac{1}{r^\alpha}
$$

第一版使用：

$$
\alpha = 1.0
$$

生成后必须同时检查 word/phrase 级别和 tokenizer 后 token id 级别的 log-rank / log-frequency 是否近似线性。

---

### 4.2 每个 pool 内部使用 Zipfian

对 common / coarse / fine word-phrase pool 分别构造 Zipfian 分布：

$$
p_{\text{common}}(v) \propto \frac{1}{r(v)^\alpha}
$$

$$
p_{\text{coarse}}(v \mid c) \propto \frac{1}{r_c(v)^\alpha}
$$

$$
p_{\text{fine}}(v \mid f) \propto \frac{1}{r_f(v)^\alpha}
$$

其中 $r(v)$ 是 word / phrase item 在对应 pool 内的 rank。

---

### 4.3 每个模板 slot 的来源

不再对每个 token position 独立采样。每条 document 由模板句子组成，每个模板有固定或可采样的 slot 来源：

$$
s_j \in \{\text{common},\text{coarse},\text{fine}\}
$$

第一版推荐：

$$
\rho_{\text{common}}=0.6
$$

$$
\rho_{\text{coarse}}=0.25
$$

$$
\rho_{\text{fine}}=0.15
$$

然后：

$$
p(v_j \mid c,f)
=\rho_{\text{common}}p_{\text{common}}(v_j)
+
\rho_{\text{coarse}}p_{\text{coarse}}(v_j\mid c)
+
\rho_{\text{fine}}p_{\text{fine}}(v_j\mid f)
$$

其中 $v_j$ 是被填入第 $j$ 个 slot 的 word / phrase item。

这个生成过程明确包含三层：

```text
common structure
→ coarse structure
→ fine structure
```

同时文本仍保持自然语言形式，而不是 bag-of-tokens。

### 4.4 与 Conditional Hierarchical MoE 的对应关系

数据源标签和第一阶段主模型的层级对应如下：

```text
token_source = common
-> global common expert

token_source = coarse
-> conditional-common expert inside the sampled coarse group

token_source = fine
-> conditional-tail / fine expert inside the sampled coarse group
```

因此：

- `coarse_label` 是 document-level 大组标签；
- `fine_label` 是 coarse group 内的细主题标签；
- `token_source = common/coarse/fine` 是 token/span-level 来源标签；
- `coarse-source tokens` 在模型中不是 global common，而是 coarse 条件下的 conditional-common；
- `fine-source tokens` 在模型中对应 conditional-tail / fine branch。

---

## 5. 为什么这样能测试 hierarchy

因为每个 phrase/span 都有真实来源标签，tokenizer 后也可以把来源映射到对应 token span：

```text
span_source = common / coarse / fine
coarse_label = c
fine_label = f
```

所以训练后可以直接检查：

1. router 是否恢复 coarse label；
2. fine router 是否恢复 fine label；
3. expert 是否对应到正确的 fine group；
4. selected expert 是否真的比其他 expert 更会预测当前 token。

其中第 4 点是必要条件之一：如果 router 看起来恢复了 coarse / fine label，但 selected expert 对当前 token 的 counterfactual NTP loss 不优于其他 expert，就不能说模型学出了 functional specialization。

这就是“学得出来”的基础。

---

## 6. 数据集输出格式

每条样本保存：

```json
{
  "text": "...",
  "input_ids": [ ... ],
  "labels": [ ... ],
  "template_ids": [ ... ],
  "coarse_label": 0,
  "fine_label": 3,
  "span_source": [
    {"char_start": 0, "char_end": 12, "source": "common"},
    {"char_start": 13, "char_end": 28, "source": "coarse"},
    {"char_start": 29, "char_end": 43, "source": "fine"}
  ],
  "token_source": ["common", "coarse", "fine", ...],
  "token_frequency_bucket": ["common", "middle", "rare", ...]
}
```

其中：

- `text` 是生成出的可读自然语言文本；
- `input_ids` 是模型输入；
- `labels` 是 next-token prediction target；
- `template_ids` 记录每个句子来自哪个模板；
- `coarse_label` 是 document-level 大类；
- `fine_label` 是 document-level 小类；
- `span_source` 是每个生成短语在原始文本中的来源；
- `token_source` 是 tokenizer 后每个 token 对应的真实来源；
- `token_frequency_bucket` 用于后续 common / middle / rare 分桶分析。

---

## 7. 数据集 sanity check

训练模型前必须先检查数据本身。

### Check 1: Zipfian slope

统计生成语料中的 word/phrase item count 和 tokenizer 后 token id count，分别按频率排序，拟合：

$$
\log n(r) = a - \alpha \log r
$$

要求：

```text
alpha_hat in [0.9, 1.2]
R^2 >= 0.95
```

如果 word/phrase 级别满足但 token id 级别不满足，需要调整 phrase 长度、pool item 或 tokenizer 后的过滤规则。

---

### Check 2: Coarse signature words / tokens

对每个 word/phrase item 和 tokenizer 后 token 分别计算：

$$
p(c\mid v)
=\frac{n(v,c)}{\sum_{c'} n(v,c')}
$$

定义 coarse concentration：

$$
C_{\text{coarse}}(v)=\max_c p(c\mid v)
$$

要求 coarse-specific item/token 的平均 concentration 明显高于 common item/token。

---

### Check 3: Fine signature words / tokens

对每个 word/phrase item 和 tokenizer 后 token 分别计算：

$$
p(f\mid v)
=\frac{n(v,f)}{\sum_{f'} n(v,f')}
$$

定义 fine concentration：

$$
C_{\text{fine}}(v)=\max_f p(f\mid v)
$$

要求 fine-specific item/token 的 concentration 最高。

---

### Check 4: 层级结构可识别

用简单统计分类器预测：

1. document coarse label；
2. document fine label。

如果只看 item/token counts 就完全无法预测 coarse / fine，说明数据太弱。

如果预测太容易，说明任务可能太简单。

第一版目标：

```text
coarse prediction accuracy > 80%
fine prediction accuracy > 60%
```

---

### Check 5: Prefix-level 可识别性

因为 NTP 模型不是一次性看到完整 document，需要检查不同 prefix 长度下是否已经有足够层级信号：

```text
prefix_len = 16 / 32 / 64 / 128
report coarse accuracy
report fine accuracy
```

如果只有完整 128 tokens 才能预测 fine，说明前缀信号太弱；如果 16 tokens 就接近 100%，说明任务可能太简单。

---

### Check 6: Template shortcut 检查

训练一个只使用 `template_id` 或模板位置特征的分类器预测 coarse / fine：

```text
template-only coarse accuracy
template-only fine accuracy
```

要求 template-only classifier 不能接近 item/token-count classifier。否则说明模型可能通过句式 shortcut 学到标签，而不是通过 common / coarse / fine 词短语结构学习。

---

### Check 7: Expert advantage 评估接口

数据集本身需要支持后续 expert advantage 评估：

```text
selected_expert_loss < alternative_expert_loss
```

必须能按以下分桶报告：

```text
common-source tokens
coarse-source tokens
fine-source tokens
rare-frequency tokens
```

如果只看到 router recovery，而 expert advantage 不为正，则只能说明 route 与标签相关，不能说明 expert 已经形成专一功能。

---

## 8. 第一版参数

```yaml
base_inventory:
  tokenizer: Qwen3-0.6B tokenizer
  common_words_phrases_from: DCLM high-frequency text
  domain_style_words_phrases_from: WoS mid/low-frequency text

text_generation:
  mode: template-based natural text
  template_slots: [common, coarse, fine]
  output_text: true
  templates_per_coarse: 8
  templates_per_fine: 4
  optional_clause_prob: 0.30
  sentence_shuffle: true
  slot_position_shuffle: true

synthetic_structure:
  num_coarse: 4
  fine_per_coarse: 4
  num_fine: 16
  sequence_length: 128

word_phrase_pools:
  common_pool_size: 512
  coarse_pool_size_per_coarse: 256
  fine_pool_size_per_fine: 128

zipf:
  alpha: 1.0

mixture:
  rho_common: 0.60
  rho_coarse: 0.25
  rho_fine: 0.15

overlap_noise:
  coarse_overlap_rate: 0.10
  fine_overlap_rate: 0.15
  background_noise_rate: 0.05
  max_signature_concentration_target: 0.85

splits:
  train_docs: 50000
  valid_docs: 2000
  test_docs: 5000
```

---

## 9. 预期结果如何更新假设

### 如果数据满足 Zipfian 且 hierarchy 可识别

可以进入模型训练。

### 如果数据不满足 Zipfian

先修数据生成，不训练模型。

### 如果 Zipfian 成立但 coarse/fine 不可识别

说明 hierarchy signal 太弱，需要提高：

$$
\rho_{\text{coarse}},\rho_{\text{fine}}
$$

或增加 signature word/phrase pool 的区分度。

### 如果数据太容易

降低：

$$
\rho_{\text{coarse}},\rho_{\text{fine}}
$$

或者增加 common slot 占比、增加 shared / overlap phrase、增加模板多样性。

### 如果 template-only classifier 太强

说明模板本身泄漏 coarse / fine label，需要增加跨类别共享模板、随机化 slot 位置，并减少某些模板和特定 label 的一一对应。

### 如果 router recovery 强但 expert advantage 不强

说明模型可能只学到了 label-correlated routing，没有学出真正 expert specialization。此时不能用该结果支持 Hierarchical MoE 的功能分工，需要调整训练目标、expert 容量或数据难度。
