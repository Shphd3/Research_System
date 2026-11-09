# 0906 校正Router假设并规划验证

> [0902 Router Selection - 0905 decision](chatgpt-conversation://6a982979-0634-83e8-8e0f-f4e1f8dcabbb) 请阅读该对话以及 [@0903\[1\]规划 SAE 粗细粒度路由分析](thread://01a06773-49c8-7e32-b504-00f3e5ddaad0?hostId=remote-ssh-codex-managed%3Amig)  + [@0903\[2\]运行实验1逐层静态审计](thread://01a0679c-7ee2-71f3-91b5-f4df234571db?hostId=remote-ssh-codex-managed%3Amig) ,现在我能给出的假设如下：
> 我怀疑离线语义标签交给在线Router时，可能存在几个问题：1. 离线语义给定的是最后一层的语义，而不是对应层的语义，很有可能对当层的语义目标发生干扰，如果用当层的语义标签，可能能够改善Router；2. 我怀疑早期的表征读出会造成Router的错训，因此会偏离oracle的语义分发；这个点我还不知道怎么继续验证
> 请基于对话给出我的认知纠正，然后给我阐明我们接下来的实验四段式验证，给出具体的目的和接下来要做的行为。再给我区分一下术语，让我知道哪些实验对象是要训练Router的，哪些是不训练的
> 接下来重新计划，我将在6:30开始我的工作，在这之前可以运行审计给出初步结果，然后调整推进方向

<details><summary>13 previous messages</summary>

> 我会先读取这三个对话，核对已有结果和“四段式验证”的上下文，再把你的两个假设拆成可验证的问题，明确哪些步骤只做审计、哪些需要训练 Router，并安排 6:30 前后的工作。
>
> <details><summary>Explored a file, 2 searches, a list, ran a command</summary>
>
> <details><summary>Explored a file, a search</summary>
>
> - Read `/root/.codex/plugins/cache/openai-curated-remote/superpowers/6.3.0/skills/using-superpowers/SKILL.md`
> - Searched for `static|静态|Router|Research_System` in `MEMORY.md`
>
> </details>
>
> Tool call
>
> Tool: read_thread
> Status: completed
>
> Tool call
>
> Tool: read_thread
> Status: completed
>
> <details><summary>Explored 2 files, a search, a list</summary>
>
> - Read `/root/.codex/plugins/cache/openai-curated-remote/superpowers/6.3.0/skills/using-superpowers/references/codex-tools.md`
> - Read `/root/.codex/plugins/cache/openai-curated-remote/superpowers/6.3.0/skills/brainstorming/SKILL.md`
> - Listed files in `250010109`
> - Searched for `static|静态|Router|Research_System` in `MEMORY.md`
>
> </details>
>
> Tool call
>
> Tool: read_thread
> Status: completed
>
> Tool call
>
> Tool: read_thread
> Status: completed
>
> Tool call
>
> Tool: read_thread
> Status: completed
>
> Tool call
>
> Tool: read_thread
> Status: completed
>
> - Ran `find /data/250010109 -maxdepth 3 -name AGENTS.md -print
> date -u
> nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv,noheader`
>
> </details>
>
> 已有结果提示，需要把“标签在哪一层生成”和“标签用了多少上下文”分开：末层标签不一定错，但整窗标签可能包含当前词元还看不到的信息。另外，既有逐层审计测的是分类器能否读出标签，并没有训练实际分发的 Router。我会用 brainstorming 技能组织这次研究方案，先核对证据和可复用的审计入口。
>
> 你说的 6:30 是哪个日期、哪个时区？当前服务器时间为 9 月 6 日 07:56 UTC（北京时间 15:56）；我先继续核对结果与审计入口。
> - 9 月 7 日早上 6:30，北京时间
> - 9 月 6 日晚上 18:30，北京时间
>
> <details><summary>Explored 3 files, 2 searches, 2 lists</summary>
>
> - Read `./Research_System/AGENTS.md`
> - Searched for `*handoff*` in `MoE_Router`
> - Listed files in `experiments`
> - Read `./Research_System/AGENTS.md`
> - Read `./Research_System/.agents/skills/research-document-explainer/SKILL.md`
> - Listed files in `20260903_a15_13_e14_gmm_pseudolabel_oracle_gap`
> - Searched for `*E14*` in `experiments`
>
> </details>
>
> **你说的 6:30 是哪个日期、哪个时区？当前服务器时间为 9 月 6 日 07:56 UTC（北京时间 15:56）；我先继续核对结果与审计入口。**
>
> 9 月 6 日晚上 18:30，北京时间
>
> <details><summary>Explored 6 files</summary>
>
> - Read `./Research_System/.agents/skills/research-document-explainer/references/explanation_contract.md`
> - Read `./Research_System/.agents/skills/research-document-explainer/references/terminology_contract.md`
> - Read `./Research_System/.agents/skills/research-document-explainer/references/experiment_reasoning.md`
> - Read `./Research_System/.agents/skills/research-document-explainer/references/research_thinking.md`
> - Read `./Research_System/docs/research_terminology.md`
> - Read `./Research_System/PROJECTS.md`
>
> </details>
>
> 收到，按今天北京时间 18:30 安排。还有两点会影响计划：插层训练已经出现两个种子方向相反的结果，不能再把第 9 块当作已验证的最优插层；当前 SAE 层级也尚未形成覆盖全部类别的可靠教师。18:30 前最有价值的是核对旧伪标签专家的路径差距，以及审计所需的检查点、标签和数据是否齐全。
>
> <details><summary>Explored 9 files, 3 searches, a list, ran 3 commands</summary>
>
> <details><summary>Explored 9 files, a search</summary>
>
> - Read `./Research_System/PROJECTS.md`
> - Read `./Research_System/daily_research_reports/0903/focus_gmm_pseudolabel_oracle_gap.md`
> - Read `./Research_System/Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_gmm_pseudolabel_oracle_gap/summary.md`
> - Read `./MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/completion_audit.py`
> - Read `./MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/checkpoint_manifest.py`
> - Searched for `*manifest*` in `runs`
> - Read `./MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/models.py`
> - Read `./MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/prepare_pseudo_labels.py`
> - Read `./Research_System/Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_gmm_pseudolabel_oracle_gap/summary.md`
> - Read `./Research_System/Projects/graphs/expert_specialization.graph.yaml`
>
> </details>
>
> - Ran `python - <<'PY'
> from pathlib import Path
> import json,numpy as np
> r=Path('/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/runs/full-20260903T042000Z')
> m=json.loads((r/'checkpoint_manifest.json').read_text())
> for a in m['checkpoints']:
>  if 'hard' in a['model_key'].lower() or 'pseudo' in a['model_key'].lower():
>   print(a['model_key'],Path(a['checkpoint_path']).is_file(),a['checkpoint_path'])
> print('eval names',[p.name for p in (r/'evaluations').glob('*')][:35])
> print('data',m.get('data_hashes'))
> print('labels',[(str(p),p.stat().st_size) for p in (r/'pseudo_labels').glob('*/*')])
> PY
> grep -nE 'unit_coefficient|force_label|intervention ==|GMM|hard_pseudo|HARD' /data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/training.py
> sed -n '1,140p' /data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/registry.py`
>
> - Ran `sed -n '160,205p' /data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/training.py
> sed -n '258,355p' /data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/training.py
> python - <<'PY'
> import numpy as np
> from pathlib import Path
> r=Path('/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/runs/full-20260903T042000Z/evaluations')
> for s in [17,29]:
>  for mode in ['intact','unit','force_label','wrong_same_parent','wrong_other_parent']:
>   p=r/f'benchmark__HIER_GMM_HARD_R8__seed{s}__{mode}.npz'
>   z=np.load(p)
>   print(s,mode,'nll',z['loss_sum'].sum()/z['token_count'].sum(),'shapes', {k:z[k].shape for k in z.files} if mode=='intact' else '')
> PY`
>
> <details><summary>Explored a file, 2 searches, a list</summary>
>
> - Searched for `def _path_arguments` in `training.py`
> - Searched for `replace\(|path_mode|pseudo_hard|evaluate_nll` in `experiment_cli.py`
> - Read `./MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/experiment_cli.py`
> - Listed files in `runtime_env`
>
> </details>
>
> - Ran `sed -n '350,455p' /data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/training.py
> sed -n '105,160p' /data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/training.py
> python - <<'PY'
> from pathlib import Path
> import numpy as np,json,hashlib
> r=Path('/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/runs/full-20260903T042000Z')
> m=json.loads((r/'checkpoint_manifest.json').read_text())
> rng=np.random.default_rng(20260906)
> for s in (17,29):
>  key=f'benchmark__HIER_GMM_HARD_R8__seed{s}'
>  row=next(x for x in m['checkpoints'] if x['model_key']==key)
>  p=Path(row['checkpoint_path']); h=hashlib.sha256(p.read_bytes()).hexdigest()
>  a=np.load(r/'evaluations'/f'{key}__intact.npz'); b=np.load(r/'evaluations'/f'{key}__force_label.npz')
>  assert np.array_equal(a['token_count'],b['token_count']) and np.array_equal(a['source'],b['source'])
>  diff=a['loss_sum']-b['loss_sum']; count=a['token_count']
>  draw=rng.integers(0,len(count),(2000,len(count)))
>  delta=diff[draw].sum(1)/count[draw].sum(1)
>  print(json.dumps({'seed':s,'checkpoint_hash_match':h==row['checkpoint_sha256'],'examples':len(count),'answer_tokens':int(count.sum()),'gap':float(diff.sum()/count.sum()),'paired_example_bootstrap_95CI':np.quantile(delta,[.025,.975]).tolist(),'leaf_accuracy':float((a['route']==a['route_target']).mean()),'parent_accuracy':float((a['parent_route']==a['parent_target']).mean()),'forced_accuracy':float((b['route']==b['route_target']).mean()),'unit_exact_same_losses':bool(np.array_equal(a['loss_sum'],np.load(r/'evaluations'/f'{key}__unit.npz')['loss_sum']))}))
> PY`
>
> </details>
>
> 我已从原始评估数组复算出初步结果：两个种子的在线路径都比同一专家库的强制伪标签路径差，差值分别为 **0.040328、0.023130**。代码确认，两条路径的专家系数都为 1，因此这份差距不能归因于概率衰减。
>
> 还发现一个关键区别：这批专家训练时始终由伪标签分发，Router 当时只旁路学习，并不控制专家。因而“早期错误分发把专家训坏”不能解释这批模型的训练过程；更应先查 Router 为什么学不会原分配，以及它读取的位置是否合适。
>
> <details><summary>Explored a list, ran 2 commands</summary>
>
> - Ran `grep -n -A30 'def _route_loss' /data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/training.py
> grep -nE 'register_forward_pre_hook|mlp|capture' /data/250010109/MoE_Router/experiments/20260903_a15_13_e15_true_label_layerwise_static_audit/*.py | head -25
> sed -n '1,36p' /data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/training.py
> sed -n '1,48p' /data/250010109/Research_System/daily_research_reports/0903/focus_sae_hierarchical_teacher_construction.md
> sed -n '1,35p' /data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_15_layerwise_moe_insertion_validation/A15_15_E01_layerwise_semantic_moe_insertion/summary.md
> sed -n '1,65p' /data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E18_dataset_conditioned_sae_semantic_hierarchy/summary.md`
>
> - Ran `python - <<'PY'
> import importlib.util
> print('torch_available',importlib.util.find_spec('torch') is not None)
> PY
> sed -n '205,235p' /data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/training.py
> find /data/250010109/MoE_Router/experiments/20260903_a15_13_e15_true_label_layerwise_static_audit -maxdepth 3 -type f | head -15
> find /data/250010109 -maxdepth 4 -type f -path '*/bin/python*' | head -10`
>
> <details><summary>Explored a file, a list</summary>
>
> - Read `/root/.codex/plugins/cache/openai-curated-remote/superpowers/6.3.0/skills/systematic-debugging/SKILL.md`
> - Listed files in `checkpoints`
>
> </details>
>
> </details>
>
> 审计又发现一个更直接的实现疑点：八任务分支只运行第二阶段，但第二阶段的分类损失只监督细 Router；粗 Router 可能一直没有得到训练信号。我会按 systematic-debugging 技能核对它在各检查点中是否更新，并检查梯度。如果成立，必须先排除这个实现问题，才能把部署差距解释为语义标签或早期表征的问题。
>
> <details><summary>Explored 2 files, a search, ran 2 commands</summary>
>
> - Ran `python - <<'PY'
> from pathlib import Path
> import torch
> r=Path('/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/runs/full-20260903T042000Z/conditions')
> for seed in (17,29):
>  d=r/f'benchmark__HIER_GMM_HARD_R8__seed{seed}'
>  states=[torch.load(p,map_location='cpu',weights_only=False)['adapter'] for p in sorted((d/'checkpoints').glob('*.pt'))]
>  final=torch.load(d/'final.pt',map_location='cpu',weights_only=False)['adapter']
>  print('seed',seed,'snapshots',len(states))
>  for k in ('parent_router.weight','parent_router.bias','leaf_router.weight','leaf_router.bias','parents.A','parents.B'):
>   if k in final:
>    print(k,'unchanged_all',all(torch.equal(s[k],final[k]) for s in states),'first_to_final_maxdelta',float((states[0][k].float()-final[k].float()).abs().max()))
>  print('keys',list(final)[:12])
> PY
> find /data/250010109/MoE_Router/experiments/20260901_a15_13_e07_e08_m2d2_causal_lm_semantic_routing -name routing_model.py
> find /data/250010109/MoE_Router/experiments/20260903_a15_13_e15_true_label_layerwise_static_audit -maxdepth 3 -name '*.py' | head -10`
>
> - Ran `python - <<'PY'
> import ast,sys
> from pathlib import Path
> import torch
> from torch.nn import functional as F
> root=Path('/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap')
> sys.path.insert(0,str(root))
> sys.path.insert(0,'/data/250010109/MoE_Router/experiments/20260901_a15_13_e07_e08_m2d2_causal_lm_semantic_routing')
> from models import HierRouterLoRA,RoutingOutput
> source=ast.parse((root/'training.py').read_text())
> node=next(n for n in source.body if isinstance(n,ast.FunctionDef) and n.name=='_route_loss')
> space={'torch':torch,'F':F,'RoutingOutput':RoutingOutput}
> exec(compile(ast.Module(body=[node],type_ignores=[]),str(root/'training.py'),'exec'),space)
> a=HierRouterLoRA(12,8,rank=2)
> x=torch.randn(2,4,12); h=torch.randn(2,4,8); leaf=torch.tensor([1,5]); parent=torch.tensor([0,1]); labels=torch.ones(2,4,dtype=torch.long)
> o=a(x,h,forced_leaf=leaf,unit_coefficient=True,stage=2)
> (o.delta.square().mean()+space['_route_loss'](o,parent,leaf,labels,2)).backward()
> print('original_stage2_hard_path', {n:None if p.grad is None else float(p.grad.norm()) for n,p in a.named_parameters() if 'router' in n})
> a.zero_grad(set_to_none=True)
> o=a(x,h,forced_leaf=leaf,unit_coefficient=True,stage=2)
> mask=labels[:,1:].ne(-100)
> coarse_loss=F.cross_entropy(o.parent_logits[:,:-1][mask], parent[:,None].expand_as(mask)[mask])
> (o.delta.square().mean()+space['_route_loss'](o,parent,leaf,labels,2)+coarse_loss).backward()
> print('diagnostic_add_parent_supervision', {n:None if p.grad is None else float(p.grad.norm()) for n,p in a.named_parameters() if 'router' in n})
> PY
> grep -nE 'register_forward_pre_hook|mlp' /data/250010109/MoE_Router/experiments/20260903_a15_13_e15_true_label_layerwise_static_audit/scripts/layerwise_static_audit.py | head -15
> date -u`
>
> <details><summary>Explored 3 files, a search</summary>
>
> - Searched for `register_forward_pre_hook|\.mlp\.` in `layerwise_static_audit.py`
> - Read `./MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/training.py`
> - Read `./MoE_Router/experiments/20260901_a15_13_e07_e08_m2d2_causal_lm_semantic_routing/routing_model.py`
> - Read `/root/.codex/plugins/cache/openai-curated-remote/superpowers/6.3.0/skills/verification-before-completion/SKILL.md`
>
> </details>
>
> </details>
</details>

**你的两个假设都值得保留，但现在应先排除一个已经查实的训练问题：八任务硬伪标签实验中的粗 Router 没有得到梯度。** 因此，当前不能把全部部署损失解释为“末层标签误导了前层”。

三个对话已读取，并核对了本地代码、检查点和原始评估数组。以下先给认知纠正，再给验证顺序和今天 **18:30（北京时间）** 前后的安排。

**先更新已有认识**

本次只读审计发现：

- 八任务实验没有先训练粗路由阶段，只执行了第二阶段。
- 第二阶段的分类损失只监督细 Router。
- 硬伪标签路径直接决定专家，且专家系数为 1，任务损失也无法通过这条路径训练粗 Router。
- 两个种子的粗 Router 权重、偏置，在第 1 次更新至最终检查点之间**完全不变**；细 Router 则有更新。
- 使用实际模块做最小反向计算，粗 Router 梯度确实为 `None`；补入粗分类监督后才出现梯度。

代码依据：[监督损失与路径设置](/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/training.py:222)。

同时，我复算了同一专家库的答案词元负对数似然（NLL，即平均预测损失，越低越好）：

| 种子 | 原在线路径 | 强制原伪标签路径 | 在线路径多出的损失 |
|---|---:|---:|---:|
| 17 | 0.845991 | 0.805663 | +0.040328 |
| 29 | 0.827523 | 0.804393 | +0.023130 |
| 平均 | 0.836757 | 0.805028 | **+0.031729** |

**差距真实存在，但其中包含“粗 Router 没有训练”的实现因素。修复后还能剩下多少差距，才是语义交接问题的下一份证据。** 这项发现限定于上述八任务硬伪标签分支，不能直接推广到采用两阶段训练的 M2D2 实验。

对你的两个假设，建议这样改写：

| 原假设 | 更准确、可验证的版本 |
|---|---|
| 末层语义干扰当层；当层标签可能更好 | **在相同上下文范围、相同标签构造方法下，当层教师是否比末层教师更容易被路由器预测，并保留任务价值？** |
| 早期表征读出造成 Router 错训 | 分别检验：**浅层输入不易读出、序列早期信息不足、训练早期错误分发影响专家责任**。三者需要不同实验。 |

这里有三个关键区别。

第一，**层深与上下文范围是两个变量**。末层当前词元状态仍然是因果的，只能看见前缀；整窗平均则可能使用当前位置之后的信息。换成“当层整窗标签”，仍然没有消除未来信息问题。

第二，**容易预测的标签不一定值得分发**。从当层状态直接聚类，再用同一状态预测簇编号，可能只是学会了几何分区；必须另测专家和任务收益。

第三，**“训练早期错误分发训坏专家”不适用于这批硬伪标签专家**：训练期间实际分发始终由教师控制，Router 只在旁路学习。这个假设适用于由学习中 Router 控制专家的另一类训练。

此外，旧静态审计读取的是**多层感知机调用前状态**，上述部署 Router 实际读取的是**整个 Transformer 块进入时的状态**。两者之间隔着该块的注意力计算等操作。不能直接用旧审计曲线证明部署 Router 已经拿到了同一种输入。[部署读取位置](/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/training.py:110)

**本次术语：训练了什么，是否控制分发**

| 对象 | 具体含义 | 是否训练 | 是否实际控制专家 |
|---|---|---|---|
| 离线教师 | 生成分组标签的聚类器或稀疏自编码器（SAE）及其分组规则 | 构造时可能训练；使用时冻结 | 强制教师路径时控制 |
| 读出探针 | 检查某个表示能否预测标签的小分类器 | **训练分类器**，冻结基座 | 否 |
| 影子 Router | 按教师标签学习，但暂不控制前向分发的路由器 | **训练 Router** | 训练时否 |
| 在线 Router | 根据当前可见信息实际选择专家 | 可以训练，也可以冻结评估 | 是 |
| 强制路径评估 | 外部指定专家编号，再测任务损失 | **不训练任何参数** | 外部编号控制 |
| Oracle 参考 | 使用真实类别指定路径的实验参考 | 专家通常另行训练；评估时冻结 | 真实类别控制 |
| 联合训练 | Router 与专家一起更新 | **训练 Router＋专家** | 取决于教师交接安排 |

**“冻结模型审计”不等于完全不训练：它可以训练探针。真正的区别是，是否更新基座、专家，以及分类器是否控制实际分发。** Oracle 也不是逐词元损失最优路径的数学保证。

**接下来的验证：四步，每步按“目的—假设—方法—结论分支”说明**

**第一步：训练与路径完整性审计——先确认比较对象有效。**

- **目的：**排除实现缺口，确定部署损失由哪一级路径产生。
- **假设：**未训练的粗 Router 是当前差距的重要来源。
- **方法：**冻结同一专家库和全部 Router，比较“预测粗＋预测细”“强制教师粗＋预测细”“强制教师粗＋教师细”，全部保持单位专家系数；再补“教师粗＋同父错误细”对照。
- **结论分支：**只强制粗路径就明显恢复，优先修复粗路由；强制细路径还带来明显恢复，再处理细路由。如果教师细路径并不优于错误细路径，就不能认定原标签与细专家具有可靠匹配。

**训练对象：无。** 本次已完成梯度、参数变化和原始损失复算；新增的粗路径单独干预尚未运行。

---

**第二步：固定专家，只修复 Router——先区分训练缺口与读出困难。**

- **目的：**检验完整训练的因果 Router 能追回多少收益。
- **假设：**补全粗细监督可以缩小差距；若历史信息读取仍不足，因果前缀摘要还能带来额外收益。
- **方法：**固定旧专家、旧标签、插入层和专家系数，按顺序比较：

| 条件 | Router 输入／训练变化 | 保护哪种解释 |
|---|---|---|
| 原模型 | 原样评估 | 历史参照 |
| 完整监督的当前词元 Router | 原输入；补全粗细监督 | 排除训练不完整 |
| 完整监督的前缀 Router | 当前状态＋截至当前位置的历史平均 | 检验历史读取方式 |
| 整窗读出诊断 | 允许读取整窗摘要 | 测量非因果信息的帮助，不能部署 |

当前词元与前缀条件匹配分类器容量、数据顺序和更新预算。先用分类损失训练影子 Router，再接入冻结专家评估。

- **结论分支：**当前词元修复已恢复大部分收益，就先修训练；前缀在相同预算外进一步降低任务损失，才支持历史读出机制。若只提高标签准确率、不降低任务损失，则应检查监督目标的功能价值。

**训练对象：只有 Router。基座与所有专家冻结。**

主要比较是：

\[
\Delta_{\text{前缀}}
=
L_{\text{完整监督当前词元}}
-
L_{\text{完整监督前缀}}.
\]

只有它为正，才说明前缀方案优于公平的当前词元对照。

---

**第三步：拆开教师层位与上下文范围——正式检验你的第一个假设。**

- **目的：**区分“末层来源不合适”和“整窗标签不适合当前前缀”。
- **假设：**限制为因果前缀后，当层教师仍可能比末层教师更适合在线预测。
- **方法：**固定 Router 插入位置和聚类方法，只做以下四格教师审计：

| 教师来源 | 整窗平均 | 因果前缀平均 |
|---|---|---|
| 末层 | 旧方案参照 | 隔离上下文范围 |
| Router 对应的具体输入位置 | 隔离层位 | 同时对齐层位与上下文 |

拟合只使用训练集。先检查分组稳定性、覆盖和留出数据上的可预测性；同层同输入构造的标签，要特别防止把“学会簇边界”解释为语义发现。

- **结论分支：**两种层位都因前缀化改善，首先支持上下文错位；固定前缀后当层仍更好，才支持层位匹配的读出优势。**两者都不能单独证明任务收益。**

**训练对象：聚类器及审计探针；此步不训练专家，也不部署新 Router。**

新标签改变了专家责任含义，不能把新簇编号直接塞进旧专家库证明有效。当前 SAE 也尚未形成完整可靠教师，不适合在这里同时替换聚类方法。[SAE 现有边界](../../../../experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E18_dataset_conditioned_sae_semantic_hierarchy/summary.md:14)

---

**第四步：功能与训练责任验证——最后判断是否成为方法。**

- **目的：**检验候选标签和交接方案是否真正改善可部署模型。
- **假设：**合格教师能塑造有用专家，完整训练的 Router 能保留这份价值。
- **方法：**只选前面胜出的一个候选，匹配训练预算比较任务损失训练、旧教师、新教师及频率匹配随机分组。分别报告教师强制路径与在线路径，并做删除、同父换错专家干预。若要检验“训练早期错误分发”，再对同一教师比较“从开始由 Router 分发”与“教师先分发、逐步交接”，保持初始化及预算匹配。
- **结论分支：**教师路径有效、在线失败，问题仍在交接；教师路径也无优势，停止优化标签恢复率；在线稳定优于匹配基线，才进入更大预算验证。

**训练对象：Router＋专家；本轮仍冻结基座。** 不同时扩大扫层、SAE 和注意力头实验。

**今天 18:30 前后的新安排**

| 北京时间 | 优先行为 | 应得到什么 |
|---|---|---|
| **现在：已完成** | 检查点核验、损失复算、粗 Router 梯度与权重审计 | 已确认训练缺口；保留真实部署差距 |
| 现在—17:00 | 优先补第一步的粗路径单独干预；检查可用运行资源 | 判断粗路径能解释多少损失 |
| 17:00—18:15 | 在吞吐允许时，先跑第二步的“完整监督当前词元”小预算修复 | 一个修复后的参照，先不混入新标签 |
| 18:15—18:30 | 汇总已完成结果、未完成项和耗时 | 供你开始工作时裁决 |
| **18:30—19:00** | 你检查修复恢复量与剩余差距 | 决定继续读出对照，还是进入教师审计 |
| 19:00 以后 | 按结果推进一个分支 | 前缀读出对照优先；教师四格后置 |

这张表是执行优先级，完成时间需由实测吞吐决定。**本轮已经运行的是只读审计和最小梯度验证，尚未修改训练代码或启动新训练。**

你在 18:30 首先需要回答的问题应收缩为：**“粗细 Router 都得到完整训练以后，同一专家库还剩多少在线交接损失？”** 这个答案会直接决定你的两个语义假设是否值得进入下一轮。

> 请给出第一步粗路径干预的具体计划，并且对应上具体4步规划

**第一步只做一件事：固定现有专家和 Router，外部纠正粗路径，测量任务损失能恢复多少。全程不训练参数。** 它对应四步规划中的“训练与路径完整性审计”，结果决定第二步先修粗 Router，还是同时处理细 Router。

**1. 目的**

判断已有的平均 **0.031729 NLL 部署差距**，有多少能通过“给定正确的伪标签粗路径”恢复，以及细专家是否真的与原伪标签匹配。

这里“正确”指**这批专家训练时使用的原伪标签**，不是人工真实类别，也不是重新生成的标签。

**2. 假设**

- **主要假设：**粗 Router 没有得到训练，使输入进入错误父组；强制原教师粗路径后，即使保留现有细 Router，也能明显降低任务损失。
- **竞争解释：**纠正粗路径仍不够，细 Router 也无法恢复教师分配；或者原伪标签细分本身缺乏专家功能价值。

**3. 分析方法**

固定八任务硬伪标签模型的两个种子 `17、29`，使用原来的 **512 条评估样本、30,442 个答案词元**。基座、语言头、共享专家、粗细专家、粗细 Router、标签及样本顺序全部冻结。所有条件的专家系数固定为 **1**。

运行以下四个条件：

| 条件 | 粗路径 | 细路径 | 回答的问题 |
|---|---|---|---|
| A：原在线路径 | 粗 Router 预测 | 在预测父组内，由细 Router 选择 | 原始部署损失是多少？ |
| B：只纠正粗路径 | **原教师粗标签** | **在教师父组内，重新由细 Router 选择** | 纠正父组能恢复多少？ |
| C：完整教师路径 | 原教师粗标签 | 原教师细标签 | 剩余细路径差距是多少？ |
| D：教师粗＋错误细 | 原教师粗标签 | 同父组内的其他细专家 | 原教师细专家是否真的更合适？ |

**B 的实现是关键：不能保留 A 选出的细专家。** A 的细专家可能属于错误父组；B 必须先把候选集合限制到教师父组，再用原细 Router 的分数重新选择。

D 使用实际标签文件中的父子映射。同父其他细专家逐一评估后取平均，避免只选某一个错误专家造成偏差；不改动该父组的粗专家。

具体执行分三项：

1. **先验证路径。** 检查 B 的父组全部等于教师父组、细专家全部属于该父组；C 完整匹配教师标签；D 保持父组不变且细专家不同。确认全部参数未更新、系数均为 1。
2. **统一前向评估。** 四个条件都在完整序列前向中应用路径干预，只在原答案掩码上计算损失；不能只改统计出来的路径记录。A、C 同时作为重放检查，与已有结果核对。
3. **逐样本配对分析。** 保存每条样本的损失总和、答案词元数、路径和任务来源；分别报告两个种子，并做 2,000 次样本级配对重采样，给出 95% 区间。

记四个条件的平均答案词元损失为 \(L_A,L_B,L_C,L_D\)，核心量是：

\[
\Delta_{\text{粗纠正}}=L_A-L_B
\]

表示**纠正父组，并让现有细 Router 在正确父组内选择**的收益。

\[
\Delta_{\text{细纠正}}=L_B-L_C
\]

表示父组正确以后，继续提供教师细标签的额外收益。

\[
\Delta_{\text{细匹配}}=L_D-L_C
\]

表示教师细专家是否优于同父错误专家。

三者均以正值为有利信号。另报告：

\[
R_{\text{粗纠正}}
=\frac{L_A-L_B}{L_A-L_C}.
\]

这是沿该干预顺序的恢复比例，**不是“粗 Router 独立解释了多少因果方差”**。纠正粗路径会同时改变粗专家和可选细专家，恢复比例也可能小于 0 或大于 100%，应原样报告。

**4. 结论分支，以及如何接上后续三步**

| 第一步的结果 | 可得到的结论 | 下一步行为 |
|---|---|---|
| B 接近 C，且两种子均明显优于 A | 给定教师父组后，现有细 Router 已能恢复大部分路径价值 | **第二步优先只训练粗 Router**，其余冻结；检验它能否在线复现 B |
| B 优于 A，但仍明显差于 C | 粗路由和父组内细路由都有缺口 | **第二步训练完整粗细 Router**；先用原当前词元输入建立修复基线 |
| B 与 A 接近，但 C 明显更好 | 只纠正父组不足，细路径是主要剩余问题 | 第二步重点检查细分类目标、父组约束与因果可预测性 |
| C 不稳定优于 D | 尚未证明教师细标签对应更合适的细专家 | 暂缓扩大交接训练，先查标签—专家匹配；不能只追求标签准确率 |
| B 比 A 更差 | 粗细路径存在交互或不匹配 | 先检查干预实现及逐任务差异，不直接解释为“粗语义无用” |
| 两种子相反或区间跨零 | 当前证据不足 | 保留不确定结论，不据此换教师或扩模型 |

与整体四步的对应关系是：

| 总体步骤 | 本步结束时要回答什么 | 训练对象 |
|---|---|---|
| **① 粗路径干预：本次计划** | 外部纠正哪一级路径能恢复收益？ | **不训练** |
| **② 固定专家修复 Router** | 完整训练的因果 Router 能否自行恢复这些路径收益？ | **只训练 Router** |
| **③ 教师层位 × 上下文审计** | 第二步仍有差距时，是教师层位还是上下文范围不合适？ | **拟合教师、训练探针；不训练专家** |
| **④ 功能与交接训练验证** | 候选方案能否产生优于匹配基线的可部署收益？ | **训练 Router＋专家，冻结基座** |

**第一步的交付物就是一张四条件损失表、一张三个干预差值图，以及一个第二步选择。** 对应原定 18:30 的决策节点，优先完成这份结果；此时不需要重训 SAE、生成新标签或重新扫描层位。

> 认同你的执行顺序，我们现在先开始执行第一步骤，将路径修复，然后进行架构审计

<details><summary>13 previous messages</summary>

> 我会先核对研究任务归属和执行协议，再落实第一步的四种路径干预。随后检查粗细路由监督、输入读取位置和训练阶段是否一致，用审计结果决定后续修复范围。
>
> <details><summary>Explored 2 files, ran a command</summary>
>
> <details><summary>Explored 4 files</summary>
>
> - Read `./PROJECTS.md`
> - Read `./daily_research_reports/0903/focus_gmm_pseudolabel_oracle_gap.md`
> - Read `./.agents/skills/experiment-card-writer/SKILL.md`
> - Read `./.agents/skills/remote-experiment-workflow/SKILL.md`
>
> </details>
>
> - Ran `cat .agents/skills/experiment-card-writer/SKILL.md
> cat .agents/skills/research-progress-core/SKILL.md
> sed -n '1,130p' Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_05_gmm_pseudolabel_oracle_gap_anchor.md
> find daily_research_reports -name '*handoff*' -o -name '*gmm*'
> git status --short`
>
> </details>
>
> 我会使用实验协议和远程执行技能，把你刚批准的四条件方案写入正式协议后执行。当前被其他任务占用的是逐层静态审计和 SAE 构造；这次处理的是原八任务伪标签模型的路径交接问题，我会单独登记归属，保留它们的记录。
>
> <details><summary>Created 3 files, edited a file, explored 3 files, ran 5 commands</summary>
>
> - Ran `cat .agents/skills/experiment-card-writer/references/blockwise_protocol_audit.md
> cat .agents/skills/experiment-card-writer/references/protocol_self_containment_and_freeze.md
> cat /root/.codex/skills/sco-control/SKILL.md
> python - <<'PY'
> import torch
> print('torch',torch.__version__,'cuda',torch.cuda.is_available())
> if torch.cuda.is_available():
>  print(torch.cuda.get_device_name(0))
>  print(torch.empty(1,device='cuda'))
> PY
> sed -n '1,130p' /data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/submit_h100_4_reserved.sh
> find /data/250010109/MoE_Router -maxdepth 2 -name AGENTS.md -print`
>
> <details><summary>Explored 5 files</summary>
>
> - Read `/data/250010109/MoE_Router/experiments/20260901_a15_13_e07_e08_m2d2_causal_lm_semantic_routing/runtime.py`
> - Read `/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/run_pipeline.sh`
> - Read `/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/training.py`
> - Read `/root/.codex/plugins/cache/openai-curated-remote/superpowers/6.3.0/skills/test-driven-development/SKILL.md`
> - Read `/root/.codex/plugins/cache/openai-curated-remote/superpowers/6.3.0/skills/using-git-worktrees/SKILL.md`
>
> </details>
>
> - Ran `grep -n -A38 'def load_backbone' /data/250010109/MoE_Router/experiments/20260901_a15_13_e07_e08_m2d2_causal_lm_semantic_routing/runtime.py
> python - <<'PY'
> import transformers,torch
> print(transformers.__version__)
> print(torch.cuda.mem_get_info())
> PY
> sed -n '1,125p' /data/250010109/MoE_Router/experiments/20260730_h768_4layer_switch_5090_smoke/scripts/activate_runtime_layer.sh
> ls /data/250010109/dependency_packages
> cat .agents/skills/experiment-card-writer/references/result_evidence_lineage.md
> cat .agents/skills/experiment-card-writer/references/detailed_record_standard.md
> cat .agents/skills/experiment-card-writer/references/plain_language_completion_reply.md`
>
> - Ran `PYTHONPATH=/data/250010109/dependency_packages/a15_e14_datasets_py310:/data/250010109/dependency_packages/hf_transformers_qwen3 python - <<'PY'
> import transformers,torch
> print(transformers.__version__)
> print(torch.cuda.mem_get_info())
> from transformers import AutoModelForCausalLM
> print('import_ok')
> PY
> sed -n '1,35p' Projects/graphs/expert_specialization.graph.yaml
> ls /data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/tests`
>
> - Wrote `./Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P1_coarse_path_intervention/protocol.md` (+63 -0)
> - Wrote `./daily_research_reports/0906/focus_gmm_pseudolabel_handoff.md` (+53 -0)
>
> - Wrote `./PROJECTS.md` (+1 -0)
>
> - Wrote `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/test_intervention.py` (+53 -0)
>
> - Ran `python -m pytest -q /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/test_intervention.py`
>
> - Ran `PYTHONPATH=/data/250010109/dependency_packages/hf_transformers_qwen3 python - <<'PY'
> import sys
> sys.path.append('/data/250010109/dependency_packages/a15_e14_datasets_py310')
> import numpy,torch,transformers
> print(numpy.__version__,torch.__version__,transformers.__version__)
> from transformers import AutoModelForCausalLM
> print('import_ok',torch.cuda.mem_get_info())
> PY`
>
> </details>
>
> 已登记本任务并保存你批准的协议。当前容器有可用的 40GB 显存分区，可以直接评估。实现上需要补通一个入口：原模型内部支持指定粗路径，但外层调用没有把它传进去；我会补上并验证，确保指定父组后，细 Router 在该组内重新选择。
>
> <details><summary>Created 2 files, edited a file, ran 6 commands</summary>
>
> - Wrote `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/intervention.py` (+52 -0)
> - Ran `python -m pytest -q /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/test_intervention.py`
> - Wrote `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/run_audit.py` (+204 -0)
> - Ran `python /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/run_audit.py --output /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/runs/smoke-v1 --limit 8`
> - Ran `python - <<'PY'
> from pathlib import Path
> import re
> paths=[Path('daily_research_reports/0906/focus_gmm_pseudolabel_handoff.md'),Path('Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P1_coarse_path_intervention/protocol.md')]
> for f in paths:
>  for dest in re.findall(r'\]\(([^)]+)\)',f.read_text()):
>   print(str(f),dest,(f.parent/dest).resolve().exists())
> PY`
> - Wrote `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/run_audit.py` (+1 -0)
> - Ran `python /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/run_audit.py --output /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/runs/smoke-v2 --limit 8`
> - Ran `python - <<'PY'
> from pathlib import Path
> import json
> root=Path('/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/runs/full-20260903T042000Z')
> m=json.loads((root/'checkpoint_manifest.json').read_text())
> print(json.dumps(m['reused_models'],indent=2)[:2000])
> PY`
> - Ran `python - <<'PY'
> import json
> from pathlib import Path
> r=Path('/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/runs/smoke-v2')
> m=json.loads((r/'metadata.json').read_text()); print(json.dumps(m['replay'],indent=2))
> PY
> ls /usr/local/bin/python* /usr/bin/python*`
>
> </details>
>
> 路径入口测试已通过，但本地重放未通过：样本、掩码和专家编号都一致，原在线损失却相差约 0.00354，超过预先固定的容差。我已停止本地完整评估。接下来会核对权重和数值环境，优先使用原实验的运行环境复现，不放宽判定标准。
>
> <details><summary>Created 2 files, explored 2 files, a list, ran 4 commands</summary>
>
> - Ran `cat /root/.codex/skills/sco-control/references/acp.md
> sed -n '1,170p' /data/250010109/MoE_Router/experiments/20260730_h768_4layer_switch_5090_smoke/scripts/sco_acp_compat.sh
> find /data/250010109/MoE_Router/experiments/20260903_a15_13_e15_true_label_layerwise_static_audit -maxdepth 3 -name '*submit*'
> python - <<'PY'
> from pathlib import Path
> import hashlib,json
> p=Path('/data/250010109/model_cache/Qwen3-0.6B-Base-official')
> for name in ('model.safetensors','config.json'):
>  h=hashlib.sha256()
>  with (p/name).open('rb') as f:
>   for b in iter(lambda:f.read(1<<20),b''):h.update(b)
>  print(name,h.hexdigest())
> PY`
>
> - Ran `sed -n '1,100p' /data/250010109/MoE_Router/experiments/20260903_a15_13_e15_true_label_layerwise_static_audit/scripts/submit_h100_1_spot.sh
> bash /data/250010109/MoE_Router/experiments/20260730_h768_4layer_switch_5090_smoke/scripts/sco_acp_compat.sh jobs list --workspace-name=share-space --page-size=5 -o json`
>
> <details><summary>Explored 2 files, a list</summary>
>
> - Read `/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/resume_unified_evaluation.sh`
> - Listed files in `logs`
> - Read `/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/runs/full-20260903T042000Z/completion_audit.json`
>
> </details>
>
> - Ran `python /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/run_audit.py --output /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/runs/smoke-batch8 --limit 8 --batch 8`
>
> - Wrote `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/run_remote.sh` (+13 -0)
> - Wrote `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/submit_evaluation.sh` (+20 -0)
>
> - Ran `bash /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/submit_evaluation.sh
> python -m pytest -q /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/test_intervention.py`
>
> </details>
>
> 基座和适配器的文件指纹均与原实验一致；改回原批大小后，重放仍未通过。已准备好使用原 PyTorch 2.8／CUDA 12.9 镜像的单张 H100 评估作业，包含小样本重放、四条件评估和 90 分钟进程上限，尚未提交。
>
> 这里只需确定新增算力的配额类型。SCO 的[资源规则](/root/.codex/skills/sco-control/references/acp.md)要求“Use `--quota-type spot` only when the user explicitly wants idle resources and accepts possible interruption”；之前批准的协议也仅登记了本地显卡，因此需要补这一项资源选择。
>
> 第一步评估将使用原运行镜像和单张 H100，最多运行 90 分钟、不训练参数。请选择配额类型：
> - 标准配额 reserved：按原实验配额类型执行
> - 空闲配额 spot：接受中断后重跑
>
> <details><summary>Created a file, ran 2 commands</summary>
>
> - Wrote `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/analyze.py` (+107 -0)
> - Ran `python - <<'PY'
> from pathlib import Path
> import json
> r=Path('/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/runs')
> for name in ('smoke-v1','smoke-v2','smoke-batch8'):
>  p=r/name/'metadata.json'
>  m=json.loads(p.read_text())
>  m['status']='FAILED_PREFLIGHT' if name=='smoke-v1' else 'FAILED_REPLAY'
>  m['failure_reason']='Incompatible ONNX protobuf import before model load' if name=='smoke-v1' else 'Historical A replay NLL differs beyond fixed 1e-4 tolerance'
>  p.write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
>  print(name,m['status'],m.get('replay'))
> PY`
> - Ran `python - <<'PY'
> from pathlib import Path
> import json,csv
> src=Path('/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/runs/smoke-batch8/architecture_audit.json')
> a=json.loads(src.read_text())
> out=Path('Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P1_coarse_path_intervention/tables')
> out.mkdir(exist_ok=True)
> rows=[]
> for seed,record in a['snapshots'].items():
>  for key,v in record['parameters'].items():rows.append({'seed':seed,'parameter':key,**v})
> with (out/'architecture_weight_audit.csv').open('w') as f:
>  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
> with (out/'architecture_gradient_audit.csv').open('w') as f:
>  w=csv.writer(f);w.writerow(['condition','parameter','gradient_is_none','gradient_norm'])
>  for c in ['original_gradient_norms','diagnostic_parent_loss_gradient_norms']:
>   for k,v in a[c].items():w.writerow([c,k,v is None,v])
> print('Architecture evidence tables written; no repaired checkpoint produced.')
> PY
> bash -n /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/run_remote.sh /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/submit_evaluation.sh
> python -m py_compile /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/intervention.py /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/run_audit.py /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/analyze.py`
>
> </details>
>
> 架构审计再次确认了两点：粗 Router 在全部七个保存点中都没有变化，原硬伪路径训练下也没有梯度；实际 Router 读取的是注意力之前的块输入，旧静态审计读取的则是注意力之后的多层感知机输入。两者不能当作同一个表示来比较。我已保存这些证据，并修好本步的粗路径干预入口；损失恢复量仍须等重放通过后才能报告。
>
> <details><summary>Created 2 files, edited 2 files, ran a command</summary>
>
> - Wrote `./Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P1_coarse_path_intervention/detailed.md` (+70 -0)
> - Wrote `./Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P1_coarse_path_intervention/protocol.md` (+6 -0)
> - Wrote `./Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P1_coarse_path_intervention/summary.md` (+23 -0)
> - Wrote `./daily_research_reports/0906/focus_gmm_pseudolabel_handoff.md` (+3 -1)
> - Ran `git diff --check
> python - <<'PY'
> from pathlib import Path
> import re
> root=Path('/data/250010109/Research_System')
> files=[root/'daily_research_reports/0906/focus_gmm_pseudolabel_handoff.md']+list((root/'Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P1_coarse_path_intervention').glob('*.md'))
> bad=[]
> for f in files:
>  for p in re.findall(r'\]\(([^)]+)\)',f.read_text()):
>   if not p.startswith(('http:','https:','#')) and not (f.parent/p).resolve().exists():bad.append((str(f),p))
> print('checked_markdown_files',len(files),'broken_links',bad)
> assert not bad
> PY`
>
> </details>
</details>

**粗路径干预入口已修复，两个功能测试通过；完整评估尚未开始。**

架构审计确认：

- 八任务硬伪路径训练中的粗 Router 没有梯度，七个检查点的参数完全不变。
- 实际 Router 与旧静态审计读取的位置不同。
- 本地重放损失未通过固定容差，已停止扩大运行，避免产生不可比结果。

已保存[审计记录](../../../../experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P1_coarse_path_intervention/summary.md)，并准备好原运行镜像下的单张 H100 评估作业。

**请在上面的选项中选择标准配额或空闲配额，随后即可提交。**

需要这项选择，是因为原协议只登记了本地显卡；[SCO 资源规则](/root/.codex/skills/sco-control/references/acp.md)要求空闲配额必须由用户明确选择并接受可能中断。此次无需重新确认实验设计。

> 选择标准配额，开始执行实验

<details><summary>16 previous messages</summary>

> 我会用标准配额提交单张 H100 作业，先验证原环境的小样本重放，通过后自动运行四条件、两个种子的完整评估。
>
> <details><summary>Edited 2 files, ran 3 commands</summary>
>
> - Ran `sed -n '20,39p' PROJECTS.md
> sed -n '1,85p' daily_research_reports/0906/focus_gmm_pseudolabel_handoff.md
> tail -22 Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P1_coarse_path_intervention/protocol.md
> cat /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/run_remote.sh`
> - Wrote `./Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P1_coarse_path_intervention/protocol.md` (+2 -0)
> - Wrote `./daily_research_reports/0906/focus_gmm_pseudolabel_handoff.md` (+2 -2)
> - Ran `ALLOW_SUBMIT=1 EVAL_QUOTA=reserved RUN_STAMP=reserved-20260906-p1-v1 bash /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/submit_evaluation.sh`
> - Ran `bash /data/250010109/MoE_Router/experiments/20260730_h768_4layer_switch_5090_smoke/scripts/sco_acp_compat.sh jobs describe --workspace-name=share-space -o json pt-a4qkvyya`
>
> </details>
>
> 作业 **pt-a4qkvyya** 已启动：单张 H100、标准配额。它会先核对旧路径的损失重放，通过后再评估四种路径；本步不更新模型参数。
>
> <details><summary>Edited 2 files, explored 3 files, ran 3 commands</summary>
>
> - Wrote `./Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P1_coarse_path_intervention/protocol.md` (+2 -0)
> - Wrote `./daily_research_reports/0906/focus_gmm_pseudolabel_handoff.md` (+3 -1)
>
> - Ran `tail -10 /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/runs/reserved-20260906-p1-v1/smoke.log
> cat /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/runs/reserved-20260906-p1-v1/tests.log`
>
> - Ran `find /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/runs/reserved-20260906-p1-v1 -maxdepth 2 -type f -print
> bash /data/250010109/MoE_Router/experiments/20260730_h768_4layer_switch_5090_smoke/scripts/sco_acp_compat.sh jobs stream-logs --workspace-name=share-space pt-a4qkvyya`
>
> - Ran `tail -12 /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/runs/reserved-20260906-p1-v1/smoke.log
> python - <<'PY'
> from pathlib import Path
> import json
> r=Path('/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/runs/reserved-20260906-p1-v1')
> for role in ('smoke','full'):
>  p=r/role/'metadata.json'
>  if p.exists():
>   m=json.loads(p.read_text()); print(role,m['status'],m.get('replay'),m.get('elapsed_seconds'))
> PY`
>
> <details><summary>Explored 3 files</summary>
>
> - Read `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/runs/reserved-20260906-p1-v1/smoke.log`
> - Read `/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/training.py`
> - Read `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/intervention.py`
>
> </details>
>
> </details>
>
> 原环境中的在线路径和完整教师路径已精确重放，损失、路径和掩码均与旧结果一致。小样本检查还发现了新干预入口的一个问题：指定粗路径后，外层调用又把它清空了。我会补上贯穿外层调用的回归测试，修复后用相同配置重跑。
>
> <details><summary>Edited 3 files, ran 6 commands</summary>
>
> - Wrote `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/test_intervention.py` (+48 -0)
> - Ran `python -m pytest -q /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/test_intervention.py`
> - Wrote `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/intervention.py` (+1 -2)
> - Ran `python -m pytest -q /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/test_intervention.py`
> - Ran `python - <<'PY'
> import subprocess,json
> c=['bash','/data/250010109/MoE_Router/experiments/20260730_h768_4layer_switch_5090_smoke/scripts/sco_acp_compat.sh','jobs','describe','--workspace-name=share-space','-o','json','pt-a4qkvyya']
> m=json.loads(subprocess.check_output(c,text=True));print(m['name'],m['state'])
> PY`
> - Wrote `./Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P1_coarse_path_intervention/protocol.md` (+2 -0)
> - Ran `ALLOW_SUBMIT=1 EVAL_QUOTA=reserved RUN_STAMP=reserved-20260906-p1-v2 bash /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/submit_evaluation.sh`
> - Ran `python - <<'PY'
> from pathlib import Path
> import json
> p=Path('/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/runs/reserved-20260906-p1-v1/smoke/metadata.json')
> m=json.loads(p.read_text());m['status']='FAILED_PATH_GUARD';m['failure_reason']='B forced parent overwritten by outer wrapper; repaired in v2, no full evaluation';p.write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
> PY`
> - Ran `python - <<'PY'
> import json,subprocess
> from pathlib import Path
> c=['bash','/data/250010109/MoE_Router/experiments/20260730_h768_4layer_switch_5090_smoke/scripts/sco_acp_compat.sh','jobs','describe','--workspace-name=share-space','-o','json','pt-5xgwtcam']
> m=json.loads(subprocess.check_output(c,text=True));print('job',m['name'],m['state'],m.get('start_time'))
> r=Path('/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/runs/reserved-20260906-p1-v2')
> for name in ('tests.log','smoke.log','full.log'):
>  p=r/name
>  if p.exists():print(name,p.read_text()[-1800:])
> PY`
>
> </details>
>
> 替代作业 **pt-5xgwtcam** 已通过全部小样本检查：两个种子的旧路径损失都精确复现，指定粗路径正确生效，模型参数保持冻结。现在已进入完整评估。
>
> <details><summary>Edited 2 files, ran 2 commands</summary>
>
> - Wrote `./Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P1_coarse_path_intervention/protocol.md` (+2 -0)
> - Wrote `./daily_research_reports/0906/focus_gmm_pseudolabel_handoff.md` (+1 -1)
> - Ran `python - <<'PY'
> from pathlib import Path
> import json
> r=Path('/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/runs/reserved-20260906-p1-v2')
> p=r/'full.log'
> print(p.read_text()[-1200:])
> PY`
> - Ran `python - <<'PY'
> from pathlib import Path
> import json
> r=Path('/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/runs/reserved-20260906-p1-v2')
> print((r/'full.log').read_text().replace('\x00','')[-1400:])
> m=json.loads((r/'full/metadata.json').read_text()); print('status',m['status'], 'replay',[(k,v['pass']) for k,v in m['replay'].items()])
> PY`
>
> </details>
>
> Context compaction
>
> Source: automatic
> Status: completed
>
> <details><summary>Ran 2 commands</summary>
>
> - Ran `python /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/analyze.py --run /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/runs/reserved-20260906-p1-v2/full --output /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/runs/reserved-20260906-p1-v2/analysis`
> - Ran `git status --short`
>
> </details>
>
> 完整评估已经完成。只替换粗路径、让原 Router 在该粗类内重新选择细专家，就恢复了两个种子分别 **98.2% 和 94.0%** 的离线—在线损失差距。本次没有训练任何参数；我正在核对统计结果与架构证据，随后写入结果记录。
>
> <details><summary>Explored 3 files, ran 3 commands</summary>
>
> - Ran `python - <<'PY'
> import subprocess,json,pathlib
> p='/data/250010109/MoE_Router/experiments/20260730_h768_4layer_switch_5090_smoke/scripts/sco_acp_compat.sh'
> m=json.loads(subprocess.check_output(['bash',p,'jobs','describe','--workspace-name=share-space','-o','json','pt-5xgwtcam'],text=True));print({k:m.get(k) for k in ['name','state','start_time','end_time']})
> w=pathlib.Path('/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention')
> print((w/'analyze.py').read_text())
> PY`
>
> <details><summary>Explored 3 files</summary>
>
> - Read `./daily_research_reports/0906/focus_gmm_pseudolabel_handoff.md`
> - Read `./Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P1_coarse_path_intervention/summary.md`
> - Read `./Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P1_coarse_path_intervention/detailed.md`
>
> </details>
>
> - Ran `python - <<'PY'
> from pathlib import Path
> p=Path('/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/analyze.py')
> s=p.read_text().replace("tokens = data['A']['token_count']", "for values in data.values():\n            values['loss_sum'] = values['loss_sum'].astype(np.float64)\n            assert np.isfinite(values['loss_sum']).all()\n            assert np.array_equal(data['A']['sample_index'], values['sample_index'])\n        tokens = data['A']['token_count']")
> p.write_text(s)
> PY
> python /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/analyze.py --run /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/runs/reserved-20260906-p1-v2/full --output /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/runs/reserved-20260906-p1-v2/analysis`
>
> - Ran `cat /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/runs/reserved-20260906-p1-v2/full/metadata.json; cat /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/runs/reserved-20260906-p1-v2/full/architecture_audit.json; tail -45 Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P1_coarse_path_intervention/protocol.md; grep -n -E 'gmm_pseudolabel_handoff|STEP1_RESERVED' PROJECTS.md`
>
> </details>
>
> Viewed 2 images
>
> <details><summary>Ran a command</summary>
>
> - Ran `sed -n '170,290p' /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/run_audit.py; head -35 PROJECTS.md`
>
> </details>
>
> 架构审计也找到了具体原因：原八任务硬伪路径训练只监督细路由，粗路由没有收到梯度；两个种子的七个保存点中，粗路由参数均未变化。因此，目前应先验证“补上粗路由训练能否恢复在线收益”，还不能把主要失败归因于末层标签或早期表征。
>
> <details><summary>Explored a file, 2 searches, a list, ran 4 commands</summary>
>
> - Ran `find /data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/runs/full-20260903T042000Z -maxdepth 2 -type f | head -25; grep -n -E 'lr|learning_rate|updates|benchmark|stage2' /data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/run*.py | head -40; sed -n '1,110p' /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/run_audit.py`
>
> <details><summary>Explored a file, 2 searches, a list</summary>
>
> - Listed files in `benchmark__HIER_GMM_HARD_R8__seed17`
> - Searched for `lr|learning_rate|stage|epochs|updates|save` in `training.py`
> - Read `/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/training.py`
> - Searched for `HIER_GMM_HARD_R8|benchmark|route_weight|epochs|train` in `registry.py`
>
> </details>
>
> - Ran `python - <<'PY'
> import json,pathlib
> p=pathlib.Path('/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/runs/full-20260903T042000Z/conditions')
> for seed in [17,29]:
>  h=json.loads((p/f'benchmark__HIER_GMM_HARD_R8__seed{seed}/train_history.json').read_text());print(seed,len(h),h[-1],sorted(set(x['epoch'] for x in h)))
> PY`
>
> - Ran ``cat > /tmp/e14_p1_record.py <<'PY'
> from pathlib import Path
> import json,shutil,csv,hashlib
> import numpy as np
> w=Path('/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention')
> r=w/'runs/reserved-20260906-p1-v2/full'; a=r.parent/'analysis'
> d=Path('/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P1_coarse_path_intervention')
> x=json.loads((a/'results.json').read_text()); m=json.loads((r/'metadata.json').read_text()); audit=json.loads((r/'architecture_audit.json').read_text())
> for name,expected in m['code_sha256'].items(): assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==expected
> for seed in [17,29]:
>  z={k:dict(np.load(r/f'seed{seed}_{k}.npz')) for k in ['A','B','C','D','D_shift1','D_shift2']}
>  den=z['D_shift1']['eligible'].astype(int)+z['D_shift2']['eligible'].astype(int)
>  assert np.array_equal(den,z['D']['alternatives']) and np.isin(den,[1,2]).all()
>  avg=(z['D_shift1']['loss_sum']*z['D_shift1']['eligible']+z['D_shift2']['loss_sum']*z['D_shift2']['eligible'])/den
>  assert np.array_equal(avg,z['D']['loss_sum'])
>  for k,v in z.items(): assert np.isfinite(v['loss_sum']).all() and v['token_count'].sum()==30442
> for sub in ['tables','figures']: (d/sub).mkdir(exist_ok=True)
> for f in a.glob('*.csv'): shutil.copy2(f,d/'tables'/f.name)
> for f in a.glob('*.png'): shutil.copy2(f,d/'figures'/f.name)
> for src,name in [(a/'results.json','results.json'),(r/'metadata.json','execution_metadata.json'),(r/'architecture_audit.json','architecture_audit.json')]: shutil.copy2(src,d/'tables'/name)
> def csvwrite(name,rows):
>  with (d/'tables'/name).open('w') as f:
>   c=csv.DictWriter(f,fieldnames=list(rows[0]));c.writeheader();c.writerows(rows)
> csvwrite('architecture_weight_audit.csv',[dict(seed=s,parameter=k,**v) for s,o in audit['snapshots'].items() for k,v in o['parameters'].items()])
> csvwrite('architecture_gradient_audit.csv',[dict(parameter=k,original_gradient_norm=v,diagnostic_parent_loss_gradient_norm=audit['diagnostic_parent_loss_gradient_norms'][k]) for k,v in audit['original_gradient_norms'].items()])
> rows='\n'.join(f"| {o['seed']} | {o['condition']} | {o['nll']:.9f} |" for o in x['rows'])
> contrasts='\n'.join(f"| {o['seed']} | {o['left']} − {o['right']} | {o['delta']:.9f} | [{o['ci_low']:.9f}, {o['ci_high']:.9f}] |" for o in x['contrasts'])
> (d/'summary.md').write_text(f'''# E14-P1: Supplying the teacher parent recovers most of the deployment gap
>
> Execution: COMPLETE; eligible frozen evaluation. Registered verdict: `COARSE_CORRECTION_SUPPORTED`.
> Knowledge wording: `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`.
> [Protocol](../../../../../../../daily_research_reports/0906/docs/protocol.md) · [Detailed evidence](../../../../../../../daily_research_reports/0906/docs/detailed.md)
>
> Supplying the original pseudo-teacher parent while reselecting the predicted child inside that parent recovers **98.24% and 93.96%** of the online-to-full-pseudo-teacher loss gap in seeds 17 and 29. The primary parent-correction contrast is positive with positive 95% interval lower endpoints in both seeds. No parameter was trained or updated. This is an externally supplied path intervention, not a repaired deployable Router.
>
> ## Conditions and direct result
>
> NLL means summed answer-target negative log probability divided by answer-token count, in nats per answer token; lower is better. Each seed uses the same 512 examples and 30,442 answer tokens. “Teacher” means the original offline pseudo assignment, not ground-truth semantic labels or the historical gold Oracle model.
>
> - A: original predicted parent and predicted child; online baseline.
> - B: teacher parent and a newly selected predicted child constrained to that parent.
> - C: original teacher parent and teacher child; privileged reference.
> - D: teacher parent and each wrong same-parent child; average alternative losses within each example before token aggregation. Parent sizes are 3, 3, 2.
>
> | Seed | Condition | NLL (nats/token) |
> |---|---|---:|
> {rows}
>
> | Seed | Contrast | Difference (nats/token) | Paired-example 95% interval |
> |---|---|---:|---|
> {contrasts}
>
> A−B measures parent correction, B−C the residual child correction, and D−C the matched-child advantage. The recovery fraction is (A−B)/(A−C), not an order-independent causal attribution. Intervals use 2,000 paired-example resamples separately for each fixed checkpoint; auxiliary intervals are descriptive.
>
> ![Frozen path intervention](../../../../../../../daily_research_reports/backup/2026/09/0906/figures/path_intervention.png)
> How to read: the large A-to-B loss reduction appears in both seeds; the positive D-minus-C contrast shows a cost to selecting the wrong child even with the parent supplied. Fine correction remains positive, so B and C have not been established equivalent.
>
> ## Architecture finding
>
> The historical eight-task hard-pseudo branch runs only stage 2, where auxiliary supervision reaches the child Router only. Hard forced indices and unit expert coefficients eliminate the task-loss route to parent logits. A small backward check finds no parent gradient. All seven stored snapshots, updates 1 through 128, have exactly unchanged parent weights and biases in both seeds. Child weights change by maximum absolute values 0.032013 and 0.032875.
>
> ![Historical Router parameter change](../../../../../../../daily_research_reports/backup/2026/09/0906/figures/architecture_weight_audit.png)
> How to read: parent weight and bias changes are exactly zero; this figure describes historical parameter updates, not the performance of a newly trained Router.
>
> This is a concrete supervision defect that must be controlled before attributing the large handoff failure to final-layer teacher semantics or inaccessible early representations. It does not establish that online parent training will recover the privileged intervention benefit. The independently staged M2D2 branch is outside this defect's audited scope.
>
> ## Eligibility and boundary
>
> ACP job `pt-5xgwtcam` succeeded on one reserved H100. All three regression tests and the two-seed smoke passed. Full A/C per-example losses and paths exactly replay the historical arrays. Every path legality, sample identity, finiteness and frozen-parameter guard passed; optimizer updates: **0**. Earlier failed smoke runs are excluded.
>
> The teacher uses full-sequence final-layer means and therefore privileged later context. Results concern previously examined internal eight-task answer losses, not uncontaminated benchmark generalization. The deployed Router's block input and the earlier static audit's post-attention MLP input are different objects. No layer/context intervention, new labels, gold-Oracle comparison, or deployment training was run here.
>
> ## One next decision
>
> Choose whether step 2 should first train only the parent Router with experts and child Router frozen. AI recommendation: prioritize this minimal repair because parent correction removes most of the observed gap; retain the measured residual child gap as a later target. This training choice and its protocol remain unconfirmed; step 1 execution approval does not launch step 2.
> ''')
> old=(d/'detailed.md').read_text(); arch=old[old.index('## 4. Actual stage'):old.index('## 6. Evidence lineage')]
> (d/'detailed.md').write_text(f'''# Detailed: E14-P1 frozen coarse-path intervention
>
> Status: COMPLETE / ELIGIBLE. Registered verdict: `COARSE_CORRECTION_SUPPORTED`.
> Knowledge wording: `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`.
> [Protocol](../../../../../../../daily_research_reports/0906/docs/protocol.md) · [Summary](../../../../../../../daily_research_reports/0906/docs/summary.md).
>
> ## 1. Actual scope and training accounting
>
> This experiment has no training stages, optimizer, learning rate, accumulation, or new checkpoint. All base, output-head, expert and Router parameters were frozen; optimizer updates are zero. Evaluation batch size is 8. Each seed executes five complete 512-example passes: A, C, B, D-shift-1 and D-shift-2. The latter two enumerate wrong children, with eligibility masks for parent sizes (3,3,2); D is their per-example eligible average, not another forward pass. Each pass scores 30,442 answer tokens. No new task-only model, gold Oracle, shuffled-label null or matched deletion was evaluated. A is the baseline, C the privileged pseudo-teacher reference, B the parent correction and D the wrong-child control.
>
> Historical source training was **not staged** for this benchmark branch: only stage 2, 128 optimizer updates, microbatch 8 with accumulation 16. Both seed histories span epochs 0–3 and record 911,644 answer-target token exposures. Base and language head were frozen; shared, parent and leaf LoRA banks and Routers were nominal optimizer members, but the parent Router received no gradient. Objective: answer NLL plus child classification cross-entropy with unit weight. Nominal learning rates: LoRA 2e-4, Router 5e-4 with the historical schedule. Final update 128 is the selected checkpoint, without best-development selection; there is no earlier parent-training stage or stage handoff. Seven saved updates are 1,6,13,32,64,96,128. Current evaluation loads those final tensors unchanged. The separate M2D2 branch does have two stages and is not the treatment under audit.
>
> ## 2. Results and analysis
>
> The complete condition table, contrast definitions, intervals and eligible figures are in [Summary](../../../../../../../daily_research_reports/0906/docs/summary.md). Machine-readable sources: [condition table](../../../../../../../daily_research_reports/0906/docs/tables/condition_nll.csv), [contrasts](../../../../../../../daily_research_reports/0906/docs/tables/contrasts.csv), [task-stratified descriptive table](../../../../../../../daily_research_reports/0906/docs/tables/source_nll.csv), [analysis result](../../../../../../../daily_research_reports/0906/docs/tables/results.json).
>
> Primary contrast A−B is 0.039619370 [0.033635655,0.046319138] for seed 17 and 0.021731576 [0.017851930,0.026396028] for seed 29. Both lower bounds exceed zero under the frozen rule. Residual B−C is 0.000708633 and 0.001398138; wrong-child D−C is 0.018794753 and 0.019650431. No equivalence threshold is introduced. Ratios are 0.982428268 and 0.939552293, conditional on this intervention order.
>
> All condition comparisons pair sample IDs, sources and answer-token counts. Analysis uses float64 accumulation of stored per-example losses, including paired differences, avoiding float32 reduction noise. Historical replay compares original stored arrays exactly; float64 display aggregates differ from old float32 aggregates by less than 6e-8 nats/token. This does not change raw losses, evaluation, tolerance or verdict. Bootstrap: 2,000 paired-example draws, NumPy generator seed 20260906, percentile 95%; checkpoints are analyzed separately, not pooled as independent examples. Seed mean is descriptive. No population-of-training-seeds or multiple-testing-adjusted auxiliary claim.
>
> ## 3. Execution and immutable evidence
>
> Worker: `{w}`.
> Eligible full run: `{r}`.
> Analysis: `{a}`.
> Historical run: `/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/runs/full-20260903T042000Z`.
> Data: `/data/250010109/datasets/a15_e14_benchmark/processed.pt`.
> Base: `/data/250010109/model_cache/Qwen3-0.6B-Base-official`.
>
> ACP `pt-5xgwtcam`: SUCCEEDED; start 2026-09-06 09:24:08 UTC (17:24:08 Beijing). One reserved H100 80GB, one `n6ls.iu.i40.1` worker, original NGC 25.06 image. Smoke elapsed 17.825 seconds; full runner elapsed 42.315 seconds, excluding container startup and separate analysis. No automatic retries; 5,400-second process limit. Resource selection was explicitly authorized by the researcher.
>
> Command: `RUN_STAMP=reserved-20260906-p1-v2 timeout 5400 bash <worker>/run_remote.sh`.
> Analysis command: `python <worker>/analyze.py --run <eligible-full-run> --output <analysis-directory>`.
> Runtime: Python {m['python'].split()[0]}, PyTorch {m['torch']}, Transformers {m['transformers']}, NumPy {m['numpy']}; bf16 frozen base, historical attention implementation. Local analysis uses NumPy 1.24 with float64 accumulation.
>
> [Execution metadata](../../../../../../../daily_research_reports/0906/docs/tables/execution_metadata.json) owns exact source-code, data, pseudo-label and adapter SHA-256 digests and replay/freeze checks. All five evaluation source-code hashes were rechecked after completion. Base safetensors SHA-256: `cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba`; config: `504a6b58c4271583724e66584b6b7698aea18450209df6b2f7582df0e89cee59`, verified against historical identity before execution.
>
> Raw arrays, logs and checkpoints remain on the worker. Curated metadata, tables and figures only are copied here. No original training code/checkpoint was modified; no commit, push or external publication occurred.
>
> {arch}
> ## 6. Guards, failures and exclusions
>
> Eligible run: 3/3 regression tests passed, including full outer-model parent forwarding and reset, parent-constrained child reselection, and uneven child-count enumeration. Both-seed smoke and full A/C replay have zero per-example loss error and exact route/source/count identity. All intervention paths are legal; B/C/D use supplied parents; C/D use supplied children. Model parameters have requires-grad disabled and adapter tensors compare exactly before/after. Full matrix is finite; every D average and its alternative counts were independently recomputed from saved arrays.
>
> Excluded local runs: `smoke-v1` failed ONNX/protobuf import; pure-Python protobuf allowed subsequent import. `smoke-v2` batch 2 and `smoke-batch8` failed original A replay at absolute aggregate errors 0.003542423 and 0.007956505 under local PyTorch 2.3/Python 3.10. No local full matrix ran and tolerance remained 1e-4.
>
> Excluded first reserved job `pt-a4qkvyya`, run `reserved-20260906-p1-v1`: original-runtime A/C smoke replay passed exactly but B parent guard failed. The intervention wrapper's base forward cleared the supplied parent. A regression test reproduced it; forwarding the argument through the base call fixed it. That job ended FAILED before replacement. Fresh directory `reserved-20260906-p1-v2` contains the only eligible full run. No failed outputs enter scientific aggregation.
>
> ## 7. Architecture evidence and visualization audit
>
> [Architecture JSON](../../../../../../../daily_research_reports/0906/docs/tables/architecture_audit.json), [weight audit](../../../../../../../daily_research_reports/0906/docs/tables/architecture_weight_audit.csv), [gradient audit](../../../../../../../daily_research_reports/0906/docs/tables/architecture_gradient_audit.csv). The gradient diagnostic uses the actual adapter and routing loss with a small squared-output surrogate to inspect task-gradient reachability; it is not a language-model training experiment. The added-parent-loss diagnostic only proves a gradient route exists.
>
> | Figure | Question and computation | Aggregation and display | Allowed conclusion / limitation |
> |---|---|---|---|
> | `figures/path_intervention.png` | Does supplying the parent reduce answer loss? Stored per-example losses and token counts | Left: A/B/C/D token-weighted NLL by seed; right: paired differences with 95% intervals; nats/answer token | Frozen intervention benefit and wrong-child cost; no deployable training gain, equivalence, or semantic causal claim |
> | `figures/architecture_weight_audit.png` | Did historical Router parameters change? Exact snapshot tensors | Max absolute update-1-to-final tensor difference; seed-colored parent/leaf weights and biases | Parent parameters unchanged at stored snapshots; no initialization snapshot or repaired-model performance claim |
>
> Both rendered PNGs inspected: axes, legends, units and labels readable; values trace to tables; zero parent changes are represented on a zero-based axis. Fine differences are visible but their precise values and intervals must be read from the table. No curve smoothing or excluded-run data.
>
> ## 8. Boundary and next decision
>
> Teacher is the original pseudo label, not gold Oracle. Full-sequence teacher context is privileged. These are previously examined internal task losses, not uncontaminated generalization scores. The intervention replaces parent identity and consequently downstream computation; its recovery fraction is not a unique decomposition of independent causal effects. No current-layer labels or causal-prefix teacher were tested. The architecture failure prevents attributing the original large deployment gap solely to final-layer semantic mismatch or early readout failure.
>
> AI recommendation pending researcher judgment: step 2 first tests parent-only training with fixed experts and child Router, preserving labels and hook to isolate supervision repair. No step-2 training was started. Human result wording, Focus knowledge update and subsequent protocol are still pending; no delayed daily report is generated.
> ''')
> p=d/'protocol.md';s=p.read_text().replace('The earlier failed job has ended and is not billed concurrently by this runner.','The earlier job reported FAILED before replacement submission.')
> s+='\nCompletion receipt: replacement job `pt-5xgwtcam` reported SUCCEEDED. Both seeds completed all arms with exact historical A/C array replay and frozen-parameter guards. Full runner elapsed 42.315 seconds, optimizer updates zero. Analysis uses float64 reduction of stored per-example losses to avoid float32 summation noise; scientific definitions and guards are unchanged. Curated evidence is recorded in [Summary](../../../../../../../daily_research_reports/0906/docs/summary.md) and [Detailed](../../../../../../../daily_research_reports/0906/docs/detailed.md); interpretation awaits researcher confirmation.\n';p.write_text(s)
> f=Path('/data/250010109/Research_System/daily_research_reports/0906/focus_gmm_pseudolabel_handoff.md');s=f.read_text().replace('status: STEP1_RESERVED_H100_RUNNING','status: STEP1_COMPLETE_AWAITING_HUMAN_RESULT')
> start=s.index('执行状态：');end=s.index('## 证据入口')
> s=s[:start]+'''执行状态：第一步已完成。标准配额单张 H100 作业 `pt-5xgwtcam` 成功；三个回归测试、两种子小样本及完整原路径重放、路径合法和参数冻结检查全部通过。优化器更新次数为零。
>
> AI 核验结果（`AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`，不代填人工认识）：外部纠正粗路径恢复种子 17、29 的原交接差距 98.24% 和 93.96%；粗纠正损失收益分别为 0.039619370 和 0.021731576 nat/答案词元，两种子的配对 95% 区间下界均大于零。正式判定为支持粗路径纠正；细路由残余差距仍为 0.000708633 和 0.001398138，不能宣布两条路径等效。原八任务硬伪路径训练没有粗路由梯度，七个保存点粗路由参数均未变化。
>
> AI 建议：第二步先冻结专家和细路由，只训练粗路由，以验证补足监督能否带来在线收益。这仍是待人工选择的下一步；本次外部供给路径没有修好可部署 Router，也没有验证末层标签优劣。人工结果、不能声称的内容和下一决策尚待研究者填写或确认。
>
> '''+s[end:]
> s=s.replace('## 唯一下一决策','- [本步结果](../../../../experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P1_coarse_path_intervention/summary.md)\n- [完整证据](../../../../experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P1_coarse_path_intervention/detailed.md)\n\n## 唯一下一决策');f.write_text(s)
> p=Path('/data/250010109/Research_System/PROJECTS.md');s=p.read_text();s=s.replace('user approved E14-P1 frozen coarse-path intervention and architecture audit; no retraining in step 1;', 'E14-P1 reserved H100 job `pt-5xgwtcam` SUCCEEDED; verdict `COARSE_CORRECTION_SUPPORTED`; parent intervention recovers 98.24%/93.96% of handoff gap; zero training updates; human result wording and step-2 decision pending;')
> # Retain the primary workstream as the first registry row, as the existing prose requires.
> lines=s.splitlines();i=next(i for i,l in enumerate(lines) if l.startswith('| `A15.gmm_pseudolabel_oracle_gap`'));j=next(i for i,l in enumerate(lines) if l.startswith('| `A15.m2d2_semantic_representation_geometric_form`'))
> if i<j: line=lines.pop(i);j=next(i for i,l in enumerate(lines) if l.startswith('| `A15.m2d2_semantic_representation_geometric_form`'));lines.insert(j+1,line)
> p.write_text('\n'.join(lines)+'\n')
> print('Curated results written; code hashes, D aggregation and finiteness verified.')
> PY
> python /tmp/e14_p1_record.py``
>
> - Ran `python - <<'PY'
> from pathlib import Path
> import re,json
> root=Path('/data/250010109/Research_System');d=root/'Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P1_coarse_path_intervention'
> files=list(d.glob('*.md'))+[root/'daily_research_reports/0906/focus_gmm_pseudolabel_handoff.md']
> bad=[]
> for p in files:
>  s=p.read_text()
>  for t in re.findall(r'\]\(([^)]+)\)',s):
>   if not t.startswith(('http','#')) and not (p.parent/t.split('#')[0]).exists():bad.append((str(p),t))
>  for t in ['FULL_EVALUATION_NOT_RUN','FULL_EVALUATION_NOT_RUN','STEP1_RESERVED_H100_RUNNING','cloud quota selection pending']: assert t not in s,(p,t)
> print('Broken links:',bad);assert not bad
> x=json.loads((d/'tables/results.json').read_text())
> for seed in [17,29]:
>  n={r['condition']:r['nll'] for r in x['rows'] if r['seed']==seed}
>  for c in x['contrasts']:
>   if c['seed']==seed:assert abs((n[c['left']]-n[c['right']])-c['delta'])<1e-12
> print('Markdown references and independent contrast arithmetic: PASS')
> PY
> git diff --check`
>
> </details>
</details>

**第一步已完成，标准配额单张 H100 作业成功。粗路径干预和架构审计均已通过检查。**以下认识标记为待你确认。

### 1. 目的

固定模型参数，确定离线伪标签路径转为在线路由时，损失主要发生在粗分发还是细分发。

### 2. 假设

如果粗分发是主要断点，外部给定原伪标签的粗路径后，损失应明显下降。

### 3. 分析方法

- 两个训练种子，各评估相同的 512 条样本；**本次没有训练 Router 或专家，参数更新次数为零**。
- 比较四种路径：原在线路径、仅给定粗路径、给定完整伪标签路径、给定粗路径但换错细专家。
- 核查历史训练梯度、参数变化和实际读取位置；原在线与完整伪标签路径均精确复现历史结果。

### 4. 结论

1. **给定粗路径恢复了绝大部分交接损失：两个种子分别恢复 98.24% 和 93.96%。**

   答案预测损失越低越好；两个种子平均如下：

   | 路径 | 损失 |
   |---|---:|
   | 原在线路径 | 0.836757 |
   | 给定粗路径，重新预测细路径 | 0.806082 |
   | 完整原伪标签路径 | 0.805028 |
   | 给定粗路径，但换错细专家 | 0.824251 |

   两个种子的粗纠正收益，其 95% 区间下界均大于零。细路径仍有残余差距，不能宣布完全恢复。

   ![路径干预结果](../../../../../../../daily_research_reports/backup/2026/09/0906/figures/path_intervention.png)

   读图：左图从 A 到 B 的下降表示粗路径纠正收益；这里的教师是原伪标签，并非真实语义标签。

2. **原八任务硬伪路径训练存在粗路由监督缺失，当前不能先把失败归因于末层标签或早期表征。**

   该分支只执行细阶段训练，粗路由没有收到梯度；两个种子的七个保存点中，粗路由权重和偏置均未变化。这一发现仅针对本次八任务分支。

   ![历史路由参数审计](../../../../../../../daily_research_reports/backup/2026/09/0906/figures/architecture_weight_audit.png)

   读图：粗路由两项变化均为零，细路由参数则发生变化。

   **下一步建议：进入第二步，先固定专家和细路由，只训练粗路由，验证补足监督能否恢复真正的在线收益。**本次修复的是干预入口，尚未训练出修复后的在线 Router；第三步标签审计、第四步联合训练仍未启动。

完整记录：[结果摘要](../../../../experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P1_coarse_path_intervention/summary.md) · [审计与执行证据](../../../../experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P1_coarse_path_intervention/detailed.md)。

> 现在我需要你给我一个完整的对话解析，因为我不知道你使用的 checkpoint，它之前运行的时候，它的这个训练情况是怎么样子。我想请问一下，之前我们用的 checkpoint，它是在什么数据集上面训练，并且以什么方式训练？它是两阶段训练吗？并且第一阶段它的出力度专家的路由和吸力度专家的路由是否都训练了，还是说直接给定的？然后我们改变了什么对照变量，从而进行了该实验？这个点我需要明确搞清楚，才能进行下一步分析

<details><summary>4 previous messages</summary>

> 我会把本次使用的检查点追溯到原训练配置和训练记录，逐项说明：数据是什么、实际执行了哪些阶段、粗细路由如何训练，以及这次干预究竟只改变了什么。我会使用研究文档解释技能，按训练到评估的顺序讲清楚。
>
> <details><summary>Explored 3 files, a list, ran 3 commands</summary>
>
> <details><summary>Explored 2 files, a list</summary>
>
> - Read `./.agents/skills/research-document-explainer/SKILL.md`
> - Read `/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/registry.py`
> - Listed files in `20260903_a15_13_e14_gmm_pseudolabel_oracle_gap`
>
> </details>
>
> - Ran `cat .agents/skills/research-document-explainer/references/{explanation_contract,terminology_contract,experiment_reasoning}.md; head -65 docs/research_terminology.md; cat /data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/prepare_data.py`
>
> <details><summary>Explored 2 files</summary>
>
> - Read `/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/training.py`
> - Read `/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/prepare_pseudo_labels.py`
>
> </details>
>
> - Ran `python - <<'PY'
> import json,torch
> from pathlib import Path
> p=Path('/data/250010109/datasets/a15_e14_benchmark/processed.pt');d=torch.load(p,map_location='cpu',weights_only=False)
> print('manifest',json.dumps({k:v for k,v in d['manifest'].items() if k!='sources'},ensure_ascii=False))
> print('unique sources', {k:v.get('unique_usable_rows') for k,v in d['manifest']['sources'].items()})
> for s,t in d['splits'].items():print(s,len(t['source']),len(set(t['record_id'])),int(t['answer_token_count'].sum()))
> for s in ['development','evaluation']:
>  print('train overlap',s,len(set(d['splits']['train']['record_id']) & set(d['splits'][s]['record_id'])))
> p=Path('/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/runs/full-20260903T042000Z/conditions')
> for seed in [17,29]:
>  f=p/f'benchmark__HIER_GMM_HARD_R8__seed{seed}/final.pt';c=torch.load(f,map_location='cpu',weights_only=False);print(str(f));print(c['metadata'])
> PY`
>
> - Ran `sed -n '70,240p' /data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/models.py; head -100 /data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/gmm_labels.py`
>
> </details>
>
> 已核实：本次用的是“八任务混合数据上的硬伪标签专家”检查点，实际只训练了一个阶段，并未先完成粗阶段再进入细阶段。需要特别区分：训练时粗、细专家的执行路径都由伪标签给定，但只有细路由另外接受了分类监督；“给定路径”和“训练路由器”是两件事。
>
> <details><summary>Ran a command</summary>
>
> - Ran `sed -n '110,190p' /data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/gmm_labels.py; sed -n '265,282p' /data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/training.py; python - <<'PY'
> import torch
> p='/data/250010109/datasets/a15_e14_benchmark/processed.pt';d=torch.load(p,map_location='cpu',weights_only=False);tr=set(d['splits']['train']['record_id']);e=d['splits']['evaluation']
> for i,name in enumerate(d['sources']):
>  ids=[rid for k,rid in enumerate(e['record_id']) if e['source'][k]==i];print(name,sum(r in tr for r in ids))
> PY`
>
> </details>
</details>

**本次使用的检查点，并不是“先训练粗专家、再训练细专家”的两阶段模型。它是在八任务混合数据上，直接同时训练粗细专家的单阶段模型：训练时粗细执行路径都由离线伪标签给定，细路由另外接受分类监督，粗路由却没有收到训练梯度。**

我之前没有先把这个检查点的训练来历解释清楚，容易让你将它和另一条真正分阶段的实验混在一起。下面按“数据 → 标签 → 模型训练 → 本次干预”完整说明。你说的“出力度、吸力度”，我按“粗粒度、细粒度”理解。

**一、到底用了哪个检查点？**

检查点就是某次训练结束后保存的模型参数。本次用了**同一训练条件下，随机种子为 17 和 29 的两个最终检查点**，都取第 128 次参数更新后的版本，没有根据此次干预结果重新挑选。

原始条件名是 `benchmark__HIER_GMM_HARD_R8`，含义是：

- `benchmark`：八任务混合数据分支。
- `HIER`：共享、粗粒度、细粒度专家组成的层级结构。
- `GMM`：用高斯混合聚类生成伪标签。
- `HARD`：训练时直接指定专家编号。
- `R8`：每个低秩专家的秩为 8。

它是**“硬伪标签路径训练的专家模型”**。它既不是人工真值路径训练的模型，也不是另一组由在线路由实际选择训练路径的模型。

两个参数文件分别为：[种子 17 检查点](/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/runs/full-20260903T042000Z/conditions/benchmark__HIER_GMM_HARD_R8__seed17/final.pt)、[种子 29 检查点](/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/runs/full-20260903T042000Z/conditions/benchmark__HIER_GMM_HARD_R8__seed29/final.pt)。

**二、它在什么数据上训练，标签又从哪里来？**

底座是已经预训练好的 **Qwen3-0.6B-Base**。我们没有重新预训练底座，而是在它上面训练新增的专家模块和路由模块。

使用的数据是八个任务来源混合：

| 数据来源 | 内容 |
|---|---|
| MMLU、MMLU-Pro | 多学科选择题 |
| BBH | 多类推理题 |
| GSM8K、MATH | 数学问题及答案或解答 |
| GPQA | 高难度科学选择题 |
| HumanEval、MBPP | 编程问题及参考代码 |

每个来源抽取 512 条训练记录、64 条开发记录、64 条评估记录。因此：

| 集合 | 记录数 | 用途 |
|---|---:|---|
| 训练集 | 4,096 | 训练专家和路由 |
| 开发集 | 512 | 观察训练过程 |
| 评估集 | 512 | 本次固定路径干预 |

输入是“问题＋参考答案”，最大长度 512 个词元。**任务损失只计算答案部分的下一词元预测，不计算问题部分。**选择题主要预测答案选项，数学题和编程题则预测保存的解答或代码。

这里有一个已核实的数据边界：训练记录中存在重复。此次评估的 **128 条记录与训练集具有相同原始记录编号**，分别是 GPQA 的 64 条和 HumanEval 的 64 条。因此这组结果只能作为内部机制诊断，不能声称无污染的公开基准泛化收益。

离线伪标签的生成过程是：

1. 用**冻结的原始底座**读取每条“问题＋答案”。
2. 对最后一层所有有效词元的表示求平均，得到每条样本的一个向量。
3. 将向量投影到 64 维，再做层级聚类：先分 3 个粗组，再在粗组内分出合计 8 个细组，实际数量为 **3、3、2**。
4. 聚类模型只在训练表示上拟合，然后固定它，给开发集和评估集分配标签。

所以，**每条样本有一个粗标签和一个细标签；标签来自末层整段表示，包含答案信息，并不是每个位置独立产生的因果标签。**这些编号也不直接等于八个任务来源。

来源：[数据构造](/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/prepare_data.py)、[伪标签生成](/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/prepare_pseudo_labels.py)。

**三、原训练究竟怎么运行？粗细专家和粗细路由分别发生了什么？**

首先分清四个对象：

- **粗专家**：实际参与计算的粗粒度参数模块。
- **细专家**：实际参与计算的细粒度参数模块。
- **粗路由器**：预测应该选择哪个粗专家。
- **细路由器**：预测应该选择哪个细专家。

**专家参数被训练，不代表选择它的路由器也被训练。**

这个模型在底座的同一个位置加入了：1 个共享专家、3 个粗专家、8 个细专家。每次计算使用：

> 原模型输出＋共享专家输出＋一个粗专家输出＋一个细专家输出。

粗细专家都加在零起始编号为 14 的块中，即按“第一层”开始数时的第 15 个块。这里的“层级”是专家分组关系，**不意味着粗专家和细专家分别插在两个不同网络深度，也不意味着训练天然分成两阶段**。

原训练的实际情况如下：

| 对象 | 训练时如何参与前向计算 | 是否获得训练信号 |
|---|---|---|
| 原始底座与输出头 | 正常计算 | 冻结 |
| 共享专家 | 每条样本都使用 | 通过答案预测损失训练 |
| 粗专家 | 根据离线粗标签选中 | 通过答案预测损失训练 |
| 细专家 | 根据离线细标签选中 | 通过答案预测损失训练 |
| 粗路由器 | 计算分数，但分数不决定执行路径 | **没有梯度，未学到粗分发** |
| 细路由器 | 计算分数，但分数不决定执行路径 | **通过细标签分类损失训练** |

例如，某条样本的伪标签指定“粗组 2、该组的细专家 1”。训练时就使用这两个专家，**即使路由器预测的是另一个组，也不会改变此次专家计算路径**。

与此同时，程序仍然可以单独要求细路由器预测正确的细标签。其分类损失会更新细路由器。这就是为什么：

> **“实际路径直接给定”和“路由器接受监督训练”可以同时成立。**

本检查点的训练目标，按含义写就是：

\[
\text{总损失}
=
\text{答案预测损失}
+
\text{细标签分类损失}.
\]

其中细标签分类是在 **8 个细类之间**计算的；没有加入粗标签分类损失。专家输出系数又固定为 1，因此任务损失也不能通过概率系数传回粗路由器。

实际训练账目：

- **只有一个训练阶段**，代码将它标为“阶段 2”。
- 粗细专家从这个阶段开始一起训练，没有前置粗阶段。
- 每小批 8 条，累计 16 个小批更新一次参数，有效批量 128 条。
- 共 128 次更新，完整遍历这份 4,096 条训练记录 **4 次**。
- 每个种子累计预测训练答案词元 911,644 个。
- 专家初始学习率为 0.0002，路由器为 0.0005。
- 使用第 128 次更新后的最终参数。

因此，你问“第一阶段粗细路由是否都训练了”，对**本次检查点**的直接回答是：**它没有第一阶段。唯一阶段中，粗细执行路径都直接给定；细路由接受监督，粗路由没有接受有效训练。**

另一条多领域语料实验确实配置了粗、细两个训练阶段，但本次没有使用那条实验的检查点。原始分支区别可以在[条件登记](/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/registry.py)和[训练实现](/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/training.py)中核对。

**四、本次实验改变的对照变量是什么？**

这次没有继续训练。我们对上述两个检查点分别做评估，**只改变“由谁指定执行路径”**。

以下字母只是本次四个评估条件的简称：

| 条件 | 粗专家由谁选 | 细专家由谁选 | 回答的问题 |
|---|---|---|---|
| A：原在线路径 | 原粗路由器 | 原细路由器在预测粗组内选择 | 原部署损失是多少？ |
| B：只供给粗路径 | 原离线粗标签 | 原细路由器在给定粗组内重新选择 | 绕过粗分发错误能恢复多少？ |
| C：完整伪标签路径 | 原离线粗标签 | 原离线细标签 | 完全恢复原训练责任分配时，损失是多少？ |
| D：错细专家对照 | 原离线粗标签 | 该粗组内其他细专家 | 正确细专家是否真的比同组错误专家有用？ |

**B 的关键不是只把粗专家换掉、保留原细专家，而是在给定粗组内重新选择细专家。**否则可能出现父子不匹配，也无法回答“如果粗组正确，原细路由还能否工作”。

四组保持相同的对象包括：

- 底座、共享专家、粗细专家、粗细路由器的全部参数。
- 原伪标签、评估样本、答案计分位置。
- 专家系数，始终为 1。
- 路由读取位置和专家插入位置。

我们没有换教师层、没有改成当层标签、没有改用前缀标签，也没有改变路由器的读取位置。

工程上修复的“路径入口”，只是保证程序确实执行指定的粗路径，并在其中重新选择细专家。**它没有修复已经保存的粗路由器参数。**

**五、因此，这次结果应该怎样理解？**

已核验证据是：给定原伪标签粗路径后，两个检查点恢复了各自原交接差距的 **98.24% 和 93.96%**。这说明在这两个固定专家库中，供给粗路径可以恢复大部分损失。

但比较的两端是：

> 原在线路径 ↔ 原伪标签完整路径。

**不是：原在线路径 ↔ 人工真值路径训练的另一套专家模型。**

因此，这个百分比不能解释为“恢复了 98% 的人工真值模型收益”，也不能解释为“训练后的粗路由已经能达到这个效果”。

对你原先两个假设的认知纠正是：

- “末层标签可能不适合当层路由”仍是待验证假设；本次没有比较不同层的标签。
- “早期表征导致路由错训”目前需要先拆开：**这两个检查点的粗路由首先是没有训练到，而不是已经证实训练了仍学不好。**
- 细路由确实接受了训练；给定粗组后，它与完整伪标签路径仍有小幅差距，所以后续也不能直接宣布细路由完全正常。

下一步最明确的验证节点是：**保持这些专家、细路由、原标签和读取位置固定，只补上粗路由训练，再观察完全在线执行时能恢复多少收益。**这样才能开始区分“缺少监督”和“现有输入根本学不好这个标签”。

> 我已经理解我们的实验了。我认为现在确实应该确定我们的验证节点，然后我确定能够给你reserved资源进行验证，现在请你构建下一步验证计划，同时重新锚定我们现在所在实验计划的位置。

<details><summary>4 previous messages</summary>

> 下一步应锚定为“补足粗路由监督，能否恢复在线分发收益”。我会把它对应到四步规划中的第二步，固定专家、细路由、原伪标签和读取位置，形成可审阅的验证协议，并纳入你已授权的标准配额资源。
>
> <details><summary>Ran 2 commands</summary>
>
> - Ran `cat .agents/skills/experiment-card-writer/SKILL.md; cat .agents/skills/research-progress-core/SKILL.md; cat daily_research_reports/0906/focus_gmm_pseudolabel_handoff.md; head -35 PROJECTS.md`
>
> - Ran `cat .agents/skills/experiment-card-writer/references/blockwise_protocol_audit.md .agents/skills/experiment-card-writer/references/protocol_self_containment_and_freeze.md; cat Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_05_gmm_pseudolabel_oracle_gap_anchor.md; head -45 Projects/graphs/expert_specialization.graph.yaml`
>
> <details><summary>Explored 2 files</summary>
>
> - Read `/root/.codex/plugins/cache/openai-curated-remote/superpowers/6.3.0/skills/brainstorming/SKILL.md`
> - Read `./.agents/skills/research-progress-core/SKILL.md`
>
> </details>
>
> </details>
>
> 我会加入一个必要对照：同样只训练粗路由，但把训练样本的粗标签打乱、保持各类数量不变。这样能区分“正确的样本—标签对应关系有效”和“仅仅让未训练的路由学会类别比例就有收益”。评估还会单列与训练记录不重叠的 384 条样本，防止原数据重复影响判断。
>
> <details><summary>Ran 2 commands</summary>
>
> - Ran ``cat > /tmp/write_p2_plan.py <<'PY'
> from pathlib import Path
> root=Path('/data/250010109/Research_System')
> d=root/'Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P2_parent_router_supervision_repair'
> d.mkdir(parents=True,exist_ok=True)
> anchor='../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_05_gmm_pseudolabel_oracle_gap_anchor.md'
> (d/'protocol.md').write_text('''# Protocol: E14-P2 parent-only supervision repair
>
> ## 0. Approval Snapshot
>
> Document status: `DRAFT_NOT_EXECUTABLE`. Scientific choices below are `AI_PROPOSAL` unless explicitly attributed to inspected sources. No implementation or training has begun.
>
> Resource choice: researcher has authorized RESERVED resources for the next validation. Do not ask again for quota selection. Proposed ceiling: one H100, sequential conditions, maximum 90 minutes, no automatic retries. This request asks for a plan; final new experimental details remain for design review.
>
> Owning Focus: [0906 handoff](../../../../focus/focus_gmm_pseudolabel_handoff.md), same problem and task owner as P1. This is step 2 of the existing four-step sequence, not a new workstream. Role: root-cause repair test. [Primary Anchor](../../../../../../../daily_research_reports/0906/docs/ANCHOR) tests whether offline assignments can be handed to a causal block-14 Router while preserving task loss. Local clause: after P1 identified missing parent supervision, does training that parent predictor alone produce useful online dispatch? This does not replace the historical gold-Oracle verdict or test new labels.
>
> Treatment: original parent classifier trained to predict original pseudo parents. Controls: original untrained parent; identically trained parent with example-permuted labels; supplied teacher parent with original predicted child; supplied full pseudo path. Experts, child Router, teacher, input hook, unit coefficients and evaluation examples remain fixed.
>
> Primary metric: answer NLL reduction from original online routing, in nats/answer token. Qualification requires superiority to the shuffled-supervision control and improvement on record-disjoint evaluation. Pass requires positive lower paired-bootstrap endpoints for all these comparisons in both seeds. Fail means at least one required comparison has nonpositive upper endpoints in both seeds. Other eligible patterns are Insufficient. Report recovery continuously, without a post-hoc equivalence threshold.
>
> Cannot claim: universal deployability, unpolluted public benchmark performance, final-layer label optimality, a causal-prefix teacher, or a newly successful two-stage expert-training method. No new expert training, teacher fitting or layer selection.
>
> A–G: PROPOSED; internal consistency checked, human design confirmation pending. Existing P1 design remains frozen. New Focus experiment account is awaiting confirmation.
>
> ## 1. Terminology / Definitions
>
> Parent means one of three coarse expert groups. Child means one of eight fine experts with parent sizes (3,3,2). Teacher means the original frozen pseudo-label assignment, not human semantic truth. A Router is the classifier that chooses an expert. NLL is summed negative log probability of reference answer tokens divided by their count. Online means routing decisions use causal model states without supplying teacher labels during evaluated inference; reference previous answer tokens remain available under ordinary teacher-forced likelihood evaluation. It is not a free-generation score.
>
> ## 2. Anchor Alignment
>
> The Anchor's handoff clause and task-loss metric are retained. P1 fixed-path evaluation found parent correction recoveries 98.24%/93.96%, and no historical parent gradient in the eight-task hard-pseudo branch. Those observations motivate a repair, but do not establish learnability. Parent-only learning tests the missing supervision path while keeping the proposed teacher context and input representation unchanged. [P1 evidence](../../../../../../../daily_research_reports/0906/A15_13_E14_P1_coarse_path_intervention/summary.md).
>
> ## 3. Tested Hypothesis
>
> Adding original pseudo-parent classification supervision to the existing parent Router lowers fully online answer NLL in both checkpoints. The sample-specific teacher relation must outperform matched training with shuffled labels; class-frequency adjustment alone is insufficient to establish the proposed mechanism.
>
> ## 4. Rival Explanations
>
> 1. Category-prior correction rather than meaningful sample-label association: match label frequencies via fixed whole-example permutation.
> 2. Causal input cannot predict a full-sequence teacher, or the linear readout/finite optimization budget is inadequate: report parent classification losses and accuracy on train/development/evaluation, without inferring intrinsic impossibility from a negative result.
> 3. Improvement depends on repeated training items: predeclare the record-disjoint evaluation subset. It excludes two sources, so report its changed composition and do not generalize it to all eight tasks.
>
> ## 5. Data Construction And Provenance
>
> Reuse `/data/250010109/datasets/a15_e14_benchmark/processed.pt` with SHA-256 `e6320e7aba92c8d9caa36ce43bda5d695843070a54955e63776893334d58a6b6`.
> Eight sources: MMLU, MMLU-Pro, BBH, GSM8K, MATH, GPQA, HumanEval, MBPP. Existing splits: train 4096, development 512, evaluation 512; max length 512. Training contains 3434 unique record IDs. Evaluation contains 512 unique IDs and 30442 answer tokens. 128 evaluation IDs occur in training: 64 GPQA and 64 HumanEval. Record-disjoint evaluation consists of the remaining 384 examples; derive its token denominator from the immutable masks and record it before training. Retain full historical data for paired comparability; no repartition or new task download.
>
> Pseudo assignments: original E14 run `full-20260903T042000Z/pseudo_labels/benchmark/assignments.pt`, digest `64baa7bc0d737f26927a509727716481a5a8862f953d7d60db1c5bc435f705fa`. They were fitted to train-only projections/clusters of frozen final-layer whole-sequence means, including reference answers. No refit in P2. Model training may use train states/labels only; development is monitoring only; evaluation cannot choose hyperparameters or checkpoints. Historical evaluation is already seen and is not called untouched confirmation.
>
> ## 6. Learning Task And Permitted Supervision
>
> At each position predicting an answer token, read the original causal block-14 input vector and predict the example's pseudo parent. Broadcast the per-example parent to those prediction positions only. Exclude padding and positions whose next-token target is masked. Input is the 1024-dimensional causal hidden state; no source ID, future-token aggregate, answer label, teacher logits or child assignment is appended as a feature.
>
> Train supervision is original parent labels in treatment and a fixed example permutation of those labels in the control. Use NumPy generator seed 20260906 for one permutation of the 4096 train-example indices, preserving counts; broadcast after permutation. Reuse it across checkpoint seeds. Do not permute individual tokens or development/evaluation ground targets. Log permutation indices, digest and fraction unchanged. No claim that every permuted label differs.
>
> ## 7. Model / Architecture And Frozen Variants
>
> Base: frozen Qwen3-0.6B-Base. Start from original `benchmark__HIER_GMM_HARD_R8__seed17/final.pt` and seed29 counterpart in the E14 source run. Digests: `a783d46fcc77233ed94afdaaf898cb9f31033f76a568dcb66de3a93f983862c2` and `6e933452334524a22147e6d065e4e27f89a5badf6a64aa4fcfee94802cc70cac`.
>
> Only the existing 1024-to-3 parent linear classifier (3075 parameters including bias) changes. Initialize from that checkpoint's parent, with a fresh optimizer. Shared, parent and child expert banks, child Router, base and language head are frozen. Preserve block-14 pre-attention input capture and rank-8 expert banks in its MLP down projection. All inference expert coefficients remain one. No capacity increase, extra context, new input hook, or probability weighting.
>
> Extract/cache bf16 causal states at answer-prediction positions using each original checkpoint in eval mode; block input precedes the adapter and is not a function of the parent output at that block. Verify cached states/logits against direct forwards. Classifier weights originate in bf16 and are cast to float32 for optimization; cast trained weights to bf16 for deployment. Both treatment and shuffled control use identical casts; zero-step deployed weights must reproduce the original checkpoint exactly.
>
> ## 8. Training Objective And Optimization
>
> Exactly one parent-only training stage, not rerunning expert stages. Objective: mean cross entropy over valid answer-prediction positions in each original eight-example microbatch, divided by accumulation 16; no task-loss term, no child loss, no balance loss. Gradients reach only parent weight and bias. At batch boundaries reproduce the old sample-balanced ordering, `balanced_order(source, seed, epoch)`.
>
> 128 optimizer updates; 4 full passes through 4096 training records; microbatch 8, accumulation 16. AdamW, learning rate 5e-4, weight decay 0.01, betas (0.9,0.999), epsilon 1e-8; warmup 5 updates followed by cosine decay to zero as the historical schedule; clip parent gradient norm at 1.0. Effective example batch 128. Train token exposures must equal 911644. Identical setup for shuffled control. No hyperparameter sweep.
>
> Save update 0, 32, 64, 96, 128 parent states and train/development classification metrics. Select final update 128 regardless of development score. Development observations cannot cause extra epochs, stopping for performance, or selection. Degenerate labels, nonfinite values, unexpected counts or frozen-parameter mutation stop execution as an engineering failure. Optimization adequacy remains a boundary of a negative result.
>
> ## 9. Conditions, Seeds, And Checkpoints
>
> | Condition | Training | Evaluated selection | Protected comparison |
> |---|---|---|---|
> | O: original | None | Original predicted parent/child | Baseline |
> | R: repaired | Parent only; true original pseudo labels | Trained parent, original child reselected within predicted parent | Missing-supervision repair |
> | S: shuffled | Parent only; permuted pseudo labels | Trained parent, original child reselected within predicted parent | Frequency/optimization rival |
> | B: teacher parent | None | Supplied parent, original child reselected there | P1 correction reference |
> | C: full teacher | None | Supplied parent and child | Residual fine-path reference |
>
> Two source seeds, 17/29; R/S both start afresh from the corresponding same original checkpoint. Total: four parent training runs, 512 optimizer updates across runs. One deployment evaluation per condition and source seed on the complete 512 examples. B and C are privileged references, not new trained models or mathematical lower bounds. P1 D wrong-child result remains background; no repeat necessary to adjudicate P2. Check that supplied-parent B and full-teacher C are invariant to parent replacement.
>
> ## 10. Primary Metric And Frozen Analysis Plan
>
> For condition k, $L_k=\\sum_i s_{ki}/\\sum_i n_i$ where s is summed answer negative log probability and n the answer-token count. Primary repair effect is $L_O-L_R$. Qualification effect is $L_S-L_R$. Compute both on full evaluation and record-disjoint evaluation, separately per seed. Recovery relative to supplied-parent reference is $(L_O-L_R)/(L_O-L_B)$; report undefined for zero denominator and do not clip. Also report R−B and R−C; a positive recovery is not equivalence.
>
> Use float64 reductions and 2000 paired-example percentile 95% bootstrap intervals with NumPy seed 20260906. Identical resampled indices across all conditions within each population, independently resample the full and disjoint populations. Unit of independence is evaluation record, not token. No pooled seed-population interval; report seeds individually and a descriptive unweighted mean. All required positive contrasts form a conjunction, not a menu for picking a favorable result. Auxiliary accuracy and residual intervals are descriptive. No post-hoc exclusions, outlier removal or threshold changes. Any missing required output yields Incomplete, not a negative scientific verdict.
>
> ## 11. Secondary Metrics And Guards
>
> Report true-parent agreement at answer-prediction positions, parent CE, per-parent predicted loads, per-source answer losses, and wrong-parent versus correct-parent strata. Agreement is not expert utility or end-task gain; load is not semantic evidence. Full and disjoint NLL protect the decision. No free-generation score required.
>
> Verify original data/checkpoint/assignment hashes, record-ID intersections, answer masks and source counts. Eval routes must not consume teacher labels in O/R/S. Prefix invariance check: changing suffix tokens cannot alter an earlier cached state or Router logits within the fixed numerical tolerance. Freeze/nonfinite/path-validity guards and source-code/config hashes are mandatory.
>
> ## 12. Known Good / Known Bad / Known Confusing Cases
>
> Known good: one forced parent selects only its allowed children; real CE backward produces finite nonzero parent gradients while all other learned tensors remain frozen. Known bad: intentional parent-child mismatch or label leakage is caught. Known confusing: parent accuracy rises but task loss does not; this is not a successful repair. An aggregate improvement that fails shuffled or disjoint qualification cannot be promoted.
>
> ## 13. Scientific Procedure And Stage Contracts
>
> | Phase | Input / operation | Output / handoff | Gate and failure |
> |---|---|---|---|
> | Identity and cache | Original data/checkpoints; extract causal states and train-only targets | Immutable cache, IDs, masks, hashes; no updates | Reject source mismatch, suffix dependence or mask errors |
> | Small smoke | Fresh disposable copies; 8 examples and 2 parent updates per label condition | Gradient/freeze checks, direct/cache comparisons, O/B/C replay | Replay paths exact and absolute aggregate loss error <=1e-4; no-op weights exact; never carry smoke weights to full training |
> | Parent-only stage | Fresh original parent; real/shuffled labels; fixed 128-update schedule | Four final parent checkpoints, curves, full parameter accounting | No parameters outside parent change; finite final output and exact budget |
> | Full model evaluation | Inject each final parent; original frozen experts and child Router | O/R/S/B/C paired arrays and task metrics | Predicted-route modes cannot access teacher; B/C remain invariant |
> | Analysis | Fixed arrays, full/disjoint masks, registered bootstrap | Summary, Detailed, tables and inspected figures | Use the one verdict rule; no post-result tuning |
>
> Cache/direct Router logits should match exactly when identical bf16 operations are used; for a float32 diagnostic cast use maximum absolute logit tolerance 1e-5 against the same float32 direct calculation. Causal suffix check uses max hidden difference 1e-5 after conversion to float32, in the same runtime and batch shape. A failure stops promotion and is investigated without relaxing thresholds using task results.
>
> ## 14. Algorithm, Output, And Provenance Contract
>
> Proposed worker: `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair`. Worker holds cache, code, raw arrays, gradients, logs, parent checkpoints and job receipts. Use original PyTorch 2.8/Python 3.12 NGC 25.06 image on one reserved H100, historical bf16 backbone/evaluator and batch 8. Do not modify E14 or P1 worker sources. Verify source digests and snapshot dependencies at execution, since other tasks may edit shared files.
>
> Resource ceiling: one `n6ls.iu.i40.1` H100 worker, sequential runs, 5400-second timeout, zero automatic retries; stop after the registered conditions. Runtime is an upper bound, not an ETA. No task submission in this planning turn. Once the design is confirmed, existing reserved-resource consent need not be requested again.
>
> Expected outputs: run metadata; source/data/pseudo/code/protocol hashes; ID overlap counts and mask; immutable cache map; shuffled assignment permutation; per-update train/development metrics; four final parent checkpoints; per-example loss sums, token counts, source/record IDs and routes for ten evaluations; frozen checks; bootstrap contrasts; one verdict JSON. Canonical `summary.md`, `detailed.md`, tables and inspected figures live beside this Protocol only after evidence exists.
>
> Figure contract: (1) per-seed O/R/S/B/C NLL and full/disjoint repair/control contrasts, nats/answer token, source paired arrays, bootstrap intervals; allowed claim is bounded online repair. (2) parent agreement versus task-loss improvement, distinct axes and explicit units, descriptive only; optional if it changes interpretation. No diagram is fabricated from missing data.
>
> ## 15. Success / Failure / Insufficient Evidence
>
> After all technical guards pass, form four contrasts per seed: O−R and S−R on full and disjoint populations.
> - `ONLINE_PARENT_REPAIR_SUPPORTED`: all eight lower 95% endpoints exceed zero.
> - `ONLINE_PARENT_REPAIR_NOT_SUPPORTED`: at least one of the four named comparisons has upper endpoint <=0 in both seeds. State which clause failed; do not imply zero benefit everywhere.
> - `INSUFFICIENT`: every other eligible pattern, including seed disagreement or intervals crossing zero.
> - `INELIGIBLE` / `INCOMPLETE`: technical guard failures / missing required arms.
>
> Report remaining R−B/R−C and recovery magnitude irrespective of verdict. No result automatically licenses a larger model, new teacher or extra training.
>
> ## 16. What This Cannot Claim
>
> Passing shows this finite-budget parent-only supervised repair benefits these frozen models on this internal workload. It does not validate a universal semantic hierarchy, compare teacher layers, prove full-sequence labels are causal, repair contamination, or prove staged coarse-to-fine expert learning. Disjoint records are only an ID-based safeguard, not a semantic decontamination audit. Failure does not prove absent information: classifier capacity, optimization and target ambiguity remain rivals.
>
> One subsequent decision: determine whether the parent-only repair is sufficient to serve as the fixed online baseline for the next diagnosis. If it passes, retain it and quantify remaining gap before changing teacher or fine routing. If it fails or is insufficient, inspect registered training/held-out readout diagnostics to choose a bounded layer/context/readout test; do not start all third-step candidates simultaneously.
>
> ## 17. Block Confirmation, Freeze, And Amendment Ledger
>
> 2026-09-06: researcher stated the first experiment is understood, requested the next validation plan and repositioning within the four-step plan, and explicitly authorized reserved resources. This is not recorded as confirmation of newly proposed shuffled control, subset qualification or training settings.
>
> A question, B data, C supervision, D architecture, E optimization, F evidence, G execution details: PROPOSED. Source identities and prior results: VERIFIED_SOURCE. Reserved quota: HUMAN_CONFIRMED. Scientific implementation/smoke/full-run promotion: pending confirmation of this draft and its Focus account. Internal consistency: PASS_AS_DRAFT; human confirmation: PENDING. No design freeze timestamp or run exists. Confirming the proposed design does not change any P1 result or historical protocol. Any post-start change must be append-only, with timing, old/new values, reason and eligibility impact.
> '''.replace('ANCHOR',anchor))
> f=root/'daily_research_reports/0906/focus_gmm_pseudolabel_handoff.md';s=f.read_text()
> s=s.replace('plain_language_design: HUMAN_CONFIRMED','plain_language_design: STEP1_HUMAN_CONFIRMED; STEP2_AI_REVISED_AWAITING_HUMAN_CONFIRMATION').replace('status: STEP1_COMPLETE_AWAITING_HUMAN_RESULT','status: STEP2_PLAN_READY_AWAITING_DESIGN_CONFIRMATION')
> s=s.replace('当前已查到八任务硬伪路径分支的粗路由缺少训练梯度；是否能解释任务损失仍需路径干预。','第一步已完成：外部纠正粗路径恢复大部分交接损失，原训练粗路由缺少梯度。当前局部验证节点推进为：补足粗路由监督，能否在不改变专家、细路由、标签和读取位置的情况下恢复在线收益。用户已表示理解原实验，要求构建第二步验证计划，并授权标准配额资源；新增具体设计仍为 AI 建议。')
> s=s.replace('## 唯一核心实验：粗路径干预与架构审计','## 实验一（已完成）：粗路径干预与架构审计')
> a=s.index('## 四步关系');b=s.index('执行状态：',a)
> s=s[:a]+'''## 实验二（设计待确认）：只补足粗路由监督
>
> ### 1. 目的
> 把第一步“外部给定粗路径有效”变成一次可部署路由验证，判断原监督缺失能否通过只训练粗路由修复。
>
> ### 2. 假设
> 用原伪标签监督粗路由，应使完全在线的答案损失低于原模型，也低于同预算打乱标签训练。竞争解释是收益仅来自类别比例调整，或只存在于训练中重复出现的题目；这些情况下不支持样本与标签对应关系带来的在线修复。
>
> ### 3. 分析方法
> 1. 固定原两种子检查点的专家、细路由、原标签和实际读取位置，分别只训练粗路由预测原粗标签、或预测按样本打乱但数量相同的粗标签；两组各训练相同的四遍数据，选择固定最后一步。
> 2. 在相同样本上比较原在线、修复后在线、打乱标签后在线，以及外部给定粗路径和完整伪路径两个参考，计算答案预测损失；同时检查粗标签预测情况，但不把分类准确率当作任务收益。
> 3. 保留完整评估以承接第一步，同时单列与训练记录编号不重叠的 384 条样本；只有两个种子在两种样本范围上都可靠优于原在线和打乱对照，才支持本次修复。报告剩余差距，不事后定义“已完全恢复”。
>
> ### 4. 结论分支
> - 满足全部损失比较：支持有限预算下的粗路由在线修复，保留其为后续基线，再判断残余差距是否需要改变标签或细路由。
> - 至少一个必要比较在两个种子上都可靠不支持：指出具体失败环节；若分类改善而任务不改善，不能宣布路由成功。
> - 种子不一致或区间跨零：证据不足；依据预先记录的训练与评估诊断定位下一检查，不同时展开所有候选。
> - 实现、数据或冻结检查失败：结果不具科学判定资格，先处理执行问题。
>
> ## 四步关系
> 1. 已完成：冻结路径干预和架构审计，定位粗路径与监督缺失。
> 2. **当前位置：只补足粗路由监督的验证计划。**训练粗路由；专家和细路由冻结。读取位置暂不改变。
> 3. 第二步仍有断点时：拆分教师层位、上下文范围及读出能力；按结果选择一个诊断。不得预先把第二步失败归因为末层标签错误。
> 4. 候选交接机制成立后：再做路由与专家的功能训练，并验证真正分阶段训练或联合训练的收益。
>
> 本轮未创建新工作流或重置问题。资源偏好已确认：标准配额；不再请求配额选择。第二步新增监督、打乱对照、数据资格检查和训练预算作为完整协议草案交由用户审阅。
>
> '''+s[b:]
> s=s.replace('这仍是待人工选择的下一步；本次外部供给路径没有修好可部署 Router，也没有验证末层标签优劣。','现已据此形成第二步候选设计；本次外部供给路径没有修好可部署 Router，也没有验证末层标签优劣。')
> s=s.replace('## 唯一下一决策\n依据第一步结果，选择第二步的粗路由单独修复或粗细完整修复。','''- [第二步完整协议草案](../../../../experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P2_parent_router_supervision_repair/protocol.md)
>
> ## 唯一下一决策
> 审定“只补足粗路由监督”的候选设计；其结果将决定该修复能否成为下一轮诊断的固定在线基线。保留第一步人工知识表述待确认状态，不把“已经理解”扩写为研究者未亲自陈述的结果结论。
> ''');f.write_text(s)
> p=root/'PROJECTS.md';s=p.read_text().replace('human result wording and step-2 decision pending;', 'step-2 parent-only repair plan drafted under the same Focus; reserved resources authorized; new design confirmation pending; human result wording remains pending;');p.write_text(s)
> print(d/'protocol.md')
> PY
> python /tmp/write_p2_plan.py``
> - Ran `python - <<'PY'
> from pathlib import Path
> import re,os
> r=Path('/data/250010109/Research_System');p=r/'Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P2_parent_router_supervision_repair/protocol.md'
> s=p.read_text();s=s.replace('../../../../../../../daily_research_reports/0906/focus_gmm_pseudolabel_handoff.md',os.path.relpath(r/'daily_research_reports/0906/focus_gmm_pseudolabel_handoff.md',p.parent));p.write_text(s)
> for f in [p,r/'daily_research_reports/0906/focus_gmm_pseudolabel_handoff.md']:
>  for link in re.findall(r'\]\(([^)]+)\)',f.read_text()):
>   assert (f.parent/link).exists(),(f,link)
> print('Links verified; draft has 18 numbered sections:',len(re.findall(r'^## \d+\.',p.read_text(),re.M)))
> PY
> git diff --check`
>
> </details>
</details>

**我们现在位于四步规划的第二步：验证“补足粗路由监督，能否恢复在线收益”。**标准配额资源已记录为你授权使用，无需再次选择配额。

计划已写入[完整协议草案](../../../../experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P2_parent_router_supervision_repair/protocol.md)，并更新了[当前研究任务卡](../../../../focus/focus_gmm_pseudolabel_handoff.md)。

**当前位置与后续顺序**

| 步骤 | 要回答的问题 | 当前状态 |
|---|---|---|
| ① 冻结路径干预 | 外部纠正粗路径是否有效？ | 已完成，恢复大部分交接差距 |
| **② 粗路由监督修复** | **让粗路由自己学，能否恢复在线收益？** | **本次计划** |
| ③ 标签与读出审计 | 剩余困难来自教师层位、上下文还是读出能力？ | 根据第二步结果选择 |
| ④ 功能训练验证 | 修复机制能否支持专家与路由的进一步训练？ | 后续验证 |

**第二步的四段式设计**

**1. 目的**

把“外部给定粗路径有效”推进为“模型自己预测粗路径也有效”。

**2. 假设**

原来的主要缺陷是粗路由没有接受监督。补足监督后，完全在线执行的答案预测损失应下降。

竞争解释是：改善只来自学会类别比例，或者只发生在训练中出现过的题目上。

**3. 分析方法**

- **只训练粗路由。**保留原两个种子的检查点，冻结底座、全部专家和细路由。原伪标签、读取位置、专家系数均不变。每个条件训练四遍原数据，共 128 次参数更新，使用固定最后一步。
- **加入同预算打乱标签对照。**将样本对应的粗标签打乱，但保持各类数量不变。这样可以判断正确的样本—标签对应关系是否带来额外收益。
- **进行完全在线评估。**比较下列五组，并同时报告完整 512 条样本和与训练记录不重叠的 384 条样本。

| 组别 | 是否训练 | 评估时如何选路径 |
|---|---|---|
| 原在线基线 | 不训练 | 原粗路由＋原细路由 |
| **粗路由修复** | **只训练粗路由，使用原伪标签** | **新粗路由＋原细路由** |
| 打乱标签对照 | 只训练粗路由，使用打乱标签 | 新粗路由＋原细路由 |
| 给定粗路径参考 | 不训练 | 外部给定粗组，原细路由在组内选择 |
| 完整伪路径参考 | 不训练 | 外部给定粗细路径 |

这里最重要的是：**修复组评估时不再供给粗标签，必须由新粗路由自己选择。**

**4. 结论与推进分支**

- **支持修复：**两个种子在完整样本和不重叠样本上，都可靠优于原在线基线与打乱对照。随后保留修复模型，判断剩余差距是否值得进入第三步。
- **分类变准、任务损失未改善：**不能宣布路由修复成功，需要检查标签预测与专家效用之间的关系。
- **两个种子不一致或统计区间跨零：**保持证据不足，利用预先记录的训练和评估诊断定位问题。
- **训练本身未学好：**不能直接推断末层标签错误；有限训练预算、线性读出能力和上下文错位仍需区分。

本次不要求事先承诺恢复某个百分比，也不把“小幅改善”表述为“完全恢复”。

资源安排为**单张 H100、标准配额，顺序完成四个粗路由训练条件**，随后统一评估；上限 90 分钟，实际时长需运行后记录。

请确认这份设计，尤其是“只训练粗路由＋打乱标签对照＋不重叠样本资格检查”，即可推进执行。

需要确认的是本次新增的科学设计，不是资源权限。[实验协议技能](../../../../../../../daily_research_reports/0906/docs/.agents/skills/experiment-card-writer/SKILL.md)要求：“Promote the same file … only when every block is CONFIRMED。”因此完整方案目前已落盘为待确认草案，尚未启动训练。

> 确定实验方案，然后现在请你开始此轮任务执行。此轮任务的明确完成标志是：完成实验并且给出确定的四段式实验分析审核。

<details><summary>16 previous messages</summary>

> 方案已确认。我会按协议执行单张 H100 标准配额实验，完成粗路由训练、统一评估和证据核验，最后交付四段式分析；即使结果不支持修复或证据不足，也会按预定判据明确报告。
>
> <details><summary>Explored 6 files, a search, ran 3 commands</summary>
>
> <details><summary>Explored 8 files, a search</summary>
>
> - Read `./.agents/skills/remote-experiment-workflow/SKILL.md`
> - Read `/root/.codex/skills/sco-control/SKILL.md`
> - Read `./daily_research_reports/0906/focus_gmm_pseudolabel_handoff.md`
> - Read `./Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P2_parent_router_supervision_repair/protocol.md`
> - Searched for `AGENTS.md` in `MoE_Router`
> - Read `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/run_remote.sh`
> - Read `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/submit_evaluation.sh`
> - Read `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/intervention.py`
> - Read `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/run_audit.py`
>
> </details>
>
> - Ran ``python - <<'PY'
> from pathlib import Path
> from datetime import datetime,timezone
> r=Path('/data/250010109/Research_System');p=r/'Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P2_parent_router_supervision_repair/protocol.md'
> s=p.read_text();s=s.replace('Document status: `DRAFT_NOT_EXECUTABLE`. Scientific choices below are `AI_PROPOSAL` unless explicitly attributed to inspected sources. No implementation or training has begun.','Document status: `APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN_AND_ANALYSIS`. All A–G scientific choices and the Focus account are HUMAN_CONFIRMED by the execution instruction on 2026-09-06. Cross-block consistency: PASS.')
> s=s.replace('A–G: PROPOSED; internal consistency checked, human design confirmation pending. Existing P1 design remains frozen. New Focus experiment account is awaiting confirmation.','A–G: CONFIRMED; cross-block consistency PASS. Existing P1 design remains frozen. P2 implementation, smoke, full execution and four-part analysis are explicitly approved.')
> s+='\nExecution approval receipt '+datetime.now(timezone.utc).isoformat()+': researcher explicitly confirmed the experiment and requested completion through the audited four-part analysis. All A–G and Focus experiment-two design confirmed; implementation, smoke, four training runs and full evaluation/analysis approved on the already authorized single reserved H100. The earlier draft-status entries below the scientific body are historical. Scientific body frozen as revision 20260906-P2-v1; subsequent material changes require append-only amendments.\n'
> p.write_text(s)
> f=r/'daily_research_reports/0906/focus_gmm_pseudolabel_handoff.md';s=f.read_text().replace('STEP2_AI_REVISED_AWAITING_HUMAN_CONFIRMATION','STEP2_HUMAN_CONFIRMED').replace('status: STEP2_PLAN_READY_AWAITING_DESIGN_CONFIRMATION','status: STEP2_APPROVED_EXECUTION_IN_PROGRESS').replace('实验二（设计待确认）','实验二（设计已确认，执行中）');s+='\n执行授权：用户明确确认第二步完整方案，并要求完成实验与四段式分析审核；标准配额单张 H100。全部设计、实现、小样本与完整运行、结果审核已授权，继续执行不再重复询问。\n';f.write_text(s)
> p=r/'PROJECTS.md';s=p.read_text().replace('new design confirmation pending;', 'P2 design confirmed; implementation, smoke, full run and four-part analysis authorized, execution in progress;');p.write_text(s)
> PY
> mkdir -p /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair
> cat /root/.codex/plugins/cache/openai-curated-remote/superpowers/6.3.0/skills/test-driven-development/SKILL.md | head -65``
>
> - Ran `cat > /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair/test_core.py <<'PY'
> import numpy as np
> import torch
> from core import token_indices, shuffled_labels, verdict, deployment_arguments
>
> def test_ragged_examples_broadcast_after_shuffle():
>     offsets=torch.tensor([0,2,3,6]); labels=torch.tensor([0,1,2])
>     indices, targets=token_indices(offsets,torch.tensor([2,0]),labels)
>     assert indices.tolist()==[3,4,5,0,1]
>     assert targets.tolist()==[2,2,2,0,0]
>     shuffled, permutation=shuffled_labels(labels,20260906)
>     assert torch.equal(shuffled, labels[permutation])
>     assert torch.equal(shuffled.sort().values,labels.sort().values)
>
> def test_online_cannot_consume_teacher_and_reference_is_explicit():
>     p,l=torch.tensor([1]),torch.tensor([4])
>     for k in ['O','R','S']:
>         assert deployment_arguments(k,p,l)=={'unit':True,'stage':2}
>     assert deployment_arguments('B',p,l)['forced_parent'] is p
>     assert deployment_arguments('C',p,l)['forced_leaf'] is l
>
> def test_verdict_conjunction_and_repeated_failed_clause():
>     rows=[dict(seed=s,population=p,contrast=c,ci_low=.01,ci_high=.02) for s in [17,29] for p in ['full','disjoint'] for c in ['repair','label_specific']]
>     assert verdict(rows)=='ONLINE_PARENT_REPAIR_SUPPORTED'
>     rows[0]['ci_low']=-.01
>     assert verdict(rows)=='INSUFFICIENT'
>     rows[0]['ci_high']=-.001;rows[4]['ci_low']=-.01;rows[4]['ci_high']=-.001
>     assert verdict(rows)=='ONLINE_PARENT_REPAIR_NOT_SUPPORTED'
> PY
> python -m pytest -q /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair/test_core.py`
>
> - Ran `cat > /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair/core.py <<'PY'
> import numpy as np
> import torch
>
> def token_indices(offsets, examples, labels):
>     starts=offsets[examples];lengths=offsets[examples+1]-starts
>     indices=torch.cat([torch.arange(int(s),int(s+n)) for s,n in zip(starts,lengths)])
>     return indices, torch.repeat_interleave(labels[examples],lengths)
>
> def shuffled_labels(labels,seed):
>     permutation=torch.from_numpy(np.random.default_rng(seed).permutation(len(labels)))
>     return labels[permutation],permutation
>
> def deployment_arguments(condition,parent=None,leaf=None):
>     args={'unit':True,'stage':2}
>     if condition=='B':args['forced_parent']=parent
>     elif condition=='C':args['forced_leaf']=leaf
>     elif condition not in ['O','R','S']:raise ValueError(condition)
>     return args
>
> def verdict(rows):
>     assert len(rows)==8
>     if all(r['ci_low']>0 for r in rows):return 'ONLINE_PARENT_REPAIR_SUPPORTED'
>     for pop in ['full','disjoint']:
>         for contrast in ['repair','label_specific']:
>             group=[r for r in rows if r['population']==pop and r['contrast']==contrast]
>             if len(group)==2 and all(r['ci_high']<=0 for r in group):return 'ONLINE_PARENT_REPAIR_NOT_SUPPORTED'
>     return 'INSUFFICIENT'
> PY
> python -m pytest -q /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair/test_core.py`
>
> </details>
>
> 执行协议已冻结。实现检查目前通过了三项测试：样本标签按正确位置展开、在线评估不接收教师标签、判定程序严格要求所有必要比较通过。接下来会先检查缓存表示与原模型一致、只有粗路由获得梯度，再开始正式训练。
>
> <details><summary>Ran 3 commands</summary>
>
> - Ran `cat > /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair/run_experiment.py <<'PY'
> from pathlib import Path
> import sys,os,json,time,hashlib,argparse,math
> os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION']='python'
> os.environ['HF_HUB_OFFLINE']='1';os.environ['TRANSFORMERS_OFFLINE']='1'
> sys.path.insert(0,'/data/250010109/dependency_packages/hf_transformers_qwen3')
> P1=Path('/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention')
> sys.path.insert(0,str(P1))
> import numpy as np
> import torch
> import torch.nn.functional as F
> import transformers
> from intervention import CoarseInterventionModel,E14,E07
> from training import build_adapter,answer_token_loss,balanced_order,e07
> from registry import condition_matrix
> from core import token_indices,shuffled_labels,deployment_arguments
> W=Path(__file__).parent
> OLD=E14/'runs/full-20260903T042000Z'
> P1RUN=P1/'runs/reserved-20260906-p1-v2/full'
> DATA=Path('/data/250010109/datasets/a15_e14_benchmark/processed.pt')
> PROTOCOL=Path('/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P2_parent_router_supervision_repair/protocol.md')
>
> def digest(p):
>  h=hashlib.sha256()
>  with Path(p).open('rb') as f:
>   for b in iter(lambda:f.read(1<<20),b''):h.update(b)
>  return h.hexdigest()
>
> def savej(p,x):
>  temp=Path(str(p)+'.tmp');temp.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n');temp.replace(p)
>
> def subset(store,n):return {k:v[:n] for k,v in store.items()}
>
> def frozen_equal(adapter,state):
>  return all(torch.equal(v.detach().cpu(),state[k]) for k,v in adapter.state_dict().items() if not k.startswith('parent_router.'))
>
> @torch.no_grad()
> def evaluate(model,store,parents,leaves,condition):
>  vals={k:[] for k in ['loss_sum','token_count','route','parent_route','parent_ce_sum','parent_correct','parent_load','correct_parent_loss_sum','correct_parent_token_count']}
>  for start in range(0,len(parents),8):
>   ids,att,labels=(store[k][start:start+8].cuda() for k in ['input_ids','attention_mask','labels'])
>   p,l=parents[start:start+8].cuda(),leaves[start:start+8].cuda()
>   logits,out,_=model(ids,att,**deployment_arguments(condition,p,l))
>   assert (model.adapter.leaf_parent[out.route]==out.parent_route).all()
>   if condition in ['B','C']:assert (out.parent_route==p[:,None]).all()
>   if condition=='C':assert (out.route==l[:,None]).all()
>   if condition in ['O','R','S']:assert model.context.forced_parent is None and model.context.forced_leaf is None
>   loss,mask=answer_token_loss(logits,labels,'none')
>   target=p[:,None].expand_as(mask)
>   scores=out.parent_logits[:,:-1].float()
>   ce=F.cross_entropy(scores.reshape(-1,3),target.reshape(-1),reduction='none').reshape_as(mask)
>   correct=out.parent_route[:,:-1]==target
>   pred=out.parent_route[:,:-1]
>   for k,v in {'loss_sum':(loss*mask).sum(1),'token_count':mask.sum(1),'route':out.route[:,:-1][mask],
>               'parent_route':pred[mask],'parent_ce_sum':(ce*mask).sum(1),'parent_correct':(correct*mask).sum(1),
>               'parent_load':torch.stack([((pred==g)*mask).sum(1) for g in range(3)],1),
>               'correct_parent_loss_sum':(loss*mask*correct).sum(1),'correct_parent_token_count':(mask*correct).sum(1)}.items():
>    assert torch.isfinite(v).all();vals[k].append(v.cpu().numpy())
>  result={k:np.concatenate(v) for k,v in vals.items()}
>  result.update(source=store['source'].numpy(),record_id=np.asarray(store['record_id']),sample_index=np.arange(len(parents)))
>  return result
>
> def replay(result,seed,condition):
>  arm={'O':'A','B':'B','C':'C'}[condition]
>  old=dict(np.load(P1RUN/f'seed{seed}_{arm}.npz'));n=len(result['token_count']);nt=int(result['token_count'].sum())
>  check={k:bool(np.array_equal(result[k],old[k][:nt if k in ['route','parent_route'] else n])) for k in ['token_count','source','route','parent_route']}
>  check['nll_abs_error']=float(abs(result['loss_sum'].astype(float).sum()-old['loss_sum'][:n].astype(float).sum())/nt)
>  check['per_example_loss_max_error']=float(abs(result['loss_sum']-old['loss_sum'][:n]).max())
>  assert all(check[k] for k in ['token_count','source','route','parent_route']) and check['nll_abs_error']<=1e-4,check
>  return check
>
> @torch.no_grad()
> def extract(model,store,output):
>  rows=[];lengths=[]
>  for start in range(0,len(store['source']),8):
>   ids,att,labels=(store[k][start:start+8].cuda() for k in ['input_ids','attention_mask','labels'])
>   model.context.forced_parent=None;model.context.forced_leaf=None;model.context.unit=True;model.context.stage=2
>   model.backbone.model(input_ids=ids,attention_mask=att,use_cache=False,return_dict=True)
>   state=model.context.state[:,:-1];mask=labels[:,1:]!=-100
>   direct=model.adapter.parent_router(state)
>   assert torch.equal(direct,model.context.output.parent_logits[:,:-1])
>   cached=state[mask].detach().cpu().clone()
>   assert torch.equal(cached.cuda(),state[mask])
>   # Matched-shape float32 reconstruction protects cache dtype and row ordering.
>   a=F.linear(cached.cuda().float(),model.adapter.parent_router.weight.float(),model.adapter.parent_router.bias.float())
>   b=F.linear(state[mask].float(),model.adapter.parent_router.weight.float(),model.adapter.parent_router.bias.float())
>   assert float((a-b).abs().max())<=1e-5
>   rows.append(cached);lengths.append(mask.sum(1).cpu())
>   if start%512==0:print(json.dumps({'cache':output.name,'done':start+len(ids),'total':len(store['source'])}),flush=True)
>  cache={'states':torch.cat(rows),'offsets':torch.cat([torch.zeros(1,dtype=torch.long),torch.cat(lengths).cumsum(0)])}
>  torch.save(cache,output);return cache
>
> @torch.no_grad()
> def causal_guard(model,store):
>  ids,att=(store[k][:8].cuda() for k in ['input_ids','attention_mask'])
>  model(ids,att,unit=True);h=model.context.state.detach().clone();logits=model.context.output.parent_logits.detach().clone()
>  altered=ids.clone();altered[:,32:]=(altered[:,32:]+1)%model.backbone.config.vocab_size
>  model(altered,att,unit=True)
>  hd=float((h[:,:32].float()-model.context.state[:,:32].float()).abs().max())
>  ld=float((logits[:,:32].float()-model.context.output.parent_logits[:,:32].float()).abs().max())
>  assert hd<=1e-5 and ld<=1e-5,(hd,ld)
>  return {'hidden_max_error':hd,'parent_logits_max_error':ld,'cut_position':32}
>
> @torch.no_grad()
> def classifier_metrics(layer,cache,labels):
>  n=int(cache['offsets'][-1]);ce=0.;correct=0;counts=torch.diff(cache['offsets']);targets=torch.repeat_interleave(labels,counts)
>  for start in range(0,n,16384):
>   y=targets[start:start+16384].cuda();logits=layer(cache['states'][start:start+16384].cuda().float())
>   ce+=float(F.cross_entropy(logits,y,reduction='sum'));correct+=int((logits.argmax(-1)==y).sum())
>  return {'ce':ce/n,'accuracy':correct/n,'tokens':n}
>
> def train_parent(initial,cache,dev,labels,true_labels,dev_labels,source,seed,arm,out,smoke=False):
>  out.mkdir(parents=True,exist_ok=False)
>  torch.manual_seed(seed)
>  layer=torch.nn.Linear(1024,3,device='cuda',dtype=torch.float32)
>  layer.load_state_dict({k:v.cuda().float() for k,v in initial.items()})
>  assert all(torch.equal(v.cpu().bfloat16(),initial[k]) for k,v in layer.state_dict().items())
>  opt=torch.optim.AdamW(layer.parameters(),lr=5e-4,weight_decay=.01,betas=(.9,.999),eps=1e-8)
>  def factor(step):
>   if step<5:return (step+1)/5
>   return .5*(1+math.cos(math.pi*min((step-5)/123,1)))
>  sched=torch.optim.lr_scheduler.LambdaLR(opt,factor)
>  history=[];updates=0;seen=0;gradient_norms=[]
>  states=cache['states'].cuda();offsets=cache['offsets']
>  def snapshot(update):
>   torch.save({'parent':{k:v.detach().cpu().clone() for k,v in layer.state_dict().items()},'update':update},out/f'update_{update:04d}.pt')
>   row={'update':update,'train_true':classifier_metrics(layer,cache,true_labels),'development_true':classifier_metrics(layer,dev,dev_labels)}
>   history.append(row);print(json.dumps({'seed':seed,'arm':arm,**row}),flush=True)
>  snapshot(0)
>  micro_history=[]
>  for epoch in range(4 if not smoke else 2):
>   order=balanced_order(source,seed,epoch) if not smoke else torch.arange(len(source))
>   opt.zero_grad(set_to_none=True);pending=0;total=0.
>   for start in range(0,len(order),8):
>    examples=order[start:start+8];idx,target=token_indices(offsets,examples,labels)
>    logits=layer(states[idx.cuda()].float());loss=F.cross_entropy(logits,target.cuda())
>    (loss/16).backward();pending+=1;seen+=len(idx);total+=float(loss.detach())
>    assert all(p.grad is not None and torch.isfinite(p.grad).all() for p in layer.parameters())
>    if pending==16 or start+8>=len(order):
>     gn=float(torch.nn.utils.clip_grad_norm_(layer.parameters(),1.));assert math.isfinite(gn)
>     gradient_norms.append(gn);opt.step();sched.step();opt.zero_grad(set_to_none=True);updates+=1
>     micro_history.append({'update':updates,'epoch':epoch,'objective':total/pending,'seen_tokens':seen,'lr_after_update':opt.param_groups[0]['lr']})
>     pending=0;total=0.
>     if updates in [32,64,96,128]:snapshot(updates)
>   if smoke and updates>=2:break
>  assert updates==(2 if smoke else 128)
>  if not smoke:assert seen==911644
>  changed=max(float((v.detach().cpu()-initial[k].float()).abs().max()) for k,v in layer.state_dict().items());assert changed>0
>  assert max(gradient_norms)>0
>  torch.save({'parent':{k:v.detach().cpu().clone() for k,v in layer.state_dict().items()},'updates':updates,'seen_tokens':seen},out/'final.pt')
>  savej(out/'history.json',history);savej(out/'updates.json',micro_history)
>  guard={'updates':updates,'passes':2 if smoke else 4,'seen_tokens':seen,'parent_parameters':3075,'parent_max_change_fp32':changed,'gradient_norm_min':min(gradient_norms),'gradient_norm_max':max(gradient_norms),'snapshot_updates':[h['update'] for h in history]}
>  savej(out/'training_audit.json',guard)
>  return {k:v.detach().cpu().bfloat16() for k,v in layer.state_dict().items()},guard
>
> def main(out):
>  out.mkdir(parents=True,exist_ok=False);start=time.time()
>  meta={'status':'RUNNING','started':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'torch':torch.__version__,'python':sys.version,'transformers':transformers.__version__,'numpy':np.__version__,'gpu':torch.cuda.get_device_name(0),'replay':{},'seeds':{}}
>  savej(out/'metadata.json',meta)
>  try:
>   oldmeta=json.loads((P1RUN/'metadata.json').read_text())
>   for path,expected in [(DATA,oldmeta['data_sha256']),(OLD/'pseudo_labels/benchmark/assignments.pt',oldmeta['pseudo_sha256'])]:assert digest(path)==expected
>   meta['data_sha256']=digest(DATA);meta['pseudo_sha256']=oldmeta['pseudo_sha256']
>   sourcefiles=[Path(__file__),W/'core.py',P1/'intervention.py',E14/'training.py',E14/'models.py',E14/'registry.py',E07/'runtime.py',PROTOCOL]
>   meta['source_sha256']={str(f):digest(f) for f in sourcefiles}
>   data=torch.load(DATA,map_location='cpu',weights_only=False)['splits'];pseudo=torch.load(OLD/'pseudo_labels/benchmark/assignments.pt',map_location='cpu',weights_only=False)['splits']
>   trainids=set(data['train']['record_id']);disjoint=np.array([x not in trainids for x in data['evaluation']['record_id']]);assert disjoint.sum()==384
>   np.save(out/'disjoint_mask.npy',disjoint)
>   meta['disjoint_examples']=384;meta['disjoint_answer_tokens']=int((data['evaluation']['labels'][disjoint,1:]!=-100).sum())
>   labels=pseudo['train']['parent'];shuffled,perm=shuffled_labels(labels,20260906)
>   np.save(out/'shuffle_permutation.npy',perm.numpy());meta['shuffle_label_unchanged_fraction']=float((shuffled==labels).float().mean());meta['shuffle_counts']=torch.bincount(shuffled,minlength=3).tolist()
>   savej(out/'metadata.json',meta)
>   backbone=e07.load_backbone(torch.device('cuda'))
>   for seed in [17,29]:
>    directory=out/f'seed{seed}';directory.mkdir()
>    cond=next(c for c in condition_matrix() if c.key==f'benchmark__HIER_GMM_HARD_R8__seed{seed}')
>    checkpoint=OLD/'conditions'/cond.key/'final.pt';assert digest(checkpoint)==oldmeta['checkpoints'][str(seed)]
>    state=torch.load(checkpoint,map_location='cpu',weights_only=False)['adapter'];adapter=build_adapter(OLD,cond,torch.device('cuda'));adapter.load_state_dict(state)
>    initial={k:v.detach().cpu().clone() for k,v in adapter.parent_router.state_dict().items()}
>    model=CoarseInterventionModel(backbone,adapter).eval();model.requires_grad_(False)
>    guards={'checkpoint_sha256':digest(checkpoint),'causal':causal_guard(model,data['train'])}
>    # Original-runtime replay and tiny disposable parent updates precede scale-up.
>    tiny_eval=subset(data['evaluation'],8);tp=pseudo['evaluation']['parent'][:8];tl=pseudo['evaluation']['global'][:8]
>    for arm in ['O','B','C']:meta['replay'][f'{seed}_{arm}_smoke']=replay(evaluate(model,tiny_eval,tp,tl,arm),seed,arm)
>    tiny_train=extract(model,subset(data['train'],8),directory/'smoke_cache.pt')
>    tiny_dev=extract(model,subset(data['development'],8),directory/'smoke_dev_cache.pt')
>    originals={arm:evaluate(model,tiny_eval,tp,tl,arm) for arm in ['B','C']}
>    for arm,targets in [('R',labels[:8]),('S',shuffled[:8])]:
>     trained,audit=train_parent(initial,tiny_train,tiny_dev,targets,labels[:8],pseudo['development']['parent'][:8],data['train']['source'][:8],seed,arm,directory/f'smoke_{arm}',smoke=True)
>     adapter.parent_router.load_state_dict(trained)
>     assert frozen_equal(adapter,state)
>     for reference in ['B','C']:
>      after=evaluate(model,tiny_eval,tp,tl,reference)
>      for key in ['loss_sum','route','parent_route']:assert np.array_equal(after[key],originals[reference][key]),'teacher reference changed'
>     adapter.parent_router.load_state_dict(initial)
>    assert all(torch.equal(v.detach().cpu(),state[k]) for k,v in adapter.state_dict().items())
>    guards['smoke']='PASS';savej(directory/'guards.json',guards)
>    caches={split:extract(model,data[split],directory/f'{split}_cache.pt') for split in ['train','development']}
>    assert int(caches['train']['offsets'][-1])==227911
>    savej(directory/'cache_manifest.json',{split:{'path':str(directory/f'{split}_cache.pt'),'sha256':digest(directory/f'{split}_cache.pt'),'tokens':int(caches[split]['offsets'][-1])} for split in caches})
>    finals={};training={}
>    for arm,targets in [('R',labels),('S',shuffled)]:
>     finals[arm],training[arm]=train_parent(initial,caches['train'],caches['development'],targets,labels,pseudo['development']['parent'],data['train']['source'],seed,arm,directory/arm)
>    for arm in ['O','R','S','B','C']:
>     adapter.parent_router.load_state_dict(finals[arm] if arm in finals else initial)
>     result=evaluate(model,data['evaluation'],pseudo['evaluation']['parent'],pseudo['evaluation']['global'],arm)
>     np.savez_compressed(directory/f'{arm}.npz',**result)
>     if arm in ['O','B','C']:meta['replay'][f'{seed}_{arm}_full']=replay(result,seed,arm)
>     assert frozen_equal(adapter,state)
>     print(json.dumps({'seed':seed,'condition':arm,'nll':float(result['loss_sum'].astype(float).sum()/result['token_count'].sum())}),flush=True)
>    adapter.parent_router.load_state_dict(initial)
>    assert all(torch.equal(v.detach().cpu(),state[k]) for k,v in adapter.state_dict().items())
>    guards['frozen_nonparent']='PASS';guards['restored_all_original']='PASS';guards['B_C_parent_invariance']='PASS';guards['training']=training
>    savej(directory/'guards.json',guards);meta['seeds'][str(seed)]=guards;savej(out/'metadata.json',meta)
>    model.close();del model,adapter,caches;torch.cuda.empty_cache()
>   assert all(digest(p)==v for p,v in meta['source_sha256'].items()),'source changed during run'
>   meta['status']='FULL_RUN_COMPLETE';meta['training_updates']=512;meta['elapsed_seconds']=time.time()-start;savej(out/'metadata.json',meta)
>  except BaseException as exc:
>   meta['status']='FAILED';meta['error']=repr(exc);meta['elapsed_seconds']=time.time()-start;savej(out/'metadata.json',meta);raise
>
> if __name__=='__main__':
>  p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args();main(args.output)
> PY
> python -m py_compile /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair/run_experiment.py`
> - Ran `python - <<'PY'
> from pathlib import Path
> import shutil
> w=Path('/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair');old=w.parent/'20260906_a15_13_e14_p1_coarse_path_intervention'
> p=w/'run_experiment.py';s=p.read_text();s=s.replace("E07/'runtime.py',PROTOCOL]","E07/'runtime.py',W/'protocol_snapshot.md']");p.write_text(s)
> protocol=Path('/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P2_parent_router_supervision_repair/protocol.md');shutil.copy2(protocol,w/'protocol_snapshot.md')
> s=(old/'submit_evaluation.sh').read_text().replace('a15-e14-p1-frozen-eval','a15-e14-p2-parent-repair').replace('Single H100 evaluation, quota=%s, zero training updates, 90-minute process limit','Single H100 parent repair, quota=%s, four training runs, 90-minute process limit');(w/'submit.sh').write_text(s)
> s=(old/'run_remote.sh').read_text();s=s[:s.index('python -m pytest')]+'''python -m pytest -q "${ROOT}/test_core.py" >"${ROOT}/runs/${STAMP}/tests.log" 2>&1
> python "${ROOT}/run_experiment.py" --output "${ROOT}/runs/${STAMP}/full" >"${ROOT}/runs/${STAMP}/full.log" 2>&1
> ''';(w/'run_remote.sh').write_text(s)
> PY
> bash -n /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair/run_remote.sh
> ALLOW_SUBMIT=1 EVAL_QUOTA=reserved RUN_STAMP=reserved-20260906-p2-v1 bash /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair/submit.sh`
> - Ran `tail -10 /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair/runs/reserved-20260906-p2-v1/full.log`
>
> </details>
>
> 标准配额作业 `pt-i5ukbgg1` 已提交。它会先完成原路径重放和小样本梯度检查，再从原检查点分别训练“正确标签”和“打乱标签”两组粗路由；检查未通过时不会进入正式结果判定。
>
> <details><summary>Ran a command</summary>
>
> - Ran `cat > /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair/analyze.py <<'PY'
> from pathlib import Path
> import argparse,json,csv
> import numpy as np
> import matplotlib
> matplotlib.use('Agg')
> import matplotlib.pyplot as plt
> from core import verdict
>
> def csvwrite(path,rows):
>  with path.open('w',newline='') as f:
>   w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
>
> def main(run,out):
>  meta=json.loads((run/'metadata.json').read_text());assert meta['status']=='FULL_RUN_COMPLETE'
>  out.mkdir(parents=True,exist_ok=True)
>  subset=np.load(run/'disjoint_mask.npy');assert subset.sum()==384
>  rng=np.random.default_rng(20260906)
>  ids={'full':np.arange(512),'disjoint':np.flatnonzero(subset)}
>  draws={p:rng.integers(0,len(v),size=(2000,len(v))) for p,v in ids.items()}
>  rows=[];contrasts=[];auxiliary=[];sources=[];recovery=[]
>  for seed in [17,29]:
>   data={k:dict(np.load(run/f'seed{seed}/{k}.npz')) for k in ['O','R','S','B','C']}
>   for k,d in data.items():
>    assert np.array_equal(d['record_id'],data['O']['record_id']) and np.array_equal(d['token_count'],data['O']['token_count'])
>    d['loss_sum']=d['loss_sum'].astype(np.float64);assert np.isfinite(d['loss_sum']).all()
>   for pop,idx in ids.items():
>    n=data['O']['token_count'][idx]
>    for arm,d in data.items():
>     rows.append({'seed':seed,'population':pop,'condition':arm,'examples':len(idx),'tokens':int(n.sum()),'nll':float(d['loss_sum'][idx].sum()/n.sum()),'parent_agreement':float(d['parent_correct'][idx].sum()/n.sum()),'parent_ce':float(d['parent_ce_sum'][idx].astype(float).sum()/n.sum()),**{f'parent_load_{i}':int(d['parent_load'][idx,i].sum()) for i in range(3)}})
>    for name,left,right in [('repair','O','R'),('label_specific','S','R'),('residual_parent','R','B'),('residual_full','R','C')]:
>     diff=data[left]['loss_sum'][idx]-data[right]['loss_sum'][idx]
>     boots=diff[draws[pop]].sum(1)/n[draws[pop]].sum(1);lo,hi=np.quantile(boots,[.025,.975])
>     row={'seed':seed,'population':pop,'contrast':name,'left':left,'right':right,'delta':float(diff.sum()/n.sum()),'ci_low':float(lo),'ci_high':float(hi)}
>     (contrasts if name in ['repair','label_specific'] else auxiliary).append(row)
>    losses={arm:float(d['loss_sum'][idx].sum()/n.sum()) for arm,d in data.items()}
>    den=losses['O']-losses['B'];recovery.append({'seed':seed,'population':pop,'recovery':(losses['O']-losses['R'])/den if den else None,'denominator':den})
>   for arm,d in data.items():
>    for source in np.unique(d['source']):
>     idx=d['source']==source;n=d['token_count'][idx];sources.append({'seed':seed,'condition':arm,'source':int(source),'examples':int(idx.sum()),'tokens':int(n.sum()),'nll':float(d['loss_sum'][idx].sum()/n.sum())})
>    for match in [True,False]:
>     sums=d['correct_parent_loss_sum'] if match else d['loss_sum']-d['correct_parent_loss_sum']
>     tokens=d['correct_parent_token_count'] if match else d['token_count']-d['correct_parent_token_count']
>     sources.append({'seed':seed,'condition':arm,'source':'correct_parent' if match else 'wrong_parent','examples':int((tokens>0).sum()),'tokens':int(tokens.sum()),'nll':float(sums.astype(float).sum()/tokens.sum()) if tokens.sum() else None})
>  result={'verdict':verdict(contrasts),'conditions':rows,'contrasts':contrasts,'auxiliary':auxiliary,'recovery':recovery,'bootstrap':{'draws':2000,'seed':20260906,'unit':'paired evaluation record','interval':'percentile 95%','scope':'conditional on fixed checkpoints; full and record-disjoint populations'},'source_run':str(run)}
>  (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
>  for name,records in [('conditions',rows),('contrasts',contrasts),('auxiliary',auxiliary),('source_and_strata',sources),('recovery',recovery)]:csvwrite(out/f'{name}.csv',records)
>  plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
>  colors={17:'#2566a8',29:'#d97820'}
>  fig,axes=plt.subplots(2,2,figsize=(12,8),layout='constrained')
>  for j,pop in enumerate(['full','disjoint']):
>   for seed in [17,29]:
>    line=[next(r['nll'] for r in rows if r['seed']==seed and r['population']==pop and r['condition']==arm) for arm in ['O','R','S','B','C']]
>    axes[j,0].plot(range(5),line,'o-',color=colors[seed],label=f'Seed {seed}')
>    for i,c in enumerate(['repair','label_specific']):
>     r=next(r for r in contrasts if r['seed']==seed and r['population']==pop and r['contrast']==c)
>     axes[j,1].errorbar(i+(-.06 if seed==17 else .06),r['delta'],yerr=[[r['delta']-r['ci_low']],[r['ci_high']-r['delta']]],fmt='o',color=colors[seed],capsize=4)
>   axes[j,0].set_xticks(range(5),['O\nOriginal','R\nRepaired','S\nShuffled','B\nTeacher parent','C\nFull teacher'])
>   axes[j,0].set_ylabel('Answer NLL (nats/token); lower is better');axes[j,0].set_title(f'{pop.title()}: {len(ids[pop])} evaluation records');axes[j,0].legend()
>   axes[j,1].axhline(0,color='gray',ls='--');axes[j,1].set_xticks(range(2),['O minus R\nRepair','S minus R\nLabel-specific benefit'])
>   axes[j,1].set_ylabel('NLL reduction (nats/token)');axes[j,1].set_title('Paired-record 95% intervals')
>  fig.savefig(out/'online_parent_repair.png',dpi=180);plt.close(fig)
>  fig,axes=plt.subplots(1,2,figsize=(11,4),layout='constrained')
>  for seed in [17,29]:
>   for arm,style in [('R','-'),('S','--')]:
>    history=json.loads((run/f'seed{seed}/{arm}/history.json').read_text())
>    axes[0].plot([r['update'] for r in history],[r['development_true']['accuracy'] for r in history],style+'o',color=colors[seed],label=f'{arm}, seed {seed}')
>    row=next(r for r in rows if r['seed']==seed and r['population']=='full' and r['condition']==arm)
>    baseline=next(r['nll'] for r in rows if r['seed']==seed and r['population']=='full' and r['condition']=='O')
>    axes[1].scatter([row['parent_agreement']],[baseline-row['nll']],color=colors[seed],marker='o' if arm=='R' else 'x',s=65)
>    axes[1].annotate(f'{arm}/{seed}',(row['parent_agreement'],baseline-row['nll']),xytext=(5,5),textcoords='offset points')
>  axes[0].set_xlabel('Parent optimizer updates');axes[0].set_ylabel('Development true-parent agreement');axes[0].set_title('R = real labels; S = shuffled labels');axes[0].legend()
>  axes[1].set_xlabel('Evaluation parent agreement');axes[1].set_ylabel('Original minus condition NLL (nats/token)');axes[1].axhline(0,color='gray',ls='--');axes[1].set_title('Classification and task effects are distinct')
>  fig.savefig(out/'parent_readout_and_task.png',dpi=180);plt.close(fig)
>  print(json.dumps({'verdict':result['verdict'],'contrasts':contrasts,'recovery':recovery,'conditions':rows},indent=2))
>
> if __name__=='__main__':
>  p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();main(a.run,a.output)
> PY
> python - <<'PY'
> import json,subprocess
> c='/data/250010109/MoE_Router/experiments/20260730_h768_4layer_switch_5090_smoke/scripts/sco_acp_compat.sh'
> m=json.loads(subprocess.check_output(['bash',c,'jobs','describe','--workspace-name=share-space','-o','json','pt-i5ukbgg1'],text=True));print({k:m.get(k) for k in ['name','state','start_time']})
> from pathlib import Path
> p=Path('/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair/runs/reserved-20260906-p2-v1/full.log')
> if p.exists():print(p.read_text().replace('\x00','')[-2500:])
> PY`
>
> </details>
>
> 首轮作业在缓存一致性检查处停止，尚未开始正式训练。检查代码把“完整序列上的路由计算”与“提前去掉最后一个位置后的计算”作了逐值比较，两者计算形状不同。我会修正为相同形状的比较，保留原容差与实验设置，再从原检查点重新运行。
>
> <details><summary>Ran 6 commands</summary>
>
> - Ran ``python - <<'PY'
> from pathlib import Path
> w=Path('/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair');p=w/'run_experiment.py';s=p.read_text().replace('direct=model.adapter.parent_router(state)\n  assert torch.equal(direct,model.context.output.parent_logits[:,:-1])','direct=model.adapter.parent_router(model.context.state)\n  assert torch.equal(direct,model.context.output.parent_logits)');p.write_text(s)
> p=Path('/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P2_parent_router_supervision_repair/protocol.md');s=p.read_text();s+='\nEngineering receipt: first reserved job `pt-i5ukbgg1` stopped during seed-17 cache smoke before any formal parent training. O/B/C replay and causal suffix guards had passed. The cache guard recomputed parent logits over 511 positions but compared with the 512-position forward sliced afterwards; this was not the registered identical-operation comparison. Repair recomputes full-shape logits before masking, preserving strict equality, all tolerances and all scientific settings. First failure retained; restart in a fresh directory with the same approved resource.\n';p.write_text(s)
> PY
> ALLOW_SUBMIT=1 EVAL_QUOTA=reserved RUN_STAMP=reserved-20260906-p2-v2 bash /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair/submit.sh``
> - Ran `cat .agents/skills/experiment-card-writer/references/result_evidence_lineage.md .agents/skills/experiment-card-writer/references/detailed_record_standard.md .agents/skills/experiment-card-writer/references/plain_language_completion_reply.md`
> - Ran `python - <<'PY'
> from pathlib import Path
> p=Path('/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair/runs/reserved-20260906-p2-v2/full.log')
> print(p.read_text().replace('\x00','')[-2200:] if p.exists() else 'Awaiting worker logs')
> PY
> python -m py_compile /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair/analyze.py`
> - Ran `python - <<'PY'
> import subprocess,json
> c='/data/250010109/MoE_Router/experiments/20260730_h768_4layer_switch_5090_smoke/scripts/sco_acp_compat.sh'
> m=json.loads(subprocess.check_output(['bash',c,'jobs','describe','--workspace-name=share-space','-o','json','pt-diap9xc9'],text=True));print({k:m.get(k) for k in ['name','state','start_time']})
> PY`
> - Ran `python - <<'PY'
> from pathlib import Path
> p=Path('/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair/runs/reserved-20260906-p2-v2/full.log');print(p.read_text().replace('\x00','')[-2000:] if p.exists() else 'No log yet')
> PY`
> - Ran `python - <<'PY'
> from pathlib import Path
> import json
> p=Path('/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair/runs/reserved-20260906-p2-v2')
> f=p/'full.log';print(f.read_text().replace('\x00','')[-2400:] if f.exists() else 'No log')
> f=p/'full/metadata.json'
> if f.exists():
>  m=json.loads(f.read_text());print({k:m.get(k) for k in ['status','error','disjoint_answer_tokens','started']})
> PY`
>
> </details>
>
> 替代作业已通过小样本检查并进入正式训练。第一个种子的正确标签组已完成 128 次更新，开发集粗标签预测准确率从约 19.5% 升至 90.1%；这只说明监督已生效，是否恢复任务收益还要看随后与原模型、打乱标签组的统一损失比较。
>
> <details><summary>Ran 4 commands</summary>
>
> - Ran ``python - <<'PY'
> from pathlib import Path
> r=Path('/data/250010109/Research_System');p=r/'Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P2_parent_router_supervision_repair/protocol.md'
> s=p.read_text();s+='\nReplacement submission receipt: reserved single-H100 job `pt-diap9xc9` RUNNING from 2026-09-06 10:44:34 UTC; fresh worker output `runs/reserved-20260906-p2-v2/full`. Original-path replay, prefix invariance and repaired matched-shape cache checks passed before formal training. The worker holds an immutable `protocol_snapshot.md` of the approved pre-run scientific body; live receipts do not alter the hashed snapshot.\n';p.write_text(s)
> PY``
> - Ran `python - <<'PY'
> from pathlib import Path
> import json
> p=Path('/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair/runs/reserved-20260906-p2-v2')
> print((p/'full.log').read_text().replace('\x00','')[-2200:]);m=json.loads((p/'full/metadata.json').read_text());print(m['status'],m.get('error'))
> PY`
> - Ran `cat .agents/skills/problem-anchor-writer/SKILL.md | head -100; git status --short`
> - Ran `python - <<'PY'
> from pathlib import Path
> import json
> p=Path('/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair/runs/reserved-20260906-p2-v2');print((p/'full.log').read_text().replace('\x00','')[-1700:]);m=json.loads((p/'full/metadata.json').read_text());print(m['status'],m.get('error'))
> PY`
>
> </details>
>
> 四个粗路由训练条件均已完成，正在完成最后几组统一评估。两个种子的修复组答案损失目前都降到了约 0.804；接下来会计算配对区间，并核验它们是否同时优于打乱标签对照、是否通过不重叠样本检查。
>
> <details><summary>Ran a command</summary>
>
> - Ran `python /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair/analyze.py --run /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair/runs/reserved-20260906-p2-v2/full --output /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair/runs/reserved-20260906-p2-v2/analysis`
>
> </details>
>
> Viewed 2 images
>
> <details><summary>Ran a command</summary>
>
> - Ran `python - <<'PY'
> import subprocess,json
> from pathlib import Path
> c='/data/250010109/MoE_Router/experiments/20260730_h768_4layer_switch_5090_smoke/scripts/sco_acp_compat.sh';m=json.loads(subprocess.check_output(['bash',c,'jobs','describe','--workspace-name=share-space','-o','json','pt-diap9xc9'],text=True));print({k:m.get(k) for k in ['name','state','start_time']})
> p=Path('/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair/runs/reserved-20260906-p2-v2/full/metadata.json');m=json.loads(p.read_text());print(json.dumps({k:v for k,v in m.items() if k not in ['replay','source_sha256']},indent=2));print('Replay max error',max(v['nll_abs_error'] for v in m['replay'].values()))
> PY`
>
> </details>
>
> 正式判定已通过：两个种子在完整样本和不重叠样本上，修复组都可靠优于原在线模型及打乱标签对照，八个必要比较的区间下界全部大于零。平均答案损失从 **0.836757 降到 0.804183**。我正在整理最终证据记录，并核对参数冻结、训练次数和图表，随后给出完整四段式分析。
>
> <details><summary>Ran 4 commands</summary>
>
> - Ran ``cat > /tmp/record_p2.py <<'PY'
> from pathlib import Path
> import json,csv,hashlib,shutil
> import numpy as np
> import torch
> root=Path('/data/250010109/Research_System');w=Path('/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair');run=w/'runs/reserved-20260906-p2-v2/full';a=run.parent/'analysis';d=root/'Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P2_parent_router_supervision_repair'
> x=json.loads((a/'results.json').read_text());m=json.loads((run/'metadata.json').read_text())
> def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
> assert m['status']=='FULL_RUN_COMPLETE'
> for p,h in m['source_sha256'].items():assert digest(Path(p))==h,p
> for seed in [17,29]:
>  for arm in ['R','S']:
>   p=run/f'seed{seed}/{arm}';audit=json.loads((p/'training_audit.json').read_text());steps=json.loads((p/'updates.json').read_text());ckpt=torch.load(p/'final.pt',map_location='cpu',weights_only=False)
>   assert len(steps)==128 and [r['update'] for r in steps]==list(range(1,129))
>   assert audit['updates']==ckpt['updates']==128 and audit['seen_tokens']==ckpt['seen_tokens']==911644
>   assert sum(t.numel() for t in ckpt['parent'].values())==3075
>   assert all(torch.isfinite(t).all() for t in ckpt['parent'].values())
>  for pop in ['full','disjoint']:
>   z={r['condition']:r['nll'] for r in x['conditions'] if r['seed']==seed and r['population']==pop}
>   for c in [r for r in x['contrasts'] if r['seed']==seed and r['population']==pop]:assert abs(z[c['left']]-z[c['right']]-c['delta'])<1e-12
> assert all(c['ci_low']>0 for c in x['contrasts']) and len(x['contrasts'])==8
> for sub in ['tables','figures']:(d/sub).mkdir(exist_ok=True)
> for p in a.glob('*.csv'):shutil.copy2(p,d/'tables'/p.name)
> for p in a.glob('*.png'):shutil.copy2(p,d/'figures'/p.name)
> shutil.copy2(a/'results.json',d/'tables/results.json');shutil.copy2(run/'metadata.json',d/'tables/execution_metadata.json')
> training=[];history=[]
> for seed in [17,29]:
>  for arm in ['R','S']:
>   training.append({'seed':seed,'condition':arm,**m['seeds'][str(seed)]['training'][arm]})
>   for item in json.loads((run/f'seed{seed}/{arm}/history.json').read_text()):history.append({'seed':seed,'condition':arm,**item})
> (d/'tables/training_audit.json').write_text(json.dumps(training,indent=2)+'\n');(d/'tables/classification_history.json').write_text(json.dumps(history,indent=2)+'\n')
> manifest=[]
> for p in list(run.glob('seed*/*.npz'))+list(run.glob('seed*/[RS]/final.pt'))+list(run.glob('seed*/[RS]/updates.json'))+[run/'disjoint_mask.npy',run/'shuffle_permutation.npy',w/'protocol_snapshot.md',w/'run_experiment.py',w/'analyze.py',w/'core.py']:
>  manifest.append({'path':str(p),'sha256':digest(p),'bytes':p.stat().st_size,'complete':True,'role':'eligible source or producer'})
> (d/'tables/artifact_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
> means={arm:np.mean([r['nll'] for r in x['conditions'] if r['population']=='full' and r['condition']==arm]) for arm in ['O','R','S','B','C']}
> table='\n'.join(f"| {arm} | {means[arm]:.9f} |" for arm in means)
> cs='\n'.join(f"| {r['seed']} | {r['population']} | {r['left']} − {r['right']} | {r['delta']:.9f} | [{r['ci_low']:.9f}, {r['ci_high']:.9f}] |" for r in x['contrasts'])
> allrows='\n'.join(f"| {r['seed']} | {r['population']} | {r['condition']} | {r['nll']:.9f} | {100*r['parent_agreement']:.3f}% |" for r in x['conditions'])
> aux='\n'.join(f"| {r['seed']} | {r['population']} | {r['left']} − {r['right']} | {r['delta']:.9f} | [{r['ci_low']:.9f}, {r['ci_high']:.9f}] |" for r in x['auxiliary'])
> anchor='../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_05_gmm_pseudolabel_oracle_gap_anchor.md'
> (d/'summary.md').write_text(f'''# Summary: E14-P2 parent-only supervision restores online task performance
>
> Primary Anchor: [handoff question](../../../../../../../daily_research_reports/0906/docs/{anchor}). [Frozen Protocol](../../../../../../../daily_research_reports/0906/docs/protocol.md) · [Detailed record](../../../../../../../daily_research_reports/0906/docs/detailed.md) · [Chinese four-part analysis](../../../../../../../daily_research_reports/0906/docs/summary_cn.md).
> Execution: COMPLETE / ELIGIBLE. Typed verdict: `ONLINE_PARENT_REPAIR_SUPPORTED`.
> Interpretation status: `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`; measured results and registered verdict are audited, researcher-owned knowledge wording remains pending.
>
> ## Result Snapshot
>
> Training only the existing 3,075-parameter parent classifier on original pseudo-parent labels lowers fully online answer NLL in both frozen expert checkpoints. Every required comparison passes: repaired routing outperforms original routing and frequency-matched shuffled supervision on both full evaluation and the record-disjoint subset, separately for both seeds. All eight paired 95% lower endpoints are positive.
>
> Mean full-evaluation NLL decreases from **0.836757276 to 0.804182618**, a reduction of **0.032574658 nats/answer token**. Only the coarse Router changes; all expert banks and the child Router remain fixed. This repairs an operational handoff failure in this workload, not evidence of universal semantic routing or unpolluted benchmark generalization.
>
> ## Decision-Bearing Setup
>
> O = original online routing; R = parent-only real-pseudo-label repair; S = identical parent-only training with shuffled labels; B = supplied pseudo parent plus original predicted child; C = supplied complete pseudo path. Teacher means the original pseudo assignment, not a gold Oracle. In O/R/S evaluation no teacher path is supplied. NLL is total reference-answer negative log probability divided by answer-token count; lower is better. It uses reference previous answer tokens, not free generation.
>
> Full evaluation has 512 records/30,442 answer tokens. The 384-record, 27,133-token disjoint subset removes all training-ID overlap and excludes GPQA and HumanEval; it is a six-source safeguard, not decontamination proof.
>
> | Condition | Mean full-evaluation NLL |
> |---|---:|
> {table}
>
> Source: [conditions](../../../../../../../daily_research_reports/0906/docs/tables/conditions.csv). Both external teacher references have slightly higher point-estimate loss than R. They are privileged references, not guaranteed lower-loss bounds. No equivalence claim or superiority over a separate gold-trained model follows.
>
> ## Verdict Basis
>
> | Seed | Population | Comparison | NLL reduction | Paired-record 95% interval |
> |---|---|---|---:|---|
> {cs}
>
> Source: [registered contrasts](../../../../../../../daily_research_reports/0906/docs/tables/contrasts.csv), [machine-readable result](../../../../../../../daily_research_reports/0906/docs/tables/results.json). The rule requires every lower endpoint above zero. Frozen analysis: 2,000 paired-record bootstrap draws, seed 20260906; no seed pooling, checkpoint selection, outlier removal or post-hoc threshold. Records are paired across conditions, not independent treatment samples.
>
> ![Online parent repair](../../../../../../../daily_research_reports/backup/2026/09/0906/figures/online_parent_repair.png)
> How to read: left panels compare five paths; right panels show both necessary improvements above zero for both seeds, including the record-disjoint subset.
>
> ## Readout Evidence And Claim Boundary
>
> Full-evaluation pseudo-parent agreement rises from 24.08% to 87.47% in seed 17 and from 31.66% to 86.53% in seed 29. Shuffled-supervision models reach only 38.54% and 34.58%. These are agreement with pseudo labels, not ground-truth semantic accuracy. The task-loss comparison, not agreement alone, establishes the registered success.
>
> ![Readout and task evidence](../../../../../../../daily_research_reports/backup/2026/09/0906/figures/parent_readout_and_task.png)
> How to read: real-label supervision raises development agreement and improves evaluation task loss; the shuffled control does not reproduce that combination. This descriptive plot is not an estimated causal relationship between accuracy and loss. Source: [classification history](../../../../../../../daily_research_reports/0906/docs/tables/classification_history.json) and [conditions](../../../../../../../daily_research_reports/0906/docs/tables/conditions.csv).
>
> The original large handoff failure cannot be used as evidence that final-layer labels necessarily mislead earlier routing: keeping those labels and the input hook fixed while supplying missing supervision suffices for a task-loss repair here. The labels remain full-sequence, privileged training targets; optimal teacher layer, fine semantics, free-generation accuracy, and generalization to clean public tasks remain untested. Class-count matching is at the example level; one fixed shuffled assignment is not a distribution over all possible null partitions.
>
> ## Next Decision
>
> Use the repaired checkpoints as the candidate fixed online baseline for subsequent teacher/readout diagnosis, subject to the researcher's knowledge confirmation. Completion criterion: preserve the verified checkpoint identities and audited loss boundary; do not start a third-step label change solely to explain the now-repaired original gap. No further experiment was launched.
> ''')
> (d/'detailed.md').write_text(f'''# Detailed: E14-P2 parent-only supervision repair
>
> [Primary Anchor](../../../../../../../daily_research_reports/0906/docs/{anchor}) · [Protocol](../../../../../../../daily_research_reports/0906/docs/protocol.md), revision `20260906-P2-v1` · [Summary](../../../../../../../daily_research_reports/0906/docs/summary.md).
> Execution COMPLETE; eligible matrix; verdict `ONLINE_PARENT_REPAIR_SUPPORTED`.
> Interpretation: `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`.
>
> ## 0. Quick Recap
>
> Question: does adding missing parent supervision restore online dispatch with fixed experts? Four parent-only training conditions (two label conditions × two source checkpoints) and ten full evaluations completed. All eight required full/disjoint original/control contrasts have positive 95% lower endpoints. Mean full NLL is 0.836757276 before and 0.804182618 after repair. No expert or child-Router update, teacher refit, new layer, probability attenuation, or free-generation test occurred.
>
> ## 1. Terminology / Definitions
>
> NLL: summed reference-answer negative log probability divided by valid answer-token count, nats/token, lower is better. Parent agreement: count of scored prediction positions whose executed parent equals original pseudo parent divided by scored token count; B/C are forced and therefore trivially 100%. Parent CE measures original classifier logits versus pseudo targets and may remain high in B/C even though executed paths agree perfectly. Do not confuse executed agreement with classifier quality.
>
> Online O/R/S: no forced parent or child provided to model forward; permitted causal states still contain reference previous answer tokens during likelihood evaluation. R changes the parent classifier only. S uses identical learning with shuffled sample-label assignments. B/C supply original pseudo paths and are not gold-trained Oracle models. A record-disjoint subset excludes matching training record IDs; it does not screen semantic near-duplicates or base-pretraining contamination.
>
> ## 2. Anchor Link And Decision Point
>
> P1 measured externally supplied parent correction and audited missing parent gradients in the benchmark hard-pseudo trainer. P2 intervenes on that supervision route rather than layer, teacher, architecture or expert responsibility. It adjudicates one local handoff repair; the historical E14 verdict for its original unmodified conditions is not retroactively changed.
>
> ## 3. Protocol Freeze, Conformance, And Deviations
>
> All A–G and implementation/smoke/full-run/analysis scopes were explicitly confirmed by the researcher. Worker `protocol_snapshot.md` preserves the approved scientific body. The live protocol contains append-only execution receipts; its draft-era prose is historical, superseded by the approval receipt.
>
> | Registered item | Actual | Status / eligibility |
> |---|---|---|
> | Only 3075 parent parameters trained | Four standalone parent fits; expert and child tensors exactly unchanged | PASS |
> | Two original checkpoints, labels, data | Exact original SHA-256 identities | PASS |
> | 128 updates, 4 passes per condition | All four: 128 updates, 911644 target exposures | PASS |
> | True/shuffled targets | One fixed train-example permutation, counts preserved; 36.0596% labels unchanged | PASS |
> | Last checkpoint, no tuning | Final update 128 in all cases; development only logged | PASS |
> | Full and record-disjoint evaluation | 512/30442 and 384/27133 records/tokens respectively | PASS |
> | Historical O/B/C replay | Both seeds, smoke and full, zero aggregate and per-example errors; paths exact | PASS |
> | Cache and causal input | Matched-shape computations exact; suffix-change hidden/logit max difference zero | PASS |
> | Supplied paths invariant to parent replacement | B/C small-sample losses/routes exact under both repaired parent types | PASS |
> | Eight conjunctive contrasts | All lower endpoints positive under fixed paired-record bootstrap | PASS |
> | Initial smoke failure | Incorrect unequal-shape cache guard stopped first job before formal training | EXCLUDED, engineering-only correction |
>
> The first job `pt-i5ukbgg1` failed because the strict cache check compared logits recomputed over 511 positions with logits from a 512-position calculation sliced afterwards. This violated the intended same-operation comparison. The correction recomputed full-shape logits before masking; no tolerance or scientific variable changed. Failed run `reserved-20260906-p2-v1` is excluded. Replacement fresh run `reserved-20260906-p2-v2` is the only eligible full matrix. No automatic retries, no post-hoc scientific amendment.
>
> The small disposable training checks use two updates on the first eight records per seed/condition; these eight smoke updates are separate from the 512 formal updates and their weights never initialize full training. Smoke can establish gradient reachability and invariants, not task performance.
>
> ## 4. Actual Setup And Training Stages
>
> This round has **one parent-only optimization stage per condition**, following offline cache preparation. It does not rerun the historical coarse/fine expert stages and does not convert the original single-stage expert training into a staged experiment.
>
> Base: Qwen3-0.6B-Base, bf16, frozen. Historical expert checkpoints are E14 `benchmark__HIER_GMM_HARD_R8__seed17/final.pt` and seed29 counterpart, final historical update 128. The existing parent linear weight and bias are cast from bf16 to float32 for optimization. A fresh AdamW optimizer is created for each condition. Final parent tensors are cast to bf16 and inserted into the original frozen model for deployment. No newly initialized classifier parameters replace the original starting values.
>
> Trainable: parent weight 3×1024 and bias 3, total 3075. Frozen: base, output head, shared rank-8 expert, three rank-8 coarse experts, eight rank-8 fine experts, child Router and all balance buffers. Route input remains zero-indexed block 14 pre-attention state. Experts remain in that block's down projection. All expert coefficients remain one.
>
> Data: original train 4096 records, 3434 unique IDs, 227911 answer-prediction positions; development 512 records/28576 target positions; full evaluation 512 records/30442 target positions. Each complete training run exposes 911644 target positions over four passes. Sampling uses the unchanged historical source-balanced ordering per source seed and epoch. Teacher: original frozen final-layer whole-sequence means, train-fitted projected hierarchical Gaussian-mixture assignments; no fitting or access to evaluation targets for parameter optimization.
>
> Targets: per-example pseudo parent expanded only at positions predicting nonmasked answer targets. Shuffled labels use NumPy generator seed 20260906, one permutation across all 4096 training records, reused for both checkpoint seeds. Example label counts are [1693,1431,972]; unchanged fraction is 0.360595703125. Counts are not constrained at the answer-token-weighted level because sample lengths differ. The null therefore controls example class frequencies under the same microbatch objective, not every possible token-prior adjustment.
>
> Objective: mean parent cross entropy within each eight-example microbatch, divided by accumulation 16. No language-model loss, child CE or balancing term is optimized. Batch 8 × accumulation 16 gives effective batch 128; 32 updates per pass, four passes, 128 updates. AdamW lr 5e-4, betas (0.9,0.999), eps 1e-8, weight decay .01; five-update warmup then historical cosine decay to zero, gradient norm clip 1.0. Save 0/32/64/96/128 and select final 128 without development selection. Each training stream has 128 finite update rows; nonzero finite parent gradients and actual parent tensor changes are verified. [Training audit](../../../../../../../daily_research_reports/0906/docs/tables/training_audit.json).
>
> Cache preparation reads causal block states from each original checkpoint and preserves bf16 values at answer-prediction positions; row offsets preserve ragged sample boundaries. This is frozen feature extraction, not network training. Float32 cache/direct checks are shape-matched and within 1e-5; actual values are exact. Parent updates cannot affect the pre-adapter block input. All frozen adapter tensors are checked before/after and restored to original after evaluation; the separate parent optimizer has no base/child/expert parameter references.
>
> ## 5. Metrics And Registered Decision Rules
>
> Token-weighted NLL is reduced in float64. Primary comparisons: O−R (repair) and S−R (label-specific advantage), each on full and disjoint populations, separately for two seeds. Positive means repair is better. Pass requires all eight percentile 95% lower endpoints positive; non-support requires the same necessary clause to have nonpositive upper endpoints in both seeds; otherwise Insufficient. Finite/missing/hash/freeze failures invalidate or leave incomplete, rather than producing scientific failure.
>
> Bootstrap uses 2000 paired-record draws, NumPy default generator seed 20260906; separate draws for full/disjoint populations and same indices across compared conditions/seeds within each population. Unit of independence is record, not token or model condition. Both populations use their own token denominator on each resample. Mean seed loss is descriptive, not a population-of-training-seeds estimate. This is a conjunction of required evidence, not selection among multiple favorable tests. No exclusions beyond the predeclared record-ID subset and failed smoke.
>
> Recovery fraction is (O−R)/(O−B), with no clipping. Values exceed one because R has lower point-estimate loss than B, not because of an impossible probability or proof of gold-Oracle superiority. Residual R−B/R−C intervals are auxiliary descriptive evidence. [Recovery](../../../../../../../daily_research_reports/0906/docs/tables/recovery.csv), [auxiliary comparisons](../../../../../../../daily_research_reports/0906/docs/tables/auxiliary.csv).
>
> ## 6. Evidence Lineage
>
> | Claim | Raw artifact | Computation | Registered criterion | Evidence / boundary |
> |---|---|---|---|---|
> | Online parent repair helps | Per-seed O/R.npz | Paired loss differences / valid token totals; bootstrap | Full and disjoint lower endpoints positive both seeds | Registered support, conditional on these checkpoints |
> | Real association beats shuffled supervision | S/R.npz | Same paired computation | Same four positive endpoints | One fixed example-permutation control, not universal semantic proof |
> | Parent learns teacher mapping | Classification histories, evaluated parent counts | Token agreement and CE | Descriptive only | Pseudo-label agreement, not task gain by itself |
> | No unrelated parameter changes | Original tensors and per-seed guards | Exact equality outside parent, fresh optimizer membership | All frozen guards pass | Parent-only intervention |
> | Historical identity | Original P1 arrays and O/B/C replay | Exact paths and losses | Loss tolerance 1e-4, actual error zero | Excludes evaluator drift explanation |
>
> ## 7. Main Results
>
> | Seed | Population | Condition | NLL | Executed parent agreement |
> |---|---|---|---:|---:|
> {allrows}
>
> [Full source table](../../../../../../../daily_research_reports/0906/docs/tables/conditions.csv).
>
> | Seed | Population | Required comparison | Reduction | 95% interval |
> |---|---|---|---:|---|
> {cs}
>
> | Seed | Population | Auxiliary residual | Difference | Descriptive 95% interval |
> |---|---|---|---:|---|
> {aux}
>
> All required comparisons are eligible. No null was discarded. S improves relative to O in seed 17 but worsens in seed 29, whereas R beats both in both seeds. R's point estimates are below B and C; the auxiliary intervals, especially seed29 R−C, must be consulted before asserting superiority. No separate task-only or gold-Oracle model was evaluated in this round. Per-source losses and condition-specific correct/wrong-parent strata are in [source and strata table](../../../../../../../daily_research_reports/0906/docs/tables/source_and_strata.csv); strata are selected by each condition's route and are descriptive, not a matched causal subgroup contrast.
>
> ## 8. Visualization Audit
>
> ![Registered online repair contrasts](../../../../../../../daily_research_reports/backup/2026/09/0906/figures/online_parent_repair.png)
> Question: does parent-only learning improve task loss beyond original and shuffled routing? Source: paired arrays through conditions/contrasts tables. Left x-axis: O/R/S/B/C; y: answer NLL in nats/token. Right x-axis: O−R/S−R; y: NLL reduction with 95% intervals. Blue/orange are seeds17/29; upper/lower rows are full/disjoint populations. All eight lower endpoints are positive. Both PNG panels are visually inspected; labels/units readable and intervals trace to tables. It cannot establish clean eight-task generalization or a gold-Oracle advantage.
>
> ![Readout evidence](../../../../../../../daily_research_reports/backup/2026/09/0906/figures/parent_readout_and_task.png)
> Question: did the parent learn the intended mapping, and is that accompanied by task improvement? Left x: optimizer updates, y: development true-pseudo-parent agreement; solid R versus dashed S. Right x: full-evaluation agreement, y: NLL reduction versus original for each condition. Sources: classification history and condition tables. Both real-label curves improve and both task deltas are positive. Rendered labels and scales inspected. No regression or accuracy-to-loss causal slope is fitted; development includes overlapping records and is monitoring only. No debug-run result is plotted.
>
> ## 9. Stage Evidence And Failure Decomposition
>
> Identity/cache: PASS; smoke: PASS after unequal-shape guard correction; four parent fits: PASS; ten full evaluations: PASS; fixed analysis: PASS. Original parent supervision absence is an implementation defect; P2 shows a narrow repair suffices to remove the original large online task-loss deterioration on this workload. It does not falsify all layer/context mismatch hypotheses. The offline labels remain imperfect/proxy labels, and training still sees privileged targets, while inference uses causal states.
>
> ## 10. Full Experiment Record
>
> Job `pt-diap9xc9` SUCCEEDED, single reserved H100 80GB worker `n6ls.iu.i40.1`; job start 2026-09-06 10:44:34 UTC, runner start 10:45:01 UTC. Runner elapsed **128.280 seconds** including checks, caches, smoke, training and evaluation, excluding scheduling and separate local analysis. Image: `registry.cn-sh-01.sensecore.cn/lepton-trainingjob/ngc-pytorch:25.06-cu12.9-py3.12-ubuntu24.04`. Runtime: Python 3.12.3, PyTorch 2.8.0a0+5228986c39.nv25.06, Transformers 4.53.3, NumPy 1.26.4. Local analysis: float64 NumPy reductions and matplotlib; its script hash is in the artifact manifest. Tests: 3 passed in the cloud; initial local missing-module RED followed by GREEN was recorded in task execution.
>
> Formal updates: 512 across four fits. Disposable smoke updates: 8 separately. Frozen references: six full evaluations; learned conditions: four full evaluations. All evaluation calls use batch 8. Prior failed job: `pt-i5ukbgg1`, excluded; no successful partial training from it was reused.
>
> ## 11. Interpretation
>
> Observed: correct sample-label supervision of only the parent layer outperforms both original and shuffled controls. AI interpretation: missing parent supervision is a sufficient practical explanation for the large handoff loss in these fixed models; the earlier experiment was not an adequate falsifier of final-layer semantic supervision itself. This does not prove that the label semantics are optimal or that better label prediction always improves tasks. In fact R's lower point-estimate task loss than forced labels illustrates that exact offline-label imitation is not the task objective.
>
> ## 12. Claim Boundary
>
> Can claim the registered parent-only repair succeeds in this internal answer-likelihood workload under fixed budget. Cannot claim clean public-task generalization, free-generation gains, universally semantic experts, best insertion layer, best teacher context, or successful staged expert training. Disjoint subset excludes two sources and only addresses exact record IDs. Only one null permutation was used. No prior historical gold/task-only comparison is promoted into a new paired result here.
>
> ## 13. One Next Decision
>
> Use the repaired checkpoints as the candidate fixed online baseline for subsequent teacher/readout diagnosis, subject to the researcher's knowledge confirmation. Completion criterion: preserve the verified checkpoint identities and audited loss boundary; do not start a third-step label change solely to explain the now-repaired original gap. No further experiment was launched.
>
> ## 14. Artifact Manifest
>
> [Manifest](../../../../../../../daily_research_reports/0906/docs/tables/artifact_manifest.json): raw evaluation arrays, four trained parent checkpoints, per-update logs, subset/permutation, frozen protocol and producer hashes. [Execution metadata](../../../../../../../daily_research_reports/0906/docs/tables/execution_metadata.json): data/pseudo/source identities, per-seed replay/causal/freeze/training guards and runtime. [Training audit](../../../../../../../daily_research_reports/0906/docs/tables/training_audit.json) and [classification history](../../../../../../../daily_research_reports/0906/docs/tables/classification_history.json) are curated extracts. Raw cached representations, checkpoints and logs remain on the worker; no publication, commit or push occurred.
>
> ## 15. Reproduction And Links
>
> Worker: `{w}`.
> Eligible run: `{run}`.
> Analysis: `{a}`.
> Run command: `RUN_STAMP=reserved-20260906-p2-v2 timeout 5400 bash <worker>/run_remote.sh`.
> Analysis command: `python <worker>/analyze.py --run <eligible-run> --output <analysis>`.
> Final parent checkpoints: `<eligible-run>/seed17/R/final.pt` and `seed29/R/final.pt` (S counterparts are controls). These contain parent tensors only: load the corresponding original E14 full adapter, then cast and replace only parent tensors with bf16 values. They are not standalone language-model checkpoints. Preserved source hashes and the original adapter path are required for reconstruction.
> ''')
> print('Records written and independent identity/training/arithmetic audits PASS')
> print(means)
> PY
> python /tmp/record_p2.py``
> - Ran `ls Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/*15_13_05*; tail -35 .agents/skills/problem-anchor-writer/SKILL.md; git diff -- AGENTS.md | head -65`
> - Ran ``cat > /tmp/close_p2.py <<'PY'
> from pathlib import Path
> import json,os
> r=Path('/data/250010109/Research_System');d=r/'Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P2_parent_router_supervision_repair';x=json.loads((d/'tables/results.json').read_text())
> (d/'summary_cn.md').write_text('''# 第二步实验：只补足粗路由监督，能否恢复在线收益？
>
> 执行与统计审核已完成。正式判定：**支持本次粗路由在线修复**。两种子、两种样本范围、两种必要对照，共八个比较全部通过预定标准。
>
> 认识表述为 AI 核验稿，等待研究者确认；不影响已完成的实验与统计判定。[英文结果](../../../../../../../daily_research_reports/0906/docs/summary.md) · [完整审核](../../../../../../../daily_research_reports/0906/docs/detailed.md) · [冻结协议](../../../../../../../daily_research_reports/0906/docs/protocol.md)。
>
> ## 1. 目的
> 验证只补足粗路由监督，能否把原来依赖外部给定路径的收益变成模型自己分发时的收益。
>
> ## 2. 假设
> 使用原伪标签训练粗路由，应降低完全在线的答案预测损失。
> 如果只是类别数量调整或训练题目重复造成的改善，就不应稳定优于同预算打乱标签对照，并通过不重叠记录检查。
>
> ## 3. 分析方法
> - **训练对象审计：**两个原检查点分别运行正确标签和打乱标签训练，共四次。每次只训练 3,075 个粗路由参数，底座、全部专家和细路由冻结。训练目标只有粗标签分类损失；原输入位置和伪标签不变。每次四遍原 4,096 条记录、128 次更新、911,644 个答案位置；小批量 8，累计 16 小批更新。使用 AdamW，学习率 0.0005，五步预热后余弦衰减，梯度裁剪 1，权重衰减 0.01。每组从原粗路由重新开始，优化器重新初始化，固定选第 128 步；这是一阶段粗路由补训，不是重跑粗细专家两阶段训练。
> - **任务比较：**评估原在线、修复在线、打乱标签在线、外部给定粗路径、外部给定完整伪路径五组。前三组评估时不提供教师路径。答案损失是参考答案词元的负对数概率之和除以词元数，单位为 nat/答案词元，越小越好；它不是自由生成准确率。
> - **资格与统计审核：**相同 512 条记录、30,442 个答案词元；另按原记录编号排除训练重叠，得到 384 条、27,133 个答案词元。每个种子分别进行 2,000 次配对记录重采样。原路径精确重放、因果前缀、缓存一致性和冻结检查均通过。首个作业的缓存检查实现失败已排除，修复检查形状后从原参数重新运行，判据未变。
>
> ## 4. 结论
>
> 1. **补足粗路由监督确实恢复了在线任务收益，八个必要比较全部通过。**
>
>    两个种子的完整评估平均答案损失如下：
>
>    | 路径 | 平均损失 |
>    |---|---:|
>    | 原在线 | 0.836757 |
>    | 修复后在线 | **0.804183** |
>    | 打乱标签训练后在线 | 0.839262 |
>    | 外部给定粗路径 | 0.806082 |
>    | 外部给定完整伪路径 | 0.805028 |
>
>    相对原在线模型，种子 17 的损失降低 **0.041751**，95% 区间为 **[0.035441, 0.048617]**；种子 29 降低 **0.023398**，区间为 **[0.019734, 0.027878]**。在不重叠记录上，两者仍降低 **0.037415** 和 **0.018620**。修复组相对打乱组的四个区间下界也都大于零。[完整比较表](../../../../../../../daily_research_reports/0906/docs/tables/contrasts.csv)。
>
>    ![粗路由修复的任务损失与配对区间](../../../../../../../daily_research_reports/backup/2026/09/0906/figures/online_parent_repair.png)
>
>    读图：左边越低越好；右边两项比较的区间都在零线上方，上下两行分别为完整样本和不重叠样本。图中 O 为原在线，R 为正确标签修复，S 为打乱对照，B 为给定粗路径，C 为给定完整伪路径。
>
>    修复模型的点估计略低于两个给定伪路径参考，因此相对粗路径参考的恢复比例可超过 100%；这不是超过了人工真值模型，也不说明给定伪路径是性能上界。这里只检验同一套冻结专家的路径与监督修复。
>
> 2. **“早期状态无法承接末层标签”不能再由原失败直接推出；当前输入至少能学到足以改善任务的粗分发。**
>
>    评估集粗伪标签一致率从 **24.08%／31.66%** 提升到 **87.47%／86.53%**；打乱组仅为 **38.54%／34.58%**。一致率表示执行路径与伪标签相同的答案预测位置比例，不是真实语义正确率。任务损失也同步改善，才使本轮通过。
>
>    ![粗路由学习与任务收益的区别](../../../../../../../daily_research_reports/backup/2026/09/0906/figures/parent_readout_and_task.png)
>
>    读图：左图实线为正确标签、虚线为打乱标签，纵轴是开发集伪标签一致率；右图分别显示评估一致率和任务损失改善，不能把两者当成同一个指标。
>
>    **认识纠正：**原八任务检查点的粗路由监督缺失是一个可修复的主要断点。这个结果不证明末层标签最优，也没有比较当层标签、因果前缀标签或其他读取位置。完整评估仍含训练重叠；不重叠子集排除了两个任务来源，也不等于严格去污染的公开基准。
>
>    **当前计划位置：第二步验证已完成。下一决策是将修复后的模型固定为后续诊断的在线基线。**第三步不应继续以“原来的大交接差距无法恢复”为前提；若要探索新标签，应相对这个已修复基线证明额外价值。未自动启动第三步或第四步。
> ''')
> p=d/'protocol.md';s=p.read_text();s+='\nCompletion receipt: replacement reserved job `pt-diap9xc9` SUCCEEDED. Four full parent fits each completed 128 updates and 911644 target exposures; ten full path evaluations complete; original O/B/C losses and routes replay exactly for both seeds. Registered analysis and rendered-figure audits are complete. Full runner elapsed 128.280 seconds. See [Summary](../../../../../../../daily_research_reports/0906/docs/summary.md), [Chinese four-part audit](../../../../../../../daily_research_reports/0906/docs/summary_cn.md), and [Detailed](../../../../../../../daily_research_reports/0906/docs/detailed.md). No post-result settings were changed.\n';p.write_text(s)
> f=r/'daily_research_reports/0906/focus_gmm_pseudolabel_handoff.md';s=f.read_text().replace('status: STEP2_APPROVED_EXECUTION_IN_PROGRESS','status: STEP2_COMPLETE_AWAITING_HUMAN_KNOWLEDGE_CONFIRMATION').replace('实验二（设计已确认，执行中）','实验二（执行与审核已完成）');s=s.replace('2. **当前位置：只补足粗路由监督的验证计划。**训练粗路由；专家和细路由冻结。读取位置暂不改变。','2. **当前位置：粗路由监督修复验证已完成并通过预定判据。**只训练了粗路由；专家、细路由、标签和读取位置均保持不变。')
> s=s.replace('审定“只补足粗路由监督”的候选设计；其结果将决定该修复能否成为下一轮诊断的固定在线基线。保留第一步人工知识表述待确认状态，不把“已经理解”扩写为研究者未亲自陈述的结果结论。','将本次修复检查点作为后续诊断的候选固定在线基线，确认其结果与不能声称的边界；第三步须以修复后的模型为比较起点。人工认识表述仍待研究者确认，不能把实验执行授权当成结果判断。')
> s+='''
>
> ## 第二步完成记录（AI 核验，不代填人工判断）
>
> 作业 `pt-diap9xc9` 已成功。四个正式训练条件各 128 次更新，十组完整评估完成。正式判定：支持粗路由在线修复；两种子在完整与不重叠记录上，对原在线与打乱标签对照的八个区间下界全部大于零。完整评估平均答案损失由 0.836757 降至 0.804183。专家、细路由、底座冻结，标签和读取位置未变；原路径精确重放，所有资格检查通过。首个作业的检查代码失败保留且排除。
>
> AI 解释：原来的大交接差距不应继续被当作“末层标签无法监督当前输入”的证据。修复只证实本内部任务上的粗路由监督有效；不证明标签最优、真实语义或干净公开基准收益。此处属于 `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`，研究者结果与认识表述仍待确认。
>
> - [第二步结果摘要](../../../../experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P2_parent_router_supervision_repair/summary.md)
> - [中文四段式审核](../../../../experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P2_parent_router_supervision_repair/summary_cn.md)
> - [完整实验账目](../../../../experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P2_parent_router_supervision_repair/detailed.md)
> ''';f.write_text(s)
> p=r/'PROJECTS.md';s=p.read_text();lines=s.splitlines()
> for i,line in enumerate(lines):
>  if line.startswith('| `A15.gmm_pseudolabel_oracle_gap`'):
>   parts=line.split('|');parts[-2]=' `CLAIMED`; P2 reserved H100 job `pt-diap9xc9` SUCCEEDED; `ONLINE_PARENT_REPAIR_SUPPORTED`, all 8 required intervals positive; parent-only repair mean NLL 0.836757→0.804183; four training runs and ten evaluations audited; human knowledge wording pending; next: retain repaired online baseline; [Result](../../../../experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P2_parent_router_supervision_repair/summary.md) ';lines[i]='|'.join(parts)
> p.write_text('\n'.join(lines)+'\n')
> # Add a bounded evidence receipt without promoting unconfirmed human judgment.
> p=r/'Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_05_gmm_pseudolabel_oracle_gap_anchor.md';s=p.read_text();link=os.path.relpath(d/'summary.md',p.parent)
> insert=f'''\n2026-09-06 local repair evidence (AI-audited wording, human knowledge confirmation pending): P1 identified absent parent supervision in the benchmark hard-pseudo branch and a large supplied-parent correction. In [P2](../../../../../../../daily_research_reports/0906/docs/{link}), training only its existing parent classifier for 128 updates, while preserving experts, child Router, teacher labels and input hook, reduced mean online answer NLL from 0.836757276 to 0.804182618. Both seeds beat original routing and a matched example-shuffled-label control on full and record-disjoint evaluation; all eight registered paired-record interval lower endpoints were positive (`ONLINE_PARENT_REPAIR_SUPPORTED`). Original-path replay and frozen-parameter guards passed. This narrows the earlier attribution: the original handoff gap is not evidence of causal-state inaccessibility alone, because a missing-supervision repair suffices in this workload. It does not establish teacher optimality, clean benchmark generalization, or superiority to the separately trained gold Oracle. Historical E14's registered verdict remains about its original conditions.\n\n'''
> s=s.replace('## 8. Claim Boundary And Next Decision',insert+'## 8. Claim Boundary And Next Decision')
> old='The one proposed next decision, pending the researcher\'s confirmation, is to hold the hard-pseudo expert bank fixed and test a prefix-conditioned teacher-to-Router handoff with both forced-correct-pseudo and forced-wrong-pseudo interventions. Continue this route only if both seeds reduce the `0.031729` deployed-versus-forced gap, move final NLL toward task-only or Oracle, and increase selective expert utility.'
> new='The current proposed next decision, pending researcher knowledge confirmation after P2, is to retain the repaired parent checkpoints as the fixed online baseline for subsequent teacher/readout diagnosis. Any later prefix- or layer-conditioned label comparison must demonstrate added value relative to that repaired baseline, not the obsolete unsupervised-parent deployment failure. P2 does not authorize a new teacher or expert-training run.'
> assert old in s;s=s.replace(old,new);p.write_text(s)
> print('Chinese audit, Focus, registry and bounded Anchor evidence updated')
> PY
> python /tmp/close_p2.py``
> - Ran `python - <<'PY'
> from pathlib import Path
> import re,json
> r=Path('/data/250010109/Research_System');d=r/'Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P2_parent_router_supervision_repair';f=r/'daily_research_reports/0906/focus_gmm_pseudolabel_handoff.md'
> s=f.read_text().replace('新增具体设计仍为 AI 建议。','第二步具体设计随后已明确确认并完成执行。').replace('第二步新增监督、打乱对照、数据资格检查和训练预算作为完整协议草案交由用户审阅。','第二步监督、打乱对照、数据资格检查和训练预算均已由用户确认，执行与分析现已完成。');f.write_text(s)
> files=list(d.glob('*.md'))+[f]
> for p in files:
>  for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
>   if not target.startswith(('http','#')):assert (p.parent/target).exists(),(p,target)
> assert len(re.findall(r'^## [1-4]\. ',(d/'summary_cn.md').read_text(),re.M))==4
> m=json.loads((d/'tables/artifact_manifest.json').read_text());assert len([i for i in m if i['path'].endswith('/final.pt')])==4
> assert len([i for i in m if i['path'].endswith('.npz')])==10
> x=json.loads((d/'tables/results.json').read_text());assert x['verdict']=='ONLINE_PARENT_REPAIR_SUPPORTED'
> print('PASS: references, 4-part report, 4 trained checkpoints, 10 full evaluation arrays, registered verdict')
> print('Auxiliary full residuals:',[a for a in x['auxiliary'] if a['population']=='full'])
> PY
> git diff --check`
>
> </details>
</details>

**本轮实验与审核已完成，正式判定：支持“只补足粗路由监督即可恢复在线收益”。**四个训练条件、十组完整评估均完成，八个必要统计比较全部通过。

完整文件：[中文四段式审核](../../../../experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P2_parent_router_supervision_repair/summary_cn.md) · [训练账目与证据](../../../../experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P2_parent_router_supervision_repair/detailed.md)。

### 1. 目的

验证补足粗路由监督后，模型能否自己完成分发，恢复原来依赖外部给定路径的任务收益。

### 2. 假设

使用原伪标签训练粗路由，应降低完全在线的答案预测损失。

如果改善只来自类别比例调整或训练题目重复，就不应同时通过打乱标签对照和不重叠记录检查。

### 3. 分析方法

- **只训练粗路由。**两个原检查点分别训练正确标签组与打乱标签组，共四次。每次仅更新 3,075 个粗路由参数；底座、全部专家、细路由、标签与读取位置保持不变。每次训练四遍原数据、128 次更新；小批量 8，累计 16 小批更新。使用粗标签分类损失，学习率 0.0005，五步预热后衰减，固定选择第 128 步。**这是单阶段粗路由补训，不是重跑粗细专家两阶段训练。**
- **比较五种路径。**原在线、修复后在线、打乱标签训练后在线，以及外部给定粗路径、完整伪路径两个参考。前三组评估时都不提供教师路径。
- **核验任务收益。**评估相同的 512 条记录，并单列与训练记录不重叠的 384 条。按记录进行 2,000 次配对重采样。原路径精确重放、参数冻结和因果输入检查均通过；首个作业的缓存检查实现失败已修正，其输出没有进入结果。

### 4. 结论

1. **粗路由补训恢复了在线任务收益，而且稳定优于打乱标签训练。**

   答案预测损失越低越好，两个种子的完整评估平均结果为：

   | 路径 | 平均损失 |
   |---|---:|
   | 原在线 | 0.836757 |
   | **修复后在线** | **0.804183** |
   | 打乱标签训练后在线 | 0.839262 |
   | 外部给定粗路径 | 0.806082 |
   | 外部给定完整伪路径 | 0.805028 |

   相对原在线模型，两个种子的损失分别降低：

   - 种子 17：**0.041751**，95% 区间 **[0.035441，0.048617]**。
   - 种子 29：**0.023398**，95% 区间 **[0.019734，0.027878]**。

   在不重叠记录上仍分别降低 **0.037415、0.018620**。两个种子在两种样本范围上也都可靠优于打乱组，八个必要比较的区间下界全部大于零。

   ![在线修复结果](../../../../../../../daily_research_reports/backup/2026/09/0906/figures/online_parent_repair.png)

   读图：左侧越低越好；右侧区间在零线上方表示修复有效。O 是原在线，R 是修复组，S 是打乱组，B/C 是外部供给路径参考。

   修复组的损失点估计略低于完整伪路径，但**不能据此声称稳定超越完整伪路径，更不能声称超过人工真值模型**；完整伪路径比较的区间仍跨零。

2. **原失败不能再直接支持“早期状态无法承接末层标签”的判断。**

   在标签和读取位置都没变的情况下，评估集粗伪标签一致率从 **24.08%／31.66%** 提升到 **87.47%／86.53%**；打乱组只有 **38.54%／34.58%**。这次不仅分类更准确，任务损失也同步改善。

   ![路由学习与任务收益](../../../../../../../daily_research_reports/backup/2026/09/0906/figures/parent_readout_and_task.png)

   读图：左侧实线表示正确标签监督，虚线表示打乱监督；右侧分别展示伪标签一致率与任务损失改善，两者不是同一个指标。

   **认知更新应是：粗路由监督缺失是这套模型中一个可修复的主要断点。**尚不能声称末层标签最优、真实语义分发成立，或公开基准泛化成功。不重叠子集也只覆盖六个任务来源。

   **当前位置：第二步验证已完成。下一决策是把修复模型固定为后续诊断的在线基线。**第三步若探索当层标签或其他读出方法，应相对这个已修复基线证明额外价值，而不能继续用原来未训练粗路由的大差距作为出发点。

> 我现在有些不理解，这个机制修复后，为什么能够得到性能提升，以及下一步我们要完成什么任务？最后根据 [0902 Router Selection - 0905 decision](chatgpt-conversation://6a982979-0634-83e8-8e0f-f4e1f8dcabbb) , 我们锚定要解决的问题是啥？我们完成的这两个实验给出了什么认识更新？我们在计划的哪一步？接下来要探究什么问题，怎么理解，需要锚定我的认知

<details><summary>2 previous messages</summary>

> 我会先对齐你引用的原对话和两次实验的结果记录，把“为什么修复有效”“原问题是什么”“下一步还缺什么证据”连起来讲清楚。本次先校准认识，不修改研究结论或启动新实验。
>
> <details><summary>Explored a file, ran a command</summary>
>
> <details><summary>Explored 2 files</summary>
>
> - Read `./Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P2_parent_router_supervision_repair/summary.md`
> - Read `./.agents/skills/research-sync-gate/SKILL.md`
>
> </details>
>
> Tool call
>
> Tool: read_thread
> Status: completed
>
> - Ran `cat Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P1_coarse_path_intervention/summary.md; tail -28 daily_research_reports/0906/focus_gmm_pseudolabel_handoff.md`
>
> </details>
</details>

**这次提升首先说明：原模型的专家已经学到了一些有用分工，但上线时粗路由没有学会正确调用它们。补上这部分训练，就能恢复收益。它还不等于“我们已经证明语义监督优于正常训练的普通路由”。**

我重新读取了[原对话](chatgpt-conversation://6a982979-0634-83e8-8e0f-f4e1f8dcabbb)。其中最后收敛的主线是：**离线得到的语义分组，怎样成为有用的在线分发。**“换成当层标签”“增加历史读出”都是候选手段，不是必须实现的研究目标。

以下是认识校准稿，标记为 `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`。

### 1. 目的

判断离线语义分组能否指导模型在只读取已有上下文时选择合适专家，并获得实际任务收益。

### 2. 假设

原先的候选解释是：末层整段标签与当前路由输入不匹配，导致在线分发失败。

现在需要更新为：**在当前八任务模型中，粗路由监督缺失是已经验证、可以修复的主要断点；层位和上下文不匹配尚未被这两次实验确认为主要原因。**

### 3. 分析方法

- **先理解收益从哪里来。**原专家训练时，伪标签直接指定粗细路径，专家据此接受答案预测训练。原在线评估却撤掉了指定路径，让没有训练好的粗路由决定粗组；粗组一旦选错，细路由只能在错误组里选择。修复训练让粗路由学会从当前状态预测原粗标签，因此更经常调用与训练责任相匹配的专家。**模型没有增加专家能力，改变的是已有能力如何被调用。**

- **第一实验验证“路径纠正是否有用”。**全部参数冻结，只在评估时供给粗路径，并让原细路由在正确粗组内重新选择。它检验的是：即使专家不再学习，仅改变分发能否改善答案预测。

- **第二实验验证“模型能否自己完成纠正”。**只训练粗路由，冻结底座、全部专家和细路由；每组四遍数据、128 次更新，小批量 8、累计 16 小批更新，学习率 0.0005，固定最后一步。训练目标只有粗标签分类损失。它是单阶段粗路由补训；评估时不再供给路径，并与同预算打乱标签训练比较。

### 4. 结论

1. **两个实验依次回答了“调用路径有问题”和“这个问题可以通过学习修复”。**

   第一实验中，供给粗路径恢复了两个种子 **98.24% 和 93.96%** 的原交接损失。同时，审计发现原粗路由没有梯度、保存的参数没有变化。

   ![第一步路径干预](../../../../../../../daily_research_reports/backup/2026/09/0906/figures/path_intervention.png)

   读图：左图从原在线路径 A 到供给粗路径 B 的下降，说明固定专家后，纠正粗分发本身就有用。

   **这里的机制解释是“训练责任与实际调用不一致”。**例如，某类样本主要训练了第二组专家，但在线粗路由把它送到第一组，第二组学到的能力就没有被调用。补训粗路由后，这种错配减少。

   这个解释有路径干预和训练审计支持，但不能扩大为“所有伪标签都正确”或“每次路由分类错误都会损害任务”。

2. **第二步已经打通了这套固定专家模型的在线交接，但还没有完成语义方法的净收益证明。**

   第二实验的平均答案损失从 **0.836757 降至 0.804183**；打乱标签训练为 **0.839262**。两个种子在完整样本和不重叠记录上，都可靠优于原在线与打乱对照，八个必要比较全部通过。

   ![第二步在线修复](../../../../../../../daily_research_reports/backup/2026/09/0906/figures/online_parent_repair.png)

   读图：修复组 R 的损失明显低于原在线 O 和打乱组 S；右侧区间均在零线上方，表示两种必要比较都通过。

   这带来三项认识更新：

   | 原来的认识或疑问 | 现在应怎样表述 |
   |---|---|
   | 聚类标签不行，所以在线路由失败 | **原失败混入了粗路由没有接受监督的问题，不能用它直接否定标签。** |
   | 当前状态可能读不出末层标签 | **当前状态至少能预测足以改善任务的粗分发；不需要先增加历史输入才能恢复这部分收益。** |
   | 恢复交接就证明语义方法成功 | **只证明了这套专家的调用可以修复，还需要比较正常、充分训练的强基线。** |

   尤其要分清本次的打乱对照：**我们打乱的是粗路由补训标签，专家库仍是原伪标签训练出来的那一套。**因此，它支持“正确的路由监督对应关系有用”，不能单独证明“语义分组训练专家优于随机分组训练专家”。

   **我们在计划中的位置是：**

   | 步骤 | 状态与意义 |
   |---|---|
   | ① 路径干预与架构审计 | 已完成：定位主要断点 |
   | ② 粗路由监督修复 | 已完成：模型自己分发也能恢复收益 |
   | ③ 标签、层位、上下文审计 | 尚未进行；是否值得启动，需要新的比较依据 |
   | ④ 专家与路由的功能训练验证 | 尚未完成，不能由本次补训代替 |

   **下一步不应机械地进入第三步、立即换标签。**原对话已经预留了这个分支：如果当前词元重训就能恢复收益，应先修复正常训练基线，而不是为了保留原直觉再添加读出机制。我们尚未比较历史摘要是否有额外收益，但它已不再是解释原大幅失败的必需条件。

   我上一轮“固定修复基线后继续标签审计”的表述不够完整。**现在更优先的候选验证问题是：在架构、数据和训练预算公平匹配后，现有伪标签路线是否比不使用语义标签、只根据任务损失训练的正常路由更有价值？**

   对应的行为应是：先审计已有普通路由基线的训练是否充分、预算是否匹配；能够公平比较的证据先统一评估，缺少的对照再设计补齐。不能把本次多出的粗路由补训预算忽略掉，也不能用旧的未训练粗路由作为方法优越性的主要对照。

   若公平比较仍有收益，才有理由研究标签如何进一步改善；若没有，就需要研究标签是否真正改善了专家分工，而不是继续追求标签预测准确率。

**你现在可以先锚定这句话：**

> 我们已经证明，原来的大幅在线退化主要可以通过补足粗路由监督修复；我们还没有证明，这种语义监督路线优于预算匹配、正常训练的普通路由。下一步要验证的是语义监督的额外价值，而不是继续解释一个已经修复的失败。

这仍是内部答案预测损失的结论，不代表无污染公开基准或自由生成能力已经提升。本次没有修改正式研究状态，也没有启动下一轮实验。

> 明白，也就是我们现在需要锚定基线模型，同时检查是否已经训完。已经训完的话，我们就可以把我们刚刚给到的的模型投入训练进行比较了，我的理解是否有问题？在这种情况下，我们的准确下一步是啥？
>
> 有一个问题，我现在暂时不知道：
>
> 1. 我们到底哪些是通过训练完成的；
> 2. 在之前训练完成的基础上，通过修改硬标签得到了什么结果。
>
> 我需要你把这些都列成一个表格，让我先了解我们到底做了什么，明白我接下来需要做什么，以及大致的计划是什么。

<details><summary>2 previous messages</summary>

> 你的方向基本正确，但“训练完成”还不等于“可以公平比较”。我会核对原基线是否完成、它与修复模型的训练预算有何差异，再用表格分清哪些结果来自训练、哪些只来自评估时改路径。
>
> <details><summary>Ran 2 commands</summary>
>
> - Ran `python - <<'PY'
> from pathlib import Path
> import json
> p=Path('/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/runs/full-20260903T042000Z')
> for name in ['HIER_TASK_R8','HIER_GMM_HARD_R8','HIER_GMM_R8','HIER_ORACLE_R8']:
>  for seed in [17,29]:
>   d=p/'conditions'/f'benchmark__{name}__seed{seed}'
>   h=json.loads((d/'train_history.json').read_text());print(name,seed,'checkpoint', (d/'final.pt').exists(),'updates',h[-1]['update'],'tokens',h[-1]['seen_target_tokens'],'stages',sorted(set(r['stage'] for r in h)))
> print((p/'analysis/02_nll.csv').read_text()[:5500])
> PY`
> - Ran `python - <<'PY'
> import csv,json
> from pathlib import Path
> p=Path('/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/runs/full-20260903T042000Z/analysis/02_nll.csv');rows=list(csv.DictReader(p.open()))
> for model in ['HIER_TASK_R8','HIER_GMM_R8','HIER_GMM_HARD_R8','HIER_ORACLE_R8']:
>  vals=[float(r['nll']) for r in rows if r['surface']=='benchmark' and r['model']==model and r['intervention']=='intact'];print(model,vals,sum(vals)/len(vals))
> p=Path('/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P2_parent_router_supervision_repair/tables/results.json');x=json.loads(p.read_text())
> print('repair',[r['nll'] for r in x['conditions'] if r['population']=='full' and r['condition']=='R'])
> PY`
>
> </details>
</details>

**你的理解需要调整一处：基线已经按原定预算训练完，我们刚刚的修复模型也已经训练完。下一步先检查能否公平比较，不是立即把修复模型再训练一次。**

我已核对：同架构普通路由基线的两个检查点都存在，均完成了原定 **128 次更新、四遍训练数据**。但“完成原定训练”不代表已经充分收敛，也不代表它与额外补训过粗路由的模型预算相同。

以下只梳理本次八任务分支，不混入另一条两阶段语料实验。

**一、哪些模型确实经过了训练？**

表中的“损失”指答案预测损失，越低越好；数值为两个种子的平均值。

| 模型 | 实际训练了什么 | 训练时谁决定专家路径 | 训练预算 | 当前结果与身份 |
|---|---|---|---|---|
| **同架构普通路由基线** | 专家和路由器，通过任务损失学习 | 路由器自己选择 | 128 次更新、四遍数据 | **已完成；损失 0.806323**。下一步主要比较对象 |
| 原来的学习式伪标签模型 | 专家和路由器；任务损失之外加入伪标签监督 | 路由器自己选择 | 128 次更新、四遍数据 | 已完成；损失 0.817358。它与下面的硬路径模型是不同检查点 |
| **原硬伪标签模型** | 共享、粗细专家，以及接受分类监督的细路由；粗路由没有有效梯度 | 离线伪标签直接指定粗细路径 | 128 次更新、四遍数据 | 已完成；撤掉指定路径后的在线损失 **0.836757** |
| **本轮修复模型** | 在原硬伪标签模型上，**只补训粗路由**；专家和细路由冻结 | 补训时只拟合标签；最终评估由路由器自己选择 | 在原训练之外，额外补训粗路由 128 次、四遍数据 | **已完成；在线损失 0.804183** |
| 本轮打乱标签对照 | 同样只补训粗路由，但打乱样本与粗标签的对应关系 | 最终评估由路由器自己选择 | 与修复组相同 | 已完成；在线损失 0.839262 |
| 原真值路径参考模型 | 按任务来源构造的指定路径训练专家 | 外部来源标签指定 | 128 次更新、四遍数据 | 已完成；指定路径损失 0.794920。不是可直接部署的普通路由基线 |

这里的关键区别是：

> **修复模型已经拥有新训练出来的粗路由参数；原硬伪标签模型与修复模型不再是完全相同的参数状态。**

另外，额外的 128 次粗路由更新，只涉及 3,075 个参数，**不能简单等同于额外训练整个专家模型 128 次**。公平预算需要同时考虑更新对象、数据暴露和计算成本。

**二、哪些结果只是改了评估路径，没有训练？**

你说的“修改硬标签”，在第一实验中更准确地说是：**评估时改由谁指定专家编号，没有重新生成标签，也没有修改模型参数。**

以下四行用的都是同一套原硬伪标签检查点：

| 第一实验的评估方式 | 评估时改变了什么 | 新训练参数？ | 平均损失 | 回答了什么 |
|---|---|---:|---:|---|
| 原在线路径 | 粗细路径都由原路由预测 | 否 | 0.836757 | 原部署状态有多差 |
| **给定粗路径，重新预测细路径** | 用原粗伪标签指定粗组；细路由在该组内选择 | 否 | **0.806082** | 绕过粗分发错误，能恢复大部分收益 |
| 给定完整伪路径 | 粗细专家都按原伪标签选择 | 否 | 0.805028 | 恢复原训练责任分配后的参考表现 |
| 给定粗路径、换错细专家 | 粗组正确，但枚举组内错误细专家 | 否 | 0.824251 | 同组细专家也不是随便换都一样 |

因此，两次实验的关系可以压缩成：

| 实验 | 我们实际做的事 | 获得的认识 |
|---|---|---|
| **第一实验：不训练** | 外部纠正专家选择 | **正确调用原专家，本身就能改善任务。** |
| **第二实验：训练粗路由** | 教模型自己预测粗组，再完全在线评估 | **这种调用改善可以通过补足粗路由监督实现。** |

打乱标签对照属于第二实验：它确实训练了一个新的粗路由。它没有重新用随机分组训练整套专家，因而不能单独证明“语义分组训练专家优于随机分组”。

来源：[第一实验记录](../../../../experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P1_coarse_path_intervention/summary.md)、[第二实验记录](../../../../experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P2_parent_router_supervision_repair/detailed.md)。

**三、准确的下一步是什么？**

**下一步应先完成“修复模型与同架构普通路由基线的公平比较审计”。**这包括已有结果的统一比较，以及确定是否需要补训练。

| 顺序 | 要做的事 | 是否需要训练 | 完成后能决定什么 |
|---|---|---|---|
| **1．核对基线训练合同** | 检查原基线的训练曲线、有效梯度、训练预算、路径系数和检查点选择 | **不需要** | 它是否是有效且训练充分的比较对象 |
| **2．统一比较已有检查点** | 用同一评估流程比较普通基线与修复模型；计算逐样本配对差异，保留不重叠记录子集 | **不需要** | 现有两个模型之间的差异是否可靠；明确预算不匹配的边界 |
| **3．补齐必要的公平对照** | 根据审计结果，冻结合理的预算匹配方案，再训练缺少的条件 | **可能需要，方案尚未确定** | 修复后的整条伪标签路线是否具有额外价值 |
| **4．据此选择后续研究** | 有净收益，再研究更好的标签或读出；无净收益，定位分组、专家训练或交接目标的问题 | 取决于结果 | 是否值得进入原计划第三步 |

当前已有数值是：

- 普通基线：**0.806323**
- 修复模型：**0.804183**
- 修复模型平均低约 **0.002140**

**这只是已有结果的描述性差异，尚不能称为公平预算下的方法优势。**我们还没有完成这两个模型的正式配对比较与预算审计。

所以，你接下来可以这样理解自己的任务：

> **两个模型都已经训练出来了。现在先确定比较是否有效，利用已有检查点完成能做的比较，再只补齐缺少的训练对照。我们要证明的是语义监督路线的额外价值，而不是再次证明补训比未训练好。**

目前仍在“第二步完成后的基线验证关口”，尚不需要立刻更换标签、扫描层位或启动联合训练。

> 我们需要审计我们的模型训练是否充分，我认为其实模型训练步数太少，并不充分。然后我认为需要加大训练量，但是又不是完整后训练的训练量，主要是把需要对比的模型都摆正，包括oracle-硬标签-学习型baseline-dense baseline-flat baseline. 以及讨论是否在第一阶段是否要加load balance trick. 为了我们的最小验证问题，你觉得我们需要训哪些模型进行对比。我实际上感觉之前训练的模型都有点混乱，不知道哪些冻结哪些是要验证啥，这次我们的规划必须把训练的模型提出来，并且给出架构的详细解析，确实以后我们再开启对比，开始训练。请先给出初步的计划规划和解析

<details><summary>3 previous messages</summary>

> 我会先审计已有训练曲线和各模型的实际更新对象，再提出统一的对比方案。重点会分清三件事：训练是否充分、粗细专家是否分阶段学习，以及语义标签是否带来额外收益；负载均衡也会单独说明它改变了哪个环节。
>
> <details><summary>Explored 2 files, ran a command</summary>
>
> <details><summary>Explored 4 files</summary>
>
> - Read `./.agents/skills/research-progress-core/SKILL.md`
> - Read `./.agents/skills/scholar-mode/SKILL.md`
> - Read `/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/registry.py`
> - Read `/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/training.py`
>
> </details>
>
> - Ran `python - <<'PY'
> import json
> from pathlib import Path
> p=Path('/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/runs/full-20260903T042000Z/conditions')
> for name in ['DENSE_R24','FLAT_TASK_R24','HIER_TASK_R8','HIER_GMM_HARD_R8','HIER_GMM_R8','HIER_ORACLE_R8']:
>  for seed in [17,29]:
>   h=json.loads((p/f'benchmark__{name}__seed{seed}/train_history.json').read_text());print(name,seed,[(r['update'],round(r['development_nll'],6),round(r.get('learning_rate',0),7)) for r in h if 'development_nll' in r])
> PY`
>
> </details>
>
> 旧曲线支持“需要审计训练充分性”，但还不能证明所有模型都只是步数不够：它们的学习率都在第 128 步降到了零，末段变平可能受这个设置影响；硬伪标签模型的旧开发曲线还混入了未训练粗路由的影响。新一轮应从相同起点重建模型，并明确区分“学习路径上的语义正则化”和“标签直接指定专家路径”这两种方法。
</details>

**我建议重新建立一套定义清楚、训练合同统一的比较，而不是继续给旧检查点零散追加训练。**但先纠正一点：**“128 步可能不充分”是合理怀疑，尚不是已证实的结论。**我们需要把训练不足、路由监督缺失和标签方法无效分开。

本轮的最小验证问题建议定为：

> **在相同架构、数据和训练预算下，语义标签监督能否让正常学习的在线路由获得额外的答案预测收益？**

“硬标签训练出来的专家能否成功交接给在线路由”作为紧邻的机制对照。以下是初步方案，尚未启动新训练。

**一、旧模型为什么不能直接拼成一张公平比较表？**

我重新检查了旧训练曲线，发现三个问题：

| 已核实情况 | 对当前判断的影响 |
|---|---|
| 所有旧模型的学习率都在第 128 步降到零 | 后期曲线变平不能独立证明训练充分 |
| 普通层级基线在第 96～128 步仍有开发损失下降 | 值得测试更长预算，但不能直接断言增加四倍训练一定有效 |
| 硬伪标签模型的开发评估使用了未训练好的粗路由 | 它的旧曲线不能直接代表专家本身是否学充分 |
| 修复模型额外补训了粗路由，其他模型没有对应追加过程 | 旧结果可以定位故障，尚不是完整的公平方法比较 |
| 原评估集有 128 条记录与训练集重叠 | 新正式比较应先重建按原始记录隔离的数据划分 |

例如，普通层级基线的开发损失在最后 32 步仍分别下降约 **0.000856、0.001224**，同时学习率逐渐归零。因此需要重新安排训练日程，并观察训练和开发曲线，而不是只检查是否存在最终检查点。[原训练实现](/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/training.py)

**二、建议训练哪些模型？**

先消除一个名称歧义：

- **普通学习型基线**：不使用语义标签，路由根据任务损失学习。
- **语义正则化学习模型**：路由自己决定执行路径，同时接受语义标签监督。
- **硬伪标签模型**：训练专家时直接由伪标签指定路径，另行监督路由器。

后两者不能都简称“语义模型”，因为它们改变了不同的训练环节。

**最小核心比较是前三组；连同你提出的架构与参考模型，完整矩阵建议七组。**

| 模型 | 训练时专家由谁选择 | 训练哪些对象 | 标签的作用 | 主要回答的问题 |
|---|---|---|---|---|
| **① 普通层级学习基线** | 粗细路由器 | 共享专家、粗细专家、粗细路由器 | 无语义标签 | 正常训练的层级路由能达到什么水平？ |
| **② 语义正则化层级模型** | 粗细路由器 | 与①完全相同 | **同时监督粗、细路由** | 在相同架构上，语义监督是否有额外收益？ |
| **③ 打乱监督层级模型** | 粗细路由器 | 与①②完全相同 | 打乱样本与标签的对应关系，保留类别数量 | 收益是否依赖正确对应关系，而非仅多一个分类损失？ |
| **④ 硬伪标签层级模型** | 离线粗细伪标签 | 共享、粗细专家；另行训练粗细路由 | 指定专家责任，并监督路由预测 | 先按标签形成专家分工，是否比在线共同学习更好？ |
| **⑤ 真值路径参考模型（Oracle）** | 外部任务来源标签 | 共享、粗细专家；本轮不要求训练部署路由 | 指定参考路径 | 已知任务来源分组能提供什么参考收益？ |
| **⑥ 稠密低秩基线（Dense）** | 无选择，始终执行同一个适配器 | 稠密低秩适配器 | 无 | 稀疏专家结构是否比普通适配有价值？ |
| **⑦ 平铺专家基线（Flat）** | 一个路由器直接选择八个专家之一 | 平铺专家和路由器 | 无 | 层级结构是否优于不分粗细的专家结构？ |

这里有两项边界：

**③应打乱完整的粗细标签对，保持父子关系合法。**它不再只是上次“固定专家、打乱粗路由补训标签”的对照，而是从头参与整段学习型模型训练。

**⑤目前的“真值”是已知任务来源，不是人工标注的所有真实语义，也不是不可超越的性能上界。**

七组中，①②③构成最直接的语义监督比较；④⑤解释路径与责任分配；⑥⑦提供架构参照。不要让七组中的每一组都承担“证明语义”的任务。

**三、架构具体怎么摆正？**

建议本轮保留已经使用过的底座和插入位置，避免同时改变太多变量：

- 底座：冻结的 Qwen3-0.6B-Base。
- 语言输出头：冻结。
- 专家插入点：零起始编号为 14 的块，其前馈网络的降维投影处。
- 路由输入：该块进入注意力计算之前的 **1,024 维状态**。
- 专家输入：前馈网络内部降维投影之前的 **3,072 维激活**。

**路由器读取的状态和专家实际处理的激活不是同一个对象。**本轮保持这个接口不变。

低秩专家可以理解为：把输入先映射到较小维度，再映射回输出维度，形成一个可训练的增量。

| 架构 | 模块组成 | 每个词元实际执行什么 | 专家低秩参数量，不含路由 |
|---|---|---|---:|
| 稠密 | 一个秩为 24 的适配器 | 一个适配器 | 98,304 |
| 平铺 | 八个秩为 24 的专家 | 选择一个专家 | 总计 786,432；每次激活 98,304 |
| 层级 | 一个共享专家、三个粗专家、八个细专家，每个秩为 8 | 共享＋一个粗专家＋一个细专家 | 总计 393,216；每次激活 98,304 |

层级模型的输出增量是：

> **共享专家贡献＋选中粗专家贡献＋选中细专家贡献。**

这些专家位于同一个网络块，并不是粗专家在前一层、细专家在后一层。

这套设置匹配了**每次激活的专家低秩参数量**，没有匹配总参数量，也没有自动匹配路由计算成本。正式报告必须分别列出，不能笼统称为“完全同规模”。

另外，**执行路径与专家系数也要分别登记**：

- 普通学习型模型需要保留能够向路由传递任务梯度的机制，例如现有的学习概率系数。
- 硬标签模型直接指定路径，专家系数固定为 1。
- 因此①②③之间可以干净地比较语义监督；④与①之间比较的是整套训练方法，不能把所有差异都归因于标签。

评估时再补一个统一“系数设为 1”的诊断，可以检查收益是否主要来自系数变化，但不能拿这个诊断代替各模型原生部署结果。

**四、“第一阶段”到底指什么？本轮先不要混入新的粗细生长实验**

我建议本轮先采用：

> **完整架构从一开始就存在，先完成统一的模型训练，再统一评估。**

具体冻结关系如下：

| 时期 | 学习型层级模型①②③ | 硬伪标签模型④ | 真值路径参考⑤ |
|---|---|---|---|
| 模型训练 | 粗细专家与粗细路由同时训练 | 粗细专家按指定路径训练；粗细路由同时接受分类监督 | 粗细专家按指定路径训练 |
| 统一评估 | 全部冻结，在线路由 | 全部冻结，分别评估指定路径与在线路径 | 全部冻结，评估指定路径 |

**这轮不建议先引入“只训练粗专家，再增加细专家”的真正两阶段生长。**因为当前要判断的是语义监督的净收益；同时改变专家出现时间，会再加入一个需要解释的变量。

如果以后验证粗细分阶段，必须单独明确：

- 第一阶段细专家是否根本不参与计算；
- 第二阶段粗路由是否冻结；
- 粗专家是否继续训练；
- 各基线如何匹配每阶段的活动容量和训练预算。

那是后续的训练组织问题，不能用“第一阶段、第二阶段”两个名称直接带过。

对硬伪标签模型，本轮最重要的修正是：**从训练开始就同时监督粗、细路由，不再漏掉粗路由，再事后补救。**最终仍然要检查在线交接；若还需要额外冻结专家补训路由，这部分必须另列预算。

**五、第一阶段要不要加负载均衡？**

负载均衡指让专家得到足够的训练样本，避免少数专家承担几乎全部计算。

**我的初步建议：先在训练充分性预审中检查它是否必要，再固定全套学习型模型共同使用的规则；不要只给语义模型加一个技巧。**

| 路径类型 | 负载均衡能改变什么 | 本轮建议 |
|---|---|---|
| 学习型路由 | 可以改变实际专家分配，因而影响专家获得的梯度 | 普通层级、语义层级、打乱层级和平铺基线采用一致的政策 |
| 硬指定路径 | 调整路由分数不会改变已经指定的专家编号 | 不把这种调整称为“改善了专家训练负载” |
| 稠密模型 | 没有专家选择 | 不适用 |

预审至少查看：各专家接收的有效词元数、连续未被使用的情况，以及实际梯度是否非零。

- 如果普通学习基线能正常使用专家，首轮可以不加额外均衡项，减少混杂。
- 如果它持续塌缩，就应先固定一个有效的常规均衡设置，再开展主比较。
- **不能拿明显塌缩、没有训练好的普通基线，来证明语义方法优越。**

本轮暂不同时研究“均衡损失”和“无梯度偏置技巧”谁更好。它们先作为保障基线有效的训练配置，而非新增研究主线。

**六、训练量怎么增加，才算可解释？**

我倾向于增加预算，但先修数据划分与训练日程。

| 项目 | 初步建议 |
|---|---|
| 模型起点 | 同一冻结底座，重新初始化适配器；不混用经历不同补训的旧检查点 |
| 数据 | 按原始记录先去重、再划分训练与验证；伪标签只在新训练集拟合 |
| 训练量 | 以 **512 次更新**作为候选主预算，约为旧专家训练更新次数的四倍 |
| 中间检查 | 记录 128、256、512 步的训练、验证、路由和专家更新情况 |
| 学习率 | 为新预算重新安排日程，不能照搬第 128 步归零的旧日程 |
| 最终预算 | 用预审的开发集证据确定；正式比较前冻结，不能看测试结果后继续加步数 |
| 随机性 | 首轮两个种子，先验证方向与训练稳定性 |
| 扩展条件 | 若仍有明确训练不足，按预先规定的公共扩展规则处理，不只延长有利条件 |

**512 步是候选预算，不是“训练充分”的证明。**在原来的小训练集上，它意味着更多次重复；如果训练损失继续下降而验证损失恶化，就应考虑过拟合或数据量，而不是继续加步数。

本轮应分别检查：

1. **有没有训练到：**应该更新的参数是否收到梯度、实际发生变化。
2. **有没有继续学：**训练目标是否仍明显改善。
3. **增加训练有没有价值：**开发集任务损失是否改善、模型之间的排序是否稳定。

对于硬标签模型，训练期间要同时记录指定路径与在线路径的开发损失，否则又会把“专家没学好”和“交接没完成”混在一起。

**我建议现在先确认的计划骨架是：七组模型、一个统一训练时期、先预审再冻结主预算、学习型模型共用负载均衡政策。**

其中唯一主比较是：

> **语义正则化层级模型，对普通层级模型和打乱监督层级模型，是否都有稳定的在线任务收益？**

其余模型负责说明收益来自哪里、参照水平在哪里。先把这张训练合同固定下来，再写正式协议与启动训练，旧实验保留为机制诊断证据。

> 我认为flat专家模型也要加上一个平铺专家的影响，是否使用秩为12 12的架构来训练？排除共享专家影响。或者是否有更好的对比方法？
> 请给出你认为这个第三步你认为可以存在的几个具体的阶段，然后我们一个阶段一个阶段进行攻克

<details><summary>4 previous messages</summary>

> 如果你说的“12＋12”是“共享专家秩 12＋每次选中的平铺专家秩 12”，它可以作为一种架构，但与我们层级模型中的共享秩 8 不一致。我会重点比较“共享 8＋平铺 16”和“共享 8＋粗 8＋细 8”，再把第三轮拆成有明确推进条件的几个阶段。
>
> <details><summary>Explored 3 files</summary>
>
> - Read `/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/models.py`
> - Read `./.agents/skills/research-progress-core/SKILL.md`
> - Read `./.agents/skills/research-document-explainer/SKILL.md`
>
> </details>
>
> Context compaction
>
> Source: automatic
> Status: completed
>
> <details><summary>Explored 2 files</summary>
>
> - Read `./.agents/skills/research-progress-core/SKILL.md`
> - Read `/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/models.py`
>
> </details>
</details>

**应该加入“带共享专家的平铺模型”。如果“12＋12”指共享专家秩 12、选中的平铺专家秩 12，我建议优先改成“共享 8＋平铺 16”，与现有“共享 8＋粗 8＋细 8”对照。**

这样可以固定共享部分的容量。不过要纠正一点：**这能控制共享专家的容量差异，仍不能单独证明层级组织有效**，因为专家总参数量、路由方式和输出权重也可能不同。

下面是第三步的建议拆分。这里的“阶段”是研究推进节点，**不代表先训练粗专家、再训练细专家的两阶段训练**。

**一、先把平铺对照摆正**

“秩”在这里表示一个低秩适配器的容量。共享专家对每个词元都参与计算；平铺专家由一个路由器直接选择；层级专家先选择粗专家，再从其下属细专家中选择一个。

根据[现有模型实现](/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/models.py)，建议先明确四种架构：

| 模型 | 每个词元使用哪些模块 | 专家库组成 | 主要回答什么 |
|---|---|---|---|
| 普通低秩适配模型（Dense） | 一个秩 24 适配器 | 1×24 | 专家分发是否比统一适配更有用？ |
| 无共享平铺模型（Flat） | 一个秩 24 专家 | 8×24 | 普通平铺分发能做到什么程度？ |
| **带共享平铺模型** | **共享 8＋选中平铺 16** | **1×8＋8×16** | 固定共享容量后，平铺结构能做到什么程度？ |
| 层级模型 | 共享 8＋选中粗 8＋选中细 8 | 1×8＋3×8＋8×8 | 粗细组织是否有额外价值？ |

四者每个词元配置的活动秩都是 24，**但总参数量不相等，也不能直接称为计算量完全相等**。

因此：

- **12＋12先后置。**它与层级模型比较时，同时改变了共享容量和分发容量，更适合以后研究“容量怎么分配”。
- “无共享平铺24”与“共享8＋平铺16”比较，回答的是**固定活动预算下，把部分容量分配给共享分支是否有利**，不是纯粹的“有无共享”效应。
- “共享8＋平铺16”与“共享8＋粗8＋细8”比较，控制了共享容量，检验的是**剩余容量采用平铺或层级组织的整体差异**。

如果后面确实需要单独判断“父子约束是否有用”，更严格的补充对照是：**保留相同共享、粗、细专家库和路由器，只取消“细专家必须属于选中粗专家”的限制。**它能匹配专家参数量，但只回答父子选择约束的作用，不代表全部层级机制。现在先不把它加入必跑矩阵。

**二、第三步分成四个阶段，逐个通过**

我们目前的位置是：**已经定位并修复旧模型的粗路由训练缺失；尚未完成训练充分、预算公平的语义方法比较。**所以第三步的核心仍然是：

> 在正常、充分且公平的训练条件下，语义监督是否比同架构的纯任务训练带来额外收益？

| 阶段 | 具体目的 | 要做的行为 | 推进条件 |
|---|---|---|---|
| **3.1 架构与训练合同审计** | 确认每个模型究竟训练什么，避免再次漏训 | 固定上表四种架构；列出路由输入、专家输入、输出系数、训练目标、可训练参数；核对粗细路由是否真的收到梯度 | 所有预期模块都有明确训练来源；参数和预算差异可以解释 |
| **3.2 训练充分性与负载预审** | 判断原来的短训练是否限制结果，以及是否需要均衡机制 | 在开发集上观察随训练词元增加的损失曲线；检查专家使用量、梯度和各专家实际接收的训练量；用小范围对照确定负载均衡政策 | 固定正式训练预算、学习率安排和均衡政策；不能仅因学习率降到零就宣布收敛 |
| **3.3 建立正常训练的架构基线** | 分清统一适配、平铺、共享和层级结构的表现 | 四种架构先都只用答案预测损失训练；统一数据、预算和评估规则；比较任务损失与训练曲线 | 得到可信的同架构学习基线；明确层级是否具有独立的架构优势 |
| **3.4 验证语义监督的增量价值** | 判断修复后是否存在真正的方法收益 | 在固定层级架构内比较纯任务训练、真实伪标签监督、打乱伪标签监督；再按需要加入硬伪路径和来源真值路径参照 | 根据对照结果决定继续改标签、研究交接，还是停止当前语义方法 |

这里有一个关键边界：**即使层级模型没有超过带共享平铺模型，也不自动否定语义监督。**语义监督是否有效，仍应由“同架构、有无语义监督”的对照回答；但此时不能声称层级结构本身是必要的。

**三、各阶段哪些对象训练，哪些冻结**

建议新一轮正式比较统一从同一个冻结基座出发，重新初始化适配器和路由器。旧模型作为历史诊断证据保留。

| 条件 | 训练专家？ | 训练路由器？ | 实际路径由谁决定？ |
|---|---|---|---|
| Dense | 是，训练单个适配器 | 没有路由器 | 所有词元使用同一适配器 |
| 三种纯任务路由基线 | 是 | 是，通过任务目标 | 在线路由器 |
| 学习型语义模型 | 是 | 是，任务目标＋语义监督 | 在线路由器 |
| 打乱标签对照 | 是 | 是，任务目标＋打乱后的监督 | 在线路由器 |
| 硬伪标签模型 | 是 | 若需要检验交接，则同步监督粗、细路由器 | 训练时由固定伪标签给定 |
| 来源真值路径参照（Oracle） | 是 | 强制路径下不需要学习路由器 | 数据来源标签给定 |

硬路径模型中，**路由器可以被监督训练，但不负责当时的实际分发**。训练后再切换到在线路由，是另一个评估条件，必须单独列出。

所有这些条件都冻结基座模型。建议先从训练开始就启用完整架构，避免同时引入“何时添加细专家”这个新变量。

**四、负载均衡先作为训练条件处理**

负载均衡指避免少数专家承担几乎全部词元。它不等于语义分工。

我的建议是：

- 在 **3.2** 检查是否发生明显负载集中，并观察它是否伴随专家训练不足。
- 正式比较前固定政策，尤其保证“纯任务／语义监督／打乱监督”三个同架构条件一致。
- 强制硬标签决定路径时，调整路由器分数不能改变实际负载；不要把这种操作算作有效均衡。
- 层级模型的细专家负载应结合父类使用量检查。当前每个父类下有 3、3、2 个子专家，不能直接要求全部细专家无条件等频。

**准确的下一步是先完成 3.1：冻结四种架构及其训练对象、输出系数和预算合同。**随后进入训练充分性预审，再确定正式训练量。12＋12和取消父子限制暂时作为有明确触发条件的补充对照，不一开始全部铺开。

> 现在我遇到了一点 token 困境。关于整个任务，我们还有哪几个步骤没有完成？请给出具体的任务执行安排，然后我让sol完成实验，将需要读取的对话给你，由你裁定。但是问题就在于，必须要把任务的细节给清楚，请构写一个具体的plan, 放进daily\_research\_reports/0906/plans中

<details><summary>6 previous messages</summary>

> 我会把剩余步骤、Sol 的执行边界、逐阶段验收条件和交回审核所需的证据写成一份可直接接手的计划，放到指定目录。先核对当前 Focus 和已完成实验，避免把建议当成已批准的训练方案。
>
> <details><summary>Ran 2 commands</summary>
>
> - Ran `cat .agents/skills/experiment-card-writer/SKILL.md .agents/skills/superpowers/SKILL.md 2>/dev/null; cat /root/.codex/plugins/cache/openai-curated-remote/superpowers/6.3.0/skills/writing-plans/SKILL.md; grep -n 'handoff\|A15\|0906' /root/.codex/memories/MEMORY.md | head -15; ./researchctl --help`
> - Ran `./researchctl context --help; cat daily_research_reports/0906/focus_gmm_pseudolabel_handoff.md; ls daily_research_reports/0906/plans; git status --short`
>
> </details>
>
> 我会使用 writing-plans 技能编写这份交接计划。核对后有一个关键点：旧 Focus 的“第三步”是交接仍失败时的诊断，而我们刚讨论的是“训练充分性与公平比较”的新推进安排；计划会明确区分两者，并把尚待冻结的训练细节列成 Sol 的首个交付，避免直接套用旧实验授权开跑。
>
> <details><summary>Explored 2 files, a search, ran a command</summary>
>
> - Ran `./researchctl context A15.gmm_pseudolabel_oracle_gap --task 'Write requested Sol execution handoff plan only; do not change scientific approval or launch training' --path daily_research_reports/0906/plans/sol_training_comparison_handoff_cn.md
> cat Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P2_parent_router_supervision_repair/summary.md
> ls /data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap
> cat .agents/skills/research-communication/SKILL.md`
>
> <details><summary>Explored 2 files, a search</summary>
>
> - Read `./.agents/skills/research-communication/references/handoff.md`
> - Searched for `lr|weight_decay|warmup|aux|batch|accum|lambda` in `training.py`
> - Read `./Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_05_gmm_pseudolabel_oracle_gap_anchor.md`
>
> </details>
>
> </details>
>
> 计划会安排四个执行阶段，再加一次独立审核：先固定架构与数据，接着审计训练量，随后完成四种纯任务基线，最后验证语义监督的增量价值。当前任务登记工具解析 Focus 时出错；我会记录这个问题，本次只写你指定的计划文件，不改 Focus、Anchor 或实验批准状态。
>
> <details><summary>Ran a command</summary>
>
> - Ran ````mkdir -p daily_research_reports/0906/plans
> cat > daily_research_reports/0906/plans/sol_training_comparison_handoff_cn.md <<'EOF'
> # 第三步：训练充分性与公平比较——Sol 执行交接计划
>
> > 执行者：Sol，逐项执行并勾选；可使用 `superpowers:executing-plans`，不必另开代理。审核者：用户将结果任务交回后，由原分析任务核对证据并提出裁定建议；研究认识与下一决策仍由用户确认。
>
> **Goal:** 建立训练过程正确、预算明确的基线，再判断同架构下语义监督是否提高在线答案预测表现。
>
> **Architecture:** 固定 Qwen3-0.6B-Base，在零基编号 block 14 的下投影处加入低秩适配器。先比较普通适配、无共享平铺、带共享平铺和层级结构；语义作用在固定层级结构内独立比较。
>
> **Tech Stack:** 既有 PyTorch 实验代码、冻结本地模型和数据快照、单张 H100 标准配额。
>
> **Spec:** 下列 Focus、Anchor 和 P1/P2 证据是现状依据。本文件是用户明确要求的中文执行交接计划，属于派生工作安排；**不是第二份 Anchor 或可执行 Protocol**。新增设计以 `PROPOSED` 标记，批准后必须进入唯一所属 `protocol.md`，本文件只跟踪任务与链接。
>
> 创建日期：2026-09-06。问题归属：`A15.gmm_pseudolabel_oracle_gap`。
>
> ## 0. 冷启动先读这里
>
> ### 已完成，不要重跑
>
> 1. **P1，冻结路径干预：**没有训练参数。固定旧专家，分别给定粗路径、完整伪路径及同父错误细路径；发现粗路径纠正恢复大部分旧部署差距。架构审计发现旧八任务硬伪路径分支的粗路由没有梯度。
> 2. **P2，只补粗路由监督：**专家、细路由、基座全部冻结，只训练原有 3,075 个粗路由参数。原标签与打乱标签两种监督、种子 17 和 29，各 128 次更新。正式判定 `ONLINE_PARENT_REPAIR_SUPPORTED`；平均在线答案损失由 0.836757276 降到 0.804182618。完整样本与记录不重叠子集的八个必要比较均通过。
> 3. 上述数字证明旧监督缺失可修复，不证明末层教师最优、不证明语义方法胜过充分训练的同架构基线，也不证明公开基准泛化。
>
> ### 剩余任务与编号
>
> | 本轮阶段 | 状态 | 最小交付 | 后继 |
> |---|---|---|---|
> | 3.1 架构、数据与训练合同 | 尚未完成 | 可审核的完整候选 Protocol 与训练对象表 | 确认新设计后实施 |
> | 3.2 训练充分性与负载预审 | 尚未运行 | 开发曲线、梯度与负载证据、正式预算建议 | 冻结正式配置 |
> | 3.3 四种纯任务基线 | 尚未运行 | 四模型×两种子、公平性审核 | 同架构语义比较 |
> | 3.4 语义增量与必要的硬路径参照 | 尚未运行 | 真实/打乱监督与任务基线；条件触发的硬路径分析 | 交回独立裁定 |
> | R 独立证据审核 | 尚未开始 | 协议符合性、四段式结果、唯一下一决策 | 用户确认认识 |
>
> **编号提醒：**旧 Focus 的第三步原本是“第二步仍失败时才诊断教师层位与读出”。P2 已修复主要断点，本次对话把“第三步”用作训练充分性与公平比较。不要暗改旧编号或声称新训练已获旧协议批准。旧第四步中的功能训练部分在此被拆细；教师换层、因果前缀、SAE、KV cache、随机降维、真正分阶段生长均不自动执行。
>
> ### 批准范围与工具状态
>
> 用户本次明确授权：写本计划，准备交给 Sol。此前标准配额偏好继续有效，无需重问配额；P1/P2 的执行授权不能扩展为本轮新增训练授权。Sol 收到用户明确执行指令后，记录它覆盖的实现、冒烟、预审或正式训练范围，已明确批准的内容不要再问。
>
> 本次 `researchctl context` 尝试登记本计划路径时，因解析 Focus 文本产生 `OSError: [Errno 36] File name too long`，未成功登记。本文件只是用户指定的派生计划，未改科学状态。Sol 在修改共享实验或科学文件前，先核对工具当前状态；不能把登记失败写成已成功获得写权限，也不要为此擅改科学文本。若登记故障持续，单独报告具体阻塞与最小修复，不启动依赖它的共享变更。
>
> ## 1. 最小读取清单与代码入口
>
> 项目根：`/data/250010109/Research_System`。以下相对路径均以此为根。
>
> 1. `AGENTS.md`。
> 2. `daily_research_reports/0906/focus_gmm_pseudolabel_handoff.md`。
> 3. `Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_05_gmm_pseudolabel_oracle_gap_anchor.md`，重点看当前证据、边界和下一决策。
> 4. 在 `Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/` 下读取：
>    - `A15_13_E14_P1_coarse_path_intervention/summary.md`，需要重查才读 detailed。
>    - `A15_13_E14_P2_parent_router_supervision_repair/summary.md`、`detailed.md`；旧训练机制不明时再读 protocol。
> 5. 实验代码根：`/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap`。优先读 `models.py`、`training.py`、`registry.py`、`prepare_data.py`、`prepare_pseudo_labels.py`、`gmm_labels.py`、`checkpoint_manifest.py`，按依赖追踪，别复制整个仓库到上下文。
> 6. 旧运行根：上述代码根的 `runs/full-20260903T042000Z`。P2 运行根：`/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair/runs/reserved-20260906-p2-v2/full`。按 manifest 定位文件，不猜 checkpoint 名称。
> 7. 写正式协议用 `experiment-card-writer`，远程执行用 `remote-experiment-workflow` 和需要的 SCO 技能；技能只读取当前工作所需部分。
>
> 对话只用于还原用户意图，不替代证据。确需读取时，每个引用先调用 `read_thread`：
> - ChatGPT：`6a982979-0634-83e8-8e0f-f4e1f8dcabbb`，首次 `turnLimit=10`，必要时沿 cursor。
> - Codex：`01a06773-49c8-7e32-b504-00f3e5ddaad0`、`01a0679c-7ee2-71f3-91b5-f4df234571db`，原 host 为 `remote-ssh-codex-managed:mig`。
> - 本交接任务：`01a075b7-17c2-7202-8027-48d0f1aac1e8`，以当前工具解析的 host 为准。
> 不要求默认把四段长对话全部装入上下文；上述 canonical 证据够用就停止。
>
> ## 2. 模型清单、变量与训练对象
>
> ### 架构合同（PROPOSED）
>
> 共享专家：所有词元都用。平铺专家：直接从八个专家中选一个。层级专家：先从三个粗专家中选一个，再从其所属细专家中选一个，子专家数为 3、3、2。
>
> | 本文简称 | 结构 | 专家适配参数，不含路由器 | 每词元活动秩 | 要回答的问题 |
> |---|---|---:|---:|---|
> | D：普通适配 | 单个 rank 24 | 98,304 | 24 | 统一适配的任务基线 |
> | F：无共享平铺 | 8 个 rank 24，选 1 | 786,432 | 24 | 普通分发的整体效果 |
> | SF：带共享平铺 | 共享 rank 8；8 个 rank 16，选 1 | 557,056 | 24 | 固定共享容量的平铺参照 |
> | H：层级 | 共享 rank 8；3 个粗 rank 8；8 个细 rank 8 | 393,216 | 24 | 粗细组织的整体效果 |
>
> 参数按下投影输入 3072、输出 1024，单个适配器参数 $r(3072+1024)$ 计算；Sol 必须从构造后的实际张量复核，并另列路由器参数、总可训练参数与实测吞吐。活动秩相同不等于总参数或实际计算量相同。
>
> SF 的 8+16 优先于 12+12。12+12 同时改变共享和分发容量，只能作为后置容量分配问题。H 与 SF 仍存在总参数、门控深度和系数差异，不能宣称纯隔离层级结构。必要时另拟“同专家库、取消父子选择限制”的单变量对照，未经触发不实现。
>
> ### 同架构语义条件（PROPOSED）
>
> | 条件 | 专家如何训练 | 粗细路由如何训练 | 训练时实际路径 | 正式主要评估路径 |
> |---|---|---|---|---|
> | H-task | 答案预测损失 | 任务损失通过选中专家系数回传 | 在线预测 | 在线 |
> | H-sem | 答案预测损失 | 任务损失＋粗、细伪标签分类损失 | 在线预测 | 在线 |
> | H-shuf | 答案预测损失 | 与 H-sem 相同，但监督标签打乱 | 在线预测 | 在线 |
> | H-hard（条件触发） | 答案预测损失 | 同步监督粗、细影子路由器 | 固定完整伪路径 | 强制路径与在线各报一行 |
> | H-oracle（条件触发） | 答案预测损失 | 强制路径不依赖学习路由器 | 固定数据来源真值路径 | 强制路径 |
>
> 影子路由器：接受分类监督，但不决定当次专家分发。Oracle 此处是来源类别特权参照，不是真实语义上帝标签，也不是数学性能上界。
>
> 所有条件冻结基座、词嵌入与语言头；共享、粗、细适配器从开始即全部参与训练。没有“先粗后细”的优化阶段。所有新正式模型从相同基座重新初始化，种子配对；P2 修复模型只作历史诊断参照，不能混入同预算的新模型排名。
>
> 当前代码中在线层级输出为 $S(x)+p_c C_c(x)+p_c p_{f|c}F_f(x)$；平铺为 $p_f E_f(x)$；SF 候选为 $S(x)+p_f E_f(x)$。H 的三个在线语义条件必须保持完全相同系数规则。硬路径使用单位系数时，同时改变了选路与缩放；不能把硬路径和在线模型全部差异归因为标签质量。需要归因时在同 checkpoint 上交叉评估索引和系数，记录合法父子组合。
>
> ## 3.1 冻结合同：先交一个可审核的具体对象
>
> **目的：**排除数据泄漏、遗漏梯度和模型定义不一致。
>
> - [ ] 核对旧 checkpoint 清单：训练数据、实际更新数、是否真的分阶段、trainable/frozen 参数。不得把八任务旧训练的 128 次更新四遍数据误写成两阶段；另一个 M2D2 分支不在本轮范围。
> - [ ] 在新工作目录实现前，先形成候选 Protocol；建议实验目录名 `A15_13_E14_P3_matched_training_semantic_comparison`，归入上述同一实验家族，先检查是否已存在、是否被其他任务占用。以一个实验的控制组组织，不为每个 baseline 新建 Focus。
> - [ ] 将本计划的四阶段映射到现有 Anchor 的具体问题。当前 Anchor 仍有旧综合裁决条款：新一轮若采用更窄的答案损失主判据，必须明确提出修订供确认，不能沿用旧通过标签而删去其必需指标。
> - [ ] 对四架构输出一个实际参数清单，明确 router 读取 block 14 的因果状态，专家读取该层下投影输入；准确记录 hook 的张量位置、维度、token 对齐和 padding/答案掩码。
> - [ ] 新数据按原始记录 ID 和规范化内容去重，再按来源分层分出训练、开发、测试，固定种子与 manifest。旧数据 `/data/250010109/datasets/a15_e14_benchmark/processed.pt` 有训练/评估重叠，不能直接作为“干净新比较”。检查原始来源快照是否足够；小来源样本不足时减少其数量并报告，不循环复制后分到不同集合。若不可构建八来源互斥拆分，先交具体数量和范围缩减建议，不能静默移除任务。
> - [ ] 只在训练集合拟合最终层整窗教师的 PCA64、三父组与 3/3/2 子组 GMM；冻结后应用到开发/测试。标签使用参考答案属于特权监督，必须声明；在线路由输入不得读取未来词元。暂不换教师层位。
> - [ ] H-shuf 按样本固定打乱完整“粗、细”标签对，保持父子合法与样本级类别频数，记录置乱 seed=20260906；不是每个 epoch 重打乱。相同标签个数不保证相同答案词元加权频数，须实报后者。
> - [ ] 在唯一 Protocol 写全粗分类损失、细分类损失及各权重。必须指定细分类是完整八类还是教师父组内条件分类、监督哪些预测位置、错误父路由时是否仍有有限损失；不可直接复用旧的仅细监督分支。候选优先使用粗三类＋教师父组内细类监督，H-sem/H-shuf 完全一致；权重从旧配置读取并列出准确值后审核，不凭聊天猜值。
>
> **本阶段出口：**完整候选 Protocol，状态 `DRAFT_NOT_EXECUTABLE`；明确数据数量、模型参数、损失公式和权重、初始化、预算候选、主判据及资源估算。用户确认设计和对应执行范围后再提升状态。若用户已在 Sol 任务中明确确认这些内容，记录原话与范围，不重复索取。
>
> ## 3.2 训练量与负载预审
>
> **目的：**判断长一点的训练是否改变比较，以及是否存在专家训练饥饿。不能仅凭旧运行结束推断训练充分。
>
> 以下为待写入 Protocol 的具体候选，不是当前已批准配置：
>
> - 种子 17 做开发预审，正式复核使用 17、29。微批量 8、梯度累积 16、序列上限 512；实际答案词元数逐更新记录。各条件共享数据顺序，不根据速度改变训练样本量。
> - 适配器学习率 2e-4、路由器 5e-4，AdamW、权重衰减 0.01，沿用旧代码可核验的起点；长训练采用总更新数 5% 的预热再余弦下降是新增候选，必须冻结后执行，不能误称完全沿用旧五步预热。
> - 先 D/F/SF/H-task 四组各 512 更新，在 128、256、384、512 保存开发曲线、训练损失、路由负载、专家梯度及参数改变量。四组固定最终 checkpoint，测试集保持封闭。
> - 若后段仍明显改善或排名未稳定，提出统一 1024 更新的预算对照；从相同初始状态按预定 1024 调度重跑，不能把学习率已降至零的 512 尾部随意续接。最大预审上限 1024；仍不足则如实标为预算内未稳定，不自动扩大预算。
> - Protocol 在预审前必须冻结“后段明显改善”的可计算规则与最小实际关注差异。先以开发曲线及配对区间支持预算建议，由用户确认最终预算；不能看测试结果定训练步数。不要把“不显著”当作等效或收敛证明。
> - 默认无负载均衡。仅当预审发现死专家或明显负载集中与欠训练并存时，增加 H-task 相同 seed/预算的均衡开关对照；复用既有按计数更新的路由偏置，先从代码核对实际默认步长和裁剪。开发表现未支持时维持关闭。它只是政策预选，不是正式两种子均衡有效性结论。
> - H-task/H-sem/H-shuf 必须使用同一冻结均衡政策。层级细负载同时报告父组内条件频数；父组 3/3/2 结构不能强求八个细专家天然等频。硬路径不能靠调整路由偏置改变给定标签的分发。
>
> **实现验收：**预期所有路由/专家梯度有限且实际更新；冻结基座权重哈希保持；hard 模式粗细影子路由均更新；SF 共享分支每个有效词元参与；不同条件答案掩码一致；在线因果输入通过前缀不变性检查；错父标签损失无 NaN。保留有针对性的回归测试与短冒烟输出，失败先修复并标明运行不合格。
>
> **出口：**开发证据支持的统一预算和均衡建议、预计 GPU 时间；冻结正式配置与判据。预审期间不得宣布最终方法优劣。若正式配置、数据和分析规则均未改变且事前允许，可复用 seed17 预审运行；否则正式运行重启并明确排除预审数据。
>
> ## 3.3 四种架构的纯任务训练
>
> **目的：**让架构基线本身具备可解释性；本阶段不证明语义标签有效。
>
> - [ ] D、F、SF、H-task，各 seed17、29，共八个正式条件；共享数据、预算、评估器及初始化规则。所有条件只优化任务损失，不接受语义分类监督。
> - [ ] 先通过单条件冒烟，再提交批准的完整范围。使用标准配额、单张 H100；具体资源类型、镜像、挂载由执行技能核验当前可用配置后写入运行回执。不要擅自扩成多卡或第三种子。
> - [ ] 每个模型报告训练/开发曲线、最终答案损失、来源分项、实际训练词元、总参数、活动参数估算与实测时长。
> - [ ] 分别解释 F 对 D 的分发整体差异、SF 对 F 的共享容量分配差异、H 对 SF 的层级组织整体差异。后两者不是纯单变量结构因果结论。
>
> **出口：**八个合格 checkpoint、配对逐样本输出和架构对照表。H 即使不胜 SF，也不自动终止同架构语义问题；但不能再声称层级结构必要。是否将后续研究改到 SF，由用户决定，不按测试结果偷偷换主架构。
>
> ## 3.4 语义增量：核心四次训练，硬路径按问题触发
>
> **目的：**比较同架构有无语义监督，随后才分解标签/交接的残余限制。
>
> - [ ] 复用 3.3 合格 H-task；新训 H-sem、H-shuf 各两个种子，共四次训练。两者共享专家、路由初始化和数据顺序，只改变样本与标签的对应关系。
> - [ ] 不改变教师、架构、在线专家系数、预算或均衡政策。语义条件开发曲线若仍显示欠训练，报告本预算不足；不得只给语义组追加步数后与旧 baseline 作正式比较。
> - [ ] 候选主指标：总参考答案负对数概率除以总答案词元数，单位 nat/答案词元，越低越好；记收益为 baseline 损失减 treatment 损失。参考答案前缀评估不等于自由生成准确率。
> - [ ] 候选主规则：分别对 seed17、29，H-task−H-sem 与 H-shuf−H-sem 的样本配对 95% 区间下界均大于零，才支持此设置下真实伪标签监督的在线增量；每次重采样整条记录，重新以总损失/总词元计算，不平均不等长样本的均值冒充主指标。候选 2,000 次重采样，固定种子 20260906，保留来源分层；须在正式测试前写入 Protocol。
> - [ ] 任一必要比较区间跨零或种子不一致，判证据不足；若必要比较稳定反向，报告具体不支持项。执行资格失败则无判定资格。上述为新候选规则，不覆盖旧 E14 A/B/C 裁决。
>
> **硬路径分支：**如果用户需要重新建立新预算下的特权参照，或 H-sem 未通过且下一决策需要区分标签价值与在线交接，则训练 H-hard 和 H-oracle，各两种子，额外四次训练。旧硬路径数字不能代替新数据新预算参照。
>
> H-hard 必须从头同时训练专家和粗细影子分类器；训练时强制原伪路径，评估时强制与在线各报一行。H-oracle 用同架构与预算的来源真值路径训练；来源到父/子组的映射须先固定并合法。三类不确定性分别回答：
> 1. 同一 H-hard 强制路径比在线好：新训练下仍有交接差距。
> 2. 硬伪路径明显落后来源真值路径：当前伪分区与来源特权参照存在差距，不直接证明应更换教师层。
> 3. H-sem 优于 H-task 和 H-shuf：支持监督增量；不能从标签一致率单独得出此结论。
>
> 如果需要声称专家功能分工，另注册同父错配/匹配删除干预；未经执行不能从任务损失或路由准确率推导专家不可互换。正式主矩阵为六模型×两种子=12 条训练；硬路径分支后为八模型×两种子=16 条。预审、失败和冒烟不计入正式条件，另立账目。
>
> ## 4. 文件与运行产物合同
>
> 本计划不放原始输出。Sol 在实验代码工作区建立独立新目录；不得覆盖 P1/P2 或旧 E14 checkpoint。新目录建议 `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p3_matched_training`，创建前检查冲突。
>
> | 产物 | 必须包含 | 所属位置 |
> |---|---|---|
> | protocol.md | 全条件、批准回执、损失公式、预算、判据、停止规则、数据定义 | 新实验 canonical 目录 |
> | run_manifest.json | 代码版本与本地差异、配置/数据/教师哈希、job ID、种子、状态、checkpoint 哈希 | 实验工作区；研究库只留审核所需清单 |
> | training_history | 更新数、数据遍数、实际词元、学习率、task/粗/细损失、负载、梯度、保存点 | 实验工作区 |
> | per_item_results | 记录 ID、来源、条件、seed、答案 NLL 总和、词元数、路径模式 | 实验工作区；提供明确产物映射 |
> | comparison tables | 每模型/种子结果、预定差值与区间、参数/预算/成本、资格状态 | canonical tables/ |
> | summary.md | 先实际阶段与比较，再目的、假设、分析方法、结论；保留负结果 | canonical 结果目录 |
> | detailed.md | 实际训练对象、完整运行账目、公式、偏差、失败、证据到判据的链条 | 同目录 |
> | figures/ | 开发损失对训练词元曲线；主要差值及区间；必要负载诊断 | 同目录，审核后嵌入 summary |
>
> 每个训练条件都必须单列：初始化来源、可训练/冻结模块、数据与遍数、微批/累积、实际更新数、损失与权重、学习率、checkpoint 选择规则、下一环节如何加载。中断恢复要保存优化器、调度器、数据顺序/RNG；缺失则标为新运行，不能假装无缝续训。
>
> ## 5. 逐阶段停止、交回与最终完成标志
>
> ### Sol 的交回节奏
>
> 1. **3.1 后：**只交候选协议路径、模型/训练对象表、确需确认的科学变化；不让用户重新读长对话。
> 2. **3.2 后：**交开发证据、建议训练量、是否启用均衡、正式运行预计资源。用户已批准的范围内自动继续，新增预算或科学变化才单列。
> 3. **3.3 后：**交八条件状态和架构边界；已批准 3.4 则继续，不因中间排名反复请求确认。
> 4. **3.4 后：**交 canonical summary/detailed、主表主图、运行清单、协议偏差；原分析任务读取这些证据后独立审核。
>
> 任何数据跨集合重叠、预期模块无梯度、checkpoint 不匹配、非有限损失、评估掩码变化均暂停受影响条件。先定位并保留失败回执，不删除失败来获得“全通过”。未完成的条件不得补预测值。资源耗尽则交已经合格的部分与准确恢复点，不宣称整个任务完成。
>
> ### 给原分析任务的最短审核输入
>
> 用户只需发送：**Sol 任务引用＋新实验绝对路径**。Sol 的最终回复须包含：
> - 批准版本与实际运行范围，完成/失败/未运行条件表。
> - summary.md、detailed.md、protocol.md、运行清单和主图的绝对路径。
> - 三个直接答案：预算内训练是否稳定；哪种架构更好及混杂；语义监督是否超过同架构任务与打乱对照。
> - 四段式审核：目的、假设、分析方法（不超过三项）、结论；每个结论带最小证据与不能声称边界。
> - 一个具体下一决策；结果解释在用户确认前标 `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`。
>
> 原分析任务应先对引用调用 read_thread，再查原件；检查统计定义、训练是否公平、污染和失败排除、图与主表一致性，不从 Sol 的文字结论直接盖章。
>
> ### 完成清单
>
> - [ ] 所有获批准必跑条件完成，未执行条件明确列出原因；可选分支不冒充必跑失败。
> - [ ] 数据、参数、梯度、运行配置和实际预算审核通过。
> - [ ] 预先规定的比较均给出真实数值、区间与 Pass/Fail/Insufficient 或资格失败结论。
> - [ ] 四段式说明可独立阅读；能区分旧修复、重新训练、固定模型路径干预三种不同证据。
> - [ ] 原分析任务完成独立核验；用户确认或纠正研究认识与下一决策后，才更新科学判断和延迟日报。
>
> ## 6. 可直接交给 Sol 的启动指令
>
> > 请读取 `/data/250010109/Research_System/daily_research_reports/0906/plans/sol_training_comparison_handoff_cn.md`，按 3.1→3.2→3.3→3.4 执行我明确批准的范围。先完成可审阅的候选 Protocol 和架构/训练对象表；识别已有批准与新增科学决策，不重复询问已确认事项。每阶段按计划提供证据与恢复点，保留失败记录。不得把 P1/P2 的旧授权当作本轮新训练批准，不重跑已完成实验，不覆盖旧模型，不自动加入 SAE、换层、KV 或分阶段生长。最终提供 canonical 结果文件和任务引用，供原分析任务独立审核。
> EOF
> python - <<'PY'
> from pathlib import Path
> p=Path('daily_research_reports/0906/plans/sol_training_comparison_handoff_cn.md')
> s=p.read_text()
> assert all(x in s for x in ['## 3.1','## 3.2','## 3.3','## 3.4','## 5.','DRAFT_NOT_EXECUTABLE'])
> assert s.count('```') % 2 == 0
> assert 'TBD' not in s and 'TODO' not in s
> print(f'UTF-8 / required phases / fence checks passed; {len(s.splitlines())} lines; {len(s)} characters')
> PY````
>
> </details>
</details>

已写入：[Sol 执行交接计划](../plans/sol_training_comparison_handoff_cn.md)。

**还剩四个执行阶段＋一次独立审核：**

1. 固定架构、数据、训练对象和正式协议。
2. 审计训练量是否足够、是否需要负载均衡。
3. 训练四种纯任务基线：普通适配、无共享平铺、共享平铺、层级。
4. 比较真实／打乱语义监督；按需要补硬伪路径和 Oracle。
5. 我根据原始证据审核结果与认识更新。

计划明确了模型配置、训练与冻结对象、预算候选、停止条件、产物路径和交回格式。**核心正式矩阵为 12 条训练；加入两个硬路径参照后为 16 条，预审另计。**

你可以直接把文件交给 Sol。完成后发给我 **Sol 任务引用＋结果目录**即可，不需要重新整理长对话。新增训练配置仍需在正式协议中冻结；本次没有启动实验。

> 请阅读 @0906 Sol 执行Router实验，确定是否按照要求完成了初步规划，需要给出设么进一步的实验指示进一步完善整个实验。请给出确定的第二步执行计划，然后新建一个文档，放入plans文件夹中

<details><summary>6 previous messages</summary>

> 我会先读取“0906 Sol 执行Router实验”的实际规划和产物，对照交接计划检查缺项，再把明确的第二步执行计划写入 plans 文件夹。
>
> <details><summary>Explored a file, ran 2 commands</summary>
>
> - Ran `cat .agents/skills/experiment-card-writer/SKILL.md | head -65; ls daily_research_reports/0906/plans; ./researchctl status`
>
> Tool call
>
> Tool: list_threads
> Status: completed
>
> <details><summary>Explored a file</summary>
>
> - Read `./Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P3_matched_training_semantic_comparison/protocol.md`
>
> </details>
>
> Tool call
>
> Tool: read_thread
> Status: completed
>
> - Ran `cat .agents/skills/experiment-card-writer/references/blockwise_protocol_audit.md .agents/skills/experiment-card-writer/references/protocol_self_containment_and_freeze.md`
>
> </details>
>
> Sol 已经写出相当完整的候选协议，但还不能直接进入长训练。我发现两个需要补实的执行细节：零初始化下，不能要求所有专家和路由器在两步内都更新；另外，新训练集已扩大到 39,576 条，512 次更新只覆盖约 1.66 遍，需要把“训练充分”的边界讲清楚。任务读取接口目前不可用，我会明确区分已核验的文件内容与尚未读到的对话授权。
>
> <details><summary>Ran 2 commands</summary>
>
> - Ran `find Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P3_matched_training_semantic_comparison -maxdepth 2 -type f; tail -65 daily_research_reports/0906/focus_gmm_pseudolabel_handoff.md; ./researchctl context A15.gmm_pseudolabel_oracle_gap --task 'Audit Sol initial P3 protocol and write second-step plan; no scientific approval changes' --path daily_research_reports/0906/plans/sol_p3_second_step_execution_plan_cn.md`
> - Ran `cat Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P3_matched_training_semantic_comparison/tables/training_object_contract.csv; cat Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P3_matched_training_semantic_comparison/tables/historical_e14_p1_p2_audit.csv; test -d /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p3_matched_training && ls /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p3_matched_training; ./researchctl release --help`
>
> </details>
>
> 我的审核结论是：**初步规划基本达标，正式执行前仍需补齐资格检查和预算核算。**第二步应限定为“修订合同、验证实现、完成四基线训练预审”，暂不直接铺开 12 条正式训练。我会把必须修改的条款、确定保留的配置、逐项验收和停止条件写清楚，并移除已被新版 AGENTS.md 取消的本地检查审批限制。
>
> <details><summary>Ran a command</summary>
>
> - Ran ``cat > daily_research_reports/0906/plans/sol_p3_second_step_execution_plan_cn.md <<'EOF'
> # Sol P3 第二步执行计划：合同补齐、实现验证与训练预审
>
> 日期：2026-09-06。问题：`A15.gmm_pseudolabel_oracle_gap`。
> 文档性质：用户要求的中文审核与派生执行安排，不替代唯一 Protocol，不自动批准远程作业或改写科研判断。
>
> ## 1. 本次审核结论与读取边界
>
> **初步规划基本完成；可以推进实现准备，但尚不具备直接启动全部正式实验的条件。**
>
> 本次实读材料：
> - [原交接计划](sol_training_comparison_handoff_cn.md)。
> - [当前 Focus](../focus_gmm_pseudolabel_handoff.md)。
> - [P3 Protocol](../../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P3_matched_training_semantic_comparison/protocol.md)。
> - [训练对象表](../../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P3_matched_training_semantic_comparison/tables/training_object_contract.csv)。
> - [历史训练审计表](../../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P3_matched_training_semantic_comparison/tables/historical_e14_p1_p2_audit.csv)。
>
> 尝试读取用户指定的 Sol 任务：运行登记对应 ID `01a07745-5ca4-71c2-b712-d332d7cb1e1f`。本机 `list_threads` 和 `read_thread` 返回接口已不可用，要求使用当前不可调用的 codex_app MCP。因此**本次核验了上述本地产物，未成功读取该任务对话，不能核定对话内是否有更新授权**。执行者应先从自己的用户指令核对批准回执，不能把本次接口故障当作要求用户重复批准的理由。
>
> 当前可见 Protocol 为 `DRAFT_NOT_EXECUTABLE`，其文字记录执行批准为 NONE；本地新 worker 目录未发现。该观察只能说明当前可见记录未证明已运行，不能据此断言其他远程位置没有作业。
>
> | 原要求 | 文件中完成情况 | 审核意见 |
> |---|---|---|
> | 区分 P1 不训练与 P2 仅粗路由训练 | 已有独立历史表 | 达标；旧代码 stage_2_only 不是两阶段训练 |
> | 四种架构、共享 8＋平铺 16 | 已给公式、rank 缩放及参数表 | 达标；属于构造合同，运行时仍须复核张量 |
> | 从共同冻结基座重训 | 已明确；H 三组初始哈希相同 | 达标 |
> | 粗细同时监督、合法打乱 | 已明确 0.5/0.5 与教师父组内细分类 | 可构造的候选；权重属于新选择 |
> | 数据互斥、教师仅训练集拟合 | 已给 56,538 条唯一内容和 70/15/15 候选计数 | 设计完整；当前两张 CSV 不能复核原始去重计数，须补机器产物 |
> | 512/1024 与负载政策 | 已有明确触发、优先级和上限 | 基本达标；“充分”仅指预算内没有触发指定晚段变化规则 |
> | 正式分析 | 有两比较×两种子的合取规则 | 达标的候选；不可套用旧 E14 A/B/C 名义 |
> | 实现和资源检查 | 有资格清单与 1/18/36 小时候选上限 | 尚缺实测；两步梯度门与全流程资源范围需修订 |
>
> ## 2. 第二步的唯一目标、范围和成功标志
>
> **目标：确定一个实现正确、开发证据支持且资源可承担的共同训练预算与负载政策。**
>
> 本文件的“第二步”是交接后的第二轮执行，不是已完成的 P2，也不是模型的第二训练阶段。覆盖原计划 3.1 的补齐及 3.2 的实现/预审；不包含 3.3/3.4 全部正式训练。
>
> 成功标志：数据/教师/代码通过资格检查；四基线 seed17 开发曲线完整；按既定规则得到唯一预算与政策；提供实测剩余成本。若达到 1024 上限仍未稳定，正确交付为 `BUDGET_LIMITED_INSUFFICIENT` 并停止，而非继续加训练。
>
> 第二步不得宣称语义方法有效，也不评选最终测试集模型。
>
> ## 3. 执行前必须修正或补实的六点
>
> 这些是本次具体审核指示。改动进入同一 P3 Protocol；不要再造 protocol_v2 或设计文件。若已有执行，采用追加修订并标明证据资格影响，不能覆盖已冻结条款。
>
> ### A. 按最新仓库规则处理批准，避免过度阻塞
>
> 最新 AGENTS.md 允许范围内本地实现与小型非破坏检查；不必为了编译、单元测试、CPU 假数据验证再单独请求科学批准。删除 Protocol/Focus 中把“所有实现、本地检查都必须重新授权”视为仓库硬规则的措辞。科学设计变化仍由用户确认，完整/昂贵远程运行仍须明确范围授权。
>
> `researchctl` 重叠是提示，不是锁。本次 context 已成功；原计划的解析故障只是历史记录。写当前任务需登记，完成后 release；不要把运行登记当科学批准。
>
> ### B. 将初始化检查、模块可训练性、自然负载分开
>
> 当前规则要求两步结束每个预期 bank 的 A/B 均改变，可能把未被选中的专家误判为实现错误，也可能把 AdamW 衰减造成的参数变化误判为收到任务梯度。
>
> 修订为三层检查：
> 1. 初始化恒等性：B 全零时输出等于冻结基座，允许 A 的首步任务梯度为零，也允许纯任务路由首步梯度为零。
> 2. 定向本地可训练性测试：用构造路径逐一覆盖每个专家；第一步更新 B，第二步检查有激活且非退化输入下 A/B 的损失梯度。单独用非零专家输出检验在线路由任务梯度；用真/打乱目标检验两个分类头；检查的是反向梯度与受梯度驱动的变化，而非仅参数差。硬路径仅用假数据验证影子路由代码，不启动 H-hard 正式训练。
> 3. 自然数据冒烟/预审：记录每个专家选择次数、梯度和参数变化；只对实际激活模块检查应有梯度。零选择专家计入饥饿诊断，不能假称已经验证其自然可训练性，也不能一律以实现失败排除。
>
> float32 小型测试使用固定误差容忍度；真实 bf16 因果检查保持相同张量形状、内核和运行方式，先实测重复前向误差再冻结容忍规则。不得在看到后缀不变性失败后放宽阈值掩盖问题。
>
> ### C. 补数据去重的可复核产物与问题重复检查
>
> 保留当前自然比例 70/15/15 作为推荐候选，不恢复循环复制。生成原文件哈希、保留/删除映射、split IDs、规范化内容键、来源计数、答案词元计数和零重叠检查 JSON/CSV。
>
> 除了完整 prompt＋answer 键，增加**只含问题文本的键**检查跨集合重复。同一问题不同答案或选项格式可能逃过当前检查。若发现，先报告数量与对应来源；在划分前以同问题组分配，更新计数与协议，而不是在看测试结果后剔除。不要求此次解决所有语义近重复或预训练污染。
>
> 当前训练候选 39,576 条，有效批量 128：512 更新约 65,536 次样本暴露，即 1.656 遍；1024 更新约 131,072 次，即 3.312 遍。实际尾批、累积跨 epoch、有效答案词元数必须实报。与旧 4096 条、128 更新四遍是不同数据分布与覆盖量，不能说“步数四倍，所以训练更充分”。
>
> ### D. 写清训练损失加权与开发指标的差别
>
> 当前 Protocol 选择每个微批对答案位置取均值，再累积16个微批；这不等于对整个有效批量的所有答案词元统一取均值。
>
> 第二步默认保留该已写候选，明确数学形式为 $\frac1{16}\sum_{b=1}^{16}\frac{\sum_{t\in b} \ell_t}{N_b}$，三个损失项使用相同有效位置和归一化。开发/测试仍使用总损失除以总答案词元数。报告这是目标加权差别，并测试小批计算与预期公式一致。若决定改成全有效批词元归一化，必须所有条件一起改并在训练前冻结，不能只改语义组。
>
> ### E. 补足教师和数据准备的资源范围
>
> 原“smoke ≤1 H100小时、预审≤18、正式≤36”没有完整实测依据。资源表必须分别列：tokenize CPU 时间、冻结基座训练集前向及缓存、PCA/GMM CPU或GPU时间、开发前向频次、训练、加载/保存、重试成本。八千余条开发样本的评估不可漏算。
>
> 先用不进入正式模型的小样本测量训练和冻结特征提取吞吐；两次更新仅验证流程，至少追加一个明确丢弃权重的短计时段以避开初始化开销。计时段包含真实 microbatch8/accum16，记录预热与计时更新数。测量均在已批准远程资源范围内；不因“准备数据”而绕过完整基座前向的成本批准。
>
> 把总成本写成各部分之和，说明 teacher/data 准备计入哪一个批准额度。超额度不得自动启动。54 小时只对应原预审＋正式候选之和，并非包含冒烟和所有准备的已批准总价。
>
> ### F. 固定预审复用和停机边界
>
> 当前条款只允许最终512且负载关闭复用原 seed17 预审。这是明确但保守的候选，第二步照此执行；若想复用1024或负载开启的最终配置运行，在测试封闭且正式开始前注册确定规则，不能事后只挑更好 checkpoint。
>
> 1024仍触发晚段规则，立即停止，不跑负载选择或正式矩阵。最终H语义条件后期仍改善，是未来正式阶段的预算资格问题；第二步不能预先证明它们会稳定。
>
> ## 4. 建议保留的具体科学配置
>
> 以下为审核者明确推荐，仍须以用户实际确认回执为科学批准依据；若 Sol 任务已有明确确认则直接记录，不重复询问。
>
> | 项目 | 推荐执行配置 | 含义/边界 |
> |---|---|---|
> | 架构 | D24；F8×24；SF共享8＋8×16；H共享8＋3粗8＋8细8 | 12+12不加入；总参数不相等 |
> | 教师 | 训练集末层整窗均值、PCA64、对角GMM三父组3/3/2 | 保留参考答案特权，不换层 |
> | 语义分类 | 0.5粗分类＋0.5教师父组内细分类 | 初始候选，不声称权重最优 |
> | 正式主指标 | 两种子分别 H-task−H-sem、H-shuf−H-sem | 两比较均支持才通过，不合并种子掩盖差异 |
> | 预审 | D/F/SF/H-task，seed17，先512更新 | 开发集选共同预算，测试封闭 |
> | 增长触发 | 384→512改善≥0.002且区间下界>0，或达到已注册幅度的排序变化 | 任一基线触发则四组共同从头1024 |
> | 上限判断 | 768→1024同规则 | 仍触发则预算内证据不足并停止 |
> | 均衡 | 默认关闭；只在当前Protocol饥饿触发时检查H-task开关 | 条件3/3/2更新；同H政策，不做全矩阵开关 |
> | 优化 | 原协议2e-4适配器、5e-4路由，AdamW，5%预热，余弦衰减 | 不一边跑一边调学习率；固定末步 |
>
> 自然来源比例及较小来源测试规模是重要选择，不把主指标解释成八来源等权能力。0.002是预审实际变化阈值，不是收敛证明或最终语义收益门槛。
>
> ## 5. 逐项执行安排
>
> 实验文档根：`Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P3_matched_training_semantic_comparison/`。
> 执行工作区候选：`/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p3_matched_training`。已有时先检查，不覆盖；旧E14/P1/P2只读引用。
>
> ### S1：补合同与本地测试
>
> - [ ] 将上节A—F逐项处理到同一Protocol，附修订表；不改历史P1/P2结论。
> - [ ] 核对五项科学选择及远程范围是否已有用户批准，缺失者集中列一次；更新实际状态，不以本计划代签。
> - [ ] 构造SF模型和统一H监督逻辑；冻结基座；断言实际参数计数和H三条件初始哈希一致。
> - [ ] 完成定向梯度、零B恒等、错父条件分类、合法置乱、SF共享覆盖、损失归一化、路径系数和因果输入测试。
> - [ ] 用极小假数据做连续训练与中断恢复对照：恢复优化器、调度、随机状态、采样游标、累积状态；结果按已声明数值规则一致。
>
> 交付：修订条目表、本地测试结果、数据去重机器记录、待授权远程范围。此时不需要新结果summary，不伪造“训练完成”。
>
> ### S2：批准范围内的小样本真模型检查与计时
>
> - [ ] 单张H100标准配额，全部权重可丢弃；测试D/F/SF/H-task/H-sem/H-shuf代码路径，非正式种子和数据身份明确标记。
> - [ ] 用有限训练记录形成小型临时教师/标签仅供冒烟；正式教师需由完整训练split重新拟合冻结，不能把临时教师投入正式训练。
> - [ ] 记录梯度、基座冻结、相同答案掩码、因果输入、数据和checkpoint身份检查。
> - [ ] 分开记录特征提取、训练和开发评估吞吐，测算正式教师＋四组512预审＋可能四组1024重跑＋一次负载分支的最坏成本。
>
> 交付：冒烟回执、测试/计时JSON、失败账目、资源估算及明确上限。如果已有授权覆盖且估算不超限，自动进入S3；否则只提出尚缺的远程范围，不重问标准配额偏好。
>
> ### S3：构造并冻结正式训练对象
>
> - [ ] 生成互斥正式split，保留完整去重映射；若问题键检查改变计数，先按修订合同验证。
> - [ ] 只对训练集合拟合正式教师，保存PCA/GMM参数、所有重启选择轨迹、分组规则、训练输入哈希；非空/收敛资格失败则停止。
> - [ ] 开发只用于预算/负载；测试标签、输出和效果保持封闭。保存初始状态、代码/环境、协议和配置哈希。
> - [ ] 明确全部任务与分类损失只在规定答案预测位置归一化；均衡计数范围按协议与答案计数分别存储。
>
> 交付：正式数据和教师manifest、初始化/配置manifest、资格检查；原始张量和日志留执行工作区。
>
> ### S4：运行四基线512预审
>
> - [ ] 顺序运行D、F、SF、H-task的seed17；同记录顺序、micro8、accum16、512更新。保存0/128/256/384/512，完整开发记录至少覆盖384和512。
> - [ ] 不查看测试。存每条开发记录loss_sum与answer_token_count，按协议来源分层配对重采样计算384→512差值；报告全部六对架构排序变化。
> - [ ] 存每层专家负载、选择数、梯度和参数变化，分开报告“从未选中”和“选中了却缺少梯度”。
>
> 出口：不触发增长则候选预算512；任一触发则S5。不得因喜欢某架构而只延长它。
>
> ### S5：仅触发时1024重跑，随后决定均衡
>
> - [ ] 四组从已记录共同初始状态按1024总调度重跑，不能续接已降到零学习率的512终点。
> - [ ] 768→1024仍触发：交预算不足结论，终止本轮，不自动扩卡、第三种子或增加步数。
> - [ ] 达到预算门后，按Protocol对该预算的无偏置H-task检测饥饿；仅触发才从同初始状态跑一次load-on，使用同总调度。
> - [ ] 开发收益至少0.002且区间下界为正、资格通过才选择开启，否则关闭；报告父组内负载，不以负载均匀当作语义证据。
>
> 出口：唯一共同预算、唯一H均衡政策、预审合格checkpoint名单及可否复用；不打开测试、不启动正式语义训练。
>
> ## 6. 交回原分析任务的文件与裁定条件
>
> 第二步完成后在同一canonical实验目录维护 `detailed.md` 的预审执行记录及 `tables/preflight_decision.csv`；若形成完整有边界的预审结果，可在 `summary.md` 明确标“仅预审完成，正式语义比较未运行”，禁止使用全实验完成状态。
>
> 必须交回：
> 1. 当前Protocol及批准记录、相对本次审核的修订表；逐项说明A—F已处理或仍未解决。
> 2. 数据计数/交叉重叠/词元、模型参数、梯度及因果资格表。
> 3. D/F/SF/H-task每条预审运行的配置、实际更新、实际数据遍数和答案词元、耗时、checkpoint及哈希。
> 4. 开发曲线图、晚段差值与区间、排序变化表、均衡触发与政策表。每张图给来源、横纵轴、单位和可支持边界。
> 5. 测试未解封证明（访问/评估记录与产物状态）、失败/排除账目、剩余正式矩阵清单及实测成本。
> 6. **唯一下一决策：**预算/政策资格通过时，建议按固定设置补齐12条正式核心矩阵；预算上限仍失败时，建议先重新讨论训练预算或学习任务，不启动正式比较。
>
> 用户随后只需提供Sol任务引用与结果目录。审核者先尝试read_thread，再以机器产物和canonical记录核对；接口不可用必须声明，不根据任务标题或口头“全通过”确认。
>
> ## 7. 可以直接发给 Sol 的指示
>
> > 请按 `daily_research_reports/0906/plans/sol_p3_second_step_execution_plan_cn.md` 完成第二轮。先处理A—F并完成本地验证；核对我已批准的科学与远程范围，已批准部分不重复询问。远程范围明确后执行小样本检查、正式数据教师冻结和四基线seed17预审，按预定规则决定512/1024及H负载政策。本轮止于预算/政策结论，不直接运行全部正式语义比较，不解封测试。交回修订协议、资格表、预审曲线与区间、完整运行回执和剩余成本供独立审核。
> EOF
> python - <<'PY'
> from pathlib import Path
> import re
> p=Path('daily_research_reports/0906/plans/sol_p3_second_step_execution_plan_cn.md')
> s=p.read_text()
> for link in re.findall(r'\]\(([^)]+)\)',s):
>     assert (p.parent/link).is_file(),link
> assert all(x in s for x in ['### S1','### S2','### S3','### S4','### S5'])
> print('UTF-8, local links, five execution steps: PASS')
> print('Lines:',len(s.splitlines()))
> PY
> ./researchctl release``
>
> </details>
</details>

已写入：[Sol 第二步执行计划](../plans/sol_p3_second_step_execution_plan_cn.md)。

**结论：Sol 的初步规划基本达标，但应先完成实现验证和训练预审，再启动正式比较。**

第二步明确安排为：

1. 补齐协议：修正梯度检查、数据重复检查、损失加权和资源核算。
2. 完成本地测试与小样本真模型检查。
3. 冻结正式数据、教师标签和初始化。
4. 运行四种基线、种子17、512次更新的开发预审。
5. 按预定规则决定是否共同重跑1024次，以及是否启用负载均衡；交回审核。

**本轮终点是确定共同训练预算和负载政策，测试集保持封闭。**文档已列出验收证据、停止条件和可直接发给 Sol 的指示，链接检查通过。

读取边界：任务对话接口目前不可用；本次实际审核了 Sol 的协议、训练对象表、历史审计表和当前 Focus，未核实其对话中的最新授权。

> 我确认一下，本次任务是否会开始跑实验，不要再让它调用 multi-agent 了。之前调用 multi-agent 效率很低，手机在一个对话里面进行就完成。然后确切地给出训练的结果，给出认识的更新，能否把后面的步骤也进行合并。

<details><summary>2 previous messages</summary>

> 会，本轮应推进到实际训练和结果分析。我会把后续基线与语义比较合并为同一任务，明确禁止 multi-agent，由 Sol 在一个对话里串行完成；保留必要的预审停止条件，避免训练不合格时仍强行给结论。
>
> <details><summary>Ran 2 commands</summary>
>
> - Ran `tail -12 daily_research_reports/0906/plans/sol_p3_second_step_execution_plan_cn.md; ./researchctl context A15.gmm_pseudolabel_oracle_gap --task 'Update requested Sol plan to single-agent end-to-end execution with results and bounded interpretation' --path daily_research_reports/0906/plans/sol_p3_second_step_execution_plan_cn.md`
> - Ran `python - <<'PY'
> from pathlib import Path
> p=Path('daily_research_reports/0906/plans/sol_p3_second_step_execution_plan_cn.md')
> s=p.read_text()
> s=s.replace('# Sol P3 第二步执行计划：合同补齐、实现验证与训练预审','# Sol P3 合并执行计划：单对话完成预审、正式训练与结果分析')
> insert='''
> ## 最新用户指示：单任务连续执行（2026-09-06）
>
> 本节覆盖下文旧版“只到预审、交回后再启动正式训练”的阶段边界。下文S1—S5保留为内部检查节点，不再是正常情况下的任务终点。
>
> - 用户要求本任务实际运行实验，并合并后续步骤至训练结果与认识更新；执行者为Sol，在同一个对话内完成。
> - **禁止调用multi-agent、spawn_agent、派生子代理或另建执行任务。**读取已有任务不属于多代理执行；也不需要代理替自己审核。Sol自行检查代码和证据。
> - 连续范围：合同补齐→本地验证→真模型小样本检查→数据/教师冻结→四基线预审→固定预算与负载政策→补齐正式核心12条件→冻结后测试→结果分析。合格时自动前进，不在预审完成、基线完成时重复请求继续。
> - 本次用户指示是合并执行与实际实验的范围授权，执行者应在唯一Protocol记录原意与范围。已有科学配置确认继续有效；本指示不等于替用户确认未定义或新改变的科学判断。执行者先核对自己对话中的确认记录，仅将尚缺且会改变解释的科学选择集中提出一次，不重复询问资源偏好或已批准步骤。
> - 沿用单张H100标准配额及已确认的资源上限；本指示不是无限预算授权。先实测总成本，准备/教师费用明确计入预算。若现有批准不能覆盖成本，报告唯一缺口；不得以串行自动执行为由越过上限。
> - 预审达到1024上限仍不合格、数据或梯度资格失败时，暂停依赖步骤，输出真实失败证据和有边界的认识；不能为了完成12条件强行继续或伪造训练结果。
>
> ### S6：自动补齐正式训练
>
> 预审通过后按唯一冻结配置完成D、F、SF、H-task、H-sem、H-shuf，各seed17和29，共12个正式条件。依照Protocol复用合格预审运行，不重复训练；不符合复用规则则从共同初始状态训练。H-hard/H-oracle仍为条件分支，不因本次合并而自动新增四条训练。
>
> 记录每个条件实际更新、数据遍数、答案词元暴露、可训练/冻结模块、优化器、学习率、最终checkpoint与哈希。全部H条件使用相同预算、在线系数和负载政策。预算资格检查在测试前完成；不得看测试结果决定续训。
>
> ### S7：测试与正式结果
>
> 代码、数据、教师、初始化、预算、政策、checkpoint和分析脚本均冻结后解封测试。按Protocol生成逐记录损失和词元数、每种子两个主差值及配对区间、架构参照表、训练曲线与成本表。严格执行支持/不支持/证据不足/资格失败规则，不用路由一致率替代答案预测收益。
>
> ### S8：完成交付与认识更新
>
> 在canonical summary.md写完整四段式说明，在detailed.md保存全设置与证据账目。最终回复给出实测训练结果表，明确回答：
> 1. 在规定预算和晚段规则下，哪些模型通过训练稳定性资格，哪些没有；不把它解释成绝对收敛。
> 2. 四种架构表现如何，共享容量与总参数差异使哪些解释仍不成立。
> 3. 真实语义监督是否在两种子上同时超过同架构任务训练和打乱标签。
> 4. 相对P1/P2，哪些认识被支持、削弱或仍未知，以及唯一下一决策。
>
> 认识更新写成AI核验建议，不代填研究者最终判断。先完整交付结果，不以“等待用户先总结”扣留分析；人工确认后再更新人拥有的科学状态和延迟日报。无需在结果生成前另叫审核代理。用户可随后把本任务引用交原分析任务独立复核。
>
> **合并任务完成标志：**所有批准的必跑条件及分析完成，结果可追溯，四段式总结和认识更新可独立阅读；或达到预先规定的硬停止条件并交付完整失败/不足证据。成功跑完不等于得到正结果。
>
> '''
> s=s.replace('## 1. 本次审核结论与读取边界',insert+'## 1. 本次审核结论与读取边界',1)
> s=s[:s.index('## 7. 可以直接发给 Sol 的指示')]+'''## 7. 可以直接发给 Sol 的指示
>
> > 按本文件顶部“最新用户指示”在当前一个对话内连续完成实际实验，禁止multi-agent及新建执行任务。先完成S1—S5，合格后自动进入S6—S8，补齐12个正式条件、测试和结果分析，不在正常阶段交接点再次问是否继续。遵守已确认的科学合同和资源上限；只对真实缺失的科学选择或超预算作一次集中说明。最终给出确切训练结果、四段式证据分析、认识更新建议和唯一下一决策；保留负结果与失败记录。\n'''
> p.write_text(s)
> assert '禁止调用multi-agent' in s and '### S8' in s
> print('Updated combined execution scope and single-agent constraint; UTF-8 check PASS')
> PY
> ./researchctl release`
>
> </details>
</details>

**是，会实际跑实验；后续步骤已合并，不再只停在规划或预审。**

已更新[执行计划](../plans/sol_p3_second_step_execution_plan_cn.md)，明确要求：

- **Sol 在一个对话内完成，禁止 multi-agent、子代理和新建执行任务。**
- 连续完成：实现检查 → 训练预审 → 固定预算 → 12个正式训练条件 → 测试 → 结果分析。
- 正常通过检查就自动继续，不在每个阶段重复询问。
- 最终交付**实际训练结果表、四段式分析、认识更新建议和唯一下一决策**。

若触发预算上限或数据、梯度资格失败，则交付具体证据并停止受影响步骤，不能强行宣布完成。

本次我已修改计划，**尚未提交训练作业**；你将计划交给 Sol 后，由它按合并范围执行。

> 请阅读/data/250010109/Research\_System/daily\_research\_reports/0906/plans/astra\_p3\_4h100\_final\_audit\_handoff\_cn.md，判定是否完成了实验任务（我们忽略了1024，但是我认为512已经足够可以判断）。同时阅读 @0906 Sol 执行Router实验，确认目前我们的任务进行到哪一步骤，现阶段结论是什么？怎么得出的结论？确切的下一步是什么？完整的下一步是什么？

<details><summary>2 previous messages</summary>

> 我会先核对交接文档、正式结果和实际运行配置，再判断任务是否完成。你接受用 512 步作判断，我会据此区分“固定预算下的方法比较”和“训练已充分收敛”，并核对 Sol 任务的最新进度。
>
> <details><summary>Explored 3 files, a list, ran 2 commands</summary>
>
> <details><summary>Explored a file</summary>
>
> - Read `./daily_research_reports/0906/plans/astra_p3_4h100_final_audit_handoff_cn.md`
>
> </details>
>
> Tool call
>
> Tool: read_thread
> Status: completed
>
> - Ran `ls /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p3_matched_training/runs/full-20260906T170500Z/analysis; cat /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p3_matched_training/runs/full-20260906T170500Z/receipts/acp_and_postrun_audit.json; find /data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p3_matched_training/runs/full-20260906T170500Z -name '*.npz' | head; tail -65 Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P3_matched_training_semantic_comparison/protocol.md`
>
> <details><summary>Explored 2 files, a list</summary>
>
> - Read `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p3_matched_training/analysis.py`
> - Read `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p3_matched_training/runs/full-20260906T170500Z/receipts/formal.json`
> - Listed files in `A15_13_E14_P3_matched_training_semantic_comparison`
>
> </details>
>
> - Ran `python - <<'PY'
> import numpy as np,json,csv
> from pathlib import Path
> r=Path('/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p3_matched_training/runs/full-20260906T170500Z')
> a={}
> for p in sorted((r/'evaluations/test').glob('*.npz')):
>  d=dict(np.load(p)); a[p.stem]=d
>  print(p.stem, len(d['record_id']),int(d['token_count'].sum()),float(d['loss_sum'].sum()/d['token_count'].sum()))
> ref=next(iter(a.values()))
> for d in a.values():
>  for k in ['record_id','source','token_count']: assert np.array_equal(ref[k],d[k])
>  assert np.isfinite(d['loss_sum']).all()
> for seed in [17,29]:
>  t=a[f'H-sem__seed{seed}__load_off']
>  for name in ['H-task','H-shuf']:
>   b=a[f'{name}__seed{seed}__load_off'];rng=np.random.default_rng(20260906); vals=[]
>   groups=[np.flatnonzero(b['source']==i) for i in range(8)]
>   for _ in range(2000):
>    ix=np.concatenate([rng.choice(g,len(g),replace=True) for g in groups]);den=b['token_count'][ix].sum()
>    vals.append(b['loss_sum'][ix].sum()/den-t['loss_sum'][ix].sum()/den)
>   print('INDEPENDENT',seed,name,float(b['loss_sum'].sum()/b['token_count'].sum()-t['loss_sum'].sum()/t['token_count'].sum()),np.percentile(vals,[2.5,97.5]).tolist())
> fm=json.loads((r/'receipts/formal.json').read_text())['formal_condition_tags']
> for key,tag in fm.items():
>  h=json.loads((r/'conditions'/tag/key/'train_history.json').read_text()); assert [int(x['update']) for x in h]==list(range(513))
> print('12 arrays matched finite; 12 histories contiguous 0..512 PASS')
> PY`
>
> </details>
</details>

**本轮核心实验已经跑完，512 步足以给出本次固定预算下的判断；结果是“证据不足”，不是“实验没完成”。**我已读取“0906 Sol 执行Router实验”，并从原始测试数组独立重算四个主比较，结果与 Sol 一致。

但完整交付还有一个缺口：目前 canonical 目录已有协议、表格和图，**尚缺正式的 `summary.md`、`detailed.md`**。因此，训练和数值分析完成，正式结果记录尚未收尾。

**1. 512 步为什么可以判？**

取消1024分支是在看到384／512步开发结果之前，由你批准的修订，不是看到结果后降低标准。

实际情况是：

- 12个核心条件全部完成512步，训练历史连续。
- 每个条件测试均为8,481条记录、562,954个答案词元；我核对了样本、来源和词元数完全配对。
- 四基线最后128步的开发损失改善均低于预设的0.002阈值，六个层级条件也未触发预算不足规则。
- 因此，**按已批准合同，512预算资格通过，无需补1024才能判定。**

边界是：这支持“512步下的比较有效”，不证明更长训练绝不会改变结论。

**2. 当前结论是什么，怎么得出？**

答案预测损失越低越好。以下“收益”均为对照损失减去语义模型损失，正值表示语义监督更好。

| 比较 | 种子17：收益及95%区间 | 种子29：收益及95%区间 |
|---|---:|---:|
| 纯任务训练 − 真实伪标签监督 | **+0.010320**［0.009795，0.010890］ | **−0.002078**［−0.002469，−0.001680］ |
| 打乱标签监督 − 真实伪标签监督 | **+0.014645**［0.014138，0.015128］ | **+0.005467**［0.005064，0.005837］ |

这些区间是我从逐记录数组重新进行2,000次来源分层、样本配对重采样得到的。

由此得到两条不同的认识：

- **真实标签对应关系比打乱对应关系更好：两个种子都支持。**但这可能包含“打乱监督造成干扰”，不能单凭它证明添加语义监督值得。
- **真实语义监督是否胜过不加监督的正常基线：两个种子方向相反。**种子17明显获益，种子29明显受损。

所以正式判定 **`INSUFFICIENT`：尚未证明语义监督具有跨这两个种子一致的增量收益。**不能用两个种子的平均正收益覆盖这一反转。

架构方面，普通平铺模型在两个种子上都优于普通适配模型；但共享平铺和层级模型的相对排名不稳定，尚不能据此认定共享或层级结构有稳定优势。

**3. 我们现在到哪一步了？**

| 环节 | 当前状态 | 认识更新 |
|---|---|---|
| P1：冻结模型，干预粗细路径 | 完成 | 旧部署差距主要与粗路径有关 |
| P2：只补粗路由监督 | 完成 | 原监督缺失可修复，不必先换教师层 |
| P3：重新训练、公平比较 | 核心训练与分析完成 | 修复训练错误之后，语义监督仍未稳定胜过纯任务训练 |
| 硬伪路径／来源真值参照 | 未运行，属于条件分支 | 当前核心矩阵不因缺少它们而不完整 |

**关键认知更新是：现在的问题已经从“粗路由有没有被正确训练”，变成“正确训练之后，语义约束为什么有时帮助、有时干扰任务优化”。**

**4. 确切下一步与完整后续路径**

**AI 建议：先用现有结果定位种子反转，不立即换标签、加1024或训练硬路径模型。**

具体顺序如下：

1. **完成本轮证据收尾。**补正式 Summary、Detailed，保留上述“证据不足”裁决，不能把交接草稿当最终结果记录。
2. **进行一次不训练的反转审计。**比较两个种子的 H-task 与 H-sem：
   - 在128、256、384、512步，优势何时出现、是否发生反转；
   - 开发集各来源中，差异是广泛存在还是集中在少数来源；
   - 路由负载、分类损失和专家更新量是否伴随异常。
   这些只能定位候选原因，不能单独证明机制。
3. **根据审计只选择一个后续实验。**
   - 若发现实现、恢复或评估异常：只修复并重跑受影响条件。
   - 若没有异常，且反转已在开发阶段持续存在：优先检查**语义监督强度是否过强**，固定架构、教师、512预算，设计一个较弱监督权重与当前权重、纯任务训练的配对比较。
   - 若主要问题是随机初始化造成的波动、没有具体机制线索：再预先固定额外种子和汇总规则，检验稳定性；不能持续加种子直到结果变正。

**当前最该锚定的问题是：真实伪标签约束在什么条件下帮助任务优化，又在什么条件下造成干扰？**先把这个反转解释清楚，再决定是否值得改教师层位或展开硬路径分解。

> 阅读 @0906 Sol 执行Router实验 最终的审计结果，给出你的进一步分析，然后为我解析实验分析，让我理解，然后为我规划下一步具体的探究问题与实验安排

<details><summary>5 previous messages</summary>

> 我会先读取 Sol 最后的审计结果，核对它是否改变了此前“种子间方向反转”的判断，再解释结果，并把下一步收缩为一个具体问题。
>
> <details><summary>Explored a list, ran a command</summary>
>
> Tool call
>
> Tool: read_thread
> Status: completed
>
> <details><summary>Explored a file, a list</summary>
>
> - Read `./.agents/skills/research-document-explainer/SKILL.md`
> - Listed files in `A15_13_E14_P3_matched_training_semantic_comparison`
>
> </details>
>
> - Ran `cat Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P3_matched_training_semantic_comparison/summary.md; cat .agents/skills/research-document-explainer/references/explanation_contract.md .agents/skills/research-document-explainer/references/terminology_contract.md .agents/skills/research-document-explainer/references/experiment_reasoning.md .agents/skills/research-document-explainer/references/research_thinking.md`
>
> </details>
>
> 最终审计补强了一个关键事实：两个种子的差异从第128步就已存在，之后一直保持，已检查的范围内没有发现训练或评估故障。因此，降低监督权重是合理的下一项干预，但目前不能说已经找到了原因。我会特别区分“比当前强监督好”和“真正比纯任务训练好”这两个目标。
>
> <details><summary>Explored a file, a search</summary>
>
> - Read `./Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P3_matched_training_semantic_comparison/tables/reversal_audit_decision.json`
> - Searched for `follow|0.25|fresh|test|seed|gradient` in `detailed.md`
>
> </details>
>
> Viewed an image
</details>

[正式实验总结](../../../../experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P3_matched_training_semantic_comparison/summary.md)和[完整证据记录](../../../../experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P3_matched_training_semantic_comparison/detailed.md)已经补齐。我也读取了 **“0906 Sol 执行Router实验”** 最新完成的反转审计。

**我的判断：本轮实验已完成。语义监督没有表现出两个种子一致的任务收益；新审计把问题进一步定位到了训练过程中持续形成的差异，但尚未证明是监督权重过强。下一步可以只做一个“监督强度减半”的配对实验。**

**一、最终审计到底增加了什么认识？**

此前只知道：语义监督在种子17上优于纯任务训练，在种子29上反而更差。现在新增了三条证据：

| 审计发现 | 能更新的认识 | 不能据此断言 |
|---|---|---|
| 第128步已经出现相反方向，持续到512步 | 差异不是只在最后一个检查点偶然出现 | 原因一定是初始化，或一定是监督太强 |
| 删除任一数据来源，最终汇总方向仍不改变 | 不是单个来源独自造成的反转 | 所有来源都同样受益或受损 |
| 已检查范围内没有恢复、冻结、配对或数值异常；专家均有更新 | 暂时没有理由优先重跑故障条件 | 已排除所有实现问题或优化问题 |

下面这张图最关键：

![开发集反转审计](../../../../../../../daily_research_reports/backup/2026/09/0906/figures/reversal_development_effects.png)

读图：纵轴是“纯任务模型损失－语义监督模型损失”，正值支持语义监督；蓝线持续为正、红线持续为负，说明两种子的差异在训练中已持续存在。

这里所谓“反转”是**两个种子之间方向相反**，不是同一个模型训练到后期突然从好变坏。

**二、怎么理解这个实验？**

纯任务模型只被要求：**把答案预测好。**

语义监督模型同时被要求：

1. 把答案预测好；
2. 粗路由尽量符合离线粗标签；
3. 细路由尽量符合离线细标签。

这些要求不必天然一致。离线标签具有可预测性，并不代表严格遵循它就能得到最好的答案预测。

审计确实发现，语义监督显著改变了分发：

- 纯任务模型最后四分之一训练中，最常用粗专家承担约 **95%** 的答案位置；
- 语义监督模型对应比例约为 **55%～56%**。

**这说明监督确实改变了路由行为，但更分散不等于更有效。**纯任务模型集中使用某个粗专家，也不自动意味着它训练失败。

我的候选解释是：语义约束可能帮助部分训练过程避开较差的分发方式，同时也可能限制另一些本来表现更好的任务分发方式。它与当前结果相容，**还需要干预实验验证**。

另外，种子同时可能影响初始化和数据顺序，所以目前不能把差异单独归因于“初始化不好”。

**三、下一步锚定一个什么问题？**

**AI 建议：**

> 在架构、教师标签和512步预算不变时，把粗细语义监督权重同时减半，能否减轻种子29的损失，同时保留种子17的收益？

这是检查当前训练目标的最小改动。它还不涉及换教师层、改聚类、增加专家或延长训练。

将训练目标写成：

\[
L=L_{\text{答案}}+\lambda L_{\text{粗分类}}+\lambda L_{\text{细分类}}
\]

其中，\(\lambda\) 表示要求路由器服从伪标签的强度。

| 条件 | \(\lambda\) | 用途 |
|---|---:|---|
| 纯任务训练 | 0 | 判断添加语义监督是否值得 |
| **减半监督** | **0.25** | 唯一新增干预 |
| 当前监督 | 0.5 | 判断当前强度是否存在可避免的代价 |

所有条件保持同一层级架构、教师、数据顺序、初始化、优化器、512步预算和关闭负载均衡的设置。

**四、具体怎么安排，怎样判断结果？**

**第一步：冻结这一项比较。**

在新协议中明确两个不同问题：

- **减半是否优于当前强度？**回答当前强度是否存在局部改进空间。
- **减半是否优于纯任务训练？**回答减弱后的语义监督是否仍有任务价值。

不能只完成第一个比较就宣布“语义方法有效”。

**第二步：最少新增两次训练。**

只训练减半监督条件，分别使用种子17、29。原有纯任务与当前监督条件，经配置、初始状态、数据顺序和检查点身份核验后作为对照复用。

新增条件必须**从相同初始状态重新训练**，不能从已训练512步的强监督模型继续训练；否则改变的是训练日程，无法回答上述问题。

由 Sol 在一个对话中完成，不调用 multi-agent。

**第三步：用开发集完成机制定位。**

主要比较512步的答案预测损失，按已有样本配对方式计算差值与区间。128／256／384步用于说明差异何时形成，负载和分类损失只作辅助解释。

已经看过的测试集不能再次充当全新的确认集。本轮应明确是**已有数据上的后续定位实验**；若得到正结果，再安排独立确认。

**第四步：按结果决定，不继续随意扫权重。**

| 结果 | 合理解释与行动 |
|---|---|
| 减半在两种子都优于当前强度，也优于纯任务 | 支持减弱约束的候选方案；下一步独立确认 |
| 减半优于当前强度，但仍未稳定超过纯任务 | 减轻了代价，但尚未获得可靠语义收益 |
| 只改善种子29，同时损害种子17 | 存在种子相关的权衡，统一减半未解决稳定性 |
| 减半没有可靠改善 | 本次减半方案不获支持；停止这轮权重试探 |

这里我对 Sol 的停止表述作一个收紧：**0.25无效，只能否定这一次减半修复，不能排除所有“监督过强”的可能。**可以因证据和预算停止这条尝试，但不要把停止研究写成机制已被彻底证伪。

当前应完成的是这一个小实验：**两次新增训练，分清“减少监督带来的伤害”和“真正获得语义监督收益”。**
