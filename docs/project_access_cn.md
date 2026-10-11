# 从 System 读取研究项目

[English](project_access.md)

System 与 `Projects/` 下的研究项目是独立仓库。只取得 System，不会同时取得 `from` 文件。
相对链接提供导航，不会复制另一个仓库。
本地项目配置的上游是 [BinaryCheater/from-attention-to-search](https://github.com/BinaryCheater/from-attention-to-search)，
分支为 `Xingyu`。本地修改只有在另行请求提交和推送后才会上游可见，读取仍需要相应仓库权限。

[资产库](../assets/README_cn.md)维护模型／SAE 检查点、保存表征和数据集的身份与存储地址，
并统一规定“先查找并实际访问，必需资产仍不可访问再暂停”的流程。
其中包含 `/data/share/109_cache_dir`、执行检查点、内嵌 SAE 权重及表征面板。
访问快照只代表检查时的主机、时间和用户上下文，不能保证另一个工作区或 GPU 任务也可访问。
数据集和检查点继续留在原存储位置，不纳入 System Git 或阅读包。

完整工作区中，优先读用户指定的文件。否则由 `PROJECTS.md` 选择项目，由项目 roadmap 选择
研究线路，再读需要的 Focus、Anchor 或 Summary。项目维护自己的研究入口，System 不再复制工作流表。
`python tools/check_current_entrypoints.py` 检查已跟踪入口；修改期间可用 `--working-tree` 检查现有文件，
并如实报告尚未跟踪的文件。路径通过检查不代表科学批准。

旧对话、凭据或归档中的路径可通过以下方式找到新位置：

```sh
python tools/research_paths.py daily_research_reports/0930/docs/domain_update_geometry/summary.md
```

`research_locations.json` 保存旧新路径、迁移前后摘要值、原仓库版本和原始字节归档位置。
链接重定位不修改注册设置、结果或批准。核对冻结哈希时使用原始字节，不拿调整过链接的 Markdown
冒充同一个文件版本。记忆、不可变凭据和历史快照保持原样；原始字节归档不是第二份现行原件。

环境无法访问项目时，明确说明未读到哪些来源，不凭项目名、System 索引或聊天补全。
能访问两个仓库就分别读取；否则在完整工作区生成本地阅读包：

```sh
python tools/build_reading_bundle.py --project from-attention-to-search --output /tmp/research-reading
```

默认跟随 roadmap 的当前 Focus 及其明确指向的设计、实验原件。
指定 `--source <相对System的路径.md>` 时，只收入所列文档、已有语言伴随稿、项目导航及引用的小型资产；
要增加记录就重复 `--source`，链接不会自动扩大文档范围。
加 `--zip` 可同时生成便携压缩包；输出目录和压缩包均不得已存在。
工具仅用 Python 标准库，不生成 HTML 页面，不需要浏览器接口或额外排版依赖。

直接用文本编辑器或 Markdown 阅读器打开 `README.md`，按所列顺序阅读。
入口同时给出包内路径，不依赖链接可点击。`documents/` 保存已调整为包内链接、附来源说明的
Markdown 阅读副本；`sources/` 保留包括原始链接在内的精确原始字节。
`manifest.json` 保存所选文件涉及的所有仓库版本、两类文件的哈希和未包含依赖。
`UNAVAILABLE.md` 区分缺失、未选入和超出范围的来源；未包含的本地链接指向这份说明，
不会默默跳向包外。

已有 Unknown 和草稿状态按原文保留，打包不确认措辞、不批准工作；修改研究仍回到原件。
清单覆盖 owner 字段、行内链接和单行引用式链接定义，其他代码路径保持字面文本。
不递归打包历史和执行数据。保留原有章节片段和 TeX 公式；阅读器不支持时按标题或文件路径定位，
通过文稿中的文字解释理解公式。工具不会自动补写缺失解释；写作按[文字规范](report_writing_cn.md)执行。

使用前核对 Markdown 与清单。缺失的执行数据、图件或历史来源仍是读取限制。
外部发送、协作同步和发布继续按各自请求范围处理。

Git 默认排除生成产物。精选的小型证据表、图和凭据可由项目清单逐项列出用途、来源和摘要值，
经过载荷检查后跟踪；原始运行目录、检查点和缓存继续排除。日期图不自动进入版本控制。
便携阅读包会携带选定且可取得的图片及来源，不能承诺被忽略的文件会随 Git 同步。
