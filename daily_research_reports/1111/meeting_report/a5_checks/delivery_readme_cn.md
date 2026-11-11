# 包内阅读顺序

1. README_cn.md：一页6项结论及规则套用。
2. analysis_cn.md：各项原始摘要表、边界及为什么；各CSV保留全部精度。
3. protocol_original_frozen_cn.md：跑前不可变规则和超参数；protocol_cn.md尾部追加实际偏差与用户接受A1微差的记录。
4. evidence/final_audit.json：完成矩阵、源文件SHA及小模型存档清单。

所有结论为AI分析，研究者判断Unknown。图为实测数据PNG/PDF。表中NaN表示未观测／不适用，不是0。小探针、字典权重和大型隐藏态缓存不进入下载包，仍在执行根；其来源和SHA可定位。部分绝对路径引用原始工作区，离线阅读请用同名CSV及相对链接。主模型未更新，原R04产物未改。

ZIP完整性与文件清单见DELIVERY_MANIFEST.json。
