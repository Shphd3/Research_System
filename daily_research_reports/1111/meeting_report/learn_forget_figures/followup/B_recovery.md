# B_recovery

AI分析；研究者判断Unknown。

| model   | reference    |   shared_features |   loss_recovered_features |   loss_recovered_fraction |   significant_5to10_improvement_features |   state_forgotten_positions_feature_occurrences |   state_recovered_occurrences |   state_recovered_fraction |
|:--------|:-------------|------------------:|--------------------------:|--------------------------:|-----------------------------------------:|------------------------------------------------:|------------------------------:|---------------------------:|
| Dense   | MoE33B       |              3169 |                       680 |                 0.2145787 |                                     2899 |                                          192103 |                         38509 |                  0.2004602 |
| Dense   | Dense_latest |              3169 |                       680 |                 0.2145787 |                                     2899 |                                           68779 |                         28516 |                  0.4146033 |
| MoE     | MoE33B       |              3169 |                       791 |                 0.2496056 |                                     2990 |                                          201285 |                         48827 |                  0.2425765 |
| MoE     | Dense_latest |              3169 |                       791 |                 0.2496056 |                                     2990 |                                           57412 |                         27936 |                  0.4865882 |
