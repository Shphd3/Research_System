# 第三轮：实现与产物复核（AI分析）

缓存提取使用requires_grad=False/eval；小probe优化器只含Probe参数，字典优化器只含Dictionary参数，不加载主optimizer续训。随机打乱在各split内固定置换，real/shuffled相同初始化及训练位置，全部DEV训练，全EVAL测试。GPU b0 topk标签统一，避免并列score的CPU/GPU选择差。原A5分组源代码被逐项复用到8192宽字典，源停止条件与0.80–1.05原观察区间的差别事前注明；没有调整超参数追求1.08。A0 500归档恢复副本与archive及原manifest SHA相同，原位置没写回。全程仅既有MIG，主模型未训练，R04位置输入最终哈希见final_audit.json。公式检查与实际图像复核分开记录；无commit/push。研究者判断Unknown。
