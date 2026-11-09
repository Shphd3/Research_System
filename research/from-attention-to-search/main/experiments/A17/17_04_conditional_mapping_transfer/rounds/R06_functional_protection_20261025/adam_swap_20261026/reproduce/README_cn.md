# 复核入口

`plan.json`锁定所有六状态、三批TRAIN、旧／新DEV和复放探针的索引与记录ID。`freeze.json`给出执行前源码、Anchor、协议哈希。原检查点不随包交付，路径／身份／前后哈希在`named_mapping_and_inputs.json`与`original_assets_immutable.json`。`frozen.json`是原完整训练设置。

`adam_swap_20261026.py`是实际单步执行源码，`engine.py`、`retention_r05_v1.py`、`local_dynamics_20261026.py`是实际复用依赖，`entry.py`是环境入口。原执行环境与数据缓存需按绝对资产路径复用；不声称单个ZIP含完整模型或可离线运行训练。已完成GPU执行拒绝覆盖原输出。

`analyze_adam_swap_20261026.py`和`run.sh`仅CPU重新聚合／作图，不启动模型前向；生产路径保留，完整逐题原始读出在执行目录（ZIP的execution_evidence亦含一份）。如另行获准复放GPU，应先将输出路径指向新的独立证据目录，保持当前冻结输入不变，计数上限不自动提高。

`input_access.json`是当前读取前资产检查；`output_access.json`是本轮输出检查（生成后添加）。`native_replay_gate.json`和`native_firstbatch_replay.csv`给出六状态24项复放，`independent_analysis_audit.json`是逐题与几何检查回执。无操作误差只是数值精度，不是抽样置信区间。
