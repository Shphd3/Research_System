# fig3_frontier

AI分析；研究者判断Unknown。Heuristic feasible objective values give lower bounds on best attainable DEV objectives; EVAL generalization may violate the DEVload cap. 4 is an upper bound only under uniform global expert load.

| label     |   lambda_value |       DEV_J |   selected_start |   selected_round |   DEV_max_load |   DEV_feasible |      EVAL_J |   low_M_median |   high_M_median |   overall_M_median |   EVAL_max_load | kind                     |
|:----------|---------------:|------------:|-----------------:|-----------------:|---------------:|---------------:|------------:|---------------:|----------------:|-------------------:|----------------:|:-------------------------|
| lambda0   |           0    |   0.3294604 |                2 |               30 |       1.191727 |              1 |   0.3250539 |      1.18432   |       1.559471  |          1.368293  |        1.27116  | optimized_binary_support |
| lambda025 |           0.25 |   0.3231549 |                1 |               30 |       1.193771 |              1 |   0.3366704 |      1.703409  |       1.618296  |          1.654442  |        1.256695 | optimized_binary_support |
| lambda05  |           0.5  |   0.3933425 |                0 |               30 |       1.161324 |              1 |   0.4175191 |      1.84422   |       1.597998  |          1.649032  |        1.216429 | optimized_binary_support |
| lambda075 |           0.75 |   0.5314714 |                3 |               27 |       1.175823 |              1 |   0.5646408 |      2.185972  |       1.328046  |          1.648102  |        1.246969 | optimized_binary_support |
| lambda1   |           1    |   1.119713  |                3 |               29 |       1.90736  |              0 |   1.039781  |      3.106175  |       0.4556024 |          0.6440971 |        1.773422 | optimized_binary_support |
| equal     |         nan    |   0.4225985 |                0 |               21 |       1.198915 |              1 |   0.4390473 |      1.930807  |       1.611283  |          1.775444  |        1.257957 | optimized_binary_support |
| A2        |         nan    | nan         |              nan |              nan |     nan        |            nan | nan         |      0.2569898 |       0.2505744 |          0.2520347 |      nan        | actual_trained_route     |
| A0        |         nan    | nan         |              nan |              nan |     nan        |            nan | nan         |      1.133037  |       0.7958827 |          1.024844  |      nan        | actual_trained_route     |
| A5        |         nan    | nan         |              nan |              nan |     nan        |            nan | nan         |      1.374499  |       1.220189  |          1.363952  |      nan        | actual_trained_route     |
| A8        |         nan    | nan         |              nan |              nan |     nan        |            nan | nan         |      1.226535  |       0.9318507 |          1.128547  |      nan        | actual_trained_route     |
| A9d       |         nan    | nan         |              nan |              nan |     nan        |            nan | nan         |      1.194947  |       0.7474543 |          1.056258  |      nan        | actual_trained_route     |
