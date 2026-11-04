派生阅读副本；原件位置：`assets/distance_attention_r05_20261028_cn.md`。
[精确原始文件](../../sources/assets/distance_attention_r05_20261028_cn.md)；研究修改仍回到原件。

---

# R05 距离响应与Attention资产

数据ID：`data_a15_27_r05_five_distance_attention_20261028`；输出ID：`analysis_a15_27_r05_distance_attention_20261028`。

复用冻结Qwen3-0.6B-Base、E16 block27 MLP输入SAE和A22原14层联合共享z。E16原FP32 Top32；A22原BF16门控和TRAIN归一化，不截取encoder。最后层及14层原空间decoder范数与贡献单列。

B人工构造/受控编辑24家族960前缀，精确16/48/80/112/144，全部240token且目标239。A复用R04真实120窗口及原划分，192token、每篇8查询、block27全16heads；并非未经编辑的B自然语料或训练标签。

频率复用R04全坐标65536参考token的z>0计数；频率区间按254规范URL组，候选最低20参考命中分组，极低支持保留。没有新参考前向。

实际新增1096=960B+120A+16检查/失败。无训练、干预、新资源或封存TEST。原始数组、全文、统计代码留执行侧；本系统只保留选择证据。原始失败eager/未遮未来的检查读出不作主结果；正式A因果权重全部校验、原生激活与R04全120文档精确一致。

[一页结论](../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R05_distance_attention_20261028/summary_cn.md)

执行地址：/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028
