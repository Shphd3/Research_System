# 1008 图与来源说明

图按研究者要求排在前；附件 `drawing_prompt.md` 的三图保留为辅助证据。这里整理测量和口径，不改变 Summary 的裁决。

## 主图顺序

| 图 | 画的对象 | 可读出的事实 | 必须保留的边界 |
| --- | --- | --- | --- |
| [受控热力图](../figures/main01_controlled_heatmap.png) | 两步长的 ρ × 答案规则有限损失差，以及翻转减保持的规则差异 | 从 ρ=0.1 到 0.8，规则差异增大；四格都平均降损 | ρ 是任务信号方向内积，不是共享参数比例或 SAE 原子比例；高低条件同时改变 A、B |
| [自然文本损失热力图](../figures/main02_natural_loss_heatmap.png) | 完整步长，四来源 × 四接收域的平均有限 CE 差和增损位置比例 | 16 格均值都为负；约 44%–53% 位置增损 | 是同一检查点的已曝光记录、固定来源的一步探索性测量 |
| [SAE 位移忠实性](../figures/main03_sae_fidelity_heatmap.png) | 各源、全／半步、稳定／全部／切换集合的动态残差能量比 | 稳定集合约 1；切换子集的比值很大 | 比值为能量汇总比；不是原生位移放大倍数，不是解释率 |
| [共同与随机损失分量](../figures/main04_sae_components_heatmap.png) | 分量增损且完整更新降损的位置比例 | 共同与随机 rank-32 都出现该现象 | 判定 φ_P>10⁻⁵ 且 I<−10⁻⁵，分母为全部 1,024 位置；分量不利不能推出移除收益 |
| [共同原子活动与解码列谱](../figures/main05_sae_atom_activity.png) | 既定前 16 共同原子的各域激活频率／正幅值，64 解码列 SVD | 原子 24605 全域均激活；rank-32 保留所选解码列能量的 71.29% | 原子在 R 前按 F 活动选定；几何谱不是梯度、loss 或语义的解释率 |
| [梯度几何与响应相关](../figures/main06_gradient_geometry_vs_finite_heatmaps.png) | 四源均值梯度余弦与同 R 面板有限损失相关；原始／等范数 SVD 主方向导数响应相关 | 跨源参数余弦约 0.062–0.171，有限响应相关约 0.357–0.699；正交参数方向仍可有响应相关 | 相关是固定源、同面板的事后关系；不是语义因果或路由收益 |
| [累计主方向与有限响应](../figures/main07_gradient_components_response_heatmaps.png) | 原始／等范数源基的累计一阶量与有限 I 相关，以及两种源能量分母 | 原始第一主方向的作用恢复因来源而异；4 方向的总一阶量接近本次有限作用 | 只有 4 个域均值梯度，4 维恢复是张成空间闭合；没有测各分量自己的有限 loss |

每图同时有同名 `.svg`。SVG 使用字体路径，可在其他机器查看，不依赖字体安装。PNG 为 180 dpi。

## 附件辅助图

- [图 1：受控两点与区间](../figures/aux01_controlled_lines.png)。区间原样读取 `verdict.json`；主坐标保留 I=0，插图局部放大。连线只连接已测条件。
- [图 2：自然 16 格均值与比例](../figures/aux02_natural_mean_adverse.png)。条件区间固定来源、按记录分层抽样；增损与符号未定分别计数。
- [图 3：SAE 三项检查](../figures/aux03_sae_three_checks.png)。静态误差、动态比值和有限损失分量分轴展示。没有给现有 SAE 数据补造区间。

受控图支持答案规则对局部下降幅度的调节，未出现平均净增损。自然文本图显示领域均值改善可以与许多位置增损同时发生。SAE 图说明静态重构准确不能保证小位移忠实，共同方向的不利分量也出现在随机同秩对照中。它们仍没有回答长期训练中应该怎样分配共享 expert。

## 数据、复算和来源

- [绘图脚本](../scripts/build_existing_figures.py) 只读取既有数据，CPU 计算选定解码列谱，并读取另行授权的梯度审计输出；不载入语言模型、不调用 GPU。
- [来源记录](figures_provenance.json) 包含原始文件 SHA256、字段映射、样本量、聚合口径、检查点、源批次与输出 hash。附件三份 CSV 的 hash 全部一致。
- [自然主步 16 格](natural_cells_main16.csv) 包含精确均值、已有区间、增损／未定比例、步长、位置数量和死区；[全／半步](natural_cells_full_and_half.csv) 分开存放。32 格已与原事件数组核对，均值最大差小于 10⁻¹⁶ nat，比例完全一致。
- [受控 8 格](controlled_cells.csv)、[规则交互](controlled_rule_interaction.csv)、[SAE 静态](sae_static_reconstruction.csv)、[动态](sae_endpoint_pooled.csv)、[有限分量](sae_component_pooled.csv) 保留完整绘图口径。
- [64 个既定共同原子的活动](sae_selected_common_activity.csv) 和 [解码列谱](sae_selected_decoder_spectrum.csv) 为全部小表，图仅截取原选择排序前 16 个原子，没有按本次损失结果重新选原子。
- 梯度审计的 5 个 `gradient_*.csv`、recipe、receipt 与 summary 由独立新增审计保留；绘图不新增统计阈值。

自然逐位置事件仍保留在执行 owner 的 `runs/finite_panel_01/effects.npz` 与 `panel_metadata.npz`：后者的 `docs`、`positions`、`domains` 和 `part==1` 定位接收事件；前者的 `source__full_step`／`source__half_step` 给实际有限 CE 差。它们的路径、hash 和字段映射登记在来源记录，不复制进 Git。

字体是 `/tmp/1008_NotoSansCJKsc-Regular.otf` 外部运行依赖，未纳入仓库。重画时使用 `python scripts/build_existing_figures.py --font /path/to/NotoSansCJKsc-Regular.otf`（工作目录为本文件夹）。
