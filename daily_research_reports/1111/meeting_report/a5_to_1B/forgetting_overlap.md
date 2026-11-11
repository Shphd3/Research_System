# forgetting_overlap

AI分析；研究者判断 Unknown。P12 original-baseline update2000 was not saved. R03 A0 proxy uses full batches instead of historical baseline partial masks; native exact-trajectory P12 remains insufficient. Interval1000steps versus1816steps is also a confound.

| period      | arm_a   | arm_b              |   forgotten_a |   forgotten_b |   intersection |   union |    Jaccard | eligibility                                                        |
|:------------|:--------|:-------------------|--------------:|--------------:|---------------:|--------:|-----------:|:-------------------------------------------------------------------|
| 1000_to2000 | A0      | A1                 |           212 |           181 |            151 |     242 | 0.62396694 | historical_matched_window                                          |
| 1000_to2000 | A0      | A2                 |           212 |           130 |            126 |     216 | 0.58333333 | historical_matched_window                                          |
| 1000_to2000 | A0      | A4                 |           212 |           212 |            171 |     253 | 0.67588933 | historical_matched_window                                          |
| 1000_to2000 | A0      | A1-deep            |           212 |           171 |            154 |     229 | 0.67248908 | historical_matched_window                                          |
| 1000_to2000 | A0      | A5                 |           212 |           199 |            159 |     252 | 0.63095238 | historical_matched_window                                          |
| 1000_to2000 | A0      | A6                 |           212 |           133 |            124 |     221 | 0.56108597 | historical_matched_window                                          |
| 1000_to2000 | A1      | A2                 |           181 |           130 |            124 |     187 | 0.6631016  | historical_matched_window                                          |
| 1000_to2000 | A1      | A4                 |           181 |           212 |            158 |     235 | 0.67234043 | historical_matched_window                                          |
| 1000_to2000 | A1      | A1-deep            |           181 |           171 |            137 |     215 | 0.6372093  | historical_matched_window                                          |
| 1000_to2000 | A1      | A5                 |           181 |           199 |            144 |     236 | 0.61016949 | historical_matched_window                                          |
| 1000_to2000 | A1      | A6                 |           181 |           133 |            123 |     191 | 0.64397906 | historical_matched_window                                          |
| 1000_to2000 | A2      | A4                 |           130 |           212 |            127 |     215 | 0.59069767 | historical_matched_window                                          |
| 1000_to2000 | A2      | A1-deep            |           130 |           171 |            114 |     187 | 0.60962567 | historical_matched_window                                          |
| 1000_to2000 | A2      | A5                 |           130 |           199 |            118 |     211 | 0.55924171 | historical_matched_window                                          |
| 1000_to2000 | A2      | A6                 |           130 |           133 |            107 |     156 | 0.68589744 | historical_matched_window                                          |
| 1000_to2000 | A4      | A1-deep            |           212 |           171 |            151 |     232 | 0.65086207 | historical_matched_window                                          |
| 1000_to2000 | A4      | A5                 |           212 |           199 |            158 |     253 | 0.62450593 | historical_matched_window                                          |
| 1000_to2000 | A4      | A6                 |           212 |           133 |            124 |     221 | 0.56108597 | historical_matched_window                                          |
| 1000_to2000 | A1-deep | A5                 |           171 |           199 |            144 |     226 | 0.63716814 | historical_matched_window                                          |
| 1000_to2000 | A1-deep | A6                 |           171 |           133 |            119 |     185 | 0.64324324 | historical_matched_window                                          |
| 1000_to2000 | A5      | A6                 |           199 |           133 |            122 |     210 | 0.58095238 | historical_matched_window                                          |
| 2000_to3816 | A5      | MoE_baseline_proxy |            27 |            14 |              9 |      32 | 0.28125    | EXPLORATORY_R03_A0_start_proxy; original baseline2000state_missing |
