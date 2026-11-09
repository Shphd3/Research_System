# 差异记录

- 读取本轮结果前：前轮新测量36条是TRAIN题，不是独立新DEV；本轮主新诊断使用固定旧DEV64的已有模式二配对题，另用前轮TRAIN36复放核验，不能混名。
- 参数名未直接存入原Adam字典；使用封存生产源码+实际参数对象重建可核验名称映射，按名交换且逐形状/组/步验证。

- Execution completed as frozen: all36cells-by-batches,10320forwardsequences, no omitted branch, no budget expansion, no failed replay, no additional exploratory model forward.
- No scientific setting was changed after outcome inspection. The previous TRAIN36 readout and new paired DEV64 are explicitly kept separate.
