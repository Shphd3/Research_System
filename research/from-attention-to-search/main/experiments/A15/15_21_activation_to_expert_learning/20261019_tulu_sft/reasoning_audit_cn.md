# 三个 Agent 的只读审计

2026-10-19，本对话研究者明确要求“给一些 Agent 帮我检查”；三个 Agent 仅做只读审计，未另开训练、推理或修改协议。

## 1 答案监督与位置审计

sft_answer_mask_audit 独立用CPU逐条核查全部实际缓存：TRAIN1024条/85548答案目标，DEV128/10340，EVAL256/22446。每条缓存目标严格等于JSON input_ids[answer_start:]，position范围为answer_start−1至n−2；全部末目标为原EOS151643。问题、模板及padding不作为目标；train.py不再shift。首答案token由prompt末端位置预测，后续由答案此前内容预测。teacher forcing保留答案前文，原因果mask禁止看未来；本轮未独立扰动未来token测试。

Base/字典冻结、原norm/head为buffer、优化器只接收Branch参数。由于残差支路在最后block之后逐位置工作，冻结h/z缓存对应同一answer-only优化对象，不是全参数SFT。TRAIN/DEV/EVAL首批native/cached logits与NLL差均0；零旁支初始差0，专家down梯度4.68025，首次更新后router CE梯度2.29225，64位置拟合1.23079→0.00007083，恢复下一步严格相同。

## 2 混合数据与历史资产审计

sft_mixture_assets_audit 核对本轮Tulu TRAIN10个来源：ShareGPT267、CoT235、CodeAlpaca156、GPT4Alpaca139、FLAN99、WizardLM91、OASST34、LIMA1、两类science各1。已经混合训练，不是各来源等权混合；token权重还取决于答案长度。当前无独立gsm8k来源字段，CoT/FLAN是否包含GSM8K细分样本未知。来源标签不能替代纯语义领域。

历史确实训练过GSM8K/MATH/MMLU/MMLU-Pro/BBH/GPQA/HumanEval/MBPP八任务混合。完整审计数据是20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z/data/data.pt，内部TRAIN39571/development8480/test8481；实际旧A6R1完成回执记录12条轨迹。该版本部分官方train/test合并重划，不等于未触碰的官方测试；与E14/E18小代理和缺失senior exact SFT身份不同。本轮遵研究者最新“只训练这个”决定，不加入独立GSM8K。

## 3 对照、预算及解释审计

sft_comparison_audit 未发现使当前各条件间比较无效的致命问题。各条件共享配对初始化、数据顺序、3epoch、504更新、256644答案目标，校准统计仅新TRAIN估计。T/R11/L964来自旧参考TRAIN；不能称新SFT低频或语义专家。本轮同时变更数据、格式、answer-only监督、校准统计及有效训练规模；不得将新旧结果差异唯一归因于DCLM、格式新颖性或预训练污染。NLL不是自由生成答案准确率。

发现并保留的元数据残留：冻结配置有旧stamp、旧report/hard deadline、target/spectra priority等未被新pipeline使用的字段。smoke的estimated20_training_eval_wall_seconds还硬编码父实验768步/65402 EVAL，不能作为本轮估时。实际训练按len新cache和新CFG执行504步；当前中位步时.04660秒，对20模型四卡纯训练理想下界约117秒，加评估与保存后另报真实耗时。不改已冻结配置或重跑；派生更正见执行侧provenance/metadata_interpretation.json。

## 证据与状态边界

执行根目录：/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/sft_route_learning/20261019T012300Z。

关键证据：code/select_data.py、extract_sft.py、prepare_sft.py、train.py、common.py，data/manifest.json、provenance/extraction.json、smoke/receipt.json、各训练identity/steps/events。审计证明当前监督与配对设置实现正确，不能替代学习结果或研究者机制判断。科学状态Unknown。
