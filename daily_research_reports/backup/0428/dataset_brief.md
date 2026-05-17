# Dataset Brief: Synthetic Natural Zipfian Hierarchy

## 一句话说明

本实验使用的是自构造的 synthetic natural text dataset：文本像科研短文，但每条 document 的生成层级是已知的，用来测试模型能否学习 `common -> coarse -> fine` 的层级结构。

## 构造方式

每条 document 先选一个 `coarse_label`，再在该 coarse 下选一个 `fine_label`。随后从三类 phrase pool 中抽取短语并填入自然语言模板：

- `common`：跨领域通用短语，例如 `study`, `method`, `baseline process`
- `coarse`：大领域相关短语，例如 computing 里的 `algorithm`, `memory cache`
- `fine`：细主题相关短语，例如 network_security 里的 `packet trace`, `intrusion event`

Zipfian 控制的是 word / phrase / token 的出现频率，不是类别采样频率。类别本身保持均匀。

## 数据规模

Formal v1 使用的数据规模：

| split | documents | seq_len | label tokens |
|---|---:|---:|---:|
| train | 20000 | 128 | 2560000 |
| valid | 1000 | 128 | 128000 |
| test | 1000 | 128 | 128000 |

Phrase pool 规模：

| pool | count |
|---|---:|
| common phrase types | 512 |
| coarse phrase types | 4 x 256 = 1024 |
| fine phrase types | 16 x 128 = 2048 |
| total phrase types | 3584 |

## Label 定义

`coarse_label` 有 4 类：

| id | name |
|---:|---|
| 0 | biomedicine |
| 1 | computing |
| 2 | materials |
| 3 | climate |

`fine_label` 有 16 类，每个 coarse 下 4 类：

| id | coarse | fine name |
|---:|---|---|
| 0 | biomedicine | cell_signaling |
| 1 | biomedicine | clinical_trial |
| 2 | biomedicine | genomics |
| 3 | biomedicine | immunology |
| 4 | computing | optimization |
| 5 | computing | language_modeling |
| 6 | computing | network_security |
| 7 | computing | robotics |
| 8 | materials | alloy_design |
| 9 | materials | crystal_growth |
| 10 | materials | polymer_film |
| 11 | materials | battery_interface |
| 12 | climate | carbon_cycle |
| 13 | climate | hydrology |
| 14 | climate | urban_heat |
| 15 | climate | biodiversity |

Formal train split 中 `coarse_label` 完全均匀：每类 5000 条。`fine_label` 也完全均匀：每类 1250 条。

Formal train split 的 label 数量：

| label level | classes | docs per class | total docs |
|---|---:|---:|---:|
| coarse_label | 4 | 5000 | 20000 |
| fine_label | 16 | 1250 | 20000 |

## 数据样式

示例：`coarse_label=1 computing`，`fine_label=6 network_security`。

```text
This study tracks the algorithm, while the intrusion event marks the local response.
Researchers noted that the systematic study altered the packet trace during the adaptive algorithm.
The observed rare threat signature supports a method for the broader observational training system.
```

这类文本包含：

- `common` signal：`study`, `method`
- `coarse` signal：`algorithm`, `training system`
- `fine` signal：`intrusion event`, `packet trace`, `threat signature`

## Sanity 结果

Formal data sanity 通过：

- word/phrase Zipf alpha = 1.052, R2 = 0.974
- token-id Zipf alpha = 1.014, R2 = 0.933
- template-only shortcut 很低：coarse accuracy = 0.254, fine accuracy = 0.064

Formal train split 的 token annotation 数量：

| token annotation | count |
|---|---:|
| token_source = common | 1802463 |
| token_source = coarse | 365093 |
| token_source = fine | 392444 |
| token_frequency_bucket = common | 1723919 |
| token_frequency_bucket = middle | 639305 |
| token_frequency_bucket = rare | 196776 |

因此，这个数据集的关键性质是：类别均匀，但词/短语/token 频率呈 Zipfian 长尾分布。
