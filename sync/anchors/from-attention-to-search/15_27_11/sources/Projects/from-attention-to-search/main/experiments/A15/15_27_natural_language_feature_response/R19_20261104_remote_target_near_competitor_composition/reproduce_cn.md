# 复算说明

小包解压后，在根目录运行`python code/offline_replay.py`，只需Python/NumPy/SciPy，无模型、GPU或网络。从真实稀疏ID/数值和逐token评分出发，复算成员、六项主检验点值/区间/校正p及四项联合统计。null完整统计轨迹与种子/原代码保留；该离线入口不重新生成null样本。

重新前向需外部模型/SAE权重，见config与包内omitted_assets.json；原环境PYTHONPATH=/data/250010109/dependency_packages/hf_transformers_qwen3，PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python，TOKENIZERS_PARALLELISM=false。CPU2线程、FP32、SDPA、2×328；分阶段脚本拒绝覆盖现有评分。训练与激活干预均未运行。

[完整算法与执行顺序](reproduce.md)、[数据字段](dataset_guide_cn.md)、[执行记录](detailed_cn.md)保留原协议、冻结门、展示修正、失败版本、旧原件保护和检验分母。本轮不需要为审阅结果再运行前向。
