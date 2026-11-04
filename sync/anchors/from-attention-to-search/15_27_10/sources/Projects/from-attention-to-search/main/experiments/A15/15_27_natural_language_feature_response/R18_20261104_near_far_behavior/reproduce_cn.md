# 只读复算

实际评分脚本为/data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R01_behavior/code/run.py，配置为/data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R01_behavior/config.json。原生模型得到最后归一化状态后，用冻结输出头在每个候选token预测位置取分；已包含候选自身先前token。与公开完整前向的差异已核对，无SAE读取。

不加载模型即可从逐token原分数复算全部点估计：

```bash
python /data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R01_behavior/code/replay_metrics.py
```

检查全部原文重新分词、物品末token与距离、候选全链、A/B不变量、逐分总和、区间及冻结来源：

```bash
env PYTHONPATH=/data/250010109/dependency_packages/hf_transformers_qwen3 python /data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R01_behavior/code/verify.py
```

复核由同一agent的独立算式实现完成，不冒充独立科学审核。Anchor事实更新及路径规范化后，原冻结字节由frozen_owner_resolution.json指向执行侧存档；协议正文、数据和权重不改。run.py会拒绝覆盖旧评分文件，上述只读命令不会重跑前向。实际数据位于data/panel.jsonl，输出在results/smoke.jsonl／heldout.jsonl。正式目录的代码是实际执行源的阅读副本，运行时使用上面的绝对执行路径。
