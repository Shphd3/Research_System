# 可复现入口

这是实际执行源码、配置和轻量回执的副本。原执行入口为执行根ops/run.sh，激活已存在依赖层后用source/entry.py运行source/engine.py。完整输入与冻结的逐步记录顺序位于原执行根provenance/，哈希在freeze.json。保护投影复用R05 basis_initial.pt。原始TRAIN/DEV、缓存和权重不入Git或轻包；所需资产ID见frozen.json。

不要直接覆盖已有执行根重跑；engine拒绝已有terminal。复现实验需复制为独立执行根并取得相应授权。本轮训练已结束，不因交付而新增训练。分析重放：python ops/analyze.py（只读既有评价/标量）；不得再次执行finalize.py重复登记。原TensorBoard轴标签问题通过repair_telemetry.py从原JSON重建，原events全部保存于tensorboard_raw。
