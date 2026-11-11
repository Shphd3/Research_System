# F_evidence_lineage

AI分析；研究者判断Unknown。

| claim                       | criterion          | raw                                                       | producer                                                  | eligibility         | limit                                                  |
|:----------------------------|:-------------------|:----------------------------------------------------------|:----------------------------------------------------------|:--------------------|:-------------------------------------------------------|
| A8 manipulation andbenefit  | P5/P6              | B_M_medians.csv;A_bootstrap_differences.csv               | analysis/finalize.py                                      | bounded as recorded | M is external geometry;single seed                     |
| Selfbenefit andearlylayers  | P7/P9              | A_learning.csv;A_bootstrap_differences.csv                | analysis/finalize.py                                      | bounded as recorded | 1000newupdates;crosshardware native training reference |
| Switch association          | P8                 | D_switch_correlations.csv;D_switch_quartiles.csv          | analysis/finalize.py                                      | bounded as recorded | Gate,bias,groupchoices jointlychange                   |
| Concentration decomposition | descriptive        | F_concentration_bands.csv;F_concentration_layers.csv      | analysis/final_supplement.py                              | bounded as recorded | Exact algebra,not independent intervention             |
| Learning/forgetting         | R04fixedthresholds | C_ledger_by_bin.csv;F_matched_learning.csv                | analysis/finalize.py;analysis/final_supplement.py         | bounded as recorded | Overlapping atoms;post-switch history differs          |
| Retainedstates              | execution          | evidence/saved_A8.json;saved_A9.json;saved_A9d.json       | analysis/finalize_records.py                              | bounded as recorded | Fullstate versusBF16 snapshots separated               |
| Runtimecontrol              | secondary          | runtime_forward_difference.csv;runtime_sensitivity_CI.csv | analysis/forward_reference_5090.py;runtime_sensitivity.py | bounded as recorded | Forwardonly;no native5090training                      |
