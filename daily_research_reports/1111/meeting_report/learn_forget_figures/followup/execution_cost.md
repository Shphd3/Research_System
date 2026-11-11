# execution_cost

AI分析；研究者判断Unknown。本轮只用已有本地H100MIG3g.40GB与CPU；没有主训练/探针训练/参数更新/新资源提交。首次中断GPU占用未记录，因此不声称一个精确总GPU小时。

| task             |   GPU_process_wall_seconds | note                                              |
|:-----------------|---------------------------:|:--------------------------------------------------|
| A                |                    0       | 纯CPU：相关、文档bootstrap与内容                  |
| B                |                    0       | 纯CPU：逐feature账本和恢复                        |
| C                |                   79.48655 | 一状态逐位置前向；包含load/IO                     |
| D                |                    0       | 纯CPU绘图                                         |
| E扩展teacher编码 |                   76.21026 | FP32冻结teacher/SAE                               |
| E梯度10条件      |                 1103.175   | 完整进程墙钟含CPU load/统计/IO，非CUDA kernel时间 |
| E首次中断        |                  nan       | 未记录精确秒数，Unknown；没有写成0                |
| F四臂前向        |                  407.9374  | 完整进程墙钟含hash/load/IO，非CUDA kernel时间     |
| F谱/方向统计     |                  404.504   | CPU/GPU混合统计进程墙钟，不能当纯GPU kernel时间   |
| F方向留出核验    |                    0       | 纯CPU；墙钟另见回执                               |
