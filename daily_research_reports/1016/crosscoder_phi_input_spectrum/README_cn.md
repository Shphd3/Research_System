# φ关系组输入谱补充

先读[中文报告和四图](report_cn.md)；定义与所有边界见[计算口径](methods_cn.md)。[English](report.md) · [英文方法](methods.md)。

R是冻结186个φ组，F/N是原学习实验的对照，按原胜组规则取真实hidden。主图为共同支持145组、每组128位置，另外保留186组全记录及R/N共同161组。四图各有PNG/PDF；每组谱、位置ID、逐组支持及上下文表、冻结配置、数值资格、审计和代码均保留。

重画四图只需NumPy、Matplotlib和已有中文字体，从本目录运行：

~~~bash
python code/plot_phi_input_hidden.py --root data --selection provenance/plot_selection.json --out /tmp/phi-input-spectrum-replot
~~~

此命令不读取模型、decoder或原始缓存。[独立重绘证据](provenance/replot_verification.json)验证4张PNG逐字节一致。完整统计重算脚本仍需要冻结的执行侧真实hidden缓存和原评分源码，不把已保存谱冒充新计算。

完整抽样位置及逐组原/余特征值在data下三份NPZ；跨全部523,136位置的胜组标签只留执行侧。模型、缓存、字体及日志不进入报告。支持不足直接记NA，原/余方差为零也不会记为0占比。
