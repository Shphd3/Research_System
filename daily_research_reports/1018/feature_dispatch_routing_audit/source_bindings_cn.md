# 原件、授权与执行绑定

用户提供的中文[Anchor](design/anchor_cn.md)和[Protocol](protocol_cn.md)逐字节保存。英文为伴随翻译，不新增科学决定。[原件哈希](provenance/design_freeze.json)。

用户本轮明确授权执行这些缓存诊断、整理项目与Daily。原始缓存和实际路由只读；评分项消融产生单独的虚拟路由，未部署到模型。无训练、模型前向、GPU、新Work、commit或push。

唯一输入run：`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z`；新诊断run：`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/routing_audit_20261018T143950Z`。主规则为A、B1(20261018)、B2(20261019)，A两seed一致只计一次；原低频名单964、高频名单C=962。C按旧TRAIN第90分位定义，不改成p≥0.5。原组分母保留。

案例只按TRAIN冻结9297、1133、2704，各从EVAL取3随机＋1高激活。有限冲突检索仅这3案例对既有可靠池，按TRAIN跨owner的n_ij/(n_i+n_j)取每规则前三，再复核固定EVAL对。没有新建全字典关系图。

附件没有固定逐feature接收率要求τ，故本轮只给条件性必要界，不能自行定义成功阈值。共同伴随全表按964×962完整保留，使用压缩CSV/NPZ减少磁盘，未删除目标。

本地最多8核、aggregate RSS≤16GiB、新增磁盘≤2GiB；只用已有稀疏缓存。200次上下文成块重采样种子20261018只给描述性区间，窗口不是独立文档。对应机器绑定为[execution_binding.json](provenance/execution_binding.json)。
