# C_A0_baseline_check

AI分析；研究者判断Unknown。Nearbyinterpolationonly;exact0.5B A0weightsabsent. Compatibilityisnotbitwiseequivalence,checkpointboundarytruncationdiffers.

|   baseline_tokens |   baseline_step |   baseline_NLL |   A0_logstep_interpolated_NLL |    difference |   tolerance | nearby_compatible   | exact_same_token_checkpoint   |
|------------------:|----------------:|---------------:|------------------------------:|--------------:|------------:|:--------------------|:------------------------------|
|         500000000 |            1908 |        4.11293 |                      4.111956 | -0.0009738656 |        0.01 | True                | False                         |
