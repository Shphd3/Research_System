# A07 Anchor Summary CN

## 一句话

A06 已经把二维核心度量固定为 M4 矩阵响应能量；A07 要回答的是：在高维均匀 feature 下，中心化或校准后的 M4 是否仍能实现接近均匀分发，并且保持非零专家偏好。

## 当前结论

- 原始 M4 不适合作为均匀负载理论目标，因为 expert 的平均能量差会制造负载偏置。
- 二维中，中心化 M4 可以严格得到 50/50 分发；这是二维 traceless quadratic form 的特殊性质。
- 高维中，中心化只保证平均分数差为 0，不保证正负区域各占一半。
- 高维推广需要额外条件：中心化分数差矩阵的谱不能被少数方向主导。
- 如果谱分散，中心化 M4 应近似均匀；如果谱尖峰，可能偏载，需要阈值校准。
- 校准本身不证明 specialization，必须同时报告 margin。

## 下一步实验

1. 在高维均匀球面上测试 raw M4、centered M4、calibrated M4、M3 top-r 和线性近似。
2. 报告 load、margin、low-margin fraction、degeneracy、M4 agreement 和谱分散指标。
3. 再进入 text-facing 静态路由实验，测试真实 hidden state 上哪种方法最稳。

## 当前方法判断

- 理论核心：centered/calibrated M4。
- 高维近似：weighted low-rank M4 / M3 top-r。
- 真实 text 最有前途：经验中心化 + 阈值校准 + 加权低秩 M4。
- 不建议作为主方法：raw M4、M1/M2 prototype、纯线性 halfspace。
