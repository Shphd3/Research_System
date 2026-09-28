# 代码范围与运行方法

## 已提供什么

本目录提供可直接运行的**数据构造、解析校验和通用自动微分数值内核**，不是已经适配用户服务器的 S7 完整运行器。主实验实施的完整规则在 [Protocol](../documents/protocol.md)，原生接口的唯一要求在 [adapter_contract.md](adapter_contract.md)。

| 文件 | 功能 |
|---|---|
| `controlled_data.py` | 从原生校准输入构建16维坐标；生成匹配的A/B向量、标签、噪声与逻辑样本ID；构造共同解证书 |
| `mechanism_core.py` | 正确累积源梯度、固定范数更新、逐样本损失与一阶分解、共同原子选择 |
| `check_calibration.py` | 检查解析公式、同范数构造、标签关系、共同解及拒绝不可实现主条件 |
| `check_numerical_core.py` | 检查微批归一化、零更新、参数—表征一致性与有符号分解 |

S7 专用加载、纯下游回放、原生 SAE 预处理和编码、远程提交、全条件调度与主统计聚合**尚未在本环境实现或验证**。执行Agent应按照接口契约和Protocol实现这些环境相关部分，不得用下面的单元测试收据代替它们。

本轮已固定的模型锚点是精确33B完整里程碑，四H100各独立负责三个完整确认方向族；当前代码目录仍没有四卡运行器。历史21B加载manifest只可帮助定位源码，不能用其模型键选择本轮权重。四卡进程分工、数值和停止门槛见Protocol §9、§13。

## 已实际运行的本地检查

```bash
cd shared_update_research_pack
python scripts/check_calibration.py checks/calibration.json
python scripts/check_numerical_core.py checks/numerical_core.json
```

检查只需要 NumPy、PyTorch CPU。当前实际环境版本见 `../checks/environment.json`。不要求升级到某个新版本，不自动安装软件。修改代码或在另一环境运行时使用新收据文件，避免覆盖本次交付收据。

两个检查通过只说明测试覆盖的数学和数值内核一致。它们没有 S7 权重，也没有训练或读取真实 SAE，因此不提供主假设的经验支持。

## 数据生成的最小示例

原环境先从真实中间层输入获得 `C_native[N,2048]`，再运行：

```python
import numpy as np
from scripts.controlled_data import calibrate

geometry, reference_index = calibrate(C_native)
np.savez_compressed(
    "basis.npz", c0=geometry.c0, Q=geometry.Q,
    sigma=geometry.sigma, beta=geometry.beta,
    x0=X_native[reference_index], reference_index=reference_index,
)
```

`C_native` 与 `X_native` 必须来自同一记录、同一位置；采集方式由真实适配器实现，不是可凭空创建的变量。命令行生成一个目标样本文件：

```bash
python scripts/controlled_data.py \
  --basis basis.npz --family 21001 --rho 0.8 --pairs 256 \
  --out generated_B_example.npz
```

该命令只是示例，不是完整96梯度／192更新运行器。全部划分必须按Protocol调用 `generate` 并保存清单；保持／翻转标签已同时返回，不另换输入。

## 数值内核的最小调用

```python
from scripts.mechanism_core import source_gradient, normalized_delta, measure

# W0、b、CA、CB、yA、yB 是同设备上的浮点/整型张量。
# tail(a) 是真实、冻结、可求导、逐行独立的 S7 下游，返回 [N, 2]。
G = source_gradient(W0, b, CA, yA, tail, microbatch=32)
dW = normalized_delta(W0, G, eps=1e-4)
result_B = measure(W0, b, CB, yB, dW, tail, Q=Q_S, microbatch=32)
```

先用独立A读出调用同一个 `measure` 验证源改善。不得把训练批次A损失下降当成独立A验证。

上述内核返回 `baseline/after/I/I1/C_S/C_perp/R/a0/da/e` 等数组。`Q_S` 可为空；为空时C_S定义为0，仅作调试，不能声称完成SAE子空间分析。正式主实验应按Protocol补齐所有结构集合和匹配对照。

## 明确不提供的承诺

不承诺服务器上的历史路径仍存在；不猜S7尾部运算；不承诺默认精度足以测出微小损失变化；不把虚拟更新计成连续训练。先通过原生适配器检查，再形成完整执行注册。
