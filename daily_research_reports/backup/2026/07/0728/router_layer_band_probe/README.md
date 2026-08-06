# Layerwise Router × Spectral-Band Probe

本实验严格限定两个 step-40000 模型：始终启用负载均衡的线性 Top-1 模型，以及使用 running-center 的 decommon 线性 Top-1 模型。两者均为 12 层、宽度 768、8 个专家。

数据不从训练目录 `global-shard_01_of_10` 内抽取，而使用官方 DCLM 的独立顶层 `global-shard_02_of_10`。原始分片保存在共享数据缓存，不进入研究记录仓库；校准集和评估集按文档哈希分离。原始文件 SHA256 为：

`4c5ce60258943051758148653c448bb57724af7592cc9d3e9c053cc6f9e10323`

每个模型测两种冻结读出：

- `native`：LB 使用原始 Router 输入；decommon 使用 checkpoint 内冻结的 running center。
- `frozen_center`：两个模型都在独立 calibration 文档上估计一次层均值并冻结，离线重算 Gate；不改变专家分发，也不向后续层传播反事实路径。

中心化特征的 covariance 按 64 维等宽切成 12 个谱带。主指标是逐频带的一阶特征 $\eta^2$、二阶总能量 $\eta^2$、能量分位 NMI，以及同秩随机正交频带和错误层频带对照。`energy_router_summary.csv` 额外比较 raw energy 与 calibration-standardized energy 的频带赢家集中性；它是二阶偏置诊断，不是专家效用或新 Router 的训练结果。

运行环境需保留项目当前 CUDA/PyTorch 依赖，同时用 Transformers 4.51.x 加载旧 checkpoint：

```bash
CUDA_VISIBLE_DEVICES=0 \
PYTHONPATH=/tmp/router_probe_pydeps_451:/mnt/bucket/MoE_Router \
HF_ENDPOINT=https://huggingface.co \
HF_HOME=/data/share/109_cache_dir/hf_data \
/root/anaconda3/envs/spectral-hier/bin/python3.10 run_probe.py
```

输出：`route_concentration.csv`、`band_separability.csv`、`energy_router_summary.csv`、`center_comparison.csv`、`layer_summary.csv` 与 `data_manifest.json`。
