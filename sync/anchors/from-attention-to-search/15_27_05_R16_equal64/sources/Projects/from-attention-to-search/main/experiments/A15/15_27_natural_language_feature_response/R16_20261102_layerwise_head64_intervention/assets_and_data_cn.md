# 原始资产与复算入口

执行目录：/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R16_20261102_layerwise_head64_intervention

- 模型、权重和tokenizer版本／哈希由manifest.json拥有；确切资产ID和当前可读检查见provenance/input_assets.json。沿用原Qwen3 Base，不混用Dense、A22或R15参考语料。
- 全部737位置的当前输入token、原文后继ID、0基位置和完整可见前文：data/positions.jsonl。自然面板700位置/175个不同文档家族，the面板37位置；两者分开报告。
- 逐位置实际前10候选及精确概率：analysis/raw_outputs.jsonl，共249843条条件记录。analysis/position_metrics.csv保存损失、KL、原首选概率/排名、目标概率/排名、能量及干预范数；document_metrics.csv是文档汇总，summary_metrics.csv是汇总与文档区间。全部在执行目录，未将大原始表复制到项目。
- 参考集data/reference_documents.jsonl含60篇固定TRAIN文档；每篇第33—192个token。原生各层参考表征data/reference_cache/*.npy；28套独立均值、完整特征向量及特征值data/bases/layer01.npz至layer28.npz。随机空间data/random1031.npy等。评估文档、tokenIDs和各层原始目标状态另存data/evaluation_documents.jsonl与data/eval_targets/*.npz。
- 词类沿用旧独立词频/格式规则。analysis/tie_policy.json记录并列最大选最小ID的统一规则，类别成员变化0；analysis/legacy_group_sensitivity.csv保留旧分组敏感性。原GPU chunk未覆盖，首次并列不一致的汇总归档为不合格历史。
- 同一参考谱的旧末层复查：analysis/legacy_replay.csv。原模型各目标状态/损失精确重放；旧谱首选全部一致，投影计算精度导致的最大损失差约0.000201nat，未当成独立复现。
- 数值与来源验证：audit/03_numerics_smoke.json、audit/validation.json、freeze.json、amendments.md。未训练任何模型、分类器或lens。
- 两张既有5090spot的作业pt-od3opbw5已成功完成；执行日志、两rank终止记录和execution_certificate.md记录实际耗时/显存。没有使用H100或修改训练。
- 数值复算顺序：CPU scripts/analyze.py → scripts/validate.py → scripts/render.py；GPU仅在原授权资源下运行scripts/run_gpu.py的fit_smoke与evaluate阶段。报告是经人工核查的AI文字，不自动被初稿生成器覆盖。具体命令见reproduce.md。

[完整认识与观察](summary_cn.md) · [逐例输入和28层候选](casebook_cn.md) · [配置与协议](protocol_cn.md)。科学接受与闭题Unknown；未提交、推送或发布。
