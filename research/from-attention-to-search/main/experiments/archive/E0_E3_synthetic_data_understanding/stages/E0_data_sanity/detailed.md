# Detailed Result: E0 Data Sanity

## Run

Workspace:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments
```

Commands:

```bash
python active/synthetic_data_understanding/scripts/generate_synthetic_patterns.py \
  --config active/synthetic_data_understanding/configs/e0_synthetic_data_sanity.json \
  --out-dir active/synthetic_data_understanding/data

python active/synthetic_data_understanding/scripts/audit_synthetic_patterns.py \
  --config active/synthetic_data_understanding/configs/e0_synthetic_data_sanity.json \
  --data-dir active/synthetic_data_understanding/data \
  --out-dir active/synthetic_data_understanding/outputs \
  --fig-dir active/synthetic_data_understanding/figures
```

Artifacts:

```text
active/synthetic_data_understanding/outputs/data_audit.json
active/synthetic_data_understanding/outputs/feature_count_table.csv
active/synthetic_data_understanding/outputs/conditional_probability_table.csv
active/synthetic_data_understanding/outputs/rank_frequency.csv
active/synthetic_data_understanding/figures/rank_frequency.png
```

## Key Figure

```text
figures/rank_frequency.png
```

![Rank frequency](figures/rank_frequency.png)

This figure supports only the dataset-construction claim: the planted features
follow the intended long-tail order. It does not show model learning.

## Intuitive Generated Data Example

Token windows around planted features:

```text
AB  [1,2]
tokens: 0 2 1 99 27 1 2 79 41 39 60 67
text:   云 跑步 小明 词99 词27 小明 跑步 词79 词41 词39 词60 词67

CDE [3,4,5]
tokens: 78 80 90 72 47 3 4 5 47 52 85 40 11
text:   词78 词80 词90 词72 词47 天气 很 好 词47 词52 词85 词40 苹果

FG  [6,7]
tokens: 59 5 91 4 48 6 7 68 27 10 59 42
text:   词59 好 词91 很 词48 猫 睡觉 词68 词27 河流 词59 词42

HI  [8,9]
tokens: 13 42 22 61 75 8 9 52 43 47 41 92
text:   蓝色 词42 词22 词61 词75 老师 讲课 词52 词43 词47 词41 词92
```

The natural-language words are only a visualization. The real experiment is on
token IDs and context relations.

## Target Feature Map

| Feature | Token relation | Naturalized relation |
|---|---|---|
| AB | `[1] -> [2]` | 小明 -> 跑步 |
| CDE | `[3,4] -> [5]` | 天气 很 -> 好 |
| FG | `[6] -> [7]` | 猫 -> 睡觉 |
| HI | `[8] -> [9]` | 老师 -> 讲课 |

## Collision Reading

For bigrams, random background collision is approximately $N/V^2=100$.
Therefore AB can tolerate this because it is planted 10000 times, but HI with
target count 100 is not clean under collision logging.
