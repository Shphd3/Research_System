# R01 measured sample cards

Source: `runs/combination/P_29_balanced_U/test.json`, frozen `data/dataset.json`, acquisition final evaluations and `analysis/positive_29.json` in the execution root. The script chooses the first correct and first incorrect TEST row by stored order, without optimizing their appearance. Native next-token predictions use the full vocabulary.

### correct: seed29, dataset row763, C1:3:7:t0

Prompt: `先执行 F1，再执行 G3。输入：狗。答案：`. Input 狗; F1 maps it to 猫; G3 maps that to 黄. Target 黄; actual single-forward prediction 黄. This row is TEST, never taught for this pair-input mapping. Atomic original-format P is100% across all256 rows, so the two explicit atomic calls execute this chain correctly. The combination prediction is directly observed; the external chain is the label derivation, not a traced neural computation.


### failed: seed29, dataset row538, C0:0:0:t0

Prompt: `先执行 F0，再执行 G0。输入：红。答案：`. Input 红; F0 maps it to 蓝; G0 maps that to 红. Target 红; actual single-forward prediction 鹿. This row is TEST, never taught for this pair-input mapping. Atomic original-format P is100% across all256 rows, so the two explicit atomic calls execute this chain correctly. The combination prediction is directly observed; the external chain is the label derivation, not a traced neural computation.


These cards explain how task meaning corresponds to actual predictions. A correct row is not proof of composition reuse; a wrong row is not a general impossibility result. The full96 rows and all three seeds, not these selected illustrations, determine the reported metrics.
