# 注意力表征审查执行资料

先阅读《0920_注意力表征空间审查与执行计划.md》。

`build_p_rel.py`和`pool_attention.py`是已测试的辅助代码；模型提取、公开数据准备和完整分析接口仍需在实际项目中接入。

```bash
python build_p_rel.py --output data/P_rel_v1 --seed 20260920
python pool_attention.py
```

后一个命令使用现有PyTorch环境。完整计划也嵌入了这两个脚本及配置模板，单独保留Markdown即可。

未打包任何第三方公开数据或用户模型。`verification_status.json`明确列出实际执行及未执行的检查。
