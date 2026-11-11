# M2_offline_reference

AI分析；研究者判断Unknown。这两行均EVAL频率口径；原1.78未满足EVAL负载<=1.2；校准1.762非独立验证。

| label   |   overall_M_median |   EVAL_max_load | condition                         |
|:--------|-------------------:|----------------:|:----------------------------------|
| equal   |           1.775444 |        1.257957 | DEV拟合A与bias，EVAL冻结          |
| equal   |           1.761726 |        1.161573 | 固定A，仅EVAL边缘负载转导校准bias |
