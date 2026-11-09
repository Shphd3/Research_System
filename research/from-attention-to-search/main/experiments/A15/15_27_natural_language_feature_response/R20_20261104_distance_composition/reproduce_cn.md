# 复算

解压包后在根目录运行`python code/offline_replay.py`，只需Python/NumPy，不需模型、GPU、网络。从真实稀疏激活与逐token分数重算全部成对成员/范数以及六项主结果的区间和校正p。原始完整h/截断前响应、分组、统计/作图/评分代码均可继续审计。若包去重重复decoder_norm，manifest注明转换；原评分cache_sha指执行原件，包内SHA由包manifest拥有。

重新前向需原模型/SAE权重及原环境，详见[英文执行顺序与环境](reproduce.md)。原件/失败版本/协议修改均保留，复算不授予训练或干预权限。
