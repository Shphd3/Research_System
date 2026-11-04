# 自然题干补充：完整核验表

S08每源257文档、8位置/篇；每个A内、B内、跨A/B均32896个不同文档对。统计单位为文档，Jaccard仅用0/1激活成员。Magicoder-OSS75K problem(train)、GSM8K question(train)、MMLU question(test)。

| SAE | A／B | A内 | B内 | 跨A/B |
|---|---|---:|---:|---:|
| ATTN_SAE | Magicoder／GSM8K | 0.035082 | 0.017114 | 0.012173 |
| ATTN_SAE | Magicoder／MMLU | 0.035082 | 0.025634 | 0.020589 |
| ATTN_SAE | GSM8K／MMLU | 0.017114 | 0.025634 | 0.011792 |
| MLPIN_SAE | Magicoder／GSM8K | 0.118729 | 0.096840 | 0.062736 |
| MLPIN_SAE | Magicoder／MMLU | 0.118729 | 0.079592 | 0.070730 |
| MLPIN_SAE | GSM8K／MMLU | 0.096840 | 0.079592 | 0.062030 |

S09严格边际零模型用新固定的128发现／129留出，而不是S08全部257样本的同一估计。以下比值均为新留出“平均内部−跨来源”参照差/真实差。

| SAE | A／B | 实测差 | 固定次数+32参照差 | 比值 |
|---|---|---:|---:|---:|
| ATTN_SAE | Magicoder／GSM8K | 0.014126 | 0.013297 | 94.1% |
| ATTN_SAE | Magicoder／MMLU | 0.010565 | 0.008760 | 82.9% |
| ATTN_SAE | GSM8K／MMLU | 0.009900 | 0.008845 | 89.3% |
| MLPIN_SAE | Magicoder／GSM8K | 0.046637 | 0.045240 | 97.0% |
| MLPIN_SAE | Magicoder／MMLU | 0.029533 | 0.027332 | 92.5% |
| MLPIN_SAE | GSM8K／MMLU | 0.026308 | 0.025209 | 95.8% |

该参照按各来源、分位分别保留次数，未把不同来源改成相同频率；比值不代表因果解释率。5/6个真实减参照的剩余差区间跨0，详原S09。S09共同激活检验已经完成，本页没有将其写成未执行的新任务，完整结果保留在其原Summary。
