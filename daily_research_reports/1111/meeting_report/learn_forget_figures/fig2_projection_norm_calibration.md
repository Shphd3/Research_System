# fig2_projection_norm_calibration

AI分析；研究者判断Unknown。Exactgradientnorm2 versus CountSketchnorm2; normagreement does not certify everynear-zero cross-group innerproduct sign.

| case           | model   |      tokens | block     |   min_sketch_to_exact_norm2 |   max_sketch_to_exact_norm2 |   mean_sketch_to_exact_norm2 |
|:---------------|:--------|------------:|:----------|----------------------------:|----------------------------:|-----------------------------:|
| registered1seq | Dense   | 10000000000 | FFN       |                   0.9962402 |                    1.00279  |                    1.000092  |
| registered1seq | Dense   | 10000000000 | attention |                   0.9971696 |                    1.002763 |                    0.9999381 |
| registered1seq | Dense   |  1000000000 | FFN       |                   0.9964549 |                    1.002194 |                    0.9998738 |
| registered1seq | Dense   |  1000000000 | attention |                   0.9959066 |                    1.002866 |                    0.9997599 |
| registered1seq | MoE     | 10000000000 | attention |                   0.9970738 |                    1.003258 |                    1.000031  |
| registered1seq | MoE     | 10000000000 | expert    |                   0.9979106 |                    1.004164 |                    1.000233  |
| registered1seq | MoE     |  1000000000 | attention |                   0.9960725 |                    1.003472 |                    1.000018  |
| registered1seq | MoE     |  1000000000 | expert    |                   0.9969077 |                    1.002736 |                    1.000087  |
| precision8seq  | Dense   | 10000000000 | FFN       |                   0.997251  |                    1.002572 |                    0.9999043 |
| precision8seq  | Dense   | 10000000000 | attention |                   0.9978168 |                    1.002369 |                    0.9999309 |
| precision8seq  | Dense   |  1000000000 | FFN       |                   0.9967119 |                    1.002566 |                    0.9996789 |
| precision8seq  | Dense   |  1000000000 | attention |                   0.9972716 |                    1.002903 |                    0.9997057 |
| precision8seq  | MoE     | 10000000000 | attention |                   0.9970371 |                    1.003535 |                    0.9999615 |
| precision8seq  | MoE     | 10000000000 | expert    |                   0.9970481 |                    1.002429 |                    0.9998676 |
| precision8seq  | MoE     |  1000000000 | attention |                   0.9971217 |                    1.00313  |                    1.000055  |
| precision8seq  | MoE     |  1000000000 | expert    |                   0.9978031 |                    1.002201 |                    1.000061  |
