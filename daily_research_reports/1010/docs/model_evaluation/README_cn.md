# 在命令行反复输入，比较模型续写

两个脚本：`run_comparison.sh`是命令入口；`compare_models.py`负责加载和生成。
只使用当前机器的已有模型与设备，不训练、不提交作业、不下载或安装软件。

## 开始交互

```bash
cd /data/250010109/Research_System/daily_research_reports/1010/docs/model_evaluation
bash run_comparison.sh --check-only   # 只检查资产与依赖，不加载模型
bash run_comparison.sh                # 默认Dense / S7 / SALL，进入交互
```

看到`输入>`后，输入文本并回车，例如`Introduce yourself:`。
程序将文本转成token，依次显示三个模型的续写、新token数、停止原因及耗时。
每轮使用相同输入token IDs；每轮独立，不拼接上一轮内容，也不加聊天模板。
输入`/quit`、`/exit`或按Ctrl-D退出；Ctrl-C中断并释放模型进程。
当前输入为单行文本，不是手工输入数字token ID；生成上限通过命令参数设置。

所有模型默认最多生成**500个新token**，不包含输入token；并不是把总上下文设为500。
生成`<|endoftext|>`（ID151643）立即停止，不要求达到500。
停止原因`eos`表示生成了停止符；`max_new_tokens`表示达到生成上限；
`context_limit`表示到达模型上下文边界。8层模型上下文为2048，不静默裁剪过长输入。
若输入较长，实际可生成的长度会小于500。上限可用`--max-new-tokens 100`统一修改。

## 原始千问与这组模型的区别

默认`base`是**8层Dense精确33B训练token检查点**，不是原始千问。
S7是fresh lambda0.1的精确33B检查点；SALL是unit-weight精确33B检查点。
准确地址与对应原生代码由[资产库](../../../../assets/README_cn.md)解析，每次运行先做严格访问检查。

```bash
# 只与原始28层Qwen3-0.6B-Base交互，最多500个新token。
bash run_comparison.sh --models base --base-source qwen

# 原始Qwen与S7/SALL接受同样输入，均最多500个新token。
bash run_comparison.sh --base-source qwen

# 只加载S7，可减少交互期间的内存与显存占用。
bash run_comparison.sh --models s7
```

原始Qwen与8层模型的架构和训练来源不同；这只能观察输出，不能作为严格配对的质量排名。
本地原始Qwen的`generation_config.json`与tokenizer均声明EOS为151643。
声明停止符说明应如何停止，不能单凭配置确认训练数据包含多少停止符。
本轮检查的8层训练数据读取器直接读取已分词的`.bin`流，不在读取时添加EOS；
本轮没有追溯全部预处理记录或统计实际训练目标中的EOS，因此是否、如何训练过EOS仍待核实。
在500个token内没生成EOS，不能反推训练中不存在EOS。

## 重复输出与解码对照

默认`greedy`：每步取概率最高的token，便于复查截图里的现象。
也可以采样：按温度调整概率，仅保留累计概率达到top-p的最小候选集合，再随机选择下一token。
以下保持模型、输入方式和长度上限不变，只改变解码规则：

```bash
bash run_comparison.sh --decode sample --temperature 0.8 --top-p 0.95 --seed 42
```

每个模型、每段输入重设同一随机种子；相同种子不意味着不同模型会抽到相同token。
未添加重复惩罚，避免把被惩罚后消失的重复误认成模型本来就不重复。
采样若减轻重复，支持输出对解码方式敏感；不能单独证明训练没有问题。

截图里Dense、S7、SALL均重复，且均以长度上限结束。
它们目前接受原文续写，并非自动接收“用户提问—助手回答”的结构。
`Introduce yourself:`可能引出介绍指南或问题清单；后续贪心选择也可能维持重复循环。
这些是待区分的解释，截图不能证明SAE导致重复或模型没有学过停止。
扩大到500只是让我们观察更长的续写和是否出现EOS，不是修复重复的方法。
可输入`The capital of France is`、`Once upon a time,`与原句对照，观察不同开头是否仍进入列表循环。

## 一次性运行、环境与保存

```bash
# 给定文本时为一次性模式；模型按顺序加载、退出，不常驻。
bash run_comparison.sh "Introduce yourself:"
bash run_comparison.sh --prompt "The capital of France is" --prompt "Once upon a time,"

# 交互退出时保存本轮所有已完成输出；拒绝覆盖已有文件，建议存执行目录。
bash run_comparison.sh --output /data/250010109/MoE_Router/experiments/20261010_text_generation/interactive_01.json

# 指定已有环境，不会自行安装包。
MODEL_EVAL_PYTHON=/path/to/python bash run_comparison.sh --check-only
```

有CUDA时默认使用本地第一张可见卡，可通过`CUDA_VISIBLE_DEVICES=1`选择物理卡。
`--device cpu`可在CPU上运行；默认float32，显存紧张可用`--dtype bfloat16`，但精度会影响输出。
**交互模式中所选模型各自占一个独立进程，并同时常驻设备**，每个模型只加载一次。
显存不足时先用`--models s7`等单模型方式；一次性模式则逐个加载并释放。
模型输出在该模型本次生成完成后显示，不是逐token流式显示。
程序没有后台超时；500-token无缓存生成可能较慢，等待时可Ctrl-C结束。

入口使用当前Python，并接入已有`/data/250010109/dependency_packages/hf_transformers_qwen3`。
可通过`MODEL_EVAL_DEPS_DIR`覆盖依赖目录。需要torch、tokenizers；原始Qwen还需要transformers。
RTX5090需使用支持该卡的已有PyTorch环境；脚本不自动替换torch。

复用各模型自己的原生配置、实现与检查点；适配只读映射、meta初始化和严格权重载入，
不恢复optimizer。S7/SALL的SAE是训练时附加重构目标所用的模块，不直接重构替换语言模型预测路径。
生成读取最后位置的原生隐藏表征与输出层，不计算附加SAE损失。
所有模型的此脚本路径均不使用KV缓存，每步重算前缀，所以长输出较慢。

本轮验证：所需资产的当前访问、两种base选择的依赖预检、微型CPU加载／生成／EOS逻辑、
交互重复输入和进程清理。没有新运行真实模型的500-token生成；截图是用户提供的既有输出。
