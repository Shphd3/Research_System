# 统计定义、数据与完整复核

## 1. 精确算式

令b为是否入选。开发侧d_j=mean(b_B−b_A)，T=sum|d|，w=|d|/T，s=sign(d)。确认X=|b_B−b_A|，M=sumwX，alpha=wX/M，m=sumalpha*p。M=0时缺失。R=sumw*s*(b_B−b_A)不除M。

K_j是每家族alpha在独立单位等权下的平均，sumK=1且mean(m)=sumKp。原矩贡献Kp与中心化贡献K(p−mean)分开：少见成员可能占大量K但Kp很小，因此不能只按数值分子挑“重要成员”。

DEV有效数1/sumw²、每家族有效数1/sumalpha²、平均K有效数1/sumK²不同。差异总量T不是成员个数，质量M不是激活幅值。

## 2. 原判定

S11原16行源字段原样摘录到S11_original_16.csv；原24重比较族同时包含共有/成员更替/共有幅值，不能只取本轮16项重新校正而改判。方向的原Holm16另含两差异通道。原反向条件按原代码保留；未决与不足不合并为不存在。

## 3. 原始表索引

- nonshared_member_events.csv.gz：所有配对/表述/家族的A_only/B_only成员、原始z、固定权重/方向、原alpha、Q/G计数。
- feature_turnover.csv.gz：每成员DEV差/权重、CONF入选/方向计数、质量K、频率矩与覆盖。
- family_turnover.csv.gz：各模式的质量、有效数、频率/分位数、原全权重方向R。R列明确标注original_weight；不冒充子集R。
- pair_summary.csv：全部配对、原权重/均匀XOR/DEV稳定子集。K和覆盖诊断标明original_weight范围；模式质量/有效数独立。
- main_contrasts_exploratory.csv：固定粗细主对，两个臂在同一有效家族上比较；子集空质量不偷偷补0。
- alternative_baselines.csv：其他父类与四条实际跨细类的等权混合。
- continuous_cdf.csv.gz：各真实配对的完整显式加权CDF。
- feature_removal_effects.csv：纯统计逐成员删除重归一化，不是模型消融。
- stable_candidate_checks.csv：DEV固定掩码，同ID的四表述方向/覆盖/区间，未通过保留。
- fixed_cases.csv与案例册：固定DEV前三与F001完整原文、位置、两侧z、预响应、Top32阈值。

## 4. 数值和缺失

新频率用整数参考计数/6000，原S11内部参考p曾为float32；点回放容差1e−8，未重写旧数值/区间。加权分位数采用整数DEV净计数逆CDF，原来的边界修复保留。

初次独立验证对全缺失稳定子集使用了数值断言，已记录为失败并只续跑剩余验证；共同缺失仍为缺失，不改成0。诊断输出澄清K/R是原权重，S13稳定覆盖补齐场景条件；初版输出保存在versions/，主均值/权重/候选未改。

## 5. 新旧/独立边界

S11/S13全部已看过；本轮无重切分、无新独立确认。S11原家族没有已核实的额外场景标签，沿其原单位但保留模板依赖限制；S13用16场景簇。Q/G、字典和feature不是独立重复。新协议冻结的是提案，材料/模型响应NOT RUN。
