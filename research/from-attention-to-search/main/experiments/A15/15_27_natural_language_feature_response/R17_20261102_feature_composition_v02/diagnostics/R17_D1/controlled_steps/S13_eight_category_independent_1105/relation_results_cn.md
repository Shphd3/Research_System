# S13固定关系全条件结果

所有已选、覆盖不足、反向和未决保留；每行48家族／16场景簇，数值pp为百分点。区间对零模型中心条件化；不包括另一批独立语料或训练随机性的外推。MLP无开发猫狗迁移边，迁移NOT RUN，不是失败验证。

## 同父细类类别差

| SAE | 表述 | 对 | 边 | 中心支持A/B | 原始条件差pp | 参照差pp | 超额差pp / 95%CI | 判定 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Attention输出 | 显式类别名 | cat→dog | 9117→5567 | 8/14 | +0.00 | +4.61 | -4.61 [-4.61, -4.61] | INSUFFICIENT |
| Attention输出 | 显式类别名 | car→bicycle | 9270→2254 | 12/16 | -6.25 | -8.06 | +1.81 [-25.06, 20.32] | UNRESOLVED |
| Attention输出 | 显式类别名 | apple→banana | 9270→2254 | 14/26 | +13.74 | +0.09 | +13.64 [-0.09, 30.86] | UNRESOLVED |
| Attention输出 | 显式类别名 | shirt→trousers | 26542→9785 | 11/20 | -8.64 | -7.97 | -0.66 [-33.84, 27.42] | UNRESOLVED |
| Attention输出 | 显式类别名 | piano→guitar | 9270→20439 | 20/17 | +9.71 | -2.11 | +11.81 [-4.20, 32.79] | UNRESOLVED |
| Attention输出 | 显式类别名 | spoon→fork | 9270→2254 | 8/8 | +12.50 | -4.50 | +17.00 [-20.50, 54.50] | INSUFFICIENT |
| Attention输出 | 保留类别名改写 | cat→dog | 9117→5567 | 13/21 | +13.55 | +9.19 | +4.36 [-9.19, 25.43] | UNRESOLVED |
| Attention输出 | 保留类别名改写 | car→bicycle | 9270→2254 | 18/23 | +15.22 | -8.57 | +23.79 [13.15, 35.33] | UNRESOLVED |
| Attention输出 | 保留类别名改写 | apple→banana | 9270→2254 | 16/27 | +16.44 | +0.21 | +16.23 [-7.10, 35.37] | UNRESOLVED |
| Attention输出 | 保留类别名改写 | shirt→trousers | 26542→9785 | 5/14 | -4.29 | +5.80 | -10.08 [-65.12, 19.20] | INSUFFICIENT |
| Attention输出 | 保留类别名改写 | piano→guitar | 9270→20439 | 20/22 | -4.09 | +4.25 | -8.34 [-24.61, 8.38] | UNRESOLVED |
| Attention输出 | 保留类别名改写 | spoon→fork | 9270→2254 | 6/6 | +33.33 | +1.90 | +31.43 [-1.90, 73.10] | INSUFFICIENT |
| Attention输出 | 无类别名属性 | cat→dog | 9117→5567 | 5/7 | -28.57 | -16.96 | -11.61 [-40.18, 16.96] | INSUFFICIENT |
| Attention输出 | 无类别名属性 | car→bicycle | 9270→2254 | 1/2 | +0.00 | -20.80 | +20.80 [20.80, 20.80] | INSUFFICIENT |
| Attention输出 | 无类别名属性 | apple→banana | 9270→2254 | 14/27 | +6.61 | +6.03 | +0.59 [-21.41, 22.28] | UNRESOLVED |
| Attention输出 | 无类别名属性 | shirt→trousers | 26542→9785 | 14/17 | +0.00 | -0.04 | +0.04 [0.04, 0.04] | UNRESOLVED |
| Attention输出 | 无类别名属性 | piano→guitar | 9270→20439 | 20/23 | +11.52 | +12.71 | -1.19 [-30.42, 32.29] | UNRESOLVED |
| Attention输出 | 无类别名属性 | spoon→fork | 9270→2254 | 20/13 | +16.54 | -4.16 | +20.69 [-7.46, 43.05] | UNRESOLVED |
| Attention输出 | 无类别名情境 | cat→dog | 9117→5567 | 1/7 | +85.71 | -4.95 | +90.66 [64.95, 104.95] | INSUFFICIENT |
| Attention输出 | 无类别名情境 | car→bicycle | 9270→2254 | 5/1 | -60.00 | -13.49 | -46.51 [-72.23, 13.49] | INSUFFICIENT |
| Attention输出 | 无类别名情境 | apple→banana | 9270→2254 | 13/23 | -14.05 | +14.94 | -28.99 [-51.79, -6.19] | UNRESOLVED |
| Attention输出 | 无类别名情境 | shirt→trousers | 26542→9785 | 22/21 | +24.46 | +10.26 | +14.20 [-1.93, 34.98] | UNRESOLVED |
| Attention输出 | 无类别名情境 | piano→guitar | 9270→20439 | 16/16 | +12.50 | +4.61 | +7.89 [-14.61, 33.85] | UNRESOLVED |
| Attention输出 | 无类别名情境 | spoon→fork | 9270→2254 | 14/21 | +2.38 | -10.43 | +12.81 [-6.49, 34.54] | UNRESOLVED |
| MLP输入 | 显式类别名 | chair→sofa | 416→5196 | 10/3 | +0.00 | -33.22 | +33.22 [33.22, 33.22] | INSUFFICIENT |
| MLP输入 | 显式类别名 | shirt→trousers | 28550→966 | 20/22 | -3.64 | -4.14 | +0.50 [-19.19, 16.64] | UNRESOLVED |
| MLP输入 | 显式类别名 | piano→guitar | 416→14913 | 8/15 | +27.50 | +6.02 | +21.48 [-6.04, 57.62] | INSUFFICIENT |
| MLP输入 | 显式类别名 | rose→tulip | 416→17390 | 7/6 | +0.00 | -2.37 | +2.37 [2.37, 2.37] | INSUFFICIENT |
| MLP输入 | 显式类别名 | spoon→fork | 416→17390 | 4/17 | +0.00 | +0.18 | -0.18 [-0.18, -0.18] | INSUFFICIENT |
| MLP输入 | 保留类别名改写 | chair→sofa | 416→5196 | 7/4 | -32.14 | -45.48 | +13.34 [-54.52, 72.15] | INSUFFICIENT |
| MLP输入 | 保留类别名改写 | shirt→trousers | 28550→966 | 26/27 | -3.42 | -6.26 | +2.84 [-8.26, 14.99] | UNRESOLVED |
| MLP输入 | 保留类别名改写 | piano→guitar | 416→14913 | 5/14 | +22.86 | +8.66 | +14.19 [-42.00, 48.95] | INSUFFICIENT |
| MLP输入 | 保留类别名改写 | rose→tulip | 416→17390 | 7/5 | +0.00 | -1.93 | +1.93 [1.93, 1.93] | INSUFFICIENT |
| MLP输入 | 保留类别名改写 | spoon→fork | 416→17390 | 3/15 | +0.00 | -0.20 | +0.20 [0.20, 0.20] | INSUFFICIENT |
| MLP输入 | 无类别名属性 | chair→sofa | 416→5196 | 21/15 | -3.81 | -17.02 | +13.21 [-10.30, 35.21] | UNRESOLVED |
| MLP输入 | 无类别名属性 | shirt→trousers | 28550→966 | 20/18 | -6.11 | -4.23 | -1.88 [-16.83, 4.23] | UNRESOLVED |
| MLP输入 | 无类别名属性 | piano→guitar | 416→14913 | 15/14 | +0.95 | -10.24 | +11.19 [-12.98, 39.48] | UNRESOLVED |
| MLP输入 | 无类别名属性 | rose→tulip | 416→17390 | 5/7 | +0.00 | +0.34 | -0.34 [-0.34, -0.34] | INSUFFICIENT |
| MLP输入 | 无类别名属性 | spoon→fork | 416→17390 | 9/8 | +0.00 | -2.16 | +2.16 [2.16, 2.16] | INSUFFICIENT |
| MLP输入 | 无类别名情境 | chair→sofa | 416→5196 | 14/14 | -14.29 | -21.08 | +6.79 [-15.29, 35.36] | UNRESOLVED |
| MLP输入 | 无类别名情境 | shirt→trousers | 28550→966 | 13/11 | -1.40 | -6.37 | +4.97 [-19.95, 28.59] | UNRESOLVED |
| MLP输入 | 无类别名情境 | piano→guitar | 416→14913 | 22/22 | -4.55 | +1.97 | -6.51 [-18.21, -0.19] | UNRESOLVED |
| MLP输入 | 无类别名情境 | rose→tulip | 416→17390 | 5/8 | +0.00 | +2.00 | -2.00 [-2.00, -2.00] | INSUFFICIENT |
| MLP输入 | 无类别名情境 | spoon→fork | 416→17390 | 4/7 | +0.00 | +0.28 | -0.28 [-0.28, -0.28] | INSUFFICIENT |


## 父子固定边（探索）

| SAE | 表述 | 对 | 边 | 中心支持A/B | 原始条件差pp | 参照差pp | 超额差pp / 95%CI | 判定 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Attention输出 | 显式类别名 | animal→cat | 9117→5567 | 7/8 | +0.00 | -9.12 | +9.12 [9.12, 9.12] | INSUFFICIENT |
| Attention输出 | 显式类别名 | animal→dog | 9117→5567 | 7/14 | +0.00 | -4.51 | +4.51 [4.51, 4.51] | INSUFFICIENT |
| Attention输出 | 显式类别名 | vehicle→car | 9270→2254 | 3/12 | +8.33 | +3.86 | +4.47 [-28.42, 66.14] | INSUFFICIENT |
| Attention输出 | 显式类别名 | vehicle→bicycle | 9270→2254 | 3/16 | +2.08 | -4.20 | +6.28 [-35.80, 64.98] | INSUFFICIENT |
| Attention输出 | 显式类别名 | fruit→apple | 9270→2254 | 15/14 | +5.24 | +4.15 | +1.09 [-9.71, 18.71] | UNRESOLVED |
| Attention输出 | 显式类别名 | fruit→banana | 9270→2254 | 15/26 | +18.97 | +4.24 | +14.73 [-4.24, 45.77] | UNRESOLVED |
| Attention输出 | 显式类别名 | clothing→shirt | 26542→9785 | 18/11 | +19.19 | +22.66 | -3.46 [-21.50, 18.77] | UNRESOLVED |
| Attention输出 | 显式类别名 | clothing→trousers | 26542→9785 | 18/20 | +10.56 | +14.68 | -4.13 [-30.07, 22.79] | UNRESOLVED |
| Attention输出 | 显式类别名 | instrument→piano | 9270→20439 | 21/20 | +7.38 | +14.53 | -7.15 [-24.53, 6.04] | UNRESOLVED |
| Attention输出 | 显式类别名 | instrument→guitar | 9270→20439 | 21/17 | +17.09 | +12.42 | +4.67 [-17.18, 24.09] | UNRESOLVED |
| Attention输出 | 显式类别名 | cutlery→spoon | 9270→2254 | 14/8 | -8.93 | -8.00 | -0.93 [-38.43, 46.46] | INSUFFICIENT |
| Attention输出 | 显式类别名 | cutlery→fork | 9270→2254 | 14/8 | +3.57 | -12.50 | +16.07 [-29.55, 55.36] | INSUFFICIENT |
| Attention输出 | 保留类别名改写 | animal→cat | 9117→5567 | 7/13 | -23.08 | -23.93 | +0.85 [-26.07, 23.93] | INSUFFICIENT |
| Attention输出 | 保留类别名改写 | animal→dog | 9117→5567 | 7/21 | -9.52 | -14.74 | +5.21 [-11.60, 14.74] | INSUFFICIENT |
| Attention输出 | 保留类别名改写 | vehicle→car | 9270→2254 | 5/18 | -10.00 | -1.09 | -8.91 [-48.91, 36.22] | INSUFFICIENT |
| Attention输出 | 保留类别名改写 | vehicle→bicycle | 9270→2254 | 5/23 | +5.22 | -9.66 | +14.88 [-23.67, 59.66] | INSUFFICIENT |
| Attention输出 | 保留类别名改写 | fruit→apple | 9270→2254 | 18/16 | -3.47 | +10.56 | -14.04 [-34.55, 10.87] | UNRESOLVED |
| Attention输出 | 保留类别名改写 | fruit→banana | 9270→2254 | 18/27 | +12.96 | +10.77 | +2.19 [-8.63, 17.87] | UNRESOLVED |
| Attention输出 | 保留类别名改写 | clothing→shirt | 26542→9785 | 9/5 | +6.67 | +2.47 | +4.20 [-27.47, 30.87] | INSUFFICIENT |
| Attention输出 | 保留类别名改写 | clothing→trousers | 26542→9785 | 9/14 | +2.38 | +8.26 | -5.88 [-30.76, 13.16] | INSUFFICIENT |
| Attention输出 | 保留类别名改写 | instrument→piano | 9270→20439 | 27/20 | +22.78 | +8.29 | +14.49 [-0.90, 34.82] | UNRESOLVED |
| Attention输出 | 保留类别名改写 | instrument→guitar | 9270→20439 | 27/22 | +18.69 | +12.54 | +6.15 [-9.73, 26.86] | UNRESOLVED |
| Attention输出 | 保留类别名改写 | cutlery→spoon | 9270→2254 | 18/6 | -55.56 | -1.62 | -53.93 [-82.65, -26.15] | INSUFFICIENT |
| Attention输出 | 保留类别名改写 | cutlery→fork | 9270→2254 | 18/6 | -22.22 | +0.28 | -22.50 [-66.95, 18.55] | INSUFFICIENT |
| Attention输出 | 无类别名属性 | animal→cat | 9117→5567 | 3/5 | +0.00 | -8.17 | +8.17 [8.17, 8.17] | INSUFFICIENT |
| Attention输出 | 无类别名属性 | animal→dog | 9117→5567 | 3/7 | -28.57 | -25.13 | -3.44 [-32.01, 25.13] | INSUFFICIENT |
| Attention输出 | 无类别名属性 | vehicle→car | 9270→2254 | 4/1 | +50.00 | +1.34 | +48.66 [-1.34, 78.66] | INSUFFICIENT |
| Attention输出 | 无类别名属性 | vehicle→bicycle | 9270→2254 | 4/2 | +50.00 | -19.46 | +69.46 [19.46, 119.46] | INSUFFICIENT |
| Attention输出 | 无类别名属性 | fruit→apple | 9270→2254 | 39/14 | +19.60 | -4.22 | +23.82 [7.39, 40.37] | UNRESOLVED |
| Attention输出 | 无类别名属性 | fruit→banana | 9270→2254 | 39/27 | +26.21 | +1.80 | +24.41 [11.53, 35.70] | CHANGE_DETECTED_EXPLORATORY |
| Attention输出 | 无类别名属性 | clothing→shirt | 26542→9785 | 13/14 | -7.69 | -8.11 | +0.42 [-13.32, 8.11] | UNRESOLVED |
| Attention输出 | 无类别名属性 | clothing→trousers | 26542→9785 | 13/17 | -7.69 | -8.15 | +0.46 [-13.27, 8.15] | UNRESOLVED |
| Attention输出 | 无类别名属性 | instrument→piano | 9270→20439 | 20/20 | +0.00 | -4.39 | +4.39 [-20.61, 32.02] | UNRESOLVED |
| Attention输出 | 无类别名属性 | instrument→guitar | 9270→20439 | 20/23 | +11.52 | +8.32 | +3.20 [-25.32, 33.75] | UNRESOLVED |
| Attention输出 | 无类别名属性 | cutlery→spoon | 9270→2254 | 5/20 | +25.00 | +6.01 | +18.99 [-22.68, 47.32] | INSUFFICIENT |
| Attention输出 | 无类别名属性 | cutlery→fork | 9270→2254 | 5/13 | +41.54 | +1.86 | +39.68 [-11.26, 75.92] | INSUFFICIENT |
| Attention输出 | 无类别名情境 | animal→cat | 9117→5567 | 4/1 | -100.00 | -6.85 | -93.15 [-93.15, -93.15] | INSUFFICIENT |
| Attention输出 | 无类别名情境 | animal→dog | 9117→5567 | 4/7 | -14.29 | -11.79 | -2.49 [-31.06, 11.79] | INSUFFICIENT |
| Attention输出 | 无类别名情境 | vehicle→car | 9270→2254 | 3/5 | -6.67 | -6.22 | -0.44 [-60.44, 56.22] | INSUFFICIENT |
| Attention输出 | 无类别名情境 | vehicle→bicycle | 9270→2254 | 3/1 | -66.67 | -19.71 | -46.96 [-80.29, 19.71] | INSUFFICIENT |
| Attention输出 | 无类别名情境 | fruit→apple | 9270→2254 | 24/13 | +13.14 | -9.03 | +22.17 [-1.01, 47.12] | UNRESOLVED |
| Attention输出 | 无类别名情境 | fruit→banana | 9270→2254 | 24/23 | -0.91 | +5.92 | -6.82 [-25.92, 11.47] | UNRESOLVED |
| Attention输出 | 无类别名情境 | clothing→shirt | 26542→9785 | 21/22 | -53.03 | -33.00 | -20.03 [-44.09, 2.71] | UNRESOLVED |
| Attention输出 | 无类别名情境 | clothing→trousers | 26542→9785 | 21/21 | -28.57 | -22.74 | -5.83 [-34.86, 23.34] | UNRESOLVED |
| Attention输出 | 无类别名情境 | instrument→piano | 9270→20439 | 27/16 | -27.78 | -13.18 | -14.60 [-32.53, 3.00] | UNRESOLVED |
| Attention输出 | 无类别名情境 | instrument→guitar | 9270→20439 | 27/16 | -15.28 | -8.57 | -6.70 [-30.00, 15.24] | UNRESOLVED |
| Attention输出 | 无类别名情境 | cutlery→spoon | 9270→2254 | 7/14 | +7.14 | +27.33 | -20.18 [-53.53, 9.60] | INSUFFICIENT |
| Attention输出 | 无类别名情境 | cutlery→fork | 9270→2254 | 7/21 | +9.52 | +16.89 | -7.37 [-30.44, 14.28] | INSUFFICIENT |
| MLP输入 | 显式类别名 | furniture→chair | 416→5196 | 2/10 | +0.00 | +17.49 | -17.49 [-17.49, -17.49] | INSUFFICIENT |
| MLP输入 | 显式类别名 | furniture→sofa | 416→5196 | 2/3 | +0.00 | -15.74 | +15.74 [15.74, 15.74] | INSUFFICIENT |
| MLP输入 | 显式类别名 | clothing→shirt | 28550→966 | 22/20 | -5.45 | -4.62 | -0.84 [-11.38, 4.62] | UNRESOLVED |
| MLP输入 | 显式类别名 | clothing→trousers | 28550→966 | 22/22 | -9.09 | -8.76 | -0.33 [-17.33, 8.76] | UNRESOLVED |
| MLP输入 | 显式类别名 | instrument→piano | 416→14913 | 6/8 | -4.17 | +4.55 | -8.72 [-19.57, -4.55] | INSUFFICIENT |
| MLP输入 | 显式类别名 | instrument→guitar | 416→14913 | 6/15 | +23.33 | +10.57 | +12.76 [-14.14, 53.07] | INSUFFICIENT |
| MLP输入 | 显式类别名 | flower→rose | 416→17390 | 5/7 | +0.00 | -1.91 | +1.91 [1.91, 1.91] | INSUFFICIENT |
| MLP输入 | 显式类别名 | flower→tulip | 416→17390 | 5/6 | +0.00 | -4.29 | +4.29 [4.29, 4.29] | INSUFFICIENT |
| MLP输入 | 显式类别名 | cutlery→spoon | 416→17390 | 2/4 | +0.00 | -2.16 | +2.16 [2.16, 2.16] | INSUFFICIENT |
| MLP输入 | 显式类别名 | cutlery→fork | 416→17390 | 2/17 | +0.00 | -1.98 | +1.98 [1.98, 1.98] | INSUFFICIENT |
| MLP输入 | 保留类别名改写 | furniture→chair | 416→5196 | 3/7 | +23.81 | +15.87 | +7.94 [-49.20, 64.13] | INSUFFICIENT |
| MLP输入 | 保留类别名改写 | furniture→sofa | 416→5196 | 3/4 | -8.33 | -29.61 | +21.28 [-20.39, 29.61] | INSUFFICIENT |
| MLP输入 | 保留类别名改写 | clothing→shirt | 28550→966 | 29/26 | -0.80 | -0.15 | -0.65 [-12.52, 9.20] | UNRESOLVED |
| MLP输入 | 保留类别名改写 | clothing→trousers | 28550→966 | 29/27 | -4.21 | -6.41 | +2.19 [-5.13, 6.41] | UNRESOLVED |
| MLP输入 | 保留类别名改写 | instrument→piano | 416→14913 | 5/5 | +0.00 | -2.59 | +2.59 [-57.41, 69.25] | INSUFFICIENT |
| MLP输入 | 保留类别名改写 | instrument→guitar | 416→14913 | 5/14 | +22.86 | +6.07 | +16.78 [-52.52, 60.59] | INSUFFICIENT |
| MLP输入 | 保留类别名改写 | flower→rose | 416→17390 | 6/7 | +0.00 | -2.25 | +2.25 [2.25, 2.25] | INSUFFICIENT |
| MLP输入 | 保留类别名改写 | flower→tulip | 416→17390 | 6/5 | +0.00 | -4.18 | +4.18 [4.18, 4.18] | INSUFFICIENT |
| MLP输入 | 保留类别名改写 | cutlery→spoon | 416→17390 | 2/3 | +0.00 | +0.31 | -0.31 [-0.31, -0.31] | INSUFFICIENT |
| MLP输入 | 保留类别名改写 | cutlery→fork | 416→17390 | 2/15 | +0.00 | +0.11 | -0.11 [-0.11, -0.11] | INSUFFICIENT |
| MLP输入 | 无类别名属性 | furniture→chair | 416→5196 | 14/21 | +47.62 | +57.12 | -9.50 [-40.71, 17.90] | UNRESOLVED |
| MLP输入 | 无类别名属性 | furniture→sofa | 416→5196 | 14/15 | +43.81 | +40.10 | +3.71 [-23.88, 29.38] | UNRESOLVED |
| MLP输入 | 无类别名属性 | clothing→shirt | 28550→966 | 23/20 | +3.70 | +10.34 | -6.64 [-11.67, 3.30] | UNRESOLVED |
| MLP输入 | 无类别名属性 | clothing→trousers | 28550→966 | 23/18 | -2.42 | +6.11 | -8.52 [-24.86, 4.61] | UNRESOLVED |
| MLP输入 | 无类别名属性 | instrument→piano | 416→14913 | 6/15 | -20.00 | -18.47 | -1.53 [-41.98, 35.13] | INSUFFICIENT |
| MLP输入 | 无类别名属性 | instrument→guitar | 416→14913 | 6/14 | -19.05 | -28.71 | +9.66 [-31.32, 46.89] | INSUFFICIENT |
| MLP输入 | 无类别名属性 | flower→rose | 416→17390 | 8/5 | +0.00 | -2.24 | +2.24 [2.24, 2.24] | INSUFFICIENT |
| MLP输入 | 无类别名属性 | flower→tulip | 416→17390 | 8/7 | +0.00 | -1.90 | +1.90 [1.90, 1.90] | INSUFFICIENT |
| MLP输入 | 无类别名属性 | cutlery→spoon | 416→17390 | 11/9 | +0.00 | +0.19 | -0.19 [-0.19, -0.19] | INSUFFICIENT |
| MLP输入 | 无类别名属性 | cutlery→fork | 416→17390 | 11/8 | +0.00 | -1.97 | +1.97 [1.97, 1.97] | INSUFFICIENT |
| MLP输入 | 无类别名情境 | furniture→chair | 416→5196 | 15/14 | +46.19 | +46.35 | -0.16 [-27.04, 20.31] | UNRESOLVED |
| MLP输入 | 无类别名情境 | furniture→sofa | 416→5196 | 15/14 | +31.90 | +25.28 | +6.63 [-22.71, 41.39] | UNRESOLVED |
| MLP输入 | 无类别名情境 | clothing→shirt | 28550→966 | 19/13 | +8.10 | +21.25 | -13.16 [-24.75, 0.97] | UNRESOLVED |
| MLP输入 | 无类别名情境 | clothing→trousers | 28550→966 | 19/11 | +6.70 | +14.89 | -8.19 [-24.71, 10.11] | UNRESOLVED |
| MLP输入 | 无类别名情境 | instrument→piano | 416→14913 | 14/22 | -29.87 | -25.94 | -3.93 [-25.72, 30.70] | UNRESOLVED |
| MLP输入 | 无类别名情境 | instrument→guitar | 416→14913 | 14/22 | -34.42 | -23.97 | -10.44 [-30.86, 18.65] | UNRESOLVED |
| MLP输入 | 无类别名情境 | flower→rose | 416→17390 | 6/5 | +0.00 | -10.68 | +10.68 [10.68, 10.68] | INSUFFICIENT |
| MLP输入 | 无类别名情境 | flower→tulip | 416→17390 | 6/8 | +0.00 | -8.68 | +8.68 [8.68, 8.68] | INSUFFICIENT |
| MLP输入 | 无类别名情境 | cutlery→spoon | 416→17390 | 10/4 | +0.00 | -0.24 | +0.24 [0.24, 0.24] | INSUFFICIENT |
| MLP输入 | 无类别名情境 | cutlery→fork | 416→17390 | 10/7 | +0.00 | +0.04 | -0.04 [-0.04, -0.04] | INSUFFICIENT |


## 固定猫狗边跨类别迁移（探索）

| SAE | 表述 | 对 | 边 | 中心支持A/B | 原始条件差pp | 参照差pp | 超额差pp / 95%CI | 判定 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Attention输出 | 显式类别名 | car→bicycle | 9117→5567 | 11/17 | +0.00 | -8.37 | +8.37 [8.37, 8.37] | UNRESOLVED |
| Attention输出 | 显式类别名 | apple→banana | 9117→5567 | 10/1 | +0.00 | +8.16 | -8.16 [-8.16, -8.16] | INSUFFICIENT |
| Attention输出 | 显式类别名 | chair→sofa | 9117→5567 | 3/0 | +nan | +nan | +nan 未定义 | INSUFFICIENT |
| Attention输出 | 显式类别名 | shirt→trousers | 9117→5567 | 12/9 | +0.00 | -4.49 | +4.49 [4.49, 4.49] | INSUFFICIENT |
| Attention输出 | 显式类别名 | piano→guitar | 9117→5567 | 3/16 | +0.00 | -3.25 | +3.25 [3.25, 3.25] | INSUFFICIENT |
| Attention输出 | 显式类别名 | rose→tulip | 9117→5567 | 5/2 | +0.00 | +0.66 | -0.66 [-0.66, -0.66] | INSUFFICIENT |
| Attention输出 | 显式类别名 | spoon→fork | 9117→5567 | 6/7 | +0.00 | -8.79 | +8.79 [8.79, 8.79] | INSUFFICIENT |
| Attention输出 | 保留类别名改写 | car→bicycle | 9117→5567 | 10/16 | -25.00 | -44.75 | +19.75 [-12.40, 39.48] | UNRESOLVED |
| Attention输出 | 保留类别名改写 | apple→banana | 9117→5567 | 9/1 | +0.00 | +21.06 | -21.06 [-21.06, -21.06] | INSUFFICIENT |
| Attention输出 | 保留类别名改写 | chair→sofa | 9117→5567 | 2/0 | +nan | +nan | +nan 未定义 | INSUFFICIENT |
| Attention输出 | 保留类别名改写 | shirt→trousers | 9117→5567 | 14/8 | -12.50 | -12.42 | -0.08 [-37.58, 12.42] | INSUFFICIENT |
| Attention输出 | 保留类别名改写 | piano→guitar | 9117→5567 | 2/15 | +0.00 | +0.44 | -0.44 [-0.44, -0.44] | INSUFFICIENT |
| Attention输出 | 保留类别名改写 | rose→tulip | 9117→5567 | 7/0 | +nan | +nan | +nan 未定义 | INSUFFICIENT |
| Attention输出 | 保留类别名改写 | spoon→fork | 9117→5567 | 4/7 | -14.29 | -11.73 | -2.55 [-88.27, 11.73] | INSUFFICIENT |
| Attention输出 | 无类别名属性 | car→bicycle | 9117→5567 | 0/4 | +nan | +nan | +nan 未定义 | INSUFFICIENT |
| Attention输出 | 无类别名属性 | apple→banana | 9117→5567 | 1/0 | +nan | +nan | +nan 未定义 | INSUFFICIENT |
| Attention输出 | 无类别名属性 | chair→sofa | 9117→5567 | 2/1 | +0.00 | +1.93 | -1.93 [-1.93, -1.93] | INSUFFICIENT |
| Attention输出 | 无类别名属性 | shirt→trousers | 9117→5567 | 1/1 | +0.00 | +21.88 | -21.88 [-21.88, -21.88] | INSUFFICIENT |
| Attention输出 | 无类别名属性 | piano→guitar | 9117→5567 | 3/6 | +0.00 | +1.70 | -1.70 [-1.70, -1.70] | INSUFFICIENT |
| Attention输出 | 无类别名属性 | rose→tulip | 9117→5567 | 0/1 | +nan | +nan | +nan 未定义 | INSUFFICIENT |
| Attention输出 | 无类别名属性 | spoon→fork | 9117→5567 | 0/2 | +nan | +nan | +nan 未定义 | INSUFFICIENT |
| Attention输出 | 无类别名情境 | car→bicycle | 9117→5567 | 5/7 | +0.00 | -21.50 | +21.50 [21.50, 21.50] | INSUFFICIENT |
| Attention输出 | 无类别名情境 | apple→banana | 9117→5567 | 1/1 | +0.00 | +10.74 | -10.74 [-10.74, -10.74] | INSUFFICIENT |
| Attention输出 | 无类别名情境 | chair→sofa | 9117→5567 | 3/0 | +nan | +nan | +nan 未定义 | INSUFFICIENT |
| Attention输出 | 无类别名情境 | shirt→trousers | 9117→5567 | 1/4 | +0.00 | +2.71 | -2.71 [-2.71, -2.71] | INSUFFICIENT |
| Attention输出 | 无类别名情境 | piano→guitar | 9117→5567 | 3/10 | +0.00 | -4.01 | +4.01 [4.01, 4.01] | INSUFFICIENT |
| Attention输出 | 无类别名情境 | rose→tulip | 9117→5567 | 1/8 | -12.50 | -7.96 | -4.54 [-29.54, 7.96] | INSUFFICIENT |
| Attention输出 | 无类别名情境 | spoon→fork | 9117→5567 | 0/3 | +nan | +nan | +nan 未定义 | INSUFFICIENT |


## 完整执行覆盖

候选不足同样保留：ATTN家具、花；MLP动物、交通、水果，没有开发固定类别边。这5个域×SAE的四种表述共20项未运行类别关系确认（不是不存在关系）。5个域的40父子边配置同理未运行。MLP无猫狗迁移边，7目标域×4表述的28迁移配置未运行。完整64项同父细类覆盖见results/relation_category_complete_coverage.csv。
