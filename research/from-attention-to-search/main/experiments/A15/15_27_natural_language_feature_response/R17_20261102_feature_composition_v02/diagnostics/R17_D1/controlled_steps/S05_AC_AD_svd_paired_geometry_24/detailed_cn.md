# S05 详细记录：总体轴、配对差与真实成员

[中文小结](summary_cn.md)先读。[冻结协议](protocol_cn.md)与[frozen_plan](frozen_plan.json)拥有执行规则；科学接受和下一步等待共同审阅。全部输入来自已完成S04的Description:冒号位置，没有模型前向或旧后缀替换。

## 样本矩阵、均值与谱

每个家族行相邻，P和对应细类一一配对。AC与AD的P逐行完全相同。原始X/中心X均6×30000，均值30000维、奇异值6个、右方向6×30000均在对应NPZ保存；最后数值零方向不解释。列均值非零项另有CSV以供人工核对，未列项为0。

| 接口 | 尺度 | 组 | 行ID（顺序） | 维度 | 数值秩 | 均值/矩阵文件 |
| --- | --- | --- | --- | --- | --- | --- |
| ATTN_SAE | raw_z | AC | S04_F01_P; S04_F01_cat; S04_F02_P; S04_F02_cat; S04_F03_P; S04_F03_cat | 6×30000 | 5 | [NPZ](cache/ATTN_SAE/raw_z/AC.npz) |
| ATTN_SAE | raw_z | AD | S04_F01_P; S04_F01_dog; S04_F02_P; S04_F02_dog; S04_F03_P; S04_F03_dog | 6×30000 | 5 | [NPZ](cache/ATTN_SAE/raw_z/AD.npz) |
| ATTN_SAE | decoder_weighted | AC | S04_F01_P; S04_F01_cat; S04_F02_P; S04_F02_cat; S04_F03_P; S04_F03_cat | 6×30000 | 5 | [NPZ](cache/ATTN_SAE/decoder_weighted/AC.npz) |
| ATTN_SAE | decoder_weighted | AD | S04_F01_P; S04_F01_dog; S04_F02_P; S04_F02_dog; S04_F03_P; S04_F03_dog | 6×30000 | 5 | [NPZ](cache/ATTN_SAE/decoder_weighted/AD.npz) |
| MLPIN_SAE | raw_z | AC | S04_F01_P; S04_F01_cat; S04_F02_P; S04_F02_cat; S04_F03_P; S04_F03_cat | 6×30000 | 5 | [NPZ](cache/MLPIN_SAE/raw_z/AC.npz) |
| MLPIN_SAE | raw_z | AD | S04_F01_P; S04_F01_dog; S04_F02_P; S04_F02_dog; S04_F03_P; S04_F03_dog | 6×30000 | 5 | [NPZ](cache/MLPIN_SAE/raw_z/AD.npz) |
| MLPIN_SAE | decoder_weighted | AC | S04_F01_P; S04_F01_cat; S04_F02_P; S04_F02_cat; S04_F03_P; S04_F03_cat | 6×30000 | 5 | [NPZ](cache/MLPIN_SAE/decoder_weighted/AC.npz) |
| MLPIN_SAE | decoder_weighted | AD | S04_F01_P; S04_F01_dog; S04_F02_P; S04_F02_dog; S04_F03_P; S04_F03_dog | 6×30000 | 5 | [NPZ](cache/MLPIN_SAE/decoder_weighted/AD.npz) |

中心化分别减AC/AD自己的探索均值，持出投影仍用对应均值；不能把不同组坐标的原点或轴直接当作同一坐标。差向量投影不用再减均值，等于子类坐标减P坐标。

| 接口 | 尺度 | 组 | 序号 | 奇异值 | 方差比例 | 到下一值间隔 | 相对间隔 | 小间隔提醒 | 非零秩内 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ATTN_SAE | raw_z | AC | 1 | 17.537702775 | 0.366741529 | 2.450534829 | 0.139729522 | False | True |
| ATTN_SAE | raw_z | AC | 2 | 15.087167946 | 0.271412678 | 2.742888022 | 0.181802710 | False | True |
| ATTN_SAE | raw_z | AC | 3 | 12.344279923 | 0.181696350 | 3.124269227 | 0.253094490 | False | True |
| ATTN_SAE | raw_z | AC | 4 | 9.220010696 | 0.101362551 | 1.091337809 | 0.118366219 | False | True |
| ATTN_SAE | raw_z | AC | 5 | 8.128672887 | 0.078786893 | 8.128672887 | 1.000000000 | False | True |
| ATTN_SAE | raw_z | AC | 6 | 0.000000000 | 0.000000000 | 不可定义 | 不可定义 | False | False |
| ATTN_SAE | raw_z | AD | 1 | 19.305307970 | 0.391634023 | 4.158231782 | 0.215393186 | False | True |
| ATTN_SAE | raw_z | AD | 2 | 15.147076188 | 0.241092980 | 1.133028321 | 0.074801784 | True | True |
| ATTN_SAE | raw_z | AD | 3 | 14.014047867 | 0.206373599 | 4.505113333 | 0.321471239 | False | True |
| ATTN_SAE | raw_z | AD | 4 | 9.508934534 | 0.095014669 | 1.590690021 | 0.167283728 | False | True |
| ATTN_SAE | raw_z | AD | 5 | 7.918244513 | 0.065884729 | 7.918244513 | 1.000000000 | False | True |
| ATTN_SAE | raw_z | AD | 6 | 0.000000000 | 0.000000000 | 不可定义 | 不可定义 | False | False |
| ATTN_SAE | decoder_weighted | AC | 1 | 17.537701624 | 0.366741506 | 2.450533712 | 0.139729468 | False | True |
| ATTN_SAE | decoder_weighted | AC | 2 | 15.087167913 | 0.271412695 | 2.742888222 | 0.181802724 | False | True |
| ATTN_SAE | decoder_weighted | AC | 3 | 12.344279691 | 0.181696356 | 3.124269669 | 0.253094530 | False | True |
| ATTN_SAE | decoder_weighted | AC | 4 | 9.220010022 | 0.101362543 | 1.091337062 | 0.118366147 | False | True |
| ATTN_SAE | decoder_weighted | AC | 5 | 8.128672960 | 0.078786900 | 8.128672960 | 1.000000000 | False | True |
| ATTN_SAE | decoder_weighted | AC | 6 | 0.000000000 | 0.000000000 | 不可定义 | 不可定义 | False | False |
| ATTN_SAE | decoder_weighted | AD | 1 | 19.305307264 | 0.391633996 | 4.158230625 | 0.215393133 | False | True |
| ATTN_SAE | decoder_weighted | AD | 2 | 15.147076639 | 0.241092996 | 1.133028543 | 0.074801796 | True | True |
| ATTN_SAE | decoder_weighted | AD | 3 | 14.014048095 | 0.206373607 | 4.505113421 | 0.321471240 | False | True |
| ATTN_SAE | decoder_weighted | AD | 4 | 9.508934675 | 0.095014672 | 1.590690194 | 0.167283744 | False | True |
| ATTN_SAE | decoder_weighted | AD | 5 | 7.918244480 | 0.065884729 | 7.918244480 | 1.000000000 | False | True |
| ATTN_SAE | decoder_weighted | AD | 6 | 0.000000000 | 0.000000000 | 不可定义 | 不可定义 | False | False |
| MLPIN_SAE | raw_z | AC | 1 | 28.784488702 | 0.374345701 | 2.739127451 | 0.095159844 | True | True |
| MLPIN_SAE | raw_z | AC | 2 | 26.045361251 | 0.306490193 | 5.171885121 | 0.198572217 | False | True |
| MLPIN_SAE | raw_z | AC | 3 | 20.873476130 | 0.196854511 | 8.408780613 | 0.402845245 | False | True |
| MLPIN_SAE | raw_z | AC | 4 | 12.464695516 | 0.070197098 | 1.724973533 | 0.138388742 | False | True |
| MLPIN_SAE | raw_z | AC | 5 | 10.739721983 | 0.052112498 | 10.739721983 | 1.000000000 | False | True |
| MLPIN_SAE | raw_z | AC | 6 | 0.000000000 | 0.000000000 | 不可定义 | 不可定义 | False | False |
| MLPIN_SAE | raw_z | AD | 1 | 29.467069461 | 0.396900995 | 4.116681437 | 0.139704474 | False | True |
| MLPIN_SAE | raw_z | AD | 2 | 25.350388023 | 0.293749757 | 5.001743294 | 0.197304408 | False | True |
| MLPIN_SAE | raw_z | AD | 3 | 20.348644729 | 0.189268906 | 7.951293950 | 0.390752999 | False | True |
| MLPIN_SAE | raw_z | AD | 4 | 12.397350780 | 0.070253194 | 1.956668753 | 0.157829587 | False | True |
| MLPIN_SAE | raw_z | AD | 5 | 10.440682026 | 0.049827148 | 10.440682026 | 1.000000000 | False | True |
| MLPIN_SAE | raw_z | AD | 6 | 0.000000000 | 0.000000000 | 不可定义 | 不可定义 | False | False |
| MLPIN_SAE | decoder_weighted | AC | 1 | 28.784490284 | 0.374345732 | 2.739130786 | 0.095159955 | True | True |
| MLPIN_SAE | decoder_weighted | AC | 2 | 26.045359498 | 0.306490143 | 5.171882323 | 0.198572123 | False | True |
| MLPIN_SAE | decoder_weighted | AC | 3 | 20.873477175 | 0.196854525 | 8.408781085 | 0.402845248 | False | True |
| MLPIN_SAE | decoder_weighted | AC | 4 | 12.464696090 | 0.070197103 | 1.724974036 | 0.138388776 | False | True |
| MLPIN_SAE | decoder_weighted | AC | 5 | 10.739722054 | 0.052112497 | 10.739722054 | 1.000000000 | False | True |
| MLPIN_SAE | decoder_weighted | AC | 6 | 0.000000000 | 0.000000000 | 不可定义 | 不可定义 | False | False |
| MLPIN_SAE | decoder_weighted | AD | 1 | 29.467070432 | 0.396901027 | 4.116684388 | 0.139704569 | False | True |
| MLPIN_SAE | decoder_weighted | AD | 2 | 25.350386044 | 0.293749715 | 5.001741347 | 0.197304346 | False | True |
| MLPIN_SAE | decoder_weighted | AD | 3 | 20.348644698 | 0.189268908 | 7.951293774 | 0.390752991 | False | True |
| MLPIN_SAE | decoder_weighted | AD | 4 | 12.397350923 | 0.070253196 | 1.956668449 | 0.157829561 | False | True |
| MLPIN_SAE | decoder_weighted | AD | 5 | 10.440682474 | 0.049827153 | 10.440682474 | 1.000000000 | False | True |
| MLPIN_SAE | decoder_weighted | AD | 6 | 0.000000000 | 0.000000000 | 不可定义 | 不可定义 | False | False |

## 固定轴上的每条坐标、类内和家族内变化

[所有24条在AC/AD前二维的坐标](results/projections_all24.csv)，包含非拟合条件及椅子；[类内中心与离散](results/class_spread_frozen_coordinates.csv)是在冻结轴中的描述统计，不是重拟合或分类。家族内变化在[配对投影](results/paired_projections_both_bases.csv)，同时投到两组轴；完整30000维差及分项保存在每site/scale的paired_differences.npz。

| 接口 | 尺度 | 家族 | 猫差长度 | 狗差长度 | 猫差/狗差有向余弦 | 猫差/探索均值余弦 | 狗差/探索均值余弦 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ATTN_SAE | raw_z | F01 | 14.953873 | 17.890601 | 0.704123 | 0.741142 | 0.774501 |
| ATTN_SAE | raw_z | F02 | 15.867589 | 15.217686 | 0.812526 | 0.732543 | 0.705723 |
| ATTN_SAE | raw_z | F03 | 13.649192 | 14.917244 | 0.621526 | 0.696498 | 0.787287 |
| ATTN_SAE | raw_z | F04 | 12.779231 | 14.226455 | 0.763945 | 0.457792 | 0.554088 |
| ATTN_SAE | raw_z | F05 | 11.447756 | 13.092658 | 0.645844 | 0.262424 | 0.409728 |
| ATTN_SAE | raw_z | F06 | 7.973834 | 8.538851 | 0.789007 | 0.299445 | 0.366524 |
| ATTN_SAE | decoder_weighted | F01 | 14.953872 | 17.890602 | 0.704124 | 0.741142 | 0.774501 |
| ATTN_SAE | decoder_weighted | F02 | 15.867588 | 15.217686 | 0.812526 | 0.732543 | 0.705723 |
| ATTN_SAE | decoder_weighted | F03 | 13.649191 | 14.917245 | 0.621526 | 0.696498 | 0.787287 |
| ATTN_SAE | decoder_weighted | F04 | 12.779230 | 14.226456 | 0.763945 | 0.457792 | 0.554088 |
| ATTN_SAE | decoder_weighted | F05 | 11.447756 | 13.092658 | 0.645844 | 0.262424 | 0.409728 |
| ATTN_SAE | decoder_weighted | F06 | 7.973833 | 8.538850 | 0.789007 | 0.299445 | 0.366524 |
| MLPIN_SAE | raw_z | F01 | 24.185553 | 25.583498 | 0.830993 | 0.799205 | 0.818498 |
| MLPIN_SAE | raw_z | F02 | 19.190883 | 17.851242 | 0.796999 | 0.725954 | 0.670441 |
| MLPIN_SAE | raw_z | F03 | 24.031918 | 22.740783 | 0.834691 | 0.833694 | 0.823703 |
| MLPIN_SAE | raw_z | F04 | 21.025904 | 21.063056 | 0.821242 | 0.533169 | 0.552104 |
| MLPIN_SAE | raw_z | F05 | 25.180397 | 25.032783 | 0.798725 | 0.370222 | 0.317424 |
| MLPIN_SAE | raw_z | F06 | 12.146327 | 13.494033 | 0.675203 | 0.504098 | 0.362102 |
| MLPIN_SAE | decoder_weighted | F01 | 24.185556 | 25.583499 | 0.830993 | 0.799205 | 0.818498 |
| MLPIN_SAE | decoder_weighted | F02 | 19.190884 | 17.851242 | 0.796999 | 0.725954 | 0.670441 |
| MLPIN_SAE | decoder_weighted | F03 | 24.031919 | 22.740783 | 0.834691 | 0.833694 | 0.823703 |
| MLPIN_SAE | decoder_weighted | F04 | 21.025905 | 21.063056 | 0.821242 | 0.533169 | 0.552104 |
| MLPIN_SAE | decoder_weighted | F05 | 25.180398 | 25.032782 | 0.798725 | 0.370223 | 0.317424 |
| MLPIN_SAE | decoder_weighted | F06 | 12.146328 | 13.494032 | 0.675203 | 0.504098 | 0.362102 |

## 共同强弱与Top32更替分开

逐家族共同正成员、换入、换出在坐标上互斥，差向量平方范数=三部分平方范数之和。份额是激活空间的几何量，不是因果重要性。逐原子原始P/细类值、pre及事件见[difference_member_events](results/difference_member_events.csv)。

| 接口 | 尺度 | 家族 | 细类 | 部分 | 成员数 | 分项L2 | 总差L2 | 平方范数份额 | 零端仍有正pre数 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ATTN_SAE | raw_z | F01 | cat | retained_amplitude | 16 | 5.865959 | 14.953873 | 0.153876 | 0/0 |
| ATTN_SAE | raw_z | F01 | cat | new_support | 16 | 11.653512 | 14.953873 | 0.607304 | 9/0 |
| ATTN_SAE | raw_z | F01 | cat | lost_support | 16 | 7.307837 | 14.953873 | 0.238820 | 0/12 |
| ATTN_SAE | raw_z | F02 | cat | retained_amplitude | 17 | 2.089552 | 15.867589 | 0.017341 | 0/0 |
| ATTN_SAE | raw_z | F02 | cat | new_support | 15 | 11.437565 | 15.867589 | 0.519571 | 14/0 |
| ATTN_SAE | raw_z | F02 | cat | lost_support | 15 | 10.797975 | 15.867589 | 0.463087 | 0/15 |
| ATTN_SAE | raw_z | F03 | cat | retained_amplitude | 19 | 6.083200 | 13.649192 | 0.198633 | 0/0 |
| ATTN_SAE | raw_z | F03 | cat | new_support | 13 | 8.345072 | 13.649192 | 0.373806 | 11/0 |
| ATTN_SAE | raw_z | F03 | cat | lost_support | 13 | 8.924958 | 13.649192 | 0.427561 | 0/12 |
| ATTN_SAE | raw_z | F04 | cat | retained_amplitude | 17 | 4.666229 | 12.779231 | 0.133328 | 0/0 |
| ATTN_SAE | raw_z | F04 | cat | new_support | 15 | 9.481238 | 12.779231 | 0.550454 | 12/0 |
| ATTN_SAE | raw_z | F04 | cat | lost_support | 15 | 7.186179 | 12.779231 | 0.316218 | 0/14 |
| ATTN_SAE | raw_z | F05 | cat | retained_amplitude | 19 | 3.894305 | 11.447756 | 0.115723 | 0/0 |
| ATTN_SAE | raw_z | F05 | cat | new_support | 13 | 7.911901 | 11.447756 | 0.477662 | 12/0 |
| ATTN_SAE | raw_z | F05 | cat | lost_support | 13 | 7.299817 | 11.447756 | 0.406615 | 0/12 |
| ATTN_SAE | raw_z | F06 | cat | retained_amplitude | 19 | 2.715502 | 7.973834 | 0.115975 | 0/0 |
| ATTN_SAE | raw_z | F06 | cat | new_support | 13 | 6.111484 | 7.973834 | 0.587434 | 12/0 |
| ATTN_SAE | raw_z | F06 | cat | lost_support | 13 | 4.342562 | 7.973834 | 0.296591 | 0/13 |
| ATTN_SAE | raw_z | F01 | dog | retained_amplitude | 17 | 7.668520 | 17.890601 | 0.183727 | 0/0 |
| ATTN_SAE | raw_z | F01 | dog | new_support | 15 | 14.573673 | 17.890601 | 0.663572 | 10/0 |
| ATTN_SAE | raw_z | F01 | dog | lost_support | 15 | 6.991098 | 17.890601 | 0.152701 | 0/11 |
| ATTN_SAE | raw_z | F02 | dog | retained_amplitude | 20 | 2.442782 | 15.217686 | 0.025767 | 0/0 |
| ATTN_SAE | raw_z | F02 | dog | new_support | 12 | 11.478621 | 15.217686 | 0.568961 | 12/0 |
| ATTN_SAE | raw_z | F02 | dog | lost_support | 12 | 9.687726 | 15.217686 | 0.405272 | 0/12 |
| ATTN_SAE | raw_z | F03 | dog | retained_amplitude | 20 | 6.896354 | 14.917244 | 0.213728 | 0/0 |
| ATTN_SAE | raw_z | F03 | dog | new_support | 12 | 9.991729 | 14.917244 | 0.448646 | 12/0 |
| ATTN_SAE | raw_z | F03 | dog | lost_support | 12 | 8.667747 | 14.917244 | 0.337625 | 0/11 |
| ATTN_SAE | raw_z | F04 | dog | retained_amplitude | 18 | 5.178314 | 14.226455 | 0.132490 | 0/0 |
| ATTN_SAE | raw_z | F04 | dog | new_support | 14 | 11.237496 | 14.226455 | 0.623944 | 12/0 |
| ATTN_SAE | raw_z | F04 | dog | lost_support | 14 | 7.021096 | 14.226455 | 0.243566 | 0/12 |
| ATTN_SAE | raw_z | F05 | dog | retained_amplitude | 18 | 5.710101 | 13.092658 | 0.190209 | 0/0 |
| ATTN_SAE | raw_z | F05 | dog | new_support | 14 | 9.197891 | 13.092658 | 0.493538 | 13/0 |
| ATTN_SAE | raw_z | F05 | dog | lost_support | 14 | 7.362829 | 13.092658 | 0.316252 | 0/13 |
| ATTN_SAE | raw_z | F06 | dog | retained_amplitude | 19 | 2.963130 | 8.538851 | 0.120421 | 0/0 |
| ATTN_SAE | raw_z | F06 | dog | new_support | 13 | 6.564663 | 8.538851 | 0.591052 | 13/0 |
| ATTN_SAE | raw_z | F06 | dog | lost_support | 13 | 4.586615 | 8.538851 | 0.288527 | 0/13 |
| ATTN_SAE | decoder_weighted | F01 | cat | retained_amplitude | 16 | 5.865958 | 14.953872 | 0.153876 | 0/0 |
| ATTN_SAE | decoder_weighted | F01 | cat | new_support | 16 | 11.653512 | 14.953872 | 0.607304 | 9/0 |
| ATTN_SAE | decoder_weighted | F01 | cat | lost_support | 16 | 7.307837 | 14.953872 | 0.238820 | 0/12 |
| ATTN_SAE | decoder_weighted | F02 | cat | retained_amplitude | 17 | 2.089552 | 15.867588 | 0.017341 | 0/0 |
| ATTN_SAE | decoder_weighted | F02 | cat | new_support | 15 | 11.437564 | 15.867588 | 0.519571 | 14/0 |
| ATTN_SAE | decoder_weighted | F02 | cat | lost_support | 15 | 10.797974 | 15.867588 | 0.463087 | 0/15 |
| ATTN_SAE | decoder_weighted | F03 | cat | retained_amplitude | 19 | 6.083200 | 13.649191 | 0.198633 | 0/0 |
| ATTN_SAE | decoder_weighted | F03 | cat | new_support | 13 | 8.345072 | 13.649191 | 0.373806 | 11/0 |
| ATTN_SAE | decoder_weighted | F03 | cat | lost_support | 13 | 8.924958 | 13.649191 | 0.427561 | 0/12 |
| ATTN_SAE | decoder_weighted | F04 | cat | retained_amplitude | 17 | 4.666228 | 12.779230 | 0.133328 | 0/0 |
| ATTN_SAE | decoder_weighted | F04 | cat | new_support | 15 | 9.481238 | 12.779230 | 0.550454 | 12/0 |
| ATTN_SAE | decoder_weighted | F04 | cat | lost_support | 15 | 7.186179 | 12.779230 | 0.316218 | 0/14 |
| ATTN_SAE | decoder_weighted | F05 | cat | retained_amplitude | 19 | 3.894305 | 11.447756 | 0.115723 | 0/0 |
| ATTN_SAE | decoder_weighted | F05 | cat | new_support | 13 | 7.911902 | 11.447756 | 0.477662 | 12/0 |
| ATTN_SAE | decoder_weighted | F05 | cat | lost_support | 13 | 7.299816 | 11.447756 | 0.406615 | 0/12 |
| ATTN_SAE | decoder_weighted | F06 | cat | retained_amplitude | 19 | 2.715502 | 7.973833 | 0.115975 | 0/0 |
| ATTN_SAE | decoder_weighted | F06 | cat | new_support | 13 | 6.111483 | 7.973833 | 0.587434 | 12/0 |
| ATTN_SAE | decoder_weighted | F06 | cat | lost_support | 13 | 4.342562 | 7.973833 | 0.296591 | 0/13 |
| ATTN_SAE | decoder_weighted | F01 | dog | retained_amplitude | 17 | 7.668520 | 17.890602 | 0.183727 | 0/0 |
| ATTN_SAE | decoder_weighted | F01 | dog | new_support | 15 | 14.573676 | 17.890602 | 0.663572 | 10/0 |
| ATTN_SAE | decoder_weighted | F01 | dog | lost_support | 15 | 6.991098 | 17.890602 | 0.152701 | 0/11 |
| ATTN_SAE | decoder_weighted | F02 | dog | retained_amplitude | 20 | 2.442781 | 15.217686 | 0.025767 | 0/0 |
| ATTN_SAE | decoder_weighted | F02 | dog | new_support | 12 | 11.478621 | 15.217686 | 0.568961 | 12/0 |
| ATTN_SAE | decoder_weighted | F02 | dog | lost_support | 12 | 9.687727 | 15.217686 | 0.405272 | 0/12 |
| ATTN_SAE | decoder_weighted | F03 | dog | retained_amplitude | 20 | 6.896353 | 14.917245 | 0.213728 | 0/0 |
| ATTN_SAE | decoder_weighted | F03 | dog | new_support | 12 | 9.991730 | 14.917245 | 0.448646 | 12/0 |
| ATTN_SAE | decoder_weighted | F03 | dog | lost_support | 12 | 8.667746 | 14.917245 | 0.337625 | 0/11 |
| ATTN_SAE | decoder_weighted | F04 | dog | retained_amplitude | 18 | 5.178313 | 14.226456 | 0.132490 | 0/0 |
| ATTN_SAE | decoder_weighted | F04 | dog | new_support | 14 | 11.237497 | 14.226456 | 0.623944 | 12/0 |
| ATTN_SAE | decoder_weighted | F04 | dog | lost_support | 14 | 7.021097 | 14.226456 | 0.243566 | 0/12 |
| ATTN_SAE | decoder_weighted | F05 | dog | retained_amplitude | 18 | 5.710101 | 13.092658 | 0.190209 | 0/0 |
| ATTN_SAE | decoder_weighted | F05 | dog | new_support | 14 | 9.197891 | 13.092658 | 0.493538 | 13/0 |
| ATTN_SAE | decoder_weighted | F05 | dog | lost_support | 14 | 7.362829 | 13.092658 | 0.316252 | 0/13 |
| ATTN_SAE | decoder_weighted | F06 | dog | retained_amplitude | 19 | 2.963129 | 8.538850 | 0.120421 | 0/0 |
| ATTN_SAE | decoder_weighted | F06 | dog | new_support | 13 | 6.564662 | 8.538850 | 0.591052 | 13/0 |
| ATTN_SAE | decoder_weighted | F06 | dog | lost_support | 13 | 4.586615 | 8.538850 | 0.288527 | 0/13 |
| MLPIN_SAE | raw_z | F01 | cat | retained_amplitude | 24 | 13.466573 | 24.185553 | 0.310029 | 0/0 |
| MLPIN_SAE | raw_z | F01 | cat | new_support | 8 | 16.102836 | 24.185553 | 0.443295 | 5/0 |
| MLPIN_SAE | raw_z | F01 | cat | lost_support | 8 | 12.012122 | 24.185553 | 0.246676 | 0/6 |
| MLPIN_SAE | raw_z | F02 | cat | retained_amplitude | 25 | 11.205003 | 19.190883 | 0.340906 | 0/0 |
| MLPIN_SAE | raw_z | F02 | cat | new_support | 7 | 11.865019 | 19.190883 | 0.382250 | 7/0 |
| MLPIN_SAE | raw_z | F02 | cat | lost_support | 7 | 10.097486 | 19.190883 | 0.276845 | 0/7 |
| MLPIN_SAE | raw_z | F03 | cat | retained_amplitude | 23 | 12.132501 | 24.031918 | 0.254873 | 0/0 |
| MLPIN_SAE | raw_z | F03 | cat | new_support | 9 | 16.158038 | 24.031918 | 0.452064 | 9/0 |
| MLPIN_SAE | raw_z | F03 | cat | lost_support | 9 | 13.009739 | 24.031918 | 0.293063 | 0/9 |
| MLPIN_SAE | raw_z | F04 | cat | retained_amplitude | 22 | 8.677598 | 21.025904 | 0.170329 | 0/0 |
| MLPIN_SAE | raw_z | F04 | cat | new_support | 10 | 14.647946 | 21.025904 | 0.485338 | 6/0 |
| MLPIN_SAE | raw_z | F04 | cat | lost_support | 10 | 12.337975 | 21.025904 | 0.344333 | 0/7 |
| MLPIN_SAE | raw_z | F05 | cat | retained_amplitude | 19 | 14.893979 | 25.180397 | 0.349862 | 0/0 |
| MLPIN_SAE | raw_z | F05 | cat | new_support | 13 | 15.413868 | 25.180397 | 0.374712 | 13/0 |
| MLPIN_SAE | raw_z | F05 | cat | lost_support | 13 | 13.214934 | 25.180397 | 0.275426 | 0/8 |
| MLPIN_SAE | raw_z | F06 | cat | retained_amplitude | 27 | 6.608832 | 12.146327 | 0.296046 | 0/0 |
| MLPIN_SAE | raw_z | F06 | cat | new_support | 5 | 8.314191 | 12.146327 | 0.468544 | 4/0 |
| MLPIN_SAE | raw_z | F06 | cat | lost_support | 5 | 5.893286 | 12.146327 | 0.235410 | 0/4 |
| MLPIN_SAE | raw_z | F01 | dog | retained_amplitude | 24 | 14.774611 | 25.583498 | 0.333513 | 0/0 |
| MLPIN_SAE | raw_z | F01 | dog | new_support | 8 | 15.786929 | 25.583498 | 0.380781 | 5/0 |
| MLPIN_SAE | raw_z | F01 | dog | lost_support | 8 | 13.674761 | 25.583498 | 0.285706 | 0/4 |
| MLPIN_SAE | raw_z | F02 | dog | retained_amplitude | 26 | 12.193805 | 17.851242 | 0.466597 | 0/0 |
| MLPIN_SAE | raw_z | F02 | dog | new_support | 6 | 8.981348 | 17.851242 | 0.253131 | 6/0 |
| MLPIN_SAE | raw_z | F02 | dog | lost_support | 6 | 9.450574 | 17.851242 | 0.280272 | 0/6 |
| MLPIN_SAE | raw_z | F03 | dog | retained_amplitude | 23 | 12.934946 | 22.740783 | 0.323533 | 0/0 |
| MLPIN_SAE | raw_z | F03 | dog | new_support | 9 | 13.273334 | 22.740783 | 0.340682 | 9/0 |
| MLPIN_SAE | raw_z | F03 | dog | lost_support | 9 | 13.177594 | 22.740783 | 0.335785 | 0/9 |
| MLPIN_SAE | raw_z | F04 | dog | retained_amplitude | 22 | 11.881557 | 21.063056 | 0.318203 | 0/0 |
| MLPIN_SAE | raw_z | F04 | dog | new_support | 10 | 12.257867 | 21.063056 | 0.338678 | 8/0 |
| MLPIN_SAE | raw_z | F04 | dog | lost_support | 10 | 12.337975 | 21.063056 | 0.343119 | 0/7 |
| MLPIN_SAE | raw_z | F05 | dog | retained_amplitude | 20 | 18.362542 | 25.032783 | 0.538081 | 0/0 |
| MLPIN_SAE | raw_z | F05 | dog | new_support | 12 | 11.228511 | 25.032783 | 0.201199 | 11/0 |
| MLPIN_SAE | raw_z | F05 | dog | lost_support | 12 | 12.781932 | 25.032783 | 0.260720 | 0/8 |
| MLPIN_SAE | raw_z | F06 | dog | retained_amplitude | 25 | 9.712999 | 13.494033 | 0.518111 | 0/0 |
| MLPIN_SAE | raw_z | F06 | dog | new_support | 7 | 6.348358 | 13.494033 | 0.221329 | 7/0 |
| MLPIN_SAE | raw_z | F06 | dog | lost_support | 7 | 6.888028 | 13.494033 | 0.260559 | 0/6 |
| MLPIN_SAE | decoder_weighted | F01 | cat | retained_amplitude | 24 | 13.466572 | 24.185556 | 0.310029 | 0/0 |
| MLPIN_SAE | decoder_weighted | F01 | cat | new_support | 8 | 16.102840 | 24.185556 | 0.443295 | 5/0 |
| MLPIN_SAE | decoder_weighted | F01 | cat | lost_support | 8 | 12.012123 | 24.185556 | 0.246676 | 0/6 |
| MLPIN_SAE | decoder_weighted | F02 | cat | retained_amplitude | 25 | 11.205003 | 19.190884 | 0.340905 | 0/0 |
| MLPIN_SAE | decoder_weighted | F02 | cat | new_support | 7 | 11.865022 | 19.190884 | 0.382250 | 7/0 |
| MLPIN_SAE | decoder_weighted | F02 | cat | lost_support | 7 | 10.097485 | 19.190884 | 0.276845 | 0/7 |
| MLPIN_SAE | decoder_weighted | F03 | cat | retained_amplitude | 23 | 12.132502 | 24.031919 | 0.254873 | 0/0 |
| MLPIN_SAE | decoder_weighted | F03 | cat | new_support | 9 | 16.158039 | 24.031919 | 0.452064 | 9/0 |
| MLPIN_SAE | decoder_weighted | F03 | cat | lost_support | 9 | 13.009739 | 24.031919 | 0.293063 | 0/9 |
| MLPIN_SAE | decoder_weighted | F04 | cat | retained_amplitude | 22 | 8.677597 | 21.025905 | 0.170329 | 0/0 |
| MLPIN_SAE | decoder_weighted | F04 | cat | new_support | 10 | 14.647946 | 21.025905 | 0.485338 | 6/0 |
| MLPIN_SAE | decoder_weighted | F04 | cat | lost_support | 10 | 12.337975 | 21.025905 | 0.344333 | 0/7 |
| MLPIN_SAE | decoder_weighted | F05 | cat | retained_amplitude | 19 | 14.893976 | 25.180398 | 0.349861 | 0/0 |
| MLPIN_SAE | decoder_weighted | F05 | cat | new_support | 13 | 15.413871 | 25.180398 | 0.374713 | 13/0 |
| MLPIN_SAE | decoder_weighted | F05 | cat | lost_support | 13 | 13.214935 | 25.180398 | 0.275426 | 0/8 |
| MLPIN_SAE | decoder_weighted | F06 | cat | retained_amplitude | 27 | 6.608831 | 12.146328 | 0.296046 | 0/0 |
| MLPIN_SAE | decoder_weighted | F06 | cat | new_support | 5 | 8.314194 | 12.146328 | 0.468544 | 4/0 |
| MLPIN_SAE | decoder_weighted | F06 | cat | lost_support | 5 | 5.893285 | 12.146328 | 0.235410 | 0/4 |
| MLPIN_SAE | decoder_weighted | F01 | dog | retained_amplitude | 24 | 14.774611 | 25.583499 | 0.333513 | 0/0 |
| MLPIN_SAE | decoder_weighted | F01 | dog | new_support | 8 | 15.786931 | 25.583499 | 0.380781 | 5/0 |
| MLPIN_SAE | decoder_weighted | F01 | dog | lost_support | 8 | 13.674762 | 25.583499 | 0.285706 | 0/4 |
| MLPIN_SAE | decoder_weighted | F02 | dog | retained_amplitude | 26 | 12.193806 | 17.851242 | 0.466597 | 0/0 |
| MLPIN_SAE | decoder_weighted | F02 | dog | new_support | 6 | 8.981348 | 17.851242 | 0.253131 | 6/0 |
| MLPIN_SAE | decoder_weighted | F02 | dog | lost_support | 6 | 9.450574 | 17.851242 | 0.280272 | 0/6 |
| MLPIN_SAE | decoder_weighted | F03 | dog | retained_amplitude | 23 | 12.934947 | 22.740783 | 0.323533 | 0/0 |
| MLPIN_SAE | decoder_weighted | F03 | dog | new_support | 9 | 13.273334 | 22.740783 | 0.340682 | 9/0 |
| MLPIN_SAE | decoder_weighted | F03 | dog | lost_support | 9 | 13.177594 | 22.740783 | 0.335785 | 0/9 |
| MLPIN_SAE | decoder_weighted | F04 | dog | retained_amplitude | 22 | 11.881557 | 21.063056 | 0.318203 | 0/0 |
| MLPIN_SAE | decoder_weighted | F04 | dog | new_support | 10 | 12.257866 | 21.063056 | 0.338678 | 8/0 |
| MLPIN_SAE | decoder_weighted | F04 | dog | lost_support | 10 | 12.337975 | 21.063056 | 0.343119 | 0/7 |
| MLPIN_SAE | decoder_weighted | F05 | dog | retained_amplitude | 20 | 18.362540 | 25.032782 | 0.538081 | 0/0 |
| MLPIN_SAE | decoder_weighted | F05 | dog | new_support | 12 | 11.228511 | 25.032782 | 0.201199 | 11/0 |
| MLPIN_SAE | decoder_weighted | F05 | dog | lost_support | 12 | 12.781933 | 25.032782 | 0.260720 | 0/8 |
| MLPIN_SAE | decoder_weighted | F06 | dog | retained_amplitude | 25 | 9.712999 | 13.494032 | 0.518111 | 0/0 |
| MLPIN_SAE | decoder_weighted | F06 | dog | new_support | 7 | 6.348358 | 13.494032 | 0.221330 | 7/0 |
| MLPIN_SAE | decoder_weighted | F06 | dog | lost_support | 7 | 6.888027 | 13.494032 | 0.260559 | 0/6 |

跨家族求均值后，同一原子可在不同家族属于不同部分，均值分项会重叠；不能把均值分项平方范数继续当互斥能量相加。下面9项把均值差点积按猫/狗三类分开，除以两条完整均值差范数积后，九项相加才等于整体有向余弦。

| 接口 | 尺度 | 猫分项 | 狗分项 | 点积 | 对整体均值差余弦的代数分项 |
| --- | --- | --- | --- | --- | --- |
| ATTN_SAE | raw_z | retained_amplitude | retained_amplitude | 12.743539 | 0.097975 |
| ATTN_SAE | raw_z | retained_amplitude | new_support | 3.359893 | 0.025831 |
| ATTN_SAE | raw_z | retained_amplitude | lost_support | 3.314915 | 0.025486 |
| ATTN_SAE | raw_z | new_support | retained_amplitude | 6.626981 | 0.050949 |
| ATTN_SAE | raw_z | new_support | new_support | 43.446791 | 0.334027 |
| ATTN_SAE | raw_z | new_support | lost_support | -0.810304 | -0.006230 |
| ATTN_SAE | raw_z | lost_support | retained_amplitude | 0.778439 | 0.005985 |
| ATTN_SAE | raw_z | lost_support | new_support | -2.006002 | -0.015423 |
| ATTN_SAE | raw_z | lost_support | lost_support | 30.661668 | 0.235733 |
| ATTN_SAE | decoder_weighted | retained_amplitude | retained_amplitude | 12.743537 | 0.097975 |
| ATTN_SAE | decoder_weighted | retained_amplitude | new_support | 3.359893 | 0.025831 |
| ATTN_SAE | decoder_weighted | retained_amplitude | lost_support | 3.314916 | 0.025486 |
| ATTN_SAE | decoder_weighted | new_support | retained_amplitude | 6.626980 | 0.050949 |
| ATTN_SAE | decoder_weighted | new_support | new_support | 43.446799 | 0.334027 |
| ATTN_SAE | decoder_weighted | new_support | lost_support | -0.810303 | -0.006230 |
| ATTN_SAE | decoder_weighted | lost_support | retained_amplitude | 0.778439 | 0.005985 |
| ATTN_SAE | decoder_weighted | lost_support | new_support | -2.006002 | -0.015423 |
| ATTN_SAE | decoder_weighted | lost_support | lost_support | 30.661668 | 0.235733 |
| MLPIN_SAE | raw_z | retained_amplitude | retained_amplitude | 90.805536 | 0.296943 |
| MLPIN_SAE | raw_z | retained_amplitude | new_support | 4.723450 | 0.015446 |
| MLPIN_SAE | raw_z | retained_amplitude | lost_support | 14.761537 | 0.048272 |
| MLPIN_SAE | raw_z | new_support | retained_amplitude | 1.492141 | 0.004879 |
| MLPIN_SAE | raw_z | new_support | new_support | 66.097606 | 0.216146 |
| MLPIN_SAE | raw_z | new_support | lost_support | -2.478777 | -0.008106 |
| MLPIN_SAE | raw_z | lost_support | retained_amplitude | 5.775094 | 0.018885 |
| MLPIN_SAE | raw_z | lost_support | new_support | -1.988314 | -0.006502 |
| MLPIN_SAE | raw_z | lost_support | lost_support | 57.152281 | 0.186894 |
| MLPIN_SAE | decoder_weighted | retained_amplitude | retained_amplitude | 90.805530 | 0.296943 |
| MLPIN_SAE | decoder_weighted | retained_amplitude | new_support | 4.723449 | 0.015446 |
| MLPIN_SAE | decoder_weighted | retained_amplitude | lost_support | 14.761540 | 0.048272 |
| MLPIN_SAE | decoder_weighted | new_support | retained_amplitude | 1.492143 | 0.004879 |
| MLPIN_SAE | decoder_weighted | new_support | new_support | 66.097611 | 0.216146 |
| MLPIN_SAE | decoder_weighted | new_support | lost_support | -2.478779 | -0.008106 |
| MLPIN_SAE | decoder_weighted | lost_support | retained_amplitude | 5.775094 | 0.018885 |
| MLPIN_SAE | decoder_weighted | lost_support | new_support | -1.988315 | -0.006502 |
| MLPIN_SAE | decoder_weighted | lost_support | lost_support | 57.152276 | 0.186894 |

## 稳定性与方向不唯一

27个有序bootstrap样本只来自3个探索家族，实际10个无序多重集；其中3个只含单一家族，秩1，二维子空间不可定义；18个含2家族，6个含3家族。27不是独立样本数，下面分位值不是置信区间。数值上余弦/重叠最大值可能因舍入高于1约1e−15，图文按1显示，原始值保留。

| 接口 | 尺度 | 量 | 有效/27 | 不可定义 | 最小 | 5% | 中位 | 95% | 最大 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ATTN_SAE | raw_z | PC1_absolute_cosine | 27 | 0 | 0.605502 | 0.605502 | 0.855997 | 0.890111 | 0.890111 |
| ATTN_SAE | raw_z | top2_overlap | 24 | 3 | 0.567017 | 0.567017 | 0.702173 | 0.745591 | 0.745591 |
| ATTN_SAE | raw_z | mean_paired_delta_signed_cosine | 27 | 0 | 0.621526 | 0.655962 | 0.738007 | 0.811872 | 0.812526 |
| ATTN_SAE | raw_z | AC_PC1_vs_full | 27 | 0 | 0.017335 | 0.086684 | 0.777800 | 1.000000 | 1.000000 |
| ATTN_SAE | raw_z | AD_PC1_vs_full | 27 | 0 | 0.016087 | 0.270832 | 0.821303 | 1.000000 | 1.000000 |
| ATTN_SAE | raw_z | AC_top2_vs_full | 24 | 3 | 0.463751 | 0.463751 | 0.597697 | 1.000000 | 1.000000 |
| ATTN_SAE | raw_z | AD_top2_vs_full | 24 | 3 | 0.484371 | 0.484371 | 0.619489 | 1.000000 | 1.000000 |
| ATTN_SAE | decoder_weighted | PC1_absolute_cosine | 27 | 0 | 0.605502 | 0.605502 | 0.855997 | 0.890111 | 0.890111 |
| ATTN_SAE | decoder_weighted | top2_overlap | 24 | 3 | 0.567016 | 0.567016 | 0.702173 | 0.745591 | 0.745591 |
| ATTN_SAE | decoder_weighted | mean_paired_delta_signed_cosine | 27 | 0 | 0.621526 | 0.655962 | 0.738007 | 0.811872 | 0.812526 |
| ATTN_SAE | decoder_weighted | AC_PC1_vs_full | 27 | 0 | 0.017335 | 0.086684 | 0.777800 | 1.000000 | 1.000000 |
| ATTN_SAE | decoder_weighted | AD_PC1_vs_full | 27 | 0 | 0.016087 | 0.270832 | 0.821303 | 1.000000 | 1.000000 |
| ATTN_SAE | decoder_weighted | AC_top2_vs_full | 24 | 3 | 0.463751 | 0.463751 | 0.597697 | 1.000000 | 1.000000 |
| ATTN_SAE | decoder_weighted | AD_top2_vs_full | 24 | 3 | 0.484371 | 0.484371 | 0.619489 | 1.000000 | 1.000000 |
| MLPIN_SAE | raw_z | PC1_absolute_cosine | 27 | 0 | 0.796999 | 0.832103 | 0.963437 | 0.976269 | 0.976269 |
| MLPIN_SAE | raw_z | top2_overlap | 24 | 3 | 0.762925 | 0.762925 | 0.808657 | 0.930958 | 0.930958 |
| MLPIN_SAE | raw_z | mean_paired_delta_signed_cosine | 27 | 0 | 0.769854 | 0.769854 | 0.794301 | 0.824056 | 0.834691 |
| MLPIN_SAE | raw_z | AC_PC1_vs_full | 27 | 0 | 0.011761 | 0.116288 | 0.864256 | 1.000000 | 1.000000 |
| MLPIN_SAE | raw_z | AD_PC1_vs_full | 27 | 0 | 0.006488 | 0.158471 | 0.877861 | 1.000000 | 1.000000 |
| MLPIN_SAE | raw_z | AC_top2_vs_full | 24 | 3 | 0.515168 | 0.515168 | 0.561343 | 1.000000 | 1.000000 |
| MLPIN_SAE | raw_z | AD_top2_vs_full | 24 | 3 | 0.511965 | 0.511965 | 0.579225 | 1.000000 | 1.000000 |
| MLPIN_SAE | decoder_weighted | PC1_absolute_cosine | 27 | 0 | 0.796999 | 0.832103 | 0.963437 | 0.976269 | 0.976269 |
| MLPIN_SAE | decoder_weighted | top2_overlap | 24 | 3 | 0.762925 | 0.762925 | 0.808657 | 0.930958 | 0.930958 |
| MLPIN_SAE | decoder_weighted | mean_paired_delta_signed_cosine | 27 | 0 | 0.769854 | 0.769854 | 0.794301 | 0.824056 | 0.834691 |
| MLPIN_SAE | decoder_weighted | AC_PC1_vs_full | 27 | 0 | 0.011761 | 0.116288 | 0.864256 | 1.000000 | 1.000000 |
| MLPIN_SAE | decoder_weighted | AD_PC1_vs_full | 27 | 0 | 0.006488 | 0.158471 | 0.877862 | 1.000000 | 1.000000 |
| MLPIN_SAE | decoder_weighted | AC_top2_vs_full | 24 | 3 | 0.515168 | 0.515168 | 0.561343 | 1.000000 | 1.000000 |
| MLPIN_SAE | decoder_weighted | AD_top2_vs_full | 24 | 3 | 0.511965 | 0.511965 | 0.579225 | 1.000000 | 1.000000 |

## 预定反例：不满足同一PC1父子方向

反例来自运行前固定规则，只挑展示家族，不用检查结果选原子或重拟合。两套原始尺度都选到F05；其完整均值差方向仍有正夹角关联，但沿自身AC第一轴的分量与探索平均父子分量反号。一个投影分量反号不等于完整向量相反。

### ATTN_SAE · F05

规则：heldout own-group PC1 paired projection reverses exploration mean projection；探索参考投影=1.191980，检查投影=-1.002533。

P：

```text
An animal is the object described in this example.
Description:
```

cat：

```text
A cat is the animal described in this example.
Description:
```

dog：

```text
A dog is the animal described in this example.
Description:
```

N：

```text
A chair is the object described in this example.
Description:
```

| AC PC1固定前5 ID | P z | cat z | dog z | N z | cat−P | P/cat预激活 |
| --- | --- | --- | --- | --- | --- | --- |
| 10021 | 0.000000 | 2.980325 | 2.695201 | 0.000000 | 2.980325 | 0.951556/2.980325 |
| 2254 | 0.000000 | 2.103012 | 2.820965 | 0.000000 | 2.103012 | 1.452525/2.103012 |
| 4647 | 0.000000 | 1.817922 | 2.489547 | 0.000000 | 1.817922 | 0.623597/1.817922 |
| 22267 | 2.185197 | 2.332824 | 2.981111 | 2.192629 | 0.147628 | 2.185197/2.332824 |
| 24998 | 0.000000 | 2.511912 | 2.109032 | 2.140040 | 2.511912 | 1.082405/2.511912 |

### MLPIN_SAE · F05

规则：heldout own-group PC1 paired projection reverses exploration mean projection；探索参考投影=-3.266106，检查投影=3.332532。

P：

```text
An animal is the object described in this example.
Description:
```

cat：

```text
A cat is the animal described in this example.
Description:
```

dog：

```text
A dog is the animal described in this example.
Description:
```

N：

```text
A chair is the object described in this example.
Description:
```

| AC PC1固定前5 ID | P z | cat z | dog z | N z | cat−P | P/cat预激活 |
| --- | --- | --- | --- | --- | --- | --- |
| 8856 | 0.000000 | 4.423741 | 0.000000 | 0.000000 | 4.423741 | 2.827668/4.423741 |
| 966 | 7.885587 | 6.982516 | 7.373055 | 9.206148 | -0.903071 | 7.885587/6.982516 |
| 18809 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 2.250324/2.081469 |
| 4127 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | -0.105820/0.692035 |
| 20157 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | -1.468263/1.995628 |

## 原始/加权尺度及数值质量

| 接口 | 量 | 原始 | 加权 | 加权−原始 |
| --- | --- | --- | --- | --- |
| ATTN_SAE | PC1_absolute_cosine | 0.866373780 | 0.866373708 | -0.000000072002 |
| ATTN_SAE | top2_normalized_overlap | 0.725714419 | 0.725714374 | -0.000000045486 |
| ATTN_SAE | exploration_mean_delta_cosine | 0.754333406 | 0.754333422 | 0.000000016293 |
| ATTN_SAE | exploration_mean_delta_cat_L2 | 10.737757836 | 10.737757428 | -0.000000408186 |
| ATTN_SAE | exploration_mean_delta_dog_L2 | 12.113301799 | 12.113302556 | 0.000000756600 |
| MLPIN_SAE | PC1_absolute_cosine | 0.963437419 | 0.963437421 | 0.000000002217 |
| MLPIN_SAE | top2_normalized_overlap | 0.930957876 | 0.930957842 | -0.000000033890 |
| MLPIN_SAE | exploration_mean_delta_cosine | 0.772857570 | 0.772857486 | -0.000000083718 |
| MLPIN_SAE | exploration_mean_delta_cat_L2 | 17.765389130 | 17.765390591 | 0.000001460748 |
| MLPIN_SAE | exploration_mean_delta_dog_L2 | 17.213296878 | 17.213296958 | 0.000000079579 |

8个基础SVD与216个bootstrap SVD；192条投影、48条完整差向量、768个成员值核对。中心化/正交/重建/Gram谱及分解闭合误差见[verification](evidence/verification.json)：`{'centering': 4.736951571734001e-15, 'orthogonality': 1.3322676295501878e-15, 'reconstruction': 1.5938597780306232e-14, 'gram_spectrum_squared': 1.0231815394945443e-12, 'projection': 0.0, 'difference_projection': 5.329070518200751e-15, 'mean_cosine_cross_terms': 1.1102230246251565e-16, 'between_within_SS': 1.9895196601282805e-13}`。S03/S04原件286个哈希保持。没有新LM/SAE前向、学习参数、optimizer、probe、干预、decoder空间比较或后续实验。

## 证据链与覆盖

| 项目 | 原始记录→计算→观察 | 状态/边界 |
|---|---|---|
| AC/AD总体方向 | matrix_manifest及各NPZ→探索SVD→绝对余弦/主角/重叠 | DONE_EXPLORATORY；总体变化 |
| 父类到细类 | S04 z→逐家族fine−P/均值→有向余弦/长度/双轴投影 | DONE_EXPLORATORY；不等同总体轴 |
| 强弱/支持更替 | 原始z/pre/Top32→三分项→逐对能量/均值交叉点积 | DONE_EXPLORATORY；无语义因果 |
| 稳定性 | 3探索家族→27成组重采样→有效数/范围 | DONE_EXPLORATORY；不是置信区间 |
| 成员与真实文本 | 只按探索系数选前5+原H2→全部24值/完整前文 | DONE_VALID；未按检查补选 |
| 数据/均值/脚本/图/数值核验 | 来源哈希/冻结/闭合 | DONE_VALID |
| 模型作用/一般概念规律 | 没有功能对照或独立大样本 | NOT_RUN/Unknown |

科学接受和下一步决定等待共同审阅。
